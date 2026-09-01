# Open MWE-aware lexical reporting: RMAL roadmap

Status: research claim reset and evidence-gated plan, reviewed 2026-09-01

## One-minute answer

In plain language: the study asks what a word-only analysis hides when an
expression such as `take it in` must also be reviewed as one lexical unit, and
whether L2 researchers can report that extra information reproducibly.

### What problem does this study address?

Word-level lexical profilers can count `take`, `it`, and `in` while hiding the
fact that `take ... in` may be one discontinuous verb-particle construction.
Contiguous n-gram lookup misses the separated form, while dictionary or list
membership alone cannot decide whether a particular occurrence is an MWE or
which contextual sense applies. This changes what is treated as the lexical
unit and what a reported denominator means.

### What will the study do?

Develop and empirically evaluate an open, browser-local, human-in-the-loop method for
second-language (L2) vocabulary research that:

1. uses researcher-supplied patterns to find reviewable English verb-particle
   construction (VPC) and verbal-idiom (VID) candidates, including separated
   members;
2. lets a researcher confirm, reject, correct, or leave each candidate
   unresolved;
3. reports word-profile membership, confirmed-MWE accounting, MWE-inventory
   membership, and unresolved mass as separate quantities; and
4. exports the decisions, denominators, resource versions, and limitations
   needed to reproduce the report.

The Web app is the executable implementation of the method. It is not the
research contribution by itself.

### What will the first paper claim?

> A transparent, human-reviewed workflow can expose MWE lexical units that a
> word-only report masks, while preserving uncertainty and making every
> denominator and resource decision auditable in L2 vocabulary research.

That claim is provisional until technical, measurement, and intended-user
evidence pass the gates below.

### What will it not claim?

The first paper will not claim automatic MWE analysis, complete English MWE
coverage, learner knowledge, text difficulty, writing quality, proficiency,
CEFR level, pedagogical priority, causal effects, or valid contextual sense
assignment. It will not present a combined word/MWE score.

## Is the purpose transparent now?

At the purpose level, yes: the study is about **the consequences of lexical-unit
decisions for transparent L2 lexical reporting**. Detection, interface design,
and resource engineering are supporting components.

At the evidence level, not yet. A beginning graduate student should currently
be told:

- the app can demonstrate the workflow on a text;
- the app cannot yet show that the workflow is accurate, useful, or
  generalizable on learner-language research data;
- TUBELEX matching and OEWN membership are resource-conditioned lookup results,
  not estimates of what a learner knows; and
- submission becomes defensible only after an honestly reported L2 measurement
  study and intended-user study; prospective registration is needed only for
  claims presented as confirmatory.

If this distinction cannot be explained without specialist terminology, the
method is not ready for participants, reviewers, or publication.

## Contribution hierarchy

The project previously allowed three possible papers to compete. The hierarchy
is now fixed.

| Rank | Contribution | Role in the first RMAL paper |
|---|---|---|
| 1 | MWE-aware lexical reporting method for L2 vocabulary research | Primary contribution |
| 2 | Open browser implementation with auditable exports | Executable method and open material |
| 3 | Candidate-generation accuracy | Necessary technical validity evidence |
| 4 | Intended-user task and interpretation evidence | Necessary use/response-process evidence |
| 5 | Contextual sense assignment | Data-model demonstration only; no first-paper validity claim |
| 6 | General lexical diversity or sophistication | Out of scope |

The planned manuscript is an empirical methods article, not a software note,
benchmark paper, corpus paper, or pedagogical intervention study. RMAL is a
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
| Technical evidence | Five project-authored fixtures; 40-occurrence STREUSLE projection; transparent surface baseline | Broader evaluation, full error analysis, learner-error sensitivity, and applied-L2 transfer evidence |
| Sense evidence | All 17 OEWN `take in#v` candidates and synthetic contextual decisions | Independent contextual gold, reliability, WSD validation, or sense-frequency coverage |
| Research data | Synthetic cases and external benchmark projection; ICNALE WE/GRA identified as local-only candidates | Corpus admission memo, reproducible sample, learner-error study, and MWE annotation protocol |
| Open science | Public source, tests, rights ledger, static deployment | Explicit exploratory decision history, immutable release, DOI/checksum bundle, analysis scripts and report |

