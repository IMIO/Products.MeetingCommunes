# -*- coding: utf-8 -*-
#
# File: overrides.py
#
# Copyright (c) 2016 by Imio.be
#
# GNU General Public License (GPL)
#

from collections import OrderedDict
from imio.history.interfaces import IImioHistory
from imio.history.utils import getLastAction
from imio.history.utils import getLastWFAction
from plone import api
from plone.api.validation import mutually_exclusive_parameters
from Products.CMFPlone.utils import safe_unicode
from Products.PloneMeeting.browser.views import FolderDocumentGenerationHelperView
from Products.PloneMeeting.browser.views import ItemDocumentGenerationHelperView
from Products.PloneMeeting.browser.views import MeetingDocumentGenerationHelperView
from Products.PloneMeeting.utils import get_annexes
from zope.component import getAdapter


class MCItemDocumentGenerationHelperView(ItemDocumentGenerationHelperView):
    """Specific printing methods used for item."""

    def printAllAnnexes(self, portal_types=['annex']):
        ''' Printing Method use in templates :
            return all viewable annexes for item '''
        res = []
        annexes = get_annexes(self.context, portal_types=portal_types)
        for annex in annexes:
            url = annex.absolute_url()
            title = annex.Title().replace('&', '&amp;')
            res.append(u'<p><a href="{0}">{1}</a></p>'.format(
                url, safe_unicode(title)))
        return (u'\n'.join(res))

    def printFormatedAdvice(self, exclude_not_given=True):
        ''' Printing Method use in templates :
            return formated advice'''
        res = []
        advices_by_type = self.context.getAdvicesByType()
        for key in advices_by_type.keys():
            for advice in advices_by_type[key]:
                if advice['type'] == 'not_given' and exclude_not_given:
                    continue
                data = self.context.getAdviceDataFor(
                    self.real_context, adviser_uid=advice['id'])
                res.append(data)
        return res

    def printFinanceAdvice(self, cases, show_hidden=False):
        """
        :param cases: collection containing either 'initiative', 'legal', 'simple' or 'not_given'
               cases can also be a string in case a single case should be returned and for backward compatibility.
        :return: an array of dictionaries same as MeetingItem.getAdviceDataFor
        or empty if no advice matching the given case.
        """

        """
        case 'simple' means the financial advice was requested but without any delay.
        case 'legal' means the financial advice was requested with a delay. It's a legal financial advice.
        case 'initiative' means the financial advice was given without being requested at the first place.
        case 'legal_not_given' means the financial advice was requested with delay.
            But was ignored by the finance director.
        case 'simple_not_given' means the financial advice was requested without delay.
            But was ignored by the finance director.
        """

        def check_given_or_not_cases(advice, case_to_check, case_given, case_not_given):
            if advice['advice_given_on']:
                return case_to_check == case_given
            else:
                return case_to_check == case_not_given

        if isinstance(cases, str):
            cases = [cases]

        result = []
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        finance_advice_ids = cfg.adapted().getUsedFinanceGroupIds()

        if finance_advice_ids:
            advices = self.context.getAdviceDataFor(self.context.context)

            for case in cases:
                if case in ['initiative', 'legal', 'simple', 'simple_not_given', 'legal_not_given']:
                    for finance_advice_id in finance_advice_ids:

                        if finance_advice_id in advices:
                            advice = advices[finance_advice_id]
                        else:
                            continue

                        # Change data if advice is hidden
                        if 'hidden_during_redaction' in advice and \
                           advice['hidden_during_redaction'] and not show_hidden:
                            message = self.translate('hidden_during_redaction', domain='PloneMeeting')
                            advice['type_translated'] = message
                            advice['type'] = 'hidden_during_redaction'
                            advice['comment'] = message

                        # check if advice was given on self initiative by the adviser
                        if advice['not_asked']:
                            if case == 'initiative' and advice['advice_given_on']:
                                result.append(advice)
                        else:
                            # set date of transmission to adviser because the advice was asked by the agent
                            advice['item_transmitted_on'] = self._getItemAdviceTransmissionDate(advice=advice)
                            if advice['item_transmitted_on']:
                                advice['item_transmitted_on_localized'] = \
                                    self.display_date(date=advice['item_transmitted_on'])
                            else:
                                advice['item_transmitted_on_localized'] = ''

                            # If there is a delay then it is a legal advice. If not, it's a simple advice
                            if advice['delay']:
                                if check_given_or_not_cases(advice, case, 'legal', 'legal_not_given'):
                                    result.append(advice)
                            elif check_given_or_not_cases(advice, case, 'simple', 'simple_not_given'):
                                result.append(advice)
        return result

    def _get_advice(self, adviser_id=None):
        """
        :param adviser_id: the adviser id to seek advice for.
               If None, it will try to find and use the fianancial adviser id.
        :return: the advice data for the used adviser id.
        """
        if adviser_id is None:
            adviser_id = self.context.adapted().getFinanceAdviceId()

        if adviser_id:
            return self.real_context.getAdviceDataFor(self.real_context, adviser_id)

        return None

    @mutually_exclusive_parameters('adviser_id', 'advice')
    def print_advice_delay_limit_date(self, adviser_id=None, advice=None):
        if advice is None:
            advice = self._get_advice(adviser_id)
            # may return None anyway
        if advice:
            return ('delay_infos' in advice and
                    'limit_date' in advice['delay_infos'] and
                    self.display_date(date=advice['delay_infos']['limit_date'])) or None

        return None

    @mutually_exclusive_parameters('adviser_id', 'advice')
    def print_advice_delay_days(self, adviser_id=None, advice=None):
        if advice is None:
            advice = self._get_advice(adviser_id)
            # may return None anyway
        if advice:
            return ('delay' in advice and advice['delay']) or None

        return None

    @mutually_exclusive_parameters('adviser_id', 'advice')
    def print_advice_given_date(self, adviser_id=None, advice=None):
        if advice is None:
            advice = self._get_advice(adviser_id)
            # may return None anyway
        if advice:
            return ('advice_given_on' in advice and self.display_date(date=advice['advice_given_on'])) or None

        return None

    @mutually_exclusive_parameters('adviser_id', 'advice')
    def print_advice_transmission_date(self, adviser_id=None, advice=None):
        return self.display_date(date=self._getItemAdviceTransmissionDate(adviser_id, advice))

    @mutually_exclusive_parameters('adviser_id', 'advice')
    def _getItemAdviceTransmissionDate(self, adviser_id=None, advice=None):
        """
        :return: The date as a string when the finance service received the advice request.
                 No matter if a legal delay applies on it or not.
        """
        if advice is None:
            advice = self._get_advice(adviser_id)
            # may return None anyway
        if advice:
            return 'delay_started_on' in advice and advice['delay_started_on'] \
                   or self._getWorkFlowAdviceTransmissionDate() \
                   or None

        return None

    def _getWorkFlowAdviceTransmissionDate(self):

        """
        :return: The date as a string when the finance service received the advice request if no legal delay applies.
        """

        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)

        wf_present_transition = list(cfg.getTransitionsForPresentingAnItem())
        item_advice_states = cfg.itemAdviceStates

        if 'itemfrozen' in item_advice_states and 'itemfreeze' not in wf_present_transition:
            wf_present_transition.append('itemfreeze')

        for item_transition in wf_present_transition:
            event = getLastWFAction(self.context, item_transition)
            if event and 'review_state' in event and event['review_state'] in item_advice_states:
                return event['time']

        return None

    def print_item_state(self):
        return self.translate(self.real_context.queryState())

    def print_creator_name(self):
        creator = api.user.get(self.real_context.Creator())
        return creator and creator.getProperty('fullname') or self.real_context.Creator()

    def print_item_number_within_category(self, listTypes=['normal', 'late'], default=''):
        res = default

        if self.real_context.hasMeeting() and \
           self.real_context.getListType() in listTypes and \
           self.real_context.getCategory():
            meeting = self.real_context.getMeeting()
            context_category = self.real_context.getCategory()
            context_uid = self.real_context.UID()
            count = 0

            for brain in meeting.getItems(listTypes=listTypes,
                                          ordered=True,
                                          theObjects=False,
                                          additional_catalog_query={'getCategory': context_category},
                                          unrestricted=True):
                count += 1
                if brain.UID == context_uid:
                    break

            res = str(count)
        return res

    def print_completeness_date(self, completeness_action, format='%d/%m/%Y'):
        completeness_changes_adapter = getAdapter(self.real_context,
                                                  IImioHistory,
                                                  'completeness_changes')
        last_action = getLastAction(completeness_changes_adapter, action=completeness_action)
        if (last_action):
            return last_action['time'].strftime(format)
        else:
            return None


