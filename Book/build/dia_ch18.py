# -*- coding: utf-8 -*-
"""অধ্যায় ১৮ — মোটর : ডায়াগ্রাম।

`Motor.docx`-এর ছবিগুলো ইন্টারনেট থেকে কপি করা স্টক ছবি ও ওয়াটারমার্কযুক্ত
স্ক্রিনশট (ব্র্যান্ডের ক্যাপাসিটর ছবি, তৃতীয় পক্ষের ওয়েবসাইটের লোগো) —
সরাসরি বসানোর মতো নয়। কোনো উৎস স্লাইডেও (`Circuit Diagram.pptx`,
`HW Connection Diagram All.pptx`) মোটরের ছবি নেই (যাচাই করা হয়েছে)।
তাই তিনটি ডায়াগ্রামই এই বইয়ের নিজস্ব স্কিমেটিক অঙ্কনরীতিতে নতুন করে
আঁকা — কোনো ব্র্যান্ড, লোগো বা ওয়াটারমার্ক নেই।

ক্যাপাসিটর-সংযোগ ও স্টার/ডেল্টা সংযোগের টপোলজি ইনস্টিটিউটের নিজস্ব
`Motor.docx`-এর লেখা ও সূত্র থেকে যাচাই করে নেওয়া (রান ক্যাপাসিটর সবসময়
সিরিজে, স্টার্ট ক্যাপাসিটর সেন্ট্রিফিউগাল সুইচ দিয়ে বিচ্ছিন্ন হয়)।

লেবেলের নিয়ম অধ্যায় ১৫ থেকে বহাল: প্যানেল/ছবির শিরোনাম বিশেষ্য, যন্ত্রাংশের
লেবেল এক-দুই শব্দ, নোট-পটি এক লাইনের একটি তথ্য — কারণ ও সতর্কবাণী লেখায়।
"""
import os
import math
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch18")

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
WCOIL = "#1D5B8F"
CAPCOL = "#B3541E"
METAL = "#8D9AA8"
STATORFILL = "#E7ECF1"
ROTORFILL = "#C9D4DE"


# ── shared helpers (অধ্যায় ১৫ থেকে অভিন্ন) ─────────────────────────────
def panel(s, x, y, w, h, title, col=STEEL):
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def note_strip(s, y, text, x=46, w=1148, fill="#EAF2FA", stroke=STEEL,
               tcolor=NAVY, size=T_NAME):
    if tw(text, size, 700) > w - 60:
        raise ValueError(f"note_strip এক লাইনে ধরে না: {text!r}")
    s.rect(x, y, w, 58, fill, stroke, 2, 11)
    s.text(x + w / 2, y + 36, text, size, tcolor, 700, "middle")
    return y + 58


def callout(s, x, y, text, tx, ty, anchor="end", size=T_CALL, col=NAVY):
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    w = tw(text, size, 700)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle"
                                      else x - w)
    x1 = x0 + w
    start = x1 + 10 if tx > x1 else x0 - 10
    s.path(f"M {start} {y} L {tx} {ty}", STEEL, 2.2)
    s.circle(tx, ty, 5, STEEL)


def node(s, x, y, col=SYM, r=6.5):
    s.circle(x, y, r, col)


# ── বর্তনীর প্রতীক ───────────────────────────────────────────────────────
def coil_sym(s, x, y, w, n=4, amp=15, col=WCOIL, sw=SW):
    """অনুভূমিক তারে n-টি বাম্প দিয়ে উইন্ডিং বোঝানো। x = বাঁ প্রান্ত।"""
    step = w / n
    d = f"M {x:.1f} {y:.1f} "
    for i in range(n):
        cx = x + step * i + step / 2
        up = y - amp if i % 2 == 0 else y + amp
        d += f"Q {cx:.1f} {up:.1f} {x + step * (i + 1):.1f} {y:.1f} "
    s.path(d, col, sw)
    return x + w


def cap_sym(s, x, y, gap=14, h=32, col=CAPCOL, sw=SW):
    """উল্লম্ব তারের উপর ক্যাপাসিটরের দুই পাত।"""
    s.path(f"M {x - gap/2:.1f} {y - h/2:.1f} L {x - gap/2:.1f} {y + h/2:.1f}",
           col, sw + 0.8)
    s.path(f"M {x + gap/2:.1f} {y - h/2:.1f} L {x + gap/2:.1f} {y + h/2:.1f}",
           col, sw + 0.8)


def switch_sym(s, x, y, w=44, col=SYM, sw=SW):
    """সেন্ট্রিফিউগাল সুইচ — খোলা অবস্থায় আঁকা।"""
    node(s, x, y, col, 5)
    node(s, x + w, y, col, 5)
    s.path(f"M {x:.1f} {y:.1f} L {x + w*0.72:.1f} {y - 15:.1f}", col, sw)