The public prototype is therefore an **implemented method hypothesis**, not a
validated research instrument.

## Learner-language errors and corpus evidence

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
The paired GRA analysis belongs in the exploratory phase; a separately
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
| 1 | “Coverage” is underdefined | Current TUBELEX output is surface-form profile membership and OEWN output is lexicon membership. Neither is automatically conventional lexical coverage, learner knowledge, or MWE frequency coverage. | Qualify every measure by resource, unit, and denominator; either admit a lawful MWE frequency/range reference or narrow the paper to inventory-aware lexical reporting. |
| 2 | The novelty is a feature difference, not a demonstrated methods contribution | TAALES, Multi-Word Units Profiler, phrase profilers, and annotation tools already cover adjacent steps. | Show empirically which occurrences or interpretations are lost by word-only/list-only workflows and what the proposed bridge changes. |
| 3 | No relevant L2 evidence exists | Synthetic examples and a small general-English benchmark do not establish usefulness for L2 vocabulary research. | Admit a lawful applied-L2 sampling frame, beginning with an exploratory ICNALE GRA original/edited sensitivity analysis, and report document-level consequences with uncertainty. |
| 4 | False negatives are invisible | User-supplied patterns can only review candidates they generate. A polished review UI cannot recover missed MWEs. | Evaluate candidate recall first, especially discontinuous and unseen forms, and expose the candidate source and known ceiling in every export. |
| 5 | Human “gold” is undefined | Confirming VPC/VID status and boundaries requires judgment; project-authored fixtures are not independent validation. | Publish annotation guidelines, train at least two independent annotators where new gold is created, adjudicate disagreements, and report category/span agreement. |
| 6 | The paper is trying to validate too much | Detection, form coverage, sense assignment, usability, pedagogy, and all MWE types would require different data and validity arguments. | Limit the first paper to exploratory English VPC/VID form-level reporting; keep sense and broader idioms as diagnostics or future work. |
| 7 | User value is assumed | Researchers may not understand separate denominators or may find manual review too burdensome. | Run declared task and interpretation studies with intended L2 vocabulary researchers, recording critical errors and review effort. |
| 8 | Resource choice may drive the result | TUBELEX models audiovisual/spoken exposure; OEWN is a lexicon, not a corpus. Tokenizers also differ by design. | Treat resource/tokenizer sensitivity as a named limitation and, only if required by RQ1, add one justified written-register contrast. |
| 9 | Generality is overstated | English VPC/VID evidence cannot support “MWE” in general, multilingual use, or pedagogical importance. | Put English VPC/VID in the title, abstract, sampling frame, interface, and claim boundary. |
| 10 | Reproducibility is ahead of validity | Hashes and tests reproduce calculations but cannot validate the construct or response process. | Organize the paper around a validity argument; present software reproducibility as one evidence source, not the conclusion. |

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
not an allegedly superior single score.

The term “lexical coverage” must be followed by its resource and unit. If an
open MWE frequency/range profile cannot be lawfully admitted, the first paper
must use **MWE-aware lexical reporting** or **inventory membership**, not imply a
frequency-based MWE coverage estimate.

## Research questions

### Core exploratory questions

1. **Measurement consequence:** On a declared sample of L2-relevant English
   texts, how much confirmed VPC/VID member-token mass and form-inventory
   information is hidden by a word-only report, and how much varies across
   documents?
2. **Technical adequacy:** With a fixed candidate method, how accurately are
   VPC/VID spans and categories surfaced for review, particularly for
   discontinuous and train-unseen occurrences, and how much human correction is
   required?
3. **Response process and utility:** Can intended L2 vocabulary researchers
   complete the workflow, reproduce a result, and correctly state what each
   denominator does and does not mean without verbal coaching?

### Secondary sensitivity questions

- How do candidate source, tokenization, unresolved policy, and reference
  profile change the reported values?
- Which errors materially change document-level conclusions rather than only an
  aggregate benchmark score?

