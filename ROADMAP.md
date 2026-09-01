# Open MWE-aware lexical-coverage measurement: RMAL roadmap

Status: MWE-aware coverage construct and criterion-evidence plan, reviewed 2026-09-01

## One-minute answer

In plain language: the study asks whether conventional word-token coverage can
misstate usable lexical coverage when a reader knows `take`, `it`, and `in`
but not the contextual meaning of `take ... in`, and whether a separate,
auditable MWE channel explains reading comprehension differences among texts
or readers with the same nominal 95% or 98% word coverage.

### What problem does this study address?

Word-level lexical profilers can count `take`, `it`, and `in` as known while
hiding that `take ... in` may be one discontinuous verb-particle construction
whose contextual meaning remains unknown. A text can therefore have 95%
word-token coverage under a conventional profile while its functional lexical
burden differs from another text at the same percentage. Contiguous n-gram
lookup misses separated forms, while dictionary or list membership alone
cannot decide whether a particular occurrence is an MWE or whether the reader
knows its contextual sense.

### What will the study do?

Develop and empirically evaluate an open, browser-local, human-in-the-loop method
for second-language (L2) vocabulary research that:

1. keeps conventional word-list and source-to-target corpus profiles as named
   baselines rather than treating either as learner knowledge;
2. uses researcher-supplied patterns to find reviewable English verb-particle
   construction (VPC) and verbal-idiom (VID) candidates, including separated
   members;
3. lets a researcher confirm, reject, correct, or leave each candidate
   unresolved;
4. reports word knowledge/profile membership, MWE-form knowledge, contextual
   MWE-sense knowledge, component-only gaps, and unresolved mass separately;
5. tests whether the MWE quantities add criterion-related information about
   reading comprehension after conventional word-token coverage; and
6. exports the decisions, denominators, resource versions, and limitations
   needed to reproduce the report.

The Web app is the executable implementation of the method. It is not the
research contribution by itself.

### What will the first paper claim?

> Conventional word-token coverage under-specifies lexical coverage when known
> component words form contextually unknown MWEs; a separate, human-reviewed
> MWE channel provides reproducible information about that hidden burden and,
> if supported by criterion data, reading comprehension beyond nominal word
> coverage alone.

That claim is provisional until technical, measurement, and intended-user
evidence pass the gates below.

### What will it not claim?

The first paper will not claim automatic MWE analysis, complete English MWE
coverage, a universal replacement for 95% or 98%, text difficulty from lexis
alone, writing quality, proficiency, CEFR level, pedagogical priority, or causal
effects. It will not subtract MWE tokens from word coverage or present a
combined word/MWE percentage unless independent criterion evidence first
supports a defensible weighting rule.

## Is the purpose transparent now?

At the purpose level, yes: the study is about **whether lexical-unit decisions
leave conventional word-token coverage under-specified as an explanation of L2
reading comprehension**. Detection, interface design, corpus transfer, and
resource engineering are supporting components.

At the evidence level, not yet. A beginning graduate student should currently
be told:

- the app can demonstrate the workflow on a text;
- the app cannot yet show that the workflow is accurate, useful, or related to
  reading comprehension;
- TUBELEX matching and OEWN membership are resource-conditioned lookup results,
  not estimates of what a learner knows; and
- a claim about 95% or 98% becomes defensible only after individual word and MWE
  knowledge are related to comprehension across multiple readers, texts, and
  items; prospective registration is needed only for the frozen criterion
  study, not the current exploratory development.

If this distinction cannot be explained without specialist terminology, the
method is not ready for participants, reviewers, or publication.

## Coverage-threshold lineage and the new hypothesis

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

### Construct decision

The primary target is now a project-defined **person-by-text MWE-aware lexical
knowledge profile**: whether a particular reader demonstrates the single-word
and contextual MWE meanings needed in a particular text. It remains a profile,
not a new combined coverage percentage. Two non-personal profiles remain useful
but cannot substitute for that criterion:

