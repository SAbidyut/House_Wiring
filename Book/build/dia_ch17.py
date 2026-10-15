# -*- coding: utf-8 -*-
"""অধ্যায় ১৭ — বিদ্যুৎ বিল : ডায়াগ্রাম।

সোর্স পিপিটিতে বিলের কোনো ছবি নেই — `HW Connection Diagram All.pptx` ও
`Circuit Diagram.pptx` দুটোই কানেকশনের বই, হিসাবের নয়।  তাই পাঁচটি ছবিই
নতুন করে আঁকা: মিটারের পাঠ, বিল তৈরির ধাপ, ট্যারিফের ধাপ, বিলের নমুনা
কাগজ আর প্রিপেইড-পোস্টপেইডের তুলনা।

লেবেলের নিয়ম (অধ্যায় ১৫ থেকে কড়া):  প্যানেলের শিরোনাম বিশেষ্য, লেবেল
এক-দুই শব্দ, নিচে এক লাইনের একটি নোট-পটি।  কারণ ও ব্যাখ্যা বইয়ের লেখায়।

**টাকার অঙ্ক ছবিতে ল্যাটিন সংখ্যায়** — কালপুরুষে বাংলা `৪` দেখতে
ল্যাটিন `8`-এর মতো, আর এখানে প্রায় প্রতিটি সংখ্যাই টাকার অঙ্ক।  বইয়ের
লেখায় বাংলা সংখ্যা থাকবে (বইয়ের নিয়ম), ছবিতে ল্যাটিন — অধ্যায় ১৬-এর
`230 V` / `1.732`-এর মতোই।  রেঞ্জে en-dash নয়, সাধারণ হাইফেন — `–`
কালপুরুষে আছে কি না যাচাই করা হয়নি।

d04-এর অঙ্কগুলো বইয়ের উদাহরণ ১৭.২-এর সঙ্গে হুবহু মেলানো।  একটি বদলালে
অন্যটিও বদলাতে হবে।
"""
import os

from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch17")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
LH = 1.42

BOXG = "#E7ECF1"
SCREEN = "#12222E"
LIFE = "#1B6E47"          # লাইফলাইনের ধাপ আলাদা রঙে


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


# ── d01 — মিটারের পাঠ ───────────────────────────────────────────────────
def d01_meter():
    s = SVG(1240, 640)
    s.title("মিটারের পাঠ থেকে ব্যবহৃত ইউনিট", T_TITLE)

    py, ph = 96, 434
    panel(s, 46, py, 560, ph, "এনার্জি মিটার", STEEL)
    panel(s, 634, py, 560, ph, "পাঠের হিসাব", GREEN)

    # ── বাঁ প্যানেল: মিটারের গা ──
    s.rect(156, 172, 340, 258, BOXG, GREY, 2.2, 14)
    s.rect(196, 214, 260, 84, SCREEN, NAVY, 2, 9)
    s.text(326, 274, "04628.5", 42, "#E8F3FF", 700, "middle")
    s.text(326, 340, "kWh", T_NODE, NAVY, 700, "middle")

    # টার্মিনাল ঢাকনা — মিটারের নিচের অংশ, লেখা নেই বলে সংঘর্ষের ভয়ও নেই
    s.rect(196, 368, 260, 44, "#FFFFFF", GREY, 2, 7)
    for k in range(4):
        s.rect(216 + k * 62, 380, 26, 20, BOXG, GREY, 1.6, 4)

    s.text(326, 466, "মিটার যা দেখাচ্ছে, সেটিই মোট পাঠ", T_SMALL, GREY,
           400, "middle")

    # ── ডান প্যানেল: বিয়োগ ──
    lx, rx = 682, 1150
    s.text(lx, 226, "এ মাসের পাঠ", T_NAME, INK, 400)
    s.text(rx, 226, "04628", T_NODE, NAVY, 700, "end")

    s.text(lx, 300, "গত মাসের পাঠ", T_NAME, INK, 400)
    s.text(1042, 300, "-", T_NODE, GREY, 700, "end")
    s.text(rx, 300, "04380", T_NODE, NAVY, 700, "end")

    s.line(lx, 332, rx, 332, STEEL, 2.6)

    s.rect(666, 356, 502, 76, GREENBG, GREEN, 2.4, 11)
    s.text(lx + 16, 406, "ব্যবহৃত ইউনিট", T_NAME, GREEN, 700)
    s.text(rx - 16, 406, "248", T_NODE, GREEN, 700, "end")

    s.text(917, 470, "মিটার ইউনিট গোনে, টাকা নয়", T_SMALL, GREY,
           400, "middle")

    y = note_strip(s, py + ph + 24,
                   "দুই মাসের পাঠের বিয়োগফলই ওই মাসের ব্যবহৃত ইউনিট")
    s.fit(y, 22)
    return s.save(f"{OUT}/d01_meter.svg")


