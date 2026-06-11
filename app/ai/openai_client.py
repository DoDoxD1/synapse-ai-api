from openai import AsyncOpenAI
from app.config import settings
from typing import Optional, List, Dict
import tiktoken
import asyncio


class OpenAIClient:
    """Wrapper for OpenAI API with retry logic and error handling"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.encoding = tiktoken.encoding_for_model("gpt-4")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None,
        response_format: Optional[dict] = None
    ) -> str:
        """Get chat completion from OpenAI"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or settings.OPENAI_TEMPERATURE,
                max_tokens=max_tokens or settings.OPENAI_MAX_TOKENS,
                response_format=response_format
            )
            return response.choices[0].message.content
        except Exception as e:
            # Log error
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    async def generate_with_retry(
        self,
        prompt: str,
        max_retries: int = 3,
        **kwargs
    ) -> str:
        """Generate with retry logic"""
        for attempt in range(max_retries):
            try:
                messages = [{"role": "user", "content": prompt}]
                return await self.chat_completion(messages, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                # Wait before retry (exponential backoff)
                await asyncio.sleep(2 ** attempt)
