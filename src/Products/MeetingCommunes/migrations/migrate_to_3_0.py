# ------------------------------------------------------------------------------
import logging
logger = logging.getLogger('MeetingCommunes')
from Products.PloneMeeting.config import TOPIC_SEARCH_SCRIPT, POWEROBSERVERS_GROUP_SUFFIX


def migrate(context):
    '''Call every migration steps.'''
    logger.info('Migrating to MeetingCommunes 3.0...')
    portal = context.portal_url.getPortalObject()
    _adaptItemsToValidateTopic(portal)
    _removeGlobalPowerObservers(portal)
    portal.portal_setup.runAllImportStepsFromProfile(u'profile-Products.MeetingCommunes:default')


def _adaptItemsToValidateTopic(portal):
    """
      Old versions of the searchitemstovalidate topic did not use a search script, correct this!
    """
    logger.info("Adding a searchScript to the 'searchitemstovalidate' topic")
    for cfg in portal.portal_plonemeeting.objectValues('MeetingConfig'):
        topic = getattr(cfg.topics, 'searchitemstovalidate', None)
        if topic:
            if not topic.hasProperty(TOPIC_SEARCH_SCRIPT):
                topic.manage_addProperty(TOPIC_SEARCH_SCRIPT, 'searchItemsToValidate', 'string')
            else:
                topic.manage_changeProperties(topic_search_script='searchItemsToValidate')


def _removeGlobalPowerObservers(portal):
    """
      Before, PowerObservers where global to every meetingConfig, now
      that PowerObservers are locally defined for each meetingConfig,
      remove the useless 'MeetingPowerObserver' role, remove the useless
      'meetingpowerobservers' group and put users of these groups in relevant
      '_powerobservers' suffixed groups for active meetingConfigs.
    """
    logger.info("Migrating from global PowerObservers to local PowerObservers")
    # remove the 'meetingpowerobservers' group
    # put every users of this group to '_powerobservers' suffixed groups of active meetingConfigs
    # generate a list of groups to transfer users to
    localPowerObserversGroupIds = []
    for cfg in portal.portal_plonemeeting.getActiveConfigs():
        localPowerObserversGroupIds.append("%s_%s" % (cfg.getId(), POWEROBSERVERS_GROUP_SUFFIX))

    powerObserverGroup = portal.portal_groups.getGroupById('meetingpowerobservers')
    existingPowerObserverUserIds = powerObserverGroup and powerObserverGroup.getGroupMemberIds() or ()
    for localPowerObserversGroupId in localPowerObserversGroupIds:
        for existingPowerObserverUserId in existingPowerObserverUserIds:
            portal.portal_groups.addPrincipalToGroup(existingPowerObserverUserId, localPowerObserversGroupId)

    # remove the 'meetingpowerobservers' group
    # first remove every role given to the 'meetingpowerobservers' group
    meetingpowerobservers = portal.portal_groups.getGroupById('meetingpowerobservers')
    if meetingpowerobservers:
        for role in portal.acl_users.portal_role_manager.getRolesForPrincipal(meetingpowerobservers):
            portal.acl_users.portal_role_manager.removeRoleFromPrincipal(role, 'meetingpowerobservers')
        # remove the group
        portal.portal_groups.removeGroup('meetingpowerobservers')
    # remove the 'MeetingPowerObserver' role
    data = list(portal.__ac_roles__)
    if 'MeetingPowerObserver' in data:
        # first on the portal
        data.remove('MeetingPowerObserver')
        portal.__ac_roles__ = tuple(data)
        # then in portal_role_manager
        try:
            portal.acl_users.portal_role_manager.removeRole('MeetingPowerObserver')
        except KeyError:
            pass
