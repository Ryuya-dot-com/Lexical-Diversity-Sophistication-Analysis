#!/usr/bin/env python3
"""Audit project sense-inventory coverage over the full STREUSLE target set."""

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from check_streusle_v5 import inspect_checkout


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "benchmarks/streusle_v5_vpc_vid.json"
INVENTORY = ROOT / "resources/hybrid_sense_inventory_v1.json"
PILOT = ROOT / "resources/inventory_population_log.json"
EXACT_AUDIT = ROOT / "resources/streusle_v5_oewn_2025_coverage_audit.json"
VID_AUDIT = ROOT / "resources/streusle_v5_kaikki_vid_audit_2026_09_03.json"


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ratio(numerator, denominator):
    return round(numerator / denominator, 6) if denominator else None


def target_rows(datasets, categories):
    rows = []
    for split in ("train", "dev", "test"):
        for sentence in datasets[split]:
            for occurrence in sentence["smwes"].values():
                if occurrence["lexcat"] not in categories:
                    continue
                tokens = occurrence["toknums"]
                rows.append({
                    "split": split,
                    "lemma": occurrence["lexlemma"].casefold(),
                    "category": occurrence["lexcat"],
                    "continuity": "discontinuous" if (
                        max(tokens) - min(tokens) + 1 > len(tokens)
                    ) else "contiguous",
                })
    return rows


def coverage_counts(items, unit):
    total = len(items)
    admitted = sum(item["admitted_senses"] > 0 for item in items)
    candidate = sum(
        item["admitted_senses"] == 0 and item["candidate_senses"] > 0
        for item in items
    )
    return {
        "denominator": total,
        "admitted_inventory_available": admitted,
        "candidate_seed_only": candidate,
        "inventory_status_unresolved": sum(
            item["inventory_status"] == "unresolved" for item in items
        ),
        "no_project_inventory_entry": total - admitted - candidate,
        "operational_inventory_coverage": ratio(admitted, total),
        "candidate_seed_availability": ratio(candidate, total),
        **({
            "contextual_adequacy_assessed": 0,
            "observed_out_of_inventory": 0,
            "contextual_status_not_assessed": total,
        } if unit == "occurrence" else {}),
    }


def distribution(items):
    counts = Counter(item["candidate_senses"] for item in items)
    return {str(key): counts[key] for key in sorted(counts)}


