# -*- coding: utf-8 -*-
#
# File: overrides.py
#
# Copyright (c) 2016 by Imio.be
#
# GNU General Public License (GPL)
#

from plone import api
from Products.MeetingCommunes.config import FINANCE_ADVICE_LEGAL_TEXT
from Products.MeetingCommunes.config import FINANCE_ADVICE_LEGAL_TEXT_NOT_GIVEN
from Products.MeetingCommunes.config import FINANCE_ADVICE_LEGAL_TEXT_PRE
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
            res.append('<a href="{0}">{1}</a><br/>'.format(url, title))
        return ('\n'.join(res))

    def printFormatedAdvice(self):
        ''' Printing Method use in templates :
            return formated advice'''
        res = []
        keys = self.context.getAdvicesByType().keys()
        for key in keys:
            for advice in self.context.getAdvicesByType()[key]:
                if advice['type'] == 'not_given':
                    continue
                comment = ''
                if advice['comment']:
                    comment = advice['comment']
                res.append({'type': self.translate(msgid=key, domain='PloneMeeting').encode('utf-8'),
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

    def printFinanceAdvice(self, case):
        """
        :param case: can be either 'initiative', 'legal', 'simple' or 'not_given'
        :return: an array dictionaries same as MeetingItem.getAdviceDataFor
        or empty if no advice matching the given case.
        """

        """
        case 'simple' means the financial advice was requested but without any delay.
        case 'legal' means the financial advice was requested with a delay. It a legal financial advice.
        case 'initiative' means the financial advice was given without being requested at the first place.
        case 'not_given' means the financial advice was requested with or without delay. But was ignored by the finance
         director.
        """
        result = []
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        finance_advice_ids = cfg.adapted().getUsedFinanceGroupIds()

        if finance_advice_ids and case in ['initiative', 'legal', 'simple', 'not_given']:
            advices = self.context.getAdviceDataFor(self.context.context)

            for finance_advice_id in finance_advice_ids:
                if finance_advice_id in advices:
                    advice = advices[finance_advice_id]
                else:
                    continue

                if advice['advice_given_on']:
                    if case == 'initiative' and advice['not_asked']:
                        result.append(advice)

                if case == 'initiative' and advice['not_asked']:
                    result.append(advice)
                elif 'delay_infos' in advice and not advice['not_asked']:
                    advice['item_transmitted_on'] = self.getItemFinanceAdviceTransmissionDate()
                    if case == 'simple' and not advice['delay_infos']:
                        result.append(advice)
                    elif advice['delay_infos']:
                        if advice['advice_given_on']:
                            if case == 'legal':
                                result.append(advice)
                        elif case == 'not_given':
                            result.append(advice)
        return result

    def getItemFinanceAdviceTransmissionDate(self):
        """
        :return: The date as a string when the finance service received the advice request.
                 No matter if a legal delay applies on it or not.
        """
        finance_id = self.context.adapted().getFinanceAdviceId()
        if finance_id:
            data = self.real_context.getAdviceDataFor(self.real_context, finance_id)
            if 'delay_infos' in data and 'delay_started_on_localized' in data['delay_infos'] \
                    and data['delay_infos']['delay_started_on_localized']:
                return data['delay_infos']['delay_started_on_localized']
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
                return event['time'].strftime('%d/%m/%Y')

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
