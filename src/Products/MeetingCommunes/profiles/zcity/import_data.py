# -*- coding: utf-8 -*-

from copy import deepcopy
from DateTime import DateTime
from Products.MeetingCommunes.config import FINANCE_ADVICES_COLLECTION_ID
from Products.MeetingCommunes.config import PORTAL_CATEGORIES
from Products.MeetingCommunes.profiles.examples_fr import import_data as examples_fr_import_data
from Products.PloneMeeting.profiles import OrgDescriptor
from Products.PloneMeeting.profiles import patch_pod_templates
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import RecurringItemDescriptor


today = DateTime().strftime('%Y/%m/%d')

# Categories -------------------------------------------------------------------
categories = []

# Users and groups -------------------------------------------------------------
# no user
groups = [OrgDescriptor('dirgen', 'Directeur Général', u'DG'),
          OrgDescriptor('secretariat', 'Secrétariat Général', u'Secr'),
          OrgDescriptor('dirfin', 'Directeur Financier', u'DF')]

# Meeting configurations -------------------------------------------------------
# College
collegeMeeting = deepcopy(examples_fr_import_data.collegeMeeting)

collegeMeeting.shortName = 'College'
collegeMeeting.assembly = ''
collegeMeeting.assemblyStaves = ''
collegeMeeting.signatures = ''
collegeMeeting.certifiedSignatures = []
collegeMeeting.places = ''
collegeMeeting.usedItemAttributes = ['description',
                                     'copyGroups',
                                     'manuallyLinkedItems',
                                     'motivation',
                                     'notes',
                                     'observations',
                                     'otherMeetingConfigsClonableToPrivacy']
collegeMeeting.usedMeetingAttributes = ['start_date',
                                        'end_date',
                                        'excused',
                                        'place',
                                        'observations',
                                        'attendees',
                                        'signatories']
collegeMeeting.insertingMethodsOnAddItem = (
    {'insertingMethod': 'on_list_type', 'reverse': '0'},
    {'insertingMethod': 'on_proposing_groups', 'reverse': '0'})
collegeMeeting.itemReferenceFormat = \
    "python: 'COL/' + (here.hasMeeting() and " \
    "here.restrictedTraverse('@@pm_unrestricted_methods').getLinkedMeetingDate().strftime('%Y%m%d') or '') " \
    "+ '-' + str(here.getItemNumber(relativeTo='meeting', for_display=True))"
collegeMeeting.contentsKeptOnSentToOtherMC = ['annexes', 'decision_annexes', 'advices']
collegeMeeting.itemWFValidationLevels = (
    {'state': 'itemcreated',
     'state_title': 'itemcreated',
     'leading_transition': '-',
     'leading_transition_title': '-',
     'back_transition': 'backToItemCreated',
     'back_transition_title': 'backToItemCreated',
     'suffix': 'creators',
     'extra_suffixes': [],
     'enabled': '1',
     },
    {'state': 'proposed',
     'state_title': 'proposed',
     'leading_transition': 'propose',
     'leading_transition_title': 'propose',
     'back_transition': 'backToProposed',
     'back_transition_title': 'backToProposed',
     'suffix': 'reviewers',
     'extra_suffixes': [],
     'enabled': '1',
     },
    {'state': 'prevalidated',
     'state_title': 'prevalidated',
     'leading_transition': 'prevalidate',
     'leading_transition_title': 'prevalidate',
     'back_transition': 'backToPrevalidated',
     'back_transition_title': 'backToPrevalidated',
     'suffix': 'reviewers',
     'extra_suffixes': [],
     'enabled': '0',
     },
)
collegeMeeting.itemColumns = ['static_item_reference',
                              'Creator',
                              'CreationDate',
                              'ModificationDate',
                              'review_state',
                              'getProposingGroup',
                              'advices',
                              'meeting_date',
                              'preferred_meeting_date',
                              'actions']
collegeMeeting.transitionsToConfirm = (
    'Meeting.close', 'Meeting.backToDecided', 'MeetingItem.backToItemCreated', 'MeetingItem.refuse',
    'MeetingItem.backToProposed', 'MeetingItem.backTo_itemfrozen_from_returned_to_proposing_group',
    'MeetingItem.backTo_presented_from_returned_to_proposing_group', 'MeetingItem.delay',
    'MeetingItem.backToValidated', 'MeetingItem.return_to_proposing_group')
