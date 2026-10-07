"""
SmartHire — Phase 3C: Skill Gap Analysis Module (Data-Driven Skill Matching — Refined)
Author: SmartHire ML Team
Description: Compares candidate resumes against dataset-derived category skill profiles.
             Uses Document-Frequency (DF) ranking and transparent generic-noise filtering.
             Caches dataset, models, and category skill profiles for lightning-fast responses.
"""

import os
import sys
import re
import json
import unicodedata
from collections import Counter
import pandas as pd
import joblib

# Force UTF-8 encoding for console output on Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

# Define File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))               # .../SmartHire/backend/src/features
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))    # .../SmartHire/backend
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))      # .../SmartHire

CLEANED_RESUME_PATH = os.path.join(BACKEND_DIR, "data", "processed", "resumes_cleaned.csv")
CORPUS_PATH = os.path.join(BACKEND_DIR, "data", "processed", "job_corpus.csv")
MODELS_DIR = os.path.join(BACKEND_DIR, "models")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

CLASSIFIER_VECTORIZER_PATH = os.path.join(MODELS_DIR, "resume_tfidf_vectorizer.joblib")
CLASSIFIER_MODEL_PATH = os.path.join(MODELS_DIR, "resume_classifier.joblib")
SAMPLE_REPORT_JSON_PATH = os.path.join(REPORTS_DIR, "sample_skill_gap_report.json")

# In-Memory Cache for Datasets, Models, and Category Skill Profiles
_cached_df_jobs = None
_cached_classifier_vectorizer = None
_cached_classifier_model = None
_CATEGORY_SKILLS_CACHE = {}

# Transparent Filter for Obvious Non-Skill Noise & HR/Posting Metadata
GENERIC_NOISE = {
    "back office", "back office executive", "data entry", "data entry operator",
    "bpo", "bpo executive", "computer science", "analytical", "analytical skills",
    "job", "jobs", "employment", "hiring", "recruitment", "recruiter", "fresher",
    "experience", "n/a", "na", "etc", "etc.", "candidate", "work", "role", "roles",
    "requirement", "requirements", "skill", "skills", "responsibility", "responsibilities",
    "location", "company", "industry", "unknown", "null", "none", "operations",
    "support", "management", "executive", "officer", "manager"
}

# Standard Casing Display Dictionary for Popular Tech Terms
TECH_CASING = {
    "sql": "SQL", "python": "Python", "machine learning": "Machine Learning",
    "data analysis": "Data Analysis", "data science": "Data Science",
    "big data": "Big Data", "spark": "Spark", "hadoop": "Hadoop",
    "java": "Java", "data modeling": "Data Modeling", "data management": "Data Management",
    "data mining": "Data Mining", "data analytics": "Data Analytics",
    "scala": "Scala", "r": "R", "aws": "AWS", "tableau": "Tableau", "power bi": "Power BI",
    "scikit-learn": "Scikit-Learn", "pandas": "Pandas", "numpy": "NumPy",
    "deep learning": "Deep Learning", "nlp": "NLP", "tensorflow": "TensorFlow", "pytorch": "PyTorch",
    "linux": "Linux", "oracle": "Oracle", "performance tuning": "Performance Tuning",
    "data warehousing": "Data Warehousing", "hive": "Hive", "git": "Git", "django": "Django"
}


