# -*- coding: utf-8 -*-
"""অধ্যায় ৫ — পদার্থের প্রকারভেদ ও ইলেকট্রিক্যাল প্রতীক : ডায়াগ্রাম।

The symbol sheets are the heart of this chapter, so every symbol is drawn to
IEC 60617 shape rather than pasted as a picture — that keeps line weights,
sizes and labels identical across all four sheets.
"""
import os, math
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams", "ch05")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
LH = 1.42
SYM = "#12324D"          # symbol ink — heavier than body text


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


# ═══════════════════════════════════════════════════════════════════════
#  Symbol library — each draws inside a cell centred on (cx, cy)
# ═══════════════════════════════════════════════════════════════════════
SW = 3.4                 # symbol stroke width


def _lead(s, x1, y, x2):
    s.path(f"M {x1:.1f} {y:.1f} L {x2:.1f} {y:.1f}", SYM, SW)


def _dot(s, x, y, r=5):
    s.circle(x, y, r, SYM)


def sym_spst(s, cx, cy):
    _lead(s, cx - 62, cy, cx - 26); _lead(s, cx + 26, cy, cx + 62)
    _dot(s, cx - 26, cy); _dot(s, cx + 26, cy)
    s.path(f"M {cx-26} {cy} L {cx+22} {cy-30}", SYM, SW)


def sym_spdt(s, cx, cy):
    _lead(s, cx - 62, cy, cx - 26)
    _dot(s, cx - 26, cy)
    _dot(s, cx + 26, cy - 22); _dot(s, cx + 26, cy + 22)
    _lead(s, cx + 26, cy - 22, cx + 62); _lead(s, cx + 26, cy + 22, cx + 62)
    s.path(f"M {cx-26} {cy} L {cx+22} {cy-22}", SYM, SW)


def sym_intermediate(s, cx, cy):
    s.rect(cx - 26, cy - 26, 52, 52, "none", SYM, SW, 3)
    s.path(f"M {cx-26} {cy-14} L {cx+26} {cy+14}", SYM, 2.6)
    s.path(f"M {cx-26} {cy+14} L {cx+26} {cy-14}", SYM, 2.6)
    _lead(s, cx - 64, cy - 14, cx - 26); _lead(s, cx - 64, cy + 14, cx - 26)
    _lead(s, cx + 26, cy - 14, cx + 64); _lead(s, cx + 26, cy + 14, cx + 64)


def sym_push(s, cx, cy):
    _lead(s, cx - 62, cy, cx - 26); _lead(s, cx + 26, cy, cx + 62)
    _dot(s, cx - 26, cy); _dot(s, cx + 26, cy)
    s.path(f"M {cx-30} {cy-18} L {cx+30} {cy-18}", SYM, SW)
    s.path(f"M {cx} {cy-18} L {cx} {cy-40}", SYM, SW)
    s.path(f"M {cx-14} {cy-40} L {cx+14} {cy-40}", SYM, SW)


def sym_main_switch(s, cx, cy):
    s.rect(cx - 34, cy - 30, 68, 60, "none", SYM, SW, 4)
    s.path(f"M {cx-16} {cy+16} L {cx+16} {cy-16}", SYM, SW)
    _dot(s, cx - 16, cy + 16); _dot(s, cx + 16, cy - 16)
    _lead(s, cx - 64, cy, cx - 34); _lead(s, cx + 34, cy, cx + 64)


def sym_earthing(s, cx, cy):
    s.path(f"M {cx} {cy-38} L {cx} {cy-4}", SYM, SW)
    for i, w_ in enumerate((56, 36, 18)):
        s.path(f"M {cx-w_/2} {cy-4+i*13} L {cx+w_/2} {cy-4+i*13}", SYM, SW)


def sym_earth_electrode(s, cx, cy):
    s.path(f"M {cx} {cy-40} L {cx} {cy+8}", SYM, SW)
    s.poly([(cx - 22, cy + 8), (cx + 22, cy + 8), (cx, cy + 40)], "none", SYM, SW)


