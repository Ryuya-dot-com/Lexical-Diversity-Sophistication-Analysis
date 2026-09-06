# Annotation platform decision and dry-run record

- Decision version: 0.1.0
- Date: 2026-09-05
- Status: INCEpTION selected provisionally; format-level synthetic dry run passed;
  live-instance and two-user acceptance remain blocked
- Human data: none

## Decision

Use a locally or institutionally managed INCEpTION instance for independent
first-pass annotation if its responsible owner approves the host, access, and
data-management route. Keep this repository's browser app as a single-reviewer
inspection/export instrument; do not add accounts, shared storage, curation, or
team permissions to it.

| Option | Relevant fit | Decision |
|---|---|---|
| INCEpTION 41.5 target | Project-scoped roles, per-user annotation documents, workload assignment, curation, agreement views, custom span/link features, and full-fidelity UIMA CAS JSON export | Provisional production choice; live acceptance still required |
| FLAT | Multi-user permissions, FoLiA provenance, and Git-backed document history | Reserve fallback; its Django/FoLiA document-server stack and a second converter add no necessary capability for this task |
| Current browser app | Already preserves the project occurrence schema and raw local workspaces | Retain for individual review and QA only; it does not enforce blinded multi-user assignment or server-side audit history |

The comparison uses the current official documentation. INCEpTION 41.2
documents project roles, static assignments, curation, link features, and UIMA
CAS JSON; the project site lists 41.5 as the 2026-09-01 release. INCEpTION has no
immediate discontinuous-span object, but its guide explicitly prescribes links
or relations for that case. FLAT documents namespaces, configurable permissions,
provenance, and Git version history.

## Frozen INCEpTION representation

Use the Brat editor and exactly two custom span layers:

- `webanno.custom.MweMember`: one token-aligned span per lexical member;
  stacking enabled so overlapping and nested occurrences remain possible.
- `webanno.custom.MweOccurrence`: anchored on the verbal-head member, with a
  multi-valued `members` Link feature targeting `MweMember`. Link roles are
  consecutive `m1`, `m2`, ... in document order and are included in comparison.

`MweOccurrence` carries these primitive String features:

`occurrenceId`, `canonicalForm`, `status`, `category`, `decisionNote`,
`idiomaticityStatus`, `idiomaticityNote`, `formLookupStatus`,
`formInventoryId`, `formInventoryVersion`, `formEntryId`, `formSenseCount`, `senseLookupStatus`,
`senseInventoryId`, `senseInventoryVersion`, `candidateSenseIdsJson`,
`senseAssignmentStatus`, `selectedSenseIdsJson`, and `senseDecisionNote`.

The two `*SenseIdsJson` fields contain JSON arrays of stable IDs. This uses a
plain custom String feature that INCEpTION supports instead of relying on the
legacy WebAnno TSV multi-value representation, which the official guide warns
may omit unsupported information. The converter rejects malformed arrays,
unknown states, missing provenance notes, invalid inventory identities, and
selected IDs outside the candidate set.

Members come only from the Link targets. Gaps are deterministically rebuilt as
every frozen token strictly between the first and last member that is not a
member. UIMA CAS JSON offsets are UTF-16 units; conversion therefore verifies
each member against an exact token boundary before assigning project token IDs.

## Independence and audit configuration

For a live dry run, all of the following must be demonstrated on the exact
installed version:

1. Create two pseudonymous users with the Annotator role only. Do not grant
   Curator, Manager, instance administrator, project creator, Explorer,
   Agreement, or Workload access.
2. Use static assignment to give both users the same synthetic documents. Each
   signs in separately. Neither receives the other user's file, screen, label,
   agreement view, or curation view before both documents are locked finished.
3. Configure no recommender, active-learning session, external service,
   knowledge-base suggestion, or assistant. Confirm visually that no grey or
   ranked suggestion is displayed during first pass.
4. Only after both users finish, export each annotation document separately in
   UIMA CAS JSON 0.4.0 and export the full project backup. Preserve the raw
   exports and project log without editing.
5. Convert each file separately. Do not merge or curate before retaining both
   pre-adjudication records and their hashes.

The converter writes a pseudonymous annotator ID, raw-export SHA-256, converter
SHA-256, platform/version, conversion time, and an explicit untrusted-timestamp
flag. The INCEpTION project backup also contains its project log. Together, the
unchanged raw export, backup/log, and converted record form the audit trail;
the converter does not claim a trusted timestamp or authorship proof.

## Synthetic format dry run

Run:

```sh
python3 scripts/convert_annotation_export.py --self-test
```

The embedded project-authored UIMA CAS JSON fixture contains one discontinuous
VPC with a two-token gap and two jointly applicable sense IDs, plus one VID
marked out of inventory. The 2026-09-05 result is `PASS`: member order, both gap
IDs, both selected senses, OOI, and the conversion audit event survive. This is
a converter/format check, not evidence from an INCEpTION installation or human
annotators.

For a real exported document:

```sh
python3 scripts/convert_annotation_export.py RAW.json OUTPUT.json \
  --annotator-id A01 --converted-at 2026-09-05T00:00:00Z \
  --platform-version 41.5
```

## Stop and acceptance rules

Do not upload production text or person-linked records until the responsible
owner approves the server, location, administrators, accounts, backups,
retention, withdrawal, and deletion route. A synthetic two-user dry run may
proceed once the host and security route are authorized; ethics review is an
additional condition only if the run is used to study people. The technical
task remains open until the instance shows mutual invisibility, no first-pass
suggestions, lossless export through this converter, and a retained project
log. If any condition fails, test FLAT or an institutionally supported
equivalent; do not build team features into the browser app.

## Official sources

- [INCEpTION project and current release](https://inception-project.github.io/)
- [INCEpTION 41.2 user guide](https://inception-project.github.io/releases/41.2/docs/user-guide.html)
- [Apache UIMA CAS JSON specification](https://github.com/apache/uima-uimaj-io-jsoncas/blob/main/SPECIFICATION.adoc)
- [FLAT repository and documented features](https://github.com/proycon/flat)
