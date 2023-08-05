import click

from sblu.cli import pass_context


@click.command('psfgen', short_help="Helpful wrapper for psfgen")
@click.argument("segments", nargs=-1, type=click.Path(exists=True))
@click.option("--link")
@click.option("--first")
@click.option("--last")
@click.option("--smod", default="")
@click.option("--wdir")
@click.option("--psfgen", default="psfgen")
@click.option("--nmin", default="nmin")
@click.option("--prm")
@click.option("--rtf")
@click.option("--auto-disu/--no-auto-disu", default=True)
@click.option("--xplor-psf/--no-xplor-psf", default=False)
@click.option("--osuffix")
@pass_context
def cli(ctx,
        segments, psfgen, nmin):
    """Generate a PSF file from pdb files"""
    ctx.log("Not implemented yet")
