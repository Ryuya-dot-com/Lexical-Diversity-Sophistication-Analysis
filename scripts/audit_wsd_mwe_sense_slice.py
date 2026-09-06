#!/usr/bin/env python3
"""Audit the multiword-verb slice of the standard English WSD framework."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from audit_mweaswsd_semcor import file_sha256, normalize_cili_sense_key


EXPECTED = {
    "framework": (165655083, "d71c4d3e93d265cb31e032ab3db8c0f9186af95a4c7a9a637d66dfef81dfbf47"),
    "streusle_train": (16845570, "36aef0205a6e2e154b681d7520858693a264d3c40ba7d97c089345bbd1149a22"),
    "streusle_dev": (2050638, "56cc1783962ce8c9f06b7649ffdccb48cea14ee7e4a8be2e35214ffc71303e9a"),
    "streusle_test": (2051895, "f8144e6227db2e845cda4aa832f8d5644cb40b9e743d1dbe05663dd687d2c70c"),
    "oewn": (9986555, "7d749f6e2c39e6970e4997839dcf6e42fd281f3c2fae0171d2192bae8cfa4b51"),
    "cili_sense_map": (6637176, "446a94e3fdf7d5b6b9604797ab99c727e15856a46d57307a23bf2cea1da418f2"),
    "cili_ili_map": (2124416, "13b6741395a8bdf20e5a19686ffa49167653696d4f523db17a79dce3211a6627"),
}
EVAL_SETS = ("senseval2", "senseval3", "semeval2007", "semeval2013", "semeval2015")
TARGET_CATEGORIES = {"V.VPC.full", "V.VPC.semi", "V.VID"}
ROOT = "WSD_Evaluation_Framework"


def checked_artifacts(paths: dict[str, Path]) -> dict:
    result = {}
    for name, path in paths.items():
        size, digest = EXPECTED[name]
        actual = {"size_bytes": path.stat().st_size, "sha256": file_sha256(path)}
        if (actual["size_bytes"], actual["sha256"]) != (size, digest):
            raise ValueError(f"{name} does not match the audited artifact")
        result[name] = actual
    return result


def member_sha256(archive: ZipFile, name: str) -> str:
    return hashlib.sha256(archive.read(name)).hexdigest()


def read_wsd_rows(archive: ZipFile, dataset: str, training: bool = False) -> tuple[list[dict], dict]:
    if training:
        stem = f"{ROOT}/Training_Corpora/SemCor/semcor"
    else:
        stem = f"{ROOT}/Evaluation_Datasets/{dataset}/{dataset}"
    xml_name, gold_name = stem + ".data.xml", stem + ".gold.key.txt"
    gold = {}
    for line in archive.read(gold_name).decode("utf-8").splitlines():
        parts = line.split()
        gold[parts[0]] = parts[1:]

    rows = []
    corpus = ET.fromstring(archive.read(xml_name))
    for text in corpus.findall("text"):
        for sentence in text.findall("sentence"):
            for instance in sentence.findall("instance"):
                lemma = instance.attrib["lemma"].casefold()
                if instance.attrib["pos"] == "VERB" and "_" in lemma:
                    rows.append({
                        "dataset": dataset,
                        "document": text.attrib["id"],
                        "sentence": sentence.attrib["id"],
                        "instance": instance.attrib["id"],
                        "lemma": lemma,
                        "surface_member_text": instance.text or "",
                        "senses": gold[instance.attrib["id"]],
                    })
    return rows, {
        "xml": {"path": xml_name, "sha256": member_sha256(archive, xml_name)},
        "gold": {"path": gold_name, "sha256": member_sha256(archive, gold_name)},
    }


def form_groups(rows: list[dict]) -> dict[str, list[dict]]:
    groups = defaultdict(list)
    for row in rows:
        groups[row["lemma"]].append(row)
    return groups


def sense_summary(rows: list[dict], include_contrasts: bool = False) -> dict:
    groups = form_groups(rows)
    cross_occurrence = {
        lemma: group
        for lemma, group in groups.items()
        if len(group) > 1 and len({sense for row in group for sense in row["senses"]}) > 1
    }
    result = {
        "rows": len(rows),
        "types": len(groups),
        "documents": len({(row["dataset"], row["document"]) for row in rows}),
        "rows_with_multiple_acceptable_gold_senses": sum(len(row["senses"]) > 1 for row in rows),
        "forms_with_cross_occurrence_sense_contrast": len(cross_occurrence),
        "rows_in_cross_occurrence_sense_contrast_forms": sum(len(group) for group in cross_occurrence.values()),
    }
    if include_contrasts:
        result["cross_occurrence_sense_contrasts"] = [
            {
                "lemma": lemma,
                "rows": len(group),
                "observed_senses": len({sense for row in group for sense in row["senses"]}),
            }
            for lemma, group in sorted(cross_occurrence.items())
        ]
    return result


def read_streusle_types(paths: list[Path]) -> dict[str, Counter]:
    types = defaultdict(Counter)
    for path in paths:
        for sentence in json.loads(path.read_text(encoding="utf-8")):
            for mwe in sentence["smwes"].values():
                if mwe["lexcat"] in TARGET_CATEGORIES:
                    lemma = mwe["lexlemma"].casefold().replace(" ", "_")
                    types[lemma][mwe["lexcat"]] += 1
    return types


def target_summary(rows: list[dict], target_types: dict[str, Counter], include_contrasts: bool = False) -> dict:
    selected = [row for row in rows if row["lemma"] in target_types]
    summary = sense_summary(selected, include_contrasts)
    selected_types = {row["lemma"] for row in selected}
    unique = {lemma for lemma in selected_types if len(target_types[lemma]) == 1}
    summary.update({
        "rows_by_dataset": dict(sorted(Counter(row["dataset"] for row in selected).items())),
        "types_with_one_streusle_category": len(unique),
        "types_with_conflicting_streusle_categories": len(selected_types - unique),
        "rows_with_one_streusle_category": sum(row["lemma"] in unique for row in selected),
        "rows_with_conflicting_streusle_categories": sum(row["lemma"] not in unique for row in selected),
        "unique_category_types": dict(sorted(Counter(next(iter(target_types[lemma])) for lemma in unique).items())),
        "conflicting_category_types": [
            {"lemma": lemma, "categories": dict(sorted(target_types[lemma].items()))}
            for lemma in sorted(selected_types - unique)
        ],
    })
    return summary


def read_inventory(oewn_path: Path, sense_map_path: Path, ili_map_path: Path) -> dict:
    source_synsets = defaultdict(set)
    for line in sense_map_path.open(encoding="utf-8"):
        synset, sense = line.rstrip("\n").split("\t")
        source_synsets[normalize_cili_sense_key(sense)].add(synset)
    source_ili = {}
    for line in ili_map_path.open(encoding="utf-8"):
        ili, synset = line.rstrip("\n").split("\t")
        source_ili[synset] = ili

    senses, synsets, candidates = {}, {}, defaultdict(set)
    with ZipFile(oewn_path) as archive:
        for name in archive.namelist():
            if name.startswith("entries-") and name.endswith(".json"):
                for _, poses in json.loads(archive.read(name)).items():
                    for pos, entry in poses.items():
                        for sense in entry.get("sense", []):
                            senses[sense["id"]] = sense["synset"]
                            if pos == "v":
                                candidates[sense["id"].split("%", 1)[0].casefold()].add(sense["id"])
            elif name.startswith(("noun.", "verb.", "adv.", "adj.")) and name.endswith(".json"):
                synsets.update(json.loads(archive.read(name)))
    return {"source_synsets": source_synsets, "source_ili": source_ili,
            "senses": senses, "synsets": synsets, "candidates": candidates}


def mapping_status(sense: str, inventory: dict) -> str:
    source = inventory["source_synsets"].get(normalize_cili_sense_key(sense), set())
    source_synset = next(iter(source)) if len(source) == 1 else None
    source_ili = inventory["source_ili"].get(source_synset)
    target_synset = inventory["senses"].get(sense)
    if target_synset:
        target_ili = inventory["synsets"][target_synset].get("ili")
        if source_ili and source_ili == target_ili:
            return "exact_same_ili"
        if not source_ili or not target_ili:
            return "exact_ili_unverified"
        return "exact_ili_mismatch"
    return "exact_sense_id_absent"


def inventory_summary(rows: list[dict], inventory: dict) -> dict:
    statuses = Counter(mapping_status(sense, inventory) for row in rows for sense in row["senses"])
    candidate_counts = [len(inventory["candidates"].get(row["lemma"], ())) for row in rows]
    non_lossless = Counter(
        (row["lemma"], sense, mapping_status(sense, inventory))
        for row in rows
        for sense in row["senses"]
        if mapping_status(sense, inventory) != "exact_same_ili"
    )
    return {
        "gold_label_mapping_status": dict(sorted(statuses.items())),
        "non_lossless_gold_labels": [
            {"lemma": lemma, "sense": sense, "status": status, "rows": count}
            for (lemma, sense, status), count in sorted(non_lossless.items())
        ],
        "rows_with_all_gold_labels_exact_same_ili": sum(
            all(mapping_status(sense, inventory) == "exact_same_ili" for sense in row["senses"])
            for row in rows
        ),
        "rows_with_inventory_entry": sum(count > 0 for count in candidate_counts),
        "rows_with_at_least_two_inventory_senses": sum(count > 1 for count in candidate_counts),
        "candidate_sense_count_distribution": {
            str(count): frequency for count, frequency in sorted(Counter(candidate_counts).items())
        },
    }


def training_overlap(eval_rows: list[dict], train_rows: list[dict]) -> dict:
    train = form_groups(train_rows)
    seen_senses = {lemma: {sense for row in rows for sense in row["senses"]} for lemma, rows in train.items()}
    return {
        "rows_with_form_seen_in_semcor": sum(row["lemma"] in train for row in eval_rows),
        "rows_with_any_gold_sense_seen_in_semcor": sum(
            bool(set(row["senses"]) & seen_senses.get(row["lemma"], set())) for row in eval_rows
        ),
        "rows_with_all_gold_senses_seen_in_semcor": sum(
            set(row["senses"]) <= seen_senses.get(row["lemma"], set()) for row in eval_rows
        ),
    }


def candidate_polysemy_slice(rows: list[dict], target_types: dict[str, Counter], inventory: dict,
                              train_rows: list[dict]) -> dict:
    target = [row for row in rows if row["lemma"] in target_types]
    one_category = [row for row in target if len(target_types[row["lemma"]]) == 1]
    lossless = [
        row for row in one_category
        if all(mapping_status(sense, inventory) == "exact_same_ili" for sense in row["senses"])
    ]
    polysemous = [
        row for row in lossless
        if len(inventory["candidates"].get(row["lemma"], ())) >= 2
    ]
    polysemous_types = {row["lemma"] for row in polysemous}
    return {
        "selection_funnel": {
            "streusle_target_rows": len(target),
            "one_streusle_category_rows": len(one_category),
            "lossless_oewn_mapping_rows": len(lossless),
            "at_least_two_oewn_candidate_senses_rows": len(polysemous),
        },
        **sense_summary(polysemous, include_contrasts=True),
        "rows_by_dataset": dict(sorted(Counter(row["dataset"] for row in polysemous).items())),
        "development_rows": sum(row["dataset"] == "semeval2007" for row in polysemous),
        "source_test_rows": sum(row["dataset"] != "semeval2007" for row in polysemous),
        "source_test_status": "fixed_but_not_blinded_after_artifact_and_label_audit",
        "types_by_streusle_category": dict(sorted(Counter(
            next(iter(target_types[lemma])) for lemma in polysemous_types
        ).items())),
        "semcor_training_overlap": training_overlap(polysemous, train_rows),
    }


def build(args: argparse.Namespace) -> dict:
    paths = {
        "framework": args.framework,
        "streusle_train": args.streusle_train,
        "streusle_dev": args.streusle_dev,
        "streusle_test": args.streusle_test,
        "oewn": args.oewn,
        "cili_sense_map": args.cili_sense_map,
        "cili_ili_map": args.cili_ili_map,
    }
    artifacts = checked_artifacts(paths)
    with ZipFile(args.framework) as archive:
        train, train_members = read_wsd_rows(archive, "semcor", training=True)
        evaluation, evaluation_members = [], {}
        for dataset in EVAL_SETS:
            rows, members = read_wsd_rows(archive, dataset)
            evaluation.extend(rows)
            evaluation_members[dataset] = members
        names = archive.namelist()
        framework_rights = {
            "license_file_present": any(Path(name).name.casefold().startswith("license") for name in names),
            "readme_requests_framework_and_source_task_citations": (
                "If you use any of the datasets, please also cite the corresponding reference paper"
                in archive.read(f"{ROOT}/README").decode("utf-8")
            ),
            "explicit_redistribution_grant_in_readme": False,
        }

    target_types = read_streusle_types([
        args.streusle_train, args.streusle_dev, args.streusle_test
    ])
    inventory = read_inventory(args.oewn, args.cili_sense_map, args.cili_ili_map)
    target_train = [row for row in train if row["lemma"] in target_types]
    target_eval = [row for row in evaluation if row["lemma"] in target_types]
    take_in = [row for row in train if row["lemma"] == "take_in"]
    return {
        "artifacts": artifacts,
        "framework_members": {"semcor": train_members, "evaluation": evaluation_members},
        "framework_rights_artifact": framework_rights,
        "semcor_multiword_verbs": {
            **sense_summary(train),
            "target_type_intersection": target_summary(train, target_types),
            "take_in": {
                "rows": len(take_in),
                "documents": len({row["document"] for row in take_in}),
                "observed_senses": len({sense for row in take_in for sense in row["senses"]}),
            },
        },
        "evaluation_multiword_verbs": {
            **sense_summary(evaluation, include_contrasts=True),
            "rows_by_dataset": dict(sorted(Counter(row["dataset"] for row in evaluation).items())),
            "target_type_intersection": target_summary(evaluation, target_types, include_contrasts=True),
            "semcor_training_overlap": training_overlap(evaluation, train),
            "target_semcor_training_overlap": training_overlap(target_eval, target_train),
            "oewn_2025_mapping": inventory_summary(evaluation, inventory),
            "target_oewn_2025_mapping": inventory_summary(target_eval, inventory),
            "admissible_candidate_polysemy_slice": candidate_polysemy_slice(
                evaluation, target_types, inventory, target_train
            ),
            "take_in_rows": sum(row["lemma"] == "take_in" for row in evaluation),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in EXPECTED:
        parser.add_argument(name, type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    observations = build(args)
    if args.check:
        expected = json.loads(args.check.read_text(encoding="utf-8"))["computed_observations"]
        if observations != expected:
            raise SystemExit("Computed WSD MWE-sense observations differ from the audit record.")
    else:
        print(json.dumps(observations, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
