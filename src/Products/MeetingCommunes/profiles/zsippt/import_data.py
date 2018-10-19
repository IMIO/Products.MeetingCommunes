# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.simple import import_data as simple_import_data
from Products.PloneMeeting.profiles import PloneMeetingConfiguration


config = deepcopy(simple_import_data.simpleMeeting)
config.id = 'sippt'
config.title = 'SIPPT'
config.folderTitle = 'SIPPT'
config.shortName = 'Sippt'

data = PloneMeetingConfiguration(
    meetingFolderTitle='Mes séances',
    meetingConfigs=(config, ),
    orgs=[])
