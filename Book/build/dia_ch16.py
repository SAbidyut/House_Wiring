# -*- coding: utf-8 -*-
"""অধ্যায় ১৬ — পাওয়ার ফর্মুলা ও ক্যালকুলেশন : ডায়াগ্রাম।

এই অধ্যায়ের ছবিগুলোর কোনো সোর্স-স্লাইড নেই।  `Circuit Diagram.pptx`-এ
অ্যামিটার-ভোল্টমিটারের সংযোগ আছে, কিন্তু সেটা অধ্যায় ৮ নিয়ে নিয়েছে।
তাই সবই নতুন করে আঁকা — সরবরাহের গঠন, সূত্রচক্র, তরঙ্গের ফেজ পার্থক্য,
পাওয়ার ত্রিভুজ, স্টার-ডেল্টা ও হিসাবের ধাপ।

লেবেলের নিয়ম (অধ্যায় ১৫ থেকে কড়া):  প্যানেলের শিরোনাম বিশেষ্য, যন্ত্রাংশের
লেবেল এক-দুই শব্দ, নিচের নোট-পটিতে এক লাইনের একটি তথ্য।  কারণ ও ব্যাখ্যা
বইয়ের লেখায় থাকে, ছবিতে নয়।

দুটো ফন্ট-ফাঁদ এই অধ্যায়ে বিশেষভাবে খেয়াল রাখতে হয়েছে — Kalpurush-এ
`√`, `²`, `Ω`, `φ` কোনোটিই নেই (ফন্টের cmap দেখে যাচাই করা)।  তাই ছবিতে
বর্গ বা রুট লেখা হয়নি; `1.732` লেখা হয়েছে, আর বর্গের সূত্রগুলো বইয়ের
লেখায় `b.math()`-এর ভেতরে রাখা হয়েছে যেখানে OMML নিজেই চিহ্ন আঁকে।
"""
import math
import os

from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch16")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
LH = 1.42

SW = 3.4
LIVE = "#D42A1F"          # L / L1 — বিএনবিসি ১.৩.৯.৩.১৫
L2COL = "#C08A05"         # L2 — হলুদ
L3COL = "#1D5B8F"         # L3 — নীল
NEUT = "#1F2933"          # N — কালো
EARTH = "#1B6E47"
BOXG = "#E7ECF1"


# ── shared helpers ──────────────────────────────────────────────────────
def panel(s, x, y, w, h, title, col=STEEL):
    """প্যানেলের শিরোনাম — কেবল নাম, কোনো মন্তব্য নয়।"""
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def note_strip(s, y, text, x=46, w=1148, fill="#EAF2FA", stroke=STEEL,
               tcolor=NAVY, size=T_NAME):
    """এক লাইনের তথ্য-পটি।  দুই লাইনে গড়ালে লেখাটা ছোট করতে হবে —
    ছবির নিচে অনুচ্ছেদ বসানো এই বইয়ের নিয়ম নয়।"""
    if tw(text, size, 700) > w - 60:
        raise ValueError(f"note_strip এক লাইনে ধরে না: {text!r}")
    s.rect(x, y, w, 58, fill, stroke, 2, 11)
    s.text(x + w / 2, y + 36, text, size, tcolor, 700, "middle")
    return y + 58


def dim_span(s, x1, x2, y, label, col=STEEL, size=T_NAME, tick=13):
    """দুই তারের মাঝের ভোল্টেজ দেখানোর মাপ-রেখা।  লেখাটা রেখার উপরে বসে,
    তাই কোনো স্ট্রোক অক্ষরের ভেতর দিয়ে যায় না।"""
    s.line(x1, y - tick, x1, y + tick, col, 2)
    s.line(x2, y - tick, x2, y + tick, col, 2)
    s.line(x1, y, x2, y, col, 2)
    s.text((x1 + x2) / 2, y - tick - 12, label, size, NAVY, 700, "middle")


