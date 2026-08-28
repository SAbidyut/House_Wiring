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
T_HEAD = 26
T_NODE = 28
T_LBL = 25
T_NAME = 24.5
T_TAG = 22
T_BODY = 21.5
T_SMALL = 20
LH = 1.42

SYM = "#12324D"
SW = 3.2
BROWN = "#7A4A21"
BLUE = "#1E63B5"
EGREEN = "#2E8B31"
COPPER = "#B5713A"


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
# ── অধ্যায় ৬-এর নিজস্ব সহায়ক ─────────────────────────────────────────
def head_bar(s, x, y, w, h, text, col=STEEL, size=T_BODY, rx=13):
    """রঙিন শিরোনাম-পটি — নিচের কোনা চৌকো।

    দ্বিতীয় চৌকো আয়তটা `y + rx` থেকেই শুরু হবে, নইলে লেখাটা ওই আয়তের
    উপরের কিনারা ডিঙিয়ে যায় আর `qc.py` "box edge cuts" বলে ধরে ফেলে।
    তাই `rx` লেখার উচ্চতা দেখে নিজেই ছোট হয়ে যায় — পটি বেঁটে হলে
    গোল কোনা এমনিতেই বাদ পড়বে, লেখা কাটা পড়বে না।
    """
    rx = max(0, min(rx, int(h / 2 - 0.46 * size) - 1))
    s.rect(x, y, w, h, col, col, 2.2, rx)
    s.rect(x, y + rx, w, h - rx, col, "none", 0, 0)
    s.text(x + w / 2, y + h / 2 + size * 0.34, text, size, "#FFFFFF", 700,
           "middle")


def note_strip(s, y, text, size=T_NAME, pad=46):
    """এক লাইনের তথ্য-পটি।  দুই লাইনে গড়ালে এখানেই থেমে যায় — ছবির নিচে
    অনুচ্ছেদ বসানো এই বইয়ের নিয়ম নয়, ওটা বইয়ের লেখার কাজ।"""
    w = s.w - 2 * pad
    if tw(text, size, 700) > w - 60:
        raise ValueError(f"note_strip এক লাইনে ধরে না: {text!r}")
    s.rect(pad, y, w, 58, "#EAF2FA", STEEL, 2, 11)
    s.text(pad + w / 2, y + 36, text, size, NAVY, 700, "middle")
    return y + 58


def lead(s, x, y, text, tx, ty, anchor="middle", size=T_LBL, col=NAVY, gap=11):
    """লেবেল ও লিডার — বাক্সটা আগে মেপে, তার বাইরের কিনারা থেকে রেখা।

    অধ্যায় ২-এর শিক্ষা: লিডার সরাসরি লেখার নোঙরে টানলে সেটা নিজের
    লেখার ভেতর দিয়েই যায়; তাই মেপে ৯–১১ px দূরে থামাতে হয়।
    """
    s.text(x, y, text, size, col, 700, anchor)
    w = tw(text, size, 700)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle"
                                      else x - w)
    x1, y0, y1 = x0 + w, y - size * 0.80, y + size * 0.26
    if ty < y0 - 4:
        sx, sy = min(max(tx, x0 + 8), x1 - 8), y0 - gap
    elif ty > y1 + 4:
        sx, sy = min(max(tx, x0 + 8), x1 - 8), y1 + gap
    elif tx > x1:
        sx, sy = x1 + gap, (y0 + y1) / 2
    else:
        sx, sy = x0 - gap, (y0 + y1) / 2
    s.path(f"M {sx:.1f} {sy:.1f} L {tx:.1f} {ty:.1f}", STEEL, 2.2)
    s.circle(tx, ty, 5, STEEL)


