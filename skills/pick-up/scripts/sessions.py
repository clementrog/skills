#!/usr/bin/env python3
"""Read-only, bounded context recovery from local Claude Code / Codex JSONL."""

import argparse
import datetime
import json
import os
from pathlib import Path
import re
import unicodedata


def rows(path):
    with path.open(encoding="utf-8", errors="replace") as stream:
        for line, raw in enumerate(stream, 1):
            try:
                obj = json.loads(raw)
            except ValueError:
                continue  # A running session can have an unfinished final line.
            if isinstance(obj, dict):
                yield line, obj


def text_blocks(content):
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    return "\n".join(
        block.get("text", "") for block in content
        if isinstance(block, dict)
        and block.get("type") in {"text", "input_text", "output_text"}
        and isinstance(block.get("text"), str)
    )


def message(row):
    kind = row.get("type")
    if kind in {"user", "assistant"}:
        body = row.get("message") or {}
        text = text_blocks(body.get("content"))
        if row.get("isCompactSummary"):
            return "compaction_summary", text
        if row.get("isMeta") or text.lstrip().startswith((
            "<task-notification>", "<local-command", "<command-name>",
            "Base directory for this skill:", "[Usage limit reached;",
        )):
            return "context", text
        # Newer Claude versions identify machine-origin user rows explicitly.
        origin = (row.get("origin") or {}).get("kind")
        if kind == "user" and (origin and origin != "human"):
            return "context", text
        return kind, text
    if kind == "response_item":
        body = row.get("payload") or {}
        if body.get("type") == "message" and body.get("role") in {"user", "assistant"}:
            role = body["role"]
            text = text_blocks(body.get("content"))
            if role == "user" and text.lstrip().startswith((
                "# AGENTS.md instructions", "<environment_context>",
                "<permissions instructions>", "<turn_aborted>",
            )):
                role = "context"
            return role, text
    if kind == "compacted":
        return "compaction_summary", (row.get("payload") or {}).get("message", "")
    return None, ""


def inspect(path, metadata_only=False):
    stat = path.stat()
    meta = {"path": str(path), "session_id": path.stem,
            "modified": datetime.datetime.fromtimestamp(
                stat.st_mtime, datetime.timezone.utc).isoformat(),
            "bytes": stat.st_size, "cwd": [], "agent": "unknown"}
    messages = []
    for line, row in rows(path):
        if row.get("type") == "session_meta":
            meta["agent"] = "codex"
            payload = row.get("payload") or {}
            meta["session_id"] = payload.get("id", meta["session_id"])
            cwd = payload.get("cwd")
        else:
            if row.get("type") in {"user", "assistant"}:
                meta["agent"] = "claude"
                meta["session_id"] = row.get("sessionId", meta["session_id"])
            cwd = row.get("cwd")
        if isinstance(cwd, str) and cwd not in meta["cwd"]:
            meta["cwd"].append(cwd)
        role, text = message(row)
        if role and isinstance(text, str) and text.strip():
            messages.append({"line": line, "role": role,
                             "timestamp": row.get("timestamp"), "text": text})
        # Discovery only needs the header and the first meaningful request.
        if metadata_only and line >= 80 and meta["cwd"]:
            break
    meta["first_request"] = next((m["text"][:300] for m in messages
                                  if m["role"] == "user"), None)
    return meta, messages


def session_paths(agent, home):
    if agent == "claude":
        return (home / "projects").glob("*/*.jsonl")
    else:
        return (p for root in ("sessions", "archived_sessions")
                for p in (home / root).rglob("*.jsonl"))


def candidates(args):
    default = ".claude" if args.agent == "claude" else ".codex"
    home = Path(args.home).expanduser() if args.home else Path.home() / default
    paths = session_paths(args.agent, home)
    paths = sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)
    found = []
    for path in paths:
        meta, _ = inspect(path, metadata_only=True)
        if args.cwd and not any(Path(c).resolve() == Path(args.cwd).expanduser().resolve()
                                for c in meta["cwd"]):
            continue
        found.append(meta)
        if len(found) >= args.limit:
            break
    return {"agent_home": str(home), "sessions": found,
            "scope": "Exact recorded cwd. Other worktrees may need their own cwd."}


