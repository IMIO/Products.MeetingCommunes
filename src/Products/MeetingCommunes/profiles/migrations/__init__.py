# -*- coding: utf-8 -*-
# Copyright (c) 2008 by PloneGov
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

'''This module defines functions that allow to migrate to a given version of
   PloneMeeting for production sites that run older versions of PloneMeeting.
   You must run every migration function in the right chronological order.
   For example, if your production site runs a version of PloneMeeting as of
   2008_04_01, and two migration functions named
   migrateToPloneMeeting_2008_05_23 and migrateToPloneMeeting_2008_08_29 exist,
   you need to execute migrateToPloneMeeting_2008_05_23 first AND
   migrateToPloneMeeting_2008_08_29 then.

   Migration functions must be run from portal_setup within your Plone site
   through the ZMI. Every migration function corresponds to a import step in
   portal_setup.'''

# ------------------------------------------------------------------------------
from Products.CMFCore.utils import getToolByName

# ------------------------------------------------------------------------------
class Migrator:
    '''Abstract class for creating a migrator.'''
    def __init__(self, context):
        self.portal = context.getSite()
        self.tool = getToolByName(self.portal, 'portal_plonemeeting')
        self.profilecontext = context
    def run(self):
        '''Must be overridden. This method does the migration job.'''
        raise 'You should have overridden me darling.'''

# ------------------------------------------------------------------------------
