# -*- coding: utf-8 -*-

import logging
from Products.PloneMeeting.migrations.migrate_to_4_1 import Migrate_To_4_1 as PMMigrate_To_4_1

logger = logging.getLogger('MeetingCommunes')


# The migration class ----------------------------------------------------------
class Migrate_To_4_1(PMMigrate_To_4_1):

    def _updateWFInterfaceNames(self):
        """Update the WF interface names in MeetingConfigs as 'College' and 'Council'
           interfaces were replaced by 'Communes' interfaces."""
        logger.info("Updating WF interface names for every MeetingConfigs...")
        for cfg in self.tool.objectValues('MeetingConfig'):
            if cfg.getItemConditionsInterface() in (
                    'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions',
                    'Products.MeetingCommunes.interfaces.IMeetingItemCouncilWorkflowConditions'):
                cfg.setItemConditionsInterface(
                    'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions')
            if cfg.getItemActionsInterface() in (
                    'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions',
                    'Products.MeetingCommunes.interfaces.IMeetingItemCouncilWorkflowActions'):
                cfg.setItemActionsInterface(
                    'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions')
            if cfg.getMeetingConditionsInterface() in (
                    'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions',
                    'Products.MeetingCommunes.interfaces.IMeetingCouncilWorkflowConditions'):
                cfg.setMeetingConditionsInterface(
                    'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions')
            if cfg.getMeetingActionsInterface() in (
                    'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions',
                    'Products.MeetingCommunes.interfaces.IMeetingCouncilWorkflowActions'):
                cfg.setMeetingActionsInterface(
                    'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions')
        logger.info('Done.')

    def run(self, step=None):
        # change self.profile_name that is reinstalled at the beginning of the PM migration
        self.profile_name = u'profile-Products.MeetingCommunes:default'

        # before anything, update the WF interfaces names
        self._updateWFInterfaceNames()

        # call steps from Products.PloneMeeting
        PMMigrate_To_4_1.run(self, step=step)
        # now MeetingCommunes specific steps
        logger.info('Migrating to MeetingCommunes 4.0...')


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Reinstall Products.MeetingCommunes and execute the Products.PloneMeeting migration.
    '''
    migrator = Migrate_To_4_1(context)
    migrator.run()
    migrator.finish()