def clean_text_normalization(text: str) -> str:
    """Standard text normalization helper."""
    if pd.isna(text) or text is None:
        return ""
    text = str(text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"[^\x20-\x7E]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_usable_skill(term: str) -> bool:
    """Filtering mechanism to reject generic metadata & noise while preserving technical skills."""
    t_lower = term.strip().lower()
    if not t_lower or len(t_lower) <= 1:
        return False
    if t_lower in GENERIC_NOISE:
        return False
    if t_lower.isdigit():
        return False
    return True


def format_skill_display(term: str) -> str:
    """Preserves clean human-readable casing for output."""
    t_lower = term.strip().lower()
    if t_lower in TECH_CASING:
        return TECH_CASING[t_lower]
    return term.strip().title()


def _get_fallback_corpus_df() -> pd.DataFrame:
    """Returns a default corpus dataframe across major job categories if raw CSV is absent."""
    seed_jobs = [
        {
            "job_id": "JOB_SEED_001",
            "title": "Senior Data Scientist & ML Engineer",
            "company": "Tech Corp",
            "location": "Remote / Bengaluru",
            "skills": "Python | Machine Learning | PyTorch | TensorFlow | SQL | Scikit-learn | MLOps | Pandas | Big Data | Spark | Hadoop | Java | Data Science | Data Analysis | Analytics | Data Modeling",
            "description": "Building end-to-end Machine Learning pipelines, NLP models, and predictive algorithms.",
            "experience": "3 - 7 yrs",
            "salary": "15,00,000 - 30,00,000 PA",
            "source": "SmartHire Index",
            "combined_text": "Senior Data Scientist & ML Engineer Tech Corp Python Machine Learning PyTorch TensorFlow SQL Scikit-learn MLOps Pandas Big Data Spark Hadoop Java Data Science Data Analysis Analytics"
        },
        {
            "job_id": "JOB_SEED_002",
            "title": "Senior Frontend Developer (React & TypeScript)",
            "company": "UI Labs",
            "location": "Remote / Mumbai",
            "skills": "React.js | TypeScript | Next.js | Tailwind CSS | HTML5 | JavaScript | Redux | Webpack | UI/UX | Figma | CSS3 | Jest | Cypress",
            "description": "Architecting high-performance modern web applications with React and TypeScript.",
            "experience": "2 - 6 yrs",
            "salary": "12,00,000 - 24,00,000 PA",
            "source": "SmartHire Index",
            "combined_text": "Senior Frontend Developer React TypeScript UI Labs React.js Next.js Tailwind CSS HTML5 JavaScript Redux Webpack UI/UX Figma CSS3 Jest Cypress"
        },
        {
            "job_id": "JOB_SEED_003",
            "title": "Full Stack Software Engineer",
            "company": "Cloud Systems",
            "location": "Bengaluru / Hyderabad",
            "skills": "Java | Spring Boot | Python | Node.js | PostgreSQL | MongoDB | Docker | AWS | REST APIs | Microservices | CI/CD | Git | System Architecture",
            "description": "Designing microservices backend APIs and responsive frontend interfaces.",
            "experience": "2 - 5 yrs",
            "salary": "10,00,000 - 20,00,000 PA",
            "source": "SmartHire Index",
            "combined_text": "Full Stack Software Engineer Cloud Systems Java Spring Boot Python Node.js PostgreSQL MongoDB Docker AWS REST APIs Microservices CI/CD Git"
        },
        {
            "job_id": "JOB_SEED_004",
            "title": "DevOps & Cloud Infrastructure Engineer",
            "company": "DevOps Global",
            "location": "Remote / Pune",
            "skills": "Kubernetes | Docker | AWS | Terraform | CI/CD | Linux | Bash | Python | Cloud Security | Ansible | Monitoring | Jenkins",
            "description": "Managing automated CI/CD deployment pipelines, cloud infrastructure, and Kubernetes clusters.",
            "experience": "3 - 8 yrs",
            "salary": "14,00,000 - 28,00,000 PA",
            "source": "SmartHire Index",
            "combined_text": "DevOps & Cloud Infrastructure Engineer DevOps Global Kubernetes Docker AWS Terraform CI/CD Linux Bash Python Cloud Security Ansible Monitoring Jenkins"
        },
        {
            "job_id": "JOB_SEED_005",
            "title": "Data Analyst & Business Intelligence Specialist",
            "company": "Analytics Insights",
            "location": "Gurugram / Delhi",
            "skills": "SQL | Tableau | Power BI | Excel | Python | Data Analysis | ETL | Statistics | Business Intelligence | Data Visualization",
            "description": "Creating executive BI dashboards and analyzing large dataset trends to drive business growth.",
            "experience": "1 - 4 yrs",
            "salary": "7,00,000 - 14,00,000 PA",
            "source": "SmartHire Index",
            "combined_text": "Data Analyst & Business Intelligence Specialist Analytics Insights SQL Tableau Power BI Excel Python Data Analysis ETL Statistics Business Intelligence Data Visualization"
        }
    ]
    return pd.DataFrame(seed_jobs)


def load_datasets_and_models():
    """Validates and loads dataset files and pre-trained classification models into memory cache."""
    global _cached_df_jobs, _cached_classifier_vectorizer, _cached_classifier_model

    if _cached_df_jobs is None:
        if os.path.exists(CORPUS_PATH):
            _cached_df_jobs = pd.read_csv(CORPUS_PATH)
        else:
            print("Job Corpus CSV not found locally. Loading seed job corpus dataframe.")
            _cached_df_jobs = _get_fallback_corpus_df()
        
    if _cached_classifier_vectorizer is None and os.path.exists(CLASSIFIER_VECTORIZER_PATH):
        _cached_classifier_vectorizer = joblib.load(CLASSIFIER_VECTORIZER_PATH)
        
    if _cached_classifier_model is None and os.path.exists(CLASSIFIER_MODEL_PATH):
        _cached_classifier_model = joblib.load(CLASSIFIER_MODEL_PATH)

    return _cached_df_jobs, _cached_classifier_vectorizer, _cached_classifier_model


def predict_category_from_resume(resume_text: str, vectorizer, model) -> str:
    """Predicts target category for a resume using Phase 3A trained classifier."""
    if not vectorizer or not model:
        return "Unknown"
    
    cleaned = clean_text_normalization(resume_text)
    tfidf_vec = vectorizer.transform([cleaned])
    predicted_cat = model.predict(tfidf_vec)[0]
    return predicted_cat


def extract_category_skills_from_corpus(df_jobs: pd.DataFrame, category: str, top_n_skills: int = 20):
    """
    Derives category skills dynamically using Document-Frequency (DF) ranking.
    Uses in-memory cache to prevent re-indexing rows on every API call.
    """
    cache_key = (category.lower().strip(), top_n_skills)
    if cache_key in _CATEGORY_SKILLS_CACHE:
        return _CATEGORY_SKILLS_CACHE[cache_key]

    cat_clean = category.lower().strip()
    cat_terms = cat_clean.split()
    main_term = cat_terms[0] if cat_terms else cat_clean

    mask = (
        df_jobs["title"].str.contains(main_term, case=False, na=False) |
        df_jobs["combined_text"].str.contains(category, case=False, na=False)
    )
    matching_jobs_df = df_jobs[mask]

    if len(matching_jobs_df) == 0:
        matching_jobs_df = df_jobs

    doc_freq = Counter()
    raw_skills_set = set()

    for raw_skills in matching_jobs_df["skills"].dropna():
        if not raw_skills or str(raw_skills).lower() == "unknown":
            continue
        
        tokens = re.split(r"[\|,;/]+", str(raw_skills))
        job_skills_in_posting = set()
        
        for token in tokens:
            cleaned = token.strip()
            if cleaned:
                raw_skills_set.add(cleaned.lower())
                if is_usable_skill(cleaned):
                    display_term = format_skill_display(cleaned)
                    job_skills_in_posting.add(display_term)
        
        for skill in job_skills_in_posting:
            doc_freq[skill] += 1

    total_raw_skills = len(raw_skills_set)
    total_usable_skills = len(doc_freq)
    top_skills_pairs = doc_freq.most_common(top_n_skills)
    top_target_skills = [skill for skill, count in top_skills_pairs]

    result = (len(matching_jobs_df), total_raw_skills, total_usable_skills, top_target_skills, doc_freq)
    _CATEGORY_SKILLS_CACHE[cache_key] = result
    return result


def extract_candidate_skills(resume_text: str, target_skills: list) -> list:
    """Rule-based candidate skill detection using phrase matching."""
    cleaned_resume_lower = clean_text_normalization(resume_text).lower()
    matched = []

    for skill in target_skills:
        skill_lower = skill.lower().strip()
        if not skill_lower:
            continue

        if re.search(r"[\+\#\.]", skill_lower):
            if skill_lower in cleaned_resume_lower:
                matched.append(skill)
        else:
            pattern = r"\b" + re.escape(skill_lower) + r"\b"
            if re.search(pattern, cleaned_resume_lower):
                matched.append(skill)

    return matched


def generate_skill_gap(resume_text: str, target_category: str = None, top_n_skills: int = 20) -> dict:
    """
    Main Skill Gap Analysis API Function.
    Uses in-memory cached datasets and skill profiles for ultra-fast performance.
    """
    df_jobs, vectorizer, model = load_datasets_and_models()

    # Step 1: Determine target category
    if not target_category or str(target_category).strip().lower() in ["none", "", "unknown"]:
        target_category = predict_category_from_resume(resume_text, vectorizer, model)
    
    # Step 2: Build category skill profile from dataset evidence
    num_jobs_found, raw_skills_count, usable_skills_count, top_target_skills, doc_freq = extract_category_skills_from_corpus(
        df_jobs, target_category, top_n_skills=top_n_skills
    )

    total_target_skills = len(top_target_skills)

    # Step 3: Extract candidate skills & compare
    matched_skills = extract_candidate_skills(resume_text, top_target_skills)
    missing_skills = [s for s in top_target_skills if s not in matched_skills]

    # Step 4: Calculate Match Percentage
    if total_target_skills > 0:
        match_percentage = round((len(matched_skills) / total_target_skills) * 100, 2)
    else:
        match_percentage = 0.0

    result = {
        "target_category": target_category,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommended_skills": missing_skills,
        "match_percentage": match_percentage,
        "total_target_skills": total_target_skills,
        "_meta": {
            "category_jobs_analyzed": num_jobs_found,
            "raw_unique_skills_found": raw_skills_count,
            "usable_skills_after_filtering": usable_skills_count,
            "top_target_skills": top_target_skills,
            "doc_freq": {s: doc_freq[s] for s in top_target_skills}
        }
    }

    return result
