# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.config import PORTAL_CATEGORIES
from Products.MeetingCommunes.profiles.zcity import import_data as zcity
from Products.PloneMeeting.profiles import OrgDescriptor
from Products.PloneMeeting.profiles import patch_pod_templates
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import RecurringItemDescriptor


# Categories -------------------------------------------------------------------
# no category

# Users and groups -------------------------------------------------------------
# no user
groups = [OrgDescriptor('secretariat', 'Secrétariat Général', u'Secr'), ]

# Meeting configurations BASED on ZCITY ----------------------------------------
# BP
collegeMeeting = deepcopy(zcity.collegeMeeting)

collegeMeeting.id = 'meeting-config-zcollege'
collegeMeeting.title = 'Collège'
collegeMeeting.folderTitle = 'Collège'
collegeMeeting.shortName = 'ZCollege'
collegeMeeting.itemReferenceFormat = "python: 'COL/' + (here.hasMeeting() and " \
                                     "here.restrictedTraverse('@@pm_unrestricted_methods').getLinkedMeetingDate().strftime('%Y%m%d') or '') " \
                                     "+ '-' + str(here.getItemNumber(relativeTo='meeting', for_display=True))"
collegeMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.motivation',
      'tal_expression': "string:"},
     {'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Bureau décide de reporter le point.</p>"}
     ))
collegeMeeting.customAdvisers = []
collegeMeeting.powerObservers = deepcopy(zcity.collegeMeeting.powerObservers)

# use template file from profile examples_fr
patch_pod_templates(zcity.collegeTemplates, '../../examples_fr/templates/')

# College Pod templates ----------------------------------------------------------------

agendaTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplate.is_reusable = True
agendaTemplate.odt_file = '../../examples_fr/templates/oj.odt'
agendaTemplate.pod_formats = ['docx']
agendaTemplate.pod_portal_types = ['Meeting']
agendaTemplate.tal_condition = u'python:tool.isManager(cfg)'

agendaTemplatePDF = PodTemplateDescriptor('oj-2', 'Ordre du jour')
agendaTemplatePDF.pod_template_to_use = {'cfg_id': collegeMeeting.id, 'template_id': agendaTemplate.id}
agendaTemplatePDF.pod_formats = ['pdf']
agendaTemplatePDF.pod_portal_types = ['Meeting']

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.is_reusable = True
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['docx']
decisionsTemplate.pod_portal_types = ['Meeting']
decisionsTemplate.tal_condition = u'python:tool.isManager(cfg)'

decisionsTemplatePDF = PodTemplateDescriptor('pv-2', 'Procès-verbal')
decisionsTemplatePDF.pod_template_to_use = {'cfg_id': collegeMeeting.id, 'template_id': decisionsTemplate.id}
decisionsTemplatePDF.pod_formats = ['pdf']
decisionsTemplatePDF.pod_portal_types = ['Meeting']

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.is_reusable = True
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['docx' ]
itemTemplate.pod_portal_types = ['MeetingItem']
itemTemplate.tal_condition = u'python:tool.isManager(cfg)'

itemTemplatePDF = PodTemplateDescriptor('deliberation-2', 'Délibération')
itemTemplatePDF.pod_template_to_use = {'cfg_id': collegeMeeting.id, 'template_id': itemTemplate.id}
itemTemplatePDF.pod_formats = ['pdf']
itemTemplatePDF.pod_portal_types = ['MeetingItem']

dashboardExportTemplate = PodTemplateDescriptor('export', 'Export', dashboard=True)
dashboardExportTemplate.is_reusable = True
dashboardExportTemplate.odt_file = '../../examples_fr/templates/dashboard.ods'
dashboardExportTemplate.pod_formats = ['xlsx', ]
dashboardExportTemplate.tal_condition = u'python: context.absolute_url().endswith("/searches_items")'

dashboardMeetingAttendances = PodTemplateDescriptor(
    'attendance-stats', 'Statistiques de présences', dashboard=True)
