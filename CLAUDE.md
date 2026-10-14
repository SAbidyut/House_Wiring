# CLAUDE.md

## Purpose

Authoring an original **Bangla textbook: "ইলেকট্রিক্যাল হাউস ওয়্যারিং"** for
Resonance Automation Professional Training Institute (RAPTI). Syllabus is
`HW Course Module.pdf` (29 lessons → 28 chapters + appendices, target 400+ pages).
Delivered **one chapter at a time as a .docx**, built by a Python pipeline.

The user is the institute's course developer and reviews each chapter before the
next is started.

## Status

**Chapter number == lesson number in `HW Course Module.pdf`.** The syllabus
order *is* the book order — do not regroup chapters by theme.

| Chapter | Title | Pages | State |
|---|---|---|---|
| 01 | কর্মক্ষেত্রে নিরাপত্তা | 32 | ✅ delivered |
| 02 | ইলেকট্রিক্যাল টুলস | 23 | ✅ delivered |
| 03 | বেসিক ইলেকট্রিক্যাল সার্কিট (১–৫) | 17 | ✅ delivered |
| 04 | ইলেকট্রিসিটি বা বিদ্যুৎ | 21 | ✅ delivered |
| 05 | পদার্থের প্রকারভেদ ও ইলেকট্রিক্যাল প্রতীক | 15 | ✅ delivered |
| 06 | বেল সার্কিট (৬–৯) | 14 | ✅ delivered |
| 07 | ইলেকট্রিক্যাল সার্কিট (সিরিজ/প্যারালাল/মিশ্র) | 24 | ✅ delivered |
| 08 | মেজারিং ইন্সট্রুমেন্টস | 21 | ✅ delivered |
| 09 | মাল্টিপ্লাগ সার্কিট | 18 | ✅ delivered |
| 10 | সিরিজ বোর্ড | 18 | ✅ delivered |
| 11 | জয়েন্ট, স্প্লাইস ও সোল্ডারিং | 24 | ✅ delivered |
| 12 | ফ্যান ও ফ্যান রেগুলেটর | 25 | ✅ delivered |
| 13 | টু-ওয়ে ও থ্রি-ওয়ে সুইচ | 21 | ✅ delivered |
| 14 | হাউস ওয়্যারিং: পদ্ধতি, লে-আউট ও এস্টিমেট | 31 | ✅ delivered |
| 15 | সুইচ বোর্ড | 24 | ✅ delivered |
| 16 | পাওয়ার ফর্মুলা ও ক্যালকুলেশন | 19 | ✅ delivered |
| 17 | বিদ্যুৎ বিল | 19 | ✅ delivered |
| 18 | মোটর | 26 | ✅ delivered |
| 19 | আইপিএস ও ইউপিএস | 36 | ✅ delivered |
| 20 | ফ্লোট সুইচ | 24 | ✅ delivered |
| 21 | বাসবার ও বাসবার ক্যালকুলেশন | 29 | ✅ delivered |
| 22 | সার্কিট ব্রেকার ও প্রতিরক্ষামূলক ডিভাইস | 52 | ✅ delivered |
| 23 | ক্যাবল ও ক্যাবল ক্যালকুলেশন | 49 | ✅ delivered |
| 24 | এমডিবি ওয়্যারিং | 40 | ✅ delivered |
| 25 | এসডিবি ওয়্যারিং | 45 | ✅ delivered |
| 26 | কন্ডুইট পাইপ ওয়্যারিং | 45 | ✅ delivered |
| 27 | চ্যানেল ওয়্যারিং | 32 | ✅ delivered |
| 28 | আর্থিং ও ওয়্যারিং টেস্ট | 49 | ✅ delivered |

