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

    def test_subproduct_call_GetAllCopyGroups(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_GetAllCopyGroups()

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

    def test_subproduct_call_SendItemToOtherMCUsingEmergency(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_SendItemToOtherMCUsingEmergency()

    def test_subproduct_call_SendItemToOtherMCActions(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_SendItemToOtherMCActions()

    def test_subproduct_call_SendItemToOtherMCManually(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_SendItemToOtherMCManually()

    def test_subproduct_call_CloneItemToMCWithoutDefinedAnnexType(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_CloneItemToMCWithoutDefinedAnnexType()

    def test_subproduct_call_Validate_optionalAdvisersCanNotUnselectAlreadyGivenAdvice(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_Validate_optionalAdvisersCanNotUnselectAlreadyGivenAdvice()

    def test_subproduct_call_Validate_optionalAdvisersCanNotSelectSameGroupAdvisers(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_Validate_optionalAdvisersCanNotSelectSameGroupAdvisers()

    def test_subproduct_call_PowerObserversLocalRoles(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_PowerObserversLocalRoles()

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

    def test_subproduct_call_HistorizedTakenOverBy(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_HistorizedTakenOverBy()

    def test_subproduct_call_ItemActionsPanelCachingInvalidatedWhenItemModified(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ItemActionsPanelCachingInvalidatedWhenItemModified()

    def test_subproduct_call_ItemActionsPanelCachingInvalidatedWhenItemStateChanged(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ItemActionsPanelCachingInvalidatedWhenItemStateChanged()

    def test_subproduct_call_ItemActionsPanelCachingInvalidatedWhenUserChanged(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ItemActionsPanelCachingInvalidatedWhenUserChanged()

    def test_subproduct_call_ItemActionsPanelCachingInvalidatedWhenItemTurnsToPresentable(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ItemActionsPanelCachingInvalidatedWhenItemTurnsToPresentable()

    def test_subproduct_call_ItemActionsPanelCachingInvalidatedWhenItemTurnsToNoMorePresentable(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ItemActionsPanelCachingInvalidatedWhenItemTurnsToNoMorePresentable()

    def ItemActionsPanelCachingInvalidatedWhenItemTurnsToNoMorePresentable(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ItemActionsPanelCachingInvalidatedWhenItemTurnsToNoMorePresentable()

    def test_subproduct_call_ItemActionsPanelCachingInvalidatedWhenLinkedMeetingIsEdited(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ItemActionsPanelCachingInvalidatedWhenLinkedMeetingIsEdited()

    def test_subproduct_call_ItemActionsPanelCachingInvalidatedWhenMeetingConfigEdited(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ItemActionsPanelCachingInvalidatedWhenMeetingConfigEdited()

    def test_subproduct_call_HistoryCommentViewability(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_HistoryCommentViewability()

    def test_subproduct_call_GetCertifiedSignatures(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_GetCertifiedSignatures()

    def test_subproduct_call_ItemCreatedOnlyUsingTemplate(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ItemCreatedOnlyUsingTemplate()

    def test_subproduct_call_GetAdviceDataFor(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_GetAdviceDataFor()

    def test_subproduct_call_CopiedFieldsWhenDuplicated(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_CopiedFieldsWhenDuplicated()

    def test_subproduct_call_CopiedFieldsWhenDuplicatedAsItemTemplate(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_CopiedFieldsWhenDuplicatedAsItemTemplate()

    def test_subproduct_call_CopiedFieldsWhenDuplicatedAsRecurringItem(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_CopiedFieldsWhenDuplicatedAsRecurringItem()

    def test_subproduct_call_CopiedFieldsWhenSentToOtherMC(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_CopiedFieldsWhenSentToOtherMC()

    def test_subproduct_call_CustomInsertingMethodRaisesNotImplementedErrorIfNotImplemented(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_CustomInsertingMethodRaisesNotImplementedErrorIfNotImplemented()

    def test_subproduct_call_EmptyLinesAreHighlighted(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_EmptyLinesAreHighlighted()

    def test_subproduct_call_ManuallyLinkedItems(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ManuallyLinkedItems()

    def test_subproduct_call_ManuallyLinkedItemsCanUpdateEvenWithNotViewableItems(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ManuallyLinkedItemsCanUpdateEvenWithNotViewableItems()

    def test_subproduct_call_ManuallyLinkedItemsSortedByMeetingDate(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ManuallyLinkedItemsSortedByMeetingDate()

    def test_subproduct_call_ToDiscussFieldBehaviourWhenCloned(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ToDiscussFieldBehaviourWhenCloned()

    def test_subproduct_call_Completeness(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_Completeness()

    def test_subproduct_call_Emergency(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_Emergency()

    def test_subproduct_call_ItemStrikedAssembly(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_ItemStrikedAssembly()

    def test_subproduct_call_DownOrUpWorkflowAgain(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_DownOrUpWorkflowAgain()

    def test_subproduct_call_groupIsNotEmpty(self):
        '''See doc string in PloneMeeting.'''
        self.test_pm_groupIsNotEmpty()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    # launch only tests prefixed by 'test_mc_' to avoid launching the tests coming from pmtmi
    suite.addTest(makeSuite(testMeetingItem, prefix='test_subproduct_'))
    return suite
