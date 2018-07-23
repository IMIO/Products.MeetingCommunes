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
agendaTemplate.pod_portal_types = ['MeetingWB']
agendaTemplate.tal_condition = 'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['MeetingWB']
decisionsTemplate.tal_condition = 'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemWB']

agTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

# Meeting configurations -------------------------------------------------------
# em
wbMeeting = MeetingConfigDescriptor(
    'meeting-config-wb', 'Comité bien-être',
    'Comité bien-être')
wbMeeting.meetingManagers = []
wbMeeting.assembly = 'Pierre Dupont - Président,\n' \
                     'Charles Exemple - Premier membre assemblée,\n' \
                     'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                     'Jacqueline Exemple, Observateur'
wbMeeting.signatures = 'Le commandant de zone\nPierre Dupont\nLe secrétaire de zone\nCharles Exemple'
wbMeeting.certifiedSignatures = [
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
wbMeeting.places = ''
wbMeeting.categories = categories
wbMeeting.shortName = 'WB'
wbMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
wbMeeting.usedItemAttributes = ['description',
                                'detailedDescription',
                                'budgetInfos',
                                'observations',
                                'toDiscuss',
                                'itemAssembly',
                                'itemIsSigned', ]
wbMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
wbMeeting.recordMeetingHistoryStates = []
wbMeeting.xhtmlTransformFields = ()
wbMeeting.xhtmlTransformTypes = ()
wbMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
wbMeeting.meetingWorkflow = 'meetingcommunes_workflow'
wbMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
wbMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
wbMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
wbMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
wbMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
wbMeeting.meetingTopicStates = ('created', 'frozen')
wbMeeting.decisionTopicStates = ('decided', 'closed')
wbMeeting.enforceAdviceMandatoriness = False
wbMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                        'reverse': '0'}, )
wbMeeting.recordItemHistoryStates = []
wbMeeting.maxShownMeetings = 5
wbMeeting.maxDaysDecisions = 60
wbMeeting.meetingAppDefaultView = 'searchmyitems'
wbMeeting.useAdvices = True
wbMeeting.itemAdviceStates = ('validated',)
wbMeeting.itemAdviceEditStates = ('validated',)
wbMeeting.itemAdviceViewStates = ('validated',
                                  'presented',
                                  'itemfrozen',
                                  'accepted',
                                  'refused',
                                  'accepted_but_modified',
                                  'delayed',
                                  'pre_accepted',)
wbMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
wbMeeting.enableAdviceInvalidation = False
wbMeeting.itemAdviceInvalidateStates = []
wbMeeting.customAdvisers = []
wbMeeting.itemPowerObserversStates = ('itemfrozen',
                                      'accepted',
                                      'delayed',
                                      'refused',
                                      'accepted_but_modified',
                                      'pre_accepted')
wbMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
wbMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group', 'refused']
wbMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
wbMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Comité décide de reporter le point.</p>"},))
wbMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
wbMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
wbMeeting.powerAdvisersGroups = ()
wbMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
wbMeeting.useCopies = True
wbMeeting.selectableCopyGroups = []
wbMeeting.podTemplates = agTemplates
wbMeeting.meetingConfigsToCloneTo = []
wbMeeting.recurringItems = []
wbMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(wbMeeting, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