Built chapters — figures / tables / worst page-foot gap (all QC-clean):
`ch01` 13/12 · `ch02` 15/13 · `ch03` 11/6 · `ch04` 8/10 · `ch05` 7/6 · `ch06` 8/4 ·
`ch07` 10/9 · `ch08` 11/8 · `ch09` 7/8 · `ch10` 7/7 · `ch11` 15/9 · `ch12` 12/10 ·
(**ch03 is 15 pp since 2026-09-04** — one redundant ব্যবহারিক-কাজ row, already
covered by essay questions গ.১/গ.৫, was dropped so সারণি ৩.৬ stops orphaning a
row onto a near-empty last page.)
`ch13` 12/7 · `ch14` 15/8 · `ch15` 12/8 · `ch16` 6/7 · `ch17` 5/8 ·
`ch18` 9/10 · `ch19` 16/19 · `ch20` 13/10 · `ch21` 14/6 · `ch22` 24/21 ·
`ch23` 17/26 · `ch24` 22/14 · `ch25` 22/14 · `ch26` 30/17 · `ch27` 22/11 ·
`ch28` 24/11 —
no gap > 5 cm (ch11's worst is 3.64 cm after the 2026-08-25 rebuild; ch16 one 4.56 cm, ch18 gaps
of 4.93/4.56/4.55 cm and ch19 one 4.80 cm, see Open
items; ch20 has none above 4.0 cm, ch21 one 4.12 cm; **ch23 has none above 4.0 cm**;
ch03's worst is now 4.26 cm since চিত্র ৩.৩ was rebuilt; **ch24 has none above 3.52 cm**; **ch25 has one 4.37 cm and none higher**; **ch26 has two — 4.28 and 4.11 cm — and none higher**; **ch27 has one 4.55 cm and none higher**; **ch28 has two — 4.77 and 4.60 cm — and none higher**).

Engine API (write a chapter without opening `bookkit.py`): `Book/build/README.md`
Full chapter plan + numbering conventions: `Book/build/BOOK_INDEX.md`
User-facing handbook (Bangla): `Book/পড়ুন — বই তৈরির নির্দেশিকা.md`

## Architecture

Chapters are **generated**, never hand-edited. Three stages:

```
dia_chNN.py  ──► diagrams/chNN/*.svg ──(render.py, headless Chrome)──► *.png
                                                    │
chNN.py ──(bookkit.py)──► out/অধ্যায়-NN — <title>.docx  ◄── assets/chNN/*.png
                                                    │
                              layout.py / qc.py  ──► verification
```

| File | Responsibility |
|---|---|
| `bookkit.py` | DOCX engine: page setup, styles, headings, boxes, tables, figures, OMML math, worked examples. All chapters share it. |
| `svgkit.py` | Measured-layout SVG builder. Measures real text width via Chrome, wraps, auto-sizes boxes, records geometry for collision checks. |
| `dia_chNN.py` | Chapter NN's diagrams. Exports `ALL = [...]`. |
| `chNN.py` | Chapter NN's content. Exports `build()` → `(path, Book)`. |
| `render.py` | SVG → high-DPI PNG via headless Chrome. |
| `qc.py` | Diagram quality gate — text/text, text/graphic, off-canvas. |
| `layout.py` | Converts DOCX→PDF, reports blank bands at page feet. |
| `tune.py` | Optional auto-shrink of figures (rarely used; reordering is preferred). |
| `mkbook.py` | Merges the per-chapter `.docx` into **one delivered book** — full-bleed cover, imprint page, clickable সূচিপত্র, book-wide footer. |
| `dia_cover.py` · `assets_cover.py` | The cover artwork and RAPTI's own logo (from `rapti.net`). |

## Directory map

| Path | Contents |
|---|---|
| `*.docx`, `*.pptx`, `*.pdf` (root) | **Institute's source material** — read-only inputs (facts, photos). Never modify. |
| `HW Course Module.pdf` | The syllabus that defines chapter scope. |
| `Book/` | Deliverables: one `.docx` per chapter + `Kalpurush.ttf` + Bangla handbook. |
| `Book/অধ্যায়-NN/` | Per chapter: preview PDF + `ডায়াগ্রাম-সোর্স (SVG)/`. |
| `Book/build/` | **The pipeline.** Python sources, `assets/`, `.textcache.json`, `BOOK_INDEX.md`. |
| `Book/build/out/`, `Book/build/diagrams/` | Generated; regenerable; not shipped. |

## Source material map

Mined already — do not re-discover:

| Source file | What is in it |
|---|---|
| `HW Course Module.pdf` | The 29-lesson syllabus. Defines chapter order. |
| `H W Course Description.docx` | Same course, *different* numbering — do not use for chapter numbers. |
| `HW 1st class.pptx` | s2–7 safety · s8–12 electricity · s13–20 symbols · s22–26 basic circuits 1–5 · s28 materials · s29–45 tools · s51–53 circuit types · s55–59 **bell circuits 6–9** |
| `HW symbol.pptx` | 36 symbols across 8 slides (already redrawn in `dia_ch05.py`) |
| `Electrical House Wiring book.docx` | Institute's old draft — facts + 210 photos (`word/media/`) |
| `HW Connection Diagram All.pptx`, `Circuit Diagram.pptx` | Wiring diagrams for later chapters |
| `Earthing.docx`, `Motor.docx`, `circuit breaker*.docx`, `Busbar All.pptx`, `Measuring Instruments.docx`, `Solar System.docx`, `SUPER STAR Cables Technical Catalog (FORCE).pdf` | Chapter-specific material for ch08, 18, 21, 22, 23, 28 + appendix |
| `HW Exam Question.docx`, `Electrical House Wiring Quistion.docx` | Question bank for the appendix |
| `angle-holder.jpg` | User-supplied photo (2026-08-25) — the only angle-holder picture anywhere; used by `assets_ch03.py` |

**PPTX traps:** images are usually shape *fills*, not `p:pic` — parse `a:blip`
inside `p:sp` and drop the one hash that repeats on ≥6 slides (page background).
Labels on `HW 1st class.pptx` **s46–50 are wrong** (all say "Hand Saw / Tool Box"
but show power tools) — name those from the photos.

## Tech stack

Python 3 + `python-docx`, `lxml`, `pymupdf`, `python-pptx`, `Pillow`.
External: **headless Google Chrome** (text measurement + SVG raster),
**LibreOffice `soffice`** (DOCX→PDF for verification), ImageMagick.

**No venv ships with the project** — create one on first use:

```bash
python3 -m venv venv && ./venv/bin/pip install python-docx python-pptx pillow lxml pymupdf
```

`Book/build/.textcache.json` (≈2000 measured strings) makes diagram generation
fast; keep it.

## Commands

Run from `Book/build/`:

```bash
python dia_ch07.py                      # generate chapter 7 SVGs
python render.py 'diagrams/ch07/*.svg'  # rasterise to PNG
python qc.py dia_ch07                   # MUST report 0 problems
python ch07.py                          # build the .docx
python layout.py "out/<file>.docx" 4.5  # report page-foot gaps
```

Merging everything delivered so far into one book:

```bash
python mkbook.py                        # → Book/…সম্পূর্ণ বই (অধ্যায় ১–NN).docx
```

**The merged `.docx` is not in git** — it is ~507 MB, over GitHub's 100 MB
per-file limit, and `mkbook.py` rebuilds it in under a minute from the
per-chapter files that *are* versioned. Only the preview PDF is committed.
After adding a chapter, bump the `(অধ্যায় ১–NN)` range in `mkbook.DEST` and
the `assert` on the chapter list, then re-run. The cover art is rebuilt with
`python dia_cover.py && python render.py 'diagrams/cover/cover.svg'` (the
PNG is gitignored like every other rendered PNG, but `mkbook.py` needs it).

## Voice — who is writing this book

**The prose style of chapters 1–11 is already right — do not change it.** The
user confirmed this on 2026-08-13: "ager ta thik e chilo". What is wanted is a
last coat of polish so it reads unmistakably as a person's writing — an
experienced electrical engineer who has taught this trade for years and has
pulled the wire himself. Same register, same formality, same structure; only
the last few machine-flavoured tells get filed off. Treat this as fine-tuning,
never as a licence to rewrite the established style.

This applies **from chapter 12 onward**. Chapters 1–11 keep their current text;
the user will ask for a voice pass over them later — do not retrofit them
unasked.

**Chapters 1–15 had a separate *formality* pass on 2026-08-30** — ch1–10 first,
then **ch11–15 the same way on the user's explicit instruction** ("chapter 11
theke 15 pojonto thik koro… avabe") — the opposite
direction from the humanising notes above. The user found parts had
drifted too informal/chatty ("অপরিহার্য অনুষঙ্গ" → they wanted "গুরুত্বপূর্ণ
উপাদান"; clipped rhetorical fragments; diminutive -টা/-টো; a stray "ভাই"
in ch13; "দোকানে গিয়ে বললে
হয় না"–type asides). What was changed, do not redo or revert:
- Expository prose: chatty/clipped/colloquial lines → graceful formal book
  Bangla (meaning, numbers, IEC/BNBC/BS clauses, figure/table numbers, markup
  all kept).
- Hands-on step lists and worked-example phrasing: তুমি-imperatives
  (লাগাও / যাচাই করো / নির্ণয় করো) → নৈর্ব্যক্তিক ("লাগাতে হবে / যাচাই করতে
  হবে")। Compressing a worked example's `steps=` lines is the layout fix when
  the longer verb forms push a page (used in ch09).
- Learning objectives: "… করতে পারবে।" → "… করতে সক্ষম হবে।" (every chapter).
- অনুশীলনী short/essay/maths questions: তুমি-imperatives → আপনি
  (লেখ → লিখুন, ব্যাখ্যা করো → ব্যাখ্যা করুন, উদাহরণ দাও → উদাহরণ দিন,
  "বলতে কী বোঝ?" → "বলতে কী বোঝায়?")। MCQ stems and the practical-work
  table were left alone.
- Diagram-internal text: ch01 (d07/d10/d11/d13, plus a "প্রকৃত অর্থে"
  trim in d04), ch10 (d05_steps), `dia_ch11` d13_solder_steps (6 sub-lines)
  and `dia_ch14` d10_estimate_steps (6 sub-lines) had তুমি-imperatives;
  converted to নৈর্ব্যক্তিক noun/verbal-noun phrases per the diagram rules
  below. No other ch1–15 diagram carried second-person text.
- Troubleshooting-table "প্রতিকার"/"করণীয়" columns and connection/estimate
  step lists in ch11–15: same তুমি → নৈর্ব্যক্তিক treatment.
- Page counts unchanged: ch1–10 27/20/16/18/14/14/24/20/17/17;
  ch11–15 24/24/19/29/21 (all match the status table). ch04's pre-existing
  4.78 cm p9 gap is unrelated. In ch13 the longer verb forms pushed
  উদাহরণ ১৩.১ off p10 (10.9 cm gap); fixed by merging its `steps=`
  ΔE lines — the standing layout fix.

**Chapters 16–23 got the same formality pass on 2026-08-31** ("baki chaper
15 theke 23 pojonto kore daw" — the user meant a formality pass, not new
authoring; ch15 was already done). Identical treatment, do not redo or
revert:
- Diminutive definite article -টা/-টো/-টে (একটা→একটি, দুটো→দুটি, সেটা→সেটি,
  কাজটা→কাজটি, ওগুলো→সেগুলো, ওটির/ওদের-of-an-inanimate→সেটির/সেগুলোর …);
  loan words that merely *end* in -টার/-টা (মিটার, স্টার, ব্যাটারি, ঘণ্টা,
  কাটা, চেষ্টা, চ্যাপ্টা, এতটাই/অনেকটাই …) left alone. A one-shot helper
  `_formality.py` with a curated word list did the bulk, then `git diff`
  reviewed; it was deleted after.
- Learning objectives "… পারবে।" → "… সক্ষম হবে।" everywhere, including the
  `পারবে**`/`পারবে,` variants the bare regex missed. Body-prose 3rd-person
  "সইতে পারবে"/"বইতে পারবে" is correct Bangla — left alone.
- Step lists, worked-example question/steps, troubleshooting-table
  প্রতিকার/করণীয়/"যা করতে হবে" columns, and ❖/tip/safety box bodies:
  তুমি-imperatives → নৈর্ব্যক্তিক (দেখো→দেখতে হবে, বসাও→বসাতে হবে,
  খোঁজো→খুঁজতে হবে, কোরো না→করা যাবে না, ধরো→ধরা যাক). Box titles that
  were imperatives → আপনি ("মনে রাখো"→"মনে রাখুন", "দেখো"→"দেখুন").
- অনুশীলনী খ/গ/ঘ: তুমি → আপনি (লেখো→লিখুন, করো→করুন, দেখাও→দেখান,
  "করবে?"→"করবেন?"). MCQ stems and the ঙ practical-work tables left alone.
- "ছবি"/"ছবিটি" in body prose → "চিত্র"/"চিত্রটি" (ch18/19/22/23);
  chatty asides removed (ch18 "…বললে দোকানদার হাসবেন", ch19 "…বেচো না",
  ch22 "মজার কথা হলো", narrative "তোমার"→"মিস্ত্রির" where it was an aside).
- Diagram-internal তুমি text: `dia_ch22` d21_select and `dia_ch23`
  d12_steps step labels ("লোড যোগ করো" → "লোড যোগ", "বের করো" → "নির্ণয়",
  "দেখো" → "দেখা"/"যাচাই"); both SVGs re-rendered, `qc.py` clean. No other
  ch16–23 diagram carried second-person rendered text (dia_ch20/21/23 code
  *comments* have "রাখো" — not rendered, left).
- Page counts unchanged: ch16–23 **19 / 19 / 25 / 35 / 24 / 29 / 52 / 49**
  (all match the status table). ch18's 4.93 cm p8 and ch19's 4.80 cm p5
  gaps are the pre-existing Open-items gaps, unchanged. ch23's opener grew
  a page (13 objectives × the longer verb form); reclaimed by collapsing the
  double "সক্ষম হবে" in compound objectives to one trailing form and merging
  উদাহরণ ২৩.১/২৩.২ `steps=` lines — the standing layout fix.

**Chapters 24–28 got the same formality pass on 2026-09-04** ("chapter 24
theke chapter 28 er lekha thik koro… formality maintain kore… jemon chapter 1
theke chapter 23 korecho"). Identical treatment; do not redo or revert:
- Diminutive -টা/-টো → -টি (curated `_formality.py` again, then `git diff`
  reviewed, deleted after): ch24 was still fully in the old chatty register
  (227 changes), ch25–28 were mostly written formal already (78/31/43/79).
  Same loan-word exclusions (মিটার, প্লাস্টার, কাটা, গোটা, উল্টো, চ্যাপ্টার,
  ঘটে/কেটে/ফাটে …); `ওগুলো(তে/র)` → `সেগুলো(তে/র)`.
- Objectives "… পারবে।" → "… সক্ষম হবে।" — **ch24 only** (17); ch25–28
  already used the formal form (0 changes).
- ❖/tip/safety/note box bodies, `b.numbered`/step lists, `worked_example`
  question text, and any procedural তুমি-imperative in a b.para (রেল আগে
  বসাও → বসাতে হবে, মেপে নাও → মেপে নিতে হবে, ধরো → ধরতে হবে, খোলো →
  খুলতে হবে): তুমি → নৈর্ব্যক্তিক. **Body-prose explanatory তুমি/তোমার
  left intact** (ch24 intro "তোমার কাজ সেই নকশা পড়া…" — the deliberate
  trainee address), same call as the ch16–23 pass.
- অনুশীলনী খ/গ/ঘ: তুমি → আপনি (লেখো→লিখুন, বর্ণনা করো→করুন, দেখাও→দেখান,
  "বের করো"→"নির্ণয় করুন", "নেবে?"→"নেবেন?") — **ch24 only**; ch25–28
  exercises were already আপনি. MCQ stems and ঙ practical-work tables left
  alone.
- "ছবি"/"ছবিটি" pointing at a figure → "চিত্র"/"চিত্রটি" (ch24 13, ch25 17,
  ch27 2, ch28 1). Left alone: "কাটা-ছবি" as a caption compound, "ছবির
  ফ্রেম"/"ছবি টাঙানো" (a literal wall picture), "বাস্তব ছবির মতো"
  (photorealistic).
- Diagram-internal -টা text in rendered labels/notes/step strings of
  `dia_ch24`–`dia_ch28` (d04 "টার্মিনাল বার দুটি নিচে", d09 "আট নম্বরটি",
  d13 note "বার দুটি আলাদা", ch25 d17/d18, ch26 d19, ch27 d09/d19, ch28
  d17/d20 …); all SVGs re-rendered, `qc.py` **0 problems** on all five.
  No ch24–28 diagram carried second-person rendered text.
- Page counts unchanged: **38 / 44 / 44 / 32 / 49** (all match the status
  table). ch27's 4.55 cm and ch28's 4.77 / 4.60 cm are the pre-existing
  gaps, unchanged; ch24 still has none above ~3.5 cm. No layout fix was
  needed — the longer verb forms did not push any page.

**Learning-objective variation pass over ALL 28 chapters, 2026-09-04**
("bivinno jaygay sokkhom hobe bar bar lekhso… ektu variant rakho nai… book
lekhar moto formality way te… chapter 1 theke chapter 28 full koro"). The
mechanical `পারবে → সক্ষম হবে` of the earlier passes had left **every**
objective in **every** chapter ending on the identical two words — a machine
tell. Reworked so each chapter's শিখনফল closes with a natural mix, the way a
person writes it:
- **`সক্ষম হবে` kept on just 1–2 weighty/summary objectives per chapter**
  (the whole-hisab line, the nameplate-reading line). Everywhere else varied:
  `… পারবে।` (the workhorse), `… জানবে।`, `… বুঝতে পারবে।`, `… সম্পর্কে
  স্পষ্ট ধারণা পাবে।`, `… আয়ত্ত করবে।`, `… করার দক্ষতা অর্জন করবে।`,
  `… শিখবে।`, `… ব্যাখ্যা করতে পারবে।` — chosen to fit each objective's own
  cognitive verb (knowledge → জানবে/ধারণা পাবে; skill/procedure → দক্ষতা
  অর্জন করবে; identify → চিনতে শিখবে; calculate → নির্ণয় করতে পারবে).
- **Content, numbers, IEC/BNBC clauses and `**bold**` spans unchanged** — only
  the trailing completion (and a few compound `… সক্ষম হবে এবং … সক্ষম হবে`
  collapsed to one). ch28 keeps its no-trailing-`।` style.
- **`bookkit.objectives_box` header changed** `"এই অধ্যায় শেষে শিক্ষার্থী
  যা পারবে"` → `"এই অধ্যায় শেষে শিক্ষার্থী —"` so the em-dash lead-in reads
  cleanly into whatever verb each bullet ends on. One line, applies to all 28.
- One-shot helper `_objvary.py` (28 hand-written lists, regex-substituted the
  `objectives=[…]` block per chapter), `git diff` reviewed, deleted after.
- **Every chapter's page count is unchanged** — verified by rebuilding all 28
  and running `layout.py`; every count matches the status table (27 20 16 18
  14 13 24 20 17 17 · 24 23 18 28 21 · 19 19 25 35 24 · 29 52 49 · 38 44 44
  32 49). ch04 p9 4.78 / ch18 p8 4.93 / ch19 p5 4.80 / ch28 p26 4.77 are the
  pre-existing Open-items gaps, untouched.

Polish towards this:
- **Ground claims in the field, not in the abstract.** Real sizes, real market
  names, what actually goes wrong on site: "বাজারে ১.৫ ও ২.৫ RM তারই বেশি
  চলে", "মিস্ত্রিরা প্রায়ই সুইচ নিউট্রালে বসিয়ে ফেলে". A sentence a working
  electrician would nod at is worth three general ones.
- **Vary the rhythm.** Long explanatory sentence, then a short one that lands.
  Paragraphs of unequal length. Not every paragraph needs a closing summary.
- **Speak to the trainee** now and then (তুমি/তোমার — the book already does),
  and let a warning carry a consequence: "…নইলে ছ'মাস পরে ওই জোড়াই পুড়বে।"
- **Bangla idiom over translated English.** Say it the way an instructor says it
  aloud in class, then keep the English term in brackets once.
- **Admit the messy bits.** Where local practice differs from the standard, or
  where the trade is divided, say so plainly instead of smoothing it over.

File off these tells (they are what keep the prose from reading fully human) —
but only where they actually occur; do not hunt them at the cost of clarity:
- Formulaic scaffolding: "চলুন জেনে নেওয়া যাক", "আশা করি বুঝতে পেরেছেন",
  every section opening by restating its own heading.
- Everything in threes; perfectly parallel, equal-length bullets that say the
  same thing three ways; a tidy summary sentence at the end of every paragraph.
- Empty intensifiers and filler — "অত্যন্ত গুরুত্বপূর্ণ", "উল্লেখযোগ্য
  ভূমিকা পালন করে", "শুধু X নয়, বরং Y" as a reflex construction.
- Dashes as a tic. One em-dash in a paragraph is a pause; four is a signature.
- Hedged, sourceless generalities where a number, a standard clause or a
  workshop example belongs.

Numbers, standards, safety rules and the structural conventions below are
unaffected — only the *prose voice* changes.

**The voice pass stops at the edge of the artwork.** Ch14's diagrams caught
the humanised register and it made them worse — panel headers became opinions
("লুপ-ইন পদ্ধতি — এটিই করতে হবে"), sub-captions repeated the body text
("গরম হলে বা আলগা হলে খুঁজে বের করা যায় না"), and note strips grew into
two-line paragraphs with market commentary. The user flagged this on
2026-08-15. From ch15 the diagram rules are:

- **Panel/box headers are nouns.** "সার্কিট ডায়াগ্রাম", "পিয়ানো বোর্ড" —
  no verbs, no judgements, no "…করতে হবে".
- **Component labels are one or two words.** Keep the English trade term where
  that is what the trade says (`L`, `N`, `E`, `DB`, `SPST`, `5A`, `1M`);
  plain Bangla noun otherwise (সুইচ, বাতি, ফ্যান).
- **One note strip per diagram, one line, a bare fact.** `note_strip()` in
  `dia_ch15.py` raises if the text does not fit on one line — keep that guard
  when copying the file forward.
- **No sub-captions under panels**, and nothing in the artwork that repeats a
  sentence from the body.
- Every *why*, consequence, market habit and warning belongs in the prose. The
  picture shows; the text explains.

## Conventions

- **Formal Bangla book prose.** The institute's existing files are bullet dumps —
  use them for facts and photos only, never as a model for writing or layout.
- **All diagrams are pictures** (vector SVG embedded with a PNG fallback). An
  earlier attempt at native-Word-table diagrams was rejected by the user.
  Word's *Convert to Shape* keeps them editable.
- **When `Circuit Diagram.pptx` / `HW Connection Diagram All.pptx` (or another
  source file) already has the matching circuit, embed that image directly —
  do not hand-redraw it.** Crop the slide at high DPI (`pymupdf`, ≥300dpi,
  autocrop white margin), save into `assets/chNN/`, and place it inside the
  usual `_sheet()`/two-panel wrapper via `SVG.image_fit()` (see `svgkit.py`).
  Pair `Circuit Diagram.pptx` (schematic) into the left "সার্কিট ডায়াগ্রাম"
  panel and `HW Connection Diagram All.pptx` (pictorial) into the right
  "কানেকশন ডায়াগ্রাম" panel — that is exactly the split the institute's own
  two source files already follow. Hand-drawing is fallback-only, for
  circuits with no source slide (e.g. ch06's bell-mechanism cutaway). Verify
  the slide number by extracting each PDF page's text (`page.get_text()`)
  before cropping — a thumbnail contact-sheet is too easy to misread by one
  row, and slide order in these files is not always the final/cleanest draft
  (prefer later, explicitly-titled slides over untitled early ones).
- **If no source slide exists, look for a public-domain textbook before
  hand-drawing.** Anything published in the US before 1931 is PD; archive.org's
  full-text search finds them (`archive.org/advancedsearch.php`). Ch11's joint
  figures all come from John M. Sharp, *Practical Electric Wiring* (1916),
  cropped page-by-page at 400 dpi — see `Book/build/assets_ch11.py` (it
  re-downloads the book, crops by page-fraction, cleans the scan's grey, splits
  multi-row plates, and writes `assets/chNN/credits.json`). Rules that came out
  of that job: autocrop must ignore isolated scan specks (count dark pixels per
  row/column, require ≥4) or a dust mote sets the bounding box; give each band
  its own explicit `(y0, y1)` instead of one shared cut point, so a neighbouring
  figure's tail is excluded from *both* halves.
- **The `❖ চিত্রসূত্র` credit boxes were removed from every chapter on
  2026-08-30 at the user's instruction** ("চিত্রসূত্র part ta sob pdf docx
  file theke delete kore"). The user was told the CC BY / CC BY-SA
  attributions are licence-required and chose to remove them anyway. The
  `assets_chNN.py` scripts and `assets/chNN/credits.json` files are kept as
  the in-repo provenance record; the `creds = json.load(...)` / `b.box(…,
  title="❖  চিত্রসূত্র")` blocks were deleted from ch06, ch11–15, ch18–24.
  Do **not** re-add a credit box to a chapter unless the user asks. Page
  counts dropped by one in ch06/12/13/14/18/19/20/21/22 (box sat on a
  near-empty last page); the status table above reflects the new counts.
- **All data tables are real Word tables**, never images.
- Numbering: `চিত্র N.M`, `সারণি N.M`, equations `(N.M)`.
- **No `§` sign anywhere in the printed text.** The user asked for it
  to be removed on 2026-08-23; a cross-reference is written plainly —
  `২২.৫.৫-এর ব্রেকিং ক্যাপাসিটি`, `২২.৫.৪ দ্রষ্টব্য`. It had crept
  into ch19–ch22 only (17 places); all four were rebuilt, and none
  changed page count. Grep `§` in `chNN.py` before shipping.
- Every chapter ends with সারসংক্ষেপ → পারিভাষিক শব্দ → অনুশীলনী
  (MCQ with answer key + short + essay + practical, plus maths where relevant).
- **Maths in textbook style**: display equations via `Book.math()` (real OMML
  fractions); problems via `Book.worked_example()` →
  প্রশ্ন → প্রদত্ত → নির্ণেয় → সমাধান → উত্তর.
  `worked_example`'s `steps=` go through the math DSL, but `given=`/`find=`
  go through `_rich` (inline markup only) — `P_{1}` there prints literally as
  `P_{1}`. Write plain `P1`, `Ir` in `given`/`find`; keep `_{…}` for `steps`.
- **Numerals: Bangla in prose, Latin inside equations** (`230`, `0.5`).
- Cite **IEC** and **BNBC** wherever a rule has a standard behind it —
  always verify the standard number by web search, never from memory.
- Diagram type sizing: a `W`-px canvas placed `P` cm wide renders `N`-px type at
  `N × P(pt) / W` points. Keep the smallest label ≥ ~7.5 pt. A **portrait**
  diagram cannot be widened to 15.4 cm without becoming ~11 cm tall (which
  opens a page-foot gap) — instead place it ~12.8 cm wide and raise that
  diagram's own type to ~26 px (`T_CALL` in `dia_ch08.py`).
- **Parts-of-a-tool figures:** embed the source photo/meter face and put the
  Bangla labels *outside* the image with leader lines (`callout()` in
  `dia_ch08.py`). `qc.py` treats an embedded image as a graphic rect, so
  text over it is reported — keep labels in the side margins.

## Constraints — do NOT change

- **Never modify the source `.docx`/`.pptx`/`.pdf` at the project root.**
- Do not hand-edit generated `.docx` — change `chNN.py` and rebuild.
- Do not rename delivered chapter files unless the user asks (they link to them).
- Cross-chapter references in prose (`অধ্যায় ২৩ দ্রষ্টব্য`) must match
  `BOOK_INDEX.md`; grep for `অধ্যায় [০-৯]` after any renumbering.
- Body font is **Kalpurush**; it ships in `Book/`. Do not switch fonts.
- Kalpurush lacks `÷` (renders as `+`) — use `\frac` or `/`.
- Kalpurush has **no Unicode subscript digits** (`₁₂₃`, verified against the
  font's cmap) — never paste them into prose, tables or SVG labels. Real
  subscripts come from the math DSL's `_{…}` (OMML `sSub`, added for ch07);
  in body text and diagram labels write plain `R1`, `V1`, `RT`.
- Bengali digits break inside OMML runs under LibreOffice (`২৩০` → `২ ৩ ০`) —
  hence the Latin-digits-in-equations rule. Do not "fix" this by reverting.
- **No Bangla words inside `b.math()` or `steps=`, not even in backticks.** OMML
  drops the spaces between words and splits conjuncts/vowel signs, and the run
  falls back off Kalpurush: `` `ডাইভার্সিটি ফ্যাক্টর` = \frac{`সর্বোচ্চ
  চাহিদা`}{`সংযুক্ত লোড`} `` came out as “ডাইভার্সিটিফ্যাক্টর = সর্বো/চ্চচাহিদা
  … সংযুক্তলো/ড” (ch14 §14.7.3, caught by the user). Write the equation with
  Latin symbols (`DF = \frac{P_{d}}{P_{c}}`) and put the Bangla key in the
  following `formula` box, where it is ordinary body text. Single short words
  with no space survive (ch04 p10's `` `বিল` … `টাকা` `` is legible, just off-font)
  — that is luck, not licence.
- **A fraction's numerator must stay wrapped in `<m:eqArr><m:e>…</m:e></m:eqArr>`**
  (both `m:num` and `m:den`, in `bookkit._math_tokens`). A bare `<m:num>` is
  left-aligned by LibreOffice, so `\frac{1}{2 π f C}` printed its `1` at the far
  left of the bar. `m:phant` padding and `m:ctrlPr` are ignored by LibreOffice;
  the one-row equation array is what makes both Word and LibreOffice centre it.
- The math DSL knows only the commands listed in `README.md` — `\cos`, `\phi`
  and friends are **not** among them and come out as garbage (`cos ii`). Write
  `` `cos φ` `` as upright text instead. `given=`/`find=` are *not* math: a
  `\times` there prints literally, so use a real `×`.
- `svgkit` path parsing must honour **relative** SVG commands; treating every
  number as absolute invents phantom points and produces false QC reports.
- Page-foot gaps are fixed by **reordering content**, not by shrinking figures
  (shrinking destroys label legibility). Word text frames made it worse.

## Workflow for a new chapter

1. Read the chapter's scope in `Book/build/BOOK_INDEX.md` and the syllabus PDF.
2. Mine the root source files for facts and photos (extract images by unzipping
   the Office file; note that PPTX images are often shape *fills*, not pictures).
3. Verify any standard/number by web search.
4. Write `dia_chNN.py`, then `chNN.py`, copying an existing chapter's shape.
5. `qc.py` must be clean, then **look at every diagram PNG** — QC catches
   geometry, not whether a drawing reads correctly.
6. Build, run `layout.py`, reorder to close gaps > ~4.5 cm.
7. Read the produced PDF page by page before delivering.
8. Copy the `.docx`, preview PDF and SVGs into `Book/`, update the status table
   here and in `Book/পড়ুন — বই তৈরির নির্দেশিকা.md`.
9. After the user approves the chapter, back the whole project up to GitHub —
   `git add -A && git commit -m "Chapter NN" && git push`. The remote is the
   private repo `SAbidyut/House_Wiring` (`origin/main`); `gh` is installed and
   authenticated, so no credentials are needed. Do this *after* approval, not
   before — an unapproved chapter should not land in the backup. Ask the user
   before pushing; publishing is theirs to confirm each time.

## Drawing bugs that keep recurring

Check these before rendering — each one shipped once and had to be fixed:

- **A worn item has to sit on the body part it protects** (ch01 review,
  2026-08-24, four figures redrawn).  What went wrong and the rule each time:
  a hard hat drawn as a semicircle *narrower than the skull* on a wide brim
  reads as a bowler perched on top — the shell must be **wider** than the head
  (34S against the head's 30S) and come down over it, with the brim clearing
  the eyebrow.  An ear plug needs an ear to sit in: draw the ear circles
  **before** the head so only the lobe shows, then put the plug at the lobe's
  centre — a callout aimed at bare skin is what the user spots first.  Goggle
  lenses must stop short of the ear or there is nowhere left for the plug, and
  the temple arm goes back *above* the ear.  A mask has to cover the mouth,
  not float on the chin.
- **A dashed "path" line ruled across a drawn face reads as a scratch, not a
  passage.**  Ch01's CPR airway ran from the mouth straight through the closed
  eye and the nose.  Route it through the anatomy it actually follows — mouth,
  jaw, neck, chest — and give it an arrowhead so it reads as flow.
- **Check that limbs and props stop above the ground line.**  The two fingers
  lifting the casualty's chin were drawn straddling the floor.
- **`callout()` must decide which side of its own text the leader leaves
  from.**  Ch10's version always started the leader at `x - 10` for a
  `start`-anchored label, so চিত্র ১০.২-এর "বোর্ড বডি (অগ্নিরোধী PVC)" —
  whose target was up and to the *right* — had its leader ruled straight
  through its own printed words.  `qc.py` passed it (a near-perpendicular
  crossing of a wide text box is under the `graphic_clashes` threshold).
  The fixed `callout()` measures the run with `tw()`, works out the text's
  real span for `start`/`middle`/`end`, and leaves from the edge facing the
  target — or, when the target sits directly above or below the text, from a
  point vertically clear of it.  Same failure as ch02's `part_label()`; keep
  whichever version a new chapter copies forward.

- **A leader that ends at a label’s anchor point runs through the label.**
  `callout()` in `dia_ch02.py` drew the line to `(x2, y2)` and then set the
  text starting at `y2 + 6`, so every "label above the part" leader crossed
  its own sub-line, and a diagonal one crossed the *neighbour’s* sub-line
  (ch02 চিত্র ২.২, caught by the user on 2026-08-24).  `qc.py` cannot see it:
  `graphic_clashes` only reports a stroke whose length *inside* the text box
  exceeds `max(14, 0.28 × box width)`, and a near-perpendicular crossing of a
  wide sub-line is ~20 px.  The fix is `part_label()` in `dia_ch02.py` —
  measure the block first, then stop the leader 9 px clear of its edge.
- **A figure about “read the nameplate” must put the lettering on the object.**
  Ch02 চিত্র ২.১২ drew a stub of a handle and floated the দ্বৈত ত্রিভুজ /
  1000 V / IEC 60900 in white space beneath it, with two callouts that
  repeated the table beside them word for word — so it read as neither a
  tool nor a marking (user, 2026-08-24).  The fix is the ch22 lesson applied
  to a *drawing*: make the handle big enough that the markings are legible
  on it (24 px ≈ 8.2 pt at 14.4 cm — check with `N × P(pt) / W` before
  drawing, not after), print them there, and delete the callouts — the
  table already explains every row.
- **Some tools cannot be drawn in the view the rest of the figure needs.**
  A wire stripper’s notches lie in the tool’s own plane, which is
  *perpendicular* to the wire — so in a side view of the wire the whole
  plier projects onto a vertical sliver, which is why ch02’s stripper read
  as two anvils.  Don’t keep redrawing it: give the tool its own well in
  plan view (handles, pivot, graded holes — holes largest at the pivot) and
  keep the side view for the *cutting edge* alone, in a band labelled as
  magnified.  Ch02 চিত্র ২.৫ is built that way — হাতিয়ার → কাটার
  মুহূর্ত → ফল — and it also closed the dead space the old two-row
  composition left.
- **A caption centred under a symbol will be crossed by any wire that drops
  from it.**  Ch01's d14 ran the fault-current conductor straight down the
  middle of the panel and through the appliance's own caption; `qc.py` passed
  it, because it scores text against rects and paths, not against `line()`.
  The fix that is also better engineering: take the earth conductor out of a
  terminal on the enclosure's **side** and down to an electrode set clear of
  the lettering.
- **Count the holes on a socket face against the plug beside it.**  Ch09's
  `face_socket2` was documented as "দুটি গোল ছিদ্র" but its loop drew a circle
  at two *y* values inside a loop over two *x* values — four holes on every
  ২-পিন socket in চিত্র ৯.১/৯.২ and চিত্র ৯.৩ (the extension board's got six),
  right next to a two-pin plug.  `qc.py` cannot see it; it checks text and
  geometry, not whether a drawn object matches the thing it is named after.
  **The right reference was already in the same chapter**: চিত্র ৯.৪-এর
  সোর্স মডিউল (`assets/ch09/d04_piano_conn.png`) — a narrow portrait module
  with the two holes **stacked one above the other**, each with a small
  shutter tab, which is how the bazar's piano board is actually built.  The
  faces are drawn that way now (two intermediate drafts — side-by-side round
  holes, then side-by-side vertical slots — were both rejected by the user).
  General rule: when a figure's whole job is *recognise this part in a shop*,
  count its features against the real object first — and when the chapter
  already embeds a source photograph of that object, that photograph is the
  reference, not a guess.
- **A circuit symbol has to be drawn inside its own outline.**  Ch10's
  `ac_source()` drew the sine with `M cx-2k … q … q …` where `k = 0.55r`, so
  the wave began at `cx-1.1r` — outside the circle — and ended dead centre;
  it read as a squiggle leaking out of the left of the source.  The wave must
  be symmetric about `cx`: start at `cx-w`, two quadratic humps of width `w`
  each (`w ≈ 0.6r`), control offset `≈ 0.74r` so the crest lands at `0.37r`.
  Check the extreme point's distance from the centre against `r` before
  shipping any symbol drawn inside a circle.
- **Three panels that differ only by a fill colour teach nothing.**  Ch10's
  চিত্র ১০.৭ drew the same intact loop three times and changed only the
  lamp's fill — so "ওপেন" and "শর্ট" were words in a box, not pictures.  It
  now carries the tested device as a box in the return leg with the fault
  drawn inside it: a gap with two red terminals (open), a load rectangle
  (normal), and the same rectangle with a red link bridging it (short).  The
  verdict box below names the state; the artwork shows it.
- **A symbol's decoration must not be given the wire's own lane.**  Ch10's
  `lamp(state="bright")` drew eight rays at 22.5°+45i, i.e. two of them
  almost on the horizontal axis, so both circuit figures that use it broke
  the incoming wire at `r+27` to make room — leaving the lamp floating 27 px
  clear of the conductor with a ray sitting where the wire should be.  It
  read as a collision, and `qc.py` passed it (rays and wires are geometry,
  not text).  The user flagged it on 2026-08-26 as চিত্র ১০.১ and ১০.৭ —
  exactly the only two figures in the chapter with a lit lamp.  Fix: rays at
  30/60/120/150/210/240/300/330°, shortened to `r+9 … r+22`, and the wire
  runs to `r+2` on both sides like the off/dim panels already did.  General
  rule: draw the glow, the spark, the arrow-halo *outside* the axis the
  conductor arrives on, and never widen a wire break to clear decoration.

- **`qc.py` only sees what `svgkit` records in `shapes`** — `rect`,
  `line`, `path`, `circle`.  **`poly()` is not recorded at all**, and an
  `image()` counts only as its own bounding rect.  Ch11's electrician's
  knife (a `poly`) ran through its panel's header chip with QC reporting
  the figure clean.  Anything drawn with `poly()` must be checked by eye.
- **`path()` argument order** is `(d, stroke, sw, fill)` but `rect()`/`circle()`/
  `poly()` are `(…, fill, stroke, sw)`. Passing `"none"` first to `path()`
  fills the shape solid black (broke the socket and bell symbols).
- **Wires must break where a component sits** — draw the loop as separate runs,
  not one rectangle with symbols laid on top (broke the plug, switch and lamp).
- **A stroke through a label** is a defect `qc.py` now catches; a *curve* through
  a label was missed until `_path_points` learned Q/C endpoints.
- Bengali `৪` renders like a Latin `8` in Kalpurush — that is correct, not a bug.
- **`s.text()`'s 7th positional arg is `weight`, not `anchor`.** Writing
  `s.text(x, y, s, size, fill, 700)` and expecting right-alignment silently
  leaves the run left-anchored; the glyphs then start at `x` and overflow their
  container, and `qc.py` reports it as `box edge cuts` on every number in the
  column (ch17 d04's whole money column). Pass `"end"` explicitly.
- `s.fit(bottom, pad)` on every diagram, or the canvas keeps dead space.
- **A "parallel" circuit copied from a working diagram can render in series** if
  the shared node is drawn as one wire chaining component→component instead of
  two independent drops to a common bus (ch06 d04/d06 shipped this — switches
  or loads that should be parallel were literally chained in series, plus a
  disconnected stray wire left over from a half-finished fix). `qc.py` cannot
  catch this — it checks label collisions, not circuit topology. Verify every
  "প্যারালালে" claim in the prose actually matches the wire routing in `circ()`,
  and check both the schematic *and* the pictorial panel — they can disagree
  with each other. **Superseded 2026-08-11:** don't even redraw from a source
  PPTX's geometry by hand anymore — embed the source slide image itself (see
  the Conventions bullet above). This whole bug class (topology invented by
  hand-drawing) cannot happen if the picture is never redrawn. Ch03 and ch06
  were rebuilt this way; also caught along the way: ch06's "emergency alarm"
  circuit is genuinely 2 switches + 2 bells in parallel (`Emergency Alarm
  Circuit` slide), not 1 switch + 2 bells — a content error, not just a style
  one, that hand-drawing had baked in.

## Condensed digest edition (সংক্ষিপ্ত সংস্করণ)

Design spec: `docs/superpowers/specs/2026-09-04-condensed-digest-edition-design.md`.
Built by `sm01.py … sm28.py` + `smkit.py` + `mkdigest.py` + `dia_digest_cover.py`
(all in `Book/build/`), merged into `Book/ইলেকট্রিক্যাল হাউস ওয়্যারিং —
সংক্ষিপ্ত সংস্করণ (গুরুত্বপূর্ণ বিষয়সমূহ).docx/.pdf` — **138 pages** as of
2026-09-05. Same reuse-only rule as the spec: no new diagram art, only real
photos and existing full-book PNGs/SVGs.

**`smkit.dpic()`/`dpics()` were rebuilt on 2026-09-05 — the layout they used
to produce was the bug, not a one-off.** The user's own words: "onek diagram
left e dite giye tumi choto kore felso ar seta dekha jay na" (many diagrams,
by placing them left, were shrunk and can't be read). The original helper
put a diagram in a ~6.6 cm left column beside its explanation text — but a
diagram's embedded labels were drawn to be legible at the *full-book*
placement width (12.5–15.4 cm per this file's `N × P(pt) / W` rule), and
there is no such thing as a legible "medium" width for the same artwork:
below the width it was drawn for, label text drops under the ~7.5 pt floor,
full stop. `dpic()`/`dpics()` now call `b.figure()` at a full-width `width_cm`
(default 13.2 cm, same default as `diagram()`) with the explanation as a
short paragraph *below* the image, not beside it — i.e. `dpic` is now just
`diagram` plus a caption paragraph. This one shared-helper fix propagated to
every chapter that used it (01, 02, 03, 06, 07, 08, 09, 10, 11, 12, 13, 14,
15, 20 — 15 chapters, ~20 call sites) without touching each chapter's prose.
`pic()`/`pics()` (small side-by-side real photos, e.g. PPE identification)
were left alone — those are fine small, the problem was specific to
diagrams and marking/nameplate photos with fine print.
**A source photo whose own aspect ratio is portrait/narrow can still balloon
past a page when forced to the same width as everything else** — ch22's
`ph_mccb_face.jpg` (396×725 px) at 13.2 cm width would render ~24 cm tall.
`dpic()` takes a per-call `width_cm` override for exactly this case; that
one photo is placed at 7 cm (still fully legible — it's a tight label crop)
instead of the section default.

**Chapter 22 (digest) was rebuilt on 2026-09-05** — the user's complaint
("circuit breaker chapter er ey obosta... ey folder onek valo hd quality er
circuit breaker real pic ase... segulo sundro moto crop kore use koro...
sundor style e thik moto all circuit breaker add korba") pointed at
`Book/build/assets/ch22/` — the same Wikimedia-Commons photo set the full
book's ch22 already uses (`ph_mcb_face.jpg`, `ph_mccb_face.jpg`,
`ph_rccb_face.jpg`, `ph_spd_face.jpg`, `ph_br_schneider/abb/legrand/chint.jpg`,
`dev_mcb/mccb/rccb/rcbo/spd/isolator/acb/vcb/mpcb/afdd.jpg` — over 25 real
photos, most unused by the old digest chapter). What was wrong wasn't a
missing folder, it was that the digest only used 7 of them, all squeezed
into the old `pics()` narrow column, with wildly inconsistent apparent size
because a whole-device portrait photo (Schneider, ABB) and a tight nameplate
crop were both forced to the same column width — a portrait photo then
filled most of a page while a wide one left the page half-empty ("ekta bhoro
ekta choto crop kore katso"). Fixed:
- Nameplate photos (MCB/MCCB/RCCB/SPD) → `dpic()`, full width, legible.
- The four-brand comparison (Schneider/ABB/Legrand/CHiNT) → the full book's
  own pre-built gallery asset `diagrams/ch22/d22_brands.png` (already a
  uniform, refined layout — see the ch22 "সুন্দর style" notes above), instead
  of re-doing the same job worse with individual photos.
- **New §২২.৩ "সব ধরনের ব্রেকার ও প্রতিরক্ষা যন্ত্র — এক নজরে"**, reusing
  the full book's own `d23_devices.png` (6 house-DB devices: MCB, MCCB,
  RCCB, RCBO, SPD, আইসোলেটর) and `d24_outside.png` (MPCB, AFDD, ACB, VCB) —
  every breaker/protection type the full chapter covers, not just four.
- `d21_select.png` (7-step selection flow) added to the selection section;
  `d08_curve.png` (B/C/D trip curve) now renders full-width — it was the
  worst offender, unreadable at the old 6.6 cm.
- `d05_inside.png` (cutaway MCB) added to make "বাইমেটাল/সোলেনয়েড" concrete.
- 5 → 9 pages, 0 page-foot gaps above 7 cm after one reorder (tables moved
  ahead of the nameplate photos) and narrowing the two odd-aspect photos.

**The four nameplate photos got the actual marking treatment later the same
day (2026-09-05)** — the previous fix above (`dpic()`, full width) was a
plain, un-annotated crop of the same jpg with the explanation only in the
paragraph below; the user pointed out the full book doesn't do that — it
draws leader-line labels **on the photo itself** (`dia_ch22.photo_callouts()`)
and asked for the same here ("ami chai tumi image er vitor marking kore
dibe..jemon tumi amar full book e kore diyecho"). Fix was a pure reuse, no
new artwork: swapped `dpic(f"{A}/ph_mcb_face.jpg", …)` etc. for the full
book's own **already-annotated output PNGs** — `diagrams/ch22/d07_face.png`,
`d10_mccb.png`, `d13_rccb_face.png`, `d17_spd_face.png` — same source
photographs, already carrying the callouts, at the same width_cm the full
book places them (15.4 / 13.4 / 15.4 / 15.4). No changes to `dia_ch22.py`
or `assets_ch22.py` were needed — this is exactly the "reuse existing
full-book PNGs" rule the digest spec itself sets. Page count unchanged (9);
merged book still 136 pages. **If a later digest chapter shows a raw,
un-annotated nameplate/marking photo via `dpic()` while the full book has
a `photo_callouts()` version of the same image, that is this same bug —
check for an existing annotated PNG in `diagrams/chNN/` before placing the
plain jpg from `assets/chNN/`.**

**That check was then run across every other digest chapter the same day
(2026-09-05)** — the user asked to "follow amar full boro book ta" chapter-
wide, not just for ch22, and to add a few more such marked pictures where
missing. `grep -l photo_callouts dia_ch*.py` found nine chapters carrying
the helper (19–26, 28; ch27 has none). Swapped the raw `assets/chNN/ph_*`
photo for its `diagrams/chNN/dNN_*.png` annotated twin, at the full book's
own width_cm, wherever the digest already showed that same photo plain:
- ch19: `ph_ups_rear.jpg` → `d05_nameplate.png` (UPS rating plate).
- ch20: `ph_cable.jpg` → `d02_parts.png`, `ph_cut_on.jpg` → `d03_inside.png`,
  `ph_contactor.jpg` → `d08_contactor.png`. `ph_cut_off.jpg` (off-state) has
  no annotated twin in the full book and was left as a plain small photo —
  it now reads as "off state (plain) → labelled cutaway showing why."
- ch21: `ph_earth.jpg` → `d08_earth.png`.
- ch23: `ph_xsec.jpg` → `d03_xsec.png`, `ph_sector.jpg` → `d15_sector.png`.
- ch24: `ph_bars.jpg` → `d13_bars.png`, `ph_lug.jpg` → `d14_lug.png`,
  `ph_done.jpg` → `d12_real.png`.
- ch25: `ph_empty.jpg` → `d12_empty.png`, `ph_flat.jpg` → `d17_flat.png`.
- ch26: `ph_mark.jpg` → `d25_mark.png` (the IS 9537 "find of the job" shot).
- ch28: `ph_ir_digital.jpg` → `d18_ir_read.png`.
13 swaps, zero new artwork — every replacement image already existed on
disk from the full-book build.

**Two genuinely new additions, not swaps** — the digest didn't show these
topics in any form, and both are safety-critical enough to be worth the
extra page:
- ch19 gained `d09_batt_label.png` (battery AH/cycle/standby nameplate) next
  to the AH formula in §১৯.২ — directly ties the reading to the formula
  right above it.
- ch23 gained `d09_colors.png` (BNBC-vs-international core colour code)
  plus a condensed সারণি ২৩.১ and the blue-wire-trap ⚠ box — this topic did
  not exist anywhere in the digest chapter before.

**Layout note, ch21 only:** adding `d08_earth.png` (full-width, ~7.6 cm
tall at 15.4 cm placement) stranded উদাহরণ ২১.১ with a 14.45 cm gap two
sections later — swapping the order of `d12_calc.png` and সারণি ২১.২ (table
now after the diagram, not before) closed it *and* dropped the chapter from
7 to 6 pages. The other seven chapters' gaps were all the standard
chapter-opener or section-end pattern already tolerated elsewhere in the
digest (≤7 cm) and needed no reordering.

Page counts: ch19 stays 5pp, ch20 stays 5pp, ch21 **7→6pp**, ch23 stays 5pp
(despite the colour-code addition — the removed pics() width more than made
room), ch24 stays 6pp, ch25 stays 5pp, ch26 stays 4pp, ch28 stays 5pp.
Merged book **136 → 140 pages**, still inside the 145–152 pp spec target.
**The merged `.docx` crossed 100 MB with this batch (98.4 → 148.3 MB)** —
same GitHub per-file limit `mkbook.py`'s own docstring already flags for
the full book's merge; the digest `.docx` is therefore in the same boat and
should not be committed to git (the `.pdf`, 14.2 MB, is fine).

**Every one of the 28 digest chapters (sm01.py–sm28.py) got a full class-9
reading-level language pass on 2026-09-05** — the user's ask, after seeing
the চিত্র ১.৪/১.৬/১.৮ + "দুর্বল কড়ি"→"দুর্বল নিরাপত্তা" fix from the
previous request, was to do the same "sohoj bhasha" treatment across the
*entire* digest book in one pass ("ekbare sohoj kore lekhba... class 9 er
student o bujhe"). This was prose-only — every b.para()/pics()/dpic()
description, box body and a few intro/objective lines were rewritten
sentence-by-sentence into shorter, plainer Bangla (common everyday words in
place of Sanskrit-heavy/formal ones — e.g. "প্রবাহের হার"→"কত জোরে বইছে",
"সুশৃঙ্খল প্রবাহ"→"একদিকে ছুটলে", "অকেজো হয়ে যায়" kept where already
plain). **Left completely untouched, on purpose**: every number, formula,
`b.math()`/`steps=` line, IEC/BNBC clause citation, figure/table caption
number, table cell content (already terse technical terms), and the
objectives' "পারবে/জানবে/সক্ষম হবে/শিখবে" variety from the 2026-09-04
objective-variation pass — this was a register change, not a content
rewrite, and it must not undo either of those two standing passes.
Chapters already carrying custom fixes from earlier the same day (ch06's
uniform-card photos, ch19–ch28's newly-annotated marking images, ch21's
table/diagram reorder) were edited only in their prose paragraphs — none
of those layout fixes were touched or need re-verifying.
- **Method**: read each `smNN.py`, rewrite the dense paragraphs with
  `Edit` (ch01 got a full-file `Write` since nearly everything in it
  needed touching), rebuild, run `layout.py`, and only reorder content if
  a *new* gap above ~7 cm appeared (none did — every chapter's page count
  either held or grew by at most one page from the naturally longer plain
  phrasing).
- **Page counts**: ch01 stayed 6pp; ch02–ch22, ch24–ch28 all held their
  pre-pass counts; **ch23 grew 5→6pp** (the only one) from longer
  connecting prose around the gauge/marking paragraphs — still a clean
  build, no gap above threshold.
- **Merged book: 140 → 141 pages.** This is now just under the digest
  spec's 145–152 pp target band — expected, since simplifying language
  makes sentences longer, not shorter, and this pass was pure rewording,
  not new content (the two content *additions* — ch19 battery label,
  ch23 colour code — were already in from the prior "marking pictures"
  request and are unaffected by this pass). Do not chase the page count
  back up by re-inserting formal phrasing; if the user wants the book
  closer to 145+ again, that has to come from new content, not padding.
- **If a future edit touches any digest chapter's prose again**, keep
  this register — short sentences, common words, technical/English trade
  terms (MCB, ohm, IEC clause numbers, বিদ্যুৎ-family vocabulary) kept
  intact since the book is *teaching* that vocabulary, not avoiding it.

**Chapter 1's fuse safety box got a fresh rewrite on 2026-09-05** — the
2026-09-04 "দুর্বল কড়ি" → "দুর্বল নিরাপত্তা" swap (done on the user's own
explicit instruction) reads awkwardly on its own ("দুর্বল নিরাপত্তা" — a
fuse acting *as* a weak safety-thing — is not really a phrase, unlike
"দুর্বল কড়ি", the actual weak-link idiom it replaced). The user caught
this ("kemon jani kothata") and asked for the whole box rewritten fresh
rather than patched again. New wording keeps the same fact (a fuse is
deliberately the weakest point so it fails first) without either the
stiff idiom or the awkward substitute: "ফিউজের বদলে কখনোই তামার তার বা
পেরেক লাগানো যাবে না। বিপদ এলে যেন ফিউজটাই সবার আগে পুড়ে যায় — এই
জন্যই একে ইচ্ছা করে সবচেয়ে দুর্বল জায়গা রাখা হয়। ফিউজ মোটা করে দিলে
বিপদের সময় বাঁচানোর আর কোনো উপায় থাকে না, তখন পুড়বে ঘরের আসল তার."
Page still 7 in the merged book.

**The merged digest book's header now shows the current chapter's name on
the right side of every page, 2026-09-05** — the user asked for this book-
wide ("pura boi er proti page er dan pashe chapter name"). The standing
constraint (documented above, under "What mkbook.py had to work around")
is that **docxcompose drops every appended chapter's own `sectPr`**, so
the merged file is one continuous section and cannot carry a real
per-chapter header/footer the way each standalone chapter docx does. The
fix does not fight that constraint — it uses Word's own mechanism for
exactly this problem, a **STYLEREF field**, which needs only one section:
- `bookkit.Book._setup_styles()` now registers a paragraph style named
  **`RaptiChapterTitle`**, added once per document (guarded by a
  `if "RaptiChapterTitle" not in [...]` check so re-running `_setup_styles`
  is idempotent). `chapter_opener()` applies this style to the chapter-title
  paragraph inside its navy title-block table cell (`p1`) — deliberately
  **not** reusing `"Heading 1"`, because `b.h1()` already uses that style
  for every in-chapter section heading (`১.১`, `১.২`, …); if the STYLEREF
  target were `"Heading 1"` the header would show the *nearest section*
  title, not the chapter title, and it would change every time a new `h1`
  section starts partway down a chapter.
- `mkdigest.py`'s header-building code (`build_front()`) now puts
  `field(hp, 'STYLEREF "RaptiChapterTitle" \* MERGEFORMAT', …)` on the
  right side of the tab stop, replacing the old static institute name
  there; the book title stays static on the left. `enable_update_fields()`
  was already being called on the final merged doc (for the TOC's
  `PAGEREF` fields) and covers this field too — no separate wiring needed.
- **This is a shared `bookkit.py` change**, so every standalone full-book
  `chNN.py` chapter now also carries an (unused, invisible) "RaptiChapterTitle"-
  styled paragraph in its own opener — harmless, since `mkbook.py`'s header
  code was not touched and still uses each chapter's own hardcoded
  `build_header_footer()` header (which is already correct per chapter
  in a standalone build). If `mkbook.py`'s merge ever wants the same
  running-header trick for the *full* book, the style is already there to
  reuse — just add the equivalent STYLEREF field to its front-matter
  header code.
- **Verified working in LibreOffice's headless PDF export** (the same
  renderer `layout.py`/preview conversions already depend on) with an
  isolated two-chapter test docx before touching the real book — STYLEREF
  correctly tracked the nearest preceding `RaptiChapterTitle` paragraph
  across page and chapter boundaries. In the real merged book, checked
  page 2 (imprint, *before* chapter 1's own title paragraph — LibreOffice
  falls back to the *next* occurrence forward when nothing precedes,
  landing on "কর্মক্ষেত্রে নিরাপত্তা", which reads correctly for a book
  that hasn't started chapter content yet) through page 141 (last page,
  "আর্থিং ও ওয়্যারিং টেস্ট") — every sampled page's header matched its
  actual chapter.
- All 28 chapters were rebuilt (bookkit.py change only, no chNN.py/smNN.py
  content edits needed beyond the sm01.py fuse-box rewording) and the book
  re-merged: still 141 pages.

**Digest `mkdigest.py` — সূচিপত্র + running-header fixes, 2026-09-06** (user:
"rapti.net right e jay nai · index e page number nai · index e shudu chapter,
ami proti section chai"). All three fixes are in `mkdigest.py` only — no
chapter or `smkit` change, and `mkbook.py` (full book) is untouched:
- **Running header: the bug was never the title length, it was a *style*
  tab stop.** The header is one line, three columns — book title (left) ·
  STYLEREF chapter number + title (centre) · `rapti.net` (right) — and
  `rapti.net` was landing mid-page. Cause: the paragraph is
  `S.header.paragraphs[0]`, which carries `pStyle="Header"`, and the
  built-in **Header style defines its own tabs (centre @4680, right @9360
  twips)** which OOXML *merges* with the paragraph's own. So the merged
  stop list was centre@4680, centre@5458(ours), right@9360, right@9411 —
  the first `\t` hit the style's centre stop and the second hit **our**
  centre stop, so `rapti.net` was centred at 5458 twips instead of
  right-aligned at 9411. **Fix: `hp.style = "Normal"`.**
  `tab_stops.clear_all()` clears only paragraph-level stops and does
  nothing to a style's — it is not enough on its own. Centre tab is now
  `cw/2` (a true column centre); measured in the built PDF, every chapter
  title's midpoint lands on 303.4 pt and `rapti.net` ends on 538.7 pt (the
  exact right text edge) on every page. There is ample room: longest title
  (ch22) is 157 pt against a 470 pt column, so one line holds all three.
  *A two-line header was tried first (title+rapti.net on line 1, chapter
  on line 2) and reverted — the user wants the chapter name centred.*
  (Same latent style-tab bug sits in mkbook.py's INST_BN header — not
  fixed, not asked.)
- **সূচিপত্র now lists every `b.h1()` section under its chapter**, indented,
  dotted leader, own page number. `chapter_sections(path)` reads each
  `সংক্ষিপ্ত-NN.docx`'s `Heading 1` paragraphs whole (e.g. `১.১  …`);
  `inject_section_bookmarks(cdoc, n)` wraps the k-th such paragraph in
  bookmark `_chNN_sK` during the merge (identical filter+order so k lines
  up with the TOC); each sub-line is a `PAGEREF _chNN_sK \h`. 28 chapters +
  **94 sections** = 122 anchors; সূচিপত্র is 4 pages now (was 1) so
  chapter 1 opens on p7. The "অনুশীলনী — বহুনির্বাচনী প্রশ্ন" h1 that
  `smmcq.py` adds to every chapter is one of the 94 and shows in the TOC
  (the imprint's "কোনো … অনুশীলনী … নেই" sentence is now stale — left as-is).
- **সূচিপত্র page numbers are baked in as STATIC TEXT — the `PAGEREF`
  fields are deleted, not just filled.** A live `PAGEREF … \h` is only as
  good as the reader's viewer: LibreOffice resolves it on PDF export, but
  Word/Pages/web viewers each do their own thing on open — leaving the
  cached `০`, or recomputing without paginating and printing **1** on
  every line (the user saw both, in that order). A generated book gains
  nothing from a live field; the numbers are recomputed from scratch on
  every build anyway. So `bake_toc_numbers(DEST)` round-trips a throwaway
  copy through `soffice --convert-to docx` (which computes every field),
  regex-reads each `PAGEREF _chNN[_sK]` → page out of the round-tripped
  `document.xml`, writes that number (`bn()`, Bangla) into the shipped
  file's field-result run, and then **removes the begin / instrText /
  separate / end runs around it**, leaving one ordinary styled run. After
  the pass `document.xml` contains **zero `PAGEREF` and zero `fldChar`**;
  the only fields left in the book are the header's STYLEREF and the
  footer's PAGE, both of which every viewer handles. The round-trip copy
  is discarded — the shipped `.docx` stays python-docx's own output. Runs
  after `enable_update_fields`, before the `--pdf` render.
- **`bake_toc_numbers` fails soft, and that bit once.** If the LO
  round-trip produces nothing it prints a warning and returns, and the
  build carries on to the PDF — so a *silent* skip is possible. It
  happened here: the disk hit ENOSPC mid-build, LO wrote nothing, the
  bake no-opped and the shipped docx still had all 122 placeholders while
  the PDF was fine. **Check the `bake:` line in the build output**, or
  grep the saved docx for `PAGEREF` (should be 0). Re-running the bake
  alone is safe and cheap — `python -c "import mkdigest;
  mkdigest.bake_toc_numbers(mkdigest.DEST)"` — the PDF does not need
  re-rendering, since LO computed the same numbers either way.
- Rebuilt `python mkdigest.py --pdf`: **184 pages** (was 181; +3 = the
  longer TOC). Verified in the PDF — chapter title centred on 303.4 pt
  and `rapti.net` ending on 538.7 pt on every sampled page incl.
  ch14/22/28; every TOC line's link target and its printed number agree;
  STYLEREF still tracks the right chapter. `.docx` scan: 122 static
  Bangla page numbers, 0 PAGEREF, 0 fldChar in the body.
- **sm01.py wording**, same request: the fuse ⚠ box's "এই জন্যই একে ইচ্ছা
  করে **সবচেয়ে দুর্বল জায়গা** রাখা হয়" → "… ইচ্ছা করে **দুর্বল করে** রাখা
  হয়"। (Third pass over this one sentence — see the 2026-09-05 note above;
  leave it alone now.)

**Disk note:** the merged digest is a **153 MB** `.docx`, and
`bake_toc_numbers` briefly writes a ~68 MB LO round-trip copy on top of
that plus the 16 MB PDF — budget ~250 MB free before running
`mkdigest.py --pdf`, or the bake will skip silently as described above.

**Digest chapters 22, 23 and 28 got three separate, unrelated fixes on
2026-09-05** ("earthing korar prokar add koro nai... ata add koro... ar
cable er chapter e cable er rm re se avabe... sundor vabe sajaya dio... ar
chapter 22 e ja dibite bose na... ey part ta kete daw"), in one batch:

- **sm28.py was missing an entire method-of-earthing section.** The digest
  had ২৮.১ (system, four parts, BNBC minimum sizes, pit) and what became
  ২৮.৩ (the four wiring tests), but never explained *how* a rod, pipe or
  plate is actually installed, or the charcoal-and-salt backfill practice —
  content the full book carries as `ch28.py`'s ২৮.৩ "আর্থিং করার পদ্ধতি".
  Added as a new **২৮.২ "আর্থিং করার পদ্ধতি"** with four h2 subsections
  condensed from that source: ২৮.২.১ রড আর্থিং (the pilot-GI-pipe
  technique — a 38 mm GI pipe is driven 4 m and withdrawn first so the
  12.5 mm copper rod slides in straight to 3 m, because a rod driven
  directly mushrooms at the head and bends), ২৮.২.২ পাইপ আর্থিং (BNBC's
  own tube-well recommendation, 12.19–24.38 m = 40–80 ft, which is *why*
  pipe earthing dominates in Bangladesh — the rig and the labour already
  exist everywhere), ২৮.২.৩ প্লেট আর্থিং (worst option at equal cost —
  ~10 Ω against a rod's ~7 and a pipe's ~3 — with the reused figure
  `d03_electrodes.png`), and ২৮.২.৪ চারকোল ও লবণ (works, but salt washes
  out over seasons and corrodes GI zinc plating; IS 3043 weights site
  selection higher than backfill chemistry). Cites BNBC ১.৩.৩৭.৩.৩ (the
  three electrode types) — the existing chapter already had ১.৩.৩৭.১–৩.৫
  verified from an earlier session, reused here rather than re-verified.
  The old ২৮.২ "ওয়্যারিং শেষের চারটি টেস্ট" renumbered to ২৮.৩; one
  objective and two সারসংক্ষেপ bullets added for the new section.
  **A page-foot gap this introduced was fixed with the standing
  playbook**: the rod-resistance worked example was moved *before* the
  আর্থ ইলেকট্রোড reference table (a worked example is one unsplittable
  block and was stranding empty space when it fell after a table that
  could otherwise flow across the page break) — same fix applied
  independently in sm23.py below. Chapter is 6 pages and `layout.py`
  reports zero gaps above threshold.
- **sm23.py's `re`/`rm`/`se`/`sm`/`G`/`X` codes were buried in one dense
  running paragraph.** Replaced with a short lead-in sentence plus a new
  reference table ("ক্যাবলের গায়ের কোড যেভাবে পড়বেন") listing all six
  codes and their meanings side by side — same content, easier to scan,
  matching how সারণি ২৩.১/২৩.৩/২৩.৪ already present similar lookup facts
  in this chapter. **This also surfaced and fixed a pre-existing 11.13 cm
  gap** on the page carrying সারণি ২৩.৫ (the ampacity/mV-per-A-per-m
  table) — উদাহরণ ২৩.১ is one unsplittable block and did not fit the
  space left after that table, stranding the whole page; moved the
  worked example *before* the table (table now trails and can flow across
  the page break instead). Chapter stayed 6 pages; `layout.py` clean.
- **sm22.py's §২২.৩ used to end with a paragraph + `d24_outside.png`
  diagram about MPCB/AFDD/ACB/VCB** — devices that do not sit in a house
  distribution board (motor starters, LT panels, 11 kV substations). Cut
  entirely on the user's instruction ("ja dibite bose na... kete daw"),
  along with the matching সারসংক্ষেপ bullet; the six-device
  `d23_devices.png` gallery (the devices that *do* sit in a house DB)
  stays. Chapter went 9→8 pages; the two remaining gaps (4.56 cm on the
  opener page, 6.37 cm before চিত্র ২২.৭'s brand gallery) are both under
  the digest spec's ">~7 cm" action threshold and were left alone.
- All three rebuilt, `layout.py`-checked, and the whole book re-merged:
  **141 → 142 pages** — still under the 145–152 pp target band (see the
  standing note above: only new content closes that gap, not padding).
  Spot-checked the merged PDF directly: the earthing-methods section,
  the cable-code table and the ch22 removal all landed correctly, and the
  running STYLEREF header still tracks the right chapter name through the
  new page count.

**Chapter 21 (digest) was rebuilt on 2026-09-05** — the user's ask:
"bus bar er calculation amon obosta keno... sundor kore with diagram soho
sundor moto calculation kore dekhaw... like amphere rating dewa thakbe...
kemon size er busbar lagbe seta ber korbe." The old §২১.২ had **zero
diagrams** and its one worked example ran the *wrong* direction (given W×T,
find I — a lookup, not a design problem). Fixed:
- Added three diagrams, all reused from `diagrams/ch21/`: `d01_why.png`
  (wire-joint chain vs busbar tap — the "why" from §২১.১), `d04_dims.png`
  (W/T/A labelled), `d12_calc.png` (the load→diversity→current→area→size
  flow chart — this is also the corrected form of the institute's own
  slide-7 formula, which had kVA multiplied by 1000 instead of divided;
  see the "verified from the sources" note lower in this file).
- New §২১.৩ "লোড থেকে কারেন্ট, কারেন্ট থেকে মাপ" replaces the old এক-দিকের
  worked example with the real design chain — 250 kW connected → 0.7
  diversity → 3-phase current (297 A) → A = I/J → BNBC ১.৩.৯.৩.৮'s +20%
  spare → pick the next standard size from a table. Same verified numbers
  as the full book's উদাহরণ ২১.২ (see the ch21 arithmetic note above) —
  not re-derived, just condensed.
- New সারণি ২১.২ — a 7-row sample of the full book's সারণি ২১.৩ (28 market
  sizes), imported as data (`J_CU`/`J_AL` from `ch21.py`) rather than
  retyped, so it can't drift from the full book's numbers.
- 3 → 6 pages, 0 page-foot gaps above 6 cm (one reorder: the calc-flow
  diagram moved from after the worked example to before it).

**Chapter 3 (digest) §৩.৩ was switched from `dpics()` to `pics()` on
2026-09-05** (user: "3.3 er diagram gulo besi boro hoye gese..egulo left ey
rakho") — the five stacked full-width circuit photos ran the section long,
and unlike a drawn SVG diagram these are real pptx-slide crops with only
2–4 huge bold word labels ("2 Pin Plug", "Light", …), so shrinking them to
`pic()`'s small-photo-beside-text layout costs no legibility (checked: the
smallest label still prints comfortably above the 7.5 pt floor at
`img_cm=7.5`, this file's own `N × P(pt) / W` rule). **This is a deliberate
exception, not a reversal of the 2026-09-05 dpic() rebuild** — that fix
stands for every *drawn* diagram with fine embedded labels; `pics()` was
already the right tool for a plain identification photo (see `smkit.py`'s
own docstring) and these five circuit crops are exactly that.
**Caught while doing it: four of the five captions did not match their own
images** — d06/d07/d09's digest descriptions described lamps, second
switches and a neon indicator that are not in those pictures at all (the
full book's own চিত্র ৩.৬/৩.৭/৩.৯ text, for the same five image files, was
correct throughout). Rewritten to match the actual pictures, reusing the
full book's own accurate descriptions condensed. **General rule, again:
read what a caption claims against the picture itself before shipping it.**

**Chapter 6 (digest) got the same treatment on 2026-09-05** (user: "6.1 er
por page ta faka..ar image gulor crop size soman kore daw..ar 6.2 er image
gulo left e niye sundor moto description kore daw"), plus one new fix:
- **§৬.১'s blank page was reordering, not a legibility problem** — the
  intro paragraph left about half a page, and the single full-width
  `diagram()` call (d01_bell_parts.png, a two-panel গঠন/কার্যপ্রণালি figure)
  couldn't fit in what was left, so LibreOffice pushed the whole image to
  the next page and stranded page 1 half-blank. Fix: moved the `pics()`
  block of four small bell-type photos *before* the big diagram — those
  four rows can split across the page boundary (each is its own table row),
  so they absorb the leftover space and the big diagram starts clean on the
  next page. 6 pages → 5, no more stranded blank page.
- **"crop size soman kore daw" — the four bell photos' raw aspect ratios
  ranged 0.51 to 1.11**, so at the same `pic()` width their row heights in
  the table looked wildly inconsistent (ph_bell_gong nearly 2.5× taller
  than ph_bell_open). Real fix lives in `assets_ch06.py`, not sm06.py — a
  new `_pad_card()` helper pads each onto a light `#F7FAFC` card with a
  thin border at a common **0.875 height/width ratio**, chosen close to
  the two photos that were already near it (single 0.855, buzzer 0.894) to
  minimise padding on those two. Padding, never cropping — ph_bell_open's
  subject already runs edge-to-edge (contact screw on the left, gong on
  the right), so trimming width to change its ratio would have cut off
  half the point of the photo. Applied only to the four names in
  `UNIFORM_CARD` (the ones §৬.১ actually uses); ph_chime/ph_alarm are
  unused by any chapter and left alone.
- **§৬.২'s five circuit images were not all safe to shrink alike.** d03–d06
  (সাধারণ কলিং বেল, দুই স্থান থেকে বেল, সিরিজ বেল, ইমার্জেন্সি অ্যালার্ম)
  carry only 3–7 big bold word labels each ("Source", "Switch 1", "Bell 2"
  …) — measured, comfortably legible shrunk to `pic(img_cm=8.5)`. **d07
  (ইন্ডিকেটরসহ কলিং সিস্টেম) is different — three repeats of "Switch" and
  "Light" packed into one row make its smallest label ≈7.5 pt even at the
  *current* full 13.2 cm width**; shrinking it to 8.5 cm the way the other
  four were would have put it under 4.5 pt. Left as a single full-width
  `dpic()`. **General rule for this whole `dpics()`→`pics()` conversion,
  chapters 3 and 6 both: check the image's own busiest/smallest label
  before shrinking it, not just how many words the whole figure carries —
  a diagram with one dense row can fail the floor while its siblings in
  the same section are nowhere close.**
- Digest chapter 6: 6 pages → 5; merged book 137 → 136 pages.

**Remaining page-foot gaps after the full 28-chapter rebuild**: 21 of 28
chapters are clean; 05, 06, 10, 13, 24 have one gap each in the 7–9 cm
range and 26, 28 one each at ~10–11 cm — none chased further (2026-09-05
session ran out of scope for it; the digest spec itself only asks to fix
gaps ">~7 cm" and these are photo/example placement, not legibility).
Total merged page count **138**, comfortably inside the spec's 145–152 pp
target with room to spare. **Superseded** — ch28's gap in this list was
closed later the same day when the আর্থিং করার পদ্ধতি section was added
(see the "three separate, unrelated fixes" entry above); the page count
has also moved since (marking swaps, class-9 pass, these three fixes —
**142** as of the last merge). This paragraph is kept as the historical
snapshot of that specific rebuild, not the current state.

## Accuracy review of the digest, 2026-09-05 (fixes applied to BOTH books)

The user asked for a full read of the merged 142-page digest — "aro sohoj kore
lekha jay kina · kothaw kono information vul ase kina · kothaw kono kisu add
kora uchit kina" — then asked for every finding to be fixed.  All 20 landed;
**do not re-derive or revert any of them.**

**The one that mattered: BNBC 1.3.12.2 vs ch14's cable table.**  ch14 said a
16–20 A geyser/AC circuit takes **4 mm²** citing 1.3.9.3.6; ch22 said **20 A →
6 mm²** citing 1.3.12.2.  Both books shipped the contradiction, and the model
flat's two AC circuits (C8/C9, 20 A) were drawn on 4 mm².  **1.3.12.2 was
extracted from the source PDF and is explicit** — 5A→1.5, 10A→2.5, 15A→4,
**20A→6**, plus "the minimum size of cable … shall depend on the rating of the
fuse or circuit breaker".  1.3.9.3.6 gives *no* cable size at all (it is the
"separate branch circuit for ≥500 W fixed appliances" clause), so ch14's
citation was wrong too.  Fixes: ch14's table row split into 16A/4 and 20A/6
citing 1.3.12.2; `dia_ch14.d09_circuits` C8/C9 → 6 mm²; the estimate table
split into a 4 mm² row (sockets+geyser, 2 coils) and a 6 mm² row (two ACs,
2 coils); a paragraph added explaining that **16 A is read against the code's
15 A row but 20 A is its own row** — same 1500 W load, different cable,
because the ladder is keyed to the breaker not the load.
**BNBC also writes 15A, not 16A, for socket circuits (1.3.9.3.12)** — the
socket rows now read "১৫–১৬A".

**Other content errors fixed (all were in the full book too unless noted):**
- **ch12 fan rotation.**  Digest said three times "স্টার্টিং কয়েলের দুই প্রান্ত
  অদলবদল করলে দিক উল্টে যায়" — impossible on a 3-lead ceiling fan, and the
  chapter's own figure shows only C/R/S.  ch12.py §১২.৫.১ had already been
  corrected to **move the neutral from R to S**; the summary and the
  troubleshooting row had not.  All now say R→S.  (ch18's version of the
  sentence is about 4-lead motors and is **correct** — left alone.)
- **ch17 উদাহরণ ১৭.১** claimed the fans eat "বাতির সাতগুণ"; 45 ÷ 8.64 = 5.2.
  Now "চার বাতির পাঁচগুণেরও বেশি".
- **ch18 সারণি ১৮.৩ vs ch20** — 2 HP printed as 10.2 A in one place and 10.9 A
  in the other.  The table is a market table whose implied efficiencies rise
  with size (0.64 / 0.70 / 0.75 / 0.78 at cos φ 0.85 — recomputed and
  realistic); ch20 computes at the 1 HP motor's 0.70.  Both are right; a note
  under the table now states the assumption and names the 10.2-vs-10.9 gap.
  **Do not "fix" the table to one number.**
- **ch28 soil resistivity.**  Digest kept the full book's ρ = 20 worked example
  and 7/3/10 Ω table but the *prose* said "বাংলাদেশের পলিমাটি প্রায় 5 ওহম-মিটার,
  তাই 1 ওহম নাগালের মধ্যে" — so p137 promised 1 Ω and p139 said one rod can
  never reach it.  The full book separates them (`RHO_DRY, RHO_WET = 20, 5`).
  Digest now labels both, marks the example and table as **শুকনো মাটি**, and
  carries the payoff the full book has: same rod in wet alluvium = 1.74 Ω,
  two in parallel = **0.87 Ω**.
- **ch18 troubleshooting** — "পাম্প ঘোরে কিন্তু পানি ওঠে না" listed *প্রাইমিং নেই*
  as a cause but only "স্টার্টিং কয়েল উল্টে দিতে হবে" as the remedy.  Prime first.
- **ch1 safety shoe (digest only)** — "সামনের দিকে লোহার আবরণ থাকে" next to
  "বিদ্যুতের শক থেকে বাঁচায়".  EH-rated boots use a **composite** toe cap;
  rewritten to say so.  The full book never carried this sentence.
- **চিত্র ৫.৪'s caption** promised MCB and RCCB symbols; that sheet
  (`d05_symbols_safety`) has neither.  Caption now names what is actually drawn.
- **চিত্র ৬.৪ (digest)** was captioned "বাজার (বাজার)" → "বাজার (Buzzer)".
- **sm21's উদাহরণ ২১.১** had `find=["ব্রেকিং/রেটেড কারেন্ট …"]` — it computes the
  load current, nothing to do with breaking capacity.
- **sm07's "লক্ষ করো"** was the last surviving তুমি-imperative in all 28 digest
  chapters (the 2026-08-30/31/09-04 formality passes missed it).
- **Socket rating was three different numbers** — 13A (ch14 legend, ch15), 15A
  (ch16), 16A (ch14 table, ch22, ch23).  ch16's aside now says "13 A বা তার
  বেশি … সকেট এবং নিজস্ব 16 A সার্কিট"; ch14's table says 15–16A.
- **ch22 উদাহরণ ২২.১** jumped 10.9 → 16 A with no mention of **13 A**, which is
  in IEC 60898-1's series.  The note now says 13 A would do but is not stocked here.

**Content added (each was promised somewhere and never delivered):**
- **ch1's পাঁচটি সোনালি নিয়ম** were named in the objectives, the §১.৩ heading and
  the সারসংক্ষেপ but **never listed anywhere in the digest**.  Added as one
  arrow-sequence sentence plus `diagrams/ch01/d07_five_rules.png`, which already
  existed on disk from the full-book build — no new artwork.  A five-item
  numbered list was tried first and **reverted**: the diagram's own sub-lines say
  the same five things, so the pair read as duplicate on facing pages (the
  standing "nothing in the artwork that repeats a sentence from the body" rule,
  read the other way round), and the list left a 6.32 cm gap on p5.  Sentence +
  diagram closes the gap and removes the repeat.  ch01 6 → 7 pp, no gap > 4 cm.
- **ch1 §১.৪ did not exist** — the আর্থিং block was a `b.h4()`, so the chapter
  ran ১.১ ১.২ ১.৩ ১.৫.  It is `b.h1(…, "১.৪")` now.  (sm01 was the only digest
  chapter with a numbering gap; the other 27 were checked.)
- **ch1 সারণি ১.২ skipped fire class D** (A B C **E** F), which reads as a typo.
  Restored from the full book.
- **ch8 CAT rating** — the objective says "যাচাই করতে পারবে" and the summary
  repeats it, but the chapter never said what CAT II/III/IV are.  The full
  book's box (`ch08.py:365–367`) is reused.
- **Wire colour was contradictory for 95 pages** — ch3/ch4 taught IEC 60445
  brown/blue with no caveat, ch15/ch21 taught BNBC red/black, and only ch23
  (p115) reconciled them.  ch3's ⚠ box and ch4's summary bullet now name both
  and point at অধ্যায় ২৩.

**Language (the class-9 register pass had left a handful):**
পরিপার্শ্ব→চারপাশের তাপমাত্রা (sm23) · ধর্তব্যই নয়→ধরাই হয় না (sm21) ·
ঊর্ধ্বে→বেশি (sm17) · সমষ্টি→নিয়ে গঠিত (sm15) · নিরবচ্ছিন্নতা→একটানা চলা (sm19).
Also **sm04's সারসংক্ষেপ still said "সুশৃঙ্খল প্রবাহ"** though the body had been
simplified to "একদিকে ছুটলেই", and **"কত জোরে" was used for both current and
power** — current is now "কত ইলেকট্রন বয়ে যাচ্ছে", power "প্রতি সেকেন্ডে কত
বিদ্যুৎ খরচ".

**Diagram work, and two traps worth keeping:**
- `dia_ch14.d05_loop_in` still carried the exact panel header the user flagged
  on 2026-08-15 — "লুপ-ইন পদ্ধতি — **এটিই করতে হবে**" — plus two sub-captions
  repeating the body.  The ch15-onward rules were applied at last: headers are
  plain nouns, one bare fact line per panel, verdict in the note strip (the
  red/green already carries it).  PH 456 → 420.
- **`d09_circuits` was printing its cable column as "8 mm²"** — that was Bangla
  ৪, and the main breaker "৪০A" read as **80A**.  In a column the reader adds
  up, that is a different number, not a curiosity (the ch23/ch24 rule).  Every
  engineering figure in that diagram is Latin now.
- The same figure was **11.2 cm tall at 15.4 cm and its T_TINY is already
  7.04 pt**, so it cannot be narrowed.  Compacted vertically instead (two spare
  rows → one row with two dashed boxes; note strip shortened to one line;
  `y` 242→238) → 10.1 cm.  **GAP 54→46 was tried and reverted** — the amp
  labels sit at `y − 25` and collide with the previous row's MCB box below
  GAP ≈ 50 (`qc.py` caught it as 10 `box edge cuts`).
- **Closing ch14's gap took four attempts and confirms the ch17 lesson.**
  Figure after the colour para → 9.71 cm; before the new para → 11.98; after
  §১৪.৭.২'s intro → **clean**; after its worked example → also clean.  Chosen:
  after the intro, so the chart sits immediately before the example that reads
  C1's 324 W off it, with a forward reference added to §১৪.৭.১.

**Counts after the fixes.**  Digest chapters 143 pp total; merged digest
**142 → 145 pages** (ch01 +1, ch14 +1, ch28 +1 — all genuine added content),
which puts it back inside the spec's 145–152 band.  Only three gaps above 7 cm
remain (ch10 7.06, ch13 7.05, ch20 7.94) and all three are pre-existing in
chapters that were not edited.  Full book: **ch14 28 → 29 pp, ch18 25 → 26 pp**
(ch18's three 4.93/4.56/4.55 cm gaps are the pre-existing Open-items ones,
unchanged); ch12 23 pp and ch17 19 pp unchanged; merged full book re-run.
`qc.py dia_ch14` reports **0 problems**.

## Digest ch18 missing the motor nameplate diagram, 2026-09-05

The user pointed out that the digest's motor chapter promised nameplate
reading ("মোটরের নেমপ্লেট পড়ে ফুল-লোড কারেন্ট নির্ণয় করতে সক্ষম হবে" in the
objectives, নেমপ্লেট mentioned four times) but never showed the annotated
nameplate figure the full book has (`diagrams/ch18/d08_nameplate.png` — a
drawn plate, ten fields, callouts both sides: kW/HP, V/A, Hz/RPM, P.F./INS,
IP/DUTY). Pure reuse, no new artwork — added via `dpic()` right after §১৮.২'s
opening paragraph, with a short explanation of which field is the FLC and
which is the power factor. Import line in `sm18.py` gained `dpic`.

Adding the figure opened a 7.40 cm gap on p5 (সারণি ১৮.৪, the troubleshooting
table, was stranded with empty space before উদাহরণ ১৮.১ on the next page).
Fixed with the standing playbook: **a worked example is one unsplittable
block and a table is not** — swapped the order so উদাহরণ ১৮.১ comes first and
সারণি ১৮.৪ trails, able to flow across the page break. Digest ch18 stayed at
6 pages, 0 gaps above threshold. Merged digest still 145 pages; nameplate
figure lands on p86.
## Two more digest figures reused, 2026-09-05 — marked motor/fan photos

The user asked, after the nameplate fix: add a marked-up picture of the
motor's construction to ch18, and mark up a real fan photo in ch12. Both were
the same bug class as the nameplate — a **raw, un-annotated photo already
sat in a `pics()` gallery while an annotated version of the same photo
already existed in the full book**, unused by the digest.

- **ch18 (motor)**: digest showed plain `ph_cutaway.jpg` ("কাটা মোটর") in the
  three-photo gallery. The full book's `diagrams/ch18/d01_parts.png`
  ("মোটরের গঠন") is the same cutaway photo with **8 callouts** — টার্মিনাল
  বক্স, স্টেটর কয়েল, রোটর, মোটরের বডি, নেমপ্লেট, শ্যাফট, বিয়ারিং, কুলিং
  ফ্যান. Swapped in via `dpic()` at 14.6 cm in §১৮.১, right where the
  chapter's own objective ("মোটরের গঠন … ব্যাখ্যা করতে পারবে") lives; dropped
  the plain `ph_cutaway.jpg` entry from the gallery, kept `ph_stator.jpg` and
  `ph_rotor.jpg` (close-ups, still useful).
  **Placing the figure between the chapter's two opening paragraphs stranded
  7.05 cm on p1** — the figure is ~8.7 cm tall at 14.6 cm width and didn't
  fit what was left after one short paragraph. Fixed by moving the *second*
  paragraph (capacitor role) ahead of the figure instead of narrowing it —
  narrowing to fit the gap would have dropped the smallest callout label
  under 7.5 pt (checked: 12.8 cm → 7.02 pt, fails; the full book's own 15.4 cm
  → 8.45 pt is the safe end of that range). Digest ch18 **6 → 7 pages**, this
  is a genuine content addition, not padding; 0 gaps above threshold.
- **ch12 (fan)**: digest showed plain `ph_fan.jpg` ("সিলিং ফ্যান") in a mixed
  gallery with five capacitor photos. The full book's `diagrams/ch12/
  d01_parts.png` has the same photo with **5 callouts** (ব্লেড, ব্লেড
  ব্র্যাকেট, মোটর হাউজিং, সিলিং রোজ ও সরবরাহ তার, মোটরের উপরের ঢাকনা) —
  but that PNG is a **two-panel figure** (real photo on top, a *drawn*
  cutaway below) and the drawn half duplicates content the digest already
  carries via `d02_motor.png` (the outer-rotor cutaway, already placed at
  14.6 cm). Using the whole two-panel PNG would have shown two different
  drawings of the same rotor/stator back to back. **Cropped the PNG to just
  the top (real-photo) panel** with PIL — `diagrams/ch12/d01a_fan_photo.png`,
  0 to y=508 of the 1240×1014 SVG canvas (scale ×3) — no new artwork drawn,
  just an existing rendered panel isolated into its own file, the same
  method already used elsewhere in this project for cropping a printed
  sheet down to one figure. Placed via `dpic()` at 14.6 cm right after the
  opening paragraph, *before* `d02_motor.png` (see the real fan first, then
  its cutaway); removed the plain `ph_fan.jpg` gallery entry, leaving five
  capacitor photos — a more coherent gallery than the old mixed one. Digest
  ch12 held at **5 pages**, 0 gaps.
- Merged digest **145 → 146 pages** (ch18's genuine +1, ch12 unchanged).
  `qc.py dia_ch12` and `qc.py dia_ch18` both report 0 problems (the crop
  did not touch anything `qc.py` tracks — the leader lines were already
  drawn and recorded by `dia_ch12.d01_parts` before the crop; PIL only cut
  the raster afterward). Verified in the merged PDF: motor figure lands on
  pp 84–85, fan figure on p 57.

## Digest ch28: undefined symbol in the Wenner formula, 2026-09-05

User caught it directly off a rendered page: "মাটির রেজিস্টিভিটি মাপা হয়
ওয়েনার পদ্ধতিতে, ρ = 2 × π × S × পাঠ" gave the formula but never said what
S is anywhere in the digest — "S ki? eta to pdf e bolay nai". The full book
has a whole subsection for this (§২৮.৯.৩, figure + `formula` box defining
ρ/S/R + worked example ২৮.৮); the digest compressed it to one clause in a
paragraph mostly about post-energisation checks and dropped the definitions
in the process. Fixed by rewriting that sentence to name **S** (spacing
between adjacent spikes, in metres) and **R** (the instrument's reading, in
ohms) right where the formula is used, without pulling in the full book's
figure/worked example — the digest's space doesn't have room for those and
the one-line fix is enough for a formula that only appears once. `sm28.py`
rebuilt clean at 7 pages, 0 gaps; merged digest still 146 pages, fix lands
on p145.
## Digest ch01: head-to-toe PPE diagram added, 2026-09-05

The user sent a screenshot of the full book's চিত্র ১.৮ (`diagrams/ch01/
d05_ppe.png` — a drawn worker figure with 8 PPE items labelled head to toe,
titled "ব্যক্তিগত প্রতিরক্ষামূলক সরঞ্জাম (PPE) — মাথা থেকে পা") and asked for it
in the digest. §১.২ already had all 8 items as individual real photos via
`pics()`, but never the combined overview the full book places at the top
of its own PPE section — same reuse-only rule, no new artwork. Added via
`diagram()` at 13.6 cm.

**Placement mattered.** Inserted first right after the intro paragraph
(matching the full book's own order — figure, then the itemised table/
gallery) and it pushed the whole chapter's tail into a 7.77 cm gap on p7 (the
CPR box got shoved whole onto p8). Moved to **after** the individual-photo
gallery instead, right before §১.৩'s heading — same content, reordered —
and the gap closed with **no page added**: ch01 held at 7 pages, merged
digest still 146. `qc.py dia_ch01` 0 problems.
## Institute material photos + a section-level সূচিপত্র, 2026-09-08

The user's three asks, in their words: "ey book tate tumi onek pic add koro
nai..jeta tumi amar sonkhipto book e add korso...ami dekhlam tumi celling rose
add koro nai..amar folder e aro onek image chilo" · "index ta sundor moto part
by part kore banaya daw..ar page number jeno index e sundor vabe docx file e
thik thake" · "book er majhe chapter name with chapter number lekha thakbe..ar
dan dike rapti.net".

**The picture complaint was exact and it had a single cause.**
`assets_hwbook.py` had already pulled **50 real photographs of house-wiring
material** out of `Electrical House Wiring book.docx` (image65–image120 — the
institute's own "হাউস ওয়ারিং এ ব্যবহৃত মালামালসমূহ" table) into
`assets/hwbook/`, and **not one chapter used any of them.**  `ceil_rose.jpg`
was sitting right there unused, which is what the user spotted.  A
hash-comparison of the media inside every built `.docx` against every file on
disk is the way to find this class of miss — a text grep over `chNN.py` does
**not** work, because chapters reach their assets through helpers
(`P("screwdriver_set")`), so a grep says "unused" for images that are used and
says nothing about images that exist but were never wired up.  All 50 are now
placed:

- **ch03** ceil_rose (new **৩.৩.১ সিলিং রোজ** — the chapter already *named* the
  ceiling rose three times and never showed or explained one), plug_2pin /
  plug_3pin_round / plug_3pin_flat in §৩.৪.
- **ch06** gang_bell (new **৬.১.৩ পুশ সুইচ** — every circuit in the chapter uses
  a push switch and none was pictured).
- **ch09** sock_3pin + sock_3pin_flat in §৯.৪.
- **ch12** reg_coil in §১২.৬ (the heat-sink fins, and why they must not be
  buried in the back box).
- **ch13** sw_twoway in §১৩.২; sw_inter + sw_inter2 in §১৩.৫.
- **ch14** main_switch in §১৪.২ (the iron-clad ancestor of today's DP MCB);
  cable_tray + cable_tray2 added to §১৪.৩'s materials row; rawl_plug /
  rawl_plug2 / rawl_bolt / screw_star / screw_flat / cable_clip in §১৪.৮.২ —
  the estimate table's own "থোক" row, finally shown.
- **ch15** box_gang_pvc / box_gang_steel / box_piano (§১৫.২), sw_oneway /
  indicator / dimmer / sock_2pin / fuse_piano / sw_bellpush (§১৫.৩),
  dp_switch + dp_switch2 as a face/back pair, gang1–gang5 (§১৫.৪.২).
- **ch19** changeover + changeover2 in a new **১৯.৯.৪ বাইপাস বা চেঞ্জওভার সুইচ**
  (the old ১৯.৯.৪ renumbered to ১৯.৯.৫).
- **ch24** lugs (§২৪.৬.৬), cable_tie (§২৪.৬.৭); also `ch24/ph_ready.jpg`,
  which was on disk and used by nothing.
- **ch25** sdb + din_rail in §২৫.২.
- **ch26** pvc_pipe / bend / elbow / tee / saddle / box_circular (§২৬.৩),
  box_circular2 (§২৬.৪).
- **ch27** pvc_channel (§২৭.৩.২).  **ch02** work_light (§২.৩.৭).

**Three captions were wrong before they shipped, and reading the pixels caught
all three** — the standing "look at the photograph before writing its caption"
rule, which is worth its keep every single time:
- `sw_inter2` is marked **16AX**, not 10AX; it also carries `TOP`,
  `BS EN 60669` and a separate brass **earth screw** on the metal plate.  All
  three are in the caption and the prose now, and the earth screw is the
  better teaching point.
- `ch24/ph_ready.jpg` is **not** "two rows of breakers with a circuit list in
  the door" — it is three vertical rows behind a grey dead-front with a copper
  neutral/earth bar chamber below a clear polycarbonate shield.  Which is
  exactly what §২৪.৬.৯'s text describes, so the figure moved to that sentence.
  It is also **portrait 1700×2907**, i.e. ~16 cm tall at any usable width;
  cropped to its bottom half as `ph_ready_bars.jpg` (1700×1454) — the ch22
  portrait-photo rule.
- `sdb.jpg` is an **RCBO** (`IΔn 30mA`, test button) plus `C40`, `C16`, `C16`
  and one blanked spare way — not "main + ways".  The blank way is BNBC
  ১.৩.৯.৩.৯'s spare, so the caption teaches that instead.

**Page-foot gaps.**  Every touched chapter was re-measured and closed with the
standing playbook; nothing was shrunk except one photo that had no lettering:
- **ch09** — three worked examples back to back (the ch13 trap).  উদাহরণ ৯.৩
  moved to *after* সারণি ৯.৫ and the fuse-selection `formula` box, which it
  is actually about.  5.57 → clean, 18 pp.
- **ch13** — উদাহরণ ১৩.১ stranded 9.26 cm.  চিত্র ১৩.১১ (বাতি জ্বলার ক্রম)
  moved to *after* the example, its two `steps=` merged with `\quad`
  (**not** `\;`, which the DSL does not know), and §১৩.৫'s explanatory
  paragraph moved *ahead* of the new photo pair.  Three gaps now 4.81 / 4.83 /
  4.88 cm, 21 pp.  *Moving the photo pair itself was tried twice and reverted
  both times — the ch17 lesson again.*
- **ch15** — 10.82 cm before উদাহরণ ১৫.২: the tip box moved *before* it, the
  §১৫.৯ step figure moved *after* its numbered list, the example's module
  `steps=` merged, and the back-box photo row moved past §১৫.২'s note box.
  One 6.64 cm gap left (an unsplittable worked example), 24 pp.
- **ch27** — the channel photo at 9.6 cm added a page and opened 10.48 cm.
  **Swapping সারণি ২৭.৬ and উদাহরণ ২৭.১ just moved the gap to p19** (9.13 cm)
  and was reverted; placing the photo at **7.4 cm** put the chapter back to
  32 pp with only its pre-existing 4.55 cm gap.  The photo carries no
  lettering, so the `N × P(pt) / W` floor does not apply to it.
- **ch25** keeps 5.68 / 4.63 cm (45 pp) — four reorderings were tried and each
  made it worse.  ch02/03/06/12/14/24/26 are clean; ch19's 4.80 cm is the
  pre-existing Open-items gap.

**`mkbook.py` — the digest's three fixes ported to the full book.**  Same
machinery as `mkdigest.py`, same reasons; see the 2026-09-06 digest entry for
the derivations, which are not repeated here:
- **Running header, three columns on one line** — book title (left) ·
  `STYLEREF "RaptiChapterTitle"` (centre) · `rapti.net` (right).  The header
  paragraph is set to style **"Normal"**, because the built-in "Header" style
  carries its own tab stops which OOXML *merges* with the paragraph's own and
  leaves `rapti.net` stranded mid-page; `tab_stops.clear_all()` does not
  touch a style's stops.  Measured in the built PDF: every chapter title's
  midpoint on **303.4 pt** and `rapti.net` ending on **538.7 pt** on every
  sampled page (2, 20, 120, 300, 500, 700, 786), each showing its own
  chapter.  `chapter_opener()`'s hidden 1 pt "অধ্যায় N · " prefix is what puts
  the number in front of the title.
- **সূচিপত্র now lists every `b.h1()` section** under its chapter, indented,
  dotted leader, own page number — 28 chapters + **364 sections = 392
  anchors**, 10 pages (p3–p12), so chapter 1 opens on **p13**.
  `chapter_sections()` reads each chapter's `Heading 1` paragraphs and
  `inject_section_bookmarks()` wraps the k-th of them in `_chNN_sK` during
  the merge — identical filter and order, so k lines up.
- **The page numbers are baked in as static text.**  `bake_toc_numbers()`
  round-trips a throwaway copy through `soffice --convert-to docx`, reads each
  resolved `PAGEREF`, writes the Bangla number into the shipped file and
  **deletes the field machinery around it**.  Verified after the build: the
  shipped `document.xml` has **0 PAGEREF and 0 fldChar**, and a sample of TOC
  lines was checked against the pages they name — all matched.  *This fails
  soft: check the `bake:` line in the build output (it should say 392).*
- **Merged book: 762 → 786 pages** (+24: the new content in eleven chapters,
  +9 for the longer সূচিপত্র).  **506.8 MB `.docx`, 44.5 MB PDF.**  No
  near-empty pages (checked: no body page under 230 characters).
- On the front-matter pages the STYLEREF shows "অধ্যায় ১ · কর্মক্ষেত্রে
  নিরাপত্তা", because LibreOffice falls forward to the next occurrence when
  nothing precedes.  Same behaviour as the digest, left as is.

## Chapter 1's PPE and CPR figures — a redraw that was rejected, 2026-09-08

> **Superseded for `d11_cpr` on 2026-09-08** — the CPR figure (চিত্র ১.১৩)
> was removed from the book entirely at the user's instruction and replaced
> with a step-by-step prose description; see "Chapter 1's CPR figure removed"
> at the end of this file. The rest of this section, and the "do not redraw"
> rule for **`d05_ppe`**, still stand.

**Do not redraw `d05_ppe` or `d11_cpr`.  It was tried and the user turned it
down: "ager drawing e valo chilo... faltu drawing hoyse... ager tay rakho".**
`dia_ch01.py` was reverted to the committed version and is byte-identical to
it again; both books were re-merged from the restored artwork.

What happened, so nobody spends the effort a second time.  The user supplied
two reference pictures at the project root —
`protective-and-safety-equipment-or-ppe-vector-illustration-helmet-JP3R39.jpg`
(Alamy stock, watermark burned in) and
`3793187-CPR-Artboard-1-1-1024x1007.avif` (Medical News Today) — and asked for
the two chapter-1 figures to be drawn "aro sundor vabe".  They were rebuilt in
a much more illustrative register: an anatomically-proportioned worker with a
hi-vis vest, a fall-arrest harness with a D-ring, gloves with fingers and real
boots; and, for CPR, a continuous supine casualty plus a kneeling rescuer with
head, torso and arms in every panel, the two figures separated by a warm/cool
palette and a paper-coloured halo.  `qc.py` was clean, both aspect ratios were
held so no page moved, and ch01 stayed at 27 pages.  **The user still preferred
the originals.**

The lesson is about register, not about craft: this book's figures are
**diagrammatic** — flat, sparse, and read at a glance beside dense technical
prose.  The reference images are consumer-infographic illustration, and pulling
the artwork toward them made it busier without making it more informative,
which is the same complaint recorded for ch14's diagrams on 2026-08-15.  A
reference picture the user sends is a pointer at *subject matter*, not a
licence to change the drawing style.  Ask before restyling a figure that is
already approved.

(Both reference files are copyrighted and were used only for checking anatomy;
nothing from either was embedded, and neither should be.)

**Two targeted defect fixes to these figures were accepted later on 2026-09-08**
— not a restyle, so they do not contradict the "do not redraw" note above.
The user pointed at concrete errors: চিত্র ১.১৩ (`d11_cpr`) panel ২
"শ্বাসনালি খোলা" reused the flat supine head from panels ১/৩ unchanged, so
with the press-forehead / lift-chin arrows around it the face read as pointing
at the floor; and চিত্র ১.৪ (`d05_ppe`) drew the hands as plain circles
identical to the joint blobs, so the "ইনসুলেটেড গ্লাভস" leader landed on what
looked like a joint. Fixes, same flat register, same proportions:
- `victim()` gained a `tilt` param (default 0 → panels ১/৩/৪ emit byte-for-byte
  the same SVG). Panel ২ calls `victim(..., tilt=22)`; the head + neck stub +
  face are wrapped in one `<g transform="rotate(tilt, pvx, pvy)">` about the
  base of the skull, and the returned `forehead`/`mouth`/`chin` anchors are
  rotated with it (so the overlaid hands and the airway line follow). +ve tilt
  = crown drops back, chin and face rotate up.
- `worker()`'s glove branch (only `d05_ppe` passes `gloves=True`; every other
  caller passes `gloves=False` and is untouched) now draws a gauntlet cuff
  trapezoid + a rounded mitten palm + a thumb bump instead of one circle.
- `qc.py dia_ch01` 0 problems; ch01 still 27 pages, no page-foot gap. Figure
  count unchanged (14/12).

**A second round on the same two figures, same day 2026-09-08** — the first
round was not enough. "hat ekhono gol..angul er moto banaw" and "cpr … mukh
chokh mukh ehono thik hoy nai … amon mone hosse buker bodole pithe chap dewa
hosse":
- **Glove now has four SEPARATE fingers** (rounded-rect bars pointing down) +
  a thumb bar on the body side + the gauntlet cuff — the mitten still read as
  a blob. Bigger footprint than a joint circle, so it can't be confused.
- **The CPR misread was the nose.** `victim()`'s face drew the nose as a
  sideways `<` on the far-left of the skull — a profile of an upright head —
  so on a horizontal body the casualty read as lying **face-down**, and the
  panel-3 chest compression looked like it was on the back. The nose is now a
  small caret poking **up** off the top-left of the skull (apex ~y−69 rel gy),
  the closed eye moved onto the upper face, the mouth sits just below the
  nose. All four panels now read as supine/face-up. An ear was tried and
  removed — it swung to the front of the face under the panel-2 rotation and
  the nose-up cue alone is enough.
- Panel 2's head-tilt dialled back 22° → **13°** (the redrawn face already
  reads face-up, so only a gentle back-tilt is needed for the airway step)
  and the forehead-hand rect nudged down to close the gap to the crown.
- `qc.py dia_ch01` 0 problems; ch01 still 27 pages, no gap; figures 14/12.
- Full book re-merged with `mkbook.py` on the user's instruction ("amar full
  tay merge kore debe … choto book touch korar dorkar nai" — digest left
  alone). Only `out/অধ্যায়-০১*.docx` was rebuilt; the other 27 in `out/`
  were current from earlier the same day.

**A third round on `d11_cpr` only, same day 2026-09-08** — user, looking at
the rendered figure: "diagram 1.13 er mathay chul add koro … amon vabe show
koro jeno tar matha matite ar mukh ar chokh upore". Still a targeted fix in
the same vein as rounds 1–2, not a restyle. `victim()`'s head was rebuilt so
it reads unambiguously supine:
- **Hair added** — one flat filled crescent (`HR = "#43372B"`, no stroke): an
  outer 35 px arc about `(x+49, gy-37)` wrapping the crown (which points left,
  away from the feet) and the occiput, its bottom reaching the ground line,
  closed by two quadratics that hug ~13 px inside the skin circle. Drawn
  after the skin circle, before the face, so the face sits on top.
- **Head dropped onto the floor** — skin circle centre `gy-50 → gy-44`; the
  hair crescent (not the skin) is what touches the ground, which is what
  supine actually looks like from the side.
- **Face moved to the TOP of the skull** — closed eye at `~(x+47, gy-56)`,
  then a small **filled** skin-colour nose bump on the skyline
  (`Q … Z`, apex ~10 px above the outline), then the mouth at `~(x+59, gy-46)`.
  Anchors: forehead `(x+48, gy-70)`, mouth `(x+56, gy-47)`, chin `(x+68,
  gy-36)` — all now on the top/upper-right.
- **Tilt sign flipped.** With the face on top, a *negative* tilt rocks the
  head back on the occiput (crown-left swings up); the pivot moved to the
  ground-contact point `(x+52, gy-16)`. Panel 2 calls `tilt=-10` (was `+13`),
  and its forehead-palm / chin-finger offsets were re-tuned to the new
  anchors — palm bottom now `fy_+8` so it sits ON the forehead, chin fingers
  to the right of the chin lifting up-and-forward.
- `qc.py dia_ch01` 0 problems; ch01 still **27 pages**, no page-foot gap;
  figures 14/12. `victim()` is only used by `d11_cpr`, so nothing else moved.

## Chapter 1's CPR figure removed, replaced with step-by-step prose, 2026-09-08

The user asked to delete চিত্র ১.১৩ (`d11_cpr`, the 2×2 CPR pictogram)
"everywhere" and replace it with a plain numbered how-to so a layperson can
follow it after one read ("1.13 diagram delete kore daw sob jayga theke… oy
diagram er bodore… sundor moto dhape dhape description… je kew porar por
kivabe korte hobe bujhe"). This **supersedes** the three "do not redraw
`d11_cpr`" rounds above — those were about restyling an approved figure; this
is the user removing it outright. `d05_ppe`'s "do not redraw" still holds.

- **`dia_ch01.py`** — `d11_cpr()` and its private helper `victim()` (used by
  nothing else) deleted; `d11_cpr` dropped from `ALL`. `import os, math`
  left as is. `diagrams/ch01/d11_cpr.svg` and `.png` deleted, and the stale
  copy under `Book/অধ্যায়-০১/ডায়াগ্রাম-সোর্স (SVG)/`.
- **`ch01.py` §১.১১.৩** — the `b.figure(d11_cpr…)` line and the old rate/ratio
  `note` box replaced with a **6-step `b.numbered()`**: সাড়া ও শ্বাস পরীক্ষা ·
  সাহায্য ডাকা (৯৯৯ + AED) · শ্বাসনালি খোলা · বুকে চাপ (৫–৬ সেমি, ১০০–১২০/মিনিট,
  full recoil) · কৃত্রিম শ্বাস (৩০ঃ২, hands-only fallback) · চক্র চালু রাখা
  (২-min swap, when to stop). The `note` box now carries the real caveat —
  **do not compress someone who is breathing; recovery position instead.**
  `W["d11"]` removed from the width dict.
- **Figure renumber is automatic** (`b.fig_n`): d10_rescue stays চিত্র ১.১২,
  d12_hierarchy shifts চিত্র ১.১৪ → **চিত্র ১.১৩**. No prose cross-references
  to either number existed. Figures 14 → **13**, tables still 12.
- **Page-foot gap.** Removing an ~11.6 cm figure for ~6 numbered steps grew
  the chapter 27 → **28 pp** and opened a 4.58 cm gap on p21 (সারণি ১.১০,
  the burns table, stranded to p22). Closed with the standing playbook — a
  two-line intro paragraph was **owed** to §১.১১.৪ anyway (it jumped straight
  from heading to table); it fills p21's foot and the table starts clean on
  p22. `layout.py`: no gap above threshold. `qc.py dia_ch01` 0 problems.
- **The digest never carried this figure** — `sm01.py` has always described
  CPR in a text `note` box, so "delete from everywhere" touched only the full
  book. `mkdigest.py` was not re-run (nothing changed in it).
- **Re-merged** with `mkbook.py` (only `out/অধ্যায়-০১*.docx` rebuilt; the
  other 27 were current from the same-day 11:53 build). Full book **786 →
  787 pages**, 506.2 MB `.docx`; `bake:` 392 anchors resolved (clean); PDF
  re-rendered from the baked DEST. Running STYLEREF header still tracks the
  chapter name across the new pagination. Deliverables copied to
  `Book/অধ্যায়-০১ — …docx` and `Book/অধ্যায়-০১/প্রিভিউ — অধ্যায় ০১.pdf`.

## Chapters 1–10 recheck, 2026-09-08 (full book only — the digest was NOT touched)

User's ask, in their own words: "chapter 1-10 recheck daw..tomar dewa lekha gulo ektu
easy kore lekho...jekhane jekhane kothin word ase segulo sohoj koro..onek sentence
kemon jani tumi purno koro na..segulo purno koro and sohoj koro...ar kono fact vul
hole segulo thik koro.....ar kono infromation ba kono topic missing thakle seta add
koro..tarpor amake final book e merge kore daw", then, on being asked: "tumi shudu
amar full book ta porba oyta thik korba...choto book ta na" — so `smNN.py` was left
completely alone.  **Merged full book: 787 → 793 pages.**

**Promised-but-never-delivered content — this was the real find.**  Four places named
a thing in a heading, an objective or an exercise question and then never said it:
- **ch01 §১.৭.১** had the heading "পাঁচটি সোনালি নিয়ম", a lead-in ending "এই ক্রম কখনো
  পরিবর্তন করা যাবে না।" and then *nothing* — the five rules appeared only inside
  `d07_five_rules.png`, two subsections later.  সংক্ষিপ্ত প্রশ্ন খ.৮ asks "পাঁচটি সোনালি নিয়ম
  কী কী?" — a question the book never answered.  Now a five-item `b.numbered()` giving
  each rule's **reason and consequence** (not the figure's own sub-lines — the digest
  lesson that a list restating the artwork reads as duplicate), with the figure moved
  up under it.  Verified by web search: **EN 50110-1:2023 clause 6.2**, same five rules
  in the same order as the figure.
- **ch01 §১.৭.২** said "যাচাই করতে হয় তিন ধাপে —" and listed no steps.  The three
  Prove–Test–Prove steps are written out now; they agree with ch08's লাইভ–ডেড–লাইভ box.
- **ch01 §১.১১.২** carried the rescue steps only inside `d10_rescue.png`, though
  রচনামূলক প্রশ্ন গ.৫ asks for "উদ্ধার থেকে শুরু করে CPR পর্যন্ত করণীয় ধাপগুলো"।  Five steps
  added in prose (CPR steps were already prose since the 2026-09-08 figure removal).
- **ch02 §২.৬** promised Class I/II/III in the objectives, MCQ ৫ and সংক্ষিপ্ত প্রশ্ন খ.৯,
  but the body had only a figure.  New **সারণি ২.৭** (IEC 61140 — how each class protects,
  how to recognise it, whether earthing is needed, examples) plus a ⚠ box on not cutting
  a class I tool's earth pin.  ch02 gained tables: **15/13**, not 15/9 — see the §২.৩ uniformity fix below.

**Factual errors fixed (all verified, do not revert):**
- **ch08 উদাহরণ ৮.২ was physically wrong.**  It measured "a lamp's coil with the supply
  off" and read **529 Ω** — but 529 Ω is the *hot* resistance; a tungsten filament is
  ~15× lower cold, so a good 100 W bulb actually reads 35–45 Ω on the meter.  The
  example's own moral ("রোধ মেপেই বাতির ক্ষমতা যাচাই করা যায়") is false for a filament
  lamp.  Rewritten around a **1000 W iron (52.9 Ω → 4.35 A → 1000 W)**, whose nichrome
  element barely changes resistance with temperature, plus a new ❖ box stating the
  tungsten trap explicitly.  ch10 §১০.৮ already said the same thing correctly — the two
  chapters had been contradicting each other.
- **Wire colour was taught as if IEC were the only rule.**  ch03 and ch04 taught
  brown/blue with no caveat, and ch04 §৪.৯.১ actively claimed "BNBC-ও … প্রযোজ্য IEC মান
  অনুসরণের নির্দেশনা দেয়" — which is not true: BNBC Table 8.1.2 (clause 1.3.9.3.15) is
  **red/yellow/blue phases, black neutral**, so **blue means a phase in BNBC and neutral
  in IEC**.  Both chapters now carry a ⚠ box naming both systems, flagging the blue trap,
  noting that only green-yellow agrees, and pointing at অধ্যায় ২৩.  Same fix the digest
  got in the 2026-09-05 accuracy review; the full book had never received it.
- **BNBC edition was inconsistent.**  ch07, ch10, ch11, ch12, ch13 cited "BNBC ২০২০"
  while ch18–ch28 — every chapter whose clause numbers were actually extracted from the
  source PDF — cite **বিএনবিসি ২০১২**.  Every clause number in this book comes from the
  2012 PDF at law.resource.org, so all five were unified to ২০১২.  (ch11–13 are outside
  the requested range but it is the same one-word error; leaving three chapters wrong
  while fixing two would have been worse.  Their page counts are unchanged: 24/24/21.)
- **ch06 §৬.১.১** pointed at "অধ্যায় ১-এ প্রতীক দ্রষ্টব্য" for the fire-alarm bell symbol.
  That symbol is `sym_fire_bell` in **dia_ch05**; ch01 has safety *signs*, not symbols.
- **ch09** cited **IEC 60446** for conductor colours in সারণি ৯.৩ and MCQ ৬, although
  ch04 itself says 60446 was merged into **IEC 60445**.  Both changed.
- **ch04 উদাহরণ ৪.৪** had `` `বিল` = 45 \times 7 = 315 `টাকা` `` inside `steps=` — the
  Bangla-in-OMML case CLAUDE.md itself calls "luck, not licence".  The taka line moved
  into `answer=` (which is `_rich` body text).  `mathguard.py` is now clean on ch01–ch10.

**Missing topic added — ch04 §৪.৭.১ "সাইকেল, পিক ও আরএমএস মান".**  The book says "২৩০ V"
several hundred times and had never said *what kind of value* that is.  New subsection
defines সাইকেল, পিক মান and আরএমএস (as the DC-equivalent-heating value), gives
`V_rms = V_m/√2` and `V_m = √2 V_rms` as real OMML (the `\sqrt` support added for ch16),
and lands the payoff in a ❖ box: **230 V RMS has a 325 V peak, which is why a 230 V fan's
capacitor is marked 400–450 V AC** — a shop-counter fact, tied forward to অধ্যায় ১২.
One MCQ added (key rebalanced to ক4 খ4 গ4 ঘ4) and one short question.

**ch05 §৫.৩ — the "৬১ %" is derivable now, not asserted.**  সারণি ৫.২ had quoted
aluminium's conductivity as 61 % of copper's with nothing behind it.  ρ_Cu = 1.72×10⁻⁸
and ρ_Al = 2.82×10⁻⁸ Ω·m are printed (as `b.math`, not Unicode superscripts), and
1.72 / 2.82 = 0.61 reproduces the table exactly, tying back to ch04's R = ρL/A.

**Language pass.**  Hard words swapped only where they actually occurred (a grep of ~45
candidates found them sparse, so this was sentence-level editing, not a blanket script):
ইন্দ্রিয়গ্রাহ্য → চোখে দেখা যায় না · অনিয়মতান্ত্রিকভাবে → নিয়ম না মেনে · প্রতিপালন → মেনে চলা ·
সিংহভাগ → বেশির ভাগ · ত্বরান্বিত → দ্রুত · অবহিত → জানানো · বাঞ্ছনীয় → দরকার ·
প্রতিস্থাপন → বদলে নেওয়া · নির্গমন পথ → বের হওয়ার পথ · অনুক্রম → ধাপক্রম · সঞ্চিত শক্তি
অপসারণ → জমে থাকা শক্তি সরানো · সংকীর্ণ → সরু · ষড়ভুজাকার → ছয় কোণা · ধ্বংসাবশেষ → ভাঙা
টুকরো · দ্রাবক → থিনার · কষ্টসাধ্য → কঠিন · নিষ্প্রভ → নিভু নিভু · সমষ্টিগত → সব · বর্জনীয় →
যা করা যাবে না · আত্মস্থ → বোঝা · সূত্রপাত → শুরু · কোলাহলপূর্ণ → যেখানে অনেক শব্দ হয় ।
**`অন্তরক`/`অন্তরণ`/`অন্তরিত` → `ইনসুলেটেড`/`ইনসুলেশন` throughout ch02**, and
`দ্বৈত অন্তরণ` → `ডাবল ইনসুলেশন` — the rest of the book already said ইনসুলেশন, so this is
consistency as much as simplification.  `dia_ch02.d04_protection_class` was re-rendered
with the same two words so picture and table agree (`qc.py dia_ch02` 0 problems).
ch01's fuse ⚠ box was rewritten fresh, matching the wording settled for sm01 on
2026-09-06 ("ইচ্ছা করে দুর্বল করে রাখা হয়") instead of the old "দুর্বল কড়ি" idiom.
One surviving তুমি-imperative in ch08 ("ফিরিয়ে নিতে ভুলো না") and one in ch10's খ.৯
("কী বুঝবে?") were made নৈর্ব্যক্তিক/আপনি — the 2026-08-30 formality pass had missed them.

**Page-foot gaps — what worked and what was tried and reverted:**
- **ch05's four symbol charts fill a page exactly two at a time** (each ≈ 12.2 cm with
  its heading and caption, against a ≈ 24.7 cm text frame), so *any* text sharing their
  page costs a whole chart.  Adding the ρ block opened 7.03 / 5.17 cm.  **Compacting the
  block made it worse (8.91 cm)** — the ch17 lesson again.  What worked was paying the
  height back: the "চারটি চার্টে ৩৬টি প্রতীক" **note box became a plain paragraph folded
  into §৫.৪'s opening** (a box costs ~40 pt of chrome the charts cannot spare) and two
  numbered rules were trimmed to one line each.  14 pages, zero gaps.
- **ch01**: the PPE figure moved *after* সারণি ১.৫ (the digest's own 2026-09-05 finding,
  re-derived here), the rescue ⚠ box moved *before* `d10_rescue`, and the new rescue-step
  list filled the p20 foot.  29 pages, zero gaps.
- **ch02**: moving `d05_drill_zones` after the paragraph that explains it turned 4.78 cm
  into 6.96 cm — **reverted**.  The 4.78 cm on p13 stands, in the same band as ch04's
  long-standing 4.78 cm on p9.
- Also worth recording: **`dia_ch05`'s `T_SMALL` is 20 px on a 1280-px canvas = 6.82 pt
  at 15.4 cm**, below this file's own ~7.5 pt floor — the same defect found in ch11/12/13.
  It was *not* fixed here (raising it changes four sheets' geometry and would have
  re-opened the packing problem above); it is left as a known item.

**Verified after the pass:** all ten chapters rebuilt; `layout.py` clean on 8 of 10
(ch02 4.78, ch04 4.78 — the latter pre-existing); `mathguard.py` clean on all ten; MCQ
keys still balanced (ch01–ch10 ক/খ/গ/ঘ within one of each other, longest run 2); no `§`
anywhere.  Page counts **29 21 17 20 14 14 24 21 18 17** (was 28 20 16 18 14 14 24 20
18 17 — +6, every page of it new content).  Re-merged: **793 pages, 506.2 MB `.docx`,
44.6 MB PDF**; `bake:` reported 392 anchors resolved and the shipped `document.xml` has
0 `PAGEREF` and 0 `fldChar`; the সূচিপত্র's chapter and section page numbers were checked
against the actual chapter openers and the running STYLEREF header still names the right
chapter from p2 to p793.

**§২.৩'s seven subsections did not present their tools the same way** (user, same
day: "2.3.6 er description age ba porer description er sathe mile na..ager gulo table
kore chilo").  ২.৩.১/২/৩/৫ each ran `figure_row` + a Word table, but **২.৩.৪ and ২.৩.৬
used `b.bullets()` and ২.৩.৭ a running paragraph** — so the reader met three different
shapes inside one section.  All three converted to tables on the `["নাম", "…"]` +
`widths=[3.0, 7.4]` pattern of ২.৩.৩, giving সারণি ২.৪ (রেঞ্চ/অ্যালেন কি/ভাইস),
২.৬ (মাপ ও মার্কিং) and ২.৮ (ওয়্যারিং সহায়ক); ২.৩.৭'s prose kept all its content,
including the work-light line about the mains being off and a phone torch costing you
a hand.  Tables 10 → 13, and every later সারণি number in ch02 shifts by three — nothing
cross-references them, so no other edit was needed.  **The conversion pushed ch02 to 22
pages with an 8.56 cm gap on p14**; closed by moving `d05_drill_zones` to the *end* of
§২.৬.২, after the tip box (and "চিত্রে দেখানো" → "নিচের চিত্রে দেখানো" so the paragraph
points forward).  Back to **21 pages with zero gaps** — better than the 4.78 cm it
carried before this fix.

**The 1–23 merged book was deleted on the user's instruction** ("1-23 chapter er book ta
delete kore daw").  The `.pdf` was tracked in git so it went via `git rm`; the 275 MB
`.docx` was untracked and was removed from disk.  Only the ১–২৮ merge remains, so a
`সম্পূর্ণ বই*` glob is now unambiguous.

## Chapters 11–15 recheck, 2026-09-09 (full book only — the digest was NOT touched)

Same ask as the 1–10 recheck, one range on: "chapter 11-15 recheck daw..tomar dewa lekha
gulo ektu easy kore lekho...jekhane jekhane kothin word ase segulo sohoj koro..onek
sentence kemon jani tumi purno koro na..segulo purno koro and sohoj koro...ar kono fact
vul hole segulo thik koro.....ar kono infromation ba kono topic missing thakle seta add
koro..tarpor amake final book e merge kore daw".  `smNN.py` was left alone, as in the
1–10 pass.  Page counts **24 / 25 / 21 / 31 / 24** (was 24 / 24 / 21 / 30 / 24).

**A Unicode trap that will bite every future scripted edit — read this first.**  The
chapter sources use **composed ো / ৌ (U+09CB, U+09CC) but DECOMPOSED nukta letters**
(য় = য + ়, ড় = ড + ়, ঢ় = ঢ + ়).  There is not a single U+09DF/09DC/09DD in any of
them.  So a `grep` for a word containing য়/ড়/ঢ় typed the ordinary way silently returns
**nothing** — the first hard-word sweep of this session reported "রেওয়াজ: 0 hits" in a
file that has two.  Every scripted search/replace has to push its needles through
`NFC` and then decompose those three letters back.  The helper that does it is
`bnedit.py` (kept in the session scratchpad, not the repo — it is ten lines); rewrite it
rather than trusting a bare grep.  It also refuses to write the file unless *every*
pattern matched its expected count, which caught four typo'd needles here.

**The one that mattered: the ECC minimum contradicted itself across three chapters.**
ch28 §২৮.৪ already prints the conflict and resolves it — **1.3.37.3.1 sets a 4.0 mm²
floor on every ECC, while 1.3.8.2.3 says only that a *socket's* ECC shall not be under
1.5** — and states plainly that the book takes the stricter reading.  ch14 and ch15 had
never got that memo: both printed **১.৫ mm² as *the* minimum**, citing 1.3.8.2.3, so a
reader going from ch14's estimate to ch28's earthing chapter met two different numbers.
Fixed in both, worded to match ch28: ch14's সার্কিটভেদে table row is now `৪ mm²
(সর্বনিম্ন) · ১.৩.৩৭.৩.১` with a ❖ box naming both clauses and pointing at অধ্যায় ২৮;
ch15's রং-ও-সাইজ table row reads `৪ mm² (সকেটে অন্তত ১.৫)` citing both.  **The estimate
had to move with it** — `১.৫ mm² সবুজ-হলুদ আর্থ তার` → `৪ mm²`, and that in turn broke
উদাহরণ ১৪.৩, which had counted **three** 1.5 mm² conductors on the SDB→board run.  The
example now counts two (ফেজ + নিউট্রাল, ইসিসি আলাদা মাপের): 14 + 54 + 20 = 88, ×1.10 =
**96.8 → ৯৭ m**, and its note keeps a real lesson instead of losing one — 97 m fits one
100 m coil with **3 m to spare**, so one extra point costs a whole coil.  অনুশীলনী ঘ.৪
was moved to the same convention (2 wires → **প্রায় ১০৮ মিটার**, was ১১৮).  ch15's
socket-specific bullet in §১৫.৭.১ was **left at 1.5** — there it really is 1.3.8.2.3's
own case and is correct as written.

**Other content that was promised and never delivered:**
- **ch12 §১২.৬ said "বাজারে তিন ধরনের রেগুলেটর পাওয়া যায়" and then described two.**
  `dia_ch12.d06_reg_types` has drawn all three since day one — রেজিস্টিভ (কয়েল টাইপ),
  ক্যাপাসিটর (স্টেপ) টাইপ, ইলেকট্রনিক (TRIAC) — with its own comparison table inside the
  artwork, so the body had a hole exactly where the picture did not.  Added a paragraph
  on the capacitor/step type: a different-value capacitor comes into series at each
  step, reactance drops the motor volts, and because a capacitor burns almost no real
  power the bill really does fall and the regulator does not get hot; the limits are
  fixed steps and one dead capacitor killing one step.  It ties back to §১২.৪.২'s
  four-or-five-wire multi-value capacitor, which the book had described and then never
  used.  **Do not add a comparison table in the body** — the diagram already carries one
  (the standing "nothing in the artwork that repeats a sentence from the body" rule).
  This also repairs MCQ ১১, whose "ক্যাপাসিটর টাইপ" option the reader had never met.
- **ch11 never explained টিনিং**, though the পারিভাষিক শব্দ table defines it and MCQ ১১
  uses it as a distractor.  Added to §১১.৮.৩, together with the **iron wattage** the
  chapter had never given: 25 W is for electronics, house wiring wants **60–100 W**, and
  an under-powered iron is a cold-joint machine.
- **ch14 §১৪.৮ referred to "চার নম্বর ধাপ" without ever naming the six steps** (they
  existed only inside `d10_estimate_steps` and in the সারসংক্ষেপ).  Named in the body now.
- **ch14 was missing "লে-আউটের প্রয়োজনীয়তা", which the syllabus names as its own line
  item** — §১৪.৬ asserted BNBC 1.3.10 and gave one reason.  Six now, plus a short
  question, and the objective is finally answerable from the text.
- **ch15 showed a photo captioned "ফিউজ ইউনিট" that the body never mentioned** (nor
  "বেল পুশ").  Both are rows in সারণি ১৫.২ now, with a paragraph on the rewirable board
  fuse, what replaced it (the SDB's MCB), and the one rule that survives it — never a
  copper wire in place of the fuse element, worded to match sm01's settled fuse box.
- **ch11 §১১.৩ said "পাঁচটি ধাপে সম্পন্ন হয়" without naming them** — named inline.

**Facts corrected:**
- **ch11 said "টিনের অনুপাত বাড়লে গলনাঙ্ক কমে", full stop** — true only up to the
  eutectic.  It now says the melting point falls to its lowest at **63 % tin, 183 °C**
  and *rises again* past that, which is also what finally makes the সারণি's ইউটেকটিক
  row mean something.
- **ch13 §১৩.৭ taught wire colour twice over and contradicted itself**: it said
  "বাংলাদেশে কড়াকড়ি কম" (BNBC 1.3.9.3.15 + Table 8.1.2 is mandatory and explicit),
  listed IEC brown/blue beside BNBC red/black with no note that the two disagree, and
  then **recommended নীল for a strapper one line after calling নীল a neutral colour**.
  Rewritten on BNBC alone: red/black/green-yellow single phase, red/yellow/blue three
  phase, strappers in **লাল ও হলুদ** (both code phase colours, and a strapper *is* a
  phase conductor), never neutral black and never earth green-yellow.  MCQ ১৩'s
  confusing "নীল-সাদা যেকোনো ফেজের রং" option went with it.
- **ch12's নেমপ্লেট table explained Class B / Class F as "কত তাপ সহ্য করতে পারে" and
  never gave the numbers** — 130 °C and 155 °C now.
- **ch15's "১০০ W ফ্যানের জন্য" rating** for a regulator → "১০০ W পর্যন্ত ফ্যান".

**Added because it is what a trainee actually needs:**
- **ch13** — a two-way switch will serve as an ordinary one-way switch (COM + either
  L1 or L2, leave the third terminal empty).  Comes up on every job where only two-way
  switches are in stock.
- **ch15 §১৫.৮** — the gang-counting rule was incomplete in the body; the subtlety
  ("সকেট গুনতে হয় দুবার") lived only inside উদাহরণ ১৫.২'s note.  Three traps in the
  text now: a socket counts twice (its own gang + its switch), a regulator is its own
  gang so a fan needs two, and a two-way switch is still one gang.

**Language.**  Sparse again — a normalized sweep of ~90 candidates over the five files
found the hard words clustered in a handful of places, so this was sentence editing,
not a script.  Changed: স্তম্ভিত → **স্ট্যাগার্ড** (ch11, 5 places — "স্তম্ভিত" means
*stunned* in Bangla and is simply not the word for a staggered joint; the book's own
habit is to transliterate the trade term, as with ওয়েস্টার্ন ইউনিয়ন and পিগটেল.
**The rename had to reach the artwork too** — `dia_ch11.d11_fixture` printed the old
word in its sheet title *and* in a panel header, so the picture would have contradicted
the prose.  A repo-wide normalized sweep for every renamed term is the check that caught
it; a `git grep` would not have, for the nukta reason above.  `d11_fixture.svg`
re-rendered, `qc.py dia_ch11` **0 problems**, figure looked at, ch11 still 24 pp.) ·
নিয়মনিষ্ঠ → নিয়ম মেনে করা · অবিচ্ছিন্ন → বাধা দেবে না · ক্ষয়রোধী → মরিচা ধরবে না ·
পরিচ্ছন্ন ও ছিমছাম → পরিষ্কার ও গোছানো · সহজলভ্য → হাতের নাগালে (×3) · ভাগ্যক্রমে →
ভালো দিক হলো · অগ্রভাগ → মাথা · অক্ষত → ভালো · অহেতুক → বিনা কারণে · জোড়াতালির →
জোড়াতালি দিয়ে করা · সংকর ধাতু glossed once · অন্তরক → ইনসুলেটিং · বাধ্যবাধকতা → বাধা ·
ধারকত্ব → ক্যাপাসিট্যান্স বা ধারকত্ব · উত্তীর্ণ → পাস করা · সংস্পর্শ → কন্টাক্ট (ch13
×2, ch14 ×1) · শৃঙ্খল → সারি · বিভ্রান্তি → গোলমাল · একঘেয়ে → প্রায় একই রকম · স্তম্ভের
→ খুঁটির · সত্যক ছক → ট্রুথ টেবিল · উত্তরসূরি → আধুনিক রূপ · অপ্রীতিকর → বিরক্তির কারণ ·
খেসারত দেয় → ভোগান্তি পোহায় · রেওয়াজ → চল / নিয়ম · নিষেধাজ্ঞা → নিষেধ · প্রয়োগক্ষেত্র →
কোথায় কোনটি ব্যবহার হয় (×2) · বিন্যাস → নিয়ম · সমষ্টি → মিলিয়ে তৈরি (×2) · অপরিবাহী →
বিদ্যুৎ চালায় না · ঐচ্ছিক → ইচ্ছার ব্যাপার · পরিদর্শন-তালিকা → পরীক্ষার তালিকা ·
গৃহকর্তা → বাড়ির মালিক।

**Page-foot gaps — what worked:**
- **ch13** — the longer tip box in §১৩.২ stranded the টু-ওয়ে সুইচের ছবি with an
  **11.41 cm** gap on p4.  Fixed by putting the **photo before the tip box** (see the
  switch, then the advice on buying it): back to 21 pp with only its three pre-existing
  4.81 / 4.83 / 4.88 cm gaps.
- **ch14** — the new content pushed it to 31 pp and stranded উদাহরণ ১৪.৪ (5.74 cm on
  p23).  Closed by moving §১৪.৮.৩'s **"মোট দর" paragraph from after the example to
  before it** — the ch18 lesson: content moved *ahead* of an unsplittable block fills
  the page the block could not fit on.  Zero gaps.  *Beware the mechanical version of
  this move*: deleting `TAIL + "    "` also ate the following line's indent and produced
  an `IndentationError`.  Move blocks, then re-check the file parses.
- **ch15** — the new §১৫.৩ fuse paragraph stranded the ডিপি সুইচ photo pair (5.06 cm on
  p6); fixed by moving **its explaining paragraph ahead of the figure** and rewording
  "পেছনের ছবিতে" → "নিচের ছবিতে".  The chapter's own **long-standing 6.64 cm gap on p15
  is now gone too** — the owed gang-counting paragraph above fills exactly that foot.
  ch15 is **24 pp with zero gaps**, better than before this pass.  (CLAUDE.md's older
  note that four reorderings had failed on that gap is superseded: the fix was not a
  reordering, it was content that was missing anyway.)

**Verified after the pass:** all five rebuilt; `layout.py` clean on ch11/12/14/15 and
ch13 unchanged at its three ~4.8 cm gaps; `mathguard.py` clean on all five; no `§`
anywhere; MCQ keys still balanced (ch11 ক৪খ৪গ৩ঘ৩ · ch12 ক৪খ৪গ৩ঘ৩ · ch13 ক৪খ৪গ৩ঘ৩ ·
ch14 ক৪খ৪গ৪ঘ৪ · ch15 ক৪খ৩গ৩ঘ৪); figures/tables unchanged (15/9 · 12/10 · 12/7 · 15/8 ·
12/8) since **only one diagram was touched — `d11_fixture`, for the স্ট্যাগার্ড
rename; the figure/table numbering did not move**.  Every new passage was read back out
of the built PDF, not just out of the source.

**Re-merged: 793 → 795 pages** (506.2 MB `.docx`, 44.7 MB PDF).  `bake:` reported 392
anchors resolved and the shipped `document.xml` has **0 PAGEREF, 0 fldChar**.  The
running STYLEREF header was checked on every page that changed (219 · 243 · 269 · 293 ·
323) and on p795, and each names its own chapter.  **The merge was restarted twice** —
once because the ch14 wire-count bullet still needed the ইসিসি clarification, once
because `dia_ch11` was found still printing "স্তম্ভিত".  Rebuild the chapter, re-copy
its deliverable to `Book/`, *then* merge; a merge already in flight is using whatever
was in `out/` when it started.

## Chapters 16–22 recheck, 2026-09-09 (full book only — the digest was NOT touched)

Same ask as the 1–10 and 11–15 rechecks ("chapter 16-22 recheck daw … kothin word
… sohoj koro … onek sentence … purno koro … fact vul hole thik koro … topic missing
thakle add koro … final book e merge kore daw").  `smNN.py` left alone.  **No chapter's
page count moved** — ch16–22 stayed **19 / 19 / 26 / 36 / 24 / 29 / 52**, figures/tables
unchanged (6/7 · 5/8 · 9/10 · 16/19 · 13/10 · 14/6 · 24/21), no diagram touched, every
pre-existing page-foot gap unchanged (ch16 p11 4.56 · ch18 4.93/4.56/4.55 · ch19 p5
4.80), no new gap.  This range had already had the 2026-09-05 digest accuracy review's
"fixes applied to BOTH books" — but several of those never actually reached the full
book, and this pass closed them:

- **ch16 উদাহরণ ১৬.১ note** still said a 2000 W / 8.7 A immersion rod needs "১৫A সকেট"
  — the digest reconciliation settled on "১৩A বা তার বেশি রেটিংয়ের সকেট, আর নিজস্ব
  একটি সার্কিট" (BNBC 1.3.9.3.6).  Now matches.
- **ch17 সারণি ১৭.৩** ষষ্ঠ ধাপ read "৬০০-এর ঊর্ধ্বে" → "৬০০-এর বেশি" (the digest's
  sm17 ঊর্ধ্বে→বেশি swap, full book had missed it).
- **ch22 উদাহরণ ২২.১ note** jumped 10.9 → 16 A with no mention of **13 A** (which is in
  IEC 60898-1's series and in the book's own সারণি ২২.১২.২).  Note now says 13 A is
  enough but is not stocked in Bangladesh, so 16 A.
- **ch19 সারণি ১৯.১ cell** "দ্রুত বদল, নিরবচ্ছিন্নতা" → "দ্রুত বদল, লোড একটানা চলা".

**Two genuine errors fixed:**
- **ch22 সারসংক্ষেপ** printed `I = P ÷ (V × cos φ)` — Kalpurush renders `÷` as `+`, so
  the summary formula was literally wrong on the page.  → `I = P / (V × cos φ)` (the
  same fix ch18's summary already carries).
- **ch22 §২২.৫.৫** pointed at "২২.১২.৭-এ ওই হিসাবটি উদাহরণসহ" for the fault-current
  calculation — that example (উদাহরণ ৫) is in **§২২.১২.৬**; §২২.১২.৭ is সিলেক্টিভিটি.
  Cross-ref corrected.

**Formality slips fixed** (regressions the 2026-08-31 pass missed — অনুশীলনী গ/ঘ are
আপনি):  ch19 গ.২ "ব্যাখ্যা করো" → "করুন"; ch21 ঘ.৪ "বের করো" → "করুন"; ch22 গ.৯
"করে দেখাও" → "করে দেখান".

**Missing topic added:**  ch18's nameplate সারণি has an RPM row but the chapter never
said why it reads 1440/2880 and not 1500/3000 — the RPM cell now names **স্লিপ** in
one clause (no new paragraph, no page growth).

**Hard words simplified** (sentence-level, not a script — a normalized sweep of ~45
candidates found them sparse):  পরিপার্শ্ব → চারপাশের তাপমাত্রা (ch21 §২১.৬.১, ch22
§২২.৫.৩ + two marking-table cells) · ষড়ভুজ মাথা → ছয় কোণা মাথা (ch21) · দ্বিরঙা →
দুই রঙের (ch21) · অনাবৃত → একখণ্ড … খোলা পড়ে থাকা (ch21) · সংকীর্ণ → তালিকা আরও ছোট
(ch22) · বাধ্যবাধকতা → বাধ্যতামূলক করা হয়নি (ch22) · কেন্দ্রাতিগ বল → ঘোরার টান
(ch18) · সারচিত্র → এক নজরে সাজানো, অবহেলিত → সবচেয়ে কম যত্ন পায়, বণ্টিত → ভাগ করা
(ch16) · গৌণ → তত জরুরি নয় (ch19).  `নিরবচ্ছিন্ন` kept once in ch19's পারিভাষিক table
(it *is* the meaning of "Uninterruptible").

**ch18 §১৮.৯.৪ note** ("অথচ ১ অশ্বশক্তির ০.৭০ দক্ষতা ধরে কষলে আসে ১০.৯ A") was
telegraphic — reworded to say plainly it is *the same 2 HP motor* recomputed with the
1 HP's 0.70 efficiency, which is what অধ্যায় ২০ uses.  The 10.2-vs-10.9 A gap stays
disclosed, table unchanged (do not "fix" to one number — standing rule).

**Verified:** all 7 rebuilt, `mathguard` clean, no `§`, `layout.py` shows the same
page counts and the same pre-existing gaps, MCQ keys untouched (all already balanced),
every cross-chapter `অধ্যায় N` reference checked valid.  Re-merged twice (the ch22
পরিপার্শ্ব cell was caught after the first merge started — the standing "rebuild,
re-copy, then merge" rule).  **Merged book unchanged at 803 pages** (506.3 MB `.docx`,
45.1 MB PDF); `bake:` 392 anchors resolved; shipped `document.xml` has 0 PAGEREF, 0
fldChar; STYLEREF header intact.  Deliverables + preview PDFs for ch16–22 copied to
`Book/`.

## Chapter 1 — "English terms in table name-columns" + plain-language edits, 2026-09-09

User asked for a set of ch01 fixes, then **explicitly scoped it to ch01 only** —
"chapter 1 avabey thakuk, ar tumi baki chapter korte hobe na" — so 2–10 were
**not** touched (an earlier plan to roll this out to 1–10 was cancelled by the
user).  What changed in `ch01.py` (page count **29 → 31**, `layout.py` clean bar
one 4.25 cm foot-gap on p13, `mathguard` clean, no `§`):

- **`পেরেক বেঁধা` → `পায়ে পেরেক ঢোকা`** (সারণি ১.৫, সেফটি শু row).
- **`নতুন দিয়ে বদলে নিতে হবে` → `বাতিল করে সঙ্গে সঙ্গে নতুন আরেকটি ব্যবহার করতে
  হবে`** (১.৫.২).
- **মই section (১.৬.৪):** `সতর্কতা অত্যন্ত জরুরি` → `সতর্ক থাকা জরুরি`; the 4:1 rule
  reworded plainly; added "মইয়ের গোড়া বসাতে হবে শক্ত ও সমতল মেঝেতে; নরম মাটি,
  বালি বা ভেজা মেঝেতে নয়।"; bullet 3 `সর্বোচ্চ তিন ধাপ … মাড়ানো যাবে না` →
  `সবচেয়ে উপরের তিনটি ধাপে কখনো পা রাখা বা দাঁড়ানো যাবে না`.
- **New dress-code bullets under ১.৪.১** (গায়ে-ফিট পোশাক, ঢিলা জামা/ওড়না/টাই
  ঘূর্ণমান যন্ত্রে বিপদ, গয়না খুলে রাখা, চুল বাঁধা, ইনসুলেটেড সোলের জুতা).
- **`রাইট অফ ওয়ে` → `রাইট অব ওয়ে`** in ১.২.২, and a **new §১.৭.৩ "লাইন ক্লিয়ারেন্স
  ও রাইট অব ওয়ে"** (2 paras — বিতরণ কর্তৃপক্ষের লিখিত অনুমতি / permit-to-work,
  নিরাপদ দূরত্ব ১ মি / ৩ মি, "কতটা দূরত্ব বিতরণ অফিস থেকে জেনে নিতে হবে").  One
  short question added to খ; glossary rows added.  Distances are framed as
  general practice + "consult the utility" — **no BNBC clause was invented**
  (a web search found no verifiable BD ROW clause).
- **English glosses in prose** — `(English)` in brackets on first mention for
  শাট-ডাউন, ফেজিং টেস্ট, ভোল্টেজ টেস্টার, গ্রাউন্ডিং, ক্যাপাসিটর ডিসচার্জ, ফিউজ
  কাট-আউট, ফিডার, কন্ডাক্টর, লুজ কানেকশন, ইনসুলেশন রেজিস্ট্যান্স, প্রোব, রিকভারি
  পজিশন, স্প্লিন্ট.
- **পারিভাষিক শব্দ (১.১৪) expanded 12 → 37 rows** so every transliterated
  technical term in the chapter is listed.
- **The headline ask — table name-columns:** the user circled সারণি ১.৯'s
  "জীবাণুমুক্ত ভেজা ওয়াইপস" and said (after two rounds of clarification) that in
  **every table's name/label column**, an English-origin word should be written
  in **Latin script**, keeping the surrounding Bangla words — *not* a
  parenthetical gloss.  So: `জীবাণুমুক্ত ভেজা ওয়াইপস` → `জীবাণুমুক্ত ভেজা Wipes`;
  `নাইট্রিল গ্লাভস` → `Nitrile Gloves`; `সেফটি হেলমেট` → `Safety Helmet`; `আর্ক
  ফ্ল্যাশ` → `Arc Flash`; `শক` → `Shock`; etc.  Applied to সারণি ১.১, ১.২, ১.৩,
  ১.৫ (PPE), ১.৮ (extinguisher column), ১.৯ (first-aid box — the circled one),
  and the ১.১৫.৪ practical-work "প্রয়োজনীয় সরঞ্জাম" column.  Descriptive columns,
  prose, headers and **diagram labels were left in Bangla** — the user was asked
  about diagram labels (e.g. চিত্র ১.৪ still says "সেফটি হেলমেট") and about any
  further ch01 changes, and answered "chapter 1 avabey thakuk" (leave it as is).
- **Layout:** the bigger tables stranded d12_hierarchy with a ~6 cm gap on the
  ঝুঁকি-নিরূপণ page; fixed with the standing playbook — moved `d12_hierarchy`
  up to right after §১.১২'s intro paragraph (before the 5-step list), and the
  closing HoC paragraph now reads "…ধাপক্রম (উপরের চিত্র)…".
- **Re-merged** with `mkbook.py` (only `out/অধ্যায়-০১*.docx` rebuilt; the other
  27 were current).  **795 → 797 pages**, 506.2 MB `.docx`, 44.8 MB PDF; `bake:`
  392 anchors resolved; PDF re-rendered via `soffice` (disk was down to ~3 GB
  free — watch this).  Deliverables copied to `Book/অধ্যায়-০১ — …docx` and
  `Book/অধ্যায়-০১/প্রিভিউ — অধ্যায় ০১.pdf`.
- The "button that shows a number on some pages" the user reported turned out to
  be the **PDF viewer's own page-position pill** (a screenshot showed "20 / 31"
  top-left and "10" in the toolbar) — not anything in the document.  Nothing to
  fix; the per-chapter files carry no body fields/links/widgets, only the footer
  `PAGE` field and one OMML `I = V/R`.

## Chapters 2–10 — English terms added to the পারিভাষিক শব্দ tables only, 2026-09-09

Follow-up to the ch01 edit above.  The user's instruction: **"chapter 2-10 e
english korte hobe na .. tumi porivasa part e english ta add kore daw ..
equipment er name guloo english lekhe dio porivasa part e"** — i.e. do **not**
touch ch2–10 body/tables the way ch01's name-columns were changed; instead, in
each chapter's **পারিভাষিক শব্দ table only**, make sure every transliterated
English technical term **and every equipment/tool name** used in the chapter is
listed, with the English form (Latin) in the "ইংরেজি পরিভাষা" column.  Nothing
else in ch2–10 changed — no body prose, no other tables, no diagrams.

Rows added per chapter (existing rows kept, new ones interleaved by first
appearance):
- **ch02** (tools) 13 → ~55 rows — every hand tool, power tool, measuring/marking
  tool and wiring aid (Screwdriver, Line Tester, Combination/Diagonal/Long-nose
  Pliers, Wire Stripper, Crimping Pliers, Ball Pein/Claw/Cross Pein Hammer,
  Mallet, Adjustable Wrench, Allen Key, Bench Vice, Hacksaw Frame, Junior
  Hacksaw, Hand Saw, File, Cold Chisel, Measuring Tape, Spirit Level, Try
  Square, Plumb Bob, Wire Gauge, Tool Box, Spring Wire, Work Light, Electric
  Drill, Rotary Hammer, Angle Grinder, Wall Chaser, Cordless Driver, Heat Gun,
  Blower, Vacuum Cleaner, Voltage Detector, Heat-shrink Sleeve, Conduit, SWG,
  SELV, BS 7671, Two-pole Voltage Detector).  **21 → 23 pp.**  *2026-09-09,
  user review:* `Cross Pein Hammer`/`Ball Pein Hammer` → `Cross Pin Hammer`/
  `Ball Pin Hammer` (the book's Bangla is ক্রস/বল পিন, so "Pin" not the
  standard "Pein").  And §২.৩.৭'s `স্প্রিং ওয়্যার` entry was a naming error —
  `assets/ch02/spring_wire.png` is a blue coiled **draw-wire/fish-wire**, but the
  table's description ("কন্ডুইট বাঁকানোর আগে পাইপের ভেতরে ঢুকিয়ে… পাইপ চ্যাপ্টা
  হয়ে না যায়") is a **bending spring**'s job.  Relabelled to `স্প্রিং বেন্ডার`
  (Bending Spring) in the সারণি, MCQ option and glossary; its description was
  already correct and stays.  *Follow-up:* the user then supplied a bending-
  spring product photo (`sys-master_root_h2b_h5b_…jpeg` at the project root) and
  asked to keep **spring wire too** — `assets/ch02/spring_bender.png` was cropped
  from it (PIL white-bg autocrop), and §২.৩.৭ now shows **both**: ফিশ ওয়্যার ·
  স্প্রিং ওয়্যার (the blue coil `spring_wire.png`, description restored — a
  spring-steel draw-wire, same job as fish wire) · স্প্রিং বেন্ডার (the new
  photo) · ওয়ার্ক লাইট, at per_row=4 (মই moved to the সারণি only, to keep the
  figure_row one line).  The user then asked for the মই tile back too, so
  §২.৩.৭'s figure_row is now **5 tiles at per_row=5** (ফিশ ওয়্যার · স্প্রিং
  ওয়্যার · স্প্রিং বেন্ডার · মই · ওয়ার্ক লাইট) — one row, ~2.6 cm thumbs, no
  page growth (per_row=3's 3+2 layout was what opened the 6.5 cm gap on the
  fussy `d05_drill_zones` p15).  Glossary has both `Spring Wire` and `Bending
  Spring` rows.  ch02 stays **23 pp**, `layout.py` clean.
- **ch03** 12 → 25 (Lamp, Angle Holder, Bayonet Cap/Edison Screw, Ceiling Rose,
  Terminal Block, Flexible Cord, One-way Switch, Phase/Neutral, Earth Busbar,
  Earth Electrode, Ceiling Fan).  17 pp unchanged.
- **ch04** 16 → 35 (Cycle, Hertz, Coulomb, Conductor, Insulator, Semiconductor,
  Resistor, Capacitor, Inductor, Battery, Generator, Transformer, Solar Cell,
  Multimeter, Ammeter, Voltmeter, Ohmmeter, Energy Meter, Phase, Neutral,
  Ground/Earth).  **20 → 21 pp.**
- **ch05** 12 → 36 (Copper, Aluminium, Mica, Porcelain, Silicone Rubber,
  Bakelite, Bi-metal Lug, Galvanic Corrosion, and the standard IEC 60617 symbol
  devices — One-/Two-way Switch, Push Button, Regulator, Fuse, MCB, Socket,
  Bell, Buzzer, Indicator Lamp, Motor, Cell/Battery, Ammeter, Voltmeter, Earth
  Symbol, Connection Diagram).  **14 → 15 pp.**
- **ch06** 10 → 20 (Make-and-break, Leaf Spring, Calling Bell, Chime, Siren,
  Bell Transformer, Terminal, Series/Parallel Connection, Annunciator).  14 pp
  unchanged.
- **ch07** 14 → 20 (Multimeter, Lamp/Bulb, Resistor, Battery/Cell, Switch,
  Fuse).  24 pp unchanged.
- **ch08** 16 → 27 (Analog/Digital/Panel Meter, Ammeter, Voltmeter, Ohmmeter,
  Galvanometer, Current Transformer, Test Lead/Probe, Insulation Tester, Earth
  Tester, Earth Resistance).  21 pp unchanged.
- **ch09** 12 → 18 (Extension Board, Terminal, Rocker Switch, Shutter, Surge
  Protector, Rating, Neon Lamp).  18 pp unchanged.
- **ch10** 12 → 22 (Test Board, Lamp Holder, LED Lamp, CFL, Plug, Socket,
  Switch, Terminal, Crocodile Clip, Multimeter, Megger).  **17 → 18 pp.**

All nine rebuilt, `layout.py` clean at 4.5 cm on every one (ch04's pre-existing
p9 4.78 cm gap is unrelated to the glossary, which sits at chapter end);
`mathguard` clean.  Deliverables copied to `Book/`.  **Merged book +5 pp overall
(2×ch02, 1× each ch04/ch05/ch10) — re-run `mkbook.py`.**

## Chapter 1 — table English swap reverted, glossary kept + extended, 2026-09-09

The user changed the call on ch01 the day after: **"chapter 1 ew same kaj kore
daw .. bangla rakho .. kintu porivasay sob add rakho"** — i.e. treat ch01 like
ch2–10: **body/tables back to Bangla, English only in the পারিভাষিক শব্দ table.**
So the 2026-09-09 "English terms in table name-columns" work above was **reverted**:

- All 29 table name-column Latin swaps undone (সারণি ১.১/১.২/১.৩/১.৫/১.৮/১.৯ and
  the ১.১৫.৪ practical-work equipment column back to `সেফটি হেলমেট`, `নাইট্রিল
  গ্লাভস`, `জীবাণুমুক্ত ভেজা ওয়াইপস`, `আর্ক ফ্ল্যাশ`, `বৈদ্যুতিক শক`, …).
- The prose `(English)` parentheticals I had added (শাট-ডাউন, ফেজিং টেস্ট,
  ভোল্টেজ টেস্টার, গ্রাউন্ডিং, ক্যাপাসিটর ডিসচার্জ, ফিউজ কাট-আউট, ফিডার,
  কন্ডাক্টর, লুজ কানেকশন, ইনসুলেশন রেজিস্ট্যান্স, প্রোব, রিকভারি পজিশন, স্প্লিন্ট,
  and the §১.৭.৩ Line Clearance / Permit to Work brackets) all removed.  The
  pre-existing `(Right of Way)` / `(Overloaded)` / `(Red-hot)` / `(Risk
  Assessment)` brackets that were in ch01 before this session are untouched.
- **Kept**: every non-English content fix — `পায়ে পেরেক ঢোকা`, `বাতিল করে নতুন
  আরেকটি ব্যবহার করতে হবে`, the ladder rewording + `সবচেয়ে উপরের তিনটি ধাপে …`,
  the ১.৪.১ dress-code bullets, the new **§১.৭.৩ লাইন ক্লিয়ারেন্স ও রাইট অব ওয়ে**
  (headings/prose all Bangla now), the `রাইট অফ ওয়ে → রাইট অব ওয়ে` fix, and the
  short question.
- **পারিভাষিক শব্দ (১.১৪) kept and extended to ~61 rows** — the earlier 37-row
  expansion plus the ch2–10-style equipment/PPE/first-aid names (Safety Helmet,
  Safety Goggles, Insulated Hand Gloves, Ear Plug/Muff, Safety Shoes, Reflective
  Apron, Dust Mask, Ladder, Line Tester, Padlock, Lockout Device, Tag, Fire
  Extinguisher, CO₂ Extinguisher, Fire Class, Ventricular Fibrillation, First
  Aid Box, Bandage/Gauze, Adhesive Dressing, Antiseptic, Microporous Tape,
  Nitrile Gloves, Tweezers, Triangular Bandage).
- **Layout:** the bigger glossary + Bangla-again first-aid table stranded
  `d10_rescue` (6.2 cm gap on the উদ্ধার page); fixed by moving `d10_rescue` up
  to right after the ⚠ box, before the 5-step list.  ch01 **31 → 32 pp**;
  `layout.py` clean bar the pre-existing p13 4.25 cm.

## Full-book language review + chapters 1–6 applied, 2026-10-14

The user asked for the whole book to read as human, formal, student-friendly
prose (no AI tells, no hard words, no broken sentences, better headings), and
explicitly forbade using any "human Bangla" skill. Every chapter was reviewed
line by line; the findings (exact «বর্তমান» → «প্রস্তাব» pairs, heading tables,
fact flags) are committed in `docs/review/পর্যালোচনা — অধ্যায় *.md`.
**Chapters 1–6 were then applied** (user: "1 theke 6 pojonto change kore amar
Full book e thik kore daw … diagram change korte hobe na"):
- Only `chNN.py` text changed — no artwork. Em-dashes 334 → ~10 across ch1–6
  (list labels `**X:**`, box titles `সংজ্ঞা: X`, table cells `X: Y`), headings
  as noun phrases, সার্কিট over বর্তনী (defined once), বেল over ঘণ্টা,
  শ্রেণি/রং/শুকনো/পুরোনো, ক্যাবল for cable, future-tense refs to later
  chapters, plus the review's fact fixes (arc flash, socket "earth pin",
  foam MCQ → বালু, ch02 §২.৬.২ "অনুমোদিত অঞ্চল", ch03 সুইচ অন/অফ and earth-pin
  logic, ch04 run capacitor + 350–450 V reasoning + heater example, ch05
  valence 5–8 and doping, ch06 indicator-lamp tip).
- ch01's user-written fuse box, ladder lines, «পায়ে পেরেক ঢোকা» and rule ৭ were
  deliberately left untouched. ch03/ch06's circuit loops now take the figure
  caption with `title.split(": ", 1)[1]` (headings use a colon, not a dash).
- Page counts unchanged (32/23/17/21/15/14); only ch04 has a new 4.60 cm gap
  (p8) beside its old 4.78 cm. ch05's four symbol charts again pack two per
  page — the text before them had to be trimmed back to fit.
- `render.py`/`svgkit.py` read Chrome from `$CHROME_BIN` (cloud container:
  `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`); Kalpurush must be
  installed system-wide (`/usr/local/share/fonts`) for LibreOffice.
- **Chapters 7–14 applied the same way on 2026-10-14** (user: "chapter 6 theke
  chapter 14 koro … sob kisu ready kore rakhba … ami ekbare sese merge korte
  bolle merge korba"). Per-chapter `.docx` + preview PDFs in `Book/` are
  rebuilt; **the full book was NOT re-merged**, the user will ask. Pages
  ch07–14: 24 / 22 / 18 / 18 / 26 / 26 / 21 / 32 (ch08 +1, ch11 +2, ch12 +1,
  ch14 +1; ch13 21 with its three old ~4.8 cm gaps gone). `layout.py` clean on
  all eight. Fact fixes worth keeping: ch07 mixed-circuit rule ("innermost part
  first", not "parallel first"), series-board row (indicator is the parallel
  part), bell transformer is not DC; ch08 CAT categories are IEC 61010-2-030,
  body on a probe is in *parallel* (reading drops), clamp-meter leakage needs a
  mA leakage clamp, RCCB (not MCB) row; ch09 gang board gets a fuse in text
  (figure is the institute's slide, unchanged), one heat-appliance rule;
  ch10 definition box no longer puts the indicator in series, the test-lamp
  "dim = OK" rule is conditional on load ≤ lamp, insulation 1 MΩ (IEC) vs
  5 MΩ (BNBC, book takes 5); ch11 copper "ক্ষয়" not "মরিচা", married-joint
  centre strand cut *shorter*; ch12 coil regulator saves "little", not
  nothing, 90° is electrical; ch13 intermediate-switch miswire gives erratic
  control, not an MCB trip; ch14 diversity vs demand factor noted in prose,
  chase depth 1/3 vertical vs 1/6 horizontal. ch08's chapter title keeps
  "ইন্সট্রুমেন্টস" (file name / TOC decision pending), body uses ইনস্ট্রুমেন্ট.
- Chapters 15–28 are reviewed but **not yet applied**; the review files list
  ~12 open book-wide decisions (acronym script, থ্রি-ওয়ে meaning, diversity vs
  demand factor, SPD position in ch22 vs ch25, insulation test values …).

## Open items

- ch18 has three ~4.5–5 cm page-foot gaps (4.93 / 4.56 / 4.55 cm),
  and ch19 one (4.80 cm on p5, where `d03_types` is too tall to follow
  §১৯.২.১); each is a `worked_example` or a figure that could not be pulled
  up further.  ch22 has none above 3.95 cm — the two photo rows added
  on 2026-08-23 reflowed everything after §২২.৪, and the three moves
  that cleared the new gaps were all from the standing playbook:
  `d09_poles` pushed past the BNBC paragraph that explains it,
  `d12_rccb_work` pulled *up* to the paragraph it illustrates, and an
  opening paragraph written for §২২.৭.২, which had begun with a figure
  straight under its heading (the ch17 rule).
- ch19 used to end on a header-only page 36 (the empty paragraph after the
  final ❖ চিত্রসূত্র box). With the credit boxes removed (2026-08-30) ch19 is
  35 pages and the artefact is gone; if any chapter still shows a trailing
  header-only page it is harmless and disappears when the chapters are merged.
- Appendix ক (symbol chart) can reuse the four sheets from `dia_ch05.py`.
- **The merge is done and shipping — all 28 chapters** — `mkbook.py`
  (2026-08-31; extended to 1–28 on 2026-09-04, section-level সূচিপত্র and
  running header added 2026-09-08) produces one file with continuous page
  numbers and a clickable chapter-**and-section** সূচিপত্র whose page numbers
  are baked in as static text; **chapters 1–28 → 803 pages** (506.2 MB `.docx`,
  45.1 MB PDF).  (786 → 787 on 2026-09-08 when ch01's CPR figure became
  step-by-step prose; 787 → 793 with the chapters 1–10 recheck; 793 → 795 with
  the chapters 11–15 recheck on 2026-09-09; 795 → 797 with the ch01
  "English terms in table name-columns" edit, then 797 → 803 when that ch01 edit
  was reverted to Bangla and the পারিভাষিক শব্দ tables of ch01–ch10 were given
  the English equipment names instead — all 2026-09-09, see the two dated notes
  below.  `bake:` reports 392 anchors every time — the section count has not
  moved, since none of these were section changes.)
  `DEST`, `chapter_list()`'s `1 <= n <= 28`, and `main()`'s
  `range(1, 29)` assert are all bumped. Still owed: চিত্রসূচি and
  সারণিসূচি (every chapter's `Book` object already collects `b.figures` /
  `b.tables`, so both lists can be generated rather than typed), and a
  section-level TOC if the user wants one.
- ~~**The 28-entry সূচিপত্র fills its page exactly**~~ — superseded
  2026-09-08. The সূচিপত্র now carries 392 lines over ten pages (p3–p12)
  and chapter 1 opens on p13. The trailing "পরিশিষ্ট …" note paragraph
  removed on 2026-09-04 stays removed (the imprint page already says it).
- **`mkbook.shrink_trailing_para()` — added 2026-09-04.** python-docx puts an
  empty paragraph after each chapter's final table (Word requires one). At
  11 pt that half-line could tip past a page boundary and strand a
  **header-only blank page** in the merged book — it was NOT reliably
  "disappearing on merge" as the note above hoped. The helper squashes that
  trailing empty para to ~1 pt (font size + paragraph-mark `w:sz` = 2) right
  before `composer.append`; it is the last element in the chapter so nothing
  above it moves. Combined with three tail trims — ch03 dropped a redundant
  ব্যবহারিক-কাজ row, ch23/ch27 tightened a few table cells — the merged book
  now has **zero near-empty pages** (checked: no page under 220 chars & >95 %
  white except the cover). Keep the helper when copying `mkbook.py` forward.
- **Every chapter still ends mid-page** — the অনুশীলনী closes on the ঙ
  ব্যবহারিক-কাজ table, and `pageBreakBefore` starts the next chapter fresh,
  so a chapter-end page is typically 60–90 % full then whitespace. That is
  normal book layout, not a gap to chase; only a page carrying a *fragment*
  of a table alone (ch03/23/27's old state) was worth fixing.
- **Page 1 (the cover) scans as "near-black"** (navy field, mean L≈49).
  That is the approved 2026-08-31 one-continuous-sheet design
  (commit 345892e), not a defect — do not "fix" it without the user
  asking.

**What `mkbook.py` had to work around, do not re-derive:**
- **docxcompose drops every appended document's body `sectPr`.** So the merged
  file cannot keep per-chapter running headers — it gets one book-wide header
  instead, set on the front-matter section. Chapters still start on a fresh
  page because `inject_chapter_start()` prepends a tiny `pageBreakBefore`
  paragraph carrying `bookmarkStart _chNN`; that bookmark is also what the
  সূচিপত্র links to (`w:hyperlink w:anchor` + `PAGEREF _chNN \h`, dotted right
  tab). `<w:updateFields val="true"/>` makes Word offer to refresh the page
  numbers on open and makes LibreOffice resolve them on PDF export.
- **The cover is a full-bleed image, and it must be *anchored*.** An inline
  picture carries line leading, so a page-height one spills onto page 2;
  `full_page_picture()` rewrites python-docx's `wp:inline` into a page-relative
  `wp:anchor` with `behindDoc`, which takes no room in the text flow. It lives
  in its own **zero-margin section**, so the merged book has two sections:
  0 = cover (no header, no footer, no page number), 1 = everything else.
- **A cover split into a white band over a navy field was rejected**
  ("cover page upore sada niche nil..amon na", 2026-08-31). The white band
  existed only because the logo's `RAPTI` wordmark is near-black and vanishes
  on navy. The fix is `_light_wordmark()` in `assets_cover.py`: it recolours
  the wordmark's RGB to white while **keeping the alpha untouched**, so the
  antialiased edges stay correct on any ground, and leaves the emblem alone
  (the emblem is already white + bright blue and reads fine on navy). The
  wordmark starts at x = 137 — columns 130–142 of the source PNG are fully
  transparent, which is how the split point was found, not by eye. The cover
  is now one continuous navy field: gradient + a faint two-level blueprint
  grid + a gold sheet border + the circuit motif, i.e. a drawing sheet.
- **The blueprint grid is two `<pattern>` fills added with `s.add()`, not
  `s.rect()`.** `qc.py` scores every recorded line against every text box, and
  a background grid runs under the lettering *by design* — recording it would
  produce a page of false `line crosses` reports. Same reasoning as the
  `<g opacity>` wrapper: decoration, not geometry that can collide.
- **The cover ships as PNG only, no SVG** — unlike every interior figure. A
  reader without Kalpurush would otherwise get a broken cover, and nobody
  edits a cover in Word.
- **`svgkit.line()` has no `opacity` argument.** Giving each shape its own
  opacity left the motif's lines solid and only its circles faint; the whole
  motif goes inside one `<g opacity="0.42">` instead.
- **`bookkit.Book.spacer(N)` is near-zero-height in LibreOffice** for large N
  (it is an empty run), so vertical space on a generated page has to come from
  `space_after` — that is what `vgap()` in `mkbook.py` does.
- RAPTI's details come from **rapti.net** (about.php / contact.php): est. 2019;
  `2101, Bhuighar, Rupayan Town, Near Gate-1, Fatullah, Narayanganj-1420` —
  **Bhuighar is ভুইঘর in Bangla** (the user corrected an earlier ভূঁইগাঁও);
  hotline 01617-345534, also 01685-953204 and 01766-221733; WhatsApp
  +8801617345534; `raptibd@gmail.com` (Cloudflare-obfuscated on the page —
  decode the `data-cfemail` hex: first byte is the XOR key); rapti.net;
  facebook.com/resonanceautomationbd. The logo is `rapti.net/assets/images/
  logo_ippi.png` (356×130, transparent) — `assets_cover.py` flattens it onto
  white and asserts the pixel size. Placed 264 px wide on the 1240 px canvas
  it prints at ~205 dpi; larger and the wordmark goes soft.
- Page-foot gaps are **not** re-checked after merging — each chapter was
  already cleared on its own, and `pageBreakBefore` means no chapter's content
  can flow into another's.

## Next step

**All 28 chapters are delivered and merged** (`mkbook.py`, 1–28, 762 pp,
2026-09-04).  What is left is the appendices and the চিত্রসূচি/সারণিসূচি:

- **পরিশিষ্ট ক** (symbol chart) can reuse the four sheets from `dia_ch05.py`.
- **পরিশিষ্ট খ/গ** (standard cable & breaker tables, breaker markings) can be
  assembled from ch22's সারণি ২২.x and ch23's সারণি ২৩.x — both are computed,
  so they can be regenerated rather than retyped.
- **পরিশিষ্ট ঘ** — সোলার সিস্টেম পরিচিতি.  `Solar System.docx` at the root is
  still unused except for ch19's battery arithmetic.
- **পরিশিষ্ট ঙ/চ** — question bank and sample paper, from `HW Exam
  Question.docx` and `Electrical House Wiring Quistion.docx` (both unused).
- **পরিশিষ্ট ছ/জ** — glossary and formula sheet;  every chapter's পারিভাষিক
  শব্দ table and every `b.math()` call are already in the source, so both can
  be generated.
- **চিত্রসূচি ও সারণিসূচি** for `mkbook.py` — each chapter's `Book` object
  already collects `b.figures` / `b.tables`.
- ~~`mkbook.py`'s `DEST` range and its chapter-list `assert` need bumping to
  1–28 before the next merge.~~  Done 2026-09-04 — `DEST` is now
  `… (অধ্যায় ১–২৮).docx`, `chapter_list()` filters `1 <= n <= 28`, the
  assert is `range(1, 29)`, and the imprint/`kv` copy says "১–২৮".

**Chapter 28's diagrams were reworked on 2026-09-04** (user: "chapter 28 er
diagram gulo onek overlap hoyeche ar sundor hoy nai"), together with ch24's
চিত্র ২৪.১২ and ch26's চিত্র ২৬.১০.  **`qc.py` reported 0 problems on all
three before and after** — every one of these is a class it cannot see, so
they are worth remembering:

- **A stale PNG is not the figure.**  The ch24 and ch28 `.svg` files were
  newer than their `.png`, so the first review pass was reading an old
  render.  Word embeds the **SVG**;  `render.py` the whole directory before
  judging a diagram by eye.
- **A fill drawn after the curve erases the curve.**  d05_depth's amber
  "প্রথম 3 m" band was `s.rect(..., AMBERBG, ...)` *after* the plot, so the
  graph appeared to start at 3 m.  Highlight bands go **before** the data.
- **A label centred on a part is centred on the wire that leaves it.**
  Five figures shipped this way — d01's "ছেঁড়া ইনসুলেশন" on the phase drop,
  d02's "আর্থিং বাসবার" on the earth lead, d12's "কেন্দ্রের ছোঁয়া" on the
  centre-contact wire, and both diameter dimensions in d03.  The fix each
  time is to anchor the text to one side (`"start"`/`"end"`) or, for a
  dimension, to shift it — hence `dim_h(..., tdx=)` and
  `dim_v(..., tpos="top")`, both added to `dia_ch28.py`.
- **A lead drawn after the instrument runs across its own face.**  d08's
  meter had `s.line(px+26, y1+34, px+26, y2_-8)` drawn on top of the box:
  the line crossed "মিটার", the screen and "ওহম".  The meter now sits to the
  **right** of the last test point with one lead into its top edge and one
  into its bottom.
- **Two wires on the same y read as one conductor.**  d12's L and N both ran
  right along `cy+132`, overlapping for 160 px, so the figure showed a single
  wire where the whole point is that they are two.  They leave in opposite
  directions now.
- **Inner leads must run *below* outer leads, never above.**  d15's four
  spike leads were routed inner-high/outer-low, so each inner lead's vertical
  cut the outer lead's horizontal — a knot under the instrument.  One tuple
  (`(338, 374, 374, 338)`) fixes it.
- **A dimension label in the callout margin reads as a callout.**  d04's
  "610 mm" and "380 mm" sat in the same left/right columns as the labels;
  both vertical dims are now **inside the pit** with their text at the top of
  the line, and the callouts are three a side.  Two of them had also been
  aimed at nearly the same point on the cover — "মাটির 38 mm উপরে থাকে" now
  points at the cover's *left* end from above ground.
- **`callout(..., elbow=True)` cuts its own text when the target is under
  the label.**  The elbow's vertical leg runs back up through the printed
  words.  Use a straight leader with the target clear of the text box, or put
  the label at the target's own height so the leader is purely horizontal
  (that is what d04's "পিতলের ক্ল্যাম্প" does now).
- **Dead space was real too** — d01/d02/d04/d05/d09/d11/d13 lost 40–75 px of
  panel or margin each, and d16's tiles now size themselves from their own
  text (`ch = 100 + 32 × lines`) instead of a fixed 168.
- **ch24 চিত্র ২৪.১২:** the earth-electrode symbol was drawn straight down
  from the bar's left end, so its three hatch bars sat on the first
  outgoing breaker.  It now steps out to x = 74, clear of the panel.
- **ch26 চিত্র ২৬.১০:** the pipe's outer circle ran through "…% ভরাট".
  `R` 118 → 100 and `cy` `top+208` → `top+194`;  the label block is
  untouched, so the panel's own proportions did the work.
- **Page counts are unchanged — 38 / 43 / 49 — and so are the gaps**
  (ch24 none > 3.52 cm, ch26 one 4.17 cm, ch28 4.77 and 4.60 cm).  Getting
  ch28 back there took one edit and it was the standing one:  the shorter
  figures re-paginated the chapter and stranded চিত্র ২৮.২ with a 6.43 cm
  gap on p4, closed by **a paragraph that was owed anyway** — §২৮.২.১ now
  says why the water/tube-well pipe and the building's rebar are not earth
  electrodes.  Moving that figure was tried twice first (later → 5.19/9.25 cm;
  as the section-opening figure → 11.34 cm, the ch17 "figure under its own
  heading" trap) and both were reverted.

**Chapter 28's sources and decisions (do not re-discover).**

- **The institute's own material covers both halves of this chapter, and it
  was checked exhaustively.**  `Earthing.docx` and paragraphs 595–653 of
  `Electrical House Wiring book.docx` are **the same text**, and the seven
  images are the same too (image1–7 = image133–139).  Paragraphs 560–572 of
  the book give the institute's own four-test list in exactly the order the
  user asked for, and `HW 1st class.pptx` **s88** is the chapter's own slide
  — but s88 is **text only** (its single image is the page background,
  hash `bbadc9fb`).  All 179 slides of both decks were extracted and read;
  there is no other earthing or test slide.  `Measuring Instruments.docx`
  has no megger and no earth tester — it is ch08's file.
- **The institute's earthing clip-art was used as a drawing reference, not
  embedded** (the ch11 precedent).  It is 450–652 px wide, and image5/6/7
  (rod / pipe / plate) are RGBA with a transparent ground, so they print
  black unless flattened (the ch18 trap).  The electrode sections in
  `dia_ch28.py` are drawn from them.
- **Two errors in the institute's text are corrected openly** (ch20/21/24/25
  rule):  (a) "গ্রাউন্ডিংয়ের তারের রঙ কালো" — black is **neutral** in BNBC
  Table 8.1.2;  earth is green+yellow with no exception (§২৮.১.৪ also
  explains that earthing and grounding are the IEC and NEC words for the
  same thing, and that the split people teach is really system vs equipment
  earthing).  (b) The same file says both "১ ওহম বা তার নিচে" and
  "বাসাবাড়ির জন্য সর্বোচ্চ ৫ ওহম";  BNBC has no 5 anywhere, so §২৮.৪.৫
  prints a table of all four clauses and takes 1.
- **BNBC contradicts itself twice, and both are printed.**  Earth lead:
  1.3.37.3.2's paragraph says `2 × 1.5` mm² but its own sub-item (c) says
  "not smaller than … 2x4mm2" → the book takes 2 × 4.  ECC: 1.3.37.3.1 says
  the minimum is 4.0 mm² but 1.3.8.2.3 says a socket's ECC may be 1.5 →
  the book takes 4, and says the market usually does not.  Same handling as
  ch24's 18-vs-20 SWG.
- **Every photograph is Wikimedia Commons** (`assets_ch28.py`, ch26's
  thumbnail-fetch pattern).  The three that carry the chapter:
  `Isolationsmessgerät 1507.jpg` — a Fluke 1507 reading `>11.0 GΩ` at
  `1050 V` with 1000/500/250/100/50 on the knob, i.e. **IEC 60364-6
  Table 6.1's three test voltages in one photograph**;  `Meger M4100
  pealt.JPG` — a hand-crank megger, literally the "direct indicating
  ohm-meter of the generator type" BNBC 1.3.47.6.1 names;  and
  `HomeEarthRodAustralia1.jpg` — a rod out of the ground with a brass clamp
  and a green-yellow lead, which is clause 1.3.37.3.4 in one frame.
  `Curtin Building 314 main earth.jpg` is an earth-pit cover with **MAIN
  EARTH cast into it** — it labels itself.
- **The neon-tester pair does not teach what its filename suggests, and
  reading the pixels caught it.**  `Voltage test light active/inactive.jpg`
  are the same frame, same socket hole, same live conductor;  the only
  difference is a finger on the cap.  The first caption said "ফেজের ছিদ্রে
  / নিউট্রালের ছিদ্রে", which would have taught a falsehood.  চিত্র ২৮.১৬
  is now "লাইন টেস্টার যেভাবে মিথ্যা বলে" — a better lesson, and honest.
  **General rule, again: look at the photograph before writing its caption.**
  The same check caught `Digital Earth resistance tester.jpg` being a
  **four**-terminal Fluke 1623 with a 3-POLE/4-POLE selector, not the
  three-terminal instrument the first caption claimed.
- **Ch28's arithmetic is ch22/23/25/26/27's nine circuits**, with one new
  column — the ECC from BNBC Table 8.1.27, which forces **4 mm² on every
  final circuit** because the table's floor is 4.  The worst circuit's ECC
  resistance is 0.129 Ω against BNBC 1.3.47.7.2's 1 Ω limit, so §২৮.৬.৪ can
  say plainly that a high continuity reading is never the cable's length —
  it is a loose joint.
- **The earth-resistance numbers are computed, not quoted.**  `r_rod()` is
  BS 7430's formula (via the IET's own article, which cites it);
  `r_plate()` is IS 3043 9.2.1 with **A = the area of both sides**.  Same
  soil, same code minimums:  3 m rod 6.96 Ω · 6.5 m pipe 3.05 Ω ·
  600 × 600 plate **10.44 Ω**.  That ordering *is* IS 3043 9.1.1's point
  about shape, and it is why BD uses pipe.  In wet alluvium (IS 3043
  Table 3 gives **5 Ω·m** for alluvium at >500 mm rainfall — i.e. the whole
  Bangladeshi plain) two rods reach 0.87 Ω.
- **BNBC's own 12.19–24.38 m for tube-well-sunk GI pipe is 40–80 feet** —
  which is why pipe earthing dominates here:  the men and the rig already
  exist in every upazila.  Worth saying; it explains the clause.
- **The test-voltage conflict is real and is reconciled, not smoothed.**
  IEC 60364-6 Table 6.1: 500 V, ≥1 MΩ for everything up to 500 V.  BNBC
  1.3.47.6.1: **1000 V** for 230–400 V circuits, and 1.3.47.6.2: **≥5 MΩ**.
  §২৮.৭.৩ takes BNBC's stricter *value* (5 MΩ) and reads BNBC's *voltage*
  in its own context — 1.3.47.6.2 is written about a **cable run before its
  two ends are terminated**, where 1000 V endangers no electronics.  So:
  1000 V on the bare run, 500 V on the finished installation, 5 MΩ either
  way.  Do not "fix" this to one number.
- **Verified from the sources, do not re-verify:**  IEC 60364-6 6.4.3.1's
  ten-step sequence and its "repeat that test and any preceding one" rule ·
  6.4.3.2 (continuity of protective conductors, exposed-conductive-parts,
  ring live conductors) · 6.4.3.3 (neutral off the MET;  SPD disconnected,
  or 250 V but still ≥1 MΩ) · 6.4.3.6 (a/b/c, with the E14/E27 exception
  per IEC 60238) · 6.4.3.7.2 (Annex C Method C1 = two auxiliary electrodes)
  · 6.4.3.7.3 (continuity test **before** loop impedance).  Continuity
  instrument = **4–24 V open-circuit, ≥200 mA**.  IS 3043 37.1.5 (C at
  ≥30 m), 37.1.4 (12.5 mm MS spikes, 1 m), 37.1.3 (disconnect the electrode),
  36.3/36.4 (Wenner, ρ = 2πSR, spikes 10–15 cm deep), 38.1 (loop tester
  open-circuit ≤ 32 V), 8.2–8.4 (site selection; 15–20 % moisture; avoid
  running water), 9.2.2 (parallel separation = driven depth).
- **The 62 % rule is presented as a three-reading field check**, not a
  single position — 52/62/72 %, flat means valid.  চিত্র ২৮.২০ shows a
  valid and an invalid set side by side with real-looking numbers rather
  than a schematic potential curve, because that is what a technician
  actually does.
- **`qc.py` reports false collisions on decorative geometry.**  `soil()`'s
  grains and both charts' grid lines are emitted with `s.add()` raw SVG,
  not `s.circle()`/`s.line()`, for exactly the reason the cover's blueprint
  grid is — they run *under* the lettering by design.  Recording them
  produced a page of bogus `circle overlaps` / `line crosses`.  Keep this
  when copying the file forward.
- **A spike label belongs beside the spike, not above it** — the lead from
  the instrument comes down at the spike's own x, straight through a
  centred label (`dia_ch28.spike()`).
- **d04_pit lost its rules panel and gained the page.**  The first draft put
  a two-column list beside the section, which squeezed the drawing to half
  width and made every dimension line and callout collide.  The rules are a
  Word table now (সারণি ২৮.২) and the section has the full 15.4 cm.
- **Page-foot gaps: seven (worst 12.94 cm) → two (4.77 / 4.60 cm), 50 pages
  → 49.**  What worked, in order:  two figures moved *after* the section's
  first paragraph, the pit table moved *before* its figure (the ch17 rule),
  two worked examples' `steps=` merged onto fewer lines, one bridging
  paragraph written between examples ২৮.২ and ২৮.৩ (the ch13 back-to-back
  trap), and a formula box for the plate equation that was owed anyway.
  **Two further figure moves were tried and reverted** — they turned
  4.77/4.60 into 5.18/5.70, which is the ch17 lesson exactly: moving a
  figure relocates the stranded block, it does not close the gap.

**Real photographs added to ch26 and ch27 on 2026-09-04** (user: "chapter 26
and chapter 27 er vitor real pic add koro… jate practically bujha jay…
diagram gulo thakuk").  Not one drawing was removed — every new figure sits
beside the drawn one it belongs to.  ch26 43 → 44 pages (24 → 28 figures),
ch27 31 → 32 pages (18 → 21).  What was found and decided:

- **ch26 চিত্র ২৬.৬ (`d25_mark`) is the find of the job** — Judgefloro's
  Baliuag, Bulacan photograph (CC0) has `MOLDTO uPVC ELECTRICAL CONDUIT
  25mm THIN WALL MADE IN THE PHILIPPINES` printed legibly along a stick of
  25 mm orange conduit, i.e. **every one of IS 9537 clause 6.1's four
  markings in one frame**.  It goes under §২৬.৩.৪ with six `photo_callouts`
  labels, placed `iw=1010` on the 1400-px canvas so the printed lettering
  is still readable at 15.4 cm.  The crop is deliberately wide
  (0.02, 0.28, 0.86, 0.80 of the original) — the untouched bottom third
  was pure page height.
- **The other three ch26 additions fill sections that had no figure at all**:
  `d26_flex` (§২৬.৯.১, coiled flexible conduit + one laid in a floor chase),
  `d27_pull` (§২৬.১০.১, a fish-tape reel and the steel-wire / nylon-rod tips
  — Commons has no fish tape under that name; it is filed as
  `Fish tape.webp` and `Fish tape material comparison.jpg`), and
  `d28_ceilbox` (§২৬.১০.২, an old ceiling junction box beside a modern
  wall one, both with the joints under the lid).
- **A near-square photograph cannot carry a page.**  `ph_ceilbox` is 1.05:1;
  alone in a `sheet()` at 15.4 cm it is ~15 cm tall, and narrowing it takes
  the type under 7.5 pt.  Pairing it with a landscape crop (the bottom-right
  cell of `Junction box for wikipedia.JPG`) makes the composite 8.6 cm.
  **Pair a square photo, never place it alone.**
- **`assets_ch26.THUMBW`** was added because a crop of one quadrant of a
  thumbnail is only ~500 px.  Commons' 1800-px default is right for a whole
  frame; ask for 3600 when only a corner is kept.
- **ch27's photographs are manufacturer product shots, and that was already
  settled** — the 2026-09-03 instruction ("net theke real image dio") and the
  ch12 precedent.  Commons was re-swept for this job (categories `Cable
  channels`, `Electrical conduit` and its subcats, `Improper electrical
  wiring`, plus `Kabelkanal` / `trunking accessories` / `mini trunking`
  keyword runs) and it is still empty of mini-trunking fittings.  চিত্র ২৭.৮
  (`d19_fitreal`) is five Modi Pipes photographs — ভেতরের কোণা, বাইরের কোণা,
  টি-জোড়া, কাপলার, জাংশন বক্স — under সারণি ২৭.৫, whose wording the tile
  names now match exactly.
- **`object_crop()` in `assets_ch27.py`** finds the white object on the
  grey studio ground (L > 185, ≥ 4 px per row/column, 6 % pad).  Without it
  a product photo in a gallery tile is mostly background.
- **`photo_grid()` in `dia_ch27.py`** is the reusable piece: rows of
  `img_panel` tiles, each row centred and checked against the canvas the way
  `pair_panels` is.  Five fittings do not fit one row at a legible tile
  height; 3 + 2 at h = 250 does.
- ch27's other two: `d20_plug` (§২৭.৬.৪, a rawl plug beside its screw, and
  three sizes) and `d21_capfit` (§২৭.৬.৫, casing with the cap half slid
  off).  Both Commons, both wide, both 240–250 px panels.
- **Page-foot gaps: every one was closed with the standing playbook, no
  figure was shrunk.**  ch26 — the marking figure sits between §২৬.৩.৪'s
  paragraph and its table; `d18_gi` moved past the note box, `d12_gijoint`
  into §২৬.৪.৩ where it also illustrates the ECC point, `d05_fill` up to
  *before* the note box (that one move alone saved a page), the table
  commentary moved ahead of উদাহরণ ২৬.৪, and `d11_loop` / `d16_wrong` past
  the paragraphs that explain them.  ch27 — `d07_fill` ended up immediately
  **before** উদাহরণ ২৭.৩ after three other positions were tried and
  measured (before §২৭.৫.৩ → 10.38 cm; after ২৭.২ → 7.32; after ২৭.৩ →
  6.62; before ২৭.৩ → clean, and a page shorter), and উদাহরণ ২৭.২'s six
  `steps=` lines merged to four.  Final: ch26 4.28 / 4.11 cm, ch27 the
  pre-existing 4.55 cm.
- `qc.py` reports 0 problems on both chapters, and every new PNG was looked
  at — plus the built PDF pages that carry them.

**Chapter 27's sources and decisions (do not re-discover).**

- **The whole chapter turns on one blunt BNBC clause, and it is stated
  openly rather than smoothed over.**  **1.3.14.1.2** says PVC channels
  "should be used only for extension work in an already installed
  building", that "a design drawing should not show use of such wiring
  except inside a false ceiling", that long distances want conduit, and
  that channels are not for many or thick cables.  The BD market ignores
  all of it.  §২৭.২.৩ names both and gives the four conditions that make
  a channel job defensible anyway (no joint inside, ECC never dropped,
  45 % fill, and conduit where the run is long).  Same shape as ch26's
  35 %-vs-40 % section.
- **`HW Connection Diagram All.pptx` slide 35 is the chapter's own
  slide** — the only one in either deck that draws a channel run round a
  room, with mitred corners and a T.  s33/s34/s36 went to ch21 and ch25.
  Two crops: the whole slide (`h35_room`) and the corner strip
  (`h35_corner`, x 0.345–0.578, y 0–0.098 — tighter than it looks,
  because 0.60 onward is the "Ceiling Rose" lettering).  **The slide
  draws no earth conductor** — ⚠ box in §২৭.৭.৩ citing 1.3.13, the same
  handling as ch20/21/24/25.
- **Commons is nearly empty on mini-trunking, and this was searched
  properly** — categories `Cable channels`, `Electrical conduit`,
  `Cable trays`, `Cable-protection tubes`, `Self-made electrical
  wiring`, `Improper electrical wiring`, plus keyword sweeps in English,
  German (`Kabelkanal`), Dutch (`kabelgoot`), Polish (`listwa`), Spanish
  (`canaleta`) and French (`goulotte`), plus Openverse.  Five usable
  files only:  `Decorative rope.JPG` (a 2×2 montage — the bottom-left
  panel is casing and capping apart, the bottom-right is a cable leaving
  the end;  crop each half separately), `Ümera 12 - feeding cable in
  channel.JPG`, `Geoeffneter Kabelkanal.jpg`, `Cable channels.jpg`.
  Rejected with reasons in `assets_ch27.py`'s docstring;  the one worth
  remembering is `Kabelbox zur Durchführung von Elektroinstallationen.jpg`,
  which carries the photographer's copyright watermark burned into the
  image.
- **Two manufacturer product photographs were used** (`ph_pair`,
  `ph_mark`), on the user's 2026-09-03 instruction "net theke real image
  dio" — the ch12 precedent.  `ph_mark` is the marking-reading figure:
  `20 × 12 MM PVC TRUNKING` printed on the cap, legible at 13.6 cm.
- **The size table is computed, not copied.**  `w = W − 2t`,
  `h = H − 2t`, with t = 1.2 mm up to 32 mm and 1.5 mm above;  wire area
  is `π/4 d²` from IEC 60227-3's outside diameters (the same 3.04 /
  3.72 / 4.35 / 5.10 / 6.60 mm as ch26).  The computed inner areas
  reproduce the trade's published mini-trunking figures within a few
  per cent (25 × 16 → 307 against a quoted ~340, 38 × 16 → 455 against
  ~530), and §২৭.৩.১ says plainly that the wall thickness has to be
  measured with a vernier because makers differ.  **Do not "fix" the
  table to the trade numbers.**
- **The space factor is 45 %, not 35 %** — BS 7671 / IET give 35 % for
  conduit and 45 % for trunking, and a channel is trunking.  Ch26 prints
  the 35 %;  ch27 prints the 45 % and says why the two differ (nothing
  is pulled through a channel).
- **The IET trunking factor tables are deliberately not printed, and
  §২৭.৫.৫ says why:  the smallest trunking in that table is 37.5 × 50 mm**,
  larger than any house channel.  The cable factors are quoted in prose
  (1.5 → 8.6, 2.5 → 12.6, 4 → 16.6, 6 → 21.2, 10 → 35.3) so a reader who
  moves up to real trunking knows they exist.
- **Ch27's arithmetic is ch22/23/25/26's.**  উদাহরণ ২৭.১ = 3 × 1.5 in
  20 × 12 → 12.9 %;  ২৭.২ = two lighting + two socket circuits →
  108.8 mm² → 25 × 16 at 35.4 %;  ২৭.৩ = the geyser's 4 mm² in a
  six-circuit channel → `Iz = 32 × 0.94 × 0.57 = 17.15 A` against a 16 A
  breaker, i.e. it passes with almost no margin — that near-miss is the
  point, and it is honest:  the derating never actually fails here, so
  the real limit is the fill and the code's own words.  ২৭.৪ = a
  3.6 × 4.5 m room → 14.8 m + 10 % = 16.28 m → nine 6-ft lengths, 55
  screws.
- **A table where every row gives the same answer was cut.**  The nine
  circuits each fit 20 × 12 (the fattest, 3 × 6 mm², is 61.3 mm² against
  a 76 mm² limit), so the table said nothing;  one sentence replaced it
  and the chapter lost a page.  Worth remembering as a general check —
  read a generated table's answer column before shipping it.
- **Kalpurush's ৪-drawn-as-8 bites hardest in this chapter**, because its
  two central numbers are **45 %** and **45°**, both of which printed as
  "85".  Angles, the space factor and the degree figures are therefore
  **Latin everywhere in ch27 — prose, captions, diagram labels and MCQ
  options alike** (the ch23 rule).  **BNBC clause numbers stay Bangla**,
  matching ch22–ch26;  changing only this chapter would be worse.
- **`_corner_plan()` in `dia_ch27.py` draws the internal and external
  corner fittings in PLAN, and that is not a style choice.**  Drawn in
  elevation the two are literally the same picture, so the figure taught
  nothing;  the first draft shipped exactly that and had to be redrawn.
  In plan the wall is an L (concave) or a pier (convex), the channel
  hugs the face, and the fitting is a coloured square at the corner.
  The gallery tiles carry a one-word view label ("সমতলে" / "উপর থেকে")
  — the ch22 `_gallery` pattern, which is what makes the mixed views
  legible.
- **A wall elevation cannot carry a ceiling rose.**  d01's first draft
  hung a pendant from a rose above the main run, so the flex crossed the
  channel it was supposed to be fed from.  It is a wall bracket light
  now, fed by a drop — the geometry is honest and no line crosses.
- **Page-foot gaps: six (worst 6.6 cm) → one 4.55 cm, 32 pages → 31.**
  Four moves, all from the standing playbook:  the redundant table cut,
  চিত্র ২৭.৮ moved to *after* উদাহরণ ২৭.১, the ⚠ ECC box moved to just
  *before* the slide figure it comments on, and চিত্র ২৭.১৩ moved past
  the two paragraphs of §২৭.৬.৫.  The last gap closed by writing a
  paragraph that was owed anyway — what painting over a channel does to
  the cap.

**Chapter 26's sources and decisions (do not re-discover).**

- **The institute has nothing more on conduit, and this was checked
  exhaustively.**  `HW 1st class.pptx` **s84, s85, s86** are the only
  conduit slides in either deck (all 139 slides' text extracted and
  read), and their pictures *are* `Electrical House Wiring book.docx`
  image124 / image129–132 — **which ch14 already printed** as
  `p_cable_in_pipe`, `p_conceal_slab`, `p_conceal_wall`, `p_surface_pipe`,
  `p_surface_ceil`.  Not one was reprinted.  `HW Connection Diagram
  All.pptx` s34/s36 went to ch25 and s35 belongs to ch27.
- **So every photograph is Wikimedia Commons** (`assets_ch26.py`), and
  the download path changed:  `upload.wikimedia.org` now answers **429 to
  a direct full-resolution fetch** and tells you to use thumbnails.  The
  script therefore asks the API for `iiurlwidth=1800`, downloads the
  **thumbnail**, and asserts the **original** pixel size (kept in the
  cache json) as the tripwire.  1800 px ≈ 300 dpi at 15.4 cm, so nothing
  is lost.  Copy this pattern forward — the old ch19/ch23/ch25 fetchers
  will start failing.
- **Six candidate photos were downloaded and rejected on sight**, and the
  reasons are in `assets_ch26.py`'s docstring;  the two worth remembering
  are that `Rigid Non-Metallic Conduit 1.jpg` is large-bore ASTM D1785
  *duct*, not wiring conduit, and `Cast conduit.jpg` has an English
  caption and arrow burned into the image.  A contact sheet built with
  PIL (thumbnails of every candidate in one grid) is the fast way to do
  this — far cheaper than reading them one at a time.
- **The chapter's spine is IS 9537 (Part 3) : 1983**, free at
  `law.resource.org/pub/in/bis/S05/is.9537.3.1983.pdf` (Parts 1 and 2 are
  **not** there — those URLs return HTML).  Extracted from it and printed:
  Table 1 (OD and light/medium/heavy minimum ID for 16–63 mm), −5 to
  +60 °C working range (0.4), the three classes (5.1), the marking rule
  (6.1 — maker, size, country, **class**, at 50 mm from one end), 3 m
  preferred length (7.3), the bending spring being **0.7–1.0 mm under the
  minimum ID** (9.2.3), the 25 % flattening limit (9.3.2), the post-bend
  bore gauge (9.5.2), and the bend-test former radii 48/60/75 mm for
  16/20/25 — **which are exactly 3 × OD**.  That last one is the
  chapter's answer to BNBC's unquantified "large radius bends".
- **The conduit-sizing tables are the IET On-Site Guide's, and only the
  "long or bent run" pair is printed.**  There is a second pair for
  straight runs under 3 m with *different* cable factors (22/27/39/58/88…);
  mixing the two pairs gives wrong answers, and the reproduction on
  tlc-direct.co.uk mislabels them.  Ch26 prints the bent-run pair only
  (cable factors 16/22/30/43/58/105/145/217) and says in prose that the
  other pair exists.  Two independent checks:  professional-electrician.com
  gives 4 mm² → 43 and 25 mm at 5 m/two bends → 358, both matching.
- **tlc-direct's grid has one typo and the book's own rule catches it.**
  25 mm, one bend, 10 m is printed as 258;  it must be **358**.  The whole
  grid obeys **one bend = double the length** (two-bend L = one-bend 2L =
  straight 4L, verified at every cell), and that identity is printed in
  §২৬.৬.৩ as a field rule — it is what makes the table usable without
  memorising it, and it is the argument for pull boxes in §২৬.৭.৪.
- **The space-factor number is 35 %, not 40 or 45.**  The IET's own
  history article (electrical.theiet.org, Wiring Matters 88) says the
  arbitrary 40 % (conduit) / 45 % (trunking) "was shown to be
  inappropriate" and current GN1/OSG use **35 % conduit, 45 % trunking**.
  BNBC 1.3.39.2 meanwhile asks for 40 % *clearance* (i.e. 60 % fill) in
  telecom conduit — much looser.  §২৬.৬.৫ states both and takes the
  stricter one.  Do not "fix" this to 45 %.
- **Cable overall diameters come from IEC 60227-3**, stranded:  1.5 →
  3.04, 2.5 → 3.72 mm.  With IS 9537's 20 mm heavy ID of 15.8 mm that
  gives 17 / 33 / 50 % for three / six / nine 2.5 mm² cables — the three
  panels of চিত্র ২৬.১০ and উদাহরণ ২৬.১.  The two methods land within one
  cable of each other and the book says so;  it does not pretend they
  agree exactly.
- **`pick_size()` chooses from 20/25/32 only.**  16 mm is in IS 9537 and
  in the printed table, but selecting from it made সারণি ২৬.১১ give two
  different sizes for the same cable purely because one run was shorter —
  which contradicted §২৬.৩.২'s own statement that 16 mm is not used in
  houses.  `PICK_FROM` exists for that reason;  don't widen it.
- **Ch26's arithmetic is ch22/ch23/ch25's, not a new chain.**  The same
  nine circuits and the same 3 × 10 mm² feed;  what is new is the conduit
  column (20 mm for every final circuit, 32 mm for the feed) and the
  per-point estimating rate, which reproduces ch14's 220 m within 5 %
  (উদাহরণ ২৬.৫:  20 × 5.5 + 10 × 4.5 + 4 × 9 = 191 m, +10 % = 210 m).
- **BNBC clauses verified from the source PDF and reusable later:**
  1.3.11.1.2 (saddles ≤ 600 mm, rowel plugs, 20 SWG GI pull wire),
  1.3.11.2 (walls vertical/horizontal only, slab conduit at **mid
  thickness** on mortar blocks or steel 'chairs', continuous throughout,
  spare capacity, **conduit rising from the floor strongly discouraged**
  because of condensation), 1.3.11.3 (false ceilings — no loose cables,
  no bare cables, no taped joints), 1.3.14.1.1 (heavy wall water grade,
  large-radius bends by heat or machine, section stays circular, solvent
  cement, **1:1000 floor slope**, 20 SWG pull wire, 18 SWG pull boxes with
  ebonite/perspex covers), 1.3.14.1.3 (flexible PVC — surface only, only
  where bends cannot be used), 1.3.14.1.4 (GI ≥ **16 SWG**, seamless, no
  internal projections, threaded sockets, edges dressed), 1.3.14.1.5
  (pull boxes mandatory on every drop from the ceiling), 1.3.15
  (expansion joints — oversize flexible PVC, pull boxes both sides),
  1.3.20.1 (spare room inside concealed conduit).
- **16 SWG is 1.626 mm, which sits at the top of BS 4568 Class 4's wall
  band.**  §২৬.৪.১'s note says to measure the wall with a vernier rather
  than trust the "Class 4" stamp.  The BS 4568 wall figures on the open
  web disagree with each other (1.35–1.6 vs 1.45–1.75), so the book does
  **not** print a BS 4568 dimension table — only BNBC's minimum.
- **BS 7671 543.2.2 / 543.3.6 / 543.2.3** — steel conduit may be a cpc if
  every joint is mechanically and electrically continuous;  **flexible
  metal conduit may never be**.  §২৬.৪.৩ gives that, then says the
  question is moot here because BNBC 1.3.13 requires a separate
  green+yellow ECC anyway.
- **`dia_ch26.py`'s reusable pieces.**  `pipe(d, od, cap=)` strokes one
  path three times (edge, body, offset highlight inside a `<g translate>`)
  — the ch11 `tube()` rule, no SVG gradients, because Word renders the
  **SVG**;  `cap="butt"` for a cut end, otherwise a short pipe draws as a
  lozenge.  `dim_h()` breaks its own line to make room for the label and
  falls back to placing the text *above* the line when the label is wider
  than the span — without that, `qc.py` reports `line crosses` on every
  dimension.  `brick_wall()`, `concrete()`, `rebar()`, `thread()`,
  `saddle()`, `rnd_box()`, `sq_box()`, `pipe_end()`, `core()` are the
  material vocabulary.
- **Labels belong in the drawing's own white space, not outside it.**
  d01's first draft put callouts in the margins and three ran off the
  canvas;  a room section has a large empty interior, and that is where
  the labels go.  d02's first draft put them *inside the brick wall*,
  where the course lines cross the lettering — the wall was narrowed to
  make a dedicated label column instead.
- **A pipe drawn on top of a wall reads as surface conduit even when the
  caption says concealed.**  d01 only started reading correctly once a
  chase band (`#E3D8C2`) was drawn behind each drop, sized to the pipe's
  actual extent rather than the full wall height.
- **`pair_panels()`'s overflow guard earns its keep.**  Three photo
  sheets raised it on the first run (ph_gi is a 2.6:1 strip and cannot
  share equal panel height with a 1.57:1 photo).  The fix is not a
  smaller `h` — it is giving a wide-and-short photo its own
  `strip_callouts` sheet.

**Chapter 25's sources and decisions (do not re-discover).**

- **Slides 33, 34 and 36 of `HW Connection Diagram All.pptx`** are the flat's
  SDB and its room layouts.  Ch21 printed the *whole* of s33 once (চিত্র
  ২১.১১); ch25 re-crops **only the grey enclosure** (x0 = 0.272, y1 = 0.605)
  at 300 dpi so the breaker lettering can be read — a different crop teaching
  a different thing.  **s35 was deliberately left for ch27** (it is the
  channel-run variant of s34).
- **None of the three slides draws an earth conductor** — red and black only.
  §২৫.১০.৩ says so in a ⚠ box and cites BNBC 1.3.13.  Same handling as ch20's
  "Magnetic Conductor", ch21's wrong formula and ch24's s30.
- **The slide's own arrangement is corrected in the book, and the correction is
  stated openly (§২৫.৭.৩).**  s33 puts the SPD on the *load* side of the RCCB
  and hangs every way off one 30 mA RCCB.  Both are real design faults and
  both are shown with numbers: a surge discharged through an RCD is seen as
  residual current (IEC 60364-5-534 then demands an S-type RCD with ≥ 3 kA
  8/20 immunity), and the accumulated standing leakage of nine circuits
  (13.2 mA) exceeds the 9 mA design budget.  The book therefore puts the SPD
  first and moves geyser + two ACs outside the RCCB.
- **Ch25's arithmetic is ch22/ch23/ch24's, not a new chain.**  The same nine
  circuits, 11,966 W → diversity 0.6 → 7200 W → 230 V, cos φ 0.95 → 32.95 A →
  40 A DP → 10 mm², 1.39 % over 22 m.  What is new is the *board* count:
  modules 2+2+2+6+2+2 = 16, plus 2 spare (1.3.9.3.9) = **18 modules**, while
  the **device** count is 14 → BNBC Table 8.1.23's "up to 24" row → 480 × 390
  × 120 mm.  §২৫.২.৫ says plainly that ways, modules and devices are three
  different numbers — that confusion is the chapter's most practical point
  after the neutral bar.
- **BNBC Table 8.1.23 (clause 1.3.17.2) is the enclosure-size table** and was
  extracted from the source PDF, not remembered.  So were 1.3.34(a) (board not
  more than 2 m above floor) and **1.3.34(d)** — the clause that makes a
  circuit list mandatory, which is the legal footing for §২৫.৯.৭.
- **Verified from the standards, do not re-verify:**  one module = 17.5 mm
  (DIN 43880), rail TH35 (IEC 60715); IEC 61439-3 = boards for ordinary
  persons, outgoing ≤ 125 A and assembly ≤ 250 A; IEC 60364-4-41 411.3.3 =
  30 mA on ≤ 32 A general-use sockets; IEC 60364-5-534 = SPD lead total
  ≤ 0.5 m (never > 1.0 m) and the 3 kA/S-type rule above; IEC 61008-1 general
  type = 300 ms at IΔn, 150 ms at 2 IΔn, 40 ms at 5 IΔn; IEC 60335-1 class-I
  leakage limits = 3.5 mA stationary motor-operated, 0.75 mA per kW (max
  5 mA) stationary heating, 0.75 mA portable.  **BNBC 2012 still contains no
  RCCB requirement at all** (ch22's finding, restated in §২৫.৬.১).
- **The 30 % standing-leakage rule** (9 mA under a 30 mA RCD) is the
  BEAMA/manufacturer design guideline, not a BNBC clause — §২৫.৬.৩ presents
  it as a design rule and uses *measured* clamp-meter values in উদাহরণ ২৫.৩,
  not invented ones.
- **Photographs: nine on Commons, seven printed.**  `assets_ch25.py` pulls
  them; none of ch24's MDB pictures is reused, because ch24's set is a *main*
  panel.  Seven of the nine are **Dmitry G's** consumer-unit series (CC BY-SA
  3.0) — empty enclosure, the flat's whole kit, comb bar before fitting, comb
  bar fitted, work in progress, the finished flat board — and they are used in
  that order, so they read as one job.  The other two are **Retired
  electrician's** `Small house distribution panel 1` and `2` (CC0): the **same
  board outside and inside**, which is what proves the circuit-chart
  requirement with a real object.  `ph_rows` is downloaded but unused (see
  below).  Two candidates were dropped from `PHOTOS` and the reasons are in
  the script's docstring: `DIN rail.JPG` is a 3:1 strip that overflows
  `pair_panels()` at equal panel height (and the rail is already labelled in
  চিত্র ২৫.৩), and `Fuse box with overlimited circuit breakers.JPG` kept
  returning 429 from Commons — সারণি ২৫.১৩ carries the mistakes instead.
  `credits.json` is written as usual;  **no ❖ চিত্রসূত্র box is printed**
  (2026-08-30 instruction).
- **`d18_rows` is drawn and QC-clean but deliberately not in `ALL`.**  Its
  lesson (a name on every way) is already carried by the drawn চিত্র ২৫.১৬
  and by the printed chart in চিত্র ২৫.১৭, and the extra portrait photo
  opened a 7 cm page-foot gap in §২৫.৯.৭.  The function keeps a docstring
  saying so; putting it back in `ALL` is a one-line change.
- **Page-foot gaps: 9 gaps (worst 11.8 cm) → one 4.37 cm, and 46 pages → 44.**
  Four moves, all from the standing playbook, plus one new one worth keeping:
  a tip box moved *before* its figure, a paragraph written between two
  adjacent photographs, figures moved *after* the paragraph that explains
  them, and — the new one — **photo sheets placed narrower**.  `sheet()` and
  `pair_panels()` set their smallest type at 23 px on a 1240-px canvas, so
  14.4 cm still prints 7.5 pt;  `photo_callouts()` uses 24.5 px, so it goes to
  13.6 cm.  That is the ch18 rule applied systematically, and it bought about
  8–12 % of height on eleven figures.  The "never shrink a figure" rule still
  binds every *drawn* diagram, whose labels already sit near the floor.
- **`module()` in `dia_ch25.py` grew a `dy` argument** because the device's
  name/rating block was colliding with the DIN rail drawn under it, and a
  `face=` argument ("toggle" / "window" / "blank") so an SPD reads as a
  status window and a spare way as a blank cover.  `bar_run()`'s label needs
  at least ~24 px of clear space to the left of the bar, and if the bar sits
  inside a panel rect that space has to come out of the panel's margin —
  otherwise `qc.py` reports `box edge cuts` on every bar name.

**Chapter 24's sources and decisions (do not re-discover).**

- **Only slide 30 of `HW Connection Diagram All.pptx` was left unused by
  ch21**, and it is exactly the distribution chain: pole → main meter → main
  MCB → sub-meter → MCB → SDB box, plus switchboard and DP-switch-to-motor
  branches.  That is চিত্র ২৪.৩.  **The slide draws no earth conductor** —
  only red and black.  §২৪.১.৩ says so in a ⚠ box and cites BNBC 1.3.13.
  Same handling as ch20's "Magnetic Conductor" and ch21's wrong formula.
- **Ch21 had already used s29/s31/s32/s33**, so ch24 does not reprint them;
  its own richer SLD (`d04_sld`) is drawn instead.
- **The photographs are one job, photographed in sequence.**  Robertbh1984's
  six Commons pictures (CC BY-SA 4.0) are a villa's main panel being built —
  empty box with wires hanging, bars on insulators, lugs on the earth bar,
  the finished dead-front board.  §২৪.৬ is written in that same order, so the
  pictures read as one continuous job.  `ph_bad` (Oto Zapletal, CC BY 4.0) is
  the counter-example BNBC 1.3.17.4(b) forbids.
- **Ch24's arithmetic is ch21's + ch22's + ch23's, not a new chain.**
  16 flats × 12 kW + lift 22 + pump 11 + common 12 + fire/gen 13 = 250 kW ·
  diversity 0.7 → 175 kW · 3Φ 400 V, cos φ 0.85 → 297 A → 400 A 4-pole MCCB →
  50 × 5 Cu busbar (400 / 1.6 = 250 mm²).  Fault level is ch22's 250 kVA /
  Z 4.5 % → 361 A → 8 kA.  Every flat feeder is ch22/ch23's 7200 W / 32.95 A /
  40 A DP.  **The 0.7 is checked a second way** — summing the three phases
  gives 162.8 kW, i.e. an effective 0.65, so 0.7 is realistic and slightly
  generous.  Say that; it is what makes the assumed number defensible.
- **The riser table is the chapter's own contribution, and it is a voltage-drop
  argument, not an ampacity one.**  BNBC 1.3.12.2 measures the 2.5 % "from the
  main distribution point"; the safe reading is the whole path, so the budget
  splits 1.31 % feeder + 1.19 % final circuit (ch23's worst circuit).  That
  forces 10 mm² on floors 1–4, 16 on 5–6, 25 on 7–8 — same current throughout,
  fatter only because of length.  Ch23's example ২৩.৬ predicted exactly this
  ("মিটার নিচতলায় আর ফ্ল্যাট ছয়তলায় হলে … ১৬ বর্গমিলিমিটারে তুলতে হয়").
  Grouping is dodged legitimately: BNBC 1.3.18.2's own 37 mm spacing exceeds
  2 × cable diameter, so Cg = 1.
- **Three-phase feeder cable sizes are deliberately blank.**  The book prints
  IEC 60364-5-52 Table B.52.2 (two loaded conductors) as সারণি ২৩.১৫; a
  three-phase feeder needs Table B.52.4, which is not printed here and could
  not be verified from a free source (ANSI/IEC previews are paywalled or
  JS-gated; ecalpro.com's B.52.2 reproduction *did* verify ch23's numbers and
  extends them to 240 mm²).  সারণি ২৪.৬ marks those two rows `(ক)` and the
  paragraph under it says why.  **Do not fill them from memory.**
- **BNBC's Table 8.1.15 board symbols were redrawn from the source PDF at
  420 dpi, not guessed** — MDB is a cross with the left and right triangles
  filled, FDB adds a vertical centre line, DB is a bare cross, SDB one
  diagonal, BDB one diagonal with the lower triangle filled, SB a brick-hatched
  bar.  An earlier invented scheme gave FDB and DB the same picture.
- **The code contradicts itself on sheet thickness and the book says so** —
  1.3.9.2 wants ≥ 18 SWG (1.22 mm) for a distribution board's box, 1.3.17.1
  wants ≥ 20 SWG (0.91 mm) for sub-distribution boards inside a building.
  §২৪.২.৫ names both and takes the stricter one for an MDB.
- **BNBC sub-item letters were mapped from the source, not assumed.**  In
  1.3.47.8.4 the run is a=ক … j=ঞ (polarity), k=ট (spare knockouts),
  n=ঢ (all strands in the terminal), p=ত (flat + spring washers).  The first
  draft was three letters out.  Extract the clause and count before citing.
- **Two engine-level traps caught in the build.**  `_n(x, 0)` — the
  strip-trailing-zeros helper copied forward from ch23 — turned 26400 into 264
  and 250 into 25, because ch23 only ever called it with d ≥ 1; it now
  short-circuits at d == 0.  And **Kalpurush has `*` in its cmap but draws it
  blank** (the `÷` trap again), so a footnote asterisk vanished from two table
  cells and from the paragraph explaining them; the marker is `(ক)` now.
- **Counting columns went Latin.**  Kalpurush's ৪-looks-like-8 is not harmless
  in a table the reader adds up: the riser table's floors ৪ and ৮ both read
  "8", and in the balance table ০ + ২ + ২ appeared to total "8".  Sizes,
  counts and floor numbers in ch24's engineering tables are Latin; prose stays
  Bangla.

**Chapter 23's sources and decisions (do not re-discover).**

- **Neither diagram deck has a cable slide** — every slide's text in both was
  extracted and checked, and `Electrical House Wiring book.docx` has no cable
  photograph either.  All eleven photographs come from Wikimedia Commons via
  `assets_ch23.py`, credited from `credits.json`.
- **The institute's own cable source is `SUPER STAR Cables Technical Catalog
  (FORCE).pdf`** (note: CLAUDE.md used to call it `SUPER STAR Cables
  catalog.pdf`; the real filename is the longer one).  Seven pages, all
  **scanned images** — `get_text()` returns nothing, so pages are rendered at
  330 dpi and cropped by fraction.  Page 2 = BYA/BAYA, 3 = BYFY/BAYFY,
  4 = flexible.  Only the three *type-designation blocks* are cropped as
  images; the catalogue's data tables are rebuilt as real Word tables.
- **`circuit breaker & cable calculation.docx` has no cable half at all** —
  despite the name it is only the load list and breaker arithmetic, already
  mined for ch22.  Don't go looking for more in it.
- **The catalogue's ampacity column and IEC 60364-5-52 agree once ambient is
  corrected**, and §২৩.৫.২ says so openly with the numbers: catalogue is
  quoted at **35 °C**, IEC's Table B.52.2 at **30 °C**; B1 × 0.94 gives
  16.5 / 22.6 / 30.1 / 38.5 / 53.6 / 71.4 against the catalogue's
  16 / 22 / 30 / 38 / 52 / 70.  That convergence is the chapter's argument
  for reading the *conditions* at the head of a table.
- **mV/A/m is computed, never memorised.**  `vdrop_rows()` derives it from
  IEC 60228 Table 2 (class 2, plain copper, max resistance at 20 °C):
  `R70 = R20 × [1 + 0.00393 × 50] = R20 × 1.1965`, then ×2 for single phase
  and ×1.732 for three.  The result reproduces BS 7671's printed table
  exactly (1.5 → 29, 2.5 → 18, 4 → 11, 6 → 7.3, 10 → 4.4) — that match *is*
  the verification.
- **Ch23's arithmetic is ch22's, from the same `CIRCUITS` list.**  সারণি
  ২৩.১৯ recomputes IB, Iz and the drop for the nine circuits of সারণি ২২.১৫,
  so the two tables cannot disagree.  Main: 11,966 W → 0.6 → 7200 W →
  230 V, cos φ 0.95 → 33 A → 40 A → 10 mm², drop 1.39 % over 22 m.
- **The star example is ২৩.৪** — the roof pump 60 m away.  Ampacity says
  1.5 mm² is fine; the drop check rules out 1.5 (4.12 %) *and* 2.5 (2.56 %,
  only just over) and forces 4 mm².  That "only just over" is deliberate:
  a limit is a limit.
- **Engineering tables use Latin digits, prose uses Bangla.**  This is
  ch22's সারণি ২২.১৫ convention (load 700, cos φ 0.9, cable 1.5) and the two
  tables are meant to be read side by side.  It also dodges a real hazard:
  Kalpurush draws Bangla ৪ like a Latin 8, which in a *cable-size* column is
  not a curiosity but a wrong number.  Voltage grades (`450/750 V`) are Latin
  for the same reason the chapter exists — that is how they are printed on
  the sheath.
- **The old imperial sizes are the market's, and they are computed too.**
  `imperial_rows()` derives the area from `n × π/4 × d²` with d in inches ×
  25.4, which is why the BD market sells 1.3 / 2.0 / 3.0 / 4.5 / 7.0 / 9.5 /
  14.5 mm² alongside the metric list: they are 3/0.029″, 3/0.036″, 7/0.029″,
  7/0.036″, 7/0.044″, 7/0.052″, 7/0.064″.  BNBC 1.3.9.3.12 writes both
  (`4 mm2 (7/0.036)`), and 7/0.036″ really is 4.60 mm², so the clause is met.
- **২৩.৪.৭ (SWG ও AWG) was added on the user's request.**  Research done, do
  not redo:  SWG is BS 3737:1964, **withdrawn** (BS 6722:1986 went metric),
  yet BNBC still uses it for sheet and pull wire (1.3.14.1.8 "18 SWG GI
  sheet", 1.3.19.2 and 1.3.30 "18 SWG GI pull wires") while using mm² for
  conductors — that split is worth stating.  AWG is ASTM B258 and its
  definition *is* the formula `d = 0.127 × 92^((36−n)/39)` mm; the computed
  areas match the AWG table printed in **IEC 60228:2004's own foreword**
  (20 → 0.519, 14 → 2.08, 10 → 5.26, 2 → 33.6 …), which is the verification.
  The +3 / +6 / +10 rules check out exactly (area ratios 2.005, 4.020,
  10.164).  The payoff that ties the section to ২৩.৪.৬:  0.036″ **is** SWG 20
  and 0.064″ **is** SWG 16, so `7/0.036` = seven strands of SWG 20 = 4.60 mm²,
  the same figure সারণি ২৩.১১ computes.  But 0.029″, 0.044″ and 0.052″ are
  **not** SWG numbers — they are plain inch diameters, so "7/0.044" must not
  be read as a gauge.  Say that plainly; it is the section's sharpest point.
- **`re` / `rm` / `se` / `sm`** = round-solid / round-stranded /
  sector-solid / sector-stranded (DIN VDE).  Both the Super Star and BBS
  price lists use them, so does `ph_sector`'s photograph.
- **No prices and no market-share percentages.**  The only verifiable share
  figures (BRB 41 %, Eastern 15 %, BBS 13 %…) are from a Daily Star piece of
  **2018** — eight years stale, so §২৩.৯ names the makers and says what to
  check instead.  Same reasoning as ch17/ch19/ch21/ch22.
- **Callout targets must be picked from the image's pixels, never by eye.**
  The user rejected the first build with "diagram gulor marking thik jaygay
  hoy nai", and they were right — a pixel check showed most leader dots
  landed on the wrong material: "ইনসুলেশন" and "সবুজ-হলুদ কোর" on bare
  copper, "বাদামি — L1" and "কালো — L2" on the background, "ফেরুল" on empty
  grey, "ফিলার" on black bedding.  The fix, and the method to reuse: build a
  colour mask for the thing being named, take the **deepest** point of that
  region (repeated erosion → the pixel furthest from any edge) inside a
  search window, then verify by averaging a 9×9 patch at the chosen point.
  A scratch helper doing exactly this is worth rewriting per chapter; it is
  ~40 lines with numpy (installed into the venv for ch23).
  Two traps it does not solve on its own:  (a) when the named thing and its
  neighbour share a colour — white filler vs aluminium conductor, grey wire
  vs grey background — constrain the *window* to where the neighbour cannot
  reach, because colour alone cannot separate them;  (b) for a wire against
  a flat background, scan a column and print every run that differs from the
  background, then read the wire's centre off that list.
- **A `strip_callouts` leader must not cross the printed lettering.**  d05's
  two "below" labels had their dots *above* the text (fy 0.66–0.68) while the
  leader came up from underneath, so both lines ran straight through the
  print — the very thing the figure exists to show.  Measure the lettering's
  row first (brightness profile per row: the print showed as a 30–42 % bright
  band at fy 0.70–0.83), then put "above" dots above it and "below" dots
  below it.  Field centres come from a per-column brightness profile too.
- **Kalpurush's ৪-looks-like-8 is not always harmless.**  In ordinary prose it
  is the familiar rendering the whole book ships.  But where the digit *is*
  the identity of the thing — a cable size, a gauge number, an inch code —
  it changes the fact:  `৭/০.০৪৪` printed as `7/0.048`, which is a different
  wire (and happens to be a real SWG size, so the sentence became wrong).
  Rule now applied in ch23: **sizes, gauge numbers and inch codes are Latin
  everywhere, in prose as well as tables**; ordinary counts and quantities
  stay Bangla.
- **Two reusable engine fixes came out of this chapter.**  `pair_panels()` in
  `dia_ch23.py` now **raises** when the panels overflow the canvas — d08 and
  d16 both shipped cut off at the page edge with `qc.py` reporting clean,
  because QC checks text, not boxes (the ch19 lesson, now enforced).  And a
  leader whose target is computed from a *radius* must have that radius
  checked against the ring it is meant to touch — d02's "আউটার শিথ" landed on
  the armour because r=195 was inside the filler, not the sheath at r=238.

**Chapter 22's sources and decisions (do not re-discover).**

- The institute's three root files (`circuit breaker.docx`, `circuit breaker
  & cable calculation.docx`, `Standard Markings on Circuit Breakers.docx`)
  were mined for facts only.  **Neither diagram deck has a breaker-specific
  slide** — every slide's text in both was extracted and checked; the
  closest are `HW Connection Diagram All.pptx` s29/s31/s32/s33, already
  used by ch21.  So every photograph comes from Wikimedia Commons via
  `assets_ch22.py`, credited in the ❖ চিত্রসূত্র box from `credits.json`.
- **The chapter's whole point is reading a nameplate.**  A whole-device
  photo placed at 15.4 cm renders its printed lettering at 3–4 pt — useless.
  The fix, and the pattern to copy: a separate tight *face* crop of each
  device (`ph_mcb_face`, `ph_mccb_face`, `ph_mccb_trip`, `ph_rccb_face`,
  `ph_spd_face`) placed with `photo_callouts()`, so the lettering lands at
  9–20 pt, each backed by its own per-marking Word table.  Two crops of one
  Commons file is normal (`ph_spd_face` and the whole-device shot came from
  the same picture) — but do not ship both unless they teach different
  things.  One such second crop was cut for exactly that reason.
- **BNBC 2012 contains no RCCB requirement at all.**  Checked clause by
  clause against the law.resource.org PDF.  §২২.৭.৫ says so openly and
  cites IEC 60364-4-41 (30 mA for socket circuits) as the governing rule
  instead.  Do not "fix" this by inventing a BNBC clause number.
- **Scope was held to house wiring on the user's explicit instruction**
  ("i want only for house wiring").  ACB, VCB, SF₆, OCB, air-blast, MPCB,
  AFDD and DC breakers get one short §২২.১০.৩ paragraph naming them and
  saying where they belong — nothing more.  The user had rejected an
  earlier `Standard Markings on Circuit Breakers.docx` for exactly this
  bloat.
- **Ch22's arithmetic ties to ch18, ch20 and ch21.**  Nine circuits totalling
  11,966 W ≈ 12 kW · diversity 0.6 → 7200 W · 230 V, cos φ 0.95 → 33 A →
  40 A DP MCB + 40 A/30 mA RCCB + 10 mm².  That 7200 W / 33 A is
  deliberately ch21's flat DB, and the 1 HP pump's 1066 W / 5.45 A is
  ch18's and ch20's motor.  `CIRCUITS` + `circuit_rows()` in `ch22.py`
  compute IB and 1.25 × IB, so সারণি ২২.১৫ can never disagree with the
  prose.  Fault level: 250 kVA, Z 4.5 % → IFL 361 A → Isc 8022 A.
- **§২২.১৩ "বাজারে কোন ব্র্যান্ড" was added on the user's request
  (2026-08-23)** — real brand photos plus a little brand information.
  Research already done, do not redo:
  - **The Bangladesh market, verified from BD dealer sites** (impress.com.bd,
    circuitbreakermart.com, brotherstrading.com.bd, infinitybd.com,
    bdtronics.com, and a Rahimafrooz Hager page): European premium — ABB,
    Schneider (Acti9), Siemens, Legrand, Hager; Japanese — Mitsubishi, Fuji,
    Terasaki (mostly MCCB); Korean — LS Electric; Indian — Havells; Chinese —
    CHiNT (NB1-63, NXB-63, NXBLE RCBO), CNC Electric, Delixi, TOMZN;
    Bangladeshi — Super Star (SP/DP MCB 6–63 A, 3/6 kA).
  - **No taka figures**, on the ch17/ch19 precedent — the table gives a
    relative tier (বেশি/মাঝারি/কম) and §২২.১৩.১ says openly why.
  - **The institute's own breaker images were rejected *for this job*.**
    `circuit breaker.docx` (20 images) and `Standard Markings on Circuit
    Breakers.docx` (11) are all CHiNT/Hager/TOMZN **catalogue renders** —
    300–780 px, so the printed lettering cannot be read, which is the whole
    point of §২২.৫.২/৬.১/৭.২/৯.৩. (They were later accepted for a *different*
    job — see the ছবি-সারি block below.) Everything came from Commons instead:
    `ph_br_schneider` (Acti9 iC60N B16), `ph_br_abb` (S203 B16),
    `ph_br_legrand` (C16), `ph_br_chint` (NB1-63 C2) — all CC BY-SA, all
    with legible markings, so `d22_brands` proves the chapter's own thesis
    (same IEC 60898-1 layout on four different makes) with real objects.
  - **The ❖ চিত্রসূত্র box used to iterate a hand-written `used = [...]`
    list.** It went stale the moment photos were added or dropped and
    silently omitted four credits — which for CC BY-SA is a licence breach.
    It now iterates `credits.json` itself. Never reintroduce a manual list.
- **Two device-identification photo rows were added on the user's request
  (2026-08-23), from the institute's own file.**  `assets_ch22_dev.py`
  pulls all eleven renders out of `Standard Markings on Circuit
  Breakers.docx` — the order inside `word/media/` is exactly the document's
  order and was verified blip-by-blip: 1 MCB · 2 MCCB · 3 RCCB · 4 RCBO ·
  5 "ELCB" · 6 MPCB · 7 AFDD · 8 Isolator · 9 SPD · 10 ACB · 11 VCB.
  Decisions, do not re-litigate:
  - **Two jobs, two kinds of picture.**  Commons photos teach *nameplate
    reading* (close crops, callouts).  These renders teach *what the device
    looks like* — white ground, one light, one angle, so six objects side by
    side show only the shape difference.  For that job a catalogue render is
    better than a photograph, and the low resolution costs nothing.
  - **`dia_ch22._gallery()`** is the reusable shape: one row of tiles, photo
    in a white well on a PLATE card, name + a one-or-two-word role under it,
    one note strip.  It raises if a label does not fit its tile.  `d23_devices`
    (six house devices, চিত্র ২২.৬, in §২২.৪ in সারণি ২২.৪'s order) and
    `d24_outside` (MPCB/AFDD/ACB/VCB, চিত্র ২২.১৯, in §২২.১০.৩) use it.
    d24 is placed 11.4 cm wide, so its type is set larger (30/24 px) — the
    `N × P(pt) / W` rule, not a different style.  Its caption reads
    "কোনটা কোথায় বসে — মোটরের স্টার্টারে, ঘরের সার্কিটে, এলটি প্যানেলে
    ও ১১ কেভি সাবস্টেশনে" — one placement per tile, in tile order.  The
    user first asked for "সাবস্টেশন এবং বিভিন্ন ইন্ডাস্ট্রিতে ব্যবহৃত…";
    that was flagged because **AFDD is a residential device** (২২.১০.৩
    puts it in bedrooms and hotels), and the user then left the wording
    to me.  The lesson is general: a caption over a mixed row must
    account for every tile, and it must not restate the artwork's own
    header (`যেগুলো বাসার ডিবিতে বসে না` already says the negative).
  - **The renders are RGBA with a transparent ground — but three of them
    (MCB, MCCB, MPCB) are not.**  Their alpha is 255 everywhere and the
    ground is solid white, so an alpha-bbox autocrop returns the whole
    canvas.  `tight_box()` falls back to a white-difference bbox when the
    alpha box covers >98 % of the image.
  - **The "ELCB" render is not an ELCB** — it is a CHiNT NXBLE-40, marked
    IEC 61009-1, i.e. an RCBO.  The source file's label is wrong.  It is
    left out of both rows rather than teaching a falsehood; §২২.১০.২ already
    says in prose that RCCB/RCBO are still sold as "ELCB".
  - **The ❖ চিত্রসূত্র box now opens by naming both sources.**  The credit
    *list* still iterates `credits.json` (Commons only) — the institute file
    is one sentence, not a per-image list, so there is nothing to drift.
  - **The MCQ answer key really was skewed** — 8 of 15 on গ, while the
    comment beside it claimed ক৪ খ৪ গ৪ ঘ৩. The CLAUDE.md standing check
    says to *read the key as a string*; counting it is the part that was
    skipped. Now 16 questions at ক৪ খ৪ গ৪ ঘ৪.

- **Seven figures were redrawn after the user's review (2026-08-23).**  The
  complaint was overlap / illegibility in চিত্র ২২.২, ২২.৫, ২২.৮, ২২.১১ and
  wrong leader targets in ২২.৭, ২২.১০, ২২.১৭.  What came out of it, reusable
  for every later chapter:
  - **A device drawn as a bare rectangle on a wire teaches nothing.**  ২২.২'s
    fuse got metal end caps and a zig-zag element (melted, with a scorched
    glass ellipse, in the fault row); the breaker got a toggle **on top of the
    case** carrying `I`/`O` — a floating chip beside the contact arm is what
    the tripped arm collided with in the first draft.
  - **Show what the mechanism *does*, not just what it is.**  ২২.৫ now ends
    both panels on the same **ট্রিপ বার**, and the bimetal is two strips in
    two colours with a legend, not one rod.
  - **Draw order carries meaning.**  In ২২.৮ the three magnetic bands are
    drawn *before* the thermal band, so each hangs off the curve at its own
    multiple (B at 3, C at 5, D at 10) — a staircase instead of three
    disconnected boxes.  Region labels moved to the two empty corners with
    arrows.
  - **`strip_callouts()` in `dia_ch22.py`** is for wide-and-short photos
    (≈3.6:1).  `photo_callouts` puts labels down both margins, which forces
    diagonal leaders when there is no height; `strip_callouts` puts them
    above and below with leaders that drop vertically and then elbow.
  - **`callout(..., elbow=True)`** and the optional 4th item field in
    `photo_callouts` (`(text, tfx, tfy, label_fy)`) route a leader
    horizontally at the label's height and then vertically to the target.
    That is the only clean way to reach a symbol that a straight line would
    have to cross a printed schematic to touch (২২.১৪'s Type-AC box).
  - **Measure targets, don't guess them.**  Overlay a 5%-grid on the cropped
    photo and read the fractions off it; every wrong leader in this batch
    came from an estimated fraction.  The two failure modes were a dot **on**
    the printed lettering (left columns of ২২.৭/২২.১০/২২.১৭) and a leader
    stopping at the photo's dark right edge instead of reaching the feature.
  - **Four rating rows 0.04 of image height apart cannot each take a
    callout** — `photo_callouts`' minimum separation is `size × 1.95` px, so
    the leaders fan out and mislabel.  ২২.১৭ moved all four ratings to the
    **right** module where they could be spread, and the per-marking table
    below the figure carries the meanings.  The picture says *where to look*;
    the table says *what it means*.

- **`\%` is not a math-DSL command** — `\frac{I_{FL}}{Z\%}` shipped once and
  printed `Z" % }} × 100 ⌐`.  Write `Z` and say in the following sentence
  that Z is the percentage number (4.5, not 0.045).

**Chapter 21's sources (do not re-discover).**  Two decks, both mined:

- `Busbar All.pptx` — 7 slides.  s1 copper + aluminium 3D renders,
  s2 twisted-wire joints + a real panel busbar photo, s3 selection
  criteria, s4 current density, s5 the W/T/L sketch, s6 a table of **28
  market sizes**, s7 the calculation flowchart.  The four embedded images
  are pulled straight out of the PPTX (full resolution) rather than
  cropped from a slide render — `assets_ch21.PPTX_PICS`, guarded by sha1
  *and* pixel size.  **Trap: the shape names are inverted** — s2's
  "Picture 6" is the panel photo and "Picture 8" is the wires.
- `HW Connection Diagram All.pptx` slides **29, 31, 32, 33** (s29 meter →
  MCCB → five busbars; s31 main meter → busbar → three sub-meters; s32
  3Φ and 1Φ off one bar-set; s33 a full flat SDB with RCCB, SPD and
  separate neutral/earthing bars).  Every slide's text in both decks was
  extracted and checked — these four are the only busbar slides.

Three decisions made while building it, do not re-litigate:

- **Slide 7's two formulas are wrong** — it prints `KVA = 1000*V*I` and
  `KW = 1000*V*I*Cosθ`; it must be *divide* by 1000.  The slide is
  therefore **not** embedded; `dia_ch21.d12_calc` is its corrected
  redrawn form, and §২১.৬.৩ states the correction in the prose.  Same
  handling as ch20's "Magnetic Conductor".
- **Slide 6's 28 sizes became সারণি ২১.৩, a real Word table**, not an
  image — with each size's area and its copper/aluminium ampacity
  computed in `ch21.SIZES` / `size_rows()`.
- **Current density**: the institute's deck says Cu 1.5–2.0 and Al
  0.5–1.5.  Verified engineering practice for LV switchgear is Cu
  1.0–1.6 (1.2 in a sealed panel, 1.6 ventilated) and Al 0.7–1.2;
  manufacturer tables for *bare bar in free air* run higher still
  (40×5 Cu = 520 A ≈ 2.6; 50×10 Cu = 920 A ≈ 1.84, at 35 °C ambient /
  30 K rise).  The book uses **Cu 1.6, Al 1.0** — inside both ranges —
  and §২১.৬.১ says openly why the numbers differ.

**Ch21's arithmetic is one chain — change one number and all of it moves.**
250 kW connected · diversity 0.7 → 175 kW · 3Φ 400 V, cos φ 0.85 →
I = 175000/588.9 = 297 A · Cu J 1.6 → 186 mm² → bar 40 × 5 (200 mm²,
320 A) · +20% spare → 356 A → 223 mm² → 50 × 5 · Al J 1.0 → 297 mm² →
60 × 5 · flat DB: 12 kW · 0.6 → 7200 W → 230 V, cos φ 0.95 → 33 A →
20.6 mm².  Worked examples ২১.১–২১.৪ and সারণি ২১.৩ all hang off it.
The denominator 1.732 × 400 × 0.85 = 588.9 is deliberately the same one
as ch16's example ১৬.৩.

BNBC clauses verified from the source PDF for ch21 and reusable later:
**1.3.9.3.8** (≥20% spare in a branch circuit), **1.3.9.3.9** (one spare
way per five used), **1.3.9.3.15 + Table 8.1.2** (L1 red, L2 yellow,
L3 blue, N black, ECC green+yellow), **1.3.9.3.16** (three-phase load
balancing, verified with a clamp meter), **1.3.14.1.6** (a small
copper/brass earth bar even inside a switchboard's metal box),
**1.3.17.2** (enclosure size depends on busbar size and insulator type),
**1.3.17.4(c)** (soldered/welded lugs), **1.3.18.2** (>9 storeys →
sandwiched copper trunking; protection at *both* the source busbar
junction and the tap-off), **1.3.18.3(a)** (solid rectangular insulated
copper, 200–3000 A feeder trunking), **1.3.18.3(c)** (never in damp
places), **1.3.18.4** (busduct bars shall be copper), **1.3.37.3.5**
(copper earthing busbar mandatory in LT panel/MDB/DB and in DB/FDB/SDB/
BDB; crimped lugs, brass bolts).

**Chapter 20's sources (do not re-discover).**  `HW Connection Diagram
All.pptx` slides **25–28** are the only float-switch slides in either
deck — s25/s26 = Single Condition (circuit / connection), s27/s28 =
Double Condition.  All four are embedded via `assets_ch20.py`.  Two
things that were decided while building it and should not be re-litigated:

- **s25 says "MC = Magnetic Conductor", which is wrong** — it is Magnetic
  *Contactor*.  The crop box deliberately cuts that legend off (x1 =
  0.775); the correct term lives in the prose and the diagram's note strip.
- **s26/s28 use com–NO on the first switch.**  That is drain/sump logic
  (pump runs when water rises), not tank-filling logic.  §২০.৬.৫ says so
  explicitly and gives the com–NC variant for filling an overhead tank.
  This is not an error in the source — it is a different job.

The ten photographs come from Wikimedia Commons.  The pair that carries
the chapter is **Float switch off / Float switch on** (Martin Meise,
CC BY 3.0) — the same cable float milled open in both states, so the
steel ball, the lever and the micro-switch pin are all visible and the
only difference between the two frames is where the ball sits.

**Ch20's arithmetic reuses ch18's motor** — 1 HP, 230 V, cos φ 0.85,
Eff 0.70, FLC 5.45 A.  Worked examples ২০.১ (5.45 A vs an 8 A inductive
rating) and ২০.২ (2 HP → 10.9 A, contactor required) and সারণি ২০.৪'s
whole column of FLC figures all come off that one chain.  Change ch18's
motor and all of it moves.

Facts verified for ch20 (do not re-verify): **"16(8) A" means 16 A
resistive, 8 A inductive** — the European marking convention behind
IEC 61058 / IEC 60730.  **Sulzer ABS KS datasheet**: minimum free cable
50 mm → minimum switching differential 100 mm, cable H07RN-F 3G1.0,
IP68, 60 °C continuous.  **BNBC Part 8 Ch 1 clause 1.3.27(d)** is the
float switch's legal footing — it forbids automatic restart after a
supply failure but explicitly does *not* preclude "starting a motor at
intervals by an automatic control device, where other adequate
precautions are taken against danger from unexpected restarting".  Also
used: 1.3.27(a) (every device in the motor's current path must carry at
least its FLC), 1.3.27(c) (>0.376 kW needs control gear with overcurrent
protection), 1.3.7.4 (×1.65 for small inductive loads), 1.3.17.3 (no
board on a damp wall).

**Chapter 19's sources (do not re-discover).**  The institute has
**nothing** on IPS/UPS — `Electrical House Wiring book.docx` has not one
paragraph, and every slide's text in both diagram decks was extracted and
checked: no IPS/UPS slide exists.  `Solar System.docx` has only the
off-grid battery/inverter sizing arithmetic, no hardware photos.  So all
ten photographs come from Wikimedia Commons via `assets_ch19.py`, credited
in the ❖ চিত্রসূত্র box.  The two that carry the chapter are **UPSRearView**
(Scott Power SDL 500 — a sharp, legible `Output 220-240V~ 50Hz, 300W,
500VA` plate; 300/500 = PF 0.6, which is the whole power-factor lesson in
one photograph) and **12V VRLA Battery** (RITAR RT1245 — `12V 4.5AH/20HR`
plus cycle 14.6–14.8 V, standby 13.7–13.9 V and a 1.35 A initial-current
limit, i.e. 0.3C).  The scope trace of a modified sine against mains was
measured on a 60 Hz system — the caption says so.

**Ch19's arithmetic is one chain — change one number and all of it moves.**
350 W design load → 437.5 VA → 600 VA · 4 h at 12 V, DoD 0.8, η 0.85 →
171.6 AH → 200 AH · 130 AH gives 3.03 h · charge 20 A for 6.5 h · DC
current 34.3 A at 12 V and 17.2 A at 24 V.  §১৯.৮.৩'s market table, the
backup-time table in §১৯.৮.৫, চিত্র ১৯.১৫ (`d13_flow`) and worked examples
১৯.১–১৯.৫ all quote these.  `ch19.py`'s docstring repeats the list.
**Prices are deliberately absent** — the ch17 tariff problem applies here
too, and the Bangladeshi price sites disagree with each other.  Capacities
and model sizes last; prices do not.

**`photo_callouts()` in `dia_ch19.py` is the reusable win from ch19** — a
photograph in the middle, Bangla labels down both margins, leaders drawn
*after* the image.  Three traps it now encodes, each of which shipped once
and had to be fixed:  (a) draw the image **before** the callouts or the
image covers the leaders and every label points at the picture's edge;
(b) aim the leader **beside** the printed lettering, never on top of it —
on a nameplate figure the lettering *is* the lesson;  (c) position each
label at its own target's height instead of spreading labels evenly down
the margin, or a two-label side gets one leader slashing diagonally across
the whole photograph.

**`qc.py` checks text, not boxes.**  Ch19's `d11_connect` shipped a "সকেট"
block whose rectangle ran off the right of the canvas while its *text*
stayed inside — QC passed it clean.  When a row of blocks is laid out by
centre, check `cx + w/2` against the note-strip's right edge (1194) by
hand.

**Chapter 18's sources (do not re-discover).** `Motor.docx` at the root holds
the institute's own connection drawings inside `word/media/` — image5 = run
capacitor, image6 = DP switch + pump, image7 = start-run capacitor, image10 =
star terminal block, image12 = delta terminal block. They are RGBA with a
transparent background, so they must be composited onto white before use or
they print black (`assets_ch18.py` does this, and asserts each image's pixel
size so a changed source file is caught). **Neither `HW Connection Diagram
All.pptx` nor `Circuit Diagram.pptx` has any motor slide** — every slide's
text was extracted and checked. The cutaway motor photo, stator and rotor come
from Wikimedia Commons (PD / CC BY-SA), credited in a ❖ চিত্রসূত্র box.
USDA Farmers' Bulletins on Commons ("Electric motors for the farm", "Selecting
and using electric motors", "Single-phase electric motors for farm use") are
public domain and full of usable motor line art if a later chapter needs it.

**Chapter 13 — চিত্র ১৩.৫ and ১৩.৯ rebuilt on 2026-08-29** on the user's
review ("13.5 er diagram er ba dan agulo change kore onno format e present
koro..like a, b · 13.9 er diagram kissu bujha jay na").  Still 19 pages, no
page-foot gap above 3 cm.  Do not re-discover:

- **চিত্র ১৩.৫'s terminals are now lettered A · B (left) and C · D (right)**,
  each in a filled `badge()` disc at the wire's outer end instead of the old
  "বাঁ ১ / ডান ১" text floating above the wire.  The verdict line reads
  `A → C · B → D` / `A → D · B → C`.  §১৩.৫'s paragraph, numbered steps ২–৩
  and the ⚠ box were rewritten to use the same letters, so picture and prose
  agree.  A "বাঁ পাশ A · B" sub-line was tried and dropped — it straddled the
  switch-body's dashed rect and `qc.py` flagged it (`box edge cuts`).
- **চিত্র ১৩.৯ was redrawn as a proper sectional elevation.**  The old one had
  a near-white staircase that read as nothing, both board labels floating in
  the wrong storey, and — worst — it drew *one* line where it said "২টি
  স্ট্র্যাপার তার", so the figure whose caption is "তার কয়টি" never showed a
  count.  Now: roof slab, two walls, a thick ground-floor slab, the mid-floor
  slab with the flight of stairs landing on it, DB + সুইচ বোর্ড ১ downstairs,
  সুইচ বোর্ড ২ upstairs, the lamp hung in the stairwell.  **Every conductor is
  drawn as its own line** — 2 to board ১, 3 between the boards, 1 to the lamp,
  1 neutral — each bundle crossed by an oblique tick with a numeral disc
  beside it (`wire_tag()`), which is the count convention on a real drawing.
  A one-line colour key (`_wire_key()`) sits under the section; the *routes*
  and what each wire is stay in সারণি ১৩.৪ right below, so the figure does not
  repeat the table.
- **A horizontal run cannot pass under a flight of stairs** — at the flight's
  foot the soffit meets the floor, so there is zero clearance and the first
  draft's strappers cut straight through the bottom two steps.  The fix is
  also the honest one: give the ground floor a **thick slab** (62 px here) and
  run the three conductors *inside* it, the way conduit is actually cast in.
- **Prose length is load-bearing here.**  §১৩.৫'s opening paragraph is exactly
  three lines in the built page; at four it no longer fits the foot of p7, the
  whole chapter shifts by one block and উদাহরণ ১৩.১ is stranded with a
  9–11 cm gap on p10.  Two rewrites of that one paragraph were needed.  Check
  `layout.py` after *any* wording change in a chapter that already sits clean.
- **`T_SMALL` was 20 px on a 1240 px canvas = 7.04 pt at 15.4 cm**, under this
  project's ~7.5 pt floor (the ch11 lesson, which post-dates ch13's delivery).
  Raised to 23 for the whole chapter; no figure's canvas height changed except
  d09's own (764 → 874 px, i.e. 15.4 × 10.9 cm placed).

**চিত্র ১৩.৫ split into two figures on 2026-09-05** (user: "13.5 diagram ta
duita alada kore dekhaw..jate ektu boro bujha jay") — the two states this
figure carries (সোজা / আড়াআড়ি) used to sit side by side in one 1240×660
canvas, each state squeezed into a 560 px-wide half. `dia_ch13.d05_inter_inside`
is now `_inter_panel()` called twice — `d05a_inter_straight` and
`d05b_inter_crossed` — each on its own full 1240-wide canvas (panel width
1148 px vs the old 560), so WD/SPR/badge radius/badge font could all scale
up (200→320, 66→106, 21→34, 24.5→36) without `qc.py` collisions. **Every
figure from চিত্র ১৩.৬ onward shifted its printed number by +1** — this is
automatic (`b.figure()`'s `fig_n` counter, not a hand-typed string) and
needs no manual fix, but it does mean the 2026-08-29 note above is stale
where it says "চিত্র ১৩.৯" for the stair sectional elevation — that figure
is **চিত্র ১৩.১০** now (`d09_stair_layout`, still the same drawing, same
file basename). Section numbers ১৩.১–১৩.১১ are separate hand-typed strings
in `b.h1()` and are untouched by this — figure numbers and section numbers
were only ever coincidentally aligned up to ১৩.৫, not by any rule.
**Closing the new page-foot gap used the standing playbook, not a
special case**: adding the extra figure pushed §১৩.৬ (টানেল বা গোডাউন
ওয়্যারিং) into a 7.82 cm gap on p10, next figure (চিত্র ১৩.৯,
বাতি জ্বলার ক্রম) stranded whole on p11. Fixed by moving that figure to
sit right after d07_tunnel's figure (figures now back-to-back), with both
explanatory paragraphs following after — not before — the pair. 18 → 19
pages, 0 gaps above threshold.

**Chapter 12 — seven figures rebuilt on 2026-08-28** on the user's review
("12.1 marking thik vabe hoy nai · 12.2 er rotor vitore keno · 12.5
polarized/non-polarized real pic soho with marking · 12.6 er fan er jonno
practically je capacitor use hoy seta daw · 12.3 e celling fan capacitor
show koro, real pic · 12.7 and 12.8 er circuit diagram er wire valo moto
connected draw kora hoy nai").  Do not re-discover any of this.

- **A ceiling fan is an OUTER-ROTOR motor and চিত্র ১২.২ had it backwards.**
  The old figure drew a textbook inner rotor inside a ring of stator poles.
  In a ceiling fan the shaft that comes down the down rod is **stationary**,
  the stator and both coils are clamped to it, and the visible housing *is*
  the rotor — it turns on two bearings around the stator and the blades bolt
  to it.  `d02_motor` is now a two-view section (পাশ থেকে / নিচ থেকে) drawn
  by `_motor_section()` + `_blades()` in `dia_ch12.py`, and §১২.৩ says so in
  prose with the reason (big-diameter rotor → more inertia → smooth at low
  speed; the spinning shell cools itself).  `qc.py` cannot catch a wrong
  machine topology — it checks text, not physics.
- **A cutaway must be broken open on one side or every interior label's
  leader crosses a wall.**  `_motor_section()` draws the left wall in full
  section and the right wall as two stubs with a jagged break between them,
  so বেয়ারিং / স্টেটর / কয়েল are reached from the right with no crossing.
  Cage bars are drawn only on the *unbroken* wall, for the same reason.
- **Commons has no 2-wire ceiling-fan run capacitor** — searched by keyword,
  by `Category:Film capacitors` / `Motor capacitors` / `Power capacitors`,
  and through Openverse.  What it does have (`Ceiling fan capacitor.png`) is
  a **4-wire multi-value CBB61 for a speed regulator**, which is what ch12
  used to print as "the fan's capacitor" in চিত্র ১২.৩ *and* চিত্র ১২.৬ —
  a content error, not just a picture problem.  The institute's own files
  have nothing either (`Motor.docx` image5/image7 are 40 MFD 440 V pump
  capacitors, already used by ch18; all 210 images of `Electrical House
  Wiring book.docx` were checked).  So `assets_ch12.WEB` pulls three
  **manufacturer product photographs** (user authorised this on 2026-08-28,
  copyright accepted): `ph_cap_fan` / `ph_cap_fan_face` (a CBB61
  `4 µF ±5%  450V.AC  50/60Hz  40/70/21  SH  S3`, every line legible) and
  `ph_cap_elko` (a 1000 µF 25 V electrolytic with the silver stripe, the
  − bars and the arrow facing the camera).  The ❖ চিত্রসূত্র box names them
  as প্রস্তুতকারকের পণ্য-আলোকচিত্র.
- **The marking figure carries six callouts, the meanings go in a Word
  table** (সারণি ১২.৬) — the ch22 pattern.  Verified: `SH` = self-healing,
  `S3` = the safety-protection class of IEC 60252-1 (segmented film, the
  top step; S0/S1/S2 are the lower ones), `40/70/21` = climatic category
  per IEC 60068-1 (−40 °C / +70 °C / 21 days damp heat).  Do not re-verify.
- **d07/d08 were redrawn as a vertical ladder with three named leads.**
  The old চিত্র ১২.৭ left the phase and neutral buses dead-ending in white
  space and never showed the কমন প্রান্ত at all, though §১২.৫'s step list
  talks about C/R/S throughout; the old চিত্র ১২.৮ crossed two red wires
  over the starting coil.  Now: C at the top, running coil down the left,
  starting coil down the right, capacitor across R–S at the bottom, neutral
  onto R.  **Direction is reversed by moving the neutral from R to S**, not
  by "swapping the starting coil's ends" — same physics, but it is what a
  technician actually does on a 3-lead fan, and §১২.৫.১ and MCQ ৯ were
  rewritten to match the picture.
- **`T_SMALL` was 20 px on a 1240 px canvas = 7.04 pt at 15.4 cm**, under
  this project's ~7.5 pt floor (the ch11 lesson, which post-dates ch12's
  delivery).  Raised to 22.5 (7.92 pt) with `T_BODY` 23.5 and `T_CALL` 25.5,
  and every figure re-checked — `d06`'s comparison table then grew a page,
  fixed by dropping its tile height 300 → 262 and shortening one cell.
- **The MCQ key was ক২ খ৯ গ৩ ঘ০** — the standing CLAUDE.md check again.
  Reordered to ক৪ খ৪ গ৩ ঘ৩.
- **Capacitor values and voltage grades went Latin** (`2.2 – 4.5 µF`,
  `400–450 V AC`) in সারণি ১২.৪, the সারসংক্ষেপ and the MCQ options — the
  ch23 rule: where the digit *is* the identity of the part, Kalpurush's
  ৪-drawn-as-8 turns it into a different component.
- **Second review, same day: the box CBB61 was the wrong "practical" part.**
  The user's own photograph settled it — what actually hangs in a Bangladeshi
  ceiling fan's canopy is a **grey cylindrical aluminium can with two spade
  terminals**, marked `SH CAPACITOR  2.5 µF  350V.AC  NO-PCB'S  MADE IN
  THAILAND` (2.5 / 3.15 / 3.5 µF are the sizes on the shelf, and the grade is
  **350** V AC, not 450).  The CBB61 box is real too but it is the second
  form, not the first.  চিত্র ১২.৩ is now three tiles (গোল কৌটা · বাক্স ·
  স্টার্ট) and চিত্র ১২.৬ reads the *can's* markings; সারণি ১২.৬ carries
  both sets, the box's extra lines under a "বাক্স ধরনে আরও যা থাকে" row.
  `NO-PCB'S` = no polychlorinated biphenyl in the impregnating oil — worth a
  table row, it is the only marking a trainee will not guess.
- **A "long leg / short leg" claim needs a photo where the legs differ.**
  The first electrolytic crop cut both leads to the same length while the
  caption taught the rule — the user caught it.  The same source photograph
  has the difference in it (upper lead to fx 0.955, lower to 0.89); the crop
  just has to reach the lead *tips*.  That forces a ~2.6:1 landscape frame,
  so চিত্র ১২.৫ became two full-width rows instead of two side-by-side
  panels — a wide component cannot share a half-width panel and stay legible.
- **An arrowhead sticks out past the path's end point.**  d08's rotation arc
  ended 16 px above its caption and `qc.py` passed it, because QC scores text
  against rects and paths, not against a marker.  Leave ≥ 25 px between a
  marker-terminated path and any text under it.
- **A rotation/flow arrow needs its own band, clear of every conductor**
  (user, 2026-08-28: "12.8 er diagram er lekhe overlap hoyeche").  d08's
  ঘূর্ণন arc sat at the panel foot on a chord of 104 px with r=54, i.e. a
  39 px bulge — fine in the left panel, where the neutral stops at R, but in
  the right panel the neutral runs the full width to S and the green arc rode
  straight over it.  `qc.py` is blind to it: it scores *text* against rects
  and paths, never path against path.  The fix is geometry, not nudging —
  flatten the arc (chord 120, r=88 → 24 px bulge) and drop it into a band
  below the lowest conductor, then let the panel grow to hold it (PH 516 →
  540, caption at `96+PH-26`).  Check a drawn arc's sagitta
  `r - √(r² - (chord/2)²)` against whatever runs above it before shipping.
  Costs nothing in pages here — still 24 pp, worst gap 4.19 cm.
- **Page-foot gaps: 24 pp with 4.19 / 5.27 / 9.95 cm → 23 pp with one
  4.19 cm.**  Three moves, all from the standing playbook: চিত্র ১২.২ went
  *after* the running/starting comparison table, উদাহরণ ১২.৩'s four
  `steps=` lines merged to two, and one genuinely-owed paragraph (the air
  gap, and why a worn bearing — not the coil — is the first suspect when an
  old fan grinds) was added at the end of §১২.৩.

**Chapter 11 — rebuilt TWICE on 2026-08-25.**  First pass answered
"vitorer lekha gulo buja jay na … ami joint er real picture chay";  the
user then came back with "real pic gulo ghola … diagram gulo drawing e
onek somossa onek vull … perfect vabe banaya daw".  Both reviews were
right.  Do not re-discover any of this.

*From the first pass (still true):*

- **The type really was under the legal minimum.**  `T_SMALL` was 20 px
  on a 1240 px canvas; at 15.4 cm that is **7.04 pt**, below the ~7.5 pt
  floor this file sets, and three figures were placed *narrower* still
  (13.8–14.6 cm), which took them to 6.7 pt.  Now `T_SMALL` 23 → 8.1 pt,
  `T_BODY` 25 → 8.8 pt, and `ch11.py` builds its width dict as
  `{f"d{n:02d}": 15.4 …}` so no figure can quietly be narrowed again.
  **Check `N × P(pt) / W` for the smallest label of every new chapter.**
- **Sharp 1916's plates are gone.**  Public domain and correct, but a
  century-old halftone's hairlines vanish at 15.4 cm — চিত্র ১১.২-এর
  "সঠিক" and "ভুল" panels printed as two identical black scribbles.
- **`s.poly()` does not register in `svgkit`'s `shapes` list**, so
  `qc.py` is blind to it;  the same is true of `image()` overlaps beyond
  the image's own rect.
- **Long tie vs short tie needs a marker, not just different geometry** —
  a plain red bracket under the middle section, no text.

*From the second pass — the drawing kit was replaced outright:*

- **The one bug behind "onek vull" was `wrap()`.**  It drew a few slanted
  strokes, nothing more.  So (a) the main conductor vanished under the
  turns and (b) the wrapping wire had no continuity with the branch — the
  branch stopped in one place and a detached spring sat beside it.  Every
  joint in the chapter read as "a spring next to a wire" instead of "a
  wire wound on a wire".  `qc.py` cannot see this: it checks text, not
  whether an object matches the thing it is named after.
- **The replacement is a real 3-D helix with depth occlusion**, and it is
  reusable for any chapter that has to draw a wound or twisted wire:

      বিন্দু(t) = p0 + u·(tL) + n·(r·cos θ)      θ = 2π·turns·t + phase
      গভীরতা(t) = sin θ        (+1 towards the viewer, −1 behind)

  `_helix_pts` samples it, `_split` cuts the sample list at the silhouette
  (sign change of sin θ, keeping the crossing point in **both** runs so
  there is no gap), and `wound_multi(s, core, *segs)` draws every
  back-facing run, then calls `core()`, then every front-facing run.  That
  ordering is the whole trick.  `twist2()` is the same machinery with two
  helices 180° apart (a true twisted pair);  `tube()` fakes roundness with
  4–6 progressively narrower, lighter, upward-offset strokes rather than an
  SVG gradient — the figure ships to Word as **SVG**, and Word's and
  LibreOffice's renderers are not the same, so plain `<path>` only.
- **Wraps must be tight — geometry comes from the wire diameter, not the
  panel.**  `পাকের দৈর্ঘ্য = পাকসংখ্যা × ব্যাস × 1.06` (`PITCH`), and
  `TPITCH = 2.05` for a mutual twist.  The first rebuild sized the joint to
  fill the panel, so six turns spread over 300 px and looked like rope.
  Each joint function now centres itself on a given `cx` and lets the
  insulated tails fill whatever is left.
- **Guards, because `qc.py` will not catch any of this.**  `within()`
  raises when a joint overruns its panel — horizontally (`bounds=`) *and*
  vertically (`ybounds=`, for the tap/cross branch that hangs below the
  wire and the one that reaches up into the header chip).  Three real
  overflows shipped in this session before the guard existed.
- **Content errors fixed in the artwork**, each the ch09 count-the-features
  class:  **Britannia** was drawn as a single thick bar, so "দুই তার
  পাশাপাশি" — the definition of the joint — was not in the picture at all;
  it is now two conductors 1.5 radii apart, one end bent up and the other
  down, and the binding is wound **from the centre outward in both
  directions** (`turns` negative on the left half, so the two halves have
  opposite handedness, exactly as ১১.৫.২ describes).  **Fixture** had two
  wires of equal thickness, though unequal size is the joint's only reason
  to exist;  the thick wire's tip now really folds back over the turns.
  **Married** stage খ now interleaves the strands (14 parallel strands,
  alternating light/dark by origin) and the finished joint tapers.  **Tap**
  gained a third panel for the stranded case ১১.৬.১ already describes in
  prose.  **Tape** was flat black fins that read as a comb;  it is now a
  wide-ribbon helix at half-lap pitch (`bands=2` keeps a ribbon flat).
- **The three blurry photographs are gone, and this is final.**  Abuz
  Mordecai's Western Union / tap / Britannia shots are out of focus in the
  2048×1536 originals — unsharp masking cannot rebuild detail that was
  never captured, it only sharpens the chroma noise.  A printed textbook is
  better served by an exact drawing.  **Do not go looking again:** on top
  of the first pass's search, a second sweep built a 333-file candidate
  list from fifteen search terms plus `Category:Splices` (rope),
  `Category:Soldering`, `Category:Electrical wiring`, `Category:Twist-on
  wire connectors` and `Category:Copper wire`, sorted by pixel size and
  checked by eye — everything is rope splicing or RNA splicing.  The two
  photographs that stayed (`ph_pig_real`, `ph_pig_nut`, cropped from Dmitry
  G's 7300×10960 junction-box shot) are sharp;  so are `ph_solder_iron`,
  `ph_wire_nuts` and `ph_lever_conn`.
- **The institute's own book DOES have joint pictures — `image58`–`image64`
  of `Electrical House Wiring book.docx`** (missed on the first pass; they
  sit between "নিম্নে বৈদ্যুতিক তারের বিভিন্ন জয়েন্ট দেখানো হয়েছে" and
  "জয়েন্ট করার পদক্ষেপ সমূহ").  They are **clip-art drawings, not
  photographs**, and the largest is 1148 px, so they were used as the
  **drawing reference** — image63 settled the Britannia geometry and
  image61 the duplex/staggered layout — not embedded.  By content they are
  58 = টি/ট্যাপ · 59 = পিগটেল · 60 = ম্যারিড · 61 = ডুপ্লেক্স ·
  62 = ওয়েস্টার্ন ইউনিয়ন · 63 = ব্রিটানিয়া · 64 = বেল হ্যাঙ্গার (a knot
  with wraps either side).  **The file's own label order for the last three
  is unreliable** — trust the pictures.  Note the institute teaches a
  **বেল হ্যাঙ্গার জয়েন্ট** that this chapter does not cover;  flagged to
  the user, not added.
- **চিত্র ১১.২ (স্কিনিং) was rebuilt a third time**, on the user's
  "11.2 diagram thik vabe banaw".  Three separate faults, all invisible to
  `qc.py` because the knife is a `poly`/`path`:  the blade was a bare
  triangle, so held steep it read as a needle and held flat as a grey
  wedge;  the peeled insulation was a line-drawn spiral that read as a
  hook hanging beside the wire with no visible connection to the blade;
  and **the খাঁজ the whole figure exists for was never drawn** — only a
  red ring and a warning triangle sat on unbroken copper.
  What it is now, and the three reusable pieces:
  - `knife()` draws a real sheepsfoot blade — **straight cutting edge,
    curved spine** — plus a bright bevel strip, a bolster and a riveted
    wooden handle.  `spine=±1` chooses which side the back is on, i.e.
    which way the edge faces;  on a "how to hold it" figure the edge must
    face the work or the picture says nothing.
  - **The handle needed a second fix** (user: "knife er hatol thik hoy
    nai").  It flared out toward the butt like a shoe, and the cause was
    one SVG path command:  the closing `Q` had its **control point at the
    handle's front-top corner and its end point at the front-bottom
    corner**, so a single curve swept diagonally across the whole handle
    instead of the top edge running straight.  A handle is two
    **parallel** `L` edges with the rounding only at the butt.  Two
    proportions also matter and were both wrong:  the handle must be
    about as long as the blade (it was 73 %, so it read as a stubby
    paddle) and only ~1.3× the blade's depth (it was 1.5×).  General
    rule when a drawn object looks "off" but the geometry seems right:
    read every `Q`/`C` and check *which* corner the control point sits
    on — a stray control point deforms the whole silhouette, and `qc.py`
    never sees it because the shape is a `path`/`poly`.
  - `notch()` cuts the nick by drawing a **V filled with the panel's own
    background over the copper**, so the conductor's dark rim is covered
    too and it reads as removed metal, plus a hairline crack from the
    apex.
  - `magnifier()` — `clip_begin` takes a rect, but side = diameter with
    `rx` = radius **is** a circle, so no extra clip-path is needed.  Both
    panels carry the same magnifier at the same size and position:
    smooth copper on one side, notch and crack on the other.  A 24 px
    conductor's nick would print under 1 mm; the magnifier is what makes
    the chapter's whole point legible.
  - **Do not draw the shaving as a curl.**  Three attempts (tight spiral,
    loose spiral, tapered spiral) all read as an iron hook.  What works is
    showing the *result*: the insulation's mouth **shaved to a long taper
    down to the copper — a sharpened pencil**, which is literally what the
    section says, with the blade lying almost flat along that taper.  The
    taper needs to be long (≈2.5× the insulation diameter) or it reads as
    a collar, and it wants the tube's own light/shade lines or it looks
    like a flat patch.  The wrong panel keeps its square-cut mouth, and
    that contrast teaches too.
- **Two ordinary text defects found while re-reading the PDF:** the MCQ key
  was ক2 খ7 গ5 **ঘ0** (the standing CLAUDE.md check again — it is easy to
  write the key and never read it as a string);  options reordered to
  ক4 খ4 গ3 ঘ3.  And "জয়েন্ট কেটে নতুন করে করে সোল্ডার" had a doubled word.
- **Page-foot gaps: the fix was one figure, not a shuffle.**  The rebuilt
  figures added ~8 cm in total and the chapter went to 25 pages with three
  6–8 cm gaps on consecutive pages — §১১.৫.২/৩ and §১১.৬.১ each run
  ~5 cm of text + ~8 cm of figure, so two sections never fit one page.
  Trimming dead space inside panels only moved the gaps (the ch17 lesson).
  What worked: **চিত্র ১১.৫ went from two stacked full-width panels to two
  side-by-side panels**, 7.3 cm → 4.5 cm, which let চিত্র ১১.৬ fit on page 9
  and unlocked everything after it.  Back to 24 pages, worst gap 3.64 cm.
  A tall figure whose content is a *comparison* is the first candidate for
  going side-by-side.

**Chapter 6's চিত্র ৬.১ and ৬.২ — rebuilt 2026-08-25 on the user's review**
("6.1 kissu bujha jay na … 6.2 te real image add koro").  Do not re-discover:

- **চিত্র ৬.১ used to be unreadable and the review was right.**  The
  electromagnet sat far from the armature joined only by a dashed line, the
  gong was a floating semicircle, and the make-and-break cycle — the whole
  point of a trembling bell — was not drawn at all, only listed in a
  five-bullet panel that repeated the body text.  It is now two panels:
  **গঠন** (the device seen face-on, exactly the view you get when the cover
  comes off — back plate, U-core, two coils, armature over the pole faces
  with the air gap filled in amber, leaf spring on a clamp, contact screw
  from the top rail, hammer, gong, terminal block) and **কার্যপ্রণালি**
  (the same mechanism twice — contact closed / contact open — with a cycle
  arrow between).  The internal wiring is deliberately **not** drawn: in a
  real bell it runs behind the plate, and every attempt to route it on the
  face either crossed the armature or shorted the contact post to the
  armature post.  The circuit belongs to the state panel and to চিত্র ৬.৩–৬.৭.
- **Six photographs from Wikimedia Commons** via `assets_ch06.py`, credited
  in a ❖ চিত্রসূত্র box that iterates `credits.json` (never a hand-written
  list — the ch22 lesson).  The institute has **no bell photograph**:
  `Electrical House Wiring book.docx` has only the bell *push switch*
  (image70) and the gang push bell switch (image82); neither diagram deck
  has a bell device shot.  `DoorBell 001.jpg` (HNH, CC BY-SA 3.0) is the
  find of the job — a trembling bell with the cover off, every part of
  চিত্র ৬.১ visible in the real object.  `Block Instruments-2.JPG` is a
  **Tyer's single stroke block bell** (the Commons description says so) —
  the only real single-stroke bell photograph on Commons.
- **A Commons title with a bracket and two scripts breaks in LibreOffice.**
  `Звонок электрический советский (সোভিয়েত গং বেল)` printed with the "("
  hoisted to the head of the line.  Credit titles that mix scripts must
  carry no brackets.
- **`head_bar()`'s rounded corner cuts its own text when the bar is short.**
  The second (square-cornered) rect starts at `y + rx`; if `h/2 - 0.46×size`
  is less than `rx`, the text box straddles that edge and `qc.py` reports
  "box edge cuts".  `dia_ch06.head_bar` now clamps `rx` from `h` and the
  type size — copy that version forward.
- **Page-foot gaps closed by two reorderings, both from the standing
  playbook.**  The four circuit sections now run steps → ⚠ safety box →
  figure (was figure → box), and §৬.৬'s numbered steps moved ahead of
  চিত্র ৬.৭.  That took 6.11 cm (p13) and 5.10 cm (p8) down to a single
  3.70 cm gap on p4.  Chapter is 14 pages now (was 13).
- **The MCQ answer key was skewed** — খ nine times out of twelve.  Options
  reordered to ক৩ খ৩ গ৩ ঘ৩; the CLAUDE.md standing check applies to a
  rebuild of an already-delivered chapter too.

**Chapter 3's holder figure — rebuilt 2026-08-25 on the user's review.**
Three complaints, all correct: চিত্র ৩.১-এর "বিদ্যুৎ বহন করে" sat on the
summary box, চিত্র ৩.২-এর "শর্ট পথ" was printed *on* the red short-path
line, and চিত্র ৩.৩-এর four holders were hand-drawn sketches that looked
nearly identical — nobody could recognise a holder in a shop from them.
What came out of it:

- **Four of the five holder photographs are the institute's own**, pulled
  from `Electrical House Wiring book.docx` by `assets_ch03.py`:
  `image88` = ব্যাটেন পিন (BC) · `image89` = ব্যাটেন প্যাঁচ (ES) ·
  `image90` = পেন্ডেন্ট পিন · `image91` = পেন্ডেন্ট প্যাঁচ (`image92` is
  the ceiling rose, not used).  The order inside `word/media/` is the
  document's own order and was verified blip-by-blip against the text
  ("ব্যাটেন হোল্ডার: এই হোল্ডার থ্রেড (প্যাচ) টাইপ ও পিন টাইপ হয়ে থাকে…").
  Institute-owned, so no ❖ চিত্রসূত্র box — that box is only for the
  CC BY-SA Commons material.
- **The fifth, the angle holder, is `angle-holder.jpg` at the project
  root — the user supplied it on 2026-08-25.**  `assets_ch03.ROOT_PICS`
  reads it exactly like the docx images (size assertion, white-flatten,
  tight crop).  It is a **pin (BC)** holder — verified from the brass
  bayonet slots in the photograph, not from the filename.
- **Do not go looking for another angle-holder photograph.**  There is
  none in the institute file (all 210 images eyeballed), none in either
  diagram deck (all 155 embedded images eyeballed), and none under a free
  licence anywhere: Wikimedia Commons was searched by category
  (Lampholders, Lampholder sockets, Light bulb sockets), by `allimages`
  prefix, and in English/German/French/Spanish/Indonesian; Openverse
  (Flickr + Science Museum + all CC sources) and Pixabay too.  What the
  open web has is seller/manufacturer product shots — copyrighted, and
  every other picture in this book is either institute-owned or CC with a
  credit.  The `Lampholder socket 01–05` files on Commons look promising
  in a title list but are ES-to-ES angled *adapters*, not holders.
- **The angle holder needed its own drawing function, `_angle_holder()`.**
  `_lamp_unit()` cannot draw it and two attempts to force it failed:
  that helper puts base, shell, ring and bulb on **one axis**, but an
  angle holder's base lies in the wall's plane while its mouth is at an
  angle to it.  Drawing the shell tilted gave a box glued to a blob;
  hiding the shell inside a dome (`body=False`) gave a grey half-circle
  with a matchstick stuck on.  The user rejected both.  What works is one
  **closed body path** — out of the wall, swelling, ending at the angled
  mouth plane — with the collar, the brass ring and the bulb drawn on top
  of it, plus a mounting plate drawn *before* the body and made a little
  taller so it peeks out top and bottom and reads as a plate.  General
  lesson: when the real object's parts are not colinear, a rotated
  one-axis helper will never look right; draw the silhouette.
- **The figure now answers two questions instead of one.**  Top row =
  আসল হোল্ডার (photographs, mounting × cap-type), bottom row = বসানোর ধরন
  (drawn: ছাদ / দেয়ালে কোণ / সিলিং রোজ থেকে ঝুলন্ত).  That split fixed a
  content error too — the old bullet list ran mounting types and cap types
  together, so "স্ক্রু হোল্ডার" read as a fifth kind of mounting.  §৩.৩'s
  prose now names three mountings and two caps and says the two are
  independent.
- `_lamp_unit()` in `dia_ch03.py` draws holder + bulb at any angle from one
  local coordinate system.  **The filament arc is deliberately not rotated**
  — at −46° a rotated arc reads as a hook, not a filament.
- Chapter is 16 pages now (was 15) and the two old ~4.6–4.8 cm gaps are
  gone; worst is 4.26 cm on p2.

**Tariff figures in ch17 will go stale.** The rates in সারণি ১৭.৩ are BERC's
retail order effective from the June 2026 billing cycle, including the 4 June
2026 correction that rolled the lifeline (0–50) and first-step (0–75) slabs
back to 4.63 and 5.26. Demand charge Tk 42/kW, VAT 5%, late-payment surcharge
5% once. When these change, সারণি ১৭.৩, `dia_ch17.d03_slab`, `d04_bill` and
worked examples ১৭.২/১৭.৩/১৭.৪ all have to be recomputed together — the
docstring of `ch17.py` says so too. Research note: the official BERC/BPDB/DPDC
PDFs live on `objectstorage.ap-dcc-gazipur-1.oraclecloud15.com`, which is
**unreachable from this machine** (connect timeout), and `berc.org.bd` has a
broken TLS chain (`curl -k` works, WebFetch does not). The slab numbers were
settled instead from Prothom Alo / Daily Star / bssnews coverage of the 3 June
2026 order cross-checked against `ebill.info.bd/tariff`; low-quality SEO blogs
disagree with each other and with the order — do not trust them.

**Standing check for any chapter with MCQs:** ch17's first draft had every
answer on option (খ). `mcq()` does not shuffle. Read the answer key as a
string before shipping and reorder options so the key spreads across ক/খ/গ/ঘ.
(ch19 ships ক২ খ২ গ৩ ঘ৩.)

**MCQ answer-key rebalance pass, 2026-09-04** (user: "class 10 pass kora
student o porbe … best way te abar check kore"). This standing check had
only ever been applied from ch16/ch17 onward (and the rebuilt ch06/11/12);
**chapters 1–5, 7–10, 13–15 still had their keys skewed hard to খ** — ch08
was 14–15 of 16 on খ, ch02/04/07/14/15 were 10–12 of ~15. Fixed
programmatically: `_fix_mcq.py` (deleted after) parsed each `mcq = […]`
list with `ast`, took the existing key as the correct-answer index, and
**rotated each question's four options** to a per-chapter, deterministically
shuffled, near-equal ক/খ/গ/ঘ target (no 3-in-a-row, seeded by chapter
number), then rewrote the উত্তরমালা line. ch15 uses inline `b.mcq(n,…)`
calls, done by hand the same way. Only option order and the key changed —
questions, distractors, facts, numbers untouched. Every one of the 12
chapters keeps its exact page count (27 20 15 18 14 · 24 20 17 · 18 28 21;
ch03 is 15 now — see below) and `layout.py` is clean. ch16–28 keys were
already balanced and were left alone (ch16 is a mild ক২ খ৪ গ৩ ঘ১, tolerated).

**Engine change made for ch16 (already in `bookkit.py`):** the math DSL now
has `\sqrt{a}`, emitted as a real OMML `<m:rad>` with `degHide`. It had to be
structural rather than a `√` character — Kalpurush has no U+221A. Verified
rendering in LibreOffice (display, and nested inside `\frac`).

**Kalpurush glyph coverage, checked against the font's cmap** (do not re-test):
missing — `√ ² ³ φ Ω ° π ∠ ≈ Δ θ ≤`; present — `× · —`. Present-in-cmap is not
proof of correct drawing: `÷` is in the cmap but draws as `+`, which is why the
existing ÷ rule stands. The missing ones fall back to another font: fine for a
lone `φ`/`Ω`/`Δ` (ch12/ch14 already ship `cos φ`), but never put `²` or `√` in
body text, a table header or an SVG label — write `ওয়াট/বর্গমিটার` in words and
get real superscripts from `^{2}` inside `b.math()`.  **The ÷ rule applies to
SVG labels too**, not just body text: ch19 drafted `ওয়াট ÷ PF` and
`1200 VA ÷ 960 W` into two diagrams before they were caught. Chrome's raster
happened to fall back and draw them correctly, so the PNG looked fine — but
Word renders the *SVG*, with Kalpurush, where it becomes `+`. Write `/`.

The Bangla-in-OMML guard from ch16 now lives in **`Book/build/mathguard.py`** —
an AST walk that flags any Bangla codepoint inside `b.math()` args or `steps=`
(`given=`/`find=` are exempt, they are `_rich` body text). Run it before
building any maths-heavy chapter:

```bash
python mathguard.py ch19.py
```

Reusable: `assets_chNN.py` (ch12/ch13/ch14/ch15) converts a source PPTX to PDF
once into `.slidepdf/` and crops any slide at 300 dpi — point `SLIDES` at the
new slide numbers and it just works. `assets_ch15.py` adds an `EXPECT` dict
that asserts each slide's page text contains the expected words and dies if it
does not; keep that, it catches an off-by-one slide before anything is cropped.
It also shows how to crop *part* of a slide (fraction box) to lift one object
out of a busy drawing — that is how ch15's piano/gang board photos were made
from slides 34 and 35.  `assets_ch19.py` is the **Wikimedia Commons** variant:
it resolves each file's URL through the Commons API, caches the download (the
API returns 429 fast if hit in a loop — sleep between requests), asserts each
image's pixel size as a tripwire, applies `ImageOps.exif_transpose` before
cropping (crop boxes are written against what commons.wikimedia.org *shows*,
and one candidate was stored rotated), and writes `credits.json` that
`ch19.py` reads to build the ❖ চিত্রসূত্র box — so the credits cannot drift
from the pictures.

Layout lesson from ch13: two `worked_example()` blocks back to back will not
share a page — Word pushes the second one whole, opening an ~11 cm gap. Put
each one in the section it topically belongs to instead of batching them.
Ch14 added the corollary: a worked example that is a page-and-a-bit long
strands a whole page. Merging its `steps=` onto fewer lines (`= 6460 W` on the
same line as the expression) shrank example ১৪.২ enough to fit, closing a
16.9 cm gap that no amount of reordering would.

Ch15's two gaps (7.9 cm and 5.7 cm) both closed by moving the figure *later*
within its own section — past the paragraph that explains it, and past a
bullet list plus a safety box. Text ahead of a figure fills the page the
figure could not fit on; the figure then starts the next page cleanly. Try
this before anything else.

Ch17 is the counter-example that sharpens the rule: moving figures around
alone turned three gaps into two and then back into three (10.5 / 8.7 / 5.6 →
7.1 / 7.0 → 9.6 / 7.0 → 13.9 / 4.8), because each move only relocated the same
stranded block. What finally cleared every gap was moving a **summary table
up**, above the subsections that explain its rows — §১৭.৫'s "বিলের অংশগুলো"
table went from the end of the section to right after its opening paragraph.
That is both better writing (list first, then one subsection per row) and the
only edit that changed how much room the following worked example had. So the
order to try is: (1) move a summary/overview table earlier, (2) put figures
*after* the worked example in their section rather than before, (3) merge
`steps=` lines, (4) only then shuffle figures. Also: shortening a diagram's
**bar/plot height** (not its width) is a legitimate way to buy 2 cm — the
placed width and therefore the type size are unchanged, so the "never shrink a
figure" rule does not apply (`dia_ch17.d03_slab`'s `base`/`top`).

Ch18 adds two more moves to that list. (a) An **embedded source image can be
placed narrower than 15.4 cm** when its own lettering is large — ch18's two
capacitor drawings went to 12.8 cm (still ~13 pt type) and two ~10 cm figures
that each owned a page then shared one. The "never shrink a figure" rule is
about *drawn* diagrams whose labels are already near 7.5 pt. (b) A **note or
formula box moved to just before a worked example** fills the page the example
could not fit on — ch18's "µF ঠিক, ভোল্টেজও দেখো" box moved from the end of
§১৮.৭ to its opening and closed a 5.4 cm gap. Adding one genuinely useful
paragraph plus a safety box ahead of a stranded example did the same for an
8.7 cm gap; if the content is real, that is better than shuffling figures.

Ch19 confirms (b) at scale: four gaps (4.8 / 7.8 / 12.1 / 5.6) went to one
(4.8) with no figure moved for its own sake. The 12.1 cm came from a bloated
worked example — five `steps=` lines and a five-line `given=` merged down to
three and two. The 7.8 cm closed by putting the **table before the figure** in
§১৯.৫.২. The last two were the ch13 back-to-back-examples trap, and both
closed by writing content that was missing anyway: a note box on the mistake
of dropping DoD and efficiency from the AH formula, and a quick-reference
table of backup hours per battery size. Prefer the paragraph you owed the
reader over the shuffle.

Also from ch15: `given=`/`find=` go through `_rich`, so Bangla numerals appear
there — and Kalpurush draws `৪` like a Latin `8`. Next to Latin values
(`বাতি ৪ × 20 W`) it reads as eight lamps. Write the count as a word in those
lines (`চারটি বাতি — প্রতিটি 20 W`), and keep `৪` out of MCQ option lists
whose other options are also numbers.

BNBC Part 8 Chapter 1 — the authority for every wiring rule in this book — is
free at `law.resource.org/pub/bd/bnbc.2012/gov.bd.bnbc.2012.08.01.pdf`.
Extract it with pymupdf and grep the clause rather than trusting memory; ch14's
clause numbers (1.3.8.2.4, 1.3.9.3.1, 1.3.9.3.12, 1.3.11.5 …) were all verified
against it.
