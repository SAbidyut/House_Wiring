# -*- coding: utf-8 -*-
"""
mkbook.py — assemble chapters 1–28 into a single delivered book.

  · full-bleed cover page (dia_cover.py artwork, its own borderless section)
  · imprint page — RAPTI details from rapti.net
  · clickable সূচিপত্র — every chapter AND every in-chapter section, with
    its page number baked in as static text (see bake_toc_numbers)
  · book-wide footer:  Resonance Automation · <page> · 01617-345534
  · running header:  book title (left) · অধ্যায় N · chapter title (centre,
    a STYLEREF field) · rapti.net (right)
  · continuous page numbers throughout

Run:   python assets_cover.py            # once — pulls the RAPTI logo
       python dia_cover.py
       python render.py 'diagrams/cover/cover.svg'
       python mkbook.py [--pdf]
Out:   ../ইলেকট্রিক্যাল হাউস ওয়্যারিং — সম্পূর্ণ বই (অধ্যায় ১–২৮).docx
"""
import os, re, glob, sys, subprocess, tempfile, shutil
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import (WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT,
                            WD_TAB_LEADER, WD_BREAK)
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml
from docxcompose.composer import Composer

from bookkit import (Book, bn, set_run_font, para_border, cell_shade,
                     cell_margins, cell_borders, field, keep_with_next,
                     NAVY, STEEL, GREY, INK, NAVY_HEX, STEEL_HEX)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "out")
COVER_PNG = os.path.join(HERE, "diagrams", "cover", "cover.png")
# full-page PPE poster that sits right after the cover, in the same
# borderless (zero-margin) section — supplied by the institute
FRONT_PPE_PNG = os.path.join(HERE, "assets", "front", "ppe_poster.png")
DEST = os.path.abspath(os.path.join(
    HERE, "..", "ইলেকট্রিক্যাল হাউস ওয়্যারিং — সম্পূর্ণ বই (অধ্যায় ১–২৮).docx"))

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
EDITION  = "প্রথম সংস্করণ · আগস্ট ২০২৬"
BN2A     = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")


GLOSS_H = "পারিভাষিক শব্দ"          # chapter tail sections that move to the
EXER_H  = "অনুশীলনী"                # consolidated back-of-book parts

# The অনুশীলনী block of every chapter is broken by question type and each
# type is consolidated chapter-wise into its own back-of-book part.  Match
# is on the Heading-2 text ending with the type name (the ক/খ/গ/ঘ/ঙ letter
# in front is not consistent between chapters).  Order = the in-chapter
# order.  Not every chapter has গাণিতিক সমস্যা (1,2,3,5,6,8 do not).
QTYPES = [
    ("বহুনির্বাচনী প্রশ্ন", "mcq"),
    ("সংক্ষিপ্ত প্রশ্ন",     "short"),
    ("রচনামূলক প্রশ্ন",      "essay"),
    ("গাণিতিক সমস্যা",       "math"),
    ("ব্যবহারিক কাজ",        "prac"),
]


def unlock_tables(doc):
    """Drop `w:cantSplit` from every table row in a pruned back-matter
    fragment.  `bookkit.table()` marks every row cantSplit — fine for the
    short, hand-placed tables inside a chapter, but a consolidated glossary
    table runs 40–60 rows and this LibreOffice drops every row past the
    first page when the whole table is unsplittable and overflows.  Letting
    it break between (and if need be within) rows paginates it correctly.
    The repeating header row (`w:tblHeader`) is kept."""
    for tbl in doc.element.body.iter(qn("w:tbl")):
        for tr in tbl.findall(qn("w:tr")):
            trPr = tr.find(qn("w:trPr"))
            if trPr is None:
                continue
            for cs in trPr.findall(qn("w:cantSplit")):
                trPr.remove(cs)


