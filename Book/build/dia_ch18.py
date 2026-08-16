# -*- coding: utf-8 -*-
"""অধ্যায় ১৮ — মোটর : ডায়াগ্রাম।

সিলেবাসের চারটি বিষয়ের ছবি ইনস্টিটিউটের নিজের `Motor.docx` থেকেই হুবহু
বসানো — রান ক্যাপাসিটর সংযোগ, স্টার্ট-রান ক্যাপাসিটর সংযোগ, ডিপি সুইচ
দিয়ে পাম্প-মোটরের সংযোগ, আর টার্মিনাল বক্সে স্টার ও ডেল্টার লিংক
(`assets_ch18.py`)।  মোটরের কাটা-ছবি, স্টেটর ও রোটরের আলোকচিত্র
উইকিমিডিয়া কমন্স থেকে; কৃতজ্ঞতা অধ্যায়ের শেষে ❖ চিত্রসূত্র বাক্সে।

`HW Connection Diagram All.pptx` ও `Circuit Diagram.pptx`-এ মোটরের কোনো
স্লাইড নেই — তাই ডিপি সুইচের সার্কিট ডায়াগ্রাম, কয়েল চেনার পদ্ধতি,
প্রকারভেদের গাছ ও নেমপ্লেট — এই চারটি নতুন করে আঁকা।

লেবেলের নিয়ম (অধ্যায় ১৫ থেকে কড়া):  প্যানেলের শিরোনাম বিশেষ্য, যন্ত্রাংশের
লেবেল এক-দুই শব্দ, নিচে এক লাইনের একটি নোট-পটি।  কারণ, পরামর্শ ও
সতর্কবাণী সবই বইয়ের লেখায়।

নেমপ্লেটে `cos φ`-এর বদলে `P.F.` লেখা — কালপুরুষে φ নেই, ছবির লেবেলে
ফলব্যাক ফন্টে গেলে বাকি লেখার সঙ্গে মেলে না।  বাংলা লেখায় `cos φ` ঠিকই
আছে (অধ্যায় ১২ ও ১৬-এর মতো)।
"""
import os

from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch18")
IMG = os.path.join(HERE, "assets", "ch18")

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
EARTH = "#1B6E47"
BOXG = "#E7ECF1"
METAL = "#8D9AA8"
PLATE = "#F4F7FA"


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


def callout(s, x, y, text, tx, ty, anchor="end", size=T_CALL, col=NAVY):
    """লেবেল ও লিডার — লেখার যে পাশে লক্ষ্য, সেই কিনারা থেকেই বেরোয়।"""
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    w = tw(text, size, 700)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle"
                                      else x - w)
    x1 = x0 + w
    start = x1 + 10 if tx > x1 else x0 - 10
    s.path(f"M {start} {y} L {tx} {ty}", STEEL, 2.2)
    s.circle(tx, ty, 5, STEEL)


def img_panel(s, x, y, w, h, title, img, col=STEEL):
    panel(s, x, y, w, h, title, col)
    s.image_fit(x + 16, y + 64, w - 32, h - 78, f"{IMG}/{img}", 6)


