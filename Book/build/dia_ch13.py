# -*- coding: utf-8 -*-
"""অধ্যায় ১৩ — টু-ওয়ে ও থ্রি-ওয়ে সুইচ : ডায়াগ্রাম।

দুই জায়গা থেকে বাতি নিয়ন্ত্রণ ও টানেল ওয়্যারিংয়ের সার্কিট ও কানেকশন
ডায়াগ্রাম RAPTI-র নিজস্ব সোর্স থেকে হুবহু বসানো — `Circuit Diagram.pptx`
স্লাইড ১৭ ও ১৮, `HW Connection Diagram All.pptx` স্লাইড ১৭ ও ১৮।

সুইচের ভেতরের গঠন, প্রতীক, চার অবস্থার ছক, ইন্টারমিডিয়েট সুইচ, তিন জায়গা
থেকে নিয়ন্ত্রণ ও সিঁড়ির লে-আউট — এগুলোর কোনো সোর্স-ছবি নেই বলে নতুন
করে আঁকা।
"""
import os
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch13")
IMG = os.path.join(HERE, "assets", "ch13")

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
STRAP = "#1D5B8F"
GLOW = "#F5C445"
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
def node(s, x, y, col=SYM, r=6.5):
    s.circle(x, y, r, col)


def lamp_sym(s, cx, cy, r=26, on=False):
    """বাতির প্রতীক — বৃত্তের ভেতরে আড়াআড়ি দুই দাগ।"""
    s.circle(cx, cy, r, GLOW if on else "#FFFFFF", SYM, SW)
    k = r * 0.62
    s.path(f"M {cx-k:.1f} {cy-k:.1f} L {cx+k:.1f} {cy+k:.1f}", SYM, SW - 0.6)
    s.path(f"M {cx+k:.1f} {cy-k:.1f} L {cx-k:.1f} {cy+k:.1f}", SYM, SW - 0.6)


def sw1_sym(s, x, y, on=False, span=78):
    """ওয়ান-ওয়ে সুইচ — একটি চলমান পাত, একটি স্থির সংস্পর্শ।"""
    node(s, x, y)
    node(s, x + span, y)
    if on:
        s.path(f"M {x} {y} L {x+span} {y}", SYM, SW)
    else:
        s.path(f"M {x} {y} L {x+span-10} {y-36}", SYM, SW)


def sw2_sym(s, x, y, sel="up", span=80, spread=46, live=False):
    """টু-ওয়ে সুইচ — কমন প্রান্ত বাঁয়ে, দুই স্ট্র্যাপার প্রান্ত ডানে।"""
    node(s, x, y)
    node(s, x + span, y - spread)
    node(s, x + span, y + spread)
    ty = y - spread if sel == "up" else y + spread
    s.path(f"M {x} {y} L {x+span-7} {ty + (7 if sel == 'up' else -7)}",
           LIVE if live else SYM, SW + 0.6)


def inter_sym(s, x, y, crossed=False, w=156, spread=46):
    """ইন্টারমিডিয়েট সুইচ — চার প্রান্ত, ভেতরে সোজা বা আড়াআড়ি সংযোগ।"""
    s.rect(x + 26, y - spread - 34, w - 52, 2 * spread + 68, "#FCFDFE",
           STEEL, 2.2, 10, dash="9 6")
    for dy in (-spread, spread):
        node(s, x, y + dy)
        node(s, x + w, y + dy)
    if crossed:
        s.path(f"M {x} {y-spread} L {x+w} {y+spread}", SYM, SW + 0.6)
        s.path(f"M {x} {y+spread} L {x+w} {y-spread}", SYM, SW + 0.6)
    else:
        s.path(f"M {x} {y-spread} L {x+w} {y-spread}", SYM, SW + 0.6)
        s.path(f"M {x} {y+spread} L {x+w} {y+spread}", SYM, SW + 0.6)


