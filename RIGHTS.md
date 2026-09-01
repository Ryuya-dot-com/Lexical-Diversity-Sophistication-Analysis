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

The archived MWE/VPC roadmap is ignored. Parent-directory data, credentials,
code, lexical resources, and research records are not part of this repository.

## External resource evidence

| Candidate | Verified evidence | Rights/construct risk | Admission |
|---|---|---|---|
| TAALES | Official site states CC BY-NC-SA 4.0 and more than 400 lexical-sophistication indices. | Sharing or adaptation must comply with NonCommercial, attribution, and ShareAlike conditions; permissive relicensing is not available under those terms. The notice also does not establish rights to every underlying list/corpus. | Methodological reference only; no code/data import and no equivalence claim. |
| COCA | Official download page offers frequency data and corpus text through paid products. | Purchase/access is not public redistribution permission; browser bundling could expose licensed data. | Exclude unless explicit rights for the exact artifact and delivery mode are obtained. |
| Open English WordNet | Official repository states CC BY 4.0 and also preserves attribution to the underlying Princeton WordNet material. | Attribution and incorporated-material notices must travel with an exact pinned release; semantic-resource scores have sense/POS/coverage assumptions. | Candidate B; not yet bundled. |
| TUBELEX | Official repository publishes aggregate frequency lists and code under BSD-3-Clause, states that full corpus text cannot be published, and documents some evaluation resources it cannot redistribute. | Repository-level license must be checked against the exact frequency artifact and upstream platform/content constraints; frequency reflects a particular multilingual YouTube-subtitle sample and processing pipeline. | Candidate B pending artifact-level notice, version, hash, and maintainer confirmation if needed. |
| NGSL family | A currently reachable project page states CC BY-SA 4.0 for NGSL-Spoken, but the site presentation/domain provenance is presently unreliable and this does not establish terms for every NGSL artifact. | ShareAlike packaging, artifact identity, corpus provenance, and current authoritative source require review. | Candidate C; do not bundle from mirrors or legacy parent files. |

Primary evidence links:

- TAALES: <https://www.linguisticanalysistools.org/taales.html>
- COCA downloads: <https://www.english-corpora.org/coca/help/download.asp>
- Open English WordNet: <https://github.com/globalwordnet/english-wordnet>
- TUBELEX: <https://github.com/naist-nlp/tubelex>
- NGSL-Spoken page reviewed: <https://www.newgeneralservicelist.org/ngsls>

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
