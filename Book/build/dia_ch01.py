# -*- coding: utf-8 -*-
"""অধ্যায় ১ — কর্মক্ষেত্রে নিরাপত্তা : টেকনিক্যাল ডায়াগ্রাম।

Type sizing rule
----------------
A diagram drawn W px wide and placed P cm wide on the page renders its N-px
type at  N × (P in pt) / W  points.  At P = 15.6 cm (442 pt) a 1060-px canvas
turns 13 px into 5.4 pt — unreadable in print.  Every size below is therefore
chosen so the smallest label lands at ~8.5 pt or larger once placed.
Purely tabular content is NOT drawn here at all; it goes into native Word
tables (see ch01.py) so it stays editable.
"""
import os, math
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, PAPER, tw, wrap)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams", "ch01")

# type scale — body label 21 px on a ~1100 px canvas ≈ 8.4 pt at 15.6 cm
T_TITLE = 34
T_NODE = 28
T_NAME = 25.5
T_BODY = 23
T_SMALL = 22.5
LH = 1.42


def lines_h(n, size, lh=LH):
    return n * size * lh


def bullet_panel(s, x, y, w, items, size=T_BODY, fill="#F7FAFC", stroke=LINE,
                 tcolor=INK, bullet_color=STEEL, pad=20, lh=LH, gap=10):
    """Auto-height bulleted panel; returns bottom y."""
    inner = w - 2 * pad - size * 1.15
    rows = [wrap(it, inner, size, 400) for it in items]
    h = pad * 2 + sum(lines_h(len(r), size, lh) for r in rows) + gap * (len(rows) - 1)
    s.rect(x, y, w, h, fill, stroke, 1.8, 12)
    yy = y + pad
    for ln_set in rows:
        base = yy + size * 0.82
        s.circle(x + pad + size * 0.22, base - size * 0.30, size * 0.19, bullet_color)
        for i, ln in enumerate(ln_set):
            s.text(x + pad + size * 1.15, base + i * size * lh, ln, size, tcolor, 400)
        yy += lines_h(len(ln_set), size, lh) + gap
    return y + h


