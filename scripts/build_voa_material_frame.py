#!/usr/bin/env python3
"""Build the frozen Gate 1 VOA material-frame metadata from archive HTML."""

import argparse
import hashlib
import json
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin


BASE = "https://learningenglish.voanews.com"
START = datetime.strptime("2017-01-01", "%Y-%m-%d").date()
END = datetime.strptime("2020-12-31", "%Y-%m-%d").date()
SEED = "gate1-voa-frame-v1"
CATEGORIES = {
    "education": {"archive_url": f"{BASE}/z/959", "pages": range(36, 78)},
    "health": {"archive_url": f"{BASE}/z/955", "pages": range(50, 87)},
}
SEEN = {
    f"{BASE}/a/national-arboretum-a-quiter-place-to-enjoy-cherry-blossoms/4342830.html",
    f"{BASE}/a/ways-to-achieve-your-goals/4758976.html",
    f"{BASE}/a/how-to-inspect-your-own-writing/5668393.html",
    f"{BASE}/a/college-admissions-advice-understanding-common-application/4010355.html",
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


class ArchiveParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.div_depth = 0
        self.block_depth = None
        self.block = None
        self.date_parts = None
        self.records = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "div":
            self.div_depth += 1
            if (self.block is None and
                    "media-block" in attributes.get("class", "").split()):
                self.block_depth = self.div_depth
                self.block = {}
        if self.block is None:
            return
        if (tag == "a" and not self.block.get("path") and
                attributes.get("href", "").startswith("/a/") and
                attributes.get("title")):
            self.block["path"] = attributes["href"]
            self.block["title"] = attributes["title"]
        if (tag == "span" and
                "date--size-3" in attributes.get("class", "").split()):
            self.date_parts = []

    def handle_data(self, data):
        if self.date_parts is not None:
            self.date_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "span" and self.date_parts is not None:
            self.block["date"] = " ".join("".join(self.date_parts).split())
            self.date_parts = None
        if tag == "div":
            if self.block_depth == self.div_depth:
                if set(self.block) != {"path", "title", "date"}:
                    raise ValueError("Incomplete VOA archive article block.")
                self.records.append(self.block)
                self.block = None
                self.block_depth = None
            self.div_depth -= 1


def parse_archive(path):
    parser = ArchiveParser()
    parser.feed(path.read_text(encoding="utf-8"))
    if len(parser.records) != 12:
        raise ValueError(f"Expected 12 VOA archive records in {path.name}.")
    return parser.records


def build(directory):
    archive_pages = []
    occurrences = []
    for category, settings in CATEGORIES.items():
        expected = list(settings["pages"])
        paths = {int(path.stem.rsplit("p", 1)[1]): path
                 for path in directory.glob(f"{category}_p*.html")}
        if sorted(paths) != expected:
            raise ValueError(f"Missing or extra {category} archive pages.")
        for page in expected:
            path = paths[page]
            source = path.read_bytes()
            records = parse_archive(path)
            dates = [datetime.strptime(item["date"], "%B %d, %Y").date()
                     for item in records]
            archive_pages.append({
                "category": category,
                "page": page,
                "url": f'{settings["archive_url"]}?p={page}',
                "source_file": path.name,
                "source_bytes": len(source),
                "source_sha256": sha256(source),
                "first_record_date": dates[0].isoformat(),
                "last_record_date": dates[-1].isoformat(),
                "record_count": len(records),
            })
            for item, date in zip(records, dates):
                if START <= date <= END:
                    occurrences.append({
                        "category": category,
                        "publication_date": date.isoformat(),
                        "title": item["title"],
                        "canonical_url": urljoin(BASE, item["path"]),
                        "archive_page": page,
                    })

    by_url = {}
    for item in occurrences:
        current = by_url.setdefault(item["canonical_url"], {
            "publication_date": item["publication_date"],
            "title": item["title"],
            "canonical_url": item["canonical_url"],
            "archive_categories": [],
            "archive_pages": [],
        })
        if (current["publication_date"] != item["publication_date"] or
                current["title"] != item["title"]):
            raise ValueError(f'Conflicting archive metadata: {item["canonical_url"]}')
        current["archive_categories"].append(item["category"])
        current["archive_pages"].append(
            {"category": item["category"], "page": item["archive_page"]}
        )

    articles = list(by_url.values())
    for item in articles:
        item["sampling_category"] = next(
            category for category in CATEGORIES
            if category in item["archive_categories"]
        )
        item["selection_hash"] = sha256(
            f'{SEED}\n{item["canonical_url"]}'.encode()
        )
        item["seen_before_frame_freeze"] = item["canonical_url"] in SEEN

    for category in CATEGORIES:
        queue = sorted(
            (item for item in articles
             if item["sampling_category"] == category and
             not item["seen_before_frame_freeze"]),
            key=lambda item: (item["selection_hash"], item["canonical_url"]),
        )
        for rank, item in enumerate(queue, 1):
            item["target_blind_queue_rank"] = rank
            item["initial_metadata_draw"] = rank <= 12

    articles.sort(key=lambda item: (
        item["sampling_category"], item.get("target_blind_queue_rank", 0),
        item["canonical_url"],
    ))
    return {
        "frame_schema_version": "1.0.0",
        "frame_id": SEED,
        "generated_on": "2026-09-01",
        "construct": {
            "purpose": "bounded development-material discovery",
            "not_a_claim": "not an untouched probability sample or participant corpus",
            "date_start": START.isoformat(),
            "date_end": END.isoformat(),
            "selection_rule": "within each sampling category, exclude previously seen URLs and sort SHA-256(seed + LF + canonical URL); inspect in order until 12 eligible articles or the queue ends",
            "cross_category_duplicate_rule": "retain one article; Education takes sampling priority over Health & Lifestyle",
            "article_eligibility_still_requires": [
                "VOA-produced credit rather than adaptation or third-party source",
                "stable complete prose boundary",
                "rights and pedagogical-marking review",
            ],
        },
        "archives": archive_pages,
        "article_count": len(articles),
        "seen_article_count": sum(item["seen_before_frame_freeze"] for item in articles),
        "initial_metadata_draw_count": sum(item.get("initial_metadata_draw", False)
                                           for item in articles),
        "articles": articles,
    }


def self_check():
    fixture = '''<div class="media-block"><a href="/a/example/1.html"
      title="A &amp; B"></a><div><span class="date date--mb date--size-3">
      January 02, 2020</span></div></div>'''
    parser = ArchiveParser()
    parser.feed(fixture)
    assert parser.records == [{
        "path": "/a/example/1.html", "title": "A & B", "date": "January 02, 2020"
    }]
    assert sha256(f"{SEED}\n{BASE}/a/example/1.html".encode()) == (
        "136743f06d9b8d4cfd737f34a80d699e9a913d4a154563afe500c78b223696a3"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("VOA material-frame self-check: PASS")
        return
    if not args.directory or not args.output:
        parser.error("directory and --output are required")
    rendered = json.dumps(
        build(args.directory), ensure_ascii=False, separators=(",", ":")
    ) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Generated frame differs from {args.output}")
        print(f"VOA material-frame verification: PASS ({args.output})")
    else:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
