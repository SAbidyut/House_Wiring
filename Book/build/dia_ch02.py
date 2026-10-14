# -*- coding: utf-8 -*-
"""অধ্যায় ২ — ইলেকট্রিক্যাল টুলস : টেকনিক্যাল ডায়াগ্রাম।

Only genuinely *illustrative* content is drawn here. Anything that is just
boxes of text (classification, comparisons, step lists) is built as a native
Word table in ch02.py so it stays editable.
"""
import os, math
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams", "ch02")

T_TITLE = 34
T_NODE = 28
T_NAME = 25.5
T_BODY = 23
T_SMALL = 22.5
LH = 1.42


def callout(s, x1, y1, x2, y2, text, anchor="start", size=T_SMALL,
            color="#8A97A6", tcolor=NAVY, sub=None, max_w=300):
    s.path(f"M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}", color, 1.8)
    s.circle(x1, y1, 4.4, color)
    lines = wrap(text, max_w, size, 700)
    for i, ln in enumerate(lines):
        s.text(x2 + (10 if anchor == "start" else -10), y2 + 6 + i * size * 1.3,
               ln, size, tcolor, 700, anchor)
    if sub:
        for j, ln in enumerate(wrap(sub, max_w, size - 2, 400)):
            s.text(x2 + (10 if anchor == "start" else -10),
                   y2 + 6 + len(lines) * size * 1.3 + j * (size - 2) * 1.3,
                   ln, size - 2, "#4A5561", 400, anchor)


# ═══════════════════════════════════════════════════════════════════════
def part_label(s, tx, ty, cx, top, name, sub, max_w=280, size=T_SMALL,
               above=True, color="#8A97A6"):
    """A part label whose leader stops at the edge of the text block.

    The old version aimed the leader at the block's *anchor point*, so the
    line ran straight through the lettering it was pointing at.  Here the
    block is measured first and the leader ends 9 px clear of it.
    """
    subs = wrap(sub, max_w, size - 2, 400) if sub else []
    w = max([tw(name, size, 700)] + [tw(l, size - 2, 400) for l in subs])
    lh1, lh2 = size * 1.32, (size - 2) * 1.32
    h = lh1 + len(subs) * lh2
    x0, x1, y1 = cx - w / 2, cx + w / 2, top + h
    ex = min(max(tx, x0 + 22), x1 - 22)
    ey = y1 + 9 if above else top - 13
    s.path(f"M {tx:.1f} {ty:.1f} L {ex:.1f} {ey:.1f}", color, 1.8)
    s.circle(tx, ty, 4.4, color)
    s.text(cx, top + size * 0.82, name, size, NAVY, 700, "middle")
    for i, ln in enumerate(subs):
        s.text(cx, top + lh1 + (size - 2) * 0.82 + i * lh2, ln,
               size - 2, "#4A5561", 400, "middle")
    return x0, top - size * 0.8, x1, y1


# ═══════════════════════════════════════════════════════════════════════
def d01_screwdriver():
    """Anatomy of a screwdriver — the parts a trainee must be able to name."""
    s = SVG(1200, 620)
    s.title("স্ক্রু ড্রাইভারের বিভিন্ন অংশ", T_TITLE)

    cy = 330
    # handle
    s.path(f"M 250 {cy-58:.1f} Q 168 {cy-58:.1f} 168 {cy:.1f} "
           f"Q 168 {cy+58:.1f} 250 {cy+58:.1f} Z", "#B8500C", 2, "#F07818")
    for i in range(5):
        s.path(f"M {196+i*13} {cy-52:.1f} L {196+i*13} {cy+52:.1f}",
               "#C25A10", 4.5)
    s.rect(248, cy - 30, 46, 60, "#3A4750", "#222C33", 2, 8)      # ferrule
    # shaft
    s.rect(292, cy - 13, 470, 26, "#C6CDD4", "#8B949C", 2, 4)
    s.rect(292, cy - 13, 470, 9, "#E4E9ED", "none", 0, 2)
    # insulated sleeve on the shaft
    s.rect(292, cy - 17, 300, 34, "#E8352A", "#A8231A", 2, 7)
    s.rect(292, cy - 17, 300, 11, "#F26A60", "none", 0, 3)
    # tip
    s.poly([(762, cy - 13), (826, cy - 7), (826, cy + 7), (762, cy + 13)],
           "#9AA3AB", "#6E767D", 2)
    s.poly([(826, cy - 7), (858, cy - 3), (858, cy + 3), (826, cy + 7)],
           "#7C858D", "#5A6167", 2)

    # ── উপরে তিনটি, নিচে তিনটি — লিডার লেখার গা ঘেঁষে থামে, ভেতর দিয়ে যায় না
    LS = 25                          # part names; sub-lines print at LS − 2
    part_label(s, 200, cy - 58, 176, 132, "হ্যান্ডেল",
               "ইনসুলেটেড প্লাস্টিক বা রাবার, হাত নিরাপদ রাখে", 270, LS)
    part_label(s, 440, cy - 17, 566, 132, "ইনসুলেটেড স্লিভ",
               "১০০০ V পর্যন্ত ইনসুলেশন (IEC 60900)", 380, LS)
    part_label(s, 690, cy - 13, 952, 132, "শ্যাফট বা ব্লেড",
               "শক্ত ইস্পাতের দণ্ড", 270, LS)

    part_label(s, 200, cy + 58, 176, 446, "গ্রিপ খাঁজ",
               "হাত পিছলে যেতে দেয় না", 270, LS, above=False)
    part_label(s, 271, cy + 30, 524, 446, "ফেরুল",
               "হ্যান্ডেল ও শ্যাফট আটকে রাখে", 270, LS, above=False)
    part_label(s, 845, cy + 3, 946, 446, "টিপ",
               "স্ক্রুর খাঁজে বসে; ফ্ল্যাট বা স্টার", 270, LS, above=False)

    s.rect(40, 548, 1120, 72, "#EAF2FA", STEEL, 2, 11)
    s.text(600, 578, "স্ক্রু ড্রাইভারের মাপ = ব্লেডের দৈর্ঘ্য × টিপের প্রস্থ",
           T_NAME, NAVY, 700, "middle")
    s.text(600, 608, "যেমন ১৫০ মিমি × ৬ মিমি; টিপ হবে স্ক্রুর খাঁজের সমান",
           T_SMALL, GREY, 400, "middle")
    s.fit(620, 22)
    return s.save(f"{OUT}/d01_screwdriver.svg")


