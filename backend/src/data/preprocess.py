"""
SmartHire — Phase 2: Dataset Cleaning & Preprocessing Pipeline
Author: SmartHire ML Team
Description: Preprocessing functions for Resumes, Naukri Jobs, LinkedIn Jobs, and Unified Job Corpus.
"""

import os
import sys
import re
import unicodedata
import pandas as pd

# Force UTF-8 output encoding for Windows compatibility
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "..", "..", "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "..", "data", "processed")

# Raw File Paths
RAW_RESUME_PATH = os.path.join(RAW_DIR, "UpdatedResumeDataSet.csv")
RAW_NAUKRI_PATH = os.path.join(RAW_DIR, "naukri_jobs.csv")
RAW_LINKEDIN_PATH = os.path.join(RAW_DIR, "linkedin_postings.csv")

# Cleaned Output File Paths
CLEANED_RESUME_PATH = os.path.join(PROCESSED_DIR, "resumes_cleaned.csv")
CLEANED_NAUKRI_PATH = os.path.join(PROCESSED_DIR, "naukri_cleaned.csv")
CLEANED_LINKEDIN_PATH = os.path.join(PROCESSED_DIR, "linkedin_cleaned.csv")
UNIFIED_CORPUS_PATH = os.path.join(PROCESSED_DIR, "job_corpus.csv")