| Profile | Admitted use | Forbidden inference |
|---|---|---|
| Fixed list-to-text, such as a declared 2K list | Reproduce conventional hypothetical word coverage and create material strata | The participant knows every item in the list |
| Source-corpus-to-target-corpus, such as textbook to examination | Describe directional lexical recurrence or curricular alignment after frequency/range rules | An occurrence in the source was attended to, learned, or retained |
| Tested person-to-text | Estimate the proportion of target word and MWE occurrences whose required meanings the participant demonstrates | Comprehension is guaranteed or caused by lexical knowledge alone |

The first two profiles are application and sensitivity modes. The third is the
criterion-validity mode required for any claim about the 95%/98% literature.
ICNALE learner production is not the first criterion dataset for this question.

### Falsifiable hypothesis

At the same measured word-token coverage, readers with more **component-only
gaps**—all component words known but the contextual MWE meaning not known—will
show lower reading comprehension. A model containing separately measured MWE
knowledge should provide useful out-of-sample information beyond conventional
word-token coverage.

The method must also retain the reverse **holistic-only gap**: the reader knows
the contextual MWE despite one or more member tokens failing the conventional
single-word rule. That pattern would mean word-token coverage understates rather
than overstates usable phrase knowledge. Its prevalence and consequences are
exploratory; it must not be forced into the directional primary hypothesis.

This hypothesis fails in a scientifically useful way if the MWE channel has
unreliable measurement, adds negligible information after word knowledge and
prespecified controls, works only for comprehension items that directly test
the target phrase, or fails to generalize across held-out readers, texts, and
items. In those cases the tool remains an annotation/reporting aid and must not
claim to revise lexical-coverage theory.

## Contribution hierarchy

The project previously allowed three possible papers to compete. The hierarchy
is now fixed.

| Rank | Contribution | Role in the first RMAL paper |
|---|---|---|
| 1 | Construct extension: word coverage plus a separate MWE knowledge channel | Primary contribution |
| 2 | Criterion evidence against L2 reading comprehension | Required substantive validity evidence |
| 3 | Open browser implementation with auditable exports | Executable method and open material |
| 4 | Candidate and contextual-decision accuracy | Required technical validity evidence |
| 5 | Intended-user task and interpretation evidence | Required response-process evidence |
| 6 | Source-to-target corpus alignment | Applied use case and sensitivity analysis |
| 7 | General lexical diversity or sophistication | Out of scope |

The planned manuscript is an empirical measurement-method article with
criterion evidence, not a software note, benchmark paper, corpus paper, or
pedagogical intervention study. RMAL is a
plausible target because its official scope covers applied-linguistics research
design, coding, analysis, reporting, ethics, and open science, but it requires
the method or tool to be examined from an applied-linguistics perspective and
to solve a problem in the discipline. A feature tour will not satisfy that
standard.

## Current truth, without promotional language

| Area | What exists | What is still absent |
|---|---|---|
| Product | Static browser-local single-text review path; candidate correction; confirm/reject/unresolved states; CSV and metadata JSON | Real-browser, assistive-technology, and intended-user evidence |
| Word reference | Pinned TUBELEX English regex ASCII surface-form profile | Written/academic contrast profile; lemma/family policy; dispersion; knowledge threshold |
| MWE reference | Pinned OEWN 2025 multiword-verb inventory projection | MWE occurrence frequency/range profile and contextual sense-frequency profile |
| Candidate method | Researcher-supplied surface-member patterns plus manual candidates | Validated default candidate generator and an estimate of missed occurrences |
| Contract | Separate word, MWE-form, idiomaticity, sense, and annotation states | Empirical evidence that users understand and apply those distinctions |
| Technical evidence | Five project-authored fixtures; 40-occurrence STREUSLE projection; transparent surface baseline | Broader occurrence/sense evaluation, full error analysis, and transfer to the selected reading materials |
| Sense evidence | All 17 OEWN `take in#v` candidates and synthetic contextual decisions | Independent contextual gold, reliability, WSD validation, or sense-frequency coverage |
| Research data | Synthetic cases and external benchmark projection; ICNALE WE/GRA identified as optional local-only production resources | Multiple natural passage materials, participant word/MWE knowledge evidence, comprehension outcomes, corpus admission memo, and MWE annotation protocol |
| Open science | Public source, tests, rights ledger, static deployment | Explicit exploratory decision history, immutable release, DOI/checksum bundle, analysis scripts and report |

