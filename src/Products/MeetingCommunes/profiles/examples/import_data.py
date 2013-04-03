# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import *

# File types -------------------------------------------------------------------
simpleAnnex = MeetingFileTypeDescriptor('annex', 'Annex', 'attach.png', '')
budgetAnnex = MeetingFileTypeDescriptor('budgetAnnex', 'Budget annex', 'budget.png', '')
requirementsAnnex = MeetingFileTypeDescriptor('requirementsAnnex', 'Requirements annex', 'cahier.gif', '')
decisionAnnex = MeetingFileTypeDescriptor('decisionAnnex', 'Decision annex', 'attach.png', '', True)
# Categories -------------------------------------------------------------------
recurring = CategoryDescriptor('recurring', 'Recurring')
categories = [recurring,
              CategoryDescriptor('work', 'Work'),
              CategoryDescriptor('townplanning', 'Town planning'),
              CategoryDescriptor('accountancy', 'Accountancy'),
              CategoryDescriptor('personnel', 'Personnel'),
              CategoryDescriptor('population', 'Population'),
              CategoryDescriptor('renting', 'Renting'),
              CategoryDescriptor('various', 'Various'),
             ]

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplate.podTemplate = 'college-oj.odt'
agendaTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'

agendaTemplatePDF = PodTemplateDescriptor('oj-pdf', 'Ordre du jour')
agendaTemplatePDF.podTemplate = 'college-oj.odt'
agendaTemplatePDF.podFormat = 'pdf'
agendaTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.podTemplate = 'college-pv.odt'
decisionsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'

decisionsTemplatePDF = PodTemplateDescriptor('pv-pdf', 'Procès-verbal')
decisionsTemplatePDF.podTemplate = 'college-pv.odt'
decisionsTemplatePDF.podFormat = 'pdf'
decisionsTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'

itemProjectTemplate = PodTemplateDescriptor('projet-deliberation', 'Projet délibération')
itemProjectTemplate.podTemplate = 'college-projet-deliberation.odt'
itemProjectTemplate.podCondition = 'python:here.meta_type=="MeetingItem" and not here.hasMeeting()'

itemProjectTemplatePDF = PodTemplateDescriptor('projet-deliberation-pdf', 'Projet délibération')
itemProjectTemplatePDF.podTemplate = 'college-projet-deliberation.odt'
itemProjectTemplatePDF.podFormat = 'pdf'
itemProjectTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem" and not here.hasMeeting()'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.podTemplate = 'college-deliberation.odt'
itemTemplate.podCondition = 'python:here.meta_type=="MeetingItem" and here.hasMeeting()'

itemTemplatePDF = PodTemplateDescriptor('deliberation-pdf', 'Délibération')
itemTemplatePDF.podTemplate = 'college-deliberation.odt'
itemTemplatePDF.podFormat = 'pdf'
itemTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem" and here.hasMeeting()'

collegeTemplates = [agendaTemplate, agendaTemplatePDF,
                decisionsTemplate, decisionsTemplatePDF,
                itemProjectTemplate, itemProjectTemplatePDF, itemTemplate, itemTemplatePDF]

# Pod templates ----------------------------------------------------------------
agendaCouncilTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaCouncilTemplate.podTemplate = 'council-oj.odt'
agendaCouncilTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'

agendaCouncilTemplatePDF = PodTemplateDescriptor('oj-pdf', 'Ordre du jour')
agendaCouncilTemplatePDF.podTemplate = 'council-oj.odt'
agendaCouncilTemplatePDF.podFormat = 'pdf'
agendaCouncilTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'

decisionsCouncilTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsCouncilTemplate.podTemplate = 'council-pv.odt'
decisionsCouncilTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'

decisionsCouncilTemplatePDF = PodTemplateDescriptor('pv-pdf', 'Procès-verbal')
decisionsCouncilTemplatePDF.podTemplate = 'council-pv.odt'
decisionsCouncilTemplatePDF.podFormat = 'pdf'
decisionsCouncilTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_plonemeeting.isManager()'

itemCouncilRapportTemplate = PodTemplateDescriptor('rapport', 'Rapport')
itemCouncilRapportTemplate.podTemplate = 'council-rapport.odt'
itemCouncilRapportTemplate.podCondition = 'python:here.meta_type=="MeetingItem"'

itemCouncilRapportTemplatePDF = PodTemplateDescriptor('rapport-pdf', 'Rapport')
itemCouncilRapportTemplatePDF.podTemplate = 'council-rapport.odt'
itemCouncilRapportTemplatePDF.podFormat = 'pdf'
itemCouncilRapportTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem"'

