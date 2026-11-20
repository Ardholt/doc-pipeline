# Form inputs

Provide UTF-8 `forms.json` and `values.json` in the input directory. The run mounts it read-only and records hashes. Additional descriptive keys are ignored. Values are matched to IDs; unknown IDs are rejected.

`forms.json` has this structure:

```json
{
  "schema_version": 1,
  "forms": [{
    "id": "request",
    "title": "School request",
    "instructions": "Select a shaded field to type.",
    "fields": [
      {"id": "details", "label": "Details", "type": "text", "required": true, "max_chars": 160},
      {"id": "confirmed", "label": "Details confirmed", "type": "checkbox", "required": true}
    ]
  }]
}
```

`values.json` maps form IDs to field values:

```json
{"request": {"details": "Morning session\nReturn in the afternoon", "confirmed": true}}
```

Supported boundaries are explicit and enforced by `source/forms.py`:

- From 1 to 20 forms; from 1 to 6 fields in each form.
- IDs start with a lowercase ASCII letter and contain only lowercase letters, digits and hyphens; maximum 40 characters. Form IDs are unique, and field IDs are unique within a form.
- Titles have at most 55 characters; instructions at most 180; labels at most 60. They are nonempty single paragraphs.
- `required` is a JSON boolean. Required means a value must be supplied. A required checkbox may be false: an explicit negative answer is preserved.
- Text `max_chars` is an integer from 1 to 160, including spaces and line breaks. A value may have at most four explicit lines. Empty text is accepted only for optional fields. Optional omitted fields become empty text or an unchecked box.
- Checkbox values must be JSON booleans and omit `max_chars`. Unsupported types, oversized values, invalid JSON and XML control characters produce an error.

The DOCX text controls support multiline entry. Limits are enforced by the pipeline, not by interactive Word-style protection. The forms are not locked: manually entering too much text can exceed the fixed areas. Content must also pass the rendered PDF bounds and text checks; unsupported glyphs or a value that cannot fit produce a failed run. The delivered forms passed these checks in LibreOffice; Microsoft Word was not run.

The pipeline delivers blank DOCX/PDF, filled DOCX/PDF, PNG previews, per-control round-trip records and a report per run. LibreOffice UNO enters values through text cursors inside content controls and the checkbox Checked property, saves and closes, then reopens metadata-cleaned files for inspection and PDF export. Blank files are also exported through LibreOffice so both states use the same DOCX layout settings. Writer adds container wrappers in the XML and does not retain all control aliases/tags; the report records raw wrapper counts separately from leaf fields. Field IDs are mapped by source order and the adjacent labels actually read in LibreOffice, not by retained alias metadata.

`./run.sh --check` inspects an existing complete output set, using the previously built image. `python3 tests/selftest.py` runs the structural negative tests independently with the Python standard library.

For a normal run the only writable persistent location is the selected output directory. Temporary profiles and intermediate conversion jobs live inside the disposable container. Dependencies use the shared pinned recipe in `../harness/Dockerfile`; `container-recipe.json` records the case additions.
