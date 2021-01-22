#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from backports import csv
from collective.contact.plonegroup.utils import get_organizations
from collective.iconifiedcategory.utils import calculate_category_id
from collective.iconifiedcategory.utils import get_config_root
from DateTime import DateTime
from datetime import datetime
from plone import namedfile
from plone.app.querystring import queryparser
from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.utils import safe_unicode
from Products.PloneMeeting import logger

import io
import os
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


class CSVMeetingItem:
    annexFileTypeDecision = 'annexeDecision'

    def __init__(self, external_id, creator, created_on, title, category, annex_path, portal_type):
        self.external_id = '{dir}-{id}'.format(dir=annex_path.split('\\')[-2],
                                               id=external_id)
        self.title = safe_unicode(title)
        self.creator_id = creator
        self.created_on = created_on
        self.category = category
        self.annex_path = safe_unicode(annex_path.replace('\\', '/')).encode('UTF8')
        self.portal_type = portal_type


class CSVMeeting:
    def __init__(self, portal_type, date, annex_oj, annex_pv):
        self.portal_type = portal_type
        self.date = date
        self.annex_oj = safe_unicode(annex_oj.replace('\\', '/')).encode('UTF8')
        self.annex_pv = safe_unicode(annex_pv.replace('\\', '/')).encode('UTF8')
        self.items = []


