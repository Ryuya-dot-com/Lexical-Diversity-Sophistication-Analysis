# Gate 1 development-material admission dossier

- Status: downstream application-material dossier; VOA, Simple English
  Wikipedia, and the first Project Gutenberg frame are stopped without final
  passage admission
- Reviewed: 2026-09-03
- Active work package: none in this dossier. Core VPC/VID occurrence-and-sense
  benchmark admission now precedes any TECO outcome join, replacement open-text
  frame, coverage study, learner recruitment, or application-driven app expansion

## Provisional domain

The initial general-science screen failed on technical load and sense
variation, the frozen VOA learner-directed frame failed on recurrence, and the
Simple English Wikipedia route was stopped because its topic filter violated
content neutrality. Those records remain development evidence, not the current
domain.

This dossier preserves two deliberately separate application domains. TECO
supplies the exact Eiken-derived expository passages already read by Japanese
L2 participants; Project Gutenberg supplies openly releasable natural prose for
app, annotation, and genre-transfer evidence. Neither domain represents
universal English.
TECO's participant outcomes do not transfer to Gutenberg texts, and older
literary Gutenberg prose does not represent present-day L2 examination or
textbook reading.

## Source-class screen

| Source class | Rights/provenance position | Method fit | Decision |
|---|---|---|---|
| eLife article digests | eLife's current terms state that journal articles and related content are CC BY unless otherwise noted; articles have DOI/version records, and official versioned JATS XML is available | Modern intact plain-language science passages, but the five exact candidates are technically dense and repeat the same broad senses | **Five candidates rejected from the primary set; retain only as possible technical-domain stress texts** |
| VOA Learning English articles | Current VOA terms identify exclusively VOA-produced text as public domain with credit, while excluding AP, Reuters, AFP, and other third-party material; pages may be silently corrected, so exact bytes must be pinned | Written for L2 readers and offers naturally occurring cross-sense repetitions | **Stopped historical candidate frame; reconsider only for a named downstream application and only when the article credit shows VOA production** |
| Simple English Wikipedia text | Current terms permit reuse under the applicable open license with attribution, revision-history credit, share-alike, and modification notice | Broad topics and possible sense variation; collaborative revision and article structure require a dated dump, fixed rendered-prose rule, and page-level review | **Selected only for the frozen Route 2 target-conditioned development frame; not a representative corpus sample** |
| OpenStax textbooks | Current book pages use artifact-specific CC BY-NC-SA terms and may include an additional generative-AI-use statement | Pedagogically coherent but longer, textbook-specific, and licensing/workflow conditions need artifact-by-artifact review | Hold; do not ingest or redistribute in this workflow without clarification |
| Project Gutenberg | Most works are unrestricted in the United States, but Project Gutenberg requires non-US users to check local status; bulk acquisition must use an official catalog/mirror rather than the human-facing site | Stable natural prose; older literary language creates explicit diachronic and genre limits | **First target-blind frame stopped below its adult-stratum goal; no replacement is active** |

Open access is not enough: every retained passage needs its own copyright line,
license, author/source attribution, version/date, DOI or revision ID, retrieval
route, exact SHA-256, modification record, and release decision. Images,
captions, references, and third-party material are excluded by default.

## Existing-data-first boundary

Natural text alone and participant data alone solve different problems. For a
later eye-movement application, the relevant source is the text actually read
by an existing participant: TECO first, with MECO-L2 or CELER inspected only
for a named variable TECO lacks.
Gutenberg can support a fully shareable natural-text workflow, but no inference
about reading behavior or knowledge follows because nobody in those corpora read
the selected Gutenberg units.

No new L2 readers will be recruited during material admission. Recruitment may
be reconsidered only after the existing-data analysis shows that the retained
claim requires the same reader's contextual component-word knowledge,
contextual MWE-sense knowledge, and global passage comprehension, and that no
admitted dataset contains those measures. Intended-researcher usability work is
a separate later population and does not repair missing learner evidence.

### TECO outcome-blind MWE desk triage

All 285 OEWN machine leads in the 30 local TECO passages were read before any
eye, answer, or proficiency file was opened. The preliminary single-project
triage retains 39 automatic leads as plausible VPC/VID occurrences, gives four
automatic leads explicit boundary or unresolved decisions, and provisionally
does not retain the other 242. A bounded missed-lead pass adds four plausible
occurrences and preserves ten hard cases for later adjudication. The combined
plausible set is 43 occurrences across 32 forms: 33 VPC.full, 7 VPC.semi, and 3
VID. It is development evidence, not independent gold or a prevalence estimate.

The screen's three `take in` leads are all contextual false spans; TECO therefore
does not supply a true `take in` occurrence. In the overlapping `take part in`
case, PARSEME's open-slot rule supports `take part` as the provisional VID and
keeps `in` outside the member ROI. The same rule keeps `with` outside nested
`catch up`. The second pass recovered `join in`, `think so`, `pass down`, and
the STREUSLE-attested VID `go out of business`; the last crosses an inferred
line, as does one retained `throw away`. `carry ... around`, `look forward to`,
`get used to`, `take turns`, `have something to do with`, and the `put ... under
the spotlight` boundary remain among the explicitly unresolved cases.

The prose-free record is
[`resources/teco_v1_1_mwe_desk_triage.json`](resources/teco_v1_1_mwe_desk_triage.json).
It retains stable text/item positions and line flags but no passage prose or
surface tokens. No outcome analysis is permitted until the plausible and hard-
case rows have later author confirmation, independent annotation, and recorded
adjudication. This TECO-specific work is deferred until the core occurrence and
sense method has independent technical evidence; it no longer defines the next
task.

The official weekly Project Gutenberg CSV catalog was retrieved through the
documented offline feed on 2026-09-02: 21,196,613 bytes, 79,288 metadata rows,
SHA-256
`253f1b2d9aead75fec8ddb732c72a2fab5cd7db2f37745ef20760254f0666c4b`.
The standard-library frame builder verified that exact local artifact and found
22,275 metadata-eligible English fiction records after excluding explicit
translations and non-prose labels: 16,122 adult/unspecified and 6,153 explicitly
juvenile records. It then hash-ranked and froze 40 candidates per stratum. No
ebook was downloaded and no MWE search was run.

Each stratum stops after ten admitted units or 40 documented screens. A unit is
the first unambiguous complete chapter, short story, or standalone body with
300–2,000 project-tokenizer words; long units are not cut and later units cannot
be chosen for lexical yield. Rights review precedes access because Project
Gutenberg makes no non-US assurance. Japanese review must address the ordinary
term, transition rules, credited contributors/translators, foreign works, and
wartime addition rather than applying a death-year shortcut. Content or MWE
presence cannot exclude or reorder a work. The metadata-only frozen frame is
[`resources/gutenberg_2026_08_30_prose_frame.json`](resources/gutenberg_2026_08_30_prose_frame.json);
the catalog and all ebook text remain unbundled.

The first metadata-only rights triage now covers the fixed ranks 1–10 in both
strata. Thirteen rows may proceed only to an ebook-internal notice and textual-
contributor check; five are held because Japanese protection is likely active,
and two are held because creator identity or death remains unresolved. These
are not public-domain declarations. The calculation respects the 2018 non-
revival rule and the wartime-addition transition: an old 50-year term that had
already expired is not mechanically revived, while a term still running because
of wartime addition receives the extension. Images and illustration-specific
text are excluded, so an illustrator is not silently treated as a co-author of
the prose. Rights-oriented Web results incidentally exposed short snippets or
front matter for five already frozen works; this is disclosed in the ledger,
and cannot change queue order or the first-intact-unit rule. No ebook file was
acquired, no unit was admitted, and no MWE search was run. The triage is
[`resources/gutenberg_2026_08_30_rights_triage_batch1.json`](resources/gutenberg_2026_08_30_rights_triage_batch1.json).
Because a public Web app is globally reachable, the United States and Japanese
checks authorize neither bundling nor worldwide serving. Any locally acquired
passage stays unbundled until a release territory or globally valid permission
is fixed.

The 13 notice-check files were then retrieved on 2026-09-03 from the official
mirror listing's `gutenberg.pglaf.org` cache into ignored local storage. The
pre-body audit pins each URL, byte size, mirror-derived modification time, and
SHA-256. Every file contains the standard United States/non-US warning, start
and end boundaries, and full license footer. Only three preambles identify an
original publication; ten require title/copyright-page review after the start
marker, and `Taken or left` also has no preamble Credits field. These are
unresolved edition/contributor checks, not exclusion reasons. The committed
audit contains no prose:
[`resources/gutenberg_2026_08_30_notice_audit_batch1.json`](resources/gutenberg_2026_08_30_notice_audit_batch1.json).

