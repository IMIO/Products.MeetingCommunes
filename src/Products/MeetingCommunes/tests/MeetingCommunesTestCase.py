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

from plone.app.testing import login, logout

from Products.PloneMeeting.tests.PloneMeetingTestCase import PloneMeetingTestCase

from Products.MeetingCommunes.testing import MC_TESTS_PROFILE_FUNCTIONAL


class MeetingCommunesTestCase(PloneMeetingTestCase):
    """Base class for defining MeetingCommunes test cases."""

    # Some default content
    descriptionText = '<p>Some description</p>'
    decisionText = '<p>Some decision.</p>'

    layer = MC_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        PloneMeetingTestCase.setUp(self)
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        self.meetingConfig2 = getattr(self.tool, 'meeting-config-council')
        # Set the default file and file type for adding annexes
        self.annexFile = 'INSTALL.TXT'
        self.annexFileType = 'annexeBudget'
        self.annexFileTypeDecision = 'annexeDecision'
        self.transitionsToCloseAMeeting = ('freeze', 'publish', 'decide', 'close')

    def getTestMethods(self, module, prefix):
        methods = {}
        for name in dir(module):
            if name.startswith(prefix) and name != 'test_mc_VerifyTestNumbers':
                methods[name] = 0
        return methods

    def _adaptCategoriesForTest(self, meetingConfig):
        """
          This test depends on existing categories, so, define the same categories
          as in PloneMeeting
        """
        originalLoggedInUser = self.portal.portal_membership.getAuthenticatedMember().getId()
        login(self.portal, 'admin')
        # Remove existing categories
        idsToRemove = []
        for cat in meetingConfig.categories.objectValues('MeetingCategory'):
            idsToRemove.append(cat.getId())
        meetingConfig.categories.manage_delObjects(idsToRemove)
        # Add new catgories
        # These are categories defined in PloneMeeting/profiles/test/import_data.py
        categories = [('deployment', 'Deployment topics'),
                      ('maintenance', 'Maintenance topics'),
                      ('development', 'Development topics'),
                      ('events', 'Events'),
                      ('research', 'Research topics'),
                      ('projects', 'Projects'),
                      ('subproducts', 'Subproducts'), ]
        for cat in categories:
            meetingConfig.categories.invokeFactory('MeetingCategory', id=cat[0], title=cat[1])
        #change the category of recurring items
        for item in meetingConfig.recurringitems.objectValues('MeetingItem'):
            item.setCategory('deployment')
        # subproducts is a usingGroups category
        meetingConfig.categories.subproducts.setUsingGroups(('vendors',))
        if originalLoggedInUser:
            login(self.portal, originalLoggedInUser)
        else:
            logout()
