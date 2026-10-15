# -*- coding: utf-8 -*-
"""অধ্যায় ২৫ — এসডিবি ওয়্যারিং : ডায়াগ্রাম।

অধ্যায় ২৪ ছিল গোটা ভবনের বোর্ড।  এটি একটি **ফ্ল্যাটের** বোর্ড — যে
বাক্সটির ঢাকনা খুলে মিস্ত্রি রোজ কাজ করে।  তাই ছবির ভাগটাও আলাদা:

**আঁকা চিত্র** — বাড়ির কাটা-ছবিতে বোর্ডের জায়গা, ভেতরের সাজ, এক-লাইন
ডায়াগ্রাম, ওয়ের ক্রম, নিউট্রাল বারের ভাগ, এসপিডির অবস্থান, কম্ব বাসবার,
সার্কিট চার্ট, কাজের ধাপ ও পরীক্ষার ক্রম।  এগুলো এক ফ্রেমে ধরা যায় না।

**আলোকচিত্র** — খালি বাক্স থেকে শুরু করে মালামাল, কাজ চলাকালীন অবস্থা,
শেষ হওয়া বোর্ড ও ডেড-ফ্রন্টের চার্ট।  তারের জঙ্গল আর সাজানো তারের
পার্থক্যটি কেবল আলোকচিত্রেই বোঝা যায় (`assets_ch25.py`)।

অধ্যায় ১৫ থেকে চলে আসা ছবির নিয়ম এখানেও কড়া:  প্যানেলের শিরোনাম
বিশেষ্য, যন্ত্রাংশের লেবেল এক-দুই শব্দ, নিচে এক লাইনের একটি নোট-পটি।
কারণ, পরামর্শ আর সতর্কবাণী সবই বইয়ের লেখায় — ছবিতে নয়।

ছবির লেবেলে যা লেখা যাবে না:  কালপুরুষে `÷ √ ² Ω φ ≤` নেই বা ভুল আঁকে।
ভাগ সবসময় `/`, বর্গমিলিমিটার কথায় — `mm2` নয়, লেখা হয় "বর্গমিমি"।
মাপ, রেটিং ও মডিউল-সংখ্যা ল্যাটিন অঙ্কে (অধ্যায় ২৩-এর নিয়ম — কালপুরুষে
বাংলা ৪ ল্যাটিন 8-এর মতো আঁকে, আর রেটিংয়ের ঘরে সেটি অন্য যন্ত্র হয়ে যায়)।
"""
import os

from bookkit import bn
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch25")
IMG = os.path.join(HERE, "assets", "ch25")

# টাইপের মাপ — W-px ক্যানভাস P সেমি চওড়ায় বসলে N-px লেখা
# N × P(pt) / W পয়েন্টে ছাপে।  ১৫.৪ সেমিতে (৪৩৬.৫ pt) ১২৪০-px
# ক্যানভাসে সবচেয়ে ছোট লেখা ২২ px = ৭.৭ pt — প্রকল্পের ~৭.৫ pt
# মেঝের উপরে।  অধ্যায় ১১–১৩-এর শিক্ষা।
T_TITLE = 34
T_NODE = 28
T_NAME = 25
T_BODY = 23
T_SMALL = 22
T_CALL = 24.5
T_TINY = 22

SYM = "#12324D"
SW = 3.4
PLATE = "#F4F7FA"
COPPER = "#B5713A"
COPPERL = "#D79A63"
STEELG = "#8E99A6"
DEAD = "#9AA6B2"

# BNBC ১.৩.৯.৩.১৫ / সারণি ৮.১.২-এর রং
C_L1 = "#D42A1F"
C_L2 = "#D9A400"
C_L3 = "#1B4F9C"
C_N = "#1F2933"
C_PE = "#1B6E47"


# ── shared helpers (অধ্যায় ২২–২৩ থেকে) ─────────────────────────────────
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
    """রঙিন শিরোনাম-পটি, নিচের কোনা চৌকো।

    অধ্যায় ৬-এর শিক্ষা:  পটি বেঁটে হলে গোল কোনা নিজের লেখাকেই কেটে
    দেয়, তাই rx উচ্চতা ও টাইপের মাপ থেকে বেঁধে নেওয়া।
    """
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
    # অধ্যায় ১৯-এর শিক্ষা:  `qc.py` লেখা দেখে, বাক্স দেখে না।  প্যানেল
    # ক্যানভাস ছাড়িয়ে গেলে ছবিটা কাটা যায় অথচ কিউসি পরিষ্কার বলে।
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
    """একটি আলোকচিত্র মাঝখানে, দুই পাশে লেবেল ও লিডার।

    অধ্যায় ১৯-এ শেখা তিনটি ফাঁদ এখানেই বাঁধা:  ছবিটা আগে আঁকো লিডার পরে;
    লিডারের ডগা ছাপা লেখার পাশে রাখো, উপরে নয়; আর প্রতিটি লেবেল তার
    নিজের লক্ষ্যের সমান উচ্চতায় বসে।
    """
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
            y0 = (iy - gap + size * 0.32 + 12) if up else (iy + ih + gap - 8)
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


# ── ছোট আঁকা উপাদান ─────────────────────────────────────────────────────
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


def mcb(s, cx, cy, w=54, h=96, label=None, col="#F2F5F8", size=T_TINY,
        on=True):
    """ডিন রেলে বসা একটি ব্রেকারের সামনের চেহারা।"""
    s.rect(cx - w / 2, cy - h / 2, w, h, col, "#7C8794", 2.2, 5)
    s.rect(cx - w / 2 + 4, cy - h / 2 + 6, w - 8, h * 0.20, "#DFE5EB",
           "none", 0, 3)
    # টগল — উপরে থাকলে চালু
    ty = cy - h * 0.06 if on else cy + h * 0.06
    s.rect(cx - 9, ty - 16, 18, 32, "#2A2E33", "#111417", 1.6, 3)
    if label:
        s.text(cx, cy + h / 2 + size * 1.1, label, size, GREY, 700,
               "middle")


def bar_run(s, x0, x1, y, col, label=None, th=17, lx=None, size=None):
    """একটি বাসবার — আড়াআড়ি তামার পাত, ডান বা বাঁ প্রান্তে নাম।"""
    s.rect(x0, y - th / 2, x1 - x0, th, COPPER, "#8A5326", 1.8, 3)
    s.rect(x0 + 3, y - th / 2 + 3, x1 - x0 - 6, 4, COPPERL, "none", 0, 2)
    if label:
        size = size or T_SMALL
        s.text(lx if lx is not None else x0 - 12, y + size * 0.4, label,
               size, col, 700, "end")


def drop(s, x, y0, y1, col, sw=SW):
    s.line(x, y0, x, y1, col, sw)


# ══════════════════════════════════════════════════════════════════════
#  ১. বিতরণের সিঁড়ি
# ══════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════
#  চ্যাপ্টার ২৫-এর নিজস্ব ছোট উপাদান
# ══════════════════════════════════════════════════════════════════════
def rail(s, x0, x1, y, th=13):
    """ডিন রেলের পাশ থেকে দেখা কাটা-অংশ।"""
    s.rect(x0, y - th / 2, x1 - x0, th, "#C9D0D8", "#8E99A6", 1.8, 2)
    s.rect(x0 + 4, y - th / 2 + 2.5, x1 - x0 - 8, 3.5, "#E7ECF1", "none", 0, 1)


