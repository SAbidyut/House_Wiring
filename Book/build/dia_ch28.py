# -*- coding: utf-8 -*-
"""অধ্যায় ২৮ — আর্থিং ও ওয়্যারিং টেস্ট : ডায়াগ্রাম।

এই অধ্যায়ের ছবির ভাগটি পরিষ্কার:

**আঁকা চিত্র** — যা ক্যামেরায় ধরা পড়ে না, কারণ জিনিসটি হয় মাটির নিচে,
নয় দেয়ালের ভেতরে, নয় সেটি একটি *পথ*:  ফল্ট কারেন্ট কোন পথে যায়,
ইলেকট্রোডের কাটা-অংশ ও মাপ, আর্থিং পিটের গাঁথুনি, রোধ কীভাবে গভীরতার
সঙ্গে কমে, চার রকম টেস্টের সংযোগ, আর ফল-অফ-পোটেনশিয়ালের বিন্যাস।

**আলোকচিত্র** (`assets_ch28.py`) — যন্ত্র ও জিনিস আসলে কেমন দেখায়:
মেগার, আর্থ টেস্টার, রডের মাথায় পিতলের ক্ল্যাম্প, আর্থিং পিটের ঢাকনা,
বোর্ডের ভেতরের তামার আর্থ বার, সকেট টেস্টার আর লাইন টেস্টার।

অধ্যায় ১৫ থেকে চলে আসা ছবির নিয়ম এখানেও কড়া:  প্যানেলের শিরোনাম
বিশেষ্য, যন্ত্রাংশের লেবেল এক-দুই শব্দ, নিচে এক লাইনের একটি নোট-পটি।
কারণ, পরামর্শ ও সতর্কবাণী বইয়ের লেখায় — ছবিতে নয়।

ছবির লেবেলে যা লেখা যাবে না:  কালপুরুষে `÷ √ ² Ω ° ≤ φ` নেই বা ভুল
আঁকে।  ভাগ সবসময় `/`, রোধের একক কথায় — "ওহম", কোণ "ডিগ্রি",
ক্ষেত্রফল "বর্গমিমি"।  মাপ, রেটিং, শতাংশ ও ধারা-নম্বরের বাইরের সব
সংখ্যা যেখানে অঙ্কটিই জিনিসটির পরিচয়, সেখানে **ল্যাটিন অঙ্ক**
(অধ্যায় ২৩-এর নিয়ম — কালপুরুষে বাংলা ৪ ল্যাটিন 8-এর মতো আঁকে, আর এই
অধ্যায়ের কেন্দ্রীয় সংখ্যাগুলোই 4, 5, 40, 62%)।

আঁকার সংখ্যা মুখস্থ নয় — BNBC ২০১২ পার্ট ৮ অধ্যায় ১, IEC 60364-6
(২০১৬), IS 3043:1987 ও BS 7430 থেকে;  `ch28.py`-র docstring-এ প্রতিটির
সূত্র লেখা আছে।
"""
import math
import os

from bookkit import bn
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch28")
IMG = os.path.join(HERE, "assets", "ch28")

# টাইপের মাপ — W-px ক্যানভাস P সেমি চওড়ায় বসলে N-px লেখা
# N × P(pt) / W পয়েন্টে ছাপে।  ১২৪০-px ক্যানভাস ১৫.৪ সেমিতে:
# ২২ px = ৭.৭ pt — প্রকল্পের ~৭.৫ pt মেঝের উপরে।
T_TITLE = 34
T_NODE = 28
T_NAME = 25
T_BODY = 23
T_SMALL = 22
T_CALL = 24.5
T_TINY = 22

SW = 3.4
PLATE = "#F4F7FA"

# উপাদানের রং
SOILF = "#E7DCC6"        # মাটি
SOILE = "#C4B394"
SOILD = "#D8C9AC"        # গভীরের ভেজা মাটি
BRICKF = "#D9B79A"       # পিটের ইটের গাঁথুনি
BRICKE = "#B08768"
CONC = "#DDE2E7"         # কংক্রিট / আরসিসি
CONCE = "#A9B3BE"
COPPER = "#B5713A"
COPPERE = "#8A5228"
BRASS = "#C9A227"
BRASSE = "#9A7B12"
GIF = "#C3CAD1"          # জিআই পাইপ
GIE = "#8C97A2"
WALLF = "#EFE6D8"
WALLE = "#C9B99F"
CASE = "#EDF1F5"         # যন্ত্রের বডি

# BNBC ১.৩.৯.৩.১৫ / সারণি ৮.১.২-এর রং
C_L = "#D42A1F"
C_N = "#1F2933"
C_PE = "#1B6E47"
C_PEY = "#E8C21A"        # সবুজ-হলুদের হলুদ ফালি


# ══════════════════════════════════════════════════════════════════════
#  সাধারণ helpers (অধ্যায় ২২–২৭ থেকে চলে আসা)
# ══════════════════════════════════════════════════════════════════════
def panel(s, x, y, w, h, title, col=STEEL):
    """প্যানেলের শিরোনাম — কেবল নাম, কোনো মন্তব্য নয়।"""
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def note_strip(s, y, text, size=T_NAME, fill="#EAF2FA", stroke=STEEL,
               tcolor=NAVY, pad=46):
    """এক লাইনের তথ্য-পটি।  দুই লাইনে গড়ালে এখানেই থেমে যায়।"""
    w = s.w - 2 * pad
    if tw(text, size, 700) > w - 60:
        raise ValueError(f"note_strip এক লাইনে ধরে না: {text!r}")
    s.rect(pad, y, w, 58, fill, stroke, 2, 11)
    s.text(pad + w / 2, y + 36, text, size, tcolor, 700, "middle")
    return y + 58


def head_bar(s, x, y, w, h, text, col, size=T_NODE, rx=13):
    """রঙিন শিরোনাম-পটি, নিচের কোনা চৌকো।"""
    rx = min(rx, max(2, h / 2 - 0.46 * size))
    s.rect(x, y, w, h, col, col, 2.4, rx)
    s.rect(x, y + rx, w, h - rx, col, "none", 0, 0)
    s.text(x + w / 2, y + h / 2 + size * 0.34, text, size, "#FFFFFF", 700,
           "middle")


def callout(s, x, y, text, tx, ty, anchor="end", size=T_CALL, col=NAVY,
            elbow=False):
    """লেবেল ও লিডার — লেখার যে পাশে লক্ষ্য, সেই কিনারা থেকেই বেরোয়।"""
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    w = tw(text, size, 700)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle"
                                      else x - w)
    x1 = x0 + w
    start = x1 + 10 if tx > x1 else x0 - 10
    d = (f"M {start} {y} L {tx} {y} L {tx} {ty}" if elbow
         else f"M {start} {y} L {tx} {ty}")
    s.path(d, STEEL, 2.2)
    s.circle(tx, ty, 5, STEEL)


def blk(s, cx, cy, text, w=None, h=64, fill="#FFFFFF", stroke=STEEL,
        size=T_BODY, tcol=NAVY, sw=2.6, rx=10):
    w = w or tw(text, size, 700) + 46
    x, y = cx - w / 2, cy - h / 2
    s.rect(x, y, w, h, fill, stroke, sw, rx)
    s.text(cx, cy + size * 0.34, text, size, tcol, 700, "middle")
    return x, y, w, h


def chip(s, cx, cy, text, fill=LIGHT, stroke=STEEL, tcol=NAVY,
         size=T_SMALL):
    w = tw(text, size, 700) + 30
    s.rect(cx - w / 2, cy - 19, w, 38, fill, stroke, 2, 19)
    s.text(cx, cy + size * 0.34, text, size, tcol, 700, "middle")
    return w


def verdict(s, x, y, w, ok, text, size=T_SMALL, pad=54):
    """রায়ের পটি — বাঁয়ে চিহ্ন, ডানে মোড়ানো লেখা।"""
    col, bg = (GREEN, GREENBG) if ok else (RED, REDBG)
    lines = wrap(text, w - pad - 30, size, 700)
    h = max(62, 30 + len(lines) * (size + 8))
    s.rect(x, y, w, h, bg, col, 2.4, 12)
    s.text(x + 24, y + h / 2 + size * 0.36, "✔" if ok else "✗",
           size + 6, col, 700, "start")
    for j, ln in enumerate(lines):
        s.text(x + pad + (w - pad) / 2, y + h / 2 + size * 0.36
               + (j - (len(lines) - 1) / 2) * (size + 8), ln, size, col,
               700, "middle")
    return y + h


def dim_h(s, x0, x1, y, text, col=NAVY, size=T_SMALL, tick=9, tdx=0):
    """আড়াআড়ি মাপের রেখা — লেখার জায়গা করতে নিজের রেখা ভেঙে নেয়।

    `tdx` দিলে লেখাটি মাপের মাঝ থেকে ওই দূরত্বে সরে বসে — সরু মাপের
    (রডের ব্যাস) লেবেল পাশের তার বা ক্ল্যাম্পের গায়ে পড়া ঠেকাতে।
    """
    w = tw(text, size, 700)
    mid = (x0 + x1) / 2 + tdx
    if x1 - x0 > w + 26 and not tdx:
        s.line(x0, y, mid - w / 2 - 10, y, col, 1.9)
        s.line(mid + w / 2 + 10, y, x1, y, col, 1.9)
        ty = y + size * 0.34
    else:
        s.line(x0, y, x1, y, col, 1.9)
        ty = y - size * 0.90
    for xx in (x0, x1):
        s.line(xx, y - tick, xx, y + tick, col, 1.9)
    s.text(mid, ty, text, size, col, 700, "middle")


def dim_v(s, x, y0, y1, text, col=NAVY, size=T_SMALL, tick=9, side="right",
          tpos="mid"):
    """খাড়া মাপের রেখা।  `tpos="top"` হলে লেখাটি রেখার মাথার দিকে বসে —
    মাঝখানে অন্য কিছু (তার, ক্ল্যাম্প) থাকলে সেটিই বাঁচার পথ।"""
    s.line(x, y0, x, y1, col, 1.9)
    for yy in (y0, y1):
        s.line(x - tick, yy, x + tick, yy, col, 1.9)
    xx = x + 14 if side == "right" else x - 14
    ty = (y0 + y1) / 2 + size * 0.34 if tpos == "mid" else y0 + size * 2.2
    s.text(xx, ty, text, size, col, 700,
           "start" if side == "right" else "end")


