#!/usr/bin/env python3
"""sheets.py PDF OUTPREFIX [dpi] — contact sheets (3x3) of a PDF's pages for visual QA."""
import sys, os, glob, subprocess, tempfile
from PIL import Image
pdf, pre = sys.argv[1], sys.argv[2]
dpi = sys.argv[3] if len(sys.argv) > 3 else "55"
tmp = tempfile.mkdtemp()
os.makedirs(os.path.dirname(os.path.abspath(pre)), exist_ok=True)
subprocess.run(["pdftoppm", "-jpeg", "-r", dpi, pdf, os.path.join(tmp, "s")], check=True)
fs = sorted(glob.glob(os.path.join(tmp, "s-*.jpg")))
ims = [Image.open(f) for f in fs]
w, h = ims[0].size
cols = 3
for f in glob.glob(pre + "*.jpg"):
    os.remove(f)
for k in range(0, len(ims), 9):
    grp = ims[k:k + 9]
    rows = (len(grp) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + (cols + 1) * 8, rows * h + (rows + 1) * 8), "#888")
    for i, im in enumerate(grp):
        sheet.paste(im, (8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 8)))
    sheet.save(f"{pre}{k // 9}.jpg", quality=85)
    print(f"{pre}{k // 9}.jpg  (slides {k + 1}–{k + len(grp)})")
