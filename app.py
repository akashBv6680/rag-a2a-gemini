import streamlit as st
import google.generativeai as genai
import json

# Page config
st.set_page_config(
    page_title="RAG AI Agent with A2A",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.markdown("# 🤖 RAG AI Agent with A2A Communication")
st.markdown("### Powered by Google Gemini & Agent-to-Agent Protocol")

# Get API key from secrets
api_key = st.secrets.get("gemini_api_key")

if not api_key:
    st.error("🚨 Please add your Gemini API key to Streamlit Secrets")
    st.info("Steps:\n1. Click Manage app (bottom right)\n2. Go to Settings > Secrets\n3. Add: gemini_api_key = YOUR_KEY")
    st.stop()

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    # Use gemini-1.5-flash (more stable, better quota)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"❌ API Configuration Error: {str(e)}")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    module = st.radio(
        "Select Module",
        ["📄 Document Loader", "💬 RAG Chatbot", "🔗 A2A Network", "🎙️ TTS Demo"]
    )
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'files' not in st.session_state:
        st.session_state.files = []
    if 'agents' not in st.session_state:
        st.session_state.agents = []
    
    # Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Files", len(st.session_state.files))
    with col2:
        st.metric("Agents", len(st.session_state.agents))
    
    if st.button("🗑️ Clear All"):
        st.session_state.messages = []
        st.session_state.files = []
        st.success("Cleared!")

# Module: Document Loader
if module == "📄 Document Loader":
    st.markdown("## 📄 Document Loader")
    st.info("Upload documents (PDF, TXT, CSV) to build RAG knowledge base")
    
    uploaded_files = st.file_uploader(
        "Upload files",
        type=["pdf", "txt", "csv"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for f in uploaded_files:
            if f.name not in st.session_state.files:
                st.session_state.files.append(f.name)
                st.success(f"✅ {f.name}")
        st.info(f"Total files loaded: {len(st.session_state.files)}")

# Module: RAG Chatbot
elif module == "💬 RAG Chatbot":
    st.markdown("## 💬 RAG Chatbot with Gemini")
    st.info("🤖 Powered by Google Gemini 1.5 Flash")
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get response from Gemini
        with st.spinner("🤖 Processing with Gemini..."):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "max_output_tokens": 1024
                    }
                )
                
                if response.text:
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
                    with st.chat_message("assistant"):
                        st.write(response.text)
                else:
                    st.warning("⚠️ No response generated")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("**Troubleshooting:**\n- Check your API key is correct\n- Verify quota limits\n- Try a different query")

# Module: A2A Network
elif module == "🔗 A2A Network":
    st.markdown("## 🔗 Agent-to-Agent Communication Network")
    st.info("Manage AI agents for distributed processing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Register New Agent")
        
        agent_name = st.text_input("Agent Name", placeholder="e.g., Document-Processor")
        agent_url = st.text_input("Agent Endpoint", placeholder="https://api.example.com/v1")
        agent_capability = st.selectbox(
            "Capability",
            ["Document Processing", "Data Analysis", "Summarization", "Classification"]
        )
        
        if st.button("✅ Register Agent"):
            if agent_name and agent_url:
                agent = {
                    "name": agent_name,
                    "url": agent_url,
                    "capability": agent_capability,
                    "status": "active"
                }
                st.session_state.agents.append(agent)
                st.success(f"✅ Agent '{agent_name}' registered!")
                st.rerun()
            else:
                st.warning("⚠️ Please fill all fields")
    
    with col2:
        st.subheader("Registered Agents")
        if st.session_state.agents:
            for i, agent in enumerate(st.session_state.agents):
                with st.expander(f"🤖 {agent['name']}"):
                    st.json(agent)
                    if st.button(f"Delete", key=f"delete_{i}"):
                        st.session_state.agents.pop(i)
                        st.rerun()
        else:
            st.info("No agents registered yet")

# Module: TTS Demo
elif module == "🎙️ TTS Demo":
    st.markdown("## 🎙️ Text-to-Speech Demo")
    st.info("Convert text to speech (ready for implementation)")
    
    tts_text = st.text_area(
        "Text to convert",
        value="Welcome to the RAG AI Agent with A2A Communication!",
        height=100
    )
    
    if st.button("🎙️ Generate Speech"):
        st.info("🎙️ TTS feature ready for integration with Edge-TTS or Google TTS")

# Footer
st.divider()
st.markdown("---")
st.markdown("**🔗 Repository**: [GitHub](https://github.com/akashBv6680/rag-a2a-gemini)")
st.markdown("**🚀 Deployed on**: Streamlit Cloud")
st.markdown("**🤖 Powered by**: Google Gemini 1.5 Flash API")
