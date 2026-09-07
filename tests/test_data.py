import json
import hashlib
import fnmatch
import subprocess
import tempfile
from collections import Counter
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
STREUSLE_GAP_BASELINE = json.loads(
    (ROOT / "resources/streusle_gap_dependency_baseline.json").read_text(
        encoding="utf-8"
    )
)
CORE_MWE_EVIDENCE = json.loads(
    (ROOT / "resources/mwe_core_evidence_admission_2026_09_03.json").read_text(
        encoding="utf-8"
    )
)
MWEASWSD_REUSE_AUDIT = json.loads(
    (ROOT / "resources/mweaswsd_semcor_reuse_audit_2026_09_03.json").read_text(
        encoding="utf-8"
    )
)
WSD_MWE_SENSE_AUDIT = json.loads(
    (ROOT / "resources/wsd_mwe_sense_slice_audit_2026_09_03.json").read_text(
        encoding="utf-8"
    )
)
HYBRID_SENSE_CONTRACT_PATH = (
    ROOT / "resources/hybrid_sense_inventory_contract_2026_09_03.json"
)
HYBRID_SENSE_CONTRACT = json.loads(
    HYBRID_SENSE_CONTRACT_PATH.read_text(encoding="utf-8")
)
KAIKKI_VID_AUDIT = json.loads(
    (ROOT / "resources/streusle_v5_kaikki_vid_audit_2026_09_03.json").read_text(
        encoding="utf-8"
    )
)
LRE_READINESS = json.loads(
    (ROOT / "resources/lre_submission_readiness_2026_09_03.json").read_text(
        encoding="utf-8"
    )
)
CLAIM_EVIDENCE_MAP = json.loads(
    (ROOT / "resources/claim_evidence_map.json").read_text(encoding="utf-8")
)
DECISION_LOG = json.loads(
    (ROOT / "resources/decision_log.json").read_text(encoding="utf-8")
)
DOWNSTREAM_SELECTION_MEMO = (
    ROOT / "resources/downstream_selection_memo.md"
).read_text(encoding="utf-8")
GOVERNANCE = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
ETHICS_DETERMINATION = (
    ROOT / "resources/ethics_determination.md"
).read_text(encoding="utf-8")
TARGET_POPULATION = json.loads(
    (ROOT / "resources/target_population_contract.json").read_text(encoding="utf-8")
)
EVALUATION_STRATA = json.loads(
    (ROOT / "resources/evaluation_strata.json").read_text(encoding="utf-8")
)
SPLIT_PROTOCOL = json.loads(
    (ROOT / "resources/split_protocol.json").read_text(encoding="utf-8")
)
PLANNING_PILOT_ADDENDUM = json.loads(
    (ROOT / "resources/planning_pilot_addendum.json").read_text(encoding="utf-8")
)
LEAKAGE_LEDGER = json.loads(
    (ROOT / "resources/leakage_ledger.json").read_text(encoding="utf-8")
)
BENCHMARK_SOURCE_DECISION = json.loads(
    (ROOT / "resources/benchmark_source_decision_2026_09_04.json").read_text(
        encoding="utf-8"
    )
)
RELEASE_LAYER_MANIFEST = json.loads(
    (ROOT / "resources/release_layer_manifest.json").read_text(encoding="utf-8")
)
TUBELEX_PROFILE = json.loads(
    (ROOT / "resources/tubelex_en_regex_ascii_2025.json").read_text(encoding="utf-8")
)
NGSL_PROFILE = json.loads(
    (ROOT / "resources/ngsl_1_2_ascii_forms.json").read_text(encoding="utf-8")
)
OEWN_FORM_PROFILE = json.loads(
    (ROOT / "resources/oewn_2025_multiword_verbs.json").read_text(encoding="utf-8")
)
VOA_MATERIAL_FRAME = json.loads(
    (ROOT / "resources/voa_gate1_frame_2017_2020.json").read_text(encoding="utf-8")
)
VOA_SOURCE_SCREEN = json.loads(
    (ROOT / "resources/voa_gate1_source_screen.json").read_text(encoding="utf-8")
)
VOA_AUTOMATED_PROFILE = json.loads(
    (ROOT / "resources/voa_gate1_automated_profile.json").read_text(encoding="utf-8")
)
VOA_RECURRENCE_TRIAGE = json.loads(
    (ROOT / "resources/voa_gate1_recurrence_triage.json").read_text(encoding="utf-8")
)
VOA_PRIORITY_REVIEW = json.loads(
    (ROOT / "resources/voa_gate1_priority_desk_review.json").read_text(encoding="utf-8")
)
VOA_DEFERRED_REVIEW = json.loads(
    (ROOT / "resources/voa_gate1_deferred_pair_desk_review.json").read_text(encoding="utf-8")
)
VOA_OUT_OF_INVENTORY_AUDIT = json.loads(
    (ROOT / "resources/voa_gate1_out_of_inventory_audit.json").read_text(encoding="utf-8")
)
SIMPLEWIKI_ROUTE2_DESIGN = json.loads(
    (ROOT / "resources/simplewiki_gate1_route2_design.json").read_text(encoding="utf-8")
)
SIMPLEWIKI_ROUTE2_CANDIDATES = json.loads(
    (ROOT / "resources/simplewiki_gate1_route2_candidates.json").read_text(encoding="utf-8")
)
SIMPLEWIKI_ROUTE2_RENDERED = json.loads(
    (ROOT / "resources/simplewiki_gate1_route2_rendered_screen.json").read_text(
        encoding="utf-8"
    )
)
SIMPLEWIKI_ROUTE2_TAKE_IN_REVIEW = json.loads(
    (ROOT / "resources/simplewiki_gate1_route2_take_in_desk_review.json").read_text(
        encoding="utf-8"
    )
)
SIMPLEWIKI_ROUTE2_PICK_UP_REVIEW = json.loads(
    (ROOT / "resources/simplewiki_gate1_route2_pick_up_desk_review.json").read_text(
        encoding="utf-8"
    )
)
SIMPLEWIKI_ROUTE2_GIVE_UP_REVIEW = json.loads(
    (ROOT / "resources/simplewiki_gate1_route2_give_up_desk_review.json").read_text(
        encoding="utf-8"
    )
)
SIMPLEWIKI_ROUTE2_CONTENT_NEUTRAL_AMENDMENT = json.loads(
    (
        ROOT
        / "resources/simplewiki_gate1_route2_content_neutral_amendment.json"
    ).read_text(encoding="utf-8")
)
TECO_CANDIDATE_MANIFEST = json.loads(
    (ROOT / "resources/teco_v1_1_candidate_manifest.json").read_text(encoding="utf-8")
)
TECO_MWE_SCREEN = json.loads(
    (ROOT / "resources/teco_v1_1_mwe_candidate_screen.json").read_text(encoding="utf-8")
)
TECO_MWE_TRIAGE = json.loads(
    (ROOT / "resources/teco_v1_1_mwe_desk_triage.json").read_text(encoding="utf-8")
)
GUTENBERG_PROSE_FRAME = json.loads(
    (ROOT / "resources/gutenberg_2026_08_30_prose_frame.json").read_text(
        encoding="utf-8"
    )
)
GUTENBERG_RIGHTS_TRIAGE = json.loads(
    (ROOT / "resources/gutenberg_2026_08_30_rights_triage_batch1.json").read_text(
        encoding="utf-8"
    )
)
GUTENBERG_NOTICE_AUDIT = json.loads(
    (ROOT / "resources/gutenberg_2026_08_30_notice_audit_batch1.json").read_text(
        encoding="utf-8"
    )
)
GUTENBERG_FRONT_MATTER_REVIEW = json.loads(
    (
        ROOT
        / "resources/gutenberg_2026_08_30_front_matter_review_batch1.json"
    ).read_text(encoding="utf-8")
)
GUTENBERG_UNIT_GATE = json.loads(
    (ROOT / "resources/gutenberg_2026_08_30_unit_gate_batch1.json").read_text(
        encoding="utf-8"
    )
)
GUTENBERG_RIGHTS_TRIAGE_BATCH2 = json.loads(
    (ROOT / "resources/gutenberg_2026_08_30_rights_triage_batch2.json").read_text(
        encoding="utf-8"
    )
)
GUTENBERG_NOTICE_AUDIT_BATCH2 = json.loads(
    (ROOT / "resources/gutenberg_2026_08_30_notice_audit_batch2.json").read_text(
        encoding="utf-8"
    )
)
GUTENBERG_FRONT_MATTER_REVIEW_BATCH2 = json.loads(
    (
        ROOT
        / "resources/gutenberg_2026_08_30_front_matter_review_batch2.json"
    ).read_text(encoding="utf-8")
)
GUTENBERG_UNIT_GATE_BATCH2 = json.loads(
    (ROOT / "resources/gutenberg_2026_08_30_unit_gate_batch2.json").read_text(
        encoding="utf-8"
    )
)
GUTENBERG_RIGHTS_TRIAGE_BATCH3 = json.loads(
    (ROOT / "resources/gutenberg_2026_08_30_rights_triage_batch3.json").read_text(
        encoding="utf-8"
    )
)
GUTENBERG_NOTICE_AUDIT_BATCH3 = json.loads(
    (ROOT / "resources/gutenberg_2026_08_30_notice_audit_batch3.json").read_text(
        encoding="utf-8"
    )
)
GUTENBERG_FRONT_MATTER_REVIEW_BATCH3 = json.loads(
    (
        ROOT
        / "resources/gutenberg_2026_08_30_front_matter_review_batch3.json"
    ).read_text(encoding="utf-8")
)
GUTENBERG_UNIT_GATE_BATCH3 = json.loads(
    (ROOT / "resources/gutenberg_2026_08_30_unit_gate_batch3.json").read_text(
        encoding="utf-8"
    )
)
GUTENBERG_RIGHTS_TRIAGE_BATCH4 = json.loads(
    (ROOT / "resources/gutenberg_2026_08_30_rights_triage_batch4.json").read_text(
        encoding="utf-8"
    )
)


