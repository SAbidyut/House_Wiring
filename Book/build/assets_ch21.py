# -*- coding: utf-8 -*-
"""অধ্যায় ২১-এর ছবি প্রস্তুত করা।

তিন উৎস:

১।  **ইনস্টিটিউটের নিজের বাসবার ডেক** — `Busbar All.pptx`।  সাত স্লাইড,
    তার ভেতরে বসানো চারটি ছবি সরাসরি তুলে নেওয়া হয় (PPTX-এর ভেতরের
    আসল ফাইলটাই, স্লাইড রেন্ডার করে নয় — তাতে রেজলিউশন পুরোটা থাকে)।

      s1  তামার তিনটি বার আর অ্যালুমিনিয়ামের তিনটি বার — উপাদান তুলনা
      s2  বাঁয়ে মোচড়ানো তারের জোড়া, ডাইনে প্যানেলে বসানো বাসবার
          থেকে সারি সারি ট্যাপ — "কেন বাসবার" গোটাটাই এই জোড়ায়

    **স্লাইড ৭-এর সূত্র দুটি ভুল, তাই ওই স্লাইড বসানো হয়নি** — ওতে লেখা
    `KVA = 1000*V*I` আর `KW = 1000*V*I*Cosθ`।  হাজার দিয়ে ভাগ হওয়ার কথা,
    গুণ নয়।  সঠিক রূপ §২১.৭.২-এ, আর d05-এর নিজের ফ্লো-চার্টে।
    স্লাইড ৬-এর মাপের তালিকাটি ছবি নয় — সারণি ২১.৪ হয়ে গেছে (বইয়ের
    নিয়ম: সব ডেটা-টেবিল আসল ওয়ার্ড টেবিল)।

২।  **ইনস্টিটিউটের কানেকশন ডেক** — `HW Connection Diagram All.pptx`-এর
    ২৯, ৩১, ৩২, ৩৩ নং স্লাইড।  দুই ডেকের প্রতিটি স্লাইডের লেখা বের করে
    দেখা হয়েছে; বাসবার-লেবেলওয়ালা স্লাইড ঠিক ওই চারটিই।

      ২৯  ৩-ফেজ মিটার → MCCB → Line 1/2/3 + Neutral + Earthing বাসবার
      ৩১  মেইন মিটার → বাসবার → তিনটি সাব-মিটার (ভাড়াটে বাড়ির ছক)
      ৩২  এক বাসবার-সেট থেকে ৩Φ আর ১Φ দুই রকম আউটপুট
      ৩৩  ফ্ল্যাটের পূর্ণ SDB — RCCB, SPD, আলাদা নিউট্রাল ও আর্থিং বার

৩।  **উইকিমিডিয়া কমন্স** — বাস্তব বাসবারের আলোকচিত্র ইনস্টিটিউটের
    কোনো ফাইলে নেই (ডেকের ছবিগুলো স্টক রেন্ডার)।

      ph_panel  এলটি প্যানেলে লাল-হলুদ-নীল রং করা তিনটি ফ্ল্যাট বার,
          স্ট্যান্ড-অফ ইনসুলেটরে বসানো, জোড়ায় বোল্ট।  বিএনবিসি
          ১.৩.৯.৩.১৫-এর রঙের কোডটা বাস্তবে ঠিক এইরকম দেখায়।
      ph_earth  আর্থিং ও নিউট্রাল বার — খোলা তামার পাত, গায়ে সারি সারি
          স্ক্রু টার্মিনাল, সবুজ-হলুদ ও নীল তার নামছে।  বিএনবিসি
          ১.৩.৩৭.৩.৫ যে জিনিসটা বাধ্যতামূলক করেছে, সেটিই।  d08-এর
          কল-আউট এই ছবির উপরে।
      ph_trunk  ছাদ থেকে ঝোলানো বাসবার ট্রাংকিং, গায়ে ট্যাপ-অফ বাক্স —
          বিএনবিসি ১.৩.১৮.৩ ও ১.৩.১৮.৪।
      ph_raw    কারখানায় থাক দেওয়া কাঁচা তামার বার, ফুটো করা —
          বাজারে জিনিসটা যেভাবে আসে।

চালানোর নিয়ম:  python assets_ch21.py     (Book/build/ থেকে)
"""
import hashlib
import io
import json
import os
import subprocess
import time
import urllib.parse
import urllib.request

import pymupdf
from PIL import Image, ImageEnhance, ImageOps
from pptx import Presentation

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "assets", "ch21")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

UA = {"User-Agent": "rapti-book/1.0 (textbook figure prep)"}
API = "https://commons.wikimedia.org/w/api.php"

HW = "HW Connection Diagram All.pptx"
BB = "Busbar All.pptx"

