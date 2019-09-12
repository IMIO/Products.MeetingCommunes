#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from backports import csv
from collective.contact.plonegroup.utils import get_organizations
from DateTime import DateTime
from datetime import datetime
from plone.app.querystring import queryparser
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.utils import safe_unicode
from Products.PloneMeeting import logger

import io
import transaction


#  pip install backports.csv

""" Reprise des données ACROPOLE de chez Stesud depuis un export de CSV
A faire dans l'instance avant migration :
1. Créer un groupe Importation.
2. Créer un utilisateur csvimport créateur d'un quelconque service (nom complet : Importation Acropole) et se 
connecter avec.
3. Créer une catégorie 'Reprise Acropole' et la désactiver [SI LES CATEGORIES SONT UTILISEES].
4. Créer les types d'annexes suivants :
    1. deliberation
    2. advise
    3. pdf-link
5. Désactiver les points récurrents dans la config, sinon lors de la création des séances on va avoir des surprises :-)

A faire dans l'instance après migration :
6. A la fin de l'import, supprimer les droits de csvimport et réactiver les points récurrents et désactiver le groupe.
"""


def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%d-%m-%Y %H:%M:%S')


class CSVMeetingItem:
    # CSV columns :
    # item_id, creator, title, proposing_group, motivation, decision, secret, meeting_id, number, portal_type
    annexFileTypeDecision = 'annexeDecision'

    def __init__(self, external_id, creator, created_on, title, proposing_group, motivation, decision,
                 secret, meeting_id, number, portal_type):
        self.external_id = external_id
        self.creator_id = creator
        self.created_on = parse_datetime(created_on)
        self.title = safe_unicode(title)
        self.proposing_group = proposing_group
        self.motivation = motivation
        self.decision = decision
        self.secret = secret
        self.meeting_id = meeting_id
        self.number = number
        self.portal_type = portal_type


class CSVMeeting:
    # CSV columns : meeting_id, date, start_date, end_date, place, meeting_type, creator, created_on
    def __init__(self, meeting_id, date, start_date, end_date, place, portal_type, creator, created_on):
        self.meeting_id = meeting_id
        self.date = parse_datetime(date)
        self.start_date = parse_datetime(start_date)
        self.end_date = parse_datetime(end_date)
        self.place = place
        self.portal_type = portal_type
        self.creator = creator
        self.created_on = parse_datetime(created_on)

        self.items = []


