# -*- coding: utf-8 -*-
"""অধ্যায় ৮ — মেজারিং ইন্সট্রুমেন্টস : ডায়াগ্রাম।

পরিমাপের সার্কিটগুলো RAPTI-র নিজস্ব `Circuit Diagram.pptx` (স্লাইড ৩০–৩৩)
থেকে হুবহু বসানো — নতুন করে আঁকা নয়। মিটারের অংশ পরিচিতির ছবিগুলোতেও
সোর্সের মিটার-ফেস বসিয়ে তার চারপাশে বাংলা লেবেল দেওয়া হয়েছে।
"""
import os
from svgkit import (SVG, NAVY, STEEL, LIGHT, RED, REDBG, GREEN, GREENBG,
                    AMBER, AMBERBG, GREY, LINE, INK, wrap, tw)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams", "ch08")
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "ch08")

T_TITLE = 34
T_NODE = 28
T_NAME = 24.5
T_BODY = 21.5
T_SMALL = 20
T_CALL = 26          # অংশ-পরিচিতির লেবেল — ছবিটি ছোট বসে বলে বড় টাইপ
LH = 1.42

SYM = "#12324D"
SW = 3.2


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


def sheet1(fname, title, img, note, ph=430, panel_title=None):
    """একটি সোর্স-ছবির শিট — শিরোনাম, একক প্যানেল ও নিচে টীকা।"""
    s = SVG(1240, 100 + ph + 130)
    s.title(title, T_TITLE)
    top = 96
    panel(s, 46, top, 1148, ph, panel_title or "সংযোগ ডায়াগ্রাম", STEEL)
    s.image_fit(70, top + 62, 1100, ph - 84, f"{IMG}/{img}", 8)
    y = note_strip(s, top + ph + 22, note)
    s.fit(y, 22)
    return s.save(f"{OUT}/{fname}.svg")


def callout(s, x, y, text, tx, ty, anchor="end", size=T_CALL, col=NAVY):
    """লেবেল ও তার লিডার লাইন — লেখা সবসময় ছবির বাইরে থাকে।"""
    s.text(x, y + size * 0.32, text, size, col, 700, anchor)
    x0 = x + 10 if anchor == "end" else x - 10
    s.path(f"M {x0} {y} L {tx} {ty}", STEEL, 2.2)
    s.circle(tx, ty, 5, STEEL)


# ═══════════════════════════════════════════════════════════════════════
def d01_classification():
    """পরিমাপক যন্ত্রের শ্রেণিবিভাগ।"""
    s = SVG(1240, 760)
    s.title("পরিমাপক যন্ত্রের শ্রেণিবিভাগ", T_TITLE)

    rx, ry, rw, rh = s.box_auto(620, 84, "পরিমাপক যন্ত্র (Measuring Instrument)",
                                T_NODE, fill=NAVY, stroke=NAVY, tcolor="#FFFFFF",
                                pad_x=34, pad_y=14)
    bus = ry + rh + 34
    s.path(f"M 620 {ry+rh} L 620 {bus}", STEEL, 2.6)
    LX, RX = 320, 920
    s.path(f"M {LX} {bus} L {RX} {bus}", STEEL, 2.6)

    cols = [(LX, "অ্যাবসলিউট ইনস্ট্রুমেন্ট", STEEL,
             ["নিজের ভেতরের নির্দিষ্ট মান থেকেই ফল দেয়, তুলনার দরকার হয় না",
              "উদাহরণ: ট্যানজেন্ট গ্যালভানোমিটার, অ্যাবসলিউট ইলেকট্রোমিটার",
              "মূলত গবেষণাগারে মানক যন্ত্র হিসেবে ব্যবহৃত"]),
            (RX, "সেকেন্ডারি ইনস্ট্রুমেন্ট", GREEN,
             ["ইন্ডিকেটিং — তাৎক্ষণিক মান দেখায় (অ্যামিটার, ভোল্টমিটার, ওয়াটমিটার)",
              "রেকর্ডিং — সময়ের সঙ্গে মান কাগজে এঁকে রাখে",
              "ইন্টিগ্রেটিং — নির্দিষ্ট সময়ের মোট পরিমাণ যোগ করে দেখায় (এনার্জি মিটার)"])]

    bottom = 0
    for cx, head, col, leaves in cols:
        s.path(f"M {cx} {bus} L {cx} {bus+28}", STEEL, 2.6)
        gx, gy, gw, gh = s.box_auto(cx, bus + 28, head, T_NAME, fill=col,
                                    stroke=col, tcolor="#FFFFFF",
                                    pad_x=26, pad_y=12, min_w=500)
        y = gy + gh
        for leaf in leaves:
            s.path(f"M {cx} {y} L {cx} {y+24}", LINE, 2.4)
            lx, ly, lw, lh = s.box_auto(cx, y + 24, leaf, T_BODY,
                                        fill="#F7FAFC", stroke=LINE,
                                        tcolor=INK, weight=600, max_w=430,
                                        pad_x=20, pad_y=13, min_w=500)
            y = ly + lh
        bottom = max(bottom, y)

    y = note_strip(s, bottom + 26,
                   "হাউস ওয়্যারিংয়ের কাজে ব্যবহৃত প্রায় সব মিটারই সেকেন্ডারি "
                   "ইন্ডিকেটিং ইনস্ট্রুমেন্ট")
    s.fit(y, 24)
    return s.save(f"{OUT}/d01_classification.svg")


