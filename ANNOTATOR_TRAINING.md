# Annotator training and qualification protocol

- Protocol version: 1.0.0
- Status: designed; not authorized, administered, or validated
- Scope: English VPC.full, VPC.semi, and VID annotation under
  `ANNOTATION_GUIDE.md` version `0.5.0-contextual-sense`

This protocol separates instruction, practice, feedback, and qualification.
It is not evidence that anyone is qualified. No person may be contacted or
observed until the responsible researcher records the applicable institutional
ethics/consent determination and data-management plan described in
`GOVERNANCE.md` and `resources/ethics_determination.md`.

## Permitted materials

Training uses only project-authored synthetic text from
`annotations/training_cases.json` and `annotations/hard_case_bank.json`. These
materials contain no human responses or natural benchmark items and may be
redistributed under MIT or CC BY 4.0. Do not use source documents, pilot,
development, holdout, or sealed-test items for instruction or qualification.

The current case answers are visible and are therefore practice keys, not
qualification evidence. All examples and responses remain training-only: they
must never enter benchmark prevalence estimates, system training/evaluation
splits, or independent gold labels.

## Stages

Complete the stages in order. Passing one stage cannot compensate for failure
in another.

1. **Teach-back.** After reading the guide, the annotator explains candidate,
   occurrence, member, gap, category, idiomaticity, inventory lookup, and
   contextual sense in their own words. They must also distinguish
   `multiple_assigned` from `ambiguous`, `abstained`, `out_of_inventory`,
   `inventory_ineligible`, and unfinished `unassigned`. Every domain must be
   clear before practice; no combined score is calculated.
2. **Guided practice.** The annotator completes the twelve cases in
   `annotations/training_cases.json` without seeing the decision key.
3. **Feedback.** The trainer reveals the key, identifies the first recoverable
   disagreement code, and asks the annotator to restate the responsible rule.
   Corrected answers are learning records, not qualification scores.
4. **Hard-case practice.** The annotator chooses an admissible route and gives
   a reason for every case in `annotations/hard_case_bank.json`. Because some
   cases permit more than one route, feedback evaluates the route and reason,
   not agreement with a hidden single gold label.
5. **Qualification.** Only after the first four stages, the annotator completes
   a separate, versioned synthetic form independently, without feedback, model
   suggestions, another annotator's labels, or access to its decision key.

## Qualification form

No qualification form is currently materialized. After the applicable work or study authorization
and before each cohort, the annotation lead must freeze a new project-authored
synthetic form that satisfies the item minima below. Store the form version,
guide and contract versions, item IDs, answer-key hash, and exposure record.
The retry uses a different, previously unexposed equivalent form.

This repository is public, so a committed form counts as exposed. Withhold the
answer key during administration, then release the form and key with the study
record. A later cohort must receive a new version. Do not treat secrecy as a
license exception: every form must remain project-authored or independently
cleared for redistribution.

## Task-specific gates

Thresholds are prospective operating rules, not validated cutoffs. Report each
numerator and denominator; do not calculate a total qualification score.

| Task | Minimum form composition | Pass rule |
|---|---|---|
| Occurrence | 12 decisions, including at least two literal/spatial negatives and two accidental sequences | Exact status accuracy at least .90, with zero `literal_or_spatial_promoted` or `accidental_sequence_promoted` sentinel errors |
| Member and gap span | 12 confirmed occurrences, including at least two pronoun insertions and two long gaps | Exact joint member-and-exhaustive-gap accuracy at least .90, with every pronoun and long-gap sentinel correct |
| Category | 12 exact confirmed spans: at least four each of VPC.full, VPC.semi, and VID | Three-class macro-F1 at least .80 and recall at least .75 in every class |
| Idiomaticity | 12 decisions covering `idiomatic`, `literal`, `ambiguous`, and `not_assessed` | Exact status accuracy at least .80, with every figurative-but-compositional, ambiguous, and not-assessed sentinel correct |
| Contextual sense | 15 matched-form decisions; at least three `assigned` and two each of `multiple_assigned`, `ambiguous`, `abstained`, `out_of_inventory`, and `inventory_ineligible` | On nonempty reference sets, assignment-state accuracy and exact unordered selected-set accuracy are each at least .80; every multiple-versus-ambiguous, abstention, OOI, and ineligibility sentinel is correct |

An annotator is qualified only for tasks whose own gate they pass. A category
pass cannot rescue a span failure, and high easy-item accuracy cannot rescue a
critical boundary error.

## Retraining and retry

On first failure, stop that task before production access. Show the relevant
rule and practice feedback, require a fresh teach-back of the failed boundary,
and provide new synthetic practice. The annotator may then make one attempt on
a new, unexposed, equivalent qualification form.

A second failure on the task, or repetition of its critical sentinel error,
excludes the annotator from production work on that task for the current guide
version. Do not add a third ad hoc attempt or average attempts. Passing other
tasks does not compensate. A substantive guide, contract, category boundary,
or sense-inventory change invalidates qualification for every affected task and
requires retraining plus a new form.

## Records after the work or study route is authorized

Retain only the approved pseudonymous annotator ID; guide, contract, training,
and form versions; dates; task numerators and denominators; critical-error
codes; pass/fail decision; retraining; and retry outcome. Keep recruitment and
contact data separately and do not collect unnecessary demographics. Use only
the institutionally approved storage, access, retention, withdrawal, and
deletion plan; this Dropbox-synced repository is not the default response store.

Stop before production if the applicable work/study authorization is absent, a form was exposed, a task
gate was not passed, a critical error recurs, or version identity cannot be
verified. The later pilot must report observed qualification and response-
process evidence; this protocol alone supplies none.
