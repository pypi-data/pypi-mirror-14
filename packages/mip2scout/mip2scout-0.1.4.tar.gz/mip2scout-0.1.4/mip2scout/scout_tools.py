# -*- coding: utf-8 -*-
import codecs
from datetime import datetime
import logging

from configobj import ConfigObj

from scout.ext.backend import MongoAdapter

logger = logging.getLogger(__name__)


class ScoutDatabase(MongoAdapter):

    """Extended interface to the Scout database."""

    def __init__(self, mongo_auth):
        super(ScoutDatabase, self).__init__()
        self.mongo_auth = mongo_auth
        self.connect_to_database(**mongo_auth)

    def case_is_loaded(self, cust_id, case_id, analysis_date=None, vtype=None):
        """Check if a case is loaded in Scout."""
        case_obj = self.case(cust_id, case_id)

        if case_obj is None:
            return False

        raw_datetime = case_obj.analysis_date.rsplit('.')[0]
        db_analysisdate = datetime.strptime(raw_datetime, '%Y-%m-%d %H:%M:%S')

        if analysis_date > db_analysisdate:
            return False
        elif vtype == 'research' and not case_obj.is_research:
            return False
        else:
            return True

    def upload(self, scout_config, case_id, threshold=5000):
        """Load a case into Scout."""
        if scout_config['variant_type'] == 'clinical':
            # add the case to the database
            case_obj = self.add_case(
                case_lines=codecs.open(scout_config['ped'], 'r'),
                case_type=scout_config['family_type'],
                owner=scout_config['owner'],
                scout_configs=scout_config
            )
        else:
            case_obj = self.case(scout_config['owner'], case_id)
            case_obj.research_requested = False
            case_obj.is_research = True
            case_obj.save()

        logger.info("load variants for case %s", case_obj.case_id)
        self.add_variants(
            vcf_file=scout_config['load_vcf'],
            variant_type=scout_config.get('variant_type', 'clinical'),
            case=case_obj,
            variant_number_treshold=threshold,
        )

    def share(self, cust_id, case_id, collaborator_id):
        """Share a case with a new institute.

        TODO: consider adding a log event to the case
        """
        case_obj = self.case(cust_id, case_id)

        if self.institute(collaborator_id) is None:
            raise ValueError("{} not an existing institute"
                             .format(collaborator_id))

        if collaborator_id in case_obj.collaborators:
            raise ValueError('new customer is already a collaborator')

        logger.info("adding %s as new collaborator to %s", collaborator_id,
                    case_obj.display_name)
        case_obj.collaborators.append(collaborator_id)
        case_obj.save()


def write_ini(data):
    """Serialize a list of INI-formated strings based on a dictionary.

    Args:
        data (dict): key/values to serialize

    Returns:
        List(str): INI serialized version of the data
    """
    config = ConfigObj(data, encoding='utf-8')
    return config.write()
