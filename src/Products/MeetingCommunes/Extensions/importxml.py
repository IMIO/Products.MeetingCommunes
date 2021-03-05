#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from collective.iconifiedcategory.utils import calculate_category_id
from collective.iconifiedcategory.utils import get_config_root
from DateTime import DateTime
from imio.helpers.cache import cleanRamCacheFor
from plone import api
from plone import namedfile
from plone.api import portal
from plone.app.querystring import queryparser
from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import createContentInContainer
from Products.CMFPlone.utils import safe_unicode
from xml.dom.minidom import parse

import csv
import os
import transaction


""" Reprise des données ACROPOLE de chez Stesud
N'oubliez-pas de fusionner les 3 fichiers xmls afin d'en avoir qu'un seul...
A faire dans l'instance avant migration :
1. Créer un groupe Importation.
2. Créer un utilisateur xmlimport créateur d'un quelconque service (nom complet : Importation Acropole) et se connecter avec.
3. Créer une catégorie 'Reprise Acropole' et la désactiver [SI LES CATEGORIES SONT UTILISEES].
4. Créer les types d'annexes suivants :
    1. deliberation
    2. advise
    3. pdf-link
5. Désactiver les points récurrents dans la config, sinon lors de la création des séances on va avoir des surprises :-)

A faire dans l'instance après migration :
6. A la fin de l'import, supprimer les droits de xmlimport et réactiver les points récurrents et désactiver le groupe.
"""


