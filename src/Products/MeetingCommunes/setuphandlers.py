# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# GNU General Public License (GPL)
#

from collections import OrderedDict
from collective.iconifiedcategory.utils import calculate_category_id
from collective.iconifiedcategory.utils import get_config_root
from datetime import datetime
from datetime import timedelta
from dexterity.localroles.utils import add_fti_configuration
from imio.helpers.content import normalize_name
from plone import api
from plone import namedfile
from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import createContentInContainer
from Products.Archetypes.event import ObjectEditedEvent
from Products.CMFPlone.utils import _createObjectByType
from Products.MeetingCommunes.config import PROJECTNAME
from Products.MeetingCommunes.config import SAMPLE_TEXT
from Products.PloneMeeting.exportimport.content import ToolInitializer
from Products.PloneMeeting.utils import cleanMemoize
from Products.PloneMeeting.utils import org_id_to_uid
from zope.event import notify

import logging
import os


logger = logging.getLogger('MeetingCommunes: setuphandlers')


def isNotMeetingCommunesProfile(context):
    return context.readDataFile("MeetingCommunes_marker.txt") is None


def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isMeetingCommunesFinancesAdviceProfile(context):
        _configureDexterityLocalRolesField()
        # update portal_types of every MeetingConfig so
        # MeetingItem.allowed_content_types is updated
        tool = api.portal.get_tool('portal_plonemeeting')
        for cfg in tool.objectValues('MeetingConfig'):
            notify(ObjectEditedEvent(cfg))

    if isNotMeetingCommunesProfile(context):
        return
    logStep("postInstall", context)
    site = context.getSite()
    # need to reinstall PloneMeeting after reinstalling MC workflows to re-apply wfAdaptations
    _reinstallPloneMeeting(context, site)
    _showHomeTab(context, site)
    _reorderSkinsLayers(context, site)


def logStep(method, context):
    logger.info("Applying '%s' in profile '%s'" %
                (method, '/'.join(context._profile_path.split(os.sep)[-3:])))


def isMeetingCommunesConfigureProfile(context):
    return context.readDataFile("MeetingCommunes_ag_marker.txt") or \
        context.readDataFile("MeetingCommunes_audit_marker.txt") or \
        context.readDataFile("MeetingCommunes_bdc_marker.txt") or \
        context.readDataFile("MeetingCommunes_bourgmestre_marker.txt") or \
        context.readDataFile("MeetingCommunes_ca_marker.txt") or \
        context.readDataFile("MeetingCommunes_city_marker.txt") or \
        context.readDataFile("MeetingCommunes_codir_marker.txt") or \
        context.readDataFile("MeetingCommunes_codir_city_cpas_marker.txt") or \
        context.readDataFile("MeetingCommunes_codir_extended_marker.txt") or \
        context.readDataFile("MeetingCommunes_coges_marker.txt") or \
        context.readDataFile("MeetingCommunes_consultation_marker.txt") or \
        context.readDataFile("MeetingCommunes_coordinateOffice_marker.txt") or \
        context.readDataFile("MeetingCommunes_cpas_marker.txt") or \
        context.readDataFile("MeetingCommunes_cppt_marker.txt") or \
        context.readDataFile("MeetingCommunes_csss_marker.txt") or \
        context.readDataFile("MeetingCommunes_etat_major_marker.txt") or \
        context.readDataFile("MeetingCommunes_examples_fr_marker.txt") or \
        context.readDataFile("MeetingCommunes_executive_marker.txt") or \
        context.readDataFile("MeetingCommunes_negociation_marker.txt") or \
        context.readDataFile("MeetingCommunes_remunarate_marker.txt") or \
        context.readDataFile("MeetingCommunes_scresthome_marker.txt") or \
        context.readDataFile("MeetingCommunes_sippt_marker.txt") or \
        context.readDataFile("MeetingCommunes_technicalcommittee_marker.txt") or \
        context.readDataFile("MeetingCommunes_testing_marker.txt") or \
        context.readDataFile("MeetingCommunes_volonteers_marker.txt") or \
        context.readDataFile("MeetingCommunes_wellbeing_marker.txt") or \
        context.readDataFile("MeetingCommunes_cadvice_marker.txt") or \
        context.readDataFile("MeetingCommunes_zones_marker.txt")


def isNotMeetingCommunesExamplesFrProfile(context):
    return context.readDataFile("MeetingCommunes_examples_fr_marker.txt") is None


def isNotMeetingCommunesDemoProfile(context):
    return context.readDataFile("MeetingCommunes_demo_marker.txt") is None


def isMeetingCommunesFinancesAdviceProfile(context):
    return context.readDataFile("MeetingCommunes_financesadvice_marker.txt")


def isMeetingCommunesTestingProfile(context):
    return context.readDataFile("MeetingCommunes_testing_marker.txt")


