# -*- coding: utf-8 -*-
"""ইনস্টিটিউটের স্লাইড থেকে নেওয়া অধ্যায় ৬-এর সার্কিট-ছবিতে তিনটি বানান ভুল
(Tow → Two, Serice → Series, Indecator → Indicator) শুধু সেই শব্দটুকুতে ঠিক করা।
মূল PPTX ছোঁয়া হয় না; কাজ হয় assets/ch06/-এর ক্রপ করা PNG-তে।"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

A = "/home/user/House_Wiring/Book/build/assets/ch06/"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"


def ink(font, s):
    x0, y0, x1, y1 = font.getbbox(s)
    return x0, y0, x1, y1


def retouch(im, box, old, new, fontfile, dark, align):
    a = np.asarray(im).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = ((r > 160) & (r < 225) & (g < 40) & (b < 40)) if dark else ((r > 235) & (g < 90) & (b < 90))
    X0, Y0, X1, Y1 = box
    sub = m[Y0:Y1, X0:X1]
    ys, xs = np.where(sub)
    x0, x1, y0, y1 = X0 + xs.min(), X0 + xs.max(), Y0 + ys.min(), Y0 + ys.max()
    width = x1 - x0 + 1
    # পুরোনো শব্দের কালির চওড়া মিলিয়ে ফন্টের মাপ
    lo, hi = 10, 600
    while hi - lo > 1:
        mid = (lo + hi) // 2
        f = ImageFont.truetype(fontfile, mid)
        bx = ink(f, old)
        if bx[2] - bx[0] < width: lo = mid
        else: hi = mid
    f = ImageFont.truetype(fontfile, lo)
    ob, nb = ink(f, old), ink(f, new)
    col = tuple(int(v) for v in np.median(a[Y0:Y1, X0:X1][sub], axis=0))
    d = ImageDraw.Draw(im)
    pad = 8
    d.rectangle([x0 - pad, y0 - pad, x1 + pad, y1 + pad], fill=(255, 255, 255))
    nw = nb[2] - nb[0]
    if align == "center":
        nx = (x0 + x1) / 2 - nw / 2
    else:
        nx = x0
    # কালির উপরের ধার মেলানো (দুই শব্দই বড় হাতের অক্ষরে শুরু)
    d.text((nx - nb[0], y0 - ob[1]), new, font=f, fill=col)
    print(f"   {old!r} → {new!r}  size {lo}px  box ({x0},{y0})–({x1},{y1})  colour {col}")


JOBS = [
    ("d04_two_switch_schem.png", (600, 10, 3500, 180), "Tow Switch Doorbell Circuit",
     "Two Switch Doorbell Circuit", SERIF, False, "center"),
    ("d05_series_schem.png", (850, 10, 3250, 180), "Serice Doorbell Circuit",
     "Series Doorbell Circuit", SERIF, False, "center"),
    ("d07_indicator_schem.png", (2700, 380, 3720, 520), "Indecator 1", "Indicator 1", SERIF, True, "left"),
    ("d07_indicator_schem.png", (2700, 800, 3720, 940), "Indecator 2", "Indicator 2", SERIF, True, "left"),
    ("d07_indicator_schem.png", (2700, 1222, 3720, 1362), "Indecator 3", "Indicator 3", SERIF, True, "left"),
    ("d07_indicator_conn.png", (780, 780, 1210, 892), "Indecator", "Indicator", SANS, True, "center"),
]
cache = {}
for fn, box, old, new, ff, dark, al in JOBS:
    if fn not in cache:
        cache[fn] = Image.open(A + fn).convert("RGB")
        print(fn)
    retouch(cache[fn], box, old, new, ff, dark, al)
for fn, im in cache.items():
    im.save(A + fn, optimize=True)
