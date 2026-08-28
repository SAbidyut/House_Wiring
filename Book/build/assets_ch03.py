# -*- coding: utf-8 -*-
"""অধ্যায় ৩-এর হোল্ডারের আসল ছবি — ইনস্টিটিউটের নিজের ফাইল থেকে।

চিত্র ৩.৩ আগে চারটি হাতে-আঁকা স্কেচ ছিল, আর চারটিই দেখতে প্রায় এক —
একই খোল, একই বাতি, শুধু উপরের ধরাটুকু আলাদা।  হোল্ডার চেনানোর কাজটা
তাতে হয় না।  তাই এখন বসানোর ধরনটুকু আঁকা থাকে, আর হোল্ডার নিজে
**আসল ছবি**।

উৎস:  ইনস্টিটিউটের `Electrical House Wiring book.docx` (প্রকল্পের গোড়ার
ফাইল, শুধু পড়া হয় — কখনো বদলানো হয় না)।  নথির ভেতরে ছবিগুলো ঠিক
লেখার ক্রমেই আছে; blip ধরে ধরে মিলিয়ে দেখা হয়েছে —

    “ব্যাটেন হোল্ডার: এই হোল্ডার থ্রেড (প্যাচ) টাইপ ও পিন টাইপ
     হয়ে থাকে…”            → image88 (পিন)  · image89 (থ্রেড)
    “প্যান্ডেন্ট হোল্ডার: …”  → image90 (পিন)  · image91 (থ্রেড)
    “সিলিং রোজ: …”           → image92

image88/90/91 RGBA, পটভূমি স্বচ্ছ — অধ্যায় ১৮-এর শিক্ষা অনুযায়ী সাদার
উপরে বসিয়ে নিতে হয়, নইলে ছাপায় কালো আসে।  image89 সাধারণ JPEG, আলফা
নেই; তখন `tight_box()` সাদা-থেকে-পার্থক্য দেখে কাটে (অধ্যায় ২২-এর
MCB/MCCB-র মতোই)।

**অ্যাঙ্গেল হোল্ডারের ছবিটি ব্যবহারকারীর দেওয়া** — প্রকল্পের গোড়ায়
`angle-holder.jpg` (২০২৬-০৮-২৫)।  ইনস্টিটিউটের নথিতে ওটির ছবি নেই, দুই
ডায়াগ্রাম-ডেকের একটি স্লাইডেও নেই, উইকিমিডিয়া কমন্স / Openverse /
Pixabay-তেও নেই (Lampholders, Lampholder sockets, Light bulb sockets —
সব ক-টি ক্যাটাগরি আর ইংরেজি-জার্মান-ফরাসি-স্প্যানিশ-ইন্দোনেশীয় নামে
খোঁজা হয়েছে)।  তাই আবার খুঁজতে যেয়ো না — ফাইলটিই একমাত্র উৎস।
ছবিটি পিন (BC) টাইপ, ভেতরের পিতলের খাঁজ দেখে যাচাই করা।

চালানোর নিয়ম:  python assets_ch03.py     (Book/build/ থেকে)
"""
import io
import os
import zipfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "assets", "ch03")
SRC = os.path.join(ROOT, "Electrical House Wiring book.docx")

os.makedirs(OUT, exist_ok=True)

# নাম → (নথির ভেতরের ছবি, প্রত্যাশিত মাপ)।  মাপটা পাহারাদার — উৎস নথি
# বদলালে ছবির ক্রম এলোমেলো হয়ে যেতে পারে, তখন ছাপার পর নয়, এখানেই
# ধরা পড়বে।
HOLDERS = {
    "ph_batten_pin":    ("image88.png", (500, 500)),
    "ph_batten_screw":  ("image89.jpg", (500, 500)),
    "ph_pendant_pin":   ("image90.png", (570, 570)),
    "ph_pendant_screw": ("image91.png", (400, 400)),
}

# ব্যবহারকারীর দেওয়া ছবি, প্রকল্পের গোড়ায় রাখা
ROOT_PICS = {
    "ph_angle": ("angle-holder.jpg", (500, 500)),
}

WMAX = 640


def flatten(im):
    """RGBA → সাদার উপরে বসানো RGB (অধ্যায় ১৮)।"""
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    return Image.alpha_composite(bg, im).convert("RGB")


def tight_box(im, thr=25, pad=6):
    """পটভূমি বাদ দিয়ে হোল্ডারটুকুর ঘেরাটোপ (অধ্যায় ২২)।"""
    a = im.convert("RGBA").split()[3].point(lambda v: 255 if v > thr else 0)
    box = a.getbbox()
    if box is None or (box[2] - box[0]) * (box[3] - box[1]) > \
            0.98 * im.width * im.height:
        grey = flatten(im).convert("L").point(lambda v: 255 if v < 244 else 0)
        box = grey.getbbox() or (0, 0, im.width, im.height)
    x0, y0, x1, y1 = box
    return (max(0, x0 - pad), max(0, y0 - pad),
            min(im.width, x1 + pad), min(im.height, y1 + pad))


def main():
    if not os.path.exists(SRC):
        raise SystemExit(f"✗ উৎস ফাইলটি নেই: {SRC}")
    z = zipfile.ZipFile(SRC)
    jobs = [(n, m, sz, Image.open(io.BytesIO(z.read("word/media/" + m))))
            for n, (m, sz) in HOLDERS.items()]
    for name, (member, size) in ROOT_PICS.items():
        path = os.path.join(ROOT, member)
        if not os.path.exists(path):
            raise SystemExit(f"✗ {name}: {path} নেই")
        jobs.append((name, member, size, Image.open(path)))

    for name, member, size, im in jobs:
        if im.size != size:
            raise SystemExit(f"✗ {name}: {member}-এর মাপ {im.size}, "
                             f"হওয়ার কথা {size} — উৎস ফাইলটি বদলেছে, "
                             f"ছবির ক্রম আবার মিলিয়ে নিতে হবে")
        im = flatten(im.crop(tight_box(im)))
        if im.width > WMAX:
            im = im.resize((WMAX, round(im.height * WMAX / im.width)),
                           Image.LANCZOS)
        im.save(os.path.join(OUT, name + ".jpg"), quality=93)
        print("✓", name, im.size, f"({member})")


if __name__ == "__main__":
    main()
