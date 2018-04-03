# -*- coding: utf-8 -*-
#
# File: overrides.py
#
# Copyright (c) 2016 by Imio.be
#
# GNU General Public License (GPL)
#

from plone import api
from Products.CMFPlone.utils import safe_unicode
from Products.MeetingCommunes.config import FINANCE_ADVICE_LEGAL_TEXT
from Products.MeetingCommunes.config import FINANCE_ADVICE_LEGAL_TEXT_NOT_GIVEN
from Products.MeetingCommunes.config import FINANCE_ADVICE_LEGAL_TEXT_PRE
from Products.PloneMeeting.browser.views import FolderDocumentGenerationHelperView
from Products.PloneMeeting.browser.views import ItemDocumentGenerationHelperView
from Products.PloneMeeting.browser.views import MeetingDocumentGenerationHelperView
from Products.PloneMeeting.utils import get_annexes
from Products.PloneMeeting.utils import getLastEvent


def formatedAssembly(assembly, focus):
    is_finish = False
    absentFind = False
    excuseFind = False
    res = []
    res.append('<p class="mltAssembly">')
    for ass in assembly:
        if is_finish:
            break
        lines = ass.split(',')
        cpt = 1
        my_line = ''
        for line in lines:
            if((line.find('Excus') >= 0 or line.find('Absent') >= 0) and focus == 'present') or \
                    (line.find('Absent') >= 0 and focus == 'excuse'):
                is_finish = True
                break
            if line.find('Excus') >= 0:
                excuseFind = True
                continue
            if line.find('Absent') >= 0:
                absentFind = True
                continue
            if (focus == 'absent' and not absentFind) or (focus == 'excuse' and not excuseFind):
                continue
            if cpt == len(lines):
                my_line = "%s%s<br />" % (my_line, line)
                res.append(my_line)
            else:
                my_line = "%s%s," % (my_line, line)
            cpt = cpt + 1
    if len(res) > 1:
        res[-1] = res[-1].replace('<br />', '')
    else:
        return ''
    res.append('</p>')
    return ('\n'.join(res))


