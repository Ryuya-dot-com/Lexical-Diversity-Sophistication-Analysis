# Focused literature search and page-level close reading

Status: scoping review and design audit, 2026-09-01

This is a focused, reproducible search record for the current method-design
decisions. It is not a systematic review and makes no exhaustiveness claim. The
selection rule was deliberately strict: a work had to change a live decision
about learner-language robustness, MWE identification, MWE-aware coverage,
contextual sense assignment, or the novelty of the proposed application; and a
lawful full PDF had to be available so that every page could be checked.

## Search scope and selection

The search covered ACL Anthology, publisher and institutional pages, author
pages, and general scholarly Web search. Query families combined terms for:

- learner English, spelling/grammar error, dependency parsing, and annotation;
- multiword expression/unit, phrasal verb, idiom, collocation, and learner
  corpus;
- vocabulary list, lexical coverage, text comprehension, CEFR, and MWE;
- lexical sophistication, polysemy, word-sense disambiguation, BERT, and TAALES;
- applied-linguistics software, validation, reproducibility, and RMAL.

Six core documents (81 PDF pages) were selected for this pass. Each was read
page by page from extracted text and visually checked from a rendered PNG. PDF
page numbers below count from the first PDF page; printed page or slide numbers
are added where useful.

| Work | Why it is core now | What it cannot establish |
|---|---|---|
| [Eguchi (2021), *Introducing Multi-Word Units Profiler*](https://masakieguchi.weebly.com/uploads/8/6/4/6/86461612/eguchi_2021_introducing_mwu_profiler.pdf) | Closest existing user-text MWU profiling application and the user-supplied source | A presentation and software description, not an accuracy or validity study |
| [Berzak et al. (2016), *Universal Dependencies for Learner English*](https://aclanthology.org/P16-1070/) | Direct evidence about raw/corrected learner text and tagging/parsing error | Performance of current parsers, MWE detection, or lexical coverage |
| [Kochmar et al. (2020), *Detecting Multiword Expression Type Helps Lexical Complexity Assessment*](https://aclanthology.org/2020.lrec-1.545/) | Separates phrase spans, MWE status, MWE type, and reader-rated complexity | Free-text MWE identification; it assumes an oracle-identified MWE at modeling time |
| [Li and Gaillat (2020), *Automatic detection of unexpected/erroneous collocations in learner corpus*](https://aclanthology.org/2020.mwe-1.13/) | Direct negative evidence on treating absence from a native reference list as learner error | A usable detector; the reported end-to-end results are very weak |
| [Lee and Uvaliyev (2023), *Automatic Generation of Vocabulary Lists with Multiword Expressions*](https://aclanthology.org/2023.mwe-1.12/) | Closest published formalization of MWE-aware vocabulary coverage and learning priority | Observed comprehension or a detector for discontinuous/contextual MWEs |
| [Hu, Lu, and Hu (2025), *Developing fine-grained sense-aware lexical sophistication indices based on the CEFR levels of word senses*](https://doi.org/10.3758/s13428-025-02741-z) | Most direct recent answer to the `take in` polysemy question and to using BERT/WSD with learner texts | Openly redistributable EVP data, phrase identification, or error-free generalization |

Deferred rather than silently ignored: Lu and Hu (2022) is the coarse-grained
predecessor fully compared in the 2025 paper; Kyle and Eguchi (2021) was not
available as a lawful full chapter PDF in this search, although its public
analysis repository remains prior art; Paquot's phraseological-complexity work,
the Constant et al. MWE survey, the 2025 MWE-processing agenda, and automated
writing-evaluation validity reviews are candidates for the next construct-
validity pass rather than substitutes for the six immediate design decisions.

## Page-level notes

### Eguchi (2021): *Introducing Multi-Word Units Profiler* — 34 slides

- **PDF p. 1 / slide 1:** Title, presenter, institutional context, and date. This
  is a methodological presentation, not a peer-reviewed validation report.
- **PDF p. 2 / slide 2:** Locates the work in an L2 vocabulary/NLP lab and links
  it to web versions of TAALED, TAALES, and TAASSC. The lineage makes a new
  generic web profiler particularly vulnerable to a “wheel reinvention” review.
- **PDF p. 3 / slide 3:** Defines the talk as motivation, features, demo,
  methodological issues, and outlook. Accuracy evidence is not promised here.
- **PDF p. 4 / slide 4:** Places MWU profiling beside Range, VocabProfiler,
  AntWordProfiler, and New Word Level Checker. The pedagogical questions are
  word knowledge, difficult items, and target occurrence counts.
- **PDF p. 5 / slide 5:** Uses a broad MWU umbrella: collocations, multiword
  verbs, lexical bundles, binomials, and idioms. These are claimed to be common,
  processable as chunks, socially relevant, and related to L2 skills, but their
  constructs are not collapsed into one measurement.
- **PDF p. 6 / slide 6:** Motivates instruction through low frequency, weak
  perceptual salience, unrecognized usefulness, and L1 incongruence. These are
  pedagogical-priority dimensions, not consequences of coverage alone.
- **PDF p. 7 / slide 7:** Shows the core product: paste text, select lists,
  receive highlighted items and a table. That workflow is already prior art.
- **PDF p. 8 / slide 8:** Demo divider only.
- **PDF p. 9 / slide 9:** Demo input view with four list checkboxes and a server
  submission. It establishes list-conditioned profiling, not local privacy or
  model validity.
- **PDF p. 10 / slide 10:** Demo output highlights multiple overlapping list
  matches in a passage. The image does not provide recoverable gold labels or
  false-positive/false-negative counts.
- **PDF p. 11 / slide 11:** Names PHRASE, Academic Formulas, and Academic
  Collocations among the lists, plus external concordance links. Resource
  choice and item-level evidence are central parts of the user experience.
- **PDF p. 12 / slide 12:** Divides the research background into intervention
  and corpus-driven list development.
- **PDF p. 13 / slide 13:** Summarizes pedagogical intervention findings,
  including chunk discovery and textual enhancement. These studies concern
  learning effects; they do not validate automatic MWU identification.
- **PDF p. 14 / slide 14:** Explicitly states that “important” MWUs depend on
  purpose, genre, and register. Frequency plus expert judgment is the recurring
  list-development pattern.
- **PDF p. 15 / slide 15:** Pipeline divider only.
- **PDF p. 16 / slide 16:** Documents Python 3.8, spaCy 2.3, tokenization,
  lemmatization, dependency parsing, n-gram/dependency candidate extraction,
  list matching, and HTML/CSS output. This is the clearest architectural prior
  art, but the versions are historical.
- **PDF p. 17 / slide 17:** Lemmatization addresses grammatical inflection in
  list matching. It does not address misspellings or contextual meaning.
- **PDF p. 18 / slide 18:** Adjacent 2–4-grams supply one candidate channel.
  Adjacency cannot recover a separated particle construction by itself.
- **PDF p. 19 / slide 19:** Direct dependency relations supply a second
  candidate channel, illustrated with a verb–object relation.
- **PDF p. 20 / slide 20:** Dependency parsing is proposed for dislocated
  collocations and avoids an arbitrary token window. The example inserts
  modifiers inside a verb–object collocation; it is not evidence that a
  pronominally separated VPC such as `take it in` is correctly detected.
- **PDF p. 21 / slide 21:** Candidates are lemmatized and matched to corpus-based
  lists. Occurrence truth and contextual sense are not separate stages here.
- **PDF p. 22 / slide 22:** Spelling variants, inflection, and dislocation are
  presented as handled; passives and type-specific restrictions are future
  work. The slide discusses orthographic varieties, not learner misspellings.
- **PDF p. 23 / slide 23:** Outlook divider only.
- **PDF p. 24 / slide 24:** Crucially, empirical comparison against expert
  annotations is a development plan. The author also anticipates n-gram false
  positives, list refinement, domain/register lists, clearer frequency, glosses,
  and intervention studies. Therefore the presentation must not be cited as
  detector-validation evidence.
- **PDF p. 25 / slide 25:** Envisions interaction among pedagogy, corpus work,
  instructed-SLA research, and CALL. This supports researcher-facing workflows,
  but not a single universal score.
- **PDF p. 26 / slide 26:** Gives the software citation, identifies Lextutor as
  related prior art, and points to Kyle and Eguchi (2021) for dependency
  collocations.
- **PDF p. 27 / slide 27:** References for the Academic Collocation List,
  AntWordProfiler, formulaic-sequence intervention, and language socialization;
  no additional software-evaluation evidence appears.
- **PDF p. 28 / slide 28:** References for textual enhancement,
  VocabProfiler, the idiom principle, and spaCy; no new empirical result for the
  profiler appears.
- **PDF p. 29 / slide 29:** References for phraseological reading knowledge,
  dependency-based sophistication, PHRASE, and New Word Level Checker; this
  confirms the tool's research lineage without validating its detector.
- **PDF p. 30 / slide 30:** References for Range, the Academic Formulas List,
  and L2 collocation production/processing; no new method claim appears.
- **PDF p. 31 / slide 31:** References for the idiom principle and oral
  collocation knowledge; no new software accuracy evidence appears.
- **PDF p. 32 / slide 32:** Extra-slides divider only.
- **PDF p. 33 / slide 33:** Contrasts the PHRASE list (receptive, BNC,
  frequency/meaning/transparency) with the Academic Formulas List (academic
  speech/writing, frequency, MI, and teacher usefulness). A list embodies a
  population, register, unit, and selection rule.
- **PDF p. 34 / slide 34:** Describes the Academic Collocations List as a
  frequency/association pipeline followed by manual exclusion and expert
  judgment. Automated corpus evidence alone is not treated as pedagogical truth.

**Decision:** do not recreate list highlighting as the contribution. Retain the
distinct local workflow: reviewable occurrence decisions plus separate
word-form, MWE-form, and MWE-sense reference channels. Treat dependency parsing
as a candidate generator to be benchmarked on `take it in`, not as proof.

### Berzak et al. (2016): *Universal Dependencies for Learner English* — 10 pages

- **PDF p. 1 / printed p. 737:** Introduces TLE: 5,124 FCE learner sentences with
  manual POS/dependency analyses for original and corrected versions. The
  two-layer design directly supports controlled error-sensitivity analysis.
- **PDF p. 2 / printed p. 738:** Reports 97,681 original tokens, 98,976 corrected
  tokens, 924 writers, ten L1s, and 2.67 errors per selected sentence. Sampling
  required at least one non-spelling, non-punctuation error, so this is an
  error-enriched sample rather than a representative prevalence estimate.
- **PDF p. 3 / printed p. 739:** Documents eight weeks of annotator training,
  practice on native and ESL data, weekly adjudication, and annotation from
  scratch. Corrected-layer annotations were copied only as reviewable drafts.
- **PDF p. 4 / printed p. 740:** Requires active review, third-person judgment,
  explicit ambiguity records, and targeted debugging; creation exceeded 2,000
  hours. Literal surface analysis is the default for noncanonical learner data.
- **PDF p. 5 / printed p. 741:** Shows literal treatment of extra/omitted
  prepositions, tense, and plausible malformed words, with exceptions when a
  literal analysis is impossible. Misspellings are interpreted using the
  correction while alternative literal POS information is retained as metadata.
- **PDF p. 6 / printed p. 742:** Reports very high post-edit agreement and sets
  up parser comparisons. High annotation consistency required a dedicated ESL
  scheme and adjudication; it did not emerge automatically from a standard
  English parser.
- **PDF p. 7 / printed p. 743:** Across training regimes, original learner text
  loses about 1.0 UPOS point, 0.61 POS, 1.9 UAS, 1.59 label accuracy, and 2.21
  LAS relative to corrected text. At error-marked tokens the average gaps versus
  unmarked tokens are much larger: 5.0 UPOS, 6.65 POS, 4.67 UAS, 6.56 label
  accuracy, and 7.39 LAS.
- **PDF p. 8 / printed p. 744:** Parsing declines as the share of erroneous
  tokens rises while corrected-text performance stays comparatively stable.
  The authors call the global effect limited, but the local error effect remains
  important for MWE members and dependencies. Comparisons control sentence
  content and length better than earlier between-sentence work.
- **PDF p. 9 / printed p. 745:** Concludes that a manual, double-reviewed,
  original/corrected learner treebank can support learner-language NLP. The rest
  of the page begins references.
- **PDF p. 10 / printed p. 746:** References only.

**Decision:** preserve raw learner text as the primary observation and run a
paired raw/corrected sensitivity analysis. Report changes in candidate recall,
span/category decisions, sense resolution, unmatched mass, and coverage. Never
silently replace learner production with corrected text. Because the study uses
an older parser and general dependencies, measure the current pipeline directly
rather than importing its error rates.

### Kochmar et al. (2020): *Detecting MWE Type Helps Lexical Complexity Assessment* — 10 pages

- **PDF p. 1 / printed p. 4426:** Re-annotates 4,732 multi-token selections from
  CWI 2018 by MWE status/type. The central argument is that a phrase such as a
  compound must be assessed as a unit; 13–14% of the original lexemes were
  multi-token selections.
- **PDF p. 2 / printed p. 4427:** Distinguishes lexicalized,
  institutionalized, and weak/statistical combinations, and asks whether a span
  is complex as a whole and should be simplified as a whole. Collocations are
  deliberately excluded for this task, showing that MWE scope is purpose-bound.
- **PDF p. 3 / printed p. 4428:** Explains that original “phrases” were not MWE
  annotations. Three expert authors adapted a 13-category scheme, adding “not
  MWE” and “contains MWE,” merging phrasal-verb categories, and dropping types
  absent from the genres. Taxonomy is an explicit modeling decision.
- **PDF p. 4 / printed p. 4429:** Defines named entities, compounds, phrasal
  verbs, verb-preposition units, verb-noun units, support verbs, PP modifiers,
  coordination, connectives, semi-fixed VPs, fixed phrases, and both negative
  categories, each with task-specific simplification consequences.
- **PDF p. 5 / printed p. 4430:** Reports substantial agreement on the first
  1,000 jointly annotated items; the remaining 3,732 were single-annotator
  chunks with consistency checks. Fully 46.09% were “not MWE,” or 55.30% when
  “contains MWE” spans are included. Candidate span is therefore not MWE truth.
- **PDF p. 6 / printed p. 4431:** Category counts are highly imbalanced (1,272
  compounds, 119 phrasal verbs, only seven support verbs). Modeling assumes an
  oracle has already identified an MWE and uses 2,551 positive MWEs; free-text
  identification is explicitly deferred.
- **PDF p. 7 / printed p. 4432:** MWE type is the strongest ablation feature in
  five-fold evaluation: MAE rises from 0.0577 to 0.0673 when removed. The model
  beats a simple baseline on News and Wikipedia but not WikiNews, whose labels
  are strongly skewed.
- **PDF p. 8 / printed p. 4433:** Native and non-native judgments differ.
  Frequency and length aid the non-native model but not the best native model;
  verbal constructions are especially difficult for non-native readers.
- **PDF p. 9 / printed p. 4434:** Concludes that type improves probabilistic
  complexity estimation, while explicitly acknowledging that neither free-text
  MWE identification nor type detection was solved. Retained duplicates and
  random cross-validation also warrant a future type/context-disjoint check.
- **PDF p. 10 / printed p. 4435:** References only.

**Decision:** retain `candidate`, `occurrence`, `category`, `idiomaticity`,
`sense`, and `difficulty/coverage` as different variables. Add MWE-category
strata to evaluation, not to a premature universal score. Do not cite this work
as evidence that automatic detection is solved.

### Li and Gaillat (2020): *Automatic detection of unexpected/erroneous collocations in learner corpus* — 6 pages

- **PDF p. 1 / printed p. 101:** Defines collocations as one subset of MWEs and
  limits the experiment to verb–noun combinations. It treats several labels for
  learner collocational error as interchangeable, a simplification that the
  present project should not inherit without annotation evidence.
- **PDF p. 2 / printed p. 102:** Implements “extract from learner corpus, then
  subtract a native-corpus reference list.” PARSEME light-verb constructions
  evaluate extraction, BNC supplies a standard list, and NUCLE error tags
  evaluate unexpected combinations.
- **PDF p. 3 / printed p. 103:** The extraction module reaches only 0.08 best F1;
  a 200-item sample of the BNC list has precision 0.57. The supposed standard
  and erroneous lists overlap. On 1,471 NUCLE errors, recall/precision trade off
  sharply across log-likelihood thresholds.
- **PDF p. 4 / printed p. 104:** Extracting all 54,471 candidates yields recall
  0.83 but precision 0.02; the best reported F1/F0.5 region is around 0.04–0.05.
  The authors identify biased light-verb gold data, a tiny 942-item reference,
  and unevaluated POS/lemmatization as major causes.
- **PDF p. 5 / printed p. 105:** References document learner-collocation error,
  extraction, and association-measure foundations.
- **PDF p. 6 / printed p. 106:** References only.

**Decision:** explicitly reject the rule “not in a native reference list =
learner error.” Absence is an unresolved reference outcome. If collocational
error becomes a target, it needs its own learner-error annotation and precision/
recall evaluation; it cannot be inferred from low frequency or non-membership.

### Lee and Uvaliyev (2023): *Automatic Generation of Vocabulary Lists with Multiword Expressions* — 6 pages

- **PDF p. 1 / printed p. 81:** Frames graded vocabulary lists as an acquisition
  sequence and includes MWEs because component-wise knowledge may not provide
  the expression's interpretation. EFLLex is the closest earlier resource; its
  MWEs had not been evaluated separately.
- **PDF p. 2 / printed p. 82:** Uses graded training corpora and a CEFR-labeled
  test corpus. The key coverage rule treats an unlearned gold MWE as unknown even
  if all component words are learned. “Understood” is operationalized as more
  than 90% known eligible words, not observed comprehension.
- **PDF p. 3 / printed p. 83:** Builds a mixed gold set of 5,722 bigram/trigram
  MWEs from EVP, GSE, and compositionality datasets. Measures simulated study
  time and mean count of texts above threshold. All candidates are lemmatized;
  discontinuity, context, and sense are outside the representation.
- **PDF p. 4 / printed p. 84:** The best automatic method uses the top 75% by a
  semantic-compositionality filter plus dispersion, but expert EVP/GSE lists are
  substantially better. Results vary by proficiency level; one extraction/rank
  rule is not uniformly optimal.
- **PDF p. 5 / printed p. 85:** Limitations are MWEs no longer than three words,
  absent POS information, and incomplete gold coverage. References begin.
- **PDF p. 6 / printed p. 86:** References only.

**Decision:** this paper supplies a useful counterfactual baseline: compute word
coverage and an MWE-unit channel separately, then show the difference under an
explicit rule. Do not call the result comprehension, vocabulary knowledge, or
learning gain without human evidence. Our app must also expose the denominator,
eligible tokens, reference, unit, overlap policy, and unresolved mass.

### Hu, Lu, and Hu (2025): fine-grained sense-aware lexical sophistication — 15 pages

- **PDF p. 1:** Motivates sense-aware measurement because the same word form can
  realize CEFR-different senses. On 1,236 FCE scripts, three new indices explain
  11.8% of holistic-score variance and complement existing indices.
- **PDF p. 2:** Contrasts frequency-band/mean-frequency approaches with
  multidimensional lexical sophistication and identifies TAALES as a broad
  comparator. The earlier sense method used only a single frequency threshold.
- **PDF p. 3:** Describes BERT-based contextual sense vectors in the 2022 method
  and motivates EVP's six-level, sense-specific alternative. EVP assignments
  draw on learner and native corpora plus lists, so they are not pure frequency.
- **PDF p. 4:** Uses 1,236 upper-intermediate FCE exam scripts. The retrieved EVP
  material has 7,393 headwords, 2,446 polysemous/homonymous headwords, 7,229
  senses, 14,076 dictionary examples, and 6,655 learner examples.
- **PDF p. 5:** Represents each EVP sense by averaging BERT contextual vectors
  over examples. Because 45.2% of senses have one example, the authors augment
  selected weak senses with automatically aligned OED Online examples. This
  also introduces cross-dictionary sense-alignment risk.
- **PDF p. 6:** On clean EVP learner examples, augmented WSD reaches 87.8% sense
  and 92.7% CEFR accuracy without POS. On 200 FCE instances, nine are uncertain;
  among 191 resolved cases, accuracy is 80.1%/85.3%. Automatic POS slightly
  degrades performance, so a dependency/POS stage is not automatically helpful.
- **PDF p. 7:** Defines moving-window token ratios by CEFR level, using a
  100-token window chosen after sensitivity inspection. Window size remains a
  user option and a researcher degree of freedom that must be disclosed.
- **PDF p. 8:** Adds type ratios and mean CEFR scores. The main `lazyA1` mode
  overrides WSD for any word whose lowest EVP level is A1 because frequent words
  were often misclassified. It compares 26 new indices with 484 TAALES indices
  and six earlier sense-aware indices using filtering and stepwise regression.
- **PDF p. 9:** The strongest TAALES correlation is |r|=.218; a nine-predictor
  stepwise model explains 12.1%. The earlier sense-aware type ratio correlates
  at .288 and explains 8.3%. Four new measures correlate more strongly than any
  of the 484 TAALES measures in this dataset.
- **PDF p. 10:** Three new predictors explain 11.8%; a nine-predictor combined
  model explains 17.4%. These are same-sample association models, not held-out
  prediction estimates, and extensive feature screening/stepwise selection can
  make generalization look better than it is.
- **PDF p. 11:** The combined model mixes new CEFR-sense, earlier sense-aware,
  n-gram, association, and psycholinguistic indices. The result supports
  complementarity, not replacement of all word-level evidence by WSD.
- **PDF p. 12:** CEFR-based type/token indices correlate more strongly with the
  FCE scores than selected frequency/familiarity comparators. This establishes
  criterion-related evidence in one corpus, not that CEFR level is an objective
  universal difficulty scale.
- **PDF p. 13:** WSD modes generally beat random/POS-only alternatives, but the
  `lazyA1` heuristic performs best on this dataset. The authors warn that the
  ordering may change across proficiency levels and text types and expose modes
  in their tool.
- **PDF p. 14:** Most important for this project: performance is worse on real
  learner text because of errors, missing EVP senses, and limited/ambiguous
  context. On 600 ELLIPSE sentences, humans leave 118 uncertain; on the remaining
  482, WSD/CEFR accuracy is 77.6%/82.8%. Future work explicitly calls for phrase
  identification, learner-adapted WSD, and preprocessing/correction.
- **PDF p. 15:** References and publisher notice. The paper points to code, but
  EVP/OED access and reuse remain separate rights questions; method openness
  does not make the lexical data openly redistributable.

**Decision:** contextual sense is not optional if the claim concerns the sense
of `take in`, but it remains a separate, uncertainty-bearing channel. Evaluate
automatic WSD on learner data with an explicit `uncertain/out-of-inventory`
state, report both all-target coverage and accuracy on the resolvable subset,
and compare raw/corrected text. Do not bundle EVP-derived sense/CEFR data without
permission. BERT is a candidate baseline only after the human-reviewed contract
and benchmark establish that it improves the target outcome.

## Cross-study synthesis: what changes now

| Live question | Evidence-backed answer | Required project action |
|---|---|---|
| Is a generic web MWU highlighter novel? | No. Eguchi already documents list-conditioned n-gram/dependency profiling with highlighted text and item tables. | Keep the contribution at auditable occurrence/sense-aware coverage, not highlighting. |
| Can dependency parsing be assumed to handle learner text and `take it in`? | No. Eguchi demonstrates dislocated verb–object collocations, not that VPC case; Berzak shows locally large learner-error effects on dependencies. | Benchmark continuous/separated VPCs and raw/corrected learner text; preserve human review and abstention. |
| Is every extracted phrase an MWE? | No. More than half of Kochmar et al.'s selected spans were not whole-span MWEs once “contains MWE” is included. | Score candidate generation and occurrence/category decisions separately. |
| Can an unmatched learner combination be called erroneous? | No. Li and Gaillat's subtraction approach has extremely low precision/F1 and a noisy reference. | Label it `unresolved/not in this reference`, never `error` by default. |
| Should MWE coverage be separate from component-word coverage? | Yes as an explicit analytical counterfactual; Lee and Uvaliyev formalize exactly that distinction. | Report separate channels and their delta; do not average them or infer actual comprehension. |
| Does polysemy matter for lexical measurement? | Yes. Hu et al. find added criterion-related evidence from contextual CEFR-sense information. | Keep sense assignment separate from form membership, with uncertainty and inventory coverage. |
| Should learner text be silently corrected before analysis? | No. Correction can improve processing, but changes the observation. | Raw is primary; corrected is a paired sensitivity condition with a full change log. |
| Should BERT/LLMs be added now? | Not yet. WSD helps but remains imperfect on real learner text; phrases and rights remain unresolved. | First create adjudicated learner benchmarks; add the smallest model baseline only if it beats transparent baselines on prespecified outcomes. |

## Revised empirical critical path

1. Freeze the construct statement: reference-conditioned word, MWE-form, and
   MWE-sense coverage are separate descriptive outcomes; none directly measures
   knowledge, comprehension, correctness, or overall proficiency.
2. Create a small, double-reviewed ICNALE GRA raw/corrected audit sample with
   VPC candidate spans, gaps, occurrence status, category, idiomaticity, sense
   state, error location/type, and reviewer confidence. Keep corpus text local.
3. Evaluate the current transparent candidate baseline by continuous versus
   discontinuous form, learner-error stratum, and raw versus corrected version.
   Report exact-span and relaxed member scores plus abstention/unresolved rates.
4. Quantify measurement consequences: word-only result, added MWE-form channel,
   added reviewed-sense channel, overlap policy, and sensitivity to reference and
   correction. Never turn the channels into one score merely for convenience.
5. Only then compare a current dependency parser and one contextual-embedding
   baseline. Promotion requires a material improvement on a genuinely held-out
   slice without hiding subgroup failures or license/runtime costs.
6. Conduct task-based usability testing with L2 vocabulary researchers and
   teachers: can they identify the unit/reference/denominator, resolve a case,
   interpret uncertainty, and avoid the prohibited inferences?

This ordering is intentionally conservative. The literature does not justify
more features; it justifies a sharper construct, learner-error sensitivity,
human-reviewed gold data, and explicit uncertainty before automation.
