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
| 01 | কর্মক্ষেত্রে নিরাপত্তা | 27 | ✅ delivered |
| 02 | ইলেকট্রিক্যাল টুলস | 20 | ✅ delivered |
| 03 | বেসিক ইলেকট্রিক্যাল সার্কিট (১–৫) | 16 | ✅ delivered |
| 04 | ইলেকট্রিসিটি বা বিদ্যুৎ | 18 | ✅ delivered |
| 05 | পদার্থের প্রকারভেদ ও ইলেকট্রিক্যাল প্রতীক | 14 | ✅ delivered |
| 06 | বেল সার্কিট (৬–৯) | 14 | ✅ delivered |
| 07 | ইলেকট্রিক্যাল সার্কিট (সিরিজ/প্যারালাল/মিশ্র) | 24 | ✅ delivered |
| 08 | মেজারিং ইন্সট্রুমেন্টস | 20 | ✅ delivered |
| 09 | মাল্টিপ্লাগ সার্কিট | 17 | ✅ delivered |
| 10 | সিরিজ বোর্ড | 17 | ✅ delivered |
| 11 | জয়েন্ট, স্প্লাইস ও সোল্ডারিং | 24 | ✅ delivered |
| 12 | ফ্যান ও ফ্যান রেগুলেটর | 24 | ✅ delivered |
| 13 | টু-ওয়ে ও থ্রি-ওয়ে সুইচ | 19 | ✅ delivered |
| 14 | হাউস ওয়্যারিং: পদ্ধতি, লে-আউট ও এস্টিমেট | 29 | ✅ delivered |
| 15 | সুইচ বোর্ড | 21 | ✅ delivered |
| 16 | পাওয়ার ফর্মুলা ও ক্যালকুলেশন | 19 | ✅ delivered |
| 17 | বিদ্যুৎ বিল | 19 | ✅ delivered |
| 18 | মোটর | 26 | ✅ delivered |
| 19 | আইপিএস ও ইউপিএস | 36 | ✅ delivered |
| 20 | ফ্লোট সুইচ | 25 | ✅ delivered |
| 21 | বাসবার ও বাসবার ক্যালকুলেশন | 30 | ✅ delivered |
| 22 | সার্কিট ব্রেকার ও প্রতিরক্ষামূলক ডিভাইস | 53 | ✅ delivered |
| 23 | ক্যাবল ও ক্যাবল ক্যালকুলেশন | 49 | ✅ delivered |
| 24 | এমডিবি ওয়্যারিং | 38 | ✅ delivered |
| 25–28 | — | — | pending |

Built chapters — figures / tables / worst page-foot gap (all QC-clean):
`ch01` 14/12 · `ch02` 15/9 · `ch03` 9/6 · `ch04` 8/10 · `ch05` 7/6 · `ch06` 7/4 ·
`ch07` 10/9 · `ch08` 11/8 · `ch09` 6/8 · `ch10` 7/7 · `ch11` 15/9 · `ch12` 11/10 ·
`ch13` 9/7 · `ch14` 13/8 · `ch15` 8/8 · `ch16` 6/7 · `ch17` 5/8 ·
`ch18` 9/10 · `ch19` 15/19 · `ch20` 13/10 · `ch21` 14/6 · `ch22` 24/21 ·
`ch23` 17/26 · `ch24` 19/14 —
no gap > 5 cm (ch11's worst is 3.64 cm after the 2026-08-25 rebuild; ch16 one 4.56 cm, ch18 gaps
of 4.93/4.56/4.55 cm and ch19 one 4.80 cm, see Open
items; ch20 has none above 4.0 cm, ch21 one 4.12 cm; **ch23 has none above 4.0 cm**;
ch03's worst is now 4.26 cm since চিত্র ৩.৩ was rebuilt; **ch24 has none above 3.52 cm**).

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
  ΔE lines — the standing layout fix. Chapters 16+ were **not** touched.

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
  figure's tail is excluded from *both* halves; and always credit the source in
  a `❖ চিত্রসূত্র` note box at the chapter's end (CC BY / CC BY-SA photos
  legally require it).
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
- ch19 ends on a header-only page 36 — the empty paragraph Word requires
  after the final ❖ চিত্রসূত্র box. ch13 already ships the same artefact.
  Harmless per chapter, and it disappears when the chapters are merged.
- Appendix ক (symbol chart) can reuse the four sheets from `dia_ch05.py`.
- Once all 28 chapters exist: merge into one file, continuous page numbers,
  single TOC + চিত্রসূচি + সারণিসূচি.

## Next step

**Chapter 25 — SDB ওয়্যারিং** (module lesson 25, ~16 pages).  The flat's own
board, i.e. the box at the *bottom* of ch24's chain: fed by one of the sixteen
40 A DP ways, 7200 W / 33 A, 10–25 mm² depending on the floor.  Ch22 already
picked every breaker inside it and ch23 every final-circuit cable, so ch25's
arithmetic is entirely spent — its job is the **board**: RCCB position, the
neutral-after-the-RCCB trap, SPD, way ordering, labelling.  `HW Connection
Diagram All.pptx` **s33** is the full flat SDB (RCCB + SPD + separate N and E
bars) and **s34/s35/s36** are three flat layouts fed from an SDB box; ch21 used
s33 once as its চিত্র ২১.১১, so check before re-cropping.  ch24's photo set
(`assets_ch24.py`) is an MDB, not an SDB — do not reuse it for the flat board.

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
