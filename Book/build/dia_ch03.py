# -*- coding: utf-8 -*-
"""অধ্যায় ৩ — বেসিক ইলেকট্রিক্যাল সার্কিট : ডায়াগ্রাম।

Each of the five practice circuits is drawn twice — once as a symbol circuit
diagram and once as a pictorial connection diagram with the real conductor
colours — because that is how the workshop teaches them.
"""
import os, math
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams", "ch03")
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "ch03")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
LH = 1.42

SYM = "#12324D"          # symbol ink
SW = 3.2
BROWN = "#7A4A21"        # line / phase   (IEC 60445)
BLUE = "#1E63B5"         # neutral
EGREEN = "#2E8B31"       # earth (green-yellow)
EYELLOW = "#F2D200"


def bullet_panel(s, x, y, w, items, size=T_BODY, fill="#F7FAFC", stroke=LINE,
                 tcolor=INK, bullet_color=STEEL, pad=20, lh=LH, gap=10):
    inner = w - 2 * pad - size * 1.15
    rows = [wrap(it, inner, size, 400) for it in items]
    h = pad * 2 + sum(len(r) * size * lh for r in rows) + gap * (len(rows) - 1)
    s.rect(x, y, w, h, fill, stroke, 1.8, 12)
    yy = y + pad
    for ln_set in rows:
        base = yy + size * 0.82
        s.circle(x + pad + size * 0.22, base - size * 0.30, size * 0.19, bullet_color)
        for i, ln in enumerate(ln_set):
            s.text(x + pad + size * 1.15, base + i * size * lh, ln, size, tcolor, 400)
        yy += len(ln_set) * size * lh + gap
    return y + h


# ── symbol primitives ───────────────────────────────────────────────────
def _dot(s, x, y, r=5):
    s.circle(x, y, r, SYM)


def sym_lamp(s, cx, cy, r=24):
    s.circle(cx, cy, r, "#FFFFFF", SYM, SW)
    k = r * 0.707
    s.path(f"M {cx-k} {cy-k} L {cx+k} {cy+k}", SYM, 2.4)
    s.path(f"M {cx-k} {cy+k} L {cx+k} {cy-k}", SYM, 2.4)


def sym_switch(s, cx, cy, gap=26):
    _dot(s, cx - gap, cy); _dot(s, cx + gap, cy)
    s.path(f"M {cx-gap} {cy} L {cx+gap-6} {cy-26}", SYM, SW)


def sym_socket(s, cx, cy, pins=2, r=26):
    s.path(f"M {cx-r} {cy} A {r} {r} 0 0 1 {cx+r} {cy}", SYM, SW)
    s.path(f"M {cx-r} {cy} L {cx+r} {cy}", SYM, SW)
    step = (2 * r - 16) / (pins + 1)
    for i in range(pins):
        px = cx - r + 8 + step * (i + 1)
        s.path(f"M {px} {cy} L {px} {cy-16}", SYM, 2.6)


def sym_earth(s, cx, cy):
    s.path(f"M {cx} {cy-16} L {cx} {cy}", SYM, SW)
    for i, w_ in enumerate((34, 22, 11)):
        s.path(f"M {cx-w_/2} {cy+i*9} L {cx+w_/2} {cy+i*9}", SYM, SW)


def sym_plug(s, cx, cy, pins=2):
    s.rect(cx - 26, cy - 22, 40, 44, "#FFFFFF", SYM, SW, 6)
    ys = (cy - 10, cy + 10) if pins == 2 else (cy - 14, cy, cy + 14)
    for yy in ys:
        s.path(f"M {cx+14} {yy} L {cx+34} {yy}", SYM, 2.8)


# ── pictorial primitives (connection diagrams) ──────────────────────────
def rails(s, x1, x2, y, has_earth=False):
    """Supply rails with IEC conductor colours."""
    s.path(f"M {x1} {y} L {x2} {y}", BROWN, 5)
    s.text(x1 - 12, y + 7, "L", T_SMALL, BROWN, 700, "end")
    s.path(f"M {x1} {y+34} L {x2} {y+34}", BLUE, 5)
    s.text(x1 - 12, y + 41, "N", T_SMALL, BLUE, 700, "end")
    if has_earth:
        s.path(f"M {x1} {y+68} L {x2} {y+68}", EGREEN, 5)
        s.text(x1 - 12, y + 75, "E", T_SMALL, EGREEN, 700, "end")
    return y, y + 34, y + 68


