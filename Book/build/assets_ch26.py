# -*- coding: utf-8 -*-
"""অধ্যায় ২৬-এর ছবি প্রস্তুত করা।

**ইনস্টিটিউটের ফাইলে কন্ডুইটের নতুন কিছু নেই — এটা যাচাই করা হয়ে গেছে,
আবার খুঁজতে যাওয়ার দরকার নেই।**

  · `HW 1st class.pptx`-এর স্লাইড ৮৪, ৮৫ ও ৮৬-ই কন্ডুইটের একমাত্র
    স্লাইড (দুই ডেকের ১৩৯টি স্লাইডের লেখা বের করে মিলিয়ে দেখা হয়েছে)।
    ওই স্লাইডের ছবিগুলোই `Electrical House Wiring book.docx`-এর
    image124 / image129–132 — আর **সেগুলো অধ্যায় ১৪ ইতিমধ্যে ছেপেছে**
    (`assets_ch14.DOC_IMAGES`-এর `p_cable_in_pipe`, `p_conceal_slab`,
    `p_conceal_wall`, `p_surface_pipe`, `p_surface_ceil`)।  অধ্যায় ১৪
    কন্ডুইটের *পরিচয়* দিয়েছে;  এই অধ্যায় *কাজটা* শেখায়, তাই একটিও
    ছবি ফিরিয়ে আনা হয়নি।
  · `HW Connection Diagram All.pptx`-এর স্লাইড ৩৪ ও ৩৬ অধ্যায় ২৫-এ
    ছাপা হয়ে গেছে, আর স্লাইড ৩৫ চ্যানেল-রানের রূপভেদ — সেটি
    অধ্যায় ২৭-এর।

তাই সব আলোকচিত্র **উইকিমিডিয়া কমন্স** থেকে (অধ্যায় ১৯ ও ২৩-এর
পদ্ধতি) — ক্রেডিট `credits.json`-এ লেখা থাকে, কিন্তু বইয়ে
❖ চিত্রসূত্র বাক্স ছাপা হয় না (২০২৬-০৮-৩০-এর নির্দেশ)।

কোনটা কেন বেছে নেওয়া হলো:

  ph_pvc      PVC কন্ডুইট — পাইপ ও তার ফিটিং, দোকানে যেমন দেখায়
  ph_gi       ভারী জিআই কন্ডুইট, মুখ কাটা — দেয়ালের পুরুত্ব দেখা যায়
  ph_thread   জিআই পাইপের মুখে কাটা প্যাঁচ (চওড়া-বেঁটে ফ্রেম,
              `strip_callouts`-এর জন্য)
  ph_spring   **বেন্ডিং স্প্রিং** — PVC পাইপ চ্যাপ্টা না করে বাঁকানোর
              একমাত্র হাতিয়ার;  কমন্সে এটাই একমাত্র পরিষ্কার ছবি
  ph_bender   হাতে-ধরা বেন্ডার দিয়ে ধাতব পাইপ বাঁকানো হচ্ছে
  ph_slab     **ছাদের ঢালাইয়ের ভেতরে বসে যাওয়া কন্ডুইট** — কনসিল্ড
              কাজের যে ধাপটা প্লাস্টারের পরে আর কোনোদিন দেখা যায় না
  ph_wall     দেয়ালের খাঁজে পাইপ ও বাক্স, প্লাস্টারের আগে
  ph_box      সুইচের জন্য দেয়ালে বসানো গোল বাক্স
  ph_surface  সারফেস কন্ডুইট — দেয়ালের গায়ে পাইপ, স্যাডল ও বাক্স
  ph_fittings স্যাডল, কাপলার ও অন্যান্য ফিটিং একসঙ্গে
  ph_uv       **রোদে দশ বছর থেকে ফেটে যাওয়া ২০ mm PVC পাইপ** —
              ২৬.৩.৪-এর পুরো যুক্তিটাই এই একটা ছবিতে
  ph_room     সারি সারি কন্ডুইট — বড় স্থাপনায় কাজটা কেমন দেখায়

তিনটি বাদ পড়েছে, কারণসহ:  `Leerrohr-Wand.jpg` ২০০×৪২৫ px (ছাপার
অযোগ্য), `金属製可とう管.jpg` ৬৫৪×৪৩৮ px (ফ্লেক্সিবল পাইপ চেনানোর
জন্য যথেষ্ট বড় নয়, আর বিএনবিসি ১.৩.১৪.১.৩ অনুযায়ী ওটা ব্যতিক্রম —
পুরো একটা ছবির দাবি রাখে না), আর `Schellen für runde Kabelkänale.jpg`
(স্যাডল `ph_fittings`-এই আছে)।

চালানোর নিয়ম:  python assets_ch26.py     (Book/build/ থেকে)
"""
import io
import json
import os
import time
import urllib.parse
import urllib.request

from PIL import Image, ImageEnhance, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "ch26")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

