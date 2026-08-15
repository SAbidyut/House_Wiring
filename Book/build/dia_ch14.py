# -*- coding: utf-8 -*-
"""অধ্যায় ১৪ — হাউস ওয়্যারিং: পদ্ধতি, লে-আউট ও এস্টিমেট : ডায়াগ্রাম।

সরবরাহ থেকে ঘরের SDB পর্যন্ত পথ এবং বসতবাড়ির সম্পূর্ণ ওয়্যারিং লে-আউট
RAPTI-র নিজস্ব `HW Connection Diagram All.pptx`-এর ৩০, ৩৪ ও ৩৬ নং স্লাইড
থেকে হুবহু বসানো।  ওয়্যারিং পদ্ধতির আলোকচিত্র ইনস্টিটিউটের
`Electrical House Wiring book.docx` থেকে।

শ্রেণীবিভাগের ছক, চার পদ্ধতির প্রস্থচ্ছেদ, লুপ-ইন বনাম জয়েন্ট বক্স,
ফ্ল্যাটের লে-আউট প্ল্যান, পয়েন্টের উচ্চতা, SDB-র সার্কিট বিভাজন ও
এস্টিমেটের ধাপ — এগুলোর সোর্স-ছবি নেই বলে নতুন করে আঁকা।
"""
import os
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch14")
IMG = os.path.join(HERE, "assets", "ch14")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
T_TINY = 20        # ৭.০ pt @ ১৫.৪ cm — বইয়ের সবচেয়ে ছোট টাইপ, এর নিচে নয়
T_CALL = 24
LH = 1.42

SYM = "#12324D"
SW = 3.4
LIVE = "#D42A1F"
NEUT = "#1F2933"
STRAP = "#1D5B8F"
GLOW = "#F5C445"
WALL = "#E4E9EF"
WALL_E = "#A2AEBB"
WOOD = "#B98A55"
PVC = "#E9EEF3"


# ── shared helpers ──────────────────────────────────────────────────────
def panel(s, x, y, w, h, title, col=STEEL):
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def note_strip(s, y, text, x=46, w=1148, fill="#EAF2FA", stroke=STEEL,
               tcolor=NAVY, size=T_NAME):
    lines = wrap(text, w - 60, size, 700)
    h = 22 + len(lines) * size * 1.36
    s.rect(x, y, w, h, fill, stroke, 2, 11)
    for i, ln in enumerate(lines):
        s.text(x + w / 2, y + 16 + size * 0.82 + i * size * 1.36, ln, size,
               tcolor, 700, "middle")
    return y + h


def img_panel(s, x, y, w, h, title, img, col=STEEL, cap=None):
    panel(s, x, y, w, h, title, col)
    top = y + 64
    bot = y + h - (44 if cap else 14)
    s.image_fit(x + 16, top, w - 32, bot - top, img, 6)
    if cap:
        for i, ln in enumerate(wrap(cap, w - 40, T_SMALL, 400)[:1]):
            s.text(x + w / 2, y + h - 18, ln, T_SMALL, GREY, 400, "middle")


def two_panel(fname, title, left, right, note, h=620, pw=560,
              lcol=STEEL, rcol=GREEN):
    s = SVG(1240, h)
    s.title(title, T_TITLE)
    ph = h - 96 - 96
    img_panel(s, 46, 96, pw, ph, left[0], f"{IMG}/{left[1]}", lcol,
              left[2] if len(left) > 2 else None)
    img_panel(s, 1194 - pw, 96, pw, ph, right[0], f"{IMG}/{right[1]}", rcol,
              right[2] if len(right) > 2 else None)
    y = note_strip(s, 96 + ph + 22, note)
    s.fit(y, 22)
    return s.save(f"{OUT}/{fname}.svg")


def one_panel(fname, title, head, img, note, h=700, col=STEEL):
    s = SVG(1240, h)
    s.title(title, T_TITLE)
    ph = h - 96 - 110
    img_panel(s, 46, 96, 1148, ph, head, f"{IMG}/{img}", col)
    y = note_strip(s, 96 + ph + 22, note)
    s.fit(y, 22)
    return s.save(f"{OUT}/{fname}.svg")


# ── plan / circuit symbols ──────────────────────────────────────────────
def lamp_sym(s, cx, cy, r=14, on=False):
    s.circle(cx, cy, r, GLOW if on else "#FFFFFF", SYM, 2.6)
    k = r * 0.66
    s.path(f"M {cx-k:.1f} {cy-k:.1f} L {cx+k:.1f} {cy+k:.1f}", SYM, 2.2)
    s.path(f"M {cx+k:.1f} {cy-k:.1f} L {cx-k:.1f} {cy+k:.1f}", SYM, 2.2)


def fan_sym(s, cx, cy, r=17):
    """সিলিং ফ্যান — কেন্দ্র থেকে তিনটি পাতা।"""
    s.circle(cx, cy, r, "#FFFFFF", SYM, 2.6)
    for a in (0, 120, 240):
        import math
        t = math.radians(a)
        x1, y1 = cx + r * 0.30 * math.cos(t), cy + r * 0.30 * math.sin(t)
        x2, y2 = cx + r * 0.92 * math.cos(t + 0.42), cy + r * 0.92 * math.sin(t + 0.42)
        s.path(f"M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}", SYM, 3.2)
    s.circle(cx, cy, r * 0.22, SYM)


