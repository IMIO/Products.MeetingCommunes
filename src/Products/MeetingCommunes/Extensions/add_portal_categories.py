#! /usr/bin/python
# -*- coding: utf-8 -*-
from plone import api
from Products.MeetingCommunes.config import PORTAL_CATEGORIES


def add_portal_category(portal, meeting_config_id="meeting-config-council", is_classifier=False):
    meeting_config = portal.portal_plonemeeting.get(meeting_config_id)
    folder = is_classifier and meeting_config.classifiers or meeting_config.categories
    for cat in PORTAL_CATEGORIES:
        data = cat.getData()
        api.content.create(container=folder, type='meetingcategory', **data)