The public prototype is therefore an **implemented method hypothesis**, not a
validated research instrument.

## Learner-language errors and corpus evidence

This section remains a valid later robustness lane, but it is no longer on the
critical path to the coverage-comprehension claim. Learner writing cannot
establish what a reader knows in an input text, and raw/edited sensitivity
cannot validate a 95% or 98% comprehension interpretation.

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
The paired GRA analysis belongs in an optional exploratory phase; a separately
annotated subset or another licensed corpus is still required for MWE recall
and boundary evaluation.

Kyle and Eguchi's learner-corpus work is a valid precedent for empirical corpus
analysis and for publishing analysis code and derived tables. It supports using
learner corpora here; it does not imply that learner errors are harmless to
tokenization, dependency parsing, candidate recall, or construct validity.

## Critical-reviewer audit

### Likely rejection risks

| Priority | Reviewer objection | Why it is serious | Required answer before submission |
|---|---|---|---|
| 1 | “Coverage” still mixes three constructs | TUBELEX membership, 2K-list coverage, source-corpus recurrence, and tested learner knowledge support different inferences; only the last can directly enter a coverage-comprehension claim. | Freeze `L_word(k)`, `C_word(A→B)`, `P_word`, `P_mwe_sense`, and every denominator; never substitute one for another. |
| 2 | “MWEs matter for reading” is already known | Martinez and Murphy and Kremmel, Brunfaut, and Alderson already show comprehension and phraseological-knowledge effects. A highlighter or another correlation is not novel. | Demonstrate an auditable person-by-text coverage operationalization and test its incremental held-out information beyond measured word-token coverage. |
| 3 | No criterion evidence exists | Synthetic examples, corpus recurrence, ICNALE production, and a general-English occurrence benchmark cannot show that the proposed quantities relate to reading comprehension. | Run the multi-passage person × text × item criterion study with contextual word/MWE knowledge and global comprehension outcomes. |
| 4 | False negatives are invisible | User-supplied patterns can only review candidates they generate. A polished review UI cannot recover missed MWEs. | Evaluate candidate recall first, especially discontinuous and unseen forms, and expose the candidate source and known ceiling in every export. |
| 5 | Human “gold” is undefined | Confirming VPC/VID status and boundaries requires judgment; project-authored fixtures are not independent validation. | Publish annotation guidelines, train at least two independent annotators where new gold is created, adjudicate disagreements, and report category/span agreement. |
| 6 | The paper is still trying to validate too much | Detection, contextual knowledge, comprehension, corpus transfer, usability, pedagogy, and all MWE types require different evidence. | Limit the core claim to English VPC/VID contextual knowledge and reading; keep source-to-target work illustrative, ICNALE optional, broader idioms deferred, and pedagogy out. |
| 7 | User value is assumed | Researchers may not understand separate denominators or may find manual review too burdensome. | Run declared task and interpretation studies with intended L2 vocabulary researchers, recording critical errors and review effort. |
| 8 | Knowledge testing creates the effect it claims to measure | Pretesting can teach or prime MWEs, posttesting can include contextual learning, and form recognition does not establish contextual meaning. | Use a piloted separate/counterbalanced session, contextual-sense scoring evidence, and a declared missing/uncertain policy. |
| 9 | Generality is overstated | English VPC/VID evidence cannot support “MWE” in general, multilingual use, or pedagogical importance. | Put English VPC/VID in the title, abstract, sampling frame, interface, and claim boundary. |
| 10 | The 95%/98% framing invites a false replacement threshold | Prior evidence is largely continuous and varies by text, task, and population. An “MWE-adjusted 96.4%” would be arbitrary without independent weighting evidence. | Model word and MWE quantities separately and continuously; report predictions at 95%/98% only as reference points and validate any later combined rule on new data. |
| 11 | Resource choice may drive nominal coverage | TUBELEX models audiovisual/spoken exposure, word lists differ in units and ranking, and OEWN is a lexicon rather than corpus frequency. | Freeze one lawful conventional list for the main material profile and treat TUBELEX, OEWN, and source-corpus variants as named sensitivity resources. |
| 12 | Reproducibility is ahead of validity | Hashes and tests reproduce calculations but cannot validate the construct or response process. | Organize the paper around a validity argument; present software reproducibility as one evidence source, not the conclusion. |

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

