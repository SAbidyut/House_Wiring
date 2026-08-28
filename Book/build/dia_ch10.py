# -*- coding: utf-8 -*-
"""অধ্যায় ১০ — সিরিজ বোর্ড : ডায়াগ্রাম।

সার্কিট ও কানেকশন ডায়াগ্রাম RAPTI-র নিজস্ব সোর্স থেকে হুবহু বসানো —
`Circuit Diagram.pptx` স্লাইড ১৬ (সার্কিট) এবং
`HW Connection Diagram All.pptx` স্লাইড ১৬ ও ৪০ (কানেকশন)।
বোর্ডের গঠন, প্রয়োজনীয়তা ও বাতির তিন অবস্থার চিত্র নতুন করে আঁকা।
"""
import os, math
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch10")
IMG = os.path.join(HERE, "assets", "ch10")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
T_CALL = 25
LH = 1.42

SYM = "#12324D"
SW = 3.4
LIVE = "#D42A1F"          # ফেজ তার — সোর্স ফাইলের মতো লাল
NEUT = "#1F2933"          # নিউট্রাল তার — কালো
PLATE = "#F2F5F8"
PLATE_E = "#9AA6B2"
METAL = "#8D9AA8"
GLASS = "#FFF2C4"


# ── shared helpers ──────────────────────────────────────────────────────
def panel(s, x, y, w, h, title, col=STEEL):
    s.rect(x, y, w, h, "#FCFDFE", LINE, 1.8, 13)
    s.box_auto(x + w / 2, y + 12, title, T_BODY, fill=col, stroke=col,
               tcolor="#FFFFFF", pad_x=22, pad_y=9)


def note_strip(s, y, text, x=46, w=1148, fill="#EAF2FA", stroke=STEEL,
               tcolor=NAVY, size=T_NAME):
    s.rect(x, y, w, 58, fill, stroke, 2, 11)
    s.text(x + w / 2, y + 36, text, size, tcolor, 700, "middle")
    return y + 58


def callout(s, x, y, text, tx, ty, anchor="end", size=T_CALL, col=NAVY):
    """লেবেল ও তার লিডার — লিডার কখনও নিজের লেখার উপর দিয়ে যায় না।"""
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    w = tw(text, size, 700)
    if anchor == "end":
        x1, x2 = x - w, x
    elif anchor == "middle":
        x1, x2 = x - w / 2, x + w / 2
    else:
        x1, x2 = x, x + w
    if tx > x2:
        p0 = (x2 + 10, y)
    elif tx < x1:
        p0 = (x1 - 10, y)
    else:                                   # লক্ষ্য লেখার নিচে বা উপরে
        p0 = (tx, y - size * 0.8 if ty < y else y + size * 0.7)
    s.path(f"M {p0[0]} {p0[1]} L {tx} {ty}", STEEL, 2.2)
    s.circle(tx, ty, 5, STEEL)


# ── circuit symbols ─────────────────────────────────────────────────────
def ac_source(s, cx, cy, r=40):
    """AC সোর্স — সাইন তরঙ্গ বৃত্তের ভেতরে, কেন্দ্র বরাবর প্রতিসম।"""
    s.circle(cx, cy, r, "#FFFFFF", SYM, SW)
    w = r * 0.60               # প্রতি অর্ধ-তরঙ্গের প্রস্থ
    a = r * 0.74               # কন্ট্রোল-পয়েন্ট; চূড়া বসে এর অর্ধেকে
    s.path(f"M {cx-w:.1f} {cy:.1f} q {w/2:.1f} {-a:.1f} {w:.1f} 0 "
           f"q {w/2:.1f} {a:.1f} {w:.1f} 0", SYM, SW)
    return r


def lamp(s, cx, cy, r=34, state="off", col=SYM):
    """বাতির প্রতীক — নিভন্ত, মৃদু বা পূর্ণ উজ্জ্বল।"""
    fill = {"off": "#FFFFFF", "dim": "#FFEDB3", "bright": "#FFC400"}[state]
    if state == "bright":
        # রশ্মি অনুভূমিক অক্ষ থেকে সরিয়ে রাখা — তার ওই পথেই বাতিতে ঢোকে
        for deg in (30, 60, 120, 150, 210, 240, 300, 330):
            a = math.radians(deg)
            s.line(cx + (r + 9) * math.cos(a), cy + (r + 9) * math.sin(a),
                   cx + (r + 22) * math.cos(a), cy + (r + 22) * math.sin(a),
                   "#F0A000", 4.2)
    s.circle(cx, cy, r, fill, col, SW)
    k = r * 0.70
    s.path(f"M {cx-k:.1f} {cy-k:.1f} L {cx+k:.1f} {cy+k:.1f}", col, SW)
    s.path(f"M {cx+k:.1f} {cy-k:.1f} L {cx-k:.1f} {cy+k:.1f}", col, SW)


