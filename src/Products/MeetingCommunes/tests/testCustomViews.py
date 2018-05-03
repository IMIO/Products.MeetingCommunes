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

from Products.MeetingCommunes.config import FINANCE_ADVICES_COLLECTION_ID
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase

from Products.PloneMeeting.utils import getLastEvent
from DateTime import DateTime
from plone import api
from plone.app.textfield import RichTextValue
from plone.dexterity.utils import createContentInContainer


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
        item.setCreators(('unknown', ))
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
        item.setOptionalAdvisers(('vendors', 'developers',))
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

        result = helper.printFormatedAdvice(True)
        self.assertListEqual(result, [])

        result = helper.printFormatedAdvice(False)
        self.assertListEqual(result,
                             [{'type': helper.translate(msgid='not_given', domain='PloneMeeting').encode('utf-8'),
                               'name': 'Vendors',
                               'comment': ''},
                              {'type': helper.translate(msgid='not_given', domain='PloneMeeting').encode('utf-8'),
                               'name': 'Developers',
                               'comment': ''}])

        # add advice for 'developers'
        self.changeUser('pmAdviser1')
        developers_advice = createContentInContainer(item,
                                                     'meetingadvice',
                                                     **{'advice_group': 'developers',
                                                        'advice_type': u'positive',
                                                        'advice_comment': RichTextValue(u'My comment')})

        result = helper.printFormatedAdvice()
        self.assertListEqual(result, [{'type': helper.translate(msgid='positive', domain='PloneMeeting').encode('utf-8'),
                              'name': 'Developers',
                              'comment': 'My comment'}])

        self.assertListEqual(helper.printFormatedAdvice(), helper.printFormatedAdvice(True))

        result = helper.printFormatedAdvice(False)
        self.assertListEqual(result,
                             [{'type': helper.translate(msgid='positive', domain='PloneMeeting').encode('utf-8'),
                               'name': 'Developers',
                               'comment': 'My comment'},
                              {'type': helper.translate(msgid='not_given', domain='PloneMeeting').encode('utf-8'),
                               'name': 'Vendors',
                               'comment': ''}])

    def _set_up_additional_finance_advisor_group(self,
                                                 new_group_name="New Group 1",
                                                 adviser_user_id='pmAdviserNG1'):
        self.changeUser('siteadmin')
        # create a new group and make sure every Plone groups are created
        new_group = self.create('MeetingGroup', title=new_group_name, acronym='N.G.')

        new_group.at_post_edit_script()

        membershipTool = api.portal.get_tool('portal_membership')
        membershipTool.addMember(id=adviser_user_id, password='12345', roles=('Member',), domains=())

        self.portal.portal_groups.addPrincipalToGroup('pmAdviserNG1', new_group.getId() + '_advisers')
        return new_group.getId()

    def _set_up_second_finance_adviser(self, adviser_group_id):
        self.changeUser('siteadmin')
        today = DateTime().strftime('%Y/%m/%d')
        cfg = self.meetingConfig
        collection = getattr(cfg.searches.searches_items, FINANCE_ADVICES_COLLECTION_ID)
        collection.setQuery(
            [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.is', 'v': [cfg.getItemTypeName(), ]},
                {'i': 'indexAdvisers', 'o': 'plone.app.querystring.operation.selection.is',
                    'v': ['delay_real_group_id__unique_id_001', 'delay_real_group_id__unique_id_002']}], )

        cfg.setCustomAdvisers((
            {'row_id': 'unique_id_001', 'group': adviser_group_id, 'for_item_created_from': today, 'delay': '10',
                'delay_left_alert': '4', 'delay_label': 'Finance advice 1', 'is_linked_to_previous_row': '0'},
            {'row_id': 'unique_id_002', 'group': 'vendors', 'for_item_created_from': today, 'delay': '10',
                'delay_left_alert': '4', 'delay_label': 'Finance advice 1', 'is_linked_to_previous_row': '0'},
            {'row_id': 'unique_id_003', 'group': adviser_group_id, 'for_item_created_from': today, 'delay': '20',
                'delay_left_alert': '4', 'delay_label': 'Finance advice 2', 'is_linked_to_previous_row': '1'},
            {'row_id': 'unique_id_004', 'group': 'vendors', 'for_item_created_from': today, 'delay': '20',
                'delay_left_alert': '4', 'delay_label': 'Finance advice 2', 'is_linked_to_previous_row': '1'},
            {'row_id': 'unique_id_005', 'group': adviser_group_id, 'for_item_created_from': today, 'delay': '20',
                'delay_left_alert': '4', 'delay_label': 'Not a finance advice', 'is_linked_to_previous_row': '0'},
            {'row_id': 'unique_id_006', 'group': 'vendors', 'for_item_created_from': today, 'delay': '20',
                'delay_left_alert': '4', 'delay_label': 'Not a finance advice', 'is_linked_to_previous_row': '0'}, ))

        cfg.setItemAdviceStates(('itemcreated',))
        cfg.setItemAdviceEditStates(('itemcreated',))
        cfg.setItemAdviceViewStates(('itemcreated',))

    def _give_advice(self, item, adviser_group_id, adviser_user_id, advice_id='meetingadvice'):
        self.changeUser(adviser_user_id)
        createContentInContainer(
            item, advice_id,
            **{'advice_group': adviser_group_id,
               'advice_type': u'positive',
               'advice_hide_during_redaction': False,
                'advice_comment': RichTextValue(u'My comment')})

    def test_getItemFinanceAdviceTransmissionDate(self):
        self.changeUser('siteadmin')
        self.meetingConfig.powerAdvisersGroups = ('vendors',)
        self.meetingConfig.setItemAdviceStates(('validated',))
        self.meetingConfig.setItemAdviceEditStates(('validated',))
        self.meetingConfig.setItemAdviceViewStates(('validated',))

        collection = getattr(self.meetingConfig.searches.searches_items, FINANCE_ADVICES_COLLECTION_ID)
        collection.setQuery(
            [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.is', 'v': [self.meetingConfig.getItemTypeName(), ]},
             {'i': 'indexAdvisers', 'o': 'plone.app.querystring.operation.selection.is',
              'v': []}], )
        today = DateTime().strftime('%Y/%m/%d')
        self.meetingConfig.setCustomAdvisers((
            {'row_id': 'unique_id_002', 'group': 'vendors', 'for_item_created_from': today, 'delay': '10',
             'delay_left_alert': '4', 'delay_label': 'Finance advice 1', 'is_linked_to_previous_row': '0'},
            {'row_id': 'unique_id_004', 'group': 'vendors', 'for_item_created_from': today, 'delay': '20',
             'delay_left_alert': '4', 'delay_label': 'Finance advice 2', 'is_linked_to_previous_row': '1'},
            {'row_id': 'unique_id_006', 'group': 'vendors', 'for_item_created_from': today, 'delay': '20',
             'delay_left_alert': '4', 'delay_label': 'Not a finance advice', 'is_linked_to_previous_row': '0'},))

        self.changeUser('pmCreator1')

        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item = self.create('MeetingItem', **data)
        item.setOptionalAdvisers(('developers', 'vendors__rowid__unique_id_002'))
        item.at_post_edit_script()

        pod_template = self.meetingConfig.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()
        # test no finance id available
        self.assertIsNone(helper._getItemFinanceAdviceTransmissionDate())

        # test no delay available
        collection.setQuery(
            [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.is',
              'v': [self.meetingConfig.getItemTypeName(), ]},
             {'i': 'indexAdvisers', 'o': 'plone.app.querystring.operation.selection.is',
              'v': ['delay_real_group_id__unique_id_002']}], )
        self.assertIsNone(helper._getItemFinanceAdviceTransmissionDate())

        # test delay started from WF
        self.changeUser('siteadmin')
        self.proposeItem(item)
        self.meetingConfig.setItemAdviceStates(('proposed', 'validated',))
        self.meetingConfig.setItemAdviceEditStates(('proposed', 'validated',))
        self.meetingConfig.setItemAdviceViewStates(('proposed', 'validated',))
        self.assertEqual(helper._getItemFinanceAdviceTransmissionDate(), getLastEvent(item, 'propose')['time'])

        # test delay started regular way
        self.meetingConfig.setItemAdviceStates(('validated',))
        self.meetingConfig.setItemAdviceEditStates(('validated',))
        self.meetingConfig.setItemAdviceViewStates(('validated',))
        self.validateItem(item)
        self.assertEqual(helper._getItemFinanceAdviceTransmissionDate(), item.getAdviceDataFor(item, 'vendors')['delay_started_on'])


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
        # creator for group 'developers'
        self.changeUser('pmCreator1')
        # create an item and ask the advice of group 'vendors'
        new_group = self._set_up_additional_finance_advisor_group()
        self._set_up_second_finance_adviser(new_group)

        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item1 = self.create('MeetingItem', **data)
        item1.at_post_edit_script()

        pod_template = self.meetingConfig.podtemplates.itemTemplate
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

        item1.setOptionalAdvisers(('vendors',))
        item1.at_post_edit_script()

        # No advice given
        result = helper.printFinanceAdvice('simple')
        self.assertEqual(result, [])
        result = helper.printFinanceAdvice(['simple'])
        self.assertEqual(result, [])

        # 1 Advice given
        self._give_advice(item1, 'vendors', 'pmReviewer2')
        result = helper.printFinanceAdvice('simple')
        self.assertEqual(len(result), 1)
        result = helper.printFinanceAdvice(['simple'])
        self.assertEqual(len(result), 1)

        self.changeUser('pmCreator1')
        item1.setOptionalAdvisers((new_group, 'vendors', 'developers'))
        item1.at_post_edit_script()

        self._give_advice(item1, 'developers', 'pmAdviser1')
        result = helper.printFinanceAdvice('simple')
        self.assertEqual(len(result), 1)
        result = helper.printFinanceAdvice(['simple'])
        self.assertEqual(len(result), 1)

        self._give_advice(item1, new_group, 'pmAdviserNG1')
        result = helper.printFinanceAdvice('simple')
        self.assertEqual(len(result), 2)
        result = helper.printFinanceAdvice(['simple'])
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('simple', helper)

    def test_printFinanceAdvice_case_simple_not_given(self):
        # creator for group 'developers'
        self.changeUser('pmCreator1')

        new_group = self._set_up_additional_finance_advisor_group()
        self._set_up_second_finance_adviser(new_group)

        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item1 = self.create('MeetingItem', **data)
        item1.at_post_edit_script()

        pod_template = self.meetingConfig.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item1.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()

        # Advice not asked
        result = helper.printFinanceAdvice('simple_not_given')
        self.assertEqual(result, [])

        item1.setOptionalAdvisers(('vendors', new_group))
        item1.at_post_edit_script()

        # No advice given
        result = helper.printFinanceAdvice('simple_not_given')
        self.assertEqual(len(result), 2)

        # 1 Advice given
        self._give_advice(item1, 'vendors', 'pmReviewer2')
        result = helper.printFinanceAdvice('simple_not_given')
        self.assertEqual(len(result), 1)

        # remove the advice
        item1.restrictedTraverse('@@delete_givenuid')(item1.meetingadvice.UID())
        item1.at_post_edit_script()
        result = helper.printFinanceAdvice('simple_not_given')
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('simple_not_given', helper)

    def test_printFinanceAdvice_case_initiative(self):
        new_group = self._set_up_additional_finance_advisor_group()

        self._set_up_second_finance_adviser(new_group)
        self.meetingConfig.powerAdvisersGroups = (new_group, 'vendors',)

        self.changeUser('pmCreator1')
        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item1 = self.create('MeetingItem', **data)
        item1.setOptionalAdvisers('developers')
        item1.at_post_edit_script()

        pod_template = self.meetingConfig.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item1.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()
        result = helper.printFinanceAdvice('initiative')
        self.assertEqual(result, [])

        self._give_advice(item1, 'vendors', 'pmReviewer2')
        result = helper.printFinanceAdvice('initiative')
        self.assertEqual(len(result), 1)

        self._give_advice(item1, 'developers', 'pmAdviser1')
        result = helper.printFinanceAdvice('initiative')
        self.assertEqual(len(result), 1)

        self._give_advice(item1, new_group, 'pmAdviserNG1')
        result = helper.printFinanceAdvice('initiative')
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('initiative', helper)

        # remove the advice
        self.changeUser('pmReviewer2')
        item1.restrictedTraverse('@@delete_givenuid')(item1.meetingadvice.UID())
        item1.at_post_edit_script()
        result = helper.printFinanceAdvice('initiative')
        self.assertEqual(len(result), 1)

    def test_printFinanceAdvice_case_legal(self):
        new_group = self._set_up_additional_finance_advisor_group()

        self._set_up_second_finance_adviser(new_group)
        self.meetingConfig.powerAdvisersGroups = (new_group, 'vendors',)

        self.changeUser('pmCreator1')
        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item1 = self.create('MeetingItem', **data)
        item1.setOptionalAdvisers(('developers', 'vendors__rowid__unique_id_002', new_group + '__rowid__unique_id_003'))
        item1.at_post_edit_script()

        pod_template = self.meetingConfig.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item1.restrictedTraverse('@@document-generation')
        view()
        helper1 = view.get_generation_context_helper()
        result = helper1.printFinanceAdvice('legal')
        self.assertEqual(result, [])

        self._give_advice(item1, 'vendors', 'pmReviewer2')
        result = helper1.printFinanceAdvice('legal')
        self.assertEqual(len(result), 1)

        self._give_advice(item1, new_group, 'pmAdviserNG1')
        result = helper1.printFinanceAdvice('legal')
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('legal', helper1)

        # test with power observer
        self.changeUser('siteadmin')
        self.meetingConfig.powerAdvisersGroups = (new_group, 'vendors',)
        self.changeUser('pmCreator1')
        item2 = self.create('MeetingItem', **data)
        item2.setOptionalAdvisers(('developers', 'vendors__rowid__unique_id_002', ))
        item2.at_post_edit_script()

        pod_template = self.meetingConfig.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item2.restrictedTraverse('@@document-generation')
        view()
        helper2 = view.get_generation_context_helper()
        result = helper2.printFinanceAdvice('legal')
        self.assertEqual(result, [])

        self._give_advice(item2, 'vendors', 'pmReviewer2')
        result = helper2.printFinanceAdvice('legal')
        self.assertEqual(len(result), 1)

        self._give_advice(item2, new_group, 'pmAdviserNG1')
        result = helper2.printFinanceAdvice('legal')
        self.assertEqual(len(result), 1)

    def test_printFinanceAdvice_case_legal_not_given(self):
        new_group = self._set_up_additional_finance_advisor_group()

        self._set_up_second_finance_adviser(new_group)
        self.meetingConfig.powerAdvisersGroups = (new_group, 'vendors',)

        self.changeUser('pmCreator1')
        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item1 = self.create('MeetingItem', **data)
        item1.setOptionalAdvisers(('developers', 'vendors__rowid__unique_id_002', new_group + '__rowid__unique_id_003'))
        item1.at_post_edit_script()

        pod_template = self.meetingConfig.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item1.restrictedTraverse('@@document-generation')
        view()
        helper1 = view.get_generation_context_helper()
        result = helper1.printFinanceAdvice('legal_not_given')

        self.assertEqual(len(result), 2)

        self._give_advice(item1, 'vendors', 'pmReviewer2')
        result = helper1.printFinanceAdvice('legal_not_given')
        self.assertEqual(len(result), 1)

        self._give_advice(item1, new_group, 'pmAdviserNG1')
        result = helper1.printFinanceAdvice('legal_not_given')
        self.assertEqual(result, [])

        # remove the advice
        self.changeUser('pmReviewer2')
        item1.restrictedTraverse('@@delete_givenuid')(item1.meetingadvice.UID())
        item1.at_post_edit_script()
        result = helper1.printFinanceAdvice('legal_not_given')
        self.assertEqual(len(result), 1)

        # remove the advice
        self.changeUser('pmAdviserNG1')
        item1.restrictedTraverse('@@delete_givenuid')(item1.getAdviceObj(new_group).UID())
        item1.at_post_edit_script()
        result = helper1.printFinanceAdvice('legal_not_given')
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('legal_not_given', helper1)

        # test with power observer
        self.changeUser('siteadmin')
        self.meetingConfig.powerAdvisersGroups = (new_group, 'vendors',)
        self.changeUser('pmCreator1')
        item2 = self.create('MeetingItem', **data)
        item2.setOptionalAdvisers(('developers', 'vendors__rowid__unique_id_002', ))
        item2.at_post_edit_script()

        pod_template = self.meetingConfig.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item2.restrictedTraverse('@@document-generation')
        view()
        helper2 = view.get_generation_context_helper()
        result = helper2.printFinanceAdvice('legal_not_given')
        self.assertEqual(len(result), 1)

        self._give_advice(item2, 'vendors', 'pmReviewer2')
        result = helper2.printFinanceAdvice('legal_not_given')
        self.assertEqual(result, [])

        self._give_advice(item2, new_group, 'pmAdviserNG1')
        result = helper2.printFinanceAdvice('legal_not_given')
        self.assertEqual(result, [])

    def test_get_multiple_level_printing(self):
        self.changeUser('pmManager')
        self.meetingConfig.useGroupsAsCategories = False
        m = self._createMeetingWithItems()
        # adapt categories to have catid and item to have category
        for item in m.getItems(ordered=True):
            item.setCategory('development')
        i6 = self.create('MeetingItem', title='Item6')
        i6.setCategory('development')
        i6.getCategory(theObject=True).setCategoryId('A.1.2.1.1')
        i6.getCategory(theObject=True).setDescription('DESCRI1|DESCRI2|DESCRI3')
        i7 = self.create('MeetingItem', title='Item7')
        i7.setCategory('research')
        i7.getCategory(theObject=True).setCategoryId('B.1')
        i7.getCategory(theObject=True).setDescription('')
        self.presentItem(i6)
        self.presentItem(i7)
        # build the list of uids
        itemUids = [anItem.UID() for anItem in m.getItems(ordered=True)]
        # create view obj
        # first, get template to use view
        pod_template = self.meetingConfig.podtemplates.agendaTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = m.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()
        # test on the meeting
        # we should have a ordereddic containing 3 lists, 6 list by category
        ordered_dico = helper.get_multiple_level_printing(itemUids=itemUids, level_number=5)
        self.assertEquals(len(ordered_dico), 7)
        keys = ordered_dico.keys()
        self.assertEquals(keys, ['<h1>A</h1>', '<h2>A.1. DESCRI1</h2>', '<h3>A.1.2. DESCRI2</h3>',
                                 '<h4>A.1.2.1. DESCRI3</h4>', '<h5>Development topics</h5>',
                                 '<h1>B</h1>', '<h2>Research topics</h2>'])
        # check somes values
        self.assertEquals(ordered_dico['<h5>Development topics</h5>'][0][0], 'A.1.2.1.1.1')
        self.assertEquals(ordered_dico['<h5>Development topics</h5>'][0][1].getId(), 'o3')
        self.assertEquals(ordered_dico['<h5>Development topics</h5>'][1][0], 'A.1.2.1.1.2')
        self.assertEquals(ordered_dico['<h5>Development topics</h5>'][1][1].getId(), 'item6')
        self.assertEquals(ordered_dico['<h1>A</h1>'], [])