def arrowhead(s, x, y, ang, size=13, col=STEEL):
    a = math.radians(ang)
    p = [(x, y),
         (x - size * math.cos(a - 0.42), y - size * math.sin(a - 0.42)),
         (x - size * math.cos(a + 0.42), y - size * math.sin(a + 0.42))]
    s.poly(p, col, col, 1)


def tile(s, x, y, w, h, name, role=None, col=STEEL):
    """অধ্যায় ২২-এর গ্যালারি-টাইল।"""
    s.rect(x, y, w, h, PLATE, LINE, 1.8, 13)
    s.text(x + w / 2, y + h - (46 if role else 22), name, T_NAME, NAVY,
           700, "middle")
    if role:
        s.text(x + w / 2, y + h - 16, role, T_SMALL, col, 600, "middle")


# ══════════════════════════════════════════════════════════════════════
#  আলোকচিত্রের শিট (অধ্যায় ২৬/২৭-এর সেই একই)
# ══════════════════════════════════════════════════════════════════════
def _ih(img, w):
    from PIL import Image as _Im
    with _Im.open(f"{IMG}/{img}") as im:
        iw_, ih_ = im.size
    return round(w * ih_ / iw_)


def img_panel(s, x, y, w, h, title, img, col=STEEL):
    panel(s, x, y, w, h, title, col)
    s.image_fit(x + 16, y + 64, w - 32, h - 78, f"{IMG}/{img}", 6)


