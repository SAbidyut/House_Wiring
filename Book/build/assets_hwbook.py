# -*- coding: utf-8 -*-
"""ইনস্টিটিউটের নিজের বইয়ের “হাউস ওয়ারিং এ ব্যবহৃত মালামালসমূহ” ছবিগুলো।

উৎস: `Electrical House Wiring book.docx` (প্রকল্পের গোড়ার ফাইল — শুধু পড়া
হয়, কখনো বদলানো হয় না)।  নথির ভেতরে একটি বড় সারণি আছে যার প্রতিটি সারিতে
একটি মালামালের নাম-ও-ব্যবহার আর তার পাশে **আসল ছবি**।  ছবিগুলো নথির লেখার
ক্রমেই বসানো — blip ধরে ধরে মিলিয়ে দেখা হয়েছে (নিচের `NAMES` তালিকার
মন্তব্যই সেই মিলকরণ)।

ইনস্টিটিউটের নিজের ছবি, তাই ❖ চিত্রসূত্র বাক্স লাগে না — ওই বাক্স কেবল
CC BY-SA কমন্স ছবির জন্য।

চালানোর নিয়ম:  python assets_hwbook.py      (Book/build/ থেকে)
"""
import io
import os
import zipfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "assets", "hwbook")
SRC = os.path.join(ROOT, "Electrical House Wiring book.docx")

os.makedirs(OUT, exist_ok=True)

# নাম → (নথির ছবি, প্রত্যাশিত পিক্সেল মাপ)।  মাপটা পাহারাদার: উৎস নথি
# বদলালে ছবির ক্রম এলোমেলো হতে পারে, তখন ছাপার পরে নয় — এখানেই ধরা পড়বে।
NAMES = {
    # ── পিয়ানো (ব্যাটেন) ধরনের সুইচ-সকেট ───────────────────────────────
    "sw_oneway":      ("image65.png", (364, 364)),   # ওয়ান ওয়ে সুইচ
    "sw_twoway":      ("image66.png", (500, 500)),   # টু ওয়ে সুইচ
    "sock_2pin":      ("image67.png", (364, 364)),   # টু পিন সকেট
    "fuse_piano":     ("image68.png", (114, 236)),   # ফিউজ
    "reg_coil":       ("image69.png", (364, 364)),   # ফ্যান রেগুলেটর
    "sw_bellpush":    ("image70.png", (364, 364)),   # বেল পুশ সুইচ
    "indicator":      ("image71.png", (500, 500)),   # ইন্ডিকেটর লাইট
    # ── গ্যাং (মডিউলার) ধরন ────────────────────────────────────────────
    "gang1":          ("image72.png", (510, 510)),
    "gang2":          ("image73.png", (510, 510)),
    "gang3":          ("image74.png", (510, 510)),
    "gang4":          ("image75.png", (510, 510)),
    "gang5":          ("image76.png", (510, 510)),
    "dimmer":         ("image77.png", (1200, 1200)),  # ফ্যান ডিমার
    "sock_3pin":      ("image78.png", (960, 960)),    # থ্রি পিন পাওয়ার সকেট
    "sock_3pin_flat": ("image79.png", (510, 510)),
    "dp_switch":      ("image80.png", (1000, 995)),   # ডিপি সুইচ
    "dp_switch2":     ("image81.png", (1792, 1780)),
    "gang_bell":      ("image82.png", (1190, 1190)),  # গ্যাং পুশ বেল সুইচ
    "sw_inter":       ("image83.png", (500, 500)),    # ইন্টারমিডিয়েট সুইচ
    "sw_inter2":      ("image84.png", (924, 913)),
    # ── প্লাগ ─────────────────────────────────────────────────────────
    "plug_2pin":      ("image85.png", (700, 700)),
    "plug_3pin_flat": ("image86.png", (609, 684)),   # ১৩A চ্যাপ্টা পিন
    "plug_3pin_round":("image87.png", (400, 400)),   # ১৫A গোল পিন
    "ceil_rose":      ("image92.png", (600, 600)),    # সিলিং রোজ
    # ── বক্স ──────────────────────────────────────────────────────────
    "box_piano":      ("image93.png", (980, 630)),
    "box_gang_steel": ("image94.png", (440, 250)),
    "box_gang_pvc":   ("image95.png", (800, 800)),
    "box_circular":   ("image96.png", (500, 500)),
    "box_circular2":  ("image97.png", (750, 750)),
    # ── কন্ডুইটের ফিটিংস ও চ্যানেল ──────────────────────────────────────
    "bend":           ("image98.png", (356, 400)),    # ব্যান
    "elbow":          ("image99.png", (500, 500)),
    "tee":            ("image100.png", (1000, 1000)),
    "saddle":         ("image101.png", (550, 550)),
    "pvc_channel":    ("image102.png", (1280, 1000)),
    "pvc_pipe":       ("image103.png", (1280, 1000)),
    "cable_tray":     ("image104.png", (807, 807)),
    "cable_tray2":    ("image105.png", (500, 500)),
    # ── বিতরণ ও সংযোগ ─────────────────────────────────────────────────
    "lugs":           ("image106.png", (500, 500)),   # ক্যাবল লাগ
    "main_switch":    ("image107.png", (500, 500)),   # DPIC মেইন সুইচ
    "sdb":            ("image108.png", (3112, 2496)),  # সাব-ডিস্ট্রিবিউশন বক্স
    "changeover":     ("image109.jpg", (1200, 1200)),
    "changeover2":    ("image110.png", (576, 384)),
    # ── ফাস্টেনার ও ছোট মালামাল ────────────────────────────────────────
    "rawl_bolt":      ("image111.png", (500, 389)),
    "rawl_plug":      ("image112.png", (225, 160)),
    "rawl_plug2":     ("image113.png", (154, 138)),
    "screw_star":     ("image116.png", (500, 500)),
    "screw_flat":     ("image117.png", (894, 779)),
    "cable_clip":     ("image118.png", (1500, 1500)),
    "cable_tie":      ("image119.png", (600, 600)),
    "din_rail":       ("image120.png", (500, 500)),   # এমসিবির ম্যাটালিক চ্যানেল
}

