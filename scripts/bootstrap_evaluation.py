#!/usr/bin/env python3
"""Cluster-bootstrap additive benchmark metric contributions."""

import argparse
from itertools import combinations
import json
import math
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parents[1]


def ratio_estimator(rows, system):
    numerator = sum(row["weight"] * row["systems"][system]["numerator"] for row in rows)
    denominator = sum(row["weight"] * row["systems"][system]["denominator"] for row in rows)
    return numerator / denominator if denominator else None


def checked_estimate(estimator, rows, system):
    value = estimator(rows, system)
    if value is not None and (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
    ):
        raise ValueError(f"Estimator returned an invalid value for {system}")
    return value


def percentile(values, probability):
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = int(position)
    fraction = position - lower
    if not fraction:
        return ordered[lower]
    return ordered[lower] + fraction * (ordered[lower + 1] - ordered[lower])


def interval(values, point_estimate, confidence, insufficient_clusters=False,
             requested_resamples=None):
    record = {
        "point_estimate": None if point_estimate is None else round(point_estimate, 6),
        "confidence_level": confidence,
        "method": "percentile_type_7_linear_interpolation",
        "defined_resamples": sum(value is not None for value in values),
        "requested_resamples": requested_resamples if requested_resamples is not None else len(values),
        "lower": None,
        "upper": None,
    }
    if point_estimate is None:
        record["state"] = "point_estimate_undefined"
    elif insufficient_clusters:
        record["state"] = "point_estimate_only_fewer_than_two_clusters_in_resampling_stratum"
    elif any(value is None for value in values):
        record["state"] = "interval_withheld_undefined_resample"
    else:
        alpha = (1 - confidence) / 2
        record.update({
            "state": "descriptive_interval_pending_IR-127_precision_gate",
            "lower": round(percentile(values, alpha), 6),
            "upper": round(percentile(values, 1 - alpha), 6),
        })
    return record


def cluster_groups(rows, cluster_key, sampling_stratum_key=None):
    groups = {}
    cluster_strata = {}
    for row in rows:
        cluster = row[cluster_key]
        stratum = row[sampling_stratum_key] if sampling_stratum_key else "all"
        if cluster in cluster_strata and cluster_strata[cluster] != stratum:
            raise ValueError(f"{cluster_key} {cluster} crosses resampling strata")
        cluster_strata[cluster] = stratum
        groups.setdefault(stratum, {}).setdefault(cluster, []).append(row)
    return {
        stratum: [(cluster, clusters[cluster]) for cluster in sorted(clusters)]
        for stratum, clusters in sorted(groups.items())
    }


def bootstrap_scope(rows, systems, estimator, cluster_key, sampling_stratum_key,
                    seed, resamples, confidence):
    grouped = cluster_groups(rows, cluster_key, sampling_stratum_key)
    cluster_counts = {stratum: len(clusters) for stratum, clusters in grouped.items()}
    cluster_count = sum(cluster_counts.values())
    points = {system: checked_estimate(estimator, rows, system) for system in systems}
    pairs = list(combinations(systems, 2))
    pair_names = {(left, right): f"{right}_minus_{left}" for left, right in pairs}
    insufficient = cluster_count < 2 or any(len(clusters) < 2 for clusters in grouped.values())
    draws = {system: [] for system in systems}
    paired_draws = {pair_names[pair]: [] for pair in pairs}

    if not insufficient:
        generator = random.Random(seed)
        for _ in range(resamples):
            sample = []
            for clusters in grouped.values():
                for _ in clusters:
                    sample.extend(generator.choice(clusters)[1])
            estimates = {
                system: checked_estimate(estimator, sample, system)
                for system in systems
            }
            for system, estimate in estimates.items():
                draws[system].append(estimate)
            for left, right in pairs:
                left_value, right_value = estimates[left], estimates[right]
                paired_draws[pair_names[(left, right)]].append(
                    right_value - left_value
                    if left_value is not None and right_value is not None
                    else None
                )

    return {
        "cluster_unit": cluster_key,
        "resampling_stratum": sampling_stratum_key,
        "cluster_count": cluster_count,
        "cluster_counts_by_resampling_stratum": cluster_counts,
        "intervals": {
            system: interval(
                draws[system], points[system], confidence, insufficient, resamples
            )
            for system in systems
        },
        "paired_differences": {
            pair_names[(left, right)]: interval(
                paired_draws[pair_names[(left, right)]],
                points[right] - points[left]
                if points[left] is not None and points[right] is not None
                else None,
                confidence,
                insufficient,
                resamples,
            )
            for left, right in pairs
        },
    }


