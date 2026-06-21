from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Optional
import os
from datetime import datetime

from app.services.resume_parser import ResumeParser
from app.services.vector_store import VectorStore
from app.services.question_generator import QuestionGenerator
from app.models.schemas import ResumeResponse, SearchRequest, SearchResponse
from app.config import settings

app = FastAPI(
    title="Resume Parser API",
    description="AI-powered Resume Parser using Google Gemini and Vector Database",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
resume_parser = ResumeParser()
vector_store = VectorStore()
question_generator = QuestionGenerator()

@app.get("/")
async def root():
    return {
        "message": "Resume Parser API is running!",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/api/upload",
            "search": "/api/search",
            "resumes": "/api/resumes",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "parser": "operational",
            "vector_db": "operational"
        }
    }

@app.post("/api/upload", response_model=ResumeResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse a resume file (PDF, DOCX, TXT)
    """
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Read file content
        content = await file.read()
        
        # Parse resume using AI
        parsed_data = await resume_parser.parse_resume(content, file.filename)
        
        # Store in vector database
        resume_id = await vector_store.add_resume(parsed_data)
        
        return ResumeResponse(
            success=True,
            message="Resume parsed successfully",
            resume_id=resume_id,
            data=parsed_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search", response_model=SearchResponse)
async def search_resumes(request: SearchRequest):
    """
    Search resumes using semantic search
    """
    try:
        results = await vector_store.search_resumes(
            query=request.query,
            filters=request.filters,
            limit=request.limit
        )
        
        return SearchResponse(
            success=True,
            count=len(results),
            results=results
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resumes")
async def get_all_resumes(skip: int = 0, limit: int = 10):
    """
    Get all parsed resumes with pagination
    """
    try:
        resumes = await vector_store.get_all_resumes(skip=skip, limit=limit)
        total = await vector_store.count_resumes()
        
        return {
            "success": True,
            "total": total,
            "skip": skip,
            "limit": limit,
            "resumes": resumes
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resume/{resume_id}")
async def get_resume(resume_id: str):
    """
    Get a specific resume by ID
    """
    try:
        resume = await vector_store.get_resume_by_id(resume_id)
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        return {
            "success": True,
            "resume": resume
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resume/{resume_id}/questions")
async def generate_questions(resume_id: str):
    """
    Generate skill-based interview questions for a resume
    """
    try:
        # Get resume data
        resume = await vector_store.get_resume_by_id(resume_id)
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        resume_data = resume.get("data", {})
        skills = resume_data.get("skills", [])
        experience_years = resume_data.get("total_experience_years", 0)
        
        if not skills:
            raise HTTPException(status_code=400, detail="No skills found in resume")
        
        # Generate questions
        questions = await question_generator.generate_questions(skills, experience_years)
        
        return {
            "success": True,
            "resume_id": resume_id,
            "total_questions": len(questions),
            "questions": questions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/resume/{resume_id}")
async def delete_resume(resume_id: str):
    """
    Delete a resume by ID
    """
    try:
        deleted = await vector_store.delete_resume(resume_id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        return {
            "success": True,
            "message": "Resume deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ============== SKILL-BASED QUESTIONS SECTION ==============
from app.data.predefined_questions import get_predefined_questions, get_questions_by_skill, get_questions_for_resume_skills

@app.get("/api/skill-questions")
async def get_skill_questions(skill: Optional[str] = None):
    """
    Get predefined skill-based medium level interview questions with answers.
    Optionally filter by skill name.
    """
    try:
        if skill:
            questions = get_questions_by_skill(skill)
        else:
            questions = get_predefined_questions()
        
        return {
            "success": True,
            "total_questions": len(questions),
            "section": "Skill-Based Medium Level Questions",
            "description": "Curated interview questions covering essential technical skills",
            "questions": questions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/skill-questions/skills")
async def get_available_skills():
    """
    Get list of all available skills for filtering questions
    """
    try:
        questions = get_predefined_questions()
        skills = list(set(q["skill"] for q in questions))
        
        return {
            "success": True,
            "skills": sorted(skills),
            "total": len(skills)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/resume/{resume_id}/skill-based-questions")
async def get_resume_skill_based_questions(resume_id: str):
    """
    Get skill-based questions matched to a specific resume's skills.
    Questions are filtered based on skills found in the resume.
    """
    try:
        # Get resume data
        resume = await vector_store.get_resume_by_id(resume_id)
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        resume_data = resume.get("data", {})
        skills = resume_data.get("skills", [])
        candidate_name = resume_data.get("name", "Candidate")
        
        # Get matched questions based on resume skills
        matched_questions = get_questions_for_resume_skills(skills)
        
        return {
            "success": True,
            "resume_id": resume_id,
            "candidate_name": candidate_name,
            "resume_skills": skills,
            "matched_skills_count": len(skills),
            "section": "Skill-Based Medium Level Questions",
            "description": f"Interview questions matched to {candidate_name}'s skills",
            "total_questions": len(matched_questions),
            "questions": matched_questions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

