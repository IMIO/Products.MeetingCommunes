#! /usr/bin/python
# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.CMFPlone.utils import normalizeString
from Products.PloneMeeting.interfaces import IAnnexable

import os
import transaction


""" Reprise des données ACROPOLE de chez Stesud
N'oubliez-pas de fusionner les 3 fichiers xmls afin d'en avoir qu'un seul...
A faire dans l'instance avant migration :
1. Créer un groupe Acropole.
2. Créer un utilisateur acropoleimport créateur d'un quelconque service (nom complet : Importation Acropole)
et se connecter avec.
3. Créer une catégorie 'Reprise Acropole' et la désactiver [SI LES CATEGORIES SONT UTILISEES].
4. Créer les types d'annexes suivants :
1. deliberation
2. advise
3. pdf-link
5. Désactiver les points récurrents dans la config, sinon lors de la création des séances on va avoir des surprises:-)
A faire dans l'instance après migration :
6. A la fin de l'import, supprimer les droits de acropoleimport et réactiver les points récurrents et désactiver le groupe.
"""


class TransformXmlToMeetingOrItem:

    __currentNode__ = None
    __meetingList__ = None
    __itemList__ = None
    __itemsInMeetingList__ = None
    __portal__ = None
    __out__ = []

    def __init__(self, portal, fname=None):
        self.__portal__ = portal
        self.readXml(fname)

    def readXml(self, fname=None):
        """
           read result xml from acsone and create meeting and meetingItems (fname received as parameter)
        """
        from xml.dom.minidom import parse
        self.doc = parse(fname)

    def getRootElement(self):
        """
           On regarde si on a déjà lu le premier élément du fichier.
           Si oui, on ne fait que retourner l'attribut __currentNode__, sinon, on prend le premier élémént du document
        """
        if self.__currentNode__ is None:
            self.__currentNode__ = self.doc.documentElement
        return self.__currentNode__

    def getSignatures(self, node, id):
        """
           Retourne les signatures pour la séance
        """
        res = ''
        try:
            res = u'Le Secr\xe9taire,\n'
            import pdb;pdb.set_trace()
            res = '%s%s\n' % (res, self.getText(node.getElementsByTagName("signatureSecretary")[0]))
            res = '%s%s\n' % (res, 'Le Pr\xe9sident,')
            res = '%s%s' % (res, self.getText(node.getElementsByTagName("signaturePresident")[0]))
        except:
            self.__out__.append('Probleme avec les signatures pour le point %s' % id)
            return ''
        return res

    def getPresences(self, node, id):
        """
           Retourne les présents pour la séance
        """
        res = ''
        i = 0
        for presences in node.getElementsByTagName("presence"):
            try:
                res = '%s%s' % (res, self.getText(node.getElementsByTagName("presence")[i]))
                i = i + 1
            except:
                self.__out__.append('Probleme avec les présences pour le point %s ' % id)
                return ''
        return res

    def insertItemInMeeting(self, meetingConfigType, meeting, itemid):
        """
           C'est ici que nous allons placer les points dans la séance.
        """
        i = 0
        meeting.REQUEST['PUBLISHED'] = meeting
        try:
            #récupération du point ayant comme référence le itemid
            kw = {}
            if meetingConfigType == 'college':
                kw['portal_type'] = ('MeetingItemCollege',)
            else:
                kw['portal_type'] = ('MeetingItemCouncil',)
            kw['id'] = itemid
            itemRef = self.__portal__.portal_catalog.searchResults(kw)
            if itemRef:
                item = itemRef[0].getObject()
                #si le point est déjà dans une séance, alors c'est que c'est un point remis
                #dans ce cas, nous allons créer une copie.
                #Mais on garde la date de création du point d'origine.
                if item.getMeeting():
                    creationDate = item.created()
                    item = item.clone()
                    item.setCreationDate(creationDate)
                    self.__portal__.portal_workflow.doActionFor(item, 'propose')
                    try:
                        self.__portal__.portal_workflow.doActionFor(item, 'prevalidate')
                    except:
                        pass  # prevalidation isn't use
                    self.__portal__.portal_workflow.doActionFor(item, 'validate')
                #présentation et insertion du point dans la séance
                self.__portal__.portal_workflow.doActionFor(item, 'present')
            else:
                self.__out__.append('Le point %s est introuvable.' % itemid)
            i = i + 1
        except:
            a = 1
            import pdb; pdb.set_trace()
        #don't closed empty meeting
        if meeting.getAllItems():
            meeting.portal_workflow.doActionFor(meeting, 'freeze')
            meeting.portal_workflow.doActionFor(meeting, 'decide')
            try:
                meeting.portal_workflow.doActionFor(meeting, 'publish')
            except:
                pass  # publish state not use
            meeting.portal_workflow.doActionFor(meeting, 'close')
        else:
            self.__out__.append('La seance %s est vide.' % meeting.Title().decode('utf-8'))

    def addMeetingAnnexe(self, meetingConfigType, meeting, node, startPath, newPath):
        """
           Nous allons ajouter l'annexe et faire un lien dans le texte de l'observation
        """
        #nous utiliserons le répertoire de acropoleimport
        if meetingConfigType == 'college':
            Memberfolder = self.__portal__.Members.acropoleimport.mymeetings.get('meeting-config-college')
        else:
            Memberfolder = self.__portal__.Members.acropoleimport.mymeetings.get('meeting-config-council')
        annexe = self.getText(node).replace(startPath, newPath)
        if not os.path.isfile(annexe):
            self.__out__.append("Le fichier %s n'a pas ete trouve." % annexe.decode('utf-8'))
            return
        #créons le fichier
        _id = os.path.basename(annexe)
        if not getattr(Memberfolder, _id, None):
            f = file(annexe, 'rb')
            fileId = Memberfolder.invokeFactory(type_name="File", id=_id, file=f)
            f.close()
        else:
            fileId = _id
        #Ajoutons le commentaire avec le lien
        fileObj = getattr(Memberfolder, fileId)
        _observations = 'Un fichier est attaché à cette séance. Vous pouvez l\'ouvrir en cliquant '\
                        '<a href="./resolveuid/%s">ici.</a>' % fileObj.UID()
        meeting.setObservations(_observations)

    def _addAnnexe(self, item, Memberfolder, _path, annexeType, title):
        """
           création et ajout de l'annexe à joindre
        """
        if not os.path.isfile(_path):
            self.__out__.append("Le fichier %s n'a pas ete trouve." % _path)
            return
        _id = os.path.basename(_path)
        _file = file(_path, 'rb')
        meetingConfig = self.__portal__.portal_plonemeeting.getMeetingConfig(item)
        annexeType = getattr(meetingConfig.meetingfiletypes, annexeType)
        IAnnexable(item).addAnnex(idCandidate=_id, annex_title=title, annex_file=_file,
                                  relatedTo='item', meetingFileTypeUID=annexeType.UID())
        _file.close()

    def addItemPDFPoint(self, item, node, Memberfolder, startPath, newPath):
        _path = self.getText(node).replace(startPath, newPath)
        self._addAnnexe(item, Memberfolder, _path, 'pdf-link', 'PDF-POINT')

    def addItemAnnexes(self, item, node, Memberfolder, startPath, newPath):
        i = 0
        for annexes in node.getElementsByTagName("annexLink"):
            try:
                _path = self.getText(node.getElementsByTagName("annexLink")[i]).replace(startPath, newPath)
                title = 'Annexe-%d' % i
                self._addAnnexe(item, Memberfolder, _path, 'annexe', title)
                i = i + 1
            except:
                self.__out__.append("Probleme avec l'annexe %s." % _path)

    def addItemAdvises(self, item, node, Memberfolder, startPath, newPath):
        i = 0
        for annexes in node.getElementsByTagName("adviseLink"):
            try:
                _path = self.getText(node.getElementsByTagName("adviseLink")[i]).replace(startPath, newPath)
                title = 'Avis-%d' % i
                self._addAnnexe(item, Memberfolder, _path, 'advise', title)
                i = i + 1
            except:
                self.__out__.append("Probleme avec l'avis %s." % _path)

    def addItemPDFDelibe(self, item, node, Memberfolder, startPath, newPath):
        _path = self.getText(node).replace(startPath, newPath)
        self._addAnnexe(item, Memberfolder, _path, 'deliberation', 'Deliberation')

    def getItems(self, fgrmapping, fcatmapping, meetingConfigType, startPath, newPath):
        """
           Notre méthode pour créer les points
        """
        if self.__itemList__ is not None:
            return self.__itemList__

        self.__itemList__ = []
        useridLst = [ud['userid'] for ud in self.__portal__.acl_users.searchUsers()]
        group_mapping = createDicoMapping(self, fgrmapping)
        if fcatmapping:
            cat_mapping = createDicoMapping(self, fcatmapping)
        else:  # Les catégories ne sont pas utilisées
            cat_mapping = ''
        if meetingConfigType == 'college':
            meetingConfig = 'meeting-config-college'
            itemType = "MeetingItemCollege"
        else:
            meetingConfig = 'meeting-config-council'
            itemType = "MeetingItemCouncil"
        cpt = 0
        import pdb;pdb.set_trace()
        try:
            for items in self.getRootElement().getElementsByTagName("point"):
                if items.nodeType == items.ELEMENT_NODE:
                    try:
                        #récuptération des données du point
                        _id = self.getText(items.getElementsByTagName("id")[0])
                        #if _id == '245':
                        #    import pdb;pdb.set_trace()
                        _title = self.getText(items.getElementsByTagName("title")[0])
                        try:
                            _description = self.getText(items.getElementsByTagName("description")[0])
                        except:
                            _description = '<p></p>'
                        _creatorId = self.getText(items.getElementsByTagName("creatorId")[0])
                        # pour mes tests en attendant mes réponses
                        #_createDate = self.getText(items.getElementsByTagName("createDate")[0])
                        _createDate = '20160310120000'
                        _old_group = self.getText(items.getElementsByTagName("proposingGroup")[0])
                        #_proposingGroup = normalizeString(group_mapping[_old_group], self)
                        _proposingGroup = 'acropole'
                        #if fcatmapping:
                        #    _old_cat = self.getText(items.getElementsByTagName("category")[0])
                        #    _category = normalizeString(cat_mapping[_old_cat], self)
                        #else:
                        #    _category = ''
                        _category = 'reprise-acropole'
                        try:
                            _decision = self.getText(items.getElementsByTagName("decision")[0])
                        except:
                            _decision = '<p></p>'
                        if _creatorId not in useridLst:
                            #utilisons le répertoire de l'utilisateur acropoleimport'
                            Memberfolder = self.__portal__.Members.acropoleimport.mymeetings.get(meetingConfig)
                            _creatorId = 'acropoleimport'
                        else:
                            Memberfolder = self.__portal__.Members.get(_creatorId).mymeetings.get(meetingConfig)
                        if getattr(Memberfolder, _id, None):
                            # Le point est déjà existant
                            continue
                        itemid = Memberfolder.invokeFactory(type_name=itemType, id=_id, title=_title,
                                                            description=_description)
                        item = getattr(Memberfolder, itemid)
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
                        try:
                            self.addItemPDFPoint(item, items.getElementsByTagName("pdfPointLink")[0], Memberfolder,
                                                 startPath, newPath)
                        except:
                            pass
                        try:
                            self.addItemAnnexes(item, items.getElementsByTagName("annexesLink")[0], Memberfolder, startPath,
                                                newPath)
                        except:
                            pass
                        try:
                            self.addItemAdvises(item, items.getElementsByTagName("advisesLink")[0], Memberfolder, startPath,
                                                newPath)
                        except:
                            pass
                        try:
                            self.addItemPDFDelibe(item, items.getElementsByTagName("pdfDeliberationLink")[0], Memberfolder,
                                                  startPath, newPath)
                        except:
                            pass
                        #plaçons le point en état validé afin qu'il puisse être placé dans une séance
                        item.portal_workflow.doActionFor(item, 'propose')
                        item.portal_workflow.doActionFor(item, 'validate')
                        self.__itemList__.append(item)
                        cpt = cpt + 1
                        # commit transaction si nous avons crÃ©Ã© 50 points
                        if cpt >= 50:
                            transaction.commit()
                            cpt = 0
                            print 'commit'
                    except Exception, msg:
                        self.__out__.append("L'importation du point %s a echouee.%s." % (_id, msg.value))
        except:
            a = 1
            import pdb; pdb.set_trace()
        transaction.commit()
        return self.__itemList__

    def getMeeting(self, meetingConfigType, startPath, newPath):
        """
           Notre méthode pour créer les séances
        """
        if self.__meetingList__ is not None:
            return self.__meetingList__

        self.__meetingList__ = []
        #nous utiliserons le répertoire de acropoleimport
        if meetingConfigType == 'college':
            Memberfolder = self.__portal__.Members.acropoleimport.mymeetings.get('meeting-config-college')
        else:
            Memberfolder = self.__portal__.Members.acropoleimport.mymeetings.get('meeting-config-council')
        #nous ajoutons les droits nécessaire sinon l'invoke factory va raler
        Memberfolder.manage_addLocalRoles('admin', ('MeetingManagerLocal', 'MeetingManager'))
        lat = list(Memberfolder.getLocallyAllowedTypes())
        if meetingConfigType == 'college':
            MeetingType = 'MeetingCollege'
            lat.append(MeetingType)
        else:
            MeetingType = 'MeetingCouncil'
            lat.append(MeetingType)
        Memberfolder.setLocallyAllowedTypes(tuple(lat))
        cpt = 0
        import pdb;pdb.set_trace()
        try:
            for meetings in self.getRootElement().getElementsByTagName("seance"):
                if meetings.nodeType == meetings.ELEMENT_NODE:
                    try:
                        #récupération des données de la séance
                        _id = self.getText(meetings.getElementsByTagName("id")[0])
                        _date = self.getText(meetings.getElementsByTagName("date")[0])
                        _startDate = self.getText(meetings.getElementsByTagName("startDate")[0])
                        if _startDate == 'NULL':
                            _startDate = _date
                        _endDate = self.getText(meetings.getElementsByTagName("endDate")[0])
                        if _endDate == 'NULL':
                            _endDate = _date
                        _signatures = self.getSignatures(meetings.getElementsByTagName("signatures")[0], _id)
                        #_presences = self.getPresences(meetings.getElementsByTagName("presences")[0], _id)
                        _place = self.getText(meetings.getElementsByTagName("place")[0])
                        _presences = ''
                        if getattr(Memberfolder, _id, None):
                            # La séance est déjà existante
                            continue
                        #14/09/2009 >>> 20090914000000 GMT+1
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
                        #la modification des dates éffectives doivent se faire après la création de la séance.
                        _heure = _startDate[8:10]
                        if _heure == '24':
                            _heure = '0'
                        date_str = '%s/%s/%s %s:%s:%s GMT+1' % (_startDate[0:4], _startDate[4:6], _startDate[6:8], _heure,
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
                        try:
                            self.addMeetingAnnexe(meetingConfigType, meeting,
                                                  meetings.getElementsByTagName("pdfSeanceLink")[0], startPath, newPath)
                        except:
                            self.__out__.append('pas de pdf pour cette seance %s.' % _id)
                        self.__meetingList__.append(meeting)

                        cpt = cpt + 1
                        # commit transaction si nous avons créé 25 séances
                        if cpt >= 25:
                            transaction.commit()
                            cpt = 0
                            print 'commit'
                    except Exception, msg:
                        self.__out__.append("L'importation de la seance %s a echouee. %s." % (_id, msg.value))
        except:
            a = 1
            import pdb; pdb.set_trace()
        Memberfolder.manage_delLocalRoles('admin', ('MeetingManagerLocal', 'MeetingManager'))
        lat = list(Memberfolder.getLocallyAllowedTypes())
        lat.remove(MeetingType)
        Memberfolder.setLocallyAllowedTypes(tuple(lat))
        return self.__meetingList__

    def insertItemsInMeeting(self, meetingConfigType):
        """
            Notre méthode pour rattacher les points dans leur séances
        """
        if self.__itemsInMeetingList__ is not None:
            return self.__itemsInMeetingList__

        self.__itemsInMeetingList__ = []
        #nous continuons d'utiliser le répertoire de acropoleimport
        if meetingConfigType == 'college':
            Memberfolder = self.__portal__.Members.acropoleimport.mymeetings.get('meeting-config-college')
        else:
            Memberfolder = self.__portal__.Members.acropoleimport.mymeetings.get('meeting-config-council')
        #nous ajoutons les droits nécessaire sinon l'invoke factory va raler
        Memberfolder.manage_addLocalRoles('admin', ('MeetingManagerLocal', 'MeetingManager'))
        lat = list(Memberfolder.getLocallyAllowedTypes())
        if meetingConfigType == 'college':
            MeetingType = 'MeetingCollege'
            lat.append(MeetingType)
        else:
            MeetingType = 'MeetingCouncil'
            lat.append(MeetingType)
        Memberfolder.setLocallyAllowedTypes(tuple(lat))
        cpt = 0
        import pdb;pdb.set_trace()
        try:
            for items in self.getRootElement().getElementsByTagName("meeting_items"):
                if items.nodeType == items.ELEMENT_NODE:
                    try:
                        _id = self.getText(items.getElementsByTagName("id")[0])
                        _itemID = self.getText(items.getElementsByTagName("item")[0])
                        _meeting = getattr(Memberfolder, _id, None)
                        if _meeting is None:
                            # La séance inexistante ... vu la requête SQL c'est impossible, mais bon ... on est jamais trop prudent
                            continue
                        self.insertItemInMeeting(meetingConfigType, _meeting, _itemID)
                        self.__itemsInMeetingList__.append(_itemID)
                        cpt = cpt + 1
                        # commit transaction si nous avons intégré 50 points
                        if cpt >= 50:
                            transaction.commit()
                            cpt = 0
                            print 'commit'
                    except Exception, msg:
                        self.__out__.append("L'importation du point %s dans la seance %s a echouee. %s."
                                            % (_itemID, _id, msg.value))
        except:
            a = 1
            import pdb; pdb.set_trace()

        Memberfolder.manage_delLocalRoles('admin', ('MeetingManagerLocal', 'MeetingManager'))
        lat = list(Memberfolder.getLocallyAllowedTypes())
        lat.remove(MeetingType)
        Memberfolder.setLocallyAllowedTypes(tuple(lat))
        return self.__itemsInMeetingList__


    def getText(self, node):
        return node.childNodes[0].nodeValue.strip()


def importResultFile(self, fname=None, fgrmapping=None, fcatmapping=None, meetingConfigType=None, startPath=None, newPath=None):
    """
       call this external method to import result file
    """
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
        return "This script needs startPath and newPath to replace path for annexes like "\
               "startPath='file:///var/gru/pdf-files',"\
               "newPath='/home/zope/repries-gembloux/pdf-files')"
    x = TransformXmlToMeetingOrItem(self, fname)
    x.getItems(fgrmapping, fcatmapping, meetingConfigType, startPath, newPath)
    x.getMeeting(meetingConfigType, startPath, newPath)
    x.insertItemsInMeeting(meetingConfigType)
    return '\n'.join(x.__out__)


def createDicoMapping(self, fmapping=None):
    """
       create dico with csv file with mapping OLD xxx and PLONE xxx
    """
    import csv
    try:
        file = open(fmapping, "rb")
        reader = csv.DictReader(file)
    except Exception, msg:
        file.close()
        self.__out__.append("Error with file : %s." % msg.value)

    dic = {}

    for row in reader:
        old = row['OLD'].decode('UTF-8').strip()
        plone = row['PLONE'].decode('UTF-8').strip()
        if old not in dic.keys():
            dic[old] = plone
        else:
            self.__out__.append('key %s - %s already present' % (old, plone))
    return dic
