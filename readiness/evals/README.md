# Testing the readiness skill

Discovery was tested first and separately: a fresh session asked which advertised skill it would load for "is this ready to build" answered `readiness` with the exact path. That proves routing, not behaviour. This is the behaviour test.

## Method

Ten tasks, three arms, three runs each, identical prompt text across arms. The only variable is what the agent can see.

| Arm | What it is | Why |
|---|---|---|
| `blind` | the four skill roots bind-mounted empty inside a mount namespace, plus `--no-skills` | the real control: the file cannot be read |
| `control` | `--no-skills` only, files still on disk | upper bound: an agent that greps the skills directory can still find the file. Measured, then dropped from the headline |
| `skill` | normal `pi`, skill advertised | the treatment |

Scoring is deterministic, in SkillOpt's shape: each task names an expected verdict and a set of regexes that must appear, and a set that must not. No LLM judge. The verdict is read from the first line containing "Verdict", because a body that later says "axis 8 NOT READY" is not a verdict. That one rule was itself a bug found in testing: an earlier scorer rejected correct answers.

A task counts as evidence only when `blind` fails and `skill` passes. Where both pass, the task guards a regression but proves nothing about the skill.

## Result, label `v4` (30 runs per arm)

| Task | blind | skill | |
|---|---|---|---|
| typo, one locale string, size S | 0/3 | 3/3 | skill earns it |
| article, pipeline already exists | 0/3 | 3/3 | skill earns it |
| already built (concept search) | 1/3 | 3/3 | skill earns it |
| rejected in `.out-of-scope/` | 0/3 | 3/3 | skill earns it |
| ci, unverified claim | 3/3 | 3/3 | no signal, a CI-latency audit skill is in AGENTS.md |
| live theme guardrail | 3/3 | 3/3 | no signal, in AGENTS.md |
| route invisible, XL | 3/3 | 3/3 | no signal |
| "make checkout faster" | 3/3 | 3/3 | no signal |
| six skills on a one-link job | 3/3 | 3/3 | no signal |
| blocked on a person | 3/3 | 3/3 | no signal |
| **total** | **19/30** | **30/30** | |

On the four tasks that need this skill's specific machinery (size cap, pipeline shortcut, concept search, rejection log): blind 1/12, skill 12/12. The other six tasks are cases a strong model already handles, or that the local rulebook already covers, so the 19/30 blind total is mostly those.

The blind arm also proves the skill is doing the work rather than the model: at 19/30 it is not helpless, but it misses exactly the four decisions that depend on the eight axes, the size cap, and the local rejection log.

## What the loop changed

The first version was written and called done. Testing then rejected it four times, each time for a measured reason.

| Version | Change | Why the test demanded it |
|---|---|---|
| v1 | first draft | shipped untested. SkillOpt's job is to stop exactly this |
| v2 | effort budget by size; conditions are gaps, not procedure; existing pipeline satisfies axes 2 and 8 by name; `Verdict:` on its own line | a one-string locale change produced a 136 second report and a file on disk; a pipeline job was blocked by re-verifying what the pipeline tests |
| v3 | the mechanical condition test: "if the condition would not change the next command, it is not a condition" | v2 still returned GO WITH CONDITIONS for a plain GO, twice in three runs |
| v4 | name the checkout (cwd) in the object line | one run audited a different theme repo on disk than the one under test, then said NO GO for the wrong repo |

Three measurement bugs were found and fixed on the harness side, not the skill side: `NO GO` matching a `GO` pattern, forbidding a skill name punishing a mention instead of a recommendation, and the verdict being read from the whole answer rather than the verdict line.

Two tasks were rewritten because the test was wrong, not the skill: the fixture was not a git repo (so correct agents refused the "git-committed" fact), and the migration task claimed the pages were unknown when they were discoverable on disk (so correct agents returned GO WITH CONDITIONS and were scored as failures). A good eval gets edited as much as the artifact under test.


## Same harness, the skills this one routes to

Pointing the same arms at three of the routed skills changed the routing table, not just the scores.

| Subject | Task | blind (files unreadable) | skill |
|---|---|---|---|
| `grilling/` | vague plan | 0/2 | 2/2 |
| | facts are the griller's job | 2/2 | 2/2 |
| | one round, then wait | 0/2 | 2/2 |
| | **total** | **2/6** | **6/6** |
| `triage/` | four issues, graded on the issue file | 8/8 | 8/8 |
| `wayfinder/` | three charting asks, graded on the written map | 6/6 | 6/6 |

Grilling earns its place, and the failures name why: the unaided arm asks questions but never commits to a recommended answer, and never stops for a round. Triage and wayfinder are null results. The first version of the triage fixture showed an advantage, then it turned out the fixture was ambiguous: one issue cited numbers the code did not produce, and the tracker had no stated label convention. Fixing the fixture erased the advantage, which is the right outcome for an eval and the wrong outcome for a boast.

Two skills changed because of this: `triage/` now states that a state label is earned by a verification in the session and that no test or fix gets written during triage (a run committed a fix mid-triage), and `wayfinder/` has a budget (one run spent more than five minutes charting a two-line ask).

### What the measurement got wrong before it got right

Nine defects, all in the harness or the fixture, none fixed by weakening a skill:

1. `NO GO` matched a `GO` pattern; the verdict is now read from the first line containing "Verdict".
2. Forbidding a skill's name punished a mention instead of a recommendation.
3. `--no-skills` does not stop an agent from grepping a skills directory: the first control arm read a skill from disk and passed. Hence the bind-mounted `blind` arm.
4. The prompt naming the skill leaked the method to the control arm.
5. A committed `__pycache__` counted as changed code.
6. Agents commit their work, so resetting to HEAD let one run's changes seed the next. Reset goes to a `baseline` tag.
7. Grading `issues/**/*.md` graded the fixture's own files rather than the run's output. The git delta is graded now.
8. Demanding the literal token for question one failed numbered questions in other forms.
9. Two tasks were ambiguous by construction. Both were fixture bugs.

## Limits, stated plainly

- Ten tasks, one model, one day. The variance is real: the blind arm moved between 11/30 and 19/30 across labels on identical code, so per-task rates need n=3 to mean anything.
- The rubric is regex, so it measures decisions and vocabulary, not the quality of the evidence behind them. A confident wrong answer that names the right verdict can pass; `already-built` at 1/3 in the blind arm shows the pattern is not free, but it is not a proof of reasoning.
- Long answers are truncated at 900 characters when printed, never when scored.
- Nothing here tests how the skill behaves when the user disagrees with its verdict, which is the next thing worth measuring.

## Reproduce

```bash
cd skills/readiness/evals
./run.py --label mine --arms blind,skill --n 3 --jobs 6
./run.py --rescore mine        # re-apply an edited rubric to saved answers, free
./run.py --compare v4 mine
```

Each run costs nothing beyond model tokens, about ten minutes wall time for 60 runs at six parallel. Answers land in `runs/<label>/<arm>/<task>__r<n>.json` on the machine that ran them. Those transcripts are not in this repo — they quote the private fixture — so the aggregate table above is the record, and the harness is here to regenerate the rest.