# ═══════════════════════════════════════════════════════════════════════
def d01_parts():
    """মোটরের প্রধান অংশ — স্কিমেটিক কাটাছেঁড়া দৃশ্য।"""
    s = SVG(1240, 620)
    s.title("মোটরের প্রধান অংশ", T_TITLE)

    cx, cy = 560, 300
    fw, fh = 480, 200               # স্টেটর ফ্রেম
    fx, fy = cx - fw / 2, cy - fh / 2

    # স্টেটর ফ্রেম
    s.rect(fx, fy, fw, fh, STATORFILL, METAL, 3.2, 22)
    # রোটর
    rw, rh = 360, 90
    rx, ry = cx - rw / 2, cy - rh / 2
    s.rect(rx, ry, rw, rh, ROTORFILL, SYM, 2.6, 16)
    # শ্যাফট — দুই পাশে বেরিয়ে থাকা
    s.rect(fx - 90, cy - 14, 90, 28, "#B7C2CE", SYM, 2, 4)
    s.rect(fx + fw, cy - 14, 96, 28, "#B7C2CE", SYM, 2, 4)
    # বিয়ারিং — শ্যাফটের গোড়ায় দুই বৃত্ত
    node(s, fx - 8, cy, "#F1F5F8", 16)
    s.circle(fx - 8, cy, 16, "#F1F5F8", METAL, 2.6)
    node(s, fx + fw + 8, cy, "#F1F5F8", 16)
    s.circle(fx + fw + 8, cy, 16, "#F1F5F8", METAL, 2.6)

    # উইন্ডিং — স্টেটরের দুই মাথায় দৃশ্যমান কুণ্ডলী
    coil_sym(s, fx + 26, fy + 20, fw - 52, n=8, amp=8, col=WCOIL, sw=2.6)
    coil_sym(s, fx + 26, fy + fh - 20, fw - 52, n=8, amp=8, col=WCOIL, sw=2.6)

    # ব্রাশ ও কমিউটেটর — শ্যাফটের ডান প্রান্তে ছোট ইনসেট
    bcx = fx + fw + 96 + 70
    s.circle(bcx, cy, 26, "#F4E7D6", "#8A6A2A", 2.6)
    for a in (60, 180, 300):
        t = math.radians(a)
        s.line(bcx + 10 * math.cos(t), cy + 10 * math.sin(t),
               bcx + 24 * math.cos(t), cy + 24 * math.sin(t),
               "#8A6A2A", 1.6)
    s.rect(bcx - 34, cy - 46, 14, 26, "#5B4632", "none", 0, 2)
    s.rect(bcx + 20, cy + 20, 14, 26, "#5B4632", "none", 0, 2)

    # লেবেল — বাইরে, লিডার লাইনে
    callout(s, 120, fy - 34, "স্টেটর", fx + 60, fy + 8, "start", T_CALL, NAVY)
    callout(s, 120, cy - 60, "উইন্ডিং", fx + 40, fy + 16, "start", T_CALL,
            WCOIL)
    callout(s, 120, cy + 90, "রোটর", rx + 30, ry + rh, "start", T_CALL, NAVY)
    callout(s, 120, cy + 150, "বিয়ারিং", fx - 8, cy + 14, "start", T_CALL,
            "#5B6672")
    callout(s, 1120, fy - 34, "শ্যাফট", fx + fw + 60, cy - 12, "end",
            T_CALL, NAVY)
    callout(s, 1120, cy + 90, "ব্রাশ ও কমিউটেটর", bcx, cy - 30, "end",
            T_CALL, "#8A6A2A")

    y = note_strip(s, fy + fh + 96,
                   "ব্রাশ ও কমিউটেটর শুধু DC মোটরে থাকে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_parts.svg")