def d02_iec60900_marking():
    """How to read the markings on an insulated (live-working) hand tool.

    আগের সংস্করণে হাতলটা ছিল একটা কমলা তাল আর মার্কিংগুলো তার নিচে
    ফাঁকা জায়গায় ভাসত — দেখে টুল মনে হতো না।  এখানে হাতলটা পুরো
    স্ক্রু ড্রাইভারের মাপে আঁকা, আর মার্কিং তিনটে হাতলের গায়েই ছাপা —
    ছবির কাজ দেখানো, অর্থ বোঝানোর কাজ ডান পাশের সারণির।
    """
    s = SVG(1200, 700)
    s.title("ইনসুলেটেড টুলের গায়ের মার্কিং পাঠ (IEC 60900)", T_TITLE)

    # ── বাঁ দিকের ঘর : টুলটা নিজে, গায়ের ছাপা লেখাসহ ────────────────
    s.rect(60, 118, 580, 292, "#FCFDFE", LINE, 2, 16)
    cy = 244
    # হাতল — গোড়ায় গোল, সামনে চ্যাপ্টা; ওই চ্যাপ্টা জায়গাতেই মার্কিং ছাপা হয়
    s.path(f"M 302 {cy-28:.1f} Q 282 {cy-45:.1f} 200 {cy-47:.1f} "
           f"Q 108 {cy-48:.1f} 100 {cy-24:.1f} Q 94 {cy:.1f} 100 {cy+24:.1f} "
           f"Q 108 {cy+48:.1f} 200 {cy+47:.1f} "
           f"Q 282 {cy+45:.1f} 302 {cy+28:.1f} Z",
           "#B8500C", 2.4, "#F07818")
    s.path(f"M 126 {cy-33:.1f} Q 210 {cy-39:.1f} 284 {cy-27:.1f}",
           "#FBA65C", 9)
    for i in range(3):
        s.path(f"M {112+i*13} {cy-38:.1f} Q {107+i*13} {cy:.1f} "
               f"{112+i*13} {cy+38:.1f}", "#C25A10", 4.5)
    s.rect(298, cy - 22, 42, 44, "#3A4750", "#222C33", 2, 7)      # ফেরুল
    s.rect(338, cy - 11, 202, 22, "#C6CDD4", "#8B949C", 2, 4)     # শ্যাফট
    s.rect(338, cy - 11, 202, 8, "#E4E9ED", "none", 0, 2)
    s.rect(338, cy - 15, 118, 30, "#E8352A", "#A8231A", 2, 6)     # অন্তরক স্লিভ
    s.rect(338, cy - 15, 118, 10, "#F26A60", "none", 0, 3)
    s.poly([(540, cy - 11), (578, cy - 6), (578, cy + 6), (540, cy + 11)],
           "#9AA3AB", "#6E767D", 2)
    s.poly([(578, cy - 6), (600, cy - 3), (600, cy + 3), (578, cy + 6)],
           "#7C858D", "#5A6167", 2)

    # হাতলের গায়ে ছাপা তিনটে মার্কিং — কাজের আগে এটুকুই খুঁজে দেখতে হয়
    MK = "#2A1405"

    def dbl_triangle(cx, cy_, k=1.0):
        for dx in (-16 * k, 16 * k):
            s.poly([(cx + dx, cy_ - 15 * k), (cx + dx + 13.5 * k, cy_ + 11 * k),
                    (cx + dx - 13.5 * k, cy_ + 11 * k)], "none", MK, 3.2 * k)
    dbl_triangle(176, cy - 14, 0.95)
    s.text(210, cy - 5, "1000 V", 24, MK, 700)
    s.text(152, cy + 32, "IEC 60900", 23, MK, 700)

    s.rect(84, 336, 532, 54, "#FFF6E5", AMBER, 2, 11)
    s.text(350, 369, "মার্কিং মুছে গেলে টুলটি আর ব্যবহার করা যাবে না",
           T_SMALL, "#7A5200", 700, "middle")

    # ── ডান দিকের ঘর : কোন লেখাটার মানে কী ─────────────────────────
    rows = [("দুই ত্রিভুজ", "লাইভ লাইনে ব্যবহারের উপযোগী", GREEN),
            ("1000 V", "১০০০ V AC / ১৫০০ V DC পর্যন্ত অনুমোদিত", STEEL),
            ("IEC 60900", "যে মান অনুসারে পরীক্ষা করা হয়েছে", STEEL),
            ("প্রস্তুতকারকের নাম", "উৎস শনাক্তকরণ", GREY),
            ("তৈরির সন", "মেয়াদ ও ট্রেসেবিলিটি", GREY)]
    x0, y0, w = 664, 118, 496
    s.rect(x0, y0, w, 46, NAVY, NAVY, 2, 10)
    s.text(x0 + w / 2, y0 + 31, "গায়ে যা যা লেখা থাকবে", T_NAME, "#FFFFFF", 700, "middle")
    yy = y0 + 54
    for name, meaning, col in rows:
        h = 26 + len(wrap(meaning, w - 210, T_SMALL, 400)) * T_SMALL * 1.32
        s.rect(x0, yy, w, h, "#F7FAFC", LINE, 1.6, 8)
        s.rect(x0, yy, 6, h, col, "none", 0, 3)
        s.text(x0 + 20, yy + 30, name, T_SMALL, NAVY, 700)
        for j, ln in enumerate(wrap(meaning, w - 210, T_SMALL, 400)):
            s.text(x0 + 200, yy + 30 + j * T_SMALL * 1.32, ln, T_SMALL, "#39434D", 400)
        yy += h + 8

    bot = max(yy, 410) + 26
    s.rect(70, bot, 1090, 62, REDBG, RED, 2, 11)
    s.text(615, bot + 28, "যে টুলে এই চিহ্ন নেই, তা দিয়ে লাইভ লাইনে কাজ করা যাবে না",
           T_NAME, "#7A1810", 700, "middle")
    s.text(615, bot + 54,
           "শুধু প্লাস্টিকের হাতল থাকলেই ইনসুলেটেড টুল হয় না; মার্কিং দেখে নিশ্চিত হতে হবে",
           T_SMALL, "#7A1810", 400, "middle")
    s.fit(bot + 62, 22)
    return s.save(f"{OUT}/d02_iec60900_marking.svg")


