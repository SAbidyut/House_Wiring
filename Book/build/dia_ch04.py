# -*- coding: utf-8 -*-
"""অধ্যায় ৪ — ইলেকট্রিসিটি বা বিদ্যুৎ : টেকনিক্যাল ডায়াগ্রাম।"""
import os, math
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams", "ch04")

T_TITLE = 34
T_NODE = 28
T_NAME = 25.5
T_BODY = 23
T_SMALL = 22.5
LH = 1.42


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
def d01_atom():
    """Atom, shells and the free electron that makes conduction possible."""
    s = SVG(1240, 700)
    s.title("পরমাণুর গঠন ও মুক্ত ইলেকট্রন", T_TITLE)
    cx, cy = 430, 380

    for i, r in enumerate((108, 158, 210)):
        s.circle(cx, cy, r, "none", "#C3CEDA", 2, 0.9 if i < 2 else 0.6)
    # nucleus
    s.circle(cx, cy, 74, "#F2C200", "#B08C00", 2.6)
    s.text(cx, cy - 4, "নিউক্লিয়াস", 23, "#5A4200", 700, "middle")
    s.text(cx, cy + 26, "প্রোটন ও নিউট্রন", 21, "#5A4200", 400, "middle")

    # bound electrons
    # 2 + 8 in the inner shells and one lone electron outside (sodium/copper-like)
    for r, angles in ((108, (40, 220)), (158, tuple(10 + 45 * k for k in range(8)))):
        for a in angles:
            ex = cx + r * math.cos(math.radians(a))
            ey = cy + r * math.sin(math.radians(a))
            s.circle(ex, ey, 13, STEEL, "#FFFFFF", 2.4)
            s.text(ex, ey + 6, "−", 19, "#FFFFFF", 700, "middle")
    # valence / free electron
    fx = cx + 210 * math.cos(math.radians(-38))
    fy = cy + 210 * math.sin(math.radians(-38))
    s.circle(fx, fy, 15, RED, "#FFFFFF", 2.6)
    s.text(fx, fy + 7, "−", 21, "#FFFFFF", 700, "middle")
    ar = s.arrow_defs(RED, "ar", 14)
    s.path(f"M {fx+22:.1f} {fy-14:.1f} L {fx+92:.1f} {fy-64:.1f}", RED, 3.2, marker=ar)

    s.text(770, 214, "মুক্ত ইলেকট্রন", T_NAME, RED, 700)
    for j, ln in enumerate(wrap(
            "সবচেয়ে বাইরের কক্ষপথের ইলেকট্রন নিউক্লিয়াসের টান কম অনুভব করে, "
            "তাই সহজেই পরমাণু ছেড়ে বেরিয়ে যেতে পারে", 420, T_SMALL, 400)):
        s.text(770, 250 + j * T_SMALL * 1.34, ln, T_SMALL, "#39434D", 400)

    bullet_panel(s, 766, 342, 462,
                 ["পরিবাহীতে মুক্ত ইলেকট্রনের সংখ্যা অনেক বেশি",
                  "অপরিবাহীতে ইলেকট্রন শক্তভাবে আবদ্ধ থাকে",
                  "মুক্ত ইলেকট্রনের সুশৃঙ্খল প্রবাহই কারেন্ট"],
                 T_BODY, "#EAF2FA", STEEL, INK, STEEL)
    # the exponent is a real raised tspan: Kalpurush has no ⁻¹⁹ glyphs
    s.add('<text x="620" y="660" font-family="Kalpurush" font-size="22.5" fill="#5A6470" '
          'text-anchor="middle">একটি ইলেকট্রনের চার্জ = 1.6 × 10'
          '<tspan dy="-10" font-size="16">−19</tspan>'
          '<tspan dy="10" font-size="22.5"> কুলম্ব (ঋণাত্মক)</tspan></text>')
    s.fit(660, 24)
    return s.save(f"{OUT}/d01_atom.svg")


