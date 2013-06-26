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
from DateTime import DateTime
from Products.PloneMeeting.exportimport.content import ToolInitializer
from Products.PloneMeeting.model.adaptations import performWorkflowAdaptations
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



##code-section FOOT
def logStep(method, context):
    logger.info("Applying '%s' in profile '%s'" %
                (method, '/'.join(context._profile_path.split(os.sep)[-3:])))


def isMeetingCommunesConfigureProfile(context):
    return context.readDataFile("MeetingCommunes_examples_fr_marker.txt") or \
        context.readDataFile("MeetingCommunes_examples_marker.txt") or \
        context.readDataFile("MeetingCommunes_cpas_marker.txt") or \
        context.readDataFile("MeetingCommunes_testing_marker.txt")

def isNotMeetingCommunesDemoProfile(context):
    return context.readDataFile("MeetingCommunes_demo_marker.txt") is None

def isMeetingCommunesTestingProfile(context):
    return context.readDataFile("MeetingCommunes_testing_marker.txt")


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

def reinstallPloneMeeting(context, site):
    '''Reinstall PloneMeeting so after install methods are called and applied,
       like performWorkflowAdaptations for example.'''

    if isNotMeetingCommunesProfile(context):
        return

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
    if isNotMeetingCommunesProfile(context):
        return

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
    if isNotMeetingCommunesProfile(context) and not isMeetingCommunesConfigureProfile:
        return

    logStep("reinstallPloneMeetingSkin", context)
    try:
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:default')
        site.portal_setup.runAllImportStepsFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin')
    except KeyError:
        # if the Products.plonemeetingskin profile is not available
        # (not using plonemeetingskin or in testing?) we pass...
        pass


def finalizeExampleInstance(context):
    """
       Some parameters can not be handled by the PloneMeeting installation,
       so we handle this here
    """
    if not isMeetingCommunesConfigureProfile(context):
        return

    # finalizeExampleInstance will behave differently if on
    # a Commune instance or CPAS instance
    specialUserId = 'bourgmestre'
    meetingConfig1Id = 'meeting-config-college'
    meetingConfig2Id = 'meeting-config-council'
    if context.readDataFile("MeetingCommunes_cpas_marker.txt"):
        specialUserId = 'president'
        meetingConfig1Id = 'meeting-config-bp'
        meetingConfig2Id = 'meeting-config-cas'

    site = context.getSite()

    logStep("finalizeExampleInstance", context)
    # add the test user 'bourgmestre' to every '_powerobservers' groups
    member = site.portal_membership.getMemberById(specialUserId)
    if member:
        site.portal_groups.addPrincipalToGroup(member.getId(), '%s_powerobservers' % meetingConfig1Id)
        site.portal_groups.addPrincipalToGroup(member.getId(), '%s_powerobservers' % meetingConfig2Id)
    # add the test user 'conseiller' to only the every 'meeting-config-council_powerobservers' groups
    member = site.portal_membership.getMemberById('conseiller')
    if member:
        site.portal_groups.addPrincipalToGroup(member.getId(), '%s_powerobservers' % meetingConfig2Id)

    # define some parameters for 'meeting-config-college'
    # items are sendable to the 'meeting-config-council'
    mc_college_or_bp = getattr(site.portal_plonemeeting, meetingConfig1Id)
    mc_college_or_bp.setMeetingConfigsToCloneTo([meetingConfig2Id, ])
    # add some topcis to the portlet_todo
    mc_college_or_bp.setToDoListTopics(
        [getattr(mc_college_or_bp.topics, 'searchdecideditems'),
         getattr(mc_college_or_bp.topics, 'searchitemstovalidate'),
         getattr(mc_college_or_bp.topics, 'searchallitemsincopy'),
         getattr(mc_college_or_bp.topics, 'searchallitemstoadvice'),
         ])
    # call updateCloneToOtherMCActions inter alia
    mc_college_or_bp.at_post_edit_script()

    # define some parameters for 'meeting-config-council'
    mc_council_or_cas = getattr(site.portal_plonemeeting, meetingConfig2Id)
    # add some topcis to the portlet_todo
    mc_council_or_cas.setToDoListTopics(
        [getattr(mc_council_or_cas.topics, 'searchdecideditems'),
         getattr(mc_council_or_cas.topics, 'searchitemstovalidate'),
         getattr(mc_council_or_cas.topics, 'searchallitemsincopy'),
         ])

    # finally, re-launch plonemeetingskin and MeetingCommunes skins step
    # because PM has been installed before the import_data profile and messed up skins layers
    site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingCommunes:default', 'skins')
    site.portal_setup.runImportStepFromProfile(u'profile-plonetheme.imioapps:default', 'skins')
    site.portal_setup.runImportStepFromProfile(u'profile-plonetheme.imioapps:plonemeetingskin', 'skins')
    # define default workflowAdaptations for council
    # due to some weird problems, the wfAdaptations can not be defined
    # thru the import_data...
    mc_council_or_cas.setWorkflowAdaptations(['no_global_observation', 'no_publication'])
    performWorkflowAdaptations(site, mc_council_or_cas, logger)


