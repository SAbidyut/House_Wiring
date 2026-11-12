# -*- coding: utf-8 -*-
"""ইনস্টিটিউটের স্লাইড থেকে নেওয়া অধ্যায় ১৩-এর টানেল ওয়্যারিং কানেকশন-ছবিতে বানান ভুল
(Indecator → Indicator) শুধু সেই লেখাটুকুতে ঠিক করা।
মূল PPTX ছোঁয়া হয় না; কাজ হয় assets/ch13/-এর ক্রপ করা PNG-তে।
একবারই চালাতে হয়: দ্বিতীয়বার চালালে পুরোনো শব্দ আর মেলে না বলে মাপ সামান্য বদলাবে।"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

A = "/home/user/House_Wiring/Book/build/assets/"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"


def retouch(im, box, old, new, fontfile, dark, align, underline=False):
    a = np.asarray(im).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = ((r > 150) & (r < 230) & (g < 45) & (b < 45)) if dark else ((r > 235) & (g < 90) & (b < 90))
    X0, Y0, X1, Y1 = box
    sub = m[Y0:Y1, X0:X1]
    ys, xs = np.where(sub)
    x0, x1, y0, y1 = X0 + xs.min(), X0 + xs.max(), Y0 + ys.min(), Y0 + ys.max()
    width = x1 - x0 + 1
    ul = None
    if underline:
        rows = sub.sum(1)
        ur = np.where(rows > 0.8 * width)[0]
        ul = (Y0 + ur.min(), Y0 + ur.max())
    lo, hi = 10, 600
    while hi - lo > 1:
        mid = (lo + hi) // 2
        f = ImageFont.truetype(fontfile, mid)
        bx = f.getbbox(old)
        if bx[2] - bx[0] < width: lo = mid
        else: hi = mid
    f = ImageFont.truetype(fontfile, lo)
    ob, nb = f.getbbox(old), f.getbbox(new)
    col = tuple(int(v) for v in np.median(a[Y0:Y1, X0:X1][sub], axis=0))
    d = ImageDraw.Draw(im)
    pad = 8
    d.rectangle([x0 - pad, y0 - pad, x1 + pad, y1 + pad], fill=(255, 255, 255))
    nw = nb[2] - nb[0]
    nx = (x0 + x1) / 2 - nw / 2 if align == "center" else x0
    d.text((nx - nb[0], y0 - ob[1]), new, font=f, fill=col)
    if ul:
        d.rectangle([nx, ul[0], nx + nw, ul[1]], fill=col)
    print(f"   {old!r} → {new!r}  size {lo}px  box ({x0},{y0})–({x1},{y1})  colour {col}  underline {ul}")


JOBS = [
    ("ch13/h18_tunnel_conn.png", (700, 990, 1150, 1110), "Indecator", "Indicator", SANS, True, "center", False),
]
cache = {}
for fn, box, old, new, ff, dark, al, u in JOBS:
    if fn not in cache:
        cache[fn] = Image.open(A + fn).convert("RGB")
        print(fn)
    retouch(cache[fn], box, old, new, ff, dark, al, u)
for fn, im in cache.items():
    im.save(A + fn, optimize=True)
