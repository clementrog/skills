# Skills

Four skills I use every day with Claude Code and Codex. Each one is a folder with a `SKILL.md`, and some come with a small script.

| Skill | What it does |
|---|---|
| [crew](skills/crew/SKILL.md) | Says who builds, who reviews and who lands, between Claude and Codex. A fresh session of the other model reviews every slice, blockers only, 3 rounds at most |
| [pick-up](skills/pick-up/SKILL.md) | Paste the last reply of a Claude Code or Codex session, and another agent finds that session on your Mac and carries on. Handy after a usage limit |
| [design-critic](skills/design-critic/SKILL.md) | A design crit of a running app: the agent walks real tasks, finds controls, context and feedback in the wrong place, and mocks the top fixes |
| [ports](skills/ports/SKILL.md) | Lists the dev servers listening on your Mac, by project, and stops the leftovers |

## Install

In Claude Code, add this repo as a plugin marketplace, then install the skills you want:

```
/plugin marketplace add clementrog/skills
/plugin install crew@clementrog
```

The others are `pick-up@clementrog`, `design-critic@clementrog` and `ports@clementrog`. Plugin skills carry a prefix, so crew runs as `/crew:crew`. Most of the time you don't type it: the agent loads a skill when your request matches its description.

Without the plugin system, or for Codex, copy the folder:

```sh
git clone https://github.com/clementrog/skills
mkdir -p ~/.claude/skills ~/.codex/skills
cp -R skills/skills/crew ~/.claude/skills/   # Claude Code
cp -R skills/skills/crew ~/.codex/skills/    # Codex
```

## What each one needs

- **crew**: both the `claude` and `codex` CLIs, signed in. The why behind it is in [My way to software engineering](https://clementrog.com/how-i-dev).
- **pick-up**: Python 3. It reads the local transcripts in `~/.claude` and `~/.codex` and makes no network request. The agent that carries on does see the excerpts it reads.
- **design-critic**: a way to run the app, such as browser tools or Playwright. With screenshots only it does a static crit and says so. The method comes from Brian Lovin's public [Crit series](https://www.youtube.com/playlist?list=PLJu44Klx1pB_8GSOUeDNDllPICvMJKSut); the lenses are my reading of his videos, not his words.
- **ports**: macOS. Projects are the folders under `~/projects`, `~/code`, `~/src` and a few others; set `PORTS_ROOTS` to change them.

## More

I write about how I work with agents at [clementrog.com/notes](https://clementrog.com/notes), and I make Mac apps for people who work with agents all day at [clementrog.com/studio](https://clementrog.com/studio). One of them, [Onadit](https://onadit.com), keeps every Claude Code and Codex session on your Mac and lets your agents search them, so pick-up is the one-off version of it.

Issues and pull requests are welcome.

MIT licence.
