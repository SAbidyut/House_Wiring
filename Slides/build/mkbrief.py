#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mkbrief.py — the merged brief deck: every chapter's brief=True slides in one file.

Built from the same deck_chNN.py specs as the chapter decks (Deck mode "brief"),
so the two can never disagree.  Adds a cover, a how-to slide, a clickable
contents (2 slides × 14 chapters), PowerPoint sections per chapter and a
closing slide.
"""
import os, uuid, math
from lxml import etree
from pptx.util import Inches
from pptx.oxml.ns import qn
import slidekit as K
from slidekit import P
import build as B


def contents(d, slides, start):
    """Fill a contents slide with chapter tiles [start, start+14)."""
    s = slides
    nums = [n for n in range(start, start + 14) if n in B.TITLES]
    cols, rows = 2, 7
    gap_x, gap_y = 0.35, 0.14
    cw = (K.BW - gap_x) / cols
    ch = (K.BB - K.BY - (rows - 1) * gap_y) / rows
    for i, n in enumerate(nums):
        c, r = i // rows, i % rows
        x, y = K.MX + c * (cw + gap_x), K.BY + r * (ch + gap_y)
        card = d.card(s, x, y, cw, ch, fill=K.ICE, name=f"Contents tile {n}")
        badge = d.badge(s, x + 0.12, y + (ch - 0.5) / 2, 0.5, K.bn2(n), pt=15)
        tb, _ = d.text(s, x + 0.78, y, cw - 0.95, ch, [P(B.TITLES[n], b=True)], pt=17, pt_min=12,
                       color=K.NAVY, anchor="m", name=f"Contents title {n}")
        first = d.chapters[n - 1]["first"] if n - 1 < len(d.chapters) else None
        if first is not None:
            for shp in (card, badge, tb):
                shp.click_action.target_slide = first


def add_sections(d, groups):
    """groups = [(name, [slide, …])] → <p14:sectionLst>."""
    pres = d.prs.part._element
    P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
    ext_lst = pres.find(qn("p:extLst"))
    if ext_lst is None:
        ext_lst = etree.SubElement(pres, qn("p:extLst"))
    ext = etree.SubElement(ext_lst, qn("p:ext"))
    ext.set("uri", "{521415D9-36F7-43E2-AB2F-B90AF26B5E84}")
    sl = etree.SubElement(ext, f"{{{P14}}}sectionLst", nsmap={"p14": P14})
    for name, slides in groups:
        if not slides:
            continue
        sec = etree.SubElement(sl, f"{{{P14}}}section")
        sec.set("name", name)
        sec.set("id", "{" + str(uuid.uuid4()).upper() + "}")
        ids = etree.SubElement(sec, f"{{{P14}}}sldIdLst")
        for s in slides:
            etree.SubElement(ids, f"{{{P14}}}sldId").set("id", str(s.slide_id))


def build(pdf=False):
    K.WARNINGS.clear()
    d = K.Deck("brief")
    d.ch, d.title, d.short = 0, "সংক্ষিপ্ত স্লাইড", "সংক্ষিপ্ত স্লাইড"
    intro = []
    # cover
    s = d._new(dark=True)
    d._title(s, "ইলেকট্রিক্যাল হাউস ওয়্যারিং", x=0.85, y=1.9, w=7.2, h=1.9, pt=50, pt_min=36,
             color=K.WHITE, anchor="t", lines=2)
    d.text(s, 0.85, 1.25, 6, 0.6, [P("সংক্ষিপ্ত প্রশিক্ষণ স্লাইড", b=True)], pt=24, color=K.GOLD)
    d.text(s, 0.85, 3.95, 6.8, 1.1, [P("২৮টি অধ্যায়ের মূল ধারণা, চিত্র, ভিডিও ও সারসংক্ষেপ এক জায়গায়")],
           pt=20, color=K.PALE)
    logo = s.shapes.add_picture(os.path.join(K.BOOK, "assets", "cover", "logo_rapti_light.png"),
                                Inches(0.85), Inches(6.05), Inches(1.75))
    d.text(s, 2.85, 6.08, 5, 0.55, [P("Resonance Automation Professional"), P("Training Institute", c=K.GOLD_L)],
           pt=13, color=K.NEARW, sa_ratio=0.1)
    d.picture(s, "cover/cover.png", 8.6, 0.6, 4.1, 6.3, frame=False, round_photo=False)
    intro.append(s)
    # how to use
    s = d._light("এই স্লাইড কীভাবে ব্যবহার করবেন", tag="সংক্ষিপ্ত স্লাইড  ·  ব্যবহারবিধি")
    d.chapters.clear()
    intro.append(s)
    cards = [
        dict(icon="book", head="প্রতিটি অধ্যায় এক নজরে",
             body="অধ্যায়ের পরিচিতি, মূল ধারণা ও চিত্র, একটি ভিডিও এবং মূল কথা"),
        dict(icon="video", head="ভিডিওসহ শেখা",
             body="ভিডিও কার্ডের থাম্বনেইলে ক্লিক করলে ব্রাউজারে ভিডিও খোলে; মোবাইলে QR কোড স্ক্যান করুন"),
        dict(icon="list", head="ক্লিকযোগ্য সূচিপত্র",
             body="সূচিপত্রের যেকোনো অধ্যায়ে ক্লিক করলে সেখানে চলে যাবে; প্রতিটি অধ্যায়ের শুরু থেকে আবার সূচিপত্রে ফেরা যায়"),
        dict(icon="layers", head="পূর্ণাঙ্গ স্লাইড আলাদা",
             body="প্রতিটি অধ্যায়ের বিস্তারিত স্লাইড (উদাহরণ, কুইজ, পরিভাষাসহ) 'অধ্যায়ভিত্তিক স্লাইড' ফোল্ডারে"),
    ]
    # draw the four cards on the existing slide
    def draw_cards(s):
        cw = (K.BW - 0.3) / 2
        chh = (K.BB - K.BY - 0.3) / 2
        for i, c in enumerate(cards):
            x = K.MX + (i % 2) * (cw + 0.3)
            y = K.BY + (i // 2) * (chh + 0.3)
            d.card(s, x, y, cw, chh, fill=K.ICE)
            d.icon_badge(s, x + 0.3, y + 0.3, 0.75, c["icon"])
            d.text(s, x + 1.3, y + 0.25, cw - 1.55, chh - 0.5,
                   [P(c["head"], b=True, c=K.NAVY, rel=1.12, sa=6), P(c["body"])], pt=20, pt_min=14,
                   anchor="m", sa_ratio=0.3)
    draw_cards(s)
    # contents (filled after the chapters exist)
    toc = [d._light("সূচিপত্র (অধ্যায় ১–১৪)", tag="সংক্ষিপ্ত স্লাইড  ·  সূচিপত্র"),
           d._light("সূচিপত্র (অধ্যায় ১৫–২৮)", tag="সংক্ষিপ্ত স্লাইড  ·  সূচিপত্র")]
    intro += toc
    d.toc_slide = toc[0]
    d.chapters.clear()
    for n in range(1, 29):
        if not os.path.exists(os.path.join(K.HERE, f"deck_ch{n:02d}.py")):
            K.warn(f"brief: deck_ch{n:02d}.py missing")
            d.chapters.append({"n": n, "title": B.TITLES[n], "first": None, "slides": []})
            continue
        d.toc_slide = toc[0] if n <= 14 else toc[1]
        B.run_chapter(d, n)
    contents(d, toc[0], 1)
    contents(d, toc[1], 15)
    # closing
    d.ch, d.title = 28, "সমাপ্তি"
    s = d._new(dark=True, bg_variant="b")
    d._title(s, "ধন্যবাদ", x=0.85, y=1.55, w=11, h=1.1, pt=48, color=K.WHITE, anchor="t")
    d.text(s, 0.85, 2.8, 11, 1.4,
           [P("নিরাপদে কাজ করুন; প্রতিটি সংযোগ শেষে টেস্ট করুন।", c=K.GOLD_L, b=True),
            P("বিস্তারিত পাঠ: ইলেকট্রিক্যাল হাউস ওয়্যারিং (পূর্ণাঙ্গ বই) ও অধ্যায়ভিত্তিক স্লাইড", c=K.NEARW)],
           pt=22, sa_ratio=0.4)
    logo = s.shapes.add_picture(os.path.join(K.BOOK, "assets", "cover", "logo_rapti_light.png"),
                                Inches(0.85), Inches(4.75), Inches(2.3))
    d.text(s, 3.45, 4.7, 8.5, 1.0,
           [P("Resonance Automation Professional Training Institute", b=True, c=K.WHITE),
            P("rapti.net  ·  হটলাইন 01617-345534  ·  raptibd@gmail.com", c=K.PALE)], pt=16, sa_ratio=0.3)
    groups = [("সূচনা", intro)] + \
             [(f"অধ্যায় {K.bn2(c['n'])}: {c['title']}", c["slides"]) for c in d.chapters] + \
             [("সমাপ্তি", [s])]
    add_sections(d, groups)
    d.ch = 0
    out = d.save(B.BRIEF)
    print(f"✓ brief: {len(d.prs.slides)} slides, {os.path.getsize(out)/1e6:.1f} MB — {len(K.WARNINGS)} warnings")
    if pdf:
        B.to_pdf(out)
    return out


if __name__ == "__main__":
    import sys
    build(pdf="--pdf" in sys.argv)
