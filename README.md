# General Purpose Sinhala Chatbot

## Overview
A fully offline, general-purpose Sinhala chatbot built with Ollama and Streamlit for natural language interaction in Sinhala and English.

## Features
- ✅ **Fully Offline**: All processing happens locally, no internet required
- 🗣️ **Bilingual Support**: Handles both Sinhala and English inputs
- 🎯 **General Purpose**: Answers questions on various topics (knowledge, creative writing, logic)
- 💬 **Conversational**: Maintains context throughout the conversation
- 🎨 **Modern UI**: Professional interface with light/dark mode support
- 🧹 **Clear History**: Button to reset conversation
- 🇱🇰 **Culturally Appropriate**: Responses tailored for Sri Lankan context

## Language Rules
- **English Input** → Responds in Sinhala with acknowledgment: "මෙය සිංහල චැට්බොට් එකක්, නමුත් මම ඔබට උදව් කරන්නම්. මම සිංහලෙන් පිළිතුරු දෙන්නම්."
- **Sinhala Input** → Responds naturally in Sinhala

## Technology Stack
- **Frontend**: Streamlit (Web UI)
- **Backend**: Python 3.8+
- **AI Engine**: Ollama (Local LLM)
- **Model**: Custom Sinhala-enabled language model
- **Deployment**: Localhost (fully offline)

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Ollama installed and running

### Installation
```bash
# 1. Install dependencies
pip install streamlit ollama

# 2. Create the Ollama model
ollama create sinhala-assistant -f Modelfile

# 3. Run the application
streamlit run hospital_app.py
```

### Access
Open your browser and navigate to: `http://localhost:8501`

## Project Structure
```
├── hospital_app.py          # Main Streamlit application
├── Modelfile                # Ollama model configuration
├── TEST_PROMPTS.md          # 20 test cases for evaluation
├── ARCHITECTURE.md          # System architecture documentation
├── FLOWCHART.md             # Operational flow description
├── OFFLINE_ANALYSIS.md      # Offline capability analysis
├── SETUP.md                 # Detailed setup guide
└── README.md                # This file
```

## Usage Examples

### Example 1: General Knowledge (Sinhala)
**User**: ශ්‍රී ලංකාවේ අගනගරය කුමක්ද?  
**Assistant**: ශ්‍රී ලංකාවේ අගනගරය කොළඹයි.

### Example 2: General Knowledge (English)
**User**: What is the capital of Sri Lanka?  
**Assistant**: මෙය සිංහල චැට්බොට් එකක්, නමුත් මම ඔබට උදව් කරන්නම්. මම සිංහලෙන් පිළිතුරු දෙන්නම්. ශ්‍රී ලංකාවේ අගනගරය කොළඹයි.

### Example 3: Creative Writing
**User**: කවියක් ලියන්න  
**Assistant**: ඇත්තෙන්ම! මෙන්න සරල කවියක්:  
සඳ එළියේ රිදී තරු,  
අහස මුළුල්ලේ රන් පෙති,  
රැයේ සුන්දරත්වය බලන්න,  
සිත සතුටෙන් පිරී යති.

### Example 4: Basic Logic
**User**: 15 + 27 කීයද?  
**Assistant**: 15 + 27 = 42

## Key Features Explained

### 1. Offline Operation
- All AI inference happens on your local machine
- No data sent to external servers
- Works without internet connection
- Model weights stored locally

### 2. Session Management
- Maintains conversation context
- Chat history visible throughout session
- Clear history button to start fresh
- Handles long conversations

### 3. Professional UI
- Clean, modern chat interface
- Color-coded message bubbles (user: blue, assistant: purple)
- Dark mode support
- Responsive design

### 4. Error Handling
- Graceful handling of long conversations
- Clear error messages
- Robust state management

## Testing

See `TEST_PROMPTS.md` for 20 comprehensive test cases covering:
- General knowledge (geography, history, science, math)
- Creative writing (poetry, stories, descriptions)
- Basic logic and reasoning
- Cultural knowledge
- Practical applications

## System Requirements

### Minimum
- CPU: Modern multi-core processor
- RAM: 4GB
- Storage: 10GB free space
- OS: Windows 10/11, Linux, macOS

### Recommended
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 20GB free space
- GPU: Optional (speeds up inference)

## Performance

- **Average Response Time**: 2-10 seconds (depends on hardware)
- **Memory Usage**: 2-4GB (model) + 1GB (app)
- **Concurrent Users**: Single user (localhost deployment)

## Documentation

Comprehensive documentation available:
- **ARCHITECTURE.md**: Technical system architecture
- **FLOWCHART.md**: Detailed operational flow
- **OFFLINE_ANALYSIS.md**: Offline capability analysis
- **SETUP.md**: Step-by-step setup guide
- **TEST_PROMPTS.md**: Testing methodology and cases

## Troubleshooting

### Model not found
```bash
ollama create sinhala-assistant -f Modelfile
```

### Cannot connect to Ollama
```bash
ollama serve
```

### Slow responses
- Close unnecessary applications
- Ensure sufficient RAM available
- Clear chat history if very long

### Port already in use
```bash
streamlit run hospital_app.py --server.port 8502
```

## Limitations

- Single-user application (not designed for multiple concurrent users)
- Chat history limited by available RAM
- Response quality depends on base model capabilities
- TTS/STT features have limited Sinhala support (optional, not enabled by default)

## Future Enhancements

- [ ] Conversation history export
- [ ] Multi-language support (Tamil, English)
- [ ] Response caching for common queries
- [ ] Improved error handling
- [ ] User preferences persistence
- [ ] Better Sinhala TTS integration

## Academic Context

This project was developed as a university assignment for Natural Language Processing (NLP) course at General Sir John Kotelawala Defence University. It demonstrates:
- Local LLM deployment
- Bilingual NLP applications
- Streamlit web framework usage
- Offline AI system design
- Cultural adaptation in AI systems

## License

This project is created for educational purposes as part of a university assignment.

## Author

Developed for NLP Coursework, Semester 7  
General Sir John Kotelawala Defence University

## Acknowledgments

- **Ollama**: For providing the local LLM runtime
- **Streamlit**: For the excellent web framework
- **Open Source Community**: For the base language models

---

## Quick Reference

### Start Application
```bash
streamlit run hospital_app.py
```

### Create/Update Model
```bash
ollama create sinhala-assistant -f Modelfile
```

### Test Model Directly
```bash
ollama run sinhala-assistant
```

### Check Running Models
```bash
ollama list
```

---

**Note**: For detailed setup instructions, see `SETUP.md`. For system architecture details, see `ARCHITECTURE.md`. For testing procedures, see `TEST_PROMPTS.md`.