def isMeetingCommunesMigrationProfile(context):
    return context.readDataFile("MeetingCommunes_migrations_marker.txt")


def installMeetingCommunes(context):
    if not isMeetingCommunesConfigureProfile(context):
        return
    logStep("installMeetingCommunes", context)
    portal = context.getSite()
    portal.portal_setup.runAllImportStepsFromProfile('profile-Products.MeetingCommunes:default')


def initializeTool(context):
    '''Initialises the PloneMeeting tool based on information from the current profile.'''
    if not isMeetingCommunesConfigureProfile(context):
        return

    logStep("initializeTool", context)
    # PloneMeeting is no more a dependency to avoid
    # magic between quickinstaller and portal_setup
    # so install it manually
    site = context.getSite()
    _installPloneMeeting(context, site)
    return ToolInitializer(context, PROJECTNAME).run()


def _reinstallPloneMeeting(context, site):
    '''Reinstall PloneMeeting so after install methods are called and applied,
       like performWorkflowAdaptations for example.'''

    logStep("reinstallPloneMeeting", context)
    _installPloneMeeting(context, site)


def _installPloneMeeting(context, site):
    profileId = u'profile-Products.PloneMeeting:default'
    site.portal_setup.runAllImportStepsFromProfile(profileId)


def _showHomeTab(context, site):
    """Make sure the 'home' tab is shown..."""
    logStep("showHomeTab", context)

    index_html = getattr(site.portal_actions.portal_tabs, 'index_html', None)
    if index_html:
        index_html.visible = True
    else:
        logger.info("The 'Home' tab does not exist !!!")


def _reorderSkinsLayers(context, site):
    """
       Re-apply MeetingCommunes skins.xml step as the reinstallation of
       MeetingCommunes and PloneMeeting changes the portal_skins layers order
    """
    logStep("reorderSkinsLayers", context)
    site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingCommunes:default', 'skins')


