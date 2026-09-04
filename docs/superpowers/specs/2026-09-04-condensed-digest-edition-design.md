# সংক্ষিপ্ত সংস্করণ — Condensed 150-page edition — design

**Date:** 2026-09-04
**Status:** approved for planning
**Owner:** RAPTI course developer (reviews the built PDF)

---

## 1. Goal

Produce a **single ~150-page Bangla book** — a condensed "revision / important-topics"
edition of the delivered *ইলেকট্রিক্যাল হাউস ওয়্যারিং* (762 pp, 28 chapters). It
must carry **every important fact, number, size, standard clause, key photograph and
safety-critical diagram** from the full book, with **more real photographs and fewer
drawn diagrams**, and **no MCQ and no অনুশীলনী / question sections at all**.

All content is drawn from the existing full book (`chNN.py` sources + the merged
`.docx`). Nothing in the full-book pipeline is modified.

## 2. Deliverable

`Book/ইলেকট্রিক্যাল হাউস ওয়্যারিং — সংক্ষিপ্ত সংস্করণ (গুরুত্বপূর্ণ বিষয়সমূহ).docx`
plus a `.pdf` preview, built by a new `mkdigest.py`. Target **145–152 printed pages**
including 3 pp of front matter.

## 3. Non-goals

- No new diagram artwork and no re-rendering. Assets are **reuse-only** from
  `Book/build/diagrams/chNN/` and `Book/build/assets/chNN/`. A figure whose art does
  not already exist is simply omitted.
- No changes to `ch01.py … ch28.py`, `dia_chNN.py`, `mkbook.py`, or any delivered
  full-book file.
- No appendices in v1.
- No MCQ, no অনুশীলনী (সংক্ষিপ্ত / রচনামূলক / ব্যবহারিক), no extra problem sets.

## 4. Architecture

Same three-stage pipeline, new content layer only.

| New file | Responsibility |
|---|---|
| `Book/build/sm01.py … sm28.py` | One condensed chapter each. Exports `build()` → `(path, Book)`. Writes `out/সংক্ষিপ্ত-NN — <title>.docx`. Uses `bookkit.Book` unchanged. Same chapter number, same title as the full book, so `চিত্র N.M` / `সারণি N.M` numbering stays consistent with the full book. |
| `Book/build/dia_digest_cover.py` | Clone of `dia_cover.py`; only the subtitle line changes to `সংক্ষিপ্ত সংস্করণ · গুরুত্বপূর্ণ বিষয়সমূহ`. Reuses the RAPTI logo asset already fetched by `assets_cover.py`. Output `diagrams/cover/cover_digest.svg` → `cover_digest.png`. |
| `Book/build/mkdigest.py` | Clone of `mkbook.py`. Globs `out/সংক্ষিপ্ত-*.docx`; `DEST` = the deliverable above; digest cover PNG; imprint "বইটি সম্পর্কে" / `kv` copy says **সংক্ষিপ্ত সংস্করণ** and notes it is a revision companion to the full 28-chapter book; same clickable সূচিপত্র + book-wide footer machinery, unchanged. |

`bookkit.py`, `svgkit.py`, `layout.py`, `mathguard.py`, `render.py` are used as-is.

### Content source per chapter

For each chapter I read `Book/build/chNN.py` and the chapter's section of the merged
PDF, then hand-select. The CLAUDE.md per-chapter "sources and decisions" notes define
what the spine of each chapter is; the condensed chapter keeps that spine and drops
the elaboration.

## 5. Condensed-chapter template

```
Book(NN, "<full title>", "<short subtitle>")
b.build_header_footer()
b.chapter_opener(objectives=[3–4 trimmed], intro=[1–2 short paragraphs])

  2–5 × h1 section:
     tight prose (pulled from full book, trimmed, humanised)
     ≤ 1 table per chapter (only the load-bearing one)
     1–3 figures per chapter — real photo preferred; a drawn diagram only when
        it is a connection/circuit diagram, a symbol chart, or safety-critical

  (calc chapters only) exactly 1 b.worked_example(...)

b.box("note", "<4–6 line bulleted সারসংক্ষেপ>", title="◆  সারসংক্ষেপ")
b.table(["বাংলা", "English"], [...], caption="পারিভাষিক শব্দ", size=Pt(9.5))
b.save(...)
```