# ── d02 — বিল তৈরির ধাপ ─────────────────────────────────────────────────
def d02_steps():
    s = SVG(1240, 480)
    s.title("বিল তৈরির ধাপ", T_TITLE)

    steps = [("১", "মিটারের পাঠ"), ("২", "ব্যবহৃত ইউনিট"),
             ("৩", "স্ল্যাব অনুযায়ী এনার্জি চার্জ"),
             ("৪", "ডিমান্ড চার্জ ও মিটার ভাড়া"),
             ("৫", "ভ্যাট যোগ করে মোট বিল")]
    CW, CH, GAP = 210, 206, 18
    ar = s.arrow_defs(STEEL, "ar", 14)

    for i, (num, name) in enumerate(steps):
        x = 46 + i * (CW + GAP)
        y = 112
        s.rect(x, y, CW, CH, "#FCFDFE", LINE, 1.8, 13)
        s.badge(x + CW / 2, y + 54, num, 27, NAVY, "#FFFFFF", T_NODE)
        for j, ln in enumerate(wrap(name, CW - 40, T_NAME, 700)):
            s.text(x + CW / 2, y + 118 + j * T_NAME * LH, ln, T_NAME, NAVY,
                   700, "middle")
        if i < len(steps) - 1:
            s.line(x + CW + 3, y + CH / 2, x + CW + GAP - 3, y + CH / 2,
                   STEEL, 2.4, marker=ar)

    y = note_strip(s, 112 + CH + 30,
                   "এনার্জি চার্জই বিলের সবচেয়ে বড় অংশ")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_steps.svg")


# ── d03 — আবাসিক ট্যারিফের ধাপ ──────────────────────────────────────────
def d03_slab():
    s = SVG(1240, 700)
    s.title("আবাসিক ট্যারিফের ধাপ", T_TITLE)

    # (রেঞ্জ, হার, রঙ)।  হারগুলো বিইআরসির জুন ২০২৬ আদেশ থেকে; বইয়ের
    # সারণি ১৭.১-এর সঙ্গে হুবহু মেলে।
    bars = [("0-50", 4.63, LIFE), ("0-75", 5.26, STEEL),
            ("76-200", 8.50, STEEL), ("201-300", 9.10, STEEL),
            ("301-400", 9.62, STEEL), ("401-600", 15.01, AMBER),
            ("600+", 17.35, RED)]

    # দণ্ডের উচ্চতা ইচ্ছে করেই কম রাখা — ছবিটা লম্বা হলে ১৫.৪ সেমিতে
    # সাড়ে ন'সেন্টিমিটার হয়ে যায় আর পাতার নিচে ফাঁক খুলে দেয়।  লেখার
    # আকার অপরিবর্তিত, তাই পাঠযোগ্যতায় কিছু যায় আসে না।
    x0, base, top = 92, 400, 170
    span = 1240 - 2 * x0
    n = len(bars)
    gap = 22
    bw = (span - (n - 1) * gap) / n
    scale = (base - top) / max(r for _, r, _ in bars)

    s.line(x0 - 16, base, x0 + span + 16, base, GREY, 2.4)
    s.text(x0 - 16, 122, "টাকা / ইউনিট", T_SMALL, GREY, 400)

    for i, (rng, rate, col) in enumerate(bars):
        bx = x0 + i * (bw + gap)
        bh = rate * scale
        s.rect(bx, base - bh, bw, bh, col, col, 1.5, 6)
        # হারের লেখা দণ্ডের ঠিক উপরে — ভেতরে নয়, নইলে qc সংঘর্ষ ধরবে
        s.text(bx + bw / 2, base - bh - 16, f"{rate:.2f}", T_NAME, NAVY,
               700, "middle")
        s.text(bx + bw / 2, base + 36, rng, T_BODY, INK, 600, "middle")

    s.text(x0 + span / 2, base + 76, "মাসিক ব্যবহার (ইউনিট)", T_SMALL,
           GREY, 400, "middle")

    y = note_strip(s, base + 106,
                   "ব্যবহার যত উপরের ধাপে ওঠে, ওই অংশের হার তত বেশি")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_slab.svg")


