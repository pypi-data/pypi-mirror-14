"""
Test reading and applying ftresults.
"""

from . import DATA_DIR

from sblu import ft
from nose.tools import ok_, eq_


def test_read_ftresults():
    ftresults = ft.read_ftresults(DATA_DIR / "ft/ft.test")

    eq_(len(ftresults), 10, "Incorrect number of ftresults")


def test_read_rotations():
    rotations = ft.read_rotations(DATA_DIR / "prms/rotation_test_set.mol2")

    eq_(len(rotations), 10, "Incorrect number of rotations")


def test_get_ftresult():
    ftresult = ft.get_ftresult(DATA_DIR / "ft/ft.test", 0)

    eq_(ftresult['roti'], 9)
    ok_((ftresult['tv'] == [1.0, 11.0, -21.0]).all())
    eq_(ftresult['E'], -451.6)
