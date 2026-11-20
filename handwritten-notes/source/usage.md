# Inputs and scope

A person reads the images, prepares `transcript.json`, records uncertainties and reviews the spelling and structure before this command. This service combines that transcription/review step with repeatable layout and checks; the command itself performs no handwriting recognition. For a real document, replace the recorded human-step provenance with the actual review record before delivery.

Both JSON files are UTF-8 with `schema_version: 1`. `pages.json` has `pages`, each with a unique string `id` and a `file` pointing to a PNG/JPEG inside the input directory. Paths cannot escape input. `transcript.json` has `pages`, each with `id`, `blocks` and `uncertainties`. Every source page occurs exactly once; source manifest order controls output. A block has a unique nonempty string `id` within its page, `kind` of `heading`, `paragraph` or `bullet`, and nonempty string `text`. Each uncertainty has `block_id`, literal `token: "[unclear]"`, and a nonempty `reason`. Each occurrence of `[unclear]` requires its own entry. Unknown descriptive keys are ignored; unsupported types are rejected.

See the shipped JSON files for complete input documents. Every source page starts separately in DOCX; long pages can flow across multiple PDF pages. The mapping uses DOCX paragraph indices and source IDs, not a promise of identical source/output pagination. Literal text is retained; list markers are formatting. Markdown in a block is ordinary text.

Run from this case directory:

```bash
./run.sh --input "/absolute/input directory" --output "/absolute/output directory"
```

Input is mounted read-only, output separately, and document processing runs without network access. Only output is written. Keep the output directory dedicated to this job. Docker needs sufficient disk for the shared Debian base plus LibreOffice Writer. The shared harness is required beside this case; `Dockerfile` is the cold-build recipe used through the harness with the Writer dependency group declared in `run.sh`. No prebuilt private image is needed.

```bash
./run.sh --input "/absolute/input directory" --output "/absolute/output directory" --check
```

The check command examines existing output using the already built image. It does not convert or rebuild. A failed converter, invalid mapping, missing input or damaged output exits nonzero. Workload and setup timings are separate. Document fonts are the included OFL Inter files; the package inventory records the resolved runtime.

Crossed-out policy: omit struck-out words, and record each omission in a reviewed decision record before running the command. This policy is a manual review responsibility. The command cannot infer strike-through or validate image reading.
