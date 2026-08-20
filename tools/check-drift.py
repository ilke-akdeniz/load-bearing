#!/usr/bin/env python3
"""Mechanical consistency checks for the book.

Catches global drift — the kind no per-chapter review can see, because no
single chapter is wrong. Local drift (an entry contradicting its own chapter)
needs judgment and stays with the author and Claude at the draft transition.

Run from the repo root:  python3 tools/check-drift.py
Exit status is 1 if anything failed, so it can gate a commit.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
problems = []
checked = 0


def fail(check, message):
    problems.append((check, message))


def read(name):
    return (ROOT / name).read_text()


def strip_fences(text):
    """Drop fenced code so prose checks do not trip over sample code."""
    out, in_fence = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


toc = read("00_toc.md")
toc_lines = toc.split("\n")
chapter_files = sorted(p.name for p in ROOT.glob("[0-9][0-9]_*.md") if p.name != "00_toc.md")

parts = [(n, l.split("—", 1)[1].strip())
         for n, l in enumerate(toc_lines, 1) if l.startswith("## Part ")]
entries = [(n, m.group(1), m.group(2).strip())
           for n, l in enumerate(toc_lines, 1)
           if (m := re.match(r"^### (\d\d)\.\s*(.+)$", l))]
status = dict(re.findall(r"^\| (\d\d) \| `([^`]+)` \|", toc, re.M))
status_state = dict(re.findall(r"^\| (\d\d) \| `[^`]+` \| (.+?) \|", toc, re.M))


# 1. A part title must not collide with a chapter title.
checked += 1
for pn, part in parts:
    for cn, num, title in entries:
        a, b = part.lower().rstrip("."), title.lower().rstrip(".")
        if a == b or a in b or b in a:
            fail("part/chapter collision",
                 f"00_toc.md:{pn} Part '{part}' overlaps 00_toc.md:{cn} ch {num} '{title}'")

# 2. Every chapter file has a TOC entry, and every entry has a file.
checked += 1
entry_files = {num: status.get(num) for _, num, _ in entries}
for num, fname in entry_files.items():
    if fname is None:
        fail("toc/status", f"ch {num} has a TOC entry but no row in the status table")
for fname in chapter_files:
    num = fname[:2]
    if num not in entry_files:
        fail("toc/status", f"{fname} exists but has no TOC entry")
    elif entry_files[num] != fname:
        fail("toc/status", f"ch {num}: status table says `{entry_files[num]}`, file is `{fname}`")

# 3. A chapter's H1 must match its TOC title (case-insensitively).
checked += 1
for _, num, title in entries:
    fname = status.get(num)
    if not fname or not (ROOT / fname).exists():
        continue
    h1 = read(fname).split("\n", 1)[0].lstrip("# ").strip()
    if h1.lower().replace(":", "") != title.lower().replace(":", ""):
        fail("h1 vs toc", f"ch {num}: H1 '{h1}' != TOC '{title}'")

# 4. Status must be one of the four defined states, and match whether a file exists.
checked += 1
for num, state in status_state.items():
    clean = state.replace("*", "").strip()
    if clean not in {"not started", "in progress", "draft", "ready"}:
        fail("status", f"ch {num}: unknown status '{clean}'")
    exists = status.get(num) in chapter_files
    if clean == "not started" and exists:
        fail("status", f"ch {num}: marked 'not started' but the file exists")
    if clean != "not started" and not exists:
        fail("status", f"ch {num}: marked '{clean}' but no file exists")

# 5. Every cross-reference resolves to a chapter that exists.
checked += 1
known = {f[:2] for f in chapter_files} | set(entry_files)
for fname in chapter_files + ["00_toc.md", "README.md", "CLAUDE.md"]:
    prose = strip_fences(read(fname))
    for n, line in enumerate(prose.split("\n"), 1):
        for ref in re.findall(r"\bCh(?:apter|\.)\s+(\d\d?)\b", line):
            num = ref.zfill(2)
            if num not in known:
                fail("dangling ref", f"{fname}:{n} refers to chapter {ref}, which is not in the TOC")

# 6. Terminology that a past sweep retired. DECISIONS.md is the historical
#    record and is deliberately exempt.
checked += 1
retired = ["five levels", "the five levels"]
for path in sorted(ROOT.glob("*.md")) + sorted(ROOT.glob("docs/*.md")) + [ROOT / "CLAUDE.md"]:
    if path.name == "DECISIONS.md":
        continue
    prose = strip_fences(path.read_text()).lower()
    for term in retired:
        if term in prose:
            fail("retired term", f"{path.relative_to(ROOT)} still contains '{term}'")

# 7. Counts asserted in more than one file must agree.
checked += 1
n_chapters = len(entries)
for fname in ["00_toc.md", "README.md"]:
    text = read(fname)
    for stated in re.findall(r"(\w+[- ]\w+|\w+) chapters", text):
        words = {"twenty-four": 24, "twenty four": 24, "24": 24}
        if stated.lower() in words and words[stated.lower()] != n_chapters:
            fail("count", f"{fname} says {stated} chapters, TOC has {n_chapters}")
if "four levels and five kinds" not in read("CLAUDE.md"):
    fail("count", "CLAUDE.md no longer states 'four levels and five kinds'")

# 8. Every chapter past 'not started' owns at least one ledger row.
checked += 1
ledger = read("docs/LEDGER.md")
owned = set(re.findall(r"\|\s*(\d\d)\s*\|", ledger))
for num, state in status_state.items():
    if state.replace("*", "").strip() != "not started" and num not in owned:
        fail("ledger", f"ch {num} is drafted but owns no row in docs/LEDGER.md")

# 9. Markdown conventions the book commits to.
checked += 1
for path in sorted(ROOT.glob("*.md")) + sorted(ROOT.glob("docs/*.md")) + [ROOT / "CLAUDE.md"]:
    rel, text = path.relative_to(ROOT), path.read_text()
    lines = text.split("\n")
    fences = [i for i, l in enumerate(lines) if l.startswith("```")]
    if len(fences) % 2:
        fail("markdown", f"{rel}: unbalanced code fences")
    for i in fences[0::2]:
        if lines[i].strip() == "```":
            fail("markdown", f"{rel}:{i+1}: code fence with no language tag")
    # Prose rule only: a formatter puts two blank lines between Python
    # top-level definitions, and fenced code goes in exactly as produced.
    in_fence = False
    for i in range(1, len(lines)):
        if lines[i].startswith("```"):
            in_fence = not in_fence
        if in_fence:
            continue
        if lines[i] == "" and lines[i - 1] == "":
            fail("markdown", f"{rel}:{i+1}: two blank lines in a row")
    for i, l in enumerate(lines, 1):
        if l != l.rstrip():
            fail("markdown", f"{rel}:{i}: trailing whitespace")
    if not text.endswith("\n") or text.endswith("\n\n"):
        fail("markdown", f"{rel}: file must end with exactly one newline")
    if path.name[:2].isdigit() and path.name != "00_toc.md":
        # Count H1s in prose only — a `#` inside a fence is a comment.
        prose_lines = strip_fences(text).split("\n")
        if sum(1 for l in prose_lines if l.startswith("# ")) != 1:
            fail("markdown", f"{rel}: a chapter must have exactly one H1")

# 10. ASCII diagrams stay under 72 columns. Only `text` fences are diagrams,
#     and terminal output is exempt — flagged as a note rather than a failure.
checked += 1
for fname in chapter_files:
    lang, wide = None, []
    for n, l in enumerate(read(fname).split("\n"), 1):
        if (m := re.match(r"^```(\w+)?$", l)):
            lang = m.group(1) if lang is None else None
            continue
        if lang == "text" and len(l) > 72:
            wide.append((n, len(l)))
    for n, w in wide:
        print(f"  note  {fname}:{n} text fence is {w} columns "
              f"(fine for terminal output, not for a diagram)")

by_check = {}
for check, message in problems:
    by_check.setdefault(check, []).append(message)

print(f"\n{checked} checks run over {len(chapter_files)} chapters.")
if not problems:
    print("No drift found.")
    sys.exit(0)
for check, messages in by_check.items():
    print(f"\n{check} ({len(messages)}):")
    for m in messages:
        print(f"  {m}")
print(f"\n{len(problems)} problems.")
sys.exit(1)