collegeMeeting.enabledAnnexesBatchActions = ['delete', 'download-annexes']
collegeMeeting.dashboardItemsListingsFilters = (
    'c4', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c13', 'c14', 'c15', 'c16', 'c29', 'c32')
collegeMeeting.dashboardMeetingAvailableItemsFilters = ('c4', 'c11', 'c16', 'c29', 'c32')
collegeMeeting.dashboardMeetingLinkedItemsFilters = ('c4', 'c6', 'c7', 'c11', 'c16', 'c19', 'c29', 'c32')
collegeMeeting.selectableAdvisers = []
collegeMeeting.itemAdviceStates = ('proposed', 'validated', 'presented')
collegeMeeting.itemAdviceEditStates = ('proposed', 'validated', 'presented')
collegeMeeting.itemAdviceViewStates = ('proposed',
                                       'validated',
                                       'presented',
                                       'itemfrozen',
                                       'returned_to_proposing_group',
                                       'pre_accepted',
                                       'accepted',
                                       'accepted_but_modified',
                                       'refused',
                                       'delayed')
collegeMeeting.usedAdviceTypes = [
    'positive', 'positive_with_comments', 'positive_with_remarks', 'cautious',
    'negative', 'negative_with_remarks', 'back_to_proposing_group', 'nil', 'read']
collegeMeeting.keepAccessToItemWhenAdviceIsGiven = True
collegeMeeting.transitionsReinitializingDelays = ['backToItemCreated']
# use template file from profile examples_fr
patch_pod_templates(collegeMeeting.podTemplates, '../../examples_fr/templates/')
# College Pod templates ----------------------------------------------------------------

agendaTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplate.is_reusable = True
agendaTemplate.odt_file = '../../examples_fr/templates/oj.odt'
agendaTemplate.pod_formats = ['docx']
agendaTemplate.pod_portal_types = ['Meeting']
agendaTemplate.tal_condition = u'python:tool.isManager(cfg)'

agendaTemplatePDF = PodTemplateDescriptor('oj-2', 'Ordre du jour')
agendaTemplatePDF.pod_template_to_use = {
    'cfg_id': collegeMeeting.id, 'template_id': agendaTemplate.id}
agendaTemplatePDF.pod_formats = ['pdf']
agendaTemplatePDF.pod_portal_types = ['Meeting']

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.is_reusable = True
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['docx']
decisionsTemplate.pod_portal_types = ['Meeting']
decisionsTemplate.tal_condition = u'python:tool.isManager(cfg)'

decisionsTemplatePDF = PodTemplateDescriptor('pv-2', 'Procès-verbal')
decisionsTemplatePDF.pod_template_to_use = {
    'cfg_id': collegeMeeting.id, 'template_id': decisionsTemplate.id}
decisionsTemplatePDF.pod_formats = ['pdf']
decisionsTemplatePDF.pod_portal_types = ['Meeting']

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.is_reusable = True
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['docx']
itemTemplate.pod_portal_types = ['MeetingItem']
itemTemplate.tal_condition = u'python:tool.isManager(cfg)'

itemTemplatePDF = PodTemplateDescriptor('deliberation-2', 'Délibération')
itemTemplatePDF.pod_template_to_use = {
    'cfg_id': collegeMeeting.id, 'template_id': itemTemplate.id}
itemTemplatePDF.pod_formats = ['pdf']
itemTemplatePDF.pod_portal_types = ['MeetingItem']

dfAdviceTemplate = PodTemplateDescriptor('avis-df', 'Avis DF')
dfAdviceTemplate.is_reusable = True
dfAdviceTemplate.odt_file = '../../examples_fr/templates/avis-df.odt'
dfAdviceTemplate.pod_formats = ['pdf']
dfAdviceTemplate.pod_portal_types = ['MeetingItem']
dfAdviceTemplate.tal_condition = u'python: context.adapted().showFinanceAdviceTemplate()'

dashboardExportTemplate = PodTemplateDescriptor('export', 'Export', dashboard=True)
dashboardExportTemplate.is_reusable = True
dashboardExportTemplate.odt_file = '../../examples_fr/templates/dashboard.ods'
dashboardExportTemplate.pod_formats = ['xlsx']
dashboardExportTemplate.tal_condition = u'python: context.absolute_url().endswith("/searches_items")'

dashboardDFTemplateOds = PodTemplateDescriptor(
    'synthese-avis-df-ods', 'Synthèse avis DF', dashboard=True)
dashboardDFTemplateOds.is_reusable = True
dashboardDFTemplateOds.odt_file = '../../examples_fr/templates/synthese-df-tb.ods'
dashboardDFTemplateOds.pod_formats = ['xlsx']
dashboardDFTemplateOds.dashboard_collections_ids = [FINANCE_ADVICES_COLLECTION_ID]

dashboardMeetingAttendances = PodTemplateDescriptor(
    'attendance-stats', 'Statistiques de présences', dashboard=True)
dashboardMeetingAttendances.is_reusable = True
dashboardMeetingAttendances.odt_file = '../../examples_fr/templates/attendance-stats.ods'
dashboardMeetingAttendances.pod_formats = ['xlsx']
dashboardMeetingAttendances.tal_condition = u'python:False'
dashboardMeetingAttendances.roles_bypassing_talcondition = set(['Manager', 'MeetingManager'])
dashboardMeetingAttendances.dashboard_collections_ids = ['searchallmeetings']

collegeTemplates = [
    dfAdviceTemplate, dashboardExportTemplate, dashboardDFTemplateOds,
    dashboardMeetingAttendances, agendaTemplate, agendaTemplatePDF, decisionsTemplate,
    decisionsTemplatePDF, itemTemplate, itemTemplatePDF]

collegeMeeting.customAdvisers = [
    {'row_id': 'unique_id_002',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '5',
     'delay_left_alert': '2',
     'delay_label': '≥ 30.000€ (urgent)',
     'available_on': "python: item.REQUEST.get('managing_available_delays', False)",
     'is_linked_to_previous_row': '0'},
    {'row_id': 'unique_id_003',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '10',
     'delay_left_alert': '4',
     'delay_label': '≥ 30.000€',
     'is_linked_to_previous_row': '1'},
    {'row_id': 'unique_id_004',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '20',
     'delay_left_alert': '4',
     'delay_label': '≥ 30.000€ (prolongé)',
     'available_on': "python: item.REQUEST.get('managing_available_delays', False)",
     'is_linked_to_previous_row': '1'},
]
collegeMeeting.powerObservers = (
    {'row_id': 'powerobservers',
     'label': 'Super observateurs',
     'item_states': ('validated',
                     'presented',
                     'itemfrozen',
                     'returned_to_proposing_group',
                     'pre_accepted',
                     'accepted',
                     'accepted_but_modified',
                     'delayed',
                     'refused'),
     'meeting_states': ('created', 'frozen', 'decided', 'closed'),
     'orderindex_': '1'},
    {'row_id': 'restrictedpowerobservers',
     'label': 'Super observateurs restreints',
     'item_states': ('itemfrozen',
                     'pre_accepted',
                     'returned_to_proposing_group',
                     'accepted',
                     'accepted_but_modified',
                     'delayed',
                     'refused'),
     'meeting_states': ('frozen', 'decided', 'closed'),
     'orderindex_': '2'})
collegeMeeting.workflowAdaptations = [
    'no_publication', 'refused', 'accepted_but_modified', 'delayed',
    'return_to_proposing_group', 'only_creator_may_delete', 'pre_accepted']
collegeMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.motivation',
      'tal_expression': "string:"},
     {'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Collège décide de reporter le point.</p>"}
     ))
