# -*- coding: utf-8 -*-
"""অধ্যায় ২৭ — চ্যানেল ওয়্যারিং : ডায়াগ্রাম।

অধ্যায় ২৬ পাইপের ভেতর দিয়ে তার নেওয়া শিখিয়েছে।  এই অধ্যায়ের জিনিসটি
তার উল্টো — **খোলা যায় এমন একটি নালা**, দেয়ালের গায়ে বসে, উপরে ঢাকনা।
তাই ছবির ভাগটাও আলাদা:

**আঁকা চিত্র** — যা ক্যামেরায় ধরা পড়ে না:  চ্যানেলের কাটা মুখ ও মাপ,
ভরাটের হিসাব, 45° কোণা কাটা, স্ক্রুর দূরত্ব, কাজের ক্রম, ফলস
সিলিংয়ের ভেতরের ব্যবস্থা, আর যে ভুলগুলো বারবার হয়।

**আলোকচিত্র** — জিনিসটি আসলে কেমন (`assets_ch27.py`):  কেসিং ও
ক্যাপিং আলাদা করে রাখা, ক্যাপের গায়ের ছাপা মাপ, ক্যাপ খোলা চ্যানেলের
ভেতরে সাজানো তার, বসানো অবস্থায় একটি রান, আর ইনস্টিটিউটের নিজের
স্লাইড ৩৫ — ঘরের দেয়াল ধরে গোটা চ্যানেলের রান।

অধ্যায় ১৫ থেকে চলে আসা ছবির নিয়ম এখানেও কড়া:  প্যানেলের শিরোনাম
বিশেষ্য, যন্ত্রাংশের লেবেল এক-দুই শব্দ, নিচে এক লাইনের একটি নোট-পটি।
কারণ, পরামর্শ আর সতর্কবাণী সবই বইয়ের লেখায় — ছবিতে নয়।

ছবির লেবেলে যা লেখা যাবে না:  কালপুরুষে `÷ √ ² Ω φ ≤` নেই বা ভুল আঁকে।
ভাগ সবসময় `/`, বর্গমিলিমিটার কথায় — "বর্গমিমি"।  মাপ, শ্রেণি ও রেটিং
ল্যাটিন অঙ্কে (অধ্যায় ২৩-এর নিয়ম — কালপুরুষে বাংলা ৪ ল্যাটিন 8-এর
মতো আঁকে, আর চ্যানেলের মাপের ঘরে সেটি অন্য চ্যানেল হয়ে যায়)।

আঁকার সংখ্যাগুলো মুখস্থ নয় — BNBC পার্ট ৮ অধ্যায় ১, বিএস ৭৬৭১-এর
45% স্পেস ফ্যাক্টর আর আইইসি ৬০২২৭-৩-এর তারের বাইরের ব্যাস থেকে নেওয়া;
`ch27.py`-র docstring-এ প্রতিটির সূত্র লেখা আছে।
"""
import math
import os

from bookkit import bn
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch27")
IMG = os.path.join(HERE, "assets", "ch27")

# টাইপের মাপ — W-px ক্যানভাস P সেমি চওড়ায় বসলে N-px লেখা
# N × P(pt) / W পয়েন্টে ছাপে।  ১৫.৪ সেমিতে (৪৩৬.৫ pt) ১২৪০-px
# ক্যানভাসে ২২ px = ৭.৭ pt — প্রকল্পের ~৭.৫ pt মেঝের উপরে।
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
PVC = "#EDEFF2"          # চ্যানেলের বডি (কেসিং)
PVCE = "#98A2AC"         # কিনারা
CAPC = "#DFE4EA"         # ক্যাপ — একটু গাঢ়, যাতে আলাদা চেনা যায়
BORE = "#FBFCFD"         # ভেতরের ফাঁকা
WALLF = "#EFE6D8"        # ইটের দেয়াল
WALLE = "#C9B99F"
BRICK = "#DCCDB4"
SLAB = "#DDE2E7"         # কংক্রিট
SLABE = "#A9B3BE"
PLAS = "#F6F1E7"         # প্লাস্টার
STEELC = "#B9C1C9"       # স্ক্রু, ধাতব জিনিস
COPPER = "#B5713A"

# BNBC ১.৩.৯.৩.১৫ / সারণি ৮.১.২-এর রং
C_L1 = "#D42A1F"
C_N = "#1F2933"
C_PE = "#1B6E47"


# ══════════════════════════════════════════════════════════════════════
#  সাধারণ helpers (অধ্যায় ২২–২৬ থেকে চলে আসা)
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


def dim_h(s, x0, x1, y, text, col=NAVY, size=T_SMALL, tick=9):
    """আড়াআড়ি মাপের রেখা — দুই প্রান্তে দাগ, মাঝখানে লেখা।"""
    w = tw(text, size, 700)
    mid = (x0 + x1) / 2
    if x1 - x0 > w + 26:
        s.line(x0, y, mid - w / 2 - 10, y, col, 1.9)
        s.line(mid + w / 2 + 10, y, x1, y, col, 1.9)
        ty = y + size * 0.34
    else:
        s.line(x0, y, x1, y, col, 1.9)
        ty = y - size * 0.90
    for xx in (x0, x1):
        s.line(xx, y - tick, xx, y + tick, col, 1.9)
    s.text(mid, ty, text, size, col, 700, "middle")


def dim_v(s, x, y0, y1, text, col=NAVY, size=T_SMALL, tick=9, side="right"):
    s.line(x, y0, x, y1, col, 1.9)
    for yy in (y0, y1):
        s.line(x - tick, yy, x + tick, yy, col, 1.9)
    xx = x + 14 if side == "right" else x - 14
    s.text(xx, (y0 + y1) / 2 + size * 0.34, text, size, col, 700,
           "start" if side == "right" else "end")


def arrowhead(s, x, y, ang, size=13, col=STEEL):
    a = math.radians(ang)
    p = [(x, y),
         (x - size * math.cos(a - 0.42), y - size * math.sin(a - 0.42)),
         (x - size * math.cos(a + 0.42), y - size * math.sin(a + 0.42))]
    s.poly(p, col, col, 1)


# ══════════════════════════════════════════════════════════════════════
#  আলোকচিত্রের শিট (অধ্যায় ২৬-এর সেই একই)
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
    """একটি ছবির শিট — শিরোনাম, প্যানেল, এক লাইনের নোট।"""
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


