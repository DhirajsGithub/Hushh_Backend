from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from backend.ml_pipeline.models.external_api import OpenAIProcessor
from backend.ml_pipeline.models.local_model import LocalModelProcessor
from backend.config.settings import settings

router = APIRouter(prefix="/llm", tags=["llm"])

class TextProcessRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000)

class ProcessedOutput(BaseModel):
    entities: List[str]
    sentiment: str
    key_insights: List[str]
    source: str

@router.post("/process", response_model=ProcessedOutput)
async def process_text(request: TextProcessRequest):
    try:
        # External API Processing
        external_processor = OpenAIProcessor(settings.OPENAI_API_KEY)
        external_result = await external_processor.process_text(request.text)
        
        # Local Model Processing
        local_processor = LocalModelProcessor(settings.LOCAL_MODEL_PATH)
        local_result = await local_processor.process_text(request.text)
        
        # Choose preferred result or combine
        return ProcessedOutput(
            entities=external_result.entities,
            sentiment=external_result.sentiment,
            key_insights=local_result.key_insights,
            source="combined"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))