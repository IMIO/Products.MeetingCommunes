# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import OrgDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import UserDescriptor

today = DateTime().strftime('%Y/%m/%d')

# File types -------------------------------------------------------------------
annexe = ItemAnnexTypeDescriptor('annexe', 'Annexe', u'attach.png')
annexeBudget = ItemAnnexTypeDescriptor('annexeBudget', 'Article Budgétaire', u'budget.png')
annexeCahier = ItemAnnexTypeDescriptor('annexeCahier', 'Cahier des Charges', u'cahier.png')
annexeDecision = ItemAnnexTypeDescriptor('annexeDecision', 'Annexe à la décision',
                                         u'attach.png', relatedTo='item_decision')
annexeAvis = AnnexTypeDescriptor('annexeAvis', 'Annexe à un avis',
                                 u'attach.png', relatedTo='advice')
annexeAvisLegal = AnnexTypeDescriptor('annexeAvisLegal', 'Extrait article de loi',
                                      u'legalAdvice.png', relatedTo='advice')
annexeSeance = AnnexTypeDescriptor('annexe', 'Annexe',
                                   u'attach.png', relatedTo='meeting')

# Categories -------------------------------------------------------------------
recurring = CategoryDescriptor('recurrents', 'Récurrents')
categories = [recurring,
              CategoryDescriptor('casernes', 'Casernes'),
              CategoryDescriptor('divers', 'Divers'),
              ]

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplate.odt_file = 'oj.odt'
agendaTemplate.pod_formats = ['odt', 'pdf', ]
agendaTemplate.pod_portal_types = ['Meeting']
agendaTemplate.tal_condition = u'python:tool.isManager(here)'

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = 'pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['Meeting']
decisionsTemplate.tal_condition = u'python:tool.isManager(here)'

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.odt_file = 'deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItem']

dashboardTemplate = PodTemplateDescriptor('recapitulatif', 'Récapitulatif', dashboard=True)
dashboardTemplate.odt_file = 'recapitulatif-tb.odt'
dashboardTemplate.tal_condition = u'python: context.absolute_url().endswith("/searches_items")'

dashboardTemplateOds = PodTemplateDescriptor('recapitulatifods', 'Récapitulatif', dashboard=True)
dashboardTemplateOds.odt_file = 'recapitulatif-tb.ods'
dashboardTemplateOds.pod_formats = ['ods', 'xls', ]
dashboardTemplateOds.tal_condition = u'python: context.absolute_url().endswith("/searches_items")'

historyTemplate = PodTemplateDescriptor('historique', 'Historique')
historyTemplate.odt_file = 'history.odt'
historyTemplate.pod_formats = ['odt', 'pdf', ]
historyTemplate.pod_portal_types = ['MeetingItem']

collegeTemplates = [agendaTemplate, decisionsTemplate,
                    itemTemplate, dashboardTemplate,
                    dashboardTemplateOds, historyTemplate]

# Pod templates ----------------------------------------------------------------
agendaCouncilTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaCouncilTemplate.odt_file = 'council-oj.odt'
agendaCouncilTemplate.pod_formats = ['odt', 'pdf', ]
agendaCouncilTemplate.pod_portal_types = ['Meeting']
agendaCouncilTemplate.tal_condition = u'python:tool.isManager(here)'

decisionsCouncilTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsCouncilTemplate.odt_file = 'council-pv.odt'
decisionsCouncilTemplate.pod_formats = ['odt', 'pdf', ]
decisionsCouncilTemplate.pod_portal_types = ['Meeting']
decisionsCouncilTemplate.tal_condition = u'python:tool.isManager(here)'

itemCouncilRapportTemplate = PodTemplateDescriptor('rapport', 'Rapport')
itemCouncilRapportTemplate.odt_file = 'council-rapport.odt'
itemCouncilRapportTemplate.pod_formats = ['odt', 'pdf', ]
itemCouncilRapportTemplate.pod_portal_types = ['MeetingItem']
itemCouncilRapportTemplate.tal_condition = u''

itemCouncilTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemCouncilTemplate.odt_file = 'deliberation.odt'
itemCouncilTemplate.pod_formats = ['odt', 'pdf', ]
itemCouncilTemplate.pod_portal_types = ['MeetingItem']

councilTemplates = [agendaCouncilTemplate, decisionsCouncilTemplate,
                    itemCouncilRapportTemplate, itemCouncilTemplate,
                    dashboardTemplate]

# Users and groups -------------------------------------------------------------
dgen = UserDescriptor('dgen', [], email="test@test.be", fullname="Henry Directeur")
bourgmestre = UserDescriptor('bourgmestre', [], email="test@test.be", fullname="Pierre Bourgmestre")
dfin = UserDescriptor('dfin', [], email="test@test.be", fullname="Directeur Financier")
agentInfo = UserDescriptor('agentInfo', [], email="test@test.be", fullname="Agent Service Informatique")
agentCompta = UserDescriptor('agentCompta', [], email="test@test.be", fullname="Agent Service Comptabilité")
agentPers = UserDescriptor('agentPers', [], email="test@test.be", fullname="Agent Service du Personnel")
agentTrav = UserDescriptor('agentTrav', [], email="test@test.be", fullname="Agent Travaux")
chefPers = UserDescriptor('chefPers', [], email="test@test.be", fullname="Chef Personnel")
chefCompta = UserDescriptor('chefCompta', [], email="test@test.be", fullname="Chef Comptabilité")
echevinPers = UserDescriptor('echevinPers', [], email="test@test.be", fullname="Echevin du Personnel")
echevinTrav = UserDescriptor('echevinTrav', [], email="test@test.be", fullname="Echevin des Travaux")
conseiller = UserDescriptor('conseiller', [], email="test@test.be", fullname="Conseiller")

emetteuravisPers = UserDescriptor('emetteuravisPers', [], email="test@test.be", fullname="Emetteur avis Personnel")

groups = [OrgDescriptor('commandant', 'Commandant de zone', u'CdZ'),
          OrgDescriptor('secretariat', 'Secrétariat de zone', u'Secr'),
          OrgDescriptor('informatique', 'Service informatique', u'Info'),
          OrgDescriptor('personnel', 'Service du personnel', u'Pers'),
          OrgDescriptor('dirfin', 'Directeur Financier', u'DF'),
          OrgDescriptor('finances', 'Service finances', u'Fin'),
          OrgDescriptor('travaux', 'Service travaux', u'Trav'), ]

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
groups[3].observers.append(echevinPers)
groups[3].advisers.append(emetteuravisPers)

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

groups[6].creators.append(agentTrav)
groups[6].creators.append(dgen)
groups[6].reviewers.append(agentTrav)
groups[6].reviewers.append(dgen)
groups[6].observers.append(agentTrav)
groups[6].observers.append(echevinTrav)
groups[6].advisers.append(agentTrav)

# Meeting configurations -------------------------------------------------------
# college
collegeMeeting = MeetingConfigDescriptor(
    'meeting-config-zcollege', 'Collège',
    'Collège', isDefault=True)
collegeMeeting.meetingManagers = ['dgen', ]
collegeMeeting.assembly = 'Marie Curie - Présidente,\n' \
                          'Isaac Newton(ville de Physique),\n' \
                          'Pythagore (ville de Mathématiques),\n' \
                          'Louis Pasteur (ville de Chimie), Bourgmestres\n' \
                          'Archimède, Secrétaire du Collège,\n' \
                          'Albert Einstein, Commandant de zone'
collegeMeeting.signatures = 'Le Commandant de zone\nAlbert Einstein\nLa présidente\nMarie Curie'
collegeMeeting.certifiedSignatures = [
    {'signatureNumber': '1',
     'name': u'Marie Curie',
     'function': u'Présidente',
     'date_from': '',
     'date_to': '',
     },
    {'signatureNumber': '2',
     'name': u'Albert Einstein',
     'function': u'Le Commandant de zone',
     'date_from': '',
     'date_to': '',
     },
]
collegeMeeting.places = """Place1\r
Place2\r
Place3\r"""
collegeMeeting.categories = categories
collegeMeeting.shortName = 'ZCollege'
collegeMeeting.annexTypes = [annexe, annexeBudget, annexeCahier,
                             annexeDecision, annexeAvis, annexeAvisLegal, annexeSeance]