def fuse_sym(s, cx, cy, w=104, h=40, col=LIVE):
    s.rect(cx - w / 2, cy - h / 2, w, h, "#FFFFFF", col, SW, 3)
    s.line(cx - w / 2, cy, cx + w / 2, cy, col, SW)


def socket_sym(s, cx, cy, r=36, col=SYM):
    s.circle(cx, cy, r, "#FFFFFF", col, SW)
    s.circle(cx, cy - 13, 7, col)
    s.circle(cx, cy + 13, 7, col)


def burst(s, cx, cy, r=34, col=RED):
    """শর্ট-সার্কিটের স্ফুলিঙ্গ।"""
    pts = []
    for i in range(12):
        a = math.radians(i * 30)
        rr = r if i % 2 == 0 else r * 0.44
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    s.poly(pts, "#FFD24A", col, 2.6)


# ── board module faces ──────────────────────────────────────────────────
def module_plate(s, cx, y, w=118, h=190):
    s.rect(cx - w / 2, y, w, h, PLATE, PLATE_E, 2.4, 12)


def face_fuse(s, cx, cy):
    """ক্যারিয়ারে বসানো কার্টিজ ফিউজ — দুই প্রান্তে ধাতব ক্যাপ, মাঝে এলিমেন্ট।"""
    s.rect(cx - 26, cy - 44, 52, 88, "#FFFFFF", "#9AA6B2", 2.2, 7)
    s.rect(cx - 22, cy - 15, 44, 30, "#FFF3C4", "#B08C00", 2, 4)
    for dx in (-22, 12):
        s.rect(cx + dx, cy - 15, 10, 30, METAL, "#6B7684", 1.6, 2)
    s.path(f"M {cx-12} {cy} L {cx+12} {cy}", "#8A6D00", 2.4)
    s.path(f"M {cx} {cy-44} L {cx} {cy-15}", "#B0BAC5", 2)
    s.path(f"M {cx} {cy+15} L {cx} {cy+44}", "#B0BAC5", 2)


def face_indicator(s, cx, cy):
    """নিয়ন ইন্ডিকেটর — বেজেলের মাঝে ছোট গোল লাল লেন্স।"""
    s.rect(cx - 26, cy - 44, 52, 88, "#FFFFFF", "#9AA6B2", 2.2, 7)
    s.circle(cx, cy, 19, "#F0F3F6", "#9AA6B2", 2)
    s.circle(cx, cy, 12, "#E8483A", "#9C2B20", 2)
    s.circle(cx - 4, cy - 4, 3.4, "#F9BDB6")


def face_switch(s, cx, cy, on=True):
    s.rect(cx - 26, cy - 44, 52, 88, "#FFFFFF", "#9AA6B2", 2.2, 7)
    s.rect(cx - 20, cy - 36, 40, 72, "#FAFBFC", "#C3CEDA", 1.6, 5)
    s.rect(cx - 6, cy - 30, 12, 20, RED if on else "#D8DEE5", "#B0BAC5", 1.4, 2)


def face_socket2(s, cx, cy):
    s.rect(cx - 28, cy - 44, 56, 88, "#FFFFFF", "#9AA6B2", 2.2, 7)
    for dy in (-18, 18):
        s.rect(cx - 13, cy + dy - 9, 26, 18, "#3B4550", "#20272E", 1.4, 5)