def worker(s, cx, top, scale=1.0, helmet=True, goggles=True, vest=True,
           gloves=True, boots=True, mask=False, harness=False, earplug=False,
           skin="#F0C9A4", cloth="#2E5F8A", pants="#37474F", reach_l=None):
    """Stylised electrician figure; returns anchor points for callouts."""
    S = scale
    head_r = 30 * S
    hy = top + head_r + 14 * S
    sh_y = hy + head_r + 16 * S
    hip_y = sh_y + 96 * S
    foot_y = hip_y + 108 * S
    body_w = 74 * S

    s.path(f"M {cx-19*S:.1f} {hip_y:.1f} L {cx-24*S:.1f} {foot_y:.1f}", pants, 21 * S)
    s.path(f"M {cx+19*S:.1f} {hip_y:.1f} L {cx+24*S:.1f} {foot_y:.1f}", pants, 21 * S)
    if boots:
        for dx in (-24 * S, 24 * S):
            s.rect(cx + dx - 15 * S, foot_y - 5 * S, 30 * S, 17 * S,
                   "#2B2B2B", "#111", 1.2, 5 * S)
            s.rect(cx + dx - 16 * S, foot_y + 9 * S, 34 * S, 6 * S,
                   "#F0A500", "#B37A00", 1, 3 * S)
    s.path(f"M {cx-body_w/2:.1f} {sh_y+4*S:.1f} "
           f"Q {cx-body_w/2-3*S:.1f} {hip_y:.1f} {cx-30*S:.1f} {hip_y+6*S:.1f} "
           f"L {cx+30*S:.1f} {hip_y+6*S:.1f} "
           f"Q {cx+body_w/2+3*S:.1f} {hip_y:.1f} {cx+body_w/2:.1f} {sh_y+4*S:.1f} "
           f"Q {cx:.1f} {sh_y-9*S:.1f} {cx-body_w/2:.1f} {sh_y+4*S:.1f} Z",
           "#1D3F5C", 1.6, cloth)
    arm_x = body_w / 2 + 6 * S
    if reach_l:
        # the left arm raised to touch something (a device body)
        s.path(f"M {cx-arm_x:.1f} {sh_y+12*S:.1f} L {reach_l[0]+9*S:.1f} {reach_l[1]:.1f}",
               cloth, 19 * S, cap="round")
    else:
        s.path(f"M {cx-arm_x:.1f} {sh_y+12*S:.1f} L {cx-arm_x-16*S:.1f} {hip_y+16*S:.1f}",
               cloth, 19 * S)
    s.path(f"M {cx+arm_x:.1f} {sh_y+12*S:.1f} L {cx+arm_x+16*S:.1f} {hip_y+16*S:.1f}",
           cloth, 19 * S)
    gcol = "#E8A33D" if gloves else skin
    gedge = "#B4761F" if gloves else "#D6A882"
    hand_l = reach_l or (cx - arm_x - 18 * S, hip_y + 26 * S)
    hand_r = (cx + arm_x + 18 * S, hip_y + 26 * S)
    for (hx_, hy_), sgn in ((hand_l, -1), (hand_r, 1)):
        if gloves:
            # an insulated glove with SEPARATE FINGERS, not a round blob — a
            # flared gauntlet cuff, a palm, four fingers pointing down and a
            # thumb on the body side, so it can never read as a joint circle
            s.path(f"M {hx_-12*S:.1f} {hy_-6*S:.1f} L {hx_-8.5*S:.1f} {hy_-30*S:.1f} "
                   f"L {hx_+8.5*S:.1f} {hy_-30*S:.1f} L {hx_+12*S:.1f} {hy_-6*S:.1f} Z",
                   gedge, 1.6, "#D98A2B")                        # gauntlet cuff
            s.rect(hx_ - sgn * 12 * S - 3 * S, hy_ - 12 * S, 6.5 * S, 14 * S,
                   gcol, gedge, 1.4, 3 * S)                      # thumb, body side
            s.rect(hx_ - 11 * S, hy_ - 14 * S, 22 * S, 15 * S,
                   gcol, gedge, 1.6, 4 * S)                      # palm
            for k in (-8.4, -2.8, 2.8, 8.4):                     # four fingers
                s.rect(hx_ + k * S - 2.5 * S, hy_ - 1 * S, 5 * S, 15 * S,
                       gcol, gedge, 1.3, 2.5 * S)
        else:
            s.circle(hx_, hy_, 11.5 * S, gcol, gedge, 1.4)
    if vest:
        s.path(f"M {cx-body_w/2+7*S:.1f} {sh_y+10*S:.1f} "
               f"L {cx-body_w/2+7*S:.1f} {hip_y+2*S:.1f} "
               f"L {cx-14*S:.1f} {hip_y+2*S:.1f} L {cx-14*S:.1f} {sh_y+6*S:.1f} Z",
               "none", 0, "#F2C200")
        s.path(f"M {cx+body_w/2-7*S:.1f} {sh_y+10*S:.1f} "
               f"L {cx+body_w/2-7*S:.1f} {hip_y+2*S:.1f} "
               f"L {cx+14*S:.1f} {hip_y+2*S:.1f} L {cx+14*S:.1f} {sh_y+6*S:.1f} Z",
               "none", 0, "#F2C200")
        s.rect(cx - body_w / 2 + 7 * S, sh_y + 40 * S, body_w - 14 * S, 8 * S,
               "#D8DEE4", "none", 0, 1)
    if harness:
        HC, HD = "#E05A1F", "#A83C10"
        # shoulder straps crossing on the chest
        s.path(f"M {cx-24*S:.1f} {sh_y+2*S:.1f} L {cx+20*S:.1f} {hip_y+2*S:.1f}", HC, 7.5 * S)
        s.path(f"M {cx+24*S:.1f} {sh_y+2*S:.1f} L {cx-20*S:.1f} {hip_y+2*S:.1f}", HC, 7.5 * S)
        # chest strap
        s.path(f"M {cx-25*S:.1f} {sh_y+28*S:.1f} L {cx+25*S:.1f} {sh_y+28*S:.1f}", HC, 5.5 * S)
        # waist belt — runs past the jacket edge so it reads as a separate strap
        s.path(f"M {cx-40*S:.1f} {hip_y-7*S:.1f} L {cx+40*S:.1f} {hip_y-7*S:.1f}", HC, 9 * S)
        # D-ring at the chest crossing
        s.circle(cx, sh_y + 50 * S, 9 * S, "#C9CFD6", "#5A6470", 1.8 * S)
        s.circle(cx, sh_y + 50 * S, 4.4 * S, "#FFFFFF", "#5A6470", 1.2 * S)
        # thigh loops
        for dx in (-21 * S, 21 * S):
            s.path(f"M {cx+dx-13*S:.1f} {hip_y+24*S:.1f} "
                   f"L {cx+dx+13*S:.1f} {hip_y+24*S:.1f}", HC, 6.5 * S)
        s.path(f"M {cx-40*S:.1f} {hip_y-7*S:.1f} L {cx+40*S:.1f} {hip_y-7*S:.1f}",
               HD, 1.2, dash="6 7")
    s.rect(cx - 9 * S, sh_y - 16 * S, 18 * S, 18 * S, skin, "none", 0, 4 * S)
    # ears first, so the head circle hides their inner half and only the
    # lobe shows — an ear plug has to have somewhere real to sit
    for ex in (cx - 28.5 * S, cx + 28.5 * S):
        s.circle(ex, hy + 3 * S, 7.5 * S, skin, "#D6A882", 1.5)
    s.circle(cx, hy, head_r, skin, "#D6A882", 1.6)
    s.circle(cx - 10 * S, hy + 1 * S, 2.6 * S, "#33383D")
    s.circle(cx + 10 * S, hy + 1 * S, 2.6 * S, "#33383D")
    s.path(f"M {cx-8*S:.1f} {hy+14*S:.1f} Q {cx:.1f} {hy+19*S:.1f} {cx+8*S:.1f} {hy+14*S:.1f}",
           "#9C6B4A", 1.8 * S)
    if mask:
        # a real dust mask: nose bridge under the goggles, pleats, ear loops
        s.path(f"M {cx-22*S:.1f} {hy+6*S:.1f} Q {cx:.1f} {hy+2*S:.1f} {cx+22*S:.1f} {hy+6*S:.1f} "
               f"L {cx+17*S:.1f} {hy+19*S:.1f} Q {cx:.1f} {hy+27*S:.1f} "
               f"{cx-17*S:.1f} {hy+19*S:.1f} Z", "#5F7383", 1.7, "#DCE7EF")
        for dy in (12, 17):
            s.path(f"M {cx-20*S:.1f} {hy+dy*S:.1f} Q {cx:.1f} {hy+(dy+4)*S:.1f} "
                   f"{cx+20*S:.1f} {hy+dy*S:.1f}", "#9DB2C1", 1.3 * S)
        # the loops hook over the TOP of the ear, clear of where a plug goes
        s.path(f"M {cx-22*S:.1f} {hy+9*S:.1f} Q {cx-34*S:.1f} {hy+5*S:.1f} "
               f"{cx-30*S:.1f} {hy-3*S:.1f}", "#5F7383", 1.5 * S)
        s.path(f"M {cx+22*S:.1f} {hy+9*S:.1f} Q {cx+34*S:.1f} {hy+5*S:.1f} "
               f"{cx+30*S:.1f} {hy-3*S:.1f}", "#5F7383", 1.5 * S)
    if goggles:
        # lens over the eyes only — it must not run onto the ear, or the
        # ear plug beside it has nowhere left to sit.  The temple arm goes
        # back ABOVE the ear, the way a strap actually runs.
        s.rect(cx - 22 * S, hy - 9 * S, 44 * S, 17 * S, "#9CC8E8", "none", 0,
               7 * S, opacity=0.55)
        s.rect(cx - 22 * S, hy - 9 * S, 44 * S, 17 * S, "none", "#2E6F9E", 2, 7 * S)
        s.line(cx - 3 * S, hy - 9 * S, cx - 3 * S, hy + 8 * S, "#2E6F9E", 1.6)
        s.line(cx - 22 * S, hy - 4 * S, cx - 31 * S, hy - 7 * S, "#2E6F9E", 2.4)
        s.line(cx + 22 * S, hy - 4 * S, cx + 31 * S, hy - 7 * S, "#2E6F9E", 2.4)
    if earplug:
        # in the ear, not on it: the plug sits at the centre of the lobe with
        # its stem showing, drawn last so nothing covers it
        for sgn in (-1, 1):
            ex = cx + sgn * 28.5 * S
            s.circle(ex, hy + 3.5 * S, 4.3 * S, "#F2C200", "#A87F00", 1.4)
            s.line(ex + sgn * 3.2 * S, hy + 3.5 * S, ex + sgn * 6.6 * S,
                   hy + 4.6 * S, "#F2C200", 3.2 * S)
    if helmet:
        # A hard hat, not a bowler.  Two things go wrong every time this is
        # drawn: the shell comes out narrower than the skull, so it perches
        # on top like a hat; and the brim gets pulled down over the eyes.
        # So the shell is a low ellipse WIDER than the head (34S against the
        # head's 30S) and it sits down over the crown, while the brim clears
        # the eyebrow line by a clear margin.
        HL, HD = "#F26B0F", "#C8500A"
        s.path(f"M {cx-34*S:.1f} {hy-11*S:.1f} "
               f"A {34*S:.1f} {27*S:.1f} 0 0 1 {cx+34*S:.1f} {hy-11*S:.1f} Z",
               HD, 1.8, HL)
        s.path(f"M {cx:.1f} {hy-37*S:.1f} L {cx:.1f} {hy-12*S:.1f}", HD, 2.2)
        for dx in (-20 * S, 20 * S):
            s.path(f"M {cx+dx:.1f} {hy-30*S:.1f} L {cx+dx*1.15:.1f} {hy-12*S:.1f}",
                   HD, 1.5, opacity=0.7)
        s.rect(cx - 43 * S, hy - 16 * S, 86 * S, 8.5 * S, HL, HD, 1.6, 4 * S)
    return {"head": (cx, hy), "helmet": (cx - 16 * S, hy - 25 * S),
            "goggles": (cx - 19 * S, hy - 1 * S),
            "mask": (cx - 10 * S, hy + 20 * S),
            "ear": (cx + 28.5 * S, hy + 3.5 * S),
            "ear_l": (cx - 28.5 * S, hy + 3.5 * S),
            "mouth": (cx, hy + 18 * S),
            "vest": (cx + 22 * S, sh_y + 70 * S),
            "hand": hand_r, "hand_l": hand_l,
            "boot": (cx + 24 * S, foot_y + 6 * S),
            "harness": (cx - 40 * S, hip_y - 7 * S),
            "bottom": foot_y + 20 * S, "scale": S,
            "shoulder_l": (cx - arm_x, sh_y + 12 * S), "hip": (cx, hip_y)}