def photo_grid(fname, title, rows, note, h=250, gap=24, top=100, w=1240):
    """কয়েক সারিতে ছবি-টাইল — এক সারিতে যতগুলো ধরে ততগুলো।

    `pair_panels` এক সারির;  পাঁচটি ফিটিং এক সারিতে বসাতে গেলে
    ক্যানভাস ছাড়িয়ে যায় (অধ্যায় ২৩-এর ওভারফ্লো-প্রহরী), তাই সারি
    ভাগ করা হয়।
    """
    from PIL import Image as _Im
    y = top
    s = SVG(w, top + len(rows) * (h + 78 + gap) + 120)
    s.title(title, T_TITLE)
    for row in rows:
        ws = []
        for _t, img, _c in row:
            with _Im.open(f"{IMG}/{img}") as im:
                ws.append(round(h * im.size[0] / im.size[1]) + 32)
        span = sum(ws) + gap * (len(row) - 1)
        if span > w - 24:
            raise ValueError(f"{fname}: সারিটি {span:.0f} px, "
                             f"ক্যানভাস {w} px — h কমাও")
        x = (w - span) / 2
        for (head, img, col), pw in zip(row, ws):
            img_panel(s, x, y, pw, h + 78, head, img, col)
            x += pw + gap
        y += h + 78 + gap
    y = note_strip(s, y + 2, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


def strip_callouts(fname, title, img, above, below, note,
                   iw=1160, top=100, gap=30, size=T_CALL, w=1240):
    """চওড়া-অথচ-বেঁটে ছবির জন্য কল-আউট — লেবেল উপরে ও নিচে।

    প্রতিটি এন্ট্রি:  (লেখা, লেবেলের fx, লক্ষ্যের fx, লক্ষ্যের fy)।
    """
    ih = _ih(img, iw)
    ix = (w - iw) / 2
    lh = size * 1.5
    iy = top + lh + gap
    s = SVG(w, iy + ih + lh + gap + 120)
    s.title(title, T_TITLE)
    s.image(ix, iy, iw, ih, f"{IMG}/{img}")

    def run(items, up):
        for text, lfx, tfx, tfy in items:
            lx = ix + lfx * iw
            ly = (iy - gap + size * 0.32) if up else (iy + ih + gap + size)
            s.text(lx, ly, text, size, NAVY, 700, "middle")
            y0 = (iy - gap + size * 0.32 + 12) if up else (iy + ih + gap - 8)
            tx, ty = ix + tfx * iw, iy + tfy * ih
            d = f"M {lx} {y0} L {lx} {ty}"
            if abs(tx - lx) > 1:
                d += f" L {tx} {ty}"
            s.path(d, STEEL, 2.2)
            s.circle(tx, ty, 5, STEEL)

    run(above, True)
    run(below, False)
    y = note_strip(s, iy + ih + lh + gap + 26, note)
    s.fit(y, 24)
    return s.save(f"{OUT}/{fname}.svg")


# ══════════════════════════════════════════════════════════════════════
#  অধ্যায় ২৭-এর নিজস্ব আঁকার উপাদান
# ══════════════════════════════════════════════════════════════════════
def brick_wall(s, x, y, w, h, fill=WALLF, edge=WALLE, course=34):
    """ইটের দেয়ালের কাটা-অংশ — গাঁথুনির রেখা সমেত।"""
    s.rect(x, y, w, h, fill, edge, 2.4, 3)
    s.clip_begin(x, y, w, h, 3)
    n = int(h // course)
    for i in range(1, n + 1):
        yy = y + i * course
        s.line(x, yy, x + w, yy, BRICK, 1.5)
        off = (course * 1.5) if i % 2 else 0
        k = 0
        while x + off + k * course * 2.2 < x + w:
            xx = x + off + k * course * 2.2
            s.line(xx, yy - course, xx, yy, BRICK, 1.5)
            k += 1
    s.clip_end()


def concrete(s, x, y, w, h, fill=SLAB, edge=SLABE):
    """কংক্রিটের কাটা-অংশ — ছিটে-দাগ দিয়ে।"""
    s.rect(x, y, w, h, fill, edge, 2.4, 3)
    s.clip_begin(x, y, w, h, 3)
    seed = 7
    for _i in range(int(w * h / 900)):
        seed = (seed * 1103515245 + 12345) % 2147483648
        px = x + (seed % 10000) / 10000 * w
        seed = (seed * 1103515245 + 12345) % 2147483648
        py = y + (seed % 10000) / 10000 * h
        seed = (seed * 1103515245 + 12345) % 2147483648
        rr = 1.4 + (seed % 100) / 100 * 2.2
        s.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rr:.1f}" '
              f'fill="#B9C2CB" opacity="0.55"/>')
    s.clip_end()


def wire_dot(s, cx, cy, r, col):
    """তারের কাটা মুখ — ইনসুলেশনের রিং, ভেতরে তামা।"""
    s.circle(cx, cy, r, col, "#4A5560", 1.2)
    s.circle(cx, cy, r * 0.44, "#C98B4B", "#8A5326", 1.0)


def chan_sec(s, cx, cy, W, H, t, cap=True, lift=0, cavity=BORE):
    """চ্যানেলের কাটা মুখ — নিচে U-আকৃতির কেসিং, উপরে ক্যাপ।

    `lift` > 0 হলে ক্যাপটি উপরে তুলে আঁকা হয় (খোলা অবস্থা)।
    ফেরত দেয় ভেতরের ফাঁকা জায়গার (x, y, w, h)।
    """
    ct = t * 1.7                                  # ক্যাপের পুরুত্ব
    x, y = cx - W / 2, cy - H / 2
    by = y + ct                                   # কেসিংয়ের উপরের কিনারা
    bh = H - ct
    s.rect(x, by, W, bh, PVC, PVCE, 2.4, 3)       # কেসিং
    ix, iy, iw_, ih_ = x + t, by, W - 2 * t, bh - t
    s.rect(ix, iy, iw_, ih_, cavity, PVCE, 1.6, 2)
    # দুই পাশের ঠোঁট — ক্যাপ এখানেই আটকায়
    for sx in (x + t, x + W - t):
        s.line(sx, by, sx, by + 7, PVCE, 2.0)
    if cap:
        cy0 = y - lift
        s.rect(x, cy0, W, ct, CAPC, PVCE, 2.2, 3)
        for sx in (x + t + 2, x + W - t - 2):     # ক্যাপের ভেতরের খাঁজ
            s.line(sx, cy0 + ct, sx, cy0 + ct + 6, PVCE, 2.0)
    return ix, iy, iw_, ih_


