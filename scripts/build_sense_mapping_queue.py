#!/usr/bin/env python3
"""Build the bounded IR-130 non-exact VID mapping review queue."""

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlparse
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "resources/hybrid_sense_inventory_contract_2026_09_03.json"
AUDIT = ROOT / "resources/streusle_v5_kaikki_vid_audit_2026_09_03.json"
DEFAULT_CACHE = ROOT / "research_data/kaikki_en_2026_08_05_vid_exact"
OEWN_SHA256 = "7d749f6e2c39e6970e4997839dcf6e42fd281f3c2fae0171d2192bae8cfa4b51"
KAIKKI_SHA256 = "506ae4786da452d066d58b580e0417aa4eb60c8b181d1a2d2cea82cf68508462"
CACHE_MANIFEST_SHA256 = "a1499e616b7ebc75de8b52e3e4d7e01c764108bc0d739946f740a0a0379479c6"
DASHES = str.maketrans({character: "-" for character in "‐‑‒–—―−"})
APOSTROPHES = str.maketrans({character: "'" for character in "’‘ʼ＇`"})


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    hasher = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def compact(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def normalize_orthography(value):
    value = unicodedata.normalize("NFKC", value).translate(DASHES).translate(APOSTROPHES)
    return " ".join(re.sub(r"\s*-\s*", " ", value.casefold()).split())


def read_cache_population(cache):
    records = {}
    for path in sorted(cache.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        url = record.get("url", "")
        name = unquote(urlparse(url).path.rsplit("/", 1)[-1])
        if not name.endswith(".jsonl"):
            raise ValueError(f"Invalid cache URL in {path}.")
        lemma = name[:-6].casefold()
        body = record.get("body")
        if (path.stem != digest(lemma.encode("utf-8")) or
                record.get("status") not in (200, 404) or
                not isinstance(body, str) or
                digest(body.encode("utf-8")) != record.get("body_sha256")):
            raise ValueError(f"Invalid cached record for {lemma!r}.")
        if lemma in records:
            raise ValueError(f"Duplicate cached lemma {lemma!r}.")
        records[lemma] = record

    manifest = []
    residual = []
    exact = 0
    for lemma, record in sorted(records.items()):
        rows = [json.loads(line) for line in record["body"].splitlines() if line.strip()]
        matched = any(
            row.get("word", "").casefold() == lemma and
            row.get("lang_code") == "en" and row.get("pos") == "verb"
            for row in rows
        )
        exact += matched
        if not matched:
            residual.append(lemma)
        manifest.append("\0".join((
            lemma, str(record["status"]), record["body_sha256"],
            record.get("last_modified") or "", record.get("etag") or "",
        )))

    identity = digest("\n".join(manifest).encode("utf-8"))
    if (len(records), exact, len(residual), identity) != (
            206, 60, 146, CACHE_MANIFEST_SHA256):
        raise ValueError("Kaikki exact-audit cache does not match the frozen population.")
    return residual


def target_index(targets):
    exact = {}
    normalized = {}
    for target in targets:
        exact.setdefault(target.casefold(), []).append(target)
        normalized.setdefault(normalize_orthography(target), []).append(target)
    return exact, normalized


def target_matches(index, declared_value):
    if not isinstance(declared_value, str):
        return []
    folded = declared_value.casefold()
    exact, normalized = index
    if folded in exact:
        return [(target, 4) for target in exact[folded]]
    return [(target, 5) for target in normalized.get(normalize_orthography(declared_value), [])]


def add_candidate(store, target, stage, source, version, artifact_sha256,
                  entry_id, entry_lemma, record, field, declared_value,
                  linked_sense_id=None):
    record_sha256 = digest(compact(record))
    key = (source, entry_id, record_sha256)
    candidates = store.setdefault(target, {})
    candidate = candidates.setdefault(key, {
        "source_inventory_id": source,
        "source_version": version,
        "source_artifact_sha256": artifact_sha256,
        "source_entry_id": entry_id,
        "source_entry_lemma": entry_lemma,
        "source_record_sha256": record_sha256,
        "stage": stage,
        "mapping_route": (
            "source_declared_variant_index" if stage == 4
            else "orthographic_equivalence"
        ),
        "mapping_relation": "candidate_only",
        "verification_status": "unreviewed",
        "evidence": [],
    })
    if stage < candidate["stage"]:
        candidate["stage"] = stage
        candidate["mapping_route"] = "source_declared_variant_index"
    evidence = {"field": field, "declared_value": declared_value}
    if linked_sense_id:
        evidence["linked_sense_id"] = linked_sense_id
    if evidence not in candidate["evidence"]:
        candidate["evidence"].append(evidence)


def collect_kaikki_candidates(index, rows, store):
    for row in rows:
        if row.get("lang_code") != "en" or row.get("pos") != "verb":
            continue
        word = row.get("word")
        if not isinstance(word, str):
            continue
        for target, stage in target_matches(index, word):
            if stage == 5:
                add_candidate(store, target, stage, "enwiktionary-kaikki",
                              "dump-2026-08-05_extract-2026-08-28", KAIKKI_SHA256,
                              f"{word}#verb", word, row, "entry_lemma", word)
        declared = []
        for form in row.get("forms", []):
            if isinstance(form, dict):
                declared.append(("forms.form", form.get("form"), None))
        for sense in row.get("senses", []):
            if not isinstance(sense, dict):
                continue
            sense_ids = sense.get("senseid") or []
            if isinstance(sense_ids, str):
                sense_ids = [sense_ids]
            linked_sense_id = ",".join(sorted(sense_ids)) or None
            for field in ("alt_of", "form_of"):
                for link in sense.get(field, []) or []:
                    if isinstance(link, dict):
                        declared.append((f"senses.{field}.word", link.get("word"),
                                         linked_sense_id))
        for field, value, linked_sense_id in declared:
            for target, stage in target_matches(index, value):
                add_candidate(store, target, stage, "enwiktionary-kaikki",
                              "dump-2026-08-05_extract-2026-08-28", KAIKKI_SHA256,
                              f"{word}#verb", word, row, field, value,
                              linked_sense_id)


def collect_oewn_candidates(index, entries, store):
    for lemma, entry in entries:
        for target, stage in target_matches(index, lemma):
            if stage == 5:
                add_candidate(store, target, stage, "oewn", "2025-edition",
                              OEWN_SHA256, f"{lemma}#v", lemma, entry,
                              "entry_lemma", lemma)
        for value in entry.get("form", []):
            for target, stage in target_matches(index, value):
                add_candidate(store, target, stage, "oewn", "2025-edition",
                              OEWN_SHA256, f"{lemma}#v", lemma, entry,
                              "form", value)
        for sense in entry.get("sense", []):
            for linked_id in sense.get("also", []):
                value = linked_id.split("%", 1)[0].replace("_", " ")
                for target, stage in target_matches(index, value):
                    add_candidate(store, target, stage, "oewn", "2025-edition",
                                  OEWN_SHA256, f"{lemma}#v", lemma, entry,
                                  "sense.also", value, linked_id)


def kaikki_rows(path):
    with path.open(encoding="utf-8") as source:
        for line in source:
            if line.strip():
                yield json.loads(line)


def oewn_entries(path):
    with ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            if not name.startswith("entries-"):
                continue
            for lemma, parts in sorted(json.loads(archive.read(name)).items()):
                if "v" in parts:
                    yield lemma, parts["v"]


def build(oewn, kaikki, cache):
    if file_digest(oewn) != OEWN_SHA256:
        raise ValueError("OEWN artifact SHA-256 does not match the frozen release.")
    if file_digest(kaikki) != KAIKKI_SHA256 or kaikki.stat().st_size != 424557919:
        raise ValueError("Kaikki verb artifact does not match the reviewed snapshot.")
    targets = read_cache_population(cache)
    index = target_index(targets)
    found = {}
    collect_oewn_candidates(index, oewn_entries(oewn), found)
    collect_kaikki_candidates(index, kaikki_rows(kaikki), found)

    items = []
    for number, target in enumerate(sorted(targets), 1):
        candidates = list(found.get(target, {}).values())
        for candidate in candidates:
            candidate["evidence"].sort(key=lambda item: tuple(item.values()))
        candidates.sort(key=lambda item: (
            item["stage"], item["source_inventory_id"], item["source_entry_id"],
            item["source_record_sha256"],
        ))
        state = "candidate_set" if candidates else "unresolved"
        items.append({
            "type_id": f"ldfreq-en-vmwe-t{number:06d}",
            "input_canonical_lemma": target,
            "observed_vmwe_categories": ["V.VID"],
            "mapping_state": state,
            "stage_reached": max((candidate["stage"] for candidate in candidates),
                                 default=5),
            "candidates": candidates,
            "review_state": "pending_independent_review" if candidates else "not_applicable",
            "adjudication_state": "not_started",
            "stop_reason": (
                "bounded_candidate_set_complete_review_pending" if candidates
                else "bounded_sources_exhausted_no_candidate"
            ),
            "rights_state": (
                "withheld_pending_enwiktionary_dump_hash_and_imported_content_review"
                if any(c["source_inventory_id"] == "enwiktionary-kaikki"
                       for c in candidates)
                else "no_source_candidate_content"
            ),
        })

    counts = Counter(item["mapping_state"] for item in items)
    candidate_sources = Counter(
        candidate["source_inventory_id"]
        for item in items for candidate in item["candidates"]
    )
    return {
        "queue_schema_version": "1.0.0",
        "queue_id": "streusle-v5-vid-nonexact-mapping-2026-09-04",
        "generated_on": "2026-09-04",
        "status": "machine_candidates_complete_human_review_and_source_admission_pending",
        "task": "IR-130",
        "dependencies": {
            "contract": {"path": str(CONTRACT.relative_to(ROOT)),
                         "sha256": file_digest(CONTRACT), "version": "1.0.0"},
            "exact_audit": {"path": str(AUDIT.relative_to(ROOT)),
                            "sha256": file_digest(AUDIT)},
            "generator": {"path": "scripts/build_sense_mapping_queue.py",
                          "sha256": file_digest(Path(__file__))},
        },
        "source_snapshots": {
            "oewn": {
                "version": "2025-edition", "artifact_size_bytes": oewn.stat().st_size,
                "artifact_sha256": OEWN_SHA256,
                "url": "https://github.com/globalwordnet/english-wordnet/releases/download/2025-edition/english-wordnet-2025-json.zip",
                "public_notice": "resources/OEWN_WORDNET_NOTICE.txt",
            },
            "enwiktionary_kaikki": {
                "reported_dump_date": "2026-08-05",
                "extraction_date": "2026-08-28",
                "artifact_last_modified": "Fri, 28 Aug 2026 15:00:38 GMT",
                "artifact_size_bytes": kaikki.stat().st_size,
                "artifact_sha256": KAIKKI_SHA256,
                "url": "https://kaikki.org/dictionary/English/pos-verb/kaikki.org-dictionary-English-by-pos-verb.jsonl",
                "public_notice": "resources/WIKTIONARY_KAIKKI_NOTICE.md",
                "admission_gap": "underlying_enwiktionary_dump_sha256_and_imported_content_review_missing",
            },
            "streusle": {
                "version": "5.0",
                "commit": "8ba61fe4f216e7967500a862554a4fff79d25f5d",
                "cache_manifest_sha256": CACHE_MANIFEST_SHA256,
                "public_notice": "resources/STREUSLE_NOTICE.md",
            },
        },
        "procedure": {
            "ordered_stages": [
                "1 exact OEWN verb entry (completed prefilter)",
                "2 fixed closed-class slot skeleton (completed prefilter)",
                "3 exact English Wiktionary verb entry (completed prefilter)",
                "4 source-declared forms and alt_of/form_of/OEWN also fields",
                "5 NFKC, casefold, whitespace, hyphen, and apostrophe equivalence",
                "6 independent review of the closed candidate set (pending)",
            ],
            "stage_5_normalization": "NFKC; Unicode casefold; listed dash variants become hyphen; spaces around hyphens and hyphens become one space; listed apostrophe variants become ASCII apostrophe; whitespace collapses",
            "candidate_generation_uses_glosses_or_examples": False,
            "free_search_allowed": False,
            "open_class_deletion_substitution_or_reordering_allowed": False,
        },
        "summary": {
            "fixed_residual_types": 146,
            "fixed_residual_occurrences": 169,
            "queue_items": len(items),
            "state_counts": dict(sorted(counts.items())),
            "candidate_records_by_source": dict(sorted(candidate_sources.items())),
            "types_with_cross_resource_support": sum(
                len({candidate["source_inventory_id"] for candidate in item["candidates"]}) > 1
                for item in items
            ),
            "exact_misses_retained_in_denominator": len(items) == 146,
            "mapped": 0,
            "ooi_pending": 0,
            "warning": "unresolved means no route in the bounded sources; it is not proof of a true lexical or semantic inventory gap",
        },
        "release_boundary": {
            "queue_license": "CC-BY-SA-4.0 AND LicenseRef-WordNet",
            "raw_oewn_or_kaikki_artifacts_bundled": False,
            "glosses_examples_translations_or_source_text_bundled": False,
            "runtime_integration": "none",
            "human_annotation_authorized": False,
        },
        "items": items,
    }


def self_check():
    assert normalize_orthography("Jump ‑ Start") == "jump start"
    assert normalize_orthography("one’s  way") == "one's way"
    store = {}
    collect_kaikki_candidates(target_index({"think so", "jump - start"}), [{
        "word": "think", "lang_code": "en", "pos": "verb", "forms": [],
        "senses": [{"alt_of": [{"word": "think so"}], "tags": ["alt-of"]}],
    }, {
        "word": "jump-start", "lang_code": "en", "pos": "verb",
        "forms": [{"form": "jump start", "tags": ["alternative"]}], "senses": [],
    }], store)
    assert set(store) == {"think so", "jump - start"}
    assert min(value["stage"] for value in store["think so"].values()) == 4
    assert min(value["stage"] for value in store["jump - start"].values()) == 5


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("oewn", type=Path, nargs="?")
    parser.add_argument("kaikki", type=Path, nargs="?")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("Sense mapping queue self-check: PASS")
        return
    if args.oewn is None or args.kaikki is None:
        parser.error("oewn and kaikki artifacts are required unless --self-check is used")
    result = json.dumps(build(args.oewn, args.kaikki, args.cache),
                        ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if args.check.read_text(encoding="utf-8") != result:
            raise SystemExit(f"Sense mapping queue differs from {args.check}.")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