def d03_stripping():
    """ইনসুলেশন ছাড়ানোর সঠিক ও ভুল পদ্ধতি।

    উপরের ঘরে হাতিয়ারটা নিজে — যেন দেখেই চেনা যায়।  নিচের ঘরে সেই
    হাতিয়ারের ধার তারের গায়ে কতদূর নামে, বিবর্ধিত করে — আসল পার্থক্যটা
    ওখানেই, খালি চোখে যা ধরা পড়ে না।
    """
    s = SVG(1240, 980)
    s.title("তারের ইনসুলেশন ছাড়ানো: সঠিক ও ভুল পদ্ধতি", 38)

    TS, TB = 23, 25                 # এই ছবির লেখা একটু বড়, নইলে ছাপায় পড়া যায় না
    INS, INS_E = "#2E6F9E", "#1D4E70"
    CU, CU_E = "#C98B3F", "#8A5A18"
    ST_L, ST_M, ST_D = "#D6DDE4", "#AEB8C2", "#7C8794"
    GRIP, GRIP_D = "#3A4750", "#222C33"
    PANEL, WELL = "#FCFDFE", "#F2F6FA"

    # ── হাতিয়ার ১ : ওয়্যার স্ট্রিপার, মুখের দিক থেকে ─────────────────
    def tool_stripper(cx, cy):
        """প্লায়ার-ধাঁচের স্ট্রিপার — হাতল, পিভট, আর মাপ-ভাগ করা খাঁজের সারি।

        খাঁজ পিভটের দিকে বড়, মুখের দিকে ছোট — আসল টুলে যেভাবে সাজানো
        থাকে (মোটা তারে বেশি চাপ লাগে, তাই সেটা পিভটের কাছে)।
        """
        cx += 49                       # আঁকা অংশটা ঘরের ঠিক মাঝে বসাতে
        hx = cx - 244                                   # হাতলের গোড়া
        pv = cx - 46                                    # পিভটের কেন্দ্র
        for sg in (-1, 1):
            # হাতল — পিভটের কাছে মোটা, প্রান্তে সরু, বাইরে ছড়ানো
            s.path(f"M {pv-10} {cy+sg*6:.1f} L {pv-16} {cy+sg*34:.1f} "
                   f"Q {hx+104} {cy+sg*74:.1f} {hx} {cy+sg*80:.1f} "
                   f"L {hx} {cy+sg*54:.1f} "
                   f"Q {hx+112} {cy+sg*48:.1f} {pv-14} {cy+sg*4:.1f} Z",
                   ST_D, 2.2, ST_L)
            # রাবার গ্রিপ
            s.path(f"M {hx+4} {cy+sg*78:.1f} Q {hx+94} {cy+sg*72:.1f} "
                   f"{hx+150} {cy+sg*50:.1f} L {hx+142} {cy+sg*30:.1f} "
                   f"Q {hx+92} {cy+sg*52:.1f} {hx+4} {cy+sg*56:.1f} Z",
                   GRIP_D, 2, GRIP)
        s.circle(pv, cy, 18, ST_M, ST_D, 2.2)           # পিভটের রিভেট
        s.circle(pv, cy, 6.5, ST_D)
        for sg in (-1, 1):
            # চোয়াল — গোড়ায় চওড়া, মুখে সরু ঠোঁট
            s.path(f"M {pv+2} {cy+sg*2:.1f} L {pv+2} {cy+sg*38:.1f} "
                   f"L {pv+104} {cy+sg*32:.1f} L {pv+158} {cy+sg*22:.1f} "
                   f"L {pv+192} {cy+sg*13:.1f} L {pv+192} {cy+sg*2:.1f} Z",
                   ST_D, 2.2, ST_L)
        s.line(pv + 8, cy, pv + 190, cy, ST_D, 2)       # দুই চোয়ালের ফাঁক
        for dx, r in ((32, 14), (70, 11.5), (103, 9.5), (132, 7.5),
                      (157, 5.5)):
            s.circle(pv + dx, cy, r, WELL, ST_D, 2.2)   # মাপ-ভাগ করা খাঁজ
        return pv + 192

    # ── হাতিয়ার ২ : ইলেকট্রিশিয়ান নাইফ ───────────────────────────────
    def tool_knife(cx, cy):
        cx += 9                        # আঁকা অংশটা ঘরের ঠিক মাঝে বসাতে
        hx = cx - 236
        s.path(f"M {hx} {cy-34:.1f} Q {hx-34} {cy:.1f} {hx} {cy+34:.1f} "
               f"L {hx+262} {cy+29:.1f} L {hx+262} {cy-29:.1f} Z",
               "#2E2013", 2.2, "#5C4327")
        s.path(f"M {hx+12} {cy-24:.1f} L {hx+252} {cy-21:.1f}", "#7A5C36", 6)
        for rx in (hx + 60, hx + 190):
            s.circle(rx, cy, 7.5, "#C9A227", "#8A6E14", 1.6)
        # ব্লেড — সোজা পিঠ, বাঁকানো ধার, সামনে ছুঁচালো মুখ
        s.path(f"M {hx+262} {cy-29:.1f} L {hx+368} {cy-31:.1f} "
               f"L {hx+454} {cy+3:.1f} Q {hx+382} {cy+31:.1f} "
               f"{hx+288} {cy+29:.1f} L {hx+262} {cy+29:.1f} Z",
               ST_D, 2.2, ST_L)
        s.path(f"M {hx+290} {cy+17:.1f} Q {hx+372} {cy+17:.1f} "
               f"{hx+440} {cy-1:.1f}", ST_M, 4.5)
        return hx + 454

    # ── নিচের ঘর : কাটার মুহূর্ত, বিবর্ধিত ────────────────────────────
    def section(x0, x1, xc, cy, bad):
        """তার পাশ থেকে — ইনসুলেশন OD ৫৮, তামা ৩৪ (দুই পাশে ১২ দেয়াল)।"""
        s.rect(xc, cy - 17, x1 - xc, 34, CU, CU_E, 2.4, 7)
        s.line(xc + 14, cy - 8, x1 - 12, cy - 8, "#E4B274", 3)
        s.rect(x0, cy - 29, xc - x0, 58, INS, INS_E, 2.4, 11)
        if bad:                       # ছুরির ধার তামার ভেতরে ঢুকেছে
            nx = xc + 40
            s.poly([(nx - 13, cy - 17), (nx + 13, cy - 17), (nx, cy + 7)],
                   "#FBE3E0", RED, 2.6)                  # তামায় কাটা খাঁজ
            s.poly([(nx - 20, cy - 74), (nx + 20, cy - 74), (nx + 20, cy - 40),
                    (nx + 7, cy - 8), (nx, cy + 6), (nx - 7, cy - 8),
                    (nx - 20, cy - 40)], ST_L, ST_D, 2.4)
            s.path(f"M {nx-9} {cy-66:.1f} L {nx-3} {cy-14:.1f}", ST_M, 3)
            ar = s.arrow_defs(RED, "kdn", 13)
            s.path(f"M {nx+40} {cy-80:.1f} L {nx+40} {cy-38:.1f}", RED, 3,
                   marker=ar)                    # the push, beside the blade
        else:                         # চোয়ালের ধার তামার গা ছুঁয়েই থেমেছে
            nx = xc + 6
            for sg in (-1, 1):
                s.poly([(nx - 22, cy + sg * 78), (nx + 22, cy + sg * 78),
                        (nx + 22, cy + sg * 40), (nx + 8, cy + sg * 21),
                        (nx, cy + sg * 17), (nx - 8, cy + sg * 21),
                        (nx - 22, cy + sg * 40)], ST_L, ST_D, 2.4)
                s.path(f"M {nx+13} {cy+sg*70:.1f} L {nx+5} {cy+sg*26:.1f}",
                       ST_M, 3)
            ar = s.arrow_defs(GREEN, "jsq", 13)
            # the squeeze, right beside the two jaws it describes
            s.path(f"M {nx+40} {cy-82:.1f} L {nx+40} {cy-42:.1f}", GREEN, 3,
                   marker=ar)
            s.path(f"M {nx+40} {cy+82:.1f} L {nx+40} {cy+42:.1f}", GREEN, 3,
                   marker=ar)
            s.path(f"M {nx+26} {cy-17:.1f} L {x1-10} {cy-17:.1f}", GREEN, 2.4,
                   dash="7 5")

    cases = [
        (46, "সঠিক: ওয়্যার স্ট্রিপার", GREEN, GREENBG, tool_stripper,
         "তারের মাপ অনুযায়ী খাঁজ বেছে নিলে চোয়ালের ধার ইনসুলেশন কেটে "
         "তামার গায়ে এসে থেমে যায়।",
         "তামার পৃষ্ঠ মসৃণ ও অক্ষত", False),
        (634, "ভুল: ছুরি সমকোণে", RED, REDBG, tool_knife,
         "ছুরি তারের সঙ্গে সমকোণে চেপে ধরলে ধার ইনসুলেশন পেরিয়ে তামার "
         "গায়ে বসে যায়।",
         "তামায় খাঁজ, টান পড়লে এখানেই ভাঙবে", True),
    ]

    PW, PH = 560, 700
    for px, head, col, bg, draw_tool, method, verdict, bad in cases:
        s.rect(px, 96, PW, PH, PANEL, LINE, 1.8, 14)
        s.box_auto(px + PW / 2, 110, head, TB, fill=col, stroke=col,
                   tcolor="#FFFFFF", pad_x=26, pad_y=10)

        # ── উপরের ঘর : হাতিয়ারটা নিজে
        s.rect(px + 26, 178, PW - 52, 190, WELL, LINE, 1.6, 12)
        draw_tool(px + PW / 2, 273)

        # ── নিচের ঘর : ধার কতদূর নামে, ×৪ বিবর্ধিত
        zy = 508
        s.rect(px + 26, 392, PW - 52, 214, "#FBFDFE", ST_D, 2, 12, dash="8 6")
        s.text(px + 46, 424, "বড় করে দেখানো", TS, GREY, 700)
        section(px + 54, px + 506, px + 236, zy, bad)
        s.text(px + 54, 584, "ইনসুলেশন", TS, "#1D4E70", 700)
        s.text(px + 506, 584, "তামা", TS, "#8A5A18", 700, "end")

        for j, ln in enumerate(wrap(method, PW - 76, TS, 400)):
            s.text(px + PW / 2, 646 + j * TS * 1.32, ln, TS,
                   "#39434D", 400, "middle")

        s.rect(px + 26, 714, PW - 52, 58, bg, col, 2, 10)
        s.text(px + PW / 2, 746, verdict, TB, col, 700, "middle")

    s.rect(60, 826, 1120, 86, "#FFF6E5", AMBER, 2, 11)
    s.text(620, 862, "তামায় সামান্য খাঁজ পড়লেই সেখানে তারের প্রস্থচ্ছেদ কমে "
           "যায়, রোধ বাড়ে ও তাপ জমে", TS, "#7A5200", 700, "middle")
    s.text(620, 894, "কাজের দিন কিছু বোঝা যায় না; কয়েক মাস পরে ঠিক ওই "
           "বিন্দুতেই তার গরম হয়ে ভেঙে যায়", TS, "#7A5200", 400,
           "middle")
    s.fit(912, 22)
    return s.save(f"{OUT}/d03_stripping.svg")


