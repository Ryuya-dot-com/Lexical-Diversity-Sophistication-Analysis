import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from sample_benchmark_documents import build, compact, load_rows


CONTRACT_PATH = ROOT / "resources/sampling_frame.json"
FIXTURE_PATH = ROOT / "tests/fixtures/sampling_candidates.jsonl"
SCRIPT_PATH = ROOT / "scripts/sample_benchmark_documents.py"


class SamplingFrameTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        self.rows = load_rows(FIXTURE_PATH)

    def test_contract_freezes_target_blind_priority_without_selecting_documents(self):
        self.assertEqual(
            self.contract["status"],
            "contract_frozen_no_source_rows_no_target_search",
        )
        self.assertEqual(
            self.contract["selection"]["allocation_status"],
            "pending_IR-127_precision_plan",
        )
        self.assertEqual(self.contract["current_boundary"]["source_row_count"], 0)
        self.assertEqual(self.contract["current_boundary"]["target_search_count"], 0)
        self.assertIn("MWE forms", self.contract["candidate_input"]["forbidden_content"][1])
        for dependency in self.contract["dependencies"].values():
            self.assertEqual(
                hashlib.sha256((ROOT / dependency["path"]).read_bytes()).hexdigest(),
                dependency["sha256"],
            )

    def test_fixture_build_is_order_invariant_and_preserves_all_decisions(self):
        result = build(self.contract, self.rows)
        reversed_result = build(self.contract, list(reversed(self.rows)))
        self.assertEqual(result, reversed_result)
        self.assertEqual(result["summary"]["source_row_count"], 12)
        self.assertEqual(result["summary"]["queued_row_count"], 6)
        self.assertEqual(result["summary"]["structurally_excluded_row_count"], 6)
        self.assertEqual(
            result["summary"]["queue_count_by_stratum"],
            {"short": 2, "medium": 2, "long": 2},
        )
        self.assertEqual(result["summary"]["selected_document_count"], 0)
        self.assertEqual(result["summary"]["target_search_count"], 0)
        for queue in result["queues"].values():
            self.assertEqual(
                [item["queue_rank"] for item in queue],
                list(range(1, len(queue) + 1)),
            )
            self.assertTrue(all(not item["selected"] for item in queue))
            self.assertEqual(
                [item["selection_hash"] for item in queue],
                sorted(item["selection_hash"] for item in queue),
            )

        row = next(item for item in self.rows if item["page_id"] == 101)
        expected_hash = hashlib.sha256(compact([
            self.contract["frame_id"],
            self.contract["selection"]["seed"],
            row["page_id"],
            row["revision_id"],
        ]).encode("utf-8")).hexdigest()
        built = next(
            item
            for queue in result["queues"].values()
            for item in queue
            if item["page_id"] == 101
        )
        self.assertEqual(built["selection_hash"], expected_hash)
        self.assertEqual(built["admission_state"], "rights_pass_candidate")

        exclusions = {
            item["page_id"]: item["exclusion_codes"]
            for item in result["structural_exclusions"]
        }
        self.assertEqual(exclusions[107], ["namespace_not_zero"])
        self.assertEqual(exclusions[108], ["redirect"])
        self.assertEqual(exclusions[109], ["below_500_tokens"])
        self.assertEqual(exclusions[110], ["above_3999_tokens"])
        self.assertEqual(exclusions[111], ["fewer_than_5_paragraphs"])
        self.assertEqual(exclusions[112], ["model_not_wikitext"])

    def test_target_derived_or_exposed_input_fails_closed(self):
        target_derived = copy.deepcopy(self.rows)
        target_derived[0]["mwe_count"] = 3
        with self.assertRaisesRegex(ValueError, "candidate schema mismatch"):
            build(self.contract, target_derived)

        exposed = copy.deepcopy(self.rows)
        exposed[0]["target_exposure_status"] = "searched_for_take_in"
        with self.assertRaisesRegex(ValueError, "not target-blind"):
            build(self.contract, exposed)

    def test_command_line_self_check(self):
        result = subprocess.run(
            ["python3", str(SCRIPT_PATH), "--self-check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Wikipedia sampling-frame self-check: PASS\n")


if __name__ == "__main__":
    unittest.main()
