# -*- coding: utf-8 -*-
"""smkit.py — সংক্ষিপ্ত সংস্করণের ছোট লেআউট-সহায়ক।

`pic()`     : একটি ছোট বাস্তব ছবি বাঁয়ে, ডানে তার বর্ণনা — পাশাপাশি। শুধু সাধারণ
              পরিচিতিমূলক ছবির জন্য (যেমন কোনো একটি যন্ত্রের চেহারা), যেখানে
              সূক্ষ্ম হরফ পড়ার দরকার নেই।
`dpic()`    : একটি ডায়াগ্রাম/সংযোগচিত্র/নেমপ্লেট-ছবি পুরো চওড়ায়, নিচে সংক্ষিপ্ত
              ব্যাখ্যা। ডায়াগ্রামের ভেতরের লেখা যে চওড়ায় আঁকা হয়েছিল সেই
              চওড়াতেই বসাতে হবে — সরু বাঁ-কলামে গুঁজে ছোট করলে লেখা পড়া যায় না
              (এই বইয়ের `N × P(pt) / W` নিয়ম)।
`diagram()` : একটি গুরুত্বপূর্ণ ডায়াগ্রাম পুরো চওড়ায়, ক্যাপশনসহ (ব্যাখ্যা ছাড়া)।
"""
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from bookkit import bn, set_run_font, cell_margins, no_split, NAVY, GREY, INK


def _sidebyside(b, path, title, desc, img_cm, size, gap_after):
    b.fig_n += 1
    label = f"চিত্র {bn(b.ch)}.{bn(b.fig_n)}"
    b.figures.append((label, title))
    doc = b.doc
    tw = b.text_width
    lw = Cm(img_cm + 0.5)
    t = doc.add_table(rows=1, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    t.allow_autofit = False
    t.columns[0].width = lw
    t.columns[1].width = tw - lw
    cL, cR = t.cell(0, 0), t.cell(0, 1)
    cL.width = lw
    cR.width = tw - lw
    cell_margins(cL, 70, 70, 40, 130)
    cell_margins(cR, 70, 70, 130, 40)
    pL = cL.paragraphs[0]
    pL.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pL.paragraph_format.space_after = Pt(0)
    pL.paragraph_format.line_spacing = 1.0
    pL.add_run().add_picture(path, width=Cm(img_cm))
    pR = cR.paragraphs[0]
    pR.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pR.paragraph_format.space_after = Pt(3)
    pR.paragraph_format.line_spacing = 1.15
    set_run_font(pR.add_run(label + " · "), size=Pt(9.5), bold=True, color=NAVY)
    set_run_font(pR.add_run(title), size=Pt(size), bold=True, color=NAVY)
    qR = cR.add_paragraph()
    qR.alignment = WD_ALIGN_PARAGRAPH.LEFT
    qR.paragraph_format.space_after = Pt(0)
    qR.paragraph_format.line_spacing = 1.28
    b._rich(qR, desc, Pt(size), False, False, INK)
    no_split(t)
    b.spacer(gap_after)
    return t


def pic(b, path, title, desc, img_cm=5.6, size=10):
    """একটি ছোট বাস্তব ছবি + পাশে বর্ণনা — কেবল সাধারণ পরিচিতিমূলক ছবির জন্য।"""
    return _sidebyside(b, path, title, desc, img_cm, size, gap_after=8)


def pics(b, rows, img_cm=5.6, size=10):
    for path, title, desc in rows:
        pic(b, path, title, desc, img_cm=img_cm, size=size)


def dpic(b, path, title, desc, width_cm=13.2, size=9.5):
    """একটি ডায়াগ্রাম/সংযোগচিত্র/নেমপ্লেট-ছবি — পূর্ণ চওড়ায়, নিচে সংক্ষিপ্ত ব্যাখ্যা।"""
    label = b.figure(path, title, width_cm=width_cm)
    p = b.doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.22
    b._rich(p, desc, Pt(size), False, False, INK)
    return label


def dpics(b, rows, width_cm=13.2, size=9.5):
    for path, title, desc in rows:
        dpic(b, path, title, desc, width_cm=width_cm, size=size)


def diagram(b, path, caption, width_cm=13.2):
    """একটি গুরুত্বপূর্ণ ডায়াগ্রাম — বড় করে, পুরো চওড়ায়।"""
    return b.figure(path, caption, width_cm=width_cm)


# ─────────────────────────────────────────────────────────────────────────────
# সচিত্র সহজ সংস্করণের নিজস্ব সহায়ক — একসাথে অনেকগুলো আসল ছবি, প্রতিটির
# নিচে নাম আর দুই-এক লাইনের সহজ বর্ণনা।  মালামাল চেনানোর কাজে `pic()`-এর
# চেয়ে এটি ভালো: একই পৃষ্ঠায় ছয়-নয়টি জিনিস পাশাপাশি দেখা যায়, তাই
# পাঠক তুলনা করতে পারে।
# ─────────────────────────────────────────────────────────────────────────────

def grid(b, items, cols=3, caption=None, img_cm=3.7, size=8.5, name_size=9.0):
    """items = [(path, নাম, বর্ণনা), …] — সারি সারি টালিতে আসল ছবি।

    প্রতিটি টালিতে উপরে ছবি, তার নিচে গাঢ় নীল হরফে নাম, তারপর সহজ ভাষায়
    এক-দুই লাইনের বর্ণনা।  পুরো গ্রিডটি একটি মাত্র চিত্র হিসেবে নম্বর পায়,
    আর `caption` থাকলে নিচে ধূসর হরফে ক্যাপশন বসে।
    """
    n = len(items)
    rows = (n + cols - 1) // cols
    tw = b.text_width
    colw = int(tw / cols)
    t = b.doc.add_table(rows=rows, cols=cols)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    t.allow_autofit = False
    for r in range(rows):
        for c in range(cols):
            cell = t.cell(r, c)
            cell.width = colw
            cell_margins(cell, 90, 110, 60, 60)
    for idx, (path, name, desc) in enumerate(items):
        cell = t.cell(idx // cols, idx % cols)
        pi = cell.paragraphs[0]
        pi.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pi.paragraph_format.space_after = Pt(3)
        pi.paragraph_format.space_before = Pt(0)
        pi.paragraph_format.line_spacing = 1.0
        pi.add_run().add_picture(path, width=Cm(img_cm))
        pn = cell.add_paragraph()
        pn.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pn.paragraph_format.space_after = Pt(1)
        pn.paragraph_format.line_spacing = 1.1
        set_run_font(pn.add_run(name), size=Pt(name_size), bold=True, color=NAVY)
        if desc:
            pd = cell.add_paragraph()
            pd.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pd.paragraph_format.space_after = Pt(0)
            pd.paragraph_format.line_spacing = 1.22
            b._rich(pd, desc, Pt(size), False, False, INK)
    b.fig_n += 1
    label = f"চিত্র {bn(b.ch)}.{bn(b.fig_n)}"
    if caption:
        cp = b.doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(3)
        cp.paragraph_format.space_after = Pt(10)
        cp.paragraph_format.line_spacing = 1.15
        set_run_font(cp.add_run(label + ": "), size=Pt(9.5), bold=True, color=NAVY)
        set_run_font(cp.add_run(caption), size=Pt(9.5), color=GREY, italic=True)
        b.figures.append((label, caption))
    else:
        b.spacer(8)
    return label
