# -*- coding: utf-8 -*-
"""dia_digest_cover.py — সংক্ষিপ্ত সংস্করণের প্রচ্ছদ।

`dia_cover.py`-এর হুবহু নকশা; শুধু তিনটি লাইন বদলেছে যাতে ফাইলটি পূর্ণাঙ্গ
বই থেকে আলাদা চেনা যায় —
  · উপ-শিরোনাম:  "গুরুত্বপূর্ণ বিষয়ভিত্তিক সংক্ষিপ্ত সংস্করণ"
  · চিপ:        "সংক্ষিপ্ত সংস্করণ · ২০২৬"
  · আউটপুট:      diagrams/cover/cover_digest.svg
"""
import os
from svgkit import SVG, tw
from dia_cover import (_sheet, _motif, _divider, W, H, CX, IMG,
                       GOLD, GOLD_L, WHITE, NEARW, PALE, PALE2, SUB, NAVY_D, LATIN)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "diagrams", "cover")


def cover_digest():
    s = SVG(W, H, bg=NAVY_D)
    _sheet(s)
    _motif(s)

    lw, lh = 250.0, 91.3
    s.image(CX - lw / 2, 100, lw, lh, os.path.join(IMG, "logo_rapti_light.png"))
    s.text(CX, 252, "রেজোন্যান্স অটোমেশন প্রফেশনাল ট্রেনিং ইনস্টিটিউট",
           29, NEARW, 700, "middle")
    s.text(CX, 284, "RESONANCE  AUTOMATION  PROFESSIONAL  TRAINING  INSTITUTE",
           15, PALE2, 500, "middle", family=LATIN, ls=2.8)
    _divider(s, 326, 290)

    s.text(CX, 424, "প্রশিক্ষণ পাঠ্যপুস্তক", 25, GOLD_L, 700, "middle", ls=13)
    s.text(CX, 564, "ইলেকট্রিক্যাল", 104, WHITE, 700, "middle")
    s.text(CX, 696, "হাউস ওয়্যারিং", 104, WHITE, 700, "middle")
    s.line(CX - 75, 754, CX + 75, 754, GOLD, 3)
    s.text(CX, 810, "ELECTRICAL HOUSE WIRING", 24, PALE, 300, "middle",
           family=LATIN, ls=8)
    s.text(CX, 872, "গুরুত্বপূর্ণ বিষয়ভিত্তিক সংক্ষিপ্ত সংস্করণ",
           25, SUB, 400, "middle")

    chip = "সংক্ষিপ্ত সংস্করণ  ·  ২০২৬"
    cwid = tw(chip, 22, 600) + 80
    s.rect(CX - cwid / 2, 910, cwid, 52, "none", GOLD, 1.5, 26, opacity=0.55)
    s.text(CX, 943, chip, 22, GOLD_L, 600, "middle")

    _divider(s, 1448, 340, sw=1.0, op=0.45)
    s.text(CX, 1508, "অ্যাডমিশন হটলাইন   ০১৬১৭-৩৪৫৫৩৪", 26, WHITE, 700, "middle")
    s.text(CX, 1552, "raptibd@gmail.com     ·     rapti.net", 21, PALE, 400,
           "middle", family=LATIN)
    s.text(CX, 1594,
           "২১০১, ভুইঘর, রূপায়ণ টাউন, গেট-১ সংলগ্ন, ফতুল্লা, নারায়ণগঞ্জ-১৪২০",
           19, PALE2, 400, "middle")

    return s.save(f"{OUT}/cover_digest.svg")


ALL = [cover_digest]

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
