# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.PloneMeeting.profiles import MeetingFileTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration

today = DateTime().strftime('%Y/%m/%d')

# File types -------------------------------------------------------------------
annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe à la décision', 'attach.png', '', 'item_decision')
annexeAvis = MeetingFileTypeDescriptor('annexeAvis', 'Annexe à un avis',
                                       'attach.png', '', 'advice')

# Categories -------------------------------------------------------------------
categories = [CategoryDescriptor('category1', 'Catégorie 1'),
              CategoryDescriptor('category2', 'Catégorie 2'),
              CategoryDescriptor('category3', 'Catégorie 3'),
              CategoryDescriptor('category4', 'Catégorie 4'),
              CategoryDescriptor('category5', 'Catégorie 5')]

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplate.podTemplate = '../../examples_fr/templates/oj.odt'
agendaTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager(here)'

agendaTemplatePDF = PodTemplateDescriptor('oj-pdf', 'Ordre du jour')
agendaTemplatePDF.podTemplate = '../../examples_fr/templates/oj.odt'
agendaTemplatePDF.podFormat = 'pdf'
agendaTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_plonemeeting.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.podTemplate = '../../examples_fr/templates/pv.odt'
decisionsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_plonemeeting.isManager(here)'

decisionsTemplatePDF = PodTemplateDescriptor('pv-pdf', 'Procès-verbal')
decisionsTemplatePDF.podTemplate = '../../examples_fr/templates/pv.odt'
decisionsTemplatePDF.podFormat = 'pdf'
decisionsTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                    'here.portal_plonemeeting.isManager(here)'

itemProjectTemplate = PodTemplateDescriptor('projet-deliberation', 'Projet délibération')
itemProjectTemplate.podTemplate = '../../examples_fr/templates/projet-deliberation.odt'
itemProjectTemplate.podCondition = 'python:here.meta_type=="MeetingItem" and not here.hasMeeting()'

itemProjectTemplatePDF = PodTemplateDescriptor('projet-deliberation-pdf', 'Projet délibération')
itemProjectTemplatePDF.podTemplate = '../../examples_fr/templates/projet-deliberation.odt'
itemProjectTemplatePDF.podFormat = 'pdf'
itemProjectTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem" and not here.hasMeeting()'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.podTemplate = '../../examples_fr/templates/deliberation.odt'
itemTemplate.podCondition = 'python:here.meta_type=="MeetingItem" and here.hasMeeting()'

itemTemplatePDF = PodTemplateDescriptor('deliberation-pdf', 'Délibération')
itemTemplatePDF.podTemplate = '../../examples_fr/templates/deliberation.odt'
itemTemplatePDF.podFormat = 'pdf'
itemTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem" and here.hasMeeting()'

agTemplates = [agendaTemplate, agendaTemplatePDF,
               decisionsTemplate, decisionsTemplatePDF,
               itemProjectTemplate, itemProjectTemplatePDF,
               itemTemplate, itemTemplatePDF]

# Meeting configurations -------------------------------------------------------
# ag
agMeeting = MeetingConfigDescriptor(
    'meeting-config-ag', 'Assemblée Générale',
    'Assemblée Générale')
agMeeting.meetingManagers = ['dgen', ]
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
agMeeting.meetingFileTypes = [annexe, annexeDecision, annexeAvis]
agMeeting.usedItemAttributes = ['detailedDescription',
                                'budgetInfos',
                                'observations',
                                'toDiscuss',
                                'itemAssembly',
                                'itemIsSigned', ]
agMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
agMeeting.recordMeetingHistoryStates = []
agMeeting.itemsListVisibleColumns = ['toDiscuss',
                                     'state',
                                     'proposingGroup',
                                     'annexes',
                                     'annexesDecision',
                                     'advices',
                                     'actions',
                                     'itemIsSigned', ]
agMeeting.itemColumns = ['creator',
                         'state',
                         'proposingGroup',
                         'annexes',
                         'annexesDecision',
                         'advices',
                         'actions',
                         'meeting',
                         'itemIsSigned', ]
agMeeting.xhtmlTransformFields = ()
agMeeting.xhtmlTransformTypes = ()
agMeeting.itemWorkflow = 'meetingitemcollege_workflow'
agMeeting.meetingWorkflow = 'meetingcollege_workflow'
agMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
agMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
agMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
agMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
agMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
agMeeting.meetingTopicStates = ('created', 'frozen')
agMeeting.decisionTopicStates = ('decided', 'closed')
agMeeting.enforceAdviceMandatoriness = False
agMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                        'reverse': '0'}, )
agMeeting.recordItemHistoryStates = []
agMeeting.maxShownMeetings = 5
agMeeting.maxDaysDecisions = 60
agMeeting.meetingAppDefaultView = 'topic_searchmyitems'
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
agMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
agMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:Le Comité décide de reporter le point."},))
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
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
