# Operational Flowchart - Sinhala Chatbot System

## Detailed Flowchart Description

This document describes the operational flow of the Fully Offline Sinhala Chatbot from user input to output display.

---

## Main Application Flow

```
START APPLICATION
    ↓
[1] Initialize Streamlit Environment
    ↓
[2] Load Page Configuration
    - Set page title: "Sinhala Assistant"
    - Set page icon: 🤖
    - Apply custom CSS (light/dark mode)
    ↓
[3] Initialize Session State
    - Check if 'messages' exists in session
    - If NO → Create empty messages list []
    - If YES → Load existing messages
    ↓
[4] Render UI Components
    - Display title: "සාමාන්‍ය සිංහල සහායක"
    - Display subtitle
    - Render Clear Chat History button
    - Display language selector (English/සිංහල)
    ↓
[5] Display Chat History
    - Loop through st.session_state.messages
    - For each message:
        * If role = "user" → Display with user icon
        * If role = "assistant" → Display with assistant icon
    ↓
[6] Wait for User Input
    - Text input box ready
    - Voice recorder ready (optional)
    ↓
[Decision Point] User Action?
    ├─→ Clear Button Clicked → Go to [CLEAR FLOW]
    ├─→ Text Input Submitted → Go to [PROCESS INPUT]
    ├─→ Voice Input Detected → Go to [PROCESS INPUT]
    └─→ No Action → Continue waiting at [6]
```

---

## Input Processing Flow

```
[PROCESS INPUT]
    ↓
[7] Capture Input
    - Source: Text OR Voice
    - If Voice → Convert speech to text (STT)
    - Store in variable: final_input
    ↓
[8] Validate Input
    - Check if input is not empty
    - If empty → Return to [6]
    ↓
[9] Display User Message
    - Render in chat interface with user icon
    - Add message to session state:
        st.session_state.messages.append({
            "role": "user",
            "content": final_input
        })
    ↓
[10] Prepare for Model Inference
    - Show spinner: "Thinking..."
    - Prepare messages array for Ollama API
    ↓
Go to [MODEL INFERENCE]
```

---

## Language Detection & Processing Flow

```
[LANGUAGE PROCESSING]
    ↓
[11] Implicit Language Detection
    - Model receives full message history
    - Model analyzes input language
    ↓
[Decision] Input Language?
    ├─→ English Detected:
    │       - Apply Rule: "මෙය සිංහල චැට්බොට් එකක්..."
    │       - Generate Sinhala response
    │       - Include acknowledgment message
    │       → Go to [RESPONSE GENERATION]
    │
    └─→ Sinhala Detected:
            - Generate Sinhala response directly
            - Follow natural conversational style
            → Go to [RESPONSE GENERATION]
```

---

## Model Inference Flow (Ollama)

```
[MODEL INFERENCE]
    ↓
[12] Send Request to Ollama API
    - Endpoint: http://localhost:11434/api/chat
    - Method: POST
    - Payload: {
        "model": "sinhala-assistant",
        "messages": st.session_state.messages
      }
    ↓
[13] Ollama Processing
    - Load model: sinhala-assistant
    - Load Modelfile configuration
    - Apply system prompt
    - Apply parameters (temperature=0.1)
    ↓
[14] Model Inference
    - Process conversation context
    - Detect input language
    - Apply language rules from system prompt
    - Generate tokens sequentially
    ↓
[15] Response Generation
    - Complete response generation
    - Format as JSON
    ↓
[16] Return Response to Application
    - Response format: {
        "message": {
            "role": "assistant",
            "content": "generated text"
        }
      }
    ↓
Go to [POST-PROCESSING]
```

---

## Response Post-Processing Flow

```
[POST-PROCESSING]
    ↓
[17] Extract Response Content
    - Parse JSON response
    - Extract: response['message']['content']
    - Store in: raw_response
    ↓
[18] Clean Response
    - Check for <think> tags (internal reasoning)
    - If found → Remove everything before </think>
    - Keep only final answer
    - Store in: full_response
    ↓
[19] Display Assistant Response
    - Render in chat interface with assistant icon
    - Add to session state:
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })
    ↓
[Decision] Was Voice Input Used?
    ├─→ YES:
    │       - Convert response to speech (TTS)
    │       - Play audio output
    │       → Go to [20]
    │
    └─→ NO:
            - Skip TTS
            → Go to [20]
    ↓
[20] Complete Processing
    - Hide spinner
    - UI returns to ready state
    ↓
Return to [6] Wait for User Input
```

---

## Clear History Flow

