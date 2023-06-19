#! /usr/bin/python
# -*- coding: utf-8 -*-

from plone import api
from Products.Archetypes.event import ObjectEditedEvent
from Products.MeetingCommunes.config import PORTAL_CATEGORIES
from zope.event import notify


def add_category(
    self, cfg_id="meeting-config-council", is_classifier=False
):
    tool = api.portal.get_tool('portal_plonemeeting')
    cfg = tool.get(cfg_id)
    folder = is_classifier and cfg.classifiers or cfg.categories
    for cat in PORTAL_CATEGORIES:
        data = cat.getData()
        api.content.create(container=folder, type="meetingcategory", **data)
    notify(ObjectEditedEvent(cfg))


def add_lisTypes(
    self,
    cfg_id="meeting-config-council",
    label_normal="Point normal (Non publiable)",
    label_late="Point supplémentaire (Non publiable)",
):
    cfg = self.portal_plonemeeting.get(cfg_id)
    new_listTypes = []
    for l_type in cfg.getListTypes():
        new_listTypes.append(l_type)

        if l_type["identifier"] == "normal":
            new_listTypes.append(
                {
                    "identifier": "normalnotpublishable",
                    "label": label_normal,
                    "used_in_inserting_method": "0",
                },
            )

        elif l_type["identifier"] == "late":
            new_listTypes.append(
                {
                    "identifier": "latenotpublishable",
                    "label": label_late,
                    "used_in_inserting_method": "0",
                },
            )

    cfg.setListTypes(new_listTypes)
    notify(ObjectEditedEvent(cfg))
