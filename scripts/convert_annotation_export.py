#!/usr/bin/env python3
"""Convert the frozen INCEpTION UIMA CAS JSON layer into project MWE records."""

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TOKEN_TYPE = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"
MEMBER_TYPE = "webanno.custom.MweMember"
OCCURRENCE_TYPE = "webanno.custom.MweOccurrence"
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def _utf16_boundaries(text):
    offsets = {0: 0}
    units = 0
    for index, character in enumerate(text, 1):
        units += len(character.encode("utf-16-le")) // 2
        offsets[units] = index
    return offsets


def _array(refs, owner, feature, expected_type):
    reference = owner.get(f"@{feature}")
    value = refs.get(reference)
    if not value or value.get("%TYPE") != expected_type:
        raise ValueError(f"{feature} must reference {expected_type}")
    elements = value.get("%ELEMENTS")
    if not isinstance(elements, list):
        raise ValueError(f"{feature} array is invalid")
    return elements


def _required_text(item, feature):
    value = item.get(feature)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{feature} must be non-empty text")
    return value.strip()


def _optional_text(item, feature):
    value = item.get(feature)
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        raise ValueError(f"{feature} must be text or null")
    return value


def _json_string_list(item, feature):
    try:
        values = json.loads(_required_text(item, feature))
    except json.JSONDecodeError as error:
        raise ValueError(f"{feature} must be a JSON array string") from error
    if not isinstance(values, list):
        raise ValueError(f"{feature} must be a JSON array string")
    return values


def _decision(source, note, required):
    if required and (not note or not note.strip()):
        raise ValueError("terminal decisions require a note")
    return {"source": source, "note": note} if note else None


