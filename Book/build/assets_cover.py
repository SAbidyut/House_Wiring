# -*- coding: utf-8 -*-
"""assets_cover.py — প্রচ্ছদের জন্য RAPTI-র নিজস্ব লোগো নামিয়ে আনে।

সূত্র: প্রতিষ্ঠানের নিজের ওয়েবসাইট rapti.net —
    assets/images/logo_ippi.png   (এমব্লেম + RAPTI ওয়ার্ডমার্ক, 356×130)
    assets/images/icon.png        (কেবল গোল এমব্লেম, 150×150)

দুটোই RGBA, চারপাশ স্বচ্ছ।  স্বচ্ছ PNG কিছু রেন্ডারারে কালো ছাপে
(অধ্যায় ১৮-এর শিক্ষা), তাই সাদার উপর ফ্ল্যাট করে রাখা হয় — প্রচ্ছদে
লোগোটি সাদা পটির উপরেই বসে।

পিক্সেল-সাইজ assert করা আছে ট্রিপওয়্যার হিসেবে: ওয়েবসাইটে ছবি বদলালে
নীরবে ভুল ছবি বসে যাবে না, বিল্ড থেমে যাবে।
"""
import os, urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "cover")
CACHE = os.path.join(HERE, ".coverdl")

FILES = {
    "logo_rapti": ("https://rapti.net/assets/images/logo_ippi.png", (356, 130)),
    "icon_rapti": ("https://rapti.net/assets/images/icon.png",      (150, 150)),
}


def _download(name, url):
    os.makedirs(CACHE, exist_ok=True)
    dst = os.path.join(CACHE, name + ".png")
    if not os.path.exists(dst):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(dst, "wb") as f:
            f.write(r.read())
    return dst


WORDMARK_X0 = 137          # লোগোর ভেতরে এমব্লেম ও "RAPTI" লেখার মাঝের ফাঁক
                            # (আলফা-চ্যানেলে ১৩০–১৪২ কলাম পুরো ফাঁকা)


def _light_wordmark(im):
    """গাঢ় নেভি "RAPTI" লেখাটিকে সাদা করে — এমব্লেমে হাত না দিয়ে।

    প্রচ্ছদ গাঢ় নীল, আর ওয়ার্ডমার্কের রং প্রায় কালো-নীল (0,24,32) — সরাসরি
    বসালে লেখাটি মিলিয়ে যায়।  আলফা অপরিবর্তিত রেখে কেবল RGB সাদা করা হয়,
    তাই কিনারার অ্যান্টি-অ্যালিয়াসিং যেকোনো পটভূমিতেই ঠিক থাকে।
    """
    im = im.copy()
    px = im.load()
    w, h = im.size
    for x in range(WORDMARK_X0, w):
        for y in range(h):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = (255, 255, 255, a)
    return im


def build():
    os.makedirs(OUT, exist_ok=True)
    made = []
    for name, (url, size) in FILES.items():
        src = _download(name, url)
        im = Image.open(src)
        assert im.size == size, f"{name}: expected {size}, got {im.size}"
        im = im.convert("RGBA")
        flat = Image.new("RGB", im.size, (255, 255, 255))
        flat.paste(im, mask=im.split()[3])
        p = os.path.join(OUT, name + ".png")
        flat.save(p)
        made.append(p)
        print("✓", os.path.relpath(p, HERE), flat.size)
        if name == "logo_rapti":
            q = os.path.join(OUT, "logo_rapti_light.png")
            _light_wordmark(im).save(q)       # স্বচ্ছ থাকে — নেভির উপর বসবে
            made.append(q)
            print("✓", os.path.relpath(q, HERE), "(wordmark → white, RGBA)")
    return made


if __name__ == "__main__":
    build()
