import json
import re
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

class QuestionGenerator:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            api_key=settings.GOOGLE_API_KEY,
            temperature=0.7
        )
    
    async def generate_questions(self, skills: List[str], experience_years: float = 0) -> List[Dict[str, Any]]:
        """
        Generate skill-based interview questions with answers
        """
        # Determine difficulty level based on experience
        if experience_years < 2:
            difficulty = "beginner to intermediate"
        elif experience_years < 5:
            difficulty = "intermediate"
        else:
            difficulty = "intermediate to advanced"
        
        # Create skills string
        skills_str = ", ".join(skills[:10])  # Limit to top 10 skills
        
        prompt = f"""
You are an expert technical interviewer. Generate exactly 12 medium-level interview questions based on the following skills: {skills_str}

The candidate has {experience_years} years of experience, so questions should be at {difficulty} level.

Generate questions that:
1. Test practical knowledge and problem-solving
2. Cover different aspects of the skills mentioned
3. Are realistic interview questions
4. Have detailed, comprehensive answers

Return the response in the following JSON format:

{{
    "questions": [
        {{
            "id": 1,
            "skill": "Primary skill being tested",
            "question": "The interview question",
            "answer": "Detailed answer with explanation",
            "difficulty": "medium",
            "topics": ["topic1", "topic2"]
        }}
    ]
}}

Important:
- Generate EXACTLY 12 questions
- Each answer should be 3-5 sentences long
- Cover variety of skills from the list
- Make questions practical and scenario-based where possible
- Ensure answers are technically accurate and comprehensive
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
            
            questions = parsed_json.get("questions", [])
            
            # Ensure we have exactly 12 questions
            if len(questions) < 12:
                # If less than 12, generate more
                return await self._ensure_twelve_questions(skills, experience_years, questions)
            
            return questions[:12]  # Return exactly 12
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "ResourceExhausted" in error_msg:
                # Return fallback questions instead of crashing if quota is hit
                return self._generate_fallback_questions(skills)
            raise Exception(f"Error generating questions: {error_msg}")
    
    async def _ensure_twelve_questions(self, skills: List[str], experience_years: float, existing_questions: List[Dict]) -> List[Dict]:
        """
        Ensure we have exactly 12 questions by generating more if needed
        """
        # If we have some questions, just return them padded
        # Otherwise, return a default set
        if len(existing_questions) >= 8:
            return existing_questions[:12]
        
        # Generate a simpler set if AI fails
        return self._generate_fallback_questions(skills)
    
    def _generate_fallback_questions(self, skills: List[str]) -> List[Dict]:
        """
        Generate fallback questions if AI generation fails
        """
        fallback = []
        for i, skill in enumerate(skills[:12], 1):
            fallback.append({
                "id": i,
                "skill": skill,
                "question": f"Explain your experience with {skill} and how you've used it in your projects.",
                "answer": f"This question assesses practical experience with {skill}. A good answer should include specific projects, challenges faced, and solutions implemented using {skill}.",
                "difficulty": "medium",
                "topics": [skill, "practical experience", "problem-solving"]
            })
        
        # Pad to 12 if needed
        while len(fallback) < 12:
            fallback.append({
                "id": len(fallback) + 1,
                "skill": "General",
                "question": "Describe a challenging technical problem you solved recently.",
                "answer": "This question evaluates problem-solving skills. Include the problem context, your approach, technologies used, and the outcome.",
                "difficulty": "medium",
                "topics": ["problem-solving", "technical skills"]
            })
        
        return fallback[:12]
    
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
