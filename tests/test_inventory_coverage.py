import hashlib
import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).parents[1]
AUDIT = ROOT / "resources/hybrid_inventory_coverage_v2.json"
SCRIPT = ROOT / "scripts/audit_hybrid_inventory_coverage.py"


class InventoryCoverageTests(unittest.TestCase):
    def test_full_denominators_states_and_reproduction_contract(self):
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        full = audit["summary"]["full_target_population"]
        self.assertEqual(full["occurrences"]["denominator"], 624)
        self.assertEqual(full["types"]["denominator"], 389)
        self.assertEqual(full["occurrences"]["admitted_inventory_available"], 0)
        self.assertEqual(full["occurrences"]["candidate_seed_only"], 57)
        self.assertEqual(full["occurrences"]["inventory_status_unresolved"], 57)
        self.assertEqual(full["by_category"]["V.VID"]["occurrences"]["denominator"], 319)
        self.assertEqual(full["by_category"]["V.VID"]["occurrences"]["candidate_seed_only"], 21)
        self.assertEqual(full["by_continuity"]["discontinuous"]["denominator"], 188)
        self.assertFalse(full["candidate_count_distribution"]["selected_only_denominator_permitted"])

        pilot = audit["summary"]["ir132_vid_pilot"]
        self.assertEqual(pilot["types"]["denominator"], 14)
        self.assertEqual(pilot["occurrences"]["denominator"], 52)
        self.assertEqual(pilot["occurrences"]["candidate_seed_only"], 19)
        self.assertEqual(pilot["occurrences"]["observed_out_of_inventory"], 0)
        self.assertEqual(audit["stop_decision"]["vid_sense_claim"], "held")
        self.assertEqual(audit["stop_decision"]["discontinuous_sense_claim"], "held")
        for dependency in audit["dependencies"].values():
            path = ROOT / dependency["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), dependency["sha256"])

        result = subprocess.run(
            ["python3", str(SCRIPT), "--self-check"], cwd=ROOT,
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"self_check": "pass"})


if __name__ == "__main__":
    unittest.main()
