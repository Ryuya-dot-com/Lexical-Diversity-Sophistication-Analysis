#!/usr/bin/env python3
"""Evaluate supplied-candidate decisions or open-text VPC/VID predictions."""

import argparse
from collections import Counter
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def ratio(numerator, denominator):
    return {
        "numerator": numerator,
        "denominator": denominator,
        "value": round(numerator / denominator, 6) if denominator else None,
    }


def prf(true_positive, predicted_positive, gold_positive):
    return {
        "precision": ratio(true_positive, predicted_positive),
        "recall": ratio(true_positive, gold_positive),
        "f1": ratio(2 * true_positive, predicted_positive + gold_positive),
    }


def calibration_scores(probabilities, labels, bins=10):
    if len(probabilities) != len(labels):
        raise ValueError("probabilities and labels must have equal length")
    if not probabilities:
        return {
            "brier": ratio(0, 0),
            "log_loss": ratio(0, 0),
            "ece": ratio(0, 0),
        }
    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or not 0 <= value <= 1
        for value in probabilities
    ):
        raise ValueError("probabilities must be finite numbers from 0 through 1")
    if any(label not in {0, 1} for label in labels):
        raise ValueError("calibration labels must be binary")

    brier = sum((probability - label) ** 2 for probability, label in zip(probabilities, labels))
    losses = []
    infinite = False
    for probability, label in zip(probabilities, labels):
        likelihood = probability if label else 1 - probability
        if likelihood == 0:
            infinite = True
            break
        losses.append(-math.log(likelihood))

    grouped = [[] for _ in range(bins)]
    for probability, label in zip(probabilities, labels):
        grouped[min(bins - 1, int(probability * bins))].append((probability, label))
    ece = sum(
        len(group) / len(probabilities)
        * abs(
            sum(probability for probability, _ in group) / len(group)
            - sum(label for _, label in group) / len(group)
        )
        for group in grouped
        if group
    )
    return {
        "brier": ratio(round(brier, 12), len(probabilities)),
        "log_loss": {
            "numerator": None if infinite else round(sum(losses), 12),
            "denominator": len(probabilities),
            "value": None if infinite else round(sum(losses) / len(probabilities), 6),
            "state": "infinite" if infinite else "defined",
        },
        "ece": ratio(round(ece * len(probabilities), 12), len(probabilities)),
        "bin_count": bins,
    }


def risk_coverage(correct_and_confidence, total_count):
    if total_count < len(correct_and_confidence):
        raise ValueError("total_count cannot be smaller than scored decisions")
    ranked = sorted(
        correct_and_confidence,
        key=lambda item: (-item[1], item[2]),
    )
    errors = 0
    points = []
    for rank, (correct, confidence, item_id) in enumerate(ranked, 1):
        errors += not correct
        points.append({
            "rank": rank,
            "item_id": item_id,
            "confidence": confidence,
            "coverage": round(rank / total_count, 6) if total_count else None,
            "risk": round(errors / rank, 6),
        })
    return {
        "decision_coverage": ratio(len(ranked), total_count),
        "aurc_over_ranked_decisions": ratio(
            round(sum(point["risk"] for point in points), 12), len(points)
        ),
        "points": points,
    }


def _validate_sense_assignment(status, selected, contract, label):
    if status not in contract["occurrence_record"]["sense_assignment_statuses"]:
        raise ValueError(f"Unknown sense assignment status: {label}.")
    if (
        not isinstance(selected, list)
        or any(not isinstance(sense_id, str) or not sense_id for sense_id in selected)
        or len(selected) != len(set(selected))
    ):
        raise ValueError(f"Invalid selected sense IDs: {label}.")
    if (status == "assigned" and len(selected) != 1) or (
        status in {"multiple_assigned", "ambiguous"} and len(selected) < 2
    ) or (status not in {"assigned", "multiple_assigned", "ambiguous"} and selected):
        raise ValueError(f"Sense state and selection disagree: {label}.")