# ═══════════════════════════════════════════════════════════════════════
def d01_2way_inside():
    """টু-ওয়ে সুইচের ভেতরের গঠন ও দুই অবস্থান।"""
    s = SVG(1240, 800)
    s.title("টু-ওয়ে সুইচের ভেতরে কী ঘটে", T_TITLE)

    PW, PH = 560, 400
    for i, (px, head, sel, col) in enumerate(
            ((46, "অবস্থান ১ — কমন যুক্ত L1-এর সঙ্গে", "up", STEEL),
             (634, "অবস্থান ২ — কমন যুক্ত L2-এর সঙ্গে", "down", GREEN))):
        panel(s, px, 96, PW, PH, head, col)
        CX, CY = px + 190, 300
        SPAN, SPR = 150, 78
        sw2_sym(s, CX, CY, sel, SPAN, SPR, live=True)

        # প্রান্তে যাওয়া তার
        s.path(f"M {CX-96} {CY} L {CX} {CY}", LIVE, SW)
        s.path(f"M {CX+SPAN} {CY-SPR} L {CX+SPAN+96} {CY-SPR}", STRAP, SW)
        s.path(f"M {CX+SPAN} {CY+SPR} L {CX+SPAN+96} {CY+SPR}", STRAP, SW)

        s.text(CX - 104, CY + 8, "COM", T_NAME, LIVE, 700, "end")
        s.text(CX + SPAN + 104, CY - SPR + 8, "L1", T_NAME, STRAP, 700)
        s.text(CX + SPAN + 104, CY + SPR + 8, "L2", T_NAME, STRAP, 700)
        s.text(px + PW / 2, 96 + PH - 34,
               "L1 চালু, L2 বিচ্ছিন্ন" if sel == "up"
               else "L2 চালু, L1 বিচ্ছিন্ন", T_NAME, col, 700, "middle")

    s.text(46 + PW / 2, 176, "চলমান পাত (ব্লেড)", T_SMALL, GREY, 400, "middle")

    # গায়ের চিহ্ন — বাজারে যেভাবে লেখা থাকে
    ty = 96 + PH + 24
    s.rect(46, ty, 1148, 150, "#F7FAFC", LINE, 1.8, 12)
    s.text(70, ty + 36, "গায়ের চিহ্ন এক রকম নয় — একই তিন প্রান্ত যেভাবে "
           "লেখা থাকতে পারে:", T_BODY, NAVY, 700)
    marks = [("COM · L1 · L2", "ইউরোপীয় ধাঁচের সুইচে"),
             ("C · 1 · 2", "ছোট মডিউলার সুইচে"),
             ("1 · 2 · 3", "সস্তা সুইচে; মাঝেরটিই কমন, এমন নয়")]
    for i, (m, note) in enumerate(marks):
        x = 90 + i * 380
        s.text(x, ty + 82, m, T_NAME, STEEL, 700)
        for j, ln in enumerate(wrap(note, 330, T_SMALL, 400)):
            s.text(x, ty + 116 + j * T_SMALL * 1.32, ln, T_SMALL, GREY, 400)

    y = note_strip(s, ty + 172,
                   "কোন প্রান্তটি কমন তা অনুমানে ধরা যাবে না — "
                   "কন্টিনিউইটি টেস্টারে যাচাই করে নিতে হবে",
                   fill=AMBERBG, stroke=AMBER, tcolor="#7A5200")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_2way_inside.svg")


