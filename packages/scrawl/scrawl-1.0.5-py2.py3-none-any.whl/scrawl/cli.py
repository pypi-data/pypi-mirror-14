import os
import sys
import click
import helpers.db as dbconn
import helpers.helpers as helpers

CONTEXT_SETTINGS = dict(auto_envvar_prefix='COMPLEX')


class Context(object):

    def __init__(self):
        pass

    def database(self):
        return dbconn.dbase('data.db')


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))

# print cmd_folder


class Scrawl(click.MultiCommand):

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
            mod = __import__('scrawl.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


class Scrawl2(click.MultiCommand):

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
            mod = __import__('scrawl.commands2.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=Scrawl, context_settings=CONTEXT_SETTINGS)
@pass_context
def scrawl(ctx):
    """
    Scrawl - Python note-taking console app \n
    Type scrawl --help to view list of commands
    """


@click.command(cls=Scrawl2, context_settings=CONTEXT_SETTINGS)
@pass_context
def scrawl2(ctx):
    """
    Scrawl2 - An enhamced version of the
    Python note-taking console app scrawl \n
    Type scrawl2 --help to view list of commands
    """