def reorderCss(context):
    """
       Make sure CSS are correctly reordered in portal_css so things
       work as expected...
    """
    if isNotMeetingCommunesProfile(context) and not isMeetingCommunesConfigureProfile(context):
        return

    site = context.getSite()

    logStep("reorderCss", context)

    portal_css = site.portal_css
    css = ['plonemeeting.css',
           'meeting.css',
           'meetingitem.css',
           'meetingcommunes.css',
           'imioapps.css',
           'plonemeetingskin.css',
           'imioapps_IEFixes.css',
           'ploneCustom.css']
    for resource in css:
        portal_css.moveResourceToBottom(resource)


def addDemoData(context):
    ''' '''
    if isNotMeetingCommunesDemoProfile(context):
        return

    site = context.getSite()
    tool = getToolByName(site, 'portal_plonemeeting')
    wfTool = getToolByName(site, 'portal_workflow')
    pTool = getToolByName(site, 'plone_utils')
    # we will create elements for some users, make sure their personal
    # area is correctly configured
    site.portal_membership.createMemberArea('agentPers')
    site.portal_membership.createMemberArea('agentInfo')
    site.portal_membership.createMemberArea('agentCompta')
    # create 5 meetings : 2 passed, 1 current and 2 future
    today = DateTime()
    dates = [today-13, today-6, today+1, today+8, today+15]
    # login as 'secretaire'
    site.portal_membership.createMemberArea('secretaire')
    secrFolder = tool.getPloneMeetingFolder('meeting-config-college', 'secretaire')
    for date in dates:
        meetingId = secrFolder.invokeFactory('MeetingCollege', id=date.strftime('%Y%m%d'))
        meeting = getattr(secrFolder, meetingId)
        meeting.setDate(date)
        pTool.changeOwnershipOf(meeting, 'secretaire')
        meeting.processForm()
        # -13 meeting is closed
        if date == today-13:
            wfTool.doActionFor(meeting, 'freeze')
            wfTool.doActionFor(meeting, 'decide')
            wfTool.doActionFor(meeting, 'close')
        # -6 meeting is frozen
        if date == today-6:
            wfTool.doActionFor(meeting, 'freeze')
            wfTool.doActionFor(meeting, 'decide')
        meeting.reindexObject()

    # items dict here : the key is the user we will create the item for
    # we use item templates so content is created for the demo
    items = {'agentPers': ({'templateId': 'template3',
                            'title': u'Engagement temporaire d\'un informaticien',
                            'budgetRelated': False,
                            'review_state': 'validated', },
                           {'templateId': 'template2',
                            'title': u'Contrôle médical de Mr Antonio',
                            'budgetRelated': False,
                            'review_state': 'proposed', },
                           {'templateId': 'template2',
                            'title': u'Contrôle médical de Mlle Debbeus',
                            'budgetRelated': False,
                            'review_state': 'proposed', },
                           {'templateId': 'template2',
                            'title': u'Contrôle médical de Mme Hanck',
                            'budgetRelated': False,
                            'review_state': 'validated', },
                           {'templateId': 'template4',
                            'title': u'Prestation réduite Mme Untelle, instritutrice maternelle',
                            'budgetRelated': False,
                            'review_state': 'validated', },),
             'agentInfo': ({'templateId': 'template5',
                            'title': u'Achat nouveaux serveurs',
                            'budgetRelated': True,
                            'review_state': 'validated',
                            },
                           {'templateId': 'template5',
                            'title': u'Marché public, contestation entreprise Untelle SA',
                            'budgetRelated': False,
                            'review_state': 'validated',
                            },),
             'agentCompta': ({'templateId': 'template5',
                              'title': u'Présentation budget 2014',
                              'budgetRelated': True,
                              'review_state': 'validated',
                              },
                             {'templateId': 'template5',
                              'title': u'Plainte de Mme Daise, taxe immondice',
                              'budgetRelated': False,
                              'review_state': 'validated',
                              },
                             {'templateId': 'template5',
                              'title': u'Plainte de Mme Uneautre, taxe piscine',
                              'budgetRelated': False,
                              'review_state': 'proposed',
                              },),
             'secretaire': ({'templateId': 'template1',
                             'title': u'Tutelle CPAS : point 1 BP du 15 juin',
                             'budgetRelated': False,
                             'review_state': 'created',
                             },
                            {'templateId': 'template5',
                             'title': u'Tutelle CPAS : point 2 BP du 15 juin',
                             'budgetRelated': False,
                             'review_state': 'proposed',
                             },
                            {'templateId': 'template5',
                             'title': u'Tutelle CPAS : point 16 BP du 15 juin',
                             'budgetRelated': True,
                             'review_state': 'validated',
                             },),
             }
    for userId in items:
        userFolder = tool.getPloneMeetingFolder('meeting-config-college', userId)
        for item in items[userId]:
            # get the template then clone it
            template = getattr(tool.getMeetingConfig(userFolder).recurringitems, item['templateId'])
            newItem = template.clone(newOwnerId=userId)
            newItem.setTitle(item['title'])
            newItem.setBudgetRelated(item['budgetRelated'])
            if item['review_state'] in ['proposed', 'validated', ]:
                wfTool.doActionFor(newItem, 'propose')
            if item['review_state'] == 'validated':
                wfTool.doActionFor(newItem, 'validate')
            newItem.reindexObject()

##/code-section FOOT