def pack_wires(s, ix, iy, iw_, ih_, n, d, col=C_L1, cols=None, pad=3):
    """ভেতরের ফাঁকায় n-টি তার সাজানো — নিচ থেকে সারি ধরে।"""
    r = d / 2
    cols = cols or max(1, int((iw_ - 2 * pad) // d))
    placed = 0
    row = 0
    while placed < n:
        k = min(cols, n - placed)
        y = iy + ih_ - pad - r - row * (d + 1.5)
        x0 = ix + pad + r
        for i in range(k):
            wire_dot(s, x0 + i * (d + 1.0), y, r,
                     col[placed + i] if isinstance(col, (list, tuple))
                     else col)
        placed += k
        row += 1
    return row


def chan_run(s, x0, x1, y, h, vert=False, cap_line=True):
    """বসানো চ্যানেলের রান — সামনে থেকে দেখা একটি পটি।"""
    if vert:
        s.rect(y, x0, h, x1 - x0, PVC, PVCE, 2.2, 2)
        if cap_line:
            s.line(y + h * 0.30, x0, y + h * 0.30, x1, PVCE, 1.5)
    else:
        s.rect(x0, y, x1 - x0, h, PVC, PVCE, 2.2, 2)
        if cap_line:
            s.line(x0, y + h * 0.30, x1, y + h * 0.30, PVCE, 1.5)


def screw(s, cx, cy, r=8, col=STEELC):
    """কাউন্টারসাঙ্ক স্ক্রুর মাথা — উপর থেকে।"""
    s.circle(cx, cy, r, col, "#6C7885", 1.6)
    s.line(cx - r * 0.62, cy, cx + r * 0.62, cy, "#5A646F", 2.0)


def plug(s, cx, cy, w=14, h=30, col="#D8CDB8"):
    """দেয়ালে বসানো রাওল প্লাগ।"""
    s.rect(cx - w / 2, cy, w, h, col, "#A2957C", 1.6, 3)
    for i in range(3):
        s.line(cx - w / 2, cy + 6 + i * 8, cx + w / 2, cy + 6 + i * 8,
               "#A2957C", 1.2)


def tile(s, x, y, w, h, name, role=None, col=STEEL):
    """ফিটিংয়ের একটি ঘর — উপরে ছবি, নিচে নাম ও এক শব্দের দৃশ্য।"""
    s.rect(x, y, w, h, PLATE, LINE, 2, 11)
    if role:
        s.text(x + w / 2, y + h - 42, name, T_SMALL, NAVY, 700, "middle")
        s.text(x + w / 2, y + h - 14, role, T_TINY, GREY, 400, "middle")
        return x + w / 2, y + (h - 62) / 2
    s.text(x + w / 2, y + h - 14, name, T_SMALL, NAVY, 700, "middle")
    return x + w / 2, y + (h - 34) / 2


# ══════════════════════════════════════════════════════════════════════
#  ১।  একটি ঘরে চ্যানেল ওয়্যারিং
# ══════════════════════════════════════════════════════════════════════
def d01_room():
    """ঘরের ভেতর থেকে দেখা একটি দেয়াল — চ্যানেল, ড্রপ ও পয়েন্ট।

    লেবেলগুলো দেয়ালের **খালি জায়গায়** — অধ্যায় ২৬-এর শিক্ষা;  মার্জিনে
    দিলে লিডার ক্যানভাস ছাড়িয়ে যায়।
    """
    s = SVG(1240, 900)
    s.title("একটি ঘরের দেয়ালে চ্যানেল ওয়্যারিং", T_TITLE)

    L, R = 96, 1144
    ceil, floor = 128, 776
    ch = 26                                      # চ্যানেলের চওড়া

    concrete(s, L, ceil - 34, R - L, 34)                    # ছাদ
    s.rect(L, ceil, R - L, floor - ceil, PLAS, "#DCD2C0", 2.2, 2)
    s.rect(L, floor, R - L, 30, "#E4DED2", "#C4BAA8", 2.2, 2)   # মেঝে

    # ── প্রধান রান:  ছাদ ঘেঁষে, দেয়াল বরাবর ──
    my = ceil + 48
    chan_run(s, L + 34, R - 34, my, ch)

    # ডিবি থেকে উঠে আসা ফিড
    dbx, dby = L + 118, 496
    s.rect(dbx - 66, dby - 54, 132, 108, "#F1F4F7", "#7C8794", 2.6, 8)
    s.rect(dbx - 50, dby - 34, 100, 40, "#FBFCFD", "#7C8794", 1.8, 4)
    s.text(dbx, dby + 34, "SDB", T_SMALL, NAVY, 700, "middle")
    chan_run(s, my + ch, dby - 54, dbx - ch / 2, ch, vert=True)

    # ── তিনটি শাখা ──
    # দেয়ালের বাতি — মূল রান থেকে নেমে আসা একটি শাখা।
    # সিলিং রোজ ইচ্ছে করে আঁকা হয়নি:  দেয়ালের এই এলিভেশনে ছাদ
    # কিনারা থেকে দেখা যায়, তাই ঝুলন্ত তার মূল রানকেই কেটে যেত।
    rx, lampy = 470, 340
    chan_run(s, my + ch, lampy, rx - ch / 2, ch, vert=True)
    s.rect(rx - 32, lampy, 64, 24, "#EDF1F5", "#7C8794", 2.2, 4)
    s.line(rx, lampy + 24, rx, lampy + 32, "#7A838D", 5)
    s.circle(rx, lampy + 64, 32, "#FFF6D8", "#D9B75A", 2.6)
    s.text(rx, lampy + 72, "★", 26, "#C79A2E", 700, "middle")

    sbx = 748                                    # সুইচ বোর্ড
    sby = floor - 288
    chan_run(s, my + ch, sby, sbx - ch / 2, ch, vert=True)
    s.rect(sbx - 86, sby, 172, 108, "#FBFCFD", "#7C8794", 2.6, 8)
    for i in range(2):
        for j in range(2):
            s.rect(sbx - 66 + j * 66, sby + 20 + i * 38, 44, 26,
                   "#EFF2F5", "#8B96A2", 1.8, 4)
    dim_v(s, sbx + 152, sby + 108, floor, "1220 mm", side="right")
    s.line(sbx + 86, sby + 108, sbx + 152, sby + 108, GREY, 1.4)
    s.line(L + 34, floor, sbx + 152, floor, GREY, 1.4, dash="6 5")

    skx = 1078                                   # সকেট
    sky = floor - 108
    chan_run(s, my + ch, sky, skx - ch / 2, ch, vert=True)
    s.rect(skx - 48, sky, 96, 78, "#FBFCFD", "#7C8794", 2.6, 8)
    s.circle(skx, sky + 30, 9, "#3C4650")
    s.circle(skx - 20, sky + 52, 9, "#3C4650")
    s.circle(skx + 20, sky + 52, 9, "#3C4650")

    # ── স্ক্রু, সমান দূরত্বে ──
    for x in range(L + 74, R - 40, 96):
        screw(s, x, my + ch / 2, 7)
    dim_h(s, L + 458, L + 554, my + ch + 42, "300 mm")

    # ── লেবেল, দেয়ালের খালি জায়গায় ──
    callout(s, 250, my + ch + 58, "প্রধান রান", 300, my + ch + 2, "start")
    callout(s, 690, 300, "বাতির শাখা", rx + ch / 2, 262, "middle")
    callout(s, dbx + ch / 2 + 34, 380, "ডিবি থেকে ফিড", dbx + ch / 2, 372,
            "start")
    callout(s, 610, 700, "সুইচ বোর্ড", sbx - 86, sby + 54, "end")
    callout(s, skx - 62, sky - 16, "সকেট", skx - 48, sky + 22, "end")

    y = note_strip(s, 826,
                   "দেয়ালে চ্যানেল শুধু খাড়া বা আড়াআড়ি; কোনাকুনি নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_room.svg")


# ══════════════════════════════════════════════════════════════════════
#  ২।  চ্যানেলের গঠন ও মাপ
# ══════════════════════════════════════════════════════════════════════
def d02_anatomy():
    """কেসিং ও ক্যাপিং — খোলা, লাগানো, আর মাপ কোথা থেকে।"""
    s = SVG(1240, 680)
    s.title("চ্যানেলের গঠন ও মাপ", T_TITLE)

    PW, PH = 384, 420
    x0, top = 26, 96
    gap = 20
    W, H, t = 232, 150, 15

    # ── প্যানেল ১:  খোলা ──
    panel(s, x0, top, PW, PH, "খোলা অবস্থা")
    cx, cy = x0 + PW / 2, top + 250
    chan_sec(s, cx, cy, W, H, t, cap=True, lift=59)
    for dx in (-58, 58):
        s.path(f"M {cx + dx} {top + 152} L {cx + dx} {top + 186}", STEEL, 2.6)
        arrowhead(s, cx + dx, top + 188, 90)
    s.text(cx, top + 88, "ক্যাপিং", T_NAME, NAVY, 700, "middle")
    s.text(cx, top + PH - 22, "কেসিং", T_NAME, NAVY, 700, "middle")

    # ── প্যানেল ২:  লাগানো + মাপ ──
    x1 = x0 + PW + gap
    panel(s, x1, top, PW, PH, "লাগানো অবস্থা")
    cx2, cy2 = x1 + PW / 2 - 16, top + 214
    ix2, iy2, iw2, ih2 = chan_sec(s, cx2, cy2, W, H, t)
    pack_wires(s, ix2, iy2, iw2, ih2, 3, 26, col=(C_L1, C_N, C_PE))
    dim_h(s, cx2 - W / 2, cx2 + W / 2, cy2 + H / 2 + 40, "W")
    dim_v(s, cx2 + W / 2 + 44, cy2 - H / 2, cy2 + H / 2, "H")
    s.text(x1 + PW / 2, top + PH - 22,
           "W × H: বাইরের মাপ", T_SMALL, NAVY, 700, "middle")

    # ── প্যানেল ৩:  ভেতরের মাপ ──
    x2 = x1 + PW + gap
    panel(s, x2, top, PW, PH, "ভেতরের মাপ")
    cx3, cy3 = x2 + PW / 2 - 10, top + 214
    ix3, iy3, iw3, ih3 = chan_sec(s, cx3, cy3, W, H, t, cap=False)
    s.rect(ix3, iy3, iw3, ih3, "#FDF6E3", "#D9B75A", 2.4, 2)
    dim_h(s, ix3, ix3 + iw3, cy3 + H / 2 + 40, "w")
    dim_v(s, ix3 + iw3 + 62, iy3, iy3 + ih3, "h")
    callout(s, x2 + 86, top + 108, "দেয়ালের পুরুত্ব t",
            ix3 - t / 2, iy3 + ih3 * 0.62, "start")
    s.text(x2 + PW / 2, top + PH - 22,
           "w = W − 2t · h = H − 2t", T_SMALL, NAVY, 700, "middle")

    y = note_strip(s, top + PH + 30,
                   "বাজার W × H বলে, হিসাব চলে w × h দিয়ে; মেপে নিতে হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_anatomy.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৩।  চ্যানেল বনাম কন্ডুইট
# ══════════════════════════════════════════════════════════════════════
def d03_vs():
    """একই দেয়ালে দুই পদ্ধতি — একটি ভেতরে, একটি বাইরে।"""
    s = SVG(1240, 760)
    s.title("চ্যানেল ও কন্ডুইট: একই দেয়ালে", T_TITLE)

    PW, PH = 586, 444
    top = 96
    xs = (26, 26 + PW + 30)
    heads = ("চ্যানেল: দেয়ালের গায়ে", "কন্ডুইট: দেয়ালের ভেতরে")

    for k, (x, hd) in enumerate(zip(xs, heads)):
        panel(s, x, top, PW, PH, hd)
        wx, wy, ww, wh = x + 46, top + 82, PW - 92, 150
        brick_wall(s, wx, wy, ww, wh)
        s.rect(wx, wy + wh, ww, 22, PLAS, "#DCD2C0", 1.8, 2)
        if k == 0:
            cy = wy + wh + 22 + 42
            s.rect(wx + 110, cy - 42, ww - 220, 84, PVC, PVCE, 2.4, 3)
            s.line(wx + 110, cy - 42 + 26, wx + ww - 110, cy - 42 + 26,
                   PVCE, 1.6)
            for i in range(3):
                wire_dot(s, wx + 162 + i * 46, cy + 12, 13, C_L1)
            screw(s, wx + 170, cy - 26, 7)
            screw(s, wx + ww - 170, cy - 26, 7)
            sub = "প্লাস্টারের উপরে: খুলে ফেলা যায়"
            foot = "বাড়তি কাজে চ্যানেল"
        else:
            cyy = wy + wh * 0.52
            s.rect(wx + 110, cyy - 34, ww - 220, 68, "#E9DFCB",
                   "#C9B99F", 2.0, 3)
            s.circle(wx + ww / 2, cyy, 30, PVC, PVCE, 2.4)
            s.circle(wx + ww / 2, cyy, 21, BORE, PVCE, 1.8)
            for i, c in enumerate((C_L1, C_N, C_PE)):
                ang = math.radians(90 + i * 120)
                wire_dot(s, wx + ww / 2 + 10 * math.cos(ang),
                         cyy + 10 * math.sin(ang), 8, c)
            sub = "ঢালাইয়ের ভেতরে: আর খোলা যায় না"
            foot = "নতুন কাজে কন্ডুইট"
        s.text(x + PW / 2, top + PH - 68, sub, T_SMALL, NAVY, 700, "middle")
        s.text(x + PW / 2, top + PH - 24, foot, T_BODY, NAVY, 700, "middle")

    y = note_strip(s, top + PH + 30,
                   "একটি খোলা যায় বলেই সস্তা;  অন্যটি খোলা যায় না বলেই টেকে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_vs.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৪।  BNBC — কোথায় চলবে, কোথায় নয়
# ══════════════════════════════════════════════════════════════════════
def d04_where():
    """কোড কী বলে — দুই কলামে, ধারার নম্বরসহ।"""
    s = SVG(1240, 720)
    s.title("চ্যানেল কোথায় চলবে, কোথায় নয়", T_TITLE)

    top = 96
    PW = 586
    xs = (26, 26 + PW + 30)
    ok_items = [("পুরোনো ভবনে বাড়তি কাজ", "1.3.14.1.2"),
                ("ফলস সিলিংয়ের ভেতরে", "1.3.11.3"),
                ("অল্প দৈর্ঘ্যের রান", "1.3.14.1.2"),
                ("সারফেস ওয়্যারিং, একক-কোর তার", "1.3.11.1.3")]
    no_items = [("নতুন ভবনের নকশায়", "1.3.14.1.2"),
                ("লম্বা রানে: কন্ডুইট", "1.3.14.1.2"),
                ("অনেকগুলো তার একসঙ্গে", "1.3.14.1.2"),
                ("মোটা ক্যাবলে", "1.3.14.1.2")]

    for x, (hd, items, ok) in zip(
            xs, (("চলবে", ok_items, True), ("চলবে না", no_items, False))):
        col, bg = (GREEN, GREENBG) if ok else (RED, REDBG)
        head_bar(s, x, top, PW, 64, hd, col)
        yy = top + 82
        for text, cl in items:
            s.rect(x, yy, PW, 82, bg, col, 2.2, 10)
            s.text(x + 26, yy + 34, "✔" if ok else "✗", T_NODE, col, 700,
                   "start")
            s.text(x + 66, yy + 34, text, T_BODY, NAVY, 700, "start")
            s.text(x + 66, yy + 66, "BNBC " + cl, T_SMALL, col, 700,
                   "start")
            yy += 92

    y = note_strip(s, yy + 12,
                   "কোড বলে: নকশায় চ্যানেল দেখানোই উচিত নয়, "
                   "ফলস সিলিং ছাড়া")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_where.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৫।  ফিটিং
# ══════════════════════════════════════════════════════════════════════
def _fit_L(s, cx, cy, a=104, w=34, inner=True):
    """সমতলে ৯০° মোড় — দেয়ালের সমতলেই, একটি টুকরো।"""
    if inner:
        s.path(f"M {cx - a} {cy - w / 2} L {cx + w / 2} {cy - w / 2} "
               f"L {cx + w / 2} {cy + a} L {cx - w / 2} {cy + a} "
               f"L {cx - w / 2} {cy + w / 2} L {cx - a} {cy + w / 2} Z",
               PVCE, 2.2, PVC)
        s.line(cx - a, cy, cx - w / 2, cy, PVCE, 1.4)
        s.line(cx, cy + w / 2, cx, cy + a, PVCE, 1.4)
    else:
        s.path(f"M {cx + a} {cy + w / 2} L {cx - w / 2} {cy + w / 2} "
               f"L {cx - w / 2} {cy - a} L {cx + w / 2} {cy - a} "
               f"L {cx + w / 2} {cy - w / 2} L {cx + a} {cy - w / 2} Z",
               PVCE, 2.2, PVC)


def _corner_plan(s, cx, cy, inner=True, arm=84, wt=32, cw=20):
    """দেয়ালের কোণা — **উপর থেকে** দেখা, গায়ে চ্যানেল।

    দুটি কোণা আঁকার একমাত্র সৎ দৃশ্য এটিই:  সামনে থেকে আঁকলে ভেতরের
    আর বাইরের কোণা হুবহু একই দেখায়, আর তখন ছবিটা কিছুই শেখায় না।
    ফিটিংটুকু আলাদা রঙে — কোন টুকরোটি কেনা লাগবে সেটিই মূল কথা।
    """
    if inner:
        # ঘর নিচে-ডানে, দেয়াল উপরে ও বাঁয়ে — কোণ অবতল
        x0, y0 = cx - arm, cy - arm
        s.poly([(x0, y0), (x0 + 2 * arm, y0), (x0 + 2 * arm, y0 + wt),
                (x0 + wt, y0 + wt), (x0 + wt, y0 + 2 * arm),
                (x0, y0 + 2 * arm)], WALLF, WALLE, 2.2)
        fx, fy = x0 + wt, y0 + wt
        s.rect(fx, fy, 2 * arm - wt, cw, PVC, PVCE, 2.2, 2)
        s.rect(fx, fy, cw, 2 * arm - wt, PVC, PVCE, 2.2, 2)
        s.rect(fx - 3, fy - 3, cw + 28, cw + 28, CAPC, STEEL, 2.8, 4)
    else:
        # দেয়ালের বেরিয়ে থাকা পিলার — কোণ উত্তল, চ্যানেল বাইরে দিয়ে
        pw = arm * 1.42
        px, py = cx - pw * 0.66, cy - pw * 0.62
        s.rect(px, py, pw, pw, WALLF, WALLE, 2.2, 2)
        ex, ey = px + pw, py + pw
        s.rect(px - 34, ey, pw + 34 + cw, cw, PVC, PVCE, 2.2, 2)
        s.rect(ex, py - 34, cw, pw + 34 + cw, PVC, PVCE, 2.2, 2)
        s.rect(ex - 6, ey - 6, cw + 24, cw + 24, CAPC, STEEL, 2.8, 4)


def d05_parts():
    """চ্যানেলের ফিটিং — ছয়টি ঘর, প্রতিটির নিচে নাম ও দৃশ্য।"""
    s = SVG(1240, 660)
    s.title("চ্যানেলের ফিটিং", T_TITLE)

    top = 96
    TWD, THT = 384, 244
    gap = 22
    names = [("সমতল কোণা", "সমতলে"), ("ভেতরের কোণা", "উপর থেকে"),
             ("বাইরের কোণা", "উপর থেকে"), ("টি-জোড়া", "সমতলে"),
             ("কাপলার", "সমতলে"), ("এন্ড ক্যাপ", "সমতলে")]
    for i, (nm, role) in enumerate(names):
        c, r = i % 3, i // 3
        x = 26 + c * (TWD + gap)
        y = top + r * (THT + gap)
        cx, cy = tile(s, x, y, TWD, THT, nm, role)
        w = 34
        if i == 0:
            _fit_L(s, cx, cy - 10, 88, w)
        elif i == 1:
            _corner_plan(s, cx, cy, inner=True, arm=82, wt=30, cw=20)
        elif i == 2:
            _corner_plan(s, cx, cy, inner=False, arm=82, cw=20)
        elif i == 3:
            s.rect(cx - 100, cy - w / 2, 200, w, PVC, PVCE, 2.2, 3)
            s.rect(cx - w / 2, cy - w / 2, w, 74, PVC, PVCE, 2.2, 3)
            s.line(cx - 100, cy, cx - w / 2, cy, PVCE, 1.4)
            s.line(cx + w / 2, cy, cx + 100, cy, PVCE, 1.4)
        elif i == 4:
            s.rect(cx - 104, cy - w / 2, 96, w, PVC, PVCE, 2.2, 3)
            s.rect(cx + 8, cy - w / 2, 96, w, PVC, PVCE, 2.2, 3)
            s.rect(cx - 30, cy - w / 2 - 8, 60, w + 16, CAPC, PVCE, 2.4, 4)
        else:
            s.rect(cx - 104, cy - w / 2, 152, w, PVC, PVCE, 2.2, 3)
            s.rect(cx + 48, cy - w / 2 - 7, 22, w + 14, CAPC, PVCE, 2.4, 4)

    y = note_strip(s, top + 2 * (THT + gap) + 14,
                   "ফিটিং না থাকলে মাপে কেটে জোড়া দিতে হয়; মুখ খোলা "
                   "রাখা যায় না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_parts.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৬।  কোণা কাটা
# ══════════════════════════════════════════════════════════════════════
def d06_corner():
    """45° মাইটার — কেন, আর কোন টুকরোয় কোন দিকে।"""
    s = SVG(1240, 700)
    s.title("কোণায় 45° কাটা (মাইটার)", T_TITLE)

    top = 96
    PW, PH = 384, 392
    gap = 22
    heads = ("ভুল: মুখোমুখি কাটা", "সঠিক: দুই টুকরো 45°", "জোড়া লাগার পর")

    for i, hd in enumerate(heads):
        x = 26 + i * (PW + gap)
        panel(s, x, top, PW, PH, hd)
        cx, cy = x + PW / 2, top + 210
        w = 40
        if i == 0:
            s.rect(cx - 130, cy - w / 2, 130, w, PVC, PVCE, 2.2, 2)
            s.rect(cx - w / 2, cy - w / 2, w, 130, PVC, PVCE, 2.2, 2)
            s.rect(cx - w / 2 - 3, cy - w / 2 - 3, w + 6, w + 6,
                   REDBG, RED, 2.6, 3)
            s.text(cx + 74, cy - 44, "ফাঁক", T_SMALL, RED, 700, "middle")
            s.path(f"M {cx + 46} {cy - 34} L {cx + 10} {cy - 8}", RED, 2.2)
        elif i == 1:
            s.path(f"M {cx - 132} {cy - w / 2} L {cx + w / 2} {cy - w / 2} "
                   f"L {cx - w / 2} {cy + w / 2} L {cx - 132} {cy + w / 2} Z",
                   PVCE, 2.4, PVC)
            s.path(f"M {cx - w / 2} {cy + w / 2 + 30} "
                   f"L {cx + w / 2} {cy - w / 2 + 30} "
                   f"L {cx + w / 2} {cy + 146} L {cx - w / 2} {cy + 146} Z",
                   PVCE, 2.4, PVC)
            # দুই কাটা মুখ একই সমতলে — সবুজ ডটেড রেখাটিই তা দেখায়
            s.path(f"M {cx + w / 2 + 26} {cy - w / 2 - 26} "
                   f"L {cx - w / 2 - 26} {cy + w / 2 + 26}", GREEN, 2.4,
                   dash="9 6")
            s.text(cx + 104, cy - 34, "45°", T_SMALL, GREEN, 700, "middle")
            s.path(f"M {cx + 76} {cy - 28} L {cx + 30} {cy - 20}", GREEN, 2.2)
        else:
            _fit_L(s, cx - 6, cy - 6, 128, w)
            s.path(f"M {cx + w / 2 - 6} {cy - w / 2 - 6} "
                   f"L {cx - w / 2 - 6} {cy + w / 2 - 6}", GREEN, 3.2,
                   dash="9 6")
            s.text(cx - 6 - w / 2 - 16, cy + 84, "কোনো ফাঁক নেই", T_SMALL,
                   GREEN, 700, "end")

    y = note_strip(s, top + PH + 30,
                   "সমতল কোণা 45°;  দেয়ালের ভেতরের ও বাইরের কোণায় "
                   "ফিটিং লাগে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_corner.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৭।  ভরাটের হিসাব
# ══════════════════════════════════════════════════════════════════════
def d07_fill():
    """একই চ্যানেলে তিন রকম ভরাট — তিনটি রায়।"""
    s = SVG(1240, 700)
    s.title("চ্যানেলে কতগুলো তার: ভরাটের হিসাব", T_TITLE)

    top = 96
    PW, PH = 384, 360
    gap = 22
    # 25 × 16 চ্যানেল, t = 1.2 → ভেতরে 22.6 × 13.6 = 307 বর্গমিমি
    # 2.5 বর্গমিমি তারের বাইরের ব্যাস 3.72 → ক্ষেত্রফল 10.87 বর্গমিমি
    cases = [(3, "33 বর্গমিমি: 11%", True, "প্রচুর জায়গা"),
             (12, "130 বর্গমিমি: 42%", True, "সীমার ভেতরে"),
             (18, "196 বর্গমিমি: 64%", False, "ক্যাপ বসবে না")]

    for i, (n, area, ok, verd) in enumerate(cases):
        x = 26 + i * (PW + gap)
        panel(s, x, top, PW, PH, f"{bn(n)}টি তার")
        cx, cy = x + PW / 2, top + 172
        W, H, t = 246, 158, 15
        # শেষ ঘরে ক্যাপ তুলে আঁকা — তার ছাপিয়ে গেছে বলেই বসছে না
        ix, iy, iw_, ih_ = chan_sec(s, cx, cy, W, H, t, lift=0 if ok else 30)
        pack_wires(s, ix, iy, iw_, ih_, n, 26)
        s.text(cx, top + PH - 82, area, T_BODY, NAVY, 700, "middle")
        col = GREEN if ok else RED
        s.text(cx, top + PH - 40, ("✔  " if ok else "✗  ") + verd,
               T_BODY, col, 700, "middle")

    yy = top + PH + 26
    yy = verdict(s, 26, yy, 1188, True,
                 "25 × 16 চ্যানেল · ভেতরে 307 বর্গমিমি · সীমা 45% = "
                 "138 বর্গমিমি · 2.5 বর্গমিমি তার প্রতিটি 10.87 বর্গমিমি")
    y = note_strip(s, yy + 22,
                   "সীমা BS 7671-এর; ট্রাঙ্কিং ও চ্যানেলে 45%, "
                   "কন্ডুইটে 35%")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_fill.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৮।  বসানো — স্ক্রু, প্লাগ, সোজা লাইন
# ══════════════════════════════════════════════════════════════════════
def d08_fix():
    """চ্যানেল দেয়ালে কীভাবে আটকায় — কাটা-ছবি ও দুটি রান।"""
    s = SVG(1240, 800)
    s.title("চ্যানেল দেয়ালে আটকানো", T_TITLE)

    top = 96
    PW, PH = 586, 440

    # ── বাঁ প্যানেল:  কাটা-ছবি ──
    # দেয়ালটি ইচ্ছে করে সরু — ডানপাশে লেবেলের জন্য একটি কলাম রাখা
    # হয়েছে।  দেয়ালের গাঁথুনির রেখা লেবেলের বাক্সে ঢুকলে `qc.py`
    # ঠিকই ধরে (অধ্যায় ২৬-এর শিক্ষা)।
    panel(s, 26, top, PW, PH, "কাটা-ছবি")
    wx, wy, ww, wh = 62, top + 96, 300, 150
    brick_wall(s, wx, wy, ww, wh)
    s.rect(wx, wy + wh, ww, 20, PLAS, "#DCD2C0", 1.8, 2)
    cy = wy + wh + 20 + 48
    s.rect(wx + 40, cy - 48, ww - 80, 96, PVC, PVCE, 2.4, 3)
    s.line(wx + 40, cy - 48 + 28, wx + ww - 40, cy - 48 + 28, PVCE, 1.6)
    for i in range(3):
        wire_dot(s, wx + 92 + i * 48, cy + 16, 14, C_L1)
    sx = wx + ww / 2
    plug(s, sx, wy + wh - 52, 16, 48)
    s.line(sx, wy + wh - 46, sx, cy - 34, "#7C8794", 5)
    screw(s, sx, cy - 32, 9)
    callout(s, 452, top + 152, "রাওল প্লাগ", sx + 8, wy + wh - 30, "start")
    callout(s, 452, top + 224, "স্ক্রু", sx + 12, cy - 32, "start")
    callout(s, 452, top + 296, "কেসিং", wx + ww - 44, cy + 2, "start")

    # ── ডান প্যানেল:  সোজা বনাম ঝুলে যাওয়া ──
    x1 = 26 + PW + 30
    panel(s, x1, top, PW, PH, "রান")
    yy = top + 118
    s.rect(x1 + 34, yy - 21, PW - 68, 42, PVC, PVCE, 2.4, 3)
    s.line(x1 + 34, yy - 9, x1 + PW - 34, yy - 9, PVCE, 1.5)
    for i in range(5):
        screw(s, x1 + 78 + i * 106, yy, 8)
    dim_h(s, x1 + 78, x1 + 78 + 106, yy - 54, "300 mm")
    s.text(x1 + PW / 2, yy + 64, "✔  সোজা, ঝোলে না", T_BODY, GREEN,
           700, "middle")

    yy = top + 286
    d = (f"M {x1 + 34} {yy - 20} Q {x1 + PW / 2} {yy + 40} "
         f"{x1 + PW - 34} {yy - 20} L {x1 + PW - 34} {yy + 22} "
         f"Q {x1 + PW / 2} {yy + 82} {x1 + 34} {yy + 22} Z")
    s.path(d, PVCE, 2.4, PVC)
    screw(s, x1 + 60, yy - 2, 8)
    screw(s, x1 + PW - 60, yy - 2, 8)
    s.text(x1 + PW / 2, yy + 116, "✗  স্ক্রু কম: ঝুলে গেছে", T_BODY, RED,
           700, "middle")

    y = note_strip(s, top + PH + 30,
                   "ড্রিল করে রাওল প্লাগ, তারপর কাউন্টারসাঙ্ক "
                   "গ্যালভানাইজড স্ক্রু")
    s.fit(y, 24)
    return s.save(f"{OUT}/d08_fix.svg")


# ══════════════════════════════════════════════════════════════════════
#  ৯।  কাজের ক্রম
# ══════════════════════════════════════════════════════════════════════
def d09_steps():
    """আট ধাপ — উপর থেকে নিচে, দুই সারিতে।"""
    s = SVG(1240, 620)
    s.title("চ্যানেল ওয়্যারিংয়ের কাজের ক্রম", T_TITLE)

    steps = ["লে-আউট ও দাগ কাটা", "মাপে কেটে নেওয়া", "কোণা 45° কাটা",
             "ড্রিল ও রাওল প্লাগ", "কেসিং স্ক্রু করা", "তার বসানো",
             "ক্যাপ চেপে বসানো", "টেস্ট ও হস্তান্তর"]
    top = 100
    BW, BH = 268, 108
    gapx, gapy = 26, 92
    for i, t_ in enumerate(steps):
        c, r = i % 4, i // 4
        x = 26 + c * (BW + gapx)
        y = top + r * (BH + gapy)
        s.rect(x, y, BW, BH, PLATE, STEEL, 2.6, 12)
        s.circle(x + 34, y + 34, 22, NAVY, NAVY, 1)
        s.text(x + 34, y + 42, str(i + 1), T_BODY, "#FFFFFF", 700,
               "middle")
        for j, ln in enumerate(wrap(t_, BW - 40, T_BODY, 700)):
            s.text(x + BW / 2, y + 76 + j * 28, ln, T_BODY, NAVY, 700,
                   "middle")
        if c < 3:
            s.path(f"M {x + BW + 4} {y + BH / 2} "
                   f"L {x + BW + gapx - 6} {y + BH / 2}", STEEL, 2.6)
            arrowhead(s, x + BW + gapx - 4, y + BH / 2, 0)
        elif r == 0:
            s.path(f"M {x + BW / 2} {y + BH + 6} "
                   f"L {x + BW / 2} {y + BH + 30} L {26 + BW / 2} "
                   f"{y + BH + 30} L {26 + BW / 2} {y + BH + gapy - 6}",
                   STEEL, 2.6)
            arrowhead(s, 26 + BW / 2, y + BH + gapy - 4, 90)

    y = note_strip(s, top + 2 * BH + gapy + 26,
                   "তার আগে, ক্যাপ পরে; ক্যাপ লাগানোর পর তার ঢোকানো যায় না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d09_steps.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১০।  ফলস সিলিংয়ের ভেতরে
# ══════════════════════════════════════════════════════════════════════
def d10_ceiling():
    """ঝুলন্ত সিলিংয়ের উপরে চ্যানেল — সঠিক ও ভুল, পাশাপাশি।"""
    s = SVG(1240, 700)
    s.title("ফলস সিলিংয়ের ভেতরে", T_TITLE)

    top = 96
    PW, PH = 586, 400
    for k, (x, hd) in enumerate(zip((26, 26 + PW + 30),
                                    ("সঠিক", "নিষিদ্ধ"))):
        panel(s, x, top, PW, PH, hd, GREEN if k == 0 else RED)
        concrete(s, x + 34, top + 82, PW - 68, 38)          # ছাদ
        gy = top + 246                                       # ফলস সিলিং
        s.rect(x + 34, gy, PW - 68, 22, "#F1EFE9", "#C9C3B4", 2.2, 2)
        for fr in (0.18, 0.82):                              # হ্যাঙ্গার
            hx = x + 34 + fr * (PW - 68)
            s.line(hx, top + 120, hx, gy, "#9AA3AC", 2.4)
        if k == 0:
            s.rect(x + 96, gy - 52, PW - 192, 40, PVC, PVCE, 2.4, 3)
            s.line(x + 96, gy - 52 + 12, x + PW - 96, gy - 52 + 12,
                   PVCE, 1.5)
            s.rect(x + PW / 2 - 46, gy - 128, 92, 62, "#EDF1F5",
                   "#7C8794", 2.4, 6)
            s.line(x + PW / 2, gy - 66, x + PW / 2, gy - 52, PVCE, 6)
            s.text(x + PW / 2, gy - 92, "জংশন", T_SMALL, NAVY, 700,
                   "middle")
            s.text(x + PW / 2, gy + 82,
                   "চ্যানেলের ভেতরে তার, জোড়া বাক্সে",
                   T_BODY, GREEN, 700, "middle")
        else:
            d = (f"M {x + 76} {gy - 22} Q {x + 190} {gy - 78} "
                 f"{x + 300} {gy - 20} T {x + PW - 76} {gy - 40}")
            s.path(d, C_L1, 6)
            s.path(d.replace(str(gy - 22), str(gy - 8)), C_N, 6)
            s.rect(x + PW / 2 - 34, gy - 66, 68, 22, "#3C4650",
                   "#22292F", 1.8, 4)
            s.text(x + PW / 2, gy + 82,
                   "খোলা তার, টেপ-মোড়া জোড়া",
                   T_BODY, RED, 700, "middle")

    y = note_strip(s, top + PH + 30,
                   "ফলস সিলিংয়ের ভেতরেও চ্যানেল বা কন্ডুইট; "
                   "খোলা তার নয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d10_ceiling.svg")


# ══════════════════════════════════════════════════════════════════════
#  ১১।  যে ভুলগুলো বারবার হয়
# ══════════════════════════════════════════════════════════════════════
def d11_wrong():
    """চারটি চেনা ভুল — ছবিতে, এক শব্দের নামসহ।"""
    s = SVG(1240, 640)
    s.title("যে ভুলগুলো বারবার হয়", T_TITLE)

    top = 96
    TWD, THT = 286, 250
    gap = 20
    names = ["ভেতরে জোড়া", "কোনাকুনি রান", "ঠাসা তার", "খোলা মুখ"]
    for i, nm in enumerate(names):
        x = 26 + i * (TWD + gap)
        s.rect(x, top, TWD, THT, REDBG, RED, 2.4, 12)
        s.text(x + TWD / 2, top + THT - 18, nm, T_BODY, RED, 700, "middle")
        cx, cy = x + TWD / 2, top + 116
        if i == 0:                                    # ভেতরে জোড়া
            s.rect(x + 26, cy - 34, TWD - 52, 68, PVC, PVCE, 2.4, 3)
            s.line(x + 46, cy, x + TWD / 2 - 10, cy, C_L1, 6)
            s.line(x + TWD / 2 + 10, cy, x + TWD - 46, cy, C_L1, 6)
            s.rect(cx - 22, cy - 12, 44, 24, "#3C4650", "#22292F", 1.8, 3)
        elif i == 1:                                  # কোনাকুনি
            brick_wall(s, x + 26, cy - 62, TWD - 52, 124)
            s.path(f"M {x + 44} {cy + 44} L {x + TWD - 44} {cy - 44}",
                   PVCE, 26)
            s.path(f"M {x + 44} {cy + 44} L {x + TWD - 44} {cy - 44}",
                   PVC, 20)
        elif i == 2:                                  # ঠাসা
            ix, iy, iw_, ih_ = chan_sec(s, cx, cy, 176, 116, 13, cap=False)
            pack_wires(s, ix, iy, iw_, ih_, 15, 22)
            # ক্যাপ হেলে আছে — এক কিনারা বসেছে, অন্যটি তারের উপরে
            s.poly([(cx - 88, cy - 46), (cx + 88, cy - 66),
                    (cx + 88, cy - 44), (cx - 88, cy - 24)],
                   CAPC, PVCE, 2.4)
        else:                                         # খোলা মুখ
            s.rect(x + 26, cy - 30, TWD - 96, 60, PVC, PVCE, 2.4, 3)
            for j in range(3):
                s.line(x + TWD - 74, cy - 16 + j * 16, x + TWD - 34,
                       cy - 24 + j * 20, C_L1, 5)

    y = note_strip(s, top + THT + 30,
                   "চারটিই BNBC-বিরোধী; কোন ধারায়, তা পাঠে বলা আছে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d11_wrong.svg")


# ══════════════════════════════════════════════════════════════════════
#  আলোকচিত্রের শিট
# ══════════════════════════════════════════════════════════════════════
def d12_piece():
    return pair_panels(
        "d12_piece", "কেসিং ও ক্যাপিং: আসল জিনিস",
        [("দুই মাপ, ক্যাপ লাগানো", "ph_pair.jpg", STEEL),
         ("ক্যাপ খোলা", "ph_piece.jpg", STEEL)],
        "নিচের U-অংশ কেসিং, উপরের ঢাকনা ক্যাপিং",
        h=330)


def d13_mark():
    return strip_callouts(
        "d13_mark", "ক্যাপের গায়ের লেখা",
        "ph_mark.jpg",
        [("প্রস্তুতকারক", 0.22, 0.22, 0.105),
         ("মাপ: 20 × 12 mm", 0.63, 0.63, 0.105)],
        [("উপাদান ও ধরন", 0.80, 0.80, 0.862)],
        "মাপ গায়েই ছাপা থাকে; কিনতে গিয়ে অনুমান করার দরকার নেই",
        iw=1060)


def d14_wire():
    return pair_panels(
        "d14_wire", "চ্যানেলের ভেতরে তার",
        [("সাজানো তার", "ph_open.jpg", STEEL),
         ("মুখ দিয়ে বেরোনো", "ph_wirein.jpg", STEEL)],
        "তার পাশাপাশি শোয়ানো; মোচড়ানো বা চাপাচাপি নয়",
        h=300)


def d15_run():
    return sheet(
        "d15_run", "বসানো অবস্থায় একটি রান",
        "ছাদ ও দেয়ালের কোণ ধরে", "ph_run.jpg",
        "টি-জোড়া থেকে বাতির শাখা নেমেছে",
        iw=880)


def d16_dado():
    return sheet(
        "d16_dado", "চ্যানেলের গায়েই আউটলেট",
        "সকেট-সমেত চ্যানেল", "ph_dado.jpg",
        "অফিসে ডেস্কের উচ্চতায়; বাসায় এটি কম চলে",
        iw=1120)


def d17_slide():
    return sheet(
        "d17_slide", "একটি ঘরের গোটা চ্যানেল রান",
        "মিটার ও এসডিবি থেকে প্রতিটি পয়েন্ট", "h35_room.png",
        "প্রতিটি পয়েন্ট চ্যানেল ধরেই; খোলা তার কোথাও নেই",
        iw=1140)


def d18_scorner():
    return sheet(
        "d18_scorner", "নকশায় কোণা যেভাবে আঁকা হয়",
        "দুই কোণা ও একটি টি-জোড়া", "h35_corner.png",
        "নকশার কোণায় ওই V-দাগটিই বাস্তবে 45° কাটা মুখ",
        iw=1000)


def d19_fitreal():
    """২৭.৪ — আসল ফিটিং, দোকানে যেমন পাওয়া যায়।"""
    return photo_grid(
        "d19_fitreal", "ফিটিং: আসল জিনিস",
        [[("ভেতরের কোণা", "ph_fit_in.jpg", STEEL),
          ("বাইরের কোণা", "ph_fit_ex.jpg", STEEL),
          ("টি-জোড়া", "ph_fit_tee.jpg", STEEL)],
         [("কাপলার", "ph_fit_cpl.jpg", STEEL),
          ("জাংশন বক্স", "ph_fit_box.jpg", STEEL)]],
        "প্রতিটি ফিটিং মাপ ধরে আলাদা; 20 × 12-এর কোণা 25 × 16-এ বসে না",
        h=250)


def d20_plug():
    """২৭.৬.৪ — রাওল প্লাগ ও স্ক্রু।"""
    return pair_panels(
        "d20_plug", "রাওল প্লাগ ও স্ক্রু",
        [("একটি জোড়া", "ph_plug.jpg", STEEL),
         ("তিন মাপ", "ph_plugsz.jpg", STEEL)],
        "প্লাগের মাপ, ড্রিল বিটের মাপ ও স্ক্রুর মাপ; তিনটিই মিলতে হবে",
        h=240)


def d21_capfit():
    """২৭.৬.৫ — ক্যাপ কীভাবে বসে।"""
    return sheet(
        "d21_capfit", "ক্যাপ যেভাবে বসে",
        "কেসিং ও ক্যাপ", "ph_capfit.jpg",
        "ক্যাপ খাঁজে আটকে বসে; আলাদা স্ক্রু লাগে না",
        iw=940, w=1240)


ALL = [d01_room, d02_anatomy, d03_vs, d04_where, d05_parts, d06_corner,
       d07_fill, d08_fix, d09_steps, d10_ceiling, d11_wrong,
       d12_piece, d13_mark, d14_wire, d15_run, d16_dado, d17_slide,
       d18_scorner, d19_fitreal, d20_plug, d21_capfit,
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
