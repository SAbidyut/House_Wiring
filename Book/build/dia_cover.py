# -*- coding: utf-8 -*-
"""dia_cover.py — বইয়ের প্রচ্ছদ (full-bleed A4 আর্টওয়ার্ক)।

ক্যানভাস ১২৪০ × ১৭৫৪ px = A4-এর অনুপাত (১:১.৪১৪২), পূর্ণ পৃষ্ঠাজুড়ে বসে।
১২৪০ px ২১০ মিমি চওড়া হলে ১ px = ০.৪৮ pt — তাই ১০০ px শিরোনাম ছাপে ৪৮ pt।

গঠন
    · উপরে সাদা মাস্টহেড পটি — RAPTI-র নিজস্ব লোগো (rapti.net) ও প্রতিষ্ঠানের নাম
    · সোনালি রুল
    · গাঢ় নেভি ক্ষেত্র — বইয়ের নাম, উপশিরোনাম, সংস্করণ
    · হালকা রেখায় একটি হাউস-ওয়্যারিং সার্কিট মোটিফ (দুটি বাস, তিনটি প্যারালাল
      ব্রাঞ্চ — বাতি, ফ্যান, সকেট; সিরিজে নয়, বইয়ের নিয়ম মেনেই আঁকা)
    · নিচে যোগাযোগ

প্রচ্ছদটি বইয়ে **PNG হিসেবেই** বসে, SVG নয় — যার কম্পিউটারে কালপুরুষ নেই তার
কাছেও প্রচ্ছদ হুবহু একই দেখাবে।  ভেতরের চিত্রগুলোর নিয়ম (SVG + PNG) এখানে
প্রযোজ্য নয়, কারণ প্রচ্ছদ কেউ Word-এ এডিট করবে না।
"""
import os
from svgkit import SVG, tw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "cover")
IMG = os.path.join(HERE, "assets", "cover")

W, H = 1240, 1754

BAND_H  = 300                     # সাদা মাস্টহেড পটি
GOLD    = "#C8A64B"
GOLD_L  = "#DCC176"
WHITE   = "#FFFFFF"
PALE    = "#A9C8E4"
PALE2   = "#8FB0CE"
SUB     = "#C5DAEC"
NAVY_D  = "#0B2947"
INKN    = "#0F3357"
GREYT   = "#5A6470"
MOTIF   = "#5C9AD4"
LATIN   = "Helvetica Neue"

CX = W / 2


def _motif(s):
    """হালকা রেখায় হাউস-ওয়্যারিং সার্কিট — দুটি বাস, তিনটি প্যারালাল ব্রাঞ্চ।

    গোটা মোটিফ একটি `<g opacity>`-এর ভেতরে আঁকা।  `svgkit.line()`-এ opacity
    আর্গুমেন্ট নেই, তাই প্রতিটি আকৃতিতে আলাদা করে দিলে রেখা পুরো গাঢ় আর
    বৃত্ত হালকা হয়ে যেত — গ্রুপে দিলে সব একই ঘনত্বে বসে।
    """
    sw = 2.4
    L_Y, N_Y = 1090.0, 1302.0
    # শেষ ব্রাঞ্চেই বাস শেষ — এর পরে টুকরো তার ঝুলে থাকলে সেটি অসমাপ্ত
    # কানেকশনের মতো দেখায়।  সুইচের ব্লেডও তাই সব কটি বাঁ দিকে, যাতে কোনোটি
    # বাসের কোণ ছাড়িয়ে না যায়।  পুরো মোটিফ ২১৫…১০২৫ — মাঝবরাবর।
    BUS_X0, BUS_X1 = 581.0, 1025.0

    s.add('<g opacity="0.42">')

    # এনার্জি মিটার
    s.rect(215, 1150, 130, 92, "none", MOTIF, sw, 6)
    s.line(215, 1182, 345, 1182, MOTIF, sw * 0.8)
    s.circle(280, 1214, 15, "none", MOTIF, sw * 0.8)

    # লাইন কন্ডাক্টর: মিটার → MCB → L বাস
    s.line(345, 1174, 425, 1174, MOTIF, sw)
    s.rect(425, 1148, 84, 52, "none", MOTIF, sw, 5)
    s.line(439, 1188, 495, 1158, MOTIF, sw * 0.85)
    s.line(509, 1174, BUS_X0, 1174, MOTIF, sw)
    s.line(BUS_X0, 1174, BUS_X0, L_Y, MOTIF, sw)
    s.line(BUS_X0, L_Y, BUS_X1, L_Y, MOTIF, sw)

    # নিউট্রাল কন্ডাক্টর: মিটার → N বাস
    s.line(345, 1218, BUS_X0, 1218, MOTIF, sw)
    s.line(BUS_X0, 1218, BUS_X0, N_Y, MOTIF, sw)
    s.line(BUS_X0, N_Y, BUS_X1, N_Y, MOTIF, sw)

    for x, kind in ((725, "lamp"), (875, "fan"), (1025, "socket")):
        cy, r = 1215.0, 27.0
        s.line(x, L_Y, x, 1136, MOTIF, sw)               # L বাস থেকে ড্রপ
        s.line(x, 1136, x - 26, 1168, MOTIF, sw)         # সুইচের ব্লেড
        s.circle(x, 1176, 4, MOTIF, "none", 0)
        s.line(x, 1176, x, cy - r, MOTIF, sw)
        s.circle(x, cy, r, "none", MOTIF, sw)
        if kind == "lamp":
            s.line(x - 19, cy - 19, x + 19, cy + 19, MOTIF, sw * 0.85)
            s.line(x - 19, cy + 19, x + 19, cy - 19, MOTIF, sw * 0.85)
        elif kind == "fan":
            s.line(x, cy, x, cy + 21, MOTIF, sw * 0.85)
            s.line(x, cy, x - 18.2, cy - 10.5, MOTIF, sw * 0.85)
            s.line(x, cy, x + 18.2, cy - 10.5, MOTIF, sw * 0.85)
        else:
            s.circle(x - 9, cy - 5, 4.5, MOTIF, "none", 0)
            s.circle(x + 9, cy - 5, 4.5, MOTIF, "none", 0)
        s.line(x, cy + r, x, N_Y, MOTIF, sw)             # N বাসে ফেরত

    s.add("</g>")


