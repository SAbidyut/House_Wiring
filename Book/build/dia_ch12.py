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
T_NAME = 26
T_BODY = 23.5
T_SMALL = 22.5          # ১৫.৪ সেমি চওড়ায় ≈ ৭.৯ pt — ৭.৫ pt-এর মেঝের উপরে
T_CALL = 25.5
T_TINY = 20.5
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


def callout(s, x, y, text, tx, ty, anchor="end", size=T_CALL, col=NAVY,
            elbow=False, lead=STEEL):
    """লেবেল ও লিডার — লাইন লেখার যে পাশে লক্ষ্য, সেই কিনারা থেকেই বেরোয়।

    `elbow=True` দিলে লিডার আগে লেবেলের উচ্চতায় আড়াআড়ি যায়, তারপর খাড়া
    নেমে লক্ষ্যে ঠেকে — ছাপা লেখা বা আঁকা অংশের উপর দিয়ে তির্যক রেখা
    টানা এড়াতে (অধ্যায় ২২-এর শিক্ষা)।
    """
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    w = tw(text, size, 700)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle"
                                      else x - w)
    x1 = x0 + w
    start = x1 + 10 if tx > x1 else x0 - 10
    d = (f"M {start} {y} L {tx} {y} L {tx} {ty}" if elbow
         else f"M {start} {y} L {tx} {ty}")
    s.path(d, lead, 2.2)
    s.circle(tx, ty, 5, lead)


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
def _hatch(s, x, y, w, h, col="#8D9AA8", step=11, sw=1.4):
    """কাটা-তলের হ্যাচিং — সেকশন বোঝাতে।"""
    s.clip_begin(x, y, w, h, 2)
    n = int((w + h) / step) + 2
    for i in range(n):
        x0 = x - h + i * step
        s.path(f"M {x0:.1f} {y + h:.1f} L {x0 + h:.1f} {y:.1f}", col, sw)
    s.clip_end()


def _motor_section(s, cx, top, bot, hw, cut_right=True):
    """বাইরের-রোটর মোটরের কাটা-চিত্র — ডান দেয়াল ভাঙা রেখে ভেতর দেখানো।"""
    shell, shed = "#C2CCD6", "#6E7A87"
    s.rect(cx - hw, top, 2 * hw, 17, shell, shed, 2.2, 3)
    s.rect(cx - hw, bot - 17, 2 * hw, 17, shell, shed, 2.2, 3)
    s.rect(cx - hw, top, 17, bot - top, shell, shed, 2.2, 3)
    if cut_right:
        s.rect(cx + hw - 17, top, 17, 28, shell, shed, 2.2, 3)
        s.rect(cx + hw - 17, bot - 28, 17, 28, shell, shed, 2.2, 3)
        d = f"M {cx+hw-17} {top+28}"
        step = (bot - top - 56) / 8
        for i in range(8):
            d += f" l {8 if i % 2 == 0 else -8} {step:.1f}"
        s.path(d, shed, 2)
    else:
        s.rect(cx + hw - 17, top, 17, bot - top, shell, shed, 2.2, 3)
    # খাঁচার বার — কাটা না-হওয়া বাঁ দেয়ালের ভেতরের গায়ে
    s.rect(cx - hw + 17, top + 22, 11, bot - top - 44, COPPER, "#8E5620",
           1.6, 2)
    # স্থির শ্যাফট
    s.rect(cx - 11, top - 4, 22, bot - top + 30, "#9AA6B2", "#63707D", 2.2, 3)
    # স্টেটর কোর ও কয়েল
    sx, swd = cx - 78, 156
    s.rect(sx, top + 34, swd, bot - top - 68, "#E3E9EF", "#8D9AA8", 2.2, 4)
    for xb in (sx + 7, sx + swd - 29):
        s.rect(xb, top + 50, 22, bot - top - 100, COPPER, "#8E5620", 1.8, 4)
    # বেয়ারিং — স্থির শ্যাফট ও ঘূর্ণায়মান পাতের মাঝে
    for yb in (top + 8, bot - 8):
        s.rect(cx - 29, yb - 9, 58, 18, "#F2F5F8", "#63707D", 2, 3)
        for dx in (-16, 16):
            s.circle(cx + dx, yb, 5, "#7C8794")
    return sx, swd


def _blades(s, cx, bot, hw, reach):
    for sgn in (-1, 1):
        s.poly([(cx + sgn * (hw + 2), bot - 22),
                (cx + sgn * reach, bot - 6),
                (cx + sgn * reach, bot + 14),
                (cx + sgn * (hw + 2), bot + 2)],
               "#5B7C99", "#3C566B", 2.2)


