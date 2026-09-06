#!/usr/bin/env python3
"""Simulate document- and canonical-type-cluster precision from pilot rows."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import random

from bootstrap_evaluation import (
    checked_estimate,
    cluster_groups,
    percentile,
    ratio_estimator,
    validate_rows,
)


ROOT = Path(__file__).resolve().parents[1]


def distribution(grouped, counts, system, simulations, seed):
    generator = random.Random(seed)
    values = []
    for _ in range(simulations):
        sample = []
        for stratum, count in counts.items():
            clusters = grouped[stratum]
            for _ in range(count):
                sample.extend(generator.choice(clusters)[1])
        values.append(checked_estimate(ratio_estimator, sample, system))
    return values


def precision_record(values, target):
    if any(value is None for value in values):
        return {
            "state": "withheld_undefined_simulation",
            "defined_simulations": sum(value is not None for value in values),
            "lower": None,
            "upper": None,
            "half_width": None,
            "target_half_width": target,
            "passes": False,
        }
    lower = percentile(values, 0.025)
    upper = percentile(values, 0.975)
    half_width = (upper - lower) / 2
    return {
        "state": "simulated",
        "defined_simulations": len(values),
        "lower": round(lower, 6),
        "upper": round(upper, 6),
        "half_width": round(half_width, 6),
        "target_half_width": target,
        "passes": half_width <= target,
    }


def simulate(rows, systems, system, allocations, target, seed, simulations,
             minimum_documents_per_length=6):
    if (not isinstance(rows, list) or not rows
            or not isinstance(systems, list) or not systems
            or len(systems) != len(set(systems))
            or any(not isinstance(item, str) or not item for item in systems)):
        raise ValueError("rows and systems must be nonempty lists")
    if system not in systems:
        raise ValueError("planning system is not present")
    if (isinstance(target, bool) or not isinstance(target, (int, float))
            or not math.isfinite(target) or not 0 < target < 1
            or not isinstance(seed, str) or not seed
            or isinstance(simulations, bool) or not isinstance(simulations, int)
            or simulations < 1
            or isinstance(minimum_documents_per_length, bool)
            or not isinstance(minimum_documents_per_length, int)
            or minimum_documents_per_length < 2):
        raise ValueError("target and simulations are invalid")
    if not isinstance(allocations, list) or not allocations:
        raise ValueError("allocations must be a nonempty list")
    validate_rows(rows, systems, {}, True)
    documents = cluster_groups(rows, "document_id", "length_stratum")
    forms = cluster_groups(rows, "canonical_type_id")
    form_clusters = forms.get("all", [])
    if (not documents or any(len(clusters) < 2 for clusters in documents.values())
            or len(form_clusters) < 2):
        return {
            "state": "blocked_insufficient_pilot_clusters",
            "document_clusters_by_length": {
                stratum: len(clusters) for stratum, clusters in documents.items()
            },
            "canonical_type_clusters": len(form_clusters),
            "allocations": [],
            "selected_allocation_id": None,
        }

    results = []
    seen_allocations = set()
    for allocation in allocations:
        required = {
            "id", "documents_by_length", "canonical_type_count",
            "uses_target_conditioned_selection",
        }
        if (not isinstance(allocation, dict) or set(allocation) != required
                or not isinstance(allocation["id"], str) or not allocation["id"]
                or allocation["id"] in seen_allocations
                or not isinstance(allocation["uses_target_conditioned_selection"], bool)):
            raise ValueError("Each allocation requires exact fields and a unique id")
        seen_allocations.add(allocation["id"])
        counts = allocation["documents_by_length"]
        if not isinstance(counts, dict) or set(counts) != set(documents) or any(
            isinstance(count, bool) or not isinstance(count, int) or count < 2
            for count in counts.values()
        ):
            raise ValueError(f"Invalid document allocation: {allocation['id']}")
        if any(count < minimum_documents_per_length for count in counts.values()):
            raise ValueError(f"Allocation leaves an empty frozen split: {allocation['id']}")
        form_count = allocation["canonical_type_count"]
        if isinstance(form_count, bool) or not isinstance(form_count, int) or form_count < 2:
            raise ValueError(f"Invalid canonical-type allocation: {allocation['id']}")
        primary = precision_record(
            distribution(
                documents,
                counts,
                system,
                simulations,
                f"{seed}:{allocation['id']}:document",
            ),
            target,
        )
        sensitivity = precision_record(
            distribution(
                forms,
                {"all": form_count},
                system,
                simulations,
                f"{seed}:{allocation['id']}:canonical_type",
            ),
            target,
        )
        selection_eligible = not allocation["uses_target_conditioned_selection"]
        results.append({
            "id": allocation["id"],
            "documents_by_length": counts,
            "document_count": sum(counts.values()),
            "canonical_type_count": form_count,
            "uses_target_conditioned_selection": allocation["uses_target_conditioned_selection"],
            "selection_eligible": selection_eligible,
            "primary_document": primary,
            "canonical_type_sensitivity": sensitivity,
            "passes": primary["passes"] and sensitivity["passes"],
        })

    eligible = [
        result for result in results if result["selection_eligible"] and result["passes"]
    ]
    selected = min(
        eligible,
        key=lambda result: (result["document_count"], result["canonical_type_count"], result["id"]),
        default=None,
    )
    return {
        "state": "candidate_selected" if selected else "claim_withheld_no_feasible_allocation",
        "document_clusters_by_length": {
            stratum: len(clusters) for stratum, clusters in documents.items()
        },
        "canonical_type_clusters": len(form_clusters),
        "allocations": results,
        "selected_allocation_id": selected["id"] if selected else None,
    }


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--plan", type=Path, default=ROOT / "resources/precision_plan.json")
    args = parser.parse_args()
    try:
        plan = load(args.plan)
        if plan["status"] != "ready_to_simulate":
            raise ValueError("precision plan remains inactive; complete every observed-input gate first")
        if plan["planning_pilot_design_resolution"]["state"] != "resolved":
            raise ValueError("planning-pilot design remains unresolved")
        if any(value is None for value in plan["required_observed_inputs"].values()):
            raise ValueError("precision plan has unresolved observed-input gates")
        for dependency in plan["dependencies"].values():
            path = ROOT / dependency["path"]
            if hashlib.sha256(path.read_bytes()).hexdigest() != dependency["sha256"]:
                raise ValueError(f"dependency hash mismatch: {dependency['path']}")
        input_bytes = args.input.read_bytes()
        if hashlib.sha256(input_bytes).hexdigest() != plan["required_observed_inputs"]["simulation_input_sha256"]:
            raise ValueError("simulation input hash mismatch")
        data = json.loads(input_bytes)
        settings = plan["simulation"]
        if data.get("simulation_contract_version") != settings["contract_version"]:
            raise ValueError("simulation_contract_version mismatch")
        if data.get("seed") != settings["seed"] or data.get("simulations") != settings["simulations"]:
            raise ValueError("simulation settings do not match the frozen plan")
        if data.get("target_half_width") not in plan["precision_targets"].values():
            raise ValueError("target_half_width is not frozen")
        population_counts = plan["required_observed_inputs"]["source_population_counts_by_length"]
        resource_ceiling = plan["required_observed_inputs"]["feasible_resource_ceiling"]
        length_strata = set(plan["candidate_allocation_contract"]["length_strata"])
        if (not isinstance(population_counts, dict) or set(population_counts) != length_strata
                or any(isinstance(count, bool) or not isinstance(count, int) or count < 1
                       for count in population_counts.values())):
            raise ValueError("source population counts are invalid")
        if (isinstance(resource_ceiling, bool) or not isinstance(resource_ceiling, int)
                or resource_ceiling < 1):
            raise ValueError("feasible resource ceiling is invalid")
        for allocation in data["allocations"]:
            if set(allocation["documents_by_length"]) != length_strata:
                raise ValueError(f"Allocation length strata mismatch: {allocation['id']}")
            if sum(allocation["documents_by_length"].values()) > resource_ceiling:
                raise ValueError(f"Allocation exceeds resource ceiling: {allocation['id']}")
            if any(
                count > population_counts[stratum]
                for stratum, count in allocation["documents_by_length"].items()
            ):
                raise ValueError(f"Allocation exceeds source population: {allocation['id']}")
        result = simulate(
            data["rows"], data["systems"], data["planning_system"],
            data["allocations"], data["target_half_width"],
            data["seed"], data["simulations"],
            plan["candidate_allocation_contract"]["minimum_documents_per_length"],
        )
        result.update({
            "simulation_contract_version": settings["contract_version"],
            "metric_id": data["metric_id"],
            "planning_system": data["planning_system"],
            "seed": data["seed"],
            "simulations": data["simulations"],
        })
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
