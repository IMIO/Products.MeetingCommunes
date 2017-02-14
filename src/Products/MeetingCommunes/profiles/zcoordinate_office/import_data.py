# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
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
agendaTemplate.pod_portal_types = ['MeetingCoordinateOffice']
agendaTemplate.tal_condition = 'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['MeetingCoordinateOffice']
decisionsTemplate.tal_condition = 'python:tool.isManager(here)'

itemProjectTemplate = PodTemplateDescriptor('projet-deliberation', 'Projet délibération')
itemProjectTemplate.odt_file = '../../examples_fr/templates/projet-deliberation.odt'
itemProjectTemplate.pod_formats = ['odt', 'pdf', ]
itemProjectTemplate.pod_portal_types = ['MeetingItemCoordinateOffice']
itemProjectTemplate.tal_condition = 'python:not here.hasMeeting()'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemCoordinateOffice']
itemTemplate.tal_condition = 'python:here.hasMeeting()'

coordinateTemplates = [agendaTemplate, decisionsTemplate,
                        itemProjectTemplate, itemTemplate]

# Meeting configurations -------------------------------------------------------
# coordinate
coordinateOffice = MeetingConfigDescriptor(
    'meeting-config-coordinate-office', 'Bureau de Coordination',
    'Bureau de Coordination')
coordinateOffice.meetingManagers = []
coordinateOffice.assembly = 'Pierre Dupont - Président,\n' \
                              'Charles Exemple - Premier membre assemblée,\n' \
                              'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                              'Jacqueline Exemple, Observateur'
coordinateOffice.certifiedSignatures = [
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
coordinateOffice.places = """Place1\r
Place2\r
Place3\r"""
coordinateOffice.categories = categories
coordinateOffice.shortName = 'CoordinateOffice'
coordinateOffice.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
coordinateOffice.usedItemAttributes = ['detailedDescription',
                                         'budgetInfos',
                                         'observations',
                                         'toDiscuss',
                                         'itemAssembly',
                                         'itemIsSigned', ]
coordinateOffice.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
coordinateOffice.recordMeetingHistoryStates = []
coordinateOffice.xhtmlTransformFields = ()
coordinateOffice.xhtmlTransformTypes = ()
coordinateOffice.itemWorkflow = 'meetingitemcommunes_workflow'
coordinateOffice.meetingWorkflow = 'meetingcommunes_workflow'
coordinateOffice.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
coordinateOffice.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
coordinateOffice.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
coordinateOffice.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
coordinateOffice.transitionsToConfirm = ['MeetingItem.delay', ]
coordinateOffice.meetingTopicStates = ('created', 'frozen')
coordinateOffice.decisionTopicStates = ('decided', 'closed')
coordinateOffice.enforceAdviceMandatoriness = False
coordinateOffice.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                                 'reverse': '0'}, )
coordinateOffice.recordItemHistoryStates = []
coordinateOffice.maxShownMeetings = 5
coordinateOffice.maxDaysDecisions = 60
coordinateOffice.meetingAppDefaultView = 'searchmyitems'
coordinateOffice.useAdvices = True
coordinateOffice.itemAdviceStates = ('validated',)
coordinateOffice.itemAdviceEditStates = ('validated',)
coordinateOffice.itemAdviceViewStates = ('validated',
                                           'presented',
                                           'itemfrozen',
                                           'accepted',
                                           'refused',
                                           'accepted_but_modified',
                                           'delayed',
                                           'pre_accepted',)
coordinateOffice.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
coordinateOffice.enableAdviceInvalidation = False
coordinateOffice.itemAdviceInvalidateStates = []
coordinateOffice.customAdvisers = []
coordinateOffice.itemPowerObserversStates = ('itemfrozen',
                                               'accepted',
                                               'delayed',
                                               'refused',
                                               'accepted_but_modified',
                                               'pre_accepted')
coordinateOffice.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
coordinateOffice.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group']
coordinateOffice.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
coordinateOffice.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le président décide de reporter le point.</p>"},))
coordinateOffice.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
coordinateOffice.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
coordinateOffice.powerAdvisersGroups = ('dirgen', 'dirfin', )
coordinateOffice.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
coordinateOffice.useCopies = True
coordinateOffice.selectableCopyGroups = []
coordinateOffice.podTemplates = coordinateTemplates
coordinateOffice.meetingConfigsToCloneTo = []
coordinateOffice.recurringItems = []
coordinateOffice.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(coordinateOffice, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