def convert(document, source_bytes, contract, annotator_id, converted_at, source_name, platform_version):
    if not isinstance(source_bytes, bytes):
        raise ValueError("source_bytes must be the unchanged raw export")
    source_document = json.loads(source_bytes.decode("utf-8", errors="strict"))
    # JSON comparison keeps True distinct from 1 without depending on key order.
    if (not isinstance(source_document, dict)
            or json.dumps(document, sort_keys=True, allow_nan=False)
            != json.dumps(source_document, sort_keys=True, allow_nan=False)):
        raise ValueError("document does not match the source_bytes JSON object")
    document = source_document
    if not ID_PATTERN.fullmatch(annotator_id):
        raise ValueError("annotator ID must be pseudonymous ASCII text")
    try:
        timestamp = datetime.fromisoformat(converted_at.replace("Z", "+00:00"))
        if timestamp.utcoffset() is None:
            raise ValueError
    except (AttributeError, ValueError) as error:
        raise ValueError("converted_at must be an ISO timestamp") from error

    structures = document.get("%FEATURE_STRUCTURES")
    if not isinstance(structures, list):
        raise ValueError("missing UIMA CAS feature structures")
    refs = {item.get("%ID"): item for item in structures}
    if None in refs or len(refs) != len(structures):
        raise ValueError("feature-structure IDs must be present and unique")

    sofas = [item for item in structures if item.get("%TYPE") == "uima.cas.Sofa"]
    if len(sofas) != 1 or not isinstance(sofas[0].get("sofaString"), str):
        raise ValueError("exactly one text Sofa is required")
    text = sofas[0]["sofaString"]
    boundaries = _utf16_boundaries(text)

    tokens = sorted(
        (item for item in structures if item.get("%TYPE") == TOKEN_TYPE),
        key=lambda item: (item.get("^begin", -1), item.get("^end", -1)),
    )
    if not tokens:
        raise ValueError("the export contains no tokens")
    token_by_span = {}
    token_ids = {}
    previous_end = -1
    for position, token in enumerate(tokens, 1):
        begin, end = token.get("^begin"), token.get("^end")
        if begin not in boundaries or end not in boundaries or begin >= end or begin < previous_end:
            raise ValueError("token offsets are invalid or overlapping")
        token_id = f"t{position}"
        token_by_span[(begin, end)] = token_id
        token_ids[token_id] = position - 1
        previous_end = end

    states = contract["occurrence_record"]
    source = f"inception-{platform_version}:{annotator_id}"
    occurrences = []
    for item in structures:
        if item.get("%TYPE") != OCCURRENCE_TYPE:
            continue
        links = _array(refs, item, "members", "uima.cas.FSArray")
        members = []
        member_spans = []
        for link_ref in links:
            link = refs.get(link_ref)
            target = refs.get((link or {}).get("@target"))
            role = (link or {}).get("role")
            if not target or target.get("%TYPE") != MEMBER_TYPE or not re.fullmatch(r"m[1-9][0-9]*", role or ""):
                raise ValueError("members must be ordered MweMember links named m1, m2, ...")
            span = (target.get("^begin"), target.get("^end"))
            if span not in token_by_span:
                raise ValueError("each MweMember must match exactly one frozen token")
            members.append((int(role[1:]), token_by_span[span]))
            member_spans.append(span)
        members.sort()
        if [order for order, _ in members] != list(range(1, len(members) + 1)):
            raise ValueError("member roles must be consecutive")
        member_token_ids = [token_id for _, token_id in members]
        if len(member_token_ids) < 2 or len(set(member_token_ids)) != len(member_token_ids):
            raise ValueError("an occurrence requires at least two unique members")
        member_positions = [token_ids[token_id] for token_id in member_token_ids]
        if member_positions != sorted(member_positions):
            raise ValueError("member roles must follow document order")
        if (item.get("^begin"), item.get("^end")) not in member_spans:
            raise ValueError("MweOccurrence must be anchored on one of its members")
        gap_token_ids = [
            f"t{position + 1}"
            for position in range(member_positions[0] + 1, member_positions[-1])
            if f"t{position + 1}" not in member_token_ids
        ]

        status = _required_text(item, "status")
        category = _required_text(item, "category")
        idiomaticity_status = _required_text(item, "idiomaticityStatus")
        form_status = _required_text(item, "formLookupStatus")
        sense_lookup = _required_text(item, "senseLookupStatus")
        assignment = _required_text(item, "senseAssignmentStatus")
        if status not in states["statuses"] or category not in states["categories"]:
            raise ValueError("unknown occurrence status or category")
        if idiomaticity_status not in states["idiomaticity_statuses"]:
            raise ValueError("unknown idiomaticity status")
        if form_status not in states["form_lookup_statuses"]:
            raise ValueError("unknown form lookup status")
        if sense_lookup not in states["sense_lookup_statuses"]:
            raise ValueError("unknown sense lookup status")
        if assignment not in states["sense_assignment_statuses"]:
            raise ValueError("unknown sense assignment status")

        candidates = _json_string_list(item, "candidateSenseIdsJson")
        selected = _json_string_list(item, "selectedSenseIdsJson")
        if any(not isinstance(value, str) or not value for value in candidates + selected):
            raise ValueError("sense IDs must be non-empty strings")
        if len(candidates) != len(set(candidates)) or len(selected) != len(set(selected)):
            raise ValueError("sense IDs must be unique")
        if not set(selected) <= set(candidates):
            raise ValueError("selected senses must be inventory candidates")
        required_selected = {"assigned": 1, "multiple_assigned": 2, "ambiguous": 2}
        if assignment in required_selected and len(selected) < required_selected[assignment]:
            raise ValueError("sense assignment has too few selected senses")
        if assignment == "assigned" and len(selected) != 1:
            raise ValueError("assigned requires exactly one selected sense")
        if assignment not in required_selected and selected:
            raise ValueError("this sense state cannot select senses")
        if assignment in {*required_selected, "abstained"} and sense_lookup != "matched":
            raise ValueError("selected or abstained states require a matched inventory")
        if assignment == "out_of_inventory" and sense_lookup not in {"matched", "out_of_inventory"}:
            raise ValueError("OOI assignment requires a completed inventory search")
        if assignment == "inventory_ineligible" and sense_lookup != "inventory_ineligible":
            raise ValueError("inventory ineligibility states must agree")
        if sense_lookup in {"out_of_inventory", "inventory_ineligible"} and assignment != sense_lookup:
            raise ValueError("sense lookup and assignment states must agree")
        if sense_lookup == "matched" and not candidates:
            raise ValueError("matched sense lookup requires candidates")
        if sense_lookup != "matched" and candidates:
            raise ValueError("only matched sense lookup can carry candidates")
        if status == "candidate" and idiomaticity_status != "not_assessed":
            raise ValueError("unresolved candidates cannot carry idiomaticity decisions")
        if status != "confirmed" and (
            form_status != "not_attempted"
            or sense_lookup != "not_attempted"
            or assignment != "unassigned"
        ):
            raise ValueError("non-confirmed occurrences cannot carry downstream decisions")

        terminal = status in {"confirmed", "rejected"}
        decision_note = _optional_text(item, "decisionNote")
        idiom_note = _optional_text(item, "idiomaticityNote")
        sense_note = _optional_text(item, "senseDecisionNote")
        decided_sense = assignment != "unassigned"
        if (not terminal and decision_note) or (idiomaticity_status == "not_assessed" and idiom_note) or (not decided_sense and sense_note):
            raise ValueError("unfinished states cannot carry terminal decision notes")
        form_inventory_id = _optional_text(item, "formInventoryId")
        form_inventory_version = _optional_text(item, "formInventoryVersion")
        sense_inventory_id = _optional_text(item, "senseInventoryId")
        sense_inventory_version = _optional_text(item, "senseInventoryVersion")
        if form_status == "not_attempted" and (form_inventory_id or form_inventory_version):
            raise ValueError("unattempted form lookup cannot name an inventory")
        if form_status != "not_attempted" and not (form_inventory_id and form_inventory_version):
            raise ValueError("attempted form lookup must name an inventory and version")
        form_entry_id = _optional_text(item, "formEntryId")
        if form_status == "matched" and not form_entry_id:
            raise ValueError("matched form lookup requires an entry ID")
        if form_status != "matched" and form_entry_id:
            raise ValueError("unmatched form lookup cannot carry an entry ID")
        form_sense_count = item.get("formSenseCount")
        if form_sense_count is not None and (
            isinstance(form_sense_count, bool)
            or not isinstance(form_sense_count, int)
            or form_sense_count < 0
            or form_status != "matched"
        ):
            raise ValueError("formSenseCount must be a nonnegative integer on a matched form")
        if sense_lookup in {"not_attempted", "inventory_ineligible"} and (sense_inventory_id or sense_inventory_version):
            raise ValueError("this sense lookup cannot name an inventory")
        if sense_lookup in {"matched", "out_of_inventory"} and not (sense_inventory_id and sense_inventory_version):
            raise ValueError("attempted sense lookup must name an inventory and version")

        occurrences.append({
            "id": _required_text(item, "occurrenceId"),
            "canonical_form": _required_text(item, "canonicalForm"),
            "category": category,
            "status": status,
            "member_token_ids": member_token_ids,
            "gap_token_ids": gap_token_ids,
            "candidate_source": {"kind": "manual-open-text", "pattern_id": None},
            "decision": _decision(source, decision_note, terminal),
            "idiomaticity": {
                "status": idiomaticity_status,
                "decision": _decision(source, idiom_note, idiomaticity_status != "not_assessed"),
            },
            "form_lookup": {
                "inventory_id": form_inventory_id,
                "inventory_version": form_inventory_version,
                "status": form_status,
                "entry_id": form_entry_id,
                "sense_count": form_sense_count,
            } if status == "confirmed" else None,
            "sense": {
                "inventory_id": sense_inventory_id,
                "inventory_version": sense_inventory_version,
                "lookup_status": sense_lookup,
                "candidate_sense_ids": candidates,
                "assignment_status": assignment,
                "selected_sense_ids": selected,
                "decision": _decision(source, sense_note, decided_sense),
            } if status == "confirmed" else None,
        })

    if not occurrences:
        raise ValueError("the export contains no MweOccurrence annotations")
    if len({item["id"] for item in occurrences}) != len(occurrences):
        raise ValueError("occurrence IDs must be unique")
    converter_hash = _sha256_bytes(Path(__file__).read_bytes())
    return {
        "schema_version": "1.0.0-independent-annotation",
        "contract_version": contract["contract_version"],
        "platform": "INCEpTION",
        "platform_version": platform_version,
        "annotator_id": annotator_id,
        "document": {
            "text_sha256_utf8": _sha256_bytes(text.encode()),
            "token_count": len(tokens),
            "occurrences": occurrences,
        },
        "audit_event": {
            "event": "annotation_export_converted",
            "converted_at": converted_at,
            "timestamp_trusted": False,
            "source_name": source_name,
            "source_sha256": _sha256_bytes(source_bytes),
            "converter": "scripts/convert_annotation_export.py",
            "converter_sha256": converter_hash,
        },
    }


