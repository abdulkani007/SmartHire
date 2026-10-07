"""
SmartHire — Pydantic API Models & Request/Response Schemas
Author: SmartHire ML Team
Description: Defines input validation schemas and response models for FastAPI endpoints.
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, field_validator


# ==========================================
# REQUEST MODELS
# ==========================================

class PredictCategoryRequest(BaseModel):
    resume_text: str = Field(..., description="Raw or extracted textual content of candidate resume.")

    @field_validator("resume_text")
    def validate_resume_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("resume_text must not be empty or whitespace only.")
        return v.strip()


class RecommendJobsRequest(BaseModel):
    resume_text: str = Field(..., description="Raw or extracted textual content of candidate resume.")
    top_n: int = Field(default=10, ge=1, le=20, description="Number of top job recommendations (1-20).")

    @field_validator("resume_text")
    def validate_resume_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("resume_text must not be empty or whitespace only.")
        return v.strip()


class SkillGapRequest(BaseModel):
    resume_text: str = Field(..., description="Raw or extracted textual content of candidate resume.")
    target_category: Optional[str] = Field(default=None, description="Target career category. If omitted, predicted automatically.")
    top_n_skills: int = Field(default=20, ge=1, le=50, description="Number of top target skills (1-50).")

    @field_validator("resume_text")
    def validate_resume_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("resume_text must not be empty or whitespace only.")
        return v.strip()


# ==========================================
# RESPONSE MODELS
# ==========================================

class PredictCategoryResponse(BaseModel):
    success: bool = True
    category: str


class JobRecommendationItem(BaseModel):
    job_id: Any
    title: str
    company: str
    location: str
    skills: str
    experience: str
    salary: str
    source: str
    similarity_score: float


class RecommendJobsResponse(BaseModel):
    success: bool = True
    recommendations: List[JobRecommendationItem]


class SkillGapResponse(BaseModel):
    success: bool = True
    target_category: str
    matched_skills: List[str]
    missing_skills: List[str]
    recommended_skills: List[str]
    match_percentage: float
    total_target_skills: int


class AnalyzeResumeResponse(BaseModel):
    success: bool = True
    filename: Optional[str] = "Uploaded Document"
    predicted_category: str
    recommendations: List[Dict[str, Any]]
    skill_gap: Dict[str, Any]