Front-matter review of all 13 exact files found no additional retained
translator, editor, adapter, or introducer. Eight have a usable print-
publication statement; five remain incomplete. Five files explicitly disclose
transcription or normalization choices. The analysis source is therefore the
SHA-256-pinned electronic artifact, not a reconstructed print edition: it may
support version-conditioned lexical/MWE analysis after unit admission, but not
diplomatic-edition or unsupported historical-orthography claims. Locating the
first-unit boundary exposed limited post-boundary material in nine files; the
exposures are recorded, no lexical/MWE search occurred, and the already frozen
order and first-unit rule prevent them from changing selection. All 13 are
ready only for mechanical first-unit measurement; none is admitted. The
prose-free record is
[`resources/gutenberg_2026_08_30_front_matter_review_batch1.json`](resources/gutenberg_2026_08_30_front_matter_review_batch1.json).

The first-unit gate then fixed the opening heading through the line before the
next sibling heading, retained exact source bytes, and removed only complete
bracketed illustration blocks. Ten first units exceed the frozen 2,000-token
maximum. Two pass mechanically: Project Gutenberg 25885 at 1,898 project
tokens and 73331 at 1,517. Project Gutenberg 53088 is 1,587 tokens but its
opening `INTRODUCTORY` section is not unambiguously one of the prespecified
chapter, short-story, or standalone-body types, so it is excluded rather than
silently treating Chapter I as the first unit. This low 2/13 yield is a design
warning: the intact-unit/length rule selects for short chapter structures and
may not reach ten units per stratum within 40 screens. The rule is not relaxed
after observing lengths; fixed-order screening continues and a shortfall at 40
requires a new design. Both passing texts remain local and unbundled because a
mechanical pass is not global release clearance or final admission. The record
contains boundaries, counts, and hashes but no prose:
[`resources/gutenberg_2026_08_30_unit_gate_batch1.json`](resources/gutenberg_2026_08_30_unit_gate_batch1.json).

The fixed ranks 11–20 per stratum were then screened without acquiring another
ebook. Seventeen of 20 may proceed only to local notice/front-matter review;
Kris Neville remains protected, while Mari Wolf and Frank Walton lack the
identity/death evidence needed for a named-author calculation. The screen does
not equate every missing death year with an automatic hold: official Japanese
guidance provides a publication-based term for anonymous or pseudonymous
works. Work-specific evidence therefore lets the 1926 `Roy Rockwood` and 1911
`Quincy Allen` publications advance without claiming to identify their human
writers. An unexplained author name is not assumed to be a pseudonym. This
metadata triage is not global release clearance and contains no source prose:
[`resources/gutenberg_2026_08_30_rights_triage_batch2.json`](resources/gutenberg_2026_08_30_rights_triage_batch2.json).

The 17 allowed files were then retrieved into ignored local storage and pinned
by exact URL, byte size, mirror-derived modification time, and SHA-256. All 17
contain the standard US/non-US warning, ebook boundaries, and full license;
three preambles identify an original publication and all include Credits. The
audit decoded only the pre-START notice for review and read complete files only
mechanically for hashes and markers. It selected no unit, ran no MWE search,
and authorizes no public serving:
[`resources/gutenberg_2026_08_30_notice_audit_batch2.json`](resources/gutenberg_2026_08_30_notice_audit_batch2.json).

Front-matter review leaves 16 files ready for the unchanged first-unit gate and
holds Project Gutenberg 6655. Five source-authored prefaces, introductions, or
reader addresses are the first retained prose section and cannot be skipped to
reach a chapter; two electronic-producer synopses are excluded as paratext.
Ten files have a usable print-publication statement, seven remain incomplete,
and six contain explicit transcriber notes. The held file, `Tom Slade`, says it
was adapted from a photoplay but omits the film's three story credits recorded
by the American Film Institute, so its textual dependency and release basis
remain unresolved. This provenance hold is independent of topic and MWE yield.
The prose-free review is
[`resources/gutenberg_2026_08_30_front_matter_review_batch2.json`](resources/gutenberg_2026_08_30_front_matter_review_batch2.json).

The unchanged mechanical gate evaluates only those 16 ready files. One unit
passes: Project Gutenberg 70572, a 1,743-token juvenile chapter. Nine intact
chapters or short stories exceed 2,000 tokens. Six first retained sections are
excluded because `part`, `preface`, `introduction`, and `reader_address` were
not frozen as allowed unit types; this includes two otherwise in-range
sections. Project Gutenberg 68552 is correctly measured as the whole 7,740-
token short story rather than only its opening numbered section. Combined with
batch 1, the frame has only three mechanical passes from 29 gated files—one
adult/unspecified and two juvenile—so the strong short-chapter selection and
stratum imbalance are now observed limitations, not reasons to alter the rule.
No pass is admitted or served, no prose is committed, and no target or MWE
search has run. Continue the frozen queue:
[`resources/gutenberg_2026_08_30_unit_gate_batch2.json`](resources/gutenberg_2026_08_30_unit_gate_batch2.json).

Ranks 21–30 per stratum were then screened from metadata only. Fifteen of 20
may proceed to local notice review. Robert Emmett McDowell and H. L. Gold have
active ordinary Japanese terms; Thornton W. Burgess's 1916 United States work
remained protected at the 2018 extension because of the 3,794-day wartime
addition. Amelia E. Johnson has no verified death year, and conflicting
secondary identifications of Victor G. Durham do not support either a named-
author or pseudonymous-publication calculation. Hildegard G. Frey's 1957 term
plus the same United States addition expired in May 2018 and was not revived.
Alice B. Emerson is supported by both publication evidence and a conservative
true-author fallback; anonymous `Young Oliver` is supported by the old-law
publication route.

Search-result rendering exposed body fragments for eight already fixed rows.
A copyright-year lookup for Project Gutenberg 36833 also displayed `take in`
in nearby prose. This was not a target or MWE query, but it is target exposure
and is recorded explicitly. It cannot change the frozen rank, rights rule,
first-unit boundary, or length gate. No file was acquired and no unit was
admitted:
[`resources/gutenberg_2026_08_30_rights_triage_batch3.json`](resources/gutenberg_2026_08_30_rights_triage_batch3.json).

The 15 allowed files were then retrieved into ignored local storage and pinned
by exact URL, byte size, mirror-derived modification time, and SHA-256. All 15
contain the standard US/non-US warning, ebook boundaries, and full license;
one preamble identifies an original publication and all include Credits. The
audit decoded only the pre-START notice for review and read complete files only
mechanically for hashes and markers. It selected no unit, ran no MWE search,
and authorizes no public serving:
[`resources/gutenberg_2026_08_30_notice_audit_batch3.json`](resources/gutenberg_2026_08_30_notice_audit_batch3.json).

Front-matter review leaves all 15 files ready for the unchanged first-unit
gate. Nine have a complete print-publication statement and six remain
incomplete; three contain explicit transcriber notes. Paul Armstrong's named
contribution to the underlying `Going Some` play is separately rights-reviewed
rather than erased from the provenance chain. The source-authored opening
letter in `The Jessica Letters`, introduction in `The Spanish Jade`, and
foreword in `The Hunters of the Hills` remain the first unit instead of being
skipped for a chapter. Two Nick Hodson electronic synopses are excluded as
producer paratext. Boundary review incidentally exposed the surface strings
`give up` in 63142 and `take in` in 36833; neither was queried or classified,
and neither can change a fixed boundary or selection. No unit is admitted and
no lexical or MWE search ran:
[`resources/gutenberg_2026_08_30_front_matter_review_batch3.json`](resources/gutenberg_2026_08_30_front_matter_review_batch3.json).

The unchanged gate leaves seven mechanical passes. The adult/unspecified
passes are 13530 (1,876 tokens) and 27996 (1,506); the juvenile passes are
36396 (1,511), 72094 (1,083), 36833 (1,945), 21326 (1,643), and 23683 (907).
Five intact first units exceed 2,000 tokens: 63142, 6488, 40587, 25817, and
44045. The opening letter in 26523, introduction in 29545, and foreword in
14890 are excluded as unfrozen unit types rather than skipped; 26523 would
also be below 300 tokens, but the structural decision is applied first.
`Young Oliver` ends at the next separately titled work rather than absorbing
the remainder of the ebook. Across all three batches, 10 of 44 gated files
pass mechanically—three adult/unspecified and seven juvenile. This remains a
short-unit-biased candidate set, not an admitted or representative corpus. No
unit text is bundled or served, and no target or MWE search ran:
[`resources/gutenberg_2026_08_30_unit_gate_batch3.json`](resources/gutenberg_2026_08_30_unit_gate_batch3.json).

