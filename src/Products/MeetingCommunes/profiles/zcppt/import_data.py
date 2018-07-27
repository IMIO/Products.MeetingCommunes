# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import PodTemplateDescriptor
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

# Categories -------------------------------------------------------------------
categories = [CategoryDescriptor('category1', 'Catégorie 1'), ]

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplate.odt_file = '../../examples_fr/templates/oj.odt'
agendaTemplate.pod_formats = ['odt', 'pdf', ]
agendaTemplate.pod_portal_types = ['Meetingcppt']
agendaTemplate.tal_condition = u'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['Meetingcppt']
decisionsTemplate.tal_condition = u'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemcppt']

cpptTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

# Meeting configurations -------------------------------------------------------
# em
cpptMeeting = MeetingConfigDescriptor(
    'meeting-config-cppt', 'CPPT',
    'CPPT')
cpptMeeting.meetingManagers = []
cpptMeeting.assembly = 'Pierre Dupont - Président,\n' \
                     'Charles Exemple - Premier membre assemblée,\n' \
                     'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                     'Jacqueline Exemple, Observateur'
cpptMeeting.signatures = 'Le commandant de zone\nPierre Dupont\nLe secrétaire de zone\nCharles Exemple'
cpptMeeting.certifiedSignatures = [
    {'signatureNumber': '1',
     'name': u'Vraiment Présent',
     'function': u'Le Secrétaire de zone',
     'date_from': '',
     'date_to': '',
     },
    {'signatureNumber': '2',
     'name': u'Charles Exemple',
     'function': u'Le Commandant de zone',
     'date_from': '',
     'date_to': '',
     },
]
cpptMeeting.places = ''
cpptMeeting.categories = categories
cpptMeeting.shortName = 'cppt'
cpptMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
cpptMeeting.usedItemAttributes = ['description', 'motivation', 'observations', 'itemAssembly']
cpptMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'observations', ]
cpptMeeting.recordMeetingHistoryStates = []
cpptMeeting.xhtmlTransformFields = ()
cpptMeeting.xhtmlTransformTypes = ()
cpptMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
cpptMeeting.meetingWorkflow = 'meetingcommunes_workflow'
cpptMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
cpptMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
cpptMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
cpptMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
cpptMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
cpptMeeting.meetingTopicStates = ('created', 'frozen')
cpptMeeting.decisionTopicStates = ('decided', 'closed')
cpptMeeting.enforceAdviceMandatoriness = False
cpptMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                        'reverse': '0'}, )
cpptMeeting.recordItemHistoryStates = []
cpptMeeting.maxShownMeetings = 5
cpptMeeting.maxDaysDecisions = 60
cpptMeeting.meetingAppDefaultView = 'searchmyitems'
cpptMeeting.useAdvices = True
cpptMeeting.itemAdviceStates = ('validated',)
cpptMeeting.itemAdviceEditStates = ('validated',)
cpptMeeting.itemAdviceViewStates = ('validated',
                                  'presented',
                                  'itemfrozen',
                                  'accepted',
                                  'refused',
                                  'accepted_but_modified',
                                  'delayed',
                                  'pre_accepted',)
cpptMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
cpptMeeting.enableAdviceInvalidation = False
cpptMeeting.itemAdviceInvalidateStates = []
cpptMeeting.customAdvisers = []
cpptMeeting.itemPowerObserversStates = ('itemfrozen',
                                      'accepted',
                                      'delayed',
                                      'refused',
                                      'accepted_but_modified',
                                      'pre_accepted')
cpptMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
cpptMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group', 'refused']
cpptMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
cpptMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Comité décide de reporter le point.</p>"},))
cpptMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
cpptMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
cpptMeeting.powerAdvisersGroups = ()
cpptMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
cpptMeeting.useCopies = True
cpptMeeting.selectableCopyGroups = []
cpptMeeting.podTemplates = cpptTemplates
cpptMeeting.meetingConfigsToCloneTo = []
cpptMeeting.recurringItems = []
cpptMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(cpptMeeting, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
