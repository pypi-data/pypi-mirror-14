from signal import signal, SIGPIPE, SIG_DFL

import click
from prody import confProDy, LOGGER

from . import pass_context, make_cli_class
from .. import __version__

from .util import config


def make_subcommand(package):
    @click.command(package, cls=make_cli_class(package))
    @pass_context
    def cli(ctx):
        pass
    return cli


@click.group('sblu')
@click.option('-v', '--verbose', count=True)
@click.version_option(version=__version__)
@pass_context
def cli(ctx, verbose):
    signal(SIGPIPE, SIG_DFL)
    LOGGER._setverbosity(confProDy('verbosity'))

    ctx.verbosity = verbose


for subcommand in ('pdb', 'docking', 'measure', 'cluspro'):
    sub_cli = make_subcommand(subcommand)
    cli.add_command(sub_cli)

cli.add_command(config)
