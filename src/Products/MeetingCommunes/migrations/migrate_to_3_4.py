# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('MeetingCommunes')

from Products.PloneMeeting.migrations import Migrator


# The migration class ----------------------------------------------------------
class Migrate_To_3_4(Migrator):

    def run(self):
        logger.info('Migrating to MeetingCommunes 3.4...')
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
