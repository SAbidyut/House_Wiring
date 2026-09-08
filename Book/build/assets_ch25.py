# -*- coding: utf-8 -*-
"""অধ্যায় ২৫-এর ছবি প্রস্তুত করা।

দুই উৎস:

১।  **ইনস্টিটিউটের কানেকশন ডেক** — `HW Connection Diagram All.pptx`-এর
    ৩৩, ৩৪ ও ৩৬ নং স্লাইড।  দুই ডেকের প্রতিটি স্লাইডের লেখা বের করে
    মিলিয়ে দেখা হয়েছে;  ফ্ল্যাটের এসডিবি কেবল ওই তিনটিতেই আছে।

      h33_board  স্লাইড ৩৩-এর **কেবল বোর্ডের ভেতরটা** — মেইন এমসিবি,
                 আরসিসিবি, এসপিডি, নিউট্রাল ও আর্থিং বার, ওয়ের সারি।
                 অধ্যায় ২১ গোটা স্লাইডটি একবার ছেপেছে (চিত্র ২১.১১);
                 এখানে ধূসর বাক্সটুকু আলাদা করে ২.৩ গুণ বড় করে কাটা
                 হয়েছে, যাতে ব্রেকারের গায়ের লেখা পড়া যায় — সেটাই
                 এই অধ্যায়ের কাজ, বারের ছবি নয়।
      h34_flat   স্লাইড ৩৪ — এসডিবি থেকে গোটা ফ্ল্যাটের কানেকশন
                 (পিয়ানো সুইচবোর্ড, সিলিং রোজ, ফ্যান, এক্সহস্ট, বেল)।
      h36_flat   স্লাইড ৩৬ — দুই ঘরের ফ্ল্যাট, একদিকে পিয়ানো একদিকে
                 গ্যাং বোর্ড।

    স্লাইড ৩৫ ছাপা হয়নি — সেটি ৩৪-এরই রূপভেদ (গ্যাং বোর্ড ও চ্যানেল
    রান), আর দুটোই ৩৬-এ আছে।

    **তিনটি স্লাইডের একটিতেও আর্থ কন্ডাক্টর আঁকা নেই** — কেবল লাল ও
    কালো।  বিএনবিসি ১.৩.১৩ প্রতিটি ফিড সংযোগে ইসিসি বাধ্যতামূলক করেছে,
    আর ২৫.১.৪-এর ⚠ বাক্সে কথাটা খোলাখুলি বলা আছে।  অধ্যায় ২০-এর
    "Magnetic Conductor" ও অধ্যায় ২৪-এর একই ব্যবস্থা।

২।  **উইকিমিডিয়া কমন্স** — ফ্ল্যাটের বোর্ডের আলোকচিত্র ইনস্টিটিউটের
    কোনো ফাইলে নেই (`Electrical House Wiring book.docx`-এর ২১০টি ছবির
    একটিও নয়, দুই ডেকের ছবিগুলোও ক্যাটালগ-রেন্ডার)।  অধ্যায় ২৪-এর
    ছবিগুলো একটি **এমডিবির**, ফ্ল্যাটের বোর্ডের নয় — তাই একটিও এখানে
    ফিরিয়ে আনা হয়নি।

      ph_empty   খালি এনক্লোজার — ডিন রেল, নিউট্রাল ও আর্থিং বার,
                 আলাদা করে রাখা ঢাকনা
      ph_kit     একটি ফ্ল্যাটের গোটা মালামাল একসঙ্গে — এমসিবি, আরসিবিও,
                 বার, ফেরুল, রেল-স্টপার
      ph_comb    কম্ব বাসবার, এমসিবির সারি ও খালি বাক্স — কেনার পর,
                 বসানোর আগে
      ph_bridge  কম্ব বাসবার বসানো অবস্থায় (চওড়া-বেঁটে ফ্রেম)
      ph_work    কাজ চলছে — রেল বসেছে, ব্রেকার বসেছে, তার এখনো খোলা
      ph_flat    শেষ হওয়া ফ্ল্যাটের বোর্ড — উপরে ও নিচে দুই বার
      ph_rows    দুই সারির বোর্ড, প্রতিটি ওয়ের গায়ে QF1…/RCBO1… লেখা
                 (`dia_ch25.d18_rows` আঁকে, কিন্তু অধ্যায়ে ব্যবহার হয়নি —
                 কারণ `dia_ch25.py`-র docstring-এ লেখা আছে)

`DIN rail.JPG` ও `Fuse box with overlimited circuit breakers.JPG` তালিকা থেকে
বাদ:  প্রথমটি ৩:১ ফিতা, `pair_panels`-এ সমান উচ্চতায় বসাতে গেলে ক্যানভাস
ছাড়িয়ে যায়, আর ডিন রেল চিত্র ২৫.৩-এই লেবেল করা আছে;  দ্বিতীয়টি বারবার
কমন্সের ৪২৯ পেয়েছে, আর ভুলের তালিকা সারণি ২৫.১৩-ই বহন করে।
      ph_chart   ডেড-ফ্রন্টের গায়ে ছাপা সার্কিট চার্ট
      ph_neat    গোছানো ভেতর — লাল ফেজ, নীল নিউট্রাল, সারি সারি

চালানোর নিয়ম:  python assets_ch25.py     (Book/build/ থেকে)
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
OUT = os.path.join(HERE, "assets", "ch25")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

UA = {"User-Agent": "rapti-book/1.0 (textbook figure prep)"}
API = "https://commons.wikimedia.org/w/api.php"

HW = "HW Connection Diagram All.pptx"

# ── ১।  কানেকশন ডেকের স্লাইড ───────────────────────────────────────────
# নাম → (সোর্স ফাইল, PDF পৃষ্ঠা-সূচক, (x0, y0, x1, y1) ভগ্নাংশে)
SLIDES = {
    "h33_board": (HW, 32, (0.272, 0.000, 1.000, 0.605)),
    "h34_flat":  (HW, 33, (0.000, 0.000, 1.000, 1.000)),
    "h36_flat":  (HW, 35, (0.000, 0.000, 1.000, 1.000)),
}

# পৃষ্ঠার লেখায় এই শব্দগুলো থাকতেই হবে — এক স্লাইড এদিক-ওদিক হলে ধরা পড়বে
EXPECT = {
    "h33_board": ["RCCB", "SPD", "Neutral", "Busbar", "Earthing", "MCB"],
    "h34_flat":  ["SDB", "Piano", "Ceiling", "Exhaust", "Doorbell", "MCB"],
    "h36_flat":  ["SDB", "Piano", "Gang", "Ceiling", "Rose", "Doorbell"],
}

# ── ২।  কমন্স ──────────────────────────────────────────────────────────
# নাম → (কমন্সের ফাইলনাম, প্রত্যাশিত মাপ, ক্রপ-বক্স, সর্বোচ্চ চওড়া, কনট্রাস্ট)
PHOTOS = {
    "ph_empty":  ("European fuse box inside.JPG", (2736, 3648),
                  (0.03, 0.03, 0.97, 0.97), 1400, 1.08),
    "ph_kit":    ("Punane 39 - materials.JPG", (3648, 2736),
                  (0.03, 0.03, 0.97, 0.97), 1600, 1.08),
    "ph_comb":   ("Fuse box preparing to installation.JPG", (3648, 2638),
                  (0.02, 0.05, 0.98, 0.95), 1600, 1.08),
    "ph_bridge": ("Wiring of European fuse box.JPG", (3648, 2056),
                  (0.02, 0.03, 0.78, 0.97), 1500, 1.08),
    "ph_work":   ("Linnamäe 37 - fuse box wiring process.JPG", (3648, 2736),
                  (0.03, 0.05, 0.97, 0.97), 1500, 1.08),
    "ph_flat":   ("Paekaare 24 - fuse box.JPG", (2056, 3648),
                  (0.03, 0.03, 0.97, 0.97), 1200, 1.08),
    "ph_rows":   ("Fuse box on hager components.JPG", (2650, 3620),
                  (0.03, 0.01, 0.97, 0.78), 1300, 1.08),
    "ph_chart":  ("Small house distribution panel 1.jpg", (3148, 4722),
                  (0.04, 0.03, 0.96, 0.97), 1200, 1.06),
    "ph_neat":   ("Small house distribution panel 2.jpg", (2923, 4385),
                  (0.03, 0.02, 0.97, 0.98), 1200, 1.06),
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
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def frac_crop(im, box):
    x0, y0, x1, y1 = box
    w, h = im.size
    return im.crop((round(x0 * w), round(y0 * h),
                    round(x1 * w), round(y1 * h)))


def slide_pdf(name):
    """PPTX → PDF, একবার, `.slidepdf/`-এ জমা থাকে।"""
    dst = os.path.join(CACHE, os.path.splitext(name)[0] + ".pdf")
    if not os.path.exists(dst):
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                        "--outdir", CACHE, os.path.join(ROOT, name)],
                       check=True)
    return dst


def do_slides():
    for name, (src, pg, box) in SLIDES.items():
        d = pymupdf.open(slide_pdf(src))
        words = d[pg].get_text()
        missing = [k for k in EXPECT[name] if k not in words]
        if missing:
            raise SystemExit(f"✗ {name}: {src}-এর {pg + 1} নং পৃষ্ঠায় "
                             f"{missing} নেই — স্লাইডের ক্রম বদলেছে")
        r = d[pg].rect
        clip = pymupdf.Rect(r.width * box[0], r.height * box[1],
                            r.width * box[2], r.height * box[3])
        pix = d[pg].get_pixmap(dpi=300, clip=clip)
        im = autocrop(Image.open(io.BytesIO(pix.tobytes("png"))))
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


def _meta():
    cache = os.path.join(CACHE, "ch25_urls.json")
    return (json.load(open(cache)) if os.path.exists(cache) else {}), cache


def commons_meta(fname):
    urls, cache = _meta()
    if fname not in urls:
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "titles": "File:" + fname,
            "prop": "imageinfo", "iiprop": "url|extmetadata"})
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
        urls[fname] = {"url": ii["url"],
                       "artist": _f("Artist") or "অজ্ঞাত",
                       "licence": _f("LicenseShortName") or "?",
                       "page": "https://commons.wikimedia.org/wiki/File:"
                               + urllib.parse.quote(fname.replace(" ", "_"))}
        json.dump(urls, open(cache, "w"), ensure_ascii=False, indent=1)
        time.sleep(4)
    return urls[fname]


def fetch(fname):
    fn = os.path.join(CACHE, "ch25_" + fname.replace(" ", "_"))
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


def do_credits():
    """প্রকল্পের প্রামাণ্য নথি।  ২০২৬-০৮-৩০ থেকে বইয়ে ❖ চিত্রসূত্র বাক্স
    ছাপা হয় না (ব্যবহারকারীর নির্দেশ), কিন্তু ফাইলটি রাখা হয়।"""
    creds = {}
    for name, (fname, *_rest) in PHOTOS.items():
        m = commons_meta(fname)
        creds[name] = {"file": fname, "artist": m["artist"],
                       "licence": m["licence"], "page": m["page"]}
    creds["_rapti_slides"] = {
        "files": sorted(SLIDES),
        "source": "RAPTI — HW Connection Diagram All.pptx (স্লাইড ৩৩, ৩৪, ৩৬)",
    }
    json.dump(creds, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=1)
    print("✓ credits.json")


if __name__ == "__main__":
    do_slides()
    do_photos()
    do_credits()
