#!/usr/bin/env python3
"""Audit exact Kaikki/Wiktionary coverage of the OEWN-unmatched STREUSLE VIDs."""

import argparse
import hashlib
import json
import ssl
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from audit_streusle_oewn_coverage import SLOT_TOKENS, load_verb_entries
from check_streusle_v5 import inspect_checkout
from extract_oewn_take_in import ARTIFACT_SHA256


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = ROOT / "benchmarks/streusle_v5_vpc_vid.json"
DEFAULT_CACHE = ROOT / "research_data/kaikki_en_2026_08_05_vid_exact"
BASE_URL = "https://kaikki.org/dictionary/English/meaning"
USER_AGENT = "LexicalDiversity-LRE-resource-audit/1.0 (aggregate research audit)"
UOFI_PREFIX = "used other than figuratively or idiomatically"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def derive_population(datasets, verbs):
    vid_occurrences = Counter()
    for sentences in datasets.values():
        for sentence in sentences:
            for occurrence in sentence["smwes"].values():
                if occurrence["lexcat"] == "V.VID":
                    vid_occurrences[occurrence["lexlemma"].casefold()] += 1

    skeleton_index = defaultdict(set)
    for lemma in verbs:
        if " " in lemma:
            skeleton = tuple(token for token in lemma.split() if token not in SLOT_TOKENS)
            skeleton_index[skeleton].add(lemma)

    targets = {}
    routes = Counter({
        "exact_oewn_types": 0,
        "exact_oewn_occurrences": 0,
        "polysemous_exact_oewn_types": 0,
        "polysemous_exact_oewn_occurrences": 0,
        "unique_slot_oewn_types": 0,
        "unique_slot_oewn_occurrences": 0,
        "polysemous_unique_slot_oewn_types": 0,
        "polysemous_unique_slot_oewn_occurrences": 0,
    })
    for lemma, occurrences in vid_occurrences.items():
        if lemma in verbs:
            routes["exact_oewn_types"] += 1
            routes["exact_oewn_occurrences"] += occurrences
            if verbs[lemma] >= 2:
                routes["polysemous_exact_oewn_types"] += 1
                routes["polysemous_exact_oewn_occurrences"] += occurrences
            continue
        skeleton = tuple(token for token in lemma.split() if token not in SLOT_TOKENS)
        candidates = skeleton_index.get(skeleton, ())
        if len(candidates) == 1:
            routes["unique_slot_oewn_types"] += 1
            routes["unique_slot_oewn_occurrences"] += occurrences
            if verbs[next(iter(candidates))] >= 2:
                routes["polysemous_unique_slot_oewn_types"] += 1
                routes["polysemous_unique_slot_oewn_occurrences"] += occurrences
            continue
        targets[lemma] = occurrences
    routes["total_vid_types"] = len(vid_occurrences)
    routes["total_vid_occurrences"] = sum(vid_occurrences.values())
    return dict(sorted(targets.items())), dict(routes)


def entry_url(lemma):
    if not lemma:
        raise ValueError("Empty Kaikki lookup lemma.")
    return "/".join((BASE_URL, quote(lemma[0], safe=""),
                     quote(lemma[:2], safe=""), quote(lemma, safe="") + ".jsonl"))


def cache_path(cache, lemma):
    return cache / f"{digest(lemma.encode('utf-8'))}.json"


def fetch_record(lemma, ca_file=None):
    url = entry_url(lemma)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        context = ssl.create_default_context(cafile=str(ca_file)) if ca_file else None
        with urlopen(request, timeout=30, context=context) as response:
            body = response.read()
            status = response.status
            headers = response.headers
    except HTTPError as error:
        if error.code != 404:
            raise
        body = b""
        status = 404
        headers = error.headers
    return {
        "url": url,
        "status": status,
        "last_modified": headers.get("Last-Modified"),
        "etag": headers.get("ETag"),
        "body_sha256": digest(body),
        "body": body.decode("utf-8"),
    }


def load_record(cache, lemma, fetch=False, ca_file=None):
    path = cache_path(cache, lemma)
    if not path.exists():
        if not fetch:
            raise FileNotFoundError(f"Missing cached Kaikki response for target digest {path.stem}.")
        record = fetch_record(lemma, ca_file)
        cache.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
        time.sleep(0.1)
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("url") != entry_url(lemma) or record.get("status") not in (200, 404):
        raise ValueError(f"Invalid cached Kaikki metadata for target digest {path.stem}.")
    body = record.get("body")
    if not isinstance(body, str) or digest(body.encode("utf-8")) != record.get("body_sha256"):
        raise ValueError(f"Invalid cached Kaikki body hash for target digest {path.stem}.")
    return record


