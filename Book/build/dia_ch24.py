# -*- coding: utf-8 -*-
"""অধ্যায় ২৪ — এমডিবি ওয়্যারিং : ডায়াগ্রাম।

দুই রকম ছবি, ভাগটি ইচ্ছাকৃত:

**আলোকচিত্র** — একটি বাড়ির মেইন প্যানেল তৈরি হওয়ার ক্রমে তোলা ছ'টি ছবি
(`assets_ch24.py`)।  বোর্ডের ভেতরটি আঁকা ছবিতে যতই পরিষ্কার হোক, তারের
জঙ্গল আর সাজানো তারের পার্থক্যটি কেবল আলোকচিত্রেই বোঝা যায়।

**আঁকা চিত্র** — সিঁড়ি, গঠন, এক-লাইন ডায়াগ্রাম, ফেজ ভারসাম্য, ড্রপের
বাজেট, ধাপ ও পরীক্ষা।  এগুলো বাস্তবে এক ফ্রেমে ধরা যায় না।

অধ্যায় ১৫ থেকে চলে আসা ছবির নিয়ম এখানেও কড়া:  প্যানেলের শিরোনাম
বিশেষ্য, যন্ত্রাংশের লেবেল এক-দুই শব্দ, নিচে এক লাইনের একটি নোট-পটি।
কারণ, পরামর্শ আর সতর্কবাণী সবই বইয়ের লেখায় — ছবিতে নয়।

ছবির লেবেলে যা লেখা যাবে না:  কালপুরুষে `÷ √ ² Ω φ ≤` নেই বা ভুল আঁকে।
ভাগ সবসময় `/`, বর্গমিলিমিটার কথায় — `mm2` নয়, লেখা হয় "বর্গমিমি"।
মাপ, গেজ ও ইঞ্চি-কোড ল্যাটিন অঙ্কে (অধ্যায় ২৩-এর নিয়ম — কালপুরুষে
বাংলা ৪ ল্যাটিন 8-এর মতো আঁকে, আর মাপের ঘরে সেটি অন্য জিনিস হয়ে যায়)।
"""
import os

from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch24")
IMG = os.path.join(HERE, "assets", "ch24")

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
def d01_tree():
    """BNBC ১.৩.৯.২-এর বোর্ড-শ্রেণি, উপর থেকে নিচে।"""
    s = SVG(1240, 900)
    s.title("বিতরণের সিঁড়ি: সার্ভিস থেকে সুইচবোর্ড", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 14)

    rows = [
        ("সার্ভিস কানেকশন", "সাবস্টেশন বা খুঁটি থেকে", STEEL),
        ("MDB", "মেইন ডিস্ট্রিবিউশন বোর্ড", NAVY),
        ("FDB", "ফ্লোর ডিস্ট্রিবিউশন বোর্ড", STEEL),
        ("SDB / DB", "ফ্ল্যাটের বোর্ড", STEEL),
        ("BDB", "শাখা বোর্ড", STEEL),
        ("সুইচবোর্ড", "বাতি, ফ্যান, সকেট", GREY),
    ]
    top, gap = 104, 128
    bw, bh = 300, 74
    cx = 500
    for i, (name, sub, col) in enumerate(rows):
        y = top + i * gap
        head_bar(s, cx - bw / 2, y, bw, bh, name, col, T_NODE)
        s.text(cx + bw / 2 + 26, y + bh / 2 + 8, sub, T_NAME, GREY, 700)
        if i:
            s.line(cx, y - gap + bh, cx, y - 12, STEEL, 3, marker=ar)

    # বাঁ পাশে সংখ্যার ইঙ্গিত — কোন স্তরে কয়টি
    counts = [None, "একটি", "প্রতি তলায়", "প্রতি ফ্ল্যাটে", "দরকারমতো",
              "প্রতি ঘরে"]
    for i, c in enumerate(counts):
        if c:
            s.text(cx - bw / 2 - 26, top + i * gap + bh / 2 + 8, c,
                   T_SMALL, STEEL, 700, "end")

    y = note_strip(s, top + len(rows) * gap - gap + bh + 40,
                   "প্রতিটি স্তরে ইনকামিং ও আউটগোয়িং দুই দিকেই সুরক্ষা")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_tree.svg")


