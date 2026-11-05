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
order of work, the owner's rules, lists of what must not be missed, and the document format. The
main file stays within the size the Agent Skills standard recommends (500 lines, about 5,000
tokens): the checklists, the examples and the review mode live in reference files the agent opens
at the step that needs them. The agent first writes the risks specific to the feature and the
project, and only then checks the lists, so they catch what was missed instead of narrowing the
view.

The skill and its template are written in English. Everything the owner reads — the
specification, the summaries and questions, plan lines, issues and comments — the agent writes in
the language the owner uses in the conversation, unless the project's rules say otherwise.

## When it runs

When the owner asks to work out, design, plan or write up a feature, including after a
discussion: "ok, let's work it out". Also when the owner asks to build a new feature and there is
no agreed plan yet: the blueprint comes first, code after the owner's go. A plain discussion of
an idea does not start it. A small point change — a button, a field, an option, a clear fix —
gets no specification, file or issue: the agent studies the code, writes in the chat what it will
change and how it will check it, and does it at once, stopping to agree with the owner only on an
important point. A bug fix starts it only when the owner asks to work it out.

## What the agent does

1. **Takes in the materials** the owner gave — chats, files, archives, links — through the
   [materials-intake](https://github.com/nyxandro/materials-intake-skill) skill: new ones are
   filed in `inbox/` with one inventory and one digest of what they say, and the agent reads the
   digest and the originals the feature rests on.
2. **Reads the project and measures its scale**: rules, similar features and mechanisms, data,
   permissions, infrastructure; data volume, load, who maintains it. It does not ask what the
   code answers and does not touch production to get numbers.
3. **Sorts the feature**: user-facing, internal (backups, sync, queues, integrations, data
   migration) or mixed.
4. **Researches what to rest on**: official docs, engineering blogs and postmortems, recognised
   guides, live popular repositories, articles and discussions (as signals to corroborate). For
   every practice it records the scale at which it pays off. Hands-on experiments go into step 0
   of the plan, not into the blueprint.
5. **Before the draft, asks only what flips most of the design**, all in one message. Its own
   recommendations from the discussion that the owner never confirmed count as open forks, not
   decisions. Questions go to the chat: a concrete situation, why the agent cannot decide it, the
   options with consequences, a recommendation.
6. **Writes the draft**: goals and non-goals, what the design rests on, options or a ladder from
   simple to "how big companies do it" with the lowest sufficient step chosen; scenarios; for
   the user-facing part — states, errors, edge cases, texts, accessibility; for the internal
   part — guarantees in numbers, failures and how anyone learns of them, recovery and its
   testing, access, cost, maintenance.
7. **Keeps a decision register**: what the agent decided itself (for review) and what goes to
   the owner — options, a recommendation and "what happens if nobody decides". Anything that
   bypasses what the project already has, and any new setting or message for users, is always
   shown to the owner.
8. **Writes the engineering part**: what is reused, the design, failures on every new path,
   maintenance, priorities, steps with tests, acceptance criteria.
9. **Checks the document** itself and, for a full blueprint, with a fresh agent that has no
   context of the conversation.
10. **Saves the document** in the project (`docs/specs/` unless the project has its own
   place) and sends one summary with the forks.
11. **After the owner's answers** updates the document. If the answers do not overturn the plan,
    that is the go: the agent says in a few lines what was taken and gets to work without asking
    again. If the owner reversed a decision, rejected the approach or asked for more
    research, the agent reworks it, shows only what changed and waits for the go.

There is also a review mode: the owner brings an existing feature plan or PR, and the agent
lists the gaps ordered by harm to users and the business.

On request the agent draws mock-ups of the screens in every state and diagrams of the scenarios
and the mechanism: one self-contained HTML file next to the specification, opened in the owner's
browser when ready. It never offers them on its own and never adds anything the specification
does not say.

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

This adds the catalog and installs the plugin from it, on Claude Code 2.1.275 or later, together
with [materials-intake](https://github.com/nyxandro/materials-intake-skill), which it depends on.
On an older version, add the catalog first:

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
both, Claude Code loads the skill twice. Install materials-intake the same way; without it the
agent still reads every material, but leaves them unfiled and says so.

The research step needs web search and page fetching in the agent; without them the agent says
so and marks unsupported decisions. The fresh-agent check needs a tool that starts subagents;
without one the agent rereads the document itself.

## Repository layout

```text
feature-blueprint/                    the skill itself
  SKILL.md                            the principles and the order of work
  references/document-template.md     the specification format with the plan section
  references/checklists.md            the don't-miss net for the pass and the self-check
  references/examples.md              good and bad forks, "At a glance", plan steps
  references/review-mode.md           finding holes in a ready plan or PR
  references/builder-check.md         the prompt for the fresh-agent check
  references/mockups.md               mock-ups and diagrams in HTML, made on request
dist/feature-blueprint.skill          downloadable archive of the skill folder
AGENTS.md, CLAUDE.md                  rules for agents working on this repository
```

## Acknowledgements

The skill is written from scratch, but builds on ideas from open projects:

- [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)
  (MIT) — a mechanism nobody asked for is built only when its absence harms unnoticed or is
  costly to add later, what two decisions give together, statements about the project checked
  against the code, earlier attempts and unwritten rules of the code, how people manage today,
  safety after each separately shipped step, costly-to-undo decisions on weak ground, the goal
  apart from the means the owner named, how the feature can be built as written and still miss
  a goal, a stop before a small change in a risky zone, what is known only at implementation, an
  option from another side, what a test with a stub does not catch;
- [obra/superpowers](https://github.com/obra/superpowers) (MIT) — study the project before
  asking, the fresh-agent check of a document, the implementation plan format, the rules every
  step keeps;
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

The shape of the skill follows guidance on writing skills:

- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
  (Anthropic) and the [Agent Skills specification](https://agentskills.io/specification) — the
  size of the main file, reference files one level deep, contents lists, examples;
- [Build skills](https://learn.chatgpt.com/docs/build-skills) (OpenAI) — the description with clear
  scope, the main use first;
- Bojie Li, «AI-агенты изнутри» (the chapters on Agent Skills and on clarifying requirements) —
  few principles with examples, and when to ask before acting and when to act at once.

## License

MIT.