def exhaust_sym(s, cx, cy, r=15):
    s.rect(cx - r, cy - r, 2 * r, 2 * r, "#FFFFFF", SYM, 2.6, 3)
    for a in (45, 135, 225, 315):
        import math
        t = math.radians(a)
        s.path(f"M {cx:.1f} {cy:.1f} L {cx + r*0.78*math.cos(t):.1f} "
               f"{cy + r*0.78*math.sin(t):.1f}", SYM, 2.6)


def socket3_sym(s, cx, cy, r=13):
    """৩-পিন সকেট — অর্ধবৃত্তের ভেতরে তিনটি বিন্দু।"""
    s.path(f"M {cx-r} {cy+r*0.5} A {r} {r} 0 0 1 {cx+r} {cy+r*0.5} Z",
           SYM, 2.6, "#FFFFFF")
    s.circle(cx, cy - r * 0.24, 2.4, SYM)
    s.circle(cx - r * 0.48, cy + r * 0.22, 2.4, SYM)
    s.circle(cx + r * 0.48, cy + r * 0.22, 2.4, SYM)


def socket2_sym(s, cx, cy, r=12):
    s.path(f"M {cx-r} {cy+r*0.5} A {r} {r} 0 0 1 {cx+r} {cy+r*0.5} Z",
           SYM, 2.4, "#FFFFFF")
    s.circle(cx - r * 0.40, cy, 2.3, SYM)
    s.circle(cx + r * 0.40, cy, 2.3, SYM)


def board_sym(s, cx, cy, w=30, h=19, col=SYM, n=3):
    s.rect(cx - w / 2, cy - h / 2, w, h, "#FFFFFF", col, 2.6, 3)
    for i in range(1, n):
        x = cx - w / 2 + i * w / n
        s.path(f"M {x:.1f} {cy-h/2:.1f} L {x:.1f} {cy+h/2:.1f}", col, 1.8)


def tag_sym(s, cx, cy, txt, w=40, h=24, fill=GREENBG, col=GREEN, size=T_TINY):
    s.rect(cx - w / 2, cy - h / 2, w, h, fill, col, 2.4, 4)
    s.text(cx, cy + size * 0.34, txt, size, col, 700, "middle")


def mcb_sym(s, x, y, w=46, h=30):
    """MCB — ছোট আয়তক্ষেত্রের ভেতরে তির্যক দাগ।"""
    s.rect(x, y - h / 2, w, h, "#FFFFFF", NAVY, 2.6, 4)
    s.path(f"M {x+9} {y+h*0.28:.1f} L {x+w-9} {y-h*0.28:.1f}", NAVY, 2.8)


# ═══════════════════════════════════════════════════════════════════════
def d01_wiring_tree():
    """বৈদ্যুতিক ওয়্যারিংয়ের শ্রেণীবিভাগ।"""
    s = SVG(1240, 760)
    s.title("বৈদ্যুতিক ওয়্যারিংয়ের শ্রেণীবিভাগ", T_TITLE)

    rx, ry, rw, rh = s.box_auto(620, 92, "বৈদ্যুতিক ওয়্যারিং", T_NODE,
                                fill=NAVY, stroke=NAVY, tcolor="#FFFFFF",
                                pad_x=30, pad_y=13)
    rb = ry + rh

    L2 = [(200, "ওভারহেড ওয়্যারিং", STEEL),
          (620, "অভ্যন্তরীণ ওয়্যারিং", NAVY),
          (1040, "আন্ডারগ্রাউন্ড ওয়্যারিং", STEEL)]
    bus1 = rb + 30
    s.path(f"M 620 {rb} L 620 {bus1}", GREY, 2.4)
    s.path(f"M {L2[0][0]} {bus1} L {L2[2][0]} {bus1}", GREY, 2.4)
    l2b = 0
    for cx, txt, col in L2:
        s.path(f"M {cx} {bus1} L {cx} {bus1+28}", GREY, 2.4)
        _, _, _, h = s.box_auto(cx, bus1 + 28, txt, T_NAME,
                                fill=LIGHT if col is STEEL else "#DCE8F4",
                                stroke=col, tcolor=NAVY, pad_x=22, pad_y=11)
        l2b = bus1 + 28 + h

    L3 = [(155, "ক্লিট বা ক্লিপ ওয়্যারিং"),
          (388, "ব্যাটেন ওয়্যারিং"),
          (620, "কেসিং ও চ্যানেল ওয়্যারিং"),
          (852, "কন্ডুইট ওয়্যারিং"),
          (1085, "ট্রাঙ্কিং ওয়্যারিং")]
    bus2 = l2b + 34
    s.path(f"M 620 {l2b} L 620 {bus2}", GREY, 2.4)
    s.path(f"M {L3[0][0]} {bus2} L {L3[-1][0]} {bus2}", GREY, 2.4)
    l3b = 0
    for cx, txt in L3:
        s.path(f"M {cx} {bus2} L {cx} {bus2+26}", GREY, 2.4)
        _, _, _, h = s.box_auto(cx, bus2 + 26, txt, T_BODY, fill="#F4F8FC",
                                stroke=STEEL, tcolor=NAVY, pad_x=16,
                                pad_y=11, max_w=182, min_w=206)
        l3b = max(l3b, bus2 + 26 + h)

    L4 = [(742, "সারফেস কন্ডুইট"), (996, "কনসিল্ড কন্ডুইট")]
    bus3 = l3b + 30
    s.path(f"M 852 {l3b} L 852 {bus3}", GREY, 2.4)
    s.path(f"M {L4[0][0]} {bus3} L {L4[1][0]} {bus3}", GREY, 2.4)
    l4b = 0
    for cx, txt in L4:
        s.path(f"M {cx} {bus3} L {cx} {bus3+24}", GREY, 2.4)
        _, _, _, h = s.box_auto(cx, bus3 + 24, txt, T_SMALL, fill=GREENBG,
                                stroke=GREEN, tcolor="#145034", pad_x=18,
                                pad_y=10)
        l4b = bus3 + 24 + h

    y = note_strip(s, l4b + 30,
                   "বাংলাদেশের বসতবাড়িতে এখন কার্যত দুটিই টেকে — "
                   "কেসিং/চ্যানেল আর কন্ডুইট; বাকিগুলো পুরোনো বা বিশেষ কাজের")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_wiring_tree.svg")


