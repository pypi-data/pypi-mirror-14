import os
import click
from sblu.pdb import parse_pdb_stream
from sblu.cli import pass_context

from . import _splitsegs


@click.command('splitsegs', short_help="Split a PDB into segments suitable for psfgen.")
@click.argument("pdb_file", type=click.File(mode='r'))
@click.option("--renum", is_flag=True, help="Renumber residues")
@click.option("--segid/--no-segid", default=True)
@click.option("--output-prefix",
              default=None,
              help="Use this prefix for the output files.")
@pass_context
def cli(ctx,
        pdb_file, renum, segid, output_prefix):
    records = parse_pdb_stream(pdb_file)

    if output_prefix is None:
        if pdb_file.name != "<stdin>":
            output_prefix = os.path.splitext(pdb_file.name)[0]
        else:
            output_prefix = "split_pdb"

    return _splitsegs(records, renum, segid, output_prefix)
