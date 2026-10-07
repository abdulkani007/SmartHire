"""
SmartHire — Phase 1: Dataset Inspection
Author: SmartHire ML Team
Description: Inspect raw CSV datasets inside backend/data/raw/ without applying transformations.
"""

import os
import sys
import pandas as pd

# Force UTF-8 encoding for standard output on Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")

def run_inspection():
    csv_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.csv')]
    print("=" * 80)
    print(f"DETECTED {len(csv_files)} CSV FILES IN backend/data/raw/:")
    for f in sorted(csv_files):
        print(f"  - {f}")
    print("=" * 80)

    for filename in sorted(csv_files):
        filepath = os.path.join(RAW_DATA_DIR, filename)
        print("\n" + "=" * 80)
        print(f"DATASET FILE: {filename}")
        print("=" * 80)

        df = pd.read_csv(filepath)

        print("\n[1] SHAPE (Rows, Columns):")
        print(f"Rows: {df.shape[0]:,}, Columns: {df.shape[1]}")

        print("\n[2] COLUMN NAMES:")
        print(list(df.columns))

        print("\n[3] FIRST 5 ROWS:")
        # Truncate text representation for clean output
        print(df.head(5).to_string(max_colwidth=80))

        print("\n[4] DATA TYPES & MEMORY INFO (df.info()):")
        df.info(verbose=True, show_counts=True)

        print("\n[5] MISSING VALUES COUNT (df.isnull().sum()):")
        null_series = df.isnull().sum()
        null_pct = (null_series / len(df)) * 100
        null_df = pd.DataFrame({"Null Count": null_series, "Percentage (%)": null_pct})
        print(null_df[null_df["Null Count"] > 0] if (null_series > 0).any() else "No null values found!")

        print("\n[6] DUPLICATE ROWS COUNT (df.duplicated().sum()):")
        print(f"Total Exact Duplicate Rows: {df.duplicated().sum()}")

        print("\n[7] COLUMN SUMMARY STATISTICS:")
        summary = []
        for col in df.columns:
            summary.append({
                "Column": col,
                "Dtype": str(df[col].dtype),
                "Non-Null Count": df[col].count(),
                "Unique Values": df[col].nunique(dropna=True),
                "Sample Entry": str(df[col].dropna().iloc[0])[:60] if not df[col].dropna().empty else "N/A"
            })
        print(pd.DataFrame(summary).to_string(index=False))

        print("=" * 80)

if __name__ == "__main__":
    run_inspection()
