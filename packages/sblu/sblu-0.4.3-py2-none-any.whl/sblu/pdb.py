"""This module contains functions for parsing and manipulating PDB files
"""
import numpy as np
import sys
import re

if sys.version_info < (3, 0):
    
    pass

RECORD_FIELD = slice(0, 6)

# yapf: disable
RECORD_TYPES = (
    # Title section
    "HEADER", "SOURCE", "AUTHOR",
    "OBSLTE", "KEYWDS", "REVDAT",
    "TITLE ", "EXPDTA", "SPRSDE",
    "SPLT  ", "NUMMDL", "JRNL  ",
    "CAVEAT", "MDLTYP", "REMARKS",
    "COMPND",
    # Primary structure section
    "DBREF ", "SEQADV", "MODRES",
    "DBREF1", "DBREF2", "SEQRES",
    # Heterogen Section
    "HET   ", "HETNAM", "HETSYN",
    "FORMUL",
    # Secondary structure section
    "HELIX ", "SHEET ",
    # Connectivity annotation section
    "SSBOND", "LINK  ", "CISPEP",
    # Miscellaneous features section
    "SITE  ",
    # Crystallographic and coordinate transformation section
    "CRYST1", "ORIGXn", "SCALEn",
    "MTRIXn",
    # Coordinate section
    "MODEL ", "ANISOU", "HETATM",
    "ATOM  ", "TER   ", "ENDMDL",
    # Connectivity section
    "CONECT",
    # Bookkeeping section
    "MASTER", "END   "
)

SKIP_RESIDUES = (
    "HOH",
    "WAT",
    "ACE",
    "NME"
)
# yapf: enable

RECORD_FIXES = ("MSE",  # selenomethionine
                "PTR",  # phosphotyrosine
                "HRG",  # homoarginine
                "DPP",  # diaminopropanoic acid
                "HSD",  # his protonation
                )
RESNAME_FIXES = {
    "ASH": "ASPH",
    "GLH": "GLUH",
    "CYX": "CYS",
    "HIP": "HSC",
    "HID": "HIS",
    "HIE": "HSD",
    "NGL": "GLYP",  # really NGLY
    "NPR": "PROP",  # really NPRO
    "UNK": "ALA",  # treat unknown residues as alanine
}
ATOM_NAME_FIXES = {"OCT1": " O  "}

# Atom Fields
ATOM_SERIAL_FIELD = slice(6, 11)
ATOM_NAME_FIELD = slice(12, 16)
ATOM_ALTLOC_FIELD = slice(16, 17)
ATOM_RESNAME_FIELD = slice(17, 20)
ATOM_CHAIN_FIELD = slice(21, 22)
ATOM_RESNUM_FIELD = slice(22, 26)
ATOM_ICODE_FIELD = slice(26, 27)
ATOM_XCOORD_FIELD = slice(30, 38)
ATOM_YCOORD_FIELD = slice(38, 46)
ATOM_ZCOORD_FIELD = slice(46, 54)
ATOM_OCCUPANCY_FIELD = slice(54, 60)
ATOM_BETA_FIELD = slice(60, 66)
ATOM_SEGMENT_FIELD = slice(72, 76)
ATOM_ELEMENT_FIELD = slice(76, 78)
ATOM_CHARGE_FIELD = slice(78, 80)


def _field_parser(_slice, _type=str):
    def _parser(line):
        return _type(line[_slice]) if len(line) > _slice.start else _type()

    return _parser


ATOM_FIELDS = {
    'record': _field_parser(RECORD_FIELD),
    'serial': _field_parser(ATOM_SERIAL_FIELD, int),
    'name': _field_parser(ATOM_NAME_FIELD),
    'altloc': _field_parser(ATOM_ALTLOC_FIELD),
    'resname': _field_parser(ATOM_RESNAME_FIELD),
    'chain': _field_parser(ATOM_CHAIN_FIELD),
    'resnum': _field_parser(ATOM_RESNUM_FIELD, int),
    'icode': _field_parser(ATOM_ICODE_FIELD),
    'x': _field_parser(ATOM_XCOORD_FIELD, float),
    'y': _field_parser(ATOM_YCOORD_FIELD, float),
    'z': _field_parser(ATOM_ZCOORD_FIELD, float),
    'occupancy': _field_parser(ATOM_OCCUPANCY_FIELD, float),
    'beta': _field_parser(ATOM_BETA_FIELD, float),
    'segment': _field_parser(ATOM_SEGMENT_FIELD),
    'element': _field_parser(ATOM_ELEMENT_FIELD),
    'charge': _field_parser(ATOM_CHARGE_FIELD),
}

ATOM_RECORD_FORMAT = ("{record:<6s}{serial:5d} {name:4s}{altloc:1s}"
                      "{resname:3s} {chain:1s}{resnum:4d}{icode:1s}"
                      "   {x:8.3f}{y:8.3f}{z:8.3f}{occupancy:6.2f}"
                      "{beta:6.2f}      {segment:<4s}{element:>2s}"
                      "{charge:2s}\n")


