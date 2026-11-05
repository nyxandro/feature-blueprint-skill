# Review mode

The owner brings a ready feature description, plan or PR and asks to find the holes. Do not rewrite
the document: report what is missing.

Read it with the eyes of steps 2, 4 and 7–11 of `SKILL.md`: does it fit the project's scale, what
are its decisions grounded on, what bypasses what the project already has, was a simpler option
missed, was anything added to people that nobody asked for. Write your own list of the feature's
main risks first, then go through the net in `references/checklists.md`, then check that the steps
have tests and the scenarios have acceptance criteria.

Order the findings by the harm to users and the business, blockers first, trifles briefly at the
end:

```
[Blocker | Serious | Minor] <what is missing> — <what a person or the business will go through>
  Where: <section, screen, file:line>
  Proposal: <a concrete addition>
```

A blocker: a person cannot finish the task or loses money or data, or a mechanism breaks so that
nobody notices. If the holes are many, offer to write a full specification instead.
