# Feature Blueprint Skill

[![Download Feature Blueprint Skill](https://img.shields.io/badge/Download-feature--blueprint.skill-blue?style=for-the-badge)](https://github.com/nyxandro/feature-blueprint-skill/raw/main/dist/feature-blueprint.skill)

A feature design skill for Claude Code, Codex and OpenCode: before any code, the agent turns a
raw feature idea into a blueprint — how people will use the feature, how it works inside, and
how to build it step by step. Every key decision rests on research (official documentation,
engineering practice of well-known companies and products, popular repositories) and is sized
to the project, so the owner gets the simplest solution that does the job, not the one a big
company needs.

An agent given an idea builds the happy path and fills in the rest silently and badly: "No
data" with no next step, an endless spinner, "Something went wrong", a double charge after a
double click, backups nobody ever restored, a sync that quietly stopped a month ago. This skill
makes the agent think all of that through first, decide everything it can decide itself, and
bring the owner only the forks that change the product — explained in plain words, with a
recommendation.

The skill does not re-teach what the model already knows about UX and engineering. It holds the
order of work, the owner's rules, short lists of what must not be missed, and the document
format. The agent first writes the risks specific to the feature and the project, and only then
checks the lists, so they catch what was missed instead of narrowing the view.

The skill's instructions and document template are in Russian.

## When it runs

When the owner asks to work out, design, plan or write up a feature, including after a
discussion: "ok, let's work it out". Also when the owner asks to build a new feature and there is
no agreed plan yet: the blueprint comes first, code after the owner's go. A plain discussion of
an idea does not start it, nor do small fixes and bug fixes unless the owner asks to work them
out.

## What the agent does

1. **Reads the project and measures its scale**: rules, similar features and mechanisms, data,
   permissions, infrastructure; data volume, load, who maintains it. It does not ask what the
   code answers and does not touch production to get numbers.
2. **Sorts the feature**: user-facing, internal (backups, sync, queues, integrations, data
   migration) or mixed.
3. **Researches what to rest on**: official docs, engineering blogs and postmortems, recognised
   guides, live popular repositories, articles and discussions (as signals to corroborate). For
   every practice it records the scale at which it pays off. Hands-on experiments go into step 0
   of the plan, not into the blueprint.
4. **Asks up to three questions before the draft**, only when the answer flips most of the
   design. Its own recommendations from the discussion that the owner never confirmed count as
   open forks, not decisions. Questions go to the chat: a concrete situation, why the agent
   cannot decide it, the options with consequences, a recommendation.
5. **Writes the draft**: goals and non-goals, what the design rests on, options or a ladder from
   simple to "how big companies do it" with the lowest sufficient step chosen; scenarios; for
   the user-facing part — states, errors, edge cases, texts, accessibility; for the internal
   part — guarantees in numbers, failures and how anyone learns of them, recovery and its
   testing, access, cost, maintenance.
6. **Keeps a decision register**: what the agent decided itself (for review) and what goes to
   the owner — options, a recommendation and "what happens if nobody decides". Anything that
   bypasses what the project already has, and any new setting or message for users, is always
   shown to the owner.
7. **Writes the engineering part**: what is reused, the design, failures on every new path,
   maintenance, priorities, steps with tests, acceptance criteria.
8. **Checks the document** itself and, for a full blueprint, with a fresh agent that has no
   context of the conversation.
9. **Saves the document** in the project (`docs/specs/` unless the project has its own
   place) and sends one summary with the forks.
10. **After the owner's answers** updates the document and sends a one-screen final summary:
    what we build, how it will work, how we will build it (what is reused, what is new and
    why), what was decided, what it rests on, what to watch. No code until the owner says go.

There is also a review mode: the owner brings an existing feature plan or PR, and the agent
lists the gaps ordered by harm to users and the business.

## What it covers

User-facing features: web apps and admin panels, websites and shops, mobile and desktop apps,
bots in messengers and Mini Apps, AI features and agents including the tools an agent calls,
voice interfaces, CLI, API, SDK and webhooks, watches, TV, cars, kiosks and VR/AR.

Internal mechanisms: backups, sync with external services, queues and background jobs, data
migration, monitoring, integrations.

## Install

**Claude Code, as a plugin.** The plugin comes from [nyxandro/skills](https://github.com/nyxandro/skills),
the catalog of my skills. Run in a Claude Code session:

```text
/plugin install feature-blueprint --marketplace nyxandro/skills
```

This adds the catalog and installs the plugin from it, on Claude Code 2.1.275 or later. On an
older version, add the catalog first:

```text
/plugin marketplace add nyxandro/skills
/plugin install feature-blueprint@nyxandro
```

No version is pinned, so every commit to this repository is a new version. To take it, run
`claude plugin marketplace update nyxandro` and then `claude plugin update feature-blueprint@nyxandro`
in your shell, or turn on auto-update for the catalog under `/plugin` → Marketplaces.

**Any agent, as a skill folder.** Download `dist/feature-blueprint.skill` (the badge above) and
unpack it into the skills folder of your agent, or clone this repository and link the
`feature-blueprint/` folder there. No build step. Install it one way or the other, not both: with
both, Claude Code loads the skill twice.

The research step needs web search and page fetching in the agent; without them the agent says
so and marks unsupported decisions. The fresh-agent check needs a tool that starts subagents;
without one the agent rereads the document itself.

## Evals

`feature-blueprint/evals/` holds three cases in the `claude plugin eval` format: a prompt, the
expected outcome and graders. They cover a raw idea for a Telegram bot, an admin feature inside a
small scaffolded project, and a mobile AI feature. The evals are not part of the `.skill`
archive.

## Repository layout

```text
feature-blueprint/                    the skill itself
  SKILL.md                            the method, the owner's rules and short don't-miss lists
  references/document-template.md     the blueprint format, full and short, with the plan section
  references/builder-check.md         the prompt for the fresh-agent check
  evals/                              eval cases with graders
dist/feature-blueprint.skill          downloadable archive of the skill folder
```

## Acknowledgements

The skill is written from scratch, but builds on ideas from open projects:

- [obra/superpowers](https://github.com/obra/superpowers) (MIT) — study the project before
  asking, the fresh-agent check of a document, the implementation plan format;
- [garrytan/gstack](https://github.com/garrytan/gstack) (MIT) — the states table, the register of
  open decisions with "what happens if nobody decides", failures on new paths;
- [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0) — propose the likely
  option and ask to correct it, the edge-case checklist, kinds of empty states;
- [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills) (MIT) — the
  error-handling chain, comparing options by behaviour;
- [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) — scenarios with
  concrete people, the "deliberately not doing" section;
- [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
  (Apache-2.0) — goals and non-goals, P0–P2 priorities, acceptance criteria.

The rules on research, scale, internal mechanisms and agent tools draw on:

- [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) —
  alternatives considered and trade-offs as the core of a design document;
- [Choose Boring Technology](https://mcfunley.com/choose-boring-technology) — the maintenance
  cost of every new technology, try the existing stack first;
- [AWS Well-Architected, Reliability pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-principles.html)
  — test recovery procedures, signals in business terms;
- [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
  (Anthropic), [Function calling](https://developers.openai.com/api/docs/guides/function-calling)
  (OpenAI), [MCP: Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) —
  designing tools for AI agents.

## License

MIT.
