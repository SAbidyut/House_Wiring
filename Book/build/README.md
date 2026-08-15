# Book engine — API reference

One page. Enough to write a whole chapter without opening `bookkit.py`.
Conventions and constraints live in `../../CLAUDE.md`; chapter plan in `BOOK_INDEX.md`.

---

## Build a chapter

```python
# chNN.py
import os, json
from docx.shared import Pt
from bookkit import Book, bn, NAVY, RED, GREEN, STEEL, GREY, INK

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "diagrams", "chNN")     # rendered PNG/SVG pairs
A = os.path.join(HERE, "assets", "chNN")       # real photographs

W = {"d01": 15.4, "d02": 15.2}                 # figure widths in cm

def build():
    b = Book(4, "অধ্যায়ের শিরোনাম", "উপশিরোনাম · কমা দিয়ে · আলাদা")
    b.build_header_footer()
    b.chapter_opener(objectives=[...], intro=["অনুচ্ছেদ ১", "অনুচ্ছেদ ২"])
    ...
    path = os.path.join(OUT, "অধ্যায়-০৪ — শিরোনাম.docx")
    b.save(path)
    return path, b

if __name__ == "__main__":
    p, b = build()
    print("saved:", p, b.fig_n, b.tab_n)
```

Run order: `dia_chNN.py` → `render.py` → `qc.py` → `chNN.py` → `layout.py`.

---

## Text

| Call | Notes |
|---|---|
| `b.h1(text, num="৪.১")` | Section. Navy, rule under it. |
| `b.h2(text, num="৪.১.১")` · `b.h3` · `b.h4(text)` | Sub-levels. `h4` takes no number. |
| `b.para(text, align="justify", size=BODY_SIZE, color=INK, indent=0, space_before=0, space_after=6)` | Body paragraph. `align`: `justify\|left\|center\|right`. |
| `b.bullets([...], tight=False)` | `•` list. |
| `b.numbered([...], start=1, tight=False)` | Bangla-numeral list. |
| `b.spacer(pts)` · `b.rule()` · `b.page_break()` | Spacing helpers. |

**Inline markup** works in every text argument:
`**bold**`, `*italic*`, `` `mono` ``, `__red bold__`.

`bn(4)` → `৪` — convert any number/string to Bangla numerals.

---

## Callout boxes

```python
b.box("safety", "শরীরের কথা…", items=["ঐচ্ছিক", "বুলেট"], title=None)
```

| `kind` | Default title | Use for |
|---|---|---|
| `safety` | ⚠ নিরাপত্তা সতর্কতা | anything that can hurt someone |
| `note` | ❖ মনে রাখুন | a fact worth remembering |
| `tip` | ✔ ব্যবহারিক পরামর্শ | field advice |
| `def` | 📘 সংজ্ঞা | definitions (pass `title="📘  সংজ্ঞা — X"`) |
| `formula` | ∑ সূত্র | formula call-outs |

`body` splits on `\n` into separate paragraphs — never leave a soft break inside
one, justification stretches the last line.

---

## Figures

```python
b.figure(f"{D}/d01_name.png", "ক্যাপশন", width_cm=W["d01"])
```

- Pass the **`.png`**; a sibling `.svg` is embedded automatically as the vector,
  with the PNG as fallback. Word's *Convert to Shape* then works.
- Auto-numbers `চিত্র N.M` and records it in `b.figures`.

```python
b.figure_row([(path, "লেবেল"), ...], per_row=3, caption="…")
```
Grid of photographs with captions under each — for real product photos.

---

## Tables

```python
b.table(headers, rows, caption="…",
        widths=[3, 4, 3],                  # relative column widths
        align=["left", "center", "left"],  # per column
        size=Pt(10))                       # shrink for dense tables
```
Auto-numbers `সারণি N.M`, repeats the header row across pages, never splits a
row. Body cells accept the same inline markup as `para`.

---

## Mathematics

```python
b.math(r"V = I \times R")
b.math(r"I = \frac{V}{R}")
```

DSL: `\frac{a}{b}` real fraction · `^{x}` superscript · `_{x}` subscript
(always brace it — `R_{T}`, `V_{AB}`) · `` `text` `` upright
(units, Bangla words) · commands `\times \cdot \approx \pm \leq \geq \rho \mu
\Omega \pi \Delta \to \quad \qquad`. Bare Latin letters come out italic, as
variables should.

