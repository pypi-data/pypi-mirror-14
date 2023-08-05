import click

from sblu.cli import pass_context


@click.command('piper', help="Helpful wrapper for PIPER.")
@pass_context
def cli(ctx):
    cmd.append(PIPER_BIN)

    for option in options:
        cmd.append(option)
    for flag in flags:
        cmd.append(flag)

    cmd += [rec, lig]
    print((" ".join(cmd)))
