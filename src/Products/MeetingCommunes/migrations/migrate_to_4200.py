# -*- coding: utf-8 -*-

from DateTime import DateTime
from plone import api
from plone.namedfile import NamedBlobFile
from Products.PloneMeeting.migrations.migrate_to_4200 import Migrate_To_4200 as PMMigrate_To_4200

import logging


logger = logging.getLogger('MeetingCommunes')


class Migrate_To_4200(PMMigrate_To_4200):

    def _fixUsedMeetingWFs(self):
        """meetingcommunes_workflow/meetingitemcommunes_workflows do not exist anymore,
           we use meeting_workflow/meetingitem_workflow."""
        logger.info("Adapting 'meetingWorkflow/meetingItemWorkflow' for every MeetingConfigs...")
        for cfg in self.tool.objectValues('MeetingConfig'):
            if cfg.getMeetingWorkflow() == 'meetingcommunes_workflow':
                cfg.setMeetingWorkflow('meeting_workflow')
            if cfg.getItemWorkflow() == 'meetingitemcommunes_workflow':
                cfg.setItemWorkflow('meetingitem_workflow')
        # delete old unused workflows, aka every workflows containing 'communes_workflow'
        wfTool = api.portal.get_tool('portal_workflow')
        wfs_to_delete = [wfId for wfId in wfTool.listWorkflows()
                         if 'communes_workflow' in wfId]
        if wfs_to_delete:
            wfTool.manage_delObjects(wfs_to_delete)
        logger.info('Done.')

    def _get_wh_key(self, itemOrMeeting):
        """Get workflow_history key to use, in case there are several keys, we take the one
           having the last event."""
        keys = itemOrMeeting.workflow_history.keys()
        if len(keys) == 1:
            return keys[0]
        else:
            lastEventDate = DateTime('1950/01/01')
            keyToUse = None
            for key in keys:
                if itemOrMeeting.workflow_history[key][-1]['time'] > lastEventDate:
                    lastEventDate = itemOrMeeting.workflow_history[key][-1]['time']
                    keyToUse = key
            return keyToUse

    def _adaptWFHistoryForItemsAndMeetings(self):
        """We use PM default WFs, no more meetingcommunes(item)_workflow..."""
        logger.info('Updating WF history items and meetings to use new WF id...')
        wfTool = api.portal.get_tool('portal_workflow')
        catalog = api.portal.get_tool('portal_catalog')
        for cfg in self.tool.objectValues('MeetingConfig'):
            # this will call especially part where we duplicate WF and apply WFAdaptations
            cfg.registerPortalTypes()
            for brain in catalog(portal_type=(cfg.getItemTypeName(), cfg.getMeetingTypeName())):
                itemOrMeeting = brain.getObject()
                itemOrMeetingWFId = wfTool.getWorkflowsFor(itemOrMeeting)[0].getId()
                if itemOrMeetingWFId not in itemOrMeeting.workflow_history:
                    wf_history_key = self._get_wh_key(itemOrMeeting)
                    itemOrMeeting.workflow_history[itemOrMeetingWFId] = \
                        tuple(itemOrMeeting.workflow_history[wf_history_key])
                    del itemOrMeeting.workflow_history[wf_history_key]
                    # do this so change is persisted
                    itemOrMeeting.workflow_history = itemOrMeeting.workflow_history
                else:
                    # already migrated
                    break
        logger.info('Done.')

    def _hook_before_meeting_to_dx(self):
        """Adapt Meeting.workflow_history before migrating to DX."""
        self._adaptWFHistoryForItemsAndMeetings()

    def _add_dashboard_pod_template_export_users_groups(self):
        """Add the export users and groups DashboardPODTemplate in the contacts directory."""
        logger.info("Adding 'Export users and groups' to 'contacts' directory...")
        pod_template_id = 'export-users-groups'
        contacts = self.portal.contacts
        if pod_template_id in contacts.objectIds():
            self._already_migrated()
            return

        profile_path = self.ps._getImportContext(self.profile_name)._profile_path
        odt_path = profile_path + '/../examples_fr/templates/users-groups-export.ods'
        odt_file = open(odt_path, 'rb')
        odt_binary = odt_file.read()
        odt_file.close()
        data = {'title': 'Export utilisateurs et groupes',
                'pod_formats': ['ods', 'xls'],
                'dashboard_collections': contacts.get('orgs-searches').all_orgs.UID(),
                'odt_file': NamedBlobFile(
                    data=odt_binary,
                    contentType='application/vnd.oasis.opendocument.text',
                    filename=u'users-groups-export.ods'),
                'use_objects': False,
                }
        pod_template = api.content.create(
            id=pod_template_id,
            type='DashboardPODTemplate',
            container=contacts,
            **data)
        pod_template.reindexObject()
        logger.info('Done.')

    def _mc_fixPODTemplatesInstructions(self):
        '''Make some replace in POD templates to fit changes in code...'''
        # for every POD templates
        replacements = {'.print_deliberation(': '.print_full_deliberation(', }
        # specific for Meeting POD Templates
        meeting_replacements = {}
        # specific for MeetingItem POD Templates
        item_replacements = {}

        self.updatePODTemplatesCode(replacements, meeting_replacements, item_replacements)

    def run(self,
            profile_name=u'profile-Products.MeetingCommunes:default',
            extra_omitted=[]):
        # change self.profile_name that is reinstalled at the beginning of the PM migration
        self.profile_name = profile_name

        # fix used WFs before reinstalling
        self._fixUsedMeetingWFs()

        # add a new DashboardPodTemplate in contacts directory
        self._add_dashboard_pod_template_export_users_groups()

        # fix some instructions in POD templates
        self._mc_fixPODTemplatesInstructions()

        # call steps from Products.PloneMeeting
        super(Migrate_To_4200, self).run(extra_omitted=extra_omitted)

        # add new searches (searchitemswithnofinanceadvice)
        self.addNewSearches()

        # now MeetingCommunes specific steps
        logger.info('Migrating to MeetingCommunes 4200...')


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Change MeetingConfig.meetingWorkflow to use meeting_workflow/meetingitem_workflow;
       2) Call PloneMeeting migration to 4200;
       3) In _after_reinstall hook, adapt items and meetings workflow_history
          to reflect new defined workflow done in 1);
       4) Add new searches.
    '''
    migrator = Migrate_To_4200(context)
    migrator.run()
    migrator.finish()
