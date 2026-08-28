# -*- coding: utf-8 -*-
"""অধ্যায় ২৩-এর ছবি প্রস্তুত করা — ক্যাবল ও ক্যাবল ক্যালকুলেশন।

দুই জায়গা থেকে ছবি আসে, আর ভাগটা ইচ্ছাকৃত:

**উইকিমিডিয়া কমন্স** — আসল ক্যাবলের আলোকচিত্র।  দুই ডায়াগ্রাম ডেকের
প্রতিটি স্লাইডের লেখা বের করে দেখা হয়েছে, ক্যাবল-নির্দিষ্ট স্লাইড নেই;
`Electrical House Wiring book.docx`-এও ক্যাবলের ছবি নেই।  তাই এগারোটি
আলোকচিত্রই কমন্স থেকে।  বাছাইয়ের শর্ত ছিল একটাই — **ছবি দেখে জিনিসটা
চেনা যাবে কি না**, কারণ এই অধ্যায়ের আসল পাঠ ক্যাবল হাতে নিয়ে চেনা আর
গায়ের লেখা পড়া।

  ph_print       ক্যাবলের গায়ে ছাপা লেখা — এই অধ্যায়ের কেন্দ্রীয় ছবি
  ph_print_face  ওই লেখাটুকুর টাইট ক্রপ (কল-আউটের জন্য)
  ph_xsec        কাটা মুখ — শিথ, ফিলার, ইনসুলেশন, খেই, নিচে মিলিমিটার স্কেল
  ph_sheath      শিথড ৩-কোর, খোলা অবস্থায়, সলিড কন্ডাক্টর
  ph_solid       ওই ছবিরই খালি তামার ডগা — ক্লাস ১
  ph_te          ফ্ল্যাট টুইন-অ্যান্ড-আর্থ, BS 6004, 6 বর্গমিমি — ক্লাস ২
  ph_flex        সরু খেইয়ের ফ্লেক্সিবল কন্ডাক্টর — ক্লাস ৫
  ph_colors      পাঁচ কোরের রঙ, L1/L2/L3/N/PE ফেরুলসহ
  ph_sector      অ্যালুমিনিয়াম ৪-কোর, সেক্টর আকৃতির কন্ডাক্টর (`se`)
  ph_lug         ক্যাবল লাগ — বিএনবিসি ১.৩.১৪.২.৪
  ph_burn        অতিরিক্ত কারেন্টে পুড়ে যাওয়া কন্ডাক্টর ও ফেরুল

**ইনস্টিটিউটের নিজের ফাইল** — `SUPER STAR Cables Technical Catalog
(FORCE).pdf`-এর টাইপ-নির্দেশক ব্লক তিনটি (`cat_bya`, `cat_byfy`,
`cat_flex`)।  বাংলাদেশের বাজারে ক্যাবলের নাম যেভাবে লেখা হয় — BYA/BAYA,
৪৫০/৭৫০ ভোল্ট, BDS 900 ও BS 6004 — সেটা এর চেয়ে ভালো করে আর কিছু দেখায়
না।  ক্যাটালগের **ছক** কিন্তু ছবি হিসেবে নয়, ওগুলো `ch23.py`-তে আসল
ওয়ার্ড টেবিল (বইয়ের নিয়ম)।

কৃতজ্ঞতা স্বীকার আইনি শর্ত (CC BY / CC BY-SA), ইচ্ছাধীন নয় — `ch23.py`
এই স্ক্রিপ্টের লেখা `credits.json` পড়েই শেষের ❖ চিত্রসূত্র বাক্সটি বানায়,
তাই ছবি আর কৃতজ্ঞতা কখনো আলাদা হয়ে যাবে না।  কখনোই হাতে-লেখা তালিকা
ফিরিয়ে আনা যাবে না (অধ্যায় ২২-এর শিক্ষা)।

চালানোর নিয়ম:  python assets_ch23.py     (Book/build/ থেকে)
"""
import io
import json
import os
import subprocess
import time
import urllib.parse

from PIL import Image, ImageEnhance, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, "assets", "ch23")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

UA = "rapti-book/1.0 (textbook figure prep)"
API = "https://commons.wikimedia.org/w/api.php"

