# -*- coding: utf-8 -*-
#
# File: testToolPloneMeeting.py
#
# GNU General Public License (GPL)
#

from imio.helpers.content import get_vocab_values
from imio.helpers.content import richtextval
from plone.dexterity.utils import createContentInContainer
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.tests.testToolPloneMeeting import testToolPloneMeeting as pmtt


class testToolPloneMeeting(MeetingCommunesTestCase, pmtt):
    '''Tests the ToolPloneMeeting class methods.'''

    def test_pm_FinancesAdvisersConfig(self):
        """Test concrete usecase with ToolPloneMeeting.advisersConfig and
           meetingadvicefinances portal_type and meetingadvicefinancessimple_workflow."""
        # configure financesadvice so meetingadvicefinances portal_type is available
        # as well as the meetingadvicefinancessimple_workflow
        self._configureFinancesAdvice()
        cfg = self.meetingConfig
        cfg.setItemAdviceStates((self._stateMappingFor('itemcreated'), ))
        cfg.setItemAdviceEditStates((self._stateMappingFor('itemcreated'), ))
        cfg.setItemAdviceViewStates((self._stateMappingFor('itemcreated'), ))
        self.tool.setAdvisersConfig(
            ({'advice_types': ['positive',
                               'positive_with_remarks'],
              'base_wf': 'meetingadvicefinancessimple_workflow',
              'default_advice_type': 'positive_with_remarks',
              'org_uids': [self.vendors_uid],
              'portal_type': 'meetingadvicefinances',
              'show_advice_on_final_wf_transition': '1',
              'wf_adaptations': []}, ))
        self.tool.at_post_edit_script()
        # create item and ask 2 advices
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem',
                           title="Item to advice",
                           category='development',
                           optionalAdvisers=(self.vendors_uid, self.developers_uid, ))
        # advice are giveable
        self.changeUser('pmAdviser1')
        dev_advice = createContentInContainer(
            item,
            item.adapted()._advicePortalTypeForAdviser(self.developers_uid),
            **{'advice_group': self.developers_uid,
               'advice_type': u'positive',
               'advice_comment': richtextval(u'My comment')})
        self.changeUser('pmReviewer2')
        vendors_advice = createContentInContainer(
            item,
            item.adapted()._advicePortalTypeForAdviser(self.vendors_uid),
            **{'advice_group': self.vendors_uid,
               'advice_type': u'positive_with_remarks',
               'advice_comment': richtextval(u'My comment')})
        # dev_advice is a meetingadvice and use global config advice types
        self.assertEqual(
            get_vocab_values(
                dev_advice,
                'Products.PloneMeeting.content.advice.advice_type_vocabulary'),
            ['positive', 'positive_with_remarks', 'negative', 'nil'])
        # vendors_advice is a meetingadvicefinances and use what is defined in
        # ToolPloneMeeting.advisersConfig.advice_types
        self.assertEqual(
            get_vocab_values(
                vendors_advice,
                'Products.PloneMeeting.content.advice.advice_type_vocabulary'),
            ['positive', 'positive_with_remarks'])
        # unselected values are taken into account
        vendors_advice.advice_type = 'negative'
        self.assertEqual(
            get_vocab_values(
                vendors_advice,
                'Products.PloneMeeting.content.advice.advice_type_vocabulary'),
            ['positive', 'positive_with_remarks', 'negative'])
        # when advice is given, it is automatically shown
        self.assertFalse(vendors_advice.advice_hide_during_redaction)
        vendors_advice.advice_hide_during_redaction = True
        item.update_local_roles()
        self.assertTrue(vendors_advice.advice_hide_during_redaction)
        self.assertTrue(item.adviceIndex[self.vendors_uid]['hidden_during_redaction'])
        self.changeUser('pmCreator1')
        self.proposeItem(item)
        self.assertFalse(vendors_advice.advice_hide_during_redaction)
        self.assertFalse(item.adviceIndex[self.vendors_uid]['hidden_during_redaction'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testToolPloneMeeting, prefix='test_pm_'))
    return suite
