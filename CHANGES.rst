Products.MeetingCommunes Changelog
==================================

The Products.MeetingCommunes version must be the same as the Products.PloneMeeting version

4.1.21 (2021-02-12)
-------------------

- Added `testCustomMeeting.test_GetPrintableItemsByCategoryWithBothLateItems`,
  moved from `Products.MeetingCharleroi`.
  [gbastien]
- Backport from 4.2.x:

  - Added 2 mores formatting examples for `view.print_attendees_by_type` in `attendees.odt` template
    [aduchene]
  - Fixed `MCMeetingDocumentGenerationHelperView.get_grouped_items` when using
    `excluded_values/included_values` parameters together with `unrestricted=True`,
    unrestricted was not propagated to sub methods giving nonsense results.
    [gbastien]
  - Added parameter `additional_catalog_query={}` to
    `MCMeetingDocumentGenerationHelperView.get_grouped_items` making it possible
    to pass additional traditional portal_catalog query to filter items.
    [gbastien]

- Changed uppercases in example_fr profile for `directory_position_types`
  [aduchene]
- Added new external method to ease the switch to proposingGroupWithGroupInCharge.
  [odelaere]

4.1.20 (2020-10-29)
-------------------

- Fixed a bug in `getPrintableItemsByCategory` (incorrect method call, categories are now in DX).
  [aduchene, gbastien]

4.1.19 (2020-10-26)
-------------------

- Added `zcsss` profile to add CSSS MeetingConfig.
  [gbastien]

4.1.18 (2020-10-14)
-------------------

- Added import script from Workflow Lux.
  [odelaere]


4.1.17 (2020-10-01)
-------------------

- Backport from 4.2.x:
  Fixed `contactsTemplate` dashboard POD template in `examples_fr` profile, set `use_objects=True`.
  [gbastien]
  Added default `directory_position_types` and `contactsTemplates` for `zcpas` profile.
  [gbastien]

4.1.16 (2020-09-23)
-------------------

- Call migrations to PloneMeeting 4108, 4109, 4110, 4111 in migration to MeetingCommunes 4.1.
  [gbastien]

4.1.15 (2020-08-21)
-------------------

- Fix translations for `MeetingExecutive`.
  [vpiret]
- Add BDC Profiles
  [anuyens]
- Add missing translations for MeetingAudit.
  [anuyens]
- Added translations for actions `sent to` from `College/BP` to `CoDir`.
  [gbastien]
- Define style `page-break` in `deliberation.odt` POD template.
  [gbastien]
- Added more `position_types` by default (secretaire) in `examples_fr` profile.
  [gbastien]

4.1.14 (2020-06-24)
-------------------

- Added `import_organizations_from_csv` to be able to import organizations from a CSV file.
  [gbastien]
- In `import_meetingsUsersAndRoles_from_csv` take into account `id` if given (fallback to normalized title if not)
  and manage extra columns `groupsInCharge`, `usingGroups` and `actif` (WF state).
  [gbastien]
- Added more `position_types` by default (first alderman to sixth alderman) in `examples_fr` profile.
  [gbastien]

4.1.13 (2020-06-11)
-------------------

- Added some methods to print an item number in different ways.
  [aduchene]

4.1.12 (2020-05-28)
-------------------

- Call migration to PloneMeeting 4107 in migration to MeetingCommunes 4.1.
  [gbastien]
- Do not use relative path to define icon path of ItemAnnexTypeDescriptor.
  [gbastien]

4.1.11 (2020-05-14)
-------------------

- Call migration to PloneMeeting 4106 in migration to MeetingCommunes 4.1.
  [gbastien]

4.1.10 (2020-04-24)
-------------------

- Added force-language external method.
  [odelaere]
- Call migration to PloneMeeting 4105 in migration to MeetingCommunes 4.1.
  [gbastien]

4.1.9 (2020-04-02)
------------------

- Fixed `all-items-to-control-completeness-of` ICompoundCriterion adapter.
- Added some example regarding 'Non attendees' in attendees.odt template.

4.1.8 (2020-03-12)
------------------

- Added ICompoundCriterion adapter `all-items-to-control-completeness-of` based on `items-to-control-completeness-of but`
  that will query every finances advice, not only delay aware advices
- Updated styles1.odt to add CKEditor's styles
- Added some more usecases with abbreviated firstname in attendees.odt

4.1.7 (2020-02-18)
------------------

