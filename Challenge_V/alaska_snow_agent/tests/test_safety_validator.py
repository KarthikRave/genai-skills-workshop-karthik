"""
Enhanced unit tests for safety validation.
"""
import unittest
from unittest.mock import patch, MagicMock
from app.safety_validator import SafetyValidator, safety_validator
from utils.exceptions import SafetyValidationError

class TestSafetyValidator(unittest.TestCase):
    """Test cases for safety validation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = SafetyValidator()
    
    @patch("app.safety_validator.GenerativeModel")
    def test_safe_prompt_validation(self, mock_model_class):
        """Test validation of safe prompts."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "SAFE"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        validator = SafetyValidator()
        result = validator.validate_prompt_safety("How do I get a snow removal permit?")
        
        self.assertTrue(result)
        mock_model.generate_content.assert_called_once()
    
    @patch("app.safety_validator.GenerativeModel")
    def test_unsafe_prompt_validation(self, mock_model_class):
        """Test validation of unsafe prompts."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "UNSAFE"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        validator = SafetyValidator()
        result = validator.validate_prompt_safety("How to create harmful substances?")
        
        self.assertFalse(result)
    
    @patch("app.safety_validator.GenerativeModel")
    def test_unexpected_response_handling(self, mock_model_class):
        """Test handling of unexpected model responses."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "MAYBE"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        validator = SafetyValidator()
        result = validator.validate_prompt_safety("Unclear input")
        
        self.assertFalse(result)  # Should default to unsafe
    
    @patch("app.safety_validator.GenerativeModel")
    def test_model_error_handling(self, mock_model_class):
        """Test handling of model errors."""
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("Model error")
        mock_model_class.return_value = mock_model
        
        validator = SafetyValidator()
        
        with self.assertRaises(SafetyValidationError):
            validator.validate_prompt_safety("Test prompt")
    
    def test_empty_prompt_handling(self):
        """Test handling of empty prompts."""
        result = self.validator.validate_prompt_safety("")
        self.assertFalse(result)
        
        result = self.validator.validate_prompt_safety("   ")
        self.assertFalse(result)
    
    def test_validation_metrics(self):
        """Test validation metrics functionality."""
        with patch.object(self.validator, 'validate_prompt_safety', return_value=True):
            metrics = self.validator.get_validation_metrics("Test prompt")
            
            self.assertIn("is_safe", metrics)
            self.assertIn("prompt_length", metrics)
            self.assertIn("word_count", metrics)
            self.assertTrue(metrics["is_safe"])
            self.assertEqual(metrics["prompt_length"], 11)
            self.assertEqual(metrics["word_count"], 2)

if __name__ == "__main__":
    unittest.main()