def _validate_gold_sense(item, contract):
    label = f"gold occurrence {item['id']}"
    if item.get("status") not in contract["occurrence_record"]["statuses"]:
        raise ValueError(f"Unknown occurrence status: {label}.")
    sense = item.get("sense")
    if item["status"] != "confirmed":
        if sense is not None:
            raise ValueError(f"Non-confirmed gold occurrence carries a sense: {item['id']}.")
        return
    if not isinstance(sense, dict):
        raise ValueError(f"Confirmed gold occurrence requires a sense record: {item['id']}.")
    status = sense.get("assignment_status")
    _validate_sense_assignment(status, sense.get("selected_sense_ids"), contract, label)
    allowed_lookups = {
        "unassigned": ("matched", "not_attempted"),
        "out_of_inventory": ("matched", "out_of_inventory"),
        "inventory_ineligible": ("inventory_ineligible",),
    }.get(status, ("matched",))
    if sense.get("lookup_status") not in allowed_lookups:
        raise ValueError(f"Sense lookup and assignment disagree: {label}.")


def evaluate_provided_candidates(gold, predictions, contract):
    versions = {gold.get("contract_version"), predictions.get("contract_version")}
    if versions != {contract["contract_version"]}:
        raise ValueError("Gold, predictions, and contract versions must match.")

    gold_cases = {case["id"]: case for case in gold["cases"]}
    if len(gold_cases) != len(gold["cases"]):
        raise ValueError("Duplicate gold document ID.")
    predicted_cases = {case["id"]: case for case in predictions["cases"]}
    if len(predicted_cases) != len(predictions["cases"]) or gold_cases.keys() != predicted_cases.keys():
        raise ValueError("Predictions must contain each gold case exactly once.")

    statuses = set(contract["occurrence_record"]["statuses"])
    idiomaticity_statuses = set(contract["occurrence_record"]["idiomaticity_statuses"])
    rows = []
    for case_id, gold_case in gold_cases.items():
        gold_items = {item["id"]: item for item in gold_case["occurrences"]}
        if len(gold_items) != len(gold_case["occurrences"]):
            raise ValueError(f"Duplicate gold occurrence ID in {case_id}.")
        predicted_list = predicted_cases[case_id]["occurrences"]
        predicted_items = {item["id"]: item for item in predicted_list}
        if len(predicted_items) != len(predicted_list) or gold_items.keys() != predicted_items.keys():
            raise ValueError(f"Predictions must contain each occurrence in {case_id} exactly once.")
        for occurrence_id, gold_item in gold_items.items():
            _validate_gold_sense(gold_item, contract)
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
                  if (gold_item.get("sense") or {}).get("assignment_status")
                  in {"assigned", "multiple_assigned", "ambiguous"}]
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


def _validate_member_span(item, token_positions, label):
    members = item.get("member_token_ids")
    gaps = item.get("gap_token_ids")
    if (
        not isinstance(members, list)
        or len(members) < 2
        or any(not isinstance(member, str) for member in members)
        or len(members) != len(set(members))
        or any(member not in token_positions for member in members)
        or [token_positions[member] for member in members]
        != sorted(token_positions[member] for member in members)
    ):
        raise ValueError(f"Invalid {label} members: {item['id']}")
    if (
        not isinstance(gaps, list)
        or any(not isinstance(gap, str) for gap in gaps)
        or len(gaps) != len(set(gaps))
        or any(gap not in token_positions or gap in members for gap in gaps)
    ):
        raise ValueError(f"Invalid {label} gaps: {item['id']}")
    expected_gaps = [
        token_id
        for token_id, position in sorted(token_positions.items(), key=lambda pair: pair[1])
        if token_positions[members[0]] < position < token_positions[members[-1]]
        and token_id not in members
    ]
    if gaps != expected_gaps:
        raise ValueError(f"{label.capitalize()} gaps are not exhaustive: {item['id']}")