def d02_types():
    """Classification of electricity."""
    s = SVG(1240, 700)
    s.title("বিদ্যুতের শ্রেণিবিন্যাস", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 16)
    rx, ry, rw, rh = s.box_auto(620, 74, "বিদ্যুৎ (Electricity)", T_NODE,
                                fill=NAVY, stroke=NAVY, tcolor="#FFFFFF",
                                pad_x=34, pad_y=17)
    y1 = 222
    for cx, name, col in ((330, "স্থির বিদ্যুৎ", AMBER), (910, "চল বিদ্যুৎ", STEEL)):
        s.path(f"M 620 {ry+rh:.1f} L 620 {y1-56:.1f} L {cx:.1f} {y1-56:.1f} "
               f"L {cx:.1f} {y1-14:.1f}", STEEL, 2.6, marker=ar)
        s.box_auto(cx, y1 - 4, name, T_NAME, fill=col, stroke=col,
                   tcolor="#FFFFFF", pad_x=28, pad_y=13, min_w=260)
    bullet_panel(s, 130, y1 + 66, 400,
                 ["উৎপত্তিস্থলেই স্থির থাকে, প্রবাহিত হয় না",
                  "ঘর্ষণে সৃষ্টি হয়, যেমন চিরুনি ও কাগজ",
                  "বজ্রপাত এর সবচেয়ে বড় উদাহরণ"],
                 T_BODY, "#FFF6E5", AMBER, INK, AMBER)

    y2 = 430
    bot = 0
    for cx, name, col, items in (
            (760, "এসি (AC)", GREEN,
             ["নির্দিষ্ট নিয়মে দিক বদলায়",
              "মান প্রতি মুহূর্তে পরিবর্তনশীল",
              "বাসার সরবরাহ: ২৩০ V, ৫০ Hz"]),
            (1060, "ডিসি (DC)", RED,
             ["সব সময় একই দিকে প্রবাহিত",
              "মান নির্দিষ্ট থাকে",
              "ব্যাটারি, সোলার প্যানেল"])):
        s.path(f"M 910 {y1+52:.1f} L 910 {y2-46:.1f} L {cx:.1f} {y2-46:.1f} "
               f"L {cx:.1f} {y2-14:.1f}", STEEL, 2.4, marker=ar)
        s.box_auto(cx, y2 - 4, name, T_BODY, fill=col, stroke=col,
                   tcolor="#FFFFFF", pad_x=24, pad_y=11, min_w=200)
        bot = max(bot, bullet_panel(s, cx - 145, y2 + 56, 290, items, T_SMALL,
                                    GREENBG if col == GREEN else REDBG, col, INK, col))
    s.fit(bot, 24)
    return s.save(f"{OUT}/d02_types.svg")


def d03_current():
    """Electron drift inside a conductor vs conventional current direction."""
    s = SVG(1240, 620)
    s.title("পরিবাহীর ভেতরে ইলেকট্রন প্রবাহ ও কারেন্টের দিক", T_TITLE)
    ar_e = s.arrow_defs(STEEL, "are", 14)
    ar_c = s.arrow_defs(RED, "arc", 15)

    # battery
    s.rect(96, 258, 34, 130, "#3A4750", "#222C33", 2, 5)
    s.rect(96, 240, 34, 20, "#B7C1CB", "#7C8794", 2, 4)
    s.text(76, 262, "+", 30, RED, 700, "middle")
    s.text(76, 386, "−", 30, STEEL, 700, "middle")
    s.text(113, 470, "ব্যাটারি", T_SMALL, "#39434D", 600, "middle")
    # the loop is closed: − terminal into the conductor, load back to +
    s.path("M 113 388 L 113 418 L 145 418 L 145 323 L 160 323", NAVY, 3)
    s.path("M 1166 323 L 1204 323 L 1204 190 L 113 190 L 113 240", NAVY, 3)

    # conductor
    s.rect(160, 286, 900, 74, "#E5D3B3", "#B08C60", 2.4, 10)
    s.rect(160, 286, 900, 22, "#F0E3CB", "none", 0, 6)
    s.text(610, 262, "পরিবাহী (তামার তার)", T_SMALL, "#7A5200", 700, "middle")

    # lamp
    s.circle(1122, 323, 44, "#FFF3C4", "#B08C00", 2.6)
    s.path("M 1104 336 q 18 -34 36 0", "#B08C00", 3)
    s.text(1122, 400, "লোড", T_SMALL, "#39434D", 600, "middle")
    s.path("M 1060 300 L 1092 300", NAVY, 2.6)
    s.path("M 1060 346 L 1092 346", NAVY, 2.6)

    # electrons drifting
    for i in range(9):
        ex = 226 + i * 96
        s.circle(ex, 323, 15, STEEL, "#FFFFFF", 2.4)
        s.text(ex, 330, "−", 19, "#FFFFFF", 700, "middle")
        if i < 8:
            s.path(f"M {ex+22:.1f} 323 L {ex+64:.1f} 323", STEEL, 2.6, marker=ar_e)

    s.text(610, 404, "ইলেকট্রন প্রবাহ  →  ঋণাত্মক থেকে ধনাত্মক", T_BODY, STEEL, 700, "middle")
    s.path("M 890 452 L 330 452", RED, 3.4, marker=ar_c)
    s.text(610, 494, "প্রচলিত কারেন্টের দিক  ←  ধনাত্মক থেকে ঋণাত্মক",
           T_BODY, RED, 700, "middle")

    s.rect(60, 522, 1120, 72, "#EAF2FA", STEEL, 2, 11)
    s.text(620, 552, "ইলেকট্রন প্রবাহ ও প্রচলিত কারেন্টের দিক পরস্পর বিপরীত",
           T_NAME, NAVY, 700, "middle")
    s.text(620, 582, "হিসাবে ও সার্কিট ডায়াগ্রামে সব সময় প্রচলিত দিকই ধরা হয়",
           T_SMALL, GREY, 400, "middle")
    s.fit(594, 22)
    return s.save(f"{OUT}/d03_current.svg")