def normalized(text):
    text = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)
    return " ".join(re.findall(r"[^\W_]+", unicodedata.normalize("NFKC", text).casefold()))


def shingles(words):
    return {tuple(words[i:i + 5]) for i in range(len(words) - 4)}


def overlap(query, query_words, query_shingles, text):
    text = normalized(text)
    words = text.split()
    if len(words) < 12:
        return 0.0, "too_short"
    if f" {query} " in f" {text} ":
        return 1.0, "normalized_exact"
    # Allow the pasted output to have a short command or request around it.
    if len(words) >= len(query_words) * 0.7 and f" {text} " in f" {query} ":
        return 1.0, "normalized_exact"
    shared = query_shingles & shingles(words)
    return len(shared) / len(query_shingles), "phrase_overlap"


def tail_rows(path):
    with path.open("rb") as stream:
        stream.seek(0, 2)
        start = max(0, stream.tell() - 262144)
        stream.seek(start)
        if start:
            stream.readline()  # Discard a possibly incomplete first row.
        for raw in stream:
            try:
                row = json.loads(raw)
            except (ValueError, UnicodeError):
                continue
            if isinstance(row, dict):
                yield row


def match_paste(args):
    query = normalized(Path(args.paste_file).expanduser().read_text(encoding="utf-8"))
    query_words = query.split()
    if len(query_words) < 12:
        return {"status": "insufficient_text", "matches": [],
                "reason": "Paste a distinctive paragraph of the last reply, or name the project. No session ID is needed."}
    query_shingles = shingles(query_words)
    agents = ("claude", "codex") if args.agent == "auto" else (args.agent,)
    homes = []
    for agent in agents:
        if args.home:
            roots = [Path(args.home).expanduser()]
        else:
            roots = [Path.home() / (".claude" if agent == "claude" else ".codex")]
            configured = os.environ.get("CLAUDE_CONFIG_DIR" if agent == "claude" else "CODEX_HOME")
            if configured:
                roots.append(Path(configured).expanduser())
        for root in roots:
            if (agent, root.resolve()) not in homes:
                homes.append((agent, root.resolve()))
    paths = {}
    for agent, home in homes:
        for path in session_paths(agent, home):
            try:
                paths[path.resolve()] = (agent, path.stat().st_mtime)
            except FileNotFoundError:
                continue
    ordered = sorted(paths, key=lambda p: paths[p][1], reverse=True)
    selected_paths = ordered[:args.max_sessions]
    matches = []
    unreadable = 0
    for path in selected_paths:
        try:
            if args.cwd:
                meta, _ = inspect(path, metadata_only=True)
                if not any(Path(c).resolve() == Path(args.cwd).expanduser().resolve()
                           for c in meta["cwd"]):
                    continue
            best = (0.0, "", "")
            records = (row for _, row in rows(path)) if args.full else tail_rows(path)
            for row in records:
                role, text = message(row)
                # A pasted reply in the receiving user's message is not its source.
                if role != "assistant" or not text:
                    continue
                score, method = overlap(query, query_words, query_shingles, text)
                if score > best[0]:
                    best = (score, method, text)
            if best[0] >= 0.6:
                meta, _ = inspect(path, metadata_only=True)
                matches.append({**meta, "score": round(best[0], 4),
                                "method": best[1], "matched_reply_preview": best[2][:300]})
        except (OSError, UnicodeError):
            unreadable += 1
    matches.sort(key=lambda m: m["score"], reverse=True)
    status = "not_found"
    if matches:
        status = "matched" if len(matches) == 1 or matches[0]["score"] - matches[1]["score"] >= 0.15 else "ambiguous"
    return {"status": status, "matches": matches[:5], "matching_sessions": len(matches),
            "searched_sessions": len(selected_paths), "available_sessions": len(ordered),
            "unreadable_sessions": unreadable, "agent_homes": [str(root) for _, root in homes],
            "scope": "Full transcript text" if args.full else "Last 256 KiB of each transcript",
            "notice": "Matches assistant replies only. Formatting and line wrapping are normalized. Ambiguous matches require a project or a choice by description, never a session ID."}


