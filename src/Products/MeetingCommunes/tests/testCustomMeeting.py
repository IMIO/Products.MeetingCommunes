# -*- coding: utf-8 -*-
#
# File: testCustomMeeting.py
#
# Copyright (c) 2007-2013 by Imio.be
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
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase


class testCustomMeeting(MeetingCommunesTestCase):
    """
        Tests the Meeting adapted methods
    """

    def testGetPrintableItemsByCategoryWithMeetingCategory(self):
        """
            This method aimed to ease printings should return a list of items ordered by category
        """
        #a list of lists where inner lists contain
        #a categrory (MeetingCategory or MeetingGroup) as first element and items of this category

        #configure PloneMeeting
        #test if the category is a MeetingCategory
        #insert items in the meeting depending on the category
        login(self.portal, 'admin')
        self.setMeetingConfig(self.meetingConfig2.getId())
        meeting = self._createMeetingWithItems()
        #build the list of uids
        itemUids = []
        for item in meeting.getItemsInOrder():
            itemUids.append(item.UID())
        #test on the meeting
        #we should have a list containing 3 lists, 1 list by category
        self.assertEquals(len(meeting.adapted().getPrintableItemsByCategory(itemUids)), 3)
        #the order and the type should be kept, the first element of inner list is a MeetingCategory
        self.assertEquals(meeting.adapted().getPrintableItemsByCategory(itemUids)[0][0].getId(), 'development')
        self.assertEquals(meeting.adapted().getPrintableItemsByCategory(itemUids)[1][0].getId(), 'events')
        self.assertEquals(meeting.adapted().getPrintableItemsByCategory(itemUids)[2][0].getId(), 'research')
        self.assertEquals(meeting.adapted().getPrintableItemsByCategory(itemUids)[0][0].meta_type, 'MeetingCategory')
        self.assertEquals(meeting.adapted().getPrintableItemsByCategory(itemUids)[1][0].meta_type, 'MeetingCategory')
        self.assertEquals(meeting.adapted().getPrintableItemsByCategory(itemUids)[2][0].meta_type, 'MeetingCategory')
        #other element of the list are MeetingItems...
        self.assertEquals(meeting.adapted().getPrintableItemsByCategory(itemUids)[0][1].meta_type, 'MeetingItem')
        self.assertEquals(meeting.adapted().getPrintableItemsByCategory(itemUids)[0][2].meta_type, 'MeetingItem')
        self.assertEquals(meeting.adapted().getPrintableItemsByCategory(itemUids)[1][1].meta_type, 'MeetingItem')
        self.assertEquals(meeting.adapted().getPrintableItemsByCategory(itemUids)[1][2].meta_type, 'MeetingItem')
        self.assertEquals(meeting.adapted().getPrintableItemsByCategory(itemUids)[2][1].meta_type, 'MeetingItem')

    def testGetPrintableItemsByCategoryWithMeetingGroup(self):
        """
            This method aimed to ease printings should return a list of items ordered by category
        """
        #a list of lists where inner lists contain
        #a categrory (MeetingCategory or MeetingGroup) as first element and items of this category

        #configure PloneMeeting
        #test if the category is a MeetingCategory
        #insert items in the meeting depending on the category
        login(self.portal, 'admin')
        self.meetingConfig.setSortingMethodOnAddItem('on_proposing_groups')

        #add a Meeting and present several items in different categories
        login(self.portal, 'pmManager')
        i1 = self.create('MeetingItem', title='Item1')
        i1.setProposingGroup('developers')
        i2 = self.create('MeetingItem', title='Item2')
        i2.setProposingGroup('developers')
        i3 = self.create('MeetingItem', title='Item3')
        i3.setProposingGroup('developers')
        i4 = self.create('MeetingItem', title='Item4')
        i4.setProposingGroup('vendors')
        i5 = self.create('MeetingItem', title='Item5')
        i5.setProposingGroup('vendors')
        i6 = self.create('MeetingItem', title='Item6')
        i6.setProposingGroup('vendors')
        i7 = self.create('MeetingItem', title='Item7')
        i7.setProposingGroup('vendors')
        items = (i1, i2, i3, i4, i5, i6, i7)
        m = self.create('Meeting', date='2007/12/11 09:00:00')
        #present every items in a meeting
        for item in items:
            self.do(item, 'propose')
            self.do(item, 'validate')
            self.do(item, 'present')
        #build the list of uids
        itemUids = []
        for item in m.getItemsInOrder():
            itemUids.append(item.UID())
        #test on the meeting
        #we should have a list containing 3 lists, 1 list by category
        self.assertEquals(len(m.adapted().getPrintableItemsByCategory(itemUids)), 2)
        #the order and the type should be kept, the first element of inner list is a MeetingCategory
        self.assertEquals(m.adapted().getPrintableItemsByCategory(itemUids)[0][0].getId(), 'developers')
        self.assertEquals(m.adapted().getPrintableItemsByCategory(itemUids)[1][0].getId(), 'vendors')
        self.assertEquals(m.adapted().getPrintableItemsByCategory(itemUids)[0][0].meta_type, 'MeetingGroup')
        self.assertEquals(m.adapted().getPrintableItemsByCategory(itemUids)[1][0].meta_type, 'MeetingGroup')
        #other element of the list are MeetingItems...
        self.assertEquals(m.adapted().getPrintableItemsByCategory(itemUids)[0][1].meta_type, 'MeetingItem')
        self.assertEquals(m.adapted().getPrintableItemsByCategory(itemUids)[0][2].meta_type, 'MeetingItem')
        self.assertEquals(m.adapted().getPrintableItemsByCategory(itemUids)[0][3].meta_type, 'MeetingItem')
        self.assertEquals(m.adapted().getPrintableItemsByCategory(itemUids)[1][1].meta_type, 'MeetingItem')
        self.assertEquals(m.adapted().getPrintableItemsByCategory(itemUids)[1][2].meta_type, 'MeetingItem')
        self.assertEquals(m.adapted().getPrintableItemsByCategory(itemUids)[1][3].meta_type, 'MeetingItem')
        self.assertEquals(m.adapted().getPrintableItemsByCategory(itemUids)[1][4].meta_type, 'MeetingItem')

    def testInitializeDecisionField(self):
        """
            In the doDecide method, we initialize the Decision field to a default value made of
            Title+Description if the field is empty...
        """
        #check that it works
        #check that if the field contains something, it is not intialized again
        login(self.portal, 'pmManager')
        #create some items
        #empty decision
        i1 = self.create('MeetingItem', title='Item1', description="<p>Description Item1</p>")
        i1.setDecision("")
        i1.setProposingGroup('developers')
        #decision field is already filled
        i2 = self.create('MeetingItem', title='Item2', description="<p>Description Item2</p>")
        i2.setDecision("<p>Decision Item2</p>")
        i2.setProposingGroup('developers')
        #create an item with the default Kupu empty value
        i3 = self.create('MeetingItem', title='Item3', description="<p>Description Item3</p>")
        i3.setDecision("<p><br /></p>")
        i3.setProposingGroup('developers')
        m = self.create('Meeting', date='2007/12/11 09:00:00')
        #present every items in the meeting
        items = (i1, i2, i3)
        for item in items:
            self.do(item, 'propose')
            self.do(item, 'validate')
            self.do(item, 'present')
        #check the decision field of every item
        self.assertEquals(i1.getDecision(), "")
        self.assertEquals(i2.getDecision(), "<p>Decision Item2</p>")
        self.assertEquals(i3.getDecision(), "<p><br /></p>")
        #decide the meeting (freez it before ;-))
        self.do(m, 'freeze')
        self.do(m, 'decide')
        #now that the meeting is decided, the decision field initialization has occured...
        #i1 should be initialized
        self.assertEquals(i1.getDecision(), "<p>Item1</p><p>Description Item1</p>")
        #i2 sould not have changed
        self.assertEquals(i2.getDecision(), "<p>Decision Item2</p>")
        #i3 is initlaized because the decision field contained an empty_value
        self.assertEquals(i3.getDecision(), "<p>Item3</p><p>Description Item3</p>")

    def testShowAllItemsAtOnce(self):
        """
          The allItemsAtOnce field is only shown for not decided meetings
        """
        login(self.portal, 'pmManager')
        item = self.create('MeetingItem', title='Item1', description="<p>Description Item1</p>")
        item.setProposingGroup('developers')
        m = self.create('Meeting', date='2009/11/26 09:00:00')
        #present the item
        self.do(item, 'propose')
        self.do(item, 'validate')
        self.do(item, 'present')
        #the field is never shown anymore now...
        self.failIf(m.showAllItemsAtOnce())
        self.do(m, 'freeze')
        #the meeting is frozen and still not decided
        self.failIf(m.showAllItemsAtOnce())
        self.do(m, 'decide')
        #now the field is no more editable
        self.failIf(m.showAllItemsAtOnce())
        self.do(m, 'close')
        self.failIf(m.showAllItemsAtOnce())

    def testGetNumberOfItems(self):
        """
          This method will return a certain number of items depending on passed paramaters.
        """
        login(self.portal, 'admin')
        # make categories available
        self.setMeetingConfig(self.meetingConfig2.getId())
        login(self.portal, 'pmManager')
        meeting = self._createMeetingWithItems()
        orderedItems = meeting.getAllItems(ordered=True)
        # the meeting is created with 5 items
        self.assertEquals(len(orderedItems), 5)
        itemUids = [item.UID() for item in orderedItems]
        # without parameters, every items are returned
        self.assertEquals(meeting.adapted().getNumberOfItems(itemUids), 5)

        # test the 'privacy' parameter
        # by default, 2 items are 'secret' and 3 are 'public'
        itemPrivacies = [item.getPrivacy() for item in orderedItems]
        self.assertEquals(itemPrivacies.count('secret'), 2)
        self.assertEquals(itemPrivacies.count('public'), 3)
        # same using getNumberOfItems
        self.assertEquals(meeting.adapted().getNumberOfItems(itemUids, privacy='secret'), 2)
        self.assertEquals(meeting.adapted().getNumberOfItems(itemUids, privacy='public'), 3)

        # test the 'categories' parameter
        # by default, 2 items are in the 'events' category,
        # 2 are in the 'development' category
        # 1 in the 'research' category
        itemCategories = [item.getCategory() for item in orderedItems]
        self.assertEquals(itemCategories.count('events'), 2)
        self.assertEquals(itemCategories.count('development'), 2)
        self.assertEquals(itemCategories.count('research'), 1)
        # same using getNumberOfItems
        self.assertEquals(meeting.adapted().getNumberOfItems(itemUids, categories=['events', ]), 2)
        self.assertEquals(meeting.adapted().getNumberOfItems(itemUids, categories=['development', ]), 2)
        # we can pass several categories
        self.assertEquals(meeting.adapted().getNumberOfItems(itemUids,
                                                             categories=['dummycategory', 'research', 'development', ]),
                          3)

        # test the 'late' parameter
        # by default, no items are late so make 2 late items
        # remove to items, freeze the meeting then add the items
        item1 = orderedItems[0]
        item2 = orderedItems[1]
        self.backToState(item1, 'proposed')
        self.backToState(item2, 'proposed')
        self.freezeMeeting(meeting)
        item1.setPreferredMeeting(meeting.UID())
        item2.setPreferredMeeting(meeting.UID())
        self.presentItem(item1)
        self.presentItem(item2)
        # now we have 4 normal items and 2 late items
        self.assertEquals(len(meeting.getItems()), 3)
        self.assertEquals(len(meeting.getLateItems()), 2)
        # same using getNumberOfItems
        self.assertEquals(meeting.adapted().getNumberOfItems(itemUids, late=False), 3)
        self.assertEquals(meeting.adapted().getNumberOfItems(itemUids, late=True), 2)

        # we can combinate parameters
        # we know that we have 2 late items that are using the 'development' category...
        lateItems = meeting.getLateItems()
        self.assertEquals(len(lateItems), 2)
        self.assertEquals(lateItems[0].getCategory(), 'development')
        self.assertEquals(lateItems[1].getCategory(), 'development')
        self.assertEquals(meeting.adapted().getNumberOfItems(itemUids, categories=['development', ], late=True), 2)
        # we have so 0 normal item using the 'development' category
        self.assertEquals(meeting.adapted().getNumberOfItems(itemUids, categories=['development', ], late=False), 0)