def d01_parts():
    """সিলিং ফ্যানের বাইরের অংশ (আলোকচিত্র) ও ভেতরের কাটা-চিত্র।"""
    s = SVG(1240, 1060)
    s.title("সিলিং ফ্যানের অংশ পরিচিতি", T_TITLE)

    # ── ১ম সারি : বাস্তব ফ্যানের ছবি, দুই পাশে লেবেল ────────────────
    PW, PH = 1148, 392
    panel(s, 46, 96, PW, PH, "বাস্তব ফ্যান: বাইরে যা দেখা যায়", STEEL)
    IW = 400
    IH = round(IW * 1456 / 1800)
    IX, IY = 46 + (PW - IW) / 2, 154
    s.image(IX, IY, IW, IH, f"{IMG}/ph_fan.jpg", 8)

    def at(fx, fy):
        return IX + fx * IW, IY + fy * IH

    # লক্ষ্যবিন্দুগুলো ছবির পিক্সেল মেপে বসানো (অধ্যায় ২৩-এর নিয়ম) —
    # চোখে আন্দাজ করলে ব্লেডের লিডার পটভূমিতেই গিয়ে পড়ে।
    callout(s, IX - 42, IY + 0.17 * IH, "ব্লেড", *at(0.136, 0.169), "end")
    callout(s, IX - 42, IY + 0.44 * IH, "ব্লেড ব্র্যাকেট",
            *at(0.381, 0.412), "end")
    callout(s, IX - 42, IY + 0.72 * IH, "মোটর হাউজিং",
            *at(0.487, 0.482), "end")
    callout(s, IX + IW + 42, IY + 0.17 * IH, "সিলিং রোজ ও সরবরাহ তার",
            *at(0.549, 0.190), "start")
    callout(s, IX + IW + 42, IY + 0.50 * IH, "মোটরের উপরের ঢাকনা",
            *at(0.478, 0.349), "start")

    # ── ২য় সারি : কাটা-চিত্র ────────────────────────────────────────
    TY = 96 + PH + 20
    PH2 = 404
    panel(s, 46, TY, PW, PH2, "পাশ থেকে কাটা-চিত্র", GREEN)
    CX = 620
    CEIL = TY + 84

    # ছাদ ও হুক
    s.rect(CX - 320, CEIL - 30, 640, 30, "#D9DFE6", "#A9B4C0", 2, 3)
    _hatch(s, CX - 320, CEIL - 30, 640, 30, "#B4BFCB", 16, 1.2)
    s.path(f"M {CX} {CEIL} L {CX} {CEIL+8}", METAL, 6)
    s.circle(CX, CEIL + 20, 12, "none", METAL, 5.5)            # হুক
    s.path(f"M {CX} {CEIL+32} L {CX} {CEIL+40}", METAL, 6)

    # ক্যানোপি — ভেতরে ক্যাপাসিটর
    s.poly([(CX - 76, CEIL + 96), (CX + 76, CEIL + 96),
            (CX + 44, CEIL + 40), (CX - 44, CEIL + 40)],
           "#EDF1F5", "#8D9AA8", 2.4)
    s.rect(CX + 16, CEIL + 56, 44, 32, "#20456F", "#12324D", 2, 3)
    s.line(CX + 24, CEIL + 88, CX + 8, CEIL + 118, "#8E5620", 2.4)
    s.line(CX + 50, CEIL + 88, CX + 16, CEIL + 118, "#8E5620", 2.4)
    s.rect(CX - 13, CEIL + 96, 26, 34, METAL_L, METAL, 2.2, 3)  # ডাউন রড

    TOP, BOT, HW = CEIL + 130, CEIL + 262, 150
    sx, swd = _motor_section(s, CX, TOP, BOT, HW)
    _blades(s, CX, BOT, HW, 300)
    for sgn in (-1, 1):                                   # ব্লেড ব্র্যাকেট
        s.rect(CX + sgn * HW - (36 if sgn > 0 else 0), BOT - 24, 36, 17,
               "#9FB0C0", "#5D6E7E", 2, 2)

    L, R = 306, 934
    callout(s, L, CEIL + 20, "ছাদের হুক", CX - 12, CEIL + 20, "end")
    callout(s, L, CEIL + 66, "ক্যানোপি", CX - 60, CEIL + 66, "end")
    callout(s, L, CEIL + 112, "ডাউন রড", CX - 13, CEIL + 112, "end")
    callout(s, L, TOP + 56, "মোটর হাউজিং", CX - HW + 8, TOP + 56, "end")
    callout(s, L, BOT + 26, "ব্লেড", CX - 250, BOT + 4, "end")
    callout(s, R, CEIL + 62, "ক্যাপাসিটর", CX + 60, CEIL + 62, "start")
    callout(s, R, TOP + 8, "বেয়ারিং", CX + 29, TOP + 8, "start")
    callout(s, R, TOP + 60, "স্টেটর ও কয়েল", sx + swd, TOP + 60, "start")
    callout(s, R, BOT + 26, "ব্লেড ব্র্যাকেট", CX + HW + 4, BOT - 6, "start")

    y = note_strip(s, TY + PH2 + 20,
                   "ফ্যানের ওজন ধরে রাখে ছাদের হুক; ডাউন রড ও ক্যানোপি "
                   "শুধু সেটিকে ঢেকে রাখে, ভার বহন করে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_parts.svg")


