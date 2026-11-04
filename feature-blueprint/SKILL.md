---
name: feature-blueprint
description: >
  Designs a feature before code and writes its specification: how people use it (scenarios,
  states, errors, texts) and how it works inside (data, failures, recovery, maintenance), plus an
  implementation plan with steps and tests. Decisions rest on research — documentation and the
  practice of known products — and are sized to the project without overengineering. For
  user-facing features (web, mobile, bots, AI agents and their tools, APIs) and internal
  mechanisms (backups, sync, queues, integrations). Use when the owner asks to work out, design,
  plan or write up a feature («прорабатываем», «спроектируй», «распиши фичу и план», «продумай
  или накидай, как сделать», «проверь план на дыры»), or asks to build a new feature with no
  agreed plan yet: specification first, code after the go. Not for a plain discussion of an idea
  («давай обсудим», «что думаешь»), small fixes or bug fixes unless asked to work them out, or
  visual styling. The owner may phrase this in any language; match on meaning.
---

# Feature specification

An agent given a feature idea builds the happy path and fills in the rest silently and badly:
"No data" with no next step, an endless spinner, a double charge after a double click, backups
nobody ever restored from, a sync that quietly stopped a month ago. You know everything needed to
avoid this. This skill sets the order in which to recall it in time, the rules for working with
the owner, and the document format. It takes from the owner only the decisions that are truly
theirs.

## Language

This skill and its template are in English. Everything the owner reads is written in the
language the owner uses in the conversation: the specification including the template's headings
(section numbers stay), both summaries and the questions, plan lines, GitHub issues and comments,
notes and inventories in `docs/`, markers such as [ASSUMPTION]. File, function and field names,
commands, paths, error codes and product names stay as they are. A project rule on language
wins.

## Main principle: propose, don't interrogate

The owner came to hand off the thinking. A questionnaire of twenty questions hands that work
right back. So:

- **The whole draft first, then the forks.** Before the draft, ask only what would force a
  rewrite (step 5). For the rest, read the idea in its most likely sense, fill the gaps with best
  practice and mark what you added.
- **Ask what matters, decide the obvious yourself.** There is no limit on questions: every
  important fork goes to the owner — one more clear question beats your suboptimal decision on
  their behalf. But do not flood them: what follows from the project, practice and common sense,
  decide yourself and show it for review.
- **Every key decision rests on verifiable ground:** a project fact, documentation, the practice
  of those who solved the same task (step 4). The agent's taste and memory are not ground.
- **Simplest sufficient.** The simplest solution that meets the goals at the project's scale,
  with a measurable condition for moving to the next level (step 7).
- **Agent time is not an argument.** An agent always builds: the difference between options is
  minutes or hours for it, even if habit says "a day or two". Do not drop an option, defer needed
  work or pick a method because it is quicker. Scope is set by the minimal complete
  production-grade version — without it the feature works wrong, loses data or fails silently —
  and it is built in full. Beyond it, only what is needed. Choices are decided by behaviour for
  people, reliability, complexity and maintenance, money, the owner's time.
- **Decisions are of two kinds.** The first follow from the project, the platform, research or
  established practice — take them yourself and list them in "Agent decisions — for review" so the owner can
  check; routine technical choices belong here. The second change the product or lock the design
  in for long: who gets what, money, user data and acceptable loss, irreversible actions, legal
  obligations, notable costs or the owner's time, the tone with customers, new settings and
  messages for people; design that is hard to reverse — a new component, store, background
  process, way of integrating. Bring these to the owner and explain what they change for the
  product, not which technology is better.
- **Do not add to people what nobody asked for.** A setting, switch, command, button,
  confirmation, message — each costs the user's attention and is the owner's decision, not a
  detail. By default the system behaves sensibly on its own and does not ask the person when a
  mistake can be undone. If you think an element is needed, bring it as a question with a
  "without it" option. This does not apply to what the pass in step 8a requires: states, error
  texts, cancelling a long operation, notifications of success and failure, confirming the
  irreversible — these are behaviour, not new elements.