def chapter_list():
    rows = []
    for f in glob.glob(os.path.join(OUT, "অধ্যায়-*.docx")):
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
def chapter_sections(path):
    """Return the chapter's in-book section headings in document order —
    the `b.h1()` paragraphs (`১.১  …`), text kept whole (number + title).
    Same filter `inject_section_bookmarks()` uses, so the k-th here is the
    k-th there and the সূচিপত্র PAGEREF anchors line up.

    Stops at the পারিভাষিক শব্দ heading: in the merged book that section and
    the অনুশীলনী after it are lifted into the back-of-book parts, so only the
    body sections up to and including সারসংক্ষেপ stay under the chapter."""
    doc = Document(path)
    out = []
    for p in doc.paragraphs:
        if not (p.style and p.style.name == "Heading 1" and p.text.strip()):
            continue
        if p.text.strip().endswith(GLOSS_H):
            break
        out.append(p.text.strip())
    return out


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


def full_page_picture(doc, png, page_w, page_h, draw_id=9001, draw_name="cover"):
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
        '<wp:wrapNone/><wp:docPr id="%d" name="%s"/><wp:cNvGraphicFramePr/>%s'
        '</wp:anchor>' % (WP, A, int(page_w), int(page_h), draw_id, draw_name, gx))
    inline.getparent().replace(inline, anchor)
    return p


