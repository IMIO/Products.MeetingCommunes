# -*- coding: utf-8 -*-
#
# File: testPortlets.py
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

from zope.component import getUtility, getMultiAdapter
from plone.portlets.interfaces import IPortletManager, IPortletRenderer
from Products.PloneMeeting.browser import portlet_plonemeeting as pm
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase
from Products.PloneMeeting.tests.testPortlets import testPortlets as pmtp

class testPortlets(MeetingCommunesTestCase, pmtp):
    '''Tests the portlets methods.'''

    def afterSetUp(self):
        MeetingCommunesTestCase.afterSetUp(self)

    def test_mc_call_PortletPMAvailableTemplates(self):
        '''Test the portlet_plonemeeting.getTemplateItems method
           returning available item templates for current user.
           template5 is available to everyone but template1 is restricted to group 'developers' and 'vendors'.'''
        #we do the test for the college config
        # pmCreator1 is member of 'developers'
        self.login('pmCreator1')
        self.getMeetingFolder()
        context = getattr(self.portal.Members.pmCreator1.mymeetings, self.meetingConfig.getId())
        request = self.portal.REQUEST
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = pm.Assignment()
        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertEquals( ['template1', 'template2', 'template3', 'template4', 'template5'], [template.getId() for template in renderer.getTemplateItems()])
        # pmCreator2 is member of 'vendors' and can so access template1 that is restricted to 'developers' and 'vendors'
        self.login('pmCreator2')
        self.getMeetingFolder()
        context = getattr(self.portal.Members.pmCreator2.mymeetings, self.meetingConfig.getId())
        request = self.portal.REQUEST
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = pm.Assignment()
        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertEquals(['template1', 'template5', ], [template.getId() for template in renderer.getTemplateItems()])
        #no templates for council config...
        # pmCreator1 is member of 'developers'
        self.login('pmCreator1')
        self.setMeetingConfig(self.meetingConfig2.getId())
        self.getMeetingFolder()
        context = getattr(self.portal.Members.pmCreator1.mymeetings, self.meetingConfig.getId())
        request = self.portal.REQUEST
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = pm.Assignment()
        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertEquals([], [template.getId() for template in renderer.getTemplateItems()])
        # pmCreator2 is member of 'vendors' and can so access template2 that is restricted to 'vendors'
        self.login('pmCreator2')
        self.getMeetingFolder()
        context = getattr(self.portal.Members.pmCreator2.mymeetings, self.meetingConfig.getId())
        request = self.portal.REQUEST
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = pm.Assignment()
        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertEquals([], [template.getId() for template in renderer.getTemplateItems()])

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testPortlets, prefix='test_mc_'))
    return suite
