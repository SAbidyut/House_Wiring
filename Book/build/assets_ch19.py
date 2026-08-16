# -*- coding: utf-8 -*-
"""অধ্যায় ১৯-এর ছবি প্রস্তুত করা।

এই অধ্যায়ের জন্য ইনস্টিটিউটের রুটে কোনো উৎস নেই — `Electrical House Wiring
book.docx`-এ আইপিএস বা ইউপিএসের একটিও অনুচ্ছেদ নেই, আর `HW Connection
Diagram All.pptx` ও `Circuit Diagram.pptx` — দুই ডেকের প্রতিটি স্লাইডের
লেখা বের করে দেখা হয়েছে, আইপিএসের কোনো স্লাইড নেই।  `Solar System.docx`-এ
শুধু অফ-গ্রিড সোলারের ব্যাটারি-ইনভার্টার হিসাব আছে, যন্ত্রের ছবি নেই।

তাই সব আলোকচিত্র উইকিমিডিয়া কমন্স থেকে — লাইসেন্স ও আলোকচিত্রীর নাম
`credits.json`-এ, আর অধ্যায়ের শেষে ❖ চিত্রসূত্র বাক্সে (CC BY / CC BY-SA
ছবির জন্য কৃতজ্ঞতা স্বীকার আইনি শর্ত, ইচ্ছাধীন নয়)।

যেগুলো বেছে নেওয়া হয়েছে, সবগুলোই আসল লেখা পড়া যায় এমন — এই অধ্যায়ের
মূল কথাই তো "গায়ের লেখা পড়তে শেখা":

  ph_ups_rear   Scott Power SDL 500 — Output 220-240V~ 50Hz, 300W, 500VA
                আর Input 3.0 A, Fuse T 3.15 A।  300 W ÷ 500 VA = ০.৬ —
                পাওয়ার ফ্যাক্টরের পুরো পাঠটা এই এক ছবিতে।
  ph_ups_rear2  APC Back-UPS RS 500 — কোন সকেট ব্যাটারি-ব্যাকআপে আর কোনটা
                শুধু সার্জ, সঙ্গে "Circuit Breaker — Push to Reset"।
  ph_batt_label RITAR RT1245 — 12V 4.5AH/20HR, সাইকেল ১৪.৬–১৪.৮ V,
                স্ট্যান্ডবাই ১৩.৭–১৩.৯ V, ইনিশিয়াল কারেন্ট ১.৩৫ A।
  ph_scope      সত্যিকারের অসিলোস্কোপে মডিফাইড সাইন (হলুদ) বনাম মেইনের
                সাইন (বেগুনি)।  মাপাটা ৬০ Hz সিস্টেমে — ক্যাপশনে বলা আছে।

`ph_home_ips` ছবিটা ধোঁয়াটে (ঘরের ভেতর, ফ্ল্যাশ ছাড়া) — কনট্রাস্ট একটু
টেনে দেওয়া হয়েছে, নইলে ছাপায় ব্যাটারির লেখা মরে যায়।

চালানোর নিয়ম:  python assets_ch19.py     (Book/build/ থেকে)
"""
import io
import json
import os
import time
import urllib.parse
import urllib.request

from PIL import Image, ImageEnhance, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "ch19")
CACHE = os.path.join(HERE, ".slidepdf")          # ডাউনলোডের ক্যাশে
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

UA = {"User-Agent": "rapti-book/1.0 (textbook figure prep)"}
API = "https://commons.wikimedia.org/w/api.php"

