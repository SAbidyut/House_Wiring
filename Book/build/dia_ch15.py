# -*- coding: utf-8 -*-
"""অধ্যায় ১৫ — সুইচ বোর্ড : ডায়াগ্রাম।

পিয়ানো বোর্ড ও সকেটসহ বোর্ডের সার্কিট ও কানেকশন ডায়াগ্রাম RAPTI-র নিজস্ব
সোর্স থেকে হুবহু বসানো — `Circuit Diagram.pptx` স্লাইড ২২ ও ২৩,
`HW Connection Diagram All.pptx` স্লাইড ২২ ও ২৩।  পিয়ানো ও গ্যাং বোর্ডের
ছবি ওই ডেকের ৩৪ ও ৩৫ নং স্লাইড থেকে কেটে নেওয়া (`assets_ch15.py`)।

বোর্ডের অংশ, সুইচের প্রতীক, বোর্ডের ভেতরের তারের পথ, মডিউলার বোর্ডের গঠন
ও বসানোর ধাপ — এগুলোর সোর্স-ছবি নেই বলে নতুন করে আঁকা।

লেবেলের নিয়ম (অধ্যায় ১৪-এর পর কড়া করা হয়েছে):  ছবির ভেতরে কেবল নাম
বসে — বাক্য নয়।  প্যানেলের শিরোনাম বিশেষ্য, যন্ত্রাংশের লেবেল এক-দুই শব্দ,
আর নিচের নোট-পটিতে এক লাইনের একটি তথ্য।  কারণ, পরামর্শ ও সতর্কবাণী সবই
বইয়ের লেখায় থাকে, ছবিতে নয়।
"""
import os
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch15")
IMG = os.path.join(HERE, "assets", "ch15")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
T_CALL = 24
LH = 1.42

SYM = "#12324D"
SW = 3.4
LIVE = "#D42A1F"
NEUT = "#1F2933"
EARTH = "#1B6E47"
SWLIVE = "#1D5B8F"
GLOW = "#F5C445"
PLATE = "#F4F7FA"
PLATE_E = "#9FAEBC"
BOXG = "#E7ECF1"
METAL = "#8D9AA8"


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


def two_panel(fname, title, left, right, note, h=600, pw=560,
              lcol=STEEL, rcol=GREEN):
    s = SVG(1240, h)
    s.title(title, T_TITLE)
    ph = h - 96 - 96
    img_panel(s, 46, 96, pw, ph, left[0], left[1], lcol)
    img_panel(s, 1194 - pw, 96, pw, ph, right[0], right[1], rcol)
    y = note_strip(s, 96 + ph + 22, note)
    s.fit(y, 22)
    return s.save(f"{OUT}/{fname}.svg")


# ── circuit symbols ─────────────────────────────────────────────────────
def node(s, x, y, col=SYM, r=6.5):
    s.circle(x, y, r, col)


def lamp_sym(s, cx, cy, r=26, on=False):
    s.circle(cx, cy, r, GLOW if on else "#FFFFFF", SYM, SW)
    k = r * 0.62
    s.path(f"M {cx-k:.1f} {cy-k:.1f} L {cx+k:.1f} {cy+k:.1f}", SYM, SW - 0.6)
    s.path(f"M {cx+k:.1f} {cy-k:.1f} L {cx-k:.1f} {cy+k:.1f}", SYM, SW - 0.6)


def fan_sym(s, cx, cy, r=28):
    import math
    s.circle(cx, cy, r, "#FFFFFF", SYM, SW)
    for a in (0, 120, 240):
        t = math.radians(a)
        x1, y1 = cx + r * 0.26 * math.cos(t), cy + r * 0.26 * math.sin(t)
        x2, y2 = (cx + r * 0.88 * math.cos(t + 0.44),
                  cy + r * 0.88 * math.sin(t + 0.44))
        s.path(f"M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}", SYM, SW - 0.4)
    s.circle(cx, cy, r * 0.20, SYM)


