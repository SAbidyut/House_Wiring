#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""slidekit — the RAPTI house-wiring slide engine (python-pptx).

One `Deck` object writes a chapter deck.  Every slide method takes
`brief=` — in the merged brief deck only the slides marked `brief=True`
(plus each chapter's divider and summary) are kept, so the brief deck is
built from exactly the same chapter specs and can never drift from them.

Design ("Blueprint & Gold", from the book cover):
  * dark slides  — cover, summary, closing: navy blueprint grid + gold
  * light slides — white, navy title, gold accents, rounded ice-blue cards
  * motif        — numbered gold badges and rounded image frames

Text is Kalpurush (the book's font, shipped in Book/).  Glyphs Kalpurush
does not have (Ω ° ² √ π φ ≈ …, and ÷, which it draws as +) are routed to
Arial run by run.  Text is measured with PIL + raqm (real Bangla shaping)
so every box is sized before it is written; anything that still does not
fit at the floor size is reported as a WARN line.

Read README.md in this folder for the authoring API.
"""
import os, re, io, json, math, hashlib, uuid, copy, urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BOOK = os.path.join(ROOT, "Book", "build")
CACHE = os.path.join(HERE, ".cache")
ICONS = os.path.join(HERE, "icons")
OUTDIR = os.path.join(ROOT, "Slides")
CH_OUT = os.path.join(OUTDIR, "অধ্যায়ভিত্তিক স্লাইড")
FONT_FILE = os.path.join(ROOT, "Book", "Kalpurush.ttf")
SYM_FILE = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
os.makedirs(CACHE, exist_ok=True)

FACE = "Kalpurush"
SYM_FACE = "Arial"

# ── palette ────────────────────────────────────────────────────────────
NAVY = "0A2440"; NAVY2 = "17406B"; BLUE = "2C6CA8"; SKY = "6FA8DC"
ICE = "EDF3F9"; ICE2 = "DCE7F2"; PALE = "A9C8E4"; NEARW = "E9F1F8"
GOLD = "C8A64B"; GOLD_L = "DFC57E"; GOLD_D = "8A6D1F"
INK = "1E2935"; MUTED = "5D6D7E"; LINE = "D2DCE7"; WHITE = "FFFFFF"
RED = "B83227"; RED_T = "FBEDEB"; GREEN = "2A7F4F"; GREEN_T = "E7F4EC"
AMBER = "B06A00"; AMBER_T = "FCF2E0"; VIOLET = "5B4A9E"; VIOLET_T = "EFECF8"
KINDS = {  # callout kinds → (accent, tint, icon, default label)
    "danger":  (RED, RED_T, "warning", "সতর্কতা"),
    "warning": (AMBER, AMBER_T, "warning", "সাবধান"),
    "tip":     (GREEN, GREEN_T, "idea", "টিপস"),
    "note":    (BLUE, ICE, "info", "মনে রাখুন"),
    "rule":    (VIOLET, VIOLET_T, "book", "মানদণ্ড"),
    "good":    (GREEN, GREEN_T, "check", "সঠিক"),
    "bad":     (RED, RED_T, "cross", "ভুল"),
    "info":    (NAVY2, ICE, "info", "তথ্য"),
}

SW, SH = 13.333, 7.5          # slide size (in)
MX = 0.6                      # side margin
BY, BB = 1.62, 6.72           # body top / bottom
BW = SW - 2 * MX

BN_DIG = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
def bn(x): return str(x).translate(BN_DIG)
def bn2(n): return bn(f"{n:02d}")

WARNINGS = []
def warn(msg):
    WARNINGS.append(msg)
    print("WARN", msg)

# ── text measurement ───────────────────────────────────────────────────
_KF = ImageFont.truetype(FONT_FILE, 100, layout_engine=ImageFont.Layout.RAQM)
_SF = ImageFont.truetype(SYM_FILE, 100)
from fontTools.ttLib import TTFont as _TT
_KCMAP = set(_TT(FONT_FILE).getBestCmap().keys())
_SCMAP = set(_TT(SYM_FILE).getBestCmap().keys())
_BAD_IN_K = {ord("÷")}

LH = 1.25        # Kalpurush line pitch (em); LibreOffice measures 1.20 — 4 % slack for PowerPoint
BOLD_W = 1.035   # fake-bold widening


def is_sym(ch):
    o = ord(ch)
    return (o not in _KCMAP or o in _BAD_IN_K) and o in _SCMAP


def clean(s):
    """Drop characters neither font can draw (emoji, other scripts)."""
    out = []
    for ch in str(s):
        o = ord(ch)
        if ch in "\n\t" or (o in _KCMAP and o not in _BAD_IN_K) or o in _SCMAP:
            out.append(ch)
        elif o in _BAD_IN_K:
            out.append(ch)
    return "".join(out)


def split_sym(s):
    """[(segment, is_symbol_font)] runs."""
    segs, cur, cs = [], "", None
    for ch in s:
        f = is_sym(ch)
        if cs is None or f == cs or ch == " ":
            cur += ch
            cs = f if cs is None or ch != " " else cs
        else:
            segs.append((cur, cs)); cur, cs = ch, f
    if cur:
        segs.append((cur, cs))
    return segs


def text_w(s, pt, bold=False):
    w = 0.0
    for seg, sym in split_sym(s):
        w += (_SF if sym else _KF).getlength(seg, **({} if sym else {"language": "bn"}))
    return w * pt / 100.0 * (BOLD_W if bold else 1.0) / 72.0     # inches


def parse_marks(s):
    """'**bold** rest' → [(text, bold)]"""
    parts = re.split(r"(\*\*.+?\*\*)", s)
    out = []
    for p in parts:
        if not p:
            continue
        if p.startswith("**") and p.endswith("**"):
            out.append((p[2:-2], True))
        else:
            out.append((p, False))
    return out


def count_lines(text, pt, width_in, bold=False):
    """Greedy word wrap of marked-up text; returns number of lines."""
    if width_in <= 0:
        return 99
    lines = 0
    for para in str(text).split("\n"):
        words = []
        for seg, b in parse_marks(para):
            for i, w in enumerate(re.split(r"( +)", seg)):
                if w:
                    words.append((w, b or bold))
        cur = 0.0
        lines += 1
        for w, b in words:
            ww = text_w(w, pt, b)
            if w.strip() == "":
                cur += ww
                continue
            if cur > 0 and cur + ww > width_in:
                lines += 1
                cur = ww
            else:
                cur += ww
    return lines


class P(dict):
    """A paragraph spec.  P(text, pt=, c=, b=, bul=, lvl=, al=, sa=, lh=)"""
    def __init__(self, t, **kw):
        super().__init__(t=t, **kw)


def para_height(p, width_in, pt):
    pt = p.get("pt", pt)
    ind = p.get("ind", 0.32 if p.get("bul") else 0.0) + p.get("lvl", 0) * 0.32
    n = count_lines(p["t"], pt, width_in - ind, p.get("b", False))
    lh = p.get("lh", 0.92)
    return n * pt * LH * lh / 72.0, n


def block_height(paras, width_in, pt, sa_ratio=0.45):
    h = 0.0
    for i, p in enumerate(paras):
        ph, _ = para_height(p, width_in, pt * p.get("rel", 1.0))
        h += ph
        if i < len(paras) - 1:
            h += p.get("sa", pt * p.get("rel", 1.0) * sa_ratio) / 72.0
    return h


def fit_pt(paras, width_in, height_in, pt_max, pt_min, sa_ratio=0.45, label=""):
    pt = pt_max
    while pt > pt_min and block_height(paras, width_in, pt, sa_ratio) > height_in:
        pt -= 0.5
    if block_height(paras, width_in, pt, sa_ratio) > height_in * 1.02:
        warn(f"overflow {label!r}: needs {block_height(paras, width_in, pt, sa_ratio):.2f}in "
             f"> {height_in:.2f}in at {pt}pt")
    return pt


# ── low-level XML helpers ──────────────────────────────────────────────
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
def _sub(parent, tag, **attrs):
    el = etree.SubElement(parent, qn(tag))
    for k, v in attrs.items():
        el.set(k, str(v))
    return el


def _rgb(hexs):
    return RGBColor.from_string(hexs)


def _set_run(r, text, pt, color, bold=False, sym=False, link=None):
    r.text = text
    rPr = r._r.get_or_add_rPr()
    for ch in list(rPr):
        rPr.remove(ch)
    rPr.set("lang", "bn-BD" if not sym else "en-US")
    rPr.set("altLang", "en-US")
    rPr.set("sz", str(int(round(pt * 100))))
    rPr.set("b", "1" if bold else "0")
    rPr.set("dirty", "0")
    fill = _sub(rPr, "a:solidFill"); _sub(fill, "a:srgbClr", val=color)
    face = SYM_FACE if sym else FACE
    _sub(rPr, "a:latin", typeface=face)
    _sub(rPr, "a:ea", typeface=face)
    _sub(rPr, "a:cs", typeface=face)
    if link:
        r.hyperlink.address = link


def _para_props(p, spec, pt):
    pPr = p._p.get_or_add_pPr()
    for ch in list(pPr):
        pPr.remove(ch)
    al = spec.get("al", "l")
    pPr.set("algn", {"l": "l", "c": "ctr", "r": "r", "j": "just"}[al])
    lvl = spec.get("lvl", 0)
    lh = spec.get("lh", 0.92)
    ln = _sub(pPr, "a:lnSpc"); _sub(ln, "a:spcPct", val=int(lh * 100000))
    if spec.get("sb"):
        sb = _sub(pPr, "a:spcBef"); _sub(sb, "a:spcPts", val=int(spec["sb"] * 100))
    sa = spec.get("sa_eff", 0)
    s = _sub(pPr, "a:spcAft"); _sub(s, "a:spcPts", val=int(sa * 100))
    bul = spec.get("bul")
    if bul:
        ind = spec.get("ind", 0.32) + lvl * 0.32
        pPr.set("marL", str(int(Inches(ind))))
        pPr.set("indent", str(int(-Inches(spec.get("ind", 0.32)))))
        c = _sub(pPr, "a:buClr"); _sub(c, "a:srgbClr", val=spec.get("bc", GOLD))
        _sub(pPr, "a:buSzPct", val=spec.get("bsz", 75000))
        _sub(pPr, "a:buFont", typeface="Arial")
        _sub(pPr, "a:buChar", char=bul if isinstance(bul, str) else "●")
    else:
        if lvl:
            pPr.set("marL", str(int(Inches(lvl * 0.32))))
        _sub(pPr, "a:buNone")


def write_paras(tf, paras, pt, color, sa_ratio=0.45, bold_color=None):
    for i, spec in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        ppt = spec.get("pt", pt * spec.get("rel", 1.0))
        spec = dict(spec)
        spec["sa_eff"] = 0 if i == len(paras) - 1 else spec.get("sa", ppt * sa_ratio)
        _para_props(p, spec, ppt)
        col = spec.get("c", color)
        bcol = spec.get("bcol", bold_color or col)
        for text, b in parse_marks(clean(spec["t"])):
            b = b or spec.get("b", False)
            for seg, sym in split_sym(text):
                _set_run(p.add_run(), seg, ppt, bcol if (b and not spec.get("b")) else col,
                         bold=b, sym=sym, link=spec.get("link"))


def _no_autofit(tf, inset=(0, 0, 0, 0), anchor="t", wrap=True):
    bp = tf._txBody.bodyPr
    for ch in list(bp):
        bp.remove(ch)
    for k, v in zip(("lIns", "tIns", "rIns", "bIns"), inset):
        bp.set(k, str(int(Inches(v))))
    bp.set("wrap", "square" if wrap else "none")
    bp.set("anchor", {"t": "t", "m": "ctr", "b": "b"}[anchor])
    bp.set("rtlCol", "0")
    _sub(bp, "a:noAutofit")


def _shadow(shape, blur=9, dist=2.5, alpha=16, color=NAVY):
    spPr = shape._element.spPr
    for e in spPr.findall(qn("a:effectLst")):
        spPr.remove(e)
    eff = _sub(spPr, "a:effectLst")
    sh = _sub(eff, "a:outerShdw", blurRad=int(Pt(blur)), dist=int(Pt(dist)), dir=5400000,
              algn="t", rotWithShape=0)
    c = _sub(sh, "a:srgbClr", val=color); _sub(c, "a:alpha", val=alpha * 1000)


def _name(shape, name):
    shape._element.xpath("./*[1]/p:cNvPr")[0].set("name", name)


# ── image preparation ──────────────────────────────────────────────────
def _hash(*parts):
    return hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:16]


def resolve(path):
    """Accept absolute paths, 'chNN/name' diagram keys, or 'assets/…' keys."""
    if os.path.isabs(path) and os.path.exists(path):
        return path
    cands = [
        os.path.join(CACHE, "diagrams", path + ".png"),
        os.path.join(CACHE, "diagrams", path),
        os.path.join(BOOK, "assets", path),
        os.path.join(BOOK, path),
        os.path.join(HERE, path),
        os.path.join(ROOT, path),
    ]
    for c in cands:
        if os.path.exists(c) and os.path.isfile(c):
            return c
    raise FileNotFoundError(path)


def _is_photo(path, im):
    if path.lower().endswith((".jpg", ".jpeg")):
        return True
    return False


def prep_image(path, maxpx=2000, trim=True):
    """Trim white margins, downscale, cache.  Returns (path, w, h, is_photo)."""
    src = resolve(path)
    key = _hash(src, os.path.getmtime(src), maxpx, trim, "v3")
    meta = os.path.join(CACHE, "img", key + ".json")
    if os.path.exists(meta):
        m = json.load(open(meta))
        if os.path.exists(m["path"]):
            return m["path"], m["w"], m["h"], m["photo"]
    os.makedirs(os.path.join(CACHE, "img"), exist_ok=True)
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    photo = _is_photo(src, im)
    if im.mode in ("P", "LA", "RGBA"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    if trim and not photo:
        g = im.convert("L").point(lambda v: 255 if v < 244 else 0)
        bbox = g.getbbox()
        if bbox:
            pad = int(0.012 * max(im.size))
            x0, y0, x1, y1 = bbox
            im = im.crop((max(0, x0 - pad), max(0, y0 - pad),
                          min(im.width, x1 + pad), min(im.height, y1 + pad)))
    if max(im.size) > maxpx:
        s = maxpx / max(im.size)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    out = os.path.join(CACHE, "img", key + (".jpg" if photo else ".png"))
    tmp = f"{out}.{os.getpid()}.tmp"
    if photo:
        im.save(tmp, "JPEG", quality=86, optimize=True)
    else:
        im.save(tmp, "PNG", optimize=True)
    os.replace(tmp, out)
    tmpm = f"{meta}.{os.getpid()}.tmp"
    json.dump({"path": out, "w": im.width, "h": im.height, "photo": photo}, open(tmpm, "w"))
    os.replace(tmpm, meta)
    return out, im.width, im.height, photo


def fit_box(iw, ih, bw, bh):
    s = min(bw / iw, bh / ih)
    return iw * s, ih * s


# ── generated art ──────────────────────────────────────────────────────
def dark_bg(variant="a"):
    out = os.path.join(CACHE, f"bg_dark_{variant}.png")
    if os.path.exists(out):
        return out
    W, H, S = 1920, 1080, 2
    im = Image.new("RGB", (W * S, H * S))
    top, bot = (10, 36, 64), (18, 56, 96)
    px = ImageDraw.Draw(im)
    for y in range(H * S):
        t = y / (H * S)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        px.line([(0, y), (W * S, y)], fill=c)
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    step = 40 * S
    for x in range(0, W * S, step):
        d.line([(x, 0), (x, H * S)], fill=(169, 200, 228, 14 if (x // step) % 5 else 30), width=S)
    for y in range(0, H * S, step):
        d.line([(0, y), (W * S, y)], fill=(169, 200, 228, 14 if (y // step) % 5 else 30), width=S)
    # circuit motif — traces + nodes in the right-hand corner
    mot = (111, 168, 220, 70)
    gold = (200, 166, 75, 120)
    rnd = [(1480, 120, 1700, 120, 1700, 300, 1860, 300), (1560, 210, 1560, 420, 1800, 420),
           (1380, 980, 1380, 840, 1640, 840, 1640, 700, 1900, 700), (1500, 1000, 1500, 920, 1760, 920),
           (1300, 60, 1300, 180, 1420, 180)]
    if variant == "b":
        rnd = [(60, 980, 260, 980, 260, 860, 520, 860), (140, 1040, 140, 920),
               (1500, 80, 1500, 200, 1780, 200, 1780, 340), (1640, 140, 1880, 140)]
    for pts in rnd:
        pts = [p * S for p in pts]
        d.line(pts, fill=mot, width=3 * S, joint="curve")
        for i in range(0, len(pts), 2):
            x, y = pts[i], pts[i + 1]
            r = 7 * S
            d.ellipse([x - r, y - r, x + r, y + r], outline=gold if i in (0, len(pts) - 2) else mot,
                      width=3 * S, fill=(10, 36, 64, 255))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    im = im.resize((W, H), Image.LANCZOS)
    im.save(out, optimize=True)
    return out


def icon(name, color="white"):
    p = os.path.join(ICONS, f"{name}_{color}.png")
    if not os.path.exists(p):
        warn(f"icon missing {name}")
        p = os.path.join(ICONS, f"info_{color}.png")
    return p


_MPL = None
def math_png(tex, color=NAVY, fs=40):
    """LaTeX-ish mathtext → transparent PNG.  Returns (path, w_in, h_in) at fs pt."""
    global _MPL
    key = _hash(tex, color, fs, "m2")
    out = os.path.join(CACHE, "math", key + ".png")
    meta = out + ".json"
    if os.path.exists(meta):
        m = json.load(open(meta))
        return out, m["w"], m["h"]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if _MPL is None:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        matplotlib.rcParams["mathtext.fontset"] = "stix"
        matplotlib.rcParams["font.family"] = "STIXGeneral"
        _MPL = plt
    plt = _MPL
    fig = plt.figure(figsize=(0.01, 0.01))
    t = fig.text(0, 0, tex if "$" in tex else f"${tex}$", fontsize=fs, color="#" + color)
    tmp = f"{out}.{os.getpid()}.tmp.png"
    fig.savefig(tmp, dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    os.replace(tmp, out)
    im = Image.open(out)
    w, h = im.width / 300.0, im.height / 300.0
    tmpm = f"{meta}.{os.getpid()}.tmp"
    json.dump({"w": w, "h": h}, open(tmpm, "w"))
    os.replace(tmpm, meta)
    return out, w, h


def qr_png(url):
    import qrcode
    out = os.path.join(CACHE, "qr", _hash(url) + ".png")
    if os.path.exists(out):
        return out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    q = qrcode.QRCode(border=1, box_size=12, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url); q.make(fit=True)
    tmp = f"{out}.{os.getpid()}.tmp"
    q.make_image(fill_color="#0A2440", back_color="white").convert("RGB").save(tmp, "PNG")
    os.replace(tmp, out)
    return out


# ── videos ─────────────────────────────────────────────────────────────
_VIDEOS = None
def video_info(vid):
    global _VIDEOS
    if _VIDEOS is None:
        _VIDEOS = {}
        p = os.path.join(HERE, "videos.json")
        if os.path.exists(p):
            for ch, lst in json.load(open(p, encoding="utf-8")).items():
                for v in lst:
                    _VIDEOS[v["id"]] = v
    if vid in _VIDEOS:
        return _VIDEOS[vid]
    cp = os.path.join(CACHE, "oembed.json")
    cache = json.load(open(cp)) if os.path.exists(cp) else {}
    if vid not in cache:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
        d = json.load(urllib.request.urlopen(url, timeout=30))
        cache[vid] = {"id": vid, "title": d["title"], "channel": d["author_name"], "lang": "en",
                      "duration": "", "views": "", "why": []}
        json.dump(cache, open(cp, "w"), ensure_ascii=False, indent=1)
    return cache[vid]


def thumb_png(vid, duration=""):
    out = os.path.join(CACHE, "thumbs", f"{vid}.jpg")
    if os.path.exists(out):
        return out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    raw = None
    for q in ("maxresdefault", "sddefault", "hqdefault"):
        try:
            data = urllib.request.urlopen(f"https://i.ytimg.com/vi/{vid}/{q}.jpg", timeout=30).read()
            im = Image.open(io.BytesIO(data)).convert("RGB")
            if im.width >= 480 and len(data) > 2000:
                raw = im
                break
        except Exception:
            continue
    if raw is None:
        raise RuntimeError(f"no thumbnail for {vid}")
    # strip letterbox bars (sd/hq thumbnails are 4:3 with black bands)
    g = raw.convert("L").point(lambda v: 255 if v > 22 else 0)
    bb = g.getbbox() or (0, 0, raw.width, raw.height)
    raw = raw.crop((0, bb[1], raw.width, bb[3]))
    tw, th = 1280, 720
    s = max(tw / raw.width, th / raw.height)
    raw = raw.resize((int(raw.width * s) + 1, int(raw.height * s) + 1), Image.LANCZOS)
    x0, y0 = (raw.width - tw) // 2, (raw.height - th) // 2
    im = raw.crop((x0, y0, x0 + tw, y0 + th)).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    # soft darkening so the play button reads on any thumbnail
    for i in range(240):
        d.line([(0, th - 240 + i), (tw, th - 240 + i)], fill=(5, 18, 36, int(150 * i / 240)))
    cx, cy, r = tw // 2, th // 2, 92
    d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], fill=(255, 255, 255, 70))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 40, 40, 235))
    tri = [(cx - 30, cy - 46), (cx - 30, cy + 46), (cx + 50, cy)]
    d.polygon(tri, fill=(255, 255, 255, 255))
    if duration:
        f = ImageFont.truetype(SYM_FILE, 44)
        tw2 = d.textlength(duration, font=f)
        d.rounded_rectangle([tw - tw2 - 60, th - 92, tw - 24, th - 30], 10, fill=(0, 0, 0, 200))
        d.text((tw - tw2 - 42, th - 86), duration, font=f, fill=(255, 255, 255, 255))
    im = Image.alpha_composite(im, ov).convert("RGB")
    tmp = f"{out}.{os.getpid()}.tmp"
    im.save(tmp, "JPEG", quality=88)
    os.replace(tmp, out)
    return out


# ── the deck ───────────────────────────────────────────────────────────
class Deck:
    def __init__(self, mode="full"):
        self.mode = mode
        self.prs = Presentation()
        self.prs.slide_width = Inches(SW)
        self.prs.slide_height = Inches(SH)
        sz = self.prs.part._element.find(qn("p:sldSz"))
        if sz is not None and "type" in sz.attrib:
            del sz.attrib["type"]
        self.toc_slide = None
        self._theme()
        self.layout = self.prs.slide_layouts[5]      # Title Only
        self.ch = None
        self.chapters = []          # (n, title, first_slide)
        self.n_slides = 0

    # ── chapter context ────────────────────────────────────────────────
    def chapter(self, n, title, short=None, next_title=None):
        self.ch, self.title = n, title
        self.short = short or title
        self.next_title = next_title
        self.chapters.append({"n": n, "title": title, "first": None, "slides": []})
        return self

    def D(self, name, ch=None):
        """Diagram key for this chapter: D('d07_five_rules') → 'chNN/d07_five_rules'."""
        return f"ch{(ch or self.ch):02d}/{name}"

    def A(self, name, ch=None):
        """Book asset: A('ph_mcb_face.jpg') → 'assets/chNN/…'.  A('hwbook/x.jpg') also works."""
        if "/" in name:
            return f"assets/{name}"
        return f"assets/ch{(ch or self.ch):02d}/{name}"

    # ── theme ──────────────────────────────────────────────────────────
    def _theme(self):
        master = self.prs.slide_masters[0]
        from pptx.opc.constants import RELATIONSHIP_TYPE as RT
        theme = master.part.part_related_by(RT.THEME)
        root = etree.fromstring(theme.blob)
        ns = {"a": A}
        cs = root.find(".//a:clrScheme", ns)
        cs.set("name", "RAPTI Blueprint")
        cols = {"dk1": INK, "lt1": WHITE, "dk2": NAVY, "lt2": ICE, "accent1": NAVY2,
                "accent2": GOLD, "accent3": BLUE, "accent4": GREEN, "accent5": RED,
                "accent6": AMBER, "hlink": BLUE, "folHlink": VIOLET}
        for k, v in cols.items():
            el = cs.find(f"a:{k}", ns)
            for ch in list(el):
                el.remove(ch)
            etree.SubElement(el, f"{{{A}}}srgbClr").set("val", v)
        fs = root.find(".//a:fontScheme", ns)
        fs.set("name", "RAPTI Kalpurush")
        for which in ("majorFont", "minorFont"):
            f = fs.find(f"a:{which}", ns)
            for tag in ("latin", "ea", "cs"):
                f.find(f"a:{tag}", ns).set("typeface", FACE)
            for el in f.findall("a:font", ns):
                if el.get("script") == "Beng":
                    el.set("typeface", FACE)
        theme._blob = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)

    # ── slide frames ───────────────────────────────────────────────────
    def _keep(self, brief):
        return self.mode == "full" or brief

    def _new(self, dark=False, bg_variant="a"):
        s = self.prs.slides.add_slide(self.layout)
        self.n_slides += 1
        if self.chapters:
            c = self.chapters[-1]
            c["slides"].append(s)
            if c["first"] is None:
                c["first"] = s
        if dark:
            self._bg_image(s, dark_bg(bg_variant))
        else:
            s.background.fill.solid()
            s.background.fill.fore_color.rgb = _rgb(WHITE)
        self._transition(s)
        return s

    def _bg_image(self, slide, path):
        _, rId = slide.part.get_or_add_image_part(path)
        cSld = slide._element.find(qn("p:cSld"))
        old = cSld.find(qn("p:bg"))
        if old is not None:
            cSld.remove(old)
        bg = etree.Element(qn("p:bg"))
        bgPr = _sub(bg, "p:bgPr")
        bf = _sub(bgPr, "a:blipFill", dpi=0, rotWithShape=1)
        blip = _sub(bf, "a:blip")
        blip.set(qn("r:embed"), rId)
        _sub(bf, "a:srcRect")
        st = _sub(bf, "a:stretch"); _sub(st, "a:fillRect")
        _sub(bgPr, "a:effectLst")
        cSld.insert(0, bg)

    def _transition(self, slide):
        el = slide._element
        clr = el.find(qn("p:clrMapOvr"))
        tr = etree.Element(qn("p:transition"))
        tr.set("spd", "med")
        _sub(tr, "p:fade")
        if clr is not None:
            clr.addnext(tr)

    def _title(self, s, text, x=MX, y=0.66, w=BW, h=0.78, pt=32, pt_min=24, color=NAVY,
               al="l", anchor="m", lines=1):
        t = s.shapes.title
        t.left, t.top, t.width, t.height = Inches(x), Inches(y), Inches(w), Inches(h)
        tf = t.text_frame
        _no_autofit(tf, anchor=anchor)
        size = pt
        while size > pt_min and count_lines(text, size, w, True) > lines:
            size -= 1
        if count_lines(text, size, w, True) > lines:
            warn(f"title wraps: {text!r}")
        write_paras(tf, [P(text, b=True, al=al, lh=0.9)], size, color)
        return t

    def _footer(self, s, dark=False):
        col = PALE if dark else MUTED
        if not dark:
            ic = s.shapes.add_picture(os.path.join(BOOK, "assets", "cover", "icon_rapti.png"),
                                      Inches(MX), Inches(7.0), Inches(0.24), Inches(0.24))
            _name(ic, "RAPTI icon")
        tb = s.shapes.add_textbox(Inches(MX + (0.32 if not dark else 0)), Inches(6.98),
                                  Inches(7), Inches(0.3))
        _name(tb, "Footer")
        _no_autofit(tb.text_frame, anchor="m")
        write_paras(tb.text_frame, [P("RAPTI  ·  ইলেকট্রিক্যাল হাউস ওয়্যারিং")], 10.5, col)
        # slide number field
        nb = s.shapes.add_textbox(Inches(SW - MX - 1.0), Inches(6.98), Inches(1.0), Inches(0.3))
        _name(nb, "Slide number")
        tf = nb.text_frame
        _no_autofit(tf, anchor="m")
        p = tf.paragraphs[0]
        _para_props(p, {"al": "r"}, 11)
        fld = _sub(p._p, "a:fld", id="{" + str(uuid.uuid4()).upper() + "}", type="slidenum")
        rPr = _sub(fld, "a:rPr", lang="en-US", sz="1100", b="0")
        f = _sub(rPr, "a:solidFill"); _sub(f, "a:srgbClr", val=col)
        _sub(rPr, "a:latin", typeface=FACE); _sub(rPr, "a:cs", typeface=FACE)
        _sub(fld, "a:t").text = str(len(self.prs.slides))

    def _tag(self, s, tag=None, dark=False):
        text = tag or f"অধ্যায় {bn2(self.ch)}  ·  {self.short}"
        dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(MX), Inches(0.37), Inches(0.13), Inches(0.13))
        dot.fill.solid(); dot.fill.fore_color.rgb = _rgb(GOLD); dot.line.fill.background()
        _name(dot, "Tag dot")
        tb = s.shapes.add_textbox(Inches(MX + 0.24), Inches(0.24), Inches(9), Inches(0.38))
        _name(tb, "Chapter tag")
        _no_autofit(tb.text_frame, anchor="m")
        write_paras(tb.text_frame, [P(text)], 13, PALE if dark else MUTED)

    def _light(self, title, tag=None, notes=None):
        s = self._new()
        self._tag(s, tag)
        self._title(s, title)
        self._footer(s)
        if notes:
            self._notes(s, notes)
        return s

    def _notes(self, s, text):
        tf = s.notes_slide.notes_text_frame
        paras = [P(t) for t in str(text).strip().split("\n") if t.strip()]
        write_paras(tf, paras, 14, INK, sa_ratio=0.3)

    # ── building blocks ────────────────────────────────────────────────
    def text(self, s, x, y, w, h, paras, pt=20, pt_min=14, color=INK, anchor="t",
             sa_ratio=0.45, bold_color=None, label="", fit=True, name="Text"):
        paras = [p if isinstance(p, P) else P(p) for p in paras]
        if fit:
            pt = fit_pt(paras, w, h, pt, pt_min, sa_ratio, label=label or paras[0]["t"][:30])
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        _name(tb, name)
        _no_autofit(tb.text_frame, anchor=anchor)
        write_paras(tb.text_frame, paras, pt, color, sa_ratio, bold_color)
        return tb, pt

    def card(self, s, x, y, w, h, fill=ICE, line=None, radius=0.08, shadow=False, name="Card"):
        sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        _name(sh, name)
        sh.adjustments[0] = min(0.5, radius / min(w, h))
        sh.fill.solid(); sh.fill.fore_color.rgb = _rgb(fill)
        if line:
            sh.line.color.rgb = _rgb(line); sh.line.width = Pt(1)
        else:
            sh.line.fill.background()
        if shadow:
            _shadow(sh)
        sh.text_frame.text = ""
        return sh

    def badge(self, s, x, y, d, text, fill=GOLD, color=NAVY, pt=None, shape=MSO_SHAPE.OVAL):
        sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(d), Inches(d))
        _name(sh, "Badge")
        sh.fill.solid(); sh.fill.fore_color.rgb = _rgb(fill); sh.line.fill.background()
        tf = sh.text_frame
        _no_autofit(tf, anchor="m", wrap=False)
        write_paras(tf, [P(str(text), b=True, al="c", lh=1.0)], pt or d * 34, color)
        return sh

    def icon_badge(self, s, x, y, d, name, fill=NAVY, color="white"):
        c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
        _name(c, f"Icon circle {name}")
        c.fill.solid(); c.fill.fore_color.rgb = _rgb(fill); c.line.fill.background()
        c.text_frame.text = ""
        m = d * 0.24
        pic = s.shapes.add_picture(icon(name, color), Inches(x + m), Inches(y + m),
                                   Inches(d - 2 * m), Inches(d - 2 * m))
        _name(pic, f"Icon {name}")
        return c

    def picture(self, s, path, x, y, w, h, frame=None, align="c", valign="m", link=None,
                caption=None, cap_pt=13, dark=False, maxpx=2000, round_photo=True):
        """Fit an image into (x,y,w,h).  Diagrams sit on a white rounded card;
        photos get rounded corners.  Returns (left, top, width, height) used."""
        cap_h = 0.42 if caption else 0
        img, iw, ih, photo = prep_image(path, maxpx=maxpx)
        if frame is None:
            frame = not photo
        pad = 0.14 if frame else 0
        bw, bh = w - 2 * pad, h - cap_h - 2 * pad
        pw, ph = fit_box(iw, ih, bw, bh)
        fx = x + {"l": 0, "c": (w - pw - 2 * pad) / 2, "r": w - pw - 2 * pad}[align]
        fy = y + {"t": 0, "m": (h - cap_h - ph - 2 * pad) / 2, "b": h - cap_h - ph - 2 * pad}[valign]
        if frame:
            c = self.card(s, fx, fy, pw + 2 * pad, ph + 2 * pad, fill=WHITE,
                          line=None if dark else LINE, radius=0.12, shadow=True, name="Image frame")
        pic = s.shapes.add_picture(img, Inches(fx + pad), Inches(fy + pad), Inches(pw), Inches(ph))
        _name(pic, "Picture")
        pic._element.xpath("./p:nvPicPr/p:cNvPr")[0].set(
            "descr", clean(caption or os.path.splitext(os.path.basename(str(path)))[0]))
        if photo and round_photo and not frame:
            geom = pic._element.spPr.find(qn("a:prstGeom"))
            geom.set("prst", "roundRect")
            av = geom.find(qn("a:avLst"))
            if av is None:
                av = _sub(geom, "a:avLst")
            gd = _sub(av, "a:gd", name="adj", fmla="val 5000")
            _shadow(pic)
        if link:
            pic.click_action.hyperlink.address = link
        if caption:
            cw = max(pw + 2 * pad, min(w, 4.0))
            cx = fx + (pw + 2 * pad - cw) / 2
            cx = max(x, min(cx, x + w - cw))
            self.text(s, cx, fy + ph + 2 * pad + 0.06, cw, cap_h - 0.04,
                      [P(caption, al="c")], pt=cap_pt, pt_min=10.5,
                      color=PALE if dark else MUTED, name="Caption")
        return fx, fy, pw + 2 * pad, ph + 2 * pad

    def bullets_block(self, s, x, y, w, h, items, pt=20, pt_min=14, color=INK, bc=GOLD,
                      anchor="t", label=""):
        paras = []
        for it in items:
            if isinstance(it, (list, tuple)):
                paras.append(P(it[0], bul="●", bc=bc))
                for sub in it[1]:
                    paras.append(P(sub, bul="–", lvl=1, rel=0.88, bc=MUTED))
            else:
                paras.append(P(it, bul="●", bc=bc))
        return self.text(s, x, y, w, h, paras, pt, pt_min, color, anchor=anchor,
                         sa_ratio=0.55, bold_color=NAVY, label=label)

    # ══════════════════════════════════════════════════════════════════
    # SLIDE TYPES
    # ══════════════════════════════════════════════════════════════════
    def cover(self, hero=None, subtitle=None, notes=None):
        """Chapter cover (dark).  In the brief deck this is the chapter divider."""
        s = self._new(dark=True)
        self._title(s, self.title, x=0.85, y=2.25, w=6.7, h=2.1, pt=48, pt_min=34,
                    color=WHITE, anchor="t", lines=2)
        lab = s.shapes.add_textbox(Inches(0.85), Inches(1.45), Inches(5), Inches(0.6))
        _no_autofit(lab.text_frame, anchor="m")
        write_paras(lab.text_frame, [P(f"অধ্যায় {bn2(self.ch)}", b=True)], 26, GOLD)
        _name(lab, "Chapter number")
        rule = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.87), Inches(2.08), Inches(0.9), Inches(0.05))
        rule.fill.solid(); rule.fill.fore_color.rgb = _rgb(GOLD); rule.line.fill.background()
        nl = count_lines(self.title, 48, 6.7, True)
        if subtitle:
            self.text(s, 0.85, 2.25 + (1.05 if nl == 1 else 2.0), 6.5, 1.2, [P(subtitle)],
                      pt=20, pt_min=15, color=PALE, name="Subtitle")
        logo = s.shapes.add_picture(os.path.join(BOOK, "assets", "cover", "logo_rapti_light.png"),
                                    Inches(0.85), Inches(6.05), Inches(1.75))
        _name(logo, "RAPTI logo")
        self.text(s, 2.85, 6.08, 4.6, 0.55,
                  [P("ইলেকট্রিক্যাল হাউস ওয়্যারিং"), P("প্রশিক্ষণ স্লাইড", c=GOLD_L)],
                  pt=13, pt_min=11, color=NEARW, sa_ratio=0.1, name="Course")
        if hero:
            self.picture(s, hero, 7.75, 1.0, 4.95, 5.5, frame=True, dark=True)
        if self.mode == "brief" and self.toc_slide is not None:
            tb, _ = self.text(s, SW - 3.4, 6.95, 2.8, 0.35, [P("↩ সূচিপত্রে ফিরুন", al="r")], pt=12,
                              pt_min=11, color=GOLD_L, name="Back to contents", fit=False)
            tb.click_action.target_slide = self.toc_slide
        if notes:
            self._notes(s, notes)
        return s

    def objectives(self, items, title="এই অধ্যায়ে যা শিখব", notes=None, brief=False):
        if not self._keep(brief):
            return
        s = self._light(title, notes=notes)
        n = len(items)
        cols = 2 if n > 4 else 1
        rows = math.ceil(n / cols)
        gap = 0.22
        cw = (BW - (cols - 1) * 0.35) / cols
        ch = min(1.2, (BB - BY - (rows - 1) * gap) / rows)
        tw = cw - 1.05 - 0.25
        pt = 21
        while pt > 14 and any(count_lines(t, pt, tw) * pt * LH * 0.92 / 72 > ch - 0.16 for t in items):
            pt -= 0.5
        total = rows * ch + (rows - 1) * gap
        top = BY + max(0, (BB - BY - total) / 2)
        for i, t in enumerate(items):
            c, r = (i // rows, i % rows) if cols == 2 else (0, i)
            x = MX + c * (cw + 0.35)
            y = top + r * (ch + gap)
            self.card(s, x, y, cw, ch, fill=ICE)
            self.badge(s, x + 0.22, y + (ch - 0.6) / 2, 0.6, bn(i + 1), pt=20)
            self.text(s, x + 1.05, y + 0.05, tw, ch - 0.1, [P(t)], pt=pt, pt_min=pt,
                      anchor="m", fit=False, bold_color=NAVY)
            if count_lines(t, pt, tw) * pt * LH * 0.92 / 72 > ch - 0.08:
                warn(f"objective overflow: {t[:40]}")
        return s

    def agenda(self, sections, title="অধ্যায়ের রূপরেখা", notes=None, brief=False):
        """sections = [("১.১", "শিরোনাম"), …]  → numbered roadmap tiles."""
        if not self._keep(brief):
            return
        s = self._light(title, notes=notes)
        n = len(sections)
        cols = 3 if n > 6 else 2 if n > 3 else 1
        cols = 4 if n > 12 else cols
        rows = math.ceil(n / cols)
        gap = 0.2
        cw = (BW - (cols - 1) * gap) / cols
        gap = 0.25
        ch = min(1.3, (BB - BY - (rows - 1) * gap) / rows)
        tw = cw - 1.3
        pt = 21
        while pt > 13 and any(count_lines(t, pt, tw, True) * pt * LH * 0.9 / 72 > ch - 0.15 for _, t in sections):
            pt -= 0.5
        top = BY + max(0, (BB - BY - rows * ch - (rows - 1) * gap) / 2)
        for i, (num, t) in enumerate(sections):
            c, r = i % cols, i // cols
            x, y = MX + c * (cw + gap), top + r * (ch + gap)
            self.card(s, x, y, cw, ch, fill=ICE)
            self.text(s, x + 0.1, y, 1.1, ch, [P(num, b=True, al="c")], pt=24, pt_min=14,
                      color=GOLD_D, anchor="m", name="Sec num")
            self.text(s, x + 1.2, y + 0.05, tw, ch - 0.1, [P(t, b=True)], pt=pt, pt_min=pt,
                      color=NAVY, anchor="m", fit=False)
        return s

    def section(self, num, title, sub=None, notes=None, brief=False):
        if not self._keep(brief):
            return
        s = self._new(dark=True, bg_variant="b")
        self.text(s, 0.85, 1.9, 4, 1.2, [P(num, b=True)], pt=60, pt_min=40, color=GOLD, name="Sec num")
        self._title(s, title, x=0.85, y=3.1, w=10.5, h=1.6, pt=42, pt_min=30, color=WHITE,
                    anchor="t", lines=2)
        if sub:
            self.text(s, 0.85, 4.75, 10, 1.2, [P(sub)], pt=20, pt_min=15, color=PALE)
        self._footer(s, dark=True)
        if notes:
            self._notes(s, notes)
        return s

    def bullets(self, title, items, img=None, caption=None, side="right", img_w=None,
                layout=None, notes=None, brief=False, tag=None, pt=21):
        """Text bullets, optionally beside (or under) an image.
        items: ["text", ("text", ["sub", "sub"]), …]  — **bold** allowed."""
        if not self._keep(brief):
            return
        s = self._light(title, tag=tag, notes=notes)
        if not img:
            self.bullets_block(s, MX, BY, BW, BB - BY, items, pt=pt, label=title)
            return s
        _, iw, ih, _ = prep_image(img)
        asp = iw / ih
        if layout is None:
            layout = "stack" if asp > 2.3 else "side"
        if layout == "stack":
            th = min(2.0, 0.3 + 0.55 * len(items))
            self.bullets_block(s, MX, BY, BW, th, items, pt=min(pt, 20), label=title)
            self.picture(s, img, MX, BY + th + 0.15, BW, BB - BY - th - 0.15, caption=caption)
            return s
        if img_w is None:
            img_w = 6.3 if asp >= 1.25 else 5.2 if asp >= 0.85 else 4.2
        tw = BW - img_w - 0.45
        if side == "right":
            tx, ix = MX, MX + tw + 0.45
        else:
            ix, tx = MX, MX + img_w + 0.45
        fx, fy, fw, fh = self.picture(s, img, ix, BY, img_w, BB - BY, caption=caption)
        self.bullets_block(s, tx, BY, tw, BB - BY, items, pt=pt, label=title, anchor="m")
        return s

    def rows(self, title, rows, img=None, caption=None, notes=None, brief=False, tag=None):
        """Icon rows: [(icon, head, body)] — icon name from icons/ ('bolt', 'shield', …)."""
        if not self._keep(brief):
            return
        s = self._light(title, tag=tag, notes=notes)
        w = BW
        if img:
            _, iw, ih, _ = prep_image(img)
            img_w = 5.6 if iw / ih >= 1.2 else 4.6
            self.picture(s, img, MX + BW - img_w, BY, img_w, BB - BY, caption=caption)
            w = BW - img_w - 0.45
        n = len(rows)
        gap = 0.16
        rh = min(1.4, (BB - BY - (n - 1) * gap) / n)
        tw = w - 1.0
        pt = 21
        def need(pt):
            return max(count_lines(h_, pt + 1, tw, True) * (pt + 1) * LH * 0.9 / 72 +
                       (count_lines(b_, pt, tw) * pt * LH * 0.92 / 72 if b_ else 0) + 0.05
                       for _, h_, b_ in rows)
        while pt > 13.5 and need(pt) > rh - 0.08:
            pt -= 0.5
        if need(pt) > rh:
            warn(f"rows overflow: {title}")
        top = BY + max(0, (BB - BY - n * rh - (n - 1) * gap) / 2)
        for i, (ic, head, body) in enumerate(rows):
            y = top + i * (rh + gap)
            self.card(s, MX, y, w, rh, fill=ICE)
            d = min(0.62, rh - 0.24)
            self.icon_badge(s, MX + 0.18, y + (rh - d) / 2, d, ic)
            paras = [P(head, b=True, c=NAVY, rel=(pt + 1) / pt, lh=0.9, sa=2)]
            if body:
                paras.append(P(body))
            self.text(s, MX + 1.0, y + 0.04, tw, rh - 0.08, paras, pt=pt, pt_min=pt,
                      anchor="m", fit=False, sa_ratio=0.1)
        return s

    def cards(self, title, cards, cols=None, img=None, caption=None, notes=None, brief=False,
              tag=None, pt=22):
        """Grid of cards.  cards = [dict(head=, body=, icon=|num=, color=, tint=)] or (head, body)."""
        if not self._keep(brief):
            return
        s = self._light(title, tag=tag, notes=notes)
        cards = [c if isinstance(c, dict) else {"head": c[0], "body": c[1]} for c in cards]
        n = len(cards)
        x0, w, top_lim, bot_lim = MX, BW, BY, BB
        stack = False
        if img:
            asp = self._aspect(img)
            if asp >= 1.9:
                stack = True
                cols = cols or n
            else:
                img_w = 5.4 if asp >= 1.2 else 4.4
                self.picture(s, img, MX + BW - img_w, BY, img_w, BB - BY, caption=caption)
                w = BW - img_w - 0.4
        if cols is None:
            cols = (2 if n in (2, 4) else 3) if not img else (1 if n <= 3 else 2)
            if n >= 7 and not img:
                cols = 4
        rows_ = math.ceil(n / cols)
        gap = 0.25
        cw = (w - (cols - 1) * gap) / cols
        has_top = any(c.get("icon") or c.get("num") is not None for c in cards)
        side_icon = has_top and (cw < 2.6 or stack)
        tw = cw - 0.4 - (0.78 if side_icon else 0)
        def paras_of(c):
            ps = [P(c["head"], b=True, rel=1.1, lh=0.9, sa=5)]
            if c.get("body"):
                ps.append(P(c["body"]))
            return ps
        def need(sz):
            return max(block_height(paras_of(c), tw, sz, 0.3) for c in cards)
        head_off = 1.02 if has_top and not side_icon else 0.22
        chh_max = (bot_lim - top_lim - (rows_ - 1) * gap) / rows_
        if stack:
            chh_max = min(chh_max, 2.0)
        size = pt
        while size > 13.5 and need(size) > chh_max - head_off - 0.25:
            size -= 0.5
        if need(size) > chh_max - head_off - 0.15:
            warn(f"cards overflow: {title}")
        chh = min(chh_max, max(need(size) + head_off + 0.4, 1.35 if side_icon else 1.9))
        if side_icon:
            chh = max(chh, 0.95)
        total = rows_ * chh + (rows_ - 1) * gap
        top = top_lim if stack else top_lim + max(0, (bot_lim - top_lim - total) / 2)
        for i, c in enumerate(cards):
            col, r = i % cols, i // cols
            x, y = x0 + col * (cw + gap), top + r * (chh + gap)
            accent = c.get("color", NAVY)
            self.card(s, x, y, cw, chh, fill=c.get("tint", ICE))
            tx, ty, th_ = x + 0.22, y + head_off, chh - head_off - 0.15
            mark = c.get("icon") or (c.get("num") is not None)
            if mark and side_icon:
                d = 0.6
                if c.get("icon"):
                    self.icon_badge(s, x + 0.18, y + 0.2, d, c["icon"], fill=accent)
                else:
                    self.badge(s, x + 0.18, y + 0.2, d, c["num"], pt=19)
                tx, ty, th_ = x + 0.98, y + 0.12, chh - 0.24
            elif mark:
                if c.get("icon"):
                    self.icon_badge(s, x + 0.22, y + 0.25, 0.64, c["icon"], fill=accent)
                else:
                    self.badge(s, x + 0.22, y + 0.25, 0.62, c["num"], pt=20)
            self.text(s, tx, ty, tw, th_, paras_of(c), pt=size, pt_min=size, fit=False,
                      sa_ratio=0.3, bold_color=NAVY, color=INK,
                      anchor="m" if side_icon else "t")
            # heading colour
        if stack:
            y0 = top + total + 0.25
            self.picture(s, img, MX, y0, BW, BB - y0, caption=caption)
        return s

    def steps(self, title, steps, img=None, caption=None, notes=None, brief=False, tag=None):
        """Process flow.  steps = [(head, body)].  Horizontal (≤6) or vertical with an image."""
        if not self._keep(brief):
            return
        s = self._light(title, tag=tag, notes=notes)
        n = len(steps)
        asp = self._aspect(img) if img else None
        horizontal = (not img and n <= 5) or (img and asp >= 1.9 and n <= 6)
        if horizontal:
            gap = 0.25 if n > 4 else 0.3
            cw = (BW - (n - 1) * gap) / n
            def pars(h_, b_):
                return [P(h_, b=True, c=NAVY, al="c", rel=1.08, sa=4)] + ([P(b_, al="c")] if b_ else [])
            avail = BB - BY - 1.0
            if img:
                avail = 2.2
            size = 21 if not img else 18
            while size > 13 and max(block_height(pars(h_, b_), cw - 0.3, size, 0.3) for h_, b_ in steps) > avail - 0.35:
                size -= 0.5
            need = max(block_height(pars(h_, b_), cw - 0.3, size, 0.3) for h_, b_ in steps)
            if need > avail - 0.25:
                warn(f"steps overflow: {title}")
            th = min(avail, max(need + 0.4, 1.3))
            total = 0.95 + th
            y0 = BY if img else BY + max(0, (BB - BY - total) / 2)
            line = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(MX + cw / 2), Inches(y0 + 0.34),
                                      Inches(BW - cw), Inches(0.05))
            line.fill.solid(); line.fill.fore_color.rgb = _rgb(GOLD_L); line.line.fill.background()
            _name(line, "Flow line")
            for i, (h_, b_) in enumerate(steps):
                x = MX + i * (cw + gap)
                self.badge(s, x + cw / 2 - 0.36, y0, 0.72, bn(i + 1), pt=22)
                self.card(s, x, y0 + 0.95, cw, th, fill=ICE)
                self.text(s, x + 0.15, y0 + 0.95, cw - 0.3, th, pars(h_, b_), pt=size,
                          pt_min=size, fit=False, sa_ratio=0.3, anchor="m")
            if img:
                yi = y0 + total + 0.25
                self.picture(s, img, MX, yi, BW, BB - yi, caption=caption)
            return s
        # vertical list (optionally with image)
        w = BW
        if img:
            img_w = 6.0 if asp >= 1.2 else 4.8
            self.picture(s, img, MX + BW - img_w, BY, img_w, BB - BY, caption=caption)
            w = BW - img_w - 0.45
        gap = 0.12
        rh_max = (BB - BY - (n - 1) * gap) / n
        tw = w - 0.85
        size = 20
        def lab(h_, b_):
            return f"**{h_}**: {b_}" if b_ else f"**{h_}**"
        def need(sz):
            return max(block_height([P(lab(h_, b_))], tw, sz) for h_, b_ in steps)
        while size > 13.5 and need(size) > rh_max - 0.06:
            size -= 0.5
        if need(size) > rh_max:
            warn(f"steps overflow: {title}")
        rh = min(rh_max, max(need(size) + 0.2, 0.62))
        total = n * rh + (n - 1) * gap
        top = BY + max(0, (BB - BY - total) / 2)
        for i, (h_, b_) in enumerate(steps):
            y = top + i * (rh + gap)
            d = min(0.52, rh - 0.06)
            if i < n - 1:
                ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(MX + d / 2 - 0.02),
                                        Inches(y + (rh + d) / 2), Inches(0.04), Inches(rh + gap - d))
                ln.fill.solid(); ln.fill.fore_color.rgb = _rgb(GOLD_L); ln.line.fill.background()
            self.badge(s, MX, y + (rh - d) / 2, d, bn(i + 1), pt=min(18, d * 34))
            self.text(s, MX + 0.75, y, tw, rh, [P(lab(h_, b_))],
                      pt=size, pt_min=size, anchor="m", fit=False, bold_color=NAVY)
        return s

    def table(self, title, header, rows, widths=None, note=None, img=None, caption=None,
              notes=None, brief=False, tag=None, pt=20, hl_col=None):
        """Native table.  rows = [[cell, …]], **bold** allowed in cells."""
        if not self._keep(brief):
            return
        s = self._light(title, tag=tag, notes=notes)
        x, w = MX, BW
        stack = False
        if img:
            asp = self._aspect(img)
            if asp >= 1.9:
                stack = True
            else:
                img_w = 4.6 if asp >= 1.2 else 3.8
                self.picture(s, img, MX + BW - img_w, BY, img_w, BB - BY, caption=caption)
                w = BW - img_w - 0.4
        ncol = len(header)
        widths = widths or [1] * ncol
        tot = sum(widths)
        colw = [w * k / tot for k in widths]
        note_h = (0.25 + block_height([P(note)], w - 0.9, 15)) if note else 0
        avail = BB - BY - note_h - (0.15 if note else 0)
        if stack:
            avail = min(avail, (BB - BY) * 0.55)
        size = pt
        def heights(sz):
            hs = []
            for r_i, row in enumerate([header] + rows):
                hmax = 0
                for ci, cell in enumerate(row):
                    hb = block_height([P(str(cell), b=(r_i == 0))], colw[ci] - 0.22, sz)
                    hmax = max(hmax, hb)
                hs.append(hmax + 0.17)
            return hs
        while size > 12 and sum(heights(size)) > avail:
            size -= 0.5
        hs = heights(size)
        if sum(hs) > avail * 1.03:
            warn(f"table overflow: {title} ({sum(hs):.2f} > {avail:.2f})")
        elif not stack:
            extra = min((avail - sum(hs)) / len(hs), 0.22)
            hs = [h_ + max(0, extra) for h_ in hs]
        gt = s.shapes.add_table(len(rows) + 1, ncol, Inches(x), Inches(BY), Inches(w),
                                Inches(sum(hs)))
        _name(gt, "Table")
        tbl = gt.table
        tblPr = tbl._tbl.tblPr
        tblPr.set("firstRow", "1"); tblPr.set("bandRow", "0")
        sid = tblPr.find(qn("a:tableStyleId"))
        if sid is not None:
            sid.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"   # No Style, Table Grid
        for ci, cw_ in enumerate(colw):
            tbl.columns[ci].width = Inches(cw_)
        for ri, row in enumerate([header] + rows):
            tbl.rows[ri].height = Inches(hs[ri])
            for ci in range(ncol):
                cell = tbl.cell(ri, ci)
                txt = str(row[ci]) if ci < len(row) else ""
                cell.margin_left = cell.margin_right = Inches(0.11)
                cell.margin_top = cell.margin_bottom = Inches(0.06)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                fill = NAVY if ri == 0 else (ICE if ri % 2 == 0 else WHITE)
                if ri > 0 and hl_col is not None and ci == hl_col:
                    fill = "F6EFD9" if ri % 2 else "EFE4C3"
                cell.fill.solid(); cell.fill.fore_color.rgb = _rgb(fill)
                tf = cell.text_frame
                tf.word_wrap = True
                write_paras(tf, [P(txt, b=(ri == 0), al="c" if ri == 0 else "l", lh=0.9)],
                            size, WHITE if ri == 0 else INK, bold_color=NAVY)
                tcPr = cell._tc.get_or_add_tcPr()
                for side in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
                    ln = tcPr.find(qn(side))
                    if ln is not None:
                        tcPr.remove(ln)
                for side in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
                    ln = etree.Element(qn(side), w=str(int(Pt(0.75))))
                    sf = _sub(ln, "a:solidFill"); _sub(sf, "a:srgbClr", val=LINE)
                    first_fill = tcPr.find(qn("a:solidFill"))
                    if first_fill is not None:
                        first_fill.addprevious(ln)
                    else:
                        tcPr.append(ln)
        y = BY + sum(hs) + 0.2
        if note:
            self.note_box(s, x, y, w, note_h, note)
            y += note_h + 0.2
        if stack:
            self.picture(s, img, MX, y, BW, BB - y, caption=caption)
        return s

    def note_box(self, s, x, y, w, h, text, kind="note"):
        accent, tint, ic, _ = KINDS[kind]
        self.card(s, x, y, w, h, fill=tint)
        d = min(0.46, h - 0.14)
        self.icon_badge(s, x + 0.14, y + (h - d) / 2, d, ic, fill=accent)
        self.text(s, x + 0.75, y + 0.04, w - 0.9, h - 0.08, [P(text)], pt=15, pt_min=12.5,
                  anchor="m", bold_color=accent)

    def formula(self, title, tex, legend=None, note=None, img=None, caption=None, extra=None,
                notes=None, brief=False, tag=None, big=46):
        """Display formula (mathtext, e.g. r'I = \\frac{V}{R}') + symbol legend.
        legend = [("V", "ভোল্টেজ (ভোল্ট, V)"), …]   extra = more formulas shown smaller."""
        if not self._keep(brief):
            return
        s = self._light(title, tag=tag, notes=notes)
        w = BW
        if img:
            _, iw, ih, _ = prep_image(img)
            img_w = 5.4 if iw / ih >= 1.2 else 4.4
            self.picture(s, img, MX + BW - img_w, BY, img_w, BB - BY, caption=caption)
            w = BW - img_w - 0.45
        forms = [tex] + list(extra or [])
        # formula panel
        imgs = []
        for i, t in enumerate(forms):
            p, fw, fh = math_png(t, NAVY, 40)
            sc = (big if i == 0 else big * 0.72) / 40
            imgs.append((p, fw * sc, fh * sc))
        maxw = w - 0.8
        shrink = min(1.0, maxw / max(iw_ for _, iw_, _ in imgs))
        imgs = [(p, a * shrink, b * shrink) for p, a, b in imgs]
        ph = sum(b for _, _, b in imgs) + 0.25 * (len(imgs) - 1) + 0.6
        self.card(s, MX, BY, w, ph, fill=ICE)
        y = BY + 0.3
        for p, a, b in imgs:
            pic = s.shapes.add_picture(p, Inches(MX + (w - a) / 2), Inches(y), Inches(a), Inches(b))
            _name(pic, "Formula")
            y += b + 0.25
        y = BY + ph + 0.3
        if legend:
            cols = 2 if len(legend) > 3 and w > 9 else 1
            rows_ = math.ceil(len(legend) / cols)
            cw = (w - (cols - 1) * 0.3) / cols
            nh = (0.25 + block_height([P(note)], w - 0.9, 15)) if note else 0
            avail = BB - y - (nh + 0.2 if note else 0)
            rh = min(0.72, avail / rows_)
            for i, (sym, meaning) in enumerate(legend):
                c, r = i // rows_, i % rows_
                lx, ly = MX + c * (cw + 0.3), y + r * rh
                p, fw, fh = math_png(sym, GOLD_D, 40)
                sc = min(30 / 40, (rh - 0.1) / fh)
                sym_w = min(fw * sc, 1.3)
                sc = min(sc, 1.3 / fw)
                pic = s.shapes.add_picture(p, Inches(lx + 0.1 + (1.3 - fw * sc) / 2),
                                           Inches(ly + (rh - fh * sc) / 2), Inches(fw * sc), Inches(fh * sc))
                _name(pic, "Symbol")
                self.text(s, lx + 1.6, ly, cw - 1.6, rh, [P(meaning)], pt=20, pt_min=13,
                          anchor="m", name="Legend")
            y += rows_ * rh + 0.2
        if note:
            nh = 0.25 + block_height([P(note)], w - 0.9, 15)
            self.note_box(s, MX, min(y, BB - nh), w, nh, note, kind="tip")
        return s

    def example(self, title, question, given=None, find=None, steps=None, answer=None,
                note=None, notes=None, brief=False, tag=None):
        """Worked example.  steps are mathtext strings (Latin only — no Bangla)."""
        if not self._keep(brief):
            return
        s = self._light(title, tag=tag, notes=notes)
        lw = 5.3
        rx = MX + lw + 0.35
        rw = BW - lw - 0.35
        self.card(s, MX, BY, lw, BB - BY, fill=ICE)
        paras = [P("প্রশ্ন", b=True, c=GOLD_D, rel=0.85, sa=2), P(question, sa=10)]
        if given:
            paras.append(P("প্রদত্ত", b=True, c=GOLD_D, rel=0.85, sa=2))
            paras += [P(g, bul="●", bc=GOLD, sa=2) for g in given]
            paras[-1]["sa"] = 10
        if find:
            paras.append(P("নির্ণেয়", b=True, c=GOLD_D, rel=0.85, sa=2))
            paras += [P(f, bul="●", bc=GOLD, sa=2) for f in find]
        self.text(s, MX + 0.28, BY + 0.22, lw - 0.56, BB - BY - 0.44, paras, pt=20, pt_min=13,
                  bold_color=NAVY, label=title, anchor="m")
        tb = s.shapes.add_textbox(Inches(rx), Inches(BY), Inches(3), Inches(0.45))
        _no_autofit(tb.text_frame, anchor="m")
        write_paras(tb.text_frame, [P("সমাধান", b=True)], 17, GOLD_D)
        steps = steps or []
        ans_h = (0.32 + block_height([P(f"উত্তর: {answer}")], rw - 1.0, 19)) if answer else 0
        note_h = (0.25 + block_height([P(note)], rw - 0.9, 15)) if note else 0
        avail = BB - (BY + 0.6) - ans_h - (0.25 if answer else 0) - note_h - (0.2 if note else 0)
        ims = [math_png(t, INK, 40) for t in steps]
        gap = 0.2
        target = 34.0
        tot = lambda pt: sum(h * pt / 40 for _, _, h in ims) + gap * max(0, len(ims) - 1)
        while target > 14 and (tot(target) > avail or
                               max([w_ * target / 40 for _, w_, _ in ims] or [0]) > rw - 0.2):
            target -= 1
        if ims and (tot(target) > avail * 1.03 or max(w_ * target / 40 for _, w_, _ in ims) > rw):
            warn(f"example steps overflow: {title}")
        y = BY + 0.62
        for p, w_, h in ims:
            pic = s.shapes.add_picture(p, Inches(rx + 0.15), Inches(y), Inches(w_ * target / 40),
                                       Inches(h * target / 40))
            _name(pic, "Step")
            y += h * target / 40 + gap
        if answer:
            ay = min(y + 0.1, BB - ans_h - note_h - (0.2 if note else 0))
            self.card(s, rx, ay, rw, ans_h, fill=GREEN_T)
            self.icon_badge(s, rx + 0.16, ay + (ans_h - 0.52) / 2, 0.52, "check", fill=GREEN)
            self.text(s, rx + 0.85, ay, rw - 1.0, ans_h, [P(f"**উত্তর:** {answer}")], pt=19,
                      pt_min=14, anchor="m", bold_color=GREEN)
            y = ay + ans_h + 0.2
        if note:
            self.note_box(s, rx, min(y, BB - note_h), rw, note_h, note, kind="tip")
        return s

    def callout(self, title, text, kind="danger", label=None, img=None, caption=None,
                points=None, notes=None, brief=False, tag=None):
        """Big safety / tip / rule box (with optional image and points)."""
        if not self._keep(brief):
            return
        s = self._light(title, tag=tag, notes=notes)
        accent, tint, ic, deflabel = KINDS[kind]
        paras = [P(text)]
        if not img and not points:
            size = 30
            while size > 16 and block_height(paras, BW - 2.4, size) > BB - BY - 1.6:
                size -= 0.5
            box_h = max(2.6, 1.55 + block_height(paras, BW - 2.4, size))
            y0 = BY + max(0, (BB - BY - box_h) / 2)
            self.card(s, MX, y0, BW, box_h, fill=tint)
            self.icon_badge(s, MX + 0.45, y0 + 0.45, 1.1, ic, fill=accent)
            self.text(s, MX + 1.95, y0 + 0.42, BW - 2.4, 0.55, [P(label or deflabel, b=True)], pt=22,
                      pt_min=16, color=accent, name="Callout label")
            self.text(s, MX + 1.95, y0 + 1.05, BW - 2.4, box_h - 1.3, paras, pt=size, pt_min=size,
                      color=INK, bold_color=accent, anchor="t", fit=False)
            return s
        size = 22
        while size > 15 and block_height(paras, BW - 1.75, size) > 1.9:
            size -= 0.5
        box_h = 0.95 + block_height(paras, BW - 1.75, size) + 0.25
        self.card(s, MX, BY, BW, box_h, fill=tint)
        self.icon_badge(s, MX + 0.3, BY + 0.3, 0.85, ic, fill=accent)
        self.text(s, MX + 1.4, BY + 0.25, BW - 1.7, 0.5, [P(label or deflabel, b=True)], pt=18,
                  pt_min=14, color=accent, name="Callout label")
        self.text(s, MX + 1.4, BY + 0.78, BW - 1.75, box_h - 0.9, paras, pt=size, pt_min=size,
                  color=INK, bold_color=accent, anchor="t", fit=False)
        y = BY + box_h + 0.3
        pts_paras = [P(p_, bul="●", bc=accent) for p_ in (points or [])]
        if points and img:
            pw = 5.4
            self.text(s, MX + 0.1, y, pw, BB - y, pts_paras, pt=20, pt_min=14, sa_ratio=0.5,
                      bold_color=NAVY, anchor="m")
            self.picture(s, img, MX + pw + 0.4, y, BW - pw - 0.4, BB - y, caption=caption)
        elif points:
            self.text(s, MX + 0.2, y, BW - 0.2, BB - y, pts_paras, pt=21, pt_min=14, sa_ratio=0.5,
                      bold_color=NAVY)
        else:
            self.picture(s, img, MX, y, BW, BB - y, caption=caption)
        return s

    def compare(self, title, left, right, notes=None, brief=False, tag=None, img=None, caption=None):
        """Two columns.  left/right = dict(head=, items=[…], kind='good'|'bad'|'info'|…)."""
        if not self._keep(brief):
            return
        s = self._light(title, tag=tag, notes=notes)
        w = BW
        if img:
            img_w = 4.4
            self.picture(s, img, MX + BW - img_w, BY, img_w, BB - BY, caption=caption)
            w = BW - img_w - 0.4
        cw = (w - 0.35) / 2
        # common font size for both columns
        def paras(col):
            return [P(it, bul="●") for it in col["items"]]
        size = 22
        while size > 13.5 and max(block_height(paras(c), cw - 0.45 - 0.32, size, 0.55)
                                  for c in (left, right)) > BB - BY - 1.4:
            size -= 0.5
        for i, col in enumerate((left, right)):
            accent, tint, ic, _ = KINDS[col.get("kind", "info")]
            x = MX + i * (cw + 0.35)
            self.card(s, x, BY, cw, BB - BY, fill=tint)
            self.icon_badge(s, x + 0.22, BY + 0.22, 0.66, col.get("icon", ic), fill=accent)
            self.text(s, x + 1.05, BY + 0.22, cw - 1.25, 0.66, [P(col["head"], b=True)], pt=23,
                      pt_min=15, color=accent, anchor="m", name="Column head")
            self.bullets_block(s, x + 0.25, BY + 1.12, cw - 0.45, BB - BY - 1.3, col["items"],
                               pt=size, pt_min=size, bc=accent, label=col["head"])
        return s

    def stats(self, title, stats, note=None, notes=None, brief=False, tag=None, img=None, caption=None):
        """Big-number callouts: [("230 V", "বাসার সাপ্লাই ভোল্টেজ"), …]"""
        if not self._keep(brief):
            return
        s = self._light(title, tag=tag, notes=notes)
        n = len(stats)
        w = BW
        if img:
            img_w = 5.0
            self.picture(s, img, MX + BW - img_w, BY, img_w, BB - BY, caption=caption)
            w = BW - img_w - 0.4
        cols = n if (n <= 4 and not img) else 2 if n >= 2 else 1
        rows_ = math.ceil(n / cols)
        gap = 0.3
        nh = (0.3 + block_height([P(note)], w - 0.9, 15)) if note else 0
        cw = (w - (cols - 1) * gap) / cols
        avail = BB - BY - nh - (0.3 if note else 0)
        chh = min((avail - (rows_ - 1) * gap) / rows_, 2.9)
        vpt = 60
        while vpt > 24 and max(text_w(v, vpt, True) for v, _ in stats) > cw - 0.35:
            vpt -= 1
        lpt = 20
        while lpt > 13 and max(block_height([P(l_, al="c")], cw - 0.4, lpt) for _, l_ in stats) > chh - vpt / 72 * 1.4 - 0.45:
            lpt -= 0.5
        total = rows_ * chh + (rows_ - 1) * gap
        top = BY + max(0, (avail - total) / 2)
        for i, (val, lab) in enumerate(stats):
            c, r = i % cols, i // cols
            x, y = MX + c * (cw + gap), top + r * (chh + gap)
            self.card(s, x, y, cw, chh, fill=ICE)
            vh = vpt / 72 * 1.45
            self.text(s, x + 0.15, y + 0.2, cw - 0.3, vh, [P(val, b=True, al="c", lh=1.0)], pt=vpt,
                      pt_min=vpt, color=NAVY, anchor="m", fit=False, name="Stat value")
            bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + cw / 2 - 0.35), Inches(y + 0.25 + vh),
                                     Inches(0.7), Inches(0.05))
            bar.fill.solid(); bar.fill.fore_color.rgb = _rgb(GOLD); bar.line.fill.background()
            self.text(s, x + 0.2, y + 0.42 + vh, cw - 0.4, chh - vh - 0.55, [P(lab, al="c")],
                      pt=lpt, pt_min=lpt, color=INK, anchor="t", fit=False, name="Stat label")
        if note:
            self.note_box(s, MX, BB - nh, w, nh, note)
        return s

    def image(self, title, img, caption=None, points=None, note=None, notes=None, brief=False,
              tag=None, side="right"):
        """One large figure; optional short points beside (or under) it."""
        if not self._keep(brief):
            return
        s = self._light(title, tag=tag, notes=notes)
        asp = self._aspect(img)
        nh = (0.3 + block_height([P(note)], BW - 0.9, 15)) if note else 0
        avail_h = BB - BY - nh - (0.2 if note else 0)
        if points and asp >= 2.0:
            cols = 2 if len(points) > 2 else 1
            per = math.ceil(len(points) / cols)
            cwp = (BW - 0.4 * (cols - 1)) / cols
            ph = max(block_height([P(p_, bul="●") for p_ in points[i * per:(i + 1) * per]], cwp - 0.32, 19, 0.5)
                     for i in range(cols)) + 0.1
            ih = avail_h - ph - 0.25
            fx, fy, fw, fh = self.picture(s, img, MX, BY, BW, ih, caption=caption)
            y = fy + fh + (0.45 if caption else 0) + 0.25
            for i in range(cols):
                self.bullets_block(s, MX + i * (cwp + 0.4), y, cwp, BY + avail_h - y,
                                   points[i * per:(i + 1) * per], pt=19, pt_min=14, label=title)
        elif points:
            pw_ = 4.1 if asp > 1.3 else 4.8
            iw_box = BW - pw_ - 0.4
            ix = MX if side == "right" else MX + pw_ + 0.4
            px = MX + iw_box + 0.4 if side == "right" else MX
            self.picture(s, img, ix, BY, iw_box, avail_h, caption=caption)
            self.bullets_block(s, px, BY, pw_, avail_h, points, pt=20, pt_min=14, anchor="m",
                               label=title)
        else:
            self.picture(s, img, MX, BY, BW, avail_h, caption=caption)
        if note:
            self.note_box(s, MX, BB - nh, BW, nh, note)
        return s

    def gallery(self, title, items, cols=None, note=None, notes=None, brief=False, tag=None,
                cap_pt=15):
        """Photo grid: items = [(img, label)] — labels under each picture."""
        if not self._keep(brief):
            return
        s = self._light(title, tag=tag, notes=notes)
        n = len(items)
        cols = cols or (n if n <= 4 else 3 if n in (5, 6, 9) else 4)
        rows_ = math.ceil(n / cols)
        nh = (0.3 + block_height([P(note)], BW - 0.9, 15)) if note else 0
        gap = 0.3
        cw = (BW - (cols - 1) * gap) / cols
        chh = (BB - BY - nh - (0.2 if note else 0) - (rows_ - 1) * gap) / rows_
        lab_h = 0.5 if any(count_lines(l, cap_pt, cw - 0.2) > 1 for _, l in items) else 0.36
        for i, (img, lab) in enumerate(items):
            c, r = i % cols, i // cols
            # centre a short last row
            last_n = n - (rows_ - 1) * cols
            off = (cols - last_n) * (cw + gap) / 2 if r == rows_ - 1 and last_n < cols else 0
            x, y = MX + off + c * (cw + gap), BY + r * (chh + gap)
            self.card(s, x, y, cw, chh, fill=ICE)
            self.picture(s, img, x + 0.12, y + 0.12, cw - 0.24, chh - lab_h - 0.24, frame=False,
                         round_photo=True)
            self.text(s, x + 0.1, y + chh - lab_h - 0.08, cw - 0.2, lab_h, [P(lab, b=True, al="c")],
                      pt=cap_pt, pt_min=11, color=NAVY, anchor="m", name="Label")
        if note:
            self.note_box(s, MX, BB - nh, BW, nh, note)
        return s

    def video(self, vid, why=None, title=None, notes=None, brief=False, tag=None):
        """YouTube video card: clickable thumbnail + QR + details (from videos.json)."""
        if not self._keep(brief):
            return
        v = video_info(vid)
        url = f"https://www.youtube.com/watch?v={vid}"
        lang = v.get("lang", "en")
        s = self._light(title or "ভিডিওতে দেখে শিখি",
                        tag=tag, notes=notes or
                        f"ভিডিও: {v['title']} ({v['channel']})\n{url}\n"
                        "স্লাইড শো চলাকালে থাম্বনেইলে ক্লিক করলে ভিডিওটি ব্রাউজারে খুলবে (ইন্টারনেট লাগবে)।")
        tw_, th_ = 7.35, 7.35 * 9 / 16
        thumb = thumb_png(vid, v.get("duration", ""))
        pic = s.shapes.add_picture(thumb, Inches(MX), Inches(BY), Inches(tw_), Inches(th_))
        _name(pic, "Video thumbnail (click to play)")
        geom = pic._element.spPr.find(qn("a:prstGeom"))
        geom.set("prst", "roundRect")
        av = geom.find(qn("a:avLst"))
        if av is None:
            av = _sub(geom, "a:avLst")
        _sub(av, "a:gd", name="adj", fmla="val 4000")
        _shadow(pic, blur=14, dist=4, alpha=22)
        pic.click_action.hyperlink.address = url
        self.text(s, MX, BY + th_ + 0.12, tw_, 0.4,
                  [P(f"youtube.com/watch?v={vid}", al="c", link=url)], pt=13, pt_min=11,
                  color=BLUE, name="Video link")
        rx = MX + tw_ + 0.4
        rw = SW - MX - rx
        rapti = v.get("rapti") or v.get("channel") == "Resonance Automation"
        chip = "RAPTI-র নিজস্ব ভিডিও" if rapti else ("বাংলা ভিডিও" if lang == "bn" else "ইংরেজি ভিডিও")
        cw_ = text_w(chip, 14, True) + 0.75
        c = self.card(s, rx, BY, cw_, 0.42, fill=NAVY if rapti else RED, radius=0.21)
        ic = s.shapes.add_picture(icon("youtube", "white"), Inches(rx + 0.13), Inches(BY + 0.08),
                                  Inches(0.26), Inches(0.26))
        self.text(s, rx + 0.45, BY, cw_ - 0.5, 0.42, [P(chip, b=True)], pt=14, pt_min=12,
                  color=WHITE, anchor="m", name="Video language")
        vt = clean(v["title"])
        self.text(s, rx, BY + 0.6, rw, 1.25, [P(vt, b=True, lh=0.95)], pt=19, pt_min=14,
                  color=NAVY, name="Video title")
        meta = f"{clean(v['channel'])}" + (f"  ·  {v['duration']}" if v.get("duration") else "")
        self.text(s, rx, BY + 1.9, rw, 0.4, [P(meta)], pt=14, pt_min=11.5, color=MUTED,
                  name="Video channel")
        why = why or v.get("why") or []
        qr = 1.45
        if why:
            self.text(s, rx, BY + 2.42, rw, 0.4, [P("ভিডিওতে যা দেখবেন", b=True)], pt=16,
                      pt_min=14, color=GOLD_D, name="Why head")
            self.bullets_block(s, rx, BY + 2.85, rw, BB - qr - 0.25 - (BY + 2.85), why, pt=17,
                               pt_min=13.5)
        q = s.shapes.add_picture(qr_png(url), Inches(rx), Inches(BB - qr), Inches(qr), Inches(qr))
        _name(q, "QR code")
        q.click_action.hyperlink.address = url
        self.text(s, rx + qr + 0.2, BB - qr, rw - qr - 0.2, qr,
                  [P("মোবাইলে স্ক্যান করে দেখুন", b=True, c=NAVY), P("ক্লাসে: থাম্বনেইলে ক্লিক করুন")],
                  pt=14, pt_min=11.5, color=MUTED, anchor="m", sa_ratio=0.3, name="QR caption")
        return s

    def videos(self, n=2, brief_first=True):
        """Video cards for this chapter's entries in videos.json (first one goes in the brief deck)."""
        p = os.path.join(HERE, "videos.json")
        lst = json.load(open(p, encoding="utf-8")).get(str(self.ch), []) if os.path.exists(p) else []
        if not lst:
            warn(f"no videos for chapter {self.ch}")
        pick = lst[:n] + [v for v in lst[n:] if v.get("rapti")]
        for i, v in enumerate(pick):
            self.video(v["id"], brief=brief_first and i == 0)

    def quiz(self, questions, title="কুইজ: নিজেকে যাচাই করুন", notes=None, brief=False):
        """questions = [(q, [o1, o2, o3, o4], answer_index)] → question + answer slides."""
        if not self._keep(brief):
            return
        LET = ["ক", "খ", "গ", "ঘ"]
        OPT = 17
        def short(q):
            return all(text_w(o, OPT) < 2.3 for o in q[1])
        groups, cur = [], []
        for q in questions:
            cur.append(q)
            per = 3 if all(short(x) for x in cur) else 2
            if len(cur) > per:
                groups.append(cur[:-1]); cur = [q]
            elif len(cur) == per:
                groups.append(cur); cur = []
        if cur:
            groups.append(cur)
        qn_ = 0
        for g in groups:
            start = qn_
            for reveal in (False, True):
                s = self._light(title if not reveal else title.split(":")[0] + ": উত্তর",
                                notes=notes)
                per_row4 = all(short(x) for x in g)
                cols = 4 if per_row4 else 2
                ow = (BW - 0.7 - (cols - 1) * 0.2) / cols
                oh = 0.56
                blocks = []
                for (q, opts, ans) in g:
                    qh = min(1.0, block_height([P(q, b=True)], BW - 0.7, 20) + 0.08)
                    blocks.append(qh + 0.14 + (4 // cols) * oh + (4 // cols - 1) * 0.12)
                gap = 0.42
                total = sum(blocks) + gap * (len(g) - 1)
                y = BY + max(0, (BB - BY - total) / 2)
                for k, (q, opts, ans) in enumerate(g):
                    num = bn(start + k + 1)
                    qh = min(1.0, block_height([P(q, b=True)], BW - 0.7, 20) + 0.08)
                    self.badge(s, MX, y + (min(qh, 0.6) - 0.5) / 2, 0.5, num, fill=NAVY, color=WHITE, pt=17)
                    self.text(s, MX + 0.7, y, BW - 0.7, qh, [P(q, b=True)], pt=20,
                              pt_min=15, color=NAVY, anchor="m", name="Question")
                    oy = y + qh + 0.14
                    for j, o in enumerate(opts):
                        c, r = j % cols, j // cols
                        ox, oyy = MX + 0.7 + c * (ow + 0.2), oy + r * (oh + 0.12)
                        good = reveal and j == ans
                        self.card(s, ox, oyy, ow, oh, fill=GREEN if good else ICE, radius=0.14)
                        self.text(s, ox + 0.16, oyy, ow - 0.3, oh,
                                  [P(f"**{LET[j]})** {o}" + ("  ✓" if good else ""))],
                                  pt=OPT, pt_min=12, color=WHITE if good else INK,
                                  bold_color=WHITE if good else GOLD_D, anchor="m", name="Option")
                    y += blocks[k] + gap
            qn_ += len(g)
        return

    def glossary(self, rows, title="পারিভাষিক শব্দ", notes=None, brief=False):
        """rows = [("বাংলা", "English"), …] → two side-by-side two-column tables."""
        if not self._keep(brief):
            return
        s = self._light(title, notes=notes)
        half = math.ceil(len(rows) / 2)
        parts = [rows[:half], rows[half:]] if len(rows) > 6 else [rows]
        w = (BW - 0.4) / len(parts) if len(parts) == 2 else BW * 0.62
        n_max = max(len(p) for p in parts) + 1
        rh = min(0.6, (BB - BY) / n_max)
        size = 19 if rh >= 0.56 else 17 if rh >= 0.48 else 15
        total = rh * n_max
        top = BY + max(0, (BB - BY - total) / 2)
        for i, part in enumerate(parts):
            x = MX + i * (w + 0.4) if len(parts) == 2 else MX + (BW - w) / 2
            n = len(part) + 1
            gt = s.shapes.add_table(n, 2, Inches(x), Inches(top), Inches(w), Inches(rh * n))
            _name(gt, "Glossary")
            tbl = gt.table
            tblPr = tbl._tbl.tblPr
            sid = tblPr.find(qn("a:tableStyleId"))
            if sid is not None:
                sid.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"
            tbl.columns[0].width = Inches(w * 0.48); tbl.columns[1].width = Inches(w * 0.52)
            for ri, row in enumerate([("বাংলা পরিভাষা", "English")] + list(part)):
                tbl.rows[ri].height = Inches(rh)
                for ci in range(2):
                    cell = tbl.cell(ri, ci)
                    cell.margin_left = cell.margin_right = Inches(0.14)
                    cell.margin_top = cell.margin_bottom = Inches(0.03)
                    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                    fill = NAVY if ri == 0 else (ICE if ri % 2 == 0 else WHITE)
                    cell.fill.solid(); cell.fill.fore_color.rgb = _rgb(fill)
                    txt = row[ci]
                    sz = size
                    cwid = (w * (0.48 if ci == 0 else 0.52)) - 0.3
                    while sz > 12 and count_lines(txt, sz, cwid, ri == 0) > 1:
                        sz -= 0.5
                    write_paras(cell.text_frame, [P(txt, b=(ri == 0))], sz,
                                WHITE if ri == 0 else (INK if ci == 0 else NAVY2))
        return s

    def summary(self, items, title="মূল কথা", notes=None):
        """Key takeaways — dark slide (always in the brief deck)."""
        s = self._new(dark=True)
        self._tag(s, dark=True)
        self._title(s, title, color=WHITE)
        self._footer(s, dark=True)
        n = len(items)
        cols = 2 if n > 5 else 1
        rows_ = math.ceil(n / cols)
        gap = 0.18
        cw = (BW - (cols - 1) * 0.4) / cols
        rh = min(1.1, (BB - BY - (rows_ - 1) * gap) / rows_)
        tw = cw - 0.85
        pt = 20
        while pt > 13.5 and any(count_lines(t, pt, tw) * pt * LH * 0.92 / 72 > rh - 0.1 for t in items):
            pt -= 0.5
        total = rows_ * rh + (rows_ - 1) * gap
        top = BY + max(0, (BB - BY - total) / 2)
        for i, t in enumerate(items):
            c, r = (i // rows_, i % rows_) if cols == 2 else (0, i)
            x, y = MX + c * (cw + 0.4), top + r * (rh + gap)
            self.card(s, x, y, cw, rh, fill="15385F")
            d = 0.44
            self.icon_badge(s, x + 0.18, y + (rh - d) / 2, d, "check", fill=GOLD, color="navy")
            self.text(s, x + 0.8, y + 0.03, tw, rh - 0.06, [P(t)], pt=pt, pt_min=pt, color=NEARW,
                      anchor="m", fit=False, bold_color=GOLD_L)
        if notes:
            self._notes(s, notes)
        return s

    def closing(self, notes=None):
        if self.mode != "full":
            return
        s = self._new(dark=True, bg_variant="b")
        self._title(s, "প্রশ্ন ও আলোচনা", x=0.85, y=1.55, w=11, h=1.1, pt=46, color=WHITE, anchor="t")
        lines = [P(f"অধ্যায় {bn2(self.ch)}: {self.title}", c=GOLD_L, b=True)]
        if self.next_title:
            lines.append(P(f"পরের অধ্যায় {bn2(self.ch + 1)}: {self.next_title}", c=NEARW))
        self.text(s, 0.85, 2.85, 11, 1.2, lines, pt=22, pt_min=16, color=NEARW, sa_ratio=0.4)
        logo = s.shapes.add_picture(os.path.join(BOOK, "assets", "cover", "logo_rapti_light.png"),
                                    Inches(0.85), Inches(4.75), Inches(2.3))
        _name(logo, "RAPTI logo")
        self.text(s, 3.45, 4.7, 8.5, 1.0,
                  [P("Resonance Automation Professional Training Institute", b=True, c=WHITE),
                   P("rapti.net  ·  হটলাইন 01617-345534  ·  raptibd@gmail.com", c=PALE)],
                  pt=16, pt_min=12, sa_ratio=0.3, name="Contact")
        if notes:
            self._notes(s, notes)
        return s

    def _aspect(self, img):
        _, iw, ih, _ = prep_image(img)
        return iw / ih

    # ── save ───────────────────────────────────────────────────────────
    def save(self, path):
        cp = self.prs.core_properties
        cp.author = "RAPTI — Resonance Automation Professional Training Institute"
        cp.title = f"অধ্যায় {bn2(self.ch)} — {self.title}" if self.mode == "full" else \
            "ইলেকট্রিক্যাল হাউস ওয়্যারিং — সংক্ষিপ্ত স্লাইড"
        cp.subject = "ইলেকট্রিক্যাল হাউস ওয়্যারিং — প্রশিক্ষণ স্লাইড"
        cp.language = "bn-BD"
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self.prs.save(path)
        return path
