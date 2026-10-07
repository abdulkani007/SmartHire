"""
SmartHire — ML Service Layer (Singleton Pattern)
Author: SmartHire ML Team
Description: Wraps Phase 3 ML models (Classifier, Recommender, Skill Gap) into reusable service functions.
             Loads heavy TF-IDF artifacts only once when initialized.
"""

import os
import sys
import pandas as pd
import joblib

# Force UTF-8 encoding for Windows compatibility
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))               # .../SmartHire/backend/src/services
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))    # .../SmartHire/backend

sys.path.append(os.path.join(BACKEND_DIR, "src"))

from features.job_recommender import JobRecommender
from features.skill_gap import generate_skill_gap as phase_3c_skill_gap, clean_text_normalization

MODELS_DIR = os.path.join(BACKEND_DIR, "models")
RESUME_VEC_PATH = os.path.join(MODELS_DIR, "resume_tfidf_vectorizer.joblib")
RESUME_CLF_PATH = os.path.join(MODELS_DIR, "resume_classifier.joblib")


class MLService:
    """Singleton ML Service managing model loading and execution."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def initialize(self):
        if self._initialized:
            return

        print("Initializing ML Service (loading Phase 3 artifacts)...")

        # 1. Load Resume Classifier Artifacts
        if not os.path.exists(RESUME_VEC_PATH) or not os.path.exists(RESUME_CLF_PATH):
            raise FileNotFoundError("Resume Classifier artifacts missing in backend/models/")

        self.resume_vectorizer = joblib.load(RESUME_VEC_PATH)
        self.resume_classifier = joblib.load(RESUME_CLF_PATH)

        # 2. Initialize and load Job Recommender Engine (fits/loads 50k TF-IDF matrix once)
        self.recommender = JobRecommender()
        self.recommender.fit_or_load(force_refit=False)

        self._initialized = True
        print("ML Service successfully initialized!")

    def predict_category(self, resume_text: str) -> str:
        """Predicts job category for candidate resume text."""
        if not self._initialized:
            self.initialize()

        cleaned_resume = clean_text_normalization(resume_text)
        if not cleaned_resume:
            return "Unknown"

        tfidf_vec = self.resume_vectorizer.transform([cleaned_resume])
        predicted_cat = self.resume_classifier.predict(tfidf_vec)[0]
        return str(predicted_cat)

    def recommend_jobs(self, resume_text: str, top_n: int = 10) -> list:
        """Recommends top_n matching jobs for candidate resume text."""
        if not self._initialized:
            self.initialize()

        df_recs = self.recommender.recommend_jobs(resume_text, top_n=top_n)
        if df_recs.empty:
            return []

        # Convert recommendations dataframe to list of dictionaries
        recs_list = df_recs.to_dict(orient="records")
        return recs_list

    def generate_skill_gap(self, resume_text: str, target_category: str = None, top_n_skills: int = 20) -> dict:
        """Generates Skill Gap Analysis report."""
        if not self._initialized:
            self.initialize()

        report = phase_3c_skill_gap(
            resume_text=resume_text,
            target_category=target_category,
            top_n_skills=top_n_skills
        )
        return report


# Global instance
ml_service = MLService()
