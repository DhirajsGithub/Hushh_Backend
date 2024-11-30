from typing import List, Dict, Any
import pandas as pd
import numpy as np
from backend.ml_pipeline.models.external_api import OpenAIProcessor
from backend.ml_pipeline.models.local_model import LocalModelProcessor

class ModelComparator:
    def __init__(self, external_api_key: str, local_model_path: str):
        self.external_processor = OpenAIProcessor(external_api_key)
        self.local_processor = LocalModelProcessor(local_model_path)
    
    async def compare_processing(self, texts: List[str]) -> Dict[str, Any]:
        """
        Compare external and local model processing across multiple texts
        """
        results = {
            'external_results': [],
            'local_results': [],
            'comparison_metrics': {}
        }
        
        for text in texts:
            # Process with external API
            external_result = await self.external_processor.process_text(text)
            results['external_results'].append(external_result)
            
            # Process with local model
            local_result = await self.local_processor.process_text(text)
            results['local_results'].append(local_result)
        
        # Compute comparison metrics
        results['comparison_metrics'] = self._compute_comparison_metrics(
            results['external_results'], 
            results['local_results']
        )
        
        return results
    
    def _compute_comparison_metrics(self, external_results, local_results):
        """
        Compute detailed comparison metrics between models
        """
        metrics = {
            'entity_similarity': self._compute_entity_similarity(external_results, local_results),
            'sentiment_accuracy': self._compute_sentiment_accuracy(external_results, local_results),
            'insights_overlap': self._compute_insights_overlap(external_results, local_results)
        }
        return metrics
    
    def _compute_entity_similarity(self, external_results, local_results):
        """
        Compute similarity of extracted entities
        """
        similarities = []
        for ext, local in zip(external_results, local_results):
            # Jaccard similarity of entities
            ext_entities = set(ext.entities)
            local_entities = set(local.entities)
            
            similarity = len(ext_entities.intersection(local_entities)) / len(ext_entities.union(local_entities))
            similarities.append(similarity)
        
        return np.mean(similarities)
    
    def _compute_sentiment_accuracy(self, external_results, local_results):
        """
        Compare sentiment predictions
        """
        accuracies = []
        for ext, local in zip(external_results, local_results):
            accuracies.append(ext.sentiment == local.sentiment)
        
        return np.mean(accuracies)
    
    def _compute_insights_overlap(self, external_results, local_results):
        """
        Compute overlap of key insights
        """
        overlaps = []
        for ext, local in zip(external_results, local_results):
            ext_insights = set(ext.key_insights)
            local_insights = set(local.key_insights)
            
            overlap = len(ext_insights.intersection(local_insights)) / len(ext_insights.union(local_insights))
            overlaps.append(overlap)
        
        return np.mean(overlaps)