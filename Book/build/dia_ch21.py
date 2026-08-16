# -*- coding: utf-8 -*-
"""অধ্যায় ২১ — বাসবার : ডায়াগ্রাম।

সার্কিট ও কানেকশন ডায়াগ্রাম ইনস্টিটিউটের নিজের ডেক থেকে হুবহু বসানো —
`HW Connection Diagram All.pptx` স্লাইড ২৯, ৩১, ৩২, ৩৩, আর `Busbar
All.pptx`-এর ভেতরের ছবি (`assets_ch21.py`)।  হাতে নতুন করে আঁকা হয়নি,
কারণ হাতে আঁকলেই টপোলজি বদলে যাওয়ার ঝুঁকি (অধ্যায় ৬-এর অভিজ্ঞতা)।

**ইনস্টিটিউটের স্লাইড ৭ ইচ্ছে করে বসানো হয়নি** — ওতে লেখা
`KVA = 1000*V*I`, হাজার দিয়ে গুণ।  ভাগ হওয়ার কথা।  d12-এর ফ্লো-চার্ট
ওই স্লাইডেরই সাজানো রূপ, সূত্র দুটি ঠিক করে নেওয়া।

যা সোর্সে নেই — জোড়ার শিকলের সঙ্গে বাসবারের তুলনা, বারের মাপ ও
প্রস্থচ্ছেদ, প্রকারভেদ, বিএনবিসির রঙের কোড, হিসাবের ধাপ, বসানোর
নিয়ম আর সাধারণ ত্রুটি — এগুলো নতুন আঁকা।

লেবেলের নিয়ম (অধ্যায় ১৫ থেকে কড়া):  প্যানেলের শিরোনাম বিশেষ্য,
যন্ত্রাংশের লেবেল এক-দুই শব্দ, নিচে এক লাইনের একটি নোট-পটি।  কারণ,
পরামর্শ ও সতর্কবাণী সবই বইয়ের লেখায় — ছবিতে নয়।

কালপুরুষে `²`, `√`, `÷` নেই (বা ভুল আঁকে)।  তাই ছবির লেবেলে
প্রস্থচ্ছেদের একক "বর্গমিলিমিটার" কথায়, তিনের বর্গমূল "1.732" সংখ্যায়,
আর ভাগ সবসময় `/` দিয়ে।
"""
import os

from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch21")
IMG = os.path.join(HERE, "assets", "ch21")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
T_CALL = 24
T_TINY = 18.5

SYM = "#12324D"
SW = 3.4
CU = "#B5713A"              # তামা
CU_D = "#7A4520"
AL = "#A8AEB4"              # অ্যালুমিনিয়াম
AL_D = "#6E757C"
DEAD = "#9AA6B2"
BOXG = "#E7ECF1"
PLATE = "#F4F7FA"
METAL = "#8D9AA8"

# বিএনবিসি ১.৩.৯.৩.১৫-এর রং — ছবির বারগুলোতেও ঠিক এই রং
C_L1 = "#D42A1F"
C_L2 = "#E8B21C"
C_L3 = "#2E6FB7"
C_N = "#1F2933"
C_PE = "#1B6E47"


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


def _ih(img, w):
    from PIL import Image as _Im
    with _Im.open(f"{IMG}/{img}") as im:
        iw_, ih_ = im.size
    return round(w * ih_ / iw_)