def _validate_open_prediction(item, token_positions, contract):
    required = {
        "id",
        "head_token_id",
        "member_token_ids",
        "gap_token_ids",
        "category",
        "status",
        "idiomaticity_status",
        "sense_assignment_status",
        "selected_sense_ids",
    }
    optional = {"confirmed_probability", "decision_confidence"}
    if not required <= set(item) or set(item) - required - optional:
        raise ValueError(f"Invalid open-text prediction fields: {item.get('id')}")
    _validate_member_span(item, token_positions, "predicted")
    if item["head_token_id"] not in item["member_token_ids"]:
        raise ValueError(f"Predicted head must be a member: {item['id']}")
    if item["category"] not in contract["occurrence_record"]["categories"]:
        raise ValueError(f"Unknown predicted category: {item['id']}")
    if item["status"] not in contract["occurrence_record"]["statuses"]:
        raise ValueError(f"Unknown predicted status: {item['id']}")
    if item["idiomaticity_status"] not in contract["occurrence_record"]["idiomaticity_statuses"]:
        raise ValueError(f"Unknown predicted idiomaticity: {item['id']}")
    sense_status = item["sense_assignment_status"]
    selected = item["selected_sense_ids"]
    _validate_sense_assignment(sense_status, selected, contract, f"prediction {item['id']}")
    if item["status"] == "candidate" and item["idiomaticity_status"] != "not_assessed":
        raise ValueError(f"Unresolved prediction carries idiomaticity: {item['id']}")
    if item["status"] != "confirmed" and (sense_status != "unassigned" or selected):
        raise ValueError(f"Non-confirmed prediction carries later-stage labels: {item['id']}")
    for field in optional & set(item):
        value = item[field]
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or not 0 <= value <= 1
        ):
            raise ValueError(f"{field} must be from 0 through 1: {item['id']}")


