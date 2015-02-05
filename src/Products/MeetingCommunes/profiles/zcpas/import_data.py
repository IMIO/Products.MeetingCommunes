# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import GroupDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import MeetingFileTypeDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import RecurringItemDescriptor
from Products.PloneMeeting.profiles import UserDescriptor

# File types -------------------------------------------------------------------
annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeBudget = MeetingFileTypeDescriptor('annexeBudget', 'Article Budgétaire', 'budget.png', '')
annexeCahier = MeetingFileTypeDescriptor('annexeCahier', 'Cahier des Charges', 'cahier.gif', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe à la décision', 'attach.png', '', 'item_decision')
annexeAvis = MeetingFileTypeDescriptor('annexeAvis', 'Annexe à un avis',
                                       'attach.png', '', 'advice')
annexeAvisLegal = MeetingFileTypeDescriptor('annexeAvisLegal', 'Extrait article de loi',
                                            'legalAdvice.png', '', 'advice')

# Categories -------------------------------------------------------------------
categories = [CategoryDescriptor('recurrents', 'Récurrents'),
              CategoryDescriptor('demissions', 'Démission(s)'),
              CategoryDescriptor('designations', 'Désignation(s)'),
              CategoryDescriptor('compte', 'Compte'),
              CategoryDescriptor('budget', 'Budget'),
              CategoryDescriptor('contentieux', 'Contentieux'),
              CategoryDescriptor('eco-sociale', 'Economie sociale'),
              CategoryDescriptor('aide-familles', "Service d'aide aux familles"),
              CategoryDescriptor('marches-publics', 'Marchés publics'),
              CategoryDescriptor('divers', 'Divers'), ]

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('agenda', 'Ordre du jour')
agendaTemplate.podTemplate = '../../examples_fr/templates/oj.odt'
agendaTemplate.podCondition = 'python:(here.meta_type=="Meeting") and here.portal_plonemeeting.isManager()'


agendaTemplatePDF = PodTemplateDescriptor('agendapdf', 'Ordre du jour')
agendaTemplatePDF.podTemplate = '../../examples_fr/templates/oj.odt'
agendaTemplatePDF.podFormat = 'pdf'
agendaTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and here.portal_plonemeeting.isManager()'

decisionsTemplate = PodTemplateDescriptor('decisions', 'Procès-verbal')
decisionsTemplate.podTemplate = '../../examples_fr/templates/pv.odt'
decisionsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and here.portal_plonemeeting.isManager()'

decisionsTemplatePDF = PodTemplateDescriptor('decisionspdf', 'Procès-verbal')
decisionsTemplatePDF.podTemplate = '../../examples_fr/templates/pv.odt'
decisionsTemplatePDF.podFormat = 'pdf'
decisionsTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and here.portal_plonemeeting.isManager()'

itemTemplate = PodTemplateDescriptor('item', 'Délibération')
itemTemplate.podTemplate = '../../examples_fr/templates/deliberation.odt'
itemTemplate.podCondition = 'python:here.meta_type=="MeetingItem"'

itemTemplatePDF = PodTemplateDescriptor('itempdf', 'Délibération')
itemTemplatePDF.podTemplate = '../../examples_fr/templates/deliberation.odt'
itemTemplatePDF.podFormat = 'pdf'
itemTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem"'

allTemplates = [agendaTemplate, agendaTemplatePDF,
                decisionsTemplate, decisionsTemplatePDF,
                itemTemplate, itemTemplatePDF]

# Users and groups -------------------------------------------------------------
president = UserDescriptor('president', [], email="test@test.be", fullname="Président")
secretaire = UserDescriptor('secretaire', [], email="test@test.be")
agentInfo = UserDescriptor('agentInfo', [], email="test@test.be")
agentCompta = UserDescriptor('agentCompta', [], email="test@test.be")
agentPers = UserDescriptor('agentPers', [], email="test@test.be")
agentIsp = UserDescriptor('agentIsp', [], email="test@test.be")
chefPers = UserDescriptor('chefPers', [], email="test@test.be")
chefCompta = UserDescriptor('chefCompta', [], email="test@test.be")
echevinPers = UserDescriptor('echevinPers', [], email="test@test.be")
emetteuravisPers = UserDescriptor('emetteuravisPers', [], email="test@test.be")
conseiller = UserDescriptor('conseiller', [], email="test@test.be", fullname="Conseiller")

groups = [GroupDescriptor('admingen', 'Administration générale', 'AdminGen'),
          GroupDescriptor('aidefamilles', 'Aide aux familles', 'Aide'),
          GroupDescriptor('comptabilite', 'Comptabilité', 'Compta'),
          GroupDescriptor('informatique', 'Informatique', 'Info'),
          GroupDescriptor('isp', 'Insertion socio-professionnelle', 'ISP'),
          GroupDescriptor('dettes', 'Médiation de dettes', 'Dettes'),
          GroupDescriptor('personnel', 'Personnel', 'Pers'),
          GroupDescriptor('social', 'Social', 'Soc'),
          GroupDescriptor('divers', 'Divers', 'Divers'), ]
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
bpMeeting.signatures = 'Pierre Dupont,\nBourgmestre\nCharles Exemple,\n1er Echevin'
bpMeeting.categories = categories
bpMeeting.shortName = 'bp'
bpMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier,
                              annexeDecision, annexeAvis, annexeAvisLegal]
