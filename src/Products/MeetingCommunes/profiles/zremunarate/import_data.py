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
agendaTemplate.pod_portal_types = ['MeetingREMUN']
agendaTemplate.tal_condition = 'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['MeetingREMUN']
decisionsTemplate.tal_condition = 'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemREMUN']

agTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

# Meeting configurations -------------------------------------------------------
# em
remunMeeting = MeetingConfigDescriptor(
    'meeting-config-remun', 'Comité de rémunération',
    'Comité de rémunération')
remunMeeting.meetingManagers = []
remunMeeting.assembly = 'Pierre Dupont - Président,\n' \
                     'Charles Exemple - Premier membre assemblée,\n' \
                     'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                     'Jacqueline Exemple, Observateur'
remunMeeting.signatures = 'Le commandant de zone\nPierre Dupont\nLe secrétaire de zone\nCharles Exemple'
remunMeeting.certifiedSignatures = [
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
remunMeeting.places = ''
remunMeeting.categories = categories
remunMeeting.shortName = 'REMUN'
remunMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
remunMeeting.usedItemAttributes = ['detailedDescription',
                                'budgetInfos',
                                'observations',
                                'toDiscuss',
                                'itemAssembly',
                                'itemIsSigned', ]
remunMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
remunMeeting.recordMeetingHistoryStates = []
remunMeeting.xhtmlTransformFields = ()
remunMeeting.xhtmlTransformTypes = ()
remunMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
remunMeeting.meetingWorkflow = 'meetingcommunes_workflow'
remunMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
remunMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
remunMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
remunMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
remunMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
remunMeeting.meetingTopicStates = ('created', 'frozen')
remunMeeting.decisionTopicStates = ('decided', 'closed')
remunMeeting.enforceAdviceMandatoriness = False
remunMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                        'reverse': '0'}, )
remunMeeting.recordItemHistoryStates = []
remunMeeting.maxShownMeetings = 5
remunMeeting.maxDaysDecisions = 60
remunMeeting.meetingAppDefaultView = 'searchmyitems'
remunMeeting.useAdvices = True
remunMeeting.itemAdviceStates = ('validated',)
remunMeeting.itemAdviceEditStates = ('validated',)
remunMeeting.itemAdviceViewStates = ('validated',
                                  'presented',
                                  'itemfrozen',
                                  'accepted',
                                  'refused',
                                  'accepted_but_modified',
                                  'delayed',
                                  'pre_accepted',)
remunMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
remunMeeting.enableAdviceInvalidation = False
remunMeeting.itemAdviceInvalidateStates = []
remunMeeting.customAdvisers = []
remunMeeting.itemPowerObserversStates = ('itemfrozen',
                                      'accepted',
                                      'delayed',
                                      'refused',
                                      'accepted_but_modified',
                                      'pre_accepted')
remunMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
remunMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group', 'refused']
remunMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
remunMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Comité décide de reporter le point.</p>"},))
remunMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
remunMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
remunMeeting.powerAdvisersGroups = ()
remunMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
remunMeeting.useCopies = True
remunMeeting.selectableCopyGroups = []
remunMeeting.podTemplates = agTemplates
remunMeeting.meetingConfigsToCloneTo = []
remunMeeting.recurringItems = []
remunMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(remunMeeting, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
