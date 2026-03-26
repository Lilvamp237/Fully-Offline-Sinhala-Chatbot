# Setup and Deployment Guide

## Prerequisites

### Required Software
1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Ensure "Add Python to PATH" is checked during installation

2. **Ollama**
   - Download from: https://ollama.ai/download
   - Install and ensure service is running

### Required Python Packages
```bash
pip install streamlit
pip install ollama
```

### Optional Packages (for voice features - not recommended for offline demo)
```bash
pip install pyttsx3
pip install streamlit-mic-recorder
```

---

## Installation Steps

### Step 1: Create Model in Ollama

1. **Navigate to project directory**:
   ```bash
   cd "C:\Users\User\OneDrive - General Sir John Kotelawala Defence University\Sem 7\NLP\Hospital Assistant"
   ```

2. **Create the model** using the Modelfile:
   ```bash
   ollama create sinhala-assistant -f Modelfile
   ```

3. **Verify model creation**:
   ```bash
   ollama list
   ```
   You should see `sinhala-assistant` in the list.

### Step 2: Test the Model (Optional)

```bash
ollama run sinhala-assistant
```

Try some test prompts:
- ඔයා කවුද? (Who are you?)
- What is Sri Lanka? (Should respond in Sinhala)
- කවියක් ලියන්න (Write a poem)

Type `/bye` to exit.

### Step 3: Run the Streamlit App

```bash
streamlit run hospital_app.py
```

The app should open in your browser at: `http://localhost:8501`

---

## Renaming Files (Recommended)

Since you're no longer a hospital assistant, rename the files:

```bash
# In the project directory
rename hospital_app.py general_assistant_app.py
```

Update the command to:
```bash
streamlit run general_assistant_app.py
```

---

## Project Structure

```
Hospital Assistant/  (or rename to "Sinhala Assistant")
│
├── Modelfile                      # Ollama model configuration
├── general_assistant_app.py       # Main Streamlit application (renamed)
├── TEST_PROMPTS.md                # 20 test cases with expected responses
├── ARCHITECTURE.md                # System architecture description
├── FLOWCHART.md                   # Operational flowchart description
├── OFFLINE_ANALYSIS.md            # Offline capability analysis
├── SETUP.md                       # This file
└── README.md                      # Project overview (create this)
```

---

## Creating Text-Only Version (Recommended for Demo)

Create a simplified version without voice features:

```bash
# In PowerShell
cd "C:\Users\User\OneDrive - General Sir John Kotelawala Defence University\Sem 7\NLP\Hospital Assistant"
```

The current version already has voice features. To disable them:

**Option 1: Comment out voice imports** (edit hospital_app.py/general_assistant_app.py):
```python
# import pyttsx3
# from streamlit_mic_recorder import speech_to_text
```

**Option 2: Use the simplified version I provided in OFFLINE_ANALYSIS.md**

---

## Running in Offline Mode

### Step 1: Ensure Everything is Downloaded
Make sure you've run the model at least once while online so all components are downloaded.

### Step 2: Disconnect Network
- Turn off WiFi
- Or unplug Ethernet cable

### Step 3: Verify Ollama Service
```bash
# Check if Ollama is running
ollama list
```

If not running, start it:
```bash
ollama serve
```

### Step 4: Run Application
```bash
streamlit run general_assistant_app.py
```

### Step 5: Access in Browser
Open: `http://localhost:8501`

---

## Troubleshooting

### Issue 1: "Model not found"
**Solution**: Create the model using Modelfile:
```bash
ollama create sinhala-assistant -f Modelfile
```

### Issue 2: "Cannot connect to Ollama"
**Solution**: Start Ollama service:
```bash
ollama serve
```
Or check if Ollama is installed and in PATH.

### Issue 3: "Module not found" errors
**Solution**: Install missing packages:
```bash
pip install streamlit ollama
```

### Issue 4: Port already in use (8501)
**Solution**: Use a different port:
```bash
streamlit run general_assistant_app.py --server.port 8502
```

### Issue 5: Voice features not working
**Solution**: Comment out voice-related code or use text-only version (recommended).

### Issue 6: Slow responses
**Possible causes**:
- Large model size
- Insufficient RAM
- CPU-only inference

**Solutions**:
- Close other applications
- Use a smaller model
- Ensure at least 8GB RAM available

### Issue 7: Chat history grows too large
**Solution**: Click the "Clear" button to reset history periodically.

---

## Performance Optimization

### 1. Reduce Model Temperature
In Modelfile:
```
PARAMETER temperature 0.1  # Lower = more consistent, faster
```

### 2. Limit Chat History
Add to app code:
```python
# Keep only last 20 messages
if len(st.session_state.messages) > 20:
    st.session_state.messages = st.session_state.messages[-20:]
```

### 3. Close Background Applications
- Close browsers (except for the demo)
- Close video players
- Close other Python processes

---

## Pre-Demo Checklist

Before recording your video demonstration:

- [ ] All dependencies installed
- [ ] Model created successfully (`ollama list` shows sinhala-assistant)
- [ ] App runs without errors
- [ ] Test all 20 prompts from TEST_PROMPTS.md
- [ ] Voice features disabled (or thoroughly tested if keeping)
- [ ] Clear history button works
- [ ] Conversation context maintains correctly
- [ ] Both English and Sinhala inputs tested
- [ ] Network disconnected to prove offline capability
- [ ] Screen recording software ready
- [ ] Backup of working code saved

---

## Updating the Model

If you need to change the system prompt:

1. **Edit Modelfile** with new prompt

2. **Delete old model**:
   ```bash
   ollama rm sinhala-assistant
   ```

3. **Recreate model**:
   ```bash
   ollama create sinhala-assistant -f Modelfile
   ```

4. **Restart Streamlit app**

---

## Deployment for Submission

### What to Submit:

1. **Source Code Files**:
   - `general_assistant_app.py` (or `hospital_app.py`)
   - `Modelfile`

2. **Documentation**:
   - `README.md` (project overview)
   - `TEST_PROMPTS.md` (test cases)
   - `ARCHITECTURE.md` (system architecture)
   - `FLOWCHART.md` (operational flow)
   - `SETUP.md` (this file)

3. **Video Demonstration** (3-5 minutes):
   - Show offline operation
   - Demonstrate Sinhala conversations
   - Show English → Sinhala response
   - Test diverse topics
   - Show features (clear history, etc.)

4. **Report** (if required):
   - Use content from ARCHITECTURE.md
   - Include diagrams based on FLOWCHART.md
   - Reference TEST_PROMPTS.md for testing methodology

---

## Quick Start Commands (Summary)

```bash
# 1. Install dependencies
pip install streamlit ollama

# 2. Create model
cd "path\to\project"
ollama create sinhala-assistant -f Modelfile

# 3. Run application
streamlit run general_assistant_app.py

# 4. Access in browser
# http://localhost:8501
```

---

## Support

If you encounter issues:

1. Check Ollama logs: `ollama serve` output
2. Check Streamlit logs: Terminal output when running app
3. Verify Python version: `python --version` (should be 3.8+)
4. Verify packages: `pip list | grep -E "streamlit|ollama"`

---

## Notes

- **Model Size**: The base model is several GB. Ensure sufficient disk space.
- **First Response**: May be slower as model loads into memory.
- **RAM Usage**: Expect 2-4GB for the model + 1GB for Streamlit.
- **Offline Requirement**: Download everything before going offline!

Good luck with your assignment! 🚀
