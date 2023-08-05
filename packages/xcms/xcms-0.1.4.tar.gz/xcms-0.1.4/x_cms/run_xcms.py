import os
import shlex
import tempfile
import pybel
import subprocess32
import math

import numpy as np

from scipy.spatial.distance import euclidean
from scipy.stats import spearmanr
from parsers import PkcombuAtomMatchParser
from parsers import ApocResultParer


def squared_distance(coordsA, coordsB):
    """Find the squared distance between two 3-tuples"""
    sqrdist = sum((a - b)**2 for a, b in zip(coordsA, coordsB))
    return sqrdist


def contactVector(lig_coords, prt_coords):
    vec = [math.sqrt(squared_distance(c1, c2))
           for c1 in lig_coords for c2 in prt_coords]
    return vec


def readLigandCoords(path, mlist, format="sdf"):
    mol = pybel.readfile(format, path).next()
    mol.removeh()
    all_coords = [atom.coords for atom in mol if not atom.OBAtom.IsHydrogen()]
    coords = []
    for idx in mlist:
        coords.append(all_coords[idx - 1])

    return coords


def checkEnv():
    """check if pkcombu and apoc are properly installed
    """
    cmd_exists = lambda x: any(os.access(os.path.join(path, x), os.X_OK) for path in os.environ["PATH"].split(os.pathsep))
    assert cmd_exists('pkcombu'), "Cannot find pkcombu"
    assert cmd_exists('apoc'), "Cannot find apoc"


def runPkcombu(a_path, b_path, oam_path):
    FNULL = open(os.devnull, 'w')
    cmds = ["pkcombu", "-A", a_path, "-B", b_path, "-oam", oam_path]
    subprocess32.call(cmds, stdout=FNULL, stderr=subprocess32.STDOUT)


class ApocInput:
    def __init__(self, lig_path, prt_path, threshold=7.0):
        self.lig_path = lig_path
        self.prt_path = prt_path
        self.threshold = threshold

    def _cleanedPdb(self):
        with open(self.prt_path, 'r') as ifs:
            cleaned = set()
            for line in ifs:
                if len(line) > 53 and line[:6] == "ATOM  ":
                    atom_type = line[13:15]
                    if atom_type == "CA" or atom_type == "CB":
                        cleaned.add(line)
            cleaned = list(cleaned)
            cleaned = sorted(cleaned, key=lambda line: int(line[22:26]))
            cleaned.append("TER")
            return "".join(cleaned)

    def pocketSection(self):
        cleaned = self._cleanedPdb()
        prt = pybel.readstring("pdb", cleaned)
        if type(self.lig_path) is str and os.path.exists(self.lig_path):
            suffix = self.lig_path.split('.')[-1]
            lig = pybel.readfile(suffix, self.lig_path).next()
        elif type(self.lig_path) is pybel.Molecule:
            lig = self.lig_path
        else:
            raise Exception("Wrong input for ligand! Please check %s" %
                            self.lig_path)

        pkt_lines = []
        residues = set()
        for line, atom in zip(cleaned.split("\n")[:-1], prt.atoms):
            coords = atom.coords
            dists = [euclidean(coords, a.coords) for a in lig.atoms]
            if any([d < self.threshold for d in dists]):
                pkt_lines.append(line)
                res_num = int(line[22:26])
                residues.add(res_num)

        start_pkt_line = "\nPKT %d 1000 %s\n" % (len(residues),
                                                 lig.title.split('/')[-1])

        return start_pkt_line + "\n".join(pkt_lines) + "\nTER\n"

    def input4Apoc(self):
        cleaned = self._cleanedPdb()
        return cleaned + self.pocketSection()


