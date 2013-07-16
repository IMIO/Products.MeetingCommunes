# ------------------------------------------------------------------------------
import logging
logger = logging.getLogger('MeetingCommunes')
from Products.PloneMeeting.migrations import Migrator


# The migration class ----------------------------------------------------------
class Migrate_To_3_0_3(Migrator):
    def __init__(self, context):
        Migrator.__init__(self, context)

    def _updateCopyGroupsLocalRoles(self):
        """Update local roles related to copyGroups.
           Set same situation as before removal of 'MeetingObserverLocalCopy'.
        """
        copyGroupsStates = ['validated',
                            'presented',
                            'itemfrozen',
                            'pre_accepted',
                            'accepted',
                            'accepted_but_modified',
                            'delayed',
                            'refused',
                            ]
        copyGroupsStatesWithPublication = list(copyGroupsStates)
        copyGroupsStatesWithPublication.append('itempublished')
        # first set correct value for meetingConfigs.itemCopyGroupsStates
        for cfg in self.portal.portal_plonemeeting.objectValues('MeetingConfig'):
            if 'itempublished' in cfg.listItemStates():
                cfg.setItemCopyGroupsStates(copyGroupsStatesWithPublication)
            else:
                cfg.setItemCopyGroupsStates(copyGroupsStates)
        brains = self.portal.portal_catalog(meta_type=('MeetingItem'))
        logger.info('Updating copyGroups local roles for %s MeetingItem objects...' % len(brains))
        for brain in brains:
            obj = brain.getObject()
            obj.updateCopyGroupsLocalRoles()
            # Update security as local_roles are modified by updateCopyGroupsLocalRoles
            obj.reindexObject(idxs=['allowedRolesAndUsers', ])
        logger.info('MeetingItems copyGroups local roles have been updated.')

    def run(self):
        logger.info('Migrating to PloneMeeting 3.0.3...')

        self._updateCopyGroupsLocalRoles()

        # reinstall regarding changes in workflows
        self.reinstall(profiles=[u'profile-Products.MeetingCommunes:default', ])
        self.finish()


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Reinstall MeetingCommunes
    '''
    Migrate_To_3_0_3(context).run()
# ------------------------------------------------------------------------------
