#!/usr/bin/env python
# coding=utf-8
"""
# manifest-checker : Implementation of main.py

Implementation of the manifest-checker cli using click

The main CLI interface - implemented using the click framework.
"""

import os
import click
import hashlib
import environment
from defaults import DEFAULT_MANIFEST_FILE, DEFAULT_HASH

import pkg_resources

import create
import check


def validate_extension(ctx, param, value):
    if len(value) == 0:
        return value
    if value[0][0] == ".":
        return value
    else:
        raise click.BadParameter("file extensions must start with a '.'")


def validate_report_out(ctx, param, value):
    if value is None:
        return None

    if value.name == '-':
        raise click.BadParameter("Cannot use stdout for this parameter : use '-v/--verbose 3' instead")
    else:
        return value


def validate_root(ctx, param, value):
    if os.path.isdir(value):
        return value
    else:
        raise click.BadParameter("Must be a existing directory")


def get_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('manifest : version {}'.format(
            pkg_resources.require("manifest-checker")[0].version))
    ctx.exit()


@click.group()
@click.option('--version', is_flag=True, callback=get_version, expose_value=False, is_eager=True)
@click.option('-v', '--verbose', type=click.Choice(['0', '1', '2', '3']), default='1')
@click.option('-a', '--hash', type=click.Choice(hashlib.algorithms), default=DEFAULT_HASH,
              help='The hash algorithm to use in order to compare file contents.')
@click.option('-f', '--manifest', envvar='MANIFEST',
              default=DEFAULT_MANIFEST_FILE,
              help='The manifest file to use - default is `{}`'.format(DEFAULT_MANIFEST_FILE))
@click.option('-r', '--root', metavar='ROOT', default=os.getcwd(), callback=validate_root,
              help='The root directory to create the manifest from, or check the manifest against.')
@click.option('-E', '--clearExtensions', is_flag=True,
              help='Reset the included file extensions to an empty list')
@click.option('-e', '--extension', multiple=True, metavar='EXTENSION', default='', callback=validate_extension,
              help='Add an file extension to the list of those to be accepted')
@click.option('-D', '--clearDirectory', is_flag=True,
              help = 'Reset the list of top level directories to be ignored to an empty list')
@click.option('-d', '--ignoreDirectory', multiple=True, metavar='DIRECTORY',
              help='Add a directory to the list of top level directories to be ignored')
@click.option('-k/-K', 'report_skipped', is_flag=True, default=False,
              help='Whether or not to report (in summary) on skipped files')
@click.option('-t/-T', 'report_extensions', is_flag=True, default=False,
              help='Whether or not to report (in summary) on checked file extensions')
@click.pass_context
def primary(ctx, **kwargs):
    """
    A utility to traverse a local directory tree under a given directory and either build or
    check against a manifest file with a hash value for each file within that directory tree.

    By default the manifest commands look for file types which are used by a typical Python or
    Django application :

    \b
        Default Extensions = ['.py','.html','.txt','.css','.js','.gif','.png','.jpg','.jpeg']

    Extra extensions can be included in the manifest by using the `-e, --extension` option.
    When the `-E, --clearExtensions` option is used this will ignore the default extensions above
    and ONLY use those extensions added by the `-e` option. Using `-E, --clearExtensions` without at
    least one `-e` option is an error.

    By default the manifest on creation and checking ignores a number of top level directories
    (i.e. those directly under the current directory). Typically these are directories which are
    used for development/testing, but which are not deployed (they are either recreated on deployment,
    they are dynamically created, or are present only for testing/development purposes). The default
    list of these ignore directories are :

    \b
        ['static','media','htmlcov','env','docs','build','dist']
        'htmlcov' is included in case you use the coverage tool with html reporting
        'env' is included in case you use the Pycharm IDE
        'build' & 'dist' are created by setuptools
        'docs' is a common directory for a number of documentation tools - including sphinx

    Extra top level directories can be extra in the manifest by using the `-i,--ignoreDirectory` option.
    When the `-D,--clearDirectory` option is used this will ignore the default ignored directories above and
    ONLY use those extensions added by the `-e` option.
    """
    ctx.obj = environment.CommandEnvironment(**kwargs)


def main():
    primary.add_command(check.check)
    primary.add_command(create.create)
    primary()
