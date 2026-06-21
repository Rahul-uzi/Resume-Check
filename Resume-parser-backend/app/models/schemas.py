from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class PersonalInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None

class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    description: Optional[str] = None

class Experience(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    current: Optional[bool] = False
    description: Optional[str] = None
    responsibilities: Optional[List[str]] = []

class Project(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[List[str]] = []
    url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Certification(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None
    date: Optional[str] = None
    credential_id: Optional[str] = None
    url: Optional[str] = None

class ParsedResume(BaseModel):
    filename: str
    personal_info: PersonalInfo
    summary: Optional[str] = None
    skills: List[str] = []
    education: List[Education] = []
    experience: List[Experience] = []
    projects: List[Project] = []
    certifications: List[Certification] = []
    languages: List[str] = []
    total_experience_years: Optional[float] = None
    parsed_at: datetime = Field(default_factory=datetime.now)
    raw_text: Optional[str] = None

class ResumeResponse(BaseModel):
    success: bool
    message: str
    resume_id: Optional[str] = None
    data: Optional[ParsedResume] = None

class SearchRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None
    limit: int = Field(default=10, ge=1, le=100)

class SearchResult(BaseModel):
    resume_id: str
    score: float
    data: ParsedResume

class SearchResponse(BaseModel):
    success: bool
    count: int
    results: List[SearchResult]
