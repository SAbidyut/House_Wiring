# -*- coding: utf-8 -*-
"""
mkdigest.py — assemble the condensed সংক্ষিপ্ত-NN chapters into one ~150-page book.

Identical machinery to mkbook.py (cover section, imprint, clickable সূচিপত্র,
book-wide footer, continuous page numbers) — only the source glob, the cover
art, the imprint copy and the output filename differ.

Run:   python dia_digest_cover.py
       python render.py 'diagrams/cover/cover_digest.svg'
       python mkdigest.py [--pdf]
Out:   ../ইলেকট্রিক্যাল হাউস ওয়্যারিং — সংক্ষিপ্ত সংস্করণ (গুরুত্বপূর্ণ বিষয়সমূহ).docx
"""
import os, re, glob, sys, subprocess, tempfile, shutil
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import (WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT,
                            WD_TAB_LEADER)
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml
from docxcompose.composer import Composer

from bookkit import (Book, bn, set_run_font, para_border, cell_shade,
                     cell_margins, cell_borders, field,
                     NAVY, STEEL, GREY, INK, NAVY_HEX, STEEL_HEX)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "out")
COVER_PNG = os.path.join(HERE, "diagrams", "cover", "cover_digest.png")
DEST = os.path.abspath(os.path.join(
    HERE, "..", "ইলেকট্রিক্যাল হাউস ওয়্যারিং — সংক্ষিপ্ত সংস্করণ (গুরুত্বপূর্ণ বিষয়সমূহ).docx"))

# ── RAPTI — from rapti.net (about.php / contact.php), Aug 2026 ──────────────
INST_BN  = "রেজোন্যান্স অটোমেশন প্রফেশনাল ট্রেনিং ইনস্টিটিউট"
INST_EN  = "R E S O N A N C E   A U T O M A T I O N   P R O F E S S I O N A L   T R A I N I N G   I N S T I T U T E"
FOOT_L   = "Resonance Automation"
FOOT_R   = "01617-345534"
HOTLINE  = "০১৬১৭-৩৪৫৫৩৪"
PHONES   = "০১৬১৭-৩৪৫৫৩৪ · ০১৬৮৫-৯৫৩২০৪ · ০১৭৬৬-২২১৭৩৩"
WHATSAPP = "+৮৮০ ১৬১৭-৩৪৫৫৩৪"
EMAIL    = "raptibd@gmail.com"
WEB      = "rapti.net"
FB       = "facebook.com/resonanceautomationbd"
ADDR_BN  = "২১০১, ভুইঘর, রূপায়ণ টাউন, গেট-১ সংলগ্ন, ফতুল্লা, নারায়ণগঞ্জ-১৪২০"
EDITION  = "সংক্ষিপ্ত সংস্করণ · সেপ্টেম্বর ২০২৬"
BN2A     = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")


def chapter_list():
    rows = []
    for f in glob.glob(os.path.join(OUT, "সংক্ষিপ্ত-*.docx")):
        base = os.path.basename(f)[:-5]
        if " — " not in base:
            continue
        left, title = base.split(" — ", 1)
        num = left.split("-", 1)[1].strip()
        try:
            n = int(num.translate(BN2A))
        except ValueError:
            continue
        if 1 <= n <= 28:
            rows.append((n, title.strip(), f))
    rows.sort(key=lambda r: r[0])
    return rows


# ── front matter ──────────────────────────────────────────────────────────
def _link(p, anchor, parts):
    """Append an internal hyperlink (to a bookmark) built from styled runs."""
    hl = OxmlElement("w:hyperlink")
    hl.set(qn("w:anchor"), anchor)
    for text, size, color, bold in parts:
        r = OxmlElement("w:r")
        rPr = OxmlElement("w:rPr")
        rf = OxmlElement("w:rFonts")
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), "Kalpurush")
        rPr.append(rf)
        for tag in ("w:sz", "w:szCs"):
            e = OxmlElement(tag); e.set(qn("w:val"), str(int(size * 2))); rPr.append(e)
        if bold:
            rPr.append(OxmlElement("w:b")); rPr.append(OxmlElement("w:bCs"))
        col = OxmlElement("w:color"); col.set(qn("w:val"), color); rPr.append(col)
        r.append(rPr)
        t = OxmlElement("w:t"); t.set(qn("xml:space"), "preserve"); t.text = text
        r.append(t)
        hl.append(r)
    p._p.append(hl)