def d02_symbols():
    """ওয়ান-ওয়ে, টু-ওয়ে ও ইন্টারমিডিয়েট সুইচের প্রতীক।"""
    s = SVG(1240, 640)
    s.title("তিন ধরনের সুইচ ও তাদের প্রতীক", T_TITLE)

    PW, GAP, PH = 365, 26, 400
    cases = [
        ("ওয়ান-ওয়ে সুইচ", RED, "২টি প্রান্ত",
         "এক জায়গা থেকে নিয়ন্ত্রণ", "SPST"),
        ("টু-ওয়ে সুইচ", STEEL, "৩টি প্রান্ত",
         "দুই জায়গা থেকে নিয়ন্ত্রণ", "SPDT"),
        ("ইন্টারমিডিয়েট সুইচ", GREEN, "৪টি প্রান্ত",
         "মাঝখানে বসে, জায়গা বাড়ায়", "DPDT"),
    ]
    for i, (head, col, term, use, kind) in enumerate(cases):
        px = 46 + i * (PW + GAP)
        panel(s, px, 96, PW, PH, head, col)
        cx, cy = px + PW / 2, 250
        if i == 0:
            sw1_sym(s, cx - 60, cy, False, 120)
        elif i == 1:
            sw2_sym(s, cx - 76, cy, "up", 130, 52)
        else:
            inter_sym(s, cx - 78, cy - 10, False, 156, 44)
        s.text(cx, 356, term, T_NAME, col, 700, "middle")
        s.text(cx, 394, kind, T_SMALL, GREY, 400, "middle")
        for j, ln in enumerate(wrap(use, PW - 60, T_SMALL, 400)):
            s.text(cx, 434 + j * T_SMALL * 1.34, ln, T_SMALL, "#39434D", 400,
                   "middle")

    y = note_strip(s, 96 + PH + 26,
                   "প্রতীকগুলো IEC 60617 অনুযায়ী; প্রান্তের সংখ্যা গুনেই "
                   "দোকানে সুইচ চেনা যায়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_symbols.svg")


def d03_2way_conn():
    """দুই জায়গা থেকে বাতি নিয়ন্ত্রণ — RAPTI সোর্স।"""
    return two_panel(
        "d03_2way_conn", "দুই জায়গা থেকে একটি বাতি নিয়ন্ত্রণ",
        ("সার্কিট ডায়াগ্রাম", "c17_2way_schem.png"),
        ("কানেকশন ডায়াগ্রাম", "h17_2way_conn.png"),
        "ফেজ যায় প্রথম সুইচের কমনে, দুই স্ট্র্যাপার দুই সুইচকে জোড়ে, "
        "দ্বিতীয় সুইচের কমন থেকে তার যায় বাতিতে", h=620)


def _mini_circuit(s, px, py, PW, PH, s1, s2):
    """ছোট মাপের টু-ওয়ে বর্তনী — দুই সুইচের অবস্থান দিয়ে আঁকা।"""
    MY = py + 158
    NY = py + PH - 40
    LX = px + 44
    C1, SPAN, SPR = px + 116, 74, 44
    C2 = px + 340
    LAMP = px + 468
    on = (s1 == s2)

    s.path(f"M {LX} {MY} L {C1} {MY}", LIVE, SW)
    s.text(px + 56, MY - 22, "ফেজ", T_SMALL, LIVE, 700)
    sw2_sym(s, C1, MY, s1, SPAN, SPR, live=True)

    # স্ট্র্যাপার — দুই সুইচের L1-L1 ও L2-L2 জোড়া
    for dy in (-SPR, SPR):
        s.path(f"M {C1+SPAN} {MY+dy} L {C2} {MY+dy}", STRAP, SW)
    node(s, C2, MY - SPR)
    node(s, C2, MY + SPR)

    # দ্বিতীয় সুইচ — আয়নার মতো উল্টো করে বসানো
    C2C = C2 + SPAN
    node(s, C2C, MY)
    ty = MY - SPR if s2 == "up" else MY + SPR
    s.path(f"M {C2C} {MY} L {C2+7} {ty + (7 if s2 == 'up' else -7)}", SYM,
           SW + 0.6)

    s.path(f"M {C2C} {MY} L {LAMP-28} {MY}", SYM, SW)
    lamp_sym(s, LAMP, MY, 28, on)
    s.path(f"M {LAMP+28} {MY} L {LAMP+62} {MY} L {LAMP+62} {NY} "
           f"L {LX} {NY}", NEUT, SW)
    s.text(px + 56, NY - 22, "নিউট্রাল", T_SMALL, NEUT, 700)

    s.text(C1 + 34, MY - SPR - 42, "সুইচ ১", T_SMALL, NAVY, 700, "middle")
    s.text(C2 + 34, MY - SPR - 42, "সুইচ ২", T_SMALL, NAVY, 700, "middle")
    s.text(LAMP, MY - 58, "বাতি জ্বলছে" if on else "বাতি নেভা", T_NAME,
           AMBER if on else GREY, 700, "middle")