def d02_motor():
    """বাইরের রোটর — ফ্যানের মোটরের গঠন ও দুই কয়েল।"""
    s = SVG(1240, 690)
    s.title("ফ্যানের মোটর: স্টেটর ভেতরে, রোটর বাইরে", T_TITLE)

    PW, PH = 1148, 484
    panel(s, 46, 96, PW, PH, "মোটরের কাটা-চিত্র", STEEL)

    # ═════ বাঁ দিক — পাশ থেকে কাটা ════════════════════════════════
    CX, TOP, BOT, HW = 336, 268, 424, 126
    s.box_auto(CX, 146, "পাশ থেকে", T_TINY, fill=LIGHT, stroke=STEEL,
               tcolor=NAVY, pad_x=14, pad_y=5)
    s.rect(CX - 13, 206, 26, 62, METAL_L, METAL, 2.2, 3)        # ডাউন রড
    sx, swd = _motor_section(s, CX, TOP, BOT, HW)
    _blades(s, CX, BOT, HW, 196)

    callout(s, 194, 232, "ডাউন রড", CX - 13, 232, "end")
    callout(s, 194, TOP + 40, "রোটর খোল", CX - HW + 8, TOP + 40, "end")
    callout(s, 194, TOP + 96, "খাঁচার বার", CX - HW + 23, TOP + 96, "end")
    callout(s, 580, TOP + 6, "বেয়ারিং", CX + 29, TOP + 6, "start")
    callout(s, 580, TOP + 42, "স্টেটর", sx + swd, TOP + 42, "start")
    callout(s, 580, BOT - 56, "কয়েল", sx + swd - 18, BOT - 56, "start")
    s.text(CX, BOT + 60, "স্থির শ্যাফট", T_SMALL, NAVY, 700, "middle")
    s.path(f"M {CX} {BOT+42} L {CX} {BOT+26}", STEEL, 2.2)
    s.text(CX - 168, BOT + 60, "ব্লেড", T_SMALL, NAVY, 700, "middle")
    s.path(f"M {CX-168} {BOT+42} L {CX-168} {BOT+22}", STEEL, 2.2)

    # ═════ ডান দিক — নিচ থেকে কাটা (সেকশন) ════════════════════════
    OX, OY, RO = 920, 352, 112
    s.box_auto(OX, 140, "নিচ থেকে", T_TINY, fill=LIGHT, stroke=STEEL,
               tcolor=NAVY, pad_x=14, pad_y=5)

    for i in range(3):                                   # ব্লেড ব্র্যাকেট
        a = math.radians(90 + i * 120)
        ux, uy = math.cos(a), math.sin(a)
        tx, ty = -uy, ux
        s.poly([(OX + RO * ux + 22 * tx, OY + RO * uy + 22 * ty),
                (OX + RO * ux - 22 * tx, OY + RO * uy - 22 * ty),
                (OX + (RO + 26) * ux - 16 * tx, OY + (RO + 26) * uy - 16 * ty),
                (OX + (RO + 26) * ux + 16 * tx, OY + (RO + 26) * uy + 16 * ty)],
               "#9FB0C0", "#5D6E7E", 2)

    s.circle(OX, OY, RO, "#C2CCD6", "#6E7A87", 2.6)             # রোটর খোল
    s.circle(OX, OY, RO - 26, "#FFFFFF", "#6E7A87", 2.2)
    for i in range(24):                                        # খাঁচার বার
        a = math.radians(i * 15)
        s.circle(OX + (RO - 14) * math.cos(a), OY + (RO - 14) * math.sin(a),
                 5.2, COPPER, "#8E5620", 1.2)

    RS = RO - 38
    s.circle(OX, OY, 42, "#E3E9EF", "#8D9AA8", 2.4)            # স্টেটর কোর
    for a_deg, col in ((90, RED), (270, RED), (0, STEEL), (180, STEEL)):
        a = math.radians(a_deg)
        ux, uy = math.cos(a), math.sin(a)
        tx, ty = -uy, ux
        s.poly([(OX + 36 * ux + 24 * tx, OY + 36 * uy + 24 * ty),
                (OX + 36 * ux - 24 * tx, OY + 36 * uy - 24 * ty),
                (OX + RS * ux - 28 * tx, OY + RS * uy - 28 * ty),
                (OX + RS * ux + 28 * tx, OY + RS * uy + 28 * ty)],
               "#E3E9EF", "#8D9AA8", 2.2)
        for i in range(4):
            rr = 44 + i * 9
            s.path(f"M {OX + rr*ux + 25*tx:.1f} {OY + rr*uy + 25*ty:.1f} "
                   f"A 25 25 0 0 {1 if a_deg in (90, 180) else 0} "
                   f"{OX + rr*ux - 25*tx:.1f} {OY + rr*uy - 25*ty:.1f}",
                   col, 4)
    s.circle(OX, OY, 15, "#9AA6B2", "#63707D", 2.2)            # শ্যাফট

    ar = s.arrow_defs(GREEN, "rot12", 14)
    s.path(f"M {OX - 44} {OY - RO - 24} A {RO+24} {RO+24} 0 0 1 "
           f"{OX + 44} {OY - RO - 24}", GREEN, 3.6, marker=ar)

    s.text(OX, OY - RO - 44, "রোটর ঘোরে", T_SMALL, GREEN, 700, "middle")
    callout(s, 1050, OY - 62, "এয়ার গ্যাপ",
            OX + 89 * math.cos(math.radians(-42)),
            OY + 89 * math.sin(math.radians(-42)), "start")
    callout(s, 1050, OY + 64, "স্টেটর", OX + 28, OY + 28, "start")

    # রং-সংকেত
    ly = OY + RO + 52
    for dx, col, txt in ((-118, RED, "রানিং কয়েল"),
                         (36, STEEL, "স্টার্টিং কয়েল")):
        s.rect(OX + dx, ly - 15, 22, 22, col, col, 1, 4)
        s.text(OX + dx + 32, ly + 3, txt, T_SMALL, NAVY, 700)

    y = note_strip(s, 96 + PH + 22,
                   "স্টেটর ভেতরে স্থির থাকে, রোটর তার বাইরে দিয়ে ঘোরে; "
                   "ব্লেড এই ঘূর্ণায়মান খোলের গায়েই বসানো")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_motor.svg")


