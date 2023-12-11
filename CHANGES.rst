
Products.MeetingCommunes Changelog
==================================

The Products.MeetingCommunes version must be the same as the Products.PloneMeeting version


4.2.6b4 (2023-12-11)
--------------------

- CSS, color in blue state `financial_advice_signed` in advice history.
  [gbastien]
- Adapted code as `ToolPloneMeeting.getUserName` is replaced by
  `imio.helpers.content.get_user_fullname` and
  `ToolPloneMeeting.isPowerObserverForCfg` is moved to
  `utils.isPowerObserverForCfg`.
  [gbastien]
- Added translations for the `add_advicecreated_state` WFA.
  [gbastien]

4.2.6b3 (2023-11-27)
--------------------

- Added parameter `ignore_advice_hidden_during_redaction=False` to
  `CustomMeetingItem.showFinanceAdviceTemplate`, when `True`, this will hide
  the POD template when advice is hidden during redaction except if member is
  `MeetingManager` or in the advice `_advisers` group.
  [gbastien]

4.2.6b2 (2023-11-27)
--------------------

- Move back `add_advicecreated_state` advice WFA related code from `PloneMeeting`.
  [gbastien]
- Fixed `meetingadvicefinancs` `portal_type.allowed_content_types` install.
  [gbastien]
- Completed translations of finances advices types.
  [gbastien]

4.2.6b1 (2023-10-27)
--------------------

- Adapted code now that custom advice portal_types is managed by
  `ToolPloneMeeting.advisersConfig`:

  - Added new advice finances WF `meetingadvicefinancessimple_workflow`;
  - Fixed tests as `MeetingConfig.listWorkflowAdaptations` was removed.

  [gbastien]

4.2.5 (2023-10-27)
------------------

- Call `PloneMeeting` migration to `4210` in MC migration to `4200`.
  [gbastien]

4.2.4 (2023-09-12)
------------------

- Updated `attendance-stats.ods`.
  [gbastien]
- Fixed `CustomMeetingConfig.getUsedFinanceGroupIds` to work when an item has
  both inheritated and not inheritated advices, it was using the wrong
  `MeetingConfig` in some cases.
  [gbastien]
- Call `PloneMeeting` migration to `4208` in MC migration to `4200`.
  [gbastien]
- Call `PloneMeeting` migration to `4209` in MC migration to `4200`.
  [gbastien]
- Adapted `examples_fr` import_data as `MeetingConfig.useCopies` was removed.
  [gbastien]

4.2.3 (2023-07-07)
------------------

- Removed confusing `transition_done_descr` translations
  (portal message displayed after a transition).
  [gbastien]
- Added translations for `create_to_bourgmestre_from_meeting-config-college`
  and `create_to_bourgmestre_from_meeting-config-college_comments`.
  [gbastien]
- Updated link to the documentation.
  [gbastien]

4.2.2 (2023-06-27)
------------------

- Call PloneMeeting migrations to 4206 and 4207 in MC migration to 4200.
  [gbastien]

4.2.1 (2023-05-31)
------------------

- Fixed `zbougmestre` profile `shortName` from wrong `AG` to `Bourgmestre`.
  [gbastien]

4.2 (2023-03-06)
----------------

- Removed useless import of `get_cachekey_volatile` in `adapters.py`.
  [gbastien]
- Fixed POD template `avis-df.odt` in `examples_fr` profile.
  [gbastien]
- Make `CustomMeetingConfig.getUsedFinanceGroupIds` work with item sent to
  another MC with inheritated advices.
  [gbastien]
- Advices is no more using Plone versioning, removed `repositorytool.xml`
  from `financesadvice` profile (migration is managed by `Products.PloneMeeting`).
  [gbastien]
- Added collection `searchadvicesbacktoitemvalidationstates` using
  `CompoundCriterion` adapter `items-with-advice-back-to-item-validation-states`
  to get items having finances advice that are return in item validation states.
  [gbastien]
- Adapted code regarding removal of `MeetingConfig.useGroupsAsCategories`.
  [gbastien]