Voice: formal Bangla per CLAUDE.md; imperatives নৈর্ব্যক্তিক; objectives end with a
natural mix (not every line on "সক্ষম হবে"); a `bangla-technical-humanizer` pass over
the prose I write. Diagram-internal text rules do not apply (no new diagrams).

Numerals: Bangla in prose, Latin in equations and where the digit *is* an identity
(cable size, gauge, voltage grade, angle) per the ch23/ch27 rule.

Cross-references: keep only "অধ্যায় NN দ্রষ্টব্য" style; drop page-specific ones.

## 6. Per-chapter page budget and spine

Front matter (cover + imprint + সূচিপত্র) = 3 pp. Chapters ≈ 146 pp.

| Ch | pp | Kept spine (condensed) | Worked ex. |
|---|---|---|---|
| 01 নিরাপত্তা | 6 | PPE on the body part it protects, electric-shock first aid / CPR airway path, lock-out, fire class, safe isolation. Photo-led. | – |
| 02 টুলস | 6 | Hand + power tool identification (photos/labels outside image), insulated-tool markings (1000 V, IEC 60900), wire-stripper plan view. | – |
| 03 বেসিক সার্কিট | 4 | Circuit elements 1–5, holder types (photos: BC/ES, batten/pendant/angle), short path vs load. | – |
| 04 ইলেকট্রিসিটি | 4 | Charge/current/voltage/resistance, AC vs DC, conductor/insulator, `বিল`/`টাকা` note. | – |
| 05 পদার্থ ও প্রতীক | 4 | Conductor/insulator/semiconductor; **symbol chart** (reuse `dia_ch05` sheets, ~1.5 pp). | – |
| 06 বেল সার্কিট | 3 | Trembling-bell mechanism (photo `DoorBell 001`), single-stroke bell, 2-place, series, emergency alarm = 2 sw + 2 bells parallel. | – |
| 07 সিরিজ/প্যারালাল/মিশ্র | 5 | Series vs parallel behaviour, R_T formulas (`b.math`), where each is used in a house. | – |
| 08 মেজারিং ইন্সট্রুমেন্টস | 5 | Ammeter/voltmeter/multimeter/megger/clamp; how to connect each; meter-face callouts. | – |
| 09 মাল্টিপ্লাগ | 3 | 2-pin/3-pin, piano board (holes stacked, shutter), earth pin longest. | – |
| 10 সিরিজ বোর্ড | 4 | Test/series board build, open vs short vs normal (device-in-return-leg figure). | – |
| 11 জয়েন্ট/সোল্ডারিং | 5 | Skinning, Western Union, tap, married, Britannia, pigtail (real photos `ph_pig_real`/`ph_pig_nut`), soldering + flux, taping. | – |
| 12 ফ্যান/রেগুলেটর | 5 | Outer-rotor ceiling-fan motor, run capacitor (grey can 2.5 µF 350 V), electronic vs resistive regulator, C/R/S leads. | – |
| 13 টু/থ্রি-ওয়ে সুইচ | 4 | Two-way A→C/B→D vs A→D/B→C, staircase wiring, wire count on the run (সারণি ১৩.৪). | – |
| 14 হাউস ওয়্যারিং লে-আউট/এস্টিমেট | 7 | Cleat/batten/casing/conduit methods, loop-in, layout symbols, load calc + material estimate. | ✔ load & estimate |
| 15 সুইচ বোর্ড | 4 | Board layout, piano/gang board (photos), circuit-diagram vs connection-diagram panels. | – |
| 16 পাওয়ার ফর্মুলা | 4 | P = VI cos φ, kVA/kW/kVAR, power factor, √3 for 3-phase (`b.math`, `\sqrt`). | ✔ 3-phase current |
| 17 বিদ্যুৎ বিল | 4 | Unit = kWh, BERC slab tariff (সারণি ১৭.৩ — dated note), demand charge, VAT, LPS. | ✔ monthly bill |
| 18 মোটর | 6 | 1-φ induction motor, start/run cap, star vs delta terminal block (photos), FLC, DOL. | – |
| 19 IPS/UPS | 6 | IPS vs UPS vs inverter, PF 0.6 on the VA plate, battery AH sizing (DoD/η), backup-time table. | ✔ battery AH |
| 20 ফ্লোট সুইচ | 4 | Cable float open/on photos, drain vs fill logic (com–NO / com–NC), contactor above FLC. | – |
| 21 বাসবার | 6 | Cu/Al current density (1.6 / 1.0), W×T×L, size table, spare capacity, BNBC colour code. | ✔ bar size |
| 22 সার্কিট ব্রেকার | 8 | Fuse/MCB/MCCB/RCCB/RCBO/SPD; **nameplate-reading** face crops + marking tables; B/C/D curves; device gallery photos; RCCB 30 mA rule (IEC 60364-4-41, no BNBC clause). | ✔ IB → breaker → Isc |
| 23 ক্যাবল | 8 | Type designation (BYA/BYFY…), IEC 60364-5-52 ampacity + derating, mV/A/m voltage drop, SWG/AWG, imperial vs metric market sizes. | ✔ size + drop |
| 24 MDB ওয়্যারিং | 6 | Distribution chain pole→MDB, SLD, diversity 0.7, 4-pole MCCB, riser voltage-drop table, ⚠ no-earth-in-source-slide note. | ✔ feeder / SLD |
| 25 SDB ওয়্যারিং | 6 | Flat SDB build (photo sequence), ways vs modules vs devices, neutral bar, SPD before RCCB, 30 % standing-leakage rule. | ✔ modules / leakage |
| 26 কন্ডুইট পাইপ | 6 | IS 9537 marking (photo `d25_mark`), 35 % fill, IET bent-run factor tables, one-bend = double length, 16 SWG GI, separate ECC. | ✔ conduit size |
| 27 চ্যানেল ওয়্যারিং | 5 | BNBC 1.3.14.1.2 (channels = extension work only) vs BD market; 45 % fill; corner fittings in plan; slide-35 room run photo; marking photo. | – |
| 28 আর্থিং ও টেস্ট | 8 | Earthing vs grounding, green+yellow, rod/pipe/plate resistance (computed), earth-lead & ECC sizing, IEC 60364-6 test sequence, IR 500/1000 V & 5 MΩ, 62 % rule, line-tester "lies" photo. | ✔ earth resistance |

