# -*- coding: utf-8 -*-
#
# File: testCustomtoolPoneMeeting.py
#
# GNU General Public License (GPL)
#

from imio.helpers.content import richtextval
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase


class testCustomToolPloneMeeting(MeetingCommunesTestCase):
    """Tests the ToolPloneMeeting adapted methods."""

    def test_GetSpecificAssemblyFor(self):
        """
            This method aimed to ease printings should return formated assembly
        """
        self.changeUser('pmManager')
        m1 = self._createMeetingWithItems()
        m1.assembly = richtextval(
            'Pierre Dupont - Bourgmestre,\n'
            'Charles Exemple - 1er Echevin,\n'
            'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n'
            'Jacqueline Exemple, Responsable du CPAS')
        attendee = '<p class="mltAssembly">Pierre Dupont - Bourgmestre,<br />' \
                   'Charles Exemple - 1er Echevin,<br />Echevin Un, Echevin Deux, ' \
                   'Echevin Trois - Echevins,<br />Jacqueline Exemple, Responsable du CPAS</p>'
        self.assertEqual(self.tool.adapted().getSpecificAssemblyFor(m1.get_assembly(), startTxt='')[0],
                         attendee)
        self.assertEqual(self.tool.adapted().getSpecificAssemblyFor(m1.get_assembly(), startTxt='Absent'),
                         '')
        self.assertEqual(self.tool.adapted().getSpecificAssemblyFor(m1.get_assembly(), startTxt='Excus'),
                         '')
        m1.assembly = richtextval(
            'Pierre Dupont - Bourgmestre,\n'
            'Charles Exemple - 1er Echevin,\n'
            'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n'
            'Jacqueline Exemple, Responsable du CPAS \n'
            'Excusés: \n '
            'Monsieur x, Mesdames Y et Z')
        self.assertEqual(self.tool.adapted().getSpecificAssemblyFor(m1.get_assembly(), startTxt='')[0],
                         attendee)
        self.assertEqual(self.tool.adapted().getSpecificAssemblyFor(m1.get_assembly(), startTxt='Absent'),
                         u'')
        self.assertEqual(self.tool.adapted().getSpecificAssemblyFor(m1.get_assembly(), startTxt='Excus')[0],
                         u'Excusés:')
        self.assertEqual(self.tool.adapted().getSpecificAssemblyFor(m1.get_assembly(), startTxt='Excus')[1],
                         u'<p class="mltAssembly">Monsieur x, Mesdames Y et Z</p>')
        m1.assembly = richtextval(
            'Pierre Dupont - Bourgmestre,\n'
            'Charles Exemple - 1er Echevin,\n'
            'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n'
            'Jacqueline Exemple, Responsable du CPAS \n'
            'Absent: \n '
            'Monsieur tartenpion \n'
            'Excusés: \n '
            'Monsieur x, Mesdames Y et Z')
        self.assertEqual(self.tool.adapted().getSpecificAssemblyFor(m1.get_assembly(), startTxt='')[0],
                         attendee)
        self.assertEqual(self.tool.adapted().getSpecificAssemblyFor(m1.get_assembly(), startTxt='Absent')[0],
                         u'Absent:')
        self.assertEqual(self.tool.adapted().getSpecificAssemblyFor(m1.get_assembly(), startTxt='Absent')[1],
                         u'<p class="mltAssembly">Monsieur tartenpion</p>')
        self.assertEqual(self.tool.adapted().getSpecificAssemblyFor(m1.get_assembly(), startTxt='Excus')[0],
                         u'Excusés:')
        self.assertEqual(self.tool.adapted().getSpecificAssemblyFor(m1.get_assembly(), startTxt='Excus')[1],
                         u'<p class="mltAssembly">Monsieur x, Mesdames Y et Z</p>')
