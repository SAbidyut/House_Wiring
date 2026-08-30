# -*- coding: utf-8 -*-
"""অধ্যায় ১৯ — আইপিএস ও ইউপিএস : ডায়াগ্রাম।

এই অধ্যায়ের কোনো ছবি ইনস্টিটিউটের সোর্স ফাইলে নেই — দুই ডায়াগ্রাম ডেকের
প্রতিটি স্লাইড খুঁজে দেখা হয়েছে (`assets_ch19.py`-এর মাথায় বিস্তারিত)।
তাই আলোকচিত্র উইকিমিডিয়া কমন্স থেকে, আর সার্কিট ও ব্লক-ডায়াগ্রাম নতুন
করে আঁকা।

লেবেলের নিয়ম (অধ্যায় ১৫ থেকে কড়া, ১৮-তেও একই):  প্যানেলের শিরোনাম
বিশেষ্য, যন্ত্রাংশের লেবেল এক-দুই শব্দ, নিচে এক লাইনের একটি নোট-পটি।
কারণ, পরামর্শ ও সতর্কবাণী সবই বইয়ের লেখায় — ছবিতে নয়।

আলোকচিত্রের উপর লেবেল বসে না, বসে ছবির দুই পাশে, লিডার দিয়ে (অধ্যায় ৮-এর
`callout()`-এর ধারা) — `qc.py` ছবিকে একটি গ্রাফিক আয়তক্ষেত্র ধরে, তাই
ছবির উপরের লেখা ত্রুটি হিসেবে ধরা পড়ে।

ডিসপ্লের ছবিতে (d06) লেখা এলসিডির ভেতরে বসানো — ওটা ইচ্ছাকৃত, আর
`graphic_clashes()` পুরোপুরি বাক্সের ভেতরের লেখাকে ত্রুটি ধরে না; কেবল
কিনারায় আটকে থাকা লেখা ধরে।  তাই প্রতিটি লেখা যেন এলসিডির ফ্রেমের
ভেতরে সম্পূর্ণ থাকে।

ইংরেজি পরিভাষা (`L`, `N`, `E`, `DB`, `MCB`, `VA`, `AH`) ইচ্ছে করেই ইংরেজি —
মাঠে ওগুলোই লেখা থাকে।  কালপুরুষে `Ω`, `φ`, `°` নেই, তাই ছবির লেবেলে
ওগুলো লেখা হয়নি।
"""
import os

from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch19")
IMG = os.path.join(HERE, "assets", "ch19")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
T_CALL = 24
T_TINY = 18.5

SYM = "#12324D"
SW = 3.4
LIVE = "#D42A1F"
NEUT = "#1F2933"
EARTH = "#1B6E47"
BOXG = "#E7ECF1"
METAL = "#8D9AA8"
PLATE = "#F4F7FA"
LCDBG = "#D7E6D2"          # সবুজাভ এলসিডির কাচ
LCDINK = "#16301C"
DEAD = "#9AA6B2"


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