def full_page_picture(doc, png, page_w, page_h):
    """Drop a picture on the page as a page-anchored, behind-text image.

    An *inline* image cannot bleed to the paper edge: its line box carries
    leading, so a page-height picture spills onto a second page. Word's own
    answer is a floating anchor positioned from the page corner, which takes
    no room in the text flow at all — that is what this builds, by rewriting
    the `wp:inline` python-docx produces into a `wp:anchor`.
    """
    WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
    A = "http://schemas.openxmlformats.org/drawingml/2006/main"
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    run = p.add_run()
    run.add_picture(png, width=page_w, height=page_h)
    set_run_font(run, size=Pt(1))

    from lxml import etree
    inline = run._r.find(qn("w:drawing"))[0]
    gx = etree.tostring(inline.find("{%s}graphic" % A)).decode("utf-8")
    anchor = parse_xml(
        '<wp:anchor xmlns:wp="%s" xmlns:a="%s" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
        'distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="1" '
        'behindDoc="1" locked="0" layoutInCell="1" allowOverlap="1">'
        '<wp:simplePos x="0" y="0"/>'
        '<wp:positionH relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionH>'
        '<wp:positionV relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionV>'
        '<wp:extent cx="%d" cy="%d"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:wrapNone/><wp:docPr id="9001" name="cover"/><wp:cNvGraphicFramePr/>%s'
        '</wp:anchor>' % (WP, A, int(page_w), int(page_h), gx))
    inline.getparent().replace(inline, anchor)
    return p


def chapter_sections(path):
    """Return the chapter's in-book section headings in document order —
    the `b.h1()` paragraphs (`১.১  …`), text kept whole (number + title).
    Same filter `inject_section_bookmarks()` uses, so the k-th here is the
    k-th there and the সূচিপত্র PAGEREF anchors line up."""
    doc = Document(path)
    out = []
    for p in doc.paragraphs:
        if p.style and p.style.name == "Heading 1" and p.text.strip():
            out.append(p.text.strip())
    return out


