from html.parser import HTMLParser
from pathlib import Path
import unittest


INDEX = Path(__file__).parents[1] / "index.html"
APP = Path(__file__).parents[1] / "app.mjs"
METRICS = Path(__file__).parents[1] / "metrics.mjs"


class StructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.label_for = set()
        self.nested_labels = set()
        self.controls = []
        self.references = []
        self.label_depth = 0
        self.html_lang = None
        self.main_count = 0
        self.h1_count = 0
        self.status_regions = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.append(element_id)
        if tag == "html":
            self.html_lang = values.get("lang")
        elif tag == "main":
            self.main_count += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "label":
            self.label_depth += 1
            if values.get("for"):
                self.label_for.add(values["for"])
        elif tag in {"input", "textarea", "select"}:
            self.controls.append(element_id)
            if self.label_depth and element_id:
                self.nested_labels.add(element_id)
        elif tag == "button":
            if values.get("type") not in {"button", "submit", "reset"}:
                raise AssertionError("Every button must declare its type.")
        if values.get("role") == "status" and values.get("aria-live"):
            self.status_regions += 1
        for name in ("aria-labelledby", "aria-describedby"):
            if values.get(name):
                self.references.extend(values[name].split())

    def handle_endtag(self, tag):
        if tag == "label":
            self.label_depth -= 1


class HtmlContractTests(unittest.TestCase):
    def test_accessibility_structure(self):
        parser = StructureParser()
        parser.feed(INDEX.read_text(encoding="utf-8"))
        ids = set(parser.ids)

        self.assertEqual(parser.html_lang, "ja")
        self.assertEqual(parser.main_count, 1)
        self.assertEqual(parser.h1_count, 1)
        self.assertEqual(len(parser.ids), len(ids), "HTML IDs must be unique")
        self.assertGreaterEqual(parser.status_regions, 1)
        self.assertTrue(set(parser.references) <= ids)
        for control in parser.controls:
            self.assertIsNotNone(control)
            self.assertTrue(
                control in parser.label_for or control in parser.nested_labels,
                f"Unlabelled control: {control}",
            )

    def test_static_boundary(self):
        source = INDEX.read_text(encoding="utf-8")
        app_source = APP.read_text(encoding="utf-8")
        metrics_source = METRICS.read_text(encoding="utf-8")
        for forbidden in ("/api/", 'type="file"', " action=", " method="):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)
        for forbidden in (
            "localStorage",
            "sessionStorage",
            "indexedDB",
            "document.cookie",
            "XMLHttpRequest",
            "sendBeacon",
            "WebSocket",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, app_source)
        network_calls_removed = app_source.replace(
            "fetch('samples.json')", ""
        ).replace("fetch('metric_contract.json')", "").replace("fetch('mwe_contract.json')", "")
        self.assertNotIn("fetch(", network_calls_removed)
        self.assertIn('<script type="module" src="app.mjs"></script>', source)
        self.assertIn("Content-Security-Policy", source)
        self.assertIn("connect-src 'self'", source)
        self.assertIn("form-action 'none'", source)
        self.assertIn("TypesとTTRは独立した証拠ではありません", app_source)
        self.assertIn('id="scenario"', source)
        self.assertIn('id="capabilities-title"', source)
        self.assertIn('id="can-do-title"', source)
        self.assertIn('id="cannot-do-title"', source)
        self.assertIn('id="workspace-form"', source)
        self.assertIn('id="mwe-form"', source)
        self.assertIn('id="mwe-occurrences"', source)
        self.assertIn('id="export-mwe-csv"', source)
        self.assertIn('id="method-references"', source)
        self.assertIn('id="rights-attestation"', source)
        self.assertIn('<option value="declared-segments">', source)
        self.assertIn('<option value="batch">', source)
        self.assertIn('id="segment-rows"', source)
        self.assertIn('id="batch-json"', source)
        self.assertIn('id="batch-rows"', source)
        self.assertIn("max_utf16_code_units_per_batch_json", app_source)
        self.assertIn("raw_text_included:false", metrics_source.replace(" ", ""))


if __name__ == "__main__":
    unittest.main()
