#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from collective.contact.plonegroup.utils import get_organizations
from copy import deepcopy
from datetime import datetime
from Products.Archetypes.event import ObjectEditedEvent
from Products.PloneMeeting import logger
from zope.event import notify

import re
import transaction


special_format = "{0}__groupincharge__{1}"


def set_default_in_charge_if_misssing_and_fix_certified_sign(default_in_charge_uid, remove_certified_signatures=[], remove_certified_signatures_ignore_pattern=None):
    cfg_groups = get_organizations(only_selected=False)
    for group in cfg_groups:
        if not group.groups_in_charge:
            group.groups_in_charge = [default_in_charge_uid]
            logger.info(u"Added default group in charge to {}".format(group.title))

        if not remove_certified_signatures_ignore_pattern or not re.match(remove_certified_signatures_ignore_pattern, group.title):
            # the organisation members create items
            certified_signatures = []
            for signature in group.certified_signatures:
                if signature.get('signature_number') not in remove_certified_signatures:
                    certified_signatures.append(signature)

            group.certified_signatures = certified_signatures
        group.reindexObject()


def set_up_meeting_config_used_items_attributes(cfg):
    logger.info(
        "Activating proposingGroupWithGroupInCharge and disabling groupsInCharge"
    )
    used_item_attributes = list(cfg.getUsedItemAttributes())
    if u"proposingGroupWithGroupInCharge" not in used_item_attributes:
        used_item_attributes.append(u"proposingGroupWithGroupInCharge")
    if u"groupsInCharge" in used_item_attributes:
        used_item_attributes.remove(u"groupsInCharge")
    cfg.setUsedItemAttributes(tuple(used_item_attributes))
    notify(ObjectEditedEvent(cfg))


def initialize_proposingGroupWithGroupInCharge(
    self, default_in_charge_uid, config_ids=[], ignore_if_others=[], remove_certified_signatures=[], remove_certified_signatures_ignore_pattern=None
):
    if not isinstance(remove_certified_signatures, list):
        remove_certified_signatures = [remove_certified_signatures]

    start_date = datetime.now()
    count_patched = 0
    count_global = 0
    set_default_in_charge_if_misssing_and_fix_certified_sign(default_in_charge_uid, remove_certified_signatures, remove_certified_signatures_ignore_pattern)

    item_type_names = []

    if not config_ids:
        meeting_configs = self.portal_plonemeeting.listFolderContents()
    else:
        meeting_configs = []
        for config_id in config_ids:
            meeting_configs.append(self.portal_plonemeeting.get(config_id))

    for meeting_config in meeting_configs:
        set_up_meeting_config_used_items_attributes(meeting_config)
        item_type_names.append(meeting_config.getItemTypeName())

    items = self.portal_catalog(portal_type=item_type_names)
    logger.info("Checking {} {}".format(len(items), item_type_names))
    for brain in items:
        if not brain.getGroupsInCharge:
            formatted_gp = None
            item = brain.getObject()
            proposing_group = item.getProposingGroup(theObject=True)
            if proposing_group:
                groups_in_charge = deepcopy(proposing_group.groups_in_charge)
                for in_charge in groups_in_charge:
                    if in_charge not in ignore_if_others:
                        formatted_gp = special_format.format(
                            item.getProposingGroup(), in_charge
                        )
                        item.setProposingGroupWithGroupInCharge(formatted_gp)
                        break
                if not formatted_gp:
                    formatted_gp = special_format.format(
                        item.getProposingGroup(),
                        item.getGroupsInCharge(fromOrgIfEmpty=True, first=True),
                    )
                item.setProposingGroupWithGroupInCharge(formatted_gp)
                item.reindexObject(idxs=["getGroupsInCharge"])
                item.updateLocalRoles()

                count_patched += 1
        count_global += 1
        if count_global % 200 == 0:
            logger.info(
                "Checked {} / {} items. Patched {} of them".format(
                    count_global,
                    len(items),
                    count_patched,
                )
            )
        # save what's already done
        if count_patched % 10000 == 0:
            transaction.commit()

    end_date = datetime.now()
    seconds = end_date - start_date
    seconds = seconds.seconds
    hours = seconds / 3600
    minutes = (seconds - hours * 3600) / 60

    logger.info(
        u"Completed in {0} seconds (about {1} h {2} m).".format(seconds, hours, minutes)
    )
    if count_patched > 0:
        ratio = count_patched / seconds
        logger.info(u"That's %2.2f items patched per second" % ratio)
