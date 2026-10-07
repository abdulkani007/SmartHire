import os
import pandas as pd

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")

def load_resumes():
    path = os.path.join(RAW_DATA_DIR, "UpdatedResumeDataSet.csv")
    return pd.read_csv(path)

def load_naukri_jobs():
    path = os.path.join(RAW_DATA_DIR, "naukri_jobs.csv")
    return pd.read_csv(path)

def load_linkedin_jobs():
    path = os.path.join(RAW_DATA_DIR, "linkedin_postings.csv")
    return pd.read_csv(path)

if __name__ == "__main__":
    print("Testing data loading...")
    df_resumes = load_resumes()
    df_naukri = load_naukri_jobs()
    df_linkedin = load_linkedin_jobs()
    print(f"Resumes shape: {df_resumes.shape}")
    print(f"Naukri shape: {df_naukri.shape}")
    print(f"LinkedIn shape: {df_linkedin.shape}")
