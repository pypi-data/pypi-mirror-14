# -*- coding: utf-8 -*-
import glob
import itertools
import os.path


def expand_paths(*glob_paths):
    """Return a flat list of expanded globs."""
    path_groups = (glob.glob(glob_path) for glob_path in glob_paths)
    return itertools.chain.from_iterable(path_groups)


def map_cases(dir_path):
    case_ids = os.listdir(dir_path)
    case_map = {}
    for case_id in case_ids:
        path_guess = glob.glob(os.path.join(dir_path, case_id, '*', case_id))
        if len(path_guess) == 1:
            case_map[case_id] = path_guess[0]
    return case_map
