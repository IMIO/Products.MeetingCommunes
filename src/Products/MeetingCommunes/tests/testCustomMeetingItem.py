# -*- coding: utf-8 -*-

from DateTime import DateTime
from imio.helpers.content import get_vocab_values
from imio.helpers.content import richtextval
from plone.dexterity.utils import createContentInContainer
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
        cfg.setItemAdviceStates((self._stateMappingFor('itemcreated'), ))
        cfg.setItemAdviceEditStates((self._stateMappingFor('itemcreated'), ))
        cfg.setItemAdviceViewStates((self._stateMappingFor('itemcreated'), ))
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
                   'real_org_uid__{0}'.format(self.developers_uid)]}
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

        # showFinanceAdviceTemplate when ignore_advice_hidden_during_redaction=True
        # will hide the document to people ouside _advisers group or not MeetingManagers
        # add advice so it may be set hidden
        self.changeUser('pmAdviser1')
        self.assertEqual(cfg.adapted().getUsedFinanceGroupIds(item), [self.developers_uid])
        advice = createContentInContainer(
            item,
            item.adapted()._advicePortalTypeForAdviser(self.developers_uid),
            **{'advice_group': self.developers_uid,
               'advice_type': u'positive',
               'advice_comment': richtextval(u'My comment'),
               'advice_hide_during_redaction': True})
        # advisers always True
        self.assertTrue(item.adapted().showFinanceAdviceTemplate(False))
        self.assertTrue(item.adapted().showFinanceAdviceTemplate(True))
        # pmManager always True
        self.changeUser('pmManager')
        self.assertTrue(item.adapted().showFinanceAdviceTemplate(False))
        self.assertTrue(item.adapted().showFinanceAdviceTemplate(True))
        # proposingGroup member will only get True when advice is not hidden
        self.changeUser('pmCreator1')
        self.assertTrue(item.adapted().showFinanceAdviceTemplate(False))
        self.assertFalse(item.adapted().showFinanceAdviceTemplate(True))
        # always True if advice not hidden
        advice.advice_hide_during_redaction = False
        item.update_local_roles()
        self.assertTrue(item.adapted().showFinanceAdviceTemplate(False))
        self.assertTrue(item.adapted().showFinanceAdviceTemplate(True))

        # if the collection does not exist, [] is returned
        self.deleteAsManager(collection.UID())
        self.assertEqual(cfg.adapted().getUsedFinanceGroupIds(item), [])
        self.assertFalse(item.adapted().showFinanceAdviceTemplate())
        self.assertIsNone(item.adapted().getFinanceAdviceId())

    def test_Get_advice_given_by(self):
        '''Test the AdviceInfos.get_advice_given_by when using 'meetingadvicefinances' workflow.'''

        # ease override by subproducts
        if not self._check_wfa_available(['add_advicecreated_state'], related_to="MeetingAdvice"):
            return

        self._configureFinancesAdvice(enable_add_advicecreated=True)
        item, advice = self._setupItemWithAdvice()
        view = item.restrictedTraverse('@@advice-infos')
        view(advice.advice_group, False, item.adapted().getCustomAdviceMessageFor(advice))
        # advice did not reach final state, we do not know who gave it
        self.assertIsNone(view.get_advice_given_by())
        self.do(advice, "proposeToFinancialManager")
        self.assertIsNone(view.get_advice_given_by())
        self.do(advice, "signFinancialAdvice")
        self.assertEqual(view.get_advice_given_by(), u'M. PMReviewer Two')
        # still viewable after
        self.validateItem(item)
        self.assertFalse(item.adviceIndex[self.vendors_uid]['advice_editable'])
        self.assertEqual(view.get_advice_given_by(), u'M. PMReviewer Two')