class TransformXmlToMeetingOrItem:
    __currentNode__ = None
    __meetingList__ = None
    __itemDict__ = None
    __portal__ = None
    __ext_ids = []
    _meetingConfigId = None
    _deactivated_recurring_items = []

    __extId_prefix = 'Import-'

    def __init__(self, portal):
        self.__portal__ = portal
        self.annexFileType = 'annexe'
        self.annexFileTypeDecision = 'annexeDecision'
        self.annexFileTypeAdvice = 'annexeAvis'
        self.annexFileTypeMeeting = 'annexe'

    def read_xml(self, fname=None):
        """
           read result xml from acsone and create meeting and meetingItems (fname received as parameter)
        """
        self.doc = parse(fname)

    def get_root_element(self):
        """
           On regarde si on a déjà lu le premier élément du fichier.
           Si oui, on ne fait que retourner l'attribut __currentNode__, sinon, on prend le premier élémént du document
        """
        if self.__currentNode__ is None:
            self.__currentNode__ = self.doc.documentElement
        return self.__currentNode__

    def get_signatures(self, meetingNode):
        """
           Retourne les signatures pour la séance
        """
        res = ''
        signatures = meetingNode.getElementsByTagName("signatures")
        if signatures:
            signatures = signatures[0]
            res = u'Le Secr\xe9taire,\n'
            res = '%s%s\n' % (res, self.get_text_from_node(signatures, "signatureSecretary", default=''))
            res = '%s%s\n' % (res, 'Le Pr\xe9sident,')
            res = '%s%s' % (res, self.get_text_from_node(signatures, "signaturePresident", default=''))
        return res

    def get_presences(self, meetingNode):
        """
           Retourne les présents pour la séance
        """
        res = ''
        i = 0
        for presences in meetingNode.getElementsByTagName("presence"):
            res = '%s%s' % (res, self.get_text(presences))
            i = i + 1
        return res

    def add_annex(self, context, _path, annexType=None, annexTitle=None, relatedTo=None, to_print=False,
                  confidential=False):
        '''Adds an annex to p_item.
           If no p_annexType is provided, self.annexFileType is used.
           If no p_annexTitle is specified, the predefined title of the annex type is used.'''
        if not os.path.isfile(_path):
            print("Le fichier %s n'a pas ete trouve." % _path)
            return

        if annexType is None:
            if context.meta_type == 'MeetingItem':
                if not relatedTo:
                    annexType = self.annexFileType
                elif relatedTo == 'item_decision':
                    annexType = self.annexFileTypeDecision
            elif context.portal_type.startswith('meetingadvice'):
                annexType = self.annexFileTypeAdvice
            elif context.meta_type == 'Meeting':
                annexType = self.annexFileTypeMeeting

        # get complete annexType id that is like
        # 'meeting-config-id-annexes_types_-_item_annexes_-_financial-analysis'
        if relatedTo == 'item_decision':
            context.REQUEST.set('force_use_item_decision_annexes_group', True)
        annexes_config_root = get_config_root(context)
        if relatedTo == 'item_decision':
            context.REQUEST.set('force_use_item_decision_annexes_group', False)
        annexTypeId = calculate_category_id(annexes_config_root.get(annexType))

        annexContentType = 'annex'
        if relatedTo == 'item_decision':
            annexContentType = 'annexDecision'

        theAnnex = createContentInContainer(
            container=context,
            portal_type=annexContentType,
            title=annexTitle or 'Annex',
            file=self._annex_file_content(_path),
            content_category=annexTypeId,
            to_print=to_print,
            confidential=confidential)
        return theAnnex

    def _annex_file_content(self, _path):
        if not os.path.isfile(_path):
            print("Le fichier %s n'a pas ete trouve." % _path)
            return None
        f = open(_path, 'r')
        name = os.path.basename(_path)
        annex_file = namedfile.NamedBlobFile(f.read(), filename=name)
        return annex_file

    def add_item_pdf_point(self, item, itemNode, Memberfolder, startPath, newPath):
        node = itemNode.getElementsByTagName("pdfPointLink")
        if node:
            raise NotImplementedError
            # _path = self.getText(node).replace(startPath, newPath)
            # self._addAnnexe(item, Memberfolder, _path, 'pdf-link', 'PDF-POINT')

    def add_annexe_to_object(self, obj, objNode, startPath, newPath, listNodeName, listItemNodeName):
        node = objNode.getElementsByTagName(listNodeName)
        if node:
            for annexe in node[0].getElementsByTagName(listItemNodeName):
                _path = self._compute_path(self.get_text(annexe), startPath, newPath)
                if _path:
                    title = 'Annexe-%s' % (_path.split('/')[-1].strip('.pdf'))
                    self.add_annex(obj, _path, annexTitle=title)

    def _compute_path(self, base, to_replace, new_value):
        return base and safe_unicode(base).replace(safe_unicode(to_replace), safe_unicode(new_value)) or None

    def add_item_advises(self, item, itemNode, Memberfolder, startPath, newPath):
        i = 0
        node = itemNode.getElementsByTagName("advisesLink")
        if node:
            raise NotImplementedError
            # for annexes in node[0].getElementsByTagName("adviseLink"):
            #     _path = self.getText(node.getElementsByTagName("adviseLink")[i]).replace(startPath, newPath)
            #     title = 'Avis-%d' % i
            #     self._addAnnexe(item, Memberfolder, _path, 'advise', title)
            #     i = i + 1

    def add_item_annex_decision(self, item, itemNode, Memberfolder, startPath, newPath):
        node = itemNode.getElementsByTagName("pdfDeliberationLink")
        if node:
            raise NotImplementedError
            # _path = self.getText(node[0]).replace(startPath, newPath)
            # self._addAnnexe(item, Memberfolder, _path, 'deliberation', 'Deliberation')

    def get_items(self, fgrmapping, fcatmapping, startPath, newPath):
        """
           Notre méthode pour créer les points
        """
        if self.__itemDict__ is not None:
            return self.__itemDict__

        self.__itemDict__ = {}
        useridLst = [ud['userid'] for ud in self.__portal__.acl_users.searchUsers()]
        group_mapping = create_dico_mapping(self, fgrmapping)
        if fcatmapping:
            cat_mapping = create_dico_mapping(self, fcatmapping)
        else:  # Les catégories ne sont pas utilisées
            cat_mapping = {}

        if self._meetingConfigId == 'meeting-config-college':
            itemType = "MeetingItemCollege"
        else:
            itemType = "MeetingItemCouncil"

        self.disable_recurring_items()

        cpt = 0
        for itemNode in self.get_root_element().getElementsByTagName("point"):
            if itemNode.nodeType == itemNode.ELEMENT_NODE:

                # récuptération des données du point
                _id = self.get_text_from_node(itemNode, 'id')
                _creatorIdXml = self.get_text_from_node(itemNode, "creatorId")
                _creatorId = 'xmlimport'
                _title = self.get_text_from_node(itemNode, "title")
                print(u'Item XML #%05d %s' % (int(_id), _title))
                if _title:
                    _title.replace('\n', '').replace('  ', ' ').strip()

                if _creatorIdXml not in useridLst:
                    # utilisons le répertoire de l'utilisateur xmlimport'
                    Memberfolder = self.__portal__.Members.xmlimport.mymeetings.get(self._meetingConfigId)
                else:
                    member = self.__portal__.Members.get(_creatorIdXml)
                    if member:
                        Memberfolder = member.mymeetings.get(self._meetingConfigId)
                        _creatorId = _creatorIdXml
                    else:
                        # utilisons le répertoire de l'utilisateur xmlimport'
                        Memberfolder = self.__portal__.Members.xmlimport.mymeetings.get(self._meetingConfigId)
                        useridLst.remove(_creatorIdXml)

                _extId = '%sitem-%s' % (self.__extId_prefix, _id)
                item = self.object_already_exists(_extId, itemType)
                if item and item[0]:
                    # Le point est déjà existant
                    self.__itemDict__[_id] = item[0].getObject()
                    self.__ext_ids.append(_extId)
                    continue

                itemid = Memberfolder.invokeFactory(type_name=itemType, id=_id, title=_title)
                item = getattr(Memberfolder, itemid)

                # createdate is a linux epoch timestamp
                # Default is Friday, March 10, 2000 12:00:00 PM GMT+01:00
                _createDate = self.get_text_from_node(itemNode, 'createDate', '952686000')

                _proposingGroup = self.get_mapping_value(self.get_text_from_node(itemNode, 'proposingGroup'),
                                                         group_mapping, 'importation')
                _category = self.get_mapping_value(self.get_text_from_node(itemNode, 'category'), cat_mapping,
                                                   'reprise')
                _description = self.get_text_html_from_node(itemNode, "description", '')
                _decision = self.get_text_html_from_node(itemNode, "decision", '')

                if _description:
                    item.setDescription(_description)
                if _decision:
                    item.setDecision(_decision)

                item.setProposingGroup(_proposingGroup)
                item.setCategory(_category)
                item.externalIdentifier = _extId

                tme = DateTime(int(_createDate))
                item.setCreationDate(tme)
                item.setCreators(_creatorId)
                if _creatorId == 'xmlimport':
                    item.setObservations(u'<p>Créateur originel : %s</p>'%safe_unicode(_creatorIdXml))
                item.externalIdentifier = _extId
                ## do not call item.at_post_create_script(). This would get only throuble with cancel quick edit in objects
                item.processForm(values={'dummy': None})

                self.add_item_pdf_point(item, itemNode, Memberfolder, startPath, newPath)
                self.add_annexe_to_object(item, itemNode, startPath, newPath, "annexesLink", "annexLink")
                self.add_item_advises(item, itemNode, Memberfolder, startPath, newPath)
                self.add_item_annex_decision(item, itemNode, Memberfolder, startPath, newPath)

                self.__itemDict__[_id] = item
                self.__ext_ids.append(_extId)
                cpt = cpt + 1
                # commit transaction si nous avons créé 50 points
                if cpt >= 50:
                    transaction.commit()
                    cpt = 0
                    print('commit')

        transaction.commit()
        return self.__itemDict__

    def get_mapping_value(self, valueName, mapping, default):
        if valueName in mapping:
            groupName = mapping[valueName]
            tool = api.portal.get_tool('portal_plonemeeting')
            groups = tool.getMeetingGroups(onlyActive=False)
            for group in groups:
                if group.Title() == groupName or group.getAcronym() == groupName:
                    return group.getId()
        return default

    def get_meeting(self, startPath, newPath):
        """
           Notre méthode pour créer les séances
        """
        if self.__meetingList__ is not None:
            return self.__meetingList__

        self.__meetingList__ = []
        # nous utiliserons le répertoire de xmlimport
        Memberfolder = self.__portal__.Members.xmlimport.mymeetings.get(self._meetingConfigId)
        # nous ajoutons les droits nécessaire sinon l'invoke factory va raler
        Memberfolder.manage_addLocalRoles('admin', ('MeetingManagerLocal', 'MeetingManager'))
        lat = list(Memberfolder.getLocallyAllowedTypes())
        if self._meetingConfigId == 'meeting-config-college':
            MeetingType = 'MeetingCollege'
            lat.append(MeetingType)
        else:
            MeetingType = 'MeetingCouncil'
            lat.append(MeetingType)

        Memberfolder.setLocallyAllowedTypes(tuple(lat))
        for meetings in self.get_root_element().getElementsByTagName("seance"):
            if meetings.nodeType == meetings.ELEMENT_NODE:
                # récupération des données de la séance
                _id = self.get_text_from_node(meetings, "id")
                # date is formatted like 31/12/2006
                _date = self.get_text_from_node(meetings, "date", 'NULL')
                print('Meeting XML %s' % _date)
                _startDate = self.get_text_from_node(meetings, "startDate", _date)
                _endDate = self.get_text_from_node(meetings, "endDate", _date)
                _signatures = self.get_signatures(meetings)
                _presences = self.get_presences(meetings)
                _place = self.get_text_from_node(meetings, "place")
                _presences = ''
                if getattr(Memberfolder, _id, None):
                    # La séance est déjà existante
                    continue

                tme = DateTime(_date, datefmt='international')
                meetingid = Memberfolder.invokeFactory(type_name=MeetingType, id=_id, date=tme)
                meeting = getattr(Memberfolder, meetingid)
                meeting.signatures = RichTextValue(_signatures)
                meeting.assembly = RichTextValue(_presences)
                meeting.place = _place

                tme = DateTime(_startDate).asdatetime()
                meeting.start_date = tme

                tme = DateTime(_endDate).asdatetime()
                meeting.end_date = tme
                self.add_annexe_to_object(meeting, meetings, startPath, newPath, "pdfsSeanceLink", "pdfSeanceLink")

                print('Inserting Items in Meetings %s' % meeting.Title())
                self._insert_items_in_meeting(meeting, meetings.getElementsByTagName("pointsRef"))

                self.__meetingList__.append(meeting)

                # don't closed empty meeting
                if meeting.get_items():
                    meeting.portal_workflow.doActionFor(meeting, 'freeze')
                    meeting.portal_workflow.doActionFor(meeting, 'decide')
                    try:
                        meeting.portal_workflow.doActionFor(meeting, 'publish')
                    except:
                        pass  # publish state not use
                    meeting.portal_workflow.doActionFor(meeting, 'close')
                    self.reset_items_modified_date(meeting.get_items())
                else:
                    print('La seance %s est vide.' % meeting.Title().decode('utf-8'))

        self.re_enable_recurring_items()
        return self.__meetingList__

    def _insert_items_in_meeting(self, meeting, node):
        """
            Notre méthode pour rattacher les points dans leur séances
        """
        if node:
            cleanRamCacheFor('Products.PloneMeeting.MeetingConfig.getMeetingsAcceptingItems')
            cleanRamCacheFor('Products.PloneMeeting.MeetingItem.getMeetingToInsertIntoWhenNoCurrentMeetingObject')
            for itemIdNode in node[0].getElementsByTagName("item"):
                _id = self.get_text(itemIdNode)
                item = self.__itemDict__[_id]
                if item:
                    if item.hasMeeting():
                        print((u'Copying Item : %s | %s' % (safe_unicode(_id), safe_unicode(item.Title()))).encode('UTF8'))
                        item = self.get_copy_of_item(item)

                    item.setPreferredMeeting(meeting.UID())
                    print((u'Presenting Item : %s | %s' % (safe_unicode(_id), safe_unicode(item.Title()))).encode('UTF8'))
                    self.do_item_transaction(item)

    def get_text_html_from_node(self, node, childName, default='<p></p>'):
        result = self.get_text_from_node(node, childName, default)
        if result:
            result.strip()
            return portal.get().portal_transforms.convertTo('text/html', result).getData()
        return default

    def get_text_from_node(self, node, childName, default='<p></p>'):
        # returns a list of child nodes matching the given name
        child = node.getElementsByTagName(childName)
        if child and child:
            result = self.get_text(child[0])
            if result:
                result.strip()
            return result
        return default

    def get_text(self, node):
        return node.firstChild and node.firstChild.nodeValue.strip() or None

    def get_copy_of_item(self, item):
        creationDate = item.created()
        newItem = item.clone()
        newItem.setCreationDate(creationDate)
        self.do_item_transaction(newItem)
        return newItem

    def do_item_transaction(self, item):
        self.__portal__.portal_workflow.doActionFor(item, 'propose')
        try:
            self.__portal__.portal_workflow.doActionFor(item, 'prevalidate')
        except:
            pass  # prevalidation isn't use
        self.__portal__.portal_workflow.doActionFor(item, 'validate')
        self.__portal__.portal_workflow.doActionFor(item, 'present')

    def object_already_exists(self, _extId, portalType):
        catalog_query = [{'i': 'portal_type',
                          'o': 'plone.app.querystring.operation.selection.is',
                          'v': portalType},
                         {'i': 'externalIdentifier',
                          'o': 'plone.app.querystring.operation.selection.is',
                          'v': _extId}, ]
        query = queryparser.parseFormquery(self, catalog_query)
        res = self.__portal__.portal_catalog(**query)
        if res:
            print('Already created %s' % _extId)
        return res

    # Asked specifically by Dison
    def reset_items_modified_date(self, items):
        for item in items:
            item.setModificationDate(item.created())

    def disable_recurring_items(self):
        self._deactivated_recurring_items = []
        cfg = self.__portal__.portal_plonemeeting.get(self._meetingConfigId)
        for item in cfg.getRecurringItems():
            self.__portal__.portal_workflow.doActionFor(item, 'deactivate')
            self._deactivated_recurring_items.append(item.UID())

    def re_enable_recurring_items(self):
        cfg = self.__portal__.portal_plonemeeting.get(self._meetingConfigId)
        for item in cfg.getRecurringItems(False):
            if item.UID() in self._deactivated_recurring_items:
                self.__portal__.portal_workflow.doActionFor(item, 'activate')



