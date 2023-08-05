__version__ = '0.9.3'

import click
click.disable_unicode_literals_warning = True

from mh_cli.common import ClickState, config_options, pass_state

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(ClickState)

@cli.command()
@config_options
@pass_state
def config(state):
    """Save typing by setting common options in a config file"""
    state.save_config()

from gi import gi
from inbox import inbox
from rec import rec
from series import series
