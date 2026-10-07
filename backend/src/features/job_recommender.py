"""
SmartHire — Phase 3B: Content-Based Job Recommendation Engine (Unsupervised ML)
Author: SmartHire ML Team
Description: Build a TF-IDF + Cosine Similarity recommendation engine on the 148,994+ Job Corpus.
             Reuses sparse matrix representation for instant candidate matching.
"""

import os
import sys
import re
import unicodedata
import pandas as pd
import numpy as np
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Force UTF-8 output encoding for Windows compatibility
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

# Define File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))               # .../SmartHire/backend/src/features
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))    # .../SmartHire/backend
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))      # .../SmartHire

CORPUS_PATH = os.path.join(BACKEND_DIR, "data", "processed", "job_corpus.csv")
MODELS_DIR = os.path.join(BACKEND_DIR, "models")

JOB_VECTORIZER_PATH = os.path.join(MODELS_DIR, "job_tfidf_vectorizer.joblib")
JOB_MATRIX_PATH = os.path.join(MODELS_DIR, "job_tfidf_matrix.joblib")


def clean_text_normalization(text: str) -> str:
    """
    Standard text normalization matching the cleaning pipeline:
    - Normalizes unicode accents
    - Replaces newlines/tabs with space
    - Strips unprintable control symbols while preserving tech terms (C++, C#, .NET, Node.js)
    - Collapses multiple spaces
    """
    if pd.isna(text) or text is None:
        return ""
    text = str(text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"[^\x20-\x7E]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


class JobRecommender:
    """
    Classical Content-Based Filtering Job Recommender.
    """

    def __init__(self, corpus_path=CORPUS_PATH, models_dir=MODELS_DIR):
        self.corpus_path = corpus_path
        self.models_dir = models_dir
        self.df_corpus = None
        self.vectorizer = None
        self.tfidf_matrix = None

    def fit_or_load(self, force_refit=False):
        """Loads corpus and either fits TF-IDF vectorizer or loads saved joblib artifacts."""
        os.makedirs(self.models_dir, exist_ok=True)

        if not os.path.exists(self.corpus_path):
            raise FileNotFoundError(f"Job Corpus dataset not found at: {self.corpus_path}")

        print(f"Loading Job Corpus from: {os.path.abspath(self.corpus_path)}...")
        self.df_corpus = pd.read_csv(self.corpus_path)

        # Validate Corpus Columns & Missing Data
        required_cols = [
            "job_id", "title", "company", "location", "skills",
            "description", "experience", "salary", "source", "combined_text"
        ]
        for col in required_cols:
            if col not in self.df_corpus.columns:
                raise ValueError(f"Missing required column in corpus: {col}")

        # Ensure no NA in combined_text
        self.df_corpus["combined_text"] = self.df_corpus["combined_text"].fillna("Unknown")

        # Load existing artifacts if available and not forcing refit
        if (
            not force_refit
            and os.path.exists(JOB_VECTORIZER_PATH)
            and os.path.exists(JOB_MATRIX_PATH)
        ):
            print("Loading pre-trained Job TF-IDF Vectorizer and Matrix artifacts...")
            self.vectorizer = joblib.load(JOB_VECTORIZER_PATH)
            self.tfidf_matrix = joblib.load(JOB_MATRIX_PATH)
            print("Loaded TF-IDF artifacts successfully.")
        else:
            print("Fitting TF-IDF Vectorizer on Job Corpus combined_text (max_features=50000)...")
            self.vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                max_features=50000
            )

            # Transform into Sparse CSR Matrix
            self.tfidf_matrix = self.vectorizer.fit_transform(self.df_corpus["combined_text"])

            # Save artifacts
            print(f"Saving TF-IDF Vectorizer to: {JOB_VECTORIZER_PATH}")
            joblib.dump(self.vectorizer, JOB_VECTORIZER_PATH)

            print(f"Saving TF-IDF Matrix to: {JOB_MATRIX_PATH}")
            joblib.dump(self.tfidf_matrix, JOB_MATRIX_PATH)

        return self

    def recommend_jobs(self, resume_text: str, top_n: int = 10) -> pd.DataFrame:
        """
        Recommends top N job postings for a given input resume text.
        Returns a DataFrame containing top job details and similarity_score.
        """
        if not resume_text or not str(resume_text).strip():
            raise ValueError("Input resume text cannot be empty.")

        if self.vectorizer is None or self.tfidf_matrix is None or self.df_corpus is None:
            raise RuntimeError("Recommender model is not initialized. Call fit_or_load() first.")

        # 1. Normalize resume text
        cleaned_resume = clean_text_normalization(resume_text)

        # 2. Transform resume using the SAME pre-fitted Job TF-IDF vectorizer
        resume_vector = self.vectorizer.transform([cleaned_resume])

        # 3. Calculate Cosine Similarity via fast sparse dot product (linear_kernel)
        sim_scores = linear_kernel(resume_vector, self.tfidf_matrix).flatten()

        if len(sim_scores) == 0:
            return pd.DataFrame()

        # 4. Rank job indices descending
        sorted_indices = np.argsort(sim_scores)[::-1]

        # 5. Extract top matching valid jobs (filtering out raw dataset error placeholders)
        results = []
        for idx in sorted_indices:
            if len(results) >= top_n:
                break

            row = self.df_corpus.iloc[idx]
            title_str = str(row["title"]).strip()

            # Skip raw dataset error placeholders if present
            if title_str.lower().startswith("error:"):
                continue

            score = float(sim_scores[idx])
            results.append({
                "job_id": row["job_id"],
                "title": title_str,
                "company": row["company"],
                "location": row["location"],
                "skills": row["skills"],
                "experience": row["experience"],
                "salary": row["salary"],
                "source": row["source"],
                "similarity_score": round(score, 4)
            })

        df_recommendations = pd.DataFrame(results)
        return df_recommendations


