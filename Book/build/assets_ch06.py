# -*- coding: utf-8 -*-
"""অধ্যায় ০৬-এর আলোকচিত্র প্রস্তুত করা।

ইনস্টিটিউটের নিজের কোনো ফাইলে বেলের ছবি নেই।  `Electrical House Wiring
book.docx`-এর ২১০টি ছবির মধ্যে বেল-সম্পর্কিত যা আছে তা কেবল **বেল পুশ
সুইচ** (image70) আর **গ্যাং পুশ বেল সুইচ** (image82) — যন্ত্রটার ছবি নেই।
`HW Connection Diagram All.pptx` ও `Circuit Diagram.pptx` — দুই ডেকেই বেলের
সার্কিট আছে (অধ্যায় ৬-এর d03–d07 সেগুলোই), কিন্তু যন্ত্রের আলোকচিত্র নেই।

তাই ছয়টি ছবিই উইকিমিডিয়া কমন্স থেকে।  লাইসেন্স ও আলোকচিত্রীর নাম
`credits.json`-এ, আর অধ্যায়ের শেষে ❖ চিত্রসূত্র বাক্সে — CC BY / CC BY-SA
ছবির কৃতজ্ঞতা স্বীকার আইনি শর্ত, ইচ্ছাধীন নয়।

কোনটা কেন বাছা হয়েছে:

  ph_bell_open  DoorBell 001 — ঢাকনা খোলা একটা ট্রেম্বলিং বেল।  দুটো
                কয়েল, তার উপরে আর্মেচার, বাঁ দিকে ঝালরকাটা কন্টাক্ট স্ক্রু,
                ডান দিকে হ্যামারের বল আর গং — চিত্র ৬.১-এর আঁকা ছবির
                প্রতিটি অংশ এখানে আসল বস্তুতে দেখা যায়।  এই একটা ছবির
                জন্যই কমন্স ঘাঁটা সার্থক।
  ph_bell_gong  সোভিয়েত গোল গং বেল — বাংলাদেশের বাজারে যেটা "কলিং বেল"
                নামে বিক্রি হয়, দেখতে হুবহু এটাই।
  ph_single     Tyer's single stroke block bell — রেলওয়ের ব্লক
                ইনস্ট্রুমেন্টের সঙ্গে চলে।  সিঙ্গেল স্ট্রোক বেলের সত্যিকারের
                ছবি এটাই; কমন্সে আর নেই।
  ph_buzzer     Kingstate KS-3206, 6 V DC — গং নেই, শুধু ঝাঁঝরি।
  ph_chime      ওয়্যারলেস মিউজিক্যাল কলিং বেল — রিসিভার ও রিমোট পুশ,
                একসঙ্গে।  এখনকার বাজারে চাইম বলতে এটাই।
  ph_alarm      Kobishi MSB-63A ফায়ার অ্যালার্ম বেল — বড় গং।

চালানোর নিয়ম:  python assets_ch06.py      (Book/build/ থেকে)
"""
import io
import json
import os
import time
import urllib.parse
import urllib.request

from PIL import Image, ImageEnhance, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "ch06")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

UA = {"User-Agent": "rapti-book/1.0 (textbook figure prep)"}
API = "https://commons.wikimedia.org/w/api.php"

# নাম → (কমন্সের ফাইলনাম, প্রত্যাশিত মাপ, ক্রপ-বক্স ভগ্নাংশে, সর্বোচ্চ চওড়া,
#         কনট্রাস্ট)।  মাপটা পাহারাদার — কমন্সে ছবি বদলালে এখানেই ধরা পড়ে।
PHOTOS = {
    "ph_bell_gong": ("Звонок электрический советский.jpg",
                     (1894, 1992), (0.05, 0.02, 0.97, 0.99), 1100, 1.10),
    "ph_bell_open": ("DoorBell 001.jpg",
                     (2284, 1160), (0.01, 0.01, 0.99, 0.99), 1500, 1.14),
    "ph_single":    ("Block Instruments-2.JPG",
                     (3648, 2432), (0.09, 0.06, 0.80, 0.97), 1300, 1.08),
    "ph_buzzer":    ("KS-3206 6VDC Electronic Buzzer.jpg",
                     (1824, 1368), (0.20, 0.26, 0.72, 0.88), 1000, 1.05),
    "ph_chime":     ("Wireless Call Bell (51948926331).jpg",
                     (2731, 2048), (0.10, 0.16, 0.95, 0.96), 1300, 1.06),
    "ph_alarm":     ("Kobishi Electric MSB-63A fire alarm bell.JPG",
                     (2448, 3264), (0.06, 0.20, 0.99, 0.91), 1200, 1.05),
}

