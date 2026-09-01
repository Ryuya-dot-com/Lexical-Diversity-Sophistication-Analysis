#!/usr/bin/env python3
"""Evaluate contextual decisions for already supplied MWE candidates."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def ratio(numerator, denominator):
    return {
        "numerator": numerator,
        "denominator": denominator,
        "value": round(numerator / denominator, 6) if denominator else None,
    }


def evaluate(gold, predictions, contract):
    versions = {gold.get("contract_version"), predictions.get("contract_version")}
    if versions != {contract["contract_version"]}:
        raise ValueError("Gold, predictions, and contract versions must match.")

    gold_cases = {case["id"]: case for case in gold["cases"]}
    predicted_cases = {case["id"]: case for case in predictions["cases"]}
    if len(predicted_cases) != len(predictions["cases"]) or gold_cases.keys() != predicted_cases.keys():
        raise ValueError("Predictions must contain each gold case exactly once.")

    statuses = set(contract["occurrence_record"]["statuses"])
    idiomaticity_statuses = set(contract["occurrence_record"]["idiomaticity_statuses"])
    rows = []
    for case_id, gold_case in gold_cases.items():
        gold_items = {item["id"]: item for item in gold_case["occurrences"]}
        predicted_list = predicted_cases[case_id]["occurrences"]
        predicted_items = {item["id"]: item for item in predicted_list}
        if len(predicted_items) != len(predicted_list) or gold_items.keys() != predicted_items.keys():
            raise ValueError(f"Predictions must contain each occurrence in {case_id} exactly once.")
        for occurrence_id, gold_item in gold_items.items():
            predicted = predicted_items[occurrence_id]
            selected = predicted.get("selected_sense_ids")
            if predicted.get("status") not in statuses:
                raise ValueError(f"Unknown predicted status: {occurrence_id}.")
            if predicted.get("idiomaticity_status") not in idiomaticity_statuses:
                raise ValueError(f"Unknown predicted idiomaticity: {occurrence_id}.")
            if (not isinstance(selected, list) or len(selected) != len(set(selected)) or
                    any(not isinstance(item, str) or not item for item in selected)):
                raise ValueError(f"Invalid predicted senses: {occurrence_id}.")
            if predicted["status"] == "candidate" and predicted["idiomaticity_status"] != "not_assessed":
                raise ValueError(f"Unresolved prediction carries idiomaticity: {occurrence_id}.")
            if predicted["status"] != "confirmed" and selected:
                raise ValueError(f"Non-confirmed prediction carries a sense: {occurrence_id}.")
            rows.append((gold_item, predicted))

    terminal = {"confirmed", "rejected"}
    decision_rows = [(gold_item, predicted) for gold_item, predicted in rows
                     if gold_item["status"] in terminal]
    decided = [(gold_item, predicted) for gold_item, predicted in decision_rows
               if predicted["status"] in terminal]
    correct_decisions = sum(gold_item["status"] == predicted["status"]
                            for gold_item, predicted in decided)
    true_positive = sum(gold_item["status"] == predicted["status"] == "confirmed"
                        for gold_item, predicted in decision_rows)
    predicted_positive = sum(predicted["status"] == "confirmed"
                             for _, predicted in decision_rows)
    gold_positive = sum(gold_item["status"] == "confirmed"
                        for gold_item, _ in decision_rows)
    precision = ratio(true_positive, predicted_positive)
    recall = ratio(true_positive, gold_positive)
    f1_denominator = predicted_positive + gold_positive

    idiom_gold = [(gold_item, predicted) for gold_item, predicted in rows
                  if gold_item["idiomaticity"]["status"] != "not_assessed"]
    idiom_predicted = [(gold_item, predicted) for gold_item, predicted in idiom_gold
                       if predicted["idiomaticity_status"] != "not_assessed"]
    idiom_correct = sum(
        gold_item["idiomaticity"]["status"] == predicted["idiomaticity_status"]
        for gold_item, predicted in idiom_predicted
    )

    sense_gold = [(gold_item, predicted) for gold_item, predicted in rows
                  if (gold_item.get("sense") or {}).get("assignment_status") == "assigned"]
    sense_predicted = [(gold_item, predicted) for gold_item, predicted in sense_gold
                       if predicted["selected_sense_ids"]]
    sense_correct = sum(
        set(gold_item["sense"]["selected_sense_ids"]) == set(predicted["selected_sense_ids"])
        for gold_item, predicted in sense_predicted
    )

    return {
        "evaluation_scope": "provided-candidate contextual decisions; not candidate generation or span detection",
        "system": predictions["system"],
        "case_count": len(gold_cases),
        "candidate_count": len(rows),
        "occurrence_decision_coverage": ratio(len(decided), len(decision_rows)),
        "occurrence_decision_accuracy": ratio(correct_decisions, len(decided)),
        "confirmed_precision": precision,
        "confirmed_recall": recall,
        "confirmed_f1": round(2 * true_positive / f1_denominator, 6)
        if f1_denominator else None,
        "idiomaticity_prediction_coverage": ratio(len(idiom_predicted), len(idiom_gold)),
        "idiomaticity_accuracy": ratio(idiom_correct, len(idiom_predicted)),
        "sense_prediction_coverage": ratio(len(sense_predicted), len(sense_gold)),
        "sense_exact_match_accuracy": ratio(sense_correct, len(sense_predicted)),
    }


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--gold", type=Path, default=ROOT / "tests/fixtures/mwe_cases.json")
    parser.add_argument("--contract", type=Path, default=ROOT / "mwe_contract.json")
    parser.add_argument("--check", action="store_true", help="compare with predictions.expected")
    args = parser.parse_args()
    try:
        predictions = load(args.predictions)
        result = evaluate(load(args.gold), predictions, load(args.contract))
        if args.check and result != predictions.get("expected"):
            raise ValueError("Evaluation does not match predictions.expected.")
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