# নাম → (কমন্সের ফাইলনাম, প্রত্যাশিত মাপ, ক্রপ-বক্স ভগ্নাংশে বা None,
#         সর্বোচ্চ চওড়া, কনট্রাস্ট)
# মাপটা পাহারাদার — কমন্সে ছবি বদলালে বা নতুন সংস্করণ উঠলে এখানেই ধরা পড়ে।
PHOTOS = {
    # ── যন্ত্র ────────────────────────────────────────────────────────
    # বাসাবাড়ির আইপিএস: দুটি ইউনিট, নিচে দুটি টল টিউবুলার ব্যাটারি,
    # উপরে ভেন্ট ক্যাপ — উপমহাদেশের ঘরে ঠিক যেমনটা বসে।
    "ph_home_ips":    ("Inverter & Battery- The power cut fighter.jpg",
                       (4000, 3000), (0.015, 0.02, 0.995, 0.985), 2000, 1.22),
    # ওই ছবিরই বাঁ দিকের ব্যাটারি — ছয়টি সেলের ভেন্ট প্লাগ গোনা যায়
    "ph_tubular":     ("Inverter & Battery- The power cut fighter.jpg",
                       (4000, 3000), (0.085, 0.30, 0.50, 0.90), 1200, 1.28),
    # ডেস্কের ইউপিএস — ছয়টি সকেট, কয়েকটি ব্যাকআপে, কয়েকটি শুধু সার্জে
    "ph_ups_desk":    ("APC Back-UPS ES525.jpg",
                       (3264, 2448), (0.03, 0.24, 0.99, 0.93), 1500, 1.06),
    # টাওয়ার ইউপিএস — ফাইলটি কাত করে তোলা, EXIF ঘুরিয়ে সোজা করা হয়
    "ph_ups_tower":   ("Uninterruptible power supply.jpg",
                       (1152, 2048), (0.08, 0.10, 0.94, 0.99), 900, 1.10),
    # বড় অনলাইন ইউপিএস — ডেটা সেন্টারের ঘর
    "ph_ups_big":     ("MGE Uninterruptible Power Supply at NERSC.jpg",
                       (3361, 2240), (0.10, 0.04, 0.92, 0.97), 1500, 1.05),

    # ── গায়ের লেখা ───────────────────────────────────────────────────
    "ph_ups_rear":    ("UPSRearView.jpg",
                       (913, 1621), (0.055, 0.235, 0.955, 0.95), 1100, 1.15),
    "ph_ups_rear2":   ("Apc ups rs500 04.jpg",
                       (1010, 1819), (0.13, 0.28, 0.97, 0.95), 1100, 1.06),
    "ph_leds":        ("Apc ups rs500 01.jpg",
                       (860, 1471), (0.23, 0.355, 0.87, 0.795), 1100, 1.10),
    "ph_batt_label":  ("12V VRLA Battery.jpg",
                       (1024, 768), (0.15, 0.07, 0.82, 0.99), 1300, 1.12),

    # ── ব্যাটারি ও রক্ষণাবেক্ষণ ─────────────────────────────────────
    # SMF/AGM ব্লক ব্যাটারি — 12 V, 100 Ah
    "ph_batt_smf":    ("VRLA Valve-Regulated-Lead-Acid-Batteries 82645.jpg",
                       (4752, 3168), (0.13, 0.16, 0.90, 0.90), 1300, 1.05),
    # ইউপিএসের ভেতরের ছোট SLA ব্যাটারি, ড্রয়ার টেনে বের করা
    "ph_batt_drawer": ("Apc ups rs500 09.jpg",
                       (2532, 1656), (0.05, 0.06, 0.97, 0.94), 1400, 1.08),

    # ── তরঙ্গ ─────────────────────────────────────────────────────────
    # হলুদ = ইউপিএসের আউটপুট (ধাপে-ধাপে), বেগুনি = মেইনের সাইন
    "ph_scope":       ("APC Back-UPS 550 Uninterruptible Power Supply "
                       "Output Waveform.jpg",
                       (1600, 960), (0.008, 0.062, 0.886, 0.872), 1500, 1.0),
}


def commons_url(fname):
    """কমন্সের ফাইলনাম → আসল ছবির URL।  ফল ক্যাশে রাখা হয়।"""
    cache = os.path.join(CACHE, "ch19_urls.json")
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
        time.sleep(1.5)
    return urls[fname]