def photo_callouts(fname, title, img, left, right, note,
                   iw=430, top=104, gap=36, size=T_CALL, w=1240):
    """একটি আলোকচিত্র মাঝখানে, দুই পাশে লেবেল ও লিডার।

    left/right — (লেখা, লক্ষ্যের fx, লক্ষ্যের fy) এর তালিকা; fx, fy ছবির
    ভগ্নাংশে।  লেবেলগুলো নিজে নিজেই সমান দূরত্বে সাজে।
    """
    from PIL import Image as _Im
    with _Im.open(f"{IMG}/{img}") as im:
        pw, ph = im.size
    ih = round(iw * ph / pw)
    ix = (w - iw) / 2
    s = SVG(w, top + ih + 130)
    s.title(title, T_TITLE)

    def place(items, side):
        """লেবেল বসে তার নিজের লক্ষ্যের প্রায় বরাবর।

        আগে সব লেবেল ছবির উচ্চতা জুড়ে সমান ভাগে বসত।  তাতে বাঁ পাশে
        দুটো আর ডান পাশে তিনটে লেবেল থাকলে বাঁয়ের দ্বিতীয়টা একেবারে
        নিচে চলে যেত, আর তার লিডার গোটা ছবি কোনাকুনি চিরে উপরে উঠত।
        এখন প্রতিটি লেবেল তার লক্ষ্যের সমান উচ্চতায় বসে, কেবল দুটো
        লেবেল গায়ে গায়ে লেগে গেলে ততটুকুই নিচে ঠেলা হয়।
        """
        if not items:
            return
        minsep = size * 2.0
        ys = [top + fy * ih for (_t, _fx, fy) in items]
        for i in range(1, len(ys)):                 # গায়ে লাগলে ঠেলে দাও
            ys[i] = max(ys[i], ys[i - 1] + minsep)
        over = ys[-1] - (top + ih - 12)             # নিচে উপচালে পুরো
        if over > 0:                                # কলামটাই উপরে তোলো
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

    # ছবিটা আগে, লিডার পরে।  উল্টো করলে ছবিই লিডারকে ঢেকে দেয় আর
    # লেবেলের রেখা ছবির কিনারাতেই থেমে যায় — কোথায় দেখাচ্ছে বোঝা যায় না।
    s.image(ix, top, iw, ih, f"{IMG}/{img}")
    place(left, "left")
    place(right, "right")
    y = note_strip(s, top + ih + 30, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def img_panel(s, x, y, w, h, title, img, col=STEEL):
    panel(s, x, y, w, h, title, col)
    s.image_fit(x + 16, y + 64, w - 32, h - 78, f"{IMG}/{img}", 6)


def photo_row(fname, title, items, note, pw=376, gap=22, top=96):
    """পাশাপাশি কয়েকটি আলোকচিত্র — প্রতিটির উপরে নামের পট্টি।"""
    from PIL import Image as _Im
    hs = []
    for _t, img in items:
        with _Im.open(f"{IMG}/{img}") as im:
            iw_, ih_ = im.size
        hs.append(round((pw - 32) * ih_ / iw_) + 78)
    ph = max(hs)
    n = len(items)
    total = n * pw + (n - 1) * gap
    x0 = (1240 - total) / 2
    s = SVG(1240, top + ph + 112)
    s.title(title, T_TITLE)
    cols = [STEEL, GREEN, AMBER, GREY]
    for i, (t, img) in enumerate(items):
        img_panel(s, x0 + i * (pw + gap), top, pw, ph, t, img, cols[i % 4])
    y = note_strip(s, top + ph + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def two_panel(fname, title, left, right, note, pw=560, gap=28, top=96,
              lcol=STEEL, rcol=GREEN, rw=None):
    """দুই ছবির শিট — বাঁয়ে-ডানে দুটি প্যানেল, নিচে এক লাইনের নোট।"""
    from PIL import Image as _Im
    rw = rw or pw
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
    """ব্লক-ডায়াগ্রামের একটি ঘর।  ফেরত দেয় (x, y, w, h)।"""
    w = w or tw(text, size, 700) + 46
    x, y = cx - w / 2, cy - h / 2
    s.rect(x, y, w, h, fill, stroke, sw, 10)
    s.text(cx, cy + size * 0.34, text, size, tcol, 700, "middle")
    return x, y, w, h


def arrow(s, x1, y1, x2, y2, mk, col=STEEL, sw=3.0, dash=None):
    s.line(x1, y1, x2, y2, col, sw, dash=dash, marker=mk)


def chip(s, cx, cy, text, fill=LIGHT, stroke=STEEL, tcol=NAVY,
         size=T_SMALL):
    w = tw(text, size, 700) + 30
    s.rect(cx - w / 2, cy - 19, w, 38, fill, stroke, 2, 19)
    s.text(cx, cy + size * 0.34, text, size, tcol, 700, "middle")
    return w


# ═══════════════════════════════════════════════════════════════════════
def d01_ips_ups():
    """দুটো যন্ত্র পাশাপাশি — ঘরের আইপিএস আর কম্পিউটারের ইউপিএস।"""
    return two_panel(
        "d01_ips_ups", "আইপিএস ও ইউপিএস",
        ("বাসাবাড়ির আইপিএস", "ph_home_ips.jpg"),
        ("কম্পিউটারের ইউপিএস", "ph_ups_desk.jpg"),
        "আইপিএস ঘণ্টার হিসাবে চালায়, ইউপিএস মিনিটের হিসাবে",
        pw=592, rw=560)


def d02_block():
    """ভেতরের চারটি অংশ ও দুই অবস্থার পথ।"""
    s = SVG(1240, 900)
    s.title("আইপিএস-ইউপিএসের ভেতরের অংশ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)
    arr = s.arrow_defs(RED, "arr", 15)
    arg = s.arrow_defs(GREEN, "arg", 15)

    # যন্ত্রের খোলস
    s.rect(196, 118, 848, 372, "#F7FAFD", STEEL, 3, 16, dash="10 7")
    s.text(620, 152, "যন্ত্রের ভেতরে", T_SMALL, GREY, 700, "middle")

    # উপরের সারি — চার্জার ও ব্যাটারি
    ch = blk(s, 358, 232, "চার্জার", 214)
    bt = blk(s, 620, 232, "ব্যাটারি", 214, fill=GREENBG, stroke=GREEN,
             tcol=GREEN)
    iv = blk(s, 882, 232, "ইনভার্টার", 214, fill=AMBERBG, stroke=AMBER,
             tcol=AMBER)
    arrow(s, 465, 232, 511, 232, ar)
    arrow(s, 727, 232, 773, 232, ar)

    # নিচের সারি — চেঞ্জওভার
    co = blk(s, 620, 410, "চেঞ্জওভার সুইচ", 306, fill=LIGHT)

    # মেইন ইন
    s.text(74, 226, "মেইন", T_NAME, NAVY, 700)
    s.text(74, 258, "সাপ্লাই", T_NAME, NAVY, 700)
    s.path("M 66 282 L 66 322 L 251 322 L 251 232", STEEL, 3.0, marker=ar)
    node(s, 251, 322)
    # মেইন সরাসরি চেঞ্জওভারে
    s.path("M 251 322 L 251 410 L 467 410", STEEL, 3.0, marker=ar)

    # ইনভার্টার → চেঞ্জওভার
    s.path("M 882 264 L 882 410 L 773 410", AMBER, 3.0, marker=arr)

    # চেঞ্জওভার → লোড
    s.path("M 620 442 L 620 556 L 1108 556 L 1108 496", GREEN, 3.2,
           marker=arg)
    blk(s, 1108, 440, "লোড", 152, 64, GREENBG, GREEN, T_BODY, GREEN)

    # দুই অবস্থার ছোট ছবি
    def state(x, head, ok, txt, col, bg):
        s.rect(x, 620, 528, 152, bg, col, 2.4, 13)
        s.text(x + 264, 656, head, T_NAME, col, 700, "middle")
        s.text(x + 264, 700, txt, T_BODY, INK, 400, "middle")
        s.text(x + 264, 740, ok, T_BODY, col, 700, "middle")

    state(60, "মেইন আছে", "মেইন → লোড, পাশাপাশি ব্যাটারি চার্জ",
          "চেঞ্জওভার মেইনের দিকে", STEEL, "#F2F7FC")
    state(652, "মেইন নেই", "ব্যাটারি → ইনভার্টার → লোড",
          "চেঞ্জওভার ইনভার্টারের দিকে", AMBER, AMBERBG)

    y = note_strip(s, 800, "মেইন কাটলে চেঞ্জওভার সুইচ দিক বদলায় — "
                           "এটুকু সময়ই ট্রান্সফার টাইম")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_block.svg")


def d03_types():
    """তিন ধরনের ইউপিএস — ব্যাটারি কোথায় জোড়া লাগে, সেটাই আসল পার্থক্য।

    তাই প্রতিটি সারিতে উপরে মূল পথ, নিচে ব্যাটারির শাখা, আর শাখাটি
    যে ঘরে ওঠে সেটিই ধরনটাকে আলাদা করে।
    """
    # শেষ দুটি ঘর: ব্যাটারির শাখা কোন ঘরে গিয়ে ওঠে, আর ওঠার আগে
    # শাখায় ইনভার্টার আছে কি না।  অনলাইনে ব্যাটারি সরাসরি ডিসি বাসে
    # বসে, তাই ওখানে শাখায় আলাদা ইনভার্টার নেই।
    rows = [
        ("অফলাইন", "VFD", "৩–৮ ms",
         ["মেইন", "চেঞ্জওভার", "লোড"], 1, True, STEEL, "#F2F7FC"),
        ("লাইন-ইন্টারঅ্যাক্টিভ", "VI", "২–৬ ms",
         ["মেইন", "AVR", "চেঞ্জওভার", "লোড"], 2, True, AMBER, AMBERBG),
        ("অনলাইন", "VFI", "০ ms",
         ["মেইন", "রেক্টিফায়ার", "ইনভার্টার", "লোড"], 2, False, GREEN,
         GREENBG),
    ]
    RH = 250
    s = SVG(1240, 116 + len(rows) * (RH + 20) + 108)
    s.title("ইউপিএসের তিন ধরন", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 13)

    y = 116
    for name, code, tt, chain, feed, has_inv, col, bg in rows:
        s.rect(46, y, 1148, RH, bg, col, 2.4, 14)
        s.text(74, y + 48, name, T_NAME, col, 700)
        chip(s, 74 + tw(name, T_NAME, 700) + 66, y + 38, code,
             "#FFFFFF", col, col, T_TINY)
        s.text(1166, y + 48, f"ট্রান্সফার {tt}", T_SMALL, GREY, 700, "end")

        # উপরের শৃঙ্খল
        n = len(chain)
        bw = 186
        gapx = (1148 - 64 - n * bw) / (n - 1)
        cy = y + 118

        def cx_of(i):
            return 78 + bw / 2 + i * (bw + gapx)

        for i, t in enumerate(chain):
            blk(s, cx_of(i), cy, t, bw, 56, "#FFFFFF", col, T_BODY, col, 2.4)
            if i:
                arrow(s, cx_of(i) - bw / 2 - gapx + 4, cy,
                      cx_of(i) - bw / 2 - 5, cy, ar, col, 2.6)

        # ব্যাটারির শাখা — `feed` নম্বর ঘরের নিচ দিয়ে উঠে আসে
        by = y + 206
        arb = s.arrow_defs(GREEN, "arb", 13)
        bx = cx_of(feed) - (420 if has_inv else 300)
        blk(s, bx, by, "ব্যাটারি", 176, 52, GREENBG, GREEN, T_BODY, GREEN,
            2.4)
        if has_inv:
            ix2 = cx_of(feed) - 210
            arrow(s, bx + 88, by, ix2 - 88 - 6, by, arb, GREEN, 2.8)
            blk(s, ix2, by, "ইনভার্টার", 176, 52, GREENBG, GREEN, T_BODY,
                GREEN, 2.4)
            start = ix2 + 88
        else:
            start = bx + 88
        s.path(f"M {start} {by} L {cx_of(feed)} {by} "
               f"L {cx_of(feed)} {cy + 32}", GREEN, 2.8, marker=arb)
        y += RH + 20

    y = note_strip(s, y + 4, "অনলাইনে লোড সব সময় ইনভার্টারের উপরে, তাই "
                             "বদলের সময় লাগেই না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_types.svg")


def d15_online():
    """অনলাইন ইউপিএস দেখতে কেমন — ছোট টাওয়ার আর ডেটা সেন্টারের ঘর।"""
    return two_panel(
        "d15_online", "অনলাইন ইউপিএস",
        ("টাওয়ার ইউপিএস", "ph_ups_tower.jpg"),
        ("ডেটা সেন্টারের ইউপিএস", "ph_ups_big.jpg"),
        "অনলাইন ইউপিএসে ইনভার্টার চব্বিশ ঘণ্টা চলে, তাই বাতাস বেরোনোর "
        "ঝাঁঝরি এত বড়",
        # টাওয়ারের ছবিটা খাড়া, ডানেরটা শোয়ানো।  দুই প্যানেল সমান উঁচু
        # হয় বলে বাঁ পাশ চওড়া দিলে গোটা শিটই লম্বা হয়ে পাতা খেয়ে ফেলে।
        pw=300, rw=660, lcol=STEEL, rcol=GREEN)


def d04_wave():
    """তিন রকম আউটপুট তরঙ্গ, পাশে সত্যিকারের অসিলোস্কোপের ছবি।"""
    from PIL import Image as _Im
    with _Im.open(f"{IMG}/ph_scope.jpg") as im:
        sw_, sh_ = im.size

    LW, RW, GAP = 560, 592, 28
    x0 = (1240 - (LW + RW + GAP)) / 2
    ph = round((RW - 32) * sh_ / sw_) + 78
    ph = max(ph, 452)
    s = SVG(1240, 96 + ph + 112)
    s.title("আউটপুট তরঙ্গের আকৃতি", T_TITLE)

    panel(s, x0, 96, LW, ph, "তিন রকম তরঙ্গ", STEEL)

    # তিনটি ছোট গ্রাফ
    import math
    gh = (ph - 96) / 3
    for k, (nm, col) in enumerate((("স্কয়ার", RED),
                                   ("মডিফাইড সাইন", AMBER),
                                   ("পিওর সাইন", GREEN))):
        gy = 96 + 74 + k * gh + gh / 2
        gx0, gxw = x0 + 168, 356
        s.line(gx0, gy, gx0 + gxw, gy, LINE, 1.8)
        s.text(x0 + 150, gy + T_BODY * 0.34, nm, T_BODY, col, 700, "end")
        a = gh * 0.30
        if k == 0:                                    # স্কয়ার
            d, seg = f"M {gx0} {gy}", gxw / 4
            for i in range(4):
                sy = gy - a if i % 2 == 0 else gy + a
                d += (f" L {gx0 + i*seg:.1f} {sy:.1f} "
                      f"L {gx0 + (i+1)*seg:.1f} {sy:.1f}")
            d += f" L {gx0 + gxw:.1f} {gy:.1f}"
            s.path(d, col, 3.2)
        elif k == 1:                                  # মডিফাইড সাইন
            seg = gxw / 8
            lv = [0, 1, 0, -1, 0, 1, 0, -1]
            d = f"M {gx0} {gy}"
            for i, v in enumerate(lv):
                sy = gy - a * v
                d += (f" L {gx0 + i*seg:.1f} {sy:.1f} "
                      f"L {gx0 + (i+1)*seg:.1f} {sy:.1f}")
            d += f" L {gx0 + gxw:.1f} {gy:.1f}"
            s.path(d, col, 3.2)
        else:                                          # পিওর সাইন
            pts = [(gx0 + i * gxw / 96,
                    gy - a * math.sin(2 * math.pi * 2 * i / 96))
                   for i in range(97)]
            d = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts)
            s.path(d, col, 3.2)

    img_panel(s, x0 + LW + GAP, 96, RW, ph, "অসিলোস্কোপে মাপা", "ph_scope.jpg",
              GREEN)

    y = note_strip(s, 96 + ph + 26,
                   "হলুদ রেখা ইউপিএসের আউটপুট, বেগুনি রেখা মেইনের সাইন")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_wave.svg")


def d05_nameplate():
    """ইউপিএসের পেছনের গায়ের লেখা — প্রতিটি ঘরের নাম।

    লিডারের ডগা ইচ্ছে করেই ছাপা লেখার **পাশে**, উপরে নয় — এই ছবিটার
    গোটা কাজই তো গায়ের লেখা পড়ানো, রেখা টেনে সেটাই ঢেকে দিলে চলে না।
    """
    return photo_callouts(
        "d05_nameplate", "ইউপিএসের নেমপ্লেট", "ph_ups_rear.jpg",
        left=[("টেলিফোন সুরক্ষা", 0.34, 0.16),
              ("মেইন সুইচ", 0.12, 0.215),
              ("আউটপুট রেটিং", 0.11, 0.40),
              ("আউটপুট সকেট", 0.16, 0.70)],
        right=[("ডেটা পোর্ট", 0.86, 0.155),
               ("ইনপুট রেটিং", 0.90, 0.44),
               ("ইনপুট সকেট", 0.90, 0.535),
               ("ফিউজ ড্রয়ার", 0.90, 0.635),
               ("মডেল নম্বর", 0.86, 0.82)],
        note="300 W ও 500 VA — দুটোই লেখা; ভাগ করলে পাওয়ার ফ্যাক্টর ০.৬",
        iw=436)


def d06_display():
    """আইপিএসের ডিসপ্লে — প্রতিটি ঘর ও চিহ্নের অর্থ।"""
    s = SVG(1240, 900)
    s.title("আইপিএসের ডিসপ্লে পড়া", T_TITLE)

    PX, PY, PW, PH = 330, 108, 580, 430
    s.rect(PX, PY, PW, PH, "#EDF1F5", METAL, 3, 16)

    # এলসিডির কাচ
    LX, LY, LW_, LH_ = PX + 34, PY + 40, PW - 68, 214
    s.rect(LX, LY, LW_, LH_, LCDBG, LCDINK, 3, 8)

    # উপরের সারি — ইনপুট ও আউটপুট ভোল্ট
    s.text(LX + 24, LY + 46, "IN", T_SMALL, LCDINK, 700)
    s.text(LX + 24, LY + 84, "225 V", T_NODE, LCDINK, 700)
    s.text(LX + LW_ - 24, LY + 46, "OUT", T_SMALL, LCDINK, 700, "end")
    s.text(LX + LW_ - 24, LY + 84, "230 V", T_NODE, LCDINK, 700, "end")

    # ব্যাটারি ও লোডের বার
    def bars(bx, by, label, filled, total=5, col=LCDINK):
        s.text(bx, by, label, T_TINY, LCDINK, 700)
        for i in range(total):
            f = col if i < filled else "none"
            s.rect(bx + i * 26, by + 12, 20, 26, f, LCDINK, 1.8, 3)

    bars(LX + 24, LY + 120, "BATT", 4)
    bars(LX + LW_ - 154, LY + 120, "LOAD", 2)

    # অবস্থার চিহ্ন
    s.text(LX + LW_ / 2, LY + 186, "MAINS", T_BODY, LCDINK, 700, "middle")

    # নিচের এলইডি সারি
    leds = [("মেইন", GREEN), ("ব্যাটারি", AMBER),
            ("ওভারলোড", RED), ("ফল্ট", RED)]
    for i, (nm, col) in enumerate(leds):
        cx = PX + 92 + i * 132
        s.circle(cx, PY + 300, 17, col if i == 0 else "#FFFFFF", col, 2.6)
        s.text(cx, PY + 348, nm, T_TINY, NAVY, 700, "middle")

    # সুইচ ও অ্যালার্ম
    s.circle(PX + 148, PY + 396, 22, "#FFFFFF", GREY, 3)
    s.text(PX + 148, PY + 396 + 6, "I/O", T_TINY, GREY, 700, "middle")
    s.circle(PX + PW - 148, PY + 396, 22, "#FFFFFF", GREY, 3)
    s.text(PX + PW - 148, PY + 396 + 6, "MUTE", 14, GREY, 700, "middle")

    # ডান-বাঁ লেবেল।  লিডারের ডগা এলসিডির লেখার গায়ে নয়, তার পাশে —
    # নইলে রেখাটা সংখ্যার উপর দিয়ে চলে যায় (qc "line crosses" ধরে)
    for text, tx, ty, ly in (("ইনপুট ভোল্ট", LX + 12, LY + 66, 150),
                             ("ব্যাটারির চার্জ", LX + 30, LY + 146, 300),
                             ("চালু-বন্ধ বোতাম", PX + 126, PY + 396, 430)):
        callout(s, PX - 34, ly, text, tx, ty, "end")
    for text, tx, ty, ly in (("আউটপুট ভোল্ট", LX + LW_ - 12, LY + 66, 150),
                             ("লোডের মাত্রা", LX + LW_ - 16, LY + 146, 240),
                             ("চলার অবস্থা", LX + LW_ / 2 + 52, LY + 180, 330),
                             ("অ্যালার্ম বন্ধ", PX + PW - 126, PY + 396, 430)):
        callout(s, PX + PW + 34, ly, text, tx, ty, "start")

    # এলইডির অর্থ — নিচে সারণির মতো
    s.rect(46, 596, 1148, 176, "#FBFCFE", LINE, 2, 13)
    s.text(620, 634, "বাতির রং ও অর্থ", T_NAME, NAVY, 700, "middle")
    meanings = [("সবুজ", "মেইনে চলছে", GREEN),
                ("হলুদ", "ব্যাটারিতে চলছে", AMBER),
                ("লাল জ্বলছে", "ওভারলোড", RED),
                ("লাল কাঁপছে", "ব্যাটারি দুর্বল", RED)]
    for i, (c, m, col) in enumerate(meanings):
        cx = 176 + i * 296
        s.circle(cx - 108, 700, 13, col, col, 2)
        s.text(cx - 86, 690, c, T_TINY, col, 700)
        s.text(cx - 86, 722, m, T_TINY, INK, 400)

    s.fit(772, 24)
    return s.save(f"{OUT}/d06_display.svg")


def d07_leds():
    """সত্যিকারের ইউপিএসের ইন্ডিকেটর প্যানেল।"""
    return photo_callouts(
        "d07_leds", "ইন্ডিকেটর প্যানেল", "ph_leds.jpg",
        left=[("মেইনে চলছে", 0.38, 0.083),
              ("ব্যাটারিতে চলছে", 0.38, 0.187)],
        right=[("ওভারলোড", 0.59, 0.288),
               ("ব্যাটারি বদলাও", 0.58, 0.388),
               ("চালু-বন্ধ বোতাম", 0.545, 0.555)],
        note="চারটি বাতির একটিও লাল হলে যন্ত্র ছুঁয়ে দেখার আগে কারণ খোঁজো",
        iw=392)


def d08_batt_types():
    """তিন রকম ব্যাটারি।"""
    return photo_row(
        "d08_batt_types", "আইপিএস-ইউপিএসের ব্যাটারি",
        [("টল টিউবুলার", "ph_tubular.jpg"),
         ("SMF বা AGM", "ph_batt_smf.jpg"),
         ("ছোট SLA", "ph_batt_drawer.jpg")],
        "টিউবুলারে পানি দিতে হয়, SMF-এ হয় না — দাম ও আয়ুও আলাদা",
        pw=376)


def d09_batt_label():
    """ব্যাটারির গায়ের লেখা।"""
    return photo_callouts(
        "d09_batt_label", "ব্যাটারির নেমপ্লেট", "ph_batt_label.jpg",
        left=[("ধনাত্মক প্রান্ত", 0.22, 0.20),
              ("মডেল নম্বর", 0.30, 0.655),
              ("চার্জিং ভোল্টেজ", 0.30, 0.80)],
        right=[("ঋণাত্মক প্রান্ত", 0.80, 0.075),
               ("ভোল্ট ও AH", 0.84, 0.555),
               ("ব্যাটারির ধরন", 0.84, 0.655),
               ("পুনর্ব্যবহার চিহ্ন", 0.85, 0.755)],
        note="4.5AH/20HR মানে ২০ ঘণ্টায় নিঃশেষ করলে ৪.৫ অ্যাম্পিয়ার-আওয়ার",
        iw=452)


def d10_series_parallel():
    """ব্যাটারির সিরিজ ও প্যারালাল সংযোগ।"""
    s = SVG(1240, 720)
    s.title("ব্যাটারির সিরিজ ও প্যারালাল সংযোগ", T_TITLE)

    def cell(x, y, w=176, h=104, label="12 V"):
        s.rect(x, y, w, h, "#FFFFFF", NAVY, 3, 9)
        s.rect(x, y, w, 26, "#DCE6F0", NAVY, 2, 9)
        s.text(x + w / 2, y + h / 2 + 22, label, T_NAME, NAVY, 700, "middle")
        # প্রান্ত।  চিহ্ন দুটি প্রান্তের ঠিক উপরে নয়, পাশে — উপরে দিলে
        # প্রান্ত থেকে ওঠা তারটাই চিহ্নের উপর দিয়ে যায়
        s.rect(x + 22, y - 15, 26, 16, RED, RED, 1.5, 3)
        s.rect(x + w - 48, y - 15, 26, 16, NEUT, NEUT, 1.5, 3)
        s.text(x + 10, y - 22, "+", T_SMALL, RED, 700, "middle")
        s.text(x + w - 10, y - 22, "−", T_SMALL, NEUT, 700, "middle")
        return x + 35, x + w - 35            # + ও − প্রান্তের x

    # ── বাঁ পাশ: সিরিজ ─────────────────────────────────────────────
    s.rect(46, 96, 552, 428, "#F2F7FC", STEEL, 2.4, 14)
    s.box_auto(322, 108, "সিরিজ", T_BODY, fill=STEEL, stroke=STEEL,
               tcolor="#FFFFFF", pad_x=24, pad_y=9)

    ap, an = cell(112, 236)
    bp, bn = cell(322, 236)
    # a-এর − থেকে b-এর + — এটাই সিরিজের লিংক
    s.path(f"M {an} 221 L {an} 190 L {bp} 190 L {bp} 221", SYM, SW)
    # বাইরের প্রান্ত
    s.path(f"M {ap} 221 L {ap} 160", RED, SW)
    s.path(f"M {bn} 221 L {bn} 160", NEUT, SW)
    s.text(ap, 148, "+", T_NODE, RED, 700, "middle")
    s.text(bn, 148, "−", T_NODE, NEUT, 700, "middle")

    s.text(322, 400, "12 V + 12 V = 24 V", T_NAME, STEEL, 700, "middle")
    s.text(322, 440, "AH একই থাকে", T_BODY, GREY, 400, "middle")
    s.text(322, 484, "বড় আইপিএসে এভাবেই", T_BODY, NAVY, 400, "middle")

    # ── ডান পাশ: প্যারালাল ────────────────────────────────────────
    s.rect(642, 96, 552, 428, GREENBG, GREEN, 2.4, 14)
    s.box_auto(918, 108, "প্যারালাল", T_BODY, fill=GREEN, stroke=GREEN,
               tcolor="#FFFFFF", pad_x=24, pad_y=9)

    cp, cn = cell(708, 236, label="100 AH")
    dp, dn = cell(918, 236, label="100 AH")
    # দুটি স্বাধীন বাস — + এক বাসে, − আরেক বাসে
    s.path(f"M {cp} 221 L {cp} 186 L {dp} 186", RED, SW)
    s.path(f"M {dp} 221 L {dp} 186", RED, SW)
    s.path(f"M {cn} 348 L {cn} 372 L {dn} 372", NEUT, SW)
    s.path(f"M {dn} 348 L {dn} 372", NEUT, SW)
    node(s, dp, 186, RED)
    node(s, cn, 372, NEUT)
    s.path(f"M {(cp + dp) / 2} 186 L {(cp + dp) / 2} 152", RED, SW)
    s.text((cp + dp) / 2, 140, "+", T_NODE, RED, 700, "middle")
    s.path(f"M {(cn + dn) / 2} 372 L {(cn + dn) / 2} 404", NEUT, SW)
    s.text((cn + dn) / 2, 428, "−", T_NODE, NEUT, 700, "middle")

    s.text(918, 462, "100 AH + 100 AH = 200 AH", T_NAME, GREEN, 700,
           "middle")
    s.text(918, 500, "ভোল্টেজ একই থাকে", T_BODY, GREY, 400, "middle")

    y = note_strip(s, 548, "একই ক্ষমতার, একই বয়সের, একই ব্র্যান্ডের "
                           "ব্যাটারি ছাড়া জোড়া দিয়ো না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d10_series_parallel.svg")


def d11_connect():
    """আইপিএসের সংযোগ — মেইন ডিবি থেকে আইপিএস ডিবি পর্যন্ত।

    মাপগুলো টেনেটুনে বসানো নয়, হিসাব করা:  নোট-পটির ডান কিনারা ১১৯৪,
    তাই সবচেয়ে ডানের লোড-ঘরটির কেন্দ্র ১১০৫-এর বেশি হতে পারে না
    (১১০৫ + ১৭০/২ = ১১৯০)।  আগে ৯৭২ ± ১৯৬ ধরা হয়েছিল, তাতে "সকেট"
    ঘরটা ক্যানভাসের বাইরে কাটা পড়েছিল — `qc.py` কেবল **লেখা** ক্যানভাসে
    আছে কি না দেখে, ঘরের কিনারা দেখে না।
    """
    s = SVG(1240, 950)
    s.title("আইপিএস সংযোগ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 14)

    # মিটার ও মেইন ডিবি
    blk(s, 130, 190, "মিটার", 168, 72, "#FFFFFF", GREY, T_BODY, GREY)
    blk(s, 356, 190, "মেইন DB", 200, 72, "#FFFFFF", NAVY, T_BODY, NAVY)
    arrow(s, 214, 190, 251, 190, ar)

    # মেইন ডিবি → দুই ভাগ
    s.text(390, 268, "দুই ভাগ", T_SMALL, GREY, 700)
    s.path("M 356 226 L 356 296", STEEL, 3.0)
    node(s, 356, 296)

    # সাধারণ লাইন (আইপিএসে যাবে না)
    s.path("M 356 296 L 170 296 L 170 356", STEEL, 3.0, marker=ar)
    blk(s, 170, 400, "সাধারণ লাইন", 228, 72, "#F4F6F8", GREY, T_BODY, GREY)
    s.text(170, 470, "এসি · ফ্রিজ · পাম্প", T_TINY, GREY, 400, "middle")

    # আইপিএসের লাইন
    s.path("M 356 296 L 620 296 L 620 340", STEEL, 3.0, marker=ar)
    blk(s, 620, 380, "IPS MCB", 190, 66, LIGHT, STEEL, T_BODY, STEEL)

    # আইপিএস
    s.path("M 620 413 L 620 462", STEEL, 3.0, marker=ar)
    ipsx, ipsy, ipsw, ipsh = 455, 462, 330, 150
    s.rect(ipsx, ipsy, ipsw, ipsh, AMBERBG, AMBER, 3, 13)
    s.text(620, 516, "আইপিএস", T_NAME, AMBER, 700, "middle")
    s.text(533, 574, "IN", T_BODY, GREY, 700, "middle")
    s.text(707, 574, "OUT", T_BODY, GREY, 700, "middle")

    # ব্যাটারি — নিচ দিয়ে।  এসির IN/OUT-এর পাশ দিয়ে নিলে ব্যাটারিকেও
    # এসি সংযোগ ভেবে বসার ভয় থাকে।
    s.path("M 520 612 L 520 706 L 334 706", GREEN, 3.2)
    blk(s, 240, 706, "ব্যাটারি", 178, 66, GREENBG, GREEN, T_BODY, GREEN)
    s.text(240, 764, "লাল +, কালো −", T_TINY, GREEN, 400, "middle")

    # আর্থিং।  ex = ৬৬০ — ডানে সরালে "আর্থ" লেখাটার উপর দিয়ে বাঁ দিকের
    # লোড-ড্রপ (x = ৭২৫) চলে যায়।
    ex = 660
    s.path(f"M {ex} 612 L {ex} 654", EARTH, 3.0)
    for i, hw in enumerate((34, 22, 11)):
        s.line(ex - hw, 654 + i * 12, ex + hw, 654 + i * 12, EARTH, 3.4)
    s.text(ex, 716, "আর্থ", T_BODY, EARTH, 700, "middle")

    # আইপিএস → আইপিএস ডিবি
    s.path("M 785 514 L 915 514 L 915 566", AMBER, 3.2,
           marker=s.arrow_defs(AMBER, "ara", 14))
    blk(s, 915, 600, "IPS DB", 196, 66, "#FFFFFF", NAVY, T_BODY, NAVY)

    # লোড
    s.path("M 915 633 L 915 690", NAVY, 2.8)
    s.path("M 725 690 L 1105 690", NAVY, 2.8)
    node(s, 915, 690)
    for nm, cx in (("বাতি", 725), ("ফ্যান", 915), ("সকেট", 1105)):
        s.path(f"M {cx} 690 L {cx} 729", NAVY, 2.8)
        blk(s, cx, 760, nm, 170, 62, "#FFFFFF", STEEL, T_BODY, STEEL)

    y = note_strip(s, 828, "আইপিএসের লাইন আলাদা DB-তে — এসি, ফ্রিজ ও পাম্প "
                           "কখনো ওতে নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d11_connect.svg")


def d12_sockets():
    """কোন সকেট ব্যাকআপে আর কোনটা শুধু সার্জে।"""
    return photo_callouts(
        "d12_sockets", "ইউপিএসের পেছনের সকেট", "ph_ups_rear2.jpg",
        # লক্ষ্যের ভগ্নাংশ ছবির উপর ৫% গ্রিড বসিয়ে মাপা।  আগের তিনটি
        # ডান লেবেলের বিন্দু যন্ত্রের কিনারার বাইরে — কার্পেটের উপর —
        # পড়ছিল; পাশ থেকে তোলা ছবি বলে ডান কিনারা নিচের দিকে ঢালু
        left=[("টেলিফোন পোর্ট", 0.34, 0.250),
              ("সার্কিট ব্রেকার", 0.20, 0.450),
              ("ইনপুট সকেট", 0.175, 0.845)],
        right=[("মডেল রেটিং", 0.78, 0.360),
               ("ব্যাকআপ সকেট", 0.66, 0.580),
               ("শুধু সার্জ", 0.62, 0.845)],
        note="নিচের সকেটটি ব্যাটারিতে চলে না — প্রিন্টার ওখানেই লাগাতে হয়",
        iw=404)


def d13_flow():
    """সাইজ নির্ণয়ের পাঁচ ধাপ।"""
    s = SVG(1240, 700)
    s.title("আইপিএস ও ব্যাটারির মাপ বের করার ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)

    steps = [
        ("১", "লোড গোনা", "মোট ওয়াট", STEEL),
        ("২", "VA বের করা", "ওয়াট / PF", STEEL),
        ("৩", "ব্যাটারি AH", "কত ঘণ্টা চাই", GREEN),
        ("৪", "চার্জিং কারেন্ট", "AH-এর ১০%", AMBER),
        ("৫", "তার ও ব্রেকার", "DC ও AC দুই দিকে", NAVY),
    ]
    bw, gapx = 206, 26
    total = len(steps) * bw + (len(steps) - 1) * gapx
    x0 = (1240 - total) / 2
    for i, (n, head, sub, col) in enumerate(steps):
        cx = x0 + bw / 2 + i * (bw + gapx)
        s.rect(cx - bw / 2, 128, bw, 172, "#FFFFFF", col, 3, 13)
        s.badge(cx, 168, n, 24, col, "#FFFFFF", T_BODY)
        s.text(cx, 236, head, T_BODY, col, 700, "middle")
        s.text(cx, 274, sub, T_TINY, GREY, 400, "middle")
        if i:
            arrow(s, cx - bw / 2 - gapx + 2, 214, cx - bw / 2 - 6, 214, ar,
                  STEEL, 3.0)

    # নমুনা হিসাব
    s.rect(46, 348, 1148, 210, "#F7FAFD", STEEL, 2.4, 14)
    s.text(620, 392, "উদাহরণের সংখ্যা", T_NAME, NAVY, 700, "middle")
    vals = [("350 W", "লোড"), ("437 VA", "→ 600 VA"),
            ("172 AH", "→ 200 AH"), ("20 A", "চার্জিং"),
            ("24 V", "দুই ব্যাটারি")]
    for i, (v, k) in enumerate(vals):
        cx = x0 + bw / 2 + i * (bw + gapx)
        s.text(cx, 458, v, T_NODE, NAVY, 700, "middle")
        s.text(cx, 500, k, T_TINY, GREY, 400, "middle")

    y = note_strip(s, 582, "প্রথমে লোড, তারপর VA, তারপর AH — ক্রম উল্টালে "
                           "হিসাব মেলে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d13_flow.svg")


def d14_ips_plate():
    """আইপিএসের রেটিং প্লেটে কোন ঘরে কী লেখা থাকে।

    আসল ছবি নয় — বাজারচলতি সাইন-ওয়েভ আইপিএসের প্লেটে যে ঘরগুলো থাকে,
    সেগুলোই সাজানো।  কোনো ব্র্যান্ডের নাম ইচ্ছে করেই লেখা হয়নি; ঘরের
    নামগুলোই সব যন্ত্রে এক।
    """
    s = SVG(1240, 790)
    s.title("আইপিএসের রেটিং প্লেট", T_TITLE)

    # সাতটি সারি ধরাতে PH ≥ ৪৬২ লাগে — কম দিলে শেষ সারিটা ভেতরের
    # সাদা আয়তক্ষেত্রের কিনারায় আটকে যায় (qc "box edge cuts" ধরে)
    PX, PY, PW, PH = 386, 128, 468, 462
    s.rect(PX, PY, PW, PH, PLATE, METAL, 3.4, 10)
    s.rect(PX + 14, PY + 14, PW - 28, PH - 28, "#FFFFFF", "#B7C2CE", 2, 6)
    for cx, cy in ((PX + 26, PY + 26), (PX + PW - 26, PY + 26),
                   (PX + 26, PY + PH - 26), (PX + PW - 26, PY + PH - 26)):
        s.circle(cx, cy, 7, BOXG, METAL, 2)

    s.text(PX + PW / 2, PY + 70, "SINE WAVE IPS", T_BODY, NAVY, 700,
           "middle")
    s.line(PX + 40, PY + 88, PX + PW - 40, PY + 88, LINE, 1.8)

    rows = [("CAPACITY", "1200 VA"),
            ("OUTPUT", "960 W"),
            ("INPUT", "230 V, 50 Hz"),
            ("OUTPUT", "230 V, 50 Hz"),
            ("BATTERY", "24 V"),
            ("CHARGING", "15 A"),
            ("WAVEFORM", "PURE SINE")]
    for i, (k, v) in enumerate(rows):
        ry = PY + 132 + i * 48
        s.text(PX + 46, ry, k, T_TINY, GREY, 400)
        s.text(PX + PW - 44, ry, v, T_BODY, INK, 700, "end")

    # লেবেল প্লেটের বাইরে, লিডার কিনারাতেই থামে
    left = ["মোট ক্ষমতা", "কাজের ক্ষমতা", "ইনপুট ভোল্ট", "আউটপুট ভোল্ট"]
    right = ["ব্যাটারির ভোল্ট", "চার্জিং কারেন্ট", "তরঙ্গের ধরন"]
    for i, text in enumerate(left):
        ty = PY + 124 + i * 48
        callout(s, PX - 42, ty, text, PX, ty, "end", T_CALL)
    for i, text in enumerate(right):
        ty = PY + 316 + i * 48
        callout(s, PX + PW + 42, ty, text, PX + PW, ty, "start", T_CALL)

    y = note_strip(s, PY + PH + 32,
                   "960 W / 1200 VA — ভাগ করলে পাওয়ার ফ্যাক্টর ০.৮")
    s.fit(y, 24)
    return s.save(f"{OUT}/d14_ips_plate.svg")


ALL = [d01_ips_ups, d02_block, d03_types, d15_online, d04_wave, d05_nameplate,
       d14_ips_plate, d06_display, d07_leds, d08_batt_types, d09_batt_label,
       d10_series_parallel, d11_connect, d12_sockets, d13_flow]


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