class ImportCSV:
    def __init__(self, portal, f_group_mapping, f_items_college, f_items_council, f_meetings, annex_dir_path,
                 default_group, default_category):
        self.grp_id_mapping = {}
        self.portal = portal
        self.f_group_mapping = f_group_mapping
        self.f_items_college = f_items_college
        self.f_items_council = f_items_council
        self.f_meetings = f_meetings
        self.annex_dir_path = annex_dir_path
        self.default_group = default_group
        self.default_category = default_category
        self.errors = {'io': [], 'item': [], 'meeting': [], 'item_without_annex': []}
        self.item_counter = 0
        self.meeting_counter = 0
        self.groups = {}
        self._deactivated_recurring_items = []

    def _check_file_exists(self, path):
        _path = self.annex_dir_path + path
        if not os.path.isfile(_path):
            raise IOError(u"File not found {path}.".format(path=path))

    def add_annex(self, context, path, annex_type=None, annex_title=None, to_print=False, confidential=False):
        """Adds an annex to p_item.
           If no p_annexType is provided, self.annexFileType is used.
           If no p_annexTitle is specified, the predefined title of the annex type is used."""
        self._check_file_exists(path)

        _path = self.annex_dir_path + path

        if annex_type is None:
            annex_type = 'annexe'

        # get complete annexType id that is like
        # 'meeting-config-id-annexes_types_-_item_annexes_-_financial-analysis'
        annexes_config_root = get_config_root(context)
        annex_type_id = calculate_category_id(annexes_config_root.get(annex_type))

        annex_content_type = 'annex'

        the_annex = createContentInContainer(
                container=context,
                portal_type=annex_content_type,
                title=annex_title or 'Annex',
                file=self._annex_file_content(_path),
                content_category=annex_type_id,
                # assume old document with extendsions .COL, .CONS, .DEL, .DEC... are all .doc files
                # contentType='application/msword',
                content_type='application/msword',
                contentType='application/msword',
                to_print=to_print,
                confidential=confidential)
        the_annex.file.contentType = 'application/msword'
        return the_annex

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
    def _annex_file_content(_path):
        if not os.path.isfile(_path):
            logger.info("Le fichier %s n'a pas ete trouve." % _path)
            return None

        with open(_path, 'r') as annexfile:
            name = safe_unicode(os.path.basename(_path))

            annex_read = annexfile.read()
            annex_file = namedfile.NamedBlobFile(annex_read, filename=name)
            return annex_file

    def add_annexe_to_object(self, obj, path, title):
        try:
            self.add_annex(obj, path, annex_title=title)
            return True
        except IOError as e:
            self.errors['io'].append(e.message)
            logger.warning(e.message)
            return False

    @staticmethod
    def get_portal_type(obj_type):
        if 'col' in obj_type.lower():
            return 'MeetingCollege'
        elif 'cons' in obj_type.lower():
            return 'MeetingCouncil'

    @staticmethod
    def add_meeting_to_dict(dictionary, meeting):
        if meeting.date in dictionary:
            raise KeyError("2 Meetings have the same date {0}".format(meeting.date))
        dictionary[meeting.date] = meeting

    def load_items(self, delib_file, portaltype, meetings):
        logger.info("Load {0}".format(delib_file))
        with io.open(delib_file, 'r', encoding='latin-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=u';')
            # ID	Titre	CreateurID	DateCreation	Categorie	DateSeance	Annexe
            for row in reader:
                try:
                    # skip header
                    if reader.line_num == 1:
                        logger.info(row)
                        continue

                    for value in row:
                        if not value:
                            raise ValueError('Malformed row : {row}'.format(row=row))

                    date = row[5].strip()
                    if date not in meetings:
                        logger.info('Unknown meeting for item : {row}'.format(row=row))
                    else:
                        item = CSVMeetingItem(external_id=row[0],
                                              creator=row[2],
                                              created_on=row[3],
                                              title=safe_unicode(row[1]),
                                              category=row[4],
                                              annex_path=row[6],
                                              portal_type=portaltype)
                        meeting = meetings[date]
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

        try:
            self._check_file_exists(csv_meeting.annex_oj)
        except IOError:
            message = 'Meeting of {date} has no OJ. Skipping...'.format(date=csv_meeting.date)
            logger.info(message)
            self.errors['meeting'].append(message)
            return False

        try:
            self._check_file_exists(csv_meeting.annex_pv)
        except IOError:
            message = 'Meeting of {date} has no PV. Skipping...'.format(date=csv_meeting.date)
            logger.info(message)
            self.errors['meeting'].append(message)
            return False
        return True

    def insert_and_close_meeting(self, member_folder, csv_meeting):
        if not self._check_meeting_data(csv_meeting):
            return

        _id = 'meetingreprise.{date}'.format(date=csv_meeting.date)

        meeting = self.object_already_exists(_id, csv_meeting.portal_type)
        if meeting and meeting[0]:
            message = 'Skipping meeting {id} and it items because it already exists'.format(id=_id)
            logger.info(message)
            self.errors['meeting'].append(message)
            return
        splitted = csv_meeting.date.split('-')
        tme = DateTime(int(splitted[2]),
                       int(splitted[1]),
                       int(splitted[0]))

        if tme.strftime('%d-%m-%y') != csv_meeting.date:
            raise ValueError('DateTime not matching {datetime} not equal {date}'.format(
                    datetime=tme,
                    date=csv_meeting.date))

        meetingid = member_folder.invokeFactory(type_name=csv_meeting.portal_type, id=_id, date=tme)
        meeting = getattr(member_folder, meetingid)
        meeting.setSignatures("")
        meeting.setAssembly("")
        meeting.setDate(tme)
        meeting.setStartDate(tme)

        # meeting.at_post_create_script()
        meeting.processForm(values={'dummy': None})
        meeting.setCreationDate(tme)
        logger.info('Created meeting of {date}'.format(date=meeting.Title()))

        inserted = self.add_annexe_to_object(meeting, csv_meeting.annex_oj, u'Ordre du jour')
        # just in case
        if not inserted:
            meeting.setDescription(meeting.Description() +
                                   '<p>Fichier non trouvé : {oj}</p>'.format(oj=csv_meeting.annex_oj))

        inserted = self.add_annexe_to_object(meeting, csv_meeting.annex_pv, u'Procès verbal')
        # just in case
        if not inserted:
            meeting.setDescription(meeting.Description() +
                                   '<p>Fichier non trouvé : {pv}</p>'.format(pv=csv_meeting.annex_pv))

        logger.info(
            'Adding {items} items to meeting of {date}'.format(items=len(csv_meeting.items), date=meeting.Title()))
        self.portal.REQUEST['PUBLISHED'] = meeting
        for csv_item in csv_meeting.items:
            self.insert_and_present_item(member_folder, csv_item)

        if meeting.get_items():
            meeting.portal_workflow.doActionFor(meeting, 'freeze')
            meeting.portal_workflow.doActionFor(meeting, 'decide')
            meeting.portal_workflow.doActionFor(meeting, 'close')

            for item in meeting.get_items():
                item.setModificationDate(tme)
                item.reindexObject(idxs=['modified', 'ModificationDate'])

        meeting.setModificationDate(tme)

        meeting.reindexObject(idxs=['modified', 'ModificationDate'])
        self.meeting_counter += 1
        transaction.commit()

    def get_matching_proposing_group(self, category):
        grp_id = category.strip() in self.groups and self.groups[category.strip()]
        return grp_id in self.grp_id_mapping and self.grp_id_mapping[grp_id].UID() or self.default_group

    def insert_and_present_item(self, member_folder, csv_item):
        tme = DateTime(csv_item.created_on, datefmt='international')

        itemid = member_folder.invokeFactory(type_name=csv_item.portal_type,
                                             id=csv_item.external_id,
                                             date=tme,
                                             title=csv_item.title)
        item = getattr(member_folder, itemid)
        item.setProposingGroup(self.get_matching_proposing_group(csv_item.category))
        item.setCategory(self.default_category)
        item.setCreators('csvimport')
        item.setDescription('<p>Créateur originel : {creator}</p>'.format(creator=csv_item.creator_id))
        # do not call item.at_post_create_script(). This would get only throuble with cancel quick edit in objects
        item.processForm(values={'dummy': None})
        item.setCreationDate(tme)

        inserted = self.add_annexe_to_object(item, csv_item.annex_path, u'Délibération')
        if not inserted:
            item.setDescription(item.Description() +
                                '<p>Fichier non trouvé : {annex}</p>'.format(annex=csv_item.annex_path))
            decicion_path = csv_item.annex_path.replace('.DEL', '.DEC')
            inserted = self.add_annexe_to_object(item, decicion_path, u'Décision')
            if not inserted:
                item.setDescription(item.Description() +
                                    '<p>Fichier non trouvé : {annex}</p>'.format(annex=decicion_path))
                self.errors['item_without_annex'].append(
                        u'Item id: {id} has no annex (title: {title})'.format(id=csv_item.external_id,
                                                                             title=csv_item.title))
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
            raise ValueError('You must be a Manager to access this script !')

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

        meetings_college = {}
        meetings_council = {}
        logger.info("Load {0}".format(self.f_meetings))
        with io.open(self.f_meetings, 'r', encoding='latin-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=u';')
            # TypeSeance	DateSeance	OJ	PV
            for row in reader:
                # skip header
                if reader.line_num == 1:
                    logger.info(row)
                    continue

                date = row[1].strip()
                portal_type = self.get_portal_type(row[0])

                meeting = CSVMeeting(portal_type=portal_type,
                                     date=date,
                                     annex_oj=row[2].strip(),
                                     annex_pv=row[3].strip())

                if portal_type == 'MeetingCollege':
                    self.add_meeting_to_dict(meetings_college, meeting)

                elif portal_type == 'MeetingCouncil':
                    self.add_meeting_to_dict(meetings_council, meeting)
                else:
                    raise NotImplementedError
        self.load_items(self.f_items_college, 'MeetingItemCollege', meetings_college)
        self.load_items(self.f_items_council, 'MeetingItemCouncil', meetings_council)
        # insert All
        logger.info('Insert Objects to College')
        self.disable_recurring_items('meeting-config-college')
        member_folder = self.portal.Members.csvimport.mymeetings.get('meeting-config-college')
        for csv_meeting in meetings_college.values():
            self.insert_and_close_meeting(member_folder, csv_meeting)
        self.re_enable_recurring_items('meeting-config-college')

        logger.info('Insert Objects to Council')
        self.disable_recurring_items('meeting-config-council')
        member_folder = self.portal.Members.csvimport.mymeetings.get('meeting-config-council')
        for csv_meeting in meetings_council.values():
            self.insert_and_close_meeting(member_folder, csv_meeting)
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


def import_data_from_csv(self,
                         f_group_mapping,
                         f_items_college,
                         f_items_council,
                         f_meetings,
                         annex_dir_path,
                         default_group,
                         default_category=None):
    start_date = datetime.now()
    import_csv = ImportCSV(self,
                           f_group_mapping,
                           f_items_college,
                           f_items_council,
                           f_meetings,
                           annex_dir_path,
                           default_group,
                           default_category)
    meeting_counter, item_counter, errors = import_csv.run()
    logger.info(u'Inserted {meeting} meetings and {item} meeting items.'.format(meeting=meeting_counter,
                                                                                item=item_counter))
    logger.warning(u'{malforemed} meeting items were not created due to missing data in csv :\n{list}'.format(
            malforemed=len(errors['item']),
            list=u'\n\t '.join(errors['item'])))

    logger.warning(u'{ioerr} errors occured while adding annexes :\n{list}'.format(ioerr=len(errors['io']),
                                                                                   list=u'\n\t '.join(errors['io'])))

    logger.warning(u'{meeting} meetings where skipped because they have no annex or no items :\n{list}'.format(meeting=len(errors['meeting']),
                                                                             list=u'\n\t '.join(errors['meeting'])))

    without_annex = u'\n\t '.join(safe_unicode(errors['item_without_annex']))
    logger.warning(u'{items} meeting items where skipped :\n{list}'.format(items=len(errors['item_without_annex']),
                                                                     list=without_annex))
    end_date = datetime.now()
    seconds = end_date - start_date
    seconds = seconds.seconds
    hours = seconds / 3600
    minutes = (seconds - hours * 3600) / 60
    logger.info(u'Import finished in {0} seconds ({1} h {2} m).'.format(seconds, hours, minutes))
