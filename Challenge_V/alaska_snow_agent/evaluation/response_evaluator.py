"""
Enhanced evaluation module for response quality assessment.
"""
import pandas as pd
import re
from typing import Dict, Any, List, Tuple
from evaluate import load
from sentence_transformers import SentenceTransformer, util
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ResponseEvaluator:
    """Enhanced evaluator for AI response quality."""
    
    def __init__(self):
        # Load evaluation metrics
        self.rouge = load("rouge")
        self.bertscore = load("bertscore")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using improved regex.
        
        Args:
            text: Input text to split
            
        Returns:
            List of sentences
        """
        # Improved sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text.strip())
        return [s.strip() for s in sentences if s.strip()]
    
    def tokenize_words(self, text: str) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of words
        """
        return re.findall(r'\b\w+\b', text.lower())
    
    def compute_fluency_score(self, text: str) -> float:
        """
        Compute fluency score based on linguistic features.
        
        Args:
            text: Text to evaluate
            
        Returns:
            Fluency score (1-5 scale)
        """
        if not text or not text.strip():
            return 1.0
        
        sentences = self.split_into_sentences(text)
        words = self.tokenize_words(text)
        
        if not sentences or not words:
            return 1.0
        
        # Calculate metrics
        avg_sentence_length = len(words) / len(sentences)
        word_variety = len(set(words)) / len(words) if words else 0
        
        # Scoring logic
        score = 5.0  # Start with perfect score
        
        # Penalize very short or very long sentences
        if avg_sentence_length < 5:
            score -= 1.5
        elif avg_sentence_length > 25:
            score -= 1.0
        
        # Reward word variety
        if word_variety < 0.5:
            score -= 1.0
        elif word_variety > 0.8:
            score += 0.5
        
        # Ensure score is within bounds
        return max(1.0, min(5.0, score))
    
    def compute_semantic_similarity(self, reference: str, prediction: str) -> float:
        """
        Compute semantic similarity using sentence embeddings.
        
        Args:
            reference: Reference text
            prediction: Predicted text
            
        Returns:
            Similarity score (0-5 scale)
        """
        try:
            ref_embedding = self.embedding_model.encode(reference, convert_to_tensor=True)
            pred_embedding = self.embedding_model.encode(prediction, convert_to_tensor=True)
            
            cosine_similarity = util.pytorch_cos_sim(ref_embedding, pred_embedding).item()
            
            # Scale to 0-5 range
            return round(cosine_similarity * 5, 2)
            
        except Exception as e:
            logger.error(f"Semantic similarity computation failed: {e}")
            return 0.0
    
    def compute_comprehensive_metrics(self, reference: str, prediction: str) -> Dict[str, Any]:
        """
        Compute comprehensive evaluation metrics.
        
        Args:
            reference: Reference/expected text
            prediction: Model prediction
            
        Returns:
            Dictionary with all evaluation metrics
        """
        try:
            # ROUGE metrics
            rouge_result = self.rouge.compute(
                predictions=[prediction], 
                references=[reference]
            )
            
            # BERTScore metrics
            bert_result = self.bertscore.compute(
                predictions=[prediction], 
                references=[reference], 
                lang="en"
            )
            
            # Custom metrics
            fluency_score = self.compute_fluency_score(prediction)
            semantic_similarity = self.compute_semantic_similarity(reference, prediction)
            
            # Additional metrics
            length_ratio = len(prediction) / max(len(reference), 1)
            word_overlap = self._compute_word_overlap(reference, prediction)
            
            return {
                "reference": reference,
                "prediction": prediction,
                "rouge1": rouge_result["rouge1"],
                "rouge2": rouge_result["rouge2"],
                "rougeL": rouge_result["rougeL"],
                "rougeLsum": rouge_result.get("rougeLsum", 0),
                "bertscore_precision": bert_result["precision"][0],
                "bertscore_recall": bert_result["recall"][0],
                "bertscore_f1": bert_result["f1"][0],
                "fluency_score": fluency_score,
                "semantic_similarity": semantic_similarity,
                "length_ratio": round(length_ratio, 3),
                "word_overlap": word_overlap
            }
            
        except Exception as e:
            logger.error(f"Comprehensive metrics computation failed: {e}")
            return self._get_default_metrics(reference, prediction)
    
    def _compute_word_overlap(self, reference: str, prediction: str) -> float:
        """Compute word overlap between reference and prediction."""
        ref_words = set(self.tokenize_words(reference))
        pred_words = set(self.tokenize_words(prediction))
        
        if not ref_words:
            return 0.0
        
        overlap = len(ref_words.intersection(pred_words))
        return round(overlap / len(ref_words), 3)
    
    def _get_default_metrics(self, reference: str, prediction: str) -> Dict[str, Any]:
        """Return default metrics in case of computation failure."""
        return {
            "reference": reference,
            "prediction": prediction,
            "rouge1": 0.0,
            "rouge2": 0.0,
            "rougeL": 0.0,
            "rougeLsum": 0.0,
            "bertscore_precision": 0.0,
            "bertscore_recall": 0.0,
            "bertscore_f1": 0.0,
            "fluency_score": 1.0,
            "semantic_similarity": 0.0,
            "length_ratio": 0.0,
            "word_overlap": 0.0,
            "error": True
        }
    
    def evaluate_response_quality(self, reference: str, prediction: str) -> pd.DataFrame:
        """
        Evaluate response quality and return as DataFrame.
        
        Args:
            reference: Reference/expected text
            prediction: Model prediction
            
        Returns:
            DataFrame with evaluation metrics
        """
        metrics = self.compute_comprehensive_metrics(reference, prediction)
        return pd.DataFrame([metrics])

# Global evaluator instance
response_evaluator = ResponseEvaluator()

# Backward compatibility function
def evaluate_text(reference: str, prediction: str) -> pd.DataFrame:
    """
    Backward compatibility function for the old API.
    
    Args:
        reference: Reference text
        prediction: Predicted text
        
    Returns:
        DataFrame with evaluation metrics
    """
    return response_evaluator.evaluate_response_quality(reference, prediction)