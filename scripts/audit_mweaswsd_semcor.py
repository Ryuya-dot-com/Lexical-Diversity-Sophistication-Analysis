#!/usr/bin/env python3
"""Reproduce aggregate MWEasWSD/SemCor reuse-audit observations."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import tarfile
from zipfile import ZipFile


EXPECTED = {
    "manual": (3575865, "b3ab0995cb5d9d9b2be2361be2ac094ba36bba18e9f49799e0d006bf4d6edd37"),
    "augmented": (117015352, "7b38aac490ff990f3eba014d141497298d2d638d27f8e91c8cec53a28231eb7e"),
    "oewn": (9986555, "7d749f6e2c39e6970e4997839dcf6e42fd281f3c2fae0171d2192bae8cfa4b51"),
    "cili_sense_map": (6637176, "446a94e3fdf7d5b6b9604797ab99c727e15856a46d57307a23bf2cea1da418f2"),
    "cili_ili_map": (2124416, "13b6741395a8bdf20e5a19686ffa49167653696d4f523db17a79dce3211a6627"),
    "semcor": (4074509, "a8000014d6fc864f8bd9d83c62be601151cadd617c6554a39a1ad38b4b3f017b"),
}
NEGATIVE = "<NOT_AN_MWE>"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_artifacts(paths: dict[str, Path]) -> dict:
    result = {}
    for name, path in paths.items():
        expected_size, expected_hash = EXPECTED[name]
        actual = {"size_bytes": path.stat().st_size, "sha256": file_sha256(path)}
        if (actual["size_bytes"], actual["sha256"]) != (expected_size, expected_hash):
            raise ValueError(f"{name} does not match the audited artifact")
        result[name] = actual
    return result


def normalize_cili_sense_key(key: str) -> str:
    """Bridge NLTK decimal lexical IDs to CILI's hexadecimal representation."""
    lemma, tail = key.split("%", 1)
    parts = tail.split(":")
    for index in (2, 4):
        if index < len(parts) and parts[index].isdigit():
            parts[index] = f"{int(parts[index]):02x}"
    return lemma.casefold() + "%" + ":".join(parts).casefold()


