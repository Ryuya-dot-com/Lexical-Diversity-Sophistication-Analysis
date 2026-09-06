# Changelog

No public release has been issued. This file records the current technical
probe without assigning it a release version or validation claim.

## Unreleased

### Fixed

- Stop open-text evaluation when gold contains an unresolved occurrence candidate,
  enforcing the existing adjudicated-reference requirement. Unknown occurrence
  truth can no longer be treated as a negative calibration target or a correct
  rejection. Preserve unresolved exports and prediction-side candidates without
  relabeling or dropping them; supplied-candidate scoring and distinct sense
  ambiguity/abstention states are unchanged. This guard does not certify that
  discovery or adjudication is complete.
- Validate gold token IDs and one-based contiguous positions before open-text
  scoring. Apply the existing predicted member/gap rules to gold occurrences
  as well, rejecting missing, duplicate, unordered or unknown members and
  incomplete gaps instead of scoring malformed reference spans. This checks
  structural alignment, not source-text identity or annotation correctness;
  valid scores, metric formulas and schemas are unchanged.
- Refuse existing annotation-converter output paths using exclusive file creation,
  protecting raw inputs and previous results, including hard links and symbolic
  links. Serialize validated results before creating the output; command-line
  help and collision errors request a new path. This prevents overwrite, not
  partial new files after a write failure or interrupted run.
- Bind converted annotation content to its raw-export hash: reject a parsed
  document that differs from the supplied UTF-8 JSON bytes, then convert the
  independently parsed raw object. Preserve harmless JSON formatting differences
  while hashing the exact original bytes; numeric/boolean substitutions are not
  treated as equal. This establishes input consistency, not authorship or a
  trusted timestamp. The converter API and output schema are unchanged.
- Preserve rejected-occurrence idiomaticity through annotation export conversion,
  emitting null form/sense records for rejected and unresolved occurrences as
  required by the MWE contract. Reject incompatible lookup/assignment states and
  whitespace-only decision notes. Synthetic conversion-to-evaluation checks retain
  gaps and literal negatives; they do not establish live-platform interoperability
  or independent annotation quality. No schema or metric definition changed.
- Reject invalid explicit evaluation modes instead of silently selecting
  supplied-candidate scoring. Keep omitted-mode legacy inputs compatible, and
  load the default open-text metric contract only when no contract is supplied;
  an explicitly empty contract no longer gets replaced. The command line rejects
  non-object metric-contract files without emitting a result. Valid results and
  metric definitions are unchanged.
- Validate gold sense records before scoring in both evaluation modes. Reuse
  the open-text prediction cardinality checks so malformed assigned, joint or
  ambiguous reference sets cannot disappear from the denominator. Reject absent
  confirmed sense records, invalid IDs/states and incompatible lookup or occurrence
  states without repairing them. This checks scoring inputs, not inventory
  provenance or semantic correctness; formulas and schemas are unchanged.
- Reject duplicate gold document/occurrence IDs in supplied-candidate evaluation
  and duplicate gold occurrence IDs in open-text evaluation; input rows can no
  longer be silently overwritten by ID. Check all seven sense states against
  their occurrence, canonical-form and eligible-reference denominators, including
  empty reference sets and missing predictions. Formulas and schemas are unchanged.
- Accept idiomaticity judgments on rejected occurrences in open-text evaluation,
  as already required by the annotation and metric contracts. Retained literal
  negatives can now be scored without falsely confirming an MWE. Unresolved
  candidates still cannot carry idiomaticity conclusions, and non-confirmed
  occurrences still cannot carry sense decisions. No metric or schema changed.
- Require nonblank text provenance and notes for recorded MWE, idiomaticity
  and sense decisions; undecided states retain null decisions. Reject malformed
  values on save, export and resume instead of accepting values the UI coerces
  into text. Check all seven sense states through JSON and document-set resume,
  keeping ambiguous, abstained and out-of-inventory decisions out of assigned
  coverage. Valid records and file schemas are unchanged; no automatic judgments.
- Cross-check all 17 runtime `take in` senses against the hybrid candidate seed
  by source sense ID, release/artifact identity, synset/ILI, definitions,
  examples and unmerged source-member rows. Matching source copies does not
  admit reserved project senses or validate contextual polysemy. No inventory,
  runtime behavior, source data or schema is changed.
- Request the browser's native leave/reload confirmation while raw drafts,
  an open review, basic-analysis results or a document set remain in memory.
  Remove the listener when work is cleared; canceling exit does not reset it.
  Downloads do not prove file-save completion, so they do not suppress the
  warning. The warning is browser-dependent and is not autosave or recovery;
  no storage, network route, dependency or file-schema change is added.
- Confirm candidate deletion and judgment-reset/status changes before discarding
  recorded decisions or affected drafts. Canceling preserves model and controls
  without advancing the save revision. Removed the UI-only idiomaticity gate
  that hid otherwise valid contextual-sense records and rebuilt sense drafts:
  the two judgments remain independent after occurrence confirmation, including
  save/resume. No annotation state, metric, or file schema is changed.
- Preserve the verified local BNC/COCA profile when a replacement fails, and
  refuse profile replacement while a review is open. Share resume-file reading
  and route wrong-kind files to the correct input. Show Japanese recovery
  guidance for read, JSON, and validation failures without exposing internal
  validator messages. Existing size/hash/resource checks and all-or-nothing
  document-set validation remain in force; no file repair or schema change.
- Keep document IDs fixed after opening a saved set entry, not only after adding
  one. Reject an attempted ID change at the save boundary as well. Display the
  active document and its in-memory update state separately from action
  messages; reflect name edits and normalized saved metadata. Clarified that
  selecting another entry does not switch reviews and that the current review
  must be explicitly cleared before opening another. File schemas are unchanged.
- Snapshot mutable MWE inputs before asynchronous hashing and validation, and
  reject stale UI results after edits, reset/clear, extraction, or a newer
  import. Late saves cannot resurrect a cleared set or mark newer judgments
  as saved; stale import errors and cleanup cannot overwrite newer results.
  Independent exports remain available, with unchanged file schemas and no
  added dependencies or persistence. Added deterministic delayed-operation
  regressions alongside the existing save/resume checks.
