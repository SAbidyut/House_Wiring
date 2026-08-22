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
| 15 | সুইচ বোর্ড | 21 | ✅ delivered |
| 16 | পাওয়ার ফর্মুলা ও ক্যালকুলেশন | 19 | ✅ delivered |
| 17 | বিদ্যুৎ বিল | 19 | ✅ delivered |
| 18 | মোটর | 26 | ✅ delivered |
| 19 | আইপিএস ও ইউপিএস | 36 | ✅ delivered |
| 20 | ফ্লোট সুইচ | 25 | ✅ delivered |
| 21 | বাসবার ও বাসবার ক্যালকুলেশন | 30 | ✅ delivered |
| 22 | সার্কিট ব্রেকার ও প্রতিরক্ষামূলক ডিভাইস | 28 | ✅ delivered |
| 23–28 | — | — | pending |

Built chapters — figures / tables / worst page-foot gap (all QC-clean):
`ch01` 14/12 · `ch02` 15/9 · `ch03` 9/6 · `ch04` 8/10 · `ch05` 7/6 · `ch06` 7/4 ·
`ch07` 10/9 · `ch08` 11/8 · `ch09` 6/8 · `ch10` 7/7 · `ch11` 15/9 · `ch12` 11/9 ·
`ch13` 9/7 · `ch14` 13/8 · `ch15` 8/8 · `ch16` 6/7 · `ch17` 5/8 ·
`ch18` 9/10 · `ch19` 15/19 · `ch20` 13/10 · `ch21` 14/6 · `ch22` 14/16 — no gap > 5 cm
(ch03 has two ~4.6–4.8 cm gaps, ch16 one 4.56 cm, ch18 gaps of
4.93/4.56/4.55 cm and ch19 one 4.80 cm, see Open items; ch20 has none
above 4.0 cm, ch21 one 4.12 cm, ch22 not checked — soffice missing in sandbox).

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

- ch03 p2 and p4 have ~4.6–4.8 cm page-foot gaps — acceptable, revisit only if
  the user objects. ch18 has three of the same size (4.93 / 4.56 / 4.55 cm)
  and ch19 one (4.80 cm on p5, where `d03_types` is too tall to follow
  §১৯.২.১); each is a `worked_example` or a figure that could not be pulled
  up further.
- ch19 ends on a header-only page 36 — the empty paragraph Word requires
  after the final ❖ চিত্রসূত্র box. ch13 already ships the same artefact.
  Harmless per chapter, and it disappears when the chapters are merged.
- Appendix ক (symbol chart) can reuse the four sheets from `dia_ch05.py`.
- Once all 28 chapters exist: merge into one file, continuous page numbers,
  single TOC + চিত্রসূচি + সারণিসূচি.

## Next step

**Chapter 23 — ক্যাবল ও ক্যাবল ক্যালকুলেশন** (module lesson 23, ~22 pages).
Scope: ক্যাবল পরিচিতি ও প্রকারভেদ · ক্যাবল ক্যালকুলেশন (ভোল্টেজ ড্রপ,
কারেন্ট ক্যাপাসিটি, BNBC). Sources: `SUPER STAR Cables Technical Catalog.pdf`,
`circuit breaker & cable calculation.docx` (cable part), `Electrical House
Wiring book.docx` cable photos. BNBC 1.3.9.3.8, 1.3.9.3.9 already verified.

**Chapter 22 delivered — notes (do not re-discover).**
Two source docx mined:
- `circuit breaker.docx` — 27 media: HRC fuse, glass cartridge, blade,
  kitkat, MCB 1P/2P/3P/4P CHNT C63, RCCB 4P 63A 30mA, MCCB Hager 160A,
  RCCB 2P, MCCB 100A, RCBO 2P/4P, SPD 2P/4P TOMZN TZG40-C. Table of B/C/D/K
  curves (3–5, 5–10, 10–20×In) and fuse vs breaker comparison.
- `Standard Markings on Circuit Breakers.docx` — 14 media: RCBO 1P+N,
  MCB marking C16 6000 3, RCCB NL1-63, MCCB 320A, AFDD NB4LE-AFD,
  MPCB NS2-25, RCBO NXBLE-40, Isolator NXHB-125, SPD NXU-I+II/F 12.5/385,
  ACB, VCB. Plus 26 tables explaining each marking.
- `circuit breaker & cable calculation.docx` — load chart (LED 10–20W,
  tube 20–40W, fan 100W, socket 300/1000/1500W) and example 12200W total
  → 58.94A (230V, cosφ 0.9) → 63A. Diversity factor formula.

IEC verified via web search:
  IEC 60898-1 MCB household, Icn 6000/10000, B/C/D [stoklink, tradeaiders]
  IEC 60947-2 MCCB industrial, Icu/Ics kA, 25/50/75/100% [haipart, viox, sincede]
  IEC 61008-1 RCCB trip times: 1×≤300ms, 2×≤150ms, 5×≤40ms, 0.5× no trip [stoklink, hager]
  IEC 61009-1 RCBO combined [viox]
  IEC 61643-11 SPD Type 1 Iimp 10/350, Type 2 In 8/20, Type 3 [trilpeak]

Ch22 arithmetic chain: 12200W → 58.94A → 73.67A design → 63A main, branches
10/16/20A. Cable coordination: 1.5RM 18A → 16A MCB, 2.5RM 24A → 20A MCB.
BNBC 1.3.9.3.8 (20% spare) and 1.3.9.3.9 (one spare per five) reused.

Diagrams: 14, QC 0 problems (Pillow fallback for measurement, dummy PNGs —
Chrome and soffice missing in sandbox, SVG is authoritative for Word).
`assets_ch22.py` writes `credits.json` that `ch22.py` reads for ❖ চিত্রসূত্র.

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