def d02_capacitor():
    """সিঙ্গেল ফেজ মোটর — ক্যাপাসিটর-স্টার্ট, ক্যাপাসিটর-রান সংযোগ।"""
    s = SVG(1240, 640)
    s.title("সিঙ্গেল ফেজ মোটর — ক্যাপাসিটর সংযোগ", T_TITLE)

    LX = 130                        # L বাস
    RX = 1030                       # ডান বাস (কমন)
    NY_TOP = 210                    # রানিং উইন্ডিং শাখা
    NY_MID = 360                    # রান ক্যাপাসিটর + স্টার্টিং উইন্ডিং শাখা
    NY_BOT = 500                    # স্টার্ট ক্যাপাসিটর + সুইচ শাখা
    NODE_X = 560                    # মাঝের শাখা যেখানে মিশছে

    # L ও N বাস
    s.path(f"M {LX} {NY_TOP-40} L {LX} {NY_BOT+40}", SYM, SW)
    s.text(LX - 34, NY_TOP - 40 + 8, "L", T_NODE, LIVE, 700, "end")
    s.path(f"M {RX} {NY_TOP} L {RX} {NY_MID} L {RX+60} {NY_MID} "
           f"L {RX+60} {NY_MID+60}", SYM, SW)
    s.text(RX + 100, NY_MID + 60 + 8, "N", T_NODE, NEUT, 700, "start")
    node(s, LX, NY_TOP); node(s, LX, NY_MID); node(s, LX, NY_BOT)

    # শাখা ১ — রানিং উইন্ডিং, সরাসরি L থেকে N
    s.path(f"M {LX} {NY_TOP} L 330 {NY_TOP}", SYM, SW)
    ex = coil_sym(s, 330, NY_TOP, 340, n=6, amp=16)
    s.path(f"M {ex:.0f} {NY_TOP} L {RX} {NY_TOP}", SYM, SW)
    s.text((330 + ex) / 2, NY_TOP - 34, "রানিং উইন্ডিং", T_NAME, WCOIL, 700,
           "middle")

    # শাখা ২ — রান ক্যাপাসিটর তারপর স্টার্টিং উইন্ডিং
    s.path(f"M {LX} {NY_MID} L 300 {NY_MID}", SYM, SW)
    cap_sym(s, 300, NY_MID)
    s.text(300, NY_MID - 34, "রান ক্যাপাসিটর", T_NAME, CAPCOL, 700, "middle")
    s.path(f"M 314 {NY_MID} L {NODE_X} {NY_MID}", SYM, SW)
    node(s, NODE_X, NY_MID)
    ex2 = coil_sym(s, NODE_X, NY_MID, 340, n=6, amp=16)
    s.path(f"M {ex2:.0f} {NY_MID} L {RX} {NY_MID}", SYM, SW)
    s.text((NODE_X + ex2) / 2, NY_MID - 34, "স্টার্টিং উইন্ডিং", T_NAME,
           WCOIL, 700, "middle")

    # শাখা ৩ — স্টার্ট ক্যাপাসিটর + সেন্ট্রিফিউগাল সুইচ, নোডে মিশছে
    s.path(f"M {LX} {NY_BOT} L 300 {NY_BOT}", SYM, SW)
    cap_sym(s, 300, NY_BOT)
    s.text(270, NY_BOT + 46, "স্টার্ট ক্যাপাসিটর", T_NAME, CAPCOL, 700,
           "end")
    s.path(f"M 314 {NY_BOT} L 400 {NY_BOT}", SYM, SW)
    switch_sym(s, 400, NY_BOT, 44)
    s.text(480, NY_BOT + 46, "সেন্ট্রিফিউগাল সুইচ", T_NAME, SYM, 700,
           "start")
    s.path(f"M 444 {NY_BOT} L {NODE_X} {NY_BOT} L {NODE_X} {NY_MID}", SYM, SW)

    y = note_strip(s, NY_BOT + 96,
                   "রান ক্যাপাসিটর সবসময় সার্কিটে থাকে, স্টার্ট ক্যাপাসিটর "
                   "কেবল চালুর মুহূর্তে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_capacitor.svg")


def _star_panel(s, x, y, w, h):
    cx, topy = x + w / 2, y + 70
    ncx, ncy = cx, y + h - 90
    ends = []
    for ang, lab in ((-58, "R"), (0, "Y"), (58, "B")):
        t = math.radians(ang - 90)
        ex = ncx + 190 * math.cos(t)
        ey = ncy + 190 * math.sin(t)
        s.path(f"M {ncx:.0f} {ncy:.0f} L {ex:.0f} {ey:.0f}", WCOIL, SW)
        node(s, ex, ey, SYM, 7)
        ends.append((ex, ey, lab))
    node(s, ncx, ncy, NEUT, 8)
    s.text(ncx, ncy + 40, "N", T_NAME, NEUT, 700, "middle")
    for ex, ey, lab in ends:
        ty = ey - 20 if ey < ncy else ey + 34
        s.text(ex, ty, lab, T_NAME, NAVY, 700, "middle")


def _delta_panel(s, x, y, w, h):
    cx = x + w / 2
    top = (cx, y + 128)
    bl = (x + 92, y + h - 70)
    br = (x + w - 92, y + h - 70)
    for (x1, y1), (x2, y2) in ((top, br), (br, bl), (bl, top)):
        s.path(f"M {x1:.0f} {y1:.0f} L {x2:.0f} {y2:.0f}", WCOIL, SW)
    for (px, py), lab, dy in ((top, "R", -20), (bl, "Y", 34), (br, "B", 34)):
        node(s, px, py, SYM, 7)
        s.text(px, py + dy, lab, T_NAME, NAVY, 700, "middle")


def d03_star_delta():
    """থ্রি-ফেজ মোটর — স্টার (Y) ও ডেল্টা (Δ) সংযোগ।"""
    s = SVG(1240, 560)
    s.title("থ্রি-ফেজ মোটর সংযোগ — স্টার ও ডেল্টা", T_TITLE)
    pw, ph = 560, 380
    panel(s, 46, 96, pw, ph, "স্টার (Y) সংযোগ", STEEL)
    panel(s, 1194 - pw, 96, pw, ph, "ডেল্টা (Δ) সংযোগ", GREEN)
    _star_panel(s, 46, 96, pw, ph)
    _delta_panel(s, 1194 - pw, 96, pw, ph)
    y = note_strip(s, 96 + ph + 24,
                   "নেমপ্লেট ও সাপ্লাই অনুযায়ী সংযোগ বাছাই হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_star_delta.svg")


ALL = [d01_parts, d02_capacitor, d03_star_delta]

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
