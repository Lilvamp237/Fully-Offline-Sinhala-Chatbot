import streamlit as st
import ollama
import pyttsx3
from streamlit_mic_recorder import speech_to_text
import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# Forest Green Theme Color Palette
THEME_COLORS = {
    "dark_green": "#1B5E20",      # Dark forest green
    "emerald": "#00C853",         # Bright emerald
    "gold": "#FFD700",            # Gold accent
    "light_green": "#4CAF50",     # Medium green
    "forest": "#2E7D32",          # Forest green
    "mint": "#A5D6A7",            # Light mint for backgrounds
    "deep_forest": "#0D3B0D",     # Very dark green for dark mode
}

# --- 1. RAG Setup (Offline Vector DB) ---
@st.cache_resource
def init_vector_db():
    # 1. Load local ground-truth facts using standard json library
    with open('./data/facts.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # 2. Create full documents without splitting (No text_splitter needed!)
    documents = []
    for item in data:
        doc = Document(
            page_content=item["fact"], 
            metadata={"category": item["category"]}
        )
        documents.append(doc)
        
    # 3. Initialize your local HuggingFace multilingual embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    
    # 4. Create and return Vector DB using the full 'documents' array directly
    return Chroma.from_documents(
        documents=documents, 
        embedding=embeddings, 
        persist_directory="./chroma_db", 
        collection_name="sinhala_bot_384"
    )

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
    # Dark mode - Forest Green Theme
    st.markdown(f"""
    <style>
        /* Main app background */
        .stApp {{
            background: linear-gradient(135deg, {THEME_COLORS['deep_forest']} 0%, #0a1f0a 100%);
            color: white !important;
        }}
        
        /* Make all text white in dark mode */
        .stApp, .stApp p, .stApp span, .stApp div, .stMarkdown {{
            color: white !important;
        }}
        
        /* Chat message text color */
        .stChatMessage, .stChatMessage p, .stChatMessage span, .stChatMessage div {{
            color: white !important;
        }}
        
        /* Top bar (header) styling */
        header[data-testid="stHeader"] {{
            background: linear-gradient(90deg, {THEME_COLORS['dark_green']} 0%, {THEME_COLORS['forest']} 100%) !important;
            border-bottom: 3px solid {THEME_COLORS['emerald']};
        }}
        
        /* Deploy button and toolbar */
        [data-testid="stToolbar"] {{
            background: transparent !important;
        }}
        
        /* Header styling */
        .main-header {{
            background: linear-gradient(90deg, {THEME_COLORS['dark_green']} 0%, {THEME_COLORS['emerald']} 50%, {THEME_COLORS['gold']} 100%);
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
            background-color: rgba(27, 94, 32, 0.3) !important;
            border-left: 4px solid {THEME_COLORS['emerald']};
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
        }}
        
        /* User message specific */
        [data-testid="stChatMessageContent"]:has(+ [data-testid="stChatMessageAvatar"]) {{
            background: linear-gradient(135deg, rgba(0, 200, 83, 0.2), rgba(76, 175, 80, 0.2));
            border-left: 4px solid {THEME_COLORS['gold']};
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {THEME_COLORS['dark_green']} 0%, {THEME_COLORS['deep_forest']} 100%);
        }}
        
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        /* Voice button component styling */
        iframe {{
            background: transparent !important;
        }}
        
        /* Column containing voice button */
        [data-testid="column"] {{
            background: transparent !important;
        }}
        
        [data-testid="column"] > div {{
            background: transparent !important;
        }}
        
        /* Any stMarkdown or element containers */
        [data-testid="stMarkdownContainer"],
        [data-testid="element-container"] {{
            background: transparent !important;
        }}
        
        /* Streamlit mic recorder component */
        .stMarkdown {{
            background: transparent !important;
        }}
        
        /* Target the voice button wrapper specifically */
        div[data-testid="column"]:first-child,
        div[data-testid="column"]:first-child > div,
        div[data-testid="column"]:first-child div {{
            background: transparent !important;
            background-color: transparent !important;
        }}
        
        /* All vertical blocks in columns */
        .stVerticalBlock {{
            background: transparent !important;
        }}
        
        /* Element container with voice button */
        [data-testid="stVerticalBlock"] > div {{
            background: transparent !important;
        }}
        
        /* Chat input container */
        .stChatInputContainer {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }}
        
        /* Ensure the entire bottom section is transparent */
        .main .block-container {{
            padding-bottom: 0 !important;
        }}
        
        /* Target white spaces */
        .stApp > div:last-child,
        .stApp [data-testid="stAppViewContainer"] > section:last-child {{
            background: linear-gradient(135deg, {THEME_COLORS['deep_forest']} 0%, #0a1f0a 100%) !important;
        }}
        
        /* Text input field itself */
        .stChatInputContainer input {{
            background: rgba(255, 255, 255, 0.1) !important;
            border: 2px solid {THEME_COLORS['emerald']} !important;
            border-radius: 12px !important;
            padding: 12px !important;
            box-shadow: 0 0 10px rgba(0, 200, 83, 0.3) !important;
            color: white !important;
        }}
        
        .stChatInputContainer input:focus {{
            border: 3px solid {THEME_COLORS['gold']} !important;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.5), 0 0 25px rgba(0, 200, 83, 0.2) !important;
        }}
        
        /* Submit button in chat input */
        .stChatInputContainer button {{
            background: linear-gradient(90deg, {THEME_COLORS['dark_green']}, {THEME_COLORS['emerald']}) !important;
            border: none !important;
            color: white !important;
            font-weight: bold !important;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: linear-gradient(90deg, {THEME_COLORS['dark_green']}, {THEME_COLORS['emerald']});
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(90deg, {THEME_COLORS['emerald']}, {THEME_COLORS['gold']});
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
            background: {THEME_COLORS['emerald']};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {THEME_COLORS['gold']};
        }}
    </style>
    
    <style>
        /* Aggressive voice button box removal */
        [data-testid="column"]:first-of-type * {{
            background-color: transparent !important;
            background: transparent !important;
        }}
        
        /* Target streamlit component wrappers */
        .element-container {{
            background: transparent !important;
        }}
        
        .stMarkdown > div {{
            background: transparent !important;
        }}
        
        /* Remove any default backgrounds in the bottom area */
        section[data-testid="stVerticalBlock"] > div:first-child [data-testid="column"] {{
            background: transparent !important;
        }}
        
        section[data-testid="stVerticalBlock"] > div:first-child [data-testid="column"] * {{
            background: transparent !important;
        }}
    </style>
    """, unsafe_allow_html=True)
else:
    # Light mode - Forest Green Theme
    st.markdown(f"""
    <style>
        /* Main app background */
        .stApp {{
            background: linear-gradient(135deg, rgba(165, 214, 167, 0.3), rgba(200, 230, 201, 0.3));
        }}
        
        /* Top bar (header) styling */
        header[data-testid="stHeader"] {{
            background: linear-gradient(90deg, {THEME_COLORS['dark_green']} 0%, {THEME_COLORS['forest']} 100%) !important;
            border-bottom: 3px solid {THEME_COLORS['emerald']};
        }}
        
        /* Header styling */
        .main-header {{
            background: linear-gradient(90deg, {THEME_COLORS['dark_green']} 0%, {THEME_COLORS['emerald']} 50%, {THEME_COLORS['gold']} 100%);
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
            border-left: 4px solid {THEME_COLORS['emerald']};
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        /* User message specific */
        [data-testid="stChatMessageContent"]:has(+ [data-testid="stChatMessageAvatar"]) {{
            background: linear-gradient(135deg, rgba(0, 200, 83, 0.1), rgba(76, 175, 80, 0.1));
            border-left: 4px solid {THEME_COLORS['gold']};
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {THEME_COLORS['dark_green']} 0%, {THEME_COLORS['forest']} 100%);
        }}
        
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        /* Voice button component styling */
        iframe {{
            background: transparent !important;
        }}
        
        [data-testid="column"] {{
            background: transparent !important;
        }}
        
        [data-testid="column"] > div {{
            background: transparent !important;
        }}
        
        [data-testid="stMarkdownContainer"],
        [data-testid="element-container"] {{
            background: transparent !important;
        }}
        
        .stMarkdown {{
            background: transparent !important;
        }}
        
        div[data-testid="column"]:first-child,
        div[data-testid="column"]:first-child > div,
        div[data-testid="column"]:first-child div {{
            background: transparent !important;
            background-color: transparent !important;
        }}
        
        .stVerticalBlock {{
            background: transparent !important;
        }}
        
        [data-testid="stVerticalBlock"] > div {{
            background: transparent !important;
        }}
        
        /* Chat input container */
        .stChatInputContainer {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }}
        
        .main .block-container {{
            padding-bottom: 0 !important;
        }}
        
        /* Target white spaces */
        .stApp > div:last-child,
        .stApp [data-testid="stAppViewContainer"] > section:last-child {{
            background: linear-gradient(135deg, rgba(165, 214, 167, 0.3), rgba(200, 230, 201, 0.3)) !important;
        }}
        
        /* Text input field itself */
        .stChatInputContainer input {{
            background: white !important;
            border: 3px solid {THEME_COLORS['emerald']} !important;
            border-radius: 12px !important;
            padding: 12px !important;
            box-shadow: 0 0 10px rgba(0, 200, 83, 0.3) !important;
        }}
        
        .stChatInputContainer input:focus {{
            border: 3px solid {THEME_COLORS['gold']} !important;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.5), 0 0 25px rgba(0, 200, 83, 0.2) !important;
        }}
        
        /* Submit button in chat input */
        .stChatInputContainer button {{
            background: linear-gradient(90deg, {THEME_COLORS['dark_green']}, {THEME_COLORS['emerald']}) !important;
            border: none !important;
            color: white !important;
            font-weight: bold !important;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: linear-gradient(90deg, {THEME_COLORS['dark_green']}, {THEME_COLORS['emerald']});
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(90deg, {THEME_COLORS['emerald']}, {THEME_COLORS['gold']});
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
            background: {THEME_COLORS['emerald']};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {THEME_COLORS['gold']};
        }}
    </style>
    
    <style>
        /* Aggressive voice button box removal */
        [data-testid="column"]:first-of-type * {{
            background-color: transparent !important;
            background: transparent !important;
        }}
        
        /* Target streamlit component wrappers */
        .element-container {{
            background: transparent !important;
        }}
        
        .stMarkdown > div {{
            background: transparent !important;
        }}
        
        /* Remove any default backgrounds in the bottom area */
        section[data-testid="stVerticalBlock"] > div:first-child [data-testid="column"] {{
            background: transparent !important;
        }}
        
        section[data-testid="stVerticalBlock"] > div:first-child [data-testid="column"] * {{
            background: transparent !important;
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

    # B. RAG Step: Search your facts.json for the answer with improved retrieval
    docs_with_scores = vectorstore.similarity_search_with_score(final_query, k=5)
    
    # IMPROVED: More intelligent relevance filtering
    relevant_docs = []
    context_signal = "NO_CONTEXT"  # Signal to LLM about context quality
    
    if docs_with_scores:
        best_score = docs_with_scores[0][1]
        
        # Stricter threshold for high-confidence retrieval
        # Lower score = more similar (cosine distance)
        if best_score <= 0.35:
            # HIGH CONFIDENCE: Very relevant context found
            context_signal = "HIGH_CONFIDENCE"
            relevant_docs = [doc for doc, score in docs_with_scores if score <= 0.40]
        elif best_score <= 0.50:
            # MEDIUM CONFIDENCE: Possibly relevant context
            context_signal = "MEDIUM_CONFIDENCE"
            relevant_docs = [doc for doc, score in docs_with_scores if score <= 0.50]
        # else: NO_CONTEXT - let LLM use general knowledge
    
    # Deduplicate and build context string
    seen = set()
    deduped_docs = []
    for doc in relevant_docs:
        if doc.page_content not in seen:
            deduped_docs.append(doc)
            seen.add(doc.page_content)
    
    context = "\n".join([d.page_content for d in deduped_docs[:3]]) if deduped_docs else ""

    # --- C. OPTIMIZED PROMPT: Clear instructions, no robotic phrasing triggers ---
    # This prompt is designed to eliminate hallucinations while allowing general knowledge
    if context_signal == "HIGH_CONFIDENCE":
        # Strong context available - prioritize it
        prompt = f"""ප්‍රශ්නය: {final_query}

අදාළ කරුණු:
{context}

උපදෙස්: ඉහත කරුණු භාවිතයෙන් ප්‍රශ්නයට පිළිතුරු දෙන්න. ස්වභාවික සිංහල භාෂාවෙන් කෙලින්ම පිළිතුර ලබා දෙන්න. කිසිදු විස්තරාත්මක වචන හෝ වාක්‍ය ඛණ්ඩ ("සන්දර්භයට අනුව", "ලබා දී ඇති තොරතුරු අනුව" වැනි) භාවිතා නොකරන්න."""

    elif context_signal == "MEDIUM_CONFIDENCE":
        # Possible context - give LLM choice to use or ignore
        prompt = f"""ප්‍රශ්නය: {final_query}

සම්බන්ධ විය හැකි කරුණු:
{context}

උපදෙස්: මෙම ප්‍රශ්නයට පිළිතුරු දෙන්න. ඉහත කරුණු අදාළ නම් ඒවා භාවිතා කරන්න. නොඑසේ නම්, ඔබේ සාමාන්‍ය දැනුම භාවිතයෙන් නිවැරදි පිළිතුරක් ලබා දෙන්න. ස්වභාවික සිංහල භාෂාවෙන් කෙලින්ම පිළිතුර ලබා දෙන්න. විස්තරාත්මක වචන ("සන්දර්භයට අනුව", "මා දන්නා පරිදි" වැනි) භාවිතා නොකරන්න."""

    else:
        # NO_CONTEXT - rely entirely on general knowledge
        prompt = f"""ප්‍රශ්නය: {final_query}

උපදෙස්: ඔබේ සාමාන්‍ය දැනුම භාවිතයෙන් මෙම ප්‍රශ්නයට නිවැරදිව පිළිතුරු දෙන්න. ස්වභාවික සිංහල භාෂාවෙන් කෙලින්ම පිළිතුර ලබා දෙන්න. ඔබට නිශ්චිතව නොදන්නා දෙයක් නම්, කාරුණිකව එය නොදන්නා බව පමණක් සඳහන් කරන්න."""

    # Build the message history for the LLM
    api_messages = []
    # Add all previous history (excluding the most recent user query we just appended)
    for msg in st.session_state.messages[:-1]:
        api_messages.append({"role": msg["role"], "content": msg["content"]})
    # Add the current optimized prompt
    api_messages.append({"role": "user", "content": prompt})

    # Display streaming response
    with chat_container:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_res = ""
            
            stream = ollama.chat(
                model='talk_talk_bot', 
                messages=api_messages, 
                stream=True
            )
            
            for chunk in stream:
                full_res += chunk['message']['content']
                response_placeholder.markdown(full_res + "▌")
            
            response_placeholder.markdown(full_res)

    # D. Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_res})
    
    # E. Speak the response (optional - uncomment to enable)
    # speak(full_res)
    
    # F. Rerun to clear input and update display
    st.rerun()