def d02_service_to_sdb():
    """সরবরাহ থেকে ঘরের SDB পর্যন্ত — RAPTI সোর্স।"""
    return one_panel(
        "d02_service_to_sdb", "সরবরাহ থেকে ঘরের বোর্ড পর্যন্ত পথ",
        "মেইন মিটার → সাব-মিটার → MCB → SDB → ঘরের পয়েন্ট",
        "h30_service_to_sdb.png",
        "খুঁটি থেকে সার্ভিস তার আসে মেইন মিটারে, সেখান থেকে সাব-মিটার ও "
        "মেইন ব্রেকার হয়ে SDB-তে; ঘরের প্রতিটি সার্কিট SDB থেকেই বেরোয়",
        h=740)


def d03_methods_section():
    """চার পদ্ধতির প্রস্থচ্ছেদ — দেয়ালের গায়ে তার কীভাবে বসে।"""
    s = SVG(1240, 640)
    s.title("চার পদ্ধতিতে দেয়ালের গায়ে তার কীভাবে বসে", T_TITLE)

    PW, GAP, PH = 278, 20, 392
    PY = 96
    FLOOR = PY + 214            # দেয়ালের উপরিতল
    cases = ["ক্লিট ওয়্যারিং", "ব্যাটেন ওয়্যারিং",
             "কেসিং-ক্যাপিং", "কন্ডুইট ওয়্যারিং"]
    descs = ["পোরসেলিনের ক্লিটে তার দেয়াল থেকে ফাঁক রেখে ঝোলে",
             "কাঠের পাটাতনের উপর ক্লিপ দিয়ে চ্যাপ্টা তার আঁটা",
             "খাঁজকাটা কেসিংয়ের ভেতরে তার, উপরে ক্যাপ আঁটা",
             "গোল পাইপের ভেতর দিয়ে তার, স্যাডলে পাইপ আঁটা"]
    cols = [RED, AMBER, STEEL, GREEN]

    for i, (head, desc, col) in enumerate(zip(cases, descs, cols)):
        px = 34 + i * (PW + GAP)
        cx = px + PW / 2
        panel(s, px, PY, PW, PH, head, col)

        # দেয়ালের প্রস্থচ্ছেদ — নিচের ব্যান্ডটাই দেয়াল
        s.rect(px + 20, FLOOR, PW - 40, 58, WALL, WALL_E, 2.2, 3)
        for k in range(6):
            hx = px + 34 + k * (PW - 68) / 5
            s.path(f"M {hx:.1f} {FLOOR+58} L {hx+14:.1f} {FLOOR+14}",
                   WALL_E, 1.4)

        if i == 0:                                   # ক্লিট
            for bx in (cx - 62, cx + 62):
                s.rect(bx - 22, FLOOR - 30, 44, 30, "#F1E4D4", "#9A7B57", 2.2, 3)
                s.rect(bx - 26, FLOOR - 44, 52, 16, "#F7EFE4", "#9A7B57", 2.2, 3)
            s.circle(cx - 74, FLOOR - 36, 7.5, LIVE, SYM, 2)
            s.circle(cx - 50, FLOOR - 36, 7.5, NEUT, SYM, 2)
            s.circle(cx + 50, FLOOR - 36, 7.5, LIVE, SYM, 2)
            s.circle(cx + 74, FLOOR - 36, 7.5, NEUT, SYM, 2)
        elif i == 1:                                 # ব্যাটেন
            s.rect(px + 44, FLOOR - 22, PW - 88, 22, WOOD, "#7E5A31", 2.2, 2)
            s.rect(px + 62, FLOOR - 42, PW - 124, 20, "#F5F7F9", SYM, 2.4, 3)
            s.circle(cx - 22, FLOOR - 32, 6.5, LIVE, SYM, 1.8)
            s.circle(cx + 22, FLOOR - 32, 6.5, NEUT, SYM, 1.8)
            for bx in (cx - 62, cx + 62):
                s.rect(bx - 6, FLOOR - 46, 12, 28, "#C6CFD8", "#7A8794", 1.8, 2)
        elif i == 2:                                 # কেসিং-ক্যাপিং
            s.rect(px + 56, FLOOR - 46, PW - 112, 46, PVC, SYM, 2.6, 3)
            s.path(f"M {cx:.1f} {FLOOR-40} L {cx:.1f} {FLOOR}", SYM, 2.2)
            s.rect(px + 50, FLOOR - 60, PW - 100, 16, "#D5DEE7", SYM, 2.6, 3)
            for ox in (-40, -16, 16, 40):
                s.circle(cx + ox, FLOOR - 22, 7, LIVE if ox < 0 else NEUT,
                         SYM, 1.8)
        else:                                        # কন্ডুইট
            s.circle(cx, FLOOR - 38, 36, PVC, SYM, 3.4)
            for ox, oy, c in ((-13, -8, LIVE), (13, -8, NEUT),
                              (0, 13, GREEN)):
                s.circle(cx + ox, FLOOR - 38 + oy, 8.5, c, SYM, 1.8)
            s.path(f"M {cx-46} {FLOOR} L {cx-46} {FLOOR-40} "
                   f"A 46 46 0 0 1 {cx+46} {FLOOR-40} L {cx+46} {FLOOR}",
                   "#8D9AA8", 4)

        s.text(cx, FLOOR + 108, "দেয়াল", T_SMALL, GREY, 400, "middle")
        for j, ln in enumerate(wrap(desc, PW - 44, T_TINY, 400)):
            s.text(cx, FLOOR + 142 + j * T_TINY * 1.38, ln, T_TINY,
                   "#39434D", 400, "middle")

    y = note_strip(s, PY + PH + 22,
                   "ক্লিট ও ব্যাটেন এখন বিএনবিসি-তে নিরুৎসাহিত; নতুন কাজে "
                   "কেসিং-ক্যাপিং বা কন্ডুইটই ব্যবহার করতে হবে",
                   fill=AMBERBG, stroke=AMBER, tcolor="#7A5200")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_methods_section.svg")