4.2b24 (2022-09-29)
-------------------

- Removed wrong ramcache cachekey for `CustomToolPloneMeeting.isFinancialUser`.
  Removed ramcache decorator for it, finally useless.
  [gbastien]

4.2b23 (2022-09-22)
-------------------

- Fixed `examples_fr` profile.
  [gbastien]

4.2b22 (2022-08-26)
-------------------

- Rename "Commission des volontaires" profile to "Bureau des volontaires".
  [aduchene]
- Add helper print method to be able to group by custom method instead of persistent value on item.
  This method must begin by "_group_by_".
  [anuyens, gbastien]
- Field `MeetingConfig.transitionsForPresentingAnItem` was removed, adapted profiles accordingly.
  [gbastien]
- In `MeetingCommunesWorkflowActions.doDecide`, call parent's `doDecide`.
  [gbastien]
- Call migrations to `PloneMeeting 4203 and 4204` in migration to `MeetingCommunes 4200`.
  [gbastien]
- In migration to 4200, removed replace `print_deliberation` by
  `print_full_deliberation` as this last method was removed.
  [gbastien]
- Adapted code now that we use `imio.helpers.cache.get_plone_groups_for_user`
  instead `ToolPloneMeeting.get_plone_groups_for_user`.
  [gbastien]

4.2b21 (2022-06-14)
-------------------

- Add user FS in examples_fr profile.
  [odelaere]
- By default enable the `FINANCE_ADVICES_COLLECTION_ID` collection
  for `meeting-config-zcollege`.
  [gbastien]

4.2b20 (2022-05-17)
-------------------

- Redo release, zest.releaser had set version to 4.2b110...
  [gbastien]

4.2b110 (2022-05-17)
--------------------

- Call migration to `PloneMeeting 4202` in migration to `MeetingCommunes 4200`.
  [gbastien]

4.2b19 (2022-05-16)
-------------------

- Adapt import-csv-inforius.py for MC 4.2.
  [odelaere]
- Fixed `oj-avec-annexes.odt` (`imageOrientation` is now `image_orientation`).
  [gbastien]
- Extended `Migrate_To_4200._adaptWFHistoryForItemsAndMeetings` and renamed it to
  `Migrate_To_4200._adaptWFDataForItemsAndMeetings` as it will also take care to
  migrate `MeetingItem.takenOverByInfos` where the key contains the workflow name.
  [gbastien]
- Do not fail in `CustomMeetingConfig.getUsedFinanceGroupIds` if the collection
  is not enabled, just log a message and return an empty result.
  [gbastien]

4.2b18 (2022-04-28)
-------------------

- Take into account fact that `Migrate_To_4200` may be executed `by parts (a, b, c)`.
  [gbastien]
- Do not redefine `MeetingItemCommunesWorkflowConditions.__init__` as parent
  (`MeetingItemWorkflowConditions`) defines more.
  [gbastien]

4.2b17 (2022-03-22)
-------------------

- Optimized POD template `meeting_assemblies.odt`, use `catalog` available by
  default in the template context instead `self.portal_catalog`.
  [gbastien]
- Call migration to `PloneMeeting 4201` in migration to `MeetingCommunes 4200`.
  [gbastien]

4.2b16 (2022-01-07)
-------------------

- Fixed `MeetingAdviceCommunesWorkflowConditions._check_completeness`, call
  `_is_complete` on the parent (`MeetingItem`).
  [gbastien]

4.2b15 (2022-01-03)
-------------------

- Added two examples in attendees.odt template.
  [aduchene]
- Fixed `council-rapport.odt`, `MeetingItem.listProposingGroups` does not exist anymore.
  [gbastien]

4.2b14 (2021-11-26)
-------------------

- Fixed print_formatted_finance_advice as it was not handling initiative advices properly.
  [aduchene]

4.2b13 (2021-11-08)
-------------------

- Fixed `MCItemDocumentGenerationHelperView.print_all_annexes` to not return
  `</img>` as `<img>` is a self closing tag.
  [gbastien]
