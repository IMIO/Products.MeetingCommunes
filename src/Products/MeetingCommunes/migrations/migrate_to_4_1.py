# -*- coding: utf-8 -*-

import logging
from Products.PloneMeeting.migrations.migrate_to_4_1 import Migrate_To_4_1 as PMMigrate_To_4_1

logger = logging.getLogger('MeetingCommunes')


# The migration class ----------------------------------------------------------
class Migrate_To_4_1(PMMigrate_To_4_1):

    def run(self, step=None):
        # change self.profile_name that is reinstalled at the beginning of the PM migration
        self.profile_name = u'profile-Products.MeetingCommunes:default'

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