```python
b.worked_example(
    1, "প্রশ্নের বাক্য …",
    given=["V = 230 `V`", "R = 460 `Ω`"],
    find=["I = ?"],
    steps=[r"I = \frac{V}{R}", r"= \frac{230}{460}", r"= 0.5 `A`"],
    answer="বাতিটির মধ্য দিয়ে 0.5 A কারেন্ট প্রবাহিত হবে।",
    note="ঐচ্ছিক টীকা")
```
Renders the প্রদত্ত → নির্ণেয় → সমাধান → উত্তর block. **Latin numerals inside
equations** — Bengali digits break in OMML under LibreOffice.

`b.equation(expr, note=…)` is the old plain-text form; prefer `b.math`.

---

## Exercises

```python
b.mcq(1, "প্রশ্ন?", ["ক-অপশন", "খ", "গ", "ঘ"], cols=2)
```
Then close with an answer key:
```python
b.box("note", "**উত্তরমালা:** ১-খ, ২-গ, …", title="✔  উত্তরমালা")
```

---

## Word-native diagram blocks

Available but **not used** — the user wants diagrams as pictures.
Keep for tabular content only: `b.tree_cols(root, [(head, [items]), …])`,
`b.concept_cards([(title, sub, desc), …])`, `b.flow_steps([(title, desc), …])`.

---

## Drawing diagrams — `svgkit`

```python
from svgkit import SVG, NAVY, STEEL, RED, GREEN, AMBER, GREY, LINE, INK, wrap, tw
# also: LIGHT, REDBG, GREENBG, AMBERBG, PAPER

def d01_name():
    s = SVG(1240, 700)
    s.title("ডায়াগ্রামের শিরোনাম", 34)
    ar = s.arrow_defs(STEEL, "ar", 15)          # returns marker id
    s.rect(x, y, w, h, fill, stroke, sw, rx)
    s.line(x1, y1, x2, y2, stroke, sw, dash="8 5", marker=ar)
    s.path("M … L …", stroke, sw, fill, dash=, marker=)
    s.circle(cx, cy, r, fill, stroke, sw)
    s.poly([(x, y), …], fill, stroke, sw)
    s.text(x, y, "লেখা", size, fill, weight, anchor="start|middle|end")
    s.box_auto(cx, y, "লেখা", size, fill=, stroke=, tcolor=, max_w=)  # → (x,y,w,h)
    s.check(cx, cy, r) ; s.heart(cx, cy, r) ; s.badge(cx, cy, "১")
    s.clip_begin(x, y, w, h, rx) ; … ; s.clip_end()   # keep strokes inside a shape
    s.fit(bottom_y, pad)                              # trim canvas to content
    return s.save(f"{OUT}/d01_name.svg")

ALL = [d01_name, …]      # qc.py and __main__ read this
```

**Argument order traps** — these differ, and getting them wrong silently fills
a shape black:

| Method | Order |
|---|---|
| `rect` | `x, y, w, h, fill, stroke, sw, rx` |
| `circle` / `poly` / `ellipse` | `…, fill, stroke, sw` |
| `path` / `line` | `d, **stroke**, sw, **fill**` |

**Text measurement** — `tw(text, size, weight)` real width in px;
`wrap(text, max_w, size, weight)` → list of lines. Always size boxes from these,
never from character count (Bangla is a complex script).

**Type size** — a `W`-px canvas placed `P` cm wide renders `N`-px type at
`N × P(pt) / W` pt. Current scale: title 34, node 28, name 24.5, body 21.5,
small 20 on a ~1240-px canvas → ~7.5 pt at 15.4 cm. Do not go smaller.

Copy the `__main__` block from any `dia_chNN.py` — it runs a collect pass, one
batched Chrome measurement, then the real draw.

---

## Verification

```bash
python qc.py dia_ch05                  # must print "total problems: 0"
python layout.py "out/<file>.docx" 4.5 # page-foot gaps in cm
```

`qc.py` reports text×text overlap, text×graphic collisions and off-canvas text.
It checks geometry only — **still look at every rendered PNG** to see whether the
drawing actually reads correctly.
