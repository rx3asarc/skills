# Combos

A combo is an ordered set of skills chosen to close the axes that failed. Pick the smallest one. Each entry below names the gap it closes, the order, the artifact it leaves behind, and what breaks if you run it out of order.

## Measured, or argued

Each combo says which it is. **Measured** means an eval compared it against an agent that could not read the skill files, and it won. **Argued** means the reasoning is sound and the evidence is missing, so treat it as a hypothesis, not a fact. The harness and the score table live in `readiness/evals/`.

Paths for every skill are in `skill-index.md`. Absolute paths, because pi has no Skill tool.

## C0: no skills

Gap: none. Every axis READY.

Cost: nothing. Artifact: the work itself. Use it far more often than the other combos, including for anything size S and for anything with an existing pipeline.

## C1: `triage`

Gap: axis 2 (claim unverified) or axis 3 (maybe already built), on work that already has a tracker issue.

Status: **argued, with a null result.** Eight runs against an agent that could not read the skill scored the same: both produced the right state and the right brief once the fixture stated its label convention and the rubric graded the issue file rather than the chat. Keep triage for its discipline and its housekeeping, not because it has been shown to decide better.

Order: gather, recommend, verify the claim, then label. Grill only if step 4 says the request is underspecified.

Artifact: an agent brief on the issue, plus the state label. The brief is the readiness artifact; `ready-for-agent` is just a label on it.

Out of order: labelling `ready-for-agent` before verifying the claim produces a brief for a problem nobody reproduced.

## C2: `grilling` + `domain-modeling`

Gap: axis 6 (decisions open), on work with no tracker issue, where the requester holds the decisions.

Status: **measured.** Six runs against an agent that could not read the skill: the unaided arm asked questions but never committed to a recommended answer, and never stopped for a round. 2/6 against 6/6. The failures are exactly the two behaviours the skill adds.

Order: grilling rounds, with domain terms sharpened in `GLOSSARY.md` as decisions land.

Artifact: a shared understanding plus the glossary entries. Then either C0 (build) or C7 (slice it).

Cost: one round of questions per frontier, and no more than two rounds before someone builds something. If the second round only re-asks the first, the real gap is not decisions but evidence; go back to axis 2.

## C3: `grill-with-docs`

Gap: same as C2, plus the decisions deserve to outlive the session.

Use when the decisions are architectural, or when the next builder is not in this conversation. Artifact: ADRs and glossary, not just agreement.

Do not run C2 and C3 together. C3 includes C2.

## C4: `triage` + `grilling`

Gap: axis 4 or 6 on a tracked bug or feature request whose edges are fuzzy.

Order: verify first (axis 2), then grill the scope and decisions, then write the brief. Verification before grilling, always: grilling a request whose claim is false wastes the requester's attention.

Artifact: one brief that carries scope boundaries, locked decisions, and acceptance criteria.

## C5: `architect` (which runs `arena`)

Gap: axis 6 where the open decision is the shape of code, and the shape is a one-way door.

Use only for L work with real blast radius. For mechanical work whose shape is already obvious, this is over-engineering and `principle-laziness-protocol` calls it out.

Artifact: types, signatures, module boundaries with unimplemented bodies, plus the rejected alternatives and why.

Out of order: architecting before axis 5 gives you a careful sketch of the wrong end condition.

## C6: `wayfinder`

Gap: axis 7 when the route is genuinely invisible and the work spans sessions.

Status: **argued, with a null result.** Six runs each arm, graded on the map written to disk: 6/6 both. An unaided agent that is told the route is foggy also writes a map. Its budget rule came out of this testing, and the discriminator worth trying next is whether the map holds decision tickets rather than build slices.

Order: name the destination, write the map, open decision tickets, resolve them one at a time. Its ticket types already include grilling, research, and prototype, so do not bolt C2 on top.

Artifact: a map plus closed decision tickets, ending in either a spec or a clear route.

Misuse: running it on a two hour job. If you can see the steps, you need C7, not a map.

## C7: `to-spec` then `to-tickets`

Gap: axis 7 when the route is visible but the work is too big for one session and nothing is written down.

