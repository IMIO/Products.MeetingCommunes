# -*- coding: utf-8 -*-
#
# File: testCustomUtils.py
#
# Copyright (c) 2017 by Imio.be
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

from AccessControl import Unauthorized
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase


class testCustomUtils(MeetingCommunesTestCase):
    """
        Tests the Extensions/utils methods.
    """

    def setUp(self):
        MeetingCommunesTestCase.setUp(self)
        # add the ExternalMethod export_orgs in Zope
        manage_addExternalMethod(self.portal.aq_inner.aq_parent,
                                 'export_orgs',
                                 '',
                                 'Products.MeetingCommunes.utils',
                                 'export_orgs')
        # add the ExternalMethod import_orgs in Zope
        manage_addExternalMethod(self.portal.aq_inner.aq_parent,
                                 'import_orgs',
                                 '',
                                 'Products.MeetingCommunes.utils',
                                 'import_orgs')

    def _exportOrgs(self):
        return self.portal.export_orgs()

    def _importOrgs(self, data):
        return self.portal.import_orgs(data=str(data))

    def test_AccessToMethods(self):
        """
          Check that only Managers can access the methods
        """
        self.assertRaises(Unauthorized, self._exportOrgs)
        self.assertRaises(Unauthorized, self._importOrgs, {})

    def test_ExportOrgs(self):
        """
          Check that calling this method returns the right content
        """
        self.changeUser('admin')
        expected = {
            'vendors': ('Vendors', '', 'Devil'),
            'endUsers': ('End users', '', 'EndUsers'),
            'developers': ('Developers', '', 'Devel')}
        res = self._exportOrgs()
        self.assertEquals(expected, res)

    def test_ImportOrgs(self):
        """
          Check that calling this method creates the organizations if not exist
        """
        self.changeUser('admin')
        # if we pass a dict containing the existing groups, it does nothing but
        # returning that the groups already exist
        data = self._exportOrgs()
        expected = 'Organization endUsers already exists\n' \
                   'Organization vendors already exists\n' \
                   'Organization developers already exists'
        res = self._importOrgs(data)
        self.assertEquals(expected, res)
        # but it can also add an organization if it does not exist
        data['newGroup'] = ('New group title', 'New group description', 'NGAcronym', 'python:False')
        expected = 'Organization endUsers already exists\n' \
                   'Organization vendors already exists\n' \
                   'Organization newGroup added\n' \
                   'Organization developers already exists'
        res = self._importOrgs(data)
        self.assertEquals(expected, res)