CATALOG = os.path.join(ROOT, "SUPER STAR Cables Technical Catalog (FORCE).pdf")

# নাম → (কমন্সের ফাইলনাম, প্রত্যাশিত মাপ, ক্রপ-বক্স ভগ্নাংশে,
#         সর্বোচ্চ চওড়া, কনট্রাস্ট)
#
# মাপটা পাহারাদার:  কমন্সে ছবি বদলালে ক্রপ-বক্স আর মিলবে না — তখন এখানেই
# ধরা পড়বে, ছাপার পর নয়।
PHOTOS = {
    # ── গায়ের ছাপা লেখা ────────────────────────────────────────────────
    # 600 V CV 5.5 বর্গমিমি — শিথের গায়ে `<PS>E  KSDK  2006  5.5mm²`
    # স্পষ্ট ছাপা, পাশে তিনটি কোর খোলা।  এই একটা ছবিই অধ্যায়ের দাবিটা
    # প্রমাণ করে:  ক্যাবলের গায়েই সব লেখা থাকে, পড়তে জানলেই হলো।
    "ph_print":      ("600V CV 5.5sqmm.jpg",
                      (1600, 1200), (0.0, 0.355, 1.0, 0.635), 1500, 1.10),
    # কেবল লেখাটুকু — ১৫.৪ সেমিতে বসালে অক্ষর ১২ পয়েন্টের উপরে থাকে
    "ph_print_face": ("600V CV 5.5sqmm.jpg",
                      (1600, 1200), (0.018, 0.428, 0.680, 0.560), 1400, 1.20),

    # ── গঠন ────────────────────────────────────────────────────────────
    # কাটা মুখ — বাইরের শিথ, ভেতরে ফিলার, তিনটি কোরে আলাদা ইনসুলেশন,
    # প্রতিটির ভেতরে গোছা করা খেই।  নিচে মিলিমিটার স্কেল, তাই মাপটাও
    # চোখে পড়ে।
    "ph_xsec":       ("Cross section of an older US power cable.jpg",
                      (4032, 3024), (0.26, 0.10, 0.84, 1.0), 1400, 1.10),

    # শিথ ছাড়ানো ৩-কোর — বাদামি/নীল/সবুজ-হলুদ, কন্ডাক্টর সলিড
    "ph_sheath":     ("Installation Cable MMJ 3x2,5S.jpg",
                      (4000, 3000), (0.0, 0.20, 0.86, 1.0), 1500, 1.06),
    # ওই ছবিরই খালি তামার ডগা — ক্লাস ১ (সলিড), এক গাছি তার
    "ph_solid":      ("Installation Cable MMJ 3x2,5S.jpg",
                      (4000, 3000), (0.60, 0.24, 0.82, 0.50), 900, 1.10),

    # ── কন্ডাক্টরের শ্রেণি ──────────────────────────────────────────────
    # ফ্ল্যাট টুইন-অ্যান্ড-আর্থ, BS 6004, 6 বর্গমিমি — সাতটি খেই গোনা যায়
    "ph_te":         ("'Twin and Earth' electrical cable. BS 6004, 6mm².jpg",
                      (1135, 1223), (0.0, 0.0, 1.0, 0.92), 1100, 1.06),
    # ক্লাস ৫ — এত সরু খেই যে গোনা যায় না, হাতে নরম
    "ph_flex":       ("Kupferlitze.jpg",
                      (1064, 1467), (0.10, 0.0, 1.0, 1.0), 900, 1.08),
    # অ্যালুমিনিয়াম ৪-কোর, সেক্টর আকৃতি (`se`) — মাটির নিচের ক্যাবল
    "ph_sector":     ("Kabel-alu-4adrig hg.jpg",
                      (1015, 1015), (0.02, 0.02, 0.98, 0.98), 1000, 1.06),

    # ── রঙের কোড ───────────────────────────────────────────────────────
    # পাঁচ কোর, প্রতিটির গায়ে L1/L2/L3/N/PE ফেরুল বসানো
    "ph_colors":     ("Europe color codes.JPG",
                      (3648, 2736), (0.0, 0.02, 1.0, 0.95), 1600, 1.08),

    # ── টার্মিনেশন ও বিপদ ──────────────────────────────────────────────
    # 70 বর্গমিমি M10 ক্যাবল লাগ, নিচে মিলিমিটার কাগজ
    "ph_lug":        ("70mm² M10 terminals.JPG",
                      (3648, 2736), (0.09, 0.05, 0.93, 0.95), 1300, 1.08),
    # পুড়ে কালো হয়ে যাওয়া কন্ডাক্টর ও ফেরুল — আলগা জোড়া বা ছোট ক্যাবল
    "ph_burn":       ("Burnt wire ferrule.jpg",
                      (4519, 2246), (0.065, 0.14, 1.0, 0.72), 1600, 1.05),
}