def build_front(chaps, toc_tree, type_map):
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

    # ---------------- PPE POSTER — second full-bleed page ----------------
    # A page-anchored (behind-text) image attaches to whatever page its
    # paragraph falls on, so force page 2 with an explicit break, then drop
    # the poster on it the same way the cover is placed.
    if not os.path.exists(FRONT_PPE_PNG):
        raise SystemExit("PPE poster missing: " + FRONT_PPE_PNG)
    brp = d.add_paragraph()
    brp.paragraph_format.space_before = brp.paragraph_format.space_after = Pt(0)
    brp.paragraph_format.line_spacing = 1.0
    _brk = brp.add_run()
    _brk.add_break(WD_BREAK.PAGE)
    set_run_font(_brk, size=Pt(1))
    full_page_picture(d, FRONT_PPE_PNG, PW, PH, draw_id=9002, draw_name="ppe_poster")

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
    #   book title (left) · অধ্যায় N · chapter title (centre) · rapti.net (right)
    #
    # The paragraph MUST be style "Normal", not the built-in "Header".
    # "Header" carries its own tab stops (centre @4680, right @9360 twips)
    # and OOXML *merges* a style's tabs with the paragraph's own — so the
    # first \t lands on the style's centre stop and the second on ours,
    # leaving `rapti.net` floating mid-page instead of at the right margin.
    # `tab_stops.clear_all()` only clears paragraph-level stops, never a
    # style's; changing the style is what actually fixes it.
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
    # STYLEREF tracks the nearest preceding "RaptiChapterTitle" paragraph —
    # the navy title block chapter_opener() stamps once per chapter, whose
    # first (hidden, 1 pt) run is "অধ্যায় N · ".  So this cell shows the
    # number and the name of whichever chapter's pages the reader is on and
    # updates by itself, without a header per section — docxcompose drops
    # every appended chapter's own sectPr, so a real per-chapter header is
    # not an option here (see the mkbook.py notes in CLAUDE.md).
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
    body("এই বইটি রেজোন্যান্স অটোমেশন প্রফেশনাল ট্রেনিং ইনস্টিটিউট (RAPTI)-এর "
         "‘ইলেকট্রিক্যাল হাউস ওয়্যারিং’ কোর্সের জন্য প্রণীত পূর্ণাঙ্গ পাঠ্যপুস্তক। "
         "কোর্স মডিউলের লেসন-ক্রম অনুসরণ করে অধ্যায় সাজানো হয়েছে, যাতে ক্লাসের "
         "পড়া আর বইয়ের অধ্যায় হুবহু মিলে যায়। প্রতিটি অধ্যায়ে তত্ত্বের সঙ্গে "
         "কর্মক্ষেত্রের বাস্তব অভিজ্ঞতা, চিত্র, সারণি ও গাণিতিক উদাহরণ একসঙ্গে "
         "দেওয়া হয়েছে এবং প্রতিটি অধ্যায়ের শেষে সারসংক্ষেপ যুক্ত হয়েছে। প্রতিটি "
         "অধ্যায়ের পারিভাষিক শব্দ ও অনুশীলনী বইয়ের শেষে ‘পরিভাষা’ ও ‘অনুশীলনী’ "
         "অংশে অধ্যায়-ক্রমে একত্র করা হয়েছে।")
    body("নিরাপত্তা বিধি, তারের মাপ, সুরক্ষা যন্ত্র ও হিসাব-নিকাশের ক্ষেত্রে "
         "IEC, BNBC ও BS মান অনুসরণ করা হয়েছে; দেশীয় প্রচলন যেখানে মান থেকে "
         "আলাদা, সেখানে তা স্পষ্ট করে উল্লেখ করা হয়েছে। চিত্র ও সারণি "
         "অধ্যায়-ভিত্তিক নম্বরে সাজানো (যেমন চিত্র ৩.২, সারণি ৭.১)। এই সংস্করণে "
         "কোর্স মডিউলের সবগুলো অধ্যায় (১ থেকে ২৮) অন্তর্ভুক্ত; পরিশিষ্ট "
         "পরবর্তী সংস্করণে যুক্ত হবে।")

    head("প্রকাশনা ও যোগাযোগ")
    kv("বইয়ের নাম", "ইলেকট্রিক্যাল হাউস ওয়্যারিং (Electrical House Wiring)")
    kv("সংস্করণ", f"{EDITION}  —  অধ্যায় ১–২৮")
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

    # ---------------- সূচিপত্র ----------------
    # `pageBreakBefore` on this heading rather than a standalone b.page_break()
    # paragraph — an empty break paragraph landing at the foot of a full
    # imprint page was stranding a header-only blank page before the সূচিপত্র.
    hp = d.add_paragraph(); hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hp.paragraph_format.page_break_before = True
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
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.05
        keep_with_next(p)
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
            q.paragraph_format.space_after = Pt(1)
            q.paragraph_format.line_spacing = 1.0
            q.paragraph_format.left_indent = Cm(0.8)
            qs = q.paragraph_format.tab_stops
            qs.add_tab_stop(cw, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
            _link(q, f"_ch{n:02d}_s{k}", [(sec, 9.5, "1A1A1A", False)])
            q.add_run("\t")
            for rr in field(q, f" PAGEREF _ch{n:02d}_s{k} \\h ", "০"):
                set_run_font(rr, size=Pt(9), color=STEEL, bold=False)

    # ── back-of-book parts — one সূচিপত্র line each, no per-chapter detail ──
    def part_line(title, anchor):
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.05
        keep_with_next(p)
        p.paragraph_format.tab_stops.add_tab_stop(
            cw, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        _link(p, anchor, [(title, 11.5, NAVY_HEX, True)])
        p.add_run("\t")
        for rr in field(p, f" PAGEREF {anchor} \\h ", "০"):
            set_run_font(rr, size=Pt(11), color=NAVY, bold=True)

    def chap_subline(n, title, anchor):
        q = d.add_paragraph()
        q.alignment = WD_ALIGN_PARAGRAPH.LEFT
        q.paragraph_format.space_after = Pt(1)
        q.paragraph_format.line_spacing = 1.0
        q.paragraph_format.left_indent = Cm(0.8)
        q.paragraph_format.tab_stops.add_tab_stop(
            cw, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        _link(q, anchor, [(f"অধ্যায়  {bn('%02d' % n)}    {title}",
                           9.5, "1A1A1A", False)])
        q.add_run("\t")
        for rr in field(q, f" PAGEREF {anchor} \\h ", "০"):
            set_run_font(rr, size=Pt(9), color=STEEL, bold=False)

    part_line("পরিভাষা", "_partGloss")
    for qname, slug in QTYPES:
        part_line(qname, f"_part_{slug}")

    front_path = os.path.join(OUT, "_front.docx")
    b.save(front_path)
    return front_path


# ── collapse a chapter's trailing spacer paragraph ───────────────────────
def shrink_trailing_para(doc):
    """python-docx puts an empty paragraph after the final table (Word needs
    one). At normal 11 pt that half-line can tip past a page boundary and
    strand a header-only blank page in the merged book. Squash it to ~1 pt so
    it never forces a new page — it is the last element in the chapter, so
    nothing above it moves."""
    paras = doc.paragraphs
    if not paras:
        return
    last = paras[-1]
    if last.text.strip():
        return
    pf = last.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(1)
    for r in last.runs:
        r.font.size = Pt(1)
    pPr = last._p.get_or_add_pPr()
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


# ── split a chapter into core / glossary / exercises ─────────────────────
def _h1_elem(doc, endswith):
    for p in doc.paragraphs:
        if (p.style and p.style.name == "Heading 1"
                and p.text.strip().endswith(endswith)):
            return p._p
    return None


def _relabel_h1(p_elem, text):
    """Swap a Heading-1 paragraph's visible runs for one navy 19 pt run —
    keeps the paragraph's style and bottom border (its bookmark too, since
    that sits in pPr, not the runs)."""
    for r in p_elem.findall(qn("w:r")):
        p_elem.remove(r)
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rf = OxmlElement("w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), "Kalpurush")
    rPr.append(rf)
    for tag in ("w:sz", "w:szCs"):
        e = OxmlElement(tag); e.set(qn("w:val"), "38"); rPr.append(e)
    rPr.append(OxmlElement("w:b")); rPr.append(OxmlElement("w:bCs"))
    col = OxmlElement("w:color"); col.set(qn("w:val"), NAVY_HEX); rPr.append(col)
    r.append(rPr)
    t = OxmlElement("w:t"); t.set(qn("xml:space"), "preserve"); t.text = text
    r.append(t)
    p_elem.append(r)


def _bookmark_elem(p_elem, name, bid):
    bs = OxmlElement("w:bookmarkStart")
    bs.set(qn("w:id"), str(bid)); bs.set(qn("w:name"), name)
    be = OxmlElement("w:bookmarkEnd"); be.set(qn("w:id"), str(bid))
    pPr = p_elem.find(qn("w:pPr"))
    if pPr is not None:
        pPr.addnext(be); pPr.addnext(bs)
    else:
        p_elem.insert(0, be); p_elem.insert(0, bs)


_H2NUM = re.compile(r'^[০-৯]+(?:\.[০-৯]+)+\s*$')


def _strip_h2_numbers(doc):
    """Drop the `NN.NN.` prefix run from the exercise block's Heading 2s
    (`১.১৫.১  ক. বহুনির্বাচনী প্রশ্ন` → `ক. বহুনির্বাচনী প্রশ্ন`). Their
    parent `NN.NN অনুশীলনী` heading is gone in the back-of-book part, so the
    sub-number is orphaned."""
    for p in doc.paragraphs:
        if not (p.style and p.style.name == "Heading 2"):
            continue
        runs = p._p.findall(qn("w:r"))
        if runs:
            t = runs[0].find(qn("w:t"))
            if t is not None and t.text and _H2NUM.match(t.text):
                p._p.remove(runs[0])


def _strip_media(doc):
    """Drop every image relationship from a pruned fragment. The glossary and
    exercise blocks carry no pictures, so the copies keep the whole chapter's
    media parts as dead weight — docxcompose would copy them into the merged
    book. Remove them before the append."""
    for rid, rel in list(doc.part.rels.items()):
        if "image" in rel.reltype:
            doc.part.drop_rel(rid)


def _p_style(el):
    """Style name of a <w:p> element, or None for anything else."""
    if el.tag != qn("w:p"):
        return None
    pPr = el.find(qn("w:pPr"))
    if pPr is None:
        return "Normal"
    ps = pPr.find(qn("w:pStyle"))
    return ps.get(qn("w:val")) if ps is not None else "Normal"


def _p_text(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t")))


def _exer_h2s(kids, ei):
    """(slug, index) for each Heading-2 in the অনুশীলনী block, in order.
    `ei` is the index of the অনুশীলনী Heading-1; scan forward to the sectPr."""
    out = []
    for i in range(ei + 1, len(kids)):
        el = kids[i]
        if el.tag == qn("w:sectPr"):
            break
        if _p_style(el) in ("Heading2", "Heading 2"):
            txt = _p_text(el).strip()
            for qname, slug in QTYPES:
                if txt.endswith(qname):
                    out.append((slug, i))
                    break
    return out


def chapter_qtypes(path):
    """Question-type slugs present in a chapter's অনুশীলনী, in order."""
    doc = Document(path)
    kids = list(doc.element.body)
    e = _h1_elem(doc, EXER_H)
    assert e is not None, f"{path}: no '{EXER_H}' Heading 1"
    return [slug for slug, _i in _exer_h2s(kids, kids.index(e))]


def split_chapter(path, n, title):
    """Pruned copies of a chapter .docx:
      core   — chapter body + সারসংক্ষেপ (পারিভাষিক শব্দ … end removed)
      gloss  — only পারিভাষিক শব্দ … up to অনুশীলনী; heading relabelled
      qfrags — {slug: Document} one per question type present in অনুশীলনী,
               each = the relabelled অনুশীলনী Heading-1 + that type's H2
               block content (the H2 heading itself dropped — the part
               divider already names the type)
    Every block in a .docx body is a direct child of <w:body>; the last child
    is <w:sectPr> and is always kept."""
    sect = qn("w:sectPr")
    label = f"অধ্যায় {bn('%02d' % n)} — {title}"

    core = Document(path)
    g = _h1_elem(core, GLOSS_H)
    assert g is not None, f"ch{n:02d}: no '{GLOSS_H}' Heading 1"
    kids = list(core.element.body)
    for el in kids[kids.index(g):]:
        if el.tag != sect:
            core.element.body.remove(el)

    gloss = Document(path)
    g = _h1_elem(gloss, GLOSS_H); e = _h1_elem(gloss, EXER_H)
    assert e is not None, f"ch{n:02d}: no '{EXER_H}' Heading 1"
    kids = list(gloss.element.body)
    gi, ei = kids.index(g), kids.index(e)
    for el in kids[:gi] + [x for x in kids[ei:] if x.tag != sect]:
        gloss.element.body.remove(el)
    _relabel_h1(g, label)
    _bookmark_elem(g, f"_gloss{n:02d}", 93000 + n)
    unlock_tables(gloss)
    _strip_media(gloss)

    qfrags = {}
    order = chapter_qtypes(path)
    assert order, f"ch{n:02d}: no recognised অনুশীলনী question types"
    for qi, (qname, slug) in enumerate(QTYPES):
        if slug not in order:
            continue
        frag = Document(path)
        kids = list(frag.element.body)
        e = kids.index(_h1_elem(frag, EXER_H))
        h2s = _exer_h2s(kids, e)
        pos = {s: idx for s, idx in h2s}
        start = pos[slug]
        later = [idx for s, idx in h2s if idx > start]
        end = min(later) if later else next(
            i for i, el in enumerate(kids) if el.tag == sect)
        keep = {id(kids[e])} | {id(kids[j]) for j in range(start + 1, end)}
        for el in kids:
            if el.tag == sect:
                continue
            if id(el) not in keep:
                frag.element.body.remove(el)
        eh1 = _h1_elem(frag, EXER_H)
        _relabel_h1(eh1, label)
        _bookmark_elem(eh1, f"_{slug}{n:02d}", 96000 + n * 10 + qi)
        _strip_h2_numbers(frag)
        shrink_trailing_para(frag)
        unlock_tables(frag)
        _strip_media(frag)
        qfrags[slug] = frag

    return core, gloss, qfrags


def add_part_divider(master, title, anchor, bid):
    """A back-of-book part opener: page break, big navy heading with a
    bookmark for the সূচিপত্র, and a hidden 1 pt RaptiChapterTitle paragraph
    so the running-header STYLEREF shows the part name instead of trailing
    'অধ্যায় ২৮' across the part's pages."""
    ph = master.add_paragraph(style="RaptiChapterTitle")
    ph.paragraph_format.page_break_before = True
    ph.paragraph_format.space_before = Pt(0)
    ph.paragraph_format.space_after = Pt(0)
    ph.paragraph_format.line_spacing = 1.0
    rh = ph.add_run(title)
    rh.font.size = Pt(1); rh.font.hidden = True

    p = master.add_paragraph(style="Heading 1")
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    keep_with_next(p)
    _bookmark_elem(p._p, anchor, bid)
    set_run_font(p.add_run(title), size=Pt(24), bold=True, color=NAVY)
    para_border(p, "bottom", NAVY_HEX, 12, 6)


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
    anchor = (r'(_ch\d\d(?:_s\d+)?|_partGloss|_part_(?:mcq|short|essay|math|prac)'
              r'|_gloss\d\d|_(?:mcq|short|essay|math|prac)\d\d)')
    tmp = tempfile.mkdtemp(prefix="booktoc_")
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
            r'PAGEREF\s+' + anchor + r'\s+\\h.*?'
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
                mm = re.search(r'PAGEREF\s+' + anchor + r'\s+\\h', it.text)
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
    global DEST
    chaps = chapter_list()
    only = os.environ.get("MKBOOK_ONLY")
    if only:                                   # dev: subset build, small + fast
        keep = {int(x) for x in only.split(",")}
        chaps = [c for c in chaps if c[0] in keep]
        DEST = os.path.join(OUT, "_subset_book.docx")
        print("SUBSET build ->", [n for n, _, _ in chaps], "->", DEST)
    print(f"chapters found: {len(chaps)}  ->", [n for n, _, _ in chaps])
    if not only:
        assert [n for n, _, _ in chaps] == list(range(1, 29)), "expected ch 1..28"

    toc_tree = [(n, title, chapter_sections(path)) for n, title, path in chaps]
    nsec = sum(len(sx) for _n, _t, sx in toc_tree)
    print(f"section headings: {nsec}  (সূচিপত্র = 28 chapters + {nsec} sections)")

    # which chapters carry which অনুশীলনী question type, in QTYPES order
    type_map = {slug: [] for _q, slug in QTYPES}
    for n, title, path in chaps:
        for slug in chapter_qtypes(path):
            type_map[slug].append((n, title))
    for _q, slug in QTYPES:
        print(f"  {slug}: {len(type_map[slug])} chapters")

    front_path = build_front(chaps, toc_tree, type_map)
    print("front matter built:", front_path)

    master = Document(front_path)
    composer = Composer(master)

    # split every chapter first: core keeps সারসংক্ষেপ; the পারিভাষিক শব্দ tail
    # becomes the পরিভাষা part; the অনুশীলনী tail is broken by question type
    # into five parts, each consolidated chapter-wise.
    cores, glosses = [], []
    qfrag_by_slug = {slug: [] for _q, slug in QTYPES}
    for n, title, path in chaps:
        core, gloss, qfrags = split_chapter(path, n, title)
        inject_chapter_start(core, f"_ch{n:02d}", 91000 + n)
        inject_section_bookmarks(core, n)
        shrink_trailing_para(core)
        cores.append((n, title, core))
        glosses.append((n, title, gloss))
        for slug, frag in qfrags.items():
            qfrag_by_slug[slug].append((n, title, frag))

    for n, title, core in cores:
        composer.append(core)
        print(f"  + অধ্যায় {n:02d}  {title}")

    add_part_divider(master, "পরিভাষা", "_partGloss", 93000)
    for n, title, gloss in glosses:
        composer.append(gloss)
        print(f"  + পরিভাষা · অধ্যায় {n:02d}  {title}")

    for qi, (qname, slug) in enumerate(QTYPES):
        add_part_divider(master, qname, f"_part_{slug}", 95000 + qi)
        for n, title, frag in qfrag_by_slug[slug]:
            composer.append(frag)
            print(f"  + {qname} · অধ্যায় {n:02d}  {title}")

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
