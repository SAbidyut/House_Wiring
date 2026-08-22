# -*- coding: utf-8 -*-
"""অধ্যায় ২২-এর ছবি প্রস্তুত করা।

দুই উৎস:
১। ইনস্টিটিউটের নিজের ফাইল — `circuit breaker.docx` ও
   `Standard Markings on Circuit Breakers.docx` — এর ভেতরের ছবি
   সরাসরি তুলে নেওয়া (PPTX-এর ভেতরের আসল ফাইলটাই)।

২। উইকিমিডিয়া কমন্স থেকে অতিরিক্ত কিছু বাস্তব ছবি — MCB-র ভেতর,
   আর্ক শুট ইত্যাদি — যদি প্রয়োজন হয়। আপাতত ইনস্টিটিউটের ছবিই
   যথেষ্ট, তাই কমন্স অংশ ঐচ্ছিক রাখা।

চালানোর নিয়ম: python assets_ch22.py (Book/build/ থেকে)
"""
import json
import os
import shutil
import hashlib
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "assets", "ch22")
os.makedirs(OUT, exist_ok=True)

# ইনস্টিটিউটের ছবি ইতিমধ্যে assets/ch22-তে কপি করা হয়েছে
# এখানে শুধু credits.json লেখা হবে, যাতে ch22.py পড়ে ❖ চিত্রসূত্র বানাতে পারে

CREDITS = {
    "fuse_hrc": {"title": "HRC Fuse", "author": "Institute source circuit breaker.docx", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "fuse_glass": {"title": "Glass Cartridge Fuse", "author": "Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "fuse_blade": {"title": "Blade Fuse automotive", "author": "Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "fuse_kitkat": {"title": "KitKat Fuse", "author": "Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "mcb_1p": {"title": "MCB 1P CHNT C63", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "mcb_2p": {"title": "MCB 2P CHNT C63", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "mcb_3p": {"title": "MCB 3P CHNT C63", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "mcb_4p": {"title": "MCB 4P CHNT C63", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "mccb_160a": {"title": "MCCB Hager 160A", "author": "Hager / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "mccb_100a": {"title": "MCCB Hager 100A", "author": "Hager / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "rccb_2p": {"title": "RCCB 2P 63A 30mA CHNT", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "rccb_4p": {"title": "RCCB 4P 63A 30mA CHNT", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "rcbo_2p": {"title": "RCBO 2P CHNT NXBLE-63", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "rcbo_4p": {"title": "RCBO 4P CHNT", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "rcbo_1pn": {"title": "RCBO 1P+N CHNT NXBLE-63", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "spd_2p": {"title": "SPD 1P+N TOMZN TZG40-C", "author": "TOMZN / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "spd_4p": {"title": "SPD 4P TOMZN TZG40-C", "author": "TOMZN / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "mcb_marking": {"title": "MCB Markings C16 6000A", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "mccb_marking": {"title": "MCCB Markings 320A", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "rccb_marking": {"title": "RCCB Markings NL1-63", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "rcbo_marking": {"title": "RCBO Markings NXBLE-40", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "spd_marking": {"title": "SPD Markings NXU-I+II/F 12.5/385", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "afdd": {"title": "AFDD NB4LE-AFD C16", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "mpcb": {"title": "MPCB NS2-25 Motor Protection", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "isolator": {"title": "Isolator Switch NXHB-125 125A", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "acb": {"title": "ACB CHNT Air Circuit Breaker", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "vcb": {"title": "VCB CHNT Vacuum Circuit Breaker NXV", "author": "CHNT / Institute source", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
    "rapti_docx": {"source": "RAPTI — circuit breaker.docx + Standard Markings on Circuit Breakers.docx", "licence": "ইনস্টিটিউটের নিজস্ব উপকরণ"},
}

if __name__ == "__main__":
    # Ensure all expected files exist
    missing = []
    for k in CREDITS:
        if k.startswith("rapti"):
            continue
        found = any(os.path.exists(os.path.join(OUT, f"{k}.{ext}")) for ext in ["png","jpg","jpeg"])
        if not found:
            missing.append(k)
    if missing:
        print("⚠ Missing:", missing)
    else:
        print("✓ All asset files present")

    with open(os.path.join(OUT, "credits.json"), "w", encoding="utf-8") as f:
        json.dump(CREDITS, f, ensure_ascii=False, indent=2)
    print("credits.json written")
