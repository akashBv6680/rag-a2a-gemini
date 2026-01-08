import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="RAG AI Agent with A2A", page_icon="🤖", layout="wide")

st.markdown("# 🤖 RAG AI Agent with A2A Communication")
st.markdown("### Powered by Google Gemini & Agent-to-Agent Protocol")

# Get API key from secrets
api_key = st.secrets.get("gemini_api_key", "")

if not api_key:
    st.error("🚨 Please add your Gemini API key to Streamlit Secrets")
    st.info("Steps:\n1. Go to App Settings > Secrets\n2. Add: gemini_api_key = YOUR_KEY")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

with st.sidebar:
    st.header("⚙️ Settings")
    module = st.radio(
        "Select Module",
        ["📄 Document Loader", "💬 RAG Chatbot", "🔗 A2A Network", "🎙️ TTS Demo"]
    )
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'files' not in st.session_state:
        st.session_state.files = []
    if 'agents' not in st.session_state:
        st.session_state.agents = []
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Files", len(st.session_state.files))
    with col2:
        st.metric("Agents", len(st.session_state.agents))
    
    if st.button("🗑️ Clear All"):
        st.session_state.messages = []
        st.session_state.files = []
        st.success("Cleared!")

if module == "📄 Document Loader":
    st.markdown("## 📄 Document Loader")
    st.info("Upload documents (PDF, TXT, CSV) to build RAG knowledge base")
    files = st.file_uploader("Upload files", type=["pdf", "txt", "csv"], accept_multiple_files=True)
    if files:
        for f in files:
            st.session_state.files.append(f.name)
            st.success(f"✅ {f.name}")

elif module == "💬 RAG Chatbot":
    st.markdown("## 💬 RAG Chatbot")
    st.info("🤖 Chat powered by Google Gemini")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.spinner("🤖 Thinking..."):
            try:
                response = model.generate_content(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                with st.chat_message("assistant"):
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

elif module == "🔗 A2A Network":
    st.markdown("## 🔗 Agent-to-Agent Network")
    st.info("Manage AI agents for distributed processing")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Register Agent")
        name = st.text_input("Agent Name")
        url = st.text_input("Agent URL")
        if st.button("Register"):
            if name and url:
                st.session_state.agents.append({"name": name, "url": url})
                st.success(f"✅ {name} registered")
    
    with col2:
        st.subheader("Registered Agents")
        for agent in st.session_state.agents:
            st.json(agent)

elif module == "🎙️ TTS Demo":
    st.markdown("## 🎙️ Text-to-Speech Demo")
    text = st.text_area("Text to convert", "Welcome to RAG A2A Gemini!")
    if st.button("🎙️ Generate Speech"):
        st.info("TTS feature - ready for implementation")

st.markdown("---")
st.markdown("**Repository**: [GitHub](https://github.com/akashBv6680/rag-a2a-gemini)")
st.markdown("**Deployed on**: Streamlit Cloud 🚀")
