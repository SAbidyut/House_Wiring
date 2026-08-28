# -*- coding: utf-8 -*-
"""অধ্যায় ২৩ — ক্যাবল ও ক্যাবল ক্যালকুলেশন : ডায়াগ্রাম।

অধ্যায় ২২-এর মতোই দুই রকম ছবি এখানে পাশাপাশি চলে, ভাগটা ইচ্ছাকৃত:

**নেমপ্লেট-চিত্র** — ক্যাবলের গায়ে ছাপা লেখার আলোকচিত্র, কল-আউটসহ।
এই অধ্যায়ের প্রধান দাবিটাই এই — যে কেউ যেন দোকানে ক্যাবল হাতে নিয়ে
গায়ের লেখাটা পড়তে পারে।  পুরো ক্যাবলের ছবি ১৫.৪ সেমিতে বসালে ওই লেখা
৩–৪ পয়েন্টে নেমে আসে, তাই কেবল লেখার অংশটুকু আলাদা করে কাটা আছে
(`ph_print_face`)।

**আঁকা চিত্র** — গঠন, কোডের ব্যাখ্যা, ইনস্টলেশন পদ্ধতি, হিসাবের ধাপ।
আসল ক্যাবলের গায়ে বাংলাদেশের ছাপা লেখাটা যেভাবে আসে, সেটা একটাই ছবিতে
সাজিয়ে দেখানোর জন্য `d06_legend` আঁকা — কারণ ওখানে প্রতিটি ঘরের অর্থ
তীর দিয়ে দেখাতে হয়, আলোকচিত্রে সেটা হয় না।

অধ্যায় ১৫ থেকে চলে আসা ছবির নিয়ম এখানেও কড়া:  প্যানেলের শিরোনাম
বিশেষ্য, যন্ত্রাংশের লেবেল এক-দুই শব্দ, নিচে এক লাইনের একটি নোট-পটি।
কারণ, পরামর্শ আর সতর্কবাণী সবই বইয়ের লেখায় — ছবিতে নয়।

ছবির লেবেলে যা লেখা যাবে না:  কালপুরুষে `÷ √ ² Ω φ ≤` নেই বা ভুল আঁকে।
ভাগ সবসময় `/`, বর্গমিলিমিটার কথায় বা `mm2` নয় — লেখা হয় "বর্গমিমি"।
ছাপা লেখার ছবিতে `5.5mm²` দেখা যায়, ওটা ছবির নিজের লেবেল নয়, ওটা
আলোকচিত্রেরই অংশ।
"""
import os

from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch23")
IMG = os.path.join(HERE, "assets", "ch23")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
T_CALL = 24
T_TINY = 18.5

SYM = "#12324D"
SW = 3.4
PLATE = "#F4F7FA"
COPPER = "#B5713A"
COPPERL = "#D79A63"
PVC = "#2A2E33"
DEAD = "#9AA6B2"

# বিএনবিসি ১.৩.৯.৩.১৫ / সারণি ৮.১.২-এর রং
C_L = "#D42A1F"
C_N = "#1F2933"
C_PE = "#1B6E47"
C_Y = "#D9A400"
C_B = "#1B4F9C"


# ── shared helpers (অধ্যায় ২২ থেকে) ────────────────────────────────────
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


def gallery(fname, title, items, note, w, m, gap, ih, t_name, t_role,
            card_pad=12):
    """চেনার সারি — এক লাইনে ছবি, নিচে নাম আর এক-দুই শব্দের কাজ।"""
    n = len(items)
    tile = (w - 2 * m - gap * (n - 1)) / n
    top = 100
    s = SVG(w, top + ih + 240)
    s.title(title, T_TITLE)
    for i, (img, name, role) in enumerate(items):
        x = m + i * (tile + gap)
        s.rect(x, top, tile, ih + 84, PLATE, LINE, 1.8, 10)
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


# ── ছোট আঁকা উপাদান ─────────────────────────────────────────────────────
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


def strands(s, cx, cy, r, n, col=COPPER, edge="#7A4A22"):
    """খেই আঁকা — n=1 সলিড, n=7 স্ট্র্যান্ডেড, বেশি হলে সরু খেই।"""
    import math
    if n == 1:
        s.circle(cx, cy, r, col, edge, 2)
        return
    if n == 7:
        rr = r / 3.0
        s.circle(cx, cy, rr, col, edge, 1.4)
        for k in range(6):
            a = math.pi / 6 + k * math.pi / 3
            s.circle(cx + 2 * rr * math.cos(a), cy + 2 * rr * math.sin(a),
                     rr, col, edge, 1.4)
        return
    rr = r / 6.0
    s.circle(cx, cy, rr, col, edge, 0.9)
    for ring, cnt in ((2, 8), (4, 16)):
        for k in range(cnt):
            a = 2 * math.pi * k / cnt + ring * 0.2
            s.circle(cx + ring * rr * math.cos(a),
                     cy + ring * rr * math.sin(a), rr, col, edge, 0.9)


