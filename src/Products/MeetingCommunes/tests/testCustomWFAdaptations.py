# -*- coding: utf-8 -*-

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase


class testCustomWFAdaptations(MeetingCommunesTestCase):
    ''' '''

    def test_WFA_meetingadvicefinances_add_advicecreated_state(self):
        '''Test the workflowAdaptation 'meetingadvicefinances_add_advicecreated_state'.'''
        # ease override by subproducts
        cfg = self.meetingConfig
        if 'meetingadvicefinances_add_advicecreated_state' not in cfg.listWorkflowAdaptations():
            return
        # apply the financesadvice profile so meetingadvicefinances portal_type is available
        self.portal.portal_setup.runAllImportStepsFromProfile(
            'profile-Products.MeetingCommunes:financesadvice')

        self.changeUser('siteadmin')
        # check while the wfAdaptation is not activated
        self._meetingadvicefinances_add_advicecreated_state_inactive()
        cfg.setWorkflowAdaptations(('meetingadvicefinances_add_advicecreated_state', ))
        cfg.at_post_edit_script()
        self._meetingadvicefinances_add_advicecreated_state_active()

    def _meetingadvicefinances_add_advicecreated_state_inactive(self):
        '''Tests while 'meetingadvicefinances_add_advicecreated_state' wfAdaptation is inactive.'''
        self.assertTrue('meetingadvicefinances_workflow' in self.wfTool)
        self.assertFalse('patched_meetingadvicefinances_workflow' in self.wfTool)

    def _meetingadvicefinances_add_advicecreated_state_active(self):
        '''Tests while 'meetingadvicefinances_add_advicecreated_state' wfAdaptation is active.'''
        self.assertTrue('meetingadvicefinances_workflow' in self.wfTool)
        self.assertTrue('patched_meetingadvicefinances_workflow' in self.wfTool)
        fin_wf = self.wfTool.get('patched_meetingadvicefinances_workflow')
        self.assertTrue('advicecreated' in fin_wf.states)
        self.assertEqual(fin_wf.initial_state, 'advicecreated')
