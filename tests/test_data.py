import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
SAMPLES = json.loads((ROOT / "samples.json").read_text(encoding="utf-8"))
REFERENCE_TEMPLATE = json.loads(
    (ROOT / "reference_profile_template.json").read_text(encoding="utf-8")
)
MWE_CONTRACT = json.loads((ROOT / "mwe_contract.json").read_text(encoding="utf-8"))
STREUSLE_PROFILE = json.loads(
    (ROOT / "benchmarks/streusle_v5_vpc_vid.json").read_text(encoding="utf-8")
)


class SampleManifestTests(unittest.TestCase):
    def test_streusle_profile_is_external_and_matches_the_mwe_contract(self):
        self.assertEqual(
            set(STREUSLE_PROFILE["projection"]["category_mapping"].values()),
            set(MWE_CONTRACT["occurrence_record"]["categories"]),
        )
        self.assertFalse(STREUSLE_PROFILE["rights"]["data_bundled_here"])
        self.assertFalse(STREUSLE_PROFILE["rights"]["upstream_code_copied_here"])
        self.assertEqual(
            STREUSLE_PROFILE["expected_report"]["test"]["target_occurrences"], 40
        )
        self.assertEqual(
            STREUSLE_PROFILE["expected_surface_baseline"]["unseen_exact_span_recall"]["value"],
            0.0,
        )

    def test_reference_profile_template_keeps_channels_and_evidence_separate(self):
        self.assertEqual(
            REFERENCE_TEMPLATE["allowed_values"]["coverage_channel"],
            ["word", "mwe_form", "mwe_sense"],
        )
        manifest = REFERENCE_TEMPLATE["manifest_template"]
        self.assertEqual(set(manifest), set(REFERENCE_TEMPLATE["required_sections"]))
        self.assertIsNone(manifest["construct"]["coverage_channel"])
        self.assertIsNone(manifest["source"]["artifact_sha256"])
        self.assertIsNone(manifest["measurement"]["denominator_definition"])
        self.assertIsNone(manifest["rights"]["browser_delivery_permitted"])
        self.assertIn(
            "no profile becomes a silent universal default; every result exports its profile identity and limitations",
            REFERENCE_TEMPLATE["admission_rules"],
        )

    def test_manifest_describes_three_reviewed_scenarios(self):
        self.assertEqual(set(SAMPLES), {"samples_version", "comparison_sets"})
        self.assertEqual(SAMPLES["samples_version"], "0.3.0-probe")
        self.assertEqual(len(SAMPLES["comparison_sets"]), 3)

        ids = set()
        for comparison in SAMPLES["comparison_sets"]:
            self.assertEqual(
                set(comparison),
                {"id", "label_ja", "question_ja", "design", "samples"},
            )
            self.assertEqual(len(comparison["samples"]), 2)
            self.assertEqual(
                set(comparison["design"]),
                {
                    "held_constant_ja",
                    "manipulated_ja",
                    "not_controlled_ja",
                    "interpretation_ja",
                },
            )
            for sample in comparison["samples"]:
                self.assertEqual(
                    set(sample), {"id", "label_ja", "text", "provenance", "result"}
                )
                self.assertNotIn(sample["id"], ids)
                ids.add(sample["id"])
                self.assertEqual(
                    set(sample["provenance"]),
                    {
                        "kind",
                        "author",
                        "created_on",
                        "authoring_method",
                        "review_status",
                        "rights_status",
                    },
                )
                self.assertEqual(sample["provenance"]["kind"], "synthetic")
                self.assertEqual(
                    sample["provenance"]["review_status"], "internal-probe"
                )
                self.assertEqual(
                    sample["provenance"]["rights_status"],
                    "project-authored; MIT or CC BY 4.0",
                )
                self.assertEqual(
                    set(sample["result"]),
                    {"tokens", "types", "type_token_ratio", "hapax_types"},
                )

    def test_scenario_relations_are_explicit(self):
        comparisons = {
            item["id"]: item for item in SAMPLES["comparison_sets"]
        }

        repeated, varied = comparisons["matched-repetition"]["samples"]
        self.assertEqual(repeated["id"], "repeated-content")
        self.assertEqual(varied["id"], "varied-content")
        self.assertEqual(repeated["result"]["tokens"], 100)
        self.assertEqual(varied["result"]["tokens"], 100)
        self.assertGreater(varied["result"]["types"], repeated["result"]["types"])

        one_sentence, seven_sentences = comparisons["segmentation-invariance"][
            "samples"
        ]
        self.assertEqual(one_sentence["text"].replace("; ", ". "), seven_sentences["text"])
        self.assertEqual(one_sentence["result"], seven_sentences["result"])

        short, full = comparisons["nested-length"]["samples"]
        self.assertTrue(full["text"].startswith(short["text"]))
        self.assertEqual(short["result"]["tokens"], 14)
        self.assertEqual(full["result"]["tokens"], 100)
        self.assertNotEqual(
            short["result"]["type_token_ratio"],
            full["result"]["type_token_ratio"],
        )


if __name__ == "__main__":
    unittest.main()