# ── ১।  বাসবার ডেকের ভেতরের ছবি ────────────────────────────────────────
# নাম → (স্লাইড নম্বর, শেপের নাম, sha1-এর প্রথম ১০ অক্ষর, প্রত্যাশিত মাপ,
#         ক্রপ-বক্স ভগ্নাংশে)
# sha1 আর মাপ — দুটোই পাহারাদার।  ডেক বদলালে এখানেই ধরা পড়বে।
PPTX_PICS = {
    "b_cu":    (1, "Picture 4", "5355c6364e", (1074, 550),
                (0.02, 0.05, 0.99, 0.96)),
    "b_al":    (1, "Picture 6", "74821cc7b5", (500, 500),
                (0.02, 0.20, 0.99, 0.82)),
    # সাবধান — ডেকে শেপের নাম আর ছবির বিষয় উল্টো:  "Picture 6"-ই
    # প্যানেলের আলোকচিত্র, আর "Picture 8" মোচড়ানো তারের ছবি।
    "b_taps":  (2, "Picture 6", "6b59cf019c", (920, 610),
                (0.02, 0.02, 0.99, 0.99)),
    "b_wires": (2, "Picture 8", "02dc1a094e", (1000, 671),
                (0.01, 0.01, 0.99, 0.99)),
}

# ── ২।  কানেকশন ডেকের স্লাইড ───────────────────────────────────────────
# নাম → (সোর্স ফাইল, PDF পৃষ্ঠা-সূচক, (x0, y0, x1, y1) ভগ্নাংশে)
# চারটিরই গোটা স্লাইডটাই ছবি — কাটার মতো ইংরেজি শিরোনাম বা ক্যাপশন
# নেই, লেখা যা আছে সবই ডায়াগ্রামের নিজের লেবেল।  সাদা মার্জিন
# autocrop ছেঁটে দেয়।
SLIDES = {
    "h29_main":     (HW, 28, (0.00, 0.00, 1.00, 1.00)),
    "h31_submeter": (HW, 30, (0.00, 0.00, 1.00, 1.00)),
    "h32_3p1p":     (HW, 31, (0.00, 0.00, 1.00, 1.00)),
    "h33_sdb":      (HW, 32, (0.00, 0.00, 1.00, 1.00)),
}

# পৃষ্ঠার লেখায় এই শব্দগুলো থাকতেই হবে — এক স্লাইড এদিক-ওদিক হলে ধরা পড়বে
EXPECT = {
    "h29_main":     ["MCCB", "Busbar", "Neutral", "Earthing", "phase"],
    "h31_submeter": ["Main", "Meter", "Sub", "Busbar", "Earthing", "MCB"],
    "h32_3p1p":     ["MCCB", "Busbar", "Earthing", "Output", "Meter"],
    "h33_sdb":      ["RCCB", "SPD", "Neutral", "Busbar", "Earthing", "SDB"],
}

# ── ৩।  কমন্স ──────────────────────────────────────────────────────────
# নাম → (কমন্সের ফাইলনাম, প্রত্যাশিত মাপ, ক্রপ-বক্স, সর্বোচ্চ চওড়া, কনট্রাস্ট)
PHOTOS = {
    # রং করা তিন ফেজের বার — বাঁয়ের ক্যাবিনেট-জঞ্জাল সামান্য ছাঁটা।
    # আসল ছবিটাই ৭৯৫ পিক্সেল চওড়া, তাই ক্রপে কৃপণ হতে হয়েছে।
    "ph_panel": ("Busbar in an LT panel.png",
                 (795, 521), (0.12, 0.10, 1.00, 1.00), 795, 1.06),
    # আর্থিং ও নিউট্রাল বার — নিচের অর্ধেকে কেবল ছাড়া কিছু নেই
    "ph_earth": ("Dornbirn-modern main earthing busbar (copper)-01ASD - "
                 "Kopie.jpg",
                 (4624, 3468), (0.015, 0.010, 0.990, 0.600), 1600, 1.06),
    # ছাদ থেকে ঝোলানো ট্রাংকিং — ট্যাপ-অফ বাক্সগুলো যেন বোঝা যায়
    "ph_trunk": ("Sample busbar trunking system.jpg",
                 (4032, 3024), (0.060, 0.020, 0.960, 0.940), 1400, 1.06),
    # কাঁচা তামার বার, ফুটো করা, কারখানায় থাক দেওয়া
    "ph_raw":   ("Picture of busbar2010126a (1).jpg",
                 (718, 884), (0.02, 0.02, 0.99, 0.92), 718, 1.05),
}


# ── সাধারণ কাজ ─────────────────────────────────────────────────────────
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


def flatten(im):
    """RGBA → সাদার উপরে বসানো RGB।  না করলে ছাপায় কালো আসে (ch18)।"""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        return Image.alpha_composite(bg, im).convert("RGB")
    return im.convert("RGB")


def frac_crop(im, box):
    w, h = im.size
    return im.crop((int(w * box[0]), int(h * box[1]),
                    int(w * box[2]), int(h * box[3])))