def _stack(anchors, box_h, gap, first_top):
    pitch = box_h + gap
    tops, prev = [], None
    for ay in anchors:
        t = ay - box_h / 2 if prev is None else max(ay - box_h / 2, prev + pitch)
        tops.append(max(t, first_top))
        prev = tops[-1]
    return tops


# ═══════════════════════════════════════════════════════════════════════
def d01_causes():
    s = SVG(1240, 900)
    s.title("বৈদ্যুতিক দুর্ঘটনার কারণসমূহের শ্রেণিবিন্যাস", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 16)
    rx, ry, rw, rh = s.box_auto(620, 74, "বৈদ্যুতিক দুর্ঘটনার কারণ", T_NODE,
                                fill=NAVY, stroke=NAVY, tcolor="#FFFFFF",
                                pad_x=32, pad_y=17)
    cols = [
        ("কারিগরি কারণ", "#E8F0F8", STEEL,
         ["শাট-ডাউন না করে বা ভুলভাবে শাট-ডাউন করে কাজ করা",
          "টেস্টার দিয়ে লাইন ডেড কি না নিশ্চিত না করা",
          "অস্থায়ী আর্থিং না দেওয়া",
          "ফিডার বা যন্ত্রপাতি ওভারলোডেড চালানো",
          "লুজ কানেকশনে কন্ডাক্টর গরম হওয়া",
          "ব্রেকার বা ফিউজের রেটিং ভুল হওয়া"]),
        ("অকারিগরি কারণ", "#FFF6E5", AMBER,
         ["কর্মীর অজ্ঞতা, অবহেলা ও অতিরিক্ত আত্মবিশ্বাস",
          "শর্ট-কাট পদ্ধতিতে কাজ সারার প্রবণতা",
          "নিম্নমানের মালামাল ও ত্রুটিপূর্ণ ওয়্যারিং",
          "অসুস্থ অবস্থায় লাইনে কাজ করা",
          "কাজের পূর্বপরিকল্পনার অভাব",
          "নিরাপত্তাবিধি না মানা"]),
        ("প্রাকৃতিক কারণ", "#EAF6EF", GREEN,
         ["বজ্রপাত, ঝড় ও ঘূর্ণিঝড়",
          "বন্যায় লাইন ডুবে যাওয়া",
          "ভূমিধসে পোল হেলে পড়া",
          "ভূমিকম্পে অবকাঠামো ক্ষতিগ্রস্ত হওয়া",
          "গাছের ডাল পড়ে লাইন ছেঁড়া"]),
    ]
    cw, gapx = 386, 26
    xs = [22, 22 + cw + gapx, 22 + 2 * (cw + gapx)]
    ytop = 236
    s.path(f"M 620 {ry+rh:.1f} L 620 {ytop-72:.1f}", STEEL, 2.6)
    for i, (name, bg, br, items) in enumerate(cols):
        cx = xs[i] + cw / 2
        s.path(f"M 620 {ytop-72:.1f} L {cx:.1f} {ytop-72:.1f} L {cx:.1f} {ytop-22:.1f}",
               STEEL, 2.6, marker=ar)
        s.box_auto(cx, ytop - 12, name, T_NAME, fill=br, stroke=br,
                   tcolor="#FFFFFF", pad_x=28, pad_y=13, min_w=250)
    bot = 0
    for i, (name, bg, br, items) in enumerate(cols):
        bot = max(bot, bullet_panel(s, xs[i], ytop + 62, cw, items,
                                    T_BODY, bg, br, INK, br))
    s.text(620, bot + 46, "একটি দুর্ঘটনার পেছনে সাধারণত একাধিক কারণ একসঙ্গে কাজ করে",
           T_SMALL, GREY, 400, "middle")
    s.fit(bot + 46, 26)
    return s.save(f"{OUT}/d01_causes.svg")


