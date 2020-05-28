# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.examples_fr.import_data import collegeMeeting
from Products.MeetingCommunes.profiles.examples_fr.import_data import data
from Products.PloneMeeting.migrations.migrate_to_4_1 import Migrate_To_4_1 as PMMigrate_To_4_1
from Products.PloneMeeting.migrations.migrate_to_4100 import Migrate_To_4100
from Products.PloneMeeting.migrations.migrate_to_4101 import Migrate_To_4101
from Products.PloneMeeting.migrations.migrate_to_4102 import Migrate_To_4102
from Products.PloneMeeting.migrations.migrate_to_4103 import Migrate_To_4103
from Products.PloneMeeting.migrations.migrate_to_4104 import Migrate_To_4104
from Products.PloneMeeting.migrations.migrate_to_4105 import Migrate_To_4105
from Products.PloneMeeting.migrations.migrate_to_4106 import Migrate_To_4106
from Products.PloneMeeting.migrations.migrate_to_4107 import Migrate_To_4107

import logging


logger = logging.getLogger('MeetingCommunes')


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

    def _hook_before_mgroups_to_orgs(self):
        """Migrate the MeetingGroup.echevinServices attribute to groupsInCharge before
           MeetingGroups are migrated to organizations."""
        logger.info("Migrating MeetingGroup.echevinServices to MeetingGroup.groupsInCharge...")

        def _adapt_expression(expr):
            """ """
            if 'getEchevinsForProposingGroup' in expr and \
               (expr.startswith("python:'") or expr.startswith("python: '")):
                expr = expr.replace(
                    "python:'",
                    "python:pm_utils.org_id_to_uid('")
                expr = expr.replace(
                    "python: '",
                    "python:pm_utils.org_id_to_uid('")
                expr = expr.replace(
                    "' in item",
                    "') == item")
                expr = expr.replace(
                    'item.adapted().getEchevinsForProposingGroup()',
                    'item.getGroupsInCharge(fromOrgIfEmpty=True, first=True)')
            return expr

        # move each value of echevinServices to groupsInCharge
        # and migrate asCopyGroupOn
        for mGroup in self.tool.objectValues('MeetingGroup'):
            if hasattr(mGroup, "echevinServices"):
                echevinServices = mGroup.echevinServices
                for echevinService in echevinServices:
                    otherMGroup = self.tool.get(echevinService)
                    if otherMGroup:
                        groupsInCharge = list(otherMGroup.getGroupsInCharge())
                        groupsInCharge.append(mGroup.getId())
                        otherMGroup.setGroupsInCharge(groupsInCharge)
            # asCopyGroupOn
            mGroup.setAsCopyGroupOn(_adapt_expression(mGroup.getAsCopyGroupOn()))
        # adapt customAdvisers
        for cfg in self.tool.objectValues('MeetingConfig'):
            customAdvisers = deepcopy(cfg.getCustomAdvisers())
            adapted_customAdvisers = []
            for customAdviser in customAdvisers:
                adapted_customAdviser = deepcopy(customAdviser)
                gives_auto_advice_on = customAdviser['gives_auto_advice_on']
                gives_auto_advice_on = _adapt_expression(gives_auto_advice_on)
                adapted_customAdviser['gives_auto_advice_on'] = gives_auto_advice_on
                adapted_customAdvisers.append(adapted_customAdviser)
            cfg.customAdvisers = adapted_customAdvisers
        logger.info('Done.')

    def _defineDirectoryPositionTypes(self):
        """Set default value for contacts directoryy 'position_types'."""
        logger.info("Setting default value for contact.position_types...")
        position_types = self.portal.contacts.position_types
        if len(position_types) == 1 and position_types[0]['token'] == 'default':
            self.portal.contacts.position_types = data.directory_position_types
        logger.info('Done.')

    def _defaultFTWLabels(self):
        """Return default FTW Labels, called by _initPersonalFTWLabels."""
        return deepcopy(collegeMeeting.defaultLabels)

    def run(self,
            profile_name=u'profile-Products.MeetingCommunes:default',
            extra_omitted=[]):
        # change self.profile_name that is reinstalled at the beginning of the PM migration
        self.profile_name = profile_name

        # before anything, update the WF interfaces names
        self._updateWFInterfaceNames()

        # call steps from Products.PloneMeeting
        super(Migrate_To_4_1, self).run(extra_omitted=extra_omitted)

        # execute upgrade steps in PM that were added after main upgrade to 4.1
        Migrate_To_4100(self.portal).run()
        Migrate_To_4101(self.portal).run(from_migration_to_41=True)
        Migrate_To_4102(self.portal).run()
        Migrate_To_4103(self.portal).run()
        Migrate_To_4104(self.portal).run(from_migration_to_41=True)
        Migrate_To_4105(self.portal).run(from_migration_to_41=True)
        Migrate_To_4106(self.portal).run(from_migration_to_41=True)
        Migrate_To_4107(self.portal).run(from_migration_to_41=True)

        # now MeetingCommunes specific steps
        logger.info('Migrating to MeetingCommunes 4.1...')
        self._defineDirectoryPositionTypes()


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Reinstall Products.MeetingCommunes and execute the Products.PloneMeeting migration;
       2) Define default values for 'contacts' directory.position_types;
       3) Define default ftw.labels labels.
    '''
    migrator = Migrate_To_4_1(context)
    migrator.run()
    migrator.finish()
