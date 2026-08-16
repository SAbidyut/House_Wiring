# -*- coding: utf-8 -*-
"""
bookkit.py — Reusable DOCX book engine for
"ইলেকট্রিক্যাল হাউস ওয়্যারিং" (Resonance Automation Professional Training Institute)

Every chapter is produced with this engine so typography, colours, figure/table
numbering and box styles stay identical across the whole 400+ page book.
"""
from docx import Document
from docx.shared import Pt, Cm, Mm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement
from docx.opc.part import Part
from docx.opc.packuri import PackURI
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import os

SVG_EXT_URI = "{96DAC541-7B7A-43D3-8B79-37D633B846F1}"
ASVG_NS = "http://schemas.microsoft.com/office/drawing/2016/SVG/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

# ────────────────────────────────────────────────────────────────────────────
#  Design tokens
# ────────────────────────────────────────────────────────────────────────────
BN_FONT   = "Kalpurush"          # Bangla body face
EN_FONT   = "Kalpurush"          # keep one face so mixed lines sit on one baseline
MONO_FONT = "Consolas"

NAVY      = RGBColor(0x0F, 0x33, 0x57)   # primary
NAVY_HEX  = "0F3357"
STEEL     = RGBColor(0x1D, 0x5B, 0x8F)
STEEL_HEX = "1D5B8F"
RED       = RGBColor(0xB3, 0x2A, 0x22)
RED_HEX   = "B32A22"
GREEN     = RGBColor(0x1B, 0x6E, 0x47)
GREEN_HEX = "1B6E47"
AMBER_HEX = "9C6500"
INK       = RGBColor(0x1A, 0x1A, 0x1A)
GREY      = RGBColor(0x55, 0x55, 0x55)

BOX_TINTS = {                       # (fill, border, title colour)
    "safety":  ("FDECEA", "B32A22", RED_HEX),
    "note":    ("EAF2FA", "1D5B8F", STEEL_HEX),
    "tip":     ("EAF6EF", "1B6E47", GREEN_HEX),
    "def":     ("F4F1E8", "9C6500", AMBER_HEX),
    "formula": ("F2F4F7", "0F3357", NAVY_HEX),
}
BOX_LABEL = {
    "safety":  "⚠  নিরাপত্তা সতর্কতা",
    "note":    "❖  মনে রাখুন",
    "tip":     "✔  ব্যবহারিক পরামর্শ",
    "def":     "📘  সংজ্ঞা",
    "formula": "∑  সূত্র",
}

BODY_SIZE = Pt(11.5)
LINE_RULE = 1.30

BN_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
def bn(n):
    """Convert any number/string to Bangla numerals."""
    return str(n).translate(BN_DIGITS)


# ────────────────────────────────────────────────────────────────────────────
#  Low level OOXML helpers
# ────────────────────────────────────────────────────────────────────────────
def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn("w:" + k), str(v))
    return e


def etree_svgblip(rId):
    """<asvg:svgBlip r:embed="rIdN"/> — the element Word looks for."""
    from lxml import etree
    el = etree.SubElement(
        etree.Element("{%s}wrap" % ASVG_NS, nsmap={"asvg": ASVG_NS}),
        "{%s}svgBlip" % ASVG_NS, nsmap={"asvg": ASVG_NS, "r": R_NS})
    el.set("{%s}embed" % R_NS, rId)
    return el


def set_run_font(run, name=BN_FONT, size=None, bold=None, italic=None,
                 color=None, spacing=None):
    """Set a font on all script slots so Bangla (complex script) obeys it."""
    rPr = run._r.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rPr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), name)
    if size is not None:
        run.font.size = size
        sz = rPr.find(qn("w:szCs"))
        if sz is None:
            sz = OxmlElement("w:szCs"); rPr.append(sz)
        sz.set(qn("w:val"), str(int(size.pt * 2)))
    if bold is not None:
        run.font.bold = bold
        b = rPr.find(qn("w:bCs"))
        if b is None:
            b = OxmlElement("w:bCs"); rPr.append(b)
        b.set(qn("w:val"), "1" if bold else "0")
    if italic is not None:
        run.font.italic = italic
        i = rPr.find(qn("w:iCs"))
        if i is None:
            i = OxmlElement("w:iCs"); rPr.append(i)
        i.set(qn("w:val"), "1" if italic else "0")
    if color is not None:
        run.font.color.rgb = color
    if spacing is not None:
        s = OxmlElement("w:spacing"); s.set(qn("w:val"), str(spacing)); rPr.append(s)
    return run


def shade(el, fill):
    pr = el.get_or_add_tcPr() if el.tag.endswith("}tc") else el.get_or_add_pPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), fill)
    pr.append(sh)


def cell_shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), fill)
    tcPr.append(sh)


def cell_borders(cell, color="BFBFBF", sz=6, edges=("top", "left", "bottom", "right")):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = tcPr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders"); tcPr.append(borders)
    for e in edges:
        el = borders.find(qn("w:" + e))
        if el is None:
            el = OxmlElement("w:" + e); borders.append(el)
        el.set(qn("w:val"), "single"); el.set(qn("w:sz"), str(sz))
        el.set(qn("w:space"), "0"); el.set(qn("w:color"), color)


def cell_margins(cell, top=90, bottom=90, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    m = OxmlElement("w:tcMar")
    for tag, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        e = OxmlElement("w:" + tag)
        e.set(qn("w:w"), str(val)); e.set(qn("w:type"), "dxa")
        m.append(e)
    tcPr.append(m)


def para_border(p, edge="bottom", color=NAVY_HEX, sz=8, space=4):
    pPr = p._p.get_or_add_pPr()
    pbdr = pPr.find(qn("w:pBdr"))
    if pbdr is None:
        pbdr = OxmlElement("w:pBdr"); pPr.append(pbdr)
    e = OxmlElement("w:" + edge)
    e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(sz))
    e.set(qn("w:space"), str(space)); e.set(qn("w:color"), color)
    pbdr.append(e)


def no_split(table):
    """Stop Word from breaking a row (or a one-cell callout box) across pages."""
    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        if trPr.find(qn("w:cantSplit")) is None:
            e = OxmlElement("w:cantSplit"); e.set(qn("w:val"), "true")
            trPr.insert(0, e)
    return table