def d02_shock_path():
    s = SVG(1120, 700)
    s.title("মানবদেহে বিদ্যুৎ প্রবাহের পথ", T_TITLE)
    ar = s.arrow_defs(RED, "arr", 15)
    GY = 462
    panels = [(282, "হাত থেকে হাত", "প্রবাহের বড় অংশ সরাসরি হৃৎপিণ্ডের ভেতর দিয়ে যায়"),
              (838, "হাত থেকে পা", "সবচেয়ে বিপজ্জনক পথ, পুরো দেহ প্রবাহপথে পড়ে")]
    for cx, title, sub in panels:
        s.rect(cx - 248, 66, 496, 512, "#FCFDFE", LINE, 1.8, 14)
        s.box_auto(cx, 80, title, T_NAME, fill=RED, stroke=RED, tcolor="#FFFFFF",
                   pad_x=26, pad_y=12)
        for j, ln in enumerate(wrap(sub, 452, T_SMALL, 400)):
            s.text(cx, 546 + j * T_SMALL * 1.35, ln, T_SMALL, GREY, 400, "middle")
        s.rect(cx - 210, GY, 420, 12, "#8D9AA8", "#6B7684", 1.2, 3)
        for i in range(14):
            s.line(cx - 204 + i * 31, GY + 12, cx - 212 + i * 31, GY + 24, "#8D9AA8", 2)

    a = worker(s, 282, 148, 0.86, goggles=False, vest=False,
               gloves=False, boots=False, cloth="#3E6E93")
    hx1, hy1 = a["hand_l"]; hx2, hy2 = a["hand"]
    hyc = 302
    s.path(f"M {hx1:.1f} {hy1-9:.1f} Q 282 236 282 {hyc-19:.1f}", RED, 3.6, dash="10 7")
    s.path(f"M 282 {hyc+19:.1f} Q 282 240 {hx2:.1f} {hy2-9:.1f}", RED, 3.6, dash="10 7")
    s.heart(282, hyc, 20)
    s.path(f"M {hx1-64:.1f} {hy1:.1f} L {hx1-18:.1f} {hy1:.1f}", RED, 3.6, marker=ar)
    s.path(f"M {hx2+18:.1f} {hy2:.1f} L {hx2+64:.1f} {hy2:.1f}", RED, 3.6, marker=ar)
    s.text(hx1 - 72, hy1 + 7, "L", T_NAME, RED, 700, "end")
    s.text(hx2 + 72, hy2 + 7, "N", T_NAME, RED, 700, "start")
    s.text(282, 518, "দুই হাতের মধ্য দিয়ে সার্কিট সম্পূর্ণ হয়", T_SMALL, "#7A1810", 600, "middle")

    b = worker(s, 838, 148, 0.86, goggles=False, vest=False,
               gloves=False, boots=False, cloth="#3E6E93")
    hx, hy = b["hand"]
    s.path(f"M {hx:.1f} {hy-9:.1f} Q 838 240 838 {hyc-19:.1f}", RED, 3.6, dash="10 7")
    s.path(f"M 838 {hyc+19:.1f} L 838 {GY-12:.1f}", RED, 3.6, dash="10 7", marker=ar)
    s.heart(838, hyc, 20)
    s.path(f"M {hx+18:.1f} {hy:.1f} L {hx+64:.1f} {hy:.1f}", RED, 3.6, marker=ar)
    s.text(hx + 72, hy + 7, "L", T_NAME, RED, 700, "start")
    s.text(838, 518, "পা হয়ে কারেন্ট মাটিতে নেমে যায়", T_SMALL, "#7A1810", 600, "middle")
    s.text(676, GY - 12, "মাটি / আর্থ", T_SMALL, "#4A5561", 600, "middle")

    s.rect(30, 600, 1060, 56, "#FFF6E5", AMBER, 1.8, 11)
    s.text(560, 636,
           "কারেন্টের পথে হৃৎপিণ্ড পড়লেই ভেন্ট্রিকুলার ফিব্রিলেশনের ঝুঁকি সবচেয়ে বেশি",
           T_BODY, "#7A5200", 600, "middle")
    s.fit(656, 24)
    return s.save(f"{OUT}/d02_shock_path.svg")


