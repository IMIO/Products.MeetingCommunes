# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import *

# File types -------------------------------------------------------------------
annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeBudget = MeetingFileTypeDescriptor('annexeBudget', 'Article Budgétaire', 'budget.png', '')
annexeCahier = MeetingFileTypeDescriptor('annexeCahier', 'Cahier des Charges', 'cahier.gif', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe à la décision', 'attach.png', '', True)
# Categories -------------------------------------------------------------------
recurring = CategoryDescriptor('recurrents', 'Récurrents')
categories = [recurring,
              CategoryDescriptor('travaux', 'Travaux'),
              CategoryDescriptor('urbanisme', 'Urbanisme'),
              CategoryDescriptor('comptabilite', 'Comptabilité/Recettes'),
              CategoryDescriptor('personnel', 'Personnel'),
              CategoryDescriptor('population', 'Population/Etat-civil'),
              CategoryDescriptor('locations', 'Locations'),
              CategoryDescriptor('divers', 'Divers'),
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
itemCouncilProjectTemplate.podTemplate = 'projet-deliberation.odt'
itemCouncilProjectTemplate.podCondition = 'python:here.meta_type=="MeetingItem" and not here.hasMeeting()'

itemCouncilProjectTemplatePDF = PodTemplateDescriptor('projet-deliberation-pdf', 'Projet délibération')
itemCouncilProjectTemplatePDF.podTemplate = 'projet-deliberation.odt'
itemCouncilProjectTemplatePDF.podFormat = 'pdf'
itemCouncilProjectTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem" and not here.hasMeeting()'

itemCouncilTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemCouncilTemplate.podTemplate = 'deliberation.odt'
itemCouncilTemplate.podCondition = 'python:here.meta_type=="MeetingItem" and here.hasMeeting()'

itemCouncilTemplatePDF = PodTemplateDescriptor('deliberation-pdf', 'Délibération')
itemCouncilTemplatePDF.podTemplate = 'deliberation.odt'
itemCouncilTemplatePDF.podFormat = 'pdf'
itemCouncilTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem" and here.hasMeeting()'

councilTemplates = [agendaCouncilTemplate, agendaCouncilTemplatePDF,
                    decisionsCouncilTemplate, decisionsCouncilTemplatePDF,
                    itemCouncilRapportTemplate, itemCouncilRapportTemplatePDF,
                    itemCouncilTemplate, itemCouncilTemplatePDF,
                    itemCouncilProjectTemplate, itemCouncilProjectTemplatePDF, ]

# Users and groups -------------------------------------------------------------
secretaire = UserDescriptor('secretaire', ['MeetingManager'], email="test@test.be", fullname="Henry Secrétaire")
bourgmestre = UserDescriptor('bourgmestre', [], email="test@test.be", fullname="Pierre Bourgmestre")
receveur = UserDescriptor('receveur', [], email="test@test.be", fullname="Receveur communal")
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

groups = [
           GroupDescriptor('secretariat', 'Secretariat communal', 'Secr'),
           GroupDescriptor('informatique', 'Service informatique', 'Info'),
           GroupDescriptor('personnel', 'Service du personnel', 'Pers'),
           GroupDescriptor('comptabilite', 'Service comptabilité', 'Compt', givesMandatoryAdviceOn='python:True'),
           GroupDescriptor('travaux', 'Service travaux', 'Trav'),
         ]

# MeetingManager
groups[0].creators.append(secretaire)
groups[0].reviewers.append(secretaire)
groups[0].observers.append(secretaire)
groups[0].advisers.append(secretaire)

groups[1].creators.append(agentInfo)
groups[1].creators.append(secretaire)
groups[1].reviewers.append(agentInfo)
groups[1].reviewers.append(secretaire)
groups[1].observers.append(agentInfo)
groups[1].advisers.append(agentInfo)

groups[2].creators.append(agentPers)
groups[2].observers.append(agentPers)
groups[2].creators.append(secretaire)
groups[2].reviewers.append(secretaire)
groups[2].creators.append(chefPers)
groups[2].reviewers.append(chefPers)
groups[2].observers.append(chefPers)
groups[2].observers.append(echevinPers)
groups[2].observers.append(receveur)
groups[2].advisers.append(emetteuravisPers)

groups[3].creators.append(agentCompta)
groups[3].creators.append(chefCompta)
groups[3].creators.append(secretaire)
groups[3].reviewers.append(chefCompta)
groups[3].reviewers.append(secretaire)
groups[3].observers.append(agentCompta)
groups[3].advisers.append(chefCompta)

groups[4].creators.append(agentTrav)
groups[4].creators.append(secretaire)
groups[4].reviewers.append(agentTrav)
groups[4].reviewers.append(secretaire)
groups[4].observers.append(agentTrav)
groups[4].observers.append(echevinTrav)
groups[4].advisers.append(agentTrav)

# Meeting configurations -------------------------------------------------------
# college
collegeMeeting = MeetingConfigDescriptor(
    'meeting-config-college', 'Collège Communal',
    'Collège communal', isDefault=True)
collegeMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                           'Charles Exemple - 1er Echevin,\n' \
                           'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                           'Jacqueline Exemple, Responsable du CPAS'
collegeMeeting.signatures = 'Le Secrétaire communal\nPierre Dupont\nLe Bourgmestre\nCharles Exemple'
collegeMeeting.certifiedSignatures = 'Le Secrétaire communal\nVraiment Présent\nLe Bourgmestre\nCharles Exemple'
collegeMeeting.places = """Place1\r
Place2\r
Place3\r"""
collegeMeeting.categories = categories
collegeMeeting.shortName = 'College'
collegeMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, annexeDecision]
collegeMeeting.usedItemAttributes = ['detailedDescription',
                                     'budgetInfos',
                                     'observations',
                                     'toDiscuss',
                                     'itemAssembly',
                                     'itemIsSigned', ]
collegeMeeting.usedMeetingAttributes = ['startDate', 'endDate', 'signatures', 'assembly', 'place', 'observations', ]
collegeMeeting.recordMeetingHistoryStates = []
collegeMeeting.itemsListVisibleColumns = ['toDiscuss',
                                          'state',
                                          'proposingGroup',
                                          'annexes',
                                          'annexesDecision',
                                          'advices',
                                          'actions',
                                          'itemIsSigned', ]
collegeMeeting.itemColumns = ['creator',
                              'state',
                              'proposingGroup',
                              'annexes',
                              'annexesDecision',
                              'advices',
                              'actions',
                              'meeting',
                              'itemIsSigned', ]
collegeMeeting.xhtmlTransformFields = ('MeetingItem.description',
                                       'MeetingItem.detailedDescription',
                                       'MeetingItem.decision',
                                       'MeetingItem.observations',
                                       'Meeting.observations', )
collegeMeeting.xhtmlTransformTypes = ('removeBlanks',)
collegeMeeting.itemWorkflow = 'meetingitemcollege_workflow'
collegeMeeting.meetingWorkflow = 'meetingcollege_workflow'
collegeMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowConditions'
collegeMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCollegeWorkflowActions'
collegeMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowConditions'
collegeMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCollegeWorkflowActions'
collegeMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
collegeMeeting.itemTopicStates = ('itemcreated',
                                  'proposed',
                                  'validated',
                                  'presented',
                                  'itemfrozen',
                                  'pre_accepted',
                                  'accepted',
                                  'refused',
                                  'delayed',
                                  'accepted_but_modified', )
collegeMeeting.meetingTopicStates = ('created', 'frozen')
collegeMeeting.decisionTopicStates = ('decided', 'closed')
collegeMeeting.enforceAdviceMandatoriness = False
collegeMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
collegeMeeting.recordItemHistoryStates = []
collegeMeeting.maxShownMeetings = 5
collegeMeeting.maxDaysDecisions = 60
collegeMeeting.meetingAppDefaultView = 'topic_searchmyitems'
collegeMeeting.itemDocFormats = ('odt', 'pdf')
collegeMeeting.meetingDocFormats = ('odt', 'pdf')
collegeMeeting.useAdvices = True
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
collegeMeeting.itemPowerObserversStates = ('itemfrozen', 'accepted', 'delayed', 'refused', 'accepted_but_modified')
collegeMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified','pre_accepted']
collegeMeeting.meetingPowerObserversStates = ('created', 'frozen', 'decided', 'closed')
collegeMeeting.useCopies = True
collegeMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                       groups[1].getIdSuffixed('reviewers'),
                                       groups[2].getIdSuffixed('reviewers'),
                                       groups[4].getIdSuffixed('reviewers')]