def d04_surface_conceal():
    """সারফেস ও কনসিল্ড কন্ডুইট — ইনস্টিটিউটের আলোকচিত্র।"""
    return two_panel(
        "d04_surface_conceal", "সারফেস বনাম কনসিল্ড কন্ডুইট",
        ("সারফেস কন্ডুইট — পাইপ দেয়ালের বাইরে", "p_surface_pipe.jpg",
         "স্যাডল দিয়ে আঁটা, পরে বদলানো সহজ"),
        ("কনসিল্ড কন্ডুইট — পাইপ দেয়ালের ভেতরে", "p_conceal_wall.jpg",
         "চ্যানেল কেটে পাইপ বসিয়ে প্লাস্টার"),
        "কনসিল্ড ওয়্যারিং দেখতে সুন্দর কিন্তু পরে বদলাতে হলে দেয়াল ভাঙতে "
        "হয় — তাই পাইপে ২০ SWG GI পুল-ওয়্যার রেখে দিতে হয়",
        h=640, lcol=GREEN, rcol=STEEL)


def d05_loop_in():
    """লুপ-ইন পদ্ধতি বনাম জয়েন্ট-বক্স পদ্ধতি।"""
    s = SVG(1240, 720)
    s.title("জয়েন্ট-বক্স পদ্ধতি বনাম লুপ-ইন পদ্ধতি", T_TITLE)

    PW, PH, PY = 560, 456, 96
    for i, (px, head, col) in enumerate(
            ((46, "জয়েন্ট-বক্স পদ্ধতি — বিএনবিসি-তে নিষিদ্ধ", RED),
             (634, "লুপ-ইন পদ্ধতি — এটিই করতে হবে", GREEN))):
        panel(s, px, PY, PW, PH, head, col)

        DB = px + 54
        BUS = PY + 186
        L1, L2 = px + 250, px + 430
        NY = PY + 330

        s.rect(DB - 26, BUS - 62, 52, 124, "#FFFFFF", NAVY, 3, 8)
        s.text(DB, BUS + 8, "DB", T_SMALL, NAVY, 700, "middle")

        if i == 0:
            # ফেজ — দুটি জোড়া বক্সের ভেতরে
            s.path(f"M {DB+26} {BUS} L {L2+52} {BUS}", LIVE, SW)
            for bx in (L1, L2):
                s.rect(bx - 21, BUS - 21, 42, 42, REDBG, RED, 2.8, 4)
                s.text(bx, BUS - 34, "জোড়া", T_TINY, RED, 700, "middle")
                s.path(f"M {bx} {BUS+21} L {bx} {BUS+72}", LIVE, SW)
                lamp_sym(s, bx, BUS + 96, 24, True)
            s.text(px + PW / 2, PY + PH - 96,
                   "জোড়াগুলো ছাদ বা দেয়ালের ভেতরে লুকিয়ে থাকে",
                   T_SMALL, RED, 700, "middle")
            s.text(px + PW / 2, PY + PH - 64,
                   "গরম হলে বা আলগা হলে খুঁজে বের করা যায় না",
                   T_SMALL, GREY, 400, "middle")
        else:
            # ফেজ — এক রোজ থেকে পরের রোজে লুপ হয়ে যায়, কোনো মাঝপথের জোড়া নেই
            s.path(f"M {DB+26} {BUS} L {L1} {BUS}", LIVE, SW)
            s.path(f"M {L1} {BUS} L {L2} {BUS}", LIVE, SW)
            for bx in (L1, L2):
                s.circle(bx, BUS, 22, "#FFFFFF", GREEN, 3)
                s.circle(bx, BUS, 5.5, GREEN)
                s.text(bx, BUS - 36, "সিলিং রোজ", T_TINY, GREEN, 700, "middle")
                s.path(f"M {bx} {BUS+22} L {bx} {BUS+72}", SYM, SW)
                lamp_sym(s, bx, BUS + 96, 24, True)
            s.text(px + PW / 2, PY + PH - 96,
                   "সব জোড়া রোজ ও সুইচবোর্ডের ভেতরে — হাতের নাগালে",
                   T_SMALL, GREEN, 700, "middle")
            s.text(px + PW / 2, PY + PH - 64,
                   "স্ক্রু খুলেই পরীক্ষা করা যায়, দেয়াল ভাঙতে হয় না",
                   T_SMALL, GREY, 400, "middle")

        # নিউট্রাল — দুই বাতির অন্য প্রান্ত একসঙ্গে DB-তে
        s.path(f"M {L1} {BUS+120} L {L1} {NY} L {DB} {NY} L {DB} {BUS+62}",
               NEUT, SW)
        s.path(f"M {L2} {BUS+120} L {L2} {NY}", NEUT, SW)

    y = note_strip(s, PY + PH + 24,
                   "বিএনবিসি পার্ট ৮-এর ১.৩.৯.৩.১ ধারা স্পষ্ট — সব ফাইনাল "
                   "সার্কিট লুপ ওয়্যারিং পদ্ধতিতে করতে হবে, কোনো জয়েন্ট বক্স "
                   "ব্যবহার করা যাবে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_loop_in.svg")