def d04_ac_dc():
    """AC sine wave with one cycle marked, next to a flat DC line."""
    s = SVG(1240, 760)
    s.title("এসি ও ডিসি তরঙ্গের পার্থক্য", T_TITLE)

    PT, PB = 112, 560          # panel top / bottom
    y0, h, w = 330, 92, 400

    def panel(px, label, col):
        s.rect(px - 54, PT, w + 128, PB - PT, "#FCFDFE", LINE, 1.8, 13)
        s.box_auto(px + w / 2, PT + 14, label, T_NAME, fill=col, stroke=col,
                   tcolor="#FFFFFF", pad_x=24, pad_y=10)
        s.path(f"M {px} {y0} L {px+w} {y0}", "#8D9AA8", 2.2)
        s.path(f"M {px} {y0-h-16} L {px} {y0+h+16}", "#8D9AA8", 2.2)
        s.text(px + w + 14, y0 - 12, "সময়", T_SMALL, GREY, 400)
        s.text(px + 12, y0 - h - 24, "মান", T_SMALL, GREY, 400)

    # ── AC
    xa = 150
    panel(xa, "এসি (AC)", GREEN)
    pts = [(xa + i, y0 - h * math.sin(2 * math.pi * i / 200)) for i in range(0, 401, 4)]
    s.path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts), GREEN, 3.6)
    s.path(f"M {xa} {y0+h+52} L {xa+200} {y0+h+52}", NAVY, 2.4)
    s.line(xa, y0 + h + 44, xa, y0 + h + 60, NAVY, 2.4)
    s.line(xa + 200, y0 + h + 44, xa + 200, y0 + h + 60, NAVY, 2.4)
    s.text(xa + 100, y0 + h + 92, "একটি সাইকেল", T_SMALL, NAVY, 700, "middle")

    # ── DC
    xd = 726
    panel(xd, "ডিসি (DC)", RED)
    s.path(f"M {xd} {y0-64} L {xd+w} {y0-64}", RED, 3.6)
    s.text(xd + w / 2, y0 + h + 92, "মান সব সময় একই", T_SMALL, NAVY, 700, "middle")

    s.rect(60, 596, 1120, 122, "#FFF6E5", AMBER, 2, 12)
    s.text(620, 632, "ফ্রিকোয়েন্সি = প্রতি সেকেন্ডে সম্পন্ন সাইকেলের সংখ্যা",
           T_NAME, "#7A5200", 700, "middle")
    s.text(620, 666,
           "বাংলাদেশে সরবরাহ ফ্রিকোয়েন্সি ৫০ হার্জ, অর্থাৎ প্রতি সেকেন্ডে ৫০টি সাইকেল",
           T_SMALL, "#7A5200", 400, "middle")
    s.text(620, 698, "একটি সাইকেলের সময় = ১ / ৫০ = ০.০২ সেকেন্ড",
           T_SMALL, "#7A5200", 400, "middle")
    s.fit(718, 22)
    return s.save(f"{OUT}/d04_ac_dc.svg")


