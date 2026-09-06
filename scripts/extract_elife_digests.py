#!/usr/bin/env python3
"""Extract pinned eLife digest text and provenance from JATS XML."""

import argparse
import hashlib
import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET


XLINK_HREF = "{http://www.w3.org/1999/xlink}href"
FILENAME = re.compile(r"elife-(\d+)-v(\d+)\.xml")


def text(element):
    return " ".join("".join(element.itertext()).split()) if element is not None else ""


def extract(path):
    match = FILENAME.fullmatch(path.name)
    if not match:
        raise ValueError(f"Unexpected eLife filename: {path.name}")
    source = path.read_bytes()
    meta = ET.fromstring(source).find("./front/article-meta")
    if meta is None:
        raise ValueError(f"Missing article metadata: {path.name}")

    ids = {item.get("pub-id-type"): text(item) for item in meta.findall("./article-id")}
    title = text(meta.find("./title-group/article-title"))
    if ids.get("publisher-id") != match.group(1) or "doi" not in ids or not title:
        raise ValueError(f"Article identity mismatch: {path.name}")
    summaries = [item for item in meta.findall("./abstract")
                 if item.get("abstract-type") in {"executive-summary", "plain-language-summary"}]
    if len(summaries) != 1 or text(summaries[0].find("./title")) != "eLife digest":
        raise ValueError(f"Expected one eLife digest: {path.name}")
    paragraphs = [text(item) for item in summaries[0].findall("./p")]
    paragraphs = [item for item in paragraphs if item and not item.startswith("DOI:")]
    if not paragraphs:
        raise ValueError(f"Empty eLife digest: {path.name}")

    publication = next((item for item in meta.findall("./pub-date")
                        if item.get("date-type") in {"pub", "publication"}), None)
    license_element = meta.find("./permissions/license")
    if publication is None or license_element is None:
        raise ValueError(f"Missing publication or license metadata: {path.name}")
    date = "-".join([
        publication.findtext("year", ""),
        publication.findtext("month", "").zfill(2),
        publication.findtext("day", "").zfill(2),
    ])
    authors = []
    for contributor in meta.findall('./contrib-group/contrib[@contrib-type="author"]'):
        surname = contributor.findtext("./name/surname")
        given = contributor.findtext("./name/given-names")
        if surname:
            authors.append(" ".join(filter(None, [given, surname])))
    digest = "\n\n".join(paragraphs)
    return {
        "article_id": ids["publisher-id"],
        "doi": ids["doi"],
        "version": int(match.group(2)),
        "title": title,
        "authors": authors,
        "publication_date": date,
        "license_url": license_element.get(XLINK_HREF),
        "copyright_statement": text(meta.find("./permissions/copyright-statement")),
        "source_file": path.name,
        "source_bytes": len(source),
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "extraction_rule": "direct eLife-digest p elements; DOI metadata paragraph excluded; internal whitespace collapsed; paragraph breaks preserved",
        "paragraph_count": len(paragraphs),
        "digest_sha256": hashlib.sha256(digest.encode()).hexdigest(),
        "digest": digest,
    }


def self_check():
    fixture = b'''<article xmlns:xlink="http://www.w3.org/1999/xlink"><front><article-meta>
      <article-id pub-id-type="publisher-id">1</article-id><article-id pub-id-type="doi">10/x</article-id>
      <title-group><article-title>A <italic>test</italic></article-title></title-group>
      <contrib-group><contrib contrib-type="author"><name><surname>Doe</surname><given-names>J</given-names></name></contrib></contrib-group>
      <pub-date date-type="publication"><day>2</day><month>3</month><year>2020</year></pub-date>
      <permissions><copyright-statement>Copyright</copyright-statement><license xlink:href="https://creativecommons.org/licenses/by/4.0/"/></permissions>
      <abstract abstract-type="executive-summary"><title>eLife digest</title><p>One  sentence.</p><p>DOI: skip</p><p>Two.</p></abstract>
    </article-meta></front></article>'''
    with TemporaryDirectory() as directory:
        path = Path(directory) / "elife-1-v2.xml"
        path.write_bytes(fixture)
        result = extract(path)
    assert result["title"] == "A test"
    assert result["publication_date"] == "2020-03-02"
    assert result["digest"] == "One sentence.\n\nTwo."
    assert result["paragraph_count"] == 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", type=Path, nargs="*")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("eLife digest extraction self-check: PASS")
        return
    if not args.sources:
        parser.error("provide at least one versioned eLife XML source")
    rendered = json.dumps({"items": [extract(path) for path in args.sources]},
                          ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {len(args.sources)} eLife digests to {args.output}")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