## Measurement contract to freeze

Every result must name its observed unit, reference function, numerator,
denominator, tokenizer, missing-value policy, and excluded inference.

Target criterion quantities:

| Symbol | Admitted meaning | Current state |
|---|---|---|
| `P_word` | For participant *p* and text *t*, target word tokens marked known under a frozen conventional single-word knowledge rule / eligible word tokens in *t*; MWE members remain individually scored | Not implemented; must reproduce the word-only construct without silently testing the phrase |
| `P_mwe_form` | Confirmed target MWE occurrences whose form/function is recognized by *p* / eligible confirmed target MWE occurrences | Not implemented |
| `P_mwe_sense` | Confirmed target MWE occurrences whose contextual meaning is demonstrated by *p* / sense-eligible confirmed target MWE occurrences | Not implemented; primary MWE criterion quantity |
| `G_component_only` | Target MWE occurrences whose member tokens are all marked known by `P_word` but whose contextual MWE meaning is not demonstrated by *p* / sense-eligible confirmed target MWE occurrences | Not implemented; central diagnostic, not an adjusted percentage |
| `G_holistic_only` | Target MWE occurrences whose contextual meaning is demonstrated by *p* despite one or more member tokens failing `P_word` / sense-eligible confirmed target MWE occurrences | Not implemented; reverse-direction diagnostic |
| `L_word(k)` | Target word tokens matched by a frozen list through level *k* / eligible target word tokens | Not implemented; hypothetical conventional baseline only |
| `C_word(A→B)` | Target-corpus *B* word tokens matched by an inventory derived from source corpus *A* under declared frequency/range rules / eligible word tokens in *B* | Not implemented; curricular-recurrence mode only |
| `C_mwe(A→B)` | Confirmed MWE occurrences in *B* whose form or sense meets separately declared evidence rules in *A* / eligible confirmed MWE occurrences in *B* | Not implemented; occurrence in *A* is not learning |

Current software diagnostic quantities:

| Symbol | Admitted meaning | Current state |
|---|---|---|
| `W_token` | TUBELEX-profile-matched surface tokens / all tokens produced by the TUBELEX-specific tokenizer | Implemented; label as profile membership coverage |
| `W_type` | Distinct TUBELEX-profile-matched forms / all distinct forms produced by that tokenizer | Implemented; label as profile membership coverage |
| `M_member` | Union of confirmed MWE member-token IDs / all word tokens; gaps excluded | Implemented; this is the word-only masking/accounting quantity |
| `M_inventory_token` | Confirmed MWE occurrences whose canonical form is in the declared inventory / all confirmed occurrences | Implemented for OEWN; inventory membership only |
| `M_inventory_type` | Distinct confirmed canonical forms in the inventory / all distinct confirmed canonical forms | Implemented for OEWN; inventory membership only |
| `A_review` | Confirmed plus rejected candidates / all generated candidates | Implemented annotation-completion measure |
| `U_review` | Unresolved candidates / all generated candidates | Must remain visible and must not be treated as absence |
| `M_frequency` | Confirmed MWE occurrences meeting a declared corpus frequency/range condition / all confirmed occurrences | Not defined or implemented; requires an admitted MWE corpus profile |
| `M_sense` | Confirmed occurrences with a defensible contextual inventory assignment / eligible confirmed occurrences | Contract only; no validity claim |

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