UA = {"User-Agent": "rapti-book/1.0 (textbook figure prep)"}
API = "https://commons.wikimedia.org/w/api.php"

# নাম → (কমন্সের ফাইলনাম, প্রত্যাশিত মাপ, ক্রপ-বক্স, সর্বোচ্চ চওড়া, কনট্রাস্ট)
PHOTOS = {
    # ── কী জিনিস, দোকানে/সাইটে কেমন দেখায় ──────────────────────────
    "ph_pvc":      ("9922Photos taken during 2020 coronavirus pandemic "
                    "Baliuag, Bulacan 24.jpg", (4608, 3456),
                    (0.11, 0.36, 0.93, 0.96), 1500, 1.06),
    "ph_gi":       ("厚鋼電線管 (G36).JPG", (1024, 768),
                    (0.00, 0.26, 0.66, 0.60), 1024, 1.10),
    "ph_room":     ("MEASURING CONDUIT 01.JPG", (4288, 3216),
                    (0.04, 0.02, 0.96, 0.92), 1500, 1.08),
    # ── ফিটিংস ও বাক্স ──────────────────────────────────────────────
    "ph_fittings": ("Conduit Straps, Fittings, and Plug "
                    "J. Morris CC BY-SA-3.0.jpg", (1152, 2048),
                    (0.02, 0.02, 0.98, 0.98), 1152, 1.08),
    "ph_clips":    ("16mm fixators.JPG", (3648, 2736),
                    (0.10, 0.10, 0.90, 0.90), 1300, 1.06),
    "ph_jbox":     ("Internal junction box 68mm.JPG", (3648, 2736),
                    (0.16, 0.06, 0.84, 0.98), 1100, 1.06),
    "ph_saddle":   ("Bügelschelle rund mit Kabelschutzschlauch.jpg",
                    (5184, 3456), (0.18, 0.10, 0.82, 0.92), 1300, 1.06),
    # ── বাঁক ────────────────────────────────────────────────────────
    "ph_bend":     ("EMT conduit 90 degree bend corrected "
                    "J. Morris CC BY-SA-3.0.jpg", (2048, 1152),
                    (0.05, 0.02, 0.92, 0.86), 1400, 1.10),
    "ph_spring":   ("Buigveer2.jpg", (4928, 3264),
                    (0.05, 0.10, 0.95, 0.90), 1500, 1.06),
    "ph_bender":   ("Demonstration of a conduit bender (2).jpg", (3500, 2332),
                    (0.39, 0.38, 0.66, 0.78), 1000, 1.08),
    # ── কাজ চলাকালীন ───────────────────────────────────────────────
    "ph_slab":     ("Electcablesinconstruction2.jpg", (1000, 750),
                    (0.00, 0.00, 1.00, 1.00), 1000, 1.08),
    "ph_wallbox":  ("Keskuse 14 installation box for light switch.JPG",
                    (2736, 3648), (0.24, 0.24, 0.83, 0.78), 1100, 1.08),
    "ph_surface":  ("Conduit junction boxes2.jpg", (1920, 2560),
                    (0.02, 0.02, 0.98, 0.80), 1300, 1.08),
    # ── ২০২৬-০৯-০৪-এ যোগ করা (ব্যবহারকারীর নির্দেশ: আরও বাস্তব ছবি) ──
    "ph_mark":     ("9922Photos taken during 2020 coronavirus pandemic "
                    "Baliuag, Bulacan 29.jpg", (4608, 3456),
                    (0.02, 0.28, 0.86, 0.80), 1500, 1.12),
    "ph_flex":     ("Electrical conduit.JPG", (3648, 2736),
                    (0.06, 0.04, 0.96, 0.96), 1300, 1.06),
    "ph_flexrun":  ("Kabelkanal rund 20221.jpg", (4048, 2624),
                    (0.04, 0.10, 0.96, 0.92), 1300, 1.08),
    "ph_fish":     ("Fish tape.webp", (1583, 3924),
                    (0.02, 0.55, 0.98, 1.00), 1100, 1.06),
    "ph_fishtip":  ("Fish tape material comparison.jpg", (2868, 1400),
                    (0.02, 0.04, 0.98, 0.96), 1500, 1.10),
    "ph_ceilbox":  ("Lasdoos duitsland.jpg", (1364, 1300),
                    (0.03, 0.03, 0.97, 0.97), 1300, 1.08),
    "ph_boxwired": ("Junction box for wikipedia.JPG", (3780, 1560),
                    (0.725, 0.508, 0.999, 0.998), 1300, 1.08),
}


def flatten(im):
    """RGBA → সাদার উপরে বসানো RGB।  না করলে ছাপায় কালো আসে (ch18)।"""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def frac_crop(im, box):
    x0, y0, x1, y1 = box
    w, h = im.size
    return im.crop((round(x0 * w), round(y0 * h),
                    round(x1 * w), round(y1 * h)))