- Added a pending-edit list with return-to-field controls and a shared check
  across judgment-bearing exports and document-set saves. It compares current
  edits to recorded values rather than treating unresolved candidates or
  recorded abstention as incomplete work. Explicit MWE/basic-workspace resets
  now ask before discarding work; cancellation preserves the current state,
  while page-exit cleanup remains dialog-free. No automatic judgments, draft
  storage format, persistence service, or publication change is introduced.
- Stopped individual review commits and candidate additions/removals from
  rebuilding the entire occurrence list and token picker. Unrelated drafts,
  expanded sense choices, and manual token selections now remain in place;
  same-status note edits preserve sibling review sections. Focus stays on the
  applicable review action after a status change and moves to a surviving
  control after deletion. Unrecorded drafts are still not part of exports.
- Protected existing and restored MWE reviews from repeated extraction or form
  submission. Clarified human-confirmed versus unresolved states, result versus
  raw-content resume exports, quoted notes in method JSON, and in-memory sets
  versus downloaded files. Added an exact public-path-set check and a Pages
  exclusion for `research_data/`; no server, account system, resource admission,
  data collection, or public deployment is introduced.
- Closed the inventory-review readiness bypass: nonempty `frozen` metadata
  can no longer enable template output or review-file processing. Both remain
  unavailable until a versioned usage-cluster contract and validator exist;
  file existence or a matching hash alone does not establish readiness.
  Synthetic self-checks still run. No cluster format, judgment, admitted sense,
  protocol revision or application change is introduced.

### Added

- Added offline contextual-contrast preparation that imports the unchanged
  SimpleWiki verifier. It verifies all 507 cached revision identities in the pool
  before querying the fixed three-form pool and emits only candidate positions
  and a deterministic first-20-page prefix per form. The source-purpose and
  exposure extensions preserve the stopped Route 2, all prior records and
  sealed-test exclusions. No article text, semantic label or runtime app change
  is included; context continuity and individual publication rights remain
  separate checks. Regression testing required a separate small command because
  the primary preprocessing contract pins the legacy extractor's complete hash;
  that extractor and contract are preserved byte-for-byte.
- Added a deterministic IR-136 usage-pair pilot before expert inventory review.
  The standard-library builder indexes all 54 matching STREUSLE train/dev
  occurrences for the nine frozen forms, excludes test, and produces 51
  connected within-form pairs without bundling sentence text. The review
  protocol now requires blinded usage judgments and provisional cluster
  diagnostics before lexicographers map source candidates to project senses;
  the review checker refuses to issue real templates until that cluster
  artifact is hash-bound. No judgment, cluster, or admitted sense is claimed.
- Revised the IR-136 inventory-review protocol to audit polysemy before human
  review. The checker now verifies the 56/11 VPC/VID imbalance, 387 possible
  candidate pairs, five gloss-only candidates, and absence of context; review
  fields separate source coverage, form relation, construction scope, and a
  retained-candidate partition. Raw reviews remain in managed storage and no
  human judgment, contextual-polysemy result, adjudication, or admitted sense
  is claimed. The inventory generator now reads the current contract version
  instead of emitting a stale constant, restoring byte-for-byte reconstruction
  against the pinned OEWN archive.
- Extended the existing hash-verifying STREUSLE checker with the frozen IR-221
  gap/dependency baseline instead of adding another runner. Train supplies
  lemma types and supported dependency arcs; development fixes a two-token gap
  and five-example relation threshold. Development discontinuous recall is
  8/14 and exact-span F1 rises from 0.316832 for the lemma-window ablation to
  0.426667 after dependency filtering. The optional audit emits rule IDs,
  evidence token numbers, and dependency arcs without sentence text. The
  exposed STREUSLE test result remains development evidence, and unseen-type
  recall remains zero.
- Reclassified IR-115 from a current P0 blocker to a conditional pre-human-work
  gate. Commissioned annotation is separated from research about annotators;
  accounts, logs, and payment no longer trigger ethics review by themselves,
  while work-product rights, fair payment, security, and retention remain
  mandatory. The GSICS checklist map now applies only if the later activity is
  a survey or experiment involving humans.
- Added a provisional INCEpTION platform decision and a dependency-free UIMA
  CAS JSON converter. Its synthetic self-test preserves discontinuous members
  and gaps, multiple selected senses, OOI, and input/converter hashes; live
  two-user isolation and audit acceptance remain blocked pending an approved
  institutional deployment.
- Added a public synthetic-only annotator training protocol that stages teach-
  back, guided practice, feedback, hard cases, and qualification. Five tasks
  have separate item minima and pass rules, critical boundary errors cannot be
  averaged away, and one failed-task retraining/retry is allowed. No form has
  been administered and no human qualification evidence is claimed.
- Added a public, wholly synthetic hard-case bank with at least two cases for
  each prespecified span/context error stratum, explicit admissible routes and
  rationales, and per-case redistribution records. It is training/QA material,
  not benchmark gold or annotator qualification evidence.
- Separated one-sense assignment, jointly applicable senses, unresolved named
  alternatives, human abstention, semantic out-of-inventory, administrative
  inventory ineligibility, and unfinished work across the guide, browser UI,
  export validation, and benchmark metrics. Sense-set accuracy and assignment-
  state accuracy are now reported independently.
- Defined the standalone idiomaticity module with separate category and sense
  decisions, explicit compositional, figurative-but-compositional,
  conventionalized, ambiguous, and not-assessed routes, candidate-origin
  separation, and a loss-aware MAGPIE binary projection. This remains synthetic
  document/software evidence and does not authorize human annotation.
- Added a tested GitHub Pages exclusion for `internal/` and removed the obsolete
  ignored root-level roadmap copy so internal planning language is not part of
  the public site build. The public repository and delivered website remain
  distinct release surfaces.
- Added the IR-141 occurrence/span/category module and 12 project-authored
  synthetic training cases. Ordered VPC and VID tests, tokenization exceptions,
  overlap, inflection, particle movement, pronoun/NP gaps, literal/spatial and
  accidental negatives, continuous/discontinuous spans, and 13 first-cause
  disagreement codes now have one dependency-free consistency check. No human
  training, qualification, agreement, or natural benchmark evidence is added.
