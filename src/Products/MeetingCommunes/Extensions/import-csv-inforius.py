#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import io
import os
import re
from datetime import datetime
from os.path import isfile, join, exists

from Products.PloneMeeting import logger
from bleach.sanitizer import Cleaner

import transaction
from DateTime import DateTime
from Products.CMFPlone.utils import safe_unicode
from backports import csv
#  pip install backports.csv
from collective.contact.plonegroup.utils import get_organizations
from collective.iconifiedcategory.utils import calculate_category_id
from collective.iconifiedcategory.utils import get_config_root
from imio.helpers.content import richtextval
from plone import namedfile, api
from plone.app.querystring import queryparser
from plone.dexterity.utils import createContentInContainer

# see https://developer.mozilla.org/fr/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
content_types = {
    ".aac": "audio/aac",
    ".abw": "application/x-abiword",
    ".avi": "video/x-msvideo",
    ".azw": "application/vnd.amazon.ebook",
    ".bmp": "image/bmp",
    ".bz": "application/x-bzip",
    ".bz2": "application/x-bzip2",
    ".col": "application/msword",
    ".csh": "application/x-csh",
    ".css": "text/css",
    ".csv": "text/csv",
    ".djvu": "image/vnd.djvu",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".eot": "application/vnd.ms-fontobject",
    ".epub": "application/epub+zip",
    ".gif": "image/gif",
    ".gpx": "application/gpx+xml",
    ".heic": "image/heic",
    ".ico": "image/x-icon",
    ".ics": "text/calendar",
    ".jar": "application/java-archive",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".json": "application/json",
    ".log": "text/plain",
    ".mht": "message/rfc822",
    ".mhtml": "message/rfc822",
    ".mid": "audio/midi",
    ".midi": "audio/midi",
    ".mpeg": "video/mpeg",
    ".mpkg": "application/vnd.apple.installer+xml",
    ".msg": "application/vnd.ms-outlook",
    ".odp": "application/vnd.oasis.opendocument.presentation",
    ".ods": "application/vnd.oasis.opendocument.spreadsheet",
    ".odt": "application/vnd.oasis.opendocument.text",
    ".oft": "application/vnd.ms-outlook",
    ".oga": "audio/ogg",
    ".ogv": "video/ogg",
    ".ogx": "application/ogg",
    ".otf": "font/otf",
    ".oxps": "application/oxps, application/vnd.ms-xpsdocument",
    ".png": "image/png",
    ".pdf": "application/pdf",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".rar": "application/x-rar-compressed",
    ".rtf": "application/rtf",
    ".svg": "image/svg+xml",
    ".swf": "application/x-shockwave-flash",
    ".tar": "application/x-tar",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
    ".ts": "application/typescript",
    ".ttf": "font/ttf",
    ".txt": "text/plain",
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
    ".xlsm": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xml": "application/xml",
    ".xps": "application/oxps, application/vnd.ms-xpsdocument",
    ".xul": "application/vnd.mozilla.xul+xml",
    ".zip": "application/zip",
    ".3gp": "video/3gpp",
    ".3g2": "video/3gpp2",
    ".7z": "application/x-7z-compressed",
}

datetime_format = "%Y-%m-%d %H:%M:%S"

cleaner = Cleaner(tags=['p', 'br', 'ul', 'ol', 'li', 'strong', 'u', 'em', 'sup', 'sub', 'a', 'img'
                        'table', 'thead', 'tr', 'th', 'tbody', 'td'],
                  attributes={'a': ['href', 'alt'],
                              'img': ['src', 'alt', 'width', 'height']},
                  strip=True)

commit_step = 10


