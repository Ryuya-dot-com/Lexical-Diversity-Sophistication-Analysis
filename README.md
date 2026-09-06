# ldfreq open contextual VPC/VID laboratory

Status: browser-local VPC/VID occurrence-and-sense review prototype; not a validated analyzer.

Canonical source: <https://github.com/Ryuya-dot-com/Lexical-Diversity-Sophistication-Analysis>

Public technical deployment: <https://ryuya-dot-com.github.io/Lexical-Diversity-Sophistication-Analysis/>

The product target is an independent, open-science application for identifying
English phrasal-verb and verbal-idiom occurrences and distinguishing their
contextual senses. The staged primary record keeps candidate generation,
members/gaps, occurrence status, category, idiomaticity, sense-inventory
coverage, contextual assignment, ambiguity, abstention, and out-of-inventory
uses separate. The current browser-local workflow is human-reviewed and is not
a validated automatic analyzer.

Word-list coverage, source-to-target recurrence, learner-text robustness,
reading comprehension, and eye-movement analysis are possible downstream uses
of the exported occurrence/sense records. They are not the core technology and
cannot validate its linguistic decisions.

The executable `mwe_contract.json` remains unchanged in this priority-only
revision because frozen audit artifacts pin its exact hash. Its next version
will be cut only with a benchmark-driven behavioral or schema change, not to
rewrite completed decision history.

The repository contains a public MWE review workflow, four admitted browser
profile projections, a versioned MWE contract, five project-authored M1–M5 gold
fixtures, and a reproducible projection of all 17 Open English
WordNet 2025 senses for `take in#v`. Dependency-free checks verify stable token
IDs, continuous and discontinuous members, gap exclusion, confirmed/rejected
states, separate form and sense lookups, contextual decision provenance, and
visible review numerators and denominators. The UI accepts a small researcher-
supplied TSV of surface-member alternatives, generates continuous or
discontinuous candidates, permits manual member/gap correction, records
idiomaticity, and—for confirmed `take in` occurrences—shows all 17 OEWN senses
for human assignment, ambiguity, or abstention. Exports preserve those review
states. The researcher must select the TUBELEX frequency profile, an explicit
NGSL first-1,000/2,000/full ranked-list condition, or an exact locally generated
Nation BNC/COCA Level 6 first-1K/2K word-family condition; OEWN separately
supplies confirmed multiword-verb form membership plus the bounded `take in`
sense inventory. This is transparent coding support, not automatic MWE
confirmation or WSD, a combined word/MWE score, or validation on learner data.

The M4 fixture explicitly represents the pronoun-object pattern `took it in`:
`took` and `in` are MWE members and `it` is a non-member gap. The same surface
sequence is confirmed in a comprehension context and rejected when `in the car`
is disambiguated by contrast with `on the bus`. This proves the record model,
not automatic parsing.

The first candidate-review scope is English verb-particle constructions
(VPCs), including contiguous and separated realizations such as `take in` and
`take it in`. Occurrence detection, form-inventory lookup, and contextual sense
assignment are different operations. One sense, jointly applicable senses,
unresolved named alternatives, abstention, semantic out-of-inventory, and
inventory ineligibility are separate states; none may silently fall back to the
most frequent sense or to the form-level result.
The [target-population contract](resources/target_population_contract.json) and
[standalone annotation guide](ANNOTATION_GUIDE.md) now fix
candidate-independent discovery, occurrence, exact member/gap spans,
tokenization exceptions, VPC.full/VPC.semi/VID routing, every current review
state, a compositional-versus-conventionalized idiomaticity decision tree,
contextual-sense and uncertainty rules, a loss-aware MAGPIE comparison
projection, and the M1–M5 decision path without
depending on the UI. The [synthetic occurrence/span/category
cases](annotations/training_cases.json) cover inflection,
particle movement, pronoun and NP gaps, embedded overlap, literal/spatial and
accidental negatives, and continuous/discontinuous spans. The full training
packet is now specified, but authorized training, an unexposed qualification
form, qualification results, and an independent pilot are still absent, so
this does not authorize production annotation.
The [synthetic hard-case bank](annotations/hard_case_bank.json) separately
covers nine prespecified boundary strata at least twice, with admissible routes,
rationales, and explicit redistribution permission rather than benchmark gold.
The [annotator training protocol](ANNOTATOR_TRAINING.md) stages teach-back,
practice, feedback, hard cases, and task-specific qualification without a
combined score; it uses only redistributable project-authored synthetic text.
The [annotation-platform decision](ANNOTATION_PLATFORM_DECISION.md)
provisionally selects an institutionally managed INCEpTION instance for later
independent first-pass work and keeps this app as an individual review tool. A
standard-library converter passes a synthetic UIMA CAS JSON format check for
gaps, multiple senses, OOI, and audit hashes; no instance or two-user workflow
has been approved or tested.

