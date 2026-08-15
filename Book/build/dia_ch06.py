# -*- coding: utf-8 -*-
"""অধ্যায় ৬ — বেল সার্কিট (৬–৯) : ডায়াগ্রাম।

Same two-panel treatment as chapter 3 — symbol circuit on the left, pictorial
connection diagram with IEC conductor colours on the right.
"""
import os, math
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams", "ch06")
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "ch06")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
LH = 1.42

SYM = "#12324D"
SW = 3.2
BROWN = "#7A4A21"
BLUE = "#1E63B5"
EGREEN = "#2E8B31"


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


# ── symbols ─────────────────────────────────────────────────────────────
def _dot(s, x, y, r=5):
    s.circle(x, y, r, SYM)


def sym_bell(s, cx, cy, r=26):
    s.path(f"M {cx-r} {cy+r*0.5} A {r} {r} 0 0 1 {cx+r} {cy+r*0.5} Z", SYM, SW)
    s.path(f"M {cx-r-6} {cy+r*0.5} L {cx+r+6} {cy+r*0.5}", SYM, SW)


def sym_buzzer(s, cx, cy, r=24):
    s.path(f"M {cx-r} {cy+12} L {cx-r} {cy-12} L {cx+r} {cy-12} L {cx+r} {cy+12} Z",
           SYM, SW)
    for k in range(3):
        s.path(f"M {cx-14+k*14} {cy-12} L {cx-7+k*14} {cy+12}", SYM, 2.2)


def sym_push(s, cx, cy, gap=24):
    _dot(s, cx - gap, cy); _dot(s, cx + gap, cy)
    s.path(f"M {cx-gap-4} {cy-16} L {cx+gap+4} {cy-16}", SYM, SW)
    s.path(f"M {cx} {cy-16} L {cx} {cy-36}", SYM, SW)
    s.path(f"M {cx-13} {cy-36} L {cx+13} {cy-36}", SYM, SW)


def sym_lamp(s, cx, cy, r=20):
    s.circle(cx, cy, r, "#FFFFFF", SYM, SW)
    k = r * 0.707
    s.path(f"M {cx-k} {cy-k} L {cx+k} {cy+k}", SYM, 2.2)
    s.path(f"M {cx-k} {cy+k} L {cx+k} {cy-k}", SYM, 2.2)


def sym_spdt(s, cx, cy, gap=24):
    _dot(s, cx - gap, cy)
    _dot(s, cx + gap, cy - 18); _dot(s, cx + gap, cy + 18)
    s.path(f"M {cx-gap} {cy} L {cx+gap-4} {cy-18}", SYM, SW)


def plug_supply(s, x, cy, ytop, ybot):
    """Plug at the supply end, pins running to the two conductors."""
    s.rect(x - 44, cy - 26, 44, 52, "#FFFFFF", SYM, SW, 6)
    for yy in (cy - 12, cy + 12):
        s.path(f"M {x} {yy} L {x+18} {yy}", SYM, 2.8)
    s.path(f"M {x+18} {cy-12} L {x+18} {ytop}", SYM, SW)
    s.path(f"M {x+18} {cy+12} L {x+18} {ybot}", SYM, SW)
    return x + 18


# ── pictorial ───────────────────────────────────────────────────────────
def rails(s, x1, x2, y):
    s.path(f"M {x1} {y} L {x2} {y}", BROWN, 5)
    s.text(x1 - 12, y + 7, "L", T_SMALL, BROWN, 700, "end")
    s.path(f"M {x1} {y+34} L {x2} {y+34}", BLUE, 5)
    s.text(x1 - 12, y + 41, "N", T_SMALL, BLUE, 700, "end")
    return y, y + 34


def pic_bell(s, cx, cy):
    s.path(f"M {cx-30} {cy+14} A 30 30 0 0 1 {cx+30} {cy+14} Z",
           "#7C8794", 2.4, "#B7C1CB")
    s.rect(cx - 36, cy + 14, 72, 10, "#8D9AA8", "#6B7684", 2, 3)
    s.circle(cx, cy + 30, 7, "#8D9AA8", "#6B7684", 1.8)
    return (cx - 18, cy + 24), (cx + 18, cy + 24)


def pic_push(s, cx, cy):
    s.rect(cx - 28, cy - 24, 56, 48, "#FFFFFF", "#7C8794", 2.4, 6)
    s.circle(cx, cy, 13, "#DCE6EC", "#8D9AA8", 2)
    return (cx - 28, cy), (cx + 28, cy)


def pic_lamp(s, cx, cy, r=17):
    s.circle(cx, cy, r, "#FFF3C4", "#B08C00", 2.2)
    s.path(f"M {cx-8} {cy+4} q 8 -14 16 0", "#B08C00", 2)
    return (cx, cy + r)