- **Bypass what the project already has only in the open.** Your own implementation instead of
  an existing integration or module, a new dependency, a second path for the same thing — always
  visible to the owner: in "Agent decisions — for review", in "At a glance" and in the summaries, with the
  reason the existing one did not fit. If it locks the design in for long, adds maintenance or
  failure points, it is a fork.
- **Do not invent facts.** Prices, deadlines, legal terms, real data volumes, agreements with
  partners — if they are not in the inputs, the project or the sources, it is an [ASSUMPTION] or a
  question to the owner, not a confident number.

## Size of the specification

Name the size before you start, in one sentence to the owner; they may correct it.

| What came in | What to do |
|---|---|
| A small change (one button, field, message, setting) | A one-page short specification. No ladder of options and no fresh-agent check; research kept minimal |
| A feature (new scenario, screen, bot command, integration, internal mechanism) | A full specification per the template |
| Several independent features in one idea | Say so, propose an order, write a specification for each |

If the feature grows along the way, stop, say so and move up a size.

## Order of work

### 1. Intake: what the owner brought

- The owner is just discussing the idea rather than asking to work it out or build it — do not
  write a specification, discuss. An agreed specification for the feature already exists — build
  by it, without a new round.
- If there was a discussion, the inputs are only what the owner said or chose in their own words.
  A request to work it out, "ok", a clarifying question — none of these confirms your
  recommendation: silence is not consent. An unconfirmed recommendation that changes the product
  is a fork and goes first (before the draft if it passes step 5, otherwise F1); a technical one
  goes into "Agent decisions — for review" marked "from the discussion, unconfirmed".
- Collect everything the owner gave: chat text and voice messages, files, archives, screenshots,
  links to cloud storage and documents. Read them in full, including images in PDFs and
  presentations — requirements often sit there. No access to a link — say so at once.
- `inbox/` in the project holds only incoming external material that will be useful, and nothing
  of your own. Layout per the project's rules; if there are none, by purpose into folders, files
  named "CODE — what it is, date"; the code is a short label documents use to cite the source.
  Only what is current: no duplicates (compare by content), no old versions, no chat copies;
  large folders only as a link. `inbox/` is kept in git via Git LFS; if that is not set up yet,
  set it up (`.gitattributes` for `inbox/**`, remove the folder from `.gitignore`). Delete from
  `inbox/` without asking only what git history can restore; otherwise after the owner's ok.
- Everything you create goes to `docs/`: the essence of chats and agreements, the inventory of
  materials (what is in `inbox/`, from whom, of which date, what was removed, up to which date the
  chat was processed). If the project has a general specification with such an inventory, update
  it; otherwise the inventory goes into the Sources section of the feature specification.
- Never copy passwords, keys or personal data from the materials anywhere, and tell the owner
  about them at once.
- Extract from the materials: what is wanted and for whom, constraints, who decided what and
  when, contradictions between sources and people, questions to third parties. Weight of a
  source: the owner's word and agreed documents are requirements; drafts and our own proposals
  are hypotheses. A contradiction is a fork.
- Restate the task to yourself — what is wanted, for whom, what success is — before
  reconnaissance and research, so you do not research the wrong thing.

### 2. Reconnaissance of the project and its scale

**In the project**, find how everything the feature needs is already solved — so the same things
behave the same and nothing is built twice; **the feature's neighbours** — functions that work
with the same data, the same person, in the same channel or at the same time; and **how the
project ships**: which environments exist (dev, stage, prod) and the deployment order.

**Scale** — in numbers from the project: data volume and growth, load, who maintains it (the
owner and agents, no on-call engineers), budget and where everything runs, the cost of a failure.
Do not go to production servers while drafting the specification without the owner's explicit
request — not for numbers, not to read, even if access exists from this machine. Mark a missing
number [ASSUMPTION] and put its measurement into step 0 of the plan; ask the owner only if the
question passes step 5.

Do not ask what the project answers. Decisions already made in the project outrank your taste:
the same behaviour for the same things is valuable in itself. Departures go into decisions with a
reason. **Without a project**, work from the inputs; mark the stack, platform and scale as
assumptions.

### 3. Feature type

The type decides the pass in step 8 and the document's sections.