- Overrided print_deliberation to include specific content
- Added MCItemDocumentGenerationHelperView.print_formatted_finance_advice to print finance advice
- Reintegrated CustomMeeting.getPrintableItemsByCategory waiting for another solution to be able to print empty categories
- Call migration to PloneMeeting 4104 in migration to MeetingCommunes 4.1
- Adapted examples_fr import_data as 'searchalldecisions' was renamed to 'searchallmeetings'
- Added parameter unrestricted=False to MCMeetingDocumentGenerationHelperView.get_grouped_items
  so it is possible to get every items of a meeting, even items current user may not access

4.1.6 (2019-11-26)
------------------

- Fixed CSS class regarding changes in imio.prettylink

4.1.5 (2019-11-19)
------------------

- Launch Products.PloneMeeting upgrade step to 4103 in migration to v4.1

4.1.4 (2019-11-04)
------------------

- The format of MeetingConfigDescriptor.defaultLabels changed, adapted import_data accordingly
- Launch Products.PloneMeeting upgrade step to 4102 in migration to v4.1

4.1.3 (2019-10-14)
------------------

- Update PODTemplates in examples_fr profile to uses new methods from PloneMeeting
- Added missing portal_types translations for the zcommittee_advice profile, do not set it as default on install neither
- Adapted workflowstate viewlet CSS regarding changes in plonetheme.imioapps
- Added bourgmestreff-president in contact position types

4.1.2 (2019-10-04)
------------------

- Wrong release

4.1.1 (2019-10-04)
------------------

- Call migration to Products.PloneMeeting 4100 and 4101 after applying migration to 4.1

4.1 (2019-09-13)
----------------

- Wrong release

4.1.dev0 (2019-09-13)
---------------------

- Fix modification date on imported meetings and items in import-csv-civadis.py
  [odelaere]

4.1rc9 (2019-09-12)
-------------------

- Use base implementation of MeetingWorkflowConditions.mayDecide as it does the same now (just check "Review portal content" permission)
- MeetingConfig.onMeetingTransitionItemTransitionToTrigger was moved to MeetingConfig.onMeetingTransitionItemActionToExecute, adapted code accordingly

4.1rc8 (2019-08-23)
-------------------

- Fixed POD templates using oj-avec-annexes.odt that failed to render late items
- In profile zcity, use same directory_position_types as in profile examples_fr
- Run Products.PloneMeeting upgrade step to 4100 after upgraded to 4.1

4.1rc7 (2019-08-13)
-------------------

- When applying 'meetingadvicefinances_add_advicecreated_state' WF adaptation, set advicecreated state as new_initial_state
- In query_itemstocontrolcompletenessof, do not use the config.FINANCE_WAITING_ADVICES_STATES but compute the states in which advice
  can be given by finances groups
- Override MeetingItem._adviceTypesForAdviser to manage finances specific advice types
- Get rid of config.FINANCE_WAITING_ADVICES_STATES, get those states dynamically using utils.finances_give_advice_states

4.1rc6 (2019-07-02)
-------------------

- Make sure to update contacts directory position_types if only the 'default' position type is defined while migrating to v4.1
- Added new finances advice search compoundcriterion adapter ItemsWithAdviceAdviceCreatedAdapter to search items having advice in state 'advicecreated'
- When using MeetingItem.completeness, set automatically completeness to 'completeness_evaluation_asked_again' when advices are asked
- Define config.FINANCE_WAITING_ADVICES_STATES=[] by default so it does not do anything if not overrided

4.1rc5 (2019-07-01)
-------------------

- Be defensive in CustomMeetingConfig.getUsedFinanceGroupIds if FINANCE_ADVICES_COLLECTION_ID does not have a
  'indexAdvisers' filter or if 'indexAdvisers' filter is empty

4.1rc4 (2019-07-01)
-------------------

- Added translations for 'meetingadvicefinances_workflow' WF adaptations

4.1rc3 (2019-06-28)
-------------------

- Added 'conseiller', 'depute' and 'conseiller-president' in examples_fr import_data directory_position_types
- Added sample view.print_attendees_by_type(group_position_type=True, render_as_html=True, ignored_pos_type_ids=[]) to attendees POD template
  to show how it works to display a single held_position label when no position_type is defined on some held_positions and we use group_position_type=True
- Added wfAdaptation 'meetingadvicefinances_controller_propose_to_manager' that adds transition from 'proposed_to_financial_controller'
  to 'proposed_to_financial_manager'