def summarize(datasets, categories, inventory, pilot):
    candidate_counts = {
        item["canonical_lemma"].casefold():
        len(item["candidate_set"]["candidates"])
        for item in inventory["types"]
    }
    admitted_counts = {
        item["canonical_lemma"].casefold():
        sum(sense["lifecycle_status"] == "active" for sense in item["senses"])
        for item in inventory["types"]
    }
    inventory_statuses = {
        item["canonical_lemma"].casefold(): item["inventory_status"]
        for item in inventory["types"]
    }
    rows = target_rows(datasets, categories)
    for row in rows:
        row["candidate_senses"] = candidate_counts.get(row["lemma"], 0)
        row["admitted_senses"] = admitted_counts.get(row["lemma"], 0)
        row["inventory_status"] = inventory_statuses.get(row["lemma"], "not_present")

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["lemma"]].append(row)
    type_rows = [{
        "lemma": lemma,
        "categories": sorted({item["category"] for item in items}),
        "candidate_senses": candidate_counts.get(lemma, 0),
        "admitted_senses": admitted_counts.get(lemma, 0),
        "inventory_status": inventory_statuses.get(lemma, "not_present"),
    } for lemma, items in sorted(grouped.items())]
    missing_inventory_forms = sorted(set(candidate_counts) - set(grouped))
    if missing_inventory_forms:
        raise ValueError(f"Inventory forms absent from target population: {missing_inventory_forms}.")

    by_category = {}
    for category in sorted(categories):
        category_occurrences = [item for item in rows if item["category"] == category]
        category_types = [item for item in type_rows if category in item["categories"]]
        by_category[category] = {
            "occurrences": coverage_counts(category_occurrences, "occurrence"),
            "types": coverage_counts(category_types, "type"),
        }

    pilot_rows = []
    for item in pilot["pilot_batch"]:
        lemma = item["canonical_lemma"].casefold()
        pilot_rows.append({
            "lemma": lemma,
            "occurrences": item["train_occurrences"],
            "discontinuous_occurrences": item["train_discontinuous_occurrences"],
            "mapping_route": item["mapping_route"],
            "candidate_senses": candidate_counts.get(lemma, 0),
            "admitted_senses": admitted_counts.get(lemma, 0),
            "inventory_status": inventory_statuses.get(lemma, "not_present"),
        })

    pilot_candidate_occurrences = sum(
        item["occurrences"] for item in pilot_rows
        if item["candidate_senses"] and not item["admitted_senses"]
    )
    pilot_admitted_occurrences = sum(
        item["occurrences"] for item in pilot_rows if item["admitted_senses"]
    )
    pilot_route_occurrences = Counter()
    for item in pilot_rows:
        pilot_route_occurrences[item["mapping_route"]] += item["occurrences"]

    return {
        "full_target_population": {
            "occurrences": coverage_counts(rows, "occurrence"),
            "types": coverage_counts(type_rows, "type"),
            "by_category": by_category,
            "by_split": {
                split: coverage_counts(
                    [item for item in rows if item["split"] == split], "occurrence"
                ) for split in ("train", "dev", "test")
            },
            "by_continuity": {
                continuity: coverage_counts(
                    [item for item in rows if item["continuity"] == continuity],
                    "occurrence",
                ) for continuity in ("contiguous", "discontinuous")
            },
            "candidate_count_distribution": {
                "type_denominator_all_target_types": distribution(type_rows),
                "occurrence_denominator_all_target_occurrences": distribution(rows),
                "types_with_multiple_candidates": sum(
                    item["candidate_senses"] >= 2 for item in type_rows
                ),
                "occurrences_with_multiple_candidates": sum(
                    item["candidate_senses"] >= 2 for item in rows
                ),
                "zero_candidate_items_included": True,
                "selected_only_denominator_permitted": False,
            },
            "category_type_count_warning": "A type observed under multiple categories enters each category denominator but only once in the overall type denominator.",
        },
        "ir132_vid_pilot": {
            "category": "V.VID",
            "types": {
                "denominator": len(pilot_rows),
                "admitted_inventory_available": sum(
                    item["admitted_senses"] > 0 for item in pilot_rows
                ),
                "candidate_seed_only": sum(
                    item["candidate_senses"] > 0 and not item["admitted_senses"]
                    for item in pilot_rows
                ),
                "inventory_status_unresolved": sum(
                    item["inventory_status"] == "unresolved" for item in pilot_rows
                ),
                "not_in_project_inventory": sum(
                    not item["candidate_senses"] and not item["admitted_senses"]
                    for item in pilot_rows
                ),
            },
            "occurrences": {
                "denominator": sum(item["occurrences"] for item in pilot_rows),
                "discontinuous": sum(
                    item["discontinuous_occurrences"] for item in pilot_rows
                ),
                "admitted_inventory_available": pilot_admitted_occurrences,
                "candidate_seed_only": pilot_candidate_occurrences,
                "inventory_status_unresolved": sum(
                    item["occurrences"] for item in pilot_rows
                    if item["inventory_status"] == "unresolved"
                ),
                "not_in_project_inventory": sum(
                    item["occurrences"] for item in pilot_rows
                ) - pilot_admitted_occurrences - pilot_candidate_occurrences,
                "contextual_adequacy_assessed": 0,
                "observed_out_of_inventory": 0,
                "contextual_status_not_assessed": sum(
                    item["occurrences"] for item in pilot_rows
                ),
            },
            "mapping_route_type_counts": pilot["summary"]["mapping_route_counts"],
            "mapping_route_occurrence_counts": dict(sorted(pilot_route_occurrences.items())),
            "candidate_count_distribution_all_14_types": distribution(pilot_rows),
            "selected_only_denominator_permitted": False,
        },
    }


