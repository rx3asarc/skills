---
name: fitness-audit
description: Situate a component — tool, method, technique, library, institution, practice — before relying on it. A fitness-for-purpose audit in seven constituents.
disable-model-invocation: true
---

> **pi note:** there is no `Skill` tool in pi. To use another skill, read its `SKILL.md` with the read tool (path shown in the skill list) and follow it.

The user is not asking what X *is*. They are assembling premises for one unstated question — **may I rely on this?** — and the deliverable is a fitness verdict carrying its evidence class: fit for *whose* purpose, to what tolerance, at normal load or at the tails and under stress.

The constituents are seven: **function, constraint, boundary, assumption, trigger, alternative, norm.** A checklist of them grows without bound; this one is worth what its pruning is worth.

A fact you can look up — price, licence, who ships it — is a lookup, not an audit. The audit starts where looking it up stops.

## Prune

Put this to every question in your set:

> **What would I do differently under each answer?**

Drop every question whose answers all lead to the same action: it is decoration. Done when each surviving question names the action that changes with its answer.

## Lead with the load-bearing word

Then ask:

> **Which word am I least entitled to assume?**

That word is **load-bearing**: the one constituent the whole verdict stands on. Answer it first, to evidence, before anything else. Answer the rest to satisfaction.

Present the seven pruned and ranked by what their answers change. The enumeration is not the deliverable.

## The seven

**function** — Stated function, or the one actually performed? Which effects are the function and which side effects, and by whose accounting? If X serves a function, what serves *that* — and where does the regress terminate? It terminates at something taken as terminal, and that something is the real assumption.

**constraint** — Which constraint is *binding*? Hard or soft? Real, or inherited convention nobody has retested? What is the price of violating each?

**boundary** — Where is it drawn, and by whom? Technical or political? What is deliberately excluded, and does the exclusion survive a hostile case?

**assumption** — Which assumptions are tacit? Which single one, if false, kills the whole thing? What would I have to believe for this to be safe?

**trigger** — Necessary or sufficient conditions? Who exercises discretion over "it's triggered"? What happens at the margin, where the criterion is nearly met?

**alternative** — Functional equivalent or true substitute? Is the next-best worse in the tool or in the operator? Does the gap narrow or widen with scale?

**norm** — Who certifies this as best practice, on what evidence class? Justified, or merely widespread? What is the norm's half-life — what supersedes it, and is it already accruing debt?

Then the contrast itself: purpose-first smuggles in a comparison (compared to what?), comparison-first smuggles in a purpose (the outcome you chose to measure). Neither escapes the other, so **say which term you treated as known and which as the unknown** — that choice is what you are taking on faith.

## Hard rules

- **Tag every claim with its evidence class** — mechanism, single study, consensus, anecdote, assumption — and keep the tags visible in the prose.
- **A comparison needs a real null** — do nothing, or the incumbent — with effect size stated beside its cost. A win without its price is not a finding.
- **Name the failure mode and the gaming vector.** How does it fail — silently? Who is optimising against it? Payer and beneficiary are often different parties; say which is which.
- **Separate descriptive from justified norms.** "Everyone does this" answers the first; the verdict needs the second, including the norm's own failure mode.
- **State the falsifier** — what evidence would flip the verdict — and the next check that would settle it.
- **Mark inferred from verified.** When the thing under audit is your own choice or your own work, hold it to the verdict you would give a stranger's.

## Output shape

1. **The sentence** — one line naming the thing and the audit.
2. **Load-bearing question** — the word you were least entitled to assume, and its answer with evidence class.
3. **Verdict** — rely / rely with conditions / don't, plus what flips it.
4. **Covered, deliberately skipped, unknown** — three explicit lists.
5. **The next question** — what would change the answer, and who could check it.

Size to the decision: a tool choice gets a page; an institution gets more, and splits into rounds.

## Dialects

When the user's field already has vocabulary for this analysis — sociology, behavioural economics, systems engineering, philosophy of technology — read [`field-vocabularies.md`](field-vocabularies.md) and answer in their words instead of inventing a private one.

## Pairs

**grilling** (`grilling/SKILL.md`) forces a choice once the audit is on the table; this skill supplies the audit when the choice is already live.