def clean_xhtml(html_value):
    xhtml = html_value.strip()
    if not xhtml.startswith(u"<p"):
        xhtml = u"<p>" + xhtml
    if not xhtml.endswith(u"</p>"):
        xhtml += u"</p>"
    # replace multiple br
    xhtml = xhtml.replace(u"\n", u"").strip()
    xhtml = re.sub(r'<br.?>((\s|\n)*<br.?>)+', u'</p>\n<p>', xhtml)
    xhtml = xhtml.replace(u"&", u"&amp;").strip()
    xhtml = xhtml.replace(u"\u00A0", u"&nbsp;").strip()
    xhtml = xhtml.replace(u"\u2022", u"*").strip()
    xhtml = xhtml.replace(u"\u25E6", u"*").strip()
    xhtml = xhtml.replace(u"\u2219", u"*").strip()
    xhtml = xhtml.replace(u"\u2023", u"*").strip()
    xhtml = xhtml.replace(u"\u2043", u"*").strip()
    xhtml = xhtml.replace(u"\00B7", u"*").strip()
    cleaned = cleaner.clean(xhtml)
    return cleaned


class CSVMeetingItem:
    annexFileTypeDecision = "annexeDecision"

    # ID    Title    Creator    CreationDate    ServiceID    CategoryID    Motivation    Decision    MeetingID
    def __init__(self, external_id, title, creator, created_on, service, category, motivation, decision, meeting_external_id, annexes_dir, classification=None, folder=None, sub_folder=None):
        self.external_id = external_id
        self.title = safe_unicode(title)
        self.creator = creator and creator or "INCONNU"
        self.created_on = created_on and datetime.strptime(created_on, datetime_format) or None
        self.proposing_group = service
        self.category = category
        self.motivation = clean_xhtml(motivation)
        self.decision = clean_xhtml(decision)
        self.meeting_external_id = meeting_external_id
        self.classification = classification
        self.folder = folder
        self.sub_folder = sub_folder
        path = "{}/{}".format(annexes_dir, external_id)
        if exists(path):
            self.annexes = [
                "{}/{}".format(path, f)
                for f in os.listdir(path)
                if isfile(join(path, f))
            ]
        else:
            self.annexes = []


class CSVMeeting:
    # ID    Date    CreationDate    StartDate    EndDate    Assembly    Type
    def __init__(self, external_id, date, created_on, started_on, ended_on, assembly, portal_type, annexes_dir):
        self.external_id = external_id
        self.date = datetime.strptime(date, datetime_format)
        self.created_on = datetime.strptime(created_on, datetime_format)
        self.started_on = datetime.strptime(started_on, datetime_format)
        self.ended_on = datetime.strptime(ended_on, datetime_format)
        self.assembly = re.sub(r'<br.?\/>', '\n\r', assembly).strip()
        self.portal_type = portal_type
        self.items = []
        path = "{}/{}".format(annexes_dir, external_id)
        if exists(path):
            self.annexes = [
                "{}/{}".format(path, f)
                for f in os.listdir(path)
                if isfile(join(path, f))
            ]
        else:
            self.annexes = []