def cable_run(s, x0, x1, y, h, col=PVC, rx=10):
    """পাশ থেকে দেখা ক্যাবলের এক টুকরো।"""
    s.rect(x0, y - h / 2, x1 - x0, h, col, "#0B0D0F", 2, rx)
    s.rect(x0 + 6, y - h / 2 + 5, x1 - x0 - 12, h * 0.22, "#4A5058",
           "none", 0, 6)


# ── ১. তার, কোর, ক্যাবল ──────────────────────────────────────────────────
def d01_wire_cable():
    """তার – কোর – ক্যাবল:  তিন ধাপে একই জিনিস মোটা হয়।"""
    s = SVG(1240, 700)
    s.title("তার, কোর ও ক্যাবল — পার্থক্যটা গঠনে", T_TITLE)
    top = 96
    pw, gap = 372, 32
    x0 = (1240 - (3 * pw + 2 * gap)) / 2
    items = [
        ("খালি পরিবাহী", "conductor",
         "কেবল তামা — কোনো ইনসুলেশন নেই"),
        ("কোর", "core", "পরিবাহীর উপরে ইনসুলেশন"),
        ("ক্যাবল", "cable", "কয়েকটি কোরের উপরে শিথ"),
    ]
    # ছবির ঘর আর লেখার ঘর আলাদা করে রাখা:  ছবি বসে `top+74` থেকে
    # `top+266` পর্যন্ত, লেখা তার নিচে।  আগে সবচেয়ে বড় বৃত্তটা
    # লেখার ঘাড়ে উঠে গিয়েছিল।
    ph = 356
    cyc = top + 172
    for i, (head, kind, _sub) in enumerate(items):
        x = x0 + i * (pw + gap)
        panel(s, x, top, pw, ph, head)
        cx = x + pw / 2
        if kind == "conductor":
            strands(s, cx, cyc, 50, 7)
        elif kind == "core":
            s.circle(cx, cyc, 72, "#B32A22", "#7A1C16", 2.4)
            strands(s, cx, cyc, 50, 7)
        else:
            s.circle(cx, cyc, 94, "#2A2E33", "#0B0D0F", 2.4)
            for dx, dy, cc, ee in ((-40, -22, "#B32A22", "#7A1C16"),
                                   (40, -22, "#1F2933", "#0B0D0F"),
                                   (0, 46, "#1B6E47", "#12482E")):
                s.circle(cx + dx, cyc + dy, 38, cc, ee, 2)
                strands(s, cx + dx, cyc + dy, 24, 7)
    # ঘরের নাম, প্যানেলের নিচে নয় — প্যানেলের ভেতরে ছবির নিচে
    for i, (_h, _k, sub) in enumerate(items):
        x = x0 + i * (pw + gap)
        for j, ln in enumerate(wrap(sub, pw - 40, T_SMALL, 400)):
            s.text(x + pw / 2, top + ph - 46 + j * 26, ln, T_SMALL, GREY,
                   400, "middle")
    y = note_strip(s, top + ph + 34,
                   "বাজারে দুটোকেই 'তার' বলা হয় — বইয়ে আলাদা")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_wire_cable.svg")


# ── ২. ক্যাবলের স্তর ─────────────────────────────────────────────────────
def d02_build():
    """একটি আর্মার্ড ক্যাবলের ছয়টি স্তর, ভেতর থেকে বাইরে।"""
    s = SVG(1240, 860)
    s.title("ক্যাবলের স্তর — ভেতর থেকে বাইরে", T_TITLE)
    cx, cy = 620, 430
    layers = [
        (250, "#2A2E33", "#0B0D0F", "আউটার শিথ"),
        (226, "#7E8894", "#4E5762", "আর্মার"),
        (206, "#3A4148", "#20262C", "বেডিং"),
        (186, "#6E7681", "#464D55", "ফিলার"),
    ]
    for r, f, e, _n in layers:
        s.circle(cx, cy, r, f, e, 2.4)
    for dx, dy, cc, ee in ((-104, -60, "#B32A22", "#7A1C16"),
                           (104, -60, "#1F2933", "#0B0D0F"),
                           (0, 120, "#1B6E47", "#12482E")):
        s.circle(cx + dx, cy + dy, 92, cc, ee, 2.2)
        strands(s, cx + dx, cy + dy, 58, 7)

    # ভেতরের অংশ বাঁ পাশে, বাইরের স্তর ডান পাশে — আর প্রতিটি লেবেল
    # তার নিজের লক্ষ্যের ক্রমেই সাজানো।  আগে সবগুলো ডান পাশে ছিল আর
    # ছয়টি লিডার একে অন্যকে কেটে যাচ্ছিল।
    left = [("পরিবাহী", cx - 104, cy - 60, 300),
            ("ইনসুলেশন", cx - 175, cy - 34, 400),
            ("ফিলার", cx - 150, cy + 90, 520)]
    right = [("আউটার শিথ", cx + 62, cy - 230, 236),
             ("আর্মার", cx + 191, cy - 101, 330),
             ("বেডিং", cx + 196, cy - 10, 424)]
    for txt, tx, ty, ly in left:
        callout(s, 340, ly, txt, tx, ty, "end", T_CALL)
    for txt, tx, ty, ly in right:
        callout(s, 940, ly, txt, tx, ty, "start", T_CALL)
    y = note_strip(s, 726,
                   "বাসার ভেতরের ক্যাবলে আর্মার আর বেডিং থাকে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_build.svg")


