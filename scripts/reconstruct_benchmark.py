#!/usr/bin/env python3
"""Verify source bytes and reconstruct stable standoff identifiers."""

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKEN_PATTERN = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def stable_id(prefix, fields):
    payload = json.dumps(fields, ensure_ascii=False, separators=(",", ":")).encode()
    return f"{prefix}-{sha256(payload)[:20]}"


def is_boundary(character):
    return not character or not (character.isalpha() or character.isnumeric() or character == "_")


def token_records(text, document_id):
    byte_offsets = [0]
    for character in text:
        byte_offsets.append(byte_offsets[-1] + len(character.encode("utf-8")))
    records = []
    for match in TOKEN_PATTERN.finditer(text):
        if not is_boundary(text[match.start() - 1] if match.start() else ""):
            continue
        if not is_boundary(text[match.end()] if match.end() < len(text) else ""):
            continue
        surface = match.group()
        records.append(
            {
                "id": f"t{len(records) + 1}",
                "document_id": document_id,
                "surface": surface,
                "normalized": surface.replace("’", "'").lower(),
                "character_start": match.start(),
                "character_end": match.end(),
                "byte_start": byte_offsets[match.start()],
                "byte_end": byte_offsets[match.end()],
            }
        )
    return records


def reconstruct_document(spec, source_root):
    source_bytes = (source_root / spec["local_path"]).read_bytes()
    if len(source_bytes) != spec["source_bytes"]:
        raise ValueError(f"source byte length mismatch: {spec['document_id']}")
    if sha256(source_bytes) != spec["source_sha256"]:
        raise ValueError(f"source SHA-256 mismatch: {spec['document_id']}")
    text = source_bytes.decode(spec["encoding"], errors="strict")
    document_id = stable_id("doc", ["document-v1", spec["immutable_source_id"]])
    if document_id != spec["document_id"]:
        raise ValueError(f"document ID mismatch: {spec['document_id']}")
    tokens = token_records(text, document_id)
    token_payload = [
        [
            token["id"],
            token["normalized"],
            token["character_start"],
            token["character_end"],
            token["byte_start"],
            token["byte_end"],
        ]
        for token in tokens
    ]
    if len(tokens) != spec["token_count"]:
        raise ValueError(f"token count mismatch: {document_id}")
    if sha256(json.dumps(token_payload, separators=(",", ":")).encode()) != spec["token_sha256"]:
        raise ValueError(f"token SHA-256 mismatch: {document_id}")

    positions = {token["id"]: index for index, token in enumerate(tokens)}
    occurrences = []
    for occurrence in spec["occurrences"]:
        members = occurrence["member_token_ids"]
        if len(members) < 2 or len(set(members)) != len(members):
            raise ValueError(f"invalid member token IDs: {document_id}")
        try:
            member_positions = [positions[token_id] for token_id in members]
        except KeyError as error:
            raise ValueError(f"unknown member token ID: {document_id}") from error
        if member_positions != sorted(member_positions):
            raise ValueError(f"unordered member token IDs: {document_id}")
        expected_gaps = [
            tokens[index]["id"]
            for index in range(member_positions[0] + 1, member_positions[-1])
            if index not in member_positions
        ]
        if occurrence["gap_token_ids"] != expected_gaps:
            raise ValueError(f"gap token IDs mismatch: {document_id}")
        occurrence_id = stable_id(
            "occ",
            [
                "occurrence-v1",
                document_id,
                occurrence["category"],
                occurrence["canonical_form"],
                members,
            ],
        )
        if occurrence_id != occurrence["occurrence_id"]:
            raise ValueError(f"occurrence ID mismatch: {document_id}")
        occurrences.append(
            {
                "occurrence_id": occurrence_id,
                "member_token_ids": members,
                "gap_token_ids": expected_gaps,
            }
        )
    return {
        "document_id": document_id,
        "source_sha256": spec["source_sha256"],
        "token_sha256": spec["token_sha256"],
        "tokens": [
            {
                key: token[key]
                for key in (
                    "id",
                    "character_start",
                    "character_end",
                    "byte_start",
                    "byte_end",
                )
            }
            for token in tokens
        ],
        "occurrences": occurrences,
    }


def reconstruct(manifest, source_root):
    if manifest["status"] != "snapshot_frozen_no_source_content_acquired":
        raise ValueError("unsupported source manifest status")
    return {
        "manifest_id": manifest["manifest_id"],
        "status": "verified",
        "documents": [
            reconstruct_document(document, source_root)
            for document in manifest["documents"]
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_root", type=Path, nargs="?", default=ROOT)
    parser.add_argument(
        "--manifest", type=Path, default=ROOT / "resources/source_manifest.json"
    )
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = reconstruct(manifest, args.source_root)
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