def pic_holder(s, cx, cy):
    """Batten holder with a lamp."""
    s.rect(cx - 26, cy - 16, 52, 26, "#E4E9ED", "#7C8794", 2, 5)
    s.path(f"M {cx-16} {cy+10} L {cx+16} {cy+10} L {cx+12} {cy+22} "
           f"L {cx-12} {cy+22} Z", "#8D9AA8", 2, "#B7C1CB")
    s.circle(cx, cy + 46, 24, "#FFF3C4", "#B08C00", 2.4)
    s.path(f"M {cx-11} {cy+52} q 11 -20 22 0", "#B08C00", 2.4)
    return (cx - 16, cy - 16), (cx + 16, cy - 16)      # two terminals


def pic_switch(s, cx, cy):
    s.rect(cx - 32, cy - 26, 64, 52, "#FFFFFF", "#7C8794", 2.4, 6)
    s.rect(cx - 14, cy - 14, 28, 28, "#DCE6EC", "#8D9AA8", 2, 4)
    return (cx - 32, cy), (cx + 32, cy)


def pic_socket(s, cx, cy, pins=2):
    s.rect(cx - 36, cy - 30, 72, 60, "#FFFFFF", "#7C8794", 2.4, 8)
    if pins == 2:
        for dx in (-13, 13):
            s.rect(cx + dx - 4, cy - 12, 8, 22, "#2B2B2B", "none", 0, 2)
    else:
        for dx in (-15, 15):
            s.rect(cx + dx - 4, cy - 4, 8, 22, "#2B2B2B", "none", 0, 2)
        s.rect(cx - 5, cy - 26, 10, 20, "#2B2B2B", "none", 0, 2)
    return cx, cy


def image_panel(s, cx, top, bottom, path, half=268, pad=14):
    """RAPTI-এর নিজস্ব সোর্স ডায়াগ্রাম হুবহু বসানো — নতুন করে আঁকা নয়।"""
    s.image_fit(cx - half, top, half * 2, bottom - top, path, pad)


def panel(s, x, y, w, h, title, col=STEEL):
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)



def plug_supply(s, x, cy, ytop, ybot, pins=2):
    """Plug at the supply end; its pins run to the top and bottom conductors."""
    s.rect(x - 44, cy - 26, 44, 52, "#FFFFFF", SYM, SW, 6)
    if pins == 2:
        ys = (cy - 12, cy + 12)
    else:
        ys = (cy - 16, cy + 16, cy)
    for yy in ys[:2]:
        s.path(f"M {x} {yy} L {x+18} {yy}", SYM, 2.8)
    s.path(f"M {x+18} {ys[0]} L {x+18} {ytop}", SYM, SW)
    s.path(f"M {x+18} {ys[1]} L {x+18} {ybot}", SYM, SW)
    return x + 18


# ═══════════════════════════════════════════════════════════════════════
def d01_circuit_parts():
    s = SVG(1240, 620)
    s.title("একটি আদর্শ বৈদ্যুতিক বর্তনীর উপাদান", T_TITLE)
    L, R_, T, B = 250, 900, 210, 430
    cx = (L + R_) / 2
    s.path(f"M {L} {T} L {cx-26} {T}", SYM, SW)
    s.path(f"M {cx+26} {T} L {R_} {T}", SYM, SW)
    s.path(f"M {R_} {T} L {R_} {B-24}", SYM, SW)
    s.path(f"M {R_} {B+24} L {R_} {B}", SYM, SW) if False else None
    s.path(f"M {R_} {320-24+48} L {R_} {B}", SYM, SW)
    s.path(f"M {R_} {B} L {L} {B}", SYM, SW)
    s.path(f"M {L} {B} L {L} {340}", SYM, SW)
    s.path(f"M {L} {300} L {L} {T}", SYM, SW)
    sym_switch(s, cx, T)
    sym_lamp(s, R_, 320)
    for dy, ww in ((-20, 34), (-7, 18), (7, 34), (20, 18)):
        s.path(f"M {L-ww/2} {320+dy} L {L+ww/2} {320+dy}", SYM, 3.4)

    labels = [("উৎস (Source)", "বিদ্যুৎ সরবরাহ করে", L, 320, "end", -60),
              ("সুইচ (Control)", "বর্তনী চালু-বন্ধ করে", cx, T, "middle", -70),
              ("লোড (Load)", "বিদ্যুৎ ব্যবহার করে", R_, 320, "start", 60),
              ("পরিবাহী (Conductor)", "বিদ্যুৎ বহন করে", cx, B, "middle", 44)]
    for name, sub, px, py, anc, off in labels:
        if anc == "middle":
            tx, ty = px, py + off
        else:
            tx, ty = px + off, py
        s.text(tx, ty, name, T_BODY, NAVY, 700, anc)
        s.text(tx, ty + 26, sub, T_SMALL, GREY, 400, anc)

    s.rect(60, 500, 1120, 62, "#EAF2FA", STEEL, 2, 11)
    s.text(620, 528, "চারটি উপাদানের যেকোনো একটি না থাকলে বর্তনী অসম্পূর্ণ",
           T_NAME, NAVY, 700, "middle")
    s.text(620, 554, "উৎস → পরিবাহী → সুইচ → লোড → আবার উৎসে ফিরে আসা",
           T_SMALL, GREY, 400, "middle")
    s.fit(562, 22)
    return s.save(f"{OUT}/d01_circuit_parts.svg")


