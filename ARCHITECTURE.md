# System Architecture - Fully Offline Sinhala Chatbot

## Overview
This document describes the technical architecture of the General Purpose Sinhala Chatbot, designed to run completely offline using Ollama and Streamlit.

## System Architecture Description

### 1. Architecture Layers

#### **Presentation Layer (Frontend)**
- **Technology**: Streamlit Web Framework
- **Components**:
  - User Interface (Chat interface with message bubbles)
  - Input Components (Text input box, Optional voice recorder)
  - Display Components (Chat history, status indicators)
  - Control Elements (Clear history button, language selector)
  
- **Styling**: Custom CSS for professional appearance
  - Light mode: Blue (#2196F3) and Purple (#9C27B0) theme
  - Dark mode: Adaptive color scheme for better visibility
  - Responsive chat bubbles with border accents

#### **Application Layer (Business Logic)**
- **Technology**: Python 3.x with Streamlit
- **Core Functions**:
  - **Session Management**: Maintains chat history using `st.session_state`
  - **Message Processing**: Handles user input (text/voice), formats messages
  - **Response Handling**: Receives and displays model responses
  - **Text-to-Speech Integration**: Optional pyttsx3 for voice output
  - **Speech-to-Text Integration**: Optional streamlit_mic_recorder for voice input

- **Key Components**:
  ```
  hospital_app.py
  ├── UI Configuration (Streamlit page setup)
  ├── Session State Management
  ├── Input Processing (Text & Voice)
  ├── Ollama API Integration
  ├── Response Display Logic
  └── TTS/STT Handlers
  ```

#### **Model Layer (AI Inference)**
- **Technology**: Ollama (Local LLM Runtime)
- **Model Configuration**: Custom Modelfile
  - Base Model: Pre-trained language model (locally stored)
  - System Prompt: Defines assistant behavior and rules
  - Parameters: Temperature (0.1), stop tokens
  - Template: Chat format with role-based prompting

- **Language Processing**:
  - Detects input language (English vs Sinhala)
  - Applies language-specific response rules
  - Generates contextually appropriate responses

#### **Data Layer (Storage)**
- **Session Storage**: In-memory storage via Streamlit session state
- **Model Storage**: Local filesystem
  - Model weights: `C:\Users\User\.ollama\models\blobs\`
  - Modelfile: Custom configuration file
  
- **Chat History Structure**:
  ```python
  messages = [
    {"role": "user", "content": "user message"},
    {"role": "assistant", "content": "assistant response"}
  ]
  ```

### 2. Data Flow

```
User Input (Text/Voice)
    ↓
[Input Processing & Validation]
    ↓
[Session State Update - Add User Message]
    ↓
[Format Messages for Ollama API]
    ↓
[Local Ollama Inference Engine]
    ↓
[Response Generation (Sinhala/Mixed)]
    ↓
[Response Post-Processing (Remove <think> tags)]
    ↓
[Display Response in UI]
    ↓
[Session State Update - Add Assistant Message]
    ↓
[Optional: Text-to-Speech Output]
```

### 3. Component Interactions

#### **Streamlit ↔ Ollama**
- Communication: REST API over localhost (default: http://localhost:11434)
- Request Format: JSON with messages array
- Response Format: JSON with message content
- Connection: Synchronous (blocking until response received)

#### **User ↔ Streamlit**
- Interface: Web browser (localhost:8501)
- Real-time updates using Streamlit's reactive framework
- Session persistence during active browser session

#### **Ollama ↔ Model Files**
- Model Loading: On-demand loading from local storage
- Configuration: Modelfile specifies system prompt and parameters
- Inference: Fully local, no external API calls

### 4. Key Features

#### **Fully Offline Operation**
- ✅ No internet required after initial setup
- ✅ All models stored locally
- ✅ Local inference (CPU/GPU based on hardware)
- ✅ Session data in memory (no external database)

#### **Language Handling**
- Bilingual support (English input → Sinhala response)
- Native Sinhala conversation
- Cultural appropriateness built into system prompt

#### **Session Management**
- Maintains conversation context
- Supports long conversations (limited by RAM)
- Clear history functionality to reset
- Stateless between app restarts

### 5. Deployment Architecture

```
┌─────────────────────────────────────────────┐
│         User's Local Machine                │
│                                             │
│  ┌────────────────────────────────────┐    │
│  │  Web Browser (localhost:8501)      │    │
│  └────────────┬───────────────────────┘    │
│               │                             │
│  ┌────────────▼───────────────────────┐    │
│  │  Streamlit App (Python Process)    │    │
│  │  - UI Rendering                    │    │
│  │  - Session Management              │    │
│  │  - API Client                      │    │
│  └────────────┬───────────────────────┘    │
│               │                             │
│  ┌────────────▼───────────────────────┐    │
│  │  Ollama Service (Background)       │    │
│  │  - Model Loading                   │    │
│  │  - Inference Engine                │    │
│  │  - API Server (localhost:11434)    │    │
│  └────────────┬───────────────────────┘    │
│               │                             │
│  ┌────────────▼───────────────────────┐    │
│  │  Local Model Storage               │    │
│  │  - Model Weights (.bin files)      │    │
│  │  - Modelfile Configuration         │    │
│  └────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

### 6. Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Streamlit | Web UI framework |
| Backend | Python 3.x | Application logic |
| Model Runtime | Ollama | Local LLM inference |
| Language Model | Qwen/Llama-based | Sinhala language support |
| TTS (Optional) | pyttsx3 | Text-to-speech |
| STT (Optional) | streamlit_mic_recorder | Speech-to-text |
| Styling | CSS | UI customization |

### 7. Performance Considerations

- **Memory**: Chat history grows linearly; implement limits for very long conversations
- **CPU/GPU**: Inference speed depends on hardware; 4GB+ RAM recommended
- **Latency**: Typical response time: 2-10 seconds (depends on model size and hardware)
- **Concurrency**: Single-user application (no multi-user support required)

### 8. Security & Privacy

- **Data Privacy**: All data stays on local machine
- **No Telemetry**: No data sent to external servers
- **Network Isolation**: Operates without internet connection
- **Session Security**: Data cleared on app restart

### 9. Scalability Considerations

- Current design: Single-user, single-session
- Chat history: Limited by available RAM
- Recommended: Clear history periodically for long conversations
- Future enhancement: Add conversation history limit (e.g., last 50 messages)

## Diagram Notes

For your documentation, create diagrams showing:
1. **Component Diagram**: Four layers (UI, Application, Model, Data)
2. **Sequence Diagram**: Message flow from user input to response
3. **Deployment Diagram**: Single machine with all components
4. **Data Flow Diagram**: Input → Processing → Inference → Output

## Technical Requirements

- Python 3.8+
- Ollama installed and running
- 4GB+ RAM (8GB recommended)
- Storage: 5-10GB for model files
- OS: Windows/Linux/macOS
