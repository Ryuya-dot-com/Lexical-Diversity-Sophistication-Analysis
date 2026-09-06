#!/usr/bin/env python3
"""Verify the pinned external STREUSLE 5.0 VPC/VID benchmark profile."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = ROOT / "benchmarks/streusle_v5_vpc_vid.json"
DEFAULT_GAP_BASELINE = ROOT / "resources/streusle_gap_dependency_baseline.json"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def summarize_split(sentences, target_categories):
    if not isinstance(sentences, list):
        raise ValueError("STREUSLE split must be a JSON array.")
    sentence_ids = set()
    occurrences = []
    token_count = 0
    for sentence in sentences:
        if not isinstance(sentence, dict) or not isinstance(sentence.get("sent_id"), str):
            raise ValueError("STREUSLE sentence identity is missing.")
        if sentence["sent_id"] in sentence_ids:
            raise ValueError(f"Duplicate STREUSLE sentence ID: {sentence['sent_id']}.")
        sentence_ids.add(sentence["sent_id"])
        tokens = sentence.get("toks")
        strong_mwes = sentence.get("smwes")
        if not isinstance(tokens, list) or not isinstance(strong_mwes, dict):
            raise ValueError(f"Invalid STREUSLE sentence structure: {sentence['sent_id']}.")
        token_count += len(tokens)
        for occurrence in strong_mwes.values():
            if occurrence.get("lexcat") not in target_categories:
                continue
            token_numbers = occurrence.get("toknums")
            if (not isinstance(occurrence.get("lexlemma"), str) or
                    not occurrence["lexlemma"].strip() or
                    not isinstance(token_numbers, list) or len(token_numbers) < 2 or
                    token_numbers != sorted(set(token_numbers)) or
                    any(not isinstance(item, int) or item < 1 or item > len(tokens)
                        for item in token_numbers)):
                raise ValueError(f"Invalid target MWE in {sentence['sent_id']}.")
            occurrences.append(occurrence)

    categories = Counter(item["lexcat"] for item in occurrences)
    types = {item["lexlemma"].casefold() for item in occurrences}
    discontinuous = sum(
        max(item["toknums"]) - min(item["toknums"]) + 1 > len(item["toknums"])
        for item in occurrences
    )
    return {
        "sentences": len(sentences),
        "tokens": token_count,
        "target_occurrences": len(occurrences),
        "target_types": len(types),
        "discontinuous_target_occurrences": discontinuous,
        "categories": dict(sorted(categories.items())),
    }, types, occurrences


def summarize_all(datasets, target_categories):
    reports = {}
    details = {}
    for split in ("train", "dev", "test"):
        reports[split], types, occurrences = summarize_split(
            datasets[split], target_categories
        )
        details[split] = (types, occurrences)
    train_types = details["train"][0]
    for split in ("dev", "test"):
        types, occurrences = details[split]
        reports[split].update({
            "types_seen_in_train": len(types & train_types),
            "types_unseen_in_train": len(types - train_types),
            "unseen_occurrences": sum(
                item["lexlemma"].casefold() not in train_types for item in occurrences
            ),
        })
    return reports


def prf(predicted, gold):
    correct = len(predicted & gold)
    precision = correct / len(predicted) if predicted else None
    recall = correct / len(gold) if gold else None
    return {
        "correct": correct,
        "predicted": len(predicted),
        "gold": len(gold),
        "precision": round(precision, 6) if precision is not None else None,
        "recall": round(recall, 6) if recall is not None else None,
        "f1": round(2 * correct / (len(predicted) + len(gold)), 6)
        if predicted or gold else None,
    }


def training_patterns(datasets, target_categories):
    train_counts = Counter()
    train_types = set()
    for sentence in datasets["train"]:
        for occurrence in sentence["smwes"].values():
            if occurrence["lexcat"] in target_categories:
                phrase = tuple(occurrence["lexlemma"].casefold().split())
                train_counts[phrase, occurrence["lexcat"]] += 1
                train_types.add(occurrence["lexlemma"].casefold())

    best_category = {}
    for phrase, category in train_counts:
        candidate = (train_counts[phrase, category], category)
        if candidate > best_category.get(phrase, (-1, "")):
            best_category[phrase] = candidate
    return best_category, train_types


def training_dependency_relations(datasets, target_categories, minimum_count):
    counts = {
        category: {"head_to_member": Counter(), "member_to_head": Counter()}
        for category in target_categories
    }
    for sentence in datasets["train"]:
        tokens = {token["#"]: token for token in sentence["toks"]}
        for occurrence in sentence["smwes"].values():
            category = occurrence["lexcat"]
            if category not in target_categories:
                continue
            first = occurrence["toknums"][0]
            for member in occurrence["toknums"][1:]:
                if tokens[member].get("head") == first:
                    counts[category]["head_to_member"][tokens[member]["deprel"]] += 1
                if tokens[first].get("head") == member:
                    counts[category]["member_to_head"][tokens[first]["deprel"]] += 1
    return {
        category: {
            direction: sorted(
                relation
                for relation, count in relation_counts.items()
                if count >= minimum_count
            )
            for direction, relation_counts in directions.items()
        }
        for category, directions in counts.items()
    }


def surface_baseline(datasets, category_mapping):
    target_categories = set(category_mapping)
    best_category, train_types = training_patterns(datasets, target_categories)

    predicted_spans = set()
    predicted_labeled = set()
    for sentence in datasets["test"]:
        lemmas = [token.get("lemma") for token in sentence["toks"]]
        if any(not isinstance(lemma, str) for lemma in lemmas):
            raise ValueError(f"Missing test lemma in {sentence['sent_id']}.")
        lemmas = [lemma.casefold() for lemma in lemmas]
        for phrase, (_, category) in best_category.items():
            for start in range(len(lemmas) - len(phrase) + 1):
                if tuple(lemmas[start:start + len(phrase)]) == phrase:
                    span = (sentence["sent_id"], tuple(range(start + 1, start + len(phrase) + 1)))
                    predicted_spans.add(span)
                    predicted_labeled.add((*span, category_mapping[category]))

    gold_spans = set()
    gold_labeled = set()
    gappy_gold = set()
    seen_gold = set()
    unseen_gold = set()
    for sentence in datasets["test"]:
        for occurrence in sentence["smwes"].values():
            category = occurrence["lexcat"]
            if category not in target_categories:
                continue
            span = (sentence["sent_id"], tuple(occurrence["toknums"]))
            gold_spans.add(span)
            gold_labeled.add((*span, category_mapping[category]))
            if max(occurrence["toknums"]) - min(occurrence["toknums"]) + 1 > len(occurrence["toknums"]):
                gappy_gold.add(span)
            (seen_gold if occurrence["lexlemma"].casefold() in train_types else unseen_gold).add(span)

    return {
        "algorithm": "casefolded contiguous token-lemma matching of train target types; most frequent train category with lexical tie-break",
        "train_target_types": len(best_category),
        "exact_span": prf(predicted_spans, gold_spans),
        "exact_span_and_category": prf(predicted_labeled, gold_labeled),
        "discontinuous_exact_span": prf(predicted_spans & gappy_gold, gappy_gold),
        "seen_exact_span_recall": {
            "matched": len(predicted_spans & seen_gold),
            "gold": len(seen_gold),
            "value": round(len(predicted_spans & seen_gold) / len(seen_gold), 6)
            if seen_gold else None,
        },
        "unseen_exact_span_recall": {
            "matched": len(predicted_spans & unseen_gold),
            "gold": len(unseen_gold),
            "value": round(len(predicted_spans & unseen_gold) / len(unseen_gold), 6)
            if unseen_gold else None,
        },
    }


def dependency_arc(tokens, member_indexes, relations):
    head_index = member_indexes[0]
    head_number = head_index + 1
    for member_index in member_indexes[1:]:
        member = tokens[member_index]
        if (
            member.get("head") == head_number
            and member.get("deprel") in relations["head_to_member"]
        ):
            return {
                "head_token_number": head_number,
                "dependent_token_number": member_index + 1,
                "direction": "head_to_member",
                "relation": member["deprel"],
            }
        head = tokens[head_index]
        if (
            head.get("head") == member_index + 1
            and head.get("deprel") in relations["member_to_head"]
        ):
            return {
                "head_token_number": member_index + 1,
                "dependent_token_number": head_number,
                "direction": "member_to_head",
                "relation": head["deprel"],
            }
    return None


def gap_predictions(sentences, patterns, category_mapping, rules, require_dependency):
    by_first_lemma = {}
    for phrase, (_, category) in patterns.items():
        by_first_lemma.setdefault(phrase[0], []).append((phrase, category))

    predictions = {}
    maximum_gap = rules["maximum_intervening_tokens_per_member_pair"]
    for sentence in sentences:
        tokens = sentence["toks"]
        lemmas = []
        for token in tokens:
            if not isinstance(token.get("lemma"), str):
                raise ValueError(f"Missing lemma in {sentence['sent_id']}.")
            lemmas.append(token["lemma"].casefold())
        for start, lemma in enumerate(lemmas):
            for phrase, category in by_first_lemma.get(lemma, []):
                matches = [(start,)]
                for wanted in phrase[1:]:
                    matches = [
                        match + (index,)
                        for match in matches
                        for index in range(
                            match[-1] + 1,
                            min(len(tokens), match[-1] + maximum_gap + 2),
                        )
                        if lemmas[index] == wanted
                    ]
                for match in matches:
                    arc = dependency_arc(
                        tokens,
                        match,
                        rules["allowed_dependency_relations"][category],
                    )
                    if require_dependency and arc is None:
                        continue
                    member_numbers = tuple(index + 1 for index in match)
                    key = (sentence["sent_id"], member_numbers)
                    prediction = {
                        "sentence_id": sentence["sent_id"],
                        "member_token_numbers": list(member_numbers),
                        "category": category_mapping[category],
                        "rule_ids": ["GD-LEMMA-WINDOW"]
                        + (["GD-DIRECT-DEPENDENCY"] if require_dependency else []),
                        "evidence": {
                            "lemma_pattern": list(phrase),
                            "dependency_arc": arc,
                        },
                    }
                    previous = predictions.get(key)
                    if previous is None or prediction["category"] < previous["category"]:
                        predictions[key] = prediction
    return [predictions[key] for key in sorted(predictions)]


def score_gap_predictions(sentences, predictions, category_mapping, train_types):
    target_categories = set(category_mapping)
    predicted_spans = {
        (item["sentence_id"], tuple(item["member_token_numbers"]))
        for item in predictions
    }
    predicted_labeled = {
        (
            item["sentence_id"],
            tuple(item["member_token_numbers"]),
            item["category"],
        )
        for item in predictions
    }
    predicted_gappy = {
        span
        for span in predicted_spans
        if span[1][-1] - span[1][0] + 1 > len(span[1])
    }
    gold_spans = set()
    gold_labeled = set()
    gappy_gold = set()
    seen_gold = set()
    unseen_gold = set()
    for sentence in sentences:
        for occurrence in sentence["smwes"].values():
            category = occurrence["lexcat"]
            if category not in target_categories:
                continue
            span = (sentence["sent_id"], tuple(occurrence["toknums"]))
            gold_spans.add(span)
            gold_labeled.add((*span, category_mapping[category]))
            if span[1][-1] - span[1][0] + 1 > len(span[1]):
                gappy_gold.add(span)
            target = seen_gold if occurrence["lexlemma"].casefold() in train_types else unseen_gold
            target.add(span)
    return {
        "prediction_count": len(predicted_spans),
        "exact_span": prf(predicted_spans, gold_spans),
        "exact_span_and_category": prf(predicted_labeled, gold_labeled),
        "discontinuous_exact_span": prf(predicted_gappy, gappy_gold),
        "seen_exact_span_recall": {
            "matched": len(predicted_spans & seen_gold),
            "gold": len(seen_gold),
            "value": round(len(predicted_spans & seen_gold) / len(seen_gold), 6)
            if seen_gold else None,
        },
        "unseen_exact_span_recall": {
            "matched": len(predicted_spans & unseen_gold),
            "gold": len(unseen_gold),
            "value": round(len(predicted_spans & unseen_gold) / len(unseen_gold), 6)
            if unseen_gold else None,
        },
    }


def gap_dependency_baseline(datasets, category_mapping, rules, include_audit=False):
    target_categories = set(category_mapping)
    maximum_gap = rules["maximum_intervening_tokens_per_member_pair"]
    if isinstance(maximum_gap, bool) or not isinstance(maximum_gap, int) or maximum_gap < 0:
        raise ValueError("maximum_intervening_tokens_per_member_pair must be a nonnegative integer.")
    minimum_count = rules["minimum_train_dependency_arc_count"]
    if isinstance(minimum_count, bool) or not isinstance(minimum_count, int) or minimum_count < 1:
        raise ValueError("minimum_train_dependency_arc_count must be a positive integer.")
    patterns, train_types = training_patterns(datasets, target_categories)
    active_rules = dict(rules)
    active_rules["allowed_dependency_relations"] = training_dependency_relations(
        datasets, target_categories, minimum_count
    )
    report = {
        "algorithm": "ordered train-type lemma matching within a frozen gap, filtered by one direct first-member dependency arc; most frequent train category with lexical tie-break",
        "rules_version": rules["rules_version"],
        "train_target_types": len(patterns),
        "derived_allowed_dependency_relations": active_rules["allowed_dependency_relations"],
    }
    audits = {}
    for split, report_key in (("dev", "development"), ("test", "exposed_test")):
        ablation = gap_predictions(
            datasets[split], patterns, category_mapping, active_rules, False
        )
        selected = gap_predictions(
            datasets[split], patterns, category_mapping, active_rules, True
        )
        report[report_key] = {
            "lemma_window_ablation": score_gap_predictions(
                datasets[split], ablation, category_mapping, train_types
            ),
            "gap_dependency": score_gap_predictions(
                datasets[split], selected, category_mapping, train_types
            ),
        }
        audits[report_key] = selected
    if include_audit:
        report["prediction_audit"] = audits
    return report


def inspect_checkout(checkout, profile):
    datasets = {}
    for split, artifact in profile["artifacts"].items():
        path = checkout / artifact["path"]
        if path.stat().st_size != artifact["size_bytes"] or sha256(path) != artifact["sha256"]:
            raise ValueError(f"STREUSLE artifact identity mismatch: {split}.")
        datasets[split] = json.loads(path.read_text(encoding="utf-8"))
    report = summarize_all(datasets, set(profile["projection"]["category_mapping"]))
    return report, datasets


def self_check():
    sentence = lambda sent_id, tokens, smwes: {
        "sent_id": sent_id, "toks": [{"lemma": token} for token in tokens], "smwes": smwes
    }
    datasets = {
        "train": [sentence("train-1", ["take", "in"], {
            "1": {"lexcat": "V.VPC.full", "lexlemma": "take in", "toknums": [1, 2]},
            "2": {"lexcat": "N", "lexlemma": "test item", "toknums": [1, 2]},
        })],
        "dev": [sentence("dev-1", ["take", "it", "in"], {
            "1": {"lexcat": "V.VPC.full", "lexlemma": "take in", "toknums": [1, 3]},
        })],
        "test": [sentence("test-1", ["take", "in"], {
            "1": {"lexcat": "V.VPC.full", "lexlemma": "TAKE IN", "toknums": [1, 2]}
        })],
    }
    for split in datasets.values():
        for sentence_item in split:
            for index, token in enumerate(sentence_item["toks"]):
                token.update({"#": index + 1, "head": 0 if index == 0 else 1, "deprel": "root" if index == 0 else "compound:prt"})
    report = summarize_all(datasets, {"V.VPC.full", "V.VPC.semi", "V.VID"})
    assert report["train"]["target_occurrences"] == 1
    assert report["train"]["discontinuous_target_occurrences"] == 0
    assert report["dev"]["discontinuous_target_occurrences"] == 1
    assert report["test"]["types_seen_in_train"] == 1
    baseline = surface_baseline(
        datasets, {"V.VPC.full": "VPC.full", "V.VPC.semi": "VPC.semi", "V.VID": "VID"}
    )
    assert baseline["exact_span"]["f1"] == 1
    assert baseline["discontinuous_exact_span"]["recall"] is None
    rules = {
        "rules_version": "self-check",
        "maximum_intervening_tokens_per_member_pair": 1,
        "minimum_train_dependency_arc_count": 1,
    }
    gap_report = gap_dependency_baseline(
        datasets,
        {"V.VPC.full": "VPC.full", "V.VPC.semi": "VPC.semi", "V.VID": "VID"},
        rules,
        include_audit=True,
    )
    assert gap_report["development"]["gap_dependency"]["discontinuous_exact_span"]["recall"] == 1
    audit = gap_report["prediction_audit"]["development"][0]
    assert audit["rule_ids"] == ["GD-LEMMA-WINDOW", "GD-DIRECT-DEPENDENCY"]
    assert audit["evidence"]["dependency_arc"]["relation"] == "compound:prt"
    return {"self_check": "pass"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, nargs="?")
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--gap-baseline-record", type=Path, default=DEFAULT_GAP_BASELINE)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--surface-baseline", action="store_true")
    parser.add_argument("--gap-dependency-baseline", action="store_true")
    parser.add_argument("--prediction-audit", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_check:
            report = self_check()
        else:
            if args.checkout is None:
                raise ValueError("A STREUSLE 5.0 checkout path is required.")
            profile = json.loads(args.profile.read_text(encoding="utf-8"))
            profile_report, datasets = inspect_checkout(args.checkout, profile)
            surface_report = surface_baseline(
                datasets, profile["projection"]["category_mapping"]
            ) if args.surface_baseline else None
            gap_record = None
            gap_report = None
            if args.gap_dependency_baseline:
                gap_record = json.loads(args.gap_baseline_record.read_text(encoding="utf-8"))
                if sha256(args.profile) != gap_record["source"]["profile_sha256"]:
                    raise ValueError("STREUSLE profile identity does not match the gap/dependency baseline record.")
                gap_report = gap_dependency_baseline(
                    datasets,
                    profile["projection"]["category_mapping"],
                    gap_record["rules"],
                    args.prediction_audit,
                )
            if args.check and profile_report != profile["expected_report"]:
                raise ValueError("STREUSLE projection does not match expected_report.")
            if args.check and surface_report is not None and surface_report != profile.get("expected_surface_baseline"):
                raise ValueError("STREUSLE surface baseline does not match expected_surface_baseline.")
            gap_summary = (
                {key: value for key, value in gap_report.items() if key != "prediction_audit"}
                if gap_report is not None else None
            )
            if args.check and gap_summary is not None and gap_summary != gap_record["expected_report"]:
                raise ValueError("STREUSLE gap/dependency baseline does not match its frozen record.")
            if surface_report is None and gap_report is None:
                report = profile_report
            else:
                report = {"profile_report": profile_report}
                if surface_report is not None:
                    report["surface_baseline"] = surface_report
                if gap_report is not None:
                    report["gap_dependency_baseline"] = gap_report
    except (AssertionError, OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
