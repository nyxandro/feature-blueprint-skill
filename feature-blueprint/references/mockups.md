# Mock-ups and diagrams

Made only when the owner asks — «покажи макет», «нарисуй схему», «сделай мокапы экранов» — at any
moment: during the draft, after the summary, after the answers. Never offer them, never make them
unasked.

## What to draw

- **Mock-up** — the feature's touchpoints as a person sees them: screens, messages, a bot chat with
  its buttons, a push, an email. Each touchpoint in its states from section 7 (empty, loading,
  error, no permission, success…), switched with tabs; transitions clickable along the scenarios
  of section 5. The frame fits the device: phone width for mobile, a chat for a bot, a page for
  the web.
- **Diagrams** — the scenarios and states the specification draws in Mermaid, and the mechanism:
  what talks to what, where the data lives, where it can fail and what happens then.
- Only what was asked: one screen, one scenario, only the diagram — that is what you make.

The mock-up shows the specification and does not extend it: every element, text and step is in
the document, texts word for word from sections 9 and 12. The drawing needs something the
document lacks — add it to the document first, or to the forks if it is the owner's decision. Each
screen is labelled with its scenario, state and section. The look is plain and neutral, or the
project's own if it already has an interface: the mock-up settles behaviour and texts, not visual
style. At the top: "Mock-up of <specification file>, <date>; on a mismatch the document wins".

## File

- One self-contained HTML file per request: styles and scripts inside; the only external script
  is Mermaid from a CDN with an exact version checked on the registry. Labels in the owner's
  language, the product's texts as in the specification.
- Next to the specification, named after it: `<specification>-mockup.html`,
  `<specification>-diagrams.html`. A new request replaces the file.
- When the specification changes, update its mock-ups and diagrams in the same pass or delete
  them; a stale one is not left behind.

## Showing it

1. If a browser automation tool is available, open the file there first: it renders, the console
   has no errors, the tabs and transitions work. Close that session and keep no screenshots.
2. Open the file in the owner's default browser: macOS — `open <file>`; Linux — `xdg-open <file>`;
   Windows — `start "" "<file>"`; WSL — `explorer.exe "$(wslpath -w <file>)"` (its exit code may
   be non-zero even when the browser opened).
3. In the chat, one or two lines: what is in the file and its path. The browser did not open — say
   so and give the path.
