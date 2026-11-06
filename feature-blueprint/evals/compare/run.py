#!/usr/bin/env python3
"""Compare feature-blueprint with another planning plugin and with no plugin on the cases in ../.

  criteria        an isolated agent that sees only a case's request and project files writes traps.md
  owner-criteria  an isolated agent writes compare/owner-checklist.md: what an owner who does not
                  write code needs from any submission
  run             runs the cases for one arm through `claude plugin eval` and keeps what each run made
  keep            keeps the runs of a saved eval JSON again, after `run` failed while keeping them
  judge           an isolated judge grades the kept submissions blind, then writes a summary; axis
                  "traps" grades against each case's traps.md, axis "owner" against the owner
                  checklist

Arm "fb" runs feature-blueprint together with the no-plugin baseline ("none"); arm "sp" runs
Superpowers. Results go to ../results/<name>/, which git ignores. Run it with `python3 -I`.
"""
import argparse
import fnmatch
import json
import os
import random
import re
import shutil
import string
import subprocess
import tempfile
import time
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent.parent
SKILL_DIR = EVALS_DIR.parent
COMPARE_DIR = EVALS_DIR / "compare"
RESULTS_DIR = EVALS_DIR / "results"
MODEL = "claude-opus-5-5"
TRAPS_COUNT = 12
OWNER_COUNT = 8
OWNER_CHECKLIST = COMPARE_DIR / "owner-checklist.md"
# What each judging axis grades against. Only the traps axis also lists serious errors.
AXES = {
    "traps": {"prompt": "judge-prompt.md", "with_errors": True, "label": "traps caught"},
    "owner": {"prompt": "owner-judge-prompt.md", "with_errors": False, "label": "owner criteria met"},
}
# Tools the cases need beyond the read-only set the eval grants from allowed_tools. No Bash: the
# eval refuses it on a machine whose Docker credential store holds a symlink, and designing needs
# only reading, web research and writing files.
GRANTED_TOOLS = ["Write", "Edit", "WebSearch", "WebFetch"]
# Pinned to the versions the skill was compared against before.
COMPETITORS = {"sp": {"repo": "https://github.com/obra/superpowers", "tag": "v7.0.2"}}
NOT_CASES = {"compare", "results"}
# A fixture file stored under another name so that this repository holds no CLAUDE.md;
# place-files.sh gives it its real name in the workspace.
SCAFFOLD_RENAMES = {"project-CLAUDE.md": "CLAUDE.md"}
# Names that reveal which plugin wrote a submission. They are removed, not replaced by a marker,
# because a marker would set plugin submissions apart from the no-plugin ones.
REVEALING = re.compile(
    r"superpowers(?::[\w-]+)?|feature[-_ ]?blueprint(?::[\w-]+)?"
    r"|\b(?:using-superpowers|subagent-driven-development|executing-plans|writing-plans"
    r"|test-driven-development)\b", re.IGNORECASE)
RUN_DIR_NAME = re.compile(r"^[a-z]+-\d+$")
VERDICTS = {"pass", "fail"}
# Keeps the user's CLAUDE.md and memory out of the criteria writer and the judge, on top of
# --safe-mode, which turns off skills, plugins, hooks and the rest of the user's customizations.
ISOLATED_ENV = {"CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1", "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"}
MAX_KEPT_FILE_BYTES = 1_000_000


def select_cases(patterns):
    """All cases, or those matching any of the given names or globs."""
    cases = [p for p in sorted(EVALS_DIR.iterdir())
             if p.is_dir() and p.name not in NOT_CASES and (p / "prompt.md").exists()]
    if patterns:
        cases = [p for p in cases if any(fnmatch.fnmatch(p.name, pat) for pat in patterns)]
    if not cases:
        raise SystemExit(f"COMPARE_NO_CASES: no case under {EVALS_DIR} matches {patterns!r}")
    print("cases:", ", ".join(p.name for p in cases), flush=True)
    return cases


def request_text(case_dir):
    text = (case_dir / "prompt.md").read_text(encoding="utf-8")
    if text.startswith("---"):
        text = text.split("---", 2)[2]
    return text.strip()


def scaffold_files(case_name):
    """Workspace path -> fixture file, for the files place-files.sh puts into the workspace."""
    files_dir = EVALS_DIR / case_name / "files"
    if not files_dir.exists():
        return {}
    mapping = {}
    for path in sorted(p for p in files_dir.rglob("*") if p.is_file()):
        rel = path.relative_to(files_dir).as_posix()
        mapping[SCAFFOLD_RENAMES.get(rel, rel)] = path
    return mapping