def validate_rows(rows, systems, stratum_levels, additive):
    seen = set()
    for row in rows:
        required = {"record_id", "document_id", "length_stratum", "canonical_type_id",
                    "weight", "strata", "systems"}
        if not isinstance(row, dict) or not required <= set(row) or row["record_id"] in seen:
            raise ValueError("Each row requires cluster fields and a unique record_id")
        seen.add(row["record_id"])
        if any(not isinstance(row[field], str) or not row[field]
               for field in ("record_id", "document_id", "length_stratum", "canonical_type_id")):
            raise ValueError(f"Invalid cluster identity: {row['record_id']}")
        if (isinstance(row["weight"], bool) or not isinstance(row["weight"], (int, float))
                or not math.isfinite(row["weight"]) or row["weight"] <= 0):
            raise ValueError(f"Invalid sampling weight: {row['record_id']}")
        if not isinstance(row["systems"], dict) or set(row["systems"]) != set(systems):
            raise ValueError(f"System contribution mismatch: {row['record_id']}")
        for system in systems if additive else ():
            contribution = row["systems"][system]
            if (not isinstance(contribution, dict)
                    or set(contribution) != {"numerator", "denominator"}):
                raise ValueError(f"Invalid contribution: {row['record_id']}:{system}")
            for field, value in contribution.items():
                if (isinstance(value, bool) or not isinstance(value, (int, float))
                        or not math.isfinite(value) or value < 0):
                    raise ValueError(f"Invalid {field}: {row['record_id']}:{system}")
        if not isinstance(row["strata"], dict) or set(row["strata"]) != set(stratum_levels):
            raise ValueError(f"Stratum fields mismatch: {row['record_id']}")
        for axis, levels in stratum_levels.items():
            if row["strata"][axis] not in levels:
                raise ValueError(f"Unknown {axis} level: {row['record_id']}")


def analyze(rows, systems, stratum_levels, seed, resamples, confidence,
            estimator=ratio_estimator):
    if (not isinstance(systems, list) or not systems or len(systems) != len(set(systems))
            or any(not isinstance(system, str) or not system for system in systems)):
        raise ValueError("systems must be a nonempty list of unique strings")
    if isinstance(resamples, bool) or not isinstance(resamples, int) or resamples < 1:
        raise ValueError("resamples must be a positive integer")
    if (not isinstance(seed, str) or not seed or isinstance(confidence, bool)
            or not isinstance(confidence, (int, float)) or not 0 < confidence < 1):
        raise ValueError("seed and confidence are invalid")
    if (not isinstance(stratum_levels, dict)
            or any(not isinstance(axis, str) or not axis or not isinstance(levels, list)
                   or not levels or any(not isinstance(level, str) or not level for level in levels)
                   or len(levels) != len(set(levels))
                   for axis, levels in stratum_levels.items())):
        raise ValueError("stratum_levels must map axes to nonempty unique level lists")
    validate_rows(rows, systems, stratum_levels, estimator is ratio_estimator)

    def scope(subset, label):
        return {
            "row_count": len(subset),
            "primary_document": bootstrap_scope(
                subset, systems, estimator, "document_id", "length_stratum",
                f"{seed}:{label}:document", resamples, confidence,
            ),
            "canonical_form_sensitivity": bootstrap_scope(
                subset, systems, estimator, "canonical_type_id", None,
                f"{seed}:{label}:canonical_form", resamples, confidence,
            ),
        }

    return {
        "overall": scope(rows, "overall"),
        "prespecified_strata": {
            axis: {
                level: scope(
                    [row for row in rows if row["strata"][axis] == level],
                    f"{axis}={level}",
                )
                for level in levels
            }
            for axis, levels in stratum_levels.items()
        },
    }


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contributions", type=Path)
    parser.add_argument("--metric-contract", type=Path, default=ROOT / "metric_contract.json")
    parser.add_argument("--strata-contract", type=Path, default=ROOT / "resources/evaluation_strata.json")
    args = parser.parse_args()
    try:
        data = load(args.contributions)
        settings = load(args.metric_contract)["benchmark_mwe_evaluation"]["bootstrap"]
        if data.get("bootstrap_contract_version") != settings["contract_version"]:
            raise ValueError("bootstrap_contract_version mismatch")
        allowed = load(args.strata_contract)["prespecified_strata"]
        axes = data["prespecified_strata"]
        if len(axes) != len(set(axes)) or any(axis not in allowed for axis in axes):
            raise ValueError("Unknown or duplicate prespecified stratum")
        result = analyze(
            data["rows"], data["systems"],
            {axis: allowed[axis]["levels"] for axis in axes},
            settings["seed"], settings["resamples"], settings["confidence_level"],
        )
        result.update({
            "metric_id": data["metric_id"],
            "bootstrap_contract_version": settings["contract_version"],
            "seed": settings["seed"],
            "resamples": settings["resamples"],
        })
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
