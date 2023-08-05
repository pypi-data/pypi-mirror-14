import logging
import os
import pkgutil
from subprocess import call

import click

from tumdlr.config import load_config, write_user_config

CONTEXT_SETTINGS = dict(auto_envvar_prefix='TUMDLR', max_content_width=100)


class Context(object):
    """
    CLI Context
    """
    def __init__(self):
        self.cookiejar      = None
        self.config         = load_config('tumdlr')
        self.config_path    = None
        self.log            = None
        self.cache          = True
        self.database       = NotImplemented


class CommandLine(click.MultiCommand):

    def list_commands(self, ctx):
        """
        Get a list of all available commands

        Args:
            ctx: Context

        Returns:
            list
        """
        commands_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'commands')
        command_list = [name for __, name, ispkg in pkgutil.iter_modules([commands_path]) if not ispkg]
        command_list.sort()
        return command_list

    def get_command(self, ctx, name):
        """
        Fetch a command module

        Args:
            ctx:        Context
            name(str):  Command name
        """
        try:
            mod = pkgutil.importlib.import_module('tumdlr.commands.{name}'.format(name=name))
            return mod.cli
        except (ImportError, AttributeError):
            raise


pass_context = click.make_pass_decorator(Context, ensure=True)


# noinspection PyIncorrectDocstring
@click.command(cls=CommandLine, context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--config', type=click.Path(dir_okay=False, resolve_path=True), envvar='TUMDLR_CONFIG_PATH',
              default='~/.config/tumdlr/tumdlr.conf',
              help='Path to the TumDLR configuration file (currently does nothing)')
@click.option('-q', '--quiet', help='Silence all output except for fatal errors', is_flag=True)
@click.option('-d', '--debug', help='Output information used for debugging', is_flag=True)
@pass_context
def cli(ctx, config, quiet, debug):
    """
    Tumblr Downloader CLI utility
    """
    # Logging setup
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.CRITICAL if quiet else logging.WARN

    ctx.log = logging.getLogger('tumdlr')
    ctx.log.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(logging.Formatter('[%(levelname)s] %(name)s: %(message)s'))
    ctx.log.addHandler(ch)

    # First run?
    if not ctx.config['Development'].getboolean('AgreedToTerms'):
        first_run(ctx)


def first_run(ctx):
    """
    Run the setup and other tasks for first-time use

    Args:
        ctx(Context)
    """
    terms_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'TERMS.rst')

    # Display the welcome message / terms and conditions agreement
    if os.name == 'nt':
        call(['more', terms_path])
    else:
        call(['less', terms_path])

    # Run the configuration setup
    save_path = click.prompt('Where should Tumblr downloads be saved to?', os.path.expanduser('~/tumblr'))

    config = {
        'Tumdlr': {
            'SavePath': save_path,
        },
        'Development': {
            'AgreedToTerms': True
        }
    }

    path = write_user_config('tumdlr', None, **config)
    ctx.config = load_config('tumdlr')
    click.echo('Configuration written to {}'.format(path))


if __name__ == '__main__':
    cli()
