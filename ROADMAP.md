# Open contextual VPC/VID identification and sense analysis: LRE roadmap

Status: evidence-first Language Resources and Evaluation critical path, reviewed 2026-09-03

## One-minute answer

In plain language: the study asks whether an open, auditable system can locate
English phrasal-verb and verbal-idiom candidates, recover their continuous or
discontinuous boundaries, decide whether each occurrence is actually an MWE,
and identify its contextual sense without collapsing polysemy, ambiguity, or
out-of-inventory uses. Lexical coverage and eye-movement analysis are downstream
demonstrations of what the resulting occurrence-and-sense records can support.

### What problem does this study address?

The same surface form can be a genuine or accidental sequence, can separate
around an object (`take it in`), and can realize different senses across
contexts. Contiguous lookup misses separated members; dictionary membership
does not establish occurrence status; an entry count does not assign a sense;
and a model score does not erase legitimate ambiguity. Without a staged record
of candidate, span, category, idiomaticity, inventory coverage, and contextual
sense, later coverage or processing analyses inherit an unmeasured lexical-unit
error.

### What will the study do?

Develop and empirically evaluate an open, browser-local, human-in-the-loop
method that:

1. generates reviewable English verb-particle construction (VPC) and verbal-
   idiom (VID) candidates, including separated and inflected realizations;
2. lets a researcher confirm, reject, correct, overlap, or leave unresolved the
   member span, gap, category, and idiomaticity of each occurrence;
3. projects a versioned candidate-sense inventory only after occurrence
   confirmation and records one sense, multiple plausible senses, abstention,
   or an out-of-inventory result without a default answer;
4. evaluates candidate recall, exact spans, categories, sense-inventory
   coverage, sense agreement, calibration, unresolved cases, and review burden
   on separated development and held-out evidence;
5. compares a transparent baseline and, only after human gold exists, at most
   one contextual ranking model for a named task; and
6. exports stable identifiers, provenance, resource versions, decisions, and
   limitations so downstream studies can reuse the text-side analysis.

The Web app is the executable review instrument; offline scripts provide the
technical evaluation. Coverage, source-to-target recurrence, learner-text
robustness, and eye-movement analyses may consume the exported records as
separate applications, but none defines whether the core technology works.

### What will the first paper claim?

> A staged, open human-in-the-loop workflow can make contextual English VPC/VID
> identification and sense analysis auditable by separating candidate discovery,
> occurrence boundaries, category, idiomaticity, sense-inventory coverage,
> contextual assignment, ambiguity, and abstention.

That claim is provisional until technical, measurement, and intended-user
evidence pass the gates below.

### What will it not claim?

The first paper will not claim unattended automatic truth, complete English MWE
or idiom coverage, universally correct fine-grained senses, corpus sense
frequency, learner knowledge, text difficulty, writing quality, proficiency,
pedagogical priority, or causal effects. Coverage percentages, eye movements,
and model rankings cannot validate an occurrence or sense by themselves.

## Is the purpose transparent now?

At the purpose level, yes: the study is about **reproducible contextual
identification and sense analysis of English VPCs and VIDs**. Detection,
boundary correction, category/idiomaticity decisions, polysemy, uncertainty,
and human review are the method. Coverage and eye tracking are applications.

At the evidence level, not yet. A beginning graduate student should currently
be told:

- the app can demonstrate the workflow on a text;
- the app cannot yet show that its candidate method has adequate recall, that
  independent reviewers agree, or that its one-form sense workflow transfers;
- TUBELEX matching and OEWN membership are resource-conditioned lookup results,
  not estimates of what a learner knows; and
- `take in#v` is a vertical slice, not evidence of general VPC/VID polysemy
  coverage; and
- coverage, gaze, or learner outcomes can illustrate later use but cannot
  replace held-out occurrence-and-sense evaluation.

If this distinction cannot be explained without specialist terminology, the
method is not ready for participants, reviewers, or publication.

## Downstream coverage application and threshold lineage

This section constrains one important application of the technology; it no
longer defines the primary contribution. A valid MWE occurrence-and-sense map
is a prerequisite for the coverage argument, not something that coverage or
comprehension results can validate after the fact.

“Nation's 95% threshold” is useful shorthand but not an accurate attribution of
a single established cutoff. Laufer (1989) associated 95% with a greater chance
of minimal comprehension under a low comprehension criterion. Hu and Nation
(2000) found that 95% generally did not yield good comprehension and inferred
that about 98% would be needed for most learners. Nation (2006) then used 98%
as the coverage target for estimating vocabulary sizes required for unassisted
reading and listening. Schmitt, Jiang, and Grabe (2011) found a largely linear
coverage-comprehension relationship rather than a sharp threshold and judged
98% a more reasonable target for academic reading.

The recent partial replication by Kremmel et al. (2023) makes a universal
percentage still less defensible: results varied by genre and response format,
and even the 98% condition did not generally reach the stipulated 85%
comprehension criterion. The project must therefore treat 95% and 98% as
historically important reference points, not natural constants to be replaced
with another universal number.

Existing phraseological evidence supplies the missing mechanism. Martinez and
Murphy (2011) held high-frequency component words constant but found worse and
overestimated comprehension when those words occurred in MWEs. Kremmel,
Brunfaut, and Alderson (2017) found phraseological knowledge related strongly
to EFL reading and retained information beyond a traditional vocabulary
measure. These studies motivate, but do not validate, the present measurement
method.

### Core construct and downstream profile boundary

The primary target is a **context-indexed VPC/VID occurrence-and-sense record**:
which tokens are members or gaps, whether the occurrence is retained, which
category and idiomaticity apply, which inventory senses were available, and
whether the contextual decision has one sense, jointly applicable senses,
unresolved alternatives, abstention, unfinished work, semantic OOI, or
inventory ineligibility. Candidate generation and every later decision remain
separate so that recall, errors, disagreement, and missing senses stay visible.

The frozen [target-population contract](resources/target_population_contract.json)
defines candidate-independent discovery, the three included categories,
inflection, separation, gaps, overlap, literal negatives, and excluded scope.
Its human-readable [guide](ANNOTATION_GUIDE.md) now supplies a UI-independent
decision order, all current contract states, detailed occurrence/span/category
tests, tokenization exceptions, disagreement codes, a separate idiomaticity
decision tree, complete contextual-sense/uncertainty rules, a loss-aware MAGPIE
projection, and an M1–M5 fixture key. The
[synthetic occurrence/span/category cases](annotations/training_cases.json) cover
continuous/discontinuous forms, movement, pronoun/NP gaps, overlap, and
literal/spatial/accidental negatives. A synthetic hard-case bank and staged,
task-specific training/qualification protocol are also public. An unexposed
qualification form, authorized training, and an independent pilot remain
blocked; this is not a production guide.

INCEpTION is the provisional independent-annotation platform because its roles,
workload assignment, link features, curation, full-fidelity UIMA CAS JSON, and
project log cover the required separation without adding accounts or shared
storage to this app. A project-authored format fixture passes the lossless
converter for discontinuous gaps, multiple senses, OOI, and audit hashes. An
authorized managed instance must still demonstrate two-user mutual invisibility and
no first-pass suggestions; the platform task therefore remains blocked.

The following profiles are downstream uses of that record. None can substitute
for core occurrence or sense validity:

| Profile | Admitted use | Forbidden inference |
|---|---|---|
| Fixed list-to-text, such as a declared 2K list | Reproduce conventional hypothetical word coverage and create material strata | The participant knows every item in the list |
| Source-corpus-to-target-corpus, such as textbook to examination | Describe directional lexical recurrence or curricular alignment after frequency/range rules | An occurrence in the source was attended to, learned, or retained |
| Tested person-to-text | Estimate the proportion of target word and MWE occurrences whose required meanings the participant demonstrates | Comprehension is guaranteed or caused by lexical knowledge alone |

All three are optional application modes. The tested person-to-text profile is
required only for a later claim about learner knowledge or the 95%/98%
literature. ICNALE production and eye movements cannot provide it.

### Downstream application-material admission charter

Nothing below is admitted merely because it is public, convenient, previously
used, or easy to load. A candidate receives a dated record with its exact
artifact, population/domain, unit, rights, intended inference, exclusions, and
reason for admission or rejection.

| Candidate | Admit only if | Reject or redesign if |
|---|---|---|
| Reading passage and counterbalanced version | Natural English in the declared genre; lawful research and release route; several independently reviewed VPC/VID targets; stable word-profile calculation; meaning, answerability, length, syntax, cohesion, and target centrality checked across versions; text and item identifiers frozen | The MWE manipulation also changes propositional content or answer cues, one passage carries the claim, targets are artificially dense, or the release cannot be independently audited |
| Contextual single-word measure | Produces participant × text-token meaning evidence for the sense required in the passage while not testing the whole MWE; records partial, uncertain, missing, and unscorable responses; order/spacing limits phrase priming; scoring reliability can be checked | List membership, decontextualized form recognition, self-report, or knowing another sense is treated as knowledge of the required token meaning |
| Contextual MWE measure | Tests the occurrence meaning separately from component-word knowledge; distinguishes form/function recognition from contextual sense; permits ambiguity, abstention, and out-of-inventory responses; scoring and adjudication can be reproduced | Recalling the citation form, selecting a transparently cued definition, or answering a comprehension item is treated as independent MWE knowledge |
| Comprehension measure | Global passage comprehension is primary and does not require naming the target MWE; target-critical items are separately labelled; item dependence, scoring, missingness, and reliability are inspectable | Only phrase-definition or phrase-cued questions succeed, passage versions differ in answerability, or the outcome is a single unvalidated item |
| Conventional word profile | Exact list/version, word-family or lemma policy, tokenizer, cutoffs, special-list handling, rights, and artifact hash are fixed; it is labelled list-conditioned hypothetical coverage | A frequency list is relabelled learner knowledge, unlike 1K/2K units are equated, or a non-redistributable artifact becomes an undeclared server dependency |
| Source corpus A → target corpus B | Direction, sampling frames, document units, deduplication, frequency/range inclusion rule, token/MWE definition, metadata, rights, and clustering are declared for both sides | Occurrence is interpreted as exposure, attention, learning, retention, or comprehension; documents are pooled so that range and dependence disappear |

This charter applies only if a downstream application is retained. Material
length, target count, coverage bands, response timing, and reliability
thresholds remain unset; they do not block core benchmark admission.

### Dated construct decisions