```
[CLEAR FLOW]
    ↓
[21] Clear Button Clicked
    ↓
[22] Reset Session State
    - st.session_state.messages = []
    ↓
[23] Trigger Rerun
    - st.rerun()
    - Application reloads with empty chat
    ↓
Return to [4] Render UI Components
```

---

## Error Handling Flow

```
[ERROR HANDLING]
    ↓
[Decision] Error Type?
    │
    ├─→ Ollama Connection Error:
    │       - Check if Ollama service running
    │       - Display error: "Cannot connect to Ollama"
    │       - Suggest: "Please start Ollama service"
    │       → Return to [6]
    │
    ├─→ Model Not Found:
    │       - Display error: "Model 'sinhala-assistant' not found"
    │       - Suggest: "Please create model using Modelfile"
    │       → Return to [6]
    │
    ├─→ Memory Error (Long Conversation):
    │       - Display warning: "Chat history too long"
    │       - Suggest: "Please clear history"
    │       → Return to [6]
    │
    └─→ Other Errors:
            - Display generic error message
            - Log error details
            → Return to [6]
```

---

## Detailed State Diagram

```
┌──────────────────────────────────────────────────┐
│              APPLICATION STATES                  │
├──────────────────────────────────────────────────┤
│                                                  │
│  [IDLE] ←──────────────────────────┐            │
│    ↓                                │            │
│  User inputs message                │            │
│    ↓                                │            │
│  [PROCESSING]                       │            │
│    ├─→ Display user message         │            │
│    ├─→ Show spinner                 │            │
│    └─→ Call Ollama API              │            │
│           ↓                         │            │
│  [WAITING_FOR_RESPONSE]             │            │
│           ↓                         │            │
│  Response received                  │            │
│           ↓                         │            │
│  [DISPLAYING]                       │            │
│    ├─→ Clean response               │            │
│    ├─→ Display assistant message    │            │
│    └─→ Optional TTS                 │            │
│           ↓                         │            │
│  Complete ─────────────────────────┘            │
│                                                  │
│  [CLEARING] (Clear button pressed)               │
│    ├─→ Reset messages                           │
│    └─→ Rerun app → Back to [IDLE]              │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## Key Decision Points

### 1. Input Source Decision
```
User Input?
├── Text → Use chat_input value
└── Voice → Convert speech to text first
```

### 2. Language Decision (in Model)
```
Input Language?
├── English → Sinhala response with acknowledgment
└── Sinhala → Direct Sinhala response
```

### 3. Voice Output Decision
```
Input Method?
├── Voice → Enable TTS output
└── Text → Skip TTS output
```

### 4. Session State Decision
```
messages in session_state?
├── YES → Load existing history
└── NO → Initialize empty list
```

---

## Performance Metrics

| Stage | Typical Duration | Notes |
|-------|------------------|-------|
| Input Capture | < 100ms | Instant |
| Display User Message | < 100ms | Instant |
| Ollama API Call | 2-10 seconds | Depends on model size & hardware |
| Response Processing | < 100ms | Instant |
| Display Response | < 100ms | Instant |
| TTS (if enabled) | 1-5 seconds | Depends on text length |
| **Total Response Time** | **2-15 seconds** | **User perceivable delay** |

---

## Data Structure Flow

```
INPUT: User types/speaks message
    ↓
STRUCTURE: String text
    ↓
TRANSFORMED TO: Message object
    {
        "role": "user",
        "content": "user's message"
    }
    ↓
ADDED TO: Session state messages array
    [
        {"role": "user", "content": "msg1"},
        {"role": "assistant", "content": "resp1"},
        {"role": "user", "content": "msg2"}
    ]
    ↓
SENT TO: Ollama API
    {
        "model": "sinhala-assistant",
        "messages": [full history]
    }
    ↓
RECEIVED FROM: Ollama API
    {
        "message": {
            "role": "assistant",
            "content": "generated response"
        }
    }
    ↓
EXTRACTED: Response content string
    ↓
CLEANED: Remove <think> tags if present
    ↓
ADDED TO: Session state messages array
    ↓
DISPLAYED: In chat interface
```

---

## Summary

This flowchart describes the complete operational flow of the Sinhala Chatbot:

1. **Initialization**: Set up environment, load configuration
2. **Input Handling**: Capture text or voice input
3. **Language Processing**: Detect language and apply rules
4. **Model Inference**: Send to Ollama, generate response locally
5. **Post-Processing**: Clean and format response
6. **Output Display**: Show response in UI, optional TTS
7. **State Management**: Maintain conversation history
8. **Error Handling**: Gracefully handle failures

The system operates in a continuous loop, waiting for user input, processing through Ollama, and displaying responses while maintaining full offline capability.