# ── ৩. কাটা মুখের আলোকচিত্র ─────────────────────────────────────────────
def d03_xsec():
    """আসল ক্যাবলের কাটা মুখ — নিচে মিলিমিটার স্কেল।"""
    return photo_callouts(
        "d03_xsec", "কাটা মুখে ক্যাবলের স্তর", "ph_xsec.jpg",
        left=[("সবুজ-হলুদ কোর", 0.203, 0.347),
              ("আউটার শিথ", 0.084, 0.581)],
        right=[("ফিলার", 0.566, 0.191),
               ("খেই (স্ট্র্যান্ড)", 0.631, 0.415),
               ("ইনসুলেশন", 0.504, 0.707),
               ("মিলিমিটার স্কেল", 0.596, 0.958)],
        note="প্রতিটি কোরের ইনসুলেশনের রঙ আলাদা, বাইরের শিথ এক",
        iw=560, w=1240, size=T_CALL)


# ── ৪. কন্ডাক্টরের শ্রেণি ────────────────────────────────────────────────
def d04_class():
    """IEC 60228-এর শ্রেণি — সলিড, স্ট্র্যান্ডেড, ফ্লেক্সিবল।"""
    return gallery(
        "d04_class", "কন্ডাক্টরের শ্রেণি — IEC 60228",
        [("ph_solid.jpg", "ক্লাস ১ — সলিড", "এক গাছি তার"),
         ("ph_te.jpg", "ক্লাস ২ — স্ট্র্যান্ডেড", "সাতটি খেই"),
         ("ph_flex.jpg", "ক্লাস ৫ — ফ্লেক্সিবল", "বহু সরু খেই")],
        "একই বর্গমিলিমিটার, তিন রকম গঠন — কাজও তিন রকম",
        w=1240, m=26, gap=18, ih=420, t_name=26, t_role=21.5, card_pad=12)


# ── ৫. গায়ের ছাপা লেখা (আলোকচিত্র) ─────────────────────────────────────
def d05_print():
    """আসল ক্যাবলের গায়ে ছাপা লেখা — এই অধ্যায়ের কেন্দ্রীয় ছবি।"""
    return strip_callouts(
        "d05_print", "ক্যাবলের গায়ে যা ছাপা থাকে", "ph_print_face.jpg",
        above=[("অনুমোদনের চিহ্ন", 0.152, 0.152, 0.62),
               ("তৈরির সাল", 0.596, 0.596, 0.62)],
        below=[("প্রস্তুতকারক", 0.320, 0.320, 0.90),
               ("পরিবাহীর ক্ষেত্রফল", 0.808, 0.808, 0.90)],
        note="লেখাটা প্রতি মিটারে ফিরে ফিরে আসে — যেকোনো জায়গায় পড়া যায়",
        iw=1130, w=1240, size=T_CALL)


# ── ৬. পূর্ণ লেখাটির ব্যাখ্যা (আঁকা) ────────────────────────────────────
def d06_legend():
    """বাংলাদেশের বাজারের একটি ক্যাবলের গায়ে যা যা লেখা থাকে।

    আলোকচিত্রে একবারে গোটা লেখাটা পড়া যায় না — ক্যাবল গোল, লেখা
    ঘুরে যায়।  তাই এখানে গোটা লেখাটা সাজিয়ে দেখানো, প্রতিটি ঘরের
    নিচে তার অর্থ।
    """
    s = SVG(1240, 700)
    s.title("গোটা লেখাটা একসঙ্গে — ঘরে ঘরে অর্থ", T_TITLE)
    y0 = 118
    cable_h = 92
    cable_run(s, 40, 1200, y0 + cable_h / 2, cable_h)

    fields = [
        ("SUPER STAR", "প্রস্তুতকারক", 148),
        ("BDS 900", "বাংলাদেশ স্ট্যান্ডার্ড", 128),
        ("BS 6004", "ব্রিটিশ স্ট্যান্ডার্ড", 124),
        ("450/750V", "ভোল্টেজ গ্রেড", 132),
        ("1X2.5 RM", "কোর ও ক্ষেত্রফল", 140),
        ("CU/PVC", "তামা / পিভিসি", 118),
        ("FR", "ফ্লেম রিটার্ডেন্ট", 74),
        ("2026", "তৈরির সাল", 90),
    ]
    total = sum(f[2] for f in fields)
    gap = (1160 - total) / (len(fields) - 1)
    x = 40 + 20
    marks = []
    for txt, _mean, w in fields:
        s.text(x + w / 2, y0 + cable_h / 2 + 9, txt, T_SMALL, "#E7ECF1",
               700, "middle")
        marks.append((x + w / 2, w))
        x += w + gap

    # নিচে অর্থের ঘর, উপরের ঘরের সঙ্গে খাড়া রেখায় জোড়া
    ry = y0 + cable_h + 92
    rh = 62
    for (cxm, _w), (txt, mean, _w2) in zip(marks, fields):
        lines = wrap(mean, 168, T_SMALL, 700)
        bw = max(tw(ln, T_SMALL, 700) for ln in lines) + 28
        bh = rh + (len(lines) - 1) * 26
        s.path(f"M {cxm} {y0 + cable_h + 6} L {cxm} {ry - bh / 2}",
               STEEL, 2.2)
        s.rect(cxm - bw / 2, ry - bh / 2, bw, bh, LIGHT, STEEL, 2, 9)
        for j, ln in enumerate(lines):
            s.text(cxm, ry - bh / 2 + 34 + j * 26, ln, T_SMALL, NAVY, 700,
                   "middle")
    y = note_strip(s, ry + 84,
                   "ক্রম প্রস্তুতকারকভেদে বদলায়, ঘরগুলো বদলায় না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_legend.svg")


