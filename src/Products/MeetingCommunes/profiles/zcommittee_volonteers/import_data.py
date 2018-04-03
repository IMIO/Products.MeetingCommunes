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
agendaTemplate.pod_portal_types = ['Meetingvolonteers']
agendaTemplate.tal_condition = 'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['Meetingvolonteers']
decisionsTemplate.tal_condition = 'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemvolonteers']

volonteersTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

# Meeting configurations -------------------------------------------------------
# em
volonteersMeeting = MeetingConfigDescriptor(
    'meeting-config-volonteers', 'Comission des volontaires',
    'Comission des volontaires')
volonteersMeeting.meetingManagers = []
volonteersMeeting.assembly = 'Pierre Dupont - Président,\n' \
                     'Charles Exemple - Premier membre assemblée,\n' \
                     'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                     'Jacqueline Exemple, Observateur'
volonteersMeeting.signatures = 'Le commandant de zone\nPierre Dupont\nLe secrétaire de zone\nCharles Exemple'
volonteersMeeting.certifiedSignatures = [
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
volonteersMeeting.places = ''
volonteersMeeting.categories = categories
volonteersMeeting.shortName = 'volonteers'
volonteersMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
volonteersMeeting.usedItemAttributes = ['motivation', 'observations', 'itemAssembly']
volonteersMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'observations', ]
volonteersMeeting.recordMeetingHistoryStates = []
volonteersMeeting.xhtmlTransformFields = ()
volonteersMeeting.xhtmlTransformTypes = ()
volonteersMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
volonteersMeeting.meetingWorkflow = 'meetingcommunes_workflow'
volonteersMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
volonteersMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
volonteersMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
volonteersMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
volonteersMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
volonteersMeeting.meetingTopicStates = ('created', 'frozen')
volonteersMeeting.decisionTopicStates = ('decided', 'closed')
volonteersMeeting.enforceAdviceMandatoriness = False
volonteersMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                        'reverse': '0'}, )
volonteersMeeting.recordItemHistoryStates = []
volonteersMeeting.maxShownMeetings = 5
volonteersMeeting.maxDaysDecisions = 60
volonteersMeeting.meetingAppDefaultView = 'searchmyitems'
volonteersMeeting.useAdvices = True
volonteersMeeting.itemAdviceStates = ('validated',)
volonteersMeeting.itemAdviceEditStates = ('validated',)
volonteersMeeting.itemAdviceViewStates = ('validated',
                                  'presented',
                                  'itemfrozen',
                                  'accepted',
                                  'refused',
                                  'accepted_but_modified',
                                  'delayed',
                                  'pre_accepted',)
volonteersMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
volonteersMeeting.enableAdviceInvalidation = False
volonteersMeeting.itemAdviceInvalidateStates = []
volonteersMeeting.customAdvisers = []
volonteersMeeting.itemPowerObserversStates = ('itemfrozen',
                                      'accepted',
                                      'delayed',
                                      'refused',
                                      'accepted_but_modified',
                                      'pre_accepted')
volonteersMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
volonteersMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group', 'refused']
volonteersMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
volonteersMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Comité décide de reporter le point.</p>"},))
volonteersMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
volonteersMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
volonteersMeeting.powerAdvisersGroups = ()
volonteersMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
volonteersMeeting.useCopies = True
volonteersMeeting.selectableCopyGroups = []
volonteersMeeting.podTemplates = volonteersTemplates
volonteersMeeting.meetingConfigsToCloneTo = []
volonteersMeeting.recurringItems = []
volonteersMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(volonteersMeeting, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
