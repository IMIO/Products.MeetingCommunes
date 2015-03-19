# -*- coding: utf-8 -*-
#
# File: testAdvices.py
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

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.tests.testAdvices import testAdvices as pmta


class testAdvices(MeetingCommunesTestCase, pmta):
    '''Tests various aspects of advices management.
       Advices are enabled for PloneGov Assembly, not for PloneMeeting Assembly.'''

    def test_subproduct_call_ViewItemToAdvice(self):
        '''Run the test_pm_ViewItemToAdvice from PloneMeeting.'''
        pmta.test_pm_ViewItemToAdvice(self)

    def test_subproduct_call_AddEditDeleteAdvices(self):
        '''Run the test_pm_AddEditDeleteAdvices from PloneMeeting.'''
        pmta.test_pm_AddEditDeleteAdvices(self)

    def test_subproduct_call_CanNotGiveAdviceIfNotAsked(self):
        '''Run the test_pm_CanNotGiveAdviceIfNotAsked from PloneMeeting.'''
        pmta.test_pm_CanNotGiveAdviceIfNotAsked(self)

    def test_subproduct_call_GiveAdviceOnCreatedItem(self):
        '''Run the test_pm_GiveAdviceOnCreatedItem from PloneMeeting.'''
        pmta.test_pm_GiveAdviceOnCreatedItem(self)

    def test_subproduct_call_AdvicesInvalidation(self):
        '''Run the test_pm_AdvicesInvalidation from PloneMeeting.'''
        pmta.test_pm_AdvicesInvalidation(self)

    def test_subproduct_call_IndexAdvisers(self):
        '''Run the test_pm_IndexAdvisers from PloneMeeting.'''
        pmta.test_pm_IndexAdvisers(self)

    def test_subproduct_call_CanNotEditAnotherGroupAdvice(self):
        '''Run the test_pm_CanNotEditAnotherGroupAdvice from PloneMeeting.'''
        pmta.test_pm_CanNotEditAnotherGroupAdvice(self)

    def test_subproduct_call_AutomaticAdvices(self):
        '''Run the test_pm_AutomaticAdvices from PloneMeeting.'''
        pmta.test_pm_AutomaticAdvices(self)

    def test_subproduct_call_GetAutomaticAdvisers(self):
        '''Run the test_pm_getAutomaticAdvisers from PloneMeeting.'''
        pmta.test_pm_GetAutomaticAdvisers(self)

    def test_subproduct_call_MayNotAddAdviceEditIfDelayExceeded(self):
        '''Run the test_pm_getAutomaticAdvisers from PloneMeeting.'''
        pmta.test_pm_MayNotAddAdviceEditIfDelayExceeded(self)

    def test_subproduct_call_DelayStartedStoppedOn(self):
        '''Run the test_pm_getAutomaticAdvisers from PloneMeeting.'''
        pmta.test_pm_DelayStartedStoppedOn(self)

    def test_subproduct_call_RowIdSetOnAdvices(self):
        '''Run the test_pm_getAutomaticAdvisers from PloneMeeting.'''
        pmta.test_pm_RowIdSetOnAdvices(self)

    def test_subproduct_call_MeetingGroupDefinedItemAdviceStatesValuesOverridesMeetingConfigValues(self):
        '''Run the test_pm_MeetingGroupDefinedItemAdviceStatesValuesOverridesMeetingConfigValues from PloneMeeting.'''
        pmta.test_pm_MeetingGroupDefinedItemAdviceStatesValuesOverridesMeetingConfigValues(self)

    def test_subproduct_call_MeetingGroupDefinedItemAdviceStatesWorksTogetherWithMeetingConfigValues(self):
        '''Run the test_pm_MeetingGroupDefinedItemAdviceStatesWorksTogetherWithMeetingConfigValues from PloneMeeting.'''
        pmta.test_pm_MeetingGroupDefinedItemAdviceStatesWorksTogetherWithMeetingConfigValues(self)

    def test_subproduct_call_PowerAdvisers(self):
        '''Run the test_pm_getAutomaticAdvisers from PloneMeeting.'''
        pmta.test_pm_PowerAdvisers(self)

    def test_subproduct_call_ComputeDelaysWorkingDaysAndHolidaysAndUnavailableEndDays(self):
        '''Run the test_pm_ComputeDelaysWorkingDaysAndHolidaysAndUnavailableEndDays from PloneMeeting.'''
        pmta.test_pm_ComputeDelaysWorkingDaysAndHolidaysAndUnavailableEndDays(self)

    def test_subproduct_call_ComputeDelaysAsCalendarDays(self):
        '''Run the test_pm_ComputeDelaysAsCalendarDays from PloneMeeting.'''
        pmta.test_pm_ComputeDelaysAsCalendarDays(self)

    def test_subproduct_call_ChangeDelayView(self):
        '''Run the test_pm_ChangeDelayView from PloneMeeting.'''
        pmta.test_pm_ChangeDelayView(self)

    def test_subproduct_call_AvailableDelaysView(self):
        '''Run the test_pm_AvailableDelaysView from PloneMeeting.'''
        pmta.test_pm_AvailableDelaysView(self)

    def test_subproduct_call_ConfigAdviceStates(self):
        '''Run the test_pm_ConfigAdviceStates from PloneMeeting.'''
        pmta.test_pm_ConfigAdviceStates(self)

    def test_subproduct_call_GivenDelayAwareAutomaticAdviceLeftEvenIfItemConditionChanged(self):
        '''Run the test_pm_GivenDelayAwareAutomaticAdviceLeftEvenIfItemConditionChanged from PloneMeeting.'''
        pmta.test_pm_GivenDelayAwareAutomaticAdviceLeftEvenIfItemConditionChanged(self)

    def test_subproduct_call_AddAnnexToAdvice(self):
        '''Run the test_pm_AddAnnexToAdvice from PloneMeeting.'''
        pmta.test_pm_AddAnnexToAdvice(self)

    def test_subproduct_call_AdvicesConfidentiality(self):
        '''Run the test_pm_AdvicesConfidentiality from PloneMeeting.'''
        pmta.test_pm_AdvicesConfidentiality(self)

    def test_subproduct_call_MayTriggerGiveAdviceWhenItemIsBackToANotViewableState(self):
        '''Run the test_pm_MayTriggerGiveAdviceWhenItemIsBackToANotViewableState from PloneMeeting.'''
        pmta.test_pm_MayTriggerGiveAdviceWhenItemIsBackToANotViewableState(self)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testAdvices, prefix='test_subproduct_'))
    return suite
