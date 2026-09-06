#!/usr/bin/env python3
"""Freeze a target-blind Project Gutenberg prose-fiction metadata queue."""

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "resources/gutenberg_2026_08_30_prose_frame.json"
FRAME_ID = "gutenberg-2026-08-30-target-blind-english-prose-v1"
CATALOG_BYTES = 21_196_613
CATALOG_SHA256 = "253f1b2d9aead75fec8ddb732c72a2fab5cd7db2f37745ef20760254f0666c4b"
CATALOG_RECORDS = 79_288
FIELDS = [
    "Text#", "Type", "Issued", "Title", "Language", "Authors", "Subjects",
    "LoCC", "Bookshelves",
]
FICTION = re.compile(r"\bfiction\b")
NONPROSE = re.compile(r"\b(?:poetry|dramas?|plays|librettos?)\b")
JUVENILE = (
    "juvenile fiction", "children's fiction", "children’s fiction",
    "children's literature", "children’s literature", "children & young adult",
    "children's book series", "category: children", "children's stories",
    "children’s stories", "young adult",
)
QUEUE_LIMIT = 40


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def stratum(row):
    metadata = f'{row["Subjects"]}; {row["Bookshelves"]}'.casefold()
    if (row["Type"] != "Text" or row["Language"] != "en" or
            not FICTION.search(metadata) or NONPROSE.search(metadata) or
            "[translator]" in row["Authors"].casefold()):
        return None
    return "juvenile" if any(term in metadata for term in JUVENILE) else "adult_or_unspecified"


def selection_hash(name, text_id):
    return digest(f"{FRAME_ID}\n{name}\n{text_id}".encode())


