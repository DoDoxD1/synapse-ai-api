from app.ai.openai_client import OpenAIClient
from app.models.topic import Topic
from typing import Dict
import json


class QuestionGenerator:
    """Generate practice questions using AI"""
    
    def __init__(self):
        self.client = OpenAIClient()
    
    async def generate_mcq(
        self,
        topic: Topic,
        difficulty: str,
        exam_type: str
    ) -> Dict:
        """Generate multiple choice question"""
        
        prompt = f"""Generate a {difficulty} difficulty {exam_type} question on the topic: {topic.name}

Topic Description: {topic.description}

Requirements:
1. Create a realistic exam-style question
2. Provide exactly 4 options (A, B, C, D)
3. Include detailed step-by-step explanation
4. Mark correct answer
5. Add 2-3 relevant tags

Return JSON format:
{{
    "question_text": "...",
    "options": {{
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "..."
    }},
    "correct_answer": "A",
    "explanation": "Step 1: ... Step 2: ... ",
    "tags": ["tag1", "tag2"]
}}"""
        
        response = await self.client.generate_with_retry(
            prompt,
            temperature=0.8,
            response_format={"type": "json_object"}
        )
        
        question_data = json.loads(response)
        question_data["topic_id"] = topic.id
        question_data["exam_type"] = exam_type
        question_data["difficulty"] = difficulty
        question_data["question_type"] = "mcq"
        question_data["source"] = "ai_generated"
        
        return question_data
    
    async def generate_numeric(
        self,
        topic: Topic,
        difficulty: str,
        exam_type: str
    ) -> Dict:
        """Generate numeric answer question"""
        
        prompt = f"""Generate a {difficulty} difficulty {exam_type} numeric question on the topic: {topic.name}

Topic Description: {topic.description}

Requirements:
1. Question requires a numeric answer
2. Include detailed step-by-step explanation
3. Provide correct numeric answer
4. Add 2-3 relevant tags

Return JSON format:
{{
    "question_text": "...",
    "correct_answer": "42.5",
    "explanation": "Step 1: ... Step 2: ... ",
    "tags": ["tag1", "tag2"],
    "unit": "meters" (optional)
}}"""
        
        response = await self.client.generate_with_retry(
            prompt,
            temperature=0.8,
            response_format={"type": "json_object"}
        )
        
        question_data = json.loads(response)
        question_data["topic_id"] = topic.id
        question_data["exam_type"] = exam_type
        question_data["difficulty"] = difficulty
        question_data["question_type"] = "numeric"
        question_data["source"] = "ai_generated"
        question_data["options"] = None
        
        return question_data
    
    async def generate_explanation(self, question_text: str, user_answer: str, correct_answer: str) -> str:
        """Generate personalized explanation for incorrect answer"""
        
        prompt = f"""A student answered this question incorrectly:

Question: {question_text}
Student's Answer: {user_answer}
Correct Answer: {correct_answer}

Provide a helpful, encouraging explanation that:
1. Explains why the correct answer is right
2. Identifies the likely misconception in the student's answer
3. Provides a clear step-by-step solution
4. Encourages the student to keep learning

Keep it concise but thorough (200-300 words)."""
        
        return await self.client.generate_with_retry(prompt, temperature=0.7)
