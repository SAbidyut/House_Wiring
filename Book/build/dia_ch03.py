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
T_NAME = 25.5
T_BODY = 23
T_SMALL = 22.5
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
    s = SVG(1240, 640)
    s.title("একটি আদর্শ বৈদ্যুতিক সার্কিটের উপাদান", T_TITLE)
    L, R_, T, B = 250, 900, 210, 430
    cx = (L + R_) / 2
    s.path(f"M {L} {T} L {cx-26} {T}", SYM, SW)
    s.path(f"M {cx+26} {T} L {R_} {T}", SYM, SW)
    s.path(f"M {R_} {T} L {R_} {B-24}", SYM, SW)
    s.path(f"M {R_} {320-24+48} L {R_} {B}", SYM, SW)
    s.path(f"M {R_} {B} L {L} {B}", SYM, SW)
    s.path(f"M {L} {B} L {L} {340}", SYM, SW)
    s.path(f"M {L} {300} L {L} {T}", SYM, SW)
    sym_switch(s, cx, T)
    sym_lamp(s, R_, 320)
    for dy, ww in ((-20, 34), (-7, 18), (7, 34), (20, 18)):
        s.path(f"M {L-ww/2} {320+dy} L {L+ww/2} {320+dy}", SYM, 3.4)

    labels = [("উৎস (Source)", "বিদ্যুৎ সরবরাহ করে", L, 320, "end", -60),
              ("সুইচ (Control)", "সার্কিট চালু-বন্ধ করে", cx, T, "middle", -70),
              ("লোড (Load)", "বিদ্যুৎ ব্যবহার করে", R_, 320, "start", 60),
              ("পরিবাহী (Conductor)", "বিদ্যুৎ বহন করে", cx, B, "middle", 44)]
    for name, sub, px, py, anc, off in labels:
        if anc == "middle":
            tx, ty = px, py + off
        else:
            tx, ty = px + off, py
        s.text(tx, ty, name, T_BODY, NAVY, 700, anc)
        s.text(tx, ty + 28, sub, T_SMALL, GREY, 400, anc)

    s.rect(60, 522, 1120, 72, "#EAF2FA", STEEL, 2, 11)
    s.text(620, 552, "চারটি উপাদানের যেকোনো একটি না থাকলে সার্কিট অসম্পূর্ণ থাকে",
           T_NAME, NAVY, 700, "middle")
    s.text(620, 582, "উৎস → পরিবাহী → সুইচ → লোড → আবার উৎসে ফিরে আসা",
           T_SMALL, GREY, 400, "middle")
    s.fit(594, 22)
    return s.save(f"{OUT}/d01_circuit_parts.svg")


