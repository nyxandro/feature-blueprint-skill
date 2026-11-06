# Checklists

The net for the pass in step 8 and the self-check of step 11. Write your own list of the feature's
main risks first: these lists catch what you missed, and what matters outside them outranks any
item here.

## Contents

- A. Interaction — for a user-facing or mixed feature (step 8)
- B. Mechanism — for an internal feature or the new mechanism of a mixed one (step 8)
- C. Self-check of the specification (step 11)

## A. Interaction

- **Entry points and exits.** Every place a person or an agent enters the feature from, not only
  the main one: another function, a notification, a link, an old message, a return visit, an
  action of the model or of a background job. Each entry has its path in the scenarios; each path
  ends in success, cancel, error or "left halfway".
- **Scenarios** with concrete people (name, role, context), the key moment and the failure branch,
  with a Mermaid diagram. Every screen or message appears in at least one scenario.
- **States** of every touchpoint — what the person sees and can do: empty (first time, nothing
  found, hidden by a filter — each with its own text and next step), loading, partial, error (not
  the same as empty), no permission, outdated, success.
- **Errors:** how we prevent it, how we notice it, the full text (what happened, why, what to do,
  a code per the project's rules), how the person gets out, what of their input is kept.
- **Edge cases:** a double press and a retry; left halfway and came back an hour or a day later; an
  old message, tab or button; two people editing the same thing; empty, huge and malformed data;
  time zones and clock changes; permissions or data changed halfway; lost network; limits of an
  external service; an expired session; abuse — guessing, someone else's identifier, spam.
- **Waiting:** something visible within a second; a long operation goes to the background and
  reports both success and failure, with cancel or a stated decision not to have it; a waiting
  limit and a "gave up waiting" state with a way out. No unmeasured promises: "usually under 2
  minutes" becomes [MEASURE].
- **Actions:** before an irreversible one, a confirmation that names what will disappear; a
  reversible one that needs protection from mistakes gets "Undo" after it rather than "Are you
  sure?" before it; with money, no double charge and a clear payment outcome; in bulk, a preview
  and a partial result; input survives an error.
- **Clarity and discovery.** After each step the person knows what happened, what comes next and
  how to undo. How they learn the feature exists and what it did without them; a hint or an
  announcement is a new element, so it is a fork with a "without it" option.
- **Texts** of key strings in full; the minimum of accessibility and localisation; privacy,
  consent and law; no dark patterns.
- **By interface type** — for each touchpoint (a bot plus an admin panel, an app plus push and
  email):
  - web and admin panels: addresses and page reload, tables and filters, roles and permissions;
  - website and shop: the first screen, search, cart and checkout, an unclear payment outcome,
    emails;
  - mobile: poor network and offline, asking for permissions when they bring value, push,
    background and a killed process, store rules (digital payments, account deletion), an old
    app version against a new server;
  - desktop: windows, hotkeys, files and saving, updates;
  - bot: old messages and buttons live forever, text typed instead of a button press, a pause of
    hours, private chats and groups, platform limits;
  - an AI feature as people see it: it is visible that this is AI and what it is doing; stop;
    preview and undo of its changes; editing the result and regenerating; "I don't know" instead
    of invention; confirming consequential actions; harmful instructions hidden in incoming
    content; which data goes to an external AI service and whether the person knows; the cost of
    requests and a per-person limit, which is the owner's fork;
  - tools for an AI agent: few tools, each for a whole task; descriptions written as for a new
    hire; unambiguous parameters and time with a zone; a response that states the outcome; an
    error with a stable code and a hint on how to fix the call; retries without duplicates; the
    person's permissions, not a superuser's; text in results is data, not instructions; the model
    learns about the new capability from its description and instructions, knows when to use it
    and when not, does not confuse it with similar ones and answers "what can you do" correctly;
  - voice: confirming what was heard, short answers, interrupting, silence and noise;
  - API and webhooks: one error format, input errors for all fields at once, an idempotency key,
    limits in the response, pages without gaps, versions and deprecation, signed webhooks and
    their redelivery;
  - CLI: exit codes, no questions in non-interactive runs, a dry run for dangerous operations,
    data to stdout and messages to stderr;
  - watches, TV, car, kiosk, VR/AR: seconds of attention, a remote or one hand, safety while
    driving, fatigue in VR, privacy on a public screen.

## B. Mechanism

- Guarantees in numbers, and who depends on the mechanism — what each of them sees when it fails.
- Data: the source of truth, the conflict rule, identifier mapping between systems, deletion on
  one side, order and duplicates, time and zones.
- Failures: the external service is down or throttles, access is revoked, a run is interrupted
  halfway or never starts, space runs out, data is unexpected, the API version changes, two copies
  run at once.
- A retry is a decision: on which errors, how many times, with what pauses, and who learns that the
  attempts ran out. Retries and restarts never duplicate work or charge twice.
- Recovery and its test: a recovery nobody tested does not count.
- An alert when success has not happened on time, not only on errors; who receives it and what they
  do.
- Access: keys, least privilege, who can delete data and its copies.
- Maintenance and a "when it breaks" runbook; money per month.
- Existing data: what happens to the data already in the system when the mechanism starts.

## C. Self-check

- Every goal has a scenario; every touchpoint has states with a way out; every error has a text and
  a recovery path; every failure of a mechanism says how it is noticed and recovered.
- Every scenario, error and acceptance criterion is closed by the test of some step ("Closes"). If
  every acceptance criterion passes, every goal is reached. Every new component serves a goal, a
  scenario or a criterion. Steps that reach production separately leave it safe after each.
- The document contains the risks from your own list in step 8, not only items of this net.
- What the owner said is separated from your unconfirmed recommendations. New settings for people
  and decisions that bypass what the project has are visible to the owner.
- Every key decision has ground; every practice has the scale at which it pays off; on a ladder,
  the chosen level fits the scale and the condition for moving up is measurable.
- No line decides nothing ("handle errors", "consider edge cases", "TBD").
- Every fork has a recommendation; no decision or move to P1 rests on "it is quicker"; the estimate
  is in hours of agent work and equals the sum of the steps.
- Names are consistent, no old version of a decision is left after edits, numbers add up, tables
  are intact, nothing is said twice, and "At a glance" fits one page.
- "At a glance" and the owner's part read without technical vocabulary, in the owner's language.