def module(s, x, y, mods, name, rating=None, w1=54, h=104, col="#F7F9FB",
           tog="#2A2E33", size=T_TINY, badge=None, face="toggle", dy=0):
    """ডিন রেলে বসা একটি মডিউলার যন্ত্র — চওড়া মডিউল-সংখ্যা অনুযায়ী।

    ফেরত দেয় (x, প্রস্থ) — পরেরটি কোথায় বসবে তা এখান থেকেই ঠিক হয়।
    """
    w = w1 * mods
    s.rect(x, y - h / 2, w, h, col, "#7C8794", 2.2, 5)
    s.rect(x + 4, y - h / 2 + 6, w - 8, h * 0.19, "#DFE5EB", "none", 0, 3)
    for k in range(mods):
        cx = x + w1 * (k + 0.5)
        if face == "blank":                       # খালি ওয়ের ঢাকনি
            s.rect(cx - 13, y - h * 0.30, 26, 16, "#DFE5EB", "none", 0, 3)
        elif face == "window":                    # এসপিডির অবস্থা-জানালা
            s.rect(cx - 13, y - h * 0.06 - 15, 26, 30, "#FFFFFF",
                   "#7C8794", 1.8, 3)
            s.rect(cx - 9, y - h * 0.06 - 11, 18, 22, tog, "none", 0, 2)
        else:
            s.rect(cx - 9, y - h * 0.06 - 16, 18, 32, tog, "#111417",
                   1.6, 3)
    if badge:
        s.rect(x + 4, y + h / 2 - 26, w - 8, 20, badge, "none", 0, 3)
    if rating:
        s.text(x + w / 2, y + h / 2 + dy + size * 1.05, rating, size,
               STEEL, 700, "middle")
    if name:
        d = dy + (size * 2.15 if rating else size * 1.05)
        for j, ln in enumerate(wrap(name, max(w + 26, 96), size, 700)):
            s.text(x + w / 2, y + h / 2 + d + j * (size + 4), ln, size,
                   NAVY, 700, "middle")
    return x + w


def term_bar(s, x0, x1, y, col, label, holes=12, th=15, lx=None,
             size=T_SMALL, anchor="end"):
    """নিউট্রাল বা আর্থিং টার্মিনাল বার — ছিদ্রসহ।"""
    s.rect(x0, y - th / 2, x1 - x0, th, "#B9C1C9", "#7C8794", 1.8, 3)
    for i in range(holes):
        s.circle(x0 + (x1 - x0) * (i + 0.5) / holes, y, 4.6, "#EDF1F5",
                 "#6C7885", 1.4)
    s.rect(x0, y - th / 2 - 7, x1 - x0, 6, col, "none", 0, 2)
    s.text(lx if lx is not None else x0 - 12, y + size * 0.4, label, size,
           col, 700, anchor)


def trip_flag(s, cx, cy, text="ট্রিপ", col=RED, bg=REDBG):
    w = tw(text, T_SMALL, 700) + 34
    s.rect(cx - w / 2, cy - 20, w, 40, bg, col, 2.2, 20)
    s.text(cx, cy + T_SMALL * 0.34, text, T_SMALL, col, 700, "middle")


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
#  ১. এসডিবি কোথায় বসে
# ══════════════════════════════════════════════════════════════════════
def d01_place():
    """বাড়ির কাটা-ছবি — এমডিবি নিচে, রাইজার, ফ্ল্যাটের এসডিবি।"""
    t_sm, t_cl = 24, 26
    s = SVG(1240, 1020)
    s.title("বিতরণের সিঁড়িতে এসডিবির জায়গা", T_TITLE)

    bx, bw = 300, 560
    ground = 856
    fh = 236
    top = ground - 3 * fh

    # ভবনের খোল ও তিনটি স্ল্যাব
    s.rect(bx - 20, top - 30, bw + 40, ground - top + 50, "#EEF2F6",
           "#A9B3BE", 3, 6)
    s.rect(bx, top, bw, ground - top, "#FDFDFE", "#A9B3BE", 2.2, 3)
    for k in range(4):
        yy = ground - k * fh
        s.rect(bx - 20, yy - 13, bw + 40, 17, "#D5DCE3", "#8E99A6", 1.8, 2)
    s.rect(bx - 96, ground + 4, bw + 192, 24, "#CBD3DA", "#8E99A6", 2, 3)

    # রাইজার — বাঁ দেয়াল ঘেঁষে
    rx = bx + 62
    mdb_y = ground - fh + 96
    s.rect(rx - 20, top + 24, 40, mdb_y - 30 - top - 24, "#E4E9EE",
           "#8E99A6", 2.2, 5)
    for k in range(1, 3):
        s.line(rx - 20, ground - 13 - k * fh, rx + 20, ground - 13 - k * fh,
               "#A9B3BE", 1.6)

    # নিচতলা — সার্ভিস ও এমডিবি
    mx = rx + 92
    s.rect(mx, mdb_y - 62, 176, 146, "#F2F5F8", "#6C7885", 2.6, 6)
    for r in range(2):
        for i in range(7):
            s.rect(mx + 16 + i * 22, mdb_y - 40 + r * 48, 15, 36,
                   "#FBFCFD", "#8E99A6", 1.4, 2)
    s.text(mx + 88, mdb_y + 68, "MDB", t_sm, NAVY, 700, "middle")
    sv_y = ground - 34
    s.line(bx - 96, sv_y, mx + 88, sv_y, C_L1, 3.4)
    s.line(mx + 88, sv_y, mx + 88, mdb_y + 84, C_L1, 3.4)
    # এমডিবি → রাইজার
    s.line(mx, mdb_y - 30, rx, mdb_y - 30, C_L1, 3.4)

    # দোতলা — মিটার, এসডিবি, ঘরের বোর্ড
    fy = ground - 2 * fh + 118
    s.line(rx, fy, rx, mdb_y - 30, C_L1, 3.2)
    s.rect(rx + 24, fy - 46, 72, 92, "#FBFCFD", "#6C7885", 2.4, 5)
    s.rect(rx + 34, fy - 28, 52, 26, "#DCE4EA", "#8E99A6", 1.6, 3)
    s.text(rx + 60, fy + 30, "মিটার", 21, NAVY, 700, "middle")
    s.line(rx, fy, rx + 24, fy, C_L1, 3.2)

    sx = rx + 148
    s.rect(sx, fy - 60, 206, 120, "#F2F5F8", "#6C7885", 2.6, 6)
    rail(s, sx + 14, sx + 192, fy + 4, 9)
    for i in range(10):
        s.rect(sx + 20 + i * 18, fy - 26, 13, 58, "#FBFCFD", "#8E99A6",
               1.4, 2)
    s.text(sx + 103, fy + 50, "SDB", t_sm, NAVY, 700, "middle")
    s.line(rx + 96, fy, sx, fy, C_L1, 3.2)

    bxs = sx + 250
    for i in range(3):
        py = fy - 54 + i * 52
        s.rect(bxs, py, 30, 34, "#FFFFFF", "#8E99A6", 1.8, 3)
        for k in range(2):
            s.rect(bxs + 6 + k * 11, py + 8, 8, 18, "#E7ECF1", "#8E99A6",
                   1.2, 1)
        s.line(sx + 206, fy, bxs, py + 17, C_L1, 2.2)

    # তিনতলা — পরের ফ্ল্যাট, আবছা
    ty = ground - 3 * fh + 118
    s.rect(sx, ty - 44, 206, 88, "#F7F9FB", "#B9C1C9", 2.2, 6)
    s.text(sx + 103, ty + 8, "পরের ফ্ল্যাট", 22, "#98A2AD", 700, "middle")
    s.line(rx, ty, sx, ty, "#C4CCD4", 2.6)
    s.line(rx, ty, rx, fy, "#C4CCD4", 2.6)

    for txt, tx, ty2, ly in [("সার্ভিস লাইন", bx - 60, sv_y, sv_y),
                             ("রাইজার", rx - 20, ground - fh - 30,
                              ground - fh - 30),
                             ("ফ্ল্যাটের মিটার", rx + 24, fy - 20, fy - 20)]:
        callout(s, bx - 108, ly, txt, tx, ty2, "end", t_cl)
    for txt, tx, ty2, ly in [("ভবনের MDB", mx + 176, mdb_y, mdb_y),
                             ("ফ্ল্যাটের SDB", sx + 206, fy - 44, fy - 130),
                             ("ঘরের সুইচবোর্ড", bxs + 30, fy - 2, fy + 44)]:
        callout(s, bx + bw + 62, ly, txt, tx, ty2, "start", t_cl)

    y = note_strip(s, ground + 56,
                   "এসডিবি ফ্ল্যাটের ভেতরে, লোডের কেন্দ্রের কাছে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_place.svg")


