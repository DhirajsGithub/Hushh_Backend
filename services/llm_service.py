from backend.ml_pipeline.models.external_api import OpenAIProcessor
from backend.ml_pipeline.models.local_model import LocalModelProcessor
from backend.ml_pipeline.prompts.template import PromptTemplate
from typing import List, Dict, Any

class LLMService:
    def __init__(self, external_api_key: str, local_model_path: str):
        self.external_processor = OpenAIProcessor(external_api_key)
        self.local_processor = LocalModelProcessor(local_model_path)
    
    async def process_text(self, text: str, processing_type: str = 'all') -> Dict[str, Any]:
        """
        Process text using different LLM techniques
        """
        results = {}
        
        if processing_type in ['all', 'entities']:
            results['entities'] = await self._extract_entities(text)
        
        if processing_type in ['all', 'sentiment']:
            results['sentiment'] = await self._analyze_sentiment(text)
        
        if processing_type in ['all', 'insights']:
            results['key_insights'] = await self._extract_key_insights(text)
        
        return results
    
    async def _extract_entities(self, text: str):
        # Use prompt template for entity extraction
        prompt = PromptTemplate.entity_extraction_prompt(text)
        
        # Process with both external and local models
        external_result = await self.external_processor.process_text(prompt)
        local_result = await self.local_processor.process_text(prompt)
        
        return {
            'external': external_result.entities,
            'local': local_result.entities
        }
    
    async def _analyze_sentiment(self, text: str):
        # Use prompt template for sentiment analysis
        prompt = PromptTemplate.sentiment_analysis_prompt(text)
        
        # Process with both external and local models
        external_result = await self.external_processor.process_text(prompt)
        local_result = await self.local_processor.process_text(prompt)
        
        return {
            'external_sentiment': external_result.sentiment,
            'local_sentiment': local_result.sentiment
        }
    
    async def _extract_key_insights(self, text: str):
        # Use prompt template for key insights
        prompt = PromptTemplate.key_insights_prompt(text)
        
        # Process with both external and local models
        external_result = await self.external_processor.process_text(prompt)
        local_result = await self.local_processor.process_text(prompt)
        
        return {
            'external_insights': external_result.key_insights,
            'local_insights': local_result.key_insights
        }