import streamlit as st
import ollama
import pyttsx3
from streamlit_mic_recorder import speech_to_text

# CORRECTED IMPORTS FOR 2026
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# Sri Lankan Flag Color Palette
SL_COLORS = {
    "maroon": "#8B1538",      # Deep maroon/red
    "gold": "#FFBE3D",        # Gold/yellow
    "green": "#006747",       # Green
    "orange": "#FF671F",      # Orange/saffron
    "dark_maroon": "#5C0E26", # Darker maroon for dark mode
    "light_gold": "#FFD97D",  # Lighter gold for backgrounds
}

# --- 1. RAG Setup (Offline Vector DB) ---
@st.cache_resource
def init_vector_db():
    # Loading local ground-truth facts from /data/facts.json
    loader = JSONLoader(file_path='./data/facts.json', jq_schema='.[] | .fact', text_content=False)
    docs = loader.load()
    
    # Split text into chunks for Gemma 3's 128K context window
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)
    
    # Using local embeddings (Run 'ollama pull nomic-embed-text' first)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory="./chroma_db")

# Initialize the library
vectorstore = init_vector_db()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# --- 2. Streamlit UI ---
st.set_page_config(
    page_title="Talk Talk Sinhala Bot", 
    page_icon="SB",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Track if voice input has been processed to prevent re-processing
if "last_voice_input" not in st.session_state:
    st.session_state.last_voice_input = None

if "processed_input" not in st.session_state:
    st.session_state.processed_input = False

# Dark mode toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Sidebar styling and controls
with st.sidebar:
    st.markdown("Talk Talk Sinhala Bot")
    st.markdown("---")
    
    # Dark mode toggle
    dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()
    
    st.markdown("---")
    
    # Reset button
    if st.button("🗑️ සංවාදය මකන්න (Clear)", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("##### About")
    st.markdown("Fully offline Sinhala chatbot powered by Ollama & RAG")

# Apply custom CSS based on theme
if st.session_state.dark_mode:
    # Dark mode - Sri Lankan flag colors adapted for dark theme
    st.markdown(f"""
    <style>
        /* Main app background */
        .stApp {{
            background: linear-gradient(135deg, {SL_COLORS['dark_maroon']} 0%, #1a1a2e 100%);
        }}
        
        /* Header styling */
        .main-header {{
            background: linear-gradient(90deg, {SL_COLORS['maroon']} 0%, {SL_COLORS['orange']} 50%, {SL_COLORS['gold']} 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}
        
        .main-header h1 {{
            color: white;
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }}
        
        /* Chat messages */
        .stChatMessage {{
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-left: 4px solid {SL_COLORS['gold']};
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
        }}
        
        /* User message specific */
        [data-testid="stChatMessageContent"]:has(+ [data-testid="stChatMessageAvatar"]) {{
            background: linear-gradient(135deg, rgba(139, 21, 56, 0.3), rgba(0, 103, 71, 0.3));
            border-left: 4px solid {SL_COLORS['green']};
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {SL_COLORS['maroon']} 0%, {SL_COLORS['dark_maroon']} 100%);
        }}
        
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        /* Input box styling */
        .stChatInputContainer {{
            border-top: 3px solid {SL_COLORS['gold']};
            background: rgba(26, 26, 46, 0.95);
            padding: 10px;
            position: sticky;
            bottom: 0;
            z-index: 999;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: linear-gradient(90deg, {SL_COLORS['maroon']}, {SL_COLORS['orange']});
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(90deg, {SL_COLORS['orange']}, {SL_COLORS['gold']});
            transform: scale(1.05);
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.3);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {SL_COLORS['gold']};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {SL_COLORS['orange']};
        }}
    </style>
    """, unsafe_allow_html=True)
else:
    # Light mode - Sri Lankan flag colors
    st.markdown(f"""
    <style>
        /* Main app background */
        .stApp {{
            background: linear-gradient(135deg, {SL_COLORS['light_gold']} 0%, #ffffff 100%);
        }}
        
        /* Header styling */
        .main-header {{
            background: linear-gradient(90deg, {SL_COLORS['maroon']} 0%, {SL_COLORS['orange']} 50%, {SL_COLORS['gold']} 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .main-header h1 {{
            color: white;
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        
        /* Chat messages */
        .stChatMessage {{
            background-color: rgba(255, 255, 255, 0.8) !important;
            border-left: 4px solid {SL_COLORS['gold']};
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        /* User message specific */
        [data-testid="stChatMessageContent"]:has(+ [data-testid="stChatMessageAvatar"]) {{
            background: linear-gradient(135deg, rgba(139, 21, 56, 0.1), rgba(0, 103, 71, 0.1));
            border-left: 4px solid {SL_COLORS['green']};
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {SL_COLORS['maroon']} 0%, {SL_COLORS['dark_maroon']} 100%);
        }}
        
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        /* Input box styling */
        .stChatInputContainer {{
            border-top: 3px solid {SL_COLORS['maroon']};
            background: rgba(255, 255, 255, 0.95);
            padding: 10px;
            position: sticky;
            bottom: 0;
            z-index: 999;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        /* Buttons */
        .stButton > button {{
            background: linear-gradient(90deg, {SL_COLORS['maroon']}, {SL_COLORS['orange']});
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(90deg, {SL_COLORS['orange']}, {SL_COLORS['gold']});
            transform: scale(1.05);
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.05);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {SL_COLORS['maroon']};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {SL_COLORS['orange']};
        }}
    </style>
    """, unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>Talk Talk Sinhala Bot (සිංහල)</h1>
</div>
""", unsafe_allow_html=True)

# Chat container - displays all messages above the input
chat_container = st.container()

with chat_container:
    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- 3. Processing Input (Fixed Input Logic) ---
# Input container - always stays at the bottom
st.markdown("<br>", unsafe_allow_html=True)  # Add spacing

# Create columns for voice and text input to keep them together
input_container = st.container()
with input_container:
    col1, col2 = st.columns([1, 5])
    
    with col1:
        text_voice = speech_to_text(language='si', start_prompt="🎤 කතා කරන්න", key='STT')
    
    with col2:
        # Empty column for spacing - actual chat_input appears below
        pass

# Chat input appears below the columns
text_input = st.chat_input("මෙතන ලියන්න...")

# Determine final query
final_query = None

# Manual text input ALWAYS takes priority over voice
if text_input:
    final_query = text_input
    # Update last_voice_input to current voice value to prevent it from being processed again
    if text_voice:
        st.session_state.last_voice_input = text_voice
# Only use voice input if: there's no text input AND voice is new/different
elif text_voice and text_voice != st.session_state.last_voice_input:
    final_query = text_voice
    st.session_state.last_voice_input = text_voice  # Mark this voice input as processed

if final_query:
    # A. Add user message to history and display immediately
    st.session_state.messages.append({"role": "user", "content": final_query})
    
    # Show the user message immediately in the chat container
    with chat_container:
        with st.chat_message("user"):
            st.markdown(final_query)

    # B. RAG Step: Search your facts.json for the answer
    docs = vectorstore.similarity_search(final_query, k=2)
    context = " ".join([d.page_content for d in docs])

    # --- C. Generate Assistant Response with streaming ---
    # We clearly separate the Context from the Question
    prompt = f"""
    සන්දර්භය (Context): {context}
    
    ප්‍රශ්නය (User Question): {final_query}
    
    උපදෙස්: ඉහත සන්දර්භය ප්‍රශ්නයට අදාළ නම් පමණක් එය භාවිතා කරන්න. ප්‍රශ්නයට අදාළ නොවන කරුණු ඇතුළත් නොකරන්න. සිංහලෙන් පමණක් පිළිතුරු දෙන්න.
    """
    
    # Display streaming response
    with chat_container:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_res = ""
            
            stream = ollama.chat(
                model='talk_talk_bot', 
                messages=[{"role": "user", "content": prompt}], 
                stream=True
            )
            
            for chunk in stream:
                full_res += chunk['message']['content']
                response_placeholder.markdown(full_res + "▌")
            
            response_placeholder.markdown(full_res)

    # D. Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_res})
    
    # E. Speak the response
    speak(full_res)
    
    # F. Rerun to clear input and update display
    st.rerun()