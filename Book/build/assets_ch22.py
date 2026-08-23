# -*- coding: utf-8 -*-
"""অধ্যায় ২২-এর ছবি প্রস্তুত করা — সার্কিট ব্রেকার ও প্রতিরক্ষামূলক ডিভাইস।

ইনস্টিটিউটের কোনো ফাইলেই ব্রেকারের ব্যবহারযোগ্য আলোকচিত্র নেই।
`circuit breaker.docx` ও `Standard Markings on Circuit Breakers.docx`-এর
ভেতরের ২৭ + ১৪টি ছবি সবই CHiNT-এর ক্যাটালগ-রেন্ডার — কপিরাইটের হিসাব
পরিষ্কার নয়, আর রেন্ডারে গায়ের লেখা পড়াও যায় না।  দুই ডায়াগ্রাম ডেকের
প্রতিটি স্লাইডের লেখা বের করে দেখা হয়েছে — ব্রেকার-নির্দিষ্ট স্লাইড নেই;
২৯/৩১/৩২/৩৩ নম্বরে যা আছে তা বাসবারের ছক, অধ্যায় ২১-এ বসে গেছে।

তাই দশটি আলোকচিত্রই **উইকিমিডিয়া কমন্স** থেকে।  বাছাইয়ের একটাই শর্ত ছিল —
গায়ের লেখা যেন সত্যিই পড়া যায়, কারণ এই অধ্যায়ের আসল পাঠই তো নেমপ্লেট
পড়া।  দুটি ছবি গোটা অধ্যায়টাকে বয়ে নিয়ে যায়:

  ph_rccb + ph_toroid   একই সিমেন্স 5SM1 344-0 RCCB — বাঁয়ে আস্ত গায়ের
      লেখা (In 40A · IΔn 30mA · Un 230/400V · টার্মিনালের ছক · T বোতাম),
      ডাইনে খোলা অবস্থায় ভেতরের টরয়েড কোর, তার ভেতর দিয়ে চারটে তার।
      নীতি আর নেমপ্লেট — দুটোই এক ছবিতে।  (অধ্যায় ১৯-এর UPSRearView-এর
      মতোই।)  একটি ফাইল, দুটি ক্রপ।

বাকিগুলো:  ph_mcb (IEK BA47-29, গায়ে C16 · 400V~ · 4500 · শ্রেণি 3 —
DIN রেলে বসানো), ph_mcb_cut (দুই ফালি করা MCB — আর্ক চুট আর সোলেনয়েড
কয়েল স্পষ্ট), ph_mcb_trans (স্বচ্ছ খোলের MCB), ph_mccb_face ও ph_mccb_trip (মার্লিন
জেরাঁ NS100N — Ui/Uimp/Ue/Icu/Ics-এর গোটা ছক, Ir ডায়াল, Im, TM 40 D),
ph_row (RCCB + বারোটা MCB-র সারি, খালি ওয়েসহ),
ph_db (তারসহ পুরো কনজিউমার ইউনিট — QS1, RCBO, RCCB, MCB)।

কৃতজ্ঞতা স্বীকার আইনি শর্ত (CC BY / CC BY-SA), ইচ্ছাধীন নয় — `ch22.py`
এই স্ক্রিপ্টের লেখা `credits.json` পড়েই শেষের ❖ চিত্রসূত্র বাক্সটি বানায়,
তাই ছবি আর কৃতজ্ঞতা কখনো আলাদা হয়ে যাবে না।

চালানোর নিয়ম:  python assets_ch22.py     (Book/build/ থেকে)
"""
import io
import json
import os
import subprocess
import time
import urllib.parse

from PIL import Image, ImageEnhance, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "ch22")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

UA = "rapti-book/1.0 (textbook figure prep)"
API = "https://commons.wikimedia.org/w/api.php"

