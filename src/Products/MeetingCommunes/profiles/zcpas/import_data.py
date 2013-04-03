# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import *

# File types -------------------------------------------------------------------
annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeBudget = MeetingFileTypeDescriptor('annexeBudget', 'Article Budgétaire', 'budget.png', '')
annexeCahier = MeetingFileTypeDescriptor('annexeCahier', 'Cahier des Charges', 'cahier.gif', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe à la décision', 'attach.png', '', True)
# Categories -------------------------------------------------------------------
categories = [
              CategoryDescriptor('recurrents', 'Récurrents'),
              CategoryDescriptor('demissions', 'Démission(s)'),
              CategoryDescriptor('designations', 'Désignation(s)'),
              CategoryDescriptor('compte', 'Compte'),
              CategoryDescriptor('budget', 'Budget'),
              CategoryDescriptor('contentieux', 'Contentieux'),
              CategoryDescriptor('eco-sociale', 'Economie sociale'),
              CategoryDescriptor('aide-familles', "Service d'aide aux familles"),
              CategoryDescriptor('marches-publics', 'Marchés publics'),
              CategoryDescriptor('divers', 'Divers'), 
             ]

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('agenda', 'Ordre du jour')
agendaTemplate.podTemplate = 'Agenda.odt'
agendaTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_membership.' \
                              'getAuthenticatedMember().has_role("' \
                              'MeetingManager")'

agendaTemplatePDF = PodTemplateDescriptor('agendapdf', 'Ordre du jour')
agendaTemplatePDF.podTemplate = 'Agenda.odt'
agendaTemplatePDF.podFormat = 'pdf'
agendaTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                  'here.portal_membership.' \
                                  'getAuthenticatedMember().has_role("' \
                                  'MeetingManager")'

decisionsTemplate = PodTemplateDescriptor('decisions', 'Procès-verbal')
decisionsTemplate.podTemplate = 'Decisions.odt'
decisionsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_membership.' \
                                 'getAuthenticatedMember().has_role("' \
                                 'MeetingManager")'

decisionsTemplatePDF = PodTemplateDescriptor('decisionspdf', 'Procès-verbal')
decisionsTemplatePDF.podTemplate = 'Decisions.odt'
decisionsTemplatePDF.podFormat = 'pdf'
decisionsTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                    'here.portal_membership.' \
                                    'getAuthenticatedMember().has_role("' \
                                    'MeetingManager")'
decisionsByCatTemplate = PodTemplateDescriptor('decisionsbycat', 'PV avec catégories')
decisionsByCatTemplate.podTemplate = 'DecisionsWithItemsByCategory.odt'
decisionsByCatTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_membership.' \
                                 'getAuthenticatedMember().has_role("' \
                                 'MeetingManager")'

decisionsByCatTemplatePDF = PodTemplateDescriptor('decisionsbycatpdf', 'PV avec catégories')
decisionsByCatTemplatePDF.podTemplate = 'DecisionsWithItemsByCategory.odt'
decisionsByCatTemplatePDF.podFormat = 'pdf'
decisionsByCatTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                    'here.portal_membership.' \
                                    'getAuthenticatedMember().has_role("' \
                                    'MeetingManager")'

itemTemplate = PodTemplateDescriptor('item', 'Délibération')
itemTemplate.podTemplate = 'MeetingItem.odt'
itemTemplate.podCondition = 'python:here.meta_type=="MeetingItem"'

itemTemplatePDF = PodTemplateDescriptor('itempdf', 'Délibération')
itemTemplatePDF.podTemplate = 'MeetingItem.odt'
itemTemplatePDF.podFormat = 'pdf'
itemTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem"'

allTemplates = [agendaTemplate, agendaTemplatePDF,
                decisionsTemplate, decisionsTemplatePDF,
                decisionsByCatTemplate, decisionsByCatTemplatePDF,
                itemTemplate, itemTemplatePDF]

# Users and groups -------------------------------------------------------------
secretaire = UserDescriptor('secretaire', ['MeetingManager'], email="test@test.be")
agentInfo = UserDescriptor('agentInfo', [], email="test@test.be")
agentCompta = UserDescriptor('agentCompta', [], email="test@test.be")
agentPers = UserDescriptor('agentPers', [], email="test@test.be")
agentIsp = UserDescriptor('agentIsp', [], email="test@test.be")
chefPers = UserDescriptor('chefPers', [], email="test@test.be")
chefCompta = UserDescriptor('chefCompta', [], email="test@test.be")
echevinPers = UserDescriptor('echevinPers', [], email="test@test.be")
emetteuravisPers = UserDescriptor('emetteuravisPers', [], email="test@test.be")

groups = [
          GroupDescriptor('admingen', 'Administration générale', 'AdminGen'),
          GroupDescriptor('aidefamilles', 'Aide aux familles', 'Aide'),
          GroupDescriptor('comptabilite', 'Comptabilité', 'Compta'),
          GroupDescriptor('informatique', 'Informatique', 'Info'),
          GroupDescriptor('isp', 'Insertion socio-professionnelle', 'ISP'),
          GroupDescriptor('dettes', 'Médiation de dettes', 'Dettes'),
          GroupDescriptor('personnel', 'Personnel', 'Pers', givesMandatoryAdviceOn='python:True'),
          GroupDescriptor('social', 'Social', 'Soc'),
          GroupDescriptor('divers', 'Divers', 'Divers'),
         ]
# MeetingManager
groups[0].creators.append(secretaire)
groups[0].reviewers.append(secretaire)
groups[0].observers.append(secretaire)
groups[0].advisers.append(secretaire)

groups[1].creators.append(secretaire)
groups[1].reviewers.append(secretaire)
groups[1].observers.append(secretaire)
groups[1].advisers.append(secretaire)

groups[2].creators.append(agentCompta)
groups[2].creators.append(chefCompta)
groups[2].creators.append(secretaire)
groups[2].reviewers.append(chefCompta)
groups[2].advisers.append(chefCompta)

groups[3].creators.append(agentInfo)
groups[3].creators.append(secretaire)
groups[3].reviewers.append(agentInfo)
groups[3].advisers.append(agentInfo)

groups[4].creators.append(agentIsp)
groups[4].creators.append(secretaire)
groups[4].reviewers.append(agentIsp)
groups[4].reviewers.append(secretaire)
groups[4].advisers.append(agentIsp)

groups[6].creators.append(agentPers)
groups[6].creators.append(secretaire)
groups[6].reviewers.append(chefPers)
groups[6].reviewers.append(secretaire)
groups[6].advisers.append(emetteuravisPers)
groups[6].observers.append(echevinPers)


# Meeting configurations -------------------------------------------------------
# bp
bpMeeting = MeetingConfigDescriptor(
    'meeting-config-bp', 'Bureau permanent',
    'Bureau permanent', isDefault=True)
bpMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                     'Charles Exemple - 1er Echevin,\n' \
                     'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                     'Jacqueline Exemple, Responsable du CPAS'
bpMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, 1er Echevin'
bpMeeting.categories = categories
bpMeeting.shortName = 'bp'
bpMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, annexeDecision]
bpMeeting.usedItemAttributes = ['budgetInfos', 'observations', ]
bpMeeting.usedMeetingAttributes = ['assembly', 'signatures', 'observations', 'place', ]
bpMeeting.itemWorkflow = 'meetingitemcollege_workflow'
bpMeeting.meetingWorkflow = 'meetingcollege_workflow'
bpMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
bpMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
bpMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
bpMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
bpMeeting.transitionsToConfirm = []
bpMeeting.itemTopicStates = ('itemcreated', 'proposed', 'validated', 'presented', 'itemfrozen', 'pre_accepted', 'accepted', 'refused', 'delayed', 'accepted_but_modified', )
bpMeeting.meetingTopicStates = ('created', 'frozen')
bpMeeting.decisionTopicStates = ('decided', 'closed')
bpMeeting.itemAdviceStates = ('validated',)
bpMeeting.enforceAdviceMandatoriness = False
bpMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
bpMeeting.recordItemHistoryStates = []
bpMeeting.maxShownMeetings = 5
bpMeeting.maxDaysDecisions = 60
bpMeeting.meetingAppDefaultView = 'topic_searchmyitems'
bpMeeting.itemDocFormats = ('odt', 'pdf')
bpMeeting.meetingDocFormats = ('odt', 'pdf')
bpMeeting.useAdvices = True
bpMeeting.itemAdviceStates = ('validated',)
bpMeeting.itemAdviceEditStates = ('validated',)
bpMeeting.itemAdviceViewStates = ('validated', 'presented', 'itemfrozen', 'accepted', 'refused', 'accepted_but_modified', 'delayed', 'pre_accepted',)
bpMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified','pre_accepted']
bpMeeting.useCopies = True
bpMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'), groups[1].getIdSuffixed('reviewers'), groups[2].getIdSuffixed('reviewers'), groups[4].getIdSuffixed('reviewers')]
bpMeeting.podTemplates = allTemplates

