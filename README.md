# ldfreq open MWE-aware lexical-coverage laboratory

Status: static scenario probe; not an MVP or validated measurement release.

Canonical source: <https://github.com/Ryuya-dot-com/Lexical-Diversity-Sophistication-Analysis>

Public technical deployment: <https://ryuya-dot-com.github.io/Lexical-Diversity-Sophistication-Analysis/>

The product target is an independent, open-science application that keeps
ordinary word coverage, multiword-unit form coverage, and sense-level coverage
separate. The current probe is only the browser-local input, comparison,
provenance, and export foundation for that target; it is not yet an MWE analyzer.

The repository now also contains a non-UI MWE contract, four project-authored
M1–M4 gold fixtures, and a reproducible projection of all 17 Open English
WordNet 2025 senses for `take in#v`. Dependency-free checks verify stable token
IDs, continuous and discontinuous members, gap exclusion, confirmed/rejected
states, separate form and sense lookups, contextual decision provenance, and
visible coverage numerators and denominators. This is resource-backed contract
evidence, not automatic MWE detection or validation on learner data.

The M4 fixture explicitly represents the pronoun-object pattern `took it in`:
`took` and `in` are MWE members and `it` is a non-member gap. The same surface
sequence is confirmed in a comprehension context and rejected when `in the car`
is disambiguated by contrast with `on the bus`. This proves the record model,
not automatic parsing.

The first automatic linguistic scope is English verb-particle constructions
(VPCs), including contiguous and separated realizations such as `take in` and
`take it in`. Occurrence detection, form-inventory lookup, and contextual sense
assignment are different operations. An unresolved or ambiguous sense must not
silently fall back to the most frequent sense or to the form-level result.

The closest existing user-text profiling applications found in the current
review are Masaki Eguchi's Multi-Word Units Profiler and Lextutor Phrase
Profiler. The former uses n-gram and dependency candidates to highlight entries
from several research-based MWU lists; the latter matches text against selected
phrase/collocation lists. FLAT/PARSEME is the closest collaborative MWE
annotation workflow. This project will reuse those precedents instead of
rebuilding them. Its distinct job is to attach reviewable VPC decisions to
separate, auditable word/MWE-form/MWE-sense coverage channels.

Prior art is reviewed by task rather than by product name: discovery,
list-conditioned profiling, occurrence identification, annotation, contextual
idiomaticity, fine-grained sense assignment, L2 pedagogical priority, and
coverage reporting. The latest PARSEME shared task and open contextual corpora
are benchmark candidates, not automatic runtime dependencies.

These fixed scenarios are the method-audit surface. The initial research
workspace now analyzes one passage, a paired transformation, or two independent
texts entirely inside the browser. It can also describe researcher-declared
non-empty line units within one text while keeping the pooled result separate,
or describe 2–100 researcher-identified documents from a pasted JSON array.
Automatic sentence splitting, group inference, length curves, MWE/VPC
identification, sense assignment, and runtime lexical-resource lookup are not
implemented. The OEWN projection is exercised only by the non-UI gold checks.

The target is a free, reproducible open-science tool for L2 vocabulary
researchers. The canonical core remains downloadable and auditable. A server
or server-side resource store is admitted only when an MWE/VPC function cannot
be delivered responsibly in the browser and the exact resource license permits
that use; a database is not treated as a substitute for permission.

## Capabilities and non-capabilities

The probe can inspect three synthetic contrasts, including a one-sentence versus
seven-sentence punctuation contrast. In the browser it can describe one text,
researcher-declared non-empty lines, paired or independent texts, and 2–100
documents. It reports tokens, types, simple TTR, and hapax types under one fixed
English ASCII tokenizer, and exports method metadata and SHA-256 identifiers
without raw text. The source, fixtures, contract, citations, rights terms, and
tests are open for audit.

It cannot yet identify `take in` as a VPC, distinguish it from a free or
directional combination, recover separated members, or disambiguate its sense
from unannotated user text. OEWN supplies 17 candidate senses but no contextual
choice, frequency, or L2 pedagogical ranking. The implemented MWE fixtures
exercise reviewed gold records only; the public interface still exposes no MWE
workflow.

It also cannot assess proficiency, CEFR, writing quality, authorship, causal
effects, or population differences; measure TAALES equivalence; independently
verify input rights; guarantee device-level erasure; or reproduce an analysis
from a metadata-only export when the exact source text was not separately
preserved.

## Run

```bash
python3 -m http.server 8000
```

Open <http://127.0.0.1:8000>. Run the dependency-free checks with:

```bash
python3 -m unittest discover -s tests -v
node tests/verify_contract.mjs
```

To reproduce the admitted OEWN subset, download the pinned 2025 JSON release
asset recorded in [`RIGHTS.md`](RIGHTS.md), then run:

```bash
python3 scripts/extract_oewn_take_in.py PATH_TO_ZIP --check resources/oewn_take_in_2025.json
```

Python is only an optional local static-file server; it is not part of the app
runtime. Use localhost or HTTPS because the reproducibility hash uses the native
Web Crypto API.

Original repository material is available under either MIT or CC BY 4.0 at the
recipient's choice; see [`LICENSE.md`](LICENSE.md). The OEWN projection is
separately licensed under OEWN CC BY 4.0 and the underlying WordNet License;
its attribution and source notices are recorded in the resource and
[`RIGHTS.md`](RIGHTS.md).

Current unreleased changes and verification gaps are recorded in
[`CHANGELOG.md`](CHANGELOG.md). No version, DOI, or public-release claim has been
assigned to this technical probe. Git text content is normalized to LF for a
stable cross-platform source archive.

## Scope boundary

- Analysis scenarios contain only reviewed, project-authored synthetic text.
  The separately licensed OEWN projection contains source definitions and
  examples for one lexical entry and is not user or learner text.
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
  [`RIGHTS.md`](RIGHTS.md) passes. The admitted OEWN projection passes that gate
  only for non-UI `take in#v` candidate-sense validation. Open resources are
  preferred as versioned, downloadable research artifacts; server-only storage
  is considered only for a separately permitted resource and never makes an
  unclear license clear.

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

Do not present this public technical deployment as a research-validated product
or formal release. Before assigning a version or recommending research use,
verify the static app in real browsers and assistive technology, and archive a
citable release containing contracts, fixtures, tests, notices, and checksums.
