# feature-blueprint-skill — project rules

- Language: the skill (`feature-blueprint/SKILL.md`, `references/`), the README, commit messages
  and PR titles are in English. The skill makes the agent write its output in the owner's
  language; eval prompts stay in the language a real owner would use. Plans and reports for the
  owner in `docs/` are in Russian.
- The skill holds the order of work, the owner's rules, the don't-miss lists and the document
  format. It does not re-teach what the model already knows and does not repeat the owner's
  global rules. Each rule says why it exists; an exception is its own condition, not a clause
  inside the rule. Examples go to `references/examples.md`.
- `SKILL.md` body: at most 500 lines and close to 5,000 tokens (count the body with `tiktoken`
  `o200k_base`). The owner's rules and clear wording come before the number: if they do not fit,
  keep them and say how far over the body is. Details that only one step needs go to
  `references/`, linked straight from `SKILL.md` with when to read them; a reference file over
  100 lines starts with a contents list.
- The frontmatter description stays within 900 characters (the limit is 1024): what the skill
  does and when to use it, the main use first, no summary of the workflow. Use only the fields
  the skill-creator validator accepts.
- After any change to `feature-blueprint/`, rebuild `dist/feature-blueprint.skill` with the
  skill-creator packager (it leaves `evals/` out) and commit it together with the change.