def socket2_sym(s, cx, cy, r=26):
    """দুই-পিন সকেটের প্রতীক — বৃত্তের ভেতরে দুই খাঁজ।"""
    s.circle(cx, cy, r, "#FFFFFF", SYM, SW)
    s.path(f"M {cx-r*0.34:.1f} {cy-r*0.12:.1f} v {-r*0.42:.1f}", SYM, SW)
    s.path(f"M {cx+r*0.34:.1f} {cy-r*0.12:.1f} v {-r*0.42:.1f}", SYM, SW)
    s.path(f"M {cx-r*0.34:.1f} {cy-r*0.12:.1f} h {r*0.68:.1f}", SYM, SW - 0.8)


def piano_switch(s, x, y, w=86, h=126, kind="switch", on=False):
    """পিয়ানো ধাঁচের একটি ইউনিট — সুইচ, ইনডিকেটর বা রেগুলেটর।"""
    s.rect(x, y, w, h, "#DDEAF5", "#8FB3D2", 2, 9)
    ix, iy, iw, ih = x + 10, y + 12, w - 20, h - 24
    if kind == "indicator":
        s.rect(ix, iy, iw, ih, "#E8443A", "#B32A22", 2, 5)
    elif kind == "regulator":
        s.rect(ix, iy, iw, ih, "#FFFFFF", "#A9B4C0", 2, 5)
        s.circle(x + w / 2, y + h / 2, min(iw, ih) * 0.30, "#F1F5F8",
                 "#7E8B99", 2.4)
    elif kind == "socket":
        s.rect(ix, iy, iw, ih, "#FFFFFF", "#A9B4C0", 2, 5)
        for dy in (-ih * 0.18, ih * 0.18):
            s.rect(x + w / 2 - 8, y + h / 2 + dy - 7, 16, 14, "#2A3440",
                   "none", 0, 3)
    else:
        s.rect(ix, iy, iw, ih, "#FFFFFF", "#A9B4C0", 2, 5)
        s.rect(x + w / 2 - 5, iy + 14 if not on else iy + ih - 40, 10, 26,
               "#B32A22" if not on else "#1B6E47", "none", 0, 3)
    return x + w / 2


# ═══════════════════════════════════════════════════════════════════════
def d01_parts():
    """সুইচ বোর্ডের তিন অংশ — ব্যাক বক্স, ইউনিট, কভার প্লেট।"""
    s = SVG(1240, 760)
    s.title("সুইচ বোর্ডের গঠন", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)

    PY, PH, PW = 118, 400, 340
    xs = [46, 450, 854]
    heads = ["ব্যাক বক্স", "সুইচ ও আনুষঙ্গিক", "কভার প্লেট"]
    cols = [STEEL, GREEN, NAVY]
    for px, head, col in zip(xs, heads, cols):
        panel(s, px, PY, PW, PH, head, col)

    # ১ — ব্যাক বক্স, দেয়ালের ভেতরে বসানো
    bx, by, bw, bh = xs[0] + 58, PY + 130, 224, 190
    s.rect(bx - 26, by - 22, bw + 52, bh + 44, "#EDE3D6", "#C6B49C", 2, 4)
    s.rect(bx, by, bw, bh, BOXG, METAL, 3, 6)
    s.rect(bx + 14, by + 14, bw - 28, bh - 28, "#F7FAFC", "#B7C2CE", 2, 4)
    for cx, cy in ((bx + 18, by + 18), (bx + bw - 18, by + 18),
                   (bx + 18, by + bh - 18), (bx + bw - 18, by + bh - 18)):
        s.circle(cx, cy, 7, "#FFFFFF", METAL, 2)
    # আর্থিং টার্মিনাল
    s.circle(bx + bw / 2, by + bh - 24, 9, "#CFE6D8", EARTH, 2.6)
    callout(s, xs[0] + 300, PY + 348, "আর্থিং টার্মিনাল",
            bx + bw / 2, by + bh - 24, "end", T_SMALL, EARTH)
    s.text(xs[0] + PW / 2, PY + 108, "দেয়ালে গাঁথা", T_SMALL, GREY, 400,
           "middle")

    # ২ — ইউনিটগুলো
    ux, uy = xs[1] + 42, PY + 148
    kinds = ["switch", "indicator", "switch", "regulator"]
    for i, k in enumerate(kinds):
        piano_switch(s, ux + i * 68, uy, 60, 150, k)
    s.text(xs[1] + PW / 2, PY + 108, "গ্যাং ধরে ধরে", T_SMALL, GREY, 400,
           "middle")
    s.text(xs[1] + PW / 2, PY + 348, "প্রতিটি ইউনিট = ১ গ্যাং", T_SMALL,
           GREEN, 700, "middle")

    # ৩ — কভার প্লেট
    px0, py0, pw0, ph0 = xs[2] + 58, PY + 130, 224, 190
    s.rect(px0, py0, pw0, ph0, PLATE, PLATE_E, 3, 8)
    for i in range(4):
        s.rect(px0 + 20 + i * 47, py0 + 30, 34, 130, "#FFFFFF", "#B7C2CE",
               2, 4)
    for cx, cy in ((px0 + 16, py0 + 16), (px0 + pw0 - 16, py0 + 16),
                   (px0 + 16, py0 + ph0 - 16),
                   (px0 + pw0 - 16, py0 + ph0 - 16)):
        s.circle(cx, cy, 6, "#FFFFFF", PLATE_E, 2)
    s.text(xs[2] + PW / 2, PY + 108, "স্ক্রু দিয়ে আটকানো", T_SMALL, GREY,
           400, "middle")

    # তিন ধাপের তির
    for x0 in (xs[0] + PW + 12, xs[1] + PW + 12):
        s.line(x0, PY + PH / 2, x0 + 48, PY + PH / 2, STEEL, 3, marker=ar)

    y = note_strip(s, PY + PH + 30,
                   "ধাতব ব্যাক বক্সে আর্থিং টার্মিনাল বাধ্যতামূলক — "
                   "বিএনবিসি ১.৩.৮.১")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_parts.svg")