def d06_house_layout_src():
    """বসতবাড়ির ওয়্যারিং লে-আউট — RAPTI সোর্স।"""
    return two_panel(
        "d06_house_layout_src", "বসতবাড়ির ওয়্যারিং — ইনস্টিটিউটের নমুনা",
        ("কন্ডুইট ওয়্যারিং, পিয়ানো সুইচবোর্ড", "h34_house_conduit.png"),
        ("দুই পদ্ধতি পাশাপাশি — পিয়ানো ও গ্যাং", "h36_house_both.png"),
        "মিটার থেকে MCB, MCB থেকে SDB, SDB থেকে প্রতিটি সার্কিট — "
        "নিচের পাইপে সার্কিটের তার, উপরের পাইপে পয়েন্টের তার",
        h=650, lcol=STEEL, rcol=GREEN)


def d07_flat_layout():
    """একটি ফ্ল্যাটের সম্পূর্ণ ইলেকট্রিক্যাল লে-আউট প্ল্যান।"""
    s = SVG(1240, 800)
    s.title("একটি ফ্ল্যাটের ইলেকট্রিক্যাল লে-আউট (১০.০ × ৬.০ মি)", T_TITLE)

    X0, Y0, SC = 56, 132, 84.0                       # px প্রতি মিটার

    def mx(m):
        return X0 + m * SC

    def my(m):
        return Y0 + m * SC

    ROOMS = [
        ((0.0, 0.0, 5.2, 3.6), "ড্রইং ও ডাইনিং", "৫.২ × ৩.৬ মি"),
        ((5.2, 0.0, 10.0, 3.6), "মাস্টার বেডরুম", "৪.৮ × ৩.৬ মি"),
        ((0.0, 3.6, 2.6, 6.0), "রান্নাঘর", "২.৬ × ২.৪ মি"),
        ((2.6, 3.6, 4.2, 6.0), "কমন ওয়াশরুম", "১.৬ × ২.৪ মি"),
        ((4.2, 3.6, 5.6, 6.0), "করিডোর", "১.৪ × ২.৪ মি"),
        ((5.6, 3.6, 10.0, 6.0), "চিলড্রেন বেডরুম", "৪.৪ × ২.৪ মি"),
    ]
    # বাইরের দেয়াল
    s.rect(mx(0), my(0), 10.0 * SC, 6.0 * SC, "#FBFCFD", NAVY, 4.5, 4)
    for (a, b, c, d), name, dim in ROOMS:
        s.rect(mx(a), my(b), (c - a) * SC, (d - b) * SC, "#FFFFFF",
               WALL_E, 2.4, 2)
    # মাস্টার বেডের অ্যাটাচড ওয়াশ
    s.rect(mx(8.6), my(2.3), 1.4 * SC, 1.3 * SC, "#F4F7FA", WALL_E, 2.4, 2)

    labels = [(0.16, 0.42, "ড্রইং ও ডাইনিং", 3.4), (5.36, 0.42, "মাস্টার বেডরুম", 3.2),
              (0.14, 3.98, "রান্নাঘর", 2.3), (2.72, 3.98, "কমন ওয়াশরুম", 1.35),
              (4.30, 5.62, "করিডোর", 1.2), (5.74, 3.98, "চিলড্রেন বেডরুম", 3.0),
              (8.70, 2.68, "অ্যাটাচড ওয়াশ", 1.25)]
    for lx, ly, name, wm in labels:
        lines = wrap(name, wm * SC, T_TINY, 700)
        for j, ln in enumerate(lines):
            s.text(mx(lx), my(ly) + j * T_TINY * 1.34, ln, T_TINY, STEEL,
                   700, "start")

    # ── পয়েন্ট বসানো ──────────────────────────────────────────────────
    for px_, py_ in ((1.15, 1.05), (2.60, 1.05), (4.05, 1.05), (1.15, 2.95)):
        lamp_sym(s, mx(px_), my(py_))
    for px_, py_ in ((2.60, 2.95), (4.05, 2.95)):
        lamp_sym(s, mx(px_), my(py_), 11)
    fan_sym(s, mx(1.90), my(2.00))
    fan_sym(s, mx(3.40), my(2.00))
    socket3_sym(s, mx(0.30), my(2.30))
    socket3_sym(s, mx(3.05), my(3.38))
    board_sym(s, mx(4.90), my(3.34))

    for px_, py_ in ((6.25, 0.95), (7.85, 0.95)):
        lamp_sym(s, mx(px_), my(py_))
    for px_, py_ in ((6.25, 2.60), (7.85, 2.60)):
        lamp_sym(s, mx(px_), my(py_), 11)
    fan_sym(s, mx(7.05), my(1.80))
    socket3_sym(s, mx(5.45), my(1.70))
    tag_sym(s, mx(9.55), my(0.55), "AC")
    board_sym(s, mx(5.48), my(3.34))
    socket2_sym(s, mx(5.95), my(3.34))     # বোর্ডের গায়েই — বিএনবিসি ১.৩.৮.২.৬
    lamp_sym(s, mx(9.55), my(3.25), 11)

    for px_, py_ in ((6.45, 4.35), (8.05, 4.35)):
        lamp_sym(s, mx(px_), my(py_))
    for px_, py_ in ((6.45, 5.55), (8.05, 5.55)):
        lamp_sym(s, mx(px_), my(py_), 11)
    fan_sym(s, mx(7.25), my(4.95))
    socket3_sym(s, mx(5.90), my(5.62))
    tag_sym(s, mx(9.55), my(4.20), "AC")
    board_sym(s, mx(5.90), my(4.62))

    lamp_sym(s, mx(1.30), my(4.35), 11)
    exhaust_sym(s, mx(0.32), my(5.25))
    socket3_sym(s, mx(1.05), my(5.70))
    socket3_sym(s, mx(2.32), my(4.62))
    board_sym(s, mx(2.30), my(5.70))

    lamp_sym(s, mx(3.40), my(4.35), 11)
    tag_sym(s, mx(3.40), my(5.30), "গিজার", 66, 24, AMBERBG, AMBER)
    socket2_sym(s, mx(4.50), my(3.34))     # ড্রইংয়ের বোর্ডের গায়ে

    lamp_sym(s, mx(4.90), my(4.95), 11)
    s.rect(mx(4.34), my(3.68), 1.12 * SC, 0.44 * SC, "#FFFFFF", NAVY, 3, 4)
    s.text(mx(4.90), my(3.98), "SDB", T_TINY, NAVY, 700, "middle")

    # ── লেজেন্ড ────────────────────────────────────────────────────────
    LX, LY = 928, 150
    s.rect(LX, LY - 34, 268, 470, "#F7FAFC", LINE, 2, 10)
    s.text(LX + 134, LY, "প্রতীক", T_BODY, NAVY, 700, "middle")
    items = [("lamp", "টিউব বাতি (২০ W)"), ("lamp_s", "এলইডি বাল্ব (১২ W)"),
             ("fan", "সিলিং ফ্যান"), ("exh", "এক্সহস্ট ফ্যান"),
             ("s3", "৩-পিন সকেট (১৩A)"), ("s2", "২-পিন সকেট (৫A)"),
             ("brd", "সুইচবোর্ড"), ("ac", "AC পয়েন্ট"),
             ("gys", "গিজার পয়েন্ট"), ("sdb", "সাব-ডিস্ট্রিবিউশন বোর্ড")]
    for i, (kind, txt) in enumerate(items):
        gy = LY + 40 + i * 42
        gx = LX + 34
        if kind == "lamp":
            lamp_sym(s, gx, gy)
        elif kind == "lamp_s":
            lamp_sym(s, gx, gy, 11)
        elif kind == "fan":
            fan_sym(s, gx, gy, 15)
        elif kind == "exh":
            exhaust_sym(s, gx, gy, 13)
        elif kind == "s3":
            socket3_sym(s, gx, gy)
        elif kind == "s2":
            socket2_sym(s, gx, gy)
        elif kind == "brd":
            board_sym(s, gx, gy)
        elif kind == "ac":
            tag_sym(s, gx, gy, "AC", 46, 26)
        elif kind == "gys":
            tag_sym(s, gx, gy, "গি", 46, 26, AMBERBG, AMBER)
        else:
            s.rect(gx - 24, gy - 11, 48, 22, "#FFFFFF", NAVY, 2.4, 3)
            s.text(gx, gy + 6, "SDB", 15, NAVY, 700, "middle")
        s.text(LX + 68, gy + 7, txt, T_TINY, "#39434D", 400, "start")

    y = note_strip(s, my(6.0) + 26,
                   "লে-আউটে আগে পয়েন্ট বসে, তারপর সার্কিট ভাগ হয়, সবশেষে "
                   "কন্ডুইটের পথ আঁকা হয় — উল্টো করলে পাইপ টানার পর পয়েন্ট "
                   "সরাতে হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d07_flat_layout.svg")


