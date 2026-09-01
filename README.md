# ldfreq open MWE-aware lexical-coverage laboratory

Status: browser-local word/MWE coverage and review prototype; not a validated measurement release.

Canonical source: <https://github.com/Ryuya-dot-com/Lexical-Diversity-Sophistication-Analysis>

Public technical deployment: <https://ryuya-dot-com.github.io/Lexical-Diversity-Sophistication-Analysis/>

The product target is an independent, open-science application that keeps
ordinary word coverage, multiword-unit form coverage, and sense-level coverage
separate. The current prototype supports browser-local, researcher-reviewed MWE
candidates but is not a validated automatic MWE analyzer. Its primary outcome
remains reference-conditioned coverage with visible denominators; candidate
review is a necessary measurement stage, not the end product.

The repository contains a public MWE review workflow, two admitted browser
reference profiles, a versioned MWE contract, five project-authored M1–M5 gold
fixtures, and a reproducible projection of all 17 Open English
WordNet 2025 senses for `take in#v`. Dependency-free checks verify stable token
IDs, continuous and discontinuous members, gap exclusion, confirmed/rejected
states, separate form and sense lookups, contextual decision provenance, and
visible review numerators and denominators. The UI accepts a small researcher-
supplied TSV of surface-member alternatives, generates continuous or
discontinuous candidates, permits manual member/gap correction, and exports
reviewed occurrences. TUBELEX supplies a separate word-frequency coverage
channel and OEWN supplies confirmed multiword-verb form membership. This is
transparent coding support, not automatic MWE confirmation, a combined
word/MWE score, or validation on learner data.

The M4 fixture explicitly represents the pronoun-object pattern `took it in`:
`took` and `in` are MWE members and `it` is a non-member gap. The same surface
sequence is confirmed in a comprehension context and rejected when `in the car`
is disambiguated by contrast with `on the bus`. This proves the record model,
not automatic parsing.

The first candidate-review scope is English verb-particle constructions
(VPCs), including contiguous and separated realizations such as `take in` and
`take it in`. Occurrence detection, form-inventory lookup, and contextual sense
assignment are different operations. An unresolved or ambiguous sense must not
silently fall back to the most frequent sense or to the form-level result.

Phrasal verbs are not treated as all MWEs. M5 holds `spill the beans` constant
across an idiomatic use and a literal physical-spilling use. Its PARSEME `VID`
category, confirmed/rejected occurrence status, idiomaticity decision, and
fine-grained sense state remain separate rather than collapsing into a generic
`idiom` label. Light-verb constructions and non-verbal idioms remain outside
the executable contract.

The first external occurrence benchmark is a metadata-only offline profile for
STREUSLE 5.0. Its fixed English test projection contains 40 strong VPC/VID
occurrences, including 16 discontinuous occurrences. No corpus text or upstream
code is bundled. A deliberately weak contiguous train-lemma baseline obtains
exact-span F1 0.404762 and zero recall on discontinuous and train-unseen items.

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
coverage reporting. STREUSLE 5.0 is the pinned English occurrence benchmark;
PARSEME 2.0 remains a multilingual method/format comparator because its fixed
production training release has no English directory. Neither is an automatic
runtime dependency.

These fixed scenarios are the method-audit surface. The initial research
workspace now analyzes one passage, a paired transformation, or two independent
texts entirely inside the browser. It can also describe researcher-declared
non-empty line units within one text while keeping the pooled result separate,
or describe 2–100 researcher-identified documents from a pasted JSON array.
Automatic sentence splitting, group inference, length curves, validated MWE/VPC
identification, sense assignment, MWE frequency, and reference-profile
comparison are not implemented. The browser performs only exact, local lookup
against the two named profiles; it does not query an external lexical service.

The target is a free, reproducible open-science tool for L2 vocabulary
researchers. The canonical core remains downloadable and auditable. A server
or server-side resource store is admitted only when an MWE/VPC function cannot
be delivered responsibly in the browser and the exact resource license permits
that use; a database is not treated as a substitute for permission.

## Capabilities and non-capabilities

The prototype can generate VPC/VID form candidates from researcher-supplied
surface patterns, preserve discontinuous members and intervening gaps, accept
manual candidates, record confirmed/rejected/unresolved decisions with notes,
and export occurrence CSV plus metadata-only method JSON. The two starter
patterns are functional examples, not an inventory.

For the same text, the prototype reports TUBELEX word-token and word-type
membership with source counts, frequency per million, competition rank, and
unmatched items. After a researcher confirms an occurrence, it reports OEWN
multiword-verb form membership by occurrence and distinct form. The channels
retain different token units and denominators and are never averaged.

