from AccessControl import Unauthorized
from collective.contact.plonegroup.utils import get_organizations
from collective.contact.plonegroup.utils import get_own_organization
from plone import api
from Products.CMFCore.exceptions import BadRequest
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.utils import safe_unicode
from Products.PloneMeeting.utils import org_id_to_uid

import csv


def export_orgs(self):
    """
      Export the existing organizations informations as a dictionnary
    """
    member = api.user.get_current()
    if not member.has_role('Manager'):
        raise Unauthorized('You must be a Manager to access this script !')

    if not hasattr(self, 'portal_plonemeeting'):
        return "PloneMeeting must be installed to run this script !"

    data = {}
    for org in get_organizations(only_selected=False):
        data[org.getId()] = (org.Title(), org.Description(), org.get_acronym())
    return data


def import_orgs(self, data=None):
    """
      Import the organizations from the 'data' dictionnaty received as parameter
    """
    member = api.user.get_current()
    if not member.has_role('Manager'):
        raise Unauthorized('You must be a Manager to access this script !')

    if not dict:
        return "This script needs a 'dict' parameter"
    if not hasattr(self, 'portal_plonemeeting'):
        return "PloneMeeting must be installed to run this script !"

    own_org = get_own_organization()
    out = []
    data = eval(data)
    for elt_id, elt_infos in data.items():
        if elt_id not in own_org.objectIds():
            api.content.create(container=own_org,
                               type="organization",
                               id=elt_id,
                               title=elt_infos[0],
                               description=elt_infos[1],
                               acronym=elt_infos[2])
            out.append("Organization %s added" % elt_id)
        else:
            out.append("Organization %s already exists" % elt_id)
    return '\n'.join(out)


def import_meetingsUsersAndRoles_from_csv(self, fname=None):
    """
      Import the users and attribute roles from the 'csv file' (fname received as parameter)
    """

    member = api.user.get_current()
    if not member.has_role('Manager'):
        raise Unauthorized('You must be a Manager to access this script !')

    if not fname:
        return "This script needs a 'fname' parameter"

    if not hasattr(self, 'portal_plonemeeting'):
        return "PloneMeeting must be installed to run this script !"

    try:
        file = open(fname, "rb")
        reader = csv.DictReader(file)
    except Exception, msg:
        file.close()
        return "Error with file : %s" % msg.value

    out = []

    acl = self.acl_users
    pms = api.portal.get_tool('portal_membership')
    pgr = api.portal.get_tool('portal_groups')
    registration = api.portal.get_tool('portal_registration')
    for row in reader:
        row_id = normalizeString(row['username'], self)
        # add users if not exist
        if row_id not in [ud['userid'] for ud in acl.searchUsers()]:
            pms.addMember(row_id, row['password'], ('Member',), [])
            member = pms.getMemberById(row_id)
            properties = {'fullname': row['fullname'], 'email': row['email']}
            failMessage = registration.testPropertiesValidity(properties, member)
            if failMessage is not None:
                raise BadRequest(failMessage)
            member.setMemberProperties(properties)
            out.append("User '%s' is added" % row_id)
        else:
            out.append("User %s already exists" % row_id)
        # attribute roles
        group_title = safe_unicode(row['grouptitle'])
        org_id = normalizeString(group_title, self)
        org_uid = org_id_to_uid(org_id)
        plone_groups = []
        if row['observers']:
            plone_groups.append(org_uid + '_observers')
        if row['creators']:
            plone_groups.append(org_uid + '_creators')
        if row['reviewers']:
            plone_groups.append(org_uid + '_reviewers')
        if row['advisers']:
            plone_groups.append(org_uid + '_advisers')
        for plone_group_id in plone_groups:
            pgr.addPrincipalToGroup(row_id, plone_group_id)
            out.append("    -> Added in group '%s'" % plone_group_id)

    file.close()

    return '\n'.join(out)


def import_meetingsCategories_from_csv(self, meeting_config='', isClassifier=False, fname=None):
    """
      Import the MeetingCategories from the 'csv file' (meeting_config, isClassifier and fname received as parameter)
    """
    member = self.portal_membership.getAuthenticatedMember()
    if not member.has_role('Manager'):
        raise Unauthorized('You must be a Manager to access this script !')

    if not fname or not meeting_config:
        return "This script needs a 'meeting_config' and 'fname' parameters"
    if not hasattr(self, 'portal_plonemeeting'):
        return "PloneMeeting must be installed to run this script !"

    import csv
    try:
        file = open(fname, "rb")
        reader = csv.DictReader(file)
    except Exception, msg:
        file.close()
        return "Error with file : %s" % msg.value

    out = []

    pm = self.portal_plonemeeting
    from Products.CMFPlone.utils import safe_unicode
    from Products.CMFPlone.utils import normalizeString
    from Products.MeetingCommunes.config import PROJECTNAME
    from Products.PloneMeeting.exportimport.content import ToolInitializer
    from Products.PloneMeeting.profiles import CategoryDescriptor

    meetingConfig = getattr(pm, meeting_config)
    if isClassifier:
        catFolder = meetingConfig.classifiers
    else:
        catFolder = meetingConfig.categories

    for row in reader:
        rowid = safe_unicode(row['title'])
        row_id = normalizeString(rowid, self)
        if row_id == '':
            continue
        if not hasattr(catFolder, row_id):
            try:
                catDescr = CategoryDescriptor(row_id, title=row['title'])
                context = self.portal_setup._getImportContext('Products.MeetingCommunes:zcity')
                TI = ToolInitializer(context, PROJECTNAME)
                TI.addCategory(cfg=meetingConfig, descr=catDescr, classifier=isClassifier)
                cat = getattr(catFolder, row_id)
                if cat:
                    cat.setCategoryId(row['categoryId'])
                out.append("Category (or Classifier) %s added" % row_id)
            except Exception, message:
                out.append('error with %s - %s : %s' % (row_id, row['title'], message))
        else:
            out.append("Category (or Classifier) %s already exists" % row_id)

    file.close()

    return '\n'.join(out)
