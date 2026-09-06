# Core English VPC/VID benchmark card

Status: pre-data protocol, version 0.1, 2026-09-04. Source, release,
preprocessing, sampling, evaluation-strata, and metric protocols are frozen;
no Wikipedia text has been acquired, sampled, annotated, or released. Every
field marked **Unknown before release** must be replaced before a release claim
is allowed.

Companion record: [DATA_STATEMENT.md](DATA_STATEMENT.md).

## Purpose and scope

The planned benchmark supports identification of English VPC.full, VPC.semi,
and VID occurrences, their possibly discontinuous token spans and categories,
and contextual-sense decisions with ambiguity, abstention, and
out-of-inventory states. The frozen construct boundary is in
`resources/target_population_contract.json`.

It is not intended to measure all English MWEs, general language ability,
learner knowledge, psycholinguistic processing, population frequency, or
causal effects. It is not a validated automatic analyzer or an unattended
sense-labeling service.

## Populations and units

| Layer | Definition | Current state |
|---|---|---|
| Source population | English Wikipedia namespace-0, non-redirect, wikitext article revisions represented in the completed 2026-09-01 dump | Frozen ceiling; dump content not acquired |
| Sampling population | Source-population documents remaining after the frozen content-neutral eligibility rules and pre-target rights review | Rules frozen; realized row count unknown until source materialization |
| Document sample | Article revisions selected from deterministic random-priority queues within three length strata | Allocation and selected rows **Unknown before release — IR-127** |
| Annotation population | Every eligible retained prose paragraph in sampled documents, reviewed candidate-independently | Defined procedurally; count unknown |
| Target population | VPC.full, VPC.semi, and VID occurrences within the annotation population | Frozen construct; count unknown |
| Evaluation population | Frozen development/test documents and labeled occurrences | **Unknown before release — IR-128** |

One document is one immutable page/revision pair. One annotation segment is a
retained paragraph; headings are context. Tokens and discontinuous members use
offsets into the exact retained text.

## Source, selection, and independence

`resources/source_manifest.json` pins the two recombined files and official
checksums for the completed 2026-09-01 dump. `/latest/` is forbidden. The dump
and index have not been downloaded, and target search count is zero.

`resources/sampling_frame.json` freezes the document hierarchy, structural
exclusions, three length strata, seed, deterministic random-priority queues,
equal within-stratum inclusion-probability formula, and ordered replacement
rule. The source rows and final per-stratum allocation remain unmaterialized;
IR-127 must fix the allocation before any document is selected. Target lists,
dictionary entries, model output, observed MWE yield, and downstream outcomes
cannot select or replace documents. STREUSLE remains exposed development
evidence and is not the independent benchmark.

## Processing and annotation

`resources/preprocessing_contract.json` freezes exact revision verification,
pinned rendering, prose extraction, paragraph segmentation, tokenization,
normalization, IDs, hashes, and character/UTF-8 byte traces. Original layers
are retained; normalized tokens never replace surface text.

The current annotation-guide version is
`0.5.0-contextual-sense`; it maps every contract state, completes the synthetic
occurrence/span/category cases, and defines separate idiomaticity, contextual-
sense, uncertainty, export, and evaluation rules, but is not approved for
production annotation. A wholly synthetic hard-case bank covers every
prespecified boundary stratum at least twice and is explicitly redistributable;
it is not gold or qualification evidence. A separate public protocol now fixes
synthetic-only staged training, task-specific gates, and one-retry rules, but no
qualification form has been administered. Annotator count/background,
qualification results, pilot size,
independent-label procedure, adjudication procedure, agreement metrics, and
label totals are **Unknown before release — IR-115 and IR-146 through IR-153**.
`GOVERNANCE.md` and `resources/ethics_determination.md` separate commissioned
annotation work from research about annotators. The former requires a fixed
work relationship, payment/rights basis, and managed data route; the latter
requires the applicable human-research review before recruitment.
No first-pass annotator may see model suggestions or another annotator's labels.
INCEpTION is the provisional independent-annotation platform, with recommenders
and assistants disabled. Its UIMA CAS JSON converter passes only a synthetic
format-level check; live two-user isolation, project logging, and export remain
unverified pending a managed deployment and completed work arrangement.

