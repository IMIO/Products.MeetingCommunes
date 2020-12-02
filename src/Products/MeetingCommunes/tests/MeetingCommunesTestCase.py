# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
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
    subproductIgnoredTestFiles = ['test_robot.py', 'testPerformances.py', 'testContacts.py']

    layer = MC_TESTING_PROFILE_FUNCTIONAL

    cfg1_id = 'meeting-config-college'
    cfg2_id = 'meeting-config-council'