class ImportCSV:

    def __init__(self, portal, f_group_mapping, f_items, f_meetings, default_group, default_category):
        self.grp_id_mapping = {}
        self.portal = portal
        self.f_group_mapping = f_group_mapping
        self.f_items = f_items
        self.f_meetings = f_meetings
        self.default_group = default_group
        self.default_category = default_category
        self.errors = {'io': [], 'item': [], 'meeting': [], 'item_without_annex': []}
        self.item_counter = 0
        self.meeting_counter = 0
        self.groups = {}
        self._deactivated_recurring_items = []

    def object_already_exists(self, obj_id, portal_type):
        catalog_query = [{
                                 'i': 'portal_type',
                                 'o': 'plone.app.querystring.operation.selection.is',
                                 'v': portal_type
                         },
                         {
                                 'i': 'id',
                                 'o': 'plone.app.querystring.operation.selection.is',
                                 'v': obj_id
                         }, ]
        query = queryparser.parseFormquery(self.portal, catalog_query)
        res = self.portal.portal_catalog(**query)
        if res:
            logger.info('Already created {object}'.format(object=obj_id))
        return res

    @staticmethod
    def get_meeting_portal_type(obj_type):
        if 'col' in obj_type.lower():
            return 'MeetingCollege'
        elif 'cons' in obj_type.lower():
            return 'MeetingCouncil'

    @staticmethod
    def get_item_portal_type(obj_type):
        if 'col' in obj_type.lower():
            return 'MeetingItemCollege'
        elif 'cons' in obj_type.lower():
            return 'MeetingItemCouncil'

    def load_items(self, delib_file,  meetings):
        logger.info("Load {0}".format(delib_file))
        with io.open(delib_file, 'r', encoding='latin-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=u',')
            # ID	Titre	CreateurID	DateCreation	Categorie	DateSeance	Annexe
            for row in reader:
                try:
                    for value in row:
                        if not value:
                            raise ValueError('Malformed row : {row}'.format(row=row))

                    meeting_id = row[8].strip()
                    if meeting_id not in meetings:
                        logger.info('Unknown meeting for item : {row}'.format(row=row))
                    else:
                        item = CSVMeetingItem(external_id=row[0],
                                              creator=row[1],
                                              created_on=row[2],
                                              title=row[3],
                                              proposing_group=row[4],
                                              motivation=row[5],
                                              decision=row[6],
                                              secret=row[7],
                                              meeting_id=row[8],
                                              number=row[9],
                                              portal_type=self.get_item_portal_type(row[10]))
                        meeting = meetings[meeting_id]
                        meeting.items.append(item)
                except ValueError as e:
                    self.errors['item'].append(e.message)
                    logger.info(e.message)

    def _check_meeting_data(self, csv_meeting):
        if not csv_meeting.items:
            message = 'Meeting of {date} has no item. Skipping...'.format(date=csv_meeting.date)
            logger.info(message)
            self.errors['meeting'].append(message)
            return False

        return True

    def insert_and_close_meeting(self, member_folder, csv_meeting):
        if not self._check_meeting_data(csv_meeting):
            return

        _id = 'meetingreprise.{id}'.format(id=csv_meeting.meeting_id)

        meeting = self.object_already_exists(_id, csv_meeting.portal_type)
        if meeting and meeting[0]:
            message = 'Skipping meeting {id} and it items because it already exists'.format(id=_id)
            logger.info(message)
            self.errors['meeting'].append(message)
            return

        meetingid = member_folder.invokeFactory(type_name=csv_meeting.portal_type, id=_id, date=csv_meeting.date)
        meeting = getattr(member_folder, meetingid)
        meeting.setSignatures("")
        meeting.setAssembly("")
        meeting.setDate(csv_meeting.date)
        meeting.setStartDate(csv_meeting.date)

        # meeting.at_post_create_script()
        meeting.processForm(values={'dummy': None})
        meeting.setCreationDate(csv_meeting.date)
        logger.info('Created meeting of {date}'.format(date=meeting.Title()))

        logger.info(
            'Adding {items} items to meeting of {date}'.format(items=len(csv_meeting.items), date=meeting.Title()))
        self.portal.REQUEST['PUBLISHED'] = meeting
        for csv_item in csv_meeting.items:
            self.insert_and_present_item(member_folder, csv_item)

        if meeting.getItems():
            meeting.portal_workflow.doActionFor(meeting, 'freeze')
            meeting.portal_workflow.doActionFor(meeting, 'decide')
            meeting.portal_workflow.doActionFor(meeting, 'close')

            for item in meeting.getItems():
                item.setModificationDate(csv_meeting.end_date)

            meeting.setModificationDate(csv_meeting.end_date)

        meeting.reindexObject()
        self.meeting_counter += 1
        transaction.commit()

    def get_matching_proposing_group(self, category):
        grp_id = category.strip() in self.groups and self.groups[category.strip()]
        return grp_id in self.grp_id_mapping and self.grp_id_mapping[grp_id].UID() or self.default_group

    def insert_and_present_item(self, member_folder, csv_item):
        itemid = member_folder.invokeFactory(type_name=csv_item.portal_type,
                                             id=csv_item.external_id,
                                             date=csv_item.created_on,
                                             title=csv_item.title)
        item = getattr(member_folder, itemid)
        item.setProposingGroup(self.get_matching_proposing_group(csv_item.category))
        item.setCategory(self.default_category)
        item.setCreators('csvimport')
        item.setDescription('<p>Créateur originel : {creator}</p>'.format(creator=csv_item.creator_id))
        # do not call item.at_post_create_script(). This would get only throuble with cancel quick edit in objects
        item.processForm(values={'dummy': None})
        item.setCreationDate(csv_item.created_on)

        try:
            self.portal.portal_workflow.doActionFor(item, 'propose')
        except WorkflowException:
            pass  # propose item is disabled
        try:
            self.portal.portal_workflow.doActionFor(item, 'prevalidate')
        except WorkflowException:
            pass  # pre validation isn't used
        self.portal.portal_workflow.doActionFor(item, 'validate')
        self.portal.portal_workflow.doActionFor(item, 'present')
        item.reindexObject()
        self.item_counter += 1

    def run(self):
        member = self.portal.portal_membership.getAuthenticatedMember()
        if not member.has_role('Manager'):
            return 'You must be a Manager to access this script !'

        # Load all csv into memory
        cfg_groups = get_organizations(only_selected=False)
        for group in cfg_groups:
            self.grp_id_mapping[group.id] = group

        logger.info("Load {0}".format(self.f_group_mapping))
        with io.open(self.f_group_mapping, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                grp_id = row[1].strip()
                if grp_id in self.grp_id_mapping:
                    self.groups[row[0].strip()] = grp_id
                else:
                    self.groups[row[0].strip()] = self.default_group

        meetings = self.load_meetings()

        self.load_items(self.f_items, meetings)
        # insert All
        logger.info('Insert Objects')
        self.disable_recurring_items('meeting-config-college')
        self.disable_recurring_items('meeting-config-council')

        previous_folder_id = 'meeting-config-college'
        member_folder = self.portal.Members.csvimport.mymeetings.get(previous_folder_id)
        for csv_meeting in meetings.values():
            if csv_meeting.portal_type == 'MeetingCollege':
                folder_id = 'meeting-config-college'
            elif csv_meeting.portal_type == 'MeetingCouncil':
                folder_id = 'meeting-config-council'
            else:
                raise NotImplementedError()

            if folder_id != previous_folder_id:
                member_folder = self.portal.Members.csvimport.mymeetings.get(folder_id)
                previous_folder_id = folder_id

            self.insert_and_close_meeting(member_folder, csv_meeting)

        self.re_enable_recurring_items('meeting-config-college')
        self.re_enable_recurring_items('meeting-config-council')

        return self.meeting_counter, self.item_counter, self.errors

    def disable_recurring_items(self, _meeting_config_id):
        cfg = self.portal.portal_plonemeeting.get(_meeting_config_id)
        self._deactivated_recurring_items = []
        for item in cfg.getRecurringItems():
            self.portal.portal_workflow.doActionFor(item, 'deactivate')
            self._deactivated_recurring_items.append(item.UID())

    def re_enable_recurring_items(self, _meeting_config_id):
        cfg = self.portal.portal_plonemeeting.get(_meeting_config_id)
        for item in cfg.getRecurringItems(False):
            if item.UID() in self._deactivated_recurring_items:
                self.portal.portal_workflow.doActionFor(item, 'activate')

    def load_meetings(self):
        meetings = {}
        logger.info("Load {0}".format(self.f_meetings))
        with io.open(self.f_meetings, 'r', encoding='latin-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=u';')
            # TypeSeance	DateSeance	OJ	PV
            for row in reader:
                # meeting_id, date, start_date, end_date, place, portal_type, creator, created_on
                meeting = CSVMeeting(meeting_id=row[0],
                                     date=row[1],
                                     start_date=row[2],
                                     end_date=row[3],
                                     place=row[4],
                                     portal_type=self.get_meeting_portal_type(row[5]),
                                     creator=row[6],
                                     created_on=row[7])

                if meeting.meeting_id in meetings:
                    raise KeyError("2 Meetings have the same id {0}".format(meeting.meeting_id))
                else:
                    meetings[meeting.meeting_id] = meeting
        return meetings


def import_data_from_csv(self,
                         f_group_mapping,
                         f_items_college,
                         f_items_council,
                         f_meetings,
                         annex_dir_path):
    start_date = datetime.now()
    import_csv = ImportCSV(self,
                           f_group_mapping,
                           f_items_college,
                           f_items_council,
                           f_meetings,
                           annex_dir_path)
    meeting_counter, item_counter, errors = import_csv.run()
    logger.info('Inserted {meeting} meetings and {item} meeting items.'.format(meeting=meeting_counter,
                                                                               item=item_counter))
    logger.warning('{malforemed} meeting items were not created due to missing data in csv :\n{list}'.format(
            malforemed=len(errors['item']),
            list=u'\n\t '.join(errors['item'])))

    logger.warning('{ioerr} errors occured while adding annexes :\n{list}'.format(ioerr=len(errors['io']),
                                                                                  list=u'\n\t '.join(errors['io'])))

    logger.warning('{meeting} meeting items have no annex :\n{list}'.format(meeting=len(errors['meeting']),
                                                                            list=u'\n\t '.join(errors['meeting'])))

    logger.warning('{items} meeting where skipped :\n{list}'.format(items=len(errors['item_without_annex']),
                                                                    list=u'\n\t '.join(errors['item_without_annex'])))
    end_date = datetime.now()
    seconds = end_date - start_date
    seconds = seconds.seconds
    hours = seconds / 3600
    minutes = (seconds - hours * 3600) / 60
    logger.info('Import finished in {0} seconds ({1} h {2} m).'.format(seconds, hours, minutes))
