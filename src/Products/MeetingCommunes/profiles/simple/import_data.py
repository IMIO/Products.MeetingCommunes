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
    'detailedDescription',
    'budgetInfos',
    'observations',
    'toDiscuss',
    'itemAssembly',
    'itemIsSigned', ]
simpleMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
simpleMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
simpleMeeting.meetingWorkflow = 'meetingcommunes_workflow'
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
simpleMeeting.itemPowerObserversStates = ('itemfrozen',
                                          'accepted',
                                          'accepted_but_modified',
                                          'delayed',
                                          'refused',
                                          'returned_to_proposing_group',
                                          'pre_accepted')
simpleMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
simpleMeeting.itemRestrictedPowerObserversStates = ('itemfrozen',
                                                    'accepted',
                                                    'accepted_but_modified',
                                                    'delayed',
                                                    'refused',
                                                    'returned_to_proposing_group',
                                                    'pre_accepted')
simpleMeeting.meetingRestrictedPowerObserversStates = ('frozen', 'decided', 'closed')
simpleMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
simpleMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group', 'refused']
simpleMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
simpleMeeting.onMeetingTransitionItemTransitionToTrigger = (
    {'meeting_transition': 'freeze',
     'item_transition': 'itemfreeze'},
    {'meeting_transition': 'decide',
     'item_transition': 'itemfreeze'},
    {'meeting_transition': 'publish_decisions',
     'item_transition': 'itemfreeze'},
    {'meeting_transition': 'publish_decisions',
     'item_transition': 'accept'},
    {'meeting_transition': 'close',
     'item_transition': 'itemfreeze'},
    {'meeting_transition': 'close',
     'item_transition': 'accept'},)

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(simpleMeeting, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
