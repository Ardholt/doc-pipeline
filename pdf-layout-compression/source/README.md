# Source and regeneration

Genco Doganay authored `content.json` and `make_input.py` for this case. The latter draws the text, rules, arrows and three coloured contour fields from mathematical curves. There are no imported pictures, client materials or hidden reference pages.

Each contour field is a full-resolution RGB image. The export deliberately stores those image pixels as ordinary uncompressed PDF image streams, an inefficient but valid image export. Every image pixel is used on a visible page; there is no padding, duplicate hidden content or embedded attachment. The recipe then sets a restrictive CropBox on the first page and a clockwise rotation flag on the second. The last page has a different MediaBox. Text remains recoverable within the original MediaBox.

From the repository root, after the normal run has built `dp-base:1`:

```bash
docker run --rm --cpus 2 --memory 2g --network none \
  --mount "type=bind,src=$PWD/pdf-layout-compression/source,dst=/source,readonly" \
  --mount "type=bind,src=$PWD/pdf-layout-compression/input,dst=/generated" \
  dp-base:1 python /source/make_input.py /generated
```

This is an explicit authoring operation that replaces `input/input.pdf`; normal `run.sh` never invokes it. On rootful Docker, add `--user "$(id -u):$(id -g)"` before the image name. DejaVu Sans is embedded in the PDF; its notice is in `../licenses/`. The generator clears PDF Info metadata before saving. Previews render that cleaned PDF.

The converter reads only `input.pdf` and `repair.json`; it does not read `content.json`. The independent reference is used only by the authored-input tests. `common.py` records each page's affine transform and the report retains the input-to-output word map. `render.py` derives every document figure from Poppler renders, including an equal-scale detail of the clipped page. Whole-page panels fit pages to each panel, as recorded in `output/previews/frames.json`.
