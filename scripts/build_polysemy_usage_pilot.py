#!/usr/bin/env python3
"""Build the exposed STREUSLE usage-pair scaffold for IR-136."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "resources/hybrid_sense_inventory_v1.json"
COVERAGE = ROOT / "resources/hybrid_inventory_coverage_v2.json"
OUTPUT = ROOT / "resources/polysemy_usage_pilot.json"
SEED = "ldfreq-polysemy-usage-pilot-v1"
TARGET_CATEGORIES = {"V.VPC.full", "V.VPC.semi", "V.VID"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_hash(value):
    payload = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_inputs():
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    expected_inventory = coverage["dependencies"]["candidate_inventory"]["sha256"]
    if sha256(INVENTORY) != expected_inventory:
        raise ValueError("Candidate inventory identity mismatch.")

    datasets = {}
    for split in ("train", "dev"):
        path = ROOT / "research_data/streusle_v5" / split / f"streusle.ud_{split}.json"
        expected = coverage["source_identity"]["streusle_artifacts"][split]["sha256"]
        if sha256(path) != expected:
            raise ValueError(f"STREUSLE {split} identity mismatch.")
        datasets[split] = json.loads(path.read_text(encoding="utf-8"))
    return inventory, coverage, datasets


def extract_occurrences(inventory, datasets):
    forms = {
        item["canonical_lemma"].casefold(): {
            "type_id": item["type_id"],
            "canonical_lemma": item["canonical_lemma"],
        }
        for item in inventory["types"]
    }
    occurrences = []
    for split in ("train", "dev"):
        for sentence in datasets[split]:
            for mwe_id, mwe in sentence["smwes"].items():
                lemma = mwe["lexlemma"].casefold()
                if lemma not in forms or mwe["lexcat"] not in TARGET_CATEGORIES:
                    continue
                token_numbers = mwe["toknums"]
                occurrence_id = f"streusle:{split}:{sentence['sent_id']}:smwe:{mwe_id}"
                occurrences.append({
                    "occurrence_id": occurrence_id,
                    "type_id": forms[lemma]["type_id"],
                    "canonical_lemma": forms[lemma]["canonical_lemma"],
                    "split": split,
                    "sentence_id": sentence["sent_id"],
                    "mwe_id": str(mwe_id),
                    "category": mwe["lexcat"],
                    "token_numbers": token_numbers,
                    "discontinuous": max(token_numbers) - min(token_numbers) + 1 > len(token_numbers),
                    "context_sha256": hashlib.sha256(sentence["text"].encode("utf-8")).hexdigest(),
                })
    return sorted(occurrences, key=lambda row: (row["type_id"], row["occurrence_id"]))


def initial_pairs(occurrences):
    by_type = {}
    for occurrence in occurrences:
        by_type.setdefault(occurrence["type_id"], []).append(occurrence)

    pairs = []
    for type_id, rows in sorted(by_type.items()):
        order = sorted(rows, key=lambda row: stable_hash([SEED, row["occurrence_id"]]))
        if len(order) < 2:
            continue
        edges = set()
        limit = 1 if len(order) == 2 else len(order)
        for index in range(limit):
            left = order[index]["occurrence_id"]
            right = order[(index + 1) % len(order)]["occurrence_id"]
            edges.add(tuple(sorted((left, right))))
        for left, right in sorted(edges):
            pairs.append({
                "pair_id": "usp-" + stable_hash([SEED, left, right])[:16],
                "type_id": type_id,
                "left_occurrence_id": left,
                "right_occurrence_id": right,
                "round": 1,
            })
    return pairs


def build_manifest(inventory, coverage, occurrences, pairs):
    occurrence_counts = Counter(row["canonical_lemma"] for row in occurrences)
    pair_counts = Counter(
        next(row["canonical_lemma"] for row in occurrences if row["type_id"] == pair["type_id"])
        for pair in pairs
    )
    per_form = [
        {
            "type_id": item["type_id"],
            "canonical_lemma": item["canonical_lemma"],
            "occurrences": occurrence_counts[item["canonical_lemma"]],
            "initial_pairs": pair_counts[item["canonical_lemma"]],
            "inference_state": "eligible_for_usage_graph" if occurrence_counts[item["canonical_lemma"]] >= 2 else "insufficient_contexts",
        }
        for item in inventory["types"]
    ]
    return {
        "schema_version": "1.0.0",
        "pilot_id": "ldfreq-polysemy-usage-pilot-v1",
        "frozen_on": "2026-09-05",
        "status": "manifest_built_no_semantic_judgments",
        "task": "IR-136",
        "purpose": "Test project sense granularity from contextual usage before expert review of dictionary-to-project mappings.",
        "dependencies": {
            "candidate_inventory": {"path": str(INVENTORY.relative_to(ROOT)), "sha256": sha256(INVENTORY)},
            "coverage_audit": {"path": str(COVERAGE.relative_to(ROOT)), "sha256": sha256(COVERAGE)},
            "streusle": {
                split: coverage["source_identity"]["streusle_artifacts"][split]
                for split in ("train", "dev")
            },
        },
        "scope": {
            "forms": len(per_form),
            "source_splits": ["train", "dev"],
            "excluded_split": "test",
            "selection": "All in-scope STREUSLE train/dev occurrences whose canonical form is in the frozen nine-form candidate inventory.",
            "source_text_bundled": False,
            "join_rule": "Resolve sentence_id against the hash-verified local STREUSLE artifact when presenting context.",
        },
        "judgment_contract": {
            "unit": "Two occurrences of the same canonical form, presented with context and without dictionary glosses or candidate IDs.",
            "scale": {
                "1": "unrelated meanings",
                "2": "distantly related meanings",
                "3": "closely related meanings",
                "4": "same meaning",
                "cannot_decide": "context is insufficient or the comparison cannot be made reliably",
            },
            "independence": "Obtain two independent ratings per released pair before discussion or cluster review.",
            "round_1": "Use the deterministic connected scaffold below; never compare occurrences from different forms.",
            "later_rounds": "Add only edges needed to examine disagreement, weakly connected regions, or provisional cluster boundaries; freeze each batch before ratings.",
            "edge_ceiling": "At most min(n*(n-1)/2, 3*n) unique pairs per form across all rounds; reaching the ceiling without stability yields unresolved granularity.",
            "dictionary_blinding": "Usage-pair raters do not see OEWN IDs, glosses, source order, candidate counts, model scores, or proposed project clusters.",
        },
        "interpretation": {
            "permitted": [
                "propose usage clusters for later lexicographic review",
                "identify unstable or underdetermined distinctions",
                "compare cluster proposals with the frozen source candidate inventory",
            ],
            "prohibited": [
                "treat source sense count as observed polysemy",
                "treat a graph cluster as an automatically admitted project sense",
                "estimate English-wide sense frequencies from this purposive exposed slice",
                "use this pilot as sealed-test evidence",
            ],
            "single_occurrence_rule": "A form with fewer than two occurrences remains insufficient_contexts; dictionary evidence may be reviewed but contextual separability is not established.",
        },
        "summary": {
            "occurrences": len(occurrences),
            "by_split": dict(sorted(Counter(row["split"] for row in occurrences).items())),
            "initial_pairs": len(pairs),
            "forms_with_at_least_two_occurrences": sum(row["occurrences"] >= 2 for row in per_form),
            "forms_with_insufficient_contexts": sum(row["occurrences"] < 2 for row in per_form),
            "per_form": per_form,
        },
        "occurrences": occurrences,
        "initial_pairs": pairs,
        "current_boundary": {
            "semantic_judgments": 0,
            "usage_clusters": 0,
            "expert_inventory_reviews": 0,
            "admitted_project_senses": 0,
        },
    }


def validate_manifest(manifest):
    occurrences = manifest["occurrences"]
    pairs = manifest["initial_pairs"]
    occurrence_by_id = {row["occurrence_id"]: row for row in occurrences}
    if len(occurrence_by_id) != len(occurrences):
        raise ValueError("Duplicate usage-pilot occurrence ID.")
    if len(occurrences) != 54 or Counter(row["split"] for row in occurrences) != {"train": 52, "dev": 2}:
        raise ValueError("Frozen usage-pilot occurrence scope changed.")
    if len(pairs) != 51 or len({row["pair_id"] for row in pairs}) != len(pairs):
        raise ValueError("Frozen usage-pilot pair scope changed.")

    edges_by_type = {}
    for pair in pairs:
        left = occurrence_by_id.get(pair["left_occurrence_id"])
        right = occurrence_by_id.get(pair["right_occurrence_id"])
        if not left or not right or left["type_id"] != right["type_id"] or left["type_id"] != pair["type_id"]:
            raise ValueError("Usage pair crosses forms or references an unknown occurrence.")
        edge = tuple(sorted((left["occurrence_id"], right["occurrence_id"])))
        type_edges = edges_by_type.setdefault(pair["type_id"], set())
        if edge in type_edges:
            raise ValueError("Duplicate usage-pilot edge.")
        type_edges.add(edge)

    for summary in manifest["summary"]["per_form"]:
        nodes = {row["occurrence_id"] for row in occurrences if row["type_id"] == summary["type_id"]}
        if len(nodes) < 2:
            continue
        reached = {next(iter(nodes))}
        while True:
            expanded = reached | {
                endpoint
                for edge in edges_by_type[summary["type_id"]]
                if reached.intersection(edge)
                for endpoint in edge
            }
            if expanded == reached:
                break
            reached = expanded
        if reached != nodes:
            raise ValueError(f"Initial usage graph is disconnected: {summary['type_id']}.")
    if any("text" in row for row in occurrences) or manifest["current_boundary"] != {
        "semantic_judgments": 0,
        "usage_clusters": 0,
        "expert_inventory_reviews": 0,
        "admitted_project_senses": 0,
    }:
        raise ValueError("Usage manifest contains source text or premature semantic evidence.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail unless the committed manifest is current")
    args = parser.parse_args()
    inventory, coverage, datasets = load_inputs()
    occurrences = extract_occurrences(inventory, datasets)
    manifest = build_manifest(inventory, coverage, occurrences, initial_pairs(occurrences))
    validate_manifest(manifest)
    rendered = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit("Polysemy usage-pilot manifest is stale.")
        print("Polysemy usage-pilot manifest: PASS")
    else:
        OUTPUT.write_text(rendered, encoding="utf-8")
        print(f"Wrote {OUTPUT.relative_to(ROOT)}: {len(manifest['occurrences'])} occurrences, {len(manifest['initial_pairs'])} initial pairs")


if __name__ == "__main__":
    main()
