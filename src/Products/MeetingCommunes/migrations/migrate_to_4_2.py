# -*- coding: utf-8 -*-

from Products.PloneMeeting.migrations.migrate_to_4200 import Migrate_To_4200 as PMMigrate_To_4200

import logging


logger = logging.getLogger('MeetingCommunes')


class Migrate_To_4200(PMMigrate_To_4200):

    def _updateMeetingWFs(self):
        """meetingcommunes_workflow does not exist anymore, we use meeting_workflow."""
        logger.info("Adapting 'meetingWorkflow' for every MeetingConfigs...")
        for cfg in self.tool.objectValues('MeetingConfig'):
            if cfg.getMeetingWorkflow() == 'meetingcommunes_workflow':
                cfg.setMeetingWorkflow('meeting_workflow')
                cfg.at_post_edit_script()
        logger.info('Done.')

    def run(self,
            profile_name=u'profile-Products.MeetingCommunes:default',
            extra_omitted=[]):
        # change self.profile_name that is reinstalled at the beginning of the PM migration
        self.profile_name = profile_name

        self._updateMeetingWFs()

        # call steps from Products.PloneMeeting
        super(Migrate_To_4200, self).run(extra_omitted=extra_omitted)

        # now MeetingCommunes specific steps
        logger.info('Migrating to MeetingCommunes 4200...')


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Change MeetingConfig.meetingWorkflow to use meeting_workflow.
    '''
    migrator = Migrate_To_4200(context)
    migrator.run()
    migrator.finish()