itemCouncilProjectTemplate = PodTemplateDescriptor('projet-deliberation', 'Projet délibération')
itemCouncilProjectTemplate.podTemplate = 'council-projet-deliberation.odt'
itemCouncilProjectTemplate.podCondition = 'python:here.meta_type=="MeetingItem" and not here.hasMeeting()'

itemCouncilProjectTemplatePDF = PodTemplateDescriptor('projet-deliberation-pdf', 'Projet délibération')
itemCouncilProjectTemplatePDF.podTemplate = 'council-projet-deliberation.odt'
itemCouncilProjectTemplatePDF.podFormat = 'pdf'
itemCouncilProjectTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem" and not here.hasMeeting()'

itemCouncilTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemCouncilTemplate.podTemplate = 'council-deliberation.odt'
itemCouncilTemplate.podCondition = 'python:here.meta_type=="MeetingItem" and here.hasMeeting()'

itemCouncilTemplatePDF = PodTemplateDescriptor('deliberation-pdf', 'Délibération')
itemCouncilTemplatePDF.podTemplate = 'council-deliberation.odt'
itemCouncilTemplatePDF.podFormat = 'pdf'
itemCouncilTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem" and here.hasMeeting()'

councilTemplates = [agendaCouncilTemplate, agendaCouncilTemplatePDF,
                    decisionsCouncilTemplate, decisionsCouncilTemplatePDF,
                    itemCouncilRapportTemplate, itemCouncilRapportTemplatePDF,
                    itemCouncilTemplate, itemCouncilTemplatePDF, itemCouncilProjectTemplate, itemCouncilProjectTemplatePDF, ]

# Users and groups -------------------------------------------------------------
secretary = UserDescriptor('secretary', ['MeetingManager'], email="test@test.be")
burgmester = UserDescriptor('burgmester', [], email="test@test.be", fullname="Pierre Bourgmestre")
computOfficial = UserDescriptor('computOfficial', [], email="test@test.be")
accountOfficial = UserDescriptor('accountOfficial', [], email="test@test.be")
persOfficial = UserDescriptor('persOfficial', [], email="test@test.be")
workOfficial = UserDescriptor('workOfficial', [], email="test@test.be")
persLeader = UserDescriptor('persLeader', [], email="test@test.be")
accountLeader = UserDescriptor('accountLeader', [], email="test@test.be")
echevinPers = UserDescriptor('echevinPers', [], email="test@test.be")
persAdviser = UserDescriptor('persAdviser', [], email="test@test.be")

groups = [
           GroupDescriptor('secretariat', 'Secretariat', 'Secr'),
           GroupDescriptor('computing', 'Computing department', 'Comp'),
           GroupDescriptor('personnel', 'Personnel department', 'Pers'),
           GroupDescriptor('accountancy', 'Accountancy department', 'Acc', givesMandatoryAdviceOn='python:True'),
           GroupDescriptor('work', 'Work department', 'Work'),
         ]

# MeetingManager
groups[0].creators.append(secretary)
groups[0].reviewers.append(secretary)
groups[0].observers.append(secretary)
groups[0].observers.append(burgmester)
groups[0].advisers.append(secretary)

groups[1].creators.append(computOfficial)
groups[1].creators.append(secretary)
groups[1].reviewers.append(computOfficial)
groups[1].reviewers.append(secretary)
groups[1].observers.append(computOfficial)
groups[1].advisers.append(computOfficial)

groups[2].creators.append(persOfficial)
groups[2].observers.append(persOfficial)
groups[2].creators.append(secretary)
groups[2].reviewers.append(secretary)
groups[2].creators.append(persLeader)
groups[2].reviewers.append(persLeader)
groups[2].observers.append(persLeader)
groups[2].observers.append(echevinPers)
groups[2].advisers.append(persAdviser)

groups[3].creators.append(accountOfficial)
groups[3].creators.append(accountLeader)
groups[3].creators.append(secretary)
groups[3].reviewers.append(accountLeader)
groups[3].reviewers.append(secretary)
groups[3].observers.append(accountOfficial)
groups[3].advisers.append(accountLeader)

groups[4].creators.append(workOfficial)
groups[4].creators.append(secretary)
groups[4].reviewers.append(workOfficial)
groups[4].reviewers.append(secretary)
groups[4].observers.append(workOfficial)
groups[4].advisers.append(workOfficial)

# Meeting configurations -------------------------------------------------------
# college
collegeMeeting = MeetingConfigDescriptor(
    'meeting-config-college', 'Administration college',
    'Administration college', isDefault=True)
