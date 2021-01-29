#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from datetime import datetime
from copy import deepcopy

from Products.PloneMeeting import logger

from collective.contact.plonegroup.utils import get_organizations

special_format = "{0}__groupincharge__{1}"


def set_default_in_charge_if_misssing(default_in_charge_uid):
    cfg_groups = get_organizations(only_selected=False)

    for group in cfg_groups:
        if not group.groups_in_charge:
            group.groups_in_charge = [default_in_charge_uid]
            group.reindexObject()
            logger.info(u"Added default group in charge to {}".format(group.title))


def set_up_meeting_config_used_items_attributes(meeting_config):
    logger.info(
        "Activating proposingGroupWithGroupInCharge and disabling groupsInCharge"
    )
    used_item_attributes = list(meeting_config.usedItemAttributes)
    if u"proposingGroupWithGroupInCharge" not in meeting_config.usedItemAttributes:
        used_item_attributes.append(u"proposingGroupWithGroupInCharge")
    if u"groupsInCharge" in used_item_attributes:
        used_item_attributes.remove(u"groupsInCharge")
    meeting_config.usedItemAttributes = tuple(used_item_attributes)
    meeting_config.at_post_edit_script()


def initialize_proposingGroupWithGroupInCharge(
    self, config_id, default_in_charge_uid, ignore_if_others=[]
):
    set_default_in_charge_if_misssing(default_in_charge_uid)
    meeting_config = self.portal_plonemeeting.get(config_id)
    set_up_meeting_config_used_items_attributes(meeting_config)
    items = self.portal_catalog(portal_type=meeting_config.getItemTypeName())

    logger.info("Checking {} {}".format(len(items), meeting_config.getItemTypeName()))
    start_date = datetime.now()
    count_patched = 0
    count_global = 0
    for brain in items:
        if not brain.getGroupsInCharge:
            formatted_gp = None
            item = brain.getObject()
            proposing_group = item.getProposingGroup(theObject=True)
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
                "Checked {} / {} {}. Patched {} of them".format(
                    count_global,
                    len(items),
                    meeting_config.getItemTypeName(),
                    count_patched,
                )
            )

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
