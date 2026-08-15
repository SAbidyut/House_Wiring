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
| 03 | বেসিক ইলেকট্রিক্যাল সার্কিট (১–৫) | 15 | ✅ delivered |
| 04 | ইলেকট্রিসিটি বা বিদ্যুৎ | 18 | ✅ delivered |
| 05 | পদার্থের প্রকারভেদ ও ইলেকট্রিক্যাল প্রতীক | 14 | ✅ delivered |
| 06 | বেল সার্কিট (৬–৯) | 13 | ✅ delivered |
| 07 | ইলেকট্রিক্যাল সার্কিট (সিরিজ/প্যারালাল/মিশ্র) | 24 | ✅ delivered |
| 08 | মেজারিং ইন্সট্রুমেন্টস | 20 | ✅ delivered |
| 09 | মাল্টিপ্লাগ সার্কিট | 17 | ✅ delivered |
| 10 | সিরিজ বোর্ড | 17 | ✅ delivered |
| 11 | জয়েন্ট, স্প্লাইস ও সোল্ডারিং | 24 | ✅ delivered |
| 12 | ফ্যান ও ফ্যান রেগুলেটর | 22 | ✅ delivered |
| 13 | টু-ওয়ে ও থ্রি-ওয়ে সুইচ | 19 | ✅ delivered |
| 14 | হাউস ওয়্যারিং: পদ্ধতি, লে-আউট ও এস্টিমেট | 29 | ✅ delivered |
| 15–28 | — | — | pending |

Built chapters — figures / tables / worst page-foot gap (all QC-clean):
`ch01` 14/12 · `ch02` 15/9 · `ch03` 9/6 · `ch04` 8/10 · `ch05` 7/6 · `ch06` 7/4 ·
`ch07` 10/9 · `ch08` 11/8 · `ch09` 6/8 · `ch10` 7/7 · `ch11` 15/9 · `ch12` 11/9 ·
`ch13` 9/7 · `ch14` 13/8 —
no gap > 5 cm (ch03 has two ~4.6–4.8 cm gaps, see Open items).

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
| `Earthing.docx`, `Motor.docx`, `circuit breaker*.docx`, `Busbar All.pptx`, `Measuring Instruments.docx`, `Solar System.docx`, `SUPER STAR Cables catalog.pdf` | Chapter-specific material for ch08, 18, 21, 22, 23, 28 + appendix |
| `HW Exam Question.docx`, `Electrical House Wiring Quistion.docx` | Question bank for the appendix |

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

## Drawing bugs that keep recurring

Check these before rendering — each one shipped once and had to be fixed:

- **`path()` argument order** is `(d, stroke, sw, fill)` but `rect()`/`circle()`/
  `poly()` are `(…, fill, stroke, sw)`. Passing `"none"` first to `path()`
  fills the shape solid black (broke the socket and bell symbols).
- **Wires must break where a component sits** — draw the loop as separate runs,
  not one rectangle with symbols laid on top (broke the plug, switch and lamp).
- **A stroke through a label** is a defect `qc.py` now catches; a *curve* through
  a label was missed until `_path_points` learned Q/C endpoints.
- Bengali `৪` renders like a Latin `8` in Kalpurush — that is correct, not a bug.
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

- ch03 p2 and p4 have ~4.6–4.8 cm page-foot gaps — acceptable, revisit only if
  the user objects.
- Appendix ক (symbol chart) can reuse the four sheets from `dia_ch05.py`.
- Once all 28 chapters exist: merge into one file, continuous page numbers,
  single TOC + চিত্রসূচি + সারণিসূচি.

## Next step

**Chapter 15 — সুইচ বোর্ড** (module lesson 15, ~16 pages). Scope in
`BOOK_INDEX.md`. Ch14 §14.6 already fixes the mounting heights (BNBC 1.3.11.5 —
1220 mm) and §14.6.3 the point-counting table; build on those instead of
restating them. `HW Connection Diagram All.pptx` has piano/gang switchboard
drawings (the two panels of ch14's চিত্র ১৪.৯ came from slides 34 and 36) —
check the deck for a board-only slide before hand-drawing.

Reusable: `assets_chNN.py` (ch12/ch13/ch14) converts a source PPTX to PDF once
into `.slidepdf/` and crops any slide at 300 dpi — point `SLIDES` at the new
slide numbers and it just works. Verify the slide number from the PDF page text
first; both decks have near-duplicate drawings a row apart.

Layout lesson from ch13: two `worked_example()` blocks back to back will not
share a page — Word pushes the second one whole, opening an ~11 cm gap. Put
each one in the section it topically belongs to instead of batching them.
Ch14 added the corollary: a worked example that is a page-and-a-bit long
strands a whole page. Merging its `steps=` onto fewer lines (`= 6460 W` on the
same line as the expression) shrank example ১৪.২ enough to fit, closing a
16.9 cm gap that no amount of reordering would.

BNBC Part 8 Chapter 1 — the authority for every wiring rule in this book — is
free at `law.resource.org/pub/bd/bnbc.2012/gov.bd.bnbc.2012.08.01.pdf`.
Extract it with pymupdf and grep the clause rather than trusting memory; ch14's
clause numbers (1.3.8.2.4, 1.3.9.3.1, 1.3.9.3.12, 1.3.11.5 …) were all verified
against it.