collegeMeeting.podTemplates = collegeTemplates

collegeMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance antérieure',
        description='Approuve le procès-verbal de la séance antérieure',
        category='recurrents',
        proposingGroup='secretariat',
        decision='Procès-verbal approuvé'),
    RecurringItemDescriptor(
        id='recurringofficialreport1',
        title='Autorise et signe les bons de commande de la semaine',
        description='Autorise et signe les bons de commande de la semaine',
        category='recurrents',
        proposingGroup='secretariat',
        decision='Bons de commande signés'),
    RecurringItemDescriptor(
        id='recurringofficialreport2',
        title='Ordonnance et signe les mandats de paiement de la semaine',
        description='Ordonnance et signe les mandats de paiement de la semaine',
        category='recurrents',
        proposingGroup='secretariat',
        decision='Mandats de paiement de la semaine approuvés'),
    RecurringItemDescriptor(
        id='template1',
        title='Tutelle CPAS',
        description='Tutelle CPAS',
        category='personnel',
        proposingGroup='secretariat',
        templateUsingGroups=['secretariat',],
        usages=['as_template_item',],
        decision="""<p>Vu la loi du 8 juillet 1976 organique des centres publics d'action sociale et plus particulièrement son article 111;</p>
<p>Vu l'Arrêté du Gouvernement Wallon du 22 avril 2004 portant codification de la législation relative aux pouvoirs locaux tel que confirmé par le décret du 27 mai 2004 du Conseil régional wallon;</p>
<p>Attendu que les décisions suivantes du Bureau permanent/du Conseil de l'Action sociale du XXX ont été reçues le XXX dans le cadre de la tutelle générale sur les centres publics d'action sociale :</p>
<p>- ...;</p>
<p>- ...;</p>
<p>- ...</p>
<p>Attendu que ces décisions sont conformes à la loi et à l'intérêt général;</p>
<p>Déclare à l'unanimité que :</p>
<p><strong>Article 1er :</strong></p>
<p>Les décisions du Bureau permanent/Conseil de l'Action sociale visées ci-dessus sont conformes à la loi et à l'intérêt général et qu'il n'y a, dès lors, pas lieu de les annuler.</p>
<p><strong>Article 2 :</strong></p>
<p>Copie de la présente délibération sera transmise au Bureau permanent/Conseil de l'Action sociale.</p>"""),
    RecurringItemDescriptor(
        id='template2',
        title='Contrôle médical systématique agent contractuel',
        description='Contrôle médical systématique agent contractuel',
        category='personnel',
        proposingGroup='personnel',
        templateUsingGroups=['personnel',],
        usages=['as_template_item',],
        decision="""
            <p>Vu la loi du 26 mai 2002 instituant le droit à l’intégration sociale;</p>
<p>Vu la délibération du Conseil communal du 29 juin 2009 concernant le cahier spécial des charges relatif au marché de services portant sur le contrôle des agents communaux absents pour raisons médicales;</p>
<p>Vu sa délibération du 17 décembre 2009 désignant le docteur XXX en qualité d’adjudicataire pour la mission de contrôle médical des agents de l’Administration communale;</p>
<p>Vu également sa décision du 17 décembre 2009 d’opérer les contrôles médicaux de manière systématique et pour une période d’essai d’un trimestre;</p>
<p>Attendu qu’un certificat médical a été  reçu le XXX concernant XXX la couvrant du XXX au XXX, avec la mention « XXX »;</p>
<p>Attendu que le Docteur XXX a transmis au service du Personnel, par fax, le même jour à XXX le rapport de contrôle mentionnant l’absence de XXX ce XXX à XXX;</p>
<p>Considérant que XXX avait été informée par le Service du Personnel de la mise en route du système de contrôle systématique que le médecin-contrôleur;</p>
<p>Considérant qu’ayant été absent(e) pour maladie la semaine précédente elle avait reçu la visite du médecin-contrôleur;</p>
<p>DECIDE :</p>
<p><strong>Article 1</strong> : De convoquer XXX devant  Monsieur le Secrétaire communal f.f. afin de lui rappeler ses obligations en la matière.</p>
<p><strong>Article 2</strong> :  De prévenir XXX, qu’en cas de récidive, il sera proposé par le Secrétaire communal au Collège de transformer les jours de congés de maladie en absence injustifiée (retenue sur traitement avec application de la loi du 26 mai 2002 citée ci-dessus).</p>
<p><strong>Article 3</strong> : De charger le service du personnel du suivi de ce dossier.</p>"""),
    RecurringItemDescriptor(
        id='template3',
        title='Engagement temporaire',
        description='Engagement temporaire',
        category='personnel',
        proposingGroup='personnel',
        templateUsingGroups=['personnel',],
        usages=['as_template_item',],
        decision="""<p>Considérant qu’il y a lieu de pourvoir au remplacement de Madame XXX, XXX bénéficiant d’une interruption de carrière pour convenances personnelles pour l’année scolaire 2009/2010. &nbsp;</p>
<p>Attendu qu’un appel public a été lancé au mois de mai dernier;</p>
<p>Vu la circulaire N° 2772 de la Communauté Française&nbsp;du 29 juin 2009 concernant &nbsp;la gestion des carrières administrative et pécuniaire dans l’enseignement fondamental ordinaire et principalement le chapitre 3 relatif aux engagements temporaires pendant l’année scolaire 2009/2010;</p>
<p>Vu la proposition du directeur concerné d’attribuer cet emploi à Monsieur XXX, titulaire des titres requis;</p>
<p>Vu le décret de la Communauté Française du 13 juillet 1998 portant restructuration de l’enseignement&nbsp;maternel et primaire ordinaires avec effet au 1er octobre 1998;</p>
<p>Vu la loi du 29 mai 1959 (Pacte scolaire) et les articles L1122-19 et L1213-1 du Code de la démocratie locale et de la décentralisation;</p>
<p>Vu l’avis favorable de l’Echevin de l’Enseignement;</p>
<p><b>DECIDE&nbsp;:</b><br>
<b><br> Article 1<sup>er</sup></b> :</p>
<p>Au scrutin secret et à l’unanimité, de désigner Monsieur XXX, né le XXX à XXX et domicilié à XXX, en qualité d’instituteur maternel temporaire mi-temps en remplacement de Madame XXX aux écoles communales fondamentales de Sambreville (section de XXX) du XXX au XXX.</p>
<p><b>Article 2</b> :</p>
<p>L’horaire hebdomadaire de l’intéressé est fixé à 13 périodes.</p>
<p><b>Article 3&nbsp;:</b></p>
<p>La présente délibération sera soumise à la ratification du Conseil Communal. Elle sera transmise au Bureau Régional de l’Enseignement primaire et maternel, à l’Inspectrice Cantonale et à la direction concernée.</p>"""),
    RecurringItemDescriptor(
        id='template4',
        title='Prestation réduite',
        description='Prestation réduite',
        category='personnel',
        proposingGroup='personnel',
        templateUsingGroups=['personnel',],
        usages=['as_template_item',],
        decision="""<p>Vu la loi de redressement du 22 janvier 1985 (article 99 et suivants) et de l’Arrêté Royal du 12 août 1991 (tel que modifié) relatifs à l’interruption de carrière professionnelle dans l’enseignement;</p>
<p>Vu la lettre du XXX par laquelle Madame XXX, institutrice maternelle, sollicite le renouvellement pendant l’année scolaire 2009/2010 de son congé pour prestations réduites mi-temps pour convenances personnelles dont elle bénéficie depuis le 01 septembre 2006;</p>
<p>Attendu que le remplacement de l’intéressée&nbsp;est assuré pour la prochaine rentrée scolaire;</p>
<p>Vu le décret de la Communauté Française du 13 juillet 1988 portant restructuration de l’enseignement maternel et primaire ordinaires avec effet au 1er octobre 1998;</p>
<p>Vu la loi du 29 mai 1959 (Pacte Scolaire) et les articles L1122-19 et L1213-1 du code de la démocratie locale et de la décentralisation;</p>
<p>Vu l’avis favorable de l’Echevin de l’Enseignement;</p>
<p><b>DECIDE&nbsp;:</b><br><b><br> Article 1<sup>er</sup></b>&nbsp;:</p>
<p>Au scrutin secret et à l’unanimité, d’accorder à Madame XXX le congé pour prestations réduites mi-temps sollicité pour convenances personnelles en qualité d’institutrice maternelle aux écoles communales fondamentales&nbsp;&nbsp;de Sambreville (section de XXX).</p>
<p><b>Article 2</b> :</p>
<p>Une activité lucrative est autorisée durant ce congé qui est assimilé à une période d’activité de service, dans le respect de la réglementation relative au cumul.</p>
<p><b>Article 3&nbsp;:</b></p>
<p>La présente délibération sera soumise pour accord au prochain Conseil, transmise au Bureau Régional de l’Enseignement primaire et maternel, à&nbsp;l’Inspectrice Cantonale, à la direction concernée et à l’intéressée.</p>"""),
    RecurringItemDescriptor(
        id='template5',
        title='Exemple modèle disponible pour tous',
        description='Exemple modèle disponible pour tous',
        category='personnel',
        proposingGroup='',
        templateUsingGroups=[],
        usages=['as_template_item',],
        decision="""<p>Vu la loi du XXX;</p>
<p>Vu ...;</p>
<p>Attendu que ...;</p>
<p>Vu le décret de la Communauté Française du ...;</p>
<p>Vu la loi du ...;</p>
<p>Vu l’avis favorable de ...;</p>
<p><b>DECIDE&nbsp;:</b><br><b><br> Article 1<sup>er</sup></b>&nbsp;:</p>
<p>...</p>
<p><b>Article 2</b> :</p>
<p>...</p>
<p><b>Article 3&nbsp;:</b></p>
<p>...</p>"""),
]