def d03_cap_types():
    """ফ্যানের দুই চেহারার রান ক্যাপাসিটর ও বড় মোটরের স্টার্ট ক্যাপাসিটর।"""
    s = SVG(1240, 700)
    s.title("ফ্যান ও মোটরে ব্যবহৃত ক্যাপাসিটর", T_TITLE)
    PW, GAP, PH = 365, 26, 452
    cases = [
        ("রান: গোল কৌটা", "ph_cap_can.jpg", STEEL),
        ("রান: বাক্স (CBB61)", "ph_cap_fan.jpg", STEEL),
        ("স্টার্ট ক্যাপাসিটর", "ph_cap_start.jpg", GREEN),
    ]
    for i, (head, img, col) in enumerate(cases):
        px = 46 + i * (PW + GAP)
        img_panel(s, px, 96, PW, PH, head, f"{IMG}/{img}", col)
    y = note_strip(s, 96 + PH + 22,
                   "গোল কৌটা আর বাক্স দুটিই ফ্যানের রান ক্যাপাসিটর, কাজ "
                   "এক; স্টার্ট ক্যাপাসিটর বড় মানের, ফ্যানে বসে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_cap_types.svg")


def d04_cap_read():
    """ফ্যানের ক্যাপাসিটরের গায়ের লেখা পড়া — বাজারের চলতি গোল কৌটা।"""
    s = SVG(1240, 800)
    s.title("ফ্যানের ক্যাপাসিটরের গায়ের লেখা", T_TITLE)
    IW = 400
    IH = round(IW * 924 / 761)
    IX, IY = (1240 - IW) / 2, 148
    s.rect(IX - 12, IY - 12, IW + 24, IH + 24, "#FCFDFE", LINE, 1.8, 12)
    s.image(IX, IY, IW, IH, f"{IMG}/ph_cap_can_face.jpg", 6)

    def at(fx, fy):
        return IX + fx * IW, IY + fy * IH

    # লিডারের ডগা ছাপা লেখার *পাশে* — নেমপ্লেটে ছাপা লেখাটাই এখানে পাঠ।
    LX, RX = IX - 34, IX + IW + 34
    callout(s, LX, IY + 0.18 * IH, "দুই স্পেড টার্মিনাল", *at(0.31, 0.16),
            "end")
    callout(s, LX, IY + 0.52 * IH, "মান: 2.5 µF", *at(0.30, 0.675), "end")
    callout(s, LX, IY + 0.84 * IH, "PCB-মুক্ত তেল", *at(0.19, 0.820), "end")
    callout(s, RX, IY + 0.36 * IH, "ব্র্যান্ড ও ধরন", *at(0.84, 0.575),
            "start")
    callout(s, RX, IY + 0.64 * IH, "কর্মক্ষম ভোল্টেজ: 350 V AC",
            *at(0.77, 0.745), "start")
    callout(s, RX, IY + 0.92 * IH, "তৈরির দেশ", *at(0.76, 0.880), "start")

    y = note_strip(s, IY + IH + 40,
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
    PH = 262

    # ১ — রেজিস্টিভ
    panel(s, 46, 96, PW, PH, "রেজিস্টিভ (কয়েল টাইপ)", RED)
    cx, cy = 46 + PW / 2, 96 + 156
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
        ("শব্দ", "শব্দ নেই", "শব্দ নেই", "কম গতিতে গুনগুন হতে পারে"),
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
                   "পুরোনো কয়েল-টাইপ রেগুলেটরে গতি কমালেও বিদ্যুৎ বিল কমে না; "
                   "বাঁচানো শক্তিটুকু রেগুলেটরেই তাপ হয়ে যায়",
                   fill=AMBERBG, stroke=AMBER, tcolor="#7A5200")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_reg_types.svg")


