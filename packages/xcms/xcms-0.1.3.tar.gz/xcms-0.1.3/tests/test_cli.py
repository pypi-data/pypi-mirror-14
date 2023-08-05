import pytest
from click.testing import CliRunner
from x_cms import run_xcms
from x_cms import parsers


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_with_checkenv():
    run_xcms.checkEnv()


def test_cli_with_calculate():
    q_lig = "./2yiw_YIW_A_1.pdb.pdbqt.vina.pdbqt"
    q_prt = "./2yiwA.pdb"
    t_lig = "./3f3u_1AW_A_1.pdb"
    t_prt = "./3f3uA.pdb"

    task = run_xcms.BioLipReferencedSpearmanR(q_lig, q_prt)
    result = task.calculateAgainstOneSystem(t_lig, t_prt)
    assert abs(result['TM-score'] - 0.756) < 0.001
    assert abs(result['ps_score'] - 0.698) < 0.001
    assert abs(result['spearmanr'] - 0.961) < 0.001
