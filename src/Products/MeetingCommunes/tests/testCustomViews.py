# -*- coding: utf-8 -*-
#
# File: testCustomViews.py
#
# GNU General Public License (GPL)
#

from collective.contact.plonegroup.utils import get_plone_group_id
from DateTime import DateTime
from imio.history.utils import getLastWFAction
from itertools import chain
from plone import api
from plone.app.textfield import RichTextValue
from plone.dexterity.utils import createContentInContainer
from Products.MeetingCommunes.browser.overrides import MCMeetingDocumentGenerationHelperView as item_dghv
from Products.MeetingCommunes.config import FINANCE_ADVICES_COLLECTION_ID
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase


class testCustomViews(MeetingCommunesTestCase):
    """
        Tests the custom views
    """

    def test_PrintAllAnnexes(self):
        """ """
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        self._enable_annex_config(item, param="confidentiality")
        self._enable_annex_config(item, param="to_be_printed")
        self._enable_annex_config(item, param="signed")
        self._enable_annex_config(item, param="publishable")
        annex1 = self.addAnnex(item, to_print=True)
        annex1_type_icon = u'<img src="{0}/{1}"/>'.format(
            self.portal.absolute_url(),
            item.categorized_elements[annex1.UID()]['icon_url'])
        annex2 = self.addAnnex(item,
                               annexTitle='Annex 2',
                               annexFile=self.annexFilePDF,
                               to_print=True,
                               confidential=True)
        annex2_type_icon = u'<img src="{0}/{1}"/>'.format(
            self.portal.absolute_url(),
            item.categorized_elements[annex2.UID()]['icon_url'])
        annex3 = self.addAnnex(item,
                               annexTitle=u'Annex 3 with special characters h\xc3\xa9h\xc3\xa9',
                               annexFile=self.annexFileCorruptedPDF,
                               to_sign=True,
                               confidential=True)
        annex3_type_icon = u'<img src="{0}/{1}"/>'.format(
            self.portal.absolute_url(),
            item.categorized_elements[annex3.UID()]['icon_url'])
        annexDecision1 = self.addAnnex(item, annexTitle='Annex decision 1', relatedTo='item_decision')
        annexDecision1_type_icon = u'<img src="{0}/{1}"/>'.format(
            self.portal.absolute_url(),
            item.categorized_elements[annexDecision1.UID()]['icon_url'])

        pod_template = self.meetingConfig.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()
        self.assertEqual(
            helper.print_all_annexes(),
            u'<p>{0}&nbsp;<a href="{1}">Annex</a>&nbsp;(txt)</p>\n'
            u'<p>{2}&nbsp;<a href="{3}">Annex 2</a>&nbsp;(pdf)</p>\n'
            u'<p>{4}&nbsp;<a href="{5}">Annex 3 with special characters h\xc3\xa9h\xc3\xa9</a>&nbsp;(pdf)</p>'.format(
                annex1_type_icon,
                annex1.absolute_url(),
                annex2_type_icon,
                annex2.absolute_url(),
                annex3_type_icon,
                annex3.absolute_url()))
        self.assertEqual(
            helper.print_all_annexes(with_icon=True),
            u'<p>{0}&nbsp;<a href="{1}">Annex</a>&nbsp;<img src="http://nohost/plone/txt.png"/>&nbsp;(txt)</p>\n'
            u'<p>{2}&nbsp;<a href="{3}">Annex 2</a>&nbsp;<img src="http://nohost/plone/pdf.png"/>&nbsp;(pdf)</p>\n'
            u'<p>{4}&nbsp;<a href="{5}">Annex 3 with special characters h\xc3\xa9h\xc3\xa9</a>&nbsp;'
            u'<img src="http://nohost/plone/pdf.png"/>&nbsp;(pdf)</p>'.format(
                annex1_type_icon,
                annex1.absolute_url(),
                annex2_type_icon,
                annex2.absolute_url(),
                annex3_type_icon,
                annex3.absolute_url()))
        self.assertEqual(
            helper.print_all_annexes(with_filename=True),
            u'<p>{0}&nbsp;<a href="{1}">Annex</a>&nbsp;(txt)</p>\n'
            u'<p><i>FILE.txt</i></p>\n'
            u'<p>{2}&nbsp;<a href="{3}">Annex 2</a>&nbsp;(pdf)</p>\n'
            u'<p><i>file_correct.pdf</i></p>\n'
            u'<p>{4}&nbsp;<a href="{5}">Annex 3 with special characters h\xc3\xa9h\xc3\xa9</a>&nbsp;(pdf)</p>\n'
            u'<p><i>file_errorDuringConversion.pdf</i></p>'.format(
                annex1_type_icon,
                annex1.absolute_url(),
                annex2_type_icon,
                annex2.absolute_url(),
                annex3_type_icon,
                annex3.absolute_url()))
        self.assertEqual(
            helper.print_all_annexes(with_filename=True, with_icon=True),
            u'<p>{0}&nbsp;<a href="{1}">Annex</a>&nbsp;<img src="http://nohost/plone/txt.png"/>&nbsp;(txt)</p>\n'
            u'<p><i>FILE.txt</i></p>\n'
            u'<p>{2}&nbsp;<a href="{3}">Annex 2</a>&nbsp;<img src="http://nohost/plone/pdf.png"/>&nbsp;(pdf)</p>\n'
            u'<p><i>file_correct.pdf</i></p>\n'
            u'<p>{4}&nbsp;<a href="{5}">Annex 3 with special characters h\xc3\xa9h\xc3\xa9</a>&nbsp;'
            u'<img src="http://nohost/plone/pdf.png"/>&nbsp;(pdf)</p>\n'
            u'<p><i>file_errorDuringConversion.pdf</i></p>'.format(
                annex1_type_icon,
                annex1.absolute_url(),
                annex2_type_icon,
                annex2.absolute_url(),
                annex3_type_icon,
                annex3.absolute_url()))

        self.assertEqual(
            helper.print_all_annexes(portal_types=('annexDecision',)),
            u'<p>{0}&nbsp;<a href="{1}">Annex decision 1</a>&nbsp;(txt)</p>'.format(annexDecision1_type_icon,
                                                                                    annexDecision1.absolute_url()))

        self.assertEqual(
            helper.print_all_annexes(portal_types=['annex', 'annexDecision'],
                                     filters={'confidential': True, 'to_sign': True}),
            u'<p>{0}&nbsp;<a href="{1}">Annex 3 with special characters h\xc3\xa9h\xc3\xa9</a>&nbsp;(pdf)</p>'.format(
                annex3_type_icon,
                annex3.absolute_url()))
        self.assertEqual(
            helper.print_all_annexes(portal_types=['annex', 'annexDecision'], filters={'confidential': True}),
            u'<p>{0}&nbsp;<a href="{1}">Annex 2</a>&nbsp;(pdf)</p>\n'
            u'<p>{2}&nbsp;<a href="{3}">Annex 3 with special characters h\xc3\xa9h\xc3\xa9</a>&nbsp;(pdf)</p>'.format(
                annex2_type_icon,
                annex2.absolute_url(),
                annex3_type_icon,
                annex3.absolute_url()))
        self.assertEqual(
            helper.print_all_annexes(portal_types=['annex', 'annexDecision'], filters={'publishable': True}), u'')

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

    def test_print_formated_advice(self):
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

        result = helper.print_formated_advice()
        self.assertListEqual(result, [])

        result = helper.print_formated_advice()
        self.assertListEqual(result, [])

        result = helper.print_formated_advice(exclude_not_given=False)
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

        result = helper.print_formated_advice()
        self.assertEqual(
            [(u'Developers', u'Positive')],
            [(res['name'], res['type_translated']) for res in result])

        self.assertListEqual(helper.print_formated_advice(), helper.print_formated_advice(True))

        result = helper.print_formated_advice(exclude_not_given=False)
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

        self._addPrincipalToGroup(adviser_user_id, get_plone_group_id(new_group_uid, 'advisers'))
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
        cfg.setItemAdviceStates((item.query_state(), 'validated',))
        cfg.setItemAdviceEditStates((item.query_state(), 'validated',))
        cfg.setItemAdviceViewStates((item.query_state(), 'validated',))
        self.assertEqual(helper._getItemAdviceTransmissionDate(),
                         getLastWFAction(item)['time'])

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
            result = helper.print_finance_advice(case)
            self.assertListEqual(result, [])
            result = helper.print_finance_advice([case])
            self.assertListEqual(result, [])

        result = helper.print_finance_advice(other_cases)
        self.assertEqual(result, [])
        result = helper.print_finance_advice(cases)
        self.assertEqual(len(result), 2)

    def test_print_finance_advice_case_simple(self):
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
        result = helper.print_finance_advice('simple')
        self.assertEqual(result, [])
        result = helper.print_finance_advice(['simple'])
        self.assertEqual(result, [])

        item1.setOptionalAdvisers((self.vendors_uid,))
        item1._update_after_edit()

        # No advice given
        result = helper.print_finance_advice('simple')
        self.assertEqual(result, [])
        result = helper.print_finance_advice(['simple'])
        self.assertEqual(result, [])

        # 1 Advice given
        self._give_advice(item1, self.vendors_uid, 'pmReviewer2')
        result = helper.print_finance_advice('simple')
        self.assertEqual(len(result), 1)
        result = helper.print_finance_advice(['simple'])
        self.assertEqual(len(result), 1)

        self.changeUser('pmCreator1')
        item1.setOptionalAdvisers((new_group_uid, self.vendors_uid, self.developers_uid))
        item1._update_after_edit()

        self._give_advice(item1, self.developers_uid, 'pmAdviser1')
        result = helper.print_finance_advice('simple')
        self.assertEqual(len(result), 1)
        result = helper.print_finance_advice(['simple'])
        self.assertEqual(len(result), 1)

        self._give_advice(item1, new_group_uid, 'pmAdviserNG1')
        result = helper.print_finance_advice('simple')
        self.assertEqual(len(result), 2)
        result = helper.print_finance_advice(['simple'])
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('simple', helper)

    def test_print_finance_advice_case_simple_not_given(self):
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
        result = helper.print_finance_advice('simple_not_given')
        self.assertEqual(result, [])

        item1.setOptionalAdvisers((self.vendors_uid, new_group_uid))
        item1._update_after_edit()

        # No advice given
        result = helper.print_finance_advice('simple_not_given')
        self.assertEqual(len(result), 2)

        # 1 Advice given
        self._give_advice(item1, self.vendors_uid, 'pmReviewer2')
        result = helper.print_finance_advice('simple_not_given')
        self.assertEqual(len(result), 1)

        # remove the advice
        item1.restrictedTraverse('@@delete_givenuid')(item1.meetingadvice.UID())
        item1._update_after_edit()
        result = helper.print_finance_advice('simple_not_given')
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('simple_not_given', helper)

    def test_print_finance_advice_case_initiative(self):
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
        result = helper.print_finance_advice('initiative')
        self.assertEqual(result, [])

        self._give_advice(item1, self.vendors_uid, 'pmReviewer2')
        result = helper.print_finance_advice('initiative')
        self.assertEqual(len(result), 1)

        self._give_advice(item1, self.developers_uid, 'pmAdviser1')
        result = helper.print_finance_advice('initiative')
        self.assertEqual(len(result), 1)

        self._give_advice(item1, new_group_uid, 'pmAdviserNG1')
        result = helper.print_finance_advice('initiative')
        self.assertEqual(len(result), 2)

        # assert other cases
        self.handle_finance_cases('initiative', helper)

        # remove the advice
        self.changeUser('pmReviewer2')
        item1.restrictedTraverse('@@delete_givenuid')(item1.meetingadvice.UID())
        item1._update_after_edit()
        result = helper.print_finance_advice('initiative')
        self.assertEqual(len(result), 1)

    def test_print_finance_advice_case_legal(self):
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
        result = helper1.print_finance_advice('legal')
        self.assertEqual(result, [])

        self._give_advice(item1, self.vendors_uid, 'pmReviewer2')
        result = helper1.print_finance_advice('legal')
        self.assertEqual(len(result), 1)

        self._give_advice(item1, new_group_uid, 'pmAdviserNG1')
        result = helper1.print_finance_advice('legal')
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
        result = helper2.print_finance_advice('legal')
        self.assertEqual(result, [])

        self._give_advice(item2, self.vendors_uid, 'pmReviewer2')
        result = helper2.print_finance_advice('legal')
        self.assertEqual(len(result), 1)

        self._give_advice(item2, new_group_uid, 'pmAdviserNG1')
        result = helper2.print_finance_advice('legal')
        self.assertEqual(len(result), 1)

    def test_print_finance_advice_case_legal_not_given(self):
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
        result = helper1.print_finance_advice('legal_not_given')

        self.assertEqual(len(result), 2)

        self._give_advice(item1, self.vendors_uid, 'pmReviewer2')
        result = helper1.print_finance_advice('legal_not_given')
        self.assertEqual(len(result), 1)

        self._give_advice(item1, new_group_uid, 'pmAdviserNG1')
        result = helper1.print_finance_advice('legal_not_given')
        self.assertEqual(result, [])

        # remove the advice
        self.changeUser('pmReviewer2')
        item1.restrictedTraverse('@@delete_givenuid')(item1.meetingadvice.UID())
        item1._update_after_edit()
        result = helper1.print_finance_advice('legal_not_given')
        self.assertEqual(len(result), 1)

        # remove the advice
        self.changeUser('pmAdviserNG1')
        item1.restrictedTraverse('@@delete_givenuid')(item1.getAdviceObj(new_group_uid).UID())
        item1._update_after_edit()
        result = helper1.print_finance_advice('legal_not_given')
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
        result = helper2.print_finance_advice('legal_not_given')
        self.assertEqual(len(result), 1)

        self._give_advice(item2, self.vendors_uid, 'pmReviewer2')
        result = helper2.print_finance_advice('legal_not_given')
        self.assertEqual(result, [])

        self._give_advice(item2, new_group_uid, 'pmAdviserNG1')
        result = helper2.print_finance_advice('legal_not_given')
        self.assertEqual(result, [])

    def test__filter_items(self):
        cfg = self.meetingConfig
        self.changeUser('pmManager')
        cfg.setUseGroupsAsCategories(False)
        cfg.setInsertingMethodsOnAddItem(
            ({'insertingMethod': 'on_categories', 'reverse': '0'},))
        m = self._createMeetingWithItems()
        # adapt categories to have catid and item to have category
        for item in m.get_items(ordered=True):
            item.setCategory('development')
            item._update_after_edit()
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
        items = m.get_items(ordered=True)

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

    def test_print_formatted_finance_advice(self):
        # Set up 2 finances advisors CFO and Vendors. See test_print_finance_advice.
        cfg = self.meetingConfig
        cfo_uid = self._set_up_additional_finance_advisor_group(
            new_group_name="Chief Financial Officer",
            adviser_user_id="CFOAdviser"
        )
        self._set_up_second_finance_adviser(cfo_uid)
        cfg.powerAdvisersGroups = (cfo_uid, self.vendors_uid,)

        # Item with legal advices (advices with delay)
        self.changeUser('pmCreator1')
        data = {'title': 'Item to advice', 'category': 'maintenance'}
        item1 = self.create('MeetingItem', **data)
        item1.setOptionalAdvisers((self.developers_uid,
                                   self.vendors_uid + '__rowid__unique_id_002',
                                   cfo_uid + '__rowid__unique_id_003'))
        item1._update_after_edit()

        pod_template = cfg.podtemplates.itemTemplate
        self.request.set('template_uid', pod_template.UID())
        self.request.set('output_format', 'odt')
        view = item1.restrictedTraverse('@@document-generation')
        view()

        # No advice given
        helper = view.get_generation_context_helper()
        result = helper.print_formatted_finance_advice()
        self.assertTrue('avis non rendu' in result and 'avis positive' not in result)

        # One legal advice given
        self._give_advice(item1, cfo_uid, "CFOAdviser")
        result = helper.print_formatted_finance_advice()
        self.assertTrue('avis non rendu' in result and 'avis positive' in result)

        # Two legal advices given
        self._give_advice(item1, self.vendors_uid, "pmReviewer2")
        result = helper.print_formatted_finance_advice()
        self.assertTrue('avis non rendu' not in result and 'avis positive' in result)

        # Item with simple advice
        self.changeUser('pmCreator1')
        data = {'title': 'Item with simple advice', 'category': 'maintenance'}
        item2 = self.create('MeetingItem', **data)
        item2.setOptionalAdvisers((self.vendors_uid,))
        item2._update_after_edit()
        view = item2.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()

        result = helper.print_formatted_finance_advice(finance_used_cases=("simple_not_given",))
        self.assertTrue('avis non rendu' in result and 'avis positive' not in result)
        self._give_advice(item2, self.vendors_uid, "pmReviewer2")
        # Simple advice should not have delay_infos
        self.assertDictEqual(item2.adviceIndex[self.vendors_uid]["delay_infos"], {})
        result = helper.print_formatted_finance_advice()
        self.assertTrue('avis positive' in result and "remis" in result)

        # Item with initiative advice
        self.changeUser('pmCreator1')
        data = {'title': 'Item with initiative advice', 'category': 'maintenance'}
        item3 = self.create('MeetingItem', **data)
        item3._update_after_edit()
        view = item3.restrictedTraverse('@@document-generation')
        view()
        helper = view.get_generation_context_helper()

        result = helper.print_formatted_finance_advice()
        self.assertEqual(result, "")
        self._give_advice(item3, self.vendors_uid, "pmReviewer2")
        # Initiative advice is 'not_asked'
        self.assertTrue(item3.adviceIndex[self.vendors_uid]["not_asked"])
        result = helper.print_formatted_finance_advice(finance_used_cases=("initiative",))
        self.assertTrue('avis' in result and 'initiative' in result)

    def test__is_different_grouping_as_previous_item(self):
        self.assertTrue(item_dghv._is_different_grouping_as_previous_item([], u'Brol', 0))
        self.assertTrue(item_dghv._is_different_grouping_as_previous_item([[u'']], u'Brol', 0))
        self.assertFalse(item_dghv._is_different_grouping_as_previous_item([u'Brol'], u'Brol', 0))
        self.assertFalse(item_dghv._is_different_grouping_as_previous_item([[u'Brol']], u'Brol', 0))
        self.assertFalse(
            item_dghv._is_different_grouping_as_previous_item([[u'Brol1',
                                                                [u'Brol2', [u'brol3', []]]]], u'Brol1', 0))
        self.assertTrue(
            item_dghv._is_different_grouping_as_previous_item([[u'Brol1', [u'Brol2', [u'brol3', []]]]], u'Brol2',
                                                              0))
        self.assertTrue(
            item_dghv._is_different_grouping_as_previous_item([[u'Brol1',
                                                                [u'Brol2', [u'brol3', []]]]], u'brol3', 0))
        self.assertTrue(
            item_dghv._is_different_grouping_as_previous_item([[u'Brol1', [
                u'Brol2', [u'brol3', []]]]], u'Machin', 0))
        self.assertFalse(
            item_dghv._is_different_grouping_as_previous_item([[u'Brol2', [u'brol3', []]]], u'Brol2', 0))
        self.assertTrue(
            item_dghv._is_different_grouping_as_previous_item([[u'Brol2', [u'brol3', []]]], u'brol3', 0))
        self.assertTrue(
            item_dghv._is_different_grouping_as_previous_item([[u'Brol2', [u'brol3', []]]], u'truc', 0))
        self.assertTrue(
            item_dghv._is_different_grouping_as_previous_item([[u'brol3', []]], u'Brol3', 0))
        self.assertFalse(
            item_dghv._is_different_grouping_as_previous_item([[u'brol3', []]], u'brol3', 0))

        self.assertFalse(
            item_dghv._is_different_grouping_as_previous_item([[u'brol3', []]], u'brol3', 1))

        self.assertFalse(
            item_dghv._is_different_grouping_as_previous_item([[u'brol3', [u'truc1', []]]], u'brol3', 2))

        self.assertTrue(
            item_dghv._is_different_grouping_as_previous_item([[u'brol3', [u'truc1', []]]], u'truc1', 2))

    def test_get_grouped_items(self):
        self.changeUser('pmManager')
        cfg = self.meetingConfig
        cfg.setUseGroupsAsCategories(False)
        cfg.setInsertingMethodsOnAddItem(
            ({'insertingMethod': 'on_categories', 'reverse': '0'},))
        m = self._createMeetingWithItems()
        # adapt categories to have catid and item to have category
        for item in m.get_items(ordered=True):
            item.setCategory('development')
            item._update_after_edit()
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
        items = m.get_items(ordered=True)
        itemUids = [anItem.UID() for anItem in items]
        self.maxDiff = None

        res = helper.get_grouped_items(itemUids)
        self.assertListEqual(res, items)

        res = helper.get_grouped_items(itemUids, group_by='category')
        self.assertListEqual(
            res,
            [[i5.getCategory(theObject=True).Title(), items[0:-1]],
             [i7.getCategory(theObject=True).Title(), [i7]]])

        res = helper.get_grouped_items(itemUids, group_by=['category'])
        self.assertListEqual(
            res,
            [[i5.getCategory(theObject=True).Title(), items[0:-1]],
             [i7.getCategory(theObject=True).Title(), [i7]]])

        res = helper.get_grouped_items(itemUids, group_by=['category', 'proposingGroup'])
        self.assertListEqual(
            res,
            [[i5.getCategory(theObject=True).Title(),
              [u'Developers', [items[0]]],
              [u'Vendors', items[1:3]],
              [u'Developers', [items[3]]],
              [u'Vendors', [items[4]]],
              [u'Developers', [i5]]],
             [i7.getCategory(theObject=True).Title(),
              [i7.getProposingGroup(theObject=True).Title(), [i7]]]])

        res = helper.get_grouped_items(itemUids, group_by='category',
                                       excluded_values={'category': i5.getCategory(theObject=True).Title()})
        self.assertListEqual(
            res,
            [[i7.getCategory(theObject=True).Title(), [i7]]])

        res = helper.get_grouped_items(itemUids, group_by='category',
                                       included_values={'category': i7.getCategory(theObject=True).Title()})
        self.assertListEqual(
            res,
            [[i7.getCategory(theObject=True).Title(), [i7]]])

        self.freezeMeeting(m)
        self.do(i7, 'backToPresented')
        res = helper.get_grouped_items(itemUids, group_by='category', ignore_review_states=['itemfrozen'])
        self.assertListEqual(
            res,
            [[i7.getCategory(theObject=True).Title(), [i7]]])

        # 2 consecutive groupings of different levels have the same value
        self.changeUser('siteadmin')
        developpers = self.create('meetingcategory', id="developers", title=u'Developers',
                                  description=u'Developers topic', category_id='developers')
        self.changeUser('pmManager')
        i5.setCategory('developers')
        res = helper.get_grouped_items(itemUids, group_by=['proposingGroup', 'category'])
        self.assertListEqual(
            res,
            [[u'Developers', [u'Development topics', [items[0]]]],
             [u'Vendors', [u'Development topics', items[1:3]]],
             [u'Developers', [u'Development topics', [items[3]]]],
             [u'Vendors', [u'Development topics', [items[4]]]],
             [u'Developers', [developpers.Title(), [i5]], [u'Research topics', [i7]]]])

    def test_get_grouped_items_unrestricted(self):
        self.changeUser('pmManager')
        meeting = self._createMeetingWithItems()
        view = meeting.restrictedTraverse('@@document-generation')
        helper = view.get_generation_context_helper()
        itemUids = [item.UID for item in meeting.get_items(ordered=True, the_objects=False)]
        self.assertEqual(len(itemUids), 7)
        self.assertEqual(len(helper.get_grouped_items(itemUids, unrestricted=False)), 7)
        self.assertEqual(len(helper.get_grouped_items(itemUids, unrestricted=True)), 7)

        # by default pmCreator1 may only get 'developers' items
        self.changeUser('pmCreator1')
        itemUids = [item.UID for item in meeting.get_items(ordered=True, the_objects=False)]
        grouped_items = helper.get_grouped_items(
            itemUids, group_by='proposingGroup', unrestricted=False)
        self.assertEqual(len(grouped_items), 1)
        self.assertEqual(grouped_items[0][0], u'Developers')
        self.assertEqual(len(grouped_items[0][1]), 4)
        # unrestricted, every items
        unrestricted_grouped_items = helper.get_grouped_items(
            itemUids, group_by='proposingGroup', unrestricted=True)
        self.assertEqual(len(unrestricted_grouped_items), 2)
        self.assertEqual(unrestricted_grouped_items[0][0], u'Developers')
        self.assertEqual(len(unrestricted_grouped_items[0][1]), 4)
        self.assertEqual(unrestricted_grouped_items[1][0], u'Vendors')
        self.assertEqual(len(unrestricted_grouped_items[1][1]), 3)

        # by default pmCreator2 may only get 'vendors' items
        self.changeUser('pmCreator2')
        itemUids = [item.UID for item in meeting.get_items(ordered=True, the_objects=False)]
        grouped_items = helper.get_grouped_items(
            itemUids, group_by='proposingGroup', unrestricted=False)
        self.assertEqual(len(grouped_items), 1)
        self.assertEqual(grouped_items[0][0], u'Vendors')
        self.assertEqual(len(grouped_items[0][1]), 3)
        # unrestricted, every items
        unrestricted_grouped_items = helper.get_grouped_items(
            itemUids, group_by='proposingGroup', unrestricted=True)
        self.assertEqual(len(unrestricted_grouped_items), 2)
        self.assertEqual(unrestricted_grouped_items[0][0], u'Developers')
        self.assertEqual(len(unrestricted_grouped_items[0][1]), 4)
        self.assertEqual(unrestricted_grouped_items[1][0], u'Vendors')
        self.assertEqual(len(unrestricted_grouped_items[1][1]), 3)
        # when using included_values and excluded_values
        # included_values
        grouped_items = helper.get_grouped_items(
            itemUids,
            included_values={'proposingGroup': [self.vendors.Title()]},
            unrestricted=True)
        self.assertEqual([item.getProposingGroup() for item in grouped_items],
                         [self.vendors_uid, self.vendors_uid, self.vendors_uid])
        grouped_items = helper.get_grouped_items(
            itemUids,
            included_values={'proposingGroup': [self.developers.Title()]},
            unrestricted=True)
        self.assertEqual([item.getProposingGroup() for item in grouped_items],
                         [self.developers_uid, self.developers_uid,
                          self.developers_uid, self.developers_uid])
        # excluded_values
        grouped_items = helper.get_grouped_items(
            itemUids,
            excluded_values={'proposingGroup': [self.vendors.Title()]},
            unrestricted=True)
        self.assertEqual([item.getProposingGroup() for item in grouped_items],
                         [self.developers_uid, self.developers_uid,
                          self.developers_uid, self.developers_uid])
        grouped_items = helper.get_grouped_items(
            itemUids,
            excluded_values={'proposingGroup': [self.developers.Title()]},
            unrestricted=True)
        self.assertEqual([item.getProposingGroup() for item in grouped_items],
                         [self.vendors_uid, self.vendors_uid, self.vendors_uid])
        # itemUids, unrestricted will return everything unless len given itemUids
        # is < every visible items meaining user filtered meeting in the UI
        # when passing itemUids of every visible items, we get more
        all_unrestricted_grouped_items = list(
            chain.from_iterable([items for gp_title, items in unrestricted_grouped_items]))
        self.assertEqual(len(itemUids), 3)
        self.assertEqual(len(all_unrestricted_grouped_items), 7)
        itemUids = [item.UID() for item in all_unrestricted_grouped_items[0:4]]
        self.assertEqual(len(itemUids), 4)
        unrestricted_grouped_items = helper.get_grouped_items(
            itemUids, group_by='proposingGroup', unrestricted=True)
        all_unrestricted_grouped_items = list(
            chain.from_iterable([items for gp_title, items in unrestricted_grouped_items]))
        self.assertEqual(len(all_unrestricted_grouped_items), 4)

    def test_get_grouped_items_additional_catalog_query(self):
        self.changeUser('pmManager')
        meeting = self._createMeetingWithItems()
        view = meeting.restrictedTraverse('@@document-generation')
        helper = view.get_generation_context_helper()
        itemUids = [item.UID for item in meeting.get_items(ordered=True, the_objects=False)]
        grouped_items = helper.get_grouped_items(
            itemUids, additional_catalog_query={})
        self.assertEqual(len(grouped_items), 7)
        grouped_items = helper.get_grouped_items(
            itemUids, additional_catalog_query={'getProposingGroup': self.vendors_uid})
        self.assertEqual(len(grouped_items), 3)
        grouped_items = helper.get_grouped_items(
            itemUids, additional_catalog_query={'getProposingGroup': self.developers_uid})
        self.assertEqual(len(grouped_items), 4)

    def test_get_multiple_level_printing(self):
        self.changeUser('pmManager')
        cfg = self.meetingConfig
        cfg.setUseGroupsAsCategories(False)
        cfg.setInsertingMethodsOnAddItem(
            ({'insertingMethod': 'on_categories', 'reverse': '0'},))
        m = self._createMeetingWithItems()
        # adapt categories to have catid and item to have category
        for item in m.get_items(ordered=True):
            item.setCategory('development')
            item._update_after_edit()
        # intel inside *Joke*
        i5 = self.create('MeetingItem', title='Item5')
        i5.setCategory('development')
        i5.getCategory(theObject=True).category_id = u'A.1.2.1.1'
        i5.getCategory(theObject=True).description = u'DESCRI1|DESCRI2|DESCRI3'
        i7 = self.create('MeetingItem', title='Item7')
        i7.setCategory('research')
        i7.getCategory(theObject=True).category_id = u'B.1'
        i7.getCategory(theObject=True).description = u''
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
        items = m.get_items(ordered=True)
        itemUids = [anItem.UID() for anItem in items]
        ordered_dico = helper.get_multiple_level_printing(itemUids=itemUids, level_number=5)
        self.assertEqual(len(ordered_dico), 7)
        self.assertEqual(
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

        def create_and_validate_item(creator, preferred_meeting=None):
            self.changeUser(creator)
            item = self.create('MeetingItem')
            self.validateItem(item)
            if preferred_meeting:
                item.setPreferredMeeting(preferred_meeting)
            return item

        def get_item_view(item):
            pod_template = cfg.podtemplates.itemTemplate
            self.request.set('template_uid', pod_template.UID())
            self.request.set('output_format', 'odt')
            view = item.restrictedTraverse('@@document-generation')
            view()
            return view.get_generation_context_helper()

        self.changeUser('pmManager')
        meeting = self.create('Meeting')
        meeting_uid = meeting.UID()

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

        self.changeUser('pmManager')
        self.freezeMeeting(meeting)

        test3 = create_and_validate_item('pmCreator1', meeting_uid)
        helper3 = get_item_view(test3)
        test4 = create_and_validate_item('pmCreator2', meeting_uid)
        helper4 = get_item_view(test4)

        self.presentItem(test3)
        self.presentItem(create_and_validate_item('pmCreator2', meeting_uid))
        self.presentItem(create_and_validate_item('pmCreator1', meeting_uid))
        self.presentItem(create_and_validate_item('pmCreator2', meeting_uid))
        self.presentItem(create_and_validate_item('pmCreator1', meeting_uid))
        self.presentItem(test4)

        self.assertEqual(helper1.print_item_number_within_category(), '4')
        self.assertEqual(helper2.print_item_number_within_category(), '3')
        self.assertEqual(helper3.print_item_number_within_category(), '6')
        self.assertEqual(helper4.print_item_number_within_category(), '6')

        self.assertEqual(helper3.print_item_number_within_category(list_types=['late']), '1')
        self.assertEqual(helper4.print_item_number_within_category(list_types=['late']), '3')

        self.assertEqual(helper3.print_item_number_within_category(list_types=['normal']), '')
        self.assertEqual(helper4.print_item_number_within_category(list_types=['normal']), '')

        self.assertEqual(helper3.print_item_number_within_category(
            list_types=['normal'], default='XXXX'), 'XXXX')
        self.assertEqual(helper4.print_item_number_within_category(
            list_types=['normal'], default='ERROR'), 'ERROR')

    def test_mc_print_item_number_with_sublevel(self):
        expected_with_alpha = {100: "1",
                               101: "1.a",
                               102: "1.b",
                               103: "1.c",
                               127: "1.aa",
                               128: "1.ab",
                               200: "2"}

        expected_with_adverbs = {100: "1",
                                 101: "1/bis",
                                 102: "1/ter",
                                 103: "1/quater",
                                 127: "1/27",
                                 128: "1/28",
                                 200: "2"}

        self.changeUser('pmManager')
        self.create('Meeting')

        for item_number in expected_with_alpha.keys():
            item = self.create('MeetingItem')
            self.presentItem(item)
            item.setItemNumber(item_number)
            view = item.restrictedTraverse('document-generation')
            helper = view.get_generation_context_helper()

            self.assertEqual(
                helper.print_item_number_with_sublevel(mode="alpha"),
                expected_with_alpha.get(item_number)
            )
            self.assertEqual(
                helper.print_item_number_with_sublevel(mode="adverb", num_format="{0}/{1}"),
                expected_with_adverbs.get(item_number)
            )
            self.assertEqual(
                helper.print_item_number_with_sublevel(mode=None, num_format="{0}.{1}"),
                item.getItemNumber(for_display=True)
            )
