import click
from .. import make_cli_class, pass_context


@click.command('docking', cls=make_cli_class(__file__))
@pass_context
def cli(ctx):
    pass