def d02_switch_types():
    """বোর্ডে যে তিন ধরনের সুইচ বসে।"""
    s = SVG(1240, 620)
    s.title("বোর্ডে ব্যবহৃত সুইচের ধরন", T_TITLE)

    PW, GAP, PH = 365, 26, 384
    cases = [
        ("এক-মুখী সুইচ", RED, "SPST", "২ প্রান্ত", "বাতি, ফ্যান"),
        ("দুই-মুখী সুইচ", STEEL, "SPDT", "৩ প্রান্ত", "সিঁড়ি, করিডোর"),
        ("দুই-পোল সুইচ", GREEN, "DPST", "৪ প্রান্ত", "গিজার, এসি"),
    ]
    for i, (head, col, kind, term, use) in enumerate(cases):
        px = 46 + i * (PW + GAP)
        panel(s, px, 96, PW, PH, head, col)
        cx, cy = px + PW / 2, 250
        if i == 0:
            node(s, cx - 70, cy)
            node(s, cx + 70, cy)
            s.path(f"M {cx-70} {cy} L {cx+58} {cy-40}", SYM, SW)
        elif i == 1:
            node(s, cx - 80, cy)
            node(s, cx + 80, cy - 44)
            node(s, cx + 80, cy + 44)
            s.path(f"M {cx-80} {cy} L {cx+72} {cy-38}", SYM, SW)
        else:
            for dy in (-46, 46):
                node(s, cx - 80, cy + dy)
                node(s, cx + 80, cy + dy)
                s.path(f"M {cx-80} {cy+dy} L {cx+68} {cy+dy-34}", SYM, SW)
            s.path(f"M {cx-4} {cy-63} L {cx-4} {cy+29}", GREY, 2.4,
                   dash="7 6")
        s.text(cx, 350, kind, T_NAME, col, 700, "middle")
        s.text(cx, 392, term, T_SMALL, GREY, 400, "middle")
        s.text(cx, 440, use, T_SMALL, "#39434D", 400, "middle")

    y = note_strip(s, 96 + PH + 26,
                   "সুইচের সর্বনিম্ন রেটিং 5A — বিএনবিসি ১.৩.৮.১")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_switch_types.svg")


def d03_piano_gang():
    """পিয়ানো ও গ্যাং বোর্ড পাশাপাশি — RAPTI সোর্স।"""
    return two_panel(
        "d03_piano_gang", "পিয়ানো বোর্ড ও গ্যাং বোর্ড",
        ("পিয়ানো বোর্ড", "h34_piano_board.png"),
        ("গ্যাং বোর্ড", "h35_gang_board.png"),
        "দুটোতেই ব্যাক বক্স এক, বদলায় কেবল প্লেট ও ইউনিটের ধরন",
        h=470, pw=560)