Phrasal verbs are not treated as all MWEs. M5 holds `spill the beans` constant
across an idiomatic use and a literal physical-spilling use. Its PARSEME `VID`
category, confirmed/rejected occurrence status, idiomaticity decision, and
fine-grained sense state remain separate rather than collapsing into a generic
`idiom` label. Light-verb constructions and non-verbal idioms remain outside
the executable contract.

The first external occurrence benchmark is a metadata-only offline profile for
STREUSLE 5.0. Its fixed English test projection contains 40 strong VPC/VID
occurrences, including 16 discontinuous occurrences. No corpus text or upstream
code is bundled. A deliberately weak contiguous train-lemma baseline obtains
exact-span F1 0.404762 and zero recall on discontinuous and train-unseen items.
The [frozen IR-221 comparator](resources/streusle_gap_dependency_baseline.json)
adds an ordered two-token gap and a direct
train-supported dependency-arc filter. On development data it recovers 8/14
discontinuous occurrences and improves exact-span F1 from 0.316832 for the
lemma-window ablation to 0.426667. Its optional audit records rule IDs, evidence
token numbers, and the accepted arc without sentence text. Unseen-type recall
remains zero.
The test projection and baseline are already exposed in this project, so they
are development evidence rather than an untouched blinded holdout.

The dated [core-evidence admission matrix](resources/mwe_core_evidence_admission_2026_09_03.json)
keeps STREUSLE occurrence/category evaluation, MAGPIE idiomaticity, and
contextual fine-sense evaluation separate.
The completed [MWEasWSD/SemCor reuse audit](resources/mweaswsd_semcor_reuse_audit_2026_09_03.json)
finds that SemCor can be reused with its notice, but rejects the added labels as
validation gold. They contain no category-confirmed VPC/VID rows, no independent
annotation or uncertainty evidence, five order-dependent conflicting duplicate
keys, only seven verb-proxy forms with observed positive sense contrasts, and
11/136 positive verb-proxy rows that do not map losslessly to OEWN 2025. Even
the five `take_in` candidates contain only one positive sense.

The bounded [standard-WSD MWE-sense audit](resources/wsd_mwe_sense_slice_audit_2026_09_03.json)
nevertheless finds a legitimate but tiny sense-only check in the original
Senseval/SemEval gold. After one-category STREUSLE type overlap, lossless OEWN
mapping, and candidate-polysemy filtering, 23 VPC rows/18 types remain: six
development and 17 fixed source-test rows. Their labels were inspected during
this audit, so they are not a blinded project holdout. This does not test member
detection, VID, `take in`, unseen forms, or uncertainty handling. It is a
conditional ranking smoke test, not target-wide validation. No contextual model
or human annotation is yet authorized.

The first-paper target is now a full-length article in *Language Resources and
Evaluation*. The
[submission-readiness audit](resources/lre_submission_readiness_2026_09_03.json)
blocks submission on five dimensions: benchmark scale/diversity, independence,
license/public availability, a frozen annotation guide, and comparative
baselines. A reproducible
[STREUSLE–OEWN coverage audit](resources/streusle_v5_oewn_2025_coverage_audit.json)
finds exact OEWN verb entries for 317/624 target occurrences and at least two
senses for 228, but only 45/319 VIDs match exactly and only 10 VIDs have two or
more senses. At type level, only 31/239 VIDs match; a fixed article/possessive-
slot normalization leaves 206 VID types unmatched. Exact inventory matching
would therefore select away most verbal idioms. The bounded
[Kaikki/Wiktionary VID audit](resources/streusle_v5_kaikki_vid_audit_2026_09_03.json)
adds exact verb-entry routes for only 60 of those 206 types. OEWN exact, simple
slot, and Kaikki exact routes together cover at most 93/239 VID types and
150/319 occurrences; only 28 types expose multiple inventory candidates. Just
5/99 Kaikki raw senses have a Wiktionary `senseid`; only one matched type has
IDs for every lexicalized sense, with no raw `id` or Wikidata ID. Wiktionary is
therefore useful candidate evidence but not direct benchmark gold. The frozen
[hybrid sense-inventory contract](resources/hybrid_sense_inventory_contract_2026_09_03.json)
now defines opaque project IDs, source-record fingerprints, merge/split rules,
layer-specific rights, and separate unresolved, ambiguous, abstained, and
out-of-inventory states. It also fixes a three-stage, no-free-search mapping pass
over all 146 residual VID types. The reproducible
[nonexact mapping queue](resources/sense_mapping_queue.json) and
[review guide](resources/sense_mapping_guide.md) now execute that bounded pass:
3 types have closed, unreviewed candidate sets and 143 retain
`unresolved/no_bounded_route`. All 146 exact misses remain in the denominator;
none is yet a mapped sense or evidence of true OOI. The raw source artifacts
remain local, no gloss or example is copied, and Kaikki links cannot enter the
formal inventory until the underlying dump hash and imported-content review are
recorded. This is not a completed inventory or runtime feature.