def parse_rows(record):
    if record["status"] == 404:
        return []
    rows = []
    for line in record["body"].splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        if not isinstance(entry, dict):
            raise ValueError("Kaikki JSONL row must be an object.")
        rows.append(entry)
    return rows


def parse_entries(rows, lemma):
    return [entry for entry in rows if (
        entry.get("word", "").casefold() == lemma and
        entry.get("lang_code") == "en" and entry.get("pos") == "verb"
    )]


def sense_summary(entries):
    senses = []
    for entry in entries:
        value = entry.get("senses", [])
        if not isinstance(value, list) or any(not isinstance(sense, dict) for sense in value):
            raise ValueError("Kaikki senses must be an array.")
        senses.extend(value)
    glossed = [sense for sense in senses if any(
        isinstance(gloss, str) and gloss.strip() for gloss in sense.get("glosses", [])
    )]
    uofi = [sense for sense in glossed if any(
        gloss.casefold().startswith(UOFI_PREFIX) for gloss in sense.get("glosses", [])
    )]
    lexicalized = [sense for sense in glossed if sense not in uofi and
                   not sense.get("form_of") and not sense.get("alt_of")]
    return {
        "entries": len(entries),
        "senses": len(senses),
        "glossed_senses": len(glossed),
        "lexicalized_candidate_senses": len(lexicalized),
        "uofi_senses": len(uofi),
        "senses_with_wiktionary_senseid": sum(bool(sense.get("senseid")) for sense in senses),
        "lexicalized_senses_with_wiktionary_senseid": sum(
            bool(sense.get("senseid")) for sense in lexicalized
        ),
        "all_lexicalized_senses_have_wiktionary_senseid": bool(lexicalized) and all(
            sense.get("senseid") for sense in lexicalized
        ),
        "senses_with_wikidata_id": sum(bool(sense.get("wikidata")) for sense in senses),
        "senses_with_raw_id_field": sum(bool(sense.get("id")) for sense in senses),
    }