class SampleManifestTests(unittest.TestCase):
    def test_github_pages_excludes_internal_material(self):
        pages_config = json.loads((ROOT / "_config.yml").read_text(encoding="utf-8"))
        for directory in ("internal", "research_data"):
            self.assertIn(directory, pages_config["exclude"])
            subprocess.run(
                ["git", "check-ignore", "--no-index", "-q", f"{directory}/boundary-probe.json"],
                cwd=ROOT, check=True,
            )
        self.assertEqual(
            pages_config["exclude"], RELEASE_LAYER_MANIFEST["site_delivery"]["excluded_paths"]
        )
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "app.mjs").read_text(encoding="utf-8")
        self.assertNotIn("internal/", index)
        self.assertNotRegex(index, r"\bIR-\d{3}\b")
        self.assertNotIn("現prototype", index)
        self.assertNotRegex(app, r"\bIR-\d{3}\b")
        self.assertIn("out_of_inventory: ['None of the listed senses fits'", app)

    def test_release_manifest_covers_every_public_file_without_unknown_rights(self):
        manifest = RELEASE_LAYER_MANIFEST
        public_files = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.rstrip("\0").split("\0")
        paths = sorted(set(public_files))
        self.assertEqual(len(paths), len(public_files))
        self.assertEqual(
            hashlib.sha256(("\0".join(paths) + "\0").encode("utf-8")).hexdigest(),
            manifest["coverage"]["public_paths_sha256_at_freeze"],
            "Public paths changed: review additions/removals before updating the release manifest.",
        )
        self.assertEqual(len(public_files), manifest["coverage"]["public_file_count_at_freeze"])
        self.assertEqual(manifest["coverage"]["rights_unknown_public_files"], 0)
        for path in public_files:
            self.assertFalse(
                path.startswith(("internal/", "research_data/")),
                f"Private working material must not enter the public repository: {path}",
            )
            rule = next(
                rule
                for rule in manifest["path_rules"]
                if any(fnmatch.fnmatchcase(path, pattern) for pattern in rule["patterns"])
            )
            for field in ("source", "license", "notice", "redistribution_state"):
                self.assertTrue(rule[field], (path, field))
            self.assertNotIn("unknown", rule["license"].lower(), path)
            self.assertNotIn("unknown", rule["redistribution_state"].lower(), path)
        for layer in manifest["benchmark_release_layers"]:
            for field in ("source", "license", "notice", "redistribution_state"):
                self.assertTrue(layer[field], (layer["layer"], field))

    def test_benchmark_source_decision_is_target_blind_and_releasable(self):
        decision = BENCHMARK_SOURCE_DECISION
        self.assertEqual(decision["status"], "accepted_protocol_no_source_acquired")
        self.assertFalse(decision["current_boundary"]["source_text_acquired"])
        source = decision["selected_source"]
        self.assertIn("namespace-0", source["population"])
        self.assertNotIn("/latest/", source["acquisition"]["required_artifact"])
        self.assertEqual(source["rights_basis"]["license"], "CC BY-SA 4.0")
        audits = decision["candidate_audit"]
        self.assertEqual(
            {audit["candidate"]: audit["decision"] for audit in audits},
            {
                "English Wikipedia dated namespace-0 article revisions": "selected",
                "STREUSLE 5.0": "rejected_as_new_core",
                "Project Gutenberg fixed-prefix prose frame": "rejected",
            },
        )
        routes = {route["route"]: route["decision"] for route in decision["release_route_comparison"]}
        self.assertEqual(routes["public_text"], "primary")
        self.assertNotEqual(routes["standoff_only"], "primary")
        self.assertNotEqual(routes["reconstruction_only"], "primary")
        self.assertLess(
            decision["target_blind_order"].index(
                "freeze content-neutral eligibility, strata, seed, and sampling under IR-121"
            ),
            decision["target_blind_order"].index(
                "only then begin candidate-independent annotation"
            ),
        )

    def test_predata_documents_separate_populations_and_keep_unknowns(self):
        card = (ROOT / "BENCHMARK_CARD.md").read_text(encoding="utf-8").casefold()
        statement = (ROOT / "DATA_STATEMENT.md").read_text(encoding="utf-8").casefold()
        pointer = (ROOT / "resources/benchmark_card_draft.md").read_text(encoding="utf-8")
        self.assertIn("../BENCHMARK_CARD.md", pointer)
        for population in (
            "source population",
            "sampling population",
            "annotation population",
            "target population",
            "evaluation population",
        ):
            self.assertIn(population, card)
            self.assertIn(population, statement)
        for category in ("vpc.full", "vpc.semi", "vid"):
            self.assertIn(category, card)
            self.assertIn(category, statement)
        self.assertIn("unknown before release", card)
        self.assertIn("unknown before release", statement)
        self.assertIn("not collected", card)
        self.assertIn("not collected", statement)

    def test_target_population_is_candidate_independent_and_scope_bounded(self):
        population = TARGET_POPULATION
        self.assertEqual(
            population["project_scope"]["categories"],
            ["VPC.full", "VPC.semi", "VID"],
        )
        discovery = population["candidate_independent_discovery"]
        for forbidden_input in ("target list", "dictionary", "model", "outcome"):
            self.assertIn(forbidden_input, discovery["first_pass"])
        self.assertIn("every sentence", discovery["document_completion"])
        rules = population["form_and_span_rules"]
        for rule in (
            "canonical_form",
            "inflection",
            "particle_separation",
            "pronoun_insertion",
            "overlap",
            "literal_use",
            "ambiguity",
        ):
            self.assertTrue(rules[rule])
        excluded = {item["class"] for item in population["out_of_scope"]}
        self.assertIn("non_verbal_idioms", excluded)
        self.assertIn("misspellings_and_nonstandard_forms", excluded)
        mapping = population["taxonomy"]["mapping"]
        self.assertEqual(
            {item["streusle_label"]: item["project_label"] for item in mapping},
            {
                "V.VPC.full": "VPC.full",
                "V.VPC.semi": "VPC.semi",
                "V.VID": "VID",
            },
        )
        for dependency in population["dependencies"].values():
            path = ROOT / dependency["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), dependency["sha256"])

    def test_evaluation_strata_never_treat_occurrences_as_independent(self):
        protocol = EVALUATION_STRATA
        self.assertEqual(
            protocol["status"],
            "predata_strata_and_cluster_contract_no_labels_no_estimates",
        )
        self.assertEqual(
            set(protocol["prespecified_strata"]),
            {
                "category",
                "continuity",
                "form_exposure",
                "variant",
                "source_genre",
                "sampling_length",
            },
        )
        dependence = protocol["units_and_dependence"]
        self.assertEqual(dependence["primary_cluster"]["id"], "document_id")
        self.assertEqual(
            dependence["secondary_cluster"]["id"], "canonical_type_id"
        )
        self.assertIn("Do not treat occurrences", dependence["prohibitions"][0])
        self.assertTrue(protocol["claim_denominators"])
        for claim in protocol["claim_denominators"]:
            self.assertTrue(claim["denominator"])
            self.assertEqual(claim["primary_cluster"], "document_id")
            self.assertEqual(claim["secondary_cluster"], "canonical_type_id")
        self.assertIn(
            "descriptive-only",
            protocol["small_stratum_rule"]["current_state"],
        )
        self.assertIn(
            "1/pi_h",
            protocol["aggregation_and_weighting"]["overall_population_estimate"],
        )
        for dependency in protocol["dependencies"].values():
            path = ROOT / dependency["path"]
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                dependency["sha256"],
            )

    def test_split_protocol_is_document_disjoint_and_unmaterialized(self):
        protocol = SPLIT_PROTOCOL
        self.assertEqual(
            protocol["status"], "assignment_protocol_frozen_no_rows_no_custodian"
        )
        shares = {item["id"]: item["share"] for item in protocol["partitions"]}
        self.assertEqual(
            shares,
            {
                "guide_training": 0.2,
                "annotation_pilot": 0.1,
                "development": 0.2,
                "sealed_test": 0.5,
            },
        )
        self.assertAlmostEqual(sum(shares.values()), 1.0)
        self.assertTrue(protocol["assignment"]["seed"])
        self.assertIn("target", " ".join(protocol["assignment"]["fail_closed_conditions"]))
        self.assertTrue(protocol["custody"]["required"])
        self.assertEqual(protocol["custody"]["status"], "unassigned")
        self.assertEqual(
            protocol["form_disjoint_policy"]["strong_whole_test_unseen_form_claim"],
            "not_authorized",
        )
        self.assertEqual(protocol["current_boundary"]["assigned_documents"], 0)
        self.assertEqual(protocol["current_boundary"]["sealed_test_labels"], 0)
        for dependency in protocol["dependencies"].values():
            path = ROOT / dependency["path"]
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(), dependency["sha256"]
            )

    def test_planning_pilot_is_target_blind_exposed_and_unmaterialized(self):
        addendum = PLANNING_PILOT_ADDENDUM
        self.assertEqual(
            addendum["status"],
            "accepted_protocol_no_pilot_rows_no_human_work_authorized",
        )
        training = addendum["two_pilot_separation"]["training_only_pilot"]
        planning = addendum["two_pilot_separation"]["representative_planning_pilot"]
        self.assertIn("Do not use its target prevalence", training["prohibited_use"])
        self.assertIn("target-blind probability-sampled", planning["material_rule"])
        self.assertEqual(addendum["planning_prefix"]["minimum_documents_per_length"], 6)
        self.assertIn("Do not stop early", addendum["planning_prefix"]["stopping_rule"])
        self.assertEqual(
            addendum["required_allocation_record"]["selected_document_count"], 0
        )
        self.assertEqual(addendum["required_allocation_record"]["target_search_count"], 0)
        for dependency in addendum["dependencies"].values():
            path = ROOT / dependency["path"]
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(), dependency["sha256"]
            )

    def test_leakage_ledger_classifies_known_exposures_and_fails_unknown(self):
        ledger = LEAKAGE_LEDGER
        self.assertEqual(
            ledger["status"],
            "current_repository_exposure_audit_complete_ongoing_append_required_no_project_test",
        )
        self.assertFalse(ledger["project_sealed_test"]["exists"])
        self.assertEqual(ledger["policy"]["unknown_rule"], "Unknown exposure is classified as exposed.")
        required = set(ledger["policy"]["minimum_fields"])
        self.assertGreaterEqual(len(ledger["records"]), 10)
        self.assertEqual(
            hashlib.sha256(json.dumps(ledger["records"][:10], ensure_ascii=False, separators=(",", ":")).encode()).hexdigest(),
            "d6460e59cb7701ab4f3bb0af4a068121d6788a77d484c25ee7252ec138adffe9",
        )
        ids = [record["id"] for record in ledger["records"]]
        self.assertEqual(len(ids), len(set(ids)))
        for record in ledger["records"]:
            self.assertEqual(set(record), required)
            if record["supersedes_id"] is not None:
                self.assertIn(record["supersedes_id"], ids[: ids.index(record["id"])])
        by_id = {record["id"]: record for record in ledger["records"]}
        self.assertEqual(
            by_id["EXP-2026-09-01-001"]["extent"]["source_test_target_occurrences"],
            40,
        )
        self.assertEqual(
            by_id["EXP-2026-09-03-002"]["extent"]["source_test_rows"], 17
        )
        self.assertEqual(
            by_id["EXP-2026-09-03-003"]["exposure_class"],
            "dictionary_and_inventory_candidate_exposed",
        )
        self.assertEqual(
            by_id["EXP-2026-09-02-004"]["extent"]["passages_admitted"], 0
        )
        extension = by_id["EXP-2026-09-05-011"]
        self.assertEqual(extension["supersedes_id"], "EXP-2026-09-02-004")
        self.assertEqual(extension["extent"]["verified_cached_revisions"], 507)
        self.assertEqual(extension["extent"]["canonical_forms"], ["pick up", "come out", "make sure"])
        self.assertEqual(extension["extent"]["maximum_selected_pages_per_form"], 20)
        self.assertEqual(extension["extent"]["maximum_selected_targets"], 60)
        self.assertEqual(extension["extent"]["new_benchmark_passages_admitted"], 0)
        self.assertEqual(extension["extent"]["independent_labels_created"], 0)
        self.assertIn("excluded from the project sealed test", extension["disposition"])
        decision = next(row for row in DECISION_LOG["records"] if row["id"] == "DEC-2026-09-05-020")
        self.assertEqual((decision["status"], decision["domain"]), ("accepted", "source"))
        self.assertEqual(
            by_id["EXP-2026-09-02-006"]["extent"][
                "participant_outcome_values_used_for_selection_or_labels"
            ],
            0,
        )
        self.assertEqual(
            by_id["EXP-2026-09-03-007"]["extent"][
                "known_incidental_target_exposure_text_ids"
            ],
            [15188, 23763, 63142, 36833],
        )
        for record in ledger["records"]:
            for evidence in record["evidence"]:
                self.assertTrue((ROOT / evidence).exists(), evidence)
        self.assertEqual(ledger["audit_coverage"]["unclassified_known_groups"], [])
        self.assertEqual(
            ledger["final_item_exposure_schema"]["records"], []
        )
        self.assertIn(
            "exposed_unknown",
            ledger["final_item_exposure_schema"]["allowed_states"],
        )
        self.assertEqual(
            ledger["model_experiment_register"][
                "contextual_or_probabilistic_model_experiments_run"
            ],
            0,
        )
        self.assertEqual(ledger["model_experiment_register"]["records"], [])

    def test_decision_log_is_append_only_and_exposure_safe(self):
        decision_log = DECISION_LOG
        policy = decision_log["policy"]
        records = decision_log["records"]
        ids = [record["id"] for record in records]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("cannot be applied retroactively", policy["sealed_test_rule"])
        self.assertIn("only rationale is improving a score", policy["score_only_rule"])
        allowed_fields = set(policy["required_fields"] + policy["optional_fields"])
        for record in records:
            self.assertTrue(set(policy["required_fields"]).issubset(record))
            self.assertTrue(set(record).issubset(allowed_fields))
            self.assertIn(record["status"], policy["allowed_statuses"])
            self.assertIn(record["domain"], policy["controlled_domains"])
            self.assertIsInstance(record["reevaluation_required"], bool)
            self.assertTrue(record["affected_tasks"])
            self.assertTrue(record["affected_artifacts"])
            self.assertTrue(record["version_change"])
            self.assertTrue(record["sealed_test_effect"])
            for superseded_id in record.get("supersedes", []):
                self.assertIn(superseded_id, ids[: ids.index(record["id"])])

    def test_first_paper_has_no_downstream_data_dependency(self):
        decision = next(
            record for record in DECISION_LOG["records"]
            if record["id"] == "DEC-2026-09-04-009"
        )
        self.assertEqual(decision["status"], "accepted")
        self.assertIn("No downstream application is selected", decision["after"])
        self.assertIn("No downstream application is selected", DOWNSTREAM_SELECTION_MEMO)
        self.assertIn("not a core-development gate", DOWNSTREAM_SELECTION_MEMO)
        self.assertIn("No eye-movement corpus", DOWNSTREAM_SELECTION_MEMO)

    def test_human_work_routes_are_separated_and_publication_is_safe(self):
        decision = next(
            record for record in DECISION_LOG["records"]
            if record["id"] == "DEC-2026-09-04-010"
        )
        correction = next(
            record for record in DECISION_LOG["records"]
            if record["id"] == "DEC-2026-09-05-014"
        )
        self.assertEqual(decision["status"], "accepted")
        self.assertEqual(correction["status"], "accepted")
        self.assertEqual(
            correction["supersedes"],
            ["DEC-2026-09-04-010", "DEC-2026-09-05-013"],
        )
        self.assertIn("written determination or approval", decision["after"])
        self.assertIn(
            "IR-115 therefore is not a present P0 blocker",
            ETHICS_DETERMINATION,
        )
        for required_control in (
            "Conditional preliminary-checklist map",
            "Do not submit an ethics application merely",
            "Raw platform exports remain restricted",
            "Data Availability Statement",
        ):
            self.assertIn(required_control, ETHICS_DETERMINATION)
        self.assertIn("Static development, public-source preparation", GOVERNANCE)
        self.assertIn(
            "does not by itself\nestablish that the activity is a human-participant study",
            GOVERNANCE,
        )
        for prohibited_destination in ("Git", "GitHub Pages", "an API response"):
            self.assertIn(prohibited_destination, GOVERNANCE)

    def test_claim_evidence_map_has_bounded_single_category_claims(self):
        claim_map = CLAIM_EVIDENCE_MAP
        categories = set(claim_map["categories"])
        self.assertEqual(
            categories,
            {"construct", "resource", "technical", "response_process", "downstream"},
        )
        claims = claim_map["claims"]
        ids = [claim["id"] for claim in claims]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(claim_map["current_ceiling"]["level"], "demonstration")
        for claim in claims:
            self.assertIn(claim["category"], categories)
            for field in (
                "claim",
                "permitted_wording",
                "current_evidence",
                "required_evidence",
                "release_artifacts",
                "prohibited_inferences",
            ):
                self.assertTrue(claim[field], (claim["id"], field))
            for evidence in claim["current_evidence"]:
                self.assertTrue((ROOT / evidence["path"]).exists(), evidence["path"])
                self.assertTrue(evidence["supports"])
            for artifact in claim["release_artifacts"]:
                self.assertIn(artifact["state"], {"available", "planned"})
                if artifact["state"] == "available":
                    self.assertTrue((ROOT / artifact["path"]).exists(), artifact["path"])

    def test_hybrid_sense_contract_separates_ids_misses_and_contextual_states(self):
        contract = HYBRID_SENSE_CONTRACT
        self.assertEqual(contract["contract_version"], "2.0.0")
        self.assertEqual(
            contract["status"], "frozen_pre_annotation_design_no_inventory_entries"
        )
        self.assertEqual(
            contract["bounded_non_exact_mapping"]["population"][
                "residual_type_count"
            ],
            KAIKKI_VID_AUDIT["summary"]["exact_kaikki_coverage"][
                "types_without_exact_verb_entry"
            ],
        )
        self.assertEqual(
            [
                item["stage"]
                for item in contract["bounded_non_exact_mapping"][
                    "completed_prefilter"
                ]
            ],
            [1, 2, 3],
        )
        self.assertEqual(
            [
                item["stage"]
                for item in contract["bounded_non_exact_mapping"][
                    "remaining_ordered_stages"
                ]
            ],
            [4, 5, 6],
        )
        self.assertIn(
            "free Web or dictionary search after the bounded sources are exhausted",
            contract["bounded_non_exact_mapping"]["prohibited_operations"],
        )
        self.assertIn(
            "never primary keys",
            contract["project_identity"]["rules"][1],
        )
        type_fields = contract["record_contract"]["type_required_fields"]
        self.assertIn("observed_vmwe_categories", type_fields)
        self.assertNotIn("vmwe_category", type_fields)
        allowed = contract["record_contract"]["allowed_values"]
        self.assertIn("hybrid", allowed["type_inventory_status"])
        self.assertIn("partly_verified", allowed["source_route_status"])
        assignment = contract["contextual_assignment"]
        self.assertEqual(
            set(assignment["allowed_statuses"]),
            {
                "assigned", "multiple_assigned", "ambiguous", "abstained",
                "unassigned", "out_of_inventory", "inventory_ineligible",
            },
        )
        self.assertIn("never licenses", assignment["rules"]["out_of_inventory"])
        self.assertIn("different questions", assignment["separation_rule"])
        self.assertEqual(
            contract["rights_and_release"]["current_release_state"],
            "contract_only_no_lexical_entries_or_source_wording",
        )
        self.assertEqual(
            hashlib.sha256(HYBRID_SENSE_CONTRACT_PATH.read_bytes()).hexdigest(),
            LRE_READINESS["candidate_inventory_review_sources"][
                "hybrid_contract_sha256"
            ],
        )

    def test_gutenberg_final_rights_prefix_proves_frame_futility(self):
        triage = GUTENBERG_RIGHTS_TRIAGE_BATCH4
        frame_path = ROOT / "resources/gutenberg_2026_08_30_prose_frame.json"
        prior_path = ROOT / "resources/gutenberg_2026_08_30_unit_gate_batch3.json"
        self.assertEqual(
            triage["input"]["frame_sha256"],
            hashlib.sha256(frame_path.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            triage["input"]["prior_unit_gate_sha256"],
            hashlib.sha256(prior_path.read_bytes()).hexdigest(),
        )
        frame_columns = GUTENBERG_PROSE_FRAME["queue_columns"]
        frame_rows = [
            dict(zip(frame_columns, row)) for row in GUTENBERG_PROSE_FRAME["queue"]
        ]
        columns = triage["screen_columns"]
        screens = [dict(zip(columns, row)) for row in triage["screens"]]
        for stratum in ("adult_or_unspecified", "juvenile"):
            self.assertEqual(
                [
                    (row["queue_rank"], row["text_id"])
                    for row in screens
                    if row["stratum"] == stratum
                ],
                [
                    (row["queue_rank"], row["text_id"])
                    for row in frame_rows
                    if row["stratum"] == stratum
                    and 31 <= row["queue_rank"] <= 40
                ],
            )
        self.assertEqual(
            Counter(row["decision"] for row in screens),
            Counter(
                {
                    "notice_check_allowed": 13,
                    "hold_term_likely_active": 5,
                    "hold_identity_or_death_unverified": 2,
                }
            ),
        )
        self.assertEqual(
            {
                row["text_id"]
                for row in screens
                if row["decision"] == "hold_term_likely_active"
            },
            {79336, 19651, 73324, 74227, 75909},
        )
        self.assertEqual(
            {
                row["text_id"]
                for row in screens
                if row["decision"] == "hold_identity_or_death_unverified"
            },
            {43344, 57827},
        )
        self.assertEqual(
            triage["method"]["incidental_search_exposure"][
                "target_forms_incidentally_exposed"
            ]["text_ids"],
            [15188, 23763],
        )
        for stratum in ("adult_or_unspecified", "juvenile"):
            allowed = sum(
                row["decision"] == "notice_check_allowed"
                for row in screens
                if row["stratum"] == stratum
            )
            self.assertEqual(triage["summary"]["allowed_by_stratum"][stratum], allowed)
            self.assertEqual(
                triage["summary"][
                    "maximum_possible_passes_if_every_allowed_file_passes"
                ][stratum],
                triage["summary"]["prior_mechanical_passes_by_stratum"][stratum]
                + allowed,
            )
        self.assertLess(
            triage["summary"][
                "maximum_possible_passes_if_every_allowed_file_passes"
            ]["adult_or_unspecified"],
            10,
        )
        self.assertFalse(triage["summary"]["frame_success_still_possible"])
        self.assertEqual(triage["input"]["ebook_files_acquired"], 0)
        self.assertEqual(triage["input"]["target_form_searches_run"], 0)
        self.assertEqual(triage["input"]["mwe_searches_run"], 0)
        self.assertEqual(triage["summary"]["admitted_units"], 0)

    def test_gutenberg_third_unit_gate_is_target_blind_and_complete(self):
        gate = GUTENBERG_UNIT_GATE_BATCH3
        front_path = (
            ROOT / "resources/gutenberg_2026_08_30_front_matter_review_batch3.json"
        )
        self.assertEqual(
            gate["inputs"]["front_matter_review_sha256"],
            hashlib.sha256(front_path.read_bytes()).hexdigest(),
        )
        front_columns = GUTENBERG_FRONT_MATTER_REVIEW_BATCH3["record_columns"]
        ready = [
            dict(zip(front_columns, row))
            for row in GUTENBERG_FRONT_MATTER_REVIEW_BATCH3["records"]
            if dict(zip(front_columns, row))["decision"]
            == "ready_for_version_conditioned_unit_gate"
        ]
        columns = gate["record_columns"]
        records = [dict(zip(columns, row)) for row in gate["records"]]
        self.assertEqual(
            [row["text_id"] for row in records],
            [row["text_id"] for row in ready],
        )
        self.assertTrue(
            all(
                record["file_sha256"] == source["file_sha256"]
                and record["raw_unit_lines_inclusive"][0]
                == source["first_unit_heading_line"]
                for record, source in zip(records, ready)
            )
        )
        record_by_id = {row["text_id"]: row for row in records}
        self.assertEqual(record_by_id[44045]["raw_unit_lines_inclusive"], [87, 387])
        self.assertEqual(
            {
                row["text_id"]
                for row in records
                if row["gate_decision"]
                == "passed_mechanical_unit_gate_release_pending"
            },
            {13530, 27996, 36396, 72094, 36833, 21326, 23683},
        )
        passed = [
            row
            for row in records
            if row["gate_decision"]
            == "passed_mechanical_unit_gate_release_pending"
        ]
        self.assertEqual(
            Counter(row["stratum"] for row in passed),
            Counter({"adult_or_unspecified": 2, "juvenile": 5}),
        )
        self.assertEqual(gate["summary"]["excluded_first_unit_over_maximum"], 5)
        self.assertEqual(gate["summary"]["excluded_ambiguous_first_unit_type"], 3)
        self.assertEqual(gate["inputs"]["front_matter_holds_excluded"], 0)
        self.assertEqual(gate["summary"]["admitted_units"], 0)
        self.assertEqual(gate["summary"]["target_or_mwe_searches_run"], 0)
        self.assertIn("ranks 31–40", gate["next_action"])
        self.assertFalse(
            gate["structural_review_exposure"][
                "target_forms_senses_or_mwes_inspected"
            ]
        )
        self.assertFalse(gate["inputs"]["source_files_bundled"])
        self.assertFalse(gate["inputs"]["unit_text_bundled"])

    def test_gutenberg_third_front_matter_review_preserves_first_units(self):
        review = GUTENBERG_FRONT_MATTER_REVIEW_BATCH3
        notice_path = (
            ROOT / "resources/gutenberg_2026_08_30_notice_audit_batch3.json"
        )
        self.assertEqual(
            review["inputs"]["notice_audit_sha256"],
            hashlib.sha256(notice_path.read_bytes()).hexdigest(),
        )
        self.assertFalse(review["inputs"]["source_files_bundled"])
        columns = review["record_columns"]
        records = [dict(zip(columns, row)) for row in review["records"]]
        self.assertEqual(
            [row["text_id"] for row in records],
            [row["text_id"] for row in GUTENBERG_NOTICE_AUDIT_BATCH3["files"]],
        )
        notice_hashes = {
            row["text_id"]: row["sha256"]
            for row in GUTENBERG_NOTICE_AUDIT_BATCH3["files"]
        }
        self.assertTrue(
            all(
                row["file_sha256"] == notice_hashes[row["text_id"]]
                and row["reviewed_front_matter_lines_inclusive"][0]
                <= row["reviewed_front_matter_lines_inclusive"][1]
                < row["first_unit_heading_line"]
                and len(row["front_matter_sha256"]) == 64
                for row in records
            )
        )
        self.assertEqual(
            Counter(row["decision"] for row in records),
            Counter({"ready_for_version_conditioned_unit_gate": 15}),
        )
        self.assertEqual(
            review["boundary_location_exposure"]
            ["incidental_target_string_exposure"]["by_text_id"],
            {"63142": ["give up"], "36833": ["take in"]},
        )
        self.assertEqual(
            review["summary"]["complete_print_publication_statement"], 9
        )
        self.assertEqual(
            review["summary"]["incomplete_print_publication_statement"], 6
        )
        self.assertEqual(
            review["summary"]["additional_retained_textual_contributors"], 1
        )
        self.assertEqual(review["summary"]["explicit_transcriber_notes"], 3)
        self.assertEqual(
            review["summary"]["source_authored_preface_or_introduction_first"],
            3,
        )
        self.assertEqual(review["summary"]["admitted_units"], 0)
        self.assertEqual(review["summary"]["mwe_searches_run"], 0)
        self.assertFalse(
            review["boundary_location_exposure"]["mwe_or_lexical_search_run"]
        )

    def test_gutenberg_third_notice_audit_pins_the_allowed_files(self):
        audit = GUTENBERG_NOTICE_AUDIT_BATCH3
        self.assertEqual(
            audit["inputs"]["rights_triage_sha256"],
            hashlib.sha256(
                (
                    ROOT
                    / "resources/gutenberg_2026_08_30_rights_triage_batch3.json"
                ).read_bytes()
            ).hexdigest(),
        )
        columns = GUTENBERG_RIGHTS_TRIAGE_BATCH3["screen_columns"]
        expected = [
            row["text_id"]
            for row in (
                dict(zip(columns, item))
                for item in GUTENBERG_RIGHTS_TRIAGE_BATCH3["screens"]
            )
            if row["decision"] == "notice_check_allowed"
        ]
        self.assertEqual([row["text_id"] for row in audit["files"]], expected)
        self.assertTrue(
            all(
                row["checks"]["start_and_end_markers_present"]
                and row["checks"]["us_notice_and_non_us_warning_present"]
                and row["checks"]["full_project_gutenberg_license_footer_present"]
                for row in audit["files"]
            )
        )
        self.assertEqual(audit["summary"]["files"], 15)
        self.assertEqual(audit["summary"]["original_publication_missing"], 14)
        self.assertEqual(audit["summary"]["credits_missing"], 0)
        self.assertFalse(audit["scope"]["body_prose_reviewed"])
        self.assertEqual(audit["scope"]["units_selected"], 0)
        self.assertEqual(audit["scope"]["mwe_searches_run"], 0)
        self.assertFalse(audit["scope"]["public_web_distribution_authorized"])

    def test_gutenberg_third_rights_triage_is_fixed_and_exposure_aware(self):
        triage = GUTENBERG_RIGHTS_TRIAGE_BATCH3
        frame_path = ROOT / "resources/gutenberg_2026_08_30_prose_frame.json"
        self.assertEqual(
            triage["input"]["frame_id"], GUTENBERG_PROSE_FRAME["frame_id"]
        )
        self.assertEqual(
            triage["input"]["frame_sha256"],
            hashlib.sha256(frame_path.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            triage["input"]["prior_unit_gate_sha256"],
            hashlib.sha256(
                (
                    ROOT / "resources/gutenberg_2026_08_30_unit_gate_batch2.json"
                ).read_bytes()
            ).hexdigest(),
        )
        frame_columns = GUTENBERG_PROSE_FRAME["queue_columns"]
        frame_rows = [
            dict(zip(frame_columns, row)) for row in GUTENBERG_PROSE_FRAME["queue"]
        ]
        columns = triage["screen_columns"]
        screens = [dict(zip(columns, row)) for row in triage["screens"]]
        for stratum in ("adult_or_unspecified", "juvenile"):
            self.assertEqual(
                [
                    (row["queue_rank"], row["text_id"])
                    for row in screens
                    if row["stratum"] == stratum
                ],
                [
                    (row["queue_rank"], row["text_id"])
                    for row in frame_rows
                    if row["stratum"] == stratum
                    and 21 <= row["queue_rank"] <= 30
                ],
            )
        self.assertEqual(
            Counter(row["decision"] for row in screens),
            Counter(
                {
                    "notice_check_allowed": 15,
                    "hold_term_likely_active": 3,
                    "hold_identity_or_death_unverified": 2,
                }
            ),
        )
        self.assertEqual(
            {
                row["text_id"]
                for row in screens
                if row["decision"] == "hold_term_likely_active"
            },
            {64755, 32413, 22816},
        )
        self.assertEqual(
            {
                row["text_id"]
                for row in screens
                if row["decision"] == "hold_identity_or_death_unverified"
            },
            {35045, 17059},
        )
        self.assertEqual(
            triage["method"]["incidental_search_exposure"][
                "target_form_incidentally_exposed"
            ]["text_ids"],
            [36833],
        )
        self.assertEqual(triage["input"]["ebook_files_acquired"], 0)
        self.assertEqual(triage["input"]["target_form_searches_run"], 0)
        self.assertEqual(triage["input"]["mwe_searches_run"], 0)
        self.assertEqual(triage["summary"]["admitted_units"], 0)

    def test_gutenberg_second_unit_gate_is_target_blind_and_complete(self):
        gate = GUTENBERG_UNIT_GATE_BATCH2
        front_path = (
            ROOT / "resources/gutenberg_2026_08_30_front_matter_review_batch2.json"
        )
        self.assertEqual(
            gate["inputs"]["front_matter_review_sha256"],
            hashlib.sha256(front_path.read_bytes()).hexdigest(),
        )
        front_columns = GUTENBERG_FRONT_MATTER_REVIEW_BATCH2["record_columns"]
        ready = [
            dict(zip(front_columns, row))
            for row in GUTENBERG_FRONT_MATTER_REVIEW_BATCH2["records"]
            if dict(zip(front_columns, row))["decision"]
            == "ready_for_version_conditioned_unit_gate"
        ]
        columns = gate["record_columns"]
        records = [dict(zip(columns, row)) for row in gate["records"]]
        self.assertEqual(
            [row["text_id"] for row in records],
            [row["text_id"] for row in ready],
        )
        self.assertTrue(
            all(
                record["file_sha256"] == source["file_sha256"]
                and record["raw_unit_lines_inclusive"][0]
                == source["first_unit_heading_line"]
                for record, source in zip(records, ready)
            )
        )
        record_by_id = {row["text_id"]: row for row in records}
        self.assertEqual(record_by_id[68552]["raw_unit_lines_inclusive"], [38, 1067])
        self.assertEqual(
            {
                row["text_id"]
                for row in records
                if row["gate_decision"]
                == "passed_mechanical_unit_gate_release_pending"
            },
            {70572},
        )
        self.assertEqual(gate["summary"]["excluded_first_unit_over_maximum"], 9)
        self.assertEqual(gate["summary"]["excluded_ambiguous_first_unit_type"], 6)
        self.assertEqual(gate["inputs"]["front_matter_holds_excluded"], 1)
        self.assertEqual(gate["summary"]["admitted_units"], 0)
        self.assertEqual(gate["summary"]["target_or_mwe_searches_run"], 0)
        self.assertFalse(
            gate["structural_review_exposure"][
                "target_forms_senses_or_mwes_inspected"
            ]
        )
        self.assertFalse(gate["inputs"]["source_files_bundled"])
        self.assertFalse(gate["inputs"]["unit_text_bundled"])

    def test_gutenberg_second_front_matter_review_preserves_first_units(self):
        review = GUTENBERG_FRONT_MATTER_REVIEW_BATCH2
        notice_path = (
            ROOT / "resources/gutenberg_2026_08_30_notice_audit_batch2.json"
        )
        self.assertEqual(
            review["inputs"]["notice_audit_sha256"],
            hashlib.sha256(notice_path.read_bytes()).hexdigest(),
        )
        self.assertFalse(review["inputs"]["source_files_bundled"])
        columns = review["record_columns"]
        records = [dict(zip(columns, row)) for row in review["records"]]
        self.assertEqual(
            [row["text_id"] for row in records],
            [row["text_id"] for row in GUTENBERG_NOTICE_AUDIT_BATCH2["files"]],
        )
        notice_hashes = {
            row["text_id"]: row["sha256"]
            for row in GUTENBERG_NOTICE_AUDIT_BATCH2["files"]
        }
        self.assertTrue(
            all(
                row["file_sha256"] == notice_hashes[row["text_id"]]
                and row["reviewed_front_matter_lines_inclusive"][0]
                <= row["reviewed_front_matter_lines_inclusive"][1]
                < row["first_unit_heading_line"]
                and len(row["front_matter_sha256"]) == 64
                for row in records
            )
        )
        self.assertEqual(
            Counter(row["decision"] for row in records),
            Counter(
                {
                    "ready_for_version_conditioned_unit_gate": 16,
                    "hold_underlying_adaptation_provenance_review": 1,
                }
            ),
        )
        self.assertEqual(
            {
                row["text_id"]
                for row in records
                if row["decision"]
                == "hold_underlying_adaptation_provenance_review"
            },
            {6655},
        )
        self.assertEqual(
            set(review["boundary_location_exposure"]["text_ids"]),
            {row["text_id"] for row in records},
        )
        self.assertEqual(review["summary"]["explicit_transcriber_notes"], 6)
        self.assertEqual(
            review["summary"]["source_authored_preface_or_introduction_first"],
            5,
        )
        self.assertEqual(review["summary"]["admitted_units"], 0)
        self.assertEqual(review["summary"]["mwe_searches_run"], 0)
        self.assertFalse(
            review["boundary_location_exposure"]["mwe_or_lexical_search_run"]
        )

    def test_gutenberg_second_notice_audit_pins_the_allowed_files(self):
        audit = GUTENBERG_NOTICE_AUDIT_BATCH2
        self.assertEqual(
            audit["inputs"]["rights_triage_sha256"],
            hashlib.sha256(
                (
                    ROOT
                    / "resources/gutenberg_2026_08_30_rights_triage_batch2.json"
                ).read_bytes()
            ).hexdigest(),
        )
        columns = GUTENBERG_RIGHTS_TRIAGE_BATCH2["screen_columns"]
        expected = [
            row["text_id"]
            for row in (
                dict(zip(columns, item))
                for item in GUTENBERG_RIGHTS_TRIAGE_BATCH2["screens"]
            )
            if row["decision"] == "notice_check_allowed"
        ]
        self.assertEqual([row["text_id"] for row in audit["files"]], expected)
        self.assertTrue(
            all(
                row["checks"]["start_and_end_markers_present"]
                and row["checks"]["us_notice_and_non_us_warning_present"]
                and row["checks"]["full_project_gutenberg_license_footer_present"]
                for row in audit["files"]
            )
        )
        self.assertEqual(audit["summary"]["files"], 17)
        self.assertEqual(audit["summary"]["original_publication_missing"], 14)
        self.assertEqual(audit["summary"]["credits_missing"], 0)
        self.assertFalse(audit["scope"]["body_prose_reviewed"])
        self.assertEqual(audit["scope"]["units_selected"], 0)
        self.assertEqual(audit["scope"]["mwe_searches_run"], 0)
        self.assertFalse(audit["scope"]["public_web_distribution_authorized"])

    def test_gutenberg_second_rights_triage_is_the_next_fixed_prefix(self):
        triage = GUTENBERG_RIGHTS_TRIAGE_BATCH2
        self.assertEqual(
            triage["input"]["prior_unit_gate_sha256"],
            hashlib.sha256(
                (
                    ROOT / "resources/gutenberg_2026_08_30_unit_gate_batch1.json"
                ).read_bytes()
            ).hexdigest(),
        )
        frame_columns = GUTENBERG_PROSE_FRAME["queue_columns"]
        frame_rows = [
            dict(zip(frame_columns, row)) for row in GUTENBERG_PROSE_FRAME["queue"]
        ]
        columns = triage["screen_columns"]
        screens = [dict(zip(columns, row)) for row in triage["screens"]]
        self.assertEqual(len(screens), 20)
        for stratum in ("adult_or_unspecified", "juvenile"):
            self.assertEqual(
                [
                    (row["queue_rank"], row["text_id"])
                    for row in screens
                    if row["stratum"] == stratum
                ],
                [
                    (row["queue_rank"], row["text_id"])
                    for row in frame_rows
                    if row["stratum"] == stratum
                    and 11 <= row["queue_rank"] <= 20
                ],
            )
        self.assertEqual(
            Counter(row["decision"] for row in screens),
            Counter(
                {
                    "notice_check_allowed": 17,
                    "hold_term_likely_active": 1,
                    "hold_identity_or_death_unverified": 2,
                }
            ),
        )
        self.assertEqual(
            {
                row["text_id"]
                for row in screens
                if row["decision"] == "hold_identity_or_death_unverified"
            },
            {31692, 50287},
        )
        self.assertEqual(triage["input"]["ebook_files_acquired"], 0)
        self.assertEqual(triage["input"]["mwe_searches_run"], 0)
        self.assertEqual(triage["summary"]["admitted_units"], 0)

    def test_gutenberg_unit_gate_keeps_passes_local_and_target_blind(self):
        gate = GUTENBERG_UNIT_GATE
        self.assertEqual(
            gate["inputs"]["front_matter_review_sha256"],
            hashlib.sha256(
                (
                    ROOT
                    / "resources/gutenberg_2026_08_30_front_matter_review_batch1.json"
                ).read_bytes()
            ).hexdigest(),
        )
        self.assertFalse(gate["inputs"]["source_files_bundled"])
        self.assertFalse(gate["inputs"]["unit_text_bundled"])
        columns = gate["record_columns"]
        self.assertTrue(all(len(row) == len(columns) for row in gate["records"]))
        records = [dict(zip(columns, row)) for row in gate["records"]]
        starts = {
            row["text_id"]: row["first_unit_heading_line"]
            for row in (
                dict(zip(GUTENBERG_FRONT_MATTER_REVIEW["record_columns"], raw))
                for raw in GUTENBERG_FRONT_MATTER_REVIEW["records"]
            )
        }
        self.assertTrue(
            all(
                row["raw_unit_lines_inclusive"][0] == starts[row["text_id"]]
                and row["raw_unit_lines_inclusive"][1] + 1
                == row["next_sibling_heading_line"]
                and len(row["raw_unit_sha256"]) == 64
                and len(row["retained_unit_sha256"]) == 64
                for row in records
            )
        )
        self.assertEqual(
            {
                row["text_id"]
                for row in records
                if row["gate_decision"]
                == "passed_mechanical_unit_gate_release_pending"
            },
            {25885, 73331},
        )
        self.assertEqual(gate["summary"]["excluded_first_unit_over_maximum"], 10)
        self.assertEqual(gate["summary"]["excluded_ambiguous_first_unit_type"], 1)
        self.assertFalse(
            gate["structural_review_exposure"][
                "target_forms_senses_or_mwes_inspected"
            ]
        )
        self.assertEqual(gate["summary"]["admitted_units"], 0)
        self.assertEqual(gate["summary"]["target_or_mwe_searches_run"], 0)

    def test_gutenberg_front_matter_review_preserves_fixed_artifacts(self):
        review = GUTENBERG_FRONT_MATTER_REVIEW
        self.assertEqual(
            review["status"],
            "front_matter_reviewed_version_conditioned_unit_gate_ready",
        )
        self.assertEqual(
            review["inputs"]["notice_audit_sha256"],
            hashlib.sha256(
                (
                    ROOT
                    / "resources/gutenberg_2026_08_30_notice_audit_batch1.json"
                ).read_bytes()
            ).hexdigest(),
        )
        self.assertFalse(review["inputs"]["source_files_bundled"])

        columns = review["record_columns"]
        self.assertEqual(len(review["records"]), 13)
        self.assertTrue(all(len(row) == len(columns) for row in review["records"]))
        records = [dict(zip(columns, row)) for row in review["records"]]
        self.assertEqual(
            [row["text_id"] for row in records],
            [row["text_id"] for row in GUTENBERG_NOTICE_AUDIT["files"]],
        )
        notice_hashes = {
            row["text_id"]: row["sha256"]
            for row in GUTENBERG_NOTICE_AUDIT["files"]
        }
        self.assertTrue(
            all(
                row["file_sha256"] == notice_hashes[row["text_id"]]
                and row["reviewed_front_matter_lines_inclusive"][0]
                <= row["reviewed_front_matter_lines_inclusive"][1]
                < row["first_unit_heading_line"]
                and len(row["front_matter_sha256"]) == 64
                and row["decision"] == "ready_for_version_conditioned_unit_gate"
                for row in records
            )
        )
        self.assertEqual(
            {
                row["text_id"]
                for row in review["boundary_location_exposure"]["records"]
            },
            {25885, 46966, 7667, 46892, 48608, 53088, 1573, 72983, 76417},
        )
        self.assertFalse(
            review["boundary_location_exposure"]["mwe_or_lexical_search_run"]
        )
        self.assertEqual(
            review["summary"]["complete_print_publication_statement"], 8
        )
        self.assertEqual(
            review["summary"]["incomplete_print_publication_statement"], 5
        )
        self.assertEqual(
            review["summary"]["additional_retained_textual_contributors"], 0
        )
        self.assertEqual(review["summary"]["explicit_transcriber_notes"], 5)
        self.assertEqual(
            review["summary"]["ready_for_version_conditioned_unit_gate"], 13
        )
        self.assertEqual(review["summary"]["admitted_units"], 0)
        self.assertEqual(review["summary"]["mwe_searches_run"], 0)

    def test_gutenberg_notice_audit_pins_only_allowed_local_files(self):
        audit = GUTENBERG_NOTICE_AUDIT
        self.assertEqual(
            audit["status"], "preambles_verified_front_matter_and_units_pending"
        )
        self.assertEqual(
            audit["inputs"]["rights_triage_sha256"],
            hashlib.sha256(
                (
                    ROOT
                    / "resources/gutenberg_2026_08_30_rights_triage_batch1.json"
                ).read_bytes()
            ).hexdigest(),
        )
        self.assertFalse(audit["inputs"]["source_files_bundled"])
        columns = GUTENBERG_RIGHTS_TRIAGE["screen_columns"]
        expected = [
            row["text_id"]
            for row in (
                dict(zip(columns, item)) for item in GUTENBERG_RIGHTS_TRIAGE["screens"]
            )
            if row["decision"] == "notice_check_allowed"
        ]
        self.assertEqual([row["text_id"] for row in audit["files"]], expected)
        self.assertEqual(len(audit["files"]), 13)
        self.assertTrue(
            all(
                row["size_bytes"] > 0
                and len(row["sha256"]) == 64
                and row["checks"]["start_and_end_markers_present"]
                and row["checks"]["us_notice_and_non_us_warning_present"]
                and row["checks"]["full_project_gutenberg_license_footer_present"]
                for row in audit["files"]
            )
        )
        self.assertEqual(audit["summary"]["original_publication_missing"], 10)
        self.assertEqual(audit["summary"]["credits_missing"], 1)
        self.assertFalse(audit["scope"]["body_prose_reviewed"])
        self.assertEqual(audit["scope"]["units_selected"], 0)
        self.assertEqual(audit["scope"]["mwe_searches_run"], 0)
        self.assertFalse(audit["scope"]["public_web_distribution_authorized"])

    def test_gutenberg_rights_triage_is_a_fixed_content_blind_prefix(self):
        triage = GUTENBERG_RIGHTS_TRIAGE
        self.assertEqual(
            triage["status"], "pre_acquisition_metadata_triage_not_legal_clearance"
        )
        self.assertEqual(
            triage["input"]["frame_sha256"],
            hashlib.sha256(
                (ROOT / "resources/gutenberg_2026_08_30_prose_frame.json").read_bytes()
            ).hexdigest(),
        )
        self.assertEqual(triage["input"]["ebook_files_acquired"], 0)
        self.assertEqual(triage["input"]["mwe_searches_run"], 0)
        self.assertEqual(
            triage["method"]["global_web_distribution_status"],
            "unresolved_do_not_bundle_or_serve_source_text",
        )

        frame_columns = GUTENBERG_PROSE_FRAME["queue_columns"]
        frame_rows = [
            dict(zip(frame_columns, row)) for row in GUTENBERG_PROSE_FRAME["queue"]
        ]
        columns = triage["screen_columns"]
        screens = [dict(zip(columns, row)) for row in triage["screens"]]
        self.assertEqual(len(screens), 20)
        for stratum in ("adult_or_unspecified", "juvenile"):
            expected = [
                (row["queue_rank"], row["text_id"])
                for row in frame_rows
                if row["stratum"] == stratum and row["queue_rank"] <= 10
            ]
            actual = [
                (row["queue_rank"], row["text_id"])
                for row in screens
                if row["stratum"] == stratum
            ]
            self.assertEqual(actual, expected)

        decisions = Counter(row["decision"] for row in screens)
        self.assertEqual(
            decisions,
            Counter(
                {
                    "notice_check_allowed": 13,
                    "hold_term_likely_active": 5,
                    "hold_identity_or_death_unverified": 2,
                }
            ),
        )
        self.assertEqual(triage["summary"]["admitted_units"], 0)
        self.assertTrue(triage["method"]["incidental_search_exposure"]["occurred"])

    def test_gutenberg_frame_is_target_blind_and_frozen_before_text(self):
        frame = GUTENBERG_PROSE_FRAME
        self.assertEqual(
            frame["status"], "frozen_before_ebook_acquisition_or_mwe_inspection"
        )
        self.assertEqual(frame["source_catalog"]["size_bytes"], 21196613)
        self.assertEqual(
            frame["source_catalog"]["sha256"],
            "253f1b2d9aead75fec8ddb732c72a2fab5cd7db2f37745ef20760254f0666c4b",
        )
        self.assertFalse(frame["source_catalog"]["catalog_bundled"])
        self.assertEqual(frame["summary"]["eligible_metadata_records"], 22275)
        self.assertEqual(frame["summary"]["eligible_adult_or_unspecified_records"], 16122)
        self.assertEqual(frame["summary"]["eligible_juvenile_records"], 6153)
        self.assertEqual(frame["summary"]["ebook_files_read"], 0)
        self.assertEqual(frame["summary"]["mwe_searches_run"], 0)

        columns = frame["queue_columns"]
        rows = [dict(zip(columns, row)) for row in frame["queue"]]
        self.assertEqual(len(rows), 80)
        self.assertEqual(len({row["text_id"] for row in rows}), len(rows))
        self.assertTrue({"subjects", "bookshelves", "source_text"}.isdisjoint(columns))
        for name in frame["construct"]["strata"]:
            selected = [row for row in rows if row["stratum"] == name]
            self.assertEqual([row["queue_rank"] for row in selected], list(range(1, 41)))
        for row in rows:
            expected = hashlib.sha256(
                (
                    f'{frame["frame_id"]}\n{row["stratum"]}\n'
                    f'{row["text_id"]}'
                ).encode()
            ).hexdigest()
            self.assertEqual(row["selection_hash"], expected)
            self.assertEqual(row["state"], "queued_for_rights_and_unit_screen")

    def test_teco_mwe_triage_is_complete_preliminary_and_outcome_blind(self):
        triage = TECO_MWE_TRIAGE
        self.assertEqual(
            triage["status"],
            "preliminary_single_project_desk_triage_not_gold_annotation",
        )
        self.assertEqual(
            triage["inputs"]["candidate_screen_sha256"],
            hashlib.sha256(
                (ROOT / "resources/teco_v1_1_mwe_candidate_screen.json").read_bytes()
            ).hexdigest(),
        )
        self.assertEqual(
            triage["inputs"]["eye_movement_or_participant_outcome_files_read"], []
        )
        screen_by_id = {
            item["candidate_id"]: item for item in TECO_MWE_SCREEN["candidates"]
        }
        plausible = dict(triage["plausible_in_scope"])
        exceptions = {row[0]: row for row in triage["automatic_exceptions"]}
        self.assertTrue(set(plausible).isdisjoint(exceptions))
        self.assertTrue((set(plausible) | set(exceptions)).issubset(screen_by_id))
        summary = triage["summary"]
        self.assertEqual(len(plausible), summary["automatic_plausible_in_scope"])
        self.assertEqual(len(exceptions), summary["automatic_exception_count"])
        self.assertEqual(
            len(screen_by_id) - len(plausible) - len(exceptions),
            summary["automatic_default_not_retained"],
        )

        manual_columns = triage["manual_lead_columns"]
        manual = [dict(zip(manual_columns, row)) for row in triage["manual_leads"]]
        manual_plausible = [
            row for row in manual if row["desk_state"] == "plausible_in_scope"
        ]
        self.assertEqual(len(manual_plausible), summary["manual_plausible_in_scope"])
        self.assertEqual(
            sum(row["desk_state"] == "unresolved" for row in manual),
            summary["manual_unresolved"],
        )
        categories = Counter(plausible.values())
        categories.update(row["provisional_category"] for row in manual_plausible)
        self.assertEqual(dict(categories), summary["plausible_category_counts"])
        self.assertEqual(
            sum(screen_by_id[key]["crosses_inferred_line"] for key in plausible)
            + sum(row["crosses_inferred_line"] for row in manual_plausible),
            summary["plausible_cross_inferred_line_occurrences"],
        )
        self.assertEqual(
            sum(screen_by_id[key]["gap_count"] > 0 for key in plausible)
            + sum(
                row["member_positions"] is not None
                and row["member_positions"][-1] - row["member_positions"][0] + 1
                > len(row["member_positions"])
                for row in manual_plausible
            ),
            summary["plausible_discontinuous_occurrences"],
        )
        take_in_ids = {
            item["candidate_id"] for item in screen_by_id.values()
            if item["canonical_form"] == "take in"
        }
        self.assertEqual(len(take_in_ids), summary["oewn_take_in_leads"])
        self.assertTrue(take_in_ids.isdisjoint(plausible))
        self.assertIn("teco-t04-c003", take_in_ids)
        self.assertEqual(plausible["teco-t04-c002"], "VID")
        self.assertEqual(screen_by_id["teco-t04-c002"]["member_positions"], [87, 88])

    def test_teco_mwe_screen_is_prose_free_and_outcome_blind(self):
        screen = TECO_MWE_SCREEN
        self.assertEqual(screen["summary"]["text_count"], 30)
        self.assertEqual(screen["summary"]["word_item_count"], 10063)
        self.assertEqual(screen["summary"]["candidate_count"], 285)
        self.assertEqual(screen["summary"]["contiguous_candidate_count"], 126)
        self.assertEqual(screen["summary"]["gapped_candidate_count"], 159)
        self.assertEqual(screen["summary"]["line_initial_item_count"], 979)
        self.assertEqual(screen["summary"]["line_final_item_count"], 960)
        self.assertEqual(screen["inputs"]["eye_movement_or_participant_outcome_files_read"], [])
        self.assertEqual(
            screen["inputs"]["teco_manifest_sha256"],
            hashlib.sha256(
                (ROOT / "resources/teco_v1_1_candidate_manifest.json").read_bytes()
            ).hexdigest(),
        )
        candidates = screen["candidates"]
        self.assertEqual(len({item["candidate_id"] for item in candidates}), len(candidates))
        self.assertTrue(all(item["review_status"] == "unreviewed" for item in candidates))
        self.assertTrue(all("ia" not in item and "lemma" not in item for item in candidates))
        take_in = [item for item in candidates if item["canonical_form"] == "take in"]
        self.assertEqual(len(take_in), 3)
        self.assertTrue(all(item["gap_count"] > 0 for item in take_in))
        self.assertIn(
            [87, 88],
            [item["member_positions"] for item in candidates
             if item["canonical_form"] == "take part"],
        )

    def test_teco_candidate_manifest_preserves_existing_data_boundary(self):
        manifest = TECO_CANDIDATE_MANIFEST
        self.assertEqual(manifest["status"], "metadata_and_join_contract_verified_not_yet_admitted_for_analysis")
        self.assertEqual(manifest["design"]["participants"], 41)
        self.assertEqual(manifest["design"]["word_items"], 10063)
        self.assertEqual(manifest["design"]["participant_word_observations"], 412583)
        joins = manifest["verified_join_contract"]
        self.assertEqual(joins["passage_subject_text_pairs"], 1230)
        self.assertEqual(joins["word_information_duplicate_keys"], 0)
        self.assertEqual(joins["word_keys_not_repeated_for_all_41_subjects"], 0)
        self.assertTrue(all("text" not in item and "participant_rows" not in item for item in manifest["verified_files"]))
        rights = manifest["rights_review"]
        self.assertEqual(
            rights["finding"],
            "hold_eiken_text_and_reconstructable_token_sequences_pending_documented_downstream_permission",
        )
        self.assertIn(
            "ordered ia, lemma, or other surface/token sequences capable of reconstructing a passage",
            rights["release_boundary"]["exclude"],
        )
        reading_materials = next(
            item for item in manifest["verified_files"]
            if item["name"] == "Reading Matarials.pdf"
        )
        self.assertTrue(reading_materials["local_hash_verified"])
        project_role = manifest["project_role"]
        self.assertFalse(project_role["core_dependency"])
        self.assertEqual(project_role["first_paper_downstream_selection"], "none")
        self.assertFalse(project_role["runtime_or_api_data_dependency"])

    def test_simplewiki_route2_is_frozen_before_text_acquisition(self):
        design = SIMPLEWIKI_ROUTE2_DESIGN
        self.assertEqual(design["status"], "frozen_before_article_text_acquisition")
        source = design["source_frame"]
        self.assertEqual(source["snapshot"], "2026-08-01")
        self.assertEqual(source["artifact_size_bytes"], 384058867)
        self.assertEqual(
            source["artifact_sha1"], "4f646363bd2d095652149a6bdd87a0cedf51f6b2"
        )
        self.assertEqual(
            [item["canonical_form"] for item in design["target_derivation"]["targets"]],
            ["take in", "pick up", "give up", "come out", "make it", "get it"],
        )
        self.assertEqual(design["sampling"]["maximum_desk_screens_per_target"], 20)
        self.assertEqual(design["gate"]["maximum_articles"], 18)
        self.assertIn("pronoun or noun-phrase object", design["gate"]["discontinuity"])
        for key, path in (
            ("streusle_profile_sha256", "benchmarks/streusle_v5_vpc_vid.json"),
            ("oewn_profile_sha256", "resources/oewn_2025_multiword_verbs.json"),
            ("ngsl_profile_sha256", "resources/ngsl_1_2_ascii_forms.json"),
            ("mwe_contract_sha256", "mwe_contract.json"),
        ):
            self.assertEqual(
                design["target_derivation"]["frozen_inputs"][key],
                hashlib.sha256((ROOT / path).read_bytes()).hexdigest(),
            )
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/simplewiki_gate1_route2_design.json").read_bytes()
            ).hexdigest(),
            "c4bb1a03b4a63c6e83f23f2589452070a9e5b9b4f3a879d10184d98c16e07cbb",
        )

    def test_simplewiki_candidate_ledger_reproduces_the_frozen_queues(self):
        ledger = SIMPLEWIKI_ROUTE2_CANDIDATES
        self.assertEqual(ledger["design_id"], SIMPLEWIKI_ROUTE2_DESIGN["design_id"])
        self.assertEqual(
            ledger["inputs"]["design_sha256"],
            hashlib.sha256(
                (ROOT / "resources/simplewiki_gate1_route2_design.json").read_bytes()
            ).hexdigest(),
        )
        source = SIMPLEWIKI_ROUTE2_DESIGN["source_frame"]
        self.assertEqual(ledger["inputs"]["dump_size_bytes"], source["artifact_size_bytes"])
        self.assertEqual(ledger["inputs"]["dump_sha1"], source["artifact_sha1"])
        columns = ledger["row_columns"]
        self.assertTrue({
            "canonical_form", "page_id", "revision_id", "title", "selection_hash",
            "state", "queue_rank",
        }.issubset(columns))
        self.assertTrue({"wikitext", "text", "contributor"}.isdisjoint(columns))
        rows = [dict(zip(columns, row)) for row in ledger["rows"]]
        self.assertEqual(len(rows), 16375)
        self.assertEqual(len({row["page_id"] for row in rows}), 14730)
        for row in rows:
            expected = hashlib.sha256(
                (
                    f'{ledger["design_id"]}\n{row["canonical_form"]}\n'
                    f'{row["page_id"]}\n{row["revision_id"]}'
                ).encode()
            ).hexdigest()
            self.assertEqual(row["selection_hash"], expected)
        for target in SIMPLEWIKI_ROUTE2_DESIGN["target_derivation"]["targets"]:
            form_rows = [
                row for row in rows
                if row["canonical_form"] == target["canonical_form"]
                and row["state"] == "queued_for_desk_screen"
            ]
            self.assertEqual(
                [row["queue_rank"] for row in form_rows],
                list(range(1, len(form_rows) + 1)),
            )
        self.assertFalse(ledger["construct"]["article_text_bundled"])
        self.assertFalse(ledger["construct"]["contributor_data_bundled"])
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/simplewiki_gate1_route2_candidates.json").read_bytes()
            ).hexdigest(),
            "0dd69c11e96e2b955ed5f459cbf60fab5253799f815fa6ff12c75981bfca59c0",
        )

    def test_simplewiki_rendered_screen_stops_at_twenty_eligible_rows(self):
        subprocess.run(
            ["python3", "-B", str(ROOT / "scripts/prepare_simplewiki_contrasts.py"), "--self-check"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        with tempfile.TemporaryDirectory() as cache:
            missing = subprocess.run(
                ["python3", "-B", str(ROOT / "scripts/prepare_simplewiki_contrasts.py"), "--contrast-plan", "--cache", cache],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertNotEqual(missing.returncode, 0)
            self.assertEqual(missing.stdout, "")
            self.assertIn("FileNotFoundError", missing.stderr)
        ledger = SIMPLEWIKI_ROUTE2_RENDERED
        self.assertEqual(
            ledger["inputs"]["candidate_ledger_sha256"],
            hashlib.sha256(
                (ROOT / "resources/simplewiki_gate1_route2_candidates.json").read_bytes()
            ).hexdigest(),
        )
        self.assertEqual(ledger["summary"]["rendered_queue_row_count"], 509)
        self.assertEqual(ledger["summary"]["unique_revision_count"], 508)
        self.assertEqual(ledger["summary"]["eligible_for_desk_review_count"], 120)
        self.assertEqual(ledger["summary"]["eligible_unique_revision_count"], 119)
        self.assertEqual(ledger["summary"]["eligible_cross_target_flag_row_count"], 42)
        self.assertEqual(ledger["summary"]["mechanically_excluded_row_count"], 389)
        self.assertEqual(ledger["summary"]["verified_source_row_count"], 508)
        self.assertEqual(ledger["summary"]["unavailable_revision_row_count"], 1)
        columns = ledger["row_columns"]
        self.assertTrue({"wikitext", "text", "rendered_html"}.isdisjoint(columns))
        rows = [dict(zip(columns, row)) for row in ledger["rows"]]
        self.assertEqual(len(rows), 509)
        for target in SIMPLEWIKI_ROUTE2_DESIGN["target_derivation"]["targets"]:
            eligible = [
                row for row in rows
                if row["canonical_form"] == target["canonical_form"] and
                row["mechanical_state"] == "eligible_for_desk_review"
            ]
            self.assertEqual([row["desk_screen_rank"] for row in eligible], list(range(1, 21)))
            self.assertTrue(all(400 <= row["profile_token_count"] <= 1000 for row in eligible))
        self.assertFalse(ledger["construct"]["article_text_bundled"])
        self.assertFalse(ledger["construct"]["rendered_html_bundled"])
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/simplewiki_gate1_route2_rendered_screen.json").read_bytes()
            ).hexdigest(),
            "e0cce039a3331fffdc0e8ff914506db5004bf7c782d5cceb2d354a5f1cfac148",
        )

    def test_simplewiki_take_in_review_exhausts_the_frozen_desk_limit(self):
        review = SIMPLEWIKI_ROUTE2_TAKE_IN_REVIEW
        self.assertEqual(
            review["inputs"]["rendered_screen_sha256"],
            hashlib.sha256(
                (ROOT / "resources/simplewiki_gate1_route2_rendered_screen.json").read_bytes()
            ).hexdigest(),
        )
        self.assertEqual(review["summary"]["desk_row_count"], 20)
        self.assertEqual(review["summary"]["take_head_token_count_reviewed"], 41)
        self.assertEqual(review["summary"]["automatic_gap_lead_count"], 28)
        self.assertEqual(review["summary"]["false_span_count"], 28)
        self.assertEqual(review["summary"]["confirmed_target_occurrence_count"], 0)
        self.assertEqual(review["summary"]["manual_missed_target_occurrence_count"], 0)
        self.assertEqual(
            review["summary"]["target_state"],
            "failed_at_frozen_20_desk_screen_limit",
        )
        rendered_columns = SIMPLEWIKI_ROUTE2_RENDERED["row_columns"]
        rendered_rows = {
            row["desk_screen_rank"]: row for row in (
                dict(zip(rendered_columns, values))
                for values in SIMPLEWIKI_ROUTE2_RENDERED["rows"]
            )
            if row["canonical_form"] == "take in" and row["desk_screen_rank"]
        }
        self.assertEqual(
            [article["desk_screen_rank"] for article in review["articles"]],
            list(range(1, 21)),
        )
        decisions = []
        for article in review["articles"]:
            rendered = rendered_rows[article["desk_screen_rank"]]
            for key in (
                "queue_rank", "page_id", "revision_id", "title",
                "extracted_text_sha256", "profile_token_count",
            ):
                self.assertEqual(article[key], rendered[key])
            self.assertEqual(
                len(article["automatic_gap_decisions"]), rendered["gap_lead_count"]
            )
            self.assertEqual(article["target_occurrence_count"], 0)
            decisions.extend(article["automatic_gap_decisions"])
        self.assertEqual(len(decisions), 28)
        self.assertTrue(all(decision[5] == "false_span" for decision in decisions))
        self.assertEqual(
            dict(sorted(Counter(decision[6] for decision in decisions).items())),
            review["summary"]["false_span_reason_counts"],
        )
        self.assertEqual(
            sum(article["take_head_token_count_reviewed"] for article in review["articles"]),
            41,
        )
        self.assertNotIn("surface_span", review["construct"]["lead_columns"])
        self.assertFalse(review["construct"]["article_text_bundled"])
        self.assertFalse(review["construct"]["surface_spans_bundled"])
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/simplewiki_gate1_route2_take_in_desk_review.json").read_bytes()
            ).hexdigest(),
            "6b73f6971be64d36f0d9e048cdc9b6468dd26c99480ecd10c7e427cf2a744bae",
        )

    def test_simplewiki_pick_up_review_stops_at_three_selected_pages(self):
        review = SIMPLEWIKI_ROUTE2_PICK_UP_REVIEW
        self.assertEqual(
            review["inputs"]["rendered_screen_sha256"],
            hashlib.sha256(
                (ROOT / "resources/simplewiki_gate1_route2_rendered_screen.json").read_bytes()
            ).hexdigest(),
        )
        summary = review["summary"]
        self.assertEqual(summary["desk_row_count"], 4)
        self.assertEqual(summary["pick_head_token_count_reviewed"], 5)
        self.assertEqual(summary["automatic_contiguous_lead_count"], 3)
        self.assertEqual(summary["automatic_gap_lead_count"], 2)
        self.assertEqual(summary["confirmed_target_occurrence_count"], 5)
        self.assertEqual(summary["false_span_count"], 0)
        self.assertEqual(summary["manual_missed_target_occurrence_count"], 0)
        self.assertEqual(summary["selected_desk_screen_ranks"], [1, 2, 4])
        self.assertEqual(len(summary["selected_operational_meaning_ids"]), 3)
        self.assertEqual(
            summary["target_state"],
            "provisionally_passed_at_frozen_early_stop_pending_author_confirmation",
        )

        rendered_columns = SIMPLEWIKI_ROUTE2_RENDERED["row_columns"]
        rendered_rows = {
            row["desk_screen_rank"]: row for row in (
                dict(zip(rendered_columns, values))
                for values in SIMPLEWIKI_ROUTE2_RENDERED["rows"]
            )
            if row["canonical_form"] == "pick up" and row["desk_screen_rank"]
        }
        self.assertEqual(
            [article["desk_screen_rank"] for article in review["articles"]],
            [1, 2, 3, 4],
        )
        decisions = []
        selected = []
        for article in review["articles"]:
            rendered = rendered_rows[article["desk_screen_rank"]]
            for key in (
                "queue_rank", "page_id", "revision_id", "revision_timestamp", "title",
                "extracted_text_sha256", "profile_token_count",
            ):
                self.assertEqual(article[key], rendered[key])
            self.assertEqual(
                len(article["automatic_decisions"]),
                rendered["contiguous_lead_count"] + rendered["gap_lead_count"],
            )
            decisions.extend(article["automatic_decisions"])
            if article["passage_state"].startswith("provisionally_selected"):
                selected.append(article)
                self.assertIsNotNone(article["assessment"]["global_question"])
                self.assertIsNotNone(article["assessment"]["target_critical_item"])
                self.assertIsNotNone(article["rights"])

        self.assertEqual(len(decisions), 5)
        self.assertTrue(all(decision[6] == "confirmed_target_occurrence" for decision in decisions))
        self.assertEqual(
            sum(article["pick_head_token_count_reviewed"] for article in review["articles"]),
            5,
        )
        self.assertEqual([article["desk_screen_rank"] for article in selected], [1, 2, 4])
        self.assertEqual(
            review["articles"][2]["passage_state"],
            "reject_prespecified_acute_violence",
        )
        non_focal = review["articles"][3]["non_focal_target_decisions"]
        self.assertEqual(
            Counter(decision[7] for decision in non_focal),
            Counter({"confirmed_non_focal_target_occurrence": 2, "false_span": 1}),
        )
        self.assertNotIn("surface_span", review["construct"]["automatic_decision_columns"])
        self.assertFalse(review["construct"]["article_text_bundled"])
        self.assertFalse(review["construct"]["surface_spans_bundled"])
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/simplewiki_gate1_route2_pick_up_desk_review.json").read_bytes()
            ).hexdigest(),
            "025286cb27f4a64e2810eb8824271ba4da487bb8e47daa0bb63f8867f217d3c5",
        )

    def test_simplewiki_give_up_review_is_preserved_under_content_neutral_amendment(self):
        review = SIMPLEWIKI_ROUTE2_GIVE_UP_REVIEW
        summary = review["summary"]
        self.assertEqual(summary["desk_row_count"], 15)
        self.assertEqual(summary["give_head_token_count_reviewed"], 35)
        self.assertEqual(summary["automatic_contiguous_lead_count"], 15)
        self.assertEqual(summary["automatic_gap_lead_count"], 4)
        self.assertEqual(summary["confirmed_target_occurrence_count"], 15)
        self.assertEqual(summary["false_span_count"], 4)
        self.assertEqual(summary["manual_missed_target_occurrence_count"], 0)
        self.assertEqual(summary["selected_desk_screen_ranks"], [3, 5, 15])

        rendered_columns = SIMPLEWIKI_ROUTE2_RENDERED["row_columns"]
        rendered_rows = {
            row["desk_screen_rank"]: row for row in (
                dict(zip(rendered_columns, values))
                for values in SIMPLEWIKI_ROUTE2_RENDERED["rows"]
            )
            if row["canonical_form"] == "give up" and row["desk_screen_rank"]
        }
        decisions = []
        for article in review["articles"]:
            rendered = rendered_rows[article["desk_screen_rank"]]
            for key in (
                "queue_rank", "page_id", "revision_id", "revision_timestamp", "title",
                "extracted_text_sha256", "profile_token_count",
            ):
                self.assertEqual(article[key], rendered[key])
            self.assertEqual(
                len(article["automatic_decisions"]),
                rendered["contiguous_lead_count"] + rendered["gap_lead_count"],
            )
            decisions.extend(article["automatic_decisions"])
        self.assertEqual(
            Counter(decision[6] for decision in decisions),
            Counter({"confirmed_target_occurrence": 15, "false_span": 4}),
        )
        self.assertEqual(
            sum(article["give_head_token_count_reviewed"] for article in review["articles"]),
            35,
        )
        self.assertFalse(review["construct"]["article_text_bundled"])
        self.assertFalse(review["construct"]["surface_spans_bundled"])
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/simplewiki_gate1_route2_give_up_desk_review.json").read_bytes()
            ).hexdigest(),
            "5a2f33818cf24f5b243d2ba1d4373da6ded544351fd77e8932a0d98bf654c4b3",
        )

        amendment = SIMPLEWIKI_ROUTE2_CONTENT_NEUTRAL_AMENDMENT
        self.assertEqual(
            amendment["inputs"]["frozen_design_sha256"],
            hashlib.sha256(
                (ROOT / "resources/simplewiki_gate1_route2_design.json").read_bytes()
            ).hexdigest(),
        )
        self.assertEqual(
            amendment["inputs"]["give_up_review_sha256"],
            hashlib.sha256(
                (ROOT / "resources/simplewiki_gate1_route2_give_up_desk_review.json").read_bytes()
            ).hexdigest(),
        )
        self.assertEqual(
            amendment["frozen_record_treatment"]["route2_state"],
            "stopped_before_come_out_pending_content_neutral_redesign",
        )
        self.assertEqual(
            amendment["affected_decisions"]["pick_up"]["content_neutral_counterfactual_ranks"],
            [1, 2, 3],
        )
        self.assertEqual(
            amendment["affected_decisions"]["give_up"]["content_neutral_counterfactual_ranks"],
            [1, 3, 5],
        )
        self.assertIn(
            "pass away",
            amendment["affected_decisions"]["target_derivation"]["material_consequence"],
        )
        pool = amendment["affected_decisions"]["target_derivation"][
            "content_neutral_pool_reproduction"
        ]
        self.assertEqual(pool["eligible_vpc_type_count"], 19)
        self.assertEqual(pool["eligible_vid_type_count"], 3)
        self.assertEqual(pool["ranked_vid_forms"], ["make it", "pass away", "get it"])
        self.assertEqual(
            hashlib.sha256(
                (
                    ROOT
                    / "resources/simplewiki_gate1_route2_content_neutral_amendment.json"
                ).read_bytes()
            ).hexdigest(),
            "f58eb68779ba0e598edf3a87fe24ce76cb06c6506af35f03adf10237f4a412b2",
        )

    def test_voa_material_frame_is_frozen_and_target_blind(self):
        frame = VOA_MATERIAL_FRAME
        self.assertEqual(frame["frame_id"], "gate1-voa-frame-v1")
        self.assertEqual(frame["article_count"], 936)
        self.assertEqual(frame["seen_article_count"], 3)
        self.assertEqual(frame["initial_metadata_draw_count"], 24)
        self.assertEqual(len(frame["archives"]), 79)
        for category in ("education", "health"):
            queue = [
                item for item in frame["articles"]
                if item["sampling_category"] == category and
                not item["seen_before_frame_freeze"]
            ]
            self.assertEqual(
                [item["target_blind_queue_rank"] for item in queue],
                list(range(1, len(queue) + 1)),
            )
            self.assertEqual(sum(item["initial_metadata_draw"] for item in queue), 12)
            for item in queue:
                expected = hashlib.sha256(
                    f'gate1-voa-frame-v1\n{item["canonical_url"]}'.encode()
                ).hexdigest()
                self.assertEqual(item["selection_hash"], expected)
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/voa_gate1_frame_2017_2020.json").read_bytes()
            ).hexdigest(),
            "cb6911287348f7e98353b65b441f1f7c421ffe47b74c4ac7d18dbb4c77190dca",
        )

    def test_voa_source_screen_stops_at_twelve_per_category(self):
        screen = VOA_SOURCE_SCREEN
        self.assertEqual(screen["frame_id"], VOA_MATERIAL_FRAME["frame_id"])
        self.assertEqual(screen["decision_count"], 63)
        reports = {
            item["sampling_category"]: item for item in screen["category_reports"]
        }
        self.assertEqual(reports["education"]["queue_stop_rank"], 25)
        self.assertEqual(reports["health"]["queue_stop_rank"], 38)
        self.assertEqual(reports["education"]["eligible_count"], 12)
        self.assertEqual(reports["health"]["eligible_count"], 12)
        self.assertEqual(
            sum(item["state"] == "eligible" for item in screen["decisions"]), 24
        )
        self.assertTrue(all("text" not in item for item in screen["decisions"]))
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/voa_gate1_source_screen.json").read_bytes()
            ).hexdigest(),
            "5ebe015f15874a127940bbd6ad196f4b031d0487bf4d56c5712e68151881e7aa",
        )

    def test_voa_automated_profile_is_a_lead_screen_not_an_admission(self):
        profile = VOA_AUTOMATED_PROFILE
        self.assertEqual(profile["source_screen_id"], VOA_SOURCE_SCREEN["screen_id"])
        self.assertEqual(profile["summary"], {
            "article_count": 24,
            "automatic_oewn_lead_count": 229,
            "distinct_canonical_form_count": 110,
            "forms_in_multiple_documents": 38,
            "automatic_oewn_gap_lead_count": 128,
            "distinct_gap_canonical_form_count": 80,
            "gap_forms_in_multiple_documents": 19,
        })
        self.assertIn("MWE occurrence truth", profile["construct"]["excluded_inferences"])
        self.assertTrue(all("text" not in item for item in profile["articles"]))
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/voa_gate1_automated_profile.json").read_bytes()
            ).hexdigest(),
            "efe61f49a81e59274d532a650da4a362dab4067eeaa0f0fe79bdebf4b8b77603",
        )

    def test_voa_recurrence_triage_covers_every_recurrent_lead_form(self):
        recurrent = {
            item["canonical_form"]
            for item in VOA_AUTOMATED_PROFILE["cross_document_recurrence"]
            if item["document_frequency"] > 1
        }
        rows = VOA_RECURRENCE_TRIAGE["forms"]
        self.assertEqual({item["canonical_form"] for item in rows}, recurrent)
        self.assertEqual(
            set(VOA_RECURRENCE_TRIAGE["gap_review"]["recurrent_canonical_forms"]),
            {
                item["canonical_form"]
                for item in VOA_AUTOMATED_PROFILE["cross_document_gap_recurrence"]
                if item["document_frequency"] > 1
            },
        )
        self.assertEqual(
            VOA_RECURRENCE_TRIAGE["source_profile_sha256"],
            hashlib.sha256(
                (ROOT / "resources/voa_gate1_automated_profile.json").read_bytes()
            ).hexdigest(),
        )
        self.assertEqual(len(rows), 38)
        self.assertEqual(
            sum(item["state"] == "retain_for_occurrence_review" for item in rows), 13
        )
        self.assertTrue(VOA_RECURRENCE_TRIAGE["summary"]["author_confirmation_pending"])
        self.assertEqual(VOA_RECURRENCE_TRIAGE["summary"]["gap_recurrent_form_count"], 19)
        self.assertEqual(
            VOA_RECURRENCE_TRIAGE["summary"]["gap_recurrent_form_retained_count"], 0
        )
        self.assertFalse(VOA_RECURRENCE_TRIAGE["construct"]["article_text_bundled"])
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/voa_gate1_recurrence_triage.json").read_bytes()
            ).hexdigest(),
            "884c087db0821131e5b76168f3640fcbd5f7f2e08171226ba0430eef030a88a0",
        )

    def test_voa_priority_review_covers_every_frozen_lead_in_three_articles(self):
        self.assertEqual(
            VOA_PRIORITY_REVIEW["inputs"]["taxonomy_standard"],
            "PARSEME shared-task annotation guidelines 1.2",
        )
        self.assertTrue(
            VOA_PRIORITY_REVIEW["inputs"]["taxonomy_url"].startswith(
                MWE_CONTRACT["scope"]["category_scheme"]["url"]
            )
        )
        self.assertEqual(
            VOA_PRIORITY_REVIEW["inputs"]["automated_profile_sha256"],
            hashlib.sha256(
                (ROOT / "resources/voa_gate1_automated_profile.json").read_bytes()
            ).hexdigest(),
        )
        reviewed_ids = {item["article_id"] for item in VOA_PRIORITY_REVIEW["articles"]}
        self.assertEqual(reviewed_ids, {"education-07", "education-12", "education-16"})
        for review in VOA_PRIORITY_REVIEW["articles"]:
            article = next(
                item for item in VOA_AUTOMATED_PROFILE["articles"]
                if item["article_id"] == review["article_id"]
            )
            self.assertEqual(review["text_sha256"], article["text_sha256"])
            self.assertEqual(
                {item[0] for item in review["automatic_contiguous_decisions"]},
                {item["lead_id"] for item in article["automatic_oewn_leads"]},
            )
            self.assertEqual(
                {item[0] for item in review["automatic_gap_decisions"]},
                {item["lead_id"] for item in article["automatic_oewn_gap_leads"]},
            )
        self.assertTrue(all(
            item["state"].startswith("reject_from_primary")
            for item in VOA_PRIORITY_REVIEW["pair_decisions"]
        ))
        self.assertFalse(VOA_PRIORITY_REVIEW["construct"]["article_text_bundled"])
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/voa_gate1_priority_desk_review.json").read_bytes()
            ).hexdigest(),
            "37b4d98de38f2dd269c5e96fdab47ba9e96fe2b479270b77bc65f5d716f622eb",
        )

    def test_voa_deferred_review_covers_every_frozen_lead_in_two_articles(self):
        self.assertEqual(
            VOA_DEFERRED_REVIEW["inputs"]["taxonomy_standard"],
            "PARSEME shared-task annotation guidelines 1.2",
        )
        self.assertTrue(
            VOA_DEFERRED_REVIEW["inputs"]["taxonomy_url"].startswith(
                MWE_CONTRACT["scope"]["category_scheme"]["url"]
            )
        )
        self.assertEqual(
            VOA_DEFERRED_REVIEW["inputs"]["automated_profile_sha256"],
            hashlib.sha256(
                (ROOT / "resources/voa_gate1_automated_profile.json").read_bytes()
            ).hexdigest(),
        )
        self.assertEqual(
            VOA_DEFERRED_REVIEW["inputs"]["priority_review_sha256"],
            hashlib.sha256(
                (ROOT / "resources/voa_gate1_priority_desk_review.json").read_bytes()
            ).hexdigest(),
        )
        reviewed_ids = {item["article_id"] for item in VOA_DEFERRED_REVIEW["articles"]}
        self.assertEqual(reviewed_ids, {"health-03", "health-22"})
        for review in VOA_DEFERRED_REVIEW["articles"]:
            article = next(
                item for item in VOA_AUTOMATED_PROFILE["articles"]
                if item["article_id"] == review["article_id"]
            )
            self.assertEqual(review["source_sha256"], article["source_sha256"])
            self.assertEqual(review["text_sha256"], article["text_sha256"])
            self.assertEqual(
                {item[0] for item in review["automatic_contiguous_decisions"]},
                {item["lead_id"] for item in article["automatic_oewn_leads"]},
            )
            self.assertEqual(
                {item[0] for item in review["automatic_gap_decisions"]},
                {item["lead_id"] for item in article["automatic_oewn_gap_leads"]},
            )
        self.assertTrue(all(
            item["state"].startswith("reject_from_primary")
            for item in VOA_DEFERRED_REVIEW["pair_decisions"]
        ))
        self.assertTrue(all(
            item["state"].startswith("reject_from_bounded")
            for item in VOA_DEFERRED_REVIEW["manual_recurrence_leads"]
        ))
        self.assertFalse(VOA_DEFERRED_REVIEW["construct"]["raw_html_bundled"])
        self.assertFalse(VOA_DEFERRED_REVIEW["construct"]["article_text_bundled"])
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/voa_gate1_deferred_pair_desk_review.json").read_bytes()
            ).hexdigest(),
            "c8bdb79a095c96c1573967403a6cd4f5b5f0736aa384debbb1463b5300d6b31d",
        )

    def test_voa_out_of_inventory_audit_exhausts_the_remaining_frame(self):
        audit = VOA_OUT_OF_INVENTORY_AUDIT
        self.assertEqual(
            audit["inputs"]["automated_profile_sha256"],
            hashlib.sha256(
                (ROOT / "resources/voa_gate1_automated_profile.json").read_bytes()
            ).hexdigest(),
        )
        for key, path in (
            ("mwe_contract_sha256", "mwe_contract.json"),
            ("ngsl_profile_sha256", "resources/ngsl_1_2_ascii_forms.json"),
            ("oewn_form_profile_sha256", "resources/oewn_2025_multiword_verbs.json"),
            ("streusle_profile_sha256", "benchmarks/streusle_v5_vpc_vid.json"),
        ):
            self.assertEqual(
                audit["inputs"][key],
                hashlib.sha256((ROOT / path).read_bytes()).hexdigest(),
            )
        reviewed_ids = {
            item["article_id"]
            for review in (VOA_PRIORITY_REVIEW, VOA_DEFERRED_REVIEW)
            for item in review["articles"]
        }
        expected_articles = {
            item["article_id"]: item
            for item in VOA_AUTOMATED_PROFILE["articles"]
            if item["article_id"] not in reviewed_ids
        }
        self.assertEqual(len(audit["source_verification"]), 19)
        self.assertEqual(
            {item[0] for item in audit["source_verification"]},
            set(expected_articles),
        )
        for article_id, source_hash, text_hash, paragraph_count in audit["source_verification"]:
            expected = expected_articles[article_id]
            self.assertEqual(source_hash, expected["source_sha256"])
            self.assertEqual(text_hash, expected["text_sha256"])
            self.assertEqual(paragraph_count, expected["paragraph_count"])
        self.assertEqual(audit["generation_summary"], {
            "streusle_strong_types_before_projection_filter": 389,
            "candidate_types_after_ascii_member_and_oewn_filters": 227,
            "contiguous_leads": 30,
            "contiguous_distinct_forms": 18,
            "contiguous_cross_document_forms": 6,
            "short_gap_leads": 41,
            "short_gap_distinct_forms": 12,
            "short_gap_cross_document_forms": 6,
            "merged_cross_document_forms": 10,
        })
        self.assertEqual(
            {item[0] for item in audit["merged_recurrent_candidate_decisions"]},
            {"base on", "be up", "have do", "have it", "have time", "have to",
             "make money", "say no", "spend time", "take time"},
        )
        pair_scan = audit["upper_bound_pair_scan"]
        self.assertEqual(pair_scan["maximum_shared_candidate_forms_per_pair"], 1)
        self.assertEqual(pair_scan["pairs_with_more_than_one_shared_candidate_form"], [])
        self.assertTrue(all(
            len(item[1]) == 1 for item in pair_scan["pairs_with_one_shared_candidate_form"]
        ))
        self.assertEqual(
            audit["decision"]["state"],
            "frozen_voa_frame_exhausted_no_passage_pair_admitted",
        )
        self.assertFalse(audit["construct"]["raw_html_bundled"])
        self.assertFalse(audit["construct"]["article_text_bundled"])
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/voa_gate1_out_of_inventory_audit.json").read_bytes()
            ).hexdigest(),
            "9a09068873e195a91cda9060af87474b69239aaa38da014846c41c009fe03802",
        )

    def test_admitted_reference_profiles_are_complete_and_separate(self):
        required = set(REFERENCE_TEMPLATE["required_sections"])
        for profile, channel, function in (
            (TUBELEX_PROFILE, "word", "frequency_distribution"),
            (NGSL_PROFILE, "word", "ranked_inventory"),
            (OEWN_FORM_PROFILE, "mwe_form", "inventory_membership"),
        ):
            self.assertTrue(required.issubset(profile))
            self.assertEqual(profile["identity"]["profile_status"], "admitted")
            self.assertEqual(profile["construct"]["coverage_channel"], channel)
            self.assertEqual(profile["construct"]["reference_function"], function)
            self.assertTrue(profile["rights"]["browser_delivery_permitted"])

        self.assertEqual(TUBELEX_PROFILE["table"]["projected_row_count"], 410400)
        self.assertEqual(TUBELEX_PROFILE["corpus_design"]["token_count"], 179139158)
        self.assertEqual(TUBELEX_PROFILE["rows"][0], ["the", 7455441])
        self.assertEqual(NGSL_PROFILE["table"]["source_headword_count"], 2809)
        self.assertEqual(NGSL_PROFILE["table"]["projected_row_count"], 10114)
        self.assertEqual(NGSL_PROFILE["table"]["ambiguous_surface_form_count"], 5)
        self.assertEqual(dict(NGSL_PROFILE["rows"])["found"], [["find", 81], ["found", 2807]])
        self.assertEqual(OEWN_FORM_PROFILE["table"]["projected_row_count"], 2847)
        forms = dict(OEWN_FORM_PROFILE["rows"])
        self.assertEqual(forms["take in"], 17)
        self.assertEqual(forms["spill the beans"], 1)
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/ngsl_1_2_ascii_forms.json").read_bytes()
            ).hexdigest(),
            "f613834eac74e19cef787faf1414a716388c047b3f5b7e39db88c78883fef6d9",
        )
        self.assertEqual(
            hashlib.sha256((ROOT / "resources/NGSL_NOTICE.md").read_bytes()).hexdigest(),
            "bd9e26de02a697d9020780d535d18a01033a072e19a3b0a680115bd511d1d931",
        )
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/tubelex_en_regex_ascii_2025.json").read_bytes()
            ).hexdigest(),
            "d177f22f5cd4c86d5d7465197eebccceda84c0e3ab8ca5ecfbcdbc9fbd29d1bc",
        )
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "resources/oewn_2025_multiword_verbs.json").read_bytes()
            ).hexdigest(),
            "513714774f0e087e9ba03c8fa04e969b8314786ccbdaa06dbbeeb35127f6a41e",
        )
        self.assertEqual(
            hashlib.sha256((ROOT / "resources/TUBELEX_LICENSE.txt").read_bytes()).hexdigest(),
            "51b9e39825bbf19e4bb777bf11a7520a3935ff859c4d0ee724dfe9ddb26a961f",
        )

    def test_streusle_profile_is_external_and_matches_the_mwe_contract(self):
        self.assertEqual(STREUSLE_PROFILE["profile_version"], "0.1.0")
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
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "benchmarks/streusle_v5_vpc_vid.json").read_bytes()
            ).hexdigest(),
            STREUSLE_GAP_BASELINE["source"]["profile_sha256"],
        )
        rules = STREUSLE_GAP_BASELINE["rules"]
        self.assertEqual(rules["maximum_intervening_tokens_per_member_pair"], 2)
        self.assertEqual(rules["minimum_train_dependency_arc_count"], 5)
        result = STREUSLE_GAP_BASELINE["expected_report"]
        self.assertGreater(
            result["development"]["gap_dependency"]["exact_span"]["f1"],
            result["development"]["lemma_window_ablation"]["exact_span"]["f1"],
        )
        self.assertEqual(
            result["development"]["gap_dependency"]["discontinuous_exact_span"]["recall"],
            0.571429,
        )
        self.assertEqual(
            result["exposed_test"]["gap_dependency"]["unseen_exact_span_recall"]["value"],
            0.0,
        )

    def test_core_mwe_evidence_keeps_occurrence_and_fine_sense_decisions_separate(self):
        resources = {item["id"]: item for item in CORE_MWE_EVIDENCE["resources"]}
        self.assertEqual(
            set(resources),
            {
                "streusle_v5",
                "magpie",
                "semeval_2022_task2",
                "mweaswsd",
                "raganato_wsd_framework_mwe_verb_slice",
            },
        )
        for resource in resources.values():
            self.assertTrue(
                set(CORE_MWE_EVIDENCE["dimensions"]).issubset(resource)
            )
        decisions = CORE_MWE_EVIDENCE["decisions"]
        self.assertEqual(decisions["occurrence_evaluation"]["state"], "go_with_limits")
        self.assertEqual(
            decisions["occurrence_evaluation"]["admitted_resource_ids"],
            ["streusle_v5"],
        )
        self.assertEqual(
            decisions["contextual_sense_evaluation"]["state"],
            "go_with_severe_limits_smoke_test_only",
        )
        self.assertEqual(
            decisions["contextual_sense_evaluation"]["admitted_resource_ids"],
            ["raganato_wsd_framework_mwe_verb_slice"],
        )
        manual = resources["mweaswsd"]["manual_annotation_observation"]
        self.assertEqual(manual["raw_rows"], 1296)
        self.assertEqual(manual["take_in_candidate_rows"], 5)
        self.assertEqual(manual["take_in_wordnet_sense_rows"], 1)
        self.assertEqual(
            resources["mweaswsd"]["admission"],
            "reject_as_contextual_fine_sense_validation_benchmark_external_development_only",
        )
        self.assertTrue(
            all(CORE_MWE_EVIDENCE["prohibited_actions_at_this_gate"].values())
        )

    def test_wsd_mwe_slice_is_only_a_conditional_smoke_test(self):
        audit = WSD_MWE_SENSE_AUDIT
        self.assertTrue(audit["bounded_search"]["search_complete"])
        self.assertEqual(
            audit["decision"]["state"],
            "go_with_severe_limits_external_conditional_sense_smoke_test",
        )
        observations = audit["computed_observations"]
        self.assertFalse(
            observations["framework_rights_artifact"]["license_file_present"]
        )
        self.assertEqual(
            observations["semcor_multiword_verbs"]["take_in"]["observed_senses"],
            8,
        )
        selected = observations["evaluation_multiword_verbs"][
            "admissible_candidate_polysemy_slice"
        ]
        self.assertEqual((selected["rows"], selected["types"]), (23, 18))
        self.assertEqual(
            (selected["development_rows"], selected["source_test_rows"]), (6, 17)
        )
        self.assertIn("not_blinded", selected["source_test_status"])
        self.assertNotIn("V.VID", selected["types_by_streusle_category"])
        self.assertEqual(
            observations["evaluation_multiword_verbs"]["take_in_rows"], 0
        )

    def test_mweaswsd_reuse_audit_rejects_validation_without_blaming_rights(self):
        audit = MWEASWSD_REUSE_AUDIT
        self.assertEqual(
            audit["decision"]["state"],
            "reject_as_contextual_fine_sense_validation_benchmark",
        )
        self.assertFalse(audit["decision"]["rights_blocking"])
        self.assertTrue(audit["decision"]["quality_and_construct_blocking"])
        self.assertIsNone(audit["decision"]["immutable_split_proposal"])
        self.assertEqual(
            audit["target_scope_audit"]["directly_category_confirmed_vpc_vid_rows"],
            0,
        )

        observations = audit["computed_observations"]
        manual = observations["manual"]
        self.assertEqual(manual["unique_accepted_sentence_span_keys"], 1159)
        self.assertEqual(manual["conflicting_duplicate_accepted_keys"], 5)
        self.assertEqual(
            manual["verb_form_proxy"]["types_with_multiple_observed_positive_senses"],
            7,
        )
        self.assertEqual(manual["take_in"]["observed_positive_sense_count"], 1)

        augmented = observations["augmented"]
        self.assertEqual(augmented["inferred_application_collisions_in_published_artifact"], 0)
        self.assertEqual(augmented["paper_table_2_comparison"]["difference"], 3)
        self.assertEqual(
            augmented["paper_table_2_comparison"]["difference_negative"], 917
        )

        mapping = observations["mapping"]
        self.assertEqual(
            mapping["verb_lossless_exact_same_ili"],
            {"numerator": 125, "denominator": 136},
        )
        self.assertEqual(
            mapping["verb_exact_sense_id"],
            {"numerator": 127, "denominator": 136},
        )
        self.assertEqual(mapping["verb_positive_rows"]["exact_ili_mismatch"], 2)

    def test_reference_profile_template_keeps_channels_and_evidence_separate(self):
        self.assertEqual(
            REFERENCE_TEMPLATE["allowed_values"]["coverage_channel"],
            ["word", "mwe_form", "mwe_sense"],
        )
        self.assertIn(
            "ranked_inventory", REFERENCE_TEMPLATE["allowed_values"]["reference_function"]
        )
        self.assertIn("local_only", REFERENCE_TEMPLATE["allowed_values"]["profile_status"])
        manifest = REFERENCE_TEMPLATE["manifest_template"]
        self.assertEqual(set(manifest), set(REFERENCE_TEMPLATE["required_sections"]))
        self.assertIsNone(manifest["construct"]["coverage_channel"])
        self.assertIsNone(manifest["source"]["artifact_sha256"])
        self.assertIsNone(manifest["measurement"]["denominator_definition"])
        self.assertIsNone(manifest["rights"]["browser_delivery_permitted"])
        self.assertIsNone(manifest["rights"]["local_user_import_permitted"])
        self.assertIn(
            "no profile becomes a silent universal default; every result exports its profile identity and limitations",
            REFERENCE_TEMPLATE["admission_rules"],
        )

    def test_manifest_describes_three_reviewed_scenarios(self):
        self.assertEqual(set(SAMPLES), {"samples_version", "comparison_sets", "mwe_examples"})
        self.assertEqual(SAMPLES["samples_version"], "0.4.0-probe")
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
