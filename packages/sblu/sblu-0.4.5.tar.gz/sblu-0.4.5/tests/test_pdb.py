from sblu.pdb import parse_pdb, is_atomic, fix_atom_records
from . import DATA_DIR
import pytest

try:
    from itertools import izip as zip
except ImportError:
    pass

with open(DATA_DIR / "pdb_list") as f:
    pdbs = [l.strip().split()[0] for l in f]


@pytest.mark.parametrize("pdb", pdbs)
def test_parse_pdb(pdb):
    pdb_file = DATA_DIR / "pdb" / (pdb + ".pdb")

    parsed = parse_pdb(pdb_file)
    with open(pdb_file) as f:
        for actual, expected in zip(parsed, filter(is_atomic, f)):
            assert str(actual) == expected


@pytest.mark.parametrize("pdb", pdbs)
def test_fix_atom_records(pdb):
    pdb_file = DATA_DIR / "pdb" / (pdb + ".pdb")
    expected_file = DATA_DIR / "pdb" / (pdb + ".clean.pdb")

    parsed = parse_pdb(pdb_file)
    fixed = fix_atom_records(parsed)

    with open(expected_file, 'r') as f:
        for actual, expected in zip(fixed, filter(is_atomic, f)):
            assert str(actual) == expected
