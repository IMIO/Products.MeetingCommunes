# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.MeetingCommunes.config import FINANCE_ADVICES_COLLECTION_ID
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.indexes import REAL_ORG_UID_PATTERN


class testCustomMeetingItem(MeetingCommunesTestCase):
    """
        Tests the MeetingItem adapted methods
    """

    def test_GetUsedFinanceGroupIds(self):
        '''Test the custom MeetingItem.getUsedFinanceGroupIds method
           that will return adviser ids used on the FINANCE_ADVICES_COLLECTION_ID
           collection, this is used in the adapted method 'showFinanceAdviceTemplate'.'''
        cfg = self.meetingConfig
        cfg.setUseAdvices(True)
        cfg2 = self.meetingConfig2
        cfg2.setUseAdvices(True)
        cfg2Id = cfg2.getId()
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
        cfg2.setCustomAdvisers([
            {'row_id': 'unique_id_001_2',
             'org': self.developers_uid,
             'for_item_created_from': today,
             'delay': '10',
             'delay_left_alert': '4',
             'delay_label': 'Finance advice 1',
             'is_linked_to_previous_row': '0'},
            {'row_id': 'unique_id_002_2',
             'org': self.developers_uid,
             'for_item_created_from': today,
             'delay': '20',
             'delay_left_alert': '4',
             'delay_label': 'Finance advice 2',
             'is_linked_to_previous_row': '1'},
            {'row_id': 'unique_id_003_2',
             'org': self.developers_uid,
             'for_item_created_from': today,
             'delay': '20',
             'delay_left_alert': '4',
             'delay_label': 'Not a finance advice',
             'is_linked_to_previous_row': '0'}, ]
        )
        cfg2.setSelectableAdvisers((self.vendors_uid, self.developers_uid))
        collection2 = getattr(cfg2.searches.searches_items, FINANCE_ADVICES_COLLECTION_ID)
        # make sure collection is active
        collection2.enabled = True
        collection2.reindexObject(idxs=['enabled'])
        collection2.setQuery([
            {'i': 'portal_type',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': [cfg.getItemTypeName(), ]},
            {'i': 'indexAdvisers',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': ['delay_row_id__unique_id_001_2',
                   'delay_row_id__unique_id_002_2',
                   REAL_ORG_UID_PATTERN.format(self.developers_uid)]}
        ], )
        # create an item without finance advice
        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        # there are financeGroupIds
        self.assertEqual(cfg.adapted().getUsedFinanceGroupIds(), [self.developers_uid])
        # but not for item
        self.assertEqual(cfg.adapted().getUsedFinanceGroupIds(item), [])
        self.assertFalse(item.adapted().showFinanceAdviceTemplate())
        self.assertIsNone(item.adapted().getFinanceAdviceId())

        # ask advice of another group
        item.setOptionalAdvisers((self.vendors_uid, ))
        item._update_after_edit()
        # no usedFinanceGroupId
        self.assertEqual(cfg.adapted().getUsedFinanceGroupIds(item), [])
        self.assertFalse(item.adapted().showFinanceAdviceTemplate())
        self.assertIsNone(item.adapted().getFinanceAdviceId())

        # now ask advice of developers, considered as an non finance
        # advice as only customAdvisers are considered
        item.setOptionalAdvisers((self.developers_uid, ))
        item._update_after_edit()
        self.assertEqual(cfg.adapted().getUsedFinanceGroupIds(item), [])
        self.assertFalse(item.adapted().showFinanceAdviceTemplate())
        self.assertIsNone(item.adapted().getFinanceAdviceId())

        # right ask a custom advice that is not a finance advice this time
        item.setOptionalAdvisers(('{0}__rowid__unique_id_003'.format(self.developers_uid), ))
        item._update_after_edit()
        self.assertEqual(cfg.adapted().getUsedFinanceGroupIds(item), [])
        self.assertFalse(item.adapted().showFinanceAdviceTemplate())
        self.assertIsNone(item.adapted().getFinanceAdviceId())

        # finally ask a real finance advice, this time it will work
        item.setOptionalAdvisers(
            (self.vendors_uid,
             '{0}__rowid__unique_id_001'.format(self.developers_uid), ))
        item._update_after_edit()
        self.assertEqual(cfg.adapted().getUsedFinanceGroupIds(item),
                         [self.developers_uid])
        self.assertTrue(item.adapted().showFinanceAdviceTemplate())
        self.assertEqual(item.adapted().getFinanceAdviceId(), self.developers_uid)

        # when using inheritated advice, it works as well
        clonedItem = item.clone(setCurrentAsPredecessor=True, inheritAdvices=True)
        self.assertEqual(cfg.adapted().getUsedFinanceGroupIds(clonedItem),
                         [self.developers_uid])
        self.assertTrue(clonedItem.adapted().showFinanceAdviceTemplate())
        self.assertEqual(clonedItem.adapted().getFinanceAdviceId(), self.developers_uid)

        # and also when item sent to other MC and advice inheritated
        cfg.setItemManualSentToOtherMCStates(('itemcreated', ))
        cfg.setContentsKeptOnSentToOtherMC((u'advices', ))
        clonedItem.setOtherMeetingConfigsClonableTo((cfg2Id, ))
        clonedItem2 = clonedItem.cloneToOtherMeetingConfig(cfg2Id)
        self.assertEqual(cfg2.adapted().getUsedFinanceGroupIds(clonedItem2),
                         [self.developers_uid])
        self.assertTrue(clonedItem2.adapted().showFinanceAdviceTemplate())
        self.assertEqual(clonedItem2.adapted().getFinanceAdviceId(), self.developers_uid)
        # remove inheritance for developers_uid
        self.request['form.widgets.advice_uid'] = unicode(self.developers_uid, 'utf-8')
        self.request['form.widgets.inherited_advice_action'] = 'ask_locally'
        form = clonedItem2.restrictedTraverse('@@advice-remove-inheritance').form_instance
        form.update()
        form.handleSaveRemoveAdviceInheritance(form, None)
        self.assertTrue(clonedItem2.adapted().showFinanceAdviceTemplate())
        self.assertEqual(clonedItem2.adapted().getFinanceAdviceId(), self.developers_uid)

        # auto asked advice
        custom_advisers = list(cfg.getCustomAdvisers()) + [{
            'row_id': 'unique_id_004',
            'org': self.vendors_uid,
            'for_item_created_from': today,
            'gives_auto_advice_on': 'python: True',
            'gives_auto_advice_on_help_message': '',
            'is_linked_to_previous_row': '0'}]
        cfg.setCustomAdvisers(custom_advisers)
        auto_item = self.create('MeetingItem')
        self.assertTrue(self.vendors_uid in auto_item.adviceIndex)
        # not a finance advice for now
        self.assertFalse(auto_item.adapted().getFinanceAdviceId())
        self.assertFalse(auto_item.adapted().showFinanceAdviceTemplate())
        # make is recognized as finance advice
        query = collection.query
        query[1]['v'].append(REAL_ORG_UID_PATTERN.format(self.vendors_uid))
        collection.setQuery(query)
        self.assertEqual(auto_item.adapted().getFinanceAdviceId(), self.vendors_uid)
        self.assertTrue(auto_item.adapted().showFinanceAdviceTemplate())

        # if the collection does not exist, [] is returned
        self.deleteAsManager(collection.UID())
        self.assertEqual(cfg.adapted().getUsedFinanceGroupIds(item), [])
        self.assertFalse(item.adapted().showFinanceAdviceTemplate())
        self.assertIsNone(item.adapted().getFinanceAdviceId())
