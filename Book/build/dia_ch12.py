# -*- coding: utf-8 -*-
"""অধ্যায় ১২ — ফ্যান ও ফ্যান রেগুলেটর : ডায়াগ্রাম।

রেগুলেটরের সার্কিট ও কানেকশন ডায়াগ্রাম RAPTI-র নিজস্ব সোর্স থেকে হুবহু
বসানো — `Circuit Diagram.pptx` স্লাইড ২১ ও ২২, `HW Connection Diagram
All.pptx` স্লাইড ২১।  ফ্যান, ক্যাপাসিটর ও রেগুলেটরের আলোকচিত্র উইকিমিডিয়া
কমন্স থেকে (CC/CC0)।  মোটরের ভেতরের গঠন, ক্যাপাসিটর সংযোগ ও ঘূর্ণনের দিক —
এগুলোর কোনো সোর্স-ছবি নেই বলে নতুন করে আঁকা।
"""
import os, math
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch12")
IMG = os.path.join(HERE, "assets", "ch12")

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
COPPER = "#C07A32"
METAL = "#8D9AA8"
METAL_L = "#C9D2DB"


# ── shared helpers ──────────────────────────────────────────────────────
def panel(s, x, y, w, h, title, col=STEEL):
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def note_strip(s, y, text, x=46, w=1148, fill="#EAF2FA", stroke=STEEL,
               tcolor=NAVY, size=T_NAME):
    s.rect(x, y, w, 58, fill, stroke, 2, 11)
    s.text(x + w / 2, y + 36, text, size, tcolor, 700, "middle")
    return y + 58


def callout(s, x, y, text, tx, ty, anchor="end", size=T_CALL, col=NAVY):
    """লেবেল ও লিডার — লাইন লেখার যে পাশে লক্ষ্য, সেই কিনারা থেকেই বেরোয়।"""
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    w = tw(text, size, 700)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle"
                                      else x - w)
    x1 = x0 + w
    start = x1 + 10 if tx > x1 else x0 - 10
    s.path(f"M {start} {y} L {tx} {ty}", STEEL, 2.2)
    s.circle(tx, ty, 5, STEEL)


def img_panel(s, x, y, w, h, title, img, col=STEEL, cap=None):
    panel(s, x, y, w, h, title, col)
    top = y + 64
    bot = y + h - (40 if cap else 14)
    s.image_fit(x + 16, top, w - 32, bot - top, img, 6)
    if cap:
        s.text(x + w / 2, y + h - 16, cap, T_SMALL, GREY, 400, "middle")


def two_panel(fname, title, left, right, note, h=600, pw=560,
              lcol=STEEL, rcol=GREEN):
    s = SVG(1240, h)
    s.title(title, T_TITLE)
    ph = h - 96 - 96
    img_panel(s, 46, 96, pw, ph, left[0], f"{IMG}/{left[1]}", lcol)
    img_panel(s, 1194 - pw, 96, pw, ph, right[0], f"{IMG}/{right[1]}", rcol)
    y = note_strip(s, 96 + ph + 22, note)
    s.fit(y, 22)
    return s.save(f"{OUT}/{fname}.svg")


# ── circuit symbols ─────────────────────────────────────────────────────
def ac_source(s, cx, cy, r=38):
    s.circle(cx, cy, r, "#FFFFFF", SYM, SW)
    k = r * 0.55
    s.path(f"M {cx-2*k:.1f} {cy:.1f} q {k/2:.1f} {-k*1.1:.1f} {k:.1f} 0 "
           f"q {k/2:.1f} {k*1.1:.1f} {k:.1f} 0", SYM, SW)


def cap_sym(s, cx, cy, w=46, h=54, col=SYM, vertical=True):
    """ক্যাপাসিটরের প্রতীক — দুই সমান্তরাল পাত।"""
    if vertical:
        s.line(cx - w / 2, cy - 7, cx + w / 2, cy - 7, col, SW + 1)
        s.line(cx - w / 2, cy + 7, cx + w / 2, cy + 7, col, SW + 1)
    else:
        s.line(cx - 7, cy - h / 2, cx - 7, cy + h / 2, col, SW + 1)
        s.line(cx + 7, cy - h / 2, cx + 7, cy + h / 2, col, SW + 1)


def coil_sym(s, x0, x1, cy, col=SYM, n=4, up=True):
    """কয়েলের প্রতীক — পরপর কয়েকটি অর্ধবৃত্ত।"""
    step = (x1 - x0) / n
    d = f"M {x0:.1f} {cy:.1f}"
    for i in range(n):
        x = x0 + i * step
        d += (f" q {step/2:.1f} {-step*0.9 if up else step*0.9:.1f} "
              f"{step:.1f} 0")
    s.path(d, col, SW, "none")


