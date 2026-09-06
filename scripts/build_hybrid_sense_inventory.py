#!/usr/bin/env python3
"""Build the IR-131/132 OEWN candidate seed with stable ID reservations."""

import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "resources/hybrid_sense_inventory_contract_2026_09_03.json"
SCHEMA = ROOT / "resources/hybrid_sense_inventory.schema.json"
PILOT_DESIGN = ROOT / "resources/simplewiki_gate1_route2_design.json"
IR130_QUEUE = ROOT / "resources/sense_mapping_queue.json"
VID_LOG = ROOT / "resources/inventory_population_log.json"
ARTIFACT_SHA256 = "7d749f6e2c39e6970e4997839dcf6e42fd281f3c2fae0171d2192bae8cfa4b51"
PILOT_DESIGN_SHA256 = "c4bb1a03b4a63c6e83f23f2589452070a9e5b9b4f3a879d10184d98c16e07cbb"
IR130_QUEUE_SHA256 = "266df189990477925f5fd16a524da7256ab14ac5ac9491416b649b95623228d8"
VPC_FORMS = ("take in", "pick up", "give up", "come out")
NOTICE = ["resources/OEWN_WORDNET_NOTICE.txt"]
LICENSE = "CC-BY-4.0 AND LicenseRef-WordNet"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    return digest(path.read_bytes())


