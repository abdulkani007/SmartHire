"""
SmartHire — MongoDB Compass Integration Module
Author: SmartHire Backend Team
Description: Connects FastAPI backend to MongoDB Compass (mongodb://localhost:27017/smarthire_db).
             Provides automated document persistence for resume analysis reports, job matches, and skill gaps.
"""

import os
from datetime import datetime
import logging
from typing import Dict, Any, List, Optional

try:
    import pymongo
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

logger = logging.getLogger("smarthire.mongodb")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "smarthire_db")


class MongoDBManager:
    def __init__(self, uri: str = MONGODB_URI, db_name: str = DB_NAME):
        self.uri = uri
        self.db_name = db_name
        self.client: Optional[Any] = None
        self.db: Optional[Any] = None
        self.is_connected: bool = False

    def connect(self) -> bool:
        """Establishes connection to MongoDB Compass / Local MongoDB instance."""
        if not PYMONGO_AVAILABLE:
            logger.warning("PyMongo package is not installed. MongoDB features disabled.")
            return False

        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=2000)
            # Verify connection with ping
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self.is_connected = True
            logger.info(f"Successfully connected to MongoDB Compass at {self.uri} (Database: {self.db_name})")

            # Create Indexes for fast querying
            self.db.resume_analyses.create_index([("created_at", pymongo.DESCENDING)])
            self.db.resume_analyses.create_index([("predicted_category", pymongo.ASCENDING)])
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            self.is_connected = False
            logger.warning(f"Could not connect to MongoDB Compass on {self.uri}: {e}. Running in standalone mode.")
            return False

    def save_analysis(
        self, 
        filename: str, 
        predicted_category: str, 
        recommendations: List[Dict[str, Any]], 
        skill_gap: Dict[str, Any],
        raw_text: Optional[str] = None
    ) -> Optional[str]:
        """Saves a completed resume analysis report to MongoDB Compass (resume_analyses collection)."""
        if not self.is_connected or self.db is None:
            # Re-attempt connection once
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
            logger.info(f"Saved resume analysis for '{filename}' to MongoDB Compass (ID: {result.inserted_id})")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to save analysis document to MongoDB: {e}")
            return None

    def get_recent_analyses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves recent resume analysis history stored in MongoDB Compass."""
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
            logger.error(f"Failed to fetch analysis history from MongoDB: {e}")
            return []

    def get_status(self) -> Dict[str, Any]:
        """Returns connection status and collection statistics for MongoDB Compass."""
        if not self.is_connected or self.db is None:
            self.connect()

        status = {
            "connected": self.is_connected,
            "uri": self.uri,
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