class MCItemDocumentGenerationHelperView(ItemDocumentGenerationHelperView):
    """Specific printing methods used for item."""

    def _financialAdviceDetails(self):
        '''Get the financial advice signature date, advice type and comment'''
        res = {}
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        financialAdvice = cfg.adapted().getUsedFinanceGroupIds()[0]
        adviceData = self.context.getAdviceDataFor(self.context.context, financialAdvice)
        res['comment'] = 'comment' in adviceData\
            and adviceData['comment'] or ''
        advice_id = 'advice_id' in adviceData\
            and adviceData['advice_id'] or ''
        signature_event = advice_id and getLastEvent(getattr(self.context, advice_id), 'signFinancialAdvice') or ''
        res['out_of_financial_dpt'] = 'time' in signature_event and signature_event['time'] or ''
        res['out_of_financial_dpt_localized'] = res['out_of_financial_dpt']\
            and res['out_of_financial_dpt'].strftime('%d/%m/%Y') or ''
        # "positive_with_remarks_finance" will be printed "positive_finance"
        if adviceData['type'] == 'positive_with_remarks_finance':
            type_translated = self.translate(msgid='positive_finance',
                                             domain='PloneMeeting').encode('utf-8')
        else:
            type_translated = adviceData['type_translated'].encode('utf-8')
        res['advice_type'] = '<p><u>Type d\'avis:</u>  %s</p>' % type_translated
        res['delay_started_on_localized'] = 'delay_started_on_localized' in adviceData['delay_infos']\
            and adviceData['delay_infos']['delay_started_on_localized'] or ''
        res['delay_started_on'] = 'delay_started_on' in adviceData\
            and adviceData['delay_started_on'] or ''
        return res

    def getLegalTextForFDAdvice(self, isMeeting=False):
        '''
        Helper method. Return legal text for each advice type.
        '''
        adviceHolder = self.context.adapted().getItemWithFinanceAdvice()
        if not self._mayGenerateFDAdvice():
            return ''

        financialStuff = self._financialAdviceDetails()
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        financeAdviceId = cfg.adapted().getUsedFinanceGroupIds()[0]
        adviceInd = adviceHolder.adviceIndex[financeAdviceId]
        advice = adviceHolder.getAdviceDataFor(adviceHolder.context, financeAdviceId)
        hidden = advice['hidden_during_redaction']
        statusWhenStopped = advice['delay_infos']['delay_status_when_stopped']
        adviceType = adviceInd['type']
        comment = financialStuff['comment']
        adviceGivenOnLocalized = advice['advice_given_on_localized']
        delayStartedOnLocalized = advice['delay_infos']['delay_started_on_localized']
        delayStatus = advice['delay_infos']['delay_status']
        outOfFinancialdptLocalized = financialStuff['out_of_financial_dpt_localized']
        limitDateLocalized = advice['delay_infos']['limit_date_localized']

        if not isMeeting:
            res = FINANCE_ADVICE_LEGAL_TEXT_PRE.format(delayStartedOnLocalized)

        if not hidden and \
           adviceGivenOnLocalized and \
           (adviceType in (u'positive_finance', u'positive_with_remarks_finance',
                           u'negative_finance', u'cautious_finance')):
            if adviceType in (u'positive_finance', u'positive_with_remarks_finance'):
                adviceTypeFr = 'favorable'
            elif adviceType == u'negative_finance':
                adviceTypeFr = 'défavorable'
            else:
                # u'cautious_finance'
                adviceTypeFr = 'réservé'
            #if it's a meetingItem, return the legal bullshit.
            if not isMeeting:
                res = res + FINANCE_ADVICE_LEGAL_TEXT.format(
                    adviceTypeFr,
                    outOfFinancialdptLocalized
                )
            #if it's a meeting, returns only the type and date of the advice.
            else:
                res = "<p>Avis {0} du Directeur Financier du {1}</p>".format(
                    adviceTypeFr, outOfFinancialdptLocalized)

            if comment and adviceType == u'negative_finance':
                res = res + "<p>{0}</p>".format(comment)
        elif statusWhenStopped == 'stopped_timed_out' or delayStatus == 'timed_out':
            if not isMeeting:
                res = res + FINANCE_ADVICE_LEGAL_TEXT_NOT_GIVEN
            else:
                res = "<p>Avis du Directeur financier expir? le {0}</p>".format(limitDateLocalized)
        else:
            res = ''
        return res

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
        keys = self.context.getAdvicesByType().keys()
        for key in keys:
            for advice in self.context.getAdvicesByType()[key]:
                if advice['type'] == 'not_given' and exclude_not_given:
                    continue

                comment = ''
                type = key

                if 'hidden_during_redaction' in advice and advice['hidden_during_redaction']:
                    type = 'hidden_during_redaction'
                elif advice['comment']:
                    comment = advice['comment']

                res.append({'type': self.translate(msgid=type, domain='PloneMeeting').encode('utf-8'),
                            'name': advice['name'].encode('utf-8'),
                            'comment': comment})
        return res

    def printFormatedItemAssembly(self, focus=''):
        ''' Printing Method use in templates :
            return formated assembly with 'absent', 'excused', ... '''
        if focus not in ('present', 'excuse', 'absent'):
            return ''
        # ie: Pierre Helson, Bourgmestre, Président
        # focus is present, excuse or absent
        assembly = self.context.getItemAssembly().replace('<p>', '').replace('</p>', '').split('<br />')
        return formatedAssembly(assembly, focus)

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
        case 'legal_not_given' means the financial advice was requested with delay. But was ignored by the finance director.
        case 'simple_not_given' means the financial advice was requested without delay. But was ignored by the finance
         director.
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
                        if 'hidden_during_redaction' in advice and advice['hidden_during_redaction'] and not show_hidden:
                            message = self.translate('hidden_during_redaction', domain='PloneMeeting')
                            advice['type_translated'] = message
                            advice['type'] = 'hidden_during_redaction'
                            advice['comment'] = message

                        # check if advice was given on self initiative by the adviser
                        if advice['not_asked']:
                            if case == 'initiative' and advice['advice_given_on']:
                                result.append(advice)
                        else:
                            # set transmission date to adviser because advice was asked by the agent
                            advice['item_transmitted_on'] = self.getItemFinanceAdviceTransmissionDate(finance_advice_id)
                            if advice['item_transmitted_on']:
                                advice['item_transmitted_on_localized'] = self.display_date(
                                    date=advice['item_transmitted_on'])
                            else:
                                advice['item_transmitted_on_localized'] = ''

                            # If there is a delay then it is a legal advice. If not, it's a simple advice
                            if advice['delay']:
                                if check_given_or_not_cases(advice, case, 'legal', 'legal_not_given'):
                                    result.append(advice)
                            elif check_given_or_not_cases(advice, case, 'simple', 'simple_not_given'):
                                result.append(advice)
        return result

    def getItemFinanceDelayLimitDate(self):
        finance_id = self.context.adapted().getFinanceAdviceId()
        if finance_id:
            data = self.real_context.getAdviceDataFor(self.real_context, finance_id)
            return ('delay_infos' in data and 'limit_date_localized' in data['delay_infos']
                    and data['delay_infos']['limit_date_localized']) or None

        return None

    def getItemFinanceAdviceDelayDays(self):
        finance_id = self.context.adapted().getFinanceAdviceId()
        if finance_id:
            data = self.real_context.getAdviceDataFor(self.real_context, finance_id)
            return ('delay' in data and data['delay']) or None

        return None

    def getItemFinanceAdviceTransmissionDate(self, finance_id=None):
        """
        :return: The date as a string when the finance service received the advice request.
                 No matter if a legal delay applies on it or not.
        """
        if not finance_id:
            finance_id = self.context.adapted().getFinanceAdviceId()
            # may return None anyway

        if finance_id:
            data = self.real_context.getAdviceDataFor(self.real_context, finance_id)
            if 'delay_infos' in data and 'delay_started_on' in data['delay_infos'] \
                    and data['delay_infos']['delay_started_on']:
                return data['delay_infos']['delay_started_on']
            else:
                return self.getWorkFlowAdviceTransmissionStep()
        return None

    def getWorkFlowAdviceTransmissionStep(self):

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
            event = getLastEvent(self.context, item_transition)
            if event and 'review_state' in event and event['review_state'] in item_advice_states:
                return event['time']

        return None

    def print_item_state(self):
        return self.translate(self.real_context.queryState())

    def print_creator_name(self):
        return (self.real_context.portal_membership.getMemberInfo(str(self.real_context.Creator())) \
               and self.real_context.portal_membership.getMemberInfo(str(self.real_context.Creator()))['fullname']) \
               or str(self.real_context.Creator())


