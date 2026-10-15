# -*- coding: utf-8 -*-
"""অধ্যায় ২২ — সার্কিট ব্রেকার ও প্রতিরক্ষামূলক ডিভাইস : ডায়াগ্রাম।

দুই রকম চিত্র এখানে পাশাপাশি চলে, আর ভাগটা ইচ্ছাকৃত:

**নেমপ্লেট-চিত্র** — আসল যন্ত্রের আলোকচিত্র, দুই পাশে বাংলা কল-আউট।
এই অধ্যায়ের মূল দাবিই তো এই — যে কেউ যেন যেকোনো ব্রেকার হাতে নিয়ে
গায়ের লেখাটা পড়তে পারে।  সেটা হাতে আঁকা ছবি দিয়ে হয় না; ছাপা
লেখাটাই পাঠ, তাই ছবিই লাগে (`assets_ch22.py`, উইকিমিডিয়া কমন্স)।
গোটা যন্ত্রের ছবি ১৫.৪ সেমিতে বসালে ওই লেখা ৩–৪ পয়েন্টে নেমে আসে —
তাই প্রতিটি যন্ত্রের কেবল লেবেল-অংশটুকু আলাদা করে কাটা আছে।

**নীতির চিত্র** — কেন ট্রিপ করে, কোন পথে কারেন্ট যায়, ডিবিতে কে কার
পরে বসে — এগুলো আঁকা।  আলোকচিত্রে নীতি দেখা যায় না।

অধ্যায় ১৫ থেকে চলে আসা ছবির নিয়ম এখানেও কড়া:  প্যানেলের শিরোনাম
বিশেষ্য, যন্ত্রাংশের লেবেল এক-দুই শব্দ, নিচে এক লাইনের একটি নোট-পটি।
কারণ, পরামর্শ আর সতর্কবাণী সবই বইয়ের লেখায় — ছবিতে নয়।

ছবির লেবেলে যা লেখা যাবে না:  কালপুরুষে `÷ √ ² Ω φ ≤` নেই বা ভুল
আঁকে।  ভাগ সবসময় `/`, বর্গমিলিমিটার কথায়, আর গ্রিক অক্ষরের বদলে
ল্যাটিন নাম (`IΔn`-এর জায়গায় `I dn` নয় — ওটা ছাপা লেখারই অংশ, ছবির
নিজের লেবেলে ওটা লেখা হয় না)।
"""
import math
import os

from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch22")
IMG = os.path.join(HERE, "assets", "ch22")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 23.5
T_SMALL = 23
T_CALL = 24
T_TINY = 22

SYM = "#12324D"
SW = 3.4
BOXG = "#E7ECF1"
PLATE = "#F4F7FA"
METAL = "#8D9AA8"
COPPER = "#B5713A"
DEAD = "#9AA6B2"

# BNBC ১.৩.৯.৩.১৫ / সারণি ৮.১.২-এর রং
C_L = "#D42A1F"
C_N = "#1F2933"
C_PE = "#1B6E47"


# ── shared helpers (অধ্যায় ২১ থেকে, চওড়া ক্যানভাসের জন্য সাধারণীকৃত) ──
def panel(s, x, y, w, h, title, col=STEEL):
    """প্যানেলের শিরোনাম — কেবল নাম, কোনো মন্তব্য নয়।"""
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def note_strip(s, y, text, size=T_NAME, fill="#EAF2FA", stroke=STEEL,
               tcolor=NAVY, pad=46):
    """এক লাইনের তথ্য-পটি, ক্যানভাসের প্রস্থ ধরে।

    দুই লাইনে গড়ালে এখানেই থেমে যায় — ছবির নিচে অনুচ্ছেদ বসানো এই
    বইয়ের নিয়ম নয়, ওটা বইয়ের লেখার কাজ।
    """
    w = s.w - 2 * pad
    if tw(text, size, 700) > w - 60:
        raise ValueError(f"note_strip এক লাইনে ধরে না: {text!r}")
    s.rect(pad, y, w, 58, fill, stroke, 2, 11)
    s.text(pad + w / 2, y + 36, text, size, tcolor, 700, "middle")
    return y + 58


def head_bar(s, x, y, w, h, text, col, size=T_NODE, rx=13):
    """রঙিন শিরোনাম-পটি, নিচের কোনা চৌকো।

    কোনা চৌকো করার জন্য দ্বিতীয় যে চৌকো আয়তটা বসাতে হয়, সেটি অবশ্যই
    `y + rx` থেকে শুরু হবে — নইলে লেখাটা ওই আয়তের উপরের কিনারা
    ডিঙিয়ে যায় আর `qc.py` "box edge cuts" বলে ধরে ফেলে।  একবার এই
    ভুলেই ছয়টা প্যানেলের শিরোনাম ধরা পড়েছিল।
    """
    s.rect(x, y, w, h, col, col, 2.4, rx)
    s.rect(x, y + rx, w, h - rx, col, "none", 0, 0)
    s.text(x + w / 2, y + h / 2 + size * 0.34, text, size, "#FFFFFF", 700,
           "middle")