bpMeeting.usedItemAttributes = ['budgetInfos', 'observations', ]
bpMeeting.usedMeetingAttributes = ['assembly', 'signatures', 'observations', 'place', ]
bpMeeting.itemWorkflow = 'meetingitemcollege_workflow'
bpMeeting.meetingWorkflow = 'meetingcollege_workflow'
bpMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
bpMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
bpMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
bpMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
bpMeeting.transitionsToConfirm = []
bpMeeting.meetingTopicStates = ('created', 'frozen')
bpMeeting.decisionTopicStates = ('decided', 'closed')
bpMeeting.itemAdviceStates = ('validated',)
bpMeeting.enforceAdviceMandatoriness = False
bpMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                        'reverse': '0'}, )
bpMeeting.recordItemHistoryStates = []
bpMeeting.maxShownMeetings = 5
bpMeeting.maxDaysDecisions = 60
bpMeeting.meetingAppDefaultView = 'topic_searchmyitems'
bpMeeting.useAdvices = True
bpMeeting.itemAdviceStates = ('validated',)
bpMeeting.itemAdviceEditStates = ('validated',)
bpMeeting.itemAdviceViewStates = ('validated', 'presented', 'itemfrozen', 'accepted',
                                  'refused', 'accepted_but_modified', 'delayed', 'pre_accepted',)
bpMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
bpMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
bpMeeting.useCopies = True
bpMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                  groups[1].getIdSuffixed('reviewers'),
                                  groups[2].getIdSuffixed('reviewers'),
                                  groups[4].getIdSuffixed('reviewers')]
bpMeeting.podTemplates = allTemplates
bpMeeting.meetingConfigsToCloneTo = [{'meeting_config': 'meeting-config-cas',
                                      'trigger_workflow_transitions_until': '__nothing__'}, ]

bpMeeting.recurringItems = [
    # Agenda items
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance antérieure',
        description='Approuve le procès-verbal de la séance antérieure',
        category='recurrents',
        proposingGroup='admingen',
        decision='Procès-verbal approuvé'), ]

# CAS
casMeeting = MeetingConfigDescriptor(
    'meeting-config-cas', "Conseil de l'Action Sociale",
    "Conseil de l'Action Sociale", isDefault=False)
casMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                      'Charles Exemple - 1er Echevin,\n' \
                      'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                      'Jacqueline Exemple, Responsable du CPAS'
casMeeting.signatures = 'Pierre Dupont,\nBourgmestre\nCharles Exemple,\n1er Echevin'
casMeeting.categories = categories
casMeeting.shortName = 'cas'
casMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier,
                               annexeDecision, annexeAvis, annexeAvisLegal]
