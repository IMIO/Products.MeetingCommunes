# coding=utf-8
import logging
import requests
from bs4 import BeautifulSoup

from collective.contact.plonegroup.utils import get_own_organization, select_organization
from imio.helpers.content import transitions
from plone import api
import transaction

from Products.PloneMeeting import logger
from Products.PloneMeeting.utils import org_id_to_uid


# MoSCoW -- Import HubSessions
# --------------------------------------------------------------------------------------------------
# Must
# --------------------------------------------------------------------------------------------------
# - Importer les séances (assemblée, signataires, ...) => OK
# - Importer les points =>  En cours, presque terminé
# - Importer les groupes proposants => OK
# - Importer les catégories
#
# --------------------------------------------------------------------------------------------------
# Should
# --------------------------------------------------------------------------------------------------
# - Abstraire l'API d'HubSession pour que l'Importer puisse gérer d'autres sources de données
# au travers d'une interface
# - Ajouter les docstrings
# - Vérifier pourquoi il y a parfois des
# 'WARNING Transience Transient object container session_data max subobjects reached' du côté de HS
# => OK, pas grave
# - S'assurer que l'import est idempotent : CàD qu'on peut le faire tourner plusieurs fois d'affilés
# sans erreurs/crashs
# --------------------------------------------------------------------------------------------------
# Could:
# --------------------------------------------------------------------------------------------------
#
#
# --------------------------------------------------------------------------------------------------
# Won't:
# --------------------------------------------------------------------------------------------------
# - Importer les participants dans les contacts
#


def import_data(
    base_url="http://localhost:8080",
    user="admin",
    user_password="admin",
    meetingconfig_id="meeting-config-college",
    verbose=False,
):
    with SilentLogging(("collective.fingerpointing", "imio.helpers.content"), verbose):
        importer = HubSessionsXMLImporter(base_url, user, user_password, meetingconfig_id)
        importer.run()
        logger.info("Import finished - " + meetingconfig_id)
        return 0


class HubSessionsXMLImporter:
    def __init__(self, base_url, user, user_password, meetingconfig_id):
        self.api = HubSessionsAPI(base_url, user, user_password)
        self.meetingconfig_id = meetingconfig_id

    def run(self):
        self.import_meetings()

    def import_meetings(self):
        meetings_url = self.api.get_meeting_urls()
        total = len(meetings_url)
        for i, meeting_url in enumerate(meetings_url):
            api_meeting = self.api.get_meeting(meeting_url)
            creator_id = api_meeting["creator"]
            self._create_user_if_not_exists(creator_id)

            member_folder = self._get_member_folder(creator_id)

            if self.meetingconfig_id == "meeting-config-college":
                meeting_type = "MeetingCollege"
            else:
                meeting_type = "MeetingCouncil"

            if not hasattr(member_folder, api_meeting["id"]):
                member_folder.invokeFactory(
                    type_name=meeting_type, id=api_meeting["id"], date=api_meeting["date"]
                )
                meeting = getattr(member_folder, api_meeting["id"])
                meeting.setCreators(creator_id)
                meeting.at_post_create_script()
            else:
                meeting = getattr(member_folder, api_meeting["id"])

            meeting.setSignatures(api_meeting["signatures"])
            meeting.setAssembly(api_meeting["assembly"])
            meeting.setAssemblyExcused(api_meeting["assembly_excused"])
            meeting.setAssemblyAbsents(api_meeting["assembly_absents"])
            meeting.setObservations(api_meeting["observations"])
            transaction.commit()
            logger.info(
                "{} - {}/{} imported - id : {}".format(
                    meeting_type, i + 1, total, api_meeting["id"]
                )
            )
            self.import_items(api_meeting, meeting_object=meeting)

            transitions(meeting, ("close",))
            logger.info(
                "{} - {}/{} closed - id : {}".format(meeting_type, i + 1, total, api_meeting["id"])
            )

    def import_items(self, api_meeting, meeting_object):
        item_urls = api_meeting["items"]
        total = len(item_urls)
        api_items = [self.api.get_item(item_url) for item_url in item_urls]

        if self.meetingconfig_id == "meeting-config-college":
            item_type = "MeetingItemCollege"
        else:
            item_type = "MeetingItemCouncil"

        for i, api_item in enumerate(api_items):
            creator_id = api_item["creator"]
            self._create_user_if_not_exists(creator_id)
            self._create_organization_if_not_exists(api_item["proposing_group_id"])

            member_folder = self._get_member_folder(creator_id)

            if not hasattr(member_folder, api_item["id"]):
                member_folder.invokeFactory(
                    type_name=item_type,
                    id=api_item["id"],
                    title=api_item["title"],
                    date=api_meeting["created_at"],
                )
            item = getattr(member_folder, api_item["id"])
            item.setProposingGroup(org_id_to_uid(api_item["proposing_group_id"]))
            # TODO : set more fields
            item.setDescription(api_item["description"])
            item.setDecision(api_item["decision"])
            item.setCreators(creator_id)
            item.setPreferredMeeting(meeting_object.UID())

            # Not sure why it is necessary
            # but it's very important to present the item in the correct meeting...
            api.portal.get().REQUEST["PUBLISHED"] = meeting_object

            transitions(item, ("propose", "validate", "present"))

            logger.info(
                "{} - {}/{} imported - id : {}".format(item_type, i + 1, total, api_item["id"])
            )

        transitions(meeting_object, ("freeze", "decide"))

        for i, api_item in enumerate(api_items):
            creator_id = api_item["creator"]
            member_folder = self._get_member_folder(creator_id)
            item = getattr(member_folder, api_item["id"])
            transitions(item, ("accept",))  # TODO set correct state
            logger.info(
                "{} - {}/{} decided - id : {}".format(item_type, i + 1, total, api_item["id"])
            )

    def _create_category_if_not_exists(self):
        pass

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