def read_manual(path: Path) -> tuple[dict, dict]:
    rows = []
    top_fields, annotation_fields = set(), set()
    for line in path.open(encoding="utf-8"):
        source = json.loads(line)
        annotation = source["_annotation"]
        sense = annotation["sense_data"]
        top_fields.update(source)
        annotation_fields.update(annotation)
        rows.append({
            "answer": source["answer"],
            "text": annotation["sentence_text"],
            "indices": tuple(annotation["word_indices"]),
            "lemma": sense["lemma"],
            "pos": sense["pos"],
            "sense": sense["gold_sense"],
            "status": annotation["status"],
            "selected": tuple(source.get("accept", [])),
            "options": tuple(option["id"] for option in source["options"]),
        })

    accepted_by_key = defaultdict(list)
    all_answers_by_key = defaultdict(set)
    first = {}
    for row in rows:
        key = (row["text"], row["indices"])
        all_answers_by_key[key].add(row["answer"])
        if row["answer"] == "accept":
            accepted_by_key[key].append(row)
            first.setdefault(key, row)

    duplicate_keys = {key: group for key, group in accepted_by_key.items() if len(group) > 1}
    verbs = [row for row in first.values() if row["pos"] == "v"]
    positive_verbs = [row for row in verbs if row["sense"] != NEGATIVE]
    negative_verbs = [row for row in verbs if row["sense"] == NEGATIVE]
    positive_by_lemma = defaultdict(list)
    for row in positive_verbs:
        positive_by_lemma[row["lemma"]].append(row)
    observed_polysemy = {
        lemma: group
        for lemma, group in positive_by_lemma.items()
        if len({row["sense"] for row in group}) > 1
    }
    take_in = [row for row in verbs if row["lemma"] == "take_in"]

    split_names = {"split", "set", "partition", "fold", "document_id", "doc_id"}
    category_names = {"category", "mwe_category", "parseme_category", "vmwe_category"}
    identity_names = {"annotator", "annotator_id", "session", "session_id", "reviewer"}
    fields = top_fields | annotation_fields
    observations = {
        "raw_rows": len(rows),
        "answer_counts": dict(sorted(Counter(row["answer"] for row in rows).items())),
        "annotation_status_counts": dict(sorted(Counter(row["status"] for row in rows).items())),
        "unique_accepted_sentence_span_keys": len(first),
        "accepted_wordnet_sense_rows": sum(row["sense"] != NEGATIVE for row in first.values()),
        "accepted_not_an_mwe_rows": sum(row["sense"] == NEGATIVE for row in first.values()),
        "duplicate_accepted_rows_removed_by_first_wins": sum(len(group) - 1 for group in duplicate_keys.values()),
        "duplicate_accepted_keys": len(duplicate_keys),
        "conflicting_duplicate_accepted_keys": sum(
            len({row["sense"] for row in group}) > 1 for group in duplicate_keys.values()
        ),
        "accept_reject_overlap_keys": sum(answers == {"accept", "reject"} for answers in all_answers_by_key.values()),
        "accepted_selection_mismatches": sum(
            row["selected"] != (row["sense"],) for row in rows if row["answer"] == "accept"
        ),
        "split_fields": sorted(fields & split_names),
        "category_fields": sorted(fields & category_names),
        "annotator_identity_fields": sorted(fields & identity_names),
        "verb_form_proxy": {
            "rows": len(verbs),
            "positive_rows": len(positive_verbs),
            "negative_rows": len(negative_verbs),
            "types": len({row["lemma"] for row in verbs}),
            "positive_types": len(positive_by_lemma),
            "negative_types": len({row["lemma"] for row in negative_verbs}),
            "types_with_positive_and_negative_rows": len(
                set(positive_by_lemma) & {row["lemma"] for row in negative_verbs}
            ),
            "positive_rows_with_multiple_wordnet_candidates": sum(
                len([option for option in row["options"] if option != NEGATIVE]) > 1
                for row in positive_verbs
            ),
            "types_with_multiple_observed_positive_senses": len(observed_polysemy),
            "rows_in_multiple_observed_positive_sense_types": sum(
                len(group) for group in observed_polysemy.values()
            ),
            "multiple_observed_positive_sense_types": [
                {
                    "lemma": lemma,
                    "rows": len(group),
                    "observed_sense_count": len({row["sense"] for row in group}),
                }
                for lemma, group in sorted(observed_polysemy.items())
            ],
            "continuous_rows": sum(
                max(row["indices"]) - min(row["indices"]) + 1 == len(row["indices"])
                for row in verbs
            ),
            "discontinuous_rows": sum(
                max(row["indices"]) - min(row["indices"]) + 1 != len(row["indices"])
                for row in verbs
            ),
        },
        "take_in": {
            "rows": len(take_in),
            "positive_rows": sum(row["sense"] != NEGATIVE for row in take_in),
            "negative_rows": sum(row["sense"] == NEGATIVE for row in take_in),
            "observed_positive_sense_count": len(
                {row["sense"] for row in take_in if row["sense"] != NEGATIVE}
            ),
        },
    }
    return observations, first


