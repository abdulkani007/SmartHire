"""
SmartHire — MongoDB Atlas Integration Module
Author: SmartHire Backend Team
Description: Connects FastAPI backend to MongoDB Atlas via MONGODB_URI.
             Provides automated document persistence for resume analysis reports, job matches, and skill gaps.
"""

import os
from datetime import datetime
import logging
from typing import Dict, Any, List, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import pymongo
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

logger = logging.getLogger("smarthire.mongodb")


class MongoDBManager:
    def __init__(self, uri: Optional[str] = None, db_name: Optional[str] = None):
        self.uri = uri or os.getenv("MONGODB_URI", "")
        self.db_name = db_name or os.getenv("MONGODB_DB_NAME", "smarthire_db")
        self.client: Optional[Any] = None
        self.db: Optional[Any] = None
        self.is_connected: bool = False

    def _sanitize_uri(self, uri: str) -> str:
        """Returns a sanitized version of the connection string hiding sensitive credentials."""
        if not uri:
            return "Not Configured"
        if "@" in uri:
            parts = uri.split("@")
            prefix = parts[0].split("://")[0] + "://" + "***:***"
            return f"{prefix}@{parts[1]}"
        return uri

    def connect(self) -> bool:
        """Establishes connection to MongoDB Atlas instance."""
        self.uri = os.getenv("MONGODB_URI", self.uri)
        self.db_name = os.getenv("MONGODB_DB_NAME", self.db_name)

        if not PYMONGO_AVAILABLE:
            logger.warning("PyMongo package is not installed. MongoDB features disabled.")
            self.is_connected = False
            return False

        if not self.uri or not self.uri.strip():
            self.is_connected = False
            logger.warning("MongoDB Atlas connection unavailable. Running in standalone mode.")
            return False

        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Verify connection with ping
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self.is_connected = True
            logger.info(f"MongoDB Atlas connected successfully. (Database: {self.db_name})")

            # Create Indexes for fast querying
            try:
                self.db.resume_analyses.create_index([("created_at", pymongo.DESCENDING)])
                self.db.resume_analyses.create_index([("predicted_category", pymongo.ASCENDING)])
            except Exception as idx_err:
                logger.warning(f"Could not create indexes on MongoDB Atlas: {idx_err}")

            return True
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            self.is_connected = False
            logger.warning("MongoDB Atlas connection unavailable. Running in standalone mode.")
            return False

    def save_analysis(
        self, 
        filename: str, 
        predicted_category: str, 
        recommendations: List[Dict[str, Any]], 
        skill_gap: Dict[str, Any],
        raw_text: Optional[str] = None
    ) -> Optional[str]:
        """Saves a completed resume analysis report to MongoDB Atlas (resume_analyses collection)."""
        if not self.is_connected or self.db is None:
            if not self.connect():
                return None

        try:
            document = {
                "filename": filename,
                "predicted_category": predicted_category,
                "recommendations_count": len(recommendations),
                "recommendations": recommendations[:10], # Top 10 recommendations
                "skill_gap": skill_gap,
                "created_at": datetime.utcnow(),
                "created_at_iso": datetime.utcnow().isoformat()
            }
            if raw_text:
                document["snippet"] = raw_text[:300] # Store preview snippet

            result = self.db.resume_analyses.insert_one(document)
            logger.info(f"Saved resume analysis for '{filename}' to MongoDB Atlas (ID: {result.inserted_id})")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to save analysis document to MongoDB Atlas: {e}")
            return None

    def get_recent_analyses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves recent resume analysis history stored in MongoDB Atlas."""
        if not self.is_connected or self.db is None:
            if not self.connect():
                return []

        try:
            cursor = self.db.resume_analyses.find(
                {}, 
                {"_id": 1, "filename": 1, "predicted_category": 1, "created_at_iso": 1, "skill_gap.match_percentage": 1, "recommendations_count": 1}
            ).sort("created_at", pymongo.DESCENDING).limit(limit)

            history = []
            for doc in cursor:
                doc["id"] = str(doc.pop("_id"))
                history.append(doc)
            return history
        except Exception as e:
            logger.error(f"Failed to fetch analysis history from MongoDB Atlas: {e}")
            return []

    def get_status(self) -> Dict[str, Any]:
        """Returns connection status and collection statistics for MongoDB Atlas."""
        if not self.is_connected or self.db is None:
            self.connect()

        status = {
            "connected": self.is_connected,
            "uri": self._sanitize_uri(self.uri),
            "database": self.db_name,
            "collections": {}
        }

        if self.is_connected and self.db is not None:
            try:
                status["collections"]["resume_analyses"] = self.db.resume_analyses.count_documents({})
                status["collections"]["job_postings"] = self.db.jobs.count_documents({}) if "jobs" in self.db.list_collection_names() else 0
            except Exception as e:
                status["error"] = str(e)

        return status


# Global MongoDB Instance
mongo_db = MongoDBManager()