def d02_circuit_states():
    s = SVG(1240, 600)
    s.title("বর্তনীর তিন অবস্থা", T_TITLE)
    pw, gapx = 372, 34
    x0 = (1240 - (3 * pw + 2 * gapx)) / 2
    states = [
        ("ক্লোজ সার্কিট", GREEN, "সুইচ বন্ধ — বর্তনী সম্পূর্ণ, বাতি জ্বলে", "close"),
        ("ওপেন সার্কিট", AMBER, "সুইচ খোলা বা তার ছেঁড়া — কারেন্ট চলে না", "open"),
        ("শর্ট সার্কিট", RED, "লোড বাদ দিয়ে দুই তার লেগে যাওয়া — বিপজ্জনক", "short"),
    ]
    for i, (name, col, note, kind) in enumerate(states):
        x = x0 + i * (pw + gapx)
        panel(s, x, 96, pw, 330, name, col)
        cx = x + pw / 2
        L, R_, T, B = cx - 118, cx + 118, 200, 340
        if kind == "short":
            s.path(f"M {L} {T} L {R_} {T}", SYM, SW)
            s.path(f"M {R_} {T} L {R_} {B}", SYM, SW)
            s.path(f"M {R_} {B} L {L} {B}", SYM, SW)
            s.path(f"M {L} {B} L {L} {T}", SYM, SW)
            s.path(f"M {cx-40} {T} L {cx-40} {B}", RED, 4.4)
            s.text(cx - 40, (T + B) / 2 + 8, "শর্ট পথ", T_SMALL, RED, 700, "end")
            sym_lamp(s, R_, (T + B) / 2, 20)
        else:
            s.path(f"M {L} {T} L {cx-26} {T}", SYM, SW)
            s.path(f"M {cx+26} {T} L {R_} {T}", SYM, SW)
            s.path(f"M {R_} {T} L {R_} {(T+B)/2-20}", SYM, SW)
            s.path(f"M {R_} {(T+B)/2+20} L {R_} {B}", SYM, SW)
            s.path(f"M {R_} {B} L {L} {B}", SYM, SW)
            s.path(f"M {L} {B} L {L} {T}", SYM, SW)
            _dot(s, cx - 26, T); _dot(s, cx + 26, T)
            if kind == "close":
                s.path(f"M {cx-26} {T} Q {cx} {T-16} {cx+26} {T}", NAVY, SW + 1.4)
                s.circle(R_, (T + B) / 2, 20, "#FFF3C4", "#B08C00", 3)
                for a in range(0, 360, 45):
                    r = math.radians(a)
                    s.path(f"M {R_+26*math.cos(r):.1f} {(T+B)/2+26*math.sin(r):.1f} "
                           f"L {R_+36*math.cos(r):.1f} {(T+B)/2+36*math.sin(r):.1f}",
                           "#E8A33D", 3)
            else:
                s.path(f"M {cx-26} {T} L {cx+20} {T-26}", SYM, SW)
                sym_lamp(s, R_, (T + B) / 2, 20)
        for j, ln in enumerate(wrap(note, pw - 48, T_SMALL, 400)):
            s.text(cx, 386 + j * T_SMALL * 1.34, ln, T_SMALL, "#39434D", 400, "middle")
    s.rect(60, 452, 1120, 62, REDBG, RED, 2, 11)
    s.text(620, 480, "শর্ট সার্কিটে রোধ প্রায় শূন্য হয়ে কারেন্ট বহুগুণ বেড়ে যায়",
           T_NAME, "#7A1810", 700, "middle")
    s.text(620, 506, "ফলে তার গরম হয়ে পুড়ে যায় — এ কারণেই ফিউজ ও ব্রেকার লাগে",
           T_SMALL, "#7A1810", 400, "middle")
    s.fit(514, 22)
    return s.save(f"{OUT}/d02_circuit_states.svg")


