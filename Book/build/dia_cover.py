# -*- coding: utf-8 -*-
"""dia_cover.py — বইয়ের প্রচ্ছদ (full-bleed A4 আর্টওয়ার্ক)।

ক্যানভাস ১২৪০ × ১৭৫৪ px = A4-এর অনুপাত (১:১.৪১৪২), পূর্ণ পৃষ্ঠাজুড়ে বসে।
১২৪০ px ২১০ মিমি চওড়া হলে ১ px = ০.৪৮ pt — তাই ১০০ px শিরোনাম ছাপে ৪৮ pt।

ভাবনা — **একটি ড্রয়িং শিট**।  পুরো পৃষ্ঠা এক টানা গাঢ় নীল; তার উপর খুব
হালকা ব্লুপ্রিন্ট-গ্রিড, সোনালি কিনারার রেখা, আর নিচের অর্ধে ম্লান রেখায়
একটি হাউস-ওয়্যারিং সার্কিট।  আগের নকশায় উপরে সাদা পটি আর নিচে নীল —
দুই টুকরো দেখাচ্ছিল বলে ব্যবহারকারী তা বাতিল করেন (২০২৬-০৮-৩১)।  তাই সাদা
পটি নেই; RAPTI-র লোগো সরাসরি নীলের উপর বসে, "RAPTI" লেখাটি সাদা করে নেওয়া
হয়েছে (`assets_cover.py`-এর `_light_wordmark`)।

সার্কিট মোটিফ: দুটি বাস, তিনটি প্যারালাল ব্রাঞ্চ — বাতি, ফ্যান, সকেট;
সিরিজে নয়, বইয়ের নিয়ম মেনেই আঁকা।

প্রচ্ছদটি বইয়ে **PNG হিসেবেই** বসে, SVG নয় — যার কম্পিউটারে কালপুরুষ নেই তার
কাছেও প্রচ্ছদ হুবহু একই দেখাবে।
"""
import os
from svgkit import SVG, tw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "cover")
IMG = os.path.join(HERE, "assets", "cover")

W, H = 1240, 1754
CX = W / 2
INSET = 40                       # শিটের কিনারার রেখা

GOLD    = "#C8A64B"
GOLD_L  = "#DFC57E"
WHITE   = "#FFFFFF"
NEARW   = "#E9F1F8"
PALE    = "#A9C8E4"
PALE2   = "#8AAECD"
SUB     = "#C0D6EA"
NAVY_D  = "#0A2440"
MOTIF   = "#6FA8DC"
LATIN   = "Helvetica Neue"


def _sheet(s):
    """পটভূমি — নীল গ্রেডিয়েন্ট, ব্লুপ্রিন্ট-গ্রিড, সোনালি কিনারা।

    গ্রিড দুটি `<pattern>`, `s.add()` দিয়ে সরাসরি বসানো — `s.rect()` দিয়ে নয়।
    কারণ `qc.py` প্রতিটি রেকর্ড করা রেখাকে লেখার সঙ্গে মিলিয়ে দেখে, আর
    পটভূমির গ্রিড তো লেখার নিচ দিয়েই যাবে — সেটিই নকশা, ত্রুটি নয়।
    """
    s.defs.append(
        '<linearGradient id="bgg" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#0A2440"/>'
        '<stop offset="0.45" stop-color="#133D63"/>'
        '<stop offset="1" stop-color="#061829"/></linearGradient>')
    s.defs.append(
        '<pattern id="grid1" width="62" height="62" patternUnits="userSpaceOnUse">'
        '<path d="M 62 0 L 0 0 0 62" fill="none" stroke="#7FB3DD" '
        'stroke-width="1" opacity="0.07"/></pattern>')
    s.defs.append(
        '<pattern id="grid2" width="310" height="310" patternUnits="userSpaceOnUse">'
        '<path d="M 310 0 L 0 0 0 310" fill="none" stroke="#7FB3DD" '
        'stroke-width="1.5" opacity="0.13"/></pattern>')
    s.add(f'<rect width="{W}" height="{H}" fill="url(#bgg)"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="url(#grid1)"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="url(#grid2)"/>')
    s.add(f'<rect x="{INSET}" y="{INSET}" width="{W - 2*INSET}" '
          f'height="{H - 2*INSET}" fill="none" stroke="{GOLD}" '
          f'stroke-width="1.5" opacity="0.38"/>')