class MCMeetingDocumentGenerationHelperView(MeetingDocumentGenerationHelperView):
    """Specific printing methods used for meeting."""

    def _is_in_value_dict(self, item, value_map={}):
        for key in value_map.keys():
            if self._get_value(item, key) in value_map[key]:
                return True
        return False

    def _filter_items(self, items, included_values={}, excluded_values={}):
        """
        Filters the items based on included_values and excluded_values.
        :param items:
        :param included_values:
        :param excluded_values:
        :return:
        """
        if not included_values and not excluded_values:
            # If there are no filter criterion, it's useless to iterate.
            return items

        result = []
        for item in items:
            if included_values and not self._is_in_value_dict(item, included_values):
                continue
            elif excluded_values and self._is_in_value_dict(item, excluded_values):
                continue
            result.append(item)
        return result

    def _get_value(self, item, value_name):
        if hasattr(item, value_name):
            return self.getDGHV(item).display(value_name)
        else:
            raise AttributeError

    def get_grouped_items(self, itemUids, listTypes=['normal'],
                          group_by=[], included_values={}, excluded_values={},
                          ignore_review_states=[], privacy='*'):

        """
        :param listTypes: is a list that can be filled with 'normal' and/or 'late ...
        :param group_by: is a list and each element can be either 'listTypes', 'category',
                         'proposingGroup' or a field name as described in MeetingItem Schema
        :param included_values: a Map to filter the returned items regarding the value of a given field.
                for example : {'proposingGroup':['Secrétariat communal',
                                                 'Service informatique',
                                                 'Service comptabilité']}
        :param excluded_values: a Map to filter the returned items regarding the value of a given field.
                for example : {'proposingGroup':['Secrétariat communal',
                                                 'Service informatique',
                                                 'Service comptabilité']}
        :param privacy: can be '*' or 'public' or 'secret'

        :return: a list of list of list ... (late or normal or both) items (depending on p_listTypes)
                 in the meeting order but wrapped in defined group_by if not empty.
        Every group condition defined increase the depth of this collection.
        """

        # Retrieve the list of items
        query = {}
        if privacy != '*':
            query['privacy'] = privacy
        if ignore_review_states:
            query['review_state'] = {'not': ignore_review_states}

        brains = self.real_context.getItems(
            uids=itemUids,
            listTypes=listTypes,
            ordered=True,
            theObjects=False,
            additional_catalog_query=query)

        items = [brain.getObject() for brain in brains]
        # because we can't assume included and excluded values are indexed in catalog.
        items = self._filter_items(items, included_values, excluded_values)

        if not group_by:
            return items

        res = []

        if isinstance(group_by, str):
            group_by = [group_by]

        for item in items:
            # compute result keeping item original order and repeating groups if needed
            node = res

            for group in group_by:
                value = self._get_value(item, group)

                if len(node) == 0 or node[-1][0] != value:
                    node.append([value])

                node = node[-1]

            if not isinstance(node[-1], (list)):
                node.append([])

            node[-1].append(item)

        return res

    def get_multiple_level_printing(self, itemUids, listTypes=['normal'],
                                    included_values={}, excluded_values={},
                                    ignore_review_states=[], privacy='*',
                                    level_number=1, text_pattern='{0}'):
        """

        :param listTypes: is a list that can be filled with 'normal' and/or 'late ...
        :param included_values: a Map to filter the returned items regarding the value of a given field.
                for example : {'proposingGroup':['Secrétariat communal',
                                                 'Service informatique',
                                                 'Service comptabilité']}
        :param excluded_values: a Map to filter the returned items regarding the value of a given field.
                for example : {'proposingGroup':['Secrétariat communal',
                                                 'Service informatique',
                                                 'Service comptabilité']}
        :param privacy: can be '*' or 'public' or 'secret'
        :param level_number: number of sublist we want
        :param text_pattern: text formatting with one string-param like this : 'xxx {0} yyy'
        This method to be used to have a multiple sublist based on an hierarchy in id's category like this :
            X.X.X.X (we want 4 levels of sublist).
            For have label, except first level and last level,
            we have the label in description's category separated by '|'
            For exemple : If we have A.1.1.4, normaly, we have in description this : subTitle1|subTitle2
                          If we have A.1.1, normaly, we have in description this : subTitle1
                          If we have A.1, normaly, we have in description this : (we use Title)
                          The first value on id is keeping
        :return: a list with formated like this :
            [Title (with class H1...Hx, depending of level number x.x.x. in id), [items list of tuple :
            item with number (num, item)]]
        """
        res = OrderedDict()
        items = self.get_grouped_items(itemUids, listTypes=listTypes, group_by=[],
                                       included_values=included_values, excluded_values=excluded_values,
                                       ignore_review_states=ignore_review_states, privacy=privacy)
        # now we construct tree structure
        for item in items:
            category = item.getCategory(theObject=True)
            category_id = category.getCategoryId()
            cats_ids = category_id.split('.')  # Exemple : A.1.2.4
            cats_descri = category.Description().split('|')  # Exemple : Organisation et structures|Secteur Hospitalier
            max_level = min(len(cats_ids), level_number)
            res_key = ''
            catid = ''
            # create key in dico if needed
            for i, cat_id in enumerate(cats_ids):
                # first level
                if i == 0:
                    catid = cat_id
                    if text_pattern == 'description':
                        text = category.Description()
                    else:
                        text = text_pattern.format(catid)
                    keyid = '<h1>{0}</h1>'.format(text)
                    if keyid not in res:
                        res[keyid] = []
                    res_key = keyid
                # sub level except last
                elif 0 < i < (max_level - 1):
                    catid += '.{0}'.format(cat_id)
                    keyid = '<h{0}>{1}. {2}</h{0}>'.format(i + 1, catid, cats_descri[i - 1])
                    if keyid not in res:
                        res[keyid] = []
                    res_key = keyid
                # last level
                else:
                    keyid = '<h{0}>{1}</h{0}>'.format(i + 1, category.Title())
                    if keyid not in res:
                        res[keyid] = []
                    res_key = keyid
            res[res_key].append(('{0}.{1}'.format(category_id, len(res[res_key]) + 1), item))  # start numbering to 1
        return res


class MCFolderDocumentGenerationHelperView(FolderDocumentGenerationHelperView):

    def get_all_items_dghv_with_finance_advice(self, brains):
        """
        :param brains: the brains collection representing @Product.PloneMeeting.MeetingItem
        :return: an array of dictionary with onnly the items linked to a finance advics which contains 2 keys
                 itemView : the documentgenerator helper view of a MeetingItem.
                 advice   : the data from a single advice linked to this MeetingItem as extracted with getAdviceDataFor.
        """
        res = []

        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        finance_advice_ids = cfg.adapted().getUsedFinanceGroupIds()
        if finance_advice_ids:
            res = self.get_all_items_dghv_with_advice(brains, finance_advice_ids)
        return res