def sym_fuse(s, cx, cy):
    s.rect(cx - 34, cy - 15, 68, 30, "none", SYM, SW, 2)
    s.path(f"M {cx-34} {cy} L {cx+34} {cy}", SYM, 2.4)
    _lead(s, cx - 64, cy, cx - 34); _lead(s, cx + 34, cy, cx + 64)


def sym_lamp(s, cx, cy):
    s.circle(cx, cy, 26, "none", SYM, SW)
    k = 26 * 0.707
    s.path(f"M {cx-k} {cy-k} L {cx+k} {cy+k}", SYM, 2.6)
    s.path(f"M {cx-k} {cy+k} L {cx+k} {cy-k}", SYM, 2.6)
    _lead(s, cx - 64, cy, cx - 26); _lead(s, cx + 26, cy, cx + 64)


def sym_tube(s, cx, cy):
    s.rect(cx - 52, cy - 13, 104, 26, "none", SYM, SW, 3)
    s.path(f"M {cx-52} {cy-13} L {cx-52} {cy+13}", SYM, SW)
    s.path(f"M {cx+52} {cy-13} L {cx+52} {cy+13}", SYM, SW)
    _lead(s, cx - 68, cy, cx - 52); _lead(s, cx + 52, cy, cx + 68)


def _coil(s, cx, cy, n=4, r=13, up=True):
    d = ""
    x0 = cx - n * r
    for i in range(n):
        a = x0 + i * 2 * r
        d += f"M {a} {cy} A {r} {r} 0 0 {1 if up else 0} {a+2*r} {cy} "
    s.path(d, SYM, SW)
    return x0, x0 + 2 * n * r


def sym_choke(s, cx, cy):
    a, b = _coil(s, cx, cy + 6, 4, 13)
    s.path(f"M {a} {cy-14} L {b} {cy-14}", SYM, 2.6)
    s.path(f"M {a} {cy-21} L {b} {cy-21}", SYM, 2.6)
    _lead(s, cx - 70, cy + 6, a); _lead(s, b, cy + 6, cx + 70)


def sym_inductor(s, cx, cy):
    a, b = _coil(s, cx, cy + 6, 4, 13)
    _lead(s, cx - 70, cy + 6, a); _lead(s, b, cy + 6, cx + 70)


def sym_starter(s, cx, cy):
    s.circle(cx, cy, 24, "none", SYM, SW)
    s.path(f"M {cx-10} {cy+6} L {cx-10} {cy-8} L {cx+10} {cy-8}", SYM, 2.8)
    _lead(s, cx - 62, cy, cx - 24); _lead(s, cx + 24, cy, cx + 62)


def sym_resistor(s, cx, cy):
    s.rect(cx - 38, cy - 15, 76, 30, "none", SYM, SW, 2)
    _lead(s, cx - 66, cy, cx - 38); _lead(s, cx + 38, cy, cx + 66)


def sym_capacitor(s, cx, cy):
    s.path(f"M {cx-9} {cy-28} L {cx-9} {cy+28}", SYM, SW + 0.6)
    s.path(f"M {cx+9} {cy-28} L {cx+9} {cy+28}", SYM, SW + 0.6)
    _lead(s, cx - 64, cy, cx - 9); _lead(s, cx + 9, cy, cx + 64)


def sym_battery(s, cx, cy):
    for i, (dx, h) in enumerate(((-21, 28), (-7, 14), (7, 28), (21, 14))):
        s.path(f"M {cx+dx} {cy-h/2} L {cx+dx} {cy+h/2}", SYM, SW + (0.8 if h > 20 else 0))
    _lead(s, cx - 64, cy, cx - 21); _lead(s, cx + 21, cy, cx + 64)