def _divider(s, y, half, sw=1.1, op=0.55):
    """মাঝখানে ছোট সোনালি হীরকসহ একটি সরু রেখা।"""
    s.add(f'<g opacity="{op}">'
          f'<line x1="{CX-half:.1f}" y1="{y}" x2="{CX-20:.1f}" y2="{y}" '
          f'stroke="{GOLD}" stroke-width="{sw}"/>'
          f'<line x1="{CX+20:.1f}" y1="{y}" x2="{CX+half:.1f}" y2="{y}" '
          f'stroke="{GOLD}" stroke-width="{sw}"/>'
          f'<polygon points="{CX:.1f},{y-6} {CX+6:.1f},{y} {CX:.1f},{y+6} '
          f'{CX-6:.1f},{y}" fill="{GOLD}"/></g>')


def _motif(s):
    """ম্লান রেখায় হাউস-ওয়্যারিং সার্কিট — দুটি বাস, তিনটি প্যারালাল ব্রাঞ্চ।

    গোটা মোটিফ একটি `<g opacity>`-এর ভেতরে।  `svgkit.line()`-এ opacity
    আর্গুমেন্ট নেই, তাই প্রতিটি আকৃতিতে আলাদা দিলে রেখা পুরো গাঢ় আর বৃত্ত
    হালকা হয়ে যেত।

    শেষ ব্রাঞ্চেই বাস শেষ — এর পরে টুকরো তার ঝুলে থাকলে অসমাপ্ত কানেকশনের
    মতো দেখায়।  সুইচের ব্লেডও তাই সব কটি বাঁ দিকে, যাতে কোনোটি বাসের কোণ
    ছাড়িয়ে না যায়।  পুরো মোটিফ ১৬৫…১০৭৫ — পৃষ্ঠার মাঝবরাবর।
    """
    sw = 2.6
    L_Y, N_Y = 1080.0, 1310.0
    BUS_X0, BUS_X1 = 575.0, 1075.0

    s.add('<g opacity="0.30">')

    # এনার্জি মিটার
    s.rect(165, 1148, 150, 100, "none", MOTIF, sw, 7)
    s.line(165, 1184, 315, 1184, MOTIF, sw * 0.8)
    s.circle(240, 1216, 17, "none", MOTIF, sw * 0.8)

    # লাইন কন্ডাক্টর: মিটার → MCB → L বাস
    s.line(315, 1176, 395, 1176, MOTIF, sw)
    s.rect(395, 1150, 100, 52, "none", MOTIF, sw, 5)
    s.line(411, 1190, 479, 1160, MOTIF, sw * 0.85)
    s.line(495, 1176, BUS_X0, 1176, MOTIF, sw)
    s.line(BUS_X0, 1176, BUS_X0, L_Y, MOTIF, sw)
    s.line(BUS_X0, L_Y, BUS_X1, L_Y, MOTIF, sw)

    # নিউট্রাল কন্ডাক্টর: মিটার → N বাস
    s.line(315, 1224, BUS_X0, 1224, MOTIF, sw)
    s.line(BUS_X0, 1224, BUS_X0, N_Y, MOTIF, sw)
    s.line(BUS_X0, N_Y, BUS_X1, N_Y, MOTIF, sw)

    for x, kind in ((715, "lamp"), (895, "fan"), (1075, "socket")):
        cy, r = 1212.0, 32.0
        s.line(x, L_Y, x, 1128, MOTIF, sw)               # L বাস থেকে ড্রপ
        s.line(x, 1128, x - 30, 1162, MOTIF, sw)         # সুইচের ব্লেড
        s.circle(x, 1170, 4.5, MOTIF, "none", 0)
        s.line(x, 1170, x, cy - r, MOTIF, sw)
        s.circle(x, cy, r, "none", MOTIF, sw)
        if kind == "lamp":
            s.line(x - 22, cy - 22, x + 22, cy + 22, MOTIF, sw * 0.85)
            s.line(x - 22, cy + 22, x + 22, cy - 22, MOTIF, sw * 0.85)
        elif kind == "fan":
            s.line(x, cy, x, cy + 25, MOTIF, sw * 0.85)
            s.line(x, cy, x - 21.7, cy - 12.5, MOTIF, sw * 0.85)
            s.line(x, cy, x + 21.7, cy - 12.5, MOTIF, sw * 0.85)
        else:
            s.circle(x - 10, cy - 6, 5, MOTIF, "none", 0)
            s.circle(x + 10, cy - 6, 5, MOTIF, "none", 0)
        s.line(x, cy + r, x, N_Y, MOTIF, sw)             # N বাসে ফেরত

    s.add("</g>")


