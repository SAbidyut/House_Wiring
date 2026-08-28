# -*- coding: utf-8 -*-
"""অধ্যায় ১১-এর ছবি প্রস্তুত করা।

সব ছবি উইকিমিডিয়া কমন্স থেকে, CC লাইসেন্সে — কৃতজ্ঞতাসহ।

**John M. Sharp, *Practical Electric Wiring* (১৯১৬)-এর প্লেটগুলো বাদ
দেওয়া হয়েছে (২০২৬-০৮-২৫)।**  পাবলিক ডোমেইন ছিল, কিন্তু ১০০ বছরের পুরনো
হাফটোনের রেখা এত সরু যে ১৫.৪ সেমিতে ছাপালে জয়েন্টের প্যাঁচ বোঝা যেত না;
স্কিনিংয়ের 'সঠিক' আর 'ভুল' ছবিদুটো তো একই রকম দেখাত।  জয়েন্ট এখন
`dia_ch11.py`-তে ভেক্টরে আঁকা, আর তার পাশে নিচের আসল আলোকচিত্র।

**জয়েন্টের ঘোলা তিনটি আলোকচিত্র বাদ দেওয়া হয়েছে (২০২৬-০৮-২৫, দ্বিতীয়
পর্যালোচনা)।**  Abuz Mordecai-র তিনটি ছবি — ওয়েস্টার্ন ইউনিয়ন, টি ও
ব্রিটানিয়া — মোবাইলে, ফোকাসের বাইরে তোলা।  মূল ফাইল ২০৪৮×১৫৩৬ হলেও
ছবিগুলো নিজেই ঝাপসা, কাজেই শার্পেনিং করে কিছু হয় না:  আনশার্প মাস্ক
ঝাপসা ছবির প্রান্ত ফেরায় না, কেবল নয়েজটাকেই ধারালো করে (প্রথম চেষ্টায়
ঠিক তা-ই হয়েছিল)।  ছাপা বইয়ে ঘোলা ছবির চেয়ে নিখুঁত আঁকা ছবি ভালো —
জয়েন্টগুলো এখন `dia_ch11.py`-তে ত্রিমাত্রিক হেলিক্স হিসাবে আঁকা,
প্রতিটি পাক গোনা যায়।

**যে খোঁজ আর করার দরকার নেই।**  মুক্ত লাইসেন্সে বৈদ্যুতিক তারের
জয়েন্টের ঝকঝকে আলোকচিত্র নেই — কমন্সে `Category:Splices` (ওটা দড়ির),
`Category:Soldering`, `Category:Electrical wiring`-এর প্রতিটি ফাইল,
`splice`/`joint`/`empalme`/`emenda`/`Spleiß`-সহ এক ডজন ভাষার সার্চ,
Openverse ও archive.org-এর ১৮৯০–১৯৩০-এর ওয়্যারিং বই — সব দেখা হয়েছে।
দ্বিতীয়বার আরও পনেরোটি সার্চ-শব্দ ও পাঁচটি ক্যাটাগরি মিলিয়ে ৩৩৩টি
ফাইলের তালিকা বানিয়ে মাপ-অনুযায়ী দেখা হয়েছে;  যা পাওয়া গেছে তা হয়
দড়ির স্প্লাইস, নয় RNA স্প্লাইসিং।  প্রতিষ্ঠানের নিজের
`Electrical House Wiring book.docx`-এ জয়েন্টের সাতটি **ছবি** আছে
(image58–image64), কিন্তু সেগুলো আলোকচিত্র নয় — ক্লিপ-আর্ট অঙ্কন, আর
সবচেয়ে বড়টিও ১১৪৮ px।  ওগুলো এই অধ্যায়ের আঁকার **রেফারেন্স** হিসেবে
কাজে লেগেছে (বিশেষত ব্রিটানিয়া ও ডুপ্লেক্স), বসানো হয়নি।

যে দুটি জয়েন্টের ছবি **ঝকঝকে**, সে দুটি আছে — Dmitry G-র জংশন-বক্সের
৭৩০০×১০৯৬০ ছবির দুই সেল (পিগটেল ও তার উপর কানেক্টর ক্যাপ)।

কপিরাইটযুক্ত ছবি (গুগল/বিক্রেতার প্রোডাক্ট শট) ইচ্ছা করেই নেওয়া হয়নি —
বইটি প্রতিষ্ঠান ছাপাবে, আর বাকি প্রতিটি ছবি হয় প্রতিষ্ঠানের নিজের, নয়তো
কৃতজ্ঞতাসহ CC।  একটাই ছবি অন্য নিয়মে বসালে পুরো বইয়ের ভিত্তি নড়ে যায়।
"""
import os, io, json, subprocess, time, urllib.parse, urllib.request
import pymupdf
from PIL import Image, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "ch11")
PDF = os.path.join(HERE, ".sharp1916.pdf")     # ~7.6 MB, ডাউনলোড করে রাখা হয়
BOOK_URL = ("https://archive.org/download/practicalelectr00shargoog/"
            "practicalelectr00shargoog.pdf")
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "rapti-book/1.0 (textbook figure prep)"}