def sym_bell(s, cx, cy):
    s.path(f"M {cx-30} {cy+16} A 30 30 0 0 1 {cx+30} {cy+16} Z", SYM, SW)
    s.path(f"M {cx-34} {cy+16} L {cx+34} {cy+16}", SYM, SW)
    _lead(s, cx - 64, cy + 16, cx - 34); _lead(s, cx + 34, cy + 16, cx + 64)


def _circle_letter(s, cx, cy, txt, r=27, size=26):
    s.circle(cx, cy, r, "none", SYM, SW)
    s.text(cx, cy + size * 0.35, txt, size, SYM, 700, "middle")
    _lead(s, cx - 64, cy, cx - r); _lead(s, cx + r, cy, cx + 64)


def sym_motor(s, cx, cy):      _circle_letter(s, cx, cy, "M")
def sym_generator(s, cx, cy):  _circle_letter(s, cx, cy, "G")
def sym_ammeter(s, cx, cy):    _circle_letter(s, cx, cy, "A")
def sym_voltmeter(s, cx, cy):  _circle_letter(s, cx, cy, "V")
def sym_wattmeter(s, cx, cy):  _circle_letter(s, cx, cy, "W")


def sym_energy_meter(s, cx, cy):
    s.rect(cx - 44, cy - 26, 88, 52, "none", SYM, SW, 3)
    s.text(cx, cy + 8, "kWh", 21, SYM, 700, "middle")
    _lead(s, cx - 70, cy, cx - 44); _lead(s, cx + 44, cy, cx + 70)


def sym_transformer(s, cx, cy):
    for sx in (-1, 1):
        d = ""
        for i in range(4):
            yy = cy - 26 + i * 13
            d += (f"M {cx+sx*12} {yy} A 6.5 6.5 0 0 {1 if sx>0 else 0} "
                  f"{cx+sx*12} {yy+13} ")
        s.path(d, SYM, SW)
    s.path(f"M {cx-3} {cy-32} L {cx-3} {cy+32}", SYM, 2.6)
    s.path(f"M {cx+3} {cy-32} L {cx+3} {cy+32}", SYM, 2.6)
    _lead(s, cx - 68, cy - 26, cx - 12); _lead(s, cx - 68, cy + 26, cx - 12)
    _lead(s, cx + 12, cy - 26, cx + 68); _lead(s, cx + 12, cy + 26, cx + 68)


def _fan_blades(s, cx, cy, r, n=4):
    for i in range(n):
        a = math.radians(i * (360 / n) + 20)
        s.path(f"M {cx} {cy} Q {cx + r*0.75*math.cos(a-0.5):.1f} "
               f"{cy + r*0.75*math.sin(a-0.5):.1f} "
               f"{cx + r*math.cos(a):.1f} {cy + r*math.sin(a):.1f}", SYM, SW)


def sym_ceiling_fan(s, cx, cy):
    s.circle(cx, cy, 30, "none", SYM, SW)
    _fan_blades(s, cx, cy, 28)
    _dot(s, cx, cy, 6)
    s.path(f"M {cx} {cy-52} L {cx} {cy-30}", SYM, SW)


def sym_exhaust_fan(s, cx, cy):
    s.rect(cx - 32, cy - 32, 64, 64, "none", SYM, SW, 3)
    _fan_blades(s, cx, cy, 26, 4)
    _dot(s, cx, cy, 5)


def _socket(s, cx, cy, pins, label=None):
    s.path(f"M {cx-30} {cy+14} A 30 30 0 0 1 {cx+30} {cy+14}", SYM, SW)
    s.path(f"M {cx-30} {cy+14} L {cx+30} {cy+14}", SYM, SW)
    if label:
        s.text(cx, cy + 4, label, 17, SYM, 700, "middle")
    else:
        step = 40 / (pins + 1)
        for i in range(pins):
            x = cx - 20 + step * (i + 1)
            s.path(f"M {x} {cy+14} L {x} {cy-8}", SYM, 2.6)
    _lead(s, cx - 62, cy + 14, cx - 30)


