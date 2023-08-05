# -*- coding: utf-8 -*-
import logging

import click

from mip2scout.scout_tools import ScoutDatabase

logger = logging.getLogger(__name__)


@click.command()
@click.option('-s', '--share', type=str, help='institute to share with')
@click.option('-r', '--remove', is_flag=True, help='remove case from database')
@click.option('-f', '--force', is_flag=True)
@click.argument('cust_id')
@click.argument('case_id')
@click.pass_context
def scout(context, share, remove, force, cust_id, case_id):
    """Interact with the Scout database."""
    scout_db = ScoutDatabase(context.obj['mongodb'])
    case_obj = scout_db.case(cust_id, case_id)
    if case_obj is None:
        logger.warn("Couldn't find the case in the database")
        context.abort()

    if share:
        scout_db.share(cust_id, case_id, collaborator_id=share)

    elif remove:
        if not force:
            prompt = ("Are you sure you want to remove '{}'"
                      .format(case_obj.display_name))
            if click.confirm(prompt):
                logger.info("remove variants")
                scout_db.delete_variants(case_obj.case_id, 'clinical')
                scout_db.delete_variants(case_obj.case_id, 'research')
                logger.info("remove case (%s, %s)", cust_id, case_id)
                scout_db.delete_case(cust_id, case_id)
    else:
        # just show some information
        click.echo("{case.display_name} - Owner: {case.owner}"
                   .format(case=case_obj))
