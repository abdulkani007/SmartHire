"""
SmartHire — Phase 4: Skill Gap Validation (Part C)
Author: SmartHire ML Team
Description: Validates structural integrity, skill set disjunction, and score bounds for the Skill Gap module.
             Does not claim to measure subjective real-world career readiness.
"""

import os
import sys
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))               # .../SmartHire/backend/src/evaluation
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))    # .../SmartHire/backend
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))      # .../SmartHire

sys.path.append(os.path.join(BACKEND_DIR, "src"))
from features.skill_gap import generate_skill_gap

REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
SKILL_GAP_EVAL_JSON_PATH = os.path.join(REPORTS_DIR, "skill_gap_evaluation.json")

TEST_RESUMES = {
    "Python / Data Science": (
        "Python developer with experience in Python, Pandas, NumPy, SQL, "
        "machine learning, data analysis and backend development."
    ),
    "Java Developer": (
        "Experienced Java Software Engineer proficient in Java, Spring Boot, Microservices, "
        "Hibernate, REST APIs, Maven and MySQL database management."
    ),
    "Web Developer": (
        "Frontend Web Developer skilled in HTML, CSS, JavaScript, React, Node.js and Web Design."
    )
}


def evaluate_skill_gap():
    print("=" * 80)
    print("PART C: SKILL GAP VALIDATION")
    print("=" * 80)

    os.makedirs(REPORTS_DIR, exist_ok=True)

    validation_results = {
        "limitation_note": (
            "This evaluation validates structural integrity and mathematical correctness. "
            "It does not claim to measure subjective real-world career readiness."
        ),
        "test_samples_evaluated": len(TEST_RESUMES),
        "validation_samples": []
    }

    all_valid = True

    for name, resume_text in TEST_RESUMES.items():
        print(f"\n🔍 Validating Profile: [{name}]")
        report = generate_skill_gap(resume_text, target_category=None, top_n_skills=20)

        target_cat = report["target_category"]
        matched = report["matched_skills"]
        missing = report["missing_skills"]
        match_pct = report["match_percentage"]
        total_skills = report["total_target_skills"]

        # Validation assertions
        check_percentage_bounds = (0.0 <= match_pct <= 100.0)
        check_disjoint = set(matched).isdisjoint(set(missing))
        check_unique_matched = (len(matched) == len(set(matched)))
        check_unique_missing = (len(missing) == len(set(missing)))
        check_sum_totals = (total_skills == (len(matched) + len(missing)))

        sample_passed = (
            check_percentage_bounds and
            check_disjoint and
            check_unique_matched and
            check_unique_missing and
            check_sum_totals
        )

        if not sample_passed:
            all_valid = False

        print(f"   Target Category:      {target_cat}")
        print(f"   Match Percentage:     {match_pct:.2f}%")
        print(f"   Matched Skills Count: {len(matched)}")
        print(f"   Missing Skills Count: {len(missing)}")
        print(f"   Validation Status:    {'PASSED' if sample_passed else 'FAILED'}")

        validation_results["validation_samples"].append({
            "profile_name": name,
            "target_category": target_cat,
            "match_percentage": match_pct,
            "total_target_skills": total_skills,
            "matched_skills_count": len(matched),
            "missing_skills_count": len(missing),
            "validation_checks": {
                "percentage_bounds_valid": check_percentage_bounds,
                "matched_missing_disjoint": check_disjoint,
                "no_duplicate_skills": check_unique_matched and check_unique_missing,
                "total_skills_sum_valid": check_sum_totals
            }
        })

    # Save Validation JSON
    with open(SKILL_GAP_EVAL_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(validation_results, f, indent=4)

    print("\n" + "-" * 50)
    print("SKILL GAP VALIDATION SUMMARY:")
    print(f"  - Evaluation Samples:   {len(TEST_RESUMES)}")
    print(f"  - Overall Status:       {'ALL CHECKS PASSED' if all_valid else 'VALIDATION ISSUES DETECTED'}")
    print(f"Saved Skill Gap Validation to: {os.path.abspath(SKILL_GAP_EVAL_JSON_PATH)}")
    print("=" * 80 + "\n")

    return validation_results


if __name__ == "__main__":
    evaluate_skill_gap()
