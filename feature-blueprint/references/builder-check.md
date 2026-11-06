# Fresh-agent check

For a full specification, after the self-check and before the summary to the owner. Launch an
agent with a clean context (no conversation history) with this prompt, filling in the product type
and the path to the document; when there is no file, put the document's text into the prompt:

```
You are an experienced product engineer who builds <product type: a web app, a bot, a mobile
app…>. You were given a document describing a feature and asked to build it. You cannot contact
the author of the document.

Read <path to the document>. Look into the project's code if needed.

List only the questions without which you cannot build the feature well: places where you would
have to guess, and a wrong guess would be visible to the user or costly. For each: the question
and what changes depending on the answer. Separately, list places where a person can end up in a
state the document does not describe (a dead end, endless waiting, lost input, a silent failure),
and places where an internal mechanism can break so that nobody notices. Separately again —
decisions that look out of proportion to the project's scale from section 4: too complex for it
or too fragile. Separately — statements about the existing project (what exists, what does not,
how a module behaves) that the code does not confirm: what the document says, what you found and
where you looked. Separately — statements about how a platform, a library, a service or a setting
behaves (what a parameter does, when a schedule fires, how two storage or retention rules work
together, what an API returns or allows, what can change without a restart) that you doubt: what
the document says, what you believe is true and why. Separately — decisions that would be
costly to undo if they prove wrong (a data format, a new store, an external contract) and rest on
an assumption or a single source: what would prove them wrong. Separately — for each goal in
section 2: the most likely way the feature gets built exactly as written, passes its tests and
still misses the goal. Order by importance.

Skip what the document explicitly leaves to the implementer and what you would reasonably decide
yourself. Do not nitpick wording.

If nothing important remains, answer "nothing important remains".
```

## What to do with the answer

| Pile | What to do |
|---|---|
| The answer already exists: the owner said or confirmed it in the conversation, or it is in the project | Add the answer to the document. Your own recommendation from the conversation is not an answer |
| A trifle: a sensible implementer would decide it, the product does not change | Decide it yourself, add it to the document, mark it in "Agent decisions — for review" |
| Changes the product, only the owner can answer | Into the forks of section 6, with the other forks |
| A statement about the project is wrong | Fix it in the document. If a decision rested on it, revisit the decision; if that changes the product, into the forks of section 6 |
| A statement about how a platform, service or setting behaves is doubted | Check it in the current documentation of the right version. Wrong — fix it and everything built on it, such as a runbook, an alert or a schedule. Still unconfirmed — into step 0 as [VERIFY] with what would prove it wrong |
| A goal is missed although everything is built as written | Close the gap in the document: the scenario, acceptance criterion or step that was missing. If closing it changes the product, into the forks of section 6 |
| A costly-to-undo decision rests on weak ground | Into step 0 as [VERIFY] with what would prove it wrong; if the owner must weigh the risk, into the forks of section 6 |

Questions from the third pile go to the owner together with the other forks, in one message, the
most important first. This is the only round of questions the check produces.
