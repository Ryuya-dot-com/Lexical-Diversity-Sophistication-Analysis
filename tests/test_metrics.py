import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate_mwe_predictions import evaluate


CONTRACT = json.loads((ROOT / "mwe_contract.json").read_text(encoding="utf-8"))
METRIC_CONTRACT = json.loads((ROOT / "metric_contract.json").read_text(encoding="utf-8"))


def occurrence(identifier, members, category, status, idiom, sense):
    return {
        "id": identifier,
        "canonical_form": identifier,
        "category": category,
        "status": status,
        "member_token_ids": members,
        "gap_token_ids": ["t5"] if members == ["t4", "t6"] else [],
        "decision": {"source": "synthetic-test", "note": "synthetic"},
        "idiomaticity": {"status": idiom, "decision": None},
        "form_lookup": None,
        "sense": sense,
    }


GOLD = {
    "contract_version": CONTRACT["contract_version"],
    "cases": [{
        "id": "d1",
        "text": "synthetic",
        "tokens": [
            {"id": f"t{position}", "position": position, "surface": "x", "normalized": "x"}
            for position in range(1, 7)
        ],
        "occurrences": [
            occurrence("g1", ["t1", "t2"], "VPC.full", "confirmed", "idiomatic", {
                "lookup_status": "matched",
                "assignment_status": "assigned",
                "selected_sense_ids": ["s1"],
            }),
            occurrence("g2", ["t4", "t6"], "VID", "confirmed", "ambiguous", {
                "lookup_status": "matched",
                "assignment_status": "multiple_assigned",
                "selected_sense_ids": ["s2", "s3"],
            }),
            occurrence("g3", ["t3", "t4"], "VPC.semi", "rejected", "literal", None),
        ],
    }],
}


def prediction(identifier, head, members, category, status, idiom, sense_status,
               senses, probability, confidence):
    return {
        "id": identifier,
        "head_token_id": head,
        "member_token_ids": members,
        "gap_token_ids": ["t5"] if members == ["t4", "t6"] else [],
        "category": category,
        "status": status,
        "idiomaticity_status": idiom,
        "sense_assignment_status": sense_status,
        "selected_sense_ids": senses,
        "confirmed_probability": probability,
        "decision_confidence": confidence,
    }


PREDICTIONS = {
    "contract_version": CONTRACT["contract_version"],
    "metric_contract_version": METRIC_CONTRACT["benchmark_mwe_evaluation"]["contract_version"],
    "evaluation_mode": "open_text",
    "system": {"name": "synthetic", "probabilistic": True, "selective": True},
    "cases": [{
        "id": "d1",
        "occurrences": [
            prediction("p1", "t1", ["t1", "t2"], "VPC.full", "confirmed",
                       "idiomatic", "assigned", ["s1"], 0.9, 0.9),
            prediction("p2", "t4", ["t4", "t6"], "VPC.full", "confirmed",
                       "not_assessed", "abstained", [], 0.6, 0.6),
            prediction("p3", "t3", ["t3", "t4"], "VPC.semi", "confirmed",
                       "literal", "unassigned", [], 0.4, 0.7),
            prediction("p4", "t2", ["t2", "t3"], "VPC.semi", "candidate",
                       "not_assessed", "unassigned", [], 0.2, 0.2),
        ],
    }],
}


