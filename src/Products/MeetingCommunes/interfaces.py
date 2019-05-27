# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2007 by CommunesPlone
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from Products.PloneMeeting.content.advice import IMeetingAdviceWorkflowActions
from Products.PloneMeeting.content.advice import IMeetingAdviceWorkflowConditions
from Products.PloneMeeting.interfaces import IMeetingItemWorkflowConditions
from Products.PloneMeeting.interfaces import IMeetingItemWorkflowActions
from Products.PloneMeeting.interfaces import IMeetingWorkflowActions
from Products.PloneMeeting.interfaces import IMeetingWorkflowConditions


class IMeetingCommunesWorkflowActions(IMeetingWorkflowActions):
    '''This interface represents a meeting as viewed by the specific meeting
       workflow that is defined in this MeetingCommunes product.'''
    def doDecide():
        """
          Triggered while doing the 'decide' transition
        """
    def doBackToPublished():
        """
          Triggered while going back to the 'published' state
        """


class IMeetingCommunesWorkflowConditions(IMeetingWorkflowConditions):
    '''This interface represents a meeting as viewed by the specific meeting
       workflow that is defined in this MeetingCommunes product.'''
    def mayDecide():
        """
          Guard for the 'decide' transition
        """


class IMeetingItemCommunesWorkflowActions(IMeetingItemWorkflowActions):
    '''This interface represents a meeting item as viewed by the specific
       item workflow that is defined in this MeetingCommunes product.'''
    def doAcceptButModify():
        """
          Triggered while doing the 'accept_but_modify' transition
        """
    def doPreAccept():
        """
          Triggered while doing the 'pre_accept' transition
        """


class IMeetingItemCommunesWorkflowConditions(IMeetingItemWorkflowConditions):
    '''This interface represents a meeting item as viewed by the specific
       meeting item workflow that is defined in this MeetingCommunes product.'''
    def mayDecide():
        """
          Guard for the 'decide' transition
        """
    def mayPublish():
        """
          Guard for the 'publish' transition
        """


class IMeetingAdviceCommunesWorkflowActions(IMeetingAdviceWorkflowActions):
    ''' '''


class IMeetingAdviceCommunesWorkflowConditions(IMeetingAdviceWorkflowConditions):
    ''' '''
