#!/usr/bin/env python3
"""Extract candidate VOA Learning English article prose from pinned AMP HTML."""

import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory

PRESENTER = re.compile(
    r"(?:(?:And (?:that['’]s|this is)[^.!?]*[.!?]\s*)|And\s+)?"
    r"I['’]m [\u00ad\u200b\u200c\u200d\ufeff]*[A-Z][A-Za-z]"
)
CREDIT = re.compile(
    r"\b(?:wrote|reported(?: on)?) this(?: story)? for (?:VOA )?Learning English\b",
    re.IGNORECASE,
)


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.article_depth = None
        self.content_depth = None
        self.paragraph = None
        self.paragraphs = []
        self.canonical_url = None
        self.json_ld = None
        self._json_parts = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.stack.append((tag, attributes))
        classes = set(attributes.get("class", "").split())
        if tag == "link" and attributes.get("rel") == "canonical":
            self.canonical_url = attributes.get("href")
        if tag == "script" and attributes.get("type") == "application/ld+json":
            self._json_parts = []
        if tag == "div" and "article-body" in classes:
            self.article_depth = len(self.stack)
        elif (tag == "div" and self.article_depth and
              len(self.stack) == self.article_depth + 1 and
              {"container", "wsw"} <= classes):
            self.content_depth = len(self.stack)
        elif tag == "p" and self.content_depth and len(self.stack) == self.content_depth + 1:
            self.paragraph = {
                "class": classes, "depth": len(self.stack), "parts": []
            }

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        if self._json_parts is not None:
            self._json_parts.append(data)
        if self.paragraph is not None:
            self.paragraph["parts"].append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._json_parts is not None:
            payload = json.loads("".join(self._json_parts))
            if payload.get("@type") == "NewsArticle":
                self.json_ld = payload
            self._json_parts = None
        if (tag == "p" and self.paragraph is not None and
                len(self.stack) == self.paragraph["depth"]):
            value = " ".join("".join(self.paragraph["parts"]).split())
            if value and "caption" not in self.paragraph["class"]:
                self.paragraphs.append(value)
            self.paragraph = None
        if self.stack:
            self.stack.pop()


def extract(path):
    source = path.read_bytes()
    parser = ArticleParser()
    parser.feed(source.decode("utf-8"))
    if not parser.json_ld or parser.json_ld.get("mainEntityOfPage") != parser.canonical_url:
        raise ValueError(f"Missing or inconsistent VOA article metadata: {path.name}")
    credit_index = next((index for index, item in enumerate(parser.paragraphs)
                         if CREDIT.search(item)), None)
    if credit_index is None:
        raise ValueError(f"Missing VOA author credit: {path.name}")
    signoff = next(((index, PRESENTER.search(parser.paragraphs[index]))
                    for index in range(credit_index - 1, -1, -1)
                    if PRESENTER.search(parser.paragraphs[index])), None)
    if signoff is None:
        raise ValueError(f"Missing VOA article boundary: {path.name}")
    while signoff[0] and PRESENTER.search(parser.paragraphs[signoff[0] - 1]):
        signoff = signoff[0] - 1, PRESENTER.search(parser.paragraphs[signoff[0] - 1])
    paragraphs = parser.paragraphs[:signoff[0]]
    prefix = parser.paragraphs[signoff[0]][:signoff[1].start()].strip()
    if prefix:
        paragraphs.append(prefix)
    if not paragraphs:
        raise ValueError(f"Missing VOA article prose: {path.name}")
    prose = "\n\n".join(paragraphs)
    return {
        "title": parser.json_ld["headline"],
        "canonical_url": parser.canonical_url,
        "publication_time": parser.json_ld["datePublished"],
        "modified_time": parser.json_ld["dateModified"],
        "credit": parser.paragraphs[credit_index],
        "source_file": path.name,
        "source_bytes": len(source),
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "extraction_rule": "direct non-caption p children of article-body container; stop before presenter sign-off; exclude media, captions, quiz, glossary, and site chrome; collapse internal whitespace; preserve paragraph breaks",
        "paragraph_count": len(paragraphs),
        "text_sha256": hashlib.sha256(prose.encode()).hexdigest(),
        "text": prose,
    }


def self_check():
    metadata = {
        "@type": "NewsArticle", "headline": "Test", "datePublished": "2020-01-01Z",
        "dateModified": "2020-01-02Z", "mainEntityOfPage": "https://example.test/a/1",
    }
    for credit in (
        "Tester wrote this story for VOA Learning English.",
        "Tester reported this for VOA Learning English.",
        "Tester reported on this story for VOA Learning English.",
        "Tester wrote this story for Learning English.",
    ):
        fixture = f'''<html><head><link rel="canonical" href="https://example.test/a/1">
          <script type="application/ld+json">{json.dumps(metadata)}</script></head><body>
          <div class="article-body"><div class="container wsw"><div><p>Nested caption</p></div>
          <p>A <strong>test</strong> paragraph. And that’s the report. I’m ­Tester.</p>
          <p>And I'm Editor.</p><p>Invitation after sign-off.</p>
          <p><em>{credit}</em></p>
          <h2>Words in This Story</h2><p>test — n.</p></div></div></body></html>'''
        with TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.html"
            path.write_text(fixture, encoding="utf-8")
            result = extract(path)
        assert result["title"] == "Test"
        assert result["text"] == "A test paragraph."
        assert result["paragraph_count"] == 1
        assert result["credit"] == credit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", type=Path, nargs="*")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        print("VOA article extraction self-check: PASS")
        return
    if not args.sources:
        parser.error("provide at least one VOA AMP HTML source")
    rendered = json.dumps({"items": [extract(path) for path in args.sources]},
                          ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote {len(args.sources)} VOA articles to {args.output}")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