- Added the IR-140 standalone annotation-guide skeleton. Eight ordered sections
  cover candidate-independent search, occurrence, spans, category,
  idiomaticity, inventory, contextual sense, and uncertainty; all current
  contract states and M1–M5 fixtures have a dependency-free coverage check.
  Detailed hard cases, human training, and independent reliability evidence
  remain future IR-143 through IR-147 work under the applicable annotation-work
  or human-study route.
- Added the IR-135 hybrid inventory coverage v2 audit over all 624 STREUSLE
  targets/389 types and the full 52-occurrence/14-type VID pilot. It reports
  category, continuity, split, candidate-count, unresolved, and unassessed OOI
  states using full denominators, and holds all sense claims at zero admitted
  and zero contextually assessed occurrences.
- Added the IR-134 synthetic lifecycle exercise and public inventory-governance
  procedure. Hash-fixed old/new versions cover split, merge, deprecated-source,
  and new-OOI-sense cases while preserving every old ID and annotation; all
  migrations remain explicit and manual, and post-test changes require a new
  major benchmark version.
- Added the IR-133 Draft 2020-12 inventory schema and append-only registry
  checks. Candidate/formal sense records now carry explicit lifecycle
  relations; cross-artifact type IDs, project sense IDs, and source-sense
  identities are collision-tested. `--prior` regeneration preserves IDs across
  source reordering/addition and fails before silently deleting an old sense.
- Added the IR-132 fixed 14-type VID population pilot. The prose-free log spans
  exact OEWN, fixed-slot OEWN, exact Kaikki, nonexact, and no-route states;
  records 52 training occurrences/21 discontinuous occurrences; and reports 2
  unresolved types without treating them as OOI. Five OEWN-routed VID forms
  extend the candidate seed to 9 forms/67 candidate senses, with zero formal
  admissions and no runtime integration.
- Added the IR-131 OEWN candidate seed for the four previously exposed
  training/development VPC forms. It reserves stable project IDs for all 56
  source senses and records source fingerprints, CILI/ILI, verbatim
  gloss/example rights, and unmerged synset-member relations. No project sense
  is admitted and nothing is loaded by the Web app pending independent review.
- Added the reproducible IR-130 bounded nonexact VID mapping queue and review
  guide. The fixed OEWN/Kaikki scan retains all 146 exact misses, yields closed
  candidate sets for 3 types, and stops 143 as `unresolved/no_bounded_route`;
  none is promoted to a mapped sense or OOI. Raw source records remain ignored,
  source wording is omitted, and the projection carries STREUSLE,
  Wiktionary/Kaikki, and OEWN/WordNet notices.
- Added a prospective planning-pilot addendum that resolves the IR-121/IR-147
  design conflict without selecting data. Target-enriched training material is
  separated from a target-blind Wikipedia planning prefix; the latter must be
  budget-frozen before target exposure, fully annotated, logged as exposed
  development evidence, and permanently excluded from the sealed test.
- Added the IR-127 pre-data precision plan, standard-library allocation
  simulator, and synthetic checks. The 0.05 overall and 0.10 single-stratum
  gates are fixed, but no sample size is reported: observed pilot inputs are
  absent and the accepted target-blind planning-pilot route is not yet active.
- Added the IR-126 fixed-seed cluster-bootstrap engine and synthetic checks.
  Whole documents are resampled within length strata, canonical types form a
  separate sensitivity analysis, and system differences share paired draws.
  Overall and frozen single-axis strata reuse one function; sparse clusters and
  undefined replicates yield point estimates without inferential claims.
- Frozen task-specific benchmark metric contract and executable point-estimate
  checks for IR-125. Candidate, span/token, category, idiomaticity, inventory,
  sense, ambiguity, abstention, burden, conditional calibration, and selective
  prediction remain separate; every metric names its input, denominator,
  undefined state, and document bootstrap unit, and a combined score is
  forbidden. No source row, prediction result, or validation claim was added.
- Completed the current-repository exposure audit for IR-124. The public ledger
  now classifies STREUSLE, the WSD slice, dictionary candidates, SimpleWiki,
  VOA, TECO, Gutenberg, MAGPIE, MWEasWSD, and synthetic results without copying
  source or participant data. It defines per-test-item and model-experiment
  records, treats unknown access as exposed, and records zero project test items
  and zero contextual/probabilistic model experiments.
- Frozen document-level split and sealing protocol for IR-123, plus an initial
  append-only exposure ledger. A separate hash assigns 20% guide training, 10%
  annotation pilot, 20% development, and 50% sealed test within each length
  stratum. STREUSLE's 40 test occurrences, the WSD slice's 17 source-test rows,
  and dictionary candidates remain exposed external evidence; no project test
  or custodian currently exists.
- Pre-data evaluation-strata and cluster contract for IR-122. Category,
  continuity, form exposure, variant, source genre, and sampling length receive
  fixed definitions; each main claim has a denominator and document/canonical-
  form cluster boundary. Underpowered strata remain descriptive, and item-level
  independence plus a combined score are forbidden.
- Target-blind Wikipedia sampling-frame contract and standard-library priority-
  queue builder for IR-121. Content-neutral eligibility, document hierarchy,
  three length strata, seed/hash ordering, inclusion-probability formula, and
  same-stratum replacements are frozen and checked with synthetic metadata.
  No source row or document was selected; allocation remains an IR-127 gate.
- Pre-data research and data-governance controls for IR-115. Static development
  and public-source preparation may proceed; independent annotation, intended-
  user research, and participant-level secondary use remain held for a written
  institutional determination. Restricted person-level data, identifiers, and
  linkage records are excluded from Git, GitHub Pages, and API responses.
- Downstream-selection memo closing the first-paper choice with no application
  selected. Eye tracking, comprehension, learner text, source recurrence, and
  broad coverage remain separate optional studies; none validates the core
  VPC/VID labels or creates a Web-app/API data dependency. TECO author contact
  is retained only as a non-blocking rights clarification.
