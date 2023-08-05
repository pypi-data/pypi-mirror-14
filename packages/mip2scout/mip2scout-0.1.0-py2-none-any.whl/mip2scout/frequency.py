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


def filter_common(in_vcf, write=False):
    """Filter out common variants using genmod.

    Args:
        in_vcf (path): path to VCF input file
        write (Optional[bool]): optionally write to a temporary directory

    Returns:
        stream: STDOUT of the command
    """
    filter_args = ['genmod', 'filter', '-t', '0.10', in_vcf]
    proc = subprocess.Popen(filter_args, stdout=subprocess.PIPE)

    if write:
        out_file = tempfile.NamedTemporaryFile('w')
        for line in proc.stdout:
            out_file.write(line)
        return out_file

    return proc.stdout


def vt_decompose(in_vcf, hum_ref, thog_ref, write=False):
    """Decompose multi-allelic variants in a VCF to STDOUT.

    Args:
        in_vcf (path): path to VCF input file
        hum_ref (path): path to human reference genome
        thog_ref (path): path to 1000 genomes reference file
        write (Optional[bool]): optionally write to a temporary directory

    Returns:
        stream: STDOUT of the command
    """
    decom_args = ['vt', 'decompose', '-s', in_vcf]
    proc1 = subprocess.Popen(decom_args, stdout=subprocess.PIPE)

    norm_args = ['vt', 'normalize', '-n', '-r', hum_ref, '-']
    proc2 = subprocess.Popen(norm_args, stdin=proc1.stdout,
                             stdout=subprocess.PIPE)

    tg_args = ['genmod', 'annotate', '--thousand_g', thog_ref, '-']
    proc3 = subprocess.Popen(tg_args, stdin=proc2.stdout,
                             stdout=subprocess.PIPE)

    filter_args = ['genmod', 'filter', '-t', '0.10', '-']
    proc4 = subprocess.Popen(filter_args, stdin=proc3.stdout,
                             stdout=subprocess.PIPE)

    if write:
        out_file = tempfile.NamedTemporaryFile('w')
        for line in proc4.stdout:
            out_file.write(line)
        return out_file

    return proc4.stdout