def d03_holders():
    s = SVG(1240, 560)
    s.title("হোল্ডার ও ল্যাম্পের প্রকারভেদ", T_TITLE)
    items = [
        ("ব্যাটেন হোল্ডার", "সোজা ছাদ বা বোর্ডে বসে", "batten"),
        ("অ্যাঙ্গেল হোল্ডার", "দেয়ালে কোণ করে বসে", "angle"),
        ("পেন্ডেন্ট হোল্ডার", "সিলিং রোজ থেকে ঝোলে", "pendant"),
        ("স্ক্রু (ES) হোল্ডার", "প্যাঁচ কেটে বাতি বসে", "screw"),
    ]
    cw, gapx = 272, 24
    x0 = (1240 - (4 * cw + 3 * gapx)) / 2
    for i, (name, note, kind) in enumerate(items):
        x = x0 + i * (cw + gapx)
        s.rect(x, 96, cw, 300, "#FCFDFE", LINE, 1.8, 13)
        cx, cy = x + cw / 2, 190
        if kind == "pendant":
            s.rect(cx - 24, cy - 66, 48, 18, "#B7C1CB", "#7C8794", 2, 4)
            s.path(f"M {cx} {cy-48} L {cx} {cy-18}", "#39434D", 3)
        if kind == "angle":
            s.rect(cx - 30, cy - 40, 60, 16, "#B7C1CB", "#7C8794", 2, 4)
            s.path(f"M {cx} {cy-24} L {cx+16} {cy-8}", "#8D9AA8", 8)
        s.rect(cx - 24, cy - 16, 48, 26, "#E4E9ED", "#7C8794", 2.2, 5)
        if kind == "screw":
            for k in range(3):
                s.path(f"M {cx-14} {cy+12+k*6} L {cx+14} {cy+14+k*6}", "#8D9AA8", 3)
        else:
            s.path(f"M {cx-15} {cy+10} L {cx+15} {cy+10} L {cx+11} {cy+22} "
                   f"L {cx-11} {cy+22} Z", "#8D9AA8", 2, "#B7C1CB")
        s.circle(cx, cy + 52, 26, "#FFF3C4", "#B08C00", 2.4)
        s.path(f"M {cx-12} {cy+58} q 12 -22 24 0", "#B08C00", 2.4)
        s.text(cx, 320, name, T_BODY, NAVY, 700, "middle")
        for j, ln in enumerate(wrap(note, cw - 40, T_SMALL, 400)):
            s.text(cx, 352 + j * T_SMALL * 1.32, ln, T_SMALL, GREY, 400, "middle")
    s.text(620, 442, "হোল্ডারের দুটি টার্মিনালের একটিতে ফেজ, অন্যটিতে নিউট্রাল যায়",
           T_SMALL, GREY, 400, "middle")
    s.fit(442, 24)
    return s.save(f"{OUT}/d03_holders.svg")


def d04_plug_socket():
    s = SVG(1240, 640)
    s.title("প্লাগ ও সকেট — ২-পিন ও ৩-পিন", T_TITLE)
    for i, (title, pins, col) in enumerate((("২-পিন", 2, STEEL), ("৩-পিন", 3, GREEN))):
        x = 70 + i * 570
        panel(s, x, 96, 530, 330, title + " প্লাগ ও সকেট", col)
        cx = x + 150
        s.rect(cx - 44, 210, 88, 96, "#FFFFFF", "#7C8794", 2.6, 8)
        if pins == 2:
            for dx in (-16, 16):
                s.rect(cx + dx - 6, 178, 12, 34, "#B8B8B8", "#7C7C7C", 2, 3)
        else:
            for dx in (-20, 20):
                s.rect(cx + dx - 6, 184, 12, 28, "#B8B8B8", "#7C7C7C", 2, 3)
            s.rect(cx - 7, 166, 14, 46, "#B8B8B8", "#7C7C7C", 2, 3)
            s.text(cx + 58, 178, "আর্থ পিন", T_SMALL, EGREEN, 700, "start")
        s.text(cx, 336, "প্লাগ", T_BODY, NAVY, 700, "middle")

        sx = x + 380
        pic_socket(s, sx, 250, pins)
        s.text(sx, 336, "সকেট", T_BODY, NAVY, 700, "middle")

    s.rect(70, 452, 1100, 130, "#FFF6E5", AMBER, 2, 12)
    s.text(620, 488, "৩-পিন প্লাগের আর্থ পিন লম্বা ও মোটা কেন?",
           T_NAME, "#7A5200", 700, "middle")
    for j, ln in enumerate([
            "লম্বা — প্লাগ লাগানোর সময় আর্থ সংযোগ সবার আগে হয়, খোলার সময় সবার শেষে ছোটে;",
            "মোটা — ২-পিন প্লাগ যেন ভুল করে আর্থ ছিদ্রে ঢুকে না যায়, আর ফল্ট কারেন্ট বইতে পারে।"]):
        s.text(620, 522 + j * 28, ln, T_SMALL, "#7A5200", 400, "middle")
    s.fit(582, 22)
    return s.save(f"{OUT}/d04_plug_socket.svg")