collegeMeeting.onMeetingTransitionItemActionToExecute = (
    {'meeting_transition': 'freeze',
     'item_action': 'itemfreeze',
     'tal_expression': ''},

    {'meeting_transition': 'decide',
     'item_action': 'itemfreeze',
     'tal_expression': ''},

    {'meeting_transition': 'close',
     'item_action': 'itemfreeze',
     'tal_expression': ''},
    {'meeting_transition': 'close',
     'item_action': 'accept',
     'tal_expression': ''},)
collegeMeeting.selectableCopyGroups = []
collegeMeeting.styleTemplates = []
collegeMeeting.podTemplates = collegeTemplates
collegeMeeting.itemCopyGroupsStates = (
    'validated',
    'presented',
    'itemfrozen',
    'returned_to_proposing_group',
    'pre_accepted',
    'accepted',
    'accepted_but_modified',
    'delayed',
    'refused')
collegeMeeting.itemManualSentToOtherMCStates = (
    'accepted',
    'accepted_but_modified',
    'pre_accepted',
    'itemfrozen',
    'presented',
    'validated')
collegeMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance précédente',
        description='',
        proposingGroup='dirgen',
        decision='Procès-verbal approuvé')]
collegeMeeting.itemTemplates = []
collegeMeeting.initItemDecisionIfEmptyOnDecide = False
collegeMeeting.meetingPresentItemWhenNoCurrentMeetingStates = ("created", "frozen")
collegeMeeting.itemBudgetInfosStates = []

