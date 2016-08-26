# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2016 by Imio.be
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier Bastien <g.bastien@imio.be>, Stephan Geulette <s.geulette@imio.be>"""
__docformat__ = 'plaintext'


import os
import logging
logger = logging.getLogger('MeetingCommunes: setuphandlers')
from DateTime import DateTime
from plone import api
from plone.app.blob.tests.utils import makeFileUpload
from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import createContentInContainer
from Products.CMFPlone.utils import _createObjectByType
from Products.PloneMeeting.exportimport.content import ToolInitializer
from Products.PloneMeeting.interfaces import IAnnexable
from Products.PloneMeeting.model.adaptations import performWorkflowAdaptations
from Products.MeetingCommunes.config import PROJECTNAME


def isNotMeetingCommunesProfile(context):
    return context.readDataFile("MeetingCommunes_marker.txt") is None


def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotMeetingCommunesProfile(context):
        return
    wft = api.portal.get_tool('portal_workflow')
    wft.updateRoleMappings()


def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotMeetingCommunesProfile(context):
        return
    logStep("postInstall", context)
    site = context.getSite()
    # need to reinstall PloneMeeting after reinstalling MC workflows to re-apply wfAdaptations
    reinstallPloneMeeting(context, site)
    showHomeTab(context, site)
    reorderSkinsLayers(context, site)


def logStep(method, context):
    logger.info("Applying '%s' in profile '%s'" %
                (method, '/'.join(context._profile_path.split(os.sep)[-3:])))


def isMeetingCommunesConfigureProfile(context):
    return context.readDataFile("MeetingCommunes_examples_fr_marker.txt") or \
        context.readDataFile("MeetingCommunes_cpas_marker.txt") or \
        context.readDataFile("MeetingCommunes_bourgmestre_marker.txt") or \
        context.readDataFile("MeetingCommunes_codir_marker.txt") or \
        context.readDataFile("MeetingCommunes_ca_marker.txt") or \
        context.readDataFile("MeetingCommunes_coges_marker.txt") or \
        context.readDataFile("MeetingCommunes_zones_marker.txt") or \
        context.readDataFile("MeetingCommunes_ag_marker.txt") or \
        context.readDataFile("MeetingCommunes_etat_major_marker.txt") or \
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
    # PloneMeeting is no more a dependency to avoid
    # magic between quickinstaller and portal_setup
    # so install it manually
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


def reorderSkinsLayers(context, site):
    """
       Re-apply MeetingCommunes skins.xml step as the reinstallation of
       MeetingCommunes and PloneMeeting changes the portal_skins layers order
    """
    if isNotMeetingCommunesProfile(context) and not isMeetingCommunesConfigureProfile(context):
        return

    logStep("reorderSkinsLayers", context)
    site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingCommunes:default', 'skins')


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
    # add the test users 'dfin' and 'bourgmestre' to every '_powerobservers' groups
    mTool = api.portal.get_tool('portal_membership')
    groupsTool = api.portal.get_tool('portal_groups')
    member = mTool.getMemberById(specialUserId)
    for memberId in ('dfin', 'bourgmestre', ):
        member = mTool.getMemberById(memberId)
        if member:
            groupsTool.addPrincipalToGroup(member.getId(), '%s_powerobservers' % meetingConfig1Id)
            groupsTool.addPrincipalToGroup(member.getId(), '%s_powerobservers' % meetingConfig2Id)
    # add the test user 'conseiller' only to the 'meeting-config-council_powerobservers' group
    member = mTool.getMemberById('conseiller')
    if member:
        groupsTool.addPrincipalToGroup(member.getId(), '%s_powerobservers' % meetingConfig2Id)

    # add the test user 'dfin' and 'chefCompta' to the 'meeting-config-xxx_budgetimpacteditors' groups
    for memberId in ('dfin', 'chefCompta', ):
        member = mTool.getMemberById(memberId)
        if member:
            groupsTool.addPrincipalToGroup(memberId, '%s_budgetimpacteditors' % meetingConfig1Id)
            groupsTool.addPrincipalToGroup(memberId, '%s_budgetimpacteditors' % meetingConfig2Id)

    # add some topics to the portlet_todo
    mc_college_or_bp = getattr(site.portal_plonemeeting, meetingConfig1Id)
    mc_college_or_bp.setToDoListSearches(
        [getattr(mc_college_or_bp.searches.searches_items, 'searchdecideditems'),
         getattr(mc_college_or_bp.searches.searches_items, 'searchallitemsincopy'),
         getattr(mc_college_or_bp.searches.searches_items, 'searchitemstoadvicewithdelay'),
         getattr(mc_college_or_bp.searches.searches_items, 'searchallitemstoadvice'),
         ])

    # add some topics to the portlet_todo
    mc_council_or_cas = getattr(site.portal_plonemeeting, meetingConfig2Id)
    mc_council_or_cas.setToDoListSearches(
        [getattr(mc_council_or_cas.searches.searches_items, 'searchdecideditems'),
         getattr(mc_council_or_cas.searches.searches_items, 'searchallitemsincopy'),
         ])

    # finally, re-launch plonemeetingskin and MeetingCommunes skins step
    # because PM has been installed before the import_data profile and messed up skins layers
    site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingCommunes:default', 'skins')
    # define default workflowAdaptations for council
    # due to some weird problems, the wfAdaptations can not be defined
    # thru the import_data...
    mc_council_or_cas.setWorkflowAdaptations(['no_global_observation', 'no_publication'])
    performWorkflowAdaptations(mc_council_or_cas, logger)


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
    css = ['imio.dashboard.css',
           'plonemeeting.css',
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
    tool = api.portal.get_tool('portal_plonemeeting')
    cfg = getattr(tool, 'meeting-config-college')
    wfTool = api.portal.get_tool('portal_workflow')
    pTool = api.portal.get_tool('plone_utils')
    mTool = api.portal.get_tool('portal_membership')
    # first we need to be sure that our IPoneMeetingLayer is set correctly
    # https://dev.plone.org/ticket/11673
    from zope.event import notify
    from zope.traversing.interfaces import BeforeTraverseEvent
    notify(BeforeTraverseEvent(site, site.REQUEST))
    # we will create elements for some users, make sure their personal
    # area is correctly configured
    # first make sure the 'Members' folder exists
    members = mTool.getMembersFolder()
    if members is None:
        _createObjectByType('Folder', site, id='Members')
    mTool.createMemberArea('agentPers')
    mTool.createMemberArea('agentInfo')
    mTool.createMemberArea('agentCompta')
    # create 5 meetings : 2 passed, 1 current and 2 future
    today = DateTime()
    dates = [today - 13, today - 6, today + 1, today + 8, today + 15]

    # items dict here : the key is the user we will create the item for
    # we use item templates so content is created for the demo
    items = {'agentPers': ({'templateId': 'template3',
                            'title': u'Engagement temporaire d\'un informaticien',
                            'budgetRelated': True,
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
             'dgen': ({'templateId': 'template1',
                                     'title': u'Tutelle CPAS : point 1 BP du 15 juin',
                                     'budgetRelated': False,
                                     'review_state': 'created', },
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
    # login as 'dgen'
    mTool.createMemberArea('dgen')
    for cfg in tool.objectValues('MeetingConfig'):
        secrFolder = tool.getPloneMeetingFolder(cfg.getId(), 'dgen')
        # create meetings
        for date in dates:
            meetingId = secrFolder.invokeFactory(cfg.getMeetingTypeName(), id=date.strftime('%Y%m%d'))
            meeting = getattr(secrFolder, meetingId)
            meeting.setDate(date)
            pTool.changeOwnershipOf(meeting, 'dgen')
            meeting.processForm()
            # -13 meeting is closed
            if date == today - 13:
                wfTool.doActionFor(meeting, 'freeze')
                wfTool.doActionFor(meeting, 'decide')
                wfTool.doActionFor(meeting, 'close')
            # -6 meeting is frozen
            if date == today - 6:
                wfTool.doActionFor(meeting, 'freeze')
                wfTool.doActionFor(meeting, 'decide')
            meeting.reindexObject()

        # create items
        for userId in items:
            userFolder = tool.getPloneMeetingFolder(cfg.getId(), userId)
            for item in items[userId]:
                # get the template then clone it
                template = getattr(tool.getMeetingConfig(userFolder).itemtemplates, item['templateId'])
                newItem = template.clone(newOwnerId=userId,
                                         destFolder=userFolder,
                                         newPortalType=cfg.getItemTypeName())
                newItem.setTitle(item['title'])
                newItem.setBudgetRelated(item['budgetRelated'])
                if item['review_state'] in ['proposed', 'validated', ]:
                    wfTool.doActionFor(newItem, 'propose')
                if item['review_state'] == 'validated':
                    wfTool.doActionFor(newItem, 'validate')
                #add annexe and advise for one item in College
                if item['templateId'] == 'template3' and cfg.id == 'meeting-config-college':
                    cpt = 1
                    for annexeType in ('annexe', 'annexe', 'annexeBudget', 'annexeCahier'):
                        annex_title = 'CV Informaticien N°2016-%s' % (cpt)
                        annexFile = makeFileUpload('Je suis le contenu du fichier', 'CV-0%s.txt' % (cpt))
                        fileType = getattr(cfg.meetingfiletypes, annexeType)
                        IAnnexable(newItem).addAnnex(idCandidate=None,
                                                     annex_title=annex_title,
                                                     annex_file=annexFile,
                                                     relatedTo='item',
                                                     meetingFileTypeUID=fileType.UID())
                        cpt += 1
                    newItem.setOptionalAdvisers(('dirfin__rowid__unique_id_003', 'informatique'))
                    newItem.at_post_create_script()
                    createContentInContainer(newItem,
                                             'meetingadvice',
                                             **{'advice_group': 'informatique',
                                                'advice_type': u'positive',
                                                'advice_comment': RichTextValue(u"<p><strong>Lorem ipsum dolor sit amet</strong>, consectetur adipiscing elit. Aliquam efficitur sapien quam, vitae auctor augue iaculis eget. <BR />Nulla blandit enim lectus. Ut in nunc ligula. Nunc nec magna et mi dictum molestie eu vitae est.<BR />Vestibulum justo erat, congue vel metus sed, condimentum vestibulum tortor. Sed nisi enim, posuere at cursus at, tincidunt eu est. Proin rhoncus ultricies justo. Nunc finibus quam non dolor imperdiet, non aliquet mi tincidunt. Aliquam at mauris suscipit, maximus purus at, dictum lectus.</p>"
                                                                                "<p>Nunc faucibus sem eu congue varius. Vestibulum consectetur porttitor nisi. Phasellus ante nunc, elementum et bibendum sit amet, tincidunt vitae est. Morbi in odio sagittis, convallis turpis a, tristique quam. Vestibulum ut urna arcu. Etiam non odio ut felis porttitor elementum. Donec venenatis porta purus et scelerisque. Nullam dapibus nec erat at pellentesque. Aliquam placerat nunc molestie venenatis malesuada. Nam ac pretium justo, id imperdiet lacus.</p>"),
                                                'advice_observations': RichTextValue(u"<p>Pellentesque ac ipsum suscipit, egestas lectus nec, mattis velit. In hac habitasse platea dictumst. Aenean vitae tortor viverra sapien mattis pretium. Pellentesque dapibus, tellus vel vulputate euismod, velit enim congue elit, vitae mollis arcu risus quis arcu. Aliquam non ante eleifend, sodales dolor at, ullamcorper nulla. Donec eget tellus a risus laoreet vestibulum sed id ante. Ut mauris magna, ultricies vel imperdiet sed, pulvinar vel nisl. Aliquam quis nisl quam. <BR />"
                                                                                     "Morbi suscipit, tortor ullamcorper ultricies iaculis, quam mauris egestas sem, eu semper urna ante eget dolor. Phasellus sed rutrum est. Aliquam quis tincidunt ipsum. Phasellus sit amet maximus odio. Fusce quis accumsan magna. Donec iaculis pretium sodales.</p>")})
                if item['templateId'] == 'template5' and cfg.id == 'meeting-config-college':
                    newItem.setOptionalAdvisers(('dirgen',))
                    newItem.at_post_create_script()
                    createContentInContainer(newItem,
                                             'meetingadvice',
                                             **{'advice_group': 'dirgen',
                                                'advice_type': u'negative',
                                                'advice_comment': RichTextValue(u"<p><strong>Lorem ipsum dolor sit amet</strong>, consectetur adipiscing elit. Aliquam efficitur sapien quam, vitae auctor augue iaculis eget. <BR />Nulla blandit enim lectus. Ut in nunc ligula. Nunc nec magna et mi dictum molestie eu vitae est.<BR />Vestibulum justo erat, congue vel metus sed, condimentum vestibulum tortor. Sed nisi enim, posuere at cursus at, tincidunt eu est. Proin rhoncus ultricies justo. Nunc finibus quam non dolor imperdiet, non aliquet mi tincidunt. Aliquam at mauris suscipit, maximus purus at, dictum lectus.</p>"
                                                                                "<p>Nunc faucibus sem eu congue varius. Vestibulum consectetur porttitor nisi. Phasellus ante nunc, elementum et bibendum sit amet, tincidunt vitae est. Morbi in odio sagittis, convallis turpis a, tristique quam. Vestibulum ut urna arcu. Etiam non odio ut felis porttitor elementum. Donec venenatis porta purus et scelerisque. Nullam dapibus nec erat at pellentesque. Aliquam placerat nunc molestie venenatis malesuada. Nam ac pretium justo, id imperdiet lacus.</p>"),
                                                'advice_observations': RichTextValue(u"<p>Pellentesque ac ipsum suscipit, egestas lectus nec, mattis velit. In hac habitasse platea dictumst. Aenean vitae tortor viverra sapien mattis pretium. Pellentesque dapibus, tellus vel vulputate euismod, velit enim congue elit, vitae mollis arcu risus quis arcu. Aliquam non ante eleifend, sodales dolor at, ullamcorper nulla. Donec eget tellus a risus laoreet vestibulum sed id ante. Ut mauris magna, ultricies vel imperdiet sed, pulvinar vel nisl. Aliquam quis nisl quam. <BR />"
                                                                                     "Morbi suscipit, tortor ullamcorper ultricies iaculis, quam mauris egestas sem, eu semper urna ante eget dolor. Phasellus sed rutrum est. Aliquam quis tincidunt ipsum. Phasellus sit amet maximus odio. Fusce quis accumsan magna. Donec iaculis pretium sodales.</p>")})

                newItem.reindexObject()
        # adapt some parameters for config
        cfg.setEnableAnnexToPrint('enabled_for_printing')
        cfg.setEnableAnnexConfidentiality(True)
