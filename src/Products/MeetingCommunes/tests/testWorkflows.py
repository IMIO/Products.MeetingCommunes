# -*- coding: utf-8 -*-
#
# File: testWorkflows.py
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
from AccessControl import Unauthorized
from zope.annotation import IAnnotations
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.interfaces import IAnnexable
from Products.PloneMeeting.tests.testWorkflows import testWorkflows as pmtw


class testWorkflows(MeetingCommunesTestCase, pmtw):
    """Tests the default workflows implemented in MeetingCommunes."""

    def test_subproduct_call_CreateItem(self):
        '''Run the test_pm_CreateItem from PloneMeeting.'''
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        self.test_pm_CreateItem()
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        self.test_pm_CreateItem()

    def test_subproduct_call_RemoveObjects(self):
        '''Run the test_pm_RemoveObjects from PloneMeeting.'''
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        self.test_pm_RemoveObjects()
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        self.test_pm_RemoveObjects()

    def test_subproduct_call_WholeDecisionProcess(self):
        """
            This test covers the whole decision workflow. It begins with the
            creation of some items, and ends by closing a meeting.
            This call 2 sub tests for each process : college and council
        """
        self._testWholeDecisionProcessCollege()
        self._testWholeDecisionProcessCouncil()

    def _testWholeDecisionProcessCollege(self):
        '''This test covers the whole decision workflow. It begins with the
           creation of some items, and ends by closing a meeting.'''
        # pmCreator1 creates an item with 1 annex and proposes it
        self.changeUser('pmCreator1')
        item1 = self.create('MeetingItem', title='The first item')
        self.addAnnex(item1)
        self.addAnnex(item1, relatedTo='item_decision')
        self.do(item1, 'propose')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # pmManager creates a meeting
        self.changeUser('pmManager')
        meeting = self.create('Meeting', date='2007/12/11 09:00:00')
        self.addAnnex(item1, relatedTo='item_decision')
        # pmCreator2 creates and proposes an item
        self.changeUser('pmCreator2')
        item2 = self.create('MeetingItem', title='The second item',
                            preferredMeeting=meeting.UID())
        self.do(item2, 'propose')
        # pmReviewer1 validates item1 and adds an annex to it
        self.changeUser('pmReviewer1')
        self.addAnnex(item1, relatedTo='item_decision')
        self.do(item1, 'validate')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # pmManager inserts item1 into the meeting and publishes it
        self.changeUser('pmManager')
        managerAnnex = self.addAnnex(item1)
        self.portal.restrictedTraverse('@@delete_givenuid')(managerAnnex.UID())
        self.do(item1, 'present')
        # Now reviewers can't add annexes anymore
        self.changeUser('pmReviewer1')
        self.assertRaises(Unauthorized, self.addAnnex, item2)
        # meeting is frozen
        self.changeUser('pmManager')
        self.do(meeting, 'freeze')  # publish in pm forkflow
        # pmReviewer2 validates item2
        self.changeUser('pmReviewer2')
        self.do(item2, 'validate')
        # pmManager inserts item2 into the meeting, as late item, and adds an
        # annex to it
        self.changeUser('pmManager')
        self.do(item2, 'present')
        self.addAnnex(item2)
        # So now we should have 3 normal item (2 recurring + 1) and one late item in the meeting
        self.failUnless(len(meeting.getItems()) == 4)
        self.failUnless(len(meeting.getItems(listTypes='late')) == 1)
        self.changeUser('pmManager')
        item1.setDecision(self.decisionText)
        # pmManager adds a decision for item2, decides and closes the meeting
        self.changeUser('pmManager')
        item2.setDecision(self.decisionText)
        self.addAnnex(item2, relatedTo='item_decision')
        self.do(meeting, 'decide')
        self.failIf(len(self.transitions(meeting)) != 2)
        self.do(meeting, 'close')

    def _testWholeDecisionProcessCouncil(self):
        """
            This test covers the whole decision workflow. It begins with the
            creation of some items, and ends by closing a meeting.
        """
        #meeting-config-college is tested in test_subproduct_WholeDecisionProcessCollege
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        # pmCreator1 creates an item with 1 annex and proposes it
        self.changeUser('pmCreator1')
        item1 = self.create('MeetingItem', title='The first item')
        self.addAnnex(item1)
        # The creator can add a decision annex on created item
        self.addAnnex(item1, relatedTo='item_decision')
        self.do(item1, 'propose')
        # The creator cannot add a decision annex on proposed item
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        # pmManager creates a meeting
        self.changeUser('pmManager')
        meeting = self.create('Meeting', date='2007/12/11 09:00:00')
        # The meetingManager can add a decision annex
        self.addAnnex(item1, relatedTo='item_decision')
        # pmCreator2 creates and proposes an item
        self.changeUser('pmCreator2')
        item2 = self.create('MeetingItem', title='The second item',
                            preferredMeeting=meeting.UID())
        self.do(item2, 'propose')
        # pmReviewer1 validates item1 and adds an annex to it
        self.changeUser('pmReviewer1')
        # The reviewer can add a decision annex on proposed item
        self.addAnnex(item1, relatedTo='item_decision')
        self.do(item1, 'validate')
        # The reviewer cannot add a decision annex on validated item
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        # pmManager inserts item1 into the meeting and freezes it
        self.changeUser('pmManager')
        managerAnnex = self.addAnnex(item1)
        self.portal.restrictedTraverse('@@delete_givenuid')(managerAnnex.UID())
        self.do(item1, 'present')
        self.changeUser('pmCreator1')
        # The creator cannot add any kind of annex on presented item
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        self.changeUser('pmManager')
        self.do(meeting, 'freeze')
        # pmReviewer2 validates item2
        self.changeUser('pmReviewer2')
        self.do(item2, 'validate')
        # pmManager inserts item2 into the meeting, as late item, and adds an
        # annex to it
        self.changeUser('pmManager')
        self.do(item2, 'present')
        self.addAnnex(item2)
        # So now I should have 1 normal item left and one late item in the meeting
        self.failIf(len(meeting.getItems()) != 2)
        self.failUnless(len(meeting.getItems(listTypes=['late'])) == 1)
        # pmReviewer1 can not add an annex on item1 as it is frozen
        self.changeUser('pmReviewer1')
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        # pmManager adds a decision to item1 and publishes the meeting
        self.changeUser('pmManager')
        item1.setDecision(self.decisionText)
        self.do(meeting, 'publish')
        # Now reviewers can't add annexes anymore
        self.changeUser('pmReviewer2')
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item2))
        self.assertRaises(Unauthorized, self.addAnnex, item2, relatedTo='item_decision')
        self.changeUser('pmReviewer1')
        self.assertRaises(Unauthorized, self.addAnnex, item2)
        self.assertRaises(Unauthorized, self.addAnnex, item2, relatedTo='item_decision')
        # pmManager adds a decision for item2, decides and closes the meeting
        self.changeUser('pmManager')
        item2.setDecision(self.decisionText)
        self.do(meeting, 'decide')
        # check that a delayed item is duplicated
        self.assertEquals(len(item1.getBRefs('ItemPredecessor')), 0)
        self.do(item1, 'delay')
        # the duplicated item has item3 as predecessor
        duplicatedItem = item1.getBRefs('ItemPredecessor')[0]
        self.assertEquals(duplicatedItem.getPredecessor().UID(), item1.UID())
        # when duplicated on delay, annexes are kept
        self.assertEquals(len(IAnnexable(duplicatedItem).getAnnexes('item')), 1)
        self.assertEquals(len(IAnnexable(duplicatedItem).getAnnexes('item_decision')), 3)
        self.addAnnex(item2, relatedTo='item_decision')
        self.failIf(len(self.transitions(meeting)) != 2)
        # When a meeting is closed, items without a decision are automatically 'accepted'
        self.do(meeting, 'close')
        self.assertEquals(item2.queryState(), 'accepted')
        # An already decided item keep his given decision
        self.assertEquals(item1.queryState(), 'delayed')
        # XXX added tests regarding ticket #5887
        # test back transitions
        self.changeUser('admin')
        self.do(meeting, 'backToDecided')
        self.changeUser('pmManager')
        self.do(meeting, 'backToPublished')
        # set an item back to published to test the 'freeze' meeting here under
        self.do(item1, 'backToItemPublished')
        self.do(meeting, 'backToFrozen')
        # this also test the 'doBackToCreated' action on the meeting
        self.do(meeting, 'backToCreated')
        self.do(meeting, 'freeze')
        self.do(meeting, 'publish')
        self.do(meeting, 'decide')
        self.do(meeting, 'close')

    def test_subproduct_call_WorkflowPermissions(self):
        """
            This test checks whether workflow permissions are correct while
            creating and changing state of items and meetings. During the test,
            some users go from one group to the other. The test checks that in
            this case local roles (whose permissions depend on) are correctly
            updated.
        """
        #we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        # XXX comment test for now has things has changed around giving an advice when an item is created
        # XXX test to set back on when using PloneMeeting 3
        #pmtw.testWorkflowPermissions(self)
        #we do the test for the council config => in a separate method : a rollback is needed

    def test_subproduct_WorkflowPermissionsCouncil(self):
        """
            This test checks whether workflow permissions are correct while
            creating and changing state of items and meetings. During the test,
            some users go from one group to the other. The test checks that in
            this case local roles (whose permissions depend on) are correctly
            updated.
        """
        #we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        # XXX comment test for now has things has changed around giving an advice when an item is created
        # XXX test to set back on when using PloneMeeting 3
        #pmtw.testWorkflowPermissions(self)

    def test_subproduct_call_RecurringItems(self):
        """
            Tests the recurring items system.
        """
        # we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        #pmtw.testRecurringItems(self) workflow is different
        self._checkRecurringItemsCollege()
        # we do the test for the council config
        # no recurring items defined...
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        meeting = self.create('Meeting', date='2007/12/11 09:00:00')
        self.assertEquals(len(meeting.getItems()), 0)

    def test_subproduct_call_RecurringItemsRespectSortingMethodOnAddItemPrivacy(self):
        '''Run the test_pm_RecurringItemsRespectSortingMethodOnAddItemPrivacy from PloneMeeting.'''
        self.test_pm_RecurringItemsRespectSortingMethodOnAddItemPrivacy()

    def test_subproduct_call_RecurringItemsWithWrongTransitionsForPresentingAnItem(self):
        '''Run the test_pm_RecurringItemsWithWrongTransitionsForPresentingAnItem from PloneMeeting.'''
        self.test_pm_RecurringItemsWithWrongTransitionsForPresentingAnItem()

    def _checkRecurringItemsCollege(self):
        '''Tests the recurring items system.'''
        # First, define recurring items in the meeting config
        self.changeUser('admin')
        # 2 recurring items already exist in the college config, add one supplementary for _init_
        self.create('MeetingItemRecurring', title='Rec item 1',
                    proposingGroup='developers',
                    meetingTransitionInsertingMe='_init_')
        # add 3 other recurring items that will be inserted at other moments in the WF
        # backToCreated is not in MeetingItem.meetingTransitionsAcceptingRecurringItems
        # so it will not be added...
        self.create('MeetingItemRecurring', title='Rec item 2',
                    proposingGroup='developers',
                    meetingTransitionInsertingMe='backToCreated')
        self.create('MeetingItemRecurring', title='Rec item 3',
                    proposingGroup='developers',
                    meetingTransitionInsertingMe='freeze')
        self.create('MeetingItemRecurring', title='Rec item 4',
                    proposingGroup='developers',
                    meetingTransitionInsertingMe='decide')
        self.changeUser('pmManager')
        # create a meeting without supplementary items, only the recurring items
        meeting = self._createMeetingWithItems(withItems=False)
        # The recurring items must have as owner the meeting creator
        for item in meeting.getItems():
            self.assertEquals(item.getOwner().getId(), 'pmManager')
        # The meeting must contain recurring items : 2 defined and one added here above
        self.failUnless(len(meeting.getItems()) == 3)
        self.failIf(meeting.getItems(listTypes=['late']))
        # After freeze, the meeting must have one recurring item more
        self.freezeMeeting(meeting)
        self.failUnless(len(meeting.getItems()) == 4)
        self.failUnless(len(meeting.getItems(listTypes=['late'])) == 1)
        # Back to created: rec item 2 is not inserted because
        # only some transitions can add a recurring item (see MeetingItem).
        self.backToState(meeting, 'created')
        self.failUnless(len(meeting.getItems()) == 4)
        self.failUnless(len(meeting.getItems(listTypes=['late'])) == 1)
        # Recurring items can be added twice...
        self.freezeMeeting(meeting)
        self.failUnless(len(meeting.getItems()) == 5)
        self.failUnless(len(meeting.getItems(listTypes=['late'])) == 2)
        # Decide the meeting, a third late item is added
        self.decideMeeting(meeting)
        self.failUnless(len(meeting.getItems()) == 6)
        self.failUnless(len(meeting.getItems(listTypes=['late'])) == 3)

    def test_subproduct_FreezeMeeting(self):
        """
           When we freeze a meeting, every presented items will be frozen
           too and their state will be set to 'itemfrozen'.  When the meeting
           come back to 'created', every items will be corrected and set in the
           'presented' state
        """
        # First, define recurring items in the meeting config
        self.changeUser('pmManager')
        # create a meeting
        meeting = self.create('Meeting', date='2007/12/11 09:00:00')
        # create 2 items and present it to the meeting
        item1 = self.create('MeetingItem', title='The first item')
        self.presentItem(item1)
        item2 = self.create('MeetingItem', title='The second item')
        self.presentItem(item2)
        wftool = self.portal.portal_workflow
        # every presented items are in the 'presented' state
        self.assertEquals('presented', wftool.getInfoFor(item1, 'review_state'))
        self.assertEquals('presented', wftool.getInfoFor(item2, 'review_state'))
        # every items must be in the 'itemfrozen' state if we freeze the meeting
        self.freezeMeeting(meeting)
        self.assertEquals('itemfrozen', wftool.getInfoFor(item1, 'review_state'))
        self.assertEquals('itemfrozen', wftool.getInfoFor(item2, 'review_state'))
        # when an item is 'itemfrozen' it will stay itemfrozen if nothing
        # is defined in the meetingConfig.onMeetingTransitionItemTransitionToTrigger
        self.meetingConfig.setOnMeetingTransitionItemTransitionToTrigger([])
        self.backToState(meeting, 'created')
        self.assertEquals('itemfrozen', wftool.getInfoFor(item1, 'review_state'))
        self.assertEquals('itemfrozen', wftool.getInfoFor(item2, 'review_state'))

    def test_subproduct_CloseMeeting(self):
        """
           When we close a meeting, every items are set to accepted if they are still
           not decided...
        """
        # First, define recurring items in the meeting config
        self.changeUser('pmManager')
        # create a meeting (with 7 items)
        meetingDate = DateTime().strftime('%y/%m/%d %H:%M:00')
        meeting = self.create('Meeting', date=meetingDate)
        item1 = self.create('MeetingItem')  # id=o2
        item1.setProposingGroup('vendors')
        item1.setAssociatedGroups(('developers',))
        item2 = self.create('MeetingItem')  # id=o3
        item2.setProposingGroup('developers')
        item3 = self.create('MeetingItem')  # id=o4
        item3.setProposingGroup('vendors')
        item4 = self.create('MeetingItem')  # id=o5
        item4.setProposingGroup('developers')
        item5 = self.create('MeetingItem')  # id=o7
        item5.setProposingGroup('vendors')
        item6 = self.create('MeetingItem', title='The sixth item')
        item6.setProposingGroup('vendors')
        item7 = self.create('MeetingItem')  # id=o8
        item7.setProposingGroup('vendors')
        for item in (item1, item2, item3, item4, item5, item6, item7):
            self.presentItem(item)
        # we freeze the meeting
        self.freezeMeeting(meeting)
        # a MeetingManager can put the item back to presented
        self.backToState(item7, 'presented')
        # we decide the meeting
        # while deciding the meeting, every items that where presented are frozen
        self.decideMeeting(meeting)
        # change all items in all different state (except first who is in good state)
        self.backToState(item7, 'presented')
        self.do(item2, 'delay')
        self.do(item3, 'pre_accept')
        self.do(item4, 'accept_but_modify')
        self.do(item5, 'refuse')
        self.do(item6, 'accept')
        # we close the meeting
        self.do(meeting, 'close')
        # every items must be in the 'decided' state if we close the meeting
        wftool = self.portal.portal_workflow
        # itemfrozen change into accepted
        self.assertEquals('accepted', wftool.getInfoFor(item1, 'review_state'))
        # delayed rest delayed (it's already a 'decide' state)
        self.assertEquals('delayed', wftool.getInfoFor(item2, 'review_state'))
        # pre_accepted change into accepted
        self.assertEquals('accepted', wftool.getInfoFor(item3, 'review_state'))
        # accepted_but_modified rest accepted_but_modified (it's already a 'decide' state)
        self.assertEquals('accepted_but_modified', wftool.getInfoFor(item4, 'review_state'))
        # refused rest refused (it's already a 'decide' state)
        self.assertEquals('refused', wftool.getInfoFor(item5, 'review_state'))
        # accepted rest accepted (it's already a 'decide' state)
        self.assertEquals('accepted', wftool.getInfoFor(item6, 'review_state'))
        # presented change into accepted
        self.assertEquals('accepted', wftool.getInfoFor(item7, 'review_state'))

    def test_subproduct_call_RemoveContainer(self):
        '''Run the test_pm_RemoveContainer from PloneMeeting.'''
        # we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        self.test_pm_RemoveContainer()
        # we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        # clean memoize because we test for status messages
        annotations = IAnnotations(self.portal.REQUEST)
        if 'statusmessages' in annotations:
            annotations['statusmessages'] = ''
        self.test_pm_RemoveContainer()

    def test_subproduct_call_DeactivateMeetingGroup(self):
        '''Run the test_pm_DeactivateMeetingGroup from PloneMeeting.'''
        self.test_pm_DeactivateMeetingGroup()

    def test_subproduct_call_RecurringItemsBypassSecutiry(self):
        '''Run the test_pm_RecurringItemsBypassSecutiry from PloneMeeting.'''
        self.test_pm_RecurringItemsBypassSecutiry()

    def test_subproduct_call_NoDefinedRecurringItems(self):
        '''Run the test_pm_NoDefinedRecurringItems from PloneMeeting.'''
        self.test_pm_NoDefinedRecurringItems()

    def test_subproduct_call_MeetingTransitionTriggerLinkedItemsTransitions(self):
        '''Run the test_pm_MeetingTransitionTriggerLinkedItemsTransitions from PloneMeeting.'''
        self.test_pm_MeetingTransitionTriggerLinkedItemsTransitions()

    def test_subproduct_call_InactiveRecurringItemsAreNotInserted(self):
        '''Run the test_pm_InactiveRecurringItemsAreNotInserted from PloneMeeting.'''
        self.test_pm_InactiveRecurringItemsAreNotInserted()

    def test_subproduct_call_MeetingNotClosableIfItemStillReturnedToProposingGroup(self):
        '''Run the test_pm_MeetingNotClosableIfItemStillReturnedToProposingGroup from PloneMeeting.'''
        self.test_pm_MeetingNotClosableIfItemStillReturnedToProposingGroup()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWorkflows, prefix='test_subproduct_'))
    return suite
