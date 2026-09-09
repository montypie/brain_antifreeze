#!/usr/bin/env python3
"""
Split one shared markdown diary into chronological files per tag.

Input format, repeated blocks:

    [YYYY-MM-DD] #tag1 #tag2 ...
    ## optional heading
    body text (markdown, may span multiple lines)

Rules:
- The [date] #tags line marks the start of a new entry; everything until the
  next such line (or EOF) is that entry's body.
- Tags are auto-detected (no fixed list) and become output filenames:
  <tag>.md
- An entry tagged with multiple tags is copied into each tag's file.
- Output files: no dates, no tags line; the ## heading (if present) and body
  are kept exactly as written; entries separated by a single blank line.
- Chronological order by date. For entries with multiple tags sharing the same date, an entry
  that starts with a ## heading comes before one(s) that don't; ties beyond
  that keep the original order in the source file.
"""  # noqa: EXE001

import argparse
import re
from datetime import date
from pathlib import Path

ENTRY_HEADER_RE = re.compile(
    r"^\[(\d{4}-\d{2}-\d{2})\]\s*((?:#\S+\s*)+)$",
    re.MULTILINE,
)
TAG_RE = re.compile(r"#(\S+)")


def parse_entries(text):
    """Return list of dicts: date, tags, body, has_heading, order."""

    headers = list(ENTRY_HEADER_RE.finditer(text))
    entries = []
    for i, m in enumerate(headers):
        date_str, tag_part = m.groups()
        entry_date = date.fromisoformat(date_str)
        tags = TAG_RE.findall(tag_part)

        body_start = m.end()
        body_end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = text[body_start:body_end].strip("\n")
        body = body.strip()  # trim leading/trailing blank lines, keep internal ones

        entries.append(
            {
                "date": entry_date,
                "tags": tags,
                "body": body,
                "has_heading": body.startswith("##"),
                "order": i,
            }
        )
    return entries


def sort_key(entry):
    return (entry["date"], 0 if entry["has_heading"] else 1, entry["order"])


def main():
    parser = argparse.ArgumentParser(description="Split a markdown file per tag.")
    parser.add_argument("file", help="Input markdown file")
    args = parser.parse_args()

    source_path = Path(args.file)

    if not source_path.exists():
        raise SystemExit(f"Source file not found: {source_path}")

    text = source_path.read_text(encoding="utf-8")
    entries = parse_entries(text)

    if not entries:
        raise SystemExit("No entries found.")

    tags = sorted({tag for e in entries for tag in e["tags"]})

    for tag in tags:
        tag_entries = sorted(
            (e for e in entries if tag in e["tags"]),
            key=sort_key,
        )
        content = "\n\n".join(e["body"] for e in tag_entries) + "\n"
        out_path = source_path.parent / f"{tag}.md"
        out_path.write_text(content, encoding="utf-8")
        print(f"Wrote {len(tag_entries)} entries to {out_path.name}")


if __name__ == "__main__":
    main()
