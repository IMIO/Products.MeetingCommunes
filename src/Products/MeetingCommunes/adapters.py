# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------

from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from collections import OrderedDict
from imio.helpers.xhtml import xhtmlContentIsEmpty
from plone import api
from plone.memoize import ram
from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.MeetingCommunes import logger
from Products.MeetingCommunes.config import FINANCE_ADVICES_COLLECTION_ID
from Products.MeetingCommunes.config import FINANCE_GROUP_SUFFIXES
from Products.MeetingCommunes.config import FINANCE_WAITING_ADVICES_STATES
from Products.MeetingCommunes.interfaces import IMeetingCommunesWorkflowActions
from Products.MeetingCommunes.interfaces import IMeetingCommunesWorkflowConditions
from Products.MeetingCommunes.interfaces import IMeetingItemCommunesWorkflowActions
from Products.MeetingCommunes.interfaces import IMeetingItemCommunesWorkflowConditions
from Products.PloneMeeting.adapters import CompoundCriterionBaseAdapter
from Products.PloneMeeting.indexes import DELAYAWARE_ROW_ID_PATTERN
from Products.PloneMeeting.indexes import REAL_ORG_UID_PATTERN
from Products.PloneMeeting.interfaces import IMeetingConfigCustom
from Products.PloneMeeting.interfaces import IMeetingCustom
from Products.PloneMeeting.interfaces import IMeetingItemCustom
from Products.PloneMeeting.interfaces import IToolPloneMeetingCustom
from Products.PloneMeeting.Meeting import Meeting
from Products.PloneMeeting.Meeting import MeetingWorkflowActions
from Products.PloneMeeting.Meeting import MeetingWorkflowConditions
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.MeetingItem import MeetingItemWorkflowActions
from Products.PloneMeeting.MeetingItem import MeetingItemWorkflowConditions
from Products.PloneMeeting.model import adaptations
from Products.PloneMeeting.model.adaptations import WF_APPLIED
from Products.PloneMeeting.ToolPloneMeeting import ToolPloneMeeting
from zope.interface import implements


# Names of available workflow adaptations.
customwfAdaptations = list(MeetingConfig.wfAdaptations)
# remove the 'creator_initiated_decisions' as this is always the case in our wfs
if 'creator_initiated_decisions' in customwfAdaptations:
    customwfAdaptations.remove('creator_initiated_decisions')
# remove the 'archiving' as we do not handle archive in our wfs
if 'archiving' in customwfAdaptations:
    customwfAdaptations.remove('archiving')

MeetingConfig.wfAdaptations = customwfAdaptations

# states taken into account by the 'no_global_observation' wfAdaptation
noGlobalObsStates = list(adaptations.noGlobalObsStates)
noGlobalObsStates.append('accepted_but_modified')
noGlobalObsStates.append('pre_accepted')
adaptations.noGlobalObsStates = noGlobalObsStates

adaptations.WF_NOT_CREATOR_EDITS_UNLESS_CLOSED = ('delayed', 'refused', 'accepted',
                                                  'pre_accepted', 'accepted_but_modified')

RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE = {'meetingitemcommunes_workflow': 'meetingitemcommunes_workflow.itemcreated'}
adaptations.RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE = RETURN_TO_PROPOSING_GROUP_STATE_TO_CLONE