def vcoil(s, cy0, cy1, x, col=SYM, n=4, left=True):
    """খাড়া কয়েলের প্রতীক — পরপর কয়েকটি অর্ধবৃত্ত।"""
    step = (cy1 - cy0) / n
    d = f"M {x:.1f} {cy0:.1f}"
    for i in range(n):
        d += (f" q {-step*0.9 if left else step*0.9:.1f} {step/2:.1f} "
              f"0 {step:.1f}")
    s.path(d, col, SW, "none")


def _node(s, x, y, col=SYM, r=7):
    s.circle(x, y, r, col)


def _term(s, x, y, tag, dx=0, dy=0, anchor="start", col=NAVY):
    """ফ্যানের বাইরে বেরোনো প্রান্তের নাম।"""
    s.circle(x, y, 8, "#FFFFFF", col, 3)
    s.text(x + dx, y + dy, tag, T_SMALL, col, 700, anchor)


def d07_cap_conn():
    """ফ্যানের তিন প্রান্ত, দুই কয়েল ও ক্যাপাসিটরের সংযোগ।"""
    s = SVG(1240, 800)
    s.title("ফ্যানের কয়েল ও ক্যাপাসিটরের সংযোগ", T_TITLE)

    LY, NY = 168, 630                       # ফেজ ও নিউট্রাল বাস
    X0 = 150
    XC, XL, XR = 690, 520, 860              # কমন, রানিং প্রান্ত, স্টার্টিং প্রান্ত
    TOPB, BOTB = 215, 478                   # ফ্যানের ঘেরের উপরে-নিচে
    CY, KY0, KY1 = 258, 300, 432            # কমন নোড ও কয়েলের দুই মাথা
    QY = 528                                # ক্যাপাসিটরের সারি

    # ── ফ্যানের ঘের ──────────────────────────────────────────────
    s.rect(440, TOPB, 500, BOTB - TOPB, "#F8FAFC", STEEL, 2.4, 14, dash="10 7")
    s.text(456, TOPB + 32, "ফ্যানের ভেতরে", T_SMALL, STEEL, 700)

    # ── ফেজ : বাস → সুইচ → রেগুলেটর → কমন প্রান্ত ────────────────
    s.path(f"M {X0} {LY} L 300 {LY}", LIVE, SW)
    s.path(f"M 300 {LY} L 336 {LY-26}", SYM, SW)          # সুইচ
    _node(s, 300, LY, SYM, 6)
    _node(s, 360, LY, SYM, 6)
    s.text(330, LY - 44, "সুইচ", T_SMALL, NAVY, 700, "middle")
    s.path(f"M 360 {LY} L 450 {LY}", LIVE, SW)
    reg_sym(s, 510, LY)
    s.text(510, LY - 46, "রেগুলেটর", T_SMALL, NAVY, 700, "middle")
    s.path(f"M 570 {LY} L {XC} {LY}", LIVE, SW)
    s.path(f"M {XC} {LY} L {XC} {CY}", LIVE, SW)
    s.text(X0 - 14, LY + 8, "ফেজ", T_CALL, LIVE, 700, "end")

    # ── কমন থেকে দুই কয়েল ───────────────────────────────────────
    _node(s, XC, CY)
    s.path(f"M {XL} {CY} L {XR} {CY}", SYM, SW)
    s.path(f"M {XL} {CY} L {XL} {KY0}", SYM, SW)
    s.path(f"M {XR} {CY} L {XR} {KY0}", SYM, SW)
    vcoil(s, KY0, KY1, XL, SYM, 4, left=True)
    vcoil(s, KY0, KY1, XR, STEEL, 4, left=False)
    s.path(f"M {XL} {KY1} L {XL} {QY}", SYM, SW)
    s.path(f"M {XR} {KY1} L {XR} {QY}", SYM, SW)
    s.text(426, (KY0 + KY1) / 2 + 8, "রানিং কয়েল", T_CALL, NAVY, 700, "end")
    s.text(954, (KY0 + KY1) / 2 + 8, "স্টার্টিং কয়েল", T_CALL, STEEL, 700,
           "start")

    # ── ক্যাপাসিটর : দুই প্রান্তের মাঝে ──────────────────────────
    s.path(f"M {XL} {QY} L {XC - 13} {QY}", SYM, SW)
    cap_sym(s, XC, QY, 46, 54, SYM, vertical=False)
    s.path(f"M {XC + 13} {QY} L {XR} {QY}", SYM, SW)
    s.text(XC, QY + 54, "ক্যাপাসিটর", T_CALL, NAVY, 700, "middle")

    # ── নিউট্রাল : বাস → রানিং প্রান্ত ───────────────────────────
    s.path(f"M {X0} {NY} L {XL} {NY}", NEUT, SW)
    s.path(f"M {XL} {NY} L {XL} {QY}", NEUT, SW)
    _node(s, XL, QY)
    _node(s, XR, QY)
    s.text(X0 - 14, NY + 8, "নিউট্রাল", T_CALL, NEUT, 700, "end")

    # ── তিন প্রান্তের নাম ───────────────────────────────────────
    _term(s, XC, TOPB, "কমন: C", 16, -14)
    _term(s, XL, BOTB, "রানিং: R", -16, 30, "end")
    _term(s, XR, BOTB, "স্টার্টিং: S", 16, 30)

    y = note_strip(s, 700,
                   "ফেজ যায় কমন প্রান্তে, নিউট্রাল রানিং প্রান্তে; "
                   "ক্যাপাসিটর বসে রানিং ও স্টার্টিং প্রান্তের মাঝে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_cap_conn.svg")


