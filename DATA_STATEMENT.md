# Data statement — planned core English VPC/VID benchmark

Status: pre-data statement, version 0.1, 2026-09-04. This combines the
project-relevant fields from Data Statements for NLP and Datasheets for
Datasets. No benchmark data or human-participant evidence exists yet.

## Language and communicative setting

- Language: English.
- Variety: collaboratively edited international English; national and regional
  varieties are neither sampled nor labeled as strata.
- Modality and genre: written encyclopedic prose from English Wikipedia.
- Time: page revisions represented in the completed 2026-09-01 dump.
- Unit: one namespace-0, non-redirect article revision; retained paragraphs are
  annotation segments.
- Authors/speakers: Wikipedia contributors. Demographics, first language,
  dialect, proficiency, location, age, gender, and socioeconomic information
  are not collected and cannot be inferred from the benchmark.
- Audience and interaction: public reference writing for Wikipedia readers;
  articles may be multi-author and edited over time. No conversational setting
  is represented.

## Population boundaries

The **source population** is the namespace-0, non-redirect wikitext article
revision population in the frozen dump. The **sampling population** is the
subset remaining after content-neutral eligibility and rights rules fixed by
IR-121. The **annotation population** is every eligible retained prose
paragraph in the sampled documents, not paragraphs found by searching a target
list. The **target population** is English VPC.full, VPC.semi, and VID
occurrences in those paragraphs. The **evaluation population** is the later
document-grouped frozen split. These populations must not be substituted for
one another in reporting.

## Collection and processing

The official dated Wikimedia dump route, exact descriptor, and zero-search
boundary are recorded in `resources/source_manifest.json`.
`resources/sampling_frame.json` freezes content-neutral eligibility, three
length strata, a deterministic random-priority seed, the equal within-stratum
inclusion-probability formula, and ordered replacements. The source rows,
stratum sizes, IR-127 allocation, and selected revision rows remain **Unknown
before release**; no document has been selected or target-searched.

Exact wikitext, API response, rendered HTML, extracted blocks/text, segment
offsets, token surfaces/normalized forms, and hashes are retained as separate
layers under `resources/preprocessing_contract.json`. Whole-text Unicode
normalization is forbidden. Non-text media and configured page furniture are
excluded.

`resources/evaluation_strata.json` fixes the evaluation axes and dependence
boundary before labels exist. A document is the primary sampling, split, and
resampling cluster; repeated occurrences of a canonical VPC/VID type form a
second cluster. Population-level overall estimates must respect the frozen
length-stratum inclusion probabilities. Category, continuity, form exposure,
variant, source genre, and length are reported as single-axis strata; sparse
cells remain descriptive unless IR-127 prospectively passes their precision
gate. The full Cartesian product is not an inferential target.

`metric_contract.json` separately freezes benchmark metric version
1.1.0-predata. Candidate, exact/member/gap span, category, idiomaticity,
occurrence/type inventory, contextual sense, ambiguity, model abstention/OOI,
and burden outputs remain separate; no combined score is allowed. Calibration
metrics require declared probability output, and risk–coverage/AURC require a
declared selective system. Fixed-seed IR-126 code resamples whole documents
within sampling-length strata, repeats the analysis with canonical types as a
secondary cluster, and uses identical draws for paired system differences.
Overall and requested frozen strata share the same estimator path; sparse or
undefined resamples withhold intervals. No observed interval or performance
result exists. `resources/precision_plan.json` and
`scripts/simulate_benchmark_precision.py` now freeze the .05 overall and .10
single-stratum gates plus fail-closed candidate simulation. The plan remains
blocked: IR-147 training material can inform guidance, agreement, and burden,
but cannot estimate Wikipedia prevalence or clustering. The accepted
`resources/planning_pilot_addendum.json` therefore creates a separate
target-blind probability-sampled prefix after guide freeze, with its size
budget-frozen before target exposure and every document excluded from the
sealed test. The route contains no pilot rows and is not yet active; no
allocation has been chosen.

The frozen split protocol assigns whole documents within each length stratum to
20% guide training, 10% annotation pilot, 20% development, and 50% sealed test
using a separate hash seed. Every paragraph and occurrence inherits its
document split. The sealed membership, text, labels, predictions, and results
remain unavailable to developers until commitment and independent-custodian
scoring. A stronger wholly canonical-form-disjoint test is not currently
authorized; it requires a prospective versioned feasibility addendum. The
public exposure ledger classifies every currently known repository evidence
group, stores no protected content, and treats missing or unverifiable access
history as exposed rather than sealed.

## Annotation and people

The annotation task covers occurrence, discontinuous members/gaps, category,
idiomaticity, contextual sense, ambiguity, abstention, and out-of-inventory
states. Candidate discovery is independent of target lists and model
suggestions.

