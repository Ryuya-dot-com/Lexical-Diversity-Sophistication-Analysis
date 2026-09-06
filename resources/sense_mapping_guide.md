# IR-130 bounded VID mapping guide 1.0.0

Status: machine candidate generation complete; independent review and source
admission pending (2026-09-04).

This guide applies only to the 146 STREUSLE 5.0 `V.VID` canonical types in
`sense_mapping_queue.json`. It distinguishes a bounded-source mapping route
from absence of such a route. It does not create contextual gold, a new sense,
or proof that an expression is absent from English.

## Frozen order and limits

The order is the one frozen in
`hybrid_sense_inventory_contract_2026_09_03.json`:

1. exact OEWN 2025 verb entry (already completed);
2. unique fixed closed-class slot skeleton (already completed);
3. exact English Wiktionary verb entry (already completed);
4. source-declared OEWN `form`/`also` and Wiktionary
   `forms`/`alt_of`/`form_of` fields;
5. orthographic equivalence only; and
6. review of the resulting closed candidate set.

Stage 5 uses NFKC, Unicode casefolding, collapsed whitespace, equivalence of
listed Unicode dash characters with a hyphen/space boundary, and equivalence
of listed Unicode apostrophes with ASCII apostrophe. It never deletes,
substitutes, or reorders an open-class member.

The source limit is exactly two pinned resources: OEWN 2025 and the English
Wiktionary verb extraction identified in the queue. No free Web or additional
dictionary search is allowed. A reviewer may spend at most 15 minutes per
candidate-bearing type and an adjudicator at most another 15 minutes. When the
limit is reached, retain `candidate_only` or `unresolved`; do not add a
candidate from memory.

## Review procedure

For each queued candidate, verify its artifact hash, entry ID, record hash,
declared field, and normalization route. Reviewers may inspect the pinned local
record, but must not copy a gloss or example into this queue or use a held-out
occurrence, gold label, baseline prediction, mutable display ID, or gloss
similarity as semantic truth.

Record exactly one relation per candidate: `equivalent`, `broader`, `narrower`,
`overlapping`, or `candidate_only`. Two reviewers work independently. A
disagreement remains pending until a separately named adjudicator records the
decision and rationale. Preserve every rejected or unresolved candidate in the
audit trail.

The type-level states mean:

- `mapped`: an `equivalent` link has independent verification, its complete
  source identity passes the contract, and its rights state permits admission;
- `candidate_set`: one or more bounded candidates exist but review or source
  admission is incomplete;
- `OOI_pending`: a later, separately authorized lexicographic phase has evidence
  for a new project sense; dictionary non-match alone can never set this state;
- `unresolved`: the bounded sources were exhausted without an admissible route.

The queue's 146 opaque type IDs are permanently reserved and must not be
reassigned. A review creates a versioned successor record; it does not rewrite
the frozen input or remove exact misses from the 146-type/169-occurrence
denominator.

## Current result and stop

The deterministic pass yields candidate sets for 3 types and no bounded route
for 143. `unresolved` is therefore a procedure result, not a claim of a true
inventory gap. No type is yet `mapped` or `OOI_pending`, and no source sense or
human annotation has entered the Web app.

The raw OEWN and Kaikki artifacts remain local and ignored. The public queue
contains canonical type identifiers, source-entry identifiers, declared
variant strings, and fingerprints, but no corpus sentence, dictionary gloss,
example, translation, or contextual label. Retain
`STREUSLE_NOTICE.md`, `WIKTIONARY_KAIKKI_NOTICE.md`, and
`OEWN_WORDNET_NOTICE.txt` with every redistribution.