# ── ৭. হারমোনাইজড কোড ───────────────────────────────────────────────────
def d07_hcode():
    """H07V-U — অক্ষর ধরে ধরে।"""
    s = SVG(1240, 720)
    s.title("হারমোনাইজড কোড — H05VV-F ভাঙা", T_TITLE)
    parts = [
        ("H", "হারমোনাইজড", "মান অনুযায়ী", STEEL),
        ("05", "300/500 ভোল্ট", "ভোল্টেজ গ্রেড", NAVY),
        ("V", "পিভিসি", "ইনসুলেশন", GREEN),
        ("V", "পিভিসি", "শিথ", GREEN),
        ("F", "সরু খেই", "কন্ডাক্টরের গঠন", AMBER),
    ]
    top = 116
    bw, gap = 196, 24
    x0 = (1240 - (len(parts) * bw + (len(parts) - 1) * gap)) / 2
    for i, (code, meaning, role, col) in enumerate(parts):
        x = x0 + i * (bw + gap)
        head_bar(s, x, top, bw, 84, code, col, 42)
        s.rect(x, top + 84, bw, 150, "#FCFDFE", LINE, 1.8, 0)
        s.rect(x, top + 84, bw, 150, "none", LINE, 1.8, 0)
        for j, ln in enumerate(wrap(meaning, bw - 26, T_NAME, 700)):
            s.text(x + bw / 2, top + 132 + j * 30, ln, T_NAME, NAVY, 700,
                   "middle")
        for j, ln in enumerate(wrap(role, bw - 26, T_SMALL, 400)):
            s.text(x + bw / 2, top + 200 + j * 26, ln, T_SMALL, GREY, 400,
                   "middle")
    # শেষে কোরের সংখ্যা ও মাপ
    ty = top + 292
    s.rect(160, ty, 920, 96, LIGHT, STEEL, 2, 11)
    s.text(190, ty + 44, "শেষে কোরের সংখ্যা ও মাপ —", T_NAME, NAVY, 700)
    s.text(190, ty + 78, "3G1.5 মানে তিন কোর, 1.5 বর্গমিমি, একটি "
                         "সবুজ-হলুদ", T_SMALL, GREY, 400)
    s.text(1050, ty + 44, "3G1.5", T_NODE, RED, 700, "end")
    s.text(1050, ty + 78, "G-এর বদলে X = আর্থ কোর নেই", T_SMALL, GREY,
           400, "end")
    y = note_strip(s, ty + 128,
                   "বাংলাদেশে এই কোড কম, তবু আমদানি করা ক্যাবলে মেলে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_hcode.svg")


# ── ৮. বাজারের নাম (ক্যাটালগ) ───────────────────────────────────────────
def d08_market():
    """সুপার স্টারের ক্যাটালগে টাইপ-নির্দেশক ব্লক তিনটি।"""
    return pair_panels(
        "d08_market", "বাজারে ক্যাবলের নাম যেভাবে লেখা",
        [("সিঙ্গেল কোর", "cat_bya.jpg", STEEL),
         ("টুইন কোর", "cat_byfy.jpg", NAVY),
         ("ফ্লেক্সিবল", "cat_flex.jpg", GREEN)],
        "নাম, ভোল্টেজ গ্রেড আর স্ট্যান্ডার্ড নম্বর — তিনটেই এক ঘরে",
        h=252, gap=22, w=1240)


# ── ৯. কোরের রঙ ────────────────────────────────────────────────────────
def d09_colors():
    """পাঁচ কোরের ক্যাবল — আন্তর্জাতিক রঙের কোড।"""
    return photo_callouts(
        "d09_colors", "কোরের রঙ — আন্তর্জাতিক কোড", "ph_colors.jpg",
        left=[("বাদামি — L1", 0.450, 0.180),
              ("কালো — L2", 0.450, 0.330),
              ("ধূসর — L3", 0.550, 0.469),
              ("সবুজ-হলুদ — আর্থ", 0.550, 0.819)],
        right=[("ফেরুল", 0.745, 0.521),
               ("নীল — নিউট্রাল", 0.680, 0.752)],
        note="বিএনবিসি বাংলাদেশে লাল-হলুদ-নীল-কালো চালু রেখেছে",
        iw=740, w=1240, size=T_CALL)


