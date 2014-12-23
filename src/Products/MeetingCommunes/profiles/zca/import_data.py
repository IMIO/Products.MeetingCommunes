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
agendaTemplate.podTemplate = '../../examples_fr/templates/college-oj.odt'
agendaTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'

agendaTemplatePDF = PodTemplateDescriptor('oj-pdf', 'Ordre du jour')
agendaTemplatePDF.podTemplate = 'ca-oj.odt'
agendaTemplatePDF.podFormat = 'pdf'
agendaTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_plonemeeting.isManager()'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.podTemplate = 'ca-pv.odt'
decisionsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_plonemeeting.isManager()'

decisionsTemplatePDF = PodTemplateDescriptor('pv-pdf', 'Procès-verbal')
decisionsTemplatePDF.podTemplate = 'ca-pv.odt'
decisionsTemplatePDF.podFormat = 'pdf'
decisionsTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                    'here.portal_plonemeeting.isManager()'

itemProjectTemplate = PodTemplateDescriptor('projet-deliberation', 'Projet délibération')
itemProjectTemplate.podTemplate = 'projet-deliberation.odt'
itemProjectTemplate.podCondition = 'python:here.meta_type=="MeetingItem" and not here.hasMeeting()'

itemProjectTemplatePDF = PodTemplateDescriptor('projet-deliberation-pdf', 'Projet délibération')
itemProjectTemplatePDF.podTemplate = 'projet-deliberation.odt'
itemProjectTemplatePDF.podFormat = 'pdf'
itemProjectTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem" and not here.hasMeeting()'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.podTemplate = 'deliberation.odt'
itemTemplate.podCondition = 'python:here.meta_type=="MeetingItem" and here.hasMeeting()'

itemTemplatePDF = PodTemplateDescriptor('deliberation-pdf', 'Délibération')
itemTemplatePDF.podTemplate = 'deliberation.odt'
itemTemplatePDF.podFormat = 'pdf'
itemTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem" and here.hasMeeting()'

caTemplates = [agendaTemplate, agendaTemplatePDF,
               decisionsTemplate, decisionsTemplatePDF,
               itemProjectTemplate, itemProjectTemplatePDF,
               itemTemplate, itemTemplatePDF]

# Users and groups -------------------------------------------------------------
dgen = UserDescriptor('dgen', ['MeetingManager'], email="test@test.be", fullname="Henry Directeur")
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
# ca
caMeeting = MeetingConfigDescriptor(
    'ca', 'Conseil d\'Administration',
    'Conseil d\'Administration')
caMeeting.assembly = 'Pierre Dupont - Président,\n' \
                     'Charles Exemple - Premier membre assemblée,\n' \
                     'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                     'Jacqueline Exemple, Observateur'
caMeeting.signatures = 'Le Secrétaire communal\nPierre Dupont\nLe Bourgmestre\nCharles Exemple'
caMeeting.certifiedSignatures = 'Le Secrétaire communal\nVraiment Présent\nLe Bourgmestre\nCharles Exemple'
caMeeting.places = """Place1\r
Place2\r
Place3\r"""
caMeeting.categories = categories
caMeeting.shortName = 'CA'
caMeeting.meetingFileTypes = [annexe, annexeDecision, annexeAvis]
caMeeting.usedItemAttributes = ['detailedDescription',
                                'budgetInfos',
                                'observations',
                                'toDiscuss',
                                'itemAssembly',
                                'itemIsSigned', ]
caMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
caMeeting.recordMeetingHistoryStates = []
caMeeting.itemsListVisibleColumns = ['toDiscuss',
                                     'state',
                                     'proposingGroup',
                                     'annexes',
                                     'annexesDecision',
                                     'advices',
                                     'actions',
                                     'itemIsSigned', ]
caMeeting.itemColumns = ['creator',
                         'state',
                         'proposingGroup',
                         'annexes',
                         'annexesDecision',
                         'advices',
                         'actions',
                         'meeting',
                         'itemIsSigned', ]
caMeeting.xhtmlTransformFields = ()
caMeeting.xhtmlTransformTypes = ()
caMeeting.itemWorkflow = 'meetingitemcollege_workflow'
caMeeting.meetingWorkflow = 'meetingcollege_workflow'
caMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
caMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
caMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
caMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
caMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
caMeeting.meetingTopicStates = ('created', 'frozen')
caMeeting.decisionTopicStates = ('decided', 'closed')
caMeeting.enforceAdviceMandatoriness = False
caMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                        'reverse': '0'}, )
caMeeting.recordItemHistoryStates = []
caMeeting.maxShownMeetings = 5
caMeeting.maxDaysDecisions = 60
caMeeting.meetingAppDefaultView = 'topic_searchmyitems'
caMeeting.useAdvices = True
caMeeting.itemAdviceStates = ('validated',)
caMeeting.itemAdviceEditStates = ('validated',)
caMeeting.itemAdviceViewStates = ('validated',
                                  'presented',
                                  'itemfrozen',
                                  'accepted',
                                  'refused',
                                  'accepted_but_modified',
                                  'delayed',
                                  'pre_accepted',)
caMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
caMeeting.enableAdviceInvalidation = False
caMeeting.itemAdviceInvalidateStates = []
caMeeting.customAdvisers = []
caMeeting.itemPowerObserversStates = ('itemfrozen',
                                      'accepted',
                                      'delayed',
                                      'refused',
                                      'accepted_but_modified',
                                      'pre_accepted')
caMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
caMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
caMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:Le Comité décide de reporter le point."},))
caMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
caMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
caMeeting.powerAdvisersGroups = ('dirgen', 'dirfin', )
caMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
caMeeting.useCopies = True
caMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                  groups[1].getIdSuffixed('reviewers'),
                                  groups[2].getIdSuffixed('reviewers'),
                                  groups[4].getIdSuffixed('reviewers')]
caMeeting.podTemplates = caTemplates
caMeeting.meetingConfigsToCloneTo = []
caMeeting.recurringItems = []
caMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(caMeeting, ),
                                 groups=groups)
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
