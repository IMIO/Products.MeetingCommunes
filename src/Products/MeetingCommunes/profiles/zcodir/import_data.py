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
agendaTemplate.podTemplate = 'codir-oj.odt'
agendaTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'

agendaTemplatePDF = PodTemplateDescriptor('oj-pdf', 'Ordre du jour')
agendaTemplatePDF.podTemplate = 'codir-oj.odt'
agendaTemplatePDF.podFormat = 'pdf'
agendaTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_plonemeeting.isManager()'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.podTemplate = 'codir-pv.odt'
decisionsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_plonemeeting.isManager()'

decisionsTemplatePDF = PodTemplateDescriptor('pv-pdf', 'Procès-verbal')
decisionsTemplatePDF.podTemplate = 'codir-pv.odt'
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

codirTemplates = [agendaTemplate, agendaTemplatePDF,
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
# codir
codirMeeting = MeetingConfigDescriptor(
    'codir', 'Comité de Direction',
    'Comité de Direction')
codirMeeting.assembly = 'Pierre Dupont - Président,\n' \
                        'Charles Exemple - Premier membre assemblée,\n' \
                        'Luc Un, Luc Deux, Luc Trois - Membres,\n' \
                        'Jacqueline Exemple, Observateur'
codirMeeting.signatures = 'Le Secrétaire communal\nPierre Dupont\nLe Bourgmestre\nCharles Exemple'
codirMeeting.certifiedSignatures = 'Le Secrétaire communal\nVraiment Présent\nLe Bourgmestre\nCharles Exemple'
codirMeeting.places = """Place1\r
Place2\r
Place3\r"""
codirMeeting.categories = categories
codirMeeting.shortName = 'CoDir'
codirMeeting.meetingFileTypes = [annexe, annexeDecision, annexeAvis]
codirMeeting.usedItemAttributes = ['detailedDescription',
                                   'budgetInfos',
                                   'observations',
                                   'toDiscuss',
                                   'itemAssembly',
                                   'itemIsSigned', ]
codirMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
codirMeeting.recordMeetingHistoryStates = []
codirMeeting.itemsListVisibleColumns = ['toDiscuss',
                                        'state',
                                        'proposingGroup',
                                        'annexes',
                                        'annexesDecision',
                                        'advices',
                                        'actions',
                                        'itemIsSigned', ]
codirMeeting.itemColumns = ['creator',
                            'state',
                            'proposingGroup',
                            'annexes',
                            'annexesDecision',
                            'advices',
                            'actions',
                            'meeting',
                            'itemIsSigned', ]
codirMeeting.xhtmlTransformFields = ()
codirMeeting.xhtmlTransformTypes = ()
codirMeeting.itemWorkflow = 'meetingitemcollege_workflow'
codirMeeting.meetingWorkflow = 'meetingcollege_workflow'
codirMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
codirMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
codirMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
codirMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
codirMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
codirMeeting.meetingTopicStates = ('created', 'frozen')
codirMeeting.decisionTopicStates = ('decided', 'closed')
codirMeeting.enforceAdviceMandatoriness = False
codirMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
codirMeeting.recordItemHistoryStates = []
codirMeeting.maxShownMeetings = 5
codirMeeting.maxDaysDecisions = 60
codirMeeting.meetingAppDefaultView = 'topic_searchmyitems'
codirMeeting.useAdvices = True
codirMeeting.itemAdviceStates = ('validated',)
codirMeeting.itemAdviceEditStates = ('validated',)
codirMeeting.itemAdviceViewStates = ('validated',
                                     'presented',
                                     'itemfrozen',
                                     'accepted',
                                     'refused',
                                     'accepted_but_modified',
                                     'delayed',
                                     'pre_accepted',)
codirMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
codirMeeting.enableAdviceInvalidation = False
codirMeeting.itemAdviceInvalidateStates = []
codirMeeting.customAdvisers = []
codirMeeting.itemPowerObserversStates = ('itemfrozen',
                                         'accepted',
                                         'delayed',
                                         'refused',
                                         'accepted_but_modified',
                                         'pre_accepted')
codirMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
codirMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
codirMeeting.itemDecisionReportText = "python:'Le collège décide de reporter le point.'"
codirMeeting.powerAdvisersGroups = ('dirgen', 'dirfin', )
codirMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
codirMeeting.useCopies = True
codirMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                     groups[1].getIdSuffixed('reviewers'),
                                     groups[2].getIdSuffixed('reviewers'),
                                     groups[4].getIdSuffixed('reviewers')]
codirMeeting.podTemplates = codirTemplates
codirMeeting.meetingConfigsToCloneTo = []
codirMeeting.recurringItems = []
codirMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(codirMeeting, ),
                                 groups=groups)
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
data.enableUserPreferences = False
# ------------------------------------------------------------------------------
