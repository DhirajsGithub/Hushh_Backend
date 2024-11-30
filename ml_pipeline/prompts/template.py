from typing import List, Optional
from pydantic import BaseModel, Field

class PromptTemplate:
    @staticmethod
    def entity_extraction_prompt(text: str) -> str:
        """
        Generate a prompt for named entity extraction
        """
        return f"""
        Extract and categorize named entities from the following text:
        TEXT: {text}
        
        Instructions:
        1. Identify all named entities
        2. Categorize them (e.g., Person, Organization, Location)
        3. Provide confidence score for each entity
        
        Output Format:
        [
            {{
                "entity": "...",
                "type": "...",
                "confidence": 0.0-1.0
            }}
        ]
        """
    
    @staticmethod
    def sentiment_analysis_prompt(text: str) -> str:
        """
        Generate a prompt for sentiment analysis
        """
        return f"""
        Perform a detailed sentiment analysis on the following text:
        TEXT: {text}
        
        Analysis Requirements:
        1. Overall sentiment (Positive/Negative/Neutral)
        2. Sentiment score (-1.0 to 1.0)
        3. Key emotional indicators
        4. Contextual nuances
        
        Output Format:
        {{
            "sentiment": "...",
            "score": 0.0,
            "emotional_indicators": [...],
            "reasoning": "..."
        }}
        """
    
    @staticmethod
    def key_insights_prompt(text: str) -> str:
        """
        Generate a prompt for extracting key insights
        """
        return f"""
        Extract key insights from the following text:
        TEXT: {text}
        
        Extraction Guidelines:
        1. Identify 3-5 most important points
        2. Summarize each insight concisely
        3. Provide relevance score
        4. Highlight potential action items
        
        Output Format:
        [
            {{
                "insight": "...",
                "relevance_score": 0.0-1.0,
                "action_potential": "..."
            }}
        ]
        """

class PromptResponse(BaseModel):
    text: str
    tokens: Optional[int] = Field(None, description="Number of tokens")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    max_tokens: Optional[int] = Field(500, description="Maximum response tokens")