# CC BY ও CC BY-SA — কৃতজ্ঞতা স্বীকার আইনি শর্ত, ইচ্ছাধীন নয়।
CREDITS = {
    "ph_print":      {"title": "600 V CV ক্যাবল, 5.5 বর্গমিমি (গায়ের লেখা)",
                      "author": "Chatama", "licence": "CC BY-SA 3.0"},
    "ph_print_face": {"title": "600 V CV ক্যাবল, 5.5 বর্গমিমি (লেখার ক্লোজ-আপ)",
                      "author": "Chatama", "licence": "CC BY-SA 3.0"},
    "ph_xsec":       {"title": "Cross section of an older US power cable",
                      "author": "TubeTimeUS", "licence": "CC BY-SA 4.0"},
    "ph_sheath":     {"title": "Installation Cable MMJ 3×2.5S",
                      "author": "Santeri Viinamäki", "licence": "CC BY-SA 4.0"},
    "ph_solid":      {"title": "Installation Cable MMJ 3×2.5S (কন্ডাক্টর)",
                      "author": "Santeri Viinamäki", "licence": "CC BY-SA 4.0"},
    "ph_te":         {"title": "'Twin and Earth' cable, BS 6004, 6 বর্গমিমি",
                      "author": "Alistair1978", "licence": "CC BY-SA 4.0"},
    "ph_flex":       {"title": "Kupferlitze (ফ্লেক্সিবল কন্ডাক্টর)",
                      "author": "Stefan Riepl (Quark48)",
                      "licence": "CC BY-SA 3.0"},
    "ph_sector":     {"title": "অ্যালুমিনিয়াম ৪-কোর ক্যাবল, সেক্টর কন্ডাক্টর",
                      "author": "Hannes Grobe", "licence": "CC BY 3.0"},
    "ph_colors":     {"title": "Europe color codes (কোরের রঙ)",
                      "author": "Dmitry G", "licence": "CC BY-SA 3.0"},
    "ph_lug":        {"title": "70 বর্গমিমি M10 ক্যাবল লাগ",
                      "author": "Dmitry G", "licence": "CC BY-SA 3.0"},
    "ph_burn":       {"title": "Burnt wire ferrule (পোড়া কন্ডাক্টর)",
                      "author": "Phiarc", "licence": "CC BY-SA 4.0"},
}

# ── ইনস্টিটিউটের ক্যাটালগ থেকে টাইপ-নির্দেশক ব্লক ──────────────────────
# (পাতা নম্বর, ক্রপ-বক্স ভগ্নাংশে, সর্বোচ্চ চওড়া)
# ক্যাটালগের পাতা ২ = BYA/BAYA, ৩ = BYFY/BAYFY, ৪ = ফ্লেক্সিবল।
# পাতার লেখা তুলে যাচাই করা যায় না (স্ক্যান করা ছবি), তাই ক্রপের পর
# চোখে দেখে মিলিয়ে নেওয়া হয়েছে — এবং পাতার সংখ্যাটা এখানেই assert করা।
CATCROPS = {
    "cat_bya":  (2, (0.070, 0.138, 0.292, 0.252), 900),
    "cat_byfy": (3, (0.070, 0.138, 0.292, 0.252), 900),
    "cat_flex": (4, (0.070, 0.138, 0.292, 0.252), 900),
}


# ── সাধারণ কাজ ─────────────────────────────────────────────────────────
def _curl(url, timeout=240, least=2048):
    """urllib দিয়ে বারবার হিট করলে কমন্স ৪২৯ ফেরায়; curl-এ ঝামেলা কম।"""
    r = subprocess.run(["curl", "-sL", "-A", UA, "--max-time", str(timeout),
                        url], capture_output=True)
    if len(r.stdout) < least:
        raise SystemExit(f"✗ নামানো গেল না: {url}")
    return r.stdout


