---
name: handoff
description: Park work for a later session as a self-contained handoff so a fresh session can pick it up with zero context. Use when the user says "hand this off", "handoff", "park this", "leave it for another session", "pick this up later", "note it and move on", "so I can solve this separately", "write this up for later", or whenever you finish work that (a) needs a decision that is not yours, or (b) needs building but cannot be finished now. Also use when a session is about to end with open threads, or when the user wants a repeatable process for deferring work across all future topics. Trigger even without the word "handoff" — any time work is being deferred to another session, this is the mechanism.
---

# Handoff — parking work so another session can pick it up

## The one test that matters

> A fresh session with **zero context** must be able to either make the decision or execute the
> work, using **only the handoff file**. If it has to ask "what did you mean by X?", it is not
> finished.

Everything below exists to pass that test.

## Canonical store

`~/handoffs/` — topic-agnostic, one directory for every area. **Not** in a repo, deliberately:
handoffs are often *about* a repo you must not write to (guardrail-gated paths, trees with
documented two-writers incidents). See `~/handoffs/_CONVENTIONS.md` for the full conventions.

```
~/handoffs/
  _TEMPLATE.md   _CONVENTIONS.md   INDEX.md   done/
  _evidence/<slug>/          ← reproducible scripts + captured output for a handoff
  YYYY-MM-DD-slug.md
  legacy/                    ← pre-convention handoffs, indexed only
```

## The CLI

```bash
handoff new <slug>             create from the template (dated, status=open)
handoff list                   what is parked — priority, status, what it needs, age
handoff show <slug>            print the whole file
handoff resume <slug>          print ONLY the paste block, ready to copy into a new session
handoff note <slug> "text"     append a dated update
handoff close <slug> --note …  finish it (status=done, moves to done/)
handoff doctor [slug]          validate frontmatter + required sections, and scan for secrets
handoff index                  regenerate INDEX.md
handoff search <term>          grep everything including closed
handoff areas                  the area vocabulary in use
```

`handoff doctor` is the gate: it fails on missing frontmatter, missing required sections,
leftover template comments, placeholder text, a suspiciously short body, and — importantly —
**any live credential format** (Shopify/GitHub/Slack/Google keys, JWTs, PEM blocks, `NAME=value`
password blocks). Run it before you consider a handoff done.

## Process

1. **Recognise the moment.** Work is being deferred when: a decision belongs to someone else;
   the work is too big for this session; it is blocked on a provider or another task; or you
   found something real while doing something else. All four are handoff moments.
2. **`handoff new <slug>`** — slug = what it is about (`wellness-kit-canonical`).
3. **Fill it in, in this order**, because it forces the thinking:
   - **TL;DR** — 3 bullets. If you cannot compress it, you do not understand it yet.
   - **What is needed** — the decision (with options and their costs) or the ordered work.
   - **Verified facts** — a table where **every row cites its evidence**: a command, a path, a
     sha, a URL. No citation ⇒ it is not a fact, it goes in §7.
   - **What was NOT changed** — the safety receipt. Name what you touched and what you did not.
   - **Why it is parked** — the blocker and whose action unblocks it.
   - **Paste block** — the self-contained opener, in a fenced block.
   - **Open unknowns** — split into *unverified* (must not be read as fact) and *known-unknown*
     (needs someone else's answer). This section is what stops a guess becoming a passed-on premise.
4. **Make the evidence reproducible.** Do not cite `/tmp` — it gets wiped. Put scripts and
   captured output in `_evidence/<slug>/` with a header comment saying how to re-run them.
5. **`handoff doctor <slug>`** — must pass.
6. **`handoff index`** — so it shows up in the parked-work view.

## Why evidence citations are non-negotiable

An uncited number in a handoff becomes a **false premise** in the next session, and the next
session has no way to know. This has already happened in practice: a claim about which product
handle the ad landers pointed at was wrong, and the correction cost a full re-derivation. Cite
the command. If you cannot, say "unverified".

## Do not

- **Do not resolve a decision that is not yours.** Naming options and tradeoffs is the job;
  choosing is the owner's. Set `needs: decision` and `owner:`.
- **Do not put a secret in a handoff.** The values live in `~/.secrets.env` and the agent
  reads them from the environment. A key in a handoff file is a burned key.
- **Do not write a handoff into a repo** unless the user asks for it there.
- **Do not leave a stale index.** Close finished handoffs — `INDEX.md` showing phantom open work
  is worse than an empty index.
