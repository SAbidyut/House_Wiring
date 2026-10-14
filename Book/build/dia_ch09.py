# -*- coding: utf-8 -*-
"""অধ্যায় ৯ — মাল্টিপ্লাগ সার্কিট : ডায়াগ্রাম।

সার্কিট ও কানেকশন ডায়াগ্রামগুলো RAPTI-র নিজস্ব সোর্স থেকে হুবহু বসানো —
`Circuit Diagram.pptx` স্লাইড ১৪–১৫ (সার্কিট) এবং
`HW Connection Diagram All.pptx` স্লাইড ১৪, ১৫ ও ৩৯ (কানেকশন)।
কেবল যন্ত্রের গঠন ও পিন-বিন্যাসের ছবি নতুন করে আঁকা।
"""
import os
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams", "ch09")
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "ch09")

T_TITLE = 34
T_NODE = 28
T_NAME = 25.5
T_BODY = 22.5
T_SMALL = 22.5
T_CALL = 25          # d01 ~14 cm চওড়া বসে বলে লেবেল একটু বড় (≈8 pt)
LH = 1.42

SYM = "#12324D"
SW = 3.2
BROWN = "#7A4A21"
BLUE = "#1E63B5"
EGREEN = "#2E8B31"
PLATE = "#F2F5F8"
PLATE_E = "#9AA6B2"
METAL = "#8D9AA8"


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
    """লেবেল ও তার লিডার লাইন — লেখা সবসময় ছবির বাইরে থাকে।"""
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    x0 = x + 10 if anchor == "end" else x - 10
    s.path(f"M {x0} {y} L {tx} {ty}", STEEL, 2.2)
    s.circle(tx, ty, 5, STEEL)


def image_panel(s, cx, top, bottom, path, half=268, pad=14):
    """সোর্স ডায়াগ্রাম হুবহু বসানো — নতুন করে আঁকা নয়।"""
    s.image_fit(cx - half, top, half * 2, bottom - top, path, pad)


def _sheet(fname, title, left_img, right_img, note, h=560):
    """দুই প্যানেলের শিট — বাঁয়ে সার্কিট, ডানে কানেকশন ডায়াগ্রাম।"""
    s = SVG(1240, h)
    s.title(title, T_TITLE)
    PW = 560
    panel(s, 46, 96, PW, h - 230, "সার্কিট ডায়াগ্রাম", STEEL)
    panel(s, 634, 96, PW, h - 230, "কানেকশন ডায়াগ্রাম", GREEN)
    image_panel(s, 46 + PW / 2, 150, h - 156, f"{IMG}/{left_img}")
    image_panel(s, 634 + PW / 2, 150, h - 156, f"{IMG}/{right_img}")
    y = note_strip(s, h - 118, note)
    s.fit(y, 22)
    return s.save(f"{OUT}/{fname}.svg")


# ── device faces (front view, mechanical only — no circuit topology) ────
def module_plate(s, cx, y, w=118, h=190):
    s.rect(cx - w / 2, y, w, h, PLATE, PLATE_E, 2.4, 12)
    return cx - w / 2, y, w, h


def face_switch(s, cx, cy, on=False):
    """রকার সুইচের সাদা কি।"""
    s.rect(cx - 26, cy - 44, 52, 88, "#FFFFFF", "#9AA6B2", 2.2, 7)
    s.rect(cx - 20, cy - 36, 40, 72, "#FAFBFC", "#C3CEDA", 1.6, 5)
    s.rect(cx - 6, cy - 30, 12, 20, RED if on else "#D8DEE5",
           "#B0BAC5", 1.4, 2)


def face_indicator(s, cx, cy):
    s.rect(cx - 26, cy - 44, 52, 88, "#FFFFFF", "#9AA6B2", 2.2, 7)
    s.rect(cx - 18, cy - 34, 36, 68, "#E8483A", "#9C2B20", 2, 5)


def face_socket2(s, cx, cy):
    """২-পিন সকেটের মুখ — খাড়া মডিউলে উপরে-নিচে দুটি ছিদ্র।

    বিন্যাসটা চিত্র ৯.৪-এর সোর্স মডিউলের হুবহু — বাজারের পিয়ানো বোর্ডে
    সকেট এভাবেই বসে, ছিদ্র দুটো পাশাপাশি নয়, একটার নিচে আরেকটা।
    """
    s.rect(cx - 31, cy - 44, 62, 88, "#FFFFFF", "#9AA6B2", 2.2, 7)
    s.rect(cx - 22, cy - 36, 44, 72, "#FAFBFC", "#C3CEDA", 1.6, 5)
    for dy in (-17, 17):
        s.circle(cx, cy + dy, 9.5, "#3B4550")