- **User-facing** — a person sees it and acts: a screen, a bot, an API for developers, tools for
  an AI agent. A background job that just carries out a person's action (a file import, a long
  generation) does not make the feature mixed.
- **Internal** — nobody interacts with it directly, but its failure hits people: backups, sync,
  queues, data migration, monitoring.
- **Mixed** — a user-facing feature that introduces a new mechanism that runs on its own and fails
  in its own ways: a sync, a schedule, an integration.

### 4. Research: what the decision rests on

Find out how others solved the same task and check the platform's capabilities. If research was
already done in the discussion, do not repeat it — extend it.

- **Profile skills first.** Look at the list of skills available to you — global and the
  project's — and load every one that concerns the feature's stack, platform or domain: a
  Telegram bot, AI agents, CI and so on. Their tools and rules come before generic search; the
  web is for what they do not cover.
- **Other sources:** official documentation and standards of the right version; engineering blogs
  and postmortems; recognised guides; live popular repositories (their open issues are a ready
  list of edge cases); the behaviour of comparable products; articles; discussions and posts — a
  signal to be confirmed by another source.
- **What to extract:** the practice, the problem it solves, the scale at which it pays off, its
  cost in complexity and maintenance. A principle carries over to any scale; a big company's
  implementation does not — it has other volumes and on-call engineers.
- **Platform:** without a profile skill, the current official documentation of the right
  version, otherwise [ASSUMPTION: not checked against <platform> documentation]. Memory is not a
  source. Prices, limits and capabilities only from fresh sources, with a date.
- **When to stop:** every fork has well-grounded options and new sources repeat what you found.
- **Into the document** — the "What it rests on" table (format in the template): only what
  shaped decisions, including "not taken and why".

