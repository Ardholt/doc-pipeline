# Reproduction and input boundaries

`../harness/run-container.sh` supplies argument handling, separate mounts, resource limits, network isolation and a fresh LibreOffice profile. `source/container.env` adds the pinned English OCR and text-document packages to `../harness/Dockerfile`. Only Git and Docker are required on the host. A cold build downloads the declared dependencies; conversion runs with no network. Setup and workload deadlines total less than the CI job limit.

From the case directory:

```bash
./run.sh --input "/absolute/input directory" --output "/absolute/output directory"
```

Input is mounted read-only. Output must be separate. The directory must contain an unencrypted `scan.pdf` of clear English page images without a text layer. Between 1 and 500 pages are supported. Headings, paragraphs and tables whose columns are separated by visible whitespace are supported. No merged cells, handwriting, complex forms or multicolumn reading-order guarantee. Blank/unreadable pages fail with a diagnostic rather than disappearing.

An optional UTF-8 `review.csv` has exactly `page,find,replace,reason` columns. Page numbers are one-based. Each row replaces exactly one literal occurrence on that page, after previous rows have run. Zero or multiple matches fail. CSV quoting follows standard rules. Review does not use regular expressions. Retained TSV and raw text are written before review. Corrections are replayable in `corrections.json`; confidence flags are in `pages.json`. A review that leaves a nonrectangular table is rejected.

For a replacement scan, the DOCX and source map are checked against retained extraction. An accuracy percentage is available only when the scan SHA-256 matches the independently authored public corpus. The scorer runs after document construction, never modifies the document, and verifies the reference hash. A different input cannot select an answer by filename.

Inspect existing output without rebuilding or converting:

```bash
./run.sh --check --input "/absolute/input directory" --output "/absolute/output directory"
```

To reproduce the corpus in a new directory:

```bash
./make-input.sh --output "/absolute/new corpus directory"
```

The frozen `source/reference.json` was authored before OCR. `source/author.py` retains its composition recipe; `source/generate.py` draws the text with the bundled DejaVu Sans Mono face, adds paper grain, small position/ink variation and page skew, then places only raster images in the PDF. The generated manifest records text, image, reference and scan hashes. It is not read by OCR or document construction. To install a regenerated corpus, copy its `scan.pdf` to `input/` and its `corpus-manifest.json` to `source/` before the next normal run. Source PNGs are inspection aids, not conversion inputs.

The accuracy calculation is exact Levenshtein edit distance per source page, summed over the reference. It collapses whitespace, but preserves case, punctuation and digits. Characters include normalized spaces; words are whitespace-delimited tokens. Insertions, deletions and substitutions each cost one. The same comparison is made against raw OCR, final mapped text and the actual DOCX XML. This is measured recognition accuracy on the authored corpus, not a claim of manual proofreading.

`output/report.json` records tools, transformations, counts, input/output hashes, checks and limits. `runtime.json` measures the container workload only. `output/packages.tsv` records resolved dependencies. Screenshots use the shared offline GitHub frame, not an authenticated capture of the public website. Page renders are made from the cleaned LibreOffice PDF. No Microsoft Word application run is claimed.
