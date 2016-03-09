# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.PloneMeeting.profiles import MeetingFileTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import UserDescriptor
from Products.PloneMeeting.profiles import GroupDescriptor
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

bourgmestreTemplates = [agendaTemplate, agendaTemplatePDF,
                        decisionsTemplate, decisionsTemplatePDF,
                        itemProjectTemplate, itemProjectTemplatePDF,
                        itemTemplate, itemTemplatePDF]

# Users and groups -------------------------------------------------------------
groups = [GroupDescriptor('groupe_bourgmestre', 'Groupe BOURGMESTRE', 'ordopol')]

# Meeting configurations -------------------------------------------------------
# bourgmestre
bourgmestreMeeting = MeetingConfigDescriptor(
    'meeting-config-bourgmestre', 'Bourgmestre',
    'Bourgmestre')
bourgmestreMeeting.meetingManagers = []
bourgmestreMeeting.assembly = 'Pierre Dupont - Président,\n' \
                              'Charles Exemple - Premier membre assemblée,\n' \
                              'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                              'Jacqueline Exemple, Observateur'
bourgmestreMeeting.certifiedSignatures = [
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
bourgmestreMeeting.places = """Place1\r
Place2\r
Place3\r"""
bourgmestreMeeting.categories = categories
bourgmestreMeeting.shortName = 'Bourgmestre'
bourgmestreMeeting.meetingFileTypes = [annexe, annexeDecision, annexeAvis]
bourgmestreMeeting.usedItemAttributes = ['detailedDescription',
                                         'budgetInfos',
                                         'observations',
                                         'toDiscuss',
                                         'itemAssembly',
                                         'itemIsSigned', ]
bourgmestreMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
bourgmestreMeeting.recordMeetingHistoryStates = []
bourgmestreMeeting.itemsListVisibleColumns = ['toDiscuss',
                                              'state',
                                              'proposingGroup',
                                              'annexes',
                                              'annexesDecision',
                                              'advices',
                                              'actions',
                                              'itemIsSigned', ]
bourgmestreMeeting.itemColumns = ['creator',
                                  'state',
                                  'proposingGroup',
                                  'annexes',
                                  'annexesDecision',
                                  'advices',
                                  'actions',
                                  'meeting',
                                  'itemIsSigned', ]
bourgmestreMeeting.xhtmlTransformFields = ()
bourgmestreMeeting.xhtmlTransformTypes = ()
bourgmestreMeeting.itemWorkflow = 'meetingitemcollege_workflow'
bourgmestreMeeting.meetingWorkflow = 'meetingcollege_workflow'
bourgmestreMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
bourgmestreMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
bourgmestreMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
bourgmestreMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
bourgmestreMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
bourgmestreMeeting.meetingTopicStates = ('created', 'frozen')
bourgmestreMeeting.decisionTopicStates = ('decided', 'closed')
bourgmestreMeeting.enforceAdviceMandatoriness = False
bourgmestreMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                                 'reverse': '0'}, )
bourgmestreMeeting.recordItemHistoryStates = []
bourgmestreMeeting.maxShownMeetings = 5
bourgmestreMeeting.maxDaysDecisions = 60
bourgmestreMeeting.meetingAppDefaultView = 'topic_searchmyitems'
bourgmestreMeeting.useAdvices = True
bourgmestreMeeting.itemAdviceStates = ('validated',)
bourgmestreMeeting.itemAdviceEditStates = ('validated',)
bourgmestreMeeting.itemAdviceViewStates = ('validated',
                                           'presented',
                                           'itemfrozen',
                                           'accepted',
                                           'refused',
                                           'accepted_but_modified',
                                           'delayed',
                                           'pre_accepted',)
bourgmestreMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
bourgmestreMeeting.enableAdviceInvalidation = False
bourgmestreMeeting.itemAdviceInvalidateStates = []
bourgmestreMeeting.customAdvisers = []
bourgmestreMeeting.itemPowerObserversStates = ('itemfrozen',
                                               'accepted',
                                               'delayed',
                                               'refused',
                                               'accepted_but_modified',
                                               'pre_accepted')
bourgmestreMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
bourgmestreMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
bourgmestreMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:Le Bourgmestre décide de reporter le point."},))
bourgmestreMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
bourgmestreMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
bourgmestreMeeting.powerAdvisersGroups = ('dirgen', 'dirfin', )
bourgmestreMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
bourgmestreMeeting.useCopies = True
bourgmestreMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers')]
bourgmestreMeeting.podTemplates = bourgmestreTemplates
bourgmestreMeeting.meetingConfigsToCloneTo = []
bourgmestreMeeting.recurringItems = []
bourgmestreMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(bourgmestreMeeting, ),
                                 groups=groups)
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