def _synthetic_cas():
    text = "They gave the proposal up, then made do."
    structures = [{"%ID": 1, "%TYPE": "uima.cas.Sofa", "sofaString": text}]
    spans = [(0, 4), (5, 9), (10, 13), (14, 22), (23, 25), (27, 31), (32, 36), (37, 39)]
    structures.extend(
        {"%ID": index + 2, "%TYPE": TOKEN_TYPE, "@sofa": 1, "^begin": begin, "^end": end}
        for index, (begin, end) in enumerate(spans)
    )
    structures.extend([
        {"%ID": 20, "%TYPE": MEMBER_TYPE, "@sofa": 1, "^begin": 5, "^end": 9},
        {"%ID": 21, "%TYPE": MEMBER_TYPE, "@sofa": 1, "^begin": 23, "^end": 25},
        {"%ID": 22, "%TYPE": MEMBER_TYPE, "@sofa": 1, "^begin": 32, "^end": 36},
        {"%ID": 23, "%TYPE": MEMBER_TYPE, "@sofa": 1, "^begin": 37, "^end": 39},
        {"%ID": 40, "%TYPE": "webanno.custom.MweOccurrenceMembersLink", "role": "m1", "@target": 20},
        {"%ID": 41, "%TYPE": "webanno.custom.MweOccurrenceMembersLink", "role": "m2", "@target": 21},
        {"%ID": 42, "%TYPE": "uima.cas.FSArray", "%ELEMENTS": [40, 41]},
        {"%ID": 43, "%TYPE": "webanno.custom.MweOccurrenceMembersLink", "role": "m1", "@target": 22},
        {"%ID": 44, "%TYPE": "webanno.custom.MweOccurrenceMembersLink", "role": "m2", "@target": 23},
        {"%ID": 45, "%TYPE": "uima.cas.FSArray", "%ELEMENTS": [43, 44]},
        {
            "%ID": 60, "%TYPE": OCCURRENCE_TYPE, "@sofa": 1, "^begin": 5, "^end": 9,
            "@members": 42, "occurrenceId": "dry-o1", "canonicalForm": "give up",
            "status": "confirmed", "category": "VPC.full", "decisionNote": "Synthetic decision.",
            "idiomaticityStatus": "idiomatic", "idiomaticityNote": "Synthetic decision.",
            "formLookupStatus": "matched", "formInventoryId": "oewn",
            "formInventoryVersion": "2025", "formEntryId": "give up#v", "formSenseCount": 3,
            "senseLookupStatus": "matched", "senseInventoryId": "synthetic-inventory",
            "senseInventoryVersion": "1", "candidateSenseIdsJson": "[\"sense-a\",\"sense-b\",\"sense-c\"]",
            "senseAssignmentStatus": "multiple_assigned", "selectedSenseIdsJson": "[\"sense-a\",\"sense-b\"]",
            "senseDecisionNote": "Both synthetic meanings apply."
        },
        {
            "%ID": 61, "%TYPE": OCCURRENCE_TYPE, "@sofa": 1, "^begin": 32, "^end": 36,
            "@members": 45, "occurrenceId": "dry-o2", "canonicalForm": "make do",
            "status": "confirmed", "category": "VID", "decisionNote": "Synthetic decision.",
            "idiomaticityStatus": "idiomatic", "idiomaticityNote": "Synthetic decision.",
            "formLookupStatus": "out_of_inventory", "formInventoryId": "oewn",
            "formInventoryVersion": "2025", "formEntryId": None,
            "senseLookupStatus": "out_of_inventory", "senseInventoryId": "synthetic-inventory",
            "senseInventoryVersion": "1", "candidateSenseIdsJson": "[]",
            "senseAssignmentStatus": "out_of_inventory", "selectedSenseIdsJson": "[]",
            "senseDecisionNote": "Complete permitted search found no adequate sense."
        },
    ])
    return {
        "%HEADER": {"%VERSION": "0.4.0"},
        "%TYPES": {},
        "%FEATURE_STRUCTURES": structures,
        "%VIEWS": {"_InitialView": {"%SOFA": 1, "%MEMBERS": [item["%ID"] for item in structures[1:]]}},
    }


