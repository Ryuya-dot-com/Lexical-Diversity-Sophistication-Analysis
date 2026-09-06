import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from simulate_benchmark_precision import simulate


PRECISION_PLAN = json.loads(
    (ROOT / "resources/precision_plan.json").read_text(encoding="utf-8")
)


def row(number, length, form, value):
    return {
        "record_id": f"r{number}",
        "document_id": f"d{number}",
        "length_stratum": length,
        "canonical_type_id": form,
        "weight": 1,
        "strata": {},
        "systems": {"pilot": {"numerator": value, "denominator": 1}},
    }


ROWS = [
    row(1, "short", "f1", 0),
    row(2, "short", "f1", 1),
    row(3, "long", "f2", 0),
    row(4, "long", "f3", 1),
]
ALLOCATIONS = [{
    "id": "target_blind_40",
    "documents_by_length": {"long": 20, "short": 20},
    "canonical_type_count": 30,
    "uses_target_conditioned_selection": False,
}]


class PrecisionSimulationTests(unittest.TestCase):
    def test_seeded_document_and_type_sensitivity_is_reproducible(self):
        first = simulate(ROWS, ["pilot"], "pilot", ALLOCATIONS, 0.5, "seed", 200)
        second = simulate(list(reversed(ROWS)), ["pilot"], "pilot", ALLOCATIONS, 0.5, "seed", 200)
        self.assertEqual(first, second)
        self.assertEqual(first["state"], "candidate_selected")
        self.assertEqual(first["selected_allocation_id"], "target_blind_40")
        self.assertTrue(first["allocations"][0]["primary_document"]["passes"])
        self.assertTrue(first["allocations"][0]["canonical_type_sensitivity"]["passes"])

    def test_insufficient_pilot_clusters_block_selection(self):
        result = simulate(ROWS[:1], ["pilot"], "pilot", ALLOCATIONS, 0.5, "seed", 20)
        self.assertEqual(result["state"], "blocked_insufficient_pilot_clusters")
        self.assertIsNone(result["selected_allocation_id"])

        conditioned = copy.deepcopy(ALLOCATIONS)
        conditioned[0]["uses_target_conditioned_selection"] = True
        result = simulate(ROWS, ["pilot"], "pilot", conditioned, 0.5, "seed", 20)
        self.assertEqual(result["state"], "claim_withheld_no_feasible_allocation")
        self.assertFalse(result["allocations"][0]["selection_eligible"])

    def test_public_plan_is_blocked_without_observed_inputs(self):
        plan = PRECISION_PLAN
        self.assertEqual(
            plan["status"],
            "blocked_pending_observed_inputs_and_pilot_activation",
        )
        self.assertEqual(plan["planning_pilot_design_resolution"]["state"], "resolved")
        self.assertTrue(all(value is None for value in plan["required_observed_inputs"].values()))
        self.assertIsNone(plan["current_result"]["selected_allocation_id"])
        self.assertFalse(plan["current_result"]["simulation_run"])
        for dependency in plan["dependencies"].values():
            path = ROOT / dependency["path"]
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(), dependency["sha256"]
            )


if __name__ == "__main__":
    unittest.main()
