# ldfreq open lexical-methods laboratory

Status: static scenario probe; not an MVP or validated measurement release.

Canonical source: <https://github.com/Ryuya-dot-com/Lexical-Diversity-Sophistication-Analysis>

The repository name allows for a broader future direction. The current probe
does not implement a lexical-sophistication score, frequency norm, reference
resource, or TAALES-compatible analysis.

This directory is an independent browser app for auditing how lexical measures
respond to controlled text comparisons. It currently includes project-authored
scenarios for fixed-length repetition, sentence-segmentation invariance, and
nested length sensitivity. It does not score writing, estimate proficiency, or
reproduce TAALES.

These fixed scenarios are the method-audit surface. The initial research
workspace now analyzes one passage, a paired transformation, or two independent
texts entirely inside the browser. It can also describe researcher-declared
non-empty line units within one text while keeping the pooled result separate,
or describe 2–100 researcher-identified documents from a pasted JSON array.
Automatic sentence splitting, group inference, length curves, and external
lexical resources are not implemented.

The target is a free, reproducible open-science tool for L2 vocabulary
researchers. The runtime is plain HTML, CSS, JavaScript, and reviewed JSON: no
account, server analysis, paid API, analytics, database, or parent-directory
dependency.

## Capabilities and non-capabilities

The probe can inspect three synthetic contrasts, including a one-sentence versus
seven-sentence punctuation contrast. In the browser it can describe one text,
researcher-declared non-empty lines, paired or independent texts, and 2–100
documents. It reports tokens, types, simple TTR, and hapax types under one fixed
English ASCII tokenizer, and exports method metadata and SHA-256 identifiers
without raw text. The source, fixtures, contract, citations, rights terms, and
tests are open for audit.

It cannot assess proficiency, CEFR, writing quality, authorship, causal effects,
or population differences. It does not automatically split sentences, run
inferential statistics, pool or rank documents, process non-English vocabulary
generally, or measure lexical sophistication, frequency, coverage, semantics,
or TAALES equivalence. It cannot independently verify input rights, guarantee
device-level erasure, or reproduce an analysis from a metadata-only export when
the exact source text was not separately preserved.

## Run

```bash
python3 -m http.server 8000
```

Open <http://127.0.0.1:8000>. Run the dependency-free checks with:

```bash
python3 -m unittest discover -s tests -v
node tests/verify_contract.mjs
```

Python is only an optional local static-file server; it is not part of the app
runtime. Use localhost or HTTPS because the reproducibility hash uses the native
Web Crypto API.

Original repository material is available under either MIT or CC BY 4.0 at the
recipient's choice; see [`LICENSE.md`](LICENSE.md). Third-party resources are
not included in that grant.

Current unreleased changes and verification gaps are recorded in
[`CHANGELOG.md`](CHANGELOG.md). No version, DOI, or public-release claim has been
assigned to this technical probe. Git text content is normalized to LF for a
stable cross-platform source archive.

## Scope boundary

- Only reviewed, project-authored synthetic text is bundled.
- Browser-local free text is restricted to synthetic or rights-cleared
  published material after an explicit attestation.
- No learner writing, personal data, confidential material, unpublished
  manuscript, upload, URL fetch, cookie, analytics, request-content log, or
  remote model.
- The app writes input only to the live form, requests clearing on page exit,
  and provides a reset control. It cannot guarantee erasure from browser/device
  memory, history, or backups. Exported JSON contains SHA-256 and provenance but
  never the raw text. Its timestamp comes from the client clock; neither the
  timestamp nor hash is a signature, trusted time proof, or proof of authorship.
  Each export also carries the selected relationship meaning, construct claim,
  excluded inferences, limitations, and meanings of its active warning codes.
- Multi-document input uses the browser's native JSON parser, preserves one row
  per declared document, and rejects the entire batch rather than silently
  dropping invalid items. It does not pool, rank, infer groups, or assume rows
  are independent participants. The raw JSON is capped before parsing, and
  unpaired Unicode surrogates are rejected before UTF-8 hashing.
- Raw counts remain descriptive. Higher values do not mean better writing,
  greater lexical knowledge, proficiency, or CEFR level.
- Formula names do not imply numerical compatibility with TAALES, TAALED, or
  another tool.
- Resource-dependent measures remain blocked until the artifact-level gate in
  [`RIGHTS.md`](RIGHTS.md) passes.

## Method evidence

The contract cites [Fergadiotis, Wright, and Green
(2015)](https://doi.org/10.1044/2015_JSLHR-L-14-0280) for sample-length
confounding and validity cautions, and [Zenker and Kyle
(2021)](https://doi.org/10.1016/j.asw.2020.100505) for the simple-TTR definition
and length behavior observed in their L2 argumentative-essay sample. These
sources constrain interpretation; they do not validate this app or justify
population, proficiency, or causal inference.

The scenario design, workspace limits, non-inferences, publication conditions,
and representative-user check are authoritative in [`ROADMAP.md`](ROADMAP.md).
Exact tokenizer, input, retention, and export behavior is frozen in
[`metric_contract.json`](metric_contract.json); scenario provenance and expected
values are in [`samples.json`](samples.json).

## Release status

Do not present this probe as a research-validated product. Before publication,
verify the static app in real browsers and assistive technology, and archive a
citable release containing contracts, fixtures, tests, notices, and checksums.