- Fixed sample POD templates for meetings to use `view.print_value('date')`
  instead `self.Title()`.
  [gbastien]

4.2b12 (2021-10-13)
-------------------

- In `MCItemDocumentGenerationHelperView.print_creator_name` use
  `ToolPloneMeeting.getUserName` instead `Member.getProperty`.
  [gbastien]

4.2b11 (2021-09-09)
-------------------

- Updated avis-df.odt template to have default value.
  [aduchene]
- Added a `IMeetingCommunesLayer BrowserLayer` so it is possible to override
  PloneMeeting's documentgenerator views without using `overrides.zcml`.
  [gbastien]
- Removed overrided method `CustomMeetingItem._is_complete` as it is the same
  implementation in `Prodducts.PloneMeeting.MeetingItem`.
  [gbastien]

4.2b10 (2021-07-16)
-------------------

- Added new external method to ease the switch to proposingGroupWithGroupInCharge.
  [odelaere]
- Added 2 new profiles `zcodir_extended` and `zcodir_city_cpas`.
  [aduchene]
- Removed default values defined for DashboardCollections `FINANCE_ADVICES_COLLECTION_ID`
  and `searchitemswithnofinanceadvice`, because if it does not exist in the
  `MeetingConfig.customAdvisers`, it breaks the dashboards when applying the profile.
  [gbastien]
- When using finances advice workflows, WF `initial_state` may vary
  (`advicecreated`, `proposed_to_financial_controller`, ...) so when using
  completeness, check that item is complete until the
  `mayProposeToFinancialReviewer` transition guard.
  [gbastien]
- Added `CustomMeetingConfig._setUsedFinanceGroupIds` to ease definition of
  advisers value for the `FINANCE_ADVICES_COLLECTION_ID` collection.
  [gbastien]
- Added PORTAL_CATEGORIES in config.py
  [odelaere]
- Added new listTypes normalnotpublishable and latenotpublishable used in portal.
  [odelaere]
- Adapted `zcity/zcommittee_advice` profiles as advice type `asked_again` is no more optional.
  [gbastien]
- Renamed parameter `listTypes` to `list_types` everywhere.
  [gbastien]
- Moved some methods to snake_case : `printFinanceAdvice/print_finance_advice`,
  `printAllAnnexes/print_all_annexes`, `printFormatedAdvice/print_formated_advice`.
  [gbastien]
- Adapted behavior of `get_grouped_items` with `unrestricted=True` that originally
  returned every items ignoring `itemUids`, it was not possible to print a subset
  of items.  Now if length of `itemUids` is smaller than len of all visible items,
  we only return these items.
  [gbastien]
- Adapted `MCItemDocumentGenerationHelperView.print_item_number_within_category`
  as `MeetingItem.getCategory` does no more return the `proposingGroup` when
  `MeetingConfig.useGroupsAsCategories` is True.
  [gbastien]
- Fixed signature of `MCItemDocumentGenerationHelperView.print_deliberation`.
  [gbastien]
- Added a new DashboardPODTemplate `export-users-groups.ods` in contacts directory.
  [aduchene]
- Improved CustomMeeting.getNumerOfItems using Meeting.getItems.
  [odelaere]
- Improved MCItemDocumentGenerationHelperView.print_all_annexes with filters, icon, better escaping, etc.
  [odelaere]

4.2b9 (2021-01-26)
------------------

- Added 2 mores formatting examples for `view.print_attendees_by_type` in
  `attendees.odt` template.
  [aduchene]
- Changed uppercases in example_fr profile for `directory_position_types`.
  [aduchene]
- Fixed `MeetingItemCommunesWorkflowActions._doWaitAdvices`, make sure
  `MeetingItem.completeness` is set to `completeness_evaluation_asked_again`
  when advices are asked for the second time (or more).
  [gbastien]
- Adpated code and tests regarding fact that `Meeting` was moved from `AT` to `DX`.
  [gbastien]

4.2b8 (2021-01-06)
------------------

- Added POD template that renders various votes on item.
  [gbastien]
