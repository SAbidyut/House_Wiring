#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render.py — rasterise SVG diagrams to high-DPI PNG with headless Chrome.

Chrome is used because it ships HarfBuzz: Bangla conjuncts / matra reordering
come out exactly as Word would draw them. cairosvg and ImageMagick do not
shape Indic text correctly.

Fallback: if Chrome not found, create a blank white PNG placeholder (so the
DOCX build can still embed the SVG vector).
"""
import os, re, subprocess, sys, glob, shutil

_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/snap/bin/chromium",
]
CHROME = None
for _c in _CANDIDATES:
    if os.path.exists(_c):
        CHROME = _c
        break

SCALE = 3

def svg_size(path):
    head = open(path, encoding="utf-8").read(2000)
    m = re.search(r'viewBox\s*=\s*"([\d.\s\-]+)"', head)
    if m:
        parts = [float(x) for x in m.group(1).split()]
        return int(round(parts[2])), int(round(parts[3]))
    w = re.search(r'\bwidth\s*=\s*"(\d+)', head)
    h = re.search(r'\bheight\s*=\s*"(\d+)', head)
    return int(w.group(1)), int(h.group(1)) if w and h else (1240, 700)

def _fallback_png(svg, png):
    try:
        from PIL import Image
        w, h = svg_size(svg)
        # Create white placeholder with same aspect, scaled
        img = Image.new("RGB", (w * SCALE, h * SCALE), "white")
        # Optionally draw text indicating placeholder
        try:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            font_path = os.path.join(os.path.dirname(__file__), "..", "Kalpurush.ttf")
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 24 * SCALE)
            else:
                font = ImageFont.load_default()
            draw.text((20, 20), f"SVG: {os.path.basename(svg)}", fill="black", font=font)
        except Exception:
            pass
        img.save(png)
        return png
    except Exception as e:
        print(f"FAIL fallback {svg}: {e}", file=sys.stderr)
        return None

def render(svg, png=None, scale=SCALE):
    svg = os.path.abspath(svg)
    png = png or os.path.splitext(svg)[0] + ".png"
    if CHROME is None:
        return _fallback_png(svg, png)
    w, h = svg_size(svg)
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
           f"--screenshot={png}", f"--window-size={w},{h}",
           "file://" + html]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except Exception as e:
        if os.path.exists(html):
            os.remove(html)
        print(f"Chrome failed, fallback: {e}", file=sys.stderr)
        return _fallback_png(svg, png)
    if os.path.exists(html):
        os.remove(html)
    if not os.path.exists(png):
        print("FAIL", svg, r.stderr[-600:], file=sys.stderr)
        # try fallback
        return _fallback_png(svg, png)
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
