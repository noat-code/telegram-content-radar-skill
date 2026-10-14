#!/usr/bin/env python3
"""Read public Telegram channel posts into a local JSONL file.

Uses the account owner's Telegram API credentials and a local session.
It never posts, joins, edits, or reacts in Telegram.
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from telethon import TelegramClient


WORKSPACE = Path(os.environ.get("CONTENT_RADAR_HOME", Path(__file__).resolve().parents[1]))


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        raise FileNotFoundError(f"Missing credentials file: {path}")
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_handles(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"Missing channels file: {path}")
    with path.open(encoding="utf-8", newline="") as f:
        rows = csv.DictReader(f)
        return [row["handle"].strip().lstrip("@") for row in rows if row.get("status", "active") == "active"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect public Telegram posts for Content Radar.")
    parser.add_argument("--days", type=int, default=14, help="Look back this many calendar days.")
    parser.add_argument("--limit", type=int, default=30, help="Maximum messages to inspect per channel.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output JSONL path. Defaults to findings/telegram-raw-YYYY-MM-DD.jsonl.",
    )
    return parser.parse_args()


async def collect(args: argparse.Namespace) -> int:
    env = load_env(WORKSPACE / ".env")
    api_id_raw = env.get("TG_API_ID", "")
    api_hash = env.get("TG_API_HASH", "")
    if not api_id_raw.isdigit() or not api_hash:
        raise ValueError("TG_API_ID and TG_API_HASH must be set in .env")

    handles = load_handles(WORKSPACE / "sources" / "telegram-channels.csv")
    if not handles:
        raise ValueError("No active channel handles found.")

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=args.days)
    output = args.output or (WORKSPACE / "findings" / f"telegram-raw-{now.date().isoformat()}.jsonl")
    output.parent.mkdir(parents=True, exist_ok=True)
    session_path = WORKSPACE / "collector" / "telegram"

    client = TelegramClient(str(session_path), int(api_id_raw), api_hash)
    await client.start(phone=env.get("TG_PHONE") or None)
    total_posts = 0
    failures: list[str] = []

    try:
        with output.open("w", encoding="utf-8") as f:
            for handle in handles:
                posts: list[dict[str, object]] = []
                try:
                    entity = await client.get_entity(handle)
                    async for message in client.iter_messages(entity, limit=args.limit):
                        if message.date and message.date < cutoff:
                            break
                        text = (message.message or "").strip()
                        if not text:
                            continue
                        posts.append(
                            {
                                "id": message.id,
                                "date": message.date.isoformat() if message.date else None,
                                "text": text,
                                "views": message.views,
                                "forwards": message.forwards,
                                "link": f"https://t.me/{handle}/{message.id}",
                                "has_media": bool(message.media),
                            }
                        )
                    total_posts += len(posts)
                    f.write(json.dumps({"handle": f"@{handle}", "posts": posts}, ensure_ascii=False) + "\n")
                    print(f"@{handle}: {len(posts)} posts")
                except Exception as exc:  # report and continue with other channels
                    failures.append(f"@{handle}: {type(exc).__name__}: {exc}")
                    print(f"@{handle}: ERROR ({type(exc).__name__})", file=sys.stderr)
    finally:
        await client.disconnect()

    print(f"Saved {total_posts} posts from {len(handles)} channels to {output}")
    if failures:
        print("Failures:", *failures, sep="\n- ", file=sys.stderr)
    return 0 if not failures else 2


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(collect(parse_args())))
    except KeyboardInterrupt:
        print("Cancelled.", file=sys.stderr)
        raise SystemExit(130)