casMeeting.usedItemAttributes = ['budgetInfos', 'observations', ]
casMeeting.usedMeetingAttributes = ['assembly', 'signatures', 'observations', 'place', ]
casMeeting.itemWorkflow = 'meetingitemcollege_workflow'
casMeeting.meetingWorkflow = 'meetingcollege_workflow'
casMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
casMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
casMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
casMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
casMeeting.transitionsToConfirm = []
casMeeting.meetingTopicStates = ('created', 'frozen')
casMeeting.decisionTopicStates = ('decided', 'closed')
casMeeting.itemAdviceStates = ('validated',)
casMeeting.enforceAdviceMandatoriness = False
casMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                         'reverse': '0'}, )
casMeeting.recordItemHistoryStates = []
casMeeting.maxShownMeetings = 5
casMeeting.maxDaysDecisions = 60
casMeeting.meetingAppDefaultView = 'topic_searchmyitems'
casMeeting.useAdvices = True
casMeeting.itemAdviceStates = ('validated',)
casMeeting.itemAdviceEditStates = ('validated',)
casMeeting.itemAdviceViewStates = ('validated', 'presented', 'itemfrozen', 'accepted',
                                   'refused', 'accepted_but_modified', 'delayed', 'pre_accepted',)
casMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
casMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
casMeeting.useCopies = True
casMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                   groups[1].getIdSuffixed('reviewers'),
                                   groups[2].getIdSuffixed('reviewers'),
                                   groups[4].getIdSuffixed('reviewers')]
casMeeting.podTemplates = allTemplates

casMeeting.recurringItems = [
    # Agenda items
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance antérieure',
        description='Approuve le procès-verbal de la séance antérieure',
        category='recurrents',
        proposingGroup='admingen',
        decision='Procès-verbal approuvé'), ]

# Comitee
comiteeMeeting = MeetingConfigDescriptor(
    'meeting-config-comitee', 'Comité de concertation Commune/CPAS',
    'Comité de concertation Commune/CPAS', isDefault=False)
comiteeMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                          'Charles Exemple - 1er Echevin,\n' \
                          'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                          'Jacqueline Exemple, Responsable du CPAS'
comiteeMeeting.signatures = 'Pierre Dupont,\nBourgmestre\nCharles Exemple,\n1er Echevin'
comiteeMeeting.categories = categories
comiteeMeeting.shortName = 'comitee'
comiteeMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier,
                                   annexeDecision, annexeAvis, annexeAvisLegal]
comiteeMeeting.usedItemAttributes = ['budgetInfos', 'observations', ]
comiteeMeeting.usedMeetingAttributes = ['assembly', 'signatures', 'observations', 'place', ]
comiteeMeeting.itemWorkflow = 'meetingitemcollege_workflow'
comiteeMeeting.meetingWorkflow = 'meetingcollege_workflow'
comiteeMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
comiteeMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
comiteeMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
comiteeMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
comiteeMeeting.transitionsToConfirm = []
comiteeMeeting.meetingTopicStates = ('created', 'frozen')
comiteeMeeting.decisionTopicStates = ('decided', 'closed')
comiteeMeeting.itemAdviceStates = ('validated',)
comiteeMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
comiteeMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
comiteeMeeting.enforceAdviceMandatoriness = False
comiteeMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                             'reverse': '0'}, )
comiteeMeeting.recordItemHistoryStates = []
comiteeMeeting.maxShownMeetings = 5
comiteeMeeting.maxDaysDecisions = 60
comiteeMeeting.meetingAppDefaultView = 'topic_searchmyitems'
comiteeMeeting.itemDocFormats = ('odt', 'pdf')
comiteeMeeting.meetingDocFormats = ('odt', 'pdf')
comiteeMeeting.useAdvices = True
comiteeMeeting.itemAdviceStates = ('validated',)
comiteeMeeting.itemAdviceEditStates = ('validated',)
comiteeMeeting.itemAdviceViewStates = ('validated', 'presented', 'itemfrozen', 'accepted',
                                       'refused', 'accepted_but_modified', 'delayed', 'pre_accepted',)
comiteeMeeting.useCopies = True
comiteeMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                       groups[1].getIdSuffixed('reviewers'),
                                       groups[2].getIdSuffixed('reviewers'),
                                       groups[4].getIdSuffixed('reviewers')]
comiteeMeeting.podTemplates = allTemplates

comiteeMeeting.recurringItems = [
    # Agenda items
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance antérieure',
        description='Approuve le procès-verbal de la séance antérieure',
        category='recurrents',
        proposingGroup='admingen',
        decision='Procès-verbal approuvé'), ]

# global data
data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=(bpMeeting, casMeeting, comiteeMeeting,),
    groups=groups)
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
data.enableUserPreferences = False
data.usersOutsideGroups = [president, conseiller]
# ------------------------------------------------------------------------------