class PDBRecord(dict):
    RECORD_TYPE_REGEX = re.compile(r'is_([a-zA-Z])_line', re.I)

    def __init__(self, line):
        super(PDBRecord, self).__init__()
        self.record_type = line[RECORD_FIELD]
        self.line = line

    def __getattr__(self, name):
        m = PDBRecord.RECORD_TYPE_REGEX.match(name)
        if m:
            return lambda: m.group(1).upper() == self.record_type.strip()

        raise AttributeError(name)

    def __repr__(self):
        return self.line

    def __str__(self):
        return self.line


class AtomRecord(PDBRecord):
    def __init__(self, line):
        super(AtomRecord, self).__init__(line)
        for field_name, field_parser in list(ATOM_FIELDS.items()):
            self[field_name] = field_parser(line)

        self.coords = np.array([self.x, self.y, self.z])

    def __getattr__(self, name):
        if name in self:
            return self[name]
        return super(AtomRecord, self).__getattr__(name)

    def __setattr__(self, name, val):
        if name in self:
            self[name] = val
        else:
            super(AtomRecord, self).__setattr__(name, val)

    def __repr__(self):
        return ATOM_RECORD_FORMAT.format(**self)[:26]

    def __str__(self):
        return ATOM_RECORD_FORMAT.format(**self)


class EndRecord(PDBRecord):
    def __init__(self):
        self.line = "END\n"


def is_atomic(line):
    return line[RECORD_FIELD] in ("ATOM  ", "HETATM")


def parse_pdb(pdb_file, only_atoms=True, chains=None):
    """Return an iterator of records from a PDB file.

    Since the return is an iterator, if you need to go through the records more
    than once you should call it like

        list(parse_pdb(filename))
    """
    with open(pdb_file) as f:
        for record in parse_pdb_stream(f, only_atoms, chains):
            yield record


def parse_pdb_stream(pdb_stream, only_atoms=True, chains=None):
    """Return an iterator of records from a stream object.

    Since the return is an iterator, if you need to go through the records more
    than once you should call it like

        list(parse_pdb(filename))
    """
    for l in pdb_stream:
        if is_atomic(l) and (not chains or l[ATOM_CHAIN_FIELD] in chains):
            yield AtomRecord(l)
        elif not only_atoms:
            yield PDBRecord(l)


def fix_atom_records(records,
                     no_skips=False,
                     all_het_to_atom=False,
                     no_record_fixes=False,
                     no_resname_fixes=False):
    """Apply common fixes to records.

    For additional fixes, write a function similar to this one with
    the fixes you need.
    """
    for record in records:
        if record.record not in ('ATOM  ', 'HETATM'):
            yield record

        if not no_skips and record.resname in SKIP_RESIDUES:
            continue

        fix_record = (all_het_to_atom or
                      (not no_record_fixes and record.resname in RECORD_FIXES))
        if fix_record:
            record.record = 'ATOM  '

        if not no_resname_fixes and record.resname in RESNAME_FIXES:
            record.resname = RESNAME_FIXES[record.resname]

        if record.name in ATOM_NAME_FIXES:
            record.name = ATOM_NAME_FIXES[record.name]

        yield record


def split_segments(records, add_segid=False, only_atoms=True):
    """Split records into segments.

    A segment ends whenever a chain ends, a TER or END record is encountered,
    we change from ATOM to HETATM or vice verse, or a break in a chain is
    detected.
    """
    segid = 0
    last_atom_record = None
    segment = []

    def end_segment(record):
        if last_atom_record is None:
            return False

        if record.record_type in ("TER   ", "END   "):
            return True

        resnum_delta = record.resnum - last_atom_record.resnum

        return (
            (resnum_delta not in (0, 1)) or
            (resnum_delta == 0 and last_atom_record.icode != record.icode) or
            (record.record_type == "HETATM" and
             last_atom_record.resname != record.resname) or
            (last_atom_record.record_type == "HETATM" and
             last_atom_record.resname != record.resname) or
            (record.chain != last_atom_record.chain))

    for record in records:
        # Must do this first, or we may accidentally end segments
        if record.record_type in ("ATOM  ", "HETATM"):
            if record.chain == ' ':
                record.chain = 'x'

        if end_segment(record):
            if last_atom_record.record_type == "HETATM":
                chain = "h{}".format(last_atom_record.resname.strip())
            else:
                chain = last_atom_record.chain

            yield (segid, chain, segment)
            segment = []
            segid += 1
        if record.record_type in ("ATOM  ", "HETATM"):
            if add_segid:
                record.segment = segid

            last_atom_record = record
            segment.append(record)
        elif not only_atoms:
            segment.append(record)

    if last_atom_record.record_type == "HETATM":
        chain = "h{}".format(last_atom_record.resname.strip())
    else:
        chain = last_atom_record.chain
    yield (segid, chain, segment)


def get_disulfide_pairs(pdb_files):
    pass
