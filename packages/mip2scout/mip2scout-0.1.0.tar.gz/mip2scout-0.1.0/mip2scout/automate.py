# -*- coding: utf-8 -*-
from glob import glob
import itertools
import os


def get_cases(root):
    """Get paths to all analyzed cases.

    Args:
        root (path): path to customer folder
    """
    # root + case + analysis type + case + case
    paths = glob(os.path.join(root, '*/*/*/*_qc_sampleInfo.yaml'))
    return [os.path.dirname(path) for path in paths]


def case_roots(*roots):
    """Get the case paths for multiple customer roots."""
    return itertools.chain.from_iterable(get_cases(root) for root in roots)


def check_case(analysis):
    """Check if a case is compelted with the updated pipeline."""
    # check the version of MIP
    if analysis.is_old:
        return False

    if not analysis.is_complete:
        return False

    return True
