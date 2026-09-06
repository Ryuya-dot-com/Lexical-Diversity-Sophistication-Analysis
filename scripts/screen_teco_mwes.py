#!/usr/bin/env python3
"""Create a prose-free, outcome-blind MWE lead screen for TECO v1.1."""

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "resources/teco_v1_1_candidate_manifest.json"
OEWN = ROOT / "resources/oewn_2025_multiword_verbs.json"
CONTRACT = ROOT / "mwe_contract.json"
OUTPUT = ROOT / "resources/teco_v1_1_mwe_candidate_screen.json"
SENTENCE_END = re.compile(r"[.!?][\"')\]]*$")


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_word_rows(path, manifest):
    artifact = next(
        item for item in manifest["verified_files"] if item["name"] == "word info_v2.csv"
    )
    if path.stat().st_size != artifact["size_bytes"] or sha256(path) != artifact["sha256"]:
        raise ValueError("TECO word info file does not match the pinned v1.1 artifact.")
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        required = {"textid", "itemid", "position", "ia", "lemma", "lmost", "rmost"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("TECO word info file lacks required columns.")
        rows = list(reader)
    if len(rows) != manifest["design"]["word_items"]:
        raise ValueError("TECO word-item count differs from the pinned manifest.")
    return rows, artifact


def prepare_texts(rows, expected_texts):
    texts = defaultdict(list)
    seen = set()
    for row in rows:
        textid, itemid, position = map(int, (row["textid"], row["itemid"], row["position"]))
        if (textid, itemid) in seen:
            raise ValueError(f"Duplicate TECO word key: {textid}, {itemid}.")
        seen.add((textid, itemid))
        if row["lmost"] not in {"0", "1"} or row["rmost"] not in {"0", "1"}:
            raise ValueError(f"Invalid line-edge flag at item {itemid}.")
        texts[textid].append({
            "itemid": itemid,
            "position": position,
            "lemma": row["lemma"].casefold(),
            "sentence_end": bool(SENTENCE_END.search(row["ia"])),
            "lmost": int(row["lmost"]),
            "rmost": int(row["rmost"]),
        })
    if sorted(texts) != list(range(1, expected_texts + 1)):
        raise ValueError("TECO text IDs differ from the pinned manifest.")
    for textid, items in texts.items():
        items.sort(key=lambda item: item["position"])
        if [item["position"] for item in items] != list(range(1, len(items) + 1)):
            raise ValueError(f"Non-contiguous TECO positions in text {textid}.")
        line_id = sentence_id = 0
        for index, item in enumerate(items):
            if index == 0 or item["lmost"]:
                line_id += 1
            item["line_id"] = line_id
            item["sentence_id"] = sentence_id
            if item["sentence_end"]:
                sentence_id += 1
    return texts


def find_leads(texts, forms, maximum_gap=8):
    by_first = defaultdict(list)
    for canonical_form, sense_count in forms.items():
        members = tuple(canonical_form.casefold().split())
        by_first[members[0]].append((members, canonical_form, sense_count))
    leads = []
    for textid, items in texts.items():
        lemmas = [item["lemma"] for item in items]
        for start, first in enumerate(lemmas):
            for members, canonical_form, sense_count in by_first.get(first, []):
                length = len(members)
                exact = items[start:start + length]
                if (len(exact) == length and
                        tuple(lemmas[start:start + length]) == members and
                        len({item["sentence_id"] for item in exact}) == 1):
                    leads.append((
                        textid, "oewn_contiguous_lemma", canonical_form, sense_count,
                        exact, [],
                    ))
                if length != 2:
                    continue
                for end in range(start + 2, min(len(items), start + maximum_gap + 2)):
                    if items[end]["sentence_id"] != items[start]["sentence_id"]:
                        break
                    if lemmas[end] == members[1]:
                        leads.append((
                            textid, "oewn_two_member_gap_lemma", canonical_form,
                            sense_count, [items[start], items[end]], items[start + 1:end],
                        ))
    unique = {}
    for lead in leads:
        textid, source, canonical, _, members, _ = lead
        unique[textid, source, canonical, tuple(item["itemid"] for item in members)] = lead
    return sorted(unique.values(), key=lambda lead: (
        lead[0], lead[4][0]["position"], lead[4][-1]["position"], lead[2], lead[1]
    ))


def public_candidate(candidate_id, lead):
    textid, source, canonical, sense_count, members, gaps = lead
    line_ids = [item["line_id"] for item in members]
    return {
        "candidate_id": candidate_id,
        "textid": textid,
        "candidate_source": source,
        "canonical_form": canonical,
        "oewn_sense_count": sense_count,
        "occurrence_status": "candidate",
        "category": None,
        "idiomaticity": "not_assessed",
        "form_lookup_status": "not_attempted",
        "sense_lookup_status": "not_attempted",
        "sense_assignment_status": None,
        "member_itemids": [item["itemid"] for item in members],
        "gap_itemids": [item["itemid"] for item in gaps],
        "member_positions": [item["position"] for item in members],
        "gap_count": len(gaps),
        "member_line_ids": line_ids,
        "member_edge_flags": [
            {"lmost": bool(item["lmost"]), "rmost": bool(item["rmost"])}
            for item in members
        ],
        "crosses_inferred_line": len(set(line_ids)) > 1,
        "review_status": "unreviewed",
    }


def build(word_info_path, manifest_path, oewn_path, contract_path, maximum_gap=8):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows, artifact = load_word_rows(word_info_path, manifest)
    texts = prepare_texts(rows, manifest["design"]["passages_per_participant"])
    oewn = json.loads(oewn_path.read_text(encoding="utf-8"))
    leads = find_leads(texts, dict(oewn["rows"]), maximum_gap)
    counters = Counter(lead[1] for lead in leads)
    per_text = Counter(lead[0] for lead in leads)
    candidates = [
        public_candidate(f"teco-t{textid:02d}-c{index:03d}", lead)
        for textid in sorted(texts)
        for index, lead in enumerate((item for item in leads if item[0] == textid), 1)
    ]
    return {
        "screen_schema_version": "0.1.0",
        "screen_id": "teco-v1.1-oewn-outcome-blind-mwe-leads-v1",
        "generated_on": "2026-09-02",
        "status": "machine_candidates_only_human_occurrence_category_and_sense_review_pending",
        "inputs": {
            "teco_manifest_sha256": sha256(manifest_path),
            "teco_word_info_name": artifact["name"],
            "teco_word_info_size_bytes": artifact["size_bytes"],
            "teco_word_info_sha256": artifact["sha256"],
            "oewn_profile_id": oewn["identity"]["profile_id"],
            "oewn_profile_sha256": sha256(oewn_path),
            "mwe_contract_sha256": sha256(contract_path),
            "eye_movement_or_participant_outcome_files_read": [],
        },
        "candidate_generation": {
            "purpose": "high-recall desk-review leads, not automatic MWE annotation",
            "token_basis": "TECO-provided casefolded lemma and stable textid/itemid/position",
            "contiguous_rule": "exact OEWN multiword-verb lemma sequence within one inferred sentence",
            "gap_rule": (
                "two-member OEWN verb form in order within one inferred sentence, with "
                f"1-{maximum_gap} intervening TECO word items"
            ),
            "sentence_boundary_rule": "infer a boundary from sentence-final punctuation in local ia; do not export ia",
            "line_rule": (
                "increment an inferred line at each lmost=1 item; retain source lmost/rmost "
                "flags without assuming that their totals are paired"
            ),
            "excluded_inferences": [
                "MWE occurrence truth", "VPC.full, VPC.semi, or VID category",
                "idiomaticity", "contextual sense", "reader knowledge",
                "reading difficulty", "comprehension", "representative MWE prevalence",
            ],
            "known_recall_limits": [
                "no out-of-OEWN form generation",
                "no gapped search for forms with more than two members",
                f"no gap longer than {maximum_gap} word items",
                "no syntactic or contextual disambiguation",
                "TECO-provided lemma errors propagate to this screen",
                "punctuation-based sentence inference may split abbreviations or miss atypical boundaries",
            ],
            "source_text_exported": False,
            "surface_tokens_exported": False,
        },
        "roi_contract_frozen_before_outcome_join": {
            "primary_analysis_unit": (
                "member word observation joined by textid and itemid, with occurrence ID "
                "and member order retained"
            ),
            "primary_member_rule": "include reviewed MWE members only; do not silently include gaps",
            "gap_sensitivity": "analyze the first-through-last span, including gap items, only as a labelled sensitivity",
            "line_sensitivity": "retain each member's lmost/rmost and the derived crosses_inferred_line stratum",
            "permitted_occurrence_summaries": [
                "all_members_skipped and any_member_skipped, with missing retained",
                "sum of nfix and tfd over members only when every contributing value is observed",
            ],
            "not_whole_mwe_measures": [
                "sum of word-level ffd", "sum of word-level gd", "sum of word-level rpd",
                "sum of binary regin, refix, or reread indicators",
            ],
            "non_derivable_from_wordmeasure_v1": (
                "a fixation-sequence-defined whole-span first-pass or regression-path duration"
            ),
            "coverage_counting_rule": (
                "conventional word coverage keeps every orthographic word token; a reviewed "
                "MWE contributes one occurrence to the separate MWE-form denominator and never "
                "changes the word-token denominator"
            ),
        },
        "summary": {
            "text_count": len(texts),
            "word_item_count": len(rows),
            "candidate_count": len(leads),
            "contiguous_candidate_count": counters["oewn_contiguous_lemma"],
            "gapped_candidate_count": counters["oewn_two_member_gap_lemma"],
            "distinct_canonical_form_count": len({lead[2] for lead in leads}),
            "cross_line_candidate_count": sum(
                candidate["crosses_inferred_line"] for candidate in candidates
            ),
            "line_initial_item_count": sum(item["lmost"] for items in texts.values() for item in items),
            "line_final_item_count": sum(item["rmost"] for items in texts.values() for item in items),
            "candidate_count_by_text": [[textid, per_text[textid]] for textid in sorted(texts)],
        },
        "candidate_record_boundary": {
            "included": [
                "textid", "candidate ID", "OEWN canonical form and sense count",
                "member/gap item IDs and positions", "line IDs and edge flags",
                "unreviewed annotation states",
            ],
            "excluded": [
                "passage text", "surface tokens", "participant rows", "eye measures",
                "passage answers", "proficiency", "comprehension or difficulty outcomes",
            ],
        },
        "candidates": candidates,
    }


def self_check():
    rows = [
        {"textid": "1", "itemid": str(i), "position": str(i), "ia": surface,
         "lemma": lemma, "lmost": str(int(i in {1, 3})),
         "rmost": str(int(i in {2, 5}))}
        for i, (surface, lemma) in enumerate(
            [("They", "they"), ("took", "take"), ("it", "it"),
             ("in.", "in"), ("Stopped.", "stop")], 1
        )
    ]
    texts = prepare_texts(rows, 1)
    leads = find_leads(texts, {"take in": 17, "take it": 1}, maximum_gap=2)
    assert [(lead[1], lead[2]) for lead in leads] == [
        ("oewn_contiguous_lemma", "take it"),
        ("oewn_two_member_gap_lemma", "take in"),
    ]
    candidate = public_candidate("test", leads[1])
    assert candidate["member_itemids"] == [2, 4]
    assert candidate["gap_itemids"] == [3]
    assert candidate["crosses_inferred_line"]
    assert "ia" not in candidate and "lemma" not in candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("word_info", type=Path, nargs="?")
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--oewn", type=Path, default=OEWN)
    parser.add_argument("--contract", type=Path, default=CONTRACT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--maximum-gap", type=int, default=8, choices=range(1, 9))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("TECO MWE candidate-screen self-check: PASS")
        return
    if args.word_info is None:
        parser.error("word_info is required")
    result = build(
        args.word_info,
        args.manifest,
        args.oewn,
        args.contract,
        args.maximum_gap,
    )
    rendered = json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Generated TECO screen differs from {args.output}")
        print(f"TECO MWE candidate-screen verification: PASS ({args.output})")
    else:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
