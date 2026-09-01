# Rights and provenance register

Status: evidence review for the independent static probe, 2026-09-01

This register distinguishes tool code, method descriptions, lexical resources,
derived tables, and example texts. Availability, free download, academic use,
and open redistribution are not synonyms. Each admitted artifact needs its own
record. The decisions below are conservative project gates, not legal advice.

## Active release tree

| Item | Origin | Runtime use | Current decision |
|---|---|---|---|
| `index.html`, contracts, and tests | Original project code | Static browser app and verification | Dual-licensed MIT or CC BY 4.0 at the recipient's choice; no third-party runtime code. |
| Scenarios in `samples.json` | Project-authored synthetic transformations | Browser comparisons | Dual-licensed MIT or CC BY 4.0; no person, learner corpus, API, or third-party text. |
| Researcher-entered text | Researcher-selected synthetic or rights-cleared published material | Browser-memory calculation only | Not bundled, transmitted, retained, or included in JSON; the checkbox records user attestation but is not a legal determination by the app. |
| Exported analysis record | Project schema plus researcher labels, provenance, hashes, client-clock time, and results, including document-batch rows | Explicit local JSON download | Raw text is omitted. The researcher controls and must review labels/provenance before sharing; the editable JSON, hash, and timestamp are not signatures or proof of authorship/time. |
| Lexical lists, corpora, models, dictionaries | None bundled | None | Not admitted. |
| Browser platform | User agent | Rendering and local calculation | No installed package or third-party script. |
| Python and Node.js | Local/CI environment | Tests and optional static serving only | Not shipped as application dependencies. |
| Method citations | Bibliographic metadata and DOI links | Interpretation evidence only | Attributed in the metric contract and export; no third-party code, data, or article text is copied. |

The archived MWE/VPC roadmap is an evidence inventory, not a release input.
Parent-directory data, credentials, code, lexical resources, and research
records are not part of this repository.

## External resource evidence