# ── ১০. মাপের সংকেত ─────────────────────────────────────────────────────
def d10_sizecode():
    """7/0.67 rm আর 7/0.036 — একই তার, দুই নামে।"""
    s = SVG(1240, 700)
    s.title("মাপের সংকেত — একই ক্যাবল, দুই নাম", T_TITLE)
    top = 106
    pw, gap = 566, 40
    x0 = (1240 - (2 * pw + gap)) / 2
    ph = 366

    def block(x, head, big, rows, col):
        panel(s, x, top, pw, ph, head, col)
        s.text(x + pw / 2, top + 132, big, 52, col, 700, "middle")
        for j, (a, b) in enumerate(rows):
            yy = top + 190 + j * 52
            s.text(x + 40, yy, a, T_NAME, NAVY, 700)
            s.text(x + pw - 40, yy, b, T_NAME, GREY, 400, "end")
            s.path(f"M {x + 30} {yy + 16} L {x + pw - 30} {yy + 16}",
                   LINE, 1.4)

    block(x0, "মেট্রিক সংকেত", "7 / 0.67  rm",
          [("খেইয়ের সংখ্যা", "সাতটি"),
           ("প্রতিটির ব্যাস", "0.67 মিলিমিটার"),
           ("rm", "গোল, স্ট্র্যান্ডেড")], STEEL)
    block(x0 + pw + gap, "পুরনো ইঞ্চি সংকেত", "7 / 0.029\"",
          [("খেইয়ের সংখ্যা", "সাতটি"),
           ("প্রতিটির ব্যাস", "0.029 ইঞ্চি"),
           ("বাজারের ডাক", "সাত-উনত্রিশ")], AMBER)

    yy = top + ph + 34
    s.rect(120, yy, 1000, 74, GREENBG, GREEN, 2, 11)
    s.text(620, yy + 46, "দুটোরই ক্ষেত্রফল প্রায় 2.5 বর্গমিলিমিটার",
           T_NAME, GREEN, 700, "middle")
    y = note_strip(s, yy + 100,
                   "দোকানে দুই নামই চলে — ক্ষেত্রফল মিলিয়ে নিতে হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d10_sizecode.svg")


# ── ১১. ইনস্টলেশন পদ্ধতি ────────────────────────────────────────────────
def d11_install():
    """একই ক্যাবল, বসানোর জায়গা আলাদা — তাপ বেরোনোর সুযোগও আলাদা।"""
    s = SVG(1240, 700)
    s.title("বসানোর পদ্ধতি — তাপ বেরোনোর সুযোগ", T_TITLE)
    top = 100
    pw, gap = 288, 22
    x0 = (1240 - (4 * pw + 3 * gap)) / 2
    ph = 322
    items = [
        ("A1", "দেয়ালের ভেতরে কন্ডুইট", "wall_in"),
        ("B1", "দেয়ালের উপরে কন্ডুইট", "wall_on"),
        ("C", "দেয়ালে সরাসরি ক্লিপ", "clip"),
        ("E", "খোলা বাতাসে ট্রে", "tray"),
    ]
    for i, (code, name, kind) in enumerate(items):
        x = x0 + i * (pw + gap)
        panel(s, x, top, pw, ph, code)
        cx = x + pw / 2
        cy = top + 158
        if kind == "wall_in":
            s.rect(x + 24, top + 70, pw - 48, 176, "#EDE7DD", "#B9AE9C", 2, 6)
            s.circle(cx, cy, 46, "#F7F9FB", GREY, 3)
            for dx, dy in ((-18, -12), (18, -12), (0, 20)):
                s.circle(cx + dx, cy + dy, 15, "#B32A22", "#7A1C16", 1.6)
        elif kind == "wall_on":
            s.rect(x + 24, top + 70, 84, 176, "#EDE7DD", "#B9AE9C", 2, 6)
            s.circle(cx + 22, cy, 46, "#F7F9FB", GREY, 3)
            for dx, dy in ((-18, -12), (18, -12), (0, 20)):
                s.circle(cx + 22 + dx, cy + dy, 15, "#B32A22", "#7A1C16", 1.6)
        elif kind == "clip":
            s.rect(x + 24, top + 70, 84, 176, "#EDE7DD", "#B9AE9C", 2, 6)
            s.circle(cx + 22, cy, 40, "#2A2E33", "#0B0D0F", 2.4)
            for dx, dy in ((-15, -10), (15, -10), (0, 17)):
                s.circle(cx + 22 + dx, cy + dy, 13, "#B32A22", "#7A1C16", 1.6)
            s.path(f"M {x + 108} {cy} L {cx - 18} {cy}", GREY, 5)
        else:
            s.path(f"M {x + 40} {cy + 52} L {x + pw - 40} {cy + 52}",
                   GREY, 6)
            for k in range(3):
                s.path(f"M {x + 60 + k * 78} {cy + 52} "
                       f"L {x + 60 + k * 78} {cy + 22}", GREY, 4)
            s.circle(cx, cy, 40, "#2A2E33", "#0B0D0F", 2.4)
            for dx, dy in ((-15, -10), (15, -10), (0, 17)):
                s.circle(cx + dx, cy + dy, 13, "#B32A22", "#7A1C16", 1.6)
        for j, ln in enumerate(wrap(name, pw - 40, T_SMALL, 700)):
            s.text(cx, top + ph - 40 + j * 26, ln, T_SMALL, NAVY, 700,
                   "middle")

    # ধারণক্ষমতার তুলনা-পটি
    yy = top + ph + 36
    s.rect(120, yy, 1000, 84, LIGHT, STEEL, 2, 11)
    s.text(150, yy + 36, "2.5 বর্গমিমি তামার ধারণক্ষমতা", T_SMALL, GREY, 400)
    caps = [("A1", "19.5 A"), ("B1", "24 A"), ("C", "27 A"), ("E", "30 A")]
    for k, (c, v) in enumerate(caps):
        cxx = 320 + k * 210
        s.text(cxx, yy + 66, f"{c} — {v}", T_NAME, NAVY, 700, "middle")
    y = note_strip(s, yy + 110,
                   "যত ঢাকা, তত কম — ছকের ঘর মিলিয়ে সংখ্যা নিতে হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d11_install.svg")


