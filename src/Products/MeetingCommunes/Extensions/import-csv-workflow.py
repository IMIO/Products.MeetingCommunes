#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
from os.path import isfile, join, exists

from backports import csv

#  pip install backports.csv
from collective.contact.plonegroup.utils import get_organizations
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
content_types = {
    ".aac": "audio/aac",
    ".abw": "application/x-abiword",
    ".arc": "application/octet-stream",
    ".avi": "video/x-msvideo",
    ".azw": "application/vnd.amazon.ebook",
    ".bin": "application/octet-stream",
    ".bmp": "image/bmp",
    ".bz": "application/x-bzip",
    ".bz2": "application/x-bzip2",
    ".csh": "application/x-csh",
    ".css": "text/css",
    ".csv": "text/csv",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".eot": "application/vnd.ms-fontobject",
    ".epub": "application/epub+zip",
    ".gif": "image/gif",
    ".htm": "text/html",
    ".html": "text/html",
    ".ico": "image/x-icon",
    ".ics": "text/calendar",
    ".jar": "application/java-archive",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".js": "application/javascript",
    ".json": "application/json",
    ".mid": "audio/midi",
    ".midi": "audio/midi",
    ".mpeg": "video/mpeg",
    ".mpkg": "application/vnd.apple.installer+xml",
    ".msg": "application/vnd.ms-outlook",
    ".odp": "application/vnd.oasis.opendocument.presentation",
    ".ods": "application/vnd.oasis.opendocument.spreadsheet",
    ".odt": "application/vnd.oasis.opendocument.text",
    ".oga": "audio/ogg",
    ".ogv": "video/ogg",
    ".ogx": "application/ogg",
    ".otf": "font/otf",
    ".png": "image/png",
    ".pdf": "application/pdf",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".rar": "application/x-rar-compressed",
    ".rtf": "application/rtf",
    ".sh": "application/x-sh",
    ".svg": "image/svg+xml",
    ".swf": "application/x-shockwave-flash",
    ".tar": "application/x-tar",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
    ".ts": "application/typescript",
    ".ttf": "font/ttf",
    ".vsd": "application/vnd.visio",
    ".wav": "audio/x-wav",
    ".weba": "audio/webm",
    ".webm": "video/webm",
    ".webp": "image/webp",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".xhtml": "application/xhtml+xml",
    ".xls": "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xml": "application/xml",
    ".xul": "application/vnd.mozilla.xul+xml",
    ".zip": "application/zip",
    ".3gp": "video/3gpp",
    ".3g2": "video/3gpp2",
    ".7z": "application/x-7z-compressed",
}


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
    annexFileTypeDecision = "annexeDecision"

    def __init__(
        self,
        portal_type,
        external_id,
        creator,
        creator_id,
        created_on,
        title,
        proposing_group,
        category,
        meeting_date,
        motivation,
        decision,
        meeting_external_id,
        beneficiary,
        annexes_base_path,
    ):
        self.portal_type = portal_type
        self.external_id = external_id
        self.title = safe_unicode(title)
        self.creator = creator
        self.creator_id = creator_id
        self.created_on = datetime.strptime(created_on, "%Y-%m-%d %H:%M:%S.%f")
        self.proposing_group = proposing_group
        self.category = category
        self.meeting_date = datetime.strptime(meeting_date, "%Y-%m-%d %H:%M:%S.%f")
        self.motivation = clean_xhtml(motivation)
        self.decision = clean_xhtml(decision)
        self.meeting_external_id = meeting_external_id
        self.beneficiary = beneficiary != u"NULL" and safe_unicode(beneficiary) or None
        path = "{}/{}".format(annexes_base_path, external_id)
        if exists(path):
            self.annexes = [
                "{}/{}".format(path, f)
                for f in os.listdir(path)
                if isfile(join(path, f))
            ]
        else:
            self.annexes = []


class CSVMeeting:
    def __init__(self, portal_type, external_id, date, created_on, assembly):
        self.portal_type = portal_type
        self.external_id = external_id
        self.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        self.created_on = datetime.strptime(created_on, "%Y-%m-%d %H:%M:%S.%f")
        self.assembly = assembly
        self.items = []


