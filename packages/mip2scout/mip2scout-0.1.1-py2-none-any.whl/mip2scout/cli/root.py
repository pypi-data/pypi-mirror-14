# -*- coding: utf-8 -*-
import os
import logging

import click
from path import path
import yaml

from mip2scout.constants import APP_ROOT, app_paths
from mip2scout.log import init_log
from .status import status
from .do import do, traverse
from .scout import scout

logger = logging.getLogger(__name__)


def build_folders(root_dir):
    """Ensure that the base folder structure is in place."""
    root_path = path(root_dir)
    root_path.joinpath('static').makedirs_p()
    root_path.joinpath('data').makedirs_p()
    root_path.joinpath('logs').makedirs_p()


@click.group()
@click.option('-c', '--config', type=click.File())
@click.option('-l', '--log', type=click.File())
@click.option('--level', default='INFO', help='logging level')
@click.option('-r', '--root-dir', type=click.Path(exists=True))
@click.pass_context
def root(context, config, log, level, root_dir):
    """Process MIP output to prepare upload to Scout."""
    if config and os.path.exists(config.name):
        context.obj = yaml.load(config)
        context.default_map = context.obj
    else:
        context.obj = {}

    app_rootdir = root_dir or context.obj.get('root_dir') or APP_ROOT
    paths = context.obj['paths'] = app_paths(app_rootdir)
    build_folders(paths.app)
    log_path = log or paths.log
    # setup logging
    init_log(log_path, email_auth=context.obj.get('email'), level=level)

root.add_command(status)
root.add_command(do)
root.add_command(traverse)
root.add_command(scout)
