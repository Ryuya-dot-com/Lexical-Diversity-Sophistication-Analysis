#!/usr/bin/env python3
"""Verify frozen SimpleWiki queues through 20 rendered desk rows per target."""

import argparse
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

from profile_voa_material_candidates import mwe_gap_leads, mwe_leads, word_profile


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "resources/simplewiki_gate1_route2_design.json"
CANDIDATES = ROOT / "resources/simplewiki_gate1_route2_candidates.json"
NGSL = ROOT / "resources/ngsl_1_2_ascii_forms.json"
OUTPUT = ROOT / "resources/simplewiki_gate1_route2_rendered_screen.json"
CACHE = ROOT / "research_data/simplewiki/rendered_api"
API = "https://simple.wikipedia.org/w/api.php"
USER_AGENT = (
    "LexicalCoverageMaterialAudit/0.1 "
    "(https://github.com/Ryuya-dot-com/Lexical-Diversity-Sophistication-Analysis; "
    "Gate 1 research material verification) Python-urllib"
)
EXPECTED_BNC_COCA_SHA256 = (
    "ebd06548187988eb1a61ab967cc39c01461023043ee7aef427606e5bf508f138"
)
TAIL_SECTIONS = {
    "bibliography", "books used as sources", "external links",
    "external websites", "footnotes", "further reading", "more reading",
    "notes", "other websites", "reference", "references", "related pages",
    "see also", "sources", "works cited",
}
EXCLUDED_TAGS = {
    "audio", "dl", "figure", "figcaption", "math", "noscript", "ol",
    "pre", "script", "style", "sup", "table", "ul", "video",
}
EXCLUDED_CLASSES = {
    "ambox", "gallery", "hatnote", "infobox", "metadata", "navbox",
    "noprint", "reference", "reflist", "shortdescription", "sistersitebox",
    "thumb", "toc", "mw-editsection", "mw-references-wrap",
}
MARKED_TAGS = {"a", "b", "blockquote", "em", "i", "strong"}
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sha256_file(path):
    return sha256_bytes(path.read_bytes())


def normalize(value):
    return re.sub(r"\s+", " ", value).strip()


