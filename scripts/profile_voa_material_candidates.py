#!/usr/bin/env python3
"""Profile source-eligible VOA articles without admitting passages or MWEs."""

import argparse
import hashlib
import itertools
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from extract_voa_articles import extract


ROOT = Path(__file__).parents[1]
WORD = re.compile(r"(?<!\w)[A-Za-z]+(?!\w)")
MWE_TOKEN = re.compile(r"(?<!\w)[A-Za-z]+(?:['’][A-Za-z]+)*(?!\w)")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ratio(numerator, denominator):
    return {
        "numerator": numerator,
        "denominator": denominator,
        "value": round(numerator / denominator, 6) if denominator else None,
    }


def word_profile(text, ngsl, bnc_coca=None):
    tokens = [item.lower() for item in WORD.findall(unicodedata.normalize("NFKC", text))]
    counts = Counter(tokens)
    result = {"token_count": len(tokens), "type_count": len(counts)}
    for cutoff in (1000, 2000):
        matched = {word for word in counts if word in ngsl and ngsl[word][0][1] <= cutoff}
        result[f"ngsl_{cutoff}"] = {
            "token_coverage": ratio(sum(counts[word] for word in matched), len(tokens)),
            "type_coverage": ratio(len(matched), len(counts)),
        }
    if bnc_coca:
        for level in (1, 2):
            matched = {
                word for word in counts
                if word in bnc_coca and bnc_coca[word][0][1] <= level
            }
            result[f"bnc_coca_{level}k"] = {
                "token_coverage": ratio(sum(counts[word] for word in matched), len(tokens)),
                "type_coverage": ratio(len(matched), len(counts)),
            }
    return result


def mwe_leads(paragraphs, ngsl, forms):
    by_length = defaultdict(dict)
    for form, sense_count in forms.items():
        by_length[len(form.split())][form] = sense_count
    leads = []
    global_position = 0
    for paragraph_index, paragraph in enumerate(paragraphs, 1):
        tokens = [match.group().replace("’", "'").lower()
                  for match in MWE_TOKEN.finditer(paragraph)]
        for start in range(len(tokens)):
            for length, candidates in by_length.items():
                window = tokens[start:start + length]
                if len(window) != length:
                    continue
                options = [dict.fromkeys(
                    [token] + [lemma for lemma, _ in ngsl.get(token, [])]
                ) for token in window]
                for members in itertools.product(*options):
                    canonical = " ".join(members)
                    if canonical in candidates:
                        leads.append({
                            "paragraph": paragraph_index,
                            "mwe_token_start": global_position + start + 1,
                            "mwe_token_end": global_position + start + length,
                            "surface_form": " ".join(window),
                            "canonical_form": canonical,
                            "oewn_sense_count": candidates[canonical],
                        })
        global_position += len(tokens)
    return sorted(
        {(
            item["paragraph"], item["mwe_token_start"], item["mwe_token_end"],
            item["canonical_form"],
        ): item for item in leads}.values(),
        key=lambda item: (item["mwe_token_start"], item["mwe_token_end"],
                          item["canonical_form"]),
    )


def mwe_gap_leads(paragraphs, ngsl, forms, maximum_gap=2):
    by_first = defaultdict(list)
    for form, sense_count in forms.items():
        members = form.split()
        if len(members) == 2:
            by_first[members[0]].append((members[1], form, sense_count))
    leads = []
    global_position = 0
    for paragraph_index, paragraph in enumerate(paragraphs, 1):
        tokens = [match.group().replace("’", "'").lower()
                  for match in MWE_TOKEN.finditer(paragraph)]
        options = [set([token] + [lemma for lemma, _ in ngsl.get(token, [])])
                   for token in tokens]
        for start in range(len(tokens)):
            candidates = {
                row for option in options[start] for row in by_first.get(option, [])
            }
            for end in range(
                start + 2, min(len(tokens), start + maximum_gap + 2)
            ):
                for second, canonical, sense_count in candidates:
                    if second in options[end]:
                        leads.append({
                            "paragraph": paragraph_index,
                            "mwe_member_token_positions": [
                                global_position + start + 1,
                                global_position + end + 1,
                            ],
                            "gap_token_count": end - start - 1,
                            "surface_span": " ".join(tokens[start:end + 1]),
                            "canonical_form": canonical,
                            "oewn_sense_count": sense_count,
                        })
        global_position += len(tokens)
    return sorted(
        {(
            item["paragraph"], tuple(item["mwe_member_token_positions"]),
            item["canonical_form"],
        ): item for item in leads}.values(),
        key=lambda item: (*item["mwe_member_token_positions"], item["canonical_form"]),
    )