# Council
councilMeeting = deepcopy(examples_fr_import_data.councilMeeting)

# Pod templates ----------------------------------------------------------------
agendaTemplateCouncil = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplateCouncil.is_reusable = True
agendaTemplateCouncil.odt_file = '../../examples_fr/templates/oj.odt'
agendaTemplateCouncil.pod_formats = ['docx']
agendaTemplateCouncil.pod_portal_types = ['Meeting']
agendaTemplateCouncil.tal_condition = u'python:tool.isManager(cfg)'

agendaTemplatePDFCouncil = PodTemplateDescriptor('oj-2', 'Ordre du jour')
agendaTemplatePDFCouncil.pod_template_to_use = {
    'cfg_id': councilMeeting.id, 'template_id': agendaTemplateCouncil.id}
agendaTemplatePDFCouncil.pod_formats = ['pdf']
agendaTemplatePDFCouncil.pod_portal_types = ['Meeting']

decisionsTemplateCouncil = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplateCouncil.is_reusable = True
decisionsTemplateCouncil.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplateCouncil.pod_formats = ['docx']
decisionsTemplateCouncil.pod_portal_types = ['Meeting']
decisionsTemplateCouncil.tal_condition = u'python:tool.isManager(cfg)'

decisionsTemplatePDFCouncil = PodTemplateDescriptor('pv-2', 'Procès-verbal')
decisionsTemplatePDFCouncil.pod_template_to_use = {
    'cfg_id': councilMeeting.id, 'template_id': decisionsTemplateCouncil.id}
decisionsTemplatePDFCouncil.pod_formats = ['pdf']
decisionsTemplatePDFCouncil.pod_portal_types = ['Meeting']

itemTemplateCouncil = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplateCouncil.is_reusable = True
itemTemplateCouncil.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplateCouncil.pod_formats = ['docx']
itemTemplateCouncil.pod_portal_types = ['MeetingItem']
itemTemplateCouncil.tal_condition = u'python:tool.isManager(cfg)'

itemTemplatePDFCouncil = PodTemplateDescriptor('deliberation-2', 'Délibération')
itemTemplatePDFCouncil.pod_template_to_use = {
    'cfg_id': councilMeeting.id, 'template_id': itemTemplateCouncil.id}
itemTemplatePDFCouncil.pod_formats = ['pdf']
itemTemplatePDFCouncil.pod_portal_types = ['MeetingItem']

dfAdviceTemplateCouncil = PodTemplateDescriptor('avis-df', 'Avis DF')
dfAdviceTemplateCouncil.pod_template_to_use = {
    'cfg_id': collegeMeeting.id, 'template_id': dfAdviceTemplate.id}
dfAdviceTemplateCouncil.pod_formats = ['pdf']
dfAdviceTemplateCouncil.pod_portal_types = ['MeetingItem']
dfAdviceTemplateCouncil.tal_condition = u'python: context.adapted().showFinanceAdviceTemplate()'

dashboardExportTemplateCouncil = PodTemplateDescriptor('export', 'Export', dashboard=True)
dashboardExportTemplateCouncil.pod_template_to_use = {'cfg_id': collegeMeeting.id,
                                                      'template_id': dashboardExportTemplate.id}
dashboardExportTemplateCouncil.pod_formats = ['xlsx']
dashboardExportTemplateCouncil.tal_condition = u'python: context.absolute_url().endswith("/searches_items")'

dashboardDFTemplateOdsCouncil = PodTemplateDescriptor(
    'synthese-avis-df-ods', 'Synthèse avis DF', dashboard=True)
dashboardDFTemplateOdsCouncil.pod_template_to_use = {
    'cfg_id': collegeMeeting.id, 'template_id': dashboardDFTemplateOds.id}
dashboardDFTemplateOdsCouncil.pod_formats = ['xlsx']
dashboardDFTemplateOdsCouncil.dashboard_collections_ids = [FINANCE_ADVICES_COLLECTION_ID]

dashboardMeetingAttendancesCouncil = PodTemplateDescriptor(
    'attendance-stats', 'Statistiques de présences', dashboard=True)
dashboardMeetingAttendancesCouncil.pod_template_to_use = {
    'cfg_id': collegeMeeting.id, 'template_id': dashboardMeetingAttendances.id}