def evaluate_open_text(gold, predictions, contract, metric_contract):
    versions = {gold.get("contract_version"), predictions.get("contract_version")}
    if versions != {contract["contract_version"]}:
        raise ValueError("Gold, predictions, and contract versions must match.")
    metric_version = metric_contract["benchmark_mwe_evaluation"]["contract_version"]
    if predictions.get("metric_contract_version") != metric_version:
        raise ValueError("Prediction metric_contract_version does not match benchmark metric contract")
    if not isinstance(predictions.get("system"), dict):
        raise ValueError("Predictions require a system object")
    gold_cases = {case["id"]: case for case in gold["cases"]}
    predicted_cases = {case["id"]: case for case in predictions["cases"]}
    if (
        len(gold_cases) != len(gold["cases"])
        or len(predicted_cases) != len(predictions["cases"])
        or gold_cases.keys() != predicted_cases.keys()
    ):
        raise ValueError("Predictions must contain each gold document exactly once.")

    categories = contract["occurrence_record"]["categories"]
    gold_positive = []
    gold_all = []
    predicted_all = []
    exact_gold = {}
    exact_predictions = {}
    for case_id, gold_case in gold_cases.items():
        tokens = gold_case.get("tokens")
        if not isinstance(tokens, list):
            raise ValueError(f"Invalid gold token list in {case_id}.")
        token_positions = {}
        for position, token in enumerate(tokens, 1):
            if (
                not isinstance(token, dict)
                or not isinstance(token.get("id"), str)
                or not token["id"].strip()
                or token["id"] in token_positions
                or type(token.get("position")) is not int
                or token["position"] != position
            ):
                raise ValueError(f"Invalid gold token ID or position in {case_id}.")
            token_positions[token["id"]] = position
        if len({item["id"] for item in gold_case["occurrences"]}) != len(gold_case["occurrences"]):
            raise ValueError(f"Duplicate gold occurrence ID in {case_id}.")
        predicted_items = predicted_cases[case_id]["occurrences"]
        if len({item["id"] for item in predicted_items}) != len(predicted_items):
            raise ValueError(f"Duplicate prediction ID in {case_id}")
        case_spans = set()
        for item in predicted_items:
            _validate_open_prediction(item, token_positions, contract)
            key = (case_id, tuple(item["member_token_ids"]))
            if key in case_spans:
                raise ValueError(f"Duplicate predicted member span in {case_id}")
            case_spans.add(key)
            predicted_all.append((case_id, item))
            exact_predictions[key] = item
        for item in gold_case["occurrences"]:
            _validate_gold_sense(item, contract)
            _validate_member_span(item, token_positions, "gold")
            if item["status"] == "candidate":
                raise ValueError(
                    f"Open-text gold contains unresolved candidate: {case_id}/{item['id']}; "
                    "scoring requires adjudicated occurrence decisions."
                )
            key = (case_id, tuple(item["member_token_ids"]))
            if key in exact_gold:
                raise ValueError(f"Duplicate gold member span in {case_id}")
            exact_gold[key] = item
            gold_all.append((case_id, item))
            if item["status"] == "confirmed":
                gold_positive.append((case_id, item))

    emitted_heads = Counter(
        (case_id, item["head_token_id"]) for case_id, item in predicted_all
    )
    gold_heads = Counter(
        (case_id, item["member_token_ids"][0]) for case_id, item in gold_positive
    )
    recovered_candidates = sum(
        min(count, emitted_heads[head]) for head, count in gold_heads.items()
    )

    confirmed_predictions = [
        (case_id, item)
        for case_id, item in predicted_all
        if item["status"] == "confirmed"
    ]
    gold_positive_keys = {
        (case_id, tuple(item["member_token_ids"])) for case_id, item in gold_positive
    }
    confirmed_prediction_keys = {
        (case_id, tuple(item["member_token_ids"]))
        for case_id, item in confirmed_predictions
    }
    exact_true_positive_keys = gold_positive_keys & confirmed_prediction_keys

    gold_member_tokens = {
        (case_id, token_id)
        for case_id, item in gold_positive
        for token_id in item["member_token_ids"]
    }
    predicted_member_tokens = {
        (case_id, token_id)
        for case_id, item in confirmed_predictions
        for token_id in item["member_token_ids"]
    }

    category_rows = {}
    category_f1_values = []
    for category in categories:
        gold_keys = {
            (case_id, tuple(item["member_token_ids"]))
            for case_id, item in gold_positive
            if item["category"] == category
        }
        predicted_keys = {
            (case_id, tuple(item["member_token_ids"]))
            for case_id, item in confirmed_predictions
            if item["category"] == category
        }
        true_positive = len({
            key for key in gold_keys & predicted_keys
            if exact_gold[key]["category"] == exact_predictions[key]["category"]
        })
        scores = prf(true_positive, len(predicted_keys), len(gold_keys))
        category_rows[category] = scores
        category_f1_values.append(scores["f1"]["value"])
    category_macro_f1 = {
        "numerator": round(sum(value for value in category_f1_values if value is not None), 12),
        "denominator": len(categories),
        "value": round(sum(category_f1_values) / len(categories), 6)
        if all(value is not None for value in category_f1_values)
        else None,
        "undefined_categories": [
            category for category, value in zip(categories, category_f1_values)
            if value is None
        ],
    }

    gap_correct = sum(
        exact_predictions[key]["gap_token_ids"] == exact_gold[key]["gap_token_ids"]
        for key in exact_true_positive_keys
    )
    idiom_gold = [
        (case_id, item)
        for case_id, item in gold_all
        if item["idiomaticity"]["status"] != "not_assessed"
    ]
    idiom_predictions = []
    for case_id, item in idiom_gold:
        predicted = exact_predictions.get((case_id, tuple(item["member_token_ids"])))
        if predicted and predicted["idiomaticity_status"] != "not_assessed":
            idiom_predictions.append((item, predicted))
    idiom_correct = sum(
        gold_item["idiomaticity"]["status"] == predicted["idiomaticity_status"]
        for gold_item, predicted in idiom_predictions
    )

    explicit_sense_gold = [
        (case_id, item)
        for case_id, item in gold_positive
        if item.get("sense") is not None
    ]
    sense_lookup_by_form = {
        canonical_form: {
            item["sense"]["lookup_status"]
            for _, item in explicit_sense_gold
            if item["canonical_form"] == canonical_form
        }
        for canonical_form in {item["canonical_form"] for _, item in gold_positive}
    }
    sense_assignment_by_form = {
        canonical_form: {
            item["sense"]["assignment_status"]
            for _, item in explicit_sense_gold
            if item["canonical_form"] == canonical_form
        }
        for canonical_form in {item["canonical_form"] for _, item in gold_positive}
    }
    sense_reference = [
        (case_id, item)
        for case_id, item in explicit_sense_gold
        if item["sense"]["assignment_status"] in {"assigned", "multiple_assigned", "ambiguous"}
        and item["sense"]["selected_sense_ids"]
    ]
    sense_exact = 0
    sense_true_positive = 0
    sense_predicted_labels = 0
    sense_gold_labels = 0
    sense_macro_values = []
    sense_predictions = 0
    sense_state_correct = 0
    sense_abstentions = 0
    predicted_ooi = 0
    for case_id, item in sense_reference:
        predicted = exact_predictions.get((case_id, tuple(item["member_token_ids"])))
        predicted_senses = set(predicted["selected_sense_ids"]) if predicted else set()
        gold_senses = set(item["sense"]["selected_sense_ids"])
        predicted_status = predicted["sense_assignment_status"] if predicted else "unassigned"
        sense_predictions += predicted_status in {"assigned", "multiple_assigned", "ambiguous"}
        sense_state_correct += predicted_status == item["sense"]["assignment_status"]
        sense_abstentions += predicted_status == "abstained"
        predicted_ooi += predicted_status == "out_of_inventory"
        sense_exact += predicted_senses == gold_senses
        sense_true_positive += len(predicted_senses & gold_senses)
        sense_predicted_labels += len(predicted_senses)
        sense_gold_labels += len(gold_senses)
        sense_macro_values.append(
            2 * len(predicted_senses & gold_senses)
            / (len(predicted_senses) + len(gold_senses))
            if predicted_senses or gold_senses
            else 0
        )

    probabilities = [
        item.get("confirmed_probability") for _, item in predicted_all
    ]
    probabilistic = predictions["system"].get("probabilistic", False)
    if not isinstance(probabilistic, bool):
        raise ValueError("system.probabilistic must be boolean")
    if probabilistic and any(value is None for value in probabilities):
        raise ValueError("Probabilistic systems require confirmed_probability on every emitted candidate")
    calibration = (
        calibration_scores(
            probabilities,
            [
                int((case_id, tuple(item["member_token_ids"])) in gold_positive_keys)
                for case_id, item in predicted_all
            ],
        )
        if probabilistic
        else {"state": "not_applicable_nonprobabilistic_system"}
    )

    selective = predictions["system"].get("selective", False)
    if not isinstance(selective, bool):
        raise ValueError("system.selective must be boolean")
    if selective:
        if any(item.get("decision_confidence") is None for _, item in predicted_all):
            raise ValueError("Selective systems require decision_confidence on every emitted candidate")
        decided_rows = []
        for case_id, item in predicted_all:
            if item["status"] not in {"confirmed", "rejected"}:
                continue
            is_gold = (case_id, tuple(item["member_token_ids"])) in gold_positive_keys
            correct = (item["status"] == "confirmed") == is_gold
            decided_rows.append((correct, item["decision_confidence"], f"{case_id}:{item['id']}"))
        selective_report = risk_coverage(decided_rows, len(predicted_all))
    else:
        selective_report = {"state": "not_applicable_nonselective_system"}

    return {
        "evaluation_scope": "open-text candidate, span, category, idiomaticity, inventory, and contextual-sense tasks; synthetic checks are not validation",
        "metric_contract_version": metric_version,
        "system": predictions["system"],
        "case_count": len(gold_cases),
        "cluster_counts": {
            "documents": len(gold_cases),
            "canonical_forms": len({
                item["canonical_form"] for _, item in gold_positive
            }),
        },
        "candidate": {
            "emitted_count": len(predicted_all),
            "recall": ratio(recovered_candidates, len(gold_positive)),
            "match_rule": "one-to-one capacity by document and gold first-member verbal-head token; span correctness is scored separately",
        },
        "span": {
            "exact": prf(
                len(exact_true_positive_keys),
                len(confirmed_prediction_keys),
                len(gold_positive_keys),
            ),
            "member_token": prf(
                len(gold_member_tokens & predicted_member_tokens),
                len(predicted_member_tokens),
                len(gold_member_tokens),
            ),
            "member_set_accuracy": ratio(len(exact_true_positive_keys), len(gold_positive)),
            "gap_set_accuracy": ratio(gap_correct, len(gold_positive)),
        },
        "category": {
            "per_category": category_rows,
            "macro_f1": category_macro_f1,
        },
        "idiomaticity": {
            "prediction_coverage": ratio(len(idiom_predictions), len(idiom_gold)),
            "accuracy_among_predictions": ratio(idiom_correct, len(idiom_predictions)),
            "gold_ambiguity_rate": ratio(
                sum(item["idiomaticity"]["status"] == "ambiguous" for _, item in idiom_gold),
                len(idiom_gold),
            ),
        },
        "inventory": {
            "occurrence_sense_inventory_coverage": ratio(
                sum(item["sense"]["lookup_status"] == "matched" for _, item in explicit_sense_gold),
                len(gold_positive),
            ),
            "canonical_form_sense_inventory_coverage": ratio(
                sum("matched" in statuses for statuses in sense_lookup_by_form.values()),
                len(sense_lookup_by_form),
            ),
            "occurrence_gold_out_of_inventory_rate": ratio(
                sum(item["sense"]["assignment_status"] == "out_of_inventory" for _, item in explicit_sense_gold),
                len(gold_positive),
            ),
            "canonical_form_gold_out_of_inventory_rate": ratio(
                sum(
                    "out_of_inventory" in statuses
                    for statuses in sense_assignment_by_form.values()
                ),
                len(sense_assignment_by_form),
            ),
            "occurrence_gold_inventory_ineligible_rate": ratio(
                sum(item["sense"]["assignment_status"] == "inventory_ineligible" for _, item in explicit_sense_gold),
                len(gold_positive),
            ),
        },
        "sense": {
            "prediction_coverage": ratio(sense_predictions, len(sense_reference)),
            "assignment_state_accuracy": ratio(sense_state_correct, len(sense_reference)),
            "exact_set_accuracy": ratio(sense_exact, len(sense_reference)),
            "micro": prf(sense_true_positive, sense_predicted_labels, sense_gold_labels),
            "macro_f1": ratio(round(sum(sense_macro_values), 12), len(sense_macro_values)),
            "gold_ambiguity_rate": ratio(
                sum(item["sense"]["assignment_status"] == "ambiguous" for _, item in explicit_sense_gold),
                len(gold_positive),
            ),
            "gold_multiple_assignment_rate": ratio(
                sum(item["sense"]["assignment_status"] == "multiple_assigned" for _, item in explicit_sense_gold),
                len(gold_positive),
            ),
            "model_abstention_rate": ratio(sense_abstentions, len(sense_reference)),
            "model_out_of_inventory_rate": ratio(predicted_ooi, len(sense_reference)),
        },
        "burden": {
            "emitted_candidates_per_document": ratio(len(predicted_all), len(gold_cases)),
            "review_time": {"state": "not_collected"},
        },
        "calibration": calibration,
        "selective_prediction": selective_report,
        "intervals": {"state": "not_calculated_pending_IR-126_document_cluster_bootstrap"},
        "combined_score": {"state": "forbidden"},
    }


