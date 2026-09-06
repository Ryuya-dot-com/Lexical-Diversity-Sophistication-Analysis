import hashlib
import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).parents[1]
QUEUE_PATH = ROOT / "resources/sense_mapping_queue.json"
SCRIPT_PATH = ROOT / "scripts/build_sense_mapping_queue.py"


class SenseMappingQueueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))

    def test_fixed_population_and_fail_closed_states(self):
        items = self.queue["items"]
        self.assertEqual(len(items), 146)
        self.assertEqual(
            [item["type_id"] for item in items],
            [f"ldfreq-en-vmwe-t{number:06d}" for number in range(1, 147)],
        )
        self.assertEqual(
            self.queue["summary"]["state_counts"],
            {"candidate_set": 3, "unresolved": 143},
        )
        self.assertTrue(self.queue["summary"]["exact_misses_retained_in_denominator"])
        self.assertEqual(self.queue["summary"]["mapped"], 0)
        self.assertEqual(self.queue["summary"]["ooi_pending"], 0)
        self.assertEqual(
            {item["input_canonical_lemma"] for item in items if item["candidates"]},
            {"home - cook", "jump - start", "think so"},
        )
        self.assertTrue(all(
            item["mapping_state"] in {"candidate_set", "unresolved"}
            and item["observed_vmwe_categories"] == ["V.VID"]
            for item in items
        ))

    def test_candidates_are_source_bounded_and_contain_no_lexicographic_text(self):
        candidates = [candidate for item in self.queue["items"]
                      for candidate in item["candidates"]]
        self.assertEqual(len(candidates), 11)
        self.assertEqual(
            {candidate["source_inventory_id"] for candidate in candidates},
            {"oewn", "enwiktionary-kaikki"},
        )
        self.assertTrue(all(
            candidate["mapping_relation"] == "candidate_only"
            and candidate["verification_status"] == "unreviewed"
            and candidate["stage"] in {4, 5}
            for candidate in candidates
        ))
        serialized = QUEUE_PATH.read_text(encoding="utf-8")
        for prohibited in ('"gloss"', '"glosses"', '"example"', '"examples"',
                           '"translation"', '"translations"', "research_data/"):
            self.assertNotIn(prohibited, serialized)

    def test_dependencies_and_self_check(self):
        for dependency in self.queue["dependencies"].values():
            path = ROOT / dependency["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                             dependency["sha256"])
        result = subprocess.run(
            ["python3", str(SCRIPT_PATH), "--self-check"], cwd=ROOT,
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Sense mapping queue self-check: PASS\n")


if __name__ == "__main__":
    unittest.main()
