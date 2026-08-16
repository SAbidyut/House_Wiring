# -*- coding: utf-8 -*-
"""অধ্যায় ১৮-এর ছবি প্রস্তুত করা।

উৎস ১ — ইনস্টিটিউটের নিজস্ব `Motor.docx`।  ওই ফাইলের ভেতরে রাখা ছবিগুলোই
        সিলেবাসের চারটি বিষয়ের সরাসরি ছবি: রান ক্যাপাসিটর সংযোগ, স্টার্ট-রান
        ক্যাপাসিটর সংযোগ, ডিপি সুইচ দিয়ে পাম্প-মোটরের সংযোগ, আর টার্মিনাল
        বক্সে স্টার ও ডেল্টার লিংক।  docx আসলে zip — `word/media/` থেকে
        সরাসরি বের করে নেওয়া হয়।  ছবিগুলো RGBA, স্বচ্ছ জায়গা কালো হয়ে
        যায় বলে আগে সাদা কাগজের উপর বসাতে হয়।

উৎস ২ — উইকিমিডিয়া কমন্স।  মোটরের কাটা-ছবি (পাবলিক ডোমেইন), স্কুইরেল কেজ
        রোটর ও স্টেটরের আলোকচিত্র।  কৃতজ্ঞতা `credits.json`-এ, আর অধ্যায়ের
        শেষে ❖ চিত্রসূত্র বাক্সে (CC BY-SA ছবির জন্য এটি আইনি শর্ত)।

`HW Connection Diagram All.pptx` ও `Circuit Diagram.pptx` — দুটোতেই মোটরের
কোনো স্লাইড নেই (প্রতিটি স্লাইডের লেখা বের করে দেখা হয়েছে), তাই এই
অধ্যায়ে ওই দুই ডেক ব্যবহার হয়নি।

চালানোর নিয়ম:  python assets_ch18.py     (Book/build/ থেকে)
"""
import os, io, json, zipfile, urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))     # প্রজেক্টের রুট
OUT = os.path.join(HERE, "assets", "ch18")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)
UA = {"User-Agent": "rapti-book/1.0 (textbook figure prep)"}

DOCX = "Motor.docx"

# নাম → (docx-এর ভেতরের ফাইল, প্রত্যাশিত মাপ, ক্রপ-বক্স ভগ্নাংশে বা None)
# মাপটা পাহারাদার — সোর্স ফাইল বদলালে বা ছবির ক্রম পাল্টালে এখানেই ধরা পড়ে।
DOC_IMAGES = {
    "m05_run_cap":     ("image5.png",  (804, 557),   None),
    "m06_dp_pump":     ("image6.png",  (1389, 717),  None),
    "m07_start_run":   ("image7.png",  (1098, 658),  None),
    "m10_star_term":   ("image10.png", (259, 337),   None),
    "m12_delta_term":  ("image12.png", (266, 339),   None),
}


def autocrop(im, thr=244, pad=18, need=4):
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


def flatten(raw):
    """RGBA → সাদা কাগজে বসানো RGB।  না করলে স্বচ্ছ জায়গা কালো ছাপে।"""
    im = Image.open(io.BytesIO(raw))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(bg, im)
    return im.convert("RGB")


def do_docx():
    zf = zipfile.ZipFile(os.path.join(ROOT, DOCX))
    for name, (member, size, box) in DOC_IMAGES.items():
        raw = zf.read("word/media/" + member)
        im = flatten(raw)
        if im.size != size:
            raise SystemExit(f"✗ {name}: {member}-এর মাপ {im.size}, "
                             f"হওয়ার কথা {size} — সোর্স ফাইল বদলেছে")
        if box:
            w, h = im.size
            im = im.crop((int(w * box[0]), int(h * box[1]),
                          int(w * box[2]), int(h * box[3])))
        im = autocrop(im)
        bg = Image.new("RGB", (im.width + 40, im.height + 40), "white")
        bg.paste(im, (20, 20))
        bg.save(os.path.join(OUT, name + ".png"))
        print("✓", name, bg.size, f"({DOCX} / {member})")


# নাম → (URL, ক্রপ-বক্স ভগ্নাংশে বা None, সর্বোচ্চ চওড়া)
PHOTOS = {
    # জাদুঘরের কাটা-মডেল।  নিচের বাঁ কোণে প্রদর্শনীর ফলক আছে — ক্রপে বাদ।
    "ph_cutaway": ("https://upload.wikimedia.org/wikipedia/commons/3/35/"
                   "TMW_50906_Schnittmodell_einer_Drehstrommaschine_"
                   "%28Asynchronmaschine%29.jpg",
                   (0.135, 0.010, 0.985, 0.900), 1800),
    # স্কুইরেল কেজ রোটর — শ্যাফট, বিয়ারিং ও প্রান্তের রিং স্পষ্ট
    "ph_rotor":   ("https://upload.wikimedia.org/wikipedia/commons/f/fc/"
                   "Wirnik_by_Zureks.jpg", (0.03, 0.05, 0.99, 0.96), 1500),
    # রি-ওয়াইন্ডিং শপে খোলা স্টেটর।  ডান-নিচে ক্যামেরার তারিখ — ক্রপে বাদ।
    "ph_stator":  ("https://upload.wikimedia.org/wikipedia/commons/e/e7/"
                   "Stator_of_a_3-phase_induction_motor.jpg",
                   (0.15, 0.06, 0.84, 0.87), 1500),
}


def fetch(url):
    """ডাউনলোড করে ক্যাশে রাখা — বারবার কমন্সে হিট করলে ৪২৯ আসে।"""
    fn = os.path.join(CACHE, os.path.basename(url))
    if not os.path.exists(fn):
        raw = urllib.request.urlopen(
            urllib.request.Request(url, headers=UA), timeout=240).read()
        open(fn, "wb").write(raw)
    return open(fn, "rb").read()


def do_photos():
    for name, (url, box, wmax) in PHOTOS.items():
        im = Image.open(io.BytesIO(fetch(url))).convert("RGB")
        if box:
            w, h = im.size
            im = im.crop((int(w * box[0]), int(h * box[1]),
                          int(w * box[2]), int(h * box[3])))
        if im.width > wmax:
            im = im.resize((wmax, round(im.height * wmax / im.width)),
                           Image.LANCZOS)
        im.save(os.path.join(OUT, f"{name}.jpg"), quality=88)
        print("✓", name, im.size)


CREDITS = {
    "rapti_motor_docx": {
        "files": sorted(DOC_IMAGES),
        "source": "RAPTI — Motor.docx (word/media images 5, 6, 7, 10, 12)",
        "licence": "Institute's own material",
    },
    "ph_cutaway": {
        "source": "Wikimedia Commons — 'TMW 50906 Schnittmodell einer "
                  "Drehstrommaschine (Asynchronmaschine)', Technisches "
                  "Museum Wien",
        "licence": "Public domain",
    },
    "ph_rotor": {
        "source": "Wikimedia Commons — 'Wirnik by Zureks', by User:Zureks",
        "licence": "CC BY-SA 3.0",
    },
    "ph_stator": {
        "source": "Wikimedia Commons — 'Stator of a 3-phase induction motor'",
        "licence": "CC BY-SA 4.0",
    },
}

if __name__ == "__main__":
    do_docx()
    do_photos()
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json written")