def compact(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def source_projection(source_form, source_sense, synset):
    return {
        "source_inventory_id": "oewn",
        "source_version": "2025-edition",
        "source_entry_id": f"{source_form}#v",
        "source_sense_id": source_sense["id"],
        "part_of_speech": "v",
        "glosses": synset["definition"],
        "examples": {
            "synset": synset.get("example", []),
            "entry": source_sense.get("sent", []),
        },
        "usage_labels": synset.get("usage", []),
        "source_synset_id": source_sense["synset"],
        "cili_ili": synset["ili"],
        "synset_members": synset["members"],
    }


def candidate(source_form, type_id, project_id, source_sense, synset, mapping_route):
    projection = source_projection(source_form, source_sense, synset)
    rights = {
        "controlling_license_id": LICENSE,
        "attribution_notice_ids": NOTICE,
        "redistribution_status": "permitted",
    }
    return {
        "reserved_project_sense_id": project_id,
        "reservation_state": "reserved_candidate_not_admitted",
        "proposed_source_basis": "oewn_anchored",
        "source_synset_id": source_sense["synset"],
        "cili": {
            "registry": "Collaborative Interlingual Index",
            "ili": synset["ili"],
        },
        "definition": {
            "text": synset["definition"][0],
            "origin": "source_verbatim",
            **rights,
        },
        "examples": {
            "items": projection["examples"],
            **rights,
        },
        "usage_labels": projection["usage_labels"],
        "identity_relations": {
            "supersedes": [],
            "split_from": [],
            "merged_from": [],
            "related_to": [],
        },
        "source_links": [{
            "source_inventory_id": "oewn",
            "source_version": "2025-edition",
            "source_repository_commit": "dc343f2683279ecbb13fab4e2fd778d7b162d287",
            "source_artifact_sha256": ARTIFACT_SHA256,
            "source_entry_id": f"{source_form}#v",
            "source_sense_id": source_sense["id"],
            "source_record_sha256": digest(compact(projection)),
            "mapping_relation": "candidate_only",
            "mapping_route": mapping_route,
            "verification_status": "unreviewed",
            "controlling_license_id": LICENSE,
            "attribution_notice_ids": NOTICE,
        }],
        "source_relations": [
            {
                "relation": "synset_member",
                "source_member_index": index,
                "target_lemma": member,
                "project_identity_action": (
                    "same_source_entry" if member == source_form else "related_not_merged"
                ),
            }
            for index, member in enumerate(synset["members"])
        ],
        "rights": rights,
    }


def sense_id_assignments(type_id, source_senses, prior_type=None):
    prior = {}
    if prior_type:
        for item in prior_type["candidate_set"]["candidates"]:
            source_id = item["source_links"][0]["source_sense_id"]
            if source_id in prior:
                raise ValueError(f"Duplicate prior source sense: {source_id}.")
            prior[source_id] = item["reserved_project_sense_id"]
    current = [item["id"] for item in source_senses]
    if len(current) != len(set(current)):
        raise ValueError(f"Duplicate current source sense under {type_id}.")
    missing = set(prior) - set(current)
    if missing:
        raise ValueError(
            f"Source senses disappeared under {type_id}; record lifecycle decisions first."
        )
    used = {
        int(match.group(1))
        for project_id in prior.values()
        if (match := re.fullmatch(re.escape(type_id) + r"-s(\d{3})", project_id))
    }
    if len(used) != len(prior):
        raise ValueError(f"Invalid or colliding prior project sense IDs under {type_id}.")
    next_number = max(used, default=0) + 1
    result = {}
    for source_id in current:
        if source_id in prior:
            result[source_id] = prior[source_id]
        else:
            result[source_id] = f"{type_id}-s{next_number:03d}"
            next_number += 1
    return result


def build(source, prior=None):
    if file_digest(source) != ARTIFACT_SHA256 or source.stat().st_size != 9986555:
        raise ValueError("OEWN artifact does not match the reviewed 2025 release.")
    if file_digest(PILOT_DESIGN) != PILOT_DESIGN_SHA256:
        raise ValueError("Pilot-form design changed after target exposure.")
    if file_digest(IR130_QUEUE) != IR130_QUEUE_SHA256:
        raise ValueError("IR-130 ID registry dependency changed.")

    pilot = json.loads(PILOT_DESIGN.read_text(encoding="utf-8"))
    targets = pilot["target_derivation"]["targets"][:4]
    if tuple(target["canonical_form"] for target in targets) != VPC_FORMS:
        raise ValueError("Frozen pilot VPC order changed.")
    vid_log = json.loads(VID_LOG.read_text(encoding="utf-8"))
    vid_targets = vid_log["pilot_batch"][:5]
    if [target["mapping_route"] for target in vid_targets] != [
            "exact_oewn", "exact_oewn", "exact_oewn", "exact_oewn",
            "unique_slot_oewn"]:
        raise ValueError("IR-132 OEWN candidate subset changed.")

    type_specs = [
        {
            "type_id": f"ldfreq-en-vmwe-t{number:06d}",
            "canonical_lemma": target["canonical_form"],
            "source_entry_lemma": target["canonical_form"],
            "observed_vmwe_categories": list(target["streusle_train_categories"]),
            "mapping_route": "exact_oewn",
            "candidate_units": target["oewn_sense_count"],
        }
        for number, target in enumerate(targets, 147)
    ] + vid_targets
    prior_types = {
        item["type_id"]: item for item in (prior or {}).get("types", [])
    }

    with ZipFile(source) as archive:
        entries = {
            spec["source_entry_lemma"]: json.loads(archive.read(
                f"entries-{spec['source_entry_lemma'][0]}.json"
            ))[spec["source_entry_lemma"]]["v"]
            for spec in type_specs
        }
        synsets = {}
        for name in archive.namelist():
            if name.startswith("verb.") and name.endswith(".json"):
                synsets.update(json.loads(archive.read(name)))

    types = []
    for spec in type_specs:
        form = spec["canonical_lemma"]
        source_form = spec["source_entry_lemma"]
        type_id = spec["type_id"]
        source_senses = entries[source_form]["sense"]
        assignments = sense_id_assignments(
            type_id, source_senses, prior_types.get(type_id)
        )
        candidates = []
        for source_sense in source_senses:
            synset = synsets[source_sense["synset"]]
            if (synset["partOfSpeech"] != "v" or source_form not in synset["members"] or
                    len(synset["definition"]) != 1):
                raise ValueError(f"Unexpected OEWN record for {source_sense['id']}.")
            candidates.append(candidate(
                source_form, type_id, assignments[source_sense["id"]],
                source_sense, synset,
                spec["mapping_route"],
            ))
        candidates.sort(key=lambda item: item["reserved_project_sense_id"])
        if len(candidates) != spec["candidate_units"]:
            raise ValueError(f"Frozen sense count changed for {form}.")
        types.append({
            "type_id": type_id,
            "language": "en",
            "canonical_lemma": form,
            "part_of_speech": "v",
            "observed_vmwe_categories": spec["observed_vmwe_categories"],
            "member_pattern": {
                "ordered_lexical_members": form.split(),
                "variable_slots": [],
                "realization_note": "Inflection and intervening non-member gaps are occurrence properties; candidate senses do not assert occurrence membership.",
            },
            "inventory_status": "unresolved",
            "source_route_status": "candidate_route_only",
            "senses": [],
            "candidate_set": {
                "status": "complete_for_pinned_oewn_entry",
                "mapping_route": spec["mapping_route"],
                "source_entry_lemma": source_form,
                "review_state": "pending_independent_review",
                "adjudication_state": "not_started",
                "candidates": candidates,
            },
        })

    anchor_rows = []
    for item in types:
        anchor_rows.append(f"{item['type_id']}\t{item['canonical_lemma']}")
        for item_candidate in item["candidate_set"]["candidates"]:
            anchor_rows.append("\t".join((
                item_candidate["reserved_project_sense_id"],
                item_candidate["source_links"][0]["source_sense_id"],
            )))

    return {
        "inventory_schema_version": "1.0.0-candidate.3",
        "inventory_id": "ldfreq-en-vmwe-hybrid-sense-inventory-v1",
        "generated_on": "2026-09-05",
        "status": "vpc_and_vid_candidate_seed_complete_independent_review_pending_no_admitted_senses",
        "task": "IR-131/IR-132/IR-133",
        "dependencies": {
            "contract": {
                "path": str(CONTRACT.relative_to(ROOT)),
                "sha256": file_digest(CONTRACT),
                "version": json.loads(CONTRACT.read_text(encoding="utf-8"))["contract_version"],
            },
            "schema": {
                "path": str(SCHEMA.relative_to(ROOT)),
                "sha256": file_digest(SCHEMA),
                "draft": "2020-12",
            },
            "pilot_form_design": {
                "path": str(PILOT_DESIGN.relative_to(ROOT)),
                "sha256": PILOT_DESIGN_SHA256,
                "role": "previously_exposed_target_conditioned_training_development_forms_only",
            },
            "prior_type_registry": {
                "path": str(IR130_QUEUE.relative_to(ROOT)),
                "sha256": IR130_QUEUE_SHA256,
                "reserved_type_id_range": "ldfreq-en-vmwe-t000001..ldfreq-en-vmwe-t000146",
            },
            "vid_population_log": {
                "path": str(VID_LOG.relative_to(ROOT)),
                "sha256": file_digest(VID_LOG),
                "role": "purposive_training_only_vid_pilot_and_append_only_id_reservations",
            },
            "generator": {
                "path": "scripts/build_hybrid_sense_inventory.py",
                "sha256": file_digest(Path(__file__)),
            },
        },
        "id_registry": {
            "allocation": "Append after the IR-130 range in frozen pilot priority and OEWN source order.",
            "allocated_type_id_range": "ldfreq-en-vmwe-t000147..ldfreq-en-vmwe-t000155",
            "population_log_only_reserved_type_id_range": "ldfreq-en-vmwe-t000156..ldfreq-en-vmwe-t000159",
            "reservation_rule": "A reserved candidate sense ID is permanent and, if admitted after review, moves unchanged into senses; rejected IDs remain retired and are never reassigned.",
            "source_update_rule": "Regenerate with --prior OLD_INVENTORY; match existing reservations by project type ID plus source sense key, append IDs for new source senses, and fail if a prior source sense disappears before a lifecycle decision is recorded.",
            "stability_anchor_format": "UTF-8 rows of type_id<TAB>lemma followed by reserved_project_sense_id<TAB>source_sense_id, LF joined, no final LF",
            "stability_anchor_sha256": digest("\n".join(anchor_rows).encode("utf-8")),
        },
        "source_snapshot": {
            "source_inventory_id": "oewn",
            "source_version": "2025-edition",
            "release_date": "2025-12-31",
            "repository_commit": "dc343f2683279ecbb13fab4e2fd778d7b162d287",
            "artifact_name": "english-wordnet-2025-json.zip",
            "artifact_size_bytes": 9986555,
            "artifact_sha256": ARTIFACT_SHA256,
            "artifact_url": "https://github.com/globalwordnet/english-wordnet/releases/download/2025-edition/english-wordnet-2025-json.zip",
            "public_notice": NOTICE[0],
        },
        "fingerprint_projection_fields": [
            "source_inventory_id", "source_version", "source_entry_id",
            "source_sense_id", "part_of_speech", "glosses", "examples",
            "usage_labels", "source_synset_id", "cili_ili", "synset_members",
        ],
        "summary": {
            "pilot_forms": len(types),
            "vpc_pilot_forms": 4,
            "vid_pilot_forms": 5,
            "candidate_senses": sum(
                len(item["candidate_set"]["candidates"]) for item in types
            ),
            "admitted_senses": 0,
            "forms_without_candidates": [],
            "source_synonyms_merged_into_project_identity": 0,
        },
        "release_boundary": {
            "inventory_layer_license": LICENSE,
            "source_wording_bundled": True,
            "source_examples_bundled": True,
            "raw_source_artifact_bundled": False,
            "corpus_occurrence_or_context_bundled": False,
            "browser_runtime_integration": "none",
            "human_annotation_authorized": False,
            "admission_gate": "two independent reviews and adjudication remain required before candidates enter senses",
        },
        "types": types,
    }


def self_check():
    projection = {
        "source_inventory_id": "oewn", "source_version": "x",
        "source_entry_id": "a#v", "source_sense_id": "a%2:00:00::",
        "part_of_speech": "v", "glosses": ["g"],
        "examples": {"synset": [], "entry": []}, "usage_labels": [],
        "source_synset_id": "00000000-v", "cili_ili": "i1",
        "synset_members": ["a"],
    }
    assert digest(compact(projection)) == digest(compact(dict(reversed(list(projection.items())))))
    prior_type = {"candidate_set": {"candidates": [
        {"reserved_project_sense_id": "ldfreq-en-vmwe-t000001-s001",
         "source_links": [{"source_sense_id": "old-a"}]},
        {"reserved_project_sense_id": "ldfreq-en-vmwe-t000001-s002",
         "source_links": [{"source_sense_id": "old-b"}]},
    ]}}
    assignments = sense_id_assignments(
        "ldfreq-en-vmwe-t000001", [{"id": "old-b"}, {"id": "new-c"}, {"id": "old-a"}],
        prior_type,
    )
    assert assignments == {
        "old-a": "ldfreq-en-vmwe-t000001-s001",
        "old-b": "ldfreq-en-vmwe-t000001-s002",
        "new-c": "ldfreq-en-vmwe-t000001-s003",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, nargs="?")
    parser.add_argument("--check", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--prior", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("Hybrid sense inventory self-check: PASS")
        return
    if args.source is None:
        parser.error("source OEWN zip is required unless --self-check is used")
    prior = json.loads(args.prior.read_text(encoding="utf-8")) if args.prior else None
    rendered = json.dumps(build(args.source, prior), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if args.check.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Hybrid sense inventory differs from {args.check}.")
    elif args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
