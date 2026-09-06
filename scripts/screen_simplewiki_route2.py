#!/usr/bin/env python3
"""Build the prose-free candidate queue for the frozen SimpleWiki Route 2 design."""

import argparse
import bz2
import hashlib
import html
import io
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

from profile_voa_material_candidates import mwe_gap_leads, mwe_leads


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "resources/simplewiki_gate1_route2_design.json"
NGSL = ROOT / "resources/ngsl_1_2_ascii_forms.json"
OUTPUT = ROOT / "resources/simplewiki_gate1_route2_candidates.json"
TAIL_SECTIONS = {
    "external links", "further reading", "notes", "other websites",
    "references", "related pages", "sources",
}
PAGE_TITLE = re.compile(r"^(glossary|index|list|timeline) of\b", re.I)
DATE_TITLE = re.compile(r"^(?:\d{1,4}|\d{1,2} [A-Za-z]+|[A-Za-z]+ \d{1,2})$")
DISAMBIG = re.compile(r"\{\{\s*(?:disambig|disambiguation|geodis|hndis)\b", re.I)
COMMENT = re.compile(r"<!--.*?-->", re.S)
BLOCK_TAG = re.compile(
    r"<(?:gallery|math|pre|syntaxhighlight|timeline)\b[^>]*>.*?</(?:gallery|math|pre|syntaxhighlight|timeline)\s*>",
    re.I | re.S,
)
REF = re.compile(r"<ref\b[^>]*>.*?</ref\s*>|<ref\b[^>]*/\s*>", re.I | re.S)
TAG = re.compile(r"<[^>]+>")
LINK = re.compile(r"\[\[([^\[\]]+)\]\]")
EXTERNAL_LINK = re.compile(r"\[(?:https?|ftp)://[^\s\]]+(?:\s+([^\]]+))?\]", re.I)
HEADING = re.compile(r"^\s*(=+)\s*(.*?)\s*\1\s*$")


def file_digest(path, algorithm):
    digest = hashlib.new(algorithm)
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def drop_balanced(text, opening, closing):
    output = []
    depth = 0
    index = 0
    while index < len(text):
        if text.startswith(opening, index):
            depth += 1
            index += len(opening)
        elif depth and text.startswith(closing, index):
            depth -= 1
            index += len(closing)
        else:
            if not depth:
                output.append(text[index])
            index += 1
    return "".join(output)


def replace_links(text):
    def replacement(match):
        body = match.group(1)
        target = body.split("|", 1)[0].strip().casefold()
        if target.startswith(("category:", "file:", "image:")):
            return " "
        return body.rsplit("|", 1)[-1]

    for _ in range(10):
        text, count = LINK.subn(replacement, text)
        if not count:
            break
    return text


def visible_paragraphs(wikitext):
    text = COMMENT.sub(" ", wikitext)
    text = BLOCK_TAG.sub(" ", text)
    text = REF.sub(" ", text)
    text = drop_balanced(text, "{|", "|}")
    text = drop_balanced(text, "{{", "}}")
    text = replace_links(text)
    text = EXTERNAL_LINK.sub(lambda match: match.group(1) or " ", text)
    text = html.unescape(TAG.sub(" ", text)).replace("'''", "").replace("''", "")
    paragraphs = []
    skip_tail = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        heading = HEADING.match(line)
        if heading:
            if heading.group(2).strip().casefold() in TAIL_SECTIONS:
                skip_tail = True
            continue
        if skip_tail or not line or line.startswith(("*", "#", ";", ":", "|", "!")):
            continue
        paragraphs.append(re.sub(r"\s+", " ", line))
    return paragraphs


def page_records(source):
    for _, element in ET.iterparse(source, events=("end",)):
        if element.tag.rsplit("}", 1)[-1] != "page":
            continue
        revision = element.find("{*}revision")
        text = revision.find("{*}text") if revision is not None else None
        yield {
            "title": element.findtext("{*}title") or "",
            "namespace": int(element.findtext("{*}ns") or -1),
            "page_id": int(element.findtext("{*}id") or 0),
            "redirect": element.find("{*}redirect") is not None,
            "revision_id": int(revision.findtext("{*}id") or 0),
            "revision_timestamp": revision.findtext("{*}timestamp"),
            "wikitext": text.text if text is not None and text.text else "",
        }
        element.clear()