def row_digest(row):
    return digest(json.dumps(row, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode())


def build(catalog_path):
    if catalog_path.stat().st_size != CATALOG_BYTES:
        raise ValueError("Project Gutenberg catalog size does not match the frozen input.")
    if file_digest(catalog_path) != CATALOG_SHA256:
        raise ValueError("Project Gutenberg catalog SHA-256 does not match the frozen input.")
    with catalog_path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != FIELDS:
            raise ValueError("Project Gutenberg catalog columns differ from the frozen schema.")
        rows = list(reader)
    if len(rows) != CATALOG_RECORDS:
        raise ValueError("Project Gutenberg catalog record count differs from the frozen input.")

    pools = {"adult_or_unspecified": [], "juvenile": []}
    for row in rows:
        name = stratum(row)
        if name:
            pools[name].append((selection_hash(name, row["Text#"]), row))

    queue = []
    for name, candidates in pools.items():
        candidates.sort(key=lambda item: (item[0], int(item[1]["Text#"])))
        for rank, (order, row) in enumerate(candidates[:QUEUE_LIMIT], 1):
            queue.append([
                name, rank, int(row["Text#"]), row["Issued"], row["Title"],
                row["Authors"], order, row_digest(row),
                "queued_for_rights_and_unit_screen",
            ])

    return {
        "frame_schema_version": "0.1.0",
        "frame_id": FRAME_ID,
        "generated_on": "2026-09-02",
        "status": "frozen_before_ebook_acquisition_or_mwe_inspection",
        "source_catalog": {
            "official_page": "https://www.gutenberg.org/ebooks/offline_catalogs.html",
            "snapshot": "2026-08-30",
            "filename": "pg_catalog.csv",
            "size_bytes": CATALOG_BYTES,
            "sha256": CATALOG_SHA256,
            "record_count": CATALOG_RECORDS,
            "columns": FIELDS,
            "metadata_rights": "Project Gutenberg robot guidance states that catalog data are granted to the public domain.",
            "catalog_bundled": False,
        },
        "construct": {
            "role": "open natural-text app and annotation stress frame, separate from participant-linked TECO evidence and from every lexical reference profile",
            "population": "Project Gutenberg English prose-fiction metadata in this snapshot after the declared filters; not contemporary English, L2 text, or a universal reference corpus",
            "strata": ["adult_or_unspecified", "juvenile"],
            "selection_inputs": "catalog Type, Language, Subjects, Bookshelves, Authors-role markers, and Text# only; no ebook text, lexical profile, MWE inventory, or participant outcome",
            "metadata_eligibility": [
                "Type equals Text",
                "Language equals en exactly",
                "Subjects or Bookshelves contains the whole word fiction",
                "Subjects and Bookshelves contain none of the whole-word labels poetry, drama(s), plays, or libretto(s)",
                "Authors contains no explicit [Translator] credit",
            ],
            "translation_limit": "Absence of a catalog translator credit does not prove original-language authorship; verify every retained work.",
            "stratum_rule": "juvenile requires an explicit juvenile-fiction, children's-fiction/literature/stories, children's-category/book-series, or young-adult marker; references to children as fictional subjects do not qualify",
            "content_neutrality": "After the declared genre and audience classification, title words, topical or sensitive subject matter, and MWE presence never exclude or reorder a candidate; titles are retained only for provenance and rights review.",
            "design_history": "Metadata queue previews informed the explicit translation-rights and juvenile-label boundaries; the final filters, seed, queue limits, and stop rules were frozen before ebook acquisition or MWE search.",
        },
        "sampling": {
            "order": "sort within stratum by SHA-256(frame_id + LF + stratum + LF + Text#), then numeric Text#",
            "queue_limit_per_stratum": QUEUE_LIMIT,
            "admission_stop_per_stratum": 10,
            "author_cap": "one admitted unit per normalized first semicolon-delimited Authors entry; an empty entry remains distinct by Text#",
            "replacement_rule": "continue in frozen rank order after a documented exclusion; stop without extending the queue if ten units are not admitted",
            "mwe_blinding": "Do not search, count, or inspect MWE forms until all admitted units and exact text hashes are frozen.",
        },
        "rights_and_acquisition": {
            "sequence": [
                "use catalog metadata and external bibliographic sources to provisionally clear every credited contributor for local access under Japanese term, transition, foreign-work, translation, and wartime-addition rules",
                "only then acquire plain UTF-8 text through an official mirror or documented robot route",
                "before substantive text inspection, verify the ebook-internal US restriction notice, license boundary, and contributor credits",
                "declare the Japanese, US, and any additional public release jurisdiction decision",
                "retain source URL, retrieval time, byte size, SHA-256, internal license boundary, and release decision",
            ],
            "official_terms": "https://www.gutenberg.org/policy/terms_of_use.html",
            "official_license": "https://www.gutenberg.org/policy/license",
            "official_robot_guidance": "https://www.gutenberg.org/policy/robot_access.html",
            "japan_term_guidance": "https://www.bunka.go.jp/seisaku/chosakuken/hokaisei/kantaiheiyo_chosakuken/1411890.html",
            "automatic_public_domain_inference": False,
        },
        "unit_gate": {
            "body": "remove the Project Gutenberg header/license/footer and front/back matter without altering retained prose",
            "unit": "first unambiguous complete chapter, short story, or standalone body containing 300-2000 project-tokenizer words",
            "never": [
                "truncate an overlong unit",
                "combine nonadjacent sections",
                "select a later unit for lexical coverage or MWE yield",
                "treat OCR repair as the source text without a separate modification record",
            ],
            "mechanical_exclusions": [
                "no stable UTF-8 plain-text artifact",
                "no unambiguous complete prose unit in range",
                "predominantly verse, drama, table, list, or image-dependent content",
                "duplicate admitted primary author",
                "rights unresolved for local access or planned release",
            ],
        },
        "summary": {
            "eligible_metadata_records": sum(map(len, pools.values())),
            "eligible_adult_or_unspecified_records": len(pools["adult_or_unspecified"]),
            "eligible_juvenile_records": len(pools["juvenile"]),
            "queued_records": len(queue),
            "queued_per_stratum": QUEUE_LIMIT,
            "ebook_files_read": 0,
            "mwe_searches_run": 0,
        },
        "queue_columns": [
            "stratum", "queue_rank", "text_id", "issued", "title", "authors",
            "selection_hash", "metadata_row_sha256", "state",
        ],
        "queue": queue,
        "excluded_inferences": [
            "reference-corpus frequency or range",
            "representativeness of contemporary English or L2 reading",
            "learner knowledge, comprehension, or eye-movement behavior",
            "95 or 98 percent comprehension threshold validation",
            "MWE prevalence before the blind unit freeze",
            "worldwide public-domain status from Project Gutenberg inclusion",
        ],
        "next_action": "Review rights and unit feasibility in frozen rank order without MWE inspection; commit only metadata, hashes, decisions, and text that passes the declared release gate.",
    }


def self_check():
    row = dict.fromkeys(FIELDS, "")
    row.update({"Text#": "7", "Type": "Text", "Language": "en",
                "Subjects": "Adventure stories -- Juvenile fiction"})
    assert stratum(row) == "juvenile"
    row["Subjects"] = "Baseball players -- Fiction"
    assert stratum(row) == "adult_or_unspecified"
    row["Subjects"] = "Literary nonfiction"
    assert stratum(row) is None
    row["Subjects"] = "English drama -- 19th century; Historical fiction"
    assert stratum(row) is None
    row["Subjects"] = "Adventure stories -- Juvenile fiction"
    row["Authors"] = "Example, A. [Translator]"
    assert stratum(row) is None
    assert selection_hash("juvenile", "7") == (
        "5d187a7eee9ff3d724ac82117add323412654e4531c736bb00d39fe7a88b1e9a"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path, nargs="?")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("Project Gutenberg frame self-check: PASS")
        return
    if args.catalog is None:
        parser.error("catalog is required")
    rendered = json.dumps(build(args.catalog), ensure_ascii=False,
                          separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Generated frame differs from {args.output}")
        print(f"Project Gutenberg frame verification: PASS ({args.output})")
    else:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
