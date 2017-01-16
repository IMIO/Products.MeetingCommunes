# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 by Imio.be
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

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.Five import BrowserView
from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.utils import _checkPermission
from Products.MeetingCommunes.config import POSITIVE_FINANCE_ADVICE_SIGNABLE_BY_REVIEWER


class AdviceWFConditionsView(BrowserView):
    """
      This is a view that manage workflow guards for the advice.
      It is called by the guard_expr of meetingadvice workflow transitions.
    """
    security = ClassSecurityInfo()

    security.declarePublic('mayBackToProposedToFinancialController')

    def mayBackToProposedToFinancialController(self):
        '''
        '''
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayBackToProposedToFinancialEditor')

    def mayBackToProposedToFinancialEditor(self):
        '''
        '''
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayBackToProposedToFinancialReviewer')

    def mayBackToProposedToFinancialReviewer(self):
        '''
        '''
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayBackToProposedToFinancialManager')

    def mayBackToProposedToFinancialManager(self):
        '''
        '''
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayProposeToFinancialEditor')

    def mayProposeToFinancialEditor(self):
        '''
        '''
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayProposeToFinancialReviewer')

    def mayProposeToFinancialReviewer(self):
        '''
        '''
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayProposeToFinancialManager')

    def mayProposeToFinancialManager(self):
        '''A financial manager may send the advice to the financial manager
           in any case (advice positive or negative) except if advice
           is still 'asked_again'.'''
        res = False
        if _checkPermission(ReviewPortalContent, self.context) and \
           not self.context.advice_type == 'asked_again':
            res = True
        return res

    security.declarePublic('maySignFinancialAdvice')

    def maySignFinancialAdvice(self):
        '''A financial reviewer may sign the advice if it is 'positive_finance'
           or 'not_required_finance', if not this will be the financial manager
           that will be able to sign it.'''
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
            # if POSITIVE_FINANCES_ADVICE_SIGNABLE_BY_REVIEWER is True, it means
            # that a finances reviewer may sign an item in place of the finances manager
            # except if it is 'negative_finance'
            if POSITIVE_FINANCE_ADVICE_SIGNABLE_BY_REVIEWER:
                if self.context.advice_type == 'negative_finance' and \
                   not self.context.queryState() == 'proposed_to_financial_manager':
                    res = False
            else:
                if not self.context.queryState() == 'proposed_to_financial_manager':
                    res = False
        return res


InitializeClass(AdviceWFConditionsView)
