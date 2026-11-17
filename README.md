# skills

[![skills.sh](https://skills.sh/b/rx3asarc/skills)](https://skills.sh/rx3asarc/skills)

Agent skills I actually use, published as they run. Plain `SKILL.md` folders — no framework, no build step, no dependencies.

```
npx skills add rx3asarc/skills
```

## The two worth reading

### `readiness/`

Answers one question before any non-trivial build: **is this work ready to be built, and if not, what closes the gap?** The output is a verdict plus the smallest set of skills that earns it — most work needs no skill at all.

Readiness is not a feeling about how well the idea was described. It is eight properties, each with evidence you can point at:

1. the actual problem, stated
2. the failure mode being prevented
3. the constraint that binds
4. the surface the change lands on
5. the definition of done, observable
6. the decisions still open
7. the first verifiable unit
8. how it gets proven

It ships with `references/axes.md`, `references/combos.md`, the routing index, the READINESS template, and an eval harness: ten tasks, three arms, three runs each, deterministic scoring, plus the score table from the last pass — including the tasks where the skill showed no signal.

### `fitness-audit/`

Situate a component — a tool, method, technique, library, institution, practice — before relying on it. A fitness-for-purpose audit in seven constituents: **function, constraint, boundary, assumption, trigger, alternative, norm.** The deliverable is a verdict carrying its evidence class: fit for *whose* purpose, to what tolerance, at normal load or at the tails and under stress.

The line that makes it an audit rather than a lookup: a fact you can look up — price, licence, who ships it — is a lookup. The audit starts where looking it up stops. `references/field-vocabularies.md` keeps the seven constituents from collapsing into each other.

## The supporting cast

`readiness` routes to narrower skills rather than improvising a combo. The generic ones ship here, unedited:

`triage` · `grilling` · `grill-with-docs` · `domain-modeling` · `to-spec` · `to-tickets` · `wayfinder` · `implement` · `implement-spec` · `diagnosing-bugs` · `prototype` · `code-review` · `handoff` · `retro` · `writing-for-agents` · `codebase-design` · `loopy`

## What is not here

Workflow skills bound to one company's storefront and ad accounts, and a third-party skill pack of someone else's work. Neither is mine to publish. A few prose passages name skills of that shape without publishing them, because the lesson needs a referent. Read them as "a skill like this exists", not as a broken link. `references/skill-index.md` lists only what ships.

## Notes

The `pi` caveat appears throughout: there is no `Skill` tool in that harness, so a skill is a file you read, and `disable-model-invocation: true` only means the model cannot auto-select it — nothing stops a run from loading it deliberately. Under a harness that exposes a skill tool, ignore the path plumbing and call the name.

Published verbatim, host-specific notes included, because the notes are usually the part that carries the lesson.
