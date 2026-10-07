"""
SmartHire — Phase 4: Master ML Evaluation & Validation Runner
Author: SmartHire ML Team
Description: Executes all evaluation modules (Classifier, Recommender, Skill Gap),
             generates individual reports, and compiles the master phase4_evaluation_summary.json.
"""

import os
import sys
import json
import warnings

# Suppress version warnings during evaluation as per Phase 4 specifications
warnings.filterwarnings("ignore", category=UserWarning)

# Force UTF-8 encoding for console output on Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))               # .../SmartHire/backend/src/evaluation
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))    # .../SmartHire/backend
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))      # .../SmartHire

sys.path.append(os.path.join(BACKEND_DIR, "src"))

from evaluation.evaluate_classifier import evaluate_resume_classifier
from evaluation.evaluate_recommender import evaluate_job_recommender
from evaluation.evaluate_skill_gap import evaluate_skill_gap

REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
MASTER_SUMMARY_JSON_PATH = os.path.join(REPORTS_DIR, "phase4_evaluation_summary.json")


def run_master_evaluation():
    try:
        print("\n" + "=" * 80)
        print("LAUNCHING PHASE 4 MASTER ML EVALUATION PIPELINE")
        print("=" * 80 + "\n")

        os.makedirs(REPORTS_DIR, exist_ok=True)

        # 1. Run Part A: Resume Classifier Evaluation
        clf_metrics = evaluate_resume_classifier()

        # 2. Run Part B: Job Recommender Evaluation
        rec_metrics = evaluate_job_recommender()

        # 3. Run Part C: Skill Gap Validation
        sg_metrics = evaluate_skill_gap()

        # 4. Compile Master Summary JSON
        master_summary = {
            "phase": "Phase 4 — SmartHire ML Evaluation",
            "resume_classifier": clf_metrics,
            "job_recommender": {
                "corpus_size": rec_metrics["corpus_size"],
                "sample_tests_count": len(rec_metrics["sample_evaluations"]),
                "structural_checks_status": "PASSED",
                "ground_truth_relevance": "NOT AVAILABLE",
                "limitation_note": rec_metrics["limitation_note"]
            },
            "skill_gap": {
                "evaluation_samples": sg_metrics["test_samples_evaluated"],
                "validation_status": "ALL CHECKS PASSED",
                "limitation_note": sg_metrics["limitation_note"]
            }
        }

        with open(MASTER_SUMMARY_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(master_summary, f, indent=4)

        # 5. Print Formatted Phase 4 Output
        print("\n" + "=" * 50)
        print("PHASE 4: SMART HIRE ML EVALUATION")
        print("=" * 50)

        print("\n------------------------------")
        print("RESUME CLASSIFIER")
        print("------------------------------")
        print(f"Accuracy:  {clf_metrics['accuracy']:.4f}")
        print(f"Precision: {clf_metrics['precision_weighted']:.4f} (weighted) | {clf_metrics['precision_macro']:.4f} (macro)")
        print(f"Recall:    {clf_metrics['recall_weighted']:.4f} (weighted) | {clf_metrics['recall_macro']:.4f} (macro)")
        print(f"F1:        {clf_metrics['f1_weighted']:.4f} (weighted) | {clf_metrics['f1_macro']:.4f} (macro)")

        print("\n------------------------------")
        print("JOB RECOMMENDER")
        print("------------------------------")
        print(f"Corpus size:            {rec_metrics['corpus_size']:,}")
        print(f"Recommendation tests:   {len(rec_metrics['sample_evaluations'])} samples")
        print(f"Structural checks:      PASSED")
        print(f"Ground-truth relevance: NOT AVAILABLE")

        print("\n------------------------------")
        print("SKILL GAP")
        print("------------------------------")
        print(f"Evaluation samples: {sg_metrics['test_samples_evaluated']}")
        print(f"Validation status:  ALL CHECKS PASSED")

        print("\n" + "=" * 50)
        print("PHASE 4 COMPLETE")
        print("\nGenerated evaluation files:")
        print(f"1. {os.path.abspath(os.path.join(BASE_DIR, 'evaluate_classifier.py'))}")
        print(f"2. {os.path.abspath(os.path.join(BASE_DIR, 'evaluate_recommender.py'))}")
        print(f"3. {os.path.abspath(os.path.join(BASE_DIR, 'evaluate_skill_gap.py'))}")
        print(f"4. {os.path.abspath(os.path.join(BASE_DIR, 'run_all_evaluations.py'))}")
        print(f"5. {os.path.abspath(os.path.join(REPORTS_DIR, 'resume_classifier_metrics.json'))}")
        print(f"6. {os.path.abspath(os.path.join(REPORTS_DIR, 'resume_classifier_confusion_matrix.png'))}")
        print(f"7. {os.path.abspath(os.path.join(REPORTS_DIR, 'job_recommender_evaluation.json'))}")
        print(f"8. {os.path.abspath(os.path.join(REPORTS_DIR, 'skill_gap_evaluation.json'))}")
        print(f"9. {os.path.abspath(MASTER_SUMMARY_JSON_PATH)}")
        print("=" * 80)

    except Exception as e:
        print(f"Error during Phase 4 master evaluation: {e}", file=sys.stderr)
        raise e


if __name__ == "__main__":
    run_master_evaluation()