def d08_direction():
    """নিউট্রাল প্রান্ত বদলে ঘূর্ণনের দিক উল্টানো।"""
    s = SVG(1240, 760)
    s.title("ফ্যানের ঘূর্ণনের দিক বদলানো", T_TITLE)
    PW, PH = 560, 540
    AY = 548                                # ঘূর্ণন-তিরের নিজস্ব ব্যান্ড

    for px, head, col, on_start, spin, rev in (
            (46, "নিউট্রাল রানিং প্রান্তে (R)", STEEL,
             False, "ঘোরে ঘড়ির কাঁটার দিকে", False),
            (634, "নিউট্রাল স্টার্টিং প্রান্তে (S)", GREEN,
             True, "ঘোরে উল্টো দিকে", True)):
        panel(s, px, 96, PW, PH, head, col)
        XC, XL, XR = px + 306, px + 186, px + 428
        LY, CY, KY0, KY1, QY, NY = 186, 236, 272, 380, 442, 500
        TOPB, BOTB = 212, 410

        s.rect(px + 126, TOPB, 362, BOTB - TOPB, "#F8FAFC", STEEL, 2,
               12, dash="9 6")

        s.path(f"M {px+134} {LY} L {XC} {LY}", LIVE, SW)
        s.path(f"M {XC} {LY} L {XC} {CY}", LIVE, SW)
        s.text(px + 126, LY + 8, "ফেজ", T_SMALL, LIVE, 700, "end")
        _node(s, XC, CY)
        s.path(f"M {XL} {CY} L {XR} {CY}", SYM, SW)
        s.path(f"M {XL} {CY} L {XL} {KY0}", SYM, SW)
        s.path(f"M {XR} {CY} L {XR} {KY0}", SYM, SW)
        vcoil(s, KY0, KY1, XL, SYM, 3, left=True)
        vcoil(s, KY0, KY1, XR, STEEL, 3, left=False)
        s.path(f"M {XL} {KY1} L {XL} {QY}", SYM, SW)
        s.path(f"M {XR} {KY1} L {XR} {QY}", SYM, SW)
        s.path(f"M {XL} {QY} L {XC - 12} {QY}", SYM, SW)
        cap_sym(s, XC, QY, 42, 48, SYM, vertical=False)
        s.path(f"M {XC + 12} {QY} L {XR} {QY}", SYM, SW)
        _node(s, XL, QY)
        _node(s, XR, QY)

        NX = XR if on_start else XL
        s.path(f"M {px+134} {NY} L {NX} {NY}", NEUT, SW)
        s.path(f"M {NX} {NY} L {NX} {QY}", NEUT, SW)
        s.text(px + 126, NY + 8, "নিউট্রাল", T_SMALL, NEUT, 700, "end")

        _term(s, XC, TOPB, "C", 14, -12)
        _term(s, XL, BOTB, "R", -14, 26, "end")
        _term(s, XR, BOTB, "S", 14, 26)

        # তিরটি নিউট্রাল তারের নিচে নিজের ব্যান্ডে — চাপা বাঁক (r=88) রাখায়
        # চূড়া NY থেকে ২৫ px নিচে থাকে, তাই তারের উপর দিয়ে যায় না।
        ar = s.arrow_defs(col, f"sp{px}", 13)
        x1, x2, sw_ = ((px + PW / 2 + 60, px + PW / 2 - 60, 0) if rev
                       else (px + PW / 2 - 60, px + PW / 2 + 60, 1))
        s.path(f"M {x1} {AY} A 88 88 0 0 {sw_} {x2} {AY}",
               col, 3.4, marker=ar)
        s.text(px + PW / 2, 96 + PH - 26, spin, T_NAME, col, 700, "middle")

    y = note_strip(s, 96 + PH + 22,
                   "ক্যাপাসিটরের তার নাড়িয়ে লাভ নেই; নিউট্রাল রানিং থেকে "
                   "স্টার্টিং প্রান্তে সরালেই ঘূর্ণনের দিক উল্টে যায়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d08_direction.svg")


