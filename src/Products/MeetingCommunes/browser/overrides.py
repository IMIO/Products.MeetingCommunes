# -*- coding: utf-8 -*-
#
# File: overrides.py
#
# Copyright (c) 2016 by Imio.be
#
# GNU General Public License (GPL)
#

from zope.i18n import translate
from plone import api
from Products.MeetingCommunes.config import FINANCE_ADVICE_LEGAL_TEXT
from Products.MeetingCommunes.config import FINANCE_ADVICE_LEGAL_TEXT_NOT_GIVEN
from Products.MeetingCommunes.config import FINANCE_ADVICE_LEGAL_TEXT_PRE
from Products.PloneMeeting.browser.views import ItemDocumentGenerationHelperView
from Products.PloneMeeting.browser.views import MeetingDocumentGenerationHelperView
from Products.PloneMeeting.utils import getLastEvent


class MCItemDocumentGenerationHelperView(ItemDocumentGenerationHelperView):
    """Specific printing methods used for item."""

    def _mayGenerateFDAdvice(self):
        '''
          Returns True if the current user has the right to generate the
          Financial Director Advice template.
          It is the case if finance advice is no more managed by finances advisers.
        '''
        tool = api.portal.get_tool('portal_plonemeeting')
        adviceHolder = self.context.adapted().getItemWithFinanceAdvice()
        financeAdviceId = self.context.adapted().getFinanceAdviceId()
        if financeAdviceId:
            financeAdviceGroup = getattr(tool, financeAdviceId)
            if financeAdviceId and \
                (adviceHolder.adviceIndex[financeAdviceId]['hidden_during_redaction'] is False or
                 financeAdviceGroup.userPloneGroups('advisers') or
                 adviceHolder.adviceIndex[adviceHolder.getFinanceAdvice()]['advice_editable'] is False):
                return True
        return False

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
            type_translated = translate('positive_finance',
                                        domain='PloneMeeting',
                                        context=self.context.REQUEST).encode('utf-8')
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
        import ipdb; ipdb.set_trace()
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


class MCMeetingDocumentGenerationHelperView(MeetingDocumentGenerationHelperView):
    """Specific printing methods used for meeting."""
