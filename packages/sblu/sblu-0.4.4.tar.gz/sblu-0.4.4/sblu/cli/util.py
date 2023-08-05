import click

from .. import CONFIG


@click.command()
def config():
    print("\n".join(CONFIG.write()))
