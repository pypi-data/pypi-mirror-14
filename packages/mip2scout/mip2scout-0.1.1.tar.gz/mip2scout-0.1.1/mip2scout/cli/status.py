# -*- coding: utf-8 -*-
import logging

import click
from tabulate import tabulate

from mip2scout import info, scout_tools, automate
from .utils import expand_paths

logger = logging.getLogger(__name__)


def analysis_info(mip_case, scout_db):
    """Gatcher useful status information on a case."""
    case_info = {}

    # MIP info
    owner = mip_case.instance_tags[0]
    case_info['customer'] = owner
    case_info['case'] = mip_case.family_id
    case_info['analysis'] = mip_case.analyzed_at
    case_info['analyzed'] = mip_case.is_complete
    case_info['samples'] = mip_case.ped.individuals.keys()
    case_info['version'] = mip_case.version

    # Scout info
    scout_case = scout_db.case(owner, mip_case.family_id)
    case_info['in_scout'] = (True if scout_case else False)
    case_info['uploaded'] = scout_db.case_is_loaded(owner, mip_case.family_id,
                                                    mip_case.analyzed_at)
    case_info['research'] = (scout_case and scout_case.is_research)
    return case_info


def serialize_status(case_info):
    """Serialize the information in the case info dict."""
    rows = [case_info['customer'], case_info['case'],
            ', '.join(case_info['samples']), case_info['version'],
            case_info['analysis'],
            'yes' if case_info['analyzed'] else 'no',
            'yes' if case_info['in_scout'] else 'no',
            'yes' if case_info['uploaded'] else 'no',
            'open' if case_info['research'] else 'close']
    return rows


@click.group()
@click.pass_context
def status(context):
    """Show status for cases and analyses."""
    pass


@status.command()
@click.argument('case_paths', type=click.Path(exists=True), nargs=-1)
@click.pass_context
def case(context, case_paths):
    """Monitor the status of an analysis (finished/running)."""
    if len(case_paths) == 0:
        logger.warn('no case paths given')
        context.abort()

    scout_db = scout_tools.ScoutDatabase(context.obj['mongodb'])

    case_infos = (analysis_info(info.analysis(case_path), scout_db)
                  for case_path in case_paths)

    headers = ['Customer', 'Case', 'Samples', 'MIP', 'Date', 'Complete',
               'In Scout', 'Up-to-date', 'Research']
    rows = (serialize_status(case_info) for case_info in case_infos)
    output = tabulate(rows, headers=headers, tablefmt='fancy_grid')
    click.echo(output)


@status.command()
@click.argument('customer_paths', type=click.Path(exists=True), nargs=-1)
@click.pass_context
def cust(context, customer_paths):
    """Display status for multiple customer cases."""
    if len(customer_paths) == 0:
        customer_paths = expand_paths(*context.obj.get('customer_roots', []))

    for customer_path in customer_paths:
        case_paths = automate.get_cases(customer_path)
        click.echo("Path: {}".format(customer_path))
        if len(case_paths) > 0:
            context.invoke(case, case_paths=case_paths)
        else:
            click.echo('No cases found here...')