class OpenTextMetricTests(unittest.TestCase):
    def test_task_metrics_remain_separate_and_conditional(self):
        result = evaluate(GOLD, PREDICTIONS, CONTRACT)

        self.assertEqual(result["candidate"]["recall"], {"numerator": 2, "denominator": 2, "value": 1.0})
        self.assertEqual(result["span"]["exact"]["f1"]["value"], 0.8)
        self.assertEqual(result["span"]["member_token"]["f1"]["value"], 0.888889)
        self.assertEqual(result["span"]["gap_set_accuracy"]["value"], 1.0)
        self.assertEqual(result["category"]["macro_f1"]["value"], 0.222222)
        self.assertEqual(result["idiomaticity"]["prediction_coverage"]["value"], 0.666667)
        self.assertEqual(result["idiomaticity"]["accuracy_among_predictions"]["value"], 1.0)
        self.assertEqual(result["inventory"]["occurrence_sense_inventory_coverage"]["value"], 1.0)
        self.assertEqual(result["inventory"]["canonical_form_sense_inventory_coverage"]["value"], 1.0)
        self.assertEqual(result["sense"]["exact_set_accuracy"]["value"], 0.5)
        self.assertEqual(result["sense"]["assignment_state_accuracy"]["value"], 0.5)
        self.assertEqual(result["sense"]["micro"]["f1"]["value"], 0.5)
        self.assertEqual(result["sense"]["gold_multiple_assignment_rate"]["value"], 0.5)
        self.assertEqual(result["sense"]["model_abstention_rate"]["value"], 0.5)
        self.assertEqual(result["calibration"]["brier"]["value"], 0.0925)
        self.assertEqual(result["calibration"]["ece"]["value"], 0.275)
        self.assertEqual(result["selective_prediction"]["decision_coverage"]["value"], 0.75)
        self.assertEqual(result["selective_prediction"]["aurc_over_ranked_decisions"]["value"], 0.277778)
        self.assertEqual(result["combined_score"]["state"], "forbidden")

        same_set_wrong_state = copy.deepcopy(PREDICTIONS)
        same_set_wrong_state["cases"][0]["occurrences"][1].update({
            "sense_assignment_status": "ambiguous",
            "selected_sense_ids": ["s2", "s3"],
        })
        separated = evaluate(GOLD, same_set_wrong_state, CONTRACT)
        self.assertEqual(separated["sense"]["exact_set_accuracy"]["value"], 1.0)
        self.assertEqual(separated["sense"]["assignment_state_accuracy"]["value"], 0.5)

        nonprobabilistic = copy.deepcopy(PREDICTIONS)
        nonprobabilistic["system"] = {"name": "synthetic", "probabilistic": False, "selective": False}
        for item in nonprobabilistic["cases"][0]["occurrences"]:
            item.pop("confirmed_probability")
            item.pop("decision_confidence")
        conditional = evaluate(GOLD, nonprobabilistic, CONTRACT)
        self.assertEqual(conditional["calibration"]["state"], "not_applicable_nonprobabilistic_system")
        self.assertEqual(conditional["selective_prediction"]["state"], "not_applicable_nonselective_system")

    def test_rejected_literal_keeps_idiomaticity_without_admitting_senses(self):
        predictions = copy.deepcopy(PREDICTIONS)
        item = predictions["cases"][0]["occurrences"][2]
        item["status"] = "rejected"
        result = evaluate(GOLD, predictions, CONTRACT)
        self.assertEqual(result["span"]["exact"]["precision"]["value"], 1.0)
        self.assertEqual(result["idiomaticity"]["prediction_coverage"],
                         {"numerator": 2, "denominator": 3, "value": 0.666667})
        self.assertEqual(result["idiomaticity"]["accuracy_among_predictions"]["value"], 1.0)
        self.assertEqual(result["sense"], evaluate(GOLD, PREDICTIONS, CONTRACT)["sense"])

        for idiomaticity in CONTRACT["occurrence_record"]["idiomaticity_statuses"]:
            item["status"] = "rejected"
            item["idiomaticity_status"] = idiomaticity
            evaluate(GOLD, predictions, CONTRACT)
            item["status"] = "candidate"
            if idiomaticity == "not_assessed":
                evaluate(GOLD, predictions, CONTRACT)
            else:
                with self.assertRaisesRegex(ValueError, "Unresolved prediction carries idiomaticity"):
                    evaluate(GOLD, predictions, CONTRACT)

        item["idiomaticity_status"] = "not_assessed"
        for status in ("candidate", "rejected"):
            item["status"] = status
            for sense_status, senses in (
                ("assigned", ["s1"]), ("multiple_assigned", ["s1", "s2"]),
                ("ambiguous", ["s1", "s2"]), ("abstained", []),
                ("out_of_inventory", []), ("inventory_ineligible", []),
            ):
                item.update(sense_assignment_status=sense_status, selected_sense_ids=senses)
                with self.assertRaisesRegex(ValueError, "Non-confirmed prediction carries"):
                    evaluate(GOLD, predictions, CONTRACT)

    def test_unresolved_gold_is_not_scored_as_a_negative_open_text_example(self):
        gold = copy.deepcopy(GOLD)
        item = gold["cases"][0]["occurrences"][2]
        item.update(status="candidate", decision=None, sense=None)
        item["idiomaticity"] = {"status": "not_assessed", "decision": None}
        original = copy.deepcopy(gold)
        for probabilistic in (True, False):
            for status in ("confirmed", "rejected", "candidate", None):
                with self.subTest(probabilistic=probabilistic, prediction=status):
                    predictions = copy.deepcopy(PREDICTIONS)
                    predictions["system"].update(probabilistic=probabilistic, selective=probabilistic)
                    predictions["cases"][0]["occurrences"] = predictions["cases"][0]["occurrences"][2:3]
                    if status is None:
                        predictions["cases"][0]["occurrences"] = []
                    else:
                        predictions["cases"][0]["occurrences"][0].update(
                            status=status, idiomaticity_status="not_assessed", confirmed_probability=0.0)
                    with self.assertRaisesRegex(ValueError, "unresolved candidate: d1/g3"):
                        evaluate(gold, predictions, CONTRACT)
        self.assertEqual(gold, original)

        provided = copy.deepcopy(PREDICTIONS)
        provided["evaluation_mode"] = "provided_candidates"
        provided["cases"][0]["occurrences"] = [
            dict(predicted, id=reference["id"])
            for reference, predicted in zip(gold["cases"][0]["occurrences"],
                                            provided["cases"][0]["occurrences"])
        ]
        result = evaluate(gold, provided, CONTRACT)
        self.assertEqual(result["candidate_count"], 3)
        self.assertEqual(result["occurrence_decision_accuracy"],
                         {"numerator": 2, "denominator": 2, "value": 1.0})
        with tempfile.TemporaryDirectory() as directory:
            gold_path = Path(directory) / "gold.json"
            prediction_path = Path(directory) / "predictions.json"
            gold_path.write_text(json.dumps(gold), encoding="utf-8")
            prediction_path.write_text(json.dumps(predictions), encoding="utf-8")
            process = subprocess.run([
                sys.executable, str(ROOT / "scripts/evaluate_mwe_predictions.py"),
                str(prediction_path), "--gold", str(gold_path),
            ], capture_output=True, text=True)
            self.assertEqual(process.returncode, 2)
            self.assertEqual(process.stdout, "")
            self.assertIn("unresolved candidate: d1/g3", process.stderr)

    def test_duplicate_gold_ids_cannot_silently_change_denominators(self):
        provided = copy.deepcopy(PREDICTIONS)
        provided["evaluation_mode"] = "provided_candidates"
        provided["cases"][0]["occurrences"] = [
            dict(predicted, id=reference["id"])
            for reference, predicted in zip(
                GOLD["cases"][0]["occurrences"], PREDICTIONS["cases"][0]["occurrences"]
            )
        ]
        for predictions in (provided, PREDICTIONS):
            evaluate(GOLD, predictions, CONTRACT)
            for level in ("document", "occurrence"):
                with self.subTest(mode=predictions["evaluation_mode"], level=level):
                    gold = copy.deepcopy(GOLD)
                    rows = gold["cases"] if level == "document" else gold["cases"][0]["occurrences"]
                    duplicate = copy.deepcopy(rows[0])
                    if level == "occurrence":
                        duplicate["member_token_ids"] = ["t2", "t3"]
                    rows.append(duplicate)
                    with self.assertRaisesRegex(ValueError, "gold.*(once|ID)"):
                        evaluate(gold, predictions, CONTRACT)

    def test_sense_denominators_keep_ineligible_and_undecided_states_separate(self):
        gold, predictions = copy.deepcopy(GOLD), copy.deepcopy(PREDICTIONS)
        gold["cases"], predictions["cases"] = [], []
        states = [
            ("assigned", "matched", ["s1"], "assigned", ["s1"]),
            ("multiple_assigned", "matched", ["s1", "s2"], "abstained", []),
            ("ambiguous", "matched", ["s1", "s2"], "out_of_inventory", []),
            ("abstained", "matched", [], "unassigned", []),
            ("unassigned", "not_attempted", [], "unassigned", []),
            ("out_of_inventory", "out_of_inventory", [], "out_of_inventory", []),
            ("inventory_ineligible", "inventory_ineligible", [], "inventory_ineligible", []),
        ]
        for index, (status, lookup, selected, predicted_status, predicted_senses) in enumerate(states):
            case = copy.deepcopy(GOLD["cases"][0])
            case["id"] = f"d{index}"
            case["occurrences"] = case["occurrences"][:1]
            item = case["occurrences"][0]
            item["canonical_form"] = "other-form" if status == "inventory_ineligible" else "shared-form"
            item["sense"].update(assignment_status=status, lookup_status=lookup,
                                 selected_sense_ids=selected)
            gold["cases"].append(case)
            predicted = copy.deepcopy(PREDICTIONS["cases"][0]["occurrences"][0])
            predicted.update(sense_assignment_status=predicted_status,
                             selected_sense_ids=predicted_senses)
            predictions["cases"].append({"id": case["id"], "occurrences": [predicted]})

        result = evaluate(gold, predictions, CONTRACT)
        self.assertEqual(result["cluster_counts"], {"documents": 7, "canonical_forms": 2})
        for metric in ("prediction_coverage", "assignment_state_accuracy", "exact_set_accuracy",
                       "macro_f1", "model_abstention_rate", "model_out_of_inventory_rate"):
            self.assertEqual(result["sense"][metric],
                             {"numerator": 1, "denominator": 3, "value": 0.333333})
        for metric in ("gold_ambiguity_rate", "gold_multiple_assignment_rate"):
            self.assertEqual(result["sense"][metric],
                             {"numerator": 1, "denominator": 7, "value": 0.142857})
        for metric, numerator, denominator in (
            ("occurrence_sense_inventory_coverage", 4, 7),
            ("canonical_form_sense_inventory_coverage", 1, 2),
            ("occurrence_gold_out_of_inventory_rate", 1, 7),
            ("canonical_form_gold_out_of_inventory_rate", 1, 2),
            ("occurrence_gold_inventory_ineligible_rate", 1, 7),
        ):
            self.assertEqual(result["inventory"][metric], {
                "numerator": numerator, "denominator": denominator,
                "value": round(numerator / denominator, 6),
            })
        for start in (3, 7):
            subset_gold, subset_predictions = copy.deepcopy(gold), copy.deepcopy(predictions)
            subset_gold["cases"] = subset_gold["cases"][start:]
            subset_predictions["cases"] = subset_predictions["cases"][start:]
            result = evaluate(subset_gold, subset_predictions, CONTRACT)
            for metric in ("prediction_coverage", "assignment_state_accuracy", "exact_set_accuracy",
                           "macro_f1", "model_abstention_rate", "model_out_of_inventory_rate"):
                self.assertEqual(result["sense"][metric],
                                 {"numerator": 0, "denominator": 0, "value": None})
            self.assertEqual(result["inventory"]["occurrence_gold_out_of_inventory_rate"]["denominator"],
                             7 - start)
        for case in predictions["cases"]:
            case["occurrences"] = []
        result = evaluate(gold, predictions, CONTRACT)
        for metric in ("prediction_coverage", "assignment_state_accuracy", "exact_set_accuracy",
                       "macro_f1", "model_abstention_rate", "model_out_of_inventory_rate"):
            self.assertEqual(result["sense"][metric],
                             {"numerator": 0, "denominator": 3, "value": 0.0})

    def test_malformed_gold_sense_states_are_rejected_before_scoring(self):
        for mode in ("open_text", "provided_candidates"):
            predictions = copy.deepcopy(PREDICTIONS)
            predictions["evaluation_mode"] = mode
            if mode == "provided_candidates":
                predictions["cases"][0]["occurrences"] = [
                    dict(predicted, id=reference["id"])
                    for reference, predicted in zip(
                        GOLD["cases"][0]["occurrences"], predictions["cases"][0]["occurrences"]
                    )
                ]
            for field, values in (
                ("selected_sense_ids", [None, [], ["s2"], ["s2", "s2"], "s2", [{}, {}], ["", "s3"]]),
                ("assignment_status", [None, "unknown", "assigned", "unassigned", "abstained",
                                       "out_of_inventory", "inventory_ineligible"]),
                ("lookup_status", [None, "unknown", "not_attempted", "out_of_inventory",
                                   "inventory_ineligible"]),
            ):
                for value in values:
                    with self.subTest(mode=mode, field=field, value=value):
                        gold = copy.deepcopy(GOLD)
                        gold["cases"][0]["occurrences"][1]["sense"][field] = value
                        with self.assertRaisesRegex(ValueError, "[Gg]old"):
                            evaluate(gold, predictions, CONTRACT)
            for value in (None, {}, [], "unassigned"):
                gold = copy.deepcopy(GOLD)
                gold["cases"][0]["occurrences"][1]["sense"] = value
                with self.assertRaisesRegex(ValueError, "[Gg]old"):
                    evaluate(gold, predictions, CONTRACT)
            for status in ("candidate", "rejected", "unknown"):
                gold = copy.deepcopy(GOLD)
                gold["cases"][0]["occurrences"][1]["status"] = status
                with self.assertRaisesRegex(ValueError, "[Gg]old"):
                    evaluate(gold, predictions, CONTRACT)

    def test_evaluation_dispatch_preserves_legacy_but_rejects_invalid_options(self):
        gold = json.loads((ROOT / "tests/fixtures/mwe_cases.json").read_text(encoding="utf-8"))
        legacy = json.loads((ROOT / "tests/fixtures/mwe_predictions_surface_baseline.json")
                            .read_text(encoding="utf-8"))
        self.assertEqual(evaluate(gold, legacy, CONTRACT), legacy["expected"])
        explicit = dict(legacy, evaluation_mode="provided_candidates")
        self.assertEqual(evaluate(gold, explicit, CONTRACT), legacy["expected"])
        for mode in (None, "", "open-text", "OPEN_TEXT", False, 0, [], {}):
            with self.subTest(mode=mode):
                with self.assertRaisesRegex(ValueError, "evaluation_mode"):
                    evaluate(gold, dict(legacy, evaluation_mode=mode), CONTRACT)
        self.assertEqual(evaluate(GOLD, PREDICTIONS, CONTRACT, METRIC_CONTRACT),
                         evaluate(GOLD, PREDICTIONS, CONTRACT))
        with self.assertRaises(KeyError):
            evaluate(GOLD, PREDICTIONS, CONTRACT, {})
        wrong_contract = copy.deepcopy(METRIC_CONTRACT)
        wrong_contract["benchmark_mwe_evaluation"]["contract_version"] = "wrong-version"
        with self.assertRaisesRegex(ValueError, "metric_contract_version"):
            evaluate(GOLD, PREDICTIONS, CONTRACT, wrong_contract)
        with tempfile.TemporaryDirectory() as directory:
            contract_path = Path(directory) / "invalid-contract.json"
            for content in ("null", "false", "[]", '"wrong-contract"'):
                contract_path.write_text(content, encoding="utf-8")
                process = subprocess.run([
                    sys.executable, str(ROOT / "scripts/evaluate_mwe_predictions.py"),
                    str(ROOT / "tests/fixtures/mwe_predictions_surface_baseline.json"),
                    "--metric-contract", str(contract_path),
                ], cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(process.returncode, 2, process.stdout)
                self.assertEqual(process.stdout, "")
                self.assertIn("Metric contract must be a JSON object", process.stderr)

    def test_contract_names_every_metric_boundary(self):
        benchmark = METRIC_CONTRACT["benchmark_mwe_evaluation"]
        self.assertEqual(benchmark["contract_version"], "1.1.0-predata")
        self.assertEqual(benchmark["common_rules"]["combined_score"], "forbidden")
        required = {"input", "denominator", "undefined", "bootstrap_unit"}
        self.assertTrue(benchmark["metrics"])
        for metric in benchmark["metrics"].values():
            self.assertTrue(required <= metric.keys())

    def test_gold_token_identity_and_order_are_validated_before_scoring(self):
        for field, values in (
            ("id", [None, "", " ", "t2", 1, True, []]),
            ("position", [None, 0, 2, 1.0, True, "1"]),
        ):
            for value in values:
                with self.subTest(field=field, value=value):
                    gold = copy.deepcopy(GOLD)
                    gold["cases"][0]["tokens"][0][field] = value
                    with self.assertRaisesRegex(ValueError, "gold token"):
                        evaluate(gold, PREDICTIONS, CONTRACT)
        for change in ("duplicate", "reverse"):
            with self.subTest(change=change):
                gold = copy.deepcopy(GOLD)
                tokens = gold["cases"][0]["tokens"]
                if change == "duplicate":
                    tokens.append(copy.deepcopy(tokens[-1]))
                else:
                    tokens.reverse()
                with self.assertRaisesRegex(ValueError, "gold token"):
                    evaluate(gold, PREDICTIONS, CONTRACT)
        for tokens in (None, {}, [None]):
            with self.subTest(tokens=tokens):
                gold = copy.deepcopy(GOLD)
                gold["cases"][0]["tokens"] = tokens
                with self.assertRaisesRegex(ValueError, "gold token"):
                    evaluate(gold, PREDICTIONS, CONTRACT)

    def test_gold_spans_use_the_same_member_and_gap_rules_as_predictions(self):
        for field, values in (
            ("member_token_ids", [[], ["t4"], ["t4", "t4"], ["t6", "t4"],
                                  ["t4", "missing"], [[], "t6"]]),
            ("gap_token_ids", [None, [], ["t5", "t5"], ["t4", "t5"], ["missing"], [[]]]),
        ):
            for value in values:
                with self.subTest(field=field, value=value, side="prediction"):
                    predictions = copy.deepcopy(PREDICTIONS)
                    predictions["cases"][0]["occurrences"][1][field] = value
                    with self.assertRaisesRegex(ValueError, "[Pp]redicted.*(members|gaps)"):
                        evaluate(GOLD, predictions, CONTRACT)
                for status in ("confirmed", "rejected", "candidate"):
                    with self.subTest(field=field, value=value, status=status):
                        gold = copy.deepcopy(GOLD)
                        item = gold["cases"][0]["occurrences"][1]
                        item[field] = value
                        item["status"] = status
                        if status != "confirmed":
                            item["sense"] = None
                            item["idiomaticity"]["status"] = "not_assessed"
                        with self.assertRaisesRegex(ValueError, "[Gg]old.*(members|gaps)"):
                            evaluate(gold, PREDICTIONS, CONTRACT)

    def test_nonexhaustive_gap_prediction_is_rejected(self):
        malformed = copy.deepcopy(PREDICTIONS)
        malformed["cases"][0]["occurrences"][1]["gap_token_ids"] = []
        with self.assertRaisesRegex(ValueError, "gaps are not exhaustive"):
            evaluate(GOLD, malformed, CONTRACT)

        wrong_version = copy.deepcopy(PREDICTIONS)
        wrong_version["metric_contract_version"] = "future-version"
        with self.assertRaisesRegex(ValueError, "metric_contract_version"):
            evaluate(GOLD, wrong_version, CONTRACT)


if __name__ == "__main__":
    unittest.main()