Order: spec first, then tracer-bullet tickets with blocking edges, blockers first. `to-spec` synthesises what is already agreed and does not interview; if the decisions are not agreed, you needed C2 or C3 first.

Artifact: a spec plus one file per ticket, or native blockers on a real tracker.

Out of order: tickets before the spec slices the wrong thing. Tickets before the decisions lock the wrong slices permanently, because the blocking edges encode the mistakes.

## C8: verification skills

Gap: axis 8. Never a reason to park the work, always the first thing built.

- a verification-skill generator when the same check will be run repeatedly.
- a TDD cycle skill when the work is code with testable behaviour.
- a CI-latency audit skill when the gate is CI itself: audit first, split waiting from setup from work, and expect the fix to be setup rather than tests.
- a guarded page-rebuild workflow when the target is a page rebuild; it carries the 15 gates and the guarded cutover.
- a third-party sequencing principle when you need each slice verified before the next starts.

Artifact: a command whose failure is unambiguous, plus a recorded failing run from before the change.

## C9: `figure-it-out`

Gap: no narrower playbook fits: a migration, an ambitious multi-part change, or work a human reviews after stepping away.

Order: frame, design the workflow, run the loop, keep the audit trail, verify and hand back. It expects to consult the principle skills by name.

Misuse: using it for work that already has a pipeline. On this box that means `the publishing pipeline skill`, a guarded page-rebuild workflow, and a CI-latency audit skill all outrank it.

## C10: `handoff`

Gap: verdict PARK. The gap needs a person, a decision that is not yours, or a session that has ended.

Artifact: a self-contained brief a fresh session can start from with zero context. Use it instead of leaving the audit half-done in a transcript nobody will reread.

## C11: `fitness-audit`

Gap: the open question is not about the build but about the thing the build rests on: a library, a method, a vendor's claim, a measurement instrument.

Order: `fitness-audit` first, then back to axis 5 or 8 with a verdict you can attach to the plan. Its seven constituents (function, constraint, boundary, assumption, trigger, alternative, norm) are the input-audit counterpart to these eight axes, which audit the action. Do not run both on the same object: if the plan is the subject, this is the wrong skill.

Artifact: a fitness verdict carrying its evidence class: fit for whose purpose, to what tolerance, at normal or under stress.

## Longer sequences

Only two earn their length:

- **XL greenfield:** `wayfinder` → `to-spec` → `to-tickets` → (`architect` on the one-way door only) → `implement-spec`. The map resolves decisions, the spec states the end, the tickets order the build. Five items, and the middle three each fall away when the work is smaller.
- **Risky change to a live system:** a CI-latency audit, or recon of the rebuilt page first, then a verification-skill generator, then build behind the guard, then `code-review` or an interrogation review pass on the diff. Note that an interrogation review pass reviews code that exists; running it before the build produces opinions, not findings.

## Worked examples

**"Add a filter section to the product page."** Size M. Axis 1 fails first: theme work, live theme untouchable, guard must pass. Axis 2: nobody measured the current section behaviour. Combo: run the theme guard, duplicate the theme, then C2 for the one open design decision, then build. Do not run `wayfinder`. Do not write a spec for a section.

**"Rewrite and push this article."** `the publishing pipeline skill` already ships the route, the tests, and the push. Axes 7 and 8 are READY because the pipeline encodes them. Verdict GO, combo C0, then run the pipeline. This is the shortcut the meta-skill exists to take.

**"Our CI is slow."** Axis 2 fails and the probe is the audit: `scripts/ci_audit.py` splits each job into waiting, setup, and work. Combo: a CI-latency audit skill, which forbids optimising before that number exists. No grilling, because the requester's opinion of the cause is the thing under test.

**"Move the store off the page builder for good."** Size XL. Axes 6 and 7 both fail. Combo C6, `wayfinder`, with a guarded page-rebuild workflow consulted as the domain playbook for each page it rebuilds. Not C7: a spec written now would be fiction.

**"Make the checkout faster."** Axis 5 fails first. "Faster" is not falsifiable. Before any skill runs, get the number and the instrument (LCP, TTFB, conversion, all with a method). Then C1 or C8.
