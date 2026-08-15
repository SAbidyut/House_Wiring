# -*- coding: utf-8 -*-
"""অধ্যায় ৭ — ইলেকট্রিক্যাল সার্কিট: সিরিজ, প্যারালাল ও মিশ্র : ডায়াগ্রাম।

সার্কিটের ছবিগুলো RAPTI-র নিজস্ব সোর্স ফাইল (Circuit Diagram.pptx ও
HW Connection Diagram All.pptx) থেকে হুবহু বসানো — হাতে আঁকা নয়।
হিসাবের ডায়াগ্রামগুলো (রোধ, ভোল্টেজ, কারেন্ট) নতুন করে আঁকা।
"""
import os
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams", "ch07")
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "ch07")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
LH = 1.42

SYM = "#12324D"
SW = 3.2


# ── shared symbols ──────────────────────────────────────────────────────
def _dot(s, x, y, r=5.5):
    s.circle(x, y, r, SYM)


def sym_source(s, cx, cy, r=30):
    """AC source — circle with a sine wave inside."""
    s.circle(cx, cy, r, "#FFFFFF", SYM, SW)
    k = r * 0.62
    s.path(f"M {cx-k} {cy} q {k/2} {-k*1.05} {k} 0 q {k/2} {k*1.05} {k} 0",
           SYM, 2.8)


def sym_lamp(s, cx, cy, r=21):
    s.circle(cx, cy, r, "#FFFFFF", SYM, SW)
    k = r * 0.707
    s.path(f"M {cx-k} {cy-k} L {cx+k} {cy+k}", SYM, 2.4)
    s.path(f"M {cx-k} {cy+k} L {cx+k} {cy-k}", SYM, 2.4)


def sym_res(s, cx, cy, w=124, h=46):
    """Rectangular resistance/load symbol (IEC 60617)."""
    s.rect(cx - w / 2, cy - h / 2, w, h, "#FFFFFF", SYM, SW, 4)
    return cx - w / 2, cx + w / 2


def panel(s, x, y, w, h, title, col=STEEL):
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def image_panel(s, cx, top, bottom, path, half=268, pad=14):
    """RAPTI-এর নিজস্ব সোর্স ডায়াগ্রাম হুবহু বসানো — নতুন করে আঁকা নয়।"""
    s.image_fit(cx - half, top, half * 2, bottom - top, path, pad)


def _sheet(fname, title, draw_circuit, draw_conn, note, h=600,
           t_left="সার্কিট ডায়াগ্রাম", t_right="কানেকশন ডায়াগ্রাম"):
    s = SVG(1240, h)
    s.title(title, T_TITLE)
    PW = 560
    panel(s, 46, 96, PW, h - 230, t_left, STEEL)
    panel(s, 634, 96, PW, h - 230, t_right, GREEN)
    draw_circuit(s, 46 + PW / 2)
    draw_conn(s, 634 + PW / 2)
    by = h - 118
    s.rect(46, by, 1148, 58, "#EAF2FA", STEEL, 2, 11)
    s.text(620, by + 36, note, T_NAME, NAVY, 700, "middle")
    s.fit(by + 58, 22)
    return s.save(f"{OUT}/{fname}.svg")


def formula_strip(s, y, text, w=1148, x=46, fill="#FFF6E5", stroke=AMBER,
                  tcolor="#7A5200"):
    s.rect(x, y, w, 60, fill, stroke, 2, 11)
    s.text(x + w / 2, y + 38, text, T_NAME, tcolor, 700, "middle")
    return y + 60