def _configureDexterityLocalRolesField():
    """Configure field meetingadvice.advice_group for meetingadvicefinances."""
    # meetingadvicefinances
    roles_config = {
        'advice_group': {
            'advice_given': {
                'advisers': {'roles': [], 'rel': ''}},
            'advicecreated': {
                u'financialprecontrollers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_controller': {
                u'financialcontrollers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_editor': {
                u'financialeditors': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_reviewer': {
                u'financialreviewers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'proposed_to_financial_manager': {
                u'financialmanagers': {'roles': [u'Editor', u'Reviewer', u'Contributor'], 'rel': ''}},
            'financial_advice_signed': {
                u'financialmanagers': {'roles': [u'Reviewer'], 'rel': ''}},
        }
    }
    msg = add_fti_configuration(portal_type='meetingadvicefinances',
                                configuration=roles_config['advice_group'],
                                keyname='advice_group',
                                force=True)
    if msg:
        logger.warn(msg)


def finalizeExampleInstance(context):
    """
       Some parameters can not be handled by the PloneMeeting installation,
       so we handle this here
    """
    if isNotMeetingCommunesDemoProfile(context) and isNotMeetingCommunesExamplesFrProfile(context):
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
    # in some tests, meetingConfig1Id/meetingConfig2Id was changed
    tool = site.portal_plonemeeting
    if hasattr(tool, meetingConfig1Id) and hasattr(tool, meetingConfig2Id):
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
        mc_college_or_bp = getattr(tool, meetingConfig1Id)
        mc_college_or_bp.setToDoListSearches(
            [getattr(mc_college_or_bp.searches.searches_items, 'searchdecideditems').UID(),
             getattr(mc_college_or_bp.searches.searches_items, 'searchallitemsincopy').UID(),
             getattr(mc_college_or_bp.searches.searches_items, 'searchitemstoadvicewithdelay').UID(),
             getattr(mc_college_or_bp.searches.searches_items, 'searchallitemstoadvice').UID(),
             ])

        # add some topics to the portlet_todo
        mc_council_or_cas = getattr(site.portal_plonemeeting, meetingConfig2Id)
        mc_council_or_cas.setToDoListSearches(
            [getattr(mc_council_or_cas.searches.searches_items, 'searchdecideditems').UID(),
             getattr(mc_council_or_cas.searches.searches_items, 'searchallitemsincopy').UID(),
             ])

    # finally, re-launch plonemeetingskin and MeetingCommunes skins step
    # because PM has been installed before the import_data profile and messed up skins layers
    site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingCommunes:default', 'skins')


def addDemoData(context):
    ''' '''
    if isNotMeetingCommunesDemoProfile(context):
        return

    site = context.getSite()
    tool = api.portal.get_tool('portal_plonemeeting')
    cfg = tool.objectValues('MeetingConfig')[0]
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
    today = datetime.now()
    dates = [today - timedelta(days=13),
             today - timedelta(days=6),
             today + timedelta(days=1),
             today + timedelta(days=8),
             today + timedelta(days=15)]

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
        # cleanMemoize so ToolPloneMeeting.getMeetingConfig returns the correct MeetingConfig
        cleanMemoize(site)
        secrFolder = tool.getPloneMeetingFolder(cfg.getId(), 'dgen')
        # build attendees and signatories passed to Meeting._doUpdateContacts
        # attendees OrderedDict([('uid1', 'attendee'), ('uid2', 'attendee'), ('uid3', 'absent')])
        # signatories {'uid1': '1'}
        attendees = OrderedDict()
        signatories = {}
        for hp_uid in cfg.getOrderedContacts():
            attendees[hp_uid] = 'attendee'
        signatories = {attendees.keys()[1]: '1',
                       attendees.keys()[0]: '2'}
        # create meetings
        for date in dates:
            meetingId = secrFolder.invokeFactory(
                cfg.getMeetingTypeName(),
                id=date.strftime('%Y%m%d'),
                date=date)
            meeting = getattr(secrFolder, meetingId)
            pTool.changeOwnershipOf(meeting, 'dgen')
            meeting._do_update_contacts(attendees=attendees, signatories=signatories)
            # -13 meeting is closed
            if date == today - timedelta(days=13):
                wfTool.doActionFor(meeting, 'freeze')
                wfTool.doActionFor(meeting, 'decide')
                wfTool.doActionFor(meeting, 'close')
            # -6 meeting is frozen
            if date == today - timedelta(days=6):
                wfTool.doActionFor(meeting, 'freeze')
                wfTool.doActionFor(meeting, 'decide')
            meeting.reindexObject()

            for item in meeting.get_items():
                pTool.changeOwnershipOf(item, 'dgen')

        # create items
        for userId in items:
            userFolder = tool.getPloneMeetingFolder(cfg.getId(), userId)
            for item in items[userId]:
                # get the template then clone it
                template = getattr(tool.getMeetingConfig(userFolder).itemtemplates, item['templateId'])
                with api.env.adopt_user(username=userId):
                    tool.invalidateAllCache()
                    newItem = template.clone(newOwnerId=userId,
                                             destFolder=userFolder,
                                             newPortalType=cfg.getItemTypeName())
                    newItem.setTitle(item['title'])
                    newItem.setBudgetRelated(item['budgetRelated'])
                    if item['review_state'] == 'proposed':
                        wfTool.doActionFor(newItem, 'propose')

                if item['review_state'] == 'validated':
                    wfTool.doActionFor(newItem, 'validate')
                # add annexe and advice for one item in College
                if item['templateId'] == 'template3' and cfg.id == 'meeting-config-college':
                    cpt = 1
                    annexes_config_root = get_config_root(newItem)
                    for annexType in ('annexe', 'annexe', 'annexeBudget', 'annexeCahier'):
                        annex_title = u'CV Informaticien N°2016-%s' % (cpt)
                        annex_file = namedfile.NamedBlobFile('Je suis le contenu du fichier',
                                                             filename=u'CV-0%s.txt' % (cpt))
                        annexTypeId = calculate_category_id(annexes_config_root.get(annexType))
                        annex_id = normalize_name(site.REQUEST, annex_title)
                        api.content.create(container=newItem,
                                           id=annex_id,
                                           type='annex',
                                           title=annex_title,
                                           file=annex_file,
                                           content_category=annexTypeId,
                                           to_print=False,
                                           confidential=False)
                        cpt += 1
                    newItem.setOptionalAdvisers(('{0}__rowid__unique_id_003'.format(org_id_to_uid('dirfin')),
                                                 org_id_to_uid('informatique')))
                    newItem.at_post_create_script()
                    createContentInContainer(newItem,
                                             'meetingadvice',
                                             **{'advice_group': org_id_to_uid('informatique'),
                                                'advice_type': u'positive',
                                                'advice_comment': RichTextValue(SAMPLE_TEXT),
                                                'advice_observations': RichTextValue()})
                if item['templateId'] == 'template5' and cfg.id == 'meeting-config-college':
                    newItem.setOptionalAdvisers((org_id_to_uid('dirgen'), ))
                    newItem.at_post_create_script()
                    createContentInContainer(newItem,
                                             'meetingadvice',
                                             **{'advice_group': org_id_to_uid('dirgen'),
                                                'advice_type': u'negative',
                                                'advice_comment': RichTextValue(SAMPLE_TEXT),
                                                'advice_observations': RichTextValue(SAMPLE_TEXT)})

                newItem.reindexObject()

        # adapt some parameters for config
        cfg.setAnnexToPrintMode('enabled_for_info')
