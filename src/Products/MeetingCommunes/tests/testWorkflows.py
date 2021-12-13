# -*- coding: utf-8 -*-
#
# File: testWorkflows.py
#
# GNU General Public License (GPL)
#

from AccessControl import Unauthorized
from Products.CMFCore.permissions import View
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.config import AddAnnex
from Products.PloneMeeting.config import AddAnnexDecision
from Products.PloneMeeting.tests.testWorkflows import testWorkflows as pmtw
from Products.PloneMeeting.utils import get_annexes
from zope.annotation import IAnnotations


class testWorkflows(MeetingCommunesTestCase, pmtw):
    """Tests the default workflows implemented in MeetingCommunes."""

    def test_pm_CreateItem(self):
        '''Run the test_pm_CreateItem from PloneMeeting.'''
        # we do the test for the college config
        self.meetingConfig = getattr(self.tool, self.cfg1_id)
        super(testWorkflows, self).test_pm_CreateItem()
        # we do the test for the council config
        self.meetingConfig = getattr(self.tool, self.cfg2_id)
        super(testWorkflows, self).test_pm_CreateItem()

    def test_pm_RemoveObjects(self):
        '''Run the test_pm_RemoveObjects from PloneMeeting.'''
        # we do the test for the college config
        self.meetingConfig = getattr(self.tool, self.cfg1_id)
        super(testWorkflows, self).test_pm_RemoveObjects()
        # we do the test for the council config
        self.meetingConfig = getattr(self.tool, self.cfg2_id)
        super(testWorkflows, self).test_pm_RemoveObjects()

    def test_pm_WholeDecisionProcess(self):
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
        # can add decision annex but not normal annex
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        self.addAnnex(item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission(AddAnnex, item1))
        # pmManager creates a meeting
        self.changeUser('pmManager')
        meeting = self.create('Meeting')
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
        # can not add decision annex or normal annex
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
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
        self.failUnless(len(meeting.get_items()) == 4)
        self.failUnless(len(meeting.get_items(list_types='late')) == 1)
        self.changeUser('pmManager')
        item1.setDecision(self.decisionText)

        # pmManager adds a decision for item2, and decides both meeting and item
        self.changeUser('pmManager')
        item2.setDecision(self.decisionText)
        self.addAnnex(item2, relatedTo='item_decision')
        self.do(meeting, 'decide')
        self.do(item1, 'accept')

        # pmCreator2/pmReviewer2 are not able to see item1
        self.changeUser('pmCreator2')
        self.failIf(self.hasPermission(View, item1))
        self.changeUser('pmReviewer2')
        self.failIf(self.hasPermission(View, item1))

        # meeting may be closed or set back to frozen
        self.changeUser('pmManager')
        self.assertEqual(self.transitions(meeting), ['backToFrozen', 'close'])
        self.changeUser('pmManager')
        self.do(meeting, 'close')

    def _testWholeDecisionProcessCouncil(self):
        """
            This test covers the whole decision workflow. It begins with the
            creation of some items, and ends by closing a meeting.
        """
        # meeting-config-college is tested in test_pm_WholeDecisionProcessCollege
        # we do the test for the council config
        self.meetingConfig = getattr(self.tool, self.cfg2_id)
        # pmCreator1 creates an item with 1 annex and proposes it
        self.changeUser('pmCreator1')
        item1 = self.create('MeetingItem', title='The first item')
        self.addAnnex(item1)
        # The creator can add a decision annex on created item
        self.addAnnex(item1, relatedTo='item_decision')
        self.do(item1, 'propose')
        # can add decision annex but not normal annex
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        self.addAnnex(item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        # pmManager creates a meeting
        self.changeUser('pmManager')
        meeting = self.create('Meeting')
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
        # can not add decision annex or normal annex
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        # pmManager inserts item1 into the meeting and freezes it
        self.changeUser('pmManager')
        managerAnnex = self.addAnnex(item1)
        self.portal.restrictedTraverse('@@delete_givenuid')(managerAnnex.UID())
        self.do(item1, 'present')
        self.changeUser('pmCreator1')
        # can not add decision annex or normal annex
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
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
        self.failIf(len(meeting.get_items()) != 2)
        self.failUnless(len(meeting.get_items(list_types=['late'])) == 1)
        self.changeUser('pmReviewer1')
        # can not add decision annex or normal annex
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        # pmManager adds a decision to item1 and publishes the meeting
        self.changeUser('pmManager')
        item1.setDecision(self.decisionText)
        self.do(meeting, 'publish')
        self.changeUser('pmReviewer2')
        # can not add decision annex or normal annex
        self.assertRaises(Unauthorized, self.addAnnex, item2)
        self.assertRaises(Unauthorized, self.addAnnex, item2, relatedTo='item_decision')
        self.changeUser('pmReviewer1')
        self.assertRaises(Unauthorized, self.addAnnex, item2)
        self.assertRaises(Unauthorized, self.addAnnex, item2, relatedTo='item_decision')
        # pmManager adds a decision for item2, decides and closes the meeting
        self.changeUser('pmManager')
        item2.setDecision(self.decisionText)
        self.do(meeting, 'decide')
        # check that a delayed item is duplicated
        self.assertEqual(len(item1.getBRefs('ItemPredecessor')), 0)
        self.do(item1, 'delay')
        # the duplicated item has item1 as predecessor
        duplicatedItem = item1.get_successors()[0]
        self.assertEqual(duplicatedItem.get_predecessor().UID(), item1.UID())
        # when duplicated on delay, only normal annexes are kept, decision annexes are not
        self.assertEqual(len(get_annexes(duplicatedItem, portal_types=('annex', ))), 1)
        self.assertEqual(len(get_annexes(duplicatedItem, portal_types=('annexDecision', ))), 0)
        self.addAnnex(item2, relatedTo='item_decision')
        self.failIf(len(self.transitions(meeting)) != 2)
        # When a meeting is closed, items without a decision are automatically 'accepted'
        self.do(meeting, 'close')
        self.assertEqual(item2.query_state(), 'accepted')
        # An already decided item keep his given decision
        self.assertEqual(item1.query_state(), 'delayed')
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

    def test_pm_WorkflowPermissions(self):
        """
          Pass this test...
        """
        pass

    def test_pm_RecurringItems(self):
        """
            Tests the recurring items system.
        """
        # we do the test for the college config
        self.meetingConfig = getattr(self.tool, self.cfg1_id)
        # super(testWorkflows, self).test_pm_RecurringItems() workflow is different
        self._checkRecurringItemsCollege()
        # we do the test for the council config
        # no recurring items defined...
        self.meetingConfig = getattr(self.tool, self.cfg2_id)
        self._checkRecurringItemsCouncil()

    def _checkRecurringItemsCollege(self):
        '''Tests the recurring items system.'''
        # First, define recurring items in the meeting config
        self.changeUser('admin')
        # 2 recurring items already exist in the college config, add one supplementary for _init_
        self.create('MeetingItemRecurring', title='Rec item 1',
                    proposingGroup=self.developers_uid,
                    meetingTransitionInsertingMe='_init_')
        # add 3 other recurring items that will be inserted at other moments in the WF
        # backToCreated is not in MeetingItem.meetingTransitionsAcceptingRecurringItems
        # so it will not be added...
        self.create('MeetingItemRecurring', title='Rec item 2',
                    proposingGroup=self.developers_uid,
                    meetingTransitionInsertingMe='backToCreated')
        self.create('MeetingItemRecurring', title='Rec item 3',
                    proposingGroup=self.developers_uid,
                    meetingTransitionInsertingMe='freeze')
        self.create('MeetingItemRecurring', title='Rec item 4',
                    proposingGroup=self.developers_uid,
                    meetingTransitionInsertingMe='decide')
        self.changeUser('pmManager')
        meeting = self.create('Meeting')
        # The recurring items must have as owner the meeting creator
        for item in meeting.get_items():
            self.assertEqual(item.getOwner().getId(), 'pmManager')
        # The meeting must contain recurring items : 2 defined and one added here above
        self.failUnless(len(meeting.get_items()) == 3)
        self.failIf(meeting.get_items(list_types=['late']))
        # After freeze, the meeting must have one recurring item more
        self.freezeMeeting(meeting)
        self.failUnless(len(meeting.get_items()) == 4)
        self.failUnless(len(meeting.get_items(list_types=['late'])) == 1)
        # Back to created: rec item 2 is inserted
        self.backToState(meeting, 'created')
        self.failUnless(len(meeting.get_items()) == 5)
        self.failUnless(len(meeting.get_items(list_types=['late'])) == 1)
        # Recurring items can be added twice...
        self.freezeMeeting(meeting)
        self.failUnless(len(meeting.get_items()) == 6)
        self.failUnless(len(meeting.get_items(list_types=['late'])) == 2)
        # Decide the meeting, a third late item is added
        self.decideMeeting(meeting)
        self.failUnless(len(meeting.get_items()) == 7)
        self.failUnless(len(meeting.get_items(list_types=['late'])) == 3)

    def _checkRecurringItemsCouncil(self):
        meeting = self.create('Meeting')
        self.assertEqual(len(meeting.get_items()), 0)

    def test_pm_RemoveContainer(self):
        '''Run the test_pm_RemoveContainer from PloneMeeting.'''
        # we do the test for the college config
        self.meetingConfig = getattr(self.tool, self.cfg1_id)
        super(testWorkflows, self).test_pm_RemoveContainer()
        # we do the test for the council config
        self.meetingConfig = getattr(self.tool, self.cfg2_id)
        # clean memoize because we test for status messages
        annotations = IAnnotations(self.portal.REQUEST)
        if 'statusmessages' in annotations:
            annotations['statusmessages'] = ''
        super(testWorkflows, self).test_pm_RemoveContainer()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWorkflows, prefix='test_pm_'))
    return suite
