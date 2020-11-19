# coding=utf-8
import logging
import unicodedata
from abc import ABCMeta, abstractmethod
from datetime import datetime

from distutils.util import strtobool

import requests
import transaction
from Products.PloneMeeting import logger
from Products.PloneMeeting.MeetingItem import MeetingItem
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.utils import org_id_to_uid, normalize
from bs4 import BeautifulSoup
from collective.contact.plonegroup.utils import get_own_organization, select_organization
from imio.helpers.content import transitions
from plone import api
from zope.i18n import translate


# Import HubSessions
# - Importer les séances (assemblée, signataires, ...) => OK
# - Importer les points =>  OK
# - Importer les groupes proposants => OK
# - Importer les catégories => OK
# - Importer les annexes
# - Garder le lien entre Collège et Conseil


def import_data(
    base_url="http://localhost:8090",
    user="admin",
    user_password="admin",
    meetingconfig_id="meeting-config-college",
    verbose=False,
):
    with SilentLogging(("collective.fingerpointing", "imio.helpers.content"), verbose):
        importer = HubSessionsXMLImporter(base_url, user, user_password, meetingconfig_id)
        importer.run()
        logger.info("Import finished - " + meetingconfig_id)
        return "<h1>Success</h1>"


class HubSessionsXMLImporter:
    def __init__(self, base_url, user, user_password, meetingconfig_id):
        self.api = HubSessionsAPI(base_url, user, user_password)
        self.meetingconfig_id = meetingconfig_id

    def run(self):
        self.import_meetings()

    def import_meetings(self):
        meeting_ids = self.api.get_meeting_ids()
        total = len(meeting_ids)
        for i, meeting_id in enumerate(meeting_ids):
            api_meeting = self.api.get_meeting(meeting_id)
            creator_id = api_meeting["creator"]
            self._create_user_if_not_exists(creator_id)

            member_folder = self._get_member_folder(creator_id)

            if self.meetingconfig_id == "meeting-config-college":
                meeting_type = "MeetingCollege"
            else:
                meeting_type = "MeetingCouncil"

            if not hasattr(member_folder, api_meeting["id"]):
                member_folder.invokeFactory(type_name=meeting_type, id=api_meeting["id"], date=api_meeting["date"])
                meeting = getattr(member_folder, api_meeting["id"])
                meeting.setCreators(creator_id)
                meeting.at_post_create_script()
            else:
                meeting = getattr(member_folder, api_meeting["id"])
                continue  # TODO : remove me

            meeting.setSignatures(api_meeting["signatures"])
            meeting.setAssembly(api_meeting["assembly"])
            meeting.setAssemblyExcused(api_meeting["assembly_excused"])
            meeting.setAssemblyAbsents(api_meeting["assembly_absents"])
            meeting.setObservations(api_meeting["observations"])
            transaction.commit()
            logger.info("{} - {}/{} imported - id : {}".format(meeting_type, i + 1, total, api_meeting["id"]))
            self.import_items(api_meeting, meeting_object=meeting)

            transitions(meeting, ("close",))
            logger.info("{} - {}/{} closed - id : {}".format(meeting_type, i + 1, total, api_meeting["id"]))

    def import_items(self, api_meeting, meeting_object):
        meetingitem_ids = api_meeting["meetingitem_ids"]
        total = len(meetingitem_ids)
        api_meetingitems = [self.api.get_meetingitem(meetingitem_id) for meetingitem_id in meetingitem_ids]

        if self.meetingconfig_id == "meeting-config-college":
            item_type = "MeetingItemCollege"
        else:
            item_type = "MeetingItemCouncil"

        for i, api_meetingitem in enumerate(api_meetingitems):
            creator_id = api_meetingitem["creator"]
            self._create_user_if_not_exists(creator_id)
            self._create_organization_if_not_exists(api_meetingitem["proposing_group_id"])
            self._create_category_if_not_exists(api_meetingitem["category_id"])

            member_folder = self._get_member_folder(creator_id)

            if not hasattr(member_folder, api_meetingitem["id"]):
                member_folder.invokeFactory(
                    type_name=item_type,
                    id=api_meetingitem["id"],
                    title=api_meetingitem["title"],
                    date=api_meeting["created_at"],
                )

            item = getattr(member_folder, api_meetingitem["id"])  # type: MeetingItem
            item.setCreationDate(api_meetingitem["created_at"])
            item.setProposingGroup(org_id_to_uid(api_meetingitem["proposing_group_id"]))
            item.setCategory(api_meetingitem["category_id"])
            item.setDescription(api_meetingitem["description"])
            item.setDecision(api_meetingitem["decision"])
            item.setObservations(api_meetingitem["observations"])
            item.setCreators(creator_id)
            item.setPreferredMeeting(meeting_object.UID())
            item.setBudgetRelated(api_meetingitem["budget_related"])
            item.setBudgetInfos(api_meetingitem["budget_infos"])
            # Not sure why it is necessary
            # but it's very important to present the item in the correct meeting...
            api.portal.get().REQUEST["PUBLISHED"] = meeting_object

            transitions(item, ("propose", "validate", "present"))

            logger.info("{} - {}/{} imported - id : {}".format(item_type, i + 1, total, api_meetingitem["id"]))

        transitions(meeting_object, ("freeze", "decide"))

        for i, api_meetingitem in enumerate(api_meetingitems):
            creator_id = api_meetingitem["creator"]
            member_folder = self._get_member_folder(creator_id)
            item = getattr(member_folder, api_meetingitem["id"])

            transitions(item, ("accept",))  # TODO set correct state
            item.setModificationDate(api_meetingitem["modified_at"])

            logger.info("{} - {}/{} decided - id : {}".format(item_type, i + 1, total, api_meetingitem["id"]))

    def _create_category_if_not_exists(self, category_id):
        pm = api.portal.get_tool("portal_plonemeeting")
        meeting_config = getattr(pm, self.meetingconfig_id)
        category_folder = meeting_config.categories
        if category_id in category_folder.objectIds():
            return

        api_category = self.api.get_category(category_id)

        title = api_category["title"]
        cat_descriptor = CategoryDescriptor(category_id, title=title)

        cat = api.content.create(container=category_folder, type="meetingcategory", **cat_descriptor.getData())
        cat.reindexObject()

    def _create_user_if_not_exists(self, user_id):
        acl = api.portal.get_tool("acl_users")

        if user_id in [user["userid"] for user in acl.searchUsers()]:
            # Nothing to do, user already exists
            return

        # Create user in portal_membership
        portal_membership = api.portal.get_tool("portal_membership")
        api_user = self.api.get_user(user_id)
        portal_membership.addMember(user_id, "Binche-2020", ("Member",), [])
        member = portal_membership.getMemberById(user_id)
        properties = {"fullname": api_user["fullname"], "email": api_user["email"]}
        member.setMemberProperties(properties)

        # Initialize user's home folder
        portal_membership.createMemberArea(member_id=user_id)
        pm_tool = api.portal.get_tool("portal_plonemeeting")
        pm_tool.getPloneMeetingFolder("meeting-config-college", user_id)
        pm_tool.getPloneMeetingFolder("meeting-config-council", user_id)

        logger.info("Importer - User {} created".format(user_id))

    def _create_organization_if_not_exists(self, org_id):
        own_org = get_own_organization()

        if org_id in own_org.objectIds():
            # Nothing to do, organization already exists
            return

        # Create organization
        api_org = self.api.get_organization(org_id)
        org = api.content.create(container=own_org, type="organization", **api_org)

        # Create Plone Groups
        org_uid = org.UID()
        select_organization(org_uid)

    def _get_member_folder(self, user_id):
        portal = api.portal.get()
        member_folder = portal.Members[user_id].mymeetings.get(self.meetingconfig_id)
        return member_folder


