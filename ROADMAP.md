# Open lexical-methods laboratory roadmap

Status: scenario architecture and rights gate, reviewed 2026-09-01

This repository is an independent, free, browser-based methods laboratory for
L2 vocabulary researchers. Its job is not to produce one authoritative lexical
score. Its job is to make controlled comparison scenarios, calculation rules,
resource coverage, and invalid inferences inspectable and reproducible.

The current matched pair is one scenario, not the product definition. The app
may eventually cover lexical variety, length sensitivity, tokenization, and
rights-cleared resource-dependent measures. It must remain useful without an
account, payment, server, proprietary API, or access to the parent repository.

## Product shape

The product has two deliberately different surfaces:

1. **Method audit:** fixed, project-authored scenarios expose what a metric
   changes, ignores, and confounds. The current probe implements this surface.
2. **Research workspace:** the initial browser-local workspace applies admitted
   methods to synthetic or rights-cleared published text selected by the
   researcher. The app writes no durable copy and provides explicit/best-effort
   clearing, but cannot guarantee erasure from browser/device memory, history,
   or backups. The JSON export deliberately omits the text, so the researcher
   must preserve the exact source separately and verify it against the exported
   hash.

The workspace must support research questions, not just input-box shapes:

| Workflow | Unit of analysis | Required output | Primary trap | State |
|---|---|---|---|---|
| Describe one passage | One declared text span | Values, denominators, method metadata, source hash | Treating a text property as an author trait | Implemented probe |
| Compare a paired A/B transformation | Matched text pair | Paired differences and documented transformation | Assuming all non-target features were controlled | Implemented probe |
| Compare two independent texts | Document as observation | Per-document values and descriptive difference | Treating two texts as population evidence | Implemented probe |
| Inspect declared units within a text | Researcher-declared non-empty lines plus pooled document | Per-unit values, unweighted min/median/max, pooled value | Confusing aggregation with between-text evidence | Implemented without automatic sentence splitting |
| Describe several texts | One researcher-identified document per row; dependence unspecified | Per-document values and unweighted descriptive distribution | Treating rows as independent participants | Implemented probe |
| Compare groups | Document plus explicit cluster/author/condition structure | Declared estimand and justified uncertainty | Inferring design from labels or filenames | Not admitted |
| Test length sensitivity | Nested prefixes/windows or repeated subsamples | Value-by-length curve and sampling rule | Calling a compositional change a pure length effect | Fixed scenario only |
| Compare resources | Same tokens under two admitted reference resources | Values, coverage, unmatched items, resource metadata | Calling one corpus a universal baseline | Blocked by rights review |

Batch and group workflows come after a stable per-document contract. The app
must never silently convert sentences into independent participants, pool texts
before analysis, or infer a statistical model from uploaded filenames.

## Descriptive multi-document admission

The fifth workspace mode is **descriptive multi-document analysis**, not
automatic sentence splitting or group inference. Sentence boundaries cannot
change the current pooled metrics; automatic splitting would instead choose the
units for a per-unit distribution and therefore import a segmentation policy.
Group labels alone do not establish independent sampling, repeated-measures
structure, or an estimand.

Its implemented contract requires:

- 2–100 researcher-identified documents, at most 1,000,000 UTF-16 code units
  each, 5,000,000 combined, and 6,000,000 in the raw JSON before parsing; input
  order and unique IDs are preserved;
- one provenance statement per document, one explicit relationship/sampling
  note for the batch, and the existing content-scope attestation for every item;
- all-or-nothing validation: malformed items, duplicate IDs, exceeded limits,
  ill-formed Unicode, or a document with zero recognized tokens reject the
  batch and name the item when applicable;
- one result row per document plus unweighted minimum, median, and maximum;
  there is no default pooled score, weighting, ranking, group difference, or
  statistical inference;
- exact per-document UTF-8 hashes, byte counts, method metadata, and warnings in
  the JSON export, while raw text remains excluded;
- fixtures proving equivalence with single-document analysis, stable ordering,
  limit and duplicate rejection, and absence of raw text from the export.

The implemented count and size limits are initial browser resource-safety ceilings,
not linguistic thresholds or data-exclusion guidance. Browser benchmarks must
justify or revise them before release.

Do not infer groups from filenames, directories, labels, or document order. A
later group workflow needs explicit cluster/author/condition identifiers,
missing-data policy, target population, estimand, and uncertainty method. Until
then, multiple rows remain a descriptive collection whose dependence is
unknown.

The locally preserved and Git-ignored `ldfreq_webapp_master_roadmap_20260831.html`
is a non-authoritative inventory for a different MWE/VPC direction. The parent
repository is an evidence vault only. Nothing is copied from it without a
file-level method, provenance, rights, and numerical review.

## Priority order

