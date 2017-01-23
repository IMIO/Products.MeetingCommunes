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
coGesTemplates = []

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
# mmCoGest
mmCoGestMeeting = MeetingConfigDescriptor(
    'meeting-config-mmcogest', 'MM - Comité de gestion',
    'MM - Comité de gestion')
mmCoGestMeeting.meetingManagers = ['dgen', ]
mmCoGestMeeting.assembly = 'A compléter'
mmCoGestMeeting.signatures = 'Le Directeur Général\nPierre Dupont\nLe Président\nCharles Exemple'
mmCoGestMeeting.certifiedSignatures = [
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
mmCoGestMeeting.places = ''
mmCoGestMeeting.categories = categories
mmCoGestMeeting.shortName = 'MMCOGES'
mmCoGestMeeting.meetingFileTypes = [annexe, annexeDecision, annexeAvis]
mmCoGestMeeting.usedItemAttributes = ['observations',
                                      'toDiscuss',
                                      'itemAssembly',
                                      'itemIsSigned', ]
mmCoGestMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
mmCoGestMeeting.recordMeetingHistoryStates = []
mmCoGestMeeting.itemsListVisibleColumns = ['toDiscuss',
                                           'state',
                                           'proposingGroup',
                                           'annexes',
                                           'annexesDecision',
                                           'advices',
                                           'actions',
                                           'itemIsSigned', ]
mmCoGestMeeting.itemColumns = ['creator',
                               'state',
                               'proposingGroup',
                               'annexes',
                               'annexesDecision',
                               'advices',
                               'actions',
                               'meeting',
                               'itemIsSigned', ]
mmCoGestMeeting.xhtmlTransformFields = ()
mmCoGestMeeting.xhtmlTransformTypes = ()
mmCoGestMeeting.itemWorkflow = 'meetingitemcollege_workflow'
mmCoGestMeeting.meetingWorkflow = 'meetingcollege_workflow'
mmCoGestMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
mmCoGestMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
mmCoGestMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
mmCoGestMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
mmCoGestMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
mmCoGestMeeting.meetingTopicStates = ('created', 'frozen')
mmCoGestMeeting.decisionTopicStates = ('decided', 'closed')
mmCoGestMeeting.enforceAdviceMandatoriness = False
mmCoGestMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                              'reverse': '0'}, )
mmCoGestMeeting.recordItemHistoryStates = []
mmCoGestMeeting.maxShownMeetings = 5
mmCoGestMeeting.maxDaysDecisions = 60
mmCoGestMeeting.meetingAppDefaultView = 'topic_searchmyitems'
mmCoGestMeeting.useAdvices = True
mmCoGestMeeting.itemAdviceStates = ('validated',)
mmCoGestMeeting.itemAdviceEditStates = ('validated',)
mmCoGestMeeting.itemAdviceViewStates = ('validated',
                                        'presented',
                                        'itemfrozen',
                                        'accepted',
                                        'refused',
                                        'accepted_but_modified',
                                        'delayed',
                                        'pre_accepted',)
mmCoGestMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
mmCoGestMeeting.enableAdviceInvalidation = False
mmCoGestMeeting.itemAdviceInvalidateStates = []
mmCoGestMeeting.customAdvisers = []
mmCoGestMeeting.itemPowerObserversStates = ('itemfrozen',
                                            'accepted',
                                            'delayed',
                                            'refused',
                                            'accepted_but_modified',
                                            'pre_accepted')
mmCoGestMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
mmCoGestMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
mmCoGestMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:Le Comité décide de reporter le point."},))
mmCoGestMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
mmCoGestMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
mmCoGestMeeting.powerAdvisersGroups = ('dirgen', 'dirfin', )
mmCoGestMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
mmCoGestMeeting.useCopies = True
mmCoGestMeeting.selectableCopyGroups = []
mmCoGestMeeting.podTemplates = coGesTemplates
mmCoGestMeeting.meetingConfigsToCloneTo = []
mmCoGestMeeting.recurringItems = []
mmCoGestMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(mmCoGestMeeting, ),
                                 groups=groups)
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
