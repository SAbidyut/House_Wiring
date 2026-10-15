# -*- coding: utf-8 -*-
"""অধ্যায় ২০ — ফ্লোট সুইচ : ডায়াগ্রাম।

সার্কিট ও কানেকশন ডায়াগ্রাম ইনস্টিটিউটের নিজের ডেক থেকে হুবহু বসানো —
`HW Connection Diagram All.pptx` স্লাইড ২৫–২৮ (`assets_ch20.py`)।  হাতে
নতুন করে আঁকা হয়নি, কারণ হাতে আঁকলেই টপোলজি বদলে যাওয়ার ঝুঁকি
(অধ্যায় ৬-এর অভিজ্ঞতা)।

আলোকচিত্র উইকিমিডিয়া কমন্স থেকে।  যেটা কেটে খোলা সুইচের ভেতর দেখায়,
সেটাই এই অধ্যায়ের প্রধান ছবি — ইস্পাতের বল, লিভার আর মাইক্রোসুইচ,
তিনটিই এক ফ্রেমে।

যা সোর্সে নেই — ঘরের পানির ব্যবস্থায় সুইচটা কোথায় বসে, ভাসা-ডোবার
সঙ্গে কোন কন্টাক্ট বদলায়, মাল্টিমিটার দিয়ে COM চেনার নিয়ম, আর ডাবল
কন্ডিশনের দুই ট্যাংক — এগুলো নতুন আঁকা।

লেবেলের নিয়ম (অধ্যায় ১৫ থেকে কড়া):  প্যানেলের শিরোনাম বিশেষ্য,
যন্ত্রাংশের লেবেল এক-দুই শব্দ, নিচে এক লাইনের একটি নোট-পটি।  কারণ,
পরামর্শ ও সতর্কবাণী সবই বইয়ের লেখায় — ছবিতে নয়।

কালপুরুষে `Ω`, `∞`, `°` নেই — তাই কন্টিনিউইটির ফল লেখা হয়েছে
"বিপ" আর "নীরব" বলে, রোধের মান দিয়ে নয়।  `÷` কালপুরুষে `+` হয়ে
আঁকে, তাই ছবির লেবেলেও কখনো নয়।
"""
import os

from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch20")
IMG = os.path.join(HERE, "assets", "ch20")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 23.5
T_SMALL = 23
T_CALL = 24
T_TINY = 22

SYM = "#12324D"
SW = 3.4
LIVE = "#D42A1F"
NEUT = "#1F2933"
EARTH = "#1B6E47"
WATER = "#BFDCEF"
WATER_E = "#5E9EC8"
BOXG = "#E7ECF1"
METAL = "#8D9AA8"
PLATE = "#F4F7FA"
DEAD = "#9AA6B2"
FLOATC = "#F2C230"          # ফ্লোটের খোলস — বাজারে হলুদই বেশি


# ── shared helpers ──────────────────────────────────────────────────────
def panel(s, x, y, w, h, title, col=STEEL):
    """প্যানেলের শিরোনাম — কেবল নাম, কোনো মন্তব্য নয়।"""
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def note_strip(s, y, text, x=46, w=1148, fill="#EAF2FA", stroke=STEEL,
               tcolor=NAVY, size=T_NAME):
    """এক লাইনের তথ্য-পটি।  দুই লাইনে গড়ালে লেখাটা ছোট করতে হবে —
    ছবির নিচে অনুচ্ছেদ বসানো এই বইয়ের নিয়ম নয়।"""
    if tw(text, size, 700) > w - 60:
        raise ValueError(f"note_strip এক লাইনে ধরে না: {text!r}")
    s.rect(x, y, w, 58, fill, stroke, 2, 11)
    s.text(x + w / 2, y + 36, text, size, tcolor, 700, "middle")
    return y + 58


def callout(s, x, y, text, tx, ty, anchor="end", size=T_CALL, col=NAVY):
    """লেবেল ও লিডার — লেখার যে পাশে লক্ষ্য, সেই কিনারা থেকেই বেরোয়।"""
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    w = tw(text, size, 700)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle"
                                      else x - w)
    x1 = x0 + w
    start = x1 + 10 if tx > x1 else x0 - 10
    s.path(f"M {start} {y} L {tx} {ty}", STEEL, 2.2)
    s.circle(tx, ty, 5, STEEL)


