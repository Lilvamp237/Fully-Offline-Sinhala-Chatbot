import streamlit as st
import ollama
import pyttsx3
from streamlit_mic_recorder import speech_to_text

# CORRECTED IMPORTS FOR 2026
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

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
st.set_page_config(page_title="Talk Talk Bot", page_icon="🤖")
st.title("🤖 Talk Talk Bot (සිංහල)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for Reset
if st.sidebar.button("🗑️ සංවාදය මකන්න (Clear)"):
    st.session_state.messages = []
    st.rerun()

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 3. Processing Input ---
text_voice = speech_to_text(language='si', start_prompt="🎤 කතා කරන්න", key='STT')
text_input = st.chat_input("මෙතන ලියන්න...")
final_query = text_voice if text_voice else text_input

if final_query:
    # A. Display User Input
    st.chat_message("user").markdown(final_query)
    st.session_state.messages.append({"role": "user", "content": final_query})

    # B. RAG Step: Search your facts.json for the answer
    # We find the top 2 most relevant facts
    docs = vectorstore.similarity_search(final_query, k=2)
    context = " ".join([d.page_content for d in docs])

    # C. Assistant Response (Streaming)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_res = ""
        
        # We tell the model to use the facts found in context
        prompt = f"කරුණාකර මෙම තොරතුරු භාවිතා කර නිවැරදිව පිළිතුරු දෙන්න: {context}\n\nප්‍රශ්නය: {final_query}"
        
        stream = ollama.chat(model='talk_talk_bot', messages=[{"role": "user", "content": prompt}], stream=True)
        
        for chunk in stream:
            full_res += chunk['message']['content']
            response_placeholder.markdown(full_res + "▌")
        
        response_placeholder.markdown(full_res)

    # D. Save to history and Speak
    st.session_state.messages.append({"role": "assistant", "content": full_res})
    speak(full_res)