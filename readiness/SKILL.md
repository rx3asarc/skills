---
name: readiness
description: "Audit whether a piece of work is ready to build, and choose which skills, if any, to run before building it and in what combination. Routes to triage, grilling, wayfinder, to-spec/to-tickets, architect, and the verification skills, and refuses to stack skills that the work does not need. Use when asked 'is this ready to build', 'should I start building', 'what do I need before I start', 'ready or not', 'which skill should I use', or before starting any non-trivial build."
---

# Readiness

Readiness answers one question: is this work ready to be built, and if not, what closes the gap. The output is a verdict plus the smallest set of skills that earns it. Most work needs no skill at all.

Readiness is not a feeling about how well the idea was described. It is eight properties, each with evidence you can point at. Run the algorithm. Do not improvise a combo because it sounds thorough.

## The pi caveat

There is no Skill tool in pi. Every skill named here is a file. Read `references/skill-index.md` for the absolute path of each one, then read that `SKILL.md` and follow it. Several of them declare `disable-model-invocation: true`, which only means they cannot be auto-selected; nothing stops you loading the file.

If a `skill` tool happens to be registered (`pi-light --with=router`), it lists every skill and loads a body by name. Use it when it exists and fall back to paths when it does not.

## Step 0: name the object

State in one line what is being judged and who builds it:

> Object: `<issue / PR diff / idea in chat / theme change / article / campaign>`. Builder: `<me now / one agent session / a fleet / a human>`.

The object decides which axes apply and whether a tracker exists at all. An idea in chat has no issue to label, so `triage` does not apply. If the user names no object, ask for that one line. Do not interview.

Name the path too, not just the object. A verdict is about one checkout: the repository at the current working directory, unless the request names another. If a second copy of the same thing exists on this box (a live theme repo, another clone), say which one the verdict applies to before auditing it.

If an artifact already exists for this object under `.scratch/readiness/`, read it and re-check its evidence instead of re-running the audit. Re-audit only when the object changed.

## Step 1: size it

Score four proxies, one letter each: blast radius (how many files, systems, or people the change touches), reversibility (can it be undone in a minute), unknowns (is the route visible), and distance to the reviewer (does someone read it cold, days later).

| Size | Looks like | Builder | Skills before build |
|---|---|---|---|
| S | one file, one value, reversible, reviewer is right here | me, now | none |
| M | one section or module, reversible with git, reviewer reads the diff | one agent session | one, sometimes two |
| L | several files or systems, one-way door somewhere, reviewer reads a spec | agent session plus brief | two or three |
| XL | spans sessions, route not visible, decision trail is the deliverable | fleet over a map | `wayfinder` and its tickets |

Size caps the combo and the effort. Spend the effort the size earns:

| Size | Reply | Artifact |
|---|---|---|
| S | the verdict, the one check that matters, nothing else. No axis table | none. Do not write a file |
| M | the verdict plus the axes that failed | one short artifact |
| L | the verdict plus all eight axes with evidence | the full template |
| XL | the verdict plus the map reference | the map, not a report |

A size S job that reaches for three skills, or writes a page, is stalling, and this skill exists partly to say so out loud. Cap the audit too: if it is taking longer than the build would, stop, state the verdict from the evidence in hand, and name what is unmeasured.

## Step 2: audit the eight axes

Read `references/axes.md`. Walk the axes in order and record READY, NOT READY, or UNKNOWN for each, with the evidence beside it: a path, a command output, a link, a number. Evidence is the whole point. Memory of the conversation is not evidence, and neither is the requester's confidence.

An UNKNOWN axis that costs one command to resolve is resolved by running the command, not by invoking a skill. Grilling a user about a fact you could have read is a failure of this skill.

## Step 3: choose the combo

Read `references/combos.md`. Pick the smallest combo that clears every NOT READY and UNKNOWN axis. Five constraints hold:

1. Axes close in dependency order, 1 through 8. A done predicate cannot be written before the scope is bounded, and a route cannot be planned before the decisions that shape it are locked.
2. At most three skills before the build. A fourth means the work is really XL and needs a map, or you are avoiding the build.
3. Every axis needs a named closing skill or a cheap probe. "Grill it more" is not a closing skill.
4. The combo ends in an artifact a builder can open cold: an agent brief, or a spec with tickets. Readiness that lives only in this conversation is not readiness.
5. Verification gets designed before the build and run after it, never skipped in between.

Two shortcuts are legitimate and should be taken when they fit. If a skill already ships the route and the gate for this kind of work, the pipeline is the answer and no planning skill is needed: `the publishing pipeline skill`, `page-rebuild`, `ci-latency`, `the theme workflow skill`. That pipeline also satisfies axes 2 and 8 by name, so do not hand-re-verify what its own tests already check. If the finding is that its tests miss something, that is a condition on the pipeline, not a reason to block the work. If the only gap is one fact held by the requester, the answer is a single question, not a combo.

## Step 4: emit the verdict

Start the reply with one greppable line, before any table or evidence:

```
Verdict: <GO | GO WITH CONDITIONS | NEEDS ONE ANSWER | PARK | NO GO>
```

Then, for M and larger, fill in `assets/READINESS-template.md` and write it to `.scratch/readiness/<slug>.md`, or to the issue itself for tracked work. One of five verdicts:

| Verdict | Means | Next |
|---|---|---|
| GO | every axis READY | build, no skills |
| GO WITH CONDITIONS | something must change before the build: a decision is missing, or a gate cannot go red yet | build, with the conditions listed |
| NEEDS ONE ANSWER | one axis blocked on a fact or decision the human holds | ask that question, nothing else |
| PARK | blocked on someone else, or not worth building now | `handoff` |
| NO GO | already built, previously rejected, or the premise fails | say so, write nothing to disk |

Conditions are gaps, not procedure. The test is mechanical: if the condition would not change the next command, it is not a condition, so delete it and write GO. The standard route for a class of work (guard first, duplicate the theme, push via the pipeline, test in a browser) is the route inside a plain GO, never a condition on it.

Then state the next command plainly: the skill to load and the artifact to read. Nothing else.

## Step 5: hand over

If the verdict is GO or GO WITH CONDITIONS, start building under the artifact, or hand the artifact to whoever builds. Do not run the audit again mid-build because it felt thin. Re-audit only when the object changes: new scope, new route, a one-way door discovered inside the work.

## Hard rules

- An axis with no evidence is UNKNOWN, never READY.
- A gate that cannot go red is not verification. Test the gate on a change that must fail it before trusting it (`ci-latency` says the same thing about hooks).
- Do not let readiness become the work. The audit is minutes. A 136 second eight-axis report for a job whose next step is one pipeline command is the failure this skill exists to prevent.
- Local guardrails come first. A perfect plan that touches the live theme, prints a secret, or quotes an unsourced product claim is not ready, it is a hazard.
- Never invent an axis verdict to reach GO. NO GO delivered early is the cheapest output this skill produces.

## The eval contract

This skill is scored by `evals/run.py`, which reads the first `Verdict:` line and checks it against a fixed answer per task. Three arms: `blind` (skill roots mounted empty, so the file cannot be read), `control` (skills undiscovered but still on disk), `skill`. A task counts only when `blind` fails and `skill` passes. Method, results and known limits are in `evals/README.md`. Run `./evals/run.py --label v5 --arms blind,skill --n 3` after any edit, then `./evals/run.py --compare v4 v5`.

## When not to use this

- A typo, a config value, a rename with no callers, a one-line CSS fix. Just do it.
- The work already has a brief or spec with tickets. Open it and build.
- The user asked a direct question about code, not about scope.
- Mid-implementation. This audits the start of work, not the middle.