def run_phase_3b_pipeline():
    try:
        recommender = JobRecommender()
        recommender.fit_or_load(force_refit=False)

        corpus_size = len(recommender.df_corpus)
        vocab_size = len(recommender.vectorizer.vocabulary_)
        matrix_shape = recommender.tfidf_matrix.shape

        print("\n" + "=" * 50)
        print("PHASE 3B: JOB RECOMMENDATION ENGINE")
        print("=" * 50)
        print(f"Job corpus size: {corpus_size:,}")
        print(f"Number of TF-IDF features: {vocab_size:,}")
        print(f"TF-IDF matrix shape: {matrix_shape}")
        print("=" * 50)

        # Sample Candidate Resume for Validation Test
        sample_resume = (
            "Python developer with experience in Python, Pandas, NumPy, SQL, "
            "machine learning, data analysis and backend development."
        )

        print("\nRunning test recommendation for sample candidate resume...")
        top_n = 10
        df_top10 = recommender.recommend_jobs(sample_resume, top_n=top_n)

        # Validation Checks
        assert len(df_top10) == top_n, f"Expected {top_n} recommendations, got {len(df_top10)}"
        assert df_top10["job_id"].nunique() == top_n, "Duplicate job_id detected in recommendations!"
        assert (df_top10["similarity_score"] >= 0.0).all() and (df_top10["similarity_score"] <= 1.0).all(), "Similarity score out of bounds [0, 1]!"

        print("\n" + "=" * 80)
        print("TOP 10 JOB RECOMMENDATIONS")
        print("=" * 80)
        
        df_display = df_top10.copy()
        df_display.insert(0, "Rank", range(1, len(df_display) + 1))
        table_cols = ["Rank", "job_id", "title", "company", "location", "source", "similarity_score"]
        print(df_display[table_cols].to_string(index=False))
        print("=" * 80)

    except Exception as e:
        print(f"Error during Phase 3B execution: {e}", file=sys.stderr)
        raise e


if __name__ == "__main__":
    run_phase_3b_pipeline()