def commons_url(fname):
    """কমন্সের ফাইলনাম → আসল ছবির URL।  ফল ক্যাশে রাখা হয়।"""
    cache = os.path.join(CACHE, "ch23_urls.json")
    urls = json.load(open(cache)) if os.path.exists(cache) else {}
    if fname not in urls:
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "titles": "File:" + fname,
            "prop": "imageinfo", "iiprop": "url"})
        d = json.loads(_curl(API + "?" + q, 90, least=64))
        page = next(iter(d["query"]["pages"].values()))
        if "imageinfo" not in page:
            raise SystemExit(f"✗ কমন্সে পাওয়া গেল না: {fname}")
        urls[fname] = page["imageinfo"][0]["url"]
        json.dump(urls, open(cache, "w"), ensure_ascii=False, indent=1)
        time.sleep(2)
    return urls[fname]


def fetch(fname):
    """ডাউনলোড করে ক্যাশে রাখা — বারবার কমন্সে হিট করলে ৪২৯ আসে।"""
    fn = os.path.join(CACHE, "ch23_" + fname.replace(" ", "_")
                      .replace("/", "_"))
    if not os.path.exists(fn) or os.path.getsize(fn) < 4096:
        open(fn, "wb").write(_curl(commons_url(fname)))
        time.sleep(3)
    return open(fn, "rb").read()


def flatten(im):
    """RGBA → সাদার উপরে বসানো RGB।  না করলে ছাপায় কালো আসে (অধ্যায় ১৮)।"""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        return Image.alpha_composite(bg, im).convert("RGB")
    return im.convert("RGB")


def frac_crop(im, box):
    w, h = im.size
    return im.crop((int(w * box[0]), int(h * box[1]),
                    int(w * box[2]), int(h * box[3])))


def save(im, name, wmax, contrast):
    if im.width > wmax:
        im = im.resize((wmax, round(im.height * wmax / im.width)),
                       Image.LANCZOS)
    if contrast != 1.0:
        im = ImageEnhance.Contrast(im).enhance(contrast)
    im.save(os.path.join(OUT, name + ".jpg"), quality=93)
    return im


def do_photos():
    for name, (fname, size, box, wmax, contrast) in PHOTOS.items():
        # EXIF-এর ওরিয়েন্টেশন আগে মেলানো — কমন্সের সাইটে ছবিটি যেভাবে
        # দেখায়, ক্রপ-বক্সও সেই হিসাবেই লেখা (অধ্যায় ১৯-এর শিক্ষা)
        im = flatten(ImageOps.exif_transpose(Image.open(io.BytesIO(
            fetch(fname)))))
        if im.size != size:
            raise SystemExit(f"✗ {name}: {fname}-এর মাপ {im.size}, "
                             f"হওয়ার কথা {size} — কমন্সে ছবিটি বদলেছে, "
                             f"ক্রপ-বক্স আবার মিলিয়ে নিতে হবে")
        out = save(frac_crop(im, box), name, wmax, contrast)
        print("✓", name, out.size, f"({fname})")


def do_catalog():
    """সুপার স্টারের ক্যাটালগ থেকে টাইপ-নির্দেশক ব্লক কেটে নেওয়া।"""
    import pymupdf
    if not os.path.exists(CATALOG):
        raise SystemExit(f"✗ ক্যাটালগ পাওয়া গেল না: {CATALOG}")
    doc = pymupdf.open(CATALOG)
    if doc.page_count != 7:
        raise SystemExit(f"✗ ক্যাটালগে {doc.page_count} পাতা, ৭টি হওয়ার কথা "
                         f"— ফাইলটি বদলেছে, ক্রপ-বক্স মিলিয়ে নিতে হবে")
    for name, (pno, box, wmax) in CATCROPS.items():
        pix = doc[pno - 1].get_pixmap(dpi=330)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        out = save(frac_crop(im, box), name, wmax, 1.05)
        print("✓", name, out.size, f"(ক্যাটালগ পাতা {pno})")


if __name__ == "__main__":
    do_photos()
    do_catalog()
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json লেখা হলো")
