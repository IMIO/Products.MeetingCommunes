# -*- coding: utf-8 -*-
#
# File: testCustomMeeting.py
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase


class testCustomMeetingType(MeetingCommunesTestCase):
    """
        Tests the Meeting adapted methods
    """
    def test_InitializeDecisionField(self):
        """
            In the doDecide method, we initialize the Decision field to a default value made of
            Title+Description if the field is empty...
        """
        # make sure we are not hit by any other xhtmlTransformations
        cfg = self.meetingConfig
        cfg.setXhtmlTransformTypes(())
        # check that it works
        # check that if the field contains something, it is not intialized again
        self.changeUser('pmManager')
        # create some items
        # empty decision
        i1 = self.create('MeetingItem', title='Item1', description="<p>Description Item1</p>")
        i1.setDecision("")
        i1.setProposingGroup(self.developers_uid)
        # decision field is already filled
        i2 = self.create('MeetingItem', title='Item2', description="<p>Description Item2</p>")
        i2.setDecision("<p>Decision Item2</p>")
        i2.setProposingGroup(self.developers_uid)
        # create an item with the default Kupu empty value
        i3 = self.create('MeetingItem', title='Item3', description="<p>Description Item3</p>")
        i3.setDecision("<p>&nbsp;</p>")
        i3.setProposingGroup(self.developers_uid)
        meeting = self.create('Meeting')
        # present every items in the meeting
        items = (i1, i2, i3)
        for item in items:
            self.presentItem(item)
        # check the decision field of every item
        self.assertTrue(i1.getDecision(keepWithNext=False) == "")
        self.assertTrue(i2.getDecision(keepWithNext=False) == '<p>Decision Item2</p>')
        self.assertTrue(i3.getDecision(keepWithNext=False) == '<p>&nbsp;</p>')
        # if cfg.initItemDecisionIfEmptyOnDecide is False, the decision field is not initialized
        cfg.setInitItemDecisionIfEmptyOnDecide(False)
        self.decideMeeting(meeting)
        self.assertTrue(i1.getDecision(keepWithNext=False) == "")
        self.assertTrue(i2.getDecision(keepWithNext=False), '<p>Decision Item2</p>')
        # a complex HTML is not 'touched'
        self.assertTrue(i3.getDecision(keepWithNext=False), '<p>&nbsp;</p>')
        # now if cfg.initItemDecisionIfEmptyOnDecide is True
        # fields will be initialized
        cfg.setInitItemDecisionIfEmptyOnDecide(True)
        # decide the meeting again
        self.backToState(meeting, 'created')
        self.decideMeeting(meeting)
        # i1 should contains now the concatenation of title and description
        self.assertEqual(i1.getDecision(keepWithNext=False), '<p>Item1</p><p>Description Item1</p>')
        # i2 sould not have changed
        self.assertEqual(i2.getDecision(keepWithNext=False), '<p>Decision Item2</p>')
        # i3 is initlaized because the decision field contained an empty_value
        self.assertEqual(i3.getDecision(keepWithNext=False), '<p>Item3</p><p>Description Item3</p>')

    def test_GetNumberOfItems(self):
        """
          This method will return a certain number of items depending on passed paramaters.
        """
        self.changeUser('admin')
        # make categories available
        self.setMeetingConfig(self.meetingConfig2.getId())
        self.changeUser('pmManager')
        meeting = self._createMeetingWithItems()
        orderedItems = meeting.get_items(ordered=True)
        # the meeting is created with 5 items
        self.assertEqual(len(orderedItems), 5)
        itemUids = [item.UID() for item in orderedItems]
        # without parameters, every items are returned
        self.assertEqual(meeting.adapted().getNumberOfItems(itemUids), 5)

        # test the 'privacy' parameter
        # by default, 2 items are 'secret' and 3 are 'public'
        itemPrivacies = [item.getPrivacy() for item in orderedItems]
        self.assertEqual(itemPrivacies.count('secret'), 2)
        self.assertEqual(itemPrivacies.count('public'), 3)
        # same using getNumberOfItems
        self.assertEqual(meeting.adapted().getNumberOfItems(itemUids, privacy='secret'), 2)
        self.assertEqual(meeting.adapted().getNumberOfItems(itemUids, privacy='public'), 3)

        # test the 'categories' parameter
        # by default, 2 items are in the 'events' category,
        # 2 are in the 'development' category
        # 1 in the 'research' category
        itemCategories = [item.getCategory() for item in orderedItems]
        self.assertEqual(itemCategories.count('events'), 2)
        self.assertEqual(itemCategories.count('development'), 2)
        self.assertEqual(itemCategories.count('research'), 1)
        # same using getNumberOfItems
        self.assertEqual(meeting.adapted().getNumberOfItems(itemUids, categories=['events', ]), 2)
        self.assertEqual(meeting.adapted().getNumberOfItems(itemUids, categories=['development', ]), 2)
        # we can pass several categories
        self.assertEqual(
            meeting.adapted().getNumberOfItems(
                itemUids, categories=['dummycategory', 'research', 'development', ]),
            3)

        # test the 'classifier' parameter
        # by default, 2 items are in the 'classifier1' category,
        # 2 are in the 'classifier2' category
        # 1 in the 'classifier3' category
        item_classifiers = [item.getClassifier() for item in orderedItems]
        self.assertEqual(item_classifiers.count('classifier1'), 2)
        self.assertEqual(item_classifiers.count('classifier2'), 2)
        self.assertEqual(item_classifiers.count('classifier3'), 1)

        # same using getNumberOfItems
        self.assertEqual(meeting.adapted().getNumberOfItems(itemUids, classifiers=['classifier1', ]), 2)
        self.assertEqual(meeting.adapted().getNumberOfItems(itemUids, classifiers=['classifier2', ]), 2)
        # we can pass several classifiers
        self.assertEqual(
            meeting.adapted().getNumberOfItems(
                itemUids, classifiers=['dummyclassifier', 'classifier2', 'classifier3', ]),
            3)

        # Mix multiple categories and classifiers
        self.assertEqual(
            meeting.adapted().getNumberOfItems(
                itemUids,
                categories=['research', ],
                classifiers=['classifier3', ]
            ),
            1)

        self.assertEqual(
            meeting.adapted().getNumberOfItems(
                itemUids,
                categories=['dummycategory', 'research', 'development', ],
                classifiers=['dummyclassifier', 'classifier2', 'classifier3', ]
            ),
            3)
        # test the 'late' parameter
        # by default, no items are late so make 2 late items
        # remove to items, freeze the meeting then add the items
        item1 = orderedItems[0]
        item2 = orderedItems[1]
        self.backToState(item1, 'proposed')
        self.backToState(item2, 'proposed')
        self.apply_meeting_transition_to_late_state(meeting)
        item1.setPreferredMeeting(meeting.UID())
        item2.setPreferredMeeting(meeting.UID())
        self.presentItem(item1)
        self.presentItem(item2)
        # now we have 4 normal items and 2 late items
        self.assertEqual(len(meeting.get_items()), 5)
        self.assertEqual(len(meeting.get_items(list_types=['late'])), 2)
        # same using getNumberOfItems
        self.assertEqual(meeting.adapted().getNumberOfItems(itemUids, list_types=['normal']), 3)
        self.assertEqual(meeting.adapted().getNumberOfItems(itemUids, list_types=['late']), 2)

        # we can combinate parameters
        # we know that we have 2 late items that are using the 'development' category...
        lateItems = meeting.get_items(list_types=['late'])
        self.assertEqual(len(lateItems), 2)
        self.assertEqual(lateItems[0].getCategory(), 'development')
        self.assertEqual(lateItems[1].getCategory(), 'development')
        self.assertEqual(
            meeting.adapted().getNumberOfItems(
                itemUids, categories=['development', ],
                list_types=['late']),
            2)
        # we have so 0 normal item using the 'development' category
        self.assertEqual(
            meeting.adapted().getNumberOfItems(
                itemUids, categories=['development', ], list_types=['normal']),
            0)

    def test_GetPrintableItemsByCategoryWithBothLateItems(self):
        self.changeUser('pmManager')
        self.setMeetingConfig(self.meetingConfig2.getId())
        meeting = self._createMeetingWithItems()
        orderedItems = meeting.get_items(ordered=True)
        item1 = orderedItems[0]
        item2 = orderedItems[1]
        item3 = orderedItems[2]
        self.do(item1, 'backToValidated')
        self.do(item2, 'backToValidated')
        self.do(item3, 'backToValidated')
        self.freezeMeeting(meeting)
        item1.setPreferredMeeting(meeting.UID())
        item2.setPreferredMeeting(meeting.UID())
        item3.setPreferredMeeting(meeting.UID())
        self.presentItem(item1)
        self.presentItem(item2)
        self.presentItem(item3)
        # now we have 2 normal items and 3 late items
        # 2 lates development, 1 normal and 1 late events
        # and 1 normal research
        # build the list of uids
        itemUids = [anItem.UID() for anItem in meeting.get_items(ordered=True)]
        # test on the meeting with list_types=['late','normal']
        # Every items (normal and late) should be in the same category, in the good order
        self.assertEqual(
            meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[0][0].getId(),
            'development')
        self.assertEqual(
            meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[1][0].getId(),
            'events')
        self.assertEqual(
            meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[2][0].getId(),
            'research')
        self.assertEqual(
            meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[0][0].portal_type,
            'meetingcategory')
        self.assertEqual(
            meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[1][0].portal_type,
            'meetingcategory')
        self.assertEqual(
            meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[2][0].portal_type,
            'meetingcategory')
        # the event category should have 2 items, research 1 and development 2 ( + 1 category element for each one)
        self.assertEqual(
            len(meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[0]),
            3)
        self.assertEqual(
            len(meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[1]),
            3)
        self.assertEqual(
            len(meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[2]),
            2)
        # other element of the list are MeetingItems...
        self.assertEqual(
            meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[0][1].meta_type,
            'MeetingItem')
        self.assertEqual(
            meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[0][2].meta_type,
            'MeetingItem')
        self.assertEqual(
            meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[1][1].meta_type,
            'MeetingItem')
        self.assertEqual(
            meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[1][2].meta_type,
            'MeetingItem')
        self.assertEqual(
            meeting.adapted().getPrintableItemsByCategory(
                itemUids, list_types=['late', 'normal'])[2][1].meta_type,
            'MeetingItem')