The [IR-131/132 candidate seed](resources/hybrid_sense_inventory_v1.json)
extends that ID registry with four already exposed training/development VPC
forms and five fixed VID pilot forms. It preserves all 67 pinned OEWN
candidates, CILI/ILI links, source-record fingerprints, verbatim gloss/example
provenance, and unmerged synset-member relations. IDs are reserved permanently,
but `senses` remains empty: every link is
`candidate_only/unreviewed`, so the file is neither contextual gold nor a
runtime inventory. Reproduce it with `python3
scripts/build_hybrid_sense_inventory.py OEWN_ZIP --prior
resources/hybrid_sense_inventory_v1.json --check
resources/hybrid_sense_inventory_v1.json`.

Before expert inventory review, the [IR-136 usage-pilot
builder](scripts/build_polysemy_usage_pilot.py) indexes all 54 matching
STREUSLE train/dev occurrences for the nine forms and creates a deterministic
51-pair connected scaffold. The [public
manifest](resources/polysemy_usage_pilot.json) excludes test, sentence text,
and semantic judgments. Pair raters see context without dictionary glosses;
provisional usage clusters are frozen before the [independent inventory-review
protocol](resources/inventory_review_protocol.json) maps the 67 OEWN candidates
to project senses. `cut short`, with one occurrence, remains contextually
underdetermined. Reproduce the scaffold with `python3
scripts/build_polysemy_usage_pilot.py --check`; the source audit and review
template still validate with `python3 scripts/check_inventory_reviews.py
--self-check`. No rating, review, cluster, or admitted sense exists yet, and
completed reviews and identity records stay outside this repository.

The [IR-132 VID population log](resources/inventory_population_log.json) freezes
a 14-type purposive STREUSLE-train pilot: 4 exact OEWN, 1 unique-slot OEWN, 4
exact Kaikki, 3 bounded nonexact, and 2 no-route types. It records 52 training
occurrences, including 21 discontinuous occurrences, without sentence or token
text. Every type has an eligibility state; 12/14 have a source route and 2/14
remain unresolved (`0.142857`). The five OEWN-routed VID types are now included
in the candidate seed, bringing it to 9 forms and 67 reserved candidate sense
IDs. Kaikki wording stays excluded pending its source-identity/rights gate, and
all formal `senses` arrays remain empty.
Reproduce the log with `python3 scripts/build_inventory_population_log.py
STREUSLE_CHECKOUT OEWN_ZIP --check resources/inventory_population_log.json`.

IR-133 adds a [Draft 2020-12 inventory
schema](resources/hybrid_sense_inventory.schema.json) and registry invariants.
Type IDs are checked across the IR-130 queue, IR-132 log, and inventory; project
sense IDs and source-sense identities must be unique. Candidate/formal records
carry explicit `supersedes`, `split_from`, `merged_from`, and `related_to`
arrays, currently empty. For a later source edition, regenerate with `--prior
OLD_INVENTORY`: existing source sense keys keep their project IDs, new senses
append IDs, and a disappeared prior sense fails until a lifecycle decision is
recorded.

IR-134 exercises that decision path with a wholly synthetic
[old/new lifecycle fixture](tests/fixtures/sense_inventory_versions/lifecycle_exercise.json)
and [governance procedure](resources/inventory_governance.md). A split
deprecates one ID and creates two, a merge deprecates two and creates one, a
deprecated source link does not erase an unchanged project sense, and a
training-only out-of-inventory case may prompt a new sense. Old annotations are
never rewritten: each receives an explicit migration status and remains tied to
its original inventory version. Any post-exposure boundary change must fork a
new major benchmark version rather than improve the same test.

The [IR-135 coverage audit](resources/hybrid_inventory_coverage_v2.json)
recounts every 624 STREUSLE target occurrence and all 389 types, plus all 52
occurrences/14 types in the IR-132 VID pilot. The current nine-form candidate
seed reaches 57 occurrences and 9 types, including 21/319 VID occurrences and
20/188 discontinuous occurrences, but it has zero admitted senses and zero
contextual-adequacy reviews. Candidate-only denominators are prohibited; OOI is
reported as unassessed rather than zero prevalence. The audit therefore holds
all contextual-sense claims. Reproduce it with `python3
scripts/audit_hybrid_inventory_coverage.py STREUSLE_CHECKOUT --check
resources/hybrid_inventory_coverage_v2.json`.

