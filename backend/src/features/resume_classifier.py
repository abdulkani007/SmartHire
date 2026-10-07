"""
SmartHire — Phase 3A: Resume Category Classification (Supervised ML)
Author: SmartHire ML Team
Description: Train a Classical Machine Learning model (Logistic Regression + TF-IDF)
             to classify resumes into 25 job categories. Save model artifacts and evaluation plots.
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Force UTF-8 encoding for console output on Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

# Define File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))               # .../SmartHire/backend/src/features
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))    # .../SmartHire/backend
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))      # .../SmartHire

CLEANED_RESUME_PATH = os.path.join(BACKEND_DIR, "data", "processed", "resumes_cleaned.csv")
MODELS_DIR = os.path.join(BACKEND_DIR, "models")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

VECTORIZER_PATH = os.path.join(MODELS_DIR, "resume_tfidf_vectorizer.joblib")
CLASSIFIER_PATH = os.path.join(MODELS_DIR, "resume_classifier.joblib")
CONFUSION_MATRIX_PATH = os.path.join(REPORTS_DIR, "resume_classifier_confusion_matrix.png")


def train_resume_classifier():
    try:
        print("=" * 80)
        print("PHASE 3A: RESUME CLASSIFIER MODEL TRAINING")
        print("=" * 80)

        # 1. Ensure output directories exist
        os.makedirs(MODELS_DIR, exist_ok=True)
        os.makedirs(REPORTS_DIR, exist_ok=True)

        # 2. Check if cleaned resume dataset exists
        if not os.path.exists(CLEANED_RESUME_PATH):
            raise FileNotFoundError(f"Cleaned dataset not found at: {CLEANED_RESUME_PATH}")

        # 3. Load Dataset
        df = pd.read_csv(CLEANED_RESUME_PATH)
        print(f"Loaded dataset from: {os.path.abspath(CLEANED_RESUME_PATH)}")

        # 4. Data Validation
        missing_count = df["cleaned_resume"].isnull().sum() + df["Category"].isnull().sum()
        total_samples = len(df)
        categories = df["Category"].unique()
        num_categories = len(categories)

        if missing_count > 0:
            print(f"Warning: Found {missing_count} missing values. Dropping missing entries...")
            df = df.dropna(subset=["cleaned_resume", "Category"]).reset_index(drop=True)

        X = df["cleaned_resume"]
        y = df["Category"]

        # 5. Stratified Train-Test Split (80% Train, 20% Test)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )

        train_samples = len(X_train)
        test_samples = len(X_test)

        # 6. Create & Fit TF-IDF Vectorizer ONLY on Training Data
        tfidf = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            max_features=10000
        )

        X_train_tfidf = tfidf.fit_transform(X_train)
        X_test_tfidf = tfidf.transform(X_test)
        vocab_size = len(tfidf.vocabulary_)

        # 7. Train Logistic Regression Classifier
        classifier = LogisticRegression(max_iter=2000, random_state=42)
        classifier.fit(X_train_tfidf, y_train)

        # 8. Predict on Test Set
        y_pred = classifier.predict(X_test_tfidf)

        # 9. Compute Evaluation Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision_macro = precision_score(y_test, y_pred, average="macro", zero_division=0)
        precision_weighted = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        recall_macro = recall_score(y_test, y_pred, average="macro", zero_division=0)
        recall_weighted = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
        f1_weighted = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        clf_report = classification_report(y_test, y_pred, zero_division=0)
        labels = sorted(list(set(y_test)))
        cm = confusion_matrix(y_test, y_pred, labels=labels)

        # 10. Save Model Artifacts
        joblib.dump(tfidf, VECTORIZER_PATH)
        joblib.dump(classifier, CLASSIFIER_PATH)

        # 11. Plot & Save Confusion Matrix
        plt.figure(figsize=(14, 10))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=labels,
            yticklabels=labels
        )
        plt.title("Resume Category Classifier — Confusion Matrix", fontsize=14, fontweight="bold")
        plt.xlabel("Predicted Category", fontsize=12)
        plt.ylabel("Actual Category", fontsize=12)
        plt.xticks(rotation=90)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(CONFUSION_MATRIX_PATH, dpi=300)
        plt.close()

        # 12. Print Final Formatted Evaluation Summary
        print("\n" + "=" * 50)
        print("PHASE 3A: RESUME CLASSIFIER")
        print("=" * 50)
        print(f"Dataset size: {total_samples}")
        print(f"Number of categories: {num_categories}")
        print(f"Training samples: {train_samples}")
        print(f"Testing samples: {test_samples}")
        print(f"TF-IDF vocabulary size: {vocab_size}")
        print("-" * 50)
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision_weighted:.4f} (weighted) | {precision_macro:.4f} (macro)")
        print(f"Recall: {recall_weighted:.4f} (weighted) | {recall_macro:.4f} (macro)")
        print(f"F1-score: {f1_weighted:.4f} (weighted) | {f1_macro:.4f} (macro)")
        print("-" * 50)
        print("\nCLASSIFICATION REPORT:")
        print(clf_report)
        print("=" * 50)

        print("\nPHASE 3A COMPLETE")
        print("\nGenerated model files:")
        print(f"  1. {os.path.abspath(VECTORIZER_PATH)}")
        print(f"  2. {os.path.abspath(CLASSIFIER_PATH)}")
        print("\nGenerated report files:")
        print(f"  1. {os.path.abspath(CONFUSION_MATRIX_PATH)}")
        print("=" * 50)

    except Exception as e:
        print(f"Error during Phase 3A execution: {e}", file=sys.stderr)
        raise e


if __name__ == "__main__":
    train_resume_classifier()