def fan_sym(s, cx, cy, r=34, col=SYM):
    s.circle(cx, cy, r, "#FFFFFF", col, SW)
    for i in range(3):
        a = math.radians(90 + i * 120)
        s.path(f"M {cx} {cy} L {cx + r*0.92*math.cos(a):.1f} "
               f"{cy + r*0.92*math.sin(a):.1f}", col, SW)


def reg_sym(s, cx, cy, w=104, h=44, col=SYM):
    """রেগুলেটর — পরিবর্তনশীল রোধের প্রতীক।"""
    s.rect(cx - w / 2, cy - h / 2, w, h, "#FFFFFF", col, SW, 4)
    ar = s.arrow_defs(col, "regar", 12)
    s.path(f"M {cx-w/2-14} {cy+h/2+18} L {cx+w/2-10} {cy-h/2-16}", col, 2.8,
           marker=ar)


# ═══════════════════════════════════════════════════════════════════════
def d01_parts():
    """সিলিং ফ্যানের বাইরের ও ভেতরের অংশ।"""
    s = SVG(1240, 700)
    s.title("সিলিং ফ্যানের অংশ পরিচিতি", T_TITLE)

    PW, PH = 560, 470
    panel(s, 46, 96, PW, PH, "নিচ থেকে দেখা", STEEL)
    IW = 400
    IH = IW * 1234 / 1700
    IX, IY = 46 + (PW - IW) / 2, 168
    s.image(IX, IY, IW, IH, f"{IMG}/ph_fan.jpg", 8)
    LY = IY + IH + 44
    # লক্ষ্যবিন্দুগুলো ছবির উপর গ্রিড ফেলে মাপা
    callout(s, 96, LY, "ব্লেড", IX + 0.22 * IW, IY + 0.72 * IH, "start")
    callout(s, 552, LY, "মোটর হাউজিং", IX + 0.55 * IW, IY + 0.52 * IH, "end")
    callout(s, 46 + PW / 2, LY + 44, "ব্লেড ব্র্যাকেট",
            IX + 0.42 * IW, IY + 0.62 * IH, "middle")

    # ── ডান পাশে কাটা-চিত্র (হাতে আঁকা) ─────────────────────────────
    panel(s, 634, 96, PW, PH, "পাশ থেকে কাটা-চিত্র", GREEN)
    CX = 634 + PW / 2 - 40
    CEIL = 176
    s.rect(CX - 190, CEIL - 26, 380, 26, "#D9DFE6", "#A9B4C0", 2, 3)
    s.text(CX - 168, CEIL - 6, "ছাদ", T_SMALL, "#54606C", 700, "middle")
    s.circle(CX, CEIL + 14, 13, "none", METAL, 5)          # হুক
    s.rect(CX - 34, CEIL + 26, 68, 26, METAL_L, METAL, 2, 5)   # ক্যানোপি
    s.rect(CX - 11, CEIL + 52, 22, 84, METAL_L, METAL, 2, 3)   # ডাউন রড
    s.rect(CX - 74, CEIL + 136, 148, 96, "#E7ECF1", "#7C8794", 2.6, 12)
    s.circle(CX, CEIL + 184, 26, "#FFFFFF", "#7C8794", 2.4)
    for dx in (-1, 1):
        s.poly([(CX + dx * 74, CEIL + 156), (CX + dx * 226, CEIL + 172),
                (CX + dx * 226, CEIL + 194), (CX + dx * 74, CEIL + 200)],
               "#5B7C99", "#3C566B", 2.4)
    callout(s, 742, CEIL + 14, "হুক", CX - 13, CEIL + 14, "end")
    callout(s, 742, CEIL + 58, "ক্যানোপি", CX - 34, CEIL + 38, "end")
    callout(s, 742, CEIL + 104, "ডাউন রড", CX - 11, CEIL + 96, "end")
    callout(s, 1146, CEIL + 122, "মোটর ও কয়েল", CX + 74, CEIL + 168, "end")
    callout(s, 1146, CEIL + 232, "ব্লেড", CX + 168, CEIL + 186, "end")

    y = note_strip(s, 96 + PH + 22,
                   "ফ্যানের ওজন ধরে রাখে ছাদের হুক — ডাউন রড ও ক্যানোপি "
                   "কেবল সেটিকে ঢেকে রাখে, ভার বহন করে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_parts.svg")