1. **Research question before metric count.** A scenario must identify the
   comparison relation and the decision it can support.
2. **Identification before interpretation.** Length, segmentation, lexical
   composition, preprocessing, and reference-resource changes must not be
   silently conflated.
3. **Rights before implementation.** A tool license, an algorithm description,
   a corpus license, and permission to redistribute derived tables are four
   separate questions.
4. **Auditability before convenience.** Raw values, formulas, parameters,
   coverage, versions, and exclusions remain visible and exportable.
5. **Open access before feature breadth.** Static browser execution and
   project-authored fixtures are the default. A server or restricted resource
   requires a demonstrated research need and a sustainable free-access plan.

## Multi-lens review

| Lens | Critical question | Current decision |
|---|---|---|
| Research design | What is held constant, manipulated, and left uncontrolled? | Store all three for every scenario and show them before results. |
| Measurement | Is a value a distinct signal or an algebraic restatement? | At fixed token count, Types and TTR are not presented as independent evidence. |
| Text unit | Does “one sentence versus several” change only segmentation, or also length and composition? | Represent invariance and nested-length comparisons as separate scenarios. |
| Construct | Is the app measuring diversity, sophistication, frequency, coverage, or preprocessing sensitivity? | Name the construct per metric; no umbrella “lexical quality” score. |
| External validity | Does a synthetic contrast generalize to L2 learners, genres, or populations? | No. It is a mechanism demonstration until rights-cleared empirical validation exists. |
| Rights | Can code, resources, derived values, and source texts all be redistributed? | Require a resource-level admission record; “free to download” is insufficient. |
| Reproducibility | Can a third party reconstruct the exact value? | Pin formula variant, tokenizer, parameters, resource version, sample provenance, and expected output. |
| Objectivity | Are deterministic numbers neutral or theory-free? | No. “Objective” means transparent and repeatable procedures, not value-free construct choices. |
| Privacy | Must research text leave the device? | No. The initial workspace uses browser memory only, omits raw text from JSON, forbids network APIs in static checks, and restricts connections/forms with CSP. |
| Equity | Does a “free” interface still depend on restricted corpora, modern hardware, or English-only norms? | Keep the core downloadable and resource-free; label language/variety scope and never make restricted add-ons the only serious workflow. |
| Accessibility | Can researchers use and audit the app without a mouse or wide screen? | Native controls and semantic HTML now; real-browser and assistive-technology checks remain required. |
| Sustainability | Can free access survive hosting or maintainer loss? | No database, account, analytics, runtime package, or paid API; downloadable static release is the target. |
| Interoperability | Does matching a metric name imply matching another tool? | No. Numerical equivalence requires an explicit versioned validation study. |

## Scenario matrix

| ID | Comparison | Identified change | Valid observation | Main boundary | State |
|---|---|---|---|---|---|
| S1 | Equal 100-token templates with 38 lexical substitutions | Surface repetition at fixed positions | Mechanical response of counts and TTR | Frequency, semantics, naturalness, and population effects are uncontrolled | Implemented probe |
| S2 | Identical 100-token sequence as one orthographic sentence or seven | Terminal punctuation / segmentation only | Current token-sequence metrics are invariant | This says nothing about sentence-aware metrics or natural syntax | Implemented probe |
| S3 | First 14-token sentence versus its containing 100-token text | Nested sample length plus accumulated continuation | TTR changes when the sample grows | Sentence count, length, and added lexical composition are not separately identified | Implemented probe |
| S4 | Same characters under documented tokenizer policies | Preprocessing policy | Sensitivity to apostrophes, hyphens, case, Unicode, and digits | No tokenizer is universally correct | Fixture evidence only |
| S5 | Same text under an admitted frequency or lexical resource | Reference distribution and coverage | Resource-conditional score and coverage | No resource is a universal English baseline | Blocked by rights and construct review |
| S6 | Rights-cleared public or corpus-derived text strata | Observed group/genre/time differences | Descriptive distribution with uncertainty | No causal, proficiency, or individual diagnosis claim | Blocked by provenance and design review |

The matrix is intentionally small. Add a scenario only when it isolates a new
decision-relevant contrast; do not add scenarios merely to showcase another
index.

## What dimensions 3 and 4 must keep separate

A defensible comparison records at least these independent coordinates:

- text unit: token sequence, sentence, passage, document, or corpus;
- sampling relation: identical, transformed pair, nested prefix, matched but
  non-identical, or independent observation;
- preprocessing: normalization, tokenization, lemmatization, part of speech,
  and sentence segmentation;
- metric family: amount, variety, repetition, frequency/range, dispersion,
  psycholinguistic norm, association, or semantic relation;
- external resource: identity, version, population/genre/time/variety,
  coverage, missing-value policy, and license;