def sheet(fname, title, head, img, note, iw=1080, top=100, w=1240):
    ph = _ih(img, iw - 32) + 78
    x0 = (w - iw) / 2
    s = SVG(w, top + ph + 112)
    s.title(title, T_TITLE)
    img_panel(s, x0, top, iw, ph, head, img)
    y = note_strip(s, top + ph + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def pair_panels(fname, title, items, note, h=560, gap=24, top=100, w=1240):
    """সমান উচ্চতার কয়েকটি ছবি-প্যানেল, প্রস্থ ছবির অনুপাতে।"""
    from PIL import Image as _Im
    ws = []
    for _t, img, _c in items:
        with _Im.open(f"{IMG}/{img}") as im:
            ws.append(round(h * im.size[0] / im.size[1]) + 32)
    ph = h + 78
    span = sum(ws) + gap * (len(items) - 1)
    # অধ্যায় ১৯-এর শিক্ষা:  `qc.py` লেখা দেখে, বাক্স দেখে না।
    if span > w - 24:
        raise ValueError(f"{fname}: প্যানেলগুলো {span:.0f} px, "
                         f"ক্যানভাস {w} px — h কমাও")
    x0 = (w - span) / 2
    s = SVG(w, top + ph + 112)
    s.title(title, T_TITLE)
    x = x0
    for (head, img, col), pw in zip(items, ws):
        img_panel(s, x, top, pw, ph, head, img, col)
        x += pw + gap
    y = note_strip(s, top + ph + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def photo_callouts(fname, title, img, left, right, note,
                   ih_=760, top=100, size=T_CALL, w=1240, colw=300):
    """ছবি মাঝখানে, দুই পাশের মার্জিনে বাংলা লেবেল (অধ্যায় ১৯)।

    প্রতিটি এন্ট্রি:  (লেখা, লক্ষ্যের fx, লক্ষ্যের fy)।
    ছবি **আগে** আঁকা হয়, নইলে ছবি লিডারগুলো ঢেকে দেয়।
    """
    from PIL import Image as _Im
    with _Im.open(f"{IMG}/{img}") as im:
        iw_, ih0 = im.size
    iw = round(ih_ * iw_ / ih0)
    if iw > w - 2 * colw - 40:
        iw = w - 2 * colw - 40
        ih_ = round(iw * ih0 / iw_)
    ix = (w - iw) / 2
    s = SVG(w, top + ih_ + 130)
    s.title(title, T_TITLE)
    s.image(ix, top, iw, ih_, f"{IMG}/{img}")

    def run(items, is_left):
        # লেবেল নিজের লক্ষ্যের উচ্চতায় বসে, সমান ভাগে নয় (ch19)
        ys = []
        for _t, _fx, fy in items:
            ys.append(top + fy * ih_)
        for i in range(1, len(ys)):
            if ys[i] - ys[i - 1] < size * 1.95:
                ys[i] = ys[i - 1] + size * 1.95
        for (text, fx, fy), ly in zip(items, ys):
            lx = ix - 22 if is_left else ix + iw + 22
            s.text(lx, ly + size * 0.32, text, size, NAVY, 700,
                   "end" if is_left else "start")
            tx, ty = ix + fx * iw, top + fy * ih_
            s.path(f"M {lx + (12 if is_left else -12)} {ly} L {tx} {ty}",
                   STEEL, 2.2)
            s.circle(tx, ty, 5, STEEL)

    run(left, True)
    run(right, False)
    y = note_strip(s, top + ih_ + 30, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


# ══════════════════════════════════════════════════════════════════════
#  অধ্যায় ২৮-এর নিজস্ব আঁকার উপাদান
# ══════════════════════════════════════════════════════════════════════
def soil(s, x, y, w, h, fill=SOILF, edge=SOILE, band=None):
    """মাটির কাটা-অংশ।  `band` দিলে নিচের ওই অংশটুকু ভেজা মাটি।"""
    s.rect(x, y, w, h, fill, edge, 2, 0)
    if band:
        s.rect(x, y + h - band, w, band, SOILD, "none", 0, 0)
        s.line(x, y + h - band, x + w, y + h - band, edge, 1.6, "10 7")
    # মাটির দানা — **সাজসজ্জা**।  `s.circle()` দিয়ে আঁকলে qc.py প্রতিটি
    # দানাকে জ্যামিতি ধরে নিয়ে লেখার সঙ্গে সংঘর্ষ রিপোর্ট করে, অথচ
    # দানা লেখার নিচ দিয়েই যাওয়ার কথা — তাই কাঁচা SVG (কভারের গ্রিডের
    # একই যুক্তি)।
    grains = "".join(
        f'<circle cx="{x + ((i * 137) % int(w - 14)) + 7:.1f}" '
        f'cy="{y + ((i * 89) % int(h - 14)) + 7:.1f}" r="2.6" '
        f'fill="{edge}" opacity="0.55"/>'
        for i in range(int(w * h / 5200)))
    s.add(f'<g>{grains}</g>')


def grade(s, x0, x1, y, col=SOILE, n=None, tick=13):
    """ভূমির সমতল — রেখা ও হ্যাচ।"""
    s.line(x0, y, x1, y, col, 3.2)
    n = n or int((x1 - x0) / 26)
    for i in range(n):
        gx = x0 + 10 + i * (x1 - x0 - 16) / max(1, n - 1)
        s.line(gx, y, gx - tick * 0.6, y - tick, col, 2)


def gy_wire(s, d, sw=7):
    """সবুজ-হলুদ ইসিসি — সবুজের উপরে হলুদ ফালি।"""
    s.path(d, C_PE, sw)
    s.path(d, C_PEY, sw * 0.52, dash="9 13")


def rod_e(s, cx, y0, y1, wpx=17, col=COPPER, edge=COPPERE, tip=True):
    """তামার রড ইলেকট্রোড — কাটা-অংশে, নিচে ছুঁচোলো মাথা।"""
    s.rect(cx - wpx / 2, y0, wpx, (y1 - y0) - (wpx if tip else 0),
           col, edge, 2, 3)
    if tip:
        s.poly([(cx - wpx / 2, y1 - wpx), (cx + wpx / 2, y1 - wpx),
                (cx, y1)], col, edge, 2)
    s.rect(cx - wpx / 2 + 3, y0 + 4, wpx * 0.26, (y1 - y0) - wpx - 8,
           "#D89A62", "none", 0, 2)


def pipe_e(s, cx, y0, y1, wpx=30, holes=True):
    """জিআই পাইপ ইলেকট্রোড — দেয়ালসহ কাটা-অংশ, গায়ে ছিদ্র।"""
    t = 5.0
    s.rect(cx - wpx / 2, y0, wpx, y1 - y0, "#F2F5F7", GIE, 2, 3)
    for sgn in (-1, 1):
        s.rect(cx + sgn * wpx / 2 - (t if sgn > 0 else 0), y0, t,
               y1 - y0, GIF, GIE, 1.6, 2)
    if holes:
        n = max(2, int((y1 - y0) / 46))
        for i in range(n):
            hy = y0 + 34 + i * (y1 - y0 - 54) / max(1, n - 1)
            for sgn in (-1, 1):
                s.circle(cx + sgn * (wpx / 2 - t / 2), hy, 3.4, GIE,
                         "none", 0)


def plate_e(s, cx, cy, w, h, th=11):
    """তামার প্লেট ইলেকট্রোড — সামান্য পরিপ্রেক্ষিতে।"""
    s.poly([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2 - h * 0.16),
            (cx + w / 2, cy + h / 2 - h * 0.16), (cx - w / 2, cy + h / 2)],
           COPPER, COPPERE, 2.4)
    s.poly([(cx - w / 2, cy + h / 2), (cx + w / 2, cy + h / 2 - h * 0.16),
            (cx + w / 2, cy + h / 2 - h * 0.16 + th),
            (cx - w / 2, cy + h / 2 + th)], "#96602F", COPPERE, 2)


def brass_clamp(s, cx, cy, w=76, h=40):
    """পিতলের ক্ল্যাম্প — দুই পাশে দুটি করে বোল্ট (১.৩.৩৭.৩.৪)।"""
    s.rect(cx - w / 2, cy - h / 2, w, h, BRASS, BRASSE, 2.4, 6)
    for sgn in (-1, 1):
        for dy in (-1, 1):
            s.circle(cx + sgn * w * 0.31, cy + dy * h * 0.22, 4.6,
                     BRASSE, "none", 0)


def instrument(s, x, y, w, h, name, terms, screen=None, col=CASE):
    """যন্ত্রের বডি — উপরে নাম, নিচে টার্মিনাল।  terms: [(লেবেল, fx)]।"""
    s.rect(x, y, w, h, col, STEEL, 2.8, 12)
    s.text(x + w / 2, y + 34, name, T_SMALL, NAVY, 700, "middle")
    if screen:
        s.rect(x + w * 0.12, y + 48, w * 0.76, 54, "#E9F0E4", STEEL, 2, 7)
        s.text(x + w / 2, y + 88, screen, T_NAME, "#1B4332", 700, "middle")
    pts = []
    for lbl, fx in terms:
        tx = x + fx * w
        s.circle(tx, y + h - 22, 9, "#4A5560", INK, 2)
        s.text(tx, y + h - 40, lbl, T_SMALL, NAVY, 700, "middle")
        pts.append((tx, y + h - 22))
    return pts


def spike(s, cx, ytop, ybot, label=None, col="#8C97A2"):
    """পরীক্ষার স্পাইক — মাটিতে গাঁথা সরু রড।"""
    s.rect(cx - 5, ytop, 10, (ybot - ytop) - 14, col, "#5F6B76", 1.8, 2)
    s.poly([(cx - 5, ybot - 14), (cx + 5, ybot - 14), (cx, ybot)],
           col, "#5F6B76", 1.8)
    if label:
        # লেবেল **পাশে**।  মাথার ঠিক উপরে বসালে যন্ত্র থেকে নামা তারটি
        # নিজের লেবেলের ভেতর দিয়ে যায় (qc: line crosses)।
        s.text(cx + 20, ytop + 16, label, T_NAME, NAVY, 700, "start")


def bulb(s, cx, cy, r=22, lit=False):
    """বাতি — জ্বললে রশ্মি, কিন্তু তারের লেনে নয় (অধ্যায় ১০-এর নিয়ম)।"""
    s.circle(cx, cy, r, "#FFF6D6" if lit else "#FFFFFF", NAVY, 2.8)
    k = r * 0.52
    s.path(f"M {cx-k} {cy+k*0.5} L {cx} {cy-k*0.55} L {cx+k} {cy+k*0.5}",
           NAVY, 2.4)
    if lit:
        for a in (30, 60, 120, 150, 210, 240, 300, 330):
            ra = math.radians(a)
            s.line(cx + (r + 9) * math.cos(ra), cy - (r + 9) * math.sin(ra),
                   cx + (r + 22) * math.cos(ra), cy - (r + 22) * math.sin(ra),
                   AMBER, 3)


def body(s, cx, cy, sc=1.0, col="#4A5560"):
    """মানুষ — ফল্ট কারেন্টের পথ দেখাতে।"""
    s.circle(cx, cy - 62 * sc, 19 * sc, col, "none", 0)
    s.path(f"M {cx} {cy - 42*sc} L {cx} {cy + 22*sc}", col, 13 * sc)
    s.path(f"M {cx} {cy - 30*sc} L {cx - 34*sc} {cy - 2*sc}", col, 11 * sc)
    s.path(f"M {cx} {cy - 30*sc} L {cx + 34*sc} {cy - 4*sc}", col, 11 * sc)
    s.path(f"M {cx} {cy + 22*sc} L {cx - 21*sc} {cy + 78*sc}", col, 12 * sc)
    s.path(f"M {cx} {cy + 22*sc} L {cx + 21*sc} {cy + 78*sc}", col, 12 * sc)


def appliance(s, x, y, w, h, name):
    """ধাতব বডির যন্ত্র — বডি, ভেতরের কয়েল, তিনটি টার্মিনাল।"""
    s.rect(x, y, w, h, "#E4E9EE", STEEL, 3, 9)
    s.rect(x + 12, y + 12, w - 24, h - 46, "#F7F9FB", GREY, 2, 6)
    s.text(x + w / 2, y + h - 14, name, T_SMALL, NAVY, 700, "middle")
    return [(x + w * f, y) for f in (0.26, 0.5, 0.74)]


# ══════════════════════════════════════════════════════════════════════
#  চিত্রগুলো
# ══════════════════════════════════════════════════════════════════════
def d01_why():
    """আর্থিং না থাকলে ফল্ট কারেন্ট শরীর দিয়ে যায়, থাকলে ইসিসি দিয়ে।"""
    W, PW, PH = 1240, 578, 566
    s = SVG(W, 1000)
    s.title("বডি হয়ে গেলে কারেন্ট কোন পথে যায়", T_TITLE)
    ar = s.arrow_defs(RED, "arr", 15)
    arg = s.arrow_defs(C_PE, "arg", 15)

    for i, (x0, has_ecc) in enumerate(((28, False), (28 + PW + 56, True))):
        panel(s, x0, 100, PW, PH,
              "আর্থিং নেই" if not has_ecc else "আর্থিং আছে",
              RED if not has_ecc else GREEN)
        gy_ = 100 + PH - 96
        soil(s, x0 + 14, gy_, PW - 28, 82)
        grade(s, x0 + 14, x0 + PW - 14, gy_)

        # যন্ত্র
        ax = x0 + 84
        appliance(s, ax, 246, 168, 128, "যন্ত্রের ধাতব বডি")
        # লেবেলটি ফেজ তারের **ডানে** — মাঝে বসালে খাড়া লাল তারটি
        # নিজের লেখার ভেতর দিয়ে নামে
        s.text(ax + 72, 230, "ছেঁড়া ইনসুলেশন", T_SMALL, RED, 700,
               "start")
        # ফেজ তার যন্ত্রে
        s.path(f"M {x0+40} 196 L {ax+52} 196 L {ax+52} 268", C_L, 5)
        s.text(x0 + 40, 182, "L", T_NAME, C_L, 700, "start")
        s.circle(ax + 52, 268, 7, RED)

        if not has_ecc:
            # মানুষটি মাটিতে দাঁড়িয়ে, বাঁ হাতে যন্ত্রের বডি ছুঁয়ে আছে;
            # লাল রেখাটি হাত, শরীর ও পা হয়ে মাটিতে নামে
            sc, col = 1.4, "#4A5560"
            cx = ax + 310
            cy = gy_ - 78 * sc
            hx, hy = ax + 172, 358                      # ছোঁয়ার বিন্দু
            sh = (cx, cy - 30 * sc)
            hip = (cx, cy + 22 * sc)
            foot = (cx - 21 * sc, cy + 78 * sc)
            s.circle(cx, cy - 62 * sc, 19 * sc, col, "none", 0)
            s.path(f"M {cx} {cy - 42*sc} L {hip[0]} {hip[1]}", col, 13 * sc)
            s.path(f"M {sh[0]} {sh[1]} L {hx} {hy}", col, 11 * sc)
            s.path(f"M {sh[0]} {sh[1]} L {cx + 34*sc} {cy - 4*sc}", col,
                   11 * sc)
            s.path(f"M {hip[0]} {hip[1]} L {foot[0]} {foot[1]}", col, 12 * sc)
            s.path(f"M {hip[0]} {hip[1]} L {cx + 21*sc} {cy + 78*sc}", col,
                   12 * sc)
            s.path(f"M {hx} {hy} L {sh[0]} {sh[1]} L {hip[0]} {hip[1]} "
                   f"L {foot[0]} {foot[1]} L {foot[0]} {gy_ + 44}", RED, 4.2,
                   marker=ar)
            s.circle(hx, hy, 7, RED)
            s.text(cx + 40, cy + 44, "ফল্ট কারেন্ট", T_CALL, RED, 700,
                   "start")
            verdict(s, x0 + 26, gy_ + 106, PW - 52, False,
                    "শরীরই একমাত্র পথ")
        else:
            gy_wire(s, f"M {ax+84} 374 L {ax+84} {gy_+22} "
                       f"L {x0+PW-128} {gy_+22} L {x0+PW-128} {gy_+66}")
            # তিরটি ইসিসির **পাশে ও নিচের দিকে** — ডানে-মুখো একটি তির
            # ফাঁকা জায়গায় ভাসত আর পথের দিকও ভুল বলত
            s.path(f"M {ax+124} 400 L {ax+124} 470", C_PE, 4.6,
                   marker=arg)
            s.text(ax + 146, 442, "ফল্ট কারেন্ট", T_CALL, C_PE, 700,
                   "start")
            rod_e(s, x0 + PW - 128, gy_ + 60, gy_ + 76, 14, tip=False)
            # বাঁ প্যানেলের মানুষটি এখানে আঁকা হয়নি — মাথার বৃত্ত
            # 'ছেঁড়া ইনসুলেশন' লেখার উপরে পড়ত।  একই কথা চিপে বলা আছে।
            # চিপটি ইসিসির ডানে সরানো — কেন্দ্রে বসালে তারটি চিপের
            # ভেতর দিয়ে যেত
            chip(s, ax + 262, 522, "শরীরে কারেন্ট যায় না", GREENBG,
                 GREEN, GREEN)
            verdict(s, x0 + 26, gy_ + 106, PW - 52, True,
                    "ব্রেকার সঙ্গে সঙ্গে ট্রিপ করে")

    y = note_strip(s, 100 + PH + 118,
                   "আর্থিং শক ঠেকায় না; কারেন্টকে সহজতর পথ দেয়, "
                   "আর ব্রেকারকে ট্রিপ করায়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_why.svg")


def d02_parts():
    """আর্থিং ব্যবস্থার চারটি অংশ — ইলেকট্রোড থেকে যন্ত্র পর্যন্ত।"""
    W = 1240
    s = SVG(W, 1010)
    s.title("আর্থিং ব্যবস্থার অংশগুলো", T_TITLE)
    gy_ = 610
    soil(s, 40, gy_, W - 80, 200, band=90)
    grade(s, 40, W - 40, gy_)

    # ভবনের কাটা-অংশ
    s.rect(90, 148, 560, gy_ - 148, WALLF, WALLE, 2.6, 0)
    s.rect(112, 170, 516, gy_ - 192, "#FBF8F2", WALLE, 1.8, 0)

    # এমডিবি
    s.rect(150, 212, 232, 210, "#EEF3F7", STEEL, 3, 10)
    s.text(266, 246, "এমডিবি / ডিবি", T_BODY, NAVY, 700, "middle")
    s.rect(176, 268, 180, 22, COPPER, COPPERE, 2, 4)
    # লেবেলটি বাসবারের ডান দিকে — মাঝে বসালে নিচে-নামা আর্থ লিড
    # নিজের লেখার ভেতর দিয়ে যায়
    s.text(218, 314, "আর্থিং বাসবার", T_SMALL, NAVY, 700, "start")
    for i in range(5):
        s.circle(196 + i * 35, 279, 4.4, BRASSE, "none", 0)

    # যন্ত্র
    appliance(s, 452, 262, 150, 118, "যন্ত্রের বডি")
    gy_wire(s, "M 527 262 L 527 224 L 356 224 L 356 268", 6)
    s.text(442, 208, "ইসিসি", T_NAME, C_PE, 700, "middle")

    # আর্থ লিড
    gy_wire(s, f"M 196 290 L 196 520 L 880 520 L 880 {gy_+40}", 7)
    s.text(770, 496, "আর্থ লিড ওয়্যার", T_NAME, C_PE, 700, "middle")
    s.text(770, 588, "পিভিসি পাইপের ভেতরে", T_SMALL, GREY, 600,
           "middle")
    s.rect(196, 506, 690, 28, "none", GREY, 2, 8, dash="9 8")

    # পিট ও ইলেকট্রোড
    px, pw = 790, 180
    s.rect(px, gy_ + 8, pw, 128, "#FCFAF6", BRICKE, 2.6, 0)
    s.rect(px, gy_ - 12, pw, 22, CONC, CONCE, 2.4, 3)
    for sgn in (0, 1):
        s.rect(px + sgn * (pw - 26), gy_ + 8, 26, 128, BRICKF, BRICKE, 2, 0)
    rod_e(s, 880, gy_ + 34, gy_ + 148)
    brass_clamp(s, 880, gy_ + 52)
    s.text(px + pw / 2, gy_ + 186, "আর্থিং পিট", T_NAME, NAVY, 700,
           "middle")

    callout(s, 1176, gy_ - 30, "আরসিসি ঢাকনা", px + pw - 40, gy_ - 2,
            "end")
    callout(s, 1176, gy_ + 62, "পিতলের ক্ল্যাম্প", 912, gy_ + 52, "end")
    callout(s, 1176, gy_ + 130, "আর্থ ইলেকট্রোড", 890, gy_ + 128, "end")

    y = note_strip(s, 850,
                   "ইলেকট্রোড → আর্থ লিড → বাসবার → ইসিসি; "
                   "যেকোনো একটি আলগা হলে গোটা ব্যবস্থা অচল")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_parts.svg")


def _electrode_panel(s, x, y, w, h, title, kind, col=STEEL):
    """একটি ইলেকট্রোডের কাটা-অংশ — মাপসহ।"""
    panel(s, x, y, w, h, title, col)
    gy_ = y + 128
    soil(s, x + 18, gy_, w - 36, h - (gy_ - y) - 20, band=(h - (gy_ - y)) * 0.42)
    grade(s, x + 18, x + w - 18, gy_)
    cx = x + w * 0.44
    bot = y + h - 34
    if kind == "rod":
        rod_e(s, cx, gy_ - 26, bot)
        brass_clamp(s, cx, gy_ - 14, 68, 34)
        gy_wire(s, f"M {cx-34} {gy_-46} L {cx-34} {gy_-14} L {cx-30} {gy_-14}")
        dim_v(s, x + w - 56, gy_, bot, "3 m", side="left")
        dim_h(s, cx - 9, cx + 9, y + 108, "12.5 mm", tdx=62)
    elif kind == "pipe":
        pipe_e(s, cx, gy_ - 22, bot)
        brass_clamp(s, cx, gy_ - 12, 82, 34)
        gy_wire(s, f"M {cx-46} {gy_-44} L {cx-46} {gy_-12} L {cx-38} {gy_-12}")
        dim_v(s, x + w - 56, gy_, bot, "6.5 m", side="left")
        dim_h(s, cx - 15, cx + 15, y + 108, "38 mm", tdx=62)
    else:
        plate_e(s, cx, bot - 46, 176, 74)
        # লিডটি প্লেটের বাঁ দিকে — কেন্দ্রের কাছে রাখলে "600 mm"
        # মাপের লেখার ভেতর দিয়ে নামে
        gy_wire(s, f"M {cx-70} {gy_-44} L {cx-70} {bot-70}")
        s.circle(cx - 70, bot - 66, 7, BRASSE)
        dim_v(s, x + w - 56, gy_, bot - 76, "2 m", side="left")
        dim_h(s, cx - 88, cx + 88, bot - 104, "600 mm")


def d03_electrodes():
    """তিন রকম ইলেকট্রোড পাশাপাশি — BNBC ১.৩.৩৭.৩.৩-এর মাপে।"""
    W, PW, PH = 1240, 386, 660
    s = SVG(W, 1010)
    s.title("তিন রকম আর্থ ইলেকট্রোড", T_TITLE)
    gap = (W - 3 * PW - 56) / 2
    for i, (t, k) in enumerate((("রড আর্থিং", "rod"),
                                ("পাইপ আর্থিং", "pipe"),
                                ("প্লেট আর্থিং", "plate"))):
        _electrode_panel(s, 28 + i * (PW + gap), 100, PW, PH, t, k)
    y = note_strip(s, 100 + PH + 30,
                   "মাপগুলো BNBC ১.৩.৩৭.৩.৩-এর সর্বনিম্ন; "
                   "শুকনো মৌসুমেও ভেজা মাটিতে পৌঁছাতে হবে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_electrodes.svg")


def d04_pit():
    """আর্থিং পিট — BNBC ১.৩.৩৭.৩.৬-এর প্রতিটি মাপ।

    প্রথম খসড়ায় ডান পাশে নিয়মের একটি তালিকা-প্যানেল ছিল;  ফলে কাটা-অংশ
    আধা চওড়ায় নেমে যায় আর মাপের রেখা ও কল-আউট একে অন্যের ঘাড়ে ওঠে।
    নিয়মগুলো এখন বইয়ের সারণিতে (২৮.৩.৫), আর ছবিটি পুরো চওড়া পায় —
    "ছবি দেখায়, লেখা বোঝায়"।
    """
    W = 1240
    s = SVG(W, 900)
    s.title("আর্থিং পিটের গাঁথুনি", T_TITLE)

    gy_ = 190
    soil(s, 40, gy_, W - 80, 470)
    grade(s, 40, W - 40, gy_)

    ix, iw_, ih_ = 470, 320, 300              # ভেতরের ঘর
    wall = 44
    s.rect(ix - wall, gy_ - 22, iw_ + 2 * wall, ih_ + wall + 22,
           BRICKF, BRICKE, 2.6, 0)
    s.rect(ix, gy_ - 22, iw_, ih_, "#FDFCFA", BRICKE, 2, 0)
    s.rect(ix - wall, gy_ + ih_ - 22, iw_ + 2 * wall, wall, CONC, CONCE,
           2.4, 0)                            # সিসি মেঝে
    s.rect(ix - wall - 10, gy_ - 46, iw_ + 2 * wall + 20, 32, CONC, CONCE,
           2.6, 3)                            # আরসিসি ঢাকনা
    s.path(f"M {ix+iw_/2-24} {gy_-46} a 24 17 0 0 1 48 0", NAVY, 3)

    cx = ix + iw_ / 2
    rod_e(s, cx, gy_ + 96, gy_ + ih_ + 118, 18)
    brass_clamp(s, cx, gy_ + 116, 82, 40)
    gy_wire(s, f"M {ix-30} {gy_+56} L {cx-48} {gy_+56} "
               f"L {cx-48} {gy_+116} L {cx-44} {gy_+116}")

    # খাড়া মাপ দুটি পিটের **ভেতরে** — বাইরে রাখলে ওগুলো বাঁ ও ডান
    # পাশের কল-আউটের কলামে ঢুকে পড়ে, আর পড়তে গিয়ে মনে হয় ওরাও
    # কল-আউট
    dim_v(s, ix + 34, gy_ - 22, gy_ + ih_ - 22, "610 mm", side="right",
          tpos="top")
    dim_v(s, ix + iw_ - 34, gy_ + 130, gy_ + ih_ - 22, "380 mm",
          side="left", tpos="top")
    # রডের ছায়া-পটি খাড়াভাবে নিচে নামে, তাই মাপের লেখাটি রডের
    # ডগারও নিচে — নইলে qc: box edge cuts
    dim_h(s, ix, ix + iw_, gy_ + ih_ + 150, "610 mm")

    # তিনটি করে কল-আউট দুই পাশে।  "মাটির 38 mm উপরে" আগে ডান পাশে
    # ছিল, আর তার বিন্দুটি "আরসিসি ঢাকনা"-র বিন্দুর ঘাড়ে বসত;  এখন
    # সেটি ঢাকনার বাঁ প্রান্ত দেখায়
    # ঢাকনার বাঁ প্রান্ত দেখায়, ভূমির উপরের ফাঁকা জায়গা থেকে —
    # লেখার ডানে লক্ষ্য, তাই লিডারটি নিজের লেখা কাটে না
    callout(s, 400, gy_ - 40, "মাটির 38 mm উপরে থাকে",
            ix - wall + 6, gy_ - 30, "end")
    callout(s, 190, gy_ + 148, "254 mm ইটের গাঁথুনি", ix - wall / 2,
            gy_ + 120, "start")
    callout(s, 190, gy_ + 268, "ভেতরে নিট সিমেন্ট ফিনিশ", ix + 14,
            gy_ + 200, "start")
    callout(s, 1160, gy_ + 24, "আরসিসি ঢাকনা: 152 mm পুরু",
            ix + iw_ + wall + 2, gy_ - 30, "end")
    callout(s, 1160, gy_ + 116, "পিতলের ক্ল্যাম্প", cx + 46, gy_ + 116,
            "end")
    callout(s, 1160, gy_ + 268, "সিসি মেঝে", ix + iw_ + wall - 22,
            gy_ + ih_ - 2, "end", elbow=True)

    y = note_strip(s, 706,
                   "পিট শুধু ঢাকনা নয়; ক্ল্যাম্পের বোল্ট বছর বছর "
                   "খুলে দেখার একমাত্র উপায়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_pit.svg")


def d05_depth():
    """গভীরতার সঙ্গে রোধ কমে — কিন্তু প্রথম কয়েক মিটারেই সবচেয়ে বেশি।"""
    W = 1240
    s = SVG(W, 900)
    s.title("গভীরতা বাড়লে আর্থ রেজিস্ট্যান্স যেভাবে কমে", T_TITLE)
    ox, oy, pw, ph = 150, 150, 640, 470
    s.rect(ox, oy, pw, ph, "#FCFDFE", LINE, 1.8, 10)
    # গ্রিড-রেখা **সাজসজ্জা** — লেখার নিচ দিয়েই যাওয়ার কথা, তাই কাঁচা
    # SVG (মাটির দানার একই যুক্তি);  নথিভুক্ত করলে qc প্রতিটি সংখ্যায়
    # 'line crosses' রিপোর্ট করে
    s.add("".join(
        f'<line x1="{ox}" y1="{oy + i * ph / 5:.1f}" x2="{ox + pw}" '
        f'y2="{oy + i * ph / 5:.1f}" stroke="#E6ECF2" stroke-width="1.6"/>'
        for i in range(1, 5)))

    # R = rho/(2 pi L) [ln(8L/d) - 1], rho = 20, d = 0.0125
    def R(L):
        return 20 / (2 * math.pi * L) * (math.log(8 * L / 0.0125) - 1)

    # প্রথম তিন মিটারের অংশটুকু আলাদা করা — **বক্ররেখার আগে**।  পরে
    # আঁকলে এর ভরাট রংটি বক্ররেখার ওই অংশটুকু ঢেকে দেয়, আর ছবিটা
    # দেখায় যেন লেখচিত্র 3 m থেকে শুরু
    x3 = ox + 3 / 12.0 * pw
    s.rect(ox, oy, x3 - ox, ph, AMBERBG, AMBER, 2, 6, dash="10 8")
    s.text((ox + x3) / 2, oy + ph - 20, "প্রথম 3 m", T_SMALL,
           "#8A5A00", 700, "middle")

    Lmax, Rmax = 12.0, 20.0
    pts = []
    for i in range(121):
        L = 0.5 + i * (Lmax - 0.5) / 120
        r = min(R(L), Rmax)
        pts.append((ox + L / Lmax * pw, oy + ph - r / Rmax * ph))
    s.path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts), NAVY, 4)

    s.line(ox, oy + ph, ox + pw, oy + ph, NAVY, 3)
    s.line(ox, oy, ox, oy + ph, NAVY, 3)
    for L in (2, 4, 6, 8, 10, 12):
        gx = ox + L / Lmax * pw
        s.line(gx, oy + ph, gx, oy + ph + 10, NAVY, 2)
        s.text(gx, oy + ph + 34, str(L), T_SMALL, NAVY, 700, "middle")
    for r in (5, 10, 15, 20):
        gy2 = oy + ph - r / Rmax * ph
        s.line(ox - 10, gy2, ox, gy2, NAVY, 2)
        s.text(ox - 18, gy2 + 8, str(r), T_SMALL, NAVY, 700, "end")
    s.text(ox + pw / 2, oy + ph + 66, "গাঁথা গভীরতা, মিটার", T_NAME,
           NAVY, 700, "middle")
    s.text(ox - 108, oy + ph / 2, "রোধ", T_NAME, NAVY, 700, "middle")
    s.text(ox - 108, oy + ph / 2 + 30, "ওহম", T_SMALL, STEEL, 700,
           "middle")

    # মানগুলো উপরের R() থেকেই আসে — লেখা আর ছবি আলাদা হতে পারে না।
    # লেবেল বিন্দুর নিচে;  যেখানে বক্ররেখা খাড়া নামছে (3 ও 12 m)
    # সেখানে বাঁ দিকে, নইলে বক্ররেখা নিজেই লেখার ভেতর দিয়ে যায়
    for L, sdx, sdy in ((1, 20, 46), (3, -20, 46), (6, 20, 46),
                        (12, -20, -18)):
        gx = ox + L / Lmax * pw
        gy2 = oy + ph - min(R(L), Rmax) / Rmax * ph
        s.circle(gx, gy2, 7, RED)
        s.text(gx + sdx, gy2 + sdy, f"{R(L):.2f}", T_SMALL, RED,
               700, "start" if sdx > 0 else "end")

    bx = ox + pw + 44
    s.rect(bx, oy, W - bx - 28, 300, PLATE, LINE, 1.8, 11)
    s.text(bx + (W - bx - 28) / 2, oy + 44, "যে শর্তে আঁকা", T_BODY,
           NAVY, 700, "middle")
    for i, t in enumerate(["মাটি: 20 ওহম-মিটার", "রড: 12.5 mm ব্যাস",
                           "একটি ইলেকট্রোড", "সূত্র: BS 7430"]):
        s.text(bx + 24, oy + 96 + i * 46, "• " + t, T_SMALL, NAVY, 600,
               "start")

    y = note_strip(s, oy + ph + 106,
                   "3 মিটারের পরে বাড়তি গভীরতায় লাভ কম; "
                   "তখন দ্বিতীয় ইলেকট্রোডই সস্তা")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_depth.svg")