- Do no more ignore testVotes when executing tests.
  [gbastien]
- Fixed demo profile, items containing annexes were broken because id is
  changed after `categorized_elements` is updated.
  [gbastien]

4.2b7 (2020-11-19)
------------------

- Fixed a bug in `getPrintableItemsByCategory` (incorrect method call, categories are now in DX).
  [aduchene, gbastien]
- Added `testCustomMeeting.test_GetPrintableItemsByCategoryWithBothLateItems`,
  moved from `Products.MeetingCharleroi`.
  [gbastien]
- Fixed `Migrate_To_4200`, call `addNewSearches` at the end because it needs
  `_adaptWFHistoryForItemsAndMeetings` to have been called in the
  `_after_reinstall` hook to have correct workflows.
  [gbastien]

4.2b6 (2020-10-27)
------------------

- Added `zcsss` profile to add CSSS MeetingConfig.
  [gbastien]
- Added missing translation for `searchadvicesignedbymanager`.
  [gbastien]

4.2b5 (2020-10-14)
------------------

- By default use finance `advice_type` for every advice `portal_types`
  that starts with `meetingadvicefinances`.
  [gbastien]

4.2b4 (2020-10-02)
------------------

- Simplified translation for `MeetingAdviceCommunesWorkflowConditions.mayProposeToFinancialManager`
  `No` message `still_asked_again`.
  [gbastien]
- Fixed `contactsTemplate` dashboard POD template in `examples_fr` profile, set `use_objects=True`.
  [gbastien]
- Added default `directory_position_types` and `contactsTemplates` for `zcpas` profile.
  [gbastien]
- Added translation for `completeness_set_to_not_required_by_app`.
  [gbastien]
- Added collection `searchadvicesignedbymanager` using `CompoundCriterion` adapter
  `items-with-advice-signed-by-financial-manager` to get items having finances advice
  in state `financial_advice_signed`.
  [gbastien]

4.2b3 (2020-09-10)
------------------

- Fixed `MCMeetingDocumentGenerationHelperView.get_grouped_items` when using
  `excluded_values/included_values` parameters together with `unrestricted=True`,
  unrestricted was not propagated to sub methods giving nonsense results.
  [gbastien]
- Added parameter `additional_catalog_query={}` to
  `MCMeetingDocumentGenerationHelperView.get_grouped_items` making it possible
  to pass additional traditional portal_catalog query to filter items.
  [gbastien]

4.2b2 (2020-09-07)
------------------

- Added collection `searchitemswithnofinanceadvice` that will use `CompoundCriterion` adapter
  `items-with-negative-previous-index` to get items for which finances advice was not asked.

4.2b1 (2020-08-24)
------------------

- Added translations for `completeness_not_complete` and `still_asked_again` WF transition button messages.
- Merged changes from 4.1.15
- Adapted profile `zbdc` as `workflowAdaptations` changed.

4.2a4 (2020-06-24)
------------------

- Merged changes from 4.1.9
- Merged changes from 4.1.10
- Merged changes from 4.1.11
- Merged changes from 4.1.12
- Merged changes from 4.1.13
- Merged changes from 4.1.14

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

4.2a3 (2020-03-13)
------------------

- Merged changes from 4.1.8

4.1.8 (2020-03-12)
------------------

- Added ICompoundCriterion adapter `all-items-to-control-completeness-of` based on `items-to-control-completeness-of but`
  that will query every finances advice, not only delay aware advices
- Updated styles1.odt to add CKEditor's styles
- Added some more usecases with abbreviated firstname in attendees.odt

4.2a2 (2020-02-21)
------------------

- Merged changes from 4.1.x

4.2a1 (2020-02-06)
------------------

- Adapted item workflow to use MeetingConfig.itemWFValidationLevels defined configuration
- Added new 'meetingadvice' related workflows : 'meetingadvicefinanceseditor_workflow' and 'meetingadvicefinancesmanager_workflow'
- MeetingConfig.itemDecidedStates and MeetingConfig.itemPositiveDecidedStates fields were removed, adapted import_data files accordingly

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
