# -*- coding: utf-8 -*-
#
# File: overrides.py
#
# Copyright (c) 2015 by Imio.be
#
# GNU General Public License (GPL)
#

import json
from eea.facetednavigation.criteria.interfaces import ICriteria
from Products.PloneMeeting.browser.views import FolderDocumentGenerationHelperView
from Products.PloneMeeting.indexes import _to_coded_adviser_index


class MCFolderDocumentGenerationHelperView(FolderDocumentGenerationHelperView):
    """ """

    def finance_advices_data(self, brains):
        """Compute finance advices data to use in template printing finance advice infos."""
        # get selected 'indexAdvisers' by finding the right faceted criterion
        criteria = ICriteria(self.real_context)._criteria()
        # get the 'indexAdvisers' value where adviser ids are stored
        advisers = []
        for criterion in criteria:
            if criterion.index == 'indexAdvisers':
                facetedQuery = json.loads(self.request.get('facetedQuery', '{}'))
                advisers = facetedQuery[criterion.__name__]

        # now build data
        # we will build following structure :
        # - a list of lists where :
        #   - first element is item;
        #   - next elements are a list of relevant advices data.
        # [
        #   [MeetingItemObject1, ['adviser_data_1', 'adviser_data_2', ]],
        #   [MeetingItemObject2, ['adviser_data_1', ]],
        #   ...
        # ]
        res = []
        advisers = set(advisers)
        for brain in brains:
            subres = {}
            item = brain.getObject()
            subres['item'] = item
            advisers_data = []
            # only keep relevant adviser data
            for groupId, advice in item.adviceIndex.iteritems():
                if advisers.intersection(set(_to_coded_adviser_index(item, groupId, advice))):
                    # we must keep this adviser
                    advisers_data.append(item.getAdviceDataFor(item, groupId))
            subres['advices'] = advisers_data
            res.append(subres)
        return res
