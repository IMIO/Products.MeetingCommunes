# -*- coding: utf-8 -*-
#
# File: testViews.py
#
# GNU General Public License (GPL)
#

from DateTime import DateTime
from Products.MeetingCommunes.config import DEFAULT_FINANCE_ADVICES_TEMPLATE
from Products.MeetingCommunes.config import FINANCE_ADVICES_COLLECTION_ID
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.tests.testViews import testViews as pmtv


class testViews(MeetingCommunesTestCase, pmtv):
    ''' '''

    def test_pm_deliberation_for_restapi(self):
        """Complete test as we have additional data."""
        cfg = self.meetingConfig
        # make sure no query for now as no customAdvisers
        collection = getattr(cfg.searches.searches_items, FINANCE_ADVICES_COLLECTION_ID)
        collection.setQuery([])
        item, view, helper, data = super(testViews, self).test_pm_deliberation_for_restapi()
        self.assertEqual(data["deliberation_finance_advice"], "")
        # add a financial advice
        cfg.setItemAdviceStates((self._stateMappingFor('itemcreated'), ))
        cfg.setItemAdviceEditStates((self._stateMappingFor('itemcreated'), ))
        cfg.setItemAdviceViewStates((self._stateMappingFor('itemcreated'), ))
        cfg.setCustomAdvisers(
            [{'row_id': 'unique_id_123',
              'org': self.vendors_uid,
              'gives_auto_advice_on': '',
              'for_item_created_from': '2016/08/08',
              'delay': '5',
              'delay_label': ''}, ])
        collection.setQuery([
            {'i': 'portal_type',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': [cfg.getItemTypeName(), ]},
            {'i': 'indexAdvisers',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': ['delay_row_id__unique_id_123']}
        ], )
        item.setOptionalAdvisers((
            '{0}__rowid__unique_id_123'.format(self.vendors_uid), ))
        item._update_after_edit()
        data = helper.deliberation_for_restapi()
        localized_now = item.restrictedTraverse('@@plone').toLocalizedTime(DateTime())
        self.assertEqual(
            data["deliberation_finance_advice"],
            DEFAULT_FINANCE_ADVICES_TEMPLATE["legal_not_given"].format(
                to="au",
                adviser="Vendors",
                item_transmitted_on_localized=localized_now,
                prefix="le").encode('utf-8'))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testViews, prefix='test_pm_'))
    return suite
