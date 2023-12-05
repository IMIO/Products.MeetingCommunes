# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#

from collections import OrderedDict
from imio.helpers.content import get_user_fullname
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
from Products.PloneMeeting.utils import get_person_from_userid
from zope.component import getAdapter

import cgi


class MCItemDocumentGenerationHelperView(ItemDocumentGenerationHelperView):
    """Specific printing methods used for item."""

    def print_all_annexes(self, portal_types=['annex'], filters={}, with_icon=False, with_filename=False):
        """
        Printing Method use in templates :
        return all viewable annexes for item
        @param: filters is a dict of {"attribute" : value}.
        It excludes all non matching annex from the result.
        Example : {'confidential': True, 'publishable': False}
        possible keys are : 'confidential', 'to_print', 'to_sign' and 'publishable' (all are bool or None)
        """
        res = []
        annexes = get_annexes(self.context, portal_types=portal_types)
        mimetypes_registry = self.portal.mimetypes_registry
        if filters:
            effective_annexes = []
            for annex in annexes:
                use_this_annex = True
                for attribute, value in filters.items():
                    if getattr(annex, attribute) != value:
                        use_this_annex = False
                        break
                if use_this_annex:
                    effective_annexes.append(annex)
            annexes = effective_annexes

        for annex in annexes:
            url = annex.absolute_url()
            title = safe_unicode(cgi.escape(annex.Title()))
            file_type_icon = u''
            if with_icon:
                mime_type = mimetypes_registry.lookup(annex.file.contentType)[0]
                file_type_icon = u'&nbsp;<img src="{0}/{1}"/>'.format(self.portal.absolute_url(),
                                                                      mime_type.icon_path)
            annex_type_icon = u'<img src="{0}/{1}"/>'.format(
                self.portal.absolute_url(),
                self.real_context.categorized_elements[annex.UID()]['icon_url'])
            # sometimes filename may be None
            if annex.file.filename:
                extension = annex.file.filename.split(u'.')[-1]
                # escape just in case there is no file extension
                file_info = u'&nbsp;({0})'.format(safe_unicode(cgi.escape(extension)))
            else:
                file_info = u'&nbsp;(???)'

            res.append(u'<p>{0}&nbsp;<a href="{1}">{2}</a>{3}{4}</p>'.format(
                annex_type_icon,
                url,
                title,
                file_type_icon,
                file_info))
            if with_filename:
                file_name = safe_unicode(cgi.escape(annex.file.filename))
                res.append(u'<p><i>{0}</i></p>'.format(file_name))
        return u'\n'.join(res)

    def print_formated_advice(self, exclude_not_given=True):
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

    def print_deliberation(self, xhtmlContents=[], **kwargs):
        """
        Print the full item deliberation and includes the finance advices
        :param contents: contents to print, include 'finance_advices'
        to specify where to put the finance advices.
        :param kwargs: print_formatted_finance_advice and printXhtml kwargs
        :return: xhtml str representing the full item deliberation
        """
        if not xhtmlContents:
            contents = (
                'motivation',
                'finance_advices',
                'decision'
            )
            item = self.real_context
            # build new list or it updates existing list
            xhtmlContents = list(xhtmlContents)
            for content in contents:
                if content == 'finance_advices':
                    xhtmlContents.append(self.print_formatted_finance_advice(
                        finance_advices_template=kwargs.pop('finance_advices_formats', None),
                        finance_used_cases=kwargs.pop('finance_used_cases', None)
                    ))
                elif content in dir(item):
                    field = item.Schema().getField(content)  # get the field from the schema
                    content_accessor = getattr(item, field.accessor)  # get the accessor method from item
                    xhtmlContents.append(content_accessor())
                else:
                    xhtmlContents.append(content)

        return super(MCItemDocumentGenerationHelperView, self).print_deliberation(
            xhtmlContents, **kwargs)

    def print_formatted_finance_advice(self,
                                       finance_used_cases=[],
                                       finance_advices_template={}):
        """
        Print the finance advices based on legal cases and a template.
        :param finance_used_cases: legal cases among 'initiative', 'legal', 'simple',
                                                  'simple_not_given', 'legal_not_given
        :param finance_advices_template: dict with the legal case as key and the pattern as value
        :return: a xhtml str representing finance advices
        """
        if not finance_used_cases:
            finance_used_cases = (
                'initiative', 'legal', 'simple', 'simple_not_given', 'legal_not_given')
        if not finance_advices_template:
            finance_advices_template = {
                "simple":
                    u"<p>Considérant l'avis {type_translated} {by} {adviser} "
                    u"remis en date du {advice_given_on_localized},</p>",

                "simple_not_given":
                    u"<p>Considérant l'avis non rendu par {prefix} {adviser}</p>",

                "legal":
                    u"<p>Considérant la transmission du dossier {to} {adviser} "
                    u"pour avis prealable en date du {item_transmitted_on_localized},</p>"
                    u"<p>Considérant l'avis {type_translated} {by} {adviser} "
                    u"remis en date du {advice_given_on_localized},</p>",

                "legal_not_given":
                    u"<p>Considérant la transmission du dossier {to} {adviser} "
                    u"pour avis prealable en date du {item_transmitted_on_localized},</p>"
                    u"<p>Considérant l'avis non rendu par {prefix} {adviser},</p>",

                "initiative":
                    u"<p>Considérant l'avis d'initiative {type_translated} {to} {adviser} "
                    u"remis en date du {advice_given_on_localized},</p>"
            }
        formatted_finance_advice = ""
        finances_advices = {case: self.print_finance_advice(case)
                            for case in finance_advices_template.keys()}
        for case, advices in finances_advices.items():
            if case not in finance_used_cases:
                continue
            for advice in advices:
                if self.get_contact_infos(userid=advice['creator_id'])['held_position_label']:
                    adviser = \
                        self.get_contact_infos(userid=advice['creator_id'])['held_position_label']
                else:
                    adviser = advice['name']

                formatted_finance_advice += finance_advices_template[case].format(
                    type_translated=advice["type_translated"].lower(),
                    adviser=adviser,
                    prefix=self._get_prefix_for_finance_advice('prefix', advice),
                    to=self._get_prefix_for_finance_advice('to', advice),
                    by=self._get_prefix_for_finance_advice('by', advice),
                    item_transmitted_on_localized=advice.get("item_transmitted_on_localized"),
                    advice_given_on_localized=advice.get("advice_given_on_localized")
                )
        return formatted_finance_advice.encode('utf-8')

    def _get_prefix_for_finance_advice(self, type, advice):
        """
        Return prefix for a given finance advise
        :param type: type of prefix, must be among 'prefix', 'by', 'to'
        :param advice: advice for which prefix must be
        :return:
        """
        PREFIXS = {
            ('prefix', 'M'): u'le',
            ('prefix', 'F'): u'la',
            ('by', 'M'): u'du',
            ('by', 'F'): u'de la',
            ('to', 'M'): u'au',
            ('to', 'F'): u'à la',
        }
        if advice['type'] == 'not_given' \
                or not self.get_contact_infos(userid=advice['creator_id'])['person']:
            # We can't bind the adviser with a contact's person so we must guest the gender
            if 'trice' in advice['name'].lower():
                gender = 'F'
            else:
                gender = 'M'
        else:  # we use the contact's gender
            gender = get_person_from_userid(advice['creator_id']).gender

        return PREFIXS[(type, gender)]

    def print_finance_advice(self, cases, show_hidden=False):
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
        return self.translate(self.real_context.query_state())

    def print_creator_name(self):
        return get_user_fullname(self.real_context.Creator())

    def print_item_number_ordinal(self, ordinals={u'1': u'er', u'default': u'ème'}):
        """
        Get the ordinal of the item number.
        :param ordinals: ordinals to apply : {u'1': u'er', u'default': u'ème'} for french
        :return: the ordinal of the item number
        """
        item_number = self.real_context.getItemNumber(for_display=True)

        return ordinals.get(item_number, ordinals['default'])

    def item_number_to_letters(self, number):
        """
        Convert a number to letters following the same principle as a numbered list with letters
        ex: 1 => a, 3 => b, 27 => aa, 28 => ab,...
        :param number: the number to convert
        :return: converted number in letters
        """
        letters = ""
        while number > 0:
            number, remainder = divmod(number - 1, 26)
            # We use the ascii table to get the correct letter ('a' start at index 97)
            letters = chr(97 + remainder) + letters
        return letters

    def print_item_number_with_sublevel(self, mode="alpha", num_format="{0}.{1}"):
        """
        Print the item number with sub-level number
        which can be : simple number (mode=None),
        numeral adverb (mode="adverb") or alphabetical letter (mode="alpha")
        :param mode: None, "alpha" or "adverb"
        :param num_format: format of the printed number
        :return: item number formatted
        """
        ADVERBS = {
            1: "bis",
            2: "ter",
            3: "quater",
            4: "quinquies",
            5: "sexies",
            6: "septies",
            7: "octies",
            8: "nonies",
            9: "decies",
            10: "undecies",
            11: "duodecies",
            12: "terdecies",
            13: "quaterdecies",
            14: "quinquies",
            15: "sexies",
            16: "septies",
            17: "octodecies",
            18: "novodecies",
            19: "vicies", }

        item_number = self.real_context.getItemNumber()
        first_part = int(item_number / 100)
        second_part = item_number % 100
        if second_part:
            if mode == "alpha":
                second_part = self.item_number_to_letters(second_part)
            if mode == "adverb":
                second_part = ADVERBS.get(second_part, second_part)

            return num_format.format(first_part, second_part)
        else:
            return str(first_part)

    def print_item_number_within_category(self, list_types=['normal', 'late'], default=''):
        res = default

        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        # proposingGroup
        if 'category' not in cfg.getUsedItemAttributes():
            catalog_index = 'getProposingGroup'
            context_category = self.real_context.getProposingGroup()
        else:
            # category
            catalog_index = 'getCategory'
            context_category = self.real_context.getCategory()

        if self.real_context.hasMeeting() and \
           self.real_context.getListType() in list_types and \
           context_category:
            meeting = self.real_context.getMeeting()
            context_uid = self.real_context.UID()
            count = 0

            for brain in meeting.get_items(list_types=list_types,
                                           ordered=True,
                                           the_objects=False,
                                           additional_catalog_query={catalog_index: context_category},
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

    def _is_in_value_dict(self, item, value_map={}, unrestricted=False):
        for key in value_map.keys():
            if self._get_value(item, key, unrestricted) in value_map[key]:
                return True
        return False

    def _filter_items(self, items, included_values={}, excluded_values={}, unrestricted=False):
        """
        Filters the items based on included_values and excluded_values.
        :param items:
        :param included_values:
        :param excluded_values:
        :param unrestricted:
        :return:
        """
        if not included_values and not excluded_values:
            # If there are no filter criterion, it's useless to iterate.
            return items

        result = []
        for item in items:
            if included_values and not self._is_in_value_dict(item, included_values, unrestricted):
                continue
            elif excluded_values and self._is_in_value_dict(item, excluded_values, unrestricted):
                continue
            result.append(item)
        return result

    def _get_value(self, item, value_name, unrestricted=False):
        if hasattr(item, value_name):
            return self.getDGHV(item).display(value_name, bypass_check_permission=unrestricted)
        else:
            custom_func_name = '_group_by_' + value_name
            if hasattr(self, custom_func_name):
                return getattr(self, custom_func_name)(item)
            else:
                raise AttributeError

    def _group_by_org_first_level(self, item):
        """Custom group_by to group elements by organization first level,
           useful when using suborganizations"""
        org = item.getProposingGroup(theObject=True)
        return org.get_organizations_chain()[1]

    def _group_by_org_first_level_title(self, item):
        """Custom group_by to group elements by organization first level title,
           useful when using suborganizations"""
        return self._group_by_org_first_level(item).Title()

    @staticmethod
    def _is_different_grouping_as_previous_item(node, value, level):
        if len(node) == 0:
            return True

        i = 0
        grouping = []
        while i <= level:
            if not isinstance(grouping, list):
                return True
            grouping = node[-1]
            i += 1

        if isinstance(grouping, list):
            grouping_value = grouping[0]
        else:
            grouping_value = grouping

        return grouping_value != value

    def get_grouped_items(self, itemUids, list_types=['normal'],
                          group_by=[], included_values={}, excluded_values={},
                          ignore_review_states=[], privacy='*', unrestricted=False,
                          additional_catalog_query={}):

        """
        :param list_types: is a list that can be filled with 'normal' and/or 'late ...
        :param group_by: is a list and each element can be either 'list_types', 'category',
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
        :param unrestricted: when True, will return every items, including no viewable ones
        :param additional_catalog_query: additional classic portal_catalog query to filter out items
                for example : {'getProposingGroup': proposing_group_uid}

        :return: a list of list of list ... (late or normal or both) items (depending on p_list_types)
                 in the meeting order but wrapped in defined group_by if not empty.
        Every group condition defined increase the depth of this collection.
        """

        # Retrieve the list of items
        query = additional_catalog_query.copy()
        if privacy != '*':
            query['privacy'] = privacy
        if ignore_review_states:
            query['review_state'] = {'not': ignore_review_states}

        # do not filter on selected itemUids when unrestricted=True
        # except if length itemUids < length all visible items
        if unrestricted:
            visible_items = self.real_context.get_items(
                ordered=False, the_objects=False, additional_catalog_query=query)
            if len(itemUids) == len(visible_items):
                # items were not unselected
                itemUids = []

        items = self.real_context.get_items(
            uids=itemUids,
            list_types=list_types,
            ordered=True,
            the_objects=True,
            additional_catalog_query=query,
            unrestricted=unrestricted)

        # because we can't assume included and excluded values are indexed in catalog.
        items = self._filter_items(items, included_values, excluded_values, unrestricted)

        if not group_by:
            return items

        res = []

        if isinstance(group_by, str):
            group_by = [group_by]

        for item in items:
            # compute result keeping item original order and repeating groups if needed
            node = res
            level = 0
            for group in group_by:
                value = self._get_value(item, group, unrestricted)

                if self._is_different_grouping_as_previous_item(node, value, level):
                    node.append([value])

                node = node[-1]
                level += 1

            if not isinstance(node[-1], list):
                node.append([])

            node[-1].append(item)

        return res

    def get_multiple_level_printing(self, itemUids, list_types=['normal'],
                                    included_values={}, excluded_values={},
                                    ignore_review_states=[], privacy='*',
                                    level_number=1, text_pattern='{0}', unrestricted=False):
        """

        :param list_types: is a list that can be filled with 'normal' and/or 'late ...
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
        :param unrestricted: when True, will return every items, including no viewable ones

        :return: a list with formated like this :
            [Title (with class H1...Hx, depending of level number x.x.x. in id), [items list of tuple :
            item with number (num, item)]]
        """
        res = OrderedDict()
        items = self.get_grouped_items(itemUids, list_types=list_types, group_by=[],
                                       included_values=included_values, excluded_values=excluded_values,
                                       ignore_review_states=ignore_review_states, privacy=privacy,
                                       unrestricted=unrestricted)
        # now we construct tree structure
        for item in items:
            category = item.getCategory(theObject=True)
            category_id = category.category_id
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
