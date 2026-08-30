# -*- coding: utf-8 -*-
"""অধ্যায় ২৪-এর ছবি প্রস্তুত করা।

দুই উৎস:

১।  **ইনস্টিটিউটের কানেকশন ডেক** — `HW Connection Diagram All.pptx`-এর
    ৩০ নং স্লাইড।  দুই ডেকের প্রতিটি স্লাইডের লেখা বের করে দেখা হয়েছে;
    বিতরণের সিঁড়িটা — খুঁটি → মেইন মিটার → মেইন এমসিবি → সাব-মিটার,
    সুইচবোর্ড, এসডিবি বাক্স, ডিপি সুইচ ও মোটর — কেবল ওই একটি স্লাইডেই
    আছে, আর সেটি অধ্যায় ২১ ব্যবহার করেনি (২১ নিয়েছে ২৯, ৩১, ৩২, ৩৩)।

    **স্লাইডে আর্থ কন্ডাক্টর আঁকা নেই** — কেবল লাল ও কালো, অর্থাৎ ফেজ
    ও নিউট্রাল।  বিএনবিসি ১.৩.১৩ অনুযায়ী প্রতিটি ফিড সংযোগে ইসিসি
    থাকতেই হবে; ২৪.১.৩-এর লেখায় কথাটা খোলাখুলি বলা আছে।  অধ্যায় ২০-এর
    "Magnetic Conductor"-এর মতোই — সোর্সের অসম্পূর্ণতা বইয়ে চুপচাপ
    যাবে না।

২।  **উইকিমিডিয়া কমন্স** — এমডিবির আলোকচিত্র ইনস্টিটিউটের কোনো ফাইলে
    নেই (`Electrical House Wiring book.docx`-এর ২১০টি ছবির একটিও বোর্ডের
    ভেতরের নয়, আর দুই ডেকের ছবিগুলো ক্যাটালগ-রেন্ডার)।

    Robertbh1984-এর ছ'টি ছবি একটি ভিলার মেইন প্যানেল **তৈরি হওয়ার
    ক্রমে** তোলা — খালি বাক্সে ঝুলন্ত তার থেকে শুরু করে সাজানো,
    ট্যাগ করা, ঢাকনা লাগানো বোর্ড পর্যন্ত।  এই অধ্যায়ের দ্বিতীয়
    অর্ধেকটা ঠিক ওই ক্রমেই লেখা, তাই ছবিগুলো একসঙ্গে একটা কাজের
    বিবরণ হয়ে যায়।

      ph_start   কাজের শুরু — খালি এনক্লোজার, কনডুইট নেমেছে, তার ঝুলছে
      ph_done    কাজের শেষ — ডিন রেলে সারি সারি এমসিবি, নিচে দুই বার
      ph_ready   সামনে থেকে সম্পূর্ণ বোর্ড — ডেড-ফ্রন্ট, স্বচ্ছ ঢাকনা,
                 দরজায় `380 V` / `220 V` লেখা (বিএনবিসি ১.৩.৩৪(ঘ))
      ph_bars    নিউট্রাল ও আর্থিং বার, লাল ইনসুলেটরে বসানো
      ph_lug     আর্থিং বারে সারি সারি রিং লাগ, প্রতিটি তারে নম্বর
      ph_bad     স্লোভাকিয়ার পুরনো বোর্ড — এলোমেলো, ক্রসিং, ধুলো;
                 বিএনবিসি ১.৩.১৭.৪(খ) যা নিষেধ করেছে তারই ছবি
      ph_ferrule ফেরুল ও ক্রিম্প প্লায়ার — একটি কোরে ফেরুল নেই, খেই
                 ছড়ানো (তুলনাটাই ছবির কাজ)
      ph_lugkind তিন রকম লাগ, মিলিমিটার-স্কেলসহ; মাঝেরটির গায়ে
                 `GT 10-5` — অর্থাৎ 10 বর্গমিমি তার, M5 বোল্ট
      ph_meter   মিটার ও তার পরের ডিপি ব্রেকার, মিটারের সিলের তারসহ

চালানোর নিয়ম:  python assets_ch24.py     (Book/build/ থেকে)
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
OUT = os.path.join(HERE, "assets", "ch24")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

UA = {"User-Agent": "rapti-book/1.0 (textbook figure prep)"}
API = "https://commons.wikimedia.org/w/api.php"

HW = "HW Connection Diagram All.pptx"

# ── ১।  কানেকশন ডেকের স্লাইড ───────────────────────────────────────────
SLIDES = {
    "h30_tree": (HW, 29, (0.00, 0.00, 1.00, 1.00)),
}
EXPECT = {
    "h30_tree": ["Main", "Meter", "Sub", "MCB", "SDB", "Box", "Motor",
                 "Switch", "Board", "Light"],
}

# ── ২।  কমন্স ──────────────────────────────────────────────────────────
# নাম → (কমন্সের ফাইলনাম, প্রত্যাশিত মাপ, ক্রপ-বক্স, সর্বোচ্চ চওড়া, কনট্রাস্ট)
PHOTOS = {
    # ১৫.৪ সেমিতে পুরো চওড়ায় বসাতে হলে ছবিটা এত খাড়া হলে চলে না —
    # ১:১.২২ অনুপাতে গোটা পাতা খেয়ে ফেলে (অধ্যায় ১১-এর শিক্ষা)
    "ph_start":   ("MAIN PANEL 1.jpg", (3120, 4160),
                   (0.06, 0.20, 0.98, 0.86), 1500, 1.10),
    "ph_done":    ("MAIN PANEL AND CABLES.jpg", (3120, 4160),
                   (0.00, 0.28, 0.72, 1.00), 1500, 1.06),
    "ph_ready":   ("MAIN PANEL READY.jpg", (3120, 4160),
                   (0.00, 0.00, 0.78, 1.00), 1700, 1.06),
    "ph_bars":    ("MAIN PANEL 1.2.jpg", (3120, 4160),
                   (0.02, 0.40, 1.00, 0.82), 1700, 1.06),
    "ph_lug":     ("MAIN PANEL BAR.jpg", (3120, 4160),
                   (0.00, 0.38, 0.76, 0.78), 1600, 1.08),
    "ph_bad":     ("Distribution board in Slovakia 01.jpg", (4000, 3000),
                   (0.03, 0.03, 0.97, 0.97), 1500, 1.06),
    "ph_ferrule": ("Wire ferrules with and without insulation.jpg",
                   (5648, 2816), (0.00, 0.02, 1.00, 0.98), 1700, 1.04),
    "ph_lugkind": ("Kabelschuh.jpg", (592, 554),
                   (0.02, 0.02, 0.99, 0.99), 592, 1.05),
    "ph_meter":   ("Electric meter and the circuit breaker.JPG",
                   (4608, 3456), (0.24, 0.02, 0.94, 0.98), 1400, 1.06),
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


# ── ১।  স্লাইড ─────────────────────────────────────────────────────────
def slide_pdf(name):
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


# ── ২।  কমন্স ──────────────────────────────────────────────────────────
def _get(url):
    for _ in range(6):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=300).read()
        except Exception as exc:                 # ৪২৯ এলে থেমে আবার চেষ্টা
            print("   … আবার চেষ্টা:", exc)
            time.sleep(25)
    raise SystemExit("✗ নামানো গেল না: " + url)


def commons_url(fname):
    cache = os.path.join(CACHE, "ch24_urls.json")
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
        time.sleep(3)
    return urls[fname]


def fetch(fname):
    fn = os.path.join(CACHE, "ch24_" + fname.replace(" ", "_"))
    if not os.path.exists(fn) or os.path.getsize(fn) < 4096:
        open(fn, "wb").write(_get(commons_url(fname)))
        time.sleep(12)
    return open(fn, "rb").read()


def do_photos(only=None):
    for name, (fname, size, box, wmax, contrast) in PHOTOS.items():
        if only and name not in only:
            continue
        # EXIF-এর ওরিয়েন্টেশন আগে মেলানো — ক্রপ-বক্স লেখা হয়েছে
        # commons.wikimedia.org যেভাবে ছবিটি দেখায় সেই হিসাবে
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
# `ch24.py` এই ফাইলটাই পড়ে অধ্যায়ের শেষের ❖ চিত্রসূত্র বাক্সটি বানায়,
# তাই কৃতজ্ঞতা আর ছবি কখনো আলাদা হয়ে যাবে না।  হাতে-লেখা তালিকা নয়
# (অধ্যায় ২২-এর শিক্ষা — তালিকা বাসি হয়ে গিয়ে চারটি কৃতজ্ঞতা বাদ
# পড়েছিল, যা CC BY-SA-র জন্য লাইসেন্স-লঙ্ঘন)।
CREDITS = {
    "ph_start": {"title": "Main panel 1",
                 "author": "Robertbh1984", "licence": "CC BY-SA 4.0"},
    "ph_done": {"title": "Main panel and cables",
                "author": "Robertbh1984", "licence": "CC BY-SA 4.0"},
    "ph_ready": {"title": "Main panel ready",
                 "author": "Robertbh1984", "licence": "CC BY-SA 4.0"},
    "ph_bars": {"title": "Main panel 1.2",
                "author": "Robertbh1984", "licence": "CC BY-SA 4.0"},
    "ph_lug": {"title": "Main panel bar",
               "author": "Robertbh1984", "licence": "CC BY-SA 4.0"},
    "ph_bad": {"title": "Distribution board in Slovakia 01",
               "author": "Oto Zapletal", "licence": "CC BY 4.0"},
    "ph_ferrule": {"title": "Wire ferrules with and without insulation",
                   "author": "Simon A. Eugster", "licence": "CC BY-SA 3.0"},
    "ph_lugkind": {"title": "Kabelschuh",
                   "author": "Ulfbastel", "licence": "পাবলিক ডোমেইন"},
    "ph_meter": {"title": "Electric meter and the circuit breaker",
                 "author": "Zimin.V.G.", "licence": "CC BY-SA 4.0"},
    "rapti_slide": {
        "files": sorted(SLIDES),
        "source": "RAPTI — HW Connection Diagram All.pptx (slide 30)",
        "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
}

if __name__ == "__main__":
    import sys
    only = set(sys.argv[1:]) or None
    do_slides()
    do_photos(only)
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json লেখা হলো")