def d06_parallel():
    """সমান্তরাল ইলেকট্রোড — দূরত্ব গাঁথা গভীরতার সমান।"""
    W = 1240
    s = SVG(W, 880)
    s.title("একাধিক ইলেকট্রোড সমান্তরালে", T_TITLE)
    gy_ = 300
    soil(s, 40, gy_, W - 80, 300, band=120)
    grade(s, 40, W - 40, gy_)

    xs = [300, 620, 940]
    for i, cx in enumerate(xs):
        rod_e(s, cx, gy_ - 20, gy_ + 260)
        brass_clamp(s, cx, gy_ - 8, 70, 34)
        # প্রতিটি ইলেকট্রোডের চারপাশের "রেজিস্ট্যান্স এরিয়া"
        for r in (68, 116, 158):
            s.circle(cx, gy_ + 130, r, "none", "#B9A47E", 1.8, 0.55)
    gy_wire(s, f"M 140 {gy_-70} L {xs[-1]} {gy_-70}", 7)
    for cx in xs:
        gy_wire(s, f"M {cx} {gy_-70} L {cx} {gy_-8}", 6)
    s.text(140, gy_ - 88, "আর্থ লিড", T_NAME, C_PE, 700, "start")

    dim_h(s, xs[0], xs[1], gy_ + 320, "দূরত্ব = গাঁথা গভীরতা")
    dim_h(s, xs[1], xs[2], gy_ + 320, "একই দূরত্ব")

    bx, bw = 60, 1120
    s.rect(bx, gy_ + 372, bw, 96, PLATE, LINE, 1.8, 11)
    for i, (a, b_) in enumerate((("একটি রড", "6.96 ওহম"),
                                 ("দুটি", "3.5 ওহম"),
                                 ("তিনটি", "2.3 ওহম"),
                                 ("সাতটি", "1 ওহম"))):
        cx = bx + 140 + i * 280
        s.text(cx, gy_ + 412, a, T_SMALL, STEEL, 700, "middle")
        s.text(cx, gy_ + 448, b_, T_NAME, NAVY, 700, "middle")

    y = note_strip(s, gy_ + 500,
                   "খুব কাছাকাছি বসালে রেজিস্ট্যান্স এরিয়া মিশে যায়, "
                   "ভাগ আর ঠিক থাকে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_parallel.svg")


