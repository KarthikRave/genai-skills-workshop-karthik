"""
Enhanced safety validation module for prompt filtering.
"""
from typing import Dict, Any
from vertexai.preview.generative_models import GenerativeModel
from config.app_settings import config
from utils.logger import setup_logger
from utils.exceptions import SafetyValidationError

logger = setup_logger(__name__)

class SafetyValidator:
    """Handles prompt safety validation using Gemini model."""
    
    def __init__(self):
        self.model = GenerativeModel(config.GENERATIVE_MODEL)
        self.safety_prompt_template = (
            "You are a content safety classifier for the Alaska Snow Department. "
            "Respond only with 'SAFE' or 'UNSAFE'. No explanation needed. "
            "Mark prompts containing hate speech, violence, illegal activities, "
            "harmful content, misleading information, or policy violations as 'UNSAFE'. "
            "Snow department related queries should generally be 'SAFE'.\n\n"
            "Prompt: {prompt}\nClassification:"
        )
    
    def validate_prompt_safety(self, prompt: str) -> bool:
        """
        Validate if a user prompt is safe for processing.
        
        Args:
            prompt: User input to validate
            
        Returns:
            True if prompt is safe, False otherwise
            
        Raises:
            SafetyValidationError: If validation process fails
        """
        if not prompt or not prompt.strip():
            logger.warning("Empty prompt received for safety validation")
            return False
        
        try:
            safety_prompt = self.safety_prompt_template.format(prompt=prompt)
            response = self.model.generate_content(safety_prompt)
            
            classification = response.text.strip().upper()
            
            if classification == "SAFE":
                logger.info(f"Prompt classified as SAFE: {prompt[:50]}...")
                return True
            elif classification == "UNSAFE":
                logger.warning(f"Prompt classified as UNSAFE: {prompt[:50]}...")
                return False
            else:
                logger.error(f"Unexpected safety classification: '{classification}'")
                return False  # Fail safely
                
        except Exception as e:
            logger.error(f"Safety validation failed: {str(e)}")
            raise SafetyValidationError(f"Safety validation error: {str(e)}")
    
    def get_validation_metrics(self, prompt: str) -> Dict[str, Any]:
        """
        Get detailed validation metrics for monitoring.
        
        Args:
            prompt: User input to analyze
            
        Returns:
            Dictionary with validation metrics
        """
        try:
            is_safe = self.validate_prompt_safety(prompt)
            return {
                "is_safe": is_safe,
                "prompt_length": len(prompt),
                "word_count": len(prompt.split()),
                "timestamp": logger.handlers[0].formatter.formatTime(
                    logging.LogRecord("", 0, "", 0, "", (), None)
                )
            }
        except Exception as e:
            return {
                "is_safe": False,
                "error": str(e),
                "prompt_length": len(prompt) if prompt else 0
            }

# Global validator instance
safety_validator = SafetyValidator()