# ── ১।  PPTX-এর ভেতরের ছবি ─────────────────────────────────────────────
def do_pptx_pics():
    prs = Presentation(os.path.join(ROOT, BB))
    slides = list(prs.slides)
    for name, (sn, shname, sha, size, box) in PPTX_PICS.items():
        shapes = [s for s in slides[sn - 1].shapes if s.name == shname]
        if not shapes:
            raise SystemExit(f"✗ {name}: {BB} স্লাইড {sn}-এ '{shname}' নেই")
        blob = shapes[0].image.blob
        got = hashlib.sha1(blob).hexdigest()[:10]
        if got != sha:
            raise SystemExit(f"✗ {name}: ছবির sha1 {got}, হওয়ার কথা {sha} "
                             f"— ডেকের ছবি বদলেছে, ক্রপ-বক্স মিলিয়ে নাও")
        im = flatten(Image.open(io.BytesIO(blob)))
        if im.size != size:
            raise SystemExit(f"✗ {name}: মাপ {im.size}, হওয়ার কথা {size}")
        im = autocrop(frac_crop(im, box), thr=248, pad=18)
        im.save(os.path.join(OUT, name + ".png"))
        print("✓", name, im.size, f"({BB} স্লাইড {sn})")


# ── ২।  স্লাইড ─────────────────────────────────────────────────────────
def slide_pdf(name):
    """PPTX → PDF (একবারই), তারপর ক্যাশ থেকে।"""
    pdf = os.path.join(CACHE, os.path.splitext(name)[0] + ".pdf")
    if not os.path.exists(pdf):
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                        "--outdir", CACHE, os.path.join(ROOT, name)],
                       check=True, capture_output=True)
    return pdf


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
        im = autocrop(frac_crop(im, box))
        bg = Image.new("RGB", (im.width + 48, im.height + 48), "white")
        bg.paste(im, (24, 24))
        bg.save(os.path.join(OUT, name + ".png"))
        print("✓", name, bg.size, f"({src} স্লাইড {pg + 1})")


# ── ৩।  কমন্স ──────────────────────────────────────────────────────────
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
    cache = os.path.join(CACHE, "ch21_urls.json")
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
    fn = os.path.join(CACHE, "ch21_" + fname.replace(" ", "_"))
    if not os.path.exists(fn) or os.path.getsize(fn) < 4096:
        open(fn, "wb").write(_get(commons_url(fname)))
        time.sleep(3)
    return open(fn, "rb").read()


def do_photos():
    for name, (fname, size, box, wmax, contrast) in PHOTOS.items():
        # EXIF-এর ওরিয়েন্টেশন আগে মেলানো — কমন্সের সাইটে ছবিটি যেভাবে
        # দেখায়, ক্রপ-বক্সও সেই হিসাবেই লেখা
        im = flatten(ImageOps.exif_transpose(Image.open(io.BytesIO(
            fetch(fname)))))
        if im.size != size:
            raise SystemExit(f"✗ {name}: {fname}-এর মাপ {im.size}, "
                             f"হওয়ার কথা {size} — কমন্সে ছবিটি বদলেছে, "
                             f"ক্রপ-বক্স আবার মিলিয়ে নিতে হবে")
        im = frac_crop(im, box)
        if im.width > wmax:
            im = im.resize((wmax, round(im.height * wmax / im.width)),
                           Image.LANCZOS)
        if contrast != 1.0:
            im = ImageEnhance.Contrast(im).enhance(contrast)
        im.save(os.path.join(OUT, name + ".jpg"), quality=92)
        print("✓", name, im.size, f"({fname})")


# CC BY ও CC BY-SA — কৃতজ্ঞতা স্বীকার আইনি শর্ত, ইচ্ছাধীন নয়।
# `ch21.py` এই ফাইলটাই পড়ে অধ্যায়ের শেষের ❖ চিত্রসূত্র বাক্সটি বানায়,
# তাই কৃতজ্ঞতা আর ছবি কখনো আলাদা হয়ে যাবে না।
CREDITS = {
    "ph_panel": {
        "title": "Busbar in an LT panel",
        "author": "Goldflakes", "licence": "CC BY-SA 4.0"},
    "ph_earth": {
        "title": "Dornbirn — modern main earthing busbar (copper)",
        "author": "Asurnipal", "licence": "CC BY-SA 4.0"},
    "ph_trunk": {
        "title": "Sample busbar trunking system",
        "author": "Blacky-CS", "licence": "CC BY-SA 4.0"},
    "ph_raw": {
        "title": "Picture of busbar2010126a",
        "author": "Motimachine", "licence": "CC BY-SA 4.0"},
    "rapti_bb": {
        "files": sorted(PPTX_PICS),
        "source": "RAPTI — Busbar All.pptx (slides 1–2)",
        "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "rapti_slides": {
        "files": sorted(SLIDES),
        "source": "RAPTI — HW Connection Diagram All.pptx "
                  "(slides 29, 31, 32, 33)",
        "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
}

if __name__ == "__main__":
    do_pptx_pics()
    do_slides()
    do_photos()
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json লেখা হলো")
