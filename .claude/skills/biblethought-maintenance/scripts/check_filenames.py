#!/usr/bin/env python3
"""Reads a NUL-separated list of file paths from stdin (i.e. the caller
must invoke `git diff ... --name-only -z`) and reports any whose filename
contains a character known to break Jekyll/HTML rendering.

Used by .git/hooks/pre-commit. Two bugs this script exists to avoid:

1. Kept as a real script file (not an inline `python3 - <<EOF` heredoc)
   because piping into `python3 -` consumes stdin for the program source
   itself, leaving nothing for a script to read via sys.stdin afterward —
   that bug previously made this check a silent no-op.
2. Reads NUL-separated (`-z`) input, not newline-separated. Git's default
   `--name-only` output quotes any path containing non-ASCII bytes in a
   literal `"..."` wrapper (with octal escapes) for human-readable display.
   That wrapper is itself made of literal `"` characters, so naively
   scanning the default output for a bad `"` character flags *every*
   Chinese filename, not just ones that actually contain a quote. `-z`
   output is the raw, unquoted bytes — no such ambiguity.
"""
import sys

# Characters that break HTML/URL when used in filenames:
#   ——   double em dash       → Jekyll URL-encodes into garbage
#   " "  curly double quotes  → break href="..." attribute syntax
#   ' '  curly single quotes  → break href='...' attribute syntax
#   "    ASCII double quote   → break href="..." immediately
#   < >  HTML angle brackets  → break HTML structure / XSS risk
#   &    HTML ampersand       → breaks entity encoding in URLs
#   #    URL fragment marker  → truncates URL path silently
#   ?    ASCII question mark  → starts URL query string (use fullwidth ？ instead)
#   :    ASCII colon          → Jekyll/Addressable parses text before it as a URI
#                                scheme and throws "Invalid scheme format", failing
#                                the entire site build (use fullwidth ： instead)
BAD = ['——', '“', '”', '‘', '’', '"', '<', '>', '&', '#', '?', ':']

found_any = False
raw = sys.stdin.buffer.read().decode('utf-8')
for path in raw.split('\0'):
    path = path.strip()
    if not path:
        continue
    filename = path.split('/')[-1]
    hits = [ch for ch in BAD if ch in filename]
    if hits:
        found_any = True
        chars = ' '.join(f'"{ch}"' for ch in hits)
        print(f"  {path}  ← 含有：{chars}")

sys.exit(1 if found_any else 0)
