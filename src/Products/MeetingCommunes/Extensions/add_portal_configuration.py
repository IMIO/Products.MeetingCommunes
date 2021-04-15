#! /usr/bin/python
# -*- coding: utf-8 -*-
from plone import api
from Products.MeetingCommunes.config import PORTAL_CATEGORIES


def add_category(
    portal, meeting_config_id="meeting-config-council", is_classifier=False
):
    meeting_config = portal.portal_plonemeeting.get(meeting_config_id)
    folder = is_classifier and meeting_config.classifiers or meeting_config.categories
    for cat in PORTAL_CATEGORIES:
        data = cat.getData()
        api.content.create(container=folder, type="meetingcategory", **data)


def add_lisTypes(portal, meeting_config_id="meeting-config-council"):
    meeting_config = portal.portal_plonemeeting.get(meeting_config_id)
    new_listTypes = []
    for l_type in meeting_config.getListTypes():
        new_listTypes.append(l_type)

        if l_type["identifier"] == "normal":
            new_listTypes.append(
                {
                    "identifier": "normalnotpublishable",
                    "label": "normalnotpublishable",
                    "used_in_inserting_method": "0",
                },
            )

        elif l_type["identifier"] == "late":
            new_listTypes.append(
                {
                    "identifier": "latenotpublishable",
                    "label": "latenotpublishable",
                    "used_in_inserting_method": "0",
                },
            )

    meeting_config.setListTypes(new_listTypes)