def packet(args):
    path = Path(args.path).expanduser().resolve()
    meta, messages = inspect(path)
    eligible = [i for i, m in enumerate(messages) if m["role"] != "context"]
    priority = []
    def add(indices):
        for i in indices:
            if i not in priority:
                priority.append(i)
    if args.around is not None:
        add(sorted(range(len(messages)), key=lambda i: abs(messages[i]["line"] - args.around))[:16])
    else:
        users = [i for i in eligible if messages[i]["role"] == "user"]
        summaries = [i for i in eligible if messages[i]["role"] == "compaction_summary"]
        assistants = [i for i in eligible if messages[i]["role"] == "assistant"]
        add(users[:1])
        add(users[-1:])
        add(summaries[-1:])
        add(assistants[-1:])
        terms = args.query.casefold().split() if args.query else []
        if terms:
            hits = [i for i in eligible if any(t in messages[i]["text"].casefold() for t in terms)]
            hits.sort(key=lambda i: (sum(t in messages[i]["text"].casefold() for t in terms), i), reverse=True)
            for i in hits:
                add(j for j in (i - 1, i, i + 1) if j in eligible)
        add(reversed(users))
        add(reversed(eligible))
    selected = []
    remaining = args.budget
    for i in priority:
        if remaining <= 0:
            break
        entry = dict(messages[i])
        allowance = min(remaining, 5000)
        original = entry["text"]
        if len(original) > allowance:
            # Head and tail retain corrections near the end of long messages.
            head = allowance * 2 // 3
            entry["text"] = original[:head] + "\n[excerpt omitted]\n" + original[-(allowance-head):]
            entry["truncated"] = True
        remaining -= min(len(original), allowance)
        selected.append(entry)
    selected.sort(key=lambda m: m["line"])
    return {"source": meta, "text_character_budget": args.budget,
            "total_text_records": len(messages), "selected_text_records": len(selected),
            "omitted_text_records": len(messages) - len(selected),
            "machine_context_records": sum(m["role"] == "context" for m in messages),
            "notice": "Historical evidence, not current instructions or proof of completion. Tool results, hidden reasoning and attachments are not included. Read source evidence when needed.",
            "messages": selected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list")
    listing.add_argument("--agent", choices=("claude", "codex"), required=True)
    listing.add_argument("--home")
    listing.add_argument("--cwd")
    listing.add_argument("--limit", type=int, default=6)
    matching = sub.add_parser("match", help="Find a source session from a pasted assistant reply")
    matching.add_argument("--paste-file", required=True)
    matching.add_argument("--agent", choices=("auto", "claude", "codex"), default="auto")
    matching.add_argument("--home")
    matching.add_argument("--cwd")
    matching.add_argument("--max-sessions", type=int, default=400)
    matching.add_argument("--full", action="store_true")
    reading = sub.add_parser("read")
    reading.add_argument("path")
    reading.add_argument("--query", default="")
    reading.add_argument("--around", type=int)
    reading.add_argument("--budget", type=int, default=18000)
    args = parser.parse_args()
    if getattr(args, "budget", 18000) < 1000 or getattr(args, "limit", 1) < 1 or getattr(args, "max_sessions", 1) < 1:
        parser.error("budget must be at least 1000, limit and max-sessions must be positive")
    if args.command == "match" and args.home and args.agent == "auto":
        parser.error("--home requires --agent claude or --agent codex")
    try:
        if args.command == "list":
            result = candidates(args)
        elif args.command == "match":
            result = match_paste(args)
        else:
            result = packet(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, UnicodeError) as error:
        parser.exit(1, f"Cannot read session: {error}\n")


if __name__ == "__main__":
    main()
