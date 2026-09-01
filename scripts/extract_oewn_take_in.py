#!/usr/bin/env python3
"""Extract the reviewed ``take in`` verb-sense projection from OEWN 2025."""

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile


ARTIFACT_SHA256 = "7d749f6e2c39e6970e4997839dcf6e42fd281f3c2fae0171d2192bae8cfa4b51"
ENTRY = "take in"
PART_OF_SPEECH = "v"


def build_subset(source: Path) -> dict:
    if hashlib.sha256(source.read_bytes()).hexdigest() != ARTIFACT_SHA256:
        raise ValueError("OEWN artifact SHA-256 does not match the reviewed release asset.")

    with ZipFile(source) as archive:
        entry = json.loads(archive.read("entries-t.json"))[ENTRY][PART_OF_SPEECH]
        synsets = {}
        for name in archive.namelist():
            if name.startswith("verb.") and name.endswith(".json"):
                synsets.update(json.loads(archive.read(name)))

    senses = []
    for source_sense in entry["sense"]:
        synset_id = source_sense["synset"]
        synset = synsets[synset_id]
        if synset["partOfSpeech"] != PART_OF_SPEECH or ENTRY not in synset["members"]:
            raise ValueError(f"Unexpected OEWN synset for {source_sense['id']}.")
        senses.append({
            "sense_id": source_sense["id"],
            "synset_id": synset_id,
            "ili": synset["ili"],
            "definitions": synset["definition"],
            "synonyms": synset["members"],
            "synset_examples": synset.get("example", []),
            "entry_examples": source_sense.get("sent", []),
        })

    if len(senses) != 17 or len({sense["sense_id"] for sense in senses}) != 17:
        raise ValueError("Reviewed OEWN take in sense set must contain 17 unique senses.")

    return {
        "subset_schema_version": "1.0.0",
        "subset_id": "oewn-2025-take-in-v",
        "resource": {
            "id": "oewn",
            "title": "Open English WordNet",
            "version": "2025",
            "release_tag": "2025-edition",
            "release_date": "2025-12-31",
            "repository_commit": "dc343f2683279ecbb13fab4e2fd778d7b162d287",
            "artifact": "english-wordnet-2025-json.zip",
            "artifact_size_bytes": 9986555,
            "artifact_sha256": ARTIFACT_SHA256,
            "artifact_url": "https://github.com/globalwordnet/english-wordnet/releases/download/2025-edition/english-wordnet-2025-json.zip",
            "retrieved_on": "2026-09-01",
        },
        "license": {
            "oewn": "CC-BY-4.0",
            "underlying_wordnet": "WordNet License",
            "attribution": "Based on or incorporating elements of the Princeton University WordNet database and Open English WordNet 2025, copyright 2019-present The Open English WordNet Team.",
            "license_url": "https://github.com/globalwordnet/english-wordnet/blob/2025-edition/LICENSE.md",
            "wordnet_license_url": "https://github.com/globalwordnet/english-wordnet/blob/2025-edition/WNDB_License.txt",
            "local_notice": "resources/OEWN_WORDNET_NOTICE.txt",
            "no_endorsement": "No endorsement by Princeton University or the Open English WordNet Team is implied.",
        },
        "citation": {
            "authors": "John P. McCrae, Alexandre Rademaker, Francis Bond, Ewa Rudnicka, and Christiane Fellbaum",
            "year": 2019,
            "title": "English WordNet 2019 – An Open-Source WordNet for English",
            "url": "https://aclanthology.org/2019.gwc-1.31/",
        },
        "projection": {
            "entry_id": "take in#v",
            "lemma": ENTRY,
            "part_of_speech": PART_OF_SPEECH,
            "sense_count": len(senses),
            "included_fields": [
                "sense_id", "synset_id", "ili", "definitions", "synonyms",
                "synset_examples", "entry_examples",
            ],
            "omitted_source_fields": [
                "lexical_relations", "synset_relations", "subcategorization_frames",
            ],
            "modification_note": "Project-derived field projection for browser-local sense review; source wording is unchanged.",
            "senses": senses,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Pinned english-wordnet-2025-json.zip")
    parser.add_argument("--check", type=Path, help="Compare output with a checked-in subset")
    args = parser.parse_args()
    rendered = json.dumps(build_subset(args.source), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if args.check.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"OEWN subset differs from {args.check}.")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
