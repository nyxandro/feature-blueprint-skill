# Evals

Two cases compare how well a design catches the problems of a feature before code, with this
skill, with Superpowers and with no skill:

- `bot-reschedule-raw-idea`: a raw idea for a Telegram bot, with no project;
- `admin-csv-import-in-project`: a price import inside a small shop admin project, placed into the
  workspace by `place-files.sh`. The project's rules file is stored as `files/project-CLAUDE.md`
  so that this repository holds no CLAUDE.md, and the script renames it in the workspace.

Every prompt ends with the same note: the owner is away, so the agent decides and collects
questions at the end, writes no code and saves the result as files. It keeps the arms comparable,
since Superpowers otherwise stops at its first question.

`<case>/traps.md` is the grading list. An isolated agent wrote it from the request and the project
files alone, before any run. The graders under `<case>/graders/` cost nothing: a document was
saved, no code file was created and a skill fired. A project file the agent changed is not a
created file, so `run.py` compares the project files after each run and reports changed ones.

## Run

`compare/run.py` drives `claude plugin eval` (tested on Claude Code 2.1.318 and 2.1.319) and
needs `git`. Each run is a full Opus session on your account. Results go to `results/<name>/`,
which git ignores.

```bash
python3 -I feature-blueprint/evals/compare/run.py run --arm fb --out <name> --runs 3 --max-cost-usd 60
python3 -I feature-blueprint/evals/compare/run.py run --arm sp --out <name> --runs 3 --max-cost-usd 60
python3 -I feature-blueprint/evals/compare/run.py judge --out <name> --seed 1
```

- `--arm fb` runs this skill and the no-skill baseline together; `--arm sp` runs Superpowers
  7.0.2, cloned for the run. Different arms may run at the same time; the same arm twice into one
  `--out` may not.
- `--case <glob>` limits the cases. Repeated `run` calls with the same `--out` add runs.
- `run` exits with `COMPARE_RUNS_INCOMPLETE` when the suite stopped early or a run ended with an
  error; such runs are kept and marked in the summary. If keeping itself failed, `keep --arm …
  --out … --json <the saved eval JSON>` keeps the rest without paying for the runs again.
- `judge` removes plugin names and grades each case in batches of one run per arm (fb-1, sp-1 and
  none-1 together, and so on), shuffled by `--seed`, one isolated session per batch, against
  `traps.md`. It writes `judge-seed<N>.json` per case and `summary-seed<N>.md`. Two seeds show how
  steady the judge is. An interrupted pass with the same seed reuses the batches already judged.
- `criteria --overwrite` rewrites `traps.md`. Do it only for a new case, never between runs that
  are to be compared.

The criteria writer and the judge run with `--safe-mode` and no tools, so the user's CLAUDE.md,
memory, skills, plugins and hooks stay out. The agents under test get no Bash: the eval refuses
Bash on a machine whose Docker credential store holds a symlink, and designing needs only reading,
web research and writing files.
