"""
SmartHire — Phase 3B: Content-Based Job Recommendation Engine (Unsupervised ML)
Author: SmartHire ML Team
Description: Build a TF-IDF + Cosine Similarity recommendation engine on the Job Corpus.
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

    def _get_fallback_corpus(self) -> pd.DataFrame:
        """Returns a default corpus dataframe across major job categories if raw CSV is absent."""
        seed_jobs = [
            {
                "job_id": "JOB_SEED_001",
                "title": "Senior Data Scientist & ML Engineer",
                "company": "Tech Corp",
                "location": "Remote / Bengaluru",
                "skills": "Python | Machine Learning | PyTorch | TensorFlow | SQL | Scikit-learn | MLOps | Pandas",
                "description": "Building end-to-end Machine Learning pipelines, NLP models, and predictive algorithms.",
                "experience": "3 - 7 yrs",
                "salary": "15,00,000 - 30,00,000 PA",
                "source": "SmartHire Index",
                "combined_text": "Senior Data Scientist & ML Engineer Tech Corp Python Machine Learning PyTorch TensorFlow SQL Scikit-learn MLOps Pandas"
            },
            {
                "job_id": "JOB_SEED_002",
                "title": "Senior Frontend Developer (React & TypeScript)",
                "company": "UI Labs",
                "location": "Remote / Mumbai",
                "skills": "React.js | TypeScript | Next.js | Tailwind CSS | HTML5 | JavaScript | Redux | Webpack",
                "description": "Architecting high-performance modern web applications with React and TypeScript.",
                "experience": "2 - 6 yrs",
                "salary": "12,00,000 - 24,00,000 PA",
                "source": "SmartHire Index",
                "combined_text": "Senior Frontend Developer React TypeScript UI Labs React.js Next.js Tailwind CSS HTML5 JavaScript Redux Webpack"
            },
            {
                "job_id": "JOB_SEED_003",
                "title": "Full Stack Software Engineer",
                "company": "Cloud Systems",
                "location": "Bengaluru / Hyderabad",
                "skills": "Java | Spring Boot | Python | Node.js | PostgreSQL | MongoDB | Docker | AWS | REST APIs",
                "description": "Designing microservices backend APIs and responsive frontend interfaces.",
                "experience": "2 - 5 yrs",
                "salary": "10,00,000 - 20,00,000 PA",
                "source": "SmartHire Index",
                "combined_text": "Full Stack Software Engineer Cloud Systems Java Spring Boot Python Node.js PostgreSQL MongoDB Docker AWS REST APIs"
            },
            {
                "job_id": "JOB_SEED_004",
                "title": "DevOps & Cloud Infrastructure Engineer",
                "company": "DevOps Global",
                "location": "Remote / Pune",
                "skills": "Kubernetes | Docker | AWS | Terraform | CI/CD | Linux | Bash | Python | Cloud Security",
                "description": "Managing automated CI/CD deployment pipelines, cloud infrastructure, and Kubernetes clusters.",
                "experience": "3 - 8 yrs",
                "salary": "14,00,000 - 28,00,000 PA",
                "source": "SmartHire Index",
                "combined_text": "DevOps & Cloud Infrastructure Engineer DevOps Global Kubernetes Docker AWS Terraform CI/CD Linux Bash Python Cloud Security"
            },
            {
                "job_id": "JOB_SEED_005",
                "title": "Data Analyst & Business Intelligence Specialist",
                "company": "Analytics Insights",
                "location": "Gurugram / Delhi",
                "skills": "SQL | Tableau | Power BI | Excel | Python | Data Analysis | ETL | Statistics",
                "description": "Creating executive BI dashboards and analyzing large dataset trends to drive business growth.",
                "experience": "1 - 4 yrs",
                "salary": "7,00,000 - 14,00,000 PA",
                "source": "SmartHire Index",
                "combined_text": "Data Analyst & Business Intelligence Specialist Analytics Insights SQL Tableau Power BI Excel Python Data Analysis ETL Statistics"
            }
        ]
        return pd.DataFrame(seed_jobs)

    def fit_or_load(self, force_refit=False):
        """Loads corpus and either fits TF-IDF vectorizer or loads saved joblib artifacts."""
        os.makedirs(self.models_dir, exist_ok=True)

        if os.path.exists(self.corpus_path):
            print(f"Loading Job Corpus from: {os.path.abspath(self.corpus_path)}...")
            self.df_corpus = pd.read_csv(self.corpus_path)
        else:
            print("Job Corpus CSV not found. Loading seed job index...")
            self.df_corpus = self._get_fallback_corpus()

        # Validate Corpus Columns
        required_cols = [
            "job_id", "title", "company", "location", "skills",
            "description", "experience", "salary", "source", "combined_text"
        ]
        for col in required_cols:
            if col not in self.df_corpus.columns:
                self.df_corpus[col] = "Unknown"

        # Ensure no NA in combined_text
        self.df_corpus["combined_text"] = self.df_corpus["combined_text"].fillna("Unknown")

        # Load existing artifacts if available
        if (
            not force_refit
            and os.path.exists(JOB_VECTORIZER_PATH)
            and os.path.exists(JOB_MATRIX_PATH)
        ):
            print("Loading pre-trained Job TF-IDF Vectorizer and Matrix artifacts...")
            self.vectorizer = joblib.load(JOB_VECTORIZER_PATH)
            self.tfidf_matrix = joblib.load(JOB_MATRIX_PATH)
            print("Loaded TF-IDF artifacts successfully.")
        elif (
            not force_refit
            and os.path.exists(JOB_VECTORIZER_PATH)
        ):
            print("Loading pre-trained Job TF-IDF Vectorizer and transforming Corpus...")
            self.vectorizer = joblib.load(JOB_VECTORIZER_PATH)
            self.tfidf_matrix = self.vectorizer.transform(self.df_corpus["combined_text"])
            print("Computed TF-IDF Matrix successfully.")
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

            # Save vectorizer artifact
            try:
                print(f"Saving TF-IDF Vectorizer to: {JOB_VECTORIZER_PATH}")
                joblib.dump(self.vectorizer, JOB_VECTORIZER_PATH)
            except Exception as e:
                print(f"Warning: Could not save vectorizer artifact: {e}")

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

        # 5. Extract top matching valid jobs
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
