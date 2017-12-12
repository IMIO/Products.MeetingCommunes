#! /usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os
from xml.dom.minidom import parse

import transaction
from DateTime import DateTime
from Products.CMFPlone.utils import safe_unicode
from collective.iconifiedcategory.utils import get_config_root, calculate_category_id
from plone import namedfile, api
from plone.dexterity.utils import createContentInContainer

""" Reprise des données ACROPOLE de chez Stesud
N'oubliez-pas de fusionner les 3 fichiers xmls afin d'en avoir qu'un seul...
A faire dans l'instance avant migration :
1. Créer un groupe Importation.
2. Créer un utilisateur xmlimport créateur d'un quelconque service (nom complet : Importation Acropole)
et se connecter avec.
3. Créer une catégorie 'Reprise Acropole' et la désactiver [SI LES CATEGORIES SONT UTILISEES].
4. Créer les types d'annexes suivants :
1. deliberation
2. advise
3. pdf-link
5. Désactiver les points récurrents dans la config, sinon lors de la création des séances on va avoir des surprises:-)
A faire dans l'instance après migration :
6. A la fin de l'import, supprimer les droits de xmlimport et réactiver les points récurrents et désactiver le groupe.
"""


class TransformXmlToMeetingOrItem:
    __currentNode__ = None
    __meetingList__ = None
    __itemList__ = None
    __portal__ = None

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
            print "Le fichier %s n'a pas ete trouve." % _path
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
            print "Le fichier %s n'a pas ete trouve." % _path
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
        i = 1
        node = objNode.getElementsByTagName(listNodeName)
        if node:
            for annexe in node[0].getElementsByTagName(listItemNodeName):
                _path = self._compute_path(self.get_text(annexe), startPath, newPath)
                title = 'Annexe-%d' % i
                self.add_annex(obj, _path, annexTitle=title)
                i = i + 1

    def _compute_path(self, base, to_replace, new_value):
        return safe_unicode(base).replace(safe_unicode(to_replace), safe_unicode(new_value))

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

    def get_items(self, fgrmapping, fcatmapping, meetingConfigType, startPath, newPath):
        """
           Notre méthode pour créer les points
        """
        if self.__itemList__ is not None:
            return self.__itemList__

        self.__itemList__ = []
        useridLst = [ud['userid'] for ud in self.__portal__.acl_users.searchUsers()]
        group_mapping = create_dico_mapping(self, fgrmapping)
        if fcatmapping:
            cat_mapping = create_dico_mapping(self, fcatmapping)
        else:  # Les catégories ne sont pas utilisées
            cat_mapping = {}
        if meetingConfigType == 'college':
            meetingConfig = 'meeting-config-college'
            itemType = "MeetingItemCollege"
        else:
            meetingConfig = 'meeting-config-council'
            itemType = "MeetingItemCouncil"
        cpt = 0
        for itemNode in self.get_root_element().getElementsByTagName("point"):
            if itemNode.nodeType == itemNode.ELEMENT_NODE:

                # récuptération des données du point
                _id = self.get_text_from_node(itemNode, 'id')
                _description = self.get_text_from_node(itemNode, "description")
                _creatorId = self.get_text_from_node(itemNode, "creatorId")
                _title = self.get_text_from_node(itemNode, "title")

                if _creatorId not in useridLst:
                    # utilisons le répertoire de l'utilisateur xmlimport'
                    Memberfolder = self.__portal__.Members.xmlimport.mymeetings.get(meetingConfig)
                    _creatorId = 'xmlimport'
                else:
                    member = self.__portal__.Members.get(_creatorId)
                    if member:
                        Memberfolder = member.mymeetings.get(meetingConfig)
                    else:
                        # utilisons le répertoire de l'utilisateur xmlimport'
                        Memberfolder = self.__portal__.Members.xmlimport.mymeetings.get(meetingConfig)
                        useridLst.remove(_creatorId)
                        _creatorId = 'xmlimport'

                if getattr(Memberfolder, _id, None):
                    # Le point est déjà existant
                    continue

                itemid = Memberfolder.invokeFactory(type_name=itemType, id=_id, title=_title,
                                                    description=_description)
                item = getattr(Memberfolder, itemid)

                # pour mes tests en attendant mes réponses
                _createDate = self.get_text_from_node(itemNode, 'createDate', '20000310120000')

                _proposingGroup = self.get_mapping_value(item, self.get_text_from_node(itemNode, 'proposingGroup'),
                                                         group_mapping, 'importation')
                _category = self.get_mapping_value(item, self.get_text_from_node(itemNode, 'category'), cat_mapping,
                                                   'reprise')
                _decision = self.get_text_from_node(itemNode, "decision")

                item.setDecision(_decision)
                item.setProposingGroup(_proposingGroup)
                item.setCategory(_category)
                _heure = _createDate[8:10]
                if _heure == '24':
                    _heure = '0'
                date_str = '%s/%s/%s %s:%s:%s GMT+1' % (_createDate[0:4], _createDate[4:6], _createDate[6:8],
                                                        _heure, _createDate[10:12], _createDate[12:14])
                tme = DateTime(date_str)
                item.setCreationDate(tme)
                item.setCreators(_creatorId)
                item.at_post_create_script()
                self.add_item_pdf_point(item, itemNode, Memberfolder, startPath, newPath)
                self.add_annexe_to_object(item, itemNode, startPath, newPath, "annexesLink", "annexLink")
                self.add_item_advises(item, itemNode, Memberfolder, startPath, newPath)
                self.add_item_annex_decision(item, itemNode, Memberfolder, startPath, newPath)
                # plaçons le point en état validé afin qu'il puisse être placé dans une séance
                self.do_item_transaction(item)
                self.__itemList__.append(item)
                cpt = cpt + 1
                # commit transaction si nous avons crÃ©Ã© 50 points
                if cpt >= 50:
                    transaction.commit()
                    cpt = 0
                    print 'commit'

        transaction.commit()
        return self.__itemList__

    def get_mapping_value(self, context, valueName, mapping, default):
        if valueName in mapping:
            groupName = mapping[valueName]
            tool = api.portal.get_tool('portal_plonemeeting')
            groups = tool.getMeetingGroups()
            for group in groups:
                if group.Title() == groupName or group.getAcronym() == groupName:
                    return group.getId()
        return default

    def get_meeting(self, meetingConfigType, startPath, newPath):
        """
           Notre méthode pour créer les séances
        """
        if self.__meetingList__ is not None:
            return self.__meetingList__

        self.__meetingList__ = []
        # nous utiliserons le répertoire de xmlimport
        if meetingConfigType == 'college':
            Memberfolder = self.__portal__.Members.xmlimport.mymeetings.get('meeting-config-college')
        else:
            Memberfolder = self.__portal__.Members.xmlimport.mymeetings.get('meeting-config-council')
        # nous ajoutons les droits nécessaire sinon l'invoke factory va raler
        Memberfolder.manage_addLocalRoles('admin', ('MeetingManagerLocal', 'MeetingManager'))
        lat = list(Memberfolder.getLocallyAllowedTypes())
        if meetingConfigType == 'college':
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
                _date = self.get_text_from_node(meetings, "date")
                _startDate = self.get_text_from_node(meetings, "startDate")
                if _startDate == 'NULL':
                    _startDate = _date
                _endDate = self.get_text_from_node(meetings, "endDate")
                if _endDate == 'NULL':
                    _endDate = _date
                _signatures = self.get_signatures(meetings)
                _presences = self.get_presences(meetings)
                _place = self.get_text_from_node(meetings, "place")
                _presences = ''
                if getattr(Memberfolder, _id, None):
                    # La séance est déjà existante
                    continue
                # 14/09/2009 >>> 20090914000000 GMT+1
                date_str = '%s/%s/%s 00:00:00 GMT+1' % (_date[6:10], _date[3:5], _date[0:2])
                tme = DateTime(date_str)
                meetingid = Memberfolder.invokeFactory(type_name=MeetingType, id=_id, date=tme)
                meeting = getattr(Memberfolder, meetingid)
                meeting.setSignatures(_signatures)
                meeting.setAssembly(_presences)
                meeting.setPlace(_place)
                meeting.at_post_create_script()
                # on prend la date pour construire la startDate et la endDate
                _startDate = '%s%s%s000000' % (_date[6:10], _date[3:5], _date[0:2])
                _endDate = '%s%s%s000000' % (_date[6:10], _date[3:5], _date[0:2])
                # la modification des dates éffectives doivent se faire après la création de la séance.
                _heure = _startDate[8:10]
                if _heure == '24':
                    _heure = '0'
                date_str = '%s/%s/%s %s:%s:%s GMT+1' % (
                    _startDate[0:4], _startDate[4:6], _startDate[6:8], _heure,
                    _startDate[10:12], _startDate[12:14])
                tme = DateTime(date_str)
                meeting.setStartDate(tme)
                _heure = _endDate[8:10]
                if _heure == '24':
                    _heure = '0'
                date_str = '%s/%s/%s %s:%s:%s GMT+1' % (_endDate[0:4], _endDate[4:6], _endDate[6:8], _heure,
                                                        _endDate[10:12], _endDate[12:14])
                tme = DateTime(date_str)
                meeting.setEndDate(tme)
                self.add_annexe_to_object(meeting, meetings, startPath, newPath, "pdfsSeanceLink", "pdfSeanceLink")

                print 'Inserting Items in Meetings %s' % meeting.Title()
                self._insert_items_in_meeting(meeting, meetingConfigType, meetings.getElementsByTagName("pointsRef"))

                self.__meetingList__.append(meeting)

                # don't closed empty meeting
                if meeting.getItems():
                    meeting.portal_workflow.doActionFor(meeting, 'freeze')
                    meeting.portal_workflow.doActionFor(meeting, 'decide')
                    try:
                        meeting.portal_workflow.doActionFor(meeting, 'publish')
                    except:
                        pass  # publish state not use
                    meeting.portal_workflow.doActionFor(meeting, 'close')
                else:
                    print 'La seance %s est vide.' % meeting.Title().decode('utf-8')

                transaction.commit()
                print 'commit'

        return self.__meetingList__

    def _insert_items_in_meeting(self, meeting, meetingConfigType, node):
        """
            Notre méthode pour rattacher les points dans leur séances
        """
        if node:
            kw = {}
            if meetingConfigType == 'college':
                kw['portal_type'] = ('MeetingItemCollege',)
            else:
                kw['portal_type'] = ('MeetingItemCouncil',)

            kw['id'] = []

            for itemIdNode in node[0].getElementsByTagName("item"):
                itemId = self.get_text(itemIdNode)
                if itemId:
                    kw['id'].append(itemId)

            if kw['id']:
                brains = self.__portal__.portal_catalog.searchResults(kw)
                meeting.REQUEST['PUBLISHED'] = meeting
                for brain in brains:
                    item = brain.getObject()

                    if item.hasMeeting():
                        item = self.get_copy_of_item(item)

                    item.setPreferredMeeting(meeting.UID())
                    item.portal_workflow.doActionFor(item, 'present')

    def get_text_from_node(self, node, childName, default='<p></p>'):
        # returns a list of child nodes matching the given name
        child = node.getElementsByTagName(childName)
        if child and child:
            return self.get_text(child[0])
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


