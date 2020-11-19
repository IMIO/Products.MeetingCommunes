# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.examples_fr import import_data as examples_fr_import_data
from Products.MeetingCommunes.profiles.examples_fr.import_data import conseiller
from Products.PloneMeeting.profiles import patch_pod_templates
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import UserDescriptor


# Users and groups -------------------------------------------------------------
president = UserDescriptor('president', [], email="test@test.be", fullname="Président")

# Meeting configurations -------------------------------------------------------
# BP
bpMeeting = deepcopy(examples_fr_import_data.collegeMeeting)
bpMeeting.id = 'meeting-config-bp'
bpMeeting.title = 'Bureau permanent'
bpMeeting.folderTitle = 'Bureau permanent'
bpMeeting.shortName = 'bp'
bpMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                     'Charles Exemple - 1er Echevin,\n' \
                     'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                     'Jacqueline Exemple, Responsable du CPAS'
bpMeeting.signatures = 'Pierre Dupont,\nPrésident\nCharles Exemple,\nDirecteur Général'
bpMeeting.selectableAdvisers = ['admingen', 'aidefamilles', 'comptabilite',
                                'informatique', 'isp', 'dettes', 'personnel',
                                'social', 'divers']
bpMeeting.meetingConfigsToCloneTo = [{'meeting_config': 'cfg2',
                                      'trigger_workflow_transitions_until': '__nothing__'}, ]
bpMeeting.addContactsCSV = False
# use template file from profile examples_fr
patch_pod_templates(bpMeeting.podTemplates, '../../examples_fr/templates/')

# CAS
casMeeting = deepcopy(examples_fr_import_data.councilMeeting)
casMeeting.id = 'meeting-config-cas'
casMeeting.title = "Conseil de l'Action Sociale"
casMeeting.folderTitle = "Conseil de l'Action Sociale"
casMeeting.shortName = 'cas'
casMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                      'Charles Exemple - 1er Echevin,\n' \
                      'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                      'Jacqueline Exemple, Responsable du CPAS'
casMeeting.signatures = 'Pierre Dupont,\nPrésident\nCharles Exemple,\nDirecteur Général'
casMeeting.meetingConfigsToCloneTo = []
# use template file from profile examples_fr
patch_pod_templates(casMeeting.podTemplates, '../../examples_fr/templates/', bpMeeting.id)

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=(bpMeeting, casMeeting, ),
    orgs=examples_fr_import_data.groups)
data.usersOutsideGroups = [president, conseiller]
data.directory_position_types = deepcopy(examples_fr_import_data.data.directory_position_types)
data.contactsTemplates = deepcopy(examples_fr_import_data.data.contactsTemplates)
