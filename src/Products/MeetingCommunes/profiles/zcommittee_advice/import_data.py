# -*- coding: utf-8 -*-

from copy import deepcopy
from DateTime import DateTime
from Products.MeetingCommunes.profiles.examples_fr import import_data as examples_fr_import_data
from Products.PloneMeeting.profiles import patch_pod_templates
from Products.PloneMeeting.profiles import RecurringItemDescriptor


today = DateTime().strftime('%Y/%m/%d')

# Categories -------------------------------------------------------------------
categories = []

# Users and groups -------------------------------------------------------------
# no user
groups = []

# Meeting configurations -------------------------------------------------------
# Advice Committee

data = deepcopy(examples_fr_import_data.data)
adviceMeeting = deepcopy(examples_fr_import_data.collegeMeeting)

adviceMeeting.id = 'meeting-config-zadvice'
adviceMeeting.title = "Comité d'avis"
adviceMeeting.folderTitle = "Comité d'avis"
adviceMeeting.shortName = 'advice-committee'
adviceMeeting.isDefault = False
adviceMeeting.assembly = ''
adviceMeeting.assemblyStaves = ''
adviceMeeting.certifiedSignatures = []
adviceMeeting.places = ''
adviceMeeting.usedItemAttributes = ['description',
                                    'motivation',
                                    'inAndOutMoves',
                                    'notes',
                                    'observations',
                                    'manuallyLinkedItems',
                                    'otherMeetingConfigsClonableToPrivacy',
                                    'sendToAuthority']
adviceMeeting.usedMeetingAttributes = ['start_date',
                                       'end_date',
                                       'assembly',
                                       'signatures',
                                       'observations']
adviceMeeting.insertingMethodsOnAddItem = (
    {'insertingMethod': 'on_list_type', 'reverse': '0'},
    {'insertingMethod': 'on_proposing_groups', 'reverse': '0'})
adviceMeeting.itemColumns = ['static_item_reference',
                             'Creator',
                             'CreationDate',
                             'ModificationDate',
                             'review_state',
                             'getProposingGroup',
                             'advices',
                             'meeting_date',
                             'preferred_meeting_date',
                             'actions']
adviceMeeting.transitionsToConfirm = (
    'Meeting.close', 'Meeting.backToDecided', 'MeetingItem.backToItemCreated', 'MeetingItem.refuse',
    'MeetingItem.backToProposed', 'MeetingItem.backTo_itemfrozen_from_returned_to_proposing_group',
    'MeetingItem.backTo_presented_from_returned_to_proposing_group', 'MeetingItem.delay',
    'MeetingItem.backToValidated', 'MeetingItem.return_to_proposing_group')
adviceMeeting.selectableAdvisers = []
adviceMeeting.itemAdviceStates = ('proposed', 'validated', 'presented')
adviceMeeting.itemAdviceEditStates = ('proposed', 'validated', 'presented')
adviceMeeting.itemAdviceViewStates = ('proposed',
                                      'validated',
                                      'presented',
                                      'itemfrozen',
                                      'returned_to_proposing_group',
                                      'pre_accepted',
                                      'accepted',
                                      'accepted_but_modified',
                                      'refused',
                                      'delayed')
adviceMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
adviceMeeting.keepAccessToItemWhenAdviceIsGiven = True
adviceMeeting.meetingConfigsToCloneTo = []
# use template file from profile examples_fr
patch_pod_templates(adviceMeeting.podTemplates, '../../examples_fr/templates/')
adviceMeeting.customAdvisers = []
adviceMeeting.powerObservers = (
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
adviceMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.motivation',
      'tal_expression': "string:"},
     {'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Collège décide de reporter le point.</p>"}
     ))
adviceMeeting.onMeetingTransitionItemActionToExecute = (
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
adviceMeeting.selectableCopyGroups = []
adviceMeeting.itemCopyGroupsStates = (
    'validated',
    'presented',
    'itemfrozen',
    'returned_to_proposing_group',
    'pre_accepted',
    'accepted',
    'accepted_but_modified',
    'delayed',
    'refused')
adviceMeeting.itemManualSentToOtherMCStates = (
    'accepted',
    'accepted_but_modified',
    'pre_accepted',
    'itemfrozen',
    'presented',
    'validated')
adviceMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance précédente',
        description='',
        category='recurrents',
        proposingGroup='dirgen',
        decision='Procès-verbal approuvé'), ]
adviceMeeting.itemTemplates = []
adviceMeeting.initItemDecisionIfEmptyOnDecide = False
adviceMeeting.meetingPresentItemWhenNoCurrentMeetingStates = ("created", "frozen")
adviceMeeting.itemBudgetInfosStates = []

data.meetingConfigs = (adviceMeeting, )
data.usersOutsideGroups = []
