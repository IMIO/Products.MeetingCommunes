# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#

from Products.MeetingCommunes.testing import MC_TESTING_PROFILE_FUNCTIONAL
from Products.MeetingCommunes.tests.helpers import MeetingCommunesTestingHelpers
from Products.PloneMeeting.tests.PloneMeetingTestCase import PloneMeetingTestCase


class MeetingCommunesTestCase(PloneMeetingTestCase, MeetingCommunesTestingHelpers):
    """Base class for defining MeetingCommunes test cases."""

    # by default, PloneMeeting's test file testPerformances.py and
    # testConversionWithDocumentViewer.py' are ignored, override the subproductIgnoredTestFiles
    # attribute to take these files into account
    subproductIgnoredTestFiles = ['test_robot.py', 'testPerformances.py', 'testContacts.py']

    layer = MC_TESTING_PROFILE_FUNCTIONAL

    cfg1_id = 'meeting-config-college'
    cfg2_id = 'meeting-config-council'

    def _configureFinancesAdvice(self, enable_add_advicecreated=False):
        """ """
        # apply the financesadvice profile so meetingadvicefinances portal_type is available
        self.portal.portal_setup.runAllImportStepsFromProfile(
            'profile-Products.MeetingCommunes:financesadvice')

        if enable_add_advicecreated is True:
            self.tool.setAdvisersConfig(
                ({'advice_types': ['positive',
                                   'positive_with_remarks'],
                  'base_wf': 'meetingadvicefinancessimple_workflow',
                  'default_advice_type': 'positive_with_remarks',
                  'org_uids': [self.vendors_uid],
                  'portal_type': 'meetingadvicefinances',
                  'show_advice_on_final_wf_transition': '1',
                  'wf_adaptations': ['add_advicecreated_state']}, ))
            self.tool.at_post_edit_script()