def face_holder(s, cx, cy):
    """ব্যাটেন হোল্ডারে বসানো টেস্ট বাতি।"""
    s.rect(cx - 30, cy + 12, 60, 30, "#FFFFFF", "#9AA6B2", 2.2, 6)
    s.rect(cx - 15, cy - 2, 30, 16, METAL, "#6B7684", 1.8, 3)
    for k in range(3):
        s.line(cx - 15, cy + 2 + k * 5, cx + 15, cy + 2 + k * 5, "#6B7684", 1.2)
    s.circle(cx, cy - 34, 30, GLASS, "#C79A1F", 2.4)
    s.path(f"M {cx-9} {cy-24} L {cx-4} {cy-38} L {cx+4} {cy-30} "
           f"L {cx+9} {cy-42}", "#B07C00", 2.4)


def plug2(s, cx, cy, scale=1.0):
    k = scale
    s.rect(cx - 46 * k, cy - 34 * k, 92 * k, 68 * k, "#FFFFFF", "#7C8794", 2.6, 9)
    for dx in (-19, 19):
        s.rect(cx + dx * k - 5 * k, cy - 78 * k, 10 * k, 44 * k,
               METAL, "#6B7684", 2, 3)


def _sheet(fname, title, left_img, right_img, note, h=560):
    """দুই প্যানেলের শিট — বাঁয়ে সার্কিট, ডানে কানেকশন ডায়াগ্রাম।"""
    s = SVG(1240, h)
    s.title(title, T_TITLE)
    PW = 560
    panel(s, 46, 96, PW, h - 230, "সার্কিট ডায়াগ্রাম", STEEL)
    panel(s, 634, 96, PW, h - 230, "কানেকশন ডায়াগ্রাম", GREEN)
    s.image_fit(46 + 14, 150, PW - 28, h - 306, f"{IMG}/{left_img}", 14)
    s.image_fit(634 + 14, 150, PW - 28, h - 306, f"{IMG}/{right_img}", 14)
    y = note_strip(s, h - 118, note)
    s.fit(y, 22)
    return s.save(f"{OUT}/{fname}.svg")


# ═══════════════════════════════════════════════════════════════════════
def d01_parts():
    """সিরিজ বোর্ডের গঠন ও অংশ পরিচিতি।"""
    s = SVG(1240, 760)
    s.title("সিরিজ বোর্ডের গঠন ও অংশ পরিচিতি", T_TITLE)

    BX, BY, BW, BH = 310, 250, 850, 262
    s.rect(BX, BY, BW, BH, "#E7ECF1", "#7C8794", 3, 18)
    s.rect(BX + 14, BY + 14, BW - 28, BH - 28, "#F7FAFC", "#B0BAC5", 1.8, 12)

    mods = [("ফিউজ", face_fuse), ("ইন্ডিকেটর", face_indicator),
            ("সুইচ", face_switch), ("টেস্ট বাতি", face_holder),
            ("২-পিন সকেট", face_socket2)]
    step = (BW - 80) / len(mods)
    cy = BY + BH / 2
    for i, (name, draw) in enumerate(mods):
        cx = BX + 40 + step * (i + 0.5)
        module_plate(s, cx, BY + 38, 118, BH - 76)
        draw(s, cx, cy)
        ly = 148 if i % 2 == 0 else 204
        s.text(cx, ly, name, T_CALL, NAVY, 700, "middle")
        s.path(f"M {cx} {ly+10} L {cx} {BY+32}", STEEL, 2.2)
        s.circle(cx, BY + 32, 5, STEEL)

    # দেয়াল-সকেটে যাওয়া ২-পিন প্লাগ ও ফ্লেক্সিবল কর্ড
    s.path(f"M {BX} {cy} C 268 {cy} 240 400 214 428", "#3B4550", 9, "none")
    plug2(s, 172, 428, 0.9)

    callout(s, 172, 540, "২-পিন প্লাগ", 172, 462, "middle")
    callout(s, 330, 604, "ফ্লেক্সিবল কর্ড", 256, 412, "middle")
    callout(s, 760, 604, "বোর্ড বডি (অগ্নিরোধী PVC)", 760, BY + BH, "middle")

    y = note_strip(s, 654,
                   "ফিউজ, সুইচ, টেস্ট বাতি ও সকেট — সবই একই লাইনে সিরিজে; "
                   "কেবল ইন্ডিকেটর বাতি ফেজ ও নিউট্রালের মাঝে প্যারালালে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_parts.svg")


