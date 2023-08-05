import subprocess

import click

from sblu.cli import pass_context
from sblu import PRMS_DIR


@click.command('pdb_psf_concat', short_help="Join two or more PDB/PSF file pairs together.")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--psfgen", default="psfgen")
@click.option("--prefix")
@click.option("--rtf")
@pass_context
def cli(ctx,
        files, psfgen, prefix, rtf):
    def construct_prefix(psf_files):
        prefix = ""
        for f in files:
            prefix += f.namebase
        return prefix

    def psf_concat(psf_files, rtf_file, prefix, psfgen="psfgen"):
        p = subprocess.Popen([psfgen],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        commands = ""
        commands += "topology {}\n".format(rtf_file)

        for psf_file in psf_files:
            commands += "readpsf {}\n".format(psf_file)

        commands += "writepsf charmm {0}.psf\n".format(prefix)

        p.communicate(commands.encode())

    def pdb_concat(pdb_files, prefix):
        atomi = 0
        with open("{}.pdb".format(prefix), "w") as out_file:
            for pdb in pdb_files:
                last_res_id = ""
                with open(pdb) as in_file:
                    for line in in_file:
                        if line.startswith("ATOM  "):
                            atomi += 1
                            res_id = line[22:27]
                            if atomi >= 99900 and last_res_id != res_id:
                                atomi = 1

                            last_res_id = res_id
                            line = "{0}{1:5d}{2}".format(line[0:6],
                                                         atomi, line[11:])
                        elif line.startswith("HEADER"):
                            atomi = 0
                        if not line.startswith("END"):
                            out_file.write(line)

    if len(files) < 4 or len(files) % 2 != 0:
        raise click.ClickException("Requires at least two pairs of files")

    psf_files = files[::2]
    pdb_files = files[1::2]

    if rtf is None:
        rtf = PRMS_DIR / "pdbamino.rtf"

    if prefix is None:
        prefix = construct_prefix(psf_files)

    psf_concat(psf_files, rtf, prefix, psfgen)
    pdb_concat(pdb_files, prefix)