- aggregation: token-weighted or type-weighted mean, quantile, threshold,
  proportion, or distribution;
- inference target: a property of this text under this method, a group
  description, a predictive association, or a causal effect.

The app must refuse or visibly qualify these conclusions:

- a higher value is better writing, greater proficiency, greater knowledge, or
  a higher CEFR level;
- a single-versus-multiple-sentence difference is a sentence-count effect when
  length or lexical composition also changed;
- a resource-dependent value is corpus-neutral, genre-neutral, timeless, or
  complete when coverage is below 100%;
- synthetic examples estimate an effect size in naturally occurring learner
  language;
- equal metric names imply numerical equivalence with TAALES, TAALED, or any
  other tool;
- deterministic output removes theoretical judgment, preprocessing choices,
  sampling bias, or measurement error;
- a descriptive contrast supports causal inference or population
  generalization.

## Rights and resource admission gate

Before a metric or sample enters the browser bundle, record:

1. the independently implemented formula and its primary methodological source;
2. whether any third-party code was copied or adapted;
3. every data/resource dependency and its exact version or retrieval date;
4. permission for redistribution, modification, browser delivery, and derived
   tables—not merely research use or free download;
5. required attribution, notices, ShareAlike or NonCommercial terms;
6. a content hash, coverage definition, missing-value rule, and removal path;
7. an independent numerical oracle and any cross-tool comparison claim.

Admission classes:

- **A — default:** independently implemented resource-free formula plus
  project-authored, openly licensed fixtures.
- **B — reviewable:** resource with explicit redistribution terms compatible
  with free public browser delivery, pinned artifact, and complete notices.
- **C — segregate or omit:** NonCommercial, ShareAlike, academic-use-only, or
  ambiguous resource requiring package-specific legal/maintainer review.
- **D — exclude:** purchased, confidential, no-redistribution, unclear-origin,
  or revoked material.

TAALES is prior art and a methodological reference, not a code or data source.
Its published license and the rights of each bundled corpus/list must be
assessed separately. This project must not claim “TAALES-compatible” output
without a versioned, rights-cleared, independently reproducible comparison.
See `RIGHTS.md` for the current evidence record. This is project governance,
not legal advice.

Rights review also protects relationships, not only files: method/tool authors
receive citation and are not represented as endorsing this app; corpus and list
creators retain their chosen conditions; source-text authors and participants
are not exposed; researchers receive reproducible provenance; and a future host
cannot place the only functional version behind an account or fee. No rights
issue should be framed as evidence of improper conduct by another project.

## Open-science release gate

- [x] Dual-license original code, documentation, contracts, and fixtures under
  MIT or CC BY 4.0 at the recipient's choice.
- [ ] Keep future third-party notices and any license-incompatible resource
  packages distinct from the original project grant.
- [ ] Publish source, static build, contracts, fixtures, tests, citations,
  release checksum, changelog, and a citable archived release together.
- [x] Keep the current core usable from a local static server, without
  login, payment, analytics, cookies, proprietary API, or text transmission.
- [x] Implement single, paired, and independent-two-text browser-local analysis
  after defining its per-document data model, limits, rights attestation, CSP,
  no-storage boundary, and metadata-only export contract.
- [x] Export method/version/parameter/resource identifiers with every result;
  never export only a score column.
- [x] Make each JSON record self-describing for its relationship, construct
  claim, excluded inferences, limitations, and active warning meanings.
- [x] Bind each current non-project-defined metric claim and its interpretation
  limit to DOI-addressed methodological evidence in the contract and export.
- [x] Admit researcher-declared non-empty line units only after making pooled
  and per-unit values distinct and warning against pseudoreplication.
- [x] Admit descriptive multi-document JSON only with unique document IDs,
  all-or-nothing validation, per-document hashes, unweighted summaries, and no
  pooled score or assumed independence.
- [ ] Admit automatic sentence segmentation, group, or statistical workflows
  only after their observation unit and error modes are independently reviewed.
- [x] Document governance for corrections, resource removal, deprecation, and
  reproducibility of older releases.
- [ ] Test keyboard, narrow-screen, contrast, and screen-reader behaviour in
  real browsers.
- [ ] Run the scenario interpretation check with representative L2 vocabulary
  researchers before calling the app an MVP.

**Release gate:** a third party with only the archived release can reproduce a
displayed value, identify all rights and method dependencies, and state what the
comparison does not establish. Free access alone does not pass this gate.

## Correction and version governance

- Never replace an archived release in place. A correction gets a new version,
  date, changelog entry, and checksums; the entry names affected versions and
  whether values, interpretation, provenance, rights, or only presentation
  changed. Rights or participant-protection duties may require withdrawing an
  archive, but its identifier must not be reused for altered contents.