def d04_safety_types():
    s = SVG(1180, 620)
    s.title("নিরাপত্তার শ্রেণিবিভাগ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 16)
    rx, ry, rw, rh = s.box_auto(590, 72, "নিরাপত্তা (Safety)", T_NODE, fill=NAVY,
                                stroke=NAVY, tcolor="#FFFFFF", pad_x=34, pad_y=16)
    items = [("পার্সোনাল সেফটি", "Personal Safety",
              "নিজেকে দুর্ঘটনা থেকে রক্ষার সব ব্যবস্থা", "#E8F0F8", STEEL),
             ("ওয়ার্কশপ সেফটি", "Workshop Safety",
              "ওয়ার্কশপে মেনে চলার নিয়ম ও শৃঙ্খলা", "#EAF6EF", GREEN),
             ("স্পেশাল সেফটি", "Special Safety",
              "অগ্নিকাণ্ড ও দুর্যোগের বিশেষ নিরাপত্তা", "#FFF6E5", AMBER)]
    cw, gapx = 356, 26
    xs = [30, 30 + cw + gapx, 30 + 2 * (cw + gapx)]
    ytop = 232
    s.path(f"M 590 {ry+rh:.1f} L 590 {ytop-70:.1f}", STEEL, 2.6)
    nl = max(len(wrap(d_, cw - 52, T_BODY, 400)) for _, _, d_, _, _ in items)
    h = 92 + lines_h(nl, T_BODY) + 36          # all three cards the same height
    for i, (bn_, en, desc, bg, br) in enumerate(items):
        cx = xs[i] + cw / 2
        s.path(f"M 590 {ytop-70:.1f} L {cx:.1f} {ytop-70:.1f} L {cx:.1f} {ytop-16:.1f}",
               STEEL, 2.6, marker=ar)
        dl = wrap(desc, cw - 52, T_BODY, 400)
        s.rect(xs[i], ytop, cw, h, bg, br, 2, 13)
        s.rect(xs[i], ytop, cw, 62, br, br, 2, 13)
        s.rect(xs[i] + 1, ytop + 52, cw - 2, 10, br, "none", 0, 0)
        s.text(cx, ytop + 40, bn_, T_NAME, "#FFFFFF", 700, "middle")
        s.text(cx, ytop + 94, en, T_BODY, br, 700, "middle")
        for j, ln in enumerate(dl):
            s.text(cx, ytop + 130 + j * T_BODY * LH, ln, T_BODY, "#2E3842", 400, "middle")
    bot = ytop + h
    s.text(590, bot + 44,
           "তিন প্রকার নিরাপত্তা একসঙ্গে নিশ্চিত হলে কর্মক্ষেত্র নিরাপদ হয়",
           T_SMALL, GREY, 400, "middle")
    s.fit(bot + 44, 26)
    return s.save(f"{OUT}/d04_safety_types.svg")


def d05_ppe():
    s = SVG(1200, 820)
    s.title("ব্যক্তিগত প্রতিরক্ষামূলক সরঞ্জাম (PPE): মাথা থেকে পা", T_TITLE)
    S = 1.42
    a = worker(s, 600, 92, S, mask=True, harness=True, earplug=True)
    hx, hy = a["head"]
    # Left-side leaders are routed round the figure, never across it: the old
    # straight leaders ran the goggles line through the ear plug and the
    # mask and harness lines across the arm and the glove.
    gog = (hx - 25, hy + 6)                 # lower-left of the lens
    msk = (hx - 12, hy + 30)                # lower-left of the mask
    thigh = (hx - 48, a["hip"][1] + 34)     # left thigh loop of the harness
    left = [("সেফটি হেলমেট", "পড়ন্ত বস্তুর আঘাত থেকে মাথা বাঁচায়", a["helmet"], None),
            ("সেফটি গগলস", "স্পার্ক, ধুলা ও ধাতুকণা থেকে চোখ বাঁচায়", gog,
             lambda m: [(440, m), (440, hy + 30), (hx - 52, hy + 30), gog]),
            ("ডাস্ট মাস্ক", "ধুলা ও ক্ষতিকর ধোঁয়া শ্বাসে ঢুকতে দেয় না", msk,
             lambda m: [(470, m), (470, hy + 50), (hx - 34, hy + 50), msk]),
            ("সেফটি হারনেস", "উঁচু থেকে পড়ে যাওয়া ঠেকায়", thigh,
             lambda m: [(thigh[0] - 10, m), (thigh[0] - 10, thigh[1]), thigh])]
    right = [("ইয়ার প্লাগ", "উচ্চ শব্দ থেকে কান রক্ষা করে", a["ear"], None),
             ("রিফ্লেক্টিভ অ্যাপ্রন", "দূর থেকে কর্মীকে সহজে দেখা যায়", a["vest"], None),
             ("ইনসুলেটেড গ্লাভস", "বিদ্যুৎ ও তাপ থেকে হাত বাঁচায়", a["hand"], None),
             ("সেফটি শু", "শক ও ভারী বস্তু থেকে পা বাঁচায়", a["boot"], None)]
    BW, GAP, LX, RX = 322, 18, 352, 848
    BH = 42 + lines_h(2, T_SMALL) + 24
    for side, items, edge in (("L", left, LX), ("R", right, RX)):
        tops = _stack([p[2][1] for p in items], BH, GAP, 74)
        for (name, desc, (px, py), route), by in zip(items, tops):
            x = edge - BW if side == "L" else edge
            s.rect(x, by, BW, BH, "#F5F9FC", STEEL, 1.8, 11)
            s.rect(x if side == "L" else x + BW - 6, by, 6, BH, STEEL, "none", 0, 2)
            tx = edge - 22 if side == "L" else edge + 22
            anc = "end" if side == "L" else "start"
            s.text(tx, by + 38, name, T_NAME, NAVY, 700, anc)
            for j, ln in enumerate(wrap(desc, BW - 46, T_SMALL, 400)):
                s.text(tx, by + 68 + j * T_SMALL * 1.35, ln, T_SMALL, "#4A5561", 400, anc)
            # the elbow must sit OUTSIDE the label box, otherwise the leader
            # doubles back across the lettering
            m = by + BH / 2
            if route:
                pts = [(edge, m)] + route(m)
                s.path("M " + " L ".join(f"{x_:.1f} {y_:.1f}" for x_, y_ in pts),
                       "#8A97A6", 1.7)
            else:
                stub = edge - 18 if side == "R" else edge + 18
                s.path(f"M {px:.1f} {py:.1f} L {stub:.1f} {m:.1f} "
                       f"L {edge:.1f} {m:.1f}", "#8A97A6", 1.7)
            s.circle(px, py, 4.2, "#8A97A6")
    fy = max(a["bottom"], 74 + 4 * (BH + GAP)) + 34
    s.rect(288, fy, 624, 58, "#EAF2FA", STEEL, 2, 11)
    s.text(600, fy + 37, "PPE ছাড়া কোনো বৈদ্যুতিক কাজ শুরু করা যাবে না",
           T_NAME, NAVY, 700, "middle")
    s.fit(fy + 58, 24)
    return s.save(f"{OUT}/d05_ppe.svg")


def d06_loto():
    s = SVG(1200, 460)
    s.title("লক-আউট ট্যাগ-আউট (LOTO) পদ্ধতির ছয়টি ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)
    steps = ["প্রস্তুতি", "সবাইকে জানানো", "সাপ্লাই বন্ধ", "লক ও ট্যাগ",
             "জমে থাকা শক্তি সরানো", "যাচাই"]
    n = len(steps)
    bw, gap = 168, 30
    x0 = (1200 - (n * bw + (n - 1) * gap)) / 2
    for i, t in enumerate(steps):
        x = x0 + i * (bw + gap)
        s.rect(x, 118, bw, 124, "#F5F9FC", STEEL, 2, 13)
        s.circle(x + bw / 2, 118, 28, NAVY)
        s.text(x + bw / 2, 128, ["১", "২", "৩", "৪", "৫", "৬"][i], T_NODE,
               "#FFFFFF", 700, "middle")
        tl = wrap(t, bw - 24, T_NAME, 700)
        y0 = 194 - (len(tl) - 1) * T_NAME * 0.65      # centred in the box below the badge
        for j, ln in enumerate(tl):
            s.text(x + bw / 2, y0 + j * T_NAME * 1.3, ln, T_NAME, NAVY, 700, "middle")
        if i < n - 1:
            s.path(f"M {x+bw+5:.1f} 186 L {x+bw+gap-7:.1f} 186", STEEL, 2.8, marker=ar)
    s.rect(x0, 276, n * bw + (n - 1) * gap, 64, REDBG, RED, 2, 12)
    s.text(600, 315,
           "যিনি তালা লাগিয়েছেন, শুধু তিনিই তালা খুলবেন",
           T_NAME, "#7A1810", 700, "middle")
    s.fit(340, 24)
    return s.save(f"{OUT}/d06_loto.svg")


def d07_five_rules():
    s = SVG(1180, 700)
    s.title("বৈদ্যুতিক কাজের পাঁচটি সোনালি নিয়ম", T_TITLE)
    rules = [("সম্পূর্ণ বিচ্ছিন্ন করা", "যেসব পথে বিদ্যুৎ আসতে পারে, সব বন্ধ"),
             ("আবার চালু হওয়া ঠেকানো", "ব্রেকারে তালা ও নামসহ ট্যাগ"),
             ("লাইন ডেড যাচাই", "অনুমোদিত টেস্টার দিয়ে নিশ্চিত হওয়া"),
             ("আর্থিং ও শর্টিং", "কাজের জায়গার দুই পাশে অস্থায়ী আর্থ"),
             ("লাইভ অংশ ঢেকে দেওয়া", "কভার দিয়ে ঢেকে সীমানা টানা")]
    cx, cy, R = 590, 414, 208
    s.circle(cx, cy, R + 5, "none", "#DCE5EE", 2.4)
    s.circle(cx, cy, 96, NAVY)
    s.text(cx, cy - 8, "পাঁচটি", T_NAME, "#9FC4E6", 700, "middle")
    s.text(cx, cy + 26, "সোনালি নিয়ম", T_NAME, "#FFFFFF", 700, "middle")
    for i, (t, d) in enumerate(rules):
        ang = math.radians(-90 + i * 72)
        px, py = cx + R * math.cos(ang), cy + R * math.sin(ang)
        s.line(cx + 99 * math.cos(ang), cy + 99 * math.sin(ang),
               px - 32 * math.cos(ang), py - 32 * math.sin(ang), "#C3CEDA", 2.4)
        s.circle(px, py, 32, STEEL, "#FFFFFF", 3.6)
        s.text(px, py + 10, ["১", "২", "৩", "৪", "৫"][i], T_NODE, "#FFFFFF", 700, "middle")
        if math.cos(ang) > 0.25:
            lx, anc = px + 48, "start"
        elif math.cos(ang) < -0.25:
            lx, anc = px - 48, "end"
        else:
            lx, anc = px, "middle"
        ly = py - 82 if math.sin(ang) < -0.4 else py + 6
        s.text(lx, ly, t, T_NAME, NAVY, 700, anc)
        for j, ln in enumerate(wrap(d, 330, T_SMALL, 400)):
            s.text(lx, ly + 31 + j * T_SMALL * 1.35, ln, T_SMALL, "#4A5561", 400, anc)
    s.fit(cy + R + 40, 18)
    return s.save(f"{OUT}/d07_five_rules.svg")


def d08_safety_signs():
    s = SVG(1180, 620)
    s.title("কর্মক্ষেত্রে ব্যবহৃত নিরাপত্তা চিহ্নের শ্রেণি", T_TITLE)
    groups = [("নিষেধাজ্ঞা", "Prohibition", "লাল বৃত্ত ও তির্যক দাগ", "যা করা নিষেধ", "#C0392B"),
              ("বাধ্যতামূলক", "Mandatory", "নীল ভরাট বৃত্ত", "যা অবশ্যই করতে হবে", "#1D5B8F"),
              ("সতর্কতা", "Warning", "হলুদ ত্রিভুজ", "সম্ভাব্য বিপদ", "#D89B00"),
              ("নিরাপদ অবস্থা", "Safe condition", "সবুজ চতুর্ভুজ", "বের হওয়ার পথ ও সহায়তা", "#1B6E47")]
    cw, gapx = 272, 24
    x0 = (1180 - (4 * cw + 3 * gapx)) / 2
    for i, (bn_, en, shape, mean, col) in enumerate(groups):
        x = x0 + i * (cw + gapx); cx = x + cw / 2
        s.rect(x, 78, cw, 386, "#FCFDFE", LINE, 1.8, 13)
        s.rect(x, 78, cw, 10, col, "none", 0, 5)
        cy = 190
        if i == 0:
            s.circle(cx, cy, 58, "#FFFFFF", col, 14)
            s.line(cx - 40, cy + 40, cx + 40, cy - 40, col, 14)
        elif i == 1:
            s.circle(cx, cy, 58, col, col, 2)
            s.path(f"M {cx-25:.1f} {cy:.1f} l 18 20 l 35 -38", "#FFFFFF", 10, cap="round")
        elif i == 2:
            s.poly([(cx, cy - 62), (cx + 65, cy + 48), (cx - 65, cy + 48)],
                   "#F5C400", "#1A1A1A", 7)
            s.text(cx, cy + 34, "!", 56, "#1A1A1A", 700, "middle")
        else:
            s.rect(cx - 58, cy - 58, 116, 116, col, col, 2, 8)
            s.path(f"M {cx-28:.1f} {cy-12:.1f} l 20 22 l 38 -42", "#FFFFFF", 10, cap="round")
        s.text(cx, 306, bn_, T_NAME, NAVY, 700, "middle")
        s.text(cx, 336, en, T_SMALL, col, 600, "middle")
        s.line(x + 30, 358, x + cw - 30, 358, "#E1E8EF", 1.6)
        yy = 390
        for ln in wrap(shape, cw - 40, T_BODY, 600):
            s.text(cx, yy, ln, T_BODY, "#39434D", 600, "middle"); yy += T_BODY * 1.35
        yy += 8
        for ln in wrap(mean, cw - 40, T_SMALL, 400):
            s.text(cx, yy, ln, T_SMALL, "#5A6470", 400, "middle"); yy += T_SMALL * 1.35
    s.text(590, 508, "লেখা পড়ার আগেই চিহ্নের রং ও আকৃতি দেখে বার্তা বোঝা যায়",
           T_SMALL, GREY, 400, "middle")
    s.fit(508, 26)
    return s.save(f"{OUT}/d08_safety_signs.svg")


def d10_rescue():
    s = SVG(1140, 900)
    s.title("বিদ্যুৎস্পৃষ্ট ব্যক্তিকে উদ্ধারের ধাপ", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)
    ar_g = s.arrow_defs(GREEN, "arg", 15)
    ar_r = s.arrow_defs(RED, "arr", 15)
    seq = [("নিজে নিরাপদ থাকা", "খালি হাতে আক্রান্ত ব্যক্তিকে স্পর্শ করা যাবে না", REDBG, RED, "#7A1810"),
           ("সাপ্লাই বন্ধ করা", "মেইন সুইচ বা ব্রেকার সঙ্গে সঙ্গে অফ করা", "#FFF6E5", AMBER, "#7A5200"),
           ("অপরিবাহী বস্তু দিয়ে সরানো", "শুকনো কাঠ, বাঁশ বা রাবার দিয়ে ঠেলে সরানো", "#F5F9FC", STEEL, NAVY),
           ("সাহায্য ডাকা", "৯৯৯-এ কল করে অ্যাম্বুলেন্স ডাকা", "#F5F9FC", STEEL, NAVY),
           ("শ্বাস ও নাড়ি পরীক্ষা", "১০ সেকেন্ড দেখে-শুনে-অনুভব করা", "#F5F9FC", STEEL, NAVY)]
    x0, w, y, rowh, vgap = 60, 1020, 84, 92, 26
    for i, (t, d, bg, br, tc) in enumerate(seq):
        yy = y + i * (rowh + vgap)
        s.rect(x0, yy, w, rowh, bg, br, 2, 12)
        s.circle(x0 + 54, yy + rowh / 2, 30, br)
        s.text(x0 + 54, yy + rowh / 2 + 10, ["১", "২", "৩", "৪", "৫"][i],
               T_NODE, "#FFFFFF", 700, "middle")
        s.text(x0 + 104, yy + 38, t, T_NAME, tc, 700)
        s.text(x0 + 104, yy + 72, d, T_BODY, "#4A5561", 400)
        if i < len(seq) - 1:
            s.path(f"M {x0+160:.1f} {yy+rowh+3:.1f} L {x0+160:.1f} {yy+rowh+vgap-5:.1f}",
                   STEEL, 2.8, marker=ar)
    dy = y + 5 * (rowh + vgap) + 16
    s.path(f"M {x0+160:.1f} {dy-26:.1f} L {x0+160:.1f} {dy+52:.1f} L 306 {dy+52:.1f}",
           STEEL, 2.8, marker=ar)
    s.poly([(570, dy), (834, dy + 52), (570, dy + 104), (306, dy + 52)],
           "#EAF2FA", STEEL, 2.2)
    s.text(570, dy + 46, "শ্বাস চলছে কি?", T_NAME, NAVY, 700, "middle")
    s.text(570, dy + 78, "১০ সেকেন্ড ধরে পরীক্ষা", T_BODY, GREY, 400, "middle")
    s.path(f"M 570 {dy+104:.1f} L 570 {dy+142:.1f} L 262 {dy+142:.1f} L 262 {dy+176:.1f}",
           GREEN, 2.8, marker=ar_g)
    s.path(f"M 834 {dy+52:.1f} L 906 {dy+52:.1f} L 906 {dy+176:.1f}",
           RED, 2.8, marker=ar_r)
    s.text(400, dy + 132, "হ্যাঁ", T_BODY, GREEN, 700, "middle")
    s.text(898, dy + 96, "না", T_BODY, RED, 700, "end")
    s.box_auto(262, dy + 184, "রিকভারি পজিশনে শুইয়ে নজরে রাখা",
               T_BODY, fill=GREENBG, stroke=GREEN, tcolor="#12523A", max_w=440,
               pad_x=22, pad_y=16)
    s.box_auto(906, dy + 184, "সঙ্গে সঙ্গে CPR শুরু করা",
               T_BODY, fill=REDBG, stroke=RED, tcolor="#7A1810", max_w=290,
               pad_x=22, pad_y=16)
    s.fit(dy + 300, 22)
    return s.save(f"{OUT}/d10_rescue.svg")


def d12_hierarchy():
    s = SVG(1200, 700)
    s.title("ঝুঁকি নিয়ন্ত্রণের ধাপক্রম (Hierarchy of Controls)", T_TITLE)
    levels = [("অপসারণ", "Elimination", "ঝুঁকির উৎসই সরিয়ে ফেলা", "#1B6E47"),
              ("প্রতিস্থাপন", "Substitution", "কম ঝুঁকির বিকল্প ব্যবহার", "#4E8C3F"),
              ("প্রকৌশলগত নিয়ন্ত্রণ", "Engineering", "গার্ড, ইনসুলেশন, আর্থিং, RCCB", "#B47500"),
              ("প্রশাসনিক নিয়ন্ত্রণ", "Administrative", "প্রশিক্ষণ, সাইনবোর্ড, কর্মপদ্ধতি", "#C86A16"),
              ("PPE", "ব্যক্তিগত সরঞ্জাম", "সুরক্ষার শেষ স্তর", "#B32A22")]
    ytop, hrow, vgap = 92, 96, 12
    wtop, wbot, cx, n = 700, 300, 524, 5
    for i, (bn_, en, d, col) in enumerate(levels):
        y = ytop + i * (hrow + vgap)
        w1 = wtop - (wtop - wbot) * i / n
        w2 = wtop - (wtop - wbot) * (i + 1) / n
        s.poly([(cx - w1 / 2, y), (cx + w1 / 2, y),
                (cx + w2 / 2, y + hrow), (cx - w2 / 2, y + hrow)], col, "#FFFFFF", 2.4)
        s.text(cx, y + 42, bn_, T_NAME, "#FFFFFF", 700, "middle")
        s.text(cx, y + 73, en, T_BODY, "#E8EEF3", 400, "middle")
        s.text(cx + w1 / 2 + 26, y + 58, d, T_BODY, "#39434D", 400)
    bot = ytop + n * (hrow + vgap) - vgap
    ax = 78
    s.text(78, ytop + 22, "বেশি", T_BODY, GREEN, 700, "middle")
    s.text(78, ytop + 51, "কার্যকর", T_BODY, GREEN, 700, "middle")
    s.text(78, bot - 40, "কম", T_BODY, RED, 700, "middle")
    s.text(78, bot - 11, "কার্যকর", T_BODY, RED, 700, "middle")
    s.path(f"M {ax} {ytop + 76:.1f} L {ax} {bot - 66:.1f}", "#9AA5B1", 3,
           marker=s.arrow_defs("#9AA5B1", "arg2", 14))
    s.text(600, bot + 46, "উপরের স্তর প্রয়োগ করা গেলে নিচের স্তরের উপর নির্ভরতা কমে যায়",
           T_BODY, GREY, 400, "middle")
    s.fit(bot + 46, 26)
    return s.save(f"{OUT}/d12_hierarchy.svg")


def d13_dead_test():
    s = SVG(1180, 560)
    s.title("লাইন ডেড যাচাই: তিন ধাপের পরীক্ষা (Prove–Test–Prove)", T_TITLE)
    ar = s.arrow_defs(STEEL, "ar", 15)
    panels = [("১", "টেস্টার যাচাই", "চালু লাইনে ধরে টেস্টার সচল কি না দেখা", GREEN, GREENBG, True),
              ("২", "লাইন পরীক্ষা", "বন্ধ করা লাইনে ধরা; কোনো সংকেত আসা চলবে না", STEEL, "#EAF2FA", False),
              ("৩", "আবার যাচাই", "আবার চালু লাইনে ধরে টেস্টার ঠিক আছে কি না নিশ্চিত হওয়া", GREEN, GREENBG, True)]
    bw, gap = 348, 34
    x0 = (1180 - (3 * bw + 2 * gap)) / 2
    for i, (num, t, d, col, bg, glow) in enumerate(panels):
        x = x0 + i * (bw + gap)
        s.rect(x, 92, bw, 322, bg, col, 2, 13)
        s.circle(x + 44, 128, 26, col)
        s.text(x + 44, 138, num, T_NODE, "#FFFFFF", 700, "middle")
        s.text(x + 82, 138, t, T_NAME, NAVY, 700)
        tx, ty = x + bw / 2, 246
        s.rect(tx - 15, ty - 54, 30, 106, "#F2C200", "#B08C00", 2, 7)
        s.rect(tx - 10, ty - 36, 20, 36, "#FFFFFF", "#B08C00", 1.4, 4)
        s.path(f"M {tx-5:.1f} {ty+52:.1f} L {tx-5:.1f} {ty+80:.1f} "
               f"L {tx+5:.1f} {ty+80:.1f} L {tx+5:.1f} {ty+52:.1f} Z", "#8D9AA8", 1.4, "#B7C1CB")
        if glow:
            s.circle(tx, ty - 18, 20, "#FF5A3C", "none", 0, 0.28)
            s.circle(tx, ty - 18, 11, "#FF3B1F")
            # rays leave sideways only, so none is drawn across the tester body
            for deg in (-30, 0, 30, 150, 180, 210):
                a_ = math.radians(deg)
                s.line(tx + 23 * math.cos(a_), ty - 18 + 23 * math.sin(a_),
                       tx + 35 * math.cos(a_), ty - 18 + 35 * math.sin(a_), "#FF7A45", 3)
            s.text(tx + 56, ty - 10, "জ্বলছে", T_BODY, RED, 700)
        else:
            s.circle(tx, ty - 18, 11, "#D8DEE4", "#9AA5B1", 1.6)
            s.text(tx + 46, ty - 10, "জ্বলবে না", T_BODY, STEEL, 700)
        for j, ln in enumerate(wrap(d, bw - 46, T_SMALL, 400)):
            s.text(x + bw / 2, 358 + j * T_SMALL * 1.35, ln, T_SMALL, "#39434D", 400, "middle")
        if i < 2:
            s.path(f"M {x+bw+5:.1f} 252 L {x+bw+gap-7:.1f} 252", STEEL, 2.8, marker=ar)
    s.rect(x0, 444, 3 * bw + 2 * gap, 58, REDBG, RED, 2, 11)
    s.text(590, 481, "শুধু দ্বিতীয় ধাপ করলে চলবে না, কারণ টেস্টার নিজেই নষ্ট থাকতে পারে",
           T_NAME, "#7A1810", 600, "middle")
    s.fit(502, 24)
    return s.save(f"{OUT}/d13_dead_test.svg")


def d14_earthing():
    s = SVG(1200, 720)
    s.title("আর্থিং কীভাবে বিদ্যুৎস্পৃষ্ট হওয়া থেকে রক্ষা করে", T_TITLE)
    ar_r = s.arrow_defs(RED, "arr", 15)
    ar_g = s.arrow_defs(GREEN, "arg", 15)

    def appliance(x, y, label, wmax=300):
        s.rect(x, y, 140, 112, "#B7C1CB", "#7C8794", 2, 11)
        s.rect(x + 20, y + 22, 100, 46, "#8D9AA8", "#6B7684", 1.4, 6)
        lines = label if isinstance(label, list) else wrap(label, wmax, T_SMALL, 600)
        for j, ln in enumerate(lines):
            s.text(x + 70, y + 150 + j * T_SMALL * 1.35, ln, T_SMALL, "#39434D", 600, "middle")

    GY = 512
    for cx, title, br in ((308, "আর্থিং ছাড়া", RED), (892, "আর্থিংসহ", GREEN)):
        s.rect(cx - 266, 72, 532, 542, "#FCFDFE", LINE, 1.8, 14)
        s.box_auto(cx, 86, title, T_NAME, fill=br, stroke=br, tcolor="#FFFFFF",
                   pad_x=26, pad_y=12)
        s.rect(cx - 240, GY, 480, 13, "#8D9AA8", "#6B7684", 1.4, 3)
        for i in range(16):
            s.line(cx - 234 + i * 31, GY + 13, cx - 242 + i * 31, GY + 26, "#8D9AA8", 2)

    # The person actually touches the appliance's body: the raised left hand
    # rests on its right-hand side.  (The old figure stood him a pace away and
    # let an arrow jump the gap, which read as current through the air.)
    TOUCH_Y = 286

    # left: no earth.  The leakage reaches the body, then the hand, and runs
    # through the man to the ground.
    appliance(132, 202, "ত্রুটিপূর্ণ যন্ত্র (বডিতে লিক)")
    s.line(66, 178, 300, 178, NAVY, 3)
    s.text(60, 172, "L", T_NAME, RED, 700, "end")
    s.path("M 202 178 L 202 202", NAVY, 3)
    s.circle(202, 228, 9, RED)
    s.path("M 210 234 L 262 274", RED, 3, dash="8 6")
    w = worker(s, 372, 246, 0.72, helmet=False, goggles=False, vest=False,
               gloves=False, boots=False, cloth="#3E6E93", reach_l=(276, TOUCH_Y))
    shx, shy = w["shoulder_l"]
    s.path(f"M 280 {TOUCH_Y:.1f} L {shx+8:.1f} {shy+6:.1f} L 372 {w['hip'][1]:.1f} "
           f"L 372 {GY-14:.1f}", RED, 3.4, dash="9 6", marker=ar_r)
    for j, ln in enumerate(wrap("দেহ দিয়ে কারেন্ট মাটিতে যায়, মারাত্মক শক লাগে",
                                470, T_SMALL, 600)):
        s.text(308, GY + 70 + j * T_SMALL * 1.35, ln, T_SMALL, "#7A1810", 600, "middle")

    # right: with earth.  Same fault, same touch, but the fault current takes
    # the earth conductor and the man is safe.
    appliance(724, 202, ["একই ত্রুটি,", "বডি আর্থ করা"])
    s.line(650, 178, 884, 178, NAVY, 3)
    s.text(644, 172, "L", T_NAME, RED, 700, "end")
    s.path("M 794 178 L 794 202", NAVY, 3)
    s.circle(794, 228, 9, RED)
    s.rect(714, 258, 12, 20, GREEN, "#0E4430", 1.4, 3)
    s.path(f"M 714 268 L 686 268 L 686 {GY-16:.1f}", GREEN, 3.8, marker=ar_g)
    s.text(704, 436, "ফল্ট কারেন্ট", T_BODY, GREEN, 700)
    s.text(704, 464, "আর্থ তারে চলে যায়", T_BODY, GREEN, 400)
    w2 = worker(s, 964, 246, 0.72, helmet=False, goggles=False, vest=False,
                gloves=False, boots=False, cloth="#3E6E93", reach_l=(868, TOUCH_Y))
    s.check(1080, 196, 21)
    for j, ln in enumerate(["স্পর্শ করলেও", "শক লাগে না"]):
        s.text(1080, 250 + j * T_SMALL * 1.35, ln, T_SMALL, GREEN, 600, "middle")
    s.line(686, GY, 686, GY + 14, GREEN, 3.6)
    for i, ww in enumerate((42, 28, 16)):
        s.line(686 - ww / 2, GY + 18 + i * 8, 686 + ww / 2, GY + 18 + i * 8, GREEN, 3.6)
    for j, ln in enumerate(wrap("বড় ফল্ট কারেন্টে ব্রেকার বা RCCB সঙ্গে সঙ্গে ট্রিপ করে",
                                470, T_SMALL, 600)):
        s.text(892, GY + 70 + j * T_SMALL * 1.35, ln, T_SMALL, "#12523A", 600, "middle")

    s.rect(40, 636, 1120, 58, "#EAF2FA", STEEL, 2, 11)
    s.text(600, 673, "ধাতব বডির প্রতিটি যন্ত্র আর্থ করা বাধ্যতামূলক",
           T_NAME, NAVY, 700, "middle")
    s.fit(694, 24)
    return s.save(f"{OUT}/d14_earthing.svg")


ALL = [d01_causes, d02_shock_path, d04_safety_types, d05_ppe, d06_loto,
       d07_five_rules, d08_safety_signs, d10_rescue, d12_hierarchy,
       d13_dead_test, d14_earthing]

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