def d02_why():
    """সিরিজ বোর্ড কেন প্রয়োজন — সরাসরি সরবরাহ বনাম সিরিজ বোর্ড।"""
    s = SVG(1240, 620)
    s.title("সিরিজ বোর্ডের প্রয়োজনীয়তা", T_TITLE)
    PW = 560
    panel(s, 46, 96, PW, 420, "সরাসরি সরবরাহ দিলে", RED)
    panel(s, 634, 96, PW, 420, "সিরিজ বোর্ডের মাধ্যমে দিলে", GREEN)

    for k, PX in enumerate((46, 634)):
        L, R, TOP, BOT = PX + 96, PX + 430, 210, 356
        scy = 283
        ac_source(s, L, scy, 38)
        s.path(f"M {L} {TOP} L {L} {scy-38}", LIVE, SW)
        s.path(f"M {L} {scy+38} L {L} {BOT}", NEUT, SW)
        s.path(f"M {L} {BOT} L {R} {BOT}", NEUT, SW)
        s.text(L, 400, "AC সরবরাহ", T_SMALL, GREY, 600, "middle")

        # ডান পাশের উল্লম্ব তারে পরীক্ষাধীন সার্কিট
        bw, bh = 172, 88
        s.rect(R - bw / 2, scy - bh / 2, bw, bh, "#FFFFFF", NAVY, 2.6, 10)
        s.path(f"M {R} {TOP} L {R} {scy-bh/2}", LIVE, SW)
        s.path(f"M {R} {scy+bh/2} L {R} {BOT}", NEUT, SW)
        s.text(R, scy - 6, "ত্রুটিপূর্ণ", T_SMALL, NAVY, 700, "middle")
        s.text(R, scy + 22, "সার্কিট (শর্ট)", T_SMALL, NAVY, 700, "middle")

        if k == 0:
            s.path(f"M {L} {TOP} L {R} {TOP}", LIVE, SW)
            burst(s, PX + 262, TOP, 32)
            s.text(PX + 228, 296, "বড় শর্ট-সার্কিট", T_SMALL, RED, 700, "middle")
            s.text(PX + 228, 324, "কারেন্ট বয়ে যায়", T_SMALL, RED, 700, "middle")
        else:
            lamp(s, PX + 262, TOP, 34, "bright")
            s.path(f"M {L} {TOP} L {PX+262-36} {TOP}", LIVE, SW)
            s.path(f"M {PX+262+36} {TOP} L {R} {TOP}", LIVE, SW)
            s.text(PX + 228, 296, "সিরিজে বসানো", T_SMALL, GREEN, 700, "middle")
            s.text(PX + 228, 324, "টেস্ট বাতি", T_SMALL, GREEN, 700, "middle")

    for PX, col, bg, t1, t2 in (
            (46, RED, REDBG,
             "ফিউজ উড়ে যায়, তার ও যন্ত্র পুড়ে যায়",
             "স্ফুলিঙ্গ ও অগ্নিকাণ্ডের ঝুঁকি থাকে"),
            (634, GREEN, GREENBG,
             "বাতি পূর্ণ উজ্জ্বল জ্বলে — ত্রুটি ধরা পড়ে",
             "বাতিই কারেন্ট সীমিত রাখে, কিছুই নষ্ট হয় না")):
        s.rect(PX + 20, 424, PW - 40, 78, bg, col, 2, 11)
        s.text(PX + PW / 2, 456, t1, T_SMALL, col, 700, "middle")
        s.text(PX + PW / 2, 486, t2, T_SMALL, "#39434D", 400, "middle")

    y = note_strip(s, 534,
                   "নতুন বা মেরামত করা যেকোনো সার্কিট সরাসরি লাইনে না দিয়ে "
                   "আগে সিরিজ বোর্ডে পরীক্ষা করে নেওয়াই নিয়ম")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_why.svg")


def d03_circuit():
    return _sheet("d03_circuit", "সিরিজ বোর্ডের সার্কিট ও কানেকশন ডায়াগ্রাম",
                  "d03_sb_schem.png", "d03_sb_conn.png",
                  "ফিউজ → সুইচ → টেস্ট বাতি → সকেট সবই সিরিজে; "
                  "ইন্ডিকেটর বাতি ফেজ ও নিউট্রালের মাঝে প্যারালালে", 620)


