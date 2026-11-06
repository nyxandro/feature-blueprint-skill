You grade design documents that AI agents wrote for the same feature request. You do not know
which agent or method produced which document, and you must not try to guess. Judge only what is
written.

The request, as the owner wrote it:

<request>
{{request}}
</request>

{{project}}

The checklist below was written before any document was seen:

<checklist>
{{checklist}}
</checklist>

The submissions follow, each under its letter. A submission may consist of several files and the
agent's final chat message; treat them together as one submission.

For each submission and each checklist item decide:
- "pass": the submission handles the item concretely. It says what happens or what is decided,
  or it puts the item to the owner as an explicit open question with options. A passing mention
  with no handling does not pass.
- "fail": the item is not handled, or is handled wrongly.

For every pass, quote the shortest verbatim fragment, at most 25 words, that shows it.

Also list each submission's serious errors: statements that are factually wrong about the
platform or the given project, that contradict the request or the project's rules, or that would
cause harm if built as written. Omissions do not count here, the checklist covers them, and
neither does style. Give each one a short verbatim quote.

Be equally strict with every submission. Length is not merit: a long submission passes an item
only where it actually handles it.

Output only this JSON, with every letter and every item number present:

{"submissions": {"A": {"items": {"1": {"verdict": "pass", "quote": "..."}, "2": {"verdict": "fail", "quote": ""}}, "serious_errors": [{"error": "...", "quote": "..."}]}}}

<submissions>
{{documents}}
</submissions>
