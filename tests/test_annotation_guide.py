import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).parents[1]


class AnnotationGuideTests(unittest.TestCase):
    def test_guide_covers_contract_states_and_training_fixtures(self):
        guide = (ROOT / "ANNOTATION_GUIDE.md").read_text(encoding="utf-8")
        contract = json.loads((ROOT / "mwe_contract.json").read_text(encoding="utf-8"))
        occurrence = contract["occurrence_record"]

        for states in (
            occurrence["statuses"],
            occurrence["categories"],
            occurrence["idiomaticity_statuses"],
            occurrence["form_lookup_statuses"],
            occurrence["sense_lookup_statuses"],
            occurrence["sense_assignment_statuses"],
        ):
            for state in states:
                self.assertIn(f"`{state}`", guide)

        for section in (
            "Candidate-independent search",
            "Occurrence status",
            "Member and gap spans",
            "Category",
            "Idiomaticity",
            "Form and sense inventory",
            "Contextual sense",
            "Uncertainty states",
        ):
            self.assertIn(f"## {section}", guide)

        for kind in ("Positive", "Negative", "Borderline"):
            self.assertGreaterEqual(guide.count(f"| {kind}"), 8)

        fixtures = json.loads(
            (ROOT / "tests/fixtures/mwe_cases.json").read_text(encoding="utf-8")
        )
        for case in fixtures["cases"]:
            self.assertIn(f"`{case['id']}`", guide)

        self.assertIn(
            "Status: standalone occurrence, span, category, idiomaticity, and contextual-sense modules complete",
            guide,
        )
        self.assertIn("Do not administer this guide to annotators yet", guide)

    def test_ir141_training_cases_have_reproducible_spans_and_diagnostics(self):
        from scripts.reconstruct_benchmark import token_records

        guide = (ROOT / "ANNOTATION_GUIDE.md").read_text(encoding="utf-8")
        training = json.loads(
            (ROOT / "annotations/training_cases.json").read_text(encoding="utf-8")
        )
        contract = json.loads((ROOT / "mwe_contract.json").read_text(encoding="utf-8"))
        codes = {item["code"]: item["level"] for item in training["disagreement_codes"]}
        used_codes = set()
        features = set()
        statuses = set()
        categories = set()

        self.assertEqual(training["task"], "IR-141")
        self.assertEqual(training["guide_version"], "0.5.0-contextual-sense")
        self.assertEqual(training["contract_version"], contract["contract_version"])
        self.assertFalse(training["provenance"]["human_response_data"])
        self.assertFalse(training["provenance"]["natural_benchmark_items"])

        for case in training["cases"]:
            expected_surfaces = [token["surface"] for token in case["tokens"]]
            actual_surfaces = [
                token["surface"] for token in token_records(case["text"], "training")
            ]
            self.assertEqual(actual_surfaces, expected_surfaces, case["id"])
            token_ids = [token["id"] for token in case["tokens"]]
            features.update(case["features"])

            for decision in case["decisions"]:
                members = decision["member_token_ids"]
                member_positions = [token_ids.index(token_id) for token_id in members]
                self.assertGreaterEqual(len(set(members)), 2, case["id"])
                self.assertEqual(member_positions, sorted(member_positions), case["id"])
                expected_gaps = [
                    token_ids[position]
                    for position in range(min(member_positions), max(member_positions) + 1)
                    if token_ids[position] not in members
                ]
                self.assertEqual(decision["gap_token_ids"], expected_gaps, case["id"])
                statuses.add(decision["status"])
                categories.add(decision["category"])
                used_codes.update(decision.get("diagnostic_codes", []))

            used_codes.update(case.get("exclusion", {}).get("diagnostic_codes", []))

        self.assertTrue({
            "inflection",
            "particle_movement",
            "pronoun_gap",
            "nested_overlap",
            "literal_particle",
            "accidental_sequence",
            "tokenization_exception",
            "continuous",
            "discontinuous",
        }.issubset(features))
        self.assertEqual(statuses, set(contract["occurrence_record"]["statuses"]))
        self.assertEqual(categories, set(contract["occurrence_record"]["categories"]))
        self.assertEqual(set(codes) - {"unclassified"}, used_codes)
        self.assertEqual(
            {code for code, level in codes.items() if level == "span"},
            {code for code in used_codes if codes[code] == "span"},
        )
        for code in codes:
            self.assertIn(f"`{code}`", guide)

    def test_idiomaticity_is_separate_and_magpie_projection_is_loss_aware(self):
        guide = (ROOT / "ANNOTATION_GUIDE.md").read_text(encoding="utf-8")
        contract = json.loads((ROOT / "mwe_contract.json").read_text(encoding="utf-8"))
        occurrence = contract["occurrence_record"]

        self.assertIn("category", occurrence["required_fields"])
        self.assertIn("idiomaticity", occurrence["required_fields"])
        self.assertEqual(
            set(occurrence["idiomaticity_statuses"]),
            {"idiomatic", "literal", "ambiguous", "not_assessed"},
        )
        for marker in (
            "`figurative_but_compositional:`",
            "`open-text-first-pass`",
            "`candidate-list-assisted`",
            "Loss-aware MAGPIE comparison projection",
            "false extraction (`f`)",
            "Never pool `open-text-first-pass` records",
        ):
            self.assertIn(marker, guide)

        fixtures = json.loads(
            (ROOT / "tests/fixtures/mwe_cases.json").read_text(encoding="utf-8")
        )
        contrast = next(
            case
            for case in fixtures["cases"]
            if case["id"] == "M5-idiomatic-versus-literal-vid"
        )
        self.assertEqual(
            {item["category"] for item in contrast["occurrences"]}, {"VID"}
        )
        self.assertEqual(
            {item["idiomaticity"]["status"] for item in contrast["occurrences"]},
            {"idiomatic", "literal"},
        )

    def test_hard_case_bank_is_synthetic_redistributable_and_stratified(self):
        bank = json.loads(
            (ROOT / "annotations/hard_case_bank.json").read_text(encoding="utf-8")
        )
        contract = json.loads((ROOT / "mwe_contract.json").read_text(encoding="utf-8"))
        occurrence = contract["occurrence_record"]
        strata = {item["id"]: item["minimum_cases"] for item in bank["prespecified_strata"]}
        counts = {stratum: 0 for stratum in strata}

        self.assertEqual(bank["guide_version"], "0.5.0-contextual-sense")
        self.assertEqual(bank["contract_version"], contract["contract_version"])
        self.assertTrue(bank["rights"]["redistribution_permitted"])
        self.assertFalse(bank["rights"]["third_party_text_reproduced"])
        self.assertEqual(len({case["id"] for case in bank["cases"]}), len(bank["cases"]))

        for case in bank["cases"]:
            self.assertEqual(case["source"]["kind"], "project_authored_synthetic")
            self.assertTrue(case["source"]["redistribution_permitted"])
            self.assertTrue(case["decision_rationale"].strip())
            self.assertNotIn("gold", case)
            for stratum in case["strata"]:
                self.assertIn(stratum, strata)
                counts[stratum] += 1
            for route in case["candidate_routes"]:
                self.assertTrue(set(route["permitted_statuses"]) <= set(occurrence["statuses"]))
                self.assertTrue(set(route["permitted_categories"]) <= set(occurrence["categories"]))
                self.assertTrue(
                    set(route["idiomaticity_statuses"])
                    <= set(occurrence["idiomaticity_statuses"])
                )

        for stratum, minimum in strata.items():
            self.assertGreaterEqual(counts[stratum], minimum, stratum)

    def test_training_program_has_separate_gates_and_retraining(self):
        protocol = (ROOT / "ANNOTATOR_TRAINING.md").read_text(encoding="utf-8")
        training = json.loads(
            (ROOT / "annotations/training_cases.json").read_text(encoding="utf-8")
        )
        program = training["training_program"]

        self.assertEqual(training["schema_version"], "1.1.0")
        self.assertFalse(program["human_use_authorized"])
        self.assertFalse(program["benchmark_material_permitted"])
        self.assertEqual(program["combined_score"], "forbidden")
        self.assertEqual(
            program["stages"],
            [
                "teach_back",
                "guided_practice",
                "feedback",
                "hard_case_practice",
                "qualification",
            ],
        )
        self.assertEqual(
            {gate["task"] for gate in program["task_gates"]},
            {
                "occurrence",
                "member_and_gap_span",
                "category",
                "idiomaticity",
                "contextual_sense",
            },
        )
        for gate in program["task_gates"]:
            self.assertGreaterEqual(gate["minimum_scored_items"], 12)
            self.assertLessEqual(sum(gate["composition_minimums"].values()), gate["minimum_scored_items"])
            for threshold in gate["thresholds"].values():
                self.assertGreater(threshold, 0)
                self.assertLessEqual(threshold, 1)

        form = program["qualification_form"]
        self.assertEqual(form["state"], "not_materialized_pending_human_use_authorization")
        self.assertIn("synthetic", form["source_requirement"])
        self.assertTrue(form["public_repository_form_counts_as_exposed"])
        retraining = program["retraining"]
        self.assertEqual(retraining["maximum_qualification_attempts_per_task_and_guide_version"], 2)
        self.assertFalse(retraining["cross_task_compensation"])

        for marker in (
            "## Stages",
            "## Task-specific gates",
            "## Retraining and retry",
            "No qualification form is currently materialized",
            "do not calculate a total qualification score",
        ):
            self.assertIn(marker, protocol)

    def test_inception_converter_preserves_required_dry_run_states(self):
        from scripts.convert_annotation_export import self_test

        contract = json.loads((ROOT / "mwe_contract.json").read_text(encoding="utf-8"))
        result = self_test(contract)
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["synthetic_only"])
        for field in (
            "discontinuous_gap_preserved",
            "multiple_senses_preserved",
            "out_of_inventory_preserved",
            "audit_event_preserved",
        ):
            self.assertTrue(result[field])

    def test_unconfirmed_conversion_preserves_states_at_evaluation_boundary(self):
        from scripts.convert_annotation_export import _synthetic_cas, convert
        from scripts.evaluate_mwe_predictions import evaluate

        contract = json.loads((ROOT / "mwe_contract.json").read_text(encoding="utf-8"))
        metric_contract = json.loads((ROOT / "metric_contract.json").read_text(encoding="utf-8"))
        for status, idiom in [("candidate", "not_assessed")] + [
            ("rejected", value) for value in contract["occurrence_record"]["idiomaticity_statuses"]
        ]:
            with self.subTest(status=status, idiom=idiom):
                document = _synthetic_cas()
                item = next(row for row in document["%FEATURE_STRUCTURES"] if row["%ID"] == 60)
                item.update(
                    status=status, decisionNote=None if status == "candidate" else "Synthetic rejection.",
                    idiomaticityStatus=idiom,
                    idiomaticityNote=None if idiom == "not_assessed" else "Synthetic idiomaticity note.",
                    formLookupStatus="not_attempted", formInventoryId=None,
                    formInventoryVersion=None, formEntryId=None, formSenseCount=None,
                    senseLookupStatus="not_attempted", senseInventoryId=None,
                    senseInventoryVersion=None, senseAssignmentStatus="unassigned",
                    candidateSenseIdsJson="[]", selectedSenseIdsJson="[]", senseDecisionNote=None,
                )
                converted = convert(document, json.dumps(document).encode(), contract, "SYN-A",
                                    "2026-09-06T00:00:00Z", "synthetic.json", "41.5-format-target")
                occurrences = converted["document"]["occurrences"]
                first = occurrences[0]
                self.assertEqual(first["status"], status)
                self.assertEqual(first["idiomaticity"]["status"], idiom)
                self.assertIsNone(first["form_lookup"])
                self.assertIsNone(first["sense"])
                self.assertEqual(first["gap_token_ids"], ["t3", "t4"])
                self.assertEqual((first["idiomaticity"]["decision"] or {}).get("note"),
                                 item["idiomaticityNote"])
                gold = {"contract_version": contract["contract_version"], "cases": [{
                    "id": "synthetic", "occurrences": occurrences,
                    "tokens": [{"id": f"t{position}", "position": position}
                               for position in range(1, converted["document"]["token_count"] + 1)],
                }]}
                predicted = []
                for occurrence in occurrences:
                    sense = occurrence["sense"] or {}
                    predicted.append({
                        **{key: occurrence[key] for key in (
                            "id", "status", "category", "member_token_ids", "gap_token_ids")},
                        "head_token_id": occurrence["member_token_ids"][0],
                        "idiomaticity_status": occurrence["idiomaticity"]["status"],
                        "sense_assignment_status": sense.get("assignment_status", "unassigned"),
                        "selected_sense_ids": sense.get("selected_sense_ids", []),
                    })
                predictions = {
                    "contract_version": contract["contract_version"], "evaluation_mode": "open_text",
                    "metric_contract_version": metric_contract["benchmark_mwe_evaluation"]["contract_version"],
                    "system": {"name": "synthetic-format-check"},
                    "cases": [{"id": "synthetic", "occurrences": predicted}],
                }
                if status == "candidate":
                    with self.assertRaisesRegex(ValueError, "unresolved candidate: synthetic/dry-o1"):
                        evaluate(gold, predictions, contract, metric_contract)
                    self.assertEqual(first["status"], "candidate")
                    item.update(idiomaticityStatus="literal", idiomaticityNote="Synthetic note.")
                    with self.assertRaisesRegex(ValueError, "unresolved candidates"):
                        convert(document, json.dumps(document).encode(), contract, "SYN-A",
                                "2026-09-06T00:00:00Z", "synthetic.json", "41.5-format-target")
                    continue
                result = evaluate(gold, predictions, contract, metric_contract)
                assessed = 1 if idiom == "not_assessed" else 2
                self.assertEqual(result["idiomaticity"]["accuracy_among_predictions"],
                                 {"numerator": assessed, "denominator": assessed, "value": 1.0})
                self.assertEqual(result["span"]["exact"]["recall"]["denominator"], 1)
                self.assertIsNone(result["sense"]["exact_set_accuracy"]["value"])

    def test_converter_binds_parsed_content_to_the_raw_export_hash(self):
        from scripts.convert_annotation_export import _synthetic_cas, convert

        contract = json.loads((ROOT / "mwe_contract.json").read_text(encoding="utf-8"))
        document = _synthetic_cas()
        note = next(row for row in document["%FEATURE_STRUCTURES"] if row["%ID"] == 60)
        note["decisionNote"] = "Synthetic café note."
        records = []
        for options in ({"ensure_ascii": False, "separators": (",", ":")},
                        {"ensure_ascii": True, "sort_keys": True, "indent": 2}):
            source_bytes = json.dumps(document, **options).encode("utf-8")
            converted = convert(document, source_bytes, contract, "SYN-A",
                                "2026-09-06T00:00:00Z", "synthetic.json", "41.5-format-target")
            self.assertEqual(converted["audit_event"]["source_sha256"],
                             hashlib.sha256(source_bytes).hexdigest())
            records.append(converted)
        self.assertEqual(records[0]["document"], records[1]["document"])
        self.assertNotEqual(records[0]["audit_event"]["source_sha256"],
                            records[1]["audit_event"]["source_sha256"])
        self.assertEqual(records[0]["document"]["occurrences"][0]["decision"]["note"],
                         note["decisionNote"])
        for change in ("note", "version", "boolean_id"):
            with self.subTest(change=change):
                changed = copy.deepcopy(document)
                if change == "note":
                    next(row for row in changed["%FEATURE_STRUCTURES"] if row["%ID"] == 60)["decisionNote"] = "Changed."
                elif change == "version":
                    changed["%HEADER"]["%VERSION"] = "different-version"
                else:
                    changed["%FEATURE_STRUCTURES"][0]["%ID"] = True
                    self.assertEqual(changed, document)  # Python equality alone conflates 1 and True.
                with self.assertRaisesRegex(ValueError, "source_bytes"):
                    convert(changed, source_bytes, contract, "SYN-A", "2026-09-06T00:00:00Z",
                            "synthetic.json", "41.5-format-target")
        for invalid_bytes in (b"not JSON", b"\xff", b"null", b"{}"):
            with self.subTest(source=invalid_bytes):
                with self.assertRaises(ValueError):
                    convert(document, invalid_bytes, contract, "SYN-A", "2026-09-06T00:00:00Z",
                            "synthetic.json", "41.5-format-target")

    def test_converter_cli_preserves_input_and_existing_outputs(self):
        from scripts.convert_annotation_export import _synthetic_cas

        source_bytes = json.dumps(_synthetic_cas()).encode("utf-8")
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "raw.json"
            output = Path(directory) / "converted.json"
            source.write_bytes(source_bytes)
            command = [sys.executable, str(ROOT / "scripts/convert_annotation_export.py"),
                       str(source)]
            options = ["--annotator-id", "SYN-A", "--converted-at", "2026-09-06T00:00:00Z"]
            result = subprocess.run(command + [str(output)] + options, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            converted_bytes = output.read_bytes()
            self.assertEqual(json.loads(converted_bytes)["audit_event"]["source_sha256"],
                             hashlib.sha256(source_bytes).hexdigest())
            self.assertEqual(source.read_bytes(), source_bytes)

            hardlink = Path(directory) / "hardlink.json"
            hardlink.hardlink_to(source)
            symlink = Path(directory) / "symlink.json"
            symlink.symlink_to(source)
            missing = Path(directory) / "missing.json"
            dangling = Path(directory) / "dangling.json"
            dangling.symlink_to(missing)
            for target in (output, source, hardlink, symlink, dangling):
                with self.subTest(target=target.name):
                    source.write_bytes(source_bytes)
                    result = subprocess.run(command + [str(target)] + options, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("Output already exists", result.stderr)
                    self.assertEqual(source.read_bytes(), source_bytes)
                    self.assertEqual(output.read_bytes(), converted_bytes)
                    self.assertTrue(symlink.is_symlink())
                    self.assertTrue(dangling.is_symlink())
                    self.assertFalse(missing.exists())

            source.write_bytes(b"{}")
            invalid_output = Path(directory) / "invalid-converted.json"
            result = subprocess.run(command + [str(invalid_output)] + options, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(invalid_output.exists())

    def test_converter_rejects_inconsistent_lookup_states_and_blank_notes(self):
        from scripts.convert_annotation_export import _synthetic_cas, convert

        contract = json.loads((ROOT / "mwe_contract.json").read_text(encoding="utf-8"))
        changes = [
            (60, {"status": "rejected"}),
            (61, {"senseAssignmentStatus": "unassigned", "senseDecisionNote": None}),
            (61, {"senseAssignmentStatus": "unassigned", "senseDecisionNote": None,
                  "senseLookupStatus": "inventory_ineligible", "senseInventoryId": None,
                  "senseInventoryVersion": None}),
        ] + [(60, {field: " \t "}) for field in ("decisionNote", "idiomaticityNote", "senseDecisionNote")]
        for identifier, fields in changes:
            with self.subTest(fields=fields):
                document = _synthetic_cas()
                item = next(row for row in document["%FEATURE_STRUCTURES"] if row["%ID"] == identifier)
                item.update(fields)
                with self.assertRaises(ValueError):
                    convert(document, json.dumps(document).encode(), contract, "SYN-A",
                            "2026-09-06T00:00:00Z", "synthetic.json", "41.5-format-target")


if __name__ == "__main__":
    unittest.main()
