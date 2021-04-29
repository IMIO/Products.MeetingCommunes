#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
from os.path import isfile, join, exists

from backports import csv

#  pip install backports.csv
from collective.iconifiedcategory.utils import calculate_category_id
from collective.iconifiedcategory.utils import get_config_root
from DateTime import DateTime
from datetime import datetime
from plone import namedfile, api
from plone.app.querystring import queryparser
from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.utils import safe_unicode
from Products.PloneMeeting import logger

import io
import os
import transaction

# see https://developer.mozilla.org/fr/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
be_meeting_type = 'MeetingExecutive'
ca_meeting_type = 'MeetingCA'
datetime_format = "%Y%m%d"


# Because we got an ugly csv with ugly formatting and a shit load of useless M$ formatting.
def clean_xhtml(xhtml_value):
    line = re.sub(r"<!--.*?-->", u"", xhtml_value.strip())
    line = re.sub(r' ?style=".*?"', u"", line.strip())
    line = re.sub(r' ?class=".*?"', u"", line.strip())
    line = re.sub(r' ?lang=".*?"', u"", line.strip())
    line = re.sub(r"<font.*?>", u"", line.strip())
    line = re.sub(r"<h\d*", u"<p", line.strip())
    line = re.sub(r"</h\d*", u"</p", line.strip())

    line = line.replace(u"</font>", u"").strip()
    line = line.replace(u"\u00A0", u"&nbsp;").strip()
    line = line.replace(u"<o:p></o:p>", u"").strip()
    line = line.replace(u"<o:p>", u"<p>").strip()
    line = line.replace(u"</o:p>", u"</p>").strip()
    line = line.replace(u"<div>", u"<p>").strip()
    line = line.replace(u"</div>", u"</p>").strip()
    line = line.replace(u"<p><br>", u"<p>").strip()
    if not re.match(r"^<p.*?</p>$", line):
        if line.endswith(u"<br>"):
            line = line[:-4]
        if line.startswith(u"<p"):
            line = u"{}</p>".format(line)
        else:
            line = u"<p>{}</p>".format(line)
    return line


class CSVMeetingItem:
    def __init__(self, meeting_external_id, external_id, title, decision):
        self.external_id = external_id
        self.title = safe_unicode(title)
        self.decision = clean_xhtml(decision)
        self.meeting_external_id = meeting_external_id


class CSVMeeting:
    def __init__(self, external_id, assembly, annexes_dir, portal_type):
        self.external_id = external_id
        self.date = datetime.strptime(str(external_id), datetime_format)
        self.assembly = assembly.strip().replace("  ", "\n\r")
        self.portal_type = portal_type
        self.items = []
        if portal_type == "MeetingCA":
            prefix = 'ca'
        elif portal_type == "MeetingExecutive":
            prefix = 'be'
        else:
            raise ValueError("Not managed portal_type")

        path = "{}/{}{}.pdf".format(annexes_dir, prefix, external_id)
        if exists(path):
            self.annexes = [path]
        else:
            self.annexes = []


