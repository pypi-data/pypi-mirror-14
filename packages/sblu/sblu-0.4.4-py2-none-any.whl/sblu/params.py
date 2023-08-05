"""Parse lab parameter files"""
import re

MODE_RE = re.compile(r"""NBON|NONB|VOLUME|HBOND|BOND|ANGL|THETA|IMPR|IMPHI|DIHE|PHI|NBFIX""")


def read_atom_param(filepath):
    with open(filepath, "r") as f:
        return read_atom_param_stream(f)


def read_atom_param_stream(stream):
    params = {'version': None, 'atoms': {}, 'pwpot': {}}

    for l in iter(stream):
        ss = l.strip().split()
        if ss:
            rec_type = ss[0]

            if rec_type == "version":
                params['version'] = ss[1]
            if rec_type == "atom":
                major, minor = ss[2], ss[3]
                pwpot_id = ss[4]
                radius = float(ss[5])
                charge = float(ss[6])

                params['atoms'][(major, minor)] = {
                    "pwpot_id": pwpot_id,
                    "radius": radius,
                    "charge": charge
                }

    return params


def read_charmm_topology(filepath):
    with open(filepath, "r") as f:
        return read_charmm_topology_stream(f)


def read_charmm_topology_stream(stream):
    pass


def read_charmm_prm(filepath):
    with open(filepath, "r") as f:
        return read_charmm_prm_stream(f)


def read_charmm_prm_stream(stream):
    def is_mode_line(l):
        return MODE_RE.match(l)

    def parse_bond(line):
        t0, t1, k, l0 = line.split()
        return (t0, t1, float(k), float(l0))

    def parse_angle(line):
        pass

    def parse_dihedral(line):
        pass

    def parse_improper(line):
        pass

    params = {}

    for l in iter(stream):
        if is_mode_line(l):
            mode = get_mode(l)
            continue

        if mode == BOND_MODE:
            parse_bond(l)
