#!/usr/bin/env python3
"""Verify existing SimpleWiki caches and emit a prose-free development prefix offline."""

import argparse
import json
from pathlib import Path

from profile_voa_material_candidates import MWE_TOKEN, mwe_gap_leads, mwe_leads
from screen_simplewiki_route2_rendered import (
    CACHE, NGSL, OUTPUT, ROOT, extract_blocks, sha256_bytes, sha256_file,
    self_check as extractor_self_check,
)


CONTRAST_FORMS = ("pick up", "come out", "make sure")
CONTRAST_SCREEN_SHA256 = "e0cce039a3331fffdc0e8ff914506db5004bf7c782d5cceb2d354a5f1cfac148"
CONTRAST_IDENTITY_SHA256 = "2a914efbd7f9a99174d083ab691e77306a647fb9d3772bfb3e6cf3567236ad0d"


def contrast_priority(form, page_id, revision_id):
    return sha256_bytes(json.dumps(
        ["IR136-ACQ-0.12", form, page_id, revision_id], separators=(",", ":")
    ).encode())


def contrast_leads(paragraphs, ngsl):
    """Reuse the old lead generators, but require the second surface member exactly."""
    tokens = [match.group().replace("’", "'").lower()
              for paragraph in paragraphs for match in MWE_TOKEN.finditer(paragraph)]
    raw = mwe_leads(paragraphs, ngsl, dict.fromkeys(CONTRAST_FORMS, 0))
    raw += mwe_gap_leads(paragraphs, ngsl, dict.fromkeys(CONTRAST_FORMS[:2], 0), maximum_gap=8)
    result = {form: set() for form in CONTRAST_FORMS}
    for lead in raw:
        form = lead["canonical_form"]
        if "mwe_member_token_positions" in lead:
            start, end = lead["mwe_member_token_positions"]
        else:
            start, end = lead["mwe_token_start"], lead["mwe_token_end"]
        if tokens[end - 1] == form.split()[1]:
            result[form].add((lead["paragraph"], start, end, end - start - 1))
    return {form: sorted(positions) for form, positions in result.items()}