# ── জয়েন্টের আসল আলোকচিত্র — কমন্স ─────────────────────────────────────
# নাম → (কমন্সের ফাইলনাম, প্রত্যাশিত মাপ, ঘোরানোর কোণ°,
#         ক্রপ-বক্স ভগ্নাংশে, চওড়া, ঝাপসা-সারাই লাগবে কি না)
#
# মাপটা পাহারাদার (অধ্যায় ২৩-এর নিয়ম):  কমন্সে ছবি বদলালে ক্রপ-বক্স আর
# মিলবে না — তখন এখানেই ধরা পড়বে, ছাপার পর নয়।
JOINT_PHOTOS = {
    # পিগটেল — জংশন বক্সে তিনটি জোড়া পাকানো (ধারাবাহিক ছবির ৪র্থ সেল)
    "ph_pig_real":  ("Junction box with wire nuts.JPG", (7300, 10960), 0,
                     (0.575, 0.250, 0.860, 0.360), 1500, False),
    # ওই তিন জোড়ার উপরেই কানেক্টর ক্যাপ (৬ষ্ঠ সেল)
    "ph_pig_nut":   ("Junction box with wire nuts.JPG", (7300, 10960), 0,
                     (0.641, 0.503, 0.851, 0.585), 1400, False),
}

API = "https://commons.wikimedia.org/w/api.php"
CACHE = os.path.join(HERE, ".commons_ch11")


def _curl(url, least=2048):
    """urllib দিয়ে বারবার হিট করলে কমন্স ৪২৯ ফেরায়; curl-এ ঝামেলা কম।"""
    r = subprocess.run(["curl", "-sL", "-A", UA["User-Agent"],
                        "--max-time", "240", url], capture_output=True)
    if len(r.stdout) < least:
        raise SystemExit(f"✗ নামানো গেল না: {url}")
    return r.stdout


def commons_fetch(fname):
    """কমন্সের ফাইলনাম → মূল ছবি, ক্যাশেসহ।"""
    os.makedirs(CACHE, exist_ok=True)
    fn = os.path.join(CACHE, fname.replace(" ", "_").replace("/", "_"))
    if not os.path.exists(fn) or os.path.getsize(fn) < 4096:
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "titles": "File:" + fname,
            "prop": "imageinfo", "iiprop": "url|size", "iiurlwidth": "2600"})
        d = json.loads(_curl(API + "?" + q, 64))
        page = next(iter(d["query"]["pages"].values()))
        if "imageinfo" not in page:
            raise SystemExit(f"✗ কমন্সে পাওয়া গেল না: {fname}")
        ii = page["imageinfo"][0]
        open(fn, "wb").write(_curl(ii.get("thumburl") or ii["url"]))
        time.sleep(3)
    return Image.open(fn).convert("RGB")