The closest existing user-text profiling applications found in the current
review are Masaki Eguchi's Multi-Word Units Profiler and Lextutor Phrase
Profiler. The former uses n-gram and dependency candidates to highlight entries
from several research-based MWU lists; the latter matches text against selected
phrase/collocation lists. FLAT/PARSEME is the closest collaborative MWE
annotation workflow. This project will reuse those precedents instead of
rebuilding them. Its distinct job is the staged, correctable link from a
continuous or discontinuous candidate to occurrence/category/idiomaticity and
then to an uncertainty-bearing contextual sense; coverage is one downstream
consumer of that record.

Prior art is reviewed by task rather than by product name: discovery,
list-conditioned profiling, occurrence identification, annotation, contextual
idiomaticity, fine-grained sense assignment, L2 pedagogical priority, and
coverage reporting. STREUSLE 5.0 is the pinned English occurrence benchmark;
PARSEME 2.0 remains a multilingual method/format comparator because its fixed
production training release has no English directory. Neither is an automatic
runtime dependency.

These fixed scenarios are the method-audit surface. The initial research
workspace now analyzes one passage, a paired transformation, or two independent
texts entirely inside the browser. It can also describe researcher-declared
non-empty line units within one text while keeping the pooled result separate,
or describe 2–100 researcher-identified documents from a pasted JSON array.
Automatic sentence splitting, group inference, length curves, validated MWE/VPC
identification, automatic sense assignment, MWE frequency, and simultaneous
reference-profile comparison are not implemented. The browser performs only
exact, local lookup against the explicitly selected word profile and the named
OEWN projections; it does not query an external lexical service.

The target is a free, reproducible open-science tool for L2 vocabulary
researchers. The canonical core remains downloadable and auditable. A server
or server-side resource store is admitted only when an MWE/VPC function cannot
be delivered responsibly in the browser and the exact resource license permits
that use; a database is not treated as a substitute for permission.

## Capabilities and non-capabilities

The prototype can generate VPC/VID form candidates from researcher-supplied
surface patterns, preserve discontinuous members and intervening gaps, accept
manual candidates, record confirmed/rejected/unresolved decisions with notes,
record separate idiomaticity decisions, and export occurrence CSV plus
metadata-only method JSON. For confirmed `take in` occurrences, it also records
a human-selected OEWN sense, multiple plausible senses, abstention, or an
unassigned state. The two starter patterns are functional examples, not an
inventory. A separate local workspace JSON preserves one text, its pattern TSV,
review decisions, source-text SHA-256, and exact runtime-resource identities for
later continuation. A named document-set JSON wraps 1–20 of those independently
validated workspaces without pooling them. Neither format is the privacy-reduced
publication export. Once a review is created or restored, its source text,
pattern, authorization, profile controls, and extraction button remain locked
until the explicit reset action. Repeated form submission also refuses to
replace an existing review, including one restored from a saved file.
The UI separates result exports from raw-content resume files. Method JSON has
no source-text field or word-item table, but retains expressions and decision
notes, including any text quoted in those notes; it is not automatically safe
to share. Adding a document to a set keeps it in page memory only; a separate
download is required for a durable file, and the browser cannot verify that the
user completed that download.
Recording a decision updates only the affected review controls and summary,
preserving drafts in other occurrences and manual token selections. Same-status
note updates also preserve the other review sections in that occurrence. A
change of occurrence status rebuilds that occurrence's controls, with a
confirmation before it discards dependent drafts or removes recorded decisions.
Candidate deletion and returning occurrence, idiomaticity, or sense judgments
to an unresolved/unassessed state also ask before clearing work; cancellation
preserves the model, controls, and save state. Idiomaticity and contextual sense
are independent: after occurrence confirmation, available sense controls stay
visible regardless of idiomaticity status and are not rebuilt by its edits.
Resetting either of these two judgments retains the other. Drafts
remain page-local and are not exported until explicitly recorded; opening a
different document starts from that document's saved decisions.
Pending occurrence notes, idiomaticity/sense edits, and unfinished manual
candidates are listed separately from unresolved judgments. Judgment-bearing
CSV/JSON downloads and document-set saves stop and return to the relevant field
until those edits are recorded or reverted; word-coverage CSV is independent.
Draft checks never assign a judgment or change the export format. Explicit
resets ask before clearing an input or review; cancellation preserves both
model and form state. Page-exit cleanup skips these dialogs, so this is not a
guarantee against closing a tab or browser. Downloads and the separate in-memory
document set are not erased by a single-document reset.
Asynchronous MWE saves and restores use a snapshot of the validated input.
Editing either MWE form, confirming a reset/clear, extracting a new review, or
starting another import invalidates older unfinished operations. Late results
cannot overwrite the current review, re-create a cleared set, mark newer edits
as saved, or start an outdated download. Independent exports may run together
when the inputs are unchanged. Retry a canceled operation after editing; an
already-started browser download cannot be recalled.
Documents opened from a set keep a fixed ID, just like newly added documents;
selecting another entry does not change the active review. A persistent status
distinguishes the active document, updates needed in the in-memory set, and
unrecorded edits, without claiming a completed file download. Document-name
edits require an update before exporting the set. Accepted IDs and names are
shown using the same trimmed values as the saved records. To open another
document, retain any needed changes first, then explicitly clear the current
review; the set itself remains in memory.
Resume-file errors give Japanese retry guidance, including the correct input
for a single-document versus document-set file. Invalid JSON, incompatible
records, and sets with an invalid member are rejected without applying them;
the app does not repair or rewrite the source file. A failed local BNC/COCA
import retains any previously verified profile. Replacement happens only after
the new file passes the existing size, hash, structure, and identity checks.

