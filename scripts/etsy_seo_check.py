#!/usr/bin/env python3
"""Check an Etsy listing title and tags against Etsy's hard limits and a few
readability heuristics. Standard library only, nothing leaves your computer.

  python3 etsy_seo_check.py --title "..." --tags "tag one, tag two" [--keyword "main phrase"] [--json]
  python3 etsy_seo_check.py --file listing.json

listing.json: {"title": "...", "tags": ["...", "..."], "keyword": "optional"}

Made by PawsOnMePet, an Etsy shop of ceramic slow feeder bowls for cats and dogs:
https://www.etsy.com/shop/PawsOnMePet  (MIT License)
"""
import argparse
import json
import re
import sys
from collections import Counter

# Etsy hard limits (Etsy Help Center; links in README)
TITLE_MAX = 140
TAGS_MAX = 13
TAG_MAX = 20
TAG_CHARS = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 '\-]*$")

# Our heuristics, not Etsy policy
KEYWORD_WITHIN = 40
SMALL_WORDS = {"a", "an", "and", "the", "for", "with", "of", "in", "on", "to", "or", "by", "your", "my", "is"}


def check(title, tags, keyword=None):
    issues = []

    def add(level, code, msg):
        issues.append({"level": level, "code": code, "message": msg})

    title = (title or "").strip()
    tags = [t.strip() for t in tags if t and t.strip()]

    if not title:
        add("error", "title-empty", "The title is empty.")
    elif len(title) > TITLE_MAX:
        add("error", "title-too-long", f"Title is {len(title)} characters. Etsy allows {TITLE_MAX}.")
    if len(tags) > TAGS_MAX:
        add("error", "too-many-tags", f"{len(tags)} tags. Etsy allows {TAGS_MAX}.")
    for t in tags:
        if len(t) > TAG_MAX:
            add("error", "tag-too-long", f'"{t}" is {len(t)} characters. Etsy allows {TAG_MAX} per tag.')
        if not TAG_CHARS.match(t):
            add("error", "tag-characters", f'"{t}" has characters Etsy does not accept in tags. '
                "Use letters, numbers and spaces; ' and - only inside a word.")

    if len(tags) < TAGS_MAX:
        add("warn", "unused-tag-slots", f"{TAGS_MAX - len(tags)} tag slot(s) left empty. "
            "Each tag is one more phrase a buyer can find you with.")
    for t, c in Counter(t.lower() for t in tags).items():
        if c > 1:
            add("warn", "duplicate-tag", f'"{t}" is used {c} times.')
    for t in tags:
        if len(t.split()) == 1:
            add("warn", "single-word-tag", f'"{t}" is one word. A short phrase like "slow feeder bowl" '
                "is closer to what buyers type.")
    words = [w for w in re.findall(r"[a-z0-9']+", title.lower()) if w not in SMALL_WORDS]
    repeats = sorted(w for w, c in Counter(words).items() if c >= 3)
    if repeats:
        add("warn", "title-repeats", "Used 3+ times in the title: " + ", ".join(repeats)
            + ". Swap a repeat for a new phrase.")
    caps = re.findall(r"\b[A-Z]{4,}\b", title)
    if caps:
        add("info", "title-all-caps", "All-caps words: " + ", ".join(caps) + ". They read as shouting.")
    if keyword:
        pos = title.lower().find(keyword.lower().strip())
        if pos < 0:
            add("warn", "keyword-missing", f'Main keyword "{keyword}" is not in the title.')
        elif pos > KEYWORD_WITHIN:
            add("info", "keyword-late", f"Main keyword starts at character {pos + 1}. "
                "Put it near the front so it is the first thing buyers read.")

    summary = {
        "title_chars": len(title),
        "tag_count": len(tags),
        "tag_chars": [[t, len(t)] for t in tags],
        "errors": sum(i["level"] == "error" for i in issues),
        "warnings": sum(i["level"] == "warn" for i in issues),
    }
    return {"summary": summary, "issues": issues}


def main(argv=None):
    p = argparse.ArgumentParser(description="Check an Etsy listing title and tags.")
    p.add_argument("--title")
    p.add_argument("--tags", help="comma-separated tags")
    p.add_argument("--keyword", help="the main phrase buyers search for")
    p.add_argument("--file", help="JSON file with title, tags and keyword")
    p.add_argument("--json", action="store_true", help="print JSON instead of text")
    a = p.parse_args(argv)
    if a.file:
        with open(a.file, encoding="utf-8") as f:
            d = json.load(f)
        title, tags, kw = d.get("title", ""), d.get("tags", []), a.keyword or d.get("keyword")
    else:
        if a.title is None or a.tags is None:
            p.error("give --title and --tags, or --file")
        title, tags, kw = a.title, a.tags.split(","), a.keyword
    r = check(title, tags, kw)
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    else:
        s = r["summary"]
        print(f"Title: {s['title_chars']}/{TITLE_MAX} characters | Tags: {s['tag_count']}/{TAGS_MAX}")
        for i in r["issues"]:
            mark = {"error": "x", "warn": "!", "info": "-"}[i["level"]]
            print(f"  {mark} [{i['code']}] {i['message']}")
        if not r["issues"]:
            print("  No issues found.")
        print(f"{s['errors']} error(s), {s['warnings']} warning(s)")
        print("etsy-listing-seo-check by PawsOnMePet | https://www.etsy.com/shop/PawsOnMePet")
    return 1 if r["summary"]["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