def read_augmented(path: Path, accepted: dict) -> dict:
    counts = Counter()
    text_counts = Counter()
    manual_groups = {}
    sentence_count = 0
    for line in path.open(encoding="utf-8"):
        sentence = json.loads(line)
        sentence_count += 1
        text_counts[sentence["text"]] += 1
        groups = {}
        for index, word in enumerate(sentence["words"]):
            mwe = word.get("mwe")
            if mwe is not None:
                groups.setdefault(mwe["idx"], {"mwe": mwe, "indices": []})["indices"].append(index)
        for group in groups.values():
            mwe = group["mwe"]
            meta = mwe.get("meta") or {}
            if meta.get("annotated") and not meta.get("auto"):
                kind = "manual"
                manual_groups[(sentence["text"], tuple(group["indices"]))] = mwe["gold_sense"]
            elif meta.get("auto"):
                kind = "synthetic"
            else:
                kind = "semcor_original"
            polarity = "negative" if mwe["gold_sense"] == NEGATIVE else "positive"
            counts[f"{kind}_{polarity}"] += 1

    missing = set(accepted) - set(manual_groups)
    mismatch = sum(
        manual_groups[key] != row["sense"]
        for key, row in accepted.items()
        if key in manual_groups
    )
    final_positive = counts["semcor_original_positive"] + counts["manual_positive"]
    final_negative = counts["manual_negative"] + counts["synthetic_negative"]
    return {
        "sentence_rows": sentence_count,
        "duplicate_sentence_text_values": sum(count > 1 for count in text_counts.values()),
        "maximum_sentence_text_multiplicity": max(text_counts.values()),
        "accepted_keys_on_duplicated_sentence_text": sum(
            text_counts[key[0]] > 1 for key in accepted
        ),
        "group_counts": dict(sorted(counts.items())),
        "manual_groups": len(manual_groups),
        "accepted_keys_missing_after_application": len(missing),
        "applied_manual_label_mismatches": mismatch,
        "inferred_application_collisions_in_published_artifact": len(missing),
        "paper_table_2_comparison": {
            "artifact_final_positive": final_positive,
            "paper_final_positive": 12907,
            "difference": final_positive - 12907,
            "artifact_final_negative": final_negative,
            "paper_final_negative": 14688,
            "difference_negative": final_negative - 14688,
        },
    }


def mapping_observations(manual: dict, oewn_path: Path, sense_map_path: Path, ili_map_path: Path) -> dict:
    normalized_source = defaultdict(set)
    for line in sense_map_path.open(encoding="utf-8"):
        synset, sense = line.rstrip("\n").split("\t")
        normalized_source[normalize_cili_sense_key(sense)].add(synset)
    source_ili = {}
    for line in ili_map_path.open(encoding="utf-8"):
        ili, synset = line.rstrip("\n").split("\t")
        source_ili[synset] = ili

    oewn_senses, oewn_synsets = {}, {}
    ili_to_oewn = defaultdict(list)
    with ZipFile(oewn_path) as archive:
        for name in archive.namelist():
            if name.startswith("entries-") and name.endswith(".json"):
                for lemma, poses in json.loads(archive.read(name)).items():
                    for pos, entry in poses.items():
                        for sense in entry.get("sense", []):
                            oewn_senses[sense["id"]] = (lemma, pos, sense["synset"])
            elif name.startswith(("noun.", "verb.", "adv.", "adj.")) and name.endswith(".json"):
                for synset_id, synset in json.loads(archive.read(name)).items():
                    oewn_synsets[synset_id] = synset
                    if synset.get("ili"):
                        ili_to_oewn[synset["ili"]].append(synset_id)

    row_status = Counter()
    sense_status = {}
    details = defaultdict(lambda: {"occurrences": 0})
    for row in manual.values():
        key = row["sense"]
        if key == NEGATIVE:
            continue
        source_synsets = normalized_source.get(normalize_cili_sense_key(key), set())
        source_synset = next(iter(source_synsets)) if len(source_synsets) == 1 else None
        ili = source_ili.get(source_synset)
        exact = oewn_senses.get(key)
        targets = ili_to_oewn.get(ili, [])
        if exact:
            oewn_ili = oewn_synsets[exact[2]].get("ili")
            if ili and oewn_ili == ili:
                status = "exact_same_ili"
            elif not ili or not oewn_ili:
                status = "exact_ili_unverified"
            else:
                status = "exact_ili_mismatch"
        elif len(targets) == 1:
            normalized_lemma = row["lemma"].replace("_", " ").casefold()
            retained = normalized_lemma in {
                member.casefold() for member in oewn_synsets[targets[0]]["members"]
            }
            status = "synset_only_lexeme_retained" if retained else "synset_only_lexeme_removed"
        elif len(targets) > 1:
            status = "synset_ambiguous"
        elif ili:
            status = "concept_absent_from_oewn_2025"
        else:
            status = "cili_mapping_unavailable"
        row_status[status] += 1
        sense_status[key] = status
        details[key].update({"lemma": row["lemma"], "pos": row["pos"], "status": status})
        details[key]["occurrences"] += 1

    verb_rows = [row for row in manual.values() if row["pos"] == "v" and row["sense"] != NEGATIVE]
    non_lossless = [
        {
            "sense_id": key,
            "lemma": value["lemma"],
            "occurrences": value["occurrences"],
            "status": value["status"],
        }
        for key, value in sorted(details.items())
        if value["pos"] == "v" and value["status"] != "exact_same_ili"
    ]
    return {
        "normalization": "case-fold lemma; convert NLTK decimal lexical/head IDs to CILI two-digit hexadecimal IDs",
        "all_positive_rows": dict(sorted(row_status.items())),
        "all_positive_source_senses": dict(sorted(Counter(sense_status.values()).items())),
        "verb_positive_rows": dict(sorted(Counter(sense_status[row["sense"]] for row in verb_rows).items())),
        "verb_lossless_exact_same_ili": {
            "numerator": sum(sense_status[row["sense"]] == "exact_same_ili" for row in verb_rows),
            "denominator": len(verb_rows),
        },
        "verb_exact_sense_id": {
            "numerator": sum(row["sense"] in oewn_senses for row in verb_rows),
            "denominator": len(verb_rows),
        },
        "non_lossless_verb_senses": non_lossless,
    }