For the same text, the prototype reports TUBELEX word-token/type membership
with corpus-frequency evidence, NGSL ranked-list coverage, or locally imported
Nation BNC/COCA word-family coverage at a declared cutoff. Ranked output
distinguishes source-listed forms above the cutoff
from absent forms and retains both candidate heads for the five declared
homographs. After a researcher confirms an occurrence, it reports OEWN
multiword-verb form membership by occurrence and distinct form. The channels
retain different units and denominators and are never averaged.

It can also inspect three synthetic contrasts, including a one-sentence versus
seven-sentence punctuation contrast. In the browser it can describe one text,
researcher-declared non-empty lines, paired or independent texts, and 2–100
documents. It reports tokens, types, simple TTR, and hapax types under one fixed
English ASCII tokenizer, and exports method metadata and SHA-256 identifiers
without raw text. The source, fixtures, contract, citations, rights terms, and
tests are open for audit.
With a separately obtained STREUSLE 5.0 checkout, the offline checker also
verifies exact train/dev/test artifacts and reproduces the declared VPC/VID
surface and gap/dependency baselines.

It can surface a declared `take in` pattern, including `take it in`, as a
candidate, but it cannot confirm that candidate as a VPC or distinguish it
automatically from a free or directional combination. After human confirmation,
the reviewer can inspect and code all 17 OEWN candidate senses without a default
selection. The app does not disambiguate them automatically, and OEWN supplies
no contextual gold choice, frequency, or L2 pedagogical ranking. Human review
remains part of the measurement method.

The selectable bundled word profiles are a deterministic 410,400-form TUBELEX
ASCII frequency projection and a 10,114-form NGSL 1.2 ranked-list projection.
An exact 13,223-form Nation BNC/COCA Level 6 first-2K profile can be generated
and imported locally but is never bundled. All three use
NFKC-normalized ASCII letter sequences, so apostrophes and hyphens are
boundaries; their denominator may differ from the MWE-review tokenizer. NGSL
first 1K/2K means its own head ranks, not Nation BNC/COCA word-family levels, and
its research forms explicitly collapse meaning senses. The active MWE-form
profile is a deterministic 2,847-form projection of OEWN 2025 verb
entries containing multiple ASCII word members. It supplies lexicon membership
and an inventory sense count, not occurrence truth, MWE frequency, category, or
contextual sense. A separate `take in#v` projection supplies candidate glosses
and examples for manual review; it is not a general dictionary or sense-
frequency profile. A future exact Leipzig package remains a written-register
contrast; STREUSLE/PARSEME remain evaluation data rather than frequency norms.

It also cannot assess proficiency, CEFR, writing quality, authorship, causal
effects, or population differences; measure TAALES equivalence; independently
verify input rights; guarantee device-level erasure; or reproduce an analysis
from a metadata-only export when the exact source text was not separately
preserved.

## Run

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000>. Run the dependency-free checks with:

```bash
python3 -m unittest discover -s tests -v
node tests/verify_contract.mjs
python3 scripts/evaluate_mwe_predictions.py tests/fixtures/mwe_predictions_surface_baseline.json --check
python3 scripts/check_streusle_v5.py --self-check
```

