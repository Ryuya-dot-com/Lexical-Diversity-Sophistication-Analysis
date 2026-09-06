# Sense inventory change governance

Status: IR-134 synthetic protocol exercise, 2026-09-05

This procedure governs non-destructive changes to project sense identity. It
does not admit a lexical sense, authorize human annotation, or validate the
synthetic meanings in the fixture.

## Version rule

- Patch: correct non-semantic metadata without changing identity, boundaries,
  mappings, or labels.
- Minor: add a type or sense without changing an existing meaning boundary.
- Major: change a meaning boundary or label interpretation, including a merge
  or split.
- Preserve every released version and its hash. Never erase or recycle an ID.
- If a test has been exposed or released, any sense-boundary change starts a
  new benchmark version. It cannot repair or tune the old test result.

## Required change record

Before changing an inventory, record the trigger, evidence partition, old and
new IDs, definitions, source fingerprints and rights, proposed version, affected
annotations, and whether any test labels, predictions, scores, or errors were
seen. A lexicographer reviews the meaning boundary; the PI approves study and
claim effects. A data steward also approves any changed source or release terms.
If sealed-test information was exposed, the custodian must confirm that the old
release remains sealed and the change is routed only to a new benchmark version.

Approval is prohibited when the proposal is justified by improving a test
metric, removing difficult cases, or fitting an exposed error. Training-only or
development evidence may motivate a prospective version, but the trigger and
approval must be recorded before the new version is evaluated.

## Non-destructive migration

- Split: deprecate the old ID, allocate at least two new IDs with `split_from`,
  and mark every old annotation `review_required_split`.
- Merge: deprecate all old IDs, allocate one new ID with `merged_from`, and mark
  every old annotation `review_required_merge`.
- Deprecated source: retain the project sense when its meaning is unchanged,
  retain the deprecated source link and reason, and add the replacement link.
- New out-of-inventory sense: allocate a new ID only after prospective review;
  keep old `out_of_inventory` annotations unchanged and mark them
  `review_required_new_inventory_sense`.

Migration records may suggest candidate IDs, but must set
`automatic_rewrite_applied` to false. A reviewer creates a new annotation record
against the new inventory; the old record remains reproducible against its exact
version.

## Exercise evidence

[`lifecycle_exercise.json`](../tests/fixtures/sense_inventory_versions/lifecycle_exercise.json)
contains one wholly synthetic old/new pair, the unchanged old annotations,
migration statuses, merge/split/source/OOI events, and the prospective approval
facts. `tests/test_sense_inventory.py` verifies its hashes and invariants. This
is a governance test only, not independent lexical or benchmark evidence.