# ═══════════════════════════════════════════════════════════════════════
def d01_classification():
    """সার্কিটের শ্রেণিবিভাগ — অবস্থা, সরবরাহ ও সংযোগ অনুসারে।"""
    s = SVG(1240, 640)
    s.title("ইলেকট্রিক্যাল সার্কিটের শ্রেণিবিভাগ", T_TITLE)

    rx, ry, rw, rh = s.box_auto(620, 84, "ইলেকট্রিক্যাল সার্কিট", T_NODE,
                                fill=NAVY, stroke=NAVY, tcolor="#FFFFFF",
                                pad_x=34, pad_y=14)
    bus = ry + rh + 34
    s.path(f"M 620 {ry+rh} L 620 {bus}", STEEL, 2.6)

    cols = [(212, "অবস্থা অনুসারে", STEEL,
             ["ওপেন সার্কিট", "ক্লোজ সার্কিট", "শর্ট সার্কিট"]),
            (620, "সরবরাহ অনুসারে", STEEL,
             ["এসি সার্কিট (AC)", "ডিসি সার্কিট (DC)"]),
            (1028, "সংযোগ অনুসারে", GREEN,
             ["সিরিজ সার্কিট", "প্যারালাল সার্কিট", "মিশ্র সার্কিট"])]

    s.path(f"M {cols[0][0]} {bus} L {cols[2][0]} {bus}", STEEL, 2.6)
    bottom = 0
    for cx, head, col, leaves in cols:
        s.path(f"M {cx} {bus} L {cx} {bus+28}", STEEL, 2.6)
        gx, gy, gw, gh = s.box_auto(cx, bus + 28, head, T_NAME, fill=col,
                                    stroke=col, tcolor="#FFFFFF",
                                    pad_x=26, pad_y=12, min_w=336)
        y = gy + gh
        for leaf in leaves:
            s.path(f"M {cx} {y} L {cx} {y+26}", LINE, 2.4)
            lx, ly, lw, lh = s.box_auto(cx, y + 26, leaf, T_BODY,
                                        fill="#F7FAFC", stroke=LINE,
                                        tcolor=INK, weight=600,
                                        pad_x=20, pad_y=13, min_w=336)
            y = ly + lh
        bottom = max(bottom, y)

    s.text(620, bottom + 44,
           "এই অধ্যায়ের মূল আলোচ্য — সংযোগ অনুসারে সার্কিটের তিন প্রকারভেদ",
           T_BODY, GREY, 400, "middle")
    s.fit(bottom + 44, 26)
    return s.save(f"{OUT}/d01_classification.svg")


def d02_current_path():
    """কারেন্টের পথ — সিরিজে একটিমাত্র পথ, প্যারালালে একাধিক পথ।"""
    s = SVG(1240, 520)
    s.title("সিরিজ ও প্যারালাল সংযোগে কারেন্টের পথ", T_TITLE)
    ar = s.arrow_defs(RED, "arc", 15)

    PW, PY, PH = 554, 96, 340
    panel(s, 46, PY, PW, PH, "সিরিজ — একটিমাত্র পথ", STEEL)
    panel(s, 640, PY, PW, PH, "প্যারালাল — একাধিক পথ", GREEN)

    # ── series loop ────────────────────────────────────────────────────
    L, R, TOP, BOT = 116, 528, 248, 400
    sx, scy = L, 324
    sym_source(s, sx, scy, 27)
    s.path(f"M {L} {TOP} L {L} {scy-27}", SYM, SW)
    s.path(f"M {L} {scy+27} L {L} {BOT}", SYM, SW)
    lamps = [214, 322, 430]
    prev = L
    for i, lx in enumerate(lamps):
        s.path(f"M {prev} {TOP} L {lx-21} {TOP}", SYM, SW)
        sym_lamp(s, lx, TOP, 21)
        s.text(lx, TOP - 42, f"লোড {['১','২','৩'][i]}", T_SMALL, NAVY, 700,
               "middle")
        prev = lx + 21
    s.path(f"M {prev} {TOP} L {R} {TOP}", SYM, SW)
    s.path(f"M {R} {TOP} L {R} {BOT}", SYM, SW)
    s.path(f"M {R} {BOT} L {L} {BOT}", RED, 3.4, marker=ar)
    s.text(322, BOT - 16, "I — সব লোডে একই কারেন্ট", T_SMALL, RED, 700,
           "middle")

    # ── parallel rails ─────────────────────────────────────────────────
    L2, R2, TR, BR = 710, 1054, 248, 400
    sym_source(s, L2, 324, 27)
    s.path(f"M {L2} {TR} L {L2} {324-27}", SYM, SW)
    s.path(f"M {L2} {324+27} L {L2} {BR}", SYM, SW)
    s.path(f"M {L2} {TR} L {R2} {TR}", SYM, SW)
    s.path(f"M {L2} {BR} L {R2} {BR}", SYM, SW)
    for i, bx in enumerate([826, 940, 1054]):
        s.path(f"M {bx} {TR} L {bx} {303}", SYM, SW)
        sym_lamp(s, bx, 324, 21)
        s.path(f"M {bx} {345} L {bx} {BR}", SYM, SW)
        _dot(s, bx, TR)
        _dot(s, bx, BR)
        s.text(bx + 34, 322, f"I{i+1}", T_SMALL, RED, 700, "start")
    s.text(768, TR - 16, "I", T_SMALL, RED, 700, "middle")
    s.path(f"M 748 {TR+22} L 790 {TR+22}", RED, 3.4, marker=ar)

    y = formula_strip(s, 466,
                      "সিরিজে কারেন্ট সমান, ভোল্টেজ ভাগ হয় — "
                      "প্যারালালে ভোল্টেজ সমান, কারেন্ট ভাগ হয়")
    s.fit(y, 22)
    return s.save(f"{OUT}/d02_current_path.svg")


