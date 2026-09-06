import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import unittest
from unittest.mock import patch


ROOT = Path(__file__).parents[1]
INVENTORY_PATH = ROOT / "resources/hybrid_sense_inventory_v1.json"
POPULATION_LOG_PATH = ROOT / "resources/inventory_population_log.json"
SCHEMA_PATH = ROOT / "resources/hybrid_sense_inventory.schema.json"
QUEUE_PATH = ROOT / "resources/sense_mapping_queue.json"
SCRIPT_PATH = ROOT / "scripts/build_hybrid_sense_inventory.py"
REVIEW_PROTOCOL_PATH = ROOT / "resources/inventory_review_protocol.json"
REVIEW_SCRIPT_PATH = ROOT / "scripts/check_inventory_reviews.py"
POPULATION_SCRIPT_PATH = ROOT / "scripts/build_inventory_population_log.py"
LIFECYCLE_FIXTURE_PATH = ROOT / "tests/fixtures/sense_inventory_versions/lifecycle_exercise.json"


def digest(value):
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()


def registry_errors(inventory, queue, population_log):
    errors = []
    type_owners = {}

    def register_type(type_id, lemma):
        prior = type_owners.setdefault(type_id, lemma)
        if prior != lemma:
            errors.append(f"type ID collision: {type_id}")

    for item in queue["items"]:
        register_type(item["type_id"], item["input_canonical_lemma"])
    for item in population_log["pilot_batch"]:
        register_type(item["type_id"], item["canonical_lemma"])

    sense_ids = set()
    source_senses = set()
    for item in inventory["types"]:
        register_type(item["type_id"], item["canonical_lemma"])
        for candidate in item["candidate_set"]["candidates"]:
            sense_id = candidate["reserved_project_sense_id"]
            if sense_id in sense_ids:
                errors.append(f"sense ID collision: {sense_id}")
            sense_ids.add(sense_id)
            if not sense_id.startswith(item["type_id"] + "-s"):
                errors.append(f"wrong sense owner: {sense_id}")
            link = candidate["source_links"][0]
            source_key = tuple(link[field] for field in (
                "source_inventory_id", "source_version", "source_artifact_sha256",
                "source_entry_id", "source_sense_id",
            ))
            if source_key in source_senses:
                errors.append(f"duplicate source sense: {source_key}")
            source_senses.add(source_key)
            for targets in candidate["identity_relations"].values():
                if sense_id in targets:
                    errors.append(f"self identity relation: {sense_id}")
    return errors


class SenseInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
        cls.population_log = json.loads(POPULATION_LOG_PATH.read_text(encoding="utf-8"))

    def test_schema_required_fields_patterns_and_enums(self):
        schema = self.schema
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertTrue(set(schema["required"]).issubset(self.inventory))
        type_schema = schema["$defs"]["typeRecord"]
        candidate_schema = schema["$defs"]["candidateSense"]
        link_schema = schema["$defs"]["sourceLink"]
        type_pattern = schema["$defs"]["typeId"]["pattern"]
        sense_pattern = schema["$defs"]["senseId"]["pattern"]
        for item in self.inventory["types"]:
            self.assertEqual(set(item), set(type_schema["properties"]))
            self.assertTrue(set(type_schema["required"]).issubset(item))
            self.assertRegex(item["type_id"], type_pattern)
            self.assertIn(item["inventory_status"], type_schema["properties"]["inventory_status"]["enum"])
            self.assertIn(item["source_route_status"], type_schema["properties"]["source_route_status"]["enum"])
            for candidate in item["candidate_set"]["candidates"]:
                self.assertEqual(set(candidate), set(candidate_schema["properties"]))
                self.assertTrue(set(candidate_schema["required"]).issubset(candidate))
                self.assertRegex(candidate["reserved_project_sense_id"], sense_pattern)
                for link in candidate["source_links"]:
                    self.assertTrue(set(link_schema["required"]).issubset(link))
                    self.assertTrue(set(link).issubset(link_schema["properties"]))
        self.assertEqual(
            set(schema["$defs"]["identityRelations"]["required"]),
            {"supersedes", "split_from", "merged_from", "related_to"},
        )
        self.assertIn("identity_relations", schema["$defs"]["formalSense"]["required"])

    def test_registry_has_no_type_sense_or_source_collisions(self):
        self.assertEqual(
            registry_errors(self.inventory, self.queue, self.population_log), []
        )
        bad_type = copy.deepcopy(self.inventory)
        bad_type["types"][1]["type_id"] = bad_type["types"][0]["type_id"]
        self.assertTrue(any("type ID collision" in error for error in registry_errors(
            bad_type, self.queue, self.population_log
        )))
        bad_sense = copy.deepcopy(self.inventory)
        bad_sense["types"][1]["candidate_set"]["candidates"][0]["reserved_project_sense_id"] = (
            bad_sense["types"][0]["candidate_set"]["candidates"][0]["reserved_project_sense_id"]
        )
        self.assertTrue(any("sense ID collision" in error for error in registry_errors(
            bad_sense, self.queue, self.population_log
        )))
        bad_source = copy.deepcopy(self.inventory)
        bad_source["types"][0]["candidate_set"]["candidates"][1]["source_links"] = copy.deepcopy(
            bad_source["types"][0]["candidate_set"]["candidates"][0]["source_links"]
        )
        self.assertTrue(any("duplicate source sense" in error for error in registry_errors(
            bad_source, self.queue, self.population_log
        )))

    def test_source_update_preserves_ids_and_fails_on_silent_deletion(self):
        spec = importlib.util.spec_from_file_location("sense_builder", SCRIPT_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        prior_type = self.inventory["types"][0]
        old = {
            candidate["source_links"][0]["source_sense_id"]:
            candidate["reserved_project_sense_id"]
            for candidate in prior_type["candidate_set"]["candidates"]
        }
        reordered = [{"id": source_id} for source_id in reversed(old)] + [{"id": "new%2:00:00::"}]
        updated = module.sense_id_assignments(prior_type["type_id"], reordered, prior_type)
        self.assertEqual({source_id: updated[source_id] for source_id in old}, old)
        self.assertEqual(updated["new%2:00:00::"], prior_type["type_id"] + "-s018")
        with self.assertRaisesRegex(ValueError, "lifecycle decisions"):
            module.sense_id_assignments(prior_type["type_id"], reordered[1:], prior_type)
        with self.assertRaisesRegex(ValueError, "Duplicate current source sense"):
            module.sense_id_assignments(
                prior_type["type_id"], [{"id": next(iter(old))}, {"id": next(iter(old))}],
                None,
            )

    def test_pilot_candidate_sets_and_stable_reserved_ids(self):
        types = self.inventory["types"]
        self.assertEqual(
            [(item["type_id"], item["canonical_lemma"]) for item in types],
            [
                ("ldfreq-en-vmwe-t000147", "take in"),
                ("ldfreq-en-vmwe-t000148", "pick up"),
                ("ldfreq-en-vmwe-t000149", "give up"),
                ("ldfreq-en-vmwe-t000150", "come out"),
                ("ldfreq-en-vmwe-t000151", "make sure"),
                ("ldfreq-en-vmwe-t000152", "make it"),
                ("ldfreq-en-vmwe-t000153", "get it"),
                ("ldfreq-en-vmwe-t000154", "cut short"),
                ("ldfreq-en-vmwe-t000155", "waste time"),
            ],
        )
        self.assertEqual(
            [len(item["candidate_set"]["candidates"]) for item in types],
            [17, 16, 12, 11, 1, 3, 2, 4, 1],
        )
        ids = [
            candidate["reserved_project_sense_id"]
            for item in types for candidate in item["candidate_set"]["candidates"]
        ]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(re.fullmatch(
            r"ldfreq-en-vmwe-t\d{6}-s\d{3}", sense_id
        ) for sense_id in ids))
        for item in types:
            self.assertEqual(item["senses"], [])
            self.assertEqual(item["inventory_status"], "unresolved")
            self.assertEqual(item["source_route_status"], "candidate_route_only")
            self.assertEqual(
                [candidate["reserved_project_sense_id"] for candidate in item["candidate_set"]["candidates"]],
                [f"{item['type_id']}-s{number:03d}" for number in range(1, len(item["candidate_set"]["candidates"]) + 1)],
            )

    def test_fingerprints_ili_rights_and_nonmerge_relations(self):
        candidates = [
            (item, candidate)
            for item in self.inventory["types"]
            for candidate in item["candidate_set"]["candidates"]
        ]
        self.assertEqual(len(candidates), 67)
        for item, candidate in candidates:
            link = candidate["source_links"][0]
            relations = sorted(candidate["source_relations"], key=lambda row: row["source_member_index"])
            projection = {
                "source_inventory_id": link["source_inventory_id"],
                "source_version": link["source_version"],
                "source_entry_id": link["source_entry_id"],
                "source_sense_id": link["source_sense_id"],
                "part_of_speech": item["part_of_speech"],
                "glosses": [candidate["definition"]["text"]],
                "examples": candidate["examples"]["items"],
                "usage_labels": candidate["usage_labels"],
                "source_synset_id": candidate["source_synset_id"],
                "cili_ili": candidate["cili"]["ili"],
                "synset_members": [relation["target_lemma"] for relation in relations],
            }
            self.assertEqual(link["source_record_sha256"], digest(projection))
            self.assertRegex(candidate["cili"]["ili"], r"^i\d+$")
            self.assertEqual(link["mapping_relation"], "candidate_only")
            self.assertEqual(link["verification_status"], "unreviewed")
            self.assertEqual(candidate["rights"]["redistribution_status"], "permitted")
            self.assertEqual(candidate["definition"]["origin"], "source_verbatim")
            self.assertTrue(all(
                relation["project_identity_action"] in {"same_source_entry", "related_not_merged"}
                for relation in relations
            ))

    def test_runtime_projection_matches_candidate_source_not_project_admission(self):
        runtime = json.loads((ROOT / "resources/oewn_take_in_2025.json").read_text(encoding="utf-8"))
        projection = runtime["projection"]
        item = next(item for item in self.inventory["types"]
                    if item["canonical_lemma"] == projection["lemma"])
        rows = {row["sense_id"]: row for row in projection["senses"]}
        candidates = item["candidate_set"]["candidates"]
        self.assertEqual(len(rows), len(projection["senses"]))
        self.assertEqual(len(rows), 17)
        self.assertEqual(set(rows), {
            candidate["source_links"][0]["source_sense_id"] for candidate in candidates
        })
        for candidate in candidates:
            self.assertEqual(len(candidate["source_links"]), 1)
            link = candidate["source_links"][0]
            with self.subTest(source_sense_id=link["source_sense_id"]):
                # Join by source identity, never array order or a proposed project ID.
                self.assertEqual(link["source_inventory_id"], runtime["resource"]["id"])
                self.assertEqual(link["source_version"], runtime["resource"]["release_tag"])
                self.assertEqual(link["source_artifact_sha256"], runtime["resource"]["artifact_sha256"])
                self.assertEqual(link["source_repository_commit"], runtime["resource"]["repository_commit"])
                self.assertEqual(link["source_entry_id"], projection["entry_id"])
                row = rows[link["source_sense_id"]]
                self.assertEqual(row["synset_id"], candidate["source_synset_id"])
                self.assertEqual(row["ili"], candidate["cili"]["ili"])
                self.assertEqual(row["definitions"], [candidate["definition"]["text"]])
                self.assertEqual(row["synset_examples"], candidate["examples"]["items"]["synset"])
                self.assertEqual(row["entry_examples"], candidate["examples"]["items"]["entry"])
                self.assertEqual(row["synonyms"], [relation["target_lemma"] for relation in sorted(
                    candidate["source_relations"], key=lambda relation: relation["source_member_index"]
                )])
                self.assertNotIn(candidate["reserved_project_sense_id"], rows)
                self.assertEqual(candidate["reservation_state"], "reserved_candidate_not_admitted")
                self.assertEqual(link["verification_status"], "unreviewed")
        self.assertEqual(item["senses"], [], "Consistent source copies do not admit project senses")

    def test_dependencies_anchor_and_generator(self):
        for dependency in self.inventory["dependencies"].values():
            path = ROOT / dependency["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), dependency["sha256"])
        rows = []
        for item in self.inventory["types"]:
            rows.append(f"{item['type_id']}\t{item['canonical_lemma']}")
            for candidate in item["candidate_set"]["candidates"]:
                rows.append("\t".join((
                    candidate["reserved_project_sense_id"],
                    candidate["source_links"][0]["source_sense_id"],
                )))
        self.assertEqual(
            hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest(),
            self.inventory["id_registry"]["stability_anchor_sha256"],
        )
        result = subprocess.run(
            ["python3", str(SCRIPT_PATH), "--self-check"], cwd=ROOT,
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Hybrid sense inventory self-check: PASS\n")

    def test_independent_review_kit_is_complete_and_collects_no_identity(self):
        protocol = json.loads(REVIEW_PROTOCOL_PATH.read_text(encoding="utf-8"))
        self.assertEqual(protocol["protocol_version"], "1.2.0")
        self.assertEqual(protocol["status"], "usage_pilot_manifest_complete_judgments_and_review_not_started")
        self.assertEqual(
            hashlib.sha256(INVENTORY_PATH.read_bytes()).hexdigest(),
            protocol["scope"]["inventory_sha256"],
        )
        self.assertEqual(protocol["scope"]["expected_forms"], 9)
        self.assertEqual(protocol["scope"]["expected_candidates"], 67)
        audit = protocol["polysemy_pre_review_audit"]["quantitative"]
        self.assertEqual(audit["candidate_pairs_if_exhaustive"], 387)
        self.assertEqual(audit["by_family"]["VPC"], {"forms": 4, "candidates": 56, "candidate_pairs": 377})
        self.assertEqual(audit["by_family"]["VID"], {"forms": 5, "candidates": 11, "candidate_pairs": 10})
        self.assertEqual(audit["source_evidence"]["candidates_without_examples"], 5)
        self.assertEqual(audit["design_state"]["contextual_occurrences_in_inventory"], 0)
        result = subprocess.run(
            ["python3", str(REVIEW_SCRIPT_PATH), "--self-check"], cwd=ROOT,
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["self_check"], "pass")
        premature_template = subprocess.run(
            ["python3", str(REVIEW_SCRIPT_PATH), "--template"], cwd=ROOT,
            capture_output=True, text=True,
        )
        self.assertEqual(premature_template.returncode, 2)
        self.assertIn("Usage-pilot judgments and clusters are not frozen", premature_template.stderr)
        public_files = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.splitlines()
        self.assertFalse(any(
            path.startswith("annotations/inventory_review_raw/") for path in public_files
        ))

    def test_unverified_cluster_claims_cannot_start_either_review_command(self):
        spec = importlib.util.spec_from_file_location("inventory_reviews", REVIEW_SCRIPT_PATH)
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        protocol, inventory = checker.load_inputs(REVIEW_PROTOCOL_PATH)
        template = checker.make_template(REVIEW_PROTOCOL_PATH, protocol, inventory)
        # Even an existing file with its correct hash is not an approved cluster artifact.
        claims = [
            (None, None),
            ("synthetic:not-a-file", "not-a-sha256"),
            ("synthetic:not-a-file", "0" * 64),
            (protocol["scope"]["inventory_path"], "0" * 64),
            (protocol["scope"]["inventory_path"], protocol["scope"]["inventory_sha256"]),
        ]
        for path, checksum in claims:
            probe = copy.deepcopy(protocol)
            probe["usage_pilot"]["cluster_artifact"].update(
                status="frozen", path=path, sha256=checksum,
            )
            for args in (["--template"], ["synthetic-review-a.json", "synthetic-review-b.json"]):
                with self.subTest(path=path, checksum=checksum, args=args), \
                        patch.object(checker, "load_inputs", return_value=(probe, inventory)), \
                        patch.object(checker, "make_template", return_value=template), \
                        patch.object(Path, "read_text", side_effect=AssertionError("Unexpected file read")), \
                        patch.object(Path, "read_bytes", side_effect=AssertionError("Unexpected file read")), \
                        patch("sys.argv", [str(REVIEW_SCRIPT_PATH), *args]), \
                        patch("sys.stdout", new_callable=io.StringIO) as stdout, \
                        patch("sys.stderr", new_callable=io.StringIO) as stderr:
                    with self.assertRaises(SystemExit) as stopped:
                        checker.main()
                    self.assertEqual(stopped.exception.code, 2)
                    self.assertEqual(stdout.getvalue(), "")
                    self.assertIn("expert review cannot start", stderr.getvalue())

    def test_lifecycle_exercise_is_non_destructive_and_prospective(self):
        fixture = json.loads(LIFECYCLE_FIXTURE_PATH.read_text(encoding="utf-8"))
        old = fixture["old_inventory"]
        new = fixture["new_inventory"]
        annotations = fixture["old_annotations"]
        self.assertEqual(fixture["hashes"], {
            "old_inventory_sha256": digest(old),
            "new_inventory_sha256": digest(new),
            "old_annotations_sha256": digest(annotations),
        })
        old_senses = {item["sense_id"]: item for item in old["senses"]}
        new_senses = {item["sense_id"]: item for item in new["senses"]}
        self.assertTrue(set(old_senses).issubset(new_senses))
        self.assertEqual(new["version"], "2.0.0")

        split_children = [item for item in new_senses.values()
                          if "ldfreq-en-vmwe-t900001-s001" in item["identity_relations"]["split_from"]]
        self.assertEqual(len(split_children), 2)
        self.assertEqual(new_senses["ldfreq-en-vmwe-t900001-s001"]["lifecycle_status"], "deprecated")
        merged = new_senses["ldfreq-en-vmwe-t900001-s007"]
        self.assertEqual(set(merged["identity_relations"]["merged_from"]), {
            "ldfreq-en-vmwe-t900001-s002", "ldfreq-en-vmwe-t900001-s003",
        })
        self.assertTrue(all(new_senses[sense_id]["lifecycle_status"] == "deprecated"
                            for sense_id in merged["identity_relations"]["merged_from"]))

        retained_links = new_senses["ldfreq-en-vmwe-t900001-s004"]["source_links"]
        self.assertEqual([link["link_status"] for link in retained_links], ["deprecated", "active"])
        self.assertEqual(fixture["events"][2]["project_identity_action"], "retained")

        migrations = {item["annotation_id"]: item for item in fixture["migration_records"]}
        self.assertEqual(set(migrations), {item["annotation_id"] for item in annotations})
        self.assertTrue(all(not item["automatic_rewrite_applied"] for item in migrations.values()))
        ooi = next(item for item in annotations if item["decision_status"] == "out_of_inventory")
        self.assertEqual(ooi["sense_ids"], [])
        self.assertEqual(migrations[ooi["annotation_id"]]["migration_status"],
                         "review_required_new_inventory_sense")
        self.assertIn("ldfreq-en-vmwe-t900001-s008", new_senses)

        approval = fixture["approval_fixture"]
        self.assertEqual(approval["evidence_partition"], "training_only_synthetic")
        self.assertFalse(approval["sealed_test_examined"])
        self.assertFalse(approval["performance_metrics_examined"])
        self.assertTrue(approval["proposal_recorded_before_change"])
        self.assertEqual(set(approval["required_approval_roles"]), {"lexicographer", "PI"})


class InventoryPopulationLogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = json.loads(POPULATION_LOG_PATH.read_text(encoding="utf-8"))

    def test_balanced_batch_and_fail_closed_states(self):
        self.assertEqual(self.log["summary"]["pilot_types"], 14)
        self.assertEqual(
            self.log["summary"]["mapping_route_counts"],
            {
                "exact_kaikki": 4,
                "exact_oewn": 4,
                "no_bounded_route": 2,
                "nonexact_candidate": 3,
                "unique_slot_oewn": 1,
            },
        )
        self.assertEqual(self.log["summary"]["types_without_bounded_route"], 2)
        self.assertEqual(self.log["summary"]["mapping_unresolved_rate"], 0.142857)
        self.assertTrue(self.log["summary"]["eligibility_state_recorded_for_every_type"])
        self.assertFalse(self.log["selection_contract"]["uses_dev_or_test_type_statistics"])
        self.assertEqual(
            [row["type_id"] for row in self.log["pilot_batch"] if row["type_id_source"] == "ir132_append_only_reservation"],
            [f"ldfreq-en-vmwe-t{number:06d}" for number in range(151, 160)],
        )
        self.assertTrue(all(row["literal_contrast_state"].startswith("future_") for row in self.log["pilot_batch"]))

    def test_source_levels_and_no_lexical_or_corpus_text(self):
        rows = self.log["pilot_batch"]
        jump_start = next(row for row in rows if row["canonical_lemma"] == "jump - start")
        self.assertEqual(jump_start["candidate_sources"], ["enwiktionary-kaikki", "oewn"])
        waste_time = next(row for row in rows if row["canonical_lemma"] == "waste time")
        self.assertEqual(waste_time["source_entry_lemma"], "waste one's time")
        self.assertEqual(
            waste_time["fixed_slot_state"],
            "source_candidate_differs_by_frozen_closed_class_slot",
        )
        prohibited = {"text", "sentence", "tokens", "gloss", "glosses", "example", "examples", "body"}

        def keys(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    yield key
                    yield from keys(child)
            elif isinstance(value, list):
                for child in value:
                    yield from keys(child)

        self.assertFalse(prohibited.intersection(keys(self.log)))

    def test_dependencies_and_generator(self):
        for dependency in self.log["dependencies"].values():
            path = ROOT / dependency["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), dependency["sha256"])
        result = subprocess.run(
            ["python3", str(POPULATION_SCRIPT_PATH), "--self-check"], cwd=ROOT,
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Inventory population log self-check: PASS\n")


if __name__ == "__main__":
    unittest.main()