def d05_ohm():
    """Ohm's law triangle beside the circuit it describes."""
    s = SVG(1240, 640)
    s.title("ওহমের সূত্র: V, I ও R-এর সম্পর্ক", T_TITLE)

    # circuit
    L, R_, T, B = 110, 540, 150, 400
    s.path(f"M {L} {T} L {R_} {T} L {R_} {B} L {L} {B} Z", NAVY, 3.4)
    s.rect(280, T - 22, 100, 44, "#FFFFFF", NAVY, 3, 4)          # resistor
    s.text(330, T + 8, "R", 30, NAVY, 700, "middle")
    s.rect(L - 17, 246, 34, 58, "#3A4750", "#222C33", 2, 5)      # battery
    s.rect(L - 17, 228, 34, 20, "#B7C1CB", "#7C8794", 2, 4)
    s.text(L - 44, 244, "+", 28, RED, 700, "middle")
    s.text(L - 44, 318, "−", 28, STEEL, 700, "middle")
    s.text(L - 66, 288, "V", 30, NAVY, 700, "middle")
    ar = s.arrow_defs(RED, "ar", 15)
    s.path(f"M 200 {T-30} L 268 {T-30}", RED, 3.2, marker=ar)
    s.text(234, T - 44, "I", 26, RED, 700, "middle")

    # triangle
    cx, top, half, hgt = 900, 176, 175, 260
    s.poly([(cx, top), (cx + half, top + hgt), (cx - half, top + hgt)],
           "#EAF2FA", NAVY, 3.4)
    s.line(cx - 88, top + 118, cx + 88, top + 118, NAVY, 3)
    s.line(cx, top + 118, cx, top + hgt, NAVY, 3)
    s.text(cx, top + 96, "V", 46, NAVY, 700, "middle")
    s.text(cx - 46, top + 200, "I", 40, STEEL, 700, "middle")
    s.text(cx + 46, top + 200, "R", 40, STEEL, 700, "middle")

    y = 486
    for i, (f, note) in enumerate((("V = I × R", "ভোল্টেজ নির্ণয়"),
                                   ("I = V / R", "কারেন্ট নির্ণয়"),
                                   ("R = V / I", "রোধ নির্ণয়"))):
        x = 110 + i * 356
        s.rect(x, y, 320, 84, "#F5F9FC", STEEL, 2, 11)
        s.text(x + 160, y + 40, f, 30, NAVY, 700, "middle")
        s.text(x + 160, y + 70, note, T_SMALL, GREY, 400, "middle")
    s.fit(y + 84, 24)
    return s.save(f"{OUT}/d05_ohm.svg")


def d06_resistance_factors():
    """The four things that set a conductor's resistance."""
    s = SVG(1240, 560)
    s.title("পরিবাহীর রোধ যেসব বিষয়ের উপর নির্ভর করে", T_TITLE)
    cards = [
        ("দৈর্ঘ্য", "L", "দৈর্ঘ্য বাড়লে রোধ বাড়ে", "R ∝ L", STEEL, "#EAF2FA"),
        ("প্রস্থচ্ছেদ", "A", "মোটা তারে রোধ কমে", "R ∝ 1/A", GREEN, GREENBG),
        ("উপাদান", "ρ", "তামার রোধ কম, লোহার বেশি", "R ∝ ρ", AMBER, AMBERBG),
        ("তাপমাত্রা", "t", "ধাতুতে তাপ বাড়লে রোধ বাড়ে", "", RED, REDBG),
    ]
    cw, gapx = 278, 22
    x0 = (1240 - (4 * cw + 3 * gapx)) / 2
    for i, (name, sym, desc, rel, col, bg) in enumerate(cards):
        x = x0 + i * (cw + gapx)
        s.rect(x, 96, cw, 300, bg, col, 2, 13)
        s.rect(x, 96, cw, 58, col, col, 2, 13)
        s.rect(x + 1, 144, cw - 2, 10, col, "none", 0, 0)
        s.text(x + cw / 2, 136, name, T_NAME, "#FFFFFF", 700, "middle")
        s.circle(x + cw / 2, 214, 38, "#FFFFFF", col, 3)
        s.text(x + cw / 2, 228, sym, 40, col, 700, "middle")
        for j, ln in enumerate(wrap(desc, cw - 44, T_SMALL, 400)):
            s.text(x + cw / 2, 290 + j * T_SMALL * 1.34, ln, T_SMALL,
                   "#2E3842", 400, "middle")
        s.text(x + cw / 2, 372, rel, T_BODY, col, 700, "middle")
    s.rect(60, 426, 1120, 74, "#F5F9FC", NAVY, 2, 12)
    s.text(620, 462, "R = ρ × L / A", 32, NAVY, 700, "middle")
    s.text(620, 492, "ρ = আপেক্ষিক রোধ · L = দৈর্ঘ্য · A = প্রস্থচ্ছেদের ক্ষেত্রফল",
           T_SMALL, GREY, 400, "middle")
    s.fit(500, 24)
    return s.save(f"{OUT}/d06_resistance_factors.svg")


