# Rebuilding the interior

The entry point is `../run.sh`, backed by `../../harness/run-container.sh`. Docker is the only host prerequisite. `../Dockerfile` records the shared recipe; the runner builds that same recipe from `../../harness/Dockerfile`, adding the exact packages declared in `../run.sh`. All document work runs without network access, with read-only input and a separate output mount. The checked package inventory is in `../output/packages.tsv`.

From the case directory:

```bash
./run.sh --input "/absolute/input directory" --output "/absolute/output directory"
```

The input directory contains `manuscript.md`, `print.json`, and any referenced local SVG files. Unknown descriptive JSON keys are ignored. An optional string `subtitle` can appear below the title; it is omitted when absent. The required keys are `schema_version` (1), `title` (nonempty string), `trim_width_mm`, `trim_height_mm`, `bleed_mm`, `margin_mm`, and `body_pt`. Width accepts 120–220 mm; height 180–300 mm; bleed 0–3 mm; margins 15–25 mm; body size 9–16 pt. Values must be finite numbers. Geometry must fit at least ten body ems between the side margins. MediaBox includes twice the bleed; TrimBox is inset by the bleed. This text interior has no art intended to reach the trimmed edge.

Supported Pandoc Markdown includes headings, paragraphs, emphasis, strong text, ordered and bullet lists, blockquotes, footnotes, Unicode, inline and fenced code, horizontal rules, local SVG illustrations with captions, fragment links and HTTP(S) text links. A level-one heading begins a chapter on a right-hand page. Front matter adds a title page and linked contents. Page numbering counts from the title page; title, contents and intentional blank pages do not display a folio. Body pages display their physical page number. A blank final verso is appended when necessary to make the total page count even. Running heads alternate book and chapter titles and are suppressed on chapter openings. Page-bottom notes preserve the manuscript text; note calls are sequential.

Only local, self-contained SVG images are accepted. Symlinks, external images, SVG scripts/resource references, raw HTML, tables, math and manuscript metadata are rejected with a diagnostic. Put the title in `print.json`. Long unbreakable text, oversized headings, or unsupported glyphs may fail the post-layout checks and need editorial adjustment. Replacement manuscripts need a new visual review; the shipped review does not certify other material.

The typesetter uses DejaVu Serif and DejaVu Sans explicitly. `SOURCE_DATE_EPOCH=0` fixes the embedded font subsets’ modification timestamps for repeatable PDF bytes. The source-view PDF uses DejaVu Sans Mono. All are embedded and licensed under the retained DejaVu/Bitstream terms. `licenses/fonts-dejavu.txt` is copied from the installed package. Body text uses the requested point size; footnotes use 78% of it. Running heads, folios and footnotes remain within the requested trim-safe margins. The body area reserves extra vertical room for running heads and folios. Widows and orphans have a minimum of three lines; chapter breaks and figure groups are intentional.

To inspect existing files without rebuilding or converting:

```bash
./run.sh --check --input "/absolute/input directory" --output "/absolute/output directory"
```

The image must already exist from a normal run. The checker reparses the manuscript and reads the shipped PDF directly, rather than trusting report flags. Single-column PDF lines are ordered by their measured position. Text matching uses Unicode NFKC, removes whitespace and soft hyphens, and matches generated footnote-call digits only at their source positions. Notes are checked separately because PDF reading order places them at page bottoms. The source map records each retained block and its physical starting page. Image resolution is reported as vector, with raster resources checked separately. Content matching does not substitute for visual inspection.

A clean output run emits `interior.pdf`, `before.pdf`, `layout.html`, `source-map.json`, `geometry.json`, `report.json`, `runtime.json`, `claims.json`, the package inventory, all-page renders, selected detailed renders, a contact sheet, before/after figures, and offline case-page screenshots. The reports contain no machine names or home paths. Only the selected output directory is writable during a normal run; copies of media and proof are kept separately.

The page screenshots use the shared harness unchanged. They show a local GitHub file-view approximation with its chrome and the Pages layout, not a live published capture. The Pages layout carries the public analytics snippet; no network request occurs during the run.
