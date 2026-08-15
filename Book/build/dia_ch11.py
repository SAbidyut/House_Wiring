# -*- coding: utf-8 -*-
"""অধ্যায় ১১ — জয়েন্ট, স্প্লাইস ও সোল্ডারিং : ডায়াগ্রাম।

জয়েন্টের ছবিগুলো হাতে আঁকা হয়নি — John M. Sharp, *Practical Electric
Wiring* (D. Appleton & Co., New York, ১৯১৬), অধ্যায় ২ 'Wire Joints and
Splices'-এর মূল প্লেট থেকে ৪০০ dpi-তে ক্রপ করে বসানো হয়েছে (পাবলিক
ডোমেইন)।  সোল্ডারিং আয়রন ও আধুনিক কানেক্টরের আলোকচিত্র উইকিমিডিয়া
কমন্স থেকে (CC লাইসেন্স)।  বিস্তারিত `assets/ch11/credits.json`-এ।

কেবল ধাপ, শ্রেণিবিভাগ ও টেপিংয়ের চিত্র নতুন করে আঁকা — এগুলোর কোনো
সোর্স-ছবি নেই।
"""
import os
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "ch11")
IMG = os.path.join(HERE, "assets", "ch11")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
T_CALL = 25
LH = 1.42

COPPER = "#C07A32"
COPPER_D = "#8A5220"
INSUL = "#2F3B47"
TAPE = "#1F2933"
TAPE_L = "#3D4A57"


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
    """লেবেল ও তার লিডার লাইন — লেখা সবসময় ছবির বাইরে থাকে।"""
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    x0 = x + 10 if anchor == "end" else x - 10
    s.path(f"M {x0} {y} L {tx} {ty}", STEEL, 2.2)
    s.circle(tx, ty, 5, STEEL)


def img_panel(s, x, y, w, h, title, img, col=STEEL, cap=None):
    """শিরোনামসহ প্যানেলের ভেতরে সোর্স-ছবি বসানো।"""
    panel(s, x, y, w, h, title, col)
    top = y + 64
    bot = y + h - (40 if cap else 14)
    s.image_fit(x + 16, top, w - 32, bot - top, img, 6)
    if cap:
        s.text(x + w / 2, y + h - 16, cap, T_SMALL, GREY, 400, "middle")


def two_panel(fname, title, left, right, note, h=600, pw=560,
              lcol=STEEL, rcol=GREEN):
    """বাঁয়ে-ডানে দুই ছবির শিট।  left/right = (শিরোনাম, ছবি, ক্যাপশন)।"""
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


