# -*- coding: utf-8 -*-
#
# File: testCustomWorkflows.py
#
# GNU General Public License (GPL)
#

from Products.CMFCore.permissions import AccessContentsInformation
from Products.CMFCore.permissions import View
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase


class testCustomWorkflows(MeetingCommunesTestCase):
    """Tests the default workflows implemented in MeetingCommunes."""

    def test_FreezeMeeting(self):
        """
           When we freeze a meeting, every presented items will be frozen
           too and their state will be set to 'itemfrozen'.  When the meeting
           come back to 'created', every items will be corrected and set in the
           'presented' state
        """
        # First, define recurring items in the meeting config
        self.changeUser('pmManager')
        # create a meeting
        meeting = self.create('Meeting')
        # create 2 items and present it to the meeting
        item1 = self.create('MeetingItem', title='The first item')
        self.presentItem(item1)
        item2 = self.create('MeetingItem', title='The second item')
        self.presentItem(item2)
        wftool = self.portal.portal_workflow
        # every presented items are in the 'presented' state
        self.assertEqual('presented', wftool.getInfoFor(item1, 'review_state'))
        self.assertEqual('presented', wftool.getInfoFor(item2, 'review_state'))
        # every items must be in the 'itemfrozen' state if we freeze the meeting
        self.freezeMeeting(meeting)
        self.assertEqual('itemfrozen', wftool.getInfoFor(item1, 'review_state'))
        self.assertEqual('itemfrozen', wftool.getInfoFor(item2, 'review_state'))
        # when an item is 'itemfrozen' it will stay itemfrozen if nothing
        # is defined in the meetingConfig.onMeetingTransitionItemActionToExecute
        self.meetingConfig.setOnMeetingTransitionItemActionToExecute([])
        self.backToState(meeting, 'created')
        self.assertEqual('itemfrozen', wftool.getInfoFor(item1, 'review_state'))
        self.assertEqual('itemfrozen', wftool.getInfoFor(item2, 'review_state'))

    def test_CloseMeeting(self):
        """
           When we close a meeting, every items are set to accepted if they are still
           not decided...
        """
        # First, define recurring items in the meeting config
        self.changeUser('pmManager')
        # create a meeting (with 7 items)
        meeting = self.create('Meeting')
        item1 = self.create('MeetingItem')  # id=o2
        item1.setProposingGroup(self.vendors_uid)
        item1.setAssociatedGroups((self.developers_uid,))
        item2 = self.create('MeetingItem')  # id=o3
        item2.setProposingGroup(self.developers_uid)
        item3 = self.create('MeetingItem')  # id=o4
        item3.setProposingGroup(self.vendors_uid)
        item4 = self.create('MeetingItem')  # id=o5
        item4.setProposingGroup(self.developers_uid)
        item5 = self.create('MeetingItem')  # id=o7
        item5.setProposingGroup(self.vendors_uid)
        item6 = self.create('MeetingItem', title='The sixth item')
        item6.setProposingGroup(self.vendors_uid)
        item7 = self.create('MeetingItem')  # id=o8
        item7.setProposingGroup(self.vendors_uid)
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
        if 'pre_accept' in self.transitions(item3):
            self.do(item3, 'pre_accept')
        self.do(item4, 'accept_but_modify')
        self.do(item5, 'refuse')
        self.do(item6, 'accept')
        # we close the meeting
        self.do(meeting, 'close')
        # every items must be in the 'decided' state if we close the meeting
        wftool = self.portal.portal_workflow
        # itemfrozen change into accepted
        self.assertEqual('accepted', wftool.getInfoFor(item1, 'review_state'))
        # delayed stays delayed (it's already a 'decide' state)
        self.assertEqual('delayed', wftool.getInfoFor(item2, 'review_state'))
        # pre_accepted change into accepted or item was accepted automatically from itemFrozen
        self.assertEqual('accepted', wftool.getInfoFor(item3, 'review_state'))
        # accepted_but_modified stays accepted_but_modified (it's already a 'decide' state)
        self.assertEqual('accepted_but_modified', wftool.getInfoFor(item4, 'review_state'))
        # refused stays refused (it's already a 'decide' state)
        self.assertEqual('refused', wftool.getInfoFor(item5, 'review_state'))
        # accepted stays accepted (it's already a 'decide' state)
        self.assertEqual('accepted', wftool.getInfoFor(item6, 'review_state'))
        # presented change into accepted
        self.assertEqual('accepted', wftool.getInfoFor(item7, 'review_state'))

    def test_pm_ObserversMayViewInEveryStates(self):
        """A MeetingObserverLocal has every 'View' permissions in every states."""
        def _checkObserverMayView(item):
            """Log as 'pmObserver1' and check if he has every 'View' like permissions."""
            original_user_id = self.member.getId()
            self.changeUser('pmObserver1')
            # compute permissions to check, it is View + ACI + every "PloneMeeting: Read ..." permissions
            itemWF = self.portal.portal_workflow.getWorkflowsFor(item)[0]
            read_permissions = [permission for permission in itemWF.permissions
                                if permission.startswith('PloneMeeting: Read')]
            read_permissions.append(View)
            read_permissions.append(AccessContentsInformation)
            for read_permission in read_permissions:
                self.assertTrue(self.hasPermission(read_permission, item))
            self.changeUser(original_user_id)
        # enable prevalidation
        cfg = self.meetingConfig
        self.changeUser('pmManager')
        self._enablePrevalidation(cfg)
        self._turnUserIntoPrereviewer(self.member)
        item = self.create('MeetingItem')
        item.setDecision(self.decisionText)
        meeting = self.create('Meeting')
        for transition in self.TRANSITIONS_FOR_PRESENTING_ITEM_1:
            _checkObserverMayView(item)
            if transition in self.transitions(item):
                self.do(item, transition)
        _checkObserverMayView(item)
        for transition in self.TRANSITIONS_FOR_CLOSING_MEETING_1:
            _checkObserverMayView(item)
            if transition in self.transitions(meeting):
                self.do(meeting, transition)
        _checkObserverMayView(item)
        # we check that item and meeting did their complete workflow
        self.assertEqual(item.query_state(), 'accepted')
        self.assertEqual(meeting.query_state(), 'closed')
