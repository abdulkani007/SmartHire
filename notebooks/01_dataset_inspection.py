"""
SmartHire — Step 1: Dataset Inspection
Author: SmartHire Team
Description: Inspect raw datasets (Resumes, Naukri Jobs, LinkedIn Jobs) without applying transformations.
"""

import os
import pandas as pd

# Define paths to raw datasets
RAW_DATA_DIR = os.path.join("..", "data", "raw")
RESUME_PATH = os.path.join(RAW_DATA_DIR, "UpdatedResumeDataSet.csv")
NAUKRI_PATH = os.path.join(RAW_DATA_DIR, "naukri_jobs.csv")
LINKEDIN_PATH = os.path.join(RAW_DATA_DIR, "linkedin_postings.csv")

def inspect_dataset(df, name):
    print("=" * 70)
    print(f" DATASET INSPECTION REPORT: {name}")
    print("=" * 70)
    
    print("\n1. SHAPE (Rows, Columns):")
    print(df.shape)
    
    print("\n2. FIRST 5 ROWS:")
    print(df.head())
    
    print("\n3. COLUMNS LIST:")
    print(list(df.columns))
    
    print("\n4. DATA TYPES & INFO:")
    df.info()
    
    print("\n5. MISSING VALUES COUNT:")
    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df)) * 100
    missing_df = pd.DataFrame({"Missing_Count": missing, "Percentage": missing_pct})
    print(missing_df[missing_df["Missing_Count"] > 0])
    
    print("\n6. DUPLICATE ROWS COUNT:")
    print(df.duplicated().sum())
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    print("Loading datasets...")
    df_resumes = pd.read_csv(RESUME_PATH)
    df_naukri = pd.read_csv(NAUKRI_PATH)
    df_linkedin = pd.read_csv(LINKEDIN_PATH)
    
    inspect_dataset(df_resumes, "1. Resume Dataset")
    inspect_dataset(df_naukri, "2. Naukri Job Listings")
    inspect_dataset(df_linkedin, "3. LinkedIn Job Postings 2023-2024")
