"""
Response generation module using RAG with BigQuery.
"""
from typing import List, Dict, Any, Optional
import pandas as pd
from google.cloud import bigquery
from vertexai.preview.generative_models import GenerativeModel, SafetySetting
from config.app_settings import config
from utils.logger import setup_logger
from utils.exceptions import RAGRetrievalError, ResponseGenerationError

logger = setup_logger(__name__)

class ResponseGenerator:
    """Handles RAG-based response generation."""
    
    def __init__(self):
        self.bq_client = bigquery.Client(project=config.PROJECT_ID)
        self.system_instruction = (
            "You are a helpful, professional assistant for the Alaska Snow Department. "
            "Provide accurate, concise responses based on the provided context. "
            "If the context doesn't contain relevant information, politely redirect "
            "the user to contact the department directly. Be friendly but professional."
        )
        
        self.chat_model = GenerativeModel(
            model_name=config.GENERATIVE_MODEL,
            system_instruction=self.system_instruction,
            safety_settings=self._get_safety_settings()
        )
    
    def _get_safety_settings(self) -> List[SafetySetting]:
        """Configure safety settings for the model."""
        return [
            SafetySetting(
                category="HARM_CATEGORY_HARASSMENT", 
                threshold=config.SAFETY_THRESHOLD
            ),
            SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH", 
                threshold=config.SAFETY_THRESHOLD
            ),
            SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT", 
                threshold=config.SAFETY_THRESHOLD
            ),
            SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT", 
                threshold=config.SAFETY_THRESHOLD
            ),
        ]
    
    def retrieve_relevant_context(self, user_question: str) -> pd.DataFrame:
        """
        Retrieve relevant FAQ context using vector search.
        
        Args:
            user_question: User's input question
            
        Returns:
            DataFrame with relevant context from BigQuery
            
        Raises:
            RAGRetrievalError: If context retrieval fails
        """
        try:
            query = f"""
            SELECT
                query.query,
                result.base.question,
                result.base.answer,
                result.distance
            FROM VECTOR_SEARCH(
                TABLE `{config.embedded_table_id}`,
                'embedding',
                (
                    SELECT
                        ml_generate_embedding_result AS embedding,
                        '{user_question}' AS query
                    FROM ML.GENERATE_EMBEDDING(
                        MODEL `{config.embedding_model_id}`,
                        (SELECT '{user_question}' AS content)
                    )
                ),
                top_k => {config.TOP_K_RESULTS},
                options => '{{"fraction_lists_to_search": 1.0}}'
            ) AS result
            WHERE result.distance <= {config.SIMILARITY_THRESHOLD}
            ORDER BY result.distance ASC
            """
            
            result_df = self.bq_client.query(query).to_dataframe()
            logger.info(f"Retrieved {len(result_df)} relevant context items")
            return result_df
            
        except Exception as e:
            logger.error(f"Context retrieval failed: {str(e)}")
            raise RAGRetrievalError(f"Failed to retrieve context: {str(e)}")
    
    def build_context_prompt(self, user_input: str, context_df: pd.DataFrame) -> str:
        """
        Build a comprehensive prompt with context for the model.
        
        Args:
            user_input: User's question
            context_df: Relevant context from BigQuery
            
        Returns:
            Formatted prompt string
        """
        if context_df.empty:
            return (
                f"No specific FAQ information found for this query. "
                f"User question: {user_input}\n\n"
                f"Please provide a helpful response directing them to contact "
                f"the Alaska Snow Department directly."
            )
        
        context_sections = []
        for _, row in context_df.iterrows():
            context_sections.append(f"Q: {row['question']}\nA: {row['answer']}")
        
        context_text = "\n\n".join(context_sections)
        
        return (
            f"Based on the following Alaska Snow Department FAQ information, "
            f"please answer the user's question:\n\n"
            f"=== CONTEXT ===\n{context_text}\n\n"
            f"=== USER QUESTION ===\n{user_input}\n\n"
            f"Please provide a helpful, accurate response based on the context above."
        )
    
    def generate_assistant_response(self, user_input: str) -> str:
        """
        Generate a response using RAG with safety measures.
        
        Args:
            user_input: User's input question
            
        Returns:
            Generated response string
            
        Raises:
            ResponseGenerationError: If response generation fails
        """
        try:
            # Retrieve relevant context
            context_df = self.retrieve_relevant_context(user_input)
            
            # Build prompt with context
            prompt = self.build_context_prompt(user_input, context_df)
            
            # Generate response
            response = self.chat_model.generate_content(prompt)
            
            if not response or not response.text:
                raise ResponseGenerationError("Model returned empty response")
            
            logger.info(f"Successfully generated response for: {user_input[:50]}...")
            return response.text.strip()
            
        except RAGRetrievalError:
            # Re-raise RAG errors
            raise
        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}")
            raise ResponseGenerationError(f"Failed to generate response: {str(e)}")

# Global response generator instance
response_generator = ResponseGenerator()