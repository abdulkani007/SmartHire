# SmartHire — Resume-to-Job Matching & Career Guidance Engine

SmartHire is an end-to-end Classical Machine Learning & NLP system designed to:
1. Classify resumes into career categories (Supervised ML).
2. Recommend top matching job postings using TF-IDF and Cosine Similarity (Unsupervised Content-Based Filtering).
3. Perform Skill-Gap Analysis comparing candidate skills against target job roles.
4. Provide interactive career guidance via a Streamlit web application.

---

## 🛠️ Project Structure
```
SmartHire/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_resume_classifier.ipynb
│   ├── 03_recommender.ipynb
│   ├── 04_clustering_topics.ipynb
│   └── 05_fit_predictor.ipynb
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── parsing/
├── models/
├── app/
│   └── streamlit_app.py
├── reports/
└── tests/
```

---

## 🚀 Tech Stack
- **Language:** Python 3.11+
- **Data Manipulation:** Pandas, NumPy
- **Classical ML & NLP:** Scikit-learn, NLTK
- **Web Interface:** Streamlit
- **Visualization:** Matplotlib, Seaborn