def d07_order():
    """IEC 60364-6-এর টেস্ট-ক্রম — বাসাবাড়িতে যতটুকু লাগে।"""
    W = 1240
    s = SVG(W, 900)
    s.title("টেস্টের ক্রম", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)

    steps = [("চোখের পরীক্ষা", "রং, টার্মিনাল, বাঁধন", NAVY),
             ("কন্টিনিউইটি", "ইসিসি ও বন্ডিং অবিচ্ছিন্ন", STEEL),
             ("ইনসুলেশন রেজিস্ট্যান্স", "তারে ফুটো আছে কি না", STEEL),
             ("পোলারিটি", "সুইচ ও ফিউজ ফেজে", STEEL),
             ("আর্থ রেজিস্ট্যান্স", "ইলেকট্রোড কত ওহম", STEEL),
             ("আরসিসিবি ও চালু-পরীক্ষা", "লাইন দেওয়ার পরে", GREEN)]
    x0, bw2, gap = 46, 1148, 18
    y = 108
    for i, (t, sub, col) in enumerate(steps):
        h = 92
        s.rect(x0, y, bw2, h, PLATE if i else "#FFF8E8",
               col if i else AMBER, 2.6, 12)
        s.badge(x0 + 52, y + h / 2, str(i + 1), 26, col, "#FFFFFF", T_BODY)
        s.text(x0 + 104, y + 40, t, T_NODE, NAVY, 700, "start")
        s.text(x0 + 104, y + 74, sub, T_SMALL, STEEL, 600, "start")
        tag = "লাইন বন্ধ" if i <= 4 else "লাইন চালু"
        tw_ = tw(tag, T_SMALL, 700) + 30
        s.rect(x0 + bw2 - tw_ - 26, y + h / 2 - 19, tw_, 38,
               REDBG if i <= 4 else GREENBG, RED if i <= 4 else GREEN,
               2, 19)
        s.text(x0 + bw2 - tw_ / 2 - 26, y + h / 2 + 8, tag, T_SMALL,
               RED if i <= 4 else GREEN, 700, "middle")
        if i < len(steps) - 1:
            s.line(x0 + 52, y + h + 3, x0 + 52, y + h + gap - 3, STEEL,
                   3, marker=ar)
        y += h + gap

    y2 = note_strip(s, y + 12,
                    "কোনো ধাপ ফেল করলে সারিয়ে নিয়ে ওই ধাপ ও তার "
                    "আগের ধাপগুলো আবার করতে হয়")
    s.fit(y2, 24)
    return s.save(f"{OUT}/d07_order.svg")


