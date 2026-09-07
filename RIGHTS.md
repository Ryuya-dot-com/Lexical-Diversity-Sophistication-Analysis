# Rights and provenance register

Status: evidence review for the independent static probe, 2026-09-05

This register distinguishes tool code, method descriptions, lexical resources,
derived tables, and example texts. Availability, free download, academic use,
and open redistribution are not synonyms. Each admitted artifact needs its own
record. The decisions below are conservative project gates, not legal advice.

## Active release tree

### Public MWE examples added locally — 2026-09-07

`samples.json` 0.4.0 adds three existing project-authored M3–M5 texts and two
verbatim Tatoeba English sentences, IDs **11202318** and **9004040**, from the
[official CC0-only export](https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences_CC0.tsv.bz2).
The [download documentation](https://tatoeba.org/en/downloads) distinguishes
CC0 sentences from the default CC BY corpus and specifies the four exported
fields. Only the selected sentence texts use
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/); this does not
relicense other Tatoeba text, translations, audio, or project-authored material.
The archive retrieved on 2026-09-07 is 1,288,331 bytes with SHA-256
`489556f5ed662d97f1350ef81aa4b0fc430ea32c0c98853020666b055ee4b40c`.
Each selected row retains its original sentence URL, source modification time,
license and exact UTF-8 text hash. The full archive is not bundled or fetched
by the browser. CC0 does not warrant authorship or remove third-party rights.

These are deliberately chosen, exposed development examples, not a random
corpus, natural discourse collection, independent labels or a sealed test.
The project-authored prompts describe review exercises, not upstream judgments.
Loading an example copies text only with the starter patterns; no occurrence,
idiomaticity or contextual-sense answer is supplied. Existing M3–M5 fixture
decisions are not loaded. Selection does not attest processing permission or
choose a word profile. Public text availability does not validate linguistic
decisions. Attribution-required external paragraphs are not added in this
iteration; preserving their attribution through every export remains needed
before such integration.

