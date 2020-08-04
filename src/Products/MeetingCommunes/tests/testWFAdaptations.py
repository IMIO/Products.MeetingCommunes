# -*- coding: utf-8 -*-

from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.tests.PloneMeetingTestCase import pm_logger
from Products.PloneMeeting.tests.testWFAdaptations import testWFAdaptations as pmtwfa


class testWFAdaptations(MeetingCommunesTestCase, pmtwfa):
    '''See doc string in PloneMeeting.tests.testWFAdaptations.'''

    def test_pm_WFA_availableWFAdaptations(self):
        '''Test what are the available wfAdaptations.'''
        # we removed the 'archiving' and 'creator_initiated_decisions' wfAdaptations
        self.assertEqual(sorted(self.meetingConfig.listWorkflowAdaptations().keys()),
                         ['accepted_out_of_meeting',
                          'accepted_out_of_meeting_and_duplicated',
                          'accepted_out_of_meeting_emergency',
                          'accepted_out_of_meeting_emergency_and_duplicated',
                          'creator_edits_unless_closed',
                          'decide_item_when_back_to_meeting_from_returned_to_proposing_group',
                          'everyone_reads_all',
                          'hide_decisions_when_under_writing',
                          'items_come_validated',
                          'mark_not_applicable',
                          'meetingmanager_correct_closed_meeting',
                          'no_global_observation',
                          'no_proposal',
                          'no_publication',
                          'only_creator_may_delete',
                          'postpone_next_meeting',
                          'pre_validation',
                          'pre_validation_keep_reviewer_permissions',
                          'presented_item_back_to_itemcreated',
                          'presented_item_back_to_prevalidated',
                          'presented_item_back_to_proposed',
                          'refused',
                          'removed',
                          'removed_and_duplicated',
                          'return_to_proposing_group',
                          'return_to_proposing_group_with_all_validations',
                          'return_to_proposing_group_with_last_validation',
                          'reviewers_take_back_validated_item',
                          'waiting_advices'])

    def test_pm_Validate_workflowAdaptations_added_no_publication(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        # we have a 'published' state in self.meetingConfig2
        self.meetingConfig = self.meetingConfig2
        super(testWFAdaptations, self).test_pm_Validate_workflowAdaptations_added_no_publication()

    def test_pm_WFA_no_publication(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        # we have a 'published' state in self.meetingConfig2
        self.meetingConfig = self.meetingConfig2
        super(testWFAdaptations, self).test_pm_WFA_no_publication()

    def test_pm_WFA_no_proposal(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        super(testWFAdaptations, self).test_pm_WFA_no_proposal()
        self.meetingConfig = self.meetingConfig2
        super(testWFAdaptations, self).test_pm_WFA_no_proposal()

    def test_pm_WFA_pre_validation(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        super(testWFAdaptations, self).test_pm_WFA_pre_validation()
        self.meetingConfig = self.meetingConfig2
        super(testWFAdaptations, self).test_pm_WFA_pre_validation()

    def test_pm_WFA_pre_validation_keep_reviewer_permissions(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        super(testWFAdaptations, self).test_pm_WFA_pre_validation_keep_reviewer_permissions()
        self.meetingConfig = self.meetingConfig2
        super(testWFAdaptations, self).test_pm_WFA_pre_validation_keep_reviewer_permissions()

    def test_pm_WFA_creator_initiated_decisions(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py
           In MC WFs this wfAdaptation is not used (deactivated in adapters.py) because it is
           always 'enabled', the creator can edit the decision field by default.'''
        # we just call the subtest while wfAdaptation should be active
        super(testWFAdaptations, self)._creator_initiated_decisions_active()

    def test_pm_WFA_items_come_validated(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        super(testWFAdaptations, self).test_pm_WFA_items_come_validated()
        self.meetingConfig = self.meetingConfig2
        super(testWFAdaptations, self).test_pm_WFA_items_come_validated()

    def test_pm_WFA_archiving(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        # we do not have an 'archived' state in the meeting/item WFs...
        # just call the subtest while wfAdaptation sould be inactive
        # it is deactived in adapters.py
        super(testWFAdaptations, self)._archiving_inactive()

    def test_pm_WFA_only_creator_may_delete(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        super(testWFAdaptations, self).test_pm_WFA_only_creator_may_delete()
        self.meetingConfig = self.meetingConfig2
        super(testWFAdaptations, self).test_pm_WFA_only_creator_may_delete()

    def test_pm_WFA_no_global_observation(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        # we have a 'published' state in self.meetingConfig2
        # once item is 'itempublished'
        self.meetingConfig = self.meetingConfig2
        super(testWFAdaptations, self).test_pm_WFA_no_global_observation()

    def test_pm_WFA_everyone_reads_all(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        self.meetingConfig = self.meetingConfig2
        super(testWFAdaptations, self).test_pm_WFA_everyone_reads_all()

    def test_pm_WFA_creator_edits_unless_closed(self):
        '''See doc in PloneMeeting/tests/testWFAdaptations.py'''
        super(testWFAdaptations, self).test_pm_WFA_creator_edits_unless_closed()
        self.meetingConfig = self.meetingConfig2
        super(testWFAdaptations, self).test_pm_WFA_creator_edits_unless_closed()

    def test_pm_WFA_decide_item_when_back_to_meeting_from_returned_to_proposing_group(self):
        cfg = self.meetingConfig
        if 'decide_item_when_back_to_meeting_from_returned_to_proposing_group' not in cfg.listWorkflowAdaptations():
            pm_logger.info('test_pm_WFA_decide_item_when_back_to_meeting_from_returned_to_proposing_group: '
                           'Bypassing test as wfAdaptation is not available!')
            return
        super(testWFAdaptations, self).test_pm_WFA_decide_item_when_back_to_meeting_from_returned_to_proposing_group()
        self.changeUser('pmManager')
        folder = self.getMeetingFolder()
        item = folder.objectValues('MeetingItem')[0]
        self.assertEqual('accepted_but_modified', item.queryState())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWFAdaptations, prefix='test_pm_'))
    return suite