def d08_heights():
    """পয়েন্ট ও বোর্ড বসানোর উচ্চতা — বিএনবিসি অনুযায়ী।"""
    s = SVG(1240, 780)
    s.title("পয়েন্ট ও বোর্ড বসানোর উচ্চতা", T_TITLE)

    FLOOR, PPM = 660, 172.0                          # px প্রতি মিটার
    CEIL = FLOOR - int(3.0 * PPM)

    def hy(m):
        return FLOOR - m * PPM

    # ছাদ ও মেঝে
    s.rect(300, CEIL - 22, 420, 22, "#DDE4EB", WALL_E, 2.2, 2)
    s.rect(220, FLOOR, 580, 26, "#DDE4EB", WALL_E, 2.2, 2)
    for k in range(14):
        s.path(f"M {230 + k*40} {FLOOR+26} L {244 + k*40} {FLOOR+6}",
               WALL_E, 1.4)
    # দেয়াল
    s.rect(300, CEIL, 24, FLOOR - CEIL, WALL, WALL_E, 2.2, 0)

    items = [
        (2.50, "সিলিং ফ্যানের পাতা", "মেঝে থেকে কমপক্ষে ২.৫ মি", "fan"),
        (2.10, "AC-র ইনডোর ইউনিট", "চোখের উপরে, বাতাসের পথ খোলা", "ac"),
        (1.60, "SDB / ডিস্ট্রিবিউশন বোর্ড", "১.৫–১.৮ মি — হাতের নাগালে, "
                                            "শিশুর নাগালের বাইরে", "sdb"),
        (1.22, "সুইচবোর্ডের তলা", "বিএনবিসি ১.৩.১১.৫ — বাসাবাড়িতে ১২২০ mm",
         "brd"),
        (0.25, "৩-পিন সকেট", "বিএনবিসি ১.৩.৮.২.৪ — ২৫৪ mm", "s3"),
    ]
    for m, name, note, kind in items:
        y = hy(m)
        gx = 380
        if kind == "fan":
            s.path(f"M 312 {y-92:.1f} L 312 {y:.1f}", "#8D9AA8", 5)
            fan_sym(s, gx, y, 30)
        elif kind == "ac":
            s.rect(gx - 62, y - 22, 124, 44, "#FFFFFF", STEEL, 3, 5)
            s.text(gx, y + 8, "AC", T_SMALL, STEEL, 700, "middle")
        elif kind == "sdb":
            s.rect(gx - 52, y - 30, 104, 60, "#FFFFFF", NAVY, 3, 5)
            s.text(gx, y + 8, "SDB", T_SMALL, NAVY, 700, "middle")
        elif kind == "brd":
            board_sym(s, gx, y, 92, 52)
        else:
            socket3_sym(s, gx, y, 24)

        s.path(f"M 324 {y:.1f} L {gx-70:.1f} {y:.1f}", GREY, 1.8, dash="7 5")
        s.path(f"M {gx+72:.1f} {y:.1f} L 742 {y:.1f}", STEEL, 2.2, dash="7 5")
        s.circle(742, y, 5, STEEL)
        s.text(762, y - 8, name, T_CALL, NAVY, 700, "start")
        s.text(762, y + 22, note, T_TINY, GREY, 400, "start")

    s.text(560, FLOOR + 70, "মেঝে", T_BODY, GREY, 700, "middle")
    s.text(510, CEIL - 36, "ছাদ (~৩.০ মি)", T_BODY, GREY, 700, "middle")

    y = note_strip(s, FLOOR + 100,
                   "উচ্চতা মাপা হয় ফিনিশড মেঝে থেকে সরঞ্জামের তলা পর্যন্ত — "
                   "টাইলস বসার আগে মাপলে দেড় ইঞ্চি ভুল হয়ে যায়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d08_heights.svg")