def d07_capacitor_inductor():
    """Construction of a capacitor and of an inductor."""
    s = SVG(1240, 620)
    s.title("ক্যাপাসিটর ও ইন্ডাক্টরের গঠন", T_TITLE)

    # ── capacitor ─────────────────────────────────────────────────────────
    s.rect(70, 96, 540, 372, "#FCFDFE", LINE, 1.8, 14)
    s.box_auto(340, 110, "ক্যাপাসিটর", T_NAME, fill=STEEL, stroke=STEEL,
               tcolor="#FFFFFF", pad_x=26, pad_y=11)
    PL, PR, PT, PH = 268, 396, 216, 150          # plate x's, top, height
    s.rect(PL + 16, PT + 10, PR - PL - 32, PH - 20, "#E8EDF1", "#B9C4CE", 1.8, 3)
    s.text((PL + PR) / 2, PT + PH / 2 - 6, "ডাই-", 21, "#4A5561", 600, "middle")
    s.text((PL + PR) / 2, PT + PH / 2 + 20, "ইলেকট্রিক", 21, "#4A5561", 600, "middle")
    s.rect(PL - 11, PT, 22, PH, "#C57A2A", "#9A5A18", 2, 3)
    s.rect(PR - 11, PT, 22, PH, "#C57A2A", "#9A5A18", 2, 3)
    s.text(PL, PT - 16, "প্লেট", 22, "#7A5200", 700, "middle")
    s.text(PR, PT - 16, "প্লেট", 22, "#7A5200", 700, "middle")
    s.path(f"M {PL} {PT+PH/2} L 168 {PT+PH/2}", NAVY, 3)
    s.path(f"M {PR} {PT+PH/2} L 512 {PT+PH/2}", NAVY, 3)
    s.text(148, PT + PH / 2 + 9, "+", 30, RED, 700, "middle")
    s.text(532, PT + PH / 2 + 9, "−", 30, STEEL, 700, "middle")
    s.text(340, 424, "চার্জ সঞ্চয় করে · একক ফ্যারাড (F)", T_SMALL, NAVY, 600, "middle")

    # ── inductor ──────────────────────────────────────────────────────────
    s.rect(630, 96, 540, 372, "#FCFDFE", LINE, 1.8, 14)
    s.box_auto(900, 110, "ইন্ডাক্টর", T_NAME, fill=GREEN, stroke=GREEN,
               tcolor="#FFFFFF", pad_x=26, pad_y=11)
    CX0, CX1, CY, CH = 768, 1032, 268, 52        # core box
    s.rect(CX0, CY, CX1 - CX0, CH, "#B7C1CB", "#7C8794", 2, 6)
    n = 6
    step = (CX1 - CX0 - 24) / n
    s.clip_begin(CX0 - 4, CY - 62, CX1 - CX0 + 8, CH + 124)
    for i in range(n):
        cxx = CX0 + 12 + i * step
        s.path(f"M {cxx:.1f} {CY+CH-6:.1f} Q {cxx+step/2:.1f} {CY-56:.1f} "
               f"{cxx+step:.1f} {CY+CH-6:.1f}", "#C57A2A", 8)
    s.clip_end()
    s.path(f"M 700 {CY+CH/2:.1f} L {CX0} {CY+CH/2:.1f}", NAVY, 3)
    s.path(f"M {CX1} {CY+CH/2:.1f} L 1100 {CY+CH/2:.1f}", NAVY, 3)
    s.text(900, CY + CH + 46, "লোহার কোর", 22, "#4A5561", 600, "middle")
    s.text(900, 424, "চৌম্বক ক্ষেত্রে শক্তি জমায় · একক হেনরি (H)",
           T_SMALL, NAVY, 600, "middle")

    s.rect(70, 492, 1100, 72, "#FFF6E5", AMBER, 2, 11)
    s.text(620, 522, "ক্যাপাসিটর বৈদ্যুতিক ক্ষেত্রে, ইন্ডাক্টর চৌম্বক ক্ষেত্রে শক্তি সঞ্চয় করে",
           T_NAME, "#7A5200", 700, "middle")
    s.text(620, 552, "দুটিই AC সার্কিটে কারেন্টকে বাধা দেয়, তবে ভিন্ন উপায়ে",
           T_SMALL, "#7A5200", 400, "middle")
    s.fit(564, 22)
    return s.save(f"{OUT}/d07_capacitor_inductor.svg")