def build_audit(checkout):
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    pilot = json.loads(PILOT.read_text(encoding="utf-8"))
    exact = json.loads(EXACT_AUDIT.read_text(encoding="utf-8"))
    vid = json.loads(VID_AUDIT.read_text(encoding="utf-8"))
    _, datasets = inspect_checkout(checkout, profile)
    summary = summarize(
        datasets, set(profile["projection"]["category_mapping"]), inventory, pilot
    )
    full = summary["full_target_population"]
    return {
        "audit_version": "2.0.0",
        "audit_id": "ldfreq-hybrid-inventory-coverage-v2",
        "generated_on": "2026-09-05",
        "status": "complete_current_project_inventory_has_zero_admitted_senses",
        "task": "IR-135",
        "purpose": "Measure operational project-inventory coverage over every STREUSLE VPC/VID target and the fixed IR-132 VID pilot without selecting dictionary-matched items.",
        "dependencies": {
            name: {"path": str(path.relative_to(ROOT)), "sha256": file_digest(path)}
            for name, path in {
                "streusle_profile": PROFILE,
                "candidate_inventory": INVENTORY,
                "vid_pilot": PILOT,
                "prior_exact_oewn_audit": EXACT_AUDIT,
                "prior_vid_route_audit": VID_AUDIT,
                "generator": Path(__file__),
            }.items()
        },
        "source_identity": {
            "streusle_tag": profile["source"]["tag"],
            "streusle_commit": profile["source"]["commit"],
            "streusle_artifacts": profile["artifacts"],
            "candidate_inventory_version": inventory["inventory_schema_version"],
            "candidate_inventory_anchor_sha256": inventory["id_registry"]["stability_anchor_sha256"],
        },
        "denominator_contract": {
            "full_occurrence_population": "All 624 pinned STREUSLE train/dev/test V.VPC.full, V.VPC.semi, and V.VID annotations.",
            "full_type_population": "All 389 casefolded canonical target types; a type may enter more than one category stratum.",
            "pilot_population": "All 14 prospectively fixed IR-132 STREUSLE-train VID types and all 52 of their train occurrences.",
            "operational_coverage": "A project sense must be formally admitted and the contextual adequacy task must be completed; source lookup or an unreviewed candidate set is not coverage.",
            "selected_only_denominator_permitted": False,
        },
        "summary": summary,
        "source_lookup_context_not_operational_coverage": {
            "exact_oewn": {
                "types": exact["summary"]["type_counts"],
                "occurrences": exact["summary"]["occurrence_counts"],
            },
            "vid_any_unreviewed_dictionary_route": vid["summary"]["combined_lookup_routes"],
        },
        "stop_decision": {
            "all_contextual_sense_claims": "held",
            "vid_sense_claim": "held",
            "discontinuous_sense_claim": "held",
            "trigger": {
                "admitted_inventory_occurrences": full["occurrences"]["admitted_inventory_available"],
                "admitted_vid_occurrences": full["by_category"]["V.VID"]["occurrences"]["admitted_inventory_available"],
                "admitted_discontinuous_occurrences": full["by_continuity"]["discontinuous"]["admitted_inventory_available"],
                "contextual_adequacy_assessed": full["occurrences"]["contextual_adequacy_assessed"],
            },
            "rule": "Zero admitted senses or zero contextual adequacy reviews is sufficient to hold the claim; nonzero coverage would still require the frozen precision and independent-review gates.",
        },
        "release_boundary": {
            "source_sentence_or_token_text_bundled": False,
            "occurrence_rows_bundled": False,
            "person_level_data_bundled": False,
            "human_annotation_added": False,
            "raw_dictionary_record_added": False,
            "runtime_integration": "none",
            "interpretation": "Aggregate candidate availability and zero formal coverage expose current selection bias; they do not measure contextual sense accuracy, OOI prevalence, or semantic adequacy.",
        },
    }


def self_check():
    occurrence = lambda category, lemma, tokens: {
        "lexcat": category, "lexlemma": lemma, "toknums": tokens,
    }
    datasets = {
        "train": [{"smwes": {
            "1": occurrence("V.VID", "alpha beta", [1, 3]),
            "2": occurrence("V.VPC.full", "gamma out", [4, 5]),
        }}],
        "dev": [],
        "test": [],
    }
    inventory = {"types": [{
        "canonical_lemma": "alpha beta", "inventory_status": "unresolved", "senses": [],
        "candidate_set": {"candidates": [{}, {}]},
    }]}
    pilot = {"summary": {"mapping_route_counts": {"exact_oewn": 1}}, "pilot_batch": [{
        "canonical_lemma": "alpha beta", "train_occurrences": 1,
        "train_discontinuous_occurrences": 1, "mapping_route": "exact_oewn",
    }]}
    result = summarize(datasets, {"V.VID", "V.VPC.full"}, inventory, pilot)
    full = result["full_target_population"]
    assert full["occurrences"]["denominator"] == 2
    assert full["occurrences"]["candidate_seed_only"] == 1
    assert full["types"]["no_project_inventory_entry"] == 1
    assert full["by_continuity"]["discontinuous"]["candidate_seed_only"] == 1
    assert full["candidate_count_distribution"]["type_denominator_all_target_types"] == {"0": 1, "2": 1}
    assert result["ir132_vid_pilot"]["occurrences"]["candidate_seed_only"] == 1
    return {"self_check": "pass"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, nargs="?")
    parser.add_argument("--check", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_check:
            result = self_check()
        else:
            if args.checkout is None:
                raise ValueError("A STREUSLE 5.0 checkout path is required.")
            result = build_audit(args.checkout)
            if args.check and result != json.loads(args.check.read_text(encoding="utf-8")):
                raise ValueError(f"Audit differs from {args.check}.")
    except (AssertionError, OSError, json.JSONDecodeError, KeyError, TypeError,
            ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