def self_test(contract):
    document = _synthetic_cas()
    source_bytes = json.dumps(document, ensure_ascii=False, separators=(",", ":")).encode()
    converted = convert(
        document, source_bytes, contract, "SYN-A", "2026-09-05T00:00:00Z",
        "project-authored-synthetic-cas.json", "41.5-format-target",
    )
    first, second = converted["document"]["occurrences"]
    assert first["member_token_ids"] == ["t2", "t5"]
    assert first["gap_token_ids"] == ["t3", "t4"]
    assert first["sense"]["selected_sense_ids"] == ["sense-a", "sense-b"]
    assert first["sense"]["assignment_status"] == "multiple_assigned"
    assert second["sense"]["assignment_status"] == "out_of_inventory"
    assert converted["audit_event"]["source_sha256"]
    return {
        "status": "PASS",
        "synthetic_only": True,
        "occurrence_count": 2,
        "discontinuous_gap_preserved": True,
        "multiple_senses_preserved": True,
        "out_of_inventory_preserved": True,
        "audit_event_preserved": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("output", nargs="?", type=Path,
                        help="New output path; existing files are never overwritten")
    parser.add_argument("--contract", type=Path, default=ROOT / "mwe_contract.json")
    parser.add_argument("--annotator-id")
    parser.add_argument("--converted-at")
    parser.add_argument("--platform-version", default="41.5")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    if args.self_test:
        print(json.dumps(self_test(contract), indent=2, sort_keys=True))
        return
    if not all((args.input, args.output, args.annotator_id, args.converted_at)):
        parser.error("input, output, --annotator-id, and --converted-at are required")
    source_bytes = args.input.read_bytes()
    document = json.loads(source_bytes.decode("utf-8", errors="strict"))
    converted = convert(
        document, source_bytes, contract, args.annotator_id, args.converted_at,
        args.input.name, args.platform_version,
    )
    serialized = json.dumps(converted, indent=2) + "\n"
    try:
        with args.output.open("x", encoding="utf-8") as output:
            output.write(serialized)
    except FileExistsError:
        parser.error(f"Output already exists: {args.output}. Choose a new output path.")


if __name__ == "__main__":
    main()