def face_socket3(s, cx, cy):
    """৩-পিন সকেটের মুখ — উপরে আর্থ, নিচে ফেজ ও নিউট্রাল।"""
    s.rect(cx - 34, cy - 46, 68, 92, "#FFFFFF", "#9AA6B2", 2.2, 8)
    s.rect(cx - 5, cy - 32, 10, 22, "#3B4550")
    s.rect(cx - 24, cy + 2, 9, 20, "#3B4550")
    s.rect(cx + 15, cy + 2, 9, 20, "#3B4550")


def fuse_body(s, cx, cy):
    s.rect(cx - 26, cy - 44, 52, 88, "#FFFFFF", "#9AA6B2", 2.2, 7)
    s.rect(cx - 17, cy - 26, 34, 52, "#FFF3C4", "#B08C00", 2, 4)
    s.path(f"M {cx} {cy-26} L {cx} {cy+26}", "#8A6D00", 3)


def plug2(s, cx, cy, scale=1.0, up=True):
    """২-পিন প্লাগ।  `up=False` হলে পিন নিচের দিকে, কর্ড ঢোকে উপর দিয়ে —
    কর্ড সব সময় পিনের উল্টো দিক থেকে আসে, পিনের পাশ থেকে নয়।"""
    k = scale
    s.rect(cx - 46 * k, cy - 34 * k, 92 * k, 68 * k, "#FFFFFF", "#7C8794", 2.6, 9)
    for dx in (-19, 19):
        y_ = cy - 78 * k if up else cy + 34 * k
        s.rect(cx + dx * k - 5 * k, y_, 10 * k, 44 * k, METAL, "#6B7684", 2, 3)
    return cy - 78 * k if up else cy - 34 * k


def plug3(s, cx, cy, scale=1.0):
    """৩-পিন প্লাগ — আর্থ পিন লম্বা ও মোটা।"""
    k = scale
    s.rect(cx - 52 * k, cy - 36 * k, 104 * k, 72 * k, "#FFFFFF", "#7C8794", 2.6, 9)
    s.rect(cx - 7 * k, cy - 104 * k, 14 * k, 68 * k, METAL, "#6B7684", 2, 3)
    for dx in (-28, 28):
        s.rect(cx + dx * k - 5 * k, cy - 82 * k, 10 * k, 46 * k,
               METAL, "#6B7684", 2, 3)
    return cy - 104 * k


# ═══════════════════════════════════════════════════════════════════════
def d01_parts():
    """পিয়ানো মাল্টিপ্লাগ বোর্ডের অংশ পরিচিতি।"""
    s = SVG(1240, 980)
    s.title("পিয়ানো মাল্টিপ্লাগের গঠন ও অংশ পরিচিতি", T_TITLE)

    BX, BY, BW, BH = 250, 268, 930, 262
    s.rect(BX, BY, BW, BH, "#E7ECF1", "#7C8794", 3, 18)
    s.rect(BX + 14, BY + 14, BW - 28, BH - 28, "#F7FAFC", "#B0BAC5", 1.8, 12)

    mods = [("ফিউজ", fuse_body), ("ইন্ডিকেটর", face_indicator),
            ("সুইচ ১", lambda a, b, c: face_switch(a, b, c, True)),
            ("সকেট ১", face_socket2),
            ("সুইচ ২", lambda a, b, c: face_switch(a, b, c, False)),
            ("সকেট ২", face_socket2)]
    n = len(mods)
    step = (BW - 80) / n
    cy = BY + BH / 2
    for i, (name, draw) in enumerate(mods):
        cx = BX + 40 + step * (i + 0.5)
        module_plate(s, cx, BY + 36, 118, BH - 72)
        draw(s, cx, cy)
        ly = 150 if i % 2 == 0 else 212
        s.text(cx, ly, name, T_CALL, NAVY, 700, "middle")
        s.path(f"M {cx} {ly+10} L {cx} {BY+30}", STEEL, 2.2)
        s.circle(cx, BY + 30, 5, STEEL)

    # flexible cord out of the left end, down and along to a 2-pin plug
    # flexible cord out of the left end, down into the BACK of the plug —
    # the pins point away from the cord, as on a real plug
    s.path(f"M {BX} {cy} L 150 {cy} L 150 650", "#3B4550", 9)
    plug2(s, 150, 682, 0.9, up=False)

    callout(s, 760, 600, "বোর্ড বডি (অগ্নিরোধী PVC)", BX + BW / 2, BY + BH + 2, "start")
    callout(s, 330, 580, "ফ্লেক্সিবল কর্ড", 156, 580, "start")
    callout(s, 330, 690, "২-পিন প্লাগ", 194, 690, "start")

    y = note_strip(s, 790,
                   "ফিউজ মেইন লাইনে সিরিজে, প্রতিটি সকেট নিজের সুইচসহ "
                   "পরস্পর প্যারালালে; তাই এটি একটি মিশ্র সার্কিট")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_parts.svg")


