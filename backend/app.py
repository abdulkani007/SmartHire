"""
SmartHire — FastAPI Backend Application Entrypoint
Author: SmartHire ML Team
Description: Main FastAPI server incorporating CORS middleware, health endpoints,
             global error handling, Phase 5B ML endpoints, and MongoDB Compass integration.
"""

import os
import sys
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Force UTF-8 encoding for standard output on Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add src to Python Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src"))

from routes.ml_routes import router as ml_router
from db.mongodb import mongo_db

# Application Metadata
API_TITLE = "SmartHire API"
API_DESCRIPTION = "Resume-to-Job Matching & Career Guidance Engine"
API_VERSION = "1.0.0"

# Initialize FastAPI Application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for all local development origins and ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Machine Learning & Database Routes
app.include_router(ml_router)


@app.on_event("startup")
async def startup_event():
    """Triggers on server startup to verify MongoDB Compass connection."""
    connected = mongo_db.connect()
    if connected:
        print(f"[MongoDB Compass] Connected to database '{mongo_db.db_name}' at '{mongo_db.uri}'")
    else:
        print(f"[MongoDB Compass] Running in standalone mode (no MongoDB instance detected at '{mongo_db.uri}')")


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An internal server error occurred.",
            "detail": str(exc)
        },
    )


# Root Endpoint
@app.get("/", summary="Root Endpoint", tags=["General"])
async def root():
    """Returns a simple greeting indicating that the SmartHire API service is running."""
    return {"message": "SmartHire API is running", "database": mongo_db.get_status()}


# Health Check Endpoint
@app.get("/health", summary="Health Check", tags=["Health"])
async def health():
    """Returns the operational status of the SmartHire API."""
    return {
        "status": "ok",
        "service": "SmartHire API",
        "mongodb": mongo_db.is_connected
    }


if __name__ == "__main__":
    import uvicorn
    # Local development runner
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
