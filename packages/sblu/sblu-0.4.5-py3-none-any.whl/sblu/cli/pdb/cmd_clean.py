import click
from sblu.pdb import (parse_pdb_stream, fix_atom_records,
                      SKIP_RESIDUES, RESNAME_FIXES, RECORD_FIXES)
from sblu.cli import pass_context


@click.command('clean', short_help="Clean a PDB file.")
@click.argument("pdb_file", type=click.File(mode='r'))
@click.option("--all-het-to-atom",
              is_flag=True,
              help="Change all HETATM records to ATOM")
@click.option("--no-skips",
              is_flag=True,
              help="Skip the following residues: " + " ".join(SKIP_RESIDUES))
@click.option(
    "--no-record-fixes",
    is_flag=True,
    help="Change the record_type to ATOM for the following residues: " +
    " ".join(RECORD_FIXES))
@click.option("--no-resname-fixes",
              is_flag=True,
              help="Fix the following residue names:\n" + "\n".join([
                  '\t{} -> {}'.format(k, v) for k, v in list(RESNAME_FIXES.items())
              ]))
@click.option("--outfile",
              type=click.File(mode='w'),
              default=click.open_file('-', 'w'))
@pass_context
def cli(ctx,
        pdb_file, all_het_to_atom, no_skips, no_record_fixes,
        no_resname_fixes, outfile):
    records = fix_atom_records(parse_pdb_stream(pdb_file),
                               no_skips=no_skips,
                               all_het_to_atom=all_het_to_atom,
                               no_record_fixes=no_record_fixes,
                               no_resname_fixes=no_resname_fixes)

    for record in records:
        outfile.write(str(record))