- If a bundled resource must be withdrawn, stop distributing it in new releases
  and, when necessary, withdraw affected archives. Retain only a lawful
  metadata tombstone containing its identifier, version, hash, removal reason,
  date, and affected methods; do not retain the artifact when deletion is
  required.
- Deprecation must be visible in the interface, contract, and export before
  removal. New analyses must not silently substitute a replacement formula,
  tokenizer, resource, or default under the old identifier.
- Older results are interpreted with their exported schema, contract, method,
  and resource versions. Compatibility code is added only for a demonstrated
  migration need; otherwise the immutable archived release is the executable
  reference.
- Browser-generated records are editable files. Their content hashes identify
  declared text bytes and their timestamps report the client clock; neither is
  authentication, authorship evidence, or trusted time attestation.
- A reproducible release contains the exact source tree, contracts, fixtures,
  tests, licenses/notices, citations, changelog, and a checksum manifest. A DOI
  or repository tag identifies that immutable bundle, not the mutable website.

## Release packaging sequence

1. Pass the real-browser and representative-researcher gates; freeze a version
   and move the relevant `CHANGELOG.md` entries out of `Unreleased`.
2. Confirm creator names, repository URL, release date, version, license choice,
   and archive identifier before writing citation metadata. Do not invent or
   preassign a DOI.
3. Tag the exact tracked source tree. The static app has no build product: archive
   the source, contracts, fixtures, tests, licenses/notices, citations, and
   changelog together.
4. Compute SHA-256 after the archive is final, publish the archive and checksum
   together, and never reuse the version or identifier for altered bytes.
5. Extract the published archive into a clean directory, run its documented
   checks, serve it locally, repeat the acceptance gate, and verify that no
   parent-directory or ignored evidence-vault file entered the bundle.

No packaging script is justified before the first version is frozen; the first
release exercise should reveal whether a repeated automation need actually
exists.

The initial tracking audit on 2026-09-01 found this directory to be the Git root
with no symlinks, file over 1 MB, or high-confidence credential signature in the
candidate source files. The local snapshot was merged with the one-line GitHub
placeholder history and pushed to the canonical repository's `main` branch;
the repository CI passed. The ignored legacy MWE/VPC roadmap and Python caches
are not tracked release inputs, and LF is normalized by `.gitattributes`.
Public source availability is not a tag, citable archive, security
certification, browser acceptance, research validation, or formal release.

The canonical repository name includes “Sophistication” as a possible future
direction. The current admitted construct remains surface lexical amount,
variety, repetition, and method sensitivity; no sophistication score or
resource-dependent measure is implemented.

## Representative-user interpretation check

For each scenario, ask at least three L2 vocabulary researchers, without verbal
coaching:

1. What exactly was held constant and changed?
2. Which apparent variables remain confounded?
3. Which result is algebraically dependent on another?
4. What population, quality, proficiency, or causal claim is not supported?
5. What method/resource metadata would be needed to reproduce the value?

Three users can expose obvious interpretation failures; they do not validate
the construct or generalize usability. Record anonymous task outcomes only and
do not add analytics.

## Pending real-browser acceptance gate

The required in-app browser connection was unavailable on 2026-09-01, so
structural checks and actual HTTP delivery passed but visual and assistive-
technology claims remain unverified. Before release, run this exact manual gate
in current Chromium, Firefox, and Safari plus at least one screen reader:

1. Reach every control by keyboard, see focus, change all five modes, and return
   to the scenario selector without a trap.
2. Analyze one text; verify the displayed value and 64-character SHA-256 against
   the saved JSON, then confirm that the JSON contains no source text.
3. Analyze three declared lines with one blank line; verify three rows, pooled
   values, min/median/max, and the non-independence warnings.
4. Analyze three JSON documents; verify input order, per-document hashes,
   unweighted summary, and absence of an A/B difference. Duplicate IDs, a
   zero-token document, or one malformed item must reject the whole batch.
5. Analyze equal-length paired texts and unequal-length independent texts;
   verify the correct algebraic-dependence or cross-length warning.
6. Change input while a large analysis is running; stale results must not appear.
7. Reset, navigate away/back, and reload; verify the app does not deliberately
   restore text while documenting any browser-managed restoration behavior.
8. At 320 CSS pixels and 200% zoom, verify labels, textareas, table scrolling,
   buttons, hashes, and warnings remain operable without hidden content.
9. Inspect the network panel: only the page, `app.mjs`, `metrics.mjs`, and the two
   reviewed JSON files may load; analysis and export must add no request.

Failure of any item blocks an MVP claim; it does not justify adding a framework.

## Ponytail disposition

Keep the app as static HTML, CSS, JavaScript, JSON, and dependency-free checks.
Do not add R, FastAPI, Plumber, a database, accounts, queues, caches, containers,
or external models until an admitted scenario cannot run transparently and
freely without them.