def sheet(fname, title, head, img, note, iw=1080, top=100):
    """একটি সোর্স-ছবির শিট — শিরোনাম, প্যানেল, এক লাইনের নোট।"""
    ph = _ih(img, iw - 32) + 78
    x0 = (1240 - iw) / 2
    s = SVG(1240, top + ph + 112)
    s.title(title, T_TITLE)
    img_panel(s, x0, top, iw, ph, head, img)
    y = note_strip(s, top + ph + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def strip_panels(fname, title, items, note, gap=24, top=100, pw=None):
    """পাশাপাশি কয়েকটি ছবি-প্যানেল, নিচে এক লাইনের নোট।

    items = [(প্যানেল-শিরোনাম, ফাইলনাম, রং), …]
    """
    n = len(items)
    pw = pw or (1148 - gap * (n - 1)) / n
    ph = max(_ih(img, pw - 32) for _t, img, _c in items) + 78
    x0 = (1240 - (pw * n + gap * (n - 1))) / 2
    s = SVG(1240, top + ph + 112)
    s.title(title, T_TITLE)
    for i, (head, img, col) in enumerate(items):
        img_panel(s, x0 + i * (pw + gap), top, pw, ph, head, img, col)
    y = note_strip(s, top + ph + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def photo_callouts(fname, title, img, left, right, note,
                   iw=430, top=104, gap=36, size=T_CALL, w=1240):
    """একটি আলোকচিত্র মাঝখানে, দুই পাশে লেবেল ও লিডার।

    অধ্যায় ১৯-এ শেখা তিনটি ফাঁদ এখানেই বাঁধা আছে:  (ক) ছবিটা আগে আঁকো,
    লিডার পরে — উল্টো করলে ছবিই লিডার ঢেকে দেয়;  (খ) লিডারের ডগা
    ছাপা লেখার পাশে রাখো, লেখার উপরে নয়;  (গ) প্রতিটি লেবেল তার
    নিজের লক্ষ্যের সমান উচ্চতায় বসে, নইলে একটি লিডার গোটা ছবি
    কোনাকুনি চিরে যায়।
    """
    ih = _ih(img, iw)
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


def bar3d(s, x, y, w, h, d=16, face=CU, edge=CU_D, holes=0):
    """একটি ফ্ল্যাট বারের ছোট ত্রিমাত্রিক ছবি।"""
    s.poly([(x, y), (x + d, y - d), (x + w + d, y - d), (x + w, y)],
           edge, edge, 1.6)
    s.poly([(x + w, y), (x + w + d, y - d), (x + w + d, y - d + h),
            (x + w, y + h)], edge, edge, 1.6)
    s.rect(x, y, w, h, face, edge, 1.8, 0)
    for i in range(holes):
        cx = x + w * (i + 0.5) / holes
        s.ellipse(cx, y + h / 2, 5.5, 4.2, "#FFFFFF", edge, 1.5)


def lamp(s, cx, cy, r=17, col=AMBER):
    s.circle(cx, cy, r, "#FFFFFF", NAVY, 2.6)
    s.path(f"M {cx - r * 0.7} {cy - r * 0.7} L {cx + r * 0.7} {cy + r * 0.7}",
           NAVY, 2.2)
    s.path(f"M {cx + r * 0.7} {cy - r * 0.7} L {cx - r * 0.7} {cy + r * 0.7}",
           NAVY, 2.2)


# ── ১. কেন বাসবার — জোড়ার শিকল বনাম সাধারণ বার ─────────────────────────
def d01_why():
    return strip_panels(
        "d01_why", "কেন বাসবার",
        [("তারে-তারে জোড়া", "b_wires.png", RED),
         ("বাসবার থেকে ট্যাপ", "b_taps.png", GREEN)],
        "একটি বার — যত সংযোগ লাগে, সব একই ধাতুর গায়ে, আলাদা জোড়া নয়",
        pw=548)


# ── ২. একই সংযোগ দুইভাবে ────────────────────────────────────────────────
def d02_concept():
    """বাঁয়ে জোড়ার শিকল, ডাইনে সাধারণ বার — একই চারটি লোড।

    বাঁ পাশের শিকলে কারেন্ট প্রথম জোড়া দিয়েই চারটি লোডের সবটা বয়,
    তাই জোড়াগুলো ক্রমেই ছোট দেখানো হয়েছে (ভার কমে আসে)।  ডান পাশে
    প্রতিটি লোড বার থেকে নিজের ট্যাপে নামে — বারের ভার সবখানে সমান।
    """
    s = SVG(1240, 640)
    s.title("একই চারটি লোড — দুইভাবে", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 14)

    ytop, ybar, yload = 150, 300, 470
    for side, x0, head, col in ((0, 60, "জোড়ার শিকল", RED),
                                (1, 660, "বাসবার", GREEN)):
        panel(s, x0, 108, 520, 452, head, col)
        xs = [x0 + 116 + i * 104 for i in range(4)]
        xl, xn = x0 + 62, x0 + 26        # লাইভ ও নিউট্রাল আলাদা খাড়া পথে

        # সাপ্লাই নামছে
        s.path(f"M {xl} {ytop} L {xl} {ybar}", C_L1, SW)
        s.path(f"M {xn} {ytop} L {xn} {yload + 54} L {xs[0]} {yload + 54}",
               C_N, SW)
        s.text(xl + 6, ytop - 14, "L", T_SMALL, C_L1, 700, "start")
        s.text(xn - 6, ytop - 14, "N", T_SMALL, NAVY, 700, "end")
        s.text((xl + xn) / 2, ytop - 44, "সাপ্লাই", T_SMALL, NAVY, 700,
               "middle")
        node(s, xl, ybar, C_L1)

        if side == 0:
            # শিকল: এক তার থেকে পরের তার, প্রতিটি সংযোগে একটি জোড়া
            prev = xl
            for i, x in enumerate(xs):
                s.path(f"M {prev} {ybar} L {x} {ybar}", C_L1,
                       SW + 1.2 - i * 0.25)
                s.circle(x, ybar, 11, "#FFFFFF", RED, 3)
                s.path(f"M {x - 6} {ybar - 6} L {x + 6} {ybar + 6}", RED, 2.4)
                s.path(f"M {x + 6} {ybar - 6} L {x - 6} {ybar + 6}", RED, 2.4)
                prev = x
            s.text(x0 + 268, ybar - 36, "প্রতিটি ✕ একেকটি জোড়া",
                   T_SMALL, RED, 700, "middle")
        else:
            # বার: একটানা ধাতু, গা থেকে ট্যাপ
            bar3d(s, x0 + 56, ybar - 15, 424, 30, 12, CU, CU_D)
            s.text(x0 + 268, ybar - 42, "একটানা তামার বার",
                   T_SMALL, GREEN, 700, "middle")

        for x in xs:
            s.path(f"M {x} {ybar + (15 if side else 0)} L {x} {yload - 26}",
                   C_L1, SW)
            lamp(s, x, yload)
            s.path(f"M {x} {yload + 17} L {x} {yload + 54}", C_N, SW)
        s.path(f"M {xs[0]} {yload + 54} L {xs[-1]} {yload + 54}", C_N, SW)

    y = note_strip(s, 578,
                   "শিকলের প্রথম জোড়া চারটি লোডেরই কারেন্ট বয় — "
                   "বার বয় সমান ভাগে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_concept.svg")


# ── ৩. উপাদান — তামা, অ্যালুমিনিয়াম, বাস্তব বার ─────────────────────────
def d03_material():
    return strip_panels(
        "d03_material", "বাসবারের উপাদান",
        [("তামার বার", "b_cu.png", STEEL),
         ("অ্যালুমিনিয়াম বার", "b_al.png", GREY),
         ("বাজারের কাঁচা বার", "ph_raw.jpg", GREEN)],
        "একই কারেন্টে অ্যালুমিনিয়ামের বার তামার চেয়ে দেড়-দুই গুণ চওড়া লাগে")


# ── ৪. বারের মাপ ও প্রস্থচ্ছেদ ───────────────────────────────────────────
def d04_dims():
    """প্রস্থ, পুরুত্ব, দৈর্ঘ্য — আর কোনটা হিসাবে লাগে।

    ইনস্টিটিউটের ৫ নং স্লাইডের বাংলা রূপ।  সেখানে লেবেল ছিল L / W / H;
    এখানে বাংলা নাম, আর ডান পাশে প্রস্থচ্ছেদের চৌকো আলাদা করে আঁকা —
    দৈর্ঘ্য যে হিসাবে ঢোকে না, ছাত্ররা সেখানেই ভুল করে।
    """
    s = SVG(1240, 600)
    s.title("বারের মাপ ও প্রস্থচ্ছেদ", T_TITLE)

    # ── বাঁয়ে: ত্রিমাত্রিক বার ─────────────────────────────────────
    # মাপের নাম বাংলায় লিখলে সেগুলো প্যানেলের কিনারা ছাড়িয়ে যায়
    # (qc.py প্রথম দফায় ধরেছিল)।  তাই ছবিতে কেবল L / W / T, আর নিচে
    # তিন লাইনের একটি ছোট তালিকা।
    panel(s, 60, 104, 620, 380, "বারের তিন মাপ", STEEL)
    bx, by, bw, bh, dd = 168, 232, 372, 48, 44
    bar3d(s, bx, by, bw, bh, dd, CU, CU_D, holes=5)

    # দৈর্ঘ্য L
    s.line(bx, by + bh + 44, bx + bw, by + bh + 44, NAVY, 2.2,
           marker=s.arrow_defs(NAVY, "a2", 12))
    s.line(bx + bw, by + bh + 44, bx, by + bh + 44, NAVY, 2.2,
           marker=s.arrow_defs(NAVY, "a3", 12))
    s.text(bx + bw / 2, by + bh + 34, "L", T_NAME, NAVY, 700, "middle")
    for x in (bx, bx + bw):
        s.path(f"M {x} {by + bh} L {x} {by + bh + 54}", GREY, 1.6, dash="5 4")

    # পুরুত্ব T
    s.line(bx - 30, by, bx - 30, by + bh, NAVY, 2.2,
           marker=s.arrow_defs(NAVY, "a4", 12))
    s.line(bx - 30, by + bh, bx - 30, by, NAVY, 2.2,
           marker=s.arrow_defs(NAVY, "a5", 12))
    s.text(bx - 44, by + bh / 2 + 8, "T", T_NAME, NAVY, 700, "end")

    # প্রস্থ W — কাত পাশ বরাবর
    s.path(f"M {bx + bw + dd + 20} {by - dd + 6} "
           f"L {bx + bw + 20} {by + 6}", NAVY, 2.2,
           marker=s.arrow_defs(NAVY, "a6", 12))
    s.text(bx + bw + dd + 30, by - dd + 2, "W", T_NAME, NAVY, 700, "start")

    for i, (tag, nm) in enumerate((("L", "দৈর্ঘ্য"), ("W", "প্রস্থ"),
                                   ("T", "পুরুত্ব"))):
        yy = 388 + i * 32
        s.text(212, yy, tag, T_BODY, NAVY, 700, "end")
        s.text(230, yy, "— " + nm, T_BODY, STEEL, 700, "start")

    # ── ডাইনে: প্রস্থচ্ছেদ ─────────────────────────────────────────
    panel(s, 700, 104, 480, 380, "প্রস্থচ্ছেদ", GREEN)
    cx, cy, cw, ch_ = 800, 230, 280, 66
    s.rect(cx, cy, cw, ch_, CU, CU_D, 2.4, 0)
    s.line(cx, cy - 30, cx + cw, cy - 30, NAVY, 2.2,
           marker=s.arrow_defs(NAVY, "a7", 12))
    s.line(cx + cw, cy - 30, cx, cy - 30, NAVY, 2.2,
           marker=s.arrow_defs(NAVY, "a8", 12))
    s.text(cx + cw / 2, cy - 40, "W", T_NAME, NAVY, 700, "middle")
    s.line(cx + cw + 30, cy, cx + cw + 30, cy + ch_, NAVY, 2.2,
           marker=s.arrow_defs(NAVY, "a9", 12))
    s.line(cx + cw + 30, cy + ch_, cx + cw + 30, cy, NAVY, 2.2,
           marker=s.arrow_defs(NAVY, "a10", 12))
    s.text(cx + cw + 44, cy + ch_ / 2 + 8, "T", T_NAME, NAVY, 700, "start")

    s.rect(760, 350, 360, 104, GREENBG, GREEN, 2.4, 12)
    s.text(940, 386, "প্রস্থচ্ছেদ  A = W × T", T_NODE, NAVY, 700, "middle")
    s.text(940, 428, "একক — বর্গমিলিমিটার", T_SMALL, STEEL, 700, "middle")

    y = note_strip(s, 512,
                   "দৈর্ঘ্য প্রস্থচ্ছেদে ঢোকে না — কারেন্ট ক্ষমতা "
                   "প্রস্থ ও পুরুত্বের গুণফলে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_dims.svg")


# ── ৫. প্রকারভেদ ────────────────────────────────────────────────────────
def d05_types():
    """তিন চেহারার বাসবার — ফ্ল্যাট বার, টার্মিনাল বার, ট্রাংকিং।"""
    s = SVG(1240, 620)
    s.title("বাসবারের প্রকারভেদ", T_TITLE)

    pw, gap, top, ph = 364, 28, 104, 386
    heads = [("ফ্ল্যাট বার", STEEL), ("টার্মিনাল বার", GREEN),
             ("বাসবার ট্রাংকিং", NAVY)]
    for i, (head, col) in enumerate(heads):
        x0 = 60 + i * (pw + gap)
        panel(s, x0, top, pw, ph, head, col)
        cx = x0 + pw / 2

        if i == 0:
            # খোলা ফ্ল্যাট বার, ইনসুলেটরে বসানো
            for j, c in enumerate((C_L1, C_L2, C_L3)):
                by = 210 + j * 58
                s.rect(x0 + 46, by, 272, 26, c, "#00000022", 1.4, 3)
                for sx in (x0 + 78, x0 + 286):
                    s.rect(sx - 11, by + 26, 22, 16, METAL, GREY, 1.4, 2)
                    s.rect(sx - 15, by + 42, 30, 12, "#5B6670", GREY, 1.4, 2)
            s.text(cx, 420, "প্যানেলে, বড় কারেন্টে", T_SMALL, STEEL, 700,
                   "middle")
            s.text(cx, 452, "খোলা ধাতু — ছোঁয়া যায় না", T_TINY, RED, 700,
                   "middle")
        elif i == 1:
            # সারি সারি স্ক্রু-টার্মিনালওয়ালা বার (ডিবির নিউট্রাল/আর্থ)
            for j, (c, nm) in enumerate(((C_N, "N"), (C_PE, "PE"))):
                by = 224 + j * 92
                s.rect(x0 + 52, by, 260, 30, CU, CU_D, 1.8, 3)
                for k in range(8):
                    tx = x0 + 66 + k * 34
                    s.rect(tx - 9, by - 14, 18, 20, METAL, GREY, 1.4, 2)
                    s.path(f"M {tx - 5} {by - 4} L {tx + 5} {by - 4}",
                           "#3A424A", 2)
                s.text(x0 + 40, by + 22, nm, T_SMALL, c, 700, "end")
            s.text(cx, 420, "ঘরের ডিবি-তে", T_SMALL, STEEL, 700, "middle")
            s.text(cx, 452, "নিউট্রাল ও আর্থিং", T_TINY, GREEN, 700, "middle")
        else:
            # ঢাকা ট্রাংকিং, গায়ে ট্যাপ-অফ বাক্স
            s.rect(x0 + 58, 196, 250, 62, BOXG, GREY, 2.4, 6)
            for j, c in enumerate((C_L1, C_L2, C_L3, C_N)):
                s.rect(x0 + 70, 206 + j * 12, 226, 7, c, "none", 0)
            s.rect(x0 + 58, 268, 250, 62, BOXG, GREY, 2.4, 6)
            for j, c in enumerate((C_L1, C_L2, C_L3, C_N)):
                s.rect(x0 + 70, 278 + j * 12, 226, 7, c, "none", 0)
            s.rect(x0 + 236, 330, 78, 56, PLATE, STEEL, 2.4, 6)
            s.text(x0 + 275, 364, "ট্যাপ-অফ", T_TINY, NAVY, 700, "middle")
            s.text(cx, 420, "উঁচু ভবনের রাইজারে", T_SMALL, STEEL, 700,
                   "middle")
            s.text(cx, 452, "ঢাকা, ইনসুলেটেড", T_TINY, NAVY, 700, "middle")

    y = note_strip(s, 500,
                   "ঘরের ডিবিতে যেটাকে বাসবার বলা হয়, সেটি "
                   "টার্মিনাল বার — ফ্ল্যাট বার নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_types.svg")


# ── ৬. মেইন প্যানেলে বাসবার ─────────────────────────────────────────────
def d06_main():
    return sheet(
        "d06_main", "মেইন প্যানেলে বাসবার", "কানেকশন ডায়াগ্রাম",
        "h29_main.png",
        "মিটার ও MCCB-র পরে বার — এরপর সব সংযোগ বারের গা থেকেই",
        iw=1120)


# ── ৭. রঙের কোড ও বার সাজানো ────────────────────────────────────────────
def d07_colour():
    """বিএনবিসি ১.৩.৯.৩.১৫ — বাঁয়ে কোড, ডাইনে বাস্তব প্যানেল।"""
    ph_w = 470
    ih = _ih("ph_panel.jpg", ph_w - 32)
    top, ph = 104, max(ih + 78, 396)
    s = SVG(1240, top + ph + 112)
    s.title("বারের রং ও সাজানোর ক্রম", T_TITLE)

    panel(s, 60, top, 630, ph, "রঙের কোড", STEEL)
    rows = [(C_L1, "L1", "লাল", "ফেজ ১"),
            (C_L2, "L2", "হলুদ", "ফেজ ২"),
            (C_L3, "L3", "নীল", "ফেজ ৩"),
            (C_N, "N", "কালো", "নিউট্রাল"),
            (C_PE, "PE", "সবুজ-হলুদ", "আর্থিং")]
    y0 = top + 70
    for i, (c, tag, colname, role) in enumerate(rows):
        yy = y0 + i * 60
        s.rect(96, yy, 300, 34, c, "#00000033", 1.6, 4)
        if tag == "PE":                       # দ্বিরঙা — হলুদ ডোরা
            for k in range(9):
                s.path(f"M {110 + k * 34} {yy + 34} L {124 + k * 34} {yy}",
                       C_L2, 7)
            s.rect(96, yy, 300, 34, "none", "#00000033", 1.6, 4)
        s.text(414, yy + 26, tag, T_NAME, NAVY, 700, "start")
        s.text(474, yy + 26, colname, T_BODY, STEEL, 700, "start")
        s.text(660, yy + 26, role, T_BODY, NAVY, 700, "end")

    panel(s, 710, top, ph_w, ph, "বাস্তব প্যানেল", GREEN)
    s.image_fit(726, top + 64, ph_w - 32, ph - 78, f"{IMG}/ph_panel.jpg", 6)

    y = note_strip(s, top + ph + 26,
                   "উপর থেকে নিচে L1-L2-L3, সবার নিচে নিউট্রাল — "
                   "ক্রম সব প্যানেলে এক")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_colour.svg")


# ── ৮. আর্থিং ও নিউট্রাল বার ────────────────────────────────────────────
def d08_earth():
    return photo_callouts(
        "d08_earth", "আর্থিং ও নিউট্রাল বার", "ph_earth.jpg",
        left=[("তামার পাত", 0.30, 0.55),
              ("স্ক্রু টার্মিনাল", 0.13, 0.72)],
        right=[("সবুজ-হলুদ PE", 0.46, 0.33),
               ("নীল নিউট্রাল", 0.63, 0.20),
               ("বার-সাপোর্ট", 0.52, 0.62)],
        note="প্রতিটি তার নিজের স্ক্রুতে — এক ছিদ্রে দুই তার নয়",
        iw=880)


# ── ৯. সাব-মিটারের সারি ─────────────────────────────────────────────────
def d09_submeter():
    return sheet(
        "d09_submeter", "বাসবার থেকে সাব-মিটার", "কানেকশন ডায়াগ্রাম",
        "h31_submeter.png",
        "ভাড়াটে বাড়ির ছক — এক বার থেকে প্রতিটি ফ্ল্যাটের নিজের মিটার",
        iw=1120)


# ── ১০. এক বার, দুই রকম আউটপুট ──────────────────────────────────────────
def d10_3p1p():
    return sheet(
        "d10_3p1p", "এক বাসবার থেকে ৩Φ ও ১Φ", "কানেকশন ডায়াগ্রাম",
        "h32_3p1p.png",
        "তিন ফেজের যেকোনো একটি আর নিউট্রাল — এই জোড়াই এক ফেজের সাপ্লাই",
        iw=1120)


# ── ১১. ফ্ল্যাটের এসডিবি ────────────────────────────────────────────────
def d11_sdb():
    return sheet(
        "d11_sdb", "ফ্ল্যাটের এসডিবি-তে বার", "কানেকশন ডায়াগ্রাম",
        "h33_sdb.png",
        "নিউট্রাল বার উপরে, আর্থিং বার নিচে — দুটি কখনো এক করা নয়",
        iw=1120)


# ── ১২. হিসাবের ধাপ ─────────────────────────────────────────────────────
def d12_calc():
    """লোড → কারেন্ট → প্রস্থচ্ছেদ → সারণির মাপ।

    ইনস্টিটিউটের ৭ নং স্লাইডের সাজানো রূপ।  ওই স্লাইডে লেখা ছিল
    `KVA = 1000*V*I` — হাজার দিয়ে গুণ, অথচ ভাগ হওয়ার কথা।  এখানে
    সূত্র দুটি ঠিক করে নেওয়া, আর তিনের বর্গমূল সংখ্যায় (1.732) লেখা,
    কারণ কালপুরুষে √ নেই।
    """
    s = SVG(1240, 700)
    s.title("বাসবার হিসাবের ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)

    cx = 620
    blk(s, cx, 150, "মোট লোড  (kW বা kVA)", 440, 66, LIGHT, STEEL, T_NODE)
    s.line(cx, 183, cx, 224, STEEL, 3, marker=ar)

    # দুই ভাগ — এক ফেজ, তিন ফেজ
    for x0, head, expr, col in (
            (200, "এক ফেজ", "I = P / (V × cos φ)", STEEL),
            (700, "তিন ফেজ", "I = P / (1.732 × V × cos φ)", NAVY)):
        w = max(tw(expr, T_BODY, 700) + 56, 340)
        s.rect(x0, 232, w, 96, "#FFFFFF", col, 2.6, 12)
        s.text(x0 + w / 2, 264, head, T_SMALL, col, 700, "middle")
        s.text(x0 + w / 2, 304, expr, T_BODY, NAVY, 700, "middle")
        s.path(f"M {x0 + w / 2} {328} L {x0 + w / 2} {366} L {cx} {366}",
               STEEL, 3)
    s.line(cx, 366, cx, 404, STEEL, 3, marker=ar)

    blk(s, cx, 438, "কারেন্ট  I  (অ্যাম্পিয়ার)", 440, 66, AMBERBG, AMBER,
        T_NODE)
    s.line(cx, 471, cx, 512, STEEL, 3, marker=ar)

    s.rect(cx - 260, 520, 520, 96, GREENBG, GREEN, 2.6, 12)
    s.text(cx, 556, "প্রস্থচ্ছেদ  A = I / J", T_NODE, NAVY, 700, "middle")
    s.text(cx, 594, "J — কারেন্ট ডেনসিটি, উপাদান অনুযায়ী", T_SMALL, STEEL,
           700, "middle")

    # ডান পাশে শেষ ধাপ — বাক্সটা হাতে আঁকা, blk() নয়:  blk() নিজেই
    # লেখা বসায়, তার উপরে আবার দুই লাইন লিখলে qc.py লেখায়-লেখায়
    # ওভারল্যাপ ধরে (প্রথম দফায় ধরেছিল)।
    s.path(f"M {cx + 260} {568} L {1006} {568}", STEEL, 3, marker=ar)
    s.rect(1024, 520, 176, 96, LIGHT, STEEL, 2.6, 12)
    s.text(1112, 558, "সারণি থেকে", T_BODY, NAVY, 700, "middle")
    s.text(1112, 596, "W × T", T_NODE, NAVY, 700, "middle")

    y = note_strip(s, 646,
                   "হিসাবের ফল যত, বাজারের মাপ তার পরের ধাপে — "
                   "নিচেরটা কখনো নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d12_calc.svg")


# ── ১৩. বসানোর নিয়ম ────────────────────────────────────────────────────
def d13_mount():
    """স্ট্যান্ড-অফ ইনসুলেটর, সাপোর্টের ব্যবধান, জোড়ার বোল্ট।"""
    s = SVG(1240, 660)
    s.title("বার বসানোর নিয়ম", T_TITLE)

    # ── বাঁয়ে: সাপোর্টে বসানো বার, পাশ থেকে ─────────────────────
    panel(s, 60, 104, 620, 420, "সাপোর্টে বসানো", STEEL)
    base = 430
    s.rect(96, base, 548, 22, "#D9DEE3", GREY, 2, 3)
    xs = [170, 340, 510]
    for x in xs:
        s.rect(x - 20, base - 74, 40, 74, "#C9713C", "#8A4A22", 2, 4)
        for k in range(3):
            s.line(x - 24, base - 62 + k * 22, x + 24, base - 62 + k * 22,
                   "#8A4A22", 1.6)
        s.rect(x - 26, base - 86, 52, 14, METAL, GREY, 1.8, 3)
    s.rect(120, base - 104, 500, 20, C_L1, "#00000033", 1.6, 3)
    for x in xs:
        s.circle(x, base - 94, 5.5, METAL, GREY, 1.4)

    # ব্যবধানের মাপ
    s.line(xs[0], base - 140, xs[1], base - 140, NAVY, 2.2,
           marker=s.arrow_defs(NAVY, "b1", 12))
    s.line(xs[1], base - 140, xs[0], base - 140, NAVY, 2.2,
           marker=s.arrow_defs(NAVY, "b2", 12))
    s.text(255, base - 152, "সাপোর্টের ব্যবধান", T_SMALL, NAVY, 700,
           "middle")
    s.text(370, base + 62, "স্ট্যান্ড-অফ ইনসুলেটর", T_NAME, NAVY, 700,
           "middle")

    # ── ডাইনে: জোড়ার বোল্ট ───────────────────────────────────────
    panel(s, 700, 104, 480, 420, "জোড়ার বোল্ট", GREEN)
    jy = 250
    s.rect(736, jy, 240, 30, CU, CU_D, 2, 3)
    s.rect(900, jy + 30, 240, 30, CU, CU_D, 2, 3)
    s.rect(900, jy, 76, 30, CU_D, CU_D, 2, 3)          # ওভারল্যাপ
    for bx in (918, 958):
        s.rect(bx - 9, jy - 18, 18, 18, METAL, GREY, 1.6, 2)   # বোল্টের মাথা
        s.rect(bx - 13, jy - 22, 26, 6, "#5B6670", GREY, 1.4, 1)  # ওয়াশার
        s.rect(bx - 4, jy, 8, 60, METAL, GREY, 1.4, 0)
        s.rect(bx - 11, jy + 60, 22, 14, "#5B6670", GREY, 1.6, 2)  # নাট
    s.text(938, jy - 40, "ওভারল্যাপ", T_SMALL, GREEN, 700, "middle")

    for txt, ty in (("বোল্ট + স্প্রিং ওয়াশার", 372),
                    ("টর্ক ধরে ধরে টাইট", 410),
                    ("জোড়ার আগে ধাতু পরিষ্কার", 448)):
        s.circle(752, ty - 7, 5, GREEN)
        s.text(770, ty, txt, T_BODY, NAVY, 700, "start")

    y = note_strip(s, 546,
                   "আলগা বোল্টই বাসবারের এক নম্বর দুর্ঘটনা — "
                   "গরম হয়ে ধাতু গলে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d13_mount.svg")


# ── ১৪. বাসবার ট্রাংকিং ─────────────────────────────────────────────────
def d14_trunk():
    return sheet(
        "d14_trunk", "বাসবার ট্রাংকিং", "ছাদ থেকে ঝোলানো",
        "ph_trunk.jpg",
        "উঁচু ভবনে রাইজার কেবলের বদলে — বিএনবিসি ১.৩.১৮.৩",
        iw=780)


ALL = [d01_why, d02_concept, d03_material, d04_dims, d05_types, d06_main,
       d07_colour, d08_earth, d09_submeter, d10_3p1p, d11_sdb, d12_calc,
       d13_mount, d14_trunk]


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