def recurrence_summary(occurrences):
    result = []
    for form, items in occurrences.items():
        article_ids = sorted({article_id for article_id, _ in items})
        result.append({
            "canonical_form": form,
            "oewn_sense_count": items[0][1]["oewn_sense_count"],
            "occurrence_count": len(items),
            "document_frequency": len(article_ids),
            "article_ids": article_ids,
        })
    return sorted(result, key=lambda item: (
        -item["document_frequency"], -item["occurrence_count"], item["canonical_form"]
    ))


def build(screen, directory, ngsl_profile, oewn_profile, paths, bnc_coca_profile=None):
    ngsl = dict(ngsl_profile["rows"])
    forms = dict(oewn_profile["rows"])
    bnc_coca = dict(bnc_coca_profile["rows"]) if bnc_coca_profile else None
    articles = []
    occurrences = defaultdict(list)
    gap_occurrences = defaultdict(list)
    for decision in screen["decisions"]:
        if decision["state"] != "eligible":
            continue
        extracted = extract(directory / decision["source_file"])
        for field in ("canonical_url", "source_sha256", "text_sha256", "paragraph_count"):
            if extracted[field] != decision[field]:
                raise ValueError(f"Frozen {field} mismatch: {decision['source_file']}")
        article_id = (
            f"{decision['sampling_category']}-"
            f"{decision['target_blind_queue_rank']:02d}"
        )
        paragraphs = extracted["text"].split("\n\n")
        leads = mwe_leads(paragraphs, ngsl, forms)
        gap_leads = mwe_gap_leads(paragraphs, ngsl, forms)
        for index, lead in enumerate(leads, 1):
            lead["lead_id"] = f"{article_id}-lead-{index:03d}"
            occurrences[lead["canonical_form"]].append((article_id, lead))
        for index, lead in enumerate(gap_leads, 1):
            lead["lead_id"] = f"{article_id}-gap-lead-{index:03d}"
            gap_occurrences[lead["canonical_form"]].append((article_id, lead))
        articles.append({
            "article_id": article_id,
            "sampling_category": decision["sampling_category"],
            "target_blind_queue_rank": decision["target_blind_queue_rank"],
            "title": extracted["title"],
            "canonical_url": extracted["canonical_url"],
            "publication_time": extracted["publication_time"],
            "source_sha256": extracted["source_sha256"],
            "text_sha256": extracted["text_sha256"],
            "paragraph_count": extracted["paragraph_count"],
            "word_profile": word_profile(extracted["text"], ngsl, bnc_coca),
            "automatic_oewn_lead_count": len(leads),
            "automatic_oewn_leads": leads,
            "automatic_oewn_gap_lead_count": len(gap_leads),
            "automatic_oewn_gap_leads": gap_leads,
        })
    recurrence = recurrence_summary(occurrences)
    gap_recurrence = recurrence_summary(gap_occurrences)
    inputs = {
        "source_screen_sha256": sha256(paths["screen"]),
        "ngsl_profile_id": ngsl_profile["identity"]["profile_id"],
        "ngsl_profile_sha256": sha256(paths["ngsl"]),
        "oewn_profile_id": oewn_profile["identity"]["profile_id"],
        "oewn_profile_sha256": sha256(paths["oewn"]),
    }
    if bnc_coca_profile:
        inputs.update({
            "bnc_coca_profile_id": bnc_coca_profile["identity"]["profile_id"],
            "bnc_coca_profile_sha256": sha256(paths["bnc_coca"]),
            "bnc_coca_delivery": "local_only_not_bundled",
        })
    return {
        "profile_schema_version": "1.0.0",
        "profile_id": "gate1-voa-automated-screen-v1",
        "generated_on": "2026-09-01",
        "source_screen_id": screen["screen_id"],
        "inputs": inputs,
        "construct": {
            "purpose": "target-blind desk-screen prioritization before exhaustive researcher review",
            "word_measure": "ASCII NFKC token/type membership at project-defined NGSL head-rank cutoffs",
            "mwe_lead_rule": "within-paragraph contiguous 2-7-token sequences plus two-member sequences with one or two intervening tokens; project through all exact NGSL surface-to-head mappings and match to OEWN verb forms",
            "excluded_inferences": [
                "MWE occurrence truth", "VPC or VID category", "idiomaticity",
                "contextual sense", "learner knowledge", "comprehension difficulty",
                "passage admission", "95 or 98 percent threshold attainment",
            ],
            "known_recall_limit": "no gap search for forms longer than two members or gaps longer than two tokens; no syntactic, spelling-variant, or out-of-OEWN lead generation",
            "raw_html_bundled": False,
            "article_text_bundled": False,
        },
        "summary": {
            "article_count": len(articles),
            "automatic_oewn_lead_count": sum(
                article["automatic_oewn_lead_count"] for article in articles
            ),
            "distinct_canonical_form_count": len(recurrence),
            "forms_in_multiple_documents": sum(
                item["document_frequency"] > 1 for item in recurrence
            ),
            "automatic_oewn_gap_lead_count": sum(
                article["automatic_oewn_gap_lead_count"] for article in articles
            ),
            "distinct_gap_canonical_form_count": len(gap_recurrence),
            "gap_forms_in_multiple_documents": sum(
                item["document_frequency"] > 1 for item in gap_recurrence
            ),
        },
        "articles": articles,
        "cross_document_recurrence": recurrence,
        "cross_document_gap_recurrence": gap_recurrence,
    }


