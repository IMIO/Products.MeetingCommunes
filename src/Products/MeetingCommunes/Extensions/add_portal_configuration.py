#! /usr/bin/python
# -*- coding: utf-8 -*-
from plone import api
from Products.MeetingCommunes.config import PORTAL_CATEGORIES


def add_category(
    self, meeting_config_id="meeting-config-council", is_classifier=False
):
    meeting_config = self.portal_plonemeeting.get(meeting_config_id)
    folder = is_classifier and meeting_config.classifiers or meeting_config.categories
    for cat in PORTAL_CATEGORIES:
        data = cat.getData()
        api.content.create(container=folder, type="meetingcategory", **data)

    meeting_config.at_post_edit_script()


def add_lisTypes(
    self,
    meeting_config_id="meeting-config-council",
    label_normal="Point normal (Non publiable)",
    label_late="Point supplémentaire (Non publiable)",
):
    meeting_config = self.portal_plonemeeting.get(meeting_config_id)
    new_listTypes = []
    for l_type in meeting_config.getListTypes():
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

    meeting_config.setListTypes(new_listTypes)
    meeting_config.at_post_edit_script()
