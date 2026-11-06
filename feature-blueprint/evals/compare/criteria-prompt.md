You are a senior product engineer. The owner of a small product gave the request below to an AI
coding agent and left. The agent will write a design and an implementation plan for the feature
without asking anything.

Before any plan exists, write the checklist that such plans will be graded against: the
{{count}} most important problems, edge cases and decisions that a good design and plan for THIS
feature must address before any code is written. Pick the ones whose omission leads to bugs, lost
or corrupted data, wrong money or time, angry users, support load or a rewrite.

Rules:
- Each item is one sentence, specific to this feature and, if project files are given, to this
  project. It is checkable in a document: "The plan says what happens when…", "The plan
  decides…".
- Substance only. No items about format, structure, diagrams, length, language or style of the
  document, and none about following a particular methodology or process.
- No item that any plan would pass trivially, such as "describes the feature".
- Most important first.
- Output exactly {{count}} items as a Markdown numbered list, and nothing else.

The request, as the owner wrote it:

<request>
{{request}}
</request>

{{project}}