dashboardMeetingAttendances.is_reusable = True
dashboardMeetingAttendances.odt_file = '../../examples_fr/templates/attendance-stats.ods'
dashboardMeetingAttendances.pod_formats = ['xlsx']
dashboardMeetingAttendances.tal_condition = u'python:False'
dashboardMeetingAttendances.roles_bypassing_talcondition = set(['Manager', 'MeetingManager'])
dashboardMeetingAttendances.dashboard_collections_ids = ['searchallmeetings']

collegeTemplates = [dashboardExportTemplate, dashboardMeetingAttendances, agendaTemplate, agendaTemplatePDF,
                    decisionsTemplate, decisionsTemplatePDF, itemTemplate, itemTemplatePDF]
collegeMeeting.podTemplates = collegeTemplates

# CAS
councilMeeting = deepcopy(zcity.councilMeeting)

councilMeeting.id = 'meeting-config-zcouncil'
councilMeeting.title = "Conseil"
councilMeeting.folderTitle = "Conseil"
councilMeeting.shortName = 'ZCouncil'

councilMeeting.categories = PORTAL_CATEGORIES
councilMeeting.usedItemAttributes = ['description',
                                     'copyGroups',
                                     'manuallyLinkedItems',
                                     'motivation',
                                     'notes',
                                     'observations',
                                     'privacy']
councilMeeting.insertingMethodsOnAddItem = (
    {'insertingMethod': 'on_privacy', 'reverse': '0'},
    {'insertingMethod': 'on_list_type', 'reverse': '0'},
    {'insertingMethod': 'on_proposing_groups', 'reverse': '0'})
councilMeeting.itemReferenceFormat = "python: 'CONSEIL/' + (here.hasMeeting() and " \
                                 "here.restrictedTraverse('@@pm_unrestricted_methods').getLinkedMeetingDate().strftime('%Y%m%d') or '') " \
                                 "+ '-' + str(here.getItemNumber(relativeTo='meeting', for_display=True))"
councilMeeting.itemColumns = [
    'static_item_reference',
    'Creator',
    'CreationDate',
    'ModificationDate',
    'review_state',
    'getProposingGroup',
    'advices',
    'meeting_date',
    'preferred_meeting_date',
    'actions']
councilMeeting.availableItemsListVisibleColumns = [
    'Creator', 'CreationDate', 'getProposingGroup', 'advices', 'actions']
councilMeeting.itemsListVisibleColumns = [
    u'static_item_reference', u'Creator', u'CreationDate', u'review_state',
    u'getProposingGroup', u'advices', u'actions']
councilMeeting.enabledAnnexesBatchActions = ['delete', 'download-annexes']
councilMeeting.dashboardItemsListingsFilters = ('c4', 'c6', 'c7', 'c8', 'c9', 'c10',
                                            'c11', 'c13', 'c14', 'c15', 'c29', 'c32')
councilMeeting.dashboardMeetingAvailableItemsFilters = ('c4', 'c11', 'c29', 'c32')
councilMeeting.dashboardMeetingLinkedItemsFilters = ('c4', 'c6', 'c7', 'c11', 'c19', 'c29', 'c32')
councilMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.motivation',
      'tal_expression': "string:"},
     {'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Conseil décide de reporter le point.</p>"}
     ))
councilMeeting.meetingConfigsToCloneTo = []
councilMeeting.customAdvisers = []
councilMeeting.powerObservers = deepcopy(zcity.councilMeeting.powerObservers)

# use template file from profile examples_fr
patch_pod_templates(zcity.councilTemplates, '../../examples_fr/templates/', collegeMeeting.id)

# Pod templates ----------------------------------------------------------------
agendaTemplateCouncil = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplateCouncil.pod_template_to_use = {'cfg_id': collegeMeeting.id, 'template_id': agendaTemplate.id}
agendaTemplateCouncil.pod_formats = ['docx']
agendaTemplateCouncil.pod_portal_types = ['Meeting']
agendaTemplateCouncil.tal_condition = u'python:tool.isManager(cfg)'

