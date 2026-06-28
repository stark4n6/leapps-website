#!/usr/bin/env python3
"""Generate (or validate) blog/posts/index.json from each post's Markdown frontmatter.

The index is a derived artifact: it is rebuilt from the posts on every push to
main (see .github/workflows/generate-blog-index.yml), so contributors never edit
it by hand. The same script runs in --check mode on pull requests to validate a
post's frontmatter and filename before merge.

Usage:
    python3 scripts/generate_blog_index.py            # write blog/posts/index.json
    python3 scripts/generate_blog_index.py --check    # validate only, write nothing
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "blog" / "posts"
INDEX_PATH = POSTS_DIR / "index.json"

FRONTMATTER_RE = re.compile(r"^---\s*\n(?P<body>.*?)\n---\s*", re.DOTALL)
SLUG_RE = re.compile(r"^[\w-]+$")            # exactly what worker.js accepts
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED_FIELDS = ("title", "date", "author", "tags", "excerpt")


def parse_scalar(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return value


def parse_value(value: str):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [parse_scalar(part) for part in inner.split(",")] if inner else []
    return parse_scalar(value)


def parse_frontmatter(markdown: str):
    match = FRONTMATTER_RE.match(markdown)
    if not match:
        return None
    metadata = {}
    for line in match.group("body").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        metadata[key.strip()] = parse_value(value)
    return metadata


def is_real_date(value) -> bool:
    if not isinstance(value, str) or not DATE_RE.match(value):
        return False
    try:
        from datetime import date
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def validate(path: Path, meta, errors: list, warnings: list) -> None:
    """Collect errors/warnings for one post. `path` names it in messages."""
    slug = path.stem
    if not SLUG_RE.match(slug):
        errors.append(f"{path.name}: filename/slug is not URL-safe — use only letters, digits, hyphen, underscore.")
    if re.search(r"[A-Z]", slug):
        warnings.append(f"{path.name}: slug has uppercase letters; lowercase is recommended for URLs.")

    if meta is None:
        errors.append(f"{path.name}: missing YAML frontmatter (--- block at the top).")
        return

    for field in REQUIRED_FIELDS:
        val = meta.get(field)
        if val is None or (isinstance(val, str) and not val.strip()):
            errors.append(f"{path.name}: missing required frontmatter field \"{field}\".")

    if "date" in meta and not is_real_date(meta["date"]):
        errors.append(f"{path.name}: date \"{meta.get('date')}\" must be a valid YYYY-MM-DD calendar date.")

    tags = meta.get("tags")
    if tags is not None:
        if not isinstance(tags, list):
            errors.append(f"{path.name}: tags must use inline array syntax, e.g. [iLEAPP, research].")
        elif any(not isinstance(t, str) or not t.strip() for t in tags):
            errors.append(f"{path.name}: every tag must be a non-empty string.")
        elif not tags:
            warnings.append(f"{path.name}: empty tags (the OG card accent falls back to gold).")

    if "pinned" in meta and not isinstance(meta["pinned"], bool):
        errors.append(f"{path.name}: \"pinned\" must be true or false.")

    m = re.match(r"^(\d{4}-\d{2}-\d{2})-", slug)
    if m and meta.get("date") and m.group(1) != meta["date"]:
        warnings.append(f"{path.name}: slug date prefix ({m.group(1)}) disagrees with the date field ({meta['date']}).")


def entry(path: Path, meta) -> dict:
    e = {
        "slug": path.stem,
        "title": meta["title"],
        "date": meta["date"],
        "author": meta["author"],
        "tags": meta["tags"],
        "excerpt": meta["excerpt"],
    }
    if meta.get("pinned"):
        e["pinned"] = True
    return e


def main() -> int:
    check_only = "--check" in sys.argv[1:]

    paths = sorted(POSTS_DIR.glob("*.md"))
    errors: list = []
    warnings: list = []
    parsed = []
    for path in paths:
        meta = parse_frontmatter(path.read_text(encoding="utf-8-sig"))
        validate(path, meta, errors, warnings)
        parsed.append((path, meta))

    for w in warnings:
        print(f"  warning: {w}")
    if errors:
        for e in errors:
            print(f"  error:   {e}", file=sys.stderr)
        print(f"\nBlog frontmatter invalid — {len(errors)} error(s), {len(warnings)} warning(s).", file=sys.stderr)
        return 1

    posts = [entry(p, m) for p, m in parsed]
    posts.sort(key=lambda post: (bool(post.get("pinned")), post.get("date", ""), post.get("slug", "")), reverse=True)

    if check_only:
        print(f"Blog frontmatter valid — {len(posts)} post(s), {len(warnings)} warning(s).")
        return 0

    INDEX_PATH.write_text(json.dumps(posts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {INDEX_PATH.relative_to(ROOT)} — {len(posts)} post(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