The separate IR-130 source-mapping queue covers all 146 STREUSLE VID types
without an exact dictionary route. A hash-pinned OEWN/Kaikki scan supplies
unreviewed candidate sets for 3 and retains 143 as
`unresolved/no_bounded_route`; none is an admitted sense or proof of OOI.
Independent review and the complete Wiktionary source-identity/rights gate
remain pending. The queue is exposed resource-development evidence and cannot
select Wikipedia documents or supply contextual labels.

The IR-131 portion of the OEWN seed covers four previously exposed
training/development VPC forms with 56 of the candidate records. Each has a
permanent
project-ID reservation, source-record fingerprint, CILI/ILI, and explicit
gloss/example rights. Synset members are retained as unmerged source relations.
All project `senses` arrays remain empty pending independent review and
adjudication; the seed is not loaded by the app and is not benchmark gold.

IR-132 fixes a separate 14-type VID workflow pilot using only exposed STREUSLE
train annotations: 52 occurrences, 21 discontinuous, 12 types with a bounded
source route, and 2 no-route types. Five OEWN-routed VID types have been added
to the candidate layer, for 9 forms and 67 candidates overall. Four Kaikki
types remain behind the source-identity/rights gate. These purposive counts do
not estimate population coverage or performance.

Inventory candidate version `1.0.0-candidate.3` validates against the public
Draft 2020-12 schema. Registry tests cover ID ownership/collision, duplicate
source senses, canonical fingerprints, lifecycle-relation fields, and
source-edition reordering. Prior senses cannot disappear silently. All current
lifecycle arrays are empty and these technical checks do not replace
independent semantic review.

IR-136 now places contextual evidence before expert inventory review. A
deterministic [usage-pilot manifest](resources/polysemy_usage_pilot.json)
indexes all 54 matching STREUSLE train/dev occurrences for the nine candidate
forms, excludes test, and creates 51 connected within-form round-1 pairs. It
contains hashes and source coordinates but no source text or semantic judgment.
Pairs are rated without dictionary glosses; only then are provisional usage
clusters compared with pinned-source coverage, form relation, construction
scope, and candidate mappings. `cut short` has only one context and therefore
remains insufficient for contextual separability. Multiple applicability,
ambiguity, abstention, and OOI still require the later occurrence-to-inventory
pilot. No rating, review, or adjudication has been collected, so zero senses
are admitted.

IR-134 adds a synthetic, hash-fixed lifecycle exercise covering one split, one
merge, one deprecated source link with retained project identity, and one new
training-only OOI-prompted sense. Old annotations are preserved under their old
inventory version and receive explicit manual-review migration states; none is
rewritten. The approval rule forbids test-metric-driven inventory changes and
requires a new major benchmark version after test exposure. This is protocol
evidence, not lexical or performance evidence.

IR-135 audits the current project inventory against the complete 624-occurrence,
389-type STREUSLE target population and the complete 52-occurrence, 14-type
IR-132 VID pilot. Candidate-seed availability is 57/624 occurrences and 9/389
types; VID availability is 21/319 and discontinuous availability is 20/188.
Formal admitted coverage and contextual adequacy are 0/624. OOI therefore
remains unassessed, not absent, and every contextual-sense claim remains held.

## Splits and evaluation

`resources/evaluation_strata.json` freezes category, continuity,
development-seen/test-unseen form, verified-variant, source-genre, and sampling-
length strata. Documents are the primary cluster; canonical VPC/VID types are a
second dependency cluster and the analysis unit for any unseen-form claim.
Overall sampling-population estimates require inverse-inclusion-probability
weights. Occurrences are never treated as independent observations, and no
combined task score is allowed. Every stratum remains descriptive until IR-127
prospectively demonstrates and freezes its precision and cluster-count gate.