def step_cards(s, steps, x0, y0, bw, bh, gx, gy, per_row, ar):
    """নম্বরযুক্ত ধাপের কার্ড — তিনটি করে সারিতে, তীরসহ।"""
    dig = ["১", "২", "৩", "৪", "৫", "৬", "৭", "৮"]
    for i, (t, d) in enumerate(steps):
        r, c = divmod(i, per_row)
        x = x0 + c * (bw + gx)
        y = y0 + r * (bh + gy)
        s.rect(x, y, bw, bh, "#F5F9FC", STEEL, 2, 13)
        s.circle(x + 44, y + 42, 26, NAVY)
        s.text(x + 44, y + 52, dig[i], T_NODE, "#FFFFFF", 700, "middle")
        s.text(x + 84, y + 52, t, T_NAME, NAVY, 700)
        for j, ln in enumerate(wrap(d, bw - 58, T_SMALL, 400)):
            s.text(x + 30, y + 100 + j * T_SMALL * 1.36, ln, T_SMALL,
                   "#39434D", 400)
        if c < per_row - 1 and i < len(steps) - 1:
            s.path(f"M {x+bw+4} {y+bh/2} L {x+bw+gx-8} {y+bh/2}", STEEL, 2.8,
                   marker=ar)
    return y0 + ((len(steps) - 1) // per_row + 1) * bh + \
        ((len(steps) - 1) // per_row) * gy


# ═══════════════════════════════════════════════════════════════════════
def d01_steps():
    """একটি আদর্শ জয়েন্টের পাঁচটি ধাপ।"""
    s = SVG(1240, 640)
    s.title("আদর্শ জয়েন্ট তৈরির পাঁচটি ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)
    steps = [
        ("স্কিনিং", "ছুরি বা স্ট্রিপার দিয়ে তারের ইনসুলেশন তুলে ফেলা"),
        ("স্ক্র্যাপিং", "খেই থেকে অক্সাইড ও ময়লা চেঁছে তামা ঝকঝকে করা"),
        ("টাইয়িং", "নিয়ম মেনে দুই তার পাকিয়ে জয়েন্ট বাঁধা"),
        ("সোল্ডারিং", "গলিত সোল্ডার ঢুকিয়ে জয়েন্ট স্থায়ী করা"),
        ("টেপিং", "ইনসুলেশন টেপ পেঁচিয়ে জয়েন্ট ঢেকে দেওয়া"),
    ]
    BW, BH, GX, GY = 356, 170, 30, 34
    x0 = (1240 - (3 * BW + 2 * GX)) / 2
    bottom = step_cards(s, steps, x0, 130, BW, BH, GX, GY, 3, ar)
    # প্রথম সারি থেকে দ্বিতীয় সারিতে
    ry = 130 + BH
    s.path(f"M {x0+2*(BW+GX)+BW/2} {ry+6} L {x0+2*(BW+GX)+BW/2} {ry+GY/2} "
           f"L {x0+BW/2} {ry+GY/2} L {x0+BW/2} {ry+GY-6}", STEEL, 2.8,
           marker=ar)
    y = note_strip(s, bottom + 30,
                   "পাঁচটি ধাপের একটিও বাদ দেওয়া চলবে না — স্ক্র্যাপিং ছাড়া "
                   "সোল্ডার ধরে না, আর টেপিং ছাড়া জয়েন্ট বিপজ্জনক")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_steps.svg")


def d02_skinning():
    """স্কিনিংয়ের সঠিক ও ভুল পদ্ধতি (Sharp ১৯১৬, চিত্র ১)।"""
    s = SVG(1240, 520)
    s.title("স্কিনিং — ছুরি ধরার সঠিক ও ভুল কোণ", T_TITLE)
    PW, PH = 560, 290
    img_panel(s, 46, 96, PW, PH, "সঠিক — পেনসিল ছোলার মতো",
              f"{IMG}/f01a_skin_ok.png", GREEN)
    img_panel(s, 634, 96, PW, PH, "ভুল — তারের সঙ্গে সমকোণে",
              f"{IMG}/f01b_skin_bad.png", RED)
    for px, col, bg, t in ((46, GREEN, GREENBG,
                            "ব্লেড ইনসুলেশনের গায়ে হেলিয়ে চালালে খেই কাটে না"),
                           (634, RED, REDBG,
                            "সমকোণে চাপ দিলে তামায় খাঁজ পড়ে, পরে ভেঙে যায়")):
        s.rect(px + 18, 96 + PH + 16, PW - 36, 62, bg, col, 2, 11)
        s.text(px + PW / 2, 96 + PH + 56, t, T_SMALL, col, 700, "middle")
    y = note_strip(s, 96 + PH + 96,
                   "ইনসুলেশন যতটুকু তোলা হবে, তার পুরোটাই জয়েন্টের ভেতরে "
                   "ঢুকবে — বাইরে খালি তামা থাকলে চলবে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_skinning.svg")


def d03_types():
    """জয়েন্টের শ্রেণিবিভাগ।"""
    s = SVG(1240, 700)
    s.title("বৈদ্যুতিক তারের জয়েন্টের শ্রেণিবিভাগ", T_TITLE)

    RW, RH = 380, 70
    rx = (1240 - RW) / 2
    s.rect(rx, 104, RW, RH, NAVY, NAVY, 2, 12)
    s.text(1240 / 2, 104 + 46, "তারের জয়েন্ট ও স্প্লাইস", T_NAME,
           "#FFFFFF", 700, "middle")

    groups = [
        ("সোজা বা স্ট্রেইট জয়েন্ট", STEEL,
         ["ওয়েস্টার্ন ইউনিয়ন জয়েন্ট", "ব্রিটানিয়া জয়েন্ট",
          "ম্যারিড বা টেপার জয়েন্ট", "স্লিভ জয়েন্ট"]),
        ("শাখা বা ট্যাপ জয়েন্ট", GREEN,
         ["টি বা ট্যাপ জয়েন্ট", "ক্রস জয়েন্ট", "নটেড ট্যাপ জয়েন্ট",
          "বহু-খেই তারের টি জয়েন্ট"]),
        ("প্রান্তিক বা টার্মিনাল জয়েন্ট", AMBER,
         ["পিগটেল বা র‍্যাট-টেইল জয়েন্ট", "ফিক্সচার জয়েন্ট",
          "লাগ বা সকেট সংযোগ", "কানেক্টর ও কাপলার"]),
    ]
    GW, GAP = 365, 26
    gx0 = 46
    ytop = 230
    s.path(f"M 620 {104+RH} L 620 {ytop-34}", STEEL, 2.6)
    for i, (name, col, items) in enumerate(groups):
        x = gx0 + i * (GW + GAP)
        cx = x + GW / 2
        s.path(f"M {cx} {ytop-34} L {cx} {ytop}", STEEL, 2.6)
        if i != 1:
            s.path(f"M {min(cx,620)} {ytop-34} L {max(cx,620)} {ytop-34}",
                   STEEL, 2.6)
        s.rect(x, ytop, GW, 64, col, col, 2, 11)
        for j, ln in enumerate(wrap(name, GW - 40, T_BODY, 700)):
            s.text(cx, ytop + (40 if len(wrap(name, GW - 40, T_BODY, 700)) == 1
                               else 28 + j * T_BODY * 1.34),
                   ln, T_BODY, "#FFFFFF", 700, "middle")
        by = ytop + 76
        s.rect(x, by, GW, 232, "#F7FAFC", LINE, 1.8, 11)
        yy = by + 42
        for it in items:
            s.circle(x + 30, yy - 7, 6, col)
            for k, ln in enumerate(wrap(it, GW - 66, T_SMALL, 400)):
                s.text(x + 50, yy + k * T_SMALL * 1.3, ln, T_SMALL,
                       "#28323C", 400)
            yy += 52 if len(wrap(it, GW - 66, T_SMALL, 400)) == 1 else 78
    y = note_strip(s, ytop + 76 + 232 + 28,
                   "একক খেইয়ের (solid) তারে যে জয়েন্ট চলে, বহু খেইয়ের "
                   "(stranded) তারে তা হুবহু চলে না — খেই আলাদা করে মেলাতে হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_types.svg")


def d04_wu():
    """ওয়েস্টার্ন ইউনিয়ন জয়েন্টের চার ধাপ (Sharp ১৯১৬, চিত্র ২)।"""
    s = SVG(1240, 860)
    s.title("ওয়েস্টার্ন ইউনিয়ন জয়েন্ট তৈরির ধাপ", T_TITLE)
    PW, PH = 520, 660
    img_panel(s, 46, 96, PW, PH, "মূল চিত্র (A → D)",
              f"{IMG}/f02_wu_steps.png", STEEL)

    x = 634
    panel(s, x, 96, 560, PH, "ধাপে ধাপে বর্ণনা", GREEN)
    rows = [
        ("A", "দুই তারের ইনসুলেশন প্রায় ৭৫ মিমি তুলে খেই পরিষ্কার করে "
              "তার দুটি আড়াআড়ি রাখো।"),
        ("B", "ক্রসিংয়ের নিচের অংশ হাতে ধরে উপরের অংশ নিজের দিকে টেনে "
              "দুই-তিন প্যাঁচ দাও।"),
        ("C", "প্লায়ার্স দিয়ে প্যাঁচ ধরে রেখে একটি প্রান্ত অন্য তারের গায়ে "
              "অন্তত পাঁচ পাক শক্ত করে জড়াও।"),
        ("D", "অন্য প্রান্তটিও একইভাবে জড়িয়ে বাড়তি তার কেটে ফেলো — "
              "প্রান্ত যেন খোঁচা হয়ে না থাকে।"),
    ]
    yy = 176
    for tag, desc in rows:
        s.circle(x + 52, yy + 6, 26, GREEN)
        s.text(x + 52, yy + 16, tag, T_NODE, "#FFFFFF", 700, "middle")
        lines = wrap(desc, 560 - 130, T_BODY, 400)
        for k, ln in enumerate(lines):
            s.text(x + 92, yy + 14 + k * T_BODY * LH, ln, T_BODY, "#28323C")
        yy += max(96, 46 + len(lines) * T_BODY * LH)
    y = note_strip(s, 96 + PH + 22,
                   "সবচেয়ে বেশি ব্যবহৃত সোজা জয়েন্ট — একক খেইয়ের তারে "
                   "দৈর্ঘ্য বাড়াতে এটিই নিয়ম")
    s.fit(y, 24)
    return s.save(f"{OUT}/d04_wu.svg")


def d05_wu_ties():
    """শর্ট টাই ও লং টাই (Sharp ১৯১৬, চিত্র ৩)।"""
    s = SVG(1240, 470)
    s.title("ওয়েস্টার্ন ইউনিয়ন জয়েন্টের দুই ধরন", T_TITLE)
    panel(s, 46, 96, 1148, 250, "A — লং টাই · B — শর্ট টাই", STEEL)
    s.image_fit(90, 160, 1060, 172, f"{IMG}/f03_wu_ties.png", 6)
    y = note_strip(s, 368,
                   "মাঝের পাকের দৈর্ঘ্যই দুটির পার্থক্য — লং টাইয়ে সোল্ডার "
                   "ভেতরে ভালো ঢোকে, শর্ট টাই জায়গা কম নেয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d05_wu_ties.svg")


def d06_pigtail():
    """পিগটেল বা র‍্যাট-টেইল জয়েন্ট (Sharp ১৯১৬, চিত্র ৫)।"""
    return two_panel(
        "d06_pigtail", "পিগটেল বা র‍্যাট-টেইল জয়েন্ট",
        ("আউটলেট বক্সে তার মেলানো", "f05a_rattail.png"),
        ("সম্পূর্ণ জয়েন্ট", "f05b_rattail.png"),
        "জংশন বা আউটলেট বক্সের ভেতরে ব্যবহার হয় — টান পড়ে এমন জায়গায় নয়",
        h=560)


def d07_tee():
    """টি বা ট্যাপ জয়েন্ট (Sharp ১৯১৬, চিত্র ৪ ও ৯)।"""
    return two_panel(
        "d07_tee", "টি বা ট্যাপ জয়েন্ট",
        ("একক খেইয়ের তারে — সাধারণ ও নটেড", "f04a_tee.png"),
        ("বহু খেইয়ের তারে (সম্পূর্ণ)", "f09b_tee_str.png"),
        "মূল লাইন না কেটে তা থেকে শাখা নেওয়ার জয়েন্ট — নট দিলে টানে খুলে যায় না",
        h=580)


def d08_cross():
    """ক্রস জয়েন্ট (Sharp ১৯১৬, চিত্র ৪ C ও D)।"""
    return two_panel(
        "d08_cross", "ক্রস বা প্লেইন ট্যাপ জয়েন্ট",
        ("দুই দিকে শাখা — সাধারণ ক্রস", "f04c_cross1.png"),
        ("নট দেওয়া ক্রস জয়েন্ট", "f04d_cross2.png"),
        "একই বিন্দু থেকে দুই দিকে শাখা নিতে হলে ক্রস জয়েন্ট ব্যবহার হয়",
        h=600)


def d09_britannia():
    """ব্রিটানিয়া জয়েন্ট (Sharp ১৯১৬, চিত্র ৭)।"""
    return two_panel(
        "d09_britannia", "ব্রিটানিয়া জয়েন্ট",
        ("প্রান্ত সমকোণে ভাঁজ করে পাশাপাশি", "f07a_britannia.png"),
        ("সরু তার দিয়ে জড়িয়ে সম্পূর্ণ", "f07b_britannia.png"),
        "মোটা একক খেইয়ের তার পাকানো যায় না বলে দুই তার পাশাপাশি রেখে সরু "
        "বাঁধন-তার দিয়ে জড়িয়ে বাঁধা হয়",
        h=420)


def d10_married():
    """ম্যারিড বা টেপার কেবল স্প্লাইস (Sharp ১৯১৬, চিত্র ৮)।"""
    return two_panel(
        "d10_married", "ম্যারিড জয়েন্ট — বহু খেইয়ের তারের স্প্লাইস",
        ("A, B — খেই ছড়িয়ে পরস্পরে গাঁথা", "f08a_married.png"),
        ("C, D — খেই জড়িয়ে সম্পূর্ণ করা", "f08b_married.png"),
        "প্রতিটি খেই আলাদা করে ছড়িয়ে, চিরুনির দাঁতের মতো গেঁথে তবেই জড়াতে হয়",
        h=620)


def d11_fixture():
    """ফিক্সচার জয়েন্ট ও স্তম্ভিত জয়েন্ট (Sharp ১৯১৬, চিত্র ৬ ও ১০)।"""
    s = SVG(1240, 700)
    s.title("ফিক্সচার জয়েন্ট ও স্তম্ভিত (staggered) জয়েন্ট", T_TITLE)
    PW = 365
    img_panel(s, 46, 96, PW, 440, "সরু তার মোটা তারে জড়ানো",
              f"{IMG}/f06a_fixture.png", STEEL)
    img_panel(s, 46 + PW + 26, 96, PW, 440, "মোটা তারের প্রান্ত ভাঁজ করা",
              f"{IMG}/f06b_fixture.png", STEEL)
    img_panel(s, 46 + 2 * (PW + 26), 96, PW, 440,
              "দুই তারের জয়েন্ট আগে-পিছে", f"{IMG}/f10_duplex.png", GREEN)
    y = note_strip(s, 560,
                   "ঝাড়বাতির সরু তার মোটা তারে জোড়ার সময় ফিক্সচার জয়েন্ট; "
                   "যমজ তারের দুই জয়েন্ট কখনো মুখোমুখি রাখা যাবে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d11_fixture.svg")


def d12_solder_tools():
    """সোল্ডারিংয়ের সরঞ্জাম পরিচিতি।"""
    s = SVG(1240, 780)
    s.title("সোল্ডারিং আয়রন ও সোল্ডার তার", T_TITLE)
    IX, IY, IW = 150, 230, 940
    IH = IW * 639 / 1600
    s.rect(IX - 12, IY - 12, IW + 24, IH + 24, "#FCFDFE", LINE, 1.8, 12)
    s.image(IX, IY, IW, IH, f"{IMG}/ph_solder_iron.jpg", 6)

    callout(s, 300, 176, "সোল্ডার তারের রোল", IX + 0.16 * IW,
            IY + 0.52 * IH, "middle")
    callout(s, 760, 176, "হ্যান্ডল", IX + 0.60 * IW, IY + 0.33 * IH, "middle")
    callout(s, 1092, 176, "সাপ্লাই কর্ড ও প্লাগ", IX + 0.86 * IW,
            IY + 0.12 * IH, "end")
    callout(s, 300, IY + IH + 62, "বিট বা টিপ", IX + 0.21 * IW,
            IY + 0.92 * IH, "middle")
    callout(s, 760, IY + IH + 62, "হিটিং এলিমেন্টসহ ব্যারেল",
            IX + 0.345 * IW, IY + 0.705 * IH, "middle")

    y = note_strip(s, IY + IH + 108,
                   "ঘরোয়া ওয়্যারিংয়ের জয়েন্টে সাধারণত ৬০–১০০ ওয়াটের আয়রন "
                   "এবং রজন-কোর সোল্ডার তার ব্যবহার করা হয়")
    s.fit(y, 24)
    return s.save(f"{OUT}/d12_solder_tools.svg")


def d13_solder_steps():
    """সোল্ডারিংয়ের ধাপ।"""
    s = SVG(1240, 660)
    s.title("সোল্ডারিং করার ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)
    steps = [
        ("জয়েন্ট পরিষ্কার", "তেল, ময়লা ও অক্সাইড তুলে তামা ঝকঝকে করো"),
        ("ফ্লাক্স লাগানো", "জয়েন্টে রজন বা সোল্ডারিং পেস্ট মাখাও"),
        ("আয়রন গরম", "বিট গরম হয়ে সোল্ডার সহজে গলা পর্যন্ত অপেক্ষা করো"),
        ("বিট টিনিং", "গরম বিটে সামান্য সোল্ডার ধরিয়ে চকচকে আবরণ দাও"),
        ("সোল্ডার প্রয়োগ", "বিট জয়েন্টে চেপে ধরে সোল্ডার জয়েন্টে গলাও"),
        ("ঠান্ডা করা", "নড়াচড়া না করে ঠান্ডা হতে দাও, তারপর টেপ লাগাও"),
    ]
    BW, BH, GX, GY = 356, 168, 30, 34
    x0 = (1240 - (3 * BW + 2 * GX)) / 2
    bottom = step_cards(s, steps, x0, 130, BW, BH, GX, GY, 3, ar)
    ry = 130 + BH
    s.path(f"M {x0+2*(BW+GX)+BW/2} {ry+6} L {x0+2*(BW+GX)+BW/2} {ry+GY/2} "
           f"L {x0+BW/2} {ry+GY/2} L {x0+BW/2} {ry+GY-6}", STEEL, 2.8,
           marker=ar)
    y = note_strip(s, bottom + 30,
                   "সোল্ডার গলবে জয়েন্টের তাপে — বিটের গায়ে গলিয়ে ফোঁটা "
                   "ফেলে দিলে ভেতরে ঢোকে না, ঠান্ডা জোড়া (dry joint) হয়",
                   fill=AMBERBG, stroke=AMBER, tcolor="#7A5200")
    s.fit(y, 24)
    return s.save(f"{OUT}/d13_solder_steps.svg")


# ── টেপিং ছবির উপাদান ───────────────────────────────────────────────────
def _wire(s, x0, x1, cy, ins_l, ins_r):
    """তামার তার, দুই প্রান্তে ইনসুলেশন।"""
    s.line(x0, cy, x1, cy, COPPER, 11)
    s.rect(x0, cy - 11, ins_l - x0, 22, INSUL, "#111820", 1.6, 5)
    s.rect(ins_r, cy - 11, x1 - ins_r, 22, INSUL, "#111820", 1.6, 5)


def _twist(s, cx, cy, w=120):
    """জয়েন্টের পাকানো অংশ।"""
    n = 7
    step = w / n
    for i in range(n):
        x = cx - w / 2 + i * step
        s.path(f"M {x:.1f} {cy+11:.1f} Q {x+step*0.5:.1f} {cy-16:.1f} "
               f"{x+step:.1f} {cy+11:.1f}", COPPER_D, 5)
        s.path(f"M {x:.1f} {cy-11:.1f} Q {x+step*0.5:.1f} {cy+16:.1f} "
               f"{x+step:.1f} {cy-11:.1f}", COPPER, 5)


def _tape(s, x0, x1, cy, half=True):
    """হাফ-ল্যাপ টেপ — প্রতিটি পাক আগেরটির অর্ধেক ঢাকে।"""
    band, step = 30, 15 if half else 30
    x = x0
    i = 0
    while x < x1:
        w = min(band, x1 - x)
        s.poly([(x, cy + 20), (x + w, cy + 20 - 10),
                (x + w, cy - 20), (x, cy - 20 + 10)],
               TAPE if i % 2 == 0 else TAPE_L, "#0E1419", 1.4)
        x += step
        i += 1


def d14_taping():
    """টেপিং পদ্ধতি।"""
    s = SVG(1240, 700)
    s.title("জয়েন্টে টেপ পেঁচানোর নিয়ম", T_TITLE)
    PW, PH = 365, 250
    cases = [
        ("১ — শুরু", "ইনসুলেশনের উপর থেকে", 0.0),
        ("২ — হাফ-ল্যাপ", "প্রতি পাকে অর্ধেক ঢেকে", 0.62),
        ("৩ — শেষ", "অন্য পাশের ইনসুলেশন ছাড়িয়ে", 1.0),
    ]
    for i, (head, sub, frac) in enumerate(cases):
        x = 46 + i * (PW + 26)
        panel(s, x, 96, PW, PH, head, STEEL)
        cy = 96 + 150
        wx0, wx1 = x + 26, x + PW - 26
        _wire(s, wx0, wx1, cy, wx0 + 78, wx1 - 78)
        _twist(s, x + PW / 2, cy, 120)
        t0, t1 = wx0 + 46, wx1 - 46
        if frac > 0:
            _tape(s, t0, t0 + (t1 - t0) * frac, cy)
        else:
            _tape(s, t0, t0 + 34, cy)
        s.text(x + PW / 2, 96 + PH - 26, sub, T_SMALL, GREY, 400, "middle")

    yb = 96 + PH + 26
    bullets = [
        "টেপ শুরু ও শেষ করতে হবে তারের ইনসুলেশনের উপরে, অন্তত ২৫ মিমি ছাড়িয়ে;",
        "প্রতিটি পাক আগের পাকের অর্ধেক ঢেকে দেবে — একেই হাফ-ল্যাপ বলে;",
        "টেপ হালকা টান দিয়ে পেঁচাতে হবে, ঢিলা টেপ খুলে যায়;",
        "টেপের মোট পুরুত্ব তারের নিজস্ব ইনসুলেশনের চেয়ে কম হবে না।",
    ]
    s.rect(46, yb, 1148, 178, "#F7FAFC", LINE, 1.8, 12)
    yy = yb + 44
    for b in bullets:
        s.circle(76, yy - 7, 6, STEEL)
        s.text(98, yy, b, T_BODY, "#28323C")
        yy += 40
    y = note_strip(s, yb + 198,
                   "PVC ইনসুলেশন টেপ IEC 60454-3-1 অনুযায়ী হতে হবে; কাপড়ের "
                   "ফিতা বা কাগজের টেপ কোনোভাবেই চলবে না")
    s.fit(y, 24)
    return s.save(f"{OUT}/d14_taping.svg")


def d15_modern():
    """আধুনিক সংযোগ-সামগ্রী।"""
    return two_panel(
        "d15_modern", "আধুনিক সংযোগ-সামগ্রী",
        ("টুইস্ট-অন কানেক্টর (ওয়্যার নাট)", "ph_wire_nuts.jpg"),
        ("লিভার-টাইপ কানেক্টর", "ph_lever_conn.jpg"),
        "জংশন বক্সের ভেতরে এখন পাকানো জয়েন্টের বদলে অনুমোদিত কানেক্টরও "
        "ব্যবহার করা হয়",
        h=620)


ALL = [d01_steps, d02_skinning, d03_types, d04_wu, d05_wu_ties, d06_pigtail,
       d07_tee, d08_cross, d09_britannia, d10_married, d11_fixture,
       d12_solder_tools, d13_solder_steps, d14_taping, d15_modern]

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
