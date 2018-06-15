# -*- coding: utf-8 -*-

import logging
import os
from plone import api

from Products.MeetingCommunes.profiles.examples_fr import import_data
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.migrations.migrate_to_4_0 import Migrate_To_4_0 as PMMigrate_To_4_0

logger = logging.getLogger('MeetingCommunes')


# The migration class ----------------------------------------------------------
class Migrate_To_4_0(PMMigrate_To_4_0):

    wfs_to_delete = []

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
           'itemPositiveDecidedStates' now it is stored in MeetingConfig.itemAutoSentToOtherMCStates.
           We store these states in the MeetingConfig.itemPositiveDecidedStates, it is used
           to display the 'sent from' leading icon on items sent from another MeetingConfig."""
        logger.info('Defining values for MeetingConfig.itemAutoSentToOtherMCStates...')
        for cfg in self.tool.objectValues('MeetingConfig'):
            cfg.setItemAutoSentToOtherMCStates(('accepted', 'accepted_but_modified', ))
            cfg.setItemPositiveDecidedStates(('accepted', 'accepted_but_modified', ))
        logger.info('Done.')

    def _after_reinstall(self):
        """Use that hook that is called just after the profile has been reinstalled by
           PloneMeeting, this way, we may launch some steps before PloneMeeting ones.
           Here we will update used workflows before letting PM do his job."""
        logger.info('Replacing old no more existing workflows...')
        PMMigrate_To_4_0._after_reinstall(self)
        for cfg in self.tool.objectValues('MeetingConfig'):
            # MeetingItem workflow
            if cfg.getItemWorkflow() == 'meetingitemcollege_workflow':
                cfg.setItemWorkflow('meetingitemcommunes_workflow')
                cfg._v_oldItemWorkflow = 'meetingitemcollege_workflow'
                wfAdaptations = list(cfg.getWorkflowAdaptations())
                if 'no_publication' not in wfAdaptations:
                    wfAdaptations.append('no_publication')
                if 'no_global_observation' not in wfAdaptations:
                    wfAdaptations.append('no_global_observation')
                cfg.setWorkflowAdaptations(wfAdaptations)
            if cfg.getItemWorkflow() == 'meetingitemcouncil_workflow':
                cfg.setItemWorkflow('meetingitemcommunes_workflow')
                cfg._v_oldItemWorkflow = 'meetingitemcouncil_workflow'
            # Meeting workflow
            if cfg.getMeetingWorkflow() == 'meetingcollege_workflow':
                cfg.setMeetingWorkflow('meetingcommunes_workflow')
                cfg._v_oldMeetingWorkflow = 'meetingcollege_workflow'
            if cfg.getMeetingWorkflow() == 'meetingcouncil_workflow':
                cfg.setMeetingWorkflow('meetingcommunes_workflow')
                cfg._v_oldMeetingWorkflow = 'meetingcouncil_workflow'
        # delete old unused workflows, aka every workflows containing 'college' or 'council'
        wfTool = api.portal.get_tool('portal_workflow')
        self.wfs_to_delete = [wfId for wfId in wfTool.listWorkflows()
                              if wfId.endswith(('meetingitemcollege_workflow',
                                                'meetingitemcouncil_workflow',
                                                'meetingcollege_workflow',
                                                'meetingcouncil_workflow'))]
        logger.info('Done.')

    def _addSampleAnnexTypeForMeetings(self):
        """Add a sample annexType for Meetings now that
           annexes may be added to meetings."""
        logger.info('Adding sample annexType in meeting_annexes...')
        for cfg in self.tool.objectValues('MeetingConfig'):
            if not cfg.annexes_types.meeting_annexes.objectIds():
                source = self.ps.getProfileInfo(
                    self.profile_name)['path'].replace('/default', '/examples_fr')
                cfg.addAnnexType(import_data.annexeSeance, source)
        logger.info('Done.')

    def _deleteUselessWorkflows(self):
        """Finally, remove useless workflows."""
        logger.info('Removing useless workflows...')
        if self.wfs_to_delete:
            wfTool = api.portal.get_tool('portal_workflow')
            wfTool.manage_delObjects(self.wfs_to_delete)
        logger.info('Done.')

    def _addMeetingAssembliesDashboardPODTemplate(self):
        """Add DashboardPODTemplate that extracts meeting assemblies."""
        logger.info('Add meeting assemblies DashboardPODTemplate...')
        templateId = 'meeting-assemblies'
        descr = PodTemplateDescriptor(id=templateId, title=u'Assemblée des séances', dashboard=True)
        descr.odt_file = 'meeting_assemblies.odt'
        descr.tal_condition = 'python:False'
        descr.roles_bypassing_talcondition = ['Manager', 'MeetingManager']
        descr.pod_formats = ['doc', 'pdf']
        descr.dashboard_collections_ids = ['searchalldecisions']
        source = os.path.dirname(import_data.__file__)
        for cfg in self.tool.objectValues('MeetingConfig'):
            templatesFolder = cfg.podtemplates
            if templateId not in templatesFolder.objectIds():
                cfg.addPodTemplate(descr, source=source)
        logger.info('Done.')

    def run(self, step=None):
        # change self.profile_name that is reinstalled at the beginning of the PM migration
        self.profile_name = u'profile-Products.MeetingCommunes:default'

        # call steps from Products.PloneMeeting
        PMMigrate_To_4_0.run(self, step=step)

        if step == 3:
            # now MeetingCommunes specific steps
            logger.info('Migrating to MeetingCommunes 4.0...')
            self._cleanCDLD()
            self._migrateItemPositiveDecidedStates()
            self._addSampleAnnexTypeForMeetings()
            self._deleteUselessWorkflows()

        if step == 4:
            # add meeting-assemblies DashboardPODTemplate
            self._addMeetingAssembliesDashboardPODTemplate()


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Reinstall Products.MeetingCommunes and execute the Products.PloneMeeting migration;
       2) Clean CDLD attributes;
       3) Add an annex type for Meetings;
       4) Remove useless workflows;
       5) Migrate positive decided states.
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run()
    migrator.finish()


def migrate_step1(context):
    '''This migration function:

       1) Reinstall Products.MeetingCommunes and execute the Products.PloneMeeting migration.
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run(step=1)
    migrator.finish()


def migrate_step2(context):
    '''This migration function:

       1) Execute step2 of Products.PloneMeeting migration profile (imio.annex).
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run(step=2)
    migrator.finish()


def migrate_step3(context):
    '''This migration function:

       1) Execute step3 of Products.PloneMeeting migration profile.
       2) Clean CDLD attributes;
       3) Add an annex type for Meetings;
       4) Remove useless workflows;
       5) Migrate positive decided states.
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run(step=3)
    migrator.finish()


def migrate_step4(context):
    '''This migration function:

       1) Add meeting assemblies DashboardPODTemplate.
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run(step=4)
    migrator.finish()