bpMeeting.recurringItems = [
    # Agenda items
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance antérieure',
        description='Approuve le procès-verbal de la séance antérieure',
        category='recurrents',
        proposingGroup='admingen',
        decision='Procès-verbal approuvé'),
    ]

# CAS
casMeeting = MeetingConfigDescriptor(
    'meeting-config-cas', "Conseil de l'Action Sociale",
    "Conseil de l'Action Sociale", isDefault=False)
casMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                      'Charles Exemple - 1er Echevin,\n' \
                      'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                      'Jacqueline Exemple, Responsable du CPAS'
casMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, 1er Echevin'
casMeeting.categories = categories
casMeeting.shortName = 'cas'
casMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, annexeDecision]
casMeeting.usedItemAttributes = ['budgetInfos', 'observations', ]
casMeeting.usedMeetingAttributes = ['assembly', 'signatures', 'observations', 'place', ]
casMeeting.itemWorkflow = 'meetingitemcollege_workflow'
casMeeting.meetingWorkflow = 'meetingcollege_workflow'
casMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
casMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
casMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
casMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
casMeeting.transitionsToConfirm = []
casMeeting.itemTopicStates = ('itemcreated', 'proposed', 'validated', 'presented', 'itemfrozen', 'pre_accepted', 'accepted', 'refused', 'delayed', 'accepted_but_modified', )
casMeeting.meetingTopicStates = ('created', 'frozen')
casMeeting.decisionTopicStates = ('decided', 'closed')
casMeeting.itemAdviceStates = ('validated',)
casMeeting.enforceAdviceMandatoriness = False
casMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
casMeeting.recordItemHistoryStates = []
casMeeting.maxShownMeetings = 5
casMeeting.maxDaysDecisions = 60
casMeeting.meetingAppDefaultView = 'topic_searchmyitems'
casMeeting.itemDocFormats = ('odt', 'pdf')
casMeeting.meetingDocFormats = ('odt', 'pdf')
casMeeting.useAdvices = True
casMeeting.itemAdviceStates = ('validated',)
casMeeting.itemAdviceEditStates = ('validated',)
casMeeting.itemAdviceViewStates = ('validated', 'presented', 'itemfrozen', 'accepted', 'refused', 'accepted_but_modified', 'delayed', 'pre_accepted',)
casMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
casMeeting.useCopies = True
casMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'), groups[1].getIdSuffixed('reviewers'), groups[2].getIdSuffixed('reviewers'), groups[4].getIdSuffixed('reviewers')]
casMeeting.podTemplates = allTemplates