agendaTemplatePDFCouncil = PodTemplateDescriptor('oj-2', 'Ordre du jour')
agendaTemplatePDFCouncil.pod_template_to_use = {'cfg_id': collegeMeeting.id, 'template_id': agendaTemplate.id}
agendaTemplatePDFCouncil.pod_formats = ['pdf']
agendaTemplatePDFCouncil.pod_portal_types = ['Meeting']

decisionsTemplateCouncil = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplateCouncil.pod_template_to_use = {'cfg_id': collegeMeeting.id, 'template_id': decisionsTemplate.id}
decisionsTemplateCouncil.pod_formats = ['docx']
decisionsTemplateCouncil.pod_portal_types = ['Meeting']
decisionsTemplateCouncil.tal_condition = u'python:tool.isManager(cfg)'

decisionsTemplatePDFCouncil = PodTemplateDescriptor('pv-2', 'Procès-verbal')
decisionsTemplatePDFCouncil.pod_template_to_use = {'cfg_id': collegeMeeting.id, 'template_id': decisionsTemplate.id}
decisionsTemplatePDFCouncil.pod_formats = ['pdf']
decisionsTemplatePDFCouncil.pod_portal_types = ['Meeting']

itemTemplateCouncil = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplateCouncil.pod_template_to_use = {'cfg_id': collegeMeeting.id, 'template_id': itemTemplate.id}
itemTemplateCouncil.pod_formats = ['docx' ]
itemTemplateCouncil.pod_portal_types = ['MeetingItem']
itemTemplateCouncil.tal_condition = u'python:tool.isManager(cfg)'

itemTemplatePDFCouncil = PodTemplateDescriptor('deliberation-2', 'Délibération')
itemTemplatePDFCouncil.pod_template_to_use = {'cfg_id': collegeMeeting.id, 'template_id': itemTemplate.id}
itemTemplatePDFCouncil.pod_formats = ['pdf']
itemTemplatePDFCouncil.pod_portal_types = ['MeetingItem']

dashboardExportTemplateCouncil = PodTemplateDescriptor('export', 'Export', dashboard=True)
dashboardExportTemplateCouncil.pod_template_to_use = {'cfg_id': collegeMeeting.id,
                                                      'template_id': dashboardExportTemplate.id}
dashboardExportTemplateCouncil.pod_formats = ['xlsx', ]
dashboardExportTemplateCouncil.tal_condition = u'python: context.absolute_url().endswith("/searches_items")'

dashboardMeetingAttendancesCouncil = PodTemplateDescriptor(
    'attendance-stats', 'Statistiques de présences', dashboard=True)
dashboardMeetingAttendancesCouncil.pod_template_to_use = {'cfg_id': collegeMeeting.id,
                                                     'template_id': dashboardMeetingAttendances.id}
dashboardMeetingAttendancesCouncil.pod_formats = ['xlsx']
dashboardMeetingAttendancesCouncil.tal_condition = u'python:False'
dashboardMeetingAttendancesCouncil.roles_bypassing_talcondition = set(['Manager', 'MeetingManager'])
dashboardMeetingAttendancesCouncil.dashboard_collections_ids = ['searchallmeetings']

councilTemplates = [dashboardExportTemplateCouncil, dashboardMeetingAttendancesCouncil,
                    agendaTemplateCouncil, agendaTemplatePDFCouncil, decisionsTemplateCouncil,
                    decisionsTemplatePDFCouncil, itemTemplateCouncil, itemTemplatePDFCouncil]

councilMeeting.podTemplates = councilTemplates

councilMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance précédente',
        description='',
        proposingGroup='dirgen',
        decision='Procès-verbal approuvé'), ]

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=(collegeMeeting, councilMeeting, ),
    orgs=groups)
data.usersOutsideGroups = []
data.directory_position_types = list(zcity.data.directory_position_types)
