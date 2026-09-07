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
        self.details_stack = []
        self.details_for = {}
        self.required_controls = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.append(element_id)
            self.details_for[element_id] = tuple(self.details_stack)
        if tag == "details":
            self.details_stack.append(element_id)
        if "required" in values:
            self.required_controls.append(element_id)
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
        elif tag == "details":
            self.details_stack.pop()


class HtmlContractTests(unittest.TestCase):
    def test_review_and_export_guidance(self):
        source = INDEX.read_text(encoding="utf-8")
        for wording in (
            "自動で正解や語義を確定する分析器ではありません",
            "決められない候補は未確定のまま残せます",
            "原文欄・語の一覧はありません",
            "根拠に引用した文章も含まれます",
            "再開用JSONには原文・候補パターン・記録済みの判断と根拠を含みます",
            "共有用の匿名化ファイルではありません",
            "ページを閉じても自動保存されません",
            "ファイル保存ではありません",
            "記録するまでは書き出し・再開用ファイルに反映されません",
            "未確定の候補が残っているだけでは保存を止めません",
            "判断を自動確定することもありません",
            'id="mwe-pending-edits"',
            'id="mwe-pending-list"',
            'id="mwe-current-document-status"',
            '選択だけではレビューは切り替わりません',
            '一方を未判定に戻しても他方は保持します',
            '取り消すと記録と入力途中の内容を保持します',
            '端末や操作によっては表示されません',
            'ファイルの保存完了をアプリでは確認できない',
        ):
            self.assertIn(wording, source)
        for help_id in (
            "mwe-result-export-help", "mwe-resume-export-help", "mwe-document-set-export-help"
        ):
            self.assertIn(f'aria-describedby="{help_id}"', source)

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
        # Keep mandatory inputs and candidate decisions outside collapsed detail panels.
        for control in parser.required_controls:
            self.assertEqual(parser.details_for[control], ())
        self.assertEqual(parser.details_for["mwe-occurrences"], ())
        self.assertEqual(parser.details_for["bnc-coca-profile"], ("mwe-local-reference",))
        self.assertEqual(parser.details_for["mwe-workspace-file"], ("mwe-resume-options",))
        self.assertEqual(parser.details_for["word-coverage-items"], ("mwe-coverage-details",))
        for earlier, later in (
            ("word-reference", "bnc-coca-profile"),
            ("mwe-analyze-button", "mwe-workspace-file"),
            ("mwe-occurrences", "mwe-manual-candidate"),
            ("mwe-occurrences", "mwe-summary"),
        ):
            self.assertLess(parser.ids.index(earlier), parser.ids.index(later))

    def test_static_boundary(self):
        source = INDEX.read_text(encoding="utf-8")
        app_source = APP.read_text(encoding="utf-8")
        metrics_source = METRICS.read_text(encoding="utf-8")
        for forbidden in ("/api/", " action=", " method="):
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
        ).replace("fetch('metric_contract.json')", "").replace(
            "fetch('mwe_contract.json')", ""
        ).replace(
            "fetch('resources/tubelex_en_regex_ascii_2025.json')", ""
        ).replace(
            "fetch('resources/ngsl_1_2_ascii_forms.json')", ""
        ).replace("fetch('resources/oewn_2025_multiword_verbs.json')", "").replace(
            "fetch('resources/oewn_take_in_2025.json')", ""
        )
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
        self.assertIn('id="export-word-coverage-csv"', source)
        self.assertIn('id="word-coverage-items"', source)
        self.assertIn('id="word-reference"', source)
        self.assertEqual(source.count('type="file"'), 3)
        self.assertIn('id="bnc-coca-profile"', source)
        self.assertIn('id="mwe-workspace-file"', source)
        self.assertIn('id="export-mwe-workspace"', source)
        self.assertIn('id="mwe-document-set-form"', source)
        self.assertIn('id="mwe-document-set-file"', source)
        self.assertIn('id="save-mwe-document"', source)
        self.assertIn('id="load-mwe-document"', source)
        self.assertIn('id="export-mwe-document-set"', source)
        self.assertIn('<option value="bnc-coca-1000" data-local-profile disabled>', source)
        self.assertIn('<option value="bnc-coca-2000" data-local-profile disabled>', source)
        self.assertIn('<option value="ngsl-2000">', source)
        self.assertIn("runtimeProfileSha256", app_source)
        self.assertIn("lockMweSourceInputs(true)", app_source)
        self.assertIn("prepareMweSenseReferenceProfile", app_source)
        self.assertIn("Save contextual sense", app_source)
        self.assertIn("Idiomaticityを保存", app_source)
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
