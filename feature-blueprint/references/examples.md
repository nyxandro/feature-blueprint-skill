# Examples

What good output looks like, and the common bad version next to it. The cases are made up. The
owner reads all of this in their own language; English here only shows the shape.

## Contents

- 1. A fork question to the owner
- 2. "At a glance"
- 3. A step of the plan
- 4. A small point change

## 1. A fork question to the owner

A Telegram bot for booking a barbershop; clients will now move their own appointments. In the
specification the fork has the format of section 6; in the chat it reads the same way, with ❓
before the question.

<example type="good">
❓ **F2. Can a client move an appointment shortly before it starts?**

**Situation:** Oleg is booked for 18:00 with master Anna. At 17:20 he moves the visit to tomorrow,
and Anna is left with a 40-minute gap nobody can book at such short notice.

**Why it is yours to decide:** it is about the masters' income and how strict the shop is with
clients; the code works either way.

- **A. Free moves until 2 hours before, later only through the administrator** — gives: masters
  lose fewer slots; at 17:20 Oleg sees «До визита меньше 2 часов, перенести через бота нельзя.
  Напишите администратору: @barber_admin»; costs: one more check and one message, some clients
  will be unhappy; locks in: nothing, the 2 hours is one setting.
- **B. Simplest: free moves at any time** — gives: the easiest path for clients, at 17:20 Oleg sees
  «Запись перенесена на завтра, 18:00»; costs: masters lose last-minute slots; locks in: nothing.

**I recommend A** because it protects the masters' time, and the shop already asks for 2 hours'
notice for phone bookings (`docs/rules.md`), so clients know the rule.

**If nobody decides:** option A with 2 hours.
</example>

<example type="bad">
F2. Reschedule policy: hard cut-off (A) or soft (B)? Recommend A — standard practice.
</example>

The bad version names no person and no consequence, uses a term the owner never used ("hard
cut-off"), does not show what the client sees and rests the recommendation on nothing checkable.
The simplest option here is "no limit", not "keep moves manual": an option that drops what the
owner asked for is not an option of this fork.

## 2. "At a glance"

An admin panel; a supplier sends a price list of 3,000 items every week.

<example type="good">
**What we build and why.** The manager uploads the supplier's file once a week and the prices and
stock of 3,000 products update in one go, instead of hours of editing one product at a time.

**How it will work.**
1. The manager uploads the file and sees what will change before anything is saved: 2,870 prices
   updated, 95 new products, 35 rows with errors. Nothing changes until they press "Apply".
2. Rows with errors are skipped and listed with the reason for each, so one bad row never blocks
   the other 2,965.
3. A product missing from the file is not deleted but marked "not in the last price list", so a
   supplier's mistake cannot empty the catalogue.
4. The upload runs in the background; the manager can leave the page and gets a notice when it is
   done or has failed.

**How we will build it.**
1. A background job on the queue the project already has (`server/jobs/`), so a long upload does
   not freeze the admin panel.
2. The existing product form's validation rules check each row, so the file and the form accept
   the same data.
3. A new table keeps every upload and its result, so any change can be traced to a file.
4. No new library for the file: the project already reads CSV in the orders export.

**What to watch.** Products are matched by the supplier's code: if the supplier changes their
codes, every product looks new. The preview shows this before saving.

**What it rests on.** The product importers of Shopify and WooCommerce (their help pages, checked
on YYYY-MM-DD): a preview before saving and a list of rejected rows → we take both.

**Awaiting your decision.**
1. Products missing from the file: mark them or hide them from the shop? I recommend marking:
   hiding would take products off sale whenever the supplier's file is incomplete (F1).

**Deployment:** the test server first, then production (F2).

**Scope:** 7 steps, about 2 h of agent work; most of the time goes to test runs on a 3,000-row
file; from you — one real price list.

**Not verified:** the supplier's file format; I only saw the column names you sent.
</example>

## 3. A step of the plan

A mobile app for voice notes gets a "Summary" button.

<example type="good">
### Step 3: summary job

**Files:** create `backend/app/jobs/summarize_note.py`; change `backend/app/jobs/__init__.py`
(register the job); test `backend/tests/jobs/test_summarize_note.py`
**Uses:** `NoteSummary` model from step 1, `transcribe_audio()` from step 2
**Provides:** `summarize_note(note_id: UUID) -> NoteSummary`
**Test:** `test_long_note_is_split_and_summarized` — a 58-minute transcript of 61,000 characters
is cut into 4 parts and gives one summary with a task list; the AI service is replaced with a
stub, so the test does not catch a change in the service's own limits.
**Closes:** scenario 1, the error «Не удалось сделать краткое содержание» from section 9,
acceptance criterion 2
**Done when:** `pytest backend/tests/jobs/test_summarize_note.py` passes.
</example>

<example type="bad">
### Step 3: implement AI summary
Add summarization with proper error handling and tests.
</example>

The bad version leaves every decision to the implementer: which file, which name, which value,
what counts as done.

## 4. A small point change

<example type="good">
Owner: "add a Copy button under the note's summary"

Agent: "A small change. I am adding a Copy button under the summary in `NoteSummaryCard`; it
copies the summary and the task list and shows the system notice «Скопировано». I will check it
with a widget test and on the emulator." Then it makes the change.
</example>

<example type="bad">
The agent writes a specification for the button, opens an issue and asks five questions about the
icon and the button's position.
</example>

<example type="good">
Owner: "add a discount field to the order form"

Agent: "This looked small, but the discount changes the order total, and the total goes to the
payment service and to the accountant's export. One question before I build it…" — then one fork
per "How to ask the owner".
</example>