class CustomMeeting(Meeting):
    '''Adapter that adapts a meeting implementing IMeeting to the
       interface IMeetingCustom.'''

    implements(IMeetingCustom)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting

    # Implements here methods that will be used by templates
    security.declarePublic('getPrintableItems')

    def getPrintableItems(self, itemUids, listTypes=['normal'], ignore_review_states=[],
                          privacy='*', oralQuestion='both', toDiscuss='both', categories=[],
                          excludedCategories=[], org_uids=[], excludedGroupIds=[],
                          firstNumber=1, renumber=False):
        '''Returns a list of items.
           An extra list of review states to ignore can be defined.
           A privacy can also be given, and the fact that the item is an
           oralQuestion or not (or both). Idem with toDiscuss.
           Some specific categories can be given or some categories to exclude.
           We can also receive in p_groupIds organization uids to take into account.
           These 2 parameters are exclusive.  If renumber is True, a list of tuple
           will be return with first element the number and second element, the item.
           In this case, the firstNumber value can be used.'''
        # We just filter ignore_review_states here and privacy and call
        # getItems(uids), passing the correct uids and removing empty uids.
        # privacy can be '*' or 'public' or 'secret' or 'public_heading' or 'secret_heading'
        # oralQuestion can be 'both' or False or True
        # toDiscuss can be 'both' or 'False' or 'True'
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)

        # check filters
        filteredItemUids = []
        uid_catalog = self.context.uid_catalog
        for itemUid in itemUids:
            obj = uid_catalog(UID=itemUid)[0].getObject()
            if obj.queryState() in ignore_review_states:
                continue
            elif not (privacy == '*' or obj.getPrivacy() == privacy):
                continue
            elif not (oralQuestion == 'both' or obj.getOralQuestion() == oralQuestion):
                continue
            elif not (toDiscuss == 'both' or obj.getToDiscuss() == toDiscuss):
                continue
            elif categories and not obj.getCategory() in categories:
                continue
            elif org_uids and not obj.getProposingGroup() in org_uids:
                continue
            elif excludedCategories and obj.getCategory() in excludedCategories:
                continue
            elif excludedGroupIds and obj.getProposingGroup() in excludedGroupIds:
                continue
            filteredItemUids.append(itemUid)
        # in case we do not have anything, we return an empty list
        if not filteredItemUids:
            return []
        else:
            items = self.context.getItems(uids=filteredItemUids, listTypes=listTypes, ordered=True)
            if renumber:
                # return a list of tuple with first element the number and second
                # element the item itself
                i = firstNumber
                res = []
                for item in items:
                    res.append((i, item))
                    i = i + 1
                items = res
            return items

    def _getAcronymPrefix(self, group, groupPrefixes):
        '''This method returns the prefix of the p_group's acronym among all
           prefixes listed in p_groupPrefixes. If group acronym does not have a
           prefix listed in groupPrefixes, this method returns None.'''
        res = None
        groupAcronym = group.getAcronym()
        for prefix in groupPrefixes.iterkeys():
            if groupAcronym.startswith(prefix):
                res = prefix
                break
        return res

    def _getGroupIndex(self, group, groups, groupPrefixes):
        '''Is p_group among the list of p_groups? If p_group is not among
           p_groups but another group having the same prefix as p_group
           (the list of prefixes is given by p_groupPrefixes), we must conclude
           that p_group is among p_groups. res is -1 if p_group is not
           among p_group; else, the method returns the index of p_group in
           p_groups.'''
        prefix = self._getAcronymPrefix(group, groupPrefixes)
        if not prefix:
            if group not in groups:
                return -1
            else:
                return groups.index(group)
        else:
            for gp in groups:
                if gp.getAcronym().startswith(prefix):
                    return groups.index(gp)
            return -1

    def _insertGroupInCategory(self, categoryList, meetingGroup, groupPrefixes, groups, item=None):
        '''Inserts a group list corresponding to p_meetingGroup in the given
           p_categoryList, following meeting group order as defined in the
           main configuration (groups from the config are in p_groups).
           If p_item is specified, the item is appended to the group list.'''
        usedGroups = [g[0] for g in categoryList[1:]]
        groupIndex = self._getGroupIndex(meetingGroup, usedGroups, groupPrefixes)
        if groupIndex == -1:
            # Insert the group among used groups at the right place.
            groupInserted = False
            i = -1
            for usedGroup in usedGroups:
                i += 1
                if groups.index(meetingGroup) < groups.index(usedGroup):
                    if item:
                        categoryList.insert(i + 1, [meetingGroup, item])
                    else:
                        categoryList.insert(i + 1, [meetingGroup])
                    groupInserted = True
                    break
            if not groupInserted:
                if item:
                    categoryList.append([meetingGroup, item])
                else:
                    categoryList.append([meetingGroup])
        else:
            # Insert the item into the existing group.
            if item:
                categoryList[groupIndex + 1].append(item)

    def _insertItemInCategory(self, categoryList, item, byProposingGroup, groupPrefixes, groups):
        '''This method is used by the next one for inserting an item into the
           list of all items of a given category. if p_byProposingGroup is True,
           we must add it in a sub-list containing items of a given proposing
           group. Else, we simply append it to p_category.'''
        if not byProposingGroup:
            categoryList.append(item)
        else:
            group = item.getProposingGroup(True)
            self._insertGroupInCategory(categoryList, group, groupPrefixes, groups, item)

    security.declarePublic('getPrintableItemsByCategory')

    def getPrintableItemsByCategory(self, itemUids=[], listTypes=['normal'],
                                    ignore_review_states=[], by_proposing_group=False, group_prefixes={},
                                    privacy='*', oralQuestion='both', toDiscuss='both', categories=[],
                                    excludedCategories=[], groupIds=[], excludedGroupIds=[],
                                    firstNumber=1, renumber=False,
                                    includeEmptyCategories=False, includeEmptyGroups=False,
                                    forceCategOrderFromConfig=False):
        '''Returns a list of (late or normal or both) items (depending on p_listTypes)
           ordered by category. Items being in a state whose name is in
           p_ignore_review_state will not be included in the result.
           If p_by_proposing_group is True, items are grouped by proposing group
           within every category. In this case, specifying p_group_prefixes will
           allow to consider all groups whose acronym starts with a prefix from
           this param prefix as a unique group. p_group_prefixes is a dict whose
           keys are prefixes and whose values are names of the logical big
           groups. A privacy,A toDiscuss and oralQuestion can also be given, the item is a
           toDiscuss (oralQuestion) or not (or both) item.
           If p_forceCategOrderFromConfig is True, the categories order will be
           the one in the config and not the one from the meeting.
           If p_groupIds are given, we will only consider these proposingGroups.
           If p_includeEmptyCategories is True, categories for which no
           item is defined are included nevertheless. If p_includeEmptyGroups
           is True, proposing groups for which no item is defined are included
           nevertheless.Some specific categories can be given or some categories to exclude.
           These 2 parameters are exclusive.  If renumber is True, a list of tuple
           will be return with first element the number and second element, the item.
           In this case, the firstNumber value can be used.'''
        # The result is a list of lists, where every inner list contains:
        # - at position 0: the category object (MeetingCategory or MeetingGroup)
        # - at position 1 to n: the items in this category
        # If by_proposing_group is True, the structure is more complex.
        # listTypes is a list that can be filled with 'normal' and/or 'late'
        # oralQuestion can be 'both' or False or True
        # toDiscuss can be 'both' or 'False' or 'True'
        # privacy can be '*' or 'public' or 'secret'
        # Every inner list contains:
        # - at position 0: the category object
        # - at positions 1 to n: inner lists that contain:
        #   * at position 0: the proposing group object
        #   * at positions 1 to n: the items belonging to this group.
        def _comp(v1, v2):
            if v1[0].getOrder(onlySelectable=False) < v2[0].getOrder(onlySelectable=False):
                return -1
            elif v1[0].getOrder(onlySelectable=False) > v2[0].getOrder(onlySelectable=False):
                return 1
            else:
                return 0
        res = []
        items = []
        tool = getToolByName(self.context, 'portal_plonemeeting')
        # Retrieve the list of items
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)

        items = self.context.getItems(uids=itemUids, listTypes=listTypes, ordered=True)

        if by_proposing_group:
            groups = tool.getMeetingGroups()
        else:
            groups = None
        if items:
            for item in items:
                # Check if the review_state has to be taken into account
                if item.queryState() in ignore_review_states:
                    continue
                elif not (privacy == '*' or item.getPrivacy() == privacy):
                    continue
                elif not (oralQuestion == 'both' or item.getOralQuestion() == oralQuestion):
                    continue
                elif not (toDiscuss == 'both' or item.getToDiscuss() == toDiscuss):
                    continue
                elif groupIds and not item.getProposingGroup() in groupIds:
                    continue
                elif categories and not item.getCategory() in categories:
                    continue
                elif excludedCategories and item.getCategory() in excludedCategories:
                    continue
                elif excludedGroupIds and item.getProposingGroup() in excludedGroupIds:
                    continue
                currentCat = item.getCategory(theObject=True)
                # Add the item to a new category, excepted if the
                # category already exists.
                catExists = False
                for catList in res:
                    if catList[0] == currentCat:
                        catExists = True
                        break
                if catExists:
                    self._insertItemInCategory(catList, item,
                                               by_proposing_group, group_prefixes, groups)
                else:
                    res.append([currentCat])
                    self._insertItemInCategory(res[-1], item,
                                               by_proposing_group, group_prefixes, groups)
        if forceCategOrderFromConfig or cmp(listTypes.sort(), ['late', 'normal']) == 0:
            res.sort(cmp=_comp)
        if includeEmptyCategories:
            meetingConfig = tool.getMeetingConfig(
                self.context)
            # onlySelectable = False will also return disabled categories...
            allCategories = [cat for cat in meetingConfig.getCategories(onlySelectable=False)
                             if api.content.get_state(cat) == 'active']
            usedCategories = [elem[0] for elem in res]
            for cat in allCategories:
                if cat not in usedCategories:
                    # Insert the category among used categories at the right
                    # place.
                    categoryInserted = False
                    for i in range(len(usedCategories)):
                        if allCategories.index(cat) < \
                           allCategories.index(usedCategories[i]):
                            usedCategories.insert(i, cat)
                            res.insert(i, [cat])
                            categoryInserted = True
                            break
                    if not categoryInserted:
                        usedCategories.append(cat)
                        res.append([cat])
        if by_proposing_group and includeEmptyGroups:
            # Include, in every category list, not already used groups.
            # But first, compute "macro-groups": we will put one group for
            # every existing macro-group.
            macroGroups = []  # Contains only 1 group of every "macro-group"
            consumedPrefixes = []
            for group in groups:
                prefix = self._getAcronymPrefix(group, group_prefixes)
                if not prefix:
                    group._v_printableName = group.Title()
                    macroGroups.append(group)
                else:
                    if prefix not in consumedPrefixes:
                        consumedPrefixes.append(prefix)
                        group._v_printableName = group_prefixes[prefix]
                        macroGroups.append(group)
            # Every category must have one group from every macro-group
            for catInfo in res:
                for group in macroGroups:
                    self._insertGroupInCategory(catInfo, group, group_prefixes,
                                                groups)
                    # The method does nothing if the group (or another from the
                    # same macro-group) is already there.
        if renumber:
            # items are replaced by tuples with first element the number and second element the item itself
            i = firstNumber
            tmp_res = []
            for cat in res:
                tmp_cat = [cat[0]]
                for item in cat[1:]:
                    tmp_cat.append((i, item))
                    i = i + 1
                tmp_res.append(tmp_cat)
            res = tmp_res
        return res

    security.declarePublic('getNumberOfItems')

    def getNumberOfItems(self, itemUids, privacy='*', categories=[], listTypes=['normal']):
        '''Returns the number of items depending on parameters.
           This is used in templates to know how many items of a particular kind exist and
           often used to determine the 'firstNumber' parameter of getPrintableItems/getPrintableItemsByCategory.'''
        # sometimes, some empty elements are inserted in itemUids, remove them...
        itemUids = [itemUid for itemUid in itemUids if itemUid != '']
        if not categories and privacy == '*':
            return len(self.context.getItems(uids=itemUids, listTypes=listTypes))
        # Either, we will have to filter (privacy, categories, late)
        filteredItemUids = []
        uid_catalog = getToolByName(self.context, 'uid_catalog')
        for itemUid in itemUids:
            obj = uid_catalog(UID=itemUid)[0].getObject()
            if not (privacy == '*' or obj.getPrivacy() == privacy):
                continue
            elif not (categories == [] or obj.getCategory() in categories):
                continue
            elif not obj.isLate() == bool(listTypes == ['late']):
                continue
            filteredItemUids.append(itemUid)
        return len(filteredItemUids)

    security.declarePublic('getPrintableItemsByNumCategory')

    def getPrintableItemsByNumCategory(self, listTypes=['normal'], uids=[],
                                       catstoexclude=[], exclude=True, allItems=False):
        '''Returns a list of items ordered by category number. If there are many
           items by category, there is always only one category, even if the
           user have chosen a different order. If exclude=True , catstoexclude
           represents the category number that we don't want to print and if
           exclude=False, catsexclude represents the category number that we
           only want to print. This is useful when we want for exemple to
           exclude a personnal category from the meeting an realize a separate
           meeeting for this personal category. If allItems=True, we return
           late items AND items in order.'''
        def getPrintableNumCategory(current_cat):
            '''Method used here above.'''
            current_cat_id = current_cat.getId()
            current_cat_name = current_cat.Title()
            current_cat_name = current_cat_name[0:2]
            try:
                catNum = int(current_cat_name)
            except ValueError:
                current_cat_name = current_cat_name[0:1]
                try:
                    catNum = int(current_cat_name)
                except ValueError:
                    catNum = current_cat_id
            return catNum

        if not allItems and listTypes == ['late']:
            items = self.context.getItems(uids=uids, listTypes=['late'], ordered=True)
        elif not allItems and not listTypes == ['late']:
            items = self.context.getItems(uids=uids, listTypes=['normal'], ordered=True)
        else:
            items = self.context.getItems(uids=uids, ordered=True)
        # res contains all items by category, the key of res is the category
        # number. Pay attention that the category number is obtain by extracting
        # the 2 first caracters of the categoryname, thus the categoryname must
        # be for exemple ' 2.travaux' or '10.Urbanisme. If not, the catnum takes
        # the value of the id + 1000 to be sure to place those categories at the
        # end.
        res = {}
        # First, we create the category and for each category, we create a
        # dictionary that must contain the list of item in in res[catnum][1]
        for item in items:
            if uids:
                if (item.UID() in uids):
                    inuid = "ok"
                else:
                    inuid = "ko"
            else:
                inuid = "ok"
            if (inuid == "ok"):
                current_cat = item.getCategory(theObject=True)
                catNum = getPrintableNumCategory(current_cat)
                if catNum in res:
                    res[catNum][1][item.getItemNumber()] = item
                else:
                    res[catNum] = {}
                    # first value of the list is the category object
                    res[catNum][0] = item.getCategory(True)
                    # second value of the list is a list of items
                    res[catNum][1] = {}
                    res[catNum][1][item.getItemNumber()] = item

        # Now we must sort the res dictionary with the key (containing catnum)
        # and copy it in the returned array.
        reskey = res.keys()
        reskey.sort()
        ressort = []
        for i in reskey:
            if catstoexclude:
                if (i in catstoexclude):
                    if exclude is False:
                        guard = True
                    else:
                        guard = False
                else:
                    if exclude is False:
                        guard = False
                    else:
                        guard = True
            else:
                guard = True

            if guard is True:
                k = 0
                ressorti = []
                ressorti.append(res[i][0])
                resitemkey = res[i][1].keys()
                resitemkey.sort()
                ressorti1 = []
                for j in resitemkey:
                    k = k + 1
                    ressorti1.append([res[i][1][j], k])
                ressorti.append(ressorti1)
                ressort.append(ressorti)
        return ressort