collegeMeeting.usedItemAttributes = ['description',
                                     'detailedDescription',
                                     'budgetInfos',
                                     'observations',
                                     'toDiscuss',
                                     'itemIsSigned',
                                     'notes',
                                     'inAndOutMoves']
collegeMeeting.usedMeetingAttributes = ['startDate',
                                        'endDate',
                                        'signatures',
                                        'assembly',
                                        'place',
                                        'observations',
                                        'notes',
                                        'inAndOutMoves']
collegeMeeting.recordMeetingHistoryStates = []
collegeMeeting.itemColumns = ['Creator', 'CreationDate', 'ModificationDate', 'review_state',
                              'getProposingGroup', 'advices', 'linkedMeetingDate',
                              'getItemIsSigned', 'actions']
collegeMeeting.itemsListVisibleColumns = ['Creator', 'CreationDate', 'review_state',
                                          'getProposingGroup', 'advices', 'actions']
collegeMeeting.xhtmlTransformFields = ('MeetingItem.description',
                                       'MeetingItem.detailedDescription',
                                       'MeetingItem.decision',
                                       'MeetingItem.observations',
                                       'Meeting.observations', )
collegeMeeting.xhtmlTransformTypes = ('removeBlanks',)
collegeMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
collegeMeeting.meetingWorkflow = 'meetingcommunes_workflow'
collegeMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
collegeMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
collegeMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
collegeMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
collegeMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
collegeMeeting.meetingTopicStates = ('created', 'frozen')
collegeMeeting.decisionTopicStates = ('decided', 'closed')
collegeMeeting.enforceAdviceMandatoriness = False
collegeMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                             'reverse': '0'}, )
collegeMeeting.recordItemHistoryStates = []
collegeMeeting.maxShownMeetings = 5
collegeMeeting.maxDaysDecisions = 60
collegeMeeting.meetingAppDefaultView = 'searchmyitems'
collegeMeeting.useAdvices = True
collegeMeeting.selectableAdvisers = []
collegeMeeting.itemAdviceStates = ('validated',)
collegeMeeting.itemAdviceEditStates = ('validated',)
collegeMeeting.itemAdviceViewStates = ('validated',
                                       'presented',
                                       'itemfrozen',
                                       'accepted',
                                       'refused',
                                       'accepted_but_modified',
                                       'delayed',
                                       'pre_accepted',)
collegeMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
collegeMeeting.enableAdviceInvalidation = False
collegeMeeting.itemAdviceInvalidateStates = []
collegeMeeting.customAdvisers = []
collegeMeeting.itemPowerObserversStates = ('itemfrozen',
                                           'accepted',
                                           'delayed',
                                           'refused',
                                           'accepted_but_modified',
                                           'pre_accepted')
collegeMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
collegeMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group', 'refused']
collegeMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
collegeMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Collège décide de reporter le point.</p>${here/getDecision}"},))
collegeMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
collegeMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
collegeMeeting.powerAdvisersGroups = ()
collegeMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
collegeMeeting.useCopies = True
collegeMeeting.selectableCopyGroups = []
collegeMeeting.podTemplates = collegeTemplates
collegeMeeting.meetingConfigsToCloneTo = [{'meeting_config': 'meeting-config-zcouncil',
                                           'trigger_workflow_transitions_until': '__nothing__'}, ]
collegeMeeting.itemAutoSentToOtherMCStates = ('accepted', 'accepted_but_modified', )
collegeMeeting.recurringItems = []
collegeMeeting.itemTemplates = []

# Conseil
councilMeeting = MeetingConfigDescriptor(
    'meeting-config-zcouncil', 'Conseil',
    'Conseil')
