# PYQ Exam Hall

A practice and mock-exam website for **GATE CSE / UGC NET** previous-year questions, organised by subject and subtopic.

- **2,136 questions** across 15 subjects and 356 subtopics
- **Practice mode** – tap an option and see right/wrong instantly, then reveal a step-by-step solution
- **Exam mode** – GATE-style console: countdown timer, colour-coded question palette, mark-for-review, clear response, save & next, negative marking (−1/3, −2/3)
- **Results** – score, accuracy, negative marks, per-subtopic breakdown, time per question and full answer review
- **Worked solutions for every question**, including corrected answers where the official key is wrong and answers for questions the key leaves as TBA

## Project layout

| Path | What it is |
|---|---|
| `site/index.html` | The whole web app (single file, no build step) |
| `site/index.json` | Question metadata: subject, subtopic, source exam, type, answer key |
| `site/sol/<subject>.json` | Compiled solutions, one file per subject |
| `site/q/<subtopic>.json` | Question images (generated, not committed – see below) |
| `solsrc/<subject>/*.txt` | Solution sources in Markdown + LaTeX |
| `scripts/` | PDF extraction, rendering and build pipeline |
| `tools/` | Small helpers used while solving (FD closures, schedule serialisability, …) |
| `tests/` | Playwright end-to-end tests |

## Building the question bank

The question images are rendered from the GATE Overflow PYQ PDF, which is not included in this repository. Put your copy at `pyq.pdf`, then:

```bash
pip install pymupdf pillow numpy
python3 scripts/clean_pdf.py pyq.pdf pyq_clean.pdf   # strip handwritten annotation layers
pdftotext -layout pyq.pdf pyq.txt
python3 scripts/extract.py pyq.pdf raw.json          # locate every question block
python3 scripts/meta.py                              # parse table of contents + answer keys
python3 scripts/render.py                            # crop each question to a WebP image
python3 scripts/build_data.py                        # write site/index.json and site/q/*.json
for s in $(seq 1 15); do python3 scripts/solbuild.py $s; done   # compile solutions
```

Then serve the `site/` folder (`python3 -m http.server -d site`) and open it in a browser.

## Solution format

Each file in `solsrc/<subject>/` holds blocks like:

```
=== 1.2.5
a: 12          (optional: answer for questions with no official key)
fix: B         (optional: corrected answer when the official key is wrong)
Markdown and $LaTeX$ explanation…
```

`scripts/check.py <subject>` cross-checks every solution's final answer against the key.

## Credits

Questions are from GATE and UGC NET papers as compiled by GATE Overflow. Solutions, site and tooling are original work.