def d08_cont():
    """কন্টিনিউইটি — R1+R2 পদ্ধতি।"""
    W = 1240
    s = SVG(W, 900)
    s.title("কন্টিনিউইটি টেস্ট: R1+R2 পদ্ধতি", T_TITLE)

    # ডিবি
    dx, dy_, dw, dh = 52, 150, 300, 322
    s.rect(dx, dy_, dw, dh, "#EEF3F7", STEEL, 3, 12)
    s.text(dx + dw / 2, dy_ + 38, "ডিস্ট্রিবিউশন বোর্ড", T_BODY, NAVY,
           700, "middle")
    ly, ny, ey = dy_ + 108, dy_ + 186, dy_ + 264
    for yy, col, lbl in ((ly, C_L, "L"), (ny, C_N, "N"), (ey, C_PE, "E")):
        s.rect(dx + 34, yy - 15, 150, 30, LIGHT, STEEL, 2, 6)
        s.text(dx + 58, yy + 8, lbl, T_NAME, col, 700, "start")
        s.circle(dx + 160, yy, 7, col)
    # অস্থায়ী লিংক
    s.path(f"M {dx+160} {ly} L {dx+228} {ly} L {dx+228} {ey} "
           f"L {dx+160} {ey}", AMBER, 6)
    s.text(dx + 244, (ly + ey) / 2 + 8, "অস্থায়ী", T_SMALL, "#8A5A00",
           700, "start")
    s.text(dx + 244, (ly + ey) / 2 + 36, "লিংক", T_SMALL, "#8A5A00",
           700, "start")

    # সার্কিটের তার
    y1, y2_ = 200, 414
    s.path(f"M {dx+dw} {ly} L 470 {ly} L 470 {y1} L 940 {y1}", C_L, 5)
    gy_wire(s, f"M {dx+dw} {ey} L 430 {ey} L 430 {y2_} L 940 {y2_}", 6)
    s.text(760, y1 + 48, "ফেজ তার: R1", T_NAME, C_L, 700, "middle")
    s.text(700, y2_ + 40, "ইসিসি: R2", T_NAME, C_PE, 700, "middle")

    # পয়েন্টগুলো
    for i, (px, nm) in enumerate(((620, "১ম পয়েন্ট"), (780, "মাঝের"),
                                  (940, "সবচেয়ে দূরের"))):
        s.circle(px, y1, 8, C_L)
        s.circle(px, y2_, 8, C_PE)
        s.text(px, 172, nm, T_SMALL, NAVY, 700, "middle")
        if i == 2:
            # যন্ত্রটি শেষ পয়েন্টের **ডানে**।  আগে এটি দুই তারের
            # মাঝখানে বসত আর ইসিসিতে যাওয়া লিডটি বাক্সের ভেতর দিয়ে —
            # লেখা ও পর্দার উপর দিয়ে — নেমে যেত
            bx0, by0, bw3, bh3 = 1000, 240, 180, 152
            s.rect(bx0, by0, bw3, bh3, "#FCFDFE", STEEL, 2.6, 10)
            s.text(bx0 + bw3 / 2, by0 + 40, "মিটার", T_SMALL, NAVY,
                   700, "middle")
            s.rect(bx0 + 38, by0 + 58, bw3 - 76, 48, "#E9F0E4", STEEL,
                   2, 6)
            s.text(bx0 + bw3 / 2, by0 + 92, "0.44", T_NAME, "#1B4332",
                   700, "middle")
            s.text(bx0 + bw3 / 2, by0 + 136, "ওহম", T_SMALL, STEEL,
                   700, "middle")
            s.path(f"M {px} {y1} L {bx0+50} {y1} L {bx0+50} {by0}",
                   STEEL, 3)
            s.path(f"M {px} {y2_} L {bx0+132} {y2_} "
                   f"L {bx0+132} {by0+bh3}", STEEL, 3)

    s.rect(60, 494, 1080, 118, PLATE, LINE, 1.8, 11)
    s.text(600, 534, "ডিবিতে L ও E এক করে দূরের পয়েন্টে মাপলে যা "
                     "পাওয়া যায়, সেটিই R1+R2", T_BODY, NAVY, 700,
           "middle")
    s.text(600, 580, "লিড দুটি ছুঁইয়ে আগেই শূন্য করে নিতে হয়", T_SMALL,
           STEEL, 600, "middle")

    y3 = note_strip(s, 634,
                    "যন্ত্রের শর্ত: খোলা অবস্থায় 4 থেকে 24 V, "
                    "অন্তত 200 mA (IEC 60364-6)")
    s.fit(y3, 24)
    return s.save(f"{OUT}/d08_cont.svg")


def d09_ir():
    """ইনসুলেশন — তিনটি মাপ।"""
    W, PW, PH = 1240, 384, 444
    s = SVG(W, 880)
    s.title("ইনসুলেশন রেজিস্ট্যান্স: তিনটি মাপ", T_TITLE)
    gap = (W - 3 * PW - 56) / 2
    combos = [("L ও N", C_L, C_N, "ফেজ ও নিউট্রালের মাঝে"),
              ("L ও E", C_L, C_PE, "ফেজ ও আর্থের মাঝে"),
              ("N ও E", C_N, C_PE, "নিউট্রাল ও আর্থের মাঝে")]
    for i, (t, ca, cb, sub) in enumerate(combos):
        x = 28 + i * (PW + gap)
        panel(s, x, 100, PW, PH, t, STEEL)
        cx = x + PW / 2
        # তিনটি তার
        for j, (col, lbl) in enumerate(((C_L, "L"), (C_N, "N"),
                                        (C_PE, "E"))):
            wx = x + 78 + j * 114
            if col == C_PE:
                gy_wire(s, f"M {wx} 194 L {wx} 330", 9)
            else:
                s.path(f"M {wx} 194 L {wx} 330", col, 9)
            s.text(wx, 182, lbl, T_NAME, col, 700, "middle")
        ia = x + 78 + (0 if t.startswith("L") else 114)
        ib = x + 78 + (114 if t.endswith("N") else 228)
        s.rect(min(ia, ib) - 22, 356, abs(ib - ia) + 44, 76, "#FCFDFE",
               STEEL, 2.6, 10)
        s.text((ia + ib) / 2, 402, "মেগার", T_BODY, NAVY, 700, "middle")
        s.path(f"M {ia} 330 L {ia} 356", STEEL, 3)
        s.path(f"M {ib} 330 L {ib} 356", STEEL, 3)
        s.text(x + PW / 2, 466, sub, T_SMALL, STEEL, 600, "middle")
        s.text(x + PW / 2, 512, "500 V DC", T_NAME, NAVY, 700, "middle")

    y = note_strip(s, 100 + PH + 30,
                   "সব বাতি খুলে, সব যন্ত্র বিচ্ছিন্ন করে, "
                   "কিন্তু ব্রেকার চালু রেখে; নইলে পাঠ মিথ্যা")
    s.fit(y, 24)
    return s.save(f"{OUT}/d09_ir.svg")


def d10_ir_limits():
    """টেস্ট ভোল্টেজ ও সর্বনিম্ন মান — দুই কোড পাশাপাশি।"""
    W = 1240
    s = SVG(W, 780)
    s.title("কত ভোল্টে, কত মেগা-ওহম", T_TITLE)
    x0, PW, PH = 28, 578, 468
    for i, (title, col, rows, foot) in enumerate((
            ("IEC 60364-6, সারণি 6.1", STEEL,
             [("SELV ও PELV", "250 V", "0.5"),
              ("500 V পর্যন্ত", "500 V", "1"),
              ("500 V-এর উপরে", "1000 V", "1")],
             "বাসাবাড়ির 230 V সার্কিট; 500 V, অন্তত 1"),
            ("BNBC ১.৩.৪৭.৬", NAVY,
             [("230 V-এর নিচে", "500 V", "5"),
              ("230 – 400 V", "1000 V", "5"),
              ("সুইচগিয়ার, ট্রান্সফরমার", "1000 V", "5")],
             "ক্যাবল রান, দুই মাথা লাগানোর আগে"))):
        x = x0 + i * (PW + 28)
        panel(s, x, 100, PW, PH, title, col)
        hy = 176
        heads = ["সার্কিট", "টেস্ট ভোল্টেজ", "সর্বনিম্ন,\nমেগা-ওহম"]
        cw = [PW * 0.40, PW * 0.30, PW * 0.30]
        cx = x + 18
        for j, hcell in enumerate(heads):
            s.rect(cx, hy, cw[j] - 8, 70, col, col, 2, 8)
            hl = hcell.split("\n")
            for k, ln in enumerate(hl):
                s.text(cx + (cw[j] - 8) / 2,
                       hy + (43 if len(hl) == 1 else 30 + k * 26), ln,
                       T_SMALL if len(hl) == 1 else T_TINY - 3,
                       "#FFFFFF", 700, "middle")
            cx += cw[j]
        for r, row in enumerate(rows):
            cx = x + 18
            for j, cell in enumerate(row):
                s.rect(cx, hy + 78 + r * 64, cw[j] - 8, 56,
                       "#FFFFFF" if r % 2 else PLATE, LINE, 1.6, 8)
                s.text(cx + (cw[j] - 8) / 2, hy + 78 + r * 64 + 37, cell,
                       T_NAME, NAVY, 700, "middle")
                cx += cw[j]
        s.rect(x + 18, hy + 274, PW - 36, 76, LIGHT, col, 2, 10)
        for k, ln in enumerate(wrap(foot, PW - 76, T_SMALL, 600)[:2]):
            s.text(x + PW / 2, hy + 274 + 32 + k * 30, ln, T_SMALL, NAVY,
                   600, "middle")


    y = note_strip(s, 100 + PH + 30,
                   "দুই কোডে মিল নেই; মান নিতে হয় BNBC-র 5, "
                   "ভোল্টেজ 500 (২৮.৭.৩ দ্রষ্টব্য)")
    s.fit(y, 24)
    return s.save(f"{OUT}/d10_ir_limits.svg")


def d11_pol():
    """পোলারিটি — সুইচ ফেজে বনাম নিউট্রালে।"""
    W, PW, PH = 1240, 578, 470
    s = SVG(W, 830)
    s.title("সুইচ কোন তারে বসেছে", T_TITLE)
    for i, right in enumerate((True, False)):
        x = 28 + i * (PW + 56)
        panel(s, x, 100, PW, PH, "সঠিক" if right else "ভুল",
              GREEN if right else RED)
        ly, ny = 214, 400
        # তার
        s.path(f"M {x+40} {ly} L {x+PW-40} {ly}", C_L, 6)
        s.path(f"M {x+40} {ny} L {x+PW-40} {ny}", C_N, 6)
        s.text(x + 30, ly + 8, "L", T_NAME, C_L, 700, "end")
        s.text(x + 30, ny + 8, "N", T_NAME, C_N, 700, "end")

        sx = x + 176                       # সুইচের অবস্থান
        swy = ly if right else ny
        s.rect(sx - 46, swy - 82, 92, 62, "#FFFFFF", NAVY, 3, 8)
        s.path(f"M {sx-26} {swy-30} L {sx+24} {swy-56}", NAVY, 4)
        s.circle(sx - 26, swy - 30, 6, NAVY)
        s.circle(sx + 26, swy - 30, 6, NAVY)
        s.path(f"M {sx-26} {swy-30} L {sx-26} {swy}", NAVY, 4)
        s.path(f"M {sx+26} {swy-30} L {sx+26} {swy}", NAVY, 4)
        # লেবেলটি সুইচের **বাঁয়ে** — ডানে বসালে "সঠিক" প্যানেলে
        # সেটি প্যানেলের শিরোনাম-চিপের নিচে ঢুকে পড়ে
        s.text(sx - 62, swy - 46, "সুইচ", T_NAME, NAVY, 700, "end")
        # কেটে ফেলা লাইন
        s.rect(sx - 30, swy - 8, 60, 16, "#FFFFFF", "#FFFFFF", 0, 0)

        bx = x + PW - 150
        bulb(s, bx, (ly + ny) / 2, 30, False)
        s.path(f"M {bx} {ly} L {bx} {(ly+ny)/2 - 32}", C_L if right
               else C_L, 6)
        s.path(f"M {bx} {(ly+ny)/2 + 32} L {bx} {ny}", C_N, 6)
        s.text(bx, ny + 40, "বাতি", T_SMALL, NAVY, 700, "middle")

        if right:
            verdict(s, x + 30, 466, PW - 60, True,
                    "সুইচ বন্ধ করলে হোল্ডারে ভোল্টেজ থাকে না")
        else:
            s.circle(bx, (ly + ny) / 2 - 30, 13, "none", RED, 4)
            verdict(s, x + 30, 466, PW - 60, False,
                    "সুইচ বন্ধ করলেও হোল্ডার লাইভ")
    y = note_strip(s, 100 + PH + 30,
                   "BNBC ১.৩.৪৭.৮.৪ (ঞ): ফিউজ ও এক-মেরু সুইচ "
                   "শুধু ফেজ তারে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d11_pol.svg")


