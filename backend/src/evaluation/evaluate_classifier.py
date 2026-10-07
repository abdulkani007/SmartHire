"""
SmartHire — Phase 4: Resume Classifier Evaluation (Part A)
Author: SmartHire ML Team
Description: Evaluates the existing Phase 3A trained Resume Classifier model against test data.
             Saves evaluation metrics JSON and confusion matrix plot without retraining artifacts.
"""

import os
import sys
import json
import warnings
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Suppress Version Warnings as per Phase 4 requirements
warnings.filterwarnings("ignore", category=UserWarning)

# Force UTF-8 encoding for console output on Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

# Define File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))               # .../SmartHire/backend/src/evaluation
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))    # .../SmartHire/backend
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))      # .../SmartHire

CLEANED_RESUME_PATH = os.path.join(BACKEND_DIR, "data", "processed", "resumes_cleaned.csv")
MODELS_DIR = os.path.join(BACKEND_DIR, "models")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

VECTORIZER_PATH = os.path.join(MODELS_DIR, "resume_tfidf_vectorizer.joblib")
CLASSIFIER_PATH = os.path.join(MODELS_DIR, "resume_classifier.joblib")
METRICS_JSON_PATH = os.path.join(REPORTS_DIR, "resume_classifier_metrics.json")
CONFUSION_MATRIX_PATH = os.path.join(REPORTS_DIR, "resume_classifier_confusion_matrix.png")


def evaluate_resume_classifier():
    print("=" * 80)
    print("PART A: RESUME CLASSIFIER EVALUATION")
    print("=" * 80)

    os.makedirs(REPORTS_DIR, exist_ok=True)

    # 1. Validate raw datasets and model artifacts
    if not os.path.exists(CLEANED_RESUME_PATH):
        raise FileNotFoundError(f"Cleaned dataset not found at: {CLEANED_RESUME_PATH}")
    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(f"Vectorizer artifact not found at: {VECTORIZER_PATH}")
    if not os.path.exists(CLASSIFIER_PATH):
        raise FileNotFoundError(f"Classifier artifact not found at: {CLASSIFIER_PATH}")

    # 2. Load dataset
    df = pd.read_csv(CLEANED_RESUME_PATH)
    X = df["cleaned_resume"]
    y = df["Category"]

    # 3. Stratified Train/Test Split matching Phase 3A setup (test_size=0.20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # 4. Load EXISTING pre-trained model artifacts (DO NOT RETRAIN)
    tfidf = joblib.load(VECTORIZER_PATH)
    classifier = joblib.load(CLASSIFIER_PATH)

    # 5. Transform test data & generate predictions
    X_test_tfidf = tfidf.transform(X_test)
    y_pred = classifier.predict(X_test_tfidf)

    # 6. Calculate Evaluation Metrics
    accuracy = float(accuracy_score(y_test, y_pred))
    precision_weighted = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
    recall_weighted = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
    f1_weighted = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

    precision_macro = float(precision_score(y_test, y_pred, average="macro", zero_division=0))
    recall_macro = float(recall_score(y_test, y_pred, average="macro", zero_division=0))
    f1_macro = float(f1_score(y_test, y_pred, average="macro", zero_division=0))

    clf_report = classification_report(y_test, y_pred, zero_division=0)
    labels = sorted(list(set(y_test)))
    cm = confusion_matrix(y_test, y_pred, labels=labels)

    # 7. Save Metrics JSON
    metrics_dict = {
        "accuracy": round(accuracy, 4),
        "precision_weighted": round(precision_weighted, 4),
        "recall_weighted": round(recall_weighted, 4),
        "f1_weighted": round(f1_weighted, 4),
        "precision_macro": round(precision_macro, 4),
        "recall_macro": round(recall_macro, 4),
        "f1_macro": round(f1_macro, 4)
    }

    with open(METRICS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_dict, f, indent=4)

    # 8. Try plotting confusion matrix plot
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns

        plt.figure(figsize=(14, 10))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
        plt.title("Resume Category Classifier — Confusion Matrix", fontsize=14, fontweight="bold")
        plt.xlabel("Predicted Category", fontsize=12)
        plt.ylabel("Actual Category", fontsize=12)
        plt.xticks(rotation=90)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(CONFUSION_MATRIX_PATH, dpi=300)
        plt.close()
    except Exception as img_err:
        print(f"Plot generation notice: {img_err}")

    # 9. Print Evaluation Summary
    print(f"Total Samples Evaluated: {len(y_test)}")
    print(f"Accuracy:           {accuracy:.4f}")
    print(f"Precision (weighted): {precision_weighted:.4f} | (macro): {precision_macro:.4f}")
    print(f"Recall (weighted):    {recall_weighted:.4f} | (macro): {recall_macro:.4f}")
    print(f"F1-score (weighted):  {f1_weighted:.4f} | (macro): {f1_macro:.4f}")
    print("\nCLASSIFICATION REPORT:")
    print(clf_report)

    print(f"\nSaved Classifier Metrics to: {os.path.abspath(METRICS_JSON_PATH)}")
    print("=" * 80 + "\n")

    return metrics_dict


if __name__ == "__main__":
    evaluate_resume_classifier()