class MCMeetingDocumentGenerationHelperView(MeetingDocumentGenerationHelperView):
    """Specific printing methods used for meeting."""

    def printFormatedMeetingAssembly(self, focus=''):
        ''' Printing Method use in templates :
            return formated assembly with 'absent', 'excused', ... '''
        if focus not in ('present', 'excuse', 'absent'):
            return ''
        # ie: Pierre Helson, Bourgmestre, Président
        # focus is present, excuse or absent
        assembly = self.context.getAssembly().replace('<p>', '').replace('</p>', '').split('<br />')
        return formatedAssembly(assembly, focus)

    def _is_in_value_dict(self, item, value_map={}):
        for key in value_map.keys():
            if self._get_value(item, key) in value_map[key]:
                return True
        return False

    def _filter_item_uids(self, itemUids, ignore_review_states=[], privacy='*', included_values={}, excluded_values={}):
        """
        We just filter ignore_review_states here and privacy in order call getItems(uids), passing the correct uids and removing empty uids.
        :param privacy: can be '*' or 'public' or 'secret' or 'public_heading' or 'secret_heading'
        """
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)

        filteredItemUids = []
        uid_catalog = self.context.uid_catalog

        for itemUid in itemUids:
            obj = uid_catalog(UID=itemUid)[0].getObject()
            if obj.queryState() in ignore_review_states:
                continue
            elif not (privacy == '*' or obj.getPrivacy() == privacy):
                continue
            elif included_values and not self._is_in_value_dict(obj, included_values):
                continue
            elif excluded_values and self._is_in_value_dict(obj, excluded_values):
                continue
            filteredItemUids.append(itemUid)
        return filteredItemUids

    def _renumber_item(self, items, firstNumber):
        """
        :return: a list of tuple with first element the number and second element the item itself
        """
        i = firstNumber
        res = []
        for item in items:
            res.append((i, item))
            i = i + 1
        return res

    def _get_list_type_value(self, item):
        return self.translate(item.getListType())

    def _get_value(self, item, value_name):
        if value_name == 'listType' or value_name == 'listTypes':
            return self._get_list_type_value(item)
        elif value_name == 'category' or 'proposingGroup':
            return self.getDGHV(item).display(value_name)
        elif item.getField(value_name):
            return item.getField(value_name).get(item)

    def get_grouped_items(self, itemUids, listTypes=['normal'],
                          group_by=[], included_values={}, excluded_values={},
                          ignore_review_states=[], privacy='*',
                          firstNumber=1, renumber=False):

        """

        :param listTypes: is a list that can be filled with 'normal' and/or 'late ...
        :param group_by: Can be either 'listTypes', 'category', 'proposingGroup' or a field name as described in MettingItem Schema
        :param included_values: a Map to filter the returned items regarding the value of a given field.
                for example : {'proposingGroup':['Secrétariat communal', 'Service informatique', 'Service comptabilité']}
        :param excluded_values: a Map to filter the returned items regarding the value of a given field.
                for example : {'proposingGroup':['Secrétariat communal', 'Service informatique', 'Service comptabilité']}
        :param privacy: can be '*' or 'public' or 'secret'
        :param firstNumber: If renumber is True, a list of tuple
           will be return with first element the number and second element, the item.
           In this case, the firstNumber value can be used.'
        :return: a list of list of list ... (late or normal or both) items (depending on p_listTypes) in the meeting order but wrapped in defined group_by if not empty.
                every group condition defined increase the depth of this collection.
        """

        # Retrieve the list of items
        filteredItemUids = self._filter_item_uids(itemUids, ignore_review_states, privacy, included_values, excluded_values)

        if not filteredItemUids:
            return []
        else:
            items = self.real_context.getItems(uids=filteredItemUids, listTypes=listTypes, ordered=True)
            if renumber:
                items = self._renumber_item(items, firstNumber)

        if not group_by:
            return items

        res = []

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
                          firstNumber=1, level_number=1, text_pattern='{0}'):
        """

        :param listTypes: is a list that can be filled with 'normal' and/or 'late ...
        :param included_values: a Map to filter the returned items regarding the value of a given field.
                for example : {'proposingGroup':['Secrétariat communal', 'Service informatique', 'Service comptabilité']}
        :param excluded_values: a Map to filter the returned items regarding the value of a given field.
                for example : {'proposingGroup':['Secrétariat communal', 'Service informatique', 'Service comptabilité']}
        :param privacy: can be '*' or 'public' or 'secret'
        :param firstNumber: If renumber is True, a list of tuple
           will be return with first element the number and second element, the item.
           In this case, the firstNumber value can be used.'
        :param level_number: number of sublist we want
        :param text_pattern: text formatting with one string-param like this : 'xxx {0} yyy'
        This method to be used to have a multiple sublist based on an hierarchy in id's category like this :
            X.X.X.X (we want 4 levels of sublist).
            For have label, except first level and last level, we have the label in description's category separated by '|'
            For exemple : If we have A.1.1.4, normaly, we have in description this : subTitle1|subTitle2
                          If we have A.1.1, normaly, we have in description this : subTitle1
                          If we have A.1, normaly, we have in description this : (we use Title)
                          The first value on id is keeping
        :return: a list with formated like this :
            [Title (with class H1...Hx, depending of level number x.x.x. in id), [items list of tuple :
            item with number (num, item)]]
        """
        res = OrderedDict()
        items = self.get_grouped_items(itemUids, listTypes, [], included_values, excluded_values,
                ignore_review_states, privacy, firstNumber, False)

        # now we construct tree structure
        for item in items:
            category = item.getCategory(theObject=True)
            category_id = category.getCategoryId()
            cats_ids = category_id.split('.')  # Exemple : A.1.2.4
            cats_descri = category.Description().split('|')  # Exemple : Organisation et structures|Secteur Hospitalier
            max_level = min(len(cats_ids), level_number)
            res_key = ''
            # create key in dico if needed
            for i, cat_id in enumerate(cats_ids):
                # first level
                if i == 0:
                    catid = cat_id
                    text = text_pattern.format(catid)
                    keyid = '<h1>{0}</h1>'.format(text)
                    if keyid not in res:
                        res[keyid] = []
                    res_key = keyid
                # sub level except last
                elif 0 < i < (max_level-1):
                    catid += '.{0}'.format(cat_id)
                    keyid = '<h{0}>{1}. {2}</h{0}>'.format(i+1, catid, cats_descri[i-1])
                    if keyid not in res:
                        res[keyid] = []
                    res_key = keyid
                #last level
                else:
                    keyid = '<h{0}>{1}</h{0}>'.format(i+1, category.Title())
                    if keyid not in res:
                         res[keyid] = []
                    res_key = keyid
            res[res_key].append(('{0}.{1}'.format(category_id, len(res[res_key])+1), item)) # start numbering to 1
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

        for brain in brains:
            item = brain.getObject()
            advices = item.getAdviceDataFor(item)
            if advices:
                for advice in advices:
                    if advice in finance_advice_ids:
                        res.append({'itemView': self.getDGHV(item), 'advice': advices[advice]})

        return res
