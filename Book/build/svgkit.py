# -*- coding: utf-8 -*-
"""
svgkit.py — measured-layout SVG builder.

Bangla is a complex script: character count tells you nothing about rendered
width. So every string is measured for real by headless Chrome (HarfBuzz +
Kalpurush, i.e. exactly the shaper that draws the final PNG), cached on disk,
and boxes are then sized from the measurement. That is what keeps labels from
overflowing their boxes or colliding with neighbours.

Fallback: if Chrome is not available, Pillow + Kalpurush.ttf is used.
"""
import json, os, re, subprocess, hashlib, html, base64

HERE = os.path.dirname(os.path.abspath(__file__))
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

CACHE_PATH = os.path.join(HERE, ".textcache.json")
FAMILY = "Kalpurush"
_FONT_PATH = os.path.join(os.path.dirname(HERE), "Kalpurush.ttf")
if not os.path.exists(_FONT_PATH):
    _FONT_PATH = os.path.join(HERE, "..", "Kalpurush.ttf")
if not os.path.exists(_FONT_PATH):
    _FONT_PATH = os.path.join(HERE, "Kalpurush.ttf")

try:
    _CACHE = json.load(open(CACHE_PATH, encoding="utf-8"))
except Exception:
    _CACHE = {}

_PENDING = set()

def _key(text, size, weight, family):
    return f"{family}|{weight}|{size}|{text}"

def request(text, size=16, weight=400, family=FAMILY):
    if _key(text, size, weight, family) not in _CACHE:
        _PENDING.add((text, size, weight, family))

def _pillow_measure(text, size, weight, family):
    try:
        from PIL import ImageFont
        fp = _FONT_PATH if os.path.exists(_FONT_PATH) else None
        if fp and os.path.exists(fp):
            font = ImageFont.truetype(fp, size)
        else:
            font = ImageFont.load_default()
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if weight >= 700:
            w *= 1.08
        return [float(w), float(h + size * 0.35)]
    except Exception:
        return [len(text) * size * 0.55, size * 1.4]