class IExternalAPI:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_meeting_ids(self):
        raise NotImplementedError

    @abstractmethod
    def get_meeting(self, meeting_id):
        raise NotImplementedError

    @abstractmethod
    def get_meetingitem(self, meetingitem_id):
        raise NotImplementedError

    @abstractmethod
    def get_category(self, category_id):
        raise NotImplementedError

    @abstractmethod
    def get_user(self, user_id):
        raise NotImplementedError


class HubSessionsAPI(IExternalAPI):
    def __init__(self, base_url, user, user_password):
        self.base_url = base_url
        self.user = user
        self.user_password = user_password

        self._pm_userid_hs_userid_mapping = self._get_pm_userid_hs_userid_mapping()
        self._pm_categoryid_hs_classifierid_mapping = self._get_pm_categoryid_hs_classifierid_mapping()

    def get_meeting_ids(self):
        meetings_xml = self._get_xml_content(
            self.base_url + "/config?do=searchAll&className=HubSessions_Meeting_Meeting&sortBy=date"
        )
        meetings_ids = [meeting_url.text.split("/")[-2] for meeting_url in meetings_xml.xmlpythondata]
        meetings_ids.reverse()
        return meetings_ids

    def get_organization(self, org_id):
        xml = self._get_xml_content("{}/config/{}/xml".format(self.base_url, org_id)).hsgroup
        group = {"id": xml["id"], "title": xml.title.text, "acronym": xml.acronym.text}
        return group

    def get_user(self, user_id):
        if user_id not in self._pm_categoryid_hs_classifierid_mapping.keys():
            return {  # User has been deleted in HubSessions and we cannot find him.
                "id": user_id,
                "fullname": user_id,
                "email": "noreply@imio.be"
            }

        url = "{}/config/{}/xml".format(self.base_url, self._pm_userid_hs_userid_mapping[user_id])
        xml = self._get_xml_content(url).hsuser
        user = {
            "id": xml.login.text,
            "fullname": xml.title.text,
            "email": xml.email.text,
        }
        return user

    def get_meeting(self, meeting_id):
        xml = self._get_xml_content(self.base_url + "/data/{}/xml".format(meeting_id)).meeting
        meeting = {
            "id": xml["id"],
            "creator": xml.creator.text,
            "created_at": xml.created.text,
            "date": xml.date.text,
            "assembly": self._get_assembly(xml),
            "assembly_excused": self._get_assembly(xml, status="excused"),
            "assembly_absents": self._get_assembly(xml, status="absent"),
            "signatures": self._get_signatures(xml),
            "observations": xml.observations.text,
            "meetingitem_ids": [item_url.text.split("/")[-2] for item_url in xml.items],
            "annexes": [annexe.text for annexe in xml.annexes],
        }

        return meeting

    def get_meetingitem(self, meetingitem_id):
        xml = self._get_xml_content(self.base_url + "/data/{}/xml".format(meetingitem_id)).item
        item = {
            "id": xml["id"],
            "creator": xml.creator.text,
            "created_at": xml.created.text,
            "modified_at": xml.modified.text,
            "title": xml.title.text,
            "proposing_group_id": normalize(xml.proposinggroup.text),
            "category_id": normalize(xml.classifier.text),
            "to_discuss": strtobool(xml.todiscuss.text),
            "budget_related": strtobool(xml.budgetrelated.text),
            "budget_infos": self._get_budget_infos(xml),
            "late": strtobool(xml.late.text),
            "description": xml.description.text,
            "detailed_description": xml.detaileddescription.text,
            "observations": self._get_item_observations(xml),
            "decision": xml.decision.text,
        }

        return item

    def get_advice(self, item_id, advice_id):
        xml = self._get_xml_content(self.base_url + "/data/{}/{}/xml".format(item_id, advice_id)).advice
        advice = {
            "id": xml["id"],
            "creator": xml.creator.text,
            "created_at": xml.created.text,
            "modified_at": xml.modified.text,
            "type": xml.advicetype.text,
            "comment": xml.comment.text,
        }
        return advice

    def get_category(self, category_id):
        url = "{}/config/{}/xml".format(self.base_url, self._pm_categoryid_hs_classifierid_mapping[category_id])
        xml = self._get_xml_content(url).category
        category = {
            "id": normalize(xml.categoryid.text),
            "title": xml.title.text,
            "description": xml.description.text,
        }
        return category

    def _get_request(self, url):
        """ A generic GET request with basic http authentication """
        return requests.get(url, auth=(self.user, self.user_password))

    def _get_xml_content(self, url):
        """ Get the xml content of the url """
        request = self._get_request(url)
        soup = BeautifulSoup(request.content, "lxml")
        return soup.html.body

    def _get_assembly(self, meeting_xml, status="attendee"):
        participant_urls = [e.text for e in meeting_xml.participants]
        assembly = u""
        LINE_FORMAT = u"{}, {} \n"
        for participant_url in participant_urls:
            participant = self._get_xml_content(participant_url).participant
            if participant.status.text == status:
                assembly += LINE_FORMAT.format(
                    self.get_user(participant.tieduser.text)["fullname"], participant.duty.text
                )
        return assembly[:-1]  # -1 so we don't have an useless newline

    def _get_signatures(self, meeting_xml):
        participant_urls = [e.text for e in meeting_xml.participants]
        signatures = u""
        for participant_url in participant_urls:
            participant = self._get_xml_content(participant_url).participant
            if participant.signer.text == "True":
                signatures += self.get_user(participant.tieduser.text)["fullname"] + "\n"
                signatures += participant.duty.text + "\n"
        return signatures[:-1]  # -1 so we don't have an useless newline

    def _get_budget_infos(self, meetingitem_xml):
        if strtobool(meetingitem_xml.budgetrelated.text):
            return meetingitem_xml.budgetinfos.text
        return None

    def _get_item_observations(self, meetingitem_xml):
        def _translate(text):
            return translate(text, domain="PloneMeeting", context=api.portal.get().REQUEST)

        def _pretty_date(date_str):
            date_str = date_str[:15]  # We only care about the first 16 chars
            datetime_object = datetime.strptime(date_str, "%Y/%m/%d %H:%M")
            return datetime_object.strftime("%d/%m/%Y à %Hh%M").decode("utf-8")

        if not meetingitem_xml.advices:
            return meetingitem_xml.observations.text

        ADVICE_FORMAT = u"""
        <p>{creator} - <strong>avis: {type}</strong> - rendu le : {created_at}</p>
        """
        advices = [
            self.get_advice(meetingitem_xml["id"], advice_url.text.split("/")[-2])
            for advice_url in meetingitem_xml.advices
        ]
        result = ""
        if advices:
            result += "<p>Avis rendus sur le point: </p>"
            for advice in advices:
                result += ADVICE_FORMAT.format(
                    creator=self.get_user(advice["creator"])["fullname"],
                    type=_translate(advice["type"]).lower(),
                    created_at=_pretty_date(advice["created_at"]),
                )
                if advice.get("comment"):
                    result += "<hr/>" + advice["comment"]
        return result + meetingitem_xml.observations.text

    def _get_user_urls(self):
        users_xml = self._get_xml_content(self.base_url + "/config/xml").hsconfig.users
        users = [user.text for user in users_xml]
        return users

    def _get_pm_userid_hs_userid_mapping(self):
        """
        In HubSession we access an user by his HS's specific user_id so we need a mapping to get
        a user by his PM's user id. We will use the login value as the PM user id.
        """
        mapping = {}
        users = self._get_user_urls()
        for user_url in users:
            user = self._get_xml_content(user_url).hsuser
            mapping[user.login.text] = user["id"]
        return mapping

    def _get_pm_categoryid_hs_classifierid_mapping(self):
        """
        In HubSession we access a category by his HS's specific category_id so we need a mapping to get
        a category by his PM's category id. We will use the categoryId value as the PM category id.
        """
        mapping = {}
        categories_urls_xml = self._get_xml_content(self.base_url + "/config/xml").hsconfig.classifiers
        categories_urls = [category.text for category in categories_urls_xml]
        for category_url in categories_urls:
            category = self._get_xml_content(category_url).category
            mapping[normalize(category.categoryid.text)] = category["id"]
        return mapping


class SilentLogging:
    """
    Reduce logs verbosity
    Use it like this :
    with SilentLogging(('loggerA', 'loggerB')):
        do_stuff()
    """

    def __init__(self, loggers, verbose=False):
        self.loggers = loggers
        self.verbose = verbose

    def __enter__(self):
        if self.verbose:
            return
        for logger_name in self.loggers:
            logger_name = logging.getLogger(logger_name)
            logger_name.disabled = True

    def __exit__(self, type, value, traceback):
        for logger_name in self.loggers:
            logger_name = logging.getLogger(logger_name)
            logger_name.disabled = False
