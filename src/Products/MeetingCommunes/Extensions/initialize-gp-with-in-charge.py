#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from datetime import datetime
from copy import deepcopy

from Products.PloneMeeting import logger

import transaction
from collective.contact.plonegroup.utils import get_organizations

special_format = "{0}__groupincharge__{1}"


def set_default_in_charge_if_misssing(default_in_charge_uid, remove_certified_signatures=[]):
    cfg_groups = get_organizations(only_selected=False)

    for group in cfg_groups:
        if not group.groups_in_charge:
            group.groups_in_charge = [default_in_charge_uid]
            logger.info(u"Added default group in charge to {}".format(group.title))

        certified_signatures = []
        for signature in group.certified_signatures:
            if signature.get('signature_number') not in remove_certified_signatures:
                certified_signatures.append(signature)

        group.certified_signatures = certified_signatures
        group.reindexObject()


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
    self, default_in_charge_uid, config_ids=[], ignore_if_others=[], remove_certified_signatures=[]
):
    start_date = datetime.now()
    count_patched = 0
    count_global = 0
    set_default_in_charge_if_misssing(default_in_charge_uid, remove_certified_signatures)

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
