"""
Main click group for CLI
"""

import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points

import crcli

@with_plugins(
    ep for ep in list(iter_entry_points('crcli.crcli_commands')))
@click.group()
@click.pass_context
def main_group(ctx):
    """This is the command line interface to the collective-reaction database.
    """
    ctx.obj = {}