def d04_protection_class():
    """Class I / II / III appliance protection classes (IEC 61140)."""
    s = SVG(1200, 560)
    s.title("বৈদ্যুতিক সরঞ্জামের সুরক্ষা শ্রেণি (IEC 61140)", T_TITLE)
    cards = [
        ("ক্লাস I", "আর্থিং নির্ভর",
         "ধাতব বডি আর্থ তারে যুক্ত থাকে। থ্রি-পিন প্লাগ লাগে।", STEEL, "#EAF2FA"),
        ("ক্লাস II", "ডাবল ইনসুলেশন",
         "দুই স্তরের ইনসুলেশন থাকে, আর্থিং লাগে না। বেশির ভাগ পাওয়ার টুল এই শ্রেণির।",
         GREEN, GREENBG),
        ("ক্লাস III", "অতি নিম্ন ভোল্টেজ",
         "SELV উৎসে চলে (৫০ V AC-এর নিচে)। শকের ঝুঁকি নেই বললেই চলে।",
         AMBER, AMBERBG),
    ]
    cw, gapx = 356, 26
    x0 = (1200 - (3 * cw + 2 * gapx)) / 2
    for i, (name, sub, desc, col, bg) in enumerate(cards):
        x = x0 + i * (cw + gapx)
        s.rect(x, 96, cw, 330, bg, col, 2, 13)
        s.rect(x, 96, cw, 60, col, col, 2, 13)
        s.rect(x + 1, 146, cw - 2, 10, col, "none", 0, 0)
        s.text(x + cw / 2, 138, name, T_NAME, "#FFFFFF", 700, "middle")
        cx, cy = x + cw / 2, 232
        if i == 0:   # earth symbol
            s.line(cx, cy - 34, cx, cy - 4, col, 4)
            for k, ww in enumerate((52, 34, 18)):
                s.line(cx - ww / 2, cy - 2 + k * 11, cx + ww / 2, cy - 2 + k * 11, col, 4.4)
        elif i == 1:  # square-in-square
            s.rect(cx - 34, cy - 26, 68, 54, "none", col, 4, 3)
            s.rect(cx - 22, cy - 17, 44, 36, "none", col, 4, 2)
        else:        # III in a diamond
            s.poly([(cx, cy - 34), (cx + 34, cy), (cx, cy + 34), (cx - 34, cy)],
                   "none", col, 4)
            s.text(cx, cy + 10, "III", 26, col, 700, "middle")
        s.text(x + cw / 2, 300, sub, T_BODY, col, 700, "middle")
        for j, ln in enumerate(wrap(desc, cw - 52, T_SMALL, 400)):
            s.text(x + cw / 2, 336 + j * T_SMALL * 1.34, ln, T_SMALL,
                   "#2E3842", 400, "middle")
    s.text(600, 470,
           "নেমপ্লেটে বর্গের ভেতর বর্গ থাকলে টুলটি ক্লাস II, তাই আলাদা আর্থিং লাগে না",
           T_SMALL, GREY, 400, "middle")
    s.fit(470, 24)
    return s.save(f"{OUT}/d04_protection_class.svg")