# Conseil communal
councilMeeting = MeetingConfigDescriptor(
    'meeting-config-council', 'Conseil Communal',
    'Conseil Communal')
councilMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                           'Charles Exemple - 1er Echevin,\n' \
                           'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                           'Jacqueline Exemple, Responsable du CPAS'
councilMeeting.signatures = 'Le Secrétaire communal\nPierre Dupont\nLe Bourgmestre\nCharles Exemple'
councilMeeting.certifiedSignatures = 'Le Secrétaire communal\nVraiment Présent\nLe Bourgmestre\nCharles Exemple'
councilMeeting.places = """Place1\n\r
Place2\n\r
Place3\n\r"""
councilMeeting.categories = categories
councilMeeting.shortName = 'Council'
councilMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, annexeDecision]
councilMeeting.usedItemAttributes = ['detailedDescription',
                                     'oralQuestion',
                                     'itemInitiator',
                                     'observations',
                                     'privacy',
                                     'itemAssembly', ]
councilMeeting.usedMeetingAttributes = ['startDate',
                                        'midDate',
                                        'endDate',
                                        'signatures',
                                        'assembly',
                                        'place',
                                        'observations', ]
councilMeeting.recordMeetingHistoryStates = []
councilMeeting.itemsListVisibleColumns = ['state', 'proposingGroup', 'annexes', 'annexesDecision', 'actions', ]
councilMeeting.itemColumns = ['creator',
                              'state',
                              'proposingGroup',
                              'annexes',
                              'annexesDecision',
                              'advices',
                              'actions',
                              'meeting', ]
