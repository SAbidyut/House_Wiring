# -*- coding: utf-8 -*-
"""অধ্যায় ২০-এর ছবি প্রস্তুত করা।

দুই উৎস:

১।  **ইনস্টিটিউটের নিজের ডেক** — `HW Connection Diagram All.pptx`-এর
    ২৫–২৮ নং স্লাইড।  দুই ডেকের প্রতিটি স্লাইডের লেখা বের করে দেখা
    হয়েছে; ফ্লোট সুইচের স্লাইড কেবল ওই চারটিই, আর `Circuit
    Diagram.pptx`-এ একটিও নেই।

      ২৫  সিঙ্গেল কন্ডিশন — সার্কিট ডায়াগ্রাম (CB, ফ্লোট সুইচ, MC-র
          A1/A2 কয়েল টার্মিনাল)
      ২৬  সিঙ্গেল কন্ডিশন — কানেকশন ডায়াগ্রাম (com–NO ব্যবহার)
      ২৭  ডাবল কন্ডিশন — সার্কিট ডায়াগ্রাম (দুই ফ্লোট সিরিজে)
      ২৮  ডাবল কন্ডিশন — কানেকশন ডায়াগ্রাম (১ম com–NO, ২য় com–NC)

    ২৫ নং স্লাইডের ডান পাশে লেখা আছে "MC = Magnetic **Conductor**" —
    শব্দটা ভুল, ওটা Magnetic **Contactor**।  তাই ক্রপ-বক্সে ওই লেখাটুকু
    বাদ, আর সঠিক পরিভাষা বইয়ের লেখায় ও ছবির নোট-পটিতে।  স্লাইডের
    ইংরেজি শিরোনাম ও ক্যাপশনও বাদ — ছবির নিজের বাংলা প্যানেল-হেডার আছে।

২।  **উইকিমিডিয়া কমন্স** — ফ্লোট সুইচের কোনো আলোকচিত্র ইনস্টিটিউটের
    কোনো ফাইলে নেই (`Electrical House Wiring book.docx`-এ একটিও নয়)।

    এই অধ্যায়ের ভারটা যে দুটো ছবি টানে:

      ph_cut_off / ph_cut_on  একই কেবল-ফ্লোট সুইচ কেটে খোলা, দুই
          অবস্থায় — ইস্পাতের বল গড়িয়ে গিয়ে কালো লিভারকে ঠেলে
          মাইক্রোসুইচের লাল পিন চাপছে।  ভেতরে কী ঘটে, তার গোটা পাঠটা
          এই এক জোড়া ছবিতে।  (Martin Meise, CC BY 3.0)
      ph_panel  বাস্তবে বসানো একটি বোর্ড — তিনটে MCB আর পাশে
          "SEMI AUTO CONTROLLER", গায়ে AUTO/MANUAL বোতাম।  আমাদের
          বাজারে ফ্লোট সুইচ ঠিক এভাবেই বসে।  (ShriniwasGajare, CC BY-SA 4.0)

চালানোর নিয়ম:  python assets_ch20.py     (Book/build/ থেকে)
"""
import io
import json
import os
import subprocess
import time
import urllib.parse
import urllib.request

import pymupdf
from PIL import Image, ImageEnhance, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "assets", "ch20")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

UA = {"User-Agent": "rapti-book/1.0 (textbook figure prep)"}
API = "https://commons.wikimedia.org/w/api.php"

HW = "HW Connection Diagram All.pptx"

# নাম → (সোর্স ফাইল, PDF পৃষ্ঠা-সূচক, (x0, y0, x1, y1) ভগ্নাংশে)
SLIDES = {
    "h25_single_schem": (HW, 24, (0.190, 0.280, 0.775, 0.800)),
    "h26_single_conn":  (HW, 25, (0.080, 0.240, 0.870, 0.900)),
    "h27_double_schem": (HW, 26, (0.120, 0.280, 0.860, 0.790)),
    "h28_double_conn":  (HW, 27, (0.040, 0.190, 0.880, 0.905)),
}

# পৃষ্ঠার লেখায় এই শব্দগুলো থাকতেই হবে — এক স্লাইড এদিক-ওদিক হলে ধরা পড়বে
EXPECT = {
    "h25_single_schem": ["MC", "CB", "A1", "A2", "Single"],
    "h26_single_conn":  ["com", "NO", "NC", "Single", "Connection"],
    "h27_double_schem": ["MC", "CB", "A1", "A2", "Double"],
    "h28_double_conn":  ["Com", "NO", "NC", "Double", "Connection"],
}