def d02_motor():
    """ফ্যানের মোটরের ভেতরে দুই কয়েল কীভাবে বসে।"""
    s = SVG(1240, 720)
    s.title("ফ্যানের মোটরে রানিং ও স্টার্টিং কয়েল", T_TITLE)

    CX, CY, R = 430, 350, 190
    s.circle(CX, CY, R, "#F3F6F9", "#8D9AA8", 3)
    s.circle(CX, CY, R - 52, "#FFFFFF", "#8D9AA8", 2.4)
    s.circle(CX, CY, 66, "#E7ECF1", "#7C8794", 3)          # রোটর
    for i in range(12):
        a = math.radians(i * 30)
        s.line(CX + 48 * math.cos(a), CY + 48 * math.sin(a),
               CX + 62 * math.cos(a), CY + 62 * math.sin(a), "#9AA6B2", 3)
    s.text(CX, CY + 8, "রোটর", T_SMALL, "#37424E", 700, "middle")

    # চার মেরু — দুই জোড়া কয়েল
    for a_deg, col in ((0, RED), (180, RED), (90, STEEL), (270, STEEL)):
        a = math.radians(a_deg)
        ux, uy = math.cos(a), math.sin(a)          # কেন্দ্র থেকে বাইরের দিক
        tx, ty = -uy, ux                           # লম্ব দিক
        # খুঁটির মুখ
        s.poly([(CX + (R - 62) * ux + 30 * tx, CY + (R - 62) * uy + 30 * ty),
                (CX + (R - 62) * ux - 30 * tx, CY + (R - 62) * uy - 30 * ty),
                (CX + (R - 40) * ux - 18 * tx, CY + (R - 40) * uy - 18 * ty),
                (CX + (R - 40) * ux + 18 * tx, CY + (R - 40) * uy + 18 * ty)],
               "#E7ECF1", "#8D9AA8", 2.2)
        # খুঁটির গায়ে জড়ানো কয়েল
        for i in range(4):
            rr = R - 36 + i * 11
            s.path(f"M {CX + rr*ux + 24*tx:.1f} {CY + rr*uy + 24*ty:.1f} "
                   f"A 24 24 0 0 1 {CX + rr*ux - 24*tx:.1f} "
                   f"{CY + rr*uy - 24*ty:.1f}", col, 4)

    s.text(CX + R + 24, CY + 6, "রানিং কয়েল", T_CALL, RED, 700)
    s.text(CX - R - 24, CY - 10, "রানিং কয়েল", T_CALL, RED, 700, "end")
    s.text(CX - R - 24, CY + 18, "(মোটা তার, রোধ কম)", T_SMALL, GREY, 400,
           "end")
    s.text(CX, CY - R - 26, "স্টার্টিং কয়েল", T_CALL, STEEL, 700, "middle")
    s.text(CX, CY + R + 46, "স্টার্টিং কয়েল (সরু তার, রোধ বেশি)", T_SMALL,
           GREY, 400, "middle")

    # ঘূর্ণনের তীর
    ar = s.arrow_defs(GREEN, "rot", 14)
    s.path(f"M {CX+108} {CY-108} A 152 152 0 0 1 {CX+108} {CY+108}", GREEN,
           3.4, marker=ar)

    # ব্যাখ্যার কার্ড
    x0, PW = 760, 434
    items = [
        ("দুটি কয়েল কেন", "একটি কয়েলে চুম্বকক্ষেত্র শুধু আগে-পিছে দোলে, "
         "ঘোরে না — তাই মোটর নিজে থেকে চালু হয় না।"),
        ("৯০° কোণে বসানো", "স্টার্টিং কয়েলকে রানিং কয়েলের সঙ্গে ৯০ ডিগ্রি "
         "কোণে বসানো হয়।"),
        ("ক্যাপাসিটরের কাজ", "ক্যাপাসিটর স্টার্টিং কয়েলের কারেন্টকে এগিয়ে "
         "দেয়; দুই কয়েলের কারেন্টে সময়ের ব্যবধান তৈরি হয়।"),
        ("ফল", "দুই মিলে ঘূর্ণায়মান চুম্বকক্ষেত্র তৈরি হয় এবং রোটর ঘুরতে "
         "শুরু করে।"),
    ]
    yy = 118
    for head, body in items:
        lines = wrap(body, PW - 44, T_SMALL, 400)
        h = 44 + len(lines) * T_SMALL * 1.34
        s.rect(x0, yy, PW, h, "#F7FAFC", LINE, 1.8, 11)
        s.text(x0 + 22, yy + 32, head, T_BODY, NAVY, 700)
        for j, ln in enumerate(lines):
            s.text(x0 + 22, yy + 62 + j * T_SMALL * 1.34, ln, T_SMALL,
                   "#39434D", 400)
        yy += h + 16

    y = note_strip(s, max(yy + 8, 594),
                   "সিলিং ফ্যানে ক্যাপাসিটর সবসময় লাইনে থাকে — চালু হওয়ার "
                   "পরেও বিচ্ছিন্ন হয় না, একে বলে PSC মোটর")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_motor.svg")