def d09_board():
    """সুইচ বোর্ডে ফ্যানসহ সম্পূর্ণ সংযোগ।"""
    return two_panel(
        "d09_board", "সুইচ বোর্ডে ফ্যান ও রেগুলেটর",
        ("সার্কিট ডায়াগ্রাম (RAPTI সোর্স)", "c22_board_schem.png"),
        ("বাস্তব বোর্ড: দুটি রেগুলেটরসহ", "ph_board_reg.jpg"),
        "প্রতিটি ফ্যানের জন্য একটি সুইচ ও একটি রেগুলেটর; রেগুলেটর সব সময় "
        "সুইচের পরে ফেজ তারে বসে", h=620)


def d10_cap_family():
    """ক্যাপাসিটরের শ্রেণিবিভাগ — বাস্তব ছবিতে।"""
    s = SVG(1240, 640)
    s.title("ক্যাপাসিটরের প্রকারভেদ", T_TITLE)
    PW, GAP, PH = 365, 26, 400
    cases = [
        ("পোলারাইজড: ইলেক্ট্রোলাইটিক", "ph_cap_elko.jpg", RED,
         "গায়ে সাদা দাগ ও − চিহ্ন থাকে; DC সার্কিটে চলে"),
        ("নন-পোলারাইজড: সিরামিক", "ph_cap_ceramic.jpg", GREEN,
         "কোনো ধনাত্মক-ঋণাত্মক নেই; দুই দিকেই বসে"),
        ("ভেরিয়েবল: এয়ার", "ph_cap_var.jpg", STEEL,
         "ঘুরিয়ে মান বদলানো যায়; রেডিও-টিউনিংয়ে"),
    ]
    for i, (head, img, col, cap) in enumerate(cases):
        px = 46 + i * (PW + GAP)
        img_panel(s, px, 96, PW, PH, head, f"{IMG}/{img}", col)
        for j, ln in enumerate(wrap(cap, PW - 40, T_SMALL, 400)):
            s.text(px + PW / 2, 96 + PH + 30 + j * T_SMALL * 1.34, ln,
                   T_SMALL, "#39434D", 400, "middle")
    y = note_strip(s, 96 + PH + 92,
                   "ফ্যানের ক্যাপাসিটর সব সময় নন-পোলারাইজড ও AC রেটিংয়ের; "
                   "ইলেক্ট্রোলাইটিক ক্যাপাসিটর ফ্যানে বসালে তা ফেটে যাবে",
                   fill=REDBG, stroke=RED, tcolor="#7A1810")
    s.fit(y, 24)
    return s.save(f"{OUT}/d10_cap_family.svg")


