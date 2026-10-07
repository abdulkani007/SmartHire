"""
SmartHire — Phase 4: Job Recommender Evaluation (Part B)
Author: SmartHire ML Team
Description: Evaluates structural and qualitative recommendation properties across representative candidate profiles.
             Explicitly records dataset ground-truth limitations without fabricating precision metrics.
"""

import os
import sys
import json
import pandas as pd
import joblib

# Import existing Recommender without modifying Phase 3B code
BASE_DIR = os.path.dirname(os.path.abspath(__file__))               # .../SmartHire/backend/src/evaluation
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))    # .../SmartHire/backend
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))      # .../SmartHire

sys.path.append(os.path.join(BACKEND_DIR, "src"))
from features.job_recommender import JobRecommender

REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
RECOMMENDER_EVAL_JSON_PATH = os.path.join(REPORTS_DIR, "job_recommender_evaluation.json")

SAMPLE_RESUMES = {
    "Python / Data Science": (
        "Python developer with experience in Python, Pandas, NumPy, SQL, "
        "machine learning, data analysis, scikit-learn, and backend development."
    ),
    "Java Developer": (
        "Experienced Java Software Engineer proficient in Java, Spring Boot, Microservices, "
        "Hibernate, REST APIs, Maven, Git, and MySQL database management."
    ),
    "Web Developer": (
        "Frontend and Full Stack Web Developer skilled in HTML5, CSS3, JavaScript, "
        "React.js, Node.js, Express, Tailwind CSS, and Responsive Web Design."
    ),
    "DevOps Engineer": (
        "DevOps Engineer experienced in Linux, Docker, Kubernetes, Jenkins, "
        "CI/CD pipelines, AWS, Ansible, Terraform, and cloud infrastructure automation."
    ),
    "Business Analyst": (
        "Business Analyst skilled in Requirements Gathering, Data Analysis, SQL, "
        "Power BI, Tableau, Excel, Agile/Scrum methodologies, and Process Mapping."
    )
}


def evaluate_job_recommender():
    print("=" * 80)
    print("PART B: JOB RECOMMENDER EVALUATION")
    print("=" * 80)

    os.makedirs(REPORTS_DIR, exist_ok=True)

    # 1. Initialize Recommender and load pre-trained artifacts
    recommender = JobRecommender()
    recommender.fit_or_load(force_refit=False)

    corpus_size = len(recommender.df_corpus)
    vocab_size = len(recommender.vectorizer.vocabulary_)

    evaluation_results = {
        "limitation_note": (
            "Ground-truth relevance labels are not available in the current job corpus, "
            "therefore formal Precision@K cannot be calculated without introducing manually labeled relevance data."
        ),
        "corpus_size": corpus_size,
        "vocab_size": vocab_size,
        "sample_evaluations": []
    }

    all_tests_passed = True

    # 2. Run Evaluation for 5 Representative Sample Resumes
    for profile_name, sample_text in SAMPLE_RESUMES.items():
        print(f"\n🔍 Testing Profile: [{profile_name}]")
        print(f"   Input Snippet: '{sample_text[:75]}...'")

        top_n = 10
        df_recs = recommender.recommend_jobs(sample_text, top_n=top_n)

        # Structural Validation Checks
        check_count = len(df_recs) == top_n
        check_unique_ids = df_recs["job_id"].nunique() == top_n
        check_score_bounds = ((df_recs["similarity_score"] >= 0.0) & (df_recs["similarity_score"] <= 1.0)).all()
        
        scores_list = list(df_recs["similarity_score"])
        check_score_sorted = (scores_list == sorted(scores_list, reverse=True))

        profile_passed = check_count and check_unique_ids and check_score_bounds and check_score_sorted
        if not profile_passed:
            all_tests_passed = False

        print(f"   Structural Validation Passed: {profile_passed}")
        print(f"   - 10 Results Returned: {check_count}")
        print(f"   - Unique Job IDs:       {check_unique_ids}")
        print(f"   - Score Bounds [0, 1]:  {check_score_bounds}")
        print(f"   - Descending Sort:      {check_score_sorted}")

        # Top 3 Recommendations Preview
        top_preview = df_recs[["job_id", "title", "company", "location", "similarity_score"]].head(3).to_dict(orient="records")

        evaluation_results["sample_evaluations"].append({
            "profile_name": profile_name,
            "structural_checks_passed": profile_passed,
            "top_match_score": float(df_recs["similarity_score"].iloc[0]),
            "top_3_recommendations": top_preview
        })

    # Save JSON Report
    with open(RECOMMENDER_EVAL_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(evaluation_results, f, indent=4)

    print("\n" + "-" * 50)
    print("RECOMMENDER EVALUATION SUMMARY:")
    print(f"  - Job Corpus Size:            {corpus_size:,}")
    print(f"  - Profiles Tested:            {len(SAMPLE_RESUMES)}")
    print(f"  - Structural Checks Status:  {'PASSED' if all_tests_passed else 'FAILED'}")
    print(f"  - Ground-truth relevance:     NOT AVAILABLE")
    print(f"Saved Recommender Evaluation to: {os.path.abspath(RECOMMENDER_EVAL_JSON_PATH)}")
    print("=" * 80 + "\n")

    return evaluation_results


if __name__ == "__main__":
    evaluate_job_recommender()