def d09_circuits():
    """SDB থেকে সার্কিট বিভাজন — সিঙ্গেল লাইন ডায়াগ্রাম।"""
    s = SVG(1240, 960)
    s.title("ফ্ল্যাটটির SDB ও সার্কিট বিভাজন", T_TITLE)

    # ইনকামিং
    s.rect(46, 104, 176, 64, "#FFFFFF", NAVY, 3, 8)
    s.text(134, 144, "এনার্জি মিটার", T_SMALL, NAVY, 700, "middle")
    s.path("M 222 136 L 268 136", LIVE, SW)
    mcb_sym(s, 268, 136, 74, 40)
    s.text(305, 108, "মেইন DP ৪০A", T_TINY, NAVY, 700, "middle")
    s.path("M 342 136 L 440 136 L 440 214", LIVE, SW)

    BX = 440
    rows = [
        ("C1", "৫A", "১.৫ mm²", "ড্রইং ও ডাইনিং — ৬ বাতি, ২ ফ্যান", "৩২৪ W", GREEN),
        ("C2", "৫A", "১.৫ mm²", "মাস্টার বেডরুম ও ওয়াশ — ৫ বাতি, ১ ফ্যান", "২১৬ W", GREEN),
        ("C3", "৫A", "১.৫ mm²", "চিলড্রেন বেডরুম — ৪ বাতি, ১ ফ্যান", "১৪৪ W", GREEN),
        ("C4", "৫A", "১.৫ mm²", "রান্নাঘর, ওয়াশ ও করিডোর — ৩ বাতি, এক্সহস্ট", "৭৬ W", GREEN),
        ("C5", "১৬A", "৪ mm²", "৩-পিন সকেট — ড্রইং ২ + মাস্টার ১", "৬০০ W", STEEL),
        ("C6", "১৬A", "৪ mm²", "৩-পিন সকেট — চিলড্রেন ১ + রান্নাঘর ২", "৬০০ W", STEEL),
        ("C7", "১৬A", "৪ mm²", "গিজার — নিজস্ব সার্কিট", "১৫০০ W", AMBER),
        ("C8", "২০A", "৪ mm²", "মাস্টার বেডরুমের AC", "১৫০০ W", AMBER),
        ("C9", "২০A", "৪ mm²", "চিলড্রেন বেডরুমের AC", "১৫০০ W", AMBER),
    ]
    y = 242
    GAP = 54
    for tag, amp, cab, desc, load, col in rows:
        s.path(f"M {BX} {y} L {BX+44} {y}", LIVE, SW)
        mcb_sym(s, BX + 44, y)
        s.path(f"M {BX+90} {y} L {BX+140} {y}", SYM, SW)
        s.circle(BX + 140, y, 5.5, col)
        s.text(BX - 14, y + 7, tag, T_SMALL, NAVY, 700, "end")
        s.text(BX + 67, y - 25, amp, T_TINY, NAVY, 700, "middle")
        s.text(BX + 158, y + 7, desc, T_SMALL, "#28313B", 400, "start")
        s.text(1192, y + 7, f"{cab} · {load}", T_TINY, col, 700, "end")
        y += GAP

    # স্পেয়ার ওয়ে
    for k in range(2):
        s.path(f"M {BX} {y} L {BX+44} {y}", GREY, 2.4, dash="8 6")
        s.rect(BX + 44, y - 15, 46, 30, "#F4F7FA", GREY, 2.2, 4, dash="7 5")
        s.text(BX + 158, y + 7, "স্পেয়ার ওয়ে — ভবিষ্যতের জন্য খালি রাখা",
               T_SMALL, GREY, 400, "start")
        y += GAP

    s.path(f"M {BX} 214 L {BX} {y - GAP}", NAVY, 5)
    s.rect(396, 196, 806, y - GAP - 170, "none", STEEL, 2.4, 12, dash="10 7")
    s.text(396, 186, "SDB — ১২ ওয়ে (উল্লম্ব মোটা দাগটিই বাসবার)",
           T_SMALL, STEEL, 700, "start")

    yy = note_strip(s, y - GAP + 46,
                    "বিএনবিসি প্রতি পাঁচটি ব্যবহৃত সার্কিটের জন্য অন্তত একটি "
                    "স্পেয়ার ওয়ে রাখতে বলে — নয়টি সার্কিটের জন্য দুটি, "
                    "অর্থাৎ ১১ ওয়ে; বাজারে পাওয়া যায় বলে ১২ ওয়ের বোর্ড কেনা হয়")
    s.fit(yy, 24)
    return s.save(f"{OUT}/d09_circuits.svg")