def d02_multimeter_parts():
    """ডিজিটাল মাল্টিমিটারের অংশ পরিচিতি — সোর্সের মিটার-ফেসে বাংলা লেবেল।"""
    s = SVG(1240, 900)
    s.title("ডিজিটাল মাল্টিমিটারের অংশ পরিচিতি", T_TITLE)

    IW, IH = 264, 459                      # 641 × 1115 এর অনুপাত
    x0, y0 = 488, 100
    s.rect(x0 - 16, y0 - 16, IW + 32, IH + 32, "#FCFDFE", LINE, 1.8, 14)
    s.image(x0, y0, IW, IH, f"{IMG}/m_multimeter_face.png")

    callout(s, 430, y0 + 0.17 * IH, "ডিসপ্লে — মান ও AC/DC দেখায়",
            x0 + 6, y0 + 0.17 * IH)
    callout(s, 430, y0 + 0.32 * IH, "অন/অফ বোতাম", x0 + 24, y0 + 0.325 * IH)
    callout(s, 430, y0 + 0.60 * IH, "ভোল্টেজ পরিমাপের অবস্থান",
            x0 + 30, y0 + 0.635 * IH)
    callout(s, 810, y0 + 0.30 * IH, "রেঞ্জ সিলেক্টর নব",
            x0 + IW - 40, y0 + 0.50 * IH, anchor="start")
    callout(s, 810, y0 + 0.62 * IH, "কারেন্ট পরিমাপের অবস্থান",
            x0 + IW - 26, y0 + 0.635 * IH, anchor="start")

    ports = [(0.22, 424, "A পোর্ট"), (0.50, 620, "com পোর্ট"),
             (0.78, 816, "Ω/V পোর্ট")]
    for fx, lx, name in ports:
        px = x0 + fx * IW
        s.path(f"M {px} {y0+IH+14} L {lx} {y0+IH+44}", STEEL, 2.2)
        s.circle(px, y0 + IH + 14, 5, STEEL)
        s.text(lx, y0 + IH + 70, name, T_CALL, NAVY, 700, "middle")

    y = note_strip(s, y0 + IH + 96,
                   "কালো প্রোব সবসময় com-এ; ভোল্ট ও রোধে লাল প্রোব Ω/V পোর্টে, "
                   "কারেন্টে লাল প্রোব A পোর্টে", size=T_CALL)
    y = note_strip(s, y + 12,
                   "সিলেক্টরের অবস্থান — V(DC) ডিসি ভোল্ট, V(AC) এসি ভোল্ট, "
                   "A(DC) ডিসি কারেন্ট, A(AC) এসি কারেন্ট, Ω রোধ",
                   fill="#FFF6E5", stroke=AMBER, tcolor="#7A5200", size=T_CALL)
    s.fit(y, 24)
    return s.save(f"{OUT}/d02_multimeter_parts.svg")