def d02_circuit_states():
    s = SVG(1240, 600)
    s.title("সার্কিটের তিন অবস্থা", T_TITLE)
    pw, gapx = 372, 34
    x0 = (1240 - (3 * pw + 2 * gapx)) / 2
    states = [
        ("ক্লোজ সার্কিট", GREEN, "সুইচ অন, সার্কিট সম্পূর্ণ, বাতি জ্বলে", "close"),
        ("ওপেন সার্কিট", AMBER, "সুইচ অফ বা তার ছেঁড়া, কারেন্ট চলে না", "open"),
        ("শর্ট সার্কিট", RED, "দুই তার সরাসরি লেগে যাওয়া, বিপজ্জনক", "short"),
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
            s.path(f"M {cx-72} {T} L {cx-72} {B}", RED, 4.4)
            # লেবেলটা লাইনের ডানপাশে — শর্ট পথ আর বাতির মাঝের ফাঁকা
            # জায়গাটাই এখানে একমাত্র জায়গা যেখানে লেখা কোনো তারের
            # গায়ে পড়ে না
            s.text(cx - 58, (T + B) / 2 - 12, "শর্ট পথ", T_SMALL, RED, 700, "start")
            s.text(cx - 58, (T + B) / 2 + 16, "রোধ প্রায় শূন্য", T_SMALL - 1,
                   "#9A4038", 400, "start")
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
                for a in (0, 45, 135, 180, 225, 315):   # none on the wire's own axis
                    r = math.radians(a)
                    s.path(f"M {R_+26*math.cos(r):.1f} {(T+B)/2+26*math.sin(r):.1f} "
                           f"L {R_+36*math.cos(r):.1f} {(T+B)/2+36*math.sin(r):.1f}",
                           "#E8A33D", 3)
            else:
                s.path(f"M {cx-26} {T} L {cx+20} {T-26}", SYM, SW)
                sym_lamp(s, R_, (T + B) / 2, 20)
        for j, ln in enumerate(wrap(note, pw - 40, T_SMALL, 400)):
            s.text(cx, 382 + j * T_SMALL * 1.34, ln, T_SMALL, "#39434D", 400, "middle")
    s.rect(60, 452, 1120, 72, REDBG, RED, 2, 11)
    s.text(620, 482, "শর্ট সার্কিটে রোধ প্রায় শূন্য হয়ে কারেন্ট বহুগুণ বেড়ে যায়",
           T_NAME, "#7A1810", 700, "middle")
    s.text(620, 512, "ফলে তার গরম হয়ে পুড়ে যায়; এ কারণেই ফিউজ ও ব্রেকার লাগে",
           T_SMALL, "#7A1810", 400, "middle")
    s.fit(524, 22)
    return s.save(f"{OUT}/d02_circuit_states.svg")


# ── হোল্ডার : আসল ছবি + বসানোর ধরন ──────────────────────────────────
T_TILE = 23          # টাইলের নাম     → 23 × 436.5 / 1240 ≈ ৮.১ পয়েন্ট
T_TSUB = 22          # টাইলের উপশিরোনাম → ≈ ৭.৪ পয়েন্ট

WOOD = "#C8A272"     # কাঠের বোর্ড / ছাদের পাটাতন
WOODL = "#8A6437"
SHELL = "#EDF1F4"    # হোল্ডারের সাদা খোল
SHELLL = "#7C8794"
BRASS = "#C79A2E"


def _hatch_slab(s, x, y, w, h, fill=WOOD, stroke=WOODL):
    """ছাদ, বোর্ড বা দেয়াল — তেরছা দাগ দিয়ে গাঁথুনি বোঝানো।"""
    s.rect(x, y, w, h, fill, stroke, 2, 3)
    step = 22
    d = min(w, h)
    for i in range(int((w + h) / step) + 1):
        x0 = x + i * step
        x1, y1 = x0 - h, y + h
        if x0 > x + w:
            x0, yy0 = x + w, y + (x0 - (x + w))
        else:
            yy0 = y
        if x1 < x:
            y1 = y + h - (x - x1)
            x1 = x
        if x0 > x1:
            s.path(f"M {x0} {yy0} L {x1} {y1}", stroke, 1.1)
    return d


def _lamp_unit(s, bx, by, ang=0.0, sc=1.0, plate=True, cap="pin", body=True):
    """হোল্ডার + বাতি, যেকোনো কোণে।

    স্থানীয় স্থানাঙ্কে +y মানে বাতির দিক; `ang` ঘোরালে গোটা জিনিসটা
    সেই কোণে বসে (ang = -45 → নিচে-ডানে, অ্যাঙ্গেল হোল্ডারের মতো)।
    """
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)

    def P(lx, ly):
        lx, ly = lx * sc, ly * sc
        return (bx + lx * ca - ly * sa, by + lx * sa + ly * ca)

    if plate:
        s.poly([P(-33, 0), P(33, 0), P(33, 10), P(-33, 10)], SHELL, SHELLL, 2)
    if body:
        s.poly([P(-25, 8), P(25, 8), P(22, 45), P(-22, 45)], SHELL, SHELLL, 2.2)
    s.poly([P(-24, 45), P(24, 45), P(24, 55), P(-24, 55)], "#DCE3E9", SHELLL, 2)
    if cap == "screw":
        for k in range(3):
            s.path("M %.1f %.1f L %.1f %.1f" % (P(-15, 47 + k * 4) +
                                                P(15, 49 + k * 4)), BRASS, 2.4)
    else:
        for dx in (-16, 16):
            s.poly([P(dx - 4, 46), P(dx + 4, 46), P(dx + 4, 55), P(dx - 4, 55)],
                   BRASS, "none", 0)
    cx, cy = P(0, 90)
    s.circle(cx, cy, 27 * sc, "#FFF3C4", "#B08C00", 2.4)
    s.path(f"M {cx-12*sc:.1f} {cy+6*sc:.1f} Q {cx:.1f} {cy-14*sc:.1f} "
           f"{cx+12*sc:.1f} {cy+6*sc:.1f}", "#B08C00", 2.4)
    return P


