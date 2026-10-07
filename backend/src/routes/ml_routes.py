"""
SmartHire — Machine Learning & MongoDB Atlas Router Endpoints
Author: SmartHire ML Team
Description: Exposes routes for Category Classification, Job Recommendation, Skill Gap Analysis,
             Resume Upload Analysis, and MongoDB Atlas persistence & status.
"""

import os
import sys
from fastapi import APIRouter, HTTPException, File, UploadFile, status

BASE_DIR = os.path.dirname(os.path.abspath(__file__))               # .../SmartHire/backend/src/routes
BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))    # .../SmartHire/backend

sys.path.append(os.path.join(BACKEND_DIR, "src"))

from services.ml_service import ml_service
from parsing.resume_parser import extract_text_from_bytes
from db.mongodb import mongo_db
from schemas.api_models import (
    PredictCategoryRequest, PredictCategoryResponse,
    RecommendJobsRequest, RecommendJobsResponse,
    SkillGapRequest, SkillGapResponse,
    AnalyzeResumeResponse
)

router = APIRouter(prefix="/api", tags=["Machine Learning & Database Engine"])


@router.post(
    "/analyze-resume",
    response_model=AnalyzeResumeResponse,
    summary="Full Resume Analysis (File Upload)",
    status_code=status.HTTP_200_OK
)
async def analyze_resume(file: UploadFile = File(...)):
    """
    Parses an uploaded resume file (PDF, DOCX, TXT), executes classical ML models,
    and automatically persists the analysis record into MongoDB Atlas (smarthire_db.resume_analyses).
    """
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty.")

        text = extract_text_from_bytes(content, file.filename)
        if not text or len(text.strip()) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract sufficient text from the file. Please ensure the document contains readable text."
            )

        # Execute ML Pipeline
        category = ml_service.predict_category(text)
        recs = ml_service.recommend_jobs(text, top_n=10)
        gap_report = ml_service.generate_skill_gap(text, target_category=category, top_n_skills=20)

        # Persist Document Record to MongoDB Atlas
        analysis_id = mongo_db.save_analysis(
            filename=file.filename,
            predicted_category=category,
            recommendations=recs,
            skill_gap=gap_report,
            raw_text=text
        )

        return AnalyzeResumeResponse(
            success=True,
            filename=file.filename,
            predicted_category=category,
            recommendations=recs,
            skill_gap=gap_report
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while analyzing the resume: {str(e)}"
        )


@router.post(
    "/predict-category",
    response_model=PredictCategoryResponse,
    summary="Predict Resume Category",
    status_code=status.HTTP_200_OK
)
async def predict_category(request: PredictCategoryRequest):
    """
    Classifies a candidate resume text into one of 25 job categories using Supervised Logistic Regression.
    """
    try:
        category = ml_service.predict_category(request.resume_text)
        return PredictCategoryResponse(success=True, category=category)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing resume category classification."
        )


@router.post(
    "/recommend-jobs",
    response_model=RecommendJobsResponse,
    summary="Recommend Matching Jobs",
    status_code=status.HTTP_200_OK
)
async def recommend_jobs(request: RecommendJobsRequest):
    """
    Recommends top matching job postings for a candidate resume text using Content-Based TF-IDF + Cosine Similarity.
    """
    try:
        recs = ml_service.recommend_jobs(request.resume_text, top_n=request.top_n)
        return RecommendJobsResponse(success=True, recommendations=recs)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing job recommendations."
        )


@router.post(
    "/skill-gap",
    response_model=SkillGapResponse,
    summary="Skill Gap Analysis & Recommendations",
    status_code=status.HTTP_200_OK
)
async def skill_gap(request: SkillGapRequest):
    """
    Compares candidate resume skills against target category skill profiles derived from the 148,000+ job corpus.
    """
    try:
        report = ml_service.generate_skill_gap(
            resume_text=request.resume_text,
            target_category=request.target_category,
            top_n_skills=request.top_n_skills
        )
        return SkillGapResponse(
            success=True,
            target_category=report["target_category"],
            matched_skills=report["matched_skills"],
            missing_skills=report["missing_skills"],
            recommended_skills=report["recommended_skills"],
            match_percentage=report["match_percentage"],
            total_target_skills=report["total_target_skills"]
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while performing skill gap analysis."
        )


@router.get(
    "/db/status",
    summary="MongoDB Atlas Connection Status",
    tags=["Database"]
)
async def get_db_status():
    """
    Returns connection status and collection statistics for MongoDB Atlas.
    """
    return mongo_db.get_status()


@router.get(
    "/db/history",
    summary="Fetch Recent Resume Analysis History",
    tags=["Database"]
)
async def get_db_history(limit: int = 10):
    """
    Fetches historical resume analysis records persisted in MongoDB Atlas.
    """
    history = mongo_db.get_recent_analyses(limit=limit)
    return {
        "success": True,
        "count": len(history),
        "history": history
    }