def d04_states():
    """চারটি অবস্থান — কখন বাতি জ্বলে, কখন নেভে।"""
    s = SVG(1240, 800)
    s.title("দুই সুইচের চার অবস্থা", T_TITLE)

    PW, PH = 560, 288
    cases = [
        (46, 96, "up", "up", "দুই সুইচই L1-এ"),
        (634, 96, "down", "up", "সুইচ ১ ঘোরানো হলো"),
        (46, 406, "up", "down", "সুইচ ২ ঘোরানো হলো"),
        (634, 406, "down", "down", "দুই সুইচই L2-এ"),
    ]
    for px, py, s1, s2, head in cases:
        col = GREEN if s1 == s2 else GREY
        panel(s, px, py, PW, PH, head, col)
        _mini_circuit(s, px, py, PW, PH, s1, s2)

    y = note_strip(s, 406 + PH + 24,
                   "দুই সুইচ একই স্ট্র্যাপারে থাকলে পথ পূর্ণ হয়, আলাদা "
                   "স্ট্র্যাপারে থাকলে পথ কাটা — তাই যেকোনো সুইচেই কাজ হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_states.svg")


def d05_inter_inside():
    """ইন্টারমিডিয়েট সুইচের দুই অবস্থান।"""
    s = SVG(1240, 660)
    s.title("ইন্টারমিডিয়েট সুইচের ভেতরে", T_TITLE)

    PW, PH = 560, 400
    for px, head, crossed, col in (
            (46, "সোজা অবস্থান — যেমন এল, তেমন গেল", False, STEEL),
            (634, "আড়াআড়ি অবস্থান — দুই পথ অদলবদল", True, GREEN)):
        panel(s, px, 96, PW, PH, head, col)
        X, Y, WD, SPR = px + 130, 290, 200, 66
        inter_sym(s, X, Y, crossed, WD, SPR)
        for dy, tag in ((-SPR, "১"), (SPR, "২")):
            s.path(f"M {X-84} {Y+dy} L {X} {Y+dy}", STRAP, SW)
            s.path(f"M {X+WD} {Y+dy} L {X+WD+84} {Y+dy}", STRAP, SW)
        s.text(px + 40, Y - SPR - 24, "বাঁ ১", T_SMALL, STEEL, 700)
        s.text(px + 40, Y + SPR - 24, "বাঁ ২", T_SMALL, STEEL, 700)
        s.text(px + PW - 40, Y - SPR - 24, "ডান ১", T_SMALL, STEEL, 700, "end")
        s.text(px + PW - 40, Y + SPR - 24, "ডান ২", T_SMALL, STEEL, 700, "end")
        s.text(px + PW / 2, 96 + PH - 40,
               "বাঁ ১ → ডান ১ · বাঁ ২ → ডান ২" if not crossed
               else "বাঁ ১ → ডান ২ · বাঁ ২ → ডান ১",
               T_NAME, col, 700, "middle")

    y = note_strip(s, 96 + PH + 26,
                   "ইন্টারমিডিয়েট সুইচ কখনো বর্তনী কাটে না — কেবল দুই "
                   "স্ট্র্যাপারের পথ বদলে দেয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_inter_inside.svg")