- Pre-data benchmark card and data statement distinguishing source, sampling,
  annotation, target, and evaluation populations. Unknown sample, annotator,
  split, result, release, and maintenance fields remain explicit release gates.
- Frozen source identity and preprocessing contract for the completed
  2026-09-01 English Wikipedia dump. Exact recombined filenames, bytes, official
  checksums, render/extraction stages, stable IDs, and character/UTF-8 byte
  traces are pinned without downloading or target-searching source content.
- Standard-library standoff/reconstruction prototype over one project-authored
  fixture. It verifies exact source bytes, reproduces stable document, token,
  and occurrence IDs with character/UTF-8 byte offsets, validates gaps, and
  fails closed on a same-length source change. It acquires no Wikipedia text
  and is not benchmark-availability evidence.
- Release-layer manifest covering every current public file with source,
  license, notice, and redistribution state. Five ordered rules preserve the
  TUBELEX, NGSL, OEWN/WordNet, and CC-BY-only exceptions; future benchmark and
  model layers stay excluded until their file-specific rights gates pass.
- Pre-acquisition core benchmark source decision. It selects namespace-0
  English Wikipedia article revisions from one completed dated dump and a
  CC BY-SA 4.0 public-text plus standoff/reconstruction route. Page-level
  notice review, exact source identity, target-blind sampling, and clean-room
  reconstruction remain required; no source text was acquired or searched.
- Frozen English VPC.full/VPC.semi/VID target-population contract and the
  initial scope-only annotation-guide module. They define candidate-independent
  discovery, inflection, separation, gaps, overlap, literal negatives,
  misspellings, excluded categories, and PARSEME 1.2/2.0 label correspondence
  without prematurely supplying the full training or adjudication guide.
- Append-only governance decision log with required before/after, rationale,
  affected-task, reevaluation, version, and sealed-test fields. Its first two
  records preserve the internal-roadmap visibility decision and adoption of the
  machine-readable claim map; neither changes a test or research result.
- Machine-readable claim–evidence–artifact map that assigns each retained claim
  to one evidence category and records its current wording ceiling, scoped
  evidence, required release artifacts, and prohibited inferences. It preserves
  the present demonstration ceiling and does not promote exposed development
  evidence, software tests, or downstream results into validation.
- Bounded exact Kaikki/Wiktionary follow-up for the 206 VID types left after
  OEWN exact/slot lookup. Sixty types receive an exact English verb entry, but
  all three routes together cover only 93/239 VID types and 150/319
  occurrences; only 28 types expose multiple candidates. Just 5/99 raw senses
  have a Wiktionary `senseid`; only one matched type has complete lexicalized-
  sense IDs, with no raw `id` or Wikidata ID. The 206 small responses remain
  ignored/local; the committed audit is aggregate-only and
  rejects direct Wiktionary-as-gold while motivating a project-stable hybrid
  inventory contract.
- LRE full-length submission gate and reproducible STREUSLE–OEWN inventory
  coverage audit. All five publication dimensions remain blocked or only
  partly ready. Across 624 VPC/VID occurrences, OEWN exact lookup covers 317,
  but only 45/319 VID occurrences and 31/239 VID types; simple article/slot
  normalization leaves 265 VID occurrences and 206 VID types unmatched. This
  triggers a bounded rights/schema/coverage audit of a dated Wiktionary-derived
  inventory, not immediate integration, human annotation, or a contextual
  model.
- Bounded existing-corpus search and reproducible standard-WSD multiword-verb
  audit. A hash-pinned Senseval/SemEval slice is admitted only for conditional
  contextual-sense smoke testing: 23 candidate-polysemous VPC rows/18 types,
  split into six SemEval-2007 development and 17 fixed source-test rows already
  exposed during audit. It has no VID or `take in` evaluation row, no unseen
  forms, only one cross-occurrence sense contrast, and no usable
  abstention/out-of-inventory test. The exact framework zip has no explicit
  redistribution grant, so only aggregate evidence is kept.
- Reproducible MWEasWSD/SemCor reuse audit over six exact external artifacts.
  The official SemCor archive resolves text reuse with a retained notice, but
  the manual additions are rejected as contextual fine-sense validation gold:
  zero category-confirmed VPC/VID rows, five conflicting first-wins duplicate
  keys, no independent annotation/uncertainty evidence, only 7 verb-proxy forms
  and 17 rows with observed positive sense contrasts, 125/136 lossless verb-
  proxy mappings to OEWN 2025, and an unresolved +3 positive/+917 negative
  artifact-versus-paper count mismatch. A stdlib checker emits aggregates only;
  no SemCor sentence or external resource is bundled.
- Artifact-level core MWE evidence admission matrix for STREUSLE 5.0, MAGPIE,
  SemEval-2022 Task 2, MWEasWSD, and the standard WSD slice. It separately
  admits bounded STREUSLE occurrence/category evaluation, external MAGPIE
  idiomaticity evidence, and only a severely limited conditional sense smoke
  test; the existing STREUSLE projection remains exposed and MWEasWSD's added
  labels remain rejected as validation gold.
- RMAL priority correction. Contextual English VPC/VID candidate, span,
  category, idiomaticity, and sense analysis is now the primary technology;
  ambiguity, abstention, and out-of-inventory states remain first-class.
  Coverage, source-corpus, learner-text, comprehension, and eye-movement work is
  explicitly downstream. The active gate is a lawful occurrence/sense benchmark
  and frozen split, not further Gutenberg or TECO analysis.
- Final Project Gutenberg fixed-prefix rights triage and futility stop. Ranks
  31–40 yield 13 files eligible only for local notice review, five likely-active
  Japanese terms, and two unresolved creator/death terms. With only five
  eligible adult/unspecified files left and three prior passes, that stratum can
  reach at most eight, below the frozen ten-unit stop. No batch-4 ebook was
  acquired, no target/MWE search ran, and incidental target-string exposure in
  two frozen search results is disclosed.
- Third Project Gutenberg unit gate. Seven of 15 fixed first units pass
  mechanically: two adult/unspecified and five juvenile. Five intact units
  exceed 2,000 project tokens; the opening letter, introduction, and foreword
  are excluded as unfrozen unit types rather than skipped. Combined yield is
  10/44 (three adult/unspecified, seven juvenile). No prose was bundled, no unit
  was admitted, and no target or MWE search ran.