councilMeeting.xhtmlTransformFields = ('MeetingItem.description',
                                       'MeetingItem.detailedDescription',
                                       'MeetingItem.decision',
                                       'MeetingItem.observations',
                                       'Meeting.observations', )
councilMeeting.xhtmlTransformTypes = ('removeBlanks',)
councilMeeting.itemWorkflow = 'meetingitemcouncil_workflow'
councilMeeting.meetingWorkflow = 'meetingcouncil_workflow'
councilMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCouncilWorkflowConditions'
councilMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCouncilWorkflowActions'
councilMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCouncilWorkflowConditions'
councilMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCouncilWorkflowActions'
councilMeeting.transitionsToConfirm = []
#show every items states
councilMeeting.itemTopicStates = ('itemcreated',
                                  'proposed',
                                  'validated',
                                  'presented',
                                  'itemfrozen',
                                  'itempublished',
                                  'accepted',
                                  'pre_accepted',
                                  'accepted_but_modified',
                                  'refused',
                                  'delayed')
councilMeeting.meetingTopicStates = ('created', 'frozen', 'published')
councilMeeting.decisionTopicStates = ('decided', 'closed')
councilMeeting.itemAdviceStates = ('validated',)
councilMeeting.enforceAdviceMandatoriness = False
councilMeeting.sortingMethodOnAddItem = 'on_proposing_groups'
councilMeeting.recordItemHistoryStates = []
councilMeeting.maxShownMeetings = 5
councilMeeting.maxDaysDecisions = 60
councilMeeting.meetingAppDefaultView = 'topic_searchmyitems'
councilMeeting.itemDocFormats = ('odt', 'pdf')
councilMeeting.meetingDocFormats = ('odt', 'pdf')
councilMeeting.useAdvices = False
councilMeeting.itemAdviceStates = ()
councilMeeting.itemAdviceEditStates = ()
councilMeeting.itemAdviceViewStates = ()
councilMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified','pre_accepted']
councilMeeting.itemPowerObserversStates = ('itemfrozen',
                                           'itempublished',
                                           'accepted', 'delayed',
                                           'refused',
                                           'accepted_but_modified')