def _cap_symbol(s, x, y, polarized, label):
    if polarized:
        s.path(f"M {x} {y} L {x+38} {y}", SYM, SW)
        s.line(x + 38, y - 24, x + 38, y + 24, SYM, SW + 1)
        s.path(f"M {x+60} {y-24} q -18 24 0 48", SYM, SW + 1)
        s.path(f"M {x+60} {y} L {x+100} {y}", SYM, SW)
        s.text(x + 28, y - 34, "+", 24, RED, 700, "middle")
    else:
        s.path(f"M {x} {y} L {x+38} {y}", SYM, SW)
        s.line(x + 38, y - 24, x + 38, y + 24, SYM, SW + 1)
        s.line(x + 60, y - 24, x + 60, y + 24, SYM, SW + 1)
        s.path(f"M {x+60} {y} L {x+100} {y}", SYM, SW)
    s.text(x + 118, y + 8, label, T_SMALL, "#39434D", 400)


def d11_cap_symbols():
    """পোলারাইজড ও নন-পোলারাইজড — আসল ছবিতে চেনার উপায় ও প্রতীক।"""
    s = SVG(1240, 920)
    s.title("পোলারাইজড ও নন-পোলারাইজড: চেনার উপায়", T_TITLE)
    PW = 1148

    # ── ১ম সারি : পোলারাইজড ─────────────────────────────────────
    PH1 = 352
    panel(s, 46, 96, PW, PH1, "পোলারাইজড: ইলেক্ট্রোলাইটিক", RED)
    EW = 604
    EH = round(EW * 775 / 2000)
    EX, EY = 46 + (PW - EW) / 2, 148
    s.image(EX, EY, EW, EH, f"{IMG}/ph_cap_elko.jpg", 6)

    def ea(fx, fy):
        return EX + fx * EW, EY + fy * EH

    callout(s, EX - 34, EY + 0.20 * EH, "মান 1000 µF · 25 V",
            *ea(0.115, 0.235), "end", T_SMALL)
    callout(s, EX - 34, EY + 0.76 * EH, "রুপালি দাগ ও − চিহ্ন",
            *ea(0.155, 0.760), "end", T_SMALL)
    callout(s, EX + EW + 34, EY + 0.24 * EH, "লম্বা পা = ধনাত্মক (+)",
            *ea(0.930, 0.520), "start", T_SMALL)
    callout(s, EX + EW + 34, EY + 0.86 * EH, "খাটো পা = ঋণাত্মক (−)",
            *ea(0.860, 0.715), "start", T_SMALL)
    _cap_symbol(s, 116, 96 + PH1 - 36, True, "পোলারাইজড প্রতীক")
    s.text(1128, 96 + PH1 - 28, "দাগের পাশের পা-ই ঋণাত্মক", T_SMALL, RED,
           700, "end")

    # ── ২য় সারি : নন-পোলারাইজড ──────────────────────────────────
    TY, PH2 = 96 + PH1 + 18, 340
    panel(s, 46, TY, PW, PH2, "নন-পোলারাইজড: ফ্যানের ক্যাপাসিটর", GREEN)
    FW = 212
    FH = round(FW * 924 / 761)
    FX, FY = 46 + (PW - FW) / 2, TY + 50
    s.image(FX, FY, FW, FH, f"{IMG}/ph_cap_can_face.jpg", 6)

    def fa(fx, fy):
        return FX + fx * FW, FY + fy * FH

    callout(s, FX - 34, FY + 0.16 * FH, "দুই টার্মিনাল একই রকম",
            *fa(0.31, 0.16), "end", T_SMALL)
    callout(s, FX - 34, FY + 0.54 * FH, "গায়ে + বা − কিছু নেই",
            *fa(0.14, 0.58), "end", T_SMALL)
    callout(s, FX + FW + 34, FY + 0.72 * FH, "350V.AC: AC লাইনের জন্য",
            *fa(0.77, 0.745), "start", T_SMALL)
    _cap_symbol(s, 116, TY + PH2 - 44, False, "নন-পোলারাইজড প্রতীক")
    s.text(1128, TY + PH2 - 36, "দুই দিকেই বসানো যায়", T_SMALL, GREEN,
           700, "end")

    y = note_strip(s, TY + PH2 + 22,
                   "AC লাইনে ভোল্টেজের দিক প্রতি অর্ধচক্রে উল্টে যায়; তাই "
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