def d05_drill_zones():
    """দেয়ালের ভেতরে ক্যাবল কোন অঞ্চলে থাকতে পারে — অর্থাৎ কোথায় ড্রিল নয়।

    ১৫০ মিমি মাপ ও তিনটি অঞ্চলের সংজ্ঞা BS 7671-এর ৫২২.৬.২০২ ধারা থেকে;
    সবুজ অংশগুলো একরঙা ভরাট বলে ওভারল্যাপেও একটিই অবিচ্ছিন্ন করিডোর দেখায়।
    """
    s = SVG(1240, 1000)
    s.title("দেয়ালের ভেতরে ক্যাবল টানার অনুমোদিত অঞ্চল", T_TITLE)

    WX, WY, WW, WH = 150, 146, 580, 560
    BAND = 56                      # ১৫০ মিমি-এর প্রতীকী প্রস্থ
    SLAB = 34
    PLASTER, CONC, CONC_E = "#F7F3EB", "#D9DFE6", "#A9B4C0"
    ZONE, ZONE_E, CABLE = "#D3E9DC", "#1B6E47", "#28323C"

    # ── কাঠামো : ছাদ, মেঝে ও দুই পাশের দেয়াল ────────────────────────
    s.rect(WX - 46, WY - SLAB, WW + 92, SLAB, CONC, CONC_E, 2, 4)
    s.rect(WX - 46, WY + WH, WW + 92, SLAB, CONC, CONC_E, 2, 4)
    s.rect(WX - 46, WY, 46, WH, CONC, CONC_E, 2, 0)
    s.rect(WX + WW, WY, 46, WH, CONC, CONC_E, 2, 0)
    s.text(WX + WW / 2, WY - 10, "ছাদ", T_SMALL, "#54606C", 700, "middle")
    s.text(WX + WW / 2, WY + WH + 24, "মেঝে", T_SMALL, "#54606C", 700, "middle")
    s.rect(WX, WY, WW, WH, PLASTER, CONC_E, 2, 0)

    SW_X, SWY, SWW, SWH = WX + 250, WY + 210, 88, 108
    SO_X, SOY, SOW, SOH = WX + 396, WY + 400, 88, 72
    SO_CY = SOY + SOH / 2

    # ── অনুমোদিত অঞ্চল ───────────────────────────────────────────────
    def zone(x, y, w_, h_):
        s.rect(x, y, w_, h_, ZONE, "none", 0, 0)

    zone(WX, WY, WW, BAND)                          # ১ — ছাদ ঘেঁষে
    zone(WX, WY, BAND, WH)                          # ২ — বাঁ কোণা
    zone(WX + WW - BAND, WY, BAND, WH)              # ২ — ডান কোণা
    zone(SW_X - SWW / 2, WY, SWW, WH)               # ৩ — সুইচ বরাবর উল্লম্ব
    zone(WX, SO_CY - 44, WW, 88)                    # ৩ — সকেট বরাবর অনুভূমিক

    # ── অঞ্চলের ভেতর দিয়ে চলা প্রকৃত ক্যাবল ──────────────────────────
    s.path(f"M {WX+BAND/2} {WY+WH} L {WX+BAND/2} {WY+BAND/2} "
           f"L {SW_X-28} {WY+BAND/2} L {SW_X-28} {SWY}", CABLE, 4.6)
    s.path(f"M {WX+WW-BAND/2} {WY+BAND} L {WX+WW-BAND/2} {SO_CY} "
           f"L {SO_X+SOW/2} {SO_CY}", CABLE, 4.6)

    # ── সুইচ ও সকেট ─────────────────────────────────────────────────
    s.rect(SW_X - SWW / 2, SWY, SWW, SWH, "#FFFFFF", "#7C8794", 2.6, 7)
    s.rect(SW_X - 16, SWY + 26, 32, 56, "#EDF1F5", "#9AA6B2", 2, 4)
    s.rect(SW_X - 9, SWY + 33, 18, 22, RED, "#9C2B20", 1.4, 2)
    s.text(SW_X + SWW / 2 + 14, SWY + 36, "সুইচ", T_SMALL, "#37424E", 700)

    s.rect(SO_X - SOW / 2, SOY, SOW, SOH, "#FFFFFF", "#7C8794", 2.6, 7)
    for dx in (-17, 17):
        s.rect(SO_X + dx - 6, SOY + 28, 12, 20, "#3B4550", "#20272E", 1.4, 3)
    s.rect(SO_X - 6, SOY + 10, 12, 14, "#3B4550", "#20272E", 1.4, 3)
    s.text(SO_X + SOW / 2 + 14, SOY + 32, "সকেট", T_SMALL, "#37424E", 700)

    # ── ১৫০ মিমি মাপ ────────────────────────────────────────────────
    ar = s.arrow_defs(NAVY, "dim", 11)
    dx_ = WX + WW - BAND - 66
    s.path(f"M {dx_} {WY+5} L {dx_} {WY+BAND-5}", NAVY, 2, marker=ar)
    s.path(f"M {dx_} {WY+BAND-5} L {dx_} {WY+5}", NAVY, 2, marker=ar)
    s.text(dx_ - 14, WY + BAND / 2 + 7, "১৫০ মিমি", T_SMALL, NAVY, 700, "end")

    dy_ = WY + BAND + 46
    s.path(f"M {WX+5} {dy_} L {WX+BAND-5} {dy_}", NAVY, 2, marker=ar)
    s.path(f"M {WX+BAND-5} {dy_} L {WX+5} {dy_}", NAVY, 2, marker=ar)
    s.text(WX + BAND + 16, dy_ + 7, "১৫০ মিমি", T_SMALL, NAVY, 700)

    # ── নিষিদ্ধ কোনাকুনি রুট ────────────────────────────────────────
    ax, ay, bx, by = WX + 92, WY + 356, WX + 180, WY + 236
    s.path(f"M {ax} {ay} L {bx} {by}", RED, 4.4, dash="13 8")
    mx, my = (ax + bx) / 2, (ay + by) / 2
    s.circle(mx, my, 24, "#FFFFFF", RED, 4)
    s.line(mx - 15, my + 15, mx + 15, my - 15, RED, 4)
    s.text(WX + 140, WY + 214, "কোনাকুনি নয়", T_SMALL, RED, 700, "middle")

    s.text(WX + 330, WY + 152, "এখানে ক্যাবল নয়", T_SMALL, "#7A8590", 400)

    # ── জোন-ব্যাজ ───────────────────────────────────────────────────
    s.badge(WX + 116, WY + BAND / 2, "১", 20, GREEN)
    s.badge(WX + BAND / 2, WY + 214, "২", 20, GREEN)
    s.badge(WX + WW - BAND / 2, WY + 214, "২", 20, GREEN)
    s.badge(SW_X + 26, WY + 148, "৩", 20, GREEN)
    s.badge(WX + 130, SO_CY, "৩", 20, GREEN)

    # ── রঙের ব্যাখ্যা ───────────────────────────────────────────────
    ly = WY + WH + SLAB + 26
    s.rect(WX - 46, ly, WW + 92, 58, "#FCFDFE", LINE, 1.8, 11)
    s.rect(WX - 22, ly + 18, 34, 22, ZONE, ZONE_E, 2, 4)
    s.text(WX + 22, ly + 36, "অনুমোদিত অঞ্চল", T_SMALL, "#12523A", 700)
    s.line(WX + 236, ly + 29, WX + 278, ly + 29, CABLE, 4.6)
    s.text(WX + 288, ly + 36, "ক্যাবল", T_SMALL, "#37424E", 700)
    s.line(WX + 388, ly + 29, WX + 430, ly + 29, RED, 4.4, dash="13 8")
    s.text(WX + 440, ly + 36, "নিষিদ্ধ রুট", T_SMALL, RED, 700)

    # ── ডান পাশের কার্ড ─────────────────────────────────────────────
    x0, PW = 800, 388

    def card(y, head, items, col, bg, tcol, badges=False):
        """কার্ডের উচ্চতা লেখার পরিমাণ থেকেই ঠিক হয় — লেখা কিনারা কাটে না।"""
        mw = PW - (84 if badges else 76)
        wrapped = [wrap(it, mw, T_SMALL, 400) for it in items]
        h = 78 + sum(len(w_) * T_SMALL * 1.32 + 16 for w_ in wrapped) + 8
        s.rect(x0, y, PW, h, bg, col, 2, 12)
        s.text(x0 + PW / 2, y + 38, head, T_BODY, tcol, 700, "middle")
        yy = y + 78
        for k, lines in enumerate(wrapped):
            if badges:
                s.badge(x0 + 32, yy - 7, ["১", "২", "৩"][k], 19, col)
                tx = x0 + 56
            else:
                s.circle(x0 + 30, yy - 7, 5, col)
                tx = x0 + 48
            for j, ln in enumerate(lines):
                s.text(tx, yy + j * T_SMALL * 1.32, ln, T_SMALL, "#2E3842", 400)
            yy += len(lines) * T_SMALL * 1.32 + 16
        return y + h + 24

    cy = card(WY - SLAB, "সবুজ অঞ্চল: এখানেই ক্যাবল টানা যায়",
              ["দেয়ালের একেবারে উপরে ১৫০ মিমি চওড়া ব্যান্ড",
               "দুই দেয়ালের কোণা ঘেঁষে ১৫০ মিমি ব্যান্ড",
               "সুইচ বা সকেট বরাবর সোজা উল্লম্ব ও অনুভূমিক পথ"],
              GREEN, GREENBG, "#12523A", badges=True)
    cy = card(cy, "যা করা যাবে না",
              ["কোনাকুনি বা তির্যকভাবে ক্যাবল টানা",
               "অনুমোদিত অঞ্চলের বাইরে অগভীরে ক্যাবল বসানো",
               "ডিটেক্টর ছাড়া অজানা দেয়ালে ছিদ্র করা"],
              RED, REDBG, "#7A1810")
    cy = card(cy, "অঞ্চলের বাইরে টানতেই হলে",
              ["ক্যাবল পৃষ্ঠ থেকে ৫০ মিমি-এর বেশি গভীরে বসাতে হবে",
               "নয়তো ধাতব কন্ডুইট বা আর্থ করা আবরণ দিতে হবে"],
              AMBER, AMBERBG, "#7A5200")

    # ── নিচের বার্তা ────────────────────────────────────────────────
    ny = max(ly + 58, cy) + 4
    s.rect(60, ny, 1120, 88, REDBG, RED, 2, 11)
    s.text(620, ny + 36, "সবুজ অঞ্চলেই ক্যাবল থাকে, তাই ওই অংশে পেরেক বা ড্রিল বসানো যাবে না।",
           T_SMALL, "#7A1810", 700, "middle")
    s.text(620, ny + 68, "অন্য জায়গাতেও আগে ডিটেক্টর দিয়ে যাচাই করে নিতে হবে।",
           T_SMALL, "#7A1810", 400, "middle")
    s.fit(ny + 88, 22)
    return s.save(f"{OUT}/d05_drill_zones.svg")



