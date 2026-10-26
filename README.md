# Skills

Four skills I use every day with Claude Code and Codex. By [Clément Rog](https://clementrog.com).

- **[crew](skills/crew/SKILL.md)**: Claude builds, Codex reviews, or the other way around. Every slice gets a fresh review.
- **[pick-up](skills/pick-up/SKILL.md)**: hit a usage limit? Paste the last reply into another agent and it carries on.
- **[design-critic](skills/design-critic/SKILL.md)**: a design crit of your running app, with the top fixes mocked.
- **[ports](skills/ports/SKILL.md)**: see the dev servers your agents left running, and stop them.

## Install

Claude Code:

```
/plugin marketplace add clementrog/skills
/plugin install crew@clementrog
```

The others are `pick-up@clementrog`, `design-critic@clementrog` and `ports@clementrog`.

Codex, or by hand:

```sh
git clone https://github.com/clementrog/skills
mkdir -p ~/.codex/skills ~/.claude/skills
cp -R skills/skills/crew ~/.codex/skills/
cp -R skills/skills/crew ~/.claude/skills/
```

## Good to know

- crew needs both `claude` and `codex`, signed in. Why I work this way: [My way to software engineering](https://clementrog.com/how-i-dev).
- pick-up reads your local transcripts in `~/.claude` and `~/.codex`. No network.
- design-critic comes from Brian Lovin's [Crit series](https://www.youtube.com/playlist?list=PLJu44Klx1pB_8GSOUeDNDllPICvMJKSut). The lenses are my reading of his videos, not his words.
- ports is macOS only. Set `PORTS_ROOTS` to change where your projects live.

I also make Mac apps for people who work with agents all day: [clementrog.com/studio](https://clementrog.com/studio).

## License

Released under the [MIT License](LICENSE).
