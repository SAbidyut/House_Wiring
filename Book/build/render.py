#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render.py — rasterise SVG diagrams to high-DPI PNG with headless Chrome.

Chrome is used because it ships HarfBuzz: Bangla conjuncts / matra reordering
come out exactly as Word would draw them. cairosvg and ImageMagick do not
shape Indic text correctly.
"""
import os, re, subprocess, sys, glob, shutil

CHROME = os.environ.get("CHROME_BIN", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
SCALE = 3          # 3x → ~300 dpi at print size
PAD = 400          # extra window height, cropped off after the screenshot


def svg_size(path):
    head = open(path, encoding="utf-8").read(2000)
    m = re.search(r'viewBox\s*=\s*"([\d.\s\-]+)"', head)
    if m:
        parts = [float(x) for x in m.group(1).split()]
        return int(round(parts[2])), int(round(parts[3]))
    w = re.search(r'\bwidth\s*=\s*"(\d+)', head)
    h = re.search(r'\bheight\s*=\s*"(\d+)', head)
    return int(w.group(1)), int(h.group(1))


def render(svg, png=None, scale=SCALE):
    svg = os.path.abspath(svg)
    png = png or os.path.splitext(svg)[0] + ".png"
    w, h = svg_size(svg)
    # wrap in HTML so the SVG lays out at exactly its viewBox size
    html = os.path.splitext(svg)[0] + ".__r.html"
    body = open(svg, encoding="utf-8").read()
    open(html, "w", encoding="utf-8").write(
        "<!doctype html><meta charset='utf-8'>"
        "<style>html,body{margin:0;padding:0;background:#fff;}"
        f"svg{{display:block;width:{w}px;height:{h}px;}}</style>" + body)
    cmd = [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
           "--disable-lcd-text", "--font-render-hinting=none",
           f"--force-device-scale-factor={scale}",
           "--default-background-color=FFFFFFFF",
           f"--screenshot={png}", f"--window-size={w},{h + PAD}",
           "file://" + html]
    if os.path.exists(png):
        os.remove(png)
    r = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(html)
    if not os.path.exists(png):
        print("FAIL", svg, r.stderr[-600:], file=sys.stderr)
        return None
    # New-style headless Chrome takes the window's outer size for
    # --window-size, so the viewport is shorter than asked and the foot of
    # the drawing was cut off.  Render into a taller window, then crop back.
    from PIL import Image
    im = Image.open(png)
    im.crop((0, 0, w * scale, h * scale)).save(png)
    return png


if __name__ == "__main__":
    args = sys.argv[1:]
    files = []
    for a in args:
        files.extend(sorted(glob.glob(a)) if any(c in a for c in "*?[") else [a])
    if not files:
        files = sorted(glob.glob("diagrams/**/*.svg", recursive=True))
    ok = 0
    for f in files:
        out = render(f)
        if out:
            ok += 1
            print("✓", os.path.relpath(out))
    print(f"\n{ok}/{len(files)} rendered")
