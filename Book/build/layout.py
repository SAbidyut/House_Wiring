# -*- coding: utf-8 -*-
"""layout.py — measure a built chapter and close the blank gaps.

Word pushes a figure to the next page whenever it does not fit in the space
left, which leaves a tall band of white at the foot of the previous page.
This module converts the .docx to PDF, measures that band on every page, and
reports which figure caused it, so the build can shrink that one figure just
enough to pull it back up.
"""
import os, subprocess, sys, glob, json
import pymupdf

PT_CM = 28.3465


def to_pdf(docx_path, outdir):
    os.makedirs(outdir, exist_ok=True)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                    "--outdir", outdir, docx_path],
                   capture_output=True, text=True, timeout=600)
    stem = os.path.splitext(os.path.basename(docx_path))[0]
    pdf = os.path.join(outdir, stem + ".pdf")
    return pdf if os.path.exists(pdf) else None


def page_report(pdf, bottom_margin_cm=2.0, footer_reserve_cm=1.2):
    """Per page: bottom of the last real content block and the gap under it."""
    doc = pymupdf.open(pdf)
    out = []
    for i, page in enumerate(doc):
        H = page.rect.height
        limit = H - (bottom_margin_cm + footer_reserve_cm) * PT_CM
        bottom = 0.0
        for b in page.get_text("blocks"):
            x0, y0, x1, y1 = b[:4]
            if y1 < limit:
                bottom = max(bottom, y1)
        for d in page.get_drawings():
            r = d["rect"]
            if r.y1 < limit:
                bottom = max(bottom, r.y1)
        for img in page.get_images(full=True):
            for r in page.get_image_rects(img[0]):
                if r.y1 < limit:
                    bottom = max(bottom, r.y1)
        out.append({"page": i + 1,
                    "bottom_cm": round(bottom / PT_CM, 2),
                    "gap_cm": round((limit - bottom) / PT_CM, 2)})
    doc.close()
    return out


def first_image_height_cm(pdf, page_no):
    """Height of the first image on a page — the figure that got pushed."""
    doc = pymupdf.open(pdf)
    page = doc[page_no - 1]
    best = None
    for img in page.get_images(full=True):
        for r in page.get_image_rects(img[0]):
            if best is None or r.y0 < best[0]:
                best = (r.y0, r.height / PT_CM, r.width / PT_CM)
    doc.close()
    return best


def report(docx_path, outdir, gap_threshold=3.5, verbose=True):
    pdf = to_pdf(docx_path, outdir)
    if not pdf:
        raise RuntimeError("PDF conversion failed")
    rows = page_report(pdf)
    bad = [r for r in rows if r["gap_cm"] > gap_threshold and r["page"] < len(rows)]
    if verbose:
        print(f"pages: {len(rows)}")
        for r in bad:
            nxt = first_image_height_cm(pdf, r["page"] + 1)
            extra = ""
            if nxt:
                extra = (f"  → next page starts with an image "
                         f"{nxt[2]:.1f}×{nxt[1]:.1f} cm")
            print(f"  p{r['page']:>3}  gap {r['gap_cm']:>5.2f} cm{extra}")
        if not bad:
            print("  no page has a gap above threshold ✓")
    return pdf, rows, bad


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob("out/*.docx"))[0]
    report(d, "out/_pdf", float(sys.argv[2]) if len(sys.argv) > 2 else 3.5)
