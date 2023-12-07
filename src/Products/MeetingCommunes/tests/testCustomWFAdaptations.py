# -*- coding: utf-8 -*-

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase


class testCustomWFAdaptations(MeetingCommunesTestCase):
    ''' '''

    def test_WFA_add_advicecreated_state(self):
        '''Test the workflowAdaptation 'add_advicecreated_state'.'''
        # ease override by subproducts
        if not self._check_wfa_available(['add_advicecreated_state'], related_to='MeetingAdvice'):
            return

        self._configureFinancesAdvice()

        self.changeUser('siteadmin')
        # check while the wfAdaptation is not activated
        self._add_advicecreated_state_inactive()
        # enable WFA and test
        self._configureFinancesAdvice(enable_add_advicecreated=True)
        self._add_advicecreated_state_active()

    def _add_advicecreated_state_inactive(self):
        '''Tests when 'add_advicecreated_state' wfAdaptation is inactive.'''
        self.assertTrue('meetingadvicefinances_workflow' in self.wfTool)
        self.assertFalse('patched_meetingadvicefinances_workflow' in self.wfTool)

    def _add_advicecreated_state_active(self):
        '''Tests when 'add_advicecreated_state' wfAdaptation is active.'''
        # base WFs
        self.assertTrue('meetingadvicefinances_workflow' in self.wfTool)
        self.assertTrue('meetingadvicefinancessimple_workflow' in self.wfTool)
        self.assertTrue('meetingadvicefinanceseditor_workflow' in self.wfTool)
        self.assertTrue('meetingadvicefinancesmanager_workflow' in self.wfTool)
        # new created WF
        fin_wf = self.wfTool.get('meetingadvicefinances__meetingadvicefinancessimple_workflow')
        self.assertEqual(fin_wf.initial_state, 'advicecreated')
        self.assertEqual(sorted(fin_wf.states),
                         ['advice_given',
                          'advicecreated',
                          'financial_advice_signed',
                          'proposed_to_financial_manager'])