def project_block(case_dir):
    files = scaffold_files(case_dir.name)
    if not files:
        return "There is no project: the agents worked in an empty folder."
    parts = [f"--- {rel} ---\n{path.read_text(encoding='utf-8')}" for rel, path in files.items()]
    return "<project>\nThe agents worked inside this project:\n" + "\n".join(parts) + "\n</project>"


def fill(template, **values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def numbered_items(text):
    """Items of a numbered list; lines under an item, such as sub-bullets, are joined into it."""
    items = []
    for line in text.splitlines():
        start = re.match(r"^\d+\.\s+(.+)$", line.strip()) if not line.startswith((" ", "\t")) else None
        if start:
            items.append(start.group(1).strip())
        elif items and line.strip():
            items[-1] += " " + re.sub(r"^[-*]\s+", "", line.strip())
    return items


def isolated_claude(prompt):
    """One answer from a session with no tools, customizations, CLAUDE.md or memory."""
    cmd = ["claude", "-p", "--safe-mode", "--model", MODEL, "--tools", "", "--disable-slash-commands",
           "--strict-mcp-config", "--no-session-persistence", "--output-format", "json"]
    with tempfile.TemporaryDirectory(prefix="fb-compare-iso-") as cwd:
        proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=cwd,
                              env={**os.environ, **ISOLATED_ENV})
    if proc.returncode != 0:
        raise RuntimeError(f"COMPARE_ISOLATED_RUN_FAILED: exit {proc.returncode}: {proc.stderr[:2000]}")
    out = json.loads(proc.stdout)
    if out.get("is_error"):
        raise RuntimeError(f"COMPARE_ISOLATED_RUN_FAILED: {out.get('result')}")
    return out["result"], out["total_cost_usd"]


def cmd_criteria(args):
    template = (COMPARE_DIR / "criteria-prompt.md").read_text(encoding="utf-8")
    for case_dir in select_cases(args.case):
        target = case_dir / "traps.md"
        if target.exists() and not args.overwrite:
            raise SystemExit(f"COMPARE_TRAPS_EXIST: {target} exists; pass --overwrite to replace it")
        prompt = fill(template, count=str(TRAPS_COUNT), request=request_text(case_dir),
                      project=project_block(case_dir))
        text, cost = isolated_claude(prompt)
        items = numbered_items(text)
        if len(items) != TRAPS_COUNT:
            raise RuntimeError(f"COMPARE_TRAPS_MALFORMED: expected {TRAPS_COUNT} items, got "
                               f"{len(items)} for {case_dir.name}:\n{text}")
        body = "\n".join(f"{i}. {item}" for i, item in enumerate(items, 1))
        target.write_text(
            f"# Traps: {case_dir.name}\n\nWritten by {MODEL} in an isolated session that saw only the "
            f"request and the project files, before any run. The judge grades every submission "
            f"against this list.\n\n{body}\n", encoding="utf-8")
        print(f"{case_dir.name}: {len(items)} traps, ${cost:.2f}")


def cmd_owner_criteria(args):
    if OWNER_CHECKLIST.exists() and not args.overwrite:
        raise SystemExit(f"COMPARE_OWNER_CHECKLIST_EXISTS: {OWNER_CHECKLIST} exists; pass --overwrite")
    template = (COMPARE_DIR / "owner-criteria-prompt.md").read_text(encoding="utf-8")
    text, cost = isolated_claude(fill(template, count=str(OWNER_COUNT)))
    items = numbered_items(text)
    if len(items) != OWNER_COUNT:
        raise RuntimeError(f"COMPARE_OWNER_CHECKLIST_MALFORMED: expected {OWNER_COUNT} items, got "
                           f"{len(items)}:\n{text}")
    body = "\n".join(f"{i}. {item}" for i, item in enumerate(items, 1))
    OWNER_CHECKLIST.write_text(
        f"# Owner checklist\n\nWritten by {MODEL} in an isolated session that saw no submission and no "
        f"skill. The owner axis of the judge grades every submission of every case against it.\n\n"
        f"{body}\n", encoding="utf-8")
    print(f"owner checklist: {len(items)} items, ${cost:.2f}")