def import_result_file(self, fname=None, fgrmapping=None, fcatmapping=None, meetingConfigType=None, startPath=None,
                       newPath=None):
    """
       call this external method to import result file
    """
    #
    # context.xmlimport(context, fname='/home/oli/Téléchargements/Dison/data.xml',
    #                   fgrmapping='/home/oli/Téléchargements/Dison/groups_mapping.csv',
    #                   meetingConfigType='college',
    #                   startPath='/home/lambil/Documents/DATA',
    #                   newPath='/home/oli/Téléchargements/Dison')
    #
    #
    member = self.portal_membership.getAuthenticatedMember()
    if not member.has_role('Manager'):
        return 'You must be a Manager to access this script !'

    if not fname:
        return "This script needs a 'fname' parameter with xml sources like 'result.xml'"

    if not fgrmapping:
        return "This script needs a 'fgrmapping' parameter like '/media/Data/Documents/Projets/'\
        'Reprises GRU/Mons/Mapping.csv'"

    x = TransformXmlToMeetingOrItem(self)
    if meetingConfigType not in ('college', 'council'):
        return "<html><body>This script needs a 'meetingConfigType' parameter equal to college or council'</body></html>"
    else:
        x._meetingConfigId = 'meeting-config-%s' % meetingConfigType

    if not startPath or not newPath:
        return "<html><body>This script needs startPath and newPath to replace path for annexes like " \
               "startPath='file:///var/gru/pdf-files'," \
               "newPath='/home/zope/repries-gembloux/pdf-files')</body></html>"

    print('Starting Import')
    x.read_xml(fname)
    x.get_items(fgrmapping, fcatmapping, safe_unicode(startPath), safe_unicode(newPath))
    transaction.commit()
    x.get_meeting(startPath, newPath)
    transaction.commit()
    print('Import finished')
    return '<html><body><h1>Done</h1></body></html>'


def create_dico_mapping(self, fmapping=None):
    """
       create dico with csv file with mapping OLD xxx and PLONE xxx
    """
    file = None
    try:
        file = open(fmapping, "rb")
        reader = csv.DictReader(file)
    except Exception:
        if file:
            file.close()
        raise Exception

    dic = {}

    for row in reader:
        old = row['OLD'].decode('UTF-8').strip()
        plone = row['PLONE'].decode('UTF-8').strip()
        if old not in dic.keys():
            dic[old] = plone
        else:
            print('key %s - %s already present' % (old, plone))
    return dic