CREDITS = {
    # শিরোনামে বন্ধনী দেওয়া যাবে না — সিরিলিক ও বাংলা মেশানো লাইনে
    # LibreOffice বন্ধনীটাকে লাইনের শুরুতে তুলে আনে
    "ph_bell_gong": {"title": "Звонок электрический советский",
                     "author": "Monoklon", "licence": "CC BY 3.0"},
    "ph_bell_open": {"title": "DoorBell 001",
                     "author": "HNH", "licence": "CC BY-SA 3.0"},
    "ph_single":    {"title": "Block Instruments — Tyer's single stroke "
                              "block bell",
                     "author": "Sir Ross BA", "licence": "CC BY 3.0"},
    "ph_buzzer":    {"title": "KS-3206 6VDC Electronic Buzzer",
                     "author": "Nvtj", "licence": "CC BY-SA 3.0"},
    "ph_chime":     {"title": "Wireless Call Bell",
                     "author": "Dilshan Jayakody", "licence": "CC BY-SA 2.0"},
    "ph_alarm":     {"title": "Kobishi Electric MSB-63A fire alarm bell",
                     "author": "BrokenSphere", "licence": "CC BY-SA 3.0"},
}


def commons_url(fname):
    """কমন্সের ফাইলনাম → আসল ছবির URL।  ফল ক্যাশে রাখা হয়।"""
    cache = os.path.join(CACHE, "ch06_urls.json")
    urls = json.load(open(cache)) if os.path.exists(cache) else {}
    if fname not in urls:
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "titles": "File:" + fname,
            "prop": "imageinfo", "iiprop": "url|extmetadata"})
        d = json.load(urllib.request.urlopen(
            urllib.request.Request(API + "?" + q, headers=UA), timeout=120))
        page = next(iter(d["query"]["pages"].values()))
        if "imageinfo" not in page:
            raise SystemExit(f"✗ কমন্সে পাওয়া গেল না: {fname}")
        urls[fname] = page["imageinfo"][0]["url"]
        json.dump(urls, open(cache, "w"), ensure_ascii=False, indent=1)
        time.sleep(2)
    return urls[fname]


def fetch(fname):
    """ডাউনলোড করে ক্যাশে রাখা — বারবার কমন্সে হিট করলে ৪২৯ আসে।"""
    fn = os.path.join(CACHE, "ch06_" + fname.replace(" ", "_")
                      .replace("&", "and"))
    if not os.path.exists(fn) or os.path.getsize(fn) < 4096:
        url = commons_url(fname)
        for _ in range(6):
            try:
                raw = urllib.request.urlopen(
                    urllib.request.Request(url, headers=UA), timeout=300).read()
                open(fn, "wb").write(raw)
                break
            except Exception as exc:
                print("   … আবার চেষ্টা:", exc)
                time.sleep(15)
        else:
            raise SystemExit(f"✗ নামানো গেল না: {fname}")
        time.sleep(3)
    return open(fn, "rb").read()


def build():
    for name, (fname, size, box, wmax, contrast) in PHOTOS.items():
        # কমন্সের পাতায় ছবিটা যেভাবে দেখায়, ক্রপ-বক্সও সেই হিসাবে লেখা —
        # তাই EXIF-এর ওরিয়েন্টেশন আগে মিলিয়ে নেওয়া
        im = ImageOps.exif_transpose(
            Image.open(io.BytesIO(fetch(fname)))).convert("RGB")
        if im.size != size:
            raise SystemExit(f"✗ {name}: {fname}-এর মাপ {im.size}, হওয়ার কথা "
                             f"{size} — কমন্সে ছবিটি বদলেছে, ক্রপ-বক্স আবার "
                             f"মিলিয়ে নিতে হবে")
        if box:
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


if __name__ == "__main__":
    build()
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("✓ credits.json")
