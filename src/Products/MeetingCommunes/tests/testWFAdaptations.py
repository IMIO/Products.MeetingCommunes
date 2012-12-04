# -*- coding: utf-8 -*-
#
# File: testAdvices.py
#
# Copyright (c) 2012 by Imio.be
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

import logging

from plone.app.testing import login

from Products.PloneMeeting.model.adaptations import performWorkflowAdaptations
from Products.PloneMeeting.tests.testWFAdaptations import testWFAdaptations as pmtwfa

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import \
    MeetingCommunesTestCase



class testWFAdaptations(MeetingCommunesTestCase, pmtwfa):
    '''See doc string in PloneMeeting.tests.testWFAdaptations.'''


    def test_mc_VerifyTestNumbers(self):
        """
            We verify that there are the same test methods in original product and this sub-product
        """
        tpm = self.getTestMethods(pmtwfa, 'test')
        tmc = self.getTestMethods(testWFAdaptations, 'test_mc_call_')
        missing = []
        for key in tpm:
            key2 = key.replace('test', 'test_mc_call_')
            if not tmc.has_key(key2):
                missing.append(key)
        if len(missing):
            self.fail("missing test methods %s from PloneMeeting test class '%s'" % (missing, 'testWFAdaptations'))

    def test_mc_call_WFA_availableWFAdaptations(self):
        '''Test what are the available wfAdaptations.'''
        self.assertEquals(set(self.meetingConfig.listWorkflowAdaptations()),
                          set(('no_global_observation', 'only_creator_may_delete',
                           'pre_validation', 'items_come_validated',
                           'no_publication', 'no_proposal', 'everyone_reads_all',
                           'creator_edits_unless_closed', 'local_meeting_managers',
                           # our wfAdaptations
                           'add_published_state',)))

    def test_mc_call_WFA_no_publication(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        # we have a 'published' state in the "meetingcouncil_worflow" in self.meetingConfig2
        self.meetingConfig = self.meetingConfig2
        pmtwfa.testWFA_no_publication(self)

    def test_mc_call_WFA_no_proposal(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        pmtwfa.testWFA_no_proposal(self)
        self.meetingConfig = self.meetingConfig2
        pmtwfa.testWFA_no_proposal(self)

    def test_mc_call_WFA_pre_validation(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        pmtwfa.testWFA_pre_validation(self)
        self.meetingConfig = self.meetingConfig2
        pmtwfa.testWFA_pre_validation(self)

    def test_mc_call_WFA_creator_initiated_decisions(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py
           In MC WFs this wfAdaptation is not used (deactivated in adapters.py) because it is
           always 'enabled', the creator can edit the decision field by default.'''
        # we just call the subtest while wfAdaptation should be active
        pmtwfa._creator_initiated_decisions_active(self)

    def test_mc_call_WFA_items_come_validated(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        pmtwfa.testWFA_items_come_validated(self)
        self.meetingConfig = self.meetingConfig2
        pmtwfa.testWFA_items_come_validated(self)

    def test_mc_call_WFA_archiving(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        # we do not have an 'archived' state in the meeting/item WFs...
        # just call the subtest while wfAdaptation sould be inactive
        # it is deactived in adapters.py
        pmtwfa._archiving_inactive(self)

    def test_mc_call_WFA_only_creator_may_delete(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        pmtwfa.testWFA_only_creator_may_delete(self)
        self.meetingConfig = self.meetingConfig2
        pmtwfa.testWFA_only_creator_may_delete(self)

    def test_mc_call_WFA_no_global_observation(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        # we have global observations in the meetingcouncil_workflow
        # once item is 'itempublished'
        self.meetingConfig = self.meetingConfig2
        pmtwfa.testWFA_no_global_observation(self)

    def test_mc_call_WFA_everyone_reads_all(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        # we have global observations in the meetingcouncil_workflow
        # once item is 'itempublished'
        self.meetingConfig = self.meetingConfig2
        pmtwfa.testWFA_no_global_observation(self)

    def test_mc_call_WFA_creator_edits_unless_closed(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        # we have global observations in the meetingcouncil_workflow
        # once item is 'itempublished'
        pmtwfa.testWFA_creator_edits_unless_closed(self)
        self.meetingConfig = self.meetingConfig2
        pmtwfa.testWFA_creator_edits_unless_closed(self)

    def test_mc_call_WFA_local_meeting_managers(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        # we have global observations in the meetingcouncil_workflow
        # once item is 'itempublished'
        pmtwfa.testWFA_local_meeting_managers(self)
        self.meetingConfig = self.meetingConfig2
        pmtwfa.testWFA_local_meeting_managers(self)

    def test_mc_WFA_add_published_state(self):
        '''Test the workflowAdaptation 'add_published_state'.
           If meeting is in decided state, only the MeetingManagers can
           view the real decision. The other people view a standard message taken from the MeetingConfig.'''
        login(self.portal, 'pmManager')
        # check while the wfAdaptation is not activated
        self._add_published_state_inactive()
        # activate the wfAdaptation and check
        self.meetingConfig.setWorkflowAdaptations('add_published_state')
        logger = logging.getLogger('MeetingCommunes: tests')
        performWorkflowAdaptations(self.portal, self.meetingConfig, logger)
        self._add_published_state_active()
        
        # test also for the meetingcouncil_workflow
        self.meetingConfig = self.meetingConfig2
        self._add_published_state_inactive()
        self.meetingConfig.setWorkflowAdaptations('add_published_state')
        logger = logging.getLogger('MeetingCommunes: tests')
        performWorkflowAdaptations(self.portal, self.meetingConfig, logger)
        # check while the wfAdaptation is not activated
        self._add_published_state_active()

    def _add_published_state_inactive(self):
        '''Tests while 'add_published_state' wfAdaptation is inactive.
           In this case, the decision is always accessible by the creator no matter it is
           adapted by any MeetingManagers.  There is NO extra 'published' state moreover.'''
        login(self.portal, 'pmManager')
        m1 = self._createMeetingWithItems()
        item = m1.getItems()[0]
        item.setDecision('<p>testing decision field</p>')
        self.changeUser('pmCreator1')
        # relevant users can see the decision
        self.assertEquals(item.getDecision(),'<p>testing decision field</p>')
        self.changeUser('pmManager')
        self.assertEquals(item.getDecision(),'<p>testing decision field</p>')
        decisionHasBeenChanged = False
        for tr in self.transitionsToCloseAMeeting:
            login(self.portal, 'pmManager')
            if tr in self.transitions(m1):
                self.do(m1, tr)
            else:
                continue
            # even when the Meeting is decided, the real decision is viewable
            if not decisionHasBeenChanged and m1.queryState() == 'decided':
                decisionHasBeenChanged = True
                item.setDecision('<p>Decision adapted by pmManager</p>')
                item.reindexObject()
            login(self.portal, 'pmCreator1')
            if decisionHasBeenChanged:
                self.assertEquals(item.getDecision(),'<p>Decision adapted by pmManager</p>')
            else:
                self.assertEquals(item.getDecision(),'<p>testing decision field</p>')
        self.failUnless(decisionHasBeenChanged)

    def _add_published_state_active(self):
        '''Tests while 'add_published_state' wfAdaptation is active.'''
        login(self.portal, 'pmManager')
        m1 = self._createMeetingWithItems()
        item = m1.getItems()[0]
        item.setDecision('<p>testing decision field</p>')
        self.changeUser('pmCreator1')
        # relevant users can see the decision
        self.assertEquals(item.getDecision(),'<p>testing decision field</p>')
        self.changeUser('pmManager')
        self.assertEquals(item.getDecision(),'<p>testing decision field</p>')
        decisionHasBeenChanged = decisionsHaveBeenPublished = False
        # a 'publish_decision' is added after the 'decide' transition
        wfAdaptedTransitionsToCloseAMeeting = list(self.transitionsToCloseAMeeting)
        wfAdaptedTransitionsToCloseAMeeting.insert(wfAdaptedTransitionsToCloseAMeeting.index('decide')+1, 'publish_decisions')
        for tr in wfAdaptedTransitionsToCloseAMeeting:
            login(self.portal, 'pmManager')
            if tr in self.transitions(m1):
                self.do(m1, tr)
            else:
                continue
            if tr == 'publish_decisions':
                decisionsHaveBeenPublished = True
            # just when the Meeting is decided, the decision is not viewable by non Managers
            if not decisionsHaveBeenPublished and m1.queryState() == 'decided':
                decisionHasBeenChanged = True
                item.setDecision('<p>Decision adapted by pmManager</p>')
                item.reindexObject()
            login(self.portal, 'pmCreator1')
            if decisionHasBeenChanged and m1.queryState() == 'decided':
                self.assertEquals(item.getDecision(),'<p>The decision is currently under edit by managers, you can not access it</p>')
            elif decisionHasBeenChanged:
                self.assertEquals(item.getDecision(),'<p>Decision adapted by pmManager</p>')
            else:
                self.assertEquals(item.getDecision(),'<p>testing decision field</p>')
        self.failUnless(decisionHasBeenChanged)
        self.failUnless(decisionsHaveBeenPublished)



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWFAdaptations, prefix='test_mc_'))
    return suite