# ❄️ Alaska Snow Department AI Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com)

A production-ready, intelligent conversational AI agent designed specifically for the Alaska Department of Snow. This system provides citizens with instant, accurate information about snow removal services, road conditions, emergency procedures, and departmental policies through an intuitive chat interface.

## 🌟 **Live Demo**
**Production URL:** [https://streamlit-app-422208597976.us-central1.run.app/](https://streamlit-app-422208597976.us-central1.run.app/)

## 🏗️ **Architecture Overview**

This AI agent leverages cutting-edge technologies to deliver reliable, safe, and contextually accurate responses:

- **🔍 RAG (Retrieval-Augmented Generation)** - Combines real-time information retrieval with generative AI
- **🛡️ Multi-layer Safety Filtering** - LLM-powered content validation and safety checks
- **📊 BigQuery Vector Search** - High-performance semantic search using Google Cloud
- **🤖 Gemini 2.0 Flash** - Advanced language model for natural conversation
- **⚡ Real-time Processing** - Sub-second response times with intelligent caching

## 📁 **Project Structure**

```
alaska_snow_agent/
├── app/
│   ├── __init__.py
│   ├── core_engine.py          # Main orchestrator (renamed from backend.py)
│   ├── safety_validator.py     # Enhanced safety validation (renamed from filters.py)
│   └── response_generator.py   # RAG response generation (new module)
├── config/
│   ├── __init__.py
│   └── app_settings.py         # Centralized configuration (renamed from settings.py)
├── ui/
│   ├── __init__.py
│   └── streamlit_interface.py  # Enhanced Streamlit UI (renamed from main.py)
├── evaluation/
│   ├── __init__.py
│   └── response_evaluator.py   # Enhanced evaluation (renamed from evaluator.py)
├── tests/
│   ├── __init__.py
│   ├── test_core_engine.py     # Core tests (renamed from test_backend_agent.py)
│   └── test_safety_validator.py # Safety tests (renamed from test_filters.py)
├── utils/                      # New utility modules
│   ├── __init__.py
│   ├── logger.py              # Centralized logging (new)
│   └── exceptions.py          # Custom exceptions (new)
├── requirements.txt            # Enhanced dependencies
├── Dockerfile                  # Production container configuration
├── RAG_BigQuery_Datastore.ipynb # Data processing notebook
└── README.md                   # This documentation
```

## ✨ **Key Features & Code Improvements**

### 🔄 **Enhanced Function Names & Architecture**
- **`AlaskaSnowAgent`**: Main orchestrator class for end-to-end request processing
- **`validate_prompt_safety()`**: Improved from `is_prompt_safe_llm()` with detailed metrics
- **`generate_assistant_response()`**: Enhanced from `generate_bot_response()` with better error handling
- **`retrieve_relevant_context()`**: Upgraded from `fetch_faq_results()` with similarity thresholds

### 🛡️ **Advanced Safety & Validation** (`app/safety_validator.py`)
- **`SafetyValidator` Class**: Centralized safety validation with metrics tracking
- **Multi-tier Content Filtering**: LLM-powered safety validation with customizable thresholds
- **`get_validation_metrics()`**: Detailed validation analytics and monitoring
- **Custom Safety Prompts**: Specialized templates for Alaska Snow Department context

### 🔍 **Intelligent RAG System** (`app/response_generator.py`)
- **`ResponseGenerator` Class**: Dedicated RAG implementation with BigQuery integration
- **`retrieve_relevant_context()`**: Vector search with configurable similarity thresholds
- **`build_context_prompt()`**: Dynamic prompt construction with retrieved context
- **Error Recovery**: Graceful handling of retrieval failures with fallback responses

### 📊 **Enhanced Evaluation** (`evaluation/response_evaluator.py`)
- **`ResponseEvaluator` Class**: Comprehensive response quality assessment
- **`compute_fluency_score()`**: Improved from `compute_fluency()` with linguistic analysis
- **`compute_semantic_similarity()`**: Advanced semantic matching using sentence transformers
- **Multiple Metrics**: ROUGE, BERTScore, word overlap, and custom domain-specific scores

### 🛠️ **Production-Ready Infrastructure**
- **Custom Exception Handling** (`utils/exceptions.py`): Specific error types for different failure modes
- **Centralized Logging** (`utils/logger.py`): Structured logging with configurable levels
- **Health Monitoring**: Built-in system health checks via `alaska_agent.health_check()`
- **Configuration Management** (`config/app_settings.py`): Environment-aware settings with the `AppConfig` class

## 🔄 **Migration from Original Version**

### **Function Name Changes**

| Original Function | Improved Function | Location | Purpose |
|------------------|-------------------|----------|---------|
| `is_prompt_safe_llm()` | `validate_prompt_safety()` | `app/safety_validator.py` | Enhanced safety validation with metrics |
| `fetch_faq_results()` | `retrieve_relevant_context()` | `app/response_generator.py` | Better context retrieval with thresholds |
| `generate_bot_response()` | `generate_assistant_response()` | `app/response_generator.py` | Improved response generation |
| `simple_sentence_split()` | `split_into_sentences()` | `evaluation/response_evaluator.py` | Better text processing |
| `simple_word_tokenize()` | `tokenize_words()` | `evaluation/response_evaluator.py` | Enhanced tokenization |
| `compute_fluency()` | `compute_fluency_score()` | `evaluation/response_evaluator.py` | More accurate fluency scoring |
| `compute_groundedness()` | `compute_semantic_similarity()` | `evaluation/response_evaluator.py` | Better semantic analysis |
| `evaluate_text()` | `evaluate_response_quality()` | `evaluation/response_evaluator.py` | Comprehensive evaluation |

### **New Architecture Benefits**

- **`AlaskaSnowAgent`**: Central orchestrator replacing scattered function calls
- **Modular Design**: Separated concerns into dedicated classes
- **Better Error Handling**: Custom exceptions and comprehensive logging
- **Production Ready**: Health checks, monitoring, and configuration management
- **Backward Compatibility**: Old function calls still work through wrapper functions

## 🚀 **Quick Start**

### Prerequisites
- Python 3.10 or higher
- Google Cloud Platform account with billing enabled
- Service account credentials with appropriate permissions

### 🐍 **Local Development Setup**

```bash
# 1. Clone the repository
git clone <repository-url>
cd alaska_snow_agent

# 2. Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up Google Cloud credentials
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"

# 5. Configure application settings (optional)
cp config/app_settings.py.example config/app_settings.py
# Edit configuration as needed

# 6. Start the application
streamlit run ui/streamlit_interface.py
```

The application will be available at `http://localhost:8501`

### 🐳 **Docker Deployment**

```bash
# Build the container
docker build -t alaska-snow-agent .

# Run locally
docker run -p 8080:8080 \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  -v /path/to/credentials.json:/app/credentials.json \
  alaska-snow-agent
```

### ☁️ **Google Cloud Run Deployment**

```bash
# 1. Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/[PROJECT-ID]/alaska-snow-agent

# 2. Deploy to Cloud Run
gcloud run deploy alaska-snow-agent \
  --image gcr.io/[PROJECT-ID]/alaska-snow-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10

# 3. Set up custom domain (optional)
gcloud run domain-mappings create \
  --service alaska-snow-agent \
  --domain your-custom-domain.com
```

## 🔧 **Configuration**

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP service account key | `alaska_admin_key.json` | Yes |
| `PROJECT_ID` | Google Cloud Project ID | `qwiklabs-gcp-04-d9bb68112d04` | Yes |
| `DATASET_NAME` | BigQuery dataset name | `Alaska_Dataset` | Yes |
| `EMBEDDING_MODEL` | Text embedding model | `text-embedding-005` | No |
| `GENERATIVE_MODEL` | Generative AI model | `gemini-2.0-flash-001` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

## 🧪 **Testing**

### Running Tests

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py"

# Run specific test modules
python -m unittest tests.test_core_engine
python -m unittest tests.test_safety_validator

# Run with verbose output
python -m unittest discover -s tests -p "test_*.py" -v

# Test specific functionality
python -m unittest tests.test_core_engine.TestCoreEngine.test_valid_snow_department_query
```

### Test Structure

- **`test_core_engine.py`**: Tests for `AlaskaSnowAgent`, `generate_assistant_response()`, and end-to-end workflows
- **`test_safety_validator.py`**: Tests for `SafetyValidator.validate_prompt_safety()` and safety metrics
- **Evaluation Tests**: Response quality assessment using `ResponseEvaluator.evaluate_response_quality()`

## 📊 **Evaluation & Monitoring**

### Response Quality Metrics

The system uses comprehensive evaluation metrics to ensure high-quality responses:

- **📝 Fluency Score** (1-5): Linguistic quality and readability
- **🎯 Semantic Similarity** (0-5): Relevance to user intent
- **📏 ROUGE Scores**: N-gram overlap with reference responses
- **🧠 BERTScore**: Contextual similarity using neural embeddings
- **📊 Custom Metrics**: Domain-specific quality indicators

### Performance Monitoring

```bash
# View system health
curl https://your-deployment-url/_health

# Check performance metrics
curl https://your-deployment-url/_metrics

# View application logs
gcloud logging read "resource.type=cloud_run_revision"
```

## 🔒 **Security Features**

### Data Protection
- **Encryption at Rest**: All data encrypted using Google Cloud KMS
- **Encryption in Transit**: TLS 1.3 for all communications
- **Access Control**: Role-based access control (RBAC) with principle of least privilege
- **Audit Logging**: Comprehensive audit trails for compliance

### Content Safety
- **Input Validation**: Multi-layer validation of user inputs
- **Output Filtering**: Real-time scanning of generated responses
- **Bias Detection**: Monitoring for potential bias in AI responses
- **Privacy Protection**: Automatic PII detection and redaction

## 🌍 **Data Sources & RAG Pipeline**

### Primary Knowledge Base
- **Location**: `gs://labs.roitraining.com/alaska-dept-of-snow/alaska-dept-of-snow-faqs.csv`
- **Format**: Structured FAQ data in CSV format with questions and answers
- **Processing**: Automated via `RAG_BigQuery_Datastore.ipynb` notebook
- **Storage**: BigQuery with vector embeddings using `text-embedding-005`

### Data Pipeline Setup

The RAG system is configured using the included Jupyter notebook:

```bash
# Open the data processing notebook
jupyter notebook RAG_BigQuery_Datastore.ipynb
```

**Pipeline Steps:**
1. **CSV Upload**: Load FAQ data from Cloud Storage to BigQuery (`Alaska_Dataset_data`)
2. **Embedding Generation**: Create vector embeddings using remote model (`Alaska_Dataset_embeddings`)
3. **Vector Storage**: Store embeddings in optimized table (`Alaska_Dataset_embedded`)
4. **Search Integration**: Enable vector search via `retrieve_relevant_context()`

### BigQuery Schema

```sql
-- Raw data table structure
CREATE TABLE Alaska_Dataset.Alaska_Dataset_data (
  string_field_0 STRING,  -- Questions
  string_field_1 STRING   -- Answers
);

-- Embedded data table structure  
CREATE TABLE Alaska_Dataset.Alaska_Dataset_embedded (
  content STRING,         -- Combined question + answer text
  question STRING,        -- Original question
  answer STRING,          -- Original answer
  embedding ARRAY<FLOAT64> -- Vector embedding
);
```

## 🛠️ **Development Guide**

### **Core Classes & Methods**

#### Main Orchestrator (`app/core_engine.py`)
```python
from app.core_engine import alaska_agent, AlaskaSnowAgent

# Process user requests
result = alaska_agent.process_user_request("How do I report unplowed roads?")
print(result["response"])

# Check system health
health = alaska_agent.health_check()
print(health["overall_healthy"])
```

#### Safety Validation (`app/safety_validator.py`)
```python
from app.safety_validator import safety_validator

# Validate prompt safety
is_safe = safety_validator.validate_prompt_safety("Your prompt here")

# Get detailed metrics
metrics = safety_validator.get_validation_metrics("Your prompt here")
print(f"Safety: {metrics['is_safe']}, Length: {metrics['prompt_length']}")
```

#### Response Generation (`app/response_generator.py`)
```python
from app.response_generator import response_generator

# Retrieve relevant context
context_df = response_generator.retrieve_relevant_context("snow removal")

# Generate response with context
response = response_generator.generate_assistant_response("How do I request snow removal?")
```

### **Adding Custom Features**

#### Extending Safety Validation
```python
from app.safety_validator import SafetyValidator
from utils.logger import setup_logger

class CustomSafetyValidator(SafetyValidator):
    def __init__(self):
        super().__init__()
        self.logger = setup_logger(__name__)
    
    def validate_department_specific_content(self, prompt: str) -> bool:
        """Add department-specific validation rules."""
        # Custom validation logic
        sensitive_keywords = ["internal", "classified", "confidential"]
        return not any(keyword in prompt.lower() for keyword in sensitive_keywords)
```

#### Custom Response Formatting
```python
from app.response_generator import ResponseGenerator
from typing import Dict, Any

class CustomResponseGenerator(ResponseGenerator):
    def format_response_with_metadata(self, response: str, context_df) -> Dict[str, Any]:
        """Add metadata to responses."""
        return {
            "response": response,
            "sources_count": len(context_df),
            "confidence_score": self._calculate_confidence(context_df),
            "timestamp": datetime.now().isoformat()
        }
```

### **Backward Compatibility**

The improved codebase maintains backward compatibility through wrapper functions:

```python
# Old API still works
from app.core_engine import generate_assistant_response, validate_prompt_safety

response = generate_assistant_response("Your question")  # Still works
is_safe = validate_prompt_safety("Your prompt")  # Still works
```

### Code Style Guidelines

- **Formatting**: Black code formatter with 88-character line limit
- **Linting**: Flake8 with custom configuration
- **Type Hints**: Comprehensive type annotations required
- **Documentation**: Google-style docstrings for all functions

## 🐛 **Troubleshooting**

### Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Authentication Error | `403 Forbidden` errors | Verify service account permissions |
| BigQuery Connection | `Connection timeout` | Check network connectivity and quotas |
| Model Unavailable | `Model not found` errors | Verify model deployment and region |
| High Latency | Slow response times | Check resource allocation and scaling settings |

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
streamlit run ui/streamlit_interface.py --logger.level debug
```

### Health Checks

```python
# Programmatic health check using the AlaskaSnowAgent
from app.core_engine import alaska_agent

health_status = alaska_agent.health_check()
print("Overall Health:", health_status["overall_healthy"])
print("Components:", health_status["components"])

# Check individual components
safety_health = health_status["components"]["safety_validator"]["healthy"]
rag_health = health_status["components"]["response_generator"]["healthy"]
```

### Debug Mode & Logging

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with detailed logging
streamlit run ui/streamlit_interface.py

# Check logs in code
from utils.logger import setup_logger
logger = setup_logger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```
