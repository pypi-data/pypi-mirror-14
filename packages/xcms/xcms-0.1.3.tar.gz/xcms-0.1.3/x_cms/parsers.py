import re


class Data:
    pass


class ApocResultParer:
    def __init__(self, content):
        self._content = content
        self.has_pocket_alignment = False

        self.global_sections = re.findall(
            r'''>>>>>>>>>>>>>>>>>>>>>>>>>   Global alignment   <<<<<<<<<<<<<<<<<<<<<<<<<<(.*?)seconds''',
            content, re.DOTALL)

        self.pocket_sections = re.findall(
            r'''>>>>>>>>>>>>>>>>>>>>>>>>>   Pocket alignment   <<<<<<<<<<<<<<<<<<<<<<<<<<(.*?)seconds''',
            content, re.DOTALL)

        if len(self.pocket_sections) > 0:
            self.has_pocket_alignment = True

        self._read_global()
        self._read_pocket()

    def hasPocketAlignment(self):
        return self.has_pocket_alignment

    def numPocketSections(self):
        return len(self.pocket_sections)

    def getContent(self):
        return self._content

    def _read_global(self):
        self.global_alignments = {}
        for string in self.global_sections:
            data = Data()
            for line in string.splitlines():
                if "Structure 1" in line:
                    data.structure_1 = line.split()[2].split('.')[0]
                if "Structure 2" in line:
                    data.structure_2 = line.split()[2].split('.')[0]
                if "TM-score" in line:
                    data.tm_score = float(line.split()[-1])
                if "RMSD" in line and "Seq identity" in line:
                    data.rmsd = float(line.split(',')[0].split()[-1])
                    data.seq_identity = float(line.split(',')[-1].split()[-1])
            key = data.structure_1 + " " + data.structure_2
            self.global_alignments[key] = data

    def _read_pocket(self):
        self.pocket_alignmets = {}
        for string in self.pocket_sections:
            data = Data()
            data.has_pocket_alignment = False
            data.template_res, data.query_res = [], []

            matching_section = re.findall(
                r'''Match List(.*?)Scoring parameters''', string, re.DOTALL)

            if len(matching_section) == 1:
                for line in matching_section[0].splitlines():
                    tokens = line.split()
                    if tokens and tokens[0].isdigit():
                        data.has_pocket_alignment = True
                        data.template_chainid = tokens[1]
                        data.query_chainid = tokens[4]
                        data.template_res.append(int(tokens[2]))
                        data.query_res.append(int(tokens[5]))

            for line in string.splitlines():
                if "Structure 1" in line and "Pocket:" in line:
                    data.tname = line.split()[-1].split(':')[-1]
                if "Structure 2" in line and "Pocket:" in line:
                    data.qname = line.split()[-1].split(':')[-1]
                if "PS-score" in line:
                    data.ps_score = float(line.split(',')[0].split("=")[-1])
                    data.p_value = float(line.split(',')[1].split("=")[-1])
                    data.z_score = float(line.split(',')[2].split("=")[-1])
                if "RMSD" in line and "Seq identity" in line:
                    data.rmsd = float(line.split(',')[0].split()[-1])
                    data.seq_identity = float(line.split(',')[-1].split()[-1])

            key = data.tname + " " + data.qname
            self.pocket_alignmets[key] = data

    def queryGlobal(self, tname="", qname=""):
        if tname == "" and qname == "":
            """by default return the first pocket alignment
            """
            return self.global_alignments.values()[0]
        else:
            structure_1 = tname.split('_')[0] + tname.split('_')[2]
            structure_2 = qname.split('_')[0] + qname.split('_')[2]
            return self.global_alignments[structure_1 + " " + structure_2]

    def queryPocket(self, tname="", qname=""):
        if tname == "" and qname == "":
            """by default return the first pocket alignment
            """
            return self.pocket_alignmets.values()[0]
        else:
            try:
                key = tname + " " + qname
                return self.pocket_alignmets[key]
            except:
                raise KeyError, "Can not find pockets for %s and %s" % (tname,
                                                                        qname)

    def writeProteinMatchingList(self, tname, qname, ofn):
        try:
            pocket_alignment = self.queryPocket(tname, qname)
            with open(ofn, 'w') as ofs:
                ofs.write("%s %s\n" % (pocket_alignment.template_chainid,
                                       pocket_alignment.query_chainid))
                for t_res_id, q_res_id in zip(pocket_alignment.template_res,
                                              pocket_alignment.query_res):
                    ofs.write("%d %d\n" % (t_res_id, q_res_id))
        except:
            raise KeyError("cannot find pocket alignment for between %s and %s"
                           % (tname, qname))


class PkcombuAtomMatchParser:
    def __init__(self, oam_fn):
        f = open(oam_fn, 'r')
        self.content = f.read()
        f.close()

        self.data = Data()

        for line in self.content.splitlines():
            if "tanimoto" in line:
                self.data.tanimoto = float(line.split()[-1])

    def getTc(self):
        return self.data.tanimoto

    def _readPdbMatchingSerialNums(self):
        lines = self.content.splitlines()
        list_a, list_b = [], []
        for line in lines:
            if line[0].isdigit():
                tokens = line.split()
                list_a.append(int(tokens[2]))
                list_b.append(int(tokens[3]))

        return list_a, list_b

    def getMatchingSerialNums(self):
        return self._readPdbMatchingSerialNums()

    def writeMatchingSerialNums(self, ofn):
        list_a, list_b = self._readPdbMatchingSerialNums()
        with open(ofn, 'w') as ofs:
            for a, b in zip(list_a, list_b):
                ofs.write("%d %d\n" % (a, b))
