# -*- coding: utf-8 -*-

from copy import deepcopy

from Products.PloneMeeting.profiles.testing import import_data as pm_import_data


# Meeting configurations -------------------------------------------------------
# college

collegeMeeting = deepcopy(pm_import_data.meetingPma)
collegeMeeting.id = 'meeting-config-college'
collegeMeeting.Title = 'Collège Communal'
collegeMeeting.folderTitle = 'Collège Communal'
collegeMeeting.shortName = 'meeting-config-college'
collegeMeeting.id = 'meeting-config-college'
collegeMeeting.isDefault = True
collegeMeeting.shortName = 'College'
collegeMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
collegeMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
collegeMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
collegeMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
collegeMeeting.itemDecidedStates = ['accepted', 'delayed', 'accepted_but_modified', 'pre_accepted']
collegeMeeting.itemPositiveDecidedStates = ['accepted', 'accepted_but_modified']
collegeMeeting.workflowAdaptations = ['apply_item_validation_levels', 'delayed',
                                      'no_publication', 'no_global_observation',
                                      'pre_accepted', 'accepted_but_modified']
# Conseil communal
councilMeeting = deepcopy(pm_import_data.meetingPga)
councilMeeting.id = 'meeting-config-council'
councilMeeting.Title = 'Conseil Communal'
councilMeeting.folderTitle = 'Conseil Communal'
councilMeeting.shortName = 'meeting-config-council'
councilMeeting.id = 'meeting-config-council'
councilMeeting.isDefault = False
councilMeeting.shortName = 'Council'
councilMeeting.itemConditionsInterface = collegeMeeting.itemConditionsInterface
councilMeeting.itemActionsInterface = collegeMeeting.itemActionsInterface
councilMeeting.meetingConditionsInterface = collegeMeeting.meetingConditionsInterface
councilMeeting.meetingActionsInterface = collegeMeeting.meetingActionsInterface
councilMeeting.itemDecidedStates = collegeMeeting.itemDecidedStates
councilMeeting.itemPositiveDecidedStates = collegeMeeting.itemPositiveDecidedStates
councilMeeting.podTemplates = []

data = deepcopy(pm_import_data.data)
data.meetingFolderTitle = 'Mes séances'
data.meetingConfigs = (collegeMeeting, councilMeeting)
