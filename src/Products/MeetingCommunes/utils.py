# -*- coding: utf-8 -*-

from collective.contact.plonegroup.utils import get_organization
from plone.memoize import forever


@forever.memoize
def finances_give_advice_states(cfg):
    """ """
    review_states = []
    for financeGroupUID in cfg.adapted().getUsedFinanceGroupIds():
        # get review_states in which advice is giveable by financeGroup
        financeGroup = get_organization(financeGroupUID)
        review_states.extend(financeGroup.get_item_advice_states(cfg))
    # manage duplicated
    return tuple(set(review_states))