def d03_cap_types():
    """রান ও স্টার্ট ক্যাপাসিটরের পার্থক্য।"""
    return two_panel(
        "d03_cap_types", "ফ্যান ও মোটরে ব্যবহৃত ক্যাপাসিটর",
        ("রান ক্যাপাসিটর — ফ্যানে এটিই থাকে", "ph_cap_run.png"),
        ("স্টার্ট ক্যাপাসিটর — বড় মোটরে", "ph_cap_start.jpg"),
        "রান ক্যাপাসিটর ছোট মানের, সারাক্ষণ চলে; স্টার্ট ক্যাপাসিটর বড় মানের, "
        "কয়েক সেকেন্ডের জন্য বসে", h=600)


def d04_cap_read():
    """ক্যাপাসিটরের গায়ের লেখা পড়া।"""
    s = SVG(1240, 940)
    s.title("ক্যাপাসিটরের গায়ের লেখা পড়া", T_TITLE)
    IX, IY, IW = 300, 200, 640
    IH = IW * 648 / 702
    s.rect(IX - 14, IY - 14, IW + 28, IH + 28, "#FCFDFE", LINE, 1.8, 12)
    s.image(IX, IY, IW, IH, f"{IMG}/ph_cap_run.png", 6)

    def at(fx, fy):
        return IX + fx * IW, IY + fy * IH

    callout(s, 274, 380, "মান (µF)", *at(0.303, 0.352), "end")
    callout(s, 274, 600, "ফ্রিকোয়েন্সি ৫০/৬০ Hz", *at(0.214, 0.604), "end")
    callout(s, 966, 330, "সহনসীমা ±৫%", *at(0.381, 0.416), "start")
    callout(s, 966, 452, "কর্মক্ষম ভোল্টেজ", *at(0.639, 0.343), "start")
    callout(s, 966, 620, "সর্বোচ্চ তাপমাত্রা ৭০°C", *at(0.559, 0.604), "start")

    y = note_strip(s, IY + IH + 52,
                   "বদলানোর সময় µF মান হুবহু মেলাতে হবে; ভোল্টেজ রেটিং সমান "
                   "বা বেশি চলবে, কম কখনোই নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_cap_read.svg")


def d05_reg_conn():
    """রেগুলেটরের সার্কিট ও কানেকশন ডায়াগ্রাম (RAPTI সোর্স)।"""
    s = SVG(1240, 620)
    s.title("ফ্যান ও রেগুলেটরের সংযোগ", T_TITLE)
    PW = 560
    img_panel(s, 46, 96, PW, 390, "সার্কিট ডায়াগ্রাম",
              f"{IMG}/c21_reg_schem.png", STEEL)
    img_panel(s, 634, 96, PW, 390, "কানেকশন ডায়াগ্রাম",
              f"{IMG}/h21_reg_conn.png", GREEN)
    y = note_strip(s, 508,
                   "ফেজ তার আগে সুইচে, সুইচ থেকে রেগুলেটরে, তারপর ফ্যানে; "
                   "নিউট্রাল সরাসরি ফ্যানে যায়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_reg_conn.svg")