councilMeeting.meetingManagers = ['dgen', ]
councilMeeting.assembly = 'Marie Curie - Présidente,\n' \
                          'Isaac Newton(ville de Physique),\n' \
                          'Pythagore (ville de Mathématiques),\n' \
                          'Louis Pasteur (ville de Chimie), Bourgmestres\n' \
                          'Archimède, Secrétaire du Collège,\n' \
                          'Albert Einstein, Commandant de zone'
councilMeeting.signatures = 'Le Commandant de zone\nAlbert Einstein\nLa présidente\nMarie Curie'
councilMeeting.certifiedSignatures = [
    {'signatureNumber': '1',
     'name': u'Marie Curie',
     'function': u'Présidente',
     'date_from': '',
     'date_to': '',
     },
    {'signatureNumber': '2',
     'name': u'Albert Einstein',
     'function': u'Le Commandant de zone',
     'date_from': '',
     'date_to': '',
     },
]
councilMeeting.places = """Place1\n\r
Place2\n\r
Place3\n\r"""
councilMeeting.categories = categories
councilMeeting.shortName = 'ZCouncil'
councilMeeting.annexTypes = [annexe, annexeBudget, annexeCahier,
                             annexeDecision, annexeAvis, annexeAvisLegal, annexeSeance]
councilMeeting.usedItemAttributes = ['detailedDescription',
                                     'oralQuestion',
                                     'itemInitiator',
                                     'observations',
                                     'privacy',
                                     'notes',
                                     'inAndOutMoves']
councilMeeting.usedMeetingAttributes = ['startDate',
                                        'midDate',
                                        'endDate',
                                        'signatures',
                                        'assembly',
                                        'place',
                                        'observations',
                                        'notes',
                                        'inAndOutMoves']
councilMeeting.recordMeetingHistoryStates = []
councilMeeting.xhtmlTransformFields = ('MeetingItem.description',
                                       'MeetingItem.detailedDescription',
                                       'MeetingItem.decision',
                                       'MeetingItem.observations',
                                       'Meeting.observations', )
councilMeeting.xhtmlTransformTypes = ('removeBlanks',)
councilMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
councilMeeting.meetingWorkflow = 'meetingcommunes_workflow'
councilMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
councilMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
councilMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
councilMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
councilMeeting.transitionsToConfirm = []
councilMeeting.meetingTopicStates = ('created', 'frozen')
councilMeeting.decisionTopicStates = ('decided', 'closed')
councilMeeting.itemAdviceStates = ('validated',)
councilMeeting.enforceAdviceMandatoriness = False
councilMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                             'reverse': '0'}, )
councilMeeting.recordItemHistoryStates = []
councilMeeting.maxShownMeetings = 5
councilMeeting.maxDaysDecisions = 60
councilMeeting.meetingAppDefaultView = 'searchmyitems'
councilMeeting.itemDocFormats = ('odt', 'pdf')
councilMeeting.meetingDocFormats = ('odt', 'pdf')
councilMeeting.useAdvices = False
councilMeeting.itemAdviceStates = ()
councilMeeting.itemAdviceEditStates = ()
councilMeeting.itemAdviceViewStates = ()
councilMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
councilMeeting.workflowAdaptations = ['no_publication', 'no_global_observation', 'return_to_proposing_group', 'refused']
councilMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
councilMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
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
councilMeeting.itemPowerObserversStates = ('itemfrozen',
                                           'accepted', 'delayed',
                                           'refused',
                                           'accepted_but_modified', 'pre_accepted')
councilMeeting.meetingPowerObserversStates = ('frozen', 'decided', 'closed')
councilMeeting.powerAdvisersGroups = ()
councilMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
councilMeeting.useCopies = True
councilMeeting.selectableCopyGroups = []
councilMeeting.podTemplates = councilTemplates
councilMeeting.recurringItems = []
councilMeeting.itemTemplates = collegeMeeting.itemTemplates

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(collegeMeeting, councilMeeting),
                                 orgs=groups)
data.enableUserPreferences = False
data.usersOutsideGroups = [bourgmestre, conseiller]
# ------------------------------------------------------------------------------
