import click

from sblu.cli import pass_context


@click.command('piper', help="Helpful wrapper for PIPER.")
@pass_context
def cli(ctx):
    print("piper")