def _bullet_panel(s, x, y, w, items, size=T_BODY, fill="#F7FAFC", stroke=LINE,
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


def d06_classification():
    """Four-way classification of electrical tools."""
    s = SVG(1400, 900)
    s.title("ইলেকট্রিক্যাল টুলসের শ্রেণিবিভাগ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 16)
    rx, ry, rw, rh = s.box_auto(700, 74, "ইলেকট্রিক্যাল টুলস", T_NODE,
                                fill=NAVY, stroke=NAVY, tcolor="#FFFFFF",
                                pad_x=34, pad_y=17)
    cols = [
        ("হ্যান্ড টুলস", "#E8F0F8", STEEL,
         ["হাতের শক্তিতে চলে, বিদ্যুতে নয়",
          "স্ক্রু ড্রাইভার, প্লায়ার্স, হ্যামার",
          "করাত, ফাইল, চিজেল, রেঞ্চ",
          "দাম কম, বহন করা সহজ"]),
        ("পাওয়ার টুলস", "#FFF6E5", AMBER,
         ["বিদ্যুৎ বা ব্যাটারিতে চলে",
          "ড্রিল, গ্রাইন্ডার, ওয়াল চেজার",
          "ভারী ও দ্রুতগতির কাজে",
          "ব্যবহারে বাড়তি সতর্কতা লাগে"]),
        ("মেজারিং টুলস", "#EAF6EF", GREEN,
         ["পরিমাপ ও যাচাইয়ের কাজে",
          "মেজারিং টেপ, ওয়্যার গেজ",
          "স্পিরিট লেভেল, ট্রাই স্কয়ার",
          "মাল্টিমিটার (অধ্যায় ৮)"]),
        ("সেফটি টুলস", "#FDECEA", RED,
         ["কর্মীকে সুরক্ষা দেয়",
          "ইনসুলেটেড টুল, রাবার ম্যাট",
          "লাইন টেস্টার, ভোল্টেজ ডিটেক্টর",
          "PPE (অধ্যায় ১)"]),
    ]
    cw, gapx = 320, 22
    x0 = (1400 - (4 * cw + 3 * gapx)) / 2
    ytop = 246
    s.path(f"M 700 {ry+rh:.1f} L 700 {ytop-76:.1f}", STEEL, 2.6)
    for i, (name, bg, br, items) in enumerate(cols):
        cx = x0 + i * (cw + gapx) + cw / 2
        s.path(f"M 700 {ytop-76:.1f} L {cx:.1f} {ytop-76:.1f} L {cx:.1f} {ytop-22:.1f}",
               STEEL, 2.6, marker=ar)
        s.box_auto(cx, ytop - 12, name, 27, fill=br, stroke=br,
                   tcolor="#FFFFFF", pad_x=24, pad_y=13, min_w=230)
    bot = 0
    for i, (name, bg, br, items) in enumerate(cols):
        bot = max(bot, _bullet_panel(s, x0 + i * (cw + gapx), ytop + 62, cw,
                                     items, 25, bg, br, INK, br))
    s.text(700, bot + 48,
           "প্রতিটি শ্রেণির টুল তার নিজের কাজেই ব্যবহার করতে হয়, অন্য কাজের বিকল্প হিসেবে নয়",
           25, GREY, 400, "middle")
    s.fit(bot + 48, 26)
    return s.save(f"{OUT}/d06_classification.svg")


def d07_maintenance():
    """Daily tool-care routine."""
    s = SVG(1240, 440)
    s.title("প্রতিদিনের কাজ শেষে টুলস রক্ষণাবেক্ষণের ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)
    steps = [("পরিষ্কার", "ধুলা ও গ্রিজ মোছা"),
             ("পরীক্ষা", "ফাটল ও ক্ষয় দেখা"),
             ("তেল দেওয়া", "কব্জা ও ধাতব অংশে"),
             ("ধার দেওয়া", "চিজেল ও ব্লেড"),
             ("সংরক্ষণ", "শুকনো টুল বক্সে")]
    bw, gap = 208, 32
    x0 = (1240 - (5 * bw + 4 * gap)) / 2
    for i, (t, d) in enumerate(steps):
        x = x0 + i * (bw + gap)
        s.rect(x, 126, bw, 150, "#F5F9FC", STEEL, 2, 13)
        s.circle(x + bw / 2, 126, 28, NAVY)
        s.text(x + bw / 2, 136, ["১", "২", "৩", "৪", "৫"][i], T_NODE,
               "#FFFFFF", 700, "middle")
        s.text(x + bw / 2, 196, t, T_NAME, NAVY, 700, "middle")
        for j, ln in enumerate(wrap(d, bw - 30, T_SMALL, 400)):
            s.text(x + bw / 2, 228 + j * T_SMALL * 1.32, ln, T_SMALL,
                   "#4A5561", 400, "middle")
        if i < 4:
            s.path(f"M {x+bw+5:.1f} 201 L {x+bw+gap-7:.1f} 201", STEEL, 2.8, marker=ar)
    s.rect(x0, 318, 5 * bw + 4 * gap, 58, "#EAF6EF", GREEN, 2, 11)
    s.text(620, 355, "গোছানো টুল বক্সই একজন কারিগরের প্রথম পরিচয়",
           T_NAME, "#12523A", 700, "middle")
    s.fit(376, 22)
    return s.save(f"{OUT}/d07_maintenance.svg")


ALL = [d01_screwdriver, d02_iec60900_marking, d03_stripping,
       d04_protection_class, d05_drill_zones,
       d06_classification, d07_maintenance]

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
