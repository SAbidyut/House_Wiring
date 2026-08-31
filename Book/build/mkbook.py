# -*- coding: utf-8 -*-
"""
mkbook.py — assemble chapters 1–23 into a single delivered book.

  · full-bleed cover page (dia_cover.py artwork, its own borderless section)
  · imprint page — RAPTI details from rapti.net
  · clickable সূচিপত্র  (internal hyperlink + PAGEREF, auto page numbers)
  · book-wide footer:  Resonance Automation · <page> · 01617-345534
  · one running header for the whole book
  · continuous page numbers throughout

Run:   python assets_cover.py            # once — pulls the RAPTI logo
       python dia_cover.py
       python render.py 'diagrams/cover/cover.svg'
       python mkbook.py [--pdf]
Out:   ../ইলেকট্রিক্যাল হাউস ওয়্যারিং — সম্পূর্ণ বই (অধ্যায় ১–২৩).docx
"""
import os, re, glob, sys, subprocess
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
COVER_PNG = os.path.join(HERE, "diagrams", "cover", "cover.png")
DEST = os.path.abspath(os.path.join(
    HERE, "..", "ইলেকট্রিক্যাল হাউস ওয়্যারিং — সম্পূর্ণ বই (অধ্যায় ১–২৩).docx"))

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
        if 1 <= n <= 23:
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


def build_front(chaps):
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

    S.header.is_linked_to_previous = False
    hp = S.header.paragraphs[0]
    hp.text = ""
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hp.paragraph_format.tab_stops.add_tab_stop(cw, WD_TAB_ALIGNMENT.RIGHT)
    set_run_font(hp.add_run("ইলেকট্রিক্যাল হাউস ওয়্যারিং"), size=Pt(9), color=GREY)
    set_run_font(hp.add_run("\t" + INST_BN), size=Pt(9), color=GREY, bold=True)
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
         "দেওয়া হয়েছে এবং অধ্যায়ের শেষে সারসংক্ষেপ, পারিভাষিক শব্দ ও অনুশীলনী "
         "যুক্ত হয়েছে।")
    body("নিরাপত্তা বিধি, তারের মাপ, সুরক্ষা যন্ত্র ও হিসাব-নিকাশের ক্ষেত্রে "
         "IEC, BNBC ও BS মান অনুসরণ করা হয়েছে; দেশীয় প্রচলন যেখানে মান থেকে "
         "আলাদা, সেখানে তা স্পষ্ট করে উল্লেখ করা হয়েছে। চিত্র ও সারণি "
         "অধ্যায়-ভিত্তিক নম্বরে সাজানো (যেমন চিত্র ৩.২, সারণি ৭.১)। এই সংস্করণে "
         "অধ্যায় ১ থেকে ২৩ অন্তর্ভুক্ত; অবশিষ্ট অধ্যায় ও পরিশিষ্ট পরবর্তী "
         "সংস্করণে যুক্ত হবে।")

    head("প্রকাশনা ও যোগাযোগ")
    kv("বইয়ের নাম", "ইলেকট্রিক্যাল হাউস ওয়্যারিং (Electrical House Wiring)")
    kv("সংস্করণ", f"{EDITION}  —  অধ্যায় ১–২৩")
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
    set_run_font(cap.add_run("শিরোনামে ক্লিক করলে সরাসরি সেই অধ্যায়ে যাওয়া যাবে।"),
                 size=Pt(9), italic=True, color=GREY)

    for n, title, _ in chaps:
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(4)
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

    note = d.add_paragraph(); note.alignment = WD_ALIGN_PARAGRAPH.LEFT
    note.paragraph_format.space_before = Pt(12)
    set_run_font(note.add_run(
        "অধ্যায় ২৪–২৮ এবং পরিশিষ্ট (ক–জ) পরবর্তী সংস্করণে যুক্ত হবে।"),
        size=Pt(9.5), italic=True, color=GREY)

    front_path = os.path.join(OUT, "_front.docx")
    b.save(front_path)
    return front_path


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


# ── main ─────────────────────────────────────────────────────────────────
def main():
    chaps = chapter_list()
    print(f"chapters found: {len(chaps)}  ->", [n for n, _, _ in chaps])
    assert [n for n, _, _ in chaps] == list(range(1, 24)), "expected ch 1..23"

    front_path = build_front(chaps)
    print("front matter built:", front_path)

    master = Document(front_path)
    composer = Composer(master)
    for n, title, path in chaps:
        cdoc = Document(path)
        inject_chapter_start(cdoc, f"_ch{n:02d}", 91000 + n)
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

    if "--pdf" in sys.argv:
        print("rendering PDF (LibreOffice)…")
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                        "--outdir", os.path.dirname(DEST), DEST],
                       capture_output=True, text=True, timeout=2400)
        pdf = DEST[:-5] + ".pdf"
        print("pdf:", pdf, "exists:", os.path.exists(pdf))


if __name__ == "__main__":
    main()