# নাম → (কমন্সের ফাইলনাম, প্রত্যাশিত মাপ, ক্রপ-বক্স ভগ্নাংশে,
#         সর্বোচ্চ চওড়া, কনট্রাস্ট)
#
# মাপটা পাহারাদার:  কমন্সে ছবি বদলালে (নতুন সংস্করণ চাপালে) ক্রপ-বক্স
# আর মিলবে না — তখন এখানেই ধরা পড়বে, ছাপার পর নয়।
PHOTOS = {
    # ── MCB ────────────────────────────────────────────────────────────
    # IEK BA47-29, 2P, C16।  গায়ের লেখা বড় ও পরিষ্কার — C16, 400V~,
    # চৌকো ঘরে 4500 (Icn) আর 3 (শক্তি-সীমাবদ্ধতার শ্রেণি), পাশে
    # টার্মিনালের ছক 1-3 / 2-4।  দুই পাশে DIN রেলের খানিকটা রাখা হয়েছে।
    "ph_mcb":       ("Circuit breaker 2 pole on DIN rail.JPG",
                     (2160, 2312), (0.16, 0.05, 0.86, 0.97), 1500, 1.05),

    # দুই ফালি করা MCB — ডান ফালিতে আর্ক চুটের ধাতব পাত আর সোলেনয়েড
    # কয়েল, বাঁ ফালিতে হ্যান্ডেল ও ল্যাচ।
    "ph_mcb_cut":   ("Wyłącznik instalacyjny w przekroju - grudzień 2021.jpg",
                     (4160, 3120), (0.06, 0.07, 0.94, 0.92), 1600, 1.08),

    # স্বচ্ছ খোলের MCB — গোটা যন্ত্রটা জোড়া অবস্থায় দেখা যায়
    "ph_mcb_trans": ("Leitungsschutzschalter transparent.JPG",
                     (2048, 1536), (0.08, 0.05, 0.92, 0.90), 1400, 1.06),

    # ── MCCB ───────────────────────────────────────────────────────────
    # মার্লিন জেরাঁ Compact NS100N — এই অধ্যায়ের সবচেয়ে সমৃদ্ধ নেমপ্লেট

    # ── RCCB ───────────────────────────────────────────────────────────
    # একই ছবি, দুটি ক্রপ — বাঁ পাশে গায়ের লেখা, ডান পাশে ভেতরের টরয়েড
    "ph_rccb":      ("Siemens I=40A ΔI=30mA RCD.JPG",
                     (3648, 2056), (0.095, 0.06, 0.475, 0.93), 1200, 1.12),
    "ph_toroid":    ("Siemens I=40A ΔI=30mA RCD.JPG",
                     (3648, 2056), (0.525, 0.04, 0.905, 0.95), 1200, 1.08),

    # ── ডিবি ───────────────────────────────────────────────────────────
    # RCCB + বারোটি MCB-র সারি, উপরে সার্কিটের নাম আর একটি খালি ওয়ে
    "ph_row":       ("RCCB and Miniature Circuit Breaker..jpg",
                     (3264, 2448), (0.02, 0.435, 0.99, 0.762), 1700, 1.08),

    # তারসহ পুরো কনজিউমার ইউনিট — QS1 (আইসোলেটর), RCBO ১-২, RC (RCCB),
    # QF1–QF3 (MCB), উপরে নিউট্রাল ও আর্থিং বার
    "ph_db":        ("Fuse box hager.JPG",
                     (4096, 2304), (0.17, 0.02, 0.76, 0.96), 1500, 1.06),

    # ── ব্র্যান্ড-গ্যালারি (§২২.১১) ─────────────────────────────────────
    # এই চারটি ব্র্যান্ডের যন্ত্রই বাংলাদেশের বাজারে মেলে, আর চারটিরই
    # গায়ে একই ছকে একই তথ্য — কার্ভ+রেটিং, চৌকো ঘরে Icn ও শ্রেণি,
    # ভোল্টেজ, IEC 60898-1।  অধ্যায়ের মূল দাবিটা এই চারটে ছবি পাশাপাশি
    # রাখলেই প্রমাণ হয়ে যায়।  বাকি দুটি টাইলে চ্যাপ্টারে আগে থেকেই
    # থাকা ph_rccb (সিমেন্স) ও ph_db (হ্যাগার) ফের ব্যবহার হয়।
    "ph_br_schneider": ("Schneider Electric circuit breakers Acti9 series 02.jpg",
                        (2000, 2297), (0.085, 0.155, 0.40, 0.92), 900, 1.06),
    "ph_br_abb":    ("Miniature Circuit Breaker S203 B16.tiff",
                     (769, 1022), (0.02, 0.01, 0.99, 0.96), 760, 1.04),
    "ph_br_legrand": ("Disjoncteur divisionaire Legrand.jpg",
                      (494, 1168), (0.09, 0.0, 1.0, 1.0), 460, 1.10),
    "ph_br_chint":  ("Chint circuit breakers.JPG",
                     (3648, 2736), (0.325, 0.14, 0.475, 0.79), 700, 1.10),

    # ── গায়ের লেখার ক্লোজ-আপ ───────────────────────────────────────────
    # গোটা যন্ত্রের ছবি ১৫.৪ সেমিতে বসালে ছাপা লেখাটা ৩–৪ পয়েন্টে নেমে
    # আসে — পড়া যায় না।  অথচ এই অধ্যায়ের আসল পাঠই ওই লেখাটুকু।  তাই
    # প্রতিটি যন্ত্রের কেবল লেবেল-অংশটুকু আলাদা করে কাটা হয়েছে; ওটাই
    # কল-আউটওয়ালা নেমপ্লেট-চিত্রে বসে, আর গোটা যন্ত্রের ছবি আলাদা
    # চিত্রে চেনার জন্য থাকে।
    "ph_mcb_face":  ("Circuit breaker 2 pole on DIN rail.JPG",
                     (2160, 2312), (0.35, 0.32, 0.84, 0.61), 1500, 1.06),
    "ph_mccb_face": ("MCCB Merlin Gerin compact NS100N (front side).jpg",
                     (1584, 1894), (0.205, 0.235, 0.455, 0.618), 1200, 1.16),
    "ph_mccb_trip": ("MCCB Merlin Gerin compact NS100N (front side).jpg",
                     (1584, 1894), (0.165, 0.645, 0.875, 0.810), 1400, 1.14),
    "ph_rccb_face": ("Siemens I=40A ΔI=30mA RCD.JPG",
                     (3648, 2056), (0.102, 0.324, 0.373, 0.692), 1300, 1.16),
    "ph_spd_face":  ("Dornbirn-Surge arresters Obo V20-C T2-01ASD.jpg",
                     (4624, 3468), (0.323, 0.320, 0.731, 0.780), 1500, 1.10),
}