def d06_reg_types():
    """রেগুলেটরের তিন ধরন।"""
    s = SVG(1240, 800)
    s.title("রেগুলেটরের প্রকারভেদ", T_TITLE)
    PW, GAP = 365, 26
    PH = 300

    # ১ — রেজিস্টিভ
    panel(s, 46, 96, PW, PH, "রেজিস্টিভ (কয়েল টাইপ)", RED)
    cx, cy = 46 + PW / 2, 96 + 170
    coil_sym(s, cx - 96, cx + 96, cy, RED, 5)
    s.text(cx, cy + 62, "সিরিজে বসানো রোধ", T_SMALL, "#39434D", 400, "middle")
    s.text(cx, cy + 92, "বাড়তি শক্তি তাপ হয়ে যায়", T_SMALL, RED, 700,
           "middle")

    # ২ — ক্যাপাসিটর টাইপ
    px2 = 46 + PW + GAP
    panel(s, px2, 96, PW, PH, "ক্যাপাসিটর (স্টেপ) টাইপ", STEEL)
    cx2 = px2 + PW / 2
    for i, dx in enumerate((-92, -14, 64)):
        cap_sym(s, cx2 + dx + 14, cy, 44, 50, SYM)
        s.text(cx2 + dx + 14, cy + 50, ["১", "২", "৩"][i], T_SMALL, GREY, 700,
               "middle")
    s.text(cx2, cy + 92, "ধাপে ধাপে ক্যাপাসিটর বদলায়", T_SMALL, "#39434D",
           400, "middle")

    # ৩ — ইলেকট্রনিক
    px3 = 46 + 2 * (PW + GAP)
    img_panel(s, px3, 96, PW, PH, "ইলেকট্রনিক (TRIAC)",
              f"{IMG}/ph_reg_elec.jpg", GREEN)

    # তুলনা
    rows = [
        ("বিদ্যুৎ খরচ", "কম গতিতেও খরচ প্রায় একই", "কম গতিতে খরচ কমে",
         "কম গতিতে খরচ কমে"),
        ("তাপ", "রেগুলেটর গরম হয়", "গরম হয় না বললেই চলে", "সামান্য গরম হয়"),
        ("দাম ও আকার", "বড় ও ভারী", "মাঝারি", "ছোট, বোর্ডে বসে যায়"),
        ("শব্দ", "শব্দ নেই", "শব্দ নেই", "কম গতিতে গুনগুন শব্দ হতে পারে"),
    ]
    ty = 96 + PH + 26
    s.rect(46, ty, 1148, 44, NAVY, NAVY, 2, 10)
    heads = ["বিষয়", "রেজিস্টিভ", "ক্যাপাসিটর", "ইলেকট্রনিক"]
    xs = [46, 316, 610, 904]
    ws = [270, 294, 294, 290]
    for h_, x_, w_ in zip(heads, xs, ws):
        s.text(x_ + w_ / 2, ty + 30, h_, T_SMALL, "#FFFFFF", 700, "middle")
    yy = ty + 44
    for r in rows:
        hh = 0
        cells = []
        for txt, w_ in zip(r, ws):
            ls = wrap(txt, w_ - 28, T_SMALL, 400)
            cells.append(ls)
            hh = max(hh, 22 + len(ls) * T_SMALL * 1.3)
        s.rect(46, yy, 1148, hh, "#F7FAFC", LINE, 1.4, 0)
        for k, (ls, x_, w_) in enumerate(zip(cells, xs, ws)):
            for j, ln in enumerate(ls):
                s.text(x_ + 14, yy + 28 + j * T_SMALL * 1.3, ln, T_SMALL,
                       NAVY if k == 0 else "#39434D", 700 if k == 0 else 400)
        yy += hh

    y = note_strip(s, yy + 22,
                   "পুরোনো কয়েল-টাইপ রেগুলেটরে গতি কমালেও বিদ্যুৎ বিল কমে না — "
                   "বাঁচানো শক্তিটুকু রেগুলেটরেই তাপ হয়ে যায়",
                   fill=AMBERBG, stroke=AMBER, tcolor="#7A5200")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_reg_types.svg")


