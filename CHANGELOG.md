# Changelog

The current version is `metadata.version` in `feature-blueprint/SKILL.md`. Every version is tagged
`vX.Y.Z` in git and published as a GitHub release with its own `.skill` archive. Versions are
numbered MAJOR.MINOR.PATCH.

- **PATCH** (1.0.1) is a fix or clearer wording. The skill behaves the same.
- **MINOR** (1.1.0) is a new or changed rule. Specifications get more or different content.
- **MAJOR** (2.0.0) changes the specification format or how the skill works with the owner, such
  as when it asks, the checkpoint or what counts as the go.

## [1.7.0] - 2026-11-11

### Changed

- Deployment is a fork only when the project leaves a choice. Reconnaissance now finds which
  environments exist, how the project deploys or releases and who starts it. A project with
  nowhere to deploy ends with a local check; a project whose rules set the path follows them; a
  library or a tool gets a question about releasing a version. Before, "where to deploy" was
  asked in every project with a stage server or production as the options (#8).

## [1.6.0] - 2026-11-10

### Changed

- Each question is asked once. When the skill stops before the draft, it asks in the same
  message where to deploy and every owner's fork already clear, and none of them is repeated
  at the checkpoint. Deployment alone does not cause a stop before the draft.
- The checkpoint after the draft does not depend on open forks: it is where the owner sees what
  will be built and agrees. With no fork left, the message is the draft for agreement and one
  question, whether to start (#7).

## [1.5.0] - 2026-11-10

### Changed

- The specification file name starts with the day it was created, in square brackets,
  day.month.year: `[DD.MM.YYYY]-<short-name>.md`, for example `[07.11.2026]-group-disconnect.md`,
  instead of `YYYY-MM-DD-<short-name>.md`. The rule holds in the project's own folder for feature
  documents as well as in `docs/specs/`, and that folder is created if it is missing (#6).

## [1.4.0] - 2026-11-10

### Changed

- If the environment has a source of the owner's earlier decisions in similar situations, the
  forks and the decisions of section 15 are checked against it at step 9, before the design, and
  the blocking questions of step 5 before they are asked. What it settles is the owner's own
  answer: the fork goes to "Accepted" with that ground and is not asked again. After the owner's
  answers the skill hands them to that source. No source is named, and without one the skill
  works as before (#5).

## [1.3.0] - 2026-11-06

### Changed

- In the chat each question to the owner opens on its own line with ❓ and the question itself in
  bold, so it stands out in the long message with "At a glance" and the forks. One mark per
  question; the specification file stays without it (#4).

## [1.2.0] - 2026-11-06

### Changed

- The fresh-agent check also questions how platforms, services and settings are said to behave:
  what a parameter does, when a schedule fires, how two retention rules work together, what can
  change without a restart. A doubted statement is checked in current documentation, then fixed
  or moved to step 0 as [VERIFY]. In the evals most of the skill's serious errors on internal
  mechanisms were of this kind (#3).
- The message to the owner carries "At a glance" copied from the file, every block, "What to
  watch" included, instead of a retelling that drops the risks (#3).
- An error from an external service reaches people as our own text and code; its original text
  goes to the log only (#3).

### Added

- Two eval cases for internal mechanisms: stock and price sync with Ozon inside the shop admin
  project, and backups of a shop on one VPS. A second judging axis grades every submission against
  what an owner who does not write code needs to understand it and decide (#2).
- `run.py run --no-baseline` re-measures a new skill version against baseline runs kept earlier.

## [1.1.0] - 2026-11-06

### Changed

- The specification has no line limit beyond "At a glance" fitting one page. Its scenarios,
  errors, failures and steps set the length. Repetition, the obvious and prose where a table would
  do are still cut, and length alone is never a reason to cut. In the evals a feature inside an
  existing project took about 870 lines, over the old limit of 600.

### Added

- Eval cases are back in `feature-blueprint/evals/`. There are two cases, a Telegram bot idea and
  a price import in a small project. The script `evals/compare/run.py` runs them with this skill,
  with Superpowers and with no skill, and a blind judge grades the results against a list of
  traps written before any run. They are not part of the `.skill` archive (#1).

## [1.0.0] - 2026-11-06

The first numbered version. The skill as it stands after the changes listed below.

### Changed

- Incoming materials go through intake the way the owner's or the project's rules set it. With no
  such rule the agent reads all of them. The skill no longer names the materials-intake skill and
  no longer depends on it (`b676696`).

### Removed

- Eval cases, plans and reports are no longer kept in the repository (`40c8998`).

## Before 1.0.0

Unnumbered changes, by date.

- **2026-11-05.** One checkpoint with the owner. Deployment only as a fork. Statements about the
  project checked against the code. A mechanism nobody asked for is built only when its absence
  harms unnoticed or is costly to add later. What two decisions give together. Earlier attempts
  and unwritten rules of the code. Ideas from Superpowers and Compound Engineering. Mockups and
  diagrams only on request. A small point change gets no specification, file or issue. The skill
  restructured to the Agent Skills best practices (`64f5dcd` to `1743ce9`).
- **2026-11-04.** Agent time never decides a fork. Every important fork goes to the owner. The
  deployment target is agreed upfront. Feature neighbours and entry points. Profile skills first in
  research. The skill in English, its output in the owner's language (`cbc7780` to `f8875de`).
- **2026-11-03.** Decisions grounded in research and sized to the project. Internal mechanisms.
  Questions in plain words (`ea95be2`).
- **2026-11-02.** First version. A raw feature idea becomes an interaction design and an
  implementation plan (`03dba25`).
