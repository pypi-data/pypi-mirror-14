import os
import sys
import tempfile
import subprocess
from itertools import combinations
from collections import OrderedDict

import click
from path import Path

from sblu import PRMS_DIR
from sblu.pdb import parse_pdb_stream, fix_atom_records
from sblu.cli import pass_context


@click.command('select', short_help="Select atoms from a PDB file.")
@click.argument("pdb_file", type=click.File(mode='r'))
@click.option("--selection")
@pass_context
def cli(ctx, pdb_file, selection):
    pass