The current collection boundary is recorded in `GOVERNANCE.md` and
`resources/ethics_determination.md`: ordinary commissioned annotation is not
presumed to be human-participant research, but its relationship, payment,
rights, access, and retention route must be fixed before engagement. Research
about annotators and intended-user studies require the applicable review before
recruitment. Annotator recruitment source, number,
language background, qualifications, training, compensation, consent/approval
basis, withdrawal process, workload, agreement, adjudication, and demographics
remain **Unknown before release — IR-115 and IR-146 through IR-153**. The
public `ANNOTATION_GUIDE.md` is version
`0.5.0-contextual-sense`: its occurrence/span/category cases are project-authored
synthetic records with no human response or natural benchmark item; its
idiomaticity module defines compositional, figurative-compositional,
conventionalized, and unresolved routes plus contextual-sense, uncertainty,
export, evaluation, and loss-aware MAGPIE rules.
`annotations/hard_case_bank.json` adds only project-authored synthetic cases,
records redistribution permission for every case, and supplies no human or
benchmark label.
`ANNOTATOR_TRAINING.md` adds a synthetic-only staged training and task-specific
qualification protocol with one retry and no combined score. It has not been
authorized or administered; no qualification results or human records exist.
`ANNOTATION_PLATFORM_DECISION.md` provisionally selects an institutionally
managed INCEpTION instance and rejects adding multi-user storage to the static
app. Its converter has passed a project-authored synthetic UIMA CAS JSON check,
but no instance, account, human record, or live independence test exists.
The guide is not approved for human use.
Contributor identities from revision
history are used only for attribution; the planned analytic records do not add
contributor profiles.

Before benchmark annotation, the IR-130 resource-development pass preserves all
146 residual STREUSLE VID types in a separate exposed queue. Three have bounded
OEWN/Kaikki candidate sets and 143 have no route in those two sources. These are
candidate and unresolved states, not human labels, admitted senses, or evidence
of true out-of-inventory use. The public projection contains identifiers and
fingerprints under upstream notices, while raw dictionary records and wording
remain outside the release.

A separate IR-131/132 projection contains complete pinned OEWN candidate sets
for four previously exposed VPC and five fixed VID training/development forms:
67 source senses in total, with stable project-ID reservations, CILI/ILI,
fingerprints, verbatim
glosses/examples, and source-member relations under the retained OEWN/WordNet
notice. It contains no corpus context or person-level data. The candidates are
unreviewed, zero senses are admitted, and the file is not runtime or evaluation
data.

The IR-132 population log adds a purposive 14-type VID workflow pilot derived
only from pinned STREUSLE 5.0 train annotations and bounded dictionary-route
metadata. It records type names, opaque IDs, counts, discontinuity counts, and
route/eligibility states, but no source sentence or token text. Twelve types
have candidate routes and two remain unresolved; the resulting rate is a pilot
workflow diagnostic, not a representative coverage estimate. Five
OEWN-routed VID forms enter the unreviewed candidate layer; Kaikki wording
remains excluded.

The candidate inventory is schema-validated and uses append-only project IDs.
Source updates preserve IDs by prior type ID and source sense key; a missing
prior sense requires an explicit lifecycle decision. The currently empty
`supersedes`, `split_from`, `merged_from`, and `related_to` fields represent
version governance, not observed semantic change or annotation evidence.

The IR-134 lifecycle fixture is wholly synthetic and contains no corpus,
dictionary, participant, or human-annotation data. It hash-fixes an old/new
inventory projection and five old annotation examples to verify that merge,
split, source deprecation, and a training-only OOI-prompted addition preserve
old records and require explicit migration status. It is not part of the
candidate inventory or benchmark and supplies no semantic or performance
evidence.

The IR-135 public audit contains only aggregate counts and source/inventory
hashes. It covers all 624 pinned STREUSLE target annotations and the full IR-132
pilot without releasing sentence, token, occurrence, dictionary, or person-level
rows. Zero-candidate items remain in every denominator. Its zero OOI count means
no contextual OOI review has occurred; it is not an estimate of OOI prevalence.

## Known bias and representativeness limits

- Wikipedia is not a probability sample of English, English speakers, genres,
  topics, or countries.
- Editorial participation, notability, survivorship, template rendering, and
  page-level rights exclusions may affect which prose is observable.
- Namespace, redirect, prose-boundary, and rights filters narrow the population.
- Annotation errors, ambiguous cases, and inventory gaps remain possible and
  must be quantified rather than silently removed.
- No inference may extend beyond the sampled English encyclopedic VPC/VID
  annotation population without separate evidence.

## Intended and prohibited uses

Intended uses are research on English VPC/VID occurrence, span/category,
idiomaticity, contextual sense, abstention, and transparent system comparison
under the frozen split and metrics.

Prohibited interpretations include all-English or multilingual coverage,
speaker or contributor profiling, learner proficiency, clinical assessment,
individual decision-making, population frequency, psycholinguistic processing,
comprehension, causal effects, or validation of an unattended production
analyzer.

## Distribution and maintenance

The planned source-text/annotation bundle is CC BY-SA 4.0 with attribution,
history links, imported-text notices, modification notice, and hashes. Project
code retains its own license. A release does not proceed until every included
page and file passes the rights and manifest gates.

The following are **Unknown before release**: archive identifier and version,
release date, file/count statistics, realized split/label distributions, agreement and
performance results, maintenance owner/contact, retention/removal schedule,
erratum process, and clean-room reproduction result. At release, each must be
replaced by a value or an explicit `not collected`/`not applicable` reason; the
card and statement must carry the same version and evidence paths.

## Framework references

- Bender, E. M., & Friedman, B. (2018). [Data statements for natural language
  processing](https://aclanthology.org/Q18-1041/).
- Gebru, T., et al. (2021). [Datasheets for
  datasets](https://doi.org/10.1145/3458723).
