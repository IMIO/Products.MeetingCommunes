# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2012 by CommunesPlone.org
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

import os.path
from warnings import warn
from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
import Products.PloneMeeting
# If I do not remove this method, some tests crash.
#from Products.PloneMeeting.MeetingItem import MeetingItem

# Initialize Zope & Plone test systems.
ZopeTestCase.installProduct('MeetingCommunes')
ZopeTestCase.installProduct('PloneMeeting')
PloneTestCase.setupPloneSite(products=['MeetingCommunes', 'PloneMeeting'])

class MeetingCommunesTestCase(PloneTestCase.PloneTestCase):
    """Base class for defining MeetingCommunes test cases."""

    # Some default content
    descriptionText = '<p>Some description</p>'
    decisionText = '<p>Some decision.</p>'

    def afterSetUp(self):
        # Define some useful attributes
        self.tool = self.portal.portal_plonemeeting
        self.wfTool = self.portal.portal_workflow
        self.pmFolder = os.path.dirname(Products.PloneMeeting.__file__)
        # Create admin user
        # Do not use 'userFolderAddUser' to avoid bug in Container
        self.createUser('admin', ('Member','Manager'))
        # Import the tests profile
        self.login('admin')
        self.portal.portal_setup.runImportStepFromProfile("profile-Products.MeetingCommunes:tests", "initializetool-MeetingCommunes")
        # Create some member areas
        for userId in ('pmManager', 'pmCreator1', 'pmCreator2'):
            self.createMemberarea(userId)
        # Disable notifications mechanism. This way, the test suite may be
        # executed even on production sites that contain many real users.
        for meetingConfig in self.tool.objectValues('MeetingConfig'):
            meetingConfig.setMailItemEvents([])
            meetingConfig.setMailMeetingEvents([])
        self.logout()
        # Set the default meeting config
#        self.meetingConfig = getattr(self.tool, 'plonegov-assembly')
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        self.meetingConfig2 = getattr(self.tool, 'meeting-config-council')
        # Set the default file and file type for adding annexes
        self.annexFile = 'INSTALL.TXT'
        self.annexFileType = 'annexeBudget'
        self.annexFileTypeDecision = 'annexeDecision'
        #classic "logger" is swallowed by the tests, so use "warn"...
        warn(self._TestCase__testMethodName)

    def getTestMethods(self, module, prefix):
        methods = {}
        for name in dir(module):
            if name.startswith(prefix) and name != 'test_mc_VerifyTestNumbers':
                methods[name] = 0
        return methods

    def createUser(self, username, roles):
        """ create a user with the good roles """
        pms = self.portal.portal_membership
        pms.addMember(username, 'password', [], [])
        self.setRoles(roles, name=username)

    def _adaptCategoriesForTest(self, meetingConfig):
        """
          This test depends on existing categories, so, define the same categories
          as in PloneMeeting
        """
        originalLoggedInUser = self.portal.portal_membership.getAuthenticatedMember().getId()
        self.login('admin')
        # Remove existing categories
        idsToRemove = []
        for cat in meetingConfig.categories.objectValues('MeetingCategory'):
            idsToRemove.append(cat.getId())
        meetingConfig.categories.manage_delObjects(idsToRemove)
        # Add new catgories
        # These are categories defined in PloneMeeting/profiles/test/import_data.py
        categories = [
                      ('deployment', 'Deployment topics'),
                      ('maintenance', 'Maintenance topics'),
                      ('development', 'Development topics'),
                      ('events', 'Events'),
                      ('research', 'Research topics'),
                      ('projects', 'Projects'),
                     ]
        for cat in categories:
            meetingConfig.categories.invokeFactory('MeetingCategory', id=cat[0], title=cat[1])
        #change the category of recurring items
        for item in meetingConfig.recurringitems.objectValues('MeetingItem'):
            item.setCategory('deployment')
        if originalLoggedInUser:
            self.login(originalLoggedInUser)
        else:
            self.logout()