WMAX = 760


def flatten(im):
    """RGBA → সাদার উপরে বসানো RGB (অধ্যায় ১৮-এর শিক্ষা)।"""
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    return Image.alpha_composite(bg, im).convert("RGB")


def tight_box(im, thr=25, pad=6):
    """পটভূমি বাদ দিয়ে বস্তুটুকুর ঘেরাটোপ (অধ্যায় ২২-এর `tight_box`)।

    আলফা-বাক্সটা যদি প্রায় গোটা ছবিই ঢেকে ফেলে (অর্থাৎ আলফা সব জায়গায়
    255 — ছবিটা সত্যিকারের স্বচ্ছ নয়), তখন সাদা-থেকে-পার্থক্য দেখে কাটা হয়।
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
    for name, (member, size) in NAMES.items():
        im = Image.open(io.BytesIO(z.read("word/media/" + member)))
        if im.size != size:
            raise SystemExit(f"✗ {name}: {member}-এর মাপ {im.size}, হওয়ার কথা "
                             f"{size} — উৎস নথি বদলেছে, ক্রম মিলিয়ে নিতে হবে")
        im = flatten(im.crop(tight_box(im)))
        if im.width > WMAX:
            im = im.resize((WMAX, round(im.height * WMAX / im.width)),
                           Image.LANCZOS)
        im.save(os.path.join(OUT, name + ".jpg"), quality=93)
        print("✓", f"{name:16s}", im.size, f"({member})")
    print(f"\n{len(NAMES)} টি ছবি → {OUT}")


if __name__ == "__main__":
    main()
