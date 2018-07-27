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
categories = [CategoryDescriptor('category1', 'Catégorie 1'),
              CategoryDescriptor('category2', 'Catégorie 2'),
              CategoryDescriptor('category3', 'Catégorie 3'),
              CategoryDescriptor('category4', 'Catégorie 4'),
              CategoryDescriptor('category5', 'Catégorie 5')]

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplate.odt_file = '../../examples_fr/templates/oj.odt'
agendaTemplate.pod_formats = ['odt', 'pdf', ]
agendaTemplate.pod_portal_types = ['Meetingexecutive']
agendaTemplate.tal_condition = u'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['Meetingexecutive']
decisionsTemplate.tal_condition = u'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemexecutive']

executiveTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

# Meeting configurations -------------------------------------------------------
# em
executiveMeeting = MeetingConfigDescriptor(
    'meeting-config-executive', 'Bureau exécutif',
    'Bureau exécutif')
executiveMeeting.meetingManagers = []
executiveMeeting.assembly = 'Pierre Dupont - Président,\n' \
                     'Charles Exemple - Premier membre assemblée,\n' \
                     'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                     'Jacqueline Exemple, Observateur'
executiveMeeting.signatures = 'Le Président\nPierre Dupont\nLe secrétaire\nCharles Exemple'
executiveMeeting.certifiedSignatures = [
    {'signatureNumber': '1',
     'name': u'Vraiment Présent',
     'function': u'Le Secrétaire',
     'date_from': '',
     'date_to': '',
     },
    {'signatureNumber': '2',
     'name': u'Charles Exemple',
     'function': u'Le Président',
     'date_from': '',
     'date_to': '',
     },
]
executiveMeeting.places = ''
executiveMeeting.categories = categories
executiveMeeting.shortName = 'executive'
executiveMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
executiveMeeting.usedItemAttributes = ['description',
                                       'detailedDescription',
                                       'budgetInfos',
                                       'observations',
                                       'toDiscuss',
                                       'itemAssembly',
                                       'itemIsSigned']
executiveMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
executiveMeeting.recordMeetingHistoryStates = []
executiveMeeting.xhtmlTransformFields = ()
executiveMeeting.xhtmlTransformTypes = ()
executiveMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
executiveMeeting.meetingWorkflow = 'meetingcommunes_workflow'
executiveMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
executiveMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
executiveMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
executiveMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
executiveMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
executiveMeeting.meetingTopicStates = ('created', 'frozen')
executiveMeeting.decisionTopicStates = ('decided', 'closed')
executiveMeeting.enforceAdviceMandatoriness = False
executiveMeeting.insertingMethodsOnAddItem = (
    {'insertingMethod': 'on_proposing_groups', 'reverse': '0'}, )
executiveMeeting.recordItemHistoryStates = []
executiveMeeting.maxShownMeetings = 5
executiveMeeting.maxDaysDecisions = 60
executiveMeeting.meetingAppDefaultView = 'searchmyitems'
executiveMeeting.useAdvices = True
executiveMeeting.itemAdviceStates = ('validated',)
executiveMeeting.itemAdviceEditStates = ('validated',)
executiveMeeting.itemAdviceViewStates = (
    'validated',
    'presented',
    'itemfrozen',
    'accepted',
    'refused',
    'accepted_but_modified',
    'delayed',
    'pre_accepted',)
executiveMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
executiveMeeting.enableAdviceInvalidation = False
executiveMeeting.itemAdviceInvalidateStates = []
executiveMeeting.customAdvisers = []
executiveMeeting.itemPowerObserversStates = (
    'itemfrozen',
    'accepted',
    'delayed',
    'refused',
    'accepted_but_modified',
    'pre_accepted')
executiveMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed',
                                      'accepted_but_modified', 'pre_accepted']
executiveMeeting.workflowAdaptations = ['no_publication', 'no_global_observation',
                                        'return_to_proposing_group', 'refused']
executiveMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
executiveMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Comité décide de reporter le point.</p>"},))
executiveMeeting.onMeetingTransitionItemTransitionToTrigger = (
    {'meeting_transition': 'freeze', 'item_transition': 'itemfreeze'},

    {'meeting_transition': 'decide', 'item_transition': 'itemfreeze'},

    {'meeting_transition': 'publish_decisions', 'item_transition': 'itemfreeze'},
    {'meeting_transition': 'publish_decisions', 'item_transition': 'accept'},

    {'meeting_transition': 'close', 'item_transition': 'itemfreeze'},
    {'meeting_transition': 'close', 'item_transition': 'accept'},)
executiveMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
executiveMeeting.powerAdvisersGroups = ()
executiveMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
executiveMeeting.useCopies = True
executiveMeeting.selectableCopyGroups = []
executiveMeeting.podTemplates = executiveTemplates
executiveMeeting.meetingConfigsToCloneTo = []
executiveMeeting.recurringItems = []
executiveMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(executiveMeeting, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