# ══════════════════════════════════════════════════════════════════════
#  ২. এসডিবির ভেতরে
# ══════════════════════════════════════════════════════════════════════
def d02_inside():
    """সামনে থেকে দেখা এসডিবি — ঢাকনা ও ডেড-ফ্রন্ট আলাদা করে নিচে।

    ভেতরের তার এখানে ইচ্ছাকৃতভাবে আঁকা নেই — এই ছবির কাজ অংশগুলো চেনানো,
    জোড়া দেখানো নয়।  জোড়া আছে চিত্র ২৫.৪-এর এক-লাইন ডায়াগ্রামে।
    """
    # ১৪০০-px ক্যানভাস ১৫.৪ সেমিতে বসে, তাই এই ছবির টাইপ বড় —
    # N × P(pt) / W নিয়মে ২৬ px = ৮.১ pt (অধ্যায় ৮-এর কৌশল)
    t_sm, t_cl, t_lb = 26, 27, 24
    s = SVG(1400, 1060)
    s.title("এসডিবির ভেতরের অংশগুলো", T_TITLE)

    bx, by, bw, bh = 300, 148, 700, 520
    s.rect(bx - 16, by - 16, bw + 32, bh + 32, "#E9EDF2", "#8E99A6", 3, 10)
    s.rect(bx, by, bw, bh, "#FBFCFD", "#8E99A6", 2.4, 6)

    ko_y = by + bh - 26
    for i in range(5):
        s.circle(bx + 150 + i * 100, by + 26, 15, "#E4E9EE", "#8E99A6", 2)
        s.circle(bx + 150 + i * 100, ko_y, 15, "#E4E9EE", "#8E99A6", 2)

    ny = by + 96
    term_bar(s, bx + 96, bx + bw - 96, ny, C_N, "N", 14, lx=bx + 82)

    ry = by + 224
    rail(s, bx + 34, bx + bw - 34, ry + 62)
    mx0 = bx + 46
    x = module(s, mx0, ry, 2, "মেইন এমসিবি", "40 A", w1=46, h=112,
               size=t_lb, dy=18)
    x = module(s, x + 20, ry, 2, "এসপিডি", "Type 2", w1=46, h=112,
               tog="#3C6E4F", size=t_lb, face="window", dy=18)
    x = module(s, x + 20, ry, 2, "আরসিসিবি", "30 mA", w1=46, h=112,
               tog="#B35C00", size=t_lb, dy=18)
    gx0 = x + 22
    x = gx0
    for i in range(5):
        x = module(s, x, ry, 1, None, None, w1=46, h=112)
    s.text((gx0 + x) / 2, ry + 74 + t_lb * 1.05, "ওয়ে এমসিবি", t_lb,
           STEEL, 700, "middle")
    s.text((gx0 + x) / 2, ry + 74 + t_lb * 2.15, "প্রতিটি 1M", t_lb,
           NAVY, 700, "middle")
    # খালি ওয়ে — ফাঁকা ঢাকনি, টগল নেই
    bl = x + 8
    s.rect(bl, ry - 56, 46, 112, "#EDF1F5", "#A9B3BE", 2.2, 5)
    s.rect(bl + 6, ry - 44, 34, 22, "#DFE5EB", "none", 0, 3)

    ey = by + bh - 108
    term_bar(s, bx + 96, bx + bw - 96, ey, C_PE, "E", 14, lx=bx + 82)

    # নিচে — ডেড-ফ্রন্ট ও ঢাকনা, আলাদা করে
    ar = s.arrow_defs(STEEL, "ar2", 13)
    py = by + bh + 112
    for i, (px, nm) in enumerate(((bx + 40, "ডেড-ফ্রন্ট"),
                                  (bx + 396, "ঢাকনা ও চার্ট পকেট"))):
        s.rect(px, py, 264, 96, "#F2F5F8", "#8E99A6", 2.4, 8)
        if i == 0:
            s.rect(px + 44, py + 30, 176, 36, "#FFFFFF", "#8E99A6", 2, 4)
            for k in range(9):
                s.rect(px + 50 + k * 19, py + 34, 13, 28, "#E4E9EE",
                       "none", 0, 2)
        else:
            s.rect(px + 26, py + 18, 150, 60, "#DCE6EE", "#8E99A6", 2, 5)
            for k in range(4):
                s.line(px + 36, py + 30 + k * 13, px + 166,
                       py + 30 + k * 13, "#9BAAB8", 2)
            s.rect(px + 194, py + 34, 46, 28, "#B9C1C9", "#7C8794", 1.8, 3)
        s.text(px + 132, py + 132, nm, t_sm, NAVY, 700, "middle")
        s.line(px + 132, py - 12, px + 132, py - 52, STEEL, 3, marker=ar)

    left = [("ধাতব বা পিভিসি বাক্স", bx, by + 40, by + 22),
            ("উপরের নকআউট", bx + 150, by + 26, by + 116),
            ("নিউট্রাল বার", bx + 120, ny, by + 210),
            ("ডিন রেল", bx + 46, ry + 62, by + 310)]
    right = [("খালি ওয়ে", bl + 46, ry - 20, by + 40),
             ("আর্থিং বার", bx + bw - 120, ey, by + 320),
             ("ক্যাবলের পথ", bx + 550, ko_y, by + 430)]
    for txt, tx, ty, ly in left:
        callout(s, bx - 70, ly, txt, tx, ty, "end", t_cl)
    for txt, tx, ty, ly in right:
        callout(s, bx + bw + 70, ly, txt, tx, ty, "start", t_cl)

    y = note_strip(s, py + 172,
                   "নিউট্রাল বার উপরে, আর্থিং বার নিচে; সব বোর্ডে একই ক্রম",
                   pad=44)
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_inside.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৩. ওয়ে সাজানোর ক্রম
# ══════════════════════════════════════════════════════════════════════
#  ফ্ল্যাটের রেলে যা যা বসে — (মডিউল, অঞ্চল)।  অঞ্চলগুলোই ছবির শিক্ষা,
#  প্রতিটি ওয়ের নাম নয়;  নাম আছে অধ্যায়ের সারণিতে।
ROW = [(2, 0), (2, 0), (2, 0),
       (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1),
       (2, 2), (1, 2), (1, 2),
       (1, 3), (1, 3)]
ZONES = [("মেইন ও সুরক্ষা", "#2E5F8A", "#E4EEF7"),
         ("আরসিসিবির অধীনে", "#B35C00", "#FBEEDD"),
         ("আরসিসিবির বাইরে", "#3C6E4F", "#E3F0E8"),
         ("খালি ওয়ে", "#6C7885", "#EDF1F5")]


def d03_ways():
    """ডিন রেলে ১৮ মডিউল — কোন অঞ্চলে কী বসে।"""
    s = SVG(1240, 760)
    s.title("রেলে ওয়ে সাজানোর ক্রম", T_TITLE)

    total = sum(m for m, _z in ROW)              # ১৮ মডিউল
    x0, x1 = 74, 1166
    w1 = (x1 - x0) / total
    ry = 400
    rail(s, x0 - 22, x1 + 22, ry + 60, 12)

    # অঞ্চলের বন্ধনী — যন্ত্রের উপরে
    x, seg = x0, []
    for mods, z in ROW:
        if seg and seg[-1][0] == z:
            seg[-1][2] = x + mods * w1
        else:
            seg.append([z, x, x + mods * w1])
        x += mods * w1
    for z, a, bb in seg:
        nm, col, bg = ZONES[z]
        s.rect(a + 3, 142, bb - a - 6, 68, bg, col, 2.2, 9)
        for j, ln in enumerate(wrap(nm, bb - a - 24, T_SMALL, 700)):
            s.text((a + bb) / 2, 172 + j * 26 - (len(wrap(nm, bb - a - 24,
                   T_SMALL, 700)) - 1) * 13, ln, T_SMALL, col, 700,
                   "middle")
        s.line((a + bb) / 2, 212, (a + bb) / 2, 336, col, 2.4)

    # যন্ত্র ও নম্বর
    x, n = x0, 1
    for mods, z in ROW:
        col = {0: "#F2F6FA", 1: "#FDF6EC", 2: "#F0F7F2",
               3: "#EDF1F5"}[z]
        tog = {0: "#2A2E33", 1: "#B35C00", 2: "#3C6E4F",
               3: "#B9C1C9"}[z]
        face = ("window" if (z == 0 and n == 3)
                else "blank" if z == 3 else "toggle")
        module(s, x, ry, mods, None, None, w1=w1, h=104, col=col, tog=tog,
               face=face)
        for k in range(mods):
            s.text(x + w1 * (k + 0.5), ry + 84, str(n + k), T_TINY,
                   NAVY, 700, "middle")
        x += mods * w1
        n += mods

    # মডিউল-মাপকাঠি
    my = ry + 128
    s.line(x0, my, x1, my, STEEL, 2.4)
    for k in range(total + 1):
        s.line(x0 + k * w1, my - 8, x0 + k * w1, my + 8, STEEL, 2)
    s.text(620, my + 44, "18 মডিউল: প্রতিটি 17.5 মিলিমিটার", T_NAME,
           NAVY, 700, "middle")

    y = note_strip(s, my + 82,
                   "বাঁ থেকে ডানে: মেইন, সুরক্ষা, তারপর সার্কিট")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_ways.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৪. এক-লাইন ডায়াগ্রাম