To reproduce the prose-free Simple English Wikipedia Route 2 candidate queue,
download the exact dated dump recorded in
[`resources/simplewiki_gate1_route2_design.json`](resources/simplewiki_gate1_route2_design.json),
keep it outside Git, and run:

```bash
python3 scripts/screen_simplewiki_route2.py PATH_TO_DUMP --check
```

The rendered-boundary screen then follows each frozen queue until the first 20
mechanically eligible pages per target. It uses the official MediaWiki Parse
API, caches raw responses outside Git, verifies source wikitext against the dump
hashes, and publishes no article prose:

```bash
python3 scripts/screen_simplewiki_route2_rendered.py PATH_TO_LOCAL_BNC_COCA_PROFILE
python3 scripts/screen_simplewiki_route2_rendered.py PATH_TO_LOCAL_BNC_COCA_PROFILE --check
```

The second command is cache-only. Old-revision source identity is reproducible;
rendered hashes also pin the retrieval snapshot because templates and parser
state may later change.

To reproduce the TUBELEX and OEWN-form profiles from the exact source assets
recorded in [`RIGHTS.md`](RIGHTS.md):

```bash
python3 scripts/build_reference_profiles.py PATH_TO_TUBELEX_XZ PATH_TO_OEWN_ZIP --check
```

To reproduce the NGSL ranked-list projection from the two pinned official files:

```bash
python3 scripts/build_ngsl_profile.py PATH_TO_NGSL_STATS PATH_TO_NGSL_RESEARCH_FORMS --check
```

To generate the exact local-only Nation BNC/COCA first-2K profile from a
lawfully obtained official v1.0.0 zip, then select that JSON in the Web app:

```bash
python3 scripts/build_bnc_coca_profile.py PATH_TO_BNC_COCA_ZIP OUTPUT.json
python3 scripts/build_bnc_coca_profile.py --check PATH_TO_BNC_COCA_ZIP OUTPUT.json
```

The builder reads only `basewrd1.txt` and `basewrd2.txt`, excludes the four
special lists, and never runs the bundled Windows executable. The app accepts
only the reviewed 366,120-byte output with SHA-256
`ebd06548187988eb1a61ab967cc39c01461023043ee7aef427606e5bf508f138`.

To reproduce the admitted OEWN subset, download the pinned 2025 JSON release
asset recorded in [`RIGHTS.md`](RIGHTS.md), then run:

```bash
python3 scripts/extract_oewn_take_in.py PATH_TO_ZIP --check resources/oewn_take_in_2025.json
```

To reproduce the external occurrence baseline without copying the corpus into
this repository:

```bash
git clone --depth 1 --branch v5.0 https://github.com/nert-nlp/streusle.git PATH
python3 scripts/check_streusle_v5.py PATH --check --surface-baseline --gap-dependency-baseline
```

To reproduce the aggregate-only MWEasWSD/SemCor audit from the six exact
external artifacts pinned in its audit record:

```bash
python3 scripts/audit_mweaswsd_semcor.py PATH_TO_MANUAL_JSONL PATH_TO_AUGMENTED_JSONL PATH_TO_OEWN_ZIP PATH_TO_CILI_PWN30_SENSE_MAP PATH_TO_CILI_PWN30_ILI_MAP PATH_TO_SEMCOR_TAR_GZ --check resources/mweaswsd_semcor_reuse_audit_2026_09_03.json
```

The checker emits no SemCor sentences. It also prevents an exact-looking
WordNet sense key from passing silently when its CILI/OEWN concept changed.

To reproduce the aggregate-only standard-WSD multiword-verb audit from the
seven exact external artifacts pinned in its record:

```bash
python3 scripts/audit_wsd_mwe_sense_slice.py PATH_TO_WSD_FRAMEWORK_ZIP PATH_TO_STREUSLE_TRAIN_JSON PATH_TO_STREUSLE_DEV_JSON PATH_TO_STREUSLE_TEST_JSON PATH_TO_OEWN_ZIP PATH_TO_CILI_PWN30_SENSE_MAP PATH_TO_CILI_PWN30_ILI_MAP --check resources/wsd_mwe_sense_slice_audit_2026_09_03.json
```

This checker also emits no source sentences. The external WSD archive is not
bundled because its exact zip contains no explicit redistribution license.

Python is used for offline resource preparation and model-independent evaluation,
and remains outside the app runtime. The included surface-list negative control
evaluates decisions for supplied candidates only; it is not candidate generation,
span detection, or a trained model. The STREUSLE checker is a separate offline
occurrence benchmark and never loads research text into the Web app. Use localhost or HTTPS
because the reproducibility hash uses the native Web Crypto API.

