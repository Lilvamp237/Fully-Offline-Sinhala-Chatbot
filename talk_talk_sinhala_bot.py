import streamlit as st
import ollama
import pyttsx3
from streamlit_mic_recorder import speech_to_text

# --- Setup TTS Engine ---
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160) # Slightly faster for natural flow
        
        # DEBUG: This will print available voices to your terminal
        # Ensure a Sinhala voice is installed in Windows/Mac settings
        voices = engine.getProperty('voices')
        
        # Attempt to find a Sinhala voice if available
        for voice in voices:
            if "sinhala" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        #engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Voice Error: {e}")

# --- Streamlit UI ---
st.set_page_config(page_title="Talk Talk Bot Sinhala Assistant", page_icon="💎")

st.title("💎 Talk Talk Bot සිංහල සහායක")
st.markdown("ඔබේ සිංහල සහායකයා වෙමි")

# --- Sidebar Features ---
with st.sidebar:
    st.header("Settings")
    enable_voice = st.checkbox("🔊 Enable Voice Response", value=True)
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Input Section ---
# Language 'si' uses the browser's local STT engine
text_input = speech_to_text(language='si', start_prompt="🎤 කතා කරන්න (Voice)", key='STT')
user_prompt = st.chat_input("මෙතන ටයිප් කරන්න... (Text)")

final_input = text_input if text_input else user_prompt

if final_input:
    # 1. User Message
    with st.chat_message("user"):
        st.markdown(final_input)
    st.session_state.messages.append({"role": "user", "content": final_input})

    # 2. Assistant Message (Streaming)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Stream from Gemma 3 (Ensure model name matches your 'ollama create' name)
        response_stream = ollama.chat(
            model='talk_talk_bot', 
            messages=st.session_state.messages,
            stream=True
        )
        
        for chunk in response_stream:
            content = chunk['message']['content']
            full_response += content
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    # 3. Save and Speak
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    if enable_voice:
        speak(full_response)