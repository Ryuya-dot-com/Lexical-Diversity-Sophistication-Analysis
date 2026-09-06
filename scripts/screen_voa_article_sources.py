#!/usr/bin/env python3
"""Screen frozen VOA queue items for source credit and extractable boundaries."""

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from extract_voa_articles import ArticleParser, CREDIT, extract


TARGET_PER_CATEGORY = 12
SOURCE_LINE = re.compile(
    r"\b(?:wrote|reported|adapted)\b.*\b(?:story|report|Learning English|VOA)\b",
    re.IGNORECASE,
)
EXTERNAL = re.compile(
    r"\badapted\b|associated press|\breuters\b|agence france-presse|\bAFP\b|"
    r"\bbased on (?:reports?|information|several online articles)|"
    r"additional re\w* from",
    re.IGNORECASE,
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def credit_state(paragraphs):
    candidates = [item for item in paragraphs if SOURCE_LINE.search(item)]
    source_credit = candidates[-1] if candidates else None
    if source_credit and EXTERNAL.search(source_credit):
        return "external_or_adapted", source_credit
    if not any(CREDIT.search(item) for item in paragraphs):
        return "missing_voa_production_credit", source_credit
    return "provisionally_eligible", source_credit


def screen(frame, directory):
    queued = {
        (item["sampling_category"], item["target_blind_queue_rank"]): item
        for item in frame["articles"]
        if not item["seen_before_frame_freeze"]
    }
    decisions = []
    category_reports = []
    for category in ("education", "health"):
        eligible = 0
        rank = 1
        while eligible < TARGET_PER_CATEGORY:
            frame_item = queued.get((category, rank))
            if frame_item is None:
                raise ValueError(f"The {category} queue ended before the target.")
            path = directory / f"{category}_{rank:02d}_amp.html"
            if not path.exists():
                raise ValueError(f"Missing downloaded queue artifact: {path.name}")
            source = path.read_bytes()
            parser = ArticleParser()
            parser.feed(source.decode("utf-8"))
            state = "unsupported_artifact"
            source_credit = None
            extracted = None
            if (parser.json_ld and parser.canonical_url and parser.paragraphs and
                    parser.json_ld.get("mainEntityOfPage") == parser.canonical_url and
                    parser.canonical_url == frame_item["canonical_url"]):
                state, source_credit = credit_state(parser.paragraphs)
                if state == "provisionally_eligible":
                    try:
                        extracted = extract(path)
                        state = "eligible"
                        eligible += 1
                    except ValueError:
                        state = "unsupported_prose_boundary"
            decision = {
                "sampling_category": category,
                "target_blind_queue_rank": rank,
                "canonical_url": frame_item["canonical_url"],
                "publication_date": frame_item["publication_date"],
                "archive_title": frame_item["title"],
                "source_file": path.name,
                "source_bytes": len(source),
                "source_sha256": sha256(source),
                "source_credit": source_credit,
                "state": state,
                "article_title": parser.json_ld.get("headline") if parser.json_ld else None,
                "modified_time": parser.json_ld.get("dateModified") if parser.json_ld else None,
                "paragraph_count": extracted["paragraph_count"] if extracted else None,
                "text_sha256": extracted["text_sha256"] if extracted else None,
            }
            decisions.append(decision)
            rank += 1
        category_decisions = [item for item in decisions
                              if item["sampling_category"] == category]
        category_reports.append({
            "sampling_category": category,
            "queue_stop_rank": rank - 1,
            "decision_count": len(category_decisions),
            "eligible_count": eligible,
            "state_counts": dict(sorted(Counter(
                item["state"] for item in category_decisions
            ).items())),
        })
    return {
        "screen_schema_version": "1.0.0",
        "screen_id": "gate1-voa-source-screen-v1",
        "frame_id": frame["frame_id"],
        "screened_on": "2026-09-01",
        "construct": {
            "purpose": "article-level source, credit, and prose-boundary eligibility before any target-form search",
            "eligible_rule": "supported canonical AMP artifact; recognized VOA/Learning English wrote/reported credit; no adaptation or AP/Reuters/AFP/additional-reporting marker; reproducible prose boundary",
            "excluded_inferences": [
                "article quality", "MWE presence", "MWE centrality", "learner suitability",
                "comprehension validity", "rights to article media or third-party material",
            ],
            "target_per_category": TARGET_PER_CATEGORY,
            "raw_html_bundled": False,
            "article_text_bundled": False,
        },
        "category_reports": category_reports,
        "decision_count": len(decisions),
        "decisions": decisions,
    }


def self_check():
    self_credit = "Tester reported on this story for VOA Learning English."
    assert credit_state([self_credit]) == ("provisionally_eligible", self_credit)
    adapted = "The Associated Press reported this story. Tester adapted it for Learning English."
    assert credit_state([adapted]) == ("external_or_adapted", adapted)
    extra = "Tester reported this story for VOA Learning English with additional reorting from the Associated Press."
    assert credit_state([extra]) == ("external_or_adapted", extra)
    assert credit_state(["No source credit."]) == (
        "missing_voa_production_credit", None
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frame", type=Path, nargs="?")
    parser.add_argument("directory", type=Path, nargs="?")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("VOA article-source screen self-check: PASS")
        return
    if not args.frame or not args.directory or not args.output:
        parser.error("frame, directory, and --output are required")
    frame = json.loads(args.frame.read_text(encoding="utf-8"))
    rendered = json.dumps(
        screen(frame, args.directory), ensure_ascii=False, separators=(",", ":")
    ) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Generated source screen differs from {args.output}")
        print(f"VOA article-source screen verification: PASS ({args.output})")
    else:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