def build_front(chaps, toc_tree):
    b = Book(0, "front")
    d = b.doc

    # ---------------- COVER — its own borderless section ----------------
    S0 = d.sections[0]
    PW, PH = S0.page_width, S0.page_height
    S0.left_margin = S0.right_margin = Cm(0)
    S0.top_margin = S0.bottom_margin = Cm(0)
    S0.header_distance = S0.footer_distance = Cm(0)
    if not os.path.exists(COVER_PNG):
        raise SystemExit("cover art missing — run:  python dia_cover.py  &&  "
                         "python render.py 'diagrams/cover/cover.svg'")
    full_page_picture(d, COVER_PNG, PW, PH)

    # everything after the cover lives in a normal-margin section
    S = d.add_section(WD_SECTION.NEW_PAGE)
    S.page_width, S.page_height = PW, PH
    S.top_margin, S.bottom_margin = Cm(2.2), Cm(2.0)
    S.left_margin, S.right_margin = Cm(2.4), Cm(2.0)
    S.header_distance, S.footer_distance = Cm(1.1), Cm(1.0)
    S.different_first_page_header_footer = False
    b.section = S
    cw = PW - S.left_margin - S.right_margin

    # One running header line, three columns:
    #   book title (left)  ·  chapter number + title (centre)  ·  rapti.net (right)
    #
    # The paragraph MUST be style "Normal", not the built-in "Header".
    # "Header" carries its own tab stops (centre @4680, right @9360 twips)
    # and OOXML *merges* a style's tabs with the paragraph's own — so the
    # first \t landed on the style's centre stop and the second on our
    # centre stop, leaving `rapti.net` floating mid-page instead of at the
    # right margin. `tab_stops.clear_all()` only clears paragraph-level
    # stops, never a style's; changing the style is what actually fixes it.
    S.header.is_linked_to_previous = False
    hp = S.header.paragraphs[0]
    hp.text = ""
    hp.style = "Normal"
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hp.paragraph_format.space_before = Pt(0)
    hp.paragraph_format.space_after = Pt(0)
    hp.paragraph_format.line_spacing = 1.0
    hp.paragraph_format.tab_stops.clear_all()
    hp.paragraph_format.tab_stops.add_tab_stop(int(cw / 2), WD_TAB_ALIGNMENT.CENTER)
    hp.paragraph_format.tab_stops.add_tab_stop(cw, WD_TAB_ALIGNMENT.RIGHT)
    set_run_font(hp.add_run("ইলেকট্রিক্যাল হাউস ওয়্যারিং"), size=Pt(8.5), color=GREY)
    hp.add_run("\t")
    # STYLEREF tracks the nearest preceding "RaptiChapterTitle" paragraph
    # (the navy title block chapter_opener() stamps once per chapter, with a
    # hidden "অধ্যায় N · " prefix) — so this cell shows the number and title
    # of whichever chapter's pages the reader is on, updating per page,
    # without needing a header per section (docxcompose drops per-chapter
    # sectPr on append, so a real per-section header is not an option here —
    # see the mkbook.py notes in CLAUDE.md).
    for rr in field(hp, 'STYLEREF "RaptiChapterTitle" \\* MERGEFORMAT',
                     "অধ্যায় ১ · কর্মক্ষেত্রে নিরাপত্তা"):
        set_run_font(rr, size=Pt(8.5), color=GREY, bold=True)
    hp.add_run("\t")
    set_run_font(hp.add_run(WEB), size=Pt(8.5), color=GREY)
    para_border(hp, "bottom", color="C9D3DC", sz=6, space=3)

    # ---------------- IMPRINT ----------------
    def head(text):
        q = d.add_paragraph(); q.alignment = WD_ALIGN_PARAGRAPH.LEFT
        q.paragraph_format.space_before = Pt(16); q.paragraph_format.space_after = Pt(7)
        set_run_font(q.add_run(text), size=Pt(15), bold=True, color=NAVY)
        para_border(q, "bottom", color="C9D3DC", sz=6, space=3)

    def body(text):
        q = d.add_paragraph(); q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        q.paragraph_format.space_after = Pt(7); q.paragraph_format.line_spacing = 1.3
        set_run_font(q.add_run(text), size=Pt(11), color=INK)

    def kv(k, v):
        q = d.add_paragraph(); q.alignment = WD_ALIGN_PARAGRAPH.LEFT
        q.paragraph_format.space_after = Pt(3)
        q.paragraph_format.left_indent = Cm(0.3)
        set_run_font(q.add_run(k + "  "), size=Pt(10.5), bold=True, color=STEEL)
        set_run_font(q.add_run(v), size=Pt(10.5), color=INK)

    b.spacer(10)
    head("বইটি সম্পর্কে")
    body("এটি RAPTI-এর ‘ইলেকট্রিক্যাল হাউস ওয়্যারিং’ কোর্সের পূর্ণাঙ্গ "
         "পাঠ্যপুস্তকের সংক্ষিপ্ত সংস্করণ। পূর্ণাঙ্গ বইয়ের ২৮টি অধ্যায়ের "
         "প্রতিটি এখানেও একই নম্বরে ও শিরোনামে আছে, তবে কেবল সবচেয়ে দরকারি "
         "অংশটুকু — মূল সংজ্ঞা, মাপ, মান, নিরাপত্তা বিধি, বাস্তব ছবি ও "
         "কয়েকটি জরুরি ডায়াগ্রাম। দ্রুত পুনরালোচনা ও কর্মক্ষেত্রে সঙ্গে "
         "রাখার জন্য তৈরি।")
    body("প্রতিটি অধ্যায়ের শেষে একটি সংক্ষিপ্ত সারসংক্ষেপ আছে; গণনানির্ভর "
         "অধ্যায়ে সমাধানকৃত উদাহরণ রাখা হয়েছে। প্রতিটি বাস্তব ছবির পাশে তার "
         "বর্ণনা দেওয়া, আর কেবল জরুরি ডায়াগ্রামগুলো বড় করে রাখা হয়েছে। কোনো "
         "বহুনির্বাচনী প্রশ্ন, অনুশীলনী বা পারিভাষিক শব্দকোষ এই সংস্করণে নেই — "
         "সেগুলোর জন্য পূর্ণাঙ্গ বই দেখুন। নিরাপত্তা বিধি ও হিসাবে IEC, BNBC ও "
         "BS মান অনুসরণ করা হয়েছে; চিত্র ও সারণির নম্বর পূর্ণাঙ্গ বইয়ের সঙ্গে "
         "মিলিয়ে রাখা।")

    head("প্রকাশনা ও যোগাযোগ")
    kv("বইয়ের নাম", "ইলেকট্রিক্যাল হাউস ওয়্যারিং — সংক্ষিপ্ত সংস্করণ")
    kv("সংস্করণ", f"{EDITION}  —  অধ্যায় ১–২৮ (গুরুত্বপূর্ণ বিষয়সমূহ)")
    kv("প্রণয়ন ও প্রকাশনা", f"{INST_BN} (RAPTI)")
    kv("ঠিকানা", ADDR_BN)
    kv("হটলাইন", PHONES)
    kv("হোয়াটসঅ্যাপ", WHATSAPP)
    kv("ইমেইল", EMAIL)
    kv("ওয়েবসাইট", WEB)
    kv("ফেসবুক", FB)
    kv("কোর্স", "হাউস ওয়্যারিং (ইলেকট্রিক্যাল) — অনলাইন ও অফলাইন")

    head("স্বত্ব")
    body("সর্বস্বত্ব © ২০২৬ রেজোন্যান্স অটোমেশন প্রফেশনাল ট্রেনিং ইনস্টিটিউট "
         "(RAPTI)। প্রতিষ্ঠানের লিখিত অনুমতি ছাড়া এই বইয়ের কোনো অংশ যেকোনো "
         "মাধ্যমে পুনরুৎপাদন, অনুলিপি বা বিতরণ করা যাবে না। এটি মূলত RAPTI-এর "
         "প্রশিক্ষণার্থীদের জন্য প্রস্তুত অভ্যন্তরীণ প্রশিক্ষণ উপকরণ।")
    b.page_break()

    # ---------------- সূচিপত্র ----------------
    hp = d.add_paragraph(); hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hp.paragraph_format.space_before = Pt(2); hp.paragraph_format.space_after = Pt(4)
    set_run_font(hp.add_run("সূচিপত্র"), size=Pt(20), bold=True, color=NAVY)
    para_border(hp, "bottom", color=NAVY_HEX, sz=10, space=4)

    cap = d.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    cap.paragraph_format.space_before = Pt(2); cap.paragraph_format.space_after = Pt(9)
    set_run_font(cap.add_run("শিরোনামে ক্লিক করলে সরাসরি সেই অধ্যায়ে বা অংশে যাওয়া যাবে।"),
                 size=Pt(9), italic=True, color=GREY)

    sec_by_n = {n: secs for n, _t, secs in toc_tree}
    for n, title, _ in chaps:
        # ── chapter line ──────────────────────────────────────────────
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.06
        ts = p.paragraph_format.tab_stops
        ts.add_tab_stop(cw, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        _link(p, f"_ch{n:02d}", [
            (f"অধ্যায়  {bn('%02d' % n)}    ", 11.5, STEEL_HEX, True),
            (title, 11.5, NAVY_HEX, False),
        ])
        p.add_run("\t")
        for rr in field(p, f" PAGEREF _ch{n:02d} \\h ", "০"):
            set_run_font(rr, size=Pt(11), color=NAVY, bold=True)

        # ── one line per in-chapter section ───────────────────────────
        for k, sec in enumerate(sec_by_n.get(n, []), start=1):
            q = d.add_paragraph()
            q.alignment = WD_ALIGN_PARAGRAPH.LEFT
            q.paragraph_format.space_after = Pt(2)
            q.paragraph_format.line_spacing = 1.04
            q.paragraph_format.left_indent = Cm(0.8)
            qs = q.paragraph_format.tab_stops
            qs.add_tab_stop(cw, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
            _link(q, f"_ch{n:02d}_s{k}", [(sec, 10, "1A1A1A", False)])
            q.add_run("\t")
            for rr in field(q, f" PAGEREF _ch{n:02d}_s{k} \\h ", "০"):
                set_run_font(rr, size=Pt(9.5), color=STEEL, bold=False)

    front_path = os.path.join(OUT, "_front.docx")
    b.save(front_path)
    return front_path


# ── collapse a chapter's trailing spacer paragraphs ─────────────────────
def shrink_trailing_para(doc):
    """After the final table a chapter carries TWO empty paragraphs — the
    one python-docx auto-adds (Word needs it) and the `spacer(5)` that
    `b.box()` emits. Either half-line can tip a full last page past the
    boundary and strand a header-only blank page in the merged book. Squash
    every empty paragraph that trails the last table to ~1 pt; stop at the
    table so nothing visible moves."""
    from docx.text.paragraph import Paragraph
    for child in reversed(list(doc.element.body)):
        if child.tag == qn("w:tbl"):
            break
        if child.tag != qn("w:p"):
            continue                      # e.g. the closing <w:sectPr>
        para = Paragraph(child, doc)
        if para.text.strip():
            break
        pf = para.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = Pt(1)
        for r in para.runs:
            r.font.size = Pt(1)
        pPr = child.find(qn("w:pPr"))
        if pPr is None:
            pPr = OxmlElement("w:pPr"); child.insert(0, pPr)
        rPr = pPr.find(qn("w:rPr"))
        if rPr is None:
            rPr = OxmlElement("w:rPr"); pPr.append(rPr)
        for tag in ("w:sz", "w:szCs"):
            e = rPr.find(qn(tag))
            if e is None:
                e = OxmlElement(tag); rPr.append(e)
            e.set(qn("w:val"), "2")


# ── page break + bookmark at each chapter start ───────────────────────────
def inject_chapter_start(doc, name, bid):
    """Prepend an anchor paragraph: page-break-before + bookmark <name>."""
    body = doc.element.body
    p = OxmlElement("w:p")
    pPr = OxmlElement("w:pPr")
    pPr.append(OxmlElement("w:pageBreakBefore"))
    rPr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "2"); rPr.append(sz)
    szcs = OxmlElement("w:szCs"); szcs.set(qn("w:val"), "2"); rPr.append(szcs)
    pPr.append(rPr)
    p.append(pPr)
    bs = OxmlElement("w:bookmarkStart")
    bs.set(qn("w:id"), str(bid)); bs.set(qn("w:name"), name)
    be = OxmlElement("w:bookmarkEnd"); be.set(qn("w:id"), str(bid))
    p.append(bs); p.append(be)
    body.insert(0, p)


def inject_section_bookmarks(doc, n):
    """Wrap each `Heading 1` paragraph in a bookmark `_chNN_sK` so the
    সূচিপত্র can point a PAGEREF at every section, not just the chapter.
    K counts Heading-1 paragraphs in document order — the same order
    chapter_sections() walks, so the সূচিপত্র's k-th sub-line matches."""
    k = 0
    for para in doc.paragraphs:
        if not (para.style and para.style.name == "Heading 1"
                and para.text.strip()):
            continue
        k += 1
        bid = 92000 + n * 100 + k
        name = f"_ch{n:02d}_s{k}"
        bs = OxmlElement("w:bookmarkStart")
        bs.set(qn("w:id"), str(bid)); bs.set(qn("w:name"), name)
        be = OxmlElement("w:bookmarkEnd"); be.set(qn("w:id"), str(bid))
        pPr = para._p.find(qn("w:pPr"))
        if pPr is not None:
            pPr.addnext(be); pPr.addnext(bs)      # → pPr, bs, be, <runs>
        else:
            para._p.insert(0, be); para._p.insert(0, bs)


# ── book-wide footer ─────────────────────────────────────────────────────
def fill_footer(ftr, sec, page_number=True):
    for extra in list(ftr.paragraphs)[1:]:
        extra._p.getparent().remove(extra._p)
    p = ftr.paragraphs[0]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    p.text = ""
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    pPr = p._p.get_or_add_pPr()
    old = pPr.find(qn("w:pBdr"))
    if old is not None:
        pPr.remove(old)
    cw = sec.page_width - sec.left_margin - sec.right_margin
    ts = p.paragraph_format.tab_stops
    ts.clear_all()
    ts.add_tab_stop(int(cw / 2), WD_TAB_ALIGNMENT.CENTER)
    ts.add_tab_stop(cw, WD_TAB_ALIGNMENT.RIGHT)
    set_run_font(p.add_run(FOOT_L), size=Pt(9), color=GREY)
    if page_number:
        set_run_font(p.add_run("\t"), size=Pt(9))
        for rr in field(p, "PAGE", "1"):
            set_run_font(rr, size=Pt(10), color=NAVY, bold=True)
    set_run_font(p.add_run("\t" + FOOT_R), size=Pt(9), color=GREY)
    para_border(p, "top", color="C9D3DC", sz=6, space=3)


def clear_footer(ftr):
    for extra in list(ftr.paragraphs)[1:]:
        extra._p.getparent().remove(extra._p)
    p = ftr.paragraphs[0]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    p.text = ""


def enable_update_fields(doc):
    st = doc.settings.element
    if st.find(qn("w:updateFields")) is None:
        e = OxmlElement("w:updateFields"); e.set(qn("w:val"), "true")
        st.insert(0, e)


def bake_toc_numbers(dest):
    """Turn the সূচিপত্র's PAGEREF fields into plain, static page numbers.

    A live `PAGEREF … \\h` field is only as good as the reader's viewer.
    LibreOffice resolves it on PDF export, but Word/Pages/web viewers each
    do their own thing on open: some leave the cached result alone, some
    recompute it without paginating the way the printed book does and put
    **1** on every line. A delivered, generated book gains nothing from a
    live field — the numbers are recomputed from scratch on every build.

    So: round-trip a throwaway copy through LibreOffice (which computes
    every field), read each `PAGEREF _chNN[_sK]` → page out of the
    round-tripped `document.xml`, write that number (in Bangla) into the
    shipped file's field-result run, and then **delete the field machinery
    around it** — begin / instrText / separate / end — leaving one ordinary
    styled run that nothing can recompute. The round-trip copy is discarded;
    the shipped .docx stays python-docx's own output."""
    tmp = tempfile.mkdtemp(prefix="digesttoc_")
    try:
        r = subprocess.run(
            ["soffice", "--headless", "--convert-to", "docx",
             "--outdir", tmp, dest],
            capture_output=True, text=True, timeout=1800)
        rt = os.path.join(tmp, os.path.basename(dest))
        if not os.path.exists(rt):
            print("  bake: LibreOffice round-trip produced nothing — "
                  "leaving placeholders\n", r.stdout, r.stderr)
            return
        import zipfile
        with zipfile.ZipFile(rt) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        pages = {}
        pat = re.compile(
            r'PAGEREF\s+(_ch\d\d(?:_s\d+)?)\s+\\h.*?'
            r'fldCharType="separate".*?<w:t[^>]*>([^<]*)</w:t>.*?'
            r'fldCharType="end"', re.S)
        for m in pat.finditer(xml):
            pages.setdefault(m.group(1), m.group(2).strip())
        if not pages:
            print("  bake: no resolved PAGEREF results found — "
                  "leaving placeholders")
            return

        def fld_type(run):
            fc = run.find(qn("w:fldChar"))
            return None if fc is None else fc.get(qn("w:fldCharType"))

        doc = Document(dest)
        baked = 0
        for para in doc.paragraphs:
            runs = list(para._p.findall(qn("w:r")))
            for i, rr in enumerate(runs):
                it = rr.find(qn("w:instrText"))
                if it is None or not it.text:
                    continue
                mm = re.search(r'PAGEREF\s+(_ch\d\d(?:_s\d+)?)\s+\\h', it.text)
                if not mm or mm.group(1) not in pages:
                    continue
                beg = next((j for j in range(i - 1, -1, -1)
                            if fld_type(runs[j]) == "begin"), None)
                sep = next((j for j in range(i + 1, len(runs))
                            if fld_type(runs[j]) == "separate"), None)
                end = next((j for j in range(i + 1, len(runs))
                            if fld_type(runs[j]) == "end"), None)
                if beg is None or sep is None or end is None or end <= sep:
                    continue
                # keep the first result run, restyled with the real number …
                res = runs[sep + 1] if sep + 1 < end else None
                if res is None:
                    continue
                t = res.find(qn("w:t"))
                if t is None:
                    t = OxmlElement("w:t"); res.append(t)
                t.set(qn("xml:space"), "preserve")
                t.text = bn(pages[mm.group(1)])
                # … and drop everything that made it a field
                drop = [runs[beg], runs[i], runs[sep], runs[end]]
                drop += [runs[k] for k in range(sep + 2, end)]
                for el in drop:
                    par = el.getparent()
                    if par is not None:
                        par.remove(el)
                baked += 1
                break                       # one PAGEREF per সূচিপত্র line
        doc.save(dest)
        print(f"  bake: {baked} সূচিপত্র page numbers written as static text "
              f"({len(pages)} anchors resolved)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ── main ─────────────────────────────────────────────────────────────────
def main():
    chaps = chapter_list()
    print(f"chapters found: {len(chaps)}  ->", [n for n, _, _ in chaps])
    assert [n for n, _, _ in chaps] == list(range(1, 29)), "expected ch 1..28"

    toc_tree = [(n, title, chapter_sections(path)) for n, title, path in chaps]
    nsec = sum(len(s) for _n, _t, s in toc_tree)
    print(f"section headings: {nsec}  (সূচিপত্র = 28 chapters + {nsec} sections)")

    front_path = build_front(chaps, toc_tree)
    print("front matter built:", front_path)

    master = Document(front_path)
    composer = Composer(master)
    for n, title, path in chaps:
        cdoc = Document(path)
        inject_chapter_start(cdoc, f"_ch{n:02d}", 91000 + n)
        inject_section_bookmarks(cdoc, n)
        shrink_trailing_para(cdoc)
        composer.append(cdoc)
        print(f"  + অধ্যায় {n:02d}  {title}")
    composer.save(DEST)
    print("composed:", DEST)

    book = Document(DEST)
    secs = book.sections
    print("sections:", len(secs), "(0 = cover, 1 = book body)")
    assert len(secs) == 2, "expected a cover section plus a body section"
    for i, sec in enumerate(secs):
        sec.footer.is_linked_to_previous = False
        sec.header.is_linked_to_previous = False
        if i == 0:                                # cover — nothing on it
            sec.different_first_page_header_footer = True
            for f in (sec.footer, sec.first_page_footer,
                      sec.header, sec.first_page_header):
                f.is_linked_to_previous = False
                clear_footer(f)
        else:
            sec.different_first_page_header_footer = False
            fill_footer(sec.footer, sec)
    enable_update_fields(book)
    book.save(DEST)
    mb = os.path.getsize(DEST) / 1e6
    print(f"saved: {DEST}  ({mb:.1f} MB)")

    print("baking সূচিপত্র page numbers (LibreOffice field pass)…")
    bake_toc_numbers(DEST)

    if "--pdf" in sys.argv:
        print("rendering PDF (LibreOffice)…")
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                        "--outdir", os.path.dirname(DEST), DEST],
                       capture_output=True, text=True, timeout=2400)
        pdf = DEST[:-5] + ".pdf"
        print("pdf:", pdf, "exists:", os.path.exists(pdf))


if __name__ == "__main__":
    main()