def d12_holder():
    """হোল্ডার ও সকেটের পোলারিটি।"""
    W, PW, PH = 1240, 578, 470
    s = SVG(W, 790)
    s.title("হোল্ডার ও সকেটে কোন প্রান্তে কোন তার", T_TITLE)

    # ── প্যাঁচ হোল্ডার ──────────────────────────────────────────────
    x = 28
    panel(s, x, 100, PW, PH, "প্যাঁচ (ES) হোল্ডার", STEEL)
    cx, cy = x + PW / 2 - 30, 300
    s.rect(cx - 52, cy - 92, 104, 130, "#E8ECF1", STEEL, 3, 10)
    for i in range(6):                    # প্যাঁচের খাঁজ
        s.path(f"M {cx-46} {cy-72+i*20} L {cx+46} {cy-78+i*20}", GREY, 3)
    s.circle(cx, cy + 54, 17, BRASS, BRASSE, 2.6)
    # নামটি ছোঁয়ার **পাশে**, ডান মার্জিন থেকে।  নিচে বসালে কেন্দ্র
    # থেকে নামা লাল তারটি নিজের লেখার ভেতর দিয়ে যায়
    callout(s, x + PW - 40, cy + 54, "কেন্দ্রের ছোঁয়া", cx + 16,
            cy + 54, "end", size=T_SMALL)
    s.text(cx, cy - 112, "প্যাঁচ", T_SMALL, NAVY, 700, "middle")
    s.path(f"M {cx} {cy-104} L {cx-28} {cy-64}", STEEL, 2.2)
    s.circle(cx - 28, cy - 64, 5, STEEL)
    # দুটি প্রান্ত-তার দুই দিকে নেমে যায়।  আগে দুটিই একই উচ্চতায়
    # ডানে চলে যেত, ফলে কালো ও লাল তার একটির উপরে আরেকটি পড়ত এবং
    # ছবিতে মনে হতো দুটি একই পরিবাহী
    s.path(f"M {cx} {cy+72} L {cx} {cy+126}", C_L, 6)
    s.path(f"M {cx-52} {cy-28} L {x+72} {cy-28} L {x+72} {cy+126}",
           C_N, 6)
    s.text(cx + 18, cy + 122, "L", T_NAME, C_L, 700, "start")
    s.text(x + 54, cy + 122, "N", T_NAME, C_N, 700, "end")
    s.rect(x + 30, 442, PW - 60, 76, GREENBG, GREEN, 2.4, 11)
    for k, ln in enumerate(wrap("ফেজ যাবে কেন্দ্রের ছোঁয়ায়, নিউট্রাল "
                                "বাইরের প্যাঁচে; উল্টো হলে বাল্ব "
                                "বদলানোর সময় হাতে লাগে",
                                PW - 110, T_SMALL, 700)[:2]):
        s.text(x + PW / 2, 442 + 32 + k * 30, ln, T_SMALL, GREEN, 700,
               "middle")

    # ── সকেট ────────────────────────────────────────────────────────
    x = 28 + PW + 56
    panel(s, x, 100, PW, PH, "তিন-পিন সকেট", STEEL)
    cx, cy = x + PW / 2, 292
    s.rect(cx - 118, cy - 118, 236, 236, "#F7F9FB", STEEL, 3.4, 22)
    # তিনটি ছিদ্র — উপরে আর্থ, নিচে দুই
    s.rect(cx - 13, cy - 88, 26, 58, "#2B333B", INK, 2, 5)
    s.rect(cx - 84, cy + 6, 26, 56, "#2B333B", INK, 2, 5)
    s.rect(cx + 58, cy + 6, 26, 56, "#2B333B", INK, 2, 5)
    s.text(cx + 26, cy - 52, "E", T_NAME, C_PE, 700, "start")
    s.text(cx - 71, cy + 96, "N", T_NAME, C_N, 700, "middle")
    s.text(cx + 71, cy + 96, "L", T_NAME, C_L, 700, "middle")
    s.rect(x + 30, 442, PW - 60, 76, GREENBG, GREEN, 2.4, 11)
    for k, ln in enumerate(wrap("সামনে থেকে দেখলে ডানে ফেজ, বাঁয়ে "
                                "নিউট্রাল, উপরে আর্থ; সব সকেটে একই",
                                PW - 110, T_SMALL, 700)[:2]):
        s.text(x + PW / 2, 442 + 32 + k * 30, ln, T_SMALL, GREEN, 700,
               "middle")

    y = note_strip(s, 100 + PH + 30,
                   "IEC 60364-6-এর ৬.৪.৩.৬: সকেট ও হোল্ডারের "
                   "সংযোগ মিলিয়ে দেখা পোলারিটি টেস্টেরই অংশ")
    s.fit(y, 24)
    return s.save(f"{OUT}/d12_holder.svg")


def d13_fop():
    """ফল-অফ-পোটেনশিয়াল — বিন্যাস ও দূরত্ব।"""
    W = 1240
    s = SVG(W, 980)
    s.title("আর্থ রেজিস্ট্যান্স মাপা: ফল-অফ-পোটেনশিয়াল", T_TITLE)
    gy_ = 470
    soil(s, 40, gy_, W - 80, 300)
    grade(s, 40, W - 40, gy_)

    ex, px_, cx_ = 190, 640, 1090
    rod_e(s, ex, gy_ - 34, gy_ + 96, 18)
    brass_clamp(s, ex, gy_ - 22, 74, 36)
    s.text(ex, gy_ + 132, "E: মাপা ইলেকট্রোড", T_NAME, NAVY, 700,
           "middle")
    spike(s, px_, gy_ - 44, gy_ + 66, "P")
    spike(s, cx_, gy_ - 44, gy_ + 66, "C")

    # যন্ত্র
    mx, mw = 470, 300
    pts = instrument(s, mx, 132, mw, 176, "আর্থ টেস্টার",
                     [("E", 0.18), ("P", 0.5), ("C", 0.82)],
                     screen="4.9 ওহম")
    s.path(f"M {pts[0][0]} {pts[0][1]+12} L {pts[0][0]} 404 "
           f"L {ex} 404 L {ex} {gy_-52}", STEEL, 3.4)
    s.path(f"M {pts[1][0]} {pts[1][1]+12} L {pts[1][0]} 428 "
           f"L {px_} 428 L {px_} {gy_-56}", STEEL, 3.4)
    s.path(f"M {pts[2][0]} {pts[2][1]+12} L {pts[2][0]} 386 "
           f"L {cx_} 386 L {cx_} {gy_-56}", STEEL, 3.4)

    dim_h(s, ex, cx_, gy_ + 214, "অন্তত 30 m")
    dim_h(s, ex, px_, gy_ + 272, "এর 62%")

    s.rect(60, 790, 1120, 74, PLATE, LINE, 1.8, 11)
    s.text(620, 836, "কারেন্ট যায় E থেকে C-তে · ভোল্টেজ মাপা হয় "
                     "E ও P-এর মাঝে", T_BODY, NAVY, 700, "middle")

    y = note_strip(s, 884,
                   "স্পাইক তিনটি একই সরলরেখায়, আর ইলেকট্রোড "
                   "ব্যবস্থা থেকে খুলে নিয়ে মাপা")
    s.fit(y, 24)
    return s.save(f"{OUT}/d13_fop.svg")


def d14_62():
    """৬২% নিয়ম — তিন পাঠ সমান হলে পাঠ ঠিক।"""
    W, PW, PH = 1240, 578, 500
    s = SVG(W, 830)
    s.title("পাঠটি ঠিক কি না, বোঝার উপায়", T_TITLE)
    cases = [("বৈধ পাঠ", GREEN, [4.8, 4.9, 5.0], True,
              "তিন পাঠ কাছাকাছি: 4.9 ওহম নেওয়া যায়"),
             ("অবৈধ পাঠ", RED, [3.9, 4.9, 6.4], False,
              "C স্পাইক আরও দূরে সরিয়ে আবার মাপতে হবে")]
    for i, (t, col, vals, ok, msg) in enumerate(cases):
        x = 28 + i * (PW + 56)
        panel(s, x, 100, PW, PH, t, col)
        ox, oy, pw, ph = x + 92, 176, PW - 150, 226
        s.rect(ox, oy, pw, ph, "#FCFDFE", LINE, 1.6, 8)
        s.add("".join(
            f'<line x1="{ox}" y1="{oy + k * ph / 4:.1f}" x2="{ox + pw}" '
            f'y2="{oy + k * ph / 4:.1f}" stroke="#E6ECF2" '
            f'stroke-width="1.5"/>' for k in range(1, 4)))
        vmax = 8.0
        pts = []
        for j, v in enumerate(vals):
            gx = ox + (j + 0.5) * pw / 3
            gy2 = oy + ph - v / vmax * ph
            pts.append((gx, gy2))
            s.circle(gx, gy2, 8, col)
            s.text(gx, gy2 - 20, f"{v}", T_SMALL, col, 700, "middle")
        s.path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts),
               col, 4)
        s.line(ox, oy + ph, ox + pw, oy + ph, NAVY, 2.6)
        s.line(ox, oy, ox, oy + ph, NAVY, 2.6)
        for j, lbl in enumerate(("52%", "62%", "72%")):
            s.text(ox + (j + 0.5) * pw / 3, oy + ph + 34, lbl, T_SMALL,
                   NAVY, 700, "middle")
        s.text(ox + pw / 2, oy + ph + 72, "P স্পাইকের অবস্থান", T_NAME,
               NAVY, 700, "middle")
        s.text(ox - 22, oy + 20, "ওহম", T_SMALL, STEEL, 700, "end")
        verdict(s, x + 30, 502, PW - 60, ok, msg)

    y = note_strip(s, 100 + PH + 30,
                   "P স্পাইক তিন জায়গায় বসিয়ে দেখা; সমতল মানে "
                   "দুই ইলেকট্রোডের এলাকা মেশেনি")
    s.fit(y, 24)
    return s.save(f"{OUT}/d14_62.svg")


