#!/usr/bin/env python3
"""Build the IR-132 purposive VID pilot population log without source text."""

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from audit_streusle_kaikki_vid import (
    load_record, parse_entries, parse_rows, sense_summary,
)
from audit_streusle_oewn_coverage import SLOT_TOKENS, load_verb_entries
from check_streusle_v5 import inspect_checkout


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "benchmarks/streusle_v5_vpc_vid.json"
CONTRACT = ROOT / "resources/hybrid_sense_inventory_contract_2026_09_03.json"
QUEUE = ROOT / "resources/sense_mapping_queue.json"
DEFAULT_CACHE = ROOT / "research_data/kaikki_en_2026_08_05_vid_exact"
QUEUE_SHA256 = "266df189990477925f5fd16a524da7256ab14ac5ac9491416b649b95623228d8"
PILOT = (
    ("make sure", "exact_oewn", "highest_train_frequency_exact_oewn"),
    ("make it", "exact_oewn", "previously_exposed_vid_pilot_polysemy"),
    ("get it", "exact_oewn", "previously_exposed_vid_pilot_polysemy"),
    ("cut short", "exact_oewn", "discontinuous_polysemous_exact_oewn"),
    ("waste time", "unique_slot_oewn", "high_frequency_discontinuous_slot_route"),
    ("take the time", "exact_kaikki", "highest_train_frequency_exact_kaikki"),
    ("let know", "exact_kaikki", "high_frequency_fully_discontinuous_exact_kaikki"),
    ("take time", "exact_kaikki", "polysemous_discontinuous_exact_kaikki"),
    ("have it", "exact_kaikki", "complete_source_sense_ids_exact_kaikki"),
    ("jump - start", "nonexact_candidate", "cross_resource_nonexact_candidate"),
    ("home - cook", "nonexact_candidate", "kaikki_nonexact_candidate"),
    ("think so", "nonexact_candidate", "declared_variant_nonexact_candidate"),
    ("get do", "no_bounded_route", "highest_train_frequency_discontinuous_no_route"),
    ("be a joke", "no_bounded_route", "high_frequency_contiguous_no_route"),
)


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def train_stats(sentences):
    result = defaultdict(lambda: {"occurrences": 0, "discontinuous": 0})
    for sentence in sentences:
        for occurrence in sentence["smwes"].values():
            if occurrence["lexcat"] != "V.VID":
                continue
            row = result[occurrence["lexlemma"].casefold()]
            row["occurrences"] += 1
            row["discontinuous"] += (
                max(occurrence["toknums"]) - min(occurrence["toknums"]) + 1
                > len(occurrence["toknums"])
            )
    return result


def route(lemma, verbs, skeletons, cache, queue):
    if lemma in verbs:
        return {
            "mapping_route": "exact_oewn",
            "source_entry_lemma": lemma,
            "candidate_units": verbs[lemma],
            "stable_source_sense_ids": verbs[lemma],
            "candidate_sources": ["oewn"],
            "eligibility_state": "source_candidate_ready_for_independent_review",
            "rights_state": "public_with_oewn_wordnet_notice",
        }
    skeleton = tuple(token for token in lemma.split() if token not in SLOT_TOKENS)
    candidates = skeletons.get(skeleton, set())
    if len(candidates) == 1:
        source_lemma = next(iter(candidates))
        return {
            "mapping_route": "unique_slot_oewn",
            "source_entry_lemma": source_lemma,
            "candidate_units": verbs[source_lemma],
            "stable_source_sense_ids": verbs[source_lemma],
            "candidate_sources": ["oewn"],
            "eligibility_state": "source_candidate_mapping_review_required",
            "rights_state": "public_with_oewn_wordnet_notice",
        }
    record = load_record(cache, lemma)
    counts = sense_summary(parse_entries(parse_rows(record), lemma))
    if counts["entries"]:
        return {
            "mapping_route": "exact_kaikki",
            "source_entry_lemma": lemma,
            "candidate_units": counts["lexicalized_candidate_senses"],
            "stable_source_sense_ids": counts["lexicalized_senses_with_wiktionary_senseid"],
            "candidate_sources": ["enwiktionary-kaikki"],
            "eligibility_state": "source_candidate_rights_and_identity_gate_pending",
            "rights_state": "withheld_pending_underlying_dump_hash_and_imported_content_review",
        }
    queued = queue[lemma]
    if queued["candidates"]:
        return {
            "mapping_route": "nonexact_candidate",
            "source_entry_lemma": None,
            "candidate_units": len(queued["candidates"]),
            "stable_source_sense_ids": 0,
            "candidate_sources": sorted({
                candidate["source_inventory_id"] for candidate in queued["candidates"]
            }),
            "eligibility_state": "source_candidate_mapping_review_required",
            "rights_state": queued["rights_state"],
        }
    return {
        "mapping_route": "no_bounded_route",
        "source_entry_lemma": None,
        "candidate_units": 0,
        "stable_source_sense_ids": 0,
        "candidate_sources": [],
        "eligibility_state": "project_lexicography_required_no_bounded_source_route",
        "rights_state": "no_source_candidate_content",
    }


