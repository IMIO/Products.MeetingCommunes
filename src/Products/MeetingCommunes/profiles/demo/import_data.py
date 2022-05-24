# -*- coding: utf-8 -*-
#
# File: import_data.py
#
# GNU General Public License (GPL)
#
from copy import deepcopy
from datetime import datetime

from Products.MeetingCommunes.profiles.examples_fr.import_data import data as examples_fr_data
from Products.PloneMeeting.profiles import MeetingDescriptor, ItemDescriptor

data = deepcopy(examples_fr_data)

collegeMeeting, councilMeeting = data.meetingConfigs

collegeMeeting.meetings = (
    MeetingDescriptor(
        date=datetime(2050, 1, 12, 10, 30),
        items=[
            ItemDescriptor(
                u'Achat nouveaux serveurs',
                'agentInfo',
                itemTemplate='template5'
            ),
            ItemDescriptor(
                u'Marché public, contestation entreprise Untelle SA',
                'agentInfo',
                itemTemplate='template5'
            ),
        ],
        to_state='frozen'
    ),
)
collegeMeeting.items = []