def d02_types():
    """মাল্টিপ্লাগের প্রকারভেদ।"""
    s = SVG(1240, 620)
    s.title("মাল্টিপ্লাগের প্রকারভেদ", T_TITLE)

    cw, gapx = 356, 40
    x0 = (1240 - (3 * cw + 2 * gapx)) / 2
    cards = [
        ("পিয়ানো মাল্টিপ্লাগ", "Piano Multiplug",
         "লম্বা বোর্ডে পিয়ানোর কি-এর মতো সারি সারি সুইচ ও সকেট", "piano"),
        ("গ্যাং মাল্টিপ্লাগ", "Gang Multiplug",
         "একই প্লেটে একাধিক ৩-পিন সকেট, প্রতিটির সঙ্গে সুইচ", "gang"),
        ("এক্সটেনশন মাল্টিপ্লাগ", "Extension Multiplug",
         "লম্বা কর্ডসহ বহনযোগ্য বোর্ড, ইচ্ছামতো সরানো যায়", "ext"),
    ]
    for i, (bn_, en, note, kind) in enumerate(cards):
        x = x0 + i * (cw + gapx)
        s.rect(x, 96, cw, 358, "#FCFDFE", LINE, 1.8, 14)
        cx = x + cw / 2
        if kind == "piano":
            s.rect(cx - 148, 168, 296, 116, "#E7ECF1", "#7C8794", 2.6, 12)
            for k in range(4):
                mx = cx - 111 + k * 74
                s.rect(mx - 28, 182, 56, 88, PLATE, PLATE_E, 2, 8)
                if k % 2 == 0:
                    face_switch(s, mx, 226, k == 0)
                else:
                    face_socket2(s, mx, 226)
        elif kind == "gang":
            s.rect(cx - 148, 162, 296, 128, "#F7FAFC", "#7C8794", 2.6, 12)
            for dx in (-74, 74):
                s.rect(cx + dx - 62, 174, 124, 104, "#FFFFFF", "#9AA6B2", 2.2, 10)
                face_socket3(s, cx + dx - 22, 226)
                face_switch(s, cx + dx + 34, 226, dx > 0)
        else:
            s.rect(cx - 84, 172, 236, 108, "#E7ECF1", "#7C8794", 2.6, 12)
            for k in range(3):
                face_socket2(s, cx - 40 + k * 74, 226)
            s.path(f"M {cx-84} 226 L {cx-140} 226 L {cx-140} 284", "#3B4550", 8)
            plug2(s, cx - 140, 302, 0.55, up=False)

        s.text(cx, 350, bn_, T_NAME, NAVY, 700, "middle")
        s.text(cx, 380, en, T_SMALL, STEEL, 600, "middle")
        for j, ln in enumerate(wrap(note, cw - 52, T_SMALL, 400)):
            s.text(cx, 412 + j * T_SMALL * 1.34, ln, T_SMALL, GREY, 400, "middle")

    y = note_strip(s, 486,
                   "প্রকার যা-ই হোক, ভেতরের সংযোগনীতি একই: "
                   "মেইন সুইচ ও ফিউজ সিরিজে, সকেটগুলো প্যারালালে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_types.svg")


