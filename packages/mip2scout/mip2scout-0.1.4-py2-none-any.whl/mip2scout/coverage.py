# -*- coding: utf-8 -*-
"""Load coverage in chanjo database."""
import logging

from chanjo.cli.load import load_transcripts
from chanjo.store.txmodels import Sample, TranscriptStat
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)


def load(chanjo_db, bed_stream, source=None, sample=None, group=None,
         threshold=None):
    """Load coverage data for a sample into the database."""
    try:
        load_transcripts(chanjo_db, bed_stream, source=source,
                         sample=sample, group=group, threshold=threshold)
    except IntegrityError as error:
        logger.warn(error)
        chanjo_db.session.rollback()


def remove(chanjo_db, group_id):
    logger.debug("find samples in database with id: %s", group_id)
    sample_objs = chanjo_db.query(Sample).filter_by(group_id=group_id)

    for sample_obj in sample_objs:
        logger.debug("delete exon statistics for %s", sample_obj.id)
        (chanjo_db.query(TranscriptStat)
                  .filter(TranscriptStat.sample_id == sample_obj.id)
                  .delete())
        logger.debug("delete '%s' from database", sample_obj.id)
        chanjo_db.session.delete(sample_obj)
    chanjo_db.save()