def panel(s, x, y, w, h, title, col=STEEL):
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def image_panel(s, cx, top, bottom, path, half=268, pad=14):
    """RAPTI-এর নিজস্ব সোর্স ডায়াগ্রাম (Circuit Diagram.pptx /
    HW Connection Diagram All.pptx থেকে) হুবহু বসানো — নতুন করে আঁকা নয়।"""
    s.image_fit(cx - half, top, half * 2, bottom - top, path, pad)


def _sheet(fname, title, draw_circuit, draw_conn, note, h=560):
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


# ═══════════════════════════════════════════════════════════════════════
def d01_bell_parts():
    s = SVG(1240, 620)
    s.title("বৈদ্যুতিক ঘণ্টার গঠন ও কার্যপ্রণালি", T_TITLE)

    ax = 480                       # armature centre-x (pivots from a spring at top)
    fy = 110                       # fixed frame bracket
    sp_top, sp_bot = 124, 172      # spring span
    mx, my = 320, 280              # electromagnet core centre
    hy = 296                       # hammer height (near the armature's free/lower end)
    gx = 640                       # gong centre-x

    # fixed frame bracket, mounted above the armature
    s.rect(ax - 32, fy - 10, 64, 16, "#B7C1CB", "#7C8794", 2, 3)

    # spring — flexible mount that returns the armature after each pull
    zig = [f"M {ax-13} {sp_top}"]
    for i in range(1, 5):
        yy = sp_top + (sp_bot - sp_top) * i / 4
        zig.append(f"L {ax + (13 if i % 2 else -13)} {yy:.0f}")
    s.path(" ".join(zig), "#6B7684", 3.4)

    # armature — soft-iron bar hanging in front of the electromagnet
    s.rect(ax - 9, sp_bot, 18, 150, "#8D9AA8", "#6B7684", 2, 3)

    # electromagnet: core + coil, pole facing the armature with a clear air-gap
    s.rect(mx - 75, my - 22, 150, 44, "#B7C1CB", "#7C8794", 2.4, 5)
    for k in range(7):
        xx = mx - 68 + k * 20
        s.path(f"M {xx} {my+20} Q {xx+9} {my-42} {xx+18} {my+20}", "#C57A2A", 6.5)
    s.path(f"M {mx+80} {my} L {ax-13} {my}", "#9AA6B2", 2, dash="5,5")

    # hammer — rigid arm off the armature's lower end, striking the gong's rim
    s.path(f"M {ax+9} {hy} L {ax+92} {hy}", "#8D9AA8", 6)
    s.circle(ax + 106, hy, 13, "#8D9AA8", "#6B7684", 2)

    # gong — bell dome, rim level with the hammer knob
    sym_bell(s, gx, hy - 24, 48)

    # contact screw — fixed bracket touching the armature's back (away from the magnet)
    csy = sp_bot + 38
    s.rect(ax + 24, csy - 8, 28, 16, "#B7C1CB", "#7C8794", 1.8, 2)
    s.path(f"M {ax+24} {csy} L {ax+9} {csy}", "#8D9AA8", 3.6)
    _dot(s, ax + 9, csy, 5)

    labels = [("ইলেকট্রোম্যাগনেট", mx, my + 46, "middle", 0, 0),
              ("আর্মেচার", ax - 15, sp_bot + 20, "end", 0, 0),
              ("স্প্রিং", ax - 46, (sp_top + sp_bot) / 2 + 6, "end", 0, 0),
              ("হ্যামার", ax + 100, hy - 26, "middle", 0, 0),
              ("গং", gx, hy - 86, "middle", 0, 0),
              ("কন্টাক্ট স্ক্রু", ax + 38, csy + 34, "middle", 0, 0)]
    for name, px, py, anc, dx, dy in labels:
        s.text(px + dx, py + dy, name, T_SMALL, NAVY, 700, anc)

    bullet_panel(s, 720, 150, 470,
                 ["সুইচ চাপলে কয়েলে কারেন্ট গিয়ে চুম্বক তৈরি হয়",
                  "চুম্বক আর্মেচারকে টেনে আনে, হ্যামার গংয়ে আঘাত করে",
                  "আর্মেচার সরে গেলে কন্টাক্ট ছুটে বর্তনী ভেঙে যায়",
                  "চুম্বকত্ব হারিয়ে আর্মেচার ফিরে এসে আবার কন্টাক্ট করে",
                  "এভাবে দ্রুত বারবার আঘাত হয় — একটানা শব্দ শোনা যায়"],
                 T_BODY, "#EAF2FA", STEEL, INK, STEEL)

    s.rect(60, 500, 1120, 58, "#FFF6E5", AMBER, 2, 11)
    s.text(620, 536,
           "এই বারবার ভাঙা-জোড়ার কারণেই একে ট্রেম্বলিং বেল বলা হয়",
           T_NAME, "#7A5200", 700, "middle")
    s.fit(558, 22)
    return s.save(f"{OUT}/d01_bell_parts.svg")


