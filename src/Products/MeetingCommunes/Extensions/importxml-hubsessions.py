# coding=utf-8
import time

import requests
from bs4 import BeautifulSoup
from plone import api
import transaction


# MoSCoW -- Import HubSessions
# --------------------------------------------------------------------------------------------------
# Must
# --------------------------------------------------------------------------------------------------
# - Importer les informations des séances (assemblée, signataires, ...)
# - Importer les points
# - Importer les groupes proposants
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
):
    importer = HubSessionsXMLImporter(base_url, user, user_password, meetingconfig_id)
    importer.run()


class HubSessionsXMLImporter:
    def __init__(self, base_url, user, user_password, meetingconfig_id):
        self.hs_api = HubSessionsAPI(base_url, user, user_password)
        self.meetingconfig_id = meetingconfig_id

    def run(self):
        self.import_meetings()
        return 0

    def import_meetings(self):
        for meeting_url in self.hs_api.get_meetings_urls():
            xml_meeting = self.hs_api.get_meeting(meeting_url)
            creator_id = xml_meeting.creator.text
            self._create_user_if_not_exists(creator_id)

            member_folder = (
                api.portal.get().Members[creator_id].mymeetings.get(self.meetingconfig_id)
            )

            if self.meetingconfig_id == "meeting-config-college":
                meeting_type = "MeetingCollege"
            else:
                meeting_type = "MeetingCouncil"

            meetingid = member_folder.invokeFactory(
                type_name=meeting_type, id=xml_meeting["id"], date=xml_meeting.date.text
            )
            meeting = getattr(member_folder, meetingid)
            meeting.at_post_create_script()
            time.sleep(1.5)
            transaction.commit()

    def import_items(self):
        pass

    def import_category(self):
        pass

    def _create_user_if_not_exists(self, user_id):
        acl = api.portal.get_tool("acl_users")

        if user_id in [ud["userid"] for ud in acl.searchUsers()]:
            return

        portal_membership = api.portal.get_tool("portal_membership")
        user = self.hs_api.get_user(user_id)
        portal_membership.addMember(user_id, "Binche-2020", ("Member",), [])
        member = portal_membership.getMemberById(user_id)
        properties = {"fullname": user.title.text, "email": user.email.text}
        member.setMemberProperties(properties)

        portal_membership.createMemberArea(member_id=user_id)
        self.pm_tool.getPloneMeetingFolder("meeting-config-college", user_id)
        self.pm_tool.getPloneMeetingFolder("meeting-config-council", user_id)


class HubSessionsAPI:
    def __init__(self, base_url, user, user_password):
        self.base_url = base_url
        self.user = user
        self.user_password = user_password

        self._pmuserid_hsuserid_mapping = self._get_pmuserid_hsuserid_mapping()

    def get_meetings_urls(self):
        meetings_xml = self._get_xml_content(
            self.base_url + "/config?do=searchAll&className=HubSessions_Meeting_Meeting&sortBy=date"
        )
        meetings = [e.text for e in meetings_xml.xmlpythondata]
        return meetings

    def get_users(self):
        users_xml = self._get_xml_content(self.base_url + "/config/xml").hsconfig.users
        users = [user.text for user in users_xml]
        return users

    def get_user(self, user_id):
        url = "{}/config/{}/xml".format(self.base_url, self._pmuserid_hsuserid_mapping[user_id])
        user = self._get_xml_content(url).hsuser
        return user

    def get_meeting(self, url):
        meeting = self._get_xml_content(url).meeting
        return meeting

    def get_item(self, url):
        item = self._get_xml_content(url).item
        return item

    def _get_request(self, url):
        """ A generic GET request with basic http authentication """
        return requests.get(url, auth=(self.user, self.user_password),)

    def _get_xml_content(self, url):
        """ Get the xml content of the url """
        request = self._get_request(url)
        soup = BeautifulSoup(request.content)
        return soup.html.body

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