def _angle_holder(s, wx, py, ang=-46.0):
    """অ্যাঙ্গেল হোল্ডার — দেয়ালের গায়ে গোল গোড়া, মুখ কোণ করে কাটা।

    `_lamp_unit()` দিয়ে এটি আঁকা যায় না।  ওটি সোজা খোলের হোল্ডার —
    কাঁধ, বলয়, বাতি এক অক্ষে।  অ্যাঙ্গেল হোল্ডারের গোড়া আর মুখ **এক
    অক্ষে নয়**:  গোড়াটা দেয়ালের সমতলে, মুখটা তার সঙ্গে কোণ করে।  তাই
    গোটা দেহটা এখানে একটাই বদ্ধ পথ — দেয়াল থেকে বেরিয়ে ফুলে উঠে কোণ
    করা মুখে গিয়ে শেষ — আর মুখের কলার, পিতলের বলয় ও বাতি তার উপরে।
    """
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    ux, uy = -sa, ca                       # মুখ যেদিকে তাকিয়ে
    px_, py_ = ca, sa                      # মুখের আড়াআড়ি

    wf = wx + 26                           # দেয়ালের সামনের তল
    bx, by = wf + 42, py + 134             # মুখের কেন্দ্র
    hw = 27                                # মুখের অর্ধ-প্রস্থ

    m1 = (bx + hw * px_, by + hw * py_)
    m2 = (bx - hw * px_, by - hw * py_)

    def off(pt, d):
        return (pt[0] + d * ux, pt[1] + d * uy)

    # দেয়ালে আটকানোর পাত — দেহের আগে, আর দেহের চেয়ে একটু লম্বা, তাই
    # উপরে-নিচে সামান্য বেরিয়ে থেকে পাত বলেই চেনা যায়
    s.rect(wf - 2, py + 88, 13, 90, "#DCE3E9", SHELLL, 2, 4)
    # দেহ — দেয়াল থেকে বেরিয়ে ফুলে উঠে কোণ করা মুখে শেষ
    s.path(f"M {m1[0]:.1f} {m1[1]:.1f} "
           f"C {wx+82} {py+94} {wx+50} {py+92} {wf} {py+98} "
           f"L {wf} {py+168} "
           f"C {wx+34} {py+170} {wx+44} {py+162} {m2[0]:.1f} {m2[1]:.1f} Z",
           SHELLL, 2.2, SHELL)
    # মুখের কলার
    s.poly([m1, off(m1, 19), off(m2, 19), m2], "#DCE3E9", SHELLL, 2)
    # ভেতরের পিতলের বলয়
    s.poly([off(m1, 6), off(m1, 12), off(m2, 12), off(m2, 6)], BRASS, "none", 0)
    # বাতি
    cbx, cby = off((bx, by), 44)
    s.circle(cbx, cby, 26, "#FFF3C4", "#B08C00", 2.4)
    s.path(f"M {cbx-12:.1f} {cby+6:.1f} Q {cbx:.1f} {cby-14:.1f} "
           f"{cbx+12:.1f} {cby+6:.1f}", "#B08C00", 2.4)
    return cbx + 26


