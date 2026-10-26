---
name: ports
description: Show which local dev servers are listening on this Mac, by project, and stop the ones that are no longer needed. Use when the user types /ports, asks what is running on localhost, which ports are open, which project a port belongs to, or wants to kill leftover dev servers.
---

# ports

`scripts/ports`, in this skill's folder, does the work. Run it, don't re-derive the list with `lsof`. It runs on macOS only (it reads `lsof`, `ps` and `launchctl`).

| Ask | Command |
|---|---|
| What is running (default) | `<skill>/scripts/ports` |
| Also apps and background services | `<skill>/scripts/ports --all` |
| Stop given ports | `<skill>/scripts/ports kill 3000 8911` |
| Stop everything older than a duration | `<skill>/scripts/ports kill --older 7d` |
| One that ignored the first ask | `<skill>/scripts/ports kill -9 3000` |

Replace `<skill>` with this skill's directory. A project is the folder a server runs in, under one of the folders in `PORTS_ROOTS` (colon-separated; by default `~/projects`, `~/clients`, `~/code`, `~/src`, `~/dev`, `~/Developer` and `~/repos`). Elsewhere, the folder's own name is used.

## Showing the list

Run `scripts/ports` and show its rows as a table, grouped by project: port, project, folder, uptime, what it is. Keep the `lan` mark, it means the server is reachable from the network and not only from this Mac. Then one line per project on whether it looks in use: a server up for days in a project with no session open today is a leftover; one started in the last hours, or in a project being worked on now, probably is not.

If the arguments name a project (`/ports site`), show only that project.

## Stopping

- Stop only what the user named, by port, project or age. "Kill the old ones" means ask which, unless they gave a duration.
- A database (Postgres in a scratchpad) or anything in a project with a live agent session today: say so and ask before stopping it.
- `ports kill` refuses apps and launchd services by design. Don't work around it with `kill`.
- After stopping, run `scripts/ports` again and show what is left.