def sym_socket2(s, cx, cy): _socket(s, cx, cy, 2)
def sym_socket3(s, cx, cy): _socket(s, cx, cy, 3)
def sym_tv_socket(s, cx, cy): _socket(s, cx, cy, 0, "TV")


def sym_ceiling_rose(s, cx, cy):
    s.circle(cx, cy, 24, "none", SYM, SW)
    _dot(s, cx, cy, 6)
    for a in (0, 120, 240):
        r = math.radians(a)
        s.path(f"M {cx+24*math.cos(r):.1f} {cy+24*math.sin(r):.1f} "
               f"L {cx+46*math.cos(r):.1f} {cy+46*math.sin(r):.1f}", SYM, SW)


def _board(s, cx, cy, fill_ratio):
    s.rect(cx - 46, cy - 26, 92, 52, "none", SYM, SW, 3)
    w = 92 * fill_ratio
    s.rect(cx - 46, cy - 26, w, 52, SYM, "none", 0, 3)


def sym_mdb(s, cx, cy): _board(s, cx, cy, 1.0)
def sym_sdb(s, cx, cy): _board(s, cx, cy, 0.5)
def sym_sb(s, cx, cy):  _board(s, cx, cy, 0.0)


def sym_fire_bell(s, cx, cy):
    s.circle(cx, cy, 30, "none", SYM, SW)
    s.path(f"M {cx-17} {cy+10} A 17 17 0 0 1 {cx+17} {cy+10} Z", SYM, 2.8)
    s.path(f"M {cx-21} {cy+10} L {cx+21} {cy+10}", SYM, 2.8)


def sym_fire_detector(s, cx, cy):
    s.circle(cx, cy, 30, "none", SYM, SW)
    s.text(cx, cy + 8, "FD", 21, SYM, 700, "middle")


def sym_smoke_detector(s, cx, cy):
    s.circle(cx, cy, 30, "none", SYM, SW)
    s.text(cx, cy + 8, "SD", 21, SYM, 700, "middle")


# ═══════════════════════════════════════════════════════════════════════
def symbol_sheet(fname, title, items, cols=3):
    """Grid of symbols with Bangla + English captions."""
    CW, CH = 400, 232
    rows = (len(items) + cols - 1) // cols
    W = 40 + cols * CW + 40
    s = SVG(W, 120 + rows * CH + 30)
    s.title(title, T_TITLE)
    for idx, (fn, bn_, en) in enumerate(items):
        r, c = divmod(idx, cols)
        x = 40 + c * CW
        y = 104 + r * CH
        s.rect(x + 6, y, CW - 12, CH - 14, "#FCFDFE", LINE, 1.6, 12)
        fn(s, x + CW / 2, y + 78)
        s.text(x + CW / 2, y + 158, bn_, T_BODY, NAVY, 700, "middle")
        s.text(x + CW / 2, y + 186, en, T_SMALL, GREY, 400, "middle")
    s.fit(104 + rows * CH - 14, 22)
    return s.save(f"{OUT}/{fname}.svg")


def d03_symbols_switch():
    return symbol_sheet(
        "d03_symbols_switch", "ইলেকট্রিক্যাল প্রতীক — সুইচ ও নিয়ন্ত্রণ (IEC 60617)",
        [(sym_spst, "এক-মুখী সুইচ", "SPST Switch"),
         (sym_spdt, "টু-ওয়ে সুইচ", "SPDT / Two-way Switch"),
         (sym_intermediate, "ইন্টারমিডিয়েট সুইচ", "Intermediate Switch"),
         (sym_push, "পুশ সুইচ", "Push Switch"),
         (sym_main_switch, "মেইন সুইচ", "Main Switch"),
         (sym_ceiling_rose, "সিলিং রোজ", "Ceiling Rose"),
         (sym_mdb, "মেইন ডিস্ট্রিবিউশন বোর্ড", "MDB"),
         (sym_sdb, "সাব ডিস্ট্রিবিউশন বোর্ড", "SDB"),
         (sym_sb, "সুইচ বোর্ড", "SB — Switch Board")])