dashboardMeetingAttendancesCouncil.pod_formats = ['xlsx']
dashboardMeetingAttendancesCouncil.tal_condition = u'python:False'
dashboardMeetingAttendancesCouncil.roles_bypassing_talcondition = set(['Manager', 'MeetingManager'])
dashboardMeetingAttendancesCouncil.dashboard_collections_ids = ['searchallmeetings']

pubTemplate = PodTemplateDescriptor('publications', 'Publications (www.deliberations.be)')
pubTemplate.odt_file = '../../examples_fr/templates/publications.odt'
pubTemplate.pod_formats = ['pdf']
pubTemplate.pod_portal_types = ['Meeting']
pubTemplate.tal_condition = u'python:tool.isManager(cfg)'

councilTemplates = [
    dfAdviceTemplateCouncil, dashboardExportTemplateCouncil,
    dashboardDFTemplateOdsCouncil, dashboardMeetingAttendancesCouncil,
    agendaTemplateCouncil, agendaTemplatePDFCouncil, decisionsTemplateCouncil,
    decisionsTemplatePDFCouncil, itemTemplateCouncil, itemTemplatePDFCouncil, pubTemplate]

councilMeeting.shortName = 'Council'
councilMeeting.assembly = ''
councilMeeting.signatures = ''
councilMeeting.assemblyStaves = ''
councilMeeting.certifiedSignatures = []
councilMeeting.places = ''
councilMeeting.categories = PORTAL_CATEGORIES
councilMeeting.usedItemAttributes = ['description',
                                     'category',
                                     'copyGroups',
                                     'manuallyLinkedItems',
                                     'motivation',
                                     'notes',
                                     'observations',
                                     'privacy']
councilMeeting.usedMeetingAttributes = ['start_date',
                                        'end_date',
                                        'excused',
                                        'place',
                                        'observations',
                                        'attendees',
                                        'signatories']
councilMeeting.insertingMethodsOnAddItem = (
    {'insertingMethod': 'on_privacy', 'reverse': '0'},
    {'insertingMethod': 'on_list_type', 'reverse': '0'},
    {'insertingMethod': 'on_proposing_groups', 'reverse': '0'})
councilMeeting.xhtmlTransformFields = ()
councilMeeting.xhtmlTransformTypes = ()
councilMeeting.itemReferenceFormat = \
    "python: 'CC/' + (here.hasMeeting() and " \
    "here.restrictedTraverse('@@pm_unrestricted_methods').getLinkedMeetingDate().strftime('%Y%m%d') or '') " \
    "+ '-' + str(here.getItemNumber(relativeTo='meeting', for_display=True))"
councilMeeting.itemWFValidationLevels = (
    {'state': 'itemcreated',
     'state_title': 'itemcreated',
     'leading_transition': '-',
     'leading_transition_title': '-',
     'back_transition': 'backToItemCreated',
     'back_transition_title': 'backToItemCreated',
     'suffix': 'creators',
     'extra_suffixes': [],
     'enabled': '1',
     },
    {'state': 'proposed',
     'state_title': 'proposed',
     'leading_transition': 'propose',
     'leading_transition_title': 'propose',
     'back_transition': 'backToProposed',
     'back_transition_title': 'backToProposed',
     'suffix': 'reviewers',
     'extra_suffixes': [],
     'enabled': '1',
     },
    {'state': 'prevalidated',
     'state_title': 'prevalidated',
     'leading_transition': 'prevalidate',
     'leading_transition_title': 'prevalidate',
     'back_transition': 'backToPrevalidated',
     'back_transition_title': 'backToPrevalidated',
     'suffix': 'reviewers',
     'extra_suffixes': [],
     'enabled': '0',
     },
)
councilMeeting.transitionsToConfirm = (
    'Meeting.close', 'Meeting.backToDecided', 'MeetingItem.backToItemCreated', 'MeetingItem.refuse',
    'MeetingItem.backToProposed', 'MeetingItem.backTo_itemfrozen_from_returned_to_proposing_group',
    'MeetingItem.backTo_presented_from_returned_to_proposing_group', 'MeetingItem.delay',
    'MeetingItem.backToValidated', 'MeetingItem.return_to_proposing_group')
councilMeeting.itemColumns = [
    'static_item_reference',
    'Creator',
    'CreationDate',
    'getCategory',
    'ModificationDate',
    'review_state',
    'getProposingGroup',
    'advices',
    'meeting_date',
    'preferred_meeting_date',
    'actions']
