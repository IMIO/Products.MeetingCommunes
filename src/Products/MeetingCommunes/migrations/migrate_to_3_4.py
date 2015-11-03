# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('MeetingCommunes')

from Products.PloneMeeting.migrations import Migrator


# The migration class ----------------------------------------------------------
class Migrate_To_3_4(Migrator):

    def _cleanCDLD(self):
        """We removed things related to 'CDLD' finance advice, so:
           - remove the 'cdld-document-generate' from document_actions;
           - remove the MeetingConfig.CdldProposingGroup attribute.
        """
        logger.info('Removing CDLD related things...')
        doc_actions = self.portal.portal_actions.document_actions
        # remove the action from document_actions
        if 'cdld-document-generate' in doc_actions:
            doc_actions.manage_delObjects(ids=['cdld-document-generate', ])
        # clean the MeetingConfigs
        for cfg in self.tool.objectValues('MeetingConfig'):
            if hasattr(cfg, 'cdldProposingGroup'):
                delattr(cfg, 'cdldProposingGroup')
        logger.info('Done.')

    def run(self):
        logger.info('Migrating to MeetingCommunes 3.4...')
        self._cleanCDLD()
        # reinstall so icons defined on workflows are applied
        self.reinstall(profiles=[u'profile-Products.MeetingCommunes:default', ])
        self.finish()


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Reinstalls Products.MeetingCommunes so changes regarding icons to use on transitions are applied.
    '''
    Migrate_To_3_4(context).run()
# ------------------------------------------------------------------------------