def d04_states():
    """সকেটে যন্ত্র লাগানোর পর টেস্ট বাতির তিন অবস্থা ও তার অর্থ।"""
    s = SVG(1240, 648)
    s.title("টেস্ট বাতির তিন অবস্থা ও তার অর্থ", T_TITLE)

    PW, GAP = 365, 26
    x0 = 46
    cases = [
        ("বাতি একেবারে জ্বলে না", "off", RED, REDBG,
         "ওপেন সার্কিট", "সংযোগ ছিঁড়েছে, ফিউজ কাটা বা সুইচ বন্ধ"),
        ("বাতি মৃদু আলোয় জ্বলে", "dim", GREEN, GREENBG,
         "সার্কিট ঠিক আছে", "যন্ত্র স্বাভাবিক কারেন্ট নিচ্ছে"),
        ("বাতি পূর্ণ উজ্জ্বল জ্বলে", "bright", RED, REDBG,
         "শর্ট সার্কিট", "ফেজ ও নিউট্রাল কোথাও লেগে গেছে"),
    ]
    TOP, SCY, BOT = 214, 280, 350
    for i, (head, state, col, bg, verdict, why) in enumerate(cases):
        PX = x0 + i * (PW + GAP)
        panel(s, PX, 96, PW, 434, head, col)

        L, R = PX + 62, PX + 262
        lx, lr = PX + 152, 27
        bw, bh = 112, 86
        ty, by = SCY - bh / 2, SCY + bh / 2

        # সরবরাহ ও লুপ
        ac_source(s, L, SCY, 26)
        s.path(f"M {L} {TOP} L {L} {SCY-26}", LIVE, SW)
        s.path(f"M {L} {SCY+26} L {L} {BOT}", NEUT, SW)
        s.path(f"M {L} {BOT} L {R} {BOT}", NEUT, SW)

        # টেস্ট বাতি ফেজ তারে সিরিজে
        lamp(s, lx, TOP, lr, state)
        s.path(f"M {L} {TOP} L {lx-lr-2} {TOP}", LIVE, SW)
        s.path(f"M {lx+lr+2} {TOP} L {R} {TOP}", LIVE, SW)

        # পরীক্ষাধীন যন্ত্র — ভেতরের প্রতীকই অবস্থাটা বলে
        s.rect(R - bw / 2, ty, bw, bh, "#FFFFFF", NAVY, 2.4, 10)
        s.path(f"M {R} {TOP} L {R} {ty}", LIVE, SW)
        s.path(f"M {R} {by} L {R} {BOT}", NEUT, SW)
        if state == "off":
            s.path(f"M {R} {ty} L {R} {SCY-16}", LIVE, SW)
            s.path(f"M {R} {SCY+16} L {R} {by}", NEUT, SW)
            s.circle(R, SCY - 16, 5.5, RED)
            s.circle(R, SCY + 16, 5.5, RED)
        else:
            s.path(f"M {R} {ty} L {R} {SCY-22}", LIVE, SW)
            s.path(f"M {R} {SCY+22} L {R} {by}", NEUT, SW)
            s.rect(R - 16, SCY - 22, 32, 44, "#FFFFFF", NAVY, 2.8, 3)
            if state == "bright":
                bx, y1, y2 = R + 34, ty + 13, by - 13
                s.path(f"M {R} {y1} L {bx} {y1} L {bx} {y2} L {R} {y2}",
                       LIVE, SW + 0.8, "none")
                s.circle(R, y1, 5.5, LIVE)
                s.circle(R, y2, 5.5, LIVE)

        s.text(PX + 24, 386, "AC সরবরাহ", T_SMALL, GREY, 600, "start")
        s.text(PX + PW - 24, 386, "পরীক্ষাধীন যন্ত্র", T_SMALL, GREY, 600,
               "end")

        # রায়ের ঘর
        s.rect(PX + 18, 402, PW - 36, 116, bg, col, 2, 11)
        lines = wrap(why, PW - 44, T_SMALL, 400)
        vy = 442 if len(lines) == 1 else 434
        s.text(PX + PW / 2, vy, verdict, T_NAME, col, 700, "middle")
        for j, ln in enumerate(lines):
            s.text(PX + PW / 2, vy + 34 + j * 30, ln, T_SMALL,
                   "#39434D", 400, "middle")

    y = note_strip(s, 564,
                   "টেস্ট বাতির ক্ষমতা লোডের চেয়ে কম হলে বাতি বেশি জ্বলে — "
                   "তাই পরীক্ষার আগে উপযুক্ত ওয়াটের বাতি বেছে নিতে হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_states.svg")