def arm_names_for(arm):
    return {"with": "fb", "without": "none"} if arm == "fb" else {"with": arm}


def prepare_target(arm, tmp, cases):
    """Build the plugin directory to evaluate, with the cases copied under its eval dir."""
    plugin = tmp / "plugin"
    if arm == "fb":
        (plugin / ".claude-plugin").mkdir(parents=True)
        (plugin / ".claude-plugin" / "plugin.json").write_text(
            json.dumps({"name": "feature-blueprint", "description": "eval wrapper"}), encoding="utf-8")
        shutil.copytree(SKILL_DIR, plugin / "skills" / "feature-blueprint",
                        ignore=shutil.ignore_patterns("evals", "__pycache__"))
        eval_dir, ablation = "evals", []
    else:
        source = COMPETITORS[arm]
        subprocess.run(["git", "clone", "-q", "--depth", "1", "--branch", source["tag"],
                        source["repo"], str(plugin)], check=True)
        eval_dir, ablation = "fb-evals", ["--ablation", "none"]
    for case_dir in cases:
        shutil.copytree(case_dir, plugin / eval_dir / case_dir.name,
                        ignore=shutil.ignore_patterns("traps.md"))
    return plugin, eval_dir, ablation


def unlock(path):
    """The eval seals a kept sandbox read-only; open it so it can be read and removed."""
    for root, dirs, _ in os.walk(path, topdown=True):
        os.chmod(root, 0o700)
        for name in dirs:
            child = Path(root) / name
            if not child.is_symlink():
                os.chmod(child, 0o700)


def trace_facts(trace):
    tools, skills, final, weekly = {}, [], "", None
    for line in trace.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        kind = record.get("type")
        if kind == "assistant":
            for block in record["message"].get("content", []):
                if block.get("type") == "tool_use":
                    tools[block["name"]] = tools.get(block["name"], 0) + 1
                    if block["name"] == "Skill":
                        skills.append(block["input"].get("skill"))
        elif kind == "result":
            final = record.get("result") or ""
        elif kind == "rate_limit_event":
            windows = record["rate_limit_info"].get("unifiedWindows", {})
            weekly = windows.get("seven_day", {}).get("utilization", weekly)
    return {"tools": tools, "skills": skills, "final": final, "weekly_utilization": weekly}


def sandbox_of(trace_path):
    """The kept sandbox a trace belongs to, checked before anything in it is opened or removed."""
    trace = Path(trace_path)
    sandbox = trace.parents[1]
    if (not sandbox.name.startswith("claude-eval-") or trace != sandbox / "out" / "trace.jsonl"
            or not (sandbox / "sealed").is_dir()):
        raise RuntimeError(f"COMPARE_SANDBOX_UNEXPECTED: {trace_path} is not <claude-eval-*>/out/"
                           f"trace.jsonl next to a sealed/ folder; the eval layout changed")
    return sandbox


def new_run_dir(case_out, arm):
    """Reserve the next free <arm>-<n> folder; mkdir is atomic, so parallel keeps do not collide."""
    case_out.mkdir(parents=True, exist_ok=True)
    index = 1
    while True:
        try:
            (case_out / f"{arm}-{index}").mkdir()
            return case_out / f"{arm}-{index}"
        except FileExistsError:
            index += 1