| Date | Decision | Consequence |
|---|---|---|
| 2026-09-03 | The bounded exact Kaikki/Wiktionary audit rejects direct use as VID sense gold. | It adds only 60 exact verb-entry routes after OEWN, leaving 146/239 VID types without an exact route; only 5/99 raw senses have a Wiktionary `senseid`. Retain aggregate candidate evidence, keep lexical content local, and freeze project-stable IDs plus a non-exact mapping protocol before annotation. |
| 2026-09-03 | Language Resources and Evaluation (LRE) replaces RMAL as the first-paper target; the intended article is a full-length resource-and-evaluation paper. | Benchmark substantiality, independent test evidence, lawful public availability, a frozen annotation guide, and comparative baselines become submission gates. L2 coverage, learner corpora, and eye tracking remain downstream demonstrations rather than the paper's validity basis. |
| 2026-09-03 | Contextual VPC/VID identification and polysemy-aware sense analysis are the primary technology and first-paper contribution. | Candidate generation, span/category/idiomaticity validation, sense-inventory coverage, contextual assignment, uncertainty, and reviewer burden move onto the critical path. Coverage, source-corpus recurrence, learner-text robustness, and eye tracking become downstream applications and cannot supply missing technical validity. |
| 2026-09-01 | The first claim is restricted to English VPC/VID contextual knowledge in reading. | “MWE” remains the wider motivation, not the validated population of lexical units. |
| 2026-09-01 | `P_word`, `P_mwe_sense`, `G_component_only`, and `G_holistic_only` remain separate person-by-text quantities. | No adjusted coverage percentage and no rule that `take part in` counts as one or three unknown words. |
| 2026-09-01 | The 95% and 98% values are historical reference points, not universal discontinuities. | Analyze coverage continuously and report those points only for interpretation. |
| 2026-09-01 | The Web app maps and reviews the text; separately governed study code joins participant responses and comprehension. | No participant testing, proficiency inference, or eye-tracking analysis is added to the app. |
| 2026-09-01 | Nation BNC/COCA is the local conventional sensitivity baseline; NGSL is an open-list contrast; TUBELEX is an exposure-frequency contrast; OEWN supplies inventory candidates only. | Resource outputs cannot substitute for contextual occurrence, sense, or learner-knowledge evidence. |
| 2026-09-01 | Current development is exploratory; prospective registration is reserved for a genuinely untouched criterion study. | Preserve decision history now, then freeze hypotheses, measures, split, exclusions, and success criteria before holdout access. |
| 2026-09-01 | Contextual models, ICNALE production robustness, and eye-movement analyses were initially treated as conditional side lanes. | Contextual models remain deferred; the 2026-09-02 existing-data-first decision promotes eye-corpus admission and a residual-gap audit while preserving their inability to measure `P_mwe_sense` directly. |
| 2026-09-01 | Cross-sense recurrence alone does not admit a reading passage. | A target must also be non-trivially cued and important to global comprehension; otherwise retain it only as a diagnostic sense case. |
| 2026-09-01 | Original pedagogical marking is part of the material, not disposable page furniture. | A bolded or gloss-defined expression is ineligible as an unmanipulated hidden-burden target; removing the cue must be declared as a material manipulation. |
| 2026-09-01 | Target-form queries may find detector diagnostics but cannot admit reading materials. | Freeze a source/date frame and inspect texts in a deterministic target-blind order; failure of the bounded frame triggers a design pivot, not wider phrase hunting. |
| 2026-09-02 | All four recurrence-triaged VOA passage pairs fail preliminary occurrence-level review; a manual `find oneself` pair also falls outside the VPC/VID scope under PARSEME 1.2. | Run one bounded out-of-inventory audit, and then stop or redesign the frame instead of broadening the construct or lowering the repeated-target rule. |
| 2026-09-02 | The bounded non-OEWN audit leaves every remaining VOA article pair with at most one shared candidate even under a deliberately generous upper bound. | Stop the frozen 24-article VOA frame with no passage or app change; freeze a new sampling design before further acquisition or annotation. |
| 2026-09-02 | Route 2 is frozen before new article-text acquisition: a dated Simple English Wikipedia dump, six externally derived targets, deterministic queues, three passages/two meanings per successful target, and a 20-page stop rule. | The material sample is openly target-conditioned and cannot estimate MWE prevalence or representative lexical coverage; Gate 1 needs at least three VPCs, one VID, and one naturally discontinuous VPC. |
| 2026-09-02 | The Route 2 desk limit applies to the first 20 **mechanically eligible** pages per target, not blindly to each queue's first 20 rows. | Follow the already frozen rank order through length/rendering exclusions: 509 target rows yielded 120 desk rows across 119 pages. This corrects an implementation label without changing a candidate, rank, target, or criterion. |
| 2026-09-02 | `take in` fails its frozen Route 2 desk screen: 28/28 gap leads are false spans and exhaustive inspection of 41 take-head tokens across 20 articles finds no missed occurrence. | Do not extend the queue or repair the detector mid-study. All three remaining VPC targets must pass for the minimum three-VPC panel to remain possible. |
| 2026-09-02 | `pick up` provisionally passes at the frozen early stop: ranks 1, 2, and 4 supply three operational meanings and two discontinuous occurrences; rank 3 is rejected for acute violence. | Preserve the deterministic selection, assign the cross-target rank-4 page to higher-priority `pick up`, and proceed to `give up` without app or sense-inventory expansion. Ranks 5–20 were viewed after the formal boundary but cannot affect or replace the selection. |
| 2026-09-02 | The original `give up` review reaches its v1 early stop at rank 15 after confirming 15 occurrences and four false gap leads in 35 `give` heads. | Preserve ranks 3, 5, and 15 as the result under the original low-risk rule and disclose that rank 16 was also viewed but not labelled. Do not mistake content sensitivity for MWE or sense invalidity. |
| 2026-09-02 | Objective lexical evidence and Web-app analysis must be content-neutral. Death, violence, coercion, persecution, or another negative topic may be sensitivity metadata but cannot by itself erase a lawful occurrence or sense. | Stop Route 2 v1 before `come out`. The counterfactual selections are `pick up` ranks 1/2/3 and `give up` ranks 1/3/5, but they cannot be relabelled as prospectively prespecified. Because the withdrawn target filter also excluded `pass away` and changed the VID pool, freeze a new target derivation and queue before more page review. |
| 2026-09-02 | Existing participant data must be exhausted before any new L2-reader recruitment. | Use TECO first for Japanese-L2 passage processing and ROI/layout evidence; audit MECO-L2 and CELER for cross-population triangulation; use ICNALE only for production/error robustness. Recruitment is no longer an active milestone and is permitted only if a retained stronger claim requires occurrence-specific word/MWE knowledge that no admitted dataset measures. |
| 2026-09-02 | Natural materials have two non-interchangeable jobs. | Analyze the exact stimuli paired with existing participant data; use a bounded, target-blind Project Gutenberg frame for openly releasable natural prose and app/annotation evidence. Gutenberg text cannot supply participant outcomes, while restricted stimulus text need not be republished to be analyzed locally. |
| 2026-09-02 | The Project Gutenberg frame must be fixed before seeing ebook text or MWE yield, and US availability is not Japanese or worldwide clearance. | Use the pinned weekly catalog only: two explicit English-fiction audience strata, SHA-256 order, 40 rights/unit screens and a ten-unit stop per stratum. Rights review precedes mirror/robot acquisition; content and MWE presence never reorder the queue. The first ten ranks per stratum have metadata-only triage: 13 advanced, five are held for likely active Japanese terms, and two for unresolved creator identity/death. The 13 exact electronic files now have pinned identities, standard notices, and front-matter review; no added retained textual contributor was found, five print-publication statements remain incomplete, five files report transcription choices, and nine boundary-location exposures are disclosed. All 13 proceed only to the mechanical first-unit gate; none is admitted and no MWE search ran. |
| 2026-09-03 | The first Gutenberg unit gate has low yield and must not be repaired after observing lengths. | Of 13 exact first units, two pass mechanically (one per stratum), ten exceed 2,000 project tokens, and one in-range `INTRODUCTORY` section is excluded as an ambiguous prespecified unit type. Do not truncate, skip to a later chapter, or raise the maximum. Continue fixed-order rights/unit screening to rank 40; if either stratum remains below ten, stop and freeze a new design. Mechanical pass is not release clearance or admission. |
| 2026-09-03 | Missing author death data and genuine pseudonymous publication are different rights cases. | Apply Japan's publication-based term only when evidence establishes anonymous/pseudonymous publication and no author-identity exception; do not assume an unexplained name is a pseudonym. In ranks 11–20, `Roy Rockwood` and `Quincy Allen` advance on work-specific publication evidence, while `Frank Walton` remains held. The batch yields 17 local-notice candidates, one likely-active term, and two unresolved identities; none is globally cleared or admitted. |
| 2026-09-03 | Front matter can invalidate a metadata-only rights assumption and can itself contain the first retained prose unit. | Batch 2 sends 16 files to the unit gate and holds Project Gutenberg 6655 because its photoplay adaptation omits the source film's three story credits. Treat five source-authored prefaces, introductions, or reader addresses as the first unit rather than skipping to a chapter; exclude two producer-added synopses. Topic and MWE yield remain irrelevant to both decisions. |
| 2026-09-03 | The second Gutenberg gate confirms that low yield is structural, not an isolated first-batch accident. | Of 16 ready first units, only the 1,743-token juvenile chapter 70572 passes; nine intact chapters/stories are overlength and six have unfrozen unit types. Combined yield is 3/29, split 1 adult/unspecified versus 2 juvenile. Continue ranks 21–40 without truncation or later-unit substitution; if either stratum remains below ten, freeze a redesigned sampling rule and report this failed design unchanged. No target/MWE search or admission precedes that decision. |
| 2026-09-03 | Search interfaces can leak outcome-relevant prose during otherwise content-blind rights work. | Ranks 21–30 yield 15 local-notice candidates, three likely-active terms, and two unresolved identities. Search rendering incidentally exposed `take in` for frozen candidate 36833; disclose it, but do not discard or favor the row, change the mechanical rules, or inspect further yield. Acquire only the 15 allowed files for notice/front-matter review next. |
| 2026-09-03 | A successful Project Gutenberg notice check is an artifact-identity gate, not release clearance. | All 15 allowed batch-3 files have pinned URL, bytes, server time, and SHA-256 and pass notice, boundary, and license-marker checks; one preamble names an original publication and all include Credits. Keep source files local, review post-START front matter next, and do not inspect MWE yield or admit a unit. |
| 2026-09-03 | Underlying-source credits and source-authored opening matter cannot disappear during front-matter cleanup. | All 15 batch-3 files reach the unit gate, but `Going Some` retains Paul Armstrong's separately rights-reviewed play contribution. An opening letter, introduction, and foreword remain first units; two electronic-producer synopses are excluded. Boundary review incidentally exposed `give up` in 63142 and `take in` in 36833 without search or classification; fixed order and boundaries prevent selection effects. |
| 2026-09-03 | The third Gutenberg gate improves yield without satisfying either frozen stratum stop. | Seven of 15 first units pass mechanically: two adult/unspecified and five juvenile; five are overlength and three have unfrozen unit types. Combined yield is 10/44, split three adult/unspecified versus seven juvenile. Screen exact ranks 31–40 next without truncation, later-unit substitution, target/MWE search, or rule relaxation; any remaining shortfall at rank 40 requires a separately frozen redesign. |
| 2026-09-03 | The final Gutenberg rights prefix proves the frozen open-material frame futile before further acquisition. | Ranks 31–40 yield 13 local-notice candidates, five likely-active terms, and two unresolved creator/death terms. Only five adult/unspecified files can advance, so the stratum's generous ceiling is `3 + 5 = 8`, below the frozen ten-unit stop. Acquire no batch-4 ebook, preserve the failed frame unchanged, and freeze a redesigned sampling rule before any MWE inspection. |
| 2026-09-03 | Source IDs and gloss hashes cannot serve as stable hybrid sense truth. | Freeze contract `1.0.0` (SHA-256 `5d84cb2ec68466f8f2b095f38da23c345a8a93aade4c0bd71eee2b0b8d2f8843`) with opaque project type/sense IDs, immutable artifact/record fingerprints, explicit mapping relations, merge/split/version rules, layer-specific rights, and distinct unresolved/ambiguous/abstained/out-of-inventory states. The residual 146-VID pass is source-bounded and stops without a target coverage quota. Type records preserve multiple observed categories and mixed source/project-defined inventories because one canonical form need not have one context-invariant VPC/VID label or one uniform source route. The contract contains no lexical entries and does not change runtime `0.10.0-mwe`. |
| 2026-09-04 | A bounded dictionary miss is not a true inventory gap. | Execute the frozen nonexact pass over all 146 residual VID types with hash-pinned OEWN and Kaikki artifacts. Three types receive closed, unreviewed candidate sets and 143 stop as `unresolved/no_bounded_route`; no type becomes mapped or OOI and none leaves the denominator. Publish only the attributed identifier/fingerprint projection and guide, not source wording or raw records; keep Kaikki candidates out of the admitted inventory until the underlying dump hash, imported-content review, and independent semantic review are complete. |

No natural passage or secondary dataset is yet admitted to a project analysis.
Candidate resources and variables have been verified, but that is not an
analysis result. This charter governs selection; it does not make absent
evidence appear complete.

### Falsifiable hypothesis

The primary method hypothesis is that a fixed candidate-and-review workflow can
recover English VPC/VID occurrences—including discontinuous and unseen forms—and
produce reproducible contextual-sense decisions while preserving false
candidates, boundary corrections, ambiguity, abstention, and out-of-inventory
uses. Its value must be demonstrated by held-out span/category results,
independent contextual-sense decisions, error strata, and reviewer workload;
the existence of a working interface is not confirmation.

The hypothesis fails in a scientifically useful way if candidate recall is too
low, agreement collapses on ordinary polysemy, the admitted inventory omits too
many contextual senses, human correction is impractical, or performance fails
under a declared domain/type split. Failure narrows the system to a transparent
annotation aid; it must not be hidden by reporting only resolved cases or one
aggregate score.

The former directional prediction about component-only gaps and reading
comprehension remains an optional downstream application hypothesis. It cannot
serve as evidence that the preceding occurrence or sense decisions are valid.

## Contribution hierarchy

The project previously allowed three possible papers to compete. The hierarchy
is now fixed.

| Rank | Contribution | Role in the first LRE paper |
|---|---|---|
| 1 | Staged VPC/VID occurrence and contextual-sense identification | Primary methodological contribution |
| 2 | Held-out span/category/sense evaluation, uncertainty, and error analysis | Required technical validity evidence |
| 3 | Open browser implementation with auditable human decisions and exports | Executable method |
| 4 | Intended-researcher task, interpretation, and burden evidence | Required response-process evidence |
| 5 | Lexical-coverage consequence | Optional applied illustration |
| 6 | Eye-movement/ROI consequence | Optional applied illustration |
| 7 | Source-to-target corpus alignment or learner-text robustness | Optional transfer illustration |
| 8 | General lexical diversity or sophistication | Out of scope |

