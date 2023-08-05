import click
from mh_cli import cli
from mh_cli.common import pass_state

from os.path import dirname
from fabric.api import local, lcd

@cli.group()
def gi():
    """Do stuff with Ghost Inspector tests"""

@gi.command(name='list', context_settings=dict(ignore_unknown_options=True))
@click.argument('gi_args', nargs=-1, type=click.UNPROCESSED)
@pass_state
def gi_list(state, gi_args):
    """Collect and list available tests"""
    cmd = "py.test -c %s --verbose --collect-only %s" % (state.conf_file, " ".join(gi_args))
    with(lcd(dirname(dirname(__file__)))):
        local(cmd)


@gi.command(name='exec', context_settings=dict(ignore_unknown_options=True))
@click.argument('gi_args', nargs=-1, type=click.UNPROCESSED)
@pass_state
def gi_exec(state, gi_args):
    """Execute tests"""
    cmd = "py.test -c %s --verbose %s" % (state.conf_file, " ".join(gi_args))
    with(lcd(dirname(dirname(__file__)))):
        local(cmd)
