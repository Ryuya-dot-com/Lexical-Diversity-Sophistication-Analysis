# Open MWE-aware lexical-coverage laboratory roadmap

Status: RMAL-targeted product and validation reset, reviewed 2026-09-01

This repository is an independent, free, browser-based methods laboratory for
L2 vocabulary researchers. Its primary job is to prevent multiword lexical
units from disappearing into ordinary word-level coverage. It must report word,
MWE-form, and MWE-sense channels separately, with visible denominators,
unresolved states, resource coverage, and invalid inferences.

The first automatic scope is English verb-particle constructions (VPCs). The
current surface-count scenarios are useful browser and method-audit scaffolding,
not the product definition and not a publishable contribution by themselves.
General lexical sophistication, all-type MWE, multilingual analysis, automated
proficiency scoring, and TAALES replication are not initial goals.

The ignored `ldfreq_webapp_master_roadmap_20260831.html` correctly preserved
the original construct priorities but over-specified a three-service system
before the minimal measurement contract existed. This roadmap restores its
word/MWE/sense separation and human-review requirements without adopting that
premature architecture.

## Publication target and contribution

The final project outcome is a submission to **Research Methods in Applied
Linguistics (RMAL)**, not merely a deployed website. The journal's official
scope, checked on 2026-09-01, includes methods for applied-linguistics research
design, data coding, analysis, reporting, ethics, and open science. The planned
submission must therefore demonstrate an applied-linguistics method that solves
a consequential measurement problem; a feature tour or software announcement
is insufficient. Source: [official RMAL journal description](https://shop.elsevier.com/journals/research-methods-in-applied-linguistics/2772-7661).

Working contribution:

> An open, reviewable method for estimating lexical coverage in L2 research
> while preventing multiword occurrences from being silently reduced to
> independent word tokens.

The primary paper audience is L2 vocabulary researchers. English-language
teaching practitioners are a secondary design and interpretation audience, not
a source of untested pedagogical-effect claims. The paper must show the full
chain from operational definition to candidate review, separate denominators,
error analysis, user interpretation, and reproducible reporting.

The provisional manuscript form is an empirical methods article. Recheck the
current RMAL Guide for Authors immediately before manuscript preparation and
again before submission; do not freeze word limits, formatting, declarations,
or open-access costs from a dated roadmap.

## Minimum useful product

The next release is accepted only if a researcher can complete this single
end-to-end task in the public interface:

> Paste one English text; inspect highlighted VPC/VID candidates including
> separated members; confirm, reject, or leave them unresolved; select an
> admitted reference profile; view ordinary-word and confirmed-MWE coverage
> with separate numerators, denominators, unmatched items, and unresolved mass;
> export an occurrence table plus a self-describing method record.

This path is the product. The current TTR scenarios become a secondary method-
audit/tutorial surface. Offline contracts, resource projections, and benchmark
scores count as enabling evidence only when they protect or validate a visible
step in this path.

The first useful increment is deliberately narrow: one text, English VPC/VID,
transparent candidate generation, human review, form-level coverage, and tidy
CSV plus method JSON. Automatic fine-sense assignment, group inference,
general all-MWE coverage, and contextual models are later increments. Sense
states remain in the contract so uncertainty is not collapsed, but sense-level
automation is not required for the first submission unless it receives its own
validation evidence.

## Product surfaces

The product has three deliberately different surfaces:

1. **MWE/VPC review:** candidate occurrences expose member tokens, gap tokens,
   canonical form, category, evidence, and status. A researcher can confirm,
   reject, or leave an occurrence unresolved and can select, reject, or abstain
   from inventory-specific sense candidates.
2. **Coverage analysis:** ordinary word coverage, MWE occurrence/density,
   form-level reference coverage, sense-level coverage, annotation coverage,
   and sense-assignment coverage remain separate outputs. There is no default
   combined score.
3. **Method audit:** fixed, project-authored scenarios expose what a metric
   changes, ignores, and confounds. The current probe implements only this
   supporting surface.
   The current browser-local workspace still restricts input to synthetic or
   rights-cleared published text. Before a useful release, replace that blanket
   restriction with a researcher-authorization boundary that can include
   appropriately governed and de-identified learner text. The app writes no
   durable copy and provides explicit/best-effort clearing, but cannot guarantee
   erasure from browser/device memory, history, or backups. The JSON export
   deliberately omits the text, so the researcher must preserve the exact
   source separately and verify it against the exported hash.

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

Batch and group workflows come after the single-text MWE-aware path. The app
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
  note for the batch, and the current public-text-only attestation; before a
  useful release, replace the latter with an attestation that the researcher is
  authorized to process the data under applicable consent, ethics, privacy, and
  institutional requirements because public availability is not the only
  lawful research basis;
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

The parent repository remains an evidence vault. Its algorithms, data, and
derived artifacts are not runtime dependencies and are not copied without a
file-level method, provenance, rights, and numerical review.

## Priority order

1. **User value before more infrastructure.** Complete the single-text MWE-
   aware coverage path before adding another benchmark, model, metric, database,
   batch mode, or governance layer.
2. **Restore the construct in the interface.** Ordinary word coverage,
   confirmed MWE-form coverage, unresolved candidate mass, and MWE-sense
   coverage are different estimands. A contract that users cannot invoke is not
   a product feature.
3. **Occurrence before sense.** VPC candidate generation, occurrence
   confirmation, inventory lookup, and contextual sense assignment are separate
   stages. `ambiguous`, `abstained`, `unassigned`, and `out_of_inventory` remain
   observable states.
4. **Actionable output before additional indices.** Show the lexical items,
   member/gap spans, decisions, unmatched items, and denominators that produced
   a result. Aggregate scores alone do not support research coding or teaching
   decisions.
5. **Reuse before invention.** Eguchi's Multi-Word Units Profiler supplies the
   closest user-text profiling prior art; FLAT/PARSEME supply an established
   MWE annotation workflow and conventions; PARSEME 2.0, CoAM, STREUSLE,
   MAGPIE, and SemEval idiomaticity data supply different validation targets;
   Open English WordNet supplies an open sense inventory; TAALES supplies
   unigram and contiguous n-gram comparators. A new profiler, annotation
   platform, detector, or sense inventory needs evidence that these cannot meet
   the admitted need.
6. **Rights and ethics before data admission.** A tool license, an algorithm
   description, a corpus license, and permission to redistribute derived tables
   are four separate questions. Local processing does not remove consent,
   privacy, or institutional obligations, but the app must not forbid all
   authorized non-public learner data by default.
7. **Auditability before claims.** Raw values, formulas, parameters,
   coverage, versions, and exclusions remain visible and exportable.
8. **Open access before feature breadth.** Static browser execution and
   project-authored fixtures are the default. A server or restricted resource
   requires a demonstrated research need and a sustainable free-access plan.

## RMAL evidence programme

| Phase | Required outcome | Evidence | Current state |
|---|---|---|---|
| 0. Claim freeze | One method problem, intended users, operational definitions, exclusions, and planned comparisons | Versioned protocol and analysis plan | In progress in this roadmap |
| 1. Useful vertical slice | The minimum useful product can analyze one text from input through reviewed occurrence export | Task-level browser checks and example release | Implemented with separate word/MWE-form coverage and exports; real-browser and intended-user checks absent |
| 2. Resource/data admission | At least one word-reference profile, one MWE inventory, and one applied-L2 evaluation sample have lawful, pinned, documented use | Manifests, hashes, notices, sampling/ethics record | TUBELEX word and OEWN MWE-form profiles admitted; applied-L2 evaluation sample absent |
| 3. Technical validation | Candidate identification and category decisions are evaluated on fixed held-out data, with contiguous/discontinuous and seen/unseen errors separated | Exact-span/category results, baselines, prediction files, error taxonomy | Transparent STREUSLE floor only; not an adequate detector |
| 4. Measurement validation | Word-only and MWE-aware coverage are compared on relevant L2 texts and the consequences of unit decisions are quantified | Predeclared estimands, sensitivity analyses, annotated examples, uncertainty | Not started |
| 5. Human evaluation | Intended users can complete the workflow and correctly interpret outputs; expert annotation reliability and adjudication are documented where human gold is created | Justified sample, task completion, interpretation errors, agreement, qualitative feedback | Not started |
| 6. Open release and manuscript | The exact tool, protocol, materials, permissible data, code, predictions, analyses, and reporting artifacts are archived and citable | Immutable release, DOI, checksums, data/code statement, manuscript supplement | Not started |

The validation study must be designed before inspecting its final held-out
results. Predeclare the unit of analysis, sampling frame, target population,
gold-annotation procedure, missing/unresolved treatment, primary metrics,
subgroup/error strata, comparisons, and claim thresholds. Exploratory work
remains labelled exploratory. STREUSLE alone cannot establish validity for L2
learner writing, teaching materials, pedagogical importance, or sense coverage.

Provisional paper questions:

1. How does treating reviewed MWEs as lexical units change word- and MWE-level
   coverage estimates relative to a transparent word-only analysis?
2. How accurately and transparently does the workflow identify contiguous and
   discontinuous English VPC/VID occurrences, including unseen types?
3. Which candidate, reference-resource, and human-review decisions most affect
   the reported numerators, denominators, and unresolved mass?
4. Can intended L2 researchers complete and interpret the workflow without
   making the invalid inferences the interface is designed to prevent?

These questions are provisional until the usable vertical slice and feasible
data sources are fixed. Do not retrofit the research questions to whichever
results happen to look strongest.

## Primary coverage estimand

The primary product purpose is reference-conditioned lexical coverage, not MWE
detection for its own sake and not another general lexical-diversity dashboard.
Detection, review, and sense decisions are required only because an invalid
lexical unit produces an invalid coverage numerator and denominator.

Three coverage channels remain distinct:

| Channel | Observed unit | Reference role | Denominator that must remain visible |
|---|---|---|---|
| Word | Recognized word token, with surface/lemma/family policy fixed per profile | Frequency or dispersion distribution | All recognized word tokens in the declared text unit |
| MWE form | Confirmed MWE occurrence or distinct confirmed form, never silently mixed | Form inventory or form-frequency distribution | Confirmed occurrences for token coverage; distinct confirmed forms for type coverage |
| MWE sense | Confirmed occurrence plus explicit inventory-specific sense state | Sense inventory and, only if available, sense-frequency distribution | Confirmed occurrences for inventory coverage; matched candidates for assignment coverage |

Annotation coverage is a fourth *quality-control measure*, not a lexical-
coverage channel: confirmed plus rejected candidates divided by all candidates.
Likewise, idiomaticity is a contextual annotation dimension, not a synonym for
MWE form or fine-grained sense coverage.

No single corpus is a theory-free default. The initial resource portfolio is:

1. **TUBELEX English regex ASCII profile** for word-form frequency approximating
   audiovisual/spoken exposure. Its 410,400 forms, profile-specific tokenizer,
   source denominator, per-million formula, competition ties, unmatched policy,
   payload ceiling, rights, and removal path are admitted and exposed. It is not
   a general English, academic, written, or learner-knowledge norm and does not
   expose dispersion or MWE frequency.
2. **One exact Leipzig written-register package**, to be selected and pinned as
   a contrast rather than pooled silently with TUBELEX. News, Web, Wikipedia,
   country, year, and corpus size are construct choices; no package is admitted
   yet.
3. **OEWN 2025** for MWE-form and sense inventory membership, not corpus
   frequency. A 2,847-form multiword-verb projection is active after human
   confirmation; the separate `take in#v` projection retains all 17 candidate
   senses for fixture validation only.
4. **STREUSLE 5.0** as the pinned external English occurrence/category
   benchmark, not a general frequency baseline. The PARSEME 2.0 production
   training release has no English directory; its English trial data remains a
   format/method reference rather than a holdout benchmark. Genre, sampling,
   annotation, source-text, and ShareAlike boundaries remain visible.

[`reference_profile_template.json`](reference_profile_template.json) is the
machine-readable admission template. One completed manifest describes one
resource projection and one coverage channel, including corpus design,
preprocessing, table schema, formula/denominator, rights, hash, validation, and
removal. It is not a generic uploader or a runtime resource.

## Beyond phrasal verbs

VPC is the first automatic validation slice, not the ontology of all MWEs.
PARSEME 1.2 separately defines verbal idioms (VID), light-verb constructions,
inherently reflexive/adpositional verbs, multi-verb constructions, and VPCs.
It explicitly excludes many non-verbal idioms from its universal VMWE scope.
STREUSLE provides a broader lexical-expression layer spanning noun, verb, and
prepositional expressions, but its labels and Web-review sample do not become a
universal MWE taxonomy or frequency reference.

Idiom handling keeps four coordinates separate:

- structural category and category-scheme version;
- confirmed/rejected/unresolved occurrence status;
- contextual idiomaticity: idiomatic, literal, ambiguous, or not assessed;
- inventory-specific fine-grained sense, including abstention and
  out-of-inventory states.

The executable fixture contract admits English `VPC.full`, `VPC.semi`, and
`VID`; M5 supplies the literal/idiomatic contrast for `VID`. Do not rename every
idiom as a VPC or add an unconstrained `idiom` bucket. This synthetic contract
does not claim import/export compatibility; an applicable open annotation
format still requires a separate round-trip fixture before interoperability is
claimed.

## What TAALES does and does not settle

TAALES 2.2/2.8.1 has separate unigram and contiguous bigram/trigram indices.
Thus contiguous `take in` can receive corpus frequency, range, proportion, or
association values while `take` and `in` also receive word-level values.
However, the n-gram path does not establish that the sequence is a VPC, does not
recover `take it in`, and does not assign a contextual phrasal-verb sense. Its
polysemy path averages word/POS inventory counts; it is not contextual WSD for
`take in`. TAALES is therefore an important comparator, not the missing MWE
measurement layer.

The local evidence-vault copy confirms the distinction: its polysemy table has
separate rows for `take` and `in`, while its n-gram tables contain `take in` as
a corpus bigram. The parent OEWN 2025 derivative contains a separate `take in`
verb entry with 17 listed senses, but the parent's ordinary raw-text profile
does not detect that MWE entry. Rebuilding another unigram profile would repeat
existing work without solving the stated construct problem.

## What Multi-Word Units Profiler settles and leaves open

Eguchi's 2021 presentation describes Multi-Word Units Profiler 2.0.1 as a free
Web application for research and pedagogy. It accepts user text, lemmatizes and
parses it with spaCy, extracts contiguous n-gram and dependency candidates,
matches them against selected corpus-based MWU lists, and returns highlighted
text plus item tables. Dependency extraction is specifically used to recover
dislocated collocations. The live 2.0.1 interface currently offers the PHRASE
List, Academic Formulas List, Biber et al. lexical bundles, and Academic
Collocations List.

This is closer to the product target than TAALES and must be the primary
profiling comparator. It also sharpens the remaining gap:

- list membership is not contextual confirmation that an occurrence is an MWE;
- absence from a selected list is not evidence that an expression is not an
  MWE;
- dependency-linked collocations and English VPCs are overlapping but different
  target constructs;
- item highlighting and occurrence tables do not by themselves provide
  separate word-, confirmed-form-, annotation-, and sense-coverage
  denominators;
- the presentation identifies false positives and expert evaluation as open
  development issues, so its output must not be treated as gold annotation;
- its four list payloads have separate provenance and reuse questions, and the
  hosted form sends input text to a server.

A 2026-09-01 black-box check used only project-authored sentences. With all
four lists selected, the live app left `take in`, separated `take ... in`, and
literal/directional `take it in the car` unmarked. It did mark the listed
expression `account for` and the dependency-separated collocation
`make ... observation`. This is a reproducible behavioral observation about
those inputs and list selections, not a general accuracy estimate or proof that
the first three strings are absent from every resource.

The design consequence is reuse, not replication: retain annotated-text and
item-table views as interaction precedents; use lemma-list plus dependency
matching as the first transparent automatic baseline if browser-local or
server-side parsing is later justified; and keep human confirmation, sense
assignment, denominators, resource versions, and export provenance as this
project's added measurement layer.

The presentation also points to Tom Cobb's Lextutor Phrase Profiler. Its live
version 1.2 page matches user text against selected phrase/collocation lists,
while Lextutor's Multiwords page separately distinguishes list profiling from
n-gram and MI-based phrase extraction. It is therefore a second list-profile
comparator, especially for checking list-conditioned coverage and interface
expectations, but not evidence of contextual VPC or sense identification.

## Prior-art search protocol

Searching only for *MWE profilers* is too narrow. Constant et al.'s survey
distinguishes corpus-level MWE discovery from occurrence identification, while
this project's sense and coverage questions add further stages. Prior art is
therefore searched and compared in separate lanes:

| Lane | Question | Representative evidence reviewed | Relevance |
|---|---|---|---|
| Discovery and extraction | Which recurrent or associated word combinations should become candidates? | `mwetoolkit`, Lextutor n-gram/MI extractors, corpus platforms | Candidate generation only; recurrence or association does not confirm MWE status |
| List-conditioned profiling | Which entries from a selected pedagogical or corpus list occur in a text? | Multi-Word Units Profiler, Lextutor Phrase Profiler | Closest Web workflow, but list membership and contextual confirmation remain separate |
| Occurrence identification | Which token spans are MWEs here, including gaps and overlap? | PARSEME 1.2/2.0, STREUSLE, DiMSUM, CoAM, rule/model baselines | Core M1/M2 benchmark lane; evaluate exact spans, categories, seen/unseen items, and errors |
| Human annotation and adjudication | How are candidate, rejection, overlap, provenance, and disagreement recorded? | FLAT, INCEpTION, CAIGen | Reuse formats and external workflows; do not rebuild team management in this app |
| Idiomaticity | Is this occurrence literal, idiomatic, or unresolved in context? | MAGPIE, SemEval-2022 Task 2 | Relevant to M4, but binary idiomaticity is not a fine-grained VPC sense |
| Fine-grained form sense | Which inventory sense applies, if any? | Open English WordNet, PHaVE methodology, the English VMWE annotations, MWEasWSD | Core M3 lane; inventory lookup, WSD, and abstention must remain separate |
| L2 pedagogical priority | Which forms and senses merit teaching or testing attention? | PHaVE and academic MWU-list research | A pedagogical importance layer, not occurrence truth or learner knowledge |
| Coverage reporting | What denominator and unresolved mass does each layer expose? | TAALES, existing profilers, this project's measurement contract | Product gap: keep word, confirmed form, annotation, and sense coverage separate |

The 2026 PARSEME 2.0 shared task materially updates the multilingual method
frame: its corpus covers verbal, nominal, adjectival, adverbial, and functional
MWEs in 17 languages, and its identification subtask received ten systems
including the baseline. However, the fixed production training release has no
English directory; English appears only in the trial tree. It therefore cannot
serve as this project's current English holdout. The admitted English benchmark
is the explicit VPC/VID projection of STREUSLE 5.0, while PARSEME 2.0 remains a
format, category, and multilingual-system comparator.

Every shortlisted artifact gets one record for task, target unit/categories,
language/domain, discontinuity/overlap behavior, input/output and hosted-text
boundary, data split and seen/unseen policy, evaluation/error analysis, current
release, and separate code/data/model/list licenses. Its disposition is one of
`adopt`, `benchmark`, `interoperate`, `cite`, `quarantine`, or `exclude`.

The search stops being implementation-blocking after at least one systematic
survey, the latest relevant shared task, one L2-facing Web profiler, one open
contextual validation corpus, and one open sense inventory have been reviewed.
Thereafter, add a source only when it changes a construct, benchmark, rights, or
architecture decision. This avoids both a narrow convenience sample and an
unbounded literature hunt.

## Existing-tool boundary

MWE-related Web tools exist, but they solve different stages. In the tools
reviewed here, none supplies the complete path from researcher-provided text to
reviewed English VPC occurrences and separate word-, form-, and contextual
sense-coverage outputs.

| Existing tool | What it already covers | Boundary for this project | Decision |
|---|---|---|---|
| Multi-Word Units Profiler 2.0.1 | User-text MWU highlighting and item tables from four research-based lists using n-gram and dependency candidates | List-driven pedagogical profiling, not confirmed VPC or contextual-sense coverage; hosted processing and third-party list rights remain separate | Primary Web-profile comparator and UI/pipeline prior art; do not copy code or lists, and do not send protected research text |
| Lextutor Phrase Profiler 1.2 | User-text matching against selectable academic, idiomatic, and transition phrase/collocation lists | List lookup rather than contextual MWE confirmation or sense assignment; resource and hosted-service rights remain separate | Secondary list-profile comparator; reuse its workflow distinction, not its payloads |
| PARSEME-configured FLAT | Web-based, multi-user MWE annotation with token/span structures, provenance, confidence, permissions, and versioned documents | Annotation/review platform, not an L2 lexical-coverage or fine-sense analysis; the public PARSEME instance requires an account | Treat as the closest external annotation workflow; preserve PARSEME-compatible occurrence interchange instead of forking or embedding FLAT |
| INCEpTION | Actively maintained, open-source Web annotation, curation, configurable layers, and assisted recommendations | General-purpose rather than MWE-specific; discontinuous spans are represented through relations or links rather than native discontinuous spans | Optional external multi-annotator workflow if FLAT interchange is insufficient; no runtime dependency |
| CAIGen | Free Google Sheets/Apps Script annotation generator supporting discontinuous and overlapping spans | Depends on Google accounts/services and is an annotation collection workflow, not coverage or sense analysis | Interface and annotation-quality comparator only; no runtime or hosted-data dependency |
| PARSEME KonText and STREUSLE ANNIS | Browser search over already annotated corpora, including MWE member identifiers and discontinuous examples | Corpus exploration, not annotation or analysis of a researcher's new text | Link as audit/teaching evidence; do not mistake corpus search for a detector |
| STREUSLE recognizer, PyMUSAS, MWEasWSD, and PARSEME 2.0 baseline | Rule, neural, hybrid, gloss/context, and LLM-based identification alternatives | Predictions are not gold decisions; inventories, compute, upstream data, and licenses differ, and the LLM baseline is too slow/heavy for the static core | Benchmark a small declared set after the contract is fixed; adopt only a measured component that improves the admitted VPC task |

The missing layer is therefore a **measurement bridge**, not another generic
annotation suite. This app needs a small candidate-confirm/reject surface only
to keep analysis decisions attached to its coverage denominators. Large-team
assignment, user management, adjudication, and document versioning belong in
FLAT or INCEpTION unless a demonstrated research workflow cannot round-trip.

Interoperability is narrower than code integration. The occurrence contract
must map stable token IDs, shared occurrence IDs, member tokens, gaps, overlap,
and PARSEME category labels without loss. App-specific provenance and
fine-grained sense-assignment states may require a documented sidecar because
PARSEME occurrence formats do not by themselves encode this study's full sense
contract. No `.cupt`, FoLiA, or INCEpTION import/export claim is admitted until
a round-trip fixture proves it.

## Resource-delivery decision

A database is not the first implementation step and is not a rights mechanism.
The relevant boundary is whether an admitted resource stays server-side and
what the public API reveals. A public lookup can still be enumerated, and no
storage design creates permission for public SaaS processing or derived-output
publication.

- Open, redistributable resources should remain pinned, attributed,
  downloadable, and usable without the hosted service. OEWN fits this route.
- ShareAlike resources may be a separately licensed validation package rather
  than silently entering the permissive core. STREUSLE fits this route.
- A restricted resource may be read from an immutable server-side file/object
  store only after its exact server-use and output rights are documented. A
  database adds no protection over that boundary unless measured query or scale
  requirements demand it.
- PHaVE/COCA/TAALES-derived payloads do not become admissible merely because the
  rows are hidden behind an API. Written permission or a user-supplied lawful
  copy remains necessary where the public terms do not cover the delivery.
- Sending research text to a server is a separate privacy decision. The minimum
  useful path remains browser-local text, project-authored fixtures, open
  inventory data, and human confirmation; move text server-side only if a
  measured user need cannot be met locally and ethics/privacy review permits it.

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
| Sustainability | Can free access survive hosting or maintainer loss? | The canonical core and open resources remain downloadable; no database, account, or paid service may become the only reproducible path. |
| Interoperability | Does matching a metric name imply matching another tool? | No. Numerical equivalence requires an explicit versioned validation study. |

## Scenario matrix

| ID | Comparison | Identified change | Valid observation | Main boundary | State |
|---|---|---|---|---|---|
| M1 | `take in` as two word tokens versus one confirmed VPC occurrence | Counting channel only | Word coverage and MWE-form coverage answer different questions | A contiguous bigram is only a candidate until its use is confirmed | Contract/fixture implemented |
| M2 | `take in the explanation` versus `take the explanation in` | Continuous versus discontinuous realization | The same VPC form can have non-adjacent member tokens | Gap tokens are not MWE members | Contract/fixture implemented |
| M3 | Confirmed `take in` uses with different contextual senses | Contextual sense while form is held constant | One form can populate different sense-profile cells | OEWN supplies 17 candidates, not the contextual gold decision or pedagogical priority | OEWN 2025 candidate projection and project-reviewed assignments implemented in the non-UI fixture |
| M4 | Comprehension `took it in` versus locative `took it in the car rather than on the bus` | Contextual VPC status with the same `took`–`it`–`in` surface sequence | A pronoun can occupy the non-member gap, while identical local tokens can still require opposite decisions | Surface matching cannot decide whether `in` is a particle or heads a location phrase | Context-disambiguated confirmed/rejected fixture implemented |
| M5 | `spill the beans` in idiomatic and literal physical-spilling contexts | Contextual idiomaticity while form is held constant | Form membership, occurrence status, idiomaticity, and fine-grained sense are not interchangeable | PARSEME VID covers verbal idioms but not all non-verbal idioms; two synthetic uses do not validate a classifier | VID/category and idiomaticity contract implemented; no automatic classifier |
| S1 | Equal 100-token templates with 38 lexical substitutions | Surface repetition at fixed positions | Mechanical response of counts and TTR | Frequency, semantics, naturalness, and population effects are uncontrolled | Implemented probe |
| S2 | Identical 100-token sequence as one orthographic sentence or seven | Terminal punctuation / segmentation only | Current token-sequence metrics are invariant | This says nothing about sentence-aware metrics or natural syntax | Implemented probe |
| S3 | First 14-token sentence versus its containing 100-token text | Nested sample length plus accumulated continuation | TTR changes when the sample grows | Sentence count, length, and added lexical composition are not separately identified | Implemented probe |
| S4 | Same characters under documented tokenizer policies | Preprocessing policy | Sensitivity to apostrophes, hyphens, case, Unicode, and digits | No tokenizer is universally correct | Fixture evidence only |
| S5 | Same text under an admitted unigram or n-gram comparator | Reference distribution and coverage | Resource-conditional baseline beside MWE results | A frequent n-gram is not necessarily an MWE or a particular sense | Deferred to resource-backed validation |
| S6 | Rights-cleared public or corpus-derived text strata | Observed group/genre/time differences | Descriptive distribution with uncertainty | No causal, proficiency, or individual diagnosis claim | Blocked by provenance and design review |

The M1–M5 contract/fixture increment is complete, but automatic candidate
generation, occurrence decisions, and sense assignment are not. S1–S4 remain
useful completed scaffolding; S5–S6 must not displace MWE work. Add a scenario
only when it isolates a new decision-relevant contrast; do not add scenarios
merely to showcase another index.

## MWE contract increment

The dependency-free `mwe_contract.json`, `tests/fixtures/mwe_cases.json`, and
shared summarizer now implement the contract-and-fixture increment:

- stable one-based token IDs tied to the existing canonical tokenizer;
- member and gap token IDs, PARSEME-compatible VPC/VID categories, canonical form,
  candidate/confirmed/rejected status, and decision provenance;
- separate versioned form lookup, sense lookup, and sense-assignment states,
  including `assigned`, `ambiguous`, `abstained`, `unassigned`, and
  `out_of_inventory`;
- M1–M5 project-authored fixtures with checked expected values and explicit
  provenance for terminal contextual-sense decisions; confirmed member density
  uses the union of member IDs and excludes gaps, while every coverage result
  preserves numerator and denominator and uses `null` when undefined;
- a positive pronoun-object VPC and a locative rejection with the same local
  `took it in` sequence, proving that `it` can be a gap without making the
  surface sequence automatically confirmable;
- an idiomatic and literal `spill the beans` contrast with category,
  occurrence status, idiomaticity, and fine-grained-sense state kept separate;
- a standard-library evaluator for contextual decisions over supplied
  candidates, plus an all-confirmed surface-list negative control. Its scores
  are contract checks, not model evidence or span-detection performance;
- the separately licensed OEWN 2025 `take in#v` projection as the complete M3
  candidate set, verified against the pinned release asset rather than copied
  from an unversioned live page.

The minimum OEWN increment is now admitted: a deterministic standard-library
extractor pins the 2025 JSON artifact and retains the complete 17-sense
`take in#v` candidate set while omitting unrelated dictionary data. M3 maps its
synthetic contexts to the understanding and deception senses with separate
project decision provenance; OEWN is not represented as the annotator.

The first occurrence-validation increment is now pinned: an external-only
STREUSLE 5.0 projection checks 40 English VPC/VID test occurrences, including
16 discontinuous and 16 train-unseen occurrences. A contiguous train-lemma
surface baseline obtains exact-span F1 0.404762 and zero recall in both hard
strata. This is a transparent floor, not a detector claim or a coverage result.

The minimum single-text path is now implemented: researcher-supplied patterns
produce reviewable member/gap candidates; manual candidates and
confirm/reject/unresolved decisions are supported; TUBELEX word-token/type and
OEWN confirmed-MWE occurrence/type coverage retain separate denominators;
unmatched items, CSV, and metadata-only method JSON are exposed. The next
increment is not another resource or model. Freeze an applied-L2 evaluation
protocol and lawful sample, run real-browser/accessibility checks, and observe
whether representative researchers can complete and correctly interpret this
workflow. Only then should one dependency or contextual candidate baseline be
evaluated against the same fixed STREUSLE projection. A contextual
transformer may rerank candidates and fastText may supply a cheap static-
semantic comparator, but neither embedding is itself an MWE definition. Add a
runtime model only if it improves predeclared exact-span, category,
discontinuous, and unseen-item results enough to justify its model/data license,
download size, compute, and privacy cost. MAGPIE remains segregated for
literal/idiomatic transfer checks, and OEWN-backed cases for fine-sense
assignment. Prove a minimal PARSEME occurrence round trip only when an external
annotation workflow enters the validation study.

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

- [x] Complete the minimum useful single-text MWE-aware coverage path; do not
  release the TTR method-audit probe as the research tool described in the
  manuscript.
- [x] Admit and expose at least one word-reference profile and one MWE inventory
  with visible versions, denominators, unmatched items, and removal paths.
- [x] Export reviewed occurrence/member/gap/category/status rows as tidy CSV and
  the full method/resource/decision record as JSON.
- [x] Add a local-processing notice and researcher authorization/ethics
  attestation to the MWE path for lawfully used, appropriately governed learner
  data; obtain institutional/legal review where required rather than presenting
  the app as legal advice.
- [x] Dual-license original code, documentation, contracts, and fixtures under
  MIT or CC BY 4.0 at the recipient's choice.
- [x] Keep future third-party notices and any license-incompatible resource
  packages distinct from the original project grant.
- [x] Admit the OEWN 2025 `take in#v` projection only with an exact release
  hash, deterministic extractor, complete 17-sense candidate set, both required
  license links, attribution/modification notice, removal path, and fixture
  checks.
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
- [ ] Run predeclared task and interpretation studies with representative L2
  vocabulary researchers; include English-language teaching practitioners for
  any practitioner-usability claim.
- [ ] Freeze a confirmatory held-out set before final model selection and retain
  all prediction files needed to reproduce the reported error analysis.
- [ ] Archive the validation protocol, annotation guidelines, code, permissible
  data or retrieval instructions, analyses, release checksum, and reporting
  materials cited by the manuscript.
- [ ] Verify the current RMAL Guide for Authors, article type, declarations,
  data/code availability wording, AI-use disclosure, and submission files at
  manuscript freeze and again immediately before upload.

**Release gate:** an intended user can complete the MWE-aware task and act on
the item-level output, while a third party can reproduce a displayed value,
identify every decision/right/method dependency, and state what the result does
not establish. Reproducibility without utility, or utility without traceability,
does not pass.

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

## Release and submission sequence

1. Freeze the method claim and validation protocol before confirmatory data or
   final held-out results are inspected.
2. Complete the useful vertical slice, resource admission, technical validation,
   L2 measurement study, and representative-user study; report failures and
   unresolved cases rather than silently tuning them away.
3. Pass the real-browser and representative-user gates; freeze a version and
   move the relevant `CHANGELOG.md` entries out of `Unreleased`.
4. Confirm creator names, repository URL, release date, version, license choice,
   and archive identifier before writing citation metadata. Do not invent or
   preassign a DOI.
5. Tag the exact tracked source tree. The static app has no build product: archive
   the source, contracts, fixtures, tests, licenses/notices, citations, and
   changelog together.
6. Compute SHA-256 after the archive is final, publish the archive and checksum
   together, and never reuse the version or identifier for altered bytes.
7. Extract the published archive into a clean directory, run its documented
   checks, serve it locally, repeat the acceptance gate, and verify that no
   parent-directory or ignored evidence-vault file entered the bundle.
8. Write the RMAL manuscript from the frozen protocol, release, and analysis
   outputs. The paper foregrounds the methodological problem, operationalization,
   validation, error boundaries, and consequences for L2 research—not the UI
   implementation chronology.
9. Audit every number, table, link, citation, availability statement, ethics
   statement, declaration, and supplement against the immutable release before
   submission.

No packaging script is justified before the first version is frozen; the first
release exercise should reveal whether a repeated automation need actually
exists.

The initial tracking audit on 2026-09-01 found this directory to be the Git root
with no symlinks, file over 1 MB, or high-confidence credential signature in the
candidate source files. The local snapshot was merged with the one-line GitHub
placeholder history and pushed to the canonical repository's `main` branch;
the repository CI passed. The same `main` root is the source of the
[public technical deployment](https://ryuya-dot-com.github.io/Lexical-Diversity-Sophistication-Analysis/).
The ignored legacy MWE/VPC roadmap and Python caches are not tracked release
inputs, and LF is normalized by `.gitattributes`. Public deployment is not a
tag, citable archive, security
certification, browser acceptance, research validation, or formal release.

The canonical repository name includes “Sophistication” as a possible future
direction. The current admitted construct remains surface lexical amount,
variety, repetition, and method sensitivity; no sophistication score or
resource-dependent measure is implemented.

## Representative-user task and interpretation study

Use a justified, predeclared sample of intended users rather than a convenience
minimum of three. Without verbal coaching, ask L2 vocabulary researchers to:

1. analyze a supplied text and locate a contiguous VPC, a separated VPC, a
   rejected free combination, and an unresolved candidate;
2. correct at least one candidate decision and explain how the change affects
   each relevant numerator and denominator;
3. distinguish word coverage, MWE-form coverage, annotation coverage, and
   unresolved mass without coaching;
4. export item-level CSV and method JSON, then identify the resource, version,
   decision provenance, and text identity needed for reproduction;
5. state which proficiency, quality, population, pedagogical, and causal claims
   the result does not support.

Teaching practitioners complete a parallel task only if the paper makes a
practitioner-usability claim: identify candidate items for review and explain
why the output does not automatically determine text suitability or what must
be taught. Record task success, time, critical errors, interpretation accuracy,
and qualitative feedback under an approved ethics/data-management plan; do not
add product analytics.

## Pending real-browser acceptance gate

The required in-app browser connection was unavailable on 2026-09-01, so
structural checks and actual HTTP delivery passed but visual and assistive-
technology claims remain unverified. Before release, run this exact manual gate
in current Chromium, Firefox, and Safari plus at least one screen reader:

1. Reach every control in the minimum useful MWE-aware path by keyboard, see
   focus, review candidates, change decisions, export results, and return to the
   input without a trap.
2. Analyze one text containing contiguous, separated, rejected, and unresolved
   cases; verify highlighted member/gap tokens and every displayed denominator
   against CSV/JSON, then confirm that exports follow the declared text policy.
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

Failure of the first two items blocks any useful-tool or manuscript claim even
if the legacy TTR workspace passes every remaining check. It does not justify
adding a framework.

## Ponytail disposition

Keep the app as static HTML, CSS, JavaScript, JSON, and dependency-free checks.
Do not add R, FastAPI, Plumber, a database, accounts, queues, caches, containers,
or external models until the minimum useful product cannot run transparently
and freely without them. Do not add another model or benchmark before the
single-text MWE-aware path exists. Add BERT/fastText only after the transparent
baseline and human-review workflow are usable and a fixed evaluation shows a
decision-relevant gain. Do not create manuscript templates or submission
automation until the validation evidence and release are frozen.