def commons_size(fname):
    """মূল ফাইলের পিক্সেল-মাপ — ক্রপ-বক্সের পাহারাদার।"""
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "titles": "File:" + fname,
        "prop": "imageinfo", "iiprop": "size"})
    d = json.loads(_curl(API + "?" + q, 64))
    ii = next(iter(d["query"]["pages"].values()))["imageinfo"][0]
    return ii["width"], ii["height"]


def unblur(im):
    """মোবাইলে তোলা ঘোলা ছবিকে ছাপার যোগ্য করা।

    ক্রোমা-নয়েজ আগে মুছতে হয় — না মুছে আনশার্প দিলে নয়েজটাই ধারালো
    হয়ে ওঠে (প্রথম চেষ্টায় ঠিক তা-ই হয়েছিল)।"""
    y, cb, cr = im.convert("YCbCr").split()
    cb = cb.filter(ImageFilter.GaussianBlur(7))
    cr = cr.filter(ImageFilter.GaussianBlur(7))
    im = Image.merge("YCbCr", (y, cb, cr)).convert("RGB")
    im = im.filter(ImageFilter.MedianFilter(3))
    im = im.filter(ImageFilter.UnsharpMask(radius=8, percent=120, threshold=4))
    im = _levels(im)
    im = ImageEnhance.Contrast(im).enhance(1.16)
    return ImageEnhance.Color(im).enhance(1.22)


def _levels(im, lo=0.02, hi=0.995):
    """হিস্টোগ্রাম টেনে সাদাকে সাদা, কালোকে কালো করা।

    তিনটি ছবিই কম আলোয় তোলা;  একটিতে (`ph_wu_real`) কাগজ ধূসর হয়ে
    থাকায় ছাপায় পুরো ছবিটা ফ্যাকাশে দেখাত।"""
    g = im.convert("L").histogram()
    tot = sum(g)
    acc, blk, wht = 0, 0, 255
    for i, v in enumerate(g):
        acc += v
        if acc <= tot * lo:
            blk = i
        if acc <= tot * hi:
            wht = i
    if wht - blk < 40:
        return im
    lut = [max(0, min(255, round((i - blk) * 255 / (wht - blk))))
           for i in range(256)] * 3
    return im.point(lut)


def do_joint_photos():
    for name, (fname, exp, rot, box, wmax, fix) in JOINT_PHOTOS.items():
        got = commons_size(fname)
        assert got == exp, f"{fname}: কমন্সে মাপ বদলেছে {got} ≠ {exp}"
        im = commons_fetch(fname)
        if rot:
            # ঘোরানোর পর কোণে যে ফাঁকা ত্রিভুজ পড়ে, সেটি সাদা রাখলে
            # ছবিতে কাটা দাগের মতো দেখায় — ছবির নিজের কাগজের রং বসানো
            im = im.rotate(rot, resample=Image.BICUBIC, expand=True,
                           fillcolor=(168, 172, 175))
        w, h = im.size
        im = im.crop((int(w * box[0]), int(h * box[1]),
                      int(w * box[2]), int(h * box[3])))
        if im.width > wmax:
            im = im.resize((wmax, round(im.height * wmax / im.width)),
                           Image.LANCZOS)
        if fix:
            im = unblur(im)
        im.save(os.path.join(OUT, name + ".jpg"), quality=93)
        print("✓", name, im.size)


PHOTOS = {
    # নাম: (URL, ক্রপ-বক্স ভগ্নাংশে বা None, সর্বোচ্চ চওড়া)
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
        dst = os.path.join(OUT, name + ".jpg")
        if os.path.exists(dst) and os.path.getsize(dst) > 4096:
            print("·", name, "(আগেই আছে)")
            continue          # বারবার হিট করলে কমন্স ৪২৯ ফেরায়
        raw = _curl(url)
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
    "ph_pig_real": {
        "source": "Wikimedia Commons — 'Junction box with wire nuts', Dmitry G",
        "licence": "CC BY-SA 3.0",
    },
    "ph_pig_nut": {
        "source": "Wikimedia Commons — 'Junction box with wire nuts', Dmitry G",
        "licence": "CC BY-SA 3.0",
    },
}

if __name__ == "__main__":
    do_photos()
    do_joint_photos()
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json written")