def d03_clamp_parts():
    """ক্ল্যাম্প মিটারের অংশ পরিচিতি।"""
    s = SVG(1240, 900)
    s.title("ক্ল্যাম্প মিটারের অংশ পরিচিতি", T_TITLE)

    IW, IH = 233, 490                      # 697 × 1466 এর অনুপাত
    x0, y0 = 504, 100
    s.rect(x0 - 16, y0 - 16, IW + 32, IH + 32, "#FCFDFE", LINE, 1.8, 14)
    s.image(x0, y0, IW, IH, f"{IMG}/m_clamp_face.png")

    callout(s, 462, y0 + 0.10 * IH, "ক্ল্যাম্প জ — তারকে ঘিরে ধরে",
            x0 + 0.32 * IW, y0 + 0.10 * IH)
    callout(s, 462, y0 + 0.40 * IH, "ট্রিগার — চোয়াল খোলার লিভার",
            x0 + 0.14 * IW, y0 + 0.40 * IH)
    callout(s, 462, y0 + 0.62 * IH, "টর্চ ও হোল্ড বোতাম",
            x0 + 0.42 * IW, y0 + 0.615 * IH)
    callout(s, 462, y0 + 0.76 * IH, "ডিসপ্লে", x0 + 0.32 * IW, y0 + 0.74 * IH)
    callout(s, 780, y0 + 0.30 * IH, "রেঞ্জ সিলেক্টর নব",
            x0 + 0.84 * IW, y0 + 0.40 * IH, anchor="start")
    callout(s, 780, y0 + 0.88 * IH, "COM ও V/Ω পোর্ট",
            x0 + 0.62 * IW, y0 + 0.90 * IH, anchor="start")

    y = note_strip(s, y0 + IH + 34,
                   "ক্ল্যাম্প মিটারে বর্তনী কাটতে হয় না — চোয়ালের ভেতর কেবল "
                   "একটিমাত্র তার রেখে কারেন্ট পড়া যায়", size=T_CALL)
    y = note_strip(s, y + 12,
                   "সিলেক্টরের অবস্থান — A(AC) এসি কারেন্ট, V(AC) এসি ভোল্ট, "
                   "V(DC) ডিসি ভোল্ট, Ω রোধ ও কন্টিনিউইটি",
                   fill="#FFF6E5", stroke=AMBER, tcolor="#7A5200", size=T_CALL)
    s.fit(y, 24)
    return s.save(f"{OUT}/d03_clamp_parts.svg")


def d04_voltage():
    return sheet1("d04_voltage", "ভোল্টমিটার দিয়ে ভোল্টেজ পরিমাপ",
                  "d04_volt_ac.png",
                  "মিটার লোডের দুই প্রান্তে প্যারালালে; সিলেক্টর V(AC)-তে, "
                  "সরবরাহ চালু অবস্থায় পাঠ নেওয়া হয়",
                  ph=420, panel_title="এসি ভোল্টেজ পরিমাপ")


def d05_current_series():
    return sheet1("d05_current_series", "মাল্টিমিটার দিয়ে কারেন্ট পরিমাপ",
                  "d05_amp_series.png",
                  "বর্তনী কেটে মিটারকে লোডের সঙ্গে সিরিজে বসাতে হয়; "
                  "লাল প্রোব A পোর্টে, সিলেক্টর A-তে",
                  ph=430, panel_title="সিরিজে অ্যামিটার সংযোগ")


def d06_current_clamp():
    return sheet1("d06_current_clamp", "ক্ল্যাম্প মিটার দিয়ে কারেন্ট পরিমাপ",
                  "d06_amp_clamp.png",
                  "বর্তনী কাটার দরকার নেই — চোয়ালের ভেতর কেবল ফেজ তারটি "
                  "রেখে সরাসরি পাঠ নেওয়া যায়",
                  ph=440, panel_title="ক্ল্যাম্প মিটারে কারেন্ট পরিমাপ")


def d07_resistance():
    return sheet1("d07_resistance", "মাল্টিমিটার দিয়ে রেজিস্ট্যান্স পরিমাপ",
                  "d07_resistance.png",
                  "সুইচ খোলা — সরবরাহ বন্ধ রেখে উপাদানের দুই প্রান্তে প্রোব "
                  "ধরে Ω মোডে পাঠ নিতে হয়",
                  ph=420, panel_title="রেজিস্ট্যান্স পরিমাপ")


ALL = [d01_classification, d02_multimeter_parts, d03_clamp_parts,
       d04_voltage, d05_current_series, d06_current_clamp, d07_resistance]

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