def sine(s, x0, y0, w, amp, cycles, phase_deg, col, sw=3.2, n=150):
    """সাইন তরঙ্গ — polyline, কারণ svgkit-এর path বিশ্লেষক প্রতিটি অংশকে
    রেখা হিসেবে ধরে, ফলে qc.py লেবেলের সঙ্গে সংঘর্ষ ধরতে পারে।"""
    pts = []
    for k in range(n + 1):
        t = k / n
        ang = 2 * math.pi * cycles * t - math.radians(phase_deg)
        pts.append((x0 + w * t, y0 - amp * math.sin(ang)))
    d = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    s.path(d, col, sw)
    return pts


# ── d01 — সিঙ্গেল ফেজ ও থ্রি-ফেজ সরবরাহ ─────────────────────────────────
def d01_supply():
    s = SVG(1240, 640)
    s.title("সিঙ্গেল ফেজ ও থ্রি-ফেজ সরবরাহ", T_TITLE)

    py, ph = 96, 424
    panel(s, 46, py, 560, ph, "সিঙ্গেল ফেজ", STEEL)
    panel(s, 634, py, 560, ph, "থ্রি-ফেজ", GREEN)

    # ── বাঁ প্যানেল ──
    s.rect(116, 178, 420, 32, STEEL, LINE, 1.6, 8)
    s.text(326, 201, "সাপ্লাই", T_BODY, "#FFFFFF", 700, "middle")

    xl, xn, wy0, wy1 = 236, 416, 210, 424
    s.line(xl, wy0, xl, wy1, LIVE, SW)
    s.line(xn, wy0, xn, wy1, NEUT, SW)
    s.text(xl - 20, 250, "L", T_NODE, LIVE, 700, "end")
    s.text(xn + 20, 250, "N", T_NODE, NEUT, 700, "start")
    dim_span(s, xl, xn, 330, "230 V")

    s.rect(196, 424, 260, 58, BOXG, STEEL, 2, 10)
    s.text(326, 461, "লোড", T_BODY, NAVY, 700, "middle")

    # ── ডান প্যানেল ──
    s.rect(704, 178, 420, 32, GREEN, LINE, 1.6, 8)
    s.text(914, 201, "সাপ্লাই", T_BODY, "#FFFFFF", 700, "middle")

    xs = [724, 824, 924, 1074]
    cols = [LIVE, L2COL, L3COL, NEUT]
    names = ["L1", "L2", "L3", "N"]
    for x, c in zip(xs, cols):
        s.line(x, wy0, x, wy1, c, SW)
    for x, c, nm in zip(xs, cols, names):
        # লেবেল তারের পাশে, তারের উপরে নয় — নইলে স্ট্রোক অক্ষর কেটে যায়
        s.text(x - 18, 406, nm, T_NODE, c, 700, "end")

    dim_span(s, xs[0], xs[1], 280, "400 V")
    dim_span(s, xs[2], xs[3], 352, "230 V")

    s.rect(684, 424, 440, 58, BOXG, GREEN, 2, 10)
    s.text(904, 461, "লোড", T_BODY, NAVY, 700, "middle")

    y = note_strip(s, py + ph + 24,
                   "বাংলাদেশে সিঙ্গেল ফেজ 230 V, থ্রি-ফেজ 400 V")
    s.fit(y, 22)
    return s.save(f"{OUT}/d01_supply.svg")


