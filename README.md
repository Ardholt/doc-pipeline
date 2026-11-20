# Document pipelines

**Seven document problems, each run end to end on the input in its folder, with the input and every output included, measured and runnable with one command.**

## The cases

<!-- cases:start -->
1. **[My PDF has cut-off pages and is too large to send](pdf-layout-compression/README.md)**  
   I restored the cut-off text and reduced this PDF from 28.40 MB to 0.125 MB, retaining all 3 pages and 224 words. · [on the web](https://ardholt.github.io/doc-pipeline/pdf-layout-compression/)  
   <sub>pdf · layout · compression</sub>

2. **[My eBook needs a properly laid-out print PDF](ebook-print-pdf/README.md)**  
   I laid out a six-chapter manuscript as a checked 26-page print interior, with editable source and before/after proof. · [on the web](https://ardholt.github.io/doc-pipeline/ebook-print-pdf/)  
   <sub>pdf · ebook · print layout</sub>

3. **[My Kindle book needs footnotes readers can tap and return from](kindle-tappable-footnotes/README.md)**  
   I built a reflowable EPUB 3 with 22 references to 18 notes, no EPUBCheck errors or warnings, and 88 passing browser tap-and-return journeys; tested in a browser, not on a Kindle or the Kindle Previewer. · [on the web](https://ardholt.github.io/doc-pipeline/kindle-tappable-footnotes/)  
   <sub>epub · ebook · footnotes</sub>

4. **[I need 150 scanned pages made editable](retype-150-pages/README.md)**  
   I made a generated 150-page typed scan editable and searchable, with every page mapped: 99.813% of characters match the source text, but 203 of its 750 record and item codes in the delivered file are still wrong. · [on the web](https://ardholt.github.io/doc-pipeline/retype-150-pages/)  
   <sub>documents · ocr · docx</sub>

5. **[I need handwritten notes typed clearly without guessing unclear words](handwritten-notes/README.md)**  
   I turned a transcript I prepared from the page into an editable document, a PDF and a page/block map, with the unclear word left marked as [unclear], not guessed; the tool performs no handwriting recognition. · [on the web](https://ardholt.github.io/doc-pipeline/handwritten-notes/)  
   <sub>transcription · handwriting · docx</sub>

6. **[I need a business presentation built from my figures](data-to-powerpoint/README.md)**  
   I built an editable PPTX with native charts, a PDF deck and checked source-to-chart reconciliation. · [on the web](https://ardholt.github.io/doc-pipeline/data-to-powerpoint/)  
   <sub>presentations · pptx · charts</sub>

7. **[I need school forms people can fill in without moving the layout](school-fillable-forms/README.md)**  
   I built trip-permission and absence-request DOCX forms, entered multiline text and checkbox states in LibreOffice, and verified the saved and reopened files. · [on the web](https://ardholt.github.io/doc-pipeline/school-fillable-forms/)  
   <sub>docx · forms · school</sub>
<!-- cases:end -->

## How every case is laid out

Each folder opens with the problem, the result and the proof from the real output, then what was wrong, what I did, the numbers linked to the files they come from, one command to run it yourself, and the tests that check it.

## Run any case

Install Git and Docker, clone the repository, then:

```bash
git clone https://github.com/Ardholt/doc-pipeline.git
cd doc-pipeline/<case folder> && ./run.sh
```

Each case builds its pinned tools in Docker, regenerates its outputs from `input/` and runs its checks; the document work itself runs offline. `./run.sh --check` inspects existing output without rebuilding, and `./run.sh --input "/absolute/input directory" --output "/absolute/output directory"` runs your own files. The tools, base image and package versions are recorded in [toolchain/](https://github.com/Ardholt/doc-pipeline/tree/main/toolchain), and every file's source and licence is in [ASSET-LICENSES.md](ASSET-LICENSES.md).

[![Checks](https://github.com/Ardholt/doc-pipeline/actions/workflows/checks.yml/badge.svg)](https://github.com/Ardholt/doc-pipeline/actions/workflows/checks.yml)

---

Maintained by Genco Doganay, Ardholt  
<sub>More of my work: [ardholt.com/p](https://ardholt.com/p/) · Licence: [MIT](LICENSE)</sub>