| Item | Origin | Runtime use | Current decision |
|---|---|---|---|
| `index.html`, contracts, annotation/training/platform guides, `annotations/training_cases.json`, `annotations/hard_case_bank.json`, `scripts/convert_annotation_export.py`, and tests | Original project code, documentation, and synthetic training/format records | Static browser app, browser-local MWE review, independent guide/training reading, external-platform export conversion, and verification | Code, annotation guide, cases, converter, and tests are dual-licensed MIT or CC BY 4.0 at the recipient's choice; protocol documents are CC BY 4.0. The starter patterns, M1–M5 contexts, practice/hard cases, and embedded CAS fixture are project-authored functional examples, not copied lexical-resource entries. No human response, qualification form, natural benchmark item, third-party runtime code, or copied guideline example is included. |
| Scenarios and examples in `samples.json`, and MWE cases in `tests/fixtures/mwe_cases.json` | Project-authored synthetic transformations and `take in`/`spill the beans` contract cases; two separately identified Tatoeba CC0 sentence texts | Browser comparisons, editable MWE examples, and contract verification | Project-authored material remains MIT or CC BY 4.0; the two Tatoeba texts are CC0 as documented above. M3's fixture assignments are project decisions, not OEWN gold, and are not loaded into the review UI. No participant response or learner corpus is included. |
| The benchmark section of `metric_contract.json`, evaluation/bootstrap/precision scripts and tests, `resources/precision_plan.json`, and the surface-list prediction fixture | Original project contract/code, synthetic metric contributions and precision resamples, and synthetic negative-control predictions | Offline supplied-candidate compatibility; open-text task point estimates; fixed-seed document-cluster intervals, canonical-type sensitivity, paired system differences, and fail-closed pre-data allocation simulation | Dual-licensed MIT or CC BY 4.0 for code/tests and CC BY 4.0 for the precision plan; no source row, natural test item, observed pilot value, final sample size, model, weights, training corpus, third-party code, or third-party Python package is included. Synthetic checks establish software behavior only. |
| `benchmarks/streusle_v5_vpc_vid.json`, `resources/streusle_gap_dependency_baseline.json`, `scripts/check_streusle_v5.py`, and `resources/STREUSLE_NOTICE.md` | Project-authored external benchmark profile, frozen aggregate baseline record, checker, and attribution/rights notice based on pinned STREUSLE 5.0 metadata and annotations | Offline artifact verification and transparent VPC/VID baselines only; no corpus or upstream code is bundled or loaded by the Web app | Original checker and notice are dual-licensed MIT or CC BY 4.0. The profile and aggregate result record preserve STREUSLE CC BY-SA 4.0 and source-text permission boundaries; researchers obtain the exact release separately. |
| `mwe_contract.json`, matchers, and coverage summarizers | Original project schema and deterministic validation/review/coverage logic | Exposed through the public UI for explicit TUBELEX/NGSL/bounded local BNC/COCA word-profile selection and separate OEWN MWE-form review; not a validated automatic MWE analyzer or combined lexical score | Dual-licensed MIT or CC BY 4.0; the schema declares the separately licensed profiles below. |
| `reference_profile_template.json` | Original project manifest template | Defines the evidence required for one resource projection and one word/MWE-form/MWE-sense coverage channel; not a resource, uploader, or runtime profile | Dual-licensed MIT or CC BY 4.0; null fields prevent the template from masquerading as an admitted resource. |
| `resources/hybrid_sense_inventory_contract_2026_09_03.json` | Original project sense-identity, source-mapping, uncertainty, lifecycle, and release rules | Frozen pre-annotation design for a future English VPC/VID inventory; it contains no lexical entries, dictionary wording, corpus text, or contextual labels and is not loaded by the Web app | CC BY 4.0. Future source-linked records must preserve their own controlling license and notices; the contract expressly does not relicense OEWN or Wiktionary material. |
| `resources/sense_mapping_queue.json`, `resources/sense_mapping_guide.md`, and `scripts/build_sense_mapping_queue.py` | Modified 146-type STREUSLE 5.0 `V.VID` label subset; bounded candidate entry/variant identifiers from pinned OEWN 2025 and the 2026-08-28 Kaikki extraction of the 2026-08-05 English Wiktionary dump; project-authored generator, opaque IDs, route states, and guide | Reproducible IR-130 nonexact candidate queue only; 3 types have closed candidate sets, 143 retain `unresolved/no_bounded_route`, and all 146 remain in the denominator. No source sentence, gloss, example, translation, contextual label, admitted sense, or Web-app runtime data is included | Queue and guide: CC BY-SA 4.0 plus the incorporated WordNet License and all three upstream notices; generator: project `LICENSE.md` choice. Raw OEWN/Kaikki files remain ignored. Kaikki links are withheld from formal inventory admission until the underlying dump hash and imported-content review are recorded; `unresolved` is not proof of a true inventory gap. |
| `resources/hybrid_sense_inventory_v1.json`, `resources/hybrid_sense_inventory.schema.json`, `scripts/build_hybrid_sense_inventory.py`, and `tests/test_sense_inventory.py` | Project-stable candidate ID reservations plus verb entries, sense keys, synsets, CILI/ILI links, glosses, examples, and synset-member relations projected from the pinned OEWN 2025 JSON release; project-authored schema, lifecycle relations, and registry checks | Reproducible IR-131/132/133 candidate seed for four VPC and five VID forms; 67 candidates are fingerprinted. Draft 2020-12 structure, cross-artifact ID uniqueness, source-sense uniqueness, and update preservation are checked; no candidate is an admitted project sense, contextual label, corpus occurrence, or Web-app runtime record | Inventory: OEWN CC BY 4.0 plus the incorporated WordNet License and retained notice; schema: CC BY 4.0; generator/tests: project `LICENSE.md` choice. Source wording and examples are marked verbatim. Synset members remain source relations, while `supersedes`, `split_from`, `merged_from`, and `related_to` are empty until a reviewed lifecycle event. The raw release archive remains ignored; independent review and adjudication are required before admission. |
| `resources/inventory_review_protocol.json` and `scripts/check_inventory_reviews.py` | Project-authored pre-review polysemy audit, blank-template generator, validator, and aggregate reporter; the frozen input is the separately licensed candidate inventory above | Recomputes source multiplicity, family imbalance, comparison burden, source-evidence sufficiency, and absence of context before preparing two 9-form/67-candidate reviews. It separates pinned-source coverage, form relation, construction scope, project-sense clustering, and later contextual assignment; no human review is included | Protocol: CC BY 4.0; script: project `LICENSE.md` choice. Completed reviews, reviewer-code keys, agreements, and access logs are restricted until their work-product or consent basis and disclosure review permit release. They must not enter Git, GitHub Pages, an API response, or this Dropbox workspace. |
| `resources/inventory_governance.md` and `tests/fixtures/sense_inventory_versions/lifecycle_exercise.json` | Project-authored procedure and wholly synthetic identities, meanings, sources, annotations, lifecycle events, and approval facts | IR-134 protocol exercise for non-destructive split, merge, source deprecation, new OOI-prompted sense, migration status, and post-test version branching; no file is loaded by the Web app | Governance procedure: CC BY 4.0; fixture: project `LICENSE.md` choice. No natural language source, dictionary record, participant data, real annotation, semantic decision, test result, or third-party material is included. Synthetic acceptance demonstrates software/governance behavior only. |
| `resources/hybrid_inventory_coverage_v2.json`, `scripts/audit_hybrid_inventory_coverage.py`, and `tests/test_inventory_coverage.py` | Aggregate counts derived from the pinned STREUSLE 5.0 VPC/VID annotations, the public OEWN/Kaikki audits, and the project candidate inventory; project-authored standard-library audit and test | IR-135 full-denominator audit of 624 target occurrences/389 types and the fixed 52-occurrence/14-type VID pilot; reports candidate availability separately from zero admitted/contextually assessed coverage and holds all sense claims | Audit: CC BY-SA 4.0 plus the incorporated WordNet License and retained STREUSLE, Wiktionary/Kaikki, and OEWN notices; script/test: project `LICENSE.md` choice. It contains no sentence, token, occurrence, dictionary, participant, human-label, prediction, or score row. Aggregate candidate availability is not semantic adequacy or performance evidence. |
| `resources/inventory_population_log.json` and `scripts/build_inventory_population_log.py` | Project-authored fixed-stratum selection and aggregate counts from the pinned STREUSLE 5.0 train `V.VID` annotations, plus bounded OEWN/Kaikki route identifiers and the prior IR-130 queue | Reproducible IR-132 pilot of 14 VID types spanning frequency, polysemy candidates, discontinuity, exact/slot/nonexact/no-route cases, and source-identity constraints. It contains no sentence/token text, dictionary wording, participant data, contextual label, or admitted sense | Log: CC BY-SA 4.0 plus the incorporated WordNet License and STREUSLE, Wiktionary/Kaikki, and OEWN notices; generator: project `LICENSE.md` choice. Four Kaikki routes remain withheld from formal admission pending underlying-dump identity/imported-content review; two no-route types remain unresolved. The local STREUSLE checkout and dictionary artifacts stay ignored. |
| `resources/benchmark_source_decision_2026_09_04.json`, `BENCHMARK_CARD.md`, `DATA_STATEMENT.md`, and the prior-draft pointer | Project-authored source/release protocol and pre-data documentation based on official Wikimedia terms and dump documentation; no Wikipedia text, media, annotation, or contributor data | Freezes English Wikipedia namespace-0 article revisions as the new core source and distinguishes source, sampling, annotation, target, and evaluation populations before acquisition or target search | Protocol documents are CC BY 4.0. Any future source-derived text/annotation layer must use CC BY-SA 4.0, preserve page/revision/history attribution and imported-text notices, identify modifications, exclude non-text media, and pass page-level review. The current files do not grant rights to or release a benchmark. |
| `resources/release_layer_manifest.json` | Project-authored first-match license/notice rules for the current public tree and gated future benchmark layers | Assigns every current public file a source, controlling license expression, notice, and redistribution state; separates source text, annotation, inventory, code, model, and documentation | CC BY 4.0. TUBELEX remains BSD-3-Clause; NGSL remains CC BY-SA 4.0; OEWN projections retain CC BY 4.0 plus the WordNet License; named CC-BY-only protocols remain CC BY 4.0; other original project files retain the `LICENSE.md` choice. Unknown-rights files and unreviewed future layers are excluded. |
| `GOVERNANCE.md` and `resources/ethics_determination.md` | Project-authored controls based on linked official institutional and privacy guidance; no institutional form or participant record is copied | Separates current no-human work, later annotation work-management controls, and human-participant or secondary-use research that may require institutional review | Dual-licensed MIT or CC BY 4.0 as project documentation. It is not legal advice, institutional approval, a work agreement, or permission to collect or release restricted records. |
| `resources/source_manifest.json`, `resources/preprocessing_contract.json`, `scripts/reconstruct_benchmark.py`, and their tests/fixture | Project-authored frozen Wikimedia dump metadata, preprocessing/reconstruction protocol, standard-library checker, tests, and synthetic prose; no Wikipedia source or annotation is present | Pins the completed dated source descriptor and demonstrates stable document/token/occurrence IDs, exact character/UTF-8 byte traces, discontinuous gaps, and fail-closed mismatch behavior | The manifests are CC BY 4.0; code, tests, and fixture use the project `LICENSE.md` choice. These files neither obtain nor license Wikipedia content and cannot support a benchmark-availability claim. |
| `resources/sampling_frame.json`, `resources/planning_pilot_addendum.json`, `scripts/sample_benchmark_documents.py`, and their test/synthetic fixture | Project-authored target-blind sampling and planning-pilot protocols, standard-library queue builder, tests, and synthetic metadata; no Wikipedia prose, MWE field, annotation, contributor profile, or outcome is present | Freezes content-neutral eligibility, document hierarchy, three length strata, deterministic random priority, and same-stratum replacement; separately permits one preallocated target-blind planning prefix after training-pilot and guide freeze, permanently outside the sealed test | The protocols are CC BY 4.0; code, tests, and fixture use the project `LICENSE.md` choice. The addendum does not authorize human work or supply N_h, pilot size, selected rows, or evidence. Future source rows and selected text remain separately gated and are not licensed or released by these files. |
| `resources/evaluation_strata.json` | Project-authored pre-data evaluation protocol; no source row, human label, system prediction, or result is present | Freezes single-axis reporting strata, claim denominators, design weighting, document/canonical-form dependence, and the rule that underpowered strata remain descriptive | CC BY 4.0. It references the separately versioned benchmark section without changing the browser metric/export version, supplying a benchmark result, or granting rights to future source or annotation layers. |
| `resources/split_protocol.json` and `resources/leakage_ledger.json` | Project-authored pre-data assignment, custody, and exposure metadata; no source text, human label, sealed membership, prediction, credential, or participant record is present | Freezes document-disjoint split roles and records known external gold, result, and dictionary exposure without representing it as a new blinded test | CC BY 4.0. These records do not redistribute the cited corpora or dictionaries, appoint a custodian, authorize human work, or establish held-out evidence. |
| `resources/tubelex_en_regex_ascii_2025.json` and `resources/TUBELEX_LICENSE.txt` | Project-derived 410,400-form projection of the pinned TUBELEX English regex frequency table and retained upstream license | Browser-local word-token/type coverage, source count, per-million frequency, rank, and unmatched-item output | TUBELEX BSD-3-Clause, including copyright notice, conditions, disclaimer, source identity, method citation, projection rules, and no-endorsement restriction. Not covered by the project's dual-license grant. |
| `resources/ngsl_1_2_ascii_forms.json` and `resources/NGSL_NOTICE.md` | Project-derived 10,114-form projection of the pinned official NGSL 1.2 statistics and research-form files, with attribution and modification notice | Browser-local first-1,000/2,000/full NGSL head-rank coverage; retains five ambiguous multi-head surface forms and distinguishes `beyond_cutoff` from `unmatched` | NGSL CC BY-SA 4.0. Attribution, ShareAlike, source hashes, modifications, construct limits, and no-Nation-level substitution travel with the projection. Not covered by the project's dual-license grant. |
| `resources/oewn_2025_multiword_verbs.json`, `resources/oewn_take_in_2025.json`, and `resources/OEWN_WORDNET_NOTICE.txt` | Project-derived projections of the pinned Open English WordNet 2025 JSON release and retained upstream notice | Browser-local exact membership for 2,847 multiword verb forms; separate complete 17-sense candidate inventory for human `take in` review, export, and fixture validation | OEWN CC BY 4.0 plus the underlying WordNet License. Attribution, source identity, modifications, citation, license text, and no-endorsement notice travel with both projections. Not covered by the project's dual-license grant. |
| `scripts/build_reference_profiles.py`, `scripts/build_ngsl_profile.py`, and `scripts/build_bnc_coca_profile.py` | Original project code | Deterministically reproduces the TUBELEX/OEWN and NGSL browser profiles and the local-only BNC/COCA first-2K profile from separately downloaded, hash-verified source assets | Dual-licensed MIT or CC BY 4.0; standard library only and no upstream code copied. The BNC/COCA builder never executes the legacy program. |
| `scripts/build_voa_material_frame.py`, `scripts/screen_voa_article_sources.py`, `scripts/profile_voa_material_candidates.py`, and their seven `resources/voa_gate1_*` JSON records | Original standard-library code and project-derived dates, titles, canonical URLs, credit classifications, source/text hashes, archive-artifact metadata, aggregate NGSL descriptors, short OEWN/STREUSLE-form leads, and preliminary desk decisions from official VOA pages | Offline Gate 1 target-blind ordering, source/prose-boundary eligibility, prioritization, five-article desk review, and a bounded non-OEWN audit of the other 19 eligible articles; no file is loaded by the Web app | Code is dual-licensed MIT or CC BY 4.0. The records contain no article/STREUSLE prose, media, or learner data and do not assert gold VOA MWE labels or passage validity. The frozen VOA frame is stopped without admission; preliminary occurrence decisions still await author confirmation. Archive/article HTML, STREUSLE data, and the local BNC/COCA overlay are not committed. |
| `resources/simplewiki_gate1_route2_design.json`, the six `resources/simplewiki_gate1_route2_*` ledgers, `scripts/screen_simplewiki_route2.py`, and `scripts/screen_simplewiki_route2_rendered.py` | Original project sampling contract/code plus official Wikimedia dump/API identities, page/revision metadata and hashes, lead/member counts, desk decisions, exclusions, ranks, draft project-authored items, aggregate evidence from the already pinned STREUSLE, OEWN, NGSL, and local BNC/COCA resources, and a project-authored content-neutral amendment | Preserves the target-conditioned Gate 1 source, constraints, 16,375-row candidate queue, rendered-boundary screen, `take in`/`pick up`/`give up` desk records, and the stop before `come out`; not loaded by the Web app | Project-authored contract/code, desk labels, amendment, and draft items are dual-licensed MIT or CC BY 4.0; cited OEWN identifiers retain upstream terms. Public ledgers contain titles/IDs, positions, span hashes, reason codes, and derived metadata but no Wikipedia prose, surface spans, HTML, media, or contributor data. The dump, 508 cached API responses, and BNC/COCA profile stay ignored and local. Recorded provisional page routes use CC BY-SA 4.0 with permanent revision/history links and extraction notices; `School bus` additionally credits the `Types of buses` source history. No counterfactual replacement page or final text is released. |
| `resources/teco_v1_1_candidate_manifest.json` and `resources/downstream_selection_memo.md` | Project-authored prose-free records of TECO's official OSF metadata, file identities, downloaded-file hash checks, aggregate join audit, and the decision not to select a downstream application for the first paper | Pins TECO's optional role and construct/rights limits; no corpus row is loaded by the Web app, and author correspondence is not a core-development gate | Dual-licensed MIT or CC BY 4.0 as project metadata. They contain no participant row, stimulus text, eye measure, or Eiken item and do not sublicense TECO or its underlying materials. |
| `scripts/screen_teco_mwes.py` and `resources/teco_v1_1_mwe_candidate_screen.json` | Original standard-library code plus a project-derived screen of OEWN canonical forms, TECO text/item positions, line-edge flags, and unreviewed states | Creates an outcome-blind desk-review queue and freezes the word-member/ROI boundary; neither file is loaded by the Web app | Code and project-authored metadata are dual-licensed MIT or CC BY 4.0; OEWN canonical forms retain OEWN/WordNet terms. The public screen contains no TECO passage/surface token, participant row, eye measure, answer, proficiency, or comprehension value and does not sublicense Eiken material. |
| Researcher-supplied BNC/COCA first-2K profile | Locally generated from the exact official v1.0.0 zip; neither source nor projection is committed | Hash-verified browser-memory first-1K/2K Level 6 word-family coverage; runtime file hash is exported | Local use route only. The app requires the reviewed 366,120-byte projection and SHA-256 `ebd06548187988eb1a61ab967cc39c01461023043ee7aef427606e5bf508f138`; public redistribution remains gated by the unresolved artifact-specific license mapping. |
| Researcher-entered text and MWE patterns | Researcher-authorized synthetic, published, teaching, or appropriately governed research material | Browser-memory calculation, candidate review, and explicit local single/document-set workspace save/restore | Not bundled, transmitted, autosaved, or copied into method JSON. User-requested workspace JSON contains raw text and pattern TSV; the checkbox records authorization/ethics attestation but is not a legal or ethics determination by the app. |
| Exported method/CSV records | Project schema plus researcher labels, provenance, hashes, client-clock time, word types, and reviewed MWE rows | Explicit local CSV or metadata JSON download | Raw text and pattern TSV are omitted from method JSON, but CSV word types, canonical forms, and decision notes may be sensitive or partially reconstructive. Editable files, hashes, and timestamps are not signatures or proof of authorship/time. |
| Exported MWE workspace and document-set records | Project resume schemas plus names/IDs, raw source text, source-text SHA-256, pattern TSV, review rows, decision notes, and runtime-resource identities | Explicit local JSON download and all-or-nothing same-contract browser re-import; a set contains 1–20 independently validated documents and is not pooled | Contains directly sensitive and potentially identifying research content. It is not a publication export, is never transmitted or browser-stored by the app, and must be governed and reviewed before sharing. Hashes detect changed bytes but do not prove authorship or trusted time. |
| Other lexical lists, corpora, models, dictionaries | None additionally bundled | None | Not admitted. The source BNC/COCA package and generated profile remain outside the release even though the exact local import route is implemented. |
| Browser platform | User agent | Rendering and local calculation | No installed package or third-party script. |
| Python and Node.js | Local/CI environment | Tests, offline resource/benchmark verification, and optional static serving only | Not shipped as application dependencies. |
| Method citations | Bibliographic metadata and DOI links | Interpretation evidence only | Attributed in the metric contract and export; no third-party code, data, or article text is copied. |