# ── d02 — সূত্রচক্র ─────────────────────────────────────────────────────
def d02_formulas():
    s = SVG(1240, 700)
    s.title("ভোল্টেজ, কারেন্ট, রেজিস্ট্যান্স ও পাওয়ারের সূত্র", T_TITLE)

    cards = [
        ("V", "ভোল্টেজ", "ভোল্ট (V)", ["V = I × R", "V = P / I"], STEEL),
        ("I", "কারেন্ট", "অ্যাম্পিয়ার (A)", ["I = V / R", "I = P / V"], LIVE),
        ("R", "রেজিস্ট্যান্স", "ওহম", ["R = V / I", "R = V × V / P"], NAVY),
        ("P", "পাওয়ার", "ওয়াট (W)", ["P = V × I", "P = I × I × R"], GREEN),
    ]

    CW, CH = 560, 214
    for i, (sym, name, unit, forms, col) in enumerate(cards):
        x = 46 + (i % 2) * 588
        y = 110 + (i // 2) * (CH + 26)
        s.rect(x, y, CW, CH, "#FCFDFE", LINE, 1.8, 13)
        s.badge(x + 54, y + 54, sym, 28, col, "#FFFFFF", T_NODE)
        s.text(x + 102, y + 64, name, T_NAME, NAVY, 700)
        s.text(x + CW - 28, y + 64, unit, T_SMALL, GREY, 400, "end")
        s.line(x + 24, y + 88, x + CW - 24, y + 88, LINE, 1.6)
        for j, f in enumerate(forms):
            s.text(x + 102, y + 132 + j * 44, f, T_NODE, INK, 600)

    y = note_strip(s, 110 + 2 * CH + 26 + 28,
                   "চারটি রাশির দুটি জানা থাকলে বাকি দুটি বের করা যায়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_formulas.svg")


# ── d03 — ভোল্টেজ ও কারেন্টের ফেজ পার্থক্য ──────────────────────────────
def d03_phase():
    s = SVG(1240, 580)
    s.title("ভোল্টেজ ও কারেন্টের ফেজ পার্থক্য", T_TITLE)

    py, ph = 96, 350
    panel(s, 46, py, 560, ph, "রেজিস্টিভ লোড", STEEL)
    panel(s, 634, py, 560, ph, "ইন্ডাকটিভ লোড", AMBER)

    # ভোল্টেজ ও কারেন্টের বিস্তার আলাদা রাখা হয়েছে ইচ্ছে করেই — সমান হলে
    # রেজিস্টিভ প্যানেলে দুটো রেখা হুবহু মিলে যায় আর একটাই দেখা যায়।
    for px, lag in ((46, 0), (634, 60)):
        ax0, aw, ay = px + 46, 468, 306
        amp_v, amp_i = 68, 48
        s.line(ax0, ay, ax0 + aw, ay, GREY, 1.8)

        # নমুনা রেখা ও নাম — তরঙ্গের নিচে, উপরে ফেজ-চিহ্নের জায়গা ছাড়তে
        s.line(px + 132, 420, px + 176, 420, NAVY, 3.2)
        s.text(px + 186, 428, "ভোল্টেজ", T_SMALL, NAVY, 700)
        s.line(px + 316, 420, px + 360, 420, LIVE, 3.2)
        s.text(px + 370, 428, "কারেন্ট", T_SMALL, LIVE, 700)

        sine(s, ax0, ay, aw, amp_v, 2, 0, NAVY)
        # ধনাত্মক lag মানে কারেন্টের চূড়া পরে আসে — ইন্ডাকটিভ লোডে যা হয়।
        # ঋণাত্মক দিলে কারেন্ট এগিয়ে যায়, যা ক্যাপাসিটিভ লোডের চিত্র।
        sine(s, ax0, ay, aw, amp_i, 2, lag, LIVE)

        if lag:
            # V ও I-এর প্রথম চূড়ার মাঝের দূরত্বই ফেজ পার্থক্য
            xv = ax0 + aw * (90 / 720.0)
            xi = ax0 + aw * ((90 + lag) / 720.0)
            top = ay - amp_v
            s.line(xv, top - 6, xv, top + 34, GREY, 1.8, dash="6 5")
            s.line(xi, top - 6, xi, top + 34, GREY, 1.8, dash="6 5")
            s.line(xv, top - 22, xi, top - 22, STEEL, 2)
            s.text((xv + xi) / 2, top - 34, "ফেজ পার্থক্য",
                   T_SMALL, NAVY, 700, "middle")

    y = note_strip(s, py + ph + 24,
                   "ইন্ডাকটিভ লোডে কারেন্ট ভোল্টেজের পেছনে পড়ে")
    s.fit(y, 22)
    return s.save(f"{OUT}/d03_phase.svg")


# ── d04 — পাওয়ার ত্রিভুজ ────────────────────────────────────────────────
def d04_triangle():
    s = SVG(1240, 660)
    s.title("পাওয়ার ত্রিভুজ", T_TITLE)

    # বাহুর অনুপাত cos φ = 0.8-এর — ভুজ 0.8, লম্ব 0.6।  ইচ্ছেমতো কোণ না
    # নিয়ে বইয়ের উদাহরণের মানটাই আঁকা হয়েছে, যাতে ছবি ও হিসাব মেলে।
    ox, oy, bx, ty = 320, 460, 760, 130
    s.line(ox, oy, bx, oy, GREEN, 5)          # kW
    s.line(bx, oy, bx, ty, AMBER, 5)          # kVAR
    s.line(ox, oy, bx, ty, NAVY, 5)           # kVA

    s.text((ox + bx) / 2, oy + 44, "kW", T_NODE, GREEN, 700, "middle")
    s.text((ox + bx) / 2, oy + 78, "প্রকৃত পাওয়ার", T_SMALL, INK, 400,
           "middle")

    s.text(bx + 26, (oy + ty) / 2 - 6, "kVAR", T_NODE, AMBER, 700, "start")
    s.text(bx + 26, (oy + ty) / 2 + 28, "রিঅ্যাকটিভ পাওয়ার", T_SMALL, INK,
           400, "start")

    s.text(470, 250, "kVA", T_NODE, NAVY, 700, "end")
    s.text(470, 284, "আপাত পাওয়ার", T_SMALL, INK, 400, "end")

    # ফেজ কোণের চাপ — লেবেলটা ত্রিভুজের বাইরে, লিডার দিয়ে যুক্ত
    r = 78
    ang = math.atan2(oy - ty, bx - ox)
    s.path(f"M {ox + r} {oy} A {r} {r} 0 0 0 "
           f"{ox + r * math.cos(ang):.1f} {oy - r * math.sin(ang):.1f}",
           STEEL, 2.6)
    s.text(ox - 34, oy + 40, "ফেজ কোণ", T_NAME, NAVY, 700, "end")
    s.path(f"M {ox - 28} {oy + 32} L {ox + 46} {oy - 20}", STEEL, 2.2)

    s.circle(ox, oy, 7, NAVY)

    y = note_strip(s, 570, "পাওয়ার ফ্যাক্টর হলো kW ও kVA-র অনুপাত")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_triangle.svg")


# ── d05 — স্টার ও ডেল্টা সংযোগ ──────────────────────────────────────────
def d05_star_delta():
    s = SVG(1240, 660)
    s.title("স্টার ও ডেল্টা সংযোগ", T_TITLE)

    py, ph = 96, 452
    panel(s, 46, py, 560, ph, "স্টার সংযোগ", STEEL)
    panel(s, 634, py, 560, ph, "ডেল্টা সংযোগ", GREEN)

    arms = [(90, LIVE, "L1"), (210, L2COL, "L2"), (330, L3COL, "L3")]

    # ── স্টার ──
    # তিন বাহু ৯০°, ২১০°, ৩৩০° — ফলে ২৭০° খালি থাকে, নিউট্রাল সেখান দিয়েই
    # নামে।  L1-এর লেবেল বাহুর পাশে, উপরে নয়: উপরে প্যানেলের শিরোনাম আছে।
    cx, cy, r = 326, 316, 104
    ends = {}
    for a, col, nm in arms:
        ex = cx + r * math.cos(math.radians(a))
        ey = cy - r * math.sin(math.radians(a))
        s.line(cx, cy, ex, ey, col, SW)
        ends[nm] = (ex, ey)
    s.line(cx, cy, cx, cy + r, NEUT, SW)
    s.circle(cx, cy, 7.5, NAVY)

    s.text(cx + 24, 200, "L1", T_NODE, LIVE, 700, "start")
    s.text(ends["L2"][0] - 18, ends["L2"][1] + 30, "L2", T_NODE, L2COL, 700,
           "end")
    s.text(ends["L3"][0] + 18, ends["L3"][1] + 30, "L3", T_NODE, L3COL, 700,
           "start")
    s.text(cx, cy + r + 36, "N", T_NODE, NEUT, 700, "middle")

    s.box_auto(196, 486, "ফেজ 230 V", T_SMALL, fill=LIGHT, stroke=STEEL)
    s.box_auto(452, 486, "লাইন 400 V", T_SMALL, fill=LIGHT, stroke=STEEL)

    # ── ডেল্টা ──
    dx, dy, dr, stub = 914, 316, 104, 44
    verts = {}
    for a, col, nm in arms:
        verts[nm] = (dx + dr * math.cos(math.radians(a)),
                     dy - dr * math.sin(math.radians(a)))
    order = ["L1", "L2", "L3"]
    for i in range(3):
        p, q = verts[order[i]], verts[order[(i + 1) % 3]]
        s.line(p[0], p[1], q[0], q[1], STEEL, SW)
    for a, col, nm in arms:
        vx, vy = verts[nm]
        s.line(vx, vy, dx + (dr + stub) * math.cos(math.radians(a)),
               dy - (dr + stub) * math.sin(math.radians(a)), col, SW)
        s.circle(vx, vy, 7.5, NAVY)

    s.text(dx + 24, 200, "L1", T_NODE, LIVE, 700, "start")
    s.text(verts["L2"][0] - 56, verts["L2"][1] + 52, "L2", T_NODE, L2COL, 700,
           "end")
    s.text(verts["L3"][0] + 56, verts["L3"][1] + 52, "L3", T_NODE, L3COL, 700,
           "start")

    s.box_auto(914, 486, "লাইন = ফেজ", T_SMALL, fill=LIGHT, stroke=STEEL)

    y = note_strip(s, py + ph + 24,
                   "স্টারে লাইন ভোল্টেজ ফেজ ভোল্টেজের 1.732 গুণ")
    s.fit(y, 22)
    return s.save(f"{OUT}/d05_star_delta.svg")


# ── d06 — কারেন্ট বের করার ধাপ ──────────────────────────────────────────
def d06_steps():
    s = SVG(1240, 460)
    s.title("লোড থেকে কারেন্ট বের করার ধাপ", T_TITLE)

    steps = [("১", "লোডের তালিকা"), ("২", "মোট ওয়াট"),
             ("৩", "BNBC গুণক"), ("৪", "পাওয়ার ফ্যাক্টর"),
             ("৫", "কারেন্ট")]
    CW, CH, GAP = 210, 186, 18
    ar = s.arrow_defs(STEEL, "ar", 14)

    for i, (num, name) in enumerate(steps):
        x = 46 + i * (CW + GAP)
        y = 112
        s.rect(x, y, CW, CH, "#FCFDFE", LINE, 1.8, 13)
        s.badge(x + CW / 2, y + 54, num, 27, NAVY, "#FFFFFF", T_NODE)
        for j, ln in enumerate(wrap(name, CW - 36, T_NAME, 700)):
            s.text(x + CW / 2, y + 116 + j * T_NAME * LH, ln, T_NAME, NAVY,
                   700, "middle")
        if i < len(steps) - 1:
            s.line(x + CW + 3, y + CH / 2, x + CW + GAP - 3, y + CH / 2,
                   STEEL, 2.4, marker=ar)

    y = note_strip(s, 112 + CH + 30,
                   "গুণক বাদ দিলে হিসাবের কারেন্ট বাস্তবের চেয়ে কম আসে",
                   fill=AMBERBG, stroke=AMBER, tcolor="#7A5200")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_steps.svg")


ALL = [d01_supply, d02_formulas, d03_phase, d04_triangle, d05_star_delta,
       d06_steps]

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