# নাম → (কমন্সের ফাইলনাম, প্রত্যাশিত মাপ, ক্রপ-বক্স, সর্বোচ্চ চওড়া, কনট্রাস্ট)
# মাপটা পাহারাদার — কমন্সে ছবি বদলালে এখানেই ধরা পড়ে।
PHOTOS = {
    # ── কেটে খোলা সুইচ, দুই অবস্থায় ─────────────────────────────────
    "ph_cut_off":   ("Float switch off.jpg",
                     (4000, 3000), (0.055, 0.135, 0.985, 0.900), 1500, 1.12),
    "ph_cut_on":    ("Float switch on.jpg",
                     (4000, 3000), (0.055, 0.135, 0.985, 0.900), 1500, 1.12),

    # ── প্রকারভেদ ───────────────────────────────────────────────────
    # কেবল-ফ্লোট (নাশপাতি আকৃতি) — সঙ্গে কাউন্টার-ওয়েটের ওজনটি
    "ph_cable":     ("Float switch for open tanks.JPG",
                     (3155, 2003), (0.015, 0.030, 0.990, 0.980), 1500, 1.06),
    # কেবল-ফ্লোট, ঝুলন্ত অবস্থায় — কোণাকৃতির খোলস।  ক্রপটা টেনে ছোট
    # করা: চারটি ছবির সারিতে (চিত্র ২০.৬) সবচেয়ে লম্বা ছবিটাই সারির
    # উচ্চতা ঠিক করে, আর লম্বাটে ক্রপে ওই সারি আধ পাতা খেয়ে ফেলে।
    "ph_cone":      ("Floating level switch.JPG",
                     (2848, 4288), (0.150, 0.230, 0.800, 0.820), 1000, 1.05),
    # ভার্টিক্যাল রিড ফ্লোট — ছোট, দুই তারের
    "ph_vert":      ("Float switches.jpg",
                     (3072, 4080), (0.150, 0.250, 0.860, 0.860), 1000, 1.08),
    # আর্ম বা লিভার টাইপ — বয়লার ও বড় ট্যাংকে
    "ph_arm":       ("Magnetic level switch.JPG",
                     (2764, 1636), (0.010, 0.020, 0.995, 0.800), 1400, 1.05),
    # যান্ত্রিক বল-কক — বিদ্যুৎ নেই, তুলনার জন্য
    "ph_ballvalve": ("Mechanical float switch waterpool.jpg",
                     (5472, 3648), (0.020, 0.060, 0.950, 0.960), 1400, 1.04),
    # কাজের অবস্থায় — ড্রামের ভেতর ভাসছে
    "ph_barrel":    ("Schwimmerschalter fass.jpg",
                     (922, 691), (0.090, 0.100, 0.880, 0.780), 900, 1.10),

    # ── সঙ্গের যন্ত্র ───────────────────────────────────────────────
    # ম্যাগনেটিক কন্টাক্টর — A1/A2 কয়েল আর L1-L3 / T1-T3 পাওয়ার টার্মিনাল
    "ph_contactor": ("JLC1-D09-10.jpg",
                     (935, 979), (0.030, 0.030, 0.980, 0.985), 900, 1.02),
    # বাস্তবে বসানো বোর্ড — MCB-র পাশে AUTO/MANUAL কন্ট্রোলার
    "ph_panel":     ("An electrical setup featuring circuit breakers and a "
                     "water level controller.jpg",
                     (1600, 720), (0.020, 0.020, 0.995, 0.995), 1500, 1.10),
}


# ── স্লাইড ──────────────────────────────────────────────────────────────
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
        words = d[pg].get_text().split()
        missing = [k for k in EXPECT[name] if k not in words]
        if missing:
            raise SystemExit(f"✗ {name}: স্লাইড {pg + 1}-এ নেই {missing} "
                             f"— নম্বর মিলিয়ে দেখো")
        pix = d[pg].get_pixmap(dpi=300)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        w, h = im.size
        im = im.crop((int(w * box[0]), int(h * box[1]),
                      int(w * box[2]), int(h * box[3])))
        im = autocrop(im)
        bg = Image.new("RGB", (im.width + 48, im.height + 48), "white")
        bg.paste(im, (24, 24))
        bg.save(os.path.join(OUT, name + ".png"))
        print("✓", name, bg.size, f"({src} স্লাইড {pg + 1})")


# ── কমন্স ───────────────────────────────────────────────────────────────
def _get(url):
    for _ in range(6):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=300).read()
        except Exception as exc:                 # ৪২৯ এলে থেমে আবার চেষ্টা
            print("   … আবার চেষ্টা:", exc)
            time.sleep(15)
    raise SystemExit("✗ নামানো গেল না: " + url)


