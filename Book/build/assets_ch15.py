# -*- coding: utf-8 -*-
"""অধ্যায় ১৫-এর ছবি প্রস্তুত করা।

উৎস — ইনস্টিটিউটের নিজস্ব দুই ডেক:
  `Circuit Diagram.pptx`            স্লাইড ২২, ২৩  (স্কিম্যাটিক)
  `HW Connection Diagram All.pptx`  স্লাইড ২২, ২৩  (পিক্টোরিয়াল)
  `HW Connection Diagram All.pptx`  স্লাইড ৩৪, ৩৫  — কেবল বোর্ডের অংশটুকু
                                    কেটে নেওয়া (পিয়ানো বনাম গ্যাং)।

স্লাইড নম্বর PDF পৃষ্ঠার লেখা থেকে যাচাই করা — দুই ডেকেই এক সারি আগে-পরে
প্রায়-একই ছবি আছে।

চালানোর নিয়ম:  python assets_ch15.py     (Book/build/ থেকে)
"""
import os, json, subprocess
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))     # প্রজেক্টের রুট
OUT = os.path.join(HERE, "assets", "ch15")
CACHE = os.path.join(HERE, ".slidepdf")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)

CD = "Circuit Diagram.pptx"
HW = "HW Connection Diagram All.pptx"

# নাম → (সোর্স ফাইল, PDF পৃষ্ঠা-সূচক, (x0, y0, x1, y1) ভগ্নাংশে বা None)
SLIDES = {
    "c22_board_schem":     (CD, 21, None),
    "c23_socket_schem":    (CD, 22, None),
    "h22_board_conn":      (HW, 21, None),
    "h23_socket_conn":     (HW, 22, None),
    # ঘরের লে-আউটের ভেতর থেকে কেবল বাঁ পাশের বোর্ডটুকু — স্লাইডের
    # শিরোনামের লেখা ও পাইপের টুকরো যাতে ছবিতে না ঢোকে
    "h34_piano_board":     (HW, 33, (0.522, 0.745, 0.775, 0.888)),
    "h35_gang_board":      (HW, 34, (0.516, 0.752, 0.760, 0.900)),
}

# পৃষ্ঠার লেখায় এই শব্দগুলো থাকতেই হবে — এক সারি এদিক-ওদিক হলে ধরা পড়বে
EXPECT = {
    "c22_board_schem":  ["Switch", "Board", "Regulator", "Fan"],
    "c23_socket_schem": ["Switch", "Board", "Socket", "Regulator"],
    "h22_board_conn":   ["Switch", "bord", "Regulator", "Indecator"],
    "h23_socket_conn":  ["Switch", "bord", "Socket", "Regulator"],
    "h34_piano_board":  ["Piano", "Switch", "board"],
    "h35_gang_board":   ["Gang", "Switch", "board"],
}


def slide_pdf(name):
    """PPTX → PDF (একবারই), তারপর ক্যাশ থেকে।"""
    pdf = os.path.join(CACHE, os.path.splitext(name)[0] + ".pdf")
    if not os.path.exists(pdf):
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                        "--outdir", CACHE, os.path.join(ROOT, name)],
                       check=True, capture_output=True)
    return pdf


def autocrop(im, thr=244, pad=24, need=4):
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


def do_slides():
    for name, (src, pg, box) in SLIDES.items():
        d = pymupdf.open(slide_pdf(src))
        words = d[pg].get_text().split()
        missing = [k for k in EXPECT[name] if k not in words]
        if missing:
            raise SystemExit(f"✗ {name}: স্লাইড {pg + 1}-এ নেই {missing} "
                             f"— নম্বর মিলিয়ে দেখো")
        pix = d[pg].get_pixmap(dpi=300)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if box:
            w, h = im.size
            im = im.crop((int(w * box[0]), int(h * box[1]),
                          int(w * box[2]), int(h * box[3])))
        im = autocrop(im)
        bg = Image.new("RGB", (im.width + 48, im.height + 48), "white")
        bg.paste(im, (24, 24))
        bg.save(os.path.join(OUT, name + ".png"))
        print("✓", name, bg.size, f"({src} স্লাইড {pg + 1})")


CREDITS = {
    "rapti_slides": {
        "files": sorted(SLIDES),
        "source": ("RAPTI — Circuit Diagram.pptx (slides 22, 23) and "
                   "HW Connection Diagram All.pptx (slides 22, 23, 34, 35)"),
        "licence": "Institute's own material",
    },
}

if __name__ == "__main__":
    do_slides()
    json.dump(CREDITS, open(os.path.join(OUT, "credits.json"), "w"),
              ensure_ascii=False, indent=2)
    print("credits.json written")
