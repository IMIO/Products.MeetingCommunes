# -*- coding: utf-8 -*-
#
# File: testMeetingItem.py
#
# Copyright (c) 2013 by Imio.be
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
from Products.PloneMeeting.tests.testMeetingItem import testMeetingItem as pmtmi


class testMeetingItem(MeetingCommunesTestCase, pmtmi):
    """
        Tests the MeetingItem class methods.
    """

    def test_subproduct_call_ListProposingGroups(self):
        '''See doc string in PloneMeeting.'''
        #we do the test for the college config
        self.setMeetingConfig(self.meetingConfig.getId())
        self.test_pm_ListProposingGroups()
        #we do the test for the council config
        self.setMeetingConfig(self.meetingConfig2.getId())
        self.test_pm_ListProposingGroups()

    def test_subproduct_call_UsedColorSystemGetColoredLink(self):
        '''See doc string in PloneMeeting.'''
        #we do the test for the college config
        self.setMeetingConfig(self.meetingConfig.getId())
        self.test_pm_UsedColorSystemGetColoredLink()
        #we do the test for the council config
        self.setMeetingConfig(self.meetingConfig2.getId())
        self.test_pm_UsedColorSystemGetColoredLink()

    def test_subproduct_call_UsedColorSystemShowColors(self):
        '''See doc string in PloneMeeting.'''
        #we do the test for the college config
        self.setMeetingConfig(self.meetingConfig.getId())
        self.test_pm_UsedColorSystemShowColors()
        #we do the test for the council config
        self.setMeetingConfig(self.meetingConfig2.getId())
        self.test_pm_UsedColorSystemShowColors()

    def test_subproduct_call_SendItemToOtherMC(self):
        '''See doc string in PloneMeeting.'''
        #we do the test for the college config, to send an item to the council
        self.setMeetingConfig(self.meetingConfig.getId())
        self.test_pm_SendItemToOtherMC()

    def test_subproduct_call_SelectableCategories(self):
        '''See doc string in PloneMeeting.'''
        #we do the test for the council config
        self.setMeetingConfig(self.meetingConfig2.getId())
        self.meetingConfig.useGroupsAsCategories = False
        self.test_pm_SelectableCategories()

    def test_subproduct_call_SendItemToOtherMCWithMappedCategories(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_SendItemToOtherMCWithMappedCategories()

    def test_subproduct_call_AddAutoCopyGroups(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_AddAutoCopyGroups()

    def test_subproduct_call_AddAutoCopyGroupsWrongExpressionDoesNotBreak(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_AddAutoCopyGroupsWrongExpressionDoesNotBreak()

    def test_subproduct_call_UpdateAdvices(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_UpdateAdvices()

    def test_subproduct_call_SendItemToOtherMCWithAnnexes(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_SendItemToOtherMCWithAnnexes()

    def test_subproduct_call_SendItemToOtherMCWithAdvices(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_SendItemToOtherMCWithAdvices()

    def test_subproduct_call_CopyGroups(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_CopyGroups()

    def test_subproduct_call_PowerObserversGroups(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_PowerObserversGroups()

    def test_subproduct_call_ItemIsSigned(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ItemIsSigned()

    def test_subproduct_call_IsPrivacyViewable(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_IsPrivacyViewable()

    def test_subproduct_call_IsLateFor(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_IsLateFor()

    def test_subproduct_call_ManageItemAssemblyAndSignatures(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ManageItemAssemblyAndSignatures()

    def test_subproduct_call_GetItemNumber(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_GetItemNumber()

    def test_subproduct_call_ListMeetingsAcceptingItems(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ListMeetingsAcceptingItems()

    def test_subproduct_call_ListCopyGroups(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ListCopyGroups()

    def test_subproduct_call_ListAssociatedGroups(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ListAssociatedGroups()

    def test_subproduct_call_ListOptionalAdvisersVocabulary(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ListOptionalAdvisersVocabulary()

    def test_subproduct_call_ListOptionalAdvisersDelayAwareAdvisers(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ListOptionalAdvisersDelayAwareAdvisers()

    def test_subproduct_call_SendItemToOtherMCRespectWFInitialState(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_SendItemToOtherMCRespectWFInitialState()

    def test_subproduct_call_SendItemToOtherMCWithTriggeredTransitions(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_SendItemToOtherMCWithTriggeredTransitions()

    def test_subproduct_call_SendItemToOtherMCActions(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_SendItemToOtherMCActions()

    def test_subproduct_call_CloneItemToMCWithoutDefinedAnnexType(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_CloneItemToMCWithoutDefinedAnnexType()

    def test_subproduct_call_Validate_optionalAdvisersCanNotUnselectAlreadyGivenAdvice(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_Validate_optionalAdvisersCanNotUnselectAlreadyGivenAdvice()

    def test_subproduct_call_Validate_optionalAdvisersCanNotSelectSameGroupAdvisers(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_Validate_optionalAdvisersCanNotSelectSameGroupAdvisers()

    def test_subproduct_call_BudgetImpactEditorsGroups(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_BudgetImpactEditorsGroups()

    def test_subproduct_call_AddAutoCopyGroupsIsCreated(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_AddAutoCopyGroupsIsCreated()

    def test_subproduct_call_Validate_proposingGroup(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_Validate_proposingGroup()

    def test_subproduct_call_Validate_category(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_Validate_category()

    def test_subproduct_call_GetDeliberation(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_GetDeliberation()

    def test_subproduct_call_GetMeetingsAcceptingItems(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_GetMeetingsAcceptingItems()

    def test_subproduct_call_OnTransitionFieldTransforms(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_OnTransitionFieldTransforms()

    def test_subproduct_call_TakenOverBy(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_TakenOverBy()

    def test_subproduct_call_ItemActionsPanelCaching(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ItemActionsPanelCaching()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from pmtmi
    suite.addTest(makeSuite(testMeetingItem, prefix='test_subproduct_'))
    return suite