def img_panel(s, x, y, w, h, title, img, col=STEEL):
    panel(s, x, y, w, h, title, col)
    s.image_fit(x + 16, y + 64, w - 32, h - 78, f"{IMG}/{img}", 6)


def photo_callouts(fname, title, img, left, right, note,
                   iw=430, top=104, gap=36, size=T_CALL, w=1240):
    """একটি আলোকচিত্র মাঝখানে, দুই পাশে লেবেল ও লিডার।

    অধ্যায় ১৯-এ শেখা তিনটি ফাঁদ এখানেই বাঁধা আছে:  (ক) ছবিটা আগে আঁকো,
    লিডার পরে — উল্টো করলে ছবিই লিডার ঢেকে দেয়;  (খ) লিডারের ডগা
    ছাপা লেখার পাশে রাখো, লেখার উপরে নয়;  (গ) প্রতিটি লেবেল তার
    নিজের লক্ষ্যের সমান উচ্চতায় বসে, নইলে একটি লিডার গোটা ছবি
    কোনাকুনি চিরে যায়।
    """
    from PIL import Image as _Im
    with _Im.open(f"{IMG}/{img}") as im:
        pw, ph = im.size
    ih = round(iw * ph / pw)
    ix = (w - iw) / 2
    s = SVG(w, top + ih + 130)
    s.title(title, T_TITLE)

    def place(items, side):
        if not items:
            return
        minsep = size * 2.0
        ys = [top + fy * ih for (_t, _fx, fy) in items]
        for i in range(1, len(ys)):
            ys[i] = max(ys[i], ys[i - 1] + minsep)
        over = ys[-1] - (top + ih - 12)
        if over > 0:
            ys = [y - over for y in ys]
        under = (top + 12) - ys[0]
        if under > 0:
            ys = [y + under for y in ys]
        for (text, fx, fy), ly in zip(items, ys):
            tx, ty = ix + fx * iw, top + fy * ih
            if side == "left":
                callout(s, ix - gap, ly, text, tx, ty, "end", size)
            else:
                callout(s, ix + iw + gap, ly, text, tx, ty, "start", size)

    s.image(ix, top, iw, ih, f"{IMG}/{img}")
    place(left, "left")
    place(right, "right")
    y = note_strip(s, top + ih + 30, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def two_panel(fname, title, left, right, note, pw=560, gap=28, top=96,
              lcol=STEEL, rcol=GREEN, rw=None, ph=None):
    """দুই ছবির শিট — বাঁয়ে-ডানে দুটি প্যানেল, নিচে এক লাইনের নোট।"""
    from PIL import Image as _Im
    rw = rw or pw
    if ph is None:
        hs = []
        for w_, (_h, img) in ((pw, left), (rw, right)):
            with _Im.open(f"{IMG}/{img}") as im:
                iw_, ih_ = im.size
            hs.append(round((w_ - 32) * ih_ / iw_) + 78)
        ph = max(hs)
    s = SVG(1240, top + ph + 112)
    s.title(title, T_TITLE)
    total = pw + gap + rw
    x0 = (1240 - total) / 2
    img_panel(s, x0, top, pw, ph, left[0], left[1], lcol)
    img_panel(s, x0 + pw + gap, top, rw, ph, right[0], right[1], rcol)
    y = note_strip(s, top + ph + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


# ── circuit / block helpers ─────────────────────────────────────────────
def node(s, x, y, col=SYM, r=6.5):
    s.circle(x, y, r, col)


def blk(s, cx, cy, text, w=None, h=64, fill="#FFFFFF", stroke=STEEL,
        size=T_BODY, tcol=NAVY, sw=2.6):
    w = w or tw(text, size, 700) + 46
    x, y = cx - w / 2, cy - h / 2
    s.rect(x, y, w, h, fill, stroke, sw, 10)
    s.text(cx, cy + size * 0.34, text, size, tcol, 700, "middle")
    return x, y, w, h


def chip(s, cx, cy, text, fill=LIGHT, stroke=STEEL, tcol=NAVY,
         size=T_SMALL):
    w = tw(text, size, 700) + 30
    s.rect(cx - w / 2, cy - 19, w, 38, fill, stroke, 2, 19)
    s.text(cx, cy + size * 0.34, text, size, tcol, 700, "middle")
    return w


def ground_hatch(s, y, x0, x1, col=GREY):
    """মাটির রেখা ও তার নিচের তির্যক দাগ।"""
    s.line(x0, y, x1, y, col, 3.2)
    x = x0 + 12
    while x < x1:
        s.path(f"M {x} {y} L {x - 14} {y + 16}", col, 2.0)
        x += 26


def water(s, x, y, w, h):
    s.rect(x, y, w, h, WATER, WATER_E, 2.2, 0)


def float_body(s, cx, cy, ang=0.0, r=26):
    """ফ্লোটের খোলস — কাত হলে ang ডিগ্রি ঘোরে (কেবল-ফ্লোট)।"""
    s.ellipse(cx, cy, r * 1.15, r * 0.86, FLOATC, "#8A6D14", 2.6)


def micro_contact(s, x, y, closed_nc, wlen=150):
    """ছোট কন্টাক্ট-চিত্র:  COM থেকে লিভার, উপরে NC নিচে NO।

    যেটি বন্ধ, সেটিতেই লিভার ঠেকে থাকে; অন্যটি ধূসর।
    """
    s.text(x - 14, y + 7, "COM", T_SMALL, NAVY, 700, "end")
    node(s, x, y)
    ty, by = y - 46, y + 46
    tip = (x + wlen * 0.78, ty if closed_nc else by)
    s.path(f"M {x} {y} L {tip[0]:.0f} {tip[1]:.0f}",
           LIVE if closed_nc else DEAD, 3.6)
    for yy, name, on in ((ty, "NC", closed_nc), (by, "NO", not closed_nc)):
        col = LIVE if on else DEAD
        node(s, x + wlen * 0.78, yy, col, 6)
        s.path(f"M {x + wlen * 0.78:.0f} {yy} L {x + wlen:.0f} {yy}", col, 3.2)
        s.text(x + wlen + 12, yy + 7, name, T_SMALL, col, 700, "start")


# ── ১. ঘরের পানির ব্যবস্থায় ফ্লোট সুইচ ─────────────────────────────────
def d01_system():
    """পাম্প, রিজার্ভার, ছাদের ট্যাংক আর ডিবি — একই ছবিতে।

    তারের পথগুলো হিসাব করে বসানো, যাতে কোনোটাই আরেকটাকে না কাটে:
    সাপ্লাই পাইপ ওঠে x = ২৫০ বরাবর, কন্ট্রোল কেবল নামে x = ৬৯০ বরাবর,
    আর পাম্পের পাওয়ার কেবল যায় y = ৪৯০ বরাবর — তিনটির কোনো মিল নেই।
    """
    s = SVG(1240, 780)
    s.title("ঘরের পানির ব্যবস্থায় ফ্লোট সুইচ", T_TITLE)

    # ছাদের ট্যাংক ও তার পায়া
    s.rect(700, 128, 450, 140, "#FFFFFF", NAVY, 3.0, 6)
    water(s, 704, 200, 442, 64)
    s.text(990, 172, "ছাদের ট্যাংক", T_NAME, NAVY, 700, "middle")
    for lx in (740, 1110):
        s.path(f"M {lx} 268 L {lx} 470", METAL, 5.0)
    s.path("M 700 268 L 1150 268", METAL, 5.0)

    # সাপ্লাই পাইপ:  পাম্প → উপরে → ট্যাংকের মাথা
    s.path("M 200 367 L 200 84 L 940 84 L 940 128", WATER_E, 5.0)
    s.text(222, 240, "সাপ্লাই পাইপ", T_BODY, WATER_E, 700, "start")

    # ফ্লোট সুইচ ট্যাংকের ভেতর
    s.rect(757, 137, 26, 26, METAL, GREY, 2, 4)
    s.path("M 770 163 L 850 214", "#3B3B3B", 3.0)
    float_body(s, 866, 224, r=22)
    s.text(1010, 232, "ফ্লোট সুইচ", T_BODY, NAVY, 700, "middle")

    # কন্ট্রোল কেবল:  ট্যাংক → ডিবি
    s.path("M 700 150 L 610 150 L 610 320", "#3B3B3B", 3.0, dash="10 7")
    s.text(598, 240, "কন্ট্রোল কেবল", T_BODY, GREY, 700, "end")

    # ডিবি
    s.rect(520, 320, 180, 140, PLATE, NAVY, 2.8, 8)
    s.text(610, 358, "DB", T_NAME, NAVY, 700, "middle")
    chip(s, 610, 398, "MCB")
    chip(s, 610, 438, "MC")

    # ডিবি → পাম্প (পাওয়ার কেবল)
    s.path("M 520 396 L 318 396", NEUT, 3.2)
    s.text(419, 368, "পাওয়ার কেবল", T_BODY, GREY, 700, "middle")

    # পাম্প
    blk(s, 230, 396, "পাম্প", 176, 58, "#FFFFFF", STEEL, T_NAME, STEEL, 3.0)

    # মাটি ও রিজার্ভার
    ground_hatch(s, 470, 40, 1200)
    s.rect(80, 490, 300, 150, "#FFFFFF", NAVY, 2.8, 4)
    water(s, 84, 552, 292, 84)
    s.text(230, 672, "আন্ডারগ্রাউন্ড রিজার্ভার", T_BODY, NAVY, 700, "middle")
    s.path("M 280 425 L 280 490", WATER_E, 5.0)

    y = note_strip(s, 700, "ফ্লোট সুইচ চালায় কয়েল; পাম্পের কারেন্ট "
                           "যায় কন্টাক্টরের ভেতর দিয়ে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_system.svg")


# ── ২. বাইরের অংশ ───────────────────────────────────────────────────────
def d02_parts():
    return photo_callouts(
        "d02_parts", "কেবল-ফ্লোট সুইচের অংশ", "ph_cable.jpg",
        left=[("ফ্লোট বডি", 0.18, 0.66), ("কেবলের মুখ", 0.42, 0.13)],
        right=[("কাউন্টার-ওয়েট", 0.66, 0.24), ("তিন-কোর কেবল", 0.84, 0.76)],
        note="ওজনটি যেখানে বাঁধা, ফ্লোট তার চারপাশেই ওঠানামা করে",
        iw=720)


# ── ৩. ভেতরের অংশ ───────────────────────────────────────────────────────
def d03_inside():
    return photo_callouts(
        "d03_inside", "ফ্লোট সুইচের ভেতরে", "ph_cut_on.jpg",
        left=[("কেবল", 0.14, 0.30), ("মাইক্রোসুইচ", 0.45, 0.40)],
        right=[("ইস্পাতের বল", 0.63, 0.42), ("লিভার", 0.76, 0.55)],
        note="বল গড়িয়ে লিভারকে ঠেলে, লিভার মাইক্রোসুইচের পিন চাপে",
        iw=760)


# ── ৪. দুই অবস্থা ───────────────────────────────────────────────────────
def d04_states():
    return two_panel(
        "d04_states", "কেটে খোলা সুইচ: দুই অবস্থায়",
        ("অফ অবস্থা", "ph_cut_off.jpg"),
        ("অন অবস্থা", "ph_cut_on.jpg"),
        "একই সুইচ, শুধু বলটির অবস্থান বদলেছে",
        lcol=GREY, rcol=GREEN)


# ── ৫. কাজের নীতি ───────────────────────────────────────────────────────
def d05_action():
    """পানি নিচে ও পানি উপরে — কোন কন্টাক্ট বন্ধ থাকে।"""
    s = SVG(1240, 660)
    s.title("ভাসা-ডোবার সঙ্গে কন্টাক্ট বদলায়", T_TITLE)

    PW, PH, PY = 564, 440, 96
    for i, (title_, low, col) in enumerate(
            (("পানি নিচে", True, STEEL), ("পানি উপরে", False, GREEN))):
        px = 46 + i * (PW + 20)
        panel(s, px, PY, PW, PH, title_, col)

        # ট্যাংক
        tx, ty, tw_, th = px + 46, PY + 62, PW - 92, 200
        s.rect(tx, ty, tw_, th, "#FFFFFF", NAVY, 2.6, 4)
        wh = 44 if low else 140
        water(s, tx + 3, ty + th - wh, tw_ - 6, wh - 3)

        # কেবলের বাঁধন ও ফ্লোট
        ax, ay = tx + 70, ty + 26
        s.rect(ax - 13, ay - 13, 26, 26, METAL, GREY, 2, 4)
        if low:
            s.path(f"M {ax} {ay} L {ax + 12} {ay + 118}", "#3B3B3B", 3.0)
            float_body(s, ax + 14, ay + 138)
        else:
            s.path(f"M {ax} {ay} L {ax + 118} {ay + 52}", "#3B3B3B", 3.0)
            float_body(s, ax + 142, ay + 62)

        # কোন কন্টাক্ট বন্ধ
        micro_contact(s, px + 128, PY + 352, low, 150)

    y = note_strip(s, 562, "ফ্লোট নিচে নামলে NC বন্ধ, উপরে উঠলে NO বন্ধ")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_action.svg")


# ── ৬. মাল্টিমিটারে COM চেনা ────────────────────────────────────────────
def d06_test():
    """তিন তারের কোনটি COM — কন্টিনিউইটি টেস্টে বেরিয়ে আসে।"""
    s = SVG(1240, 700)
    s.title("তিন তারের কোনটি COM", T_TITLE)

    # বাঁয়ে ফ্লোট সুইচ ও তিন তার
    fx, fy = 210, 250
    float_body(s, fx, fy, r=44)
    s.text(fx, fy + 92, "ফ্লোট সুইচ", T_BODY, NAVY, 700, "middle")
    for i, (nm, dy) in enumerate((("তার ১", -66), ("তার ২", 0),
                                  ("তার ৩", 66))):
        s.path(f"M {fx + 52} {fy} L {fx + 120} {fy + dy} "
               f"L {fx + 196} {fy + dy}", "#3B3B3B", 3.0)
        node(s, fx + 196, fy + dy)
        s.text(fx + 210, fy + dy + 7, nm, T_BODY, NAVY, 700, "start")

    # ডানে ফলের ছক।  ডান কিনারা ১১৮০ — নোট-পটির ১১৯৪ পেরোয় না।
    gx, gy, lw = 610, 148, 150
    cw, rh = 140, 62
    gw = lw + 3 * cw
    heads = ["১–২", "১–৩", "২–৩"]
    rows = [("ফ্লোট নিচে", ["বিপ", "নীরব", "নীরব"]),
            ("ফ্লোট উপরে", ["নীরব", "বিপ", "নীরব"])]
    s.rect(gx, gy, gw, rh * 3, "#FFFFFF", LINE, 2, 8)
    for c, h in enumerate(heads):
        s.text(gx + lw + c * cw + cw / 2, gy + rh * 0.64, h, T_NAME, NAVY,
               700, "middle")
    s.line(gx, gy + rh, gx + gw, gy + rh, LINE, 2)
    for r, (nm, vals) in enumerate(rows):
        ry = gy + rh * (r + 1)
        s.text(gx + lw / 2, ry + rh * 0.64, nm, T_BODY, NAVY, 700, "middle")
        for c, v in enumerate(vals):
            col = GREEN if v == "বিপ" else GREY
            s.text(gx + lw + c * cw + cw / 2, ry + rh * 0.64, v, T_BODY,
                   col, 700, "middle")
        if r:
            s.line(gx, ry, gx + gw, ry, LINE, 2)
    for c in range(4):
        s.line(gx + lw + c * cw, gy, gx + lw + c * cw, gy + rh * 3, LINE, 2)

    # ফল — বাক্য নয়, কেবল মিল
    for i, (a, b) in enumerate((("তার ১", "COM"), ("তার ২", "NC"),
                                ("তার ৩", "NO"))):
        cx = gx + 100 + i * 200
        chip(s, cx, 400, f"{a} = {b}", GREENBG, GREEN, GREEN, T_NAME)

    y = note_strip(s, 466, "মিটার বিপ মোডে; সুইচে বিদ্যুৎ থাকা অবস্থায় নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_test.svg")


# ── ৭. সরাসরি সংযোগ ─────────────────────────────────────────────────────
def d07_direct():
    """ছোট পাম্পে কন্টাক্টর ছাড়া সংযোগ — পুরো কারেন্ট সুইচের ভেতর দিয়ে।"""
    s = SVG(1240, 560)
    s.title("সরাসরি সংযোগ: ছোট পাম্পে", T_TITLE)

    LY, NY = 190, 400
    s.text(96, LY + 9, "L", T_NODE, LIVE, 700, "end")
    s.text(96, NY + 9, "N", T_NODE, NEUT, 700, "end")

    # লাইভ লাইন:  MCB → ফ্লোট সুইচ → মোটর
    s.path(f"M 112 {LY} L 300 {LY}", LIVE, SW)
    # MCB
    s.rect(300, LY - 44, 96, 88, PLATE, NAVY, 2.6, 8)
    s.text(348, LY - 56, "MCB", T_BODY, NAVY, 700, "middle")
    s.path(f"M 348 {LY - 26} L 348 {LY + 26}", NAVY, 3.0)
    s.path(f"M 396 {LY} L 560 {LY}", LIVE, SW)

    # ফ্লোট সুইচের প্রতীক
    node(s, 560, LY, LIVE)
    s.path(f"M 560 {LY} L 648 {LY - 40}", LIVE, SW)
    node(s, 664, LY, LIVE)
    s.path(f"M 664 {LY} L 880 {LY}", LIVE, SW)
    s.text(612, LY - 62, "ফ্লোট সুইচ", T_BODY, NAVY, 700, "middle")
    s.path(f"M 596 {LY + 18} L 596 {LY + 60}", "#3B3B3B", 2.6)
    float_body(s, 596, LY + 82, r=20)

    # মোটর
    s.path(f"M 880 {LY} L 880 {LY + 52}", LIVE, SW)
    s.circle(880, 295, 52, "#FFFFFF", SYM, SW)
    s.text(880, 307, "M", T_NODE, SYM, 700, "middle")
    s.text(966, 302, "পাম্প মোটর", T_BODY, NAVY, 700, "start")
    s.path(f"M 880 {295 + 52} L 880 {NY}", NEUT, SW)

    # নিউট্রাল
    s.path(f"M 112 {NY} L 1000 {NY}", NEUT, SW)
    node(s, 880, NY, NEUT)

    y = note_strip(s, 462, "পাম্পের পুরো কারেন্ট ফ্লোট সুইচের কন্টাক্টের "
                           "ভেতর দিয়েই যায়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_direct.svg")


# ── ৮. কন্টাক্টরের টার্মিনাল ────────────────────────────────────────────
def d08_contactor():
    return photo_callouts(
        "d08_contactor", "ম্যাগনেটিক কন্টাক্টরের টার্মিনাল",
        "ph_contactor.jpg",
        left=[("কয়েল A1", 0.35, 0.13), ("ইনপুট L1 L2 L3", 0.46, 0.29)],
        right=[("কয়েল A2", 0.70, 0.11), ("অক্সিলিয়ারি 13-14", 0.83, 0.27),
               ("আউটপুট T1 T2 T3", 0.62, 0.85)],
        note="ফ্লোট সুইচের তার যায় শুধু A1 আর A2-তে",
        iw=560)


# ── ৯–১০. ইনস্টিটিউটের সোর্স স্লাইড ─────────────────────────────────────
def d09_single():
    return two_panel(
        "d09_single", "সিঙ্গেল কন্ডিশন: এক ফ্লোট সুইচ",
        ("সার্কিট ডায়াগ্রাম", "h25_single_schem.png"),
        ("কানেকশন ডায়াগ্রাম", "h26_single_conn.png"),
        "MC = ম্যাগনেটিক কন্টাক্টর; A1 ও A2 তার কয়েলের দুই প্রান্ত",
        pw=574, rw=574, ph=420)


def d10_double():
    return two_panel(
        "d10_double", "ডাবল কন্ডিশন: দুই ফ্লোট সুইচ",
        ("সার্কিট ডায়াগ্রাম", "h27_double_schem.png"),
        ("কানেকশন ডায়াগ্রাম", "h28_double_conn.png"),
        "দুই সুইচ সিরিজে; দুটিই বন্ধ হলে তবেই কয়েল টান পায়",
        pw=574, rw=574, ph=420)


# ── ১১. ডাবল কন্ডিশনের দুই ট্যাংক ───────────────────────────────────────
def d11_levels():
    """কোন সুইচ কোথায় বসে আর কোন কন্টাক্ট ব্যবহার হয়।"""
    s = SVG(1240, 700)
    s.title("ডাবল কন্ডিশন: দুই ট্যাংকে দুই সুইচ", T_TITLE)

    # ছাদের ট্যাংক (ডানে, উপরে)
    s.rect(806, 108, 344, 150, "#FFFFFF", NAVY, 2.8, 5)
    water(s, 810, 190, 336, 64)
    s.text(978, 96, "ছাদের ট্যাংক", T_NAME, NAVY, 700, "middle")
    s.rect(867, 128, 22, 22, METAL, GREY, 2, 4)
    s.path("M 878 150 L 900 208", "#3B3B3B", 2.8)
    float_body(s, 916, 224, r=22)
    s.text(1132, 150, "FS-2 · com–NC", T_BODY, GREEN, 700, "end")
    s.path("M 806 262 L 1150 262", METAL, 5.0)          # ছাদ

    # রিজার্ভার (বাঁয়ে, নিচে)
    ground_hatch(s, 352, 40, 470)
    s.rect(96, 372, 320, 154, "#FFFFFF", NAVY, 2.8, 4)
    water(s, 100, 438, 312, 84)
    s.text(256, 556, "আন্ডারগ্রাউন্ড রিজার্ভার", T_NAME, NAVY, 700, "middle")
    s.rect(157, 390, 22, 22, METAL, GREY, 2, 4)
    s.path("M 168 412 L 190 458", "#3B3B3B", 2.8)
    float_body(s, 206, 472, r=22)
    s.text(96, 604, "FS-1 · com–NO", T_BODY, STEEL, 700, "start")

    # পাম্প ও পাইপ
    blk(s, 590, 316, "পাম্প", 176, 60, "#FFFFFF", STEEL, T_NAME, STEEL, 3.0)
    s.path("M 416 428 L 470 428 L 470 316 L 502 316", WATER_E, 5.0)
    s.path("M 678 316 L 730 316 L 730 148 L 806 148", WATER_E, 5.0)

    # কন্ট্রোল সার্কিট — দুই সুইচ সিরিজে
    s.rect(430, 512, 620, 108, LIGHT, STEEL, 2.2, 10)
    s.text(740, 500, "কন্ট্রোল সার্কিট", T_BODY, STEEL, 700, "middle")
    bx = 470
    s.text(bx - 12, 592, "L", T_BODY, LIVE, 700, "end")
    s.path(f"M {bx} 585 L {bx + 56} 585", LIVE, 3.0)
    for i, nm in enumerate(("FS-1", "FS-2")):
        x = bx + 56 + i * 168
        node(s, x, 585, LIVE)
        s.path(f"M {x} 585 L {x + 62} 561", LIVE, 3.0)
        node(s, x + 78, 585, LIVE)
        s.text(x + 39, 540, nm, T_TINY, NAVY, 700, "middle")
        s.path(f"M {x + 78} 585 L {x + 168} 585", LIVE, 3.0)
    s.rect(870, 561, 96, 48, "#FFFFFF", NAVY, 2.6, 8)
    s.text(918, 593, "MC", T_BODY, NAVY, 700, "middle")
    s.path("M 966 585 L 1020 585", NEUT, 3.0)
    s.text(1032, 592, "N", T_BODY, NEUT, 700, "start")

    y = note_strip(s, 640, "রিজার্ভারে পানি থাকলে আর ট্যাংক না ভরলে; "
                           "তবেই পাম্প চলে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d11_levels.svg")


# ── ১২. বাস্তবে বসানো বোর্ড ─────────────────────────────────────────────
def d12_panel():
    return photo_callouts(
        "d12_panel", "বসানো অবস্থায়: বোর্ডে কন্ট্রোলার", "ph_panel.jpg",
        left=[("MCB", 0.21, 0.44), ("ইন্ডিকেটর", 0.27, 0.90)],
        right=[("লেভেল কন্ট্রোলার", 0.63, 0.16),
               ("AUTO / MANUAL", 0.71, 0.42),
               ("কন্ট্রোল তার", 0.62, 0.80)],
        note="ম্যানুয়াল মোড থাকতেই হবে; ফ্লোট নষ্ট হলে পাম্প যেন চলে",
        iw=760)


ALL = [d01_system, d02_parts, d03_inside, d04_states, d05_action, d06_test,
       d07_direct, d08_contactor, d09_single, d10_double, d11_levels,
       d12_panel]


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