def d04_symbols_light():
    return symbol_sheet(
        "d04_symbols_light", "ইলেকট্রিক্যাল প্রতীক — আলো, ফ্যান ও আউটলেট",
        [(sym_lamp, "বাতি", "Lamp"),
         (sym_tube, "টিউব লাইট", "Tube Light"),
         (sym_choke, "চোক কয়েল", "Choke Coil"),
         (sym_starter, "স্টার্টার", "Tube Light Starter"),
         (sym_ceiling_fan, "সিলিং ফ্যান", "Ceiling Fan"),
         (sym_exhaust_fan, "এক্সহস্ট ফ্যান", "Exhaust Fan"),
         (sym_socket2, "টু-পিন সকেট", "2 Pin Socket"),
         (sym_socket3, "থ্রি-পিন সকেট", "3 Pin Socket"),
         (sym_tv_socket, "টিভি সকেট", "TV Socket Outlet")])


def d05_symbols_safety():
    return symbol_sheet(
        "d05_symbols_safety", "ইলেকট্রিক্যাল প্রতীক — সুরক্ষা, আর্থিং ও সংকেত",
        [(sym_fuse, "ফিউজ", "Fuse"),
         (sym_earthing, "আর্থিং", "Earthing"),
         (sym_earth_electrode, "আর্থ ইলেকট্রোড", "Earth Electrode"),
         (sym_bell, "বৈদ্যুতিক ঘণ্টা", "Bell"),
         (sym_fire_bell, "ফায়ার অ্যালার্ম বেল", "Fire Alarm Bell"),
         (sym_fire_detector, "ফায়ার ডিটেক্টর", "Fire Detector"),
         (sym_smoke_detector, "স্মোক ডিটেক্টর", "Smoke Detector"),
         (sym_battery, "ব্যাটারি", "Battery"),
         (sym_resistor, "রেজিস্ট্যান্স", "Resistance")])


def d06_symbols_machine():
    return symbol_sheet(
        "d06_symbols_machine", "ইলেকট্রিক্যাল প্রতীক — যন্ত্র ও পরিমাপক",
        [(sym_capacitor, "ক্যাপাসিটর", "Capacitor"),
         (sym_inductor, "ইন্ডাক্টিভ কয়েল", "Inductive Coil"),
         (sym_transformer, "ট্রান্সফরমার", "Transformer"),
         (sym_motor, "মোটর", "Motor"),
         (sym_generator, "জেনারেটর", "Generator"),
         (sym_ammeter, "অ্যামিটার", "Ammeter"),
         (sym_voltmeter, "ভোল্টমিটার", "Voltmeter"),
         (sym_wattmeter, "ওয়াট মিটার", "Watt Meter"),
         (sym_energy_meter, "এনার্জি মিটার", "Energy Meter")])


