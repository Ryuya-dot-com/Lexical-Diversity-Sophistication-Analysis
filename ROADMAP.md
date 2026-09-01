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

Develop and validate an open, browser-local, human-in-the-loop method for
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
- submission becomes defensible only after a preregistered L2 measurement study
  and intended-user study.

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
| Technical evidence | Five project-authored fixtures; 40-occurrence STREUSLE projection; transparent surface baseline | Adequately sized held-out evaluation, full error analysis, and applied-L2 transfer evidence |
| Sense evidence | All 17 OEWN `take in#v` candidates and synthetic contextual decisions | Independent contextual gold, reliability, WSD validation, or sense-frequency coverage |
| Research data | Synthetic cases and external benchmark projection | Lawful, pinned, sampled L2 evaluation texts and annotation protocol |
| Open science | Public source, tests, rights ledger, static deployment | Preregistration, immutable release, DOI/checksum bundle, analysis scripts and report |

The public prototype is therefore an **implemented method hypothesis**, not a
validated research instrument.

## Critical-reviewer audit

### Likely rejection risks

| Priority | Reviewer objection | Why it is serious | Required answer before submission |
|---|---|---|---|
| 1 | “Coverage” is underdefined | Current TUBELEX output is surface-form profile membership and OEWN output is lexicon membership. Neither is automatically conventional lexical coverage, learner knowledge, or MWE frequency coverage. | Qualify every measure by resource, unit, and denominator; either admit a lawful MWE frequency/range reference or narrow the paper to inventory-aware lexical reporting. |
| 2 | The novelty is a feature difference, not a demonstrated methods contribution | TAALES, Multi-Word Units Profiler, phrase profilers, and annotation tools already cover adjacent steps. | Show empirically which occurrences or interpretations are lost by word-only/list-only workflows and what the proposed bridge changes. |
| 3 | No relevant L2 evidence exists | Synthetic examples and a small general-English benchmark do not establish usefulness for L2 vocabulary research. | Freeze a lawful applied-L2 sampling frame and report document-level measurement consequences with uncertainty. |
| 4 | False negatives are invisible | User-supplied patterns can only review candidates they generate. A polished review UI cannot recover missed MWEs. | Evaluate candidate recall first, especially discontinuous and unseen forms, and expose the candidate source and known ceiling in every export. |
| 5 | Human “gold” is undefined | Confirming VPC/VID status and boundaries requires judgment; project-authored fixtures are not independent validation. | Publish annotation guidelines, train at least two independent annotators where new gold is created, adjudicate disagreements, and report category/span agreement. |
| 6 | The paper is trying to validate too much | Detection, form coverage, sense assignment, usability, pedagogy, and all MWE types would require different data and validity arguments. | Limit the confirmatory first paper to English VPC/VID form-level reporting; keep sense and broader idioms exploratory or future work. |
| 7 | User value is assumed | Researchers may not understand separate denominators or may find manual review too burdensome. | Run predeclared task and interpretation studies with intended L2 vocabulary researchers, recording critical errors and review effort. |
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

### Confirmatory questions

1. **Measurement consequence:** On a preregistered sample of L2-relevant English
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
knowledge, proficiency relations, and pedagogical decisions are not
confirmatory questions for the first paper.

## Validation design to preregister

### Evidence lanes

| Lane | Data | Purpose | Separation rule |
|---|---|---|---|
| Development | Project-authored diagnostics and a declared training/development partition | Fix contracts, annotation guidance, and candidate method | Never report as held-out performance |
| Technical holdout | Rights-compliant English VPC/VID annotations with contiguous/discontinuous and seen/unseen strata | Exact span, category, and candidate-recall evidence | Freeze before final method selection |
| Applied-L2 sample | Lawfully usable English learner or L2-facing texts sampled by a written protocol | Estimate document-level measurement consequences | No claim beyond the sampled genres/population |
| User study | Intended L2 vocabulary researchers; practitioners only if a practitioner claim remains | Task completion, interpretation, reproducibility, burden | Ethics and data-management approval before recruitment |
| Diagnostic sense cases | Project-authored or lawfully annotated polysemy/literalness contrasts | Demonstrate why sense cannot be collapsed into form | Exploratory; not WSD validation |

The applied-L2 corpus decision is a Phase 0 blocker. Record population, genre,
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

