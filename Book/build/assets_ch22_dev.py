# -*- coding: utf-8 -*-
"""অধ্যায় ২২-এর যন্ত্র-চেনার ছবি — ইনস্টিটিউটের নিজের ফাইল থেকে।

`assets_ch22.py`-র ছবিগুলো উইকিমিডিয়া কমন্স থেকে, আর তাদের কাজ একটাই —
**গায়ের লেখা পড়ানো**।  সেজন্য ওগুলো আসল যন্ত্রের আলোকচিত্র, ঘনিষ্ঠ ক্রপ,
পাশে কল-আউট।

এই ফাইলের ছবিগুলোর কাজ আলাদা — **যন্ত্রটা দেখতে কেমন**।  একজন
শিক্ষার্থী যেন MCB আর RCBO পাশাপাশি রাখলে চিনতে পারে, MCCB-র খোল যে
আলাদা তা বুঝতে পারে, SPD-র প্লাগ-ইন মডিউল দেখলে ধরতে পারে।  তার জন্য
ক্যাটালগ-রেন্ডারই বরং ভালো:  সাদা পটভূমি, এক আলো, এক কোণ — এগারোটি
যন্ত্র পাশাপাশি বসালে চোখ কেবল আকৃতির পার্থক্যটাই দেখে।

উৎস:  ইনস্টিটিউটের `Standard Markings on Circuit Breakers.docx`
(প্রকল্পের গোড়ার ফাইল, শুধু পড়া হয় — কখনো বদলানো হয় না)।  ভেতরের
`word/media/image1..11.png` ঠিক নথির ক্রমেই আছে, যাচাই করা:

    1 MCB · 2 MCCB · 3 RCCB · 4 RCBO · 5 ELCB · 6 MPCB
    7 AFDD · 8 আইসোলেটর · 9 SPD · 10 ACB · 11 VCB

সবগুলোই CHiNT-এর পণ্য-রেন্ডার।  ছবিগুলো RGBA, পটভূমি স্বচ্ছ — অধ্যায়
১৮-এর শিক্ষা অনুযায়ী সাদার উপরে বসিয়ে নিতে হয়, নইলে ছাপায় কালো আসে।
আলফা চ্যানেলই এখানে নিখুঁত ক্রপ-বক্স দেয়, তাই পিক্সেল গুনে অটোক্রপ
করার দরকার নেই।

চালানোর নিয়ম:  python assets_ch22_dev.py     (Book/build/ থেকে)
"""
import io
import os
import zipfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "assets", "ch22")
SRC = os.path.join(ROOT, "Standard Markings on Circuit Breakers.docx")

os.makedirs(OUT, exist_ok=True)

# নাম → (নথির ভেতরের ছবি, প্রত্যাশিত মাপ)
#
# মাপটা পাহারাদার — ইনস্টিটিউট নথিটি বদলালে ক্রম এলোমেলো হয়ে যেতে
# পারে, তখন ছাপার পর নয়, এখানেই ধরা পড়বে।
DEVICES = {
    "dev_mcb":      ("image1.png",  (600, 600)),
    "dev_mccb":     ("image2.png",  (600, 600)),
    "dev_rccb":     ("image3.png",  (557, 688)),
    "dev_rcbo":     ("image4.png",  (452, 557)),
    "dev_elcb":     ("image5.png",  (602, 779)),
    "dev_mpcb":     ("image6.png",  (501, 677)),
    "dev_afdd":     ("image7.png",  (522, 615)),
    "dev_isolator": ("image8.png",  (554, 735)),
    "dev_spd":      ("image9.png",  (487, 702)),
    "dev_acb":      ("image10.png", (614, 721)),
    "dev_vcb":      ("image11.png", (757, 682)),
}

WMAX = 700


def flatten(im):
    """RGBA → সাদার উপরে বসানো RGB (অধ্যায় ১৮)।"""
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    return Image.alpha_composite(bg, im).convert("RGB")


def tight_box(im, thr=25, pad=6):
    """পটভূমি বাদ দিয়ে যন্ত্রটুকুর ঘেরাটোপ।

    ছায়ার আলফা কম, তাই সীমা ২৫ — নইলে ছায়াটুকুও বাক্সের ভেতরে ঢুকে
    যন্ত্রটিকে টাইলের মধ্যে ছোট করে দেয়।

    এগারোটির মধ্যে তিনটি (MCB, MCCB, MPCB) আসলে স্বচ্ছ নয় — আলফা
    সর্বত্র ২৫৫, পটভূমি নিরেট সাদা।  ওদের বেলায় আলফা-বাক্স গোটা ছবিই
    ফেরত দেয়, তাই তখন সাদা-থেকে-পার্থক্য দেখে কাটতে হয়।
    """
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
    for name, (member, size) in DEVICES.items():
        raw = z.read("word/media/" + member)
        im = Image.open(io.BytesIO(raw))
        if im.size != size:
            raise SystemExit(f"✗ {name}: {member}-এর মাপ {im.size}, "
                             f"হওয়ার কথা {size} — উৎস নথিটি বদলেছে, "
                             f"ছবির ক্রম আবার মিলিয়ে নিতে হবে")
        im = flatten(im.crop(tight_box(im)))
        if im.width > WMAX:
            im = im.resize((WMAX, round(im.height * WMAX / im.width)),
                           Image.LANCZOS)
        im.save(os.path.join(OUT, name + ".jpg"), quality=93)
        print("✓", name, im.size, f"({member})")


if __name__ == "__main__":
    main()