def d03_holders():
    """চিত্র ৩.৩ — উপরের সারিতে আসল হোল্ডার, নিচের সারিতে কে কোথায় বসে।

    আগের সংস্করণে চারটি হোল্ডারই হাতে আঁকা ছিল এবং চারটি দেখতে প্রায়
    এক — শিক্ষার্থী বাজারে গিয়ে ওগুলো চিনত না।  ছবিগুলো এখন
    ইনস্টিটিউটের নিজের নথি থেকে নেওয়া আসল আলোকচিত্র (`assets_ch03.py`);
    আঁকা থাকে কেবল সেটুকু, ছবি যা দেখাতে পারে না — কোন হোল্ডার ছাদে
    বসে, কোনটা দেয়ালে কোণ করে, কোনটা সিলিং রোজ থেকে ঝোলে।
    """
    s = SVG(1240, 960)
    s.title("হোল্ডার: আসল চেহারা ও বসানোর ধরন", T_TITLE)

    # ── সারি ১ : আসল ছবি ───────────────────────────────────────────
    s.box_auto(620, 92, "আসল হোল্ডার", T_NAME, fill=STEEL, stroke=STEEL,
               tcolor="#FFFFFF", pad_x=26, pad_y=9)
    # নাম থেকে “হোল্ডার” শব্দটা বাদ — ছবির শিরোনামেই আছে, আর পাঁচটা
    # টাইলে ওটা রাখলে লেখা টাইলের বাইরে চলে যায়
    photos = [
        ("ph_batten_pin.jpg", "ব্যাটেন", "পিন (BC)"),
        ("ph_batten_screw.jpg", "ব্যাটেন", "প্যাঁচ (ES)"),
        ("ph_angle.jpg", "অ্যাঙ্গেল", "পিন (BC)"),
        ("ph_pendant_pin.jpg", "পেন্ডেন্ট", "পিন (BC)"),
        ("ph_pendant_screw.jpg", "পেন্ডেন্ট", "প্যাঁচ (ES)"),
    ]
    m, gap, well = 22, 15, 196
    tile = (1240 - 2 * m - gap * (len(photos) - 1)) / len(photos)
    top = 150
    for i, (img, name, sub) in enumerate(photos):
        x = m + i * (tile + gap)
        s.rect(x, top, tile, well + 82, "#F7FAFC", LINE, 1.8, 12)
        s.rect(x + 11, top + 9, tile - 22, well - 12, "#FFFFFF", LINE, 1.2, 8)
        s.image_fit(x + 15, top + 12, tile - 30, well - 18, f"{IMG}/{img}", 3)
        for txt, dy, size, col, wt in ((name, well + 26, T_TILE, NAVY, 700),
                                       (sub, well + 58, T_TSUB, GREY, 400)):
            if tw(txt, size, wt) > tile - 14:
                raise ValueError(f"d03: টাইলে ধরে না — {txt!r}")
            s.text(x + tile / 2, top + dy, txt, size, col, wt, "middle")

    # ── সারি ২ : কোথায় কীভাবে বসে ──────────────────────────────────
    s.box_auto(620, 470, "বসানোর ধরন", T_NAME, fill=GREEN, stroke=GREEN,
               tcolor="#FFFFFF", pad_x=26, pad_y=9)
    pw, pgap = (1240 - 2 * m - 2 * 20) / 3, 20
    py, ph = 528, 292
    kinds = [("ব্যাটেন হোল্ডার", "ছাদ বা কাঠের বোর্ডে সোজা", "batten"),
             ("অ্যাঙ্গেল হোল্ডার", "দেয়ালে কোণ করে, বাতি নিচে", "angle"),
             ("পেন্ডেন্ট হোল্ডার", "সিলিং রোজ থেকে ঝুলন্ত", "pendant")]
    for i, (name, role, kind) in enumerate(kinds):
        x = m + i * (pw + pgap)
        s.rect(x, py, pw, ph, "#FCFDFE", LINE, 1.8, 13)
        cx = x + pw / 2
        s.text(cx, py + 34, name, T_TILE, NAVY, 700, "middle")

        if kind == "batten":
            # তার ছাদের ভেতর দিয়ে এসে পাতের নিচে ঢোকে — বাইরে থেকে
            # কিছুই দেখা যায় না, তাই আঁকাও নেই
            _hatch_slab(s, cx - 122, py + 54, 244, 24)
            _lamp_unit(s, cx, py + 78, 0, 0.94)

        elif kind == "angle":
            # দেয়ালটা প্যানেলের বাঁয়ে নয়, গোটা জিনিসটা যাতে মাঝখানে বসে
            wx = cx - 66
            _hatch_slab(s, wx, py + 62, 26, 148)
            _angle_holder(s, wx, py)

        else:
            _hatch_slab(s, cx - 122, py + 54, 244, 24)
            # সিলিং রোজ — ছাদের গায়ে চ্যাপ্টা গোল বাক্স
            s.path(f"M {cx-36} {py+78} A 36 36 0 0 0 {cx+36} {py+78} Z",
                   SHELLL, 2, SHELL)
            s.path(f"M {cx-36} {py+78} L {cx+36} {py+78}", SHELLL, 2)
            # সিলিং রোজের নাম প্যানেলের নিচের লাইনেই আছে — ছবির ভেতরে
            # আবার লিখলে লেখাটা কাঠের পাটাতনের কোণে গিয়ে ঠেকে
            s.path(f"M {cx-6} {py+108} L {cx-6} {py+146}", BROWN, 3.4)
            s.path(f"M {cx+6} {py+108} L {cx+6} {py+146}", BLUE, 3.4)
            _lamp_unit(s, cx, py + 146, 0, 0.80, plate=False)

        s.text(cx, py + ph - 20, role, T_TSUB, GREY, 400, "middle")

    note = "প্যাঁচ টাইপ হোল্ডারে ফেজ যায় কেন্দ্রের সংযোগে, নিউট্রাল বাইরের প্যাঁচে"
    ny = 854
    s.rect(m, ny, 1240 - 2 * m, 58, "#EAF2FA", STEEL, 2, 11)
    s.text(620, ny + 36, note, T_NAME, NAVY, 700, "middle")
    s.fit(ny + 58, 24)
    return s.save(f"{OUT}/d03_holders.svg")


