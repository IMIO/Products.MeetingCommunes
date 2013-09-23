# ------------------------------------------------------------------------------
import logging
logger = logging.getLogger('PloneMeeting')
from Products.PloneMeeting.migrations import Migrator


# The migration class ----------------------------------------------------------
class Migrate_To_3_0_4(Migrator):

    def run(self):
        logger.info('Migrating to MeetingCommunes 3.0.4...')
        # reinstall so update in meetingitemcouncil_workflow regarding backToCreated
        # transition renamed to backToItemCreated is applied
        self.reinstall(profiles=[u'profile-Products.MeetingCommunes:default', ])
        self.finish()


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Reinstall MeetingCommunes so workflow are updated (meetingitemcouncil_workflow);
    '''
    Migrate_To_3_0_4(context).run()
# ------------------------------------------------------------------------------
