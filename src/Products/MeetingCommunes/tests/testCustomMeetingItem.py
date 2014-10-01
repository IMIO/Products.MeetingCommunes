# -*- coding: utf-8 -*-
#
# File: testCustomMeetingItem.py
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

from DateTime import DateTime
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase


class testCustomMeetingItem(MeetingCommunesTestCase):
    """
        Tests the MeetingItem adapted methods
    """
    def test_GetCertifiedSignatures(self):
        '''Check that the certified signature is defined on developers group but not defined on vendors.'''
        #create an item for test
        self.changeUser('pmManager')
        meetingDate = DateTime('2008/06/12 08:00:00')
        self.create('Meeting', date=meetingDate)
        #create items
        self.changeUser('pmCreator1')
        i1 = self.create('MeetingItem')
        i1.setProposingGroup('vendors')
        #before present in meeting, certfiedSignatures must be empty
        res, isGrpSign = i1.adapted().getCertifiedSignatures()
        self.assertEquals(res, '')
        self.assertEquals(isGrpSign, False)
        self.do(i1, 'propose')
        self.changeUser('pmReviewer1')
        self.do(i1, 'validate')
        self.changeUser('pmManager')
        self.do(i1, 'present')
        # no signatures defined for vendors group, the MeetingConfig.certifiedSignatures are used
        res, isGrpSign = i1.adapted().getCertifiedSignatures()
        self.assertEquals(
            res,
            'Mr Pr\xc3\xa9sent Actuellement, Bourgmestre ff - Charles Exemple, Secr\xc3\xa9taire communal')
        self.assertEquals(isGrpSign, False)
        self.changeUser('pmCreator1')
        i2 = self.create('MeetingItem')
        i2.setProposingGroup('developers')
        #before present in meeting, certfiedSignatures must be empty
        res, isGrpSign = i2.adapted().getCertifiedSignatures()
        self.assertEquals(res, '')
        self.assertEquals(isGrpSign, False)
        self.do(i2, 'propose')
        self.changeUser('pmReviewer1')
        self.do(i2, 'validate')
        self.changeUser('pmManager')
        self.do(i2, 'present')
        #signatures defined for developers group, get it
        res, isGrpSign = i2.adapted().getCertifiedSignatures()
        self.assertEquals(res, 'developers signatures')
        self.assertEquals(isGrpSign, True)

    def test_GetEchevinsForProposingGroup(self):
        '''Check a meetingItem for developers group return an echevin (the Same group in our case)
           and a meetingItem for vendors return no echevin.'''
        #create an item for test
        self.changeUser('pmManager')
        meetingDate = DateTime('2008/06/12 08:00:00')
        self.create('Meeting', date=meetingDate)
        #create items
        self.changeUser('pmCreator1')
        i1 = self.create('MeetingItem')
        i1.setProposingGroup('vendors')
        #before present in meeting, certfiedSignatures must be empty
        res = i1.adapted().getEchevinsForProposingGroup()
        self.assertEquals(res, [])
        self.changeUser('pmCreator1')
        i2 = self.create('MeetingItem')
        i2.setProposingGroup('developers')
        #before present in meeting, certfiedSignatures must be empty
        res = i2.adapted().getEchevinsForProposingGroup()
        self.assertEquals(res, ['developers'])
