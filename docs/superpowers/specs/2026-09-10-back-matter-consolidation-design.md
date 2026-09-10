# Back-matter consolidation for the merged full book

**Date:** 2026-09-10
**Scope:** the merged full book only (`mkbook.py` output). Standalone
`Book/অধ্যায়-NN — ….docx` and the digest (`mkdigest.py`) are NOT changed.

## Goal

In the merged **ইলেকট্রিক্যাল হাউস ওয়্যারিং — সম্পূর্ণ বই**, every chapter's
পারিভাষিক শব্দ and অনুশীলনী move out of the chapter and into two consolidated
back-of-book sections after অধ্যায় ২৮. সারসংক্ষেপ stays with its chapter.

Plus: expand the পারিভাষিক শব্দ tables of chapters 11–28 to the ch1–10
standard (every transliterated technical/trade term + every
tool/device/instrument/equipment name the chapter uses, as
`English (Latin) · বাংলা · short gloss`), before the merge.

## Final merged structure

```
Cover  (own borderless section)
Imprint
সূচিপত্র
অধ্যায় ১ … অধ্যায় ২৮      body + সারসংক্ষেপ only
পরিভাষা                    28 chapter-wise glossary blocks
অনুশীলনী                   28 chapter-wise exercise blocks
```

## Part A — glossary expansion, ch11–28

- Edit `chNN.py` only (the `b.table(...)` under `b.h1("পারিভাষিক শব্দ", …)`).
- Keep every existing row. Add rows for each transliterated term and each
  named tool/device/instrument/equipment/material used in that chapter,
  ordered by first appearance. Format `["ইংরেজি পরিভাষা", "বাংলা অর্থ",
  "সংক্ষিপ্ত ব্যাখ্যা"]`, keeping the file's existing `widths` / `size`.
- Method per chapter: read `chNN.py`, list candidate terms from prose,
  tables, box titles, diagram captions and the existing MCQ/short-question
  text; write the expanded list; rebuild; `python layout.py "out/<file>" 4.5`;
  close any new gap > ~4.5 cm with the standard reorder playbook (summary
  table earlier → figure after the worked example → merge `steps=` lines →
  move a figure past the paragraph that explains it).
- `mathguard.py` must stay clean (no math is touched, but run it).
- Update the CLAUDE.md status table page counts + the Bangla handbook.

Chapters already at or near the standard (11–15 have 3-column ~18-row
tables) still get swept for missing device/tool names; 16–28 need the
larger pass.

## Part B — `mkbook.py` restructure

`chNN.py` and `bookkit.py` are untouched. All splitting is done in
`mkbook.py` at merge time.

### Splitting a chapter `.docx`

Each chapter body ends with three consecutive `Heading 1` paragraphs whose
text ends in `সারসংক্ষেপ`, `পারিভাষিক শব্দ`, `অনুশীলনী`. Every block is a
direct child of `<w:body>` (last child is `<w:sectPr>`). For chapter `n`
load three pruned `Document` copies of `out/অধ্যায়-NN — <title>.docx`:

- **core** — remove every body child from the `পারিভাষিক শব্দ` heading
  through the last non-`sectPr` child. Keep `<w:sectPr>`.
- **glossary** — keep only children from the `পারিভাষিক শব্দ` heading up to
  (not including) the `অনুশীলনী` heading, plus `<w:sectPr>`. Replace that
  first `Heading 1`'s text with `অধ্যায় NN — <title>`.
- **exercises** — keep only children from the `অনুশীলনী` heading to the end,
  plus `<w:sectPr>`. Replace that `Heading 1`'s text with
  `অধ্যায় NN — <title>`.

Heading match is on `p.style.name == "Heading 1"` and
`p.text.strip().endswith("পারিভাষিক শব্দ")` / `endswith("অনুশীলনী")`, with an
assert that exactly one of each is found per chapter.

Pruned glossary/exercise copies keep their (now unused) image relationships;
those blocks carry no images, so nothing needed is orphaned. `docxcompose`
merges rels on append as today.

### Compose order

```
front  (build_front)
for n in 1..28:  append core_n      + inject_chapter_start(_chNN) + section bookmarks
append  পরিভাষা divider  (pageBreakBefore, h1 "পরিভাষা", RaptiChapterTitle stamp, bookmark _partGloss)
for n in 1..28:  append glossary_n  + bookmark _gloss_NN on its heading
append  অনুশীলনী divider  (pageBreakBefore, h1 "অনুশীলনী", RaptiChapterTitle stamp, bookmark _partExer)
for n in 1..28:  append exercises_n + bookmark _exer_NN on its heading
```

The two divider pages each carry a `RaptiChapterTitle`-styled paragraph
(`পরিভাষা` / `অনুশীলনী`) so the STYLEREF running header stops trailing
"অধ্যায় ২৮" and shows the part name on those pages.

### সূচিপত্র (`build_front`)

- `chapter_sections(path)` now returns only the `Heading 1` paragraphs of
  the **core** — i.e. stop collecting at the `পারিভাষিক শব্দ` heading. So
  chapter sub-lines run `NN.1 … সারসংক্ষেপ` and no further.
- After the 28 chapter blocks, add two top-level সূচিপত্র entries:
  - `পরিভাষা` → `PAGEREF _partGloss`, then 28 indented sub-lines
    `অধ্যায় NN — <title>` → `PAGEREF _gloss_NN`.
  - `অনুশীলনী` → `PAGEREF _partExer`, then 28 sub-lines → `PAGEREF _exer_NN`.
- `bake_toc_numbers` regex already matches `_ch\d\d(_s\d+)?`; widen it to
  also match `_partGloss`, `_partExer`, `_gloss_\d\d`, `_exer_\d\d` so every
  new line's number is baked to static text too.

### Bookmarks / `inject_section_bookmarks`

Unchanged for the core (`_chNN_sK` on each core `Heading 1`). The glossary
and exercise fragments get a single bookmark each (`_gloss_NN` / `_exer_NN`)
wrapped on their relabelled `Heading 1` at append time.

## Verification

1. `mathguard.py chNN.py` clean for every edited chapter.
2. `layout.py` on every rebuilt standalone chapter — page counts recorded,
   no gap > ~4.5 cm left unaddressed.
3. `python mkbook.py --pdf` completes; assert:
   - composed doc has the cover section + body section (2 sections),
   - `document.xml` contains 0 `PAGEREF` and 0 `fldChar` after `bake:`,
   - `bake:` line reports all anchors resolved (28 chapters + core sections
     + 2 part anchors + 56 chapter sub-anchors),
   - no chapter core page ends with a stray fragment of a moved table
     (spot-check: each chapter tail ends on সারসংক্ষেপ).
4. Read merged PDF spot pages: a mid-book chapter tail, the পরিভাষা divider,
   one glossary block, the অনুশীলনী divider, one exercise block, the last
   page. Header STYLEREF tracks chapter names then `পরিভাষা` / `অনুশীলনী`.
5. Update CLAUDE.md (status table page counts; a new dated note describing
   the merged-book structure and the `mkbook.py` split) and the Bangla
   handbook.

## Out of scope

- Standalone per-chapter `.docx` and their preview PDFs (stay inline).
- The digest (`mkdigest.py`, `smNN.py`).
- Appendices, চিত্রসূচি/সারণিসূচি.
- Renumbering the leftover section numbers: a chapter simply ends at its
  সারসংক্ষেপ number (e.g. ১৬.১২) with no ১৬.১৩/১৬.১৪ — acceptable, no
  cross-references point at those.
