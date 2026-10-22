#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build.py — build the RAPTI house-wiring slide decks.

    python3 build.py 1 5 12      # chapter decks
    python3 build.py all         # all 28 chapter decks
    python3 build.py brief       # the merged brief deck (all chapters)
    python3 build.py 1 --pdf     # also write a preview PDF (LibreOffice) to .cache/pdf/
"""
import os, sys, importlib, subprocess
import slidekit as K

TITLES = {
    1: "কর্মক্ষেত্রে নিরাপত্তা", 2: "ইলেকট্রিক্যাল টুলস", 3: "বেসিক ইলেকট্রিক্যাল সার্কিট",
    4: "ইলেকট্রিসিটি বা বিদ্যুৎ", 5: "পদার্থের প্রকারভেদ ও ইলেকট্রিক্যাল প্রতীক", 6: "বেল সার্কিট",
    7: "ইলেকট্রিক্যাল সার্কিট", 8: "মেজারিং ইন্সট্রুমেন্টস", 9: "মাল্টিপ্লাগ সার্কিট",
    10: "সিরিজ বোর্ড", 11: "জয়েন্ট, স্প্লাইস ও সোল্ডারিং", 12: "ফ্যান ও ফ্যান রেগুলেটর",
    13: "টু-ওয়ে ও থ্রি-ওয়ে সুইচ", 14: "হাউস ওয়্যারিং: পদ্ধতি, লে-আউট ও এস্টিমেট",
    15: "সুইচ বোর্ড", 16: "পাওয়ার ফর্মুলা ও ক্যালকুলেশন", 17: "বিদ্যুৎ বিল", 18: "মোটর",
    19: "আইপিএস ও ইউপিএস", 20: "ফ্লোট সুইচ", 21: "বাসবার ও বাসবার ক্যালকুলেশন",
    22: "সার্কিট ব্রেকার ও প্রতিরক্ষামূলক ডিভাইস", 23: "ক্যাবল ও ক্যাবল ক্যালকুলেশন",
    24: "এমডিবি ওয়্যারিং", 25: "এসডিবি ওয়্যারিং", 26: "কন্ডুইট পাইপ ওয়্যারিং",
    27: "চ্যানেল ওয়্যারিং", 28: "আর্থিং ও ওয়্যারিং টেস্ট",
}
SHORT = {14: "হাউস ওয়্যারিং: পদ্ধতি, লে-আউট ও এস্টিমেট",
         22: "সার্কিট ব্রেকার ও প্রতিরক্ষামূলক ডিভাইস"}
SOFFICE = "/root/.claude/skills/synced/ee97b5b7-73bb-4b1a-888f-dc3441c47e09_1dc82599-9150-43f7-8aab-c0aa1ff2f99f/pptx/scripts/office/soffice.py"


def safe(name):
    return name.replace(":", " —").replace("/", "-")


def chapter_path(n):
    return os.path.join(K.CH_OUT, f"অধ্যায়-{K.bn2(n)} — {safe(TITLES[n])}.pptx")


BRIEF = os.path.join(K.OUTDIR, "ইলেকট্রিক্যাল হাউস ওয়্যারিং — সংক্ষিপ্ত স্লাইড (অধ্যায় ১–২৮).pptx")


def run_chapter(d, n):
    mod = importlib.import_module(f"deck_ch{n:02d}")
    d.chapter(n, TITLES[n], short=SHORT.get(n, TITLES[n]), next_title=TITLES.get(n + 1))
    mod.build(d)


def build_chapter(n, pdf=False):
    K.WARNINGS.clear()
    d = K.Deck("full")
    run_chapter(d, n)
    out = d.save(chapter_path(n))
    print(f"✓ ch{n:02d}: {len(d.prs.slides)} slides, {os.path.getsize(out)/1e6:.1f} MB "
          f"— {len(K.WARNINGS)} warnings")
    if pdf:
        to_pdf(out)
    return out


def to_pdf(path):
    od = os.path.join(K.CACHE, "pdf")
    os.makedirs(od, exist_ok=True)
    subprocess.run([sys.executable, SOFFICE, "--headless", "--convert-to", "pdf", "--outdir", od, path],
                   capture_output=True)
    pdf = os.path.join(od, os.path.splitext(os.path.basename(path))[0] + ".pdf")
    print("  pdf:", pdf if os.path.exists(pdf) else "FAILED")
    return pdf


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    pdf = "--pdf" in sys.argv
    if args == ["all"]:
        args = [str(n) for n in range(1, 29) if os.path.exists(f"deck_ch{n:02d}.py")]
    for a in args:
        if a == "brief":
            import mkbrief
            mkbrief.build(pdf=pdf)
        else:
            build_chapter(int(a), pdf=pdf)