# CC BY ও CC BY-SA — কৃতজ্ঞতা স্বীকার আইনি শর্ত, ইচ্ছাধীন নয়।
CREDITS = {
    "ph_mcb":       {"title": "Circuit breaker 2 pole on DIN rail",
                     "author": "Kae", "licence": "CC BY-SA 3.0"},
    "ph_mcb_cut":   {"title": "Wyłącznik instalacyjny w przekroju",
                     "author": "Koefbac", "licence": "CC BY-SA 4.0"},
    "ph_mcb_trans": {"title": "Leitungsschutzschalter transparent",
                     "author": "Cherubino", "licence": "CC BY 3.0"},
    "ph_rccb":      {"title": "Siemens RCCB 40 A, 30 mA (নেমপ্লেট)",
                     "author": "Dmitry G", "licence": "CC BY-SA 3.0"},
    "ph_toroid":    {"title": "Siemens RCCB 40 A, 30 mA (ভেতরের অংশ)",
                     "author": "Dmitry G", "licence": "CC BY-SA 3.0"},
    "ph_row":       {"title": "RCCB and Miniature Circuit Breaker",
                     "author": "Balurbala", "licence": "CC BY-SA 3.0"},
    "ph_db":        {"title": "Fuse box hager",
                     "author": "Dmitry G", "licence": "CC BY-SA 3.0"},
    "ph_br_schneider": {"title": "Schneider Electric Acti9 iC60N",
                        "author": "Zimin.V.G.", "licence": "CC BY-SA 4.0"},
    "ph_br_abb":    {"title": "Miniature Circuit Breaker S203 B16",
                     "author": "ABB ltd", "licence": "CC BY-SA 3.0"},
    "ph_br_legrand": {"title": "Disjoncteur divisionnaire Legrand",
                      "author": "France64160", "licence": "CC BY-SA 3.0"},
    "ph_br_chint":  {"title": "Chint circuit breakers",
                     "author": "Dmitry G", "licence": "CC BY-SA 3.0"},
    # ক্লোজ-আপগুলো উপরের ছবিরই অংশ — কৃতজ্ঞতাও তাই একই
    "ph_mcb_face":  {"title": "Circuit breaker 2 pole on DIN rail (লেবেল)",
                     "author": "Kae", "licence": "CC BY-SA 3.0"},
    "ph_mccb_face": {"title": "MCCB Merlin Gerin Compact NS100N (লেবেল)",
                     "author": "Pui108108", "licence": "CC BY 4.0"},
    "ph_mccb_trip": {"title": "MCCB Merlin Gerin Compact NS100N "
                              "(ট্রিপ ইউনিট)",
                     "author": "Pui108108", "licence": "CC BY 4.0"},
    "ph_rccb_face": {"title": "Siemens RCCB 40 A, 30 mA (লেবেল)",
                     "author": "Dmitry G", "licence": "CC BY-SA 3.0"},
    "ph_spd_face":  {"title": "Dornbirn — Surge arresters OBO V20-C (লেবেল)",
                     "author": "Asurnipal", "licence": "CC BY-SA 4.0"},
}


# ── সাধারণ কাজ ─────────────────────────────────────────────────────────
def _curl(url, timeout=240, least=2048):
    """urllib দিয়ে বারবার হিট করলে কমন্স ৪২৯ ফেরায়; curl-এ ঝামেলা কম।

    `least` — এর চেয়ে ছোট উত্তর মানে ছবি নয়, ভুল বা রেট-লিমিটের বার্তা।
    API-র উত্তর ছোট হয়, তাই সেখানে সীমাটা আলাদা করে দিতে হয়।
    """
    r = subprocess.run(["curl", "-sL", "-A", UA, "--max-time", str(timeout),
                        url], capture_output=True)
    if len(r.stdout) < least:
        raise SystemExit(f"✗ নামানো গেল না: {url}")
    return r.stdout


def commons_url(fname):
    """কমন্সের ফাইলনাম → আসল ছবির URL।  ফল ক্যাশে রাখা হয়।"""
    cache = os.path.join(CACHE, "ch22_urls.json")
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
    fn = os.path.join(CACHE, "ch22_" + fname.replace(" ", "_"))
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
        im = frac_crop(im, box)
        if im.width > wmax:
            im = im.resize((wmax, round(im.height * wmax / im.width)),
                           Image.LANCZOS)
        if contrast != 1.0:
            im = ImageEnhance.Contrast(im).enhance(contrast)
        im.save(os.path.join(OUT, name + ".jpg"), quality=93)
        print("✓", name, im.size, f"({fname})")


if __name__ == "__main__":
    do_photos()
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json লেখা হলো")
