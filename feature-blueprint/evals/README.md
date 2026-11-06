# Evals

Four cases compare designs written with this skill, with Superpowers and with no skill:

| Case | Kind | Project |
|---|---|---|
| `bot-reschedule-raw-idea` | user-facing, a Telegram bot | none |
| `admin-csv-import-in-project` | user-facing, a price import | small shop admin |
| `shop-ozon-sync-in-project` | mechanism, stock and price sync with a marketplace | small shop admin |
| `vps-backups-raw-idea` | mechanism, backups of one VPS | none |

The shop admin project is placed into the workspace by each case's `place-files.sh`. Its rules
file is stored as `files/project-CLAUDE.md` so that this repository holds no CLAUDE.md, and the
script renames it in the workspace.

Every prompt ends with the same note: the owner is away, so the agent decides and collects
questions at the end, writes no code and saves the result as files. It keeps the arms comparable,
since Superpowers otherwise stops at its first question.

Two grading lists, both written by an isolated agent before any run:

- `<case>/traps.md`: the problems a good design of that feature must handle, from the request and
  the project files alone;
- `compare/owner-checklist.md`: what an owner who does not write code needs from any submission to
  understand it, decide and approve the start.

The graders under `<case>/graders/` cost nothing: a document was saved, no code file was created
and a skill fired. A project file the agent changed is not a created file, so `run.py` compares
the project files after each run and reports changed ones.

## Run

`compare/run.py` drives `claude plugin eval` (tested on Claude Code 2.1.318 and 2.1.319) and
needs `git`. Each run is a full Opus session on your account. Results go to `results/<name>/`,
which git ignores.

```bash
python3 -I feature-blueprint/evals/compare/run.py run --arm fb --out <name> --runs 3 --max-cost-usd 60
python3 -I feature-blueprint/evals/compare/run.py run --arm sp --out <name> --runs 3 --max-cost-usd 60
python3 -I feature-blueprint/evals/compare/run.py judge --out <name> --axis traps --seed 1
python3 -I feature-blueprint/evals/compare/run.py judge --out <name> --axis owner --seed 1
```

- `--arm fb` runs this skill and the no-skill baseline together; `--arm sp` runs Superpowers
  7.0.2, cloned for the run. Different arms may run at the same time; the same arm twice into one
  `--out` may not.
- `--no-baseline` with `--arm fb` skips the no-skill runs. Use it to re-measure a new skill
  version: copy the earlier `none-*` and `sp-*` run folders of the same cases into the new
  `--out`, so the judge sees the new runs in the same company as before.
- `--case <name> [<name> …]` limits the cases; names and globs both work, and `run` prints the
  cases it took. Repeated `run` calls with the same `--out` add runs.
- `run` exits with `COMPARE_RUNS_INCOMPLETE` when the suite stopped early or a run ended with an
  error; such runs are kept and marked in the summary. If keeping itself failed, `keep --arm …
  --out … --json <the saved eval JSON>` keeps the rest without paying for the runs again.
- `judge` removes plugin names and grades each case in batches of one run per arm (fb-1, sp-1 and
  none-1 together, and so on), shuffled by `--seed`, one isolated session per batch. `--axis
  traps` grades against `traps.md` and also lists serious errors; `--axis owner` grades against
  the owner checklist. It writes `judge[-owner]-seed<N>.json` per case and
  `summary[-owner]-seed<N>.md`. Two seeds show how steady the judge is. An interrupted pass with
  the same seed reuses the batches already judged.
- `criteria --case …` and `owner-criteria` write the grading lists. `--overwrite` replaces one; do
  it only for a new case, never between runs that are to be compared.

The criteria writer and the judge run with `--safe-mode` and no tools, so the user's CLAUDE.md,
memory, skills, plugins and hooks stay out. The agents under test get no Bash: the eval refuses
Bash on a machine whose Docker credential store holds a symlink, and designing needs only reading,
web research and writing files.