def d06_three_place():
    """তিন জায়গা থেকে একটি বাতি নিয়ন্ত্রণ।"""
    s = SVG(1240, 700)
    s.title("তিন জায়গা থেকে একটি বাতি নিয়ন্ত্রণ", T_TITLE)

    MY, NY = 330, 540
    LX = 84
    C1, SPAN, SPR = 168, 94, 62
    IX, IW = 452, 190
    C2 = 796
    LAMP = 1010

    s.path(f"M {LX} {MY} L {C1} {MY}", LIVE, SW)
    s.text(LX - 14, MY + 8, "ফেজ", T_CALL, LIVE, 700, "end")
    sw2_sym(s, C1, MY, "up", SPAN, SPR, live=True)

    # সুইচ ১ → ইন্টারমিডিয়েট
    for dy in (-SPR, SPR):
        s.path(f"M {C1+SPAN} {MY+dy} L {IX} {MY+dy}", STRAP, SW)
    inter_sym(s, IX, MY, False, IW, SPR)

    # ইন্টারমিডিয়েট → সুইচ ২
    for dy in (-SPR, SPR):
        s.path(f"M {IX+IW} {MY+dy} L {C2} {MY+dy}", STRAP, SW)
    node(s, C2, MY - SPR)
    node(s, C2, MY + SPR)

    C2C = C2 + SPAN
    node(s, C2C, MY)
    s.path(f"M {C2C} {MY} L {C2+7} {MY-SPR+7}", SYM, SW + 0.6)

    s.path(f"M {C2C} {MY} L {LAMP-32} {MY}", SYM, SW)
    lamp_sym(s, LAMP, MY, 32, True)
    s.path(f"M {LAMP+32} {MY} L {1122} {MY} L {1122} {NY} L {LX} {NY}",
           NEUT, SW)
    s.text(LX - 14, NY + 8, "নিউট্রাল", T_CALL, NEUT, 700, "end")

    s.text(C1 + SPAN / 2, MY - SPR - 52, "টু-ওয়ে সুইচ ১", T_CALL, NAVY, 700,
           "middle")
    s.text(IX + IW / 2, MY - SPR - 76, "ইন্টারমিডিয়েট সুইচ", T_CALL, GREEN,
           700, "middle")
    s.text(C2 + SPAN / 2, MY - SPR - 52, "টু-ওয়ে সুইচ ২", T_CALL, NAVY, 700,
           "middle")
    s.text(LAMP, MY - 62, "বাতি", T_CALL, NAVY, 700, "middle")
    s.text(IX + IW / 2, MY + SPR + 96,
           "সিঁড়ির মাঝের তলায় এই সুইচটি বসে", T_SMALL, GREY, 400, "middle")

    y = note_strip(s, 592,
                   "চার জায়গা থেকে নিয়ন্ত্রণ করতে হলে আর একটি "
                   "ইন্টারমিডিয়েট সুইচ মাঝখানে যোগ করলেই হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_three_place.svg")


def d07_tunnel():
    """টানেল ওয়্যারিং — RAPTI সোর্স।"""
    return two_panel(
        "d07_tunnel", "টানেল বা গোডাউন ওয়্যারিং",
        ("সার্কিট ডায়াগ্রাম", "c18_tunnel_schem.png"),
        ("কানেকশন ডায়াগ্রাম", "h18_tunnel_conn.png"),
        "প্রতিটি টু-ওয়ে সুইচের এক প্রান্তে বাতি, অন্য প্রান্তে পরের সুইচ — "
        "তাই একবারে একটি বাতিই জ্বলে", h=640)


def d08_tunnel_seq():
    """টানেল ওয়্যারিংয়ে কোন সুইচে কোন বাতি জ্বলে।"""
    s = SVG(1240, 700)
    s.title("টানেল ওয়্যারিংয়ে বাতি জ্বলার ক্রম", T_TITLE)

    XS = [452, 636, 820, 1004]
    rows = [
        ("মেইন সুইচ অন, ২-ওয়ে ১ উপরে", 0),
        ("২-ওয়ে ১ নিচে, ২-ওয়ে ২ উপরে", 1),
        ("২-ওয়ে ২ নিচে, ২-ওয়ে ৩ উপরে", 2),
        ("২-ওয়ে ৩ নিচে", 3),
    ]

    # শিরোনামের সারি
    s.rect(46, 96, 1148, 52, NAVY, NAVY, 2, 10)
    s.text(70, 130, "সুইচের অবস্থা", T_BODY, "#FFFFFF", 700)
    for i, x in enumerate(XS):
        s.text(x, 130, f"বাতি {['১', '২', '৩', '৪'][i]}", T_BODY, "#FFFFFF",
               700, "middle")

    yy = 148
    for head, lit in rows:
        s.rect(46, yy, 1148, 108, "#F7FAFC", LINE, 1.6, 0)
        s.text(70, yy + 62, head, T_NAME, NAVY, 700)
        for i, x in enumerate(XS):
            lamp_sym(s, x, yy + 54, 30, i == lit)
        yy += 108

    y = note_strip(s, yy + 24,
                   "একজন যত এগোবে, পেছনের বাতি নিভবে আর সামনেরটি জ্বলবে — "
                   "গুদাম ও লম্বা করিডোরে এভাবেই বিদ্যুৎ বাঁচে",
                   fill=GREENBG, stroke=GREEN, tcolor="#145034")
    s.fit(y, 24)
    return s.save(f"{OUT}/d08_tunnel_seq.svg")