**Read as much as decisions need; do not experiment.** A quick check in minutes (documentation, a
library's source, a tiny example) is fine. Spinning up a database or service, calling a live API,
a load test, comparing prices across a dozen vendors — into step 0 of the plan, marked [VERIFY],
with the decision that depends on it. The platform limits a decision, it does not set it: change
a decision only on a limit you found, and name it. Nothing to research with — say so; mark
decisions without ground [NO SOURCE].

### 5. Questions before the draft — blocking only

After reconnaissance and research, check for a fork that turns the whole feature over: which level
of the ladder to build or what product to make at all (one-way or two-way sync; losing a day of
data is fine or not a minute is). Ask before the draft only if all three hold:

- the answer changes most of the specification — a wrong guess means rewriting the document;
- the answer is not in the project, the inputs or the research;
- it is the owner's decision in the sense of the main principle, not yours.

Ask all such questions in one message, per "How to ask the owner", and wait for the answer. Your
unconfirmed recommendation from the discussion that changes the product is the first candidate.
The other important forks are not lost — they go to the owner after the draft.

Not blocking: rules and limits, prices, retention, texts, technology choice — propose them in the
draft with a recommendation. No blocking forks, or in doubt — do not ask: write the draft on the
most likely reading, put that fork first (F1) and describe what changes with the other answer.
Working without a person — the same, marked "taken as recommended, awaiting the owner's
confirmation".

### 6. Frame: goals and non-goals

In your own words: what we build, for whom, why, what success is. Separate what the owner said or
confirmed from what you added — including your recommendations from the discussion they did not
answer. Goals, non-goals and anti-goals (what would make the feature a failure even if it works).
For an internal mechanism, goals in numbers: how much data may be lost, how long it may be down,
how fast changes arrive.

### 7. Options and scale

If there is one sensible path, say so in one sentence and why. If several — 2–3 options that
differ in **behaviour**: for a user-facing feature, in what the person does (order of steps, one
by one or in bulk, who decides, the point of no return); for an internal one, in the mechanism
(what it protects against, what can diverge or be lost, who maintains it).

When options differ in reliability, complexity and cost, build a **ladder** of 2–4 levels: from the
simplest working solution to how big companies do it. For each level: what it protects against and
what not, complexity (moving parts, failure points), money per month, maintenance, when it is
needed. Choose the lowest level that meets the goals of step 6 at the project's scale; write a
measurable condition for moving up; check that moving up will not require reworking the data
format and interfaces. Goals demand a high level while the project is small — that is the owner's
fork: costly protection or accepted risk, in money and consequences.

- **Overengineering:** a separately maintained component when the existing stack suffices;
  headroom for many times today's load with no data on growth; technology nobody can fix; "just
  in case" with no measurable condition; a big company's practice without its reason.
- **Where not to economise:** the irreversible (data, money, deletion, sending to people);
  security and access; what is cheap now and costly later (data format and identifiers, duplicate
  protection, history, rollback); the failure signal.

Options rest on step 4. Criteria first, then the comparison. Recommend one and name what it pays
for its strengths. For the rejected ones — where they lost and what would bring them back. Do not
glue the best of each into a hybrid — nobody argued for it.

### 8. Pass through the feature

**Think first, then check.** Before the lists below, write the 3–7 main risks and forks of this
particular feature: what is specific to it and the project, what will break in what already
works, what is already there to reuse, what in the owner's idea can be read two ways. This is the
core of the pass: each risk goes to the document section where it is closed, or into a fork; the
main ones into "What to watch" in "At a glance". The lists are a net to catch what you missed, not a boundary:
what matters outside them outranks any item. Check every item; write only the applicable ones
into the document. For a mixed feature, both passes, without repetition.

**Seams with neighbours** — for a feature of any type. For each neighbouring function from
reconnaissance: what happens when they meet — the same data, one person in different roles or
places, the same time, the same permissions, the same notifications — and which of them wins. In
the calendar session three of the four serious gaps were seams.

**8a. Interaction** (user-facing and mixed):

- **Entry points and exits.** Every place a person or an agent enters the feature from, not just
  the main one: another function, a notification, a link, an old message, a return visit, an
  action of the model itself or of a background job. Each entry has its path in the scenarios;
  each path has an exit: success, cancel, error, left halfway.
- **Scenarios** with concrete people (name, role, context), the key moment and the failure
  branch; a Mermaid diagram; every screen or message appears in at least one scenario.
- **States** of every touchpoint — what the person sees and can do: empty (first time, nothing
  found, hidden by a filter — each with its own text and next step), loading, partial, error (not
  to be confused with empty), no permission, outdated, success.
- **Errors:** how we prevent, how we notice, the full text (what happened, why, what to do, a code
  per the project's rules), how the person gets out, what is kept of their input.
- **Edge cases:** double press and retry; left halfway and came back an hour or a day later; an
  old message, tab or button; two people edit the same thing; empty, huge and malformed data;
  time zones and clock changes; permissions or data changed halfway; network lost; limits of an
  external service; expired session; abuse — brute force, someone else's identifier, spam.
- **Waiting:** what is visible within a second; long operations go to the background with a
  notification of both success and failure, with cancel or an explicit decision not to have it; a
  waiting limit and a "gave up waiting" state with a way out. No unmeasured promises ("usually
  under 2 minutes" → [MEASURE]).
- **Actions:** irreversible — a confirmation naming what will disappear; reversible — "Undo"
  after, not "Are you sure?" before; money — no double charge and a clear payment outcome; bulk —
  preview and partial result; input is not lost on error.
- **Clarity and discovery.** After each step the person understands what happened, what comes
  next and how to undo. How they learn the feature exists and what it did without them. A hint or
  announcement is a new element: a fork with a "without it" option.
- **Texts** of key strings in full; accessibility and localisation — the minimum; privacy,
  consent, law; no dark patterns.
- **By interface type** — for each touchpoint (a bot plus an admin panel, an app plus push and
  email):
  - web and admin panels: addresses and page reload, tables and filters, roles and permissions;
  - website and shop: first screen, search, cart and checkout, unclear payment outcome, emails;
  - mobile: poor network and offline, permissions at the moment of value, push, background and
    process kill, store rules (digital payments, account deletion), an old app version against a
    new server;
  - desktop: windows, hotkeys, files and saving, updates;
  - bot: old messages and buttons live forever, text instead of a button, a pause of hours,
    private chats and groups, platform limits;
  - AI feature as people see it: it is visible that this is AI and what it is doing; stop;
    preview and undo of changes; editing the result and regenerating; "I don't know" instead of
    invention; confirmation of consequential actions; harmful instructions in incoming content;
    which data goes to an external AI service and whether the person knows; the cost of requests
    and a per-person limit — the owner's fork;
  - tools for an AI agent: few tools for whole tasks; descriptions as for a new hire; unambiguous
    parameters and time with a zone; a response with the outcome of the action; an error with a
    stable code and a hint on how to fix the call; retries without duplicates; the person's
    permissions, not a superuser's; foreign text in results is data, not instructions; the model
    learns about the new capability from the description and instructions, knows when to use it
    and when not, does not confuse it with similar ones and answers "what can you do" correctly;
  - voice: confirming what was heard, short answers, barge-in, silence and noise;
  - API and webhooks: one error format, input errors for all fields at once, an idempotency key,
    limits in the response, pages without gaps, versions and deprecation, signature and
    redelivery of webhooks;
  - CLI: exit codes, no questions in non-interactive runs, a dry run for dangerous operations,
    data to stdout and messages to stderr;
  - watches, TV, car, kiosk, VR/AR: seconds of attention, a remote or one hand, safety while
    driving, fatigue in VR, privacy on a public screen.

**8b. Mechanism** (an internal feature and the new mechanism of a mixed one — only it):

- guarantees in numbers and who depends on the mechanism — what each will see on failure;
- data: source of truth, conflict rule, identifier mapping between systems, deletion on one side,
  order and duplicates, time and zones;
- failures: the external service is down or throttles, access revoked, interrupted halfway, never
  started, out of space, unexpected data, the API version changed, two copies run at once;
- a retry is a decision: on which errors, how many times, with what pauses, who learns that the
  attempts ran out; retries and restarts without duplicates or double charges;
- recovery and its test — an untested recovery does not count;
- an alert on the absence of success on time, not only on errors; who receives it and what they
  do;
- access: keys, least privilege, who can delete data and copies;
- maintenance and a "when it breaks" runbook; money per month;
- launch: existing data, gradual rollout, rollback.

### 9. Decisions

**To the owner** — all decisions of the second kind (main principle), with no limit on number. If
there are very many, check whether you are passing on your own work and whether the feature
should be split. **Deployment is always a fork:** after implementation and tests, straight to dev
or stage (if they exist), straight to production (if that is all there is) or wait for a command;
what to check after deployment; the risk of the irreversible (data migration, sending to people).
Recommend based on the environments the project has. In technical features, ask as a business
consequence: not "which RPO" but "if the server burns down, can you lose the last day of
orders?". Format:

```
### F1. <The question as the owner would understand it>
**Why decide now:** <what depends on the answer: behaviour for people, data, money, reliability>
- **A. <option>** — gives: <what the user or business gets>; costs: <complexity and failure
  points, maintenance, money per month, the owner's time>; locks in: <what is hard to change later>
- **B. <option>** — gives: …; costs: …; locks in: …
- **C. Simplest: without it / as now** — gives: …; costs: …
**I recommend A** because <reason in product terms, citing the ground>.
**If nobody decides:** <what the implementer does by default and what the user sees>
```

Options must not rest on one assumption of yours: if a switch is in both, the question is really
about something else.

**Your own decisions** — the "Agent decisions — for review" list: only those the owner could
reasonably disagree with, usually up to ten. Decisions that bypass what the project has, if they
did not become a fork, always go here. Do not list the obvious.

### 10. How to build

The engineering part follows part 3 of the template: it holds the rules for the plan, priorities,
scope and deployment. The plan is the decisions the implementer cannot make alone: files, names,
values, a test for each step; no function bodies and no code files. The design implements the
level chosen in step 7 and builds on what the project already has; any departure in the open.

### 11. Check

**Yourself**, with fresh eyes:

- every goal has a scenario, every touchpoint has states with a way out; every error has a text
  and a recovery path, every failure of the mechanism — how it is noticed and recovered;
- the document contains the risks from your step 8 list, not only items of the net;
- inputs are separated from unconfirmed recommendations; new settings for people and decisions
  that bypass what exists are visible to the owner;
- every key decision has ground; practices have the scale at which they pay off; if you built a
  ladder, the level matches the scale and the condition for moving up is measurable;
- no lines that decide nothing ("handle errors", "consider edge cases", "TBD");
- every decision has a recommendation; no decision or move to P1 rests on "it is quicker"; the
  estimate is in hours of agent work and equals the sum of the steps;
- names are consistent, no old versions of a decision remain after edits, numbers add up, tables
  are intact;
- "At a glance" and the owner's part read without technical vocabulary, in the owner's language;
- the length is within limits (template).

**With a fresh agent** — for a full specification, if a tool for launching agents exists: the
prompt from `references/builder-check.md`. It sees neither the conversation nor these lists —
that is why it looks wider. Its questions: the answer exists (said by the owner or in the
project) — add it; a trifle — decide it yourself and mark it; it changes the product — into the
forks. Without the tool, read the document yourself as the implementer.

### 12. File and first summary

**File.** The project's place for feature documents, otherwise
`docs/specs/YYYY-MM-DD-<short-name>.md`; without a project, ask or give it in the chat. Template —
`references/document-template.md`. Status: "draft, awaiting the owner's decisions". A short
specification — up to 80 lines, a full one — 300–600; if longer, cut repetitions and the obvious,
not scenarios, errors and failures.

**Summary in the chat** — one message, essentially repeating "At a glance":

1. Two to four lines: what came out, the path to the file.
2. How it will work — 4–7 points, each with its consequence for the user or business.
3. How we will build it — 4–8 points: what appears in the system, what is reused, what is
   written anew and why the existing did not fit.
4. What it rests on — 2–4 supports in words: practice → what we took. Links only in the
   document.
5. Scope: steps, agent work — about N h (estimate), what is needed from the owner.
6. On a separate line — what is not verified and why.
7. Materials: what went into `inbox/`, what was removed, what could not be opened.
8. Found along the way — legacy code and old defects in the affected area: what they are and how
   they get in the way. Fixing or removing — as a fork; do not touch without consent.
9. Forks for the owner — per "How to ask the owner", all important ones, including deployment.

Then stop and wait for the answer. Do not write code. **Without a person** — the recommended
options, marked "taken as recommended, awaiting the owner's confirmation", and the summary says
so plainly.

### 13. After the owner's answers — final summary

1. Put the decisions into the document and move them to "Accepted". Check that answers do not
   contradict each other and do not pull changes into other sections: find all the places and
   update them, including "At a glance".
2. An answer opened a new fork or contradicts another — ask per "How to ask the owner". Do not
   choose silently. Do not change the status until the fork is closed; the final summary comes
   after.
3. No open forks — status "agreed".
4. **A final summary in the chat is mandatory**, even if every answer matched the
   recommendations: by it the owner checks whether the agent understood everything before the
   feature goes into work. "Decisions accepted, document updated" is not a summary. One screen,
   plain words:

```
**Result: <feature name>** — document agreed: <path to file>

**What we build.** 2–3 lines: what appears and why.

**How it will work.** 4–7 points — the path step by step: what happens when a person does X or
when the mechanism fires; what the person sees if something goes wrong.

**How we will build it.** 4–8 points: what appears in the system (data, background processes,
changes for the model or the interface), what is reused, what is written anew and why the
existing did not fit.

**What we decided.** Your decisions and my key decisions that affect the project — one line
each, with the reason. Especially what will be hard to change later and what bypasses what the
project has.

**What it rests on.** 2–4 supports in words: practice → what we took (links in the document).

**What to watch.** Risks; what is deferred, why it is not needed now and when to return; what is
not verified.

**Deployment.** <where and when — per your decision; what I will check after>.

**Scope and next step.** Agent work — about N h (estimate); from you — <decisions, access, a live
check>; after the go I will create issues: <which>; "say go — I start with <step 0: checks |
step 1>: <what exactly>".
```

Do not start implementation without the owner's permission. Permission is "go" («делай»,
«отработай», «погнали», «реализуй») in any language, and any reply that meets the start
conditions you named yourself (you asked to pick an account for the checks — they picked it and
said «отработай»). A request to work something out further («проработай ещё») is not
permission. Do not ask again. But permission does not close open forks: for unanswered ones, ask
in one line whether to take the recommendations.

Once you have permission, before any code split the specification into issues per the rules on
tasks: an issue for each part that can be checked and deployed separately (often one per
feature), with a link to the specification and everything needed to resume work on the issue
without this conversation; plan lines link to the issues. Then build per the project's rules
following part 3 of the document. Step 0 (checks and measurements) is part of implementation:
after it, carry on if the result does not change the owner's decisions or "How we will build
it"; if it does, briefly show what changed and wait. If permission came together with the
answers: when "How we will build it" has not changed since the first summary — the final summary
and start, saying where; when it has — the summary and wait for the answer.

After implementation and tests, deploy the way the owner decided in the specification: that is
their permission, do not ask again. Stop and ask only if something appeared during
implementation that was not there at agreement: an irreversible data migration, sending to
people, a new risk. After deployment, check what was agreed and send a report: what was deployed,
where, whether it works. The ban on production applies to drafting the specification, not to an
agreed deployment.

## Review mode

The owner brings a ready feature description, plan or PR and asks to find the holes — do not
rewrite the document. Go through its text with steps 2, 4 and 7–11: fit to scale, the ground of
decisions, what bypasses what exists, whether a simpler option was missed, whether anything was
added to people needlessly, your own risk list and the step 8 net, steps with tests and
acceptance criteria. Findings by harm to users and the business, blockers first, trifles briefly
at the end:

```
[Blocker | Serious | Minor] <what is missing> — <what a person or the business will go through>
  Where: <section, screen, file:line>
  Proposal: <a concrete addition>
```

A blocker: a person cannot finish the task, loses money or data; a mechanism breaks so that
nobody notices. Many holes — offer to write a full specification.

## How to ask the owner

The owner decides only what they understood. A question without an explanation they either
cannot answer or click the recommended option without reading — and reverse it an hour later.

- **In the chat, one message, then wait.** First 2–4 lines: what you are designing, what you have
  found out, why these questions cannot be decided without the owner. Then the questions.
- **Each question has four parts:**
  1. **Situation** — a live example: "a person opened their list of calendars, saw an unfamiliar
     'Reminders' and deleted it";
  2. **Why I do not decide it myself** — what depends on the answer in the product, data, money,
     reliability;
  3. **Options** — what the person will see, what it costs, what becomes hard to change;
     including the simplest ("without it", "as now"), and not all resting on one assumption of
     yours;
  4. **I recommend** — the option, why it is better for the product and what that rests on.
- **No internal words:** rule numbers, module names, terms the owner has not seen — replace with
  a description or explain.
- **The choice dialog** (a structured question tool) covers the text before it. The owner's forks
  always go first as an explanation in the chat; open the dialog only after the owner has read it
  (for example, replied "ask"). Straight to the dialog only for a service choice understandable
  without context: where to put a file, which account to use for checks. Every question in the
  dialog stands on its own, the recommended option first.

## Typical failures

| Thought | Reality |
|---|---|
| "I recommended A in the discussion and the owner did not object — so A is chosen" | Silence is not consent. An unconfirmed recommendation is a fork, and the first one |
| "I went through every item of the lists — so I covered everything" | The main risks are usually specific to the feature and project and are not in the lists. Your own list first, the lists after |
| "I will write my own client, it is more reliable" | Bypassing what the project has is a visible decision with a reason, not a line in the implementer's part |
| "I will ask through the choice dialog, it is faster" | The dialog covers the explanation and the owner clicks without reading. Explanation and questions in the chat, the dialog after "ask" |
| "The owner answered — I will write 'accepted' and that is it" | The final summary with "How we will build it" is mandatory: by it the owner catches misunderstandings before work starts |
| "The owner said «отработай» — I will run the checks and ask again" | They met the start conditions you named. That is permission, do not ask again |
| "I will decide this important fork myself so as not to bother the owner" | What matters goes to the owner, clearly and with a recommendation; only the obvious is yours |
