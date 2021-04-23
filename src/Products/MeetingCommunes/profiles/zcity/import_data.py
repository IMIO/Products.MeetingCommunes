# -*- coding: utf-8 -*-

from copy import deepcopy
from DateTime import DateTime
from Products.MeetingCommunes.profiles.examples_fr import import_data as examples_fr_import_data
from Products.PloneMeeting.profiles import OrgDescriptor
from Products.PloneMeeting.profiles import patch_pod_templates
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import RecurringItemDescriptor


today = DateTime().strftime('%Y/%m/%d')

# Categories -------------------------------------------------------------------
categories = []

# Users and groups -------------------------------------------------------------
# no user
groups = [OrgDescriptor('dirgen', 'Directeur Général', u'DG'),
          OrgDescriptor('secretariat', 'Secrétariat Général', u'Secr', groups_in_charge=['dirgen']),
          OrgDescriptor('dirfin', 'Directeur Financier', u'DF'), ]

# Meeting configurations -------------------------------------------------------
# College
collegeMeeting = deepcopy(examples_fr_import_data.collegeMeeting)

collegeMeeting.shortName = 'College'
collegeMeeting.assembly = ''
collegeMeeting.assemblyStaves = ''
collegeMeeting.certifiedSignatures = []
collegeMeeting.places = ''
collegeMeeting.usedItemAttributes = ['description',
                                     'motivation',
                                     'inAndOutMoves',
                                     'notes',
                                     'observations',
                                     'manuallyLinkedItems',
                                     'otherMeetingConfigsClonableToPrivacy',
                                     'sendToAuthority']
collegeMeeting.usedMeetingAttributes = ['start_date',
                                        'end_date',
                                        'assembly',
                                        'signatures',
                                        'observations']
collegeMeeting.insertingMethodsOnAddItem = (
    {'insertingMethod': 'on_list_type', 'reverse': '0'},
    {'insertingMethod': 'on_proposing_groups', 'reverse': '0'})
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
collegeMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
collegeMeeting.keepAccessToItemWhenAdviceIsGiven = True
# use template file from profile examples_fr
patch_pod_templates(collegeMeeting.podTemplates, '../../examples_fr/templates/')
collegeMeeting.customAdvisers = [
    {'row_id': 'unique_id_002',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '5',
     'delay_left_alert': '2',
     'delay_label': 'Incidence financière >= 22.000€',
     'is_linked_to_previous_row': '0'},
    {'row_id': 'unique_id_003',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '10',
     'delay_left_alert': '4',
     'delay_label': 'Incidence financière >= 22.000€',
     'is_linked_to_previous_row': '1'},
    {'row_id': 'unique_id_004',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '20',
     'delay_left_alert': '4',
     'delay_label': 'Incidence financière >= 22.000€',
     'is_linked_to_previous_row': '1'},
]
collegeMeeting.powerObservers = (
    {'row_id': 'powerobservers',
     'label': 'Super observateurs',
     'item_states': ('validated',
                     'presented',
                     'itemfrozen',
                     'returned_to_proposing_group',
                     'pre_accepted'
                     'accepted',
                     'accepted_but_modified',
                     'delayed',
                     'refused'),
     'meeting_states': ('created', 'frozen', 'decided', 'closed'),
     'orderindex_': '1'},
    {'row_id': 'restrictedpowerobservers',
     'label': 'Super observateurs restreints',
     'item_states': ('itemfrozen',
                     'pre_accepted'
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
        category='recurrents',
        proposingGroup='dirgen',
        decision='Procès-verbal approuvé'), ]
collegeMeeting.itemTemplates = []
collegeMeeting.initItemDecisionIfEmptyOnDecide = False
collegeMeeting.meetingPresentItemWhenNoCurrentMeetingStates = ("created", "frozen")
collegeMeeting.itemBudgetInfosStates = []

# Council
councilMeeting = deepcopy(examples_fr_import_data.councilMeeting)

councilMeeting.shortName = 'Council'
councilMeeting.assembly = ''
councilMeeting.assemblyStaves = ''
councilMeeting.certifiedSignatures = []
councilMeeting.places = ''
councilMeeting.usedItemAttributes = ['description',
                                     'motivation',
                                     'inAndOutMoves',
                                     'notes',
                                     'observations',
                                     'manuallyLinkedItems',
                                     'privacy',
                                     'sendToAuthority']
councilMeeting.usedMeetingAttributes = ['start_date',
                                        'end_date',
                                        'assembly',
                                        'signatures',
                                        'observations']
councilMeeting.insertingMethodsOnAddItem = (
    {'insertingMethod': 'on_list_type', 'reverse': '0'},
    {'insertingMethod': 'on_proposing_groups', 'reverse': '0'})
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
councilMeeting.transitionsToConfirm = (
    'Meeting.close', 'Meeting.backToDecided', 'MeetingItem.backToItemCreated', 'MeetingItem.refuse',
    'MeetingItem.backToProposed', 'MeetingItem.backTo_itemfrozen_from_returned_to_proposing_group',
    'MeetingItem.backTo_presented_from_returned_to_proposing_group', 'MeetingItem.delay',
    'MeetingItem.backToValidated', 'MeetingItem.return_to_proposing_group')
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
councilMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
councilMeeting.keepAccessToItemWhenAdviceIsGiven = True
# use template file from profile examples_fr
patch_pod_templates(councilMeeting.podTemplates, '../../examples_fr/templates/', collegeMeeting.id)
councilMeeting.customAdvisers = [
    {'row_id': 'unique_id_002',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '5',
     'delay_left_alert': '2',
     'delay_label': 'Incidence financière >= 22.000€',
     'is_linked_to_previous_row': '0'},
    {'row_id': 'unique_id_003',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '10',
     'delay_left_alert': '4',
     'delay_label': 'Incidence financière >= 22.000€',
     'is_linked_to_previous_row': '1'},
    {'row_id': 'unique_id_004',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '20',
     'delay_left_alert': '4',
     'delay_label': 'Incidence financière >= 22.000€',
     'is_linked_to_previous_row': '1'},
]
councilMeeting.powerObservers = (
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
                     'returned_to_proposing_group',
                     'pre_accepted',
                     'accepted',
                     'accepted_but_modified',
                     'delayed',
                     'refused'),
     'meeting_states': ('frozen', 'decided', 'closed'),
     'orderindex_': '2'})
councilMeeting.workflowAdaptations = list(collegeMeeting.workflowAdaptations)
councilMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.motivation',
      'tal_expression': "string:"},
     {'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Collège décide de reporter le point.</p>"}
     ))
councilMeeting.onMeetingTransitionItemActionToExecute = deepcopy(
    collegeMeeting.onMeetingTransitionItemActionToExecute)
councilMeeting.selectableCopyGroups = []
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
        category='recurrents',
        proposingGroup='dirgen',
        decision='Procès-verbal approuvé'), ]
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