collegeMeeting.assembly = 'Pierre Dupont - Burgomaster,\n' \
                           'Charles Example - 1st municipal councillor,\n' \
                           'Councillor one, councillor two, councillor three - Councillors,\n' \
                           'Jacqueline Example, SA leader'
collegeMeeting.signatures = '1st municipal councillor\nPierre Dupont\nThe Burgmester\nCharles Example'
collegeMeeting.places = """Place1\n\r
Place2\n\r
Place3\n\r"""
collegeMeeting.categories = categories
collegeMeeting.shortName = 'College'
collegeMeeting.meetingFileTypes = [simpleAnnex, budgetAnnex, requirementsAnnex, decisionAnnex]
collegeMeeting.usedItemAttributes = ['detailedDescription', 'budgetInfos', 'observations', 'toDiscuss', 'itemAssembly', 'itemIsSigned',]
collegeMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
collegeMeeting.recordMeetingHistoryStates = []
collegeMeeting.itemsListVisibleColumns = ['toDiscuss', 'state', 'proposingGroup', 'annexes', 'annexesDecision', 'advices', 'actions', 'itemIsSigned',]
collegeMeeting.itemColumns = ['creator', 'state', 'proposingGroup', 'annexes', 'annexesDecision', 'advices', 'actions', 'meeting', 'itemIsSigned', ]
collegeMeeting.xhtmlTransformFields = ('MeetingItem.description', 'MeetingItem.detailedDescription', 'MeetingItem.decision', 'MeetingItem.observations', 'Meeting.observations', )
collegeMeeting.xhtmlTransformTypes = ('removeBlanks',)
collegeMeeting.itemWorkflow = 'meetingitemcollege_workflow'
collegeMeeting.meetingWorkflow = 'meetingcollege_workflow'
collegeMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
collegeMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
collegeMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
collegeMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
collegeMeeting.transitionsToConfirm = ['MeetingItem.delay',]
collegeMeeting.itemTopicStates = ('itemcreated', 'proposed', 'validated', 'presented', 'itemfrozen', 'pre_accepted', 'accepted', 'refused', 'delayed', 'accepted_but_modified', )
collegeMeeting.meetingTopicStates = ('created', 'frozen')
collegeMeeting.decisionTopicStates = ('decided', 'closed')
collegeMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
collegeMeeting.enforceAdviceMandatoriness = False
collegeMeeting.recordItemHistoryStates = []
collegeMeeting.maxShownMeetings = 5
collegeMeeting.maxDaysDecisions = 60
collegeMeeting.meetingAppDefaultView = 'topic_searchmyitems'
collegeMeeting.itemDocFormats = ('odt', 'pdf')
collegeMeeting.meetingDocFormats = ('odt', 'pdf')
collegeMeeting.useAdvices = True
collegeMeeting.itemAdviceStates = ('validated',)
collegeMeeting.itemAdviceEditStates = ('validated',)
collegeMeeting.itemAdviceViewStates = ('validated', 'presented', 'itemfrozen', 'accepted', 'refused', 'accepted_but_modified', 'delayed', 'pre_accepted',)
collegeMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
collegeMeeting.enableAdviceInvalidation = False
collegeMeeting.itemAdviceInvalidateStates = []
collegeMeeting.itemPowerObserversStates = ('itemfrozen', 'accepted', 'delayed', 'refused', 'accepted_but_modified')
collegeMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified','pre_accepted']
collegeMeeting.meetingPowerObserversStates = ('created', 'frozen', 'decided', 'closed')
collegeMeeting.useCopies = True
collegeMeeting.selectableCopyGroups = ['secretariat_reviewers', 'computing_reviewers', 'personnel_reviewers', 'accountancy_reviewers', 'work_reviewers']
collegeMeeting.podTemplates = collegeTemplates

collegeMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approve the decisions report of the last meeting',
        description='Approve the decisions report of the last meeting',
        category='recurring',
        proposingGroup='secretariat',
        decision='The last decisions report is approved.'),
    RecurringItemDescriptor(
        id='recurringofficialreport1',
        title='Approve and sign the weeks purchase orders',
        description='Approve and sign the weeks purchase orders',
        category='recurring',
        proposingGroup='secretariat',
        decision='The weeks purchase orders are signed.'),
    RecurringItemDescriptor(
        id='recurringofficialreport2',
        title='Sign weeks payment orders',
        description='Sign weeks payment orders',
        category='recurring',
        proposingGroup='secretariat',
        decision='The weeks payment orders are signed.'),
    ]

