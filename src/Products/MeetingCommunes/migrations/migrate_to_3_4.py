# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('MeetingCommunes')

from Products.PloneMeeting.migrations.migrate_to_3_4 import Migrate_To_3_4 as PMMigrate_To_3_4


# The migration class ----------------------------------------------------------
class Migrate_To_3_4(PMMigrate_To_3_4):

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

    def _migrateItemPositiveDecidedStates(self):
        """Before, the states in which an item was auto sent to
           selected other meetingConfig was defined in a method
           'itemPositiveDecidedStates' now it is stored in MeetingConfig.itemAutoSentToOtherMCStates."""
        logger.info('Defining values for MeetingConfig.itemAutoSentToOtherMCStates...')
        for cfg in self.tool.objectValues('MeetingConfig'):
            cfg.setItemAutoSentToOtherMCStates(('accepted', 'accepted_but_modified', ))
        logger.info('Done.')

    def run(self):
        # change self.profile_name everything is right before launching steps
        self.profile_name = u'profile-Products.MeetingCommunes:default'
        # call steps from Products.PloneMeeting
        PMMigrate_To_3_4.run(self)
        # now MeetingLiege specific steps
        logger.info('Migrating to MeetingCommunes 3.4...')
        self._cleanCDLD()
        self._migrateItemPositiveDecidedStates()
        self.finish()


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Reinstalls Products.MeetingCommunes so changes regarding icons to use on transitions are applied.
    '''
    Migrate_To_3_4(context).run()
# ------------------------------------------------------------------------------