def d03_pins():
    """২-পিন ও ৩-পিন প্লাগ-সকেটের পিন বিন্যাস।"""
    s = SVG(1240, 700)
    s.title("২-পিন ও ৩-পিন প্লাগ-সকেটের পিন বিন্যাস", T_TITLE)

    PW = 560
    panel(s, 46, 96, PW, 452, "২-পিন প্লাগ ও সকেট", STEEL)
    panel(s, 634, 96, PW, 452, "৩-পিন প্লাগ ও সকেট", GREEN)

    # ── two-pin ────────────────────────────────────────────────────────
    cx = 46 + PW / 2 - 40
    plug2(s, cx, 300, 1.0)
    s.text(cx, 412, "প্লাগ", T_BODY, NAVY, 700, "middle")
    s.text(cx - 19, 196, "L", T_NAME, BROWN, 700, "middle")
    s.text(cx + 19, 196, "N", T_NAME, BLUE, 700, "middle")

    sx = 46 + PW - 130
    s.rect(sx - 45, 236, 90, 144, "#FFFFFF", "#9AA6B2", 2.4, 10)
    s.rect(sx - 32, 250, 64, 116, "#FAFBFC", "#C3CEDA", 1.8, 7)
    for dy in (-28, 28):
        s.circle(sx, 308 + dy, 13, "#3B4550")
    s.text(sx, 412, "সকেট", T_BODY, NAVY, 700, "middle")

    s.text(46 + PW / 2, 460,
           "শুধু ফেজ ও নিউট্রাল, আর্থ নেই", T_BODY, RED, 700, "middle")
    s.text(46 + PW / 2, 496,
           "ধাতব বডির যন্ত্রে ব্যবহার করা যাবে না", T_SMALL, GREY, 400, "middle")

    # ── three-pin ──────────────────────────────────────────────────────
    cx = 634 + PW / 2 - 40
    plug3(s, cx, 300, 1.0)
    s.text(cx, 412, "প্লাগ", T_BODY, NAVY, 700, "middle")
    s.text(cx, 172, "E", T_NAME, EGREEN, 700, "middle")
    s.text(cx - 28, 200, "L", T_NAME, BROWN, 700, "middle")
    s.text(cx + 28, 200, "N", T_NAME, BLUE, 700, "middle")

    sx = 634 + PW - 130
    s.rect(sx - 56, 238, 112, 136, "#FFFFFF", "#9AA6B2", 2.4, 10)
    s.rect(sx - 7, 264, 14, 30, "#3B4550")
    s.rect(sx - 34, 314, 12, 28, "#3B4550")
    s.rect(sx + 22, 314, 12, 28, "#3B4550")
    s.text(sx, 412, "সকেট", T_BODY, NAVY, 700, "middle")

    s.text(634 + PW / 2, 460,
           "আর্থ পিন লম্বা ও মোটা; আগে ঢোকে, পরে বের হয়",
           T_BODY, EGREEN, 700, "middle")
    s.text(634 + PW / 2, 496,
           "লম্বা পিনই সকেটের শাটার খুলে দেয়", T_SMALL, GREY, 400, "middle")

    y = note_strip(s, 576,
                   "IEC 60884-1 অনুযায়ী গৃহস্থালির প্লাগ-সকেট সর্বোচ্চ 440 V, "
                   "32 A পর্যন্ত রেটিংয়ে তৈরি হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_pins.svg")


def d04_piano():
    return _sheet("d04_piano", "পিয়ানো মাল্টিপ্লাগ (২-পিন) সার্কিট",
                  "d04_piano_schem.png", "d04_piano_conn.png",
                  "ফিউজ মেইন লাইনে সিরিজে; ইন্ডিকেটর ও প্রতিটি সুইচ-সকেট "
                  "শাখা পরস্পর প্যারালালে", 600)


def d05_gang():
    return _sheet("d05_gang", "গ্যাং মাল্টিপ্লাগ (৩-পিন) সার্কিট",
                  "d05_gang_schem.png", "d05_gang_conn.png",
                  "প্রতিটি সকেটের L, N ও E আলাদা বাসে প্যারালালে; "
                  "সুইচ বসে শুধু ফেজ তারে", 600)


def d06_three():
    """তিন সকেটের পিয়ানো মাল্টিপ্লাগ — কেবল কানেকশন ডায়াগ্রাম।"""
    s = SVG(1240, 820)
    s.title("তিন সকেটের পিয়ানো মাল্টিপ্লাগের কানেকশন ডায়াগ্রাম", T_TITLE)
    panel(s, 46, 96, 1148, 588, "কানেকশন ডায়াগ্রাম", GREEN)
    s.image_fit(70, 158, 1100, 508, f"{IMG}/d06_three_conn.png", 8)
    y = note_strip(s, 712,
                   "সকেটের সংখ্যা বাড়লেও নিয়ম একই; প্রতিটি নতুন সুইচ-সকেট "
                   "শাখা আগের শাখার সঙ্গে প্যারালালে বসে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_three.svg")


ALL = [d01_parts, d02_types, d03_pins, d04_piano, d05_gang, d06_three]

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