def _get(url):
    for _ in range(6):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=300).read()
        except Exception as exc:                 # ৪২৯ এলে থেমে আবার চেষ্টা
            print("   … আবার চেষ্টা:", exc)
            time.sleep(25)
    raise SystemExit("✗ নামানো গেল না: " + url)


def _meta():
    cache = os.path.join(CACHE, "ch26_urls2.json")
    return (json.load(open(cache)) if os.path.exists(cache) else {}), cache


# কয়েকটি ছবির সামান্য অংশ কাটা হয়, তাই তাদের বড় থাম্বনেইল লাগে
THUMBW = {"Junction box for wikipedia.JPG": 3600}


def commons_meta(fname):
    urls, cache = _meta()
    if fname not in urls:
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "titles": "File:" + fname,
            "prop": "imageinfo", "iiprop": "url|size|extmetadata",
            "iiurlwidth": str(THUMBW.get(fname, 1800))})
        d = json.loads(_get(API + "?" + q))
        page = next(iter(d["query"]["pages"].values()))
        if "imageinfo" not in page:
            raise SystemExit(f"✗ কমন্সে পাওয়া গেল না: {fname}")
        ii = page["imageinfo"][0]
        em = ii["extmetadata"]

        def _f(k):
            import re
            v = em.get(k, {}).get("value", "")
            return re.sub("<[^>]+>", "", v).strip()
        urls[fname] = {"url": ii.get("thumburl") or ii["url"],
                       "size": [ii["width"], ii["height"]],
                       "artist": _f("Artist") or "অজ্ঞাত",
                       "licence": _f("LicenseShortName") or "?",
                       "page": "https://commons.wikimedia.org/wiki/File:"
                               + urllib.parse.quote(fname.replace(" ", "_"))}
        json.dump(urls, open(cache, "w"), ensure_ascii=False, indent=1)
        time.sleep(4)
    return urls[fname]


def fetch(fname):
    """কমন্সের **থাম্বনেইল** নামানো হয় (সর্বোচ্চ ১৮০০ px চওড়া)।

    আসল ফাইল সরাসরি টানলে upload.wikimedia.org ৪২৯ ফেরত দেয় এবং
    নিজেই থাম্বনেইল ব্যবহার করতে বলে।  ছাপার জন্য ১৮০০ px যথেষ্ট —
    ১৫.৪ সেমিতে সেটি ~৩০০ dpi।  তার-চিহ্ন (tripwire) হিসেবে **আসল
    ফাইলের** পিক্সেল-মাপ `credits`-এ রাখা হয় ও যাচাই করা হয়, তাই
    কমন্সে ছবিটি বদলালে ধরা পড়বে।
    """
    safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in fname)
    fn = os.path.join(CACHE, "ch26_" + safe)
    if not os.path.exists(fn) or os.path.getsize(fn) < 4096:
        open(fn, "wb").write(_get(commons_meta(fname)["url"]))
        time.sleep(12)
    return open(fn, "rb").read()


def do_photos(only=None):
    for name, (fname, size, box, wmax, contrast) in PHOTOS.items():
        if only and name not in only:
            continue
        # EXIF-এর ওরিয়েন্টেশন আগে মেলানো — ক্রপ-বক্স লেখা হয়েছে
        # commons.wikimedia.org যেভাবে ছবিটি দেখায় সেই হিসাবে
        real = tuple(commons_meta(fname)["size"])
        if real != size:
            raise SystemExit(f"✗ {name}: {fname}-এর আসল মাপ {real}, "
                             f"হওয়ার কথা {size} — কমন্সে ছবিটি বদলেছে, "
                             f"ক্রপ-বক্স আবার মিলিয়ে নিতে হবে")
        im = flatten(ImageOps.exif_transpose(Image.open(io.BytesIO(
            fetch(fname)))))
        im = frac_crop(im, box)
        if im.width > wmax:
            im = im.resize((wmax, round(im.height * wmax / im.width)),
                           Image.LANCZOS)
        if contrast != 1.0:
            im = ImageEnhance.Contrast(im).enhance(contrast)
        im.save(os.path.join(OUT, name + ".jpg"), quality=92)
        print("✓", name, im.size, f"({fname})")


def do_credits():
    """প্রকল্পের প্রামাণ্য নথি।  ২০২৬-০৮-৩০ থেকে বইয়ে ❖ চিত্রসূত্র বাক্স
    ছাপা হয় না (ব্যবহারকারীর নির্দেশ), কিন্তু ফাইলটি রাখা হয়।"""
    creds = {}
    for name, (fname, *_rest) in PHOTOS.items():
        m = commons_meta(fname)
        creds[name] = {"file": fname, "artist": m["artist"],
                       "licence": m["licence"], "page": m["page"]}
    json.dump(creds, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=1)
    print("✓ credits.json")


if __name__ == "__main__":
    do_photos()
    do_credits()
