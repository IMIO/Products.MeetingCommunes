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
# College
collegeMeeting = deepcopy(examples_fr_import_data.collegeMeeting)
collegeMeeting.id = 'meeting-config-zcollege'
collegeMeeting.title = 'Collège'
collegeMeeting.folderTitle = 'Collège'
collegeMeeting.shortName = 'ZCollege'
collegeMeeting.assembly = ''
collegeMeeting.signatures = ''
collegeMeeting.selectableAdvisers = []
collegeMeeting.meetingConfigsToCloneTo = [{'meeting_config': 'cfg2',
                                           'trigger_workflow_transitions_until': '__nothing__'}, ]
collegeMeeting.addContactsCSV = False
# use template file from profile examples_fr
patch_pod_templates(collegeMeeting.podTemplates, '../../examples_fr/templates/')

# Council
councilMeeting = deepcopy(examples_fr_import_data.councilMeeting)
councilMeeting.id = 'meeting-config-zcouncil'
councilMeeting.title = "Conseil"
councilMeeting.folderTitle = "Conseil"
councilMeeting.shortName = 'ZCouncil'
councilMeeting.assembly = ''
councilMeeting.signatures = ''
councilMeeting.selectableAdvisers = []
councilMeeting.meetingConfigsToCloneTo = []
patch_pod_templates(councilMeeting.podTemplates, '../../examples_fr/templates/', collegeMeeting.id)

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=(collegeMeeting, councilMeeting, ),
    orgs=examples_fr_import_data.groups)
data.usersOutsideGroups = [president, conseiller]