def d02_bell_types():
    s = SVG(1240, 560)
    s.title("বেল ও বাজারের প্রকারভেদ", T_TITLE)
    items = [("ট্রেম্বলিং বেল", "Trembling Bell", "একটানা শব্দ করে", "bell"),
             ("সিঙ্গেল স্ট্রোক বেল", "Single Stroke Bell", "একবার চাপে একবার শব্দ", "bell"),
             ("বাজার", "Buzzer", "ভোঁ ভোঁ শব্দ করে", "buzz"),
             ("ইলেকট্রনিক চাইম", "Electronic Chime", "সুরেলা শব্দ", "chime")]
    cw, gapx = 272, 24
    x0 = (1240 - (4 * cw + 3 * gapx)) / 2
    for i, (bn_, en, note, kind) in enumerate(items):
        x = x0 + i * (cw + gapx)
        s.rect(x, 96, cw, 292, "#FCFDFE", LINE, 1.8, 13)
        cx, cy = x + cw / 2, 190
        if kind == "bell":
            sym_bell(s, cx, cy - 6, 32)
            if "সিঙ্গেল" in bn_:
                s.path(f"M {cx+40} {cy-30} L {cx+58} {cy-30}", SYM, 3)
        elif kind == "buzz":
            sym_buzzer(s, cx, cy, 30)
        else:
            s.rect(cx - 34, cy - 26, 68, 52, "#FFFFFF", SYM, SW, 6)
            for k in range(3):
                s.path(f"M {cx-16+k*16} {cy+12} L {cx-16+k*16} {cy-14}", SYM, 3)
        s.text(cx, 292, bn_, T_BODY, NAVY, 700, "middle")
        s.text(cx, 320, en, T_SMALL, STEEL, 600, "middle")
        for j, ln in enumerate(wrap(note, cw - 40, T_SMALL, 400)):
            s.text(cx, 352 + j * T_SMALL * 1.32, ln, T_SMALL, GREY, 400, "middle")
    s.text(620, 432, "সব ক্ষেত্রেই নিয়ন্ত্রণ হয় পুশ সুইচ দিয়ে — চাপলে বাজে, ছাড়লে থামে",
           T_SMALL, GREY, 400, "middle")
    s.fit(432, 24)
    return s.save(f"{OUT}/d02_bell_types.svg")


def d03_simple():
    def circ(s, cx):
        image_panel(s, cx, 150, 406, f"{IMG}/d03_simple_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 406, f"{IMG}/d03_simple_conn.png")

    return _sheet("d03_simple", "বেল সার্কিট ৬ — সাধারণ কলিং বেল", circ, conn,
                  "পুশ সুইচ ফেজ তারে বসে; চাপ দিলে বর্তনী সম্পূর্ণ হয়ে বেল বাজে")


def d04_two_switch():
    def circ(s, cx):
        image_panel(s, cx, 150, 466, f"{IMG}/d04_two_switch_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 466, f"{IMG}/d04_two_switch_conn.png")

    return _sheet("d04_two_switch", "বেল সার্কিট ৭ — দুই স্থান থেকে একটি বেল",
                  circ, conn,
                  "দুটি পুশ সুইচ প্যারালালে — যেকোনো একটি চাপলেই বেল বাজবে", 620)


def d05_series():
    def circ(s, cx):
        image_panel(s, cx, 150, 406, f"{IMG}/d05_series_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 406, f"{IMG}/d05_series_conn.png")

    return _sheet("d05_series", "বেল সার্কিট ৮ — সিরিজ বেল সার্কিট", circ, conn,
                  "সুইচ, বাতি ও বেল একই সিরিজে — একসঙ্গে চালু হয়, একটি নষ্ট হলে সব বন্ধ")


def d06_emergency():
    def circ(s, cx):
        image_panel(s, cx, 150, 426, f"{IMG}/d06_emergency_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 426, f"{IMG}/d06_emergency_conn.png")

    return _sheet("d06_emergency", "বেল সার্কিট ৯ — ইমার্জেন্সি অ্যালার্ম",
                  circ, conn,
                  "দুটি সুইচ, দুটি বেল প্যারালালে — যেকোনো একটি চাপলেই সব বেল বাজে", 580)


def d07_indicator():
    """Three rooms, each switch+lamp in series, sharing one common bell."""
    def circ(s, cx):
        image_panel(s, cx, 150, 466, f"{IMG}/d07_indicator_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 466, f"{IMG}/d07_indicator_conn.png")

    return _sheet("d07_indicator", "তিন স্থান থেকে বেল ও ইন্ডিকেটর বাতি", circ, conn,
                  "প্রতিটি সুইচ-বাতি শাখা সিরিজে, শাখাগুলো পরস্পর প্যারালালে — "
                  "যেকোনো একটি চাপলে সেই কক্ষের বাতিসহ বেল বাজে", 620)


ALL = [d01_bell_parts, d02_bell_types, d03_simple, d04_two_switch,
       d05_series, d06_emergency, d07_indicator]

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