def build(checkout, oewn, cache):
    if file_digest(QUEUE) != QUEUE_SHA256:
        raise ValueError("IR-130 queue changed after the pilot ID allocation.")
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    _, datasets = inspect_checkout(checkout, profile)
    verbs = load_verb_entries(oewn)
    queue_items = {
        item["input_canonical_lemma"]: item
        for item in json.loads(QUEUE.read_text(encoding="utf-8"))["items"]
    }
    skeletons = defaultdict(set)
    for lemma in verbs:
        if " " in lemma:
            skeletons[tuple(
                token for token in lemma.split() if token not in SLOT_TOKENS
            )].add(lemma)
    stats = train_stats(datasets["train"])

    next_type_number = 151
    rows = []
    for priority, (lemma, expected_route, stratum) in enumerate(PILOT, 1):
        source = route(lemma, verbs, skeletons, cache, queue_items)
        if source["mapping_route"] != expected_route or lemma not in stats:
            raise ValueError(f"Frozen pilot evidence changed for {lemma}.")
        if lemma in queue_items:
            type_id = queue_items[lemma]["type_id"]
            id_source = "ir130_registry"
        else:
            type_id = f"ldfreq-en-vmwe-t{next_type_number:06d}"
            next_type_number += 1
            id_source = "ir132_append_only_reservation"
        rows.append({
            "priority": priority,
            "type_id": type_id,
            "type_id_source": id_source,
            "canonical_lemma": lemma,
            "observed_vmwe_categories": ["V.VID"],
            "selection_stratum": stratum,
            "train_occurrences": stats[lemma]["occurrences"],
            "train_discontinuous_occurrences": stats[lemma]["discontinuous"],
            "fixed_slot_state": (
                "source_candidate_differs_by_frozen_closed_class_slot"
                if expected_route == "unique_slot_oewn"
                else "canonical_members_preserved_no_slot_transform"
            ),
            "literal_contrast_state": "future_occurrence_level_negative_required_not_supplied_by_dictionary_route",
            **source,
        })

    route_counts = Counter(row["mapping_route"] for row in rows)
    eligibility_counts = Counter(row["eligibility_state"] for row in rows)
    unresolved = route_counts["no_bounded_route"]
    return {
        "log_schema_version": "1.0.0",
        "log_id": "ldfreq-ir132-vid-pilot-population-2026-09-05",
        "generated_on": "2026-09-05",
        "status": "pilot_population_frozen_candidate_population_partial_human_review_pending",
        "task": "IR-132",
        "dependencies": {
            "contract": {
                "path": str(CONTRACT.relative_to(ROOT)),
                "sha256": file_digest(CONTRACT),
                "version": "1.0.0",
            },
            "streusle_profile": {
                "path": str(PROFILE.relative_to(ROOT)),
                "sha256": file_digest(PROFILE),
            },
            "ir130_queue": {
                "path": str(QUEUE.relative_to(ROOT)),
                "sha256": QUEUE_SHA256,
            },
            "generator": {
                "path": "scripts/build_inventory_population_log.py",
                "sha256": file_digest(Path(__file__)),
            },
        },
        "selection_contract": {
            "population": "STREUSLE 5.0 train V.VID types only",
            "method": "purposive fixed stress-test strata, not probability sampling",
            "uses_dev_or_test_type_statistics": False,
            "uses_sentence_text_or_context": False,
            "uses_model_predictions_or_scores": False,
            "inference_limit": "The batch tests inventory workflow feasibility and cannot estimate type prevalence, mapping coverage, or system performance.",
        },
        "id_registry": {
            "preserved_ir130_ids": sorted(
                row["type_id"] for row in rows if row["type_id_source"] == "ir130_registry"
            ),
            "new_reserved_range": "ldfreq-en-vmwe-t000151..ldfreq-en-vmwe-t000159",
            "reservation_rule": "IDs are permanent; rejected or deferred types retain their IDs and IDs are never reassigned.",
        },
        "source_identity": {
            "streusle_version": "5.0",
            "streusle_commit": profile["source"]["commit"],
            "streusle_artifacts": profile["artifacts"],
            "oewn_version": "2025-edition",
            "oewn_artifact_sha256": "7d749f6e2c39e6970e4997839dcf6e42fd281f3c2fae0171d2192bae8cfa4b51",
            "kaikki_version": "dump-2026-08-05_extract-2026-08-28",
            "kaikki_artifact_sha256": "506ae4786da452d066d58b580e0417aa4eb60c8b181d1a2d2cea82cf68508462",
        },
        "summary": {
            "pilot_types": len(rows),
            "train_occurrences": sum(row["train_occurrences"] for row in rows),
            "train_discontinuous_occurrences": sum(
                row["train_discontinuous_occurrences"] for row in rows
            ),
            "mapping_route_counts": dict(sorted(route_counts.items())),
            "eligibility_state_counts": dict(sorted(eligibility_counts.items())),
            "types_with_candidate_route": len(rows) - unresolved,
            "types_without_bounded_route": unresolved,
            "mapping_unresolved_rate": round(unresolved / len(rows), 6),
            "eligibility_state_recorded_for_every_type": all(
                row["eligibility_state"] for row in rows
            ),
        },
        "release_boundary": {
            "source_sentence_or_token_text_bundled": False,
            "dictionary_gloss_or_example_bundled": False,
            "person_level_data_bundled": False,
            "formal_sense_admissions": 0,
            "runtime_integration": "none",
            "human_annotation_authorized": False,
        },
        "pilot_batch": rows,
    }


def self_check():
    data = train_stats([{"smwes": {
        "1": {"lexcat": "V.VID", "lexlemma": "Make It", "toknums": [1, 3]},
        "2": {"lexcat": "V.VPC.full", "lexlemma": "take in", "toknums": [4, 5]},
    }}])
    assert data["make it"] == {"occurrences": 1, "discontinuous": 1}
    assert "take in" not in data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, nargs="?")
    parser.add_argument("oewn", type=Path, nargs="?")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("Inventory population log self-check: PASS")
        return
    if args.checkout is None or args.oewn is None:
        parser.error("STREUSLE checkout and OEWN zip are required unless --self-check is used")
    rendered = json.dumps(
        build(args.checkout, args.oewn, args.cache), ensure_ascii=False, indent=2
    ) + "\n"
    if args.check:
        if args.check.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Inventory population log differs from {args.check}.")
    elif args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