The archived MWE/VPC roadmap is an evidence inventory, not a release input.
Parent-directory data, credentials, code, lexical resources, and research
records are not part of this repository.

## External resource evidence

| Candidate | Verified evidence | Rights/construct risk | Admission |
|---|---|---|---|
| TAALES | The official site and index guide document separate word, contiguous bigram/trigram, coverage, and POS-tagged polysemy indices; the tool is CC BY-NC-SA 4.0. The audited 2.8.1 copy forms all adjacent n-grams mechanically and looks up polysemy by word/POS rows. | A `take in` bigram value does not identify a VPC, recover separated `take ... in`, or assign a contextual sense. Sharing or adaptation must also satisfy NonCommercial/ShareAlike, and the tool notice does not establish rights to every bundled corpus/list. | Comparator and methodological prior art only; no code/data import or compatibility claim. |
| Multi-Word Units Profiler 2.0.1 | The live site labels the profiler CC BY-NC-SA 4.0 and offers four research-based lists. Eguchi's 2021 presentation documents Python/spaCy lemmatization and parsing, n-gram/dependency candidate extraction, list matching, highlighted text, and item tables. Project-authored probes confirmed both contiguous and dependency-separated matches while the M1-M4 `take in` strings remained unmarked. | The site-level license does not establish reusable licenses for each incorporated list, example, frequency, or corpus-derived field; no corresponding source/data release was located in this review. The hosted POST sends raw input to PythonAnywhere, and no retention guarantee is presented on the input page. Its list-driven matches are not contextual VPC or fine-sense gold labels. | Primary behavioral comparator and methodological/UI prior art only. Do not copy code, lists, examples, or frequency fields, automate the hosted service, or send protected research text without permission and a documented privacy basis. |
| [Kyle and Eguchi (2021) public analysis repository](https://github.com/kristopherkyle/dependency_bigrams_Kyle_Eguchi_2021) | The public repository contains R Markdown, rendered HTML, and a 480-row derived table of file IDs, holistic scores, word counts, and aggregate word/bigram/dependency measures. | No source essays or MWE occurrence/sense labels are present; the R Markdown references an absent refined CSV; no explicit repository license was located. A writing-quality score is not MWE truth, learner MWE knowledge, or reading comprehension. | Method and document-level comparator only. Do not bundle the table/code or infer rights to the underlying TOEFL essays; review corpus terms separately and create new governed VPC/VID annotations before any BERT evaluation. |
| Lextutor Phrase Profiler 1.2 | The official page describes matching up to 30,000 words against selectable phrase/collocation lists; its Multiwords page distinguishes this from n-gram and MI-based extractors. | No explicit open redistribution license for the profiler payloads was found on the reviewed pages, and each incorporated list has separate rights and construct assumptions. Hosted input leaves the researcher's browser. | Secondary behavioral comparator only; do not copy its lists or make it a required reproducibility dependency. |
| COCA | The official download page sells word-frequency and 2–5-gram data and describes more than 40 million downloadable n-grams. | Purchase/offline processing does not state permission to expose the data through this public service. Hiding it in a database would not establish server-use, public-query, or derived-output rights. | Exclude unless written permission covers the exact artifact and delivery/output mode. |
| Open English WordNet | The official repository releases OEWN under CC BY 4.0. Its 2025 entry for `take in` has 17 verb senses, demonstrating that the MWE needs an inventory entry distinct from `take` and `in`. | Attribution and incorporated-material notices must travel with the exact pinned release. Inventory membership and sense count do not perform occurrence identification or contextual WSD, and automatic use must preserve ambiguity/abstention. | B-MWE1 admitted as a 2,847-form multiword-verb membership projection and a separate complete `take in#v` human-review projection; no full dictionary, frequency, automatic occurrence, or WSD claim. |
| English Wiktionary / Wiktextract / Kaikki | Wikimedia's current terms state CC BY-SA 4.0 and GFDL reuse routes for contributed text, and official dated English Wiktionary dumps are available. Wiktextract is MIT-licensed extraction software. The bounded audit pins the Kaikki-reported 2026-08-05 dump/2026-08-28 extraction and the combined hash of 206 locally cached type responses. Exact lookup adds 60 verb-entry routes and 99 raw senses. | The software license does not relicense extracted Wiktionary content. Only 5/99 raw senses have a Wiktionary `senseid`, and only one matched type has IDs for every lexicalized sense; none has a raw `id` or Wikidata ID. Attribution/history, ShareAlike/GFDL and imported-content conditions, stable IDs, extraction version, sense granularity, and derivative licensing remain relevant. Per-word URLs are mutable, and the full raw endpoint is deprecated. | Completed audit candidate, **not admitted as gold or runtime data**. Public output is aggregate-only; cached entries, glosses, examples, and target list remain ignored and local. Retain Wiktionary only as candidate evidence behind a future project-stable, versioned, separately licensed sense layer. |
| PHaVE List | Garnier and Schmitt's article defines 150 frequent phrasal verbs and key meaning senses covering at least 75% of their COCA occurrences. | This is the closest L2-pedagogical target, but the publisher labels the article restricted access and routes reuse of its non-OA supplemental lists to the copyright holder. COCA-derived percentages add a separate provenance question. | Candidate C-MWE2 for method/citation or written permission; do not copy the lists, glosses, examples, or percentages into the app. |
| STREUSLE | The official repository's 5.0 release (2025-11-15) provides more than 55,000 Web-review words, more than 3,000 MWE instances, supersenses across noun/verb/preposition expressions, recoverable gaps, and PARSEME-derived verbal categories; annotations are CC BY-SA 4.0. | It is a genre-specific lexical-semantic gold corpus, not a general English frequency distribution, literal-negative corpus, universal taxonomy, or OEWN-compatible fine-sense inventory. Its README distinguishes CC BY-SA annotations from source sentences/PTB annotations redistributed with Google/LDC permission. | B-MWE2 admitted as an external, non-bundled STREUSLE 5.0 VPC/VID offline benchmark profile. No corpus text, annotation rows, upstream code, or model enters the Web app or permissive core. |
| PARSEME guidelines | The official guidelines distinguish verbal idioms, light-verb constructions, inherently reflexive/adpositional verbs, multi-verb constructions, VPCs, and language-specific categories under CC BY 4.0. | The scheme is deliberately verbal and excludes many non-verbal idioms. Guidelines establish annotation decisions, not an English production detector, contextual idiomaticity scale, or fine-grained sense inventory. Corpus licenses must be checked per language/release. | Methodological source for VPC and future verbal-idiom contracts; do not use `VID` as a catch-all for non-verbal idioms. |
| PARSEME corpus/shared task 2.0 | The 2026 shared-task paper reports 17 languages, all five syntactic category families, ten identification systems including a baseline, and a new paraphrasing task. The fixed `st2.0-release-training-v1` tree contains 14 production language directories but no English directory; English occurs only in `subtask1_trial`. | The guidelines' license does not establish every corpus/model term, and a trial file is not an English production holdout. All-type multilingual performance is not English-VPC performance. | Current multilingual method frame and format trial only. Do not describe PARSEME 2.0 as this project's English production benchmark; use the pinned STREUSLE profile. |
| MAGPIE | Commit `7fa677b` publishes 56,622 BNC/PMB-based PIE instances, member offsets, five-way usage evidence, confidence, and random/type-disjoint splits under CC BY 4.0. | It tests supplied idiom targets rather than open-text recall, has no PARSEME VPC/VID category, and its usage classes are not dictionary fine senses. | Admit externally as a secondary type-disjoint idiomatic/literal benchmark only; do not bundle it or use it to validate fine-sense assignment. |
| SemEval-2022 Task 2 idiomaticity data/code | Commit `872625c` provides multilingual three-sentence contexts, binary idiomaticity data, paraphrase-similarity data, and GPL-3.0 evaluators. | It has no member offsets or VPC/VID categories. Expert paraphrases are exposed as similarity pairs rather than stable occurrence-level sense IDs, and final test gold is not released. | Method and secondary development evidence only; not the occurrence or contextual fine-sense benchmark. |
| MWEasWSD | Commit `5af8007` filters rule-generated candidates by WordNet 3.0 sense-versus-`NOT_AN_MWE` scores. The official SemCor 3.0 archive permits database use, copying, modification, and distribution with the retained Princeton notice; MWEasWSD's added layer is available under the repository-level AGPL-3.0. Exact manual/processed/CILI/OEWN/SemCor artifacts and hashes are pinned in the completed reuse audit. | Rights permit external analysis, but validity does not follow. The 1,159 first-kept labels have zero VPC/VID category fields, five conflicting duplicate keys, no independent annotation/adjudication evidence or uncertainty states, and a paper/artifact count mismatch. Only 7 verb-proxy forms/17 positive rows show observed sense contrasts; only 125/136 positive verb-proxy rows map losslessly to OEWN 2025 by exact ID plus ILI. `take_in` has one positive sense and four negatives. | Reject as contextual fine-sense validation gold. Retain only as an attributed external development/error-analysis comparator; do not bundle, relicense, acquire its model, or report a retrospective split as independent validation. |
| Raganato standard WSD framework, multiword-verb slice | The public project distributes a fixed zip of SemCor plus five Senseval/SemEval XML/gold sets. The exact 165,655,083-byte archive and internal files are hash-pinned; primary task papers document double annotation/resolution or adjudication for several source sets. | The exact zip has no LICENSE file or explicit redistribution grant. Source texts and procedures are heterogeneous. Complete MWE member spans are not reliable; STREUSLE category compatibility is only type-level. After lossless OEWN and candidate-polysemy filtering, only 23 VPC rows/18 types remain, with no VID or `take in` test row. | Admit only as an external conditional sense-ranking smoke test: SemCor training, six SemEval-2007 development rows, and 17 fixed Senseval-2/3 plus SemEval-2015 source-test rows already exposed during audit. Do not bundle or claim a blinded holdout, automatic detection, target-wide validity, ambiguity calibration, or unseen-form generalization. |
| English VMWE annotations (Kato et al.) | The paper reports 7,833 VMWE instances and 1,608 types, including discontinuous items, with literal/non-literal definitions plus `none` and `hard to judge` choices. The repository exposes indices and masked dependencies. | No repository license was found, and reconstruction depends on LDC OntoNotes/WSJ text. Its Wiktionary-era sense choices are not automatically OEWN-compatible. | Quarantine as methodological and evaluation prior art; do not redistribute or make it a required benchmark. |
| CoAM / CAIGen | CoAM reports 1.3K human-annotated, reviewed, consistency-checked all-type MWE sentences. Its CAIGen annotation interface is MIT-licensed and supports discontinuous/overlapping spans. | Interface code and corpus data are separate artifacts. The exact CoAM dataset license was not confirmed in this review; Google-based annotation also sends data outside the local browser. | Cite as an all-type stress-test and annotation precedent; quarantine the data and exclude CAIGen as a runtime dependency pending a demonstrated workflow need. |
| Project Gutenberg | Official terms direct bulk users to catalogs/mirrors rather than the human-facing site. Most book text is unrestricted under US copyright, but Project Gutenberg requires non-US users to verify local status. The frozen frame fixes 40 adult/unspecified plus 40 juvenile candidates. Ranks 1–30 produced 44 provenance-ready first units and ten mechanical passes: three adult/unspecified and seven juvenile. The final 20 metadata rows add 13 local-notice candidates (five adult/unspecified, eight juvenile), five likely-active terms, and two unresolved creator/death terms; no final-batch ebook was acquired. | A US determination does not establish Japanese or worldwide redistribution rights. Japan's named-author, anonymous/pseudonymous, old-law, non-revival, and wartime-addition rules are distinct. Front matter can add omitted contributors or source dependencies: `Going Some` names Paul Armstrong's underlying play contribution, and the `Mugby Junction` catalog omits four retained textual collaborators. The `Nat Ridley` work maps to Howard R. Garis and remains held. Transcriptions may differ from print editions, and the exact electronic artifact is the analysis version. Rights/boundary searches incidentally exposed target strings in frozen files, including 15188 and 23763 in the final screen; they cannot be treated as fully unseen outcome evidence. | Keep every source/unit text local, unbundled and unserved. Stop this frame unchanged before final-batch acquisition: only five adult/unspecified files can advance, so its ceiling is `3 + 5 = 8`, below the frozen ten-unit stop. Freeze a redesigned sampling rule before any further acquisition or MWE inspection, and declare public release scope before serving prose. |
| English Wikipedia core benchmark source | Official Wikimedia terms permit text reuse under CC BY-SA 4.0 with attribution, ShareAlike, imported-text notice preservation, change indication, and a license notice/link. Official dated `pages-articles` dumps provide page/revision metadata and complete content; the multistream index records offsets, page IDs, and titles. | A dump is not a blanket page-level clearance. Imported text may add attribution, fair-use and non-text media have different terms, `/latest/` is mutable, and prior Simple English Wikipedia work was target-conditioned. | Select only namespace-0 text from one completed dated dump. Before target search, exclude revisions with unresolved footer/history/talk-page notices. Release sampled text plus standoff annotations under CC BY-SA 4.0 with permanent revision/history URLs, exact IDs and hashes, and a fail-closed reconstruction route. No source has yet been acquired or admitted. |
| TECO v1.1 | The public OSF project is set to CC BY 4.0. The article describes the 30 passages as previously used in Eiken Tests, not as TECO-authored prose; its acknowledgement names JSPS funding but no Eiken permission. The current README lists the full passages but gives only disclaimers. The hash-verified 34-page `Reading Matarials.pdf` contains Eiken-labelled passages and questions but no copyright, permission, attribution, CC, or redistribution notice. The candidate manifest records the source-level evidence and nine file identities; the outcome-blind screen adds only 285 OEWN lead identities and positions. | Public availability and a project-level CC BY setting do not prove authority to license third-party prose. Eiken's current terms claim rights in past-test content and require permission for public copying/research use; those terms do not prove whether the TECO team received an earlier private permission. Candidate leads are not MWE truth; gaze and general proficiency do not establish occurrence-specific MWE knowledge. | Keep `Reading Matarials.pdf`, the proficiency test, questions/answers, and ordered `ia`/lemma or other passage-reconstructive sequences local. Publish only code, rights metadata, prose-free IDs/positions, and non-reconstructive derived results that separately pass participant-data review. Reconsider only on written evidence covering public/API redistribution, downstream reuse, transformation/information analysis, commercial or segregated terms, attribution, term, territory, and upstream rights. |
| MECO-L2 and CELER | Primary papers describe publicly available L2 eye-movement data with proficiency and comprehension-related variables: MECO-L2 uses 12 ACCUPLACER-derived passages; CELER uses WSJ sentences and provides its corpus repository. | Stimulus licenses, exact release terms, and variable completeness remain unaudited. Broad vocabulary/proficiency scores are not contextual word/MWE knowledge for each occurrence. | Not core or runtime dependencies. Compare them with TECO only after a separate downstream hypothesis passes IR-410 re-entry; no data import or redistribution before artifact-level review. |
| Santos et al. (2026) L2 idiom eye data | The Zenodo record applies CC BY 4.0 to a verified 140,609,151-byte archive of literal/figurative MWE sentence stimuli and raw/processed gaze data from Portuguese-L1 readers. | The paper omits N and claims A1–C2, while the archive contains 16 B1–C2 IDs; README group counts sum to 17; P08/P10 derived metrics are byte-identical. Source contexts and raw-to-derived provenance also need checking. | Quarantine pending author clarification or independent raw-data reproduction; do not use its derived metrics in a primary result. |
| FLAT / PARSEME FLAT | PARSEME identifies FLAT as its online annotation platform. FLAT is GPL-3.0 Web software with multi-user storage, permissions, provenance, confidence, token/span annotation, and document history; the reviewed PARSEME deployment reports FLAT 0.11.6 and requires login. | A software license does not grant access to the hosted PARSEME project or its documents. Forking its Django/CherryPy/FoLiA stack would add infrastructure without providing this project's coverage or sense estimands. | External annotation workflow and interoperability target only; no code, service, or data import. |
| INCEpTION | The official project releases the Web annotation platform under Apache-2.0; version 41.4 was released 2026-08-18. It supports configurable spans/relations and recommenders. | It is not MWE-specific, and its guide says discontinuous spans require relation/link emulation. Hosted services have their own access and privacy conditions. | Optional external annotation/adjudication workflow; no runtime dependency or embedding. |
| PyMUSAS | The official Apache-2.0 Python project provides rule-based, neural, and hybrid semantic taggers and reports MWE support for English. | It is a library rather than the target Web app; USAS semantic tagging is not OEWN fine-sense assignment, and code, models, rules, and upstream data require artifact-level review. | Candidate detector baseline only; benchmark before any component admission. |
| TUBELEX | The official repository publishes aggregate word-frequency and dispersion lists alongside a BSD-3-Clause license and states that full corpus text is not published. In a 2026-08-10 repository issue, the maintainer expressly confirmed that the published frequency lists are covered by BSD-3-Clause and may be redistributed, incorporated commercially, or reformatted under its conditions. The pinned English regex artifact was independently streamed and checked below. | YouTube-subtitle sampling, normalization, denominator, and upstream-content constraints remain part of the construct record even though the frequency-list redistribution question is resolved. It supplies word-frequency evidence, not MWE occurrence or sense truth. | B1 admitted as the reproducible 410,400-form ASCII frequency profile with visible profile-specific tokenizer, source denominator, ties, unmatched items, notice, fixtures, and removal path. Dispersion is not included. |
| Leipzig Corpora Collection | Official terms state that downloadable text corpora are CC BY, while other data/applications are offered for private and scientific use under CC BY-NC. Download packages include a frequency-ordered `*_words.txt`. | The exact English corpus, date, genre, package, and boundary between the CC BY download and CC BY-NC services must be fixed before deriving a browser table. Web/news/Wikipedia samples are not interchangeable baselines. | Candidate B2 for a contrasting written register; no artifact selected yet. |
| Lancaster Sensorimotor Norms | The official OSF project and article license the data under CC BY 4.0. The aggregated 39,707-concept CSV has a public artifact identifier and SHA-256 recorded below. | Sensorimotor strength is a semantic/experiential norm, not a synonym for lexical sophistication. The 17 MB CSV needs an attributed, reproducible browser subset or researcher-supplied loading path. | Candidate B3 for a later semantic profile; not a frequency baseline. |
| `wordfreq` | The official project says its code is Apache-licensed and redistributable data are CC BY-SA 4.0; it combines multiple domains and upstream sources and explicitly advises against conversion to CSV because attribution would be lost. | ShareAlike/attribution packaging, Python-specific normalization, mixed-domain weighting, large size, and a data snapshot through about 2021 make a silent browser extraction inappropriate. | Candidate C; evaluate only as a separately attributed add-on or external validation source. |
| SUBTLEX-US | Ghent University's official page provides 51-million-token American subtitle frequencies and contextual diversity; the paper says the norms are freely available for research purposes. | Research availability does not explicitly grant this project general redistribution, modification, or public browser delivery. Wordform/POS/Zipf files are distinct artifacts. | Candidate C; researcher-supplied use or written permission only. |
| EFLLex | UCLouvain provides 15,280 English lemmas with level frequencies across A1–C1 under CC BY-NC-SA 4.0. | NonCommercial and ShareAlike terms conflict with an unrestricted canonical core; textbook/receptive-frequency distributions are not learner mastery thresholds. | Candidate C; segregated researcher-supplied use only unless licensing strategy changes. |
| MorphoLex-en | The official repository contains roughly 70,000 English entries and morphological variables under CC BY-NC-SA 4.0. | NonCommercial and ShareAlike restrictions plus segmentation and family assumptions prevent inclusion in the permissively reusable core. | Candidate C; researcher-supplied or separately licensed module only. |
| Nation BNC/COCA word-family lists | Victoria University of Wellington's official Paul Nation pages distribute the BNC/COCA Level 6 v1.0.0 package and state that Paul Nation resources use CC BY-SA 4.0 or GPL 2/3 as appropriate. The downloaded package contains 25 one-thousand word-family files plus proper-name, marginal-word, transparent-compound, and acronym lists. | The package itself contains no artifact-specific license file, and the parent page does not explicitly map data to CC BY-SA versus the bundled legacy executable to GPL. Word-family Level 6 decisions, special lists, and tokenizer rules materially affect coverage. | Admit the exact local artifact for first-paper analysis and a researcher-supplied/import route. Before bundling a derived public profile, preserve the parent-page license evidence and obtain or document an artifact-specific license mapping; do not execute or redistribute the legacy Windows program. |
| NGSL 1.2 | The authors' current official `.com` site identifies itself as the only official NGSL Project site, provides NGSL 1.2 statistics and research-lemmatized files, and licenses the list under CC BY-SA 4.0. The abandoned `.org` domain now resolves to unrelated gambling content and is not a source. | NGSL's 2,809 ranked lemmas are not Nation BNC/COCA 1K/2K word families. The research form file explicitly collapses across meaning senses, generates possible forms, and flags homographs for researcher adjustment. | L2 admitted as an attributed 10,114-form browser profile with explicit first-1,000/2,000/full cutoffs, five retained multi-head homographs, `beyond_cutoff`/`unmatched` separation, source hashes, and ShareAlike modification notice. |
| Academic Word List / Academic Vocabulary List | University and author sites describe downloadable lists; the AVL is derived from COCA academic data. No explicit open redistribution license for the exact artifacts was found in the reviewed primary pages. | Free download and teaching/research use do not establish modification or browser redistribution rights; family/lemma/POS definitions also differ. | Candidate C; cite methods or accept researcher-supplied files, but do not bundle. |
| English Vocabulary Profile | Official terms permit personal noncommercial research/teaching uses and require prior written consent for broader reuse; Cambridge separately licenses dictionary data. | Account-bound access and restrictive reuse terms are incompatible with a freely redistributable static core. CEFR assignments are sense- and evidence-specific, not a universal word difficulty scale. | Candidate D; exclude from the bundle without a separate written license. |

### Core MWE evidence admission decision — 2026-09-03

The machine-readable [admission matrix](resources/mwe_core_evidence_admission_2026_09_03.json)
pins all four snapshots and keeps eight questions separate. Its result is not a
single resource ranking:

| Resource | Artifact / text rights | Span / category | Idiomaticity | Fine sense / uncertainty | Split | Decision |
|---|---|---|---|---|---|---|
| STREUSLE 5.0 | Exact external files; CC BY-SA plus source/PTB permission notice | Yes, including gaps and VPC.full/VPC.semi/VID | No separate label | Supersense only; no ambiguity state | Fixed, but this project's 40-item test projection is already exposed | **Go** for bounded occurrence/category evaluation |
| MAGPIE | Exact untagged commit; CC BY; BNC/PMB provenance retained externally | Member offsets, no VPC/VID category; supplied targets only | Five-way evidence and binary filtered sets | No inventory fine sense; agreement proxy only | Random and type-disjoint | **Go** only for secondary type-disjoint idiomaticity |
| SemEval-2022 Task 2 | Exact untagged commit; GPL; row-level web-source rights incomplete | No member offsets/category; supplied targets only | Binary | Paraphrase similarity, not a stable sense ID; unresolved cases discarded | Zero/one-shot, but final gold withheld | Development/method evidence only |
| MWEasWSD | Exact external artifacts; SemCor reusable with notice; added layer AGPL | Token indices/gaps, but zero category-confirmed VPC/VID rows | Sense-vs-not-MWE, not binary idiomaticity | Sparse observed polysemy; no uncertainty or independent labels; 125/136 verb-proxy rows lossless to OEWN | No document ID or manual-sense split | **Reject** as validation gold; external development only |
| Standard WSD multiword-verb slice | Exact external archive; no explicit zip redistribution grant | Head/lemma only; STREUSLE type-category proxy | No separate label | WordNet gold; 23 candidate-polysemous VPC rows losslessly mapped to OEWN; no usable uncertainty test | SemCor train; 6-row development; 17-row exposed source test | **Go with severe limits** for conditional sense smoke testing only |

The occurrence decision is **go with limits** using external STREUSLE: report
English Web-review strong VPC/VID exact spans/categories and the declared
continuous/discontinuous and seen/unseen strata, without tuning on or calling
the already inspected test projection blinded. The contextual fine-sense
decision is now **go with severe limits for a smoke test only**. The standard
WSD slice supplies 23 conditional VPC sense rows, but no located resource gives
an adequate target-wide VPC/VID test that also preserves member spans,
ambiguity, abstention, and out-of-inventory outcomes.

The completed
[MWEasWSD/SemCor reuse audit](resources/mweaswsd_semcor_reuse_audit_2026_09_03.json)
shows that rights are not the blocking issue: the official SemCor archive
contains a permissive notice and the added layer can remain external under
AGPL. Construct and quality are blocking. The artifact supplies no confirmed
VPC/VID category, independent/adjudicated labels, uncertainty states, or
credible untouched split, and its WordNet-to-OEWN mapping has real loss. It is
therefore rejected as validation gold. The bounded search is now closed by the
separate
[standard-WSD MWE-sense audit](resources/wsd_mwe_sense_slice_audit_2026_09_03.json):
the original source-task gold is admitted only as a tiny, external, sense-only
floor. This is not permission to create new gold or acquire a contextual model;
transparent baseline scoring comes first.

Primary evidence links:

- TAALES: <https://www.linguisticanalysistools.org/taales.html>
- Multi-Word Units Profiler, presentation, and author notes: <https://multiwordunitsprofiler.pythonanywhere.com/>, <https://masakieguchi.weebly.com/uploads/8/6/4/6/86461612/eguchi_2021_introducing_mwu_profiler.pdf>, <https://masakieguchi.weebly.com/egumasa_notes/category/all>
- Lextutor Phrase Profiler and Multiwords overview: <https://www.lextutor.ca/vp/collocs/>, <https://lextutor.ca/multiwords/>
- COCA downloads: <https://www.english-corpora.org/coca/help/download.asp>
- Open English WordNet and `take in`: <https://github.com/globalwordnet/english-wordnet>, <https://en-word.net/view/lemma/take%20in>
- PHaVE List: <https://doi.org/10.1177/1362168814559798>
- STREUSLE: <https://github.com/nert-nlp/streusle>
- MWE processing and experiment surveys: <https://aclanthology.org/J17-4005/>, <https://aclanthology.org/2023.mwe-1.15/>
- PARSEME guidelines, 2.0 shared task, and release tags: <https://parsemefr.lis-lab.fr/parseme-st-guidelines/1.2/>, <https://aclanthology.org/2026.mwe-1.33/>, <https://gitlab.com/parseme/sharedtask-data/-/tags>
- MAGPIE: <https://github.com/hslh/magpie-corpus>, <https://aclanthology.org/2020.lrec-1.35/>
- SemEval-2022 Task 2: <https://aclanthology.org/2022.semeval-1.13/>, <https://github.com/H-TayyarMadabushi/SemEval_2022_Task2-idiomaticity>
- MWEasWSD: <https://aclanthology.org/2023.findings-emnlp.14/>, <https://github.com/Mindful/MWEasWSD>
- SemCor 3.0 official distribution and CILI WordNet mappings: <https://web.eecs.umich.edu/~mihalcea/downloads.html#semcor>, <https://github.com/globalwordnet/cili>
- Standard WSD framework and source-task annotation papers: <https://lcl.uniroma1.it/wsdeval/>, <https://aclanthology.org/E17-1010/>, <https://aclanthology.org/W04-0811/>, <https://aclanthology.org/S07-1016/>, <https://aclanthology.org/S15-2049/>
- Idiom-dataset survey, KIT MWE/WSD data, and PVC Data: <https://aclanthology.org/2025.konvens-1.9/>, <https://doi.org/10.5281/zenodo.5167248>, <https://cogcomp.seas.upenn.edu/page/resource_view/26>
- English VMWE annotations: <https://aclanthology.org/L18-1396/>, <https://github.com/naist-cl-parsing/Verbal-MWE-annotations>
- CoAM and CAIGen: <https://aclanthology.org/2025.acl-long.1311/>, <https://github.com/Yusuke196/CAIGen>
- Project Gutenberg terms, license, robot guidance, Japanese term guidance, creator authority, and adaptation provenance: <https://www.gutenberg.org/policy/terms_of_use.html>, <https://www.gutenberg.org/policy/license>, <https://www.gutenberg.org/policy/robot_access.html>, <https://www.bunka.go.jp/seisaku/chosakuken/hokaisei/kantaiheiyo_chosakuken/1411890.html>, <https://www.bunka.go.jp/seisaku/chosakuken/seidokaisetsu/pdf/94383901_01.pdf>, <https://www.gutenberg.org/ebooks/author/35189>, <https://catalog.afi.com/Film/13671-THE-ADVENTURES-OF-A-BOY-SCOUT>
- Wikimedia Terms of Use and official dump documentation: <https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use/en>, <https://meta.wikimedia.org/wiki/Data_dumps/What%27s_available_for_download>, <https://meta.wikimedia.org/wiki/Data_dumps/Dump_format>
- TECO article and live OSF project: <https://doi.org/10.1016/j.rmal.2024.100123>, <https://osf.io/wrvj3/>
- MECO-L2 Wave 2 and CELER: <https://eprints.soton.ac.uk/494999/>, <https://pmc.ncbi.nlm.nih.gov/articles/PMC9692049/>, <https://github.com/berzak/celer>
- Santos et al. L2 idiom eye data: <https://arxiv.org/abs/2605.04857>, <https://doi.org/10.5281/zenodo.19582953>
- PARSEME FLAT and FLAT source: <https://parsemefr.lis-lab.fr/parseme-st-guidelines/2.0/?page=flat>, <https://flat.lisn.upsaclay.fr/>, <https://github.com/proycon/flat>
- INCEpTION: <https://inception-project.github.io/>
- PyMUSAS: <https://github.com/UCREL/pymusas>
- TUBELEX repository, license clarification, and paper: <https://github.com/naist-nlp/tubelex>, <https://github.com/naist-nlp/tubelex/issues/2#issuecomment-5235410477>, <https://aclanthology.org/2025.coling-main.641/>
- Leipzig terms and download format: <https://wortschatz.uni-leipzig.de/en/usage>, <https://wortschatz.uni-leipzig.de/public/documents/Format_Download_File-eng.pdf>
- Lancaster Sensorimotor Norms: <https://osf.io/7emr6/>, <https://doi.org/10.3758/s13428-019-01316-z>
- `wordfreq`: <https://github.com/rspeer/wordfreq>
- SUBTLEX-US: <https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus>
- EFLLex: <https://cental.uclouvain.be/cefrlex/efllex/download/>
- MorphoLex-en: <https://github.com/hugomailhot/MorphoLex-en>
- Nation BNC/COCA resource page and list description: <https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/vocabulary-analysis-programs>, <https://www.wgtn.ac.nz/__data/assets/pdf_file/0004/1689349/Information-on-the-BNC_COCA-word-family-lists-20180705.pdf>
- NGSL 1.2 official project page: <https://www.newgeneralservicelist.com/new-general-service-list>
- Academic Word List and Academic Vocabulary List: <https://www.wgtn.ac.nz/lals/resources/academicwordlist/information>, <https://www.academicwords.info/>
- English Vocabulary Profile terms: <https://englishprofile.org/?menu=evp-terms-of-use>
- English Wiktionary reuse terms, dated dumps, Wiktextract, and Kaikki exports:
  <https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use>,
  <https://dumps.wikimedia.org/enwiktionary/>,
  <https://github.com/tatuylonen/wiktextract>,
  <https://kaikki.org/dictionary/rawdata.html>
- Simple English Wikipedia About page, dated dump, Wikimedia terms, Parse API,
  and API etiquette: <https://simple.wikipedia.org/wiki/Wikipedia:About>,
  <https://dumps.wikimedia.org/simplewiki/20260801/>,
  <https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use>,
  <https://www.mediawiki.org/wiki/API:Parsing_wikitext>,
  <https://www.mediawiki.org/wiki/API:Etiquette>

## Pinned resource evidence

B-MWE1, B1, and L2 are bundled as attributed projections of pinned open resources.
B-MWE2 admits only an external offline benchmark profile: its corpus remains in
the upstream checkout. The other checks establish reviewable candidate
identities but do not admit those artifacts.

### B-MWE1 — OEWN 2025 `take in#v` projection

- Official release: Open English WordNet 2025 Edition, released 2025-12-31;
  tag `2025-edition`, repository commit
  `dc343f2683279ecbb13fab4e2fd778d7b162d287`.
- Source asset: `english-wordnet-2025-json.zip`, 9,986,555 bytes. The GitHub
  release reports—and the downloaded asset independently matched—SHA-256
  `7d749f6e2c39e6970e4997839dcf6e42fd281f3c2fae0171d2192bae8cfa4b51`
  on 2026-09-01.
- Projection: the one verb entry `take in#v`, all 17 sense keys, and only the
  linked synset ID, ILI, definition, synonyms, and source examples needed for
  human review. Lexical/synset relations and subcategorization frames are
  omitted; source wording is unchanged. The checked-in projection has SHA-256
  `cd5381a09769f9d3e66e0a608ecd8016d775350abd4e882095a085c471df6867` and is
  loaded locally for human review and lossless decision export.
- Browser form projection: 2,847 normalized verb entries containing two or more
  ASCII word members, stored only as canonical form plus source sense count.
  Exact lookup occurs after human confirmation. `take in` has 17 source senses
  and `spill the beans` has one; those counts do not assign a contextual sense.
  The 52,420-byte checked-in profile has SHA-256
  `513714774f0e087e9ba03c8fa04e969b8314786ccbdaa06dbbeeb35127f6a41e`.
- Reproduction: download the exact asset and run
  `python3 scripts/extract_oewn_take_in.py PATH --check resources/oewn_take_in_2025.json`.
  The standard-library script rejects any source with a different SHA-256 or a
  candidate set other than 17 unique senses.
- Rights: the OEWN notice requires attribution to both Princeton WordNet and
  the Open English WordNet team. The subset retains the CC BY 4.0 link, the
  underlying WordNet License link and exact local notice,
  copyright/attribution, modification, source, citation, and no-endorsement
  notices. It is not covered by this project's dual-license grant.
- Construct boundary: OEWN supplies the complete candidate inventory for this
  form and POS, not occurrence detection, sense frequencies, L2 pedagogical
  priority, or contextual gold labels. M3's two assignments are visibly
  project-authored decisions and the contract preserves ambiguity and
  abstention.
- Removal: delete the projection, remove its contract dependency, and return
  M3 to clearly project-only toy IDs or an unavailable inventory state. Never
  substitute a new OEWN release under the 2025 identifier.

### B-MWE2 — external STREUSLE 5.0 VPC/VID benchmark profile

- Official release: tag `v5.0`, commit
  `8ba61fe4f216e7967500a862554a4fff79d25f5d`, dated 2025-11-15.
- Pinned JSON artifacts: train 16,845,570 bytes / SHA-256
  `36aef0205a6e2e154b681d7520858693a264d3c40ba7d97c089345bbd1149a22`;
  dev 2,050,638 bytes / `56cc1783962ce8c9f06b7649ffdccb48cea14ee7e4a8be2e35214ffc71303e9a`;
  test 2,051,895 bytes / `f8144e6227db2e845cda4aa832f8d5644cb40b9e743d1dbe05663dd687d2c70c`.
- Projection: strong `V.VPC.full`, `V.VPC.semi`, and `V.VID` occurrences only.
  Test has 40 target occurrences/35 types, including 16 discontinuous
  occurrences and 16 occurrences whose casefolded `lexlemma` is unseen in
  train.
- Transparent floor: contiguous train-lemma matching yields exact-span
  precision 0.386364, recall 0.425, F1 0.404762; exact span-plus-category F1
  0.380952; discontinuous and unseen recall are both zero.
- Frozen gap/dependency comparator: train-derived lemma and dependency evidence
  plus development-only threshold selection yields development exact-span F1
  0.426667 and discontinuous recall 8/14. Its exposed-test exact-span F1 is
  0.536585 and discontinuous recall is 6/16; unseen-type recall remains zero.
  These are external development diagnostics, not sealed project results.
- Reproduction: obtain the free tagged release separately and run
  `python3 scripts/check_streusle_v5.py PATH --check --surface-baseline --gap-dependency-baseline`. The
  checker validates all three hashes before reading the projection and emits no
  raw text.
- Sense-inventory planning audit: obtain the separately licensed OEWN 2025 JSON
  release and run
  `python3 scripts/audit_streusle_oewn_coverage.py STREUSLE_PATH OEWN_ZIP --check resources/streusle_v5_oewn_2025_coverage_audit.json`.
  The audit emits only aggregate counts and lexical type identifiers. It finds
  exact OEWN verb entries for 317/624 target occurrences but only 45/319 VIDs;
  this is an inventory-alignment warning, not permission to relicense either
  source or evidence that the unmatched meanings are absent from OEWN.
- Wiktionary follow-up audit: with the 206 separately derived residual VID types
  and ignored local cache, run
  `python3 scripts/audit_streusle_kaikki_vid.py STREUSLE_PATH OEWN_ZIP --check resources/streusle_v5_kaikki_vid_audit_2026_09_03.json`.
  The committed result contains aggregate counts and one combined response-
  manifest hash only. It does not contain or relicense target lists, entries,
  glosses, examples, or sense text; `--fetch` is needed only to create a new
  explicitly dated audit and must not be used as a live app dependency.
- Bounded nonexact queue: the exact-audit cache, pinned OEWN zip, and ignored
  424,557,919-byte Kaikki English-verb JSONL reproduce
  `resources/sense_mapping_queue.json` with
  `python3 scripts/build_sense_mapping_queue.py OEWN_ZIP KAIKKI_JSONL --check resources/sense_mapping_queue.json`.
  Its source scan produces candidate sets for 3/146 residual types and preserves
  143/146 as unresolved. The projection includes modified STREUSLE type labels
  and minimal source identifiers under the notices above, but no dictionary
  wording or corpus text; it is a review queue, not a sense inventory.
- VPC/VID candidate seed: the pinned OEWN zip reproduces
  `resources/hybrid_sense_inventory_v1.json` with
  `python3 scripts/build_hybrid_sense_inventory.py OEWN_ZIP --check resources/hybrid_sense_inventory_v1.json`.
  Its 67 gloss/example records retain OEWN/WordNet terms and notice; the nine
  forms come only from already exposed training/development design metadata.
  Reserved IDs are not admitted senses, and the raw OEWN archive stays ignored.
- VID inventory pilot: obtain the exact STREUSLE 5.0 checkout and pinned OEWN
  zip, retain the existing ignored Kaikki audit cache, and run
  `python3 scripts/build_inventory_population_log.py STREUSLE_CHECKOUT OEWN_ZIP --check resources/inventory_population_log.json`.
  The public log contains only 14 selected train type identifiers, aggregate
  occurrence/gap counts, and source-route/eligibility metadata. It contains no
  sentence/token text or dictionary wording and cannot estimate population
  coverage.
- Hybrid inventory coverage v2: using the exact STREUSLE checkout and the public
  inventory/audit records, run `python3
  scripts/audit_hybrid_inventory_coverage.py STREUSLE_CHECKOUT --check
  resources/hybrid_inventory_coverage_v2.json`. The result uses all 624 targets
  and all 14 pilot types, emits aggregates only, and treats candidate routes as
  unreviewed availability rather than operational sense coverage.
- Rights: retain [`resources/STREUSLE_NOTICE.md`](resources/STREUSLE_NOTICE.md).
  No upstream corpus, annotations, code, or model is copied here. STREUSLE is an
  occurrence benchmark, not a reference distribution or fine-sense resource.
- Removal: delete the metadata profile, checker, notice, and related claims. No
  corpus artifact requires deletion from this repository because none is
  bundled.

### B1 — TUBELEX English regex ASCII word frequency

- Repository commit: `7cb5fb36add76b83a266d1967536e1a1d3faa513`
  (2025-04-24).
- Artifact: `frequencies/tubelex-en-regex.tsv.xz`, 3,198,336 bytes; Git blob
  SHA-1 `be2ca3c9076cfc4bdc58bc1599ea20f410964c4d`.
- Independently streamed SHA-256 on 2026-09-01:
  `363de2f2ea58c3b4ff25306a6819c7424198d250902b3b0e566573015560c3ec`.
- Observed schema: `word`, `count`, `videos`, `channels`, and 15 `count:*`
  category columns. There are 445,954 lines including the header and total row.
- The `[TOTAL]` row reports 179,139,158 tokens, 105,733 videos, and 68,405
  channels. It occurs at line 2,615, not at the final line as the README states;
  an importer must locate and validate the label rather than assume row order.
- The admitted projection retains 410,400 lowercase ASCII alphabetic surface
  forms and their counts, representing 170,705,938 source tokens. It uses an
  explicit profile tokenizer (NFKC, ASCII letters, apostrophe/hyphen boundaries),
  the 179,139,158-token source total for per-million values, competition ranks,
  and unmatched rather than invented zero values. It does not include or infer
  dispersion because the selected projection exposes frequency only.
- The 6,157,414-byte checked-in profile has SHA-256
  `d177f22f5cd4c86d5d7465197eebccceda84c0e3ab8ca5ecfbcdbc9fbd29d1bc`.
- Rights evidence: the repository maintainer's 2026-08-10 response confirms
  that published frequency lists and reformatted copies are covered by the
  repository's BSD-3-Clause conditions.
- Reproduction: download both pinned source assets and run
  `python3 scripts/build_reference_profiles.py TUBELEX_XZ OEWN_ZIP --check`.
  The standard-library builder rejects changed hashes, schemas, totals, row
  counts, and fixed `the`/`take`/`xylophone` and OEWN checks.
- Browser preparation smoke check on Node 24.9.0 arm64: 6,157,414-byte initial
  payload, 71.0 ms JSON parse, 43.0 ms Map construction, about 72.5 MB heap after
  load. This is a machine-specific ceiling check, not real-browser usability
  evidence.
- Rights: retain [`resources/TUBELEX_LICENSE.txt`](resources/TUBELEX_LICENSE.txt),
  whose exact checked-in text has SHA-256
  `51b9e39825bbf19e4bb777bf11a7520a3935ff859c4d0ee724dfe9ddb26a961f`.
- Removal: delete the profile, notice, runtime fetch/use/tests, and related
  claims. Never substitute a newer TUBELEX table under this profile version.

### L1 — Nation BNC/COCA Level 6 local-only word-family profile

- Official source: Victoria University of Wellington's Paul Nation vocabulary
  analysis page, file `BNC_COCA_25000.zip`, described as BNC/COCA v1.0.0.
- Local candidate artifact: 600,930 bytes; SHA-256
  `ac81c7a60e5c76cd2bbf0c59b0501808f0d4fa026b2936919dd54329a9bb6a69`,
  retrieved 2026-09-01 and kept under ignored `research_data/` only.
- Observed contents: `basewrd1.txt` through `basewrd25.txt`, four special
  lists, empty placeholder levels, `range.txt`, and a legacy Windows Range
  executable. The first and second levels each contain exactly 1,000 headword
  families; their files contain 5,857 and 5,370 indented family-member rows,
  respectively.
- Rights evidence: the official parent page states that Paul Nation resources
  use CC BY-SA 4.0 or GPL 2/3 as appropriate, but the zip contains no license
  file mapping the word-list data and executable to those alternatives. The
  study may pin and analyze the locally obtained data. Public bundling remains
  gated on preserving or confirming the resource-specific mapping; the legacy
  executable will not be run, copied, or made a dependency.
- Local projection: `scripts/build_bnc_coca_profile.py` validates the exact zip,
  reads only levels 1 and 2, and produces 13,223 sorted ASCII surface rows for
  2,000 family heads. Four accented duplicate variants are excluded. The exact
  generated JSON is 366,120 bytes with SHA-256
  `ebd06548187988eb1a61ab967cc39c01461023043ee7aef427606e5bf508f138`.
  Browser import requires that size and hash; the method export records the
  runtime hash. Neither source nor generated JSON is committed or transmitted.
- Construct boundary: this is the primary conventional 1K/2K Level 6
  word-family baseline for the Nation comparison. Proper names, marginal words,
  transparent compounds, and acronyms are excluded; tokenization and family-
  member matching remain reported decisions. It supplies no MWE occurrence, sense,
  learner-knowledge, or comprehension evidence.

### L2 — NGSL 1.2 open-list profile

- Official source: the authors' current
  `newgeneralservicelist.com/new-general-service-list` page, which identifies
  that `.com` site as the only official NGSL Project site, dates NGSL 1.2 to
  April 2023, and applies CC BY-SA 4.0. The old `.org` domain is unrelated and
  must never be used as a source.
- Statistics artifact: `NGSL_1.2_stats.csv`, 62,566 bytes; SHA-256
  `2098bab8955a120a9766c6282a51d7d578c6cb0a7d946600d2ffb73ba25a0b44`.
  It contains 2,809 unique lemma rows, ranks 1–2,809 without gaps or duplicate
  ranks, SFI, and adjusted frequency per million.
- Research-form artifact: `NGSL_1.2_lemmatized_for_research.csv`, 89,485 bytes;
  SHA-256
  `d814f2a0a3c61479a2c5ad037661719a0cc6e7dbcde31f181b54f12d0f1e11a4`.
  It contains the same 2,809 headwords with proposed surface forms. Its own
  header says it disregards meaning sense, generates possible forms, and
  requires researcher adjustment for homographs such as `found`, `left`,
  `mine`, `rose`, and `wound`.
- Admitted projection: `resources/ngsl_1_2_ascii_forms.json`, 308,816 bytes;
  SHA-256
  `f613834eac74e19cef787faf1414a716388c047b3f5b7e39db88c78883fef6d9`.
  It retains 10,114 ASCII forms and all head/rank mappings; `found`, `left`,
  `mine`, `rose`, and `wound` each retain two candidates. Seven hyphenated
  variants are excluded because the declared tokenizer splits hyphens and the
  source also supplies unhyphenated variants.
- Reproduction: run
  `python3 scripts/build_ngsl_profile.py STATS_CSV RESEARCH_FORMS_CSV --check`.
  The standard-library builder verifies both source hashes, their composite
  identity, 2,809 ranks, form/head mappings, ambiguous forms, and cutoff
  boundary fixtures.
- Rights: retain [`resources/NGSL_NOTICE.md`](resources/NGSL_NOTICE.md), whose
  exact checked-in text has SHA-256
  `bd9e26de02a697d9020780d535d18a01033a072e19a3b0a680115bd511d1d931`.
  The projection remains CC BY-SA 4.0 and is not covered by the project's dual
  license. First-1,000/2,000 results are NGSL rank cutoffs, not Nation/BNC/COCA
  word-family levels.
- Construct boundary: NGSL is an open general-service-list contrast. It does
  not determine contextual meaning, MWE membership, individual knowledge, or a
  universal 95% threshold.

### B2 — Leipzig written-register candidate

The official download format supplies word, frequency, optional POS/baseform,
source, and metadata files. Selection remains deliberately open because choosing
news, web, Wikipedia, country, year, and corpus size is a construct decision, not
just a download decision. The next review must pin one English package and its
license notice before computing a checksum or derived list.

### B3 — Lancaster semantic candidate

- OSF project `7emr6`, Data component `rwhs6`, CC BY 4.0.
- Aggregated artifact `Lancaster_sensorimotor_norms_for_39707_words.csv`, OSF
  file `48wsc`, 17,196,336 bytes, version 1.
- OSF-recorded SHA-256:
  `445d363fb1f9f3e50b86d88e2f46cdc9a22b5dd8a713ce4e7be2a773d57f43c5`.
- Use only the aggregated word-level artifact. A corrected 2024 file applies to
  trial-level participant data; the OSF component states the aggregated norms
  were unaffected.

### Researcher-supplied route

The pinned BNC/COCA route now accepts only the exact generated first-2K profile,
hashes it in the browser, and exports the selected level and runtime identity.
SUBTLEX-US, EFLLex, MorphoLex-en, and other lawfully
held tables can still be scientifically useful without entering this
repository. A future local-file adapter may accept another documented table, hash it
in the browser, require the researcher to name its version and rights basis,
and export coverage and column mapping. The app must not provide, proxy, or
silently normalize a restricted artifact. A generic plugin system is not justified.

## Admission record required per artifact

No resource-dependent metric may move from candidate to bundled until its row
has all of the following:

- canonical source URL, rights holder, artifact name, version/retrieval date,
  and SHA-256 hash;
- exact license text and attribution, including incorporated or upstream data;
- explicit analysis of redistribution, modification, derived-value publication,
  browser delivery, commercial/noncommercial scope, and ShareAlike obligations;
- method citation, population/genre/time/language-variety description,
  preprocessing, unit, coverage denominator, and missing-value behavior;
- package location separated from project code where license obligations differ;
- independent numerical fixture and a removal/replacement procedure.

Complete these fields in a copy of `reference_profile_template.json` for each
resource projection and coverage channel. One source used for two channels gets
two manifests when its unit, denominator, or processing differs.

If any field is unknown, the artifact remains unbundled. A metric can still be
documented conceptually with project-authored toy data, but must not silently
substitute another resource or inherit the name of an established tool.

## Stakeholder and independence policy

- Tool and method authors receive exact citations and license compliance; this
  app does not imply their endorsement or allege wrongdoing from restrictive
  terms.
- Corpus/list creators and platform/content rightsholders are distinct parties;
  permission from one does not automatically bind the others.
- Authors and research participants represented in source texts retain privacy,
  consent, and withdrawal interests beyond copyright alone.
- Browser-local processing reduces disclosure risk but does not make unsuitable
  input acceptable; this probe explicitly excludes private learner text,
  personal data, confidential material, and unpublished manuscripts.
- Researchers need stable versions, coverage diagnostics, and exportable
  provenance rather than dependence on one opaque hosted service.
- Maintainers and hosts may recover legitimate costs, but the canonical core
  release must remain downloadable, locally runnable, and forkable without a
  paid corpus or proprietary API.
- Names such as TAALES and TAALED are references to independent projects, not
  compatibility marks, certifications, or product branding for this app.