class ImportCSV:
    def __init__(
        self,
        portal,
        f_group_mapping,
        f_items,
        f_meetings,
        annex_dir_path,
        default_group,
        default_category=None,
    ):
        self.grp_id_mapping = {}
        self.portal = portal
        self.f_group_mapping = f_group_mapping
        self.f_items = f_items
        self.f_meetings = f_meetings
        self.annex_dir_path = annex_dir_path
        self.default_group = default_group
        self.default_category = default_category
        self.errors = {"io": [], "item": [], "meeting": [], "item_without_annex": []}
        self.item_counter = 0
        self.meeting_counter = 0
        self.groups = {}
        self._deactivated_recurring_items = []

    # def _check_file_exists(self, path):
    #     _path = path
    #     if not os.path.isfile(_path):
    #         raise IOError(u"File not found {path}.".format(path=_path))
    #     return _path

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
        file_ext = path[path.rindex(".") :].lower()
        content_type = content_types[file_ext]

        the_annex = createContentInContainer(
            container=context,
            portal_type=annex_portal_type,
            title=annex_title or "Annex",
            file=self._annex_file_content(path),
            content_category=annex_type_id,
            content_type=content_type,
            contentType=content_type,
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

    def add_annexe_to_object(self, obj, path, title):
        try:
            self.add_annex(obj, path, annex_title=title)
            return True
        except IOError as e:
            self.errors["io"].append(e.message)
            logger.warning(e.message)
            return False

    @staticmethod
    def add_meeting_to_dict(dictionary, meeting):
        if meeting.external_id in dictionary:
            raise KeyError(
                "2 Meetings have the same id {0}".format(meeting.external_id)
            )
        dictionary[meeting.external_id] = meeting

    def parse_and_clean_raw_csv_item(self, csv_item, portaltype):
        # Because numbers are not numbers but unicode chars...
        _id = csv_item[0].encode("ascii", errors="ignore")
        external_id = int(_id)
        _id = csv_item[9].encode("ascii", errors="ignore")
        meeting_external_id = int(_id)

        creator = safe_unicode(csv_item[2].strip())
        creator_id = u"{}{}".format(creator[0], creator.split(u" ")[-1])
        creator_id = creator_id.lower()

        item = CSVMeetingItem(
            portal_type=portaltype,
            external_id=external_id,
            title=safe_unicode(csv_item[1].strip()),
            creator=creator,
            creator_id=creator_id,
            created_on=safe_unicode(csv_item[3].strip()),
            proposing_group=safe_unicode(csv_item[4].strip()),
            category=safe_unicode(csv_item[5].strip()),
            meeting_date=safe_unicode(csv_item[6].strip()),
            motivation=safe_unicode(csv_item[7].strip()),
            decision=safe_unicode(csv_item[8].strip()),
            meeting_external_id=meeting_external_id,
            beneficiary=safe_unicode(csv_item[10].strip()),
            annexes_base_path=self.annex_dir_path,
        )
        return item

    def load_items(self, delib_file, portaltype, meetings):
        logger.info("Load {0}".format(delib_file))
        csv.field_size_limit(100000000)
        with io.open(delib_file, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=u";")
            for row in reader:
                try:
                    meeting_external_id = int(row[9].strip())
                    if meeting_external_id not in meetings:
                        logger.info("Unknown meeting for item : {row}".format(row=row))
                    else:
                        item = self.parse_and_clean_raw_csv_item(row, portaltype)
                        meeting = meetings[meeting_external_id]
                        meeting.items.append(item)
                except ValueError as e:
                    self.errors["item"].append(e.message)
                    logger.info(e.message)

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
        meeting.setAssembly("")
        meeting.setDate(meeting_date)
        meeting.setStartDate(meeting_date)

        # meeting.at_post_create_script()
        meeting.processForm(values={"dummy": None})
        meeting.setCreationDate(DateTime(csv_meeting.created_on))
        logger.info("Created meeting {id} {date}".format(id=_id, date=meeting.Title()))

        logger.info(
            "Adding {items} items to meeting of {date}".format(
                items=len(csv_meeting.items), date=meeting.Title()
            )
        )
        self.portal.REQUEST["PUBLISHED"] = meeting
        for csv_item in csv_meeting.items:
            self.insert_and_present_item(member_folder, csv_item)

        if meeting.getItems():
            meeting.portal_workflow.doActionFor(meeting, "freeze")
            meeting.portal_workflow.doActionFor(meeting, "decide")
            meeting.portal_workflow.doActionFor(meeting, "close")

            for item in meeting.getItems():
                item.setModificationDate(meeting_date)
                item.reindexObject(idxs=["modified"])

        meeting.setModificationDate(meeting_date)

        meeting.reindexObject(idxs=["modified"])
        self.meeting_counter += 1
        transaction.commit()

    def get_matching_proposing_group(self, proposing_group):
        grp_id = (
            proposing_group.strip() in self.groups
            and self.groups[proposing_group.strip()]
        )
        return (
            grp_id in self.grp_id_mapping
            and self.grp_id_mapping[grp_id].UID()
            or self.default_group
        )

    def insert_and_present_item(self, member_folder, csv_item):
        tme = DateTime(csv_item.created_on, datefmt="international")

        itemid = member_folder.invokeFactory(
            type_name=csv_item.portal_type,
            id=csv_item.external_id,
            date=tme,
            title=csv_item.title,
        )
        item = getattr(member_folder, itemid)
        item.setProposingGroup(
            self.get_matching_proposing_group(csv_item.proposing_group)
        )
        user = api.user.get(csv_item.creator_id)
        if user:
            item.setCreators(user.id)
        else:
            item.setCreators("csvimport")
        item.setDescription(
            u"<p>Créateur originel : {creator}</p>".format(creator=csv_item.creator)
        )

        item.setMotivation(csv_item.motivation)
        item.setDecision(csv_item.decision)

        if csv_item.beneficiary:
            item.setDescription(
                u"{}{}".format(
                    safe_unicode(item.Description()),
                    u"<p>Bénéficiaire : {}</p>".format(csv_item.beneficiary),
                )
            )
        # do not call item.at_post_create_script(). This would get only throuble with cancel quick edit in objects
        item.processForm(values={"dummy": None})
        item.setCreationDate(tme)

        if csv_item.annexes:
            for annex_file in csv_item.annexes:
                # remove weird naming with double extension
                annex_name = annex_file.replace(".doc.docx", ".doc")
                annex_name = annex_name[
                    annex_name.rindex("/") + 1 : annex_name.rindex(".")
                ]
                annex_name = annex_name.strip()
                annex_name = annex_name.strip("-_")
                inserted = self.add_annexe_to_object(
                    item, annex_file, safe_unicode(annex_name)
                )
                if not inserted:
                    item.setDescription(
                        "{}{}".format(
                            item.Description(),
                            "<p>Fichier non trouvé : {}</p>".format(
                                annex_file[annex_file.rindex("/") + 1 :]
                            ),
                        )
                    )
        else:
            item.setDescription(
                "{}{}".format(item.Description(), "<p>Ce point n'a aucune annexe</p>")
            )

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
        self.item_counter += 1

    def run(self):
        member = self.portal.portal_membership.getAuthenticatedMember()
        if not member.has_role("Manager"):
            raise ValueError("You must be a Manager to access this script !")

        # Load all csv into memory
        cfg_groups = get_organizations(only_selected=False)
        for group in cfg_groups:
            self.grp_id_mapping[group.UID()] = group

        logger.info("Load {0}".format(self.f_group_mapping))
        with io.open(self.f_group_mapping, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                grp_id = row[1].strip()
                if grp_id in self.grp_id_mapping:
                    self.groups[row[0].strip()] = self.grp_id_mapping[grp_id].UID()
                else:
                    self.groups[row[0].strip()] = self.default_group

        meetings_cas = {}
        with io.open(self.f_meetings, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=u";")
            # TypeSeance	DateSeance	OJ	PV
            for row in reader:
                # Because numbers are not numbers but unicode chars...
                _id = row[0].encode("ascii", errors="ignore")
                external_id = int(_id)
                meeting = CSVMeeting(
                    portal_type="Meetingcas",
                    external_id=external_id,
                    date=safe_unicode(row[1].strip()),
                    created_on=safe_unicode(row[2].strip()),
                    assembly=safe_unicode(row[3].strip()),
                )

                self.add_meeting_to_dict(meetings_cas, meeting)
        self.load_items(self.f_items, "MeetingItemcas", meetings_cas)
        # insert All
        logger.info("Insert Objects to CAS")
        self.disable_recurring_items("meeting-config-cas")
        member_folder = self.portal.Members.csvimport.mymeetings.get(
            "meeting-config-cas"
        )
        for csv_meeting in meetings_cas.values():
            self.insert_and_close_meeting(member_folder, csv_meeting)

        self.re_enable_recurring_items("meeting-config-cas")

        return self.meeting_counter, self.item_counter, self.errors

    def disable_recurring_items(self, _meeting_config_id):
        cfg = self.portal.portal_plonemeeting.get(_meeting_config_id)
        self._deactivated_recurring_items = []
        for item in cfg.getRecurringItems():
            self.portal.portal_workflow.doActionFor(item, "deactivate")
            self._deactivated_recurring_items.append(item.UID())

    def re_enable_recurring_items(self, _meeting_config_id):
        cfg = self.portal.portal_plonemeeting.get(_meeting_config_id)
        for item in cfg.getRecurringItems(False):
            if item.UID() in self._deactivated_recurring_items:
                self.portal.portal_workflow.doActionFor(item, "activate")


def import_data_from_csv(
    self,
    f_group_mapping,
    f_items,
    f_meetings,
    annex_dir_path,
    default_group,
    default_category=None,
):
    start_date = datetime.now()
    import_csv = ImportCSV(
        self,
        f_group_mapping,
        f_items,
        f_meetings,
        annex_dir_path,
        default_group,
        default_category,
    )
    meeting_counter, item_counter, errors = import_csv.run()
    logger.info(
        u"Inserted {meeting} meetings and {item} meeting items.".format(
            meeting=meeting_counter, item=item_counter
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
    minutes = (seconds - hours * 3600) / 60
    logger.info(
        u"Import finished in {0} seconds ({1} h {2} m).".format(seconds, hours, minutes)
    )