class ImportCSV:
    def __init__(
        self,
        portal,
        f_group_mapping,
        f_items,
        f_meetings,
        meeting_annex_dir_path,
        item_annex_dir_path,
        default_group,
        hr_group=None,
        default_category_college=None,
        default_category_council=None,
    ):
        self.grp_id_mapping = {}
        self.portal = portal
        self.f_group_mapping = f_group_mapping
        self.f_items = f_items
        self.f_meetings = f_meetings
        self.meeting_annex_dir_path = meeting_annex_dir_path
        self.item_annex_dir_path = item_annex_dir_path
        self.default_group = default_group
        self.hr_group = hr_group
        self.errors = {"io": [], "item": [], "meeting": [], "item_without_annex": []}
        self.item_counter = 0
        self.meeting_counter = 0
        self.groups = {}
        self._deactivated_recurring_items = []

        self.college_cfg = self.portal.portal_plonemeeting.get('meeting-config-college')
        if self.college_cfg is None:
            self.college_cfg = self.portal.portal_plonemeeting.get('meeting-config-zcollege')
        self.college_member_folder = self.portal.Members.csvimport.mymeetings.get(self.college_cfg.getId())
        self.default_category_college = default_category_college

        self.council_cfg = self.portal.portal_plonemeeting.get('meeting-config-council')
        if self.council_cfg is None:
            self.council_cfg = self.portal.portal_plonemeeting.get('meeting-config-zcouncil')
        self.council_member_folder = self.portal.Members.csvimport.mymeetings.get(self.council_cfg.getId())
        self.default_category_council = default_category_council

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
        if file_ext not in content_types:
            message = u"Annex skipped because of unsupported file extension \"{}\" at path {}".format(
                safe_unicode(file_ext),
                safe_unicode(path)
            )
            self.errors["io"].append(message)
            logger.warning(message)
            return None

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

    def add_annexe_to_object(self, obj, path, title, confidential=False):
        try:
            self.add_annex(obj, path, annex_title=title, confidential=confidential)
            return True
        except IOError as e:
            self.errors["io"].append(safe_unicode(e.message))
            logger.warning(e.message)
            return False

    @staticmethod
    def add_meeting_to_dict(dictionary, meeting):
        if meeting.external_id in dictionary:
            raise KeyError(
                "2 Meetings have the same id {0}".format(meeting.external_id)
            )
        dictionary[meeting.external_id] = meeting

    def parse_and_clean_raw_csv_item(self, csv_item):
        # Because numbers are not numbers but unicode chars...
        external_id = int(csv_item[0].strip())
        meeting_external_id = int(csv_item[8].strip())

        item = CSVMeetingItem(external_id=external_id,
                              title=safe_unicode(csv_item[1]),
                              creator=safe_unicode(csv_item[2].strip()),
                              created_on=csv_item[3].strip(),
                              service=csv_item[4].strip(),
                              category=csv_item[5].strip(),
                              motivation=safe_unicode(csv_item[6].strip()),
                              decision=safe_unicode(csv_item[7].strip()),
                              meeting_external_id=meeting_external_id,
                              annexes_dir=self.item_annex_dir_path)
        if len(csv_item) > 9:
            item.classification = csv_item[9].strip()
        if len(csv_item) > 10:
            item.folder = csv_item[10].strip()
        if len(csv_item) > 11:
            item.sub_folder = csv_item[11].strip()

        return item

    def load_items(self, delib_file, meetings):
        logger.info("Load {0}".format(delib_file))
        csv.field_size_limit(100000000)
        self.item_meeting_ids = []
        with io.open(delib_file, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if reader.line_num == 1:
                    # skip header line
                    continue
                try:
                    meeting_external_id = int(row[8].strip())
                    if meeting_external_id not in self.item_meeting_ids:
                        self.item_meeting_ids.append(meeting_external_id)

                    if meeting_external_id not in meetings:
                        logger.info("Unknown meeting for item : {row}".format(row=row))
                    else:
                        item = self.parse_and_clean_raw_csv_item(row)
                        meeting = meetings[meeting_external_id]
                        if meeting.portal_type == self.college_cfg.getMeetingTypeName():
                            portal_type = self.college_cfg.getItemTypeName()
                        elif meeting.portal_type == self.council_cfg.getMeetingTypeName():
                            portal_type = self.council_cfg.getItemTypeName()
                        else:
                            raise NotImplementedError("Unknown meeting type {}".format(type))
                        item.portal_type = portal_type
                        if not item.created_on:
                            item.created_on = meeting.date
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

        meeting_date = csv_meeting.date
        meetingid = member_folder.invokeFactory(
            type_name=csv_meeting.portal_type, id=_id, date=meeting_date
        )
        meeting = getattr(member_folder, meetingid)
        meeting.signatures = None
        if csv_meeting.assembly:
            meeting.assembly = richtextval(csv_meeting.assembly)
        meeting.date = meeting_date
        meeting.start_date = csv_meeting.started_on
        meeting.end_date = csv_meeting.ended_on

        meeting.creation_date = DateTime(csv_meeting.created_on)
        logger.info(u"Created {type} {id} {date}".format(type=csv_meeting.portal_type, id=_id, date=meeting.title))

        if csv_meeting.annexes:
            self.add_all_annexes_to_object(csv_meeting.annexes, meeting, confidential=True)
        else:
            meeting.observations = u"<p><strong>Cette séance n'a aucune annexe</strong></p>"

        logger.info(
            u"Adding {items} items to {type} of {date}".format(
                items=len(csv_meeting.items), type=csv_meeting.portal_type, date=meeting.title
            )
        )

        self.portal.REQUEST["PUBLISHED"] = meeting
        for csv_item in csv_meeting.items:
            self.insert_and_present_item(member_folder, csv_item)

        if meeting.get_items():
            meeting.portal_workflow.doActionFor(meeting, "freeze")
            meeting.portal_workflow.doActionFor(meeting, "decide")
            meeting.portal_workflow.doActionFor(meeting, "close")

            for item in meeting.get_items():
                item.setModificationDate(meeting_date)
                item.reindexObject(idxs=["modified"])

        meeting.setModificationDate(DateTime(meeting_date))

        meeting.reindexObject(idxs=["modified"])
        self.meeting_counter += 1
        if self.meeting_counter % commit_step == 0:
            transaction.commit()

    def get_matching_proposing_group(self, csv_item):
        # avoid leak of sensitive HR topics
        if self.hr_group and csv_item.classification and re.match(r'^2\.?08.*$', csv_item.classification):
            return self.hr_group

        grp_id = (
            csv_item.proposing_group.strip() in self.groups
            and self.groups[csv_item.proposing_group.strip()]
        )
        return (
            grp_id in self.grp_id_mapping
            and self.grp_id_mapping[grp_id].UID()
            or self.default_group
        )

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

    def insert_and_present_item(self, member_folder, csv_item):
        tme = DateTime(csv_item.created_on, datefmt="international")

        itemid = member_folder.invokeFactory(
            type_name=csv_item.portal_type,
            id=csv_item.external_id,
            date=tme,
            title=csv_item.title,
        )
        item = getattr(member_folder, itemid)

        if csv_item.portal_type == self.college_cfg.getItemTypeName():
            item_meeting_cfg = self.college_cfg
        elif csv_item.portal_type == self.council_cfg.getItemTypeName():
            item_meeting_cfg = self.council_cfg
        else:
            raise ValueError('Impossible to determine MC for ' + csv_item.portal_type)

        item.setProposingGroup(
            self.get_matching_proposing_group(csv_item)
        )

        if item_meeting_cfg.getId() == self.college_cfg.getId():
            item.setCategory(self.default_category_college)
        elif item_meeting_cfg.getId() == self.council_cfg.getId():
            item.setCategory(self.default_category_council)

        item.setCreators("csvimport")
        description = u"<p>Service originel : {}</p>".format(csv_item.proposing_group)
        description += u"<p>Créateur originel : {}</p>".format(csv_item.creator)
        if csv_item.classification:
            description += u"<p>Classement : {}</p>".format(csv_item.classification)
        if csv_item.folder:
            description += u"<p>Farde : {}</p>".format(csv_item.folder)
        if csv_item.sub_folder:
            description += u"<p>Chemise : {}</p>".format(csv_item.sub_folder)
        item.setDescription(description)
        item.setMotivation(csv_item.motivation)
        item.setDecision(csv_item.decision)

        # do not call item.at_post_create_script(). This would get only throuble with cancel quick edit in objects
        item.processForm(values={"dummy": None})
        item.setCreationDate(tme)

        if csv_item.annexes:
            self.add_all_annexes_to_object(csv_item.annexes, item)
        else:
            item.setDescription(
                "{}{}".format(item.Description(), "<p><strong>Ce point n'a aucune annexe</strong></p>")
            )

        self.portal.portal_workflow.doActionFor(item, 'validate')
        self.portal.portal_workflow.doActionFor(item, 'present')
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

        meetings = {}
        logger.info("Load {0}".format(self.f_meetings))
        with io.open(self.f_meetings, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if reader.line_num == 1:
                    # skip header line
                    continue
                # Because numbers are not numbers but unicode chars...
                external_id = int(row[0].strip())
                csv_type = safe_unicode(row[6].strip()).lower()
                if 'col' in csv_type:
                    portal_type = self.college_cfg.getMeetingTypeName()
                elif 'cons' in csv_type:
                    portal_type = self.council_cfg.getMeetingTypeName()
                else:
                    continue

                meeting = CSVMeeting(external_id=external_id,
                                     date=row[1].strip(),
                                     created_on=row[2].strip(),
                                     started_on=row[3].strip(),
                                     ended_on=row[4].strip(),
                                     assembly=safe_unicode(row[5].strip()),
                                     portal_type=portal_type,
                                     annexes_dir=self.meeting_annex_dir_path)

                self.add_meeting_to_dict(meetings, meeting)
        self.load_items(self.f_items, meetings)
        # insert All
        self.disable_recurring_items()
        logger.info("Inserting Objects")
        try:
            for csv_meeting in meetings.values():
                if csv_meeting.portal_type == self.college_cfg.getMeetingTypeName():
                    self.insert_and_close_meeting(self.college_member_folder, csv_meeting)
                elif csv_meeting.portal_type == self.council_cfg.getMeetingTypeName():
                    self.insert_and_close_meeting(self.council_member_folder, csv_meeting)
                else:
                    raise NotImplementedError(u"Not managed meeting type '{}' for meeting id {}".format(csv_meeting.type, meeting.external_id))
        finally:
            tool = api.portal.get_tool('portal_plonemeeting')
            self.re_enable_recurring_items()
            tool.invalidateAllCache()

        return self.meeting_counter, self.item_counter, self.errors

    def disable_recurring_items(self):
        self._deactivated_recurring_items = []
        for cfg in (self.college_cfg, self.council_cfg):
            for item in cfg.getRecurringItems():
                self.portal.portal_workflow.doActionFor(item, 'deactivate')
                self._deactivated_recurring_items.append(item.UID())

    def re_enable_recurring_items(self):
        for cfg in (self.college_cfg, self.council_cfg):
            for item in cfg.getRecurringItems():
                if item.UID() in self._deactivated_recurring_items:
                    self.portal.portal_workflow.doActionFor(item, 'activate')


def import_data_from_csv(
    self,
    f_group_mapping,
    f_items,
    f_meetings,
    default_group,
    hr_group,
    meeting_annex_dir_path,
    item_annex_dir_path,
    default_category_college=None,
    default_category_council=None,
):
    start_date = datetime.now()
    import_csv = ImportCSV(
        self,
        f_group_mapping,
        f_items,
        f_meetings,
        meeting_annex_dir_path,
        item_annex_dir_path,
        default_group,
        hr_group,
        default_category_college,
        default_category_council,
    )
    meeting_counter, item_counter, errors = import_csv.run()
    logger.info(
        u"Inserted {meeting} meetings and {item} meeting items.".format(
            meeting=meeting_counter, item=item_counter
        )
    )
    logger.warning(
        u"{malforemed} meeting items were not created due to missing data in csv :\n\t{list}".format(
            malforemed=len(errors["item"]), list=u"\n\t ".join(errors["item"])
        )
    )

    logger.warning(
        u"{ioerr} errors occured while adding annexes :\n{list}".format(
            ioerr=len(errors["io"]), list=u"\n\t ".join(errors["io"])
        )
    )

    logger.warning(
        u"{meeting} meetings where skipped because they have no annex or no items :\n\t{list}".format(
            meeting=len(errors["meeting"]), list=u"\n\t ".join(errors["meeting"])
        )
    )

    without_annex = u"\n\t ".join(safe_unicode(errors["item_without_annex"]))
    logger.warning(
        u"{items} meeting items where skipped :\n\t{list}".format(
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