1. **Construct and criterion consequence:** At the same measured `P_word`, does
   `G_component_only` relate to lower global and MWE-critical reading
   comprehension, and does separately measured `P_mwe_sense` add useful
   out-of-sample information beyond a prespecified word-only model?
2. **Technical and scoring adequacy:** With a fixed candidate method, how
   accurately are VPC/VID spans and categories surfaced for review, particularly for
   discontinuous and train-unseen occurrences; how reliably can contextual MWE
   knowledge be scored; and how much human correction is required?
3. **Response process and utility:** Can intended L2 vocabulary researchers
   complete the workflow, reproduce a result, and correctly state what each
   denominator does and does not mean without verbal coaching?

### Secondary sensitivity questions

- How do candidate source, tokenization, unresolved policy, 2K-list version,
  source corpus, frequency/range rule, and word-unit definition change the
  reported values?
- Which errors materially change document-level conclusions rather than only an
  aggregate benchmark score?
- Do MWE transparency, discontinuity, genre, target centrality, and response
  format moderate the relationship without supporting a universal new cutoff?
- How often does `G_holistic_only` reverse the assumed direction of word-only
  misclassification?

Broader idioms, multilingual transfer, learner writing quality, proficiency
prediction, and pedagogical decisions are not core questions for the first
paper. Contextual MWE knowledge is now core; fully automatic word-sense
disambiguation remains out of scope.

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

### Criterion-study architecture

The smallest design capable of informing the 95%/98% literature has three
stages. A corpus-only demonstration or intended-user study cannot replace the
third stage.

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
3. **Prospectively frozen criterion study:** recruit the declared L2 reading
   population, administer several counterbalanced passages, and measure each
   participant's required word and MWE meanings in a separate or counterbalanced
   session to limit test priming. Analyze genuinely untouched readers, texts,
   or items under the registered split.

The design must not assume that list membership equals knowledge. Nominal 95%
and 98% list conditions describe materials; `P_word` is computed from each
participant's demonstrated contextual knowledge and analyzed continuously.
Predicted comprehension at 95% and 98% may be reported as interpretable
reference points, but the analysis must not force a discontinuity there.

The primary outcome is global passage comprehension scored without requiring a
direct definition of each target MWE. MWE-critical comprehension items and
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
| Development | Project-authored diagnostics and a declared training/development partition | Revise contracts, annotation guidance, and candidate method | Report as exploratory development only |
| Coverage materials pilot | Multiple natural, counterbalanced passages near conventional 95%/98% reference points | Calibrate knowledge measures, MWE manipulation, comprehension tasks, scoring, and variance | Pilot readers, texts, and items cannot silently become confirmatory holdout data |
| Criterion study | Tested L2 readers × multiple passages × comprehension items | Test incremental information from `P_mwe_sense` and `G_component_only` beyond `P_word` | Prospective protocol, non-priming knowledge design, crossed dependence, and genuine holdout required for confirmatory language |
| Source-to-target application | Lawfully usable instructional and target corpora | Demonstrate directional word/MWE recurrence such as textbook → examination | Corpus occurrence is not learner knowledge or comprehension |
| ICNALE GRA original/edited pairs | Registered-user, local-only corpus data | Explore sensitivity to expert editing and learner-language noise | Not MWE gold; do not redistribute text or call edits pure spelling correction |
| Technical holdout | Rights-compliant English VPC/VID annotations with contiguous/discontinuous and seen/unseen strata | Optional confirmatory exact-span, category, and candidate-recall evidence | Use as holdout only if genuinely uninspected and prospectively frozen |
| User study | Intended L2 vocabulary researchers; practitioners only if a practitioner claim remains | Task completion, interpretation, reproducibility, burden | Ethics and data-management approval before recruitment |
| Diagnostic sense cases | Project-authored or lawfully annotated polysemy/literalness contrasts | Demonstrate why sense cannot be collapsed into form | Exploratory; not WSD validation |

