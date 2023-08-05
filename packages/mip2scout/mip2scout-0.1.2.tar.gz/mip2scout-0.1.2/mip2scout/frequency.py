# -*- coding: utf-8 -*-
import logging
import subprocess
import tempfile

from loqusdb.utils import get_family

from mip2scout.exc import FrequencyError

logger = logging.getLogger(__name__)


def affected_individuals(ped_path):
    """Extract affected individuals from a PED file.

    Args:
        ped_path (path): path to the PED file

    Returns:
        list: list of affected individuals

    Raises:
        mip2scout.exc.FrequencyError: if no affected individals in PED
    """
    with open(ped_path, 'r') as ped_stream:
        locus_fam = get_family(family_lines=ped_stream, family_type='alt')

    if not locus_fam.affected_individuals:
        message = "no affected individuals in ped file"
        logger.error(message)
        raise FrequencyError(message)

    return locus_fam.affected_individuals