def coil(s, x, y, w, h, turns=6):
    """ববিনে জড়ানো তামার কয়েল — দুই মাথায় ফ্ল্যাঞ্জ।"""
    s.rect(x - 5, y - 7, w + 10, 11, "#E3D6BC", "#A08E6C", 1.6, 3)
    s.rect(x - 5, y + h - 4, w + 10, 11, "#E3D6BC", "#A08E6C", 1.6, 3)
    s.rect(x, y, w, h, COPPER, "#7A4A21", 1.8, 4)
    for k in range(1, turns):
        xx = x + w * k / turns
        s.path(f"M {xx:.1f} {y+2:.1f} L {xx:.1f} {y+h-2:.1f}", "#8A5426", 2)


def spring(s, x, y0, y1, amp=13, n=5):
    """টানা স্প্রিং — লম্বা হলে টান বেশি, চোখেই ধরা পড়ে।"""
    d = [f"M {x} {y0}"]
    for i in range(1, n + 1):
        yy = y0 + (y1 - y0) * i / n
        d.append(f"L {x + (amp if i % 2 else -amp)} {yy:.1f}")
    d.append(f"L {x} {y1}")
    s.path(" ".join(d), "#5F6B77", 3.4)


def sound_arcs(s, cx, cy, r0=1.0, col="#B47500"):
    """গংয়ের গা থেকে ছড়ানো শব্দ-রেখা।"""
    for k, r in enumerate((46, 60, 74)):
        s.path(f"M {cx + r*0.35:.1f} {cy - r*0.72:.1f} "
               f"Q {cx + r:.1f} {cy:.1f} {cx + r*0.35:.1f} {cy + r*0.72:.1f}",
               col, 3.2 - k * 0.5)


