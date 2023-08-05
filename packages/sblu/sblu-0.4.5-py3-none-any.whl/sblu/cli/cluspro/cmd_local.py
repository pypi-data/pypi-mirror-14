import click

from sblu import CONFIG
from sblu.cli import pass_context


@click.command('local', short_help="Run ClusPro docking locally.")
@click.argument("rec")
@click.argument("lig")
@click.option('-m', "--mode", default='enzyme',
              type=click.Choice(['enzyme', 'other', 'antibody']))
@pass_context
def cli(ctx):
    pass