class CustomMeetingItem(MeetingItem):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCustom.'''
    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    def getFinanceAdviceId(self):
        """ """
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        usedFinanceGroupIds = cfg.adapted().getUsedFinanceGroupIds(self.context)
        adviserIds = self.context.adviceIndex.keys()
        financeAdvisersIds = set(usedFinanceGroupIds).intersection(set(adviserIds))
        if financeAdvisersIds:
            return list(financeAdvisersIds)[0]
        else:
            return None

    def _initDecisionFieldIfEmpty(self):
        '''
          If decision field is empty, it will be initialized
          with data coming from title and description.
        '''
        # set keepWithNext to False as it will add a 'class' and so
        # xhtmlContentIsEmpty will never consider it empty...
        if xhtmlContentIsEmpty(self.getDecision(keepWithNext=False)):
            self.setDecision("<p>%s</p>%s" % (self.Title(),
                                              self.Description()))
            self.reindexObject()
    MeetingItem._initDecisionFieldIfEmpty = _initDecisionFieldIfEmpty

    def adviceDelayIsTimedOutWithRowId(self, groupId, rowIds=[]):
        ''' Check if advice with delay from a certain p_groupId and with
            a row_id contained in p_rowIds is timed out.
        '''
        self = self.getSelf()
        if self.getAdviceDataFor(self) and groupId in self.getAdviceDataFor(self):
            adviceRowId = self.getAdviceDataFor(self, groupId)['row_id']
        else:
            return False

        if not rowIds or adviceRowId in rowIds:
            return self._adviceDelayIsTimedOut(groupId)
        else:
            return False

    def showFinanceAdviceTemplate(self):
        """ """
        item = self.getSelf()
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(item)
        return bool(set(cfg.adapted().getUsedFinanceGroupIds(item)).
                    intersection(set(item.adviceIndex.keys())))


class CustomMeetingConfig(MeetingConfig):
    '''Adapter that adapts a meetingConfig implementing IMeetingConfig to the
       interface IMeetingConfigCustom.'''

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    security.declarePublic('getUsedFinanceGroupIds')

    def getUsedFinanceGroupIds(self, item=None):
        """Possible finance advisers group ids are defined on
           the FINANCE_ADVICES_COLLECTION_ID collection."""
        cfg = self.getSelf()
        collection = getattr(cfg.searches.searches_items, FINANCE_ADVICES_COLLECTION_ID, None)
        res = []
        if not collection:
            logger.warn(
                "Method 'getUsedFinanceGroupIds' could not find the '{0}' collection!".format(
                    FINANCE_ADVICES_COLLECTION_ID))
            return res
        # if collection is not enabled, we just return an empty list
        # for convenience, the collection is added to every MeetingConfig, even if not used
        if not collection.enabled:
            return res
        # get the indexAdvisers value defined on the collection
        # and find the relevant group, indexAdvisers form is :
        # 'delay_row_id__2014-04-16.9996934488', 'real_org_uid__[directeur-financier_UID]'
        # it is either a customAdviser row_id or an organization uid
        values = [term['v'] for term in collection.getRawQuery()
                  if term['i'] == 'indexAdvisers'][0]

        for v in values:
            real_org_uid_prefix = REAL_ORG_UID_PATTERN.format('')
            if v.startswith(real_org_uid_prefix):
                org_uid = v.replace(real_org_uid_prefix, '')
                # append it only if not already into res and if
                # we have no 'row_id' for this adviser in adviceIndex
                if item and org_uid not in res and \
                   (org_uid in item.adviceIndex and not item.adviceIndex[org_uid]['row_id']):
                    res.append(org_uid)
                elif not item:
                    res.append(org_uid)
            else:
                # v.startswith(delayaware_row_id_prefix)
                delayaware_row_id_prefix = DELAYAWARE_ROW_ID_PATTERN.format('')
                row_id = v.replace(delayaware_row_id_prefix, '')
                org_uid = cfg._dataForCustomAdviserRowId(row_id)['org']
                # append it only if not already into res and if
                # we have a 'row_id' for this adviser in adviceIndex
                if item and org_uid not in res and \
                    (org_uid in item.adviceIndex and
                     item.adviceIndex[org_uid]['row_id'] == row_id):
                    res.append(org_uid)
                elif not item:
                    res.append(org_uid)
        # remove duplicates
        return list(set(res))

    def _extraSearchesInfo(self, infos):
        """Add some specific searches."""
        cfg = self.getSelf()
        itemType = cfg.getItemTypeName()
        extra_infos = OrderedDict(
            [
                # Items in state 'proposed'
                ('searchproposeditems',
                    {
                        'subFolderId': 'searches_items',
                        'active': True,
                        'query':
                        [
                            {'i': 'portal_type',
                             'o': 'plone.app.querystring.operation.selection.is',
                             'v': [itemType, ]},
                            {'i': 'review_state',
                             'o': 'plone.app.querystring.operation.selection.is',
                             'v': ['proposed']}
                        ],
                        'sort_on': u'created',
                        'sort_reversed': True,
                        'showNumberOfItems': False,
                        'tal_condition': "python: not tool.userIsAmong(['reviewers'])",
                        'roles_bypassing_talcondition': ['Manager', ]
                    }
                 ),
                # Items in state 'validated'
                ('searchvalidateditems',
                    {
                        'subFolderId': 'searches_items',
                        'active': True,
                        'query':
                        [
                            {'i': 'portal_type',
                             'o': 'plone.app.querystring.operation.selection.is',
                             'v': [itemType, ]},
                            {'i': 'review_state',
                             'o': 'plone.app.querystring.operation.selection.is',
                             'v': ['validated']}
                        ],
                        'sort_on': u'created',
                        'sort_reversed': True,
                        'showNumberOfItems': False,
                        'tal_condition': "",
                        'roles_bypassing_talcondition': ['Manager', ]
                    }
                 ),
                # Items for finance advices synthesis
                (FINANCE_ADVICES_COLLECTION_ID,
                    {
                        'subFolderId': 'searches_items',
                        'active': True,
                        'query':
                        [
                            {'i': 'portal_type',
                             'o': 'plone.app.querystring.operation.selection.is',
                             'v': [itemType, ]},
                            {'i': 'indexAdvisers',
                             'o': 'plone.app.querystring.operation.selection.is',
                             'v': ['delay_real_group_id__unique_id_002',
                                   'delay_real_group_id__unique_id_003',
                                   'delay_real_group_id__unique_id_004']}
                        ],
                        'sort_on': u'created',
                        'sort_reversed': True,
                        'showNumberOfItems': False,
                        'tal_condition':
                        "python: '%s_budgetimpacteditors' % cfg.getId() in tool.getPloneGroupsForUser() or "
                        "tool.isManager(here)",
                        'roles_bypassing_talcondition': ['Manager', ]
                    }
                 ),
            ]
        )
        infos.update(extra_infos)

        # disable FINANCE_ADVICES_COLLECTION_ID excepted for 'meeting-config-college' and 'meeting-config-bp'
        if cfg.getId() not in ('meeting-config-college', 'meeting-config-bp'):
            infos[FINANCE_ADVICES_COLLECTION_ID]['active'] = False

        # add some specific searches while using 'meetingadvicefinances'
        typesTool = api.portal.get_tool('portal_types')
        if 'meetingadvicefinances' in typesTool and cfg.getUseAdvices():
            financesadvice_infos = OrderedDict(
                [
                    # Items in state 'proposed_to_finance' for which
                    # completeness is not 'completeness_complete'
                    ('searchitemstocontrolcompletenessof',
                        {
                            'subFolderId': 'searches_items',
                            'active': True,
                            'query':
                            [
                                {'i': 'CompoundCriterion',
                                 'o': 'plone.app.querystring.operation.compound.is',
                                 'v': 'items-to-control-completeness-of'},
                            ],
                            'sort_on': u'created',
                            'sort_reversed': True,
                            'tal_condition': "python: (here.REQUEST.get('fromPortletTodo', False) and "
                                             "tool.userIsAmong(['financialcontrollers'])) "
                                             "or (not here.REQUEST.get('fromPortletTodo', False) and "
                                             "tool.adapted().isFinancialUser())",
                            'roles_bypassing_talcondition': ['Manager', ]
                        }
                     ),
                    # Items having advice in state 'proposed_to_financial_controller'
                    ('searchadviceproposedtocontroller',
                        {
                            'subFolderId': 'searches_items',
                            'active': True,
                            'query':
                            [
                                {'i': 'CompoundCriterion',
                                 'o': 'plone.app.querystring.operation.compound.is',
                                 'v': 'items-with-advice-proposed-to-financial-controller'},
                            ],
                            'sort_on': u'created',
                            'sort_reversed': True,
                            'tal_condition': "python: (here.REQUEST.get('fromPortletTodo', False) and "
                                             "tool.userIsAmong(['financialcontrollers'])) "
                                             "or (not here.REQUEST.get('fromPortletTodo', False) and "
                                             "tool.adapted().isFinancialUser())",
                            'roles_bypassing_talcondition': ['Manager', ]
                        }
                     ),
                    # Items having advice in state 'proposed_to_financial_editor'
                    ('searchadviceproposedtoeditor',
                        {
                            'subFolderId': 'searches_items',
                            'active': True,
                            'query':
                            [
                                {'i': 'CompoundCriterion',
                                 'o': 'plone.app.querystring.operation.compound.is',
                                 'v': 'items-with-advice-proposed-to-financial-editor'},
                            ],
                            'sort_on': u'created',
                            'sort_reversed': True,
                            'tal_condition': "python: (here.REQUEST.get('fromPortletTodo', False) and "
                                             "tool.userIsAmong(['financialeditors'])) "
                                             "or (not here.REQUEST.get('fromPortletTodo', False) and "
                                             "tool.adapted().isFinancialUser())",
                            'roles_bypassing_talcondition': ['Manager', ]
                        }
                     ),
                    # Items having advice in state 'proposed_to_financial_reviewer'
                    ('searchadviceproposedtoreviewer',
                        {
                            'subFolderId': 'searches_items',
                            'active': True,
                            'query':
                            [
                                {'i': 'CompoundCriterion',
                                 'o': 'plone.app.querystring.operation.compound.is',
                                 'v': 'items-with-advice-proposed-to-financial-reviewer'},
                            ],
                            'sort_on': u'created',
                            'sort_reversed': True,
                            'tal_condition': "python: (here.REQUEST.get('fromPortletTodo', False) and "
                                             "tool.userIsAmong(['financialreviewers'])) "
                                             "or (not here.REQUEST.get('fromPortletTodo', False) and "
                                             "tool.adapted().isFinancialUser())",
                            'roles_bypassing_talcondition': ['Manager', ]
                        }
                     ),
                    # Items having advice in state 'proposed_to_financial_manager'
                    ('searchadviceproposedtomanager',
                        {
                            'subFolderId': 'searches_items',
                            'active': True,
                            'query':
                            [
                                {'i': 'CompoundCriterion',
                                 'o': 'plone.app.querystring.operation.compound.is',
                                 'v': 'items-with-advice-proposed-to-financial-manager'},
                            ],
                            'sort_on': u'created',
                            'sort_reversed': True,
                            'tal_condition': "python: (here.REQUEST.get('fromPortletTodo', False) and "
                                             "tool.userIsAmong(['financialmanagers'])) "
                                             "or (not here.REQUEST.get('fromPortletTodo', False) and "
                                             "tool.adapted().isFinancialUser())",
                            'roles_bypassing_talcondition': ['Manager', ]
                        }
                     ),
                ]
            )
            infos.update(financesadvice_infos)
        return infos

    def extraAdviceTypes(self):
        '''See doc in interfaces.py.'''
        typesTool = api.portal.get_tool('portal_types')
        if 'meetingadvicefinances' in typesTool:
            return ['positive_finance', 'positive_with_remarks_finance',
                    'cautious_finance', 'negative_finance', 'not_given_finance',
                    'not_required_finance']
        return []


class MeetingCommunesWorkflowActions(MeetingWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCommunesWorkflowActions'''

    implements(IMeetingCommunesWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doDecide')

    def doDecide(self, stateChange):
        '''We pass every item that is 'presented' in the 'itemfrozen'
           state.  It is the case for late items. Moreover, if
           MeetingConfig.initItemDecisionIfEmptyOnDecide is True, we
           initialize the decision field with content of Title+Description
           if decision field is empty.'''
        tool = getToolByName(self.context, 'portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        if cfg.getInitItemDecisionIfEmptyOnDecide():
            for item in self.context.getItems():
                # If deliberation (motivation+decision) is empty,
                # initialize it the decision field
                item._initDecisionFieldIfEmpty()

    security.declarePrivate('doBackToPublished')

    def doBackToPublished(self, stateChange):
        '''We do not impact items while going back from decided.'''
        pass


class MeetingCommunesWorkflowConditions(MeetingWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCommunesWorkflowConditions'''

    implements(IMeetingCommunesWorkflowConditions)
    security = ClassSecurityInfo()

    security.declarePublic('mayCorrect')

    def mayCorrect(self, destinationState=None):
        '''Override to avoid call to _decisionsWereConfirmed.'''
        if not _checkPermission(ReviewPortalContent, self.context):
            return
        return True

    security.declarePublic('mayDecide')

    def mayDecide(self):
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res


class MeetingItemCommunesWorkflowActions(MeetingItemWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCommunesWorkflowActions'''

    implements(IMeetingItemCommunesWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doAccept_but_modify')

    def doAccept_but_modify(self, stateChange):
        pass

    security.declarePrivate('doPre_accept')

    def doPre_accept(self, stateChange):
        pass


class MeetingItemCommunesWorkflowConditions(MeetingItemWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCommunesWorkflowConditions'''

    implements(IMeetingItemCommunesWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item  # Implements IMeetingItem

    security.declarePublic('mayDecide')

    def mayDecide(self):
        '''We may decide an item if the linked meeting is in relevant state.'''
        res = False
        meeting = self.context.getMeeting()
        if _checkPermission(ReviewPortalContent, self.context) and \
           meeting and meeting.adapted().isDecided():
            res = True
        return res

    security.declarePublic('mayPublish')

    def mayPublish(self):
        """
          A MeetingManager may publish (itempublish) an item if the meeting is at least published
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            if self.context.hasMeeting() and \
               (self.context.getMeeting().queryState() in ('published', 'decided', 'closed', 'decisions_published',)):
                res = True
        return res


class CustomToolPloneMeeting(ToolPloneMeeting):
    '''Adapter that adapts a tool implementing ToolPloneMeeting to the
       interface IToolPloneMeetingCustom'''

    implements(IToolPloneMeetingCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    def isFinancialUser_cachekey(method, self, brain=False):
        '''cachekey method for self.isFinancialUser.'''
        return str(self.context.REQUEST._debug), self.context.REQUEST['AUTHENTICATED_USER']

    security.declarePublic('isFinancialUser')

    @ram.cache(isFinancialUser_cachekey)
    def isFinancialUser(self):
        '''Is current user a financial user, so in groups FINANCE_GROUP_SUFFIXES.'''
        tool = api.portal.get_tool('portal_plonemeeting')
        for groupId in tool.getPloneGroupsForUser():
            for suffix in FINANCE_GROUP_SUFFIXES:
                if groupId.endswith('_%s' % suffix):
                    return True
        return False

    def performCustomWFAdaptations(self, meetingConfig, wfAdaptation, logger, itemWorkflow, meetingWorkflow):
        """ """
        if wfAdaptation == 'no_publication':
            # we override the PloneMeeting's 'no_publication' wfAdaptation
            # First, update the meeting workflow
            wf = meetingWorkflow
            # Delete transitions 'publish' and 'backToPublished'
            for tr in ('publish', 'backToPublished'):
                if tr in wf.transitions:
                    wf.transitions.deleteTransitions([tr])
            # Update connections between states and transitions
            wf.states['frozen'].setProperties(
                title='frozen', description='',
                transitions=['backToCreated', 'decide'])
            wf.states['decided'].setProperties(
                title='decided', description='', transitions=['backToFrozen', 'close'])
            # Delete state 'published'
            if 'published' in wf.states:
                wf.states.deleteStates(['published'])
            # Then, update the item workflow.
            wf = itemWorkflow
            # Delete transitions 'itempublish' and 'backToItemPublished'
            for tr in ('itempublish', 'backToItemPublished'):
                if tr in wf.transitions:
                    wf.transitions.deleteTransitions([tr])
            # Update connections between states and transitions
            wf.states['itemfrozen'].setProperties(
                title='itemfrozen', description='',
                transitions=['accept', 'accept_but_modify', 'delay', 'pre_accept', 'backToPresented'])
            for decidedState in ['accepted', 'delayed', 'accepted_but_modified']:
                wf.states[decidedState].setProperties(
                    title=decidedState, description='',
                    transitions=['backToItemFrozen', ])
            wf.states['pre_accepted'].setProperties(
                title='pre_accepted', description='',
                transitions=['accept', 'accept_but_modify', 'backToItemFrozen'])
            # Delete state 'published'
            if 'itempublished' in wf.states:
                wf.states.deleteStates(['itempublished'])
            logger.info(WF_APPLIED % ("no_publication", meetingConfig.getId()))
            return True
        return False

    security.declarePublic('getSpecificAssemblyFor')

    def getSpecificAssemblyFor(self, assembly, startTxt=''):
        ''' Return the Assembly between two tag.
            This method is used in templates.
        '''
        # Pierre Dupont - Bourgmestre,
        # Charles Exemple - 1er Echevin,
        # Echevin Un, Echevin Deux excusé, Echevin Trois - Echevins,
        # Jacqueline Exemple, Responsable du CPAS
        # Absentes:
        # Mademoiselle x
        # Excusés:
        # Monsieur Y, Madame Z
        res = []
        tmp = ['<p class="mltAssembly">']
        splitted_assembly = assembly.replace('<p>', '').replace('</p>', '').split('<br />')
        start_text = startTxt == ''
        for assembly_line in splitted_assembly:
            assembly_line = assembly_line.strip()
            # check if this line correspond to startTxt (in this cas, we can begin treatment)
            if not start_text:
                start_text = assembly_line.startswith(startTxt)
                if start_text:
                    # when starting treatment, add tag (not use if startTxt=='')
                    res.append(assembly_line)
                continue
            # check if we must stop treatment...
            if assembly_line.endswith(':'):
                break
            lines = assembly_line.split(',')
            cpt = 1
            my_line = ''
            for line in lines:
                if cpt == len(lines):
                    my_line = "%s%s<br />" % (my_line, line)
                    tmp.append(my_line)
                else:
                    my_line = "%s%s," % (my_line, line)
                cpt = cpt + 1
        if len(tmp) > 1:
            tmp[-1] = tmp[-1].replace('<br />', '')
            tmp.append('</p>')
        else:
            return ''
        res.append(''.join(tmp))
        return res

    def initializeProposingGroupWithGroupInCharge(self):
        """Initialize every items of MeetingConfig for which
           'proposingGroupWithGroupInCharge' is in usedItemAttributes."""
        tool = self.getSelf()
        catalog = api.portal.get_tool('portal_catalog')
        logger.info('Initializing proposingGroupWithGroupInCharge...')
        for cfg in tool.objectValues('MeetingConfig'):
            if 'proposingGroupWithGroupInCharge' in cfg.getUsedItemAttributes():
                brains = catalog(portal_type=cfg.getItemTypeName())
                logger.info('Updating MeetingConfig {0}'.format(cfg.getId()))
                len_brains = len(brains)
                i = 1
                for brain in brains:
                    logger.info('Updating item {0}/{1}'.format(i, len_brains))
                    i = i + 1
                    item = brain.getObject()
                    proposingGroup = item.getProposingGroup(theObject=True)
                    groupsInCharge = proposingGroup.getGroupsInCharge()
                    groupInCharge = groupsInCharge and groupsInCharge[0] or ''
                    value = '{0}__groupincharge__{1}'.format(proposingGroup.getId(),
                                                             groupInCharge)
                    item.setProposingGroupWithGroupInCharge(value)
                    if cfg.getItemGroupInChargeStates():
                        item._updateGroupInChargeLocalRoles()
                        item.reindexObjectSecurity()
                    item.reindexObject(idxs=['getGroupInCharge'])
        logger.info('Done.')

# ------------------------------------------------------------------------------
InitializeClass(CustomMeeting)
InitializeClass(CustomMeetingItem)
InitializeClass(CustomMeetingConfig)
InitializeClass(MeetingCommunesWorkflowActions)
InitializeClass(MeetingCommunesWorkflowConditions)
InitializeClass(MeetingItemCommunesWorkflowActions)
InitializeClass(MeetingItemCommunesWorkflowConditions)
InitializeClass(CustomToolPloneMeeting)
# ------------------------------------------------------------------------------


class ItemsToControlCompletenessOfAdapter(CompoundCriterionBaseAdapter):

    def itemstocontrolcompletenessof_cachekey(method, self):
        '''cachekey method for every CompoundCriterion adapters.'''
        return str(self.request._debug)

    @property
    @ram.cache(itemstocontrolcompletenessof_cachekey)
    def query_itemstocontrolcompletenessof(self):
        '''Queries all items for which there is completeness to evaluate, so where completeness
           is not 'completeness_complete'.'''
        groupIds = []
        userGroups = self.tool.getPloneGroupsForUser()
        for financeGroup in self.cfg.adapted().getUsedFinanceGroupIds():
            # only keep finance groupIds the current user is controller for
            if '%s_financialcontrollers' % financeGroup in userGroups:
                # advice not given yet
                groupIds.append('delay__%s_advice_not_giveable' % financeGroup)
                # advice was already given once and come back to the finance
                groupIds.append('delay__%s_proposed_to_financial_controller' % financeGroup)
        return {'portal_type': {'query': self.cfg.getItemTypeName()},
                'getCompleteness': {'query': ('completeness_not_yet_evaluated',
                                              'completeness_incomplete',
                                              'completeness_evaluation_asked_again')},
                'indexAdvisers': {'query': groupIds},
                'review_state': {'query': FINANCE_WAITING_ADVICES_STATES}}

    # we may not ram.cache methods in same file with same name...
    query = query_itemstocontrolcompletenessof


class ItemsWithAdviceProposedToFinancialControllerAdapter(CompoundCriterionBaseAdapter):

    def itemswithadviceproposedtofinancialcontroller_cachekey(method, self):
        '''cachekey method for every CompoundCriterion adapters.'''
        return str(self.request._debug)

    @property
    @ram.cache(itemswithadviceproposedtofinancialcontroller_cachekey)
    def query_itemswithadviceproposedtofinancialcontroller(self):
        '''Queries all items for which there is an advice in state 'proposed_to_financial_controller'.
           We only return items for which completeness has been evaluated to 'complete'.'''
        groupIds = []
        userGroups = self.tool.getPloneGroupsForUser()
        for financeGroup in self.cfg.adapted().getUsedFinanceGroupIds():
            # only keep finance groupIds the current user is controller for
            if '%s_financialcontrollers' % financeGroup in userGroups:
                groupIds.append('delay__%s_proposed_to_financial_controller' % financeGroup)
        # Create query parameters
        return {'portal_type': {'query': self.cfg.getItemTypeName()},
                'getCompleteness': {'query': 'completeness_complete'},
                'indexAdvisers': {'query': groupIds}}

    # we may not ram.cache methods in same file with same name...
    query = query_itemswithadviceproposedtofinancialcontroller


class ItemsWithAdviceProposedToFinancialEditorAdapter(CompoundCriterionBaseAdapter):

    def itemswithadviceproposedtofinancialeditor_cachekey(method, self):
        '''cachekey method for every CompoundCriterion adapters.'''
        return str(self.request._debug)

    @property
    @ram.cache(itemswithadviceproposedtofinancialeditor_cachekey)
    def query_itemswithadviceproposedtofinancialeditor(self):
        '''Queries all items for which there is an advice in state 'proposed_to_financial_editor'.
           We only return items for which completeness has been evaluated to 'complete'.'''
        groupIds = []
        userGroups = self.tool.getPloneGroupsForUser()
        for financeGroup in self.cfg.adapted().getUsedFinanceGroupIds():
            # only keep finance groupIds the current user is controller for
            if '%s_financialeditors' % financeGroup in userGroups:
                groupIds.append('delay__%s_proposed_to_financial_editor' % financeGroup)
        # Create query parameters
        return {'portal_type': {'query': self.cfg.getItemTypeName()},
                'getCompleteness': {'query': 'completeness_complete'},
                'indexAdvisers': {'query': groupIds}}

    # we may not ram.cache methods in same file with same name...
    query = query_itemswithadviceproposedtofinancialeditor


class ItemsWithAdviceProposedToFinancialReviewerAdapter(CompoundCriterionBaseAdapter):

    def itemswithadviceproposedtofinancialreviewer_cachekey(method, self):
        '''cachekey method for every CompoundCriterion adapters.'''
        return str(self.request._debug)

    @property
    @ram.cache(itemswithadviceproposedtofinancialreviewer_cachekey)
    def query_itemswithadviceproposedtofinancialreviewer(self):
        '''Queries all items for which there is an advice in state 'proposed_to_financial_reviewer'.'''
        groupIds = []
        userGroups = self.tool.getPloneGroupsForUser()
        for financeGroup in self.cfg.adapted().getUsedFinanceGroupIds():
            # only keep finance groupIds the current user is reviewer for
            if '%s_financialreviewers' % financeGroup in userGroups:
                groupIds.append('delay__%s_proposed_to_financial_reviewer' % financeGroup)
        return {'portal_type': {'query': self.cfg.getItemTypeName()},
                'indexAdvisers': {'query': groupIds}}

    # we may not ram.cache methods in same file with same name...
    query = query_itemswithadviceproposedtofinancialreviewer


class ItemsWithAdviceProposedToFinancialManagerAdapter(CompoundCriterionBaseAdapter):

    def itemswithadviceproposedtofinancialmanager_cachekey(method, self):
        '''cachekey method for every CompoundCriterion adapters.'''
        return str(self.request._debug)

    @property
    @ram.cache(itemswithadviceproposedtofinancialmanager_cachekey)
    def query_itemswithadviceproposedtofinancialmanager(self):
        '''Queries all items for which there is an advice in state 'proposed_to_financial_manager'.'''
        groupIds = []
        userGroups = self.tool.getPloneGroupsForUser()
        for financeGroup in self.cfg.adapted().getUsedFinanceGroupIds():
            # only keep finance groupIds the current user is manager for
            if '%s_financialmanagers' % financeGroup in userGroups:
                groupIds.append('delay__%s_proposed_to_financial_manager' % financeGroup)
        return {'portal_type': {'query': self.cfg.getItemTypeName()},
                'indexAdvisers': {'query': groupIds}}

    # we may not ram.cache methods in same file with same name...
    query = query_itemswithadviceproposedtofinancialmanager
