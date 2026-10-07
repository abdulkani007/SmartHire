"""
SmartHire — Model Artifacts Rebuild Script (Scikit-learn 1.9.1)
Author: SmartHire ML Team
Description: Regenerates all 4 ML artifacts in scikit-learn 1.9.1 to ensure zero InconsistentVersionWarning logs.
"""

import os
import sys
import warnings
import pandas as pd
import numpy as np
import joblib

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import linear_kernel

# Force UTF-8 encoding for console output on Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))               # .../SmartHire/backend/src/models
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))    # .../SmartHire/backend

RESUMES_PATH = os.path.join(BACKEND_DIR, "data", "processed", "resumes_cleaned.csv")
CORPUS_PATH = os.path.join(BACKEND_DIR, "data", "processed", "job_corpus.csv")
MODELS_DIR = os.path.join(BACKEND_DIR, "models")

RESUME_VEC_PATH = os.path.join(MODELS_DIR, "resume_tfidf_vectorizer.joblib")
RESUME_CLF_PATH = os.path.join(MODELS_DIR, "resume_classifier.joblib")
JOB_VEC_PATH = os.path.join(MODELS_DIR, "job_tfidf_vectorizer.joblib")
JOB_MAT_PATH = os.path.join(MODELS_DIR, "job_tfidf_matrix.joblib")


def rebuild_artifacts():
    print("=" * 80)
    print("SCIKIT-LEARN ARTIFACT REBUILD (VERSION COMPATIBILITY)")
    print("=" * 80)

    # 1. Print Environment Info
    py_version = sys.version.split()[0]
    skl_version = sklearn.__version__
    print(f"Current Python version:       {py_version}")
    print(f"Current scikit-learn version: {skl_version}")
    print("=" * 80)

    os.makedirs(MODELS_DIR, exist_ok=True)

    # -------------------------------------------------------------
    # STEP 1: Regenerate Resume Classifier Artifacts
    # -------------------------------------------------------------
    print("\n1️⃣ Regenerating Resume Classifier Artifacts (scikit-learn 1.9.1)...")
    df_resumes = pd.read_csv(RESUMES_PATH)
    X_res = df_resumes["cleaned_resume"]
    y_res = df_resumes["Category"]

    X_train, X_test, y_train, y_test = train_test_split(
        X_res, y_res,
        test_size=0.20,
        random_state=42,
        stratify=y_res
    )

    resume_tfidf = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=10000
    )
    X_train_tfidf = resume_tfidf.fit_transform(X_train)

    resume_clf = LogisticRegression(max_iter=2000, random_state=42)
    resume_clf.fit(X_train_tfidf, y_train)

    joblib.dump(resume_tfidf, RESUME_VEC_PATH)
    joblib.dump(resume_clf, RESUME_CLF_PATH)
    print(f"  - Saved: {os.path.abspath(RESUME_VEC_PATH)}")
    print(f"  - Saved: {os.path.abspath(RESUME_CLF_PATH)}")

    # -------------------------------------------------------------
    # STEP 2: Regenerate Job Recommender Artifacts
    # -------------------------------------------------------------
    print("\n2️⃣ Regenerating Job Recommender Artifacts (scikit-learn 1.9.1)...")
    df_corpus = pd.read_csv(CORPUS_PATH)
    job_text = df_corpus["combined_text"].fillna("Unknown")

    job_tfidf = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=50000
    )
    job_matrix = job_tfidf.fit_transform(job_text)

    joblib.dump(job_tfidf, JOB_VEC_PATH)
    joblib.dump(job_matrix, JOB_MAT_PATH)
    print(f"  - Saved: {os.path.abspath(JOB_VEC_PATH)}")
    print(f"  - Saved: {os.path.abspath(JOB_MAT_PATH)}")

    # -------------------------------------------------------------
    # STEP 3: Artifact Reload Test & Warning Checks
    # -------------------------------------------------------------
    print("\n3️⃣ Verifying Artifact Reloading without Warnings...")
    warning_caught = False

    with warnings.catch_warnings(record=True) as w_list:
        warnings.simplefilter("always")
        
        loaded_res_vec = joblib.load(RESUME_VEC_PATH)
        loaded_res_clf = joblib.load(RESUME_CLF_PATH)
        loaded_job_vec = joblib.load(JOB_VEC_PATH)
        loaded_job_mat = joblib.load(JOB_MAT_PATH)

        for w in w_list:
            if "InconsistentVersionWarning" in str(w.category):
                warning_caught = True
                print(f"WARNING DETECTED: {w.message}")

    reload_passed = not warning_caught
    print(f"  - Reload Successful: True")
    print(f"  - Warning-Free Reload: {reload_passed}")

    # -------------------------------------------------------------
    # STEP 4: Smoke Test
    # -------------------------------------------------------------
    sample_resume = (
        "Python developer with experience in Python, Pandas, NumPy, SQL, "
        "machine learning and data analysis."
    )

    # Resume Classifier Smoke Test
    sample_tfidf = loaded_res_vec.transform([sample_resume])
    pred_category = loaded_res_clf.predict(sample_tfidf)[0]

    # Job Recommender Smoke Test
    sample_job_tfidf = loaded_job_vec.transform([sample_resume])
    sim_scores = linear_kernel(sample_job_tfidf, loaded_job_mat).flatten()
    top_3_idx = np.argsort(sim_scores)[::-1][:3]

    top_3_jobs = df_corpus.iloc[top_3_idx].copy()
    top_3_jobs["similarity_score"] = sim_scores[top_3_idx]

    clf_smoke_passed = bool(pred_category)
    rec_smoke_passed = len(top_3_jobs) == 3

    print("\n4️⃣ SMOKE TEST RESULTS:")
    print(f"  - Sample Resume: '{sample_resume[:60]}...'")
    print(f"  - Predicted Category: {pred_category}")
    print("\n  - Top 3 Job Recommendations:")
    for idx, row in top_3_jobs.iterrows():
        print(f"    * [{row['job_id']}] {row['title']} | {row['company']} | Score: {row['similarity_score']:.4f}")

    # -------------------------------------------------------------
    # STEP 5: Final Output
    # -------------------------------------------------------------
    print("\n========================================")
    print("SCIKIT-LEARN ARTIFACT REBUILD COMPLETE")
    print("========================================")
    print(f"\nEnvironment:")
    print(f"scikit-learn: {skl_version}")

    print("\nRegenerated:")
    print(f"1. {os.path.abspath(RESUME_VEC_PATH)}")
    print(f"2. {os.path.abspath(RESUME_CLF_PATH)}")
    print(f"3. {os.path.abspath(JOB_VEC_PATH)}")
    print(f"4. {os.path.abspath(JOB_MAT_PATH)}")

    print("\nArtifact reload test:")
    print("PASSED" if reload_passed else "FAILED")

    print("\nWarning-free reload:")
    print("PASSED" if reload_passed else "FAILED")

    print("\nResume classifier smoke test:")
    print("PASSED" if clf_smoke_passed else "FAILED")

    print("\nJob recommender smoke test:")
    print("PASSED" if rec_smoke_passed else "FAILED")
    print("=" * 80)


if __name__ == "__main__":
    rebuild_artifacts()