def d07_cap_conn():
    """ফ্যানের ক্যাপাসিটর ও কয়েলের সংযোগ।"""
    s = SVG(1240, 700)
    s.title("ফ্যানের কয়েল ও ক্যাপাসিটরের সংযোগ", T_TITLE)

    L_Y, N_Y = 176, 560
    X0, X1 = 120, 1060
    s.path(f"M {X0} {L_Y} L {X1} {L_Y}", LIVE, SW)
    s.path(f"M {X0} {N_Y} L {X1} {N_Y}", NEUT, SW)
    s.text(X0 - 12, L_Y + 8, "ফেজ", T_CALL, LIVE, 700, "end")
    s.text(X0 - 12, N_Y + 8, "নিউট্রাল", T_CALL, NEUT, 700, "end")

    # সুইচ ও রেগুলেটর ফেজ লাইনে
    s.path(f"M 240 {L_Y} L 268 {L_Y-22}", SYM, SW)
    s.circle(240, L_Y, 5, SYM)
    s.circle(288, L_Y, 5, SYM)
    s.text(264, L_Y - 40, "সুইচ", T_SMALL, NAVY, 700, "middle")
    reg_sym(s, 420, L_Y)
    s.text(420, L_Y - 48, "রেগুলেটর", T_SMALL, NAVY, 700, "middle")

    # ফ্যানের ভেতর
    BX, BY, BW, BH = 560, 236, 520, 300
    s.rect(BX, BY, BW, BH, "#FCFDFE", STEEL, 2.4, 14, dash="10 7")
    s.text(BX + 16, BY + 30, "ফ্যানের ভেতরে", T_SMALL, STEEL, 700)

    A_X, B_X = 660, 980            # দুই প্রান্তের নোড
    RUN_Y, ST_Y = BY + 96, BY + 208
    s.path(f"M {A_X} {L_Y} L {A_X} {ST_Y}", LIVE, SW)
    s.path(f"M {B_X} {N_Y} L {B_X} {ST_Y}", NEUT, SW)
    s.circle(A_X, L_Y, 6, LIVE)
    s.circle(B_X, N_Y, 6, NEUT)

    # রানিং কয়েল
    s.path(f"M {A_X} {RUN_Y} L {A_X+70} {RUN_Y}", SYM, SW)
    coil_sym(s, A_X + 70, A_X + 230, RUN_Y, SYM, 4)
    s.path(f"M {A_X+230} {RUN_Y} L {B_X} {RUN_Y}", SYM, SW)
    s.text(A_X + 150, RUN_Y - 46, "রানিং কয়েল", T_CALL, NAVY, 700, "middle")

    # স্টার্টিং কয়েল + ক্যাপাসিটর
    s.path(f"M {A_X} {ST_Y} L {A_X+52} {ST_Y}", SYM, SW)
    cap_sym(s, A_X + 78, ST_Y, 46, 54, SYM, vertical=False)
    s.path(f"M {A_X+104} {ST_Y} L {A_X+140} {ST_Y}", SYM, SW)
    coil_sym(s, A_X + 140, A_X + 280, ST_Y, STEEL, 4, up=False)
    s.path(f"M {A_X+280} {ST_Y} L {B_X} {ST_Y}", SYM, SW)
    s.text(A_X + 78, ST_Y + 52, "ক্যাপাসিটর", T_SMALL, NAVY, 700, "middle")
    s.text(A_X + 220, ST_Y + 52, "স্টার্টিং কয়েল", T_SMALL, STEEL, 700,
           "middle")

    # দুই কয়েলের সংযোগ বিন্দু
    s.path(f"M {A_X} {RUN_Y} L {A_X} {ST_Y}", SYM, SW)
    s.circle(A_X, RUN_Y, 6, SYM)
    s.path(f"M {B_X} {RUN_Y} L {B_X} {ST_Y}", SYM, SW)
    s.circle(B_X, RUN_Y, 6, SYM)

    y = note_strip(s, 600,
                   "দুই কয়েলই ফেজ ও নিউট্রালের মাঝে প্যারালালে বসে; "
                   "ক্যাপাসিটর কেবল স্টার্টিং কয়েলের সঙ্গে সিরিজে থাকে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_cap_conn.svg")


def d08_direction():
    """ঘূর্ণনের দিক উল্টানো।"""
    s = SVG(1240, 660)
    s.title("ফ্যানের ঘূর্ণনের দিক বদলানো", T_TITLE)
    PW, PH = 560, 420

    for k, (px, head, col, swap) in enumerate(
            ((46, "স্বাভাবিক সংযোগ", STEEL, False),
             (634, "স্টার্টিং কয়েলের দুই প্রান্ত উল্টানো", GREEN, True))):
        panel(s, px, 96, PW, PH, head, col)
        A_X, B_X = px + 96, px + 464
        RUN_Y, ST_Y = 220, 340
        s.text(A_X - 46, RUN_Y + 8, "ফেজ", T_SMALL, LIVE, 700, "middle")
        s.text(B_X + 46, RUN_Y + 8, "নিউট্রাল", T_SMALL, NEUT, 700, "middle")
        s.path(f"M {A_X-14} {RUN_Y} L {A_X} {RUN_Y}", LIVE, SW)
        s.path(f"M {B_X} {RUN_Y} L {B_X+14} {RUN_Y}", NEUT, SW)

        coil_sym(s, A_X + 60, A_X + 200, RUN_Y, SYM, 4)
        s.path(f"M {A_X} {RUN_Y} L {A_X+60} {RUN_Y}", SYM, SW)
        s.path(f"M {A_X+200} {RUN_Y} L {B_X} {RUN_Y}", SYM, SW)
        s.text(A_X + 130, RUN_Y - 42, "রানিং কয়েল", T_SMALL, NAVY, 700,
               "middle")

        s.path(f"M {A_X} {RUN_Y} L {A_X} {ST_Y}", SYM, SW)
        s.path(f"M {B_X} {RUN_Y} L {B_X} {ST_Y}", SYM, SW)
        s.circle(A_X, RUN_Y, 6, SYM)
        s.circle(B_X, RUN_Y, 6, SYM)
        cap_sym(s, A_X + 40, ST_Y, 44, 50, SYM, vertical=False)
        s.path(f"M {A_X} {ST_Y} L {A_X+18} {ST_Y}", SYM, SW)
        coil_sym(s, A_X + 108, A_X + 238, ST_Y, STEEL, 4, up=False)
        if not swap:
            s.path(f"M {A_X+62} {ST_Y} L {A_X+108} {ST_Y}", SYM, SW)
            s.path(f"M {A_X+238} {ST_Y} L {B_X} {ST_Y}", SYM, SW)
        else:                       # দুই প্রান্ত অদলবদল — তার ঘুরিয়ে আনা
            s.path(f"M {A_X+62} {ST_Y} L {A_X+80} {ST_Y} L {A_X+80} {ST_Y+44} "
                   f"L {A_X+238} {ST_Y+44} L {A_X+238} {ST_Y}", RED, SW)
            s.path(f"M {A_X+108} {ST_Y} L {A_X+108} {ST_Y-40} "
                   f"L {B_X} {ST_Y-40} L {B_X} {ST_Y}", RED, SW)

        # কয়েলের দুই প্রান্তের চিহ্ন — উল্টালে জায়গা বদলায়
        left_tag, right_tag = ("U", "V") if not swap else ("V", "U")
        ty_ = ST_Y + 76 if swap else ST_Y + 40
        s.text(A_X + 100, ty_, left_tag, T_SMALL, RED, 700, "middle")
        s.text(A_X + 246, ty_, right_tag, T_SMALL, RED, 700, "middle")
        s.text(px + PW / 2, 96 + PH - 26,
               "ঘোরে ঘড়ির কাঁটার দিকে" if not swap else "ঘোরে উল্টো দিকে",
               T_NAME, col, 700, "middle")

    y = note_strip(s, 96 + PH + 26,
                   "ক্যাপাসিটরের তার নয় — স্টার্টিং কয়েলের দুই প্রান্ত "
                   "অদলবদল করলেই ঘূর্ণনের দিক উল্টে যায়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d08_direction.svg")


