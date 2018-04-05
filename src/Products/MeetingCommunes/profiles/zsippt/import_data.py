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
agendaTemplate.pod_portal_types = ['Meetingsippt']
agendaTemplate.tal_condition = 'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = '../../examples_fr/templates/pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['Meetingsippt']
decisionsTemplate.tal_condition = 'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = '../../examples_fr/templates/deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItemsippt']

sipptTemplates = [agendaTemplate, decisionsTemplate, itemTemplate]

# Meeting configurations -------------------------------------------------------
# em
sipptMeeting = MeetingConfigDescriptor(
    'meeting-config-sippt', 'SIPPT',
    'SIPPT')
sipptMeeting.meetingManagers = []
sipptMeeting.assembly = 'Pierre Dupont - Président,\n' \
                     'Charles Exemple - Premier membre assemblée,\n' \
                     'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                     'Jacqueline Exemple, Observateur'
sipptMeeting.signatures = 'Le commandant de zone\nPierre Dupont\nLe secrétaire de zone\nCharles Exemple'
sipptMeeting.certifiedSignatures = [
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
sipptMeeting.places = ''
sipptMeeting.categories = categories
sipptMeeting.shortName = 'sippt'
sipptMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
sipptMeeting.usedItemAttributes = ['motivation', 'observations', 'itemAssembly']
sipptMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'observations', ]
sipptMeeting.recordMeetingHistoryStates = []
sipptMeeting.xhtmlTransformFields = ()
sipptMeeting.xhtmlTransformTypes = ()
sipptMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
sipptMeeting.meetingWorkflow = 'meetingcommunes_workflow'
sipptMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
sipptMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
sipptMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
sipptMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
sipptMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
sipptMeeting.meetingTopicStates = ('created', 'frozen')
sipptMeeting.decisionTopicStates = ('decided', 'closed')
sipptMeeting.enforceAdviceMandatoriness = False
sipptMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                        'reverse': '0'}, )
sipptMeeting.recordItemHistoryStates = []
sipptMeeting.maxShownMeetings = 5
sipptMeeting.maxDaysDecisions = 60
sipptMeeting.meetingAppDefaultView = 'searchmyitems'
sipptMeeting.useAdvices = True
sipptMeeting.itemAdviceStates = ('validated',)
sipptMeeting.itemAdviceEditStates = ('validated',)
sipptMeeting.itemAdviceViewStates = ('validated',
                                  'presented',
                                  'itemfrozen',
                                  'accepted',
                                  'refused',
                                  'accepted_but_modified',
                                  'delayed',
                                  'pre_accepted',)
sipptMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
sipptMeeting.enableAdviceInvalidation = False
sipptMeeting.itemAdviceInvalidateStates = []
sipptMeeting.customAdvisers = []
sipptMeeting.itemPowerObserversStates = ('itemfrozen',
                                      'accepted',
                                      'delayed',
                                      'refused',
                                      'accepted_but_modified',
                                      'pre_accepted')
sipptMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
sipptMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group']
sipptMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
sipptMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Comité décide de reporter le point.</p>"},))
sipptMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
sipptMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
sipptMeeting.powerAdvisersGroups = ()
sipptMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
sipptMeeting.useCopies = True
sipptMeeting.selectableCopyGroups = []
sipptMeeting.podTemplates = sipptTemplates
sipptMeeting.meetingConfigsToCloneTo = []
sipptMeeting.recurringItems = []
sipptMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(sipptMeeting, ),
                                 groups=[])
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