def clean_text_general(text) -> str:
    """
    General text cleaning helper:
    - Normalizes unicode accents
    - Replaces newlines, carriage returns, and tabs with single space
    - Collapses multiple consecutive spaces into a single space
    """
    if pd.isna(text) or text is None:
        return ""
    text = str(text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def preprocess_resume_dataset():
    """Phase 2A: Resume Dataset Cleaning"""
    print("=" * 80)
    print("PHASE 2A: RESUME DATASET CLEANING & PREPROCESSING")
    print("=" * 80)

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df_raw = pd.read_csv(RAW_RESUME_PATH)
    rows_before = len(df_raw)

    print(f"1. Rows before cleaning: {rows_before}")

    df_raw["Category"] = df_raw["Category"].astype(str).str.strip()
    df_raw["cleaned_resume"] = df_raw["Resume"].apply(clean_text_general)

    duplicates_before = df_raw.duplicated(subset=["Category", "cleaned_resume"]).sum()
    print(f"2. Duplicate rows found: {duplicates_before}")

    df_cleaned = df_raw.drop_duplicates(subset=["Category", "cleaned_resume"]).reset_index(drop=True)

    expected_cols = ["Category", "Resume", "cleaned_resume"]
    df_final = df_cleaned[expected_cols]
    df_final.to_csv(CLEANED_RESUME_PATH, index=False)

    print(f"3. Rows after cleaning: {len(df_final)}")
    print(f"4. Cleaned Resume saved to: {CLEANED_RESUME_PATH}")
    print("=" * 80 + "\n")


def preprocess_naukri_dataset():
    """Phase 2B: Naukri Job Dataset Cleaning & Standardizing"""
    print("=" * 80)
    print("PHASE 2B: NAUKRI JOB DATASET CLEANING & PREPROCESSING")
    print("=" * 80)

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df_raw = pd.read_csv(RAW_NAUKRI_PATH)
    rows_before = len(df_raw)

    print(f"1. Rows before cleaning: {rows_before:,}")

    metadata_cols = ["Uniq Id", "Crawl Timestamp"]
    df_work = df_raw.drop(columns=[c for c in metadata_cols if c in df_raw.columns])

    for col in df_work.columns:
        df_work[col] = df_work[col].apply(clean_text_general)

    def resolve_title(row):
        t = row["Job Title"]
        r = row["Role"]
        if t:
            return t
        if r:
            return r
        return "Unknown Job Title"

    title_series = df_work.apply(resolve_title, axis=1)
    company_series = "Naukri Listing"
    location_series = df_work["Location"].apply(lambda x: x if x else "Unknown")
    skills_series = df_work["Key Skills"].apply(lambda x: x if x else "Unknown")
    experience_series = df_work["Job Experience Required"].apply(lambda x: x if x else "Not Specified")
    salary_series = df_work["Job Salary"].apply(lambda x: x if (x and x.lower() != "nan") else "Not Disclosed")
    source_series = "Naukri"

    def build_description(row):
        parts = []
        fields = ["Job Title", "Key Skills", "Role Category", "Functional Area", "Industry", "Role"]
        for field in fields:
            val = row[field]
            if val and val not in parts:
                parts.append(val)
        return " | ".join(parts) if parts else "No Description Available"

    description_series = df_work.apply(build_description, axis=1)

    df_clean = pd.DataFrame({
        "title": title_series,
        "company": company_series,
        "location": location_series,
        "skills": skills_series,
        "description": description_series,
        "experience": experience_series,
        "salary": salary_series,
        "source": source_series
    })

    df_clean["salary"] = df_clean["salary"].fillna("Not Disclosed")
    df_clean["location"] = df_clean["location"].fillna("Unknown")
    df_clean["skills"] = df_clean["skills"].fillna("Unknown")
    df_clean["title"] = df_clean["title"].fillna("Unknown Job Title")

    def build_combined_text(row):
        combined = f"{row['title']} {row['skills']} {row['description']}"
        return re.sub(r"\s+", " ", combined).strip()

    df_clean["combined_text"] = df_clean.apply(build_combined_text, axis=1)

    expected_final_cols = [
        "title", "company", "location", "skills",
        "description", "experience", "salary", "source", "combined_text"
    ]
    df_final = df_clean[expected_final_cols]
    df_final.to_csv(CLEANED_NAUKRI_PATH, index=False)

    print(f"2. Rows after cleaning: {len(df_final):,}")
    print(f"3. Cleaned Naukri dataset saved to: {CLEANED_NAUKRI_PATH}")
    print("=" * 80 + "\n")


def preprocess_linkedin_dataset():
    """Phase 2C: LinkedIn Job Dataset Cleaning & Standardizing"""
    print("=" * 80)
    print("PHASE 2C: LINKEDIN JOB DATASET CLEANING & PREPROCESSING")
    print("=" * 80)

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df_raw = pd.read_csv(RAW_LINKEDIN_PATH)
    rows_before = len(df_raw)

    print(f"1. Rows before cleaning: {rows_before:,}")

    useful_cols = [
        "job_id", "company_name", "title", "description", "location",
        "formatted_experience_level", "normalized_salary", "min_salary", "max_salary", "skills_desc"
    ]
    df_work = df_raw[[c for c in useful_cols if c in df_raw.columns]].copy()

    text_cols = ["company_name", "title", "description", "location", "formatted_experience_level", "skills_desc"]
    for col in text_cols:
        if col in df_work.columns:
            df_work[col] = df_work[col].apply(clean_text_general)

    title_series = df_work["title"].apply(lambda x: x if x else "Unknown Job Title")
    company_series = df_work["company_name"].apply(lambda x: x if x else "Unknown")
    location_series = df_work["location"].apply(lambda x: x if x else "Unknown")
    experience_series = df_work["formatted_experience_level"].apply(lambda x: x if x else "Unknown")
    skills_series = df_work["skills_desc"].apply(lambda x: x if x else "Unknown")
    description_series = df_work["description"].apply(lambda x: x if x else "No Description Available")

    def resolve_salary(row):
        norm = row.get("normalized_salary")
        if pd.notna(norm) and str(norm).strip() != "" and str(norm).lower() != "nan":
            return str(norm)
        min_s = row.get("min_salary")
        max_s = row.get("max_salary")
        if pd.notna(min_s) and pd.notna(max_s):
            return f"{min_s} - {max_s}"
        elif pd.notna(min_s):
            return str(min_s)
        elif pd.notna(max_s):
            return str(max_s)
        return "Not Disclosed"

    salary_series = df_work.apply(resolve_salary, axis=1)
    source_series = "LinkedIn"

    df_clean = pd.DataFrame({
        "title": title_series,
        "company": company_series,
        "location": location_series,
        "skills": skills_series,
        "description": description_series,
        "experience": experience_series,
        "salary": salary_series,
        "source": source_series
    })

    def build_combined_text(row):
        combined = f"{row['title']} {row['skills']} {row['description']}"
        return re.sub(r"\s+", " ", combined).strip()

    df_clean["combined_text"] = df_clean.apply(build_combined_text, axis=1)

    expected_final_cols = [
        "title", "company", "location", "skills",
        "description", "experience", "salary", "source", "combined_text"
    ]
    df_final = df_clean[expected_final_cols]
    df_final.to_csv(CLEANED_LINKEDIN_PATH, index=False)

    print(f"2. Rows after cleaning: {len(df_final):,}")
    print(f"3. Cleaned LinkedIn dataset saved to: {CLEANED_LINKEDIN_PATH}")
    print("=" * 80 + "\n")


def create_unified_job_corpus():
    """Phase 2D: Create Unified Job Corpus (Naukri + LinkedIn)"""
    print("=" * 80)
    print("PHASE 2D: CREATE UNIFIED JOB CORPUS (Naukri + LinkedIn)")
    print("=" * 80)

    # 1. Load cleaned datasets
    print("1️⃣ LOADING CLEANED DATASETS:")
    df_naukri = pd.read_csv(CLEANED_NAUKRI_PATH)
    df_linkedin = pd.read_csv(CLEANED_LINKEDIN_PATH)

    naukri_count = len(df_naukri)
    linkedin_count = len(df_linkedin)
    total_combined_pre = naukri_count + linkedin_count

    print(f"  - Naukri job count: {naukri_count:,}")
    print(f"  - LinkedIn job count: {linkedin_count:,}")
    print(f"  - Total combined rows before deduplication: {total_combined_pre:,}")

    # 2. Verify standardized columns match
    naukri_cols = list(df_naukri.columns)
    linkedin_cols = list(df_linkedin.columns)
    assert naukri_cols == linkedin_cols, f"Column mismatch! Naukri: {naukri_cols}, LinkedIn: {linkedin_cols}"
    print(f"  - Column schemas match: {naukri_cols}")

    # 3. Concatenate row-wise
    df_unified = pd.concat([df_naukri, df_linkedin], ignore_index=True)

    # Fill any NA values in string columns
    for col in df_unified.columns:
        df_unified[col] = df_unified[col].fillna("Unknown")

    # 4. Deduplicate based on title + company + location + combined_text
    dup_subset = ["title", "company", "location", "combined_text"]
    duplicates_found = df_unified.duplicated(subset=dup_subset).sum()
    print("\n2️⃣ DEDUPLICATION METRICS:")
    print(f"  - Rows before deduplication: {len(df_unified):,}")
    print(f"  - Duplicate job postings found: {duplicates_found:,}")

    df_dedup = df_unified.drop_duplicates(subset=dup_subset).reset_index(drop=True)
    rows_after_dedup = len(df_dedup)
    print(f"  - Rows after deduplication: {rows_after_dedup:,}")

    # 5. Generate unique job_id
    df_dedup["job_id"] = [f"JOB_{i+1:06d}" for i in range(rows_after_dedup)]

    # 6. Ensure combined_text is non-empty
    def ensure_combined_text(row):
        c = str(row["combined_text"]).strip()
        if not c or c.lower() == "unknown":
            c = f"{row['title']} {row['skills']} {row['description']}"
        return re.sub(r"\s+", " ", c).strip()

    df_dedup["combined_text"] = df_dedup.apply(ensure_combined_text, axis=1)

    # 7. Final Validation Checks
    print("\n3️⃣ FINAL CORPUS VALIDATION CHECKS:")
    print(f"  - Total final jobs in corpus: {len(df_dedup):,}")
    print(f"  - Duplicate job_id count: {df_dedup['job_id'].duplicated().sum()}")
    print(f"  - Missing values count per column:")
    print(df_dedup.isnull().sum())

    print("\n4️⃣ SOURCE DISTRIBUTION IN UNIFIED CORPUS:")
    source_counts = df_dedup["source"].value_counts()
    print(source_counts.to_string())

    # 8. Save unified job corpus
    expected_order = [
        "job_id", "title", "company", "location", "skills",
        "description", "experience", "salary", "source", "combined_text"
    ]
    df_corpus = df_dedup[expected_order]
    df_corpus.to_csv(UNIFIED_CORPUS_PATH, index=False)

    print("\n5️⃣ UNIFIED JOB CORPUS SAVED SUCCESSFULLY:")
    print(f"  - Output File: {os.path.abspath(UNIFIED_CORPUS_PATH)}")
    print(f"  - Saved File Size: {os.path.getsize(UNIFIED_CORPUS_PATH) / (1024*1024):.2f} MB")
    print(f"  - Columns Saved: {list(df_corpus.columns)}")
    print("=" * 80)


if __name__ == "__main__":
    create_unified_job_corpus()
