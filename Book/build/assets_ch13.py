# -*- coding: utf-8 -*-
"""অধ্যায় ১৩-এর ছবি প্রস্তুত করা।

উৎস ১ — ইনস্টিটিউটের নিজস্ব `Circuit Diagram.pptx` (স্লাইড ১৭, ১৮) ও
         `HW Connection Diagram All.pptx` (স্লাইড ১৭, ১৮)।  soffice দিয়ে PDF
         বানিয়ে ৩০০ dpi-তে ক্রপ করা হয়।
উৎস ২ — উইকিমিডিয়া কমন্সের CC/CC0 লাইসেন্সের আলোকচিত্র।

চালানোর নিয়ম:  python assets_ch13.py     (Book/build/ থেকে)
"""
import os, io, json, subprocess, urllib.request
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))     # প্রজেক্টের রুট
OUT = os.path.join(HERE, "assets", "ch13")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)
UA = {"User-Agent": "rapti-book/1.0 (textbook figure prep)"}

# নাম → (সোর্স ফাইল, PDF পৃষ্ঠা-সূচক, (x0, y0, x1, y1) ভগ্নাংশে বা None)
SLIDES = {
    "c17_2way_schem":  ("Circuit Diagram.pptx", 16, None),
    "c18_tunnel_schem": ("Circuit Diagram.pptx", 17, None),
    "h17_2way_conn":   ("HW Connection Diagram All.pptx", 16, None),
    "h18_tunnel_conn": ("HW Connection Diagram All.pptx", 17, None),
}


def slide_pdf(name):
    """PPTX → PDF (একবারই), তারপর ক্যাশ থেকে।"""
    pdf = os.path.join(CACHE, os.path.splitext(name)[0] + ".pdf")
    if not os.path.exists(pdf):
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                        "--outdir", CACHE, os.path.join(ROOT, name)],
                       check=True, capture_output=True)
    return pdf


def autocrop(im, thr=244, pad=24, need=3):
    """সাদা মার্জিন ছাঁটা; বিচ্ছিন্ন দাগ উপেক্ষা করা হয়।"""
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


# নাম → (URL, ক্রপ-বক্স ভগ্নাংশে বা None, সর্বোচ্চ চওড়া)
PHOTOS = {
    "ph_2way_back": ("https://upload.wikimedia.org/wikipedia/commons/8/8f/"
                     "Two_way_switch.jpg", None, 1500),
    "ph_staircase": ("https://upload.wikimedia.org/wikipedia/commons/1/13/"
                     "Staircase_lighting.jpg", None, 1400),
}


def fetch(url):
    """ডাউনলোড করে ক্যাশে রাখা — বারবার কমন্সে হিট করলে ৪২৯ আসে।"""
    fn = os.path.join(CACHE, os.path.basename(url))
    if not os.path.exists(fn):
        raw = urllib.request.urlopen(
            urllib.request.Request(url, headers=UA), timeout=180).read()
        open(fn, "wb").write(raw)
    return open(fn, "rb").read()


def do_photos():
    for name, (url, box, wmax) in PHOTOS.items():
        im = Image.open(io.BytesIO(fetch(url))).convert("RGB")
        if box:
            w, h = im.size
            im = im.crop((int(w * box[0]), int(h * box[1]),
                          int(w * box[2]), int(h * box[3])))
        if im.width > wmax:
            im = im.resize((wmax, round(im.height * wmax / im.width)),
                           Image.LANCZOS)
        im.save(os.path.join(OUT, f"{name}.jpg"), quality=88)
        print("✓", name, im.size)


CREDITS = {
    "rapti_slides": {
        "files": sorted(SLIDES),
        "source": "RAPTI — Circuit Diagram.pptx (slides 17, 18) and "
                  "HW Connection Diagram All.pptx (slides 17, 18)",
        "licence": "Institute's own material",
    },
}

if __name__ == "__main__":
    do_slides()
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json written")
