# Shared document harness

Keep this directory beside the case directories. `../harness/run-container.sh CASE_DIR "$@"` provides Docker argument handling, separate read-only input and writable output mounts, rootless/rootful user handling, offline execution, a read-only root filesystem, resource limits and a fresh `LO_PROFILE_URI`. The case supplies `source/pipeline.py` and `tests/check.py`. Only the output directory is written by a normal run. The `--check` mode inspects existing output with the existing image, without conversion or image building.

The Debian bookworm-slim base is pinned by digest. Direct package versions and pypdf are pinned in `Dockerfile`; the complete resolved package inventory is emitted as `output/packages.tsv`. Current Debian mirrors supply these exact versions: missing versions fail, rather than silently upgrading. Apt has two retries, a connection timeout, an update deadline and an install deadline. Pip has two retries and an operation deadline. The runner allows at most 25 minutes for build and 18 minutes for workload, within the 45-minute CI job. No cache is required. The base is built and tagged `dp-base:1` locally; it is not a private registry prerequisite.

This first image installs only PDF creation/repair/checking tools, fonts and Chromium for page proof. To build another document case, reuse the recipe with the pinned optional groups below and set its image name in a copy of the runner or via `DP_IMAGE`. Pass `DP_EXTRA_APT` / `DP_EXTRA_PIP` to opt in. Do not install every group by default.

| Need | Exact build-argument values |
|---|---|
| Headless text documents | `EXTRA_APT="libreoffice-writer=4:7.4.7-1+deb12u14 python3-docx=0.8.11+dfsg1-5"` |
| Headless presentations | `EXTRA_APT="libreoffice-impress=4:7.4.7-1+deb12u14"` and `EXTRA_PIP="python-pptx==1.0.2"` |
| Markdown conversion | `EXTRA_APT="pandoc=2.17.1.1-2~deb12u1"` |

Use `timeout 180 libreoffice "-env:UserInstallation=$LO_PROFILE_URI" --headless ...` inside the container. The profile is created afresh for every run and removed on exit. Locale is `C.UTF-8`, timezone UTC. Other cases must verify their own cold build and record actual application versions; the optional groups above are declared pins, not claims of an application run. Review the resolved dependency inventory when changing a pin.

## Evidence contract

All JSON uses UTF-8 and `schema_version: 1`. Reports describe actual outputs. Preserve these literal keys:

- `report.json`: `case`, `input_hashes` and `output_hashes` (relative filenames to SHA-256), `transformations` (ordered operations with parameters), `counts` (measured facts), `checks` (name, passed, observation), `tools` (actual version strings), `uncertainties` (limitations), `human_steps` (accurate manual steps, or empty).
- `runtime.json`: `scope`, `elapsed_seconds`, `limits`, `status`. State whether setup and manual work are included.
- `claims.json`: `claims`, each with `claim`, `evidence` (relative path and JSON pointer/line/frame), and `calculation` where arithmetic is used. Separate machine checks from visual review and untested compatibility.

Case-specific fields may extend these shapes. Page and text maps should preserve source order. Publish `output/report.json` and `output/runtime.json`; mirror them to `proof/` if the case keeps a copy. The converter must not write to its mounted case source. Page proof and claims go in the selected output directory, then the reviewed versions are copied to tracked `proof/` and `media/`.

## Page screenshots

`screenshot.py /case /output/page-previews` renders the case README using a local GitHub file-view frame and the Pages layout, at 390×844 and 1366×768 CSS pixels with device scale 1. It uses Python Markdown 3.4.1, vendored github-markdown-css 5.8.1 and Chromium from the pinned image. It runs offline. The GitHub header, repository navigation, path bar and file controls stay visible. The frame is a local layout approximation, not a capture of a published URL. The unavailable CI badge says so, never "passing". Images are embedded from actual case files. The production Pages layout carries the public analytics snippet; it makes no request in the offline run.

Copy `pages/_config.yml`, `pages/_layouts/` and `pages/assets/` to the repository root. The footer has one link, to https://ardholt.com/p/. `vendor/github-frame.css` is the casebook page frame; `vendor/github-markdown.css` retains its MIT notice in `licenses/`. No live-site or workflow reachability is claimed by the offline run. The two HTML render sources are built in a temporary folder and are not kept: only the four PNG frames and `screenshots.json` are written to the output, so no look-alike or offline copy of the page can be published by accident.
