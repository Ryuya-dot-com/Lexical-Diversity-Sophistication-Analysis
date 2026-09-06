#!/usr/bin/env python3
"""Verify Project Gutenberg file identities and pre-body notices."""

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRIAGE = ROOT / "resources/gutenberg_2026_08_30_rights_triage_batch1.json"
FRAME = ROOT / "resources/gutenberg_2026_08_30_prose_frame.json"
OUTPUT = ROOT / "resources/gutenberg_2026_08_30_notice_audit_batch1.json"
MIRROR = "https://gutenberg.pglaf.org/cache/epub"
FIELDS = re.compile(
    r"^\s*(Title|Author|Creator|Illustrator|Release date|"
    r"Most recently updated|Language|Original publication|Credits):\s*(.*)$"
)
START = b"*** START OF THE PROJECT GUTENBERG EBOOK"
END = b"*** END OF THE PROJECT GUTENBERG EBOOK"


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def parse_fields(preamble):
    values = {}
    current = None
    for line in preamble.decode("utf-8-sig").splitlines():
        match = FIELDS.match(line)
        if match:
            current = match.group(1).casefold().replace(" ", "_")
            values[current] = match.group(2).strip()
        elif current and line[:1].isspace() and line.strip():
            values[current] += " " + line.strip()
        else:
            current = None
    return values


def inspect_file(path, text_id):
    data = path.read_bytes()
    start = data.find(START)
    if start < 0 or data.find(END, start) < 0:
        raise ValueError(f"Missing Project Gutenberg boundary marker: {path}")
    preamble = data[:start]
    fields = parse_fields(preamble)
    match = re.search(rf"\[eBook #{text_id}\]", fields.get("release_date", ""), re.I)
    if not match:
        raise ValueError(f"Header ebook number does not match {text_id}: {path}")
    notice = preamble.decode("utf-8-sig")
    if ("United States" not in notice or
            "check the laws of the country where you are located" not in notice):
        raise ValueError(f"Missing US/non-US restriction notice: {path}")
    creator = fields.get("author") or fields.get("creator")
    if not fields.get("title") or not creator or fields.get("language") != "English":
        raise ValueError(f"Incomplete title/creator/language header: {path}")
    return {
        "text_id": text_id,
        "source_url": f"{MIRROR}/{text_id}/pg{text_id}.txt",
        "local_path_unbundled": str(path.relative_to(ROOT)),
        "size_bytes": path.stat().st_size,
        "sha256": hashlib.sha256(data).hexdigest(),
        "file_mtime_utc_from_curl_remote_time": datetime.fromtimestamp(
            path.stat().st_mtime, timezone.utc
        ).isoformat(),
        "preamble_sha256": hashlib.sha256(preamble).hexdigest(),
        "header": {
            "title": fields["title"],
            "primary_creator": creator,
            "illustrator": fields.get("illustrator"),
            "release_date": fields["release_date"],
            "most_recently_updated": fields.get("most_recently_updated"),
            "language": fields["language"],
            "original_publication": fields.get("original_publication"),
            "credits": fields.get("credits"),
        },
        "checks": {
            "start_and_end_markers_present": True,
            "us_notice_and_non_us_warning_present": True,
            "full_project_gutenberg_license_footer_present":
                b"START: FULL LICENSE" in data[data.find(END):],
            "original_publication_in_preamble": bool(fields.get("original_publication")),
            "credits_in_preamble": bool(fields.get("credits")),
        },
    }