- Added helper method CustomMeetingConfig._has_meetingadvicefinances_wf_adaptations that returns True if some finances advice related
  workflow adaptations are selected, this will trigger the fact that 'patched_meetingadvicefinances_workflow' is created
- In financesadvice_workflow, Manage MeetingItem.completeness in mayProposeToFinancialController so an item that needs completeness evaluation
  can not be proposed to financial controller
- Remove import_step calling setuphandlers.updateRoleMappings
- Adapted code to use MeetingItem.getGroupsInCharge(first=True) instead MeetingItem.getGroupInCharge that was removed

4.1rc2 (2019-06-14)
-------------------

- Take into account new parameter extra_omitted passed to Migrate_To_4_1.run

4.1rc1 (2019-06-11)
-------------------

- Adapted 'meetingadvicefinances_workflow' to use MeetingAdviceCommunesWorkflowActions/MeetingAdviceCommunesWorkflowConditions
  instead the '@@advice-wf-conditions' view
- Added workflow adaptation for the meetingadvicefinances_workflow to add the 'advicecreated' intial state
- Adapted finances advice workflow to use dexterity.localrolesfield

4.1b3 (2019-05-16)
------------------
- Hide 'searchvalidateditems' to power observers (restricted included)
- Updated decide_item_when_back_to_meeting_from_returned_to_proposing_group decided state to 'accept_but_modify' instead of 'accept' (from PloneMeeting)
- In profile 'examples_fr', enable WFAdaptations 'presented_item_back_to_itemcreated' and 'presented_item_back_to_proposed'
- In profile 'examples_fr', enable relevant transitions to confirm
- In profile 'examples_fr', enable 'groups_in_charge' for 'Secrétariat Général' and configure auto asked advice for it
- In profile 'examples_fr', enable 'MeetingItem.manuallyLinkedItems' field
- In profile 'examples_fr', enable 'Agenda with annexes' by default
- Adapted code regarding MeetingConfig.powerObservers
- Enabled wfAdaptation 'only_creator_may_delete' by default for profiles 'examples_fr' and 'simple'
- Added JenkinsFile for CI triggers
- PloneMeeting's MeetingWorkflowConditions was simplified, no need to redefine mayCorrect anymore
- Give 'Review portal content' permission to MeetingManager in Meeting WF in state 'closed' as it is now possible for
  MeetingManagers to correct a closed meeting depending on MeetingConfig.meetingPresentItemWhenNoCurrentMeetingStates
- Make test test_pm_ObserversMayViewInEveryStates easier to override by plugins
- Added standard install profile for city

4.1b2 (2019-01-29)
------------------

- Fix profile, 'item_reference' was renamed to 'static_item_reference' for MeetingConfig.itemsListVisibleColumns
- Changed default tal_condition for searchproposeditems DashboardCollection to only display it if current user is a creator
- Adapted code to user imio.history.utils.getLastWFAction instead Products.PloneMeeting.utils.getLastEvent

4.1b1 (2018-12-04)
------------------

- Do not call at_post_edit_script directly anymore, use Meeting(Item)._update_after_edit
- Adapted default 'deliberation.odt' to no more use global margin and integrate printAllAnnexes
- Fix reviewer groups of pmReviewerLevel1 and pmReviewerLevel2 to avoid importing MEETINGREVIEWERS
- Do not use separated 'College'/'Council' interfaces for WF actions and conditions, use 'Communes'
  interfaces in both cases
- Added a "simple" profile that add the most simple configuration possible.  Useable to create a very
  simple configuration or as base for another complex configuration
- Added variables cfg1_id and cfg2_id to MeetingCommunesTestCase, this is used when defining
  meetingConfig and meetingConfig2 attributes of tests and useful for profiles based on MeetingCommunes
- Added helper method to print item number within a category
- Use _addPrincipalToGroup from PloneMeetingTestCase in tests
- DashboardCollection have no more WF but have a 'enabled' field, use it in adapters.getUsedFinanceGroupIds
  to check if finance DashboardCollection is enabled or not
- Added sample Meeting POD template 'attendees' to show various possibilities of printing methods
  'print_attendees' and 'print_attendees_by_type'
- Adapted profiles import_data to select 'description' in usedItemAttributes as MeetingItem.description
  is now an optional field
- Fixed PODTemplateDescriptor definitions in various import_data.py to use correct field type
- Use simpler way to define import_data of testing profile now available in PloneMeeting
- Remove no more used (hopefuly...) CustomMeetingItem.adviceDelayIsTimedOutWithRowId method
- Base MCItemDocumentGenerationHelperView.printFormatedAdvice on MeetingItem.getAdviceDataFor to avoid
  rewriting code and to have every available data