# ── ১২. সাইজ বাছার ধাপ ─────────────────────────────────────────────────
def d12_steps():
    """ক্যাবল সাইজ বাছার ছয় ধাপ — উপর থেকে নিচে।"""
    s = SVG(1240, 900)
    s.title("ক্যাবল সাইজ বাছার ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)
    steps = [
        ("১", "লোড থেকে ডিজাইন কারেন্ট IB বের করো", STEEL),
        ("২", "IB-এর পরের স্ট্যান্ডার্ড ব্রেকার In বাছো", STEEL),
        ("৩", "ছক থেকে ক্যাবলের ধারণক্ষমতা It দেখো", STEEL),
        ("৪", "তাপমাত্রা ও গ্রুপিং দিয়ে Iz = It × Ca × Cg", AMBER),
        ("৫", "মিলিয়ে দেখো  IB ছোট, In মাঝে, Iz বড়", GREEN),
        ("৬", "ভোল্টেজ ড্রপ 2.5 শতাংশের নিচে কি না দেখো", GREEN),
    ]
    top = 108
    bh, gap = 92, 26
    bw = 880
    x = (1240 - bw) / 2
    for i, (n, txt, col) in enumerate(steps):
        yy = top + i * (bh + gap)
        s.rect(x, yy, bw, bh, "#FCFDFE", col, 2.6, 12)
        s.circle(x + 52, yy + bh / 2, 27, col)
        s.text(x + 52, yy + bh / 2 + 10, n, T_NODE, "#FFFFFF", 700, "middle")
        s.text(x + 100, yy + bh / 2 + 10, txt, T_NAME, NAVY, 700)
        if i < len(steps) - 1:
            s.path(f"M {x + bw / 2} {yy + bh + 3} "
                   f"L {x + bw / 2} {yy + bh + gap - 5}", STEEL, 3,
                   marker=ar)
    yy = top + len(steps) * (bh + gap) + 6
    y = note_strip(s, yy,
                   "৬ নম্বরে আটকালে এক ধাপ মোটা ক্যাবল নিতে হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d12_steps.svg")


# ── ১৩. ভোল্টেজ ড্রপ ────────────────────────────────────────────────────
def d13_vdrop():
    """একই কারেন্ট, দৈর্ঘ্য বাড়লে ড্রপ বাড়ে — সীমা 2.5 শতাংশ।"""
    s = SVG(1240, 760)
    s.title("দৈর্ঘ্য বাড়লে ভোল্টেজ ড্রপ বাড়ে", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 14)
    ox, oy = 190, 560          # মূলবিন্দু
    W, H = 880, 400
    s.path(f"M {ox} {oy} L {ox + W} {oy}", NAVY, 3, marker=ar)
    s.path(f"M {ox} {oy} L {ox} {oy - H}", NAVY, 3, marker=ar)
    s.text(ox + W / 2, oy + 62, "ক্যাবলের দৈর্ঘ্য (মিটার)", T_NAME, NAVY,
           700, "middle")
    s.text(ox - 118, oy - H / 2, "ভোল্টেজ ড্রপ", T_NAME, NAVY, 700)
    s.text(ox - 118, oy - H / 2 + 30, "(শতাংশ)", T_NAME, NAVY, 700)

    # x: 0..80 মিটার, y: 0..5 শতাংশ
    def px(m):
        return ox + W * m / 80.0

    def py(p):
        return oy - H * p / 5.0

    for m in range(0, 81, 20):
        s.path(f"M {px(m)} {oy} L {px(m)} {oy + 10}", NAVY, 2)
        s.text(px(m), oy + 36, str(m), T_SMALL, GREY, 400, "middle")
    for p in range(0, 6):
        s.path(f"M {ox - 10} {py(p)} L {ox} {py(p)}", NAVY, 2)
        s.text(ox - 20, py(p) + 7, str(p), T_SMALL, GREY, 400, "end")
        if p:
            s.path(f"M {ox} {py(p)} L {ox + W} {py(p)}", LINE, 1.2,
                   dash="6 6")

    # 5.45 A পাম্প, তিন মাপে — mV/A/m: 1.5→29, 2.5→18, 4→11
    lines = [("1.5 বর্গমিমি", 29, RED), ("2.5 বর্গমিমি", 18, AMBER),
             ("4 বর্গমিমি", 11, GREEN)]
    I = 5.45
    for name, mv, col in lines:
        pts = []
        for m in range(0, 81, 4):
            drop = I * mv * m / 1000.0 / 230.0 * 100
            pts.append(f"{px(m)} {py(min(drop, 5.0))}")
        s.path("M " + " L ".join(pts), col, 4)
        drop80 = I * mv * 80 / 1000.0 / 230.0 * 100
        s.text(px(80) - 14, py(min(drop80, 4.85)) - 16, name, T_SMALL, col,
               700, "end")

    # সীমারেখা
    s.path(f"M {ox} {py(2.5)} L {ox + W} {py(2.5)}", RED, 3.4, dash="12 7")
    s.box_auto(ox + 190, py(2.5) - 46,
               "বিএনবিসির সীমা — 2.5 শতাংশ", T_SMALL, fill=REDBG,
               stroke=RED, tcolor=RED, pad_x=18, pad_y=8)
    y = note_strip(s, oy + 86,
                   "5.45 A পাম্প — একই কারেন্টে মোটা ক্যাবলে ড্রপ কম")
    s.fit(y, 24)
    return s.save(f"{OUT}/d13_vdrop.svg")


# ── ১৪. ডিরেটিং ────────────────────────────────────────────────────────
def d14_derate():
    """ছকের সংখ্যাটা কাগজের, বাস্তবে দুই কারণে কমে।"""
    s = SVG(1240, 700)
    s.title("ছকের সংখ্যা থেকে বাস্তবের সংখ্যা", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)
    top = 116
    ph = 300
    pw, gap = 350, 40
    x0 = (1240 - (3 * pw + 2 * gap)) / 2

    panel(s, x0, top, pw, ph, "ছকের ধারণক্ষমতা")
    s.text(x0 + pw / 2, top + 150, "24 A", 62, STEEL, 700, "middle")
    s.text(x0 + pw / 2, top + 200, "2.5 বর্গমিমি, B1", T_SMALL, GREY, 400,
           "middle")
    s.text(x0 + pw / 2, top + 240, "30 ডিগ্রি, একা", T_SMALL, GREY, 400,
           "middle")

    x1 = x0 + pw + gap
    panel(s, x1, top, pw, ph, "দুটো গুণক", AMBER)
    for j, (lab, val) in enumerate((("তাপমাত্রা 35 ডিগ্রি", "0.94"),
                                    ("ছয় সার্কিট একসঙ্গে", "0.57"))):
        yy = top + 132 + j * 84
        s.text(x1 + 34, yy, lab, T_SMALL, NAVY, 700)
        s.text(x1 + pw - 34, yy + 6, val, T_NODE, AMBER, 700, "end")
        s.path(f"M {x1 + 26} {yy + 24} L {x1 + pw - 26} {yy + 24}",
               LINE, 1.4)

    x2 = x1 + pw + gap
    panel(s, x2, top, pw, ph, "আসল ধারণক্ষমতা", GREEN)
    s.text(x2 + pw / 2, top + 150, "12.9 A", 62, GREEN, 700, "middle")
    s.text(x2 + pw / 2, top + 208, "10 A ব্রেকার এখনো চলে", T_SMALL, GREY,
           400, "middle")
    s.text(x2 + pw / 2, top + 244, "16 A হলে চলত না", T_SMALL, RED, 700,
           "middle")

    for xa in (x0 + pw, x1 + pw):
        s.path(f"M {xa + 6} {top + ph / 2} L {xa + gap - 8} {top + ph / 2}",
               STEEL, 3.4, marker=ar)
    y = note_strip(s, top + ph + 40,
                   "এক কন্ডুইটে যত বেশি সার্কিট, প্রতিটির ক্ষমতা তত কম")
    s.fit(y, 24)
    return s.save(f"{OUT}/d14_derate.svg")


# ── ১৫. সেক্টর কন্ডাক্টর ────────────────────────────────────────────────
def d15_sector():
    """অ্যালুমিনিয়াম সার্ভিস ক্যাবল — সেক্টর আকৃতির কন্ডাক্টর।"""
    return photo_callouts(
        "d15_sector", "মাটির নিচের সার্ভিস ক্যাবল", "ph_sector.jpg",
        left=[("আউটার শিথ", 0.070, 0.249),
              ("ফিলার", 0.206, 0.738)],
        right=[("সবুজ-হলুদ কোর", 0.670, 0.203),
               ("সেক্টর কন্ডাক্টর", 0.806, 0.482)],
        note="অ্যালুমিনিয়াম, সেক্টর আকৃতি — একই ক্ষেত্রফলে ক্যাবল সরু",
        iw=620, w=1240, size=T_CALL)


# ── ১৬. টার্মিনেশন ও তার ফল ─────────────────────────────────────────────
def d16_term():
    """লাগ ঠিকমতো বসলে যা হয়, আর না বসলে যা হয়।"""
    return pair_panels(
        "d16_term", "প্রান্ত ঠিক হলে, আর না হলে",
        [("ক্যাবল লাগ", "ph_lug.jpg", GREEN),
         ("আলগা প্রান্ত", "ph_burn.jpg", RED)],
        "বিএনবিসি ১.৩.১৪.২.৪ — খেইওয়ালা প্রান্তে লাগ বাধ্যতামূলক",
        h=238, gap=26, w=1240)


# ── ১৭. তারের গেজ ───────────────────────────────────────────────────────
def d17_gauge():
    """ওয়্যার গেজ প্লেট — খাঁজে খেই ঢুকিয়ে নম্বর পড়া।

    গেজ একটা **নম্বর**, মাপ নয় — আর নম্বর বাড়লে তার সরু হয়।  উল্টো
    এই সম্পর্কটাই ছাত্রদের গুলিয়ে যায়, তাই ছবিতে খাঁজগুলো বাঁ থেকে
    ডানে ছোট হতে হতে গেছে আর নিচে প্রতিটির মিলিমিটার লেখা।
    """
    s = SVG(1240, 760)
    s.title("ওয়্যার গেজ — নম্বর বাড়লে তার সরু", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 14)

    # গেজ প্লেট — গোল চাকতি, কিনারায় খাঁজ
    cx, cy, R0 = 380, 330, 200
    s.circle(cx, cy, R0, "#C9D2DB", "#8D9AA8", 3.6)
    s.circle(cx, cy, 74, "#FCFDFE", "#8D9AA8", 3.0)
    s.text(cx, cy - 6, "SWG", 30, GREY, 700, "middle")
    s.text(cx, cy + 30, "গেজ প্লেট", T_SMALL, GREY, 400, "middle")
    import math
    slots = [(8, 4.06), (10, 3.25), (12, 2.64), (14, 2.03), (16, 1.63),
             (18, 1.22), (20, 0.91), (22, 0.71), (24, 0.56), (26, 0.46)]
    for i, (n, mm) in enumerate(slots):
        a = math.radians(-150 + i * 30)
        sx, sy = cx + R0 * math.cos(a), cy + R0 * math.sin(a)
        r = 5 + mm * 4.4                      # খাঁজের ব্যাসার্ধ মাপের অনুপাতে
        s.circle(sx, sy, r, "#FCFDFE", "#5A6470", 2.4)
        lx, ly = cx + (R0 - 44) * math.cos(a), cy + (R0 - 44) * math.sin(a)
        s.text(lx, ly + 7, str(n), T_SMALL, NAVY, 700, "middle")

    # ডান পাশে ব্যাখ্যা
    x0 = 690
    head_bar(s, x0, 150, 480, 62, "গেজ যা বলে, যা বলে না", STEEL, T_NODE)
    rows = [("গেজ নম্বর", "এক গাছি খেইয়ের ব্যাস"),
            ("নম্বর বড়", "তার সরু"),
            ("SWG 20", "0.91 মিলিমিটার"),
            ("AWG 20", "0.81 মিলিমিটার"),
            ("যা বলে না", "কতটা কারেন্ট বইবে")]
    for j, (a_, b_) in enumerate(rows):
        yy = 252 + j * 62
        s.text(x0 + 26, yy, a_, T_NAME, NAVY, 700)
        s.text(x0 + 454, yy, b_, T_NAME, GREY, 400, "end")
        s.path(f"M {x0 + 16} {yy + 18} L {x0 + 464} {yy + 18}", LINE, 1.4)
    s.path(f"M {x0 + 240} {560} L {x0 + 240} {600}", STEEL, 3, marker=ar)
    s.box_auto(x0 + 240, 606, "ক্ষেত্রফলে বদলে নিতে হয়", T_NAME,
               fill=GREENBG, stroke=GREEN, tcolor=GREEN, pad_x=22, pad_y=10)
    y = note_strip(s, 672, "একই নম্বরে SWG আর AWG এক মাপ নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d17_gauge.svg")


ALL = [d01_wire_cable, d02_build, d03_xsec, d04_class, d05_print,
       d06_legend, d07_hcode, d08_market, d09_colors, d10_sizecode,
       d11_install, d12_steps, d13_vdrop, d14_derate, d15_sector,
       d16_term, d17_gauge,
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