def summarize(targets, records, prior_routes):
    rows = []
    manifest = []
    for lemma, occurrences in targets.items():
        record = records[lemma]
        source_rows = parse_rows(record)
        counts = sense_summary(parse_entries(source_rows, lemma))
        exact_word = any(entry.get("word", "").casefold() == lemma and
                         entry.get("lang_code") == "en" for entry in source_rows)
        rows.append({
            "occurrences": occurrences,
            "http_status": record["status"],
            "source_rows": len(source_rows),
            "exact_english_word": exact_word,
            **counts,
        })
        manifest.append("\0".join((lemma, str(record["status"]), record["body_sha256"],
                                    record.get("last_modified") or "",
                                    record.get("etag") or "")))

    def weighted(predicate):
        return sum(row["occurrences"] for row in rows if predicate(row))

    matched = [row for row in rows if row["entries"]]
    raw_senses = sum(row["senses"] for row in rows)
    stable_senses = sum(row["senses_with_wiktionary_senseid"] for row in rows)
    kaikki_types = len(matched)
    kaikki_occurrences = weighted(lambda row: row["entries"] > 0)
    combined_types = (prior_routes["exact_oewn_types"] +
                      prior_routes["unique_slot_oewn_types"] + kaikki_types)
    combined_occurrences = (prior_routes["exact_oewn_occurrences"] +
                            prior_routes["unique_slot_oewn_occurrences"] +
                            kaikki_occurrences)
    modified = [records[lemma].get("last_modified") for lemma in targets
                if records[lemma].get("last_modified")]
    return {
        "target_population": {
            "types": len(rows),
            "occurrences": sum(row["occurrences"] for row in rows),
            "definition": "STREUSLE V.VID canonical types with neither an exact OEWN verb entry nor a unique fixed article/possessive-slot OEWN candidate",
        },
        "exact_kaikki_coverage": {
            "types_with_verb_entry": len(matched),
            "occurrences_with_verb_entry": weighted(lambda row: row["entries"] > 0),
            "types_with_lexicalized_candidate": sum(
                row["lexicalized_candidate_senses"] > 0 for row in rows
            ),
            "occurrences_with_lexicalized_candidate": weighted(
                lambda row: row["lexicalized_candidate_senses"] > 0
            ),
            "types_with_multiple_lexicalized_candidates": sum(
                row["lexicalized_candidate_senses"] >= 2 for row in rows
            ),
            "occurrences_with_multiple_lexicalized_candidates": weighted(
                lambda row: row["lexicalized_candidate_senses"] >= 2
            ),
            "types_without_exact_verb_entry": len(rows) - len(matched),
            "occurrences_without_exact_verb_entry": weighted(lambda row: row["entries"] == 0),
            "http_200_without_exact_english_verb_entry": sum(
                row["http_status"] == 200 and row["entries"] == 0 for row in rows
            ),
            "http_200_with_exact_word_but_no_verb_entry": sum(
                row["http_status"] == 200 and row["exact_english_word"] and
                row["entries"] == 0 for row in rows
            ),
            "http_200_without_exact_english_word": sum(
                row["http_status"] == 200 and not row["exact_english_word"] for row in rows
            ),
        },
        "combined_lookup_routes": {
            "total_vid_types": prior_routes["total_vid_types"],
            "total_vid_occurrences": prior_routes["total_vid_occurrences"],
            "exact_oewn_types": prior_routes["exact_oewn_types"],
            "exact_oewn_occurrences": prior_routes["exact_oewn_occurrences"],
            "unique_slot_oewn_candidate_types": prior_routes["unique_slot_oewn_types"],
            "unique_slot_oewn_candidate_occurrences": prior_routes["unique_slot_oewn_occurrences"],
            "exact_kaikki_verb_types_after_oewn": kaikki_types,
            "exact_kaikki_verb_occurrences_after_oewn": kaikki_occurrences,
            "types_with_any_unreviewed_dictionary_route": combined_types,
            "occurrences_with_any_unreviewed_dictionary_route": combined_occurrences,
            "type_coverage": round(combined_types / prior_routes["total_vid_types"], 6),
            "occurrence_coverage": round(
                combined_occurrences / prior_routes["total_vid_occurrences"], 6
            ),
            "types_with_multiple_inventory_candidates": (
                prior_routes.get("polysemous_exact_oewn_types", 0) +
                prior_routes.get("polysemous_unique_slot_oewn_types", 0) +
                sum(row["lexicalized_candidate_senses"] >= 2 for row in rows)
            ),
            "warning": "These disjoint lookup routes are unreviewed inventory candidates, not accepted mappings or evidence that multiple senses occur in STREUSLE.",
        },
        "sense_schema": {
            "raw_senses": raw_senses,
            "glossed_senses": sum(row["glossed_senses"] for row in rows),
            "lexicalized_candidate_senses": sum(
                row["lexicalized_candidate_senses"] for row in rows
            ),
            "uofi_literal_fallback_senses": sum(row["uofi_senses"] for row in rows),
            "senses_with_wiktionary_senseid": stable_senses,
            "senseid_coverage": round(stable_senses / raw_senses, 6) if raw_senses else None,
            "lexicalized_senses_with_wiktionary_senseid": sum(
                row["lexicalized_senses_with_wiktionary_senseid"] for row in rows
            ),
            "types_with_complete_lexicalized_senseids": sum(
                row["all_lexicalized_senses_have_wiktionary_senseid"] for row in rows
            ),
            "senses_with_wikidata_id": sum(row["senses_with_wikidata_id"] for row in rows),
            "senses_with_raw_id_field": sum(row["senses_with_raw_id_field"] for row in rows),
        },
        "response_identity": {
            "combined_manifest_sha256": digest("\n".join(manifest).encode("utf-8")),
            "http_status_counts": dict(sorted(Counter(
                str(records[lemma]["status"]) for lemma in targets
            ).items())),
            "responses_with_last_modified": len(modified),
            "unique_last_modified_values": len(set(modified)),
            "responses_with_etag": sum(bool(records[lemma].get("etag")) for lemma in targets),
            "raw_lexical_content_committed": False,
        },
        "construct_limits": [
            "Exact canonical-form lookup measures dictionary-entry alignment, not occurrence identification or contextual sense truth.",
            "A Wiktionary gloss is lexicographic evidence, not an independently annotated STREUSLE occurrence label.",
            "UOFI literal fallbacks are reported separately from lexicalized candidate senses.",
            "The raw per-word endpoint omits Kaikki-generated display IDs; optional Wiktionary senseid and Wikidata fields are measured separately.",
        ],
    }