def build(directory, retrieved_on, triage_path=TRIAGE,
          audit_id="gutenberg-2026-08-30-notice-audit-batch1"):
    directory = directory.resolve()
    triage_path = triage_path.resolve()
    triage = json.loads(triage_path.read_text(encoding="utf-8"))
    frame = json.loads(FRAME.read_text(encoding="utf-8"))
    columns = triage["screen_columns"]
    allowed = [dict(zip(columns, row)) for row in triage["screens"]
               if row[3] == "notice_check_allowed"]
    expected = {f"pg{row['text_id']}.txt" for row in allowed}
    present = {path.name for path in directory.glob("pg*.txt")}
    if present != expected:
        raise ValueError(
            f"Local file set differs: missing={sorted(expected - present)}, "
            f"unexpected={sorted(present - expected)}"
        )
    frame_columns = frame["queue_columns"]
    queue = {(row[0], row[1]): dict(zip(frame_columns, row)) for row in frame["queue"]}
    files = []
    for row in allowed:
        record = inspect_file(directory / f"pg{row['text_id']}.txt", row["text_id"])
        source = queue[row["stratum"], row["queue_rank"]]
        if source["text_id"] != row["text_id"]:
            raise ValueError("Rights triage no longer matches the frozen queue.")
        record.update({"stratum": row["stratum"], "queue_rank": row["queue_rank"]})
        files.append(record)
    original_count = sum(row["checks"]["original_publication_in_preamble"] for row in files)
    credit_count = sum(row["checks"]["credits_in_preamble"] for row in files)
    license_count = sum(
        row["checks"]["full_project_gutenberg_license_footer_present"] for row in files
    )
    return {
        "audit_schema_version": 1,
        "audit_id": audit_id,
        "retrieved_on": retrieved_on,
        "status": "preambles_verified_front_matter_and_units_pending",
        "inputs": {
            "rights_triage_sha256": digest(triage_path),
            "frame_sha256": digest(FRAME),
            "official_mirror_listing": "https://www.gutenberg.org/dirs/MIRRORS.ALL",
            "mirror_base": MIRROR,
            "source_files_bundled": False,
        },
        "scope": {
            "parsed_content": "Only bytes before each Project Gutenberg START marker were decoded and parsed; the complete file was read mechanically only for SHA-256 and boundary/license-marker checks.",
            "body_prose_reviewed": False,
            "front_matter_after_start_reviewed": False,
            "units_selected": 0,
            "mwe_searches_run": 0,
            "public_web_distribution_authorized": False,
        },
        "files": files,
        "summary": {
            "files": len(files),
            "preambles_verified": len(files),
            "license_footers_present": license_count,
            "original_publication_present": original_count,
            "original_publication_missing": len(files) - original_count,
            "credits_present": credit_count,
            "credits_missing": len(files) - credit_count,
            "admitted_units": 0,
        },
        "next_action": (
            "For the ten files lacking Original publication and the one lacking Credits, inspect only title-page, copyright-page, and transcriber-note front matter after the START marker. Resolve retained textual contributors and edition identity before fixing any first intact prose unit; keep every source file local and unbundled."
            if audit_id == "gutenberg-2026-08-30-notice-audit-batch1" else
            "For files lacking Original publication or Credits, inspect only title-page, copyright-page, and transcriber-note front matter after the START marker. Resolve retained textual contributors and edition identity before fixing any first intact prose unit; keep every source file local and unbundled."
        ),
    }


def self_check():
    preamble = b"""The Project Gutenberg eBook\nUnited States\ncheck the laws of the country where you are located\nTitle: Test\nAuthor: A. Writer\nRelease date: Test [eBook #7]\nLanguage: English\nCredits: First line\n  second line\n\n"""
    fields = parse_fields(preamble)
    assert fields["credits"] == "First line second line"
    assert fields["author"] == "A. Writer"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?")
    parser.add_argument("--retrieved-on", default="2026-09-03")
    parser.add_argument("--triage", type=Path, default=TRIAGE)
    parser.add_argument("--audit-id", default="gutenberg-2026-08-30-notice-audit-batch1")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("Project Gutenberg notice-audit self-check: PASS")
        return
    if args.directory is None:
        parser.error("directory is required")
    rendered = json.dumps(build(args.directory, args.retrieved_on, args.triage, args.audit_id), ensure_ascii=False,
                          separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Generated audit differs from {args.output}")
        print(f"Project Gutenberg notice-audit verification: PASS ({args.output})")
    else:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
