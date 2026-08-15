# -*- coding: utf-8 -*-
"""অধ্যায় ১১-এর ছবি প্রস্তুত করা।

উৎস ১ — John M. Sharp, *Practical Electric Wiring* (D. Appleton, 1916),
         Chapter II "Wire Joints and Splices"।  যুক্তরাষ্ট্রে ১৯৩১-এর আগে
         প্রকাশিত, কপিরাইট শেষ — পাবলিক ডোমেইন।
         archive.org/details/practicalelectr00shargoog
উৎস ২ — Wikimedia Commons-এর CC লাইসেন্সের আলোকচিত্র।
"""
import os, io, json, urllib.request
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "ch11")
PDF = os.path.join(HERE, ".sharp1916.pdf")     # ~7.6 MB, ডাউনলোড করে রাখা হয়
BOOK_URL = ("https://archive.org/download/practicalelectr00shargoog/"
            "practicalelectr00shargoog.pdf")
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "rapti-book/1.0 (textbook figure prep)"}

# name → (pdf page index, y0, y1, x0, x1) — সবই পাতার ভগ্নাংশে
CROPS = {
    "f01a_skin_ok":  (25, 0.428, 0.4905, 0.235, 0.520),
    "f01b_skin_bad": (25, 0.428, 0.4905, 0.525, 0.800),
    "f02_wu_steps":  (26, 0.220, 0.7345, 0.00, 1.00),
    "f03_wu_ties":   (27, 0.350, 0.512, 0.00, 1.00),
    "f04_tap":       (29, 0.020, 0.880, 0.00, 0.90),
    "f05_rattail":   (30, 0.225, 0.700, 0.00, 1.00),
    "f06_fixture":   (31, 0.265, 0.630, 0.00, 0.85),
    "f07_britannia": (32, 0.300, 0.600, 0.00, 1.00),
    "f08_married":   (34, 0.080, 0.880, 0.00, 1.00),
    "f09_tee_str":   (35, 0.190, 0.745, 0.00, 1.00),
    "f10_duplex":    (36, 0.190, 0.330, 0.00, 1.00),
}


def autocrop(im, thr=232, pad=26, need=4):
    """কালি-ঘন সারি/কলাম ধরে ছাঁটা।  `need`-এর কম পিক্সেলের বিচ্ছিন্ন
    স্ক্যান-দাগ উপেক্ষা করা হয়, নইলে সেগুলোই ছবির সীমা টেনে বড় করে।"""
    g = im.convert("L")
    px = g.load()
    w, h = g.size
    cols = [x for x in range(w)
            if sum(1 for y in range(0, h, 2) if px[x, y] < thr) >= need]
    rows = [y for y in range(h)
            if sum(1 for x in range(0, w, 2) if px[x, y] < thr) >= need]
    if not cols or not rows:
        return im
    box = (max(0, cols[0] - pad), max(0, rows[0] - pad),
           min(w, cols[-1] + pad), min(h, rows[-1] + pad))
    return im.crop(box)


def clean(im, black=118, white=196):
    """স্ক্যানের ধূসর কাগজ সাদা করা, কালি গাঢ় করা।"""
    g = im.convert("L")
    lut = [0 if i < black else (255 if i > white else
           int((i - black) * 255 / (white - black))) for i in range(256)]
    return g.point(lut).convert("RGB")


def fetch_book():
    """পাবলিক-ডোমেইন মূল বইটি না থাকলে archive.org থেকে নামিয়ে নেয়।"""
    if os.path.exists(PDF):
        return
    print("… downloading Sharp 1916 from archive.org")
    raw = urllib.request.urlopen(
        urllib.request.Request(BOOK_URL, headers=UA), timeout=300).read()
    open(PDF, "wb").write(raw)


def do_pdf():
    fetch_book()
    d = pymupdf.open(PDF)
    for name, (pg, y0, y1, x0, x1) in CROPS.items():
        page = d[pg]
        pix = page.get_pixmap(dpi=400)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        im = im.crop((int(im.width * x0), int(im.height * y0),
                      int(im.width * x1), int(im.height * y1)))
        im = clean(autocrop(im))
        im = autocrop(im, pad=30)
        bg = Image.new("RGB", (im.width + 60, im.height + 60), "white")
        bg.paste(im, (30, 30))
        bg.save(os.path.join(OUT, name + ".png"))
        print("✓", name, bg.size)
    do_splits()