The reading-material and source-to-target corpus admission records are Phase 0
tasks, not data-availability blockers. ICNALE remains a later production-noise
resource rather than the main criterion dataset. Record population, genre,
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

1. one frozen and lawfully reproducible conventional 1K/2K-banded word-list
   profile for nominal material coverage;
2. participant-specific contextual word knowledge (`P_word`) as the substantive
   word-only criterion model;
3. the current all-confirmed surface-pattern negative control;
4. one transparent list/n-gram or rule-based candidate baseline that can be
   reproduced lawfully; and
5. at most one contextual model only after the first four are frozen.

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

Measurement outcomes:

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

Criterion outcomes:

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

| Phase | Required output | Exit gate | State |
|---|---|---|---|
| 0. Construct and material charter | One-page claim map; accurate 95%/98% lineage; person/list/corpus profile separation; passage, word-test, MWE-test, comprehension, and source-corpus admission criteria; dated decision log | Another researcher can state the target construct, unit, criterion, comparison, and exclusions without reading source code | **Next; not complete** |
| 1. Product truthfulness | UI/export names match the frozen estimands; candidate source and unresolved ceiling are visible; real-browser/accessibility gate passes | No display implies learner knowledge, universal English, automatic confirmation, or MWE frequency when only membership exists | Partial |
| 2. Exploratory criterion pilot | Multiple natural passage versions; contextual word/MWE knowledge measures; global and target-critical comprehension tasks; scoring evidence; variance estimates and simulation-based sample plan | The manipulation is natural, non-tautological, measurable, and capable of distinguishing word coverage from component-only MWE gaps | Not started |
| 3. Technical evaluation | Baseline predictions and stratified span/category/sense/error results on the selected passage domain; optional prospectively frozen holdout | Candidate recall, contextual-decision reliability, and correction burden are reported honestly | Only a transparent occurrence floor exists |
| 4. Frozen criterion study | Registered person × passage × item design; word-only and MWE-extended models; uncertainty, calibration, and genuine held-out results | Any claim beyond reporting is supported after `P_word`; a negative or heterogeneous result is accepted without inventing a new score | Not started |
| 5. Applied corpus and user evaluation | Directional source-to-target example plus declared researcher tasks, interpretation evidence, burden, and qualitative failures | Corpus recurrence is not presented as knowledge, and users correctly interpret all profile types | Not started |
| 6. Optional learner-production robustness | Local ICNALE WE/GRA raw/edited sensitivity and error taxonomy | Kept outside the critical path unless the paper retains learner-writing claims | Deferred |
| 7. Frozen open release | Versioned source, permissible materials, data/retrieval instructions, code, predictions, analysis, checksums, licenses, protocol, report, archive identifier | Clean-room reproduction and browser acceptance succeed from the archive | Not started |
| 8. RMAL submission | Methods-first manuscript and supplement tied to the frozen release | Every manuscript claim maps to a passed evidence gate | Not started |

Failure at a gate changes the claim; it does not trigger silent tuning on the
holdout. Negative findings remain publishable evidence if they clarify when an
MWE-aware method is not worth its cost.

## Stop/go decisions

1. **Contextual word/MWE knowledge cannot be measured without priming or weak
   scoring:** do not claim to inform 95%/98% coverage; narrow the paper to an
   annotation/reporting method.
2. **MWE quantities add negligible held-out information after `P_word`:** report
   the boundary and do not create an adjusted coverage score.