def cover():
    s = SVG(W, H, bg=NAVY_D)

    s.defs.append(
        '<linearGradient id="bgg" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#0B2947"/>'
        '<stop offset="0.42" stop-color="#133F67"/>'
        '<stop offset="1" stop-color="#08203B"/></linearGradient>')
    s.add(f'<rect x="0" y="{BAND_H}" width="{W}" height="{H - BAND_H}" '
          f'fill="url(#bgg)"/>')

    # ── মাস্টহেড ────────────────────────────────────────────────────────
    s.rect(0, 0, W, BAND_H, WHITE, "none", 0, 0)
    # লোগোর উৎস-ফাইল ৩৫৬ px চওড়া; ২৬৪ px-এ বসালে ছাপে ≈২০৫ dpi — এর চেয়ে
    # বড় করলে ওয়ার্ডমার্ক নরম দেখাবে।
    lw, lh = 264.0, 96.4
    s.image(CX - lw / 2, 54, lw, lh, os.path.join(IMG, "logo_rapti.png"))
    s.text(CX, 208, "রেজোন্যান্স অটোমেশন প্রফেশনাল ট্রেনিং ইনস্টিটিউট",
           30, INKN, 700, "middle")
    s.text(CX, 240,
           "RESONANCE  AUTOMATION  PROFESSIONAL  TRAINING  INSTITUTE",
           13.5, GREYT, 500, "middle", family=LATIN, ls=2.6)
    s.text(CX, 274, "প্রতিষ্ঠাকাল ২০১৯   ·   ভুইঘর, নারায়ণগঞ্জ",
           17, GREYT, 400, "middle")
    s.rect(0, BAND_H, W, 5, GOLD, "none", 0, 0)

    # ── নেভি ক্ষেত্রের কিনারার রেখা ────────────────────────────────────
    s.rect(46, 348, W - 92, 1360, "none", GOLD, 1.4, 0, opacity=0.30)

    _motif(s)

    # ── শিরোনাম ব্লক ───────────────────────────────────────────────────
    s.text(CX, 452, "প্রশিক্ষণ পাঠ্যপুস্তক", 27, GOLD_L, 700, "middle", ls=12)
    s.text(CX, 592, "ইলেকট্রিক্যাল", 100, WHITE, 700, "middle")
    s.text(CX, 720, "হাউস ওয়্যারিং", 100, WHITE, 700, "middle")
    s.line(CX - 92, 774, CX + 92, 774, GOLD, 3)
    s.text(CX, 828, "ELECTRICAL HOUSE WIRING", 25, PALE, 300, "middle",
           family=LATIN, ls=7)
    s.text(CX, 896, "কোর্স মডিউল অনুযায়ী প্রণীত পূর্ণাঙ্গ পাঠ্যপুস্তক",
           26, SUB, 400, "middle")

    chip = "অধ্যায় ১–২৩   ·   প্রথম সংস্করণ ২০২৬"
    cwid = tw(chip, 23, 600) + 76
    s.rect(CX - cwid / 2, 934, cwid, 52, "none", GOLD, 1.5, 26, opacity=0.55)
    s.text(CX, 967, chip, 23, GOLD_L, 600, "middle")

    # ── যোগাযোগ ────────────────────────────────────────────────────────
    s.line(150, 1432, W - 150, 1432, GOLD, 1.2, dash=None)
    s.text(CX, 1492, "অ্যাডমিশন হটলাইন   ০১৬১৭-৩৪৫৫৩৪", 27, WHITE, 700, "middle")
    s.text(CX, 1538, "raptibd@gmail.com     ·     rapti.net", 22, PALE, 400,
           "middle", family=LATIN)
    s.text(CX, 1582,
           "২১০১, ভুইঘর, রূপায়ণ টাউন, গেট-১ সংলগ্ন, ফতুল্লা, নারায়ণগঞ্জ-১৪২০",
           20, PALE2, 400, "middle")

    return s.save(f"{OUT}/cover.svg")


ALL = [cover]

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
