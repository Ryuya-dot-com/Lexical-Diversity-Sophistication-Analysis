# Downstream application selection memo

Status: accepted decision for IR-410, 2026-09-04

## Decision

No downstream application is selected for the first paper. Eye tracking,
reading comprehension, learner-text analysis, source recurrence, and broad
coverage remain possible later studies; none is a dependency of the Web app,
the core benchmark, or the first paper's technical claims.

The core evidence target is agreement with independent human decisions about
VPC/VID occurrence, members and gaps, category, idiomaticity, contextual sense,
ambiguity, abstention, and out-of-inventory use. Reading time, regressions,
comprehension, proficiency, and corpus frequency are different outcomes and
cannot validate those labels.

## Candidate dispositions

| Candidate | First-paper decision | Reason |
|---|---|---|
| Word/MWE coverage | Not selected | Describes resource incidence but does not establish occurrence or sense validity. |
| Learner-text robustness | Not selected | Changes the target population and needs its own lawful, independently annotated sample. |
| Source recurrence | Not selected | Adds a corpus-distribution question rather than evidence for the core labels. |
| Eye tracking | Not selected | Adds a cognitive-processing question, participant-data governance, stimulus rights, and a separate statistical model. |
| Reading comprehension | Not selected | Adds a behavioral-outcome question and cannot be inferred from technical accuracy. |

TECO is the closest reviewed option for Japanese L2 readers, but its gaze and
general proficiency variables are not occurrence-specific MWE gold. Its Eiken
stimuli and reconstructable token sequences also remain outside every public
repository, GitHub Pages build, download, and API response pending written
downstream-redistribution evidence. Contact with the TECO authors is therefore
a non-blocking rights clarification, not a core-development gate.

Other eye-movement resources do not remove the construct/rights split:
MECO-L2 offers a larger cross-L1 sample but uses ACCUPLACER-derived passages;
CELER requires separately licensed PTB-WSJ/BLLIP text; GECO studies
monolingual/bilingual novel reading rather than Japanese L2 MWE decisions; and
the 2026 Santos et al. idiom release remains quarantined under the recorded
data-consistency audit. No one resource supplies independent VPC/VID gold,
Japanese-L2 processing outcomes, and clearly sublicensable stimulus text.

## Re-entry gate

A downstream study may begin only after the core benchmark is frozen and all
of the following are true:

1. One explicit hypothesis requires a behavioral or corpus outcome.
2. The chosen resource matches that hypothesis and target population.
3. Artifact-level stimulus, participant-data, and redistribution review passes.
4. Outcomes, joins, exclusions, covariates, missingness, multiplicity, and
   sensitivity analyses are frozen before any outcome join.
5. The study is reported as a separate downstream claim, never as validation
   of the core linguistic labels.

Until then, the repository may publish only code, rights/provenance metadata,
prose-free identifiers, and separately reviewed non-reconstructive aggregates.
No eye-movement corpus, participant row, restricted stimulus, or reconstructive
token sequence is a runtime or API dependency.

## Evidence boundary

This decision used source and rights metadata already recorded in `RIGHTS.md`
and `resources/teco_v1_1_candidate_manifest.json`. It did not inspect a new
outcome, change an annotation rule, or expose a sealed test.