3. **The MWE manipulation changes nonlexical passage properties:** redesign in
   the pilot or use a naturalistic observational design with narrower causal
   language.
4. **No lawful MWE frequency/range resource:** continue with form-inventory and
   member-accounting claims, but remove “MWE frequency coverage” from the first
   paper.
5. **Candidate recall is practically inadequate:** do not market an automatic
   analyzer; keep manual candidate addition and evaluate one better baseline.
6. **Manual burden is unacceptable:** reduce the target category or improve
   ranking; do not hide the burden in aggregate accuracy.
7. **Users misinterpret outputs:** revise labels/instructions and rerun a new
   evaluation sample; unit tests cannot substitute for response-process evidence.
8. **MWE-aware reporting rarely changes interpretation:** report the boundary or
   reconsider whether a standalone tool is justified.
9. **ICNALE use cannot be made reproducible within its terms:** keep it as an
   unshared optional audit, obtain permission, or omit it; do not copy its text
   into the release.

## Immediate execution order

Do these next, in order:

1. write the construct/evidence matrix that separates `L_word(k)`,
   `C_word(A→B)`, `P_word`, `P_mwe_sense`, `G_component_only`, and
   `G_holistic_only`, and record the 95%/98% attribution and non-inferences;
2. specify passage-pair admission, naturalness review, global comprehension,
   target-critical comprehension, contextual word knowledge, contextual MWE
   knowledge, and anti-priming requirements;
3. select only a small development set of natural VPC/VID contrasts and design
   the exploratory pilot before adding another reference dataset or model;
4. audit and rename every unqualified UI/export use of “coverage” against the
   frozen construct table; keep the current TUBELEX and OEWN outputs explicitly
   diagnostic;
5. pilot the measures, preserve every material change, estimate crossed sources
   of variance, and simulate the later sample size;
6. complete candidate/scoring reliability and intended-user pilots, then
   prospectively register only the untouched criterion study;
7. run the criterion study before returning to optional ICNALE learner-writing
   robustness or BERT/fastText comparisons.

Only after these seven steps may the project compare BERT, fastText, a parser, or
another candidate method. Add one dependency only if it improves a declared
decision-relevant outcome enough to justify model/data rights, payload,
compute, privacy, and reproducibility costs.

## Deferred work

The following are legitimate later studies, not first-paper requirements:

- automatic contextual sense assignment and corpus sense-frequency reporting;
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
- archive permissible materials, predictions, analysis, annotation guidance,
  and a simulated or redacted substitute when primary text cannot be shared;
- tag an immutable source release and publish checksums plus an archive DOI;
- reproduce every table and figure from that archive in a clean directory;
- state why any restricted data cannot be shared and how qualified researchers
  can verify the analysis where possible;
- retain pre-adjudication annotations and all negative/error results; and
- recheck the current RMAL Guide for Authors, article type, declarations,
  data/code statement, AI-use disclosure, and fees immediately before upload.

Corrections receive a new version and changelog entry. A resource withdrawal
must not silently substitute a new profile under an old identifier. Browser
hashes identify bytes, not authorship or trusted time.

## Manuscript logic

The paper should be readable without opening the app:

1. **Problem:** conventional known-word token coverage can mark all components
   of an unknown contextual MWE as covered, leaving 95%/98% interpretations
   under-specified.
2. **Evidence boundary:** present 95% and 98% as historically important reference
   points whose relationship with comprehension varies by reader, genre, task,
   and measurement—not as fixed laws.
3. **Operationalization:** separate list-to-text, source-corpus-to-target, and
   tested person-to-text profiles; define occurrence, member, gap, contextual
   sense, component-only gap, unresolved mass, and every denominator.
4. **Method:** describe passage/knowledge/comprehension measurement, the
   human-reviewed workflow, and the open implementation.
