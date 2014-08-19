# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('PloneMeeting')

from Products.PloneMeeting.migrations import Migrator


# The migration class ----------------------------------------------------------
class Migrate_To_3_3(Migrator):

    def run(self):
        logger.info('Migrating to MeetingCommunes 3.3...')
        # reinstall so skins and so on are correct
        self.reinstall(profiles=[u'profile-Products.MeetingCommunes:default', ])
        self.finish()


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Reinstall Products.MeetingCommunes so skin and so on are correct.
    '''
    Migrate_To_3_3(context).run()
# ------------------------------------------------------------------------------
