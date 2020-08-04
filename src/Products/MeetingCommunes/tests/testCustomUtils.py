# -*- coding: utf-8 -*-

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
        self.assertEqual(expected, res)

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
        self.assertEqual(expected, res)
        # but it can also add an organization if it does not exist
        data['newGroup'] = ('New group title', 'New group description', 'NGAcronym', 'python:False')
        expected = 'Organization endUsers already exists\n' \
                   'Organization vendors already exists\n' \
                   'Organization newGroup added\n' \
                   'Organization developers already exists'
        res = self._importOrgs(data)
        self.assertEqual(expected, res)