def keep_run(out, case_name, arm, run):
    sandbox = sandbox_of(run["tracePath"])
    unlock(sandbox)
    workspace = sandbox / "sealed" / "home" / "cwd"
    if not workspace.is_dir():
        raise RuntimeError(f"COMPARE_WORKSPACE_MISSING: {workspace} does not exist; the eval layout changed")
    scaffold = scaffold_files(case_name)
    run_dir = new_run_dir(out / case_name, arm)
    kept, skipped, modified = [], [], []
    for path in sorted(workspace.rglob("*")):
        rel = path.relative_to(workspace)
        if not path.is_file() or ".git" in rel.parts:
            continue
        key = rel.as_posix()
        if key in scaffold:
            # Project files are not the agent's submission, but a change to one is recorded: the
            # request says not to write code, and the eval's own graders see created files only.
            if path.read_bytes() != scaffold[key].read_bytes():
                modified.append(key)
                dest = run_dir / "modified-project-files" / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dest)
            continue
        if path.stat().st_size > MAX_KEPT_FILE_BYTES:
            skipped.append(key)
            continue
        dest = run_dir / "files" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        kept.append({"path": key, "lines": path.read_bytes().count(b"\n")})
    trace = sandbox / "out" / "trace.jsonl"
    shutil.copy2(trace, run_dir / "trace.jsonl")
    facts = trace_facts(trace)
    (run_dir / "final-message.md").write_text(facts.pop("final"), encoding="utf-8")
    meta = {
        "case": case_name, "arm": arm, "tracePath": run["tracePath"], "score": run["score"],
        "error": run["error"], "aborted": run.get("aborted"), "costUsd": run["costUsd"],
        "turns": run["turns"], "durationSeconds": run["durationSeconds"],
        "graders": {g["name"]: g["passed"] for g in run["graders"]},
        "files": kept, "skippedLargeFiles": skipped, "modifiedProjectFiles": modified,
        "docLines": sum(f["lines"] for f in kept if f["path"].endswith(".md")), **facts,
    }
    # meta.json is written last: a run folder without it was not kept completely.
    (run_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.rmtree(sandbox)
    print(f"kept {run_dir.relative_to(EVALS_DIR)}: ${run['costUsd']:.2f}, {run['turns']} turns, "
          f"{meta['docLines']} doc lines, weekly limit {facts['weekly_utilization']}")


def kept_traces(out):
    return {json.loads(m.read_text(encoding="utf-8")).get("tracePath") for m in out.glob("*/*/meta.json")}


def keep_all(out, result, arm_names):
    """Keep every run of an eval result; returns the problems that make the result incomplete."""
    problems = [f"suite stopped early: {result.get('partialReason')}"] if result["partial"] else []
    already = kept_traces(out)
    for case in result["cases"]:
        for arm_key, runs in case["arms"].items():
            for run in runs:
                label = f"{case['name']}/{arm_names[arm_key]}"
                if run["error"] or run.get("aborted"):
                    problems.append(f"{label}: {run['error'] or run['aborted']}")
                if not run["tracePath"]:
                    continue
                if run["tracePath"] in already:
                    print(f"already kept: {label} {run['tracePath']}")
                    continue
                keep_run(out, case["name"], arm_names[arm_key], run)
    return problems


def finish(result, problems):
    print(f"partial={result['partial']}, total ${result['costUsd']:.2f}")
    if problems:
        raise RuntimeError("COMPARE_RUNS_INCOMPLETE: compare these runs with care or run them again:\n"
                           + "\n".join(problems))


def cmd_run(args):
    cases = select_cases(args.case)
    out = RESULTS_DIR / args.out
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / f"{args.arm}-{time.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}.json"
    with tempfile.TemporaryDirectory(prefix="fb-compare-") as tmp:
        plugin, eval_dir, ablation = prepare_target(args.arm, Path(tmp), cases)
        cmd = ["claude", "plugin", "eval", str(plugin), "--allow-tools", *GRANTED_TOOLS,
               "--eval-dir", eval_dir, "--runs", str(args.runs), "--model", MODEL,
               "--concurrency", str(args.concurrency), "--max-cost-usd", str(args.max_cost_usd),
               "--threshold", "0", "--keep-temp", "--no-publish", "--trust-plugin", "--scaffold",
               *ablation, "--json", str(json_path)]
        print("+", " ".join(cmd), flush=True)
        proc = subprocess.run(cmd)
        if not json_path.exists():
            raise RuntimeError(f"COMPARE_EVAL_NO_RESULT: claude plugin eval exited {proc.returncode} "
                               f"without writing {json_path}")
        result = json.loads(json_path.read_text(encoding="utf-8"))
        problems = keep_all(out, result, arm_names_for(args.arm))
        for report in (plugin / eval_dir / "results").glob("*/report.html"):
            shutil.copy2(report, json_path.with_suffix(".report.html"))
    finish(result, problems)


def cmd_keep(args):
    out = RESULTS_DIR / args.out
    result = json.loads(Path(args.json).read_text(encoding="utf-8"))
    finish(result, keep_all(out, result, arm_names_for(args.arm)))


def submission(letter, run_dir):
    parts = [f"=== Submission {letter} ==="]
    files_dir = run_dir / "files"
    paths = sorted(p for p in files_dir.rglob("*") if p.is_file()) if files_dir.exists() else []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # a binary file: the judge reads text only
        rel = path.relative_to(files_dir).as_posix()
        parts.append(f"--- file: {REVEALING.sub('', rel)} ---\n{REVEALING.sub('', text)}")
    final = (run_dir / "final-message.md").read_text(encoding="utf-8")
    parts.append(f"--- final chat message ---\n{REVEALING.sub('', final)}")
    parts.append(f"=== End of submission {letter} ===")
    return "\n".join(parts)


def parse_verdict(text, letters, item_count, with_errors):
    start, end = text.find("{"), text.rfind("}")
    try:
        verdict = json.loads(text[start:end + 1])["submissions"]
    except (ValueError, KeyError) as error:
        raise RuntimeError(f"COMPARE_JUDGE_NOT_JSON: {error}; the judge answered:\n{text[:4000]}") from error
    for letter in letters:
        entry = verdict.get(letter)
        if entry is None or "items" not in entry or (
                with_errors and not isinstance(entry.get("serious_errors"), list)):
            raise RuntimeError(f"COMPARE_JUDGE_INCOMPLETE: submission {letter} lacks items or serious_errors")
        for n in range(1, item_count + 1):
            item = entry["items"].get(str(n))
            if item is None or item.get("verdict") not in VERDICTS:
                raise RuntimeError(f"COMPARE_JUDGE_INCOMPLETE: submission {letter} item {n} is {item!r}")
    return verdict


def judge_batches(runs):
    """Runs with the same number form one batch, one per arm, so every batch compares the arms
    and no single judge call has to hold all submissions of a case."""
    batches = {}
    for run in runs:
        batches.setdefault(run.name.rsplit("-", 1)[1], []).append(run)
    return [batches[key] for key in sorted(batches, key=int)]


def run_dirs(case_out):
    runs = sorted(p for p in case_out.iterdir() if p.is_dir() and RUN_DIR_NAME.match(p.name))
    incomplete = [p.name for p in runs if not (p / "meta.json").exists()]
    if incomplete:
        raise RuntimeError(f"COMPARE_RUN_INCOMPLETE: {case_out.name}/{incomplete} have no meta.json; "
                           f"remove them or keep them again with `keep`")
    return runs


def judge_file_stem(axis, seed):
    return f"judge-seed{seed}" if axis == "traps" else f"judge-{axis}-seed{seed}"


def checklist_items(axis, case_name):
    path = EVALS_DIR / case_name / "traps.md" if axis == "traps" else OWNER_CHECKLIST
    return numbered_items(path.read_text(encoding="utf-8"))


def cmd_judge(args):
    out = RESULTS_DIR / args.out
    axis = AXES[args.axis]
    template = (COMPARE_DIR / axis["prompt"]).read_text(encoding="utf-8")
    rng = random.Random(args.seed)
    for case_out in sorted(p for p in out.iterdir() if p.is_dir()):
        case_dir = EVALS_DIR / case_out.name
        traps = checklist_items(args.axis, case_out.name)
        judge_path = case_out / f"{judge_file_stem(args.axis, args.seed)}.json"
        # Batches already paid for in an interrupted pass with the same seed are reused.
        done = json.loads(judge_path.read_text(encoding="utf-8"))["batches"] if judge_path.exists() else []
        done_sets = {frozenset(b["mapping"].values()): b for b in done}
        judged = []
        for batch in judge_batches(run_dirs(case_out)):
            rng.shuffle(batch)
            names = frozenset(r.name for r in batch)
            if names in done_sets:
                judged.append(done_sets[names])
                continue
            letters = list(string.ascii_uppercase[:len(batch)])
            # The owner axis grades how the owner reads the submission, not the project's code.
            project = project_block(case_dir) if args.axis == "traps" else ""
            prompt = fill(template, request=request_text(case_dir), project=project,
                          checklist="\n".join(f"{i}. {t}" for i, t in enumerate(traps, 1)),
                          documents="\n\n".join(submission(l, r) for l, r in zip(letters, batch)))
            text, cost = isolated_claude(prompt)
            judged.append({"mapping": dict(zip(letters, (r.name for r in batch))), "costUsd": cost,
                           "verdict": parse_verdict(text, letters, len(traps), axis["with_errors"])})
            judge_path.write_text(json.dumps({"seed": args.seed, "axis": args.axis, "batches": judged},
                                             ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"{case_out.name}: judged {', '.join(r.name for r in batch)}, ${cost:.2f}", flush=True)
    write_summary(out, args.seed, args.axis)


def write_summary(out, seed, axis_name):
    axis = AXES[axis_name]
    lines = [f"# Summary, axis {axis_name}, judge seed {seed}", ""]
    judge_cost = 0.0
    for case_out in sorted(p for p in out.iterdir() if p.is_dir()):
        stem = judge_file_stem(axis_name, seed)
        judge = json.loads((case_out / f"{stem}.json").read_text(encoding="utf-8"))
        judge_cost += sum(b["costUsd"] for b in judge["batches"])
        traps = checklist_items(axis_name, case_out.name)
        by_run = {run: batch["verdict"][letter]
                  for batch in judge["batches"] for letter, run in batch["mapping"].items()}
        arms = sorted({run.rsplit("-", 1)[0] for run in by_run})
        errors_head = " serious errors |" if axis["with_errors"] else ""
        lines += [f"## {case_out.name}", "",
                  f"| arm | {axis['label']} per run |{errors_head} cost $ | turns | doc lines | minutes "
                  "| skills | run errors | changed project files |",
                  "|---|---|" + "---|" * (8 if axis["with_errors"] else 7)]
        for arm in arms:
            runs = sorted(r for r in by_run if r.rsplit("-", 1)[0] == arm)
            metas = [json.loads((case_out / r / "meta.json").read_text(encoding="utf-8")) for r in runs]
            caught = [sum(v["verdict"] == "pass" for v in by_run[r]["items"].values()) for r in runs]
            errors = [", ".join(str(len(by_run[r]["serious_errors"])) for r in runs)] \
                if axis["with_errors"] else []
            cells = [
                ", ".join(map(str, caught)) + f" of {len(traps)}",
                *errors,
                ", ".join("%.2f" % m["costUsd"] for m in metas),
                ", ".join(str(m["turns"]) for m in metas),
                ", ".join(str(m["docLines"]) for m in metas),
                ", ".join(str(round(m["durationSeconds"] / 60)) for m in metas),
                "; ".join(",".join(filter(None, m["skills"])) or "-" for m in metas),
                "; ".join(str(m["error"] or m.get("aborted") or "-") for m in metas),
                ", ".join(str(len(m.get("modifiedProjectFiles", []))) for m in metas),
            ]
            lines.append(f"| {arm} | " + " | ".join(cells) + " |")
        lines += ["", "| # | trap | " + " | ".join(arms) + " |", "|---|---|" + "---|" * len(arms)]
        for n, trap in enumerate(traps, 1):
            cells = []
            for arm in arms:
                runs = [r for r in by_run if r.rsplit("-", 1)[0] == arm]
                cells.append(f"{sum(by_run[r]['items'][str(n)]['verdict'] == 'pass' for r in runs)}/{len(runs)}")
            lines.append(f"| {n} | {trap} | " + " | ".join(cells) + " |")
        lines.append("")
    lines.append(f"Judge cost: ${judge_cost:.2f}")
    path = out / f"{judge_file_stem(axis_name, seed).replace('judge', 'summary', 1)}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(EVALS_DIR)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    criteria = sub.add_parser("criteria")
    criteria.add_argument("--case", nargs="+", help="case names or globs")
    criteria.add_argument("--overwrite", action="store_true")
    owner_criteria = sub.add_parser("owner-criteria")
    owner_criteria.add_argument("--overwrite", action="store_true")
    run = sub.add_parser("run")
    run.add_argument("--arm", required=True, choices=["fb", *COMPETITORS])
    run.add_argument("--out", required=True, help="results folder name under ../results/")
    run.add_argument("--runs", required=True, type=int)
    run.add_argument("--max-cost-usd", required=True, type=float)
    run.add_argument("--concurrency", type=int, default=1)
    run.add_argument("--case", nargs="+", help="case names or globs")
    keep = sub.add_parser("keep")
    keep.add_argument("--arm", required=True, choices=["fb", *COMPETITORS])
    keep.add_argument("--out", required=True)
    keep.add_argument("--json", required=True, help="the eval JSON that `run` saved")
    judge = sub.add_parser("judge")
    judge.add_argument("--out", required=True)
    judge.add_argument("--seed", type=int, default=1)
    judge.add_argument("--axis", choices=list(AXES), default="traps")
    args = parser.parse_args()
    commands = {"criteria": cmd_criteria, "owner-criteria": cmd_owner_criteria, "run": cmd_run,
                "keep": cmd_keep, "judge": cmd_judge}
    commands[args.command](args)


if __name__ == "__main__":
    main()
