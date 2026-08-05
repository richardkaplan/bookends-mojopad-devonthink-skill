#!/usr/bin/env python3
"""Post-build encoding check for a generated report (R-BOOKENDS-ENCODING-ASCII-01).
FAILS the run on any UTF-8 mojibake marker, a missing charset meta (HTML), or a literal
unsubstituted format token (e.g. a stray %s). Usage: validate_encoding.py <report.html> [...]"""
import sys, re
MOJI = ["Ã", "â€", "â‰", ",ââ", "âˆ", "Â "]
def check(path):
    txt = open(path, "rb").read().decode("utf-8", "replace")
    fails = []
    hits = [m for m in MOJI if m in txt]
    if hits:
        fails.append("mojibake markers present: %r" % hits)
    if path.lower().endswith((".html", ".htm")):
        low = txt.lower().replace(" ", "")
        if 'charset="utf-8"' not in low and "charset=utf-8" not in low:
            fails.append('missing <meta charset="utf-8">')
    if re.search(r"(?<!%)%s(?![0-9A-Za-z])", txt):
        fails.append("literal unsubstituted format token '%s' present")
    return fails
def main(argv):
    bad = False
    for p in argv:
        f = check(p)
        if f:
            bad = True; print("FAIL %s: %s" % (p, "; ".join(f)))
        else:
            print("OK %s: no mojibake, charset present, no unsubstituted tokens" % p)
    return 1 if bad else 0
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: validate_encoding.py <report.html> [more...]"); sys.exit(2)
    sys.exit(main(sys.argv[1:]))
