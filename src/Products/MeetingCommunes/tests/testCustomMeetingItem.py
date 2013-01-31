# -*- coding: utf-8 -*-
#
# File: testCustomMeetingItem.py
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

from DateTime import DateTime
from plone.app.testing import login
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase
from Products.PloneMeeting.tests.testMeetingItem import testMeetingItem as pmtmi

class testCustomMeetingItem(MeetingCommunesTestCase, pmtmi):
    """
        Tests the MeetingItem adapted methods
    """

    def test_mc_GetMeetingsAcceptingItems(self):
        """
           We have to test this adapted method.
           It should only return meetings that are "created" or "frozen"
        """
        login(self.portal, 'pmManager')
        #create 4 meetings with items so we can play the workflow
        #will stay 'created'
        m1 = self.create('Meeting', date=DateTime('2013/02/01 08:00:00'))
        #go to state 'frozen'
        m2 = self.create('Meeting', date=DateTime('2013/02/08 08:00:00'))
        self.do(m2, 'freeze')
        #go to state 'decided'
        m3 = self.create('Meeting', date=DateTime('2013/02/15 08:00:00'))
        self.do(m3, 'freeze')
        self.do(m3, 'decide')
        #go to state 'closed'
        m4 = self.create('Meeting', date=DateTime('2013/02/22 08:00:00'))
        self.do(m4, 'freeze')
        self.do(m4, 'decide')
        self.do(m4, 'close')
        item = self.create('MeetingItem')
        #getMeetingsAcceptingItems should only return meetings 
        #that are 'created', 'frozen' or 'decided' for the meetingManager
        self.assertEquals([m.id for m in item.adapted().getMeetingsAcceptingItems()], [m1.id, m2.id, m3.id])
        #getMeetingsAcceptingItems should only return meetings 
        #that are 'created' or 'frozen' for the meetingMember
        login(self.portal, 'pmCreator1')
        item = self.create('MeetingItem')
        self.assertEquals([m.id for m in item.adapted().getMeetingsAcceptingItems()], [m1.id, m2.id])

    def test_mc_GetCertifiedSignatures(self):
        '''Check that the certified signature is defined on developers group but not defined on vendors.'''
        #create an item for test
        login(self.portal, 'pmManager')
        meetingDate = DateTime('2008/06/12 08:00:00')
        self.create('Meeting', date=meetingDate)
        #create items
        login(self.portal, 'pmCreator1')
        i1 = self.create('MeetingItem')
        i1.setProposingGroup('vendors')
        #before present in meeting, certfiedSignatures must be empty
        res, isGrpSign = i1.adapted().getCertifiedSignatures()
        self.assertEquals(res,'')
        self.assertEquals(isGrpSign,False)
        self.do(i1, 'propose')
        login(self.portal, 'pmReviewer1')
        self.do(i1, 'validate')
        login(self.portal, 'pmManager')
        self.do(i1, 'present')
        # no signatures defined for vendors group, the MeetingConfig.certifiedSignatures are used
        res, isGrpSign = i1.adapted().getCertifiedSignatures()
        self.assertEquals(res,'Mr Pr\xc3\xa9sent Actuellement, Bourgmestre ff - Charles Exemple, Secr\xc3\xa9taire communal')
        self.assertEquals(isGrpSign,False)
        login(self.portal, 'pmCreator1')
        i2 = self.create('MeetingItem')
        i2.setProposingGroup('developers')
        #before present in meeting, certfiedSignatures must be empty
        res, isGrpSign = i2.adapted().getCertifiedSignatures()
        self.assertEquals(res,'')
        self.assertEquals(isGrpSign,False)
        self.do(i2, 'propose')
        login(self.portal, 'pmReviewer1')
        self.do(i2, 'validate')
        login(self.portal, 'pmManager')
        self.do(i2, 'present')
        #signatures defined for developers group, get it
        res, isGrpSign = i2.adapted().getCertifiedSignatures()
        self.assertEquals(res,'developers signatures')
        self.assertEquals(isGrpSign,True)

    def test_mc_GetEchevinsForProposingGroup(self):
        '''Check a meetingItem for developers group return an echevin (the Same group in our case)
           and a meetingItem for vendors return no echevin.'''
        #create an item for test
        login(self.portal, 'pmManager')
        meetingDate = DateTime('2008/06/12 08:00:00')
        self.create('Meeting', date=meetingDate)
        #create items
        login(self.portal, 'pmCreator1')
        i1 = self.create('MeetingItem')
        i1.setProposingGroup('vendors')
        #before present in meeting, certfiedSignatures must be empty
        res = i1.adapted().getEchevinsForProposingGroup()
        self.assertEquals(res,[])
        login(self.portal, 'pmCreator1')
        i2 = self.create('MeetingItem')
        i2.setProposingGroup('developers')
        #before present in meeting, certfiedSignatures must be empty
        res = i2.adapted().getEchevinsForProposingGroup()
        self.assertEquals(res,['developers'])

    def test_mc_getDelayedDecision(self):
        '''If item is reported, the decision can be changed'''
        login(self.portal, 'pmManager')
        #create a meeting with items so we can play the workflow
        #will stay 'created'
        m1 = self._createMeetingWithItems()
        self.do(m1, 'freeze')
        self.do(m1, 'decide')
        item = m1.getItems()[0]
        item.setDecision('<p>Testing decision field</p>')
        #field itemDecisionReportText in configuration is empty
        self.assertEquals(item.getDecision(),'<p>Testing decision field</p>')
        self.do(item, 'delay')
        self.assertEquals(item.getDecision(),'<p>Testing decision field</p>')
        #change field itemDecisionReportText in configuration by python:'item is delay'
        item = m1.getItems()[1]
        meetingConfig = item.portal_plonemeeting.getMeetingConfig(item)
        login(self.portal, 'admin')
        meetingConfig.setItemDecisionReportText("python:'<p>Item is delayed</p>'")
        login(self.portal, 'pmManager')
        item.setDecision('<p>Testing decision field</p>')
        #field itemDecisionReportText in configuration is empty
        self.assertEquals(item.getDecision(),'<p>Testing decision field</p>')
        self.do(item, 'delay')
        self.assertEquals(item.getDecision(),'<p>Item is delayed</p>')
        #change field itemDecisionReportText in configuration by python:'%s delay this item'%here.getDecision()'
        item = m1.getItems()[2]
        meetingConfig = item.portal_plonemeeting.getMeetingConfig(item)
        meetingConfig.setItemDecisionReportText("python:'%s<p>Delay this item</p>' % here.getDecision()")
        item.setDecision('<p>Testing decision field</p>')
        #field itemDecisionReportText in configuration is empty
        self.do(item, 'delay')
        self.assertEquals(item.getDecision(),'<p>Testing decision field</p><p>Delay this item</p>')



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from pmtmi
    suite.addTest(makeSuite(testCustomMeetingItem, prefix='test_mc_'))
    return suite