- Use simple profile import_data as base for every secondary profiles (zag, zbourgmestre, ...)
- Adapted profiles import_data usedItemAttributes as MeetingItem.itemAssembly is no more an optional field
- ToolPloneMeeting.getPloneGroupsForUser was renamed to ToolPloneMeeting.get_plone_groups_for_user
- Use a better cachekey for finances advice related searches (cached as long as user/groups/cfg did not changed) 

4.0 (2017-08-04)
----------------
- Adapted workflows to define the icon to use for transitions
- Removed field MeetingConfig.cdldProposingGroup and use the 'indexAdvisers' value
  defined in the 'searchitemswithfinanceadvice' collection to determinate what are
  the finance adviser group ids
- 'getEchevinsForProposingGroup' does also return inactive MeetingGroups so when used
  as a TAL condition in a customAdviser, an inactive MeetingGroup/customAdviser does
  still behaves correctly when updating advices
- Use ToolPloneMeeting.performCustomWFAdaptations to manage our own WFAdaptation 
  (override of the 'no_publication' WFAdaptation)
- Adapted tests, keep test... original PM files to overrides original PM tests and
  use testCustom... for every other tests, added a testCustomWorkflow.py
- Now that the same WF may be used in several MeetingConfig in PloneMeeting, removed the
  2 WFs meetingcollege and meetingcouncil and use only one meetingcommunes where wfAdaptations
  'no_publication' and 'no_global_observation' are enabled
- Added profile 'financesadvice' to manage advanced finances advice using a particular
  workflow and a specific meetingadvicefinances portal_type
- Adapted profiles to reflect imio.annex integration
- Added new adapter method to ease financial advices management while generating documents
  printFinanceAdvice(self, case)
- Added parameter 'excludedGroupIds' to getPrintableItems and getPrintableItemsByCategory
- MeetingObserverLocal has every View-like permissions in every states

3.3 (2015-02-27)
----------------
- Updated regarding changes in PloneMeeting
- Removed profile 'examples' that loaded examples in english
- Removed dependencies already defined in PloneMeeting's setup.py
- Added parameter MeetingConfig.initItemDecisionIfEmptyOnDecide that let enable/disable
  items decision field initialization when meeting 'decide' transition is triggered
- Added MeetingConfig 'CoDir'
- Added MeetingConfig 'CA'
- Field 'MeetingGroup.signatures' was moved to PloneMeeting

3.2.0.1 (2014-03-06)
--------------------
- Updated regarding changes in PloneMeeting
- Moved some translations from the plone domain to the PloneMeeting domain

3.2.0 (2014-02-12)
------------------
- Updated regarding changes in PloneMeeting
- Use getToolByName where necessary

3.1.0 (2013-11-04)
------------------
- Simplified overrides now that PloneMeeting manage this correctly
- Moved 'add_published_state' to PloneMeeting and renamed to 'hide_decisions_when_under_writing'
- Moved 'searchitemstovalidate' topic to PloneMeeting now that PloneMeeting also manage a 'searchitemstoprevalidate' search

3.0.3 (2013-08-19)
------------------
- Added method getNumberOfItems usefull in pod templates
- Adapted regarding changes about "less roles" from PloneMeeting
- Added "demo data" profile
- Refactored tests regarding changes in PloneMeeting

3.0.2 (2013-06-21)
------------------
- Removed override of Meeting.mayChangeItemsOrder
- Removed override of meeting_changeitemsorder
- Removed override of browser.async.Discuss.isAsynchToggleEnabled, now enabled by default
- Added missing tests from PloneMeeting
- Corrected bug in printAdvicesInfos leading to UnicodeDecodeError when no advice was asked on an item

3.0.1 (2013-06-07)
------------------
- Added sample of document template with printed annexes
- Added method to ease pritning of assembly with 'category' of assembly members
- Make printing by category as functionnal as printing without category
- Corrected bug while going back to published that could raise a WorkflowException sometimes

3.0 (2013-04-03)
----------------
- Migrated to Plone 4 (use PloneMeeting 3.x, see PloneMeeting's HISTORY.txt for full changes list)

2.1.3 (2012-09-19)
------------------
- Added possibility to give, modify and view an advice on created item
- Added possibility to define a decision of replacement when an item is delayed
- Added new workflow adaptation to add publish state with hidden decision for no meeting-manager
