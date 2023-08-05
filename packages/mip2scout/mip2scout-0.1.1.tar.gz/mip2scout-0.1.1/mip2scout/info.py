# -*- coding: utf-8 -*-
"""Get information on a MIP analysis for a case."""
import logging

from pymip.api import load_analysis

logger = logging.getLogger(__name__)


def analysis(family_dir):
    """Load data on an analysis.

    Args:
        family_dir (path): path to wrapping case folder
    """
    try:
        return load_analysis(family_dir)
    except OSError as error:
        logger.error('qc sample info file not found')
        raise error