Original repository material is available under either MIT or CC BY 4.0 at the
recipient's choice; see [`LICENSE.md`](LICENSE.md). TUBELEX data retain the
included BSD-3-Clause notice. The NGSL projection retains CC BY-SA 4.0 and its
[attribution/modification notice](resources/NGSL_NOTICE.md). OEWN projections
are separately licensed under OEWN CC BY 4.0 and the underlying WordNet
License. Attribution and source terms are recorded in each profile and
[`RIGHTS.md`](RIGHTS.md).

Current unreleased changes and verification gaps are recorded in
[`CHANGELOG.md`](CHANGELOG.md). No version, DOI, or public-release claim has been
assigned to this technical probe. Git text content is normalized to LF for a
stable cross-platform source archive.

Human-data work is governed separately by [`GOVERNANCE.md`](GOVERNANCE.md) and
the current [`ethics determination record`](resources/ethics_determination.md).
Static development, public-source preparation, sampling, and synthetic platform
checks may proceed. Later independent annotation requires a documented work
relationship, payment/rights terms, and secure data handling; ethics review is
required only if the arrangement is human-participant research. Intended-user
research and participant-level secondary use remain separate conditional gates.

## Scope boundary

- Analysis scenarios contain only reviewed, project-authored synthetic text.
  The separately licensed OEWN projection contains source definitions and
  examples for one lexical entry and is not user or learner text.
- The MWE path accepts researcher-authorized text, including appropriately
  governed learner data, only after an explicit authorization/ethics
  attestation. The legacy basic workspace remains restricted to synthetic or
  rights-cleared published material.
- No network text upload, URL fetch, cookie, analytics, request-content log, or
  remote model. Explicitly selected workspace and BNC/COCA files are read only
  in browser memory. The app does not independently establish consent, anonymization,
  institutional approval, or lawful processing.
- The app writes input only to the live form, requests clearing on page exit,
  and provides a reset control. It cannot guarantee erasure from browser/device
  memory, history, downloaded workspace files, or backups. Method JSON contains
  SHA-256 and provenance without a source-text field, but MWE expressions and
  decision notes (including quoted text) remain; the explicitly requested resume
  JSON and document-set JSON contain raw text, pattern TSV, labels, and review
  notes. Timestamps come from the client clock; neither a timestamp nor hash is a
  signature, trusted time proof, or proof of authorship. The descriptive-workspace method export also carries
  the selected relationship meaning, construct claim,
  excluded inferences, limitations, and meanings of its active warning codes.
- Multi-document input uses the browser's native JSON parser, preserves one row
  per declared document, and rejects the entire batch rather than silently
  dropping invalid items. It does not pool, rank, infer groups, or assume rows
  are independent participants. The raw JSON is capped before parsing, and
  unpaired Unicode surrogates are rejected before UTF-8 hashing.
- MWE document-set import likewise validates every embedded workspace, source-
  text SHA-256, contract, profile identity, and occurrence before replacing the
  in-memory set. It provides no autosave, database, collaboration, aggregation,
  or evidence that the documents form a population sample.
- Raw counts remain descriptive. Higher values do not mean better writing,
  greater lexical knowledge, proficiency, or CEFR level.
- Formula names do not imply numerical compatibility with TAALES, TAALED, or
  another tool.
- Resource-dependent measures remain blocked until the artifact-level gate in
  [`RIGHTS.md`](RIGHTS.md) passes. The active TUBELEX frequency, NGSL ranked-
  list, and OEWN MWE-form profiles pass that gate only for their declared
  channels; the smaller `take in#v` projection passes only for local human
  candidate-sense review and export, not automatic WSD or a general sense-
  coverage claim. The Nation BNC/COCA route is local-only: the user supplies the
  exact derived file, its runtime hash is exported, and neither its source nor
  projection is distributed by this repository.
  Open resources are versioned downloadable artifacts rather than hidden
  server data, and database storage never makes an unclear license clear.
- A reference result always names one completed resource profile. The app must
  not silently pool registers, substitute a lexicon for a frequency corpus, or
  present TUBELEX, NGSL, Leipzig, OEWN, STREUSLE, or PARSEME as a universal norm.

## Method evidence

The machine-readable
[claim–evidence–artifact map](resources/claim_evidence_map.json) records the
current wording ceiling, narrowly scoped evidence, required release artifacts,
and prohibited inferences for each construct, resource, technical,
response-process, and downstream claim. The append-only
[decision log](resources/decision_log.json) records changes and prevents rule
updates after test exposure from being applied retroactively.