def d05_steps():
    """সিরিজ বোর্ড দিয়ে পরীক্ষার ছয়টি ধাপ।"""
    s = SVG(1240, 620)
    s.title("সিরিজ বোর্ড দিয়ে সার্কিট পরীক্ষার ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)

    steps = [
        ("বোর্ড পরীক্ষা", "ফিউজ, বাতি ও সকেট ঠিক আছে কি না দেখে নাও"),
        ("সরবরাহ বন্ধ রাখো", "পরীক্ষাধীন সার্কিটের সুইচ অফ রাখো"),
        ("সংযোগ দাও", "পরীক্ষাধীন সার্কিটের প্লাগ বোর্ডের সকেটে লাগাও"),
        ("বোর্ডে সরবরাহ দাও", "বোর্ডের প্লাগ দেয়াল-সকেটে লাগাও"),
        ("ইন্ডিকেটর দেখো", "ইন্ডিকেটর জ্বললে বোর্ডে সরবরাহ এসেছে"),
        ("বাতি লক্ষ করো", "উজ্জ্বলতা দেখে সার্কিটের অবস্থা সিদ্ধান্ত নাও"),
    ]
    BW, BH, GX, GY = 356, 168, 30, 34
    x0 = (1240 - (3 * BW + 2 * GX)) / 2
    for i, (t, d) in enumerate(steps):
        x = x0 + (i % 3) * (BW + GX)
        y = 130 + (i // 3) * (BH + GY)
        s.rect(x, y, BW, BH, "#F5F9FC", STEEL, 2, 13)
        s.circle(x + 44, y + 42, 26, NAVY)
        s.text(x + 44, y + 52, ["১", "২", "৩", "৪", "৫", "৬"][i], T_NODE,
               "#FFFFFF", 700, "middle")
        s.text(x + 84, y + 52, t, T_NAME, NAVY, 700)
        for j, ln in enumerate(wrap(d, BW - 60, T_SMALL, 400)):
            s.text(x + 30, y + 100 + j * T_SMALL * 1.36, ln, T_SMALL,
                   "#39434D", 400)
        if i % 3 < 2:
            s.path(f"M {x+BW+4} {y+BH/2} L {x+BW+GX-8} {y+BH/2}", STEEL, 2.8,
                   marker=ar)
    # প্রথম সারি থেকে দ্বিতীয় সারিতে
    ry = 130 + BH
    s.path(f"M {x0+2*(BW+GX)+BW/2} {ry+6} L {x0+2*(BW+GX)+BW/2} {ry+GY/2} "
           f"L {x0+BW/2} {ry+GY/2} L {x0+BW/2} {ry+GY-6}", STEEL, 2.8, marker=ar)

    y = note_strip(s, 130 + 2 * BH + GY + 30,
                   "পরীক্ষার সময় খালি হাতে সার্কিটের কোনো অংশ স্পর্শ করা যাবে না — "
                   "বাতি নিভন্ত থাকলেও তারে ফেজ থাকতে পারে",
                   fill=REDBG, stroke=RED, tcolor="#7A1810")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_steps.svg")


def d06_socket():
    """সিরিজ বোর্ডের সকেট অংশের কানেকশন ডায়াগ্রাম।"""
    s = SVG(1240, 800)
    s.title("ফিউজ ও সুইচসহ ২-পিন সকেটের কানেকশন ডায়াগ্রাম", T_TITLE)
    panel(s, 46, 96, 1148, 568, "কানেকশন ডায়াগ্রাম", GREEN)
    s.image_fit(70, 158, 1100, 488, f"{IMG}/d06_socket_conn.png", 8)
    y = note_strip(s, 692,
                   "ফেজ তার ফিউজ ও সুইচ হয়ে সকেটে যায়, নিউট্রাল তার সরাসরি — "
                   "সিরিজ বোর্ডে এই সকেটেই পরীক্ষাধীন যন্ত্রের প্লাগ লাগে")
    s.fit(y, 24)
    return s.save(f"{OUT}/d06_socket.svg")


ALL = [d01_parts, d02_why, d03_circuit, d04_states, d05_steps, d06_socket]

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