# ═══════════════════════════════════════════════════════════════════════
def d01_bell_parts():
    """ট্রেম্বলিং বেল — বাঁয়ে গঠন, ডানে কেন একটানা বাজে।

    আগের সংস্করণে যন্ত্রটাই পড়া যেত না: ইলেকট্রোম্যাগনেট বসেছিল
    আর্মেচার থেকে অনেক দূরে, মাঝখানে শুধু একটা ফুটকি-রেখা; গং ছিল
    একটা ভাসমান অর্ধবৃত্ত; আর ভাঙা-জোড়ার চক্রটা ছবিতে কোথাও দেখানোই
    হয়নি — পাশে পাঁচ লাইনের বুলেট বসিয়ে বলে দেওয়া হয়েছিল, যেটা
    আবার বইয়ের লেখারই পুনরাবৃত্তি।

    এখন যন্ত্রটা সামনে থেকে দেখা — যেভাবে ঢাকনা খুললে চোখে পড়ে
    (চিত্র ৬.২-এর আসল ছবির সঙ্গে মিলিয়ে দেখা যায়): পিঠের প্লেটে
    ইউ-আকৃতির কোর, তার দুই বাহুতে দুটো কয়েল, উপরে সামান্য ফাঁক রেখে
    আর্মেচার, বাঁয়ে ক্ল্যাম্প-করা পাতা-স্প্রিং, তার উপর কন্টাক্ট
    স্ক্রু, ডানে হ্যামার ও গং।  ভেতরের তার আঁকা হয়নি — ওটা প্লেটের
    পেছনে থাকে, আর বর্তনীর কথা ডান প্যানেলেই বলা।
    """
    s = SVG(1240, 1000)
    s.title("বৈদ্যুতিক ঘণ্টার গঠন ও কার্যপ্রণালি", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 13)
    arR = s.arrow_defs(RED, "arR", 13)
    arG = s.arrow_defs(GREEN, "arG", 13)
    arA = s.arrow_defs(AMBER, "arA", 11)

    # ── প্যানেল ক : গঠন ────────────────────────────────────────────
    s.rect(46, 92, 1148, 470, "#FCFDFE", LINE, 1.8, 14)
    head_bar(s, 46, 92, 1148, 40, "গঠন", STEEL, T_HEAD)

    s.rect(196, 150, 856, 386, "#EEF2F6", "#9AA6B2", 2.6, 20)   # পিঠের প্লেট
    for hx, hy in ((224, 178), (1024, 178), (224, 508), (1024, 508)):
        s.circle(hx, hy, 9, "#DCE3EA", "#9AA6B2", 1.8)

    # স্তম্ভ, উপরের র‍্যাক ও ক্ল্যাম্প — এই তিনটেই স্থির কাঠামো
    s.rect(236, 200, 34, 316, "#B7C1CB", "#7C8794", 2.2, 4)
    s.rect(236, 200, 236, 24, "#B7C1CB", "#7C8794", 2.2, 4)
    s.rect(236, 282, 74, 30, "#A6B2BE", "#6B7684", 2.2, 4)

    # পাতা-স্প্রিং — দুই পাতার গোছা, ক্ল্যাম্প থেকে আর্মেচার পর্যন্ত
    s.path("M 310 297 Q 352 286 394 297", "#5F6B77", 12)
    s.path("M 318 307 Q 352 298 386 307", "#8D9AA8", 6)

    # আর্মেচার — নরম লোহার পাত, দুই খুঁটির উপরে সামান্য ফাঁক রেখে
    s.rect(394, 284, 292, 26, "#8D9AA8", "#5F6B77", 2.4, 3)

    # কন্টাক্ট স্ক্রু — র‍্যাক থেকে নেমে আর্মেচারের গায়ে ঠেকে থাকে
    s.rect(412, 212, 17, 72, "#B7C1CB", "#6B7684", 2, 2)
    for ty_ in (232, 248, 264):
        s.path(f"M 412 {ty_} L 429 {ty_}", "#7C8794", 1.8)
    s.circle(420, 200, 17, "#C6D0DA", "#5F6B77", 2.4)
    s.path("M 409 200 L 431 200", "#5F6B77", 2.4)
    s.circle(420, 286, 7, GREEN)                                # ছোঁয়ার বিন্দু

    # ইউ-কোর ও তার দুই বাহুর কয়েল
    s.rect(448, 348, 52, 88, "#B7C1CB", "#7C8794", 2.2, 3)
    s.rect(572, 348, 52, 88, "#B7C1CB", "#7C8794", 2.2, 3)
    s.rect(448, 436, 176, 34, "#B7C1CB", "#7C8794", 2.2, 3)
    coil(s, 426, 360, 96, 68)
    coil(s, 550, 360, 96, 68)

    # এয়ার গ্যাপ — আর্মেচারের তলা আর খুঁটির মাথার মাঝের ফাঁক।  ফাঁকটা
    # রং দিয়ে ভরে দেখানো হয়েছে; কেবল একটা ছোট তির দিলে চোখেই পড়ে না।
    s.rect(448, 310, 176, 38, "#FFF3D6", AMBER, 1.8, 0, dash="7,6")
    s.line(536, 316, 536, 342, AMBER, 2.6, marker=arA)
    s.line(536, 342, 536, 316, AMBER, 2.6, marker=arA)

    # হ্যামার ও গং
    s.path("M 686 297 L 800 310", "#8D9AA8", 11)
    s.circle(814, 312, 20, "#8D9AA8", "#5F6B77", 2.4)
    s.circle(940, 336, 86, "#B7C1CB", "#6B7684", 3.2)
    s.circle(940, 336, 66, "#CBD5DE", "#9AA6B2", 1.6)
    s.circle(940, 336, 13, "#8D9AA8", "#5F6B77", 2.2)
    s.path("M 931 336 L 949 336", "#4E5A66", 2.4)

    # টার্মিনাল ব্লক — সরবরাহের তার এখানেই লাগে
    s.rect(700, 476, 170, 44, "#E7ECF1", "#7C8794", 2.2, 5)
    for sx_ in (742, 828):
        s.circle(sx_, 498, 13, "#C6D0DA", "#5F6B77", 2)
        s.path(f"M {sx_-8} 498 L {sx_+8} 498", "#5F6B77", 2.2)

    # লেবেল
    lead(s, 492, 196, "কন্টাক্ট স্ক্রু", 430, 250, "start")
    lead(s, 600, 254, "আর্মেচার", 600, 285)
    lead(s, 352, 362, "স্প্রিং", 352, 303)
    lead(s, 644, 338, "এয়ার গ্যাপ", 600, 330, "start")
    lead(s, 400, 508, "ইলেকট্রোম্যাগনেট", 424, 430)
    lead(s, 664, 456, "লোহার কোর", 610, 452, "start")
    lead(s, 800, 250, "হ্যামার", 760, 305)
    lead(s, 940, 236, "গং", 940, 266)
    lead(s, 855, 460, "টার্মিনাল", 828, 498)

    # ── প্যানেল খ : কার্যপ্রণালি ───────────────────────────────────
    s.rect(46, 586, 1148, 268, "#FCFDFE", LINE, 1.8, 14)
    head_bar(s, 46, 586, 1148, 40, "কার্যপ্রণালি", GREEN, T_HEAD)

    def state(X, Y, title, live):
        """এক অবস্থার ছোট ছবি।  `live` — কারেন্ট চলছে কি না।"""
        W_, H_ = 484, 200
        s.rect(X, Y, W_, H_, "#FCFDFE", LINE, 1.8, 12)
        head_bar(s, X, Y, W_, 34, title, STEEL if live else GREY, T_TAG, 11)
        ay = Y + 86 if live else Y + 118          # আর্মেচারের উপরের কিনারা

        # স্থির অংশ — কোর, কয়েল, গং
        s.rect(X + 152, Y + 132, 92, 46, "#B7C1CB", "#7C8794", 2, 3)
        coil(s, X + 142, Y + 140, 112, 30, 5)
        s.circle(X + 400, Y + 132, 34, "#B7C1CB", "#6B7684", 2.6)
        s.circle(X + 400, Y + 132, 24, "#CBD5DE", "#9AA6B2", 1.4)

        # ব্র্যাকেট, স্প্রিং ও কন্টাক্ট স্ক্রু (স্ক্রুর দৈর্ঘ্য বদলায় না)
        s.rect(X + 98, Y + 40, 30, 12, "#B7C1CB", "#7C8794", 1.8, 3)
        s.rect(X + 152, Y + 40, 40, 12, "#B7C1CB", "#7C8794", 1.8, 3)
        spring(s, X + 113, Y + 52, ay, 11, 5)
        s.rect(X + 167, Y + 52, 10, 34, "#B7C1CB", "#6B7684", 1.8, 2)

        # আর্মেচার, হ্যামার
        s.rect(X + 96, ay, 200, 14, "#8D9AA8", "#5F6B77", 2, 3)
        s.path(f"M {X+296} {ay+7} L {X+348} {ay+10}", "#8D9AA8", 6)
        s.circle(X + 357, ay + 11, 11, "#8D9AA8", "#5F6B77", 2)

        if live:
            s.circle(X + 172, Y + 88, 6, GREEN)
            s.line(X + 276, ay + 24, X + 276, ay + 46, RED, 3, marker=arR)
            s.text(X + 288, ay + 44, "টান", T_TAG, RED, 700)
        else:
            s.path(f"M {X+156} {Y+90} L {X+188} {Y+90}", RED, 3)
            s.path(f"M {X+156} {Y+118} L {X+188} {Y+118}", RED, 3)
            s.line(X + 276, ay - 8, X + 276, ay - 30, GREEN, 3, marker=arG)
            s.text(X + 288, ay - 14, "ফেরত", T_TAG, GREEN, 700)
            sound_arcs(s, X + 428, Y + 132)

        # কারেন্টের পথ — কয়েলের নিচে একটা ইউ
        col_ = GREEN if live else GREY
        s.path(f"M {X+142} {Y+178} L {X+142} {Y+188} L {X+254} {Y+188} "
               f"L {X+254} {Y+178}", col_, 3.4,
               dash=None if live else "7,6")
        if live:
            s.line(X + 176, Y + 188, X + 216, Y + 188, GREEN, 3.4, marker=arG)
        else:
            s.path(f"M {X+188} {Y+180} L {X+208} {Y+196}", RED, 3.4)
            s.path(f"M {X+208} {Y+180} L {X+188} {Y+196}", RED, 3.4)
        s.text(X + 270, Y + 194, "কারেন্ট চলছে" if live else "কারেন্ট বন্ধ",
               T_TAG, GREEN if live else GREY, 700)

    state(82, 630, "১ · কন্টাক্ট লাগানো", True)
    state(674, 630, "২ · কন্টাক্ট ছোটা", False)

    # দুই অবস্থার চক্র
    s.path("M 592 706 A 40 40 0 0 1 648 706", STEEL, 3.4, marker=ar)
    s.path("M 648 774 A 40 40 0 0 1 592 774", STEEL, 3.4, marker=ar)
    s.text(620, 668, "চক্র", T_TAG, NAVY, 700, "middle")

    y = note_strip(s, 872, "কয়েল, কোর আর গং স্থির — নড়ে কেবল "
                           "আর্মেচার ও হ্যামার")
    s.fit(y, 22)
    return s.save(f"{OUT}/d01_bell_parts.svg")