def build_audit(checkout, oewn, profile, cache, fetch=False, ca_file=None):
    _, datasets = inspect_checkout(checkout, profile)
    targets, routes = derive_population(datasets, load_verb_entries(oewn))
    records = {}
    for index, lemma in enumerate(targets, 1):
        if fetch:
            print(f"Kaikki VID audit: {index}/{len(targets)}", file=sys.stderr)
        records[lemma] = load_record(cache, lemma, fetch, ca_file)
    summary = summarize(targets, records, routes)
    return {
        "audit_version": "1.0.0",
        "audit_id": "streusle-v5-oewn-unmatched-vid-kaikki-enwiktionary-2026-08-05",
        "purpose": "Test whether exact English Wiktionary entries repair the measured OEWN VID inventory gap and whether their raw sense identifiers are adequate for a fixed public benchmark.",
        "source_identity": {
            "streusle_tag": profile["source"]["tag"],
            "streusle_commit": profile["source"]["commit"],
            "streusle_profile": "benchmarks/streusle_v5_vpc_vid.json",
            "streusle_artifacts": profile["artifacts"],
            "oewn_release": "2025-edition",
            "oewn_sha256": ARTIFACT_SHA256,
            "kaikki_endpoint": BASE_URL,
            "enwiktionary_dump_date_reported_by_kaikki": "2026-08-05",
            "kaikki_extraction_date": "2026-08-28",
            "wiktextract_commits_reported_by_kaikki": ["872fc7b", "4deed51"],
            "retrieval_warning": "Per-word URLs are not date-versioned; local response hashes identify this audit, but a fixed benchmark must use a dated dump and pinned extractor or lawfully archive the exact derived layer.",
        },
        "rights_and_release": {
            "state": "audit_only_not_admitted",
            "terms": "Wiktionary text reuse remains subject to applicable CC BY-SA 4.0/GFDL attribution and derivative obligations, including any imported-content conditions; the MIT Wiktextract software license does not relicense extracted data.",
            "public_output": "Aggregate counts and a combined response-manifest hash only; no gloss, example, entry row, or target list is committed.",
            "evidence_urls": [
                "https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use",
                "https://kaikki.org/dictionary/rawdata.html",
                "https://github.com/tatuylonen/wiktextract"
            ],
        },
        "summary": summary,
        "decision_rule": "Do not admit Wiktionary as benchmark gold solely from coverage. Require a fixed lawful artifact, reproducible entry-to-canonical mapping, adequate sense identifiers or a separately versioned project ID layer, and independent contextual annotation.",
    }


def self_check():
    datasets = {
        "train": [{"smwes": {
            "1": {"lexcat": "V.VID", "lexlemma": "covered form"},
            "2": {"lexcat": "V.VID", "lexlemma": "waste time"},
            "3": {"lexcat": "V.VID", "lexlemma": "wiki form"},
            "4": {"lexcat": "V.VID", "lexlemma": "missing form"},
        }}],
        "dev": [],
        "test": [{"smwes": {
            "1": {"lexcat": "V.VID", "lexlemma": "wiki form"},
        }}],
    }
    verbs = {"covered form": 2, "waste one's time": 1}
    targets, routes = derive_population(datasets, verbs)
    assert targets == {"missing form": 1, "wiki form": 2}
    found = json.dumps({
        "word": "wiki form", "lang_code": "en", "pos": "verb", "senses": [
            {"glosses": ["A lexical sense."], "senseid": ["sense-1"]},
            {"glosses": ["Used other than figuratively or idiomatically: see wiki, form."]},
        ],
    })
    records = {
        "missing form": {"status": 404, "body": "", "body_sha256": digest(b""),
                         "last_modified": None, "etag": None},
        "wiki form": {"status": 200, "body": found, "body_sha256": digest(found.encode()),
                      "last_modified": "date", "etag": "tag"},
    }
    report = summarize(targets, records, routes)
    assert report["target_population"] == {
        "types": 2,
        "occurrences": 3,
        "definition": "STREUSLE V.VID canonical types with neither an exact OEWN verb entry nor a unique fixed article/possessive-slot OEWN candidate",
    }
    assert report["exact_kaikki_coverage"]["types_with_lexicalized_candidate"] == 1
    assert report["sense_schema"]["uofi_literal_fallback_senses"] == 1
    assert report["sense_schema"]["senseid_coverage"] == 0.5
    assert report["combined_lookup_routes"]["types_with_any_unreviewed_dictionary_route"] == 3
    return {"self_check": "pass"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, nargs="?")
    parser.add_argument("oewn", type=Path, nargs="?")
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--ca-file", type=Path)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_check:
            result = self_check()
        else:
            if args.checkout is None or args.oewn is None:
                raise ValueError("A STREUSLE checkout and OEWN zip are required.")
            profile = json.loads(args.profile.read_text(encoding="utf-8"))
            result = build_audit(args.checkout, args.oewn, profile, args.cache,
                                 args.fetch, args.ca_file)
            if args.check and result != json.loads(args.check.read_text(encoding="utf-8")):
                raise ValueError(f"Audit differs from {args.check}.")
    except (AssertionError, HTTPError, OSError, URLError, json.JSONDecodeError,
            KeyError, TypeError, UnicodeDecodeError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
