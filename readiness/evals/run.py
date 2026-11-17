#!/usr/bin/env python3
"""Behavioural eval for the readiness skill, in SkillOpt's shape.

Why this exists: discovery was already proven (a fresh session named the skill and
its path). That says nothing about whether the skill produces the right verdict.
This runs each task twice against a real headless pi, with the prompt byte-identical
across arms, so the only variable is whether skills are loaded:

    control   pi --no-skills     no skill can be read
    skill     pi                 readiness is advertised and readable

Scoring is deterministic, in SkillOpt's style: every `expect` regex must match the
answer, no `forbid` regex may match. No LLM judge. A control pass means the model
got there without the skill, so that task proves nothing; a skill-only pass means
the file earned it.

USAGE
  ./run.py                        all tasks, both arms, 1 run each
  ./run.py --split val            just the validation split
  ./run.py --tasks ci,faster      named tasks
  ./run.py --label v2             save under evals/runs/v2
  ./run.py --jobs 4               parallel runs (default 4)
  ./run.py --compare v1 v2        per-task delta between two labels

LAYOUT
  evals/tasks.jsonl                     one task per line
  evals/runs/<label>/<arm>/<task>.json   raw answer, exit code, seconds
  evals/runs/<label>/results.jsonl      one line per run
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASKS = HERE / "tasks.jsonl"
RUNS = HERE / "runs"
PI = "/usr/bin/pi"
AGENT_DIR = "~/.pi/light/agent"
SKILL_ROOTS = [
    "~/.pi/skills",
    "~/.agents/skills",
    "~/config/skills",
    "third-party/skills",
]
TIMEOUT = 300
# A GO must be a GO: "NO GO" contains GO, so the verdict word alone is not enough.
GO_YES = r"(?i)(?:verdict\W{0,4})?\bGO\b(?![\w ]*\bwith conditions\b)"
NOT_GO = r"(?i)\bNO GO\b|\bnot ready\b|NEEDS ONE ANSWER|\bPARK\b"
GO_ANY = r"(?i)(?:verdict\W{0,4})?\bGO\b(?:\s+with conditions)?\b"


def load_tasks(only: str | None, split: str | None) -> list[dict]:
    """Tasks are pretty-printed JSON objects, one after another, blank-line separated."""
    text = TASKS.read_text()
    dec, i, found = json.JSONDecoder(), 0, []
    while True:
        while i < len(text) and text[i] in " \t\r\n":
            i += 1
        if i >= len(text):
            break
        obj, i = dec.raw_decode(text, i)
        found.append(obj)
    out = []
    for t in found:
        if only and t["id"] not in only.split(","):
            continue
        if split and t.get("split", "train") != split:
            continue
        out.append(t)
    return out


def verdict_text(answer: str) -> str:
    """The verdict line only. A body that later says 'axis 8 NOT READY' is not a verdict."""
    for line in answer.splitlines():
        if re.search(r"(?i)\bverdict\b", line):
            return line[:200]
    for line in answer.splitlines():
        if line.strip():
            return line[:200]
    return ""


def is_go(answer: str) -> bool:
    """True when the answer's verdict is GO, not NO GO / NEEDS ONE ANSWER / PARK."""
    head = verdict_text(answer)
    return bool(re.search(GO_YES, head)) and not re.search(NOT_GO, head)


def score(answer: str, task: dict) -> tuple[bool, list[str], list[str]]:
    missing = [p for p in task.get("expect", []) if not re.search(p, answer)]
    forbidden = [p for p in task.get("forbid", []) if re.search(p, answer)]
    if task.get("verdict") and not verdict_ok(answer, task["verdict"]):
        missing.append(f"verdict={task['verdict']}")
    if task.get("not_go") and is_go(answer):
        forbidden.append("verdict=GO (should not be)")
    return (not missing and not forbidden), missing, forbidden


def verdict_ok(answer: str, want: str) -> bool:
    if want == "GO*":  # GO or GO WITH CONDITIONS: both mean build now
        head = verdict_text(answer)
        return bool(re.search(GO_ANY, head)) and not re.search(NOT_GO, head)
    if want == "GO":
        return is_go(answer)
    return bool(re.search(rf"(?i)\b{want}\b", verdict_text(answer) or answer))


def build_cmd(task: dict, arm: str) -> list[str]:
    """Three arms, one variable: what the agent can see.

    blind    skills dirs bind-mounted empty inside a mount namespace, plus --no-skills.
             The file cannot be read, so this is the real no-skill control.
    control  --no-skills only. Discovery is off, but the files are still on disk, so a
             determined agent can list and read them. Upper bound on unaided behaviour.
    skill    the skill is advertised and readable.
    """
    base = [PI, "--no-session", "-p", task["prompt"]]
    if arm in ("blind", "control"):
        base.insert(1, "--no-skills")
    if arm != "blind":
        return base
    mounts = "; ".join(
        f"mount --bind /tmp/empty {root} 2>/dev/null" for root in SKILL_ROOTS if Path(root).exists()
    )
    inner = f"{mounts}; exec " + " ".join(shlex.quote(c) for c in base)
    return ["unshare", "-m", "--propagation", "private", "bash", "-c", inner]