- Third Project Gutenberg front-matter review. All 15 exact files proceed to
  the unchanged first-unit gate: nine have complete print-publication
  statements, six remain incomplete, three have explicit transcriber notes,
  and two producer summaries are excluded. Paul Armstrong's named underlying
  play contribution is rights-reviewed rather than ignored. Three source-
  authored opening sections remain first; no unit or MWE decision was made.
- Third Project Gutenberg pre-body notice audit. The 15 rights-triaged files
  were retrieved into ignored local storage and pinned by URL, bytes, mirror
  file time, and SHA-256. All pass the notice, ebook-boundary, and full-license
  checks; one preamble identifies an original publication and all include
  Credits. No body was reviewed, no unit admitted, no MWE search run, and no
  source file entered Git or the Web app.
- Third fixed-prefix Project Gutenberg rights triage. Ranks 21–30 in each
  stratum yield 15 files eligible only for local notice review, three likely-
  active Japanese terms, and two unresolved author identities/death terms.
  Rights-search output incidentally exposed `take in` for one already frozen
  candidate; the exposure is recorded and changes no selection or gate rule.
  No ebook was acquired, no target/MWE search ran, and no unit was admitted.
- Second Project Gutenberg unit gate. Of the 16 provenance-ready fixed first
  units, one juvenile chapter passes mechanically, nine complete chapters or
  short stories exceed 2,000 project tokens, and six first sections have unit
  types outside the frozen rule. The held photoplay is not evaluated. No unit
  was admitted, no prose was bundled, and no target or MWE search ran.
- Second Project Gutenberg front-matter review. Sixteen of 17 exact files are
  ready for the unchanged first-unit gate. Five source-authored prefaces or
  introductions remain the first unit instead of being skipped for a chapter;
  two producer-added synopses are excluded. `Tom Slade` is held because its
  electronic title matter names a photoplay adaptation but omits the source
  film's three story credits. No unit was admitted and no MWE search ran.
- Second Project Gutenberg pre-body notice audit. The 17 rights-triaged files
  were retrieved into ignored local storage and pinned by URL, bytes, mirror
  file time, and SHA-256. All pass the notice, ebook-boundary, and full-license
  checks; three preambles identify an original publication and all 17 include
  Credits. No body was reviewed, no unit admitted, no MWE search run, and no
  source file entered Git or the Web app.
- Second fixed-prefix Project Gutenberg rights triage. Ranks 11–20 in each
  stratum yield 17 files eligible only for local notice review, one active-term
  hold, and two unresolved-identity/death holds. The review adds the official
  Japanese publication-term route for genuine anonymous/pseudonymous works:
  `Roy Rockwood` and `Quincy Allen` advance on work-specific evidence, while
  the unexplained `Frank Walton` name remains held. No ebook was acquired, no
  unit admitted, and no target or MWE search ran.
- First Project Gutenberg unit gate. Exact heading-to-next-sibling ranges and
  retained-text hashes are pinned for all 13 files, using the app tokenizer
  after removing only bracketed illustration blocks. Two units pass
  mechanically (one per audience stratum), ten first units exceed 2,000
  tokens, and one in-range introductory section is excluded because it is not
  an unambiguous frozen unit type. No later unit was substituted, no MWE or
  target search ran, no prose entered Git, and no unit is admitted for serving.
- Project Gutenberg front-matter review for all 13 locally pinned candidates.
  The exact electronic file—not an inferred print edition—is now the analysis
  source; no additional retained translator, editor, adapter, or introducer was
  found. Five incomplete print-publication statements and five explicit
  transcription/normalization notes remain visible. Nine cases of limited body
  exposure while locating boundaries are disclosed; none affected the frozen
  queue. All 13 proceed only to the mechanical first-unit gate: no unit was
  admitted and no lexical or MWE search ran.
- Project Gutenberg pre-body notice audit. The 13 metadata-triaged files were
  retrieved from the listed high-speed Project Gutenberg mirror into ignored
  local storage and pinned by URL, byte size, server-derived file time, and
  SHA-256. All contain the US/non-US warning, ebook boundaries, and full
  license footer; only three preambles name an original publication and one
  omits production credits, so front-matter review remains mandatory. No body
  prose was decoded for review, no unit selected, no MWE search run, and no
  source file entered Git or the Web app.
- First fixed-prefix Project Gutenberg rights triage. Ranks 1–10 in each
  audience stratum were screened before file acquisition: 13 may proceed only
  to internal-notice checking, five are held because Japanese protection is
  likely active, and two are held because author identity/death remains
  unresolved. The ledger applies Japan's 2018 non-revival and wartime-addition
  transition instead of a death-plus-70 shortcut, separates excluded visual
  contributions from retained prose, and discloses incidental search-snippet
  exposure. It permits local notice review, not source-text inclusion in a
  globally reachable app. No ebook was acquired, no unit admitted, and no MWE
  search ran.
- Target-blind Project Gutenberg prose frame. A standard-library pass verifies
  the pinned 2026-08-30 weekly catalog, defines separate adult/unspecified and
  juvenile English-fiction strata, and freezes 40 metadata-ranked candidates
  per stratum before any ebook or MWE inspection. Rights review precedes local
  acquisition; each stratum stops at ten intact 300–2,000-token prose units.
  The 80-row queue contains metadata and hashes only and is not a reference
  corpus, participant dataset, or claim of worldwide public-domain status.
- Preliminary outcome-blind TECO MWE desk triage. All 285 machine leads were
  read in context before any participant outcome join; 39 were retained as
  plausible VPC/VID occurrences, 4 received explicit boundary or unresolved
  exceptions, and the remaining 242 were provisionally not retained. A bounded
  missed-lead pass adds four plausible occurrences and preserves ten hard cases
  as unresolved. The record contains positions and decisions but no passage
  prose, surface tokens, answers, proficiency, or eye measures; it is not gold
  annotation.
