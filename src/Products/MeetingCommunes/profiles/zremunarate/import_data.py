# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.simple import import_data as simple_import_data
from Products.PloneMeeting.profiles import PloneMeetingConfiguration


config = deepcopy(simple_import_data.simpleMeeting)
config.id = 'remuneration'
config.title = 'Comité de rémunération'
config.folderTitle = 'Comité de rémunération'
config.shortName = 'Remun'

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=(config, ),
    orgs=[])
