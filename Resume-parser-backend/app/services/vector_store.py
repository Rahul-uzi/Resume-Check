import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import uuid
import json
from datetime import datetime

from app.models.schemas import ParsedResume, SearchResult
from app.config import settings

class VectorStore:
    def __init__(self):
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="resumes",
            metadata={"description": "Resume embeddings and metadata"}
        )
    
    async def add_resume(self, resume: ParsedResume) -> str:
        """
        Add resume to vector database
        """
        try:
            resume_id = str(uuid.uuid4())
            
            # Create searchable text
            searchable_text = self._create_searchable_text(resume)
            
            # Convert resume to dict for metadata
            metadata = {
                "filename": resume.filename,
                "name": resume.personal_info.name or "Unknown",
                "email": resume.personal_info.email or "",
                "phone": resume.personal_info.phone or "",
                "skills": json.dumps(resume.skills),
                "total_experience": resume.total_experience_years or 0,
                "parsed_at": resume.parsed_at.isoformat(),
            }
            
            # Store full resume data as document
            document = resume.model_dump_json()
            
            # Add to collection
            self.collection.add(
                ids=[resume_id],
                documents=[searchable_text],
                metadatas=[metadata]
            )
            
            # Store full data separately (in metadata or separate storage)
            # For now, we'll store it in a separate collection
            full_data_collection = self.client.get_or_create_collection("resume_full_data")
            full_data_collection.add(
                ids=[resume_id],
                documents=[document],
                metadatas={"resume_id": resume_id}
            )
            
            return resume_id
            
        except Exception as e:
            raise Exception(f"Error adding resume to vector store: {str(e)}")
    
    async def search_resumes(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10
    ) -> List[SearchResult]:
        """
        Search resumes using semantic search
        """
        try:
            # Build where clause for filters
            where = {}
            if filters:
                if "min_experience" in filters:
                    where["total_experience"] = {"$gte": filters["min_experience"]}
                if "skills" in filters and filters["skills"]:
                    # Note: ChromaDB doesn't support array contains, so we'll filter after
                    pass
            
            # Perform search
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where=where if where else None
            )
            
            # Get full resume data
            full_data_collection = self.client.get_or_create_collection("resume_full_data")
            
            search_results = []
            if results['ids'] and results['ids'][0]:
                for i, resume_id in enumerate(results['ids'][0]):
                    # Get full data
                    full_data = full_data_collection.get(ids=[resume_id])
                    
                    if full_data['documents']:
                        resume_data = json.loads(full_data['documents'][0])
                        
                        # Apply skill filter if needed
                        if filters and "skills" in filters and filters["skills"]:
                            resume_skills = resume_data.get("skills", [])
                            if not any(skill.lower() in [s.lower() for s in resume_skills] for skill in filters["skills"]):
                                continue
                        
                        search_results.append(
                            SearchResult(
                                resume_id=resume_id,
                                score=1 - results['distances'][0][i],  # Convert distance to similarity
                                data=ParsedResume(**resume_data)
                            )
                        )
            
            return search_results
            
        except Exception as e:
            raise Exception(f"Error searching resumes: {str(e)}")
    
    async def get_all_resumes(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get all resumes with pagination
        """
        try:
            full_data_collection = self.client.get_or_create_collection("resume_full_data")
            
            # Get all data (ChromaDB doesn't have built-in pagination, so we'll do it manually)
            all_data = full_data_collection.get()
            
            resumes = []
            if all_data['documents']:
                for i in range(skip, min(skip + limit, len(all_data['documents']))):
                    resume_data = json.loads(all_data['documents'][i])
                    resumes.append({
                        "resume_id": all_data['ids'][i],
                        "data": resume_data
                    })
            
            return resumes
            
        except Exception as e:
            raise Exception(f"Error getting all resumes: {str(e)}")
    
    async def get_resume_by_id(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific resume by ID
        """
        try:
            full_data_collection = self.client.get_or_create_collection("resume_full_data")
            result = full_data_collection.get(ids=[resume_id])
            
            if result['documents']:
                return {
                    "resume_id": resume_id,
                    "data": json.loads(result['documents'][0])
                }
            
            return None
            
        except Exception as e:
            raise Exception(f"Error getting resume: {str(e)}")
    
    async def delete_resume(self, resume_id: str) -> bool:
        """
        Delete a resume by ID
        """
        try:
            self.collection.delete(ids=[resume_id])
            
            full_data_collection = self.client.get_or_create_collection("resume_full_data")
            full_data_collection.delete(ids=[resume_id])
            
            return True
            
        except Exception as e:
            raise Exception(f"Error deleting resume: {str(e)}")
    
    async def count_resumes(self) -> int:
        """
        Get total count of resumes
        """
        try:
            result = self.collection.get()
            return len(result['ids']) if result['ids'] else 0
        except Exception as e:
            raise Exception(f"Error counting resumes: {str(e)}")
    
    def _create_searchable_text(self, resume: ParsedResume) -> str:
        """
        Create searchable text from resume data
        """
        parts = []
        
        # Personal info
        if resume.personal_info.name:
            parts.append(f"Name: {resume.personal_info.name}")
        
        # Summary
        if resume.summary:
            parts.append(f"Summary: {resume.summary}")
        
        # Skills
        if resume.skills:
            parts.append(f"Skills: {', '.join(resume.skills)}")
        
        # Education
        for edu in resume.education:
            parts.append(f"Education: {edu.degree} in {edu.field_of_study} from {edu.institution}")
        
        # Experience
        for exp in resume.experience:
            parts.append(f"Experience: {exp.title} at {exp.company}")
            if exp.description:
                parts.append(exp.description)
        
        # Projects
        for proj in resume.projects:
            parts.append(f"Project: {proj.name} - {proj.description}")
        
        # Certifications
        for cert in resume.certifications:
            parts.append(f"Certification: {cert.name} from {cert.issuer}")
        
        return "\n".join(parts)