- Outcome-blind TECO MWE lead screen and frozen ROI boundary. A standard-library
  pass over the pinned 10,063 word-information rows found 285 OEWN-based review
  leads across all 30 passages (126 contiguous, 159 gapped) while exporting no
  passage tokens, participant rows, or eye/comprehension/proficiency outcomes.
  The primary empirical unit remains the member word; word-summary sums are not
  mislabeled as fixation-sequence-defined whole-MWE gaze measures.
- Existing-data-first roadmap correction. New L2-reader recruitment is removed
  from the active path: TECO v1.1 becomes the first participant-linked
  processing/ROI dataset, MECO-L2 and CELER are gap-specific complements, and
  ICNALE remains production/error evidence. Project Gutenberg becomes the
  separate target-blind open-natural-material route. A verified 2026
  Portuguese-L1 idiom-eye archive is quarantined after participant-count,
  proficiency-range, and duplicated-derived-file inconsistencies were found.
- Prose-free TECO v1.1 candidate manifest. It pins nine OSF artifacts and their
  SHA-256 identities and verifies complete, duplicate-free joins for 41 readers
  × 10,063 word items and 41 readers × 30 passages. It admits no Eiken prose or
  analysis result and forbids treating gaze or general proficiency as
  occurrence-specific MWE knowledge.
- Source-level TECO/Eiken redistribution review. The article, OSF README and
  node license, hash-verified 34-page reading-material file, CC BY scope, and
  current Eiken terms now support a fail-closed release boundary: passage and
  question text plus ordered reconstructable token sequences stay local unless
  written downstream/API permission is archived. Prose-free IDs/positions and
  non-reconstructive results remain separately eligible for review.
- Content-neutral amendment stopping SimpleWiki Route 2 before `come out`.
  It preserves the frozen design and completed desk records but withdraws topic
  sensitivity as a lexical-evidence exclusion: sensitivity is separate
  metadata, while rights, extraction coherence, target validity, meaning, and
  centrality remain distinct passage gates. The disclosed counterfactual ranks
  are `pick up` 1/2/3 and `give up` 1/3/5. Because the original filter also
  excluded `pass away` and thereby changed the VID pool, a new target derivation
  must be frozen rather than silently repairing Route 2 v1.
- Prose-free `give up` desk review under the original Route 2 v1 rules. Fifteen
  true target occurrences and four false gap leads were adjudicated across the
  first 15 ranks, with 35 `give` heads checked and no missed occurrence. The v1
  selection at ranks 3, 5, and 15 is retained as audit history, not as the
  content-neutral result; rank 16 was viewed after the old stop and is disclosed
  without a label.
- Prose-free `pick up` desk review for SimpleWiki Route 2. The frozen early
  stop selected desk ranks 1, 2, and 4 across three operational meanings and
  two naturally discontinuous occurrences; rank 3 was rejected for acute
  violence. The ledger records all five automatic leads and `pick` heads in
  the formal prefix, OEWN candidates, draft global/target-critical items,
  cross-target `come out` decisions, and revision-level rights routes. Ranks
  5–20 were viewed after the formal boundary but are disclosed and cannot alter
  the deterministic selection. No article prose, app feature, or final
  admission was added.
- Complete bounded `take in` desk review for SimpleWiki Route 2. All 20
  mechanically eligible rows and all 41 take-head tokens were read; every one
  of the 28 automatic gap leads was a false span and no missed target occurrence
  was found. The prose-free ledger retains member positions, span hashes, and
  six reason codes. `take in` therefore fails at its frozen stop limit, with no
  passage or app change.
- Prose-free rendered-boundary screen for the frozen SimpleWiki Route 2 queues.
  It followed rank order until each target supplied 20 mechanically eligible
  pages: 509 target rows across 508 unique revisions, 508 source-hash-verified
  rows, 389 mechanical exclusions, and one API-unavailable revision. The 120
  desk rows represent 119 pages, with the one duplicate and all cross-target
  flags preserved. Raw API HTML/wikitext and the BNC/COCA profile remain ignored
  and local; no occurrence, sense, centrality, content, or passage-admission
  decision is claimed.
- Checksum-verified, standard-library Simple English Wikipedia dump screen. It
  streamed 398,768 main-namespace pages into a prose-free 16,375-row ledger,
  retained every exclusion and unselected candidate, and fixed each full queue
  before rendered inspection. The first 20 `take in` rows are all gap-only,
  exposing the detector's likely false-positive burden instead of silently
  reordering the sample; no passage or occurrence has been admitted.
- Prespecified Simple English Wikipedia Route 2 material design after the VOA
  stop. It pins the 2026-08-01 dump and checksum, derives four VPC and two VID
  targets from frozen STREUSLE/OEWN/NGSL evidence, bounds each deterministic
  queue at 20 desk screens, and requires three VPCs, one VID, three articles and
  two meanings per target, plus one naturally discontinuous VPC. No article
  prose, annotation task, Web-app feature, or 95%/98% selection band was added.
- Bounded out-of-inventory audit closing the frozen VOA frame without an
  admission. All 19 remaining source/text hashes were reproduced; 227
  STREUSLE-derived non-OEWN strong-type leads yielded 30 contiguous and 41
  short-gap hits. Even a deliberately generous union with all prior triage
  forms left every article pair with at most one shared candidate, so further
  VOA searching stops before human annotation or app expansion.
- Full preliminary desk review of both deferred VOA passage pairs. The
  prose-free ledger covers all 45 contiguous and 25 short-gap automatic leads
  in Health 03 and 22 plus 16 manual additions, verifies both pinned AMP/text
  hashes, and rejects both the Health pair and the Education 07 + Health 03
  cross-program pair pending author confirmation. It also records the newly
  exposed `find oneself` manual-recurrence lead and excludes it as PARSEME IRV
  rather than widening the VPC/VID target, without admitting a passage or
  expanding the app.
- PARSEME 1.2/STREUSLE taxonomy correction across both occurrence ledgers.
  `deal with`, `come with`, and `turn into` are no longer mislabeled as VPCs;
  weak/prepositional expressions and noun-complement `go on` constructions are
  separated from the bounded strong VPC/VID projection. Pair rejections are
  unchanged, but their reasons now match the app contract.
