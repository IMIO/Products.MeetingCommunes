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
# mmbexecutif
mmbexecutifMeeting = MeetingConfigDescriptor(
    'meeting-config-mmbexecutif', 'MM - Bureau exécutif',
    'MM - Bureau exécutif')
mmbexecutifMeeting.meetingManagers = ['dgen', ]
mmbexecutifMeeting.assembly = 'A compléter'
mmbexecutifMeeting.signatures = 'Le Directeur Général\nPierre Dupont\nLe Président\nCharles Exemple'
mmbexecutifMeeting.certifiedSignatures = [
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
mmbexecutifMeeting.places = ''
mmbexecutifMeeting.categories = categories
mmbexecutifMeeting.shortName = 'MMBE'
mmbexecutifMeeting.meetingFileTypes = [annexe, annexeDecision, annexeAvis]
mmbexecutifMeeting.usedItemAttributes = ['observations',
                                         'toDiscuss',
                                         'itemAssembly',
                                         'itemIsSigned', ]
mmbexecutifMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
mmbexecutifMeeting.recordMeetingHistoryStates = []
mmbexecutifMeeting.itemsListVisibleColumns = ['toDiscuss',
                                              'state',
                                              'proposingGroup',
                                              'annexes',
                                              'annexesDecision',
                                              'advices',
                                              'actions',
                                              'itemIsSigned', ]
mmbexecutifMeeting.itemColumns = ['creator',
                                  'state',
                                  'proposingGroup',
                                  'annexes',
                                  'annexesDecision',
                                  'advices',
                                  'actions',
                                  'meeting',
                                  'itemIsSigned', ]
mmbexecutifMeeting.xhtmlTransformFields = ()
mmbexecutifMeeting.xhtmlTransformTypes = ()
mmbexecutifMeeting.itemWorkflow = 'meetingitemcollege_workflow'
mmbexecutifMeeting.meetingWorkflow = 'meetingcollege_workflow'
mmbexecutifMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
mmbexecutifMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
mmbexecutifMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
mmbexecutifMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
mmbexecutifMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
mmbexecutifMeeting.meetingTopicStates = ('created', 'frozen')
mmbexecutifMeeting.decisionTopicStates = ('decided', 'closed')
mmbexecutifMeeting.enforceAdviceMandatoriness = False
mmbexecutifMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                                 'reverse': '0'}, )
mmbexecutifMeeting.recordItemHistoryStates = []
mmbexecutifMeeting.maxShownMeetings = 5
mmbexecutifMeeting.maxDaysDecisions = 60
mmbexecutifMeeting.meetingAppDefaultView = 'topic_searchmyitems'
mmbexecutifMeeting.useAdvices = True
mmbexecutifMeeting.itemAdviceStates = ('validated',)
mmbexecutifMeeting.itemAdviceEditStates = ('validated',)
mmbexecutifMeeting.itemAdviceViewStates = ('validated',
                                           'presented',
                                           'itemfrozen',
                                           'accepted',
                                           'refused',
                                           'accepted_but_modified',
                                           'delayed',
                                           'pre_accepted',)
mmbexecutifMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
mmbexecutifMeeting.enableAdviceInvalidation = False
mmbexecutifMeeting.itemAdviceInvalidateStates = []
mmbexecutifMeeting.customAdvisers = []
mmbexecutifMeeting.itemPowerObserversStates = ('itemfrozen',
                                               'accepted',
                                               'delayed',
                                               'refused',
                                               'accepted_but_modified',
                                               'pre_accepted')
mmbexecutifMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
mmbexecutifMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
mmbexecutifMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:Le Comité décide de reporter le point."},))
mmbexecutifMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
mmbexecutifMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
mmbexecutifMeeting.powerAdvisersGroups = ('dirgen', 'dirfin', )
mmbexecutifMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
mmbexecutifMeeting.useCopies = True
mmbexecutifMeeting.selectableCopyGroups = []
mmbexecutifMeeting.podTemplates = coGesTemplates
mmbexecutifMeeting.meetingConfigsToCloneTo = []
mmbexecutifMeeting.recurringItems = []
mmbexecutifMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(mmbexecutifMeeting, ),
                                 groups=groups)
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
