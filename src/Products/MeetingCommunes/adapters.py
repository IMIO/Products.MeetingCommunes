# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#

from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from appy.gen import No
from collections import OrderedDict
from collective.contact.plonegroup.utils import get_organizations
from imio.helpers.xhtml import xhtmlContentIsEmpty
from plone import api
from plone.memoize import ram
from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.utils import _checkPermission
from Products.MeetingCommunes import logger
from Products.MeetingCommunes.config import FINANCE_ADVICES_COLLECTION_ID
from Products.MeetingCommunes.config import FINANCE_GROUP_SUFFIXES
from Products.MeetingCommunes.config import POSITIVE_FINANCE_ADVICE_SIGNABLE_BY_REVIEWER
from Products.MeetingCommunes.interfaces import IMeetingAdviceCommunesWorkflowActions
from Products.MeetingCommunes.interfaces import IMeetingAdviceCommunesWorkflowConditions
from Products.MeetingCommunes.interfaces import IMeetingCommunesWorkflowActions
from Products.MeetingCommunes.interfaces import IMeetingCommunesWorkflowConditions
from Products.MeetingCommunes.interfaces import IMeetingItemCommunesWorkflowActions
from Products.MeetingCommunes.interfaces import IMeetingItemCommunesWorkflowConditions
from Products.MeetingCommunes.utils import finances_give_advice_states
from Products.PloneMeeting.adapters import CompoundCriterionBaseAdapter
from Products.PloneMeeting.adapters import query_user_groups_cachekey
from Products.PloneMeeting.config import PMMessageFactory as _
from Products.PloneMeeting.content.meeting import Meeting
from Products.PloneMeeting.indexes import DELAYAWARE_ROW_ID_PATTERN
from Products.PloneMeeting.indexes import REAL_ORG_UID_PATTERN
from Products.PloneMeeting.interfaces import IMeetingConfigCustom
from Products.PloneMeeting.interfaces import IMeetingCustom
from Products.PloneMeeting.interfaces import IMeetingItemCustom
from Products.PloneMeeting.interfaces import IToolPloneMeetingCustom
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.MeetingItem import MeetingItemWorkflowActions
from Products.PloneMeeting.MeetingItem import MeetingItemWorkflowConditions
from Products.PloneMeeting.model import adaptations
from Products.PloneMeeting.ToolPloneMeeting import ToolPloneMeeting
from Products.PloneMeeting.utils import duplicate_workflow
from Products.PloneMeeting.workflows.advice import MeetingAdviceWorkflowActions
from Products.PloneMeeting.workflows.advice import MeetingAdviceWorkflowConditions
from Products.PloneMeeting.workflows.meeting import MeetingWorkflowActions
from Products.PloneMeeting.workflows.meeting import MeetingWorkflowConditions
from zope.i18n import translate
from zope.interface import implements