def d09_board():
    """সুইচ বোর্ডে ফ্যানসহ সম্পূর্ণ সংযোগ।"""
    return two_panel(
        "d09_board", "সুইচ বোর্ডে ফ্যান ও রেগুলেটর",
        ("সার্কিট ডায়াগ্রাম (RAPTI সোর্স)", "c22_board_schem.png"),
        ("বাস্তব বোর্ড — দুটি রেগুলেটরসহ", "ph_board_reg.jpg"),
        "প্রতিটি ফ্যানের জন্য একটি সুইচ ও একটি রেগুলেটর — রেগুলেটর সবসময় "
        "সুইচের পরে ফেজ তারে বসে", h=620)


def d10_cap_family():
    """ক্যাপাসিটরের শ্রেণিবিভাগ — বাস্তব ছবিতে।"""
    s = SVG(1240, 640)
    s.title("ক্যাপাসিটরের প্রকারভেদ", T_TITLE)
    PW, GAP, PH = 365, 26, 400
    cases = [
        ("পোলারাইজড — ইলেক্ট্রোলাইটিক", "ph_cap_polar.jpg", RED,
         "গায়ে সাদা দাগ ও − চিহ্ন থাকে; DC বর্তনীতে চলে"),
        ("নন-পোলারাইজড — সিরামিক", "ph_cap_ceramic.jpg", GREEN,
         "কোনো ধনাত্মক-ঋণাত্মক নেই; দুই দিকেই বসে"),
        ("ভেরিয়েবল — এয়ার", "ph_cap_var.jpg", STEEL,
         "ঘুরিয়ে মান বদলানো যায়; রেডিও-টিউনিংয়ে"),
    ]
    for i, (head, img, col, cap) in enumerate(cases):
        px = 46 + i * (PW + GAP)
        img_panel(s, px, 96, PW, PH, head, f"{IMG}/{img}", col)
        for j, ln in enumerate(wrap(cap, PW - 40, T_SMALL, 400)):
            s.text(px + PW / 2, 96 + PH + 30 + j * T_SMALL * 1.34, ln,
                   T_SMALL, "#39434D", 400, "middle")
    y = note_strip(s, 96 + PH + 92,
                   "ফ্যানের ক্যাপাসিটর সবসময় নন-পোলারাইজড ও AC রেটিংয়ের — "
                   "ইলেক্ট্রোলাইটিক ক্যাপাসিটর ফ্যানে বসালে তা ফেটে যাবে",
                   fill=REDBG, stroke=RED, tcolor="#7A1810")
    s.fit(y, 24)
    return s.save(f"{OUT}/d10_cap_family.svg")


