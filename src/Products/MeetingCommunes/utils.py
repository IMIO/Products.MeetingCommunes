# -*- coding: utf-8 -*-

from collective.contact.plonegroup.utils import get_organization
from plone.memoize import forever
from Products.PloneMeeting.esign.utils import get_advice_esign_signatories


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


def get_finance_advice_esign_signatories(item, cfg, signature_numbers=['1'], position_types=[], **kwargs):
    """ """
    item_fin_advice_uids = cfg.adapted().getUsedFinanceGroupIds(item)
    if not item_fin_advice_uids:
        return {}
    item_fin_advice_uid = item_fin_advice_uids[0]
    userid = item.getAdviceDataFor(item, adviser_uid=item_fin_advice_uid)['creator_id']
    return get_advice_esign_signatories(
        item, userid, signature_numbers=signature_numbers, position_types=position_types, **kwargs)
