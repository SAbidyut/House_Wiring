#!/usr/bin/env python3
"""Render every book diagram SVG to a slide-sized PNG (2x) in parallel."""
import os, sys, glob
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "Book", "build"))
import render
SRC = os.path.join(os.path.dirname(__file__), "..", "..", "Book", "build", "diagrams")
DST = os.path.join(os.path.dirname(__file__), ".cache", "diagrams")

def job(svg):
    rel = os.path.relpath(svg, SRC)
    png = os.path.join(DST, os.path.splitext(rel)[0] + ".png")
    if os.path.exists(png) and os.path.getmtime(png) > os.path.getmtime(svg):
        return png
    os.makedirs(os.path.dirname(png), exist_ok=True)
    tmp = os.path.join(os.path.dirname(png), "_" + os.path.basename(svg))
    open(tmp, "w", encoding="utf-8").write(open(svg, encoding="utf-8").read())
    out = render.render(tmp, png, scale=2)
    os.remove(tmp)
    return out

if __name__ == "__main__":
    pats = sys.argv[1:] or ["ch*/*.svg"]
    files = [f for p in pats for f in sorted(glob.glob(os.path.join(SRC, p)))]
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(job, files))
    print(sum(1 for r in res if r), "/", len(files), "rendered")