def self_check():
    ngsl = {
        "ended": [["end", 100]], "took": [["take", 59]],
        "taking": [["take", 59]],
    }
    forms = {"end up": 2, "take part": 1, "take in": 17}
    leads = mwe_leads(["They took part, ended up taking it in."], ngsl, forms)
    assert [(item["surface_form"], item["canonical_form"]) for item in leads] == [
        ("took part", "take part"), ("ended up", "end up")
    ]
    gap_leads = mwe_gap_leads(["They took part, ended up taking it in."], ngsl, forms)
    assert [(item["surface_span"], item["canonical_form"]) for item in gap_leads] == [
        ("taking it in", "take in")
    ]
    assert word_profile("A a difficulty.", {
        "a": [["a", 6]], "difficulty": [["difficulty", 1001]],
    })["ngsl_1000"]["token_coverage"] == ratio(2, 3)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?")
    parser.add_argument("--screen", type=Path,
                        default=ROOT / "resources/voa_gate1_source_screen.json")
    parser.add_argument("--ngsl", type=Path,
                        default=ROOT / "resources/ngsl_1_2_ascii_forms.json")
    parser.add_argument("--oewn", type=Path,
                        default=ROOT / "resources/oewn_2025_multiword_verbs.json")
    parser.add_argument("--bnc-coca", type=Path)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "resources/voa_gate1_automated_profile.json")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("VOA automated material-profile self-check: PASS")
        return
    if not args.directory:
        parser.error("directory is required")
    paths = {"screen": args.screen, "ngsl": args.ngsl, "oewn": args.oewn,
             "bnc_coca": args.bnc_coca}
    bnc_coca = (json.loads(args.bnc_coca.read_text(encoding="utf-8"))
                if args.bnc_coca else None)
    result = build(
        json.loads(args.screen.read_text(encoding="utf-8")), args.directory,
        json.loads(args.ngsl.read_text(encoding="utf-8")),
        json.loads(args.oewn.read_text(encoding="utf-8")), paths, bnc_coca,
    )
    rendered = json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Generated material profile differs from {args.output}")
        print(f"VOA automated material-profile verification: PASS ({args.output})")
    else:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