- Full preliminary desk review of the two priority Education passage pairs.
  The prose-free ledger covers all 44 contiguous and 21 short-gap leads in
  three articles plus 15 manual additions, checks the pinned OEWN sense source
  and original source marking, and rejects both pairs pending author
  confirmation. Each retains only one shared form that is plausibly
  target-critical across both passages; no passage or app sense projection is
  admitted.
- VOA presenter-boundary normalization for attested soft hyphens. Education 12
  and 16 had retained `I’m Pete Musto` because U+00AD interrupted the first
  presenter name while a later presenter still matched; the shared extractor
  now recognizes that format character, its self-check fixes the regression,
  and all dependent text hashes and profiles were regenerated.
- Preliminary recurrence triage before full passage review. It retains 13 of
  38 cross-document contiguous forms and identifies four article pairs with at
  least two retained forms, prioritizing two topically and lexically closer
  Education pairs. A bounded one-to-two-token gap pass adds 128 diagnostic
  leads but rejects all 19 recurrent gap forms after context inspection; its
  only `take in` hit is the false span `taking classes in`, not `take it in`.
  The triage contains no prose, awaits author confirmation, and admits nothing.
- Target-blind automated pre-review for all 24 source-eligible VOA articles.
  The standard-library pass verifies frozen source/text hashes, reports open
  NGSL 1K/2K descriptors, and retains 229 contiguous plus 128 short-gap OEWN
  leads without prose or an admission claim. An optional local-only
  BNC/COCA overlay stays under ignored `research_data/`; its values are not
  bundled while derived-output rights remain unresolved. No article reaches
  nominal 95% under either first-2K screen, and no passage is admitted before
  manual MWE, marking, centrality, sense, and content review.
- Target-blind VOA source-eligibility screen over the frozen queue. It needed
  25 Education and 38 Health & Lifestyle records to retain 12 per category;
  39 records were excluded for external/adapted credit, missing recognized
  production credit, or unsupported quiz/non-article structure. The compact
  result preserves source and eligible-text hashes without HTML or prose. The
  shared extractor now accepts observed `reported on this story` and
  `for Learning English` production-credit variants; neither change admits an
  adaptation or makes an MWE/material-validity claim.
- Fifth Gate 1 screen rejecting a 2011 VOA education near-match despite two
  central `end up` occurrences: no second decision-relevant form repeats in the
  retained pair, `drop out` is title-cued, and the legacy page adds age,
  background-knowledge, and extraction differences. Exact source/text hashes
  and NGSL profiles are retained, but no legacy parser or source prose was
  added. Target-form-conditioned passage hunting is now closed. A
  standard-library reproducer freezes 79 VOA Education/Health archive pages as
  a 936-URL 2017–2020 development frame, marks three previously seen texts, and
  records a deterministic 24-item metadata queue plus source hashes before a
  design pivot.
- Kyle and Eguchi (2021) artifact disposition for the conditional BERT lane:
  use the public 480-row word/bigram/dependency result structure as a
  document-level production comparator, not as MWE gold. The audit records the
  absence of source essays and occurrence/sense labels, an unavailable refined
  CSV referenced by the R Markdown, and no located repository license. Any
  original-corpus use remains optional, local, rights-reviewed, and dependent
  on new double-reviewed VPC/VID annotations; it cannot replace the reading
  criterion study or justify a browser model.
- Fourth Gate 1 VOA screen finding one provisional, unmarked, globally relevant
  `end up` pair in the Goals and Common Application articles while refusing to
  admit it as a material set: only one repeated target survives, and length,
  U.S.-admissions knowledge, and inline-gloss differences remain. A proposed
  `write down` pair is rejected because the Goals source explicitly teaches the
  expression in a bold section heading. The writing article's separated
  `passes it off` occurrence is retained only as a context-cued detector
  diagnostic. The standard-library extractor now recognizes the observed VOA
  `reported this` credit form and checks both supported forms.
- Third Gate 1 VOA screen retaining one near-95/98 fixed-list Goals singleton
  while rejecting its NASA `take up` partner. The NASA target is bolded and
  glossary-defined on the source page, its technical profile is much lower, and
  silently stripping those cues would change the original reading condition.
  The extractor now preserves substantive prose that shares a paragraph with a
  presenter sign-off and its self-check covers a two-presenter boundary.
  A dated Twitter partner was rejected before parser expansion because current
  platform knowledge and a structurally essential HTML list would confound the
  reading task.
- Standard-library extraction and provenance checks for candidate VOA Learning
  English AMP articles, excluding media, captions, quizzes, glossaries, and
  presenter credits from the passage. Full paragraph-level OEWN-lead and manual
  desk review rejects the first cross-sense `take in` pair from the primary
  material set: both meanings are strongly cued, globally peripheral, and
  unlikely to support non-tautological comprehension items. The pair remains a
  diagnostic sense case only; no source prose, human task, or app feature was
  added.
- Standard-library extraction and provenance verification for five pinned eLife
  JATS digests, including an embedded parser self-check, article-level license,
  source/digest hashes, and exact version identities. The first Gate 1 screen
  rejects all five from the primary passage set: their first-2K profiles are far
  below the intended interpretive range and repeated `break down`, `carry out`,
  and `take up` cases do not provide contrasting contextual senses. No source
  prose is committed and no app feature or human task was added.
- Gate 1 development-material source screen narrowing the first pass to intact
  modern general-science explanations, with an eLife CC-BY/versioned-XML
  shortlist, cross-document `break down`/`carry out`/`take up` leads, explicit
  topical-knowledge and same-sense threats, hard per-passage admission fields,
  and conditional rejection of less reproducible source classes.
- Gate 0 construct teach-back preflight with a separate English participant
  packet, seven response/transfer questions, claim-to-implementation audit,
  decision-anchored coding, strict pass rule, and response-process memo template.
  The optional check is deferred so non-publishable human feedback does not
  block desk-based material admission. If later used, human contact remains
  blocked until local ethics/consent, retention, and non-coercive recruitment
  decisions are recorded. The governance draft follows BAAL, current Japanese
  PPC, and JSPS guidance and rejects Git ignore or an unapproved Dropbox path as
  privacy protection.
