# -*- coding: utf-8 -*-
#
# File: testCustomMeetingItem.py
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

from DateTime import DateTime
from Products.MeetingCommunes.config import FINANCE_ADVICES_COLLECTION_ID
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase


class testCustomMeetingItem(MeetingCommunesTestCase):
    """
        Tests the MeetingItem adapted methods
    """

    def test_GetUsedFinanceGroupIds(self):
        '''Test the custom MeetingItem.getUsedFinanceGroupIds method
           that will return adviser ids used on the FINANCE_ADVICES_COLLECTION_ID
           collection, this is used in the adapted method 'showFinanceAdviceTemplate'.'''
        cfg = self.meetingConfig
        collection = getattr(cfg.searches.searches_items, FINANCE_ADVICES_COLLECTION_ID)
        # make sure collection is active
        if not collection.enabled:
            collection.enabled = True
            collection.reindexObject(idxs=['enabled'])

        collection.setQuery([
            {'i': 'portal_type',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': [cfg.getItemTypeName(), ]},
            {'i': 'indexAdvisers',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': ['delay_row_id__unique_id_001',
                   'delay_row_id__unique_id_002']}
        ], )
        today = DateTime().strftime('%Y/%m/%d')
        cfg.setCustomAdvisers([
            {'row_id': 'unique_id_001',
             'org': self.developers_uid,
             'for_item_created_from': today,
             'delay': '10',
             'delay_left_alert': '4',
             'delay_label': 'Finance advice 1',
             'is_linked_to_previous_row': '0'},
            {'row_id': 'unique_id_002',
             'org': self.developers_uid,
             'for_item_created_from': today,
             'delay': '20',
             'delay_left_alert': '4',
             'delay_label': 'Finance advice 2',
             'is_linked_to_previous_row': '1'},
            {'row_id': 'unique_id_003',
             'org': self.developers_uid,
             'for_item_created_from': today,
             'delay': '20',
             'delay_left_alert': '4',
             'delay_label': 'Not a finance advice',
             'is_linked_to_previous_row': '0'}, ]
        )
        # create an item without finance advice
        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        # there are financeGroupIds
        self.assertEquals(cfg.adapted().getUsedFinanceGroupIds(), [self.developers_uid])
        # but not for item
        self.assertEquals(cfg.adapted().getUsedFinanceGroupIds(item), [])
        self.assertFalse(item.adapted().showFinanceAdviceTemplate())

        # ask advice of another group
        item.setOptionalAdvisers((self.vendors_uid, ))
        item._update_after_edit()
        # no usedFinanceGroupId
        self.assertEquals(cfg.adapted().getUsedFinanceGroupIds(item), [])
        self.assertFalse(item.adapted().showFinanceAdviceTemplate())

        # now ask advice of developers, considered as an non finance
        # advice as only customAdvisers are considered
        item.setOptionalAdvisers((self.developers_uid, ))
        item._update_after_edit()
        self.assertEquals(cfg.adapted().getUsedFinanceGroupIds(item), [])
        self.assertFalse(item.adapted().showFinanceAdviceTemplate())

        # right ask a custom advice that is not a finance advice this time
        item.setOptionalAdvisers(('{0}__rowid__unique_id_003'.format(self.developers_uid), ))
        item._update_after_edit()
        self.assertEquals(cfg.adapted().getUsedFinanceGroupIds(item), [])
        self.assertFalse(item.adapted().showFinanceAdviceTemplate())

        # finally ask a real finance advice, this time it will work
        item.setOptionalAdvisers(('{0}__rowid__unique_id_001'.format(self.developers_uid), ))
        item._update_after_edit()
        self.assertEquals(cfg.adapted().getUsedFinanceGroupIds(item), [self.developers_uid])
        self.assertTrue(item.adapted().showFinanceAdviceTemplate())

        # if the collection does not exist, [] is returned
        self.deleteAsManager(collection.UID())
        self.assertEquals(cfg.adapted().getUsedFinanceGroupIds(item), [])
        self.assertFalse(item.adapted().showFinanceAdviceTemplate())