def fetch(fname):
    """ডাউনলোড করে ক্যাশে রাখা — বারবার কমন্সে হিট করলে ৪২৯ আসে।"""
    fn = os.path.join(CACHE, "ch19_" + fname.replace(" ", "_")
                      .replace("&", "and"))
    if not os.path.exists(fn) or os.path.getsize(fn) < 4096:
        url = commons_url(fname)
        for attempt in range(5):
            try:
                raw = urllib.request.urlopen(
                    urllib.request.Request(url, headers=UA), timeout=300).read()
                open(fn, "wb").write(raw)
                break
            except Exception as exc:                       # ৪২৯ হলে থেমে যাই
                print("   … আবার চেষ্টা:", exc)
                time.sleep(10)
        else:
            raise SystemExit(f"✗ নামানো গেল না: {fname}")
        time.sleep(2)
    return open(fn, "rb").read()


def build():
    for name, (fname, size, box, wmax, contrast) in PHOTOS.items():
        # EXIF-এর ওরিয়েন্টেশন আগে মেলানো — কমন্সের ওয়েবসাইটে ছবিটি যেভাবে
        # দেখায়, ক্রপ-বক্সও সেই হিসাবেই লেখা
        im = ImageOps.exif_transpose(
            Image.open(io.BytesIO(fetch(fname)))).convert("RGB")
        if im.size != size:
            raise SystemExit(f"✗ {name}: {fname}-এর মাপ {im.size}, "
                             f"হওয়ার কথা {size} — কমন্সে ছবিটি বদলেছে, "
                             f"ক্রপ-বক্স আবার মিলিয়ে নিতে হবে")
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


# CC BY ও CC BY-SA — কৃতজ্ঞতা স্বীকার বাধ্যতামূলক।  অধ্যায়ের শেষের
# ❖ চিত্রসূত্র বাক্সটি `ch19.py` এখান থেকেই পড়ে বানায় না — হাতে লেখা,
# কিন্তু দুটো যেন এক থাকে সেজন্য এখানে পুরোটা তোলা রইল।
CREDITS = {
    "ph_home_ips": {
        "files": ["ph_home_ips", "ph_tubular"],
        "title": "Inverter & Battery — The power cut fighter",
        "author": "Deepanshu.sr9", "licence": "CC BY-SA 4.0"},
    "ph_ups_desk": {
        "title": "APC Back-UPS ES525",
        "author": "MSDN.WhiteKnight", "licence": "CC0 (পাবলিক ডোমেইন)"},
    "ph_ups_tower": {
        "title": "Uninterruptible power supply",
        "author": "Tahir mq", "licence": "CC BY-SA 4.0"},
    "ph_ups_big": {
        "title": "MGE Uninterruptible Power Supply at NERSC",
        "author": "Derrick Coetzee", "licence": "CC0 (পাবলিক ডোমেইন)"},
    "ph_ups_rear": {
        "title": "UPSRearView (Scott Power SDL 500)",
        "author": "Amakuru", "licence": "CC BY-SA 3.0"},
    "ph_ups_rear2": {
        "files": ["ph_ups_rear2", "ph_leds", "ph_batt_drawer"],
        "title": "APC Back-UPS RS 500 (BR500I) — ছবি ০১, ০৪, ০৯",
        "author": "Hundehalter", "licence": "CC BY-SA 3.0"},
    "ph_batt_label": {
        "title": "12V VRLA Battery (RITAR RT1245)",
        "author": "Dudinyúl", "licence": "CC BY-SA 3.0"},
    "ph_batt_smf": {
        "title": "VRLA Valve-Regulated Lead-Acid Batteries (DB12-100)",
        "author": "Emilian Robert Vicol", "licence": "CC BY 2.0"},
    "ph_scope": {
        "title": "APC Back-UPS 550 Uninterruptible Power Supply Output "
                 "Waveform",
        "author": "Timothy Quill", "licence": "CC BY-SA 4.0"},
}

if __name__ == "__main__":
    build()
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json লেখা হলো")