def import_result_file(self, fname=None, fgrmapping=None, fcatmapping=None, meetingConfigType=None, startPath=None,
                       newPath=None):
    """
       call this external method to import result file
    """
    #
    # context.xmlimport(context, fname='/home/oli/Téléchargements/Dison/data.xml',
    #                   fgrmapping='/home/oli/Téléchargements/Dison/groups_mapping.csv', meetingConfigType='college',
    #                   startPath='/home/lambil/Documents/DATA', newPath='/home/oli/Téléchargements/Dison')
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

    if meetingConfigType not in ('college', 'council'):
        return "This script needs a 'meetingConfigType' parameter equal to college or council'"
    if not startPath or not newPath:
        return "This script needs startPath and newPath to replace path for annexes like " \
               "startPath='file:///var/gru/pdf-files'," \
               "newPath='/home/zope/repries-gembloux/pdf-files')"

    print 'Starting Import'
    x = TransformXmlToMeetingOrItem(self)
    x.read_xml(fname)
    x.get_items(fgrmapping, fcatmapping, meetingConfigType, safe_unicode(startPath), safe_unicode(newPath))
    transaction.commit()
    x.get_meeting(meetingConfigType, startPath, newPath)
    transaction.commit()
    print 'Import finished'
    return '<body><h1>Done</h1></body>'


def create_dico_mapping(self, fmapping=None):
    """
       create dico with csv file with mapping OLD xxx and PLONE xxx
    """
    try:
        file = open(fmapping, "rb")
        reader = csv.DictReader(file)
    except Exception:
        file.close()
        raise Exception

    dic = {}

    for row in reader:
        old = row['OLD'].decode('UTF-8').strip()
        plone = row['PLONE'].decode('UTF-8').strip()
        if old not in dic.keys():
            dic[old] = plone
        else:
            print 'key %s - %s already present' % (old, plone)
    return dic
