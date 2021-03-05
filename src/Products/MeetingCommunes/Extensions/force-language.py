#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import datetime
from plone.app.querystring import queryparser
from Products.PloneMeeting import logger
from Products.PloneMeeting.config import HAS_SOLR

import transaction


class FixLanguage:
    def __init__(self, portal):
        self.portal = portal
        self.item_counter = 0
        self.meeting_counter = 0
        self.odds = []
        self.treated_count = {}

    def get_objects_to_correct(self):
        if HAS_SOLR:
            # with solr, its possible to query on Language attribute
            query = {'Language': {'not': ['fr', 'any']}, }
        else:
            catalog_query = [
                {
                    "i": "meta_type",
                    "o": "plone.app.querystring.operation.selection.is",
                    "v": ["Meeting", "MeetingItem"],
                },
            ]
            query = queryparser.parseFormquery(self.portal, catalog_query)
        res = self.portal.portal_catalog(**query)
        return res

    def commit_and_print_state(self):
        transaction.commit()
        message = "Transaction commited. {}".format(self.treated_count)
        logger.info(message)

    def run(self, reindex_meetings, commit_threshold, target_lang):
        counter = 0
        member = self.portal.portal_membership.getAuthenticatedMember()
        if not member.has_role("Manager"):
            return "You must be a Manager to access this script !"
        logger.info("Querying objects to fix")
        brains = self.get_objects_to_correct()
        logger.info("Treating {} Meeting or MeetingItems".format(len(brains)))
        for brain in brains:
            if brain.__class__.__name__ == "PloneFlare":
                lang = brain['Language']
            else:
                lang = brain.Language()

            if lang not in (target_lang, 'any'):
                if brain.meta_type == "Meeting":
                    self.meeting_counter += 1
                elif brain.meta_type == "MeetingItem":
                    self.item_counter += 1

                if lang not in self.odds:
                    self.odds.append("'{}'".format(lang))

                obj = brain.getObject()
                obj.setLanguage("fr")
                if brain.meta_type != "Meeting" or reindex_meetings:
                    obj.reindexObject(idxs=['modified', 'ModificationDate', 'Date'])
                if brain.meta_type not in self.treated_count:
                    self.treated_count[brain.meta_type] = 1
                else:
                    self.treated_count[brain.meta_type] += 1

                counter += 1
                if counter % commit_threshold == 0:
                    self.commit_and_print_state()
        self.commit_and_print_state()


def fix_language(self, reindex_meetings=False, commit_threshold=1000, target_lang="fr"):
    start_date = datetime.now()
    logger.info("Start fixing languages converting to {}".format(target_lang))
    fixer = FixLanguage(self)
    fixer.run(reindex_meetings, commit_threshold, target_lang)
    end_date = datetime.now()
    seconds = end_date - start_date
    seconds = seconds.seconds
    hours = seconds / 3600
    minutes = (seconds - hours * 3600) / 60
    logger.info(
        "Fixing finished in {0} seconds ({1} h {2} m).".format(seconds, hours, minutes)
    )