def page_class_reasons(page):
    title = page["title"].strip()
    reasons = []
    if page["namespace"] != 0:
        reasons.append("not_main_namespace")
    if page["redirect"]:
        reasons.append("redirect")
    if (PAGE_TITLE.search(title) or DATE_TITLE.fullmatch(title) or
            title.casefold().endswith("(disambiguation)")):
        reasons.append("excluded_title_class")
    if DISAMBIG.search(page["wikitext"]):
        reasons.append("disambiguation_template")
    return reasons


def selection_hash(design_id, form, page_id, revision_id):
    value = f"{design_id}\n{form}\n{page_id}\n{revision_id}"
    return hashlib.sha256(value.encode()).hexdigest()


def matcher_config(ngsl, targets):
    forms = {item["canonical_form"]: item["oewn_sense_count"] for item in targets}
    vpc_forms = {
        item["canonical_form"]: item["oewn_sense_count"]
        for item in targets if item["target_class"] == "VPC"
    }
    verbs = {item["canonical_form"].split()[0] for item in targets}
    surfaces = {
        surface for surface, heads in ngsl.items()
        if any(head in verbs for head, _ in heads)
    } | verbs
    verb_filter = re.compile(
        r"(?<![A-Za-z])(?:" + "|".join(map(re.escape, sorted(surfaces))) + r")(?![A-Za-z])",
        re.I,
    )
    return forms, vpc_forms, verb_filter


def lead_counts(paragraphs, title, ngsl, matcher):
    forms, vpc_forms, verb_filter = matcher
    relevant = [paragraph for paragraph in paragraphs if verb_filter.search(paragraph)]
    contiguous = Counter(item["canonical_form"] for item in mwe_leads(relevant, ngsl, forms))
    gaps = mwe_gap_leads(relevant, ngsl, vpc_forms, maximum_gap=8)
    gap_counts = Counter(item["canonical_form"] for item in gaps)
    gap_sizes = defaultdict(Counter)
    for item in gaps:
        gap_sizes[item["canonical_form"]][item["gap_token_count"]] += 1
    title_forms = {
        item["canonical_form"] for item in mwe_leads([title], ngsl, forms)
    }
    return contiguous, gap_counts, gap_sizes, title_forms


