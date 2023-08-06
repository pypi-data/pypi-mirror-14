import os
import sys
import traceback

import click

from .io import error
from .config import read_global_config
from planemo import __version__

PYTHON_2_7_COMMANDS = ["cwl_run", "cwl_script"]
IS_PYTHON_2_7 = sys.version_info[0] == 2 and sys.version_info[1] >= 7


CONTEXT_SETTINGS = dict(auto_envvar_prefix='PLANEMO')
COMMAND_ALIASES = {
    "l": "lint",
    "t": "test",
    "s": "serve",
}


class Context(object):

    def __init__(self):
        self.home = os.getcwd()
        self._global_config = None
        # Will be set by planemo CLI driver
        self.verbose = False
        self.planemo_config = None
        self.planemo_directory = None

    @property
    def global_config(self):
        if self._global_config is None:
            self._global_config = read_global_config(self.planemo_config)
        return self._global_config

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args, **kwds):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)
            if kwds.get("exception", False):
                traceback.print_exc(file=sys.stderr)

    @property
    def workspace(self):
        if not self.planemo_directory:
            raise Exception("No planemo workspace defined.")
        workspace = self.planemo_directory
        if not os.path.exists(workspace):
            os.makedirs(workspace)
        if not os.path.isdir(workspace):
            template = "Planemo workspace directory [%s] unavailable."
            message = template % workspace
            raise Exception(message)
        return workspace


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))


def list_cmds():
    rv = []
    for filename in os.listdir(cmd_folder):
        if filename.endswith('.py') and \
           filename.startswith('cmd_'):
            rv.append(filename[len("cmd_"):-len(".py")])
    rv.sort()
    if not IS_PYTHON_2_7:
        for command in PYTHON_2_7_COMMANDS:
            rv.remove(command)
    return rv


def name_to_command(name):
    try:
        if sys.version_info[0] == 2:
            name = name.encode('ascii', 'replace')
        mod_name = 'planemo.commands.cmd_' + name
        mod = __import__(mod_name, None, None, ['cli'])
    except ImportError as e:
        error("Problem loading command %s, exception %s" % (name, e))
        return
    return mod.cli


class PlanemoCLI(click.MultiCommand):

    def list_commands(self, ctx):
        return list_cmds()

    def get_command(self, ctx, name):
        if name in COMMAND_ALIASES:
            name = COMMAND_ALIASES[name]
        return name_to_command(name)


@click.command(cls=PlanemoCLI, context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@click.option('--config',
              default="~/.planemo.yml",
              envvar="PLANEMO_GLOBAL_CONFIG_PATH",
              help="Planemo configuration YAML file.")
@click.option('--directory',
              default="~/.planemo",
              envvar="PLANEMO_GLOBAL_WORKSPACE",
              help="Workspace for planemo.")
@pass_context
def planemo(ctx, config, directory, verbose):
    """Utilities to assist with the development of Galaxy tools."""
    ctx.verbose = verbose
    ctx.planemo_config = os.path.expanduser(config)
    ctx.planemo_directory = os.path.expanduser(directory)