def evaluate(gold, predictions, contract, metric_contract=None):
    mode = predictions.get("evaluation_mode", "provided_candidates")
    if mode not in ("provided_candidates", "open_text"):
        raise ValueError("evaluation_mode must be provided_candidates or open_text.")
    if mode == "open_text":
        if metric_contract is None:
            metric_contract = load(ROOT / "metric_contract.json")
        return evaluate_open_text(gold, predictions, contract, metric_contract)
    return evaluate_provided_candidates(gold, predictions, contract)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--gold", type=Path, default=ROOT / "tests/fixtures/mwe_cases.json")
    parser.add_argument("--contract", type=Path, default=ROOT / "mwe_contract.json")
    parser.add_argument("--metric-contract", type=Path, default=ROOT / "metric_contract.json")
    parser.add_argument("--check", action="store_true", help="compare with predictions.expected")
    args = parser.parse_args()
    try:
        predictions = load(args.predictions)
        metric_contract = load(args.metric_contract)
        if not isinstance(metric_contract, dict):
            raise ValueError("Metric contract must be a JSON object.")
        result = evaluate(
            load(args.gold),
            predictions,
            load(args.contract),
            metric_contract,
        )
        if args.check and result != predictions.get("expected"):
            raise ValueError("Evaluation does not match predictions.expected.")
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
