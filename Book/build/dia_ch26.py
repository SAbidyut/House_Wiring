# -*- coding: utf-8 -*-
"""অধ্যায় ২৬ — কন্ডুইট পাইপ ওয়্যারিং : ডায়াগ্রাম।

অধ্যায় ১৪ কন্ডুইট ওয়্যারিংয়ের **পরিচয়** দিয়েছে — কোন পদ্ধতি কী, সারফেস
আর কনসিল্ডের পার্থক্য কী।  এই অধ্যায় সেই কাজটিই **হাতে করে দেখায়**।
তাই ছবির ভাগটাও আলাদা:

**আঁকা চিত্র** — যেগুলো ক্যামেরায় ধরা যায় না:  দেয়াল ও ছাদের ভেতরের
কাটা-ছবি, পাইপের কাটা মুখ ও মাপ, বাঁকের ব্যাসার্ধ, খাঁজের নিয়ম, পুল
বাক্সের অবস্থান, লুপ-ইন ওয়্যারিং, জিআই পাইপের প্যাঁচ ও ধারাবাহিকতা,
কাজের ধাপ ও সাধারণ ভুল।

**আলোকচিত্র** — জিনিসগুলো আসলে কেমন দেখায়:  কমলা PVC পাইপের আঁটি,
জিআই পাইপের কাটা প্যাঁচ, স্যাডল ও ফিটিং, বেন্ডিং স্প্রিং, বেন্ডার,
ঢালাইয়ের আগে জালের উপরে বসানো পাইপ, দেয়ালে বসা বাক্স, সারফেস রান
(`assets_ch26.py`)।

অধ্যায় ১৫ থেকে চলে আসা ছবির নিয়ম এখানেও কড়া:  প্যানেলের শিরোনাম
বিশেষ্য, যন্ত্রাংশের লেবেল এক-দুই শব্দ, নিচে এক লাইনের একটি নোট-পটি।
কারণ, পরামর্শ আর সতর্কবাণী সবই বইয়ের লেখায় — ছবিতে নয়।

ছবির লেবেলে যা লেখা যাবে না:  কালপুরুষে `÷ √ ² Ω φ ≤` নেই বা ভুল আঁকে।
ভাগ সবসময় `/`, বর্গমিলিমিটার কথায় — "বর্গমিমি"।  মাপ, শ্রেণি ও
রেটিং ল্যাটিন অঙ্কে (অধ্যায় ২৩-এর নিয়ম — কালপুরুষে বাংলা ৪ ল্যাটিন
8-এর মতো আঁকে, আর পাইপের মাপের ঘরে সেটি অন্য পাইপ হয়ে যায়)।

আঁকার সংখ্যাগুলো মুখস্থ নয় — IS 9537 (Part 3) : 1983-এর সারণি ১ ও
বিএনবিসি পার্ট ৮ অধ্যায় ১ থেকে নেওয়া;  `ch26.py`-র docstring-এ
প্রতিটির সূত্র লেখা আছে।
"""
import math
import os

from bookkit import bn
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch26")
IMG = os.path.join(HERE, "assets", "ch26")

# টাইপের মাপ — W-px ক্যানভাস P সেমি চওড়ায় বসলে N-px লেখা
# N × P(pt) / W পয়েন্টে ছাপে।  ১৫.৪ সেমিতে (৪৩৬.৫ pt) ১২৪০-px
# ক্যানভাসে ২২ px = ৭.৭ pt — প্রকল্পের ~৭.৫ pt মেঝের উপরে।
T_TITLE = 34
T_NODE = 28
T_NAME = 25
T_BODY = 23
T_SMALL = 22
T_CALL = 24.5
T_TINY = 22

SW = 3.4
PLATE = "#F4F7FA"

# উপাদানের রং
PVC = "#E7EBEF"          # সাদাটে-ধূসর PVC পাইপ
PVCE = "#98A2AC"
PVCD = "#CBD3DA"
GI = "#C3CAD2"           # গ্যালভানাইজড ইস্পাত
GIE = "#6F7A85"
GIH = "#EAEEF2"
BORE = "#FBFCFD"
WALLF = "#EFE6D8"        # ইটের দেয়াল
WALLE = "#C9B99F"
BRICK = "#DCCDB4"
SLAB = "#DDE2E7"         # কংক্রিট
SLABE = "#A9B3BE"
PLAS = "#F6F1E7"         # প্লাস্টার
COPPER = "#B5713A"

# বিএনবিসি ১.৩.৯.৩.১৫ / সারণি ৮.১.২-এর রং
C_L1 = "#D42A1F"
C_N = "#1F2933"
C_PE = "#1B6E47"


# ══════════════════════════════════════════════════════════════════════
#  সাধারণ helpers (অধ্যায় ২২–২৫ থেকে চলে আসা)
# ══════════════════════════════════════════════════════════════════════
def panel(s, x, y, w, h, title, col=STEEL):
    """প্যানেলের শিরোনাম — কেবল নাম, কোনো মন্তব্য নয়।"""
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def note_strip(s, y, text, size=T_NAME, fill="#EAF2FA", stroke=STEEL,
               tcolor=NAVY, pad=46):
    """এক লাইনের তথ্য-পটি।  দুই লাইনে গড়ালে এখানেই থেমে যায়।"""
    w = s.w - 2 * pad
    if tw(text, size, 700) > w - 60:
        raise ValueError(f"note_strip এক লাইনে ধরে না: {text!r}")
    s.rect(pad, y, w, 58, fill, stroke, 2, 11)
    s.text(pad + w / 2, y + 36, text, size, tcolor, 700, "middle")
    return y + 58


def head_bar(s, x, y, w, h, text, col, size=T_NODE, rx=13):
    """রঙিন শিরোনাম-পটি, নিচের কোনা চৌকো।"""
    rx = min(rx, max(2, h / 2 - 0.46 * size))
    s.rect(x, y, w, h, col, col, 2.4, rx)
    s.rect(x, y + rx, w, h - rx, col, "none", 0, 0)
    s.text(x + w / 2, y + h / 2 + size * 0.34, text, size, "#FFFFFF", 700,
           "middle")


def callout(s, x, y, text, tx, ty, anchor="end", size=T_CALL, col=NAVY,
            elbow=False):
    """লেবেল ও লিডার — লেখার যে পাশে লক্ষ্য, সেই কিনারা থেকেই বেরোয়।"""
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    w = tw(text, size, 700)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle"
                                      else x - w)
    x1 = x0 + w
    start = x1 + 10 if tx > x1 else x0 - 10
    d = (f"M {start} {y} L {tx} {y} L {tx} {ty}" if elbow
         else f"M {start} {y} L {tx} {ty}")
    s.path(d, STEEL, 2.2)
    s.circle(tx, ty, 5, STEEL)


def blk(s, cx, cy, text, w=None, h=64, fill="#FFFFFF", stroke=STEEL,
        size=T_BODY, tcol=NAVY, sw=2.6, rx=10):
    w = w or tw(text, size, 700) + 46
    x, y = cx - w / 2, cy - h / 2
    s.rect(x, y, w, h, fill, stroke, sw, rx)
    s.text(cx, cy + size * 0.34, text, size, tcol, 700, "middle")
    return x, y, w, h


def chip(s, cx, cy, text, fill=LIGHT, stroke=STEEL, tcol=NAVY,
         size=T_SMALL):
    w = tw(text, size, 700) + 30
    s.rect(cx - w / 2, cy - 19, w, 38, fill, stroke, 2, 19)
    s.text(cx, cy + size * 0.34, text, size, tcol, 700, "middle")
    return w


def verdict(s, x, y, w, ok, text, size=T_SMALL, pad=54):
    """রায়ের পটি — বাঁয়ে চিহ্ন, ডানে মোড়ানো লেখা।"""
    col, bg = (GREEN, GREENBG) if ok else (RED, REDBG)
    lines = wrap(text, w - pad - 30, size, 700)
    h = max(62, 30 + len(lines) * (size + 8))
    s.rect(x, y, w, h, bg, col, 2.4, 12)
    s.text(x + 24, y + h / 2 + size * 0.36, "✔" if ok else "✗",
           size + 6, col, 700, "start")
    for j, ln in enumerate(lines):
        s.text(x + pad + (w - pad) / 2, y + h / 2 + size * 0.36
               + (j - (len(lines) - 1) / 2) * (size + 8), ln, size, col,
               700, "middle")
    return y + h


# ══════════════════════════════════════════════════════════════════════
#  আলোকচিত্রের শিট
# ══════════════════════════════════════════════════════════════════════
def _ih(img, w):
    from PIL import Image as _Im
    with _Im.open(f"{IMG}/{img}") as im:
        iw_, ih_ = im.size
    return round(w * ih_ / iw_)


def img_panel(s, x, y, w, h, title, img, col=STEEL):
    panel(s, x, y, w, h, title, col)
    s.image_fit(x + 16, y + 64, w - 32, h - 78, f"{IMG}/{img}", 6)