# ── d04 — বিলের নমুনা কাগজ ──────────────────────────────────────────────
def d04_bill():
    s = SVG(1240, 800)
    s.title("বিদ্যুৎ বিলের নমুনা", T_TITLE)

    BX, BY, BW = 150, 96, 940
    HDR = 58
    ROW = 46
    rows = [
        ("পূর্বের পাঠ", "04380", False),
        ("বর্তমান পাঠ", "04628", False),
        ("ব্যবহৃত ইউনিট", "248", False),
        ("এনার্জি চার্জ", "1893.80", False),
        ("ডিমান্ড চার্জ: 2 kW", "84.00", False),
        ("মিটার ভাড়া", "40.00", False),
        ("ভ্যাট 5%", "100.89", False),
        ("সময়মতো পরিশোধে মোট", "2118.69", True),
        ("বিলম্ব মাশুল 5%", "105.93", False),
        ("বিলম্বে পরিশোধে মোট", "2224.62", True),
    ]
    BH = HDR + 34 + len(rows) * ROW + 22

    s.rect(BX, BY, BW, BH, "#FFFFFF", GREY, 2.2, 13)
    s.rect(BX, BY, BW, HDR, NAVY, NAVY, 2, 13)
    s.text(BX + BW / 2, BY + 38, "মাসিক বিদ্যুৎ বিল", T_NODE, "#FFFFFF",
           700, "middle")

    lx, rx = BX + 34, BX + BW - 34
    hy = BY + HDR + 24
    s.text(lx, hy, "বিবরণ", T_SMALL, GREY, 700)
    s.text(rx, hy, "টাকা", T_SMALL, GREY, 700, "end")
    s.line(BX + 22, hy + 14, BX + BW - 22, hy + 14, LINE, 1.8)

    y = BY + HDR + 34
    for label, amount, strong in rows:
        if strong:
            s.rect(BX + 22, y + 4, BW - 44, ROW - 8, LIGHT, STEEL, 1.8, 8)
        col = NAVY if strong else INK
        s.text(lx, y + 32, label, T_BODY, col, 700 if strong else 400)
        s.text(rx, y + 32, amount, T_BODY, col, 700, "end")
        y += ROW

    # ইউনিটের ঘর আর টাকার ঘর আলাদা — মাঝে একটা রেখা, লেখার ফাঁকে
    s.line(BX + 22, BY + HDR + 34 + 3 * ROW - 4, BX + BW - 22,
           BY + HDR + 34 + 3 * ROW - 4, LINE, 1.8)

    y = note_strip(s, BY + BH + 26,
                   "এনার্জি চার্জ, ডিমান্ড চার্জ ও মিটার ভাড়ার যোগফলে ভ্যাট বসে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_bill.svg")


# ── d05 — পোস্টপেইড ও প্রিপেইড ──────────────────────────────────────────
def d05_prepaid():
    s = SVG(1240, 700)
    s.title("পোস্টপেইড ও প্রিপেইড মিটার", T_TITLE)

    py, ph = 96, 494
    panel(s, 46, py, 560, ph, "পোস্টপেইড", STEEL)
    panel(s, 634, py, 560, ph, "প্রিপেইড", GREEN)

    left = ["মিটার চলে", "মাস শেষে পাঠ", "বিলের কাগজ", "বিল পরিশোধ"]
    right = ["রিচার্জ", "টোকেন নম্বর", "মিটারে বসানো", "ব্যালান্স কমে"]

    ar_l = s.arrow_defs(STEEL, "arl", 14)
    ar_r = s.arrow_defs(GREEN, "arr", 14)

    for items, px, col, ar in ((left, 46, STEEL, ar_l),
                               (right, 634, GREEN, ar_r)):
        bx, bw = px + 60, 440
        for i, name in enumerate(items):
            by = 176 + i * 100
            s.rect(bx, by, bw, 68, "#FCFDFE", col, 2.2, 10)
            s.text(bx + bw / 2, by + 44, name, T_NAME, NAVY, 700, "middle")
            if i < len(items) - 1:
                s.line(bx + bw / 2, by + 72, bx + bw / 2, by + 96, col, 2.6,
                       marker=ar)

    y = note_strip(s, py + ph + 24,
                   "প্রিপেইডে টাকা আগে, বিদ্যুৎ পরে; বিলম্ব মাশুল নেই")
    s.fit(y, 22)
    return s.save(f"{OUT}/d05_prepaid.svg")


ALL = [d01_meter, d02_steps, d03_slab, d04_bill, d05_prepaid]

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
