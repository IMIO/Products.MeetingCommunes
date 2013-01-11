# -*- coding: utf-8 -*-
#
# File: testVotes.py
#
# Copyright (c) 2012-2013 by PloneGov
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


from plone.app.testing import login

from Products.PloneMeeting.tests.testVotes import testVotes as pmtv
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase


class testVotes(MeetingCommunesTestCase, pmtv):
    '''Tests various aspects of votes management.
       Advices are enabled for PloneMeeting Assembly, not for PloneGov Assembly.
       By default, vote are encoded by 'theVoterHimself'.'''

    def setUp(self):
        # call parent setUp
        MeetingCommunesTestCase.setUp(self)
        # avoid recurring items
        login(self.portal, 'admin')
        self.meetingConfig.recurringitems.manage_delObjects([self.meetingConfig.recurringitems.objectValues()[0].getId(),])

    def test_mc_VerifyTestNumbers(self):
        """
            We verify that there are the same test methods in original product and this sub-product
        """
        tpm = self.getTestMethods(pmtv, 'test')
        tmc = self.getTestMethods(testVotes, 'test_mc_call_')
        missing = []
        for key in tpm:
            key2 = key.replace('test', 'test_mc_call_')
            if not tmc.has_key(key2):
                missing.append(key)
        if len(missing):
            self.fail("missing test methods %s from PloneMeeting test class '%s'" % (missing, 'testVotes'))

    def test_mc_call_MayConsultVotes(self):
        """
           Run the testMayConsultVotes from PloneMeeting
        """
        # votes are only enabled for the meeting-config-council
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtv.testMayConsultVotes(self)

    def test_mc_call_MayEditVotes(self):
        """
           Run the testMayEditVotes from PloneMeeting
        """
        # votes are only enabled for the meeting-config-council
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtv.testMayEditVotes(self)

    def test_mc_call_OnSaveItemPeopleInfos(self):
        """
           Run the testOnSaveItemPeopleInfos from PloneMeeting
        """
        # votes are only enabled for the meeting-config-council
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtv.testOnSaveItemPeopleInfos(self)

    def test_mc_call_SecretVotes(self):
        """
           Run the testSecretVotes from PloneMeeting
        """
        # votes are only enabled for the meeting-config-council
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        pmtv.testSecretVotes(self)



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testVotes, prefix='test_mc_'))
    return suite
