# Handwritten notes, typed without guesswork

**I turned a transcript I prepared from the page into editable notes, with the unclear word left marked as `[unclear]`, not guessed. The tool performs no handwriting recognition.**

The input is a page of digital pen strokes I made for this case, not a photo or scan of paper. I rendered the DOCX in LibreOffice; Microsoft Word was not run.

[![Typed by a person from a drawn page: the pen-stroke note says Move, an unresolved mark, shelf; the typed note says Move [unclear] shelf.](media/hero.png)](media/hero.png)

*Typed by a person from a drawn page.*

## What was wrong

- The notes needed a clear, editable version.
- An unresolved word could change the instruction.
- The typed text needed a route back to the original page.

## What I did

- I read the original digital pen-stroke page and prepared the reviewed transcript.
- I retained spelling, punctuation and the literal `[unclear]` marker.
- I laid out the heading, paragraph and bullet in an editable document.
- I checked the text and kept a page/block map with the reading decision.

## Proof and downloads

The [source crop and PDF crop](media/hero.png) above come from the [original page](input/page-01.png) and [rendered PDF](output/preview.pdf). These are original digital strokes, not a photograph of physical writing; the [editable strokes](source/pen-strokes.svg) and [authorship record](source/authorship.md) explain their origin.

The [report](output/report.json) records **1 source page, 3 text blocks and 1 unresolved token**, measured from JSON, DOCX XML and PDF text with Python 3.11.2, python-docx 0.8.11 and pypdf 5.1.0. This is a content-preservation check, not a handwriting accuracy score. Manual review time was not measured.

Downloads: [editable DOCX](https://github.com/Ardholt/doc-pipeline/raw/refs/heads/main/handwritten-notes/output/notes.docx) · [plain text](output/notes.txt) · [PDF preview](output/preview.pdf) · [full rendered page](output/preview.png).

Audit: [page/block map](output/mapping.json) · [uncertainty list](output/uncertainties.json) · [reviewed transcript](input/transcript.json) · [source manifest](input/pages.json) · [runtime](output/runtime.json) · [claim evidence](proof/claims.json).

LibreOffice 7.4.7.2 rendered the DOCX. Microsoft Word was not run. The command formats a reviewed transcript; it performs no handwriting recognition. A person prepares the transcript by reading the image before running it. Struck-out words are omitted and each omission must be recorded during review; this page has none.

## Try it yourself

Clone the repository and install Docker. From the clone root:

```bash
cd handwritten-notes && ./run.sh
```

Open `output/preview.pdf` or edit `output/notes.docx`. [Input format and replacement-directory options](source/usage.md) describe the supported boundaries.

## How it is tested

[![Tests](https://github.com/Ardholt/doc-pipeline/actions/workflows/checks.yml/badge.svg)](https://github.com/Ardholt/doc-pipeline/actions/workflows/checks.yml)

The checks compare actual DOCX text and styles, plain text, PDF text, source hashes, mapping and uncertainty entries. They reject missing/duplicate pages and blocks, unlisted uncertainty markers and a deliberately damaged DOCX value. To inspect existing output without rebuilding, run `./run.sh --check`.

[Phone and desktop page proofs](proof/visual-review.md) use local GitHub-style and Pages renders, not captures of the published pages; CI status comes from the badge above.

Fixed price in a written scope, sent within hours

Maintained by Genco Doganay, Ardholt · [All cases](../README.md) · [MIT licence](../LICENSE)
