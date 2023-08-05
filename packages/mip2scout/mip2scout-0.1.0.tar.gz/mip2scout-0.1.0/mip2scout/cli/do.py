# -*- coding: utf-8 -*-
import codecs
import logging
import os

import click
from chanjo.store import Store as ChanjoStore
from chanjo.store.txmodels import Sample as ChanjoSample
from loqusdb.plugins import MongoAdapter as LoqusdbAdapter
from loqusdb.utils import load_variants, delete_variants
from loqusdb.exceptions import CaseError
from configobj import ConfigObj
from path import path
from taboo.store import Database as TabooDatabase
from taboo.input import load_bcf, load_vcf

from mip2scout import automate, coverage, info, madeline, scout_tools
from mip2scout.constants import APP_ROOT, app_paths
from mip2scout.exc import (SinglePedigreeError, MadelineIncompatibleError,
                           FrequencyError, ChanjoSampleLoadedError)
from mip2scout.frequency import affected_individuals, filter_common
from .utils import expand_paths

SEX = {1: 'male', 2: 'female', 'other': 'unknown', 0: 'unknown'}
logger = logging.getLogger(__name__)


@click.command()
@click.option('-s', '--step', help='step to run',
              type=click.Choice(['svg', 'config', 'upload', 'frequency',
                                 'genotype', 'coverage']))
@click.argument('cust_roots', nargs=-1, type=click.Path(exists=True))
@click.pass_context
def traverse(context, step, cust_roots):
    """Upload all cases found by traversing the root directories."""
    if len(cust_roots) == 0:
        cust_roots = expand_paths(*context.obj.get('customer_roots', []))

    for case_path in automate.case_roots(*cust_roots):
        mip_case = info.analysis(case_path)
        if not mip_case.is_complete:
            logger.debug("skipping non-complete case: %s", case_path)
        elif step:
            logger.info("processing %s: %s", case_path, step)
            context.invoke(do, case_path=case_path, step=step)
        else:
            logger.info("processing case: %s", case_path)
            context.invoke(do, case_path=case_path, run_all=True)


@click.group()
@click.argument('case_path', type=click.Path(exists=True))
@click.option('-a', '--all', 'run_all', is_flag=True,
              help='do all the processing')
@click.option('-s', '--step', help='step to run',
              type=click.Choice(['svg', 'config', 'upload', 'frequency',
                                 'genotype', 'coverage']))
@click.option('-f', '--force', is_flag=True, help='process unfinished analyses')
@click.pass_context
def do(context, case_path, run_all, step, force):
    """Perform action on a completed analysis."""
    mip_case = info.analysis(case_path)
    context.obj['case'] = mip_case

    # check if analysis is complete
    if not force and not mip_case.is_complete:
        logger.warn("analysis not finished")
        context.abort()

    if run_all:
        context.invoke(all_cmd)
    elif step:
        context.invoke(STEPS[step])


@do.command()
@click.option('-m', '--madeline', help='Madeline executable')
@click.option('-o', '--out', type=click.File('w'), default='-')
@click.pass_context
def svg(context, madeline, out):
    """Run madeline on the pedigree file."""
    mip_case = context.obj['case']
    madeline_exe = madeline or context.obj['madeline_exe']
    svg_content = run_madeline(mip_case, madeline_exe=madeline_exe)
    click.echo(svg_content.decode('utf-8'), file=out)


@do.command('coverage')
@click.option('-u', '--uri', type=str)
@click.option('-rm', '--remove', is_flag=True)
@click.option('-t', '--threshold', type=int, default=10)
@click.option('-f', '--force', is_flag=True)
@click.pass_context
def coverage_cmd(context, uri, remove, threshold, force):
    """Upload coverage to the Chanjo database."""
    mip_case = context.obj['case']
    if not force and mip_case.is_old:
        logger.warn("unsupported MIP version for coverage: %s", mip_case.version)
    else:
        case_group_id = group_id(mip_case)
        chanjo_db = ChanjoStore(uri or context.obj['chanjo_uri'])
        if remove:
            coverage.remove(chanjo_db, case_group_id)
        else:
            # load coverage for the case
            try:
                load_coverage(chanjo_db, mip_case, case_group_id,
                              threshold=threshold)
            except ChanjoSampleLoadedError as error:
                logger.warn("sample already loaded: %s", error.message)