def flush():
    global _PENDING
    if not _PENDING:
        return
    items = sorted(_PENDING)
    if CHROME is None:
        for (t, s, w, f) in items:
            _CACHE[_key(t, s, w, f)] = _pillow_measure(t, s, w, f)
        try:
            json.dump(_CACHE, open(CACHE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        except Exception:
            pass
        _PENDING = set()
        return
    spans = []
    for i, (t, s, w, f) in enumerate(items):
        spans.append(
            f'<span id="m{i}" style="font-family:\'{f}\';font-size:{s}px;'
            f'font-weight:{w};white-space:pre">{html.escape(t)}</span>')
    doc = ("<!doctype html><meta charset='utf-8'>"
           "<style>body{margin:0}span{display:inline-block}</style>"
           "<div id='wrap'>" + "".join(spans) + "</div>"
           "<script>var o=[];for(var i=0;i<" + str(len(items)) + ";i++){"
           "var e=document.getElementById('m'+i);var r=e.getBoundingClientRect();"
           "o.push([r.width,r.height]);}"
           "document.getElementById('wrap').outerHTML="
           "'<pre id=out>'+JSON.stringify(o)+'</pre>';</script>")
    tmp = os.path.join(HERE, ".__measure.html")
    open(tmp, "w", encoding="utf-8").write(doc)
    try:
        out = subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--dump-dom",
             "--virtual-time-budget=4000", "file://" + tmp],
            capture_output=True, text=True, timeout=15).stdout
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        for (t, s, w, f) in items:
            _CACHE[_key(t, s, w, f)] = _pillow_measure(t, s, w, f)
        try:
            json.dump(_CACHE, open(CACHE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        except Exception:
            pass
        _PENDING = set()
        return
    if os.path.exists(tmp):
        os.remove(tmp)
    m = re.search(r'<pre id="out">(.*?)</pre>', out, re.S)
    if not m:
        for (t, s, w, f) in items:
            _CACHE[_key(t, s, w, f)] = _pillow_measure(t, s, w, f)
        try:
            json.dump(_CACHE, open(CACHE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        except Exception:
            pass
        _PENDING = set()
        return
    vals = json.loads(m.group(1))
    for (t, s, w, f), (wd, ht) in zip(items, vals):
        _CACHE[_key(t, s, w, f)] = [round(wd, 2), round(ht, 2)]
    try:
        json.dump(_CACHE, open(CACHE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    except Exception:
        pass
    _PENDING = set()

COLLECT = False

def _estimate(text, size):
    return len(text) * size * 0.52

def measure(text, size=16, weight=400, family=FAMILY):
    k = _key(text, size, weight, family)
    if k not in _CACHE:
        request(text, size, weight, family)
        if COLLECT:
            return [_estimate(text, size), size * 1.55]
        flush()
    return _CACHE[k]

def tw(text, size=16, weight=400, family=FAMILY):
    k = _key(text, size, weight, family)
    if k in _CACHE:
        return _CACHE[k][0]
    if " " not in text:
        return measure(text, size, weight, family)[0]
    words = text.split(" ")
    for w_ in words:
        request(w_, size, weight, family)
    request(" ", size, weight, family)
    if COLLECT:
        return _estimate(text, size)
    flush()
    sp_key = _key(" ", size, weight, family)
    sp = _CACHE.get(sp_key, [size * 0.33, size])[0]
    total = 0.0
    for w_ in words:
        wk = _key(w_, size, weight, family)
        if wk in _CACHE:
            total += _CACHE[wk][0]
        else:
            total += _pillow_measure(w_, size, weight, family)[0]
    total += sp * (len(words) - 1)
    return total

def wrap(text, max_w, size=16, weight=400, family=FAMILY):
    words = text.split(" ")
    if not COLLECT:
        for w_ in words:
            request(w_, size, weight, family)
        request(" ", size, weight, family)
        flush()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if cur and tw(trial, size, weight, family) > max_w:
            lines.append(cur)
            cur = w_
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines

def two_pass(fn):
    global COLLECT
    COLLECT = True
    try:
        fn()
    except Exception:
        pass
    COLLECT = False
    flush()
    return fn()

def prewarm(strings):
    for s in strings:
        request(*s)
    flush()

NAVY = "#0F3357"
STEEL = "#1D5B8F"
LIGHT = "#EAF2FA"
RED = "#B32A22"
REDBG = "#FDECEA"
GREEN = "#1B6E47"
GREENBG = "#EAF6EF"
AMBER = "#B47500"
AMBERBG = "#FFF6E5"
GREY = "#5A6470"
LINE = "#C3CEDA"
INK = "#1A1A1A"
PAPER = "#FFFFFF"

_PATH_TOKENS = re.compile(r"([MmLlHhVvCcSsQqTtAaZz])|(-?\d*\.?\d+(?:[eE][-+]?\d+)?)")

def _path_points(d):
    toks = [(c, n) for c, n in _PATH_TOKENS.findall(d)]
    pts, i = [], 0
    cx = cy = sx = sy = 0.0
    cmd = None
    seq = []
    for c, n in toks:
        if c:
            seq.append(("cmd", c))
        else:
            seq.append(("num", float(n)))
    i = 0
    while i < len(seq):
        kind, val = seq[i]
        if kind == "cmd":
            cmd = val
            i += 1
            if cmd in "Zz":
                cx, cy = sx, sy
                pts.append((cx, cy))
            continue
        if cmd is None:
            i += 1
            continue
        need = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7}[cmd.upper()]
        args = []
        while len(args) < need and i < len(seq) and seq[i][0] == "num":
            args.append(seq[i][1]); i += 1
        if len(args) < need:
            break
        rel = cmd.islower()
        u = cmd.upper()
        if u == "H":
            cx = cx + args[0] if rel else args[0]
        elif u == "V":
            cy = cy + args[0] if rel else args[0]
        else:
            ex, ey = args[-2], args[-1]
            if u == "A":
                ex, ey = args[5], args[6]
            cx = cx + ex if rel else ex
            cy = cy + ey if rel else ey
        if u == "M":
            sx, sy = cx, cy
        pts.append((cx, cy))
        if u == "M":
            cmd = "l" if rel else "L"
    return pts

class SVG:
    def __init__(self, w, h, bg=PAPER):
        self.w, self.h = w, h
        self.parts = []
        self.defs = []
        self.boxes = []
        self.shapes = []
        self.bg = bg
    def add(self, s):
        self.parts.append(s); return self
    def rect(self, x, y, w, h, fill="none", stroke="none", sw=1.5, rx=8, dash=None, opacity=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{opacity}"' if opacity is not None else ""
        if not COLLECT:
            self.shapes.append(("rect", x, y, x + w, y + h))
        return self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')
    def line(self, x1, y1, x2, y2, stroke=NAVY, sw=2, dash=None, cap="round", marker=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{marker})"' if marker else ""
        if not COLLECT:
            self.shapes.append(("line", x1, y1, x2, y2))
        return self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{d}{m}/>')
    def path(self, d, stroke=NAVY, sw=2, fill="none", dash=None, marker=None, cap="round", join="round", opacity=None):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{marker})"' if marker else ""
        o = f' opacity="{opacity}"' if opacity is not None else ""
        if not COLLECT:
            pts = _path_points(d)
            for a, b_ in zip(pts, pts[1:]):
                self.shapes.append(("line", a[0], a[1], b_[0], b_[1]))
        return self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="{join}"{ds}{m}{o}/>')
    def circle(self, cx, cy, r, fill="none", stroke="none", sw=2, opacity=None):
        o = f' opacity="{opacity}"' if opacity is not None else ""
        if not COLLECT:
            self.shapes.append(("circle", cx, cy, r, 0))
        return self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{o}/>')
    def ellipse(self, cx, cy, rx, ry, fill="none", stroke="none", sw=2):
        return self.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def image(self, x, y, w, h, path, rx=0):
        data = base64.b64encode(open(path, "rb").read()).decode("ascii")
        ext = os.path.splitext(path)[1].lstrip(".").lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext or "png"
        if not COLLECT:
            self.shapes.append(("rect", x, y, x + w, y + h))
        clip = ""
        if rx:
            self._clip_n = getattr(self, "_clip_n", 0) + 1
            cid = f"imgclip{self._clip_n}"
            self.defs.append(f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}"/></clipPath>')
            clip = f' clip-path="url(#{cid})"'
        return self.add(f'<image x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" href="data:image/{mime};base64,{data}"{clip} preserveAspectRatio="xMidYMid meet"/>')
    def image_fit(self, x, y, w, h, path, pad=0):
        from PIL import Image as _Image
        with _Image.open(path) as im:
            iw, ih = im.size
        bw, bh = w - 2 * pad, h - 2 * pad
        scale = min(bw / iw, bh / ih)
        dw, dh = iw * scale, ih * scale
        return self.image(x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, path)
    def poly(self, pts, fill="none", stroke="none", sw=2):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return self.add(f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')
    def text(self, x, y, s, size=16, fill=INK, weight=400, anchor="start", family=FAMILY, opacity=None, ls=None):
        o = f' opacity="{opacity}"' if opacity is not None else ""
        l = f' letter-spacing="{ls}"' if ls else ""
        if s.strip() and not COLLECT:
            w = tw(s, size, weight, family)
            x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
            self.boxes.append((x0, y - size * 0.80, x0 + w, y + size * 0.26, s))
        return self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{o}{l}>{html.escape(s)}</text>')
    def overlaps(self, pad=1.5):
        hits = []
        b = self.boxes
        for i in range(len(b)):
            ax0, ay0, ax1, ay1, at = b[i]
            for j in range(i + 1, len(b)):
                bx0, by0, bx1, by1, bt = b[j]
                ox = min(ax1, bx1) - max(ax0, bx0)
                oy = min(ay1, by1) - max(ay0, by0)
                if ox > pad and oy > pad:
                    hits.append((at, bt, round(ox, 1), round(oy, 1)))
        return hits
    def graphic_clashes(self, pad=2.0):
        def seg_inside_len(x1, y1, x2, y2, bx0, by0, bx1, by1):
            dx, dy = x2 - x1, y2 - y1
            t0, t1 = 0.0, 1.0
            for p, q in ((-dx, x1 - bx0), (dx, bx1 - x1), (-dy, y1 - by0), (dy, by1 - y1)):
                if p == 0:
                    if q < 0:
                        return 0.0
                    continue
                t = q / p
                if p < 0:
                    if t > t1:
                        return 0.0
                    t0 = max(t0, t)
                else:
                    if t < t0:
                        return 0.0
                    t1 = min(t1, t)
            if t0 > t1:
                return 0.0
            return ((t1 - t0) ** 2 * (dx * dx + dy * dy)) ** 0.5
        circles = [sh for sh in self.shapes if sh[0] == "circle"]
        def badged(bx0, by0, bx1, by1):
            cxm, cym = (bx0 + bx1) / 2, (by0 + by1) / 2
            for _, cx, cy, r, _f in circles:
                if (cxm - cx) ** 2 + (cym - cy) ** 2 <= r * r and (bx1 - bx0) <= 2.2 * r:
                    return True
            return False
        hits = []
        for bx0, by0, bx1, by1, t in self.boxes:
            if not t.strip() or badged(bx0, by0, bx1, by1):
                continue
            for sh in self.shapes:
                if sh[0] == "line":
                    _, x1, y1, x2, y2 = sh
                    inside = seg_inside_len(x1, y1, x2, y2, bx0 + pad, by0 + pad, bx1 - pad, by1 - pad)
                    if inside > max(14.0, 0.28 * (bx1 - bx0)):
                        hits.append(("line crosses", t))
                        break
                elif sh[0] == "circle":
                    _, cx, cy, r, _f = sh
                    inside = ((bx0 - cx) ** 2 + (by0 - cy) ** 2 <= r * r and
                              (bx1 - cx) ** 2 + (by1 - cy) ** 2 <= r * r and
                              (bx0 - cx) ** 2 + (by1 - cy) ** 2 <= r * r and
                              (bx1 - cx) ** 2 + (by0 - cy) ** 2 <= r * r)
                    if inside:
                        continue
                    nx = min(max(cx, bx0 + pad), bx1 - pad)
                    ny = min(max(cy, by0 + pad), by1 - pad)
                    if (nx - cx) ** 2 + (ny - cy) ** 2 < r * r:
                        hits.append(("circle overlaps", t))
                        break
                elif sh[0] == "rect":
                    _, rx0, ry0, rx1, ry1 = sh
                    inside = rx0 <= bx0 and bx1 <= rx1 and ry0 <= by0 and by1 <= ry1
                    outside = bx1 < rx0 or bx0 > rx1 or by1 < ry0 or by0 > ry1
                    if inside or outside:
                        continue
                    ox = min(bx1, rx1) - max(bx0, rx0)
                    oy = min(by1, ry1) - max(by0, ry0)
                    if ox > pad * 3 and oy > pad * 3:
                        hits.append(("box edge cuts", t))
                        break
        return hits
    def out_of_frame(self, margin=0.0):
        bad = []
        for x0, y0, x1, y1, t in self.boxes:
            if x0 < -margin or x1 > self.w + margin or y0 < -margin or y1 > self.h + margin:
                bad.append((t, round(x0, 1), round(x1, 1), round(y0, 1), round(y1, 1)))
        return bad
    def textlines(self, x, y, lines, size=16, fill=INK, weight=400, anchor="start", lh=1.42, family=FAMILY):
        for i, ln in enumerate(lines):
            self.text(x, y + i * size * lh, ln, size, fill, weight, anchor, family)
        return self
    def title(self, s, size=23, y=None, fill=NAVY):
        y = y if y is not None else size + 14
        self.text(self.w / 2, y, s, size, fill, 700, "middle")
        return self
    def box_auto(self, cx, y, text, size=16, pad_x=20, pad_y=13, fill=LIGHT, stroke=STEEL, tcolor=NAVY, weight=600, max_w=None, rx=9, sw=1.8, min_w=0, lh=1.4):
        lines = wrap(text, max_w, size, weight) if max_w else [text]
        wd = max(tw(l, size, weight) for l in lines)
        w = max(wd + 2 * pad_x, min_w)
        line_h = size * lh
        h = len(lines) * line_h + 2 * pad_y - (line_h - size * 1.02)
        x = cx - w / 2
        self.rect(x, y, w, h, fill, stroke, sw, rx)
        first = y + pad_y + size * 0.80
        for i, ln in enumerate(lines):
            self.text(cx, first + i * line_h, ln, size, tcolor, weight, "middle")
        return x, y, w, h
    def badge(self, cx, cy, s, r=17, fill=NAVY, tcolor="#FFFFFF", size=15):
        self.circle(cx, cy, r, fill)
        self.text(cx, cy + size * 0.35, s, size, tcolor, 700, "middle")
        return self
    def arrow_defs(self, color=STEEL, name="ar", size=13):
        if any(f'id="{name}"' in d for d in self.defs):
            return name
        self.defs.append(
            f'<marker id="{name}" viewBox="0 0 10 10" refX="8.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse">'
            f'<path d="M 0.5 0.8 L 9.5 5 L 0.5 9.2 z" fill="{color}"/></marker>')
        return name
    def heart(self, cx, cy, r, fill="#E24A3B", stroke="#B32A22", sw=2):
        k = r / 16.0
        d = (f"M {cx:.1f} {cy + 15*k:.1f} "
             f"C {cx - 6*k:.1f} {cy + 9*k:.1f} {cx - 16*k:.1f} {cy + 2*k:.1f} "
             f"{cx - 16*k:.1f} {cy - 5*k:.1f} "
             f"C {cx - 16*k:.1f} {cy - 12*k:.1f} {cx - 7*k:.1f} {cy - 14*k:.1f} "
             f"{cx:.1f} {cy - 6*k:.1f} "
             f"C {cx + 7*k:.1f} {cy - 14*k:.1f} {cx + 16*k:.1f} {cy - 12*k:.1f} "
             f"{cx + 16*k:.1f} {cy - 5*k:.1f} "
             f"C {cx + 16*k:.1f} {cy + 2*k:.1f} {cx + 6*k:.1f} {cy + 9*k:.1f} "
             f"{cx:.1f} {cy + 15*k:.1f} Z")
        return self.path(d, stroke, sw, fill)
    def check(self, cx, cy, r, color=GREEN, bg="#FFFFFF"):
        self.circle(cx, cy, r, bg, color, r * 0.17)
        self.path(f"M {cx-r*0.45:.1f} {cy+r*0.02:.1f} l {r*0.32:.1f} {r*0.36:.1f} l {r*0.62:.1f} {-r*0.72:.1f}", color, r * 0.20, cap="round")
        return self
    def fit(self, bottom=None, pad=18):
        if bottom is None:
            ys = [float(m) for m in re.findall(r'y2?="(-?[\d.]+)"', "".join(self.parts))]
            bottom = max(ys) if ys else self.h
        self.h = int(round(bottom + pad))
        return self
    def shadow_defs(self, name="sh"):
        self.defs.append(
            f'<filter id="{name}" x="-20%" y="-20%" width="140%" height="140%">'
            f'<feDropShadow dx="0" dy="1.5" stdDeviation="2" flood-color="#0F3357" flood-opacity="0.16"/></filter>')
        return name
    def clip_begin(self, x, y, w, h, rx=0):
        self._clip_n = getattr(self, "_clip_n", 0) + 1
        cid = f"clip{self._clip_n}"
        self.defs.append(f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}"/></clipPath>')
        self.parts.append(f'<g clip-path="url(#{cid})">')
        return cid
    def clip_end(self):
        self.parts.append("</g>")
        return self
    def render(self):
        defs = ("<defs>" + "".join(self.defs) + "</defs>") if self.defs else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
                f'{defs}<rect width="{self.w}" height="{self.h}" fill="{self.bg}"/>'
                + "".join(self.parts) + "</svg>")
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(self.render())
        return path
