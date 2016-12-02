# -*- coding: utf-8 -*-
#
# File: testCustomMeeting.py
#
# Copyright (c) 2007-2013 by Imio.be
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase


class testCustomViews(MeetingCommunesTestCase):
    """
        Tests the custom views
    """

    def test_PrintAllAnnexes(self):
        """ """
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        annex1 = self.addAnnex(item)
        annex2 = self.addAnnex(item, annexTitle='Annex 2')
        annexDecision1 = self.addAnnex(item,
                                       annexTitle='Annex decision 1',
                                       relatedTo='item_decision')

        view = item.restrictedTraverse('@@document-generation')
        helper = view.get_generation_context_helper()
        self.assertEqual(
            helper.printAllAnnexes(),
            '<a href="{0}">Annex</a><br/>\n<a href="{1}">Annex 2</a><br/>'.format(
                annex1.absolute_url(), annex2.absolute_url())
            )
        self.assertEqual(
            helper.printAllAnnexes(portal_types=('annexDecision', )),
            '<a href="{0}">Annex decision 1</a><br/>'.format(
                annexDecision1.absolute_url())
            )
