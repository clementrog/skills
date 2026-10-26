---
name: crew
description: Who builds, who reviews and who lands work, between Claude and Codex. Use when the user gives roles ("codex builds, claude reviews", "you land"), asks for a review by the other model, asks to build a slice and get it reviewed, or asks to merge, land, ship, install or deploy finished work. Also when they type crew.
---

# Crew

The user chooses who plays which role, in their own words, and can change it at any time, in any session. Claude and Codex can each take any role. Nothing here fixes a direction.

- **Front door:** the session the user is talking to. It reports to them and starts the other roles. They may talk to several sessions; this is a convenience, not a rule.
- **Builder:** makes the change.
- **Reviewer:** checks the change against what the user asked. Always a fresh session, never the builder's own context. By default the other model; if the user names the same model, use a fresh session of it.
- **Lander:** puts reviewed work on `main` and prepares the release.

If the user has not said: the front door builds and lands, the other model reviews. Say in your first reply who plays what, in one line, so they can change it.

## Rules

1. One writer per folder. A lone builder works in the main folder, on its own branch. A second writer takes a worktree inside the repo (`.worktrees/<branch>`, never `/tmp`), installs dependencies from its own lockfile, and copies the local config it needs (`.env`).
2. Each slice gets a review against what the user asked: blockers only, at most 3 rounds. A blocker still held after the builder's answer goes to the user with both positions. A review starts only once every check and journey the repo names for the change has passed: the reviewer reads the code and doesn't run it, so its SHIP covers the code, not how the product behaves.
3. One landing at a time per repo. Land exactly the reviewed commit. If landing needs a code edit (a conflict), that edit goes back to the reviewer. Check the combined result before `main` moves.
4. Before an install or deploy, list everything that changes compared with what is live or installed, and release only what is meant to go.
5. Ask the user before anything that cannot be undone, reaches other people, or replaces one of their daily apps, unless they have allowed automatic installs for that app.

How to brief, how many slices and which checks: your call, unless the user says.

## Model and effort

The model and effort the user names take precedence. Otherwise pick the reviewer's model by what a wrong SHIP would cost. For Codex, for example:

- A strong model at high effort (`gpt-6.1-sol` at `xhigh` when this was written) for routine, contained slice reviews
- The strongest model available (`gpt-6-astra` at `xhigh`) when a wrong SHIP could be hard to undo: migrations or backfills, auth or permissions, cross-device or cross-process sync, actions that send to others or move money, or a concrete builder doubt about data, security or reversibility
- The strongest model for consequential decisions about architecture, scope, dependencies or conflicting requirements

Choose by concrete consequences and uncertainty. An ordinary stored-data write or a large file count alone is not an escalation trigger. Keep Claude's CLI default unless the user names another selection.

On consequential slices, consider a short challenge of the plan before building: mistaken assumptions, likely failure paths, and whether a smaller solution works. This is optional, not an extra phase for every slice.

Choose the review tier before round 1. Keep the same session, model and effort for follow-up fixes. If a stronger model becomes necessary, start a fresh review with the current brief, diff and unresolved blockers. It still counts toward the same three-round limit. Report an unavailable named selection rather than silently substituting.

## Starting the other model

Always call `claude` and `codex` by name, started from inside the repo. Run them in the background, prompt on stdin, answer in a file. Keep the session id to send rounds 2 and 3 to the same session. Do not edit the repo while a review reads it.

| Role | Codex | Claude |
|---|---|---|
| Review | `codex exec -s read-only -C <repo> --json -o <reply> - < <brief>` | `claude -p --permission-mode plan --output-format json < <brief> > <reply.json>` |
| Next round | `codex exec resume <thread_id> -c sandbox_mode="read-only" -o <reply> - < <followup>` | `claude -p --resume <session_id> --permission-mode plan --output-format json < <followup> > <reply.json>` |
| Build or land | `codex exec -s workspace-write --add-dir <repo>/.git -C <folder> --json -o <reply> - < <brief>` | `claude -p --permission-mode auto --output-format json < <brief> > <reply.json>`, started in `<folder>` |

- Codex's `thread_id` is on the first `thread.started` line of `--json` output; Claude's `session_id` is in its JSON reply, with the answer in `result`.
- `--add-dir <repo>/.git` lets Codex commit from a worktree, whose git data lives in the main folder.
- Codex calling `claude` needs the network and `~/.claude`: in `codex exec` add `-c sandbox_workspace_write.network_access=true --add-dir ~/.claude`; in an interactive Codex session, ask for the escalation.
- A `codex exec` given its prompt as an argument waits on stdin: pass `< /dev/null`.
- Pass the selected model and effort on every review round, including resumes: Codex `-m <model> -c 'model_reasoning_effort="<effort>"'`, Claude `--model <model> --effort <effort>` when selected. Resume does not pin them, and the front door's model selection does not choose a subprocess reviewer's model. Include the actual model and effort with its verdict.
- Give a review 30 minutes. A failed or timed-out review is not an approval; run it once more.

## The review brief

The front door writes it. It holds: what the user asked, in their words, with its "Done when" line; what changed and where the diff is (base commit); what was run and seen; what the builder is unsure of. A default ending that has worked:

```
Read the real diff in this repo. Do not trust my summary.
Report blockers only: data loss or corruption, a security or privacy leak,
an action that cannot be undone, behaviour that breaks what was asked,
or a claim in the summary that the code does not back.
For each blocker: file and line, the concrete way it fails, the smallest fix.
No style, no refactors, no extra tests, no nice-to-haves.
First line of your reply: VERDICT: SHIP or VERDICT: FIX.
```

Keep each round's reply in its own file, so an old SHIP is never read as the current verdict.

When a reviewer's restraint and the user's stated look conflict (motion, colour), the user's look wins. Ask them before stripping it.

## While a review runs

- Tell the user which review is running and on which round, then end the turn. You are woken when the background job ends; don't poll it.
- Cap the reviewer at 30 minutes: put `perl -e 'alarm shift; exec @ARGV' 1800` in front of `codex exec` or `claude -p`. A review stopped by the cap is a failed review: run it once more.

## Goals

A `/goal` condition holds 4,000 characters, so point it to a spec file. The model that decides "done" reads only the conversation, so the goal names what the last message must show, with a SUCCESS and an INCOMPLETE ending.

## Landing

- Take the landing lock: `mkdir <repo>/.git/crew-landing` (it fails if another lander holds it). Write who and when inside; remove it when done. One older than an hour with no live session behind it can be removed, saying so.
- Merge reviewed branches in an order that works: what others depend on first, then the smallest risk. Note the reviewed commit of each.
- Release the way the repo's README or AGENTS.md says. If it says nothing, ask the user once and write the answer there.
- Before installing over one of the user's daily apps, read the whole build log for "NOT", "missing", "skipped".
- Afterwards remove merged worktrees, and merged branches unless the repo keeps them.

## Handoff

End with four short parts, so someone outside the chat can check the work:

- **Asked:** what the user asked, in their words, including scope changes on the way
- **Changed:** commits or files
- **Verified:** what you ran or saw, against the "Done when" line
- **Needs me:** one question or action for the user, or "nothing"

Then one line: who built, who reviewed (verdict, rounds), who landed, and what is released or waiting for the user.
