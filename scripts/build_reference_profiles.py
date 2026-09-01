#!/usr/bin/env python3
"""Build the pinned browser reference profiles from reviewed source assets."""

import argparse
import csv
import hashlib
import json
import lzma
import re
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
TUBELEX_OUTPUT = ROOT / "resources/tubelex_en_regex_ascii_2025.json"
OEWN_OUTPUT = ROOT / "resources/oewn_2025_multiword_verbs.json"
TUBELEX_SHA256 = "363de2f2ea58c3b4ff25306a6819c7424198d250902b3b0e566573015560c3ec"
OEWN_SHA256 = "7d749f6e2c39e6970e4997839dcf6e42fd281f3c2fae0171d2192bae8cfa4b51"
TUBELEX_WORD = re.compile(r"[a-z]+\Z")
MWE_MEMBER = re.compile(r"[a-z]+(?:'[a-z]+)*\Z")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n").encode()


def tubelex_profile(source: Path) -> dict:
    if digest(source) != TUBELEX_SHA256:
        raise ValueError("TUBELEX artifact SHA-256 does not match the reviewed source.")
    with lzma.open(source, "rt", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        expected = [
            "word", "count", "videos", "channels", "count:howto", "count:gaming",
            "count:entertainment", "count:education", "count:science", "count:sports",
            "count:nonprofits", "count:autos", "count:people", "count:music",
            "count:news", "count:film", "count:travel", "count:comedy", "count:pets",
        ]
        if reader.fieldnames != expected:
            raise ValueError("TUBELEX source columns changed.")
        counts = {}
        totals = []
        source_rows = 0
        for row in reader:
            source_rows += 1
            if row["word"] == "[TOTAL]":
                totals.append(row)
            elif TUBELEX_WORD.fullmatch(row["word"]):
                if row["word"] in counts:
                    raise ValueError(f"Duplicate TUBELEX projected form: {row['word']}")
                counts[row["word"]] = int(row["count"])
    if len(totals) != 1 or int(totals[0]["count"]) != 179_139_158:
        raise ValueError("TUBELEX total row changed or is not unique.")
    rows = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    if len(rows) != 410_400 or sum(count for _, count in rows) != 170_705_938:
        raise ValueError("TUBELEX ASCII projection no longer matches its reviewed fixture.")
    return {
        "profile_schema_version": "0.1.0",
        "identity": {
            "profile_id": "tubelex-en-regex-ascii-word-frequency",
            "profile_version": "2025-04-24.projection-1",
            "title": "TUBELEX English regex ASCII word-frequency profile",
            "profile_status": "admitted",
            "language": "en",
        },
        "construct": {
            "coverage_channel": "word",
            "reference_function": "frequency_distribution",
            "unit": "lowercase NFKC-normalized ASCII alphabetic surface token",
            "population_or_exposure_claim": "frequency evidence from the sampled English YouTube subtitle corpus, used only as an audiovisual/spoken-exposure approximation",
            "excluded_inferences": [
                "general English frequency", "written or academic frequency", "learner knowledge",
                "CEFR level", "word-family frequency", "MWE frequency", "pedagogical importance",
            ],
        },
        "source": {
            "source_kind": "corpus_aggregate",
            "creator_or_rights_holder": "Adam Nohejl and TUBELEX contributors",
            "canonical_url": "https://github.com/naist-nlp/tubelex",
            "release_or_edition": "repository commit 7cb5fb36add76b83a266d1967536e1a1d3faa513",
            "retrieved_on": "2026-09-01",
            "artifact_name": "frequencies/tubelex-en-regex.tsv.xz",
            "artifact_size_bytes": 3_198_336,
            "artifact_sha256": TUBELEX_SHA256,
            "citation_url": "https://aclanthology.org/2025.coling-main.641/",
        },
        "corpus_design": {
            "applies": True,
            "registers": ["YouTube manual subtitles"],
            "language_varieties": ["multiple English varieties and non-native speech are present"],
            "time_span": {"start": "not reported for the aggregate", "end": "not reported for the aggregate"},
            "sampling_frame": "videos discovered by searches for Wikipedia article titles; 120,000 English videos sampled before cleaning",
            "sampling_unit": "video subtitle file",
            "token_count": 179_139_158,
            "document_count": 105_733,
            "balancing_or_weighting": "no project reweighting; source aggregate counts",
            "known_biases": [
                "YouTube discovery and availability bias", "manual-subtitle selection",
                "topic/category imbalance", "subtitle-speech mismatches and synthetic speech",
                "unknown upload-date distribution", "not a learner corpus",
            ],
        },
        "processing": {
            "source_tokenization": "TUBELEX regex orthographic words (Unicode word characters excluding digits), lowercased and NFKC-normalized",
            "input_tokenizer_mapping": "NFKC-normalize input, then recognize whole ASCII alphabetic tokens; apostrophes and hyphens are boundaries",
            "normalization": "Unicode NFKC followed by ASCII lowercase",
            "case_policy": "lowercase",
            "lemmatization": "none",
            "part_of_speech_policy": "none",
            "word_family_policy": "none; surface forms remain separate",
            "mwe_matching_policy": "not applicable; component counts never become MWE counts",
            "sense_mapping_policy": "not applicable",
            "derivation_command": "python3 scripts/build_reference_profiles.py TUBELEX_XZ OEWN_ZIP --check",
            "derivation_code_path": "scripts/build_reference_profiles.py",
            "derivation_code_commit": "release commit containing this profile",
        },
        "table": {
            "path": "resources/tubelex_en_regex_ascii_2025.json",
            "format": "JSON; compact array rows nested in this manifest",
            "encoding": "UTF-8",
            "compression": None,
            "row_unit": "normalized ASCII surface form",
            "columns": ["word", "source_count"],
            "total_row_rule": "source [TOTAL] is located by label, validated, and excluded from rows",
            "duplicate_key_rule": "reject",
            "source_data_row_count": source_rows,
            "projected_row_count": len(rows),
            "projected_source_token_count": sum(count for _, count in rows),
        },
        "measurement": {
            "numerator_definition": "profile-tokenized input tokens whose normalized form occurs in rows",
            "denominator_definition": "all profile-tokenized input tokens in the declared text",
            "frequency_or_rank_formula": "count / 179139158 * 1000000; competition rank by descending count",
            "band_boundaries": [],
            "rank_tie_policy": "equal counts share the first rank occupied by the tie; alphabetical order only stabilizes serialization",
            "dispersion_field": None,
            "missing_item_policy": "retain as unmatched with no invented zero frequency",
            "zero_denominator_policy": "value is null; preserve numerator and denominator",
        },
        "rights": {
            "license_identifier": "BSD-3-Clause",
            "license_url": "https://github.com/naist-nlp/tubelex/blob/7cb5fb36add76b83a266d1967536e1a1d3faa513/LICENSE",
            "redistribution_permitted": True,
            "modification_permitted": True,
            "browser_delivery_permitted": True,
            "derived_output_publication_permitted": True,
            "required_attribution": "TUBELEX, copyright 2022-4 Adam Nohejl; cite Nohejl et al. (2025)",
            "notice_paths": ["resources/TUBELEX_LICENSE.txt", "RIGHTS.md"],
            "restrictions": ["no endorsement", "retain BSD notice and disclaimer"],
            "reviewed_on": "2026-09-01",
        },
        "validation": {
            "fixture_ids": ["tubelex-the", "tubelex-take", "tubelex-xylophone", "tubelex-unmatched"],
            "expected_results": [["the", 7_455_441], ["take", 192_575], ["xylophone", 23]],
            "cross_tool_claim": "none",
            "browser_size_or_latency_evidence": "Node 24.9.0 arm64 smoke check on 2026-09-01: 6,157,414 bytes, JSON parse 71.0 ms, Map build 43.0 ms, about 72.5 MB heap after load; real-browser latency remains a release-gate test",
            "removal_or_replacement_procedure": "delete this profile, its fetch/use/tests and TUBELEX notice; retain old releases for reproducibility where lawful",
        },
        "rows": rows,
    }


def oewn_profile(source: Path) -> dict:
    if digest(source) != OEWN_SHA256:
        raise ValueError("OEWN artifact SHA-256 does not match the reviewed source.")
    forms = {}
    with ZipFile(source) as archive:
        for name in sorted(archive.namelist()):
            if not name.startswith("entries-") or not name.endswith(".json"):
                continue
            for source_form, by_pos in json.loads(archive.read(name)).items():
                if "v" not in by_pos or " " not in source_form:
                    continue
                canonical = " ".join(source_form.lower().replace("’", "'").split())
                if not all(MWE_MEMBER.fullmatch(member) for member in canonical.split(" ")):
                    continue
                sense_ids = {sense["id"] for sense in by_pos["v"]["sense"]}
                if canonical in forms:
                    raise ValueError(f"Collapsed OEWN multiword verb form: {canonical}")
                forms[canonical] = sense_ids
    rows = [[form, len(forms[form])] for form in sorted(forms)]
    if len(rows) != 2_847 or len(forms["take in"]) != 17 or len(forms["spill the beans"]) != 1:
        raise ValueError("OEWN multiword verb projection no longer matches its reviewed fixture.")
    return {
        "profile_schema_version": "0.1.0",
        "identity": {
            "profile_id": "oewn-2025-ascii-multiword-verb-forms",
            "profile_version": "2025.projection-1",
            "title": "Open English WordNet 2025 ASCII multiword verb-form inventory",
            "profile_status": "admitted",
            "language": "en",
        },
        "construct": {
            "coverage_channel": "mwe_form",
            "reference_function": "inventory_membership",
            "unit": "OEWN verb entry containing two or more space-separated ASCII alphabetic members",
            "population_or_exposure_claim": "lexicographic membership in the pinned OEWN 2025 projection",
            "excluded_inferences": [
                "corpus frequency", "VPC or VID category", "occurrence truth", "contextual sense",
                "idiomaticity", "learner knowledge", "CEFR level", "pedagogical importance",
            ],
        },
        "source": {
            "source_kind": "lexicon",
            "creator_or_rights_holder": "Open English WordNet Team and Princeton University",
            "canonical_url": "https://github.com/globalwordnet/english-wordnet",
            "release_or_edition": "2025-edition; commit dc343f2683279ecbb13fab4e2fd778d7b162d287",
            "retrieved_on": "2026-09-01",
            "artifact_name": "english-wordnet-2025-json.zip",
            "artifact_size_bytes": 9_986_555,
            "artifact_sha256": OEWN_SHA256,
            "citation_url": "https://aclanthology.org/2019.gwc-1.31/",
        },
        "corpus_design": {
            "applies": False,
            "registers": [], "language_varieties": [],
            "time_span": {"start": None, "end": None},
            "sampling_frame": "not applicable to a lexicon",
            "sampling_unit": "not applicable",
            "token_count": None, "document_count": None,
            "balancing_or_weighting": None,
            "known_biases": ["lexicographic coverage is not corpus representativeness", "ASCII space-separated projection excludes other orthographic forms"],
        },
        "processing": {
            "source_tokenization": "OEWN entry lemma string",
            "input_tokenizer_mapping": "exact lowercase canonical-form lookup after whitespace collapse",
            "normalization": "curly apostrophe to straight, lowercase, collapse whitespace; retain only ASCII alphabetic members",
            "case_policy": "lowercase", "lemmatization": "researcher supplies canonical form",
            "part_of_speech_policy": "verb entries only", "word_family_policy": "not applicable",
            "mwe_matching_policy": "lookup occurs only after human occurrence confirmation; exact canonical-form membership",
            "sense_mapping_policy": "sense count is descriptive inventory metadata; no contextual assignment",
            "derivation_command": "python3 scripts/build_reference_profiles.py TUBELEX_XZ OEWN_ZIP --check",
            "derivation_code_path": "scripts/build_reference_profiles.py",
            "derivation_code_commit": "release commit containing this profile",
        },
        "table": {
            "path": "resources/oewn_2025_multiword_verbs.json",
            "format": "JSON; compact array rows nested in this manifest", "encoding": "UTF-8",
            "compression": None, "row_unit": "normalized multiword verb form",
            "columns": ["canonical_form", "sense_count"], "total_row_rule": None,
            "duplicate_key_rule": "reject after normalization", "projected_row_count": len(rows),
        },
        "measurement": {
            "numerator_definition": "confirmed MWE occurrences or distinct confirmed canonical forms matched in rows",
            "denominator_definition": "confirmed MWE occurrences or distinct confirmed canonical forms, reported separately",
            "frequency_or_rank_formula": None, "band_boundaries": [], "rank_tie_policy": None,
            "dispersion_field": None,
            "missing_item_policy": "retain as out_of_inventory; do not reject the occurrence or infer non-MWE status",
            "zero_denominator_policy": "value is null; preserve numerator and denominator",
        },
        "rights": {
            "license_identifier": "CC-BY-4.0 AND WordNet",
            "license_url": "https://github.com/globalwordnet/english-wordnet/blob/2025-edition/LICENSE.md",
            "redistribution_permitted": True, "modification_permitted": True,
            "browser_delivery_permitted": True, "derived_output_publication_permitted": True,
            "required_attribution": "Open English WordNet Team and Princeton University WordNet",
            "notice_paths": ["resources/OEWN_WORDNET_NOTICE.txt", "RIGHTS.md"],
            "restrictions": ["attribution", "retain incorporated WordNet license", "no endorsement"],
            "reviewed_on": "2026-09-01",
        },
        "validation": {
            "fixture_ids": ["oewn-take-in", "oewn-spill-the-beans", "oewn-out-of-inventory"],
            "expected_results": [["take in", 17], ["spill the beans", 1]],
            "cross_tool_claim": "none",
            "browser_size_or_latency_evidence": "Node 24.9.0 arm64 smoke check on 2026-09-01: 52,420 bytes, JSON parse 0.6 ms, Map build 0.2 ms; real-browser latency remains a release-gate test",
            "removal_or_replacement_procedure": "delete this profile and its fetch/use/tests; preserve explicit out_of_inventory states and old releases where lawful",
        },
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("tubelex", type=Path)
    parser.add_argument("oewn", type=Path)
    parser.add_argument("--check", action="store_true", help="compare with checked-in profiles")
    args = parser.parse_args()
    outputs = {
        TUBELEX_OUTPUT: encode(tubelex_profile(args.tubelex)),
        OEWN_OUTPUT: encode(oewn_profile(args.oewn)),
    }
    if len(outputs[TUBELEX_OUTPUT]) >= 7_000_000 or len(outputs[OEWN_OUTPUT]) >= 100_000:
        raise ValueError("A browser reference payload exceeded its reviewed size ceiling.")
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_bytes() != content:
                raise SystemExit(f"Reference profile differs from {path}.")
        else:
            path.write_bytes(content)
            print(f"wrote {path.relative_to(ROOT)} ({len(content)} bytes)")


if __name__ == "__main__":
    main()
