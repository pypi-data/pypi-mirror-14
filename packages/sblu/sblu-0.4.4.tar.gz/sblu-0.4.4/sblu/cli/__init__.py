import os
import sys
import click
from click import Context as _Context

CONTEXT_SETTINGS = dict(auto_envvar_prefix='COMPLEX')


class Context(_Context):

    def __init__(self):
        self.verbosity = 0
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbosity > 0:
            self.log(msg, *args)

pass_context = click.make_pass_decorator(Context, ensure=True)


def make_cli_class(package):
    cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              package))

    class ComplexCLI(click.MultiCommand):

        def list_commands(self, ctx):
            rv = []
            for filename in os.listdir(cmd_folder):
                if filename.endswith('.py') and \
                   filename.startswith('cmd_'):
                    rv.append(filename[4:-3])
            rv.sort()
            return rv

        def get_command(self, ctx, name):
            try:
                if sys.version_info[0] == 2:
                    name = name.encode('ascii', 'replace')
                mod = __import__('sblu.cli.{0}.cmd_{1}'.format(package, name),
                                 None, None, ['cli'])
            except ImportError:
                return
            return mod.cli

    return ComplexCLI