# ═══════════════════════════════════════════════════════════════════════
def d01_material_classes():
    s = SVG(1300, 900)
    s.title("তড়িৎ পরিবাহিতার ভিত্তিতে পদার্থের শ্রেণিবিভাগ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 16)
    rx, ry, rw, rh = s.box_auto(650, 74, "পদার্থ (Material)", T_NODE,
                                fill=NAVY, stroke=NAVY, tcolor="#FFFFFF",
                                pad_x=34, pad_y=17)
    cols = [
        ("পরিবাহী", "Conductor", "#E8F0F8", STEEL,
         ["বিদ্যুৎ চলাচলে প্রায় কোনো বাধা দেয় না",
          "বাইরের কক্ষপথে ১–৩টি ইলেকট্রন",
          "মুক্ত ইলেকট্রন প্রচুর",
          "সোনা, রুপা, তামা, অ্যালুমিনিয়াম",
          "তার ও বাসবার তৈরিতে ব্যবহৃত"]),
        ("অর্ধপরিবাহী", "Semiconductor", "#FFF6E5", AMBER,
         ["আংশিক বাধা দেয় — মাঝামাঝি অবস্থা",
          "বাইরের কক্ষপথে ৪টি ইলেকট্রন",
          "তাপ বাড়লে পরিবাহিতা বাড়ে",
          "সিলিকন, জার্মেনিয়াম, কার্বন",
          "ডায়োড, LED, ট্রানজিস্টরে ব্যবহৃত"]),
        ("অপরিবাহী", "Insulator", "#EAF6EF", GREEN,
         ["বিদ্যুৎ চলাচল করতে দেয় না",
          "বাইরের কক্ষপথে ৮টি ইলেকট্রন",
          "মুক্ত ইলেকট্রন প্রায় নেই",
          "রাবার, PVC, কাচ, চিনামাটি, কাঠ",
          "ইনসুলেশন ও আবরণে ব্যবহৃত"]),
    ]
    cw, gapx = 396, 26
    x0 = (1300 - (3 * cw + 2 * gapx)) / 2
    ytop = 244
    s.path(f"M 650 {ry+rh:.1f} L 650 {ytop-76:.1f}", STEEL, 2.6)
    for i, (bn_, en, bg, br, items) in enumerate(cols):
        cx = x0 + i * (cw + gapx) + cw / 2
        s.path(f"M 650 {ytop-76:.1f} L {cx:.1f} {ytop-76:.1f} L {cx:.1f} {ytop-22:.1f}",
               STEEL, 2.6, marker=ar)
        s.box_auto(cx, ytop - 12, bn_, T_NAME, fill=br, stroke=br,
                   tcolor="#FFFFFF", pad_x=28, pad_y=13, min_w=250)
        s.text(cx, ytop + 74, en, T_SMALL, br, 700, "middle")
    bot = 0
    for i, (bn_, en, bg, br, items) in enumerate(cols):
        bot = max(bot, bullet_panel(s, x0 + i * (cw + gapx), ytop + 94, cw,
                                    items, T_BODY, bg, br, INK, br))
    s.text(650, bot + 46,
           "একই পদার্থ অবস্থাভেদে আচরণ বদলাতে পারে — যেমন শুকনা কাঠ অপরিবাহী, ভেজা কাঠ নয়",
           T_SMALL, GREY, 400, "middle")
    s.fit(bot + 46, 26)
    return s.save(f"{OUT}/d01_material_classes.svg")


def d02_energy_band():
    """Valence band / forbidden gap / conduction band for the three classes."""
    s = SVG(1240, 660)
    s.title("এনার্জি ব্যান্ড — তিন শ্রেণির পার্থক্য", T_TITLE)
    panels = [("পরিবাহী", STEEL, "#EAF2FA", 0),
              ("অর্ধপরিবাহী", AMBER, "#FFF6E5", 58),
              ("অপরিবাহী", GREEN, "#EAF6EF", 150)]
    pw, gapx = 356, 30
    x0 = (1240 - (3 * pw + 2 * gapx)) / 2
    BASE = 470
    for i, (name, col, bg, gap) in enumerate(panels):
        x = x0 + i * (pw + gapx)
        s.rect(x, 96, pw, 456, "#FCFDFE", LINE, 1.8, 13)
        s.box_auto(x + pw / 2, 110, name, T_NAME, fill=col, stroke=col,
                   tcolor="#FFFFFF", pad_x=24, pad_y=10)
        vb_top = BASE - 60
        s.rect(x + 46, vb_top - 46, pw - 92, 46, col, col, 1.6, 4)
        s.text(x + pw / 2, vb_top - 16, "ভ্যালেন্স ব্যান্ড", T_SMALL,
               "#FFFFFF", 700, "middle")
        cb_bot = vb_top - 46 - gap
        s.rect(x + 46, cb_bot - 46, pw - 92, 46, "#9FC4E6" if i == 0 else "#C9D6E2",
               col, 1.6, 4)
        s.text(x + pw / 2, cb_bot - 16, "কন্ডাকশন ব্যান্ড", T_SMALL,
               NAVY, 700, "middle")
        if gap:
            s.rect(x + 46, cb_bot, pw - 92, gap, "#FFFFFF", "none", 0, 0)
            s.path(f"M {x+56} {cb_bot} L {x+56} {cb_bot+gap}", GREY, 2, dash="7 5")
            s.path(f"M {x+pw-56} {cb_bot} L {x+pw-56} {cb_bot+gap}", GREY, 2, dash="7 5")
            s.text(x + pw / 2, cb_bot + gap / 2 + 7,
                   "ফরবিডেন গ্যাপ", T_SMALL, GREY, 600, "middle")
        note = ["দুই ব্যান্ড পরস্পরকে স্পর্শ করে — ইলেকট্রন সহজেই চলে",
                "গ্যাপ ছোট — তাপ বা আলো পেলে ইলেকট্রন লাফ দিতে পারে",
                "গ্যাপ অনেক বড় — ইলেকট্রন লাফ দিতে পারে না"][i]
        for j, ln in enumerate(wrap(note, pw - 56, T_SMALL, 400)):
            s.text(x + pw / 2, BASE + 22 + j * T_SMALL * 1.34, ln, T_SMALL,
                   "#39434D", 400, "middle")
    s.text(620, 596, "গ্যাপ যত বড়, পদার্থ তত ভালো অপরিবাহী",
           T_NAME, NAVY, 700, "middle")
    s.fit(604, 24)
    return s.save(f"{OUT}/d02_energy_band.svg")


def d07_diagram_types():
    """The same lamp circuit shown three ways."""
    s = SVG(1240, 620)
    s.title("একই বর্তনীর তিন ধরনের অঙ্কন", T_TITLE)
    pw, gapx = 372, 34
    x0 = (1240 - (3 * pw + 2 * gapx)) / 2
    heads = [("সার্কিট ডায়াগ্রাম", "Circuit Diagram",
              "প্রতীক দিয়ে বৈদ্যুতিক সম্পর্ক দেখায়"),
             ("কানেকশন ডায়াগ্রাম", "Connection Diagram",
              "কোন তার কোথায় লাগবে তা দেখায়"),
             ("লে-আউট ডায়াগ্রাম", "Layout Diagram",
              "ঘরের কোথায় কী বসবে তা দেখায়")]
    for i, (bn_, en, note) in enumerate(heads):
        x = x0 + i * (pw + gapx)
        s.rect(x, 96, pw, 356, "#FCFDFE", LINE, 1.8, 13)
        s.box_auto(x + pw / 2, 110, bn_, T_BODY, fill=STEEL, stroke=STEEL,
                   tcolor="#FFFFFF", pad_x=22, pad_y=10)
        s.text(x + pw / 2, 182, en, T_SMALL, STEEL, 700, "middle")
        cx, cy = x + pw / 2, 300
        if i == 0:
            L, R_, T, B = cx - 118, cx + 118, cy - 62, cy + 62
            # the loop is drawn as separate runs so the wire breaks where the
            # switch and the lamp sit, instead of running straight through them
            s.path(f"M {L} {T} L {cx-26} {T}", SYM, 3)          # top, left of switch
            s.path(f"M {cx+26} {T} L {R_} {T}", SYM, 3)         # top, right of switch
            s.path(f"M {R_} {T} L {R_} {cy-22}", SYM, 3)        # right, above lamp
            s.path(f"M {R_} {cy+22} L {R_} {B}", SYM, 3)        # right, below lamp
            s.path(f"M {R_} {B} L {L} {B}", SYM, 3)             # bottom
            s.path(f"M {L} {B} L {L} {cy+20}", SYM, 3)          # left, below battery
            s.path(f"M {L} {cy-20} L {L} {T}", SYM, 3)          # left, above battery
            # switch (open)
            _dot(s, cx - 26, T); _dot(s, cx + 26, T)
            s.path(f"M {cx-26} {T} L {cx+20} {T-26}", SYM, 3)
            # lamp
            s.circle(R_, cy, 22, "#FFFFFF", SYM, 3)
            k = 22 * .707
            s.path(f"M {R_-k} {cy-k} L {R_+k} {cy+k}", SYM, 2.4)
            s.path(f"M {R_-k} {cy+k} L {R_+k} {cy-k}", SYM, 2.4)
            # battery — plates across the left conductor, long/short alternating
            for dy, ww in ((-20, 34), (-7, 18), (7, 34), (20, 18)):
                s.path(f"M {L-ww/2} {cy+dy} L {L+ww/2} {cy+dy}", SYM, 3.2)
            s.text(cx, B + 34, "প্রতীকভিত্তিক", T_SMALL, GREY, 400, "middle")
        elif i == 1:
            s.rect(cx - 108, cy - 56, 70, 46, "none", SYM, 3, 4)
            s.text(cx - 73, cy - 26, "সুইচ", 17, SYM, 600, "middle")
            s.circle(cx + 86, cy - 34, 22, "none", SYM, 3)
            s.text(cx + 86, cy - 28, "বাতি", 15, SYM, 600, "middle")
            s.path(f"M {cx-108} {cy+40} L {cx+120} {cy+40}", "#B32A22", 3.2)
            s.path(f"M {cx-108} {cy+58} L {cx+120} {cy+58}", "#1E63B5", 3.2)
            s.path(f"M {cx-90} {cy+40} L {cx-90} {cy-10}", "#B32A22", 3.2)
            s.path(f"M {cx-50} {cy-10} L {cx-50} {cy+4} L {cx+86} {cy+4} "
                   f"L {cx+86} {cy-12}", "#B32A22", 3.2)
            s.path(f"M {cx+108} {cy+58} L {cx+108} {cy-34} L {cx+108} {cy-34}",
                   "#1E63B5", 3.2)
            s.text(cx + 6, cy + 88, "তারের রং অনুযায়ী", T_SMALL, GREY, 400, "middle")
        else:
            s.rect(cx - 118, cy - 66, 236, 132, "none", "#8D9AA8", 3, 4)
            s.path(f"M {cx-40} {cy-66} L {cx+10} {cy-66}", "#FFFFFF", 6)
            s.path(f"M {cx-40} {cy-66} L {cx+10} {cy-66}", "#8D9AA8", 3, dash="6 6")
            sym_ceiling_fan(s, cx - 44, cy - 4)
            s.circle(cx + 54, cy - 24, 17, "none", SYM, 2.6)
            k = 17 * .707
            s.path(f"M {cx+54-k} {cy-24-k} L {cx+54+k} {cy-24+k}", SYM, 2.2)
            s.path(f"M {cx+54-k} {cy-24+k} L {cx+54+k} {cy-24-k}", SYM, 2.2)
            _socket(s, cx + 56, cy + 34, 3)
            s.text(cx, cy + 100, "ঘরের নকশার উপর", T_SMALL, GREY, 400, "middle")
        for j, ln in enumerate(wrap(note, pw - 44, T_SMALL, 400)):
            s.text(x + pw / 2, 476 + j * T_SMALL * 1.34, ln, T_SMALL,
                   "#39434D", 400, "middle")
    s.rect(40, 540, 1160, 56, "#EAF2FA", STEEL, 2, 11)
    s.text(620, 575,
           "তিনটিই এক বর্তনীর ভিন্ন উপস্থাপন — উদ্দেশ্য অনুযায়ী বেছে নিতে হয়",
           T_NAME, NAVY, 700, "middle")
    s.fit(596, 22)
    return s.save(f"{OUT}/d07_diagram_types.svg")


ALL = [d01_material_classes, d02_energy_band, d03_symbols_switch,
       d04_symbols_light, d05_symbols_safety, d06_symbols_machine,
       d07_diagram_types]

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
