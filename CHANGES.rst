Products.MeetingCommunes Changelog
==================================

Older versions than 3.0 can be found at http://svn.communesplone.org/svn/communesplone/MeetingCommunes/tags/
The Products.MeetingCommunes version must be the same as the Products.PloneMeeting version

4.1b3 (unreleased)
------------------

- Hide 'searchvalidateditems' to power observers (restricted included)
- In profile 'examples_fr', enable WFAdaptations 'presented_item_back_to_itemcreated' and 'presented_item_back_to_proposed'
- In profile 'examples_fr', enable relevant transitions to confirm
- In profile 'examples_fr', enable 'groups_in_charge' for 'Secrétariat Général' and configure auto asked advice for it
- In profile 'examples_fr', enable 'MeetingItem.manuallyLinkedItems' field
- In profile 'examples_fr', enable 'Agenda with annexes' by default

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
