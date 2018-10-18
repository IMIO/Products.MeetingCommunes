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

from collective.contact.plonegroup.utils import get_plone_group_id
from DateTime import DateTime
from plone import api
from plone.app.textfield import RichTextValue
from plone.dexterity.utils import createContentInContainer
from Products.MeetingCommunes.config import FINANCE_ADVICES_COLLECTION_ID
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.utils import getLastEvent


class testCustomViews(MeetingCommunesTestCase):
    """
        Tests the custom views
    """

    def test_PrintAllAnnexes(self):
        """ """
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        annex1 = self.addAnnex(item)
        annex2 = self.addAnnex(item, annexTitle='Annex 2')
        annex3 = self.addAnnex(item, annexTitle=u'Annex 3 with special characters h\xc3\xa9h\xc3\xa9')
        annexDecision1 = self.addAnnex(item, annexTitle='Annex decision 1', relatedTo='item_decision')

        pod_template = self.meetingConfig.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()
        self.assertEqual(
            helper.printAllAnnexes(),
            u'<p><a href="{0}">Annex</a></p>\n'
            u'<p><a href="{1}">Annex 2</a></p>\n'
            u'<p><a href="{2}">Annex 3 with special characters h\xc3\xa9h\xc3\xa9</a></p>'.format(
                annex1.absolute_url(),
                annex2.absolute_url(),
                annex3.absolute_url()))
        self.assertEqual(
            helper.printAllAnnexes(portal_types=('annexDecision',)),
            u'<p><a href="{0}">Annex decision 1</a></p>'.format(annexDecision1.absolute_url()))

    def test_print_methods(self):
        """Test various print methods :
           - print_creator_name;
           - print_item_state.
        """
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        pod_template = self.meetingConfig.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()

        # print_creator_name
        self.assertEqual(helper.print_creator_name(), 'M. PMCreator One')
        # does not fail if user not found
        item.setCreators(('unknown',))
        self.assertEqual(helper.print_creator_name(), 'unknown')

        # print_item_state
        self.assertEqual(helper.print_item_state(), u'Created')
        self.validateItem(item)
        self.assertEqual(helper.print_item_state(), u'Validated')

    def test_printFormatedAdvice(self):
        # advice are addable/editable when item is 'proposed'
        # create an item and ask advice of 'vendors'
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        item.setOptionalAdvisers((self.vendors_uid, self.developers_uid,))
        item.at_post_edit_script()
        # an advice can be given when an item is 'proposed'
        self.proposeItem(item)

        self.changeUser('pmManager')

        pod_template = self.meetingConfig.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()

        result = helper.printFormatedAdvice()
        self.assertListEqual(result, [])

        result = helper.printFormatedAdvice()
        self.assertListEqual(result, [])

        result = helper.printFormatedAdvice(exclude_not_given=False)
        # result contains every informations getAdviceDataFor returns
        self.assertEqual(
            [(u'Developers', u'Not given yet'), (u'Vendors', u'Not given yet')],
            sorted([(res['name'], res['type_translated']) for res in result]))

        # add advice for 'developers'
        self.changeUser('pmAdviser1')
        createContentInContainer(item,
                                 'meetingadvice',
                                 **{'advice_group': self.developers_uid,
                                    'advice_type': u'positive',
                                    'advice_comment': RichTextValue(u'My comment')})

        result = helper.printFormatedAdvice()
        self.assertEqual(
            [(u'Developers', u'Positive')],
            [(res['name'], res['type_translated']) for res in result])

        self.assertListEqual(helper.printFormatedAdvice(), helper.printFormatedAdvice(True))

        result = helper.printFormatedAdvice(exclude_not_given=False)
        self.assertEqual(
            [(u'Developers', u'Positive'), (u'Vendors', u'Not given yet')],
            sorted([(res['name'], res['type_translated']) for res in result]))

    def _set_up_additional_finance_advisor_group(self,
                                                 new_group_name="New Group 1",
                                                 adviser_user_id='pmAdviserNG1'):
        self.changeUser('siteadmin')
        # create a new group and make sure every Plone groups are created
        new_group = self.create('organization', title=new_group_name, acronym='N.G.')
        new_group_uid = new_group.UID()
        self._select_organization(new_group_uid)

        membershipTool = api.portal.get_tool('portal_membership')
        membershipTool.addMember(id=adviser_user_id, password='12345', roles=('Member',), domains=())

        self._addPrincipalToGroup('pmAdviserNG1', get_plone_group_id(new_group_uid, 'advisers'))
        return new_group_uid

    def _set_up_second_finance_adviser(self, adviser_group_uid):
        self.changeUser('siteadmin')
        today = DateTime().strftime('%Y/%m/%d')
        cfg = self.meetingConfig
        collection = getattr(cfg.searches.searches_items, FINANCE_ADVICES_COLLECTION_ID)
        collection.setQuery(
            [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.is', 'v': [cfg.getItemTypeName(), ]},
             {'i': 'indexAdvisers', 'o': 'plone.app.querystring.operation.selection.is',
              'v': ['delay_row_id__unique_id_001', 'delay_row_id__unique_id_002']}], )

        cfg.setCustomAdvisers((
            {'row_id': 'unique_id_001',
             'org': adviser_group_uid,
             'for_item_created_from': today,
             'delay': '10',
             'delay_left_alert': '4',
             'delay_label': 'Finance advice 1',
             'is_linked_to_previous_row': '0'},
            {'row_id': 'unique_id_002',
             'org': self.vendors_uid,
             'for_item_created_from': today,
             'delay': '10',
             'delay_left_alert': '4',
             'delay_label': 'Finance advice 1',
             'is_linked_to_previous_row': '0'},
            {'row_id': 'unique_id_003',
             'org': adviser_group_uid,
             'for_item_created_from': today,
             'delay': '20',
             'delay_left_alert': '4',
             'delay_label': 'Finance advice 2',
             'is_linked_to_previous_row': '1'},
            {'row_id': 'unique_id_004',
             'org': self.vendors_uid,
             'for_item_created_from': today,
             'delay': '20',
             'delay_left_alert': '4',
             'delay_label': 'Finance advice 2',
             'is_linked_to_previous_row': '1'},
            {'row_id': 'unique_id_005',
             'org': adviser_group_uid,
             'for_item_created_from': today,
             'delay': '20',
             'delay_left_alert': '4',
             'delay_label': 'Not a finance advice',
             'is_linked_to_previous_row': '0'},
            {'row_id': 'unique_id_006',
             'org': self.vendors_uid,
             'for_item_created_from': today,
             'delay': '20',
             'delay_left_alert': '4',
             'delay_label': 'Not a finance advice',
             'is_linked_to_previous_row': '0'},))

        cfg.setItemAdviceStates(('itemcreated',))
        cfg.setItemAdviceEditStates(('itemcreated',))
        cfg.setItemAdviceViewStates(('itemcreated',))

    def _give_advice(self, item, adviser_group_uid, adviser_user_id, advice_id='meetingadvice'):
        self.changeUser(adviser_user_id)
        createContentInContainer(
            item, advice_id,
            **{'advice_group': adviser_group_uid,
               'advice_type': u'positive',
               'advice_hide_during_redaction': False,
               'advice_comment': RichTextValue(u'My comment')})

    def test_getItemAdviceTransmissionDate(self):
        cfg = self.meetingConfig
        self.changeUser('siteadmin')
        cfg.powerAdvisersGroups = (self.vendors_uid,)
        cfg.setItemAdviceStates(('validated',))
        cfg.setItemAdviceEditStates(('validated',))
        cfg.setItemAdviceViewStates(('validated',))

        collection = getattr(cfg.searches.searches_items, FINANCE_ADVICES_COLLECTION_ID)
        collection.setQuery(
            [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.is',
              'v': [cfg.getItemTypeName(), ]},
             {'i': 'indexAdvisers', 'o': 'plone.app.querystring.operation.selection.is',
              'v': []}], )
        today = DateTime().strftime('%Y/%m/%d')
        cfg.setCustomAdvisers((
            {'row_id': 'unique_id_002',
             'org': self.vendors_uid,
             'for_item_created_from': today,
             'delay': '10',
             'delay_left_alert': '4',
             'delay_label': 'Finance advice 1',
             'is_linked_to_previous_row': '0'},
            {'row_id': 'unique_id_004',
             'org': self.vendors_uid,
             'for_item_created_from': today,
             'delay': '20',
             'delay_left_alert': '4',
             'delay_label': 'Finance advice 2',
             'is_linked_to_previous_row': '1'},
            {'row_id': 'unique_id_006',
             'org': self.vendors_uid,
             'for_item_created_from': today,
             'delay': '20',
             'delay_left_alert': '4',
             'delay_label': 'Not a finance advice',
             'is_linked_to_previous_row': '0'},))

        self.changeUser('pmCreator1')

        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item = self.create('MeetingItem', **data)
        item.setOptionalAdvisers((self.developers_uid, '{0}__rowid__unique_id_002'.format(self.vendors_uid)))
        item.at_post_edit_script()

        pod_template = cfg.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()
        # test no finance id available
        self.assertIsNone(helper._getItemAdviceTransmissionDate())

        # test no delay available
        collection.setQuery(
            [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.is',
              'v': [cfg.getItemTypeName(), ]},
             {'i': 'indexAdvisers', 'o': 'plone.app.querystring.operation.selection.is',
              'v': ['delay_row_id__unique_id_002']}], )
        self.assertIsNone(helper._getItemAdviceTransmissionDate())

        # test delay started from WF
        self.changeUser('siteadmin')
        self.proposeItem(item)
        cfg.setItemAdviceStates(('proposed', 'validated',))
        cfg.setItemAdviceEditStates(('proposed', 'validated',))
        cfg.setItemAdviceViewStates(('proposed', 'validated',))
        self.assertEqual(helper._getItemAdviceTransmissionDate(), getLastEvent(item, 'propose')['time'])

        # test delay started regular way
        cfg.setItemAdviceStates(('validated',))
        cfg.setItemAdviceEditStates(('validated',))
        cfg.setItemAdviceViewStates(('validated',))
        self.validateItem(item)
        self.assertEqual(helper._getItemAdviceTransmissionDate(),
                         item.getAdviceDataFor(item, self.vendors_uid)['delay_started_on'])

    def handle_finance_cases(self, case_to_test, helper):
        cases = ['simple', 'legal_not_given', 'simple_not_given', 'legal', 'initiative']
        other_cases = list(cases)
        other_cases.remove(case_to_test)

        for case in other_cases:
            result = helper.printFinanceAdvice(case)
            self.assertListEqual(result, [])
            result = helper.printFinanceAdvice([case])
            self.assertListEqual(result, [])

        result = helper.printFinanceAdvice(other_cases)
        self.assertEqual(result, [])
        result = helper.printFinanceAdvice(cases)
        self.assertEqual(len(result), 2)

    def test_printFinanceAdvice_case_simple(self):
        cfg = self.meetingConfig
        # creator for group 'developers'
        self.changeUser('pmCreator1')
        # create an item and ask the advice of group 'vendors'
        new_group_uid = self._set_up_additional_finance_advisor_group()
        self._set_up_second_finance_adviser(new_group_uid)

        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item1 = self.create('MeetingItem', **data)
        item1._update_after_edit()

        pod_template = cfg.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item1.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()

        # Advice not asked
        result = helper.printFinanceAdvice('simple')
        self.assertEqual(result, [])
        result = helper.printFinanceAdvice(['simple'])
        self.assertEqual(result, [])

        item1.setOptionalAdvisers((self.vendors_uid,))
        item1._update_after_edit()

        # No advice given
        result = helper.printFinanceAdvice('simple')
        self.assertEqual(result, [])
        result = helper.printFinanceAdvice(['simple'])
        self.assertEqual(result, [])

        # 1 Advice given
        self._give_advice(item1, self.vendors_uid, 'pmReviewer2')
        result = helper.printFinanceAdvice('simple')
        self.assertEqual(len(result), 1)
        result = helper.printFinanceAdvice(['simple'])
        self.assertEqual(len(result), 1)

        self.changeUser('pmCreator1')
        item1.setOptionalAdvisers((new_group_uid, self.vendors_uid, self.developers_uid))
        item1._update_after_edit()

        self._give_advice(item1, self.developers_uid, 'pmAdviser1')
        result = helper.printFinanceAdvice('simple')
        self.assertEqual(len(result), 1)
        result = helper.printFinanceAdvice(['simple'])
        self.assertEqual(len(result), 1)

        self._give_advice(item1, new_group_uid, 'pmAdviserNG1')
        result = helper.printFinanceAdvice('simple')
        self.assertEqual(len(result), 2)
        result = helper.printFinanceAdvice(['simple'])
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('simple', helper)

    def test_printFinanceAdvice_case_simple_not_given(self):
        cfg = self.meetingConfig
        # creator for group 'developers'
        self.changeUser('pmCreator1')

        new_group_uid = self._set_up_additional_finance_advisor_group()
        self._set_up_second_finance_adviser(new_group_uid)

        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item1 = self.create('MeetingItem', **data)
        item1._update_after_edit()

        pod_template = cfg.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item1.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()

        # Advice not asked
        result = helper.printFinanceAdvice('simple_not_given')
        self.assertEqual(result, [])

        item1.setOptionalAdvisers((self.vendors_uid, new_group_uid))
        item1._update_after_edit()

        # No advice given
        result = helper.printFinanceAdvice('simple_not_given')
        self.assertEqual(len(result), 2)

        # 1 Advice given
        self._give_advice(item1, self.vendors_uid, 'pmReviewer2')
        result = helper.printFinanceAdvice('simple_not_given')
        self.assertEqual(len(result), 1)

        # remove the advice
        item1.restrictedTraverse('@@delete_givenuid')(item1.meetingadvice.UID())
        item1._update_after_edit()
        result = helper.printFinanceAdvice('simple_not_given')
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('simple_not_given', helper)

    def test_printFinanceAdvice_case_initiative(self):
        cfg = self.meetingConfig
        new_group_uid = self._set_up_additional_finance_advisor_group()

        self._set_up_second_finance_adviser(new_group_uid)
        cfg.powerAdvisersGroups = (new_group_uid, self.vendors_uid,)

        self.changeUser('pmCreator1')
        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item1 = self.create('MeetingItem', **data)
        item1.setOptionalAdvisers(self.developers_uid)
        item1._update_after_edit()

        pod_template = cfg.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item1.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()
        result = helper.printFinanceAdvice('initiative')
        self.assertEqual(result, [])

        self._give_advice(item1, self.vendors_uid, 'pmReviewer2')
        result = helper.printFinanceAdvice('initiative')
        self.assertEqual(len(result), 1)

        self._give_advice(item1, self.developers_uid, 'pmAdviser1')
        result = helper.printFinanceAdvice('initiative')
        self.assertEqual(len(result), 1)

        self._give_advice(item1, new_group_uid, 'pmAdviserNG1')
        result = helper.printFinanceAdvice('initiative')
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('initiative', helper)

        # remove the advice
        self.changeUser('pmReviewer2')
        item1.restrictedTraverse('@@delete_givenuid')(item1.meetingadvice.UID())
        item1._update_after_edit()
        result = helper.printFinanceAdvice('initiative')
        self.assertEqual(len(result), 1)

    def test_printFinanceAdvice_case_legal(self):
        cfg = self.meetingConfig
        new_group_uid = self._set_up_additional_finance_advisor_group()

        self._set_up_second_finance_adviser(new_group_uid)
        cfg.powerAdvisersGroups = (new_group_uid, self.vendors_uid,)

        self.changeUser('pmCreator1')
        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item1 = self.create('MeetingItem', **data)
        item1.setOptionalAdvisers((self.developers_uid,
                                   self.vendors_uid + '__rowid__unique_id_002',
                                   new_group_uid + '__rowid__unique_id_003'))
        item1._update_after_edit()

        pod_template = cfg.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item1.restrictedTraverse('@@document-generation')
        view()
        helper1 = view.get_generation_context_helper()
        result = helper1.printFinanceAdvice('legal')
        self.assertEqual(result, [])

        self._give_advice(item1, self.vendors_uid, 'pmReviewer2')
        result = helper1.printFinanceAdvice('legal')
        self.assertEqual(len(result), 1)

        self._give_advice(item1, new_group_uid, 'pmAdviserNG1')
        result = helper1.printFinanceAdvice('legal')
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('legal', helper1)

        # test with power observer
        self.changeUser('siteadmin')
        cfg.powerAdvisersGroups = (new_group_uid, self.vendors_uid,)
        self.changeUser('pmCreator1')
        item2 = self.create('MeetingItem', **data)
        item2.setOptionalAdvisers((self.developers_uid,
                                   self.vendors_uid + '__rowid__unique_id_002',))
        item2._update_after_edit()

        pod_template = cfg.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item2.restrictedTraverse('@@document-generation')
        view()
        helper2 = view.get_generation_context_helper()
        result = helper2.printFinanceAdvice('legal')
        self.assertEqual(result, [])

        self._give_advice(item2, self.vendors_uid, 'pmReviewer2')
        result = helper2.printFinanceAdvice('legal')
        self.assertEqual(len(result), 1)

        self._give_advice(item2, new_group_uid, 'pmAdviserNG1')
        result = helper2.printFinanceAdvice('legal')
        self.assertEqual(len(result), 1)

    def test_printFinanceAdvice_case_legal_not_given(self):
        cfg = self.meetingConfig
        new_group_uid = self._set_up_additional_finance_advisor_group()

        self._set_up_second_finance_adviser(new_group_uid)
        cfg.powerAdvisersGroups = (new_group_uid, self.vendors_uid,)

        self.changeUser('pmCreator1')
        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item1 = self.create('MeetingItem', **data)
        item1.setOptionalAdvisers((self.developers_uid,
                                   self.vendors_uid + '__rowid__unique_id_002',
                                   new_group_uid + '__rowid__unique_id_003'))
        item1._update_after_edit()

        pod_template = cfg.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item1.restrictedTraverse('@@document-generation')
        view()
        helper1 = view.get_generation_context_helper()
        result = helper1.printFinanceAdvice('legal_not_given')

        self.assertEqual(len(result), 2)

        self._give_advice(item1, self.vendors_uid, 'pmReviewer2')
        result = helper1.printFinanceAdvice('legal_not_given')
        self.assertEqual(len(result), 1)

        self._give_advice(item1, new_group_uid, 'pmAdviserNG1')
        result = helper1.printFinanceAdvice('legal_not_given')
        self.assertEqual(result, [])

        # remove the advice
        self.changeUser('pmReviewer2')
        item1.restrictedTraverse('@@delete_givenuid')(item1.meetingadvice.UID())
        item1._update_after_edit()
        result = helper1.printFinanceAdvice('legal_not_given')
        self.assertEqual(len(result), 1)

        # remove the advice
        self.changeUser('pmAdviserNG1')
        item1.restrictedTraverse('@@delete_givenuid')(item1.getAdviceObj(new_group_uid).UID())
        item1._update_after_edit()
        result = helper1.printFinanceAdvice('legal_not_given')
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('legal_not_given', helper1)

        # test with power observer
        self.changeUser('siteadmin')
        cfg.powerAdvisersGroups = (new_group_uid, self.vendors_uid,)
        self.changeUser('pmCreator1')
        item2 = self.create('MeetingItem', **data)
        item2.setOptionalAdvisers((self.developers_uid,
                                   self.vendors_uid + '__rowid__unique_id_002',))
        item2._update_after_edit()

        pod_template = cfg.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item2.restrictedTraverse('@@document-generation')
        view()
        helper2 = view.get_generation_context_helper()
        result = helper2.printFinanceAdvice('legal_not_given')
        self.assertEqual(len(result), 1)

        self._give_advice(item2, self.vendors_uid, 'pmReviewer2')
        result = helper2.printFinanceAdvice('legal_not_given')
        self.assertEqual(result, [])

        self._give_advice(item2, new_group_uid, 'pmAdviserNG1')
        result = helper2.printFinanceAdvice('legal_not_given')
        self.assertEqual(result, [])

    def test__filter_items(self):
        cfg = self.meetingConfig
        self.changeUser('pmManager')
        cfg.setUseGroupsAsCategories(False)
        cfg.setInsertingMethodsOnAddItem(
            ({'insertingMethod': 'on_categories', 'reverse': '0'},))
        m = self._createMeetingWithItems()
        # adapt categories to have catid and item to have category
        for item in m.getItems(ordered=True):
            item.setCategory('development')
        # intel inside *Joke*
        i5 = self.create('MeetingItem', title='Item5')
        i5.setCategory('development')
        i7 = self.create('MeetingItem', title='Item7')
        i7.setCategory('research')
        self.presentItem(i5)
        self.presentItem(i7)
        # create view obj
        # first, get template to use view
        pod_template = cfg.podtemplates.agendaTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = m.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()
        items = m.getItems(ordered=True)

        res = helper._filter_items(items,
                                   included_values={},
                                   excluded_values={})
        self.assertListEqual(res, items)

        res = helper._filter_items(
            items,
            included_values={},
            excluded_values={'category': [i7.getCategory(theObject=True).Title()]})
        self.assertListEqual(res, items[0:-1])

        res = helper._filter_items(
            items,
            included_values={'category': [i5.getCategory(theObject=True).Title()]},
            excluded_values={'category': [i7.getCategory(theObject=True).Title()]})
        self.assertListEqual(res, items[0:-1])

        res = helper._filter_items(
            items,
            included_values={'category': [i5.getCategory(theObject=True).Title()]},
            excluded_values={})
        self.assertListEqual(res, items[0:-1])

        res = helper._filter_items(
            items,
            included_values={'category': [i5.getCategory(theObject=True).Title()]},
            excluded_values={'category': [i5.getCategory(theObject=True).Title()]})
        self.assertListEqual(res, [])

    def test_get_grouped_items(self):
        self.changeUser('pmManager')
        cfg = self.meetingConfig
        cfg.setUseGroupsAsCategories(False)
        cfg.setInsertingMethodsOnAddItem(
            ({'insertingMethod': 'on_categories', 'reverse': '0'},))
        m = self._createMeetingWithItems()
        # adapt categories to have catid and item to have category
        for item in m.getItems(ordered=True):
            item.setCategory('development')
        # intel inside *Joke*
        i5 = self.create('MeetingItem', title='Item5')
        i5.setCategory('development')
        i7 = self.create('MeetingItem', title='Item7')
        i7.setCategory('research')
        self.presentItem(i5)
        self.presentItem(i7)
        # create view obj
        # first, get template to use view
        pod_template = cfg.podtemplates.agendaTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = m.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()
        items = m.getItems(ordered=True)
        itemUids = [anItem.UID() for anItem in items]

        res = helper.get_grouped_items(itemUids)
        self.assertListEqual(res, items)

        res = helper.get_grouped_items(itemUids, group_by='category')
        self.assertListEqual(
            res,
            [[i5.getCategory(theObject=True).Title(), items[0:-1]],
             [i7.getCategory(theObject=True).Title(), [i7]]])

    def test_get_multiple_level_printing(self):
        self.changeUser('pmManager')
        cfg = self.meetingConfig
        cfg.setUseGroupsAsCategories(False)
        cfg.setInsertingMethodsOnAddItem(
            ({'insertingMethod': 'on_categories', 'reverse': '0'},))
        m = self._createMeetingWithItems()
        # adapt categories to have catid and item to have category
        for item in m.getItems(ordered=True):
            item.setCategory('development')
        # intel inside *Joke*
        i5 = self.create('MeetingItem', title='Item5')
        i5.setCategory('development')
        i5.getCategory(theObject=True).setCategoryId('A.1.2.1.1')
        i5.getCategory(theObject=True).setDescription('DESCRI1|DESCRI2|DESCRI3')
        i7 = self.create('MeetingItem', title='Item7')
        i7.setCategory('research')
        i7.getCategory(theObject=True).setCategoryId('B.1')
        i7.getCategory(theObject=True).setDescription('')
        self.presentItem(i5)
        self.presentItem(i7)
        # create view obj
        # first, get template to use view
        pod_template = cfg.podtemplates.agendaTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = m.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()
        # test on the meeting
        # we should have a ordereddic containing 3 lists, 6 list by category
        # build the list of uids
        items = m.getItems(ordered=True)
        itemUids = [anItem.UID() for anItem in items]
        ordered_dico = helper.get_multiple_level_printing(itemUids=itemUids, level_number=5)
        self.assertEquals(len(ordered_dico), 7)
        self.assertEquals(
            ordered_dico.items(),
            [('<h1>A</h1>', []),
             ('<h2>A.1. DESCRI1</h2>', []),
             ('<h3>A.1.2. DESCRI2</h3>', []),
             ('<h4>A.1.2.1. DESCRI3</h4>', []),
             ('<h5>Development topics</h5>',
              [('A.1.2.1.1.1', items[0]),
               ('A.1.2.1.1.2', items[1]),
               ('A.1.2.1.1.3', items[2]),
               ('A.1.2.1.1.4', items[3]),
               ('A.1.2.1.1.5', items[4]),
               ('A.1.2.1.1.6', i5)]),
             ('<h1>B</h1>', []),
             ('<h2>Research topics</h2>',
              [('B.1.1', i7)])]
        )

    def test_print_item_number_within_category(self):
        cfg = self.meetingConfig
        cfg.setUseGroupsAsCategories(True)

        def create_and_validate_item(creator, preffered_meeting=None):
            self.changeUser(creator)
            item = self.create('MeetingItem')
            self.validateItem(item)
            if preffered_meeting:
                item.setPreferredMeeting(preffered_meeting)
            return item

        def get_item_view(item):
            pod_template = cfg.podtemplates.itemTemplate
            self.request.set('template_uid', pod_template.UID())
            self.request.set('output_format', 'odt')
            view = item.restrictedTraverse('@@document-generation')
            view()
            return view.get_generation_context_helper()

        self.changeUser('pmManager')
        meeting = self.create('Meeting', date=DateTime('2015/12/12'))

        test1 = create_and_validate_item('pmCreator1')
        helper1 = get_item_view(test1)
        test2 = create_and_validate_item('pmCreator2')
        helper2 = get_item_view(test2)

        self.presentItem(create_and_validate_item('pmCreator1'))
        self.presentItem(create_and_validate_item('pmCreator2'))
        self.presentItem(test1)
        self.presentItem(create_and_validate_item('pmCreator2'))
        self.presentItem(create_and_validate_item('pmCreator1'))
        self.presentItem(test2)

        self.freezeMeeting(meeting)

        test3 = create_and_validate_item('pmCreator1', meeting.UID())
        helper3 = get_item_view(test3)
        test4 = create_and_validate_item('pmCreator2', meeting.UID())
        helper4 = get_item_view(test4)

        self.presentItem(test3)
        self.presentItem(create_and_validate_item('pmCreator2', meeting.UID()))
        self.presentItem(create_and_validate_item('pmCreator1', meeting.UID()))
        self.presentItem(create_and_validate_item('pmCreator2', meeting.UID()))
        self.presentItem(create_and_validate_item('pmCreator1', meeting.UID()))
        self.presentItem(test4)

        self.assertEquals(helper1.print_item_number_within_category(), '4')
        self.assertEquals(helper2.print_item_number_within_category(), '3')
        self.assertEquals(helper3.print_item_number_within_category(), '6')
        self.assertEquals(helper4.print_item_number_within_category(), '6')

        self.assertEquals(helper3.print_item_number_within_category(listTypes=['late']), '1')
        self.assertEquals(helper4.print_item_number_within_category(listTypes=['late']), '3')

        self.assertEquals(helper3.print_item_number_within_category(listTypes=['normal']), '')
        self.assertEquals(helper4.print_item_number_within_category(listTypes=['normal']), '')

        self.assertEquals(helper3.print_item_number_within_category(listTypes=['normal'], default='XXXX'), 'XXXX')
        self.assertEquals(helper4.print_item_number_within_category(listTypes=['normal'], default='ERROR'), 'ERROR')