The protocol must set sample sizes from a precision or information target, not
from convenience. Numerical success thresholds are fixed after a development
pilot and before the held-out data are inspected; this roadmap does not invent
them in advance of feasibility evidence.

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
| 0. Claim and protocol freeze | One-page claim map, qualified terminology, corpus/resource decision memo, annotation plan, sampling/analysis plan, dev/holdout split, failure thresholds | Another researcher can state the target construct, unit, comparison, population, and exclusions without reading source code | **Next; not complete** |
| 1. Product truthfulness | UI/export names match the frozen estimands; candidate source and unresolved ceiling are visible; real-browser/accessibility gate passes | No display implies learner knowledge, universal English, automatic confirmation, or MWE frequency when only membership exists | Partial |
| 2. Data and gold admission | Lawful applied-L2 sample, annotation guide, independent decisions, adjudication record, immutable hashes | Rights/ethics and annotation evidence permit independent audit | Not started |
| 3. Technical validation | Frozen baseline predictions and stratified span/category/error results | Candidate recall and correction burden pass preregistered thresholds; otherwise narrow the task or keep the tool manual | Only a transparent floor exists |
| 4. Measurement study | Document-level word-only/MWE-aware consequences and sensitivity analyses | The added MWE channel changes decision-relevant reporting often enough to justify the method; otherwise report a negative result | Not started |
| 5. Intended-user validation | Predeclared researcher tasks, interpretation evidence, burden, qualitative failures | Intended users can complete and correctly interpret the core workflow at the preregistered standard | Not started |
| 6. Frozen open release | Versioned source, data/retrieval instructions, code, predictions, analysis, checksums, licenses, protocol, report, archive identifier | Clean-room reproduction and browser acceptance succeed from the archive | Not started |
| 7. RMAL submission | Methods-first manuscript and supplement tied to the frozen release | Every manuscript claim maps to a passed evidence gate | Not started |

Failure at a gate changes the claim; it does not trigger silent tuning on the
holdout. Negative findings remain publishable evidence if they clarify when an
MWE-aware method is not worth its cost.

## Stop/go decisions

1. **No lawful applied-L2 sample:** stop empirical generalization; publish only
   a protocol/tool note elsewhere or obtain a new data basis.
2. **No lawful MWE frequency/range resource:** continue with form-inventory and
   member-accounting claims, but remove “MWE frequency coverage” from the first
   paper.
3. **Candidate recall below the frozen threshold:** do not market an automatic
   analyzer; keep manual candidate addition and evaluate one better baseline.
4. **Manual burden is unacceptable:** reduce the target category or improve
   ranking; do not hide the burden in aggregate accuracy.
5. **Users misinterpret outputs:** revise labels/instructions and rerun a new
   evaluation sample; unit tests cannot substitute for response-process evidence.
6. **MWE-aware reporting rarely changes interpretation:** report the boundary or
   reconsider whether a standalone tool is justified.

## Immediate execution order

Do these next, in order:

1. write the preregistration-ready claim/evidence matrix and choose the
   form-level first-paper scope;
2. audit and rename every unqualified UI/export use of “coverage” against the
   measurement table above;
3. select one lawful applied-L2 evaluation sample and decide whether a lawful
   MWE frequency/range profile exists; record a go/no-go decision for each;
4. freeze annotation guidance, development data, technical holdout, primary
   outcomes, uncertainty method, and failure thresholds;
5. complete real-browser, keyboard, narrow-screen, network, and screen-reader
   checks on the existing vertical slice;
6. run a development-only annotation and user-task pilot, revise once, then
   freeze the confirmatory protocol.

Only after these six steps may the project compare BERT, fastText, a parser, or
another candidate method. Add one dependency only if it improves a predeclared
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

- preregister the confirmatory protocol before inspecting final holdout results;
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
4. **Technical validity:** report held-out candidate/span/category results and
   error strata.
5. **Measurement consequence:** report what changes on the applied-L2 sample and
   under sensitivity choices.
6. **Response process:** report whether intended users can perform and interpret
   the method.
7. **Boundary:** state where the method fails, what remains manual, and which
   populations/resources are not represented.
8. **Open materials:** map every result to the frozen protocol and archive.

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

- [RMAL official scope](https://shop.elsevier.com/journals/research-methods-in-applied-linguistics/2772-7661)
- [Computational reproducibility in applied linguistics](https://doi.org/10.1016/j.rmal.2022.100030)
- [TUBELEX](https://aclanthology.org/2025.coling-main.641/)
- [Open English WordNet 2025](https://github.com/globalwordnet/english-wordnet/releases/tag/2025-edition)
- [Public technical deployment](https://ryuya-dot-com.github.io/Lexical-Diversity-Sophistication-Analysis/)
- `README.md` for current operation, `mwe_contract.json` for executable method
  states, `RIGHTS.md` for resource admission, and `CHANGELOG.md` for history.

## Ponytail disposition

Do not add a framework, server, database, account system, model, metric family,
or manuscript automation while the claim, lawful L2 sample, and validation
protocol remain unfrozen. The next useful artifact is evidence, not code.
