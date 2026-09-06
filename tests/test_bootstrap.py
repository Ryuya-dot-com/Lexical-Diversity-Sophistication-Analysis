import copy
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from bootstrap_evaluation import analyze


def row(identifier, document, length, form, category, left, right, denominator=1):
    return {
        "record_id": identifier,
        "document_id": document,
        "length_stratum": length,
        "canonical_type_id": form,
        "weight": 1,
        "strata": {"category": category},
        "systems": {
            "left": {"numerator": left, "denominator": denominator},
            "right": {"numerator": right, "denominator": denominator},
        },
    }


ROWS = [
    row("r1", "d1", "short", "f1", "VPC.full", 1, 1),
    row("r2", "d2", "short", "f1", "VPC.full", 0, 1),
    row("r3", "d3", "long", "f2", "VID", 0, 0),
    row("r4", "d4", "long", "f3", "VID", 1, 0),
]


class BootstrapTests(unittest.TestCase):
    def test_seeded_stratified_cluster_and_paired_results_are_reproducible(self):
        args = (["left", "right"], {"category": ["VPC.full", "VID"]}, "fixed-seed", 200, 0.95)
        first = analyze(ROWS, *args)
        second = analyze(list(reversed(ROWS)), *args)
        self.assertEqual(first, second)

        overall = first["overall"]
        primary = overall["primary_document"]
        sensitivity = overall["canonical_form_sensitivity"]
        self.assertEqual(primary["cluster_count"], 4)
        self.assertEqual(sensitivity["cluster_count"], 3)
        self.assertEqual(primary["intervals"]["left"]["point_estimate"], 0.5)
        self.assertEqual(primary["intervals"]["right"]["point_estimate"], 0.5)
        self.assertEqual(primary["paired_differences"]["right_minus_left"]["point_estimate"], 0.0)
        self.assertEqual(
            first["prespecified_strata"]["category"]["VPC.full"]["primary_document"]["cluster_count"],
            2,
        )

    def test_degenerate_and_undefined_resamples_withhold_intervals(self):
        one = analyze(ROWS[:1], ["left", "right"], {"category": ["VPC.full"]}, "seed", 20, 0.95)
        interval = one["overall"]["primary_document"]["intervals"]["left"]
        self.assertEqual(interval["state"], "point_estimate_only_fewer_than_two_clusters_in_resampling_stratum")
        self.assertIsNone(interval["lower"])
        self.assertEqual(interval["requested_resamples"], 20)

        one_per_length = analyze(ROWS[::2], ["left", "right"], {"category": ["VPC.full", "VID"]}, "seed", 20, 0.95)
        stratified = one_per_length["overall"]["primary_document"]["intervals"]["left"]
        self.assertEqual(stratified["state"], "point_estimate_only_fewer_than_two_clusters_in_resampling_stratum")

        sparse = copy.deepcopy(ROWS[:2])
        sparse[0]["systems"]["left"] = {"numerator": 0, "denominator": 0}
        sparse[0]["systems"]["right"] = {"numerator": 0, "denominator": 0}
        result = analyze(sparse, ["left", "right"], {"category": ["VPC.full"]}, "seed", 50, 0.95)
        state = result["overall"]["primary_document"]["intervals"]["left"]["state"]
        self.assertEqual(state, "interval_withheld_undefined_resample")


if __name__ == "__main__":
    unittest.main()