class BioLipReferencedSpearmanR:
    def __init__(self, lig_path, prt_path):
        self.lig_path = lig_path
        self.prt_path = prt_path
        apoc_input = ApocInput(self.lig_path, self.prt_path, threshold=7.0)
        self.apoc_input = apoc_input.input4Apoc()
        self.pkt = apoc_input.pocketSection()
        suffix = lig_path.split('.')[-1]
        # only read the first molecule
        self.lig = pybel.readfile(suffix, self.lig_path).next()

    def alignProteins(self, pkt1, res1, pkt2, res2):
        def prt_coords(pkt):
            res_coords = {}
            for line in pkt.splitlines():
                if len(line) > 56:
                    fullname = line[12:16]
                    # get rid of whitespace in atom names
                    split_list = fullname.split()
                    name = ""
                    if len(split_list) != 1:
                        # atom name has internal spaces, e.g. " N B ", so
                        # we do not strip spaces
                        name = fullname
                    else:
                        # atom name is like " CA ", so we can strip spaces
                        name = split_list[0]
                    resseq = int(line[22:26].split()[0])  # sequence identifier
                    if name == "CA" or name == "CB":  # only count the backbone
                        residue_id = (name, resseq)
                        try:
                            x = float(line[30:38])
                            y = float(line[38:46])
                            z = float(line[46:54])
                            res_coords[residue_id] = np.array((x, y, z), "f")
                        except Exception as detail:
                            raise (detail)
            return res_coords

        def align(pc1, pc2, res1, res2):
            reorded_pc1, reorded_pc2 = [], []
            for r1, r2 in zip(res1, res2):
                if ("CA", r1) in pc1 and ("CA", r2) in pc2:
                    reorded_pc1.append(pc1[("CA", r1)])
                    reorded_pc2.append(pc2[("CA", r2)])
                if ("CB", r1) in pc1 and ("CB", r2) in pc2:
                    reorded_pc1.append(pc1[("CB", r1)])
                    reorded_pc2.append(pc2[("CB", r2)])
            return reorded_pc1, reorded_pc2

        pc1 = prt_coords(pkt1)
        pc2 = prt_coords(pkt2)
        pc1, pc2 = align(pc1, pc2, res1, res2)
        if len(pc1) != len(pc2):
            raise Exception("Unequal pocket residue number %d vs %d" %
                            (len(pc1), len(pc2)))
        else:
            return pc1, pc2

    def alignLigands(self, lig1, lig2):
        try:
            sdf1 = tempfile.mkstemp()[-1]
            sdf2 = tempfile.mkstemp()[-1]
            oam_path = tempfile.mkstemp()[-1]

            lig1.removeh()
            lig2.removeh()

            lig1.write("sdf", sdf1, overwrite=True)
            lig2.write("sdf", sdf2, overwrite=True)

            runPkcombu(sdf1, sdf2, oam_path)
            kcombu = PkcombuAtomMatchParser(oam_path)
            list1, list2 = kcombu.getMatchingSerialNums()
            c1 = readLigandCoords(sdf1, list1)
            c2 = readLigandCoords(sdf2, list2)
            return kcombu, c1, c2
        finally:
            os.remove(oam_path)
            os.remove(sdf1)
            os.remove(sdf2)

    def calculateAgainstOneSystem(self, ref_lig_path, ref_prt_path):
        """apply the XCMS calculation between identical systems
        Keyword Arguments:
        ref_lig_path -- file path, string
        ref_prt_path -- file path, string
        """
        # build native pocket, write to file
        ref_apoc_input = ApocInput(ref_lig_path, ref_prt_path, threshold=7.0)
        ref_pkt_path = tempfile.mkstemp()[1]
        with open(ref_pkt_path, 'w') as ofs:
            ofs.write(ref_apoc_input.input4Apoc())

        # align pockets
        pkt_path = tempfile.mkstemp()[1]
        with open(pkt_path, 'w') as ofs:
            ofs.write(self.apoc_input)
        cmd = "apoc -plen 1 %s %s" % (pkt_path, ref_pkt_path)
        args = shlex.split(cmd)
        apoc_result = subprocess32.check_output(args)
        apoc_parser = ApocResultParer(apoc_result)

        if apoc_parser.numPocketSections() == 1:
            pocket_alignment = apoc_parser.queryPocket()
            global_alignment = apoc_parser.queryGlobal()
            self_res = pocket_alignment.template_res
            ref_res = pocket_alignment.query_res

            pc1, pc2 = self.alignProteins(
                self.pkt, self_res, ref_apoc_input.pocketSection(), ref_res)
            suffix = ref_lig_path.split('.')[-1]
            native_lig = pybel.readfile(suffix, ref_lig_path).next()
            kcombu, lc1, lc2 = self.alignLigands(self.lig, native_lig)
            query_lig_atn, template_lig_atn = kcombu.getMatchingSerialNums()

            assert len(pc1) == len(pc2)
            non_euqal_cnts = 0
            for idx in range(len(pc1)):
                c1, c2 = pc1[idx], pc2[idx]
                if euclidean(c1, c2) > 0.01:
                    non_euqal_cnts += 1

            vec1 = contactVector(lc1, pc1)
            vec2 = contactVector(lc2, pc2)
            tc = kcombu.getTc()
            rho, pval = spearmanr(vec1, vec2)

            my_result = {
                "Tc": tc,
                "spearmanr": rho,
                "ps_score_pval": pocket_alignment.p_value,
                "num_binding_res": len(ref_res),
                "num_lig_atoms": len(lc1),
                "pval": pval,
                "ps_score": pocket_alignment.ps_score,
                "tc_times_ps": tc * pocket_alignment.ps_score,
                "TM-score": global_alignment.tm_score,
                "rmsd": global_alignment.rmsd,
                "seq_identity": global_alignment.seq_identity,
                "query_res": pocket_alignment.query_res,
                "query_lig_atom_num": query_lig_atn,
                "template_lig_atom_num": template_lig_atn,
                "template_res": pocket_alignment.template_res,
            }

        # free the resources
        os.remove(pkt_path)
        os.remove(ref_pkt_path)

        return my_result
