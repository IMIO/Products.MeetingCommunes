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
agendaTemplate.pod_portal_types = ['MeetingAG']
agendaTemplate.tal_condition = u'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['MeetingAG']
decisionsTemplate.tal_condition = u'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemAG']

agTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

# Meeting configurations -------------------------------------------------------
# ag
agMeeting = MeetingConfigDescriptor(
    'meeting-config-ag', 'Assemblée Générale',
    'Assemblée Générale')
agMeeting.meetingManagers = []
agMeeting.assembly = 'Pierre Dupont - Président,\n' \
                     'Charles Exemple - Premier membre assemblée,\n' \
                     'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                     'Jacqueline Exemple, Observateur'
agMeeting.signatures = 'Le Secrétaire communal\nPierre Dupont\nLe Bourgmestre\nCharles Exemple'
agMeeting.certifiedSignatures = [
    {'signatureNumber': '1',
     'name': u'Vraiment Présent',
     'function': u'Le Secrétaire communal',
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
agMeeting.places = """Place1\r
Place2\r
Place3\r"""
agMeeting.categories = categories
agMeeting.shortName = 'AG'
agMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
agMeeting.usedItemAttributes = ['description',
                                'detailedDescription',
                                'budgetInfos',
                                'observations',
                                'toDiscuss',
                                'itemAssembly',
                                'itemIsSigned', ]
agMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
agMeeting.recordMeetingHistoryStates = []
agMeeting.xhtmlTransformFields = ()
agMeeting.xhtmlTransformTypes = ()
agMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
agMeeting.meetingWorkflow = 'meetingcommunes_workflow'
agMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
agMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
agMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
agMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
agMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
agMeeting.meetingTopicStates = ('created', 'frozen')
agMeeting.decisionTopicStates = ('decided', 'closed')
agMeeting.enforceAdviceMandatoriness = False
agMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                        'reverse': '0'}, )
agMeeting.recordItemHistoryStates = []
agMeeting.maxShownMeetings = 5
agMeeting.maxDaysDecisions = 60
agMeeting.meetingAppDefaultView = 'searchmyitems'
agMeeting.useAdvices = True
agMeeting.itemAdviceStates = ('validated',)
agMeeting.itemAdviceEditStates = ('validated',)
agMeeting.itemAdviceViewStates = ('validated',
                                  'presented',
                                  'itemfrozen',
                                  'accepted',
                                  'refused',
                                  'accepted_but_modified',
                                  'delayed',
                                  'pre_accepted',)
agMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
agMeeting.enableAdviceInvalidation = False
agMeeting.itemAdviceInvalidateStates = []
agMeeting.customAdvisers = []
agMeeting.itemPowerObserversStates = ('itemfrozen',
                                      'accepted',
                                      'delayed',
                                      'refused',
                                      'accepted_but_modified',
                                      'pre_accepted')
agMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
agMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group', 'refused']
agMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
agMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Comité décide de reporter le point.</p>"},))
agMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
agMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
agMeeting.powerAdvisersGroups = ()
agMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
agMeeting.useCopies = True
agMeeting.selectableCopyGroups = []
agMeeting.podTemplates = agTemplates
agMeeting.meetingConfigsToCloneTo = []
agMeeting.recurringItems = []
agMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(agMeeting, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