# City council
councilMeeting = MeetingConfigDescriptor(
    'meeting-config-council', 'Administration council',
    'Administration Council')
councilMeeting.assembly = 'Pierre Dupont - Burgmester,\n' \
                           'Charles Exemple - 1er Echevin,\n' \
                           'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                           'Jacqueline Exemple, Responsable du CPAS'
councilMeeting.signatures = '1st municipal councillor\nPierre Dupont\nThe Burgmester\nCharles Example'
councilMeeting.places = """Place1\n\r
Place2\n\r
Place3\n\r"""
councilMeeting.categories = categories
councilMeeting.shortName = 'Council'
councilMeeting.meetingFileTypes = [simpleAnnex, budgetAnnex, requirementsAnnex, decisionAnnex]
councilMeeting.usedItemAttributes = ['detailedDescription', 'oralQuestion', 'itemInitiator', 'observations', 'privacy', 'itemAssembly', ]
councilMeeting.usedMeetingAttributes = ['startDate', 'midDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
councilMeeting.recordMeetingHistoryStates = []
councilMeeting.itemsListVisibleColumns = ['state', 'proposingGroup', 'annexes', 'annexesDecision', 'actions', ]
councilMeeting.itemColumns = ['creator', 'state', 'proposingGroup', 'annexes', 'annexesDecision', 'advices', 'actions', 'meeting', ]
councilMeeting.xhtmlTransformFields = ('MeetingItem.description', 'MeetingItem.detailedDescription', 'MeetingItem.decision', 'MeetingItem.observations', 'Meeting.observations', )
councilMeeting.xhtmlTransformTypes = ('removeBlanks',)
councilMeeting.itemWorkflow = 'meetingitemcouncil_workflow'
councilMeeting.meetingWorkflow = 'meetingcouncil_workflow'
councilMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCouncilWorkflowConditions'
councilMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCouncilWorkflowActions'
councilMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCouncilWorkflowConditions'
councilMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCouncilWorkflowActions'
#show every items states
councilMeeting.transitionsToConfirm = []
councilMeeting.itemTopicStates = ('itemcreated', 'proposed', 'validated', 'presented', 'itemfrozen', 'itempublished', 'accepted', 'pre_accepted', 'accepted_but_modified', 'refused', 'delayed')
councilMeeting.meetingTopicStates = ('created', 'frozen', 'published')
councilMeeting.decisionTopicStates = ('decided', 'closed')
councilMeeting.itemAdviceStates = ('validated',)
councilMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
councilMeeting.enforceAdviceMandatoriness = False
councilMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
councilMeeting.recordItemHistoryStates = []
councilMeeting.maxShownMeetings = 5
councilMeeting.maxDaysDecisions = 60
councilMeeting.meetingAppDefaultView = 'topic_searchmyitems'
councilMeeting.itemDocFormats = ('odt', 'pdf')
councilMeeting.meetingDocFormats = ('odt', 'pdf')
councilMeeting.useAdvices = False
councilMeeting.itemPowerObserversStates = ('itemfrozen', 'accepted', 'delayed', 'refused', 'accepted_but_modified')
councilMeeting.meetingPowerObserversStates = ('created', 'frozen', 'published', 'decided', 'closed')
councilMeeting.useCopies = True
councilMeeting.selectableCopyGroups = ['secretariat_reviewers', 'computing_reviewers', 'personnel_reviewers', 'accountancy_reviewers', 'work_reviewers']
councilMeeting.podTemplates = councilTemplates

secretaire_mu = MeetingUserDescriptor('secretaire', duty='Secrétaire communal', usages=['assemblyMember', 'signer', 'asker', ])
bourgmestre_mu = MeetingUserDescriptor('bourgmestre', duty='Bourgmestre', usages=['assemblyMember', 'asker', ])
echevinPers_mu = MeetingUserDescriptor('echevinPers', duty='Echevin GRH', usages=['assemblyMember', 'asker', ])

councilMeeting.meetingUsers = [secretaire_mu, bourgmestre_mu, echevinPers_mu, ]

councilMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approve the decisions report of the last meeting',
        description='Approve the decisions report of the last meeting',
        category='recurring',
        proposingGroup='secretariat',
        decision='The last decisions report is approved.'),
    ]

data = PloneMeetingConfiguration(
           meetingFolderTitle='My meetings',
           meetingConfigs=(collegeMeeting,councilMeeting),
           groups=groups)
data.unoEnabledPython='/usr/bin/python'
# ------------------------------------------------------------------------------