class CustomMeeting(Meeting):
    '''Adapter that adapts a meeting implementing IMeeting to the
       interface IMeetingCustom.'''

    implements(IMeetingCustom)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting

    # Implements here methods that will be used by templates
    security.declarePublic('getPrintableItems')

    def getPrintableItems(self, itemUids, list_types=['normal'], ignore_review_states=[],
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
        # get_items(uids), passing the correct uids and removing empty uids.
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
            if obj.query_state() in ignore_review_states:
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
            items = self.context.get_items(uids=filteredItemUids, list_types=list_types, ordered=True)
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

    security.declarePublic('getPrintableItemsByCategory')

    def getPrintableItemsByCategory(self, itemUids=[], list_types=['normal'],
                                    ignore_review_states=[], by_proposing_group=False, group_prefixes={},
                                    privacy='*', oralQuestion='both', toDiscuss='both', categories=[],
                                    excludedCategories=[], groupIds=[], excludedGroupIds=[],
                                    firstNumber=1, renumber=False,
                                    includeEmptyCategories=False, includeEmptyGroups=False,
                                    forceCategOrderFromConfig=False):
        '''Returns a list of (late or normal or both) items (depending on p_list_types)
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
        # - at position 0: the category object (MeetingCategory or organization)
        # - at position 1 to n: the items in this category
        # If by_proposing_group is True, the structure is more complex.
        # list_types is a list that can be filled with 'normal' and/or 'late'
        # oralQuestion can be 'both' or False or True
        # toDiscuss can be 'both' or 'False' or 'True'
        # privacy can be '*' or 'public' or 'secret'
        # Every inner list contains:
        # - at position 0: the category object
        # - at positions 1 to n: inner lists that contain:
        #   * at position 0: the proposing group object
        #   * at positions 1 to n: the items belonging to this group.
        def _comp(v1, v2):
            if v1[0].get_order(only_selectable=False) < v2[0].get_order(only_selectable=False):
                return -1
            elif v1[0].get_order(only_selectable=False) > v2[0].get_order(only_selectable=False):
                return 1
            else:
                return 0
        res = []
        items = []
        tool = api.portal.get_tool('portal_plonemeeting')
        # Retrieve the list of items
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)

        items = self.context.get_items(uids=itemUids, list_types=list_types, ordered=True)

        if by_proposing_group:
            groups = get_organizations()
        else:
            groups = None
        if items:
            for item in items:
                # Check if the review_state has to be taken into account
                if item.query_state() in ignore_review_states:
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
        if forceCategOrderFromConfig or cmp(list_types.sort(), ['late', 'normal']) == 0:
            res.sort(cmp=_comp)
        if includeEmptyCategories:
            meetingConfig = tool.getMeetingConfig(
                self.context)
            # onlySelectable = False will also return disabled categories...
            allCategories = [cat for cat in meetingConfig.getCategories(onlySelectable=False)
                             if cat.enabled]
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

    security.declarePublic('getNumberOfItems')

    def getNumberOfItems(self, itemUids, privacy=[], categories=[], classifiers=[],
                         list_types=['normal']):
        '''Returns the number of items depending on parameters.
           This is used in templates to know how many items of a particular kind exist and
           often used to determine the 'firstNumber' parameter of getPrintableItems/getPrintableItemsByCategory.'''
        # sometimes, some empty elements are inserted in itemUids, remove them...
        additional_catalog_query = {}
        if privacy:
            additional_catalog_query['privacy'] = privacy
        if categories:
            additional_catalog_query['getCategory'] = categories
        if classifiers:
            additional_catalog_query['getRawClassifier'] = classifiers

        items = self.getSelf().get_items(itemUids,
                                         the_objects=False,
                                         list_types=list_types,
                                         additional_catalog_query=additional_catalog_query)
        return len(items)

    security.declarePublic('getPrintableItemsByNumCategory')

    def getPrintableItemsByNumCategory(self, list_types=['normal'], uids=[],
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

        if not allItems and list_types == ['late']:
            items = self.context.get_items(uids=uids, list_types=['late'], ordered=True)
        elif not allItems and not list_types == ['late']:
            items = self.context.get_items(uids=uids, list_types=['normal'], ordered=True)
        else:
            items = self.context.get_items(uids=uids, ordered=True)
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

    def showFinanceAdviceTemplate(self):
        """ """
        item = self.getSelf()
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(item)
        return bool(set(cfg.adapted().getUsedFinanceGroupIds(item)).
                    intersection(set(item.adviceIndex.keys())))

    def _adviceTypesForAdviser(self, meeting_advice_portal_type):
        """Return the advice types (positive, negative, ...) for given p_meeting_advice_portal_type.
           By default we always use every MeetingConfig.usedAdviceTypes but this is useful
           when using several portal_types for meetingadvice and some may use particular advice types."""
        item = self.getSelf()
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(item)
        if meeting_advice_portal_type.startswith('meetingadvicefinances'):
            return [t for t in cfg.getUsedAdviceTypes() if t.endswith('_finance')]
        else:
            return [t for t in cfg.getUsedAdviceTypes() if not t.endswith('_finance')]


class CustomMeetingConfig(MeetingConfig):
    '''Adapter that adapts a meetingConfig implementing IMeetingConfig to the
       interface IMeetingConfigCustom.'''

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    def _setUsedFinanceGroupIds(self, values):
        """Helper to set values for FINANCE_ADVICES_COLLECTION_ID collection."""
        cfg = self.getSelf()
        collection = getattr(cfg.searches.searches_items, FINANCE_ADVICES_COLLECTION_ID, None)
        query = collection.getQuery()
        query[1]['v'] = values
        collection.setQuery(query)

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
        # get the indexAdvisers value defined on the collection
        # and find the relevant group, indexAdvisers form is :
        # 'delay_row_id__2014-04-16.9996934488', 'real_org_uid__[directeur-financier_UID]'
        # it is either a customAdviser row_id or an organization uid
        # do not break if no 'indexAdvisers' defined or empty 'indexAdvisers' defined
        values = [term.get('v') for term in collection.getRawQuery()
                  if term.get('v') and term['i'] == 'indexAdvisers']

        # we get a list of advisers in values like [[v1, v2, v3]]
        if values:
            values = values[0]

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
                        'tal_condition': "python: tool.userIsAmong(['creators']) " \
                            "and not tool.userIsAmong(['reviewers'])",
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
                        'tal_condition': "python: not tool.isPowerObserverForCfg(cfg)",
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
                             'v': []}
                        ],
                        'sort_on': u'created',
                        'sort_reversed': True,
                        'showNumberOfItems': False,
                        'tal_condition':
                        "python: '%s_budgetimpacteditors' % cfg.getId() in tool.get_plone_groups_for_user() or "
                        "tool.isManager(cfg)",
                        'roles_bypassing_talcondition': ['Manager', ]
                    }
                 ),
                # Items for which finance advices were not asked
                ('searchitemswithnofinanceadvice',
                    {
                        'subFolderId': 'searches_items',
                        'active': False,
                        'query':
                            [
                                {'i': 'indexAdvisers',
                                 'o': 'plone.app.querystring.operation.selection.is',
                                 'v': []},
                                {'i': 'CompoundCriterion',
                                 'o': 'plone.app.querystring.operation.compound.is',
                                 'v': 'items-with-negative-previous-index'},
                            ],
                        'sort_on': u'created',
                        'sort_reversed': True,
                        'showNumberOfItems': False,
                        'tal_condition': "",
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
                    # Items having advice in state 'advicecreated'
                    ('searchadviceadvicecreated',
                        {
                            'subFolderId': 'searches_items',
                            'active': True,
                            'query':
                            [
                                {'i': 'CompoundCriterion',
                                 'o': 'plone.app.querystring.operation.compound.is',
                                 'v': 'items-with-advice-advicecreated'},
                            ],
                            'sort_on': u'created',
                            'sort_reversed': True,
                            'tal_condition': "python: (here.REQUEST.get('fromPortletTodo', False) and "
                                             "tool.userIsAmong(['financialprecontrollers'])) "
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
                    # Items having advice in state 'financial_advice_signed'
                    ('searchadvicesignedbymanager',
                        {
                            'subFolderId': 'searches_items',
                            'active': True,
                            'query':
                            [
                                {'i': 'CompoundCriterion',
                                 'o': 'plone.app.querystring.operation.compound.is',
                                 'v': 'items-with-advice-signed-by-financial-manager'},
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

    def _has_meetingadvicefinances_wf_adaptations(self):
        '''Check if some meetingadvicefinances_workflow related WFAdaptations are enabled.'''
        cfg = self.getSelf()
        finadv_wfas = [wfa for wfa in cfg.getWorkflowAdaptations()
                       if wfa.startswith('meetingadvicefinances_')]
        return bool(finadv_wfas)

    def _updateMeetingAdvicePortalTypes(self):
        '''Make sure we use a patched_ wokflow instead 'base_wf' for eachmeetingadvicefinances_workflow
           to apply advice related workflow adaptations.'''
        if self._has_meetingadvicefinances_wf_adaptations():
            fin_wf = 'meetingadvicefinances_workflow'
            wfTool = api.portal.get_tool('portal_workflow')
            if fin_wf in wfTool:
                patched_fin_wf = 'patched_meetingadvicefinances_workflow'
                duplicate_workflow(fin_wf, patched_fin_wf, portalTypeNames=['meetingadvicefinances'])

    def _adviceConditionsInterfaceFor(self, advice_obj):
        '''See doc in interfaces.py.'''
        if advice_obj.portal_type == 'meetingadvicefinances':
            return IMeetingAdviceCommunesWorkflowConditions.__identifier__
        else:
            return super(CustomMeetingConfig, self)._adviceConditionsInterfaceFor(advice_obj)

    def _adviceActionsInterfaceFor(self, advice_obj):
        '''See doc in interfaces.py.'''
        if advice_obj.portal_type.startswith('meetingadvicefinances'):
            return IMeetingAdviceCommunesWorkflowActions.__identifier__
        else:
            return super(CustomMeetingConfig, self)._adviceActionsInterfaceFor(advice_obj)


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
        if self.cfg.getInitItemDecisionIfEmptyOnDecide():
            for item in self.context.get_items():
                # If deliberation (motivation+decision) is empty,
                # initialize it the decision field
                item._initDecisionFieldIfEmpty()


class MeetingCommunesWorkflowConditions(MeetingWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCommunesWorkflowConditions'''

    implements(IMeetingCommunesWorkflowConditions)
    security = ClassSecurityInfo()


class MeetingItemCommunesWorkflowActions(MeetingItemWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCommunesWorkflowActions'''

    implements(IMeetingItemCommunesWorkflowActions)
    security = ClassSecurityInfo()

    def _will_ask_completeness_eval_again(self):
        ''' '''
        return 'completeness' in self.cfg.getUsedItemAttributes() and \
            self.context.query_state() in finances_give_advice_states(self.cfg) and \
            self.context.getCompleteness() in ['completeness_incomplete',
                                               'completeness_evaluation_not_required']

    def _will_set_completeness_to_not_required(self):
        ''' '''
        return False

    def _doWaitAdvices(self):
        '''When advices are asked again and we use MeetingItem.completeness field,
           make sure the item completeness evaluation is asked again so advice is not
           addable/editable when item come back again to this state.'''
        if self._will_ask_completeness_eval_again():
            wfTool = api.portal.get_tool('portal_workflow')
            history = self.context.workflow_history[wfTool.getWorkflowsFor(self.context)[0].getId()][:-1]
            for event in history:
                # set completeness to asked_again if it is not the first time that advices are asked
                if event['action'] and event['action'].startswith('wait_advices_from_'):
                    changeCompleteness = self.context.restrictedTraverse('@@change-item-completeness')
                    comment = translate('completeness_asked_again_by_app',
                                        domain='PloneMeeting',
                                        context=self.context.REQUEST)
                    # change completeness even if current user is not able to set it to
                    # 'completeness_evaluation_asked_again', here it is the application that set
                    # it automatically
                    changeCompleteness._changeCompleteness('completeness_evaluation_asked_again',
                                                           bypassSecurityCheck=True,
                                                           comment=comment)
                    break
        elif self._will_set_completeness_to_not_required():
            changeCompleteness = self.context.restrictedTraverse('@@change-item-completeness')
            comment = translate('completeness_set_to_not_required_by_app',
                                domain='PloneMeeting',
                                context=self.context.REQUEST)
            # change completeness even if current user is not able to
            changeCompleteness._changeCompleteness('completeness_evaluation_not_required',
                                                   bypassSecurityCheck=True,
                                                   comment=comment)

    security.declarePrivate('doWait_advices_from')

    def doWait_advices_from(self, stateChange):
        """ """
        self._doWaitAdvices()


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
           meeting and meeting.adapted().is_decided():
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
               (self.context.getMeeting().query_state() in (
                    'published', 'decided', 'closed', 'decisions_published',)):
                res = True
        return res


class MeetingAdviceCommunesWorkflowActions(MeetingAdviceWorkflowActions):
    ''' '''

    implements(IMeetingAdviceCommunesWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doProposeToFinancialController')

    def doProposeToFinancialController(self, stateChange):
        ''' '''
        pass

    security.declarePrivate('doProposeToFinancialEditor')

    def doProposeToFinancialEditor(self, stateChange):
        ''' '''
        pass

    security.declarePrivate('doProposeToFinancialReviewer')

    def doProposeToFinancialReviewer(self, stateChange):
        ''' '''
        pass

    security.declarePrivate('doProposeToFinancialManager')

    def doProposeToFinancialManager(self, stateChange):
        ''' '''
        pass

    security.declarePrivate('doSignFinancialAdvice')

    def doSignFinancialAdvice(self, stateChange):
        ''' '''
        pass


class MeetingAdviceCommunesWorkflowConditions(MeetingAdviceWorkflowConditions):
    ''' '''

    implements(IMeetingAdviceCommunesWorkflowConditions)
    security = ClassSecurityInfo()

    def _check_completeness(self):
        """When MeetingItem.completeness is used, we may only propose
           if completeness is complete or not required."""
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(self.context)
        res = True
        if 'completeness' in cfg.getUsedItemAttributes() and \
           not self.context.adapted()._is_complete():
            res = No(_('completeness_not_complete'))
        return res

    security.declarePublic('mayProposeToFinancialController')

    def mayProposeToFinancialController(self):
        ''' '''
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = self._check_completeness()
        return res

    security.declarePublic('mayProposeToFinancialEditor')

    def mayProposeToFinancialEditor(self):
        ''' '''
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = self._check_completeness()
        return res

    security.declarePublic('mayProposeToFinancialReviewer')

    def mayProposeToFinancialReviewer(self):
        ''' '''
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = self._check_completeness()
        return res

    security.declarePublic('mayProposeToFinancialManager')

    def mayProposeToFinancialManager(self):
        '''A financial manager may send the advice to the financial manager
           in any case (advice positive or negative) except if advice
           is still 'asked_again'.'''
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            if self.context.advice_type == 'asked_again':
                res = No(_('still_asked_again'))
            else:
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
                   not self.context.query_state() == 'proposed_to_financial_manager':
                    res = False
            else:
                if not self.context.query_state() == 'proposed_to_financial_manager':
                    res = False
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
        tool = api.portal.get_tool('portal_plonemeeting')
        return tool.get_plone_groups_for_user()

    security.declarePublic('isFinancialUser')

    @ram.cache(isFinancialUser_cachekey)
    def isFinancialUser(self):
        '''Is current user a financial user, so in groups FINANCE_GROUP_SUFFIXES.'''
        tool = api.portal.get_tool('portal_plonemeeting')
        for groupId in tool.get_plone_groups_for_user():
            for suffix in FINANCE_GROUP_SUFFIXES:
                if groupId.endswith('_%s' % suffix):
                    return True
        return False

    def performCustomAdviceWFAdaptations(self, meetingConfig, wfAdaptation, logger, advice_wf_id):
        ''' '''
        if wfAdaptation == 'add_advicecreated_state':
            # adapt WF, add new initial_state (and leading transitions)
            adaptations.addState(
                wf_id=advice_wf_id,
                new_state_id='advicecreated',
                new_state_title='advicecreated',
                permissions_cloned_state_id='proposed_to_financial_controller',
                leading_transition_id=None,
                leading_transition_title=None,
                back_transitions=[{'back_transition_id': 'backToAdviceCreated',
                                   'back_transition_title': 'backToAdviceCreated',
                                   'back_from_state_id': 'proposed_to_financial_controller'}],
                leaving_transition_id='proposeToFinancialController',
                leaving_to_state_id='proposed_to_financial_controller',
                existing_leaving_transition_ids=['giveAdvice'],
                existing_back_transition_ids=['backToAdviceInitialState'],
                new_initial_state=True)
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
                    item.reindexObject(idxs=['getGroupsInCharge'])
        logger.info('Done.')


# ------------------------------------------------------------------------------
InitializeClass(CustomMeeting)
InitializeClass(CustomMeetingItem)
InitializeClass(CustomMeetingConfig)
InitializeClass(MeetingAdviceCommunesWorkflowActions)
InitializeClass(MeetingAdviceCommunesWorkflowConditions)
InitializeClass(MeetingCommunesWorkflowActions)
InitializeClass(MeetingCommunesWorkflowConditions)
InitializeClass(MeetingItemCommunesWorkflowActions)
InitializeClass(MeetingItemCommunesWorkflowConditions)
InitializeClass(CustomToolPloneMeeting)
# ------------------------------------------------------------------------------


class ItemsToControlCompletenessOfAdapter(CompoundCriterionBaseAdapter):

    def _query(self, only_delay_advices=True):
        '''Queries items for which there is completeness to evaluate,
           so where completeness is not 'completeness_complete'.
           If p_only_delay_advices=True, only return delay aware advices.'''
        if not self.cfg:
            return {}
        groupIds = []
        for financeGroupUID in self.cfg.adapted().getUsedFinanceGroupIds():
            # advice was already given once and come back to the finance
            # in it's initial state
            wfTool = api.portal.get_tool('portal_workflow')
            initial_state = wfTool.getWorkflowsFor('meetingadvicefinances')[0].initial_state
            groupIds.append('delay__{0}_{1}'.format(financeGroupUID, initial_state))
            # advice not giveable
            groupIds.append('delay__%s_advice_not_giveable' % financeGroupUID)
            if not only_delay_advices:
                groupIds.append('{0}_{1}'.format(financeGroupUID, initial_state))
                groupIds.append('%s_advice_not_giveable' % financeGroupUID)
        review_states = finances_give_advice_states(self.cfg)
        return {'portal_type': {'query': self.cfg.getItemTypeName()},
                'getCompleteness': {'query': ('completeness_not_yet_evaluated',
                                              'completeness_incomplete',
                                              'completeness_evaluation_asked_again')},
                'indexAdvisers': {'query': groupIds},
                'review_state': {'query': tuple(set(review_states))}}

    @property
    @ram.cache(query_user_groups_cachekey)
    def query_itemstocontrolcompletenessof(self):
        """ """
        query = self._query()
        return query

    # we may not ram.cache methods in same file with same name...
    query = query_itemstocontrolcompletenessof


class AllItemsToControlCompletenessOfAdapter(ItemsToControlCompletenessOfAdapter):

    @property
    @ram.cache(query_user_groups_cachekey)
    def query_allitemstocontrolcompletenessof(self):
        ''' '''
        return self._query(only_delay_advices=False)
    # we may not ram.cache methods in same file with same name...
    query = query_allitemstocontrolcompletenessof


class BaseItemsWithAdviceAdapter(CompoundCriterionBaseAdapter):

    def _query(self, advice_review_state):
        ''' '''
        if not self.cfg:
            return {}
        groupIds = []
        for financeGroup in self.cfg.adapted().getUsedFinanceGroupIds():
            groupIds.append('delay__{0}_{1}'.format(financeGroup, advice_review_state))
            groupIds.append('{0}_{1}'.format(financeGroup, advice_review_state))
        # Create query parameters
        return {'portal_type': {'query': self.cfg.getItemTypeName()},
                'indexAdvisers': {'query': groupIds}}


class ItemsWithAdviceAdviceCreatedAdapter(BaseItemsWithAdviceAdapter):

    @property
    @ram.cache(query_user_groups_cachekey)
    def query_itemswithadviceadvicecreated(self):
        '''Queries all items for which there is an advice in state 'advicecreated'.'''
        query = self._query('advicecreated')
        return query

    # we may not ram.cache methods in same file with same name...
    query = query_itemswithadviceadvicecreated


class ItemsWithAdviceProposedToFinancialControllerAdapter(BaseItemsWithAdviceAdapter):

    @property
    @ram.cache(query_user_groups_cachekey)
    def query_itemswithadviceproposedtofinancialcontroller(self):
        '''Queries all items for which there is an advice in state 'proposed_to_financial_controller'.'''
        query = self._query('proposed_to_financial_controller')
        return query

    # we may not ram.cache methods in same file with same name...
    query = query_itemswithadviceproposedtofinancialcontroller


class ItemsWithAdviceProposedToFinancialEditorAdapter(BaseItemsWithAdviceAdapter):

    @property
    @ram.cache(query_user_groups_cachekey)
    def query_itemswithadviceproposedtofinancialeditor(self):
        '''Queries all items for which there is an advice in state 'proposed_to_financial_editor'.'''
        query = self._query('proposed_to_financial_editor')
        return query

    # we may not ram.cache methods in same file with same name...
    query = query_itemswithadviceproposedtofinancialeditor


class ItemsWithAdviceProposedToFinancialReviewerAdapter(BaseItemsWithAdviceAdapter):

    @property
    @ram.cache(query_user_groups_cachekey)
    def query_itemswithadviceproposedtofinancialreviewer(self):
        '''Queries all items for which there is an advice in state 'proposed_to_financial_reviewer'.'''
        query = self._query('proposed_to_financial_reviewer')
        return query

    # we may not ram.cache methods in same file with same name...
    query = query_itemswithadviceproposedtofinancialreviewer


class ItemsWithAdviceProposedToFinancialManagerAdapter(BaseItemsWithAdviceAdapter):

    @property
    @ram.cache(query_user_groups_cachekey)
    def query_itemswithadviceproposedtofinancialmanager(self):
        '''Queries all items for which there is an advice in state 'proposed_to_financial_manager'.'''
        query = self._query('proposed_to_financial_manager')
        return query

    # we may not ram.cache methods in same file with same name...
    query = query_itemswithadviceproposedtofinancialmanager


class ItemsWithAdviceSignedByFinancialManagerAdapter(BaseItemsWithAdviceAdapter):

    @property
    @ram.cache(query_user_groups_cachekey)
    def query_itemswithadvicesignedbyfinancialmanager(self):
        '''Queries all items for which there is an advice in state 'financial_advice_signed'.'''
        query = self._query('financial_advice_signed')
        return query

    # we may not ram.cache methods in same file with same name...
    query = query_itemswithadvicesignedbyfinancialmanager