Budgets are targets; ±1 pp per chapter is fine as long as the total stays ≈150.

## 7. Verification

1. `python mathguard.py smNN.py` for every chapter that calls `b.math` / `worked_example`.
2. `python smNN.py` builds clean for all 28.
3. `python layout.py "out/সংক্ষিপ্ত-NN … .docx" 6.0` — a digest tolerates larger
   page-foot gaps than the full book; only fix gaps > ~7 cm, by reordering.
4. `python dia_digest_cover.py && python render.py 'diagrams/cover/cover_digest.svg'`.
5. `python mkdigest.py --pdf`.
6. Read the full merged PDF page by page. Confirm page count 145–152, no MCQ/অনুশীলনী
   anywhere, সূচিপত্র links resolve, every chapter has its সারসংক্ষেপ + term table.
7. Deliver the `.docx` + `.pdf`; do not commit the merged `.docx` (size); the `.pdf`
   preview and all `smNN.py` / `mkdigest.py` / `dia_digest_cover.py` sources are
   committed after the user approves.

## 8. Risks

- **Page count drift.** 28 hand-trimmed chapters can overshoot. Mitigation: build in
  chapter-number order, run a running page tally after every ~5 chapters, tighten
  earlier chapters if the trend projects past 155.
- **"Important" is a judgement call.** The per-chapter spine table above is the
  contract; the user's PDF review is the backstop. A wrong call is a prose edit in one
  `smNN.py`, cheap to fix.
- **Asset gaps.** Some full-book figures are drawn inline with no standalone PNG.
  Those are dropped, not recreated. If a chapter loses too much by this, it gets a
  photo from that chapter's `assets/` instead.
- **Cover confusion.** Distinct subtitle on `cover_digest` + distinct filename keep
  the two books apart.

## 9. Out of scope / future

Appendices (symbol chart, cable/breaker tables, glossary, formula sheet), a
section-level TOC, and চিত্রসূচি/সারণিসূচি — same backlog as the full book, not part
of this deliverable.