def d15_wenner():
    """মাটির রেজিস্টিভিটি — ওয়েনারের চার-ইলেকট্রোড পদ্ধতি।"""
    W = 1240
    s = SVG(W, 800)
    s.title("মাটির রেজিস্টিভিটি মাপা: ওয়েনার পদ্ধতি", T_TITLE)
    gy_ = 430
    soil(s, 40, gy_, W - 80, 170)
    grade(s, 40, W - 40, gy_)

    xs = [230, 500, 770, 1040]
    for cx, lbl in zip(xs, ("C1", "P1", "P2", "C2")):
        spike(s, cx, gy_ - 40, gy_ + 54, lbl)
    mx, mw = 460, 320
    pts = instrument(s, mx, 148, mw, 168, "চার-টার্মিনাল আর্থ টেস্টার",
                     [("C1", 0.13), ("P1", 0.38), ("P2", 0.62),
                      ("C2", 0.87)])
    # বাইরের দুটি লিড **উপরের** সারিতে, ভেতরের দুটি নিচের সারিতে।
    # উল্টো করলে ভেতরের লিডের খাড়া অংশ বাইরের লিডের আড়াআড়ি অংশ
    # কেটে যায় — আগের খসড়ায় যন্ত্রের নিচে তারের জট বাঁধত
    for (tx, ty), cx, dy2 in zip(pts, xs, (338, 374, 374, 338)):
        s.path(f"M {tx} {ty+12} L {tx} {dy2} L {cx} {dy2} "
               f"L {cx} {gy_-48}", STEEL, 3.2)

    for a, b_ in zip(xs, xs[1:]):
        dim_h(s, a, b_, gy_ + 122, "S")
    dim_v(s, 200, gy_, gy_ + 44, "10–15 cm", side="left")

    s.rect(240, gy_ + 176, 760, 108, PLATE, STEEL, 2.4, 12)
    s.text(620, gy_ + 222, "রেজিস্টিভিটি = 2 × পাই × S × পাঠ", T_NODE,
           NAVY, 700, "middle")
    s.text(620, gy_ + 262, "S মিটারে, পাঠ ওহমে, ফল ওহম-মিটারে",
           T_SMALL, STEEL, 600, "middle")

    y = note_strip(s, gy_ + 306,
                   "চারটি স্পাইক সমান দূরত্বে, একই সরলরেখায়, "
                   "মাটিতে মাত্র 10–15 cm গাঁথা")
    s.fit(y, 24)
    return s.save(f"{OUT}/d15_wenner.svg")


def d16_wrong():
    """যে ভুলগুলো বারবার হয়।"""
    W = 1240
    s = SVG(W, 900)
    s.title("আর্থিং ও টেস্টে যে ভুলগুলো বারবার হয়", T_TITLE)
    items = [("নিউট্রাল আর আর্থ এক করা", "বোর্ডেই দুটিকে জোড়া লাগানো"),
             ("ইলেকট্রোড শুকনো মাটিতে", "শীতে ভালো, বর্ষার পরে খারাপ"),
             ("ক্ল্যাম্প ঢিলা", "রং করা হয়নি, বছর ঘুরতেই মরিচা"),
             ("পিট নেই", "মাটি চাপা দিয়ে দেওয়া, খুলে দেখার উপায় নেই"),
             ("যন্ত্র লাগানো রেখে মেগার", "ইলেকট্রনিক্স পুড়ে যায়"),
             ("লিড শূন্য না করে কন্টিনিউইটি", "প্রতিটি পাঠে বাড়তি রোধ"),
             ("সুইচ নিউট্রালে", "সুইচ বন্ধ করেও হোল্ডার লাইভ"),
             ("লাইন দেওয়ার পরে টেস্ট", "কোডে বলা আছে: আগে টেস্ট")]
    cols, cw = 2, 578
    ch = 100 + 32 * max(len(wrap(sub, cw - 110, T_SMALL, 600))
                        for _, sub in items)
    for i, (t, sub) in enumerate(items):
        x = 28 + (i % cols) * (cw + 28)
        y = 108 + (i // cols) * (ch + 18)
        s.rect(x, y, cw, ch, REDBG, RED, 2.4, 12)
        s.text(x + 30, y + 48, "✗", T_NODE + 6, RED, 700, "start")
        for k, ln in enumerate(wrap(t, cw - 110, T_NODE, 700)[:1]):
            s.text(x + 74, y + 52, ln, T_NODE, NAVY, 700, "start")
        for k, ln in enumerate(wrap(sub, cw - 110, T_SMALL, 600)[:2]):
            s.text(x + 74, y + 96 + k * 32, ln, T_SMALL, "#8A2B22", 600,
                   "start")
    y = note_strip(s, 108 + 4 * (ch + 18) + 8,
                   "প্রতিটি ভুলই টেস্টে ধরা পড়ে; শর্ত একটিই, "
                   "টেস্টটি আসলে করতে হবে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d16_wrong.svg")


# ── আলোকচিত্রের শিট ───────────────────────────────────────────────────
def d17_ir_meters():
    return pair_panels(
        "d17_ir_meters", "ইনসুলেশন টেস্টার",
        [("হাতে-ঘোরানো মেগার", "ph_megger.jpg", STEEL),
         ("অ্যানালগ", "ph_ir_analog.jpg", STEEL)],
        "BNBC ১.৩.৪৭.৬.১ যে 'জেনারেটর টাইপ' যন্ত্রের কথা বলেছে, "
        "বাঁয়েরটি সেটিই", h=520)


def d18_ir_read():
    return photo_callouts(
        "d18_ir_read", "ডিজিটাল ইনসুলেশন টেস্টারের পাঠ",
        "ph_ir_digital.jpg",
        [("পাঠ", 0.44, 0.13),
         ("প্রয়োগ করা ভোল্টেজ", 0.50, 0.243),
         ("টেস্ট বোতাম", 0.47, 0.40)],
        [("রেঞ্জ নব", 0.47, 0.575),
         ("টেস্ট ভোল্টেজ বাছাই", 0.72, 0.46),
         ("প্রোবের সকেট", 0.60, 0.75)],
        "নবেই IEC 60364-6-এর তিনটি ভোল্টেজ: 250, 500 ও 1000",
        ih_=800)


def d19_earth_test():
    # ছবিটি চার-টার্মিনাল যন্ত্র (Fluke 1623) — নবে 3-POLE ও 4-POLE
    # দুটিই আছে।  প্রথম ক্যাপশনে "তিন-টার্মিনাল" লেখা হয়েছিল, যা ছবির
    # সঙ্গে মেলে না;  ছবি খুঁটিয়ে দেখে ঠিক করা হয়েছে।
    return sheet("d19_earth_test", "আর্থ রেজিস্ট্যান্স টেস্টার",
                 "ডিজিটাল আর্থ / গ্রাউন্ড টেস্টার",
                 "ph_earth_test.jpg",
                 "নবে 3-POLE ও 4-POLE; একটি ইলেকট্রোডের রোধের জন্য, "
                 "অন্যটি মাটির রেজিস্টিভিটির", iw=980)


def d20_rod_pit():
    return pair_panels(
        "d20_rod_pit", "মাটির নিচের অংশ",
        [("রডের মাথায় ক্ল্যাম্প", "ph_rod_clamp.jpg", STEEL),
         ("আর্থিং পিটের ঢাকনা", "ph_pit.jpg", STEEL)],
        "ক্ল্যাম্প ও লিড; এই জোড়াটিই গোটা ব্যবস্থার সবচেয়ে দুর্বল "
        "জায়গা", h=520)


def d21_bar():
    return pair_panels(
        "d21_bar", "আর্থিং বাসবার",
        [("বোর্ডের ভেতরে", "ph_bar_panel.jpg", STEEL),
         ("আলাদা করে", "ph_bar_parts.jpg", STEEL)],
        "BNBC ১.৩.৩৭.৩.৫: প্রতিটি বোর্ডে অন্তত একটি তামার "
        "আর্থিং বাসবার", h=390)


def d22_socket():
    return pair_panels(
        "d22_socket", "সকেট টেস্টার",
        [("নিয়ন বাতির ছক", "ph_socket_eu.jpg", STEEL),
         ("ডিজিটাল", "ph_socket_dig.jpg", STEEL)],
        "সকেটের গড়ন দেশে দেশে আলাদা, কিন্তু যা যাচাই হয় তা একই",
        h=520)


def d23_neon():
    """একই ছিদ্র, একই তার — তফাত কেবল বুড়ো আঙুলে।

    ছবি দুটি একই ফ্রেমের;  টেস্টারটি দুবারই **একই ছিদ্রে**, আর
    সংযোগটি দুবারই জীবন্ত।  বাঁয়েরটিতে মাথার ধাতব প্রান্তে আঙুল নেই,
    তাই বাতি জ্বলেনি।  ছবি জোড়াটির পাঠ তাই "ফেজ বনাম নিউট্রাল" নয় —
    লাইন টেস্টারের মিথ্যা "লাইন নেই" পাঠ, যা এই বইয়ের বেশি দরকারি
    শিক্ষা।  ছবি দুটি খুঁটিয়ে না দেখে ক্যাপশন লিখলে উল্টো শেখানো হতো।
    """
    return pair_panels(
        "d23_neon", "লাইন টেস্টার যেভাবে মিথ্যা বলে",
        [("আঙুল নেই: জ্বলছে না", "ph_neon_off.jpg", RED),
         ("আঙুল আছে: জ্বলছে", "ph_neon_on.jpg", GREEN)],
        "একই ছিদ্র, একই লাইভ তার; তফাত শুধু মাথার প্রান্তে আঙুল",
        h=460)


def d24_testlamp():
    return pair_panels(
        "d24_testlamp", "নিরাপদ টেস্টের যন্ত্র",
        [("দুই-মেরু টেস্ট ল্যাম্প", "ph_testlamp.jpg", STEEL),
         ("আধুনিক ইনসুলেশন টেস্টার", "ph_ir_group.jpg", STEEL)],
        "প্রোবের খোলা ধাতু যত ছোট, ছোঁয়া লাগার ঝুঁকি তত কম",
        h=440)


ALL = [d01_why, d02_parts, d03_electrodes, d04_pit, d05_depth,
       d06_parallel, d07_order, d08_cont, d09_ir, d10_ir_limits,
       d11_pol, d12_holder, d13_fop, d14_62, d15_wenner, d16_wrong,
       d17_ir_meters, d18_ir_read, d19_earth_test, d20_rod_pit,
       d21_bar, d22_socket, d23_neon, d24_testlamp,
       ]


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
