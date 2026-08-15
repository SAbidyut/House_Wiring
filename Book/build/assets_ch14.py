# -*- coding: utf-8 -*-
"""অধ্যায় ১৪-এর ছবি প্রস্তুত করা।

উৎস ১ — ইনস্টিটিউটের নিজস্ব `HW Connection Diagram All.pptx`
         (স্লাইড ৩০, ৩৪, ৩৫, ৩৬)।  soffice দিয়ে PDF বানিয়ে ৩০০ dpi-তে ক্রপ।
উৎস ২ — ইনস্টিটিউটের নিজস্ব `Electrical House Wiring book.docx`-এর
         `word/media/` থেকে ওয়্যারিং পদ্ধতির আলোকচিত্র (image121–132)।

চালানোর নিয়ম:  python assets_ch14.py     (Book/build/ থেকে)
"""
import os, json, shutil, subprocess, zipfile
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))     # প্রজেক্টের রুট
OUT = os.path.join(HERE, "assets", "ch14")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

# নাম → (সোর্স ফাইল, PDF পৃষ্ঠা-সূচক, (x0, y0, x1, y1) ভগ্নাংশে বা None)
SLIDES = {
    "h30_service_to_sdb": ("HW Connection Diagram All.pptx", 29, None),
    "h34_house_conduit":  ("HW Connection Diagram All.pptx", 33, None),
    "h35_house_casing":   ("HW Connection Diagram All.pptx", 34, None),
    "h36_house_both":     ("HW Connection Diagram All.pptx", 35, None),
}

# নাম → (docx-এর media ফাইল, সর্বোচ্চ চওড়া px)
DOC_IMAGES = {
    "p_internal":     ("image121.png", 1200),
    "p_overhead":     ("image122.png", 1100),
    "p_underground":  ("image123.png", 1100),
    "p_cable_in_pipe": ("image124.png", 1200),
    "p_casing_goods": ("image125.jpg", 1200),
    "p_batten":       ("image126.png", 1000),
    "p_cleat":        ("image127.png", 1100),
    "p_trunking":     ("image128.png", 1300),
    "p_conceal_slab": ("image129.png", 1300),
    "p_conceal_wall": ("image130.png", 1300),
    "p_surface_pipe": ("image131.png", 1300),
    "p_surface_ceil": ("image132.png", 1300),
}
DOCX = "Electrical House Wiring book.docx"


def slide_pdf(name):
    """PPTX → PDF (একবারই), তারপর ক্যাশ থেকে।"""
    pdf = os.path.join(CACHE, os.path.splitext(name)[0] + ".pdf")
    if not os.path.exists(pdf):
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                        "--outdir", CACHE, os.path.join(ROOT, name)],
                       check=True, capture_output=True)
    return pdf


def autocrop(im, thr=244, pad=24, need=4):
    """সাদা মার্জিন ছাঁটা; বিচ্ছিন্ন দাগ উপেক্ষা করা হয় (need ≥ ৪ পিক্সেল)।"""
    g = im.convert("L")
    px = g.load()
    w, h = g.size
    cols = [x for x in range(w)
            if sum(1 for y in range(0, h, 2) if px[x, y] < thr) >= need]
    rows = [y for y in range(h)
            if sum(1 for x in range(0, w, 2) if px[x, y] < thr) >= need]
    if not cols or not rows:
        return im
    return im.crop((max(0, cols[0] - pad), max(0, rows[0] - pad),
                    min(w, cols[-1] + pad), min(h, rows[-1] + pad)))


def do_slides():
    for name, (src, pg, box) in SLIDES.items():
        d = pymupdf.open(slide_pdf(src))
        pix = d[pg].get_pixmap(dpi=300)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if box:
            w, h = im.size
            im = im.crop((int(w * box[0]), int(h * box[1]),
                          int(w * box[2]), int(h * box[3])))
        im = autocrop(im)
        bg = Image.new("RGB", (im.width + 48, im.height + 48), "white")
        bg.paste(im, (24, 24))
        bg.save(os.path.join(OUT, name + ".png"))
        print("✓", name, bg.size, f"({src} স্লাইড {pg + 1})")


def do_doc_images():
    """docx-এর ভেতরের ছবিগুলো বের করা — RGBA হলে সাদা পটে বসানো হয়,
    নইলে কালো পটভূমিতে ছাপা হয়।"""
    zf = zipfile.ZipFile(os.path.join(ROOT, DOCX))
    for name, (member, wmax) in DOC_IMAGES.items():
        with zf.open("word/media/" + member) as fh:
            im = Image.open(fh)
            im.load()
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, "white")
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        im = autocrop(im, thr=248, pad=6, need=6)
        if im.width > wmax:
            im = im.resize((wmax, round(im.height * wmax / im.width)),
                           Image.LANCZOS)
        im.save(os.path.join(OUT, name + ".jpg"), quality=90)
        print("✓", name, im.size, f"({member})")


CREDITS = {
    "rapti_slides": {
        "files": sorted(SLIDES),
        "source": "RAPTI — HW Connection Diagram All.pptx (slides 30, 34, 35, 36)",
        "licence": "Institute's own material",
    },
    "rapti_photos": {
        "files": sorted(DOC_IMAGES),
        "source": "RAPTI — Electrical House Wiring book.docx (word/media)",
        "licence": "Institute's own material",
    },
}

if __name__ == "__main__":
    do_slides()
    do_doc_images()
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json written")