casMeeting.recurringItems = [
    # Agenda items
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance antérieure',
        description='Approuve le procès-verbal de la séance antérieure',
        category='recurrents',
        proposingGroup='admingen',
        decision='Procès-verbal approuvé'),
    ]

# Comitee
comiteeMeeting = MeetingConfigDescriptor(
    'meeting-config-comitee', 'Comité de concertation Commune/CPAS',
    'Comité de concertation Commune/CPAS', isDefault=False)
comiteeMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                          'Charles Exemple - 1er Echevin,\n' \
                          'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                          'Jacqueline Exemple, Responsable du CPAS'
comiteeMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, 1er Echevin'
comiteeMeeting.categories = categories
comiteeMeeting.shortName = 'comitee'
comiteeMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, annexeDecision]
comiteeMeeting.usedItemAttributes = ['budgetInfos', 'observations', ]
comiteeMeeting.usedMeetingAttributes = ['assembly', 'signatures', 'observations', 'place', ]
comiteeMeeting.itemWorkflow = 'meetingitemcollege_workflow'
comiteeMeeting.meetingWorkflow = 'meetingcollege_workflow'
comiteeMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
comiteeMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
comiteeMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
comiteeMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
comiteeMeeting.transitionsToConfirm = []
comiteeMeeting.itemTopicStates = ('itemcreated', 'proposed', 'validated', 'presented', 'itemfrozen', 'pre_accepted', 'accepted', 'refused', 'delayed', 'accepted_but_modified', )
comiteeMeeting.meetingTopicStates = ('created', 'frozen')
comiteeMeeting.decisionTopicStates = ('decided', 'closed')
comiteeMeeting.itemAdviceStates = ('validated',)
comiteeMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
comiteeMeeting.enforceAdviceMandatoriness = False
comiteeMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
comiteeMeeting.recordItemHistoryStates = []
comiteeMeeting.maxShownMeetings = 5
comiteeMeeting.maxDaysDecisions = 60
comiteeMeeting.meetingAppDefaultView = 'topic_searchmyitems'
comiteeMeeting.itemDocFormats = ('odt', 'pdf')
comiteeMeeting.meetingDocFormats = ('odt', 'pdf')
comiteeMeeting.useAdvices = True
comiteeMeeting.itemAdviceStates = ('validated',)
comiteeMeeting.itemAdviceEditStates = ('validated',)
comiteeMeeting.itemAdviceViewStates = ('validated', 'presented', 'itemfrozen', 'accepted', 'refused', 'accepted_but_modified', 'delayed', 'pre_accepted',)
comiteeMeeting.useCopies = True
comiteeMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'), groups[1].getIdSuffixed('reviewers'), groups[2].getIdSuffixed('reviewers'), groups[4].getIdSuffixed('reviewers')]
comiteeMeeting.podTemplates = allTemplates

comiteeMeeting.recurringItems = [
    # Agenda items
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance antérieure',
        description='Approuve le procès-verbal de la séance antérieure',
        category='recurrents',
        proposingGroup='admingen',
        decision='Procès-verbal approuvé'),
    ]

# global data
data = PloneMeetingConfiguration(
           meetingFolderTitle='Mes séances',
           meetingConfigs=(bpMeeting, casMeeting, comiteeMeeting,),
           groups=groups)
data.unoEnabledPython='/usr/bin/python'
# ------------------------------------------------------------------------------
