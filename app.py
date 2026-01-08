import streamlit as st
import os
import json
from pathlib import Path
import google.generativeai as genai
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="RAG AI Agent with A2A 📚🔗",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1f77b4; margin-bottom: 1rem; }
    .status-box { padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; }
    .status-success { background-color: #d4edda; border: 1px solid #28a745; color: #155724; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_gemini():
    try:
        api_key = st.secrets["gemini_api_key"]
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        st.error(f"Gemini API Error: {e}")
        return None

def main():
    st.markdown("# 🤖 RAG AI Agent with A2A Communication")
    st.markdown("### Powered by Google Gemini & Agent-to-Agent Protocol")
    
    model = init_gemini()
    if not model:
        st.error("Configure Gemini API key in secrets")
        return
    
    with st.sidebar:
        st.header("⚙️ Settings")
        module = st.radio(
            "Select Module",
            ["📄 Document Loader", "💬 RAG Chatbot", "🔗 A2A Network", "🎙️ TTS Demo"]
        )
        
        if 'loaded_chunks' not in st.session_state:
            st.session_state.loaded_chunks = []
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'agents' not in st.session_state:
            st.session_state.agents = []
        
        st.metric("Loaded Chunks", len(st.session_state.loaded_chunks))
        st.metric("Registered Agents", len(st.session_state.agents))
        
        if st.button("🗑️ Clear Storage"):
            st.session_state.loaded_chunks = []
            st.session_state.chat_history = []
            st.success("Storage cleared!")
    
    if module == "📄 Document Loader":
        st.markdown("## 📄 Document Loader")
        st.info("Upload documents to build RAG knowledge base")
        files = st.file_uploader("Upload files", type=["pdf", "txt", "csv", "html", "json"], accept_multiple_files=True)
        if files:
            for f in files:
                st.success(f"✅ {f.name}")
    
    elif module == "💬 RAG Chatbot":
        st.markdown("## 💬 RAG Chatbot")
        st.info("🤖 Hello! Ask me about your documents (powered by Gemini)")
        
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.write(f"👤 You: {msg['content']}")
            else:
                st.write(f"🤖 Bot: {msg['content']}")
        
        user_input = st.text_area("Ask a question...", placeholder="What would you like to know?")
        if st.button("Send"):
            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                try:
                    response = model.generate_content(user_input)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                    st.success("✅ Response generated")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
    
    elif module == "🔗 A2A Network":
        st.markdown("## 🔗 Agent-to-Agent Communication")
        st.info("Manage AI agents for distributed RAG processing")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Register Agent")
            agent_name = st.text_input("Agent Name")
            agent_url = st.text_input("Agent URL")
            if st.button("Register"):
                if agent_name and agent_url:
                    agent_card = {
                        "name": agent_name,
                        "url": agent_url,
                        "capability": "RAG Processing",
                        "status": "active"
                    }
                    st.session_state.agents.append(agent_card)
                    st.success(f"Agent {agent_name} registered!")
        
        with col2:
            st.subheader("Registered Agents")
            if st.session_state.agents:
                for agent in st.session_state.agents:
                    st.json(agent)
            else:
                st.warning("No agents registered yet")
    
    elif module == "🎙️ TTS Demo":
        st.markdown("## 🎙️ Text-to-Speech Demo")
        tts_text = st.text_area("Text to convert", "This is a TTS demonstration.")
        if st.button("Generate Speech"):
            st.info("🎙️ TTS feature (ready for implementation)")

if __name__ == "__main__":
    main()
