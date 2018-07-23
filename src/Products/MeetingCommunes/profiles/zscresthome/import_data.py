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
agendaTemplate.pod_portal_types = ['MeetingSCRH']
agendaTemplate.tal_condition = 'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['MeetingSCRH']
decisionsTemplate.tal_condition = 'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemSCRH']

agTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

# Meeting configurations -------------------------------------------------------
# em
scrhMeeting = MeetingConfigDescriptor(
    'meeting-config-scrh', 'Comité spécial MR',
    'Comité spécial MR')
scrhMeeting.meetingManagers = []
scrhMeeting.assembly = 'Pierre Dupont - Président,\n' \
                     'Charles Exemple - Premier membre assemblée,\n' \
                     'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                     'Jacqueline Exemple, Observateur'
scrhMeeting.signatures = 'Le commandant de zone\nPierre Dupont\nLe secrétaire de zone\nCharles Exemple'
scrhMeeting.certifiedSignatures = [
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
scrhMeeting.places = ''
scrhMeeting.categories = categories
scrhMeeting.shortName = 'SCRH'
scrhMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
scrhMeeting.usedItemAttributes = [
    'description',
    'detailedDescription',
    'budgetInfos',
    'observations',
    'toDiscuss',
    'itemAssembly',
    'itemIsSigned', ]
scrhMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
scrhMeeting.recordMeetingHistoryStates = []
scrhMeeting.xhtmlTransformFields = ()
scrhMeeting.xhtmlTransformTypes = ()
scrhMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
scrhMeeting.meetingWorkflow = 'meetingcommunes_workflow'
scrhMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
scrhMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
scrhMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
scrhMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
scrhMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
scrhMeeting.meetingTopicStates = ('created', 'frozen')
scrhMeeting.decisionTopicStates = ('decided', 'closed')
scrhMeeting.enforceAdviceMandatoriness = False
scrhMeeting.insertingMethodsOnAddItem = (
    {'insertingMethod': 'on_proposing_groups', 'reverse': '0'}, )
scrhMeeting.recordItemHistoryStates = []
scrhMeeting.maxShownMeetings = 5
scrhMeeting.maxDaysDecisions = 60
scrhMeeting.meetingAppDefaultView = 'searchmyitems'
scrhMeeting.useAdvices = True
scrhMeeting.itemAdviceStates = ('validated',)
scrhMeeting.itemAdviceEditStates = ('validated',)
scrhMeeting.itemAdviceViewStates = (
    'validated',
    'presented',
    'itemfrozen',
    'accepted',
    'refused',
    'accepted_but_modified',
    'delayed',
    'pre_accepted',)
scrhMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
scrhMeeting.enableAdviceInvalidation = False
scrhMeeting.itemAdviceInvalidateStates = []
scrhMeeting.customAdvisers = []
scrhMeeting.itemPowerObserversStates = (
    'itemfrozen',
    'accepted',
    'delayed',
    'refused',
    'accepted_but_modified',
    'pre_accepted')
scrhMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed',
                                 'accepted_but_modified', 'pre_accepted']
scrhMeeting.workflowAdaptations = ['no_publication', 'no_global_observation',
                                   'return_to_proposing_group', 'refused']
scrhMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
scrhMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Comité décide de reporter le point.</p>"},))
scrhMeeting.onMeetingTransitionItemTransitionToTrigger = (
    {'meeting_transition': 'freeze', 'item_transition': 'itemfreeze'},

    {'meeting_transition': 'decide', 'item_transition': 'itemfreeze'},

    {'meeting_transition': 'publish_decisions', 'item_transition': 'itemfreeze'},
    {'meeting_transition': 'publish_decisions', 'item_transition': 'accept'},

    {'meeting_transition': 'close', 'item_transition': 'itemfreeze'},
    {'meeting_transition': 'close', 'item_transition': 'accept'},)
scrhMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
scrhMeeting.powerAdvisersGroups = ()
scrhMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
scrhMeeting.useCopies = True
scrhMeeting.selectableCopyGroups = []
scrhMeeting.podTemplates = agTemplates
scrhMeeting.meetingConfigsToCloneTo = []
scrhMeeting.recurringItems = []
scrhMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(scrhMeeting, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