@do.command()
@click.option('-o', '--out', type=click.File('w'), default='-')
@click.option('-t', '--vtype', type=click.Choice(['clinical', 'research']),
              default='clinical')
@click.option('-m', '--madeline-path', type=click.Path(exists=True))
@click.pass_context
def config(context, out, vtype, madeline_path):
    """Create a scout config file."""
    mip_case = context.obj['case']
    scout_data = mip_case.scout_config(vtype)
    if madeline_path:
        scout_data['madeline'] = os.path.abspath(madeline_path)

    ini_lines = scout_tools.write_ini(scout_data)
    click.echo('\n'.join(ini_lines).decode('utf-8'), file=out)


@do.command()
@click.option('-d', '--database', help='Mongo database to use')
@click.option('--host', help='Host where Mongo is running')
@click.option('--port', help='Port where Mongo is running')
@click.option('-u', '--username', help='Mongo username')
@click.option('-p', '--password', help='Mongo password')
@click.option('-c', '--config', type=click.Path(exists=True), required=True,
              help='Scout config object')
@click.option('-f', '--force', is_flag=True)
@click.pass_context
def upload(context, database, host, port, username, password, config, force):
    """Upload processed analysis to Scout."""
    mongo_auth = context.obj.get('mongodb', {})
    mongo_auth['database'] = database or mongo_auth.get('database')
    mongo_auth['host'] = host or mongo_auth.get('host') or 'localhost'
    mongo_auth['port'] = port or mongo_auth.get('port') or 27017
    mongo_auth['username'] = username or mongo_auth.get('username')
    mongo_auth['password'] = password or mongo_auth.get('password')
    scout_db = scout_tools.ScoutDatabase(mongo_auth)

    # load the config file
    scout_config = ConfigObj(config)
    vtype = scout_config['variant_type']
    mip_case = context.obj['case']
    owner = mip_case.instance_tags[0]
    case_loaded = scout_db.case_is_loaded(owner, mip_case.family_id,
                                          mip_case.analyzed_at, vtype=vtype)
    if force or not case_loaded:
        scout_db.upload(scout_config, mip_case.family_id)
    else:
        logger.warn('case already uploaded, skipping')


@do.command()
@click.option('--bulk/--no-bulk', default=True)
@click.option('-r', '--remove', is_flag=True)
@click.pass_context
def frequency(context, bulk, remove):
    """Upload or remove variants to/from frequency database."""
    loqusdb_auth = context.obj.get('loqusdb', {})
    adapter = LoqusdbAdapter()
    adapter.connect(**loqusdb_auth)

    mip_case = context.obj['case']
    if mip_case.is_old:
        logger.warn("unsupported MIP version for frequency: %s", mip_case.version)
    else:
        if mip_case.version == 'v2.6.1':
            vcf_path = filter_common(mip_case.research_vcf, write=True)
        else:
            vcf_path = mip_case.research_vcf

        case_group_id = group_id(mip_case)
        # we only care about "rare" variants
        ped_path = mip_case.configs.pedigree

        try:
            affected_inds = affected_individuals(ped_path)
        except FrequencyError as error:
            logger.warn("LOQUSDB: {}".format(error.message))

        if 'affected_inds' in locals():
            with open(vcf_path, 'r') as vcf_stream:
                try:
                    if remove:
                        count = delete_variants(adapter, vcf_stream,
                                                case_group_id, affected_inds)
                        logger.info("removed {} variants".format(count))
                    else:
                        load_variants(adapter, case_group_id, affected_inds,
                                      vcf_stream, bulk_insert=bulk,
                                      vcf_path=vcf_path)
                except CaseError as error:
                    logger.warn("LOQUSDB: {}".format(error.message))


@do.command()
@click.option('-f', '--force', is_flag=True, help='overwrite existing samples')
@click.pass_context
def genotype(context, force):
    """Upload results from sequencing to the genotype platform."""
    mip_case = context.obj['case']
    store = TabooDatabase(context.obj['taboo_db'])

    with codecs.open(context.obj['rsnumber_ref']) as rs_stream:
        if mip_case.bcf_path and mip_case.bcf_path.exists():
            analyses = load_bcf(store, mip_case.bcf_path, rs_stream,
                                force=force)
        else:
            analyses = load_vcf(store, mip_case.ready_vcf, rs_stream,
                                force=force)
        for analysis in analyses:
            logger.info("added analysis: %s", analysis.sample.sample_id)
            sample_id = analysis.sample.sample_id
            ped_sex = mip_case.ped.individuals[sample_id].sex
            analysis.sample.expected_sex = SEX[ped_sex]
        store.save()