class RenderedProseParser(HTMLParser):
    """Keep rendered headings and paragraphs, while marking focal-text cues."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.blocks = []
        self.current = None
        self.stopped = False

    def handle_starttag(self, tag, attrs):
        tag = tag.casefold()
        values = dict(attrs)
        classes = set(values.get("class", "").casefold().split())
        excluded = (self.stack[-1][1] if self.stack else False) or (
            tag in EXCLUDED_TAGS or bool(classes & EXCLUDED_CLASSES)
        )
        marked = (self.stack[-1][2] if self.stack else False) or tag in MARKED_TAGS
        if tag not in VOID_TAGS:
            self.stack.append((tag, excluded, marked))
        if self.stopped or excluded:
            return
        if tag in {"p", "h2", "h3", "h4", "h5", "h6"}:
            self._finish()
            self.current = {"tag": tag, "plain": [], "unmarked": []}
        elif tag == "br" and self.current:
            self.current["plain"].append(" ")
            self.current["unmarked"].append(" ")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag.casefold() not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        tag = tag.casefold()
        if self.current and self.current["tag"] == tag:
            self._finish()
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        if not self.current or self.stopped:
            return
        excluded = self.stack[-1][1] if self.stack else False
        if excluded:
            return
        self.current["plain"].append(data)
        marked = self.stack[-1][2] if self.stack else False
        self.current["unmarked"].append(" " if marked else data)

    def close(self):
        super().close()
        self._finish()

    def _finish(self):
        if not self.current:
            return
        block = {
            "tag": self.current["tag"],
            "plain": normalize("".join(self.current["plain"])),
            "unmarked": normalize("".join(self.current["unmarked"])),
        }
        self.current = None
        if not block["plain"]:
            return
        if block["tag"].startswith("h") and block["plain"].casefold() in TAIL_SECTIONS:
            self.stopped = True
            return
        self.blocks.append(block)


def extract_blocks(rendered_html):
    parser = RenderedProseParser()
    parser.feed(rendered_html)
    parser.close()
    return parser.blocks


def request_parameters(revision_id):
    return {
        "action": "parse",
        "format": "json",
        "formatversion": "2",
        "oldid": str(revision_id),
        "prop": "text|wikitext|revid",
        "disableeditsection": "1",
        "disabletoc": "1",
        "disablelimitreport": "1",
        "maxlag": "5",
    }


def fetch_parse(revision_id, cache_directory, offline=False):
    path = cache_directory / f"{revision_id}.json"
    if path.exists():
        raw = path.read_bytes()
    elif offline:
        raise FileNotFoundError(f"Missing cached API response: {path}")
    else:
        url = API + "?" + urllib.parse.urlencode(request_parameters(revision_id))
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    raw = response.read()
                payload = json.loads(raw)
                if payload.get("error", {}).get("code") == "maxlag":
                    raise urllib.error.URLError("MediaWiki maxlag")
                if (
                    "parse" not in payload and
                    payload.get("error", {}).get("code") != "nosuchrevid"
                ):
                    raise ValueError(f"MediaWiki parse error for revision {revision_id}: {payload}")
                cache_directory.mkdir(parents=True, exist_ok=True)
                temporary = path.with_suffix(".tmp")
                temporary.write_bytes(raw)
                temporary.replace(path)
                time.sleep(0.1)
                break
            except (urllib.error.HTTPError, urllib.error.URLError) as error:
                if attempt == 4:
                    raise
                headers = getattr(error, "headers", None)
                retry_after = headers.get("Retry-After") if headers else None
                time.sleep(float(retry_after) if retry_after else 2 ** attempt)
    payload = json.loads(raw)
    if (
        "parse" not in payload and
        payload.get("error", {}).get("code") != "nosuchrevid"
    ):
        raise ValueError(f"Cached MediaWiki parse error for revision {revision_id}: {payload}")
    return raw, payload.get("parse"), payload.get("error")


def queued_rows(candidate_ledger):
    columns = candidate_ledger["row_columns"]
    rows = [
        dict(zip(columns, values)) for values in candidate_ledger["rows"]
        if values[columns.index("state")] == "queued_for_desk_screen"
    ]
    for form in {row["canonical_form"] for row in rows}:
        ranks = [row["queue_rank"] for row in rows if row["canonical_form"] == form]
        if ranks != list(range(1, len(ranks) + 1)):
            raise ValueError(f"Non-contiguous frozen queue ranks for {form}.")
    return rows


def lead_summary(paragraphs, form, target_class, sense_count, ngsl):
    forms = {form: sense_count}
    contiguous = mwe_leads(paragraphs, ngsl, forms)
    gaps = (
        mwe_gap_leads(paragraphs, ngsl, forms, maximum_gap=8)
        if target_class == "VPC" else []
    )
    return contiguous, gaps


def build(design, candidate_ledger, ngsl_profile, bnc_coca_profile,
          cache_directory, offline=False):
    if candidate_ledger["design_id"] != design["design_id"]:
        raise ValueError("Candidate-ledger design ID mismatch.")
    if candidate_ledger["inputs"]["design_sha256"] != sha256_file(DESIGN):
        raise ValueError("Candidate-ledger design hash mismatch.")
    if candidate_ledger["inputs"]["ngsl_profile_sha256"] != sha256_file(NGSL):
        raise ValueError("Candidate-ledger NGSL hash mismatch.")
    if sha256_file(Path(bnc_coca_profile["_path"])) != EXPECTED_BNC_COCA_SHA256:
        raise ValueError("BNC/COCA profile is not the reviewed local-only artifact.")

    ngsl = dict(ngsl_profile["rows"])
    bnc_coca = dict(bnc_coca_profile["rows"])
    targets = {item["canonical_form"]: item for item in design["target_derivation"]["targets"]}
    minimum, maximum = design["passage_constraints"]["profile_token_range_inclusive"]
    desk_limit = design["sampling"]["maximum_desk_screens_per_target"]
    desk_counts = Counter()
    rows = []
    for frozen in queued_rows(candidate_ledger):
        form = frozen["canonical_form"]
        if desk_counts[form] == desk_limit:
            continue
        raw, parsed, api_error = fetch_parse(
            frozen["revision_id"], cache_directory, offline
        )
        base = {
            "canonical_form": frozen["canonical_form"],
            "page_id": frozen["page_id"],
            "revision_id": frozen["revision_id"],
            "revision_timestamp": frozen["revision_timestamp"],
            "title": frozen["title"],
            "queue_rank": frozen["queue_rank"],
            "other_candidate_forms": frozen["other_candidate_forms"],
            "api_response_sha256": sha256_bytes(raw),
            "source_text_sha256": frozen["source_text_sha256"],
        }
        if not parsed:
            rows.append(base | {
                "source_identity_state": "unverified_revision_unavailable",
                "api_error_code": api_error["code"],
                "rendered_html_sha256": None,
                "extracted_text_sha256": None,
                "block_count": None,
                "paragraph_count": None,
                "heading_count": None,
                "profile_token_count": None,
                "profile_type_count": None,
                "ngsl_1k_token_coverage": None,
                "ngsl_1k_type_coverage": None,
                "ngsl_2k_token_coverage": None,
                "ngsl_2k_type_coverage": None,
                "bnc_coca_1k_token_coverage": None,
                "bnc_coca_1k_type_coverage": None,
                "bnc_coca_2k_token_coverage": None,
                "bnc_coca_2k_type_coverage": None,
                "contiguous_lead_count": None,
                "gap_lead_count": None,
                "gap_size_counts": [],
                "unmarked_contiguous_lead_count": None,
                "unmarked_gap_lead_count": None,
                "desk_screen_rank": None,
                "mechanical_state": "mechanically_excluded",
                "exclusion_reasons": ["pinned_revision_unavailable_from_api"],
            })
            continue
        if (
            parsed.get("pageid") != frozen["page_id"] or
            parsed.get("revid") != frozen["revision_id"] or
            parsed.get("title") != frozen["title"]
        ):
            raise ValueError(f"Frozen page identity mismatch: {frozen['revision_id']}")
        source = parsed.get("wikitext", "")
        if sha256_bytes(source.encode()) != frozen["source_text_sha256"]:
            raise ValueError(f"Frozen source-text hash mismatch: {frozen['revision_id']}")
        rendered_html = parsed.get("text", "")
        blocks = extract_blocks(rendered_html)
        paragraphs = [block["plain"] for block in blocks if block["tag"] == "p"]
        unmarked = [block["unmarked"] for block in blocks if block["tag"] == "p"]
        text = "\n\n".join(block["plain"] for block in blocks)
        target = targets[form]
        contiguous, gaps = lead_summary(
            paragraphs, frozen["canonical_form"], target["target_class"],
            target["oewn_sense_count"], ngsl,
        )
        unmarked_contiguous, unmarked_gaps = lead_summary(
            unmarked, frozen["canonical_form"], target["target_class"],
            target["oewn_sense_count"], ngsl,
        )
        profile = word_profile(text, ngsl, bnc_coca)
        reasons = []
        if not minimum <= profile["token_count"] <= maximum:
            reasons.append("outside_frozen_token_range")
        if not contiguous and not gaps:
            reasons.append("no_target_lead_in_rendered_main_prose")
        elif not unmarked_contiguous and not unmarked_gaps:
            reasons.append("target_lead_only_in_linked_emphasized_or_block_quote_text")
        if not reasons:
            desk_counts[form] += 1
        gap_sizes = Counter(item["gap_token_count"] for item in gaps)
        rows.append(base | {
            "source_identity_state": "verified_against_dump_wikitext_sha256",
            "api_error_code": None,
            "rendered_html_sha256": sha256_bytes(rendered_html.encode()),
            "extracted_text_sha256": sha256_bytes(text.encode()),
            "block_count": len(blocks),
            "paragraph_count": len(paragraphs),
            "heading_count": len(blocks) - len(paragraphs),
            "profile_token_count": profile["token_count"],
            "profile_type_count": profile["type_count"],
            "ngsl_1k_token_coverage": profile["ngsl_1000"]["token_coverage"],
            "ngsl_1k_type_coverage": profile["ngsl_1000"]["type_coverage"],
            "ngsl_2k_token_coverage": profile["ngsl_2000"]["token_coverage"],
            "ngsl_2k_type_coverage": profile["ngsl_2000"]["type_coverage"],
            "bnc_coca_1k_token_coverage": profile["bnc_coca_1k"]["token_coverage"],
            "bnc_coca_1k_type_coverage": profile["bnc_coca_1k"]["type_coverage"],
            "bnc_coca_2k_token_coverage": profile["bnc_coca_2k"]["token_coverage"],
            "bnc_coca_2k_type_coverage": profile["bnc_coca_2k"]["type_coverage"],
            "contiguous_lead_count": len(contiguous),
            "gap_lead_count": len(gaps),
            "gap_size_counts": [[size, count] for size, count in sorted(gap_sizes.items())],
            "unmarked_contiguous_lead_count": len(unmarked_contiguous),
            "unmarked_gap_lead_count": len(unmarked_gaps),
            "desk_screen_rank": desk_counts[form] if not reasons else None,
            "mechanical_state": "mechanically_excluded" if reasons else "eligible_for_desk_review",
            "exclusion_reasons": reasons,
        })

    if set(desk_counts.values()) != {desk_limit} or len(desk_counts) != len(targets):
        raise ValueError(f"Frozen queues did not supply {desk_limit} mechanical eligibles: {desk_counts}")
    summaries = []
    for target in design["target_derivation"]["targets"]:
        target_rows = [row for row in rows if row["canonical_form"] == target["canonical_form"]]
        reasons = Counter(reason for row in target_rows for reason in row["exclusion_reasons"])
        summaries.append({
            "canonical_form": target["canonical_form"],
            "rendered_queue_row_count": len(target_rows),
            "eligible_for_desk_review_count": sum(
                row["mechanical_state"] == "eligible_for_desk_review" for row in target_rows
            ),
            "exclusion_reason_counts": dict(sorted(reasons.items())),
            "contiguous_lead_page_count": sum(bool(row["contiguous_lead_count"]) for row in target_rows),
            "gap_only_lead_page_count": sum(
                not row["contiguous_lead_count"] and bool(row["gap_lead_count"])
                for row in target_rows
            ),
        })
    columns = list(rows[0])
    return {
        "ledger_schema_version": "1.0.0",
        "ledger_id": "gate1-simplewiki-route2-rendered-screen-v1",
        "generated_on": "2026-09-02",
        "design_id": design["design_id"],
        "inputs": {
            "design_sha256": sha256_file(DESIGN),
            "candidate_ledger_sha256": sha256_file(CANDIDATES),
            "ngsl_profile_id": ngsl_profile["identity"]["profile_id"],
            "ngsl_profile_sha256": sha256_file(NGSL),
            "bnc_coca_profile_id": bnc_coca_profile["identity"]["profile_id"],
            "bnc_coca_profile_sha256": EXPECTED_BNC_COCA_SHA256,
            "bnc_coca_delivery": "local_only_not_bundled",
        },
        "acquisition": {
            "api": API,
            "retrieved_on": "2026-09-02",
            "request_parameters_except_oldid": request_parameters("REVISION_ID") | {"oldid": "REVISION_ID"},
            "user_agent": USER_AGENT,
            "cache_delivery": "local_only_not_bundled",
            "rendering_limit": "The old-revision wikitext is hash-verified, but the API rendering may expand templates with parser and template state current at retrieval; exact response and rendered-HTML hashes therefore identify this cached rendering snapshot.",
        },
        "construct": {
            "purpose": "prose-free rendered-boundary and lexical-profile screen before exhaustive desk review",
            "main_prose_rule": "Rendered paragraphs and h2-h6 headings before frozen tail sections; exclude tables, lists, media, references, navigation, captions, and page furniture.",
            "ordinary_target_rule": "Require a focal lead in a retained paragraph after suppressing hyperlink, bold, italic, emphasis, and block-quote text.",
            "excluded_inferences": [
                "MWE occurrence truth", "VPC or VID category", "idiomaticity",
                "contextual sense", "target centrality", "passage coherence",
                "content suitability", "learner knowledge", "comprehension",
                "passage admission", "95 or 98 percent threshold attainment",
            ],
            "article_text_bundled": False,
            "rendered_html_bundled": False,
            "contributor_data_bundled": False,
        },
        "summary": {
            "rendered_queue_row_count": len(rows),
            "unique_revision_count": len({row["revision_id"] for row in rows}),
            "eligible_for_desk_review_count": sum(
                row["mechanical_state"] == "eligible_for_desk_review" for row in rows
            ),
            "eligible_unique_revision_count": len({
                row["revision_id"] for row in rows
                if row["mechanical_state"] == "eligible_for_desk_review"
            }),
            "eligible_cross_target_flag_row_count": sum(
                row["mechanical_state"] == "eligible_for_desk_review" and
                bool(row["other_candidate_forms"])
                for row in rows
            ),
            "mechanically_excluded_row_count": sum(
                row["mechanical_state"] == "mechanically_excluded" for row in rows
            ),
            "verified_source_row_count": sum(
                row["source_identity_state"] == "verified_against_dump_wikitext_sha256"
                for row in rows
            ),
            "unavailable_revision_row_count": sum(
                row["source_identity_state"] == "unverified_revision_unavailable"
                for row in rows
            ),
            "targets": summaries,
        },
        "row_columns": columns,
        "rows": [[row[column] for column in columns] for row in rows],
    }


def self_check():
    html = (
        '<div class="mw-parser-output"><table><tr><td><p>Skip me.</p></td></tr></table>'
        '<h2>History</h2><p>They <a href="#">took it in</a> and took the scene in.<sup>1</sup></p>'
        '<h2>References</h2><p>Skip this tail.</p></div>'
    )
    blocks = extract_blocks(html)
    assert [(block["tag"], block["plain"]) for block in blocks] == [
        ("h2", "History"),
        ("p", "They took it in and took the scene in."),
    ]
    assert blocks[1]["unmarked"] == "They and took the scene in."
    ngsl = {"took": [["take", 59]]}
    plain = lead_summary([blocks[1]["plain"]], "take in", "VPC", 17, ngsl)
    unmarked = lead_summary([blocks[1]["unmarked"]], "take in", "VPC", 17, ngsl)
    assert len(plain[1]) == 3 and len(unmarked[1]) == 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bnc_coca", type=Path, nargs="?")
    parser.add_argument("--cache", type=Path, default=CACHE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("SimpleWiki Route 2 rendered-screen self-check: PASS")
        return
    if not args.bnc_coca:
        parser.error("bnc_coca is required")
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    ngsl = json.loads(NGSL.read_text(encoding="utf-8"))
    bnc_coca = json.loads(args.bnc_coca.read_text(encoding="utf-8"))
    bnc_coca["_path"] = str(args.bnc_coca)
    result = build(design, candidates, ngsl, bnc_coca, args.cache, args.check)
    rendered = json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Generated rendered screen differs from {args.output}")
        print(f"SimpleWiki Route 2 rendered-screen verification: PASS ({args.output})")
    else:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
