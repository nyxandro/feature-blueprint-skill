# feature-blueprint-skill — project rules

- Language: the skill (`feature-blueprint/SKILL.md`, `references/`), the README, commit messages
  and PR titles are in English. The skill itself makes the agent write its output in the owner's
  language; eval prompts stay in the language a real owner would use.
- The skill holds the order of work, the owner's rules, short don't-miss lists and the document
  format. It does not re-teach what the model already knows and does not repeat the owner's
  global rules.
- `SKILL.md` body stays around 500 lines; the frontmatter description stays within 1024
  characters and uses only the fields the skill-creator validator accepts.
- After any change to `feature-blueprint/`, rebuild `dist/feature-blueprint.skill` with the
  skill-creator packager (it leaves `evals/` out) and commit it together with the change.