def one_panel(fname, title, head, img, note, pw=1000, col=STEEL):
    """এক ছবির শিট — সোর্স থেকে নেওয়া ছবি যেমন আছে তেমনই।"""
    from PIL import Image as _Im
    with _Im.open(f"{IMG}/{img}") as im:
        iw, ih = im.size
    ph = round((pw - 32) * ih / iw) + 78
    s = SVG(1240, 96 + ph + 110)
    s.title(title, T_TITLE)
    img_panel(s, (1240 - pw) / 2, 96, pw, ph, head, img, col)
    y = note_strip(s, 96 + ph + 24, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def two_panel(fname, title, left, right, note, pw=560, gap=28,
              lcol=STEEL, rcol=GREEN, rw=None):
    """দুই ছবির শিট — বাঁয়ে-ডানে দুটি প্যানেল, নিচে এক লাইনের নোট।"""
    from PIL import Image as _Im
    rw = rw or pw
    hs = []
    for w_, (_h, img) in ((pw, left), (rw, right)):
        with _Im.open(f"{IMG}/{img}") as im:
            iw, ih = im.size
        hs.append(round((w_ - 32) * ih / iw) + 78)
    ph = max(hs)
    s = SVG(1240, 96 + ph + 110)
    s.title(title, T_TITLE)
    total = pw + gap + rw
    x0 = (1240 - total) / 2
    img_panel(s, x0, 96, pw, ph, left[0], left[1], lcol)
    img_panel(s, x0 + pw + gap, 96, rw, ph, right[0], right[1], rcol)
    y = note_strip(s, 96 + ph + 24, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


# ── circuit symbols ─────────────────────────────────────────────────────
def node(s, x, y, col=SYM, r=6.5):
    s.circle(x, y, r, col)


def coil_sym(s, x, y, w, n=5, up=True, sw=SW):
    """কয়েল — অর্ধবৃত্তের সারি।  x থেকে x+w পর্যন্ত, y উচ্চতায়।"""
    r = w / (2 * n)
    d = f"M {x} {y}"
    for i in range(n):
        cx = x + (2 * i + 1) * r
        d += (f" A {r:.1f} {r:.1f} 0 0 {1 if up else 0} "
              f"{cx + r:.1f} {y:.1f}")
    s.path(d, SYM, sw)
    return x + w


# ═══════════════════════════════════════════════════════════════════════
def d01_parts():
    """মোটরের কাটা-ছবি — বাংলা লেবেল ছবির বাইরে, লিডার দিয়ে।"""
    s = SVG(1240, 860)
    s.title("মোটরের গঠন", T_TITLE)

    IX, IY, IW = 320, 110, 600
    IH = round(IW * 1482 / 1716)          # ph_cutaway-এর অনুপাত
    s.image(IX, IY, IW, IH, f"{IMG}/ph_cutaway.jpg")

    def at(fx, fy):
        return IX + fx * IW, IY + fy * IH

    # বাঁ পাশের লেবেল
    for text, fx, fy, ly in (("টার্মিনাল বক্স", 0.22, 0.12, 168),
                             ("স্টেটর কয়েল", 0.14, 0.39, 292),
                             ("রোটর", 0.36, 0.53, 386),
                             ("মোটরের বডি", 0.20, 0.87, 502)):
        tx, ty = at(fx, fy)
        callout(s, IX - 34, ly, text, tx, ty, "end")

    # ডান পাশের লেবেল — লক্ষ্যের বাঁ-থেকে-ডান ক্রমেই সাজানো, নইলে
    # শ্যাফট ও বিয়ারিংয়ের লিডার একে অন্যকে কেটে যায়
    for text, fx, fy, ly in (("নেমপ্লেট", 0.57, 0.26, 190),
                             ("শ্যাফট", 0.62, 0.53, 330),
                             ("বিয়ারিং", 0.76, 0.55, 424),
                             ("কুলিং ফ্যান", 0.90, 0.62, 528)):
        tx, ty = at(fx, fy)
        callout(s, IX + IW + 34, ly, text, tx, ty, "start")

    y = note_strip(s, IY + IH + 26,
                   "স্টেটর স্থির থাকে, রোটর ঘোরে — মাঝের ফাঁকটির নাম "
                   "এয়ার গ্যাপ")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_parts.svg")


def d02_types():
    """মোটরের প্রকারভেদের গাছ।"""
    s = SVG(1240, 700)
    s.title("মোটরের প্রকারভেদ", T_TITLE)

    def nodebox(cx, y, text, col=STEEL, size=T_BODY):
        return s.box_auto(cx, y, text, size, fill="#FFFFFF", stroke=col,
                          tcolor=NAVY, pad_x=20, pad_y=10, sw=2.2)

    # স্তর ১
    r = nodebox(620, 108, "ইলেকট্রিক মোটর", NAVY, T_NAME)
    ry = 108 + r[3]

    # স্তর ২ — এসি, ডিসি, ইউনিভার্সেল
    l2 = [(300, "এসি মোটর", STEEL), (620, "ডিসি মোটর", GREY),
          (940, "ইউনিভার্সেল মোটর", GREY)]
    boxes2 = []
    for cx, name, col in l2:
        boxes2.append((cx, nodebox(cx, 216, name, col)))
    b2y = 216 + boxes2[0][1][3]

    s.path(f"M 620 {ry} L 620 190", STEEL, 2.4)
    s.path("M 300 190 L 940 190", STEEL, 2.4)
    for cx, _b in boxes2:
        s.path(f"M {cx} 190 L {cx} 216", STEEL, 2.4)

    # স্তর ৩ — এসির নিচে ইন্ডাকশন ও সিনক্রোনাস
    l3 = [(180, "ইন্ডাকশন মোটর", STEEL), (440, "সিনক্রোনাস মোটর", GREY)]
    boxes3 = []
    for cx, name, col in l3:
        boxes3.append((cx, nodebox(cx, 336, name, col)))
    b3y = 336 + boxes3[0][1][3]

    s.path(f"M 300 {b2y} L 300 310", STEEL, 2.4)
    s.path("M 180 310 L 440 310", STEEL, 2.4)
    for cx, _b in boxes3:
        s.path(f"M {cx} 310 L {cx} 336", STEEL, 2.4)

    # স্তর ৪ — ইন্ডাকশনের নিচে সিঙ্গেল ও থ্রি ফেজ
    l4 = [(150, "সিঙ্গেল ফেজ", GREEN), (400, "থ্রি ফেজ", STEEL)]
    for cx, name, col in l4:
        s.box_auto(cx, 456, name, T_BODY, fill=GREENBG if col == GREEN
                   else "#FFFFFF", stroke=col, tcolor=NAVY, pad_x=20,
                   pad_y=10, sw=2.4)
    s.path(f"M 180 {b3y} L 180 430", STEEL, 2.4)
    s.path("M 150 430 L 400 430", STEEL, 2.4)
    for cx, _n, _c in [(150, 0, 0), (400, 0, 0)]:
        s.path(f"M {cx} 430 L {cx} 456", STEEL, 2.4)

    # ডান পাশে ব্যবহারের উদাহরণ — এক শব্দে
    s.rect(700, 336, 494, 174, "#FCFDFE", LINE, 1.8, 12)
    s.text(724, 374, "বাসাবাড়িতে যা বসে", T_BODY, NAVY, 700)
    for i, ln in enumerate(["পানির পাম্প · এক্সহস্ট ফ্যান",
                            "গ্রাইন্ডার · ওয়াশিং মেশিন",
                            "ফ্রিজের কম্প্রেসর"]):
        s.text(724, 412 + i * 32, ln, T_SMALL, "#39434D", 400)

    y = note_strip(s, 552,
                   "বাসাবাড়ির প্রায় সব মোটরই সিঙ্গেল ফেজ ইন্ডাকশন মোটর")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_types.svg")


def d03_stator_rotor():
    """স্টেটর ও রোটরের আলোকচিত্র — কমন্স।"""
    return two_panel(
        "d03_stator_rotor", "স্টেটর ও রোটর",
        ("স্টেটর", "ph_stator.jpg"),
        ("রোটর", "ph_rotor.jpg"),
        "স্টেটরের খাঁজে তামার কয়েল, রোটরের খাঁজে ঢালাই করা বার",
        pw=520, rw=580)


def d04_coils():
    """দুই কয়েল ও তিন প্রান্ত — মিটার দিয়ে চেনার পদ্ধতি।"""
    s = SVG(1240, 700)
    s.title("মোটরের তিন প্রান্ত ও কয়েলের রেজিস্ট্যান্স", T_TITLE)

    PY, PH = 96, 430
    panel(s, 46, PY, 620, PH, "কয়েলের সংযোগ", STEEL)
    panel(s, 694, PY, 500, PH, "মিটারের পাঠ", GREEN)

    # ── বাঁ প্যানেল — C থেকে দুই কয়েল বেরিয়ে R ও S-এ
    CX, CY = 130, 320
    node(s, CX, CY)
    s.text(CX - 24, CY + 10, "C", T_NODE, NAVY, 700, "end")

    # রানিং কয়েল — উপরের পথ, মোটা তার
    s.path(f"M {CX} {CY} L {CX} 210", SYM, SW)
    s.path(f"M {CX} 210 L 210 210", SYM, SW)
    x = coil_sym(s, 210, 210, 200, 5, True, SW + 1.2)
    s.path(f"M {x} 210 L 560 210", SYM, SW)
    s.path("M 560 210 L 560 260", SYM, SW)
    node(s, 560, 260)
    s.text(560, 300, "R", T_NODE, NAVY, 700, "middle")
    s.text(310, 168, "রানিং কয়েল", T_BODY, NAVY, 700, "middle")

    # স্টার্টিং কয়েল — নিচের পথ, সরু তার
    s.path(f"M {CX} {CY} L {CX} 430", SYM, SW)
    s.path(f"M {CX} 430 L 210 430", SYM, SW)
    x = coil_sym(s, 210, 430, 200, 8, True, SW - 1.4)
    s.path(f"M {x} 430 L 560 430", SYM, SW)
    s.path("M 560 430 L 560 380", SYM, SW)
    node(s, 560, 380)
    s.text(560, 358, "S", T_NODE, NAVY, 700, "middle")
    s.text(310, 480, "স্টার্টিং কয়েল", T_BODY, NAVY, 700, "middle")

    # ── ডান প্যানেল — তিন জোড়ার পাঠ
    rows = [("C – R", "4 Ω", "রানিং কয়েল", GREEN),
            ("C – S", "12 Ω", "স্টার্টিং কয়েল", STEEL),
            ("S – R", "16 Ω", "দুই কয়েল একসাথে", RED)]
    for i, (pair, val, name, col) in enumerate(rows):
        ry = 190 + i * 100
        s.rect(724, ry, 440, 78, "#FCFDFE", col, 2.2, 10)
        s.text(752, ry + 34, pair, T_NAME, col, 700)
        s.text(1136, ry + 34, val, T_NAME, NAVY, 700, "end")
        s.text(752, ry + 64, name, T_SMALL, "#39434D", 400)

    y = note_strip(s, PY + PH + 26,
                   "সবচেয়ে বড় পাঠ যে দুই প্রান্তে, বাকি প্রান্তটিই কমন")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_coils.svg")


def d05_run_cap():
    """রান ক্যাপাসিটর সংযোগ — RAPTI সোর্স।"""
    return one_panel(
        "d05_run_cap", "রান ক্যাপাসিটর সংযোগ", "কানেকশন ডায়াগ্রাম",
        "m05_run_cap.png",
        "ক্যাপাসিটর বসে স্টার্টিং কয়েলের সিরিজে, রানিং কয়েলে নয়",
        pw=880)


def d06_start_run():
    """স্টার্ট ও রান — দুই ক্যাপাসিটরের সংযোগ, RAPTI সোর্স।"""
    return one_panel(
        "d06_start_run", "স্টার্ট ও রান ক্যাপাসিটরের সংযোগ",
        "কানেকশন ডায়াগ্রাম", "m07_start_run.png",
        "গতি উঠলে সেন্ট্রিফিউগাল সুইচ স্টার্ট ক্যাপাসিটরটি কেটে দেয়",
        pw=1000, col=GREEN)


def d07_dp_switch():
    """ডিপি সুইচ দিয়ে মোটরের সংযোগ — বাঁয়ে আঁকা সার্কিট, ডানে RAPTI সোর্স।"""
    from PIL import Image as _Im
    with _Im.open(f"{IMG}/m06_dp_pump.png") as im:
        iw, ih = im.size

    LW, GAP, RW = 452, 26, 716
    PY = 96
    PH = max(510, round((RW - 32) * ih / iw) + 78)
    s = SVG(1240, PY + PH + 120)
    s.title("ডিপি সুইচ দিয়ে মোটরের সংযোগ", T_TITLE)

    x0 = (1240 - (LW + GAP + RW)) / 2
    panel(s, x0, PY, LW, PH, "সার্কিট ডায়াগ্রাম", STEEL)
    img_panel(s, x0 + LW + GAP, PY, RW, PH, "কানেকশন ডায়াগ্রাম",
              "m06_dp_pump.png", GREEN)

    # ── আঁকা সার্কিট — উপরে সাপ্লাই, মাঝে দুই-পোল সুইচ, নিচে মোটর।
    # মোটরের বৃত্তের বাঁ ও ডান কিনারায় ফেজ ও নিউট্রাল সোজা নেমে ঢোকে,
    # আর্থ ঘুরে এসে নিচ দিয়ে বডিতে — তিন তার কোথাও একে অন্যকে কাটে না।
    MCX, MR = x0 + 190, 52
    LX, NX, EX = MCX - MR, MCX + MR, x0 + 356
    TOP, S1, S2 = PY + 118, PY + 186, PY + 248
    MY = PY + 318
    MCY = MY + 48

    for xx, col, lab in ((LX, LIVE, "L"), (NX, NEUT, "N"), (EX, EARTH, "E")):
        s.text(xx, TOP - 22, lab, T_CALL, col, 700, "middle")
        node(s, xx, TOP, col)

    # ফেজ ও নিউট্রাল — দুটোই সুইচের ভেতর দিয়ে
    for xx, col in ((LX, LIVE), (NX, NEUT)):
        s.path(f"M {xx} {TOP} L {xx} {S1}", col, SW)
        node(s, xx, S1, col)
        node(s, xx, S2, col)
        s.path(f"M {xx} {S2} L {xx + 26} {S1 + 12}", SYM, SW)   # ব্লেড
        s.path(f"M {xx} {S2} L {xx} {MCY}", col, SW)

    # দুই ব্লেড একসঙ্গে চলে — ভাঙা রেখা
    s.path(f"M {LX + 13} {S1 + 26} L {NX + 13} {S1 + 26}", GREY, 2.4,
           dash="7 6")
    s.text(LX - 30, (S1 + S2) / 2 + 8, "ডিপি সুইচ", T_SMALL, NAVY, 700,
           "end")

    # মোটর
    s.circle(MCX, MCY, MR, "#FFFFFF", SYM, SW)
    s.text(MCX, MCY + 14, "M", T_NODE, NAVY, 700, "middle")
    s.text(LX - 30, MCY + 8, "মোটর", T_CALL, NAVY, 700, "end")

    # আর্থ — বৃত্তের নিচ দিয়ে বডিতে
    EY = MCY + MR + 44
    s.path(f"M {EX} {TOP} L {EX} {EY} L {MCX} {EY} L {MCX} {MCY + MR}",
           EARTH, SW)
    node(s, MCX, MCY + MR, EARTH)

    y = note_strip(s, PY + PH + 26,
                   "ডিপি সুইচ ফেজ আর নিউট্রাল — দুটোই একসঙ্গে কাটে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_dp_switch.svg")


def d08_nameplate():
    """নেমপ্লেটে কোন ঘরে কী লেখা থাকে।"""
    s = SVG(1240, 760)
    s.title("মোটরের নেমপ্লেট", T_TITLE)

    PX, PY, PW, PH = 380, 130, 480, 400
    s.rect(PX, PY, PW, PH, PLATE, METAL, 3.4, 10)
    s.rect(PX + 14, PY + 14, PW - 28, PH - 28, "#FFFFFF", "#B7C2CE", 2, 6)
    for cx, cy in ((PX + 26, PY + 26), (PX + PW - 26, PY + 26),
                   (PX + 26, PY + PH - 26), (PX + PW - 26, PY + PH - 26)):
        s.circle(cx, cy, 7, BOXG, METAL, 2)

    # ১~ — প্লেটের মানগুলো (230 V, 1 HP) সিঙ্গেল ফেজ পাম্প-মোটরের
    s.text(PX + PW / 2, PY + 72, "1~ INDUCTION MOTOR", T_BODY, NAVY, 700,
           "middle")
    s.line(PX + 40, PY + 90, PX + PW - 40, PY + 90, LINE, 1.8)

    rows = [("kW", "0.75", "HP", "1.0"),
            ("V", "230", "A", "5.5"),
            ("Hz", "50", "RPM", "2850"),
            ("P.F.", "0.85", "INS", "B"),
            ("IP", "44", "DUTY", "S1")]
    for i, (k1, v1, k2, v2) in enumerate(rows):
        ry = PY + 132 + i * 56
        s.text(PX + 46, ry, k1, T_SMALL, GREY, 400)
        s.text(PX + 200, ry, v1, T_NAME, INK, 700, "end")
        s.text(PX + 250, ry, k2, T_SMALL, GREY, 400)
        s.text(PX + PW - 40, ry, v2, T_NAME, INK, 700, "end")

    # লেবেল — প্লেটের বাইরে।  লিডার প্লেটের কিনারাতেই থামে, নইলে ভেতরের
    # লেখার উপর দিয়ে চলে যায় (qc সেটিকে 'line crosses' বলে ধরে)।
    for i, text in enumerate(["আউটপুট পাওয়ার", "সাপ্লাই ভোল্টেজ",
                              "ফ্রিকোয়েন্সি", "পাওয়ার ফ্যাক্টর",
                              "সুরক্ষা মাত্রা"]):
        ty = PY + 124 + i * 56
        callout(s, PX - 42, ty, text, PX, ty, "end", T_CALL)

    for i, text in enumerate(["অশ্বশক্তি", "ফুল-লোড কারেন্ট", "ঘূর্ণন গতি",
                              "ইনসুলেশন ক্লাস", "ডিউটি"]):
        ty = PY + 124 + i * 56
        callout(s, PX + PW + 42, ty, text, PX + PW, ty, "start", T_CALL)

    y = note_strip(s, PY + PH + 34,
                   "ব্রেকার ও তারের মাপ ঠিক হয় নেমপ্লেটের অ্যাম্পিয়ার দেখে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d08_nameplate.svg")


def d09_star_delta():
    """টার্মিনাল বক্সে স্টার ও ডেল্টার লিংক — RAPTI সোর্স।"""
    return two_panel(
        "d09_star_delta", "টার্মিনাল বক্সে স্টার ও ডেল্টা",
        ("স্টার (Y)", "m10_star_term.png"),
        ("ডেল্টা (Δ)", "m12_delta_term.png"),
        "উপরের তিন প্রান্ত এক করলে স্টার, উপর-নিচ জোড়া দিলে ডেল্টা",
        pw=380, rw=380, gap=120)


ALL = [d01_parts, d02_types, d03_stator_rotor, d04_coils, d05_run_cap,
       d06_start_run, d07_dp_switch, d08_nameplate, d09_star_delta]

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