def build(design, ngsl_profile, dump_path):
    source = design["source_frame"]
    if dump_path.stat().st_size != source["artifact_size_bytes"]:
        raise ValueError("SimpleWiki dump size does not match the frozen design.")
    dump_sha1 = file_digest(dump_path, "sha1")
    if dump_sha1 != source["artifact_sha1"]:
        raise ValueError("SimpleWiki dump SHA-1 does not match the frozen design.")
    ngsl = dict(ngsl_profile["rows"])
    targets = design["target_derivation"]["targets"]
    matcher = matcher_config(ngsl, targets)
    rows = []
    main_article_count = 0
    with bz2.open(dump_path, "rb") as source_file:
        for page in page_records(source_file):
            if page["namespace"] != 0:
                continue
            main_article_count += 1
            if not matcher[2].search(page["wikitext"]):
                continue
            paragraphs = visible_paragraphs(page["wikitext"])
            contiguous, gaps, gap_sizes, title_forms = lead_counts(
                paragraphs, page["title"], ngsl, matcher
            )
            for target in targets:
                form = target["canonical_form"]
                if not contiguous[form] and not gaps[form]:
                    continue
                reasons = page_class_reasons(page)
                if form in title_forms:
                    reasons.append("target_in_title")
                rows.append({
                    "canonical_form": form,
                    "page_id": page["page_id"],
                    "revision_id": page["revision_id"],
                    "revision_timestamp": page["revision_timestamp"],
                    "title": page["title"],
                    "source_text_sha256": hashlib.sha256(
                        page["wikitext"].encode()
                    ).hexdigest(),
                    "contiguous_lead_count": contiguous[form],
                    "gap_lead_count": gaps[form],
                    "gap_size_counts": [
                        [size, count] for size, count in sorted(gap_sizes[form].items())
                    ],
                    "selection_hash": selection_hash(
                        design["design_id"], form, page["page_id"], page["revision_id"]
                    ),
                    "state": "mechanically_excluded" if reasons else "candidate",
                    "exclusion_reasons": reasons,
                })

    priorities = {
        item["canonical_form"]: item["priority"] for item in targets
    }
    forms_by_page = defaultdict(set)
    for row in rows:
        if row["state"] == "candidate":
            forms_by_page[row["page_id"]].add(row["canonical_form"])
    summaries = []
    for target in targets:
        form = target["canonical_form"]
        target_rows = sorted(
            (row for row in rows if row["canonical_form"] == form),
            key=lambda row: row["selection_hash"],
        )
        queue_rank = 0
        for row in target_rows:
            if row["state"] != "candidate":
                continue
            queue_rank += 1
            row["state"] = "queued_for_desk_screen"
            row["queue_rank"] = queue_rank
            row["other_candidate_forms"] = sorted(forms_by_page[row["page_id"]] - {form})
        states = Counter(row["state"] for row in target_rows)
        summaries.append({
            "canonical_form": form,
            "priority": priorities[form],
            "raw_candidate_page_count": len(target_rows),
            "mechanically_excluded_page_count": states["mechanically_excluded"],
            "cross_target_candidate_page_count": sum(
                bool(row.get("other_candidate_forms")) for row in target_rows
            ),
            "queue_page_count": states["queued_for_desk_screen"],
        })

    rows.sort(key=lambda row: (
        priorities[row["canonical_form"]], row["selection_hash"], row["page_id"]
    ))
    columns = [
        "canonical_form", "page_id", "revision_id", "revision_timestamp", "title",
        "source_text_sha256", "contiguous_lead_count", "gap_lead_count",
        "gap_size_counts", "selection_hash", "state", "exclusion_reasons",
        "queue_rank", "other_candidate_forms",
    ]
    return {
        "ledger_schema_version": "1.0.0",
        "ledger_id": "gate1-simplewiki-route2-candidates-v1",
        "generated_on": "2026-09-02",
        "design_id": design["design_id"],
        "inputs": {
            "design_sha256": file_digest(DESIGN, "sha256"),
            "ngsl_profile_sha256": file_digest(NGSL, "sha256"),
            "dump_name": dump_path.name,
            "dump_size_bytes": dump_path.stat().st_size,
            "dump_sha1": dump_sha1,
        },
        "construct": {
            "purpose": "prose-free deterministic candidate queue before desk review",
            "excluded_inferences": [
                "rendered passage eligibility", "MWE occurrence truth",
                "category or idiomaticity truth", "contextual sense",
                "target centrality", "learner knowledge", "comprehension",
                "MWE prevalence", "representative lexical coverage",
            ],
            "known_recall_limit": "Candidate-only stdlib wikitext projection removes templates, tables, list lines, media, references, and tail matter; final review must use the pinned rendered revision and search the complete retained prose.",
            "article_text_bundled": False,
            "contributor_data_bundled": False,
        },
        "summary": {
            "main_namespace_page_count": main_article_count,
            "target_page_rows": len(rows),
            "unique_candidate_page_count": len({row["page_id"] for row in rows}),
            "targets": summaries,
        },
        "row_columns": columns,
        "rows": [[row.get(column) for column in columns] for row in rows],
    }


def self_check():
    xml = b"""<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.11/"><page><title>Example</title><ns>0</ns><id>7</id><revision><id>11</id><timestamp>2026-01-01T00:00:00Z</timestamp><text sha1="abc">{{box|take in}}\nThey took it fully in.\n== References ==\nThey pick up.</text></revision></page></mediawiki>"""
    page = next(page_records(io.BytesIO(xml)))
    assert page["page_id"] == 7 and page["revision_id"] == 11
    paragraphs = visible_paragraphs(page["wikitext"])
    assert paragraphs == ["They took it fully in."]
    ngsl = {"took": [["take", 59]]}
    targets = [{
        "canonical_form": "take in", "target_class": "VPC", "oewn_sense_count": 17
    }]
    matcher = matcher_config(ngsl, targets)
    contiguous, gaps, gap_sizes, title_forms = lead_counts(
        paragraphs, page["title"], ngsl, matcher
    )
    assert not contiguous and gaps["take in"] == 1
    assert gap_sizes["take in"] == Counter({2: 1}) and not title_forms
    assert selection_hash("d", "take in", 7, 11) == hashlib.sha256(
        b"d\ntake in\n7\n11"
    ).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dump", type=Path, nargs="?")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("SimpleWiki Route 2 candidate-screen self-check: PASS")
        return
    if not args.dump:
        parser.error("dump is required")
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    ngsl = json.loads(NGSL.read_text(encoding="utf-8"))
    result = build(design, ngsl, args.dump)
    rendered = json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Generated candidate ledger differs from {args.output}")
        print(f"SimpleWiki Route 2 candidate-ledger verification: PASS ({args.output})")
    else:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