def d09_stair_layout():
    """সিঁড়ির বাস্তব লে-আউট ও তারের সংখ্যা।"""
    s = SVG(1240, 800)
    s.title("সিঁড়ির ওয়্যারিং — বোর্ড কোথায়, তার কয়টি", T_TITLE)

    SLAB = 330                       # দুই তলার মাঝের ছাদ
    s.rect(120, SLAB, 1000, 20, "#DDE4EB", "#A9B4C0", 2, 3)
    s.text(1110, 316, "উপরতলা", T_SMALL, GREY, 700, "end")
    s.text(1110, 386, "নিচতলা", T_SMALL, GREY, 700, "end")

    # সিঁড়ির ধাপ — নিচ থেকে উপরে
    for k in range(7):
        s.rect(620 + 34 * k, 570 - 34 * (k + 1), 34, 34, "#EEF2F6",
               "#B7C2CE", 1.8, 0)

    # ডিস্ট্রিবিউশন বোর্ড
    s.rect(120, 450, 92, 120, "#FFFFFF", NAVY, 3, 10)
    s.text(166, 520, "DB", T_CALL, NAVY, 700, "middle")

    # দুই সুইচ বোর্ড
    for bx, by, lab, col in (
            (268, 450, "নিচতলার বোর্ড — টু-ওয়ে সুইচ ১", STEEL),
            (880, 170, "উপরতলার বোর্ড — টু-ওয়ে সুইচ ২", GREEN)):
        s.rect(bx, by, 100, 120, "#FFFFFF", col, 3, 10)
        s.rect(bx + 20, by + 26, 60, 68, "#E7ECF1", "#8D9AA8", 2.2, 6)
        for j, ln in enumerate(wrap(lab, 200, T_SMALL, 700)):
            s.text(bx + 50, by - 78 + j * T_SMALL * 1.32, ln, T_SMALL, col,
                   700, "middle")

    # সিঁড়ির বাতি
    lamp_sym(s, 620, 230, 34, True)
    s.text(620, 170, "সিঁড়ির বাতি", T_CALL, NAVY, 700, "middle")

    # ফেজ — DB থেকে নিচতলার বোর্ডে
    s.path("M 212 500 L 268 500", LIVE, SW)
    s.text(240, 478, "ফেজ", T_SMALL, LIVE, 700, "middle")

    # স্ট্র্যাপার — দুই বোর্ডের মাঝে
    s.path("M 318 570 L 318 610 L 930 610 L 930 290", STRAP, SW + 1)
    s.text(620, 648, "২টি স্ট্র্যাপার তার", T_CALL, STRAP, 700, "middle")

    # সুইচ করা ফেজ — উপরতলার বোর্ড থেকে বাতিতে
    s.path("M 880 230 L 654 230", SYM, SW)
    s.text(768, 202, "সুইচ করা ফেজ — ১ তার", T_SMALL, NAVY, 700, "middle")

    # নিউট্রাল — DB থেকে সরাসরি বাতিতে, কোনো সুইচ ছোঁয় না
    s.path("M 150 450 L 150 230 L 586 230", NEUT, SW)
    s.text(300, 208, "নিউট্রাল", T_SMALL, NEUT, 700, "middle")

    y = note_strip(s, 682,
                   "দুই বোর্ডের মাঝে অন্তত ৩ তার টানতে হয় — "
                   "১টি নয়, এটাই নতুনদের সবচেয়ে বড় ভুল",
                   fill=AMBERBG, stroke=AMBER, tcolor="#7A5200")
    s.fit(y, 24)
    return s.save(f"{OUT}/d09_stair_layout.svg")


ALL = [d01_2way_inside, d02_symbols, d03_2way_conn, d04_states,
       d05_inter_inside, d06_three_place, d07_tunnel, d08_tunnel_seq,
       d09_stair_layout]

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
