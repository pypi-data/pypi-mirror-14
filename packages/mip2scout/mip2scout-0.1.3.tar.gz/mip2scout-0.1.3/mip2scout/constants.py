# -*- coding: utf-8 -*-
from collections import namedtuple
import os

Paths = namedtuple('Paths', ['app', 'out', 'config', 'log'])
APP_ROOT = os.path.expanduser('~/.mip2scout')


def app_paths(root=APP_ROOT):
    out_root = os.path.join(root, 'static')
    config_path = os.path.join(root, 'config.yaml')
    log_path = os.path.join(root, 'logs/main.log')
    return Paths(app=root, out=out_root, config=config_path, log=log_path)