# ══════════════════════════════════════════════════════════════════════
def _dot(s, x, y, col):
    s.circle(x, y, 7, col, "none", 0)


def d04_sld():
    """মডেল ফ্ল্যাটের এসডিবি — এক-লাইন ডায়াগ্রাম।

    জোড়ার নিয়ম চিত্রের নিজের ভাষায়:  ভরাট ফোঁটা মানে জোড়া;  ফোঁটা ছাড়া
    যেখানে তার বার পেরিয়ে গেছে, সেখানে জোড়া নেই।  অধ্যায় ২৪-এর একই রীতি।
    পাঁচটি বার উপরে সাজানো, প্রতিটি সার্কিট নিচে নামে — তাই কোনো তারকে
    উল্টো দিকে উঠতে হয় না।
    """
    s = SVG(1240, 1180)
    s.title("মডেল ফ্ল্যাটের এসডিবি: এক-লাইন ডায়াগ্রাম", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 12)

    bx0, bx1 = 116, 1160
    cx = 250
    ORNG = "#B35C00"

    y = 112
    blk(s, cx, y, "ফ্ল্যাটের মিটার", 280, 60)
    s.line(cx, y + 30, cx, y + 64, STEEL, SW, marker=ar)
    y += 96
    blk(s, cx, y, "মেইন এমসিবি  40 A DP", 320, 60)

    b1l, b1n = 286, 326
    for k, (yy, col, nm) in enumerate(((b1l, C_L1, "L"), (b1n, C_N, "N"))):
        bar_run(s, bx0, bx1, yy, col, nm, 15, bx0 - 20)
        dx = cx - 26 + k * 52
        s.line(dx, y + 30, dx, yy, col, 2.8)
        _dot(s, dx, yy, col)

    # আরসিসিবি — মূল বার থেকে খাওয়া
    rx = 560
    s.rect(rx - 108, 372, 216, 82, "#FBEEDD", ORNG, 2.6, 9)
    s.text(rx, 406, "আরসিসিবি", T_SMALL, ORNG, 700, "middle")
    s.text(rx, 438, "40 A / 30 mA", T_SMALL, NAVY, 700, "middle")
    s.line(rx - 40, b1l, rx - 40, 372, C_L1, 2.8)
    _dot(s, rx - 40, b1l, C_L1)
    s.line(rx + 40, b1n, rx + 40, 372, C_N, 2.8)
    _dot(s, rx + 40, b1n, C_N)

    # এসপিডি — আরসিসিবির আগে, মূল বার-জোড়াতেই
    sx = 838
    s.rect(sx - 48, 376, 96, 74, "#E3F0E8", "#3C6E4F", 2.4, 8)
    s.text(sx, 420, "SPD", T_SMALL, "#3C6E4F", 700, "middle")
    s.line(sx - 22, b1l, sx - 22, 376, C_L1, 2.6)
    _dot(s, sx - 22, b1l, C_L1)
    s.line(sx + 22, b1n, sx + 22, 376, C_N, 2.6)
    _dot(s, sx + 22, b1n, C_N)

    # আরসিসিবির পরের বার-জোড়া, তারপর আর্থিং বার
    b2l, b2n, be = 528, 570, 614
    bar_run(s, bx0, 730, b2l, ORNG, "L2", 15, bx0 - 20)
    bar_run(s, bx0, 730, b2n, ORNG, "N2", 15, bx0 - 20)
    bar_run(s, bx0, bx1, be, C_PE, "E", 15, bx0 - 20)
    s.line(rx - 40, 454, rx - 40, b2l, C_L1, 2.8)
    _dot(s, rx - 40, b2l, ORNG)
    s.line(rx + 40, 454, rx + 40, b2n, C_N, 2.8)
    _dot(s, rx + 40, b2n, ORNG)
    s.line(sx, 450, sx, be, C_PE, 2.8)
    _dot(s, sx, be, C_PE)

    wy, out_y = 700, 826

    def way(x, nm, rt, lbar, nbar, lcol, tog="#2A2E33"):
        s.line(x, lbar, x, wy - 44, lcol, 2.6)
        _dot(s, x, lbar, lcol)
        module(s, x - 25, wy, 1, None, None, w1=50, h=88, tog=tog)
        s.line(x, wy + 44, x, out_y, lcol, 2.6)
        s.line(x + 26, nbar, x + 26, out_y, lcol, 2.2)
        _dot(s, x + 26, nbar, lcol)
        s.line(x + 48, be, x + 48, out_y, C_PE, 2.2)
        _dot(s, x + 48, be, C_PE)
        s.line(x - 4, out_y, x + 48, out_y, STEEL, 2.4)
        s.line(x + 22, out_y, x + 22, out_y + 40, STEEL, 3, marker=ar)
        s.text(x + 22, out_y + 76, rt, T_TINY, STEEL, 700, "middle")
        for j, ln in enumerate(wrap(nm, 100, T_TINY, 700)):
            s.text(x + 22, out_y + 108 + j * 26, ln, T_TINY, NAVY, 700,
                   "middle")

    under = [("বাতি-ফ্যান ১", "6 A"), ("বাতি-ফ্যান ২", "6 A"),
             ("সকেট ১", "10 A"), ("সকেট ২", "10 A"),
             ("রান্নাঘর", "16 A"), ("পাম্প", "10 A")]
    for i, (nm, rt) in enumerate(under):
        way(140 + i * 104, nm, rt, b2l, b2n, ORNG, ORNG)

    out = [("গিজার", "16 A RCBO"), ("এসি 2 টন", "20 A"),
           ("এসি 1 টন", "10 A")]
    for i, (nm, rt) in enumerate(out):
        way(880 + i * 116, nm, rt, b1l, b1n, C_L1,
            ORNG if i == 0 else "#2A2E33")

    ex = 790
    s.line(ex, be, ex, be + 54, C_PE, 3)
    _dot(s, ex, be, C_PE)
    for k, hw in enumerate((30, 20, 10)):
        s.line(ex - hw, be + 58 + k * 12, ex + hw, be + 58 + k * 12,
               C_PE, 3.4)

    y2 = note_strip(s, out_y + 178,
                    "L2 ও N2 বার আরসিসিবির পরে; সেখানকার ওয়ের নিউট্রাল "
                    "ওই বারেই")
    s.fit(y2, 24)
    return s.save(f"{OUT}/d04_sld.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৫. নিউট্রাল বারের ভাগ — এই অধ্যায়ের কেন্দ্রীয় ছবি
# ══════════════════════════════════════════════════════════════════════
ORNG = "#B35C00"


def _nboard(s, x0, w, split, top=170):
    """একটি ছোট বোর্ড — আরসিসিবি, দুই ওয়ে, নিউট্রাল বার এক বা দুই।"""
    a, b = x0 + 64, x0 + w - 34
    yl, yn = top, top + 40
    bar_run(s, a, b, yl, C_L1, "L", 13, a - 24)
    bar_run(s, a, b, yn, C_N, "N", 13, a - 24)

    rx = x0 + w / 2
    s.rect(rx - 92, top + 96, 184, 68, "#FBEEDD", ORNG, 2.4, 9)
    s.text(rx, top + 128, "আরসিসিবি", T_SMALL, ORNG, 700, "middle")
    s.text(rx, top + 156, "30 mA", T_TINY, NAVY, 700, "middle")
    s.line(rx - 34, yl, rx - 34, top + 96, C_L1, 2.6)
    _dot(s, rx - 34, yl, C_L1)
    s.line(rx + 34, yn, rx + 34, top + 96, C_N, 2.6)
    _dot(s, rx + 34, yn, C_N)

    y2 = top + 216
    bar_run(s, a, b, y2, ORNG, "L2", 13, a - 24)
    s.line(rx - 34, top + 164, rx - 34, y2, C_L1, 2.6)
    _dot(s, rx - 34, y2, ORNG)
    yn2 = None
    if split:
        yn2 = top + 256
        bar_run(s, a, b, yn2, ORNG, "N2", 13, a - 24)
        s.line(rx + 34, top + 164, rx + 34, yn2, C_N, 2.6)
        _dot(s, rx + 34, yn2, ORNG)
    return yl, yn, y2, yn2


def d05_neutral():
    """আরসিসিবির পরের নিউট্রাল কোথায় যাবে — ভুল ও সঠিক।"""
    s = SVG(1240, 1080)
    s.title("আরসিসিবির নিউট্রাল কোন বারে", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar5", 12)

    pw, gap = 590, 26
    px = [(1240 - 2 * pw - gap) / 2 + i * (pw + gap) for i in range(2)]
    for i, (hd, split) in enumerate((("এক নিউট্রাল বার", False),
                                     ("দুই নিউট্রাল বার", True))):
        x0 = px[i]
        col = RED if not split else GREEN
        s.rect(x0, 100, pw, 700, "#FCFDFE", LINE, 1.8, 13)
        s.box_auto(x0 + pw / 2, 112, hd, T_BODY, fill=col, stroke=col,
                   tcolor="#FFFFFF", pad_x=22, pad_y=9)

        yl, yn, y2, yn2 = _nboard(s, x0, pw, split, 200)
        wy, oy = 560, 660
        for k, (nm, on_rccb) in enumerate((("ওয়ে ১", True),
                                           ("ওয়ে ২", False))):
            wx = x0 + 150 + k * 250
            lb = y2 if on_rccb else yl
            lc = ORNG if on_rccb else C_L1
            s.line(wx, lb, wx, wy - 40, lc, 2.6)
            _dot(s, wx, lb, lc)
            module(s, wx - 24, wy, 1, None, None, w1=48, h=80,
                   tog=ORNG if on_rccb else "#2A2E33")
            s.line(wx, wy + 40, wx, oy, lc, 2.6)
            # নিউট্রাল — এখানেই ভুলটি হয়
            nb = (yn if (not split and on_rccb) or (not on_rccb) else yn2)
            bad = on_rccb and not split
            s.line(wx + 30, nb, wx + 30, oy, RED if bad else
                   (ORNG if on_rccb else C_N), 2.4,
                   dash="9 6" if bad else None)
            _dot(s, wx + 30, nb, RED if bad else
                 (ORNG if on_rccb else C_N))
            s.line(wx - 6, oy, wx + 30, oy, STEEL, 2.4)
            s.line(wx + 12, oy, wx + 12, oy + 34, STEEL, 3, marker=ar)
            s.text(wx + 12, oy + 68, nm, T_SMALL, NAVY, 700, "middle")
            s.text(wx + 12, oy + 96,
                   "আরসিসিবির অধীনে" if on_rccb else "আরসিসিবির বাইরে",
                   T_TINY, GREY, 700, "middle")
        if not split:
            trip_flag(s, x0 + pw / 2, 480, "আরসিসিবি ট্রিপ")

    vy = 0
    for i, (ok, txt) in enumerate((
            (False, "ওয়ে ১-এর নিউট্রাল আরসিসিবির বাইরে; "
                    "যন্ত্র অসাম্য দেখে ট্রিপ করে"),
            (True, "যে বার থেকে ফেজ, সেই বারেই নিউট্রাল; অসাম্য শূন্য"))):
        vy = max(vy, verdict(s, px[i] + 16, 824, pw - 32, ok, txt))

    y = note_strip(s, vy + 34,
                   "ভাঙা লাল রেখা: যে তারটি ভুল বারে গেছে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_neutral.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৬. এসপিডি কোথায় বসবে
# ══════════════════════════════════════════════════════════════════════
def d06_spd():
    """এসপিডি আরসিসিবির আগে না পরে — সার্জ কারেন্টের পথ।"""
    s = SVG(1240, 1060)
    s.title("এসপিডি আরসিসিবির কোন পাশে", T_TITLE)
    ar = s.arrow_defs("#C8880E", "sg", 14)
    ar2 = s.arrow_defs(STEEL, "ld", 12)

    pw, gap = 590, 26
    px = [(1240 - 2 * pw - gap) / 2 + i * (pw + gap) for i in range(2)]
    for i, before in enumerate((True, False)):
        x0 = px[i]
        col = GREEN if before else RED
        hd = "এসপিডি আরসিসিবির আগে" if before else "এসপিডি আরসিসিবির পরে"
        s.rect(x0, 100, pw, 720, "#FCFDFE", LINE, 1.8, 13)
        s.box_auto(x0 + pw / 2, 112, hd, T_BODY, fill=col, stroke=col,
                   tcolor="#FFFFFF", pad_x=20, pad_y=9)

        a, b = x0 + 66, x0 + pw - 40
        yl, yn, ye = 218, 260, 664
        bar_run(s, a, b, yl, C_L1, "L", 13, a - 24)
        bar_run(s, a, b, yn, C_N, "N", 13, a - 24)
        bar_run(s, a, b, ye, C_PE, "E", 13, a - 24)

        rxp = x0 + 172                       # আরসিসিবি সবসময় বাঁয়ে
        sxp = x0 + 424                       # এসপিডি সবসময় ডানে
        # আরসিসিবি
        s.rect(rxp - 84, 330, 168, 74, "#FBEEDD", ORNG, 2.4, 9)
        s.text(rxp, 362, "আরসিসিবি", T_SMALL, ORNG, 700, "middle")
        s.text(rxp, 390, "30 mA", T_TINY, NAVY, 700, "middle")
        s.line(rxp - 30, yl, rxp - 30, 330, C_L1, 2.6)
        _dot(s, rxp - 30, yl, C_L1)
        s.line(rxp + 30, yn, rxp + 30, 330, C_N, 2.6)
        _dot(s, rxp + 30, yn, C_N)

        # আরসিসিবির পরের বার-জোড়া
        y2l, y2n = 470, 508
        bar_run(s, a, b, y2l, ORNG, "L2", 12, a - 24)
        bar_run(s, a, b, y2n, ORNG, "N2", 12, a - 24)
        s.line(rxp - 30, 404, rxp - 30, y2l, C_L1, 2.6)
        _dot(s, rxp - 30, y2l, ORNG)
        s.line(rxp + 30, 404, rxp + 30, y2n, C_N, 2.6)
        _dot(s, rxp + 30, y2n, ORNG)
        # সার্কিটের দিকে
        cxp = x0 + 296
        s.line(cxp, y2l, cxp, 566, ORNG, 2.6)
        _dot(s, cxp, y2l, ORNG)
        s.line(cxp + 26, y2n, cxp + 26, 566, ORNG, 2.4)
        _dot(s, cxp + 26, y2n, ORNG)
        s.line(cxp - 6, 566, cxp + 26, 566, STEEL, 2.4)
        s.line(cxp + 10, 566, cxp + 10, 600, STEEL, 3, marker=ar2)
        s.text(cxp + 10, 634, "সার্কিটের দিকে", T_TINY, NAVY, 700,
               "middle")

        # এসপিডি — আগে হলে মূল বারে, পরে হলে L2/N2-তে
        tl, tn, tc = ((yl, yn, C_L1) if before else (y2l, y2n, ORNG))
        s.rect(sxp - 60, 330, 120, 74, "#E3F0E8", "#3C6E4F", 2.4, 8)
        s.text(sxp, 374, "SPD", T_SMALL, "#3C6E4F", 700, "middle")
        if before:
            s.line(sxp - 24, tl, sxp - 24, 330, tc, 2.6)
            s.line(sxp + 24, tn, sxp + 24, 330, C_N, 2.6)
            _dot(s, sxp - 24, tl, tc)
            _dot(s, sxp + 24, tn, C_N)
        else:
            s.line(sxp - 24, 404, sxp - 24, tl, tc, 2.6)
            s.line(sxp + 24, 404, sxp + 24, tn, tc, 2.6)
            _dot(s, sxp - 24, tl, tc)
            _dot(s, sxp + 24, tn, tc)
        s.line(sxp, 404, sxp, ye, C_PE, 2.8)
        _dot(s, sxp, ye, C_PE)

        # সার্জ কারেন্টের পথ
        s.path(f"M {a + 10} {yl - 36} L {(sxp - 24) if before else (rxp - 30)}"
               f" {yl - 36} L {(sxp - 24) if before else (rxp - 30)}"
               f" {yl - 12}", "#C8880E", 4, marker=ar)
        s.text(a, yl - 28, "সার্জ", T_TINY, "#8A5C05", 700, "end")
        if not before:
            trip_flag(s, x0 + pw / 2, 762, "আরসিসিবি ট্রিপ")

    vy = 0
    for i, (ok, txt) in enumerate((
            (True, "সার্জ কারেন্ট আরসিসিবির ভেতর দিয়ে যায় না"),
            (False, "সার্জ কারেন্ট আরসিসিবির ভেতর দিয়ে আর্থে যায়"))):
        vy = max(vy, verdict(s, px[i] + 16, 848, pw - 32, ok, txt))

    y = note_strip(s, vy + 34,
                   "এসপিডির L, N ও PE তারের মোট দৈর্ঘ্য 0.5 মিটারের বেশি নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_spd.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৭. কম্ব বাসবার
# ══════════════════════════════════════════════════════════════════════
def d07_comb():
    """ফেজ বিলির দুই পদ্ধতি — আলাদা জাম্পার ও কম্ব বাসবার।"""
    s = SVG(1240, 900)
    s.title("ওয়েতে ফেজ বিলি করার দুই পদ্ধতি", T_TITLE)

    pw, gap = 570, 40
    px = [(1240 - 2 * pw - gap) / 2 + i * (pw + gap) for i in range(2)]
    for i, comb in enumerate((False, True)):
        x0 = px[i]
        hd = "কম্ব বাসবার" if comb else "আলাদা জাম্পার তার"
        panel(s, x0, 100, pw, 470, hd)

        ry = 330
        xs = [x0 + 108 + k * 96 for k in range(4)]
        if comb:
            # কম্ব — ইনসুলেটেড দেহ, নিচে দাঁত
            s.rect(xs[0] - 34, ry - 154, xs[-1] - xs[0] + 68, 40,
                   "#E7ECF1", "#7C8794", 2.2, 6)
            bar_run(s, xs[0] - 26, xs[-1] + 26, ry - 134, COPPER, None, 13)
            for x in xs:
                s.rect(x - 7, ry - 114, 14, 66, COPPER, "#8A5326", 1.6, 3)
            s.line(xs[0] - 34, ry - 172, xs[0] - 34, ry - 154, C_L1, 3.4)
            s.text(xs[0] - 34, ry - 186, "L", T_TINY, C_L1, 700, "middle")
        else:
            for k in range(3):
                hy = ry - 100 - k * 26
                s.path(f"M {xs[k]} {ry - 48} L {xs[k]} {hy} "
                       f"L {xs[k + 1]} {hy} L {xs[k + 1]} {ry - 48}",
                       C_L1, 3.2)
            for x in xs:
                s.circle(x, ry - 48, 5.4, "#8A5326", "none", 0)
            s.line(xs[0], ry - 100, xs[0], ry - 176, C_L1, 3.4)
            s.text(xs[0], ry - 190, "L", T_TINY, C_L1, 700, "middle")

        for k, x in enumerate(xs):
            module(s, x - 24, ry, 1, None, None, w1=48, h=96)
            s.line(x, ry + 48, x, ry + 92, C_L1, 2.6)
            s.text(x, ry + 128, f"ওয়ে {bn(k + 1)}", T_TINY, NAVY, 700,
                   "middle")

    vy = 0
    for i, (ok, txt) in enumerate((
            (False, "প্রতিটি জোড়ায় একটি করে আলগা হওয়ার জায়গা"),
            (True, "একটি টুকরো, একবার আঁটা, সব ওয়েতে সমান ফেজ"))):
        vy = max(vy, verdict(s, px[i] + 16, 596, pw - 32, ok, txt))

    y = note_strip(s, vy + 34,
                   "কম্বের দাঁত কাটার পর খোলা প্রান্তে ঢাকনি লাগে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_comb.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৮. বোর্ড কোথায় বসবে
# ══════════════════════════════════════════════════════════════════════
def d08_where():
    """বসানোর জায়গা — চলে ও চলে না।"""
    s = SVG(1240, 900)
    s.title("এসডিবি বসানোর জায়গা", T_TITLE)
    ar = s.arrow_defs(STEEL, "dim", 11)

    pw, gap = 570, 40
    px = [(1240 - 2 * pw - gap) / 2 + i * (pw + gap) for i in range(2)]

    def board(x, y, w=132, h=92):
        s.rect(x, y, w, h, "#F2F5F8", "#6C7885", 2.6, 6)
        rail(s, x + 12, x + w - 12, y + h / 2 + 8, 8)
        for k in range(7):
            s.rect(x + 16 + k * 15, y + 22, 11, 46, "#FBFCFD", "#8E99A6",
                   1.3, 2)

    # ── ক : চলে ──────────────────────────────────────────────────────
    x0 = px[0]
    panel(s, x0, 100, pw, 500, "প্রবেশপথের দেয়াল")
    fl = 520
    s.rect(x0 + 40, 176, pw - 80, fl - 176, "#F7F9FB", "#C4CCD4", 2, 3)
    s.rect(x0 + 30, fl, pw - 60, 20, "#CBD3DA", "#8E99A6", 2, 3)
    bx = x0 + 300
    board(bx, 236)
    # উচ্চতার মাপ
    dx = x0 + 250
    s.line(dx, 236, dx, fl, STEEL, 2, dash="7 5")
    s.line(dx, 240, dx, 236, STEEL, 2.4, marker=ar)
    s.line(dx, fl - 4, dx, fl, STEEL, 2.4, marker=ar)
    s.text(dx - 14, 380, "2 মিটারের নিচে", T_TINY, NAVY, 700, "end")
    # সামনে খালি জায়গা
    s.rect(bx - 20, fl - 96, 172, 96, "#EAF2FA", "#7FA6C9", 2, 6,
           dash="9 6")
    s.text(bx + 66, fl - 42, "সামনে খালি", T_TINY, "#2E5F8A", 700,
           "middle")

    # ── খ : চলে না ───────────────────────────────────────────────────
    x1 = px[1]
    panel(s, x1, 100, pw, 500, "গোসলখানার দেয়াল")
    s.rect(x1 + 40, 176, pw - 80, fl - 176, "#F2F7FA", "#C4CCD4", 2, 3)
    s.rect(x1 + 30, fl, pw - 60, 20, "#CBD3DA", "#8E99A6", 2, 3)
    # ঝরনা
    s.rect(x1 + 96, 200, 20, 46, "#B9C1C9", "#7C8794", 2, 3)
    s.ellipse(x1 + 106, 254, 34, 13, "#B9C1C9", "#7C8794", 2)
    for k in range(7):
        s.line(x1 + 82 + k * 8, 268 + (k % 3) * 8, x1 + 78 + k * 8,
               300 + (k % 3) * 8, "#7FA6C9", 2.4)
    bx2 = x1 + 300
    board(bx2, 236)
    for k in range(3):
        s.circle(bx2 + 22 + k * 24, 212 + (k % 2) * 10, 5, "#7FA6C9",
                 "none", 0)
    # আলমারি — বোর্ডের সামনে
    s.rect(bx2 - 34, fl - 150, 118, 150, "#E4D9C8", "#A08A66", 2.4, 4)
    s.line(bx2 + 25, fl - 150, bx2 + 25, fl, "#A08A66", 2)
    s.circle(bx2 + 18, fl - 76, 5, "#8A7350", "none", 0)
    s.circle(bx2 + 32, fl - 76, 5, "#8A7350", "none", 0)
    trip_flag(s, x1 + 462, 214, "ভেজা দেয়াল", RED, REDBG)

    vy = 0
    for i, (ok, txt) in enumerate((
            (True, "শুকনো দেয়াল, হাতের নাগালে, সামনে দাঁড়ানোর জায়গা"),
            (False, "ভেজা দেয়াল, আর সামনে আসবাব; দুটিই নিষেধ"))):
        vy = max(vy, verdict(s, px[i] + 16, 626, pw - 32, ok, txt))

    y = note_strip(s, vy + 34,
                   "মেঝে থেকে বোর্ডের দূরত্ব 2 মিটারের বেশি নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d08_where.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৯. নম্বর, লেবেল ও সার্কিট চার্ট
# ══════════════════════════════════════════════════════════════════════
CHART = [("1", "মেইন", "40 A"), ("2", "এসপিডি", "Type 2"),
         ("3", "আরসিসিবি", "30 mA"), ("4", "বাতি-ফ্যান ১", "6 A"),
         ("5", "বাতি-ফ্যান ২", "6 A"), ("6", "সকেট ১", "10 A")]


def d09_label():
    """ডেড-ফ্রন্টে নম্বর, নিচে লেবেল, দরজায় চার্ট।"""
    t_cl = 25
    s = SVG(1240, 900)
    s.title("নম্বর, লেবেল ও সার্কিট চার্ট", T_TITLE)
    ar = s.arrow_defs(STEEL, "lb", 12)

    # ডেড-ফ্রন্ট
    fx, fy, fw, fh = 252, 190, 520, 230
    s.rect(fx, fy, fw, fh, "#F2F5F8", "#8E99A6", 2.6, 8)
    n = 12
    ww = (fw - 60) / n
    for k in range(n):
        x = fx + 30 + k * ww
        s.rect(x + 2, fy + 42, ww - 4, 84, "#FFFFFF", "#A9B3BE", 1.6, 3)
        s.rect(x + ww / 2 - 7, fy + 62, 14, 28, "#2A2E33", "#111417",
               1.4, 3)
        s.text(x + ww / 2, fy + 30, str(k + 1), T_TINY, NAVY, 700,
               "middle")
    # লেবেল পটি
    s.rect(fx + 30, fy + 140, fw - 60, 40, "#FFF9E8", "#C8A44E", 2, 4)
    for k in range(n):
        x = fx + 30 + k * ww
        if k:
            s.line(x, fy + 140, x, fy + 180, "#C8A44E", 1.4)
    for k, t in enumerate(("মে", "SPD", "RC", "বা১", "বা২", "স১", "স২",
                           "রান্না", "পাম্প", "গিজ", "AC2", "AC1")):
        s.text(fx + 30 + (k + 0.5) * ww, fy + 168, t, 19, "#8A6A12", 700,
               "middle")

    # দরজার ভেতরে চার্ট
    cx, cy, cw = 830, 160, 376
    ch = 60 + len(CHART) * 44
    s.rect(cx - 14, cy - 14, cw + 28, ch + 28, "#F2F5F8", "#8E99A6",
           2.6, 8)
    s.rect(cx, cy, cw, ch, "#FFFFFF", "#A9B3BE", 2, 5)
    s.text(cx + cw / 2, cy + 34, "সার্কিট চার্ট", T_BODY, NAVY, 700,
           "middle")
    s.line(cx + 14, cy + 50, cx + cw - 14, cy + 50, "#C4CCD4", 1.8)
    for k, (num, nm, rt) in enumerate(CHART):
        yy = cy + 84 + k * 44
        s.text(cx + 40, yy, num, T_SMALL, STEEL, 700, "middle")
        s.text(cx + 76, yy, nm, T_SMALL, NAVY, 700, "start")
        s.text(cx + cw - 30, yy, rt, T_SMALL, STEEL, 700, "end")
        s.line(cx + 14, yy + 14, cx + cw - 14, yy + 14, "#E4E9EE", 1.4)
    s.text(cx + cw / 2, cy + ch - 14, "…", T_BODY, GREY, 700, "middle")

    callout(s, fx - 26, fy + 24, "ওয়ে নম্বর", fx + 32, fy + 26, "end",
            t_cl)
    callout(s, fx - 26, fy + 168, "লেবেল পটি", fx + 30, fy + 160, "end",
            t_cl)
    s.line(fx + fw + 12, fy + 100, cx - 26, fy + 100, STEEL, 3,
           marker=ar)

    y = note_strip(s, max(fy + fh, cy + ch) + 90,
                   "ওয়ের নম্বর, লেবেলের নম্বর ও চার্টের নম্বর একই হতে হবে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d09_label.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১০. কাজের ধাপ
# ══════════════════════════════════════════════════════════════════════
def d10_steps():
    """এসডিবি ওয়্যারিংয়ের আটটি ধাপ, ক্রমে।"""
    s = SVG(1240, 820)
    s.title("এসডিবি ওয়্যারিংয়ের ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "st", 12)

    steps = ["সার্কিট তালিকা", "বাক্স বসানো", "রেল ও যন্ত্র",
             "ফেজ বিলি", "নিউট্রাল ও আর্থ", "প্রান্ত ও ফেরুল",
             "নম্বর ও চার্ট", "পরীক্ষা ও চালু"]
    cols, top = 4, 118
    cw, chh, gx, gy = 262, 130, 24, 96
    x0 = (1240 - (cols * cw + (cols - 1) * gx)) / 2
    for i, txt in enumerate(steps):
        r, c = divmod(i, cols)
        if r % 2:                                # সাপের মতো
            c = cols - 1 - c
        x = x0 + c * (cw + gx)
        y = top + r * (chh + gy)
        s.rect(x, y, cw, chh, "#FBFCFD", STEEL, 2.6, 12)
        # কালপুরুষে বাংলা ৪ আর ৮ প্রায় একই দেখায়; ধাপের নম্বর
        # পরিচয়ের ঘর, তাই ল্যাটিন অঙ্কে (অধ্যায় ২৩-এর নিয়ম)
        s.badge(x + 34, y + 32, "12345678"[i], 20, NAVY)
        lines = wrap(txt, cw - 48, T_BODY, 700)
        for j, ln in enumerate(lines):
            s.text(x + cw / 2, y + 84 + j * 30 - (len(lines) - 1) * 15,
                   ln, T_BODY, NAVY, 700, "middle")
    for i in range(len(steps) - 1):
        r, c = divmod(i, cols)
        r2, c2 = divmod(i + 1, cols)
        cc = cols - 1 - c if r % 2 else c
        cc2 = cols - 1 - c2 if r2 % 2 else c2
        if r == r2:
            xa = x0 + min(cc, cc2) * (cw + gx) + cw
            xb = x0 + max(cc, cc2) * (cw + gx)
            ya = top + r * (chh + gy) + chh / 2
            if cc2 > cc:
                s.line(xa + 4, ya, xb - 8, ya, STEEL, 3, marker=ar)
            else:
                s.line(xb - 4, ya, xa + 8, ya, STEEL, 3, marker=ar)
        else:
            xa = x0 + cc * (cw + gx) + cw / 2
            ya = top + r * (chh + gy) + chh
            s.line(xa, ya + 4, xa, ya + gy - 8, STEEL, 3, marker=ar)

    y = note_strip(s, top + 2 * (chh + gy) - gy + 40,
                   "সার্কিট তালিকা আগে না হলে বাক্সের মাপই ঠিক করা যায় না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d10_steps.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১১. চালু করার আগে
# ══════════════════════════════════════════════════════════════════════
def d11_test():
    """চালু করার আগের পাঁচটি পরীক্ষা, ক্রমে।"""
    s = SVG(1240, 760)
    s.title("চালু করার আগে: পাঁচটি পরীক্ষা", T_TITLE)
    ar = s.arrow_defs(STEEL, "ts", 12)

    items = [("চোখে দেখা", "আলগা স্ক্রু, খোলা নকআউট"),
             ("কন্টিনিউইটি", "প্রতিটি ইসিসি বারে পৌঁছেছে"),
             ("ইনসুলেশন", "500 V মেগারে, লোড খুলে"),
             ("পোলারিটি", "ফেজ ব্রেকারে, নিউট্রাল বারে"),
             ("আরসিসিবি ট্রিপ", "টেস্ট বোতাম ও ট্রিপ মিটার")]
    top = 120
    bw, bh, gap = 214, 214, 22
    x0 = (1240 - (5 * bw + 4 * gap)) / 2
    for i, (name, sub) in enumerate(items):
        x = x0 + i * (bw + gap)
        s.rect(x, top, bw, bh, "#FBFCFD", STEEL, 2.6, 12)
        s.badge(x + bw / 2, top + 44, "12345"[i], 24, NAVY, size=21)
        for j, ln in enumerate(wrap(name, bw - 26, T_BODY, 700)):
            s.text(x + bw / 2, top + 100 + j * 28, ln, T_BODY, NAVY, 700,
                   "middle")
        for j, ln in enumerate(wrap(sub, bw - 24, T_SMALL, 400)):
            s.text(x + bw / 2, top + 158 + j * 25, ln, T_SMALL, GREY, 400,
                   "middle")
        if i:
            s.line(x - gap - 2, top + bh / 2, x - 6, top + bh / 2, STEEL,
                   3, marker=ar)

    s.rect(x0, top + bh + 46, 5 * bw + 4 * gap, 74, GREENBG, GREEN, 2.4, 12)
    s.text(620, top + bh + 92, "পাঁচটিই পাশ করলে তবেই মেইন ব্রেকার চালু",
           T_NAME, GREEN, 700, "middle")

    y = note_strip(s, top + bh + 146,
                   "ফলাফল কাগজে লিখে গ্রাহককে দিতে হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d11_test.svg")


# ══════════════════════════════════════════════════════════════════════
#  আলোকচিত্র ও সোর্স-স্লাইড
# ══════════════════════════════════════════════════════════════════════
def d12_empty():
    return photo_callouts(
        "d12_empty", "খালি এসডিবি বাক্স", "ph_empty.jpg",
        left=[("ঢাকনা", 0.300, 0.300),
              ("বাক্সের খোল", 0.178, 0.700),
              ("ডিন রেল", 0.420, 0.775)],
        right=[("নিউট্রাল বার", 0.500, 0.605),
               ("আর্থিং প্রান্ত", 0.845, 0.605)],
        note="বাক্স কেনার সময়েই দুটি বার আছে কি না দেখে নিতে হয়",
        iw=560, w=1240, size=T_CALL)


def d13_comb():
    # ph_rail.jpg (৩:১ ফিতা) এখানে জোড়া লাগানো যায় না — সমান উচ্চতার
    # প্যানেলে সে ১০৩৪ px চওড়া হয়ে ক্যানভাস ছাড়িয়ে যায়।  ডিন রেল
    # চিত্র ২৫.১০-এর ছবিতেই লেবেল করা আছে, তাই আলাদা ফ্রেম লাগে না।
    return sheet(
        "d13_comb", "কেনার পর, বসানোর আগে", "কম্ব বাসবার ও ব্রেকার",
        "ph_comb.jpg", "কম্বের দৈর্ঘ্য বাক্সের ওয়ে-সংখ্যার সমান হতে হয়",
        iw=1060, w=1240)


def d14_kit():
    return sheet(
        "d14_kit", "একটি ফ্ল্যাটের মালামাল", "কাজ শুরুর আগে",
        "ph_kit.jpg", "ফেরুল, রেল-স্টপার আর বার; এগুলোই আগে ফুরায়",
        iw=1120, w=1240)


def d15_bridge():
    return sheet(
        "d15_bridge", "কম্ব বাসবার বসানো অবস্থায়", "ওয়ের উপরের প্রান্ত",
        "ph_bridge.jpg", "কম্বের নিচে প্রতিটি স্ক্রু আলাদা করে আঁটতে হয়",
        iw=900, w=1240)


def d16_work():
    return sheet(
        "d16_work", "কাজ চলাকালীন বোর্ড", "রেল ও যন্ত্র বসেছে",
        "ph_work.jpg", "তার এখনো লম্বা; কেটে মাপে আনা হয় সবার শেষে",
        iw=1000, w=1240)


def d17_flat():
    return photo_callouts(
        "d17_flat", "শেষ হওয়া ফ্ল্যাটের বোর্ড", "ph_flat.jpg",
        left=[("উপরের টার্মিনাল বার", 0.300, 0.105),
              ("আর্থিং টার্মিনাল", 0.258, 0.270),
              ("ওয়ে এমসিবি", 0.280, 0.720)],
        right=[("মেইন এমসিবি", 0.432, 0.330),
               ("আরসিসিবি সারি", 0.470, 0.455),
               ("নিচের টার্মিনাল বার", 0.620, 0.885)],
        note="উপরে-নিচে টার্মিনাল বার, মাঝে যন্ত্র; চেনা সাজ",
        iw=470, w=1240, size=T_CALL)


def d18_rows():
    """দুই সারির বোর্ডে ওয়ের নাম।

    **অধ্যায়ে ব্যবহার করা হয়নি** — ছবিটি ভালো, কিন্তু লেবেলের শিক্ষা
    আঁকা চিত্র ২৫.১৬ (d09_label) ও চিত্র ২৫.১৭-এর (d19_chart) ছাপা
    চার্টেই সম্পূর্ণ হয়ে যায়, আর একটি বাড়তি খাড়া আলোকচিত্র
    ২৫.৯.৭-এ পাতার পাদদেশে ৭ সেন্টিমিটারের ফাঁক খুলে দিচ্ছিল।
    ব্যবহারকারী চাইলে `ALL`-এ ফিরিয়ে আনলেই চলবে।
    """
    return photo_callouts(
        "d18_rows", "দুই সারির বোর্ডে লেবেল", "ph_rows.jpg",
        left=[("উপরের সারি", 0.300, 0.320),
              ("নিচের সারি", 0.200, 0.720)],
        right=[("টার্মিনাল বার", 0.820, 0.062),
               ("ওয়ের নাম", 0.638, 0.420)],
        note="প্রতিটি ওয়ের গায়ে নাম; চার্ট আর বোর্ড এক কথা বলে",
        iw=520, w=1240, size=T_CALL)


def d19_chart():
    return pair_panels(
        "d19_chart", "একই বোর্ড: বাইরে ও ভেতরে",
        [("ডেড-ফ্রন্টে চার্ট", "ph_chart.jpg", STEEL),
         ("ঢাকনা খোলা", "ph_neat.jpg", STEEL)],
        "প্রতিটি সারির উপরে ছাপা নাম; ব্যবহারকারীর জন্য", h=660)


def d20_board_src():
    return sheet(
        "d20_board_src", "ইনস্টিটিউটের ফ্ল্যাট-এসডিবি",
        "সোর্স সংযোগ-ছক", "h33_board.png",
        "মেইন এমসিবি, আরসিসিবি, এসপিডি, তারপর ওয়ের সারি",
        iw=1160, w=1240)


def d21_flat_src():
    return sheet(
        "d21_flat_src", "এসডিবি থেকে গোটা ফ্ল্যাট",
        "সোর্স সংযোগ-ছক", "h34_flat.png",
        "একটি ঘরের বাতি, ফ্যান, এক্সহস্ট ও বেল; একই বোর্ড থেকে",
        iw=1160, w=1240)


def d22_two_src():
    return sheet(
        "d22_two_src", "দুই ঘরের ফ্ল্যাট",
        "সোর্স সংযোগ-ছক", "h36_flat.png",
        "একদিকে পিয়ানো বোর্ড, একদিকে গ্যাং বোর্ড",
        iw=1160, w=1240)


ALL = [d01_place, d02_inside, d03_ways, d04_sld, d05_neutral, d06_spd,
       d07_comb, d08_where, d09_label, d10_steps, d11_test,
       d12_empty, d13_comb, d14_kit, d15_bridge, d16_work,
       d17_flat, d19_chart,
       d20_board_src, d21_flat_src, d22_two_src,
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
