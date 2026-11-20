# Input contract and checks

Only Git and Docker are required on the host. Run from this case directory:

```bash
./run.sh --input "/absolute/input directory" --output "/absolute/output directory"
```

The input directory must contain `input.pdf` (unencrypted digital PDF with searchable text and oversized images) and `repair.json`:

```json
{"schema_version":1,"target_width_mm":210,"target_height_mm":297,"margin_mm":10,"image_dpi":150}
```

The target is portrait A4. Margins accept 8–20 mm and image resolution accepts 150–200 dpi. Additional descriptive JSON keys are ignored. Unknown schema versions, invalid values, non-digital pages, encrypted or malformed PDFs and missing files fail with a diagnostic. Input and output must be separate directories, and comma-containing paths are rejected because Docker mount syntax uses commas. Spaces are supported. Input is mounted read-only; only output and temporary container storage are writable.

Content must be recoverable inside MediaBox. The dominant physical text baseline determines upright orientation; right-angle rotations are supported. Oblique text needs review. Mixed-direction layouts may need manual orientation review. Annotations, forms, actions, named destinations, attachments and layers are rejected before conversion: they are never silently removed as a compression trick. Very small text, low-resolution images or a result that is not smaller also fail the delivery checks. This is an intentionally bounded repair service, not arbitrary PDF reconstruction.

Inspect an existing output without running conversion or rebuilding the image:

```bash
./run.sh --check
```

`--check` also accepts `--input` and `--output`. It requires the already-built `dp-base:1`. Checks independently inspect the actual PDF, compare word order and page count with the supplied input, check image count and resolution, embedded fonts, page boxes and text bounds, and run qpdf. A Poppler render comparison against the restored uncompressed source checks image and vector conservation. It also verifies report facts and hashes.

For the authored input, run the mutation and reference tests after a normal run:

```bash
docker run --rm --cpus 2 --memory 2g --network none \
  --mount "type=bind,src=$PWD,dst=/case,readonly" \
  --mount "type=bind,src=$PWD/input,dst=/input,readonly" \
  --mount "type=bind,src=$PWD/output,dst=/output" \
  dp-base:1 python /case/tests/adversarial.py /input /output
```

On rootful Docker add `--user "$(id -u):$(id -g)"` before the image name. This test removes a page, changes text, crops a page and removes an image. It requires each defect to be rejected; it also exercises malformed, encrypted, annotated and invalid-configuration inputs. The reference comparison checks actual output words against `source/content.json`, independently of input extraction. Temporary mutations are never published as repaired PDFs.

The run uses a fresh LibreOffice profile even for cases that do not invoke LibreOffice. This case does not install or claim a LibreOffice run. The shared harness documents how other cases opt into it.

`bash tests/repeat.sh` verifies a second run using absolute paths containing spaces, compares the PDF bytes and complete report, and confirms missing/overlapping input paths fail without modifying the input. This test uses a temporary directory and cleans it afterwards.