councilMeeting.availableItemsListVisibleColumns = [
    'Creator', 'CreationDate', 'getCategory', 'getProposingGroup', 'advices', 'actions']
councilMeeting.itemsListVisibleColumns = [
    u'static_item_reference', u'Creator', u'CreationDate', u'review_state', u'getCategory',
    u'getProposingGroup', u'advices', u'actions']
councilMeeting.enabledAnnexesBatchActions = ['delete', 'download-annexes']
councilMeeting.dashboardItemsListingsFilters = (
    'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c13', 'c14', 'c15', 'c29', 'c32')
councilMeeting.dashboardMeetingAvailableItemsFilters = ('c4', 'c5', 'c11', 'c29', 'c32')
councilMeeting.dashboardMeetingLinkedItemsFilters = ('c4', 'c5', 'c6', 'c7', 'c11', 'c19', 'c29', 'c32')
councilMeeting.useAdvices = True
councilMeeting.selectableAdvisers = []
councilMeeting.itemAdviceStates = ('proposed', 'validated', 'presented')
councilMeeting.itemAdviceEditStates = ('proposed', 'validated', 'presented')
councilMeeting.itemAdviceViewStates = ('proposed',
                                       'validated',
                                       'presented',
                                       'itemfrozen',
                                       'returned_to_proposing_group',
                                       'pre_accepted',
                                       'accepted',
                                       'accepted_but_modified',
                                       'refused',
                                       'delayed')
councilMeeting.usedAdviceTypes = [
    'positive', 'positive_with_comments', 'positive_with_remarks', 'cautious',
    'negative', 'negative_with_remarks', 'back_to_proposing_group', 'nil', 'read']
collegeMeeting.transitionsReinitializingDelays = ['backToItemCreated']
councilMeeting.keepAccessToItemWhenAdviceIsGiven = True
councilMeeting.inheritedAdviceRemoveableByAdviser = True
# use template file from profile examples_fr
patch_pod_templates(councilMeeting.podTemplates, '../../examples_fr/templates/', collegeMeeting.id)
councilMeeting.customAdvisers = [
    {'row_id': 'unique_id_002',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '5',
     'delay_left_alert': '2',
     'delay_label': '≥ 30.000€ (urgent)',
     'available_on': "python: item.REQUEST.get('managing_available_delays', False)",
     'is_linked_to_previous_row': '0'},
    {'row_id': 'unique_id_003',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '10',
     'delay_left_alert': '4',
     'delay_label': '≥ 30.000€',
     'is_linked_to_previous_row': '1'},
    {'row_id': 'unique_id_004',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '20',
     'delay_left_alert': '4',
     'delay_label': '≥ 30.000€ (prolongé)',
     'available_on': "python: item.REQUEST.get('managing_available_delays', False)",
     'is_linked_to_previous_row': '1'},
]
councilMeeting.powerObservers = deepcopy(collegeMeeting.powerObservers)
councilMeeting.workflowAdaptations = list(collegeMeeting.workflowAdaptations)
councilMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.motivation',
      'tal_expression': "string:"},
     {'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Conseil décide de reporter le point.</p>"}
     ))
councilMeeting.onMeetingTransitionItemActionToExecute = deepcopy(
    collegeMeeting.onMeetingTransitionItemActionToExecute)
councilMeeting.selectableCopyGroups = []
councilMeeting.styleTemplates = []
councilMeeting.podTemplates = councilTemplates
councilMeeting.itemCopyGroupsStates = (
    'validated',
    'presented',
    'itemfrozen',
    'returned_to_proposing_group',
    'pre_accepted',
    'accepted',
    'accepted_but_modified',
    'delayed',
    'refused')
councilMeeting.itemManualSentToOtherMCStates = []
councilMeeting.itemAutoSentToOtherMCStates = []

councilMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance précédente',
        description='',
        category='administration',
        proposingGroup='dirgen',
        decision='Procès-verbal approuvé')]
councilMeeting.itemTemplates = []
councilMeeting.itemIconColor = "orange"
councilMeeting.initItemDecisionIfEmptyOnDecide = False
councilMeeting.meetingPresentItemWhenNoCurrentMeetingStates = ("created", "frozen")
councilMeeting.itemBudgetInfosStates = []

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=(collegeMeeting, councilMeeting, ),
    orgs=groups)
data.usersOutsideGroups = []
data.directory_position_types = list(examples_fr_import_data.data.directory_position_types)
data.contactsTemplates = list(examples_fr_import_data.data.contactsTemplates)