Contextual sense assignment, broader idioms, multilingual transfer, learner
knowledge, proficiency relations, and pedagogical decisions are not core
questions for the first paper.

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

### Evidence lanes

| Lane | Data | Purpose | Separation rule |
|---|---|---|---|
| Development | Project-authored diagnostics and a declared training/development partition | Revise contracts, annotation guidance, and candidate method | Report as exploratory development only |
| ICNALE GRA original/edited pairs | Registered-user, local-only corpus data | Explore sensitivity to expert editing and learner-language noise | Not MWE gold; do not redistribute text or call edits pure spelling correction |
| Technical holdout | Rights-compliant English VPC/VID annotations with contiguous/discontinuous and seen/unseen strata | Optional confirmatory exact-span, category, and candidate-recall evidence | Use as holdout only if genuinely uninspected and prospectively frozen |
| Applied-L2 sample | Lawfully usable English learner or L2-facing texts sampled by a written protocol | Estimate document-level measurement consequences | Label exploratory unless a confirmatory sampling/analysis plan was frozen in advance |
| User study | Intended L2 vocabulary researchers; practitioners only if a practitioner claim remains | Task completion, interpretation, reproducibility, burden | Ethics and data-management approval before recruitment |
| Diagnostic sense cases | Project-authored or lawfully annotated polysemy/literalness contrasts | Demonstrate why sense cannot be collapsed into form | Exploratory; not WSD validation |

The applied-L2 corpus admission record is a Phase 0 task, not a data-availability
blocker. ICNALE makes access feasible, but its role and restrictions still need
to be fixed. Record population, genre,
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

1. the TUBELEX word-only report;
2. the current all-confirmed surface-pattern negative control;
3. one transparent list/n-gram or rule-based candidate baseline that can be
   reproduced lawfully; and
4. at most one contextual model only after the first three are frozen.

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

- per-document `W_token`, `W_type`, `M_member`, `M_inventory_token`,
  `M_inventory_type`, `A_review`, and `U_review`;
- paired within-document consequences of word-only versus MWE-aware reporting;
- sensitivity to candidate method, unresolved policy, and any admitted reference
  contrast; and
- annotated cases where the methodological interpretation changes.

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
| 0. Exploratory charter and corpus admission | One-page claim map, qualified terminology, ICNALE WE/GRA rights-and-role memo, annotation plan, exploratory questions, and dated decision log | Another researcher can state the target construct, unit, corpus role, comparison, and exclusions without reading source code | **Next; not complete** |
| 1. Product truthfulness | UI/export names match the frozen estimands; candidate source and unresolved ceiling are visible; real-browser/accessibility gate passes | No display implies learner knowledge, universal English, automatic confirmation, or MWE frequency when only membership exists | Partial |
| 2. Exploratory learner-data study | Local ICNALE WE distribution study, GRA original/edited analysis, error taxonomy, paired sensitivity results, and MWE annotation feasibility | The study identifies which learner-language phenomena materially affect matching and candidate review without redistributing corpus text | Not started |
| 3. Technical evaluation | Baseline predictions and stratified span/category/error results; optional prospectively frozen holdout | Candidate recall and correction burden are reported honestly; a validated-analyzer claim requires prospectively defined criteria | Only a transparent floor exists |
| 4. Measurement study | Document-level word-only/MWE-aware consequences and sensitivity analyses | The evidence establishes the observed boundary; a negative or heterogeneous result is acceptable | Not started |
| 5. Intended-user evaluation | Declared researcher tasks, interpretation evidence, burden, qualitative failures | The paper reports what intended users can and cannot complete or interpret; a success-rate claim requires a prospective standard | Not started |
| 6. Frozen open release | Versioned source, data/retrieval instructions, code, predictions, analysis, checksums, licenses, protocol, report, archive identifier | Clean-room reproduction and browser acceptance succeed from the archive | Not started |
| 7. RMAL submission | Methods-first manuscript and supplement tied to the frozen release | Every manuscript claim maps to a passed evidence gate | Not started |

Failure at a gate changes the claim; it does not trigger silent tuning on the
holdout. Negative findings remain publishable evidence if they clarify when an
MWE-aware method is not worth its cost.

