# -*- coding: utf-8 -*-
"""tune.py — shrink the specific figures that leave blank bands.

Builds the chapter, measures every page, and for each page whose foot is left
empty because the next page opens with a figure, scales that one figure down
just enough to pull it back onto the page. Repeats until nothing improves.
Widths live in figwidths_<chapter>.json, which the chapter module reads.
"""
import json, os, subprocess, sys, importlib
import pymupdf
from layout import to_pdf, page_report, PT_CM

HERE = os.path.dirname(os.path.abspath(__file__))
CAPTION_CM = 1.15          # caption line + spacing under a figure
MIN_SCALE = 0.58           # never shrink a figure below this fraction


def figures_on_page(pdf, page_no, top_cm=5.0):
    """Bounding box of the graphic that opens a page.

    An embedded SVG is drawn by LibreOffice as vector operations, not as an
    image, so raster detection alone misses exactly the figures we care about.
    Vector ops are clustered by vertical continuity and the topmost cluster is
    returned alongside any real images.
    """
    doc = pymupdf.open(pdf)
    page = doc[page_no - 1]
    out = []
    for img in page.get_images(full=True):
        for r in page.get_image_rects(img[0]):
            out.append({"y0": r.y0 / PT_CM, "y1": r.y1 / PT_CM,
                        "h": r.height / PT_CM, "w": r.width / PT_CM})

    rects = [d["rect"] for d in page.get_drawings()
             if d["rect"].height > 0.6 and d["rect"].width > 0.6]
    rects.sort(key=lambda r: r.y0)
    cluster = []
    for r in rects:
        if not cluster:
            cluster.append(r)
            continue
        cy1 = max(x.y1 for x in cluster)
        if r.y0 <= cy1 + 14:          # still part of the same graphic
            cluster.append(r)
        else:
            break
    if cluster:
        x0 = min(r.x0 for r in cluster); x1 = max(r.x1 for r in cluster)
        y0 = min(r.y0 for r in cluster); y1 = max(r.y1 for r in cluster)
        out.append({"y0": y0 / PT_CM, "y1": y1 / PT_CM,
                    "h": (y1 - y0) / PT_CM, "w": (x1 - x0) / PT_CM})
    doc.close()
    out = [o for o in out if o["y0"] < top_cm]
    return sorted(out, key=lambda d: d["y0"])


def run(chapter="ch01", rounds=4, threshold=3.2):
    wpath = os.path.join(HERE, f"figwidths_{chapter}.json")
    mod = importlib.import_module(chapter)
    widths = dict(mod.W)
    if os.path.exists(wpath):
        widths.update(json.load(open(wpath)))
    base = dict(mod.W)

    for rnd in range(1, rounds + 1):
        json.dump(widths, open(wpath, "w"), indent=1)
        importlib.reload(mod)
        docx, _ = mod.build()
        pdf = to_pdf(docx, os.path.join(HERE, "out", "_pdf"))
        rows = page_report(pdf)
        bad = [r for r in rows if r["gap_cm"] > threshold and r["page"] < len(rows)]
        print(f"round {rnd}: {len(rows)} pages, {len(bad)} gaps "
              f"{[ (r['page'], r['gap_cm']) for r in bad ]}")
        if not bad:
            break
        changed = False
        for r in bad:
            figs = figures_on_page(pdf, r["page"] + 1)
            if not figs or figs[0]["y0"] > 4.0:
                continue                      # page does not open with a figure
            f = figs[0]
            target_h = r["gap_cm"] - CAPTION_CM - 0.35
            if target_h <= 1.5:
                continue
            scale = target_h / f["h"]
            if scale >= 0.995:
                continue
            # find the width key whose current value matches this figure
            key = min(widths, key=lambda k: abs(widths[k] - f["w"]))
            if abs(widths[key] - f["w"]) > 0.45:
                continue
            new = max(round(widths[key] * scale, 2), base[key] * MIN_SCALE)
            if new < widths[key] - 0.05:
                print(f"    p{r['page']}: shrink {key} "
                      f"{widths[key]:.2f} → {new:.2f} cm")
                widths[key] = new
                changed = True
        if not changed:
            print("    nothing further to adjust")
            break
    json.dump(widths, open(wpath, "w"), indent=1)
    return widths


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "ch01")
