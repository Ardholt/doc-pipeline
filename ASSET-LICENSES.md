# Asset licences

Original code, documents, inputs and generated outputs in this repository are by Genco Doganay and released under the [MIT licence](LICENSE). Every input document, image, drawing and text was newly authored for these cases. No client material, no photographs, no downloaded images and no handwriting typeface is included; the handwriting page is original pen strokes drawn as an SVG and rasterised.

Third-party material and what it is licensed under:

| Material | Where | Licence |
|---|---|---|
| DejaVu Sans, Sans Bold, Serif, Serif Bold/Italic and Sans Mono (Debian `fonts-dejavu-core` 2.37-6; one unmodified copy of DejaVu Sans Mono 2.37 in `retype-150-pages/source/`) | rendered into document text and embedded as subsets in PDFs; installed in the build image | Bitstream Vera licence; DejaVu changes are public domain. Notices: `*/licenses/`, `*/output/font-licen*`, `kindle-tappable-footnotes/source/licenses/dejavu.txt` |
| Inter Regular and SemiBold (unmodified) | `handwritten-notes/source/fonts/`; embedded as subsets in its PDF and drawn into its hero image | SIL Open Font Licence 1.1; notice `handwritten-notes/source/fonts/LICENSE-Inter.txt` |
| Liberation fonts (Debian `fonts-liberation`) | installed by the shared build image only; not used in any document | SIL OFL 1.1; notice `school-fillable-forms/output/font-licenses/` |
| github-markdown-css 5.8.1 | `harness/vendor/github-markdown.css`, used for the offline GitHub-style page previews | MIT; notice `harness/licenses/github-markdown-css.txt` |
| Debian packages and Python packages named in `toolchain/` | installed in Docker at build time; not redistributed here | each package's own licence, as shipped by Debian or PyPI |

Upstream licence notices keep the contact lines their licences require; none of those lines appears in any document, page or image of the cases.

Every tracked file is listed below with its provenance and licence. Derived outputs cite the inputs and code they come from.