| Candidate | Verified evidence | Rights/construct risk | Admission |
|---|---|---|---|
| TAALES | The official site and index guide document separate word, contiguous bigram/trigram, coverage, and POS-tagged polysemy indices; the tool is CC BY-NC-SA 4.0. The audited 2.8.1 copy forms all adjacent n-grams mechanically and looks up polysemy by word/POS rows. | A `take in` bigram value does not identify a VPC, recover separated `take ... in`, or assign a contextual sense. Sharing or adaptation must also satisfy NonCommercial/ShareAlike, and the tool notice does not establish rights to every bundled corpus/list. | Comparator and methodological prior art only; no code/data import or compatibility claim. |
| Multi-Word Units Profiler 2.0.1 | The live site labels the profiler CC BY-NC-SA 4.0 and offers four research-based lists. Eguchi's 2021 presentation documents Python/spaCy lemmatization and parsing, n-gram/dependency candidate extraction, list matching, highlighted text, and item tables. Project-authored probes confirmed both contiguous and dependency-separated matches while the M1-M4 `take in` strings remained unmarked. | The site-level license does not establish reusable licenses for each incorporated list, example, frequency, or corpus-derived field; no corresponding source/data release was located in this review. The hosted POST sends raw input to PythonAnywhere, and no retention guarantee is presented on the input page. Its list-driven matches are not contextual VPC or fine-sense gold labels. | Primary behavioral comparator and methodological/UI prior art only. Do not copy code, lists, examples, or frequency fields, automate the hosted service, or send protected research text without permission and a documented privacy basis. |
| Lextutor Phrase Profiler 1.2 | The official page describes matching up to 30,000 words against selectable phrase/collocation lists; its Multiwords page distinguishes this from n-gram and MI-based extractors. | No explicit open redistribution license for the profiler payloads was found on the reviewed pages, and each incorporated list has separate rights and construct assumptions. Hosted input leaves the researcher's browser. | Secondary behavioral comparator only; do not copy its lists or make it a required reproducibility dependency. |
| COCA | The official download page sells word-frequency and 2–5-gram data and describes more than 40 million downloadable n-grams. | Purchase/offline processing does not state permission to expose the data through this public service. Hiding it in a database would not establish server-use, public-query, or derived-output rights. | Exclude unless written permission covers the exact artifact and delivery/output mode. |
| Open English WordNet | The official repository releases OEWN under CC BY 4.0. Its 2025 entry for `take in` has 17 verb senses, demonstrating that the MWE needs an inventory entry distinct from `take` and `in`. | Attribution and incorporated-material notices must travel with the exact pinned release. Inventory membership and sense count do not perform contextual WSD, and automatic use must preserve ambiguity/abstention. | Candidate B-MWE1 for the first open form/sense inventory; not yet bundled. |
| PHaVE List | Garnier and Schmitt's article defines 150 frequent phrasal verbs and key meaning senses covering at least 75% of their COCA occurrences. | This is the closest L2-pedagogical target, but the publisher labels the article restricted access and routes reuse of its non-OA supplemental lists to the copyright holder. COCA-derived percentages add a separate provenance question. | Candidate C-MWE2 for method/citation or written permission; do not copy the lists, glosses, examples, or percentages into the app. |
| STREUSLE | The official repository provides more than 55,000 words, more than 3,000 MWE instances, supersenses, recoverable gaps, and PARSEME-compatible VPC categories; annotations are CC BY-SA 4.0. | It is a web-review gold corpus and coarse semantic annotation, not a general phrasal-verb frequency or fine-grained sense inventory. ShareAlike and source-text notices require separate packaging. | Candidate C-MWE3 as a segregated validation corpus and existing-tagger benchmark, not the canonical runtime lexicon. |
| PARSEME guidelines | The official guidelines define verbal MWEs, syntactic variants, lexicalized components/open slots, and VPC tests under CC BY 4.0. | Guidelines establish annotation decisions, not an English production detector or fine-grained sense inventory. Corpus licenses must be checked per language/release. | Methodological source for the VPC annotation contract; no new category scheme should be invented first. |
| PARSEME corpus/shared task 2.0 | The 2026 shared-task paper reports 17 languages, all five syntactic category families, ten identification systems including a baseline, and a new paraphrasing task. Official GitLab tags pin the 2025 training and blind releases. | The guidelines' license does not automatically establish the license and source-text terms for every language corpus, model, or derived artifact. All-type performance is not English-VPC performance. | Current benchmark frame; select and pin an English VPC projection only after file-level license, split, and provenance review. |
| MAGPIE | The official repository publishes 56,622 BNC-based potentially idiomatic-expression instances across 1,756 types, crowdsourced sense labels, confidence filtering, and random/type-disjoint splits under CC BY 4.0. | It primarily supports literal/idiomatic contextual classification across idiom types; it is not a VPC occurrence corpus or an OEWN-compatible fine-sense gold standard. BNC-derived context and notices must remain visible. | Candidate B-MWE4 for a segregated M4 transfer/error benchmark; do not use it to validate fine-sense coverage. |
| SemEval-2022 Task 2 idiomaticity data/code | The shared task provides English, Portuguese, and Galician contextual idiomaticity data; the official repository contains data and preprocessing under GPL-3.0. | Binary idiomaticity and sentence representation differ from VPC identification and fine-sense assignment. Repository licensing still requires checking incorporated source text and each artifact. | Secondary benchmark/method source only; no runtime or model dependency. |
| MWEasWSD | The published method filters rule-generated MWE candidates using context and sense glosses and reports results on DiMSUM and PARSEME English. The official code is AGPL-3.0. | The repository combines SemCor, PARSEME, DiMSUM, synthetic annotations, and separately hosted models; a code license does not flatten those data/model terms. Its model stack is not browser-minimal. | Published baseline candidate; reproduce externally on a pinned test projection before considering any component. |
| English VMWE annotations (Kato et al.) | The paper reports 7,833 VMWE instances and 1,608 types, including discontinuous items, with literal/non-literal definitions plus `none` and `hard to judge` choices. The repository exposes indices and masked dependencies. | No repository license was found, and reconstruction depends on LDC OntoNotes/WSJ text. Its Wiktionary-era sense choices are not automatically OEWN-compatible. | Quarantine as methodological and evaluation prior art; do not redistribute or make it a required benchmark. |
| CoAM / CAIGen | CoAM reports 1.3K human-annotated, reviewed, consistency-checked all-type MWE sentences. Its CAIGen annotation interface is MIT-licensed and supports discontinuous/overlapping spans. | Interface code and corpus data are separate artifacts. The exact CoAM dataset license was not confirmed in this review; Google-based annotation also sends data outside the local browser. | Cite as an all-type stress-test and annotation precedent; quarantine the data and exclude CAIGen as a runtime dependency pending a demonstrated workflow need. |
| FLAT / PARSEME FLAT | PARSEME identifies FLAT as its online annotation platform. FLAT is GPL-3.0 Web software with multi-user storage, permissions, provenance, confidence, token/span annotation, and document history; the reviewed PARSEME deployment reports FLAT 0.11.6 and requires login. | A software license does not grant access to the hosted PARSEME project or its documents. Forking its Django/CherryPy/FoLiA stack would add infrastructure without providing this project's coverage or sense estimands. | External annotation workflow and interoperability target only; no code, service, or data import. |
| INCEpTION | The official project releases the Web annotation platform under Apache-2.0; version 41.4 was released 2026-08-18. It supports configurable spans/relations and recommenders. | It is not MWE-specific, and its guide says discontinuous spans require relation/link emulation. Hosted services have their own access and privacy conditions. | Optional external annotation/adjudication workflow; no runtime dependency or embedding. |
| PyMUSAS | The official Apache-2.0 Python project provides rule-based, neural, and hybrid semantic taggers and reports MWE support for English. | It is a library rather than the target Web app; USAS semantic tagging is not OEWN fine-sense assignment, and code, models, rules, and upstream data require artifact-level review. | Candidate detector baseline only; benchmark before any component admission. |
| TUBELEX | The official repository publishes aggregate word-frequency and dispersion lists alongside a BSD-3-Clause license and states that full corpus text is not published. In a 2026-08-10 repository issue, the maintainer expressly confirmed that the published frequency lists are covered by BSD-3-Clause and may be redistributed, incorporated commercially, or reformatted under its conditions. The pinned English regex artifact was independently streamed and checked below. | YouTube-subtitle sampling, normalization, denominator, and upstream-content constraints remain part of the construct record even though the frequency-list redistribution question is resolved. | Candidate B1; rights-cleared for preparation, but not bundled until projection, notice, performance, and fixture checks pass. |
| Leipzig Corpora Collection | Official terms state that downloadable text corpora are CC BY, while other data/applications are offered for private and scientific use under CC BY-NC. Download packages include a frequency-ordered `*_words.txt`. | The exact English corpus, date, genre, package, and boundary between the CC BY download and CC BY-NC services must be fixed before deriving a browser table. Web/news/Wikipedia samples are not interchangeable baselines. | Candidate B2 for a contrasting written register; no artifact selected yet. |
| Lancaster Sensorimotor Norms | The official OSF project and article license the data under CC BY 4.0. The aggregated 39,707-concept CSV has a public artifact identifier and SHA-256 recorded below. | Sensorimotor strength is a semantic/experiential norm, not a synonym for lexical sophistication. The 17 MB CSV needs an attributed, reproducible browser subset or researcher-supplied loading path. | Candidate B3 for a later semantic profile; not a frequency baseline. |
| `wordfreq` | The official project says its code is Apache-licensed and redistributable data are CC BY-SA 4.0; it combines multiple domains and upstream sources and explicitly advises against conversion to CSV because attribution would be lost. | ShareAlike/attribution packaging, Python-specific normalization, mixed-domain weighting, large size, and a data snapshot through about 2021 make a silent browser extraction inappropriate. | Candidate C; evaluate only as a separately attributed add-on or external validation source. |
| SUBTLEX-US | Ghent University's official page provides 51-million-token American subtitle frequencies and contextual diversity; the paper says the norms are freely available for research purposes. | Research availability does not explicitly grant this project general redistribution, modification, or public browser delivery. Wordform/POS/Zipf files are distinct artifacts. | Candidate C; researcher-supplied use or written permission only. |
| EFLLex | UCLouvain provides 15,280 English lemmas with level frequencies across A1–C1 under CC BY-NC-SA 4.0. | NonCommercial and ShareAlike terms conflict with an unrestricted canonical core; textbook/receptive-frequency distributions are not learner mastery thresholds. | Candidate C; segregated researcher-supplied use only unless licensing strategy changes. |
| MorphoLex-en | The official repository contains roughly 70,000 English entries and morphological variables under CC BY-NC-SA 4.0. | NonCommercial and ShareAlike restrictions plus segmentation and family assumptions prevent inclusion in the permissively reusable core. | Candidate C; researcher-supplied or separately licensed module only. |
| NGSL/NAWL family | Previously indexed project pages stated CC BY-SA 4.0 for some named lists, but the former project domain resolved to unrelated gambling content during the 2026-09-01 review. | A stale search result or mirror is not an authoritative artifact. ShareAlike packaging, exact version, corpus provenance, and current rights-holder source are unresolved. | Candidate C; quarantine until an authoritative stable source is confirmed. |
| Academic Word List / Academic Vocabulary List | University and author sites describe downloadable lists; the AVL is derived from COCA academic data. No explicit open redistribution license for the exact artifacts was found in the reviewed primary pages. | Free download and teaching/research use do not establish modification or browser redistribution rights; family/lemma/POS definitions also differ. | Candidate C; cite methods or accept researcher-supplied files, but do not bundle. |
| English Vocabulary Profile | Official terms permit personal noncommercial research/teaching uses and require prior written consent for broader reuse; Cambridge separately licenses dictionary data. | Account-bound access and restrictive reuse terms are incompatible with a freely redistributable static core. CEFR assignments are sense- and evidence-specific, not a universal word difficulty scale. | Candidate D; exclude from the bundle without a separate written license. |

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
- English VMWE annotations: <https://aclanthology.org/L18-1396/>, <https://github.com/naist-cl-parsing/Verbal-MWE-annotations>
- CoAM and CAIGen: <https://aclanthology.org/2025.acl-long.1311/>, <https://github.com/Yusuke196/CAIGen>
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
- Academic Word List and Academic Vocabulary List: <https://www.wgtn.ac.nz/lals/resources/academicwordlist/information>, <https://www.academicwords.info/>
- English Vocabulary Profile terms: <https://englishprofile.org/?menu=evp-terms-of-use>

## Pinned candidate evidence

No external resource has entered the active tree. The checks below establish a
reviewable candidate identity; they do not by themselves admit the artifact.

### B1 — TUBELEX English regex frequency and dispersion

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
- The table contains punctuation and non-ASCII entries. Any English-ASCII
  projection would be a documented derived artifact, not the original list;
  coverage must use an explicit denominator and report unmatched input.
- Rights evidence: the repository maintainer's 2026-08-10 response confirms
  that published frequency lists and reformatted copies are covered by the
  repository's BSD-3-Clause conditions.
- Before admission: define the projection, preserve the upstream identity, add
  attribution and notice files, test browser transfer/memory cost, and create
  independent numerical fixtures.

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

SUBTLEX-US, EFLLex, MorphoLex-en, and other lawfully held tables can still be
scientifically useful without entering this repository. A future local-file
adapter may accept a documented table, hash it in the browser, require the
researcher to name its version and rights basis, and export coverage and column
mapping. The app must not provide, proxy, or silently normalize a restricted
artifact. Implement this route only with the first concrete schema; a generic
plugin system is not justified.

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
