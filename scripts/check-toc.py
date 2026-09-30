#!/usr/bin/env python3
"""Check that ToC.md lists every tracked file and that every link in it resolves.

Usage (from anywhere): python3 scripts/check-toc.py
Tested with Python 3.10. Exit code 0 means the table of contents is consistent.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Files that are intentionally not listed (tooling and editor files).
IGNORED_PREFIXES = ('.',)
IGNORED_FILES = {'.gitignore'}

with open(os.path.join(ROOT, 'ToC.md'), encoding='utf-8') as fh:
    toc = fh.read()
linked = set(re.findall(r'\]\(([^)#]+?)(?:#[^)]*)?\)', toc))

# Untracked files count too, so a new note is caught before it is committed.
listed = subprocess.run(
    ['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
    cwd=ROOT, capture_output=True, text=True, check=True).stdout.split('\n')
files = {f for f in listed if f and not f.startswith(IGNORED_PREFIXES) and f not in IGNORED_FILES and os.path.exists(os.path.join(ROOT, f))}

missing = sorted(files - linked)
broken = sorted(p for p in linked if not p.startswith('http') and not os.path.exists(os.path.join(ROOT, p)))

for f in missing:
    print('not listed in ToC.md:', f)
for p in broken:
    print('broken link in ToC.md:', p)
sys.exit(1 if missing or broken else 0)