def d04_piano_circuit():
    """পিয়ানো সুইচবোর্ডের সার্কিট ও কানেকশন — RAPTI সোর্স।"""
    return two_panel(
        "d04_piano_circuit", "পিয়ানো সুইচবোর্ড কানেকশন",
        ("সার্কিট ডায়াগ্রাম", "c22_board_schem.png"),
        ("কানেকশন ডায়াগ্রাম", "h22_board_conn.png"),
        "তিন সুইচের উপরের প্রান্ত এক ফেজে, নিচের প্রান্ত আলাদা লোডে",
        h=610)


def d05_inside():
    """বোর্ডের ভেতরে তার কোথায় কীভাবে যায়।"""
    s = SVG(1240, 880)
    s.title("বোর্ডের ভেতরের তারের পথ", T_TITLE)

    # ── লোড — বোর্ডের বাইরে, উপরে
    LY = 268                      # লোডের কেন্দ্র
    loads = [(392, "বাতি ১", "lamp"), (600, "বাতি ২", "lamp"),
             (808, "ফ্যান", "fan"), (1016, "বাতি ৩", "lamp")]
    for lx, name, kind in loads:
        if kind == "lamp":
            lamp_sym(s, lx, LY, 30, True)
        elif kind == "fan":
            fan_sym(s, lx, LY, 30)
        else:
            socket2_sym(s, lx, LY, 30)
        # নাম পাশে — প্রতীকের নিচ দিয়ে সুইচ-করা ফেজের তার ওঠে
        s.text(lx - 42, LY + 8, name, T_CALL, NAVY, 700, "end")

    # ── নিউট্রাল রেল — সব লোডের উপরে, কোনো সুইচ ছোঁয় না
    NRAIL = 156
    s.path(f"M 1128 {NRAIL} L 356 {NRAIL}", NEUT, SW)
    for lx, _n, _k in loads:
        s.path(f"M {lx} {NRAIL} L {lx} {LY - 30}", NEUT, SW)
        node(s, lx, NRAIL, NEUT)
    s.text(340, NRAIL + 8, "N", T_CALL, NEUT, 700, "end")

    # ── ব্যাক বক্স
    BX, BY, BW, BH = 90, 430, 1058, 296
    s.rect(BX, BY, BW, BH, "#FBFCFD", STEEL, 2.6, 14, dash="11 7")
    s.text(BX + BW - 40, BY + BH - 22, "ব্যাক বক্সের ভেতর", T_SMALL, STEEL,
           700, "end")

    LBUS = BY + 196               # ফেজ বাসের উচ্চতা
    NBUS = BY + 236               # নিউট্রাল বাসের উচ্চতা
    ETY = BY + BH - 18            # আর্থিং টার্মিনালের উচ্চতা
    UY, UH = BY + 62, 106         # ইউনিটের উপরের কিনারা ও উচ্চতা

    # ── ইউনিট — ইনডিকেটর + তিন সুইচ + সকেটের সুইচ
    # রেগুলেটর এখানে ইচ্ছে করেই নেই — সেটি সুইচের পরে সিরিজে বসে, তার
    # সংযোগ অধ্যায় ১২-এর বিষয়।  এই ছবির কাজ L, N ও ECC-র পথ দেখানো।
    units = [(196, "indicator", "ইনডিকেটর", None),
             (392, "switch", "সুইচ ১", 392),
             (600, "switch", "সুইচ ২", 600),
             (808, "switch", "সুইচ ৩", 808),
             (1016, "switch", "সুইচ ৪", 1016)]
    for ux, kind, name, _t in units:
        piano_switch(s, ux - 43, UY, 86, UH, kind)
        # নাম বাঁ দিকে সরানো — ইউনিটের মাথা থেকে তার সোজা উপরে ওঠে
        s.text(ux - 10, UY - 16, name, T_SMALL, NAVY, 700, "end")

    # ── ফেজ বাস — প্রতিটি ইউনিটের নিচের প্রান্তে ট্যাপ
    s.path(f"M {BX + 36} {LBUS} L 1016 {LBUS}", LIVE, SW)
    for ux, _k, _n, _t in units:
        s.path(f"M {ux} {LBUS} L {ux} {UY + UH}", LIVE, SW)
        node(s, ux, LBUS, LIVE)

    # ── নিউট্রাল বাস — ইনডিকেটর ছাড়া কোনো ইউনিট ছোঁয় না
    s.path(f"M {BX + 36} {NBUS} L 1128 {NBUS} L 1128 {NRAIL}", NEUT, SW)
    s.path(f"M 196 {NBUS} L 196 {UY + UH}", NEUT, SW)
    node(s, 196, NBUS, NEUT)

    # ── সুইচ করা ফেজ — প্রতিটি ইউনিটের উপর থেকে নিজের লোডে
    for ux, _k, _n, tgt in units:
        if tgt is None:
            continue
        s.path(f"M {ux} {UY} L {ux} {LY + 30}", SWLIVE, SW)

    # ── আর্থ — ব্যাক বক্সের টার্মিনালে গিয়েই শেষ
    s.circle(BX + 36, ETY, 10, "#CFE6D8", EARTH, 2.8)

    # ── ভেতরে আসা তিন তার
    for yy, col, lab in ((LBUS, LIVE, "L"), (NBUS, NEUT, "N"),
                         (ETY, EARTH, "E")):
        s.path(f"M 62 {yy} L {BX + 36} {yy}", col, SW)
        s.text(52, yy + 8, lab, T_CALL, col, 700, "end")

    # ── রঙের চাবি
    KY = BY + BH + 34
    keys = [(LIVE, "ফেজ"), (SWLIVE, "সুইচ করা ফেজ"), (NEUT, "নিউট্রাল"),
            (EARTH, "আর্থ")]
    kx = 150
    for col, lab in keys:
        s.path(f"M {kx} {KY} L {kx + 48} {KY}", col, SW)
        s.text(kx + 60, KY + 8, lab, T_SMALL, "#39434D", 400)
        kx += 60 + tw(lab, T_SMALL, 400) + 54

    y = note_strip(s, KY + 34,
                   "নিউট্রাল সরাসরি লোডে যায়; ফেজই কেবল সুইচের ভেতর দিয়ে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_inside.svg")


