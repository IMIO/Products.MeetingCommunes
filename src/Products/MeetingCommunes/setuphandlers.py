# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2013 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier Bastien <g.bastien@imio.be>, Stephan Geulette <s.geulette@imio.be>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('MeetingCommunes: setuphandlers')
from Products.MeetingCommunes.config import PROJECTNAME
from Products.MeetingCommunes.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
from Products.PloneMeeting.config import TOPIC_TYPE, TOPIC_SEARCH_SCRIPT, TOPIC_TAL_EXPRESSION
from Products.PloneMeeting.exportimport.content import ToolInitializer
##/code-section HEAD


def isNotMeetingCommunesProfile(context):
    return context.readDataFile("MeetingCommunes_marker.txt") is None



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotMeetingCommunesProfile(context): return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotMeetingCommunesProfile(context):
        return
    logStep("postInstall", context)
    site = context.getSite()
    #need to reinstall PloneMeeting after reinstalling MC workflows to re-apply wfAdaptations
    reinstallPloneMeeting(context, site)
    showHomeTab(context, site)
    reinstallPloneMeetingSkin(context, site)
    reorderCss(context, site)



##code-section FOOT
def logStep(method, context):
    logger.info("Applying '%s' in profile '%s'"%(method, '/'.join(context._profile_path.split(os.sep)[-3:])))


def isMeetingCommunesConfigureProfile(context):
    return context.readDataFile("MeetingCommunes_examples_fr_marker.txt") or \
        context.readDataFile("MeetingCommunes_examples_marker.txt") or \
        context.readDataFile("MeetingCommunes_cpas_marker.txt") or \
        context.readDataFile("MeetingCommunes_tests_marker.txt")


def isMeetingCommunesMigrationProfile(context):
    return context.readDataFile("MeetingCommunes_migrations_marker.txt")


def installMeetingCommunes(context):
    """ Run the default profile"""
    if not isMeetingCommunesConfigureProfile(context):
        return
    logStep("installMeetingCommunes", context)
    portal = context.getSite()
    portal.portal_setup.runAllImportStepsFromProfile('profile-Products.MeetingCommunes:default')


def initializeTool(context):
    '''Initialises the PloneMeeting tool based on information from the current
       profile.'''
    if not isMeetingCommunesConfigureProfile(context):
        return

    logStep("initializeTool", context)
    #PloneMeeting is no more a dependency to avoid
    #magic between quickinstaller and portal_setup
    #so install it manually
    _installPloneMeeting(context)
    return ToolInitializer(context, PROJECTNAME).run()


def _addTopics(context, site):
    '''
       Add searches to the added meetingConfigs
       Proposed items, validated items and decided items
    '''
    logStep("_addTopics", context)
    topicsInfo = (
        # Items in state 'proposed'
        ('searchproposeditems',
        (('Type', 'ATPortalTypeCriterion', 'MeetingItem'),),
        ('proposed', ), "python: not here.portal_plonemeeting.userIsAmong('reviewers')", '',
         ),
        # Items that need to be validated
        ('searchitemstovalidate',
        (('Type', 'ATPortalTypeCriterion', 'MeetingItem'),),
        ('proposed', ), "python: here.portal_plonemeeting.userIsAmong('reviewers')", 'searchItemsToValidate',
         ),
        # Items in state 'validated'
        ('searchvalidateditems',
        (('Type', 'ATPortalTypeCriterion', 'MeetingItem'),),
        ('validated', ), '', '',
         ),
        # All 'decided' items
        ('searchdecideditems',
        (('Type', 'ATPortalTypeCriterion', 'MeetingItem'),),
        ('accepted', 'refused', 'delayed', 'accepted_but_modified',), '', '',
         ),
    )

    #Add these searches by meeting config
    for meetingConfig in site.portal_plonemeeting.objectValues("MeetingConfig"):
        for topicId, topicCriteria, stateValues, topicCondition, topicScript in topicsInfo:
            #if reinstalling, we need to check if the topic does not already exist
            if hasattr(meetingConfig.topics, topicId):
                continue
            meetingConfig.topics.invokeFactory('Topic', topicId)
            topic = getattr(meetingConfig.topics, topicId)
            topic.setExcludeFromNav(True)
            topic.setTitle(topicId)
            for criterionName, criterionType, criterionValue in topicCriteria:
                criterion = topic.addCriterion(field=criterionName,
                                                criterion_type=criterionType)
                topic.manage_addProperty(TOPIC_TYPE, criterionValue, 'string')
                criterionValue = '%s%s' % (criterionValue, meetingConfig.getShortName())
                criterion.setValue([criterionValue])
            topic.manage_addProperty(TOPIC_TAL_EXPRESSION, topicCondition, 'string')
            topic.manage_addProperty(TOPIC_SEARCH_SCRIPT, topicScript, 'string')

            stateCriterion = topic.addCriterion(field='review_state', criterion_type='ATListCriterion')
            stateCriterion.setValue(stateValues)
            topic.setLimitNumber(True)
            topic.setItemCount(20)
            topic.setSortCriterion('created', True)
            topic.setCustomView(True)
            topic.setCustomViewFields(['Title', 'CreationDate', 'Creator', 'review_state'])
            topic.reindexObject()