councilMeeting.meetingPowerObserversStates = ('created', 'frozen', 'published', 'decided', 'closed')
councilMeeting.useCopies = True
councilMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                       groups[1].getIdSuffixed('reviewers'),
                                       groups[2].getIdSuffixed('reviewers'),
                                       groups[4].getIdSuffixed('reviewers')]
councilMeeting.podTemplates = councilTemplates

bourgmestre_mu = MeetingUserDescriptor('bourgmestre',
                                       duty='Bourgmestre',
                                       usages=['assemblyMember', 'signer', 'asker', ],
                                       signatureIsDefault=True)
receveur_mu = MeetingUserDescriptor('receveur',
                                    duty='Receveur communal',
                                    usages=['assemblyMember', 'signer', 'asker', ])
echevinPers_mu = MeetingUserDescriptor('echevinPers',
                                       duty='Echevin GRH',
                                       usages=['assemblyMember', 'asker', ])
echevinTrav_mu = MeetingUserDescriptor('echevinTrav',
                                       duty='Echevin Travaux',
                                       usages=['assemblyMember', 'asker', ])
secretaire_mu = MeetingUserDescriptor('secretaire',
                                      duty='Secrétaire communal',
                                      usages=['assemblyMember', 'signer', 'asker', ],
                                      signatureIsDefault=True)

councilMeeting.meetingUsers = [bourgmestre_mu, receveur_mu, echevinPers_mu, echevinTrav_mu, secretaire_mu]

councilMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance antérieure',
        description='Approuve le procès-verbal de la séance antérieure',
        category='recurrents',
        proposingGroup='secretariat',
        decision='Procès-verbal approuvé'),
    ]

data = PloneMeetingConfiguration(
           meetingFolderTitle='Mes séances',
           meetingConfigs=(collegeMeeting, councilMeeting),
           groups=groups)
data.unoEnabledPython = '/usr/bin/python'
data.usedColorSystem = 'state_color'
data.enableUserPreferences = False
data.usersOutsideGroups = [bourgmestre, conseiller]
# ------------------------------------------------------------------------------
