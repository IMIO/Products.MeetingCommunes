# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.simple import import_data as simple_import_data
from Products.PloneMeeting.profiles import PloneMeetingConfiguration


config = deepcopy(simple_import_data.simpleMeeting)
config.id = 'bdc'
config.title = "Bons de commande"
config.folderTitle = "Bons de commande"
config.shortName = 'BDC'
config.workflowAdaptations = [
    'no_publication', 'refused', 'accepted_but_modified', 'delayed',
    'return_to_proposing_group', 'only_creator_may_delete', 'pre_accepted',
    'accepted_out_of_meeting']
data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=(config, ),
    orgs=[])