def reinstallPloneMeeting(context, site):
    '''Reinstall PloneMeeting so after install methods are called and applied,
       like performWorkflowAdaptations for example.'''

    if isNotMeetingCommunesProfile(context): return

    logStep("reinstallPloneMeeting", context)
    _installPloneMeeting(context)


def _installPloneMeeting(context):
    site = context.getSite()
    profileId = u'profile-Products.PloneMeeting:default'
    site.portal_setup.runAllImportStepsFromProfile(profileId)


def showHomeTab(context, site):
    """
       Make sure the 'home' tab is shown...
    """
    if isNotMeetingCommunesProfile(context): return

    logStep("showHomeTab", context)

    index_html = getattr(site.portal_actions.portal_tabs, 'index_html', None)
    if index_html:
        index_html.visible = True
    else:
        logger.info("The 'Home' tab does not exist !!!")


def reinstallPloneMeetingSkin(context, site):
    """
       Reinstall Products.plonemeetingskin as the reinstallation of MeetingCommunes
       change the portal_skins layers order
    """
    if isNotMeetingCommunesProfile(context) and not isMeetingCommunesConfigureProfile: return

    logStep("reinstallPloneMeetingSkin", context)
    try:
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:default')
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin')
    except KeyError:
        # if the Products.plonemeetingskin profile is not available
        # (not using plonemeetingskin or in tests?) we pass...
        pass


def finalizeExampleInstance(context):
    """
       Some parameters can not be handled by the PloneMeeting installation,
       so we handle this here
    """
    if not isMeetingCommunesConfigureProfile(context): return

    site = context.getSite()

    logStep("finalizeExampleInstance", context)
    # add the test user 'bourgmestre' to every '_powerobservers' groups
    member = site.portal_membership.getMemberById('bourgmestre')
    if member:
        site.portal_groups.addPrincipalToGroup(member.getId(), 'meeting-config-college_powerobservers')
        site.portal_groups.addPrincipalToGroup(member.getId(), 'meeting-config-council_powerobservers')
    # add the test user 'conseiller' to only the every 'meeting-config-council_powerobservers' groups
    member = site.portal_membership.getMemberById('conseiller')
    if member:
        site.portal_groups.addPrincipalToGroup(member.getId(), 'meeting-config-council_powerobservers')

    # add some topics
    _addTopics(context, site)

    # define some parameters for 'meeting-config-college'
    # items are sendable to the 'meeting-config-council'
    mc_college = getattr(site.portal_plonemeeting, 'meeting-config-college')
    mc_college.setMeetingConfigsToCloneTo(['meeting-config-council', ])
    # add some topcis to the portlet_todo
    mc_college.setToDoListTopics(
        [getattr(mc_college.topics, 'searchdecideditems'),
         getattr(mc_college.topics, 'searchitemstovalidate'),
         getattr(mc_college.topics, 'searchallitemsincopy'),
         getattr(mc_college.topics, 'searchallitemstoadvice'),
         ])
    # call updateCloneToOtherMCActions inter alia
    mc_college.at_post_edit_script()

    # define some parameters for 'meeting-config-council'
    mc_council = getattr(site.portal_plonemeeting, 'meeting-config-council')
    # add some topcis to the portlet_todo
    mc_council.setToDoListTopics(
        [getattr(mc_council.topics, 'searchdecideditems'),
         getattr(mc_council.topics, 'searchitemstovalidate'),
         getattr(mc_council.topics, 'searchallitemsincopy'),
         ])
    #finally, re-launch plonemeetingskin and MeetingCommunes skins step
    # because PM has been installed before the import_data profile and messed up skins layers
    site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingCommunes:default', 'skins')
    site.portal_setup.runImportStepFromProfile(u'profile-plonetheme.imioapps:default', 'skins')
    site.portal_setup.runImportStepFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin', 'skins')
    # call reoerderCss again because it is correctly called while re-installing MeetingCommunes
    # but not while a profile is called from PloneMeeting
    reorderCss(context, site)


def reorderCss(context, site):
    """
       Make sure CSS are correctly reordered in portal_css so things
       work as expected...
    """
    if isNotMeetingCommunesProfile(context):
        return

    logStep("reorderCss", context)

    portal_css = site.portal_css
    css = ['plonemeeting.css', 'meeting.css', 'meetingitem.css', 'meetingcommunes.css', 'imioapps.css', 'plonemeetingskin.css', 'ploneCustom.css']
    css.reverse()
    for resource in css:
        portal_css.moveResourceToBottom(css)

##/code-section FOOT
