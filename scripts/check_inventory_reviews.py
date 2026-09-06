#!/usr/bin/env python3
"""Create and validate privacy-bounded independent inventory review files."""

import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "resources/inventory_review_protocol.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_evidence(candidate):
    has_gloss = bool(candidate.get("definition", {}).get("text"))
    examples = candidate.get("examples", {}).get("items", {})
    has_example = any(examples.values())
    if has_gloss and has_example:
        return "gloss_and_example"
    if has_gloss:
        return "gloss_only"
    return "insufficient_source_evidence"


def polysemy_audit(inventory):
    counts = []
    per_form = []
    by_family = {family: {"forms": 0, "candidates": 0, "candidate_pairs": 0}
                 for family in ("VPC", "VID")}
    source_routes = {}
    candidates = []
    for item in inventory["types"]:
        current = item["candidate_set"]["candidates"]
        count = len(current)
        pairs = count * (count - 1) // 2
        family = "VPC" if any("VPC" in category for category in item["observed_vmwe_categories"]) else "VID"
        route = item["candidate_set"]["mapping_route"]
        without_examples = sum(source_evidence(candidate) == "gloss_only" for candidate in current)
        counts.append(count)
        candidates.extend(current)
        by_family[family]["forms"] += 1
        by_family[family]["candidates"] += count
        by_family[family]["candidate_pairs"] += pairs
        route_counts = source_routes.setdefault(route, {"forms": 0, "candidates": 0})
        route_counts["forms"] += 1
        route_counts["candidates"] += count
        per_form.append({
            "type_id": item["type_id"],
            "canonical_lemma": item["canonical_lemma"],
            "family": family,
            "observed_categories": item["observed_vmwe_categories"],
            "route": route,
            "candidates": count,
            "candidate_pairs": pairs,
            "candidates_without_examples": without_examples,
        })
    sorted_counts = sorted(counts)
    return {
        "forms": len(counts),
        "candidates": len(candidates),
        "candidate_pairs_if_exhaustive": sum(row["candidate_pairs"] for row in per_form),
        "candidate_count": {
            "minimum": min(counts),
            "median": sorted_counts[len(sorted_counts) // 2],
            "maximum": max(counts),
            "mean": round(sum(counts) / len(counts), 6),
        },
        "by_family": by_family,
        "source_routes": source_routes,
        "source_evidence": {
            "unique_definitions": len({candidate["definition"]["text"] for candidate in candidates}),
            "unique_synsets": len({candidate["source_synset_id"] for candidate in candidates}),
            "unique_ili": len({candidate["cili"]["ili"] for candidate in candidates}),
            "candidates_without_examples": sum(source_evidence(candidate) == "gloss_only" for candidate in candidates),
            "forms_with_any_candidate_without_examples": sum(row["candidates_without_examples"] > 0 for row in per_form),
            "candidates_with_usage_labels": sum(bool(candidate["usage_labels"]) for candidate in candidates),
            "source_relation_rows": sum(len(candidate["source_relations"]) for candidate in candidates),
            "candidates_with_related_not_merged_member": sum(
                any(relation["project_identity_action"] == "related_not_merged"
                    for relation in candidate["source_relations"])
                for candidate in candidates
            ),
        },
        "design_state": {
            "forms_with_multiple_observed_vmwe_categories": sum(
                len(item["observed_vmwe_categories"]) > 1 for item in inventory["types"]
            ),
            "admitted_project_senses": sum(len(item["senses"]) for item in inventory["types"]),
            "contextual_occurrences_in_inventory": sum(
                len(item.get("occurrences", [])) for item in inventory["types"]
            ),
        },
        "per_form": per_form,
    }


def load_inputs(protocol_path):
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    inventory_path = ROOT / protocol["scope"]["inventory_path"]
    if sha256(inventory_path) != protocol["scope"]["inventory_sha256"]:
        raise ValueError("Candidate inventory identity mismatch.")
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if inventory["inventory_id"] != protocol["scope"]["inventory_id"]:
        raise ValueError("Candidate inventory ID mismatch.")
    if inventory["inventory_schema_version"] != protocol["scope"]["inventory_schema_version"]:
        raise ValueError("Candidate inventory schema version mismatch.")
    for inventory_field, protocol_field in (
        ("source_inventory_id", "source_inventory_id"),
        ("source_version", "source_version"),
        ("artifact_sha256", "source_artifact_sha256"),
    ):
        if inventory["source_snapshot"][inventory_field] != protocol["scope"][protocol_field]:
            raise ValueError(f"Candidate source snapshot {protocol_field} mismatch.")
    forms = inventory["types"]
    candidates = sum(len(item["candidate_set"]["candidates"]) for item in forms)
    if len(forms) != protocol["scope"]["expected_forms"] or candidates != protocol["scope"]["expected_candidates"]:
        raise ValueError("Frozen review scope changed.")
    if polysemy_audit(inventory) != protocol["polysemy_pre_review_audit"]["quantitative"]:
        raise ValueError("Frozen polysemy audit mismatch.")
    usage_path = ROOT / protocol["usage_pilot"]["path"]
    if sha256(usage_path) != protocol["usage_pilot"]["sha256"]:
        raise ValueError("Usage-pilot manifest identity mismatch.")
    usage = json.loads(usage_path.read_text(encoding="utf-8"))
    if (
        usage["status"] != protocol["usage_pilot"]["status"]
        or usage["summary"]["occurrences"] != 54
        or usage["summary"]["initial_pairs"] != 51
        or usage["scope"]["excluded_split"] != "test"
    ):
        raise ValueError("Usage-pilot manifest scope mismatch.")
    return protocol, inventory


def require_review_ready(protocol):
    clusters = protocol["usage_pilot"]["cluster_artifact"]
    if clusters["status"] != "frozen" or not clusters["path"] or not clusters["sha256"]:
        raise ValueError("Usage-pilot judgments and clusters are not frozen; expert review cannot start.")
    # ponytail: keep review closed until a versioned cluster contract and validator exist.
    raise ValueError(
        "Usage-cluster artifact validation is not implemented; expert review cannot start."
    )


def make_template(protocol_path, protocol, inventory):
    return {
        "review_version": protocol["protocol_version"],
        "protocol_id": protocol["protocol_id"],
        "protocol_sha256": sha256(protocol_path),
        "inventory_sha256": protocol["scope"]["inventory_sha256"],
        "reviewer_code": None,
        "completed_date": None,
        "independence": {
            "other_review_seen_before_completion": None,
            "prohibited_signal_used": None,
            "unpinned_source_used": None,
        },
        "forms": [
            {
                "type_id": item["type_id"],
                "source_candidate_coverage": None,
                "missing_candidates": [],
                "candidate_reviews": [
                    {
                        "candidate_id": candidate["reserved_project_sense_id"],
                        "source_evidence": source_evidence(candidate),
                        "form_relation": None,
                        "construction_scope": None,
                        "action": None,
                        "rationale_code": None,
                    }
                    for candidate in item["candidate_set"]["candidates"]
                ],
                "project_sense_clusters": [],
            }
            for item in inventory["types"]
        ],
    }


def require_exact_fields(value, fields, label):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError(f"{label} fields do not match the protocol.")


def validate_review(review, template, protocol):
    require_exact_fields(review, template, "Review")
    for field in ("review_version", "protocol_id", "protocol_sha256", "inventory_sha256"):
        if review[field] != template[field]:
            raise ValueError(f"Review {field} mismatch.")
    if not isinstance(review["reviewer_code"], str) or not re.fullmatch(r"LX\d{2}", review["reviewer_code"]):
        raise ValueError("reviewer_code must be a pseudonymous LX00-style code.")
    try:
        date.fromisoformat(review["completed_date"])
    except (TypeError, ValueError):
        raise ValueError("completed_date must be YYYY-MM-DD.") from None
    if review["independence"] != {
        "other_review_seen_before_completion": False,
        "prohibited_signal_used": False,
        "unpinned_source_used": False,
    }:
        raise ValueError("Review independence declarations must all be false.")
    if not isinstance(review["forms"], list) or len(review["forms"]) != len(template["forms"]):
        raise ValueError("Review form coverage mismatch.")

    decisions = protocol["decision_fields"]
    missing_fields = protocol["missing_candidate_fields"]
    for actual, expected in zip(review["forms"], template["forms"]):
        require_exact_fields(actual, expected, "Form review")
        if actual["type_id"] != expected["type_id"]:
            raise ValueError("Review type order or identity mismatch.")
        if actual["source_candidate_coverage"] not in decisions["source_candidate_coverage"]:
            raise ValueError(f"Invalid source-coverage decision: {actual['type_id']}.")
        missing = actual["missing_candidates"]
        if not isinstance(missing, list) or bool(missing) != (
            actual["source_candidate_coverage"] == "omitted_pinned_source_sense"
        ):
            raise ValueError(f"Missing-candidate state mismatch: {actual['type_id']}.")
        missing_keys = set()
        for candidate in missing:
            require_exact_fields(candidate, missing_fields, "Missing candidate")
            if not all(isinstance(candidate[field], str) and candidate[field] for field in missing_fields):
                raise ValueError("Missing-candidate source identities must be non-empty strings.")
            if not re.fullmatch(r"[0-9a-f]{64}", candidate["source_record_sha256"]):
                raise ValueError("Missing-candidate source_record_sha256 is invalid.")
            if (
                candidate["source_inventory_id"] != protocol["scope"]["source_inventory_id"]
                or candidate["source_version"] != protocol["scope"]["source_version"]
                or candidate["source_artifact_sha256"] != protocol["scope"]["source_artifact_sha256"]
            ):
                raise ValueError("Missing candidate is outside the pinned source snapshot.")
            key = tuple(candidate[field] for field in missing_fields[:-1])
            if key in missing_keys:
                raise ValueError("Duplicate missing-candidate source identity.")
            missing_keys.add(key)

        actual_candidates = actual["candidate_reviews"]
        expected_candidates = expected["candidate_reviews"]
        if not isinstance(actual_candidates, list) or len(actual_candidates) != len(expected_candidates):
            raise ValueError(f"Candidate coverage mismatch: {actual['type_id']}.")
        candidate_ids = {item["candidate_id"] for item in expected_candidates}
        for candidate, expected_candidate in zip(actual_candidates, expected_candidates):
            require_exact_fields(candidate, expected_candidate, "Candidate review")
            if candidate["candidate_id"] != expected_candidate["candidate_id"]:
                raise ValueError("Candidate order or identity mismatch.")
            if candidate["source_evidence"] != expected_candidate["source_evidence"]:
                raise ValueError(f"Derived source evidence changed: {candidate['candidate_id']}.")
            if candidate["form_relation"] not in decisions["form_relation"]:
                raise ValueError(f"Invalid candidate relation: {candidate['candidate_id']}.")
            if candidate["construction_scope"] not in decisions["construction_scope"]:
                raise ValueError(f"Invalid construction scope: {candidate['candidate_id']}.")
            if candidate["action"] not in decisions["candidate_action"]:
                raise ValueError(f"Invalid candidate action: {candidate['candidate_id']}.")
            if candidate["rationale_code"] not in decisions["rationale_code"]:
                raise ValueError(f"Invalid rationale code: {candidate['candidate_id']}.")
            if candidate["action"] == "retain" and (
                candidate["form_relation"] == "unrelated"
                or candidate["construction_scope"] == "literal_or_free_combination"
            ):
                raise ValueError(f"Retain decision contradicts candidate scope: {candidate['candidate_id']}.")

        clusters = actual["project_sense_clusters"]
        if not isinstance(clusters, list) or any(not isinstance(cluster, list) or not cluster for cluster in clusters):
            raise ValueError(f"Invalid project-sense clusters: {actual['type_id']}.")
        if any(cluster != sorted(cluster) for cluster in clusters) or clusters != sorted(clusters, key=lambda row: row[0]):
            raise ValueError(f"Project-sense clusters are not in canonical ID order: {actual['type_id']}.")
        members = [candidate_id for cluster in clusters for candidate_id in cluster]
        retained = [candidate["candidate_id"] for candidate in actual_candidates if candidate["action"] == "retain"]
        if len(members) != len(set(members)) or set(members) != set(retained) or set(members) - candidate_ids:
            raise ValueError(f"Project-sense clusters are not a partition of retained candidates: {actual['type_id']}.")
    return review


def aggregate(review_a, review_b, review_hashes):
    candidate_total = relation_agreement = scope_agreement = action_agreement = rationale_agreement = 0
    source_coverage_agreement = cluster_agreement = 0
    missing_total = reject_total = merge_cluster_total = 0
    for form_a, form_b in zip(review_a["forms"], review_b["forms"]):
        source_coverage_agreement += form_a["source_candidate_coverage"] == form_b["source_candidate_coverage"]
        cluster_agreement += form_a["project_sense_clusters"] == form_b["project_sense_clusters"]
        missing_total += len(form_a["missing_candidates"]) + len(form_b["missing_candidates"])
        merge_cluster_total += sum(len(cluster) > 1 for cluster in form_a["project_sense_clusters"])
        merge_cluster_total += sum(len(cluster) > 1 for cluster in form_b["project_sense_clusters"])
        for candidate_a, candidate_b in zip(form_a["candidate_reviews"], form_b["candidate_reviews"]):
            candidate_total += 1
            relation_agreement += candidate_a["form_relation"] == candidate_b["form_relation"]
            scope_agreement += candidate_a["construction_scope"] == candidate_b["construction_scope"]
            action_agreement += candidate_a["action"] == candidate_b["action"]
            rationale_agreement += candidate_a["rationale_code"] == candidate_b["rationale_code"]
            reject_total += candidate_a["action"] == "reject"
            reject_total += candidate_b["action"] == "reject"
    form_total = len(review_a["forms"])
    return {
        "status": "pre_adjudication_reviews_complete_adjudication_pending",
        "review_file_sha256": review_hashes,
        "coverage": {"reviewers": 2, "forms_per_reviewer": form_total, "candidates_per_reviewer": candidate_total},
        "agreement": {
            "candidate_form_relation": {"agreed": relation_agreement, "disagreed": candidate_total - relation_agreement, "total": candidate_total, "rate": round(relation_agreement / candidate_total, 6)},
            "candidate_construction_scope": {"agreed": scope_agreement, "disagreed": candidate_total - scope_agreement, "total": candidate_total, "rate": round(scope_agreement / candidate_total, 6)},
            "candidate_action": {"agreed": action_agreement, "disagreed": candidate_total - action_agreement, "total": candidate_total, "rate": round(action_agreement / candidate_total, 6)},
            "candidate_rationale_codes": {"agreed": rationale_agreement, "disagreed": candidate_total - rationale_agreement, "total": candidate_total, "rate": round(rationale_agreement / candidate_total, 6)},
            "source_candidate_coverage": {"agreed": source_coverage_agreement, "disagreed": form_total - source_coverage_agreement, "total": form_total, "rate": round(source_coverage_agreement / form_total, 6)},
            "project_sense_clusters": {"agreed": cluster_agreement, "disagreed": form_total - cluster_agreement, "total": form_total, "rate": round(cluster_agreement / form_total, 6)},
        },
        "pre_adjudication_signals": {
            "missing_candidate_proposals": missing_total,
            "reject_decisions": reject_total,
            "multi_candidate_clusters": merge_cluster_total,
        },
        "inventory_revision_count": None,
        "claim_boundary": "Counts are workflow evidence only; actual inventory revisions require preserved adjudication records.",
    }


def self_check(protocol_path, protocol, inventory):
    template = make_template(protocol_path, protocol, inventory)
    reviews = []
    for reviewer_code in ("LX01", "LX02"):
        review = json.loads(json.dumps(template))
        review.update({"reviewer_code": reviewer_code, "completed_date": "2026-09-05"})
        review["independence"] = {
            "other_review_seen_before_completion": False,
            "prohibited_signal_used": False,
            "unpinned_source_used": False,
        }
        for form in review["forms"]:
            form["source_candidate_coverage"] = "complete_for_pinned_source"
            for candidate in form["candidate_reviews"]:
                candidate.update({
                    "form_relation": "equivalent",
                    "construction_scope": "in_scope_lexicalized_vmwe",
                    "action": "retain",
                    "rationale_code": "fits_form_and_scope",
                })
            form["project_sense_clusters"] = [[candidate["candidate_id"]] for candidate in form["candidate_reviews"]]
        reviews.append(validate_review(review, template, protocol))
    assert sum(len(item["candidate_reviews"]) for item in reviews[0]["forms"]) == 67
    assert reviews[0]["reviewer_code"] != reviews[1]["reviewer_code"]
    report = aggregate(reviews[0], reviews[1], ["0" * 64, "1" * 64])
    assert report["agreement"]["candidate_form_relation"]["agreed"] == 67
    assert report["agreement"]["candidate_construction_scope"]["agreed"] == 67
    assert report["agreement"]["candidate_action"]["agreed"] == 67
    assert report["agreement"]["project_sense_clusters"]["agreed"] == 9
    invalid = json.loads(json.dumps(reviews[0]))
    invalid["forms"][0]["project_sense_clusters"].pop()
    try:
        validate_review(invalid, template, protocol)
    except ValueError:
        pass
    else:
        raise AssertionError("Incomplete retained-candidate partition was accepted.")
    return {"self_check": "pass", "forms": 9, "candidates": 67}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reviews", type=Path, nargs="*")
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--template", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    try:
        protocol, inventory = load_inputs(args.protocol)
        template = make_template(args.protocol, protocol, inventory)
        if args.self_check:
            report = self_check(args.protocol, protocol, inventory)
        elif args.template:
            require_review_ready(protocol)
            report = template
        elif len(args.reviews) == 2:
            require_review_ready(protocol)
            reviews = [
                validate_review(json.loads(path.read_text(encoding="utf-8")), template, protocol)
                for path in args.reviews
            ]
            if reviews[0]["reviewer_code"] == reviews[1]["reviewer_code"]:
                raise ValueError("Two distinct reviewer codes are required.")
            report = aggregate(reviews[0], reviews[1], [sha256(path) for path in args.reviews])
        else:
            raise ValueError("Use --template, --self-check, or provide exactly two review files.")
    except (AssertionError, OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