| File | Source / provenance | Licence |
|---|---|---|
| `.github/workflows/checks.yml` | Original CI workflow | MIT |
| `LICENSE` | MIT licence for original code/content. | MIT |
| `README.md` | Original repository root file (tools/build-index comes from the Ardholt casebook page template) | MIT |
| `_config.yml` | Pages config, layout and styles from the Ardholt casebook page template, adapted for this repository | MIT |
| `_layouts/default.html` | Pages config, layout and styles from the Ardholt casebook page template, adapted for this repository | MIT |
| `assets/site.css` | Pages config, layout and styles from the Ardholt casebook page template, adapted for this repository | MIT |
| `cases.json` | Original repository root file (tools/build-index comes from the Ardholt casebook page template) | MIT |
| `data-to-powerpoint/Dockerfile` | Shared document harness recipe adapted with the declared presentation dependency pins | MIT; installed dependencies retain their own package licences |
| `data-to-powerpoint/LICENSE` | Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout | MIT |
| `data-to-powerpoint/README.md` | Genco Doganay's case text using the shared case-page structure | MIT |
| `data-to-powerpoint/input/data.csv` | Newly authored anonymous department figures, Genco Doganay | MIT |
| `data-to-powerpoint/input/deck.json` | Newly authored neutral title, department order and colour settings, Genco Doganay | MIT |
| `data-to-powerpoint/media/hero.png` | Byte-identical copy of generated hero after visual review | MIT |
| `data-to-powerpoint/output/acceptance.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/acceptance.log` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/arguments.log` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/chart-detail.png` | Literal crop from the rendered profit slide, coordinates in `output/hero-map.json` | MIT |
| `data-to-powerpoint/output/check.log` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/claims.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/contact-sheet.png` | Montage of actual cleaned PDF slide renders | MIT |
| `data-to-powerpoint/output/deck.pdf` | LibreOffice rendering of cleaned PPTX, then PDF properties removed | MIT for content/layout; DejaVu font terms for embedded fonts |
| `data-to-powerpoint/output/deck.pptx` | Generated from the listed CSV and settings; editable text, charts and embedded numeric spreadsheets | MIT for content/layout |
| `data-to-powerpoint/output/font-inventory.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/font-licences/DejaVu.txt` | Verbatim Debian package copyright/licence notice | Original notices retained |
| `data-to-powerpoint/output/hero-map.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/hero.png` | Reformatted source cells beside an actual crop from the rendered profit slide | MIT |
| `data-to-powerpoint/output/image-identity.txt` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/packages.tsv` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/page-previews/github-1366.png` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/page-previews/github-390.png` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/page-previews/pages-1366.png` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/page-previews/pages-390.png` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/page-previews/screenshots.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/pdf-fonts.txt` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/regression.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/report.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/run.log` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/runtime.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/output/slides/slide-01.png` | Rendered title and summary slide | MIT |
| `data-to-powerpoint/output/slides/slide-02.png` | Rendered revenue overview | MIT |
| `data-to-powerpoint/output/slides/slide-03.png` | Rendered revenue/cost comparisons | MIT |
| `data-to-powerpoint/output/slides/slide-04.png` | Rendered profit trends | MIT |
| `data-to-powerpoint/output/slides/slide-05.png` | Rendered source and method notes | MIT |
| `data-to-powerpoint/output/source-map.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/acceptance.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/acceptance.log` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/arguments.log` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/asset-manifest.json` | Generated by the case pipeline from the inputs, or the measurement/review record; derived from the original inputs | MIT content; embedded or rendered font portions keep their font licences |
| `data-to-powerpoint/proof/check.log` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/claims.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/image-identity.txt` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/page-previews/github-1366.png` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/page-previews/github-390.png` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/page-previews/pages-1366.png` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/page-previews/pages-390.png` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/page-previews/screenshots.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/publication.json` | Generated by the case pipeline from the inputs, or the measurement/review record; derived from the original inputs | MIT content; embedded or rendered font portions keep their font licences |
| `data-to-powerpoint/proof/regression.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/report.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/run.log` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/runtime.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/proof/visual-review.json` | Generated from input/data.csv and input/deck.json by this pipeline, or recorded from checks of those outputs; page captures use the shared harness layout and vendored GitHub Markdown CSS | MIT for original content and layouts; DejaVu font terms apply to embedded font programs; shared GitHub Markdown CSS retains its MIT notice in harness/licenses/github-markdown-css.txt |
| `data-to-powerpoint/run.sh` | Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout | MIT |
| `data-to-powerpoint/source/USAGE.md` | Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout | MIT |
| `data-to-powerpoint/source/asset_manifest.py` | Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout | MIT |
| `data-to-powerpoint/source/data.py` | Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout | MIT |
| `data-to-powerpoint/source/fonts.conf` | Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout | MIT |
| `data-to-powerpoint/source/pipeline.py` | Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout | MIT |
| `data-to-powerpoint/tests/acceptance.py` | Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout | MIT |
| `data-to-powerpoint/tests/acceptance.sh` | Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout | MIT |
| `data-to-powerpoint/tests/check.py` | Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout | MIT |
| `data-to-powerpoint/tests/publication.py` | Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout | MIT |
| `data-to-powerpoint/tests/regression.py` | Original case text, implementation or verification code, Genco Doganay; README follows the shared case-page layout | MIT |
| `ebook-print-pdf/Dockerfile` | Copy of the shared harness/Dockerfile; optional groups selected in run.sh. | MIT |
| `ebook-print-pdf/LICENSE` | Original case code, documentation or licence by Genco Doganay; README follows the shared case-page layout. | MIT |
| `ebook-print-pdf/README.md` | Original case code, documentation or licence by Genco Doganay; README follows the shared case-page layout. | MIT |
| `ebook-print-pdf/input/manuscript.md` | Original prose, The Unhurried Notebook, written for this case by Genco Doganay. | MIT |
| `ebook-print-pdf/input/notebook.svg` | Original vector drawing, composed from paths, shapes and text; no imported artwork. | MIT |
| `ebook-print-pdf/input/print.json` | Original public print settings. | MIT |
| `ebook-print-pdf/licenses/fonts-dejavu.txt` | Copyright and permission notice from Debian fonts-dejavu-core 2.37-6; packaging metadata and the optional contact sentence omitted; copyright, trademark and permission conditions retained. | Bitstream Vera terms; DejaVu changes public domain |
| `ebook-print-pdf/media/contact-sheet.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/media/hero.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-detail.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-01.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-02.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-03.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-04.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-05.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-06.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-07.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-08.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-09.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-10.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-11.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-12.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-13.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-14.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before-pages/page-15.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/before.pdf` | Derived from this case’s original inputs by source/pipeline.py. Contains embedded subsets of the individually listed DejaVu faces. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/claims.json` | Generated by source/pipeline.py, source/inspect_pdf.py and tests/validation.py from the original inputs and the actual installed tools; dependency inventory lists package versions. | MIT (original content and records) |
| `ebook-print-pdf/output/contact-sheet.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/details/page-01.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/details/page-03.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/details/page-07.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/details/page-09.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/details/page-11.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/details/page-15.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/details/page-19.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/details/page-23.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/details/page-26.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/extracted-text.txt` | Generated by source/pipeline.py, source/inspect_pdf.py and tests/validation.py from the original inputs and the actual installed tools; dependency inventory lists package versions. | MIT (original content and records) |
| `ebook-print-pdf/output/fonts-dejavu.txt` | Copyright and permission notice from Debian fonts-dejavu-core 2.37-6; packaging metadata and the optional contact sentence omitted; copyright, trademark and permission conditions retained. | Bitstream Vera terms; DejaVu changes public domain |
| `ebook-print-pdf/output/geometry.json` | Generated by source/pipeline.py, source/inspect_pdf.py and tests/validation.py from the original inputs and the actual installed tools; dependency inventory lists package versions. | MIT (original content and records) |
| `ebook-print-pdf/output/hero.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/interior.pdf` | Derived from this case’s original inputs by source/pipeline.py. Contains embedded subsets of the individually listed DejaVu faces. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/layout.html` | Generated by source/pipeline.py, source/inspect_pdf.py and tests/validation.py from the original inputs and the actual installed tools; dependency inventory lists package versions. | MIT (original content and records) |
| `ebook-print-pdf/output/packages.tsv` | Generated by source/pipeline.py, source/inspect_pdf.py and tests/validation.py from the original inputs and the actual installed tools; dependency inventory lists package versions. | MIT (original content and records) |
| `ebook-print-pdf/output/page-pair.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/page-previews/github-1366.png` | Offline render of README.md and output/hero.png via harness/screenshot.py, Pages/GitHub frame, and github-markdown-css 5.8.1; see harness/licenses/github-markdown-css.txt. DejaVu glyphs in PNG renders. | MIT; DejaVu font terms for rendered glyphs |
| `ebook-print-pdf/output/page-previews/github-390.png` | Offline render of README.md and output/hero.png via harness/screenshot.py, Pages/GitHub frame, and github-markdown-css 5.8.1; see harness/licenses/github-markdown-css.txt. DejaVu glyphs in PNG renders. | MIT; DejaVu font terms for rendered glyphs |
| `ebook-print-pdf/output/page-previews/pages-1366.png` | Offline render of README.md and output/hero.png via harness/screenshot.py, Pages/GitHub frame, and github-markdown-css 5.8.1; see harness/licenses/github-markdown-css.txt. DejaVu glyphs in PNG renders. | MIT; DejaVu font terms for rendered glyphs |
| `ebook-print-pdf/output/page-previews/pages-390.png` | Offline render of README.md and output/hero.png via harness/screenshot.py, Pages/GitHub frame, and github-markdown-css 5.8.1; see harness/licenses/github-markdown-css.txt. DejaVu glyphs in PNG renders. | MIT; DejaVu font terms for rendered glyphs |
| `ebook-print-pdf/output/page-previews/screenshots.json` | Offline render of README.md and output/hero.png via harness/screenshot.py, Pages/GitHub frame, and github-markdown-css 5.8.1; see harness/licenses/github-markdown-css.txt. DejaVu glyphs in PNG renders. | MIT; DejaVu font terms for rendered glyphs |
| `ebook-print-pdf/output/pages/page-01.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-02.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-03.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-04.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-05.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-06.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-07.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-08.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-09.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-10.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-11.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-12.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-13.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-14.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-15.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-16.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-17.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-18.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-19.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-20.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-21.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-22.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-23.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-24.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-25.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/pages/page-26.png` | Derived from input/manuscript.md, input/print.json and input/notebook.svg through output/interior.pdf or output/before.pdf; exact frames/crops in output/render-map.json. DejaVu glyphs. | MIT content; DejaVu font terms |
| `ebook-print-pdf/output/render-map.json` | Generated by source/pipeline.py, source/inspect_pdf.py and tests/validation.py from the original inputs and the actual installed tools; dependency inventory lists package versions. | MIT (original content and records) |
| `ebook-print-pdf/output/report.json` | Generated by source/pipeline.py, source/inspect_pdf.py and tests/validation.py from the original inputs and the actual installed tools; dependency inventory lists package versions. | MIT (original content and records) |
| `ebook-print-pdf/output/runtime.json` | Generated by source/pipeline.py, source/inspect_pdf.py and tests/validation.py from the original inputs and the actual installed tools; dependency inventory lists package versions. | MIT (original content and records) |
| `ebook-print-pdf/output/source-map.json` | Generated by source/pipeline.py, source/inspect_pdf.py and tests/validation.py from the original inputs and the actual installed tools; dependency inventory lists package versions. | MIT (original content and records) |
| `ebook-print-pdf/output/validation.json` | Generated by source/pipeline.py, source/inspect_pdf.py and tests/validation.py from the original inputs and the actual installed tools; dependency inventory lists package versions. | MIT (original content and records) |
| `ebook-print-pdf/proof/claims.json` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/proof/existing-check.log` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/proof/links.json` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/proof/publication-scan.json` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/proof/repeat-run.log` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/proof/report.json` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/proof/reproducibility.json` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/proof/run.log` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/proof/runtime.json` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/proof/schema-tests.json` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/proof/scope.json` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/proof/validation.json` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/proof/visual-review.json` | Build/check records, source-based claim mapping, or direct visual review of this case’s generated files; runtime/report/validation mirror output files. | MIT |
| `ebook-print-pdf/run.sh` | Original case code, documentation or licence by Genco Doganay; README follows the shared case-page layout. | MIT |
| `ebook-print-pdf/source/README.md` | Original case code, documentation or licence by Genco Doganay; README follows the shared case-page layout. | MIT |
| `ebook-print-pdf/source/inspect_pdf.py` | Original case code, documentation or licence by Genco Doganay; README follows the shared case-page layout. | MIT |
| `ebook-print-pdf/source/layout.py` | Original case code, documentation or licence by Genco Doganay; README follows the shared case-page layout. | MIT |
| `ebook-print-pdf/source/pipeline.py` | Original case code, documentation or licence by Genco Doganay; README follows the shared case-page layout. | MIT |
| `ebook-print-pdf/tests/check.py` | Original case code, documentation or licence by Genco Doganay; README follows the shared case-page layout. | MIT |
| `ebook-print-pdf/tests/links.py` | Original case code, documentation or licence by Genco Doganay; README follows the shared case-page layout. | MIT |
| `ebook-print-pdf/tests/publication_scan.py` | Original case code, documentation or licence by Genco Doganay; README follows the shared case-page layout. | MIT |
| `ebook-print-pdf/tests/validation.py` | Original case code, documentation or licence by Genco Doganay; README follows the shared case-page layout. | MIT |
| `handwritten-notes/Dockerfile` | shared pinned harness recipe with declared Writer dependency group | MIT; installed dependencies retain their own notices in the image |
| `handwritten-notes/README.md` | Original case prose, pipeline, validation or test code authored for this delivery; run.sh uses the shared harness | MIT |
| `handwritten-notes/input/page-01.png` | Raster of source/pen-strokes.svg; identical-pixel reproduction verified in proof/source-raster-check.json | MIT |
| `handwritten-notes/input/pages.json` | Original source manifest and reviewed transcript of input/page-01.png | MIT |
| `handwritten-notes/input/transcript.json` | Original source manifest and reviewed transcript of input/page-01.png | MIT |
| `handwritten-notes/media/hero.png` | Source crop input/page-01.png plus crop of actual sanitized output/preview.pdf rendered by Poppler; captions in Inter | MIT content; Inter OFL 1.1 |
| `handwritten-notes/output/hero.png` | Source crop input/page-01.png plus crop of actual sanitized output/preview.pdf rendered by Poppler; captions in Inter | MIT content; Inter OFL 1.1 |
| `handwritten-notes/output/mapping.json` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/output/notes.docx` | Derived from input/transcript.json via original source/pipeline.py and LibreOffice; Inter font files licensed separately | MIT content; embedded Inter font portions OFL 1.1 |
| `handwritten-notes/output/notes.txt` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/output/packages.tsv` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/output/page-previews/github-1366.png` | Derived from this case README and real output hero; shared harness frame/Pages layout and MIT github-markdown-css 5.8.1 (notice: harness/licenses/github-markdown-css.txt); Chromium renderer | MIT for content/layout; third-party CSS MIT; rendered font licence records below |
| `handwritten-notes/output/page-previews/github-390.png` | Derived from this case README and real output hero; shared harness frame/Pages layout and MIT github-markdown-css 5.8.1 (notice: harness/licenses/github-markdown-css.txt); Chromium renderer | MIT for content/layout; third-party CSS MIT; rendered font licence records below |
| `handwritten-notes/output/page-previews/pages-1366.png` | Derived from this case README and real output hero; shared harness frame/Pages layout and MIT github-markdown-css 5.8.1 (notice: harness/licenses/github-markdown-css.txt); Chromium renderer | MIT for content/layout; third-party CSS MIT; rendered font licence records below |
| `handwritten-notes/output/page-previews/pages-390.png` | Derived from this case README and real output hero; shared harness frame/Pages layout and MIT github-markdown-css 5.8.1 (notice: harness/licenses/github-markdown-css.txt); Chromium renderer | MIT for content/layout; third-party CSS MIT; rendered font licence records below |
| `handwritten-notes/output/page-previews/screenshots.json` | Derived from this case README and real output hero; shared harness frame/Pages layout and MIT github-markdown-css 5.8.1 (notice: harness/licenses/github-markdown-css.txt); Chromium renderer | MIT for content/layout; third-party CSS MIT; rendered font licence records below |
| `handwritten-notes/output/pdf-fonts.txt` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/output/preview.pdf` | Derived from input/transcript.json via original source/pipeline.py and LibreOffice; Inter font files licensed separately | MIT content; embedded Inter font portions OFL 1.1 |
| `handwritten-notes/output/preview.png` | Derived from input/transcript.json via original source/pipeline.py and LibreOffice; Inter font files licensed separately | MIT content; embedded Inter font portions OFL 1.1 |
| `handwritten-notes/output/report.json` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/output/runtime.json` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/output/uncertainties.json` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/proof/boundary-checks.json` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/proof/claims.json` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/proof/links.json` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/proof/publication-scan.json` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/proof/report.json` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/proof/reproducibility.json` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/proof/run.txt` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/proof/runtime.json` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/proof/source-raster-check.json` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/proof/visual-review.md` | Generated measurements, original audit records or derived transcript content; sources named in each report | MIT |
| `handwritten-notes/run.sh` | Original case prose, pipeline, validation or test code authored for this delivery; run.sh uses the shared harness | MIT |
| `handwritten-notes/source/authorship.md` | Original case prose, pipeline, validation or test code authored for this delivery; run.sh uses the shared harness | MIT |
| `handwritten-notes/source/fonts/Inter-Regular.ttf` | Inter Project Authors; template font, unmodified; upstream https://github.com/rsms/inter; SHA-256 in toolchain.json | SIL OFL 1.1; source/fonts/LICENSE-Inter.txt |
| `handwritten-notes/source/fonts/Inter-SemiBold.ttf` | Inter Project Authors; template font, unmodified; upstream https://github.com/rsms/inter; SHA-256 in toolchain.json | SIL OFL 1.1; source/fonts/LICENSE-Inter.txt |
| `handwritten-notes/source/fonts/LICENSE-Inter.txt` | Inter Project Authors; original required copyright and font licence notice | SIL OFL 1.1 |
| `handwritten-notes/source/model.py` | Original case prose, pipeline, validation or test code authored for this delivery; run.sh uses the shared harness | MIT |
| `handwritten-notes/source/pen-strokes.svg` | Original editable digital full-word coordinate strokes, authored fresh; source/authorship.md records origin | MIT |
| `handwritten-notes/source/pipeline.py` | Original case prose, pipeline, validation or test code authored for this delivery; run.sh uses the shared harness | MIT |
| `handwritten-notes/source/publish-check.py` | Original case prose, pipeline, validation or test code authored for this delivery; run.sh uses the shared harness | MIT |
| `handwritten-notes/source/usage.md` | Original case prose, pipeline, validation or test code authored for this delivery; run.sh uses the shared harness | MIT |
| `handwritten-notes/tests/check.py` | Original case prose, pipeline, validation or test code authored for this delivery; run.sh uses the shared harness | MIT |
| `handwritten-notes/tests/prepare-boundary.py` | Original case prose, pipeline, validation or test code authored for this delivery; run.sh uses the shared harness | MIT |
| `handwritten-notes/tests/provenance.py` | Original case prose, pipeline, validation or test code authored for this delivery; run.sh uses the shared harness | MIT |
| `handwritten-notes/tests/regression.py` | Original case prose, pipeline, validation or test code authored for this delivery; run.sh uses the shared harness | MIT |
| `harness/Dockerfile` | Genco Doganay; newly authored for this pipeline | MIT |
| `harness/README.md` | Genco Doganay; newly authored for this pipeline | MIT |
| `harness/entrypoint.sh` | Genco Doganay; newly authored for this pipeline | MIT |
| `harness/licenses/github-markdown-css.txt` | github-markdown-css 5.8.1, Sindre Sorhus; npm distribution, notice in harness/licenses/github-markdown-css.txt | MIT |
| `harness/pages/_config.yml` | Adapted from the Ardholt S2 casebook template | MIT |
| `harness/pages/_layouts/default.html` | Adapted from the Ardholt S2 casebook template | MIT |
| `harness/pages/assets/site.css` | Adapted from the Ardholt S2 casebook template | MIT |
| `harness/run-container.sh` | Genco Doganay; newly authored for this pipeline | MIT |
| `harness/screenshot.py` | Genco Doganay; newly authored for this pipeline | MIT |
| `harness/vendor/github-frame.css` | Adapted from the Ardholt S2 casebook template | MIT |
| `harness/vendor/github-markdown.css` | github-markdown-css 5.8.1, Sindre Sorhus; npm distribution, notice in harness/licenses/github-markdown-css.txt | MIT |
| `kindle-tappable-footnotes/Dockerfile` | Shared document harness recipe for this case; case options are declared in run.sh. | MIT |
| `kindle-tappable-footnotes/LICENSE` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `kindle-tappable-footnotes/README.md` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `kindle-tappable-footnotes/input/book.json` | Genco Doganay; newly authored neutral book settings. | MIT |
| `kindle-tappable-footnotes/input/manuscript.md` | Genco Doganay; newly authored prose and footnote text. | MIT |
| `kindle-tappable-footnotes/media/hero.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/media/reader-note-1366-100.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/media/reader-note-1366-150.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/media/reader-note-390-100.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/media/reader-note-390-150.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/media/reader-passage.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/media/reader-return-1366-100.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/media/reader-return-1366-150.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/media/reader-return-390-100.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/media/reader-return-390-150.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/book.epub` | Derived from input/manuscript.md and input/book.json using source/book.py and source/book.css; no embedded fonts or external assets. | MIT |
| `kindle-tappable-footnotes/output/browser-audit.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/output/claims.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/output/epubcheck.log` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/output/font-license.txt` | Debian fonts-dejavu-core 2.37-6 copyright notice, copied without alteration. | Bitstream Vera permissive font licence; DejaVu changes public domain; packaging notices retained. |
| `kindle-tappable-footnotes/output/font-selection.txt` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/output/hero.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/negative-tests.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/output/note-detail.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/packages.tsv` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/output/page-previews/github-1366.png` | Offline render of README.md and actual media, using harness layouts and github-markdown-css 5.8.1; DejaVu fonts. | MIT for case and layout; upstream MIT CSS notice and permissive font notice retained. |
| `kindle-tappable-footnotes/output/page-previews/github-390.png` | Offline render of README.md and actual media, using harness layouts and github-markdown-css 5.8.1; DejaVu fonts. | MIT for case and layout; upstream MIT CSS notice and permissive font notice retained. |
| `kindle-tappable-footnotes/output/page-previews/pages-1366.png` | Offline render of README.md and actual media, using harness layouts and github-markdown-css 5.8.1; DejaVu fonts. | MIT for case and layout; upstream MIT CSS notice and permissive font notice retained. |
| `kindle-tappable-footnotes/output/page-previews/pages-390.png` | Offline render of README.md and actual media, using harness layouts and github-markdown-css 5.8.1; DejaVu fonts. | MIT for case and layout; upstream MIT CSS notice and permissive font notice retained. |
| `kindle-tappable-footnotes/output/page-previews/screenshots.json` | Offline render of README.md and actual media, using harness layouts and github-markdown-css 5.8.1; DejaVu fonts. | MIT for case and layout; upstream MIT CSS notice and permissive font notice retained. |
| `kindle-tappable-footnotes/output/passage-detail.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/pip-freeze.txt` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/output/reader-note-1366-100.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/reader-note-1366-150.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/reader-note-390-100.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/reader-note-390-150.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/reader-passage.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/reader-return-1366-100.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/reader-return-1366-150.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/reader-return-390-100.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/reader-return-390-150.png` | Chromium render of output/book.epub from input/manuscript.md and input/book.json; original crop composition where applicable. DejaVu glyphs; no image metadata. | MIT |
| `kindle-tappable-footnotes/output/report.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/output/run.log` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/output/runtime.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/output/source-map.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/proof/check-run.log` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/proof/claims.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/proof/first-run-report.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/proof/link-audit.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/proof/paths-run.log` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/proof/publication-scan.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/proof/report.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/proof/reproducibility.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/proof/runtime.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/proof/second-run-report.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/proof/visual-review.json` | Generated or reviewed evidence of the original input files, delivered EPUB and documented checks; tool output and measurements are factual records. | MIT |
| `kindle-tappable-footnotes/run.sh` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `kindle-tappable-footnotes/source/INPUT.md` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `kindle-tappable-footnotes/source/book.css` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `kindle-tappable-footnotes/source/book.py` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `kindle-tappable-footnotes/source/browser.py` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `kindle-tappable-footnotes/source/fonts.conf` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `kindle-tappable-footnotes/source/licenses/dejavu.txt` | Debian fonts-dejavu-core 2.37-6 copyright notice, copied without alteration. | Bitstream Vera permissive font licence; DejaVu changes public domain; packaging notices retained. |
| `kindle-tappable-footnotes/source/licenses/github-markdown-css.txt` | Shared harness notice for github-markdown-css 5.8.1; retained without alteration. | MIT, upstream copyright retained. |
| `kindle-tappable-footnotes/source/pipeline.py` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `kindle-tappable-footnotes/source/reader.html` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `kindle-tappable-footnotes/tests/check.py` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `kindle-tappable-footnotes/tests/contracts.py` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `kindle-tappable-footnotes/tests/publication.py` | Genco Doganay; original case code, documentation or generated evidence. | MIT |
| `pdf-layout-compression/Dockerfile` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/README.md` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/input/input.pdf` | Genco Doganay; source/content.json and source/make_input.py | MIT content; DejaVu font permission |
| `pdf-layout-compression/input/repair.json` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/licenses/DejaVu.txt` | Debian fonts-dejavu-core 2.37-6 upstream copyright and permission notice | Bitstream Vera permission; DejaVu changes public domain |
| `pdf-layout-compression/media/hero.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/adversarial.json` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/output/claims.json` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/output/fixed.pdf` | Derived from input/input.pdf by source/pipeline.py; embedded DejaVu Sans subsets | MIT content; DejaVu font permission |
| `pdf-layout-compression/output/packages.tsv` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/output/page-previews/github-1366.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/page-previews/github-390.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/page-previews/pages-1366.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/page-previews/pages-390.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/page-previews/screenshots.json` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/after-1.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/after-2.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/after-3.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/all-pages.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/before-1.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/before-2.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/before-3.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/comparison-1.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/comparison-2.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/comparison-3.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/detail-1.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/detail-2.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/detail-3.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/frames.json` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/output/previews/hero.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/image-detail-1.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/image-detail-2.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/previews/image-detail-3.png` | Poppler render of input/input.pdf or output/fixed.pdf; or Chromium render of README.md as identified by frames.json and screenshots.json | MIT authored content; DejaVu font permission; page CSS MIT |
| `pdf-layout-compression/output/report.json` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/output/runtime.json` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/proof/adversarial.log` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/proof/check.log` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/proof/claims.json` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/proof/malware.json` | Generated final publication/security evidence | MIT |
| `pdf-layout-compression/proof/malware.log` | Generated final publication/security evidence | MIT |
| `pdf-layout-compression/proof/publication-audit.json` | Generated final publication/security evidence | MIT |
| `pdf-layout-compression/proof/repeat.log` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/proof/report.json` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/proof/run.log` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/proof/runtime.json` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/proof/visual-review.json` | Measured/generated evidence from this run; figure derivations in output/previews/frames.json | MIT |
| `pdf-layout-compression/run.sh` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/source/README.md` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/source/claim_map.py` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/source/common.py` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/source/content.json` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/source/make_input.py` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/source/pipeline.py` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/source/render.py` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/tests/README.md` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/tests/adversarial.py` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/tests/audit.py` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/tests/check.py` | Genco Doganay; newly authored for this pipeline | MIT |
| `pdf-layout-compression/tests/repeat.sh` | Genco Doganay; newly authored for this pipeline | MIT |
| `retype-150-pages/Dockerfile` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/LICENSE` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/README.md` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/input/review.csv` | Original literal corrections from visual inspection of the source scan (sources: input/scan.pdf, source/review-record.md) | MIT |
| `retype-150-pages/input/scan.pdf` | Original typed records rendered fresh as raster-only pages (sources: source/reference.json, source/generate.py, source/DejaVuSansMono.ttf) | MIT original content; rendered DejaVu glyphs under Bitstream Vera permission |
| `retype-150-pages/licenses/DejaVu.txt` | DejaVu fonts copyright notice, font portion only; unrelated Debian packaging notices omitted (sources: https://dejavu-fonts.github.io/) | Retained Bitstream Vera permission notice |
| `retype-150-pages/make-input.sh` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/media/hero.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/accuracy.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/checks.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/claims.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/conversion.log` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/corrections.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/layout.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/media/contact-001.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/media/contact-031.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/media/contact-061.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/media/contact-091.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/media/contact-121.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/media/contact-sheets.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/media/detail-001.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/media/detail-031.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/media/detail-075.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/media/detail-121.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/media/detail-150.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/media/document-page-001.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/media/figure-map.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/media/hero.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/media/scan-page-001.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/packages.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/page-previews/github-1366.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/page-previews/github-390.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/page-previews/pages-1366.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/page-previews/pages-390.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/page-previews/screenshots.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/pages.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/preview.pdf` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/raw/page-001.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-001.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-002.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-002.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-003.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-003.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-004.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-004.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-005.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-005.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-006.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-006.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-007.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-007.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-008.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-008.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-009.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-009.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-010.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-010.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-011.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-011.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-012.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-012.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-013.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-013.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-014.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-014.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-015.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-015.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-016.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-016.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-017.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-017.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-018.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-018.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-019.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-019.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-020.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-020.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-021.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-021.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-022.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-022.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-023.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-023.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-024.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-024.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-025.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-025.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-026.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-026.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-027.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-027.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-028.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-028.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-029.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-029.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-030.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-030.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-031.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-031.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-032.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-032.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-033.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-033.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-034.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-034.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-035.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-035.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-036.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-036.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-037.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-037.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-038.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-038.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-039.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-039.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-040.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-040.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-041.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-041.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-042.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-042.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-043.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-043.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-044.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-044.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-045.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-045.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-046.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-046.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-047.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-047.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-048.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-048.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-049.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-049.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-050.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-050.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-051.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-051.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-052.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-052.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-053.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-053.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-054.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-054.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-055.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-055.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-056.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-056.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-057.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-057.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-058.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-058.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-059.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-059.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-060.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-060.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-061.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-061.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-062.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-062.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-063.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-063.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-064.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-064.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-065.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-065.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-066.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-066.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-067.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-067.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-068.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-068.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-069.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-069.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-070.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-070.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-071.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-071.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-072.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-072.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-073.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-073.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-074.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-074.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-075.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-075.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-076.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-076.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-077.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-077.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-078.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-078.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-079.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-079.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-080.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-080.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-081.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-081.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-082.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-082.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-083.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-083.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-084.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-084.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-085.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-085.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-086.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-086.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-087.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-087.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-088.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-088.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-089.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-089.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-090.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-090.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-091.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-091.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-092.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-092.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-093.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-093.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-094.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-094.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-095.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-095.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-096.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-096.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-097.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-097.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-098.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-098.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-099.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-099.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-100.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-100.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-101.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-101.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-102.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-102.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-103.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-103.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-104.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-104.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-105.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-105.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-106.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-106.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-107.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-107.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-108.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-108.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-109.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-109.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-110.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-110.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-111.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-111.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-112.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-112.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-113.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-113.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-114.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-114.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-115.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-115.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-116.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-116.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-117.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-117.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-118.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-118.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-119.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-119.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-120.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-120.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-121.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-121.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-122.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-122.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-123.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-123.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-124.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-124.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-125.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-125.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-126.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-126.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-127.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-127.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-128.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-128.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-129.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-129.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-130.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-130.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-131.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-131.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-132.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-132.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-133.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-133.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-134.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-134.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-135.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-135.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-136.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-136.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-137.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-137.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-138.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-138.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-139.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-139.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-140.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-140.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-141.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-141.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-142.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-142.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-143.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-143.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-144.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-144.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-145.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-145.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-146.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-146.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-147.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-147.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-148.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-148.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-149.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-149.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-150.tsv` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/raw/page-150.txt` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/report.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/output/retyped.docx` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/output/runtime.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/adversarial.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/antivirus-acquisition.log` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/antivirus-update.log` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/antivirus.log` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/check.log` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/checks.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/claims.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/code-errors.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/page-previews/github-1366.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/proof/page-previews/github-390.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/proof/page-previews/pages-1366.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/proof/page-previews/pages-390.png` | Derived from the shipped scan and delivered document by the recorded applications (sources: input/scan.pdf, input/review.csv, output/report.json, licenses/DejaVu.txt, ../harness/licenses/github-markdown-css.txt) | MIT original content; DejaVu font permission; GitHub Markdown CSS MIT where present |
| `retype-150-pages/proof/page-previews/screenshots.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/publication.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/repeat-run.log` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/repeat.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/report.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/run.log` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/runtime.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/proof/visual-review.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/run.sh` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/DejaVuSansMono.ttf` | Unmodified DejaVu Sans Mono 2.37; DejaVu project distribution (sources: licenses/DejaVu.txt) | Bitstream Vera permission; DejaVu changes public domain |
| `retype-150-pages/source/REPRODUCING.md` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/asset-manifest.json` | Original per-file provenance inventory by Genco Doganay | MIT |
| `retype-150-pages/source/assets.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/author.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/common.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/container.env` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/corpus-manifest.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/document.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/extract.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/figures.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/generate.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/layout.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/pipeline.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/reference.json` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/review-record.md` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/source/score.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/tests/adversarial.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/tests/adversarial.sh` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/tests/check.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/tests/code_errors.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/tests/publication.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/tests/repeat.py` | Original code, text or generated measurements by Genco Doganay | MIT |
| `retype-150-pages/tests/security.sh` | Original code, text or generated measurements by Genco Doganay | MIT |
| `school-fillable-forms/INPUT.md` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/LICENSE` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/README.md` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/container-recipe.json` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/input/forms.json` | Genco Doganay | MIT / Fresh generic school form definitions or neutral values authored for this case; no pupil identities or contact data. |
| `school-fillable-forms/input/values.json` | Genco Doganay | MIT / Fresh generic school form definitions or neutral values authored for this case; no pupil identities or contact data. |
| `school-fillable-forms/media/README.md` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/media/hero.png` | Genco Doganay | MIT / Unscaled crops from actual LibreOffice/Poppler output; source PDF/PNG rectangles and placements in output/preview-map.json. Captions and original form content MIT; DejaVu faces licensed as recorded. |
| `school-fillable-forms/output/absence-request-blank.docx` | Genco Doganay | MIT / Derived from input/forms.json and, for filled states, input/values.json by source/forms.py and actual LibreOffice UNO entry/export. Original content MIT; no embedded font or image files. |
| `school-fillable-forms/output/absence-request-blank.pdf` | Genco Doganay | MIT content; DejaVu subset fonts under Bitstream Vera / public domain / LibreOffice export of the matching delivered DOCX, followed by removal of PDF Info/XMP. Source input JSON is listed above; font notices retained in output/font-licenses/. |
| `school-fillable-forms/output/absence-request-blank.png` | Genco Doganay | MIT / Poppler rasterization of the matching sanitized PDF from the actual LibreOffice run; original form content MIT, DejaVu font notices retained. |
| `school-fillable-forms/output/absence-request-filled.docx` | Genco Doganay | MIT / Derived from input/forms.json and, for filled states, input/values.json by source/forms.py and actual LibreOffice UNO entry/export. Original content MIT; no embedded font or image files. |
| `school-fillable-forms/output/absence-request-filled.pdf` | Genco Doganay | MIT content; DejaVu subset fonts under Bitstream Vera / public domain / LibreOffice export of the matching delivered DOCX, followed by removal of PDF Info/XMP. Source input JSON is listed above; font notices retained in output/font-licenses/. |
| `school-fillable-forms/output/absence-request-filled.png` | Genco Doganay | MIT / Poppler rasterization of the matching sanitized PDF from the actual LibreOffice run; original form content MIT, DejaVu font notices retained. |
| `school-fillable-forms/output/claims.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/output/font-licenses/fonts-dejavu-core.txt` | Bitstream, Inc.; DejaVu contributors; Debian package contributors | Bitstream Vera / public domain; Debian packaging notices GPL-2+ / Verbatim copyright record from fonts-dejavu-core 2.37-6 in the pinned container. Covers the actual DejaVu faces and embedded subsets used in the output. |
| `school-fillable-forms/output/font-licenses/fonts-liberation.txt` | Red Hat, Inc.; Debian package contributors | GPL-2 with font embedding exception; packaging notices retained / Verbatim copyright record from fonts-liberation 1:1.07.4-11, installed by the shared base. Retained as a dependency notice; no claim of use in the forms. |
| `school-fillable-forms/output/hero.png` | Genco Doganay | MIT / Unscaled crops from actual LibreOffice/Poppler output; source PDF/PNG rectangles and placements in output/preview-map.json. Captions and original form content MIT; DejaVu faces licensed as recorded. |
| `school-fillable-forms/output/packages.tsv` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/output/page-previews/github-1366.png` | Genco Doganay | MIT / Offline Chromium rendering of this README with the shared harness. Original case content MIT; vendored github-markdown-css 5.8.1 MIT notice remains in harness/licenses/github-markdown-css.txt. DejaVu font notices retained. |
| `school-fillable-forms/output/page-previews/github-390.png` | Genco Doganay | MIT / Offline Chromium rendering of this README with the shared harness. Original case content MIT; vendored github-markdown-css 5.8.1 MIT notice remains in harness/licenses/github-markdown-css.txt. DejaVu font notices retained. |
| `school-fillable-forms/output/page-previews/pages-1366.png` | Genco Doganay | MIT / Offline Chromium rendering of this README with the shared harness. Original case content MIT; vendored github-markdown-css 5.8.1 MIT notice remains in harness/licenses/github-markdown-css.txt. DejaVu font notices retained. |
| `school-fillable-forms/output/page-previews/pages-390.png` | Genco Doganay | MIT / Offline Chromium rendering of this README with the shared harness. Original case content MIT; vendored github-markdown-css 5.8.1 MIT notice remains in harness/licenses/github-markdown-css.txt. DejaVu font notices retained. |
| `school-fillable-forms/output/page-previews/screenshots.json` | Genco Doganay | MIT / Offline Chromium rendering of this README with the shared harness. Original case content MIT; vendored github-markdown-css 5.8.1 MIT notice remains in harness/licenses/github-markdown-css.txt. DejaVu font notices retained. |
| `school-fillable-forms/output/preview-map.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/output/publication-audit.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/output/rendered-negative.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/output/report.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/output/roundtrip.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/output/runtime.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/output/selftest.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/output/trip-permission-blank.docx` | Genco Doganay | MIT / Derived from input/forms.json and, for filled states, input/values.json by source/forms.py and actual LibreOffice UNO entry/export. Original content MIT; no embedded font or image files. |
| `school-fillable-forms/output/trip-permission-blank.pdf` | Genco Doganay | MIT content; DejaVu subset fonts under Bitstream Vera / public domain / LibreOffice export of the matching delivered DOCX, followed by removal of PDF Info/XMP. Source input JSON is listed above; font notices retained in output/font-licenses/. |
| `school-fillable-forms/output/trip-permission-blank.png` | Genco Doganay | MIT / Poppler rasterization of the matching sanitized PDF from the actual LibreOffice run; original form content MIT, DejaVu font notices retained. |
| `school-fillable-forms/output/trip-permission-filled.docx` | Genco Doganay | MIT / Derived from input/forms.json and, for filled states, input/values.json by source/forms.py and actual LibreOffice UNO entry/export. Original content MIT; no embedded font or image files. |
| `school-fillable-forms/output/trip-permission-filled.pdf` | Genco Doganay | MIT content; DejaVu subset fonts under Bitstream Vera / public domain / LibreOffice export of the matching delivered DOCX, followed by removal of PDF Info/XMP. Source input JSON is listed above; font notices retained in output/font-licenses/. |
| `school-fillable-forms/output/trip-permission-filled.png` | Genco Doganay | MIT / Poppler rasterization of the matching sanitized PDF from the actual LibreOffice run; original form content MIT, DejaVu font notices retained. |
| `school-fillable-forms/proof/argument-validation.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/proof/claims.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/proof/publication-audit.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/proof/publication-review.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/proof/repeatability.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/proof/report.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/proof/run.txt` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/proof/runtime.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/proof/selftest.json` | Genco Doganay | MIT / Generated measurements, actual tool/runtime records, static scan or publishing-read evidence for the delivered case. Source and methodology identified in each record; no inherited result figures. |
| `school-fillable-forms/run.sh` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/source/forms.py` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/source/office.py` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/source/pipeline.py` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/tests/check.py` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/tests/compare_runs.py` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/tests/fixtures/replacement/forms.json` | Genco Doganay | MIT / Fresh generic school form definitions or neutral values authored for this case; no pupil identities or contact data. |
| `school-fillable-forms/tests/fixtures/replacement/values.json` | Genco Doganay | MIT / Fresh generic school form definitions or neutral values authored for this case; no pupil identities or contact data. |
| `school-fillable-forms/tests/publication_audit.py` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/tests/rendered_negative.py` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `school-fillable-forms/tests/selftest.py` | Genco Doganay | MIT / Original case implementation, test, documentation or licence text. Uses the separately shared harness; no recovered implementation or external image was reused. |
| `toolchain/data-to-powerpoint.json` | Dependency and toolchain record for the case: image, base digest, pins and tool versions | MIT |
| `toolchain/ebook-print-pdf.json` | Dependency and toolchain record for the case: image, base digest, pins and tool versions | MIT |
| `toolchain/handwritten-notes.json` | Dependency and toolchain record for the case: image, base digest, pins and tool versions | MIT |
| `toolchain/kindle-tappable-footnotes.json` | Dependency and toolchain record for the case: image, base digest, pins and tool versions | MIT |
| `toolchain/pdf-layout-compression.json` | Dependency and toolchain record for the case: image, base digest, pins and tool versions | MIT |
| `toolchain/retype-150-pages.json` | Dependency and toolchain record for the case: image, base digest, pins and tool versions | MIT |
| `toolchain/school-fillable-forms.json` | Dependency and toolchain record for the case: image, base digest, pins and tool versions | MIT |
| `tools/build-index` | Original repository root file (tools/build-index comes from the Ardholt casebook page template) | MIT |
