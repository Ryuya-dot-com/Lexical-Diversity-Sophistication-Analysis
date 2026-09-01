# Changelog

No public release has been issued. This file records the current technical
probe without assigning it a release version or validation claim.

## Unreleased

### Added

- Browser-local VPC/VID candidate review from researcher-supplied four-column
  TSV patterns, including discontinuous member/gap display, manual candidates,
  confirmed/rejected/unresolved decisions with required notes, occurrence CSV,
  and metadata-only method JSON.
- A separate authorization/ethics attestation for appropriately governed text
  in the MWE workflow; candidate patterns and raw text remain local and are
  represented in method JSON by SHA-256 identifiers rather than copied text.
- Three project-authored method-audit scenarios for repetition, punctuation-only
  segmentation, and nested length sensitivity.
- Browser-local single-text, researcher-declared-line, paired, independent-two-
  text, and descriptive multi-document workflows.
- Versioned metric, tokenizer, input, warning, retention, and JSON export
  contracts with primary-method citations.
- Per-input SHA-256 identifiers, metadata-only export, explicit rights
  attestation, dual licensing, and an artifact-level resource admission gate.
- Public technical deployment from the canonical repository's `main` root.
- Primary-source screening ledger for frequency, CEFR, academic, morphological,
  semantic, and psycholinguistic resources, including pinned TUBELEX and
  Lancaster candidate artifacts without bundling either dataset.
- Strategic reset making separate word, MWE-form, and MWE-sense coverage the
  product target, with English VPCs as the first automatic scope.
- Primary-source comparison of TAALES n-gram/polysemy behavior and screening of
  OEWN, PHaVE, STREUSLE, and PARSEME for MWE occurrence and sense work.
- Existing-tool boundary covering PARSEME FLAT, INCEpTION, corpus search
  portals, the STREUSLE recognizer, and PyMUSAS: reuse conventions,
  interchange, and measured baselines instead of rebuilding an annotation
  platform.
- MWU Profiler 2.0.1 and Lextutor Phrase Profiler prior-art review, including
  list matching, the former's n-gram/dependency pipeline, hosted-input and
  resource-rights boundaries, and a project-authored `take in`/known-item
  black-box comparison.
- Systematic eight-lane prior-art search protocol with a decision-based stopping
  rule, plus screening of PARSEME 2.0, MAGPIE, SemEval idiomaticity data,
  MWEasWSD, English VMWE annotations, CoAM, and CAIGen.
- Dependency-free MWE occurrence/sense contract and five project-authored M1–M5
  gold cases covering stable token IDs, discontinuous gaps, contextual fixture
  senses, explicit rejection, and separate coverage denominators.
- Pinned Open English WordNet 2025 `take in#v` projection with all 17 candidate
  senses, source hash, attribution/license notices, a standard-library
  reproducer, project-authored M3 assignments, and mandatory sense-decision
  provenance.
- Context-disambiguated M4 pronoun contrast: confirmed comprehension
  `took it in` and rejected locative `took it in the car rather than on the
  bus`, both preserving `it` as a non-member gap.
- Machine-readable reference-profile manifest template separating word,
  MWE-form, and MWE-sense channels while requiring corpus design, preprocessing,
  denominator, rights, artifact identity, validation, and removal evidence.
- M5 `spill the beans` contrast with separate PARSEME `VID`, occurrence status,
  contextual idiomaticity, and fine-grained-sense fields for idiomatic and
  literal uses.
- Standard-library Python evaluator for supplied MWE candidates and an
  all-confirmed surface-list negative control; no model or runtime dependency.
- Pinned, external-only STREUSLE 5.0 VPC/VID benchmark profile with exact
  artifact hashes, fixed train/dev/test strata, target-only scoring, and a
  dependency-free contiguous-lemma baseline. The test floor is exact-span F1
  0.404762 with zero recall on discontinuous and train-unseen occurrences; no
  corpus text or upstream evaluator code is bundled.
- Corrected the shared-task evidence boundary: the PARSEME 2.0 production
  training release has no English directory, so its English trial is retained
  only as a format/method reference rather than represented as a holdout.

### Integrity boundaries

- No account, server analysis, analytics, cookie, database, external model,
  third-party runtime code, automatic lexical-resource lookup, or raw-text
  export. User patterns create review candidates but do not automatically
  confirm MWE status. The admitted OEWN subset is fixture-only and not loaded
  by the UI.
- Server-side storage is not treated as licensing permission; open resources
  remain downloadable, and restricted resources require delivery-specific
  permission even when hidden behind an API.
- Input count and size limits, all-or-nothing batch validation, unique normalized
  IDs, well-formed Unicode checks, and exact client-clock timestamp formatting.
- Exported hashes and timestamps are explicitly non-authenticating; results are
  descriptive and exclude proficiency, quality, authorship, causal, and
  population claims.

### Not yet verified

- Real-browser visual, keyboard, narrow-screen, zoom, and screen-reader behavior.
- Interpretation by representative L2 vocabulary researchers.
- Construct validity, population validity, cross-tool equivalence, public archive,
  release checksums, and citable release metadata.