# একটি প্লেটে একাধিক ধাপ থাকলে প্যানেলে বসানোর জন্য ভাগ করা হয়
SPLITS = {   # src → [(y0, y1, নাম), …]  মূল ছবির ভগ্নাংশে
    "f04_tap":     [(0.000, 0.385, "f04a_tee"), (0.415, 0.695, "f04c_cross1"),
                    (0.705, 1.000, "f04d_cross2")],
    "f05_rattail": [(0.000, 0.620, "f05a_rattail"), (0.640, 1.000, "f05b_rattail")],
    "f06_fixture": [(0.000, 0.505, "f06a_fixture"), (0.525, 1.000, "f06b_fixture")],
    "f07_britannia": [(0.000, 0.480, "f07a_britannia"),
                      (0.520, 1.000, "f07b_britannia")],
    "f08_married": [(0.000, 0.520, "f08a_married"), (0.545, 1.000, "f08b_married")],
    "f09_tee_str": [(0.000, 0.545, "f09a_tee_str"), (0.570, 1.000, "f09b_tee_str")],
}


def do_splits():
    for src, bands in SPLITS.items():
        p = os.path.join(OUT, src + ".png")
        im = Image.open(p)
        for y0, y1, n in bands:
            part = autocrop(im.crop((0, int(im.height * y0),
                                     im.width, int(im.height * y1))), pad=26)
            bg = Image.new("RGB", (part.width + 50, part.height + 50), "white")
            bg.paste(part, (25, 25))
            bg.save(os.path.join(OUT, n + ".png"))
            print("   ↳", n, bg.size)
        os.remove(p)


PHOTOS = {
    # name: (url, crop-box fraction or None, target width)
    "ph_solder_iron": (
        "https://upload.wikimedia.org/wikipedia/commons/7/7b/"
        "Solderin_Iron%2C_Tin-Solder_and_wires_%2814943579150%29.jpg",
        (0.11, 0.02, 0.90, 0.44), 1600),
    "ph_wire_nuts": (
        "https://upload.wikimedia.org/wikipedia/commons/6/69/"
        "Array_of_twist-on_wire_connectors_aka_wire_nuts_in_different_sizes.jpg",
        None, 1600),
    "ph_lever_conn": (
        "https://upload.wikimedia.org/wikipedia/commons/6/61/"
        "Wago_221-413_splicing_connector_with_stranded_wire.jpg",
        (0.10, 0.12, 0.92, 0.88), 1600),
}


def do_photos():
    for name, (url, box, wmax) in PHOTOS.items():
        raw = urllib.request.urlopen(
            urllib.request.Request(url, headers=UA), timeout=120).read()
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if box:
            w, h = im.size
            im = im.crop((int(w * box[0]), int(h * box[1]),
                          int(w * box[2]), int(h * box[3])))
        if im.width > wmax:
            im = im.resize((wmax, round(im.height * wmax / im.width)),
                           Image.LANCZOS)
        im.save(os.path.join(OUT, name + ".jpg"), quality=88)
        print("✓", name, im.size)


CREDITS = {
    "sharp1916": {
        "files": sorted(CROPS),
        "source": "John M. Sharp, Practical Electric Wiring, D. Appleton & Co., "
                  "New York, 1916, ch. II — archive.org/details/"
                  "practicalelectr00shargoog",
        "licence": "Public domain (US, published before 1931)",
    },
    "ph_solder_iron": {
        "source": "Wikimedia Commons — 'Solderin Iron, Tin-Solder and wires', "
                  "Flickr user Ruocaled",
        "licence": "CC BY 2.0",
    },
    "ph_wire_nuts": {
        "source": "Wikimedia Commons — 'Array of twist-on wire connectors aka "
                  "wire nuts in different sizes'",
        "licence": "CC0",
    },
    "ph_lever_conn": {
        "source": "Wikimedia Commons — 'Wago 221-413 splicing connector with "
                  "stranded wire'",
        "licence": "CC BY-SA 4.0",
    },
}

if __name__ == "__main__":
    do_pdf()
    do_photos()
    CREDITS["sharp1916"]["files"] = sorted(
        os.path.splitext(f)[0] for f in os.listdir(OUT) if f.startswith("f"))
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json written")