def d06_socket_board():
    """সকেটসহ পূর্ণ বোর্ড — RAPTI সোর্স।"""
    return two_panel(
        "d06_socket_board", "সকেটসহ সুইচবোর্ড কানেকশন",
        ("সার্কিট ডায়াগ্রাম", "c23_socket_schem.png"),
        ("কানেকশন ডায়াগ্রাম", "h23_socket_conn.png"),
        "সকেটের ফেজও নিজের সুইচ হয়ে যায়, নিউট্রাল যায় সরাসরি",
        h=660)


def d07_gang_module():
    """মডিউলার বা গ্যাং বোর্ডের গঠন ও মডিউলের হিসাব।"""
    s = SVG(1240, 780)
    s.title("মডিউলার বোর্ডের গঠন", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)

    PY, PH, PW = 118, 320, 340
    xs = [46, 450, 854]
    for px, head, col in zip(xs, ["ব্যাক বক্স", "গ্রিড প্লেট ও মডিউল",
                                  "কভার প্লেট"], [STEEL, GREEN, NAVY]):
        panel(s, px, PY, PW, PH, head, col)

    # ব্যাক বক্স
    bx, by, bw, bh = xs[0] + 70, PY + 116, 200, 148
    s.rect(bx, by, bw, bh, BOXG, METAL, 3, 6)
    s.rect(bx + 14, by + 14, bw - 28, bh - 28, "#F7FAFC", "#B7C2CE", 2, 4)

    # গ্রিড প্লেট ও মডিউল
    gx, gy, gw, gh = xs[1] + 46, PY + 116, 248, 148
    s.rect(gx, gy, gw, gh, "#FFFFFF", METAL, 3, 5)
    s.rect(gx + 16, gy + 18, gw - 32, gh - 36, "#F1F5F8", "#B7C2CE", 2,
           4, dash="7 5")
    mx = gx + 24
    for mw in (34, 34, 68, 34):
        s.rect(mx, gy + 26, mw, gh - 52, "#FFFFFF", "#7E8B99", 2.2, 4)
        mx += mw + 10
    s.text(xs[1] + PW / 2, PY + 292, "মডিউল খাপে বসে", T_SMALL, GREEN, 700,
           "middle")

    # কভার প্লেট
    cx0, cy0, cw0, ch0 = xs[2] + 62, PY + 116, 216, 148
    s.rect(cx0, cy0, cw0, ch0, PLATE, PLATE_E, 3, 10)
    s.rect(cx0 + 18, cy0 + 20, cw0 - 36, ch0 - 40, "#FFFFFF", "#C3CEDA", 2, 6)

    for x0 in (xs[0] + PW + 12, xs[1] + PW + 12):
        s.line(x0, PY + PH / 2, x0 + 48, PY + PH / 2, STEEL, 3, marker=ar)

    # ── মডিউলের মাপের সারি
    MY = PY + PH + 34
    s.rect(46, MY, 1148, 158, "#F7FAFC", LINE, 1.8, 12)
    s.text(70, MY + 40, "কোন ইউনিট কয় মডিউল", T_BODY, NAVY, 700)
    items = [("সুইচ", 1, "১M"), ("সকেট", 2, "২M"), ("রেগুলেটর", 2, "২M"),
             ("১৩A সকেট", 3, "৩M")]
    ux = 96
    for name, m, lab in items:
        wdt = 26 * m + 8 * (m - 1)
        for k in range(m):
            s.rect(ux + k * 34, MY + 66, 26, 56, "#FFFFFF", STEEL, 2.2, 3)
        s.text(ux + wdt / 2, MY + 146, f"{name} — {lab}", T_SMALL, "#39434D",
               400, "middle")
        ux += max(wdt, tw(f"{name} — {lab}", T_SMALL, 400)) + 104

    y = note_strip(s, MY + 182,
                   "প্লেটের নাম মডিউলের সংখ্যায় — ২M, ৩M, ৪M, ৬M, ৮M")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_gang_module.svg")