def d04_plug_socket():
    s = SVG(1240, 640)
    s.title("প্লাগ ও সকেট: ২-পিন ও ৩-পিন", T_TITLE)
    for i, (title, pins, col) in enumerate((("২-পিন", 2, STEEL), ("৩-পিন", 3, GREEN))):
        x = 70 + i * 570
        panel(s, x, 96, 530, 280, title + " প্লাগ ও সকেট", col)
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

    s.rect(70, 402, 1100, 130, "#FFF6E5", AMBER, 2, 12)
    s.text(620, 438, "৩-পিন প্লাগের আর্থ পিন লম্বা ও মোটা কেন?",
           T_NAME, "#7A5200", 700, "middle")
    for j, ln in enumerate([
            "লম্বা: লাগানোর সময় আর্থ সংযোগ সবার আগে হয়, খোলার সময় সবার শেষে ছোটে।",
            "মোটা: আর্থ পিন ফেজ বা নিউট্রাল ছিদ্রে ঢোকে না, তাই প্লাগ উল্টো লাগানো যায় না।"]):
        s.text(620, 474 + j * 31, ln, T_SMALL, "#7A5200", 400, "middle")
    s.fit(532, 22)
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
        "d05_circuit1", "সার্কিট ১: ২-পিন প্লাগ দিয়ে বাতি সংযোগ", circ, conn,
        "সুইচ নেই, তাই প্লাগ লাগালেই বাতি জ্বলে, খুললেই নেভে")


def d06_circuit2():
    def circ(s, cx):
        image_panel(s, cx, 150, 406, f"{IMG}/d06_circuit2_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 406, f"{IMG}/d06_circuit2_conn.png")

    return _circuit_sheet(
        "d06_circuit2", "সার্কিট ২: সুইচ দিয়ে একটি বাতি নিয়ন্ত্রণ", circ, conn,
        "সুইচ সব সময় ফেজ তারে বসাতে হয়, নিউট্রালে নয়")


def d07_circuit3():
    def circ(s, cx):
        image_panel(s, cx, 150, 426, f"{IMG}/d07_circuit3_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 426, f"{IMG}/d07_circuit3_conn.png")

    return _circuit_sheet(
        "d07_circuit3", "সার্কিট ৩: ২-পিন সকেট সংযোগ", circ, conn,
        "সকেটের দুই টার্মিনালে সরাসরি ফেজ ও নিউট্রাল যায়", 580)


def d08_circuit4():
    def circ(s, cx):
        image_panel(s, cx, 150, 426, f"{IMG}/d08_circuit4_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 426, f"{IMG}/d08_circuit4_conn.png")

    return _circuit_sheet(
        "d08_circuit4", "সার্কিট ৪: সুইচ দিয়ে সকেট নিয়ন্ত্রণ", circ, conn,
        "সুইচ ফেজ তারে বসে; নিউট্রাল সরাসরি সকেটে যায়", 580)


def d09_circuit5():
    def circ(s, cx):
        image_panel(s, cx, 150, 486, f"{IMG}/d09_circuit5_schem.png")

    def conn(s, cx):
        image_panel(s, cx, 150, 486, f"{IMG}/d09_circuit5_conn.png")

    return _circuit_sheet(
        "d09_circuit5", "সার্কিট ৫: ৩-পিন সকেট সংযোগ (আর্থসহ)", circ, conn,
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
