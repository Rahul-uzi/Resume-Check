import os
import json
import re
from typing import Dict, Any
from datetime import datetime
import PyPDF2
import docx
from io import BytesIO

from langchain_google_genai import ChatGoogleGenerativeAI

from app.models.schemas import ParsedResume, PersonalInfo, Education, Experience, Project, Certification
from app.config import settings

class ResumeParser:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            api_key=settings.GOOGLE_API_KEY,
            temperature=0.1
        )
        
    async def parse_resume(self, file_content: bytes, filename: str) -> ParsedResume:
        """
        Parse resume using Google Gemini AI
        """
        # Extract text from file
        text = self._extract_text(file_content, filename)
        
        # Parse using AI
        parsed_data = await self._parse_with_ai(text, filename)
        
        return parsed_data
    
    def _extract_text(self, file_content: bytes, filename: str) -> str:
        """
        Extract text from PDF, DOCX, or TXT files
        """
        file_ext = os.path.splitext(filename)[1].lower()
        
        try:
            if file_ext == '.pdf':
                return self._extract_from_pdf(file_content)
            elif file_ext in ['.docx', '.doc']:
                return self._extract_from_docx(file_content)
            elif file_ext == '.txt':
                return file_content.decode('utf-8')
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")
    
    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF"""
        pdf_file = BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX"""
        doc_file = BytesIO(file_content)
        doc = docx.Document(doc_file)
        
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text.strip()
    
    async def _parse_with_ai(self, text: str, filename: str) -> ParsedResume:
        """
        Parse resume text using Google Gemini AI
        """
        prompt = f"""
You are an expert resume parser. Analyze the following resume text and extract structured information.

Resume Text:
{text}

Extract and return the following information in JSON format:

{{
    "personal_info": {{
        "name": "Full name",
        "email": "Email address",
        "phone": "Phone number",
        "location": "Location/Address",
        "linkedin": "LinkedIn URL",
        "github": "GitHub URL",
        "portfolio": "Portfolio URL"
    }},
    "summary": "Professional summary or objective",
    "skills": ["skill1", "skill2", ...],
    "education": [
        {{
            "degree": "Degree name",
            "institution": "University/College name",
            "field_of_study": "Major/Field",
            "start_date": "Start date",
            "end_date": "End date or Expected",
            "gpa": "GPA if mentioned",
            "description": "Additional details"
        }}
    ],
    "experience": [
        {{
            "title": "Job title",
            "company": "Company name",
            "location": "Location",
            "start_date": "Start date",
            "end_date": "End date or Present",
            "current": true/false,
            "description": "Job description",
            "responsibilities": ["responsibility1", "responsibility2", ...]
        }}
    ],
    "projects": [
        {{
            "name": "Project name",
            "description": "Project description",
            "technologies": ["tech1", "tech2", ...],
            "url": "Project URL if available",
            "start_date": "Start date",
            "end_date": "End date"
        }}
    ],
    "certifications": [
        {{
            "name": "Certification name",
            "issuer": "Issuing organization",
            "date": "Date obtained",
            "credential_id": "Credential ID",
            "url": "Verification URL"
        }}
    ],
    "languages": ["language1", "language2", ...],
    "total_experience_years": 0.0
}}

Important:
- Extract all available information accurately
- If information is not found, use null
- For dates, use the format mentioned in the resume
- Calculate total_experience_years based on work experience
- Be thorough and precise
"""

        try:
            response = await self.llm.ainvoke(prompt)
            
            # Extract content (Gemini 3 returns a list of dictionaries, earlier models return string)
            content = response.content
            if isinstance(content, list):
                # Concatenate all text parts
                content = "".join([part.get("text", "") for part in content if isinstance(part, dict)])
            
            # Extract JSON from response
            json_str = self._extract_json(content)
            parsed_json = json.loads(json_str)
            
            # Create ParsedResume object
            resume_data = {
                "filename": filename,
                "personal_info": PersonalInfo(**(parsed_json.get("personal_info") or {})),
                "summary": parsed_json.get("summary"),
                "skills": parsed_json.get("skills") or [],
                "education": [Education(**edu) for edu in (parsed_json.get("education") or [])],
                "experience": [Experience(**exp) for exp in (parsed_json.get("experience") or [])],
                "projects": [Project(**proj) for proj in (parsed_json.get("projects") or [])],
                "certifications": [Certification(**cert) for cert in (parsed_json.get("certifications") or [])],
                "languages": parsed_json.get("languages") or [],
                "total_experience_years": parsed_json.get("total_experience_years"),
                "parsed_at": datetime.now(),
                "raw_text": text
            }
            
            return ParsedResume(**resume_data)
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "ResourceExhausted" in error_msg:
                raise Exception("Google AI quota exceeded. Please wait a minute before trying again.")
            elif "API_KEY_INVALID" in error_msg:
                raise Exception("Invalid Google API Key. Please check your .env file.")
            raise Exception(f"Error parsing with AI: {error_msg}")
    
    def _extract_json(self, text: str) -> str:
        """
        Extract JSON from AI response
        """
        # Try to find JSON in code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # Try to find JSON directly
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        return text
