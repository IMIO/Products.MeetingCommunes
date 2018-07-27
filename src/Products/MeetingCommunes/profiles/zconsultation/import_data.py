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
agendaTemplate.pod_portal_types = ['Meetingconcertation']
agendaTemplate.tal_condition = u'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['Meetingconcertation']
decisionsTemplate.tal_condition = u'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemconcertation']

concertationTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

# Meeting configurations -------------------------------------------------------
# em
concertationMeeting = MeetingConfigDescriptor(
    'meeting-config-concertation', 'Concertation',
    'Concertation')
concertationMeeting.meetingManagers = []
concertationMeeting.assembly = 'Pierre Dupont - Président,\n' \
                     'Charles Exemple - Premier membre assemblée,\n' \
                     'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                     'Jacqueline Exemple, Observateur'
concertationMeeting.signatures = 'Le commandant de zone\nPierre Dupont\nLe secrétaire de zone\nCharles Exemple'
concertationMeeting.certifiedSignatures = [
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
concertationMeeting.places = ''
concertationMeeting.categories = categories
concertationMeeting.shortName = 'concertation'
concertationMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
concertationMeeting.usedItemAttributes = ['description', 'motivation', 'observations', 'itemAssembly']
concertationMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'observations', ]
concertationMeeting.recordMeetingHistoryStates = []
concertationMeeting.xhtmlTransformFields = ()
concertationMeeting.xhtmlTransformTypes = ()
concertationMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
concertationMeeting.meetingWorkflow = 'meetingcommunes_workflow'
concertationMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
concertationMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
concertationMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
concertationMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
concertationMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
concertationMeeting.meetingTopicStates = ('created', 'frozen')
concertationMeeting.decisionTopicStates = ('decided', 'closed')
concertationMeeting.enforceAdviceMandatoriness = False
concertationMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                        'reverse': '0'}, )
concertationMeeting.recordItemHistoryStates = []
concertationMeeting.maxShownMeetings = 5
concertationMeeting.maxDaysDecisions = 60
concertationMeeting.meetingAppDefaultView = 'searchmyitems'
concertationMeeting.useAdvices = True
concertationMeeting.itemAdviceStates = ('validated',)
concertationMeeting.itemAdviceEditStates = ('validated',)
concertationMeeting.itemAdviceViewStates = ('validated',
                                  'presented',
                                  'itemfrozen',
                                  'accepted',
                                  'refused',
                                  'accepted_but_modified',
                                  'delayed',
                                  'pre_accepted',)
concertationMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
concertationMeeting.enableAdviceInvalidation = False
concertationMeeting.itemAdviceInvalidateStates = []
concertationMeeting.customAdvisers = []
concertationMeeting.itemPowerObserversStates = ('itemfrozen',
                                      'accepted',
                                      'delayed',
                                      'refused',
                                      'accepted_but_modified',
                                      'pre_accepted')
concertationMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
concertationMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group', 'refused']
concertationMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
concertationMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Comité décide de reporter le point.</p>"},))
concertationMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
concertationMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
concertationMeeting.powerAdvisersGroups = ()
concertationMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
concertationMeeting.useCopies = True
concertationMeeting.selectableCopyGroups = []
concertationMeeting.podTemplates = concertationTemplates
concertationMeeting.meetingConfigsToCloneTo = []
concertationMeeting.recurringItems = []
concertationMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(concertationMeeting, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
