#!/usr/bin/env python3
"""Build the pinned NGSL 1.2 browser ranked-list projection."""

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "resources/ngsl_1_2_ascii_forms.json"
STATS_SHA256 = "2098bab8955a120a9766c6282a51d7d578c6cb0a7d946600d2ffb73ba25a0b44"
FORMS_SHA256 = "d814f2a0a3c61479a2c5ad037661719a0cc6e7dbcde31f181b54f12d0f1e11a4"
COMPOSITE_SHA256 = "61e6824034795eabdf3543646f6196eae3a1afaf8ef76e1aa578e73e5c3c9643"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build(stats_path: Path, forms_path: Path) -> dict:
    stats_bytes = stats_path.read_bytes()
    forms_bytes = forms_path.read_bytes()
    if digest(stats_bytes) != STATS_SHA256 or digest(forms_bytes) != FORMS_SHA256:
        raise ValueError("NGSL source SHA-256 does not match the reviewed artifacts.")
    if digest(stats_bytes + b"\0" + forms_bytes) != COMPOSITE_SHA256:
        raise ValueError("NGSL composite source identity changed.")

    reader = csv.DictReader(stats_bytes.decode("utf-8").splitlines())
    if reader.fieldnames != ["Lemma", "SFI Rank", "SFI", "Adjusted Frequency per Million (U)"]:
        raise ValueError("NGSL statistics columns changed.")
    ranks = {}
    for row in reader:
        lemma = row["Lemma"].strip().lower()
        rank = int(row["SFI Rank"])
        float(row["SFI"])
        float(row["Adjusted Frequency per Million (U)"])
        if not lemma.isascii() or not lemma.isalpha() or lemma in ranks:
            raise ValueError(f"Invalid or duplicate NGSL lemma: {lemma}")
        ranks[lemma] = rank
    if len(ranks) != 2_809 or sorted(ranks.values()) != list(range(1, 2_810)):
        raise ValueError("NGSL lemma ranks changed.")

    source_rows = csv.reader(
        line for line in forms_bytes.decode("utf-8").splitlines()
        if line.strip() and not line.startswith("##")
    )
    forms = defaultdict(list)
    excluded = []
    head_count = 0
    for row in source_rows:
        head_count += 1
        lemma = row[0].strip().lower()
        if lemma not in ranks:
            raise ValueError(f"NGSL research-form head is not ranked: {lemma}")
        for source_form in row:
            form = source_form.strip().lower()
            if not form.isascii() or not form.isalpha():
                excluded.append(form)
                continue
            mapping = [lemma, ranks[lemma]]
            if mapping in forms[form]:
                raise ValueError(f"Duplicate NGSL form/head mapping: {form} -> {lemma}")
            forms[form].append(mapping)
    if head_count != 2_809 or len(forms) != 10_114 or len(excluded) != 7:
        raise ValueError("NGSL research-form projection changed.")
    for mappings in forms.values():
        mappings.sort(key=lambda item: (item[1], item[0]))
    rows = [[form, forms[form]] for form in sorted(forms)]
    expected = {
        "the": [["the", 1]], "taken": [["take", 59]],
        "favorite": [["favorite", 1_000]], "difficulty": [["difficulty", 1_001]],
        "thick": [["thick", 2_000]], "found": [["find", 81], ["found", 2_807]],
    }
    if any(forms.get(form) != value for form, value in expected.items()):
        raise ValueError("NGSL fixed projection fixtures changed.")

    return {
        "profile_schema_version": "0.1.0",
        "identity": {
            "profile_id": "ngsl-1.2-ascii-research-forms",
            "profile_version": "1.2.projection-1",
            "title": "NGSL 1.2 ASCII research-form ranked inventory",
            "profile_status": "admitted",
            "language": "en",
        },
        "construct": {
            "coverage_channel": "word",
            "reference_function": "ranked_inventory",
            "unit": "lowercase NFKC-normalized ASCII alphabetic surface token mapped to one or more NGSL head lemmas",
            "population_or_exposure_claim": "membership in the NGSL 1.2 research-form inventory at an explicitly selected headword-rank cutoff",
            "excluded_inferences": [
                "Nation BNC/COCA word-family level", "contextual word sense", "learner knowledge",
                "CEFR level", "MWE knowledge", "universal 95 or 98 percent threshold",
            ],
        },
        "source": {
            "source_kind": "lexicon",
            "creator_or_rights_holder": "Browne, Culligan, and Phillips",
            "canonical_url": "https://www.newgeneralservicelist.com/new-general-service-list",
            "release_or_edition": "NGSL 1.2, April 2023",
            "retrieved_on": "2026-09-01",
            "artifact_name": "NGSL_1.2_stats.csv + NGSL_1.2_lemmatized_for_research.csv",
            "artifact_size_bytes": len(stats_bytes) + len(forms_bytes),
            "artifact_sha256": COMPOSITE_SHA256,
            "composite_sha256_formula": "SHA-256(stats bytes + NUL byte + research-form bytes)",
            "artifacts": [
                {"name": "NGSL_1.2_stats.csv", "size_bytes": len(stats_bytes), "sha256": STATS_SHA256},
                {"name": "NGSL_1.2_lemmatized_for_research.csv", "size_bytes": len(forms_bytes), "sha256": FORMS_SHA256},
            ],
        },
        "corpus_design": {
            "applies": False,
            "registers": [],
            "language_varieties": [],
            "time_span": {"start": None, "end": None},
            "sampling_frame": "not applicable to this derived ranked lexical inventory",
            "sampling_unit": "not applicable",
            "token_count": None,
            "document_count": None,
            "balancing_or_weighting": "source SFI rank retained; source-corpus construction is documented by NGSL",
            "known_biases": [
                "research forms deliberately disregard meaning sense",
                "homographs require researcher interpretation",
                "generated possible forms include rare and contraction-fragment strings",
            ],
        },
        "processing": {
            "source_tokenization": "source-supplied comma-separated research-form strings",
            "input_tokenizer_mapping": "NFKC-normalize input, then recognize whole ASCII alphabetic tokens; apostrophes and hyphens are boundaries",
            "normalization": "ASCII lowercase; seven hyphenated source variants excluded because unhyphenated variants are also supplied",
            "case_policy": "lowercase",
            "lemmatization": "no runtime lemmatizer; exact source-supplied form-to-head mapping",
            "part_of_speech_policy": "none",
            "word_family_policy": "NGSL research-form grouping, not a Nation Level 6 word family",
            "mwe_matching_policy": "not applicable",
            "sense_mapping_policy": "none; source explicitly collapses meaning senses",
            "derivation_command": "python3 scripts/build_ngsl_profile.py NGSL_1.2_stats.csv NGSL_1.2_lemmatized_for_research.csv --check",
            "derivation_code_path": "scripts/build_ngsl_profile.py",
            "derivation_code_commit": "release commit containing this profile",
        },
        "table": {
            "path": "resources/ngsl_1_2_ascii_forms.json",
            "format": "JSON; compact array rows nested in this manifest",
            "encoding": "UTF-8",
            "compression": None,
            "row_unit": "normalized ASCII surface form",
            "columns": ["surface_form", "candidate_head_lemma_rank_pairs"],
            "total_row_rule": None,
            "duplicate_key_rule": "one surface row; retain multiple head mappings for the five source-identified homographs",
            "source_headword_count": head_count,
            "projected_row_count": len(rows),
            "ambiguous_surface_form_count": sum(len(mappings) > 1 for mappings in forms.values()),
            "excluded_source_forms": sorted(excluded),
        },
        "measurement": {
            "numerator_definition": "profile-tokenized input tokens with at least one candidate NGSL head rank at or below the selected cutoff; all candidate mappings remain visible",
            "denominator_definition": "all profile-tokenized input tokens in the declared text",
            "frequency_or_rank_formula": "retain source SFI Rank of the mapped head lemma; no runtime frequency is inferred for a surface form",
            "band_boundaries": [1_000, 2_000, 2_809],
            "rank_tie_policy": "retain source integer SFI Rank",
            "dispersion_field": None,
            "missing_item_policy": "retain source-listed forms above the cutoff as beyond_cutoff and absent forms as unmatched",
            "zero_denominator_policy": "value is null; preserve numerator and denominator",
        },
        "rights": {
            "license_identifier": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "redistribution_permitted": True,
            "modification_permitted": True,
            "browser_delivery_permitted": True,
            "derived_output_publication_permitted": True,
            "required_attribution": "New General Service List 1.2 by Browne, Culligan, and Phillips; modified ASCII browser projection",
            "notice_paths": ["resources/NGSL_NOTICE.md", "RIGHTS.md"],
            "restrictions": ["attribution", "ShareAlike", "indicate modifications"],
            "reviewed_on": "2026-09-01",
        },
        "validation": {
            "fixture_ids": ["ngsl-the", "ngsl-taken", "ngsl-cutoff-1000", "ngsl-cutoff-2000", "ngsl-homograph-found"],
            "expected_results": [[form, mappings] for form, mappings in expected.items()],
            "cross_tool_claim": "none",
            "browser_size_or_latency_evidence": "not yet measured in a real browser",
            "removal_or_replacement_procedure": "delete this profile, notice, fetch/use/tests, and NGSL claims; never relabel a cutoff as a Nation word-family level",
        },
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stats", type=Path)
    parser.add_argument("forms", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = (json.dumps(build(args.stats, args.forms), ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != payload:
            raise SystemExit(f"Generated profile differs from {OUTPUT}")
        print(f"Profile verification: PASS ({OUTPUT.relative_to(ROOT)}, {len(payload)} bytes)")
    else:
        OUTPUT.write_bytes(payload)
        print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(payload)} bytes)")


if __name__ == "__main__":
    main()
