#!/usr/bin/env python3
"""Verify the pinned external STREUSLE 5.0 VPC/VID benchmark profile."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = ROOT / "benchmarks/streusle_v5_vpc_vid.json"


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


def surface_baseline(datasets, category_mapping):
    target_categories = set(category_mapping)
    train_counts = Counter()
    train_types = set()
    for sentence in datasets["train"]:
        for occurrence in sentence["smwes"].values():
            if occurrence["lexcat"] in target_categories:
                phrase = tuple(occurrence["lexlemma"].casefold().split())
                train_counts[phrase, occurrence["lexcat"]] += 1
                train_types.add(occurrence["lexlemma"].casefold())

    # ponytail: contiguous exact-lemma baseline; add gap/dependency matching only
    # when this deliberately weak benchmark warrants the extra machinery.
    best_category = {}
    for phrase, category in train_counts:
        candidate = (train_counts[phrase, category], category)
        if candidate > best_category.get(phrase, (-1, "")):
            best_category[phrase] = candidate

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
        "train": [sentence("train-1", ["take", "it", "in"], {
            "1": {"lexcat": "V.VPC.full", "lexlemma": "take in", "toknums": [1, 3]},
            "2": {"lexcat": "N", "lexlemma": "test item", "toknums": [1, 2]},
        })],
        "dev": [sentence("dev-1", ["spill", "beans"], {
            "1": {"lexcat": "V.VID", "lexlemma": "spill beans", "toknums": [1, 2]}
        })],
        "test": [sentence("test-1", ["take", "in"], {
            "1": {"lexcat": "V.VPC.full", "lexlemma": "TAKE IN", "toknums": [1, 2]}
        })],
    }
    report = summarize_all(datasets, {"V.VPC.full", "V.VPC.semi", "V.VID"})
    assert report["train"]["target_occurrences"] == 1
    assert report["train"]["discontinuous_target_occurrences"] == 1
    assert report["dev"]["types_unseen_in_train"] == 1
    assert report["test"]["types_seen_in_train"] == 1
    baseline = surface_baseline(
        datasets, {"V.VPC.full": "VPC.full", "V.VPC.semi": "VPC.semi", "V.VID": "VID"}
    )
    assert baseline["exact_span"]["f1"] == 1
    assert baseline["discontinuous_exact_span"]["recall"] is None
    return {"self_check": "pass"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, nargs="?")
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--surface-baseline", action="store_true")
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
            baseline_report = surface_baseline(
                datasets, profile["projection"]["category_mapping"]
            ) if args.surface_baseline else None
            if args.check and profile_report != profile["expected_report"]:
                raise ValueError("STREUSLE projection does not match expected_report.")
            if args.check and baseline_report is not None and baseline_report != profile.get("expected_surface_baseline"):
                raise ValueError("STREUSLE surface baseline does not match expected_surface_baseline.")
            report = {
                "profile_report": profile_report,
                "surface_baseline": baseline_report,
            } if baseline_report is not None else profile_report
    except (AssertionError, OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