- Evidence-first RMAL programme roadmap with a submission claim ladder,
  dependency-gated material/instrument/criterion gates, one-work-package limit,
  explicit exploratory versus prospective claim ceilings, and three immediate
  deliverable/stop-condition packages. Source-to-target corpus work is no longer
  a first-paper gate, and unmeasured model/resource expansion is frozen.
- Browser-local 1–20-document named MWE review sets built from the existing
  single-document workspace contract. Each document retains its ID, label,
  text, pattern, profile identity, and decisions; import validates the complete
  set before replacement and exports refuse unsaved current review changes.
  Source inputs are locked during review to prevent edits from silently
  discarding decisions.
- Required source-text SHA-256 in single-document workspace schema 0.2.0 and
  document-set restore, so changed text is rejected even when token positions
  and occurrence IDs would otherwise remain structurally valid.
- Phase 0 admission charter and dated construct-decision record covering
  passages, contextual word and MWE measures, comprehension, conventional word
  profiles, source-to-target corpora, the 95%/98% interpretation boundary, and
  criteria that remain exploratory rather than prematurely numerical.
- Explicit single-document MWE workspace save/restore using a local JSON file.
  The resume file contains raw text, pattern TSV, occurrence decisions, and
  runtime-resource identities; restore requires current authorization plus an
  exact contract/profile match and reconstructs canonical token records rather
  than trusting serialized tokens. No autosave, browser storage, or server was
  added.
- Standard-library Nation BNC/COCA Level 6 v1.0.0 first-2K local-profile
  builder and exact browser import. The app verifies the 366,120-byte derived
  file and SHA-256, exposes separate first-1K/2K word-family conditions,
  excludes all four special lists, never executes or bundles Range, and records
  the runtime file hash in method JSON.
- Reproducible NGSL 1.2 ranked-list projection and required browser selection
  among NGSL first-1,000/2,000/full and TUBELEX frequency conditions. Item rows
  distinguish `beyond_cutoff` from `unmatched` and retain both candidate heads
  for the five source-identified homographs instead of silently disambiguating.
- Browser-local idiomaticity review and a bounded `take in#v` sense-review
  workflow that displays all 17 OEWN candidate glosses/examples, records
  assigned/ambiguous/abstained/unassigned states without a default, and exports
  the complete inventory and human-decision provenance in CSV and method JSON.
- Criterion-evidence roadmap for testing whether component-known but
  contextually unknown MWEs under-specify conventional 95%/98% word-token
  coverage, separating list, source-corpus, and tested person-to-text profiles
  and requiring non-priming word/MWE knowledge measures before any adjusted
  coverage score or threshold claim.
- Focused literature search and 81-page, page-level close-reading record for
  learner-error parsing, MWU profiling, MWE complexity, erroneous collocation
  detection, MWE-aware vocabulary coverage, and sense-aware lexical
  sophistication, with explicit design consequences and non-inferences.
- Admitted, browser-loaded reference profiles for 410,400 TUBELEX English regex
  ASCII word forms and 2,847 OEWN 2025 ASCII multiword verb forms, with pinned
  source hashes, full manifests, notices, removal procedures, and a deterministic
  standard-library builder.
- Separate TUBELEX word-token/type membership and OEWN confirmed-MWE
  occurrence/type membership, preserving profile-specific tokenizers,
  denominators, unmatched items, source counts, frequency-per-million, rank,
  and explicit non-inferences.
- Word item CSV and extended occurrence CSV exports; method JSON names both
  active profiles but omits raw text, pattern TSV, and word item rows.
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

- Removed the implemented document-set MWE review from the contract's
  `not_implemented` list and added a contract check preventing that stale claim.
- No account, server analysis, analytics, cookie, database, external model,
  third-party runtime code, or external lexical-service query. Method JSON omits
  raw text; the separate resume JSON includes it only after an explicit local
  save action. User patterns create review candidates but do not automatically
  confirm MWE status. Static reference profiles remain separate rather than
  forming a composite score.
- Server-side storage is not treated as licensing permission; open resources
  remain downloadable, and restricted resources require delivery-specific
  permission even when hidden behind an API.
- Input count and size limits, all-or-nothing batch validation, unique normalized
  IDs, well-formed Unicode checks, and exact client-clock timestamp formatting.
- Exported hashes and timestamps are explicitly non-authenticating; results are
  descriptive and exclude proficiency, quality, authorship, causal, and
  population claims.

### Verification

- Reconstructed the current tracked diff plus four intended new release files
  over `HEAD` in an empty temporary tree. The reconstruction matched the working
  tree after excluding `.git`, ignored `research_data`, caches, and the internal
  roadmap HTML.
- In that reconstructed tree, all Python and Node contract tests, the supplied-
  candidate evaluator, STREUSLE self-check, JSON parsing, and JavaScript syntax
  checks passed. The HTML checker reported no structural error and six legacy-
  checker warnings for `autocomplete` on `textarea`.
- The reconstructed `index.html`, both JavaScript modules, MWE contract, NGSL
  profile, and OEWN sense projection each returned HTTP 200 from local static
  serving.
- After the application checkpoint `d3accc0`, a non-local clone into an empty
  temporary directory had a clean worktree and reproduced all checks above;
  its same six public files returned HTTP 200. This is a clean-checkout result,
  not an interactive-browser acceptance or frozen public-release archive.
- Defined the real-browser acceptance gate in `ROADMAP.md`, including browser
  diversity, keyboard and screen-reader operation, lossless resume, responsive
  reflow, restricted-profile rejection, privacy inspection, evidence fields,
  and fail-closed criteria. The gate remains unrun.
- Re-ran all dependency-free checks after the document-set change. Node covers
  single/set round-trips, duplicate IDs, occurrence limits, source-text
  tampering, and resource mismatch; Python reports seven passing tests. The six
  public static files again returned HTTP 200. Interactive-browser acceptance
  remains unrun.

### Not yet verified

- Real-browser workspace save/re-import, visual, keyboard, narrow-screen, zoom,
  and screen-reader behavior.
- Interpretation by representative L2 vocabulary researchers.
- Construct validity, population validity, cross-tool equivalence, public archive,
  release checksums, and citable release metadata.