# ── the five practice circuits ──────────────────────────────────────────
def _circuit_sheet(fname, title, draw_circuit, draw_conn, note, h=560):
    s = SVG(1240, h)
    s.title(title, T_TITLE)
    PW = 560
    panel(s, 46, 96, PW, h - 230, "সার্কিট ডায়াগ্রাম", STEEL)
    panel(s, 634, 96, PW, h - 230, "কানেকশন ডায়াগ্রাম", GREEN)
    draw_circuit(s, 46 + PW / 2)
    draw_conn(s, 634 + PW / 2)
    by = h - 118
    s.rect(46, by, 1148, 58, "#EAF2FA", STEEL, 2, 11)
    s.text(620, by + 36, note, T_NAME, NAVY, 700, "middle")
    s.fit(by + 58, 22)
    return s.save(f"{OUT}/{fname}.svg")


def _conn_head(s, cx, earth=False):
    """L/N(/E) rails across a connection panel; returns their y positions."""
    return rails(s, cx - 210, cx + 210, 190, earth)


def d05_circuit1():
    def circ(s, cx):
        image_panel(s, cx, 150, 406, f"{IMG}/d05_circuit1_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 406, f"{IMG}/d05_circuit1_conn.png")

    return _circuit_sheet(
        "d05_circuit1", "সার্কিট ১ — ২-পিন প্লাগ দিয়ে বাতি সংযোগ", circ, conn,
        "সুইচ নেই — প্লাগ লাগালেই বাতি জ্বলে, খুললেই নেভে")


def d06_circuit2():
    def circ(s, cx):
        image_panel(s, cx, 150, 406, f"{IMG}/d06_circuit2_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 406, f"{IMG}/d06_circuit2_conn.png")

    return _circuit_sheet(
        "d06_circuit2", "সার্কিট ২ — সুইচ দিয়ে একটি বাতি নিয়ন্ত্রণ", circ, conn,
        "সুইচ সব সময় ফেজ (বাদামি) তারে বসাতে হয় — নিউট্রালে নয়")


def d07_circuit3():
    def circ(s, cx):
        image_panel(s, cx, 150, 426, f"{IMG}/d07_circuit3_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 426, f"{IMG}/d07_circuit3_conn.png")

    return _circuit_sheet(
        "d07_circuit3", "সার্কিট ৩ — ২-পিন সকেট সংযোগ", circ, conn,
        "সকেটের দুই টার্মিনালে সরাসরি ফেজ ও নিউট্রাল যায়", 580)


def d08_circuit4():
    def circ(s, cx):
        image_panel(s, cx, 150, 426, f"{IMG}/d08_circuit4_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 426, f"{IMG}/d08_circuit4_conn.png")

    return _circuit_sheet(
        "d08_circuit4", "সার্কিট ৪ — সুইচ দিয়ে সকেট নিয়ন্ত্রণ", circ, conn,
        "সুইচ ফেজ তারে বসে; নিউট্রাল সরাসরি সকেটে যায়", 580)


def d09_circuit5():
    def circ(s, cx):
        image_panel(s, cx, 150, 486, f"{IMG}/d09_circuit5_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 486, f"{IMG}/d09_circuit5_conn.png")

    return _circuit_sheet(
        "d09_circuit5", "সার্কিট ৫ — ৩-পিন সকেট সংযোগ (আর্থসহ)", circ, conn,
        "ধাতব বডির যন্ত্রের জন্য আর্থ সংযোগ বাধ্যতামূলক", 640)


ALL = [d01_circuit_parts, d02_circuit_states, d03_holders, d04_plug_socket,
       d05_circuit1, d06_circuit2, d07_circuit3, d08_circuit4, d09_circuit5]

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