def d03_simple():
    def circ(s, cx):
        image_panel(s, cx, 150, 500, f"{IMG}/d03_simple_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 500, f"{IMG}/d03_simple_conn.png")

    return _sheet("d03_simple", "সাধারণ সার্কিট — এক উৎস, এক লোড", circ, conn,
                  "উৎস → ফিউজ → সুইচ → লোড → নিউট্রাল: বর্তনী সম্পূর্ণ হলেই "
                  "বাতি জ্বলে", 660)


def d04_series():
    def circ(s, cx):
        image_panel(s, cx, 150, 440, f"{IMG}/d04_series_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 440, f"{IMG}/d04_series_conn.png")

    return _sheet("d04_series", "সিরিজ সার্কিট — দুটি বাতি একই পথে",
                  circ, conn,
                  "প্রথম বাতির শেষ প্রান্ত দ্বিতীয় বাতির শুরুতে — "
                  "একটি নষ্ট হলে দুটোই বন্ধ", 600)


def d05_parallel():
    def circ(s, cx):
        image_panel(s, cx, 150, 440, f"{IMG}/d05_parallel_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 440, f"{IMG}/d05_parallel_conn.png")

    return _sheet("d05_parallel", "প্যারালাল সার্কিট — প্রতিটি বাতির নিজস্ব পথ",
                  circ, conn,
                  "প্রতিটি শাখা আলাদা সুইচসহ ফেজ ও নিউট্রালের মাঝে — "
                  "প্রত্যেকে পূর্ণ ভোল্টেজ পায়", 600)


def d06_mixed():
    def circ(s, cx):
        image_panel(s, cx, 150, 400, f"{IMG}/d06_mixed_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 400, f"{IMG}/d06_mixed_conn.png")

    return _sheet("d06_mixed", "মিশ্র সার্কিট — সিরিজ ও প্যারালাল একসঙ্গে",
                  circ, conn,
                  "বাতি ১ ও বাতি ২ প্যারালালে; বাতি ৩ ও বাতি ৪ নিজেদের মধ্যে "
                  "সিরিজে থেকে ওই দুটির সঙ্গে প্যারালালে", 560)


def d07_series_calc():
    """সিরিজ সার্কিটের রোধ, কারেন্ট ও ভোল্টেজের হিসাব।"""
    s = SVG(1240, 520)
    s.title("সিরিজ সার্কিটে রোধ ও ভোল্টেজের হিসাব", T_TITLE)
    ar = s.arrow_defs(RED, "ars", 15)

    L, R, TOP, BOT = 168, 1072, 190, 400
    scy = 300
    sym_source(s, L, scy, 30)
    s.path(f"M {L} {TOP} L {L} {scy-30}", SYM, SW)
    s.path(f"M {L} {scy+30} L {L} {BOT}", SYM, SW)
    s.text(L - 46, scy + 8, "V = 230 V", T_BODY, NAVY, 700, "end")

    boxes = [(398, "R1 = 100 Ω", "V1"), (620, "R2 = 200 Ω", "V2"),
             (842, "R3 = 160 Ω", "V3")]
    prev = L
    for cx, rlab, vlab in boxes:
        s.path(f"M {prev} {TOP} L {cx-62} {TOP}", SYM, SW)
        x0, x1 = sym_res(s, cx, TOP)
        s.text(cx, TOP - 48, rlab, T_BODY, NAVY, 700, "middle")
        s.text(cx, TOP + 66, vlab, T_BODY, RED, 700, "middle")
        prev = x1
    s.path(f"M {prev} {TOP} L {R} {TOP}", SYM, SW)
    s.path(f"M {R} {TOP} L {R} {BOT}", SYM, SW)
    s.path(f"M {R} {BOT} L {L} {BOT}", RED, 3.4, marker=ar)
    s.text(620, BOT - 18, "I — প্রতিটি রোধে একই মানের কারেন্ট", T_BODY, RED,
           700, "middle")

    y = formula_strip(s, 438,
                      "RT = R1 + R2 + R3    এবং    V = V1 + V2 + V3    "
                      "(কারেন্ট I সব রোধে সমান)")
    s.fit(y, 22)
    return s.save(f"{OUT}/d07_series_calc.svg")


def d08_parallel_calc():
    """প্যারালাল সার্কিটের রোধ ও কারেন্টের হিসাব।"""
    s = SVG(1240, 520)
    s.title("প্যারালাল সার্কিটে রোধ ও কারেন্টের হিসাব", T_TITLE)
    ar = s.arrow_defs(RED, "arp", 15)

    L, R, TR, BR = 210, 922, 176, 400
    scy = 288
    sym_source(s, L, scy, 30)
    s.path(f"M {L} {TR} L {L} {scy-30}", SYM, SW)
    s.path(f"M {L} {scy+30} L {L} {BR}", SYM, SW)
    s.text(L - 46, scy + 8, "V = 230 V", T_BODY, NAVY, 700, "end")
    s.path(f"M {L} {TR} L {R} {TR}", SYM, SW)
    s.path(f"M {L} {BR} L {R} {BR}", SYM, SW)

    for bx, rlab, ilab in [(478, "R1 = 460 Ω", "I1"), (700, "R2 = 920 Ω", "I2"),
                           (922, "R3 = 920 Ω", "I3")]:
        s.path(f"M {bx} {TR} L {bx} {265}", SYM, SW)
        sym_res(s, bx, 288, 46, 124)
        s.path(f"M {bx} {350} L {bx} {BR}", SYM, SW)
        _dot(s, bx, TR)
        _dot(s, bx, BR)
        s.text(bx + 44, 268, rlab, T_BODY, NAVY, 700, "start")
        s.text(bx + 44, 322, ilab, T_BODY, RED, 700, "start")

    s.path(f"M {L+46} {TR-22} L {L+146} {TR-22}", RED, 3.4, marker=ar)
    s.text(L + 96, TR - 34, "I", T_BODY, RED, 700, "middle")
    s.text(566, BR + 40, "প্রতিটি রোধের দুই প্রান্তেই উৎসের পূর্ণ ভোল্টেজ",
           T_BODY, GREY, 400, "middle")

    y = formula_strip(s, 476,
                      "1/RT = 1/R1 + 1/R2 + 1/R3    এবং    I = I1 + I2 + I3    "
                      "(ভোল্টেজ V সব শাখায় সমান)")
    s.fit(y, 22)
    return s.save(f"{OUT}/d08_parallel_calc.svg")


def d09_mixed_calc():
    """মিশ্র সার্কিট — R1 সিরিজে, তার পরে R2 ও R3 প্যারালালে।"""
    s = SVG(1240, 520)
    s.title("মিশ্র সার্কিটের হিসাব — R1 সিরিজে, R2 ও R3 প্যারালালে", T_TITLE)

    L, R, TOP, BOT = 190, 1082, 186, 420
    scy = 300
    sym_source(s, L, scy, 30)
    s.path(f"M {L} {TOP} L {L} {scy-30}", SYM, SW)
    s.path(f"M {L} {scy+30} L {L} {BOT}", SYM, SW)
    s.text(L - 46, scy + 8, "V = 230 V", T_BODY, NAVY, 700, "end")

    # R1 — সিরিজ অংশ
    s.path(f"M {L} {TOP} L {330-62} {TOP}", SYM, SW)
    sym_res(s, 330, TOP)
    s.text(330, TOP - 48, "R1 = 30 Ω", T_BODY, NAVY, 700, "middle")

    A, B = 520, 900          # প্যারালাল অংশের দুই নোড
    LOW = 330                # নিচের শাখার উচ্চতা
    s.path(f"M {330+62} {TOP} L {A} {TOP}", SYM, SW)
    _dot(s, A, TOP)
    s.path(f"M {A} {TOP} L {A} {LOW}", SYM, SW)

    # উপরের শাখা — R2
    s.path(f"M {A} {TOP} L {710-62} {TOP}", SYM, SW)
    sym_res(s, 710, TOP)
    s.text(710, TOP - 48, "R2 = 250 Ω", T_BODY, NAVY, 700, "middle")
    s.path(f"M {710+62} {TOP} L {B} {TOP}", SYM, SW)

    # নিচের শাখা — R3
    s.path(f"M {A} {LOW} L {710-62} {LOW}", SYM, SW)
    sym_res(s, 710, LOW)
    s.text(710, LOW + 66, "R3 = 1000 Ω", T_BODY, NAVY, 700, "middle")
    s.path(f"M {710+62} {LOW} L {B} {LOW}", SYM, SW)
    s.path(f"M {B} {LOW} L {B} {TOP}", SYM, SW)
    _dot(s, B, TOP)

    s.text(A - 18, TOP - 20, "A", T_BODY, RED, 700, "end")
    s.text(B + 18, TOP - 20, "B", T_BODY, RED, 700, "start")

    s.path(f"M {B} {TOP} L {R} {TOP}", SYM, SW)
    s.path(f"M {R} {TOP} L {R} {BOT}", SYM, SW)
    s.path(f"M {R} {BOT} L {L} {BOT}", SYM, SW)

    y = formula_strip(s, 452,
                      "RP = (R2 × R3) / (R2 + R3)    এবং    RT = R1 + RP")
    s.fit(y, 22)
    return s.save(f"{OUT}/d09_mixed_calc.svg")


def d10_meters():
    def amm(s, cx):
        image_panel(s, cx, 150, 440, f"{IMG}/d10_ammeter.png")

    def volt(s, cx):
        image_panel(s, cx, 150, 440, f"{IMG}/d10_voltmeter.png")

    return _sheet("d10_meters", "অ্যামিটার ও ভোল্টমিটারের সংযোগ পদ্ধতি",
                  amm, volt,
                  "অ্যামিটার সবসময় লোডের সঙ্গে সিরিজে, ভোল্টমিটার সবসময় "
                  "লোডের সঙ্গে প্যারালালে", 600,
                  t_left="অ্যামিটার — সিরিজে", t_right="ভোল্টমিটার — প্যারালালে")


ALL = [d01_classification, d02_current_path, d03_simple, d04_series,
       d05_parallel, d06_mixed, d07_series_calc, d08_parallel_calc,
       d09_mixed_calc, d10_meters]

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
