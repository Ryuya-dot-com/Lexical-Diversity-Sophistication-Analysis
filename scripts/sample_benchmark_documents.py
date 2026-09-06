#!/usr/bin/env python3
"""Build target-blind Wikipedia sampling priority queues from metadata rows."""

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from reconstruct_benchmark import stable_id


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "resources/sampling_frame.json"
DEFAULT_FIXTURE = ROOT / "tests/fixtures/sampling_candidates.jsonl"
HEX64 = set("0123456789abcdef")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def require_integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def require_sha256(value, name):
    if not isinstance(value, str) or len(value) != 64 or any(
        character not in HEX64 for character in value
    ):
        raise ValueError(f"{name} must be a lowercase SHA-256")


def validate_dependencies(contract):
    for name, dependency in contract["dependencies"].items():
        path = ROOT / dependency["path"]
        if sha256(path.read_bytes()) != dependency["sha256"]:
            raise ValueError(f"dependency SHA-256 mismatch: {name}")


def load_rows(path):
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid JSON on line {line_number}") from error
        if not isinstance(row, dict):
            raise ValueError(f"line {line_number} must contain an object")
        rows.append(row)
    return rows


def validate_row(row, required_fields, rights_statuses):
    if set(row) != set(required_fields):
        missing = sorted(set(required_fields) - set(row))
        extra = sorted(set(row) - set(required_fields))
        raise ValueError(f"candidate schema mismatch; missing={missing}, extra={extra}")
    for name in ("page_id", "revision_id"):
        require_integer(row[name], name, 1)
    for name in ("namespace", "prose_token_count", "retained_paragraph_count"):
        require_integer(row[name], name)
    if not isinstance(row["redirect"], bool):
        raise ValueError("redirect must be boolean")
    if not isinstance(row["title"], str) or not row["title"].strip():
        raise ValueError("title must be nonempty")
    if not isinstance(row["model"], str) or not row["model"]:
        raise ValueError("model must be nonempty")
    timestamp = row["revision_timestamp"]
    if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
        raise ValueError("revision_timestamp must be an ISO-8601 UTC value")
    try:
        datetime.fromisoformat(timestamp[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError("revision_timestamp must be an ISO-8601 UTC value") from error
    for name in (
        "dump_wikitext_sha256",
        "api_response_sha256",
        "rendered_html_sha256",
        "extracted_text_sha256",
    ):
        require_sha256(row[name], name)
    if row["rights_status"] not in rights_statuses:
        raise ValueError("unsupported rights_status")
    reasons = row["rights_reason_codes"]
    if not isinstance(reasons, list) or any(
        not isinstance(reason, str) or not reason for reason in reasons
    ):
        raise ValueError("rights_reason_codes must be a list of nonempty strings")
    if row["rights_status"] in {"pass", "not_reviewed"} and reasons:
        raise ValueError("pass/not_reviewed rights rows cannot have reason codes")
    if row["rights_status"] in {"hold", "fail"} and not reasons:
        raise ValueError("hold/fail rights rows require reason codes")
    if row["target_exposure_status"] != "unexposed":
        raise ValueError("candidate row is not target-blind")


def structural_exclusions(row):
    reasons = []
    if row["namespace"] != 0:
        reasons.append("namespace_not_zero")
    if row["redirect"]:
        reasons.append("redirect")
    if row["model"] != "wikitext":
        reasons.append("model_not_wikitext")
    if row["prose_token_count"] < 500:
        reasons.append("below_500_tokens")
    if row["prose_token_count"] > 3999:
        reasons.append("above_3999_tokens")
    if row["retained_paragraph_count"] < 5:
        reasons.append("fewer_than_5_paragraphs")
    return reasons


def length_stratum(contract, token_count):
    matches = [
        item["id"]
        for item in contract["length_strata"]
        if item["minimum_tokens"] <= token_count <= item["maximum_tokens"]
    ]
    if len(matches) != 1:
        raise ValueError(f"eligible token count has {len(matches)} length strata")
    return matches[0]


def admission_state(rights_status):
    return {
        "not_reviewed": "queued_for_rights_review",
        "pass": "rights_pass_candidate",
        "hold": "held_rights",
        "fail": "excluded_rights",
    }[rights_status]


def build(contract, rows):
    validate_dependencies(contract)
    required_fields = contract["candidate_input"]["required_fields"]
    rights_statuses = set(contract["candidate_input"]["rights_statuses"])
    seen_pages = set()
    seen_revisions = set()
    queues = {item["id"]: [] for item in contract["length_strata"]}
    exclusions = []

    canonical_input = []
    for row in rows:
        validate_row(row, required_fields, rights_statuses)
        if row["page_id"] in seen_pages or row["revision_id"] in seen_revisions:
            raise ValueError("duplicate page_id or revision_id")
        seen_pages.add(row["page_id"])
        seen_revisions.add(row["revision_id"])
        canonical_input.append([row[field] for field in required_fields])

        reasons = structural_exclusions(row)
        if reasons:
            exclusions.append({
                "page_id": row["page_id"],
                "revision_id": row["revision_id"],
                "exclusion_codes": reasons,
            })
            continue

        stratum = length_stratum(contract, row["prose_token_count"])
        immutable_source_id = (
            f'enwiki:page:{row["page_id"]}:revision:{row["revision_id"]}'
        )
        selection_payload = [
            contract["frame_id"],
            contract["selection"]["seed"],
            row["page_id"],
            row["revision_id"],
        ]
        queues[stratum].append({
            "page_id": row["page_id"],
            "revision_id": row["revision_id"],
            "revision_timestamp": row["revision_timestamp"],
            "title": row["title"],
            "immutable_source_id": immutable_source_id,
            "document_id": stable_id("doc", ["document-v1", immutable_source_id]),
            "extracted_text_sha256": row["extracted_text_sha256"],
            "prose_token_count": row["prose_token_count"],
            "retained_paragraph_count": row["retained_paragraph_count"],
            "length_stratum": stratum,
            "selection_hash": sha256(compact(selection_payload).encode("utf-8")),
            "rights_status": row["rights_status"],
            "rights_reason_codes": row["rights_reason_codes"],
            "admission_state": admission_state(row["rights_status"]),
            "selected": False,
        })

    for queue in queues.values():
        queue.sort(key=lambda item: (
            item["selection_hash"], item["page_id"], item["revision_id"]
        ))
        for rank, item in enumerate(queue, 1):
            item["queue_rank"] = rank

    exclusions.sort(key=lambda item: (item["page_id"], item["revision_id"]))
    state_counts = Counter(
        item["admission_state"] for queue in queues.values() for item in queue
    )
    canonical_input.sort(key=lambda item: (item[0], item[1]))
    return {
        "schema_version": "1.0.0",
        "frame_id": contract["frame_id"],
        "status": "target_blind_priority_queues_no_documents_selected",
        "source_snapshot": contract["population"]["source_snapshot"],
        "input_rows_sha256": sha256(compact(canonical_input).encode("utf-8")),
        "summary": {
            "source_row_count": len(rows),
            "queued_row_count": sum(map(len, queues.values())),
            "structurally_excluded_row_count": len(exclusions),
            "queue_count_by_stratum": {
                name: len(queue) for name, queue in queues.items()
            },
            "admission_state_counts": dict(sorted(state_counts.items())),
            "selected_document_count": 0,
            "target_search_count": 0,
        },
        "allocation_status": contract["selection"]["allocation_status"],
        "queues": queues,
        "structural_exclusions": exclusions,
    }


def self_check():
    contract = json.loads(DEFAULT_CONTRACT.read_text(encoding="utf-8"))
    result = build(contract, load_rows(DEFAULT_FIXTURE))
    assert result["summary"]["source_row_count"] == 12
    assert result["summary"]["queued_row_count"] == 6
    assert result["summary"]["selected_document_count"] == 0
    assert all(
        [item["queue_rank"] for item in queue] == list(range(1, len(queue) + 1))
        for queue in result["queues"].values()
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates", type=Path, nargs="?")
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_check:
            self_check()
            print("Wikipedia sampling-frame self-check: PASS")
            return
        if args.candidates is None:
            parser.error("candidates JSONL is required")
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
        result = build(contract, load_rows(args.candidates))
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
            print(f"Wrote {args.output}")
        else:
            print(rendered, end="")
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")


if __name__ == "__main__":
    main()