def d11_cap_symbols():
    """পোলারাইজড ও নন-পোলারাইজড ক্যাপাসিটর চেনা ও তাদের প্রতীক।"""
    s = SVG(1240, 620)
    s.title("পোলারাইজড ও নন-পোলারাইজড — চেনার উপায়", T_TITLE)
    PW, PH = 560, 400

    # ── বাঁ প্যানেল : পোলারাইজড
    panel(s, 46, 96, PW, PH, "পোলারাইজড (ইলেক্ট্রোলাইটিক)", RED)
    bx, by = 110, 215
    s.rect(bx, by, 96, 150, "#2B4E7E", "#17325A", 2.6, 10)     # কৌটা
    s.rect(bx + 62, by + 8, 24, 134, "#DCE6F2", "#9AB0CC", 2, 6)  # সাদা দাগ
    for k in range(3):
        s.text(bx + 74, by + 44 + k * 34, "−", 26, "#17325A", 700, "middle")
    s.path(f"M {bx+24} {by} L {bx+24} {by-42}", "#8D9AA8", 4)   # লম্বা পা
    s.path(f"M {bx+72} {by+150} L {bx+72} {by+184}", "#8D9AA8", 4)
    s.text(bx + 24, by - 54, "+", 30, RED, 700, "middle")
    callout(s, 250, by - 30, "লম্বা পা = ধনাত্মক", bx + 24, by - 24, "start")
    callout(s, 250, by + 75, "সাদা দাগ ও − চিহ্ন", bx + 86, by + 75, "start")
    callout(s, 250, by + 177, "খাটো পা = ঋণাত্মক", bx + 72, by + 170, "start")

    # প্রতীক
    sx, sy = 120, 452
    s.path(f"M {sx} {sy} L {sx+40} {sy}", SYM, SW)
    s.line(sx + 40, sy - 26, sx + 40, sy + 26, SYM, SW + 1)
    s.path(f"M {sx+62} {sy-26} q -18 26 0 52", SYM, SW + 1)
    s.path(f"M {sx+62} {sy} L {sx+104} {sy}", SYM, SW)
    s.text(sx + 30, sy - 38, "+", 24, RED, 700, "middle")
    s.text(sx + 130, sy + 8, "পোলারাইজড ক্যাপাসিটরের প্রতীক", T_SMALL,
           "#39434D", 400)

    # ── ডান প্যানেল : নন-পোলারাইজড
    panel(s, 634, 96, PW, PH, "নন-পোলারাইজড (ফ্যানের ক্যাপাসিটর)", GREEN)
    cx2, cy2 = 800, 200
    s.rect(cx2, cy2, 150, 130, "#1F2933", "#0E1419", 2.6, 10)
    s.text(cx2 + 75, cy2 + 58, "3.15 µF", T_NAME, "#FFFFFF", 700, "middle")
    s.text(cx2 + 75, cy2 + 94, "450 V AC", T_SMALL, "#C9D2DB", 400, "middle")
    s.path(f"M {cx2+40} {cy2} L {cx2+40} {cy2-46}", "#8D9AA8", 4)
    s.path(f"M {cx2+110} {cy2} L {cx2+110} {cy2-46}", "#8D9AA8", 4)
    callout(s, 1150, cy2 + 40, "দুই তার একই রকম", cx2 + 150, cy2 + 40, "end")
    callout(s, 1150, cy2 + 128, "গায়ে + বা − নেই", cx2 + 150, cy2 + 110, "end")

    sx2, sy2 = 740, 452
    s.path(f"M {sx2} {sy2} L {sx2+40} {sy2}", SYM, SW)
    s.line(sx2 + 40, sy2 - 26, sx2 + 40, sy2 + 26, SYM, SW + 1)
    s.line(sx2 + 62, sy2 - 26, sx2 + 62, sy2 + 26, SYM, SW + 1)
    s.path(f"M {sx2+62} {sy2} L {sx2+104} {sy2}", SYM, SW)
    s.text(sx2 + 150, sy2 + 8, "নন-পোলারাইজড ক্যাপাসিটরের প্রতীক", T_SMALL,
           "#39434D", 400)

    y = note_strip(s, 96 + PH + 26,
                   "AC লাইনে ভোল্টেজের দিক প্রতি অর্ধচক্রে উল্টে যায় — তাই "
                   "সেখানে পোলারিটিহীন ক্যাপাসিটর ছাড়া চলে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d11_cap_symbols.svg")


ALL = [d01_parts, d02_motor, d03_cap_types, d04_cap_read, d05_reg_conn,
       d06_reg_types, d07_cap_conn, d08_direction, d09_board,
       d10_cap_family, d11_cap_symbols]

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
