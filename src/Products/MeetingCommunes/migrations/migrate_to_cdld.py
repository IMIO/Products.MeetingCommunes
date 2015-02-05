# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('PloneMeeting')

from Products.PloneMeeting.migrations import Migrator


# The migration class ----------------------------------------------------------
class Migrate_To_cdld(Migrator):

    def _addCDLDTopics(self):
        '''
          Add CDLD topics for synthesis of all advice.'''
        logger.info('Add CDLD topics')
        # add some extra topics to each MeetingConfig
        topicsInfo = (
            # Items for cdld synthesis
            ('searchcdlditems',
            (('Type', 'ATPortalTypeCriterion', ('MeetingItem',)),
             ),
            'created',
            'searchCDLDItems',
            "python: '%s_budgetimpacteditors' % here.portal_plonemeeting.getMeetingConfig(here)"
            ".getId() in member.getGroups() or here.portal_plonemeeting.isManager(here)", ),
        )

        site = self.portal
        for cfg in site.portal_plonemeeting.objectValues('MeetingConfig'):
            cfg.createTopics(topicsInfo)
        logger.info('Done.')

    def run(self):
        logger.info('Migrating to MeetingCommunes with cdld synthesis')
        self._addCDLDTopics()
        self.finish()


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Add topics for CDLD synthesis;
    '''
    Migrate_To_cdld(context).run()
# ------------------------------------------------------------------------------