def cover():
    s = SVG(W, H, bg=NAVY_D)
    _sheet(s)
    _motif(s)

    # ── প্রতিষ্ঠানের পরিচয় ─────────────────────────────────────────────
    # উৎস-ফাইল ৩৫৬ px চওড়া; ২৫০ px-এ বসালে ছাপে ≈২১৭ dpi — এর বেশি বড়
    # করলে ওয়ার্ডমার্ক নরম দেখাবে।
    lw, lh = 250.0, 91.3
    s.image(CX - lw / 2, 100, lw, lh, os.path.join(IMG, "logo_rapti_light.png"))
    s.text(CX, 252, "রেজোন্যান্স অটোমেশন প্রফেশনাল ট্রেনিং ইনস্টিটিউট",
           29, NEARW, 700, "middle")
    s.text(CX, 284, "RESONANCE  AUTOMATION  PROFESSIONAL  TRAINING  INSTITUTE",
           15, PALE2, 500, "middle", family=LATIN, ls=2.8)
    _divider(s, 326, 290)

    # ── শিরোনাম ────────────────────────────────────────────────────────
    s.text(CX, 424, "প্রশিক্ষণ পাঠ্যপুস্তক", 25, GOLD_L, 700, "middle", ls=13)
    s.text(CX, 564, "ইলেকট্রিক্যাল", 104, WHITE, 700, "middle")
    s.text(CX, 696, "হাউস ওয়্যারিং", 104, WHITE, 700, "middle")
    s.line(CX - 75, 754, CX + 75, 754, GOLD, 3)
    s.text(CX, 810, "ELECTRICAL HOUSE WIRING", 24, PALE, 300, "middle",
           family=LATIN, ls=8)
    s.text(CX, 872, "কোর্স মডিউল অনুযায়ী প্রণীত পূর্ণাঙ্গ পাঠ্যপুস্তক",
           25, SUB, 400, "middle")

    chip = "অধ্যায় ১–২৩   ·   প্রথম সংস্করণ ২০২৬"
    cwid = tw(chip, 22, 600) + 80
    s.rect(CX - cwid / 2, 910, cwid, 52, "none", GOLD, 1.5, 26, opacity=0.55)
    s.text(CX, 943, chip, 22, GOLD_L, 600, "middle")

    # ── যোগাযোগ ────────────────────────────────────────────────────────
    _divider(s, 1448, 340, sw=1.0, op=0.45)
    s.text(CX, 1508, "অ্যাডমিশন হটলাইন   ০১৬১৭-৩৪৫৫৩৪", 26, WHITE, 700, "middle")
    s.text(CX, 1552, "raptibd@gmail.com     ·     rapti.net", 21, PALE, 400,
           "middle", family=LATIN)
    s.text(CX, 1594,
           "২১০১, ভুইঘর, রূপায়ণ টাউন, গেট-১ সংলগ্ন, ফতুল্লা, নারায়ণগঞ্জ-১৪২০",
           19, PALE2, 400, "middle")

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
