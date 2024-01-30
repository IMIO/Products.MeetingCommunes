# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# GNU General Public License (GPL)
#

from dexterity.localroles.utils import add_fti_configuration
from plone import api
from Products.MeetingCommunes.config import PROJECTNAME
from Products.PloneMeeting.exportimport.content import ToolInitializer

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
        context.readDataFile("MeetingCommunes_demo_marker.txt") or \
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
