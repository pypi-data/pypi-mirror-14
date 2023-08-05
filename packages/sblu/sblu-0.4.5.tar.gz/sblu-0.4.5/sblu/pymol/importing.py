import glob
from itertools import chain

from path import Path
from pymol import cmd

from .. import CONFIG

try:
    _str = basestring
except:
    _str = str


def cl_load_job(cluspro_id, coeffs=None, auto_group=True):
    """Load a ClusPro job into a PyMOL session.
    """
    if CONFIG['cluspro']['local_path'] is None:
        raise "ClusPro local path not configured"

    local_cache = Path(CONFIG['cluspro']['local_path']) / str(cluspro_id)
    group_auto_mode = cmd.get("group_auto_mode")

    if coeffs is None:
        ligs = glob.glob(str(local_cache / "model.???.??.pdb.gz"))
    else:
        if isinstance(coeffs, _str):
            coeffs = coeffs.split(" ")

        ligs = chain(*[glob.glob(local_cache /
                                 "model.{}.??.pdb.gz".format(coeff))
                       for coeff in coeffs])

    for lig in ligs:
        coeff, translation = Path(lig).basename().split(".")[1:3]
        lig_name = "lig.{}.{}.pdb".format(coeff, translation)
        new_lig_name = "{}.lig.{}.{}".format(cluspro_id, coeff, translation)

        cmd.load(lig)

        if auto_group:
            cmd.set_name(lig_name, new_lig_name)
            cmd.set("group_auto_mode", 2)
            cmd.group("{}.lig.{}".format(cluspro_id, coeff),
                      "{}.lig.{}.{}".format(cluspro_id, coeff, translation),
                      "auto")
            cmd.set("group_auto_mode", 0)

    cmd.delete("rec.pdb")
    cmd.load(local_cache / "rec.pdb.gz", "{}.rec".format(cluspro_id))
    if auto_group:
        cmd.group(str(cluspro_id), "{}.rec".format(cluspro_id), "auto")

    cmd.set("group_auto_mode", group_auto_mode)

    if auto_group:
        cmd.order("{}.*".format(cluspro_id), "yes")
        cmd.show_as("cartoon", str(cluspro_id))
    cmd.orient("{}.rec".format(cluspro_id))

# Register extensions
cmd.extend('cl_load_job', cl_load_job)
