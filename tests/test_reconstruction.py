import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts/reconstruct_benchmark.py"
MANIFEST = ROOT / "resources/source_manifest.json"
FIXTURE = ROOT / "tests/fixtures/reconstruction_source.txt"


class ReconstructionTests(unittest.TestCase):
    def copy_source(self, destination):
        target = destination / "tests/fixtures/reconstruction_source.txt"
        target.parent.mkdir(parents=True)
        shutil.copyfile(FIXTURE, target)
        return target

    def run_check(self, source_root):
        return subprocess.run(
            ["python3", str(SCRIPT), str(source_root), "--manifest", str(MANIFEST)],
            capture_output=True,
            text=True,
        )

    def test_clean_copy_reconstructs_stable_token_and_occurrence_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            source_root = Path(directory)
            self.copy_source(source_root)
            result = self.run_check(source_root)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        document = report["documents"][0]
        self.assertEqual(
            [token["id"] for token in document["tokens"]],
            [f"t{index}" for index in range(1, 10)],
        )
        self.assertEqual(
            document["tokens"][1],
            {
                "id": "t2",
                "character_start": 5,
                "character_end": 9,
                "byte_start": 5,
                "byte_end": 9,
            },
        )
        self.assertEqual(
            [item["occurrence_id"] for item in document["occurrences"]],
            ["occ-9f4a76534fc43fb7d76a", "occ-75fd33706aa20bfb76f7"],
        )

    def test_same_length_source_change_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            source_root = Path(directory)
            target = self.copy_source(source_root)
            source = target.read_bytes()
            target.write_bytes(b"X" + source[1:])
            result = self.run_check(source_root)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("source SHA-256 mismatch", result.stderr)


if __name__ == "__main__":
    unittest.main()
