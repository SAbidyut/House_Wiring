# -*- coding: utf-8 -*-
"""অধ্যায় ১২-এর ছবি প্রস্তুত করা।

উৎস ১ — ইনস্টিটিউটের নিজস্ব `Circuit Diagram.pptx` (স্লাইড ২১, ২২) ও
         `HW Connection Diagram All.pptx` (স্লাইড ২১)।  soffice দিয়ে PDF
         বানিয়ে ৩০০ dpi-তে ক্রপ করা হয়।
উৎস ২ — উইকিমিডিয়া কমন্সের CC/CC0 লাইসেন্সের আলোকচিত্র।

চালানোর নিয়ম:  python assets_ch12.py     (Book/build/ থেকে)
"""
import os, io, json, subprocess, urllib.request
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))     # প্রজেক্টের রুট
OUT = os.path.join(HERE, "assets", "ch12")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)
UA = {"User-Agent": "rapti-book/1.0 (textbook figure prep)"}

# নাম → (সোর্স ফাইল, PDF পৃষ্ঠা-সূচক, (x0, y0, x1, y1) ভগ্নাংশে বা None)
SLIDES = {
    "c21_reg_schem":   ("Circuit Diagram.pptx", 20, None),
    "c22_board_schem": ("Circuit Diagram.pptx", 21, None),
    "h21_reg_conn":    ("HW Connection Diagram All.pptx", 20, None),
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
    # সিলিং ফ্যানের পরিচিতি-ছবি — পরিষ্কার, তিন ব্লেডের দেশীয় ফ্যান
    "ph_fan": ("https://upload.wikimedia.org/wikipedia/commons/"
               "c/c4/Fan_2024.jpg", (0.185, 0.12, 0.955, 0.95), 1800),
    "ph_cap_run": ("https://upload.wikimedia.org/wikipedia/commons/c/ca/"
                   "Ceiling_fan_capacitor.png", (0.00, 0.00, 0.50, 1.00), 1500),
    "ph_cap_run2": ("https://upload.wikimedia.org/wikipedia/commons/c/ca/"
                    "Ceiling_fan_capacitor.png", (0.50, 0.00, 1.00, 1.00), 1500),
    "ph_cap_start": ("https://upload.wikimedia.org/wikipedia/commons/2/28/"
                     "Motor-Start-Capacitor.jpg", None, 1500),
    "ph_reg_elec": ("https://upload.wikimedia.org/wikipedia/commons/9/98/"
                    "Fan_electronic_regulator.jpg", (0.04, 0.17, 0.96, 1.00),
                    1400),
    "ph_board_reg": ("https://upload.wikimedia.org/wikipedia/commons/7/77/"
                     "Switch_box_with_fan_regulator.jpg",
                     (0.10, 0.14, 0.92, 0.86), 1600),
    # ক্যাপাসিটরের শ্রেণিবিভাগের জন্য
    "ph_cap_polar": ("https://upload.wikimedia.org/wikipedia/commons/8/87/"
                     "Polarity-wet-Al-Elcaps.jpg", (0.02, 0.17, 0.98, 0.97),
                     1500),
    "ph_cap_ceramic": ("https://upload.wikimedia.org/wikipedia/commons/5/50/"
                       "Soviet_ceramic_disc_capacitors_01.jpg",
                       (0.06, 0.10, 0.94, 0.90), 1500),
    "ph_cap_var": ("https://upload.wikimedia.org/wikipedia/commons/c/cb/"
                   "Air_variable_capacitor.jpg", (0.04, 0.04, 0.96, 0.96),
                   1200),
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
        ext = "png" if name.startswith("ph_cap_run") else "jpg"
        im.save(os.path.join(OUT, f"{name}.{ext}"), quality=88)
        print("✓", name, im.size)


# ── উৎস ৩ — প্রস্তুতকারক/বিক্রেতার পণ্য-আলোকচিত্র ────────────────────
# কমন্সে ফ্যানের ২-তারের রান ক্যাপাসিটরের কোনো ছবি নেই (সব ক-টি
# ক্যাটাগরি ও অনুসন্ধান দেখা হয়েছে), অথচ অধ্যায়ের মূল কাজই গায়ের
# লেখা পড়া।  তাই এই তিনটি ছবি প্রস্তুতকারকের পণ্য-আলোকচিত্র থেকে
# নেওয়া — ব্যবহারকারীর নির্দেশে (২০২৬-০৮-২৮)।
WEB = {
    # ফ্যানের আসল রান ক্যাপাসিটর — CBB61, দুই তার, 4 µF 450 V.AC
    "ph_cap_fan": ("https://image.made-in-china.com/2f0j00eZwqzyfgMDcn/"
                   "Cbb61-3-5UF-4UF-450VAC-Electrolyte-Capacitor-Fan-"
                   "Capacitors.jpg", (0.10, 0.02, 0.93, 0.95), 1500),
    # একই ছবির গায়ের-লেখা অংশ — কাছ থেকে, ছাপা পড়ার জন্য
    "ph_cap_fan_face": ("https://image.made-in-china.com/2f0j00eZwqzyfgMDcn/"
                        "Cbb61-3-5UF-4UF-450VAC-Electrolyte-Capacitor-Fan-"
                        "Capacitors.jpg", (0.165, 0.27, 0.905, 0.84), 1800),
    # ফ্যানের আসল রান ক্যাপাসিটর — গোল ধূসর কৌটা, দুই স্পেড টার্মিনাল
    # (বাংলাদেশের সিলিং ফ্যানে এটিই সবচেয়ে বেশি বসে)
    "ph_cap_can": ("https://image.made-in-china.com/2f0j00JOKidIBjKVpn/"
                   "Made-in-Thailand-RoHS-Sh-Generator-Sk-Capacitor-3-5UF.jpg",
                   (0.06, 0.02, 0.95, 0.97), 1500),
    # একই ছবির সামনের কৌটাটি — টার্মিনাল ও গায়ের লেখাসহ
    "ph_cap_can_face": ("https://image.made-in-china.com/2f0j00JOKidIBjKVpn/"
                        "Made-in-Thailand-RoHS-Sh-Generator-Sk-Capacitor-"
                        "3-5UF.jpg", (0.43, 0.03, 0.90, 0.60), 1500),
    # পোলারাইজড — অ্যালুমিনিয়াম ইলেক্ট্রোলাইটিক 1000 µF 25 V.
    # ক্রপটা দুই পায়ের ডগা পর্যন্ত নেওয়া — লম্বা পা আর খাটো পা-র
    # পার্থক্যটাই এখানে দেখানোর জিনিস।
    "ph_cap_elko": ("https://www.embeddinator.com/public/upload/pros/"
                    "1000uf_11.png", (0.05, 0.33, 0.985, 0.685), 2000),
}


def do_web():
    for name, (url, box, wmax) in WEB.items():
        im = Image.open(io.BytesIO(fetch(url))).convert("RGB")
        if box:
            w, h = im.size
            im = im.crop((int(w * box[0]), int(h * box[1]),
                          int(w * box[2]), int(h * box[3])))
        if im.width > wmax:
            im = im.resize((wmax, round(im.height * wmax / im.width)),
                           Image.LANCZOS)
        im.save(os.path.join(OUT, f"{name}.jpg"), quality=92)
        print("✓", name, im.size)


CREDITS = {
    "rapti_slides": {
        "files": sorted(SLIDES),
        "source": "RAPTI — Circuit Diagram.pptx (slides 21, 22) and "
                  "HW Connection Diagram All.pptx (slide 21)",
        "licence": "Institute's own material",
    },
    "ph_fan": {
        "source": "Wikimedia Commons — 'An Old model three blade ceiling fan'",
        "licence": "CC BY-SA 3.0",
    },
    "ph_cap_run / ph_cap_run2": {
        "source": "Wikimedia Commons — 'Ceiling fan capacitor'",
        "licence": "CC BY-SA 4.0",
    },
    "ph_cap_start": {
        "source": "Wikimedia Commons — 'Motor-Start-Capacitor'",
        "licence": "CC0",
    },
    "ph_reg_elec": {
        "source": "Wikimedia Commons — 'Fan electronic regulator'",
        "licence": "CC BY-SA 4.0",
    },
    "ph_board_reg": {
        "source": "Wikimedia Commons — 'Switch box with fan regulator'",
        "licence": "CC0",
    },
    "ph_cap_polar": {
        "source": "Wikimedia Commons — 'Polarity-wet-Al-Elcaps'",
        "licence": "CC0",
    },
    "ph_cap_fan / ph_cap_fan_face": {
        "source": "made-in-china.com — CBB61 fan capacitor product photo",
        "licence": "Manufacturer's product photograph",
    },
    "ph_cap_elko": {
        "source": "embeddinator.com — 1000 uF 25 V electrolytic capacitor",
        "licence": "Manufacturer's product photograph",
    },
    "ph_cap_can / ph_cap_can_face": {
        "source": "made-in-china.com — SH 350 V.AC fan capacitor photo",
        "licence": "Manufacturer's product photograph",
    },
    "ph_cap_ceramic": {
        "source": "Wikimedia Commons — 'Soviet ceramic disc capacitors 01'",
        "licence": "CC0",
    },
    "ph_cap_var": {
        "source": "Wikimedia Commons — 'Air variable capacitor'",
        "licence": "CC BY-SA 3.0",
    },
}

if __name__ == "__main__":
    do_slides()
    do_photos()
    do_web()
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json written")
