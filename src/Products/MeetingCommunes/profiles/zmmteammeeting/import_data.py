# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.PloneMeeting.profiles import MeetingFileTypeDescriptor
from Products.PloneMeeting.profiles import UserDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration

today = DateTime().strftime('%Y/%m/%d')

# File types -------------------------------------------------------------------
annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe à la décision', 'attach.png', '', 'item_decision')
annexeAvis = MeetingFileTypeDescriptor('annexeAvis', 'Annexe à un avis',
                                       'attach.png', '', 'advice')

# No Categories -------------------------------------------------------------------
categories = []

# No Pod templates ----------------------------------------------------------------
teamTemplates = []

# Users and groups -------------------------------------------------------------
dgen = UserDescriptor('dgen', [], email="test@test.be", fullname="Henry Directeur")
dfin = UserDescriptor('dfin', [], email="test@test.be", fullname="Directeur Financier")
agentInfo = UserDescriptor('agentInfo', [], email="test@test.be", fullname="Agent Service Informatique")
agentCompta = UserDescriptor('agentCompta', [], email="test@test.be", fullname="Agent Service Comptabilité")
agentPers = UserDescriptor('agentPers', [], email="test@test.be", fullname="Agent Service du Personnel")
chefPers = UserDescriptor('chefPers', [], email="test@test.be", fullname="Chef Personnel")
chefCompta = UserDescriptor('chefCompta', [], email="test@test.be", fullname="Chef Comptabilité")

groups = []

# Meeting configurations -------------------------------------------------------
# mmteam
mmteamMeeting = MeetingConfigDescriptor(
    'meeting-config-mmteam', 'MM - Bureau exécutif',
    'MM - Bureau exécutif')
mmteamMeeting.meetingManagers = ['dgen', ]
mmteamMeeting.assembly = 'A compléter'
mmteamMeeting.signatures = 'Le Directeur Général\nPierre Dupont\nLe Président\nCharles Exemple'
mmteamMeeting.certifiedSignatures = [
    {'signatureNumber': '1',
     'name': u'Vraiment Présent',
     'function': u'Le Directeur Général',
     'date_from': '',
     'date_to': '',
     },
    {'signatureNumber': '2',
     'name': u'Charles Exemple',
     'function': u'Le Bourgmestre',
     'date_from': '',
     'date_to': '',
     },
]
mmteamMeeting.places = ''
mmteamMeeting.categories = categories
mmteamMeeting.shortName = 'MMBE'
mmteamMeeting.meetingFileTypes = [annexe, annexeDecision, annexeAvis]
mmteamMeeting.usedItemAttributes = ['observations',
                                    'toDiscuss',
                                    'itemAssembly',
                                    'itemIsSigned', ]
mmteamMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
mmteamMeeting.recordMeetingHistoryStates = []
mmteamMeeting.itemsListVisibleColumns = ['toDiscuss',
                                         'state',
                                         'proposingGroup',
                                         'annexes',
                                         'annexesDecision',
                                         'advices',
                                         'actions',
                                         'itemIsSigned', ]
mmteamMeeting.itemColumns = ['creator',
                             'state',
                             'proposingGroup',
                             'annexes',
                             'annexesDecision',
                             'advices',
                             'actions',
                             'meeting',
                             'itemIsSigned', ]
mmteamMeeting.xhtmlTransformFields = ()
mmteamMeeting.xhtmlTransformTypes = ()
mmteamMeeting.itemWorkflow = 'meetingitemcollege_workflow'
mmteamMeeting.meetingWorkflow = 'meetingcollege_workflow'
mmteamMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
mmteamMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
mmteamMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
mmteamMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
mmteamMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
mmteamMeeting.meetingTopicStates = ('created', 'frozen')
mmteamMeeting.decisionTopicStates = ('decided', 'closed')
mmteamMeeting.enforceAdviceMandatoriness = False
mmteamMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                            'reverse': '0'}, )
mmteamMeeting.recordItemHistoryStates = []
mmteamMeeting.maxShownMeetings = 5
mmteamMeeting.maxDaysDecisions = 60
mmteamMeeting.meetingAppDefaultView = 'topic_searchmyitems'
mmteamMeeting.useAdvices = True
mmteamMeeting.itemAdviceStates = ('validated',)
mmteamMeeting.itemAdviceEditStates = ('validated',)
mmteamMeeting.itemAdviceViewStates = ('validated',
                                      'presented',
                                      'itemfrozen',
                                      'accepted',
                                      'refused',
                                      'accepted_but_modified',
                                      'delayed',
                                      'pre_accepted',)
mmteamMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
mmteamMeeting.enableAdviceInvalidation = False
mmteamMeeting.itemAdviceInvalidateStates = []
mmteamMeeting.customAdvisers = []
mmteamMeeting.itemPowerObserversStates = ('itemfrozen',
                                          'accepted',
                                          'delayed',
                                          'refused',
                                          'accepted_but_modified',
                                          'pre_accepted')
mmteamMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
mmteamMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
mmteamMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:Le Comité décide de reporter le point."},))
mmteamMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
mmteamMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
mmteamMeeting.powerAdvisersGroups = ('dirgen', 'dirfin', )
mmteamMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
mmteamMeeting.useCopies = True
mmteamMeeting.selectableCopyGroups = []
mmteamMeeting.podTemplates = teamTemplates
mmteamMeeting.meetingConfigsToCloneTo = []
mmteamMeeting.recurringItems = []
mmteamMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(mmteamMeeting, ),
                                 groups=groups)
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
