# -*- coding: utf-8 -*-
import logging
import pkg_resources

__title__ = __package__
__version__ = pkg_resources.get_distribution(__package__).version
__author__ = 'Robin Andeer'

# the user should dictate what happens when a logging event occurs
logging.getLogger(__name__).addHandler(logging.NullHandler())
