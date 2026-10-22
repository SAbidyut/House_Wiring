# Slide pipeline — RAPTI "ইলেকট্রিক্যাল হাউস ওয়্যারিং"

Classroom PowerPoint decks built from the book's own content, diagrams and
photos, plus verified YouTube videos.  One spec file per chapter
(`deck_chNN.py`) produces **two** outputs:

* `Slides/অধ্যায়ভিত্তিক স্লাইড/অধ্যায়-NN — <title>.pptx` — the full chapter deck
* `Slides/ইলেকট্রিক্যাল হাউস ওয়্যারিং — সংক্ষিপ্ত স্লাইড (অধ্যায় ১–২৮).pptx` — the merged
  brief deck (each chapter's cover, its `brief=True` slides, first video, summary)

## Setup (fresh container)

```bash
pip install python-pptx pillow lxml matplotlib qrcode pymupdf fonttools
cp Book/Kalpurush.ttf /usr/local/share/fonts/ && fc-cache -f      # LibreOffice previews
export CHROME_BIN=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
python3 render_all.py                 # book SVGs → .cache/diagrams/chNN/*.png (2x)
python3 render_all.py "cover/*.svg"   # book cover art (brief deck cover)
```

## Commands (run from `Slides/build/`)

```bash
python3 build.py 5 --pdf              # chapter 5 deck (+ preview PDF in .cache/pdf/)
python3 build.py all                  # every chapter that has a deck_chNN.py
python3 build.py brief --pdf          # merged brief deck
python3 sheets.py ".cache/pdf/<deck>.pdf" .cache/qa/ch05_   # 3×3 contact sheets for visual QA
```

The build prints `WARN …` for every text block the measurer thinks will not
fit, a title that wraps, a missing icon or image.  **Ship with zero warnings.**

## Files

| File | Role |
|---|---|
| `slidekit.py` | The engine: theme, frames, every slide type, Bangla text measurement (PIL + raqm, Kalpurush), image prep, math (matplotlib mathtext), QR, YouTube thumbnails |
| `build.py` | Chapter titles, output paths, `build.py N` / `all` / `brief` |
| `mkbrief.py` | The merged brief deck: cover, how-to, clickable contents, chapter sections, closing |
| `deck_chNN.py` | Chapter NN's slides — `def build(d): …` |
| `videos.json` | Verified videos per chapter (`"1": [ {id, lang, title, channel, duration, views, why, rapti?}, … ]`) |
| `ytsearch.py` | YouTube search helper used to pick the videos |
| `render_all.py` | Renders `Book/build/diagrams/**/*.svg` to `.cache/diagrams/` |
| `icons/` | `<name>_{white,navy,copper}.png` (Font Awesome 6, rendered) |
| `.cache/` | Regenerable: diagram PNGs, prepped images, math, QR, thumbnails, PDFs (gitignored) |

## Writing a chapter deck

`deck_ch01.py` is the reference — read it first.  `build.py` has already
called `d.chapter(n, title, …)`, so a deck file only adds slides:

```python
from slidekit import P

def build(d):
    D, A = d.D, d.A                       # image key helpers
    d.cover(hero=D("d05_ppe"), subtitle="…")
    d.objectives([...])
    ...
    d.videos()                            # this chapter's videos from videos.json
    d.quiz([...]); d.glossary([...]); d.summary([...]); d.closing()
```

### Images

* `D("d07_five_rules")` → this chapter's book diagram (`.cache/diagrams/chNN/d07_five_rules.png`)
* `D("d07_face", ch=22)` → another chapter's diagram
* `A("ppe_helmet.jpg")` → `Book/build/assets/chNN/ppe_helmet.jpg` (photos)
* `A("hwbook/ceil_rose.jpg")` → any other folder under `Book/build/assets/`

White margins are trimmed automatically.  Diagrams sit on a white rounded
card; JPEG photos get rounded corners.  Very wide images (aspect ≥ ~1.9) are
placed *under* the content automatically instead of beside it.

### Text

* `**bold**` inside any string (rendered navy / accent).
* Glyphs Kalpurush lacks (Ω ° ² √ π φ ≈ Δ µ ± → ✓ ₂ …) and `÷` are switched to Arial
  automatically — write them freely in text, never inside a Bangla word.
* Prose numerals Bangla (`২৩০ V`), maths Latin.

### Slide types (all take `notes="teacher notes"`, most take `brief=True`, `tag=`)

| Call | Use |
|---|---|
| `cover(hero=img, subtitle=…)` | Dark chapter cover; in the brief deck it is the chapter divider |
| `objectives([str…])` | 4–8 numbered learning outcomes |
| `agenda([(num, title)…])` | Roadmap tiles of the chapter's sections |
| `section(num, title, sub=)` | Dark divider (use sparingly, only for very long chapters) |
| `bullets(title, items, img=, caption=, side="right", layout="stack"\|"side", pt=21)` | Text + picture.  `items`: `"text"` or `("text", ["sub", …])` |
| `rows(title, [(icon, head, body)…], img=)` | Icon rows (3–5) |
| `cards(title, [dict(icon=\|num=, head=, body=, color=, tint=)…], cols=, img=)` | 2–8 cards in a grid |
| `steps(title, [(head, body)…], img=)` | Process: horizontal (≤5, no image) or vertical with image |
| `table(title, header, rows, widths=, note=, img=, hl_col=)` | Native table; ≤ 8 rows, ≤ 4 columns |
| `formula(title, tex, legend=[(sym_tex, meaning)…], extra=[tex…], note=, img=)` | Display formula + symbol legend |
| `example(title, question, given=[…], find=[…], steps=[tex…], answer=, note=)` | Worked example: প্রশ্ন / প্রদত্ত / নির্ণেয় left, maths steps right |
| `callout(title, text, kind=, label=, points=, img=)` | Big rule/safety box.  `kind`: danger, warning, tip, note, rule, info |
| `compare(title, dict(head, items, kind="good"), dict(head, items, kind="bad"))` | Do / don't, A vs B |
| `stats(title, [(value, label)…], note=)` | 2–4 big numbers |
| `image(title, img, caption=, points=[…], note=)` | One large figure (+ short points beside or under it) |
| `gallery(title, [(img, label)…], cols=)` | Photo grid, 3–8 items |
| `videos()` / `video(id, why=[…])` | YouTube card: clickable thumbnail + QR + details |
| `quiz([(q, [o1, o2, o3, o4], answer_index)…])` | Question slide(s) + answer-reveal slide(s) |
| `glossary([(bn, en)…])` | 8–14 terms in two tables |
| `summary([str…])` | Dark "মূল কথা" slide (always in the brief deck) |
| `closing()` | Dark Q&A / next-chapter / contact slide (full decks only) |

Maths (`tex`, `steps`, legend symbols) is matplotlib mathtext — `\frac{}{}`,
`\sqrt{}`, `^{}`, `_{}`, `\times`, `\cos\phi`, `\Omega`, `\approx`, `\Delta`,
`\mathrm{A}`, `\ ` (space).  **No Bangla inside maths.**

Icons: `bolt helmet fire extinguisher firstaid warning plug bulb fan calculator
play youtube tools gauge target house toggle ruler money droplet check cross
book list battery gears shield search student building sun heat link bell
branch layers clock wrench hammer lock tag pointer teacher fall heart idea
question info stop recycle cable chart table eye hand water motor pump globe
ground compass clipboard box key star flag people microscope atom magnet wave
phone map pen screwdriver paint bolt2 quiz glossary summary video shock plugx
plugcheck server solar snow arrows`.

## Design (do not drift)

Palette from the book cover: navy `0A2440` (dominant), gold `C8A64B`
(accent), ice `EDF3F9` (cards); red/green/amber only for danger/good/warning.
Dark slides = cover, summary, closing; everything else white.  Titles 32 pt
navy, body 18–22 pt, nothing under 12 pt.  Kalpurush throughout (the user's
PowerPoint needs it installed — it ships in `Book/`).