def frame_para(p, width_twips, align="center", wrap="notBeside",
               vanchor="text", hanchor="margin", space_before=0):
    """Put a paragraph into a Word text frame.

    Consecutive paragraphs carrying identical framePr become ONE frame, so a
    figure and its caption travel together. A frame that will not fit moves to
    the next page and the following body text flows up into the space it left —
    which is what stops a tall figure from stranding a blank band behind it.
    """
    pPr = p._p.get_or_add_pPr()
    old = pPr.find(qn("w:framePr"))
    if old is not None:
        pPr.remove(old)
    fp = OxmlElement("w:framePr")
    fp.set(qn("w:w"), str(int(width_twips)))
    fp.set(qn("w:h"), "0")
    fp.set(qn("w:hRule"), "auto")
    fp.set(qn("w:wrap"), wrap)
    fp.set(qn("w:vAnchor"), vanchor)
    fp.set(qn("w:hAnchor"), hanchor)
    fp.set(qn("w:xAlign"), align)
    fp.set(qn("w:y"), "1")
    fp.set(qn("w:vSpace"), str(int(space_before)))
    pPr.insert(0, fp)
    return p


def keep_with_next(p, on=True):
    pPr = p._p.get_or_add_pPr()
    k = pPr.find(qn("w:keepNext"))
    if k is None:
        k = OxmlElement("w:keepNext"); pPr.append(k)
    k.set(qn("w:val"), "1" if on else "0")


def keep_lines(p):
    pPr = p._p.get_or_add_pPr()
    k = OxmlElement("w:keepLines"); pPr.append(k)


def no_widow_control(p):
    pPr = p._p.get_or_add_pPr()
    w = OxmlElement("w:widowControl"); w.set(qn("w:val"), "1"); pPr.append(w)


def field(paragraph, code, placeholder=" "):
    r1 = paragraph.add_run(); fc = _el("w:fldChar", fldCharType="begin"); r1._r.append(fc)
    r2 = paragraph.add_run()
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = code
    r2._r.append(it)
    r3 = paragraph.add_run(); fc2 = _el("w:fldChar", fldCharType="separate"); r3._r.append(fc2)
    r4 = paragraph.add_run(placeholder)
    r5 = paragraph.add_run(); fc3 = _el("w:fldChar", fldCharType="end"); r5._r.append(fc3)
    return [r1, r2, r3, r4, r5]


