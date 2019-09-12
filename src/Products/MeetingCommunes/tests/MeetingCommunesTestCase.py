# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2012 by CommunesPlone.org
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

from Products.MeetingCommunes.testing import MC_TESTING_PROFILE_FUNCTIONAL
from Products.MeetingCommunes.tests.helpers import MeetingCommunesTestingHelpers
from Products.PloneMeeting.tests.PloneMeetingTestCase import PloneMeetingTestCase


class MeetingCommunesTestCase(PloneMeetingTestCase, MeetingCommunesTestingHelpers):
    """Base class for defining MeetingCommunes test cases."""

    # Some default content
    descriptionText = '<p>Some description</p>'
    decisionText = '<p>Some decision.</p>'
    # by default, PloneMeeting's test file testPerformances.py and
    # testConversionWithDocumentViewer.py' are ignored, override the subproductIgnoredTestFiles
    # attribute to take these files into account
    subproductIgnoredTestFiles = ['test_robot.py', 'testPerformances.py', 'testContacts.py', 'testVotes.py']

    layer = MC_TESTING_PROFILE_FUNCTIONAL

    cfg1_id = 'meeting-config-college'
    cfg2_id = 'meeting-config-council'