def d08_install_steps():
    """বোর্ড বসানোর ছয় ধাপ।"""
    s = SVG(1240, 620)
    s.title("সুইচ বোর্ড বসানোর ধাপ", T_TITLE)

    steps = [
        ("দাগ কাটা", "মেঝে থেকে ১২২০ mm"),
        ("খাঁজ ও ব্যাক বক্স", "ওয়াটারপাস ধরে সমান"),
        ("তার টানা", "L, N ও ECC জোড়াবিহীন"),
        ("ইউনিট বসানো", "ফেজ সুইচের প্রান্তে"),
        ("প্লেট আটকানো", "চার স্ক্রু সমান চাপে"),
        ("পরীক্ষা", "পোলারিটি ও কন্টিনিউইটি"),
    ]
    CW, GAP, CH = 356, 30, 172
    for i, (head, sub) in enumerate(steps):
        col, row = i % 3, i // 3
        x = 46 + col * (CW + GAP)
        y = 106 + row * (CH + 26)
        s.rect(x, y, CW, CH, "#FCFDFE", LINE, 1.8, 12)
        s.badge(x + 44, y + CH / 2, ["১", "২", "৩", "৪", "৫", "৬"][i], 26,
                NAVY, "#FFFFFF", 24)
        s.text(x + 88, y + 68, head, T_NAME, NAVY, 700)
        for j, ln in enumerate(wrap(sub, CW - 118, T_SMALL, 400)):
            s.text(x + 88, y + 104 + j * T_SMALL * 1.34, ln, T_SMALL,
                   "#39434D", 400)

    y = note_strip(s, 106 + 2 * CH + 26 + 26,
                   "সাপ্লাই দেওয়ার আগেই শেষ ধাপের পরীক্ষা — ব্যতিক্রম নেই",
                   fill=AMBERBG, stroke=AMBER, tcolor="#7A5200")
    s.fit(y, 24)
    return s.save(f"{OUT}/d08_install_steps.svg")


ALL = [d01_parts, d02_switch_types, d03_piano_gang, d04_piano_circuit,
       d05_inside, d06_socket_board, d07_gang_module, d08_install_steps]

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
