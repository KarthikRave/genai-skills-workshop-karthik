"""
Core engine that orchestrates the AI agent functionality.
"""
from typing import Dict, Any, Optional
from app.safety_validator import safety_validator
from app.response_generator import response_generator
from utils.logger import setup_logger
from utils.exceptions import (
    SafetyValidationError, 
    RAGRetrievalError, 
    ResponseGenerationError
)

logger = setup_logger(__name__)

class AlaskaSnowAgent:
    """Main orchestrator for the Alaska Snow Department AI Agent."""
    
    def __init__(self):
        self.safety_validator = safety_validator
        self.response_generator = response_generator
        self.default_error_message = (
            "I apologize, but I'm experiencing technical difficulties. "
            "Please contact the Alaska Snow Department directly for assistance."
        )
        self.safety_blocked_message = (
            "I'm sorry, but your message was flagged by our safety filters. "
            "Please rephrase your question and try again."
        )
    
    def process_user_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process a user request end-to-end with safety and error handling.
        
        Args:
            user_input: User's input message
            
        Returns:
            Dictionary containing response and metadata
        """
        request_id = id(user_input)  # Simple request tracking
        logger.info(f"Processing request {request_id}: {user_input[:100]}...")
        
        result = {
            "request_id": request_id,
            "user_input": user_input,
            "response": "",
            "success": False,
            "error": None,
            "safety_passed": False,
            "context_retrieved": False
        }
        
        try:
            # Step 1: Safety validation
            if not self.safety_validator.validate_prompt_safety(user_input):
                result["response"] = self.safety_blocked_message
                result["error"] = "Safety validation failed"
                logger.warning(f"Request {request_id} blocked by safety filter")
                return result
            
            result["safety_passed"] = True
            
            # Step 2: Generate response
            response = self.response_generator.generate_assistant_response(user_input)
            result["response"] = response
            result["context_retrieved"] = True
            result["success"] = True
            
            logger.info(f"Request {request_id} processed successfully")
            
        except SafetyValidationError as e:
            result["response"] = self.safety_blocked_message
            result["error"] = str(e)
            logger.error(f"Safety validation error for request {request_id}: {e}")
            
        except (RAGRetrievalError, ResponseGenerationError) as e:
            result["response"] = self.default_error_message
            result["error"] = str(e)
            logger.error(f"Processing error for request {request_id}: {e}")
            
        except Exception as e:
            result["response"] = self.default_error_message
            result["error"] = f"Unexpected error: {str(e)}"
            logger.error(f"Unexpected error for request {request_id}: {e}")
        
        return result
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of all components.
        
        Returns:
            Health status of all components
        """
        health_status = {
            "overall_healthy": True,
            "components": {}
        }
        
        # Check safety validator
        try:
            test_result = self.safety_validator.validate_prompt_safety("test message")
            health_status["components"]["safety_validator"] = {
                "healthy": True,
                "test_result": test_result
            }
        except Exception as e:
            health_status["components"]["safety_validator"] = {
                "healthy": False,
                "error": str(e)
            }
            health_status["overall_healthy"] = False
        
        # Check response generator (simplified)
        try:
            # This is a basic check - in production you might want more thorough testing
            health_status["components"]["response_generator"] = {
                "healthy": True,
                "bigquery_client": str(type(self.response_generator.bq_client))
            }
        except Exception as e:
            health_status["components"]["response_generator"] = {
                "healthy": False,
                "error": str(e)
            }
            health_status["overall_healthy"] = False
        
        return health_status

# Global agent instance
alaska_agent = AlaskaSnowAgent()

# Backward compatibility functions
def generate_assistant_response(user_input: str) -> str:
    """
    Backward compatibility function for the old API.
    
    Args:
        user_input: User's input message
        
    Returns:
        Generated response string
    """
    result = alaska_agent.process_user_request(user_input)
    return result["response"]

def validate_prompt_safety(prompt: str) -> bool:
    """
    Backward compatibility function for safety validation.
    
    Args:
        prompt: Prompt to validate
        
    Returns:
        True if safe, False otherwise
    """
    return safety_validator.validate_prompt_safety(prompt)