# ══════════════════════════════════════════════════════════════════════
#  ২. এমডিবির ভেতরে কী থাকে (আঁকা)
# ══════════════════════════════════════════════════════════════════════
def d02_inside():
    """সামনে থেকে দেখা এমডিবি — দরজা খোলা, ভেতরের ঘরগুলো নামসহ।"""
    # ১৪০০-px ক্যানভাস ১৫.৪ সেমিতে বসে, তাই এই ছবির নিজের টাইপ বড় —
    # N × P(pt) / W নিয়মে ২৬ px = ৮.১ pt (অধ্যায় ৮-এর T_CALL কৌশল)
    t_sm, t_cl = 26, 27
    s = SVG(1400, 1140)
    s.title("এমডিবির ভেতরের ঘরগুলো", T_TITLE)

    bx, by, bw, bh = 300, 130, 640, 880
    # ইনকামিং ক্যাবলের ডগা — শিরোনামের নিচ থেকে নেমে ছাদে ঢোকে
    s.rect(bx + 292, 78, 56, by - 62, "#2A2E33", "#0B0D0F", 2.4, 8)

    # বাক্স
    s.rect(bx - 16, by - 16, bw + 32, bh + 32, "#E9EDF2", "#8E99A6", 3, 10)
    s.rect(bx, by, bw, bh, "#FBFCFD", "#8E99A6", 2.4, 6)

    # ছাদে গ্ল্যান্ড প্লেট
    gy = by + 10
    s.rect(bx + 8, gy, bw - 16, 44, "#D5DCE3", "#8E99A6", 2, 4)
    for i in range(4):
        s.circle(bx + 152 + i * 92, gy + 22, 14, "#AEB8C2", "#6C7885", 2)

    # মেইন ব্রেকার
    my = by + 96
    s.rect(bx + 214, my, 212, 128, "#2F343A", "#14181C", 2.4, 8)
    s.rect(bx + 236, my + 20, 168, 46, "#4C545C", "none", 0, 5)
    s.rect(bx + 290, my + 78, 60, 34, "#C7CDD4", "#7C8794", 2, 4)
    s.text(bx + 320, my + 103, "I / O", t_sm, "#1A1A1A", 700, "middle")

    # বাসবার চেম্বার
    byy = by + 262
    s.rect(bx + 6, byy - 16, bw - 12, 178, "#F2F5F8", LINE, 2, 6)
    bars = []
    for i, (col, nm) in enumerate(((C_L1, "L1"), (C_L2, "L2"),
                                   (C_L3, "L3"), (C_N, "N"))):
        yy = byy + 18 + i * 40
        bar_run(s, bx + 96, bx + bw - 96, yy, col, nm, 17, bx + 52,
                size=t_sm)
        s.rect(bx + 62, yy - 16, 24, 32, "#B33027", "#7A1C16", 1.8, 4)
        s.rect(bx + bw - 86, yy - 16, 24, 32, "#B33027", "#7A1C16", 1.8, 4)
        bars.append(yy)

    # ডিন রেলে আউটগোয়িং ব্রেকার — দুই সারি
    rails = []
    for r in range(2):
        ry = by + 520 + r * 148
        s.rect(bx + 40, ry - 58, bw - 80, 12, "#C7CDD4", "#8E99A6", 1.6, 2)
        rails.append(ry)
        for i in range(9):
            mcb(s, bx + 76 + i * 62, ry, 50, 92)

    # নিচে নিউট্রাল ও আর্থিং টার্মিনাল বার
    ny = by + 790
    bar_run(s, bx + 70, bx + bw - 70, ny, C_N, "N", 15, bx + 44,
            size=t_sm)
    bar_run(s, bx + 70, bx + bw - 70, ny + 46, C_PE, "E", 15, bx + 44,
            size=t_sm)
    for i in range(12):
        s.circle(bx + 96 + i * 42, ny, 6, "#E7ECF1", "#7C8794", 1.6)
        s.circle(bx + 96 + i * 42, ny + 46, 6, "#E7ECF1", "#7C8794", 1.6)

    left = [("ইনকামিং ক্যাবল", bx + 292, 108, 130),
            ("গ্ল্যান্ড প্লেট", bx + 152, gy + 22, 250),
            ("মেইন ব্রেকার", bx + 214, my + 64, 372),
            ("বাসবার চেম্বার", bx + 12, byy + 78, 520),
            ("আউটগোয়িং ব্রেকার", bx + 76, rails[0], 690),
            ("নিউট্রাল বার", bx + 96, ny, 872)]
    right = [("ধাতব বাক্স", bx + bw + 14, by + 60, 150),
             ("ইনসুলেটর", bx + bw - 74, bars[0], 330),
             ("ফেজ বার", bx + bw - 100, bars[2], 452),
             ("ডিন রেল", bx + bw - 46, rails[1] - 52, 640),
             ("আর্থিং বার", bx + bw - 88, ny + 46, 862)]
    for txt, tx, ty, ly in left:
        callout(s, bx - 64, ly, txt, tx, ty, "end", t_cl)
    for txt, tx, ty, ly in right:
        callout(s, bx + bw + 64, ly, txt, tx, ty, "start", t_cl)

    y = note_strip(s, by + bh + 44,
                   "ফেজ বার উপরে, টার্মিনাল বার দুটি নিচে; সব সময় এই ক্রমে",
                   pad=40)
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_inside.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৩. বসানোর জায়গা ও মাপ
# ══════════════════════════════════════════════════════════════════════
def d03_place():
    """দুই ভিউ — দেয়ালে উচ্চতা, আর পাশ থেকে সামনের ফাঁকা জায়গা।

    উচ্চতা আর সামনের ফাঁকা জায়গা একই ভিউয়ে আঁকা যায় না:  উচ্চতা
    দেখা যায় সামনে থেকে, আর গভীরতা পাশ থেকে।  এক ছবিতে দুটি জোর
    করলে তীরটা কোথা থেকে শুরু হলো তা-ই বোঝা যায় না।
    """
    s = SVG(1240, 780)
    s.title("বোর্ড কোথায়, কত উঁচুতে", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 12)

    pw, gap, ph, top = 590, 30, 500, 100
    x0 = (1240 - (2 * pw + gap)) / 2

    def wall_hatch(x, y, w, h):
        s.rect(x, y, w, h, "#EDF1F5", "#9AA6B2", 2, 3)
        k = int(h // 26)
        for i in range(k + 1):
            s.line(x, y + i * 26, x + w, y + max(0, i * 26 - w), GREY, 1.1)

    # ── প্যানেল ১:  সামনে থেকে ──────────────────────────────────────
    px = x0
    panel(s, px, top, pw, ph, "সামনে থেকে")
    fy = top + ph - 78                       # মেঝে
    s.rect(px + 30, fy, pw - 60, 20, "#E1E6EC", "#9AA6B2", 2, 3)
    s.text(px + pw / 2, fy + 52, "মেঝে", T_SMALL, GREY, 700, "middle")

    # বোর্ড
    bw2, bh2 = 168, 190
    bx2, bcy = px + 132, top + 168
    s.rect(bx2, bcy - bh2 / 2, bw2, bh2, "#FBFCFD", "#7C8794", 3, 6)
    for r in range(3):
        s.rect(bx2 + 20, bcy - 62 + r * 44, bw2 - 40, 26, "#DDE4EA",
               "#9AA6B2", 1.8, 3)
    s.text(bx2 + bw2 / 2, bcy + bh2 / 2 - 16, "MDB", T_BODY, NAVY, 700,
           "middle")
    dx = bx2 + bw2 + 56
    s.line(bx2 + bw2, bcy, dx + 10, bcy, STEEL, 1.4, dash="7 5")
    s.line(dx, bcy, dx, fy, STEEL, 2.2, marker=ar)
    chip(s, dx + 84, (bcy + fy) / 2, "সর্বোচ্চ 2 m")

    # ── প্যানেল ২:  পাশ থেকে ────────────────────────────────────────
    qx = x0 + pw + gap
    panel(s, qx, top, pw, ph, "পাশ থেকে")
    wall_hatch(qx + 40, top + 66, 44, ph - 154)
    s.rect(qx + 30, fy, pw - 60, 20, "#E1E6EC", "#9AA6B2", 2, 3)
    s.text(qx + pw / 2, fy + 52, "মেঝে", T_SMALL, GREY, 700, "middle")

    # পাশ থেকে বোর্ড — দেয়াল থেকে বেরিয়ে আসা গভীরতা
    dpt = 74
    s.rect(qx + 84, top + 96, dpt, 168, "#FBFCFD", "#7C8794", 3, 5)
    s.text(qx + 84 + dpt / 2, top + 292, "MDB", T_BODY, NAVY, 700,
           "middle")

    # সামনের ফাঁকা জায়গা
    cz0, cz1 = qx + 84 + dpt, qx + 84 + dpt + 288
    s.rect(cz0, top + 96, cz1 - cz0, fy - top - 96, GREENBG, GREEN, 2,
           6)
    cy2 = fy - 54
    s.line(cz0 + 6, cy2, cz1 - 6, cy2, STEEL, 2.4, marker=ar)
    s.line(cz1 - 6, cy2, cz0 + 6, cy2, STEEL, 2.4, marker=ar)
    chip(s, (cz0 + cz1) / 2, cy2 - 52, "সামনে 1 m ফাঁকা")

    y = note_strip(s, top + ph + 30,
                   "ভেজা দেয়ালে নয়, চুলা বা সিঙ্কের উপরে নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_place.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৪. মডেল ভবনের এক-লাইন ডায়াগ্রাম
# ══════════════════════════════════════════════════════════════════════
def d04_sld():
    """এক-লাইন ডায়াগ্রাম — সার্ভিস থেকে প্রতিটি আউটগোয়িং ওয়ে।

    জোড়ার নিয়ম চিত্রের নিজের ভাষায়:  তারের সঙ্গে বারের জোড়া বোঝাতে
    ভরাট ফোঁটা;  ফোঁটা ছাড়া যেখানে তার বার পেরিয়ে গেছে, সেখানে জোড়া
    নেই।  এটি বৈদ্যুতিক নকশার প্রচলিত রীতি — না মানলে নিচের বারের
    প্রতিটি ড্রপ উপরের সব বারের সঙ্গে জোড়া বলে পড়া যায়।
    """
    s = SVG(1240, 1080)
    s.title("মডেল ভবনের এমডিবি: এক-লাইন ডায়াগ্রাম", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 12)

    def dot(x, y, col):
        s.circle(x, y, 7.5, col, "none", 0)

    cx = 250
    y = 118
    chain = [("সার্ভিস কানেকশন", 300), ("এনার্জি মিটার", 260),
             ("400 A MCCB: 4P", 300)]
    for i, (txt, w) in enumerate(chain):
        blk(s, cx, y, txt, w, 66)
        if i < len(chain) - 1:
            s.line(cx, y + 33, cx, y + 82, STEEL, SW, marker=ar)
        y += 115

    # বাসবার — পাঁচটি আড়াআড়ি পাত
    bx0, bx1 = 128, 1092
    by = y + 22
    s.rect(bx0 - 16, by - 24, bx1 - bx0 + 32, 220, "#F2F5F8", LINE, 2, 8)
    bars, cols = [], (C_L1, C_L2, C_L3, C_N, C_PE)
    for i, nm in enumerate(("L1", "L2", "L3", "N", "E")):
        yy = by + 4 + i * 42
        bar_run(s, bx0, bx1, yy, cols[i], nm, 16, bx0 - 22)
        bars.append(yy)
    s.text(bx1 + 22, by + 62, "50 × 5", T_SMALL, GREY, 700)
    s.text(bx1 + 22, by + 92, "তামা", T_SMALL, GREY, 700)

    # ইনকামিং — চার পোল, চার বারে; আর্থ বারে নয়
    for k in range(4):
        dx = cx - 48 + k * 32
        s.line(dx, y - 60, dx, bars[k], cols[k], 2.8)
        dot(dx, bars[k], cols[k])
    s.line(cx, y - 82, cx, y - 60, STEEL, SW)
    s.line(cx - 48, y - 60, cx + 48, y - 60, STEEL, SW)

    # আউটগোয়িং ওয়ে
    ways = [
        ("ফ্ল্যাট ১–৬", "40 A DP × 6", (0,), True, 6),
        ("ফ্ল্যাট ৭–১১", "40 A DP × 5", (1,), True, 5),
        ("ফ্ল্যাট ১২–১৬", "40 A DP × 5", (2,), True, 5),
        ("কমন সার্ভিস", "16 A DP × 4", (1, 2), True, 4),
        ("মোটর প্যানেল", "63 A TP", (0, 1, 2), False, 1),
        ("ফায়ার ও জেনারেটর", "25 A TP", (0, 1, 2), True, 1),
    ]
    wy = by + 306
    n = len(ways)
    step = (bx1 - bx0 - 80) / (n - 1)
    for i, (name, rating, phs, has_n, cnt) in enumerate(ways):
        wx = bx0 + 40 + i * step
        lines = list(phs) + ([3] if has_n else []) + [4]
        x0 = wx - (len(lines) - 1) * 8
        for k, bi in enumerate(lines):
            lx = x0 + k * 16
            s.line(lx, bars[bi], lx, wy - 54, cols[bi], 2.6)
            dot(lx, bars[bi], cols[bi])
        # একাধিক ব্রেকার হলে পেছনে থাক
        if cnt > 1:
            s.rect(wx - 22, wy - 42, 56, 96, "#E4E9EE", "#A9B3BE", 2, 5)
            s.rect(wx - 15, wy - 45, 56, 96, "#EDF1F5", "#A0AAB5", 2, 5)
        mcb(s, wx, wy, 56, 96)
        s.text(wx, wy + 78, rating, T_TINY, STEEL, 700, "middle")
        for j, ln in enumerate(wrap(name, 178, T_SMALL, 700)):
            s.text(wx, wy + 114 + j * 26, ln, T_SMALL, NAVY, 700, "middle")
        s.line(wx, wy + 48, wx, wy + 62, STEEL, 2.4)

    # আর্থ ইলেকট্রোড — বারের বাঁ প্রান্ত থেকে নেমে মাটির প্রতীকে
    # প্রতীকটি বারের বাঁ প্রান্ত থেকে নেমে **প্যানেলের বাইরে** সরে
    # যায়।  সোজা নিচে নামালে মাটির তিনটি পাত প্রথম আউটগোয়িং
    # ব্রেকারের গায়ে পড়ত — qc এটি ধরে না, কারণ পাতগুলো লেখা নয়
    tx0 = bx0 + 6
    ex, ey0 = 74, bars[4] + 110
    s.line(tx0, bars[4], tx0, bars[4] + 44, C_PE, 3)
    s.line(tx0, bars[4] + 44, ex, bars[4] + 44, C_PE, 3)
    s.line(ex, bars[4] + 44, ex, ey0, C_PE, 3)
    dot(tx0, bars[4], C_PE)
    for k, hw in enumerate((30, 20, 10)):
        s.line(ex - hw, ey0 + 6 + k * 12, ex + hw, ey0 + 6 + k * 12,
               C_PE, 3.4)

    y2 = note_strip(s, wy + 190,
                    "ভরাট ফোঁটা মানে জোড়া; ফোঁটা ছাড়া ক্রসিংয়ে জোড়া নেই",
                    pad=40)
    s.fit(y2, 24)
    return s.save(f"{OUT}/d04_sld.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৫. ফেজ ভারসাম্য
# ══════════════════════════════════════════════════════════════════════
def d05_balance():
    """তিন ফেজে লোড ভাগ — আগে ও পরে।"""
    s = SVG(1240, 840)
    s.title("তিন ফেজে লোড ভাগ", T_TITLE)

    pw, gap = 570, 44
    x0 = (1240 - (2 * pw + gap)) / 2
    ph = 520
    top = 100
    scenes = [
        ("ভুল ভাগ", [(96.0, C_L1), (43.2, C_L2), (23.6, C_L3)], REDBG, RED),
        ("ঠিক ভাগ", [(55.5, C_L1), (53.7, C_L2), (53.7, C_L3)],
         GREENBG, GREEN),
    ]
    for k, (head, vals, bg, edge) in enumerate(scenes):
        x = x0 + k * (pw + gap)
        panel(s, x, top, pw, ph, head, edge)
        base = top + ph - 104
        s.rect(x + 16, top + 66, pw - 32, base - top - 66,
               bg, "none", 0, 8)
        maxv = 100.0
        for i, (v, col) in enumerate(vals):
            bx = x + 155 + i * 130
            hgt = (v / maxv) * 236
            s.rect(bx - 44, base - hgt, 88, hgt, col, "#00000022", 1.4, 5)
            s.text(bx, base - hgt - 14, f"{v:.1f}", T_SMALL, NAVY, 700,
                   "middle")
            s.text(bx, base + 32, ("L1", "L2", "L3")[i], T_BODY, NAVY, 700,
                   "middle")
        s.line(x + 34, base, x + pw - 34, base, GREY, 2)
        s.text(x + pw / 2, base + 74, "কিলোওয়াট", T_SMALL, GREY, 700,
               "middle")

    y = note_strip(s, top + ph + 30,
                   "নিউট্রালে কারেন্ট কমে, বার তিনটিই সমান গরম হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_balance.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৬. ভোল্টেজ ড্রপের বাজেট
# ══════════════════════════════════════════════════════════════════════
def d06_budget():
    """এমডিবি থেকে শেষ বাতি — ২.৫ শতাংশ তিন ভাগে ভাগ।"""
    s = SVG(1240, 700)
    s.title("ভোল্টেজ ড্রপের বাজেট: এমডিবি থেকে শেষ বাতি", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 12)

    nodes = [("MDB", 150), ("ফ্ল্যাটের ডিবি", 620), ("শেষ বাতি", 1090)]
    ny = 190
    for name, x in nodes:
        blk(s, x, ny, name, tw(name, T_BODY, 700) + 54, 66)

    legs = [(150, 620, "ফিডারের ভাগ", "1.31 %", C_L1),
            (620, 1090, "ফাইনাল সার্কিটের ভাগ", "1.19 %", C_L3)]
    for x0, x1, nm, pct, col in legs:
        s.line(x0 + 96, ny, x1 - 96, ny, STEEL, SW, marker=ar)
        s.text((x0 + x1) / 2, ny - 26, nm, T_SMALL, GREY, 700, "middle")
        s.text((x0 + x1) / 2, ny + 44, pct, T_NAME, col, 700, "middle")

    # বাজেটের পটি
    ty, th = 330, 66
    tx0, tx1 = 150, 1090
    s.rect(tx0, ty, tx1 - tx0, th, "#F2F5F8", LINE, 2, 8)
    segs = [(1.31, C_L1, "1.31"), (1.19, C_L3, "1.19")]
    total = 2.50
    x = tx0
    for v, col, lab in segs:
        w = (v / total) * (tx1 - tx0)
        s.rect(x, ty, w, th, col, "#00000022", 1.4, 0)
        if lab:
            s.text(x + w / 2, ty + th / 2 + 8, lab + " %", T_BODY,
                   "#FFFFFF", 700, "middle")
        x += w
    s.text(tx0, ty - 18, "0 %", T_SMALL, GREY, 700)
    s.text(tx1, ty - 18, "2.50 %", T_SMALL, GREY, 700, "end")
    s.text((tx0 + tx1) / 2, ty + th + 40,
           "দুই ভাগ মিলে 2.50 %, যা BNBC-র সীমা", T_NAME, NAVY, 700,
           "middle")

    y = note_strip(s, ty + th + 76,
                   "সীমাটি গোটা পথের, একটি টুকরোর নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_budget.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৭. গ্ল্যান্ড প্লেট
# ══════════════════════════════════════════════════════════════════════
def d07_gland():
    """ক্যাবল কীভাবে বাক্সে ঢোকে — গ্ল্যান্ড, লকনাট, ফাঁকা ছিদ্র বন্ধ।"""
    s = SVG(1240, 700)
    s.title("ক্যাবল বাক্সে ঢোকানো: গ্ল্যান্ড প্লেট", T_TITLE)

    px, py, pw, ph = 300, 150, 640, 220
    s.rect(px, py, pw, ph, "#E9EDF2", "#8E99A6", 3, 8)
    s.rect(px + 18, py + 18, pw - 36, ph - 36, "#F7F9FB", "#AEB8C2", 2, 5)

    # তিনটি অবস্থা: গ্ল্যান্ডসহ · ফাঁকা ছিদ্র বন্ধ · ভুল (খোলা ছিদ্র)
    slots = [(px + 130, "গ্ল্যান্ড", True, False),
             (px + 320, "ব্লকিং প্লাগ", False, False),
             (px + 510, "খোলা ছিদ্র", False, True)]
    for sx, name, gland, open_ in slots:
        s.circle(sx, py + ph / 2, 46, "#FFFFFF", "#8E99A6", 2.4)
        if gland:
            import math as _m
            cy0 = py + ph / 2
            hexp = [(sx + 42 * _m.cos(_m.pi / 6 + k * _m.pi / 3),
                     cy0 + 42 * _m.sin(_m.pi / 6 + k * _m.pi / 3))
                    for k in range(6)]
            s.poly(hexp, "#C7CDD4", "#6C7885", 2.4)
            s.circle(sx, cy0, 30, "#DDE4EA", "#8E99A6", 2.2)
            s.circle(sx, cy0, 22, "#2A2E33", "#0B0D0F", 2.4)
            s.circle(sx, cy0, 12, "#4C545C", "none", 0)
        elif open_:
            s.circle(sx, py + ph / 2, 38, "#2A2E33", "none", 0)
            s.circle(sx, py + ph / 2, 38, "none", RED, 3.4)
        else:
            s.circle(sx, py + ph / 2, 38, "#DDE4EA", "#8E99A6", 2.4)
            s.circle(sx, py + ph / 2, 16, "#C7CDD4", "#8E99A6", 1.8)
        s.text(sx, py + ph + 44, name, T_BODY, NAVY, 700, "middle")

    s.text(px + 510, py + ph + 78, "চলবে না", T_SMALL, RED, 700, "middle")
    s.text(px - 24, py + ph / 2 + 8, "গ্ল্যান্ড প্লেট", T_CALL, NAVY, 700,
           "end")

    y = note_strip(s, py + ph + 130,
                   "খোলা ছিদ্র মানে ইঁদুর, ধুলো আর আঙুল ঢোকার পথ")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_gland.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৮. তার সাজানো — ভুল ও ঠিক
# ══════════════════════════════════════════════════════════════════════
def d08_route():
    """বোর্ডের ভেতরে তার সাজানোর দুই চেহারা।"""
    s = SVG(1240, 720)
    s.title("বোর্ডের ভেতরে তার সাজানো", T_TITLE)

    pw, gap = 570, 44
    x0 = (1240 - (2 * pw + gap)) / 2
    ph = 430
    top = 100

    for k, head in enumerate(("এলোমেলো", "সাজানো")):
        x = x0 + k * (pw + gap)
        edge = RED if k == 0 else GREEN
        panel(s, x, top, pw, ph, head, edge)
        ix, iy, iw2, ih2 = x + 40, top + 84, pw - 80, ph - 130
        s.rect(ix, iy, iw2, ih2, "#FBFCFD", LINE, 1.8, 6)
        # উপরের সারিতে ব্রেকার
        for i in range(6):
            mcb(s, ix + 44 + i * 64, iy + 62, 44, 84)
        # নিচে টার্মিনাল বার
        by2 = iy + ih2 - 46
        bar_run(s, ix + 24, ix + iw2 - 24, by2, C_N, None, 14)
        if k == 0:
            # আঁকাবাঁকা, একে অন্যকে কেটে
            pts = [(0, 3), (1, 5), (2, 0), (3, 4), (4, 1), (5, 2)]
            for a, b in pts:
                sx = ix + 44 + a * 64
                ex = ix + 32 + b * 64
                s.path(f"M {sx} {iy + 108} C {sx} {iy + 190}, "
                       f"{ex} {iy + 150}, {ex} {by2 - 8}", C_N, 2.6)
        else:
            # খাড়া নেমে, একটি আড়াআড়ি লেনে, তারপর নিজের বোল্টে
            lane = iy + 176
            for a in range(6):
                sx = ix + 44 + a * 64
                ex = ix + 32 + a * 64
                s.path(f"M {sx} {iy + 108} L {sx} {lane} L {ex} {lane} "
                       f"L {ex} {by2 - 8}", C_N, 2.6)
            s.rect(ix + 16, lane - 16, iw2 - 32, 32, "none", STEEL, 2,
                   6)
            # নাম লেনের ভেতরেই, শেষ তারের ডানে; কোনো তার একে কাটে না
            s.text(ix + iw2 - 22, lane + 8, "তারের লেন", T_SMALL, STEEL,
                   700, "end")

    y = note_strip(s, top + ph + 30,
                   "যন্ত্রের ক্রমেই তার; অকারণে একটি আরেকটিকে কাটবে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d08_route.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৯. ওয়্যারিংয়ের ধাপ
# ══════════════════════════════════════════════════════════════════════
def d09_steps():
    """এমডিবি ওয়্যারিংয়ের আটটি ধাপ, ক্রমে।"""
    s = SVG(1240, 820)
    s.title("এমডিবি ওয়্যারিংয়ের ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 12)

    steps = ["বাক্স বসানো", "গ্ল্যান্ড ও ক্যাবল", "বাসবার ও ইনসুলেটর",
             "মেইন ব্রেকার", "আউটগোয়িং ব্রেকার", "প্রান্ত ও লাগ",
             "নম্বর ও লেবেল", "পরীক্ষা ও চালু"]
    cols, top = 4, 118
    cw, chh, gx, gy = 262, 130, 24, 96
    x0 = (1240 - (cols * cw + (cols - 1) * gx)) / 2
    for i, txt in enumerate(steps):
        r, c = divmod(i, cols)
        # সাপের মতো — দ্বিতীয় সারি ডান থেকে বাঁয়ে
        if r % 2:
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
    # তীর
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
                   "সাত নম্বর ধাপ বাদ দিলে আট নম্বরটি করা যায় না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d09_steps.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১০. চালু করার আগে
# ══════════════════════════════════════════════════════════════════════
def d10_test():
    """চালু করার আগের পাঁচটি পরীক্ষা, ক্রমে।"""
    s = SVG(1240, 700)
    s.title("চালু করার আগে: পাঁচটি পরীক্ষা", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 12)

    items = [("চোখে দেখা", "আলগা বোল্ট, খোলা ছিদ্র"),
             ("কন্টিনিউইটি", "প্রতিটি ইসিসি বারে পৌঁছেছে"),
             ("ইনসুলেশন", "500 V মেগারে, বোর্ড বিচ্ছিন্ন"),
             ("পোলারিটি", "ফেজ ব্রেকারে, নিউট্রাল বারে"),
             ("আর্থ রেজিস্ট্যান্স", "লিড 1 ওহমের নিচে")]
    top = 120
    bw, bh, gap = 214, 200, 22
    x0 = (1240 - (5 * bw + 4 * gap)) / 2
    for i, (name, sub) in enumerate(items):
        x = x0 + i * (bw + gap)
        s.rect(x, top, bw, bh, "#FBFCFD", STEEL, 2.6, 12)
        s.badge(x + bw / 2, top + 44, "12345"[i], 24, NAVY, size=21)
        for j, ln in enumerate(wrap(name, bw - 26, T_BODY, 700)):
            s.text(x + bw / 2, top + 100 + j * 28, ln, T_BODY, NAVY, 700,
                   "middle")
        for j, ln in enumerate(wrap(sub, bw - 24, T_SMALL, 400)):
            s.text(x + bw / 2, top + 150 + j * 25, ln, T_SMALL, GREY, 400,
                   "middle")
        if i:
            s.line(x - gap - 2, top + bh / 2, x - 6, top + bh / 2, STEEL,
                   3, marker=ar)

    s.rect(x0, top + bh + 46, 5 * bw + 4 * gap, 74, GREENBG, GREEN, 2.4, 12)
    s.text(620, top + bh + 92, "পাঁচটিই পাশ করলে তবেই মেইন ব্রেকার চালু",
           T_NAME, GREEN, 700, "middle")

    y = note_strip(s, top + bh + 146,
                   "কাগজে লিখে রাখা: কে, কবে, কী পেয়েছিল")
    s.fit(y, 24)
    return s.save(f"{OUT}/d10_test.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১১. নকশার প্রতীক
# ══════════════════════════════════════════════════════════════════════
def d11_symbols():
    """BNBC সারণি ৮.১.১৫-এর বোর্ড-প্রতীক, হুবহু।

    প্রতীকগুলো মূল পিডিএফের (law.resource.org) সারণি ৮.১.১৫ থেকে
    ৪২০ dpi-তে দেখে নতুন করে আঁকা — অনুমান করে নয়।  ছ'টির পার্থক্য
    সূক্ষ্ম, তাই ভুল হলে চোখে পড়ে না:
        MDB  আড়াআড়ি ক্রস, বাঁ ও ডান ত্রিভুজ ভরাট
        FDB  ক্রস, সঙ্গে খাড়া মাঝরেখা
        DB   কেবল ক্রস
        SDB  একটি কর্ণ
        BDB  একটি কর্ণ, নিচের ত্রিভুজ ভরাট
        SB   ছোট ভরাট আয়ত, ইটের মতো হ্যাচ
    """
    s = SVG(1240, 600)
    s.title("নকশার কাগজে বোর্ডের প্রতীক", T_TITLE)

    items = [("MDB", "মেইন"), ("FDB", "ফ্লোর"), ("DB", "সাধারণ"),
             ("SDB", "সাব"), ("BDB", "শাখা"), ("SB", "সুইচবোর্ড")]
    top = 118
    bw, bh, gap = 178, 232, 20
    x0 = (1240 - (6 * bw + 5 * gap)) / 2
    for i, (code, name) in enumerate(items):
        x = x0 + i * (bw + gap)
        s.rect(x, top, bw, bh, PLATE, LINE, 1.8, 10)
        sw2 = bw - 62
        sh2 = sw2 / 2.4
        sx, sy = x + 31, top + 46
        x1, y1 = sx + sw2, sy + sh2
        if code == "SB":
            # ছোট আয়ত, ইটের মতো সাদা দাগ
            bw3, bh3 = sw2 * 0.72, sh2 * 0.60
            bx3 = x + bw / 2 - bw3 / 2
            by3 = sy + (sh2 - bh3) / 2
            s.rect(bx3, by3, bw3, bh3, SYM, SYM, 2, 0)
            rows = 3
            for r in range(rows):
                yy = by3 + bh3 * (r + 0.5) / rows
                off = 0 if r % 2 else bw3 / 12
                for c in range(6):
                    xx = bx3 + 3 + off + c * (bw3 - 6) / 6
                    s.rect(xx, yy - 2.2, (bw3 - 6) / 12, 4.4, "#FFFFFF",
                           "none", 0, 0)
        else:
            if code == "MDB":
                s.poly([(sx, sy), (sx + sw2 / 2, sy + sh2 / 2), (sx, y1)],
                       SYM, SYM, 1)
                s.poly([(x1, sy), (sx + sw2 / 2, sy + sh2 / 2), (x1, y1)],
                       SYM, SYM, 1)
            if code == "BDB":
                s.poly([(sx, y1), (x1, sy), (x1, y1)], SYM, SYM, 1)
            s.rect(sx, sy, sw2, sh2, "none", SYM, 3.2, 0)
            if code in ("MDB", "FDB", "DB"):
                s.line(sx, sy, x1, y1, SYM, 2.6)
                s.line(sx, y1, x1, sy, SYM, 2.6)
            else:
                s.line(sx, y1, x1, sy, SYM, 2.6)
            if code == "FDB":
                s.line(sx + sw2 / 2, sy, sx + sw2 / 2, y1, SYM, 2.6)
        s.text(x + bw / 2, top + 158, code, T_NODE, NAVY, 700, "middle")
        s.text(x + bw / 2, top + 196, name, T_SMALL, GREY, 700, "middle")

    y = note_strip(s, top + bh + 40,
                   "ছ'টি প্রতীকের পার্থক্য সূক্ষ্ম; কর্ণ, ক্রস আর ভরাট")
    s.fit(y, 24)
    return s.save(f"{OUT}/d11_symbols.svg")


# ══════════════════════════════════════════════════════════════════════
#  আলোকচিত্র-ভিত্তিক ছবি
# ══════════════════════════════════════════════════════════════════════
def d12_real():
    """সম্পূর্ণ একটি এমডিবি — ভেতরের প্রতিটি ঘর চিহ্নিত।

    কল-আউটের ডগাগুলো ছবির পিক্সেল থেকে বেছে নেওয়া (রঙের মাস্ক →
    বারবার ক্ষয় → অঞ্চলের গভীরতম বিন্দু → ৯×৯ প্যাচের গড় রং মিলিয়ে
    যাচাই), চোখে আন্দাজ করে নয় — অধ্যায় ২৩-এর শিক্ষা।
    """
    return photo_callouts(
        "d12_real", "বাস্তব এমডিবি: কোথায় কী", "ph_done.jpg",
        left=[("ধাতব এনক্লোজার", 0.093, 0.093),
              ("ডিন রেল", 0.276, 0.177),
              ("আউটগোয়িং ব্রেকার", 0.271, 0.560),
              ("আর্থিং বার", 0.320, 0.815),
              ("নিউট্রাল বার", 0.330, 0.938)],
        right=[("কনডুইট প্রবেশ", 0.790, 0.021),
               ("ডেড-ফ্রন্ট ঢাকনা", 0.714, 0.155),
               ("হিঞ্জ দরজা", 0.865, 0.254),
               ("স্বচ্ছ ঢাকনা", 0.640, 0.888)],
        note="সামনে থেকে কোনো লাইভ অংশে আঙুল পৌঁছায় না",
        iw=580, w=1240, size=T_CALL)


def d13_bars():
    """বাসবার চেম্বার — দুই বার, ইনসুলেটর, বোল্টের সারি।"""
    return photo_callouts(
        "d13_bars", "নিউট্রাল ও আর্থিং বার", "ph_bars.jpg",
        left=[("এমসিবির সারি", 0.320, 0.035),
              ("আর্থিং বার", 0.714, 0.262),
              ("ইনসুলেটর", 0.128, 0.492),
              ("ফেলে রাখা যন্ত্রপাতি", 0.280, 0.730)],
        right=[("ডিন রেল", 0.300, 0.380),
               ("টার্মিনাল ব্লক", 0.626, 0.459),
               ("নিউট্রাল বার", 0.629, 0.551)],
        note="বার দুটি আলাদা, আর আলাদাই থাকবে",
        iw=760, w=1240, size=T_CALL)


def d14_lug():
    """আর্থিং বারে ইসিসি বসানো — লাগ, বোল্ট, নম্বর।"""
    return photo_callouts(
        "d14_lug", "আর্থিং বারে ইসিসি: এক বোল্টে এক তার", "ph_lug.jpg",
        left=[("তামার আর্থিং বার", 0.302, 0.252),
              ("রিং লাগ", 0.328, 0.341),
              ("সবুজ-হলুদ ইসিসি", 0.282, 0.568)],
        right=[("আর্থের প্রতীক", 0.868, 0.300),
               ("নম্বর-চিহ্ন", 0.630, 0.660)],
        note="প্রতিটি তারের গায়ে নম্বর; নইলে পরে কেউ চিনবে না",
        iw=740, w=1240, size=T_CALL)


def d15_term():
    """প্রান্ত তৈরির দুই জিনিস — লাগ আর ফেরুল।"""
    return pair_panels(
        "d15_term", "প্রান্ত তৈরি: লাগ ও ফেরুল",
        [("লাগ", "ph_lugkind.jpg", STEEL),
         ("ফেরুল", "ph_ferrule.jpg", STEEL)],
        "মোটা তার বারে যায় লাগে, সরু তার ব্রেকারে যায় ফেরুলে",
        h=330, w=1240)


def d16_bad():
    """যেভাবে করা যাবে না — পুরনো একটি বোর্ডের ভেতর।"""
    return sheet(
        "d16_bad", "যেভাবে করা যাবে না", "পুরনো একটি বোর্ড",
        "ph_bad.jpg",
        "ক্রম নেই, নম্বর নেই, তার একে অন্যকে কেটে গেছে",
        iw=940, w=1240)


def d17_start():
    """কাজের শুরু — খালি বাক্সে ঝুলন্ত তার।"""
    return sheet(
        "d17_start", "কাজের শুরু", "খালি এনক্লোজার",
        "ph_start.jpg",
        "সব তার আগে ঢোকে, সাজানো হয় তার পরে",
        iw=740, w=1240)


def d18_meter():
    """মিটার আর তার পরের ব্রেকার।"""
    return photo_callouts(
        "d18_meter", "মিটার ও তার পরের ব্রেকার", "ph_meter.jpg",
        left=[("এনার্জি মিটার", 0.300, 0.270),
              ("সিলের তার", 0.145, 0.665)],
        right=[("ডিপি ব্রেকার", 0.660, 0.320),
               ("ডিন রেল", 0.880, 0.455),
               ("মিটারের টার্মিনাল", 0.460, 0.660)],
        note="মিটারের সিল ভাঙার অধিকার শুধু বিতরণ কোম্পানির",
        iw=520, w=1240, size=T_CALL)


def d19_tree_src():
    """ইনস্টিটিউটের নিজের ছকে গোটা বিতরণ-শৃঙ্খল।"""
    return sheet(
        "d19_tree_src", "সার্ভিস থেকে শেষ বাতি পর্যন্ত",
        "ইনস্টিটিউটের সংযোগ-ছক", "h30_tree.png",
        "মিটারের পরেই মেইন ব্রেকার, তারপর ভাগ",
        iw=1160, w=1240)


ALL = [d01_tree, d02_inside, d03_place, d04_sld, d05_balance, d06_budget,
       d07_gland, d08_route, d09_steps, d10_test, d11_symbols,
       d12_real, d13_bars, d14_lug, d15_term, d16_bad, d17_start,
       d18_meter, d19_tree_src,
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