def d08_colour_code():
    """Conductor colours: IEC 60445 beside BNBC Table 8.1.2.

    The figure is captioned "IEC ও BNBC" in ch04.py, and the chapter's ⚠ box
    explains the blue-wire trap, so the picture has to show both systems.
    """
    s = SVG(1240, 700)
    s.title("পরিবাহীর রং সংকেত: IEC ও BNBC", T_TITLE)
    GY_ = "green-yellow"
    rows = [
        ("ফেজ (প্রথম)", "L বা L1", ("বাদামি", "#7A4A21"), ("লাল", "#C62828")),
        ("ফেজ (দ্বিতীয়)", "L2", ("কালো", "#232323"), ("হলুদ", "#F2C200")),
        ("ফেজ (তৃতীয়)", "L3", ("ধূসর", "#8D9AA8"), ("নীল", "#1E63B5")),
        ("নিউট্রাল", "N", ("নীল", "#1E63B5"), ("কালো", "#232323")),
        ("আর্থ", "PE", ("সবুজ-হলুদ", GY_), ("সবুজ-হলুদ", GY_)),
    ]
    x0, w = 60, 1120
    y = 104
    hrow = 70
    cols = {"name": x0 + 140, "sym": x0 + 340, "iec": x0 + 450, "bnbc": x0 + 790}
    s.rect(x0, y, w, 54, NAVY, NAVY, 2, 10)
    s.text(cols["name"], y + 36, "পরিবাহী", T_BODY, "#FFFFFF", 700, "middle")
    s.text(cols["sym"], y + 36, "চিহ্ন", T_BODY, "#FFFFFF", 700, "middle")
    s.text(cols["iec"] + 150, y + 36, "IEC 60445", T_BODY, "#FFFFFF", 700, "middle")
    s.text(cols["bnbc"] + 150, y + 36, "BNBC (সারণি ৮.১.২)", T_BODY, "#FFFFFF", 700, "middle")

    def swatch(x, yy, hexc):
        if hexc == GY_:
            s.rect(x, yy, 120, 38, "#2E8B31", "none", 0, 6)
            s.clip_begin(x, yy, 120, 38, 6)
            for k in range(6):
                s.path(f"M {x-12+k*26} {yy+44} L {x+20+k*26} {yy-4}", "#F2D200", 12)
            s.clip_end()
            s.rect(x, yy, 120, 38, "none", "#20621F", 2, 6)
        else:
            s.rect(x, yy, 120, 38, hexc, "#5A6470", 2, 6)

    yy = y + 62
    for name, sym, (ci, hi), (cb, hb) in rows:
        trap = ci == "নীল" or cb == "নীল"
        s.rect(x0, yy, w, hrow, "#FFF6E5" if trap else "#F7FAFC",
               AMBER if trap else LINE, 1.6, 9)
        my = yy + hrow / 2 + 8
        s.text(cols["name"], my, name, T_BODY, "#2E3842", 400, "middle")
        s.text(cols["sym"], my, sym, T_BODY, NAVY, 700, "middle")
        for cx_, cname, hexc in ((cols["iec"], ci, hi), (cols["bnbc"], cb, hb)):
            s.text(cx_ + 10, my, cname, T_BODY, "#2E3842", 600)
            swatch(cx_ + 170, yy + 16, hexc)
        yy += hrow + 8
    s.rect(x0, yy + 6, w, 72, REDBG, RED, 2, 11)
    s.text(x0 + w / 2, yy + 38, "নীল তার IEC-তে নিউট্রাল, কিন্তু BNBC-তে ফেজ",
           T_NAME, "#7A1810", 700, "middle")
    s.text(x0 + w / 2, yy + 68, "দুই নিয়মে মিল শুধু আর্থে: সবুজ-হলুদ",
           T_SMALL, "#7A1810", 400, "middle")
    s.fit(yy + 78, 24)
    return s.save(f"{OUT}/d08_colour_code.svg")


ALL = [d01_atom, d02_types, d03_current, d04_ac_dc, d05_ohm,
       d06_resistance_factors, d07_capacitor_inductor, d08_colour_code]

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