@do.command('all')
@click.option('-r', '--root-dir', type=click.Path())
@click.option('-t', '--vtype', default='clinical')
@click.option('-f', '--force', is_flag=True)
@click.option('--no-upload', is_flag=True)
@click.pass_context
def all_cmd(context, root_dir, vtype, force, no_upload):
    """Do all the preprocessing for an analysis."""
    paths = app_paths(root_dir or context.obj['root_dir'] or APP_ROOT)
    mip_case = context.obj['case']
    owner = mip_case.instance_tags[0]
    case_root = build_case_root(paths.out, cust_id=owner,
                                case_id=mip_case.family_id)
    config_path = case_root.joinpath("{}.conf.ini".format(vtype))
    madeline_path = case_root.joinpath('madeline.xml')

    scout_db = scout_tools.ScoutDatabase(context.obj['mongodb'])
    logger.debug('checking if case is loaded in Scout')
    case_loaded = scout_db.case_is_loaded(owner, mip_case.family_id,
                                          mip_case.analyzed_at,
                                          vtype=vtype)
    if not force and case_loaded:
        logger.info("case (%s) already uploaded", vtype)

    else:
        if vtype == 'clinical':
            logger.info('generating madeline SVG file')
            try:
                context.invoke(svg, out=madeline_path.open('w'))
            except SinglePedigreeError:
                logger.debug('skipping pedigree generation, single sample')
            except MadelineIncompatibleError:
                logger.debug('skipping pedigree generation, no connections')

            case_obj = scout_db.case(owner, mip_case.family_id)
            if case_obj and not case_loaded:
                logger.info("removing coverage from old analysis (%s)",
                            case_obj.analysis_date)
                context.invoke(coverage_cmd, remove=True)

                logger.info('remove variants from frequency database')
                context.invoke(frequency, remove=True)

            logger.info('uploading coverage to chanjo database')
            context.invoke(coverage_cmd)

            logger.info('uploading variants to frequency database')
            context.invoke(frequency)

            logger.info('uploading genotypes to taboo database')
            context.invoke(genotype, force=force)

        logger.info("generating '%s' config file", vtype)
        context.invoke(config, out=config_path.open('w'), vtype=vtype,
                       madeline_path=madeline_path)

        if not no_upload:
            logger.info('uploading case and variants to scout')
            context.invoke(upload, config=config_path, force=force)


def run_madeline(mip_case, madeline_exe):
    """Run and process madeline."""
    external_individuals = madeline.external_ped(mip_case.ped.individuals)
    mip_case.ped.families[mip_case.family_id].individuals = external_individuals
    svg_content = madeline.run(mip_case.ped, exe=madeline_exe)
    return svg_content


def group_id(mip_case):
    """Compose globally unique group id (case)."""
    owner = mip_case.instance_tags[0]
    return "{}-{}".format(owner, mip_case.family_id)


def load_coverage(chanjo_db, mip_case, group_id, threshold=None):
    """Load coverage for a case."""
    for sample_id, bed_path in mip_case.chanjo_sample_outputs():
        logger.info("load coverage for %s", sample_id)
        if chanjo_db.query(ChanjoSample).filter_by(id=sample_id).first():
            raise ChanjoSampleLoadedError(sample_id)
        with open(bed_path, 'r') as bed_stream:
            coverage.load(chanjo_db, bed_stream, source=bed_path,
                          group=group_id, threshold=threshold)


def build_case_root(root_dir, cust_id, case_id):
    """Ensure that the base folder structure is in place."""
    root_path = path(root_dir)
    case_root = root_path.joinpath('static', cust_id, case_id)
    case_root.makedirs_p()
    return case_root


STEPS = {'svg': svg, 'coverage': coverage_cmd, 'config': config,
         'upload': upload, 'frequency': frequency, 'genotype': genotype}