def semcor_rights_observations(path: Path) -> dict:
    with tarfile.open(path, "r:gz") as archive:
        names = set(archive.getnames())
        readme = archive.extractfile("semcor3.0/README.semcor3.0").read().decode("utf-8")
        license_text = archive.extractfile("semcor3.0/LICENSE").read().decode("utf-8")
    return {
        "has_readme": "semcor3.0/README.semcor3.0" in names,
        "has_license": "semcor3.0/LICENSE" in names,
        "readme_identifies_semcor_1_6_as_princeton_property": "property of Princeton University" in readme,
        "readme_grants_use_copy_modify_and_distribute": "permission to use, copy, modify and distribute" in readme,
        "license_requires_notice_on_all_copies": "same appear on ALL copies" in license_text,
    }


def build(args: argparse.Namespace) -> dict:
    paths = {
        "manual": args.manual,
        "augmented": args.augmented,
        "oewn": args.oewn,
        "cili_sense_map": args.cili_sense_map,
        "cili_ili_map": args.cili_ili_map,
        "semcor": args.semcor,
    }
    artifacts = checked_artifacts(paths)
    manual, accepted = read_manual(args.manual)
    return {
        "artifacts": artifacts,
        "manual": manual,
        "augmented": read_augmented(args.augmented, accepted),
        "mapping": mapping_observations(accepted, args.oewn, args.cili_sense_map, args.cili_ili_map),
        "semcor_rights_artifact": semcor_rights_observations(args.semcor),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manual", type=Path)
    parser.add_argument("augmented", type=Path)
    parser.add_argument("oewn", type=Path)
    parser.add_argument("cili_sense_map", type=Path)
    parser.add_argument("cili_ili_map", type=Path)
    parser.add_argument("semcor", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    observations = build(args)
    if args.check:
        expected = json.loads(args.check.read_text(encoding="utf-8"))["computed_observations"]
        if observations != expected:
            raise SystemExit("Computed MWEasWSD/SemCor observations differ from the audit record.")
    else:
        print(json.dumps(observations, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
