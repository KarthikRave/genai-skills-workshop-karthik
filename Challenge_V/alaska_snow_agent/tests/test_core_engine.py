"""
Enhanced unit tests for the core engine.
"""
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from app.core_engine import alaska_agent, AlaskaSnowAgent
from evaluation.response_evaluator import response_evaluator
from utils.exceptions import SafetyValidationError, ResponseGenerationError

class TestCoreEngine(unittest.TestCase):
    """Test cases for the core engine functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = AlaskaSnowAgent()
        self.test_questions = [
            "What about unplowed roads?",
            "How do I report snow issues?",
            "What are your office hours?"
        ]
    
    def test_valid_snow_department_query(self):
        """Test valid Alaska Snow Department queries."""
        question = "How do I report an unplowed road?"
        
        expected_response = (
            "You can report an unplowed road by contacting your local ADS regional office. "
            "Each region has a dedicated hotline for snow-related service requests and emergencies."
        )
        
        with patch.object(alaska_agent.safety_validator, 'validate_prompt_safety', return_value=True), \
             patch.object(alaska_agent.response_generator, 'generate_assistant_response', return_value=expected_response):
            
            result = alaska_agent.process_user_request(question)
            
            self.assertTrue(result["success"])
            self.assertTrue(result["safety_passed"])
            self.assertIn("report", result["response"].lower())
            
            # Evaluate response quality
            eval_df = response_evaluator.evaluate_response_quality(expected_response, result["response"])
            
            fluency = float(eval_df["fluency_score"].iloc[0])
            semantic_sim = float(eval_df["semantic_similarity"].iloc[0])
            
            self.assertGreaterEqual(fluency, 3.0, "Fluency score too low for valid response")
            self.assertGreaterEqual(semantic_sim, 3.0, "Semantic similarity too low for valid response")
    
    def test_irrelevant_query_handling(self):
        """Test handling of irrelevant queries."""
        question = "How do I apply for a driver's license?"
        
        expected_response = (
            "I'm sorry, I am only an assistant for the Alaska Snow Department. "
            "For information about driver's licenses, please visit the Alaska DMV."
        )
        
        with patch.object(alaska_agent.safety_validator, 'validate_prompt_safety', return_value=True), \
             patch.object(alaska_agent.response_generator, 'generate_assistant_response', return_value=expected_response):
            
            result = alaska_agent.process_user_request(question)
            
            self.assertTrue(result["success"])
            self.assertTrue(result["safety_passed"])
            
            # Evaluate response quality
            eval_df = response_evaluator.evaluate_response_quality(expected_response, result["response"])
            
            semantic_sim = float(eval_df["semantic_similarity"].iloc[0])
            self.assertLessEqual(semantic_sim, 4.0, f"Expected low similarity for unrelated query, got {semantic_sim}")
    
    def test_safety_validation_failure(self):
        """Test safety validation failure handling."""
        unsafe_question = "How to make a dangerous device?"
        
        with patch.object(alaska_agent.safety_validator, 'validate_prompt_safety', return_value=False):
            result = alaska_agent.process_user_request(unsafe_question)
            
            self.assertFalse(result["success"])
            self.assertFalse(result["safety_passed"])
            self.assertIn("safety", result["response"].lower())
    
    def test_response_generation_error_handling(self):
        """Test response generation error handling."""
        question = "What are your services?"
        
        with patch.object(alaska_agent.safety_validator, 'validate_prompt_safety', return_value=True), \
             patch.object(alaska_agent.response_generator, 'generate_assistant_response', 
                         side_effect=ResponseGenerationError("Test error")):
            
            result = alaska_agent.process_user_request(question)
            
            self.assertFalse(result["success"])
            self.assertTrue(result["safety_passed"])
            self.assertIn("technical difficulties", result["response"])
    
    def test_health_check(self):
        """Test health check functionality."""
        with patch.object(alaska_agent.safety_validator, 'validate_prompt_safety', return_value=True):
            health_status = alaska_agent.health_check()
            
            self.assertIn("overall_healthy", health_status)
            self.assertIn("components", health_status)
            self.assertIn("safety_validator", health_status["components"])
            self.assertIn("response_generator", health_status["components"])

class TestResponseQualityMetrics(unittest.TestCase):
    """Test cases for response quality evaluation."""
    
    def test_fluency_scoring(self):
        """Test fluency scoring algorithm."""
        # Test high fluency text
        high_fluency = "The Alaska Snow Department provides comprehensive snow removal services throughout the state."
        score = response_evaluator.compute_fluency_score(high_fluency)
        self.assertGreaterEqual(score, 4.0)
        
        # Test low fluency text
        low_fluency = "Snow. Department. Services. Available."
        score = response_evaluator.compute_fluency_score(low_fluency)
        self.assertLessEqual(score, 3.0)
    
    def test_semantic_similarity(self):
        """Test semantic similarity computation."""
        reference = "Contact the Alaska Snow Department for road issues."
        similar = "Reach out to Alaska Snow Department regarding road problems."
        dissimilar = "The weather is nice today."
        
        similar_score = response_evaluator.compute_semantic_similarity(reference, similar)
        dissimilar_score = response_evaluator.compute_semantic_similarity(reference, dissimilar)
        
        self.assertGreater(similar_score, dissimilar_score)

def save_evaluation_results(df: pd.DataFrame, filename: str):
    """Save evaluation results to file."""
    import os
    from tabulate import tabulate
    
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)
    
    with open(filepath, "w") as f:
        f.write(tabulate(df, headers="keys", tablefmt="grid", showindex=False))

if __name__ == "__main__":
    unittest.main()