The pre-acquisition [benchmark source decision](resources/benchmark_source_decision_2026_09_04.json)
selects English Wikipedia namespace-0 article revisions and a CC BY-SA 4.0
public-text plus reconstruction route. It releases no source or benchmark and
does not lift the current availability claim gate.
The [release-layer manifest](resources/release_layer_manifest.json) resolves
every current public file to its source, license, notice, and redistribution
state while excluding unreviewed future benchmark or model files.
The boundary check pins the exact public path set as well as its count, so
same-count file replacements require release-scope review too. This path hash
does not verify file contents or grant redistribution rights. Both `internal/`
and `research_data/` are Git-ignored and excluded from the Jekyll Pages build;
tests also reject their inclusion in the public file set.
The [source manifest](resources/source_manifest.json) freezes the completed
2026-09-01 dump metadata, while the
[preprocessing contract](resources/preprocessing_contract.json), synthetic
probe, and [checker](scripts/reconstruct_benchmark.py) preserve exact text,
document/token IDs, and character/byte offsets. No dump content was downloaded,
so this does not establish benchmark availability.
The [sampling-frame contract](resources/sampling_frame.json) and
[standard-library queue builder](scripts/sample_benchmark_documents.py) freeze
content-neutral eligibility, three document-length strata, a seed, deterministic
random-priority order, and same-stratum replacements. They contain only protocol
and synthetic test rows: source rows, the IR-127 allocation, selected documents,
and every target-derived field remain absent.
The [evaluation-strata contract](resources/evaluation_strata.json) fixes the
claim denominators, document and canonical-form clusters, design weighting, and
small-stratum withholding rule. The `benchmark_mwe_evaluation` section of
[`metric_contract.json`](metric_contract.json) separately freezes the IR-125
candidate, span/token, category, idiomaticity, inventory, sense, abstention,
burden, conditional calibration, and selective-prediction formulas with their
input schemas, denominators, undefined states, and document bootstrap unit.
The [bootstrap evaluator](scripts/bootstrap_evaluation.py) now implements the
IR-126 fixed-seed, sampling-length-stratified document-cluster percentile
interval, global canonical-type sensitivity, and paired same-resample system
difference. Overall and requested frozen single-axis strata use the same
function; degenerate or undefined resamples fall back to point-estimate-only
output.
Every interval remains descriptive until IR-127 freezes a feasible allocation,
cluster-count, and precision threshold.
The [pre-data precision plan](resources/precision_plan.json) and
[allocation simulator](scripts/simulate_benchmark_precision.py) freeze the .05
overall/.10 single-stratum gates and fail closed on unresolved inputs, sparse
clusters, target-conditioned selection, or an empty frozen split. They report
no sample size, and all observed inputs remain null. The IR-121/IR-147 design
dependency is now prospectively resolved in the
[planning-pilot addendum](resources/planning_pilot_addendum.json): IR-147 uses
training material only, while a separate budget-frozen target-blind Wikipedia
prefix supplies later planning inputs and can never enter the sealed test. The
addendum selects no document and does not authorize human work.
The [split protocol](resources/split_protocol.json) freezes a separate hash and
document-level 20/10/20/50 guide-training, pilot, development, and sealed-test
allocation. The [exposure ledger](resources/leakage_ledger.json) classifies all
currently known external-resource, prior-material, dictionary, and synthetic-
result exposure in the repository and requires unknown access to fail as
exposed. No contextual/probabilistic model experiment or project test exists,
and no custodian has yet been appointed.
The pre-data [benchmark card](BENCHMARK_CARD.md) and
[data statement](DATA_STATEMENT.md) keep source, sampling, annotation, target,
and evaluation populations separate and mark every release-time unknown.

The contract cites [Fergadiotis, Wright, and Green
(2015)](https://doi.org/10.1044/2015_JSLHR-L-14-0280) for sample-length
confounding and validity cautions, and [Zenker and Kyle
(2021)](https://doi.org/10.1016/j.asw.2020.100505) for the simple-TTR definition
and length behavior observed in their L2 argumentative-essay sample. These
sources constrain interpretation; they do not validate this app or justify
population, proficiency, or causal inference.

The scenario design, workspace limits, non-inferences, publication conditions,
and representative-user check are authoritative in [`ROADMAP.md`](ROADMAP.md).
Exact tokenizer, input, retention, and export behavior is frozen in
[`metric_contract.json`](metric_contract.json); scenario provenance and expected
values are in [`samples.json`](samples.json).

## Release status

Do not present this public technical deployment as a research-validated product
or formal release. Before assigning a version or recommending research use,
verify the static app in real browsers and assistive technology, and archive a
citable release containing contracts, fixtures, tests, notices, and checksums.
