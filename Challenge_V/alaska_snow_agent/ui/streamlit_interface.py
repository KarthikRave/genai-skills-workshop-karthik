"""
Enhanced Streamlit interface for the Alaska Snow Department AI Agent.
"""
import streamlit as st
import sys
import os
from typing import Dict, Any

# Add parent directory to path for imports
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from app.core_engine import alaska_agent
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="Alaska Snow Department Assistant",
    page_icon="❄️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #1f4e79;
    margin-bottom: 2rem;
}
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
.user-message {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
}
.bot-message {
    background-color: #f5f5f5;
    border-left: 4px solid #4caf50;
}
.error-message {
    background-color: #ffebee;
    border-left: 4px solid #f44336;
    color: #c62828;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "clear_input" not in st.session_state:
        st.session_state.clear_input = False
    if "request_count" not in st.session_state:
        st.session_state.request_count = 0

def display_message(role: str, content: str, is_error: bool = False):
    """
    Display a chat message with appropriate styling.
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
        is_error: Whether this is an error message
    """
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        css_class = "error-message" if is_error else "bot-message"
        st.markdown(f"""
        <div class="chat-message {css_class}">
            <strong>Alaska Snow Assistant:</strong> {content}
        </div>
        """, unsafe_allow_html=True)

def display_chat_history():
    """Display the chat history."""
    for msg in st.session_state.messages:
        is_error = msg.get("is_error", False)
        display_message(msg["role"], msg["content"], is_error)

def process_user_input(user_input: str):
    """
    Process user input and generate response.
    
    Args:
        user_input: User's message
    """
    # Add user message to history
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input,
        "is_error": False
    })
    
    # Process the request
    with st.spinner("🤖 Generating response..."):
        try:
            result = alaska_agent.process_user_request(user_input)
            
            # Add response to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": result["response"],
                "is_error": not result["success"]
            })
            
            # Update request count
            st.session_state.request_count += 1
            
            # Log the interaction
            logger.info(f"Processed request {result['request_id']}: success={result['success']}")
            
        except Exception as e:
            # Handle unexpected errors
            error_message = "I apologize, but I'm experiencing technical difficulties. Please try again later."
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message,
                "is_error": True
            })
            logger.error(f"Unexpected error in UI: {str(e)}")

def main():
    """Main Streamlit application."""
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">❄️ Alaska Snow Department Assistant</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Welcome! I'm here to help you with questions about snow removal services, 
    road conditions, and Alaska Snow Department policies. How can I assist you today?
    """)
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ Information")
        st.write(f"**Requests processed:** {st.session_state.request_count}")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.request_count = 0
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        **Emergency Contact:**
        - Phone: 1-800-SNOW-HELP
        - Email: help@alaskasnow.gov
        
        **Office Hours:**
        - Mon-Fri: 8:00 AM - 6:00 PM
        - Sat-Sun: 9:00 AM - 4:00 PM
        """)
    
    # Chat history display
    chat_container = st.container()
    with chat_container:
        display_chat_history()
    
    # Input handling
    if st.session_state.clear_input:
        st.session_state.user_input = ""
        st.session_state.clear_input = False
    
    # User input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your message:",
            key="user_input",
            placeholder="e.g., How do I report an unplowed road?"
        )
    
    with col2:
        send_button = st.button("Send 📤", use_container_width=True)
    
    # Process input
    if (send_button or user_input) and user_input.strip():
        process_user_input(user_input.strip())
        st.session_state.clear_input = True
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8em;">
        Alaska Snow Department AI Assistant | Powered by Google Cloud & Gemini
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()