It can also inspect three synthetic contrasts, including a one-sentence versus
seven-sentence punctuation contrast. In the browser it can describe one text,
researcher-declared non-empty lines, paired or independent texts, and 2–100
documents. It reports tokens, types, simple TTR, and hapax types under one fixed
English ASCII tokenizer, and exports method metadata and SHA-256 identifiers
without raw text. The source, fixtures, contract, citations, rights terms, and
tests are open for audit.
With a separately obtained STREUSLE 5.0 checkout, the offline checker also
verifies exact train/dev/test artifacts and reproduces the declared VPC/VID
surface baseline.

It can surface a declared `take in` pattern, including `take it in`, as a
candidate, but it cannot confirm that candidate as a VPC, distinguish it
automatically from a free or directional combination, or disambiguate its
sense. OEWN supplies 17 candidate senses but no contextual choice, frequency,
or L2 pedagogical ranking. Human review remains part of the measurement method.

The active word profile is a deterministic 410,400-form ASCII projection of the
pinned TUBELEX English regex aggregate. Its profile-specific tokenizer uses
NFKC-normalized ASCII letter sequences, so apostrophes and hyphens are
boundaries; its denominator may differ from the MWE-review tokenizer. The active
MWE-form profile is a deterministic 2,847-form projection of OEWN 2025 verb
entries containing multiple ASCII word members. It supplies lexicon membership
and an inventory sense count, not occurrence truth, MWE frequency, category, or
contextual sense. A future exact Leipzig package remains a written-register
contrast; STREUSLE/PARSEME remain evaluation data rather than frequency norms.

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
python3 scripts/evaluate_mwe_predictions.py tests/fixtures/mwe_predictions_surface_baseline.json --check
python3 scripts/check_streusle_v5.py --self-check
```

To reproduce both active reference profiles from the exact source assets
recorded in [`RIGHTS.md`](RIGHTS.md):

```bash
python3 scripts/build_reference_profiles.py PATH_TO_TUBELEX_XZ PATH_TO_OEWN_ZIP --check
```

To reproduce the admitted OEWN subset, download the pinned 2025 JSON release
asset recorded in [`RIGHTS.md`](RIGHTS.md), then run:

```bash
python3 scripts/extract_oewn_take_in.py PATH_TO_ZIP --check resources/oewn_take_in_2025.json
```

To reproduce the external occurrence baseline without copying the corpus into
this repository:

```bash
git clone --depth 1 --branch v5.0 https://github.com/nert-nlp/streusle.git PATH
python3 scripts/check_streusle_v5.py PATH --check --surface-baseline
```

Python is used for offline resource preparation and model-independent evaluation,
and remains outside the app runtime. The included surface-list negative control
evaluates decisions for supplied candidates only; it is not candidate generation,
span detection, or a trained model. The STREUSLE checker is a separate offline
occurrence benchmark and never loads research text into the Web app. Use localhost or HTTPS
because the reproducibility hash uses the native Web Crypto API.

Original repository material is available under either MIT or CC BY 4.0 at the
recipient's choice; see [`LICENSE.md`](LICENSE.md). TUBELEX data retain the
included BSD-3-Clause notice. OEWN projections are separately licensed under
OEWN CC BY 4.0 and the underlying WordNet License. Attribution and source terms
are recorded in each profile and [`RIGHTS.md`](RIGHTS.md).

Current unreleased changes and verification gaps are recorded in
[`CHANGELOG.md`](CHANGELOG.md). No version, DOI, or public-release claim has been
assigned to this technical probe. Git text content is normalized to LF for a
stable cross-platform source archive.

## Scope boundary

- Analysis scenarios contain only reviewed, project-authored synthetic text.
  The separately licensed OEWN projection contains source definitions and
  examples for one lexical entry and is not user or learner text.
- The MWE path accepts researcher-authorized text, including appropriately
  governed learner data, only after an explicit authorization/ethics
  attestation. The legacy basic workspace remains restricted to synthetic or
  rights-cleared published material.
- No text upload, URL fetch, cookie, analytics, request-content log, or remote
  model. The app does not independently establish consent, anonymization,
  institutional approval, or lawful processing.
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
  [`RIGHTS.md`](RIGHTS.md) passes. The active TUBELEX word-frequency and OEWN
  MWE-form profiles pass that gate only for their declared channels; the smaller
  `take in#v` projection remains fixture-only for candidate-sense validation.
  Open resources are versioned downloadable artifacts rather than hidden
  server data, and database storage never makes an unclear license clear.
- A reference result always names one completed resource profile. The app must
  not silently pool registers, substitute a lexicon for a frequency corpus, or
  present TUBELEX, Leipzig, OEWN, STREUSLE, or PARSEME as a universal norm.

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