def d10_estimate_steps():
    """এস্টিমেট তৈরির ছয় ধাপ।"""
    s = SVG(1240, 560)
    s.title("এস্টিমেট তৈরির ছয় ধাপ", T_TITLE)

    steps = [
        ("১", "লে-আউট চূড়ান্ত", "প্রতিটি ঘরে বাতি, ফ্যান, সকেট ও বোর্ড "
                                "কোথায় বসবে তা কাগজে বসাও"),
        ("২", "পয়েন্ট গোনা", "লাইট, ফ্যান, সকেট, AC, গিজার — ধরনভেদে "
                              "আলাদা করে সংখ্যা লেখো"),
        ("৩", "সার্কিট ভাগ", "বাতি-ফ্যান আলাদা, সকেট আলাদা; প্রতিটির "
                             "তার ও ব্রেকার ঠিক করো"),
        ("৪", "দৈর্ঘ্য মাপা", "প্রতিটি পয়েন্টের তার ও পাইপের দৈর্ঘ্য "
                              "প্ল্যান থেকে মেপে যোগ করো"),
        ("৫", "মালামালের তালিকা", "পরিমাণে ১০% অপচয় ধরে বাজারদর বসিয়ে "
                                  "মোট মূল্য বের করো"),
        ("৬", "মজুরি ও আনুষঙ্গিক", "পয়েন্ট-রেটে মজুরি, তারপর পরিবহন ও "
                                   "অন্যান্য খরচ যোগ করো"),
    ]
    BW, BH, GX, GY = 360, 172, 30, 34
    X0, Y0 = 50, 110
    ar = s.arrow_defs(STEEL, "ar14", 15)
    for i, (num, head, body) in enumerate(steps):
        col, row = i % 3, i // 3
        x = X0 + col * (BW + GX)
        y = Y0 + row * (BH + GY)
        s.rect(x, y, BW, BH, "#F7FAFC", STEEL, 2.4, 12)
        s.badge(x + 40, y + 40, num, 22, NAVY, "#FFFFFF", 22)
        s.text(x + 76, y + 48, head, T_NAME, NAVY, 700, "start")
        for j, ln in enumerate(wrap(body, BW - 60, T_TINY, 400)):
            s.text(x + 30, y + 92 + j * T_TINY * 1.42, ln, T_TINY,
                   "#39434D", 400, "start")
        if col < 2:
            s.path(f"M {x+BW+4} {y+BH/2:.1f} L {x+BW+GX-6} {y+BH/2:.1f}",
                   STEEL, 2.6, marker=ar)
        elif row == 0:
            s.path(f"M {x+BW/2:.1f} {y+BH+4} L {x+BW/2:.1f} {y+BH+GY-6}",
                   STEEL, 2.6, marker=ar)

    y = note_strip(s, Y0 + 2 * BH + GY + 26,
                   "ধাপ এড়িয়ে সরাসরি মালামালের তালিকা লিখলে হিসাব "
                   "প্রায় সবসময়ই কম পড়ে — বিশেষত তারের দৈর্ঘ্যে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d10_estimate_steps.svg")


ALL = [d01_wiring_tree, d02_service_to_sdb, d03_methods_section,
       d04_surface_conceal, d05_loop_in, d06_house_layout_src,
       d07_flat_layout, d08_heights, d09_circuits, d10_estimate_steps]

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