def commons_url(fname):
    """কমন্সের ফাইলনাম → আসল ছবির URL।  ফল ক্যাশে রাখা হয়।"""
    cache = os.path.join(CACHE, "ch20_urls.json")
    urls = json.load(open(cache)) if os.path.exists(cache) else {}
    if fname not in urls:
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "titles": "File:" + fname,
            "prop": "imageinfo", "iiprop": "url|extmetadata"})
        d = json.loads(_get(API + "?" + q))
        page = next(iter(d["query"]["pages"].values()))
        if "imageinfo" not in page:
            raise SystemExit(f"✗ কমন্সে পাওয়া গেল না: {fname}")
        urls[fname] = page["imageinfo"][0]["url"]
        json.dump(urls, open(cache, "w"), ensure_ascii=False, indent=1)
        time.sleep(2)
    return urls[fname]


def fetch(fname):
    """ডাউনলোড করে ক্যাশে রাখা — বারবার কমন্সে হিট করলে ৪২৯ আসে।"""
    fn = os.path.join(CACHE, "ch20_" + fname.replace(" ", "_"))
    if not os.path.exists(fn) or os.path.getsize(fn) < 4096:
        open(fn, "wb").write(_get(commons_url(fname)))
        time.sleep(3)
    return open(fn, "rb").read()


def do_photos():
    for name, (fname, size, box, wmax, contrast) in PHOTOS.items():
        # EXIF-এর ওরিয়েন্টেশন আগে মেলানো — কমন্সের সাইটে ছবিটি যেভাবে
        # দেখায়, ক্রপ-বক্সও সেই হিসাবেই লেখা
        im = ImageOps.exif_transpose(
            Image.open(io.BytesIO(fetch(fname)))).convert("RGB")
        if im.size != size:
            raise SystemExit(f"✗ {name}: {fname}-এর মাপ {im.size}, "
                             f"হওয়ার কথা {size} — কমন্সে ছবিটি বদলেছে, "
                             f"ক্রপ-বক্স আবার মিলিয়ে নিতে হবে")
        w, h = im.size
        im = im.crop((int(w * box[0]), int(h * box[1]),
                      int(w * box[2]), int(h * box[3])))
        if im.width > wmax:
            im = im.resize((wmax, round(im.height * wmax / im.width)),
                           Image.LANCZOS)
        if contrast != 1.0:
            im = ImageEnhance.Contrast(im).enhance(contrast)
        im.save(os.path.join(OUT, name + ".jpg"), quality=90)
        print("✓", name, im.size, f"({fname})")


# CC BY ও CC BY-SA — কৃতজ্ঞতা স্বীকার আইনি শর্ত, ইচ্ছাধীন নয়।
# `ch20.py` এই ফাইলটাই পড়ে অধ্যায়ের শেষের ❖ চিত্রসূত্র বাক্সটি বানায়,
# তাই কৃতজ্ঞতা আর ছবি কখনো আলাদা হয়ে যাবে না।
CREDITS = {
    "ph_cut": {
        "files": ["ph_cut_off", "ph_cut_on"],
        "title": "Float switch off / Float switch on",
        "author": "Martin Meise", "licence": "CC BY 3.0"},
    "ph_cable": {
        "files": ["ph_cable", "ph_cone", "ph_arm"],
        "title": "Float switch for open tanks · Floating level switch · "
                 "Magnetic level switch",
        "author": "S.J. de Waard", "licence": "CC BY 2.5"},
    "ph_vert": {
        "title": "Float switches",
        "author": "Honmingjun", "licence": "CC BY-SA 4.0"},
    "ph_ballvalve": {
        "title": "Mechanical float switch waterpool",
        "author": "Hp.Baumeler", "licence": "CC BY-SA 4.0"},
    "ph_barrel": {
        "title": "Schwimmerschalter fass",
        "author": "Stefan Riepl (Quark48)", "licence": "পাবলিক ডোমেইন"},
    "ph_contactor": {
        "title": "JLC1-D09-10 (ম্যাগনেটিক কন্টাক্টর)",
        "author": "Редактор1511", "licence": "CC BY-SA 4.0"},
    "ph_panel": {
        "title": "An electrical setup featuring circuit breakers and a "
                 "water level controller",
        "author": "ShriniwasGajare", "licence": "CC BY-SA 4.0"},
    "rapti_slides": {
        "files": sorted(SLIDES),
        "source": "RAPTI — HW Connection Diagram All.pptx (slides 25–28)",
        "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
}

if __name__ == "__main__":
    do_slides()
    do_photos()
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json লেখা হলো")
