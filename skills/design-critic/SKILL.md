---
name: design-critic
description: Design crit of a running product or flow, done the way a senior product designer does one — walk real tasks through the app, find where controls, context and feedback sit in the wrong place, and show the top fixes as rough before/after. Use when the user asks for a design crit or critique, a UX review, a teardown, "fresh eyes", "what's wrong with this app / flow / navigation", "why does this feel confusing or clunky", or wants a second opinion on a product that already exists or was just built, even if they only share a URL, a repo or a few screenshots. It critiques across screens and through interaction. It does not build screens or check one screen against layout rules (that is product-design), and it does not pick colors or fonts (frontend-design).
---

# Design critic

A crit asks a different question from a review. A review takes one screenshot and asks whether the screen is built to the rules. A crit takes a running product and asks whether it makes sense to someone doing a job in it: is each control where its effect is, can they see what they are acting on, do they see what their action did. Most of those failures are invisible in a screenshot. They show up when you click.

The method is distilled from five recorded crits of real products by Brian Lovin, a working product designer, in his public [Crit series](https://www.youtube.com/playlist?list=PLJu44Klx1pB_8GSOUeDNDllPICvMJKSut) (Placemark, Buttondown, Outline, Less Annoying CRM, Sizzy). The lenses and their wording are this skill's reading of those videos, not his. That is a small sample of one person's practice, so treat the lenses as questions to ask, not laws.

## 1. Frame the crit

Write this in a few lines, show it to the user, and continue. Don't interview.

- **Product and user**: what it is, who works in it, how often. If the product-design skill is installed, borrow its brief vocabulary (mode, posture, primary object). Read the project's `DESIGN.md` if there is one.
- **Constraints**: what must not move. People who use a product every day know where things are, so a proposal that relocates everything can be right on paper and still be rejected. If nobody told you, assume the layout and feature set stay, and say so.
- **Jobs to walk**: pick two or three. The most frequent job. One job that creates or configures something across several screens (invite, permissions, setup). One high-consequence action (delete, send, publish, pay).

## 2. Walk it

Use the real thing. Run the app or open the URL with whatever browser automation you have (Chrome tools, Playwright, a preview server). Keep every screenshot in a scratch folder; they are your evidence.

1. **Survey.** Visit every top-level destination and open every menu once, with a screenshot of each. This is the inventory of chrome that the scope lens needs.
2. **Walk each job** start to finish as its user would, with realistic data. At every step take a screenshot before and after the action, and note four things: what I expected, what happened, where I am now, what Back would do.
3. **Probe rows and toolbars.** Where one row or bar holds several targets, hover each one and screenshot the hover state before clicking.

Stop before anything irreversible on real data. Walk up to the confirmation of a delete, send or payment, capture it, then cancel. Go through only on a test account or seeded data.

**If you cannot run it** (screenshots, a recording or a design file only), do a static crit and say so at the top of the report. Scope, prominence, treatment, scan lines and simplification loss survive stills. Consequence and signifier mostly do not, so list those as things to check, not as findings.

## 3. Lenses

Go through all eight for each job. How to test each one, what the fix usually looks like and worked cases are in `references/lenses.md`; read it before your first crit in a session.

| Lens | Question | Fails like |
|---|---|---|
| **Scope** | What does this control change (app, account, workspace, view, selected object), and does its position say so? | Account menu and document menu side by side in one strip; a team-labelled entry that opens personal settings |
| **Context** | While I decide or act, can I still see what I am acting on? | A full-page confirmation that covers the thing being deleted; a mixed activity feed that does not say whose record each event belongs to |
| **Consequence** | After I act, is the result visible where I acted? | The person I added vanishes from the list and shows up two screens back |
| **Signifier** | Does it look like what it does before I click? | One hover highlight over a row with three different actions; clickable items that look like plain text |
| **Prominence** | Does size and position match how often the job is done? | Rarely used export controls holding fixed space while the main list scrolls inside a small box |
| **One treatment, one meaning** | Does the same color or shape always mean the same thing? | One blue for titles, fields and footers; green for both Save and a dropdown |
| **Scan lines** | In repeated rows, does each field keep its position? | Stars and metadata landing at a different x on every row |
| **Simplification loss** | What did the cleanup remove that people needed? | A "cleaner" redesign with smaller text, no click targets and no event metadata |

Start with scope. It came up in all five source crits and drove the largest change in most of them, and it is cheap to run: list the controls, tag what each one changes, look for regions that mix tags.

## 4. Turn observations into a crit

A crit is not the list of everything you noticed.

- **Three themes at most.** A theme is one cause that explains several observations ("controls don't show what they act on" explains a mixed top strip, a misplaced tab and a buried undo). A list of twenty nits gets skimmed and ignored; three causes get fixed. What you observed and still believe, but that fits no theme, goes under Smaller things. Don't let the cap delete it.
- **Rank from the outside in.** First where regions begin and end and what each one owns, then grouping inside regions, then states (selected, active, hover), then row detail. Detail fixes are thrown away when a region moves.
- **Sort every claim into observed, proposed or question.** *Observed*: it happened and you have the screenshot. *Proposed*: a change you recommend. *Question*: the answer depends on usage or intent you cannot see ("is this inner scroll a real problem or an artifact of demo data?"). Before filing a question, check what you can: analytics, routes, the default landing screen, the code. A proposal that rests on a guess about usage has to say so.
- **Write the keep list.** Name what works and has to survive the fixes. It is a constraint on your own proposals, not a courtesy.
- **Name the cost.** If a fix trades something away (a full-width header moves actions people find by position), say it. If you see a problem and have no fix, say that too. "Still feels detached, no fix yet" is more useful than an invented one.
- **Feel words need a cause.** "Heavy", "floaty", "technical" and "enterprise" are fine as a starting point. Each becomes a finding only once you can point to what on screen produces it. If product-design is installed, its `references/diagnose.md` maps feelings to causes.
- **More signal is a valid fix.** Sometimes the answer is a border, a stronger selected state or larger text. That does not contradict product-design's "lowest rung that works": a click target nobody can find is a rung that is not working.

## 5. Show the after

A designer ends a crit with a rough mock, because a described fix is easy to nod at and hard to judge. You can make one cheaply, so do it for the top theme, and for up to three.

- **Where**: in a git worktree or scratch copy of the repo if you have it, in a connected design tool (Paper, Figma), or as a single HTML wireframe. Leave the user's working tree alone unless they asked you to fix things.
- **Fidelity**: structure only. Keep real content and the existing styles, use placeholders for icons, leave unrelated areas blank. One glance should show the move and nothing else should invite debate. `references/cases.md` shows what rough looks like.
- **Same shot**: screenshot the same step again so before and after can sit side by side.
- **Check your own after** against the keep list, against the other jobs you walked, and with the simplification-loss lens. In the source crits the designer's own first pass failed that lens and had to be walked back.

## 6. Report

Reply in the conversation with this shape. Write a file only if asked.

```markdown
# Crit: <product>
Walked: <job 1>; <job 2>; <job 3>. <Live | Static: screenshots only>. <n> steps captured in <folder>.
Assumed: <constraints you assumed>

<Two sentences: what the product does well, and where it loses people.>

## 1. <Theme, stated as what is wrong>
- Observed: <what happened, step by step> (<screenshot paths>)
- Lens: <scope | context | …>. Who it costs: <which user, doing what>
- Proposed: <the change>. Before <path> → after <path>
- Cost: <what the change trades away, or "none seen">

## 2. … (three themes at most)

## Keep
- <what works and must survive>

## Questions
- <what depends on usage or intent, and how to find out>

## Smaller things
- <five at most, one line each>

## Not checked
- <jobs, states, widths or lenses you could not test>
```

## Boundaries

- This is not the product-design review. Don't run its checklist or measure spacing. If a screen plainly has rule-level problems (cards in cards, no rhythm), say "run a product-design review on this screen" in one line under Smaller things.
- Colors, fonts and brand belong to the design system. Raise them only through the one-treatment and simplification-loss lenses.
- Building the approved fixes for real is a separate job. Structural ones go back through product-design.
