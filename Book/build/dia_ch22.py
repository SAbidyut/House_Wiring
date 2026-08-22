# -*- coding: utf-8 -*-
"""অধ্যায় ২২ — সার্কিট ব্রেকার : ডায়াগ্রাম।

ফিউজের ছবি ও ব্রেকারের ছবি ইনস্টিটিউটের `circuit breaker.docx`
এবং `Standard Markings on Circuit Breakers.docx` থেকে — সরাসরি
তুলে আনা, হাতে নতুন করে আঁকা নয়। বাকি সব ডায়াগ্রাম (কার্যপ্রণালী,
কার্ভ, আরসিসিবির মূলনীতি, এসপিডি, হিসাবের ফ্লো) নতুন আঁকা।

লেবেলের নিয়ম (অধ্যায় ১৫ থেকে কড়া):
  প্যানেলের শিরোনাম বিশেষ্য, যন্ত্রাংশের লেবেল এক-দুই শব্দ,
  নিচে এক লাইনের একটি নোট-পটি। কারণ, পরামর্শ ও সতর্কবাণী সবই
  বইয়ের লেখায় — ছবিতে নয়।

কালপুরুষে ², √, ÷ নেই (বা ভুল আঁকে)। তাই ছবির লেবেলে ভাগ সবসময়
/ দিয়ে, বর্গমূল সংখ্যায় (1.732)।
"""
import os
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch22")
IMG = os.path.join(HERE, "assets", "ch22")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
T_CALL = 24
T_TINY = 18.5

SYM = "#12324D"
SW = 3.4
BOXG = "#E7ECF1"
PLATE = "#F4F7FA"
METAL = "#8D9AA8"

# BNBC colours not needed, but keep
C_L1 = "#D42A1F"
C_L2 = "#E8B21C"
C_L3 = "#2E6FB7"
C_N = "#1F2933"
C_PE = "#1B6E47"


def panel(s, x, y, w, h, title, col=STEEL):
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def note_strip(s, y, text, x=46, w=1148, fill="#EAF2FA", stroke=STEEL,
               tcolor=NAVY, size=T_NAME):
    if tw(text, size, 700) > w - 60:
        raise ValueError(f"note_strip এক লাইনে ধরে না: {text!r}")
    s.rect(x, y, w, 58, fill, stroke, 2, 11)
    s.text(x + w / 2, y + 36, text, size, tcolor, 700, "middle")
    return y + 58


def callout(s, x, y, text, tx, ty, anchor="end", size=T_CALL, col=NAVY):
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    w = tw(text, size, 700)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    x1 = x0 + w
    start = x1 + 10 if tx > x1 else x0 - 10
    s.path(f"M {start} {y} L {tx} {ty}", STEEL, 2.2)
    s.circle(tx, ty, 5, STEEL)


def img_panel(s, x, y, w, h, title, img, col=STEEL):
    panel(s, x, y, w, h, title, col)
    s.image_fit(x + 16, y + 64, w - 32, h - 78, f"{IMG}/{img}", 6)


def _ih(img, w):
    from PIL import Image as _Im
    with _Im.open(f"{IMG}/{img}") as im:
        iw_, ih_ = im.size
    return round(w * ih_ / iw_)


