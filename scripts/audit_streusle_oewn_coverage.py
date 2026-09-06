#!/usr/bin/env python3
"""Audit exact OEWN sense-inventory coverage of STREUSLE VPC/VID types."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

from check_streusle_v5 import inspect_checkout, sha256
from extract_oewn_take_in import ARTIFACT_SHA256


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = ROOT / "benchmarks/streusle_v5_vpc_vid.json"
SLOT_TOKENS = {
    "a", "an", "her", "his", "its", "my", "one's", "our", "someone's",
    "somebody's", "the", "their", "your",
}


def load_verb_entries(source):
    if sha256(source) != ARTIFACT_SHA256:
        raise ValueError("OEWN artifact SHA-256 does not match the reviewed release asset.")
    verbs = {}
    with ZipFile(source) as archive:
        for name in archive.namelist():
            if not name.startswith("entries-") or not name.endswith(".json"):
                continue
            for lemma, entries in json.loads(archive.read(name)).items():
                senses = entries.get("v", {}).get("sense")
                if senses is not None:
                    key = lemma.casefold()
                    candidate = (lemma == key, len(senses))
                    if key not in verbs or candidate[0] > verbs[key][0]:
                        verbs[key] = candidate
                    elif candidate[0] == verbs[key][0] and candidate[1] != verbs[key][1]:
                        raise ValueError(f"Ambiguous OEWN verb entry: {lemma}.")
    return {key: value[1] for key, value in verbs.items()}


def summarize(datasets, category_mapping, verbs):
    rows = []
    type_rows = defaultdict(list)
    for split, sentences in datasets.items():
        for sentence in sentences:
            for occurrence in sentence["smwes"].values():
                if occurrence["lexcat"] not in category_mapping:
                    continue
                lemma = occurrence["lexlemma"].casefold()
                sense_count = verbs.get(lemma)
                row = {
                    "split": split,
                    "lemma": lemma,
                    "category": occurrence["lexcat"],
                    "sense_count": sense_count,
                    "discontinuous": (
                        max(occurrence["toknums"]) - min(occurrence["toknums"]) + 1
                        > len(occurrence["toknums"])
                    ),
                }
                rows.append(row)
                type_rows[lemma].append(row)

    def counts(items):
        return {
            "total": len(items),
            "exact_oewn_match": sum(item["sense_count"] is not None for item in items),
            "polysemous_oewn_entry": sum((item["sense_count"] or 0) >= 2 for item in items),
            "monosemous_oewn_entry": sum(item["sense_count"] == 1 for item in items),
            "no_exact_oewn_entry": sum(item["sense_count"] is None for item in items),
        }

    categories = sorted(category_mapping)
    splits = ["train", "dev", "test"]
    type_items = [items[0] for items in type_rows.values()]
    distribution = Counter(item["sense_count"] for item in type_items
                           if item["sense_count"] is not None)
    skeleton_index = defaultdict(list)
    for lemma in verbs:
        if " " in lemma:
            skeleton = tuple(token for token in lemma.split() if token not in SLOT_TOKENS)
            skeleton_index[skeleton].append(lemma)
    unmatched_candidate_rows = []
    unmatched_candidate_types = []
    unique_candidate_pairs = []
    for lemma, items in sorted(type_rows.items()):
        if items[0]["sense_count"] is not None:
            continue
        skeleton = tuple(token for token in lemma.split() if token not in SLOT_TOKENS)
        candidates = sorted(set(skeleton_index.get(skeleton, [])))
        status = "none" if not candidates else "unique" if len(candidates) == 1 else "multiple"
        unmatched_candidate_rows.extend({"status": status, "category": item["category"]}
                                        for item in items)
        unmatched_candidate_types.extend({"status": status, "category": category}
                                         for category in {item["category"] for item in items})
        if status == "unique":
            unique_candidate_pairs.append({
                "streusle_lemma": lemma,
                "oewn_candidate": candidates[0],
                "occurrences": len(items),
                "categories": sorted({item["category"] for item in items}),
            })
    candidate_statuses = ("none", "unique", "multiple")
    return {
        "matching_rule": "Unicode-casefolded exact STREUSLE lexlemma to OEWN lemma with part of speech v; no slot, article, or lexical normalization",
        "construct_warning": "An exact entry and sense count establish inventory candidates only, not occurrence truth, contextual adequacy, or observed polysemy.",
        "occurrence_counts": counts(rows),
        "type_counts": counts(type_items),
        "occurrence_counts_by_split": {
            split: counts([item for item in rows if item["split"] == split])
            for split in splits
        },
        "occurrence_counts_by_category": {
            category: counts([item for item in rows if item["category"] == category])
            for category in categories
        },
        "type_counts_by_category": {
            category: counts([
                items[0] for items in type_rows.values()
                if any(item["category"] == category for item in items)
            ])
            for category in categories
        },
        "category_type_count_warning": "A canonical type with conflicting STREUSLE categories is counted once in each represented category, so category type totals need not equal the global type total.",
        "polysemous_discontinuous_occurrences": sum(
            item["discontinuous"] and (item["sense_count"] or 0) >= 2 for item in rows
        ),
        "matched_type_sense_count_distribution": {
            str(key): distribution[key] for key in sorted(distribution)
        },
        "types_with_conflicting_categories": [
            lemma for lemma, items in sorted(type_rows.items())
            if len({item["category"] for item in items}) > 1
        ],
        "named_type_checks": {
            lemma.replace(" ", "_"): {
                "occurrences": len(type_rows.get(lemma, [])),
                "exact_oewn_sense_count": verbs.get(lemma),
            }
            for lemma in ("take in", "spill the beans")
        },
        "slot_skeleton_candidate_audit": {
            "rule": "Remove only the declared article/possessive-slot tokens from unmatched STREUSLE and OEWN multiword verb lemmas, then require exact remaining token order.",
            "removed_tokens": sorted(SLOT_TOKENS),
            "warning": "A skeleton match is an unreviewed mapping candidate, not an accepted lemma equivalence or contextual sense.",
            "unmatched_occurrence_counts": {
                status: sum(item["status"] == status for item in unmatched_candidate_rows)
                for status in candidate_statuses
            },
            "unmatched_occurrence_counts_by_category": {
                category: {
                    status: sum(item["status"] == status and item["category"] == category
                                for item in unmatched_candidate_rows)
                    for status in candidate_statuses
                }
                for category in categories
            },
            "unmatched_type_counts": {
                status: sum(item["status"] == status for item in unmatched_candidate_types)
                for status in candidate_statuses
            },
            "unmatched_type_counts_by_category": {
                category: {
                    status: sum(item["status"] == status and item["category"] == category
                                for item in unmatched_candidate_types)
                    for status in candidate_statuses
                }
                for category in categories
            },
            "unique_candidate_pairs": unique_candidate_pairs,
        },
    }


def build_audit(checkout, oewn, profile):
    _, datasets = inspect_checkout(checkout, profile)
    summary = summarize(datasets, profile["projection"]["category_mapping"],
                        load_verb_entries(oewn))
    return {
        "audit_version": "1.2.0",
        "audit_id": "streusle-v5-oewn-2025-exact-coverage",
        "purpose": "Measure the maximum exact inventory-lookup pool before designing a new contextual-sense annotation benchmark.",
        "source_identity": {
            "streusle_tag": profile["source"]["tag"],
            "streusle_commit": profile["source"]["commit"],
            "streusle_profile": "benchmarks/streusle_v5_vpc_vid.json",
            "streusle_artifacts": profile["artifacts"],
            "oewn_release": "2025-edition",
            "oewn_sha256": ARTIFACT_SHA256,
        },
        "summary": summary,
        "decision": "Use this as a target-population and normalization audit only. Do not select only exact matches as benchmark gold, because that would hide inventory gaps and bias against non-canonical VID forms.",
    }


def self_check():
    datasets = {
        "train": [{"smwes": {
            "1": {"lexcat": "V.VPC.full", "lexlemma": "Take In", "toknums": [1, 3]},
            "2": {"lexcat": "V.VID", "lexlemma": "spill beans", "toknums": [4, 5]},
        }}],
        "dev": [],
        "test": [],
    }
    report = summarize(datasets, {"V.VPC.full": "VPC.full", "V.VID": "VID"},
                       {"take in": 17, "one sense": 1})
    assert report["occurrence_counts"]["total"] == 2
    assert report["occurrence_counts"]["polysemous_oewn_entry"] == 1
    assert report["polysemous_discontinuous_occurrences"] == 1
    assert report["type_counts"]["no_exact_oewn_entry"] == 1
    assert report["slot_skeleton_candidate_audit"]["unmatched_occurrence_counts"]["none"] == 1
    assert report["slot_skeleton_candidate_audit"]["unmatched_type_counts"]["none"] == 1
    return {"self_check": "pass"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, nargs="?")
    parser.add_argument("oewn", type=Path, nargs="?")
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_check:
            result = self_check()
        else:
            if args.checkout is None or args.oewn is None:
                raise ValueError("A STREUSLE checkout and OEWN zip are required.")
            profile = json.loads(args.profile.read_text(encoding="utf-8"))
            result = build_audit(args.checkout, args.oewn, profile)
            if args.check and result != json.loads(args.check.read_text(encoding="utf-8")):
                raise ValueError(f"Audit differs from {args.check}.")
    except (AssertionError, OSError, json.JSONDecodeError, KeyError, TypeError,
            ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