def d02_bell_types():
    """বাজারের যন্ত্র — ছয়টা আসল আলোকচিত্র, ছয়টা টাইলে।

    আগের সংস্করণে চারটে টাইলেই ছিল প্রতীক, আর তিনটে প্রতীক প্রায় একই
    রকম দেখতে — বই থেকে চিনে বাজারে গিয়ে কেউ ধরতে পারত না।  ছবিগুলো
    উইকিমিডিয়া কমন্স থেকে (`assets_ch06.py`), কৃতজ্ঞতা অধ্যায়ের
    শেষের ❖ চিত্রসূত্র বাক্সে।
    """
    items = [
        ("ph_bell_gong.jpg", "ট্রেম্বলিং বেল", "একটানা বাজে"),
        ("ph_bell_open.jpg", "খোলা ট্রেম্বলিং বেল", "কয়েল, আর্মেচার, গং"),
        ("ph_single.jpg", "সিঙ্গেল স্ট্রোক বেল", "এক চাপে এক আঘাত"),
        ("ph_buzzer.jpg", "বাজার", "গং নেই, কম্পনে শব্দ"),
        ("ph_chime.jpg", "ইলেকট্রনিক চাইম", "সুরেলা শব্দ"),
        ("ph_alarm.jpg", "ফায়ার অ্যালার্ম বেল", "বড় গং, জোরালো শব্দ"),
    ]
    W_, M, GAP, IH, COLS = 1240, 26, 16, 250, 3
    tile = (W_ - 2 * M - GAP * (COLS - 1)) / COLS
    s = SVG(W_, 1000)
    s.title("বেল, বাজার ও চাইম — বাস্তবের যন্ত্র", T_TITLE)
    for i, (img, name, role) in enumerate(items):
        x = M + (i % COLS) * (tile + GAP)
        top = 100 + (i // COLS) * (IH + 84 + 24)
        s.rect(x, top, tile, IH + 84, "#F4F7FA", LINE, 1.8, 11)
        s.rect(x + 9, top + 8, tile - 18, IH - 10, "#FFFFFF", LINE, 1.2, 7)
        s.image_fit(x + 12, top + 11, tile - 24, IH - 16, f"{IMG}/{img}", 3)
        # ১৫.২ সেমিতে বসানো ১২৪০ px ক্যানভাসে ২৩ px ≈ ৮.০ pt — সবচেয়ে
        # ছোট লেখাটাও ছাপায় ৭.৫ pt-এর নিচে নামে না
        for txt, dy, size, colr in ((name, 36, 27.5, NAVY),
                                    (role, 68, 23, GREY)):
            if tw(txt, size, 700) > tile - 14:
                raise ValueError(f"d02: টাইলে ধরে না — {txt!r}")
            s.text(x + tile / 2, top + IH + dy, txt, size, colr, 700, "middle")
    y = note_strip(s, 100 + 2 * (IH + 108) + 20,
                   "বাইরে থেকে ট্রেম্বলিং আর সিঙ্গেল স্ট্রোক বেল "
                   "প্রায় একই রকম দেখায়", pad=M)
    s.fit(y, 24)
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
