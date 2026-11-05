# feature-blueprint-skill — project rules

- Language: the skill (`feature-blueprint/SKILL.md`, `references/`), the README, the CHANGELOG,
  commit messages and PR titles are in English. The skill makes the agent write its output in the
  owner's language.
- The skill holds the order of work, the owner's rules, the don't-miss lists and the document
  format. It does not re-teach what the model already knows and does not repeat the owner's
  global rules. Each rule says why it exists; an exception is its own condition, not a clause
  inside the rule. Examples go to `references/examples.md`.
- The skill names no other skill and depends on none. Work another skill may do, such as intake of
  incoming materials, is described in general words; the owner maps it to a skill in their own
  rules.
- `SKILL.md` body: at most 500 lines and close to 5,000 tokens (count the body with `tiktoken`
  `o200k_base`). The owner's rules and clear wording come before the number: if they do not fit,
  keep them and say how far over the body is. Details that only one step needs go to
  `references/`, linked straight from `SKILL.md` with when to read them; a reference file over
  100 lines starts with a contents list.
- The frontmatter description stays within 900 characters (the limit is 1024): what the skill
  does and when to use it, the main use first, no summary of the workflow. Use only the fields
  the skill-creator validator accepts.
- Every change to `feature-blueprint/` raises `metadata.version` in `SKILL.md` and adds an entry
  to `CHANGELOG.md` in the same commit, by the rules at the top of the CHANGELOG: a fix or wording
  is a patch, a new or changed rule is a minor version, a change to the specification format or to
  how the skill works with the owner is a major one. After the push, tag that commit `vX.Y.Z` and
  push the tag. The catalog entry carries no version: a pinned version that nobody raises stops
  plugin updates.
- After any change to `feature-blueprint/`, rebuild `dist/feature-blueprint.skill` with the
  skill-creator packager and commit it together with the change.
