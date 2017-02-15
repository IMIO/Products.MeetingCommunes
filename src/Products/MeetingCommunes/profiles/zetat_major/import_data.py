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
agendaTemplate.pod_portal_types = ['MeetingEM']
agendaTemplate.tal_condition = 'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['MeetingEM']
decisionsTemplate.tal_condition = 'python:tool.isManager(here)'

itemProjectTemplate = PodTemplateDescriptor('projet-deliberation', 'Projet délibération')
itemProjectTemplate.odt_file = '../../examples_fr/templates/projet-deliberation.odt'
itemProjectTemplate.pod_formats = ['odt', 'pdf', ]
itemProjectTemplate.pod_portal_types = ['MeetingItemEM']
itemProjectTemplate.tal_condition = 'python:not here.hasMeeting()'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemEM']
itemTemplate.tal_condition = 'python:here.hasMeeting()'

agTemplates = [agendaTemplate, decisionsTemplate,
               itemProjectTemplate, itemTemplate]

# Meeting configurations -------------------------------------------------------
# em
emMeeting = MeetingConfigDescriptor(
    'meeting-config-em', 'Etat Major',
    'Etat Major')
emMeeting.meetingManagers = []
emMeeting.assembly = 'Pierre Dupont - Président,\n' \
                     'Charles Exemple - Premier membre assemblée,\n' \
                     'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                     'Jacqueline Exemple, Observateur'
emMeeting.signatures = 'Le commandant de zone\nPierre Dupont\nLe secrétaire de zone\nCharles Exemple'
emMeeting.certifiedSignatures = [
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
emMeeting.places = """Place1\r
Place2\r
Place3\r"""
emMeeting.categories = categories
emMeeting.shortName = 'EM'
emMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
emMeeting.usedItemAttributes = ['detailedDescription',
                                'budgetInfos',
                                'observations',
                                'toDiscuss',
                                'itemAssembly',
                                'itemIsSigned', ]
emMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
emMeeting.recordMeetingHistoryStates = []
emMeeting.xhtmlTransformFields = ()
emMeeting.xhtmlTransformTypes = ()
emMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
emMeeting.meetingWorkflow = 'meetingcommunes_workflow'
emMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
emMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
emMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
emMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
emMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
emMeeting.meetingTopicStates = ('created', 'frozen')
emMeeting.decisionTopicStates = ('decided', 'closed')
emMeeting.enforceAdviceMandatoriness = False
emMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                        'reverse': '0'}, )
emMeeting.recordItemHistoryStates = []
emMeeting.maxShownMeetings = 5
emMeeting.maxDaysDecisions = 60
emMeeting.meetingAppDefaultView = 'searchmyitems'
emMeeting.useAdvices = True
emMeeting.itemAdviceStates = ('validated',)
emMeeting.itemAdviceEditStates = ('validated',)
emMeeting.itemAdviceViewStates = ('validated',
                                  'presented',
                                  'itemfrozen',
                                  'accepted',
                                  'refused',
                                  'accepted_but_modified',
                                  'delayed',
                                  'pre_accepted',)
emMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
emMeeting.enableAdviceInvalidation = False
emMeeting.itemAdviceInvalidateStates = []
emMeeting.customAdvisers = []
emMeeting.itemPowerObserversStates = ('itemfrozen',
                                      'accepted',
                                      'delayed',
                                      'refused',
                                      'accepted_but_modified',
                                      'pre_accepted')
emMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
emMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group']
emMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
emMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Comité décide de reporter le point.</p>"},))
emMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
emMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
emMeeting.powerAdvisersGroups = ()
emMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
emMeeting.useCopies = True
emMeeting.selectableCopyGroups = []
emMeeting.podTemplates = agTemplates
emMeeting.meetingConfigsToCloneTo = []
emMeeting.recurringItems = []
emMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(emMeeting, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