def sheet(fname, title, head, img, note, iw=1080, top=100, w=1240):
    """একটি ছবির শিট — শিরোনাম, প্যানেল, এক লাইনের নোট।"""
    ph = _ih(img, iw - 32) + 78
    x0 = (w - iw) / 2
    s = SVG(w, top + ph + 112)
    s.title(title, T_TITLE)
    img_panel(s, x0, top, iw, ph, head, img)
    y = note_strip(s, top + ph + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def pair_panels(fname, title, items, note, h=560, gap=24, top=100, w=1240):
    """সমান উচ্চতার কয়েকটি ছবি-প্যানেল, প্রস্থ ছবির অনুপাতে।"""
    from PIL import Image as _Im
    ws = []
    for _t, img, _c in items:
        with _Im.open(f"{IMG}/{img}") as im:
            ws.append(round(h * im.size[0] / im.size[1]) + 32)
    ph = h + 78
    span = sum(ws) + gap * (len(items) - 1)
    # অধ্যায় ১৯-এর শিক্ষা:  `qc.py` লেখা দেখে, বাক্স দেখে না।
    if span > w - 24:
        raise ValueError(f"{fname}: প্যানেলগুলো {span:.0f} px, "
                         f"ক্যানভাস {w} px — h কমাও")
    x0 = (w - span) / 2
    s = SVG(w, top + ph + 112)
    s.title(title, T_TITLE)
    x = x0
    for (head, img, col), pw in zip(items, ws):
        img_panel(s, x, top, pw, ph, head, img, col)
        x += pw + gap
    y = note_strip(s, top + ph + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def photo_callouts(fname, title, img, left, right, note,
                   iw=800, top=104, gap=34, size=T_CALL, w=1400):
    """একটি আলোকচিত্র মাঝখানে, দুই পাশে লেবেল ও লিডার।"""
    ih = _ih(img, iw)
    ix = (w - iw) / 2
    s = SVG(w, top + ih + 130)
    s.title(title, T_TITLE)

    def place(items, side):
        if not items:
            return
        minsep = size * 1.95
        items = [(it + (None,))[:4] for it in items]
        ys = [top + (lfy if lfy is not None else fy) * ih
              for (_t, _fx, fy, lfy) in items]
        for i in range(1, len(ys)):
            ys[i] = max(ys[i], ys[i - 1] + minsep)
        over = ys[-1] - (top + ih - 10)
        if over > 0:
            ys = [y - over for y in ys]
        under = (top + 10) - ys[0]
        if under > 0:
            ys = [y + under for y in ys]
        for (text, fx, fy, lfy), ly in zip(items, ys):
            tx, ty = ix + fx * iw, top + fy * ih
            anc = "end" if side == "left" else "start"
            lx = ix - gap if side == "left" else ix + iw + gap
            callout(s, lx, ly, text, tx, ty, anc, size,
                    elbow=(lfy is not None))

    s.image(ix, top, iw, ih, f"{IMG}/{img}")
    place(left, "left")
    place(right, "right")
    y = note_strip(s, top + ih + 30, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def strip_callouts(fname, title, img, above, below, note,
                   iw=1160, top=100, gap=30, size=T_CALL, w=1240):
    """চওড়া-অথচ-বেঁটে ছবির জন্য কল-আউট — লেবেল উপরে ও নিচে।

    প্রতিটি এন্ট্রি:  (লেখা, লেবেলের fx, লক্ষ্যের fx, লক্ষ্যের fy)।
    """
    ih = _ih(img, iw)
    ix = (w - iw) / 2
    lh = size * 1.5
    iy = top + lh + gap
    s = SVG(w, iy + ih + lh + gap + 120)
    s.title(title, T_TITLE)
    s.image(ix, iy, iw, ih, f"{IMG}/{img}")

    def run(items, up):
        for text, lfx, tfx, tfy in items:
            lx = ix + lfx * iw
            ly = (iy - gap + size * 0.32) if up else (iy + ih + gap + size)
            s.text(lx, ly, text, size, NAVY, 700, "middle")
            y0 = (iy - gap + 8) if up else (iy + ih + gap - 8)
            tx, ty = ix + tfx * iw, iy + tfy * ih
            d = f"M {lx} {y0} L {lx} {ty}"
            if abs(tx - lx) > 1:
                d += f" L {tx} {ty}"
            s.path(d, STEEL, 2.2)
            s.circle(tx, ty, 5, STEEL)

    run(above, True)
    run(below, False)
    y = note_strip(s, iy + ih + lh + gap + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


# ══════════════════════════════════════════════════════════════════════
#  অধ্যায় ২৬-এর নিজস্ব আঁকার উপাদান
# ══════════════════════════════════════════════════════════════════════
def pipe(s, d, od=34, col=PVC, edge=PVCE, hi="#FFFFFF", cap="round"):
    """একটি কন্ডুইটের রান — যেকোনো পথ ধরে, গোলত্ব সমেত।

    অধ্যায় ১১-এর `tube()`-এর নিয়ম:  SVG গ্রেডিয়েন্ট নয়, ক্রমশ সরু ও
    হালকা কয়েকটি স্ট্রোক — কারণ ছবিটা ওয়ার্ডে **SVG** হিসেবে যায়, আর
    ওয়ার্ড ও লিব্রেঅফিসের রেন্ডারার এক নয়।
    """
    s.path(d, edge, od, cap=cap)
    s.path(d, col, od - 5.0, cap=cap)
    s.add(f'<g transform="translate(0,{-od * 0.20:.1f})" opacity="0.62">')
    s.path(d, hi, od * 0.20, cap=cap)
    s.add("</g>")


def pipe_h(s, x0, x1, y, od=34, **kw):
    pipe(s, f"M {x0} {y} L {x1} {y}", od, **kw)


def pipe_v(s, x, y0, y1, od=34, **kw):
    pipe(s, f"M {x} {y0} L {x} {y1}", od, **kw)


def pipe_end(s, cx, cy, r, wall, col=PVC, edge=PVCE, bore=BORE):
    """পাইপের কাটা মুখ — বাইরের বৃত্ত, ভেতরের ফাঁপা।"""
    s.circle(cx, cy, r, col, edge, 2.4)
    s.circle(cx, cy, r - wall, bore, edge, 2.0)
    return r - wall


def core(s, cx, cy, r, col, label=None, size=T_TINY):
    """পাইপের ভেতরে একটি তারের কাটা মুখ।"""
    s.circle(cx, cy, r, col, "#4A5560", 1.3)
    s.circle(cx, cy, r * 0.42, "#C98B4B", "#8A5326", 1.0)
    if label:
        s.text(cx, cy + size * 0.34, label, size, "#FFFFFF", 700, "middle")


def brick_wall(s, x, y, w, h, fill=WALLF, edge=WALLE, course=34):
    """ইটের দেয়ালের কাটা-অংশ — গাঁথুনির রেখা সমেত।"""
    s.rect(x, y, w, h, fill, edge, 2.4, 3)
    s.clip_begin(x, y, w, h, 3)
    n = int(h // course)
    for i in range(1, n + 1):
        yy = y + i * course
        s.line(x, yy, x + w, yy, BRICK, 1.5)
        off = (course * 1.5) if i % 2 else 0
        k = 0
        while x + off + k * course * 2.2 < x + w:
            xx = x + off + k * course * 2.2
            s.line(xx, yy - course, xx, yy, BRICK, 1.5)
            k += 1
    s.clip_end()


def plaster(s, x, y, w, h):
    s.rect(x, y, w, h, PLAS, "#DCD2C0", 1.8, 2)


def concrete(s, x, y, w, h, fill=SLAB, edge=SLABE):
    """কংক্রিটের কাটা-অংশ — ছিটে-দাগ দিয়ে।"""
    s.rect(x, y, w, h, fill, edge, 2.4, 3)
    s.clip_begin(x, y, w, h, 3)
    seed = 7
    for i in range(int(w * h / 900)):
        seed = (seed * 1103515245 + 12345) % 2147483648
        px = x + (seed % 10000) / 10000 * w
        seed = (seed * 1103515245 + 12345) % 2147483648
        py = y + (seed % 10000) / 10000 * h
        seed = (seed * 1103515245 + 12345) % 2147483648
        rr = 1.4 + (seed % 100) / 100 * 2.2
        s.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rr:.1f}" '
              f'fill="#B9C2CB" opacity="0.55"/>')
    s.clip_end()


def rebar(s, x, y, w, h, pitch=44):
    """স্ল্যাবের রডের জাল — উপর থেকে দেখা।"""
    k = 0
    while x + k * pitch <= x + w:
        s.line(x + k * pitch, y, x + k * pitch, y + h, "#8A6A4A", 2.2)
        k += 1
    k = 0
    while y + k * pitch <= y + h:
        s.line(x, y + k * pitch, x + w, y + k * pitch, "#8A6A4A", 2.2)
        k += 1


def rnd_box(s, cx, cy, r, col="#F2F5F8", edge="#7C8794", lid=True):
    """গোল কন্ডুইট বাক্স (জংশন/সুইচ বাক্স) — সামনে থেকে।"""
    s.circle(cx, cy, r, col, edge, 2.6)
    if lid:
        s.circle(cx, cy, r * 0.72, "#FBFCFD", edge, 1.8)
        for a in (0, math.pi):
            s.circle(cx + r * 0.5 * math.cos(a), cy + r * 0.5 * math.sin(a),
                     r * 0.13, "#DFE5EB", edge, 1.4)


def sq_box(s, cx, cy, w, h, col="#EDF1F5", edge="#6C7885", knock=True):
    """চৌকো পুল/জংশন বাক্স — ঢাকনা ও নকআউট সমেত।"""
    s.rect(cx - w / 2, cy - h / 2, w, h, col, edge, 2.6, 5)
    s.rect(cx - w / 2 + 7, cy - h / 2 + 7, w - 14, h - 14, "#FBFCFD",
           edge, 1.6, 3)
    if knock:
        for dx, dy in ((-w / 2, 0), (w / 2, 0), (0, -h / 2), (0, h / 2)):
            s.circle(cx + dx * 0.98, cy + dy * 0.98, 6.5, "#DFE5EB",
                     edge, 1.3)


def saddle(s, cx, cy, od, col="#B9C1C9", edge="#7C8794"):
    """স্যাডল — পাইপকে দেয়ালে আঁটে।"""
    r = od / 2 + 5
    s.path(f"M {cx - r - 14} {cy + r} L {cx - r} {cy + r} "
           f"A {r} {r} 0 0 1 {cx + r} {cy + r} L {cx + r + 14} {cy + r}",
           edge, 7)
    s.path(f"M {cx - r - 14} {cy + r} L {cx - r} {cy + r} "
           f"A {r} {r} 0 0 1 {cx + r} {cy + r} L {cx + r + 14} {cy + r}",
           col, 4)
    for dx in (-r - 8, r + 8):
        s.circle(cx + dx, cy + r, 3.4, "#6C7885")


def thread(s, x0, x1, y, od, n=9, col=GIE):
    """পাইপের মুখে কাটা প্যাঁচ — করাতের দাঁতের মতো ছোট রেখা।"""
    for i in range(n):
        xx = x0 + (x1 - x0) * (i + 0.5) / n
        s.line(xx, y - od / 2 + 1, xx + (x1 - x0) / n * 0.55,
               y + od / 2 - 1, col, 1.7)


def arrowhead(s, x, y, ang, size=13, col=STEEL):
    a = math.radians(ang)
    p = [(x, y),
         (x - size * math.cos(a - 0.42), y - size * math.sin(a - 0.42)),
         (x - size * math.cos(a + 0.42), y - size * math.sin(a + 0.42))]
    s.poly(p, col, col, 1)


def dim_h(s, x0, x1, y, text, col=NAVY, size=T_SMALL, tick=9):
    """আড়াআড়ি মাপের রেখা — দুই প্রান্তে দাগ, মাঝখানে লেখা।"""
    # লেখার জায়গাটি ফাঁকা রেখে দুই টুকরোয় আঁকা — নইলে `qc.py` ঠিকই
    # ধরে যে রেখাটি নিজের লেখার উপর দিয়ে গেছে
    w = tw(text, size, 700)
    mid = (x0 + x1) / 2
    if x1 - x0 > w + 26:                       # লেখা দুই দাগের মাঝে ধরে
        s.line(x0, y, mid - w / 2 - 10, y, col, 1.9)
        s.line(mid + w / 2 + 10, y, x1, y, col, 1.9)
        ty = y + size * 0.34
    else:                                      # ধরে না — রেখার উপরে
        s.line(x0, y, x1, y, col, 1.9)
        ty = y - size * 0.90
    for xx in (x0, x1):
        s.line(xx, y - tick, xx, y + tick, col, 1.9)
    s.text(mid, ty, text, size, col, 700, "middle")


def dim_v(s, x, y0, y1, text, col=NAVY, size=T_SMALL, tick=9, side="right"):
    s.line(x, y0, x, y1, col, 1.9)
    for yy in (y0, y1):
        s.line(x - tick, yy, x + tick, yy, col, 1.9)
    xx = x + 14 if side == "right" else x - 14
    s.text(xx, (y0 + y1) / 2 + size * 0.34, text, size, col, 700,
           "start" if side == "right" else "end")


# ══════════════════════════════════════════════════════════════════════
#  ১।  কন্ডুইট ওয়্যারিং — গোটা ছবিটা
# ══════════════════════════════════════════════════════════════════════
def d01_house():
    """একটি ঘরের কাটা-ছবি — ছাদের ভেতরে পাইপ, দেয়ালের ভেতরে ড্রপ।

    লেবেলগুলো ঘরের **ভেতরের ফাঁকা জায়গায়** — কাটা-ছবিতে ওখানেই
    জায়গা আছে, আর ক্যানভাসের বাইরে যাওয়ার ভয় থাকে না।
    """
    s = SVG(1240, 890)
    s.title("একটি ঘরে কন্ডুইট ওয়্যারিং — কাটা-ছবি", T_TITLE)

    wt = 76                                   # দেয়ালের পুরুত্ব
    st = 62                                   # ছাদের পুরুত্ব
    L, R = 132, 1108                          # ভবনের বাইরের কিনারা
    top, floor = 128, 706
    iL, iR = L + wt, R - wt                   # ঘরের ভেতরের কিনারা

    concrete(s, L, top, R - L, st)                     # ছাদ
    brick_wall(s, L, top + st, wt, floor - top - st)   # বাঁ দেয়াল
    brick_wall(s, iR, top + st, wt, floor - top - st)  # ডান দেয়াল
    concrete(s, L - 34, floor, R - L + 68, 32)         # মেঝে

    # ── ছাদের ভেতরের কন্ডুইট — পুরুত্বের ঠিক মাঝখানে ──
    my = top + st / 2
    s.line(L, my, R, my, "#7B8794", 1.4, dash="11 8")
    pipe_h(s, L + 14, R - 14, my, 26)

    # সিলিং রোজের বাক্স ও ঝুলন্ত বাতি
    cx = 624
    pipe_v(s, cx, my, top + st + 8, 26)
    rnd_box(s, cx, my + 2, 26, "#EDF1F5", "#6C7885", False)
    s.line(cx, top + st + 8, cx, top + st + 84, "#5A6572", 2.6)
    s.circle(cx, top + st + 114, 29, "#FFF3CE", AMBER, 2.6)
    for k in range(8):
        a_ = math.radians(30 + k * 40)
        s.line(cx + 38 * math.cos(a_), top + st + 114 + 38 * math.sin(a_),
               cx + 50 * math.cos(a_), top + st + 114 + 50 * math.sin(a_),
               AMBER, 2.4)

    # ── বাঁ দেয়ালের ভেতরে ড্রপ:  পুল বাক্স → এসডিবি → সুইচ বোর্ড ──
    # পাইপের পেছনে খাঁজের পটি — নইলে পাইপটা দেয়ালের *গায়ে* আছে বলে
    # মনে হয়, ভেতরে নয়
    lx = L + wt / 2
    s.rect(lx - 21, top + st, 42, floor - 176 + 46 + 21 - top - st,
           "#E3D8C2", "#C9B99F", 1.6, 2)
    pb_y = top + st + 78
    sq_box(s, lx, pb_y, 74, 62)
    pipe_v(s, lx, my, pb_y - 31, 26)
    pipe_v(s, lx, pb_y + 31, floor - 296, 26)
    # এসডিবি — ভেতরের দেয়ালে
    ex, ey = iL, floor - 350
    s.rect(ex, ey, 138, 116, "#F2F5F8", "#6C7885", 2.6, 6)
    for r in range(2):
        for i in range(5):
            s.rect(ex + 16 + i * 22, ey + 18 + r * 46, 15, 34,
                   "#FBFCFD", "#8E99A6", 1.4, 2)
    pipe_h(s, lx, ex + 6, floor - 296, 26)
    # সুইচ বোর্ড — একই দেয়ালে, নিচে
    sbx, sby = iL + 8, floor - 176
    s.rect(sbx, sby, 118, 92, "#F2F5F8", "#6C7885", 2.6, 6)
    for i in range(3):
        s.rect(sbx + 14 + i * 32, sby + 22, 23, 46, "#FBFCFD",
               "#8E99A6", 1.6, 3)
    pipe_v(s, lx, floor - 296, sby + 46, 26)
    pipe_h(s, lx, sbx + 4, sby + 46, 26)

    # ── ডান দেয়ালের ভেতরে ড্রপ:  সকেট ──
    rx = iR + wt / 2
    s.rect(rx - 21, top + st, 42, floor - 216 + 33 + 21 - top - st,
           "#E3D8C2", "#C9B99F", 1.6, 2)
    pipe_v(s, rx, my, floor - 186, 26)
    skx, sky = iR - 4, floor - 216
    s.rect(skx - 74, sky, 78, 66, "#F2F5F8", "#6C7885", 2.6, 5)
    for dx_, dy_ in ((-26, 14), (-14, 40), (-38, 40)):
        s.circle(skx - 74 + 39 + dx_ + 26, sky + dy_, 5.5, "#3D4650")
    pipe_h(s, rx, skx, sky + 33, 26)

    # ── লেবেল:  সব ঘরের ভেতরের সাদা জায়গায় ──
    callout(s, 330, my + 70, "স্ল্যাবে কন্ডুইট", 460, my + 13, "start",
            T_SMALL)
    callout(s, 830, my + 96, "সিলিং রোজ", cx + 26, my + 2, "end", T_SMALL)
    callout(s, 300, pb_y + 34, "পুল বাক্স", lx + 37, pb_y, "start", T_SMALL)
    callout(s, 386, ey + 54, "এসডিবি", ex + 138, ey + 54, "start", T_SMALL)
    callout(s, 366, sby + 46, "সুইচ বোর্ড", sbx + 118, sby + 46, "start",
            T_SMALL)
    callout(s, 900, sky + 33, "সকেট", skx - 74, sky + 33, "end", T_SMALL)
    callout(s, 900, floor - 396, "দেয়ালের ভেতরে ড্রপ", rx - 13,
            floor - 396, "end", T_SMALL)

    y = note_strip(s, 790, "ছাদের পাইপ থেকে নেমে বাক্স — জোড়া কেবল "
                           "বাক্সের ভেতরে, পাইপের ভেতরে নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_house.svg")


# ══════════════════════════════════════════════════════════════════════
#  ২।  সারফেস বনাম কনসিল্ড
# ══════════════════════════════════════════════════════════════════════
def d02_two():
    """দুই পদ্ধতির দেয়াল-কাটা ছবি, পাশাপাশি।"""
    s = SVG(1240, 720)
    s.title("সারফেস ও কনসিল্ড কন্ডুইট — দেয়ালের কাটা-ছবি", T_TITLE)

    PW, PH = 578, 452
    top = 106
    for i, (x, head, col) in enumerate(
            [(30, "সারফেস কন্ডুইট", STEEL),
             (632, "কনসিল্ড কন্ডুইট", NAVY)]):
        panel(s, x, top, PW, PH, head, col)

    # ── বাঁ প্যানেল:  সারফেস ──
    # দেয়াল সরু, বাঁয়ে লেবেলের নিজস্ব কলাম — নইলে গাঁথুনির রেখা
    # লেখার উপর দিয়ে যায় আর `qc.py` ঠিকই ধরে
    x0 = 30
    wx, wy, ww, wh = x0 + 196, top + 88, 316, 300
    brick_wall(s, wx, wy, ww, wh)
    plaster(s, wx + ww - 26, wy, 26, wh)          # প্লাস্টারের পাতলা স্তর
    px = wx + ww + 22                              # পাইপ দেয়ালের বাইরে
    pipe_v(s, px, wy + 26, wy + wh - 26, 30)
    for yy in (wy + 74, wy + 198):
        saddle(s, px, yy, 30)
    lc = x0 + 176
    callout(s, lc, wy + 40, "দেয়াল", wx + 40, wy + 40, "end", T_SMALL)
    callout(s, lc, wy + 150, "পাইপ বাইরে", px - 16, wy + 150, "end",
            T_SMALL)
    callout(s, lc, wy + 250, "স্যাডল", px - 20, wy + 218, "end", T_SMALL)
    s.text(x0 + PW / 2, top + PH - 22, "মেরামত সহজ · দেখা যায়",
           T_SMALL, GREY, 700, "middle")

    # ── ডান প্যানেল:  কনসিল্ড ──
    x0 = 632
    wx, wy, ww, wh = x0 + 196, top + 88, 316, 300
    brick_wall(s, wx, wy, ww, wh)
    # খাঁজ কেটে পাইপ ভেতরে, তারপর প্লাস্টার
    cxp = wx + ww - 68
    s.rect(cxp - 26, wy + 20, 52, wh - 40, "#E3D8C2", "#C9B99F", 1.8, 3)
    pipe_v(s, cxp, wy + 26, wy + wh - 26, 30)
    plaster(s, wx + ww - 26, wy, 26, wh)
    lc = x0 + 176
    callout(s, lc, wy + 40, "খাঁজ", cxp - 26, wy + 40, "end", T_SMALL)
    callout(s, lc, wy + 150, "পাইপ ভেতরে", cxp - 15, wy + 150, "end",
            T_SMALL)
    callout(s, lc, wy + 254, "প্লাস্টার", wx + ww - 13, wy + 254, "end",
            T_SMALL)
    s.text(x0 + PW / 2, top + PH - 22, "দেখা যায় না · প্লাস্টারের নিচে",
           T_SMALL, GREY, 700, "middle")

    y = note_strip(s, top + PH + 30,
                   "দুটিতেই পাইপ একই — বদলায় কেবল পাইপটি দেয়ালের "
                   "কোন পাশে থাকে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_two.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৩।  পাইপের কাটা মুখ ও মাপ
# ══════════════════════════════════════════════════════════════════════
def d03_anatomy():
    """PVC ও জিআই পাইপ — বাইরের ব্যাস, ভেতরের ব্যাস, দেয়ালের পুরুত্ব।"""
    s = SVG(1240, 690)
    s.title("পাইপের মাপ — বাইরে, ভেতরে ও দেয়াল", T_TITLE)

    PW, PH = 578, 438
    top = 106
    panel(s, 30, top, PW, PH, "PVC কন্ডুইট", STEEL)
    panel(s, 632, top, PW, PH, "জিআই কন্ডুইট", NAVY)

    def one(x0, col, edge, od_r, wall, od_t, id_t, wl_t, bore=BORE):
        """বাঁয়ে পাইপের এক টুকরো, ডানে সেটিরই কাটা মুখ বড় করে।"""
        cy = top + 214
        # পাইপের টুকরো — দুই মুখই কাটা, তাই butt cap
        bx0, bx1 = x0 + 52, x0 + 244
        pipe(s, f"M {bx0} {cy} L {bx1} {cy}", od_r * 0.86, col, edge,
             cap="butt")
        s.ellipse(bx1, cy, 11, od_r * 0.43, col, edge, 2.2)
        s.ellipse(bx1, cy, 11 * (1 - 2 * wall / (od_r * 0.86)),
                  od_r * 0.43 - wall * 0.43, bore, edge, 1.8)
        # কাটা মুখ, বড় করে
        cx = x0 + 400
        pipe_end(s, cx, cy, od_r, wall, col, edge, bore)
        s.line(bx1 + 12, cy - od_r * 0.43, cx - od_r, cy - od_r,
               STEEL, 1.6, dash="7 6")
        s.line(bx1 + 12, cy + od_r * 0.43, cx - od_r, cy + od_r,
               STEEL, 1.6, dash="7 6")
        # মাপ
        dim_h(s, cx - od_r, cx + od_r, cy + od_r + 54, od_t)
        dim_h(s, cx - od_r + wall, cx + od_r - wall, cy - od_r - 48, id_t)
        s.line(cx - od_r, cy, cx - od_r + wall, cy, RED, 3.4)
        callout(s, x0 + 46, cy + 128, wl_t, cx - od_r + wall / 2, cy,
                "start", T_SMALL, RED)

    one(30, PVC, PVCE, 74, 14, "OD 20 mm", "ID 15.8 mm", "দেয়াল 2.1 mm")
    one(632, GI, GIE, 74, 9, "OD 20 mm", "ID 16.7 mm", "দেয়াল 1.63 mm",
        bore="#F0F3F6")

    y = note_strip(s, top + PH + 30,
                   "মাপ বলতে বাইরের ব্যাস — 20 mm পাইপের ভেতরটি কখনোই "
                   "20 mm নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_anatomy.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৪।  মালামাল
# ══════════════════════════════════════════════════════════════════════
def d04_parts():
    """কন্ডুইট ওয়্যারিংয়ের ফিটিং — আঁকা, নাম সমেত।"""
    s = SVG(1240, 760)
    s.title("কন্ডুইটের সঙ্গে যা যা লাগে", T_TITLE)

    CW, CH = 288, 232
    gap = 18
    x0 = (1240 - 4 * CW - 3 * gap) / 2
    top = 104

    def cell(i, name):
        cx = x0 + (i % 4) * (CW + gap)
        cy = top + (i // 4) * (CH + gap)
        s.rect(cx, cy, CW, CH, PLATE, LINE, 1.8, 10)
        s.text(cx + CW / 2, cy + CH - 18, name, T_SMALL, NAVY, 700,
               "middle")
        return cx + CW / 2, cy + (CH - 34) / 2 + 8

    # ১ — সোজা পাইপ
    cx, cy = cell(0, "কন্ডুইট পাইপ")
    pipe_h(s, cx - 108, cx + 108, cy, 34)

    # ২ — বেন্ড
    cx, cy = cell(1, "বেন্ড (90°)")
    pipe(s, f"M {cx - 96} {cy + 52} L {cx - 30} {cy + 52} "
            f"Q {cx + 44} {cy + 52} {cx + 44} {cy - 22} L {cx + 44} {cy - 56}",
         34)

    # ৩ — কাপলার / সকেট
    cx, cy = cell(2, "কাপলার")
    pipe_h(s, cx - 108, cx - 6, cy, 34)
    pipe_h(s, cx + 6, cx + 108, cy, 34)
    s.rect(cx - 40, cy - 26, 80, 52, PVCD, PVCE, 2.4, 6)

    # ৪ — গোল বাক্স
    cx, cy = cell(3, "গোল বাক্স")
    pipe_h(s, cx - 108, cx - 40, cy, 30)
    pipe_v(s, cx, cy + 40, cy + 74, 30)
    rnd_box(s, cx, cy, 46)

    # ৫ — পুল বাক্স
    cx, cy = cell(4, "পুল বাক্স")
    pipe_h(s, cx - 108, cx - 46, cy, 30)
    pipe_h(s, cx + 46, cx + 108, cy, 30)
    sq_box(s, cx, cy, 92, 78)

    # ৬ — স্যাডল
    cx, cy = cell(5, "স্যাডল")
    s.rect(cx - 110, cy + 22, 220, 22, "#E7E1D4", "#C9B99F", 1.8, 3)
    pipe_h(s, cx - 96, cx + 96, cy, 34)
    saddle(s, cx, cy, 34)

    # ৭ — চেক নাট ও বুশ
    cx, cy = cell(6, "চেক নাট ও বুশ")
    pipe_h(s, cx - 108, cx + 26, cy, 34, col=GI, edge=GIE)
    s.rect(cx + 4, cy - 30, 18, 60, "#AEB6BE", GIE, 2.2, 3)
    s.rect(cx + 28, cy - 30, 18, 60, "#AEB6BE", GIE, 2.2, 3)
    s.path(f"M {cx + 46} {cy - 22} Q {cx + 74} {cy} {cx + 46} {cy + 22}",
           GIE, 3, "#C6CDD4")

    # ৮ — পুল-ওয়্যার
    cx, cy = cell(7, "GI পুল-ওয়্যার")
    pipe_h(s, cx - 108, cx + 62, cy, 34)
    s.path(f"M {cx - 100} {cy} L {cx + 84} {cy} "
           f"q 18 0 18 -16 q 0 -16 -18 -16", "#9AA3AC", 3.4)

    y = note_strip(s, top + 2 * (CH + gap) + 16,
                   "পাইপ এক জিনিস, ফিটিং আরেক — মাপ ও শ্রেণি দুটিরই "
                   "মিলতে হবে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_parts.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৫।  এক পাইপে কয়টি তার
# ══════════════════════════════════════════════════════════════════════
def d05_fill():
    """একই 20 mm পাইপে ৩, ৬ ও ৯টি 2.5 বর্গমিমি তার।"""
    s = SVG(1240, 700)
    s.title("এক পাইপে কয়টি তার — 20 mm হেভি গেজ", T_TITLE)

    PW, PH = 386, 448
    top = 104
    gap = 20
    x0 = (1240 - 3 * PW - 2 * gap) / 2

    # IS 9537 (Part 3) — 20 mm হেভি:  ID 15.8 mm → ক্ষেত্রফল 196 বর্গমিমি
    # IEC 60227-3 — 2.5 বর্গমিমি খেই-তারের বাইরের ব্যাস 3.72 mm
    #             → প্রতি তারে 10.9 বর্গমিমি
    # ব্যাসার্ধটি আগে 118 ছিল;  তাতে পাইপের বাইরের বৃত্ত নিচের
    # "…% ভরাট" লেখার ভেতর দিয়ে যেত
    R = 100                                     # ছবিতে ভেতরের ব্যাসার্ধ
    scale = R / (15.8 / 2)
    cr = 3.72 / 2 * scale
    cols = [C_L1, C_N, C_PE]

    # π/4 × 3.72² = 10.87 বর্গমিমি প্রতি তার;  পাইপের ভেতরের
    # ক্ষেত্রফল π/4 × 15.8² = 196 বর্গমিমি
    data = [(3, "৩টি তার", "১৭%", True),
            (6, "৬টি তার", "৩৩%", True),
            (9, "৯টি তার", "৫০%", False)]
    for i, (n, head, pct, ok) in enumerate(data):
        px = x0 + i * (PW + gap)
        panel(s, px, top, PW, PH, head, STEEL if ok else RED)
        cx, cy = px + PW / 2, top + 194
        pipe_end(s, cx, cy, R + 24, 24)
        # তারগুলো — কেন্দ্র ও বলয়ে সাজানো
        pts = []
        if n <= 3:
            for k in range(n):
                a = math.radians(-90 + k * 120)
                pts.append((cx + cr * 1.16 * math.cos(a),
                            cy + cr * 1.16 * math.sin(a)))
        else:
            inner = 1 if n % 6 else 0
            ring = n - inner
            if inner:
                pts.append((cx, cy))
            rr = cr / math.sin(math.pi / ring) if ring > 2 else cr * 1.16
            rr = min(rr, R - cr - 3)
            for k in range(ring):
                a = 2 * math.pi * k / ring - math.pi / 2
                pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        for k, (qx, qy) in enumerate(pts):
            core(s, qx, qy, cr, cols[k % 3])
        s.text(cx, top + PH - 96, pct + " ভরাট", T_NODE,
               GREEN if ok else RED, 700, "middle")
        s.text(cx, top + PH - 56, "সীমা ৩৫%", T_SMALL, GREY, 700, "middle")
        s.text(cx, top + PH - 22, "✔ চলবে" if ok else "✗ চলবে না",
               T_BODY, GREEN if ok else RED, 700, "middle")

    y = note_strip(s, top + PH + 30,
                   "ভেতরের ফাঁকা জায়গার ৩৫ ভাগের বেশি তারে ভরলে টান "
                   "দিলেই ইনসুলেশন ছেঁচে যায়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_fill.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৬।  বাঁকের ব্যাসার্ধ
# ══════════════════════════════════════════════════════════════════════
def d06_bend():
    """ঠিক বাঁক বনাম চ্যাপ্টা বাঁক — কাটা মুখ সমেত।"""
    s = SVG(1240, 760)
    s.title("বাঁকের ব্যাসার্ধ — ঠিক ও ভুল", T_TITLE)

    PW, PH = 578, 486
    top = 104
    panel(s, 30, top, PW, PH, "বড় ব্যাসার্ধের বাঁক", GREEN)
    panel(s, 632, top, PW, PH, "চ্যাপ্টা বাঁক", RED)

    # ── ঠিক ──
    x0 = 30
    cx, cy = x0 + 250, top + 262
    Rb = 150
    pipe(s, f"M {cx - 210} {cy + Rb} L {cx - Rb} {cy + Rb} "
            f"A {Rb} {Rb} 0 0 1 {cx} {cy} L {cx} {cy - 128}", 36)
    s.path(f"M {cx - Rb} {cy + Rb} L {cx - Rb} {cy} L {cx} {cy}",
           STEEL, 2, dash="8 6")
    dim_h(s, cx - Rb, cx, cy - 26, "R = 3 × OD")
    # কাটা মুখ — গোল থেকে গেছে
    ex, ey = x0 + 462, top + 132
    pipe_end(s, ex, ey, 46, 9, PVC, PVCE)
    s.text(ex, ey + 76, "মুখ গোল", T_SMALL, GREEN, 700, "middle")

    # ── ভুল ──
    x0 = 632
    cx, cy = x0 + 250, top + 262
    Rb = 46
    pipe(s, f"M {cx - 210} {cy + Rb} L {cx - Rb} {cy + Rb} "
            f"A {Rb} {Rb} 0 0 1 {cx} {cy} L {cx} {cy - 128}", 36)
    dim_h(s, cx - Rb, cx, cy + Rb + 84, "R ছোট", RED)
    # চ্যাপ্টা, ফাটা মুখ
    ex, ey = x0 + 462, top + 132
    s.ellipse(ex, ey, 56, 30, PVC, PVCE, 2.4)
    s.ellipse(ex, ey, 46, 20, BORE, PVCE, 2.0)
    s.path(f"M {ex + 40} {ey - 22} l 14 -14 l -6 14 l 12 4",
           RED, 3.2)
    s.text(ex, ey + 66, "মুখ চ্যাপ্টা", T_SMALL, RED, 700, "middle")
    s.text(x0 + 250, top + PH - 30, "তার আটকে যায় · ইনসুলেশন ছেঁড়ে",
           T_SMALL, RED, 700, "middle")

    y = note_strip(s, top + PH + 30,
                   "IS 9537-এর বাঁক-পরীক্ষার ফরমাই 3 × OD — 20 mm "
                   "পাইপে ব্যাসার্ধ 60 mm")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_bend.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৭।  PVC পাইপ বাঁকানো
# ══════════════════════════════════════════════════════════════════════
def d07_bendwork():
    """স্প্রিং ঢুকিয়ে গরম করে বাঁকানো — চার ধাপ।"""
    s = SVG(1240, 620)
    s.title("PVC পাইপ বাঁকানো — চার ধাপ", T_TITLE)

    CW, CH = 288, 300
    gap = 18
    x0 = (1240 - 4 * CW - 3 * gap) / 2
    top = 104

    def cell(i, name, sub):
        cx = x0 + i * (CW + gap)
        s.rect(cx, top, CW, CH, PLATE, LINE, 1.8, 10)
        s.badge(cx + 28, top + 28, bn(i + 1), 19)
        s.text(cx + CW / 2, top + CH - 44, name, T_BODY, NAVY, 700,
               "middle")
        s.text(cx + CW / 2, top + CH - 16, sub, T_SMALL, GREY, 700,
               "middle")
        return cx + CW / 2, top + 142

    # ১ — স্প্রিং ঢোকানো
    cx, cy = cell(0, "স্প্রিং ঢোকানো", "ID-র চেয়ে 1 mm ছোট")
    pipe_h(s, cx - 108, cx + 108, cy, 38)
    for k in range(13):
        xx = cx - 92 + k * 15
        s.path(f"M {xx} {cy + 11} Q {xx + 7} {cy} {xx + 15} {cy - 11}",
               "#7C8794", 2.6)
    arrowhead(s, cx + 108, cy, 0, 12, STEEL)

    # ২ — গরম করা
    cx, cy = cell(1, "সমানভাবে গরম", "খোলা আগুনে নয়")
    pipe_h(s, cx - 108, cx + 108, cy - 26, 38)
    for k in range(5):
        xx = cx - 72 + k * 36
        s.path(f"M {xx} {cy + 46} q -10 -16 0 -28 q 10 -12 0 -26",
               AMBER, 3.2)
    s.text(cx, cy + 78, "গরম বাতাস", T_TINY, AMBER, 700, "middle")

    # ৩ — ছাঁচে বাঁকানো
    cx, cy = cell(2, "ছাঁচে বাঁকানো", "একটানে, ধীরে")
    Rb = 74
    pipe(s, f"M {cx - 104} {cy + Rb - 20} L {cx - Rb} {cy + Rb - 20} "
            f"A {Rb} {Rb} 0 0 1 {cx} {cy - 20} L {cx} {cy - 86}", 34)
    s.circle(cx - Rb, cy + Rb - 20, Rb - 26, "none", STEEL, 2.4)

    # ৪ — ঠান্ডা করে স্প্রিং বার
    cx, cy = cell(3, "ঠান্ডা, স্প্রিং বার", "মুখ গোল আছে কি না দেখা")
    Rb = 74
    pipe(s, f"M {cx - 104} {cy + Rb - 20} L {cx - Rb} {cy + Rb - 20} "
            f"A {Rb} {Rb} 0 0 1 {cx} {cy - 20} L {cx} {cy - 86}", 34)
    s.path(f"M {cx - 104} {cy + Rb - 20} l -34 0", "#7C8794", 3.4)
    s.circle(cx - 146, cy + Rb - 20, 9, "none", "#7C8794", 3.2)

    y = note_strip(s, top + CH + 30,
                   "স্প্রিং ছাড়া বাঁকালে ভেতরটি বসে যায়, আর সোজা হয় না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_bendwork.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৮।  দেয়ালের খাঁজ
# ══════════════════════════════════════════════════════════════════════
def d08_chase():
    """খাঁজ কেবল খাড়া ও আড়াআড়ি — কোনাকুনি নয়।"""
    s = SVG(1240, 700)
    s.title("দেয়ালের খাঁজ কাটার নিয়ম", T_TITLE)

    PW, PH = 578, 430
    top = 104
    panel(s, 30, top, PW, PH, "খাড়া ও আড়াআড়ি", GREEN)
    panel(s, 632, top, PW, PH, "কোনাকুনি", RED)

    for x0, ok in ((30, True), (632, False)):
        wx, wy, ww, wh = x0 + 46, top + 78, 486, 292
        brick_wall(s, wx, wy, ww, wh)
        # বোর্ড ও বাক্স
        sq_box(s, wx + 96, wy + 214, 72, 60)
        rnd_box(s, wx + 386, wy + 58, 28, "#EDF1F5", "#6C7885", False)
        if ok:
            s.rect(wx + 84, wy + 40, 24, 154, "#E3D8C2", "#C9B99F", 1.8, 3)
            s.rect(wx + 84, wy + 40, 302, 24, "#E3D8C2", "#C9B99F", 1.8, 3)
            pipe_v(s, wx + 96, wy + 52, wy + 190, 20)
            pipe_h(s, wx + 96, wy + 374, wy + 52, 20)
            pipe_v(s, wx + 386, wy + 52, wy + 58, 20)
        else:
            s.path(f"M {wx + 96} {wy + 190} L {wx + 386} {wy + 58}",
                   "#C9B99F", 30)
            pipe(s, f"M {wx + 96} {wy + 190} L {wx + 386} {wy + 58}", 20)
            s.text(x0 + PW / 2, top + PH - 26,
                   "পরে পেরেক ঠুকলে কোথায় পাইপ কেউ জানে না",
                   T_SMALL, RED, 700, "middle")

    y = note_strip(s, top + PH + 30,
                   "বিএনবিসি ১.৩.১১.২ — দেয়ালে কন্ডুইট কেবল খাড়া বা "
                   "আড়াআড়ি, কোনাকুনি নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d08_chase.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৯।  ছাদের ঢালাইয়ে কন্ডুইট
# ══════════════════════════════════════════════════════════════════════
def d09_slab():
    """স্ল্যাবের পুরুত্বের মাঝখানে, চেয়ারের উপরে।"""
    s = SVG(1240, 700)
    s.title("ঢালাইয়ের আগে ছাদে কন্ডুইট", T_TITLE)

    PW, PH = 578, 430
    top = 104
    panel(s, 30, top, PW, PH, "কাটা-ছবি", NAVY)
    panel(s, 632, top, PW, PH, "উপর থেকে", STEEL)

    # ── বাঁ:  স্ল্যাবের কাটা অংশ ──
    x0 = 30
    sx, sy, sw_, sh = x0 + 48, top + 122, 482, 128
    concrete(s, sx, sy, sw_, sh)
    mid = sy + sh / 2
    s.line(sx, mid, sx + sw_, mid, "#7B8794", 1.6, dash="10 8")
    pipe_h(s, sx + 16, sx + sw_ - 16, mid, 30)
    # রড ও চেয়ার
    for yy in (sy + 22, sy + sh - 22):
        s.line(sx + 10, yy, sx + sw_ - 10, yy, "#8A6A4A", 3.0)
    for cxx in (sx + 110, sx + 250, sx + 390):
        s.path(f"M {cxx - 26} {sy + sh - 22} L {cxx - 26} {mid + 16} "
               f"L {cxx + 26} {mid + 16} L {cxx + 26} {sy + sh - 22}",
               "#8A6A4A", 3.0)
    callout(s, sx + 24, sy - 46, "পুরুত্বের মাঝখানে", sx + 220, mid,
            "start", T_SMALL)
    callout(s, sx + 24, sy + sh + 62, "চেয়ার", sx + 250, mid + 16,
            "start", T_SMALL)
    callout(s, sx + sw_ - 24, sy + sh + 62, "রডের জাল", sx + sw_ - 90,
            sy + sh - 22, "end", T_SMALL)

    # ── ডান:  উপর থেকে ──
    x0 = 632
    gx, gy, gw, gh = x0 + 48, top + 74, 482, 288
    s.rect(gx, gy, gw, gh, "#F3EFE6", "#C9B99F", 2.2, 4)
    s.clip_begin(gx, gy, gw, gh, 4)
    rebar(s, gx, gy, gw, gh, 40)
    s.clip_end()
    pipe_h(s, gx + 18, gx + gw - 18, gy + 96, 26)
    pipe_v(s, gx + 300, gy + 96, gy + gh - 24, 26)
    rnd_box(s, gx + 300, gy + 96, 34, "#EDF1F5", "#6C7885", False)
    rnd_box(s, gx + 120, gy + 96, 34, "#EDF1F5", "#6C7885", False)
    callout(s, gx + 26, gy + gh + 40, "কন্ডুইটের রান", gx + 90, gy + 96,
            "start", T_SMALL)
    callout(s, gx + gw - 26, gy + gh + 40, "আউটলেট বাক্স", gx + 300,
            gy + 96 + 34, "end", T_SMALL)

    y = note_strip(s, top + PH + 30,
                   "ঢালাইয়ের পর আর বদলানো যায় না — পুল-ওয়্যার তখনই "
                   "ঢোকাতে হবে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d09_slab.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১০।  পুল বাক্স
# ══════════════════════════════════════════════════════════════════════
def d10_pullbox():
    """অনেক বাঁকের লম্বা রান বনাম পুল বাক্সে ভাগ করা রান।"""
    s = SVG(1240, 700)
    s.title("পুল বাক্স কোথায় দিতে হয়", T_TITLE)

    PW, PH = 578, 428
    top = 104
    panel(s, 30, top, PW, PH, "চার বাঁক, এক টান", RED)
    panel(s, 632, top, PW, PH, "পুল বাক্সে ভাগ", GREEN)

    def run(x0, boxed):
        bx, by = x0 + 62, top + 92
        d = (f"M {bx} {by} L {bx + 210} {by} "
             f"Q {bx + 250} {by} {bx + 250} {by + 40} L {bx + 250} {by + 96} "
             f"Q {bx + 250} {by + 136} {bx + 290} {by + 136} "
             f"L {bx + 400} {by + 136} "
             f"Q {bx + 440} {by + 136} {bx + 440} {by + 176} "
             f"L {bx + 440} {by + 228}")
        pipe(s, d, 28)
        for i, (px, py) in enumerate(((bx + 240, by + 12),
                                      (bx + 258, by + 128),
                                      (bx + 430, by + 148))):
            s.badge(px, py, bn(i + 1), 15, AMBER, "#FFFFFF", 14)
        if boxed:
            sq_box(s, bx + 250, by + 68, 74, 62)
        return bx, by

    bx, by = run(30, False)
    s.text(30 + PW / 2, top + PH - 34, "তার টানতে গিয়ে ছিঁড়ে",
           T_SMALL, RED, 700, "middle")
    bx, by = run(632, True)
    s.text(632 + PW / 2, top + PH - 34, "দুই ছোট টান, দুটিই সহজ",
           T_SMALL, GREEN, 700, "middle")

    y = note_strip(s, top + PH + 30,
                   "বিএনবিসি ১.৩.১৪.১.৫ — ছাদ থেকে নামা প্রতিটি রানে "
                   "পুল বাক্স বাধ্যতামূলক")
    s.fit(y, 24)
    return s.save(f"{OUT}/d10_pullbox.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১১।  লুপ-ইন ওয়্যারিং
# ══════════════════════════════════════════════════════════════════════
def d11_loop():
    """কন্ডুইটে লুপ-ইন — জোড়া কেবল বাক্সের টার্মিনালে।"""
    s = SVG(1240, 660)
    s.title("কন্ডুইটে লুপ-ইন ওয়্যারিং", T_TITLE)

    top = 118
    y_db = top + 106
    # এসডিবি
    s.rect(74, y_db - 62, 150, 124, "#F2F5F8", "#6C7885", 2.6, 6)
    for i in range(4):
        s.rect(92 + i * 32, y_db - 42, 22, 54, "#FBFCFD", "#8E99A6",
               1.4, 2)
    s.text(149, y_db + 50, "এসডিবি", T_SMALL, NAVY, 700, "middle")

    # সিলিং রোজের বাক্স ও সুইচ বাক্স
    rose_x, rose_y = 640, y_db
    sw_x, sw_y = 640, y_db + 250
    lamp_x, lamp_y = 1052, y_db

    pipe_h(s, 224, rose_x - 52, rose_y, 30)
    pipe_v(s, sw_x, rose_y + 52, sw_y - 44, 30)
    pipe_h(s, rose_x + 52, lamp_x - 46, rose_y, 30)

    rnd_box(s, rose_x, rose_y, 52, "#EDF1F5", "#6C7885", False)
    s.text(rose_x, rose_y - 74, "সিলিং রোজের বাক্স", T_SMALL, NAVY, 700,
           "middle")
    sq_box(s, sw_x, sw_y, 96, 82)
    s.text(sw_x, sw_y + 66, "সুইচ বাক্স", T_SMALL, NAVY, 700, "middle")

    # বাতি
    s.circle(lamp_x, lamp_y, 34, "#FFF3CE", AMBER, 2.6)
    for k in range(8):
        a = math.radians(30 + k * 40)
        s.line(lamp_x + 44 * math.cos(a), lamp_y + 44 * math.sin(a),
               lamp_x + 58 * math.cos(a), lamp_y + 58 * math.sin(a),
               AMBER, 2.4)
    s.text(lamp_x, lamp_y + 84, "বাতি", T_SMALL, NAVY, 700, "middle")

    # তিনটি কোর — পাইপের ভেতরে, একটু আলাদা করে আঁকা
    for k, col in enumerate((C_L1, C_N, C_PE)):
        dy = (k - 1) * 8
        s.line(224, rose_y + dy, rose_x - 52, rose_y + dy, col, 3.0)
    for k, col in enumerate((C_N, C_PE)):
        dy = (k - 0.5) * 10
        s.line(rose_x + 52, rose_y + dy, lamp_x - 46, rose_y + dy, col, 3.0)
    s.line(rose_x + 52, rose_y - 12, lamp_x - 46, rose_y - 12, C_L1, 3.0)
    for k, col in enumerate((C_L1, C_L1)):
        dx = (k - 0.5) * 12
        s.line(sw_x + dx, rose_y + 52, sw_x + dx, sw_y - 44, col, 3.0)

    # রঙের চাবি
    kx = 150
    ky = top + 372
    for i, (col, name) in enumerate(((C_L1, "ফেজ"), (C_N, "নিউট্রাল"),
                                     (C_PE, "আর্থ"))):
        s.line(kx + i * 178, ky, kx + i * 178 + 44, ky, col, 5)
        s.text(kx + i * 178 + 54, ky + T_SMALL * 0.34, name, T_SMALL,
               NAVY, 700, "start")

    y = note_strip(s, top + 430,
                   "পাইপের ভেতরে একটিও জোড়া নেই — সব জোড়া বাক্সের "
                   "টার্মিনালে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d11_loop.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১২।  জিআই পাইপের জোড়া
# ══════════════════════════════════════════════════════════════════════
def d12_gijoint():
    """প্যাঁচ, সকেট, বুশ ও ধারাবাহিকতা।"""
    s = SVG(1240, 720)
    s.title("জিআই কন্ডুইটের জোড়া", T_TITLE)

    PW, PH = 578, 300
    top = 104
    panel(s, 30, top, PW, PH, "সকেট দিয়ে জোড়া", NAVY)
    panel(s, 632, top, PW, PH, "বাক্সের মুখে বুশ", STEEL)

    # ── বাঁ ──
    x0, cy = 30, top + 168
    pipe_h(s, x0 + 46, x0 + 250, cy, 40, col=GI, edge=GIE, hi=GIH)
    pipe_h(s, x0 + 330, x0 + PW - 46, cy, 40, col=GI, edge=GIE, hi=GIH)
    thread(s, x0 + 208, x0 + 250, cy, 40)
    thread(s, x0 + 330, x0 + 372, cy, 40)
    s.rect(x0 + 236, cy - 30, 108, 60, "#AEB6BE", GIE, 2.6, 6)
    callout(s, x0 + 62, top + 66, "প্যাঁচ", x0 + 228, cy - 18, "start",
            T_SMALL)
    callout(s, x0 + PW - 62, top + 66, "সকেট", x0 + 290, cy - 30, "end",
            T_SMALL)

    # ── ডান ──
    x0, cy = 632, top + 168
    sq_box(s, x0 + 420, cy, 116, 132)
    pipe_h(s, x0 + 46, x0 + 362, cy, 40, col=GI, edge=GIE, hi=GIH)
    thread(s, x0 + 300, x0 + 344, cy, 40)
    s.rect(x0 + 336, cy - 30, 16, 60, "#AEB6BE", GIE, 2.2, 3)
    s.rect(x0 + 356, cy - 30, 16, 60, "#AEB6BE", GIE, 2.2, 3)
    s.path(f"M {x0 + 372} {cy - 22} Q {x0 + 398} {cy} {x0 + 372} {cy + 22}",
           GIE, 3, "#C6CDD4")
    callout(s, x0 + 66, top + 66, "চেক নাট", x0 + 344, cy - 30, "start",
            T_SMALL)
    callout(s, x0 + PW - 62, top + 250, "বুশ", x0 + 386, cy + 18, "end",
            T_SMALL)

    # ── নিচের পটি:  আর্থিং ──
    ty = top + PH + 34
    panel(s, 30, ty, 1180, 176, "ধারাবাহিকতা ও আর্থিং", GREEN)
    cy2 = ty + 118
    pipe_h(s, 92, 1148, cy2, 38, col=GI, edge=GIE, hi=GIH)
    for xx in (420, 760):
        s.rect(xx - 52, cy2 - 28, 104, 56, "#AEB6BE", GIE, 2.4, 6)
    s.line(92, cy2 + 4, 1148, cy2 + 4, C_PE, 4.2)
    callout(s, 300, cy2 + 74, "আলাদা সবুজ-হলুদ ইসিসি", 300, cy2 + 4,
            "start", T_SMALL, C_PE)

    y = note_strip(s, ty + 200,
                   "জিআই পাইপ নিজেই আর্থ তার নয় — বিএনবিসি ১.৩.১৩ "
                   "আলাদা ইসিসি চায়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d12_gijoint.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১৩।  কাজের ধাপ
# ══════════════════════════════════════════════════════════════════════
def d13_steps():
    """কনসিল্ড কন্ডুইট ওয়্যারিংয়ের ক্রম — নির্মাণকাজের সঙ্গে মিলিয়ে।"""
    s = SVG(1240, 700)
    s.title("কনসিল্ড কন্ডুইটের কাজের ক্রম", T_TITLE)

    rows = [("ছাদ ঢালাইয়ের আগে", ["লে-আউট দাগানো", "স্ল্যাবে পাইপ ও বাক্স",
                                   "পুল-ওয়্যার ঢোকানো"], NAVY),
            ("গাঁথুনির পরে", ["দেয়ালে খাঁজ কাটা", "পাইপ ও বাক্স বসানো",
                              "প্লাস্টার"], STEEL),
            ("প্লাস্টারের পরে", ["তার টানা", "বোর্ড ও ফিটিং",
                                  "পরীক্ষা ও হস্তান্তর"], GREEN)]
    top = 104
    RH = 152
    gap = 16
    n = 0
    for r, (stage, items, col) in enumerate(rows):
        ry = top + r * (RH + gap)
        s.rect(30, ry, 1180, RH, PLATE, LINE, 1.8, 10)
        head_bar(s, 30, ry, 268, RH, stage, col, T_BODY, 10)
        for i, it in enumerate(items):
            n += 1
            cx = 330 + i * 292
            s.rect(cx, ry + 30, 262, RH - 60, "#FFFFFF", LINE, 2, 9)
            s.badge(cx + 30, ry + 30, bn(n), 18, col, "#FFFFFF", 17)
            for j, ln in enumerate(wrap(it, 222, T_BODY, 700)):
                s.text(cx + 131, ry + RH / 2 + 6 + (j - 0.5 *
                       (len(wrap(it, 222, T_BODY, 700)) - 1)) * 30,
                       ln, T_BODY, NAVY, 700, "middle")
            if i < 2:
                arrowhead(s, cx + 282, ry + RH / 2, 0, 13)

    y = note_strip(s, top + 3 * (RH + gap) + 12,
                   "ক্রম উল্টালে খরচ বাড়ে — ঢালাই হয়ে গেলে পাইপ আর "
                   "ঢোকানো যায় না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d13_steps.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১৪।  তার টানা
# ══════════════════════════════════════════════════════════════════════
def d14_pull():
    """পুল-ওয়্যারের সঙ্গে বেঁধে তার টানা।"""
    s = SVG(1240, 620)
    s.title("পুল-ওয়্যার দিয়ে তার টানা", T_TITLE)

    PW, PH = 386, 356
    top = 104
    gap = 20
    x0 = (1240 - 3 * PW - 2 * gap) / 2
    heads = ["পুল-ওয়্যার আগেই ভেতরে", "মাথা বেঁধে টেপ",
             "একজন টানে, একজন ছাড়ে"]
    for i, head in enumerate(heads):
        px = x0 + i * (PW + gap)
        panel(s, px, top, PW, PH, head, STEEL)

    # ১
    px = x0
    cy = top + 200
    pipe_h(s, px + 40, px + PW - 40, cy, 42)
    s.path(f"M {px + 52} {cy} L {px + PW - 66} {cy} "
           f"q 18 0 18 -16 q 0 -16 -18 -16", "#9AA3AC", 3.6)
    s.text(px + PW / 2, cy + 96, "20 SWG GI তার", T_SMALL, GREY, 700,
           "middle")

    # ২
    px = x0 + PW + gap
    cy = top + 200
    pipe_h(s, px + 40, px + 190, cy, 42)
    s.line(px + 190, cy, px + 300, cy, "#9AA3AC", 3.6)
    for k, col in enumerate((C_L1, C_N, C_PE)):
        s.path(f"M {px + 300} {cy} L {px + 330} {cy + (k - 1) * 13} "
               f"L {px + PW - 40} {cy + (k - 1) * 13}", col, 3.4)
    s.rect(px + 282, cy - 22, 34, 44, "#3D4650", "#22282F", 2, 5)
    s.text(px + PW / 2, cy + 96, "টেপ মসৃণ, গিঁট নয়", T_SMALL, GREY,
           700, "middle")

    # ৩
    px = x0 + 2 * (PW + gap)
    cy = top + 200
    pipe_h(s, px + 96, px + PW - 96, cy, 42)
    for k, col in enumerate((C_L1, C_N, C_PE)):
        s.line(px + 30, cy + (k - 1) * 13, px + 108, cy + (k - 1) * 13,
               col, 3.4)
        s.line(px + PW - 108, cy + (k - 1) * 13, px + PW - 30,
               cy + (k - 1) * 13, col, 3.4)
    arrowhead(s, px + 24, cy, 180, 15, STEEL)
    s.text(px + PW / 2, cy + 96, "ঝাঁকি নয়, সমান টান", T_SMALL, GREY,
           700, "middle")

    y = note_strip(s, top + PH + 30,
                   "শুকনো পাইপে টানতে কষ্ট হলে সামান্য ট্যালকম — সাবান "
                   "বা তেল নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d14_pull.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১৫।  এক্সপ্যানশন জয়েন্ট
# ══════════════════════════════════════════════════════════════════════
def d15_expansion():
    """ভবনের এক্সপ্যানশন জয়েন্ট পেরোনো (বিএনবিসি ১.৩.১৫)।"""
    s = SVG(1240, 560)
    s.title("এক্সপ্যানশন জয়েন্ট পেরোনো", T_TITLE)

    top = 116
    sy, sh = top + 34, 116
    concrete(s, 60, sy, 520, sh)
    concrete(s, 660, sy, 520, sh)
    s.rect(580, sy - 14, 80, sh + 28, "#F1DFDF", "#D7A9A9", 2, 3)
    s.text(620, sy - 30, "জয়েন্ট", T_SMALL, RED, 700, "middle")

    cy = sy + sh / 2
    sq_box(s, 470, cy, 92, 78)
    sq_box(s, 770, cy, 92, 78)
    pipe_h(s, 92, 424, cy, 30)
    pipe_h(s, 816, 1148, cy, 30)

    # নমনীয় পাইপ, ভেতরে সরু পাইপ
    fx0, fx1 = 516, 724
    s.path(f"M {fx0} {cy} L {fx1} {cy}", "#8E99A6", 52)
    s.path(f"M {fx0} {cy} L {fx1} {cy}", "#C9D0D8", 46)
    for k in range(14):
        xx = fx0 + 8 + k * 15
        s.line(xx, cy - 22, xx, cy + 22, "#98A2AC", 2.4)
    pipe_h(s, 500, 740, cy, 28)

    callout(s, 300, top + 232, "পুল বাক্স", 470, cy + 39, "start", T_SMALL)
    callout(s, 940, top + 232, "পুল বাক্স", 770, cy + 39, "end", T_SMALL)
    callout(s, 620, top + 268, "বড় মাপের নমনীয় পাইপ", 620, cy + 26,
            "middle", T_SMALL)

    y = note_strip(s, top + 306,
                   "দুই পাশে পুল বাক্স, মাঝখানে ঢিলে নমনীয় পাইপ — "
                   "ভবন নড়লেও তার টানে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d15_expansion.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১৬।  সাধারণ ভুল
# ══════════════════════════════════════════════════════════════════════
def d16_wrong():
    """ছয়টি ভুল, ছয়টি ছোট প্যানেলে।"""
    s = SVG(1240, 780)
    s.title("যে ছয়টি ভুল সবচেয়ে বেশি হয়", T_TITLE)

    CW, CH = 386, 268
    gap = 20
    x0 = (1240 - 3 * CW - 2 * gap) / 2
    top = 104

    def cell(i, name):
        cx = x0 + (i % 3) * (CW + gap)
        cy = top + (i // 3) * (CH + gap)
        s.rect(cx, cy, CW, CH, "#FDF6F6", "#E3B9B9", 2, 10)
        s.text(cx + CW / 2, cy + CH - 20, name, T_SMALL, RED, 700,
               "middle")
        return cx + CW / 2, cy + (CH - 40) / 2 + 14

    # ১ — চ্যাপ্টা বাঁক
    cx, cy = cell(0, "চ্যাপ্টা বাঁক")
    Rb = 34
    pipe(s, f"M {cx - 118} {cy + Rb} L {cx - Rb} {cy + Rb} "
            f"A {Rb} {Rb} 0 0 1 {cx} {cy} L {cx} {cy - 62}", 30)
    s.circle(cx - 22, cy + 12, 26, "none", RED, 3.4)

    # ২ — পাইপের ভেতরে জোড়া
    cx, cy = cell(1, "পাইপের ভেতরে জোড়া")
    pipe_h(s, cx - 130, cx + 130, cy, 40)
    s.line(cx - 122, cy, cx - 14, cy, C_L1, 3.4)
    s.line(cx + 14, cy, cx + 122, cy, C_L1, 3.4)
    s.rect(cx - 20, cy - 13, 40, 26, "#3D4650", "#22282F", 2, 4)
    s.circle(cx, cy, 30, "none", RED, 3.4)

    # ৩ — পুল-ওয়্যার নেই
    cx, cy = cell(2, "পুল-ওয়্যার নেই")
    pipe_h(s, cx - 130, cx + 130, cy, 40)
    s.path(f"M {cx - 40} {cy - 40} l 80 80 M {cx + 40} {cy - 40} l -80 80",
           RED, 3.6)
    s.text(cx, cy - 62, "ভেতরে কিছুই নেই", T_TINY, GREY, 700, "middle")

    # ৪ — বেশি তার
    cx, cy = cell(3, "ধারণক্ষমতার বেশি তার")
    R = 54
    pipe_end(s, cx, cy, R + 12, 12)
    for k in range(9):
        a = 2 * math.pi * k / 9
        core(s, cx + R * 0.62 * math.cos(a), cy + R * 0.62 * math.sin(a),
             15, (C_L1, C_N, C_PE)[k % 3])
    s.circle(cx, cy, R + 26, "none", RED, 3.4)

    # ৫ — কোনাকুনি খাঁজ
    cx, cy = cell(4, "কোনাকুনি খাঁজ")
    brick_wall(s, cx - 140, cy - 62, 280, 124, WALLF, WALLE, 26)
    s.path(f"M {cx - 120} {cy + 44} L {cx + 120} {cy - 44}", "#C9B99F", 26)
    pipe(s, f"M {cx - 120} {cy + 44} L {cx + 120} {cy - 44}", 18)

    # ৬ — মেঝে থেকে উপরে
    cx, cy = cell(5, "মেঝে থেকে উঠে আসা পাইপ")
    concrete(s, cx - 140, cy + 34, 280, 40)
    pipe_v(s, cx, cy - 58, cy + 60, 30)
    for k in range(3):
        s.circle(cx + (k - 1) * 12, cy + 22 - k * 8, 5, "#4C9BD6")
    s.text(cx, cy - 74, "জমা পানি", T_TINY, "#2F6FA8", 700, "middle")

    y = note_strip(s, top + 2 * (CH + gap) + 14,
                   "ছয়টিই ধরা পড়ে অনেক পরে — যখন দেয়াল ভাঙা ছাড়া উপায় "
                   "থাকে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d16_wrong.svg")


# ══════════════════════════════════════════════════════════════════════
#  আলোকচিত্র
# ══════════════════════════════════════════════════════════════════════
def d17_pvc():
    return sheet(
        "d17_pvc", "PVC কন্ডুইট — দোকানে যেমন দেখায়",
        "হেভি গেজ পাইপের আঁটি", "ph_pvc.jpg",
        "প্রতিটি লাঠির গায়ে ৫০ মিলিমিটার দূরত্বে মাপ ও শ্রেণি ছাপা থাকে",
        iw=1000, w=1240)


def d18_gi():
    return strip_callouts(
        "d18_gi", "জিআই কন্ডুইটের মুখ",
        "ph_gi.jpg",
        above=[("গ্যালভানাইজড গা", 0.28, 0.32, 0.42)],
        below=[("কাটা প্যাঁচ", 0.70, 0.755, 0.55),
               ("কাটা মুখ", 0.92, 0.845, 0.47)],
        note="প্যাঁচ কেটে সকেট দিয়ে জোড়া — বিএনবিসি ১.৩.১৪.১.৪",
        iw=1000, w=1240)


def d19_fittings():
    return pair_panels(
        "d19_fittings", "ফিটিং ও বাক্স",
        [("স্যাডল ও কাপলার", "ph_fittings.jpg", STEEL),
         ("প্লাস্টিক ক্লিপ", "ph_clips.jpg", STEEL),
         ("গোল বাক্স", "ph_jbox.jpg", STEEL)],
        "মাপ না মিললে ফিটিং বসে না — পাইপ কেনার সময়েই মিলিয়ে নিতে হবে",
        h=370)


def d20_spring():
    return sheet(
        "d20_spring", "বেন্ডিং স্প্রিং",
        "স্প্রিং ও PVC পাইপ", "ph_spring.jpg",
        "স্প্রিংয়ের বাইরের ব্যাস পাইপের ভেতরের ব্যাসের চেয়ে ১ মিলিমিটার কম",
        iw=980, w=1240)


def d21_bend():
    return pair_panels(
        "d21_bend", "বাঁক — ফল ও হাতিয়ার",
        [("তৈরি ৯০° বাঁক", "ph_bend.jpg", GREEN),
         ("হাতে-ধরা বেন্ডার", "ph_bender.jpg", STEEL)],
        "ধাতব পাইপ বেন্ডারে, PVC স্প্রিং ঢুকিয়ে গরম করে",
        h=390)


def d22_work():
    return pair_panels(
        "d22_work", "কাজ চলাকালীন",
        [("ঢালাইয়ের আগে ছাদে", "ph_slab.jpg", NAVY),
         ("দেয়ালে বসা বাক্স", "ph_wallbox.jpg", NAVY)],
        "বাঁ পাশের অবস্থা ঢালাইয়ের পর আর কোনোদিন দেখা যাবে না",
        h=430)


def d23_surface():
    return pair_panels(
        "d23_surface", "সারফেস কন্ডুইট",
        [("দেয়ালের গায়ে রান", "ph_surface.jpg", STEEL),
         ("স্যাডলে আঁটা", "ph_saddle.jpg", STEEL)],
        "সোজা লাইন, সমান দূরত্বে স্যাডল — বিএনবিসি বলে ৬০০ মিলিমিটার",
        h=430)


def d24_room():
    return sheet(
        "d24_room", "বড় স্থাপনায় কন্ডুইট",
        "একটি বিদ্যুৎ কক্ষ", "ph_room.jpg",
        "একই নিয়ম, শুধু পাইপ মোটা ও সংখ্যায় বেশি",
        iw=1040, w=1240)


def d25_mark():
    """২৬.৩.৪ — একটি আসল পাইপের গায়ে ছাপা লেখা পড়া।"""
    return photo_callouts(
        "d25_mark", "পাইপের গায়ে যা ছাপা থাকে", "ph_mark.jpg",
        left=[("প্রস্তুতকারক", 0.279, 0.305),
              ("উপাদান — uPVC", 0.313, 0.337),
              ("কী জিনিস", 0.409, 0.417)],
        right=[("মাপ — 25 mm", 0.469, 0.492),
               ("দেয়ালের শ্রেণি", 0.543, 0.586),
               ("তৈরির দেশ", 0.650, 0.727)],
        note="প্রস্তুতকারক, মাপ, শ্রেণি ও দেশ — আইএস ৯৫৩৭-এর ৬.১ এই চারটিই চায়",
        iw=1010)


def d26_flex():
    """২৬.৯.১ — নমনীয় পাইপ, হাতে ও বসানো অবস্থায়।"""
    return pair_panels(
        "d26_flex", "নমনীয় পাইপ",
        [("কুণ্ডলী পাকানো অবস্থায়", "ph_flex.jpg", STEEL),
         ("খাঁজে বসানো অবস্থায়", "ph_flexrun.jpg", STEEL)],
        "ঢেউ-খেলানো গা বলেই বাঁকে, আর ওই ঢেউয়েই ময়লা জমে",
        h=360)


def d27_pull():
    """২৬.১০.১ — তার টানার হাতিয়ার।"""
    return pair_panels(
        "d27_pull", "তার টানার হাতিয়ার",
        [("ফিশ টেপের রিল", "ph_fish.jpg", STEEL),
         ("স্টিলের তার ও নাইলনের রড", "ph_fishtip.jpg", STEEL)],
        "পাইপ বসানোর সময়েই পুল-ওয়্যার রেখে দিলে এই হাতিয়ার আর লাগে না",
        h=360)


def d28_ceilbox():
    """২৬.১০.২ — জোড়া বাক্সের ভেতরে, পাইপের ভেতরে নয়।"""
    return pair_panels(
        "d28_ceilbox", "জোড়া যেখানে হয়",
        [("ছাদের জাংশন বাক্স", "ph_ceilbox.jpg", STEEL),
         ("দেয়ালের জাংশন বাক্স", "ph_boxwired.jpg", STEEL)],
        "প্রতিটি জোড়া বাক্সের ভেতরে — ঢাকনা খুললেই হাতের নাগালে",
        h=400)


ALL = [d01_house, d02_two, d03_anatomy, d04_parts, d05_fill, d06_bend,
       d07_bendwork, d08_chase, d09_slab, d10_pullbox, d11_loop,
       d12_gijoint, d13_steps, d14_pull, d15_expansion, d16_wrong,
       d17_pvc, d18_gi, d19_fittings, d20_spring, d21_bend,
       d22_work, d23_surface, d24_room,
       d25_mark, d26_flex, d27_pull, d28_ceilbox,
       ]


if __name__ == "__main__":
    import svgkit as K
    os.makedirs(OUT, exist_ok=True)
    K.COLLECT = True
    for f in ALL:
        try:
            f()
        except Exception as e:
            print("  (collect)", f.__name__, e)
    K.COLLECT = False
    K.flush()
    for f in ALL:
        print("✓", os.path.relpath(f()))
