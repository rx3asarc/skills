# The eight axes

Walk them in order. Each one has a probe you can run now, a test for real evidence, and the skills that close a gap. Stop walking at the first NOT READY that blocks everything downstream, and report it; there is no value in auditing axis 7 when axis 2 failed.

Status vocabulary: READY, NOT READY, UNKNOWN. UNKNOWN is not a soft READY.

## Axis 1: constraints and guardrails known

What the build must not break, and who said so.

Probe: read the rulebook for the domain before anything else (`~/config/AGENTS.md` in full, plus the domain skill when one exists). Name the constraints in one line each.

Evidence: a named constraint and where it lives. "Live theme the live theme is untouchable, guard is `theme_guard.py check`" beats "I will be careful".

Closers: `the theme workflow skill` (theme work), `ci-latency` (workflow work), `the ads skill` (campaign work), `design-mastery` (image work). No skill closes it for a new domain; reading the rulebook does.

Fake version: skimming the rulebook and asserting compliance. If a guard command exists, run it and paste the output.

## Axis 2: the problem is real

For a bug, reproduce it. For an enhancement, find the current behaviour and where it hurts. For a performance or cost claim, measure it.

Probe: run the thing, or run the measurement the claim implies. Cheap and read-only.

Evidence: a command and its output, a URL, a screenshot, a number with units. "Users complain" is not evidence.

Closers: `diagnosing-bugs`, `triage` step 3, `ci-latency` for anything that starts with "CI is slow", `recall` when there is history on this box.

Fake version: verifying the claim in prose rather than in the system, then planning against a problem that does not exist.

## Axis 3: not already built, not already rejected

The cheapest NO GO there is.

Probe: search the codebase by domain concept, not by the requester's wording. Then read `.out-of-scope/*.md` for prior rejections and any `DECISIONS.md` or ADR directory.

Evidence: where you looked and what you found, including the search that came up empty.

Closers: `triage` step 1, `recall`, `why` when the rejection reason is old and you need the reason, not the ruling.

Fake version: grepping for the exact noun in the request, finding nothing, and declaring it new.

## Axis 4: scope is bounded

The work has an edge. You can say what is out and why.

Probe: write the out-of-scope list. Three lines of "not doing this" is the whole test.

Evidence: the out-of-scope list, plus the things adjacent work would tempt a builder to swallow.

Closers: `triage` (agent brief carries scope boundaries), `grilling`, `to-spec`.

Fake version: "scope is clear" with no exclusions written. Unbounded scope is the most common reason real work stalls.

## Axis 5: done is a falsifiable predicate

You can state the end condition, and someone else's check on it can disagree with you.

Probe: write the acceptance criteria as things a stranger could test, with numbers where numbers exist.

Evidence: each criterion has a check attached. "Articles are good" is not a criterion; "the page returns 200 over HTTPS on `www.`, LCP under 2.5s on a throttled mobile run, and no unsourced claim in the copy" is three checks.

Closers: `principle-prove-it-works`, `to-tickets` (each ticket carries one), the agent brief template in `triage/AGENT-BRIEF.md`, `page-rebuild` when the target is a rebuilt page with its 15 gates.

Fake version: criteria that restate the description of the work. "Add the section" is not a done predicate.

## Axis 6: decisions are locked

Every choice a builder would otherwise make alone has been made, or explicitly delegated with bounds.

Probe: list the decisions the work forces. Mark each as settled, delegated, or open. Only open ones block.

Evidence: each settled decision with its reason, in `GLOSSARY.md`, an ADR, or the brief. Decisions that live only in chat are lost decisions.

Closers: `grilling` (rounds over the design tree), `grill-with-docs` (same, writing ADRs and glossary as it goes), `domain-modeling` for vocabulary, `architect` and its `arena` sub-step for one-way doors in code shape.

Fake version: locking decisions the requester never agreed to. Readiness the builder invented is a trap for whoever builds.

## Axis 7: the route is known and sequenced

The steps exist, each lands on its own, and the risky unknowns are first.

Probe: sketch the sequence. If you cannot order the steps without guessing, the route is unknown, not merely un-ticketed.

Evidence: an ordered list of independently landable slices, with blockers marked, each small enough for one session.

Closers: `wayfinder` when the route is genuinely invisible and the work spans sessions (it maps decision tickets and resolves them one at a time), `to-tickets` when the route is visible and needs slicing, `implement-spec` to consume the result.

Fake version: a route that is a wish list. If half the steps depend on an unanswered question, `to-tickets` will lock the wrong slices, which is worse than no tickets.

## Axis 8: verification can go red

A check exists that fails when the work is wrong, and you have seen it fail.

Probe: run the check against the current, unbuilt state. It must fail, or report a number that will move.

Evidence: the failing run, or the baseline number from the pre-change state.

Closers: `ci-latency` (which starts with an audit that splits jobs into waiting, setup, and work before anyone optimises), `create-verification-skill` for repeated checks, `tdd` for code-shaped work, `page-rebuild` for rebuilt pages, `principle-sequence-verifiable-units` for ordering.

Fake version: a check that reports green on an unbuilt system. That is worse than no check, because it buys trust it did not earn.

## Reading the result

The chain is one directional: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. A failure at axis 1 or 3 ends the audit with NO GO or PARK. A failure at 2, 4, or 5 is cheap and mostly yours to fix without asking anyone. Failures at 6 and 7 are the ones worth a grilling session. A failure at 8 is never a reason to delay the build; it is the first thing you build.
