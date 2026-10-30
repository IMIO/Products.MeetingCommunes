# CLAUDE.md — Products.MeetingCommunes

## What is this project?

Products.MeetingCommunes is a **PloneMeeting extension** that provides meeting management profiles specifically for Belgian local authorities (communes). It configures workflows, categories, document templates, and financial advice processes for communal colleges, councils, and specialized committees.

It does **not** define its own content types — it customizes Products.PloneMeeting objects through **Zope adapters** and **GenericSetup profiles**.

Part of the **iMio** ecosystem, commercially known as **iA.Delib**.

## Tech stack

Same as Products.PloneMeeting:

- **Python 2.7** on **Plone 4.3** (Zope 2)
- Build system: **zc.buildout** (extends `buildout.pm`)
- Document generation: **appy** (ODT/POD templates)
- Search/dashboard: **eea.facetednavigation** + `collective.eeafaceted.dashboard`

Dependencies: `Products.PloneMeeting`, `Products.CMFPlone`, `Pillow`

## Repository layout

```
src/Products/MeetingCommunes/
  config.py               # Constants: finance groups, advice states, portal categories
  interfaces.py           # Workflow action/condition interfaces, browser layer
  adapters.py             # Core: Custom* adapters + workflow adapters + search filters
  utils.py                # Utility functions (memoized helpers)
  setuphandlers.py        # GenericSetup import handlers (postInstall, profile detection)
  testing.py              # Test layers (MC_TESTING_PROFILE_FUNCTIONAL, etc.)
  browser/
    overrides.py          # Document generation helpers (MCItem/Meeting/FolderDocumentGenerationHelperView)
    configure.zcml        # Browser view registrations on IMeetingCommunesLayer
  model/
    pm_updates.py         # Schema extensions to MeetingConfig (e.g. initItemDecisionIfEmptyOnDecide)
  migrations/             # Upgrade steps (migrate_to_4_1, migrate_to_4200)
  profiles/               # 33 GenericSetup profiles (see below)
  tests/                  # ~30 test modules
  locales/                # Translation overrides (loaded before PloneMeeting's)
```

## Architecture: adapter pattern

All customization goes through Zope adapters registered in `configure.zcml`. No PloneMeeting code is patched.

**Model adapters** (extend PloneMeeting objects with commune-specific behavior):
- `CustomMeeting` → `IMeetingCustom` — printing helpers (getPrintableItems, etc.)
- `CustomMeetingItem` → `IMeetingItemCustom`
- `CustomMeetingConfig` → `IMeetingConfigCustom` — finance configuration
- `CustomToolPloneMeeting` → `IToolPloneMeetingCustom`

**Workflow adapters** (implement custom workflow transitions/guards):
- `MeetingCommunesWorkflowActions/Conditions` (for `IMeeting`)
- `MeetingItemCommunesWorkflowActions/Conditions` (for `IMeetingItem`)
- `MeetingAdviceCommunesWorkflowActions/Conditions` (for `IMeetingAdvice`)

**Search filter adapters** (`ICompoundCriterionFilter`):
- Completeness checks, finance advice state filters (created → controller → editor → reviewer → manager → signed)

## GenericSetup profiles

- **default** — base profile
- **testing** — test configuration
- **demo** / **examples_fr** — demo data
- **simple** — minimal configuration
- **financesadvice** — financial advice workflow extension
- **z\*** (25+ profiles) — organization-specific: `zca` (advisory committee), `zbdc` (strategic committee), `zcpas` (social action center), `zones` (police/help zones), `zbourgmestre` (mayor), etc.

Each organization profile contains: `import_data.py` (MeetingConfig), `templates/` (ODT), `images/` (logos), and a marker file for profile detection.

## Building & running

From the buildout root (`pm42_dev/`):

```bash
bin/buildout              # Build/install
bin/instance fg           # Run Plone in foreground
```

## Running tests

From the buildout root (`pm42_dev/`):

```bash
bin/testmc                                        # All MeetingCommunes tests
bin/testmc -t testCustomMeetingItem               # Single test module
bin/testmc -t testCustomMeetingItem.test_method    # Single test method
```

Some tests require LibreOffice for document conversion (`OO_SERVER=localhost OO_PORT=2002`).

### Test architecture

- Base class: `MeetingCommunesTestCase` (extends `PloneMeetingTestCase` + `MeetingCommunesTestingHelpers`)
- Layer: `MC_TESTING_PROFILE_FUNCTIONAL`
- Test profile: `Products.MeetingCommunes:testing`
- Meeting configs in tests: `self.cfg1_id = 'meeting-config-college'`, `self.cfg2_id = 'meeting-config-council'`
- Ignored test files: `test_robot.py`, `testPerformances.py`, `testContacts.py`

Test modules follow PloneMeeting's pattern — most inherit from PloneMeeting test classes and override with commune-specific behavior.

## Code style & conventions

Follows Products.PloneMeeting conventions:

- **Encoding header**: `# -*- coding: utf-8 -*-` on every `.py` file
- **License header**: GPL block at top of every file
- **Imports**: single-line, alphabetically sorted (`isort` with `force_single_line = True`)
- **Line length**: 200 characters max
- **Naming**: `PascalCase` classes, `snake_case` functions, `UPPER_SNAKE_CASE` constants
- **Security**: `AccessControl.ClassSecurityInfo` declarations on class methods
- **i18n**: `from Products.PloneMeeting.config import PMMessageFactory as _` — wrap translatable strings with `_()`
- **Python 3 compat**: write compatible code where possible (`from __future__ import`, use `six`)

## Commit message style

Short imperative sentence. Reference issues with `#NNN` (GitHub PR) or `#PROJECT-NNN` (external tracker). Examples:

```
Fixed actions_panel cache issue for reviewers (#42)
Added new finance advice workflow state (#SUP-50375)
```

## Changelog

Update `CHANGES.rst` for every user-facing change. Format:

```rst
- Description of change with `backtick-quoted` code references.
  [author_shortname]
```

## Financial advice workflow

A key feature of this product. Adds a multi-step financial review process with 5 group suffixes:
`financialprecontrollers` → `financialcontrollers` → `financialeditors` → `financialreviewers` → `financialmanagers`

Configured via the `financesadvice` profile and `ADVICE_STATES_MAPPING` in `config.py`.