class ImportCSV:
    def __init__(
        self,
        portal,
        f_items_be,
        f_items_ca,
        f_meetings_be,
        f_meetings_ca,
        meeting_annex_dir_path,
        default_group,
        default_category_be=None,
        default_category_ca=None,
    ):
        self.portal = portal
        self.f_items_be = f_items_be
        self.f_items_ca = f_items_ca
        self.f_meetings_be = f_meetings_be
        self.f_meetings_ca = f_meetings_ca
        self.meeting_annex_dir_path = meeting_annex_dir_path
        self.default_group = default_group
        self.errors = {"io": [], "item": [], "meeting": [], "item_without_annex": []}
        self.item_be_counter = 0
        self.item_ca_counter = 0
        self.meeting_be_counter = 0
        self.meeting_ca_counter = 0
        self._deactivated_recurring_items = []

        self.be_cfg = self.portal.portal_plonemeeting.get('executive')
        self.be_member_folder = self.portal.Members.csvimport.mymeetings.get('executive')
        self.default_category_be = default_category_be
        self.be_portal_type = self.be_cfg.getItemTypeName()

        self.ca_cfg = self.portal.portal_plonemeeting.get('ca')
        self.ca_member_folder = self.portal.Members.csvimport.mymeetings.get('ca')
        self.default_category_ca = default_category_ca
        self.ca_portal_type = self.ca_cfg.getItemTypeName()

        self.meetings_be = {}
        self.meetings_ca = {}

    def add_annex(
        self,
        context,
        path,
        annex_type=None,
        annex_title=None,
        to_print=False,
        confidential=False,
    ):
        """Adds an annex to p_item.
           If no p_annexType is provided, self.annexFileType is used.
           If no p_annexTitle is specified, the predefined title of the annex type is used."""
        # _path = self._check_file_exists(path)

        if annex_type is None:
            annex_type = "annexe"

        # get complete annexType id that is like
        # 'meeting-config-id-annexes_types_-_item_annexes_-_financial-analysis'
        annexes_config_root = get_config_root(context)
        annex_type_id = calculate_category_id(annexes_config_root.get(annex_type))

        annex_portal_type = "annex"

        the_annex = createContentInContainer(
            container=context,
            portal_type=annex_portal_type,
            title=annex_title or "Annex",
            file=self._annex_file_content(path),
            content_category=annex_type_id,
            content_type="application/pdf",
            contentType="application/pdf",
            to_print=to_print,
            confidential=confidential,
        )
        return the_annex

    def object_already_exists(self, obj_id, portal_type):
        catalog_query = [
            {
                "i": "portal_type",
                "o": "plone.app.querystring.operation.selection.is",
                "v": portal_type,
            },
            {
                "i": "id",
                "o": "plone.app.querystring.operation.selection.is",
                "v": obj_id,
            },
        ]
        query = queryparser.parseFormquery(self.portal, catalog_query)
        res = self.portal.portal_catalog(**query)
        if res:
            logger.info("Already created {object}".format(object=obj_id))
        return res

    @staticmethod
    def _annex_file_content(_path):
        if not os.path.isfile(_path):
            logger.info("Le fichier %s n'a pas ete trouve." % _path)
            return None

        with open(_path, "r") as annex_file:
            name = safe_unicode(os.path.basename(_path))

            annex_read = annex_file.read()
            annex_blob = namedfile.NamedBlobFile(annex_read, filename=name)
            return annex_blob

    def add_annexe_to_object(self, obj, path, title, confidential=False):
        try:
            self.add_annex(obj, path, annex_title=title, confidential=confidential)
            return True
        except IOError as e:
            self.errors["io"].append(e.message)
            logger.warning(e.message)
            return False

    @staticmethod
    def add_meeting_to_dict(dictionary, meeting):
        if meeting.external_id in dictionary:
            print("2 {0} have the same id {1}".format(meeting.portal_type, meeting.external_id))
            # raise KeyError(
            #     "2 {0} have the same id {1}".format(meeting.portal_type, meeting.external_id)
            # )
        dictionary[meeting.external_id] = meeting

    def parse_and_clean_raw_csv_item(self, csv_item, meetings):
        # Because numbers are not numbers but unicode chars...
        meeting_external_id = int(csv_item[0].strip())
        external_id = int(csv_item[1].strip())

        if meeting_external_id not in meetings:
            logger.info("Unknown meeting {} for item {}".format(meeting_external_id, external_id))
            return None

        item = CSVMeetingItem(external_id=external_id,
                              title=safe_unicode(csv_item[2]),
                              decision=safe_unicode(csv_item[3].strip()),
                              meeting_external_id=meeting_external_id)
        return item

    def load_items(self, delib_file, meetings):
        logger.info("Load {0}".format(delib_file))
        csv.field_size_limit(100000000)
        with io.open(delib_file, "r", encoding='latin-1') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if reader.line_num == 1:
                    # skip header line
                    continue
                try:
                    item = self.parse_and_clean_raw_csv_item(row, meetings)
                    if item:
                        meeting = meetings[item.meeting_external_id]
                        if meeting.portal_type == be_meeting_type:
                            portal_type = self.be_portal_type
                        elif meeting.portal_type == ca_meeting_type:
                            portal_type = self.ca_portal_type
                        else:
                            raise NotImplementedError("Unknown meeting type {}".format(type))
                        item.portal_type = portal_type
                        meeting.items.append(item)
                except ValueError as e:
                    self.errors["item"].append(e.message)
                    logger.info(e.message)

    def load_meetings(self, f_meetings, meeting_dict, portal_type):
        logger.info("Load {0}".format(f_meetings))
        with io.open(f_meetings, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if reader.line_num == 1:
                    # skip header line
                    continue
                # Because numbers are not numbers but unicode chars...
                external_id = int(row[0].strip())
                meeting = CSVMeeting(external_id=external_id,
                                     assembly=safe_unicode(row[1].strip()),
                                     portal_type=portal_type,
                                     annexes_dir=self.meeting_annex_dir_path)

                self.add_meeting_to_dict(meeting_dict, meeting)

    def _check_meeting_data(self, csv_meeting):
        if not csv_meeting.items:
            message = "Meeting id {id} has no item. Skipping...".format(
                id=csv_meeting.external_id
            )
            logger.info(message)
            self.errors["meeting"].append(message)
            return False

        return True

    def insert_and_close_meeting(self, member_folder, csv_meeting):
        if not self._check_meeting_data(csv_meeting):
            return

        _id = "meetingimport.{external_id}".format(external_id=csv_meeting.external_id)

        meeting = self.object_already_exists(_id, csv_meeting.portal_type)
        if meeting and meeting[0]:
            message = "Skipping meeting {id} and it items because it already exists".format(
                id=_id
            )
            logger.info(message)
            self.errors["meeting"].append(message)
            return

        meeting_date = DateTime(csv_meeting.date)
        meetingid = member_folder.invokeFactory(
            type_name=csv_meeting.portal_type, id=_id, date=meeting_date
        )
        meeting = getattr(member_folder, meetingid)
        meeting.setSignatures("")
        meeting.setAssembly(csv_meeting.assembly)
        meeting.setDate(meeting_date)
        meeting.setStartDate(meeting_date)
        meeting.setEndDate(meeting_date)

        meeting.processForm(values={"dummy": None})
        meeting.setCreationDate(DateTime(meeting_date))
        logger.info("Created {type} {id} {date}".format(type=csv_meeting.portal_type, id=_id, date=meeting.Title()))

        if csv_meeting.annexes:
            self.add_all_annexes_to_object(csv_meeting.annexes, meeting, confidential=True)
        else:
            meeting.setObservations(u"<p><strong>Cette séance n'a aucune annexe</strong></p>")

        logger.info(
            "Adding {items} items to {type} of {date}".format(
                items=len(csv_meeting.items), type=csv_meeting.portal_type, date=meeting.Title()
            )
        )
        self.portal.REQUEST["PUBLISHED"] = meeting
        for csv_item in csv_meeting.items:
            self.insert_and_present_item(member_folder, csv_item, meeting_date)

        if meeting.getItems():
            meeting.portal_workflow.doActionFor(meeting, "freeze")
            meeting.portal_workflow.doActionFor(meeting, "decide")
            meeting.portal_workflow.doActionFor(meeting, "close")

            for item in meeting.getItems():
                item.setModificationDate(meeting_date)
                item.reindexObject(idxs=["modified"])

        meeting.setModificationDate(meeting_date)

        meeting.reindexObject(idxs=["modified"])

        if csv_meeting.portal_type == be_meeting_type:
            self.meeting_be_counter += 1
        elif csv_meeting.portal_type == ca_meeting_type:
            self.meeting_ca_counter += 1

        transaction.commit()

    def add_all_annexes_to_object(self, annexes, obj, confidential=False):
        if annexes:
            for annex_file in annexes:
                # remove weird naming with double extension
                # annex_name = annex_file.replace('\xc2\x82', 'é')
                annex_name = annex_file[
                    annex_file.rindex("/") + 1: annex_file.rindex(".")
                ]
                annex_name = annex_name.strip()
                annex_name = annex_name.strip("-_")
                inserted = self.add_annexe_to_object(
                    obj, annex_file, safe_unicode(annex_name), confidential=confidential
                )
                if not inserted:
                    raise ValueError("Annex not inserted : {}".format(annex_file))

    def insert_and_present_item(self, member_folder, csv_item, tme):
        itemid = member_folder.invokeFactory(
            type_name=csv_item.portal_type,
            id=csv_item.external_id,
            date=tme,
            title=csv_item.title,
        )
        item = getattr(member_folder, itemid)
        item.setProposingGroup(self.default_group)

        if csv_item.portal_type == self.be_portal_type:
            item.setCategory(self.default_category_be)
        elif csv_item.portal_type == self.ca_portal_type:
            item.setCategory(self.default_category_ca)

        item.setCreators("csvimport")
        item.setDecision(csv_item.decision)

        # do not call item.at_post_create_script(). This would get only throuble with cancel quick edit in objects
        item.processForm(values={"dummy": None})
        item.setCreationDate(tme)

        try:
            self.portal.portal_workflow.doActionFor(item, "propose")
        except WorkflowException:
            pass  # propose item is disabled
        try:
            self.portal.portal_workflow.doActionFor(item, "prevalidate")
        except WorkflowException:
            pass  # pre validation isn't used
        self.portal.portal_workflow.doActionFor(item, "validate")
        self.portal.portal_workflow.doActionFor(item, "present")
        item.reindexObject()

        if csv_item.portal_type == self.be_portal_type:
            self.item_be_counter += 1
        elif csv_item.portal_type == self.ca_portal_type:
            self.item_ca_counter += 1

    def run(self):
        member = self.portal.portal_membership.getAuthenticatedMember()
        if not member.has_role("Manager"):
            raise ValueError("You must be a Manager to access this script !")

        # Load all csv into memory
        self.load_meetings(self.f_meetings_be, self.meetings_be, be_meeting_type)
        self.load_meetings(self.f_meetings_ca, self.meetings_ca, ca_meeting_type)

        self.load_items(self.f_items_be, self.meetings_be)
        self.load_items(self.f_items_ca, self.meetings_ca)
        # insert All
        self.disable_recurring_items()
        logger.info("Inserting Objects")

        for meetings in (self.meetings_be, self.meetings_ca):
            for csv_meeting in meetings.values():
                if csv_meeting.portal_type == be_meeting_type:
                    self.insert_and_close_meeting(self.be_member_folder, csv_meeting)
                elif csv_meeting.portal_type == ca_meeting_type:
                    self.insert_and_close_meeting(self.ca_member_folder, csv_meeting)
                else:
                    raise NotImplementedError(u"Not managed meeting type '{}' for meeting id {}".format(csv_meeting.type, csv_meeting.external_id))

        self.re_enable_recurring_items()

        return self.meeting_be_counter, self.meeting_be_counter, self.item_be_counter, self.item_ca_counter, self.errors

    def disable_recurring_items(self):
        self._deactivated_recurring_items = []
        for cfg in (self.be_cfg, self.ca_cfg):
            for item in cfg.getRecurringItems():
                self.portal.portal_workflow.doActionFor(item, 'deactivate')
                self._deactivated_recurring_items.append(item.UID())

    def re_enable_recurring_items(self):
        for cfg in (self.be_cfg, self.ca_cfg):
            for item in cfg.getRecurringItems():
                if item.UID() in self._deactivated_recurring_items:
                    self.portal.portal_workflow.doActionFor(item, 'activate')


def import_data_from_csv(
    self,
    f_items_be,
    f_items_ca,
    f_meetings_be,
    f_meetings_ca,
    meeting_annex_dir_path,
    default_group,
    default_category_be,
    default_category_ca,
):
    start_date = datetime.now()
    import_csv = ImportCSV(
        self,
        f_items_be,
        f_items_ca,
        f_meetings_be,
        f_meetings_ca,
        meeting_annex_dir_path,
        default_group,
        default_category_be,
        default_category_ca,
    )
    meeting_be_counter, meeting_ca_counter, item_be_counter, item_ca_counter, errors = import_csv.run()
    logger.info(
        u"Inserted {meeting} meetings and {item} meeting items in BE.".format(
            meeting=meeting_be_counter, item=item_be_counter
        )
    )
    logger.info(
        u"Inserted {meeting} meetings and {item} meeting items in CA.".format(
            meeting=meeting_ca_counter, item=item_ca_counter
        )
    )
    logger.warning(
        u"{malforemed} meeting items were not created due to missing data in csv :\n{list}".format(
            malforemed=len(errors["item"]), list=u"\n\t ".join(errors["item"])
        )
    )

    logger.warning(
        u"{ioerr} errors occured while adding annexes :\n{list}".format(
            ioerr=len(errors["io"]), list=u"\n\t ".join(errors["io"])
        )
    )

    logger.warning(
        u"{meeting} meetings where skipped because they have no annex or no items :\n{list}".format(
            meeting=len(errors["meeting"]), list=u"\n\t ".join(errors["meeting"])
        )
    )

    without_annex = u"\n\t ".join(safe_unicode(errors["item_without_annex"]))
    logger.warning(
        u"{items} meeting items where skipped :\n{list}".format(
            items=len(errors["item_without_annex"]), list=without_annex
        )
    )
    end_date = datetime.now()
    seconds = end_date - start_date
    seconds = seconds.seconds
    hours = seconds / 3600
    left_sec = seconds - hours * 3600
    minutes = left_sec / 60
    left_sec = left_sec - minutes * 60
    logger.info(
        u"Import finished in {0} seconds ({1} h {2} m {3} s).".format(seconds, hours, minutes, left_sec)
    )