## Stop/go decisions

1. **ICNALE use cannot be made reproducible within its terms:** keep it as an
   unshared exploratory audit, obtain permission, or choose another corpus; do
   not copy its text into the release.
2. **No lawful MWE frequency/range resource:** continue with form-inventory and
   member-accounting claims, but remove “MWE frequency coverage” from the first
   paper.
3. **Candidate recall is practically inadequate:** do not market an automatic
   analyzer; keep manual candidate addition and evaluate one better baseline.
4. **Manual burden is unacceptable:** reduce the target category or improve
   ranking; do not hide the burden in aggregate accuracy.
5. **Users misinterpret outputs:** revise labels/instructions and rerun a new
   evaluation sample; unit tests cannot substitute for response-process evidence.
6. **MWE-aware reporting rarely changes interpretation:** report the boundary or
   reconsider whether a standalone tool is justified.

## Immediate execution order

Do these next, in order:

1. write an exploratory claim/evidence matrix and choose the form-level
   first-paper scope;
2. audit and rename every unqualified UI/export use of “coverage” against the
   measurement table above;
3. create an ICNALE WE v2.6/GRA v2.1 admission memo, a local-only distribution
   plan, and an original/edited sensitivity plan; decide separately whether a
   lawful MWE frequency/range profile exists;
4. define the learner-error taxonomy, exploratory outcomes, annotation guidance,
   and uncertainty summaries; reserve an untouched holdout only if a later
   confirmatory claim is planned;
5. complete real-browser, keyboard, narrow-screen, network, and screen-reader
   checks on the existing vertical slice;
6. run an exploratory annotation and user-task pilot and preserve the decision
   history; optionally register a bounded follow-up validation after the method
   stabilizes.

Only after these six steps may the project compare BERT, fastText, a parser, or
another candidate method. Add one dependency only if it improves a declared
decision-relevant outcome enough to justify model/data rights, payload,
compute, privacy, and reproducibility costs.

## Deferred work

The following are legitimate later studies, not first-paper requirements:

- validated contextual sense assignment and sense-frequency reporting;
- non-verbal idioms and broader MWE taxonomies;
- multilingual transfer;
- multiple word-reference profiles and register-sensitive comparisons;
- group modelling, proficiency relations, or pedagogical intervention studies;
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

1. **Problem:** word-only and list-only procedures can hide or misclassify MWE
   lexical units and denominators in L2 vocabulary research.
2. **Operationalization:** define candidate, confirmed occurrence, member, gap,
   inventory membership, unresolved mass, and each reference-conditioned rate.
3. **Method:** describe the human-reviewed workflow and open implementation.
4. **Technical evaluation:** report candidate/span/category results, error
   strata, learner-error sensitivity, and any genuinely prospective holdout.
5. **Measurement consequence:** report what changes on the applied-L2 sample and
   under sensitivity choices.
6. **Response process:** report whether intended users can perform and interpret
   the method.
7. **Boundary:** state where the method fails, what remains manual, and which
   populations/resources are not represented.
8. **Open materials:** map every result to its dated exploratory decision record
   or prospectively registered analysis and to the frozen archive.

The title and abstract must say **English VPC/VID** unless broader evidence is
actually collected. “Objective” should mean explicit and repeatable decisions,
not theory-free measurement.

## Definition of done

The project is ready for RMAL submission only when a critical reader can answer
all of the following from the manuscript and archive:

1. What applied-linguistics measurement problem is being solved?
2. What exactly is the lexical unit in each channel?
3. Which population, texts, MWE categories, resources, and tokenizers were used?
4. How many candidates were missed, corrected, rejected, or unresolved?
5. What changed relative to the word-only and transparent baseline reports?
6. Can intended researchers perform and interpret the method?
7. Which claims are unsupported?
8. Can every reported number be independently reproduced?

Today the project can answer 1, 2, and much of 8 at the software-contract level.
It cannot yet answer 3–6 empirically. That is the critical path.

## Core references and live records

- [Focused literature search and page-level close reading](LITERATURE_CLOSE_READ.md)
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