def sheet(fname, title, head, img, note, iw=1080, top=100):
    ph = _ih(img, iw - 32) + 78
    x0 = (1240 - iw) / 2
    s = SVG(1240, top + ph + 112)
    s.title(title, T_TITLE)
    img_panel(s, x0, top, iw, ph, head, img)
    y = note_strip(s, top + ph + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def strip_panels(fname, title, items, note, gap=24, top=100, pw=None):
    n = len(items)
    pw = pw or (1148 - gap * (n - 1)) / n
    ph = max(_ih(img, pw - 32) for _t, img, _c in items) + 78
    x0 = (1240 - (pw * n + gap * (n - 1))) / 2
    s = SVG(1240, top + ph + 112)
    s.title(title, T_TITLE)
    for i, (head, img, col) in enumerate(items):
        img_panel(s, x0 + i * (pw + gap), top, pw, ph, head, img, col)
    y = note_strip(s, top + ph + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def photo_callouts(fname, title, img, left, right, note,
                   iw=430, top=104, gap=36, size=T_CALL, w=1240):
    ih = _ih(img, iw)
    ix = (w - iw) / 2
    s = SVG(w, top + ih + 130)
    s.title(title, T_TITLE)

    def place(items, side):
        if not items:
            return
        minsep = size * 2.0
        ys = [top + fy * ih for (_t, _fx, fy) in items]
        for i in range(1, len(ys)):
            ys[i] = max(ys[i], ys[i - 1] + minsep)
        over = ys[-1] - (top + ih - 12)
        if over > 0:
            ys = [y - over for y in ys]
        under = (top + 12) - ys[0]
        if under > 0:
            ys = [y + under for y in ys]
        for (text, fx, fy), ly in zip(items, ys):
            tx, ty = ix + fx * iw, top + fy * ih
            if side == "left":
                callout(s, ix - gap, ly, text, tx, ty, "end", size)
            else:
                callout(s, ix + iw + gap, ly, text, tx, ty, "start", size)

    s.image(ix, top, iw, ih, f"{IMG}/{img}")
    place(left, "left")
    place(right, "right")
    y = note_strip(s, top + ih + 30, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def node(s, x, y, col=SYM, r=6.5):
    s.circle(x, y, r, col)


def blk(s, cx, cy, text, w=None, h=64, fill="#FFFFFF", stroke=STEEL,
        size=T_BODY, tcol=NAVY, sw=2.6):
    w = w or tw(text, size, 700) + 46
    x, y = cx - w / 2, cy - h / 2
    s.rect(x, y, w, h, fill, stroke, sw, 10)
    s.text(cx, cy + size * 0.34, text, size, tcol, 700, "middle")
    return x, y, w, h


# ── ১. ফিউজ বনাম ব্রেকার ───────────────────────────────────────────────
def d01_fuse_vs_breaker():
    return strip_panels(
        "d01_fuse_vs_breaker", "ফিউজ বনাম ব্রেকার",
        [("এইচআরসি ফিউজ", "fuse_hrc.png", STEEL),
         ("কার্টিজ ফিউজ", "fuse_glass.png", GREY),
         ("কিটক্যাট ফিউজ", "fuse_kitkat.png", AMBER),
         ("ব্লেড ফিউজ", "fuse_blade.png", GREEN)],
        "ফিউজ একবার পুড়লে বদলাতে হয় — ব্রেকার রিসেট করলেই চলে")


# ── ২. ব্রেকারের প্রকারভেদ ─────────────────────────────────────────────
def d02_types():
    return strip_panels(
        "d02_types", "সুরক্ষা ডিভাইসের পরিবার",
        [("এমসিবি", "mcb_1p.png", STEEL),
         ("এমসিসিবি", "mccb_160a.png", NAVY),
         ("আরসিসিবি", "rccb_2p.jpg", GREEN),
         ("আরসিবিও", "rcbo_2p.jpg", RED)],
        "একই কাজ নয় — ওভারলোড, শর্ট সার্কিট ও লিকেজের জন্য আলাদা ডিভাইস")


# ── ৩. এমসিবির ভেতরের গঠন ─────────────────────────────────────────────
def d03_mcb_inside():
    s = SVG(1240, 660)
    s.title("এমসিবির ভেতরের গঠন", T_TITLE)
    panel(s, 60, 104, 1120, 440, "কার্যপ্রণালী", STEEL)

    xL, xR = 180, 1060
    yT = 220
    yB = 400

    s.line(xL, yT, 320, yT, NAVY, SW)
    s.text(250, yT - 18, "L ইন", T_SMALL, NAVY, 700, "middle")

    s.rect(320, yT - 18, 180, 36, AMBERBG, AMBER, 2.2, 6)
    s.text(410, yT + 6, "বাইমেটাল", T_SMALL, NAVY, 700, "middle")
    s.text(410, yT + 28, "ওভারলোড", T_TINY, GREY, 700, "middle")

    s.line(500, yT, 600, yT, NAVY, SW)

    for i in range(4):
        cx = 640 + i * 18
        s.ellipse(cx, yT, 14, 18, LIGHT, STEEL, 2)
    s.text(670, yT - 28, "ম্যাগনেটিক কয়েল", T_SMALL, NAVY, 700, "middle")
    s.text(670, yT + 28, "শর্ট সার্কিট", T_TINY, GREY, 700, "middle")

    s.line(720, yT, 800, yT, NAVY, SW)

    s.line(800, yT, 800, yB - 20, NAVY, SW)
    s.circle(800, yB, 12, "#FFFFFF", RED, 3)
    s.circle(860, yB, 12, "#FFFFFF", RED, 3)
    s.text(830, yB + 40, "কন্টাক্ট", T_SMALL, RED, 700, "middle")

    s.line(860, yB, xR, yB, NAVY, SW)
    s.text(980, yB - 18, "L আউট", T_SMALL, NAVY, 700, "middle")

    for i in range(6):
        yy = yB - 80 + i * 12
        s.line(900, yy, 960, yy, METAL, 2)
    s.text(930, yB - 90, "আর্ক শুট", T_SMALL, GREY, 700, "middle")

    # Trip mechanism — moved left, line to side so it does not cross text
    s.rect(700, yT + 80, 90, 70, REDBG, RED, 2, 8)
    s.text(745, yT + 108, "ট্রিপ", T_SMALL, RED, 700, "middle")
    s.text(745, yT + 130, "লিভার", T_TINY, RED, 700, "middle")
    # dashed line from side of box to top wire, not through centre
    s.line(700, yT + 90, 700, yT, GREY, 1.8, dash="5 4")

    s.rect(920, 160, 36, 70, STEEL, NAVY, 2, 6)
    s.text(938, 150, "হাতল", T_SMALL, NAVY, 700, "middle")

    y = note_strip(s, 568, "তাপে বাইমেটাল বাঁকে — ওভারলোডে ধীরে, কয়েলে চুম্বকে — শর্টে সঙ্গে সঙ্গে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_mcb_inside.svg")


# ── ৪. B C D কার্ভ ─────────────────────────────────────────────────────
def d04_curves():
    s = SVG(1240, 700)
    s.title("B C D কার্ভ — কখন ট্রিপ করবে", T_TITLE)
    panel(s, 60, 104, 1120, 500, "টাইম-কারেন্ট কার্ভ", STEEL)

    ox, oy = 180, 520
    ex, ey = 1100, 160
    s.line(ox, oy, ex, oy, NAVY, 2.4)
    s.line(ox, oy, ox, ey, NAVY, 2.4)
    s.text(ex - 10, oy + 28, "কারেন্ট (In-এর গুণ)", T_SMALL, NAVY, 700, "end")
    s.text(ox - 20, ey, "সময়", T_SMALL, NAVY, 700, "middle")

    for val, x in [(1, 220), (3, 360), (5, 500), (10, 700), (20, 920)]:
        s.line(x, oy, x, oy - 8, NAVY, 1.8)
        s.text(x, oy + 22, f"{val}x", T_SMALL, NAVY, 700, "middle")

    s.path(f"M {ox} {ey+40} L 400 {ey+40} L 420 {ey+80} L 500 {ey+120}", GREEN, 2.6)
    s.text(260, ey+20, "থার্মাল — ওভারলোড", T_SMALL, GREEN, 700, "start")

    # B curve — end before label box
    s.path(f"M 360 {ey+80} L 360 {oy-80} L 340 {oy-80}", RED, 3.2)
    s.rect(360, oy-80, 140, 36, REDBG, RED, 1.6, 6)
    s.text(430, oy-58, "B 3-5x", T_SMALL, RED, 700, "middle")

    # C curve
    s.path(f"M 500 {ey+120} L 500 {oy-140} L 480 {oy-140}", AMBER, 3.2)
    s.rect(500, oy-140, 200, 36, AMBERBG, AMBER, 1.6, 6)
    s.text(600, oy-118, "C 5-10x", T_SMALL, AMBER, 700, "middle")

    # D curve
    s.path(f"M 700 {ey+160} L 700 {oy-200} L 680 {oy-200}", NAVY, 3.2)
    s.rect(700, oy-200, 220, 36, LIGHT, STEEL, 1.6, 6)
    s.text(810, oy-178, "D 10-20x", T_SMALL, NAVY, 700, "middle")

    s.text(900, 210, "বাসা — B", T_BODY, RED, 700, "start")
    s.text(900, 250, "অফিস/দোকান — C", T_BODY, AMBER, 700, "start")
    s.text(900, 290, "মোটর/ট্রান্সফরমার — D", T_BODY, NAVY, 700, "start")

    y = note_strip(s, 628, "B-তে কম ইনরাশ, C-তে মাঝারি, D-তে বেশি — ভুল কার্ভে বারবার ট্রিপ")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_curves.svg")


# ── ৫. এমসিসিবির সেটিং ─────────────────────────────────────────────────
def d05_mccb():
    s = SVG(1240, 660)
    s.title("এমসিসিবি — অ্যাডজাস্টেবল সেটিং", T_TITLE)
    panel(s, 60, 104, 560, 440, "ট্রিপ ইউনিট", NAVY)
    # Dial representation
    cx1, cy1 = 220, 280
    s.circle(cx1, cy1, 70, LIGHT, STEEL, 2.4)
    s.text(cx1, cy1 - 90, "Ir — ওভারলোড", T_BODY, NAVY, 700, "middle")
    for ang, txt in [(-60, "0.8"), (-20, "0.9"), (20, "1.0"), (60, "1.0xIn")]:
        import math
        rad = math.radians(ang)
        x = cx1 + 48 * math.cos(rad)
        y = cy1 + 48 * math.sin(rad)
        s.text(x, y, txt, T_TINY, STEEL, 700, "middle")
    s.path(f"M {cx1} {cy1} L {cx1+40} {cy1-20}", RED, 3)

    cx2, cy2 = 460, 280
    s.circle(cx2, cy2, 70, LIGHT, STEEL, 2.4)
    s.text(cx2, cy2 - 90, "Im — শর্ট সার্কিট", T_BODY, NAVY, 700, "middle")
    for ang, txt in [(-60, "5"), (-20, "8"), (20, "10"), (60, "xIn")]:
        import math
        rad = math.radians(ang)
        x = cx2 + 48 * math.cos(rad)
        y = cy2 + 48 * math.sin(rad)
        s.text(x, y, txt, T_TINY, STEEL, 700, "middle")
    s.path(f"M {cx2} {cy2} L {cx2+38} {cy2-18}", RED, 3)

    s.text(340, 400, "In 100A হলে Ir=80-100A সেট করা যায়", T_SMALL, GREEN, 700, "middle")
    s.text(340, 430, "Im=500-1000A — মোটরের স্টার্টে কাজে লাগে", T_SMALL, GREY, 700, "middle")

    panel(s, 640, 104, 540, 440, "ব্রেকিং ক্যাপাসিটি", RED)
    s.text(760, 170, "Icu — একবার সর্বোচ্চ", T_BODY, RED, 700, "start")
    s.text(760, 200, "36kA / 50kA / 70kA", T_SMALL, NAVY, 700, "start")
    s.text(760, 250, "Ics — বারবার যতটা পারে", T_BODY, GREEN, 700, "start")
    s.text(760, 280, "25% / 50% / 75% / 100% of Icu", T_SMALL, NAVY, 700, "start")
    s.rect(720, 320, 380, 80, GREENBG, GREEN, 2, 10)
    s.text(910, 350, "হাসপাতাল/ডাটা সেন্টারে", T_SMALL, NAVY, 700, "middle")
    s.text(910, 378, "Ics = 100% Icu নিতে হয়", T_BODY, GREEN, 700, "middle")

    y = note_strip(s, 568, "এমসিসিবির দাম Icu দিয়ে বাড়ে — 25kA-র বদলে 50kA নিলে দাম 40% বেশি")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_mccb.svg")


# ── ৬. আরসিসিবির মূলনীতি ───────────────────────────────────────────────
def d06_rccb_principle():
    s = SVG(1240, 700)
    s.title("আরসিসিবি কীভাবে লিকেজ ধরে", T_TITLE)
    panel(s, 60, 104, 1120, 480, "কোর ব্যালান্স", GREEN)

    cx, cy = 500, 300
    s.circle(cx, cy, 90, "#FFFFFF", NAVY, 3)
    s.circle(cx, cy, 60, LIGHT, STEEL, 2)
    s.text(cx, cy + 6, "টরয়েড", T_SMALL, NAVY, 700, "middle")

    s.line(160, 240, cx - 10, 240, C_L1, SW)
    s.line(cx + 10, 240, 1050, 240, C_L1, SW)
    s.text(260, 200, "L — যাওয়া", T_SMALL, C_L1, 700, "middle")
    s.line(160, 360, cx - 10, 360, C_N, SW)
    s.line(cx + 10, 360, 1050, 360, C_N, SW)
    s.text(260, 400, "N — ফেরা", T_SMALL, C_N, 700, "middle")

    s.line(cx, cy - 60, cx, 180, STEEL, 2.2, dash="6 4")
    s.rect(cx + 80, 160, 120, 50, REDBG, RED, 2, 8)
    s.text(cx + 140, 190, "ট্রিপ কয়েল", T_SMALL, RED, 700, "middle")
    s.line(cx + 140, 210, cx + 140, 240, RED, 2.2)

    # Texts away from wires (wires at 240 and 360)
    s.text(760, 180, "স্বাভাবিক: IL = IN", T_BODY, GREEN, 700, "start")
    s.text(760, 210, "তাই টরয়েডে ফ্লাক্স শূন্য", T_SMALL, GREY, 700, "start")
    s.text(760, 400, "লিকেজে: IL ≠ IN", T_BODY, RED, 700, "start")
    s.text(760, 430, "পার্থক্য = লিকেজ কারেন্ট", T_SMALL, RED, 700, "start")
    s.text(760, 460, "30mA হলে 300ms-এ ট্রিপ", T_SMALL, NAVY, 700, "start")

    s.path(f"M 1050 240 L 1050 520 L 160 520 L 160 360", C_PE, 2.4, dash="6 4")
    s.text(1060, 400, "লিকেজ পথ", T_SMALL, C_PE, 700, "start")

    y = note_strip(s, 608, "আরসিসিবি ওভারলোড বোঝে না — তাই এমসিবির সঙ্গে বসাতেই হবে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_rccb_principle.svg")


# ── ৭. আরসিসিবির সেনসিটিভিটি ──────────────────────────────────────────
def d07_rccb_types():
    s = SVG(1240, 740)
    s.title("আরসিসিবির সেনসিটিভিটি ও টাইপ", T_TITLE)
    panel(s, 60, 104, 540, 240, "IΔn — কত লিকেজে ট্রিপ", STEEL)
    rows = [("10mA", "হাসপাতাল, ভেজা জায়গা"),
            ("30mA", "মানুষের সুরক্ষা — বাসা/অফিস"),
            ("100mA", "মাঝারি — কিছু কারখানা"),
            ("300mA", "আগুন থেকে সুরক্ষা")]
    for i, (val, use) in enumerate(rows):
        yy = 180 + i * 44
        s.text(100, yy, val, T_BODY, NAVY, 700, "start")
        s.text(200, yy, use, T_SMALL, GREY, 700, "start")
        if val == "30mA":
            s.rect(80, yy - 26, 460, 36, GREENBG, GREEN, 1.6, 6)

    panel(s, 60, 360, 540, 280, "ট্রিপ টাইম IEC 61008", GREEN)
    s.text(100, 430, "1xIΔn (30mA) — ≤300ms", T_SMALL, NAVY, 700, "start")
    s.text(100, 460, "2xIΔn (60mA) — ≤150ms", T_SMALL, NAVY, 700, "start")
    s.text(100, 490, "5xIΔn (150mA) — ≤40ms", T_BODY, RED, 700, "start")
    s.text(100, 530, "0.5xIΔn-এ ট্রিপ করবে না", T_SMALL, GREY, 700, "start")

    panel(s, 620, 104, 560, 516, "তরঙ্গের টাইপ", NAVY)
    ty = [("AC", "শুধু AC — পুরোনো, এখন চলে না"),
          ("A", "AC + পালসেটিং DC — বাসায় এটাই"),
          ("F", "A + উচ্চ ফ্রিকোয়েন্সি — ইনভার্টার"),
          ("B", "AC/DC সব — EV, সোলার, UPS")]
    for i, (t, d) in enumerate(ty):
        yy = 180 + i * 56
        s.box_auto(680, yy - 16, t, T_SMALL, fill=LIGHT, stroke=STEEL,
                   tcolor=NAVY, pad_x=12, pad_y=6)
        s.text(750, yy, d, T_SMALL, INK, 400, "start")
        if t == "A":
            s.rect(630, yy - 26, 540, 42, GREENBG, GREEN, 1.4, 6)

    y = note_strip(s, 648, "বাসায় 30mA টাইপ A — বাজারে এখনো AC বিক্রি হয়, নেবেন না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_rccb_types.svg")


# ── ৮. আরসিবিও ─────────────────────────────────────────────────────────
def d08_rcbo():
    return strip_panels(
        "d08_rcbo", "আরসিবিও — দুই কাজ এক যন্ত্রে",
        [("আরসিসিবি + এমসিবি আলাদা", "rccb_2p.jpg", STEEL),
         ("আরসিবিও — একটাই", "rcbo_1pn.png", GREEN)],
        "আলাদা দুটোয় জায়গা বেশি — আরসিবিওতে প্রতিটি সার্কিট আলাদা সুরক্ষা পায়")


# ── ৯. এসপিডি ──────────────────────────────────────────────────────────
def d09_spd():
    s = SVG(1240, 680)
    s.title("এসপিডি — সার্জ থেকে সুরক্ষা", T_TITLE)
    panel(s, 60, 104, 1120, 460, "তিন ধাপের সুরক্ষা IEC 61643", NAVY)

    # MDB -> SDB -> Socket
    boxes = [("MDB", "Type 1\nIimp 12.5-25kA\n10/350µs", 200),
             ("SDB", "Type 2\nIn 20kA, Imax 40kA\n8/20µs", 560),
             ("সকেট", "Type 3\nUp ≤1.5kV\nযন্ত্রের কাছে", 920)]

    for label, desc, cx in boxes:
        s.rect(cx - 120, 200, 240, 220, LIGHT, STEEL, 2.4, 12)
        s.text(cx, 230, label, T_NODE, NAVY, 700, "middle")
        lines = desc.split("\n")
        for i, ln in enumerate(lines):
            s.text(cx, 270 + i * 28, ln, T_SMALL, INK, 700, "middle")
        if cx != 920:
            s.line(cx + 120, 310, cx + 240, 310, STEEL, 3,
                   marker=s.arrow_defs(STEEL, f"ar{cx}", 14))

    s.text(380, 460, "LPZ 0→1 বজ্র সরাসরি", T_SMALL, RED, 700, "middle")
    s.text(700, 460, "LPZ 1→2 অবশিষ্ট সার্জ", T_SMALL, AMBER, 700, "middle")
    s.text(920, 460, "LPZ 2→3 শেষ সুরক্ষা", T_SMALL, GREEN, 700, "middle")

    s.rect(80, 500, 1080, 40, AMBERBG, AMBER, 1.6, 8)
    s.text(620, 526, "এসপিডির আর্থ তার ≤0.5m — যত ছোট তত ভালো, 16 বর্গমিমি তামা Type 1-এ", T_SMALL, NAVY, 700, "middle")

    y = note_strip(s, 588, "Type 1 ছাড়া বজ্র ঠেকবে না, Type 2 ছাড়া সুইচিং সার্জ ঠেকবে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d09_spd.svg")


# ── ১০. এমসিবির গায়ের লেখা ───────────────────────────────────────────
def d10_mcb_marking():
    return photo_callouts(
        "d10_mcb_marking", "এমসিবির গায়ের লেখা", "mcb_marking.png",
        left=[("C16 — C কার্ভ, 16A", 0.18, 0.42),
              ("6000 — Icn 6kA", 0.20, 0.60),
              ("3 — এনার্জি ক্লাস", 0.22, 0.66)],
        right=[("400V~ — রেটেড ভোল্টেজ", 0.78, 0.68),
               ("IEC 60898-1 — স্ট্যান্ডার্ড", 0.80, 0.78),
               ("ডায়াগ্রাম — 1/2 টার্মিনাল", 0.75, 0.88)],
        note="C মানে 5-10xIn-এ ম্যাগনেটিক ট্রিপ — বাসায় সবচেয়ে বেশি চলে",
        iw=460)


# ── ১১. এমসিসিবির গায়ের লেখা ─────────────────────────────────────────
def d11_mccb_marking():
    return photo_callouts(
        "d11_mccb_marking", "এমসিসিবির গায়ের লেখা", "mccb_marking.png",
        left=[("In 320A — রেটেড কারেন্ট", 0.15, 0.52),
              ("Ue 400V — অপারেটিং ভোল্টেজ", 0.15, 0.60),
              ("Icu/Ics — ব্রেকিং ক্যাপাসিটি", 0.18, 0.70)],
        right=[("Ir — ওভারলোড সেটিং", 0.72, 0.65),
               ("Im — শর্ট সার্কিট সেটিং", 0.75, 0.72),
               ("PUSH TO TRIP — টেস্ট", 0.70, 0.50)],
        note="Ir 0.8-1.0xIn ঘুরিয়ে সেট করা যায় — মোটরে কাজে লাগে",
        iw=520)


# ── ১২. আরসিসিবির গায়ের লেখা ─────────────────────────────────────────
def d12_rccb_marking():
    return photo_callouts(
        "d12_rccb_marking", "আরসিসিবির গায়ের লেখা", "rccb_marking.png",
        left=[("63A — রেটেড কারেন্ট", 0.22, 0.48),
              ("IΔn 0.03A — 30mA", 0.24, 0.54),
              ("t ≤0.1s — ট্রিপ টাইম", 0.26, 0.60)],
        right=[("Test বোতাম", 0.72, 0.42),
               ("Inc 10kA — শর্ট সহ্য", 0.76, 0.68),
               ("ডায়াগ্রাম — L/N", 0.74, 0.88)],
        note="Test বোতাম মাসে একবার চাপুন — কাজ না করলে বদলাতে হবে",
        iw=460)


# ── ১৩. হিসাবের ফ্লো ───────────────────────────────────────────────────
def d13_calc_flow():
    s = SVG(1240, 720)
    s.title("ব্রেকার সিলেকশন — হিসাবের ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 14)

    cx = 620
    steps = [
        ("লোডের তালিকা — ওয়াট যোগ", LIGHT),
        ("ডাইভার্সিটি × — সর্বোচ্চ চাহিদা", LIGHT),
        ("কারেন্ট I = P / (V × cosφ)", AMBERBG),
        ("I × 1.25 — ভবিষ্যৎ + নিরাপত্তা", LIGHT),
        ("ব্রেকার In — পরের স্ট্যান্ডার্ড মাপ", GREENBG),
        ("কেবলের ক্ষমতা ≥ In — সমন্বয়", LIGHT),
        ("Icn/Icu — ফল্ট কারেন্টের চেয়ে বড়", REDBG),
    ]

    y = 140
    for txt, fill in steps:
        blk(s, cx, y, txt, w=520, h=56, fill=fill, stroke=STEEL, size=T_BODY)
        if y > 140:
            s.line(cx, y - 56, cx, y - 28, STEEL, 2.4, marker=ar)
        y += 76

    # Side notes
    s.text(180, 260, "অধ্যায় ১৪", T_SMALL, GREY, 700, "start")
    s.text(180, 340, "1.732 তিন ফেজে", T_SMALL, GREY, 700, "start")
    s.text(950, 360, "BNBC 1.3.9.3.8 — 20%", T_SMALL, GREY, 700, "start")
    s.text(950, 460, "তারের চেয়ে বড়", T_SMALL, RED, 700, "start")
    s.text(950, 484, "ব্রেকার নয়", T_SMALL, RED, 700, "start")

    y2 = note_strip(s, 680, "ব্রেকার তারকে বাঁচায় — তারের চেয়ে বড় ব্রেকার দিলে তার পুড়েও ব্রেকার ট্রিপ করবে না")
    s.fit(y2, 24)
    return s.save(f"{OUT}/d13_calc_flow.svg")


# ── ১৪. সাধারণ ভুল ─────────────────────────────────────────────────────
def d14_mistakes():
    s = SVG(1240, 700)
    s.title("সাধারণ ভুল — যা মাঠে প্রায়ই দেখা যায়", T_TITLE)

    mistakes = [
        ("নিউট্রাল বাইপাস", "আরসিসিবির N বাদ দিয়ে সরাসরি", "আরসিসিবি সঙ্গে সঙ্গে ট্রিপ"),
        ("এক ছিদ্রে দুই তার", "নিউট্রাল বারে জায়গা নেই", "গরম হয়ে পুড়বে"),
        ("তারের চেয়ে বড় ব্রেকার", "1.5 RM-এ 32A এমসিবি", "তার পুড়বে, ব্রেকার নয়"),
        ("আর্থ ছাড়া আরসিসিবি", "আর্থিং নেই, তবু আরসিসিবি", "শক লাগার পর ট্রিপ — আগে নয়"),
        ("এসপিডির লম্বা আর্থ", "আর্থ তার 2 মিটার", "সার্জ ঠেকবে না"),
    ]

    panel(s, 60, 104, 1120, 460, "ভুল — কারণ — ফল", RED)
    y0 = 170
    s.text(120, y0, "ভুল", T_BODY, RED, 700, "start")
    s.text(380, y0, "কেন হয়", T_BODY, NAVY, 700, "start")
    s.text(700, y0, "ফল", T_BODY, RED, 700, "start")
    s.line(60, y0 + 14, 1180, y0 + 14, LINE, 1.6)

    for i, (wrong, why, result) in enumerate(mistakes):
        yy = y0 + 46 + i * 72
        s.rect(80, yy - 24, 1080, 56, "#FFFFFF" if i % 2 == 0 else BOXG, LINE, 1.2, 8)
        s.text(100, yy, wrong, T_SMALL, RED, 700, "start")
        s.text(360, yy, why, T_SMALL, STEEL, 400, "start")
        s.text(680, yy, result, T_SMALL, INK, 700, "start")

    y = note_strip(s, 588, "আরসিসিবির N কখনো বাইপাস নয় — বাইপাস করলে ওটা শুধু দামি সুইচ")
    s.fit(y, 24)
    return s.save(f"{OUT}/d14_mistakes.svg")


ALL = [d01_fuse_vs_breaker, d02_types, d03_mcb_inside, d04_curves, d05_mccb,
       d06_rccb_principle, d07_rccb_types, d08_rcbo, d09_spd,
       d10_mcb_marking, d11_mccb_marking, d12_rccb_marking,
       d13_calc_flow, d14_mistakes]

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