def run_one(task: dict, arm: str, label: str, repeat: int = 1) -> dict:
    env = dict(os.environ, PI_CODING_AGENT_DIR=AGENT_DIR, PI_OFFLINE="1")
    cmd = build_cmd(task, arm)
    started = time.time()
    try:
        proc = subprocess.run(
            cmd, cwd=task.get("cwd", "/root"), env=env,
            capture_output=True, text=True, timeout=TIMEOUT,
        )
        answer, code, err = proc.stdout, proc.returncode, proc.stderr[-2000:]
    except subprocess.TimeoutExpired:
        answer, code, err = "", 124, f"timeout after {TIMEOUT}s"
    seconds = round(time.time() - started, 1)
    ok, missing, forbidden = score(answer, task)
    row = {
        "label": label, "task": task["id"], "split": task.get("split", "train"),
        "arm": arm, "repeat": repeat, "pass": ok, "missing": missing, "forbidden": forbidden,
        "seconds": seconds, "exit": code, "answer": answer, "stderr": err,
        "ts": datetime.now().isoformat(timespec="seconds"),
    }
    out = RUNS / label / arm
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{task['id']}__r{repeat}.json").write_text(json.dumps(row, indent=2))
    return row


def summarise(rows: list[dict], tasks: list[dict], arms: list[str]) -> str:
    def cell(tid: str, arm: str) -> str:
        rs = [r for r in rows if r["task"] == tid and r["arm"] == arm]
        if not rs:
            return "-"
        return f"{sum(1 for r in rs if r['pass'])}/{len(rs)}"

    head = f"{'task':14}{'split':7}" + "".join(f"{a:9}" for a in arms) + "verdict"
    lines = [head]
    for t in tasks:
        tid = t["id"]
        s_rate = cell(tid, "skill")
        b_arm = "blind" if any(r["arm"] == "blind" for r in rows) else "control"
        b_rate = cell(tid, b_arm)
        if s_rate not in ("-", "0/0") and b_rate not in ("-", "0/0"):
            sp = int(s_rate.split("/")[0]) / int(s_rate.split("/")[1])
            bp = int(b_rate.split("/")[0]) / int(b_rate.split("/")[1])
            if sp == 1 and bp == 0:
                v = f"skill earns it (vs {b_arm})"
            elif sp == 1 and bp == 1:
                v = "no signal (unaided also passed)"
            elif bp == 1 and sp < 1:
                v = "REGRESSION"
            elif sp == 0 and bp == 0:
                v = "both failed"
            else:
                v = f"partial (skill {s_rate}, {b_arm} {b_rate})"
        else:
            v = "incomplete"
        lines.append(f"{tid:14}{t.get('split','train'):7}" + "".join(f"{cell(tid,a):9}" for a in arms) + v)
    for arm in arms:
        arm_rows = [r for r in rows if r["arm"] == arm]
        if arm_rows:
            p = sum(1 for r in arm_rows if r["pass"])
            lines.append(f"{arm}: {p}/{len(arm_rows)} runs pass")
    return "\n".join(lines)


def rescore(label: str) -> None:
    """Re-apply today's rubric to yesterday's saved answers. Rubric edits are free."""
    tasks = {t["id"]: t for t in load_tasks(None, None)}
    rows = []
    for f in sorted((RUNS / label).glob("*/*.json")):
        r = json.loads(f.read_text())
        if r.get("task") not in tasks:
            continue
        ok, missing, forbidden = score(r["answer"], tasks[r["task"]])
        r["pass"], r["missing"], r["forbidden"] = ok, missing, forbidden
        f.write_text(json.dumps(r, indent=2))
        rows.append(r)
    arms = sorted({r["arm"] for r in rows})
    print(summarise(rows, list(tasks.values()), arms))
    for r in rows:
        if not r["pass"]:
            print(f"  [{r['arm']}/{r['task']}] missing={r['missing']} forbidden={r['forbidden']}")


def compare(labels: list[str]) -> str:
    a, b = labels
    out = [f"{'task':14} {a:10} {b:10}"]

    def load(label: str) -> dict[str, str]:
        got = {}
        for f in (RUNS / label).glob("**/*.json"):
            if f.name == "results.jsonl":
                continue
            try:
                r = json.loads(f.read_text())
            except Exception:
                continue
            if "task" in r:
                got[f"{r['task']}/{r['arm']}"] = "PASS" if r["pass"] else "fail"
        return got
    la, lb = load(a), load(b)
    for key in sorted(set(la) | set(lb)):
        out.append(f"{key:22} {la.get(key,'-'):10} {lb.get(key,'-'):10}")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks")
    ap.add_argument("--split", choices=["train", "val"])
    ap.add_argument("--arms", default="control,skill")
    ap.add_argument("--label", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--n", type=int, default=1, help="runs per task per arm")
    ap.add_argument("--compare", nargs=2)
    ap.add_argument("--rescore", metavar="LABEL")
    args = ap.parse_args()

    if args.rescore:
        rescore(args.rescore)
        return 0
    if args.compare:
        print(compare(args.compare))
        return 0

    tasks = load_tasks(args.tasks, args.split)
    if not tasks:
        print("no tasks matched", file=sys.stderr)
        return 2
    jobs = [(t, arm, i) for t in tasks for arm in args.arms.split(",") for i in range(1, args.n + 1)]
    print(f"{len(tasks)} tasks x {len(args.arms.split(','))} arms x {args.n} runs, {args.jobs} parallel, label {args.label}")
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        rows = list(pool.map(lambda j: run_one(j[0], j[1], args.label, j[2]), jobs))
    out = RUNS / args.label
    out.mkdir(parents=True, exist_ok=True)
    with (out / "results.jsonl").open("w") as fh:
        for row in rows:
            fh.write(json.dumps({k: v for k, v in row.items() if k != "answer"}) + "\n")
    print()
    print(summarise(rows, tasks, args.arms.split(",")))
    for row in rows:
        if not row["pass"]:
            print(f"\n[{row['arm']}/{row['task']}] missing={row['missing']} forbidden={row['forbidden']}")
            print(row["answer"][:900])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