def build_contrast_plan(cache_directory):
    """Offline metadata only; this does not reopen Route 2 or display/release article text."""
    decisions = json.loads((ROOT / "resources/decision_log.json").read_text())["records"]
    exposure = json.loads((ROOT / "resources/leakage_ledger.json").read_text())["records"]
    if not any(row["id"] == "DEC-2026-09-05-020" and row["status"] == "accepted" for row in decisions):
        raise ValueError("The development-purpose extension is not accepted.")
    if not any(row["id"] == "EXP-2026-09-05-011" and row["supersedes_id"] == "EXP-2026-09-02-004" for row in exposure):
        raise ValueError("The development pool exposure is not registered.")
    if sha256_file(OUTPUT) != CONTRAST_SCREEN_SHA256:
        raise ValueError("Frozen rendered-screen identity mismatch.")
    extractor_hash = sha256_file(ROOT / "scripts/screen_simplewiki_route2_rendered.py")
    if extractor_hash != "094a90596a14e4bfa0b7fd84f8d58df7cedeeb7cdb36f0cd1c025aa3519dddb8":
        raise ValueError("Pinned extractor identity mismatch.")
    if sha256_file(ROOT / "scripts/profile_voa_material_candidates.py") != "a35ba66cb05e6207a056328e1829de8c4e4448c165597e6709eb3b695a561172":
        raise ValueError("Pinned profile helper identity mismatch.")
    screen = json.loads(OUTPUT.read_text())
    unique = {}
    fields = ["page_id", "revision_id", "api_response_sha256", "rendered_html_sha256", "extracted_text_sha256"]
    for values in screen["rows"]:
        row = dict(zip(screen["row_columns"], values))
        if row["source_identity_state"] != "verified_against_dump_wikitext_sha256":
            continue
        key = (row["page_id"], row["revision_id"])
        if key in unique and any(row[f] != unique[key][f] for f in fields + ["source_text_sha256", "title"]):
            raise ValueError("Conflicting duplicate source identity.")
        unique[key] = row
    identities = [[row[field] for field in fields] for _, row in sorted(unique.items())]
    if len(unique) != 507 or sha256_bytes(json.dumps(identities, separators=(",", ":")).encode()) != CONTRAST_IDENTITY_SHA256:
        raise ValueError("Frozen deduplicated source pool mismatch.")
    if sha256_file(NGSL) != screen["inputs"]["ngsl_profile_sha256"]:
        raise ValueError("Frozen inflection projection mismatch.")
    # Verify the complete pool before any target search; never fetch missing caches.
    source_paragraphs, byte_count, block_count, paragraph_count = [], 0, 0, 0
    for (page_id, revision_id), row in sorted(unique.items()):
        raw = (cache_directory / f"{revision_id}.json").read_bytes()
        if sha256_bytes(raw) != row["api_response_sha256"]:
            raise ValueError(f"Cached response mismatch: {revision_id}")
        parsed = json.loads(raw).get("parse", {})
        if (parsed.get("pageid"), parsed.get("revid"), parsed.get("title")) != (page_id, revision_id, row["title"]):
            raise ValueError(f"Cached revision identity mismatch: {revision_id}")
        for field, expected in [("wikitext", "source_text_sha256"), ("text", "rendered_html_sha256")]:
            if not isinstance(parsed.get(field), str) or sha256_bytes(parsed[field].encode()) != row[expected]:
                raise ValueError(f"Cached {field} mismatch: {revision_id}")
        blocks = extract_blocks(parsed["text"])
        paragraphs = [block["plain"] for block in blocks if block["tag"] == "p"]
        if (sha256_bytes("\n\n".join(block["plain"] for block in blocks).encode()) != row["extracted_text_sha256"]
                or len(blocks) != row["block_count"] or len(paragraphs) != row["paragraph_count"]):
            raise ValueError(f"Cached extraction mismatch: {revision_id}")
        source_paragraphs.append((page_id, revision_id, paragraphs))
        byte_count += len(raw)
        block_count += len(blocks)
        paragraph_count += len(paragraphs)
    ngsl = dict(json.loads(NGSL.read_text())["rows"])
    by_form = {form: [] for form in CONTRAST_FORMS}
    for page_id, revision_id, paragraphs in source_paragraphs:
        for form, positions in contrast_leads(paragraphs, ngsl).items():
            if positions:
                by_form[form].append([form, page_id, revision_id, contrast_priority(form, page_id, revision_id), positions])
    rows, selected, summary = [], [], []
    for form, candidates in by_form.items():
        candidates.sort(key=lambda row: (row[3], row[1], row[2]))
        rows.extend(candidates)
        selected.extend(row[:3] for row in candidates[:20])
        summary.append({"form": form, "candidate_pages": len(candidates),
                        "lead_count": sum(len(row[4]) for row in candidates),
                        "selected_pages": min(20, len(candidates))})
    return {
        "plan_id": "IR136-SIMPLEWIKI-CONTRAST-1.0.0",
        "status": "fixed_prefix_metadata_only_no_context_review",
        "inputs": {"screen_sha256": CONTRAST_SCREEN_SHA256, "identity_sha256": CONTRAST_IDENTITY_SHA256,
                   "script_sha256": sha256_file(Path(__file__)), "extractor_sha256": extractor_hash, "ngsl_sha256": sha256_file(NGSL),
                   "profile_helper_sha256": sha256_file(ROOT / "scripts/profile_voa_material_candidates.py")},
        "verified": {"revisions": len(unique), "cache_bytes": byte_count, "blocks": block_count,
                     "paragraphs": paragraph_count, "excluded_unavailable_revisions": 1},
        "boundary": {"network_requests": 0, "context_reviews": 0, "text_releases": 0,
                     "prefix_limit_per_form": 20, "first_lead_only_for_later_review": True},
        "summary": summary,
        "row_columns": ["form", "page_id", "revision_id", "selection_sha256", "lead_positions"],
        "lead_position_columns": ["paragraph_1based", "mwe_token_start_1based", "mwe_token_end_1based", "gap_tokens"],
        "rows": rows,
        "selected_columns": ["form", "page_id", "revision_id"],
        "selected": selected,
    }


def self_check():
    extractor_self_check()
    inflections = {"picked": [["pick", 1]], "came": [["come", 2]], "makes": [["make", 3]], "ups": [["up", 4]]}
    leads = contrast_leads(["They picked him up. It came out. She makes sure."], inflections)
    assert [len(leads[form]) for form in CONTRAST_FORMS] == [1, 1, 1]
    assert leads["pick up"] == [(1, 2, 4, 1)]
    assert contrast_leads(["pick " + "x " * 8 + "up"], {})["pick up"] == [(1, 1, 10, 8)]
    assert not any(contrast_leads(["pick " + "x " * 9 + "up", "make quite sure", "pick ups"], inflections).values())
    assert not any(contrast_leads(["pick", "up"], {}).values())
    assert contrast_priority("pick up", 1, 2) == sha256_bytes(b'["IR136-ACQ-0.12","pick up",1,2]')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=CACHE)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-check", action="store_true")
    mode.add_argument("--contrast-plan", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("Offline SimpleWiki contrast preparation self-check: PASS")
    else:
        print(json.dumps(build_contrast_plan(args.cache), ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
