# -*- coding: utf-8 -*-
#
# The most simple configuration possible, this is made to be overrided
# when we want to base a configuration on a very simple existing one
# No : categories, users/groups, templates, ...
#

from DateTime import DateTime
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration


today = DateTime().strftime('%Y/%m/%d')

# File types -------------------------------------------------------------------
annexe = ItemAnnexTypeDescriptor('annexe', 'Annexe', u'attach.png')
annexeDecision = ItemAnnexTypeDescriptor('annexeDecision', 'Annexe à la décision',
                                         u'attach.png', relatedTo='item_decision')
annexeAvis = AnnexTypeDescriptor('annexeAvis', 'Annexe à un avis',
                                 u'attach.png', relatedTo='advice')
annexeSeance = AnnexTypeDescriptor('annexe', 'Annexe',
                                   u'attach.png', relatedTo='meeting')

# Meeting configurations -------------------------------------------------------
simpleMeeting = MeetingConfigDescriptor(
    'simple', 'Simple', 'Simple')
simpleMeeting.assembly = 'Pierre Dupont - Président,\n' \
                         'Charles Exemple - Premier membre assemblée,\n' \
                         'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                         'Jacqueline Exemple, Observateur'
simpleMeeting.signatures = 'Le Signataire 1\nPierre Dupont\nLe Signataire 2\nCharles Exemple'
simpleMeeting.certifiedSignatures = [
    {'signatureNumber': '1',
     'name': u'Vraiment Présent',
     'function': u'Le Signataire 1 FF',
     'date_from': '',
     'date_to': '',
     },
    {'signatureNumber': '2',
     'name': u'Vraiment Exemple',
     'function': u'Le Signataire 2 FF',
     'date_from': '',
     'date_to': '',
     },
]
simpleMeeting.places = """Place1\r
Place2\r
Place3\r"""
simpleMeeting.shortName = 'Simple'
simpleMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
simpleMeeting.usedItemAttributes = [
    'motivation',
    'budgetInfos',
    'observations',
    'sendToAuthority',
    'toDiscuss',
    'itemIsSigned',
    'notes', ]
simpleMeeting.usedMeetingAttributes = ['start_date', 'end_date', 'signatures', 'assembly', 'place', 'observations', ]
simpleMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
simpleMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
simpleMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
simpleMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
simpleMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
simpleMeeting.meetingTopicStates = ('created', 'frozen')
simpleMeeting.decisionTopicStates = ('decided', 'closed')
simpleMeeting.insertingMethodsOnAddItem = (
    {'insertingMethod': 'on_proposing_groups', 'reverse': '0'}, )
simpleMeeting.useAdvices = True
simpleMeeting.itemAdviceStates = ('validated',)
simpleMeeting.itemAdviceEditStates = ('validated',)
simpleMeeting.itemAdviceViewStates = ('validated',
                                      'presented',
                                      'itemfrozen',
                                      'accepted',
                                      'refused',
                                      'accepted_but_modified',
                                      'delayed',
                                      'pre_accepted',)
simpleMeeting.powerObservers = (
    {'row_id': 'powerobservers',
     'label': 'Super observateurs',
     'item_states': ('itemfrozen',
                     'accepted',
                     'delayed',
                     'refused',
                     'accepted_but_modified',
                     'pre_accepted'),
     'meeting_states': ('frozen', 'decided', 'closed'),
     'orderindex_': '1'},
    {'row_id': 'restrictedpowerobservers',
     'label': 'Super observateurs restreints',
     'item_states': [],
     'meeting_states': [],
     'orderindex_': '2'})
simpleMeeting.workflowAdaptations = [
    'no_publication', 'refused', 'accepted_but_modified', 'delayed',
    'return_to_proposing_group', 'only_creator_may_delete', 'pre_accepted']
simpleMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
simpleMeeting.onMeetingTransitionItemActionToExecute = (
    {'meeting_transition': 'freeze',
     'item_action': 'itemfreeze',
     'tal_expression': ''},

    {'meeting_transition': 'decide',
     'item_action': 'itemfreeze',
     'tal_expression': ''},

    {'meeting_transition': 'publish_decisions',
     'item_action': 'itemfreeze',
     'tal_expression': ''},
    {'meeting_transition': 'publish_decisions',
     'item_action': 'accept',
     'tal_expression': ''},

    {'meeting_transition': 'close',
     'item_action': 'itemfreeze',
     'tal_expression': ''},
    {'meeting_transition': 'close',
     'item_action': 'accept',
     'tal_expression': ''},)

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(simpleMeeting, ),
                                 orgs=[])
# ------------------------------------------------------------------------------