The planned manuscript is a full-length language-resource-and-evaluation paper
about a bounded MWE identification-and-sense workflow, not a feature tour,
corpus dump, or pedagogical intervention study. The LRE
[scope](https://link.springer.com/journal/10579/aims-and-scope) explicitly
covers corpora, lexica, dictionaries, annotation tools, benchmarking, and
usability. Its current
[submission guidelines](https://link.springer.com/journal/10579/submission-guidelines)
require full-length papers to report original substantive resource research or
a new and substantial major resource, describe creation and evaluation, and
compare similar resources where appropriate. They also ask that described
resources be publicly available or that non-availability be explained, and
require a Data Availability Statement for original research. The article is
therefore not eligible merely because the browser app works. At least one
downstream L2 illustration may show reuse, but it cannot substitute for a
substantial, independently evaluated, lawfully releasable core resource.

### LRE five-part submission gate

The machine-readable
[LRE readiness audit](resources/lre_submission_readiness_2026_09_03.json)
records the current evidence and pass conditions. All five rows must pass for a
full-length-paper claim; the journal publishes Project Notes, but that fallback
must not be used to call an interim prototype a validated major resource.

| Dimension | Current evidence | Full-length pass condition | State |
|---|---|---|---|
| Benchmark scale and diversity | STREUSLE supplies 624 VPC/VID occurrences, but only 40 each are development and test. For the 239 VID types, OEWN exact plus unique simple-slot lookup supplies 33 unreviewed routes; exact Kaikki/Wiktionary lookup adds 60, leaving 146 without an exact route. The combined upper bound is 93/239 types and 150/319 occurrences, with only 28 types exposing multiple inventory candidates. The separate contextual-sense slice has 23 rows/18 types/10 documents, zero VID, zero `take in`, and one form with cross-occurrence sense contrast. | Freeze the population, sampling frame, primary metrics, strata, and clustering units; use pilot-based simulation/resampling to obtain 95% interval half-widths no greater than .05 overall and .10 for each inferential stratum; withhold any claim for a stratum that misses its target. Do not select exact matches alone: define project-stable IDs and distinguish resolvable mapping mismatch from genuine inventory gaps. These are project gates, not LRE-mandated sample sizes. | **Blocked** |
| Independence | The current gold sources are externally authored, but this project inspected both the STREUSLE test projection and WSD source-test labels. There are no independent project pre-adjudication labels. | Separate pilot/development/test documents; use a form-disjoint test only for a declared unseen-form claim; hash and seal final labels under a non-developer custodian; obtain and retain at least two independent pre-adjudication labels for every final test item, then compute task-specific agreement before adjudication. | **Blocked** |
| License and availability | Original code/docs and OEWN projection have declared licenses; STREUSLE remains an attributed external ShareAlike corpus; the WSD archive has no explicit redistribution grant. The Kaikki audit commits aggregates only: its mutable URLs and Wiktionary obligations prevent direct admission. | Select the release route before annotation; publish the core benchmark under a controlling license and persistent identifier, or lawful standoff annotations plus immutable source IDs/hashes and reconstruction code; retain third-party notices and publish a layer-specific Data Availability Statement. A private database is not a rights grant. | **Partial; core release blocked** |
| Annotation guide | Version 0.5 completes standalone occurrence/span/category/idiomaticity/contextual-sense rules, 12 synthetic cases, and a ten-case hard-case bank. The public training protocol separates teach-back, practice, feedback, and task-specific qualification with one retry and no combined score. It has not been administered; no qualification, agreement, or adjudication evidence exists. | After the annotation work relationship, rights, payment, and data route are fixed—and ethics review only if the activity is human-participant research—materialize an unexposed synthetic qualification form, run the training-only pilot, freeze the production guide, and report span, category, idiomaticity, and sense agreement separately. | **Blocked; guide and training protocol complete, human evidence absent** |
| Baselines and comparison | The contiguous train-lemma floor has exact-span F1 .404762 and zero discontinuous/unseen recall. The frozen transparent gap/dependency comparator reaches development exact-span F1 .426667 and discontinuous recall 8/14, with rule/token/arc audit output; unseen recall remains zero. No sense baseline or reproduced competitive system is frozen. | Apply the frozen transparent comparators without retuning to the future project split, then reproduce one published system only if the measured residual gap justifies it; for sense, score train-only MFS and deterministic gloss/rule ranking before at most one contextual model. Report task-specific intervals, human burden, and a task-aware resource comparison with STREUSLE, MAGPIE, PARSEME, and MWEasWSD. | **Partial; IR-221 implementation complete, project evaluation blocked** |

Changing the journal does not relax theory or validity. It changes the central
theoretical obligation from an account of L2 learning to explicit linguistic
constructs, resource design, annotation reliability, evaluation validity, and
comparison with prior MWE/WSD resources.

## Keep three work products separate

The project has three connected outputs, but they are not one application.

| Output | Job | Must not become |
|---|---|---|
| Browser-local Web app | Import authorized text; surface and correct VPC/VID candidates; record members, gaps, category, idiomaticity, contextual sense, ambiguity, and abstention; export every decision | An eye-tracking analyzer, participant-testing platform, or automatic truth machine |
| Offline core evaluation | Evaluate candidate recall, exact spans, categories, sense-inventory coverage, contextual decisions, error strata, reviewer burden, and at most one model-assisted ranker | A hidden runtime service required to use the Web app |
| Downstream applied studies | Reuse stable occurrence/sense IDs for coverage, source-corpus recurrence, learner-text robustness, eye movements, or comprehension | Evidence that retroactively validates the core labels or a required feature of the Web app |

Nahatame/TECO-style eye-movement analysis, ROI construction, participant
proficiency models, ICNALE error analyses, and criterion-study statistics stay
in separate analysis code. The Web app only needs stable document, token,
member, occurrence, and sense identifiers so that authorized external data can
be joined without copying those analyses into the interface.

A contextual model also starts in the offline lane. It may enter the Web app
only as an optional, versioned candidate-ranking aid after the admission gate
below. The core app must remain useful with no model, server, database, account,
or network call.

## Current truth, without promotional language

| Area | What exists | What is still absent |
|---|---|---|
| Product | Static browser-local single/paired/batch descriptive workspace; resumable single-text and 1–20-document named MWE review; explicit TUBELEX/NGSL/bounded local BNC/COCA word-profile selection; candidate correction; confirm/reject/unresolved states; idiomaticity review; `take in` sense review; CSV, metadata JSON, and raw local workspace JSON | A complete researcher workflow: sense inventories for benchmark-admitted forms, an MWE-only start path (the current prototype still requires a downstream word-profile selection), real-browser/accessibility evidence, and intended-user evidence |
| Word reference | Pinned TUBELEX English regex frequency profile, selectable NGSL 1.2 first-1K/2K/full ranked-list profile, and exact hash-validated local Nation BNC/COCA Level 6 first-1K/2K word-family profile | A distributable conventional baseline remains blocked by artifact-specific license mapping; special-list sensitivity and natural-text method evidence remain absent |
| MWE reference | Pinned OEWN 2025 multiword-verb inventory projection | MWE occurrence frequency/range profile and contextual sense-frequency profile |
| Candidate method | Researcher-supplied surface-member patterns plus manual candidates | Validated default candidate generator and an estimate of missed occurrences |
| Contract | Separate word, MWE-form, idiomaticity, sense, and annotation states; runtime review controls; privacy-reduced method export; exact-contract and source-hash-validated single/document-set re-import | Evidence that users understand and reliably apply the states |
| Technical evidence | Five project-authored fixtures; 40-occurrence STREUSLE projection; transparent surface and frozen gap/dependency baselines; hash-pinned 23-occurrence/18-type standard-WSD conditional sense slice | Adequately powered target-wide occurrence/sense evaluation, full error analysis, and transfer to selected reading materials |
| Sense support | The runtime loads all 17 OEWN `take in#v` candidates, displays glosses/examples, distinguishes `assigned`, `multiple_assigned`, `ambiguous`, `abstained`, `out_of_inventory`, and `inventory_ineligible`, and exports candidate and decision provenance | Natural independent gold, inter-annotator evidence, broader selected target forms, sense frequency, and any validated automatic ranking or WSD |
| Contextual models | None in the browser or offline evaluation path | A frozen task, human gold, transparent baseline, held-out comparison, calibration/abstention evidence, and a deployment decision |
| Research data | Synthetic cases, a 40-occurrence external STREUSLE projection, and a 23-occurrence external WSD sense-only slice with six development and 17 source-test rows already exposed during audit; TECO v1.1 metadata/joins plus 43 provisional VPC/VID occurrences remain a later eye-movement application | Adequate target-wide independent occurrence/sense evidence, ambiguity/abstention/out-of-inventory labels, full technical error analysis, and reviewer evidence |
| Open science | Public source, tests, rights ledger, static deployment, dated construct decisions, and changelog | Immutable release, DOI/checksum bundle, participant-analysis scripts, permissible materials, and report |

The public prototype is therefore an **implemented method hypothesis**, not a
validated research instrument.

### Strategic bottleneck and work-in-progress rule

The software is no longer the main bottleneck. The document-set workflow now
makes a bounded study possible; it does not make the method valid. The critical
unknowns are candidate recall, boundary/category error, inventory coverage,
contextual-sense agreement, ambiguity calibration, cross-form/domain transfer,
and human correction burden. TECO outcomes, Gutenberg passages, coverage bands,
and new runtime features do not resolve those unknowns.

Until those unknowns are tested:

- keep only one active critical-path work package;
- freeze new runtime features except defects, accessibility failures, or a need
  demonstrated by the admitted material/annotation pilot;
- add sense entries only for forms admitted by the frozen core evaluation set;
- do not add BERT, fastText, another word list, MWE frequency data, a server, or
  a database before the core benchmark identifies a named deficit; and
- let a failed gate narrow the claim before it expands the software.

Calendar dates would be false precision before material/data access, rights
review, and annotator availability are known. Recruitment capacity is relevant
only if the residual-gap decision later authorizes new data collection. The
roadmap is therefore dependency-gated; attach owners and dates only to the next
gate.

### Submission claim ladder

| Ceiling | Evidence available | Permitted claim | Disposition |
|---|---|---|---|
| Demonstration | Synthetic fixtures and passing software contracts | The proposed workflow is executable and auditable | Not sufficient for an LRE full-length paper |
| Resource feasibility | Natural development evidence, an annotation-guide pilot, browser acceptance, and preliminary agreement | Researchers can create and inspect bounded English VPC/VID occurrence-and-sense records | At most a Project Note candidate; not a validated benchmark |
| Validated resource and method | A substantial lawfully releasable benchmark, sealed held-out span/category/sense results, inventory coverage, uncertainty, error strata, and reviewer burden | The released resource and workflow provide an auditable and empirically characterized VPC/VID identification-and-sense method | Required first-paper ceiling for the intended LRE full-length route |
| Applied reuse | The validated resource plus one separately governed coverage, learner-text, source-corpus, or processing study | The released records support the named application in the sampled domain | Optional reuse evidence; not needed to define technical truth |
| Model-assisted method | Independent gold and held-out evidence that one contextual ranker improves accuracy, calibration, or review effort over a transparent baseline | The model assists the named candidate or sense-ranking task under the tested conditions | Does not authorize unattended automatic truth |

Do not postpone a defensible exploratory methods paper merely to manufacture a
confirmatory label. Conversely, do not use a small feasibility pilot to imply a
new universal threshold. The evidence determines the ceiling.

The machine-readable [claim–evidence–artifact map](resources/claim_evidence_map.json)
is the claim ledger for this ladder. It assigns every retained claim to exactly
one of construct, resource, technical, response-process, or downstream evidence;
records its current ceiling, required evidence, and release artifact; and states
the inferences that remain prohibited. A shared source file transfers no support
between those categories unless its role is separately named in the map.
Changes to claims, taxonomy, sources, splits, metrics, inventory, and release
governance are append-only records in the
[decision log](resources/decision_log.json). After test exposure, a changed rule
starts a new version or remains explicitly post hoc; it never rewrites the same
evaluation.

### Minimum useful Web app before downstream application studies

The following is the first usable instrument, not an optional feature list.

| Priority | Capability | Minimum exit test |
|---|---|---|
| P0 | Complete occurrence review | A researcher can confirm/reject/correct a VPC/VID, edit discontinuous members/gaps, assess idiomaticity, and preserve unresolved cases |
| P0 | Contextual sense review | For an admitted target sense inventory, the interface shows sentence/passage context plus candidate glosses/examples and records one sense, multiple plausible senses, abstention, or out-of-inventory |
| P0 | Lossless research export | CSV/JSON preserve word-profile identity, candidate source, members/gaps, form lookup, idiomaticity, sense candidates/selections, notes, unresolved states, and stable identifiers |
| P1 | Recoverable document-set workflow | A researcher can process named passages without pooling them, re-import source text plus each review record after a hash check, and continue locally without an account or database |
| P1 | Usable candidate start | A frozen target-scope candidate baseline is available without requiring a novice to author every TSV pattern; manual addition remains available and missed-occurrence recall is reported |
| P1 | Intended-user evidence | L2 vocabulary researchers can complete, resume, export, and correctly interpret declared tasks; keyboard and screen-reader basics pass |
| P2 | Honest coverage illustration | If retained, the report runs a frozen conventional profile and labels every word/MWE denominator as a downstream application rather than core validation |

Batch dashboards, collaborative accounts, a general annotation platform,
pedagogical recommendations, and automated participant testing are not needed
for the first paper. Existing tools should be used if those needs arise.

### Real-browser acceptance gate

Run this gate from a clean checkout before Gate 2 can pass. Test one current
Chromium browser and one current non-Chromium browser, using only
project-authored text. Record the commit, browser/OS versions, date, tester,
viewport, zoom, result, and a redacted failure note; never retain submitted
learner text in the evidence record.

1. **Keyboard:** reach and operate every input, review action, save/import, and
   export control in a logical order, with visible focus and no keyboard trap.
2. **Core result:** analyze the frozen `take it in` fixture under TUBELEX and
   one conventional profile; confirm the occurrence, idiomaticity, and sense;
   then verify the displayed and downloaded values against the tested Node
   contract.
3. **Lossless resume:** save the local workspace, reload/reset the page,
   re-attest, and import it. Text, profile, pattern, occurrence, member/gap,
   review, idiomaticity, sense, note, and identifiers must match. A wrong
   contract/resource or tampered occurrence must be rejected without replacing
   the open work.
4. **Local restricted profile:** the exact generated BNC/COCA profile must
   enable its declared cutoffs; wrong size or hash must fail closed.
5. **Reflow:** at a 320 CSS-pixel viewport and, separately, desktop 400% zoom,
   controls and content must remain operable without two-dimensional scrolling,
   except intrinsically two-dimensional data tables.
6. **Screen reader:** with one documented desktop browser/screen-reader pair,
   headings, labels, groups, focus, status changes, validation errors, and
   blocking errors must be perceivable in task order.
7. **Privacy:** browser network and storage inspection must show no submitted
   text leaving the same-origin static app, no analytics or third-party runtime
   request, and no persistence beyond the explicit downloaded workspace.

Any data loss, changed restored decision, inaccessible required control,
unannounced blocking error, unexpected persistence/network transmission, or
calculation mismatch fails the gate. Fix the cause and rerun the whole affected
browser row; do not average failures into a pass. This is an instrument check,
not evidence that researchers interpret the constructs correctly.

### Polysemy: implement the claim already present in the contract

`sense_count = 17` for `take in#v` establishes only that OEWN lists 17 entries.
It does not determine which sense occurs in “take it in,” whether the use is
idiomatic, how frequent that sense is, or whether a learner knows it. The
current contract and fixtures preserve this distinction, but the current Web
app operationalizes it only as a human-reviewed `take in#v` vertical slice.

The minimum implementation is human-first:

1. admit a rights-cleared, versioned sense projection for the deliberately
   bounded VPC/VID target set, or accept the same schema as a local researcher
   import;
2. after occurrence confirmation, display the full local context and the
   candidate sense identifier, gloss, and example without selecting a default;
3. record `assigned`, `ambiguous`, `abstained`, `unassigned`, or
   `out_of_inventory` separately from `idiomatic`, `literal`, `ambiguous`, or
   `not_assessed`;
4. export both the candidate set and the human decision with inventory/model
   version, source, note, and unresolved status; and
5. evaluate contextual-sense agreement and adjudication separately from span,
   category, literalness, and participant knowledge.

Items 1–4 now run in the browser for `take in#v`; item 5 and expansion to the
eventual passage-pilot target forms remain open. An unlisted form is reported as
`not_attempted`, not falsely labelled out of inventory.

Do not load the whole dictionary merely because it exists. Start with the
forms and senses admitted to the core development/holdout protocol, measure
inventory coverage and reviewer burden, and widen only when the error analysis
shows that a bounded projection is inadequate. No
MWE-sense-frequency percentage is permitted until a corpus sense-frequency
resource and its sampling claim are independently admitted.

### BERT/fastText: conditional core comparators, not semantic truth

No BERT-family or fastText model is currently implemented. Adding the model
name to the interface would not expand the construct: embeddings do not prove
MWE status, contextual idiomaticity, learner knowledge, or comprehension.

| Possible task | First comparator | Model considered only if needed | Forbidden use |
|---|---|---|---|
| Candidate discovery/ranking | Frozen surface/rule baseline plus manual additions | One contextual ranker after missed-occurrence and workload analysis | Silently treating every high score as an MWE |
| Contextual sense ranking | Human-visible complete candidate list plus lexical context/gloss-overlap baseline | One BERT-family ranker trained/evaluated on independent contextual decisions | Automatic sense “truth,” most-likely-sense substitution, or learner-knowledge inference |
| Spelling/variant retrieval | Exact matching plus an explicit researcher normalization map | fastText only if learner-error recall is a retained question and simple variants fail | Silent correction of learner text |
| Coverage/comprehension | Frozen formulas and participant evidence | None | Using embedding similarity as word/MWE coverage or comprehension |

Admission proceeds in the shortest defensible sequence:

1. freeze the passage-pilot target forms, extend the existing manual
   contextual-sense workflow only to those forms, and create independent,
   double-reviewed development/holdout decisions;
2. freeze one transparent lexical baseline;
3. if review burden or ranking error remains material, evaluate at most one
   contextual model offline with document-separated and, where the claim
   requires it, lexeme-separated holdout data; compare top-*k* recall,
   calibration/selective risk, subgroup errors, review time, and post-review
   error—not development accuracy alone;
4. record model/weights/data licenses, version/hash, payload, latency, memory,
   privacy, and reproducibility; and
5. expose only ranked suggestions with confidence/abstention and human override
   if the held-out benefit justifies those costs.

Default deployment remains model-free and browser-local. If a useful model is
too large for that boundary, keep it as an optional Python preprocessing step
that emits the existing import schema; do not create a server solely to host
BERT. If the human workflow is already accurate and tolerable, skip the model.

### Kyle and Eguchi corpus precedent: comparator, not BERT gold

The [Kyle and Eguchi (2021) analysis
repository](https://github.com/kristopherkyle/dependency_bigrams_Kyle_Eguchi_2021)
must be used before inventing a new document-level sophistication comparator.
The public artifact inspected on 2026-09-01 contains an R Markdown analysis, a
rendered HTML report, and a 480-row, 48-column table with file identifiers,
holistic scores, word counts, and word/bigram/dependency-index summaries. It
does **not** contain the source essays, token/span annotations, VPC/VID
decisions, idiomaticity, or contextual senses. The R Markdown also reads a
`5_mc_refined_dataset.csv` file absent from the four-file public `data`
directory, and no explicit repository license was located.

This evidence lowers the cost of specifying a transparent **document-level
production comparator**; it does not supply examples for BERT fine-tuning or a
reading criterion. If the original TOEFL essays can be obtained under terms
that cover the planned analysis, they may support an optional L2-production
stress test of tokenization, parsing, candidate yield, and model ranking. Any
BERT VPC/VID task still requires a separately sampled, double-reviewed set of
occurrence spans, gaps, categories, idiomaticity, contextual senses, and
unresolved cases. Split it by document and, where inference requires, target
form; never use the holistic writing score as MWE truth, contextual knowledge,
or reading comprehension. Until artifact permission is resolved, cite the
method and inspect the public outputs but do not copy them into the app or
release.

### Reference resources: use each source for one job

Vocabulary lists are available, and dictionary data are useful, but they answer
different questions. The first-paper resource plan is now:

| Role | Selected route | What it can support | What it cannot support |
|---|---|---|---|
| Occurrence/category benchmark | Pinned external STREUSLE 5.0 VPC/VID projection, followed by an artifact-level audit of the exact corpus release | Contiguous/discontinuous occurrence, span, gap, and VPC/VID category evaluation | Literal negatives, representative L2 English, or OEWN-compatible fine-sense truth |
| Contextual fine-sense benchmark | Hash-pinned multiword-verb slice of the Raganato et al. standard WSD framework, restricted by one-category STREUSLE type overlap and lossless OEWN mapping | A 23-row conditional sense-ranking smoke test: six development and 17 fixed source-test rows | Source-test labels were inspected during audit; no blinded claim, occurrence/member-span score, VID or `take in` test row, unseen-form claim, or ambiguity/abstention/out-of-inventory calibration |
| Dictionary/sense inventory | Open English WordNet 2025 under CC BY 4.0 plus the underlying WordNet notice | Lemmas, parts of speech, stable sense IDs, synsets, glosses, examples, and candidate senses for admitted word/MWE forms | Frequency, CEFR, contextual sense truth, learner knowledge, or proof that a surface occurrence is an MWE |
| Downstream historically aligned word-family baseline | Nation's BNC/COCA Level 6 lists v1.0.0, pinned from the official distribution and processed locally | Conventional 1K/2K word-family `L_word(k)` that is interpretable against the Nation literature | Contextual word meaning, MWE status/sense, participant knowledge, or an open-ended modern-frequency norm |
| Downstream open public list contrast | Admitted NGSL 1.2 projection: 2,809 ranked heads and 10,114 ASCII forms under CC BY-SA 4.0 | A reproducible general-service-list profile and explicitly project-defined first-1,000/2,000/full rank cutoffs | Nation's 1K/2K word-family bands; the five multi-head homographs and source-wide sense collapse remain visible limitations |
| Corpus-frequency contrast | Existing TUBELEX profile; a later written profile only if its corpus claim is admitted | Named exposure-frequency and range evidence | A vocabulary list, dictionary meaning, or known/unknown classification |
| Learner-oriented lexical reference | EFLLex only through a segregated local import if the noncommercial study needs it | A1–C1 textbook-distribution evidence for 15,280 English lemmas, including MWEs | A redistributable permissive default, individual mastery, or a universal CEFR truth |
| Restricted dictionary/level source | English Vocabulary Profile | Citation or separately permitted research only | Bundling, bulk extraction, or public app delivery without written permission |

The reproducible
[STREUSLE–OEWN exact-coverage audit](resources/streusle_v5_oewn_2025_coverage_audit.json)
checks all 624 target occurrences without emitting source text. Exact lookup
finds an OEWN verb entry for 317 occurrences and at least two inventory senses
for 228, but the apparent coverage is structurally biased: 45/319 VID
occurrences and 31/239 VID types match, versus 189/207 VPC.full and 83/98
VPC.semi occurrences. Only 10 VID occurrences have two or more exact-matched
senses. Removing a fixed set of article and possessive-slot tokens produces a
unique OEWN candidate for only 9/307 unmatched occurrences and 2/233 unmatched
types; 265 VID occurrences and 206 VID types remain unmatched. This does not
prove that OEWN lacks the VID meanings, but it does reject cheap normalization
as an adequate solution. Never exclude all exact-unmatched forms, because doing
so would select away the category whose semantic treatment is part of the main
claim.

The follow-up
[Kaikki/Wiktionary VID audit](resources/streusle_v5_kaikki_vid_audit_2026_09_03.json)
retrieves only the 206 residual type endpoints into ignored local storage and
commits no lexical content. Exact English verb entries exist for 60 types/96
occurrences and lexicalized gloss candidates for 57/93; 146 types/169
occurrences still have no exact verb entry. Across OEWN exact, two simple-slot
candidates, and Kaikki exact lookup, the unreviewed upper bound is only 93/239
VID types and 150/319 occurrences. Only 28 types have multiple inventory
candidates. More critically, just 5/99 Kaikki raw senses have a Wiktionary
`senseid`, and only one matched type has IDs for every lexicalized sense; none
has a raw `id` or Wikidata ID. Five successful HTTP pages have the exact English
word but no verb entry, and are not counted as coverage.

This rejects direct Wiktionary-as-gold, not Wiktionary as evidence. Exact misses
do not establish lexical absence, and glosses do not establish contextual
truth. A retained VID scope therefore needs project-stable sense IDs, immutable
source and sense fingerprints, explicit merge/split/version rules, and
layer-specific licensing. Non-exact candidate mapping needs a frozen procedure
and stop rule; it must not become an unlogged manual search that favors familiar
idioms.

That design is now frozen in the
[hybrid sense-inventory contract](resources/hybrid_sense_inventory_contract_2026_09_03.json)
version 2.0.0, SHA-256
`e389eafd39b68a9f93058a1ad4c34f899547405f02df7c4d2f669b279310d596`.
All admitted types and senses receive opaque project IDs; OEWN and Wiktionary
identifiers remain attributed source links. Artifact and canonical source-record
hashes detect change but never become semantic IDs. The contract separates a
type with no bounded source route from an annotator abstention and from a
confirmed contextual use that is genuinely out of the frozen inventory. Its
remaining pass exhausts source-declared variants, tightly bounded orthographic
equivalence, and the resulting complete candidate set for all 146 residual VID
types, then stops without free search or a desired coverage quota. The contract
contains no lexical entries and makes no runtime claim.

The reproducible [IR-130 queue](resources/sense_mapping_queue.json) and
[review guide](resources/sense_mapping_guide.md) now execute that pass against
the pinned local artifacts. Three types have unreviewed candidate sets and 143
retain `unresolved/no_bounded_route`; all 146 types/169 occurrences stay in the
denominator, and zero types are mapped or marked OOI. The queue contains only
attributed canonical/source identifiers, declared variant values, route states,
and fingerprints—no corpus sentence, gloss, example, translation, or
contextual label. Independent review and full Wiktionary source admission are
still blocked, so this is not a completed inventory.

The OEWN-only seed is now reproducible in
[`hybrid_sense_inventory_v1.json`](resources/hybrid_sense_inventory_v1.json).
It appends four previously exposed training/development VPC forms and five VID
pilot forms after the IR-130 ID range and reserves 67 project sense IDs in
pinned OEWN source order.
Every candidate carries its sense-key fingerprint, CILI/ILI, verbatim
gloss/example provenance, and non-merging synset-member relations. All nine
types remain `unresolved/candidate_route_only`, with zero admitted senses,
because independent review and adjudication have not occurred. The seed does
not use Wikipedia text, sealed-test context, or runtime integration.

The companion [IR-132 population log](resources/inventory_population_log.json)
freezes a purposive 14-type VID batch using only STREUSLE train annotations: 4
exact OEWN, 1 unique-slot OEWN, 4 exact Kaikki, 3 nonexact candidate, and 2
no-route types. Its 52 training occurrences include 21 discontinuous cases.
Every type has an eligibility state, 12/14 have a source route, and 2/14 remain
unresolved (`0.142857`). This is a workflow stress test, not a probability
sample or coverage estimate. Kaikki wording remains excluded pending its
source-identity/rights gate.

IR-133 now supplies a
[Draft 2020-12 schema](resources/hybrid_sense_inventory.schema.json) plus
registry checks over the queue, population log, and inventory. It rejects
type/sense ID collisions, duplicated source-sense identities, invalid ownership
prefixes, and self-relations. Candidate and future formal sense records expose
`supersedes`, `split_from`, `merged_from`, and `related_to`; the present arrays
are empty. Source updates use the prior inventory as the registry, preserve IDs
by project type plus source sense key despite source reordering, append only for
new senses, and fail before silently deleting a prior sense. This establishes
technical version identity, not semantic equivalence or independent review.

IR-134 now exercises the non-destructive update rules with one synthetic,
hash-fixed [lifecycle fixture](tests/fixtures/sense_inventory_versions/lifecycle_exercise.json)
and a public [approval/migration procedure](resources/inventory_governance.md).
The old/new pair covers split, merge, deprecated-source replacement, and a new
training-only OOI-prompted sense. Every old ID remains present, affected IDs are
deprecated rather than redirected, and all five old annotation records remain
unchanged with separate migration statuses and no automatic rewrite. The
exercise consulted no test label or metric; after any test exposure, a boundary
change must preserve the old release and start a new major benchmark version.
It demonstrates governance behavior only, not a valid semantic change.

IR-135 now reproduces [hybrid inventory coverage
v2](resources/hybrid_inventory_coverage_v2.json) over all 624 STREUSLE targets,
all 389 types, and the full 52-occurrence/14-type IR-132 VID pilot. The current
candidate seed is available for 57 occurrences/9 types, but this is only 21/319
VID occurrences and 20/188 discontinuous occurrences; 7/389 types have multiple
candidates when all zero-candidate types remain in the denominator. Formal
inventory coverage and contextual adequacy are both 0/624, and OOI has not been
assessed. The selected-only denominator is forbidden, so all contextual-sense,
VID-sense, and discontinuous-sense claims remain held pending IR-136 and later
independent contextual review.

IR-136 preparation now puts usage evidence before lexicographic adjudication.
The standard-library [usage-pilot builder](scripts/build_polysemy_usage_pilot.py)
reproduces a [public manifest](resources/polysemy_usage_pilot.json) containing
all 54 matching STREUSLE train/dev occurrences for the nine frozen forms and a
51-edge connected round-1 scaffold; test, sentence text, and semantic judgments
are excluded. Usage-pair raters see context but not dictionary glosses or
candidate IDs. Additional edges are limited to disagreement, weakly connected
regions, or provisional cluster boundaries. Only after the usage-cluster
diagnostics are frozen do two independent lexicographers review pinned-source
coverage, form relation, construction scope, and retained-candidate clustering
under the [inventory protocol](resources/inventory_review_protocol.json) and
[validator](scripts/check_inventory_reviews.py). `cut short` remains
contextually underdetermined because only one eligible occurrence exists. Raw
decisions and identity keys stay outside Git, GitHub Pages, APIs, and this
Dropbox workspace. IR-136 remains incomplete until the usage judgments,
independent reviews, and adjudication exist.

STREUSLE and the severely bounded WSD sense slice answer different core tasks
and must not be merged into one score. BNC/COCA and NGSL are downstream
coverage resources; report either only under its own unit and never choose the
one that gives the preferred application result.

Dictionary information should be added in two narrow places:

1. use the declared list's own family/form rows for ordinary word-list matching;
   do not ask BERT to rediscover inflectional membership already supplied by the
   resource;
2. use OEWN only after a VPC/VID occurrence has been admitted, to display the
   complete candidate-sense projection for the bounded target forms and retain
   ambiguity or out-of-inventory decisions.

Do not merge these into one “master lexical database.” Separate versioned
browser files make the unit, license, tokenizer, and removal path auditable. The
bounded English Wiktionary audit is complete and fails direct admission as gold:
it improves exact candidate coverage but leaves most VID types unmatched and
almost all senses without a source-stable ID. The Wiktextract code license does
not replace the license on extracted dictionary content, and Kaikki's moving
“current” export cannot be an immutable benchmark identity. Keep its cache local
and keep the original audit aggregate-only. The separately hash-fixed IR-130
projection may expose only the attributed candidate identifiers and
fingerprints described by its three notices; its raw JSONL remains local.
Because VID is central rather than an optional stratum, proceed with a
project-stable hybrid inventory before considering VPC-only narrowing; silently
dropping VIDs is prohibited.

The NGSL and exact local-only BNC/COCA first-2K profile paths are implemented;
the latter excludes all four special lists and records the imported file hash.
Public bundling remains gated by artifact-specific license mapping. The
existing OEWN extractor is now generalized only across nine fixed VPC/VID
training/development forms. Do not fetch a live dictionary API from the browser
or ship every dictionary entry. The next inventory action is to freeze and
verify the multi-axis review input, then commission independent review of the
fixed candidate sets and resolve the Kaikki identity/rights gate. Automatic
admission, gloss-similarity merging, and expansion from held-out context remain
prohibited.

## Learner-language errors and corpus evidence

This section remains a valid later robustness lane, but it is not on the core
technical path. Learner writing can stress candidate and sense methods after
they are validated; it cannot supply independent MWE gold, establish what a
reader knows, or validate a 95%/98% comprehension interpretation.

### What the app currently does

The current app preserves the submitted text and performs no spelling or
grammar correction. That is the correct default for learner-corpus research:
silent correction would replace the observed learner production with a new,
researcher- or model-authored text.

| Input feature | Current behavior | Consequence |
|---|---|---|
| ASCII misspelling such as `tkae` | Kept as a token; it may even match a noisy rare form in TUBELEX (`tkae` has source count 1) | “Matched” does not establish correct spelling, and “unmatched” does not establish an error or unknown word |
| Misspelling inside an MWE member | Exact surface pattern normally misses it | Candidate recall falls unless the pattern declares the variant or a researcher adds the occurrence manually |
| Noncanonical grammar around correctly spelled members | Ordered member matching may still find the candidate when members fall within the declared gap | The matcher neither validates nor corrects grammar; contextual status remains a human decision |
| Inflected or innovative learner form | Found only when an allowed surface alternative matches | Lemmatization and error-tolerant matching are not implemented |
| Corrected/edited version | Must be analyzed as a separate text | Raw and corrected outputs cannot be pooled or silently substituted |

Thus the answer to “can it handle learner errors?” is **partly, but not
robustly**. It can preserve, tokenize, expose reference matches/non-matches, and
manually review many cases. It cannot currently recover misspelled MWE members,
use reference membership to validate spelling, distinguish an error from an
innovative/off-list form, or determine whether noncanonical grammar still
instantiates the target construction.

### Error-policy to evaluate before adding correction code

1. Keep the original learner text as the primary observation.
2. Never autocorrect before measurement without retaining an immutable original
   and a token-level correction map with source, confidence, and decision
   provenance.
3. If a corrected version is justified, report raw and corrected analyses as a
   paired sensitivity analysis, not as interchangeable inputs.
4. Separate at least `matched`, `unmatched`, `researcher-normalized`, and
   `unresolved` in any future correction-aware contract; unmatched alone is not
   an error label.
5. Measure how spelling, morphology, and syntax affect word matching, candidate
   recall, member boundaries, and document-level conclusions before choosing a
   spellchecker, parser, BERT model, or handcrafted variant list.

### ICNALE GRA disposition

ICNALE GRA v2.1 is a strong **exploratory sensitivity dataset** because it
contains 140 essays drawn from ICNALE Written Essays, fully edited versions of
those essays, and ratings from 80 raters. The original/edited pairs can show how
expert editing changes word-profile membership, candidate yield, confirmed MWE
accounting, and interpretation.

The 140 essays may contain too few VPC/VID occurrences for stable prevalence or
error-stratum estimates. ICNALE Written Essays v2.6 offers a much larger pool
(5,600 essays; about 1.3 million words) for a local exploratory distribution
study and selection of a documented annotation sample. Use GRA for paired
error/edit sensitivity and the larger WE module, if admitted, for breadth; do
not pretend that one corpus role substitutes for the other.

It does not solve every evidence need:

- GRA and WE are not MWE span/category gold corpora;
- a fully edited essay may change wording and syntax as well as spelling, so the
  pair is not a pure spelling-error intervention;
- access requires registration for the download package; and
- ICNALE terms prohibit reproducing or redistributing part or all of its data.

Accordingly, keep ICNALE text outside this public repository. A reproducible
study can publish corpus version, sample IDs, selection code, hashes where
permitted, derived statistics, and instructions for registered users, subject
to a project-specific review of whether each derived output is publishable.
If learner-production robustness remains in the claim, the paired GRA analysis
belongs in the existing-data phase before any new data collection. A separately
annotated subset or another licensed corpus is still required for MWE recall
and boundary evaluation; GRA raters are not the essay writers and their writing
ratings are neither MWE knowledge nor reading comprehension.

Kyle and Eguchi's learner-corpus work is a valid precedent for empirical corpus
analysis and for publishing analysis code and derived tables. It supports using
learner corpora here; it does not imply that learner errors are harmless to
tokenization, dependency parsing, candidate recall, or construct validity.

## Critical-reviewer audit

### Likely rejection risks

| Priority | Reviewer objection | Why it is serious | Required answer before submission |
|---|---|---|---|
| 1 | The sense evidence is far too small and narrow | The admitted WSD slice has only 23 VPC rows/18 types, 17 already exposed source-test rows, no VID or `take in` test row, and only one form with contrasting evaluation senses. | Report it only as a conditional smoke-test floor; obtain adequate independent target-wide evidence or narrow the claim before expanding the app or training a model. |
| 2 | False negatives are invisible | User-supplied patterns can only review candidates they generate. A polished interface cannot recover missed MWEs. | Evaluate candidate recall first, especially discontinuous and form-unseen cases, and expose candidate source and known ceiling in every export. |
| 3 | Form membership is being confused with polysemy | A dictionary can list 17 `take in` entries without showing that the inventory fits a context or that reviewers can distinguish them. | Report inventory coverage, ambiguity, abstention, out-of-inventory cases, and independent contextual-sense agreement separately. |
| 4 | Human “gold” is undefined | Occurrence, span, category, idiomaticity, and fine sense each require a distinct judgment; project-authored fixtures are not validation. | Publish the guide, preserve independent pre-adjudication labels, adjudicate disagreements, and report task-specific agreement and errors. |
| 5 | A generic MWE highlighter is not novel | Eguchi's MWU Profiler and other tools already expose list/dependency matches. | Demonstrate the distinct staged occurrence-and-sense contract, correction path, uncertainty, held-out evidence, and reproducible export. |
| 6 | Train/test leakage exaggerates generalization | Random occurrences of the same form or source document can place nearly identical lexical evidence in both partitions. | Freeze document- and, for unseen-form claims, canonical-form-disjoint partitions; disclose all prior inspection. |
| 7 | User value is assumed | Researchers may misunderstand states or find correction and sense review too burdensome. | Run declared tasks with intended L2 vocabulary researchers and report critical errors, time, corrections, and unresolved decisions. |
| 8 | The paper is still trying to validate too much | Occurrence detection, fine sense, coverage, gaze, learner errors, pedagogy, and all MWE types require different evidence. | Restrict the first technical scope to English VPC.full/VPC.semi/VID; make coverage, eye tracking, and learner corpora optional applications. |
| 9 | BERT can add opacity without validity | A contextual score may improve one aggregate while worsening calibration, reviewer effort, privacy, reproducibility, or inventory coverage. | Compare one model only after manual gold and transparent baselines; admit it only for a named held-out human-workflow benefit. |
| 10 | Generality is overstated | English VPC/VID evidence cannot support all MWEs, non-verbal idioms, multilingual use, or pedagogical importance. | Put English VPC/VID in the title, abstract, sampling frame, interface, and claim boundary. |
| 11 | Resource rights and label mappings are flattened | Code, corpus sentences, annotations, model weights, dictionaries, and derived mappings can have different terms and constructs. | Preserve artifact-level rights and never merge incompatible labels into a convenient synthetic gold standard. |
| 12 | A downstream result is being used as label validation | Coverage differences or shorter gaze durations can occur even when an MWE boundary or sense is wrong. | Validate labels first; present coverage and processing only as separately bounded consequences. |
| 13 | Learner-language robustness is assumed | Misspellings and grammatical deviations can break surface, lemma, parser, and sense stages differently. | If retained, test original/corrected pairs after core validation and report stage-specific changes without silent correction. |
| 14 | Reproducibility is ahead of validity | Hashes and tests reproduce calculations but cannot validate linguistic decisions or response processes. | Organize the paper around a validity argument; present software reproducibility as one evidence source, not the conclusion. |

### Important but non-fatal limitations

- Surface-form TUBELEX tokenization splits apostrophes and hyphens and excludes
  non-ASCII word forms; the MWE tokenizer follows a different contract.
- Inflection, lemmatization, particle/preposition ambiguity, overlaps, and
  nested MWEs remain sources of error.
- OEWN entry count is not corpus frequency, learner familiarity, or teaching
  priority; its sense count must not be treated as contextual polysemy evidence.
- Local processing reduces text transmission risk but does not remove consent,
  privacy, copyright, device-history, or institutional obligations.
- The 6.1 MB TUBELEX projection is small enough for the current static design
  in a Node smoke check, but real-browser load and low-resource-device evidence
  remain absent.
- The repository name contains “Diversity” and “Sophistication,” while the
  admitted study concerns MWE-aware lexical reporting. The manuscript and UI
  must not inherit claims from the repository name.

## Core technical and downstream measurement contracts

Every result must name its observed unit, reference function, numerator,
denominator, tokenizer, missing-value policy, and excluded inference.

Primary technical outcomes:

| Outcome | Admitted meaning | Current state |
|---|---|---|
| Candidate recall | Gold occurrences surfaced before manual addition / all gold occurrences | The 40-item exposed STREUSLE projection now has surface and gap/dependency diagnostics, but unseen-type recall remains zero and no domain-general estimate exists |
| Exact-span/category performance | Exact member boundaries and VPC.full/VPC.semi/VID category under frozen scoring | Contract and fixtures exist; independent natural gold and error analysis are absent |
| Sense-inventory coverage | Confirmed occurrences for which the declared inventory contains an adequate contextual sense / all sense-eligible confirmed occurrences | Implemented only as lookup state; no natural estimate |
| Contextual-sense decision | Agreement and adjudicated accuracy for one/multiple assignment, ambiguity, abstention, out-of-inventory, and inventory-ineligible states | Implemented for `take in#v` review; independent gold is absent |
| Review burden | Human additions, corrections, unresolved decisions, and time per candidate/document | States are exportable; time and intended-user evidence are absent |
| Model assistance | Held-out change in ranking quality, calibration, correction time, and unresolved rate over the transparent baseline | No contextual model is implemented |

Downstream participant/coverage quantities for optional application studies:

| Symbol | Admitted meaning | Current state |
|---|---|---|
| `P_word` | For participant *p* and text *t*, target word tokens marked known under a frozen conventional single-word knowledge rule / eligible word tokens in *t*; MWE members remain individually scored | Not implemented; must reproduce the word-only construct without silently testing the phrase |
| `P_mwe_form` | Confirmed target MWE occurrences whose form/function is recognized by *p* / eligible confirmed target MWE occurrences | Not implemented |
| `P_mwe_sense` | Confirmed target MWE occurrences whose contextual meaning is demonstrated by *p* / sense-eligible confirmed target MWE occurrences | Not implemented; primary MWE criterion quantity |
| `G_component_only` | Target MWE occurrences whose member tokens are all marked known by `P_word` but whose contextual MWE meaning is not demonstrated by *p* / sense-eligible confirmed target MWE occurrences | Not implemented; central diagnostic, not an adjusted percentage |
| `G_holistic_only` | Target MWE occurrences whose contextual meaning is demonstrated by *p* despite one or more member tokens failing `P_word` / sense-eligible confirmed target MWE occurrences | Not implemented; reverse-direction diagnostic |
| `L_word(k)` | Target word tokens matched by a frozen list through level *k* / eligible target word tokens | Implemented diagnostically for explicit NGSL head-rank cutoffs and exact local Nation BNC/COCA Level 6 first-1K/2K family cutoffs; neither is participant knowledge |
| `C_word(A→B)` | Target-corpus *B* word tokens matched by an inventory derived from source corpus *A* under declared frequency/range rules / eligible word tokens in *B* | Not implemented; curricular-recurrence mode only |
| `C_mwe(A→B)` | Confirmed MWE occurrences in *B* whose form or sense meets separately declared evidence rules in *A* / eligible confirmed MWE occurrences in *B* | Not implemented; occurrence in *A* is not learning |

Current software diagnostic quantities:

| Symbol | Admitted meaning | Current state |
|---|---|---|
| `W_token` | Tokens meeting the selected TUBELEX membership, NGSL head-rank cutoff, or local BNC/COCA family-level cutoff / all tokens produced by the selected profile tokenizer | Implemented; label with profile ID, function, cutoff, and runtime file hash where applicable |
| `W_type` | Distinct forms meeting the selected TUBELEX membership, NGSL head-rank cutoff, or local BNC/COCA family-level cutoff / all distinct selected-profile forms | Implemented; `beyond_cutoff`, `unmatched`, and ambiguous heads remain separate |
| `M_member` | Union of confirmed MWE member-token IDs / all word tokens; gaps excluded | Implemented; this is the word-only masking/accounting quantity |
| `M_inventory_token` | Confirmed MWE occurrences whose canonical form is in the declared inventory / all confirmed occurrences | Implemented for OEWN; inventory membership only |
| `M_inventory_type` | Distinct confirmed canonical forms in the inventory / all distinct confirmed canonical forms | Implemented for OEWN; inventory membership only |
| `A_review` | Confirmed plus rejected candidates / all generated candidates | Implemented annotation-completion measure |
| `U_review` | Unresolved candidates / all generated candidates | Must remain visible and must not be treated as absence |
| `M_frequency` | Confirmed MWE occurrences meeting a declared corpus frequency/range condition / all confirmed occurrences | Not defined or implemented; requires an admitted MWE corpus profile |
| `M_sense` | Confirmed occurrences with a defensible contextual inventory assignment / eligible confirmed occurrences | Implemented for the `take in#v` target projection; no validity claim |

The `P_*` and `G_*` quantities are study-analysis estimands, not promises that
the Web app will test participants. The app supplies the text-side word-token,
MWE-occurrence, member, and contextual-sense map; external study code joins that
map to separately governed participant responses. `M_sense` currently describes
human coding against the one admitted `take in#v` projection; it is neither
automatic WSD nor participant knowledge, and it is not yet independently
validated.

No formula may average word and MWE channels. A word token can remain in the
word report while also being a member of a confirmed MWE; `M_member` makes that
overlap visible. The study examines the consequence of reporting that overlap,
not an allegedly superior single score. An unknown three-word MWE must not be
declared equivalent to one, two, or three unknown word tokens without criterion
evidence: transparency, contextual importance, reader knowledge, and task can
change its effect.

The term “lexical coverage” must be followed by its reference and unit. Only the
tested person-to-text mode may be related directly to learner comprehension.
List and source-corpus modes must be labelled **list-conditioned hypothetical
coverage**, **directional corpus recurrence**, or **inventory membership** as
appropriate; a lawful frequency resource does not turn occurrence into learner
knowledge.

## Research questions

### Core exploratory questions

1. **Occurrence identification:** With a fixed candidate method, how accurately
   are continuous/discontinuous and train-seen/unseen VPC/VID occurrences,
   member spans, gaps, and categories surfaced, and which false-negative/error
   classes require human correction?
2. **Polysemy and contextual sense:** For confirmed occurrences, how often does
   the declared inventory contain an adequate sense, how reliably do reviewers
   distinguish senses while retaining ambiguity/abstention/out-of-inventory,
   and where does form-only analysis collapse consequential distinctions?
3. **Assistance and usability:** Can intended L2 vocabulary researchers
   complete, resume, interpret, and reproduce the workflow, and does one
   contextual ranker improve a named held-out decision or reviewer-time outcome
   over the transparent baseline enough to justify its costs?

### Secondary application and sensitivity questions

- How do candidate source, tokenization, inventory, category scope, unresolved
  policy, domain, and type-disjoint split change technical results?
- Which errors materially change document-level conclusions rather than only an
  aggregate benchmark score?
- Once the core records are validated, how do sense-aware MWE decisions change
  a clearly labelled coverage, source-corpus, learner-text, or eye-movement
  analysis relative to form-only and word-only alternatives?
- In an optional person-by-text study, how often do `G_component_only` and
  `G_holistic_only` alter the interpretation of nominal word coverage?

Non-verbal idioms, multilingual transfer, learner writing quality, proficiency
prediction, and pedagogical decisions remain outside the first validated scope.
Coverage and eye tracking are retained as candidate applications. Unattended
automatic word-sense truth remains out of scope; model-assisted ranking is a
core comparator only after the human task and gold evidence are frozen.

## Exploration and prospective validation design

### Registration policy

This project is currently exploratory method development. It does not need a
preregistration before inspecting development corpora, revising definitions,
discovering failure modes, or generating hypotheses. Requiring one now would
create false certainty and encourage pretending that already informed choices
were specified in advance.

The minimum open-science requirement for this phase is instead:

- label analyses and decisions as exploratory;
- preserve dated versions, code, outputs, discarded alternatives, and reasons
  for changing the method;
- state which data informed each change; and
- avoid confirmatory language, threshold claims, and post hoc generalization.

Prospective registration becomes useful only if the eventual paper adds a
confirmatory claim. After an exploratory pilot, freeze the relevant method,
sample partition, hypotheses, outcomes, exclusions, uncertainty method, and
success criteria before opening a genuinely untouched holdout. Register that
bounded validation study, not the entire software project. A later registration
cannot make already inspected data confirmatory.

### Optional downstream criterion-study architecture

This architecture is not active. If a later application retains a reader-
outcome claim, secondary analysis precedes recruitment. Existing reader corpora
can test whether reviewed MWE occurrences have distinct processing costs and
whether those costs vary with proficiency or broad vocabulary measures. They
cannot by themselves estimate `P_mwe_sense` unless the same readers were tested
on the contextual meaning of those occurrences.

Only if the project retains the stronger person-by-text criterion claim after
that audit does the smallest new-data design have three stages:

1. **Material and measurement development:** select multiple natural English
   passages and identify contextual VPC/VID occurrences, including separated
   forms. Create counterbalanced versions in which conventional word-list
   coverage is held near the same value while MWE burden differs, using
   high-frequency component words and natural paraphrases. Expert review must
   verify meaning preservation, naturalness, and whether each target MWE is
   necessary or merely incidental to comprehension.
2. **Exploratory pilot:** test the word-meaning measure, contextual MWE-meaning
   measure, passage versions, response formats, timing, and scoring reliability.
   Use the pilot to estimate participant, text, and item variance and simulate
   the confirmatory sample size. Revise materials only here.
3. **Conditional prospectively frozen criterion study:** recruit the declared
   L2 reading population only for variables still absent from admitted data,
   administer several counterbalanced passages, and measure each participant's
   required word and MWE meanings in a separate or counterbalanced session to
   limit test priming. Analyze genuinely untouched readers, texts, or items
   under the registered split.

The design must not assume that list membership equals knowledge. Nominal 95%
and 98% list conditions describe materials; `P_word` is computed from each
participant's demonstrated contextual knowledge and analyzed continuously.
Predicted comprehension at 95% and 98% may be reported as interpretable
reference points, but the analysis must not force a discontinuity there.

Within that optional criterion study, the primary outcome is global passage
comprehension scored without requiring a direct definition of each target MWE.
MWE-critical comprehension items and
delayed recall are secondary outcomes. If only MWE-definition or MWE-critical
items improve, the result may show local phrase knowledge but cannot establish
an improvement in global lexical-coverage measurement. Reading time may be
recorded with the ordinary browser clock as an exploratory outcome; eye
tracking is not required for the first study.

The frozen analysis compares, at minimum:

- a word-only model using `P_word` plus prespecified passage, task, and reader
  controls;
- a prespecified extension adding `P_mwe_sense`; and
- a prespecified extension adding `G_component_only`.

The two MWE quantities need not enter the same model because they are
structurally related. Their roles and comparison rule must be frozen after the
pilot rather than selected from whichever model looks strongest.

Use crossed participant, passage, and item variation where the design supports
it, report uncertainty and held-out performance, and inspect calibration rather
than selecting predictors stepwise. MWE transparency, discontinuity, genre,
and target centrality are prespecified moderators only if the pilot supplies
enough information; otherwise they remain descriptive strata. Do not tune a
new combined coverage formula on the same data used to claim that it works.

### Design threats that can invalidate the claim

- Altering MWE and comparison passages must not also alter propositional
  content, syntax, length, cohesion, or answer cues enough to explain the result.
- Pretesting the exact MWEs immediately before reading can teach or prime them;
  posttesting alone can confound prior knowledge with contextual learning.
- A form-recognition item cannot establish knowledge of the contextual MWE
  sense. The single-word test must measure meaning rather than spelling while
  remaining independent of the phrase meaning it is meant to omit; that tension
  is part of the conventional construct being tested, not something to hide.
- Word and MWE knowledge are graded. Any binary known/unknown rule must define
  partial and uncertain responses and be checked against a prespecified
  polytomous or probabilistic sensitivity analysis.
- Treating all MWEs as equal ignores transparency and discourse centrality;
  treating an unknown three-token MWE as three unknown words invents a weight.
- Assuming that MWE knowledge can only lower coverage ignores holistically known
  expressions with an individually unknown member; retain both mismatch
  directions before proposing any adjustment.
- Questions written around the target phrases can make MWE knowledge
  tautologically predictive. Global and target-critical outcomes must remain
  separate.
- One passage, one genre, or one learner group cannot support a universal
  threshold claim, even with a large participant count.
- Artificially concentrating opaque MWEs may create power while destroying
  ecological validity; using only natural prevalence may provide too little
  within-text variation. The pilot must quantify this tradeoff and freeze the
  admitted passage domain.

### Evidence lanes

| Lane | Data | Purpose | Separation rule |
|---|---|---|---|
| Core occurrence benchmark | Rights-compliant English VPC.full/VPC.semi/VID annotations with contiguous/discontinuous and form-seen/unseen strata; STREUSLE is the admitted starting benchmark | Candidate recall, member-span, gap, and category evaluation | Benchmark annotations are occurrence/category evidence, not OEWN fine-sense truth or representative L2 English |
| Core sense benchmark | Rights-compliant confirmed occurrences mapped to an explicit sense inventory, with genuine polysemy, ambiguity, abstention, and out-of-inventory states | Inventory coverage, contextual-sense agreement/accuracy, calibration, and ranking burden | Do not convert supersenses, binary idiomaticity, examples, or dictionary membership into fine-sense gold |
| Development | Project-authored diagnostics and a declared training/development partition | Revise contracts, annotation guidance, transparent baselines, and candidate method | Report as exploratory development only; never tune on the held-out partition |
| User study | Intended L2 vocabulary researchers; practitioners only if a practitioner claim remains | Task completion, interpretation, reproducibility, and correction burden | Ethics and data-management approval before recruitment; user agreement is not linguistic truth by itself |
| Existing-reader processing | TECO first only if the eye-movement illustration is retained; MECO-L2/CELER only for a named missing variable | Reuse validated member/occurrence IDs in an ROI/layout analysis | Processing is not knowledge and cannot validate MWE status or sense |
| Coverage materials pilot | Only if a coverage illustration remains after core validation | Show how word-only, form-aware, and sense-aware records change a declared analysis | No universal 95%/98% replacement; application materials cannot become core gold |
| Criterion study | Optional tested L2 readers × passages × comprehension items | Test `P_mwe_sense` or component-only gaps as a separate substantive study | Prospective protocol and genuine holdout required for confirmatory language |
| Source-to-target application | Lawfully usable instructional and target corpora | Demonstrate directional word/MWE recurrence such as textbook → examination | Corpus occurrence is not learner knowledge or comprehension |
| ICNALE GRA original/edited pairs | Registered-user, local-only corpus data | Explore sensitivity to expert editing and learner-language noise | Not MWE gold; do not redistribute text or call edits pure spelling correction |
| Diagnostic sense cases | Project-authored or lawfully annotated polysemy/literalness contrasts | Demonstrate why sense cannot be collapsed into form | Exploratory; not WSD validation |
| Contextual-model benchmark | Independent contextual VPC/VID decisions from the frozen core set | Compare a transparent lexical baseline and at most one contextual ranker | Offline until held-out accuracy, calibration, workload, rights, privacy, and runtime gates pass |
| Open natural-material frame | The stopped Project Gutenberg frame and any later separately frozen replacement | Optional releasable app/application examples | The first frame failed its adult stop; do not redesign until a named downstream illustration needs it |
| Quarantined idiom-eye candidate | Santos et al. (2026) literal/figurative sentence data | Potential direct idiom-processing stress test | Do not analyze until the participant-count contradiction, duplicated P08/P10 metrics, proficiency claims, provenance, and raw-to-derived pipeline are resolved |

The occurrence benchmark, sense benchmark, inventories, and split are Gate 1
tasks. TECO, coverage materials, source-to-target corpora, and ICNALE enter only
after a specific downstream illustration is retained. Record population, genre,
task, proficiency metadata if used, sampling unit, author/document clustering,
license, consent/ethics basis, redistribution boundary, and the exact text made
available to annotators. “Public” and “free” are not sufficient rights states.

### Annotation evidence

Before new gold decisions:

1. define VPC/VID inclusion, token/member boundaries, gaps, overlaps,
   literal/idiomatic uncertainty, and abstention;
2. pilot only on development texts and revise the guide before holdout coding;
3. use independent first-pass annotation by at least two trained annotators for
   the subset used as new gold;
4. preserve pre-adjudication decisions, disagreements, reasons, and final
   adjudication; and
5. report exact-span and category agreement rather than a single undifferentiated
   coefficient.

Sample sizes should follow a precision or information target rather than
convenience. Exploratory work reports uncertainty without retrofitted pass/fail
thresholds. Numerical success criteria are needed only for a later confirmatory
claim and must then be fixed after the development pilot and before the holdout
is inspected.

### Comparators

Use the smallest set that answers the research questions:

1. the current all-confirmed supplied-candidate negative control;
2. one transparent list, surface, or rule-based candidate baseline that can be
   reproduced lawfully;
3. one transparent contextual-sense comparator based on the complete admitted
   candidate list; and
4. at most one contextual model after the task, gold, split, and first three
   comparators are frozen.

A conventional 1K/2K word profile and participant-specific `P_word` enter only
if the coverage illustration is retained; they are not core comparators.

TUBELEX remains an optional spoken-exposure frequency contrast, not the default
word-knowledge baseline and not evidence that a participant knows an item.

TAALES and Multi-Word Units Profiler remain methodological and interface
comparators. Do not claim numerical equivalence, copy restricted payloads, or
send protected learner text to a hosted comparator. A black-box comparison is
included only when its terms, inputs, outputs, and reproducibility support the
declared question.

### Outcomes

Technical outcomes:

- candidate recall before human review;
- exact-span precision, recall, and F1 after the declared automatic stage;
- category performance;
- discontinuous, contiguous, train-seen, and train-unseen strata;
- false-negative, boundary, particle/preposition, overlap, inflection, and
  category error counts; and
- human additions, corrections, decision time, and unresolved rate.

Optional downstream measurement outcomes:

- per-person-by-text `P_word`, `P_mwe_form`, `P_mwe_sense`,
  `G_component_only`, and `G_holistic_only`, retaining missing and unresolved
  decisions;
- nominal `L_word(k)` and optional source-to-target `C_word(A→B)` and
  `C_mwe(A→B)` as separately labelled profiles;
- per-document software diagnostics `W_token`, `W_type`, `M_member`,
  `M_inventory_token`, `M_inventory_type`, `A_review`, and `U_review`;
- paired within-document consequences of word-only versus MWE-aware reporting;
- sensitivity to candidate method, unresolved policy, and any admitted reference
  contrast; and
- annotated cases where the methodological interpretation changes.

Optional criterion-study outcomes:

- global passage comprehension as the primary outcome;
- MWE-critical item accuracy and delayed recall as secondary outcomes;
- incremental information, uncertainty, calibration, and held-out performance
  of the MWE quantities beyond the frozen word-only model; and
- predicted outcomes at 95% and 98% `P_word` as reference points without fitting
  an unsupported step threshold.

User outcomes:

- completion of candidate review and export tasks;
- correct identification of numerators, denominators, resources, and text hash;
- correct rejection of proficiency, knowledge, quality, causal, and pedagogical
  overclaims;
- critical error rate, completion time, review burden, and qualitative reasons
  for failure.

Do not infer independent participants from sentences or documents, infer groups
from filenames, or pool texts before reporting document-level distributions.
Any population estimate requires a sampling frame and dependence structure that
support it.

## Evidence-gated phases

| Gate | Required package | Depends on | Exit decision | State |
|---|---|---|---|---|
| 0. Construct and implementation audit | Claim map, staged occurrence/sense states, profile separation, dated decisions, and a UI/contract/export audit | None | The primary technology, downstream applications, and forbidden inferences are consistent and novice-readable | **Complete after the 2026-09-03 priority correction; runtime behavior and the historically pinned contract remain unchanged** |
| 1. LRE resource protocol and evidence admission | Target population, source/sampling frame, precision plan, annotation and adjudication guide, exact occurrence/sense inventories, rights and public-release route, development/holdout split, and leakage record | Gate 0 | The planned data can separately and substantially evaluate candidate/span/category and contextual-sense tasks and can be lawfully released; otherwise use a Project Note ceiling or stop | **Active and blocked.** The external resources support occurrence evaluation and a 23-row sense smoke test, not an LRE-scale independent benchmark. The five-part readiness audit now governs the gate |
| 2. Technical and annotation validity | Independent pre-adjudication labels; candidate recall; span/category/sense results; inventory coverage; task-specific agreement; calibration; error analysis; review time; unresolved and adjudication rates | Gate 1, a documented annotation work relationship, and any applicable ethics/data-management approval | The released resource and bounded workflow meet the frozen precision, independence, and reliability criteria; otherwise narrow the resource and claims before modeling | Software contract, standalone rules, synthetic practice/hard cases, and training protocol complete; qualification, independent sense gold, and reviewer evidence absent |
| 3. Intended-user and browser validity | Real-browser/accessibility record plus L2-researcher task completion, interpretation, resume/export integrity, and burden | Gate 2 | Intended researchers can use and correctly interpret the method without hidden coaching | Not started |
| 4. Optional downstream application | One prespecified coverage, learner-text, source-corpus, eye-movement, or comprehension analysis with its own rights and inference boundary | Gate 2; Gate 3 if humans use the app | Show the method's consequence in one applied-linguistics setting without treating that application as label validation | Existing candidate records are exploratory and not on the critical path |
| 5. Claim-ceiling decision | Frozen audit of resource substantiality, technical, response-process, availability, and any application evidence against the submission claim ladder | Gates 2–4 as required by the retained claim | Submit a full-length paper, downgrade honestly to a Project Note, add one justified evidence package, or stop | Not started |
| 6. Frozen open release | Versioned permissible materials or redacted/simulated substitutes, source, contracts, annotations, predictions, analysis, report, checksums, license records, and archive identifier | Claim ceiling chosen at Gate 5 | A clean directory reproduces every shared result and the browser acceptance protocol passes on the archived version | Not started |
| 7. LRE submission | Resource-and-evaluation manuscript, editable source, declarations, Data Availability Statement, artifact citations, claim-evidence map, and current author-guide check | Gate 6 | Every claim is at or below the evidence ceiling; the resource, comparison, availability, and reproducibility requirements remain satisfied at upload | Not started |

Failure at a gate changes the claim; it does not trigger silent tuning on the
holdout. Negative findings remain publishable evidence if they clarify when an
MWE-aware method is not worth its cost.

The core occurrence/sense evidence package is now the only active lane. TECO,
Gutenberg replacement sampling, coverage thresholds, source-to-target
recurrence, MECO-L2, CELER, and ICNALE are optional applications. A contextual
ranker is conditional but no longer peripheral: after gold and splits are
frozen, it is the one allowed model comparison for the primary technology.

## Stop/go decisions

1. **Only the 23-row conditional sense slice is defensible:** keep the first
   paper's sense claim at feasibility/smoke-test level unless stronger evidence
   is separately authorized; do not call dictionary membership or a model's
   preferred gloss a validated target-wide sense decision.
2. **Candidate recall is practically inadequate:** do not market an automatic
   analyzer; keep manual candidate addition and evaluate one better baseline.
3. **Span/category agreement is inadequate:** clarify one measured ambiguity or
   reduce the VPC/VID scope; do not average incompatible categories together.
4. **Sense-inventory coverage is inadequate:** permit out-of-inventory decisions
   and revise the bounded projection before modeling; never score omitted senses
   as reviewer errors.
5. **Manual burden is unacceptable:** reduce the target category or improve
   ranking; do not hide the burden in aggregate accuracy.
6. **A contextual ranker does not improve held-out accuracy, calibration, or
   review effort over the transparent baseline:** omit it; a null result is
   preferable to permanent model infrastructure.
7. **Users misinterpret outputs:** revise labels/instructions and rerun a new
   evaluation sample; unit tests cannot substitute for response-process evidence.
8. **A downstream coverage or processing application adds no distinct
   interpretation:** omit it from the first paper rather than expanding data or
   inventing a combined score.
9. **ICNALE use cannot be made reproducible within its terms:** keep it as an
   unshared optional audit, obtain permission, or omit it; do not copy its text
   into the release.
10. **No runtime model is needed to complete the validated workflow:** keep the
    Web app browser-local and human-in-the-loop; offline evidence alone does not
    justify a server, database, or model download.

## Active queue: evidence before features

Only Work Package C is active: admit and freeze the core occurrence-and-sense
evaluation evidence before changing candidate code, adding sense projections,
or running a contextual model. The VOA, Simple English Wikipedia, TECO, and
Project Gutenberg work remains useful audit/application evidence but no longer
controls the technical roadmap. No learner or intended-user recruitment is
authorized at this gate.

**Completed deliverable:** the 2026-09-03
[core-evidence admission matrix](resources/mwe_core_evidence_admission_2026_09_03.json)
pins STREUSLE, MAGPIE, SemEval idiomaticity, MWEasWSD, and the standard WSD
multiword-verb slice at the artifact,
license, text, span/category, idiomaticity, fine-sense, ambiguity, and split
levels. It admits STREUSLE only for bounded occurrence/category evaluation,
MAGPIE only for secondary type-disjoint idiomaticity, and the WSD slice only
for a severely bounded conditional sense smoke test.

**Completed deliverable:** the
[MWEasWSD/SemCor reuse audit](resources/mweaswsd_semcor_reuse_audit_2026_09_03.json)
separately checks rights, provenance, duplicates/application, VPC/VID scope,
observed polysemy, and a CILI-mediated WordNet 3.0 to OEWN 2025 mapping. SemCor
is reusable with its notice, but the added artifact is rejected as validation
gold. It has zero category-confirmed VPC/VID rows, five conflicting duplicate
keys, no independent annotation/uncertainty evidence, only seven verb-proxy
forms with observed positive sense contrasts, and only 125/136 positive verb-
proxy rows with an exact-ID/same-ILI mapping. The pinned processed data also
disagree with paper Table 2 by +3 positive and +917 negative groups.

**Completed deliverable:** the bounded
[standard-WSD MWE-sense audit](resources/wsd_mwe_sense_slice_audit_2026_09_03.json)
closes the existing-corpus search. It rejects binary idiomaticity, single-word,
compound-noun, and occurrence-only resources for the fine-sense job, while
admitting a hash-pinned external slice only after one-category STREUSLE type
overlap, lossless OEWN mapping, and candidate-polysemy filtering. The result is
23 VPC occurrences/18 types: six SemEval-2007 development rows and 17 fixed
Senseval-2/3 plus SemEval-2015 source-test rows. Their labels were inspected in
the audit and are not a blinded project holdout. It has no VID or `take in` test
row, and only `find out` contrasts senses across evaluation occurrences.

**Completed deliverable:** the pre-acquisition
[benchmark source decision](resources/benchmark_source_decision_2026_09_04.json)
selects namespace-0 English Wikipedia article revisions from one completed
dated dump. A sampled text-and-standoff bundle will use CC BY-SA 4.0 with
revision/history attribution, modification notice, exact hashes, and a
fail-closed reconstruction route. Page-level imported-text and attribution
review precedes target search; images and unresolved pages cannot enter.

**Completed deliverable:** the
[release-layer manifest](resources/release_layer_manifest.json) resolves every
current public file to a source, license expression, notice, and redistribution
state. It preserves TUBELEX, NGSL, OEWN/WordNet, and CC-BY-only exceptions and
keeps future text, annotation, inventory, and model layers fail-closed.

**Completed deliverable:** the synthetic
[source reconstruction probe](resources/source_manifest.json) and
[checker](scripts/reconstruct_benchmark.py) reproduce stable document, token,
and occurrence IDs with character/UTF-8 byte offsets and discontinuous gaps.
Exact-byte or hash mismatch exits before a verified report; the probe contains
no Wikipedia text and is not benchmark reconstruction evidence.

**Completed deliverable:** the exact recombined files and official checksums for
the completed 2026-09-01 dump are pinned in the source manifest. The
[preprocessing contract](resources/preprocessing_contract.json) freezes
loss-aware rendering, prose extraction, segmentation, token normalization, and
source-trace rules before sampling; no dump content was acquired.

**Completed deliverable:** the pre-data [benchmark card](BENCHMARK_CARD.md) and
[data statement](DATA_STATEMENT.md) separate source, sampling, annotation,
target, and evaluation populations; release-time unknowns stay explicit rather
than being filled speculatively.

**Immediate next deliverable:** commission the two frozen independent inventory
reviews and authorize the managed synthetic platform dry run. The review kit
and transparent gap/dependency baseline are implemented; neither substitutes
for independent judgments, adjudication, or the future sealed-project
evaluation. The conditional human-work decision activates only before
commissioned annotation or a study about people.

### Work Package A — Gate 0 complete

The claim map has been audited against the roadmap, UI, contract, exports, and
current implementation. Present app output is separated from future participant
quantities. An English teach-back packet and governance draft are preserved as
an optional later check, but the check is not a publication sample and no longer
blocks material work. If used, all listed human-use prerequisites must first be
completed.

### Work Package B — archived downstream-material dossier

The first implementation is closed as a negative result: the frozen VOA frame
supplies no admissible pair. Route 2 v1 is preserved in
[`resources/simplewiki_gate1_route2_design.json`](resources/simplewiki_gate1_route2_design.json).
It uses the checksum-pinned 2026-08-01 Simple English Wikipedia dump and the
externally derived targets `take in`, `pick up`, `give up`, `come out`, `make
it`, and `get it`. The sample is openly target-conditioned and cannot support a
prevalence or representative-coverage inference. The later
[content-neutral amendment](resources/simplewiki_gate1_route2_content_neutral_amendment.json)
stops this design before further target review.

Archived sequence:

1. ~~Download the exact dump and verify its 384,058,867-byte size and official
   SHA-1.~~ Complete; both matched before parsing.
2. ~~Generate the prose-free candidate ledger using the frozen surface, gap,
   article, hash-order, and stop rules.~~ Complete; every queue rank and every
   unselected/excluded row is retained.
3. ~~Follow each frozen queue through rendered-boundary and 400–1,000-token
   checks until 20 mechanically eligible pages are available.~~ Complete; 509
   target rows across 508 unique revisions yielded 120 desk rows across 119
   pages. Source
   wikitext matched the dump hash for 508 rows; one unavailable revision was
   retained as an exclusion. Raw API responses remain local.
4. ~~Run the v1 desk review through `give up`, preserving occurrences, members,
   gaps, category, idiomaticity, contextual sense, source cues, coherence,
   sensitivity metadata, centrality, and unresolved decisions.~~ Complete as
   an audit record: `take in` failed, while `pick up` and `give up` reached the
   original rule's early stops.
5. ~~Pin TECO v1.1's OSF version/files and verify its join contract.~~ Complete:
   all checked downloads match OSF SHA-256 records; 41 readers each have all
   10,063 word items, and all 1,230 participant-passage pairs are unique.
   ~~Create a prose-free, outcome-blind lead screen and freeze the ROI boundary.~~
   Complete: 285 OEWN-based leads (126 contiguous, 159 gapped) retain member,
   gap, and inferred-line positions across all 30 passages. The primary unit is
   the member-word observation; only complete `nfix`/`tfd` member sums are
   permitted sensitivity summaries, because word-level summaries cannot recover
   a fixation-sequence-defined whole-MWE gaze or regression-path duration.
   ~~Complete a contextual desk triage and bounded missed-target pass without
   outcomes.~~ Complete: 39 automatic and 4 manually recovered occurrences are
   plausible across 32 forms; 10 manual hard cases and one automatic category
   case remain unresolved. The three `take in` leads are false spans; `take part`
   excludes its open-slot `in`, and `go out of business` corrects one nested
   boundary. These are single-project provisional decisions, not gold. Keep
   stimulus text local and require later independent labels/adjudication before
   any outcome join.
6. Inspect MECO-L2 and CELER only for variables TECO lacks. Do not duplicate the
   same analysis merely to increase corpus count. Keep the 2026 Portuguese-L1
   idiom-eye dataset quarantined until its documented QA contradictions are
   resolved.
7. ~~Freeze a bounded, content-neutral Project Gutenberg frame for openly
   releasable natural prose.~~ Complete. The official 2026-08-30 weekly CSV input is
   pinned at 21,196,613 bytes and SHA-256
   `253f1b2d9aead75fec8ddb732c72a2fab5cd7db2f37745ef20760254f0666c4b`.
   The frame has 22,275 metadata-eligible records and freezes two audience
   strata of 40 hash-ranked candidates, each stopping at ten intact units. The
   first ten ranks per stratum have metadata-only rights triage: 13 advanced,
   five are held for likely active Japanese terms, and two for unresolved
   identity/death. The 13 allowed files have been acquired into unbundled local
   storage through the official mirror listing and pinned by URL, bytes, file
   time and SHA-256. Standard notices were verified and front-matter review
   found no additional retained textual contributor; five print-publication
   statements remain incomplete, five files disclose transcription choices,
   and nine boundary-location exposures are recorded. The exact electronic
   file is the analysis version. The first-unit gate leaves two mechanical
   passes, ten overlength exclusions, and one ambiguous-unit exclusion. No later
   unit was substituted. Continue fixed-order rights and unit screening; if a
   stratum has fewer than ten passes at rank 40, stop and redesign rather than
   relaxing the observed rule. Ranks 11–20 are now rights-triaged: 17 may
   advance only to local notice/front-matter review, one is held for an active
   term, and two for unresolved identity/death. Those 17 exact files are now
   locally pinned; all pass notice, boundary, and full-license checks, three
   preambles identify an original publication, and all include Credits. Their
   front-matter review sent 16 to the unchanged first-unit gate and held one
   photoplay adaptation for missing source-story provenance. Five retained
   prefaces or introductions remain first; two producer synopses are excluded.
   That gate yields one further juvenile pass, nine overlength exclusions, and
   six unit-type exclusions. Ranks 21–30 are now metadata-triaged: 15 may
   advance only to local notice review, three have likely-active terms, and two
   have unresolved identities. An incidental `take in` exposure for frozen row
   36833 is disclosed and changes no decision. Those 15 files are now locally
   pinned and all pass notice, boundary, and full-license checks; one preamble
   identifies an original publication and all include Credits. Front-matter
   review sends all 15 to the unchanged unit gate, retains three source-authored
   opening sections, excludes two producer summaries, and records Paul
   Armstrong's underlying play contribution. Their unit gate adds seven passes,
   five overlength exclusions, and three unit-type exclusions. Combined yield
   is 10/44: three adult/unspecified and seven juvenile. The final metadata-only
   screen leaves only five rights-eligible adult/unspecified files; even if all
   pass, that stratum reaches only eight. Stop before batch-4 acquisition and
   preserve the failed frame. A replacement is conditional on a later named
   application need. No unit is admitted and no target/MWE search has run.
   Do not serve prose in the globally reachable app until its release scope is
   independently cleared. Treat diachronic
   literary prose as one source class with explicit audience strata, not L2/exam
   representativeness or a frequency norm.
8. Do not replace the failed Gutenberg frame or join TECO outcomes unless a
   later downstream application is selected after core validation. Only the
   frozen core evaluation set—not incidental application passages—defines the
   next sense projections.

**Output:** preserved negative material frames and optional application inputs.
They are not Gate 1 prerequisites. **Restart condition:** a retained downstream
claim names the exact missing source, outcome, and inference that this dossier
can supply.

### Work Package C — core occurrence and sense evaluation (active)

1. Freeze the first-paper taxonomy at English VPC.full, VPC.semi, and VID;
   non-verbal idioms remain a later scope extension rather than an untested
   claim hidden under “idiom.”
2. ~~Audit the four immediate candidates without merging their labels.~~ The
   2026-09-03 matrix admits external STREUSLE for bounded occurrence/category
   evaluation and external MAGPIE for secondary type-disjoint idiomaticity.
3. ~~Audit the MWEasWSD/SemCor reuse lead.~~ Rights allow external analysis, but
   zero category-confirmed target rows, weak annotation provenance, conflicting
   first-wins duplicates, sparse polysemy, mapping loss, and paper/artifact
   count disagreement reject it as validation gold. No retrospective split is
   proposed.
4. ~~Run the bounded existing-corpus search defined above.~~ The standard WSD
   framework supplies only a task-separated 23-row conditional VPC sense slice;
   freeze SemEval-2007 for development and the 17 remaining eligible rows for
   source-test smoke testing. These labels are already exposed; do not call them
   blinded, call type-level STREUSLE overlap an occurrence category, or call
   this tiny slice target-wide validation.
5. Score SemCor most-frequent-sense and the smallest existing transparent
   gloss/rule baseline on the frozen slice as an implementation check. Stop
   before BERT unless this exposes a specific non-trivial ranking problem.
6. ~~Test exact and simple article/possessive-slot OEWN mapping, then run a
   bounded exact Kaikki/Wiktionary audit.~~ The combined unreviewed routes cover
   only 93/239 VID types and 150/319 occurrences, with 28 polysemy candidates;
   only 5/99 Kaikki raw senses have a source `senseid`. Direct Wiktionary-as-gold
   is rejected, while aggregate candidate evidence is retained.
7. ~~Freeze the hybrid sense-inventory contract: project-stable IDs, immutable
   source/sense fingerprints, merge/split/version rules, layer-specific license,
   and ambiguity/out-of-inventory states. Predeclare a bounded non-exact mapping
   procedure and stop rule for the remaining 146 types.~~ Contract 1.0.0 is
   frozen and hash-pinned. The bounded machine pass is also complete: 3 types
   have candidate sets and 143 retain no-route unresolved states. It is not an
   admitted sense inventory or runtime integration; independent review and the
   Wiktionary source-identity gate remain. Exact misses stay in the denominator
   rather than becoming lexical absence or selection exclusions. The IR-131
   OEWN seed additionally reserves stable IDs for all 67 candidates of four
   VPC and five VID training/development forms. The IR-132 population log
   retains another four Kaikki-gated, three mapping-review, and two no-route
   pilot states, while every candidate remains unreviewed and every project
   `senses` list remains empty.
8. Freeze the LRE benchmark source, lawful public-release route, sampling frame,
   clustering units, primary metrics, and pilot-based precision rule. The new
   independent benchmark is required for a full-length paper regardless of the
   23-row smoke-test score, but annotation must not start before this protocol
   passes the rights gate.
9. Pilot the span/category/idiomaticity/sense/ambiguity/abstention guide on
   training material. The standalone rules, synthetic practice/hard-case bank,
   and task-specific training/qualification protocol are written; an unexposed
   qualification form, authorized live-platform dry run and training, and
   an independent pilot remain. The provisional INCEpTION UIMA CAS JSON
   converter has passed a synthetic format check only.
   Preserve independent pre-adjudication decisions,
   report task-specific agreement and unresolved rates, then size the final
   benchmark by simulation/resampling rather than a convenient round number.
10. Hash and seal the final document-disjoint test labels under a non-developer
   custodian. Use a canonical-form-disjoint partition only if the paper claims
   unseen-form generalization; otherwise retain and report seen/unseen strata.
11. Add at most
   one contextual ranker only for the task where held-out error or reviewer
   burden leaves a measured gap; final decisions remain human-reviewable.
12. Expand browser sense projections only to benchmark-admitted forms, then
   cut one explicit contract version that makes the downstream word-profile
   overlay optional; then run browser/accessibility and intended-researcher
   evidence at Gate 3. Do not mutate the currently hash-pinned contract in place.

**Output:** a publicly citable benchmark or lawful standoff release, core
evidence manifest, frozen split, annotation guide, pre-adjudication labels,
technical comparison/error report, and bounded instrument. **Stop condition:**
if the five LRE gates cannot support a substantial resource, downgrade to a
Project Note or stop rather than presenting dictionary membership, model
confidence, or an exposed smoke test as target-wide contextual-sense validity.

After C, choose at most one downstream application whose result could change
the LRE reuse argument. TECO/eye tracking, coverage, and learner production do
not run automatically. Prospective registration remains conditional on a later
confirmatory application or untouched technical holdout.

fastText is not a generic alternative to BERT: consider it only for a retained
learner-variant retrieval question. A parser or another candidate method enters
only after the target-domain recall audit identifies a concrete failure. Add one
dependency only if it improves a declared decision-relevant outcome enough to
justify model/data rights, payload, compute, privacy, and reproducibility costs.

## Deferred work

The following are legitimate later studies, not first-paper requirements:

- unattended automatic contextual sense assignment and corpus sense-frequency
  reporting; bounded contextual ranking and human sense review are core;
- non-verbal idioms and broader MWE taxonomies;
- multilingual transfer;
- multiple source-corpus profiles and broad register-sensitive comparisons;
- ICNALE learner-production error robustness unless a writing claim is restored;
- proficiency prediction or pedagogical intervention studies;
- annotation-team accounts, assignment, adjudication, and version management;
- a server, database, API, or private resource service.

Use FLAT or INCEpTION for large-team annotation unless a demonstrated
round-trip failure requires local functionality. A database does not create
permission to use or redistribute a resource and is not a rights mechanism.

## Open-science and governance gate

The free static core remains downloadable, usable without an account, and free
of analytics, proprietary APIs, and deliberate text transmission. Each admitted
resource retains a version, hash, license, attribution, construct boundary,
missing-value rule, and removal path in `RIGHTS.md` and the machine-readable
contracts.

Before submission:

- archive the exploratory decision history; if the manuscript later makes a
  confirmatory claim, prospectively register only that bounded validation before
  inspecting its holdout;
- publicly archive the core benchmark, independent pre-adjudication labels,
  adjudicated labels, predictions, analysis, and annotation guidance; use
  standoff annotations, immutable source IDs/hashes, and reconstruction code
  when source text cannot lawfully be redistributed;
- tag an immutable source release and publish checksums plus an archive DOI;
- reproduce every table and figure from that archive in a clean directory;
- state why any restricted layer cannot be shared, how it can be accessed, and
  why the publicly reusable core remains sufficient to reproduce the paper's
  central claims;
- retain pre-adjudication annotations and all negative/error results; and
- recheck the current LRE submission guidelines, article type, single-blind
  review policy, declarations, editable-source requirements, Data Availability
  Statement, AI-use disclosure, and fees immediately before upload.

Corrections receive a new version and changelog entry. A resource withdrawal
must not silently substitute a new profile under an old identifier. Browser
hashes identify bytes, not authorship or trusted time.

## Manuscript logic

The paper should be readable without opening the app:

1. **Problem:** a surface sequence such as `take in` can be contiguous or
   discontinuous, literal or idiomatic, and polysemous; string or dictionary
   lookup cannot establish its occurrence boundaries or contextual sense.
2. **Operationalization:** separate candidate, occurrence, member, gap,
   category, idiomaticity, sense-inventory coverage, assignment, ambiguity,
   abstention, and out-of-inventory states.
3. **Open method:** describe the human-in-the-loop browser workflow, stable
   identifiers, resource/version provenance, correction path, and exports.
4. **Technical evaluation:** report candidate recall, exact span/category
   results, inventory coverage, contextual-sense agreement/accuracy,
   calibration, error strata, correction burden, and held-out policy.
5. **Comparator decision:** compare transparent baselines and at most one
   contextual ranker; show whether any gain justifies added opacity, rights,
   compute, privacy, and reproducibility costs.
6. **Response evidence:** report whether intended L2 vocabulary researchers can
   perform, resume, interpret, and reproduce the retained tasks.
7. **Applied illustration:** include at most one coverage, learner-text,
   source-corpus, or eye-movement analysis if it adds a distinct disciplinary
   insight; label it as downstream rather than technical validation.
8. **Boundary and open materials:** state where the method fails, retain
   unresolved and negative results, and map every claim to its decision record,
   permissible artifact, and reproducible output.

The title and abstract must say **English VPC/VID** unless broader evidence is
actually collected. “Objective” should mean explicit and repeatable decisions,
not theory-free measurement.

## Definition of done

The project is ready for an LRE full-length submission only when a critical
reader can answer
all of the following from the manuscript and archive:

1. What counts as an English VPC/VID occurrence, member, gap, and category?
2. How are candidate generation, occurrence truth, idiomaticity, and contextual
   sense kept separate?
3. How are polysemy, ambiguity, abstention, and out-of-inventory uses represented?
4. Which resources, domains, forms, splits, and prior exposures define each
   technical result?
5. How many occurrences were missed, falsely proposed, corrected, disagreed on,
   or left unresolved?
6. How accurate and calibrated are span/category and sense decisions on held-out
   evidence, including discontinuous and form-unseen strata?
7. What human time and correction remain, and does any model materially reduce
   that burden over a transparent baseline?
8. Can intended researchers perform, resume, interpret, and reproduce the method?
9. What does any downstream coverage or eye-movement example add—and not prove?
10. Can every reported number be independently reproduced from permissible
    artifacts?
11. Is the released benchmark substantial enough under the frozen precision and
    diversity criteria, rather than merely larger than the five fixtures?
12. Can a third party obtain or reconstruct the core resource, identify every
    controlling license, and reproduce the comparisons without privileged
    database access?

Today the project can answer 1–3 at the contract/fixture level, has frozen a
minimal external answer for part of 4, and can answer part of 10. It still
cannot answer 4–8 or 11–12 at a target-wide validation level or with held-out
results, a public core benchmark, and intended-user evidence. The benchmark
protocol, release route, annotation guide, precision plan, and transparent
sense-baseline scoring—not another coverage corpus, eye analysis, or feature
family—are the critical path.

## Core references and live records

- [Executable MWE occurrence-and-sense contract](mwe_contract.json)
- [LRE full-length submission-readiness audit](resources/lre_submission_readiness_2026_09_03.json)
- [External STREUSLE VPC/VID benchmark profile](benchmarks/streusle_v5_vpc_vid.json)
- [Frozen STREUSLE gap/dependency comparator](resources/streusle_gap_dependency_baseline.json)
- [Independent inventory-review protocol](resources/inventory_review_protocol.json)
- [STREUSLE–OEWN exact inventory-coverage audit](resources/streusle_v5_oewn_2025_coverage_audit.json)
- [Residual VID Kaikki/Wiktionary coverage and identifier audit](resources/streusle_v5_kaikki_vid_audit_2026_09_03.json)
- [Bounded residual VID mapping queue](resources/sense_mapping_queue.json)
- [Bounded residual VID mapping guide](resources/sense_mapping_guide.md)
- [MWE prediction evaluator](scripts/evaluate_mwe_predictions.py)
- [Resource rights and admission ledger](RIGHTS.md)
- [Focused literature search and page-level close reading](LITERATURE_CLOSE_READ.md)
- [Gate 1 development-material admission dossier](MATERIAL_ADMISSION.md)
- [TECO v1.1 candidate and join-contract manifest](resources/teco_v1_1_candidate_manifest.json)
- [TECO v1.1 outcome-blind MWE candidate screen](resources/teco_v1_1_mwe_candidate_screen.json)
- [TECO v1.1 preliminary outcome-blind MWE desk triage](resources/teco_v1_1_mwe_desk_triage.json)
- [Frozen Project Gutenberg target-blind prose frame](resources/gutenberg_2026_08_30_prose_frame.json)
- [Project Gutenberg fixed-prefix rights triage, batch 1](resources/gutenberg_2026_08_30_rights_triage_batch1.json)
- [Project Gutenberg pre-body notice audit, batch 1](resources/gutenberg_2026_08_30_notice_audit_batch1.json)
- [Project Gutenberg front-matter review, batch 1](resources/gutenberg_2026_08_30_front_matter_review_batch1.json)
- [Project Gutenberg first-unit gate, batch 1](resources/gutenberg_2026_08_30_unit_gate_batch1.json)
- [Project Gutenberg fixed-prefix rights triage, batch 2](resources/gutenberg_2026_08_30_rights_triage_batch2.json)
- [Project Gutenberg pre-body notice audit, batch 2](resources/gutenberg_2026_08_30_notice_audit_batch2.json)
- [Project Gutenberg front-matter review, batch 2](resources/gutenberg_2026_08_30_front_matter_review_batch2.json)
- [Project Gutenberg first-unit gate, batch 2](resources/gutenberg_2026_08_30_unit_gate_batch2.json)
- [Project Gutenberg fixed-prefix rights triage, batch 3](resources/gutenberg_2026_08_30_rights_triage_batch3.json)
- [Project Gutenberg pre-body notice audit, batch 3](resources/gutenberg_2026_08_30_notice_audit_batch3.json)
- [Project Gutenberg front-matter review, batch 3](resources/gutenberg_2026_08_30_front_matter_review_batch3.json)
- [Project Gutenberg first-unit gate, batch 3](resources/gutenberg_2026_08_30_unit_gate_batch3.json)
- [Project Gutenberg final fixed-prefix rights triage and futility stop](resources/gutenberg_2026_08_30_rights_triage_batch4.json)
- [Frozen Simple English Wikipedia Route 2 design](resources/simplewiki_gate1_route2_design.json)
- [Simple English Wikipedia Route 2 candidate queue](resources/simplewiki_gate1_route2_candidates.json)
- [Simple English Wikipedia Route 2 rendered mechanical screen](resources/simplewiki_gate1_route2_rendered_screen.json)
- [Simple English Wikipedia Route 2 `take in` desk review](resources/simplewiki_gate1_route2_take_in_desk_review.json)
- [Simple English Wikipedia Route 2 `pick up` desk review](resources/simplewiki_gate1_route2_pick_up_desk_review.json)
- [Simple English Wikipedia Route 2 `give up` desk review](resources/simplewiki_gate1_route2_give_up_desk_review.json)
- [Route 2 content-neutral amendment and stop record](resources/simplewiki_gate1_route2_content_neutral_amendment.json)
- [Frozen VOA Gate 1 development frame](resources/voa_gate1_frame_2017_2020.json)
- [Target-blind VOA source eligibility screen](resources/voa_gate1_source_screen.json)
- [Target-blind VOA automated pre-review](resources/voa_gate1_automated_profile.json)
- [Preliminary VOA recurrence triage](resources/voa_gate1_recurrence_triage.json)
- [Priority VOA Education-pair desk review](resources/voa_gate1_priority_desk_review.json)
- [Deferred VOA pair desk review](resources/voa_gate1_deferred_pair_desk_review.json)
- [VOA out-of-inventory recurrence audit and frame stop](resources/voa_gate1_out_of_inventory_audit.json)
- [Gate 0 preflight and construct teach-back protocol](GATE_0_TEACH_BACK.md)
- [Hu and Nation (2000), unknown vocabulary density and comprehension](https://doi.org/10.64152/10125/66973)
- [Nation (2006), vocabulary size for 98% reading/listening coverage](https://doi.org/10.3138/cmlr.63.1.59)
- [Schmitt, Jiang, and Grabe (2011), word coverage and comprehension](https://doi.org/10.1111/j.1540-4781.2011.01146.x)
- [Kremmel et al. (2023), partial replication and threshold critique](https://doi.org/10.1111/lang.12622)
- [Martinez and Murphy (2011), MWE effects on L2 reading](https://ora.ox.ac.uk/objects/uuid%3Aebfa9868-f48b-40da-9b74-513684f28c25)
- [Kremmel, Brunfaut, and Alderson (2017), phraseological knowledge and reading](https://doi.org/10.1093/applin/amv070)
- [LRE official scope](https://link.springer.com/journal/10579/aims-and-scope)
- [LRE submission guidelines](https://link.springer.com/journal/10579/submission-guidelines)
- [Computational reproducibility in applied linguistics](https://doi.org/10.1016/j.rmal.2022.100030)
- [ICNALE modules, GRA description, and terms](https://language.sakura.ne.jp/icnale/)
- [TECO article and current OSF project](https://doi.org/10.1016/j.rmal.2024.100123), [data](https://osf.io/wrvj3/)
- [MECO-L2 Wave 2 accepted manuscript](https://eprints.soton.ac.uk/494999/)
- [CELER article and data](https://pmc.ncbi.nlm.nih.gov/articles/PMC9692049/), [repository](https://github.com/berzak/celer)
- [Santos et al. (2026) idiom eye-data preprint and archive](https://arxiv.org/abs/2605.04857), [data](https://doi.org/10.5281/zenodo.19582953)
- [Project Gutenberg terms and permission guidance](https://www.gutenberg.org/policy/terms_of_use.html), [permission](https://www.gutenberg.org/policy/permission)
- [Kyle and Eguchi (2021)](https://doi.org/10.21832/9781788924863-007)
- [Kyle and Eguchi analysis resources](https://github.com/kristopherkyle/dependency_bigrams_Kyle_Eguchi_2021)
- [Nation BNC/COCA vocabulary-analysis resources](https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/vocabulary-analysis-programs)
- [NGSL 1.2 official downloads and CC BY-SA license](https://www.newgeneralservicelist.com/new-general-service-list)
- [EFLLex download and CC BY-NC-SA terms](https://cental.uclouvain.be/cefrlex/efllex/download/)
- [English Vocabulary Profile terms of use](https://englishprofile.org/?menu=evp-terms-of-use)
- [TUBELEX](https://aclanthology.org/2025.coling-main.641/)
- [Open English WordNet 2025](https://github.com/globalwordnet/english-wordnet/releases/tag/2025-edition)
- [Public technical deployment](https://ryuya-dot-com.github.io/Lexical-Diversity-Sophistication-Analysis/)
- `README.md` for current operation, `mwe_contract.json` for executable method
  states, `RIGHTS.md` for resource admission, and `CHANGELOG.md` for history.

## Ponytail disposition

Do not add a framework, server, database, account system, metric family, or
manuscript automation while the core benchmark, label mapping, and split remain
unfrozen. The manual `take in` sense vertical slice exercises the existing
contract; broaden it only to forms admitted by the core evaluation protocol.
Add one model only after gold and transparent baselines expose a named gap;
otherwise the next useful artifact is evidence, not infrastructure.
