#!/usr/bin/env python3
"""Build a local-only BNC/COCA Level 6 first-2K browser profile."""

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile


SOURCE_SHA256 = "ac81c7a60e5c76cd2bbf0c59b0501808f0d4fa026b2936919dd54329a9bb6a69"
SOURCE_SIZE = 600_930
LEVEL_FIXTURES = {
    1: {"line_count": 6_857, "head_count": 1_000, "member_count": 5_857},
    2: {"line_count": 6_370, "head_count": 1_000, "member_count": 5_370},
}


def build(source: Path) -> dict:
    source_bytes = source.read_bytes()
    if len(source_bytes) != SOURCE_SIZE or hashlib.sha256(source_bytes).hexdigest() != SOURCE_SHA256:
        raise ValueError("BNC/COCA zip identity does not match the reviewed v1.0.0 artifact.")
    forms = defaultdict(list)
    excluded = []
    with ZipFile(source) as archive:
        names = set(archive.namelist())
        required = {f"basewrd{level}.txt" for level in (1, 2, 31, 32, 33, 34)}
        if not required <= names or "Range32H.exe" not in names:
            raise ValueError("BNC/COCA archive structure changed.")
        for level in (1, 2):
            lines = archive.read(f"basewrd{level}.txt").decode("utf-8").splitlines()
            head = None
            heads = set()
            member_count = 0
            for number, line in enumerate(lines, 1):
                if not line.endswith(" 0"):
                    raise ValueError(f"Unexpected BNC/COCA row {level}:{number}.")
                indented = line.startswith("\t")
                form = line[:-2].strip().lower()
                if not indented:
                    head = form
                    if head in heads:
                        raise ValueError(f"Duplicate BNC/COCA family head: {head}")
                    heads.add(head)
                elif head is None:
                    raise ValueError(f"BNC/COCA member precedes its head: {level}:{number}")
                else:
                    member_count += 1
                if not form.isascii() or not form.isalpha():
                    excluded.append([form, head, level])
                    continue
                mapping = [head, level]
                if mapping in forms[form]:
                    raise ValueError(f"Duplicate BNC/COCA form/family mapping: {form} -> {head}")
                forms[form].append(mapping)
            expected = LEVEL_FIXTURES[level]
            if (len(lines), len(heads), member_count) != (
                expected["line_count"], expected["head_count"], expected["member_count"]
            ):
                raise ValueError(f"BNC/COCA level {level} counts changed.")
    for mappings in forms.values():
        mappings.sort(key=lambda item: (item[1], item[0]))
    if len(forms) != 13_223 or len(excluded) != 4 or any(len(value) != 1 for value in forms.values()):
        raise ValueError("BNC/COCA first-2K ASCII projection changed.")
    expected = {
        "a": [["a", 1]], "abilities": [["able", 1]], "taken": [["take", 1]],
        "accent": [["accent", 2]], "unaccented": [["accent", 2]],
    }
    if any(forms.get(form) != mappings for form, mappings in expected.items()):
        raise ValueError("BNC/COCA fixed projection fixtures changed.")
    rows = [[form, forms[form]] for form in sorted(forms)]
    return {
        "profile_schema_version": "0.1.0",
        "identity": {
            "profile_id": "bnc-coca-level6-v1.0.0-first-2k-local",
            "profile_version": "1.0.0.local-projection-1",
            "title": "Nation BNC/COCA Level 6 first-2K word-family profile",
            "profile_status": "local_only",
            "language": "en",
        },
        "construct": {
            "coverage_channel": "word",
            "reference_function": "ranked_inventory",
            "unit": "lowercase NFKC-normalized ASCII alphabetic surface token mapped to a Nation BNC/COCA Level 6 word family",
            "population_or_exposure_claim": "membership in the first or first two 1,000 word-family levels of the pinned BNC/COCA Level 6 v1.0.0 lists",
            "excluded_inferences": [
                "contextual word sense", "learner knowledge", "CEFR level", "MWE knowledge",
                "universal 95 or 98 percent threshold", "automatic inclusion of special lists",
            ],
        },
        "source": {
            "source_kind": "lexicon",
            "delivery_mode": "researcher_supplied_local_file",
            "creator_or_rights_holder": "I. S. P. Nation",
            "canonical_url": "https://www.wgtn.ac.nz/lals/resources/paul-nations-resources/vocabulary-analysis-programs",
            "method_description_url": "https://www.wgtn.ac.nz/__data/assets/pdf_file/0004/1689349/Information-on-the-BNC_COCA-word-family-lists-20180705.pdf",
            "release_or_edition": "BNC/COCA Level 6 word family lists v1.0.0",
            "retrieved_on": "2026-09-01",
            "artifact_name": "BNC_COCA_25000.zip",
            "artifact_size_bytes": SOURCE_SIZE,
            "artifact_sha256": SOURCE_SHA256,
        },
        "corpus_design": {
            "applies": False,
            "registers": [],
            "language_varieties": [],
            "time_span": {"start": None, "end": None},
            "sampling_frame": "not applicable to the released lexical inventory; source construction is documented by Nation",
            "sampling_unit": "not applicable",
            "token_count": None,
            "document_count": None,
            "balancing_or_weighting": "retain source Level 6 family assignments",
            "known_biases": [
                "word-family membership assumes receptive control of Level 6 derivational relations",
                "surface matching cannot establish whether the family relationship is available to a learner",
                "proper names and other special lists are excluded from this projection",
            ],
        },
        "processing": {
            "source_tokenization": "Range basewrd1.txt and basewrd2.txt family rows",
            "input_tokenizer_mapping": "NFKC-normalize input, then recognize whole ASCII alphabetic tokens; apostrophes and hyphens are boundaries",
            "normalization": "ASCII lowercase; four accented duplicate variants excluded while their ASCII forms remain",
            "case_policy": "lowercase",
            "lemmatization": "no runtime lemmatizer; exact source-supplied family-member lookup",
            "part_of_speech_policy": "source family assignments retained without runtime POS disambiguation",
            "word_family_policy": "Nation BNC/COCA Level 6 v1.0.0 family membership",
            "mwe_matching_policy": "not applicable",
            "sense_mapping_policy": "none; surface homographs are not contextually disambiguated",
            "special_list_policy": "exclude basewrd31 proper nouns, basewrd32 marginal words, basewrd33 transparent compounds, and basewrd34 acronyms; report them as unmatched unless handled separately outside this profile",
            "legacy_executable_policy": "Range32H.exe is neither read nor executed",
            "derivation_command": "python3 scripts/build_bnc_coca_profile.py BNC_COCA_25000.zip OUTPUT.json",
            "derivation_code_path": "scripts/build_bnc_coca_profile.py",
            "derivation_code_commit": "release commit containing this builder",
        },
        "table": {
            "path": "researcher-selected local JSON; never bundled by this project",
            "format": "JSON; compact array rows nested in this manifest",
            "encoding": "UTF-8",
            "compression": None,
            "row_unit": "normalized ASCII surface form",
            "columns": ["surface_form", "candidate_family_head_level_pairs"],
            "total_row_rule": None,
            "duplicate_key_rule": "one surface row; reject duplicate form/family mappings",
            "source_headword_count": 2_000,
            "projected_row_count": len(rows),
            "ambiguous_surface_form_count": 0,
            "excluded_source_forms": sorted(excluded),
            "excluded_special_lists": {
                "basewrd31.txt": "proper nouns", "basewrd32.txt": "marginal words",
                "basewrd33.txt": "transparent compounds", "basewrd34.txt": "acronyms",
            },
        },
        "measurement": {
            "numerator_definition": "profile-tokenized input tokens whose mapped family level is at or below the selected 1K or 2K cutoff",
            "denominator_definition": "all profile-tokenized input tokens in the declared text",
            "frequency_or_rank_formula": "retain source integer 1,000-family level; no corpus frequency is inferred",
            "band_boundaries": [1, 2],
            "band_labels": {"1": "BNC/COCA Level 6 first 1,000 families", "2": "BNC/COCA Level 6 first 2,000 families"},
            "rank_tie_policy": "not applicable; each value is a 1,000-family level",
            "dispersion_field": None,
            "missing_item_policy": "retain level-2 forms above the first-1K cutoff as beyond_cutoff and all other forms, including excluded special-list items, as unmatched",
            "zero_denominator_policy": "value is null; preserve numerator and denominator",
        },
        "rights": {
            "license_identifier": "UNRESOLVED-PARENT-PAGE-CC-BY-SA-4.0-OR-GPL-2.0-OR-GPL-3.0",
            "license_url": "https://www.wgtn.ac.nz/lals/resources/paul-nations-resources",
            "redistribution_permitted": False,
            "modification_permitted": None,
            "browser_delivery_permitted": False,
            "local_user_import_permitted": True,
            "derived_output_publication_permitted": None,
            "required_attribution": "Nation, I. S. P. (2017), BNC/COCA Level 6 word family lists v1.0.0",
            "notice_paths": ["RIGHTS.md"],
            "restrictions": [
                "do not redistribute the source or generated profile from this project",
                "confirm the artifact-specific license before public profile delivery",
                "review derived-output publication and ShareAlike obligations",
            ],
            "reviewed_on": "2026-09-01",
        },
        "validation": {
            "fixture_ids": ["bnc-coca-a", "bnc-coca-abilities", "bnc-coca-taken", "bnc-coca-level2"],
            "expected_results": [[form, mappings] for form, mappings in expected.items()],
            "cross_tool_claim": "none",
            "browser_size_or_latency_evidence": "researcher must record the generated local profile hash; real-browser evidence remains pending",
            "removal_or_replacement_procedure": "remove the local file from the browser session; no BNC/COCA data are stored in the repository or app",
        },
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = (json.dumps(build(args.source), ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    if args.check:
        if not args.output.exists() or args.output.read_bytes() != payload:
            raise SystemExit(f"Generated profile differs from {args.output}")
        print(f"Local profile verification: PASS ({len(payload)} bytes)")
    else:
        args.output.write_bytes(payload)
        print(f"Wrote local-only profile {args.output} ({len(payload)} bytes)")


if __name__ == "__main__":
    main()