The final metadata-only rights screen closes rather than extends this frozen
frame. Ranks 31–40 yield 13 files eligible only for local notice review, five
likely-active Japanese terms, and two unresolved creator/death terms. The
`Mugby Junction` catalog row omits four retained textual collaborators, but all
five contributors' terms are old enough to advance; conversely, the `Nat
Ridley` house name is linked work-specifically to Howard R. Garis, whose 1962
death keeps that work on hold under the applicable term analysis. Rights-search
rendering incidentally exposed target strings for frozen rows 15188 and 23763;
neither was queried, classified, or allowed to alter the queue. Most
importantly, only five adult/unspecified files can advance, so even the generous
assumption that all five pass the unit gate gives `3 + 5 = 8 < 10`. The
prespecified two-stratum success condition is therefore impossible. No batch-4
ebook was acquired: preserve this failed frame and freeze a redesigned sampling
rule before any further acquisition or MWE inspection:
[`resources/gutenberg_2026_08_30_rights_triage_batch4.json`](resources/gutenberg_2026_08_30_rights_triage_batch4.json).

```bash
python3 scripts/build_gutenberg_prose_frame.py PATH/pg_catalog.csv --check
python3 scripts/audit_gutenberg_notices.py research_data/gutenberg/2026-08-30-batch1 --check
python3 scripts/audit_gutenberg_notices.py research_data/gutenberg/2026-08-30-batch2 --triage resources/gutenberg_2026_08_30_rights_triage_batch2.json --audit-id gutenberg-2026-08-30-notice-audit-batch2 --output resources/gutenberg_2026_08_30_notice_audit_batch2.json --check
python3 scripts/audit_gutenberg_notices.py research_data/gutenberg/2026-08-30-batch3 --triage resources/gutenberg_2026_08_30_rights_triage_batch3.json --audit-id gutenberg-2026-08-30-notice-audit-batch3 --output resources/gutenberg_2026_08_30_notice_audit_batch3.json --check
python3 scripts/audit_gutenberg_units.py research_data/gutenberg/2026-08-30-batch1 --check
python3 scripts/audit_gutenberg_units.py research_data/gutenberg/2026-08-30-batch2 --front-matter resources/gutenberg_2026_08_30_front_matter_review_batch2.json --gate-id gutenberg-2026-08-30-unit-gate-batch2 --output resources/gutenberg_2026_08_30_unit_gate_batch2.json --check
python3 scripts/audit_gutenberg_units.py research_data/gutenberg/2026-08-30-batch3 --front-matter resources/gutenberg_2026_08_30_front_matter_review_batch3.json --gate-id gutenberg-2026-08-30-unit-gate-batch3 --output resources/gutenberg_2026_08_30_unit_gate_batch3.json --check
```

## eLife screen 1: exact artifacts

Only the five versioned XML files below were retrieved from the official eLife
corpus on 2026-09-01. The XML files and extracted prose remain in a temporary
local cache and are not committed. Git blob identity and ordinary file SHA-256
are both recorded because they are different hash constructions.

| Article/XML | Article license | Bytes; XML SHA-256 | Official Git blob SHA |
|---|---|---|---|
| [12102](https://elifesciences.org/articles/12102), `elife-12102-v3.xml` | CC BY 4.0 | 196,603; `b7d68b8af4e9e4e7a717926c2b6fb039bf8fb116f23491d60f8b4e453bb63b00` | `44ea264d61df4e9f49a48c05e170a6666fb622e7` |
| [55659](https://elifesciences.org/articles/55659), `elife-55659-v3.xml` | CC BY 4.0 | 305,837; `1714cff15e94b88c53467692453bf1e8f96c8eac3cca524ce2a574d0cdbf04f2` | `374bad0f942c928f2294036c138413ed4af4686c` |
| [65282](https://elifesciences.org/articles/65282), `elife-65282-v3.xml` | CC0 1.0 | 253,686; `595c51789b562804424e6d75ad792198ec6a2b6400b66652051139a121c48f19` | `fa362844c50fa87a8699c193774b119f1a8bfe5e` |
| [80014](https://elifesciences.org/articles/80014), `elife-80014-v2.xml` | CC BY 4.0 | 260,402; `fdcec772acf87835b226bb6b90a7678647a1ba7e8f70d49342cdfdbdef6bd4e1` | `df820fde24b42ea3341591f31635e1b094a115c2` |
| [82015](https://elifesciences.org/articles/82015), `elife-82015-v2.xml` | CC BY 4.0 | 315,098; `55493e77d965d177ca8500cecc4a2f8721373f0e383f2d62be5664a02c8d826c` | `39f7862876848b481cfd5a5ad7196ef9c8ed7572` |

The standard-library reproducer is
[`scripts/extract_elife_digests.py`](scripts/extract_elife_digests.py). It
requires a filename matching the article/version metadata, extracts only direct
paragraph children of the `eLife digest`, excludes a legacy DOI-only metadata
paragraph, collapses internal whitespace, preserves paragraph breaks, and
records source and derived-text hashes. Its embedded self-check covers inline
markup, date normalization, DOI exclusion, and paragraph preservation.

## eLife screen 1: list-conditioned profiles

The existing app tokenizer and profiles produced the following descriptive
values. Each cell is token coverage followed by type coverage. These are
list-conditioned profiles, not estimates of any reader's `P_word`.

| Article | Paragraphs; tokens/types | NGSL 1K | NGSL 2K | BNC/COCA 1K | BNC/COCA 2K |
|---|---:|---:|---:|---:|---:|
| 12102 | 3; 286/160 | 214/286 (74.83%); 120/160 (75.00%) | 239/286 (83.57%); 139/160 (86.88%) | 190/286 (66.43%); 100/160 (62.50%) | 223/286 (77.97%); 130/160 (81.25%) |
| 55659 | 5; 418/201 | 293/418 (70.10%); 133/201 (66.17%) | 328/418 (78.47%); 162/201 (80.60%) | 265/418 (63.40%); 112/201 (55.72%) | 318/418 (76.08%); 154/201 (76.62%) |
| 65282 | 4; 298/159 | 194/298 (65.10%); 97/159 (61.01%) | 226/298 (75.84%); 112/159 (70.44%) | 182/298 (61.07%); 83/159 (52.20%) | 207/298 (69.46%); 107/159 (67.30%) |
| 80014 | 6; 342/179 | 221/342 (64.62%); 104/179 (58.10%) | 260/342 (76.02%); 131/179 (73.18%) | 200/342 (58.48%); 87/179 (48.60%) | 249/342 (72.81%); 127/179 (70.95%) |
| 82015 | 4; 288/152 | 188/288 (65.28%); 92/152 (60.53%) | 219/288 (76.04%); 112/152 (73.68%) | 166/288 (57.64%); 77/152 (50.66%) | 201/288 (69.79%); 106/152 (69.74%) |

The BNC/COCA projection was regenerated byte-for-byte from the pinned local
v1.0.0 ZIP before this screen: 366,120 bytes, SHA-256
`ebd06548187988eb1a61ab967cc39c01461023043ee7aef427606e5bf508f138`.
It contains only the first two levels, so `unmatched` must not be read as a
claim that a form is absent from later levels or special lists.

## eLife screen 1: MWE leads and decision

The existing transparent pattern matcher recovered the following **lead**
occurrences; these are not exhaustive annotations or human-confirmed gold.

| Article | Lead occurrences |
|---|---|
| 12102 | `clear out` ×1, `break down` ×1, `carry out` ×1, `switch off` ×2, `cut off` ×1 |
| 55659 | `break down` ×3 |
| 65282 | `take up` ×2 |
| 80014 | `carry out` ×1, `break down` ×1, `take up` ×1 |
| 82015 | `carry out` ×1, `make up` ×1 |

The decisive failure is not rights. The repeated forms do not supply the
needed contextual contrast: `break down` consistently denotes biological
degradation/decomposition, `carry out` denotes performing a role/process, and
`take up` denotes absorption. The passages are also dominated by specialized
biological names and concepts; their first-2K token profiles are 69.46–83.57%,
not materials naturally near the historical 95%/98% reference points.

Therefore none of the five is admitted to the primary university-L2 passage
set. They remain lawful candidates for a later technical-domain stress test,
where same-sense recurrence could be useful. No comprehension items, expanded
OEWN sense projections, external annotators, or app features will be spent on
them now. This rejection does **not** show that a particular reader would have
less than 95% tested word knowledge; list membership and `P_word` remain
different constructs.

## VOA screen 2: rejected primary `take in` sense pair

Two VOA Learning English articles survived the source, rights, audience, and
first lexical screen. Their author credits name VOA Learning English production
rather than adaptation of an AP, Reuters, or AFP story. The current VOA reuse
page says Learning English text is public domain and asks for source credit, but
excludes outside news-agency material. Accordingly, only the direct article
paragraphs are candidates: images, captions, audio, quizzes, glossaries, links,
and site furniture are excluded.

| Candidate | Fixed metadata and provenance | Candidate `take in` occurrence | State |
|---|---|---|---|
| [National Arboretum](https://learningenglish.voanews.com/a/national-arboretum-a-quiter-place-to-enjoy-cherry-blossoms/4342830.html) | Published 2018-04-11; modified 2018-04-13; Ashley Thompson author credit; 88,700-byte AMP HTML, SHA-256 `16d2ff20ff694ea261b30b57d7e82537db3332318d7465e8e2005b5924fcd02b`; 26-paragraph text SHA-256 `894bfbd040fab7d0bb49c52584be7688206f765f4a108e2b5152693008e56d6a` | viewing a scene; OEWN candidate `take_in%2:39:06::` | Reject from primary set; retain as a diagnostic sense case |
| [Lightning prediction](https://learningenglish.voanews.com/a/scientists-test-systems-to-predict-control-lightning/5164418.html) | Published/modified 2019-11-13; Bryan Lynn author credit based on named scientific-project reports; 90,782-byte AMP HTML, SHA-256 `eae98af029181abeae222fa26de84edfa345da81bf04c43dad2f9785c703c1a2`; 16-paragraph text SHA-256 `b946418491846e9e1929018688b1a4cf66ef1b25401fd10a08fa254d05cd20cd` | absorbing/receiving an electrical charge; OEWN candidate `take_in%2:43:00::` | Reject from primary set; retain as a diagnostic sense case |

The standard-library extractor
[`scripts/extract_voa_articles.py`](scripts/extract_voa_articles.py) checks the
canonical URL against the embedded NewsArticle record, records publication and
modification times plus author credit, takes only direct non-caption paragraph
children, stops before the presenter sign-off, and excludes all nested media
and post-article teaching material. Its self-check covers metadata consistency,
inline text, nested-caption exclusion, sign-off boundaries, and credit recovery.
The source HTML stays outside the repository; only provenance and derived-text
hashes are recorded here.

| Candidate | Tokens/types | NGSL 1K | NGSL 2K | BNC/COCA 1K | BNC/COCA 2K |
|---|---:|---:|---:|---:|---:|
| National Arboretum | 826/334 | 656/826 (79.42%); 239/334 (71.56%) | 689/826 (83.41%); 267/334 (79.94%) | 653/826 (79.06%); 241/334 (72.16%) | 720/826 (87.17%); 283/334 (84.73%) |
| Lightning prediction | 582/264 | 440/582 (75.60%); 181/264 (68.56%) | 502/582 (86.25%); 222/264 (84.09%) | 406/582 (69.76%); 159/264 (60.23%) | 488/582 (83.85%); 218/264 (82.58%) |

### VOA screen 2: full desk inventory

The full extracted prose was read paragraph by paragraph. A second high-recall
pass matched every contiguous token sequence against all 2,847 OEWN multiword
verb forms after applying the existing NGSL surface-to-head mappings. A manual
pass then checked discontinuity and likely omissions. OEWN membership generated
**leads**, not occurrence truth or PARSEME labels. The states below are one
researcher's development decisions, not independent gold.

| Passage/paragraph | Span | Desk state | Relevance to passage admission |
|---|---|---|---|
| Arboretum 7, 15 | `work on` ×2 | Possible VPC; category remains unresolved | Research activity, but not a repeated cross-sense target |
| Arboretum 9 | `hang down` | Manual possible VPC.semi; literal spatial meaning; absent from the OEWN form projection | Useful detector-miss case, not an idiomatic target |
| Arboretum 10 | `come to life` | Probable VID; OEWN matched | Describes flowering and is moderately central, but occurs once |
| Arboretum 12 | `put it on` | Rejected as a target occurrence: literal placement of pollen, with `it` as the object gap | Confirms why a separated surface match cannot establish an MWE |
| Arboretum 14 | `end up` | Probable VPC | Eventual naming is locally relevant, but occurs once |
| Arboretum 24 | `walked up on` | Manual lead; compositional approach reading and category unresolved | Not an admitted lexical target |
| Arboretum 24 | `take in` | Probable VPC.full; viewing sense, OEWN `take_in%2:39:06::` | Peripheral visitor quotation; “with your own eyes” supplies a near-definition |
| Arboretum 25–26 | `count on` ×2 | Probable VPC.full; same rely sense, OEWN matched | Central to the closing claim, but offers recurrence without sense contrast |
| Arboretum 26 | `drawn out` | Rejected as a verbal MWE occurrence: adjectival/participial use | Surface lexicon hit only |
| Lightning 14 | `work on` | Possible VPC; category remains unresolved | Project-description lead, not a repeated target |
| Lightning 15 | `take in` | Probable VPC.full; absorption sense, OEWN `take_in%2:43:00::` | One mechanism detail; the object “electrical charges” strongly constrains the sense |

The exhaustive lexicon pass also surfaced `travel to`, `known as`, `live in`,
`go to`, `look at`, and future `going to` in the Arboretum text. These are
literal directional/prepositional or grammatical sequences outside the bounded
VPC/VID target. In the lightning text, `strikes up to 30 minutes` falsely
matched `strike up`: `up` belongs to the quantity phrase, not the verb. Manual
review found no hidden idiomatic occurrence in the latter passage; `keep
developing` is aspectual and outside the current category scheme, while passive
`have been cut` contains no particle.

### VOA screen 2: decision

This pair succeeds only as a compact **polysemy demonstration**: the same form
occurs naturally in two OEWN candidate senses in L2-directed prose. It fails the
harder material criterion. Neither `take in` occurrence is important to global
understanding, both senses are strongly cued by nearby words, the passages
differ by 244 profile tokens and by topic, and a target-critical question would
likely collapse into a phrase-definition question. Cutting out only the two
target-bearing sections would shorten the texts but would not repair target
centrality or contextual transparency.

The pair is therefore rejected from the primary 95%/98% passage set before item
writing or outside annotation. It may remain a development diagnostic for
sense-interface testing, explicitly without criterion-validity claims. The
negative result fixes an important selection rule: **cross-sense recurrence is
necessary for a polysemy claim but is not sufficient for a comprehension
material**.

Their first-2K values are screening descriptors, not failed 95% tests. The
historical 95%/98% question concerns person-by-text tested coverage in the
criterion study; no fixed-list percentage can establish that a participant
knows or does not know these texts.

## Simple English Wikipedia screen

Six current `take in` leads were checked by exact revision ID and rejected
before full extraction: Animal `10939537`, Drink `10711126`, Bank `10553711`,
Insulin `9568048`, Adoption `9969597`, and Duluth, Minnesota `10733332`.
Collectively they supplied absorption, viewing, receiving, and understanding
senses, but the actual passages introduced decisive quality threats: one was
only about 100 words, several used awkward or questionable phrasing, one had
malformed extract boundaries, the adoption page included sensitive and
stigmatizing unsupported generalizations, and the longer pages carried lists or
heavy proper-name/topic demands. Revision pinning solved mutability, not text
quality. These exact revisions are rejected; Wikimedia remains a fallback
source class rather than a convenience pool.

## VOA screen 3: `take up` pair and pedagogical-marking confound

Two further VOA-produced articles were pinned and run through the revised
standard-library extractor. This screen exposed a threat that source licensing
and plain-text extraction alone do not solve: Learning English pages sometimes
bold a target and define it in a post-article glossary. Removing the typography
and glossary changes the original reading environment; retaining them cues the
target. Such an occurrence cannot be called an unmanipulated criterion target.

| Candidate | Fixed metadata and provenance | State |
|---|---|---|
| [Ways to Achieve Your Goals](https://learningenglish.voanews.com/a/ways-to-achieve-your-goals/4758976.html) | Published/modified 2019-01-28; Anna Matteo author credit; 87,393-byte AMP HTML, SHA-256 `132303b642a84e7927612ba27d43f6770c961fe57c93de215ed71b4e6811a371`; 28-paragraph text SHA-256 `ac67501695c4f04172f2564b4909e55009c5cfc9fc377919cd8cabb5fbeebf6a` | Retain as one singleton only: unbolded `takes up all of your time` is central and not glossed, but no lawful partner has passed the screen |
| [NASA Keeping Watch on the Earth’s Health](https://learningenglish.voanews.com/a/us-space-agency-keeping-watch-on-earths-health/2615927.html) | Published/modified 2015-01-28; Christopher Cruise author credit based on a VOA Science Correspondent report; 86,521-byte AMP HTML, SHA-256 `09934fdc52475cb6e61c08fb6459967171b5ddd2df209861bd5c23c8d640ac1b`; 14-paragraph text SHA-256 `daf6ec1857adf5722296acc0f44a51ce54fdd29152fea8ac3e5c8269960a3227` | Reject from the primary set: technical load and explicit source-page marking/definition of `taken up by` |

| Candidate | Tokens/types | NGSL 1K | NGSL 2K | BNC/COCA 1K | BNC/COCA 2K |
|---|---:|---:|---:|---:|---:|
| Goals | 739/294 | 685/739 (92.69%); 248/294 (84.35%) | 715/739 (96.75%); 271/294 (92.18%) | 634/739 (85.79%); 237/294 (80.61%) | 711/739 (96.21%); 270/294 (91.84%) |
| NASA | 499/236 | 374/499 (74.95%); 156/236 (66.10%) | 426/499 (85.37%); 186/236 (78.81%) | 384/499 (76.95%); 159/236 (67.37%) | 433/499 (86.77%); 194/236 (82.20%) |

The Goals passage is materially stronger than the earlier candidates under a
fixed-list screen, but that is not an admission by itself. Its central OEWN and
manual leads include `take up`, `work on` ×2, `end up`, `sign up`, `write down`
×5, separated `let ... down`, `break ... down`, `make up` ×2, and `check in`.
The source itself bolds or teaches several of these, and the `break down`
heading plus following sentence nearly defines its meaning. Those expressions
cannot be counted as natural hidden-burden targets. The unbolded `take up`
occurrence remains plausible because losing all available time is the passage's
opening problem and the expression is not in the glossary.

The NASA passage contains plausible `take up`, `figure out`, and `go on` leads,
but `taken up by` is bolded and the excluded glossary defines it as absorption.
It also falls 11.38 percentage points below the Goals passage on NGSL-2K token
membership and carries mission acronyms and climate-science background. Pairing
the two would therefore confound target sense with lexical/topic difficulty and
with original pedagogical marking. NASA is rejected before item writing. Goals
remains **not admitted** until an unmarked partner and more than one
decision-relevant repeated target survive the same audit.

A third lead, [Changes to Twitter Let You Say More in a
Tweet](https://learningenglish.voanews.com/a/twitter-update-2016/3364301.html),
was rejected before full extraction despite an unbolded, central `take up`.
Its present-tense explanation is tied to the obsolete 2016 140-character
policy and former Twitter identity, so current platform knowledge could compete
with passage information. Its article argument also depends on a six-item HTML
list that a paragraph-only extraction would omit. The retrieved ordinary HTML
was 109,166 bytes with SHA-256
`13eef939b3c0705df6f8c3c9efdcc7f58554d957172e5fd7a9b2c061bf9e5971`;
the site's advertised AMP route redirected to itself. No second parser or
special material repair was added for a passage already rejected on content
and structure.

## VOA screen 4: one unmarked `end up` pair, but no admissible set

The next search tested the Goals passage's `write down` and `end up` leads
against two further VOA-produced articles. It did not treat search-engine
snippets as evidence: both pages were downloaded as AMP HTML, pinned by hash,
extracted, profiled, and read in full. The shared extractor now accepts the
observed `reported this for VOA Learning English` credit in addition to its
existing `wrote this story` form; the same source-boundary check and self-check
cover both forms.

| Candidate | Fixed metadata and provenance | State |
|---|---|---|
| [How to Inspect Your Own Writing](https://learningenglish.voanews.com/a/how-to-inspect-your-own-writing/5668393.html) | Published/modified 2020-12-05; Jill Robbins author credit; 89,031-byte AMP HTML, SHA-256 `0723e7fa75dcc830609b9204f85d9627e976971ba1a96e058b7f74bbf3f7ed75`; 16-paragraph text SHA-256 `78ab9c2fa390490353963e1a7fce16d5d553fbac32db8cf075e2075d6aa01416` | Reject as a `write down` partner; retain the separated `passes it off` case as a detection diagnostic only |
| [College Admissions: Understanding the Common Application](https://learningenglish.voanews.com/a/college-admissions-advice-understanding-common-application/4010355.html) | Published 2017-09-16; modified 2017-09-19; Pete Musto reporter credit; 91,314-byte AMP HTML, SHA-256 `cf7de94e0643c832fd60a3868719862f82b7aaa91fd3abda0e4d01eeebe723e5`; 25-paragraph text SHA-256 `a3aa2390fd2cba7e0dc751e416abf9e775bfd0ed39f16878dbd5ced8d292faea` | Retain with Goals as a provisional unmarked `end up` pair; do not admit either passage yet |

| Candidate | Tokens/types | NGSL 1K | NGSL 2K | BNC/COCA 1K | BNC/COCA 2K |
|---|---:|---:|---:|---:|---:|
| Goals | 739/294 | 685/739 (92.69%); 248/294 (84.35%) | 715/739 (96.75%); 271/294 (92.18%) | 634/739 (85.79%); 237/294 (80.61%) | 711/739 (96.21%); 270/294 (91.84%) |
| Inspect writing | 643/261 | 538/643 (83.67%); 196/261 (75.10%) | 576/643 (89.58%); 221/261 (84.67%) | 526/643 (81.80%); 182/261 (69.73%) | 572/643 (88.96%); 219/261 (83.91%) |
| Common Application | 1,122/397 | 1,016/1,122 (90.55%); 324/397 (81.61%) | 1,052/1,122 (93.76%); 360/397 (90.68%) | 932/1,122 (83.07%); 283/397 (71.28%) | 1,045/1,122 (93.14%); 353/397 (88.92%) |

In the writing article, unbolded `write down notes` is locally relevant but
occurs once. Its apparent partner is not an unmanipulated target: the Goals
page gives **Write your goals down** its own bold section heading and then
explains why writing a goal down matters. Removing that heading or treating
the repeated expression as hidden lexical burden would change the source
condition. The writing article is also 7.17 percentage points below Goals on
NGSL-2K token membership and contains book titles, named style guides, and
academic-writing terminology. This branch is rejected before item writing.

The high-recall pass over the writing article also found `turn to`, `look for`,
`look at`, `make sure`, and `think about`. It falsely matched nominal `writing
in school` to `write in` and `work in different styles` across the wrong local
structure. Manual discontinuity review recovered `passes it off as their own`:
the pronoun is a genuine object gap, but the sentence is itself the article's
definition of plagiarism and therefore almost supplies the meaning. This is a
useful `take it in`-type detector case, not a criterion target.

In the Common Application article, unbolded `end up applying` supports the
opening causal proposition: rising competition leads students to apply to
several schools, motivating the common application system. Goals has the same
unbolded resultative construction in `end up feeling guilty`, where the result
of neglecting goals motivates the article's advice. OEWN supplies one canonical
`end up` verb entry, and the provisional desk review treats both as the same
probable resultative VPC sense. Other exact leads in the admissions article
include `get into`, `go ahead`, `send in`, `has to do with`, and `give up`;
future `going to`, `have ... on campus`, and several gapped particle matches are
not VPC/VID occurrences. The only plausible cross-passage VPC/VID target is
`end up`; shared `think about` is a transparent prepositional verb outside the
bounded target, and `go to` includes false future-construction matches.

This is the first pair retained by the centrality and marking screen, but it is
**not an admitted material set**. It supplies only one repeated
decision-relevant target, while the admission rule requires more than one. The
1,122-token admissions article is 383 tokens longer than Goals and carries
U.S.-specific admissions processes, proper names, numbers, and several inline
learner glosses. Those differences could shift global comprehension without
any MWE effect. No post-hoc excerpt, target insertion, item, or external label
was created to rescue the pair.

## VOA screen 5: education near-match and end of target-form search

[Paying Tech Talents to Drop Out of
College](https://learningenglish.voanews.com/a/paying-tech-talents-to-drop-out-of-college-122799744/116827.html)
was the closest education-domain lead found by asking a search engine for an
`end up` partner. The official page identifies it as a VOA Special English
Technology Report written by June Simms, published and last modified on
2011-05-29. The retrieved HTML was 73,160 bytes with SHA-256
`b3e45f52b6cbe33b65febba43da563b7aa3877bd370d7591badb68df87837816`.
A temporary legacy-page boundary check extracted 14 article-content prose paragraphs,
529 ASCII word-profile tokens and 252 types; the derived text SHA-256 was
`2da14547855f62a48d8aab2b6b9da1e363b8b801a98dc1ef0ffeda89f82425eb`.
Its NGSL first-1K profile was 439/529 tokens (82.99%) and 188/252 types
(74.60%); first-2K was 463/529 tokens (87.52%) and 208/252 types (82.54%).
These remain list-conditioned descriptors.

The current extractor did not accept this legacy layout as one of
its supported modern article artifacts. No old-page parser was added for a text
that already fails the material decision. The temporary prose and source HTML
remain uncommitted; the hashes and explicit boundary—exclude the opening
program label and closing presenter/credit paragraph—make the desk decision
auditable without turning the exception into production code.

The full prose check found resultative `end up` twice, `drop out`, quoted
`stop out`, possible `work on`, separated `carry it forward`, increase-sense
`gone up`, and separated `paying the debt off`. `take back to school`, `go to
college/law school`, and `look at` were compositional in context, while nominal
`start-up` was an orthographic false lead. Both `end up` occurrences matter to
the account of educational choice and debt, but no second decision-relevant
form recurs in Goals or Common Application. `drop out` is also announced in the
title and immediately contrasted with `stop out`, so it is not a hidden lexical
burden. The 2011 technology-policy setting, named entrepreneurs and firms, and
Obama-era claim add age and background-knowledge differences.

The article is therefore rejected as a partner before BNC/COCA profiling,
item writing, or extractor expansion. More importantly, this ends
target-form-conditioned passage discovery. Searches for `end up` plus `give
up`, `work on`, `sign up`, or `get into` mostly returned third-party
adaptations, long external-interview transcripts, off-domain stories, or
peripheral occurrences. Continuing until a desired pair appears would select
texts on the lexical outcome and conceal the number of failed opportunities.

### Frozen development-frame rule

The next screen starts from source metadata, not MWE strings:

1. Snapshot the official VOA [Education](https://learningenglish.voanews.com/z/959)
   and [Health & Lifestyle](https://learningenglish.voanews.com/z/955) archive
   pages for 2017-01-01 through 2020-12-31, recording every archive artifact
   hash and canonical article URL. This window deliberately includes the
   already-seen Goals and Common Application texts and is therefore a bounded
   development frame, not an untouched probability sample.
2. Before reading target content, exclude only records outside the dates,
   duplicates, non-article media, and credits that identify AP, Reuters, AFP,
   another external source, or adaptation. Preserve every exclusion and do not
   filter titles or snippets for an MWE.
3. Order the remaining unseen URLs by SHA-256 of
   `gate1-voa-frame-v1\n` plus the canonical URL. Fully inspect the first 12
   eligible unseen articles from each source program (24 maximum). The number
   is a development-workload cap, not a statistical power claim.
4. If this prespecified frame supplies no minimally coherent passage set, do
   not extend the dates, add a third genre, or resume phrase search. Switch to
   the roadmap's naturalistic observational design or narrow the paper to the
   annotation/reporting method.

The 2026-09-01 snapshot is now frozen in
[`resources/voa_gate1_frame_2017_2020.json`](resources/voa_gate1_frame_2017_2020.json)
and reproducible with
[`scripts/build_voa_material_frame.py`](scripts/build_voa_material_frame.py).
It records 79 archive pages, 936 unique in-window article URLs (499 Education;
437 Health & Lifestyle), three previously seen URLs, and 24 target-blind
initial metadata draws. Archive HTML and article prose are not committed. The
frame file is 498,234 bytes with SHA-256
`cb6911287348f7e98353b65b441f1f7c421ffe47b74c4ac7d18dbb4c77190dca`.
The draw is only a review queue: article-level credit, prose boundary, rights,
and source-marking checks can still reject an item, in which case the next URL
in the same precomputed queue is inspected.

### Target-blind source eligibility result

The source-only gate is frozen in
[`resources/voa_gate1_source_screen.json`](resources/voa_gate1_source_screen.json)
and regenerated by
[`scripts/screen_voa_article_sources.py`](scripts/screen_voa_article_sources.py).
It inspected the precomputed queue without searching article text for an MWE.
Education required ranks 1–25 to reach 12 eligible articles: seven were
external/adapted, two lacked a recognized VOA-production credit, and four were
unsupported quiz/non-article artifacts. Health & Lifestyle required ranks 1–38:
25 were external/adapted and one lacked a recognized production credit. Thus 24
of 63 inspected records passed only the source, canonical-artifact, credit, and
extractable-prose checks.

The screen stores titles, URLs, dates, credit lines, source hashes, and eligible
derived-text hashes, but no HTML or article prose. Its 47,956-byte JSON has
SHA-256
`5ebe015f15874a127940bbd6ad196f4b031d0487bf4d56c5712e68151881e7aa`.
The shared extractor now accepts attested `reported on this story` and `for
Learning English` credit variants. It still does not convert an adaptation into
an eligible article. Passing this gate says nothing about MWE presence,
centrality, text quality, list profile, or comprehension validity.

### Target-blind automated pre-review result

[`resources/voa_gate1_automated_profile.json`](resources/voa_gate1_automated_profile.json)
now freezes the open-resource first pass for all 24 source-eligible articles.
The standard-library reproducer
[`scripts/profile_voa_material_candidates.py`](scripts/profile_voa_material_candidates.py)
verifies every source/text hash, applies the same ASCII word tokenizer, reports
NGSL 1K/2K token and type membership, and generates within-paragraph contiguous
OEWN leads after projecting exact NGSL surface forms to all supplied heads. A
second pass tests two-member OEWN forms with one or two intervening tokens. It
stores only article metadata, hashes, aggregate counts, and short matched spans,
not HTML or passage prose. The 113,140-byte result has SHA-256
`efe61f49a81e59274d532a650da4a362dab4067eeaa0f0fe79bdebf4b8b77603`.

Across the 24 intact articles, NGSL-2K token membership ranges from 74.42% to
93.40% (median 89.46%); none reaches 95%. The local-only Nation BNC/COCA overlay
was generated under ignored `research_data/` from the already verified profile:
its first-2K token membership ranges from 77.78% to 93.14% (median 89.72%), also
with no article at 95%. These are full-article fixed-list descriptors, not
participant knowledge or failed comprehension thresholds. Proper names,
special-list policy, article topic, and tokenizer decisions contribute to the
values and must remain visible rather than being silently recoded to obtain a
preferred percentage. The local overlay is not a release artifact while its
derived-output rights remain unresolved.

The high-recall pass produced 229 automatic leads covering 110 OEWN canonical
forms; 38 forms appear in more than one article. That apparent recurrence is
not yet substantive evidence. The highest-frequency rows include compositional
or syntactically accidental strings such as `go to`, `do in`, and `have on`.
More plausible cross-document review priorities include `grow up` and `look
for` in three articles each, plus `go out`, `point out`, `find out`, `get into`,
and `work on` in two or more. No `take in`, `take part`, or `take up` lead occurs
in this bounded set. Every lead still needs paragraph-level confirmation,
discontinuous/out-of-inventory recovery, source-marking review, contextual
sense, centrality, and content-quality judgment. Therefore no passage is
admitted and no app sense inventory is expanded at this stage.

The gap pass produced another 128 leads covering 80 forms. Nineteen forms
appeared in more than one article, but context inspection rejected every one as
a separated occurrence: they crossed ordinary phrase boundaries or skipped a
member of a different contiguous expression, such as treating `come up with`
as gapped `come with`. The only automatic gapped `take in` lead was `taking
classes in`, not a VPC; no `take it in`-type occurrence was found. This does not
establish perfect recall: forms longer than two members, gaps over two tokens,
spelling variants, and out-of-OEWN expressions remain manual-review duties.

The preliminary recurrence decisions are frozen without prose in
[`resources/voa_gate1_recurrence_triage.json`](resources/voa_gate1_recurrence_triage.json).
Of the 38 contiguous recurrent forms, 13 remain for occurrence-level review and
25 are non-decision-relevant recurrence. Four article pairs share at least two
retained forms. The first two are Education 07 + 12 (`go on`, `work on`) and
Education 12 + 16 (`go on`, `point out`), because their topics, lengths, and
fixed-list profiles are substantially better matched than the two deferred
cross-program/health pairs. This is project-internal triage with author
confirmation pending, not gold annotation or passage admission.

### Priority Education-pair desk review

The complete preliminary review is frozen without prose in
[`resources/voa_gate1_priority_desk_review.json`](resources/voa_gate1_priority_desk_review.json).
It covers every one of the 44 contiguous and 21 short-gap automatic leads in
Education 07, 12, and 16, plus 15 manual additions. The three exact extracted
texts contain 932, 994, and 1,193 profile tokens. Their NGSL-2K token values are
92.27%, 91.85%, and 91.95%; the close percentages remain list-conditioned
descriptors, not participant coverage.

The manual pass exposed three failures that an OEWN form count cannot show.
First, out-of-inventory expressions do not automatically belong to the bounded
target: STREUSLE labels `deal with` as IAV, while PARSEME 1.2 places `find
oneself` under IRV. Second, an inventory entry may not supply either the
contextual sense or the projected category: Education 07's `do well` sense is
missing, and `go on the market` has a noun-phrase complement rather than the
retained intransitive particle construction. Third, original pedagogy matters:
Education 12 explicitly bolds and defines `allow for`, and Education 16 does
the same for `applying to`. A source's broad “phrasal verb” label is a teaching
cue, not proof of a PARSEME VPC/VID category.

Both priority pairs are therefore rejected from the primary material set,
pending author confirmation. Education 07 + 12 retains `go on`; STREUSLE puts
`work on` only in its weak-MWE layer, outside the strong VPC/VID projection.
Education 12 + 16 retains `point out`, but Education 16's `go on the market` is
outside the intransitive VPC and `point out` mainly marks reported evidence.
Each pair therefore retains only one independently defensible repeated form,
below the prespecified requirement of more than one. No passage or new app
sense projection is admitted.

### Deferred-pair desk review

The matching prose-free ledger is
[`resources/voa_gate1_deferred_pair_desk_review.json`](resources/voa_gate1_deferred_pair_desk_review.json).
The two official AMP artifacts exactly reproduce their frozen source and text
hashes. The review covers all 45 contiguous and 25 short-gap automatic leads in
Health 03 and 22 plus 16 manual additions. Health 03 contains 1,326 profile
tokens with 91.10% NGSL-2K membership; Health 22 contains 823 tokens with
83.72%. These descriptors are not learner-knowledge estimates. The ignored
local BNC/COCA overlay shows the same imbalance but is not copied into the
public review ledger.

The Health pair confirms the useful contrast anticipated by triage: `going out
with a man` uses the dating sense of `go out`, while the mushroom article uses
`go out` three times for leaving to forage. Both are locally important. The
second shared form fails, however. In `go on` plus a date or walk, `on` heads a
noun-phrase complement rather than the retained intransitive particle
construction. The 503-token, 7.38-point NGSL-2K, topic, and
interview-versus-exposition differences add avoidable non-target variance.

The cross-program Education 07 + Health 03 pair also fails. Its `feel like`
occurrences are quoted finite-clause stance frames, whereas the selected
STREUSLE VID evidence is inclination plus gerund. Health 03's `go on a date` is
also outside the retained intransitive VPC. Health 03 is 394 tokens longer and
adds COVID, dating sensitivity, four interviewees, and conversational
disfluency.

Manual review did expose one candidate that automatic recurrence triage could
not: Education 16 and Health 03 both use a result-state `find oneself`
construction, alongside `go on`. It still cannot rescue the frame. PARSEME
1.2 places English `find oneself in a difficult situation` under inherently
reflexive verbs, outside this project's VPC/VID target. In `go on a date` and
`go on the market`, `on` heads a noun-phrase complement rather than functioning
as the particle in the retained intransitive `go on` VPC; any inherently
adpositional or productive-construction analysis is also outside the bounded
target. All four frozen recurrence pairs and this manual pair remain rejected
pending author confirmation, and no app sense projection is expanded.

### Bounded out-of-inventory audit and frame stop

The final prose-free ledger is
[`resources/voa_gate1_out_of_inventory_audit.json`](resources/voa_gate1_out_of_inventory_audit.json).
All 19 remaining official AMP files reproduced their frozen source/text hashes.
An adversarial search used 227 ASCII multi-member strong VPC/VID types from all
STREUSLE 5.0 splits that were absent from the OEWN projection. The existing
matcher generated 30 contiguous and 41 short-gap leads; merging both channels
left 10 cross-document forms. Many were grammatical or boundary collisions,
including `have to`, `have do`, and `have it`. Generous upper-bound retention
kept unresolved or plausible `base on`, `have time`, `make money`, `say no`,
`spend time`, and `take time` cases.

The decisive check combined those upper-bound cases with all 13 forms retained
by the earlier preliminary triage—even forms later excluded as weak MWEs or
IAVs. Fifteen article pairs shared one candidate form; none shared more than
one. The result therefore does not depend on resolving the remaining borderline
categories, source marking, or centrality: those reviews could only remove
candidates, not create the missing second form. The frozen 24-article VOA frame
is stopped with no passage or app change.

## Frozen redesign: Simple English Wikipedia Route 2

The complete prespecified contract is
[`resources/simplewiki_gate1_route2_design.json`](resources/simplewiki_gate1_route2_design.json).
It was frozen before acquiring or reading any article from the new frame. The
source is the 2026-08-01 Simple English Wikipedia articles multistream dump:
384,058,867 bytes, official SHA-1
`4f646363bd2d095652149a6bdd87a0cedf51f6b2`. The dump remains local and ignored;
each selected revision still requires page-level attribution and imported-text
review before any release.

Route 2 v1 is now stopped before the `come out` desk review. The
[content-neutral amendment](resources/simplewiki_gate1_route2_content_neutral_amendment.json)
preserves the original bytes and decisions but identifies a construct error:
topic sensitivity was used as if it invalidated an occurrence or contextual
meaning. Existing ledgers therefore remain exploratory audit records, not a
content-neutral material panel.

The target pool is no longer discovered from the target corpus. It is derived
from the pinned STREUSLE 5.0 train split, OEWN 2025 sense inventory, and NGSL
first-2K component ranks. The frozen search targets are `take in`, `pick up`,
`give up`, `come out`, `make it`, and `get it`. `pass away` was excluded before
retrieval under the low-risk first-pilot rule. That exclusion is now withdrawn
as a content-neutral construct rule: under the frozen ranking inputs, `pass
away` would outrank `get it` for the second VID position. A successor must
therefore rederive the whole target pool rather than merely changing passage
labels. `take part (in)` remains a
declared unit-boundary/adposition stress case: it has no exact occurrence type
in the pinned STREUSLE train split, while OEWN projects `take part` rather than
`take part in`; adding it here would require a new construct rule, not a silent
exception.

For each target, candidate pages are ordered by a prespecified SHA-256 key. The
queue advances through mechanical exclusions, then desk review stops after 20
mechanically eligible pages. Exactly three distinct articles must span at least
two clearly different provisional paraphrase meanings. Gate 1 needs at least
four successful targets—three VPCs and one VID—and at least one naturally
separated VPC with an intervening pronoun or noun-phrase object. Thus `take it
in`-type structure is a hard material check rather than an optional detector
demo. The maximum panel is 18 articles, one focal target per article.

Only whole standardized main-prose views of 400–1,000 profile tokens are
eligible. No target may be inserted, rewritten, selectively excerpted, taught,
glossed, or specially marked. NGSL and local BNC/COCA values are computed only
after selection and cannot be used to hunt for passages near 95% or 98%. This
target-conditioned panel can test a bounded mechanism; it cannot estimate MWE
prevalence, representative L2 lexical coverage, or a revised universal
threshold.

### Automated candidate queue

The ignored dump reproduced its frozen byte size and SHA-1 before parsing. The
standard-library screener
[`scripts/screen_simplewiki_route2.py`](scripts/screen_simplewiki_route2.py)
then streamed 398,768 main-namespace pages and wrote the prose-free
[`resources/simplewiki_gate1_route2_candidates.json`](resources/simplewiki_gate1_route2_candidates.json).
The ledger retains all 16,375 target-page rows across 14,730 unique pages,
including automatic exclusions, cross-target candidate flags, exact revision
and source-text hashes, and deterministic ranks. It contains no article prose
or contributor data.

| Target | Raw page leads | Mechanically excluded before queue | Ranked queue |
|---|---:|---:|---:|
| `take in` | 7,202 | 91 | 7,111 |
| `pick up` | 618 | 8 | 610 |
| `give up` | 948 | 3 | 945 |
| `come out` | 1,540 | 27 | 1,513 |
| `make it` | 5,324 | 76 | 5,248 |
| `get it` | 743 | 22 | 721 |

These are page leads, not 16,375 MWEs. Most importantly, all first 20 `take
in` rows are gap-only leads. The permissive 1–8-token rule can capture `take it
in`, but also unrelated verb-plus-preposition sequences. That is now an exposed
precision/burden risk; it is not a reason to reorder the frozen queue after
seeing titles. The next screen must distinguish false spans from genuine
separable particles using the exact retained prose.

### Rendered mechanical screen

The standard-library rendered screener
[`scripts/screen_simplewiki_route2_rendered.py`](scripts/screen_simplewiki_route2_rendered.py)
followed each frozen queue until the first 20 pages passed the rendered main-
prose, ordinary-target-location, and 400–1,000-token checks. It fetched 508
unique revision responses for 509 target rows, cached the responses locally,
and published only hashes, counts, profiles, and exclusion states in
[`resources/simplewiki_gate1_route2_rendered_screen.json`](resources/simplewiki_gate1_route2_rendered_screen.json).
It verified 508 row-level source-wikitext hashes against the dump. Revision
`10905348` returned `nosuchrevid`; that row remains an explicit exclusion and
was not replaced out of rank order.

| Target | Queue rows rendered | Mechanically eligible desk rows | Last queue rank |
|---|---:|---:|---:|
| `take in` | 97 | 20 | 97 |
| `pick up` | 63 | 20 | 63 |
| `give up` | 70 | 20 | 70 |
| `come out` | 107 | 20 | 107 |
| `make it` | 62 | 20 | 62 |
| `get it` | 110 | 20 | 110 |

Across targets, 389 rows were mechanically excluded, chiefly because the intact
article fell outside the frozen token bracket. Cue-only target locations and
the unavailable revision were also retained. The 120 survivors are only desk-
review rows across 119 distinct pages. Forty-two rows carry a cross-target flag,
and one page occurs in two focal queues; the frozen one-page/one-target rule must
be resolved during review. No automatic lead is yet a VPC/VID occurrence,
idiomatic sense, central target, coherent passage, or admission.

### `take in` desk review: target failure

The first bounded target review is preserved without article prose in
[`resources/simplewiki_gate1_route2_take_in_desk_review.json`](resources/simplewiki_gate1_route2_take_in_desk_review.json).
All 20 mechanically eligible articles were read in full. The review adjudicated
all 28 automatic one-to-eight-token gap leads and separately inspected all 41
tokens projected to the `take` head for contiguous, longer-gap, and missed
occurrences. Every lead was false and no `take in` occurrence was found.

| False-span structure | Count |
|---|---:|
| `take place` plus an `in` modifier | 6 |
| Literal `take + NP` plus an `in` modifier | 6 |
| Another `take` construction plus unrelated `in` | 6 |
| Embedded `take part in` | 5 |
| Sentence/clause boundary crossing | 3 |
| Long lead crossing a complete `take` construction | 2 |

This is a detector/sampling failure, not evidence that `take in` is rare in
Simple English Wikipedia. The permissive gap channel generated candidates from
competing constructions and ignored syntactic and sentence boundaries; the
frozen hash order then sampled those leads as specified. The queue is not
extended and the detector is not repaired mid-study. `take in` fails its
three-article/two-meaning requirement and supplies no discontinuity evidence.
Because Gate 1 needs three successful VPC targets, all three remaining VPCs—
`pick up`, `give up`, and `come out`—had to pass for Route 2 to remain viable.

### `pick up` desk review: preserved v1 early-stop result

The second target review is preserved without article prose in
[`resources/simplewiki_gate1_route2_pick_up_desk_review.json`](resources/simplewiki_gate1_route2_pick_up_desk_review.json).
The frozen sense-stratified rule reached its third provisional selection at
desk rank 4, so the formal review prefix is ranks 1–4 rather than all 20 rows.
All five `pick` heads and all five automatic leads in that prefix were genuine
`pick up` occurrences; no occurrence was missed.

| Rank | Article | Operational meaning | Decision |
|---:|---|---|---|
| 1 | *The Cat in the Hat* | raise or gather scattered objects | Provisionally selected; two occurrences, including `pick ... up` |
| 2 | *School bus* | collect a person for transport | Provisionally selected; naturally discontinuous |
| 3 | *Liverpool Women's Hospital bombing* | collect a person for transport | Rejected only by the now-withdrawn v1 content rule |
| 4 | *The Guardian Legend* | acquire a game item | Provisionally selected; also assigned here as the higher-priority target page |

Under v1, the three selected pages span three operational paraphrases and
include two discontinuous occurrences. Exact OEWN 2025 candidates remain
review aids rather than gold: the physical-gathering and passenger cases cross
closely related inventory boundaries. *The Guardian Legend* also contains two
non-focal `come out` release occurrences and one false long gap crossing those
two complete occurrences; they are logged and the page cannot later serve
`come out`.

The page-level rights review uses a CC BY-SA 4.0 release route, permanent
revision and history links, and an extraction modification notice. *School
bus* was split from *Types of buses*, so that source page, revision, and history
are additional required attribution. The repository still bundles no article
text. Final admission awaits author confirmation, independent labels, language
and content review, sentence verification, and final item/release review.

For transparency, ranks 5–20 were viewed during an internal double-check before
the early-stop clause was re-read. They receive no formal labels and cannot
replace the deterministic rank 1, 2, and 4 selection. This does not change the
selection, but it is a protocol deviation rather than hidden analyst exposure.

Under the content-neutral correction, rank 3 is lexical evidence rather than a
content rejection and would be the third deterministic selection after ranks 1
and 2; rank 4 would remain occurrence evidence but not be selected. This
1/2/3 result is counterfactual only because rank 3 lacks the rights and item
record that v1 never completed, and the correction followed analyst exposure.

### `give up` desk review: preserved v1 result and corrected interpretation

The original review is preserved without prose in
[`resources/simplewiki_gate1_route2_give_up_desk_review.json`](resources/simplewiki_gate1_route2_give_up_desk_review.json).
Ranks 1–15 contained 15 genuine contiguous `give up` occurrences and four false
gap leads; all 35 `give` heads were checked and no target occurrence was missed.
The v1 rule selected ranks 3, 5, and 15 across four operational paraphrases.
Ranks 2 and 9 failed because mechanical extraction broke propositional
coherence, and ranks 4, 7, and 14 contained no target occurrence.

The former topic-based rejections at ranks 1, 6, 8, 10, 11, and 12 and the hold
at rank 13 do not invalidate their preliminary occurrence or meaning evidence.
They are sensitivity annotations only. Applied counterfactually, the
content-neutral rule would select ranks 1, 3, and 5 and stop at rank 5. Later
reviewed rows remain disclosed evidence but cannot enter that early-stop set.
Rank 16 was displayed with the final v1 batch but remains unlabelled. Neither
the v1 3/5/15 set nor the counterfactual 1/3/5 set completes Route 2.

## Hard admission record for each passage

A passage remains rejected until all fields can be completed:

1. exact title, authors, DOI/revision, version-of-record date, retrieval URL and
   date, source artifact, extracted byte hash, and extraction rule;
2. article-level license/copyright statement, attribution string, third-party
   exclusions, modification notice, and release destination allowed;
3. intact passage boundaries, token count, sentence count, heading/citation
   treatment, and a declaration that no target was inserted;
4. NGSL and local Nation BNC/COCA word-token/type profiles with tokenizer,
   cutoff, unmatched/special-list policy, and denominators;
5. exhaustive candidate inventory followed by reviewed VPC/VID span, members,
   gaps, category, idiomaticity, contextual sense, target centrality, and
   unresolved cases;
6. cross-passage form and sense recurrence, including whether a case is merely
   a technical term or transparent compositional use;
7. language-review threats, propositional coherence, topic familiarity,
   avoidable cultural/background-knowledge demands, and sensitivity metadata
   kept separate from lexical validity; and
8. draft global comprehension and separately labelled target-critical items
   that do not simply ask for the target expression's definition.

Route 2 fixes a pragmatic 400–1,000 profile-token passage bracket and its target
recurrence limits before acquisition. It deliberately fixes no coverage band,
target-density success value, comprehension cutoff, or reliability threshold.
Rejection reasons are retained to prevent convenience sampling from
disappearing.

## Next bounded actions

This application-material dossier is closed while the core VPC/VID occurrence
and contextual-sense evidence package is active. The completed steps below are
retained as audit history, not as the current priority.

1. ~~Obtain rendered views in frozen rank order and apply the mechanical
   boundary, source-marking, and 400–1,000-token rules until 20 eligible rows
   per target remain.~~ Complete; all public records are prose-free.
2. ~~Run the bounded `take in` occurrence screen and measure its gap-channel
   false-positive burden.~~ Complete; 28/28 leads were false and the target
   failed with zero occurrences.
3. ~~Preserve the original `pick up` and `give up` desk outcomes.~~ Complete;
   the v1 selections were ranks 1/2/4 and 3/5/15 respectively, and the later
   content-neutral counterfactuals are disclosed rather than silently
   substituted.
4. ~~Pin TECO v1.1's file/variable manifest and verify its join contract.~~
   Complete: all downloaded hashes match OSF and the 41 × 10,063 word and 41 ×
   30 passage grids are complete. ~~Create an outcome-blind, prose-free machine
   inventory before reading any eye/proficiency/comprehension outcome.~~ Complete:
   285 OEWN-based leads across all passages (126 contiguous, 159 gapped), with
   item/member/gap and line-edge positions but no passage tokens. ~~Complete an
   outcome-blind contextual desk triage and bounded missed-lead pass.~~ Complete:
   43 occurrences across 32 forms are plausible in scope and ten manual hard
   cases remain unresolved; no contextual sense or participant outcome was
   used. Independent labels and adjudication are still required before an
   outcome join; both are deferred application work.
5. ~~Freeze a bounded Project Gutenberg frame from the pinned official catalog,
   with per-work rights, stable chapter/unit, version, extraction, queue, and
   stop rules before inspecting target content.~~ Complete: 40 metadata-only
   candidates in each of two audience strata are fixed before ebook acquisition
   or MWE search. The first 13 exact artifacts have completed their mechanical
   gate; batch 2 adds one further pass after 16 ready files and one adaptation-
   provenance hold. Batch 3 adds seven passes from 15 ready files, five
   overlength exclusions, and three unfrozen-unit-type exclusions. The combined
   yield is 10/44—three adult/unspecified and seven juvenile. The final
   metadata-only screen finds only five rights-eligible adult/unspecified files,
   so that stratum can reach at most eight even if every file passes. Stop before
   batch-4 acquisition and preserve the failed frame. Do not freeze a replacement
   unless a later downstream application names the need.
6. Keep core occurrence/sense validity separate from empirical stimulus,
   open-material, coverage, eye-movement, and experimental evidence. Expand app
   senses only from the frozen core benchmark; do not let application-corpus
   convenience define the validated form inventory.

## Rights sources checked

- [eLife terms](https://elifesciences.org/terms)
- [Official eLife versioned article XML corpus](https://github.com/elifesciences/elife-article-xml)
- [VOA terms of use](https://learningenglish.voanews.com/p/5374.html)
- [VOA Learning English content-reuse statement](https://learningenglish.voanews.com/p/6861.html)
- [Wikimedia Terms of Use](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use)
- [Simple English Wikipedia About page](https://simple.wikipedia.org/wiki/Wikipedia:About)
- [Pinned 2026-08-01 Simple English Wikipedia dump](https://dumps.wikimedia.org/simplewiki/20260801/)
- [OpenStax licensing information](https://help.openstax.org/s/article/Licensing-information-of-OpenStax-textbooks)
- [Project Gutenberg terms of use](https://www.gutenberg.org/policy/terms_of_use.html)
- [Project Gutenberg offline catalogs](https://www.gutenberg.org/ebooks/offline_catalogs.html)
- [Project Gutenberg permission guidance](https://www.gutenberg.org/policy/permission)
- [Japan Agency for Cultural Affairs: term extension and wartime-addition Q&A](https://www.bunka.go.jp/seisaku/chosakuken/hokaisei/kantaiheiyo_chosakuken/1411890.html)
- [Project Gutenberg authority record for Edith K. Dunton / Margaret Warde](https://www.gutenberg.org/ebooks/author/35189)
- [American Film Institute record for *The Adventures of a Boy Scout*](https://catalog.afi.com/Film/13671-THE-ADVENTURES-OF-A-BOY-SCOUT)
- [TECO v1.1 OSF project](https://osf.io/wrvj3/)
- [TECO corpus article](https://doi.org/10.1016/j.rmal.2024.100123)