def callout(s, x, y, text, tx, ty, anchor="end", size=T_CALL, col=NAVY,
            elbow=False):
    """লেবেল ও লিডার — লেখার যে পাশে লক্ষ্য, সেই কিনারা থেকেই বেরোয়।

    `elbow=True` দিলে লিডার প্রথমে লেবেলের উচ্চতায় আড়াআড়ি যায়, তারপর
    খাড়া নেমে লক্ষ্যে ঠেকে — নেমপ্লেটে ছাপা কোনো ছক বা লেখার উপর
    দিয়ে সোজা তির্যক রেখা টানা এড়াতে।
    """
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
    """একটি সোর্স-ছবির শিট — শিরোনাম, প্যানেল, এক লাইনের নোট।"""
    ph = _ih(img, iw - 32) + 78
    x0 = (w - iw) / 2
    s = SVG(w, top + ph + 112)
    s.title(title, T_TITLE)
    img_panel(s, x0, top, iw, ph, head, img)
    y = note_strip(s, top + ph + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def strip_panels(fname, title, items, note, gap=24, top=100, pw=None, w=1240):
    """পাশাপাশি কয়েকটি ছবি-প্যানেল, নিচে এক লাইনের নোট।

    items = [(প্যানেল-শিরোনাম, ফাইলনাম, রং), …]
    """
    n = len(items)
    pw = pw or (w - 92 - gap * (n - 1)) / n
    ph = max(_ih(img, pw - 32) for _t, img, _c in items) + 78
    x0 = (w - (pw * n + gap * (n - 1))) / 2
    s = SVG(w, top + ph + 112)
    s.title(title, T_TITLE)
    for i, (head, img, col) in enumerate(items):
        img_panel(s, x0 + i * (pw + gap), top, pw, ph, head, img, col)
    y = note_strip(s, top + ph + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def pair_panels(fname, title, items, note, h=560, gap=24, top=100, w=1240):
    """সমান উচ্চতার কয়েকটি ছবি-প্যানেল, প্রস্থ ছবির অনুপাতে।

    `strip_panels` সব প্যানেলকে সমান চওড়া করে, ফলে একটি লম্বাটে ছবি
    থাকলেই গোটা শিটটা লম্বা হয়ে যায় (১৫.৪ সেমিতে বসালে ১২ সেমির বেশি
    উঁচু — পাতার পায়ে ফাঁক)।  এখানে উচ্চতা বাঁধা, প্রস্থ ছবিভেদে।
    """
    from PIL import Image as _Im
    ws = []
    for _t, img, _c in items:
        with _Im.open(f"{IMG}/{img}") as im:
            ws.append(round(h * im.size[0] / im.size[1]) + 32)
    ph = h + 78
    x0 = (w - (sum(ws) + gap * (len(items) - 1))) / 2
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

    অধ্যায় ১৯-এ শেখা তিনটি ফাঁদ এখানেই বাঁধা আছে:  (ক) ছবিটা আগে আঁকো,
    লিডার পরে — উল্টো করলে ছবিই লিডার ঢেকে দেয়;  (খ) লিডারের ডগা
    ছাপা লেখার পাশে রাখো, লেখার উপরে নয় — নেমপ্লেটে ছাপা লেখাটাই তো
    পাঠ;  (গ) প্রতিটি লেবেল তার নিজের লক্ষ্যের সমান উচ্চতায় বসে, নইলে
    একটি লিডার গোটা ছবি কোনাকুনি চিরে যায়।
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
            # চতুর্থ মান দিলে লিডার কনুই খেয়ে যায় — আগে আড়াআড়ি, পরে
            # খাড়া।  ছাপা ছবির উপর দিয়ে সোজা টানলে যেখানে ছক কেটে
            # যেত, সেখানে এটাই একমাত্র পরিষ্কার পথ।
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

    `photo_callouts` দুই পাশে লেবেল বসায়; তাতে ৩·৬ঃ১ অনুপাতের একটা
    ফালি ছবির বেলায় সব লিডার কোনাকুনি চিরে যায়, কারণ উচ্চতায় জায়গাই
    নেই।  এখানে লিডার আগে খাড়া নামে, দরকার হলে শেষে একটুখানি আড়াআড়ি
    সরে লক্ষ্যে ঠেকে — ছবির উপর কোনো তির্যক দাগ পড়ে না।

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


def lamp(s, cx, cy, r=17, col=NAVY):
    s.circle(cx, cy, r, "#FFFFFF", col, 2.6)
    s.path(f"M {cx - r * 0.7} {cy - r * 0.7} L {cx + r * 0.7} {cy + r * 0.7}",
           col, 2.2)
    s.path(f"M {cx + r * 0.7} {cy - r * 0.7} L {cx - r * 0.7} {cy + r * 0.7}",
           col, 2.2)


def breaker_sym(s, cx, cy, tripped=False, col=SYM, h=54):
    """ব্রেakারের প্রতীক — দুই টার্মিনাল, মাঝে হেলানো কন্টাক্ট বাহু।"""
    y0, y1 = cy - h / 2, cy + h / 2
    node(s, cx, y0, col, 5.5)
    node(s, cx, y1, col, 5.5)
    if tripped:
        s.path(f"M {cx} {y1} L {cx + 22} {y0 - 6}", col, 3.2)
    else:
        s.path(f"M {cx} {y1} L {cx + 10} {y0 + 2} L {cx} {y0}", col, 3.2)
    # কাটার চিহ্ন — ব্রেকার, নিছক সুইচ নয়
    s.path(f"M {cx - 10} {y0 - 9} L {cx + 10} {y0 - 9}", col, 3.0)
    return cx, y0, y1


def bolt(s, x, y, sc=1.0, col=AMBER):
    """বজ্রপাত / সার্জের চিহ্ন।"""
    d = (f"M {x} {y} l {14 * sc} {-30 * sc} l {-9 * sc} {2 * sc} "
         f"l {13 * sc} {-28 * sc} l {-26 * sc} {30 * sc} "
         f"l {10 * sc} {-2 * sc} z")
    s.path(d, "#8A5A00", 1.6, col)


def person(s, cx, cy, sc=1.0, col=NAVY):
    """মানুষের ছোট প্রতীক — শক-সুরক্ষার ছবিতে।"""
    s.circle(cx, cy - 26 * sc, 9 * sc, "#FFFFFF", col, 2.6)
    s.path(f"M {cx} {cy - 17 * sc} L {cx} {cy + 8 * sc}", col, 2.8)
    s.path(f"M {cx - 13 * sc} {cy - 8 * sc} L {cx + 13 * sc} {cy - 8 * sc}",
           col, 2.8)
    s.path(f"M {cx} {cy + 8 * sc} L {cx - 11 * sc} {cy + 28 * sc}", col, 2.8)
    s.path(f"M {cx} {cy + 8 * sc} L {cx + 11 * sc} {cy + 28 * sc}", col, 2.8)


def earth(s, cx, cy, col=C_PE, w=34):
    """আর্থের প্রতীক — তিনটি ক্রমহ্রাসমান রেখা।"""
    for i, k in enumerate((1.0, 0.62, 0.28)):
        y = cy + i * 9
        s.path(f"M {cx - w * k / 2} {y} L {cx + w * k / 2} {y}", col, 3.4)


# ── ১. তিন রকম ত্রুটি ────────────────────────────────────────────────────
def d01_faults():
    """ওভারলোড · শর্ট সার্কিট · আর্থ লিকেজ — তিনটি আলাদা রোগ।

    ছাত্ররা তিনটেকে এক করে ফেলে, অথচ ধরার যন্ত্র তিনটেই আলাদা।  তাই
    প্রথম ছবিতেই তিনটেকে পাশাপাশি বসানো — একই সাপ্লাই, একই তার,
    কেবল গোলমালের জায়গাটা আলাদা।
    """
    s = SVG(1240, 640)
    s.title("তিন রকম বৈদ্যুতিক ত্রুটি", T_TITLE)
    ar = s.arrow_defs(RED, "arR", 14)

    pw, gap = 376, 26
    x0 = (1240 - (pw * 3 + gap * 2)) / 2
    heads = [("ওভারলোড", AMBER), ("শর্ট সার্কিট", RED), ("আর্থ লিকেজ", STEEL)]
    for i, (head, col) in enumerate(heads):
        px = x0 + i * (pw + gap)
        panel(s, px, 104, pw, 396, head, col)
        xl, xn = px + 96, px + 280        # লাইভ ও নিউট্রালের খাড়া পথ
        ytop, ybot = 176, 430

        s.path(f"M {xl} {ytop} L {xl} {ybot}", C_L, SW)
        s.text(xl, ytop - 12, "L", T_SMALL, C_L, 700, "middle")
        s.text(xn, ytop - 12, "N", T_SMALL, NAVY, 700, "middle")

        if i == 0:
            # ওভারলোড — বৈধ পথ, কিন্তু অনেকগুলো লোড একসঙ্গে
            s.path(f"M {xn} {ytop} L {xn} {ybot}", C_N, SW)
            for k, ly in enumerate((228, 300, 372)):
                s.path(f"M {xl} {ly} L {xl + 58} {ly}", C_L, 3.0)
                s.path(f"M {xn - 58} {ly} L {xn} {ly}", C_N, 3.0)
                lamp(s, (xl + xn) / 2, ly, 21)
                node(s, xl, ly)
                node(s, xn, ly)
            s.text(px + pw / 2, 466, "বৈধ পথ, কিন্তু কারেন্ট বেশি",
                   T_SMALL, AMBER, 700, "middle")

        elif i == 1:
            # শর্ট সার্কিট — L আর N সরাসরি জোড়া
            s.path(f"M {xn} {ytop} L {xn} {ybot}", C_N, SW)
            s.path(f"M {xl} {300} L {xn} {300}", RED, 6.0)
            node(s, xl, 300, RED, 8)
            node(s, xn, 300, RED, 8)
            bolt(s, (xl + xn) / 2 - 4, 288, 0.9, "#F2C744")
            s.path(f"M {xl} {372} L {xl + 58} {372}", DEAD, 3.0)
            s.path(f"M {xn - 58} {372} L {xn} {372}", DEAD, 3.0)
            lamp(s, (xl + xn) / 2, 372, 21, DEAD)
            s.text(px + pw / 2, 466, "L আর N সরাসরি মিলে গেছে",
                   T_SMALL, RED, 700, "middle")

        else:
            # আর্থ লিকেজ — কারেন্টের একাংশ শরীর/আর্থ দিয়ে
            s.path(f"M {xn} {ytop} L {xn} {ybot}", C_N, SW)
            s.path(f"M {xl} {252} L {xl + 46} {252}", C_L, 3.0)
            s.path(f"M {xn - 46} {252} L {xn} {252}", C_N, 3.0)
            lamp(s, (xl + xn) / 2, 252, 21)
            node(s, xl, 252)
            node(s, xn, 252)
            person(s, px + 196, 350, 0.95)
            s.path(f"M {xl} {342} L {px + 176} {342}", RED, 3.0,
                   dash="7 5", marker=ar)
            node(s, xl, 342, RED, 7)
            earth(s, px + 196, 394)
            s.text(px + pw / 2, 466, "কারেন্টের অংশ আর্থের পথে",
                   T_SMALL, STEEL, 700, "middle")

    y = note_strip(s, 512,
                   "তিনটি আলাদা রোগ; তাই ধরার যন্ত্রও এক নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_faults.svg")


# ── ২. ফিউজ ও সার্কিট ব্রেকার ────────────────────────────────────────────
def d02_fuse_cb():
    """একই কাজ, দুই চেহারা — একটা গলে, অন্যটা ফেলে দেয়।

    প্রথম খসড়ায় ফিউজটা ছিল নিছক একটা ফাঁকা আয়ত আর ব্রেকারটা একটা
    রেখা — কোনটা কী, দেখে বোঝা যেত না, আর `O` চিপটার উপর দিয়ে ট্রিপ
    হওয়া হাতলটা চলে যেত।  এখন ফিউজের দুই প্রান্তে ধাতব ক্যাপ ও ভেতরে
    সরু তার আঁকা, আর ব্রেকারের হাতলটা খোলের **উপরে** — চিপ নয়, হাতলের
    গায়েই `I`/`O`, তাই ঢাকাঢাকির প্রশ্নই ওঠে না।
    """
    s = SVG(1240, 660)
    s.title("ফিউজ ও সার্কিট ব্রেকার", T_TITLE)

    pw, gap = 548, 32
    x0 = (1240 - (pw * 2 + gap)) / 2
    for i, (head, col) in enumerate((("ফিউজ", AMBER),
                                     ("সার্কিট ব্রেকার", GREEN))):
        px = x0 + i * (pw + gap)
        panel(s, px, 104, pw, 404, head, col)
        cx = px + pw / 2

        for j, (state, ly) in enumerate((("স্বাভাবিক", 244),
                                         ("ত্রুটির পর", 392))):
            s.text(px + 30, ly + 8, state, T_BODY, GREY, 700, "start")
            xa, xb = px + 190, px + pw - 42
            s.path(f"M {xa - 52} {ly} L {xa} {ly}", C_L, SW)
            s.path(f"M {xb} {ly} L {xb + 28} {ly}", C_L, SW)

            if i == 0:
                # ── ফিউজ: দুই প্রান্তে ধাতব ক্যাপ, ভেতরে সরু তার ──
                cw, mx = 30, (xa + xb) / 2
                s.rect(xa, ly - 28, xb - xa, 56, "#FFFFFF", NAVY, 2.8, 9)
                s.rect(xa, ly - 28, cw, 56, METAL, NAVY, 2.2, 9)
                s.rect(xb - cw, ly - 28, cw, 56, METAL, NAVY, 2.2, 9)
                ea, eb = xa + cw, xb - cw

                def zig(x1, x2, n=8, amp=7):
                    step = (x2 - x1) / n
                    d = f"M {x1} {ly}"
                    for k in range(n):
                        d += (f" L {x1 + step * (k + 0.5)} "
                              f"{ly + (amp if k % 2 == 0 else -amp)}")
                    return d + f" L {x2} {ly}"

                if j == 0:
                    s.path(zig(ea, eb), COPPER, 2.6)
                else:
                    # কাচ কালচে হয়ে যায়, তার গলে দুই টুকরো
                    s.ellipse(mx, ly, 72, 23, "#EFE3DC")
                    s.ellipse(mx, ly, 42, 16, "#D9C6BA")
                    s.path(zig(ea, mx - 46, 4), COPPER, 2.6)
                    s.path(zig(mx + 46, eb, 4), COPPER, 2.6)
                    s.circle(mx - 46, ly, 5.5, COPPER)
                    s.circle(mx + 46, ly, 5.5, COPPER)
            else:
                # ── ব্রেকার: খোল, উপরে হাতল, ভেতরে কন্টাক্ট ──
                bx, bw = xa, xb - xa
                mx = bx + bw / 2
                s.rect(bx, ly - 30, bw, 60, "#FFFFFF", NAVY, 2.8, 9)
                # ডিন-রেলের খাঁজ
                s.rect(bx + 26, ly + 24, bw - 52, 12, BOXG, NAVY, 1.8, 3)
                piv, fix = bx + 34, bx + bw - 104
                node(s, piv, ly, SYM, 5.5)
                s.path(f"M {fix} {ly} L {bx + bw - 34} {ly}", SYM, 3.2)
                node(s, bx + bw - 34, ly, SYM, 5.5)
                on = (j == 0)
                lc, lb = (GREEN, GREENBG) if on else (RED, REDBG)
                if on:
                    # কন্টাক্ট লেগে আছে — জোড়ের জায়গায় গোল নোড
                    s.path(f"M {piv} {ly} L {fix} {ly}", SYM, 3.4)
                    node(s, fix, ly, SYM, 5.5)
                else:
                    # খুলে গেছে — স্থির কন্টাক্ট প্লেট আর ফাঁক দেখা যায়
                    s.path(f"M {fix} {ly - 11} L {fix} {ly + 11}", SYM, 3.4)
                    s.path(f"M {piv} {ly} L {piv + 72} {ly - 21}", SYM, 3.4)
                # হাতল — খোলের উপরে, তাই কিছুই ঢাকে না
                hx = mx - 22 + (0 if on else 5)
                s.rect(hx + 7, ly - 40, 30, 14, lc, lc, 0, 3)
                s.rect(hx, ly - 78, 44, 44, lb, lc, 2.8, 8)
                s.text(hx + 22, ly - 48, "I" if on else "O",
                       T_NAME, lc, 700, "middle")

        s.text(cx, 474, "বদলাতে হয়" if i == 0 else "রিসেট করলেই চলে",
               T_NAME, RED if i == 0 else GREEN, 700, "middle")

    y = note_strip(s, 522,
                   "ফিউজের তার একবারই গলে; ব্রেকার ট্রিপ করে, পুড়ে যায় না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_fuse_cb.svg")


# ── ৩. সুরক্ষার স্তর ─────────────────────────────────────────────────────
def d03_layers():
    """সাপ্লাই থেকে লোড — পথে চারটি স্তর, প্রতিটির কাজ আলাদা।

    এক ডিভাইস সব বিপদ ঠেকায় না।  ছবিটা সেই কথাটাই একবারে বলে দেয়,
    আর ডিবির ভেতরে যন্ত্রগুলো ঠিক এই ক্রমেই বসে।
    """
    s = SVG(1240, 520)
    s.title("সুরক্ষার স্তর: কে কী থেকে বাঁচায়", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar3", 15)

    items = [("আইসোলেটর", "হাত দেওয়ার আগে\nলাইন কাটা", STEEL),
             ("SPD", "বজ্রপাতের\nঅতিরিক্ত ভোল্টেজ", AMBER),
             ("RCCB / RCBO", "শরীরে বা আর্থে\nকারেন্ট লিক", GREEN),
             ("MCB / MCCB", "ওভারলোড ও\nশর্ট সার্কিট", RED)]
    bw, gap = 244, 26
    x0 = (1240 - (bw * 4 + gap * 3)) / 2
    ytop = 152

    s.text(x0 - 8, ytop - 26, "সাপ্লাই", T_NAME, NAVY, 700, "start")
    s.text(x0 + bw * 4 + gap * 3 + 8, ytop - 26, "লোড", T_NAME, NAVY,
           700, "end")
    s.line(x0 - 8, ytop - 60, x0 + bw * 4 + gap * 3 + 8, ytop - 60,
           STEEL, 3, marker=ar)

    for i, (name, why, col) in enumerate(items):
        bx = x0 + i * (bw + gap)
        s.rect(bx, ytop, bw, 196, "#FFFFFF", col, 3.0, 13)
        head_bar(s, bx, ytop, bw, 54, name, col)
        for k, ln in enumerate(why.split("\n")):
            s.text(bx + bw / 2, ytop + 104 + k * 34, ln, T_BODY, NAVY,
                   700, "middle")
        s.badge(bx + 26, ytop + 168, "১২৩৪"[i], 19, col, "#FFFFFF", 20)
        if i < 3:
            s.path(f"M {bx + bw + 4} {ytop + 98} L {bx + bw + gap - 4} "
                   f"{ytop + 98}", STEEL, 3.2, marker=ar)

    y = note_strip(s, 400,
                   "একটি যন্ত্র সব বিপদ ঠেকায় না; চারটি মিলে পুরো সুরক্ষা")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_layers.svg")


# ── ৪. MCB — বাইরে ও ভেতরে ───────────────────────────────────────────────
def d04_mcb():
    return pair_panels(
        "d04_mcb", "মিনিয়েচার সার্কিট ব্রেকার",
        [("DIN রেলে বসানো MCB", "ph_mcb.jpg", STEEL),
         ("স্বচ্ছ খোলে ভেতরের অংশ", "ph_mcb_trans.jpg", GREEN)],
        "প্রতিটি পোল ১৮ মিলিমিটার চওড়া; ডিবিতে জায়গার হিসাব এই মাপেই",
        h=548)


# ── ৫. MCB-র ভেতরের অংশ ──────────────────────────────────────────────────
def d05_inside():
    """দুই ফালি করা একটি MCB।

    লেবেল কেবল সেই অংশগুলোতে যেগুলো ছবিতে নির্ভুলভাবে চেনা যায় —
    আর্ক চুটের পাতের থাক, তামার সোলেনয়েড কয়েল, টার্মিনাল আর হাতলের
    ল্যাচ।  বাইমেটাল স্ট্রিপ কোথায় বসে সেটা আঁকা ছবিতে (d06) দেখানো
    হয়েছে — আলোকচিত্রে ওটা অন্য ধাতব পাতের সঙ্গে মিলে যায়, আন্দাজে
    লেবেল বসানোর জায়গা এটা নয়।
    """
    return photo_callouts(
        "d05_inside", "MCB-র ভেতরে", "ph_mcb_cut.jpg",
        left=[("সাপ্লাই টার্মিনাল", 0.24, 0.11),
              ("হাতল ও ল্যাচ", 0.09, 0.44),
              ("স্প্রিং", 0.13, 0.60)],
        right=[("সোলেনয়েড কয়েল", 0.79, 0.54),
               ("আর্ক চুট", 0.65, 0.60),
               ("লোড টার্মিনাল", 0.80, 0.87)],
        note="দুই ফালি করা একটি MCB; সব ক'টি পোলে এই একই যন্ত্রাংশ",
        iw=880)


# ── ৬. থার্মাল ও ম্যাগনেটিক ট্রিপ ────────────────────────────────────────
def d06_trip():
    """একই ব্রেকারে দুটো আলাদা ট্রিপ-ব্যবস্থা, দুই রকম গতিতে।

    প্রথম খসড়ায় দুটো ব্যবস্থাই আঁকা ছিল, কিন্তু তারা **কী করে** সেটা
    ছিল না — পটি বাঁকে, প্লাঞ্জার নামে, তারপর?  পাঠক ধরতে পারত না যে
    দুটো নড়াচড়াই শেষ পর্যন্ত একই ট্রিপ বারে গিয়ে ধাক্কা দেয়।  এখন
    দুই প্যানেলেই লাল তির একটি ট্রিপ বারে গিয়ে থামে, আর বাইমেটালের
    দুই ধাতু আলাদা রঙে, মাঝে জোড়ের রেখা টেনে দেখানো।
    """
    s = SVG(1240, 726)
    s.title("ব্রেকারের দুই ট্রিপ-ব্যবস্থা", T_TITLE)
    ar = s.arrow_defs(RED, "arT", 14)

    pw, gap = 548, 32
    x0 = (1240 - (pw * 2 + gap)) / 2
    PH = 466

    # ── বাঁ প্যানেল: থার্মাল ─────────────────────────────────────────
    px = x0
    panel(s, px, 104, pw, PH, "থার্মাল ট্রিপ", AMBER)
    cx = px + pw / 2
    s.text(cx - 60, 178, "বাইমেটাল স্ট্রিপ", T_NAME, NAVY, 700, "middle")

    for dx, lab, hot in ((-140, "স্বাভাবিক", False),
                         (4, "ওভারলোডে", True)):
        bx = cx + dx
        s.rect(bx - 64, 204, 128, 166, PLATE, LINE, 1.8, 8)
        s.rect(bx - 30, 344, 60, 16, METAL, NAVY, 1.8, 3)   # গোড়ার ব্লক
        if hot:
            # তামা বেশি ছড়ায়, তাই ইনভার-এর দিকে বেঁকে যায়
            s.path("M %g 344 C %g 300 %g 282 %g 244"
                   % (bx - 6, bx - 6, bx + 16, bx + 30), COPPER, 9)
            s.path("M %g 344 C %g 300 %g 288 %g 250"
                   % (bx + 4, bx + 4, bx + 26, bx + 40), "#AFB6BE", 9)
            s.path("M %g 344 C %g 300 %g 285 %g 247"
                   % (bx - 1, bx - 1, bx + 21, bx + 35), NAVY, 1.2)
            for hy in (256, 288, 320):                       # তাপের ঢেউ
                s.path("M %g %g q 9 -9 18 0 q 9 9 18 0"
                       % (bx - 56, hy), AMBER, 2.6)
        else:
            s.path(f"M {bx - 6} 344 L {bx - 6} 240", COPPER, 9)
            s.path(f"M {bx + 4} 344 L {bx + 4} 240", "#AFB6BE", 9)
            s.path(f"M {bx - 1} 344 L {bx - 1} 240", NAVY, 1.2)
        s.text(bx, 398, lab, T_BODY, RED if hot else GREY, 700, "middle")

    # দুই ধাতুর পরিচয় — রঙের নমুনা সহ, নইলে কোন পটি কোনটা বোঝা যায় না
    s.rect(cx - 208, 428, 26, 13, COPPER, COPPER, 0, 3)
    s.text(cx - 172, 440, "তামা", T_TINY, COPPER, 700, "start")
    s.rect(cx - 96, 428, 26, 13, "#AFB6BE", "#AFB6BE", 0, 3)
    s.text(cx - 60, 440, "ইনভার", T_TINY, GREY, 700, "start")
    # তির গিয়ে ট্রিপ বারে ঠেকে
    s.path(f"M {cx + 74} 248 L {cx + 128} 248", RED, 3.2, marker=ar)
    s.rect(cx + 140, 216, 18, 132, NAVY, NAVY, 0, 4)
    s.text(cx + 149, 398, "ট্রিপ বার", T_BODY, NAVY, 700, "middle")

    s.text(cx, 500, "গরম হয়ে বেঁকে যায়: সেকেন্ড থেকে মিনিট",
           T_BODY, NAVY, 700, "middle")
    s.text(cx, 542, "কাজ: ওভারলোড", T_NAME, AMBER, 700, "middle")

    # ── ডান প্যানেল: ম্যাগনেটিক ───────────────────────────────────────
    px = x0 + pw + gap
    panel(s, px, 104, pw, PH, "ম্যাগনেটিক ট্রিপ", RED)
    cx = px + pw / 2
    s.text(cx, 178, "সোলেনয়েড কয়েল ও প্লাঞ্জার", T_NAME, NAVY, 700,
           "middle")

    # ফল্ট কারেন্টের লেবেল তারের উপরে, তারের গায়ে নয়
    s.text(px + 36, 232, "ফল্ট কারেন্ট", T_SMALL, RED, 700, "start")
    bolt(s, px + 196, 248, 0.7, "#F2C744")

    ky, kx = 250, cx - 70
    s.rect(kx, ky - 16, 140, 134, "#FFFFFF", LINE, 1.8, 8)
    for i in range(7):
        s.path(f"M {kx + 14} {ky + i * 17} L {kx + 126} {ky + i * 17}",
               COPPER, 6.4)
    s.rect(cx - 22, ky - 8, 44, 118, METAL, NAVY, 2.2, 4)
    s.path(f"M {px + 36} {ky} L {kx + 14} {ky}", C_L, SW)
    node(s, px + 36, ky, C_L, 6)
    s.path(f"M {kx + 126} {ky + 102} L {px + pw - 40} {ky + 102}", C_L, SW)
    node(s, px + pw - 40, ky + 102, C_L, 6)

    s.path(f"M {cx} {ky + 118} L {cx} {ky + 156}", RED, 3.2, marker=ar)
    s.rect(cx - 84, ky + 164, 168, 18, NAVY, NAVY, 0, 4)
    s.text(cx, ky + 216, "ট্রিপ বার", T_BODY, NAVY, 700, "middle")

    s.text(cx, 500, "চুম্বকক্ষেত্র টেনে নামায়; সেকেন্ডের এক-শতাংশে",
           T_BODY, NAVY, 700, "middle")
    s.text(cx, 542, "কাজ: শর্ট সার্কিট", T_NAME, RED, 700, "middle")

    y = note_strip(s, 596,
                   "দুই ব্যবস্থার নড়াচড়া গিয়ে ঠেকে একই ট্রিপ বারে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_trip.svg")


# ── ৭. MCB-র গায়ের লেখা ─────────────────────────────────────────────────
def d07_face():
    """এই অধ্যায়ের কেন্দ্রীয় ছবি — একটি সত্যিকারের MCB-র লেবেল।

    ছবিটা IEK BA47-29-এর, কিন্তু লেখার ছকটি সব ব্র্যান্ডেই এক (IEC
    60898-1 ঠিক করে দিয়েছে) — তাই ওয়ালটন, চিন্ট, সিমেন্স বা এবিবি,
    যেটাই হাতে পড়ুক, একই জায়গায় একই জিনিস খুঁজতে হবে।
    """
    return photo_callouts(
        "d07_face", "MCB-র গায়ের লেখা", "ph_mcb_face.jpg",
        # লিডারের ডগা ছাপা লেখার **পাশে**, লেখার উপরে নয়;  আর ডানের
        # তিনটে আগে ছবির কালো কিনারায় গিয়ে থামত — এখন যথাক্রমে
        # টার্মিনাল-নম্বর, পোল-জোড়ার ড্যাশ-রেখা আর হাতলে।
        left=[("ব্র্যান্ড ও সিরিজ", 0.190, 0.130),
              ("কার্ভ ও রেটেড কারেন্ট", 0.196, 0.410),
              ("রেটেড ভোল্টেজ", 0.194, 0.518),
              ("ব্রেকিং ক্যাপাসিটি", 0.205, 0.699),
              ("শক্তি-সীমার শ্রেণি", 0.230, 0.783)],
        right=[("টার্মিনালের ছক", 0.928, 0.282),
               ("দুই পোল একসঙ্গে চলে", 0.932, 0.414),
               ("হাতল", 0.862, 0.925)],
        note="ছকটি সব ব্র্যান্ডেই এক; IEC 60898-1 ঠিক করে দিয়েছে",
        iw=860)


# ── ৮. ট্রিপ কার্ভ ───────────────────────────────────────────────────────
def d08_curve():
    """B, C, D কার্ভের আদর্শ রূপ — লগ-লগ ছকে।

    সংখ্যাগুলো IEC 60898-1-এর:  তাপীয় অংশে 1.13 গুণে ট্রিপ করবে না,
    1.45 গুণে নির্ধারিত সময়ের ভেতরে করবে; ম্যাগনেটিক অংশে B 3–5,
    C 5–10, D 10–20 গুণ।  ছবিটা মাপা কার্ভ নয়, আদর্শ রূপ — আসল
    সীমা প্রস্তুতকারকের ছকে দেখতে হয়, কথাটা বইয়ের লেখাতেই আছে।

    আঁকার ক্রমটাই এখানে আসল কৌশল:  **খাড়া পটি তিনটে আগে, তাপীয়
    ব্যান্ড তার উপরে**।  তাতে প্রতিটি পটি তাপীয় কার্ভের তলা থেকে
    নেমে এসেছে বলে মনে হয় — যেটা সত্যিই ঘটে, কার্ভটা ওখানেই খাড়া
    হয়ে যায়।  আগের খসড়ায় পটিগুলো সবাই একই উচ্চতা থেকে শুরু হয়ে
    কার্ভ থেকে বিচ্ছিন্ন চৌকো হয়ে ছিল, আর দুটো ব্যাখ্যা-লেখা
    ব্যান্ডের গায়ে বসে পড়ায় পড়াই যেত না।
    """
    s = SVG(1240, 700)
    s.title("ট্রিপ কার্ভ: B, C ও D", T_TITLE)
    arA = s.arrow_defs("#8A5A00", "arA", 12)
    arN = s.arrow_defs(NAVY, "arN", 12)

    X0, XW = 214, 856
    Y0, YH = 148, 396
    MMIN, MMAX = 1.0, 30.0
    TMAX, TMIN = 4000.0, 0.005

    def X(m):
        return X0 + (math.log10(m) - math.log10(MMIN)) / (
            math.log10(MMAX) - math.log10(MMIN)) * XW

    def Y(t):
        return Y0 + (math.log10(TMAX) - math.log10(t)) / (
            math.log10(TMAX) - math.log10(TMIN)) * YH

    s.rect(X0, Y0, XW, YH, "#FCFDFE", LINE, 1.8, 6)

    for m, lab in ((1, "1"), (1.45, "1.45"), (2, "2"), (3, "3"), (5, "5"),
                   (10, "10"), (20, "20"), (30, "30")):
        # 2-এর রেখা "ম্যাগনেটিক অংশ" লেখার আগেই থামে
        yb = Y(0.6) if m == 2 else Y0 + YH
        s.path(f"M {X(m)} {Y0} L {X(m)} {yb}", "#E4EBF2", 1.4)
        s.text(X(m), Y0 + YH + 32, lab, T_SMALL, GREY, 700, "middle")
    for t, lab in ((3600, "1 ঘণ্টা"), (60, "1 মিনিট"), (10, "10 s"),
                   (1, "1 s"), (0.1, "0.1 s"), (0.01, "0.01 s")):
        s.path(f"M {X0} {Y(t)} L {X0 + XW} {Y(t)}", "#E4EBF2", 1.4)
        s.text(X0 - 14, Y(t) + 7, lab, T_SMALL, GREY, 700, "end")

    s.text(X0 + XW / 2, Y0 + YH + 74, "কারেন্ট: রেটেড কারেন্টের গুণিতক",
           T_NAME, NAVY, 700, "middle")
    s.text(64, Y0 + YH / 2 - 6, "ট্রিপ হতে", T_NAME, NAVY, 700, "middle")
    s.text(64, Y0 + YH / 2 + 26, "সময়", T_NAME, NAVY, 700, "middle")

    # ── ম্যাগনেটিক পটি — আগে আঁকা, যাতে ব্যান্ডের তলায় ঢুকে যায় ──
    bands = ((3, 5, 9.0, "B", "#2E6FB7", "#DCE8F6"),
             (5, 10, 3.0, "C", "#1B6E47", "#DCEFE4"),
             (10, 20, 1.3, "D", "#B32A22", "#F8DFDC"))
    for a, b, top, name, col, bg in bands:
        x1, x2 = X(a), X(b)
        s.rect(x1, Y(top), x2 - x1, Y(0.008) - Y(top), bg, col, 2.4, 5)

    # ── তাপীয় অংশ — উপরের ও নিচের সীমা মিলিয়ে একটি ব্যান্ড ──
    up = [(1.45, 3600), (2, 200), (3, 55), (5, 16), (7, 9), (10, 6)]
    lo = [(1.45, 800), (2, 26), (3, 8), (5, 2.6), (7, 1.6), (10, 1.1)]
    d = "M " + " L ".join(f"{X(m):.1f} {Y(t):.1f}" for m, t in up)
    d += " L " + " L ".join(f"{X(m):.1f} {Y(t):.1f}" for m, t in
                            reversed(lo)) + " Z"
    s.path(d, AMBER, 2.2, "#FDF0D6")

    # পটির নাম — নিচের দিকে, ব্যান্ডের অনেক তলায়
    for a, b, top, name, col, bg in bands:
        xm = (X(a) + X(b)) / 2
        s.text(xm, Y(0.085), name, T_NODE, col, 700, "middle")
        s.text(xm, Y(0.028), f"{a}-{b}", T_SMALL, col, 700, "middle")

    # ── 1.13 ও 1.45 গুণের খাড়া রেখা ──
    s.path(f"M {X(1.13)} {Y0} L {X(1.13)} {Y(0.6)}", GREEN, 2.4, dash="8 5")
    s.path(f"M {X(1.45)} {Y0} L {X(1.45)} {Y(0.6)}", RED, 2.4, dash="8 5")
    s.text(X0, Y0 - 24, "1.13 গুণ: ট্রিপ করবে না", T_SMALL, GREEN, 700,
           "start")
    s.text(X0 + 320, Y0 - 24, "1.45 গুণ: ট্রিপ করবে", T_SMALL, RED, 700,
           "start")

    # ── দুই অংশের নাম, ছকের ফাঁকা কোণে, তির দিয়ে দেখানো ──
    s.text(X(15.5), Y(1100), "তাপীয় অংশ", T_BODY, "#8A5A00", 700, "middle")
    s.text(X(15.5), Y(420), "ওভারলোড", T_BODY, "#8A5A00", 700, "middle")
    s.path(f"M {X(12.4)} {Y(300)} L {X(7.2)} {Y(13)}", "#8A5A00", 2.2,
           marker=arA)

    s.text(X(1.62), Y(0.18), "ম্যাগনেটিক অংশ", T_BODY, NAVY, 700, "middle")
    s.text(X(1.62), Y(0.022), "শর্ট সার্কিট", T_BODY, NAVY, 700, "middle")
    s.path(f"M {X(2.35)} {Y(0.05)} L {X(2.85)} {Y(0.05)}", NAVY, 2.2,
           marker=arN)

    y = note_strip(s, Y0 + YH + 108,
                   "একই তাপীয় অংশ, আলাদা ম্যাগনেটিক সীমা; পার্থক্য এটুকুই")
    s.fit(y, 24)
    return s.save(f"{OUT}/d08_curve.svg")


# ── ৯. পোল ──────────────────────────────────────────────────────────────
def d09_poles():
    """SP · SPN · DP · TP · TPN · 4P — কোনটা কী কাটে।"""
    s = SVG(1240, 680)
    s.title("পোল অনুযায়ী ব্রেকার", T_TITLE)

    kinds = [
        ("SP", [("L", C_L, 1)], "এক ফেজ"),
        ("SPN", [("L", C_L, 1), ("N", C_N, 0)], "ফেজ + নিউট্রাল পথ"),
        ("DP", [("L", C_L, 1), ("N", C_N, 1)], "ফেজ + নিউট্রাল"),
        ("TP", [("L1", C_L, 1), ("L2", "#B8860B", 1), ("L3", "#2E6FB7", 1)],
         "তিন ফেজ"),
        ("TPN", [("L1", C_L, 1), ("L2", "#B8860B", 1), ("L3", "#2E6FB7", 1),
                 ("N", C_N, 0)], "তিন ফেজ + নিউট্রাল পথ"),
        ("4P", [("L1", C_L, 1), ("L2", "#B8860B", 1), ("L3", "#2E6FB7", 1),
                ("N", C_N, 1)], "তিন ফেজ + নিউট্রাল"),
    ]
    pw, gap = 186, 16
    x0 = (1240 - (pw * 6 + gap * 5)) / 2
    ytop, ph = 108, 356

    for i, (name, poles, sub) in enumerate(kinds):
        px = x0 + i * (pw + gap)
        s.rect(px, ytop, pw, ph, "#FCFDFE", LINE, 1.8, 11)
        head_bar(s, px, ytop, pw, 52, name, STEEL, T_NODE, 11)

        n = len(poles)
        step = min(40, (pw - 44) / max(n, 1))
        sx = px + pw / 2 - step * (n - 1) / 2
        ya, yb = ytop + 96, ytop + 214
        for k, (lab, col, switched) in enumerate(poles):
            xx = sx + k * step
            s.text(xx, ya - 16, lab, T_SMALL, col, 700, "middle")
            s.path(f"M {xx} {ya} L {xx} {ya + 20}", col, 3.2)
            s.path(f"M {xx} {yb - 20} L {xx} {yb}", col, 3.2)
            node(s, xx, ya + 20, col, 5)
            node(s, xx, yb - 20, col, 5)
            if switched:
                s.path(f"M {xx} {yb - 20} L {xx + 13} {ya + 22}", col, 3.2)
                s.path(f"M {xx - 8} {ya + 12} L {xx + 8} {ya + 12}", col, 2.8)
            else:
                # নিউট্রাল কেবল সুইচ হয়, সুরক্ষা পায় না — সরু, ধূসর
                s.path(f"M {xx} {yb - 20} L {xx + 13} {ya + 22}", DEAD, 2.6,
                       dash="6 4")
        if n > 1:
            # পোলগুলো যান্ত্রিকভাবে বাঁধা — সরু ফুটকি রেখা, মোটা পটি নয়
            # (মোটা পটি কন্টাক্টের বাহুগুলোই ঢেকে দিচ্ছিল)
            s.path(f"M {sx - 14} {ya + 62} L {sx + step * (n - 1) + 14} "
                   f"{ya + 62}", GREY, 2.2)
        for k, ln in enumerate(wrap(sub, pw - 24, T_SMALL, 700)):
            s.text(px + pw / 2, ytop + 268 + k * 30, ln, T_SMALL, NAVY, 700,
                   "middle")

    s.rect(x0, 482, 1240 - 2 * x0, 84, "#F6F8FB", LINE, 1.6, 9)
    s.path(f"M {x0 + 34} 508 L {x0 + 82} 508", GREY, 2.2)
    s.text(x0 + 96, 516, "আড়াআড়ি নিরেট রেখা = পোলগুলো একসঙ্গে চলে",
           T_SMALL, NAVY, 700, "start")
    s.path(f"M {x0 + 34} 548 L {x0 + 82} 548", DEAD, 2.6, dash="6 4")
    s.text(x0 + 96, 556, "ফুটকি বাহু = নিউট্রাল শুধু কাটে, সুরক্ষা দেয় না",
           T_SMALL, NAVY, 700, "start")

    y = note_strip(s, 588,
                   "বাসার মেইনে DP, শাখায় SP; তিন ফেজে TPN বা 4P")
    s.fit(y, 24)
    return s.save(f"{OUT}/d09_poles.svg")


# ── ১০. MCCB-র গায়ের লেখা ───────────────────────────────────────────────
def d10_mccb():
    return photo_callouts(
        "d10_mccb", "MCCB-র গায়ের লেখা", "ph_mccb_face.jpg",
        # বাঁয়ের ডগাগুলো আগে ছাপা অক্ষরের **উপরে** পড়ত (`Ui`-র U, 380/415-র
        # ৩) আর ডানেরগুলো লেবেল ছেড়ে কালো কিনারায় গিয়ে থামত।  এখন
        # প্রতিটি ঠিক তার নিজের সারির পাশে।
        left=[("ব্র্যান্ড ও ফ্রেম", 0.155, 0.190),
              ("ইনসুলেশন ভোল্টেজ", 0.155, 0.248),
              ("ছকের শিরোনাম", 0.155, 0.309),
              ("415 V-এ Icu ও Ics", 0.155, 0.400),
              ("DC-তে ব্যবহার", 0.155, 0.6225)],
        right=[("ইমপালস ভোল্টেজ", 0.720, 0.248),
               ("Ics: শতকরা হিসাবে", 0.888, 0.400),
               ("ক্যাটাগরি A", 0.888, 0.7325),
               ("যে মান মেনে তৈরি", 0.655, 0.8800)],
        note="Ue বদলালে Icu বদলায়; নিজের ভোল্টেজের সারিটিই দেখতে হয়",
        iw=470)


def d11_mccb_trip():
    """ট্রিপ ইউনিটের ফালি — লেবেল উপরে-নিচে, দুই পাশে নয়।

    ছবিটা ৩·৬ঃ১ অনুপাতের।  দুই পাশে লেবেল বসালে চারটে লিডারই
    কোনাকুনি চলে যেত আর ভুল জায়গা দেখাত — প্রথম খসড়ায় ঠিক তা-ই
    হয়েছিল, "শর্ট সার্কিট সেটিং" গিয়ে ঠেকেছিল ফ্রেমের কোণায়।
    """
    return strip_callouts(
        "d11_mccb_trip", "MCCB-র ট্রিপ ইউনিট", "ph_mccb_trip.jpg",
        above=[("ওভারলোড সেটিং", 0.230, 0.230, 0.285),
               ("শর্ট সার্কিট সেটিং", 0.500, 0.500, 0.283),
               ("থার্মাল-ম্যাগনেটিক", 0.858, 0.858, 0.270)],
        below=[("সেটিং ডায়াল", 0.265, 0.297, 0.500),
               ("ট্রিপ কার্ভের ছবি", 0.775, 0.775, 0.550)],
        note="ডায়াল ঘুরিয়ে ওভারলোড সেটিং লোডের FLC-তে নামিয়ে আনা যায়")


# ── ১২. RCCB কীভাবে কাজ করে ──────────────────────────────────────────────
def d12_rccb_work():
    """যাওয়া আর ফেরার হিসাব — RCCB-র গোটা নীতি এইটুকুই।"""
    s = SVG(1240, 690)
    s.title("RCCB কীভাবে কাজ করে", T_TITLE)

    pw, gap = 548, 32
    x0 = (1240 - (pw * 2 + gap)) / 2

    for i, (head, col) in enumerate((("স্বাভাবিক অবস্থা", GREEN),
                                     ("লিকেজ হলে", RED))):
        px = x0 + i * (pw + gap)
        panel(s, px, 104, pw, 442, head, col)
        cx = px + pw / 2
        arf = s.arrow_defs(C_L, f"aL{i}", 13)
        arb = s.arrow_defs(C_N, f"aN{i}", 13)

        ring_x, ring_y = px + 176, 268
        yL, yN = 238, 298
        xin, xout = px + 44, px + pw - 60

        # টরয়েড কোরের ভেতর দিয়ে দুই তার
        s.path(f"M {xin} {yL} L {xout - 96} {yL}", C_L, SW, marker=arf)
        s.path(f"M {xout - 96} {yN} L {xin} {yN}", C_N, SW, marker=arb)
        s.ellipse(ring_x, ring_y, 46, 62, "none", "#7A4520", 13)
        s.ellipse(ring_x, ring_y, 46, 62, "none", "#C98A55", 4)
        s.text(ring_x, 176, "টরয়েড কোর", T_SMALL, NAVY, 700, "middle")
        s.text(xin + 6, yL - 14, "L", T_SMALL, C_L, 700, "start")
        s.text(xin + 6, yN + 26, "N", T_SMALL, NAVY, 700, "start")

        # সেন্সিং কয়েল ও ট্রিপ রিলে
        s.path(f"M {ring_x} {ring_y + 62} L {ring_x} {392}", STEEL, 2.6)
        rx, ry, rw, rh = ring_x - 88, 392, 176, 52
        s.rect(rx, ry, rw, rh, LIGHT if i == 0 else REDBG, col, 2.6, 9)
        s.text(ring_x, ry + 33, "ট্রিপ রিলে: চুপ" if i == 0
               else "ট্রিপ রিলে: ট্রিপ", T_BODY, col, 700, "middle")

        # লোড
        s.rect(xout - 90, yL - 34, 84, 98, "#FFFFFF", NAVY, 2.6, 9)
        s.text(xout - 48, yL + 24, "লোড", T_BODY, NAVY, 700, "middle")
        s.path(f"M {xout - 96} {yL} L {xout - 90} {yL}", C_L, SW)
        s.path(f"M {xout - 90} {yN} L {xout - 96} {yN}", C_N, SW)

        if i == 0:
            s.text(cx, 470, "গেল 5.000 A · ফিরল 5.000 A", T_NAME, NAVY,
                   700, "middle")
            s.text(cx, 506, "পার্থক্য শূন্য", T_NAME, GREEN, 700, "middle")
        else:
            arE = s.arrow_defs(RED, "aE", 13)
            person(s, xout - 48, 382, 0.8)
            s.path(f"M {xout - 48} {yL + 64} L {xout - 48} {350}", RED, 3.0,
                   dash="7 5", marker=arE)
            earth(s, xout - 48, 420, C_PE, 30)
            s.text(cx, 470, "গেল 5.000 A · ফিরল 4.970 A", T_NAME, NAVY,
                   700, "middle")
            s.text(cx, 506, "পার্থক্য 30 mA", T_NAME, RED, 700, "middle")

    y = note_strip(s, 566,
                   "যাওয়া আর ফেরার পার্থক্যই ধরে; লিকেজ কোথায়, তা দেখে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d12_rccb_work.svg")


# ── ১৩. RCCB-র গায়ের লেখা ───────────────────────────────────────────────
def d13_rccb_face():
    return photo_callouts(
        "d13_rccb_face", "RCCB-র গায়ের লেখা", "ph_rccb_face.jpg",
        left=[("ব্র্যান্ড ও মডেল", 0.042, 0.10),
              ("দুই নামেই বিক্রি হয়", 0.042, 0.215),
              ("রেটেড কারেন্ট", 0.042, 0.29),
              ("লিকেজ সেন্সিটিভিটি", 0.042, 0.35),
              ("রেটেড ভোল্টেজ", 0.042, 0.465),
              ("ব্যাকআপ ফিউজের মাপ", 0.042, 0.555)],
        # আগে "টার্মিনালের ছক" গিয়ে ঠেকত পাশের উপর-নিচ তিরচিহ্নে —
        # ছকটিই দেখাত না।  এখন ছাপা ছকের নিচের সারির ডান পাশে।
        right=[("টাইপ AC-র চিহ্ন", 0.330, 0.352, 0.240),
               ("টার্মিনালের ছক", 0.822, 0.576),
               ("টেস্ট বোতাম", 0.925, 0.84)],
        note="30 mA মানুষের জন্য; 100 বা 300 mA শুধু আগুন ঠেকাতে",
        iw=800)


# ── ১৪. RCCB-র ভেতরের টরয়েড ─────────────────────────────────────────────
def d14_toroid():
    return pair_panels(
        "d14_toroid", "RCCB: বাইরে ও ভেতরে",
        [("গোটা যন্ত্র", "ph_rccb.jpg", STEEL),
         ("খোল খুললে", "ph_toroid.jpg", GREEN)],
        "নিউট্রালসহ চারটি তারই কোরের ভেতর দিয়ে গেছে",
        h=548)


# ── ১৫. RCBO ────────────────────────────────────────────────────────────
def d15_rcbo():
    """MCB + RCCB = RCBO — এক মডিউলে দুই কাজ।"""
    s = SVG(1240, 560)
    s.title("RCBO: দুই কাজ এক মডিউলে", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar15", 16)

    def unit(px, py, w, h, name, jobs, col):
        s.rect(px, py, w, h, "#FFFFFF", col, 3.0, 13)
        head_bar(s, px, py, w, 54, name, col)
        for k, j in enumerate(jobs):
            s.check(px + 34, py + 96 + k * 44, 13, col)
            s.text(px + 58, py + 104 + k * 44, j, T_BODY, NAVY, 700, "start")

    unit(96, 132, 312, 232, "MCB", ["ওভারলোড", "শর্ট সার্কিট"], RED)
    s.text(444, 262, "+", 44, GREY, 700, "middle")
    unit(480, 132, 312, 232, "RCCB", ["আর্থ লিকেজ", "বৈদ্যুতিক শক"], GREEN)
    s.path("M 828 248 L 872 248", STEEL, 3.4, marker=ar)
    unit(892, 132, 252, 232, "RCBO",
         ["ওভারলোড", "শর্ট সার্কিট", "আর্থ লিকেজ"], STEEL)

    s.text(252, 402, "এক বা দুই মডিউল", T_SMALL, GREY, 700, "middle")
    s.text(636, 402, "দুই বা চার মডিউল", T_SMALL, GREY, 700, "middle")
    s.text(1018, 402, "এক বা দুই মডিউল", T_SMALL, GREY, 700, "middle")

    y = note_strip(s, 434,
                   "একটি সার্কিট ট্রিপ করলে বাকিগুলো চালু থাকে; এটিই লাভ")
    s.fit(y, 24)
    return s.save(f"{OUT}/d15_rcbo.svg")


# ── ১৬. সার্জ ও SPD ─────────────────────────────────────────────────────
def d16_spd_work():
    """SPD স্বাভাবিক সময়ে খোলা, সার্জের সময়ে বন্ধ — এটুকুই নীতি।"""
    s = SVG(1240, 680)
    s.title("সার্জ কোন পথে যায়", T_TITLE)

    pw, gap = 548, 32
    x0 = (1240 - (pw * 2 + gap)) / 2

    for i, (head, col) in enumerate((("স্বাভাবিক সময়ে", GREEN),
                                     ("সার্জের সময়ে", RED))):
        px = x0 + i * (pw + gap)
        panel(s, px, 104, pw, 432, head, col)
        cx = px + pw / 2
        xin, xload = px + 56, px + pw - 96
        yL, yN = 194, 268
        spdx = px + 236
        wcol = STEEL if i == 0 else RED
        wsw = SW if i == 0 else 6.0

        # SPD-র ড্রপ নিউট্রাল রেখাটা পার হয় — সংযোগ নয়, তাই ফুটকি নয়,
        # ছোট একটি সেতু-চাপ (hop) দিয়ে পার করানো হয়েছে।
        node(s, spdx, yL, SYM, 6)
        s.path(f"M {spdx} {yL} L {spdx} {yN - 11}", wcol, wsw)
        s.path(f"M {spdx} {yN - 11} A 11 11 0 0 1 {spdx} {yN + 11}",
               wcol, wsw)
        s.path(f"M {spdx} {yN + 11} L {spdx} {310}", wcol, wsw)

        s.path(f"M {xin} {yL} L {xload} {yL}", C_L, SW)
        s.path(f"M {xin} {yN} L {xload} {yN}", C_N, SW)
        s.text(xin + 4, yL - 14, "L", T_SMALL, C_L, 700, "start")
        s.text(xin + 4, yN + 26, "N", T_SMALL, NAVY, 700, "start")

        # লোড
        s.rect(xload, yL - 26, 76, 134, "#FFFFFF", NAVY, 2.6, 9)
        s.text(xload + 38, yL + 48, "যন্ত্র", T_BODY, NAVY, 700, "middle")

        s.rect(spdx - 36, 310, 72, 70, LIGHT if i == 0 else REDBG,
               STEEL if i == 0 else RED, 2.8, 8)
        s.text(spdx, 352, "SPD", T_BODY, STEEL if i == 0 else RED, 700,
               "middle")
        s.path(f"M {spdx} {380} L {spdx} {414}", wcol, wsw)
        earth(s, spdx, 418, C_PE, 40)
        s.text(spdx, 466, "আর্থ বার", T_SMALL, C_PE, 700, "middle")

        if i == 0:
            s.text(cx, 508, "SPD পথ বন্ধ রাখে: কারেন্ট যায় না", T_BODY,
                   GREEN, 700, "middle")
        else:
            arS = s.arrow_defs(RED, "aS", 15)
            bolt(s, xin + 78, yL - 30, 1.15, "#F2C744")
            s.path(f"M {spdx + 58} {322} L {spdx + 58} {402}", RED, 3.0,
                   marker=arS)
            s.text(spdx + 116, 344, "সার্জ", T_SMALL, RED, 700, "middle")
            s.text(cx, 508, "পথ খুলে যায়: সার্জ নামে আর্থে", T_BODY, RED,
                   700, "middle")

    y = note_strip(s, 556,
                   "আর্থিং দুর্বল হলে SPD-র কিছুই করার নেই; পথটিই থাকে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d16_spd_work.svg")


# ── ১৭. SPD-র গায়ের লেখা ────────────────────────────────────────────────
def d17_spd_face():
    return photo_callouts(
        "d17_spd_face", "SPD-র গায়ের লেখা", "ph_spd_face.jpg",
        # আগে চারটে রেটিং-লেবেল বাঁ মডিউলের ছাপা `Uc`/`Imax`-এর উপরেই
        # বসত, আর সারিগুলো এত কাছাকাছি (ছবির উচ্চতার ০·০৪) যে লিডার
        # পাখার মতো ছড়িয়ে ভুল সারি দেখাত।  এখন সব রেটিং **ডান**
        # মডিউলের ডান পাশ থেকে, আর প্রতিটি সারির ফাঁক ন্যূনতম
        # দূরত্বের চেয়ে বেশি।  কোন চিহ্ন কী বোঝায় তার পুরো ব্যাখ্যা
        # ঠিক পরের সারণিতেই আছে — ছবিটা কেবল কোথায় তাকাতে হবে বলে।
        left=[("মডেলের নাম", 0.040, 0.185),
              ("সবুজ জানালা: ঠিক আছে", 0.055, 0.440),
              ("টাইপ ও IP শ্রেণি", 0.036, 0.850)],
        right=[("লাল জানালা: বদলাতে হবে", 0.925, 0.440),
               ("Uc: চালু ভোল্টেজ", 0.958, 0.650),
               ("In ও Imax: ডিসচার্জ", 0.958, 0.7145),
               ("Up: সুরক্ষা-স্তর", 0.958, 0.779)],
        note="জানালা লাল হলে গোটা SPD নয়, ওই মডিউলটিই বদলাতে হয়",
        iw=860)


# ── ১৮. ডিবিতে ডিভাইসের ক্রম ────────────────────────────────────────────
def d18_db():
    """একটি ফ্ল্যাটের ডিবি — মিটার থেকে সার্কিট পর্যন্ত এক লাইনে।

    উপর থেকে নিচে, কারণ ডিবির ভেতরেও ক্রমটা ঠিক এই — উপরে বড় রেটিং,
    নিচে শাখা।  সপ্তম ড্রপটি SPD-র:  বাসবার → ব্যাকআপ MCB → SPD →
    আর্থিং বার।  আর্থিং বার নিউট্রাল বারের উপরে আঁকা, যাতে SPD-র তার
    নিউট্রাল বার ডিঙিয়ে যেতে না হয়।
    """
    s = SVG(1240, 940)
    s.title("ডিবিতে ডিভাইসের ক্রম", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar18", 15)

    xm = 620
    chain = [("মিটার", None, STEEL, 152),
             ("মেইন সুইচ", "40 A DP", NAVY, 264),
             ("RCCB", "40 A / 30 mA", GREEN, 366)]
    for i, (name, sub, col, cy) in enumerate(chain):
        w, h = 300, 76
        s.rect(xm - w / 2, cy - h / 2, w, h, "#FFFFFF", col, 3.0, 11)
        if sub:
            s.text(xm, cy - 2, name, T_BODY, col, 700, "middle")
            s.text(xm, cy + 28, sub, T_SMALL, NAVY, 700, "middle")
        else:
            s.text(xm, cy + 8, name, T_NODE, col, 700, "middle")
        if i < len(chain) - 1:
            s.path(f"M {xm} {cy + h / 2 + 2} L {xm} {chain[i + 1][3] - 40}",
                   STEEL, 3.2, marker=ar)

    # ফেজ বাসবার
    by = 470
    bx0, bx1 = 82, 1158
    s.path(f"M {xm} {404} L {xm} {by - 14}", STEEL, 3.2, marker=ar)
    s.rect(bx0, by - 14, bx1 - bx0, 28, "#D8A15E", "#7A4520", 2.2, 4)
    s.text(bx0 + 6, by - 26, "ফেজ বাসবার", T_SMALL, "#7A4520", 700, "start")

    # সাতটি ড্রপ — ছয়টি সার্কিট, একটি SPD
    drops = [("6 A", "বাতি ও ফ্যান ১"), ("6 A", "বাতি ও ফ্যান ২"),
             ("10 A", "সকেট ১"), ("16 A", "রান্নাঘর"),
             ("20 A", "এসি"), ("10 A", "পাম্প"), ("20 A", None)]
    mw, mgap = 140, 16
    n = len(drops)
    mx0 = bx0 + ((bx1 - bx0) - (mw * n + mgap * (n - 1))) / 2
    ytop = 552
    for i, (rating, use) in enumerate(drops):
        mx = mx0 + i * (mw + mgap)
        cx = mx + mw / 2
        s.path(f"M {cx} {by + 14} L {cx} {ytop}", C_L, 3.0)
        s.rect(mx, ytop, mw, 74, "#FFFFFF", RED, 2.8, 10)
        s.text(cx, ytop + 32, "MCB", T_SMALL, RED, 700, "middle")
        s.text(cx, ytop + 61, rating, T_BODY, NAVY, 700, "middle")
        if use:
            for k, ln in enumerate(wrap(use, mw + 14, T_SMALL, 700)):
                s.text(cx, ytop + 108 + k * 28, ln, T_SMALL, GREY, 700,
                       "middle")
        else:
            s.path(f"M {cx} {ytop + 74} L {cx} {ytop + 104}", AMBER, 3.0)
            s.rect(mx + 6, ytop + 104, mw - 12, 62, AMBERBG, AMBER, 2.8, 10)
            s.text(cx, ytop + 143, "SPD", T_BODY, AMBER, 700, "middle")
            s.path(f"M {cx} {ytop + 166} L {cx} {ytop + 196}", AMBER, 3.0)

    # আর্থিং ও নিউট্রাল বার
    for yy, lab, col in ((ytop + 196, "আর্থিং বার", C_PE),
                         (ytop + 252, "নিউট্রাল বার", NAVY)):
        s.rect(bx0, yy - 15, bx1 - bx0, 30, "#EDEFF2", col, 2.4, 5)
        s.text(bx0 + 14, yy + 7, lab, T_SMALL, col, 700, "start")

    y = note_strip(s, ytop + 296,
                   "SPD-ও বাসবার থেকেই খায়; নিজের ব্যাকআপ MCB নিয়ে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d18_db.svg")


# ── ১৯–২০. বাস্তব ডিবি ──────────────────────────────────────────────────
def d19_dbreal():
    return sheet(
        "d19_dbreal", "তারসহ একটি ডিবি", "কনজিউমার ইউনিট",
        "ph_db.jpg",
        "নিচে সব লোড-তার, উপরে নিউট্রাল ও আর্থিং বার; মাঝখানে যন্ত্র",
        iw=680)


def d20_row():
    return sheet(
        "d20_row", "RCCB ও MCB-র সারি", "সার্কিটের নামসহ ডিবি",
        "ph_row.jpg",
        "প্রতিটি ওয়ের গায়ে নাম, আর একটি ওয়ে ইচ্ছে করে খালি রাখা",
        iw=1148)


# ── ২১. নির্বাচনের ধাপ ───────────────────────────────────────────────────
def d21_select():
    """ব্রেকার বাছার সাত ধাপ — উপর থেকে নিচে।"""
    s = SVG(1240, 720)
    s.title("ব্রেকার নির্বাচনের ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar21", 15)

    steps = [
        ("লোড যোগ", "সার্কিটের সব যন্ত্রের ওয়াট"),
        ("কারেন্ট নির্ণয়", "I = P / (V × পাওয়ার ফ্যাক্টর)"),
        ("রেটিং নির্বাচন", "In কমপক্ষে 1.25 গুণ, তারপর স্ট্যান্ডার্ড মান"),
        ("ক্যাবল মিলিয়ে দেখা", "ক্যাবলের ক্ষমতা ব্রেকারের চেয়ে কম নয়"),
        ("কার্ভ নির্বাচন", "B রেজিস্টিভ · C সাধারণ · D উচ্চ ইনরাশ"),
        ("ব্রেকিং ক্যাপাসিটি", "বাসায় 6 kA, ভবনের মেইনে 10 kA"),
        ("পোল ও লিকেজ সুরক্ষা", "SP না DP · RCCB না RCBO"),
    ]
    bw, bh, gap = 1000, 62, 18
    x0 = (1240 - bw) / 2
    y = 112
    for i, (name, sub) in enumerate(steps):
        s.rect(x0, y, bw, bh, "#FCFDFE", STEEL, 2.4, 11)
        s.badge(x0 + 40, y + bh / 2, "১২৩৪৫৬৭"[i], 20, STEEL, "#FFFFFF", 21)
        s.text(x0 + 80, y + bh / 2 + 8, name, T_NAME, NAVY, 700, "start")
        s.text(x0 + bw - 26, y + bh / 2 + 7, sub, T_BODY, GREY, 700, "end")
        if i < len(steps) - 1:
            s.path(f"M {x0 + bw / 2} {y + bh + 2} L {x0 + bw / 2} "
                   f"{y + bh + gap - 2}", STEEL, 2.8, marker=ar)
        y += bh + gap

    yy = note_strip(s, y + 12,
                    "ব্রেকার ক্যাবলকে বাঁচায়; তাই ক্যাবলের চেয়ে বড় নয়")
    s.fit(yy, 24)
    return s.save(f"{OUT}/d21_select.svg")


# ── ২২. প্যানেলে বসানো SPD ──────────────────────────────────────────────
# ── ২২. বাজারের ব্র্যান্ড ────────────────────────────────────────────────
def d22_brands():
    """বাজারে চেনা চার ব্র্যান্ডের MCB, পাশাপাশি।

    অধ্যায়ের মূল দাবিটা — "ছকটি সব ব্র্যান্ডেই এক" — কথায় বলার চেয়ে
    চারটে আসল যন্ত্র পাশাপাশি রেখে দেখানো ঢের জোরালো।  চারটিই
    বাংলাদেশের বাজারে মেলে, আর চারটিরই গায়ে একই ক্রমে একই তথ্য:
    কার্ভ + রেটেড কারেন্ট, চৌকো ঘরে Icn ও শক্তি-সীমার শ্রেণি, রেটেড
    ভোল্টেজ, IEC/EN 60898-1 আর টার্মিনালের ছক।
    """
    items = [("ph_br_schneider.jpg", "Schneider Electric",
              "ফ্রান্স · Acti9 iC60N · B16"),
             ("ph_br_abb.jpg", "ABB", "সুইজারল্যান্ড · S203 · B16"),
             ("ph_br_legrand.jpg", "Legrand", "ফ্রান্স · C16"),
             ("ph_br_chint.jpg", "CHiNT", "চীন · NB1-63 · C2")]
    w, m, gap, top, ih = 1240, 36, 20, 100, 402
    s = SVG(w, top + ih + 240)
    s.title("বাজারের চেনা চার ব্র্যান্ড", T_TITLE)
    n = len(items)
    tile = (w - 2 * m - gap * (n - 1)) / n
    for i, (img, name, sub) in enumerate(items):
        x = m + i * (tile + gap)
        s.rect(x, top, tile, ih + 88, PLATE, LINE, 1.8, 10)
        s.image_fit(x + 12, top + 12, tile - 24, ih - 16, f"{IMG}/{img}", 4)
        s.text(x + tile / 2, top + ih + 34, name, T_BODY, NAVY, 700, "middle")
        s.text(x + tile / 2, top + ih + 66, sub, T_TINY, GREY, 700, "middle")
    y = note_strip(s, top + ih + 122,
                   "চার কারখানা, এক ছক; IEC 60898-1 ঠিক করে দিয়েছে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d22_brands.svg")


def _gallery(fname, title, items, note, w, m, gap, ih, t_name, t_role,
             card_pad=12):
    """যন্ত্র-চেনার সারি — এক লাইনে ছবি, নিচে নাম আর এক-দুই শব্দের কাজ।

    এই ছবির কাজ নেমপ্লেট পড়ানো নয় (সেটা কল-আউট-চিত্রগুলোর), কাজ
    কেবল **চেনানো** — কোনটা দেখতে কেমন।  তাই ছবি ছোট, সাদা পটভূমি,
    এক কোণ, এক আলো; চোখ তখন কেবল আকৃতির পার্থক্যটাই ধরে।
    """
    n = len(items)
    tile = (w - 2 * m - gap * (n - 1)) / n
    top = 100
    s = SVG(w, top + ih + 240)
    s.title(title, T_TITLE)
    for i, (img, name, role) in enumerate(items):
        x = m + i * (tile + gap)
        s.rect(x, top, tile, ih + 84, PLATE, LINE, 1.8, 10)
        # ছবির ঘর সাদা — উৎস-রেন্ডারগুলোর পটভূমিই সাদা, টাইলের হালকা
        # নীলের উপরে বসালে প্রতিটি ছবির চারদিকে একটা সাদা চৌকো ফুটে ওঠে
        s.rect(x + card_pad - 3, top + 7, tile - 2 * (card_pad - 3), ih - 8,
               "#FFFFFF", LINE, 1.2, 7)
        s.image_fit(x + card_pad, top + 10, tile - 2 * card_pad, ih - 14,
                    f"{IMG}/{img}", 3)
        for txt, dy, size, col in ((name, 34, t_name, NAVY),
                                   (role, 66, t_role, GREY)):
            if tw(txt, size, 700) > tile - 10:
                raise ValueError(f"{fname}: টাইলে ধরে না — {txt!r}")
            s.text(x + tile / 2, top + ih + dy, txt, size, col, 700, "middle")
    y = note_strip(s, top + ih + 120, note, size=t_name, pad=m)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def d23_devices():
    """বাসার ডিবিতে যে ছয়টি যন্ত্র বসে — পাশাপাশি, চেনার জন্য।

    ক্রমটা ইচ্ছাকৃতভাবে সারণি ২২.৪-এর ক্রম।  ছবি দেখে নাম, তারপর
    ছকে দেখে কে কোন বিপদটা ঠেকায় — দুটো একই ক্রমে পড়লে মাথায় বসে।
    ছবিগুলো ইনস্টিটিউটের `Standard Markings on Circuit Breakers.docx`
    থেকে (`assets_ch22_dev.py`)।
    """
    return _gallery(
        "d23_devices", "ডিবিতে যে যন্ত্রগুলো বসে",
        [("dev_mcb.jpg", "MCB", "ওভারলোড, শর্ট"),
         ("dev_mccb.jpg", "MCCB", "বড় লোড"),
         ("dev_rccb.jpg", "RCCB", "আর্থ লিকেজ"),
         ("dev_rcbo.jpg", "RCBO", "সব একসঙ্গে"),
         ("dev_spd.jpg", "SPD", "সার্জ"),
         ("dev_isolator.jpg", "আইসোলেটর", "বিচ্ছিন্নকরণ")],
        "ছয়টির কাজ ছয় রকম; একটির বদলে আরেকটি চলে না",
        w=1240, m=24, gap=13, ih=290, t_name=27, t_role=21.5, card_pad=10)


def d24_outside():
    """হাউস ওয়্যারিংয়ের বাইরের চারটি — নাম শুনে যেন থমকে না যায়।"""
    return _gallery(
        "d24_outside", "যেগুলো বাসার ডিবিতে বসে না",
        [("dev_mpcb.jpg", "MPCB", "মোটরের জন্য"),
         ("dev_afdd.jpg", "AFDD", "আর্ক ফল্ট"),
         ("dev_acb.jpg", "ACB", "এলটি প্যানেল"),
         ("dev_vcb.jpg", "VCB", "১১ কেভি")],
        "ACB ও VCB চালানো শুধু অনুমোদিত কর্মীর কাজ",
        w=900, m=22, gap=14, ih=250, t_name=30, t_role=24)


ALL = [d01_faults, d02_fuse_cb, d03_layers, d04_mcb, d05_inside, d06_trip,
       d07_face, d08_curve, d09_poles, d10_mccb, d11_mccb_trip,
       d12_rccb_work, d13_rccb_face, d14_toroid, d15_rcbo, d16_spd_work,
       d17_spd_face, d18_db, d19_dbreal, d20_row, d21_select,
       d22_brands, d23_devices, d24_outside,
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