# ────────────────────────────────────────────────────────────────────────────
#  Book class
# ────────────────────────────────────────────────────────────────────────────
class Book:
    def __init__(self, chapter_no, chapter_title, subtitle="",
                 book_title="ইলেকট্রিক্যাল হাউস ওয়্যারিং",
                 institute="রেজোন্যান্স অটোমেশন প্রফেশনাল ট্রেনিং ইনস্টিটিউট"):
        self.doc = Document()
        self.ch = chapter_no
        self.ch_title = chapter_title
        self.subtitle = subtitle
        self.book_title = book_title
        self.institute = institute
        self.fig_n = 0
        self.tab_n = 0
        self.eq_n = 0
        self.figures = []   # (label, caption)
        self.tables = []
        self._setup_page()
        self._setup_styles()

    # ── page / section ────────────────────────────────────────────────────
    def _setup_page(self):
        s = self.doc.sections[0]
        s.page_width, s.page_height = Mm(210), Mm(297)
        s.top_margin, s.bottom_margin = Cm(2.2), Cm(2.0)
        s.left_margin, s.right_margin = Cm(2.4), Cm(2.0)
        s.header_distance, s.footer_distance = Cm(1.1), Cm(1.0)
        self.section = s

    @property
    def text_width(self):
        s = self.section
        return s.page_width - s.left_margin - s.right_margin

    def _setup_styles(self):
        d = self.doc
        st = d.styles["Normal"]
        st.font.name = BN_FONT
        st.font.size = BODY_SIZE
        st.font.color.rgb = INK
        rf = st.element.get_or_add_rPr().get_or_add_rFonts()
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), BN_FONT)
        szcs = OxmlElement("w:szCs"); szcs.set(qn("w:val"), str(int(BODY_SIZE.pt * 2)))
        st.element.get_or_add_rPr().append(szcs)
        pf = st.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        pf.line_spacing = LINE_RULE
        pf.space_after = Pt(6)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        for name, size, color, bold in (
            ("Heading 1", 19, NAVY, True),
            ("Heading 2", 15, NAVY, True),
            ("Heading 3", 13, STEEL, True),
            ("Heading 4", 12, STEEL, True),
        ):
            s = d.styles[name]
            s.font.name = BN_FONT; s.font.size = Pt(size)
            s.font.color.rgb = color; s.font.bold = bold
            rf = s.element.get_or_add_rPr().get_or_add_rFonts()
            for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                rf.set(qn(a), BN_FONT)
            for tag, val in (("w:szCs", str(size * 2)), ):
                e = OxmlElement(tag); e.set(qn("w:val"), val)
                s.element.get_or_add_rPr().append(e)
            b = OxmlElement("w:bCs"); b.set(qn("w:val"), "1")
            s.element.get_or_add_rPr().append(b)
            s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            s.paragraph_format.keep_with_next = True
            s.paragraph_format.line_spacing = 1.15

    # ── header & footer ───────────────────────────────────────────────────
    def build_header_footer(self):
        sec = self.section
        sec.different_first_page_header_footer = True

        hdr = sec.header
        p = hdr.paragraphs[0]
        p.text = ""
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        tabs = p.paragraph_format.tab_stops
        tabs.add_tab_stop(self.text_width, 2)  # right aligned
        r = p.add_run(f"অধ্যায় {bn(self.ch)} · {self.ch_title}")
        set_run_font(r, size=Pt(9), color=GREY)
        r2 = p.add_run("\t" + self.book_title)
        set_run_font(r2, size=Pt(9), color=GREY, bold=True)
        para_border(p, "bottom", color="C9D3DC", sz=6, space=3)

        ftr = sec.footer
        fp = ftr.paragraphs[0]
        fp.text = ""
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = fp.add_run("")
        set_run_font(r, size=Pt(9), color=GREY)
        runs = field(fp, "PAGE", "1")
        for rr in runs:
            set_run_font(rr, size=Pt(10), color=NAVY, bold=True)
        para_border(fp, "top", color="C9D3DC", sz=6, space=3)

        # first page footer only
        fftr = sec.first_page_footer
        fpp = fftr.paragraphs[0]
        fpp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        runs = field(fpp, "PAGE", "1")
        for rr in runs:
            set_run_font(rr, size=Pt(10), color=NAVY, bold=True)

    # ── generic paragraph builders ────────────────────────────────────────
    def para(self, text="", size=BODY_SIZE, bold=False, italic=False,
             color=INK, align="justify", space_after=6, space_before=0,
             indent=0, first_line=0, style=None, font=BN_FONT):
        p = self.doc.add_paragraph(style=style)
        amap = {"justify": WD_ALIGN_PARAGRAPH.JUSTIFY, "left": WD_ALIGN_PARAGRAPH.LEFT,
                "center": WD_ALIGN_PARAGRAPH.CENTER, "right": WD_ALIGN_PARAGRAPH.RIGHT}
        p.alignment = amap[align]
        pf = p.paragraph_format
        pf.space_after = Pt(space_after); pf.space_before = Pt(space_before)
        pf.line_spacing = LINE_RULE
        if indent: pf.left_indent = Cm(indent)
        if first_line: pf.first_line_indent = Cm(first_line)
        if text:
            self._rich(p, text, size, bold, italic, color, font)
        return p

    def _rich(self, p, text, size, bold, italic, color, font=BN_FONT):
        """Supports **bold**, *italic*, `mono`, and __red__ inline markers."""
        import re
        tokens = re.split(r"(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`|__[^_]+?__)", text)
        for t in tokens:
            if not t:
                continue
            if t.startswith("**") and t.endswith("**"):
                set_run_font(p.add_run(t[2:-2]), font, size, True, italic, color)
            elif t.startswith("__") and t.endswith("__"):
                set_run_font(p.add_run(t[2:-2]), font, size, True, italic, RED)
            elif t.startswith("*") and t.endswith("*"):
                set_run_font(p.add_run(t[1:-1]), font, size, bold, True, color)
            elif t.startswith("`") and t.endswith("`"):
                set_run_font(p.add_run(t[1:-1]), MONO_FONT, Pt(size.pt - 0.5), bold, italic, NAVY)
            else:
                set_run_font(p.add_run(t), font, size, bold, italic, color)
        return p

    # ── headings ──────────────────────────────────────────────────────────
    def chapter_opener(self, objectives, intro, hero_image=None, hero_caption=None):
        """Full-width chapter title block + learning objectives."""
        d = self.doc
        # number strip
        t = d.add_table(rows=1, cols=1)
        t.autofit = False
        t.columns[0].width = self.text_width
        c = t.cell(0, 0)
        c.width = self.text_width
        cell_shade(c, NAVY_HEX)
        cell_margins(c, top=200, bottom=200, left=260, right=200)
        cell_borders(c, NAVY_HEX, 4)
        p0 = c.paragraphs[0]; p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_after = Pt(2)
        set_run_font(p0.add_run(f"অধ্যায়  {bn(self.ch)}"),
                     size=Pt(12), bold=True, color=RGBColor(0x9F, 0xC4, 0xE6), spacing=60)
        p1 = c.add_paragraph(); p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.space_after = Pt(0); p1.paragraph_format.line_spacing = 1.05
        set_run_font(p1.add_run(self.ch_title), size=Pt(26), bold=True,
                     color=RGBColor(0xFF, 0xFF, 0xFF))
        if self.subtitle:
            p2 = c.add_paragraph(); p2.paragraph_format.space_before = Pt(4)
            p2.paragraph_format.space_after = Pt(0)
            set_run_font(p2.add_run(self.subtitle), size=Pt(11.5),
                         color=RGBColor(0xC5, 0xDA, 0xEC), italic=True)
        self.spacer(8)

        if hero_image:
            self.figure(hero_image, hero_caption, width_cm=15.4)

        # objectives box
        self.objectives_box(objectives)
        self.spacer(4)
        for para in intro:
            self.para(para, first_line=0.0)

    def objectives_box(self, items):
        t = self.doc.add_table(rows=1, cols=1)
        t.autofit = False
        t.columns[0].width = self.text_width
        c = t.cell(0, 0); c.width = self.text_width
        cell_shade(c, "F2F6FA")
        cell_borders(c, STEEL_HEX, 4, edges=("left",))
        cell_borders(c, "D5E0EA", 4, edges=("top", "bottom", "right"))
        cell_margins(c, top=140, bottom=140, left=200, right=180)
        p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(5)
        set_run_font(p.add_run("এই অধ্যায় শেষে শিক্ষার্থী যা পারবে"),
                     size=Pt(12), bold=True, color=NAVY)
        for it in items:
            q = c.add_paragraph()
            q.paragraph_format.space_after = Pt(3)
            q.paragraph_format.left_indent = Cm(0.55)
            q.paragraph_format.first_line_indent = Cm(-0.55)
            q.paragraph_format.line_spacing = 1.2
            set_run_font(q.add_run("▸  "), size=Pt(10.5), color=STEEL, bold=True)
            self._rich(q, it, Pt(11), False, False, INK)
        no_split(t)
        return t

    def h1(self, text, num=None):
        p = self.doc.add_paragraph(style="Heading 1")
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(7)
        keep_with_next(p); keep_lines(p)
        if num:
            set_run_font(p.add_run(num + "  "), size=Pt(19), bold=True, color=STEEL)
        set_run_font(p.add_run(text), size=Pt(19), bold=True, color=NAVY)
        para_border(p, "bottom", NAVY_HEX, 10, 5)
        return p

    def h2(self, text, num=None):
        p = self.doc.add_paragraph(style="Heading 2")
        p.paragraph_format.space_before = Pt(13)
        p.paragraph_format.space_after = Pt(5)
        keep_with_next(p); keep_lines(p)
        if num:
            set_run_font(p.add_run(num + "  "), size=Pt(15), bold=True, color=STEEL)
        set_run_font(p.add_run(text), size=Pt(15), bold=True, color=NAVY)
        return p

    def h3(self, text, num=None):
        p = self.doc.add_paragraph(style="Heading 3")
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        keep_with_next(p); keep_lines(p)
        if num:
            set_run_font(p.add_run(num + "  "), size=Pt(12.5), bold=True, color=STEEL)
        set_run_font(p.add_run(text), size=Pt(12.5), bold=True, color=STEEL)
        return p

    def h4(self, text):
        p = self.doc.add_paragraph(style="Heading 4")
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        keep_with_next(p)
        set_run_font(p.add_run(text), size=Pt(11.8), bold=True, color=RGBColor(0x2A, 0x2A, 0x2A))
        return p

    # ── lists ─────────────────────────────────────────────────────────────
    def bullets(self, items, indent=0.6, bullet="•", size=BODY_SIZE, tight=False):
        out = []
        for it in items:
            p = self.doc.add_paragraph()
            pf = p.paragraph_format
            pf.left_indent = Cm(indent + 0.55)
            pf.first_line_indent = Cm(-0.55)
            pf.space_after = Pt(2 if tight else 4)
            pf.line_spacing = 1.25
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            set_run_font(p.add_run(f"{bullet}  "), size=size, bold=True, color=STEEL)
            self._rich(p, it, size, False, False, INK)
            out.append(p)
        return out

    def numbered(self, items, indent=0.6, size=BODY_SIZE, start=1, tight=False):
        out = []
        for i, it in enumerate(items, start):
            p = self.doc.add_paragraph()
            pf = p.paragraph_format
            pf.left_indent = Cm(indent + 0.75)
            pf.first_line_indent = Cm(-0.75)
            pf.space_after = Pt(2 if tight else 4)
            pf.line_spacing = 1.25
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            set_run_font(p.add_run(f"{bn(i)}.  "), size=size, bold=True, color=STEEL)
            self._rich(p, it, size, False, False, INK)
            out.append(p)
        return out

    # ── callout box ───────────────────────────────────────────────────────
    def box(self, kind, body, title=None, items=None):
        fill, border, tcol = BOX_TINTS[kind]
        t = self.doc.add_table(rows=1, cols=1)
        t.autofit = False
        t.columns[0].width = self.text_width
        c = t.cell(0, 0); c.width = self.text_width
        cell_shade(c, fill)
        cell_borders(c, border, 12, edges=("left",))
        cell_borders(c, border, 4, edges=("top", "bottom", "right"))
        cell_margins(c, top=130, bottom=130, left=200, right=170)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.2
        set_run_font(p.add_run(title or BOX_LABEL[kind]),
                     size=Pt(11.5), bold=True, color=RGBColor.from_string(tcol))
        if body:
            # a newline means a new paragraph — a soft break inside a justified
            # paragraph gets its last line stretched across the full width
            parts = [x for x in body.split("\n") if x.strip()]
            for k, part in enumerate(parts):
                q = c.add_paragraph()
                last = (k == len(parts) - 1)
                q.paragraph_format.space_after = Pt((0 if not items else 4) if last else 4)
                q.paragraph_format.line_spacing = 1.28
                q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                self._rich(q, part, Pt(11), False, False, INK)
        if items:
            for i, it in enumerate(items):
                q = c.add_paragraph()
                q.paragraph_format.space_after = Pt(0 if i == len(items) - 1 else 2)
                q.paragraph_format.left_indent = Cm(0.5)
                q.paragraph_format.first_line_indent = Cm(-0.5)
                q.paragraph_format.line_spacing = 1.22
                q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                set_run_font(q.add_run("▪  "), size=Pt(10.5), bold=True,
                             color=RGBColor.from_string(tcol))
                self._rich(q, it, Pt(11), False, False, INK)
        no_split(t)
        self.spacer(5)
        return t

    # ── vector (SVG) pictures ─────────────────────────────────────────────
    def _add_svg(self, run, png_path, svg_path, width):
        """Insert a picture that carries the real SVG plus a PNG fallback.

        Word renders the vector (crisp at any zoom / print size) and
        'Convert to Shape' on it turns the whole diagram into editable shapes.
        Older readers fall back to the PNG automatically.
        """
        shape = run.add_picture(png_path, width=width)
        doc_part = self.doc.part
        self._svg_seq = getattr(self, "_svg_seq", 0) + 1
        name = f"bookdia{self._svg_seq}.svg"
        partname = PackURI(f"/word/media/{name}")
        with open(svg_path, "rb") as fh:
            blob = fh.read()
        svg_part = Part(partname, "image/svg+xml", blob, doc_part.package)
        rId = doc_part.relate_to(svg_part, RT.IMAGE)

        blip = shape._inline.graphic.graphicData.pic.blipFill.find(qn("a:blip"))
        extLst = blip.find(qn("a:extLst"))
        if extLst is None:
            extLst = OxmlElement("a:extLst")
            blip.append(extLst)
        ext = OxmlElement("a:ext")
        ext.set("uri", SVG_EXT_URI)
        svg_blip = etree_svgblip(rId)
        ext.append(svg_blip)
        extLst.append(ext)
        return shape

    # ── figures ───────────────────────────────────────────────────────────
    def figure(self, path, caption=None, width_cm=None, border=True,
               center=True, float_=False):
        """path may be a .png (a sibling .svg is used as the vector when present)."""
        self.fig_n += 1
        label = f"চিত্র {bn(self.ch)}.{bn(self.fig_n)}"
        if width_cm is None:
            width_cm = 12.5
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        keep_with_next(p)
        r = p.add_run()
        svg = os.path.splitext(path)[0] + ".svg"
        if path.lower().endswith(".png") and os.path.exists(svg):
            self._add_svg(r, path, svg, Cm(width_cm))
        else:
            r.add_picture(path, width=Cm(width_cm))
        if caption:
            cp = self.doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_after = Pt(9)
            cp.paragraph_format.space_before = Pt(0)
            cp.paragraph_format.line_spacing = 1.15
            set_run_font(cp.add_run(label + ": "), size=Pt(9.5), bold=True, color=NAVY)
            set_run_font(cp.add_run(caption), size=Pt(9.5), color=GREY, italic=True)
            self.figures.append((label, caption))
        if float_:
            # image + caption become one frame that reflows instead of
            # stranding a blank band at the foot of the previous page
            tw_ = int(Cm(width_cm + 0.3).twips)
            frame_para(p, tw_, space_before=int(Pt(7).twips))
            if caption:
                frame_para(cp, tw_, space_before=int(Pt(7).twips))
        return label

    def figure_row(self, items, per_row=3, width_cm=None, caption=None,
                   thumb_labels=True):
        """items = [(path, label_text), ...] laid out in a borderless grid."""
        n = len(items)
        rows = (n + per_row - 1) // per_row
        tw = self.text_width
        colw = int(tw / per_row)
        img_w = width_cm or (colw / 360000 - 0.45)
        t = self.doc.add_table(rows=rows * (2 if thumb_labels else 1), cols=per_row)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        for r in range(len(t.rows)):
            for cidx in range(per_row):
                t.cell(r, cidx).width = colw
        for idx, (path, lbl) in enumerate(items):
            r = idx // per_row
            cidx = idx % per_row
            rr = r * (2 if thumb_labels else 1)
            c = t.cell(rr, cidx); c.width = colw
            cell_margins(c, 40, 20, 60, 60)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.add_run().add_picture(path, width=Cm(img_w))
            if thumb_labels:
                c2 = t.cell(rr + 1, cidx); c2.width = colw
                cell_margins(c2, 10, 70, 60, 60)
                p2 = c2.paragraphs[0]
                p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p2.paragraph_format.space_after = Pt(0)
                p2.paragraph_format.line_spacing = 1.1
                set_run_font(p2.add_run(lbl), size=Pt(9.5), bold=True, color=NAVY)
        no_split(t)
        if caption:
            self.fig_n += 1
            label = f"চিত্র {bn(self.ch)}.{bn(self.fig_n)}"
            cp = self.doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_before = Pt(3)
            cp.paragraph_format.space_after = Pt(9)
            set_run_font(cp.add_run(label + ": "), size=Pt(9.5), bold=True, color=NAVY)
            set_run_font(cp.add_run(caption), size=Pt(9.5), color=GREY, italic=True)
            self.figures.append((label, caption))
        return t

    # ── tables ────────────────────────────────────────────────────────────
    def table(self, headers, rows, caption=None, widths=None, align=None,
              size=Pt(10.5), header_fill=NAVY_HEX, zebra="F4F7FA",
              caption_above=True, col_colors=None):
        if caption and caption_above:
            self.tab_n += 1
            label = f"সারণি {bn(self.ch)}.{bn(self.tab_n)}"
            cp = self.doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.LEFT
            cp.paragraph_format.space_before = Pt(9)
            cp.paragraph_format.space_after = Pt(3)
            keep_with_next(cp)
            set_run_font(cp.add_run(label + ": "), size=Pt(10), bold=True, color=NAVY)
            set_run_font(cp.add_run(caption), size=Pt(10), color=RGBColor(0x33, 0x33, 0x33))
            self.tables.append((label, caption))

        ncol = len(headers)
        t = self.doc.add_table(rows=1 + len(rows), cols=ncol)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        tw = self.text_width
        if widths:
            tot = sum(widths)
            ws = [int(tw * w / tot) for w in widths]
        else:
            ws = [int(tw / ncol)] * ncol
        # header
        for i, h in enumerate(headers):
            c = t.cell(0, i); c.width = ws[i]
            cell_shade(c, header_fill)
            cell_borders(c, header_fill, 6)
            cell_margins(c, 70, 70, 100, 100)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            self._rich(p, h, Pt(size.pt), True, False, RGBColor(0xFF, 0xFF, 0xFF))
            for r in p.runs:
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        # body
        for ri, row in enumerate(rows):
            for ci, val in enumerate(row):
                c = t.cell(ri + 1, ci); c.width = ws[ci]
                cell_borders(c, "C8D2DC", 4)
                cell_margins(c, 60, 60, 100, 100)
                if zebra and ri % 2 == 1:
                    cell_shade(c, zebra)
                p = c.paragraphs[0]
                a = (align[ci] if align else ("left" if ci == 0 else "center"))
                p.alignment = {"left": WD_ALIGN_PARAGRAPH.LEFT,
                               "center": WD_ALIGN_PARAGRAPH.CENTER,
                               "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
                               "right": WD_ALIGN_PARAGRAPH.RIGHT}[a]
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.2
                col = INK
                if col_colors and col_colors.get(ci):
                    col = col_colors[ci]
                self._rich(p, str(val), Pt(size.pt), False, False, col)
        no_split(t)
        # repeat header row on page break
        trPr = t.rows[0]._tr.get_or_add_trPr()
        th = OxmlElement("w:tblHeader"); th.set(qn("w:val"), "true"); trPr.append(th)

        if caption and not caption_above:
            self.tab_n += 1
            label = f"সারণি {bn(self.ch)}.{bn(self.tab_n)}"
            cp = self.doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_after = Pt(9)
            set_run_font(cp.add_run(label + ": "), size=Pt(9.5), bold=True, color=NAVY)
            set_run_font(cp.add_run(caption), size=Pt(9.5), color=GREY, italic=True)
            self.tables.append((label, caption))
        else:
            self.spacer(7)
        return t

    # ── editable "diagrams" built from native Word tables ─────────────────
    #
    #    Anything whose content is only text and boxes is built here rather
    #    than drawn as a picture, so the reader can retype a label, recolour a
    #    box or add a row with ordinary Word editing.
    #
    def _panel_cell(self, cell, title=None, items=None, body=None,
                    fill="F5F9FC", border=STEEL_HEX, tcolor=None,
                    title_size=Pt(11.5), size=Pt(10.5), accent_top=False):
        cell_shade(cell, fill)
        cell_borders(cell, border, 8)
        cell_margins(cell, 110, 110, 150, 150)
        first = cell.paragraphs[0]
        used = False
        if title is not None:
            p = first
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(4 if (items or body) else 0)
            p.paragraph_format.line_spacing = 1.15
            set_run_font(p.add_run(title), size=title_size, bold=True,
                         color=tcolor or NAVY)
            used = True
        if body:
            p = first if not used else cell.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.25
            self._rich(p, body, size, False, False, INK)
            used = True
        for i, it in enumerate(items or []):
            p = first if not used else cell.add_paragraph()
            used = True
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0 if i == len(items) - 1 else 3)
            p.paragraph_format.left_indent = Cm(0.42)
            p.paragraph_format.first_line_indent = Cm(-0.42)
            p.paragraph_format.line_spacing = 1.22
            set_run_font(p.add_run("▪  "), size=Pt(size.pt - 1), bold=True,
                         color=RGBColor.from_string(border))
            self._rich(p, it, size, False, False, INK)
        return cell

    def tree_cols(self, root, columns, caption=None, colors=None):
        """Root box + N colour-coded columns of bullets. Fully editable."""
        colors = colors or [(STEEL_HEX, "E8F0F8"), (AMBER_HEX, "FFF6E5"),
                            (GREEN_HEX, "EAF6EF"), (RED_HEX, "FDECEA")]
        n = len(columns)
        t = self.doc.add_table(rows=3, cols=n)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        colw = int(self.text_width / n)
        for r in range(3):
            for c in range(n):
                t.cell(r, c).width = colw
        # root spans the full width
        root_cell = t.cell(0, 0)
        for c in range(1, n):
            root_cell = root_cell.merge(t.cell(0, c))
        cell_shade(root_cell, NAVY_HEX)
        cell_borders(root_cell, NAVY_HEX, 8)
        cell_margins(root_cell, 130, 130, 150, 150)
        p = root_cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        set_run_font(p.add_run(root), size=Pt(13.5), bold=True,
                     color=RGBColor(0xFF, 0xFF, 0xFF))
        for i, (head, items) in enumerate(columns):
            border, fill = colors[i % len(colors)]
            hc = t.cell(1, i); hc.width = colw
            cell_shade(hc, border)
            cell_borders(hc, border, 8)
            cell_margins(hc, 90, 90, 120, 120)
            hp = hc.paragraphs[0]
            hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            hp.paragraph_format.space_after = Pt(0)
            set_run_font(hp.add_run(head), size=Pt(11.5), bold=True,
                         color=RGBColor(0xFF, 0xFF, 0xFF))
            self._panel_cell(t.cell(2, i), items=items, fill=fill,
                             border=border, size=Pt(10))
            t.cell(2, i).width = colw
        no_split(t)
        self._diagram_caption(caption)
        return t

    def concept_cards(self, cards, caption=None, colors=None):
        """N side-by-side cards: heading strip + subtitle + description."""
        colors = colors or [(STEEL_HEX, "E8F0F8"), (GREEN_HEX, "EAF6EF"),
                            (AMBER_HEX, "FFF6E5"), (RED_HEX, "FDECEA")]
        n = len(cards)
        t = self.doc.add_table(rows=2, cols=n)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        colw = int(self.text_width / n)
        for r in range(2):
            for c in range(n):
                t.cell(r, c).width = colw
        for i, (title, sub, desc) in enumerate(cards):
            border, fill = colors[i % len(colors)]
            hc = t.cell(0, i); hc.width = colw
            cell_shade(hc, border)
            cell_borders(hc, border, 8)
            cell_margins(hc, 100, 100, 120, 120)
            hp = hc.paragraphs[0]
            hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            hp.paragraph_format.space_after = Pt(0)
            set_run_font(hp.add_run(title), size=Pt(12), bold=True,
                         color=RGBColor(0xFF, 0xFF, 0xFF))
            bc = t.cell(1, i); bc.width = colw
            cell_shade(bc, fill)
            cell_borders(bc, border, 8)
            cell_margins(bc, 110, 120, 140, 140)
            p = bc.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            set_run_font(p.add_run(sub), size=Pt(10.5), bold=True,
                         color=RGBColor.from_string(border))
            q = bc.add_paragraph()
            q.alignment = WD_ALIGN_PARAGRAPH.CENTER
            q.paragraph_format.space_after = Pt(0)
            q.paragraph_format.line_spacing = 1.25
            self._rich(q, desc, Pt(10.5), False, False, INK)
        no_split(t)
        self._diagram_caption(caption)
        return t

    def flow_steps(self, steps, caption=None, per_row=None, color=STEEL_HEX):
        """Numbered step chain with arrows between. Editable text everywhere."""
        n = len(steps)
        per_row = per_row or n
        rows_of = [steps[i:i + per_row] for i in range(0, n, per_row)]
        ncols = per_row * 2 - 1
        t = self.doc.add_table(rows=len(rows_of), cols=ncols)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        arrow_w = int(Cm(0.62))
        step_w = int((self.text_width - arrow_w * (per_row - 1)) / per_row)
        idx = 0
        for r, row in enumerate(rows_of):
            for c in range(ncols):
                t.cell(r, c).width = arrow_w if c % 2 else step_w
            for k, step in enumerate(row):
                idx += 1
                title, desc = (step if isinstance(step, (tuple, list))
                               else (step, None))
                cell = t.cell(r, k * 2); cell.width = step_w
                cell_shade(cell, "F5F9FC")
                cell_borders(cell, color, 8)
                cell_margins(cell, 100, 100, 90, 90)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.1
                set_run_font(p.add_run(f"{bn(idx)}"), size=Pt(13), bold=True,
                             color=RGBColor.from_string(color))
                q = cell.add_paragraph()
                q.alignment = WD_ALIGN_PARAGRAPH.CENTER
                q.paragraph_format.space_after = Pt(0 if not desc else 3)
                q.paragraph_format.line_spacing = 1.15
                set_run_font(q.add_run(title), size=Pt(10.5), bold=True, color=NAVY)
                if desc:
                    d = cell.add_paragraph()
                    d.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    d.paragraph_format.space_after = Pt(0)
                    d.paragraph_format.line_spacing = 1.2
                    set_run_font(d.add_run(desc), size=Pt(9.5), color=GREY)
                if k * 2 + 1 < ncols:
                    ac = t.cell(r, k * 2 + 1); ac.width = arrow_w
                    cell_borders(ac, "FFFFFF", 2)
                    cell_margins(ac, 0, 0, 10, 10)
                    ap = ac.paragraphs[0]
                    ap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    ap.paragraph_format.space_after = Pt(0)
                    # Arial carries the arrow glyph; Kalpurush does not
                    set_run_font(ap.add_run("➜"), name="Arial", size=Pt(14),
                                 bold=True, color=RGBColor.from_string(color))
        no_split(t)
        self._diagram_caption(caption)
        return t

    def _diagram_caption(self, caption):
        if not caption:
            self.spacer(7)
            return
        self.fig_n += 1
        label = f"চিত্র {bn(self.ch)}.{bn(self.fig_n)}"
        cp = self.doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(4)
        cp.paragraph_format.space_after = Pt(9)
        set_run_font(cp.add_run(label + ": "), size=Pt(9.5), bold=True, color=NAVY)
        set_run_font(cp.add_run(caption), size=Pt(9.5), color=GREY, italic=True)
        self.figures.append((label, caption))

    # ── multiple-choice question ──────────────────────────────────────────
    def mcq(self, n, question, options, cols=2):
        """Question + a borderless option grid, so long options never wrap raggedly."""
        p = self.para(f"**{bn(n)}.**  {question}", space_after=3, space_before=5)
        keep_with_next(p)
        letters = ["ক", "খ", "গ", "ঘ", "ঙ"]
        rows = (len(options) + cols - 1) // cols
        t = self.doc.add_table(rows=rows, cols=cols)
        t.autofit = False
        avail = self.text_width - Cm(0.9)
        colw = int(avail / cols)
        for r in range(rows):
            for c in range(cols):
                t.cell(r, c).width = colw
        for i, opt in enumerate(options):
            c = t.cell(i // cols, i % cols)
            c.width = colw
            cell_margins(c, 20, 20, 140, 60)
            q = c.paragraphs[0]
            q.alignment = WD_ALIGN_PARAGRAPH.LEFT
            q.paragraph_format.space_after = Pt(0)
            q.paragraph_format.line_spacing = 1.2
            q.paragraph_format.left_indent = Cm(0.5)
            q.paragraph_format.first_line_indent = Cm(-0.5)
            set_run_font(q.add_run(f"({letters[i]}) "), size=Pt(10.5),
                         bold=True, color=STEEL)
            self._rich(q, opt, Pt(10.5), False, False, INK)
        no_split(t)
        self.spacer(3)
        return t

    # ── mathematics, set the way a textbook sets it ───────────────────────
    def math(self, expr, align="center", size=None, before=6, after=6):
        """A display equation with real fractions (Office Math)."""
        p = self.doc.add_paragraph()
        el = _omml_paragraph(expr, align, size, before, after)
        p._p.addnext(el)
        p._p.getparent().remove(p._p)
        return el

    def worked_example(self, num, question, given=None, find=None,
                       steps=None, answer=None, note=None):
        """A fully worked example: প্রদত্ত → নির্ণেয় → সমাধান → উত্তর.

        `steps` are display equations in the math DSL; the reader sees a
        stacked fraction and an aligned chain of equalities rather than a
        run-on line of text.
        """
        self.eq_n = getattr(self, "eq_n", 0)
        t = self.doc.add_table(rows=1, cols=1)
        t.autofit = False
        t.columns[0].width = self.text_width
        c = t.cell(0, 0); c.width = self.text_width
        cell_shade(c, "F7F9FB")
        cell_borders(c, STEEL_HEX, 10, edges=("left",))
        cell_borders(c, "D5DEE6", 4, edges=("top", "bottom", "right"))
        cell_margins(c, 150, 150, 210, 190)

        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(4)
        set_run_font(p.add_run(f"উদাহরণ {bn(self.ch)}.{bn(num)}"),
                     size=Pt(12), bold=True, color=NAVY)

        q = c.add_paragraph()
        q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        q.paragraph_format.space_after = Pt(7)
        q.paragraph_format.line_spacing = 1.28
        self._rich(q, question, Pt(11), False, False, INK)

        for label, items in (("প্রদত্ত", given), ("নির্ণেয়", find)):
            if not items:
                continue
            r = c.add_paragraph()
            r.paragraph_format.space_after = Pt(2)
            r.paragraph_format.left_indent = Cm(1.7)
            r.paragraph_format.first_line_indent = Cm(-1.7)
            r.paragraph_format.line_spacing = 1.25
            set_run_font(r.add_run(label + " : "), size=Pt(11), bold=True,
                         color=STEEL)
            self._rich(r, "   ".join(items) if isinstance(items, (list, tuple))
                       else items, Pt(11), False, False, INK)

        if steps:
            h = c.add_paragraph()
            h.paragraph_format.space_before = Pt(6)
            h.paragraph_format.space_after = Pt(0)
            set_run_font(h.add_run("সমাধান :"), size=Pt(11), bold=True, color=STEEL)
            for k, st in enumerate(steps):
                el = _omml_paragraph(st, "center", None,
                                     before=(4 if k == 0 else 2), after=2)
                c._tc.append(el)

        if answer:
            a = c.add_paragraph()
            a.paragraph_format.space_before = Pt(6)
            a.paragraph_format.space_after = Pt(0)
            a.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_run_font(a.add_run("উত্তর : "), size=Pt(11), bold=True, color=GREEN)
            self._rich(a, answer, Pt(11.5), True, False, NAVY)

        if note:
            n = c.add_paragraph()
            n.paragraph_format.space_before = Pt(5)
            n.paragraph_format.space_after = Pt(0)
            n.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            n.paragraph_format.line_spacing = 1.25
            self._rich(n, note, Pt(10.5), False, True, GREY)

        no_split(t)
        self.spacer(7)
        return t

    # ── equation ──────────────────────────────────────────────────────────
    def equation(self, expr, number=True, note=None):
        self.eq_n += 1
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        tabs = p.paragraph_format.tab_stops
        tabs.add_tab_stop(self.text_width, 2)
        set_run_font(p.add_run(expr), size=Pt(13), bold=True, color=NAVY)
        if number:
            set_run_font(p.add_run(f"\t({bn(self.ch)}.{bn(self.eq_n)})"),
                         size=Pt(10.5), color=GREY)
        if note:
            q = self.doc.add_paragraph()
            q.alignment = WD_ALIGN_PARAGRAPH.CENTER
            q.paragraph_format.space_after = Pt(8)
            set_run_font(q.add_run(note), size=Pt(10), italic=True, color=GREY)
        return p

    # ── misc ──────────────────────────────────────────────────────────────
    def spacer(self, pts=6):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        set_run_font(p.add_run(""), size=Pt(pts))
        return p

    def rule(self, color="C9D3DC", sz=6):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        set_run_font(p.add_run(""), size=Pt(1))
        para_border(p, "bottom", color, sz, 1)
        return p

    def page_break(self):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.add_run().add_break(WD_BREAK.PAGE)
        return p

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.doc.save(path)
        return path


# ────────────────────────────────────────────────────────────────────────────
#  Office Math (OMML) — real fractions, so worked examples look like a
#  printed textbook rather than a line of plain text.
# ────────────────────────────────────────────────────────────────────────────
from docx.oxml import parse_xml
from docx.oxml.ns import nsmap as _NSMAP

M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
_NSMAP.setdefault("m", M_NS)
_MDECL = ('xmlns:m="%s" xmlns:w="http://schemas.openxmlformats.org/'
          'wordprocessingml/2006/main"' % M_NS)


def _mrun(text, italic=False, upright=False, font=BN_FONT, size=None):
    """One OMML run.

    `upright` emits <m:nor/>, which tells the math layout engine to treat the
    run as ordinary text — without it Word/LibreOffice inserts operator spacing
    around things like the decimal point and sets unit letters in italics.
    """
    props = ""
    if upright:
        props += "<m:nor/>"
    mrpr = f"<m:rPr>{props}</m:rPr>" if props else ""
    it = "<w:i/>" if italic else ""
    sz = ""
    if size:
        sz = f'<w:sz w:val="{int(size*2)}"/><w:szCs w:val="{int(size*2)}"/>'
    esc = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return (f'<m:r>{mrpr}<w:rPr><w:rFonts w:ascii="{font}" w:hAnsi="{font}" '
            f'w:cs="{font}"/>{it}{sz}</w:rPr>'
            f'<m:t xml:space="preserve">{esc}</m:t></m:r>')


def _brace(expr, i):
    """Read a {...} group starting at expr[i] == '{'. Returns (content, next)."""
    depth, out, j = 1, "", i + 1
    while j < len(expr) and depth:
        if expr[j] == "{":
            depth += 1
        elif expr[j] == "}":
            depth -= 1
            if depth == 0:
                break
        out += expr[j]
        j += 1
    return out, j + 1


_MATH_CMD = {
    r"\times": "×", r"\cdot": "·", r"\approx": "≈", r"\neq": "≠",
    r"\leq": "≤", r"\geq": "≥", r"\pm": "±", r"\degree": "°",
    r"\Omega": "Ω", r"\ohm": "Ω", r"\rho": "ρ", r"\mu": "µ",
    r"\alpha": "α", r"\Delta": "Δ", r"\pi": "π", r"\to": "→",
    r"\qquad": "  ", r"\quad": " ",
}


def _math_tokens(expr, size=None):
    r"""Small DSL → OMML.

      \frac{a}{b}   real stacked fraction
      \sqrt{a}      square root
      ^{x}          superscript
      _{x}          subscript  (R_{T}, V_{AB} — always brace the index)
      `text`        upright (units, words) — everything else that is a bare
                    Latin letter is set italic, the way variables are printed.
    """
    out, i = [], 0
    while i < len(expr):
        if expr.startswith(r"\frac{", i):
            num, j = _brace(expr, i + 5)
            den = ""
            if j < len(expr) and expr[j] == "{":
                den, j = _brace(expr, j)
            # numerator/denominator each wrapped in a one-row equation array:
            # LibreOffice left-aligns a bare <m:num>, so a short numerator over
            # a long denominator sat at the far left.  Inside <m:eqArr> both
            # renderers centre it.
            out.append('<m:f><m:fPr><m:type m:val="bar"/></m:fPr>'
                       f"<m:num><m:eqArr><m:e>{_math_tokens(num, size)}</m:e>"
                       "</m:eqArr></m:num>"
                       f"<m:den><m:eqArr><m:e>{_math_tokens(den, size)}</m:e>"
                       "</m:eqArr></m:den></m:f>")
            i = j
        elif expr.startswith(r"\sqrt{", i):
            rad, j = _brace(expr, i + 5)
            # A real <m:rad>, not a "√" character: Kalpurush has no U+221A
            # (verified against the font's cmap), so a literal radical sign
            # would fall off the font.  degHide draws the plain square-root
            # sign with no index, in both Word and LibreOffice.
            out.append("<m:rad><m:radPr><m:degHide m:val=\"1\"/></m:radPr>"
                       "<m:deg/>"
                       f"<m:e>{_math_tokens(rad, size)}</m:e></m:rad>")
            i = j
        elif expr.startswith("^{", i):
            sup, j = _brace(expr, i + 1)
            base = out.pop() if out else _mrun("", size=size)
            out.append(f"<m:sSup><m:e>{base}</m:e>"
                       f"<m:sup>{_math_tokens(sup, size)}</m:sup></m:sSup>")
            i = j
        elif expr.startswith("_{", i):
            sub, j = _brace(expr, i + 1)
            base = out.pop() if out else _mrun("", size=size)
            out.append(f"<m:sSub><m:e>{base}</m:e>"
                       f"<m:sub>{_math_tokens(sub, size)}</m:sub></m:sSub>")
            i = j
        elif expr[i] == "\\" and not expr.startswith(r"\frac{", i):
            for cmd, ch in _MATH_CMD.items():
                if expr.startswith(cmd, i):
                    out.append(_mrun(ch, upright=True, size=size))
                    i += len(cmd)
                    break
            else:
                out.append(_mrun("\\", upright=True, size=size))
                i += 1
        elif expr[i] == "`":
            j = expr.find("`", i + 1)
            j = len(expr) if j < 0 else j
            out.append(_mrun(expr[i + 1:j], upright=True, size=size))
            i = j + 1
        else:
            k = i
            while k < len(expr) and expr[k] not in "`\\" \
                    and not expr.startswith("^{", k) \
                    and not expr.startswith("_{", k):
                k += 1
            chunk = expr[i:k]
            buf, mode = "", None
            for ch in chunk:
                m = "var" if (ch.isascii() and ch.isalpha()) else "txt"
                if mode is None:
                    mode = m
                if m != mode:
                    out.append(_mrun(buf, italic=(mode == "var"),
                                     upright=(mode == "txt"), size=size))
                    buf, mode = "", m
                buf += ch
            if buf:
                out.append(_mrun(buf, italic=(mode == "var"),
                                 upright=(mode == "txt"), size=size))
            i = k
    return "".join(out)


def _omml_paragraph(expr, align="center", size=None, before=6, after=6):
    jc = {"center": "center", "left": "left", "right": "right"}[align]
    return parse_xml(
        f'<w:p {_MDECL}><w:pPr><w:spacing w:before="{int(before*20)}" '
        f'w:after="{int(after*20)}"/><w:jc w:val="{jc}"/></w:pPr>'
        f'<m:oMathPara><m:oMathParaPr><m:jc m:val="{jc}"/></m:oMathParaPr>'
        f'<m:oMath>{_math_tokens(expr, size)}</m:oMath></m:oMathPara></w:p>')
