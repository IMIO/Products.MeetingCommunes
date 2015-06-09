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

coGesTemplates = [agendaTemplate, agendaTemplatePDF,
                  decisionsTemplate, decisionsTemplatePDF,
                  itemProjectTemplate, itemProjectTemplatePDF,
                  itemTemplate, itemTemplatePDF]

# Users and groups -------------------------------------------------------------
dgen = UserDescriptor('dgen', [], email="test@test.be", fullname="Henry Directeur")
dfin = UserDescriptor('dfin', [], email="test@test.be", fullname="Directeur Financier")
agentInfo = UserDescriptor('agentInfo', [], email="test@test.be", fullname="Agent Service Informatique")
agentCompta = UserDescriptor('agentCompta', [], email="test@test.be", fullname="Agent Service Comptabilité")
agentPers = UserDescriptor('agentPers', [], email="test@test.be", fullname="Agent Service du Personnel")
chefPers = UserDescriptor('chefPers', [], email="test@test.be", fullname="Chef Personnel")
chefCompta = UserDescriptor('chefCompta', [], email="test@test.be", fullname="Chef Comptabilité")

groups = [GroupDescriptor('dirgen', 'Directeur Général', 'DG'),
          GroupDescriptor('secretariat', 'Secrétariat communal', 'Secr'),
          GroupDescriptor('informatique', 'Service informatique', 'Info'),
          GroupDescriptor('personnel', 'Service du personnel', 'Pers'),
          GroupDescriptor('dirfin', 'Directeur Financier', 'DF'),
          GroupDescriptor('comptabilite', 'Service comptabilité', 'Compt')]

# MeetingManager
groups[0].creators.append(dgen)
groups[0].reviewers.append(dgen)
groups[0].observers.append(dgen)
groups[0].advisers.append(dgen)

groups[1].creators.append(dgen)
groups[1].reviewers.append(dgen)
groups[1].observers.append(dgen)
groups[1].advisers.append(dgen)

groups[2].creators.append(agentInfo)
groups[2].creators.append(dgen)
groups[2].reviewers.append(agentInfo)
groups[2].reviewers.append(dgen)
groups[2].observers.append(agentInfo)
groups[2].advisers.append(agentInfo)

groups[3].creators.append(agentPers)
groups[3].observers.append(agentPers)
groups[3].creators.append(dgen)
groups[3].reviewers.append(dgen)
groups[3].creators.append(chefPers)
groups[3].reviewers.append(chefPers)
groups[3].observers.append(chefPers)

groups[4].creators.append(dfin)
groups[4].reviewers.append(dfin)
groups[4].observers.append(dfin)
groups[4].advisers.append(dfin)

groups[5].creators.append(agentCompta)
groups[5].creators.append(chefCompta)
groups[5].creators.append(dfin)
groups[5].creators.append(dgen)
groups[5].reviewers.append(chefCompta)
groups[5].reviewers.append(dfin)
groups[5].reviewers.append(dgen)
groups[5].observers.append(agentCompta)
groups[5].advisers.append(chefCompta)
groups[5].advisers.append(dfin)

# Meeting configurations -------------------------------------------------------
# coGest
coGestMeeting = MeetingConfigDescriptor(
    'cogest', 'Comité de gestion',
    'Comité de gestion')
coGestMeeting.meetingManagers = ['dgen', ]
coGestMeeting.assembly = 'Pierre Dupont - Secrétaire,\n' \
                         'Charles Exemple - Premier membre assemblée,\n' \
                         'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                         'Charles Exemple - Président,\n' \
                         'Jacqueline Exemple, Observateur'
coGestMeeting.signatures = 'Le Secrétaire communal\nPierre Dupont\nLe Président\nCharles Exemple'
coGestMeeting.certifiedSignatures = [
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
coGestMeeting.places = """Place1\r
Place2\r
Place3\r"""
coGestMeeting.categories = categories
coGestMeeting.shortName = 'COGES'
coGestMeeting.meetingFileTypes = [annexe, annexeDecision, annexeAvis]
coGestMeeting.usedItemAttributes = ['detailedDescription',
                                    'budgetInfos',
                                    'observations',
                                    'toDiscuss',
                                    'itemAssembly',
                                    'itemIsSigned', ]
coGestMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
coGestMeeting.recordMeetingHistoryStates = []
coGestMeeting.itemsListVisibleColumns = ['toDiscuss',
                                         'state',
                                         'proposingGroup',
                                         'annexes',
                                         'annexesDecision',
                                         'advices',
                                         'actions',
                                         'itemIsSigned', ]
coGestMeeting.itemColumns = ['creator',
                             'state',
                             'proposingGroup',
                             'annexes',
                             'annexesDecision',
                             'advices',
                             'actions',
                             'meeting',
                             'itemIsSigned', ]
coGestMeeting.xhtmlTransformFields = ()
coGestMeeting.xhtmlTransformTypes = ()
coGestMeeting.itemWorkflow = 'meetingitemcollege_workflow'
coGestMeeting.meetingWorkflow = 'meetingcollege_workflow'
coGestMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
coGestMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
coGestMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
coGestMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
coGestMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
coGestMeeting.meetingTopicStates = ('created', 'frozen')
coGestMeeting.decisionTopicStates = ('decided', 'closed')
coGestMeeting.enforceAdviceMandatoriness = False
coGestMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                            'reverse': '0'}, )
coGestMeeting.recordItemHistoryStates = []
coGestMeeting.maxShownMeetings = 5
coGestMeeting.maxDaysDecisions = 60
coGestMeeting.meetingAppDefaultView = 'searchmyitems'
coGestMeeting.useAdvices = True
coGestMeeting.itemAdviceStates = ('validated',)
coGestMeeting.itemAdviceEditStates = ('validated',)
coGestMeeting.itemAdviceViewStates = ('validated',
                                      'presented',
                                      'itemfrozen',
                                      'accepted',
                                      'refused',
                                      'accepted_but_modified',
                                      'delayed',
                                      'pre_accepted',)
coGestMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
coGestMeeting.enableAdviceInvalidation = False
coGestMeeting.itemAdviceInvalidateStates = []
coGestMeeting.customAdvisers = []
coGestMeeting.itemPowerObserversStates = ('itemfrozen',
                                          'accepted',
                                          'delayed',
                                          'refused',
                                          'accepted_but_modified',
                                          'pre_accepted')
coGestMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
coGestMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
coGestMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:Le Comité décide de reporter le point."},))
coGestMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
coGestMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
coGestMeeting.powerAdvisersGroups = ('dirgen', 'dirfin', )
coGestMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
coGestMeeting.useCopies = True
coGestMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                      groups[1].getIdSuffixed('reviewers'),
                                      groups[2].getIdSuffixed('reviewers'),
                                      groups[4].getIdSuffixed('reviewers')]
coGestMeeting.podTemplates = coGesTemplates
coGestMeeting.meetingConfigsToCloneTo = []
coGestMeeting.recurringItems = []
coGestMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(coGestMeeting, ),
                                 groups=groups)
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
