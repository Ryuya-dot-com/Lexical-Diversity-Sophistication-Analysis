import hashlib
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from reconstruct_benchmark import stable_id, token_records
from screen_simplewiki_route2_rendered import extract_blocks


MANIFEST = ROOT / "resources/source_manifest.json"
CONTRACT = ROOT / "resources/preprocessing_contract.json"


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class SourceIdentityTests(unittest.TestCase):
    def test_dated_snapshot_identity_is_complete_without_source_acquisition(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        snapshot = manifest["source_snapshot"]
        self.assertEqual(
            [(item["name"], item["bytes"], item["md5"], item["sha1"]) for item in snapshot["files"]],
            [
                (
                    "enwiki-20260901-pages-articles-multistream.xml.bz2",
                    26797495184,
                    "f251f445259e452fafcb67d9f2c26513",
                    "e0a53c30c3a3b444018df95704d3d101cd618440",
                ),
                (
                    "enwiki-20260901-pages-articles-multistream-index.txt.bz2",
                    284375992,
                    "1d730f63aae2805882f11cbaf639ca53",
                    "ce0cbff600b0be2eed98da5ce189f847232d2282",
                ),
            ],
        )
        self.assertTrue(all(job["status"] == "done" for job in snapshot["jobs"].values()))
        self.assertTrue(all("/20260901/" in item["url"] for item in snapshot["files"]))
        self.assertFalse(any("/latest/" in item["url"] for item in snapshot["files"]))
        self.assertTrue(all(not item["acquired"] and item["local_sha256"] is None for item in snapshot["files"]))
        self.assertEqual(snapshot["target_search_count"], 0)

        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        for name in ("source_manifest", "metric_contract", "extractor", "reconstructor"):
            self.assertEqual(
                sha256_file(ROOT / contract["inputs"][name]),
                contract["inputs"][f"{name}_sha256"],
            )

    def test_extracted_surfaces_retain_character_and_byte_trace(self):
        html = """
        <h2>Lead</h2><p>Café, We’ll <b>take</b> it in.</p>
        <table><tr><td>discard this</td></tr></table>
        <p>They spill the beans.</p><h2>References</h2><p>discard tail</p>
        """
        blocks = extract_blocks(html)
        self.assertEqual(
            [(block["tag"], block["plain"]) for block in blocks],
            [
                ("h2", "Lead"),
                ("p", "Café, We’ll take it in."),
                ("p", "They spill the beans."),
            ],
        )
        text = "\n\n".join(block["plain"] for block in blocks)
        document_id = stable_id("doc", ["document-v1", "probe:rendered:v1"])
        first = token_records(text, document_id)
        second = token_records(text, document_id)
        self.assertEqual(first, second)
        self.assertEqual(first[1]["surface"], "We’ll")
        self.assertEqual(first[1]["normalized"], "we'll")
        encoded = text.encode("utf-8")
        for token in first:
            self.assertEqual(text[token["character_start"]:token["character_end"]], token["surface"])
            self.assertEqual(encoded[token["byte_start"]:token["byte_end"]].decode(), token["surface"])


if __name__ == "__main__":
    unittest.main()