5. **Technical evaluation:** report candidate/span/category/contextual-decision
   results, scoring reliability, error strata, correction burden, and any
   genuinely prospective holdout.
6. **Criterion evidence:** compare the frozen word-only and MWE-extended models
   on global and MWE-critical comprehension, with uncertainty, calibration, and
   held-out results at continuous coverage and the 95%/98% reference points.
7. **Applied and response evidence:** demonstrate one directional corpus use
   case and report whether intended users can perform and correctly interpret
   the three profile types.
8. **Boundary and open materials:** state where the method fails, avoid a new
   universal threshold or combined score without evidence, and map every result
   to its decision record, prospective protocol where applicable, and archive.

The title and abstract must say **English VPC/VID** unless broader evidence is
actually collected. “Objective” should mean explicit and repeatable decisions,
not theory-free measurement.

## Definition of done

The project is ready for RMAL submission only when a critical reader can answer
all of the following from the manuscript and archive:

1. What applied-linguistics measurement problem is being solved?
2. What exactly is the lexical unit in each channel?
3. How do list, corpus-recurrence, and tested learner-knowledge profiles differ?
4. Which population, texts, MWE categories, resources, and tokenizers were used?
5. How were contextual word and MWE knowledge measured without circularity or
   uncontrolled priming?
6. How many candidates were missed, corrected, rejected, or unresolved?
7. Does the MWE channel add held-out information beyond measured word coverage,
   including at the 95% and 98% reference points?
8. Can intended researchers perform and interpret the method?
9. Which claims are unsupported?
10. Can every reported number be independently reproduced?

Today the project can answer 1, much of 2, and part of 10 at the
software-contract level. It cannot yet answer 3–8 empirically. That is the
critical path.

## Core references and live records

- [Focused literature search and page-level close reading](LITERATURE_CLOSE_READ.md)
- [Hu and Nation (2000), unknown vocabulary density and comprehension](https://doi.org/10.64152/10125/66973)
- [Nation (2006), vocabulary size for 98% reading/listening coverage](https://doi.org/10.3138/cmlr.63.1.59)
- [Schmitt, Jiang, and Grabe (2011), word coverage and comprehension](https://doi.org/10.1111/j.1540-4781.2011.01146.x)
- [Kremmel et al. (2023), partial replication and threshold critique](https://doi.org/10.1111/lang.12622)
- [Martinez and Murphy (2011), MWE effects on L2 reading](https://ora.ox.ac.uk/objects/uuid%3Aebfa9868-f48b-40da-9b74-513684f28c25)
- [Kremmel, Brunfaut, and Alderson (2017), phraseological knowledge and reading](https://doi.org/10.1093/applin/amv070)
- [RMAL official scope](https://shop.elsevier.com/journals/research-methods-in-applied-linguistics/2772-7661)
- [Computational reproducibility in applied linguistics](https://doi.org/10.1016/j.rmal.2022.100030)
- [ICNALE modules, GRA description, and terms](https://language.sakura.ne.jp/icnale/)
- [Kyle and Eguchi (2021)](https://doi.org/10.21832/9781788924863-007)
- [Kyle and Eguchi analysis resources](https://github.com/kristopherkyle/dependency_bigrams_Kyle_Eguchi_2021)
- [TUBELEX](https://aclanthology.org/2025.coling-main.641/)
- [Open English WordNet 2025](https://github.com/globalwordnet/english-wordnet/releases/tag/2025-edition)
- [Public technical deployment](https://ryuya-dot-com.github.io/Lexical-Diversity-Sophistication-Analysis/)
- `README.md` for current operation, `mwe_contract.json` for executable method
  states, `RIGHTS.md` for resource admission, and `CHANGELOG.md` for history.

## Ponytail disposition

Do not add a framework, server, database, account system, model, metric family,
or manuscript automation while the claim, lawful L2 sample, and validation
protocol remain unfrozen. The next useful artifact is evidence, not code.
