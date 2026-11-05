# Changelog

The current version is `metadata.version` in `feature-blueprint/SKILL.md`. Every version is tagged
`vX.Y.Z` in git. Versions are numbered MAJOR.MINOR.PATCH:

- **PATCH** (1.0.1) — a fix or clearer wording; the skill behaves the same.
- **MINOR** (1.1.0) — a new or changed rule; specifications get more or different content.
- **MAJOR** (2.0.0) — a change to the specification format or to how the skill works with the
  owner: when it asks, the checkpoint, what counts as the go.

## [1.0.0] — 2026-11-06

The first numbered version: the skill as it stands after the changes listed below.

### Changed

- Incoming materials go through intake the way the owner's or the project's rules set it; with no
  such rule the agent reads all of them. The skill no longer names the materials-intake skill and
  no longer depends on it (`b676696`).

### Removed

- Eval cases, plans and reports are no longer kept in the repository (`40c8998`).

## Before 1.0.0

Unnumbered changes, by date:

- **2026-11-05** — one checkpoint with the owner; deployment only as a fork; statements about the
  project checked against the code; a mechanism nobody asked for is built only when its absence
  harms unnoticed or is costly to add later; what two decisions give together; earlier attempts
  and unwritten rules of the code; ideas from Superpowers and Compound Engineering; mock-ups and
  diagrams only on request; a small point change gets no specification, file or issue; the skill
  restructured to the Agent Skills best practices (`64f5dcd`…`1743ce9`).
- **2026-11-04** — agent time never decides a fork; every important fork goes to the owner; the
  deployment target agreed upfront; feature neighbours and entry points; profile skills first in
  research; the skill in English, its output in the owner's language (`cbc7780`…`f8875de`).
- **2026-11-03** — decisions grounded in research and sized to the project; internal mechanisms;
  questions in plain words (`ea95be2`).
- **2026-11-02** — first version: a raw feature idea becomes an interaction design and an
  implementation plan (`03dba25`).