class HubSessionsAPI:
    def __init__(self, base_url, user, user_password):
        self.base_url = base_url
        self.user = user
        self.user_password = user_password

        self._pmuserid_hsuserid_mapping = self._get_pmuserid_hsuserid_mapping()

    def get_meeting_urls(self):
        meetings_xml = self._get_xml_content(
            self.base_url + "/config?do=searchAll&className=HubSessions_Meeting_Meeting&sortBy=date"
        )
        meetings = [e.text for e in meetings_xml.xmlpythondata]
        meetings.reverse()
        return meetings

    def get_users(self):
        users_xml = self._get_xml_content(self.base_url + "/config/xml").hsconfig.users
        users = [user.text for user in users_xml]
        return users

    def get_organization(self, org_id):
        xml = self._get_xml_content("{}/config/{}/xml".format(self.base_url, org_id)).hsgroup
        group = {"id": xml["id"], "title": xml.title.text, "acronym": xml.acronym.text}
        return group

    def get_user(self, user_id):
        url = "{}/config/{}/xml".format(self.base_url, self._pmuserid_hsuserid_mapping[user_id])
        xml = self._get_xml_content(url).hsuser
        user = {
            "id": xml.login.text,
            "fullname": xml.title.text,
            "email": xml.email.text,
        }
        return user

    def get_meeting(self, url):
        xml = self._get_xml_content(url).meeting
        meeting = {
            "id": xml["id"],
            "creator": xml.creator.text,
            "created_at": xml.created.text,
            "date": xml.date.text,
            "assembly": self._get_assembly(url),
            "assembly_excused": self._get_assembly(url, status="excused"),
            "assembly_absents": self._get_assembly(url, status="absent"),
            "signatures": self._get_signatures(url),
            "observations": xml.observations.text,
            "items": [item.text for item in xml.items],
            "annexes": [annexe.text for annexe in xml.annexes],
        }

        return meeting

    def get_item(self, url):
        xml = self._get_xml_content(url).item
        item = {
            "id": xml["id"],
            "creator": xml.creator.text,
            "created_at": xml.created.text,
            "title": xml.title.text,
            "proposing_group_id": xml.proposinggroup.text,
            "category": xml.classifier.text,
            "to_discuss": bool(xml.todiscuss.text),
            "description": xml.description.text,
            "detailed_description": xml.detaileddescription.text,
            "observations": xml.observations.text,
            "decision": xml.decision.text,
        }
        return item

    def _get_request(self, url):
        """ A generic GET request with basic http authentication """
        return requests.get(url, auth=(self.user, self.user_password))

    def _get_xml_content(self, url):
        """ Get the xml content of the url """
        request = self._get_request(url)
        soup = BeautifulSoup(request.content, "lxml")
        return soup.html.body

    def _get_assembly(self, url, status="attendee"):
        participant_urls = [e.text for e in self._get_xml_content(url).meeting.participants]
        assembly = u""
        LINE_FORMAT = u"{}, {} \n"
        for participant_url in participant_urls:
            participant = self._get_xml_content(participant_url).participant
            if participant.status.text == status:
                assembly += LINE_FORMAT.format(
                    self.get_user(participant.tieduser.text)["fullname"], participant.duty.text
                )
        return assembly[:-1]  # -1 so we don't have an useless newline

    def _get_signatures(self, url):
        participant_urls = [e.text for e in self._get_xml_content(url).meeting.participants]
        signatures = u""
        for participant_url in participant_urls:
            participant = self._get_xml_content(participant_url).participant
            if participant.signer.text == "True":
                signatures += self.get_user(participant.tieduser.text)["fullname"] + "\n"
                signatures += participant.duty.text + "\n"
        return signatures[:-1]  # -1 so we don't have an useless newline

    def _get_pmuserid_hsuserid_mapping(self):
        """
        In HubSession we access an user by his HS's specific user_id so we need a mapping to get
        a user by his PM's user id. We will use the login value as the PM user id.
        """
        mapping = {}
        users = self.get_users()
        for user_url in users:
            user = self._get_xml_content(user_url).hsuser
            mapping[user.login.text] = user["id"]
        return mapping


class SilentLogging:
    """
    Reduce logs verbosity
    Use it like this :
    with SilentLogging((loggerA, loggerB)):
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
