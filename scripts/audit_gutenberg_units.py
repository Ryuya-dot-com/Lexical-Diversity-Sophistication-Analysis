#!/usr/bin/env python3
"""Verify the fixed first-unit boundaries and length gate for Gutenberg files."""

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONT_MATTER = ROOT / "resources/gutenberg_2026_08_30_front_matter_review_batch1.json"
OUTPUT = ROOT / "resources/gutenberg_2026_08_30_unit_gate_batch1.json"
TOKEN = re.compile(r"(?<!\w)[A-Za-z]+(?:['’][A-Za-z]+)*(?!\w)")
MIN_TOKENS = 300
MAX_TOKENS = 2000

# End line, exact opening heading, exact next sibling heading, unit type, structure.
BOUNDARIES = {
    27601: (505, "CHAPTER I.", "CHAPTER II.", "chapter", "complete_allowed_unit_type"),
    43731: (318, "CHAPTER I", "CHAPTER II", "chapter", "complete_allowed_unit_type"),
    25885: (302, "I", "II", "chapter", "complete_allowed_unit_type"),
    46966: (491, "*CHAPTER I.*", "*CHAPTER II.*", "chapter", "complete_allowed_unit_type"),
    76417: (412, "I", "II", "chapter", "complete_allowed_unit_type"),
    7667: (496, "CHAPTER I.", "CHAPTER II.", "chapter", "complete_allowed_unit_type"),
    72983: (356, "CHAPTER I.", "CHAPTER II.", "chapter", "complete_allowed_unit_type"),
    6973: (395, "CHAPTER I.", "CHAPTER II.", "chapter", "complete_allowed_unit_type"),
    46892: (612, "THE AWAKENING OF HICKEY", "THE GREAT PANCAKE RECORD", "short_story", "complete_allowed_unit_type"),
    73331: (295, "CHAPTER I.", "CHAPTER II.", "chapter", "complete_allowed_unit_type"),
    48608: (1645, "THE ORPHAN'S HOME.", '"THE BATTLE OF ROANOKE ISLAND."', "short_story", "complete_allowed_unit_type"),
    53088: (290, "INTRODUCTORY.", "CHAPTER I.", "introductory_section", "ambiguous_not_frozen_unit_type"),
    1573: (298, "CHAPTER I. THE WAR MEETING", "CHAPTER II. THE PRIZE", "chapter", "complete_allowed_unit_type"),
    14654: (568, "CHAPTER I", "CHAPTER II", "chapter", "complete_allowed_unit_type"),
    72192: (654, "On our abandoned Martian landing field there hangs a man's discarded", "*** END OF THE PROJECT GUTENBERG EBOOK HANG HEAD, VANDAL ***", "short_story", "complete_allowed_unit_type"),
    17793: (514, "Chapter I", "Chapter II", "chapter", "complete_allowed_unit_type"),
    36753: (466, "CHAPTER I.", "CHAPTER II.", "chapter", "complete_allowed_unit_type"),
    7517: (1125, "PART I", "PART II", "part", "ambiguous_not_frozen_unit_type"),
    68552: (1067, "I.", "[Transcriber’s Note: This story appeared in the December 29, 1917", "short_story", "complete_allowed_unit_type"),
    14832: (425, "CHAPTER I", "CHAPTER II", "chapter", "complete_allowed_unit_type"),
    33298: (281, "IF ENGLAND KNEW", "THE PERIL OF ENGLAND", "preface", "ambiguous_not_frozen_unit_type"),
    21729: (484, "CHAPTER ONE.", "CHAPTER TWO.", "chapter", "complete_allowed_unit_type"),
    55040: (141, "PREFACE.", "CONTENTS.", "preface", "ambiguous_not_frozen_unit_type"),
    70572: (392, "CHAPTER I", "CHAPTER II", "chapter", "complete_allowed_unit_type"),
    64033: (151, "INTRODUCTION", "Betty Wales, Junior", "introduction", "ambiguous_not_frozen_unit_type"),
    23072: (410, "CHAPTER ONE.", "CHAPTER TWO.", "chapter", "complete_allowed_unit_type"),
    14130: (340, "CHAPTER I", "CHAPTER II", "chapter", "complete_allowed_unit_type"),
    46205: (121, "_My Dear Nephews and Nieces_:--", "CONTENTS.", "reader_address", "ambiguous_not_frozen_unit_type"),
    47128: (142, "_To the Reader_", "CONTENTS", "reader_address", "ambiguous_not_frozen_unit_type"),
    13530: (346, "CHAPTER I", "CHAPTER II", "chapter", "complete_allowed_unit_type"),
    63142: (443, "CHAPTER I.", "CHAPTER II.", "chapter", "complete_allowed_unit_type"),
    26523: (92, "_Dear Jessica_:", "CONTENTS", "prefatory_letter", "ambiguous_not_frozen_unit_type"),
    29545: (199, "INTRODUCTION", "THE SPANISH JADE", "introduction", "ambiguous_not_frozen_unit_type"),
    27996: (230, "CHAPTER ONE.", "CHAPTER TWO.", "chapter", "complete_allowed_unit_type"),
    6488: (388, "CHAPTER I", "CHAPTER II", "chapter", "complete_allowed_unit_type"),
    40587: (448, "CHAPTER I", "CHAPTER II", "chapter", "complete_allowed_unit_type"),
    36396: (387, "CHAPTER I--WHAT IS COMING", "CHAPTER II--EAVESDROPPING", "chapter", "complete_allowed_unit_type"),
    72094: (225, "I.", "II.", "chapter", "complete_allowed_unit_type"),
    36833: (313, "CHAPTER I.—ONOWAY HOUSE.", "CHAPTER II.—NEIGHBORS.", "chapter", "complete_allowed_unit_type"),
    14890: (71, "FOREWORD", "CHARACTERS IN THE FRENCH AND INDIAN WAR SERIES", "foreword", "ambiguous_not_frozen_unit_type"),
    21326: (275, "CHAPTER ONE.", "CHAPTER TWO.", "chapter", "complete_allowed_unit_type"),
    25817: (379, "CHAPTER ONE.", "CHAPTER TWO.", "chapter", "complete_allowed_unit_type"),
    23683: (294, "CHAPTER I.", "CHAPTER II.", "chapter", "complete_allowed_unit_type"),
    44045: (387, "YOUNG OLIVER.", "TWO WAYS _OF ATTAINING WISDOM_.", "standalone_body", "complete_allowed_unit_type"),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def remove_illustration_blocks(data):
    kept = []
    inside = False
    removed = 0
    for line in data.splitlines(keepends=True):
        text = line.decode("utf-8").lstrip()
        if not inside and text.startswith("[Illustration"):
            inside = "]" not in text
            removed += 1
            continue
        if inside:
            inside = "]" not in text
            continue
        kept.append(line)
    if inside:
        raise ValueError("Unclosed illustration block in candidate unit")
    return b"".join(kept), removed


def build(directory, reviewed_on, front_matter_path=FRONT_MATTER,
          gate_id="gutenberg-2026-08-30-unit-gate-batch1"):
    front_matter_path = front_matter_path.resolve()
    review = json.loads(front_matter_path.read_text(encoding="utf-8"))
    columns = review["record_columns"]
    reviewed = [dict(zip(columns, row)) for row in review["records"]]
    sources = [row for row in reviewed
               if row["decision"] == "ready_for_version_conditioned_unit_gate"]
    missing = {row["text_id"] for row in sources} - set(BOUNDARIES)
    if missing:
        raise ValueError(f"Boundary table lacks ready files: {sorted(missing)}")

    records = []
    for source in sources:
        text_id = source["text_id"]
        end, opening, following, unit_type, structure = BOUNDARIES[text_id]
        path = directory / f"pg{text_id}.txt"
        data = path.read_bytes()
        if digest(data) != source["file_sha256"]:
            raise ValueError(f"Source hash differs for {text_id}")
        lines = data.splitlines(keepends=True)
        start = source["first_unit_heading_line"]
        if lines[start - 1].decode("utf-8").strip() != opening:
            raise ValueError(f"Opening heading differs for {text_id}")
        if lines[end].decode("utf-8").strip() != following:
            raise ValueError(f"Following heading differs for {text_id}")

        raw_unit = b"".join(lines[start - 1:end])
        retained, illustration_blocks = remove_illustration_blocks(raw_unit)
        token_count = len(TOKEN.findall(retained.decode("utf-8")))
        if structure != "complete_allowed_unit_type":
            length = "within_300_2000" if MIN_TOKENS <= token_count <= MAX_TOKENS else "outside_300_2000"
            decision = "excluded_ambiguous_first_unit_type"
            reasons = [
                "introductory_section_not_frozen_chapter_short_story_or_standalone_body"
                if gate_id == "gutenberg-2026-08-30-unit-gate-batch1" else
                "first_unit_type_not_frozen_chapter_short_story_or_standalone_body"
            ]
        elif token_count < MIN_TOKENS:
            length = "under_300"
            decision = "excluded_first_unit_under_minimum"
            reasons = ["first_unit_under_300_tokens"]
        elif token_count > MAX_TOKENS:
            length = "over_2000"
            decision = "excluded_first_unit_over_maximum"
            reasons = ["first_unit_over_2000_tokens"]
        else:
            length = "within_300_2000"
            decision = "passed_mechanical_unit_gate_release_pending"
            reasons = []
        records.append([
            source["stratum"], source["queue_rank"], text_id,
            source["file_sha256"], unit_type, [start, end], end + 1,
            digest(raw_unit), illustration_blocks, digest(retained), token_count,
            structure, length, decision, reasons,
        ])

    decisions = [row[13] for row in records]
    result = {
        "gate_schema_version": 1,
        "gate_id": gate_id,
        "reviewed_on": reviewed_on,
        "status": "mechanical_unit_gate_complete_release_review_pending",
        "inputs": {
            "front_matter_review_sha256": digest(front_matter_path.read_bytes()),
            "source_files_bundled": False,
            "unit_text_bundled": False,
        },
        "method": {
            "boundary": (
                "Inclusive one-based range from the fixed opening heading through the line before the next sibling heading; headings remain in the unit."
                if gate_id == "gutenberg-2026-08-30-unit-gate-batch1" else
                "Inclusive one-based range from the fixed opening boundary through the line before the following structural or end boundary; opening content remains in the unit."
            ),
            "retention": "Preserve exact source bytes and line endings, removing only complete bracketed Illustration blocks.",
            "tokenizer": "ASCII alphabetic word with internal straight or curly apostrophes; Unicode letters, numbers, and underscore block partial matches; hyphens split.",
            "length_gate_inclusive": [MIN_TOKENS, MAX_TOKENS],
            "later_unit_substitution": False,
            "release_rule": "A mechanical pass is not admission or worldwide serving permission.",
            "target_or_mwe_searches_run": 0,
        },
        "record_columns": [
            "stratum", "queue_rank", "text_id", "file_sha256", "unit_type",
            "raw_unit_lines_inclusive", "next_sibling_heading_line",
            "raw_unit_sha256", "removed_illustration_blocks",
            "retained_unit_sha256", "project_token_count",
            "structural_decision", "length_decision", "gate_decision", "reasons",
        ],
        "records": records,
        "structural_review_exposure": {
            "text_ids": [row[2] for row in records],
            "scope": (
                "Opening and following heading context was inspected for every candidate; the complete 53088 introductory section was read only to assess unit type and image dependence."
                if gate_id == "gutenberg-2026-08-30-unit-gate-batch1" else
                "Opening and following boundary context was inspected for every ready candidate; complete retained sections were processed mechanically only for structure, illustration removal, hashes, and token counts."
            ),
            "selection_effect": "None: fixed order, first-unit rule, allowed unit types, and length limits predated inspection.",
            "target_forms_senses_or_mwes_inspected": False,
        },
        "summary": {
            "records": len(records),
            "passed_mechanical_unit_gate_release_pending": decisions.count("passed_mechanical_unit_gate_release_pending"),
            "excluded_first_unit_over_maximum": decisions.count("excluded_first_unit_over_maximum"),
            "excluded_first_unit_under_minimum": decisions.count("excluded_first_unit_under_minimum"),
            "excluded_ambiguous_first_unit_type": decisions.count("excluded_ambiguous_first_unit_type"),
            "admitted_units": 0,
            "target_or_mwe_searches_run": 0,
        },
        "next_action": (
            "Continue rights triage in frozen rank order because each stratum has only one mechanical pass. Keep the two passing unit texts local and unbundled pending a separately declared release scope."
            if gate_id == "gutenberg-2026-08-30-unit-gate-batch1" else
            "Combine these results with batch 1 and continue the frozen queue only if either stratum still has fewer than ten mechanical passes. Keep every passing unit local and unbundled; do not inspect MWE yield or admit prose before the full unit set and release scope are frozen."
            if gate_id == "gutenberg-2026-08-30-unit-gate-batch2" else
            "Combine these results with batches 1 and 2 and screen exact ranks 31–40 because both strata remain below ten mechanical passes. Keep every passing unit local and unbundled; do not inspect MWE yield or admit prose before the full unit set and release scope are frozen."
        ),
    }
    if gate_id != "gutenberg-2026-08-30-unit-gate-batch1":
        result["inputs"]["front_matter_holds_excluded"] = len(reviewed) - len(sources)
    return result


def self_check():
    assert len(TOKEN.findall("can't re-enter naïve abc123 d’Art alpha_beta")) == 4
    source = b"A\r\n[Illustration: one\r\ntwo]\r\nB\r\n"
    assert remove_illustration_blocks(source) == (b"A\r\nB\r\n", 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?")
    parser.add_argument("--front-matter", type=Path, default=FRONT_MATTER)
    parser.add_argument("--gate-id", default="gutenberg-2026-08-30-unit-gate-batch1")
    parser.add_argument("--reviewed-on", default="2026-09-03")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("Project Gutenberg unit-gate self-check: PASS")
        return
    if args.directory is None:
        parser.error("directory is required")
    rendered = json.dumps(build(args.directory.resolve(), args.reviewed_on,
                                args.front_matter, args.gate_id),
                          ensure_ascii=False, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Generated gate differs from {args.output}")
        print(f"Project Gutenberg unit-gate verification: PASS ({args.output})")
    else:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