The `benchmark_mwe_evaluation` section of `metric_contract.json` freezes
version 1.1.0-predata inputs, formulas, denominators, zero-denominator states,
and document bootstrap units for candidate recall; exact/member/gap span
results; category macro-F1; idiomaticity; occurrence- and type-level inventory
coverage; sense assignment-state accuracy and exact-set/micro/macro F1;
multiple assignment, ambiguity, abstention, OOI, and inventory ineligibility; and
candidate burden. Brier score, log loss, and ten-bin ECE apply only to declared
probabilistic systems; risk–coverage and AURC apply only to declared selective
systems. `scripts/evaluate_mwe_predictions.py` implements point estimates on
synthetic checks. `scripts/bootstrap_evaluation.py` fixes 10,000 seeded
percentile resamples: documents are sampled within sampling-length strata,
canonical types receive a separate global sensitivity analysis, and systems
share each draw for paired differences. The same function handles overall and
requested frozen single-axis strata. A populated resampling stratum with fewer
than two clusters, or any undefined replicate, receives no interval. These
synthetic implementation checks are not performance evidence; IR-127 still
must freeze and pass allocation, cluster-count, and precision gates.

`resources/precision_plan.json` fixes the IR-127 targets at a 95% interval
half-width of .05 overall and .10 for an inferential single-axis stratum.
`scripts/simulate_benchmark_precision.py` can compare target-blind candidate
allocations once its hashed observed inputs exist, while rejecting sparse,
undefined, target-conditioned, or split-empty designs. It has not been run on
natural data. The current sampling frame permits selection only after IR-127,
except for the limited pre-allocation route now accepted in
`resources/planning_pilot_addendum.json`. That addendum separates the
target-enriched IR-147 training pilot from a target-blind, probability-sampled
planning prefix after guide freeze. Its size must be budget-frozen before
target exposure, every document is exposed development material, and none may
enter the sealed test. No prefix size or identity exists yet.

`resources/split_protocol.json` freezes a document-disjoint 20% guide-training,
10% annotation-pilot, 20% development, and 50% sealed-test allocation within
each sampling-length stratum, with a separate seed and exact integer rule.
STREUSLE, the WSD slice, dictionaries, prior material screens, and synthetic
results are classified as exposed in `resources/leakage_ledger.json`; unknown
access also fails as exposed. There are zero registered contextual/probabilistic
model experiments and zero project test items. Actual memberships, the
independent custodian, label/prediction commitments, baseline results,
confidence intervals, and abstention coverage are **Unknown before release —
IR-128 and IR-220 through IR-232**. No technical-performance claim is permitted
until the sealed evaluation passes.

The external STREUSLE development lane now has two reproducible transparent
occurrence baselines. The contiguous train-lemma floor has zero discontinuous
recall. The [frozen IR-221 rule](resources/streusle_gap_dependency_baseline.json)
permits at most two intervening tokens and
requires a direct dependency relation supported by at least five train target
arcs; development exact-span F1 is 0.426667 and discontinuous recall is 8/14.
Its optional prediction audit emits rule IDs, token numbers, and dependency
arcs without source text. The STREUSLE test was already exposed, so its results
remain development diagnostics and do not fill any project release unknown.

## Rights and distribution

The planned primary bundle contains sampled text and standoff annotations under
CC BY-SA 4.0 with revision/history attribution, imported-text notices, a change
notice, hashes, and the license link. Non-text media are excluded. Each page
must pass footer, history, talk-page, and visible-notice review before target
search; unresolved pages use only the next presampled replacement.

Release archive identifier, version, size, document/token/label counts,
checksums, maintenance contact, removal route, and clean-room reconstruction
result are **Unknown before release — IR-610 through IR-614**. Until then, this
card documents a plan, not an available dataset.

## Known limitations

- The source is collaboratively edited international encyclopedic prose;
  national variety and contributor demographics are uncontrolled.
- Wikipedia coverage, editorial practices, survivorship, and page-level rights
  review can bias the sampled content.
- Candidate-independent annotation reduces target-selection bias but does not
  guarantee exhaustive recognition or sense-inventory completeness.
- English VPC/VID evidence cannot support multilingual, all-MWE, learner, user,
  frequency, comprehension, or causal claims.

## Update rule

At release, replace every **Unknown before release** field with a value or an
explicit `not collected`/`not applicable` reason, add versioned evidence paths,
and rerun rights, manifest, and clean-room checks. Any change to population,
sampling, preprocessing, labels, splits, or metrics requires the governed
version change in `resources/decision_log.json`.
