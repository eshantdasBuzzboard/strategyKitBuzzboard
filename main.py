import streamlit as st
import base64
import os
import asyncio
from pathlib import Path

from strategy_kit_core_model.utils.constants import pumpkin_porters_transcript

# Set page config
st.set_page_config(
    page_title="StrategyKit Report Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better UI
st.markdown(
    """
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    color: #2E4057;
    margin-bottom: 2rem;
}

.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    display: flex;
    align-items: center;
}

.chat-message.user {
    background-color: #000000
    justify-content: flex-end;
}

.chat-message.bot {
    background-color: #000000;
    justify-content: flex-start;
}

.summary-box {
    background-color: #000000;
    padding: 1.5rem;
    border-radius: 0.5rem;
    border-left: 4px solid #000000;
    margin: 1rem 0;
}

.audio-container {
    margin: 1rem 0;
    padding: 1rem;
    background-color: ##000000;
    border-radius: 0.5rem;
}

.maintenance-banner {
    background: linear-gradient(90deg, #FFA500, #FF6B35);
    color: white;
    padding: 1rem;
    border-radius: 0.5rem;
    text-align: center;
    font-weight: bold;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.disabled-overlay {
    position: relative;
    opacity: 0.6;
    pointer-events: none;
}

.disabled-overlay::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(128, 128, 128, 0.3);
    border-radius: 0.5rem;
}

.file-info {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #1f77b4;
    margin: 1rem 0;
}
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Configuration - Set this to False to enable chatbot
CHATBOT_ENABLED = False

# Your transcript string (replace this with your actual transcript)
TRANSCRIPT = pumpkin_porters_transcript

# File paths - Using relative paths and Path for better cross-platform compatibility
BASE_DIR = Path(__file__).parent
PDF_PATH = (
    BASE_DIR / "pdf" / "Pumpkin Porters - Social Performance Progress-Aug-report-v1.pdf"
)
AUDIO_PATH = BASE_DIR / "audio" / "audio.wav"

# Alternative file paths to check
ALTERNATIVE_PDF_PATHS = [
    "pdf/Pumpkin Porters - Social Performance Progress-Aug-report-v1.pdf",
    "./pdf/Pumpkin Porters - Social Performance Progress-Aug-report-v1.pdf",
    "Pumpkin Porters - Social Performance Progress-Aug-report-v1.pdf",
    "./Pumpkin Porters - Social Performance Progress-Aug-report-v1.pdf",
]

ALTERNATIVE_AUDIO_PATHS = [
    "audio/audio.wav",
    "./audio/audio.wav",
    "audio.wav",
    "./audio.wav",
]


def find_file(primary_path, alternative_paths):
    """Find file from multiple possible locations"""
    # Check primary path first
    if os.path.exists(primary_path):
        return str(primary_path)

    # Check alternative paths
    for path in alternative_paths:
        if os.path.exists(path):
            return path

    return None


def display_pdf(pdf_path):
    """Display PDF from local file with better error handling"""
    try:
        # Find the actual file location
        actual_pdf_path = find_file(pdf_path, ALTERNATIVE_PDF_PATHS)

        if actual_pdf_path:
            with open(actual_pdf_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode("utf-8")
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)

            # Show file info
            st.markdown(
                f"""
                <div class="file-info">
                    📁 <strong>File loaded successfully:</strong> {actual_pdf_path}
                </div>
            """,
                unsafe_allow_html=True,
            )

        else:
            st.error("📄 PDF file not found!")
            st.markdown(
                """
                <div class="file-info">
                    <strong>Troubleshooting Tips:</strong><br>
                    1. Make sure the PDF file is uploaded to your repository<br>
                    2. Check that the file path is correct<br>
                    3. Ensure the file is in the same directory structure as your code<br>
                    4. Verify the file name matches exactly (including spaces and hyphens)
                </div>
            """,
                unsafe_allow_html=True,
            )

            # Show current directory contents for debugging
            st.write("**Current directory contents:**")
            try:
                current_files = os.listdir(".")
                st.write(current_files)

                # Check if pdf folder exists
                if "pdf" in current_files:
                    st.write("**Contents of pdf folder:**")
                    pdf_files = os.listdir("pdf")
                    st.write(pdf_files)
                else:
                    st.warning("⚠️ 'pdf' folder not found in current directory")

            except Exception as e:
                st.error(f"Error listing directory contents: {str(e)}")

            # Provide file upload option as fallback
            st.markdown("---")
            st.subheader("Upload PDF File")
            uploaded_file = st.file_uploader(
                "Upload the PDF file here as a temporary solution:",
                type="pdf",
                help="This will display the PDF for this session only",
            )

            if uploaded_file is not None:
                # Display uploaded PDF
                base64_pdf = base64.b64encode(uploaded_file.read()).decode("utf-8")
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
                st.success("✅ PDF uploaded and displayed successfully!")

    except Exception as e:
        st.error(f"❌ Error displaying PDF: {str(e)}")
        st.info(
            "💡 **Deployment Tip**: Make sure your PDF file is included in your Git repository and the path is correct for Streamlit Cloud."
        )


def display_audio(audio_path):
    """Display audio with better error handling"""
    try:
        # Find the actual file location
        actual_audio_path = find_file(audio_path, ALTERNATIVE_AUDIO_PATHS)

        if actual_audio_path:
            with open(actual_audio_path, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/wav")

            st.markdown(
                f"""
                <div class="file-info">
                    🔊 <strong>Audio file loaded:</strong> {actual_audio_path}
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.error("🔊 Audio file not found!")
            st.info(
                "Please make sure the audio.wav file is uploaded to your repository in the correct location."
            )

            # Provide file upload option as fallback
            uploaded_audio = st.file_uploader(
                "Upload the audio file here:",
                type=["wav", "mp3", "m4a"],
                help="Upload audio file as a temporary solution",
            )

            if uploaded_audio is not None:
                st.audio(uploaded_audio.read())
                st.success("✅ Audio uploaded and ready to play!")

    except Exception as e:
        st.error(f"❌ Error loading audio: {str(e)}")


def get_bot_response(user_input):
    """Simple chatbot with predefined responses"""
    user_input = user_input.lower().strip()

    # Greeting responses
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    if any(greeting in user_input for greeting in greetings):
        return "Hello! I'm here to help you with information about the PDF document. How can I assist you today?"

    # PDF related questions
    if "pdf" in user_input or "document" in user_input:
        return "This PDF contains the Social Performance Progress report for Pumpkin Porters from August. You can view it in the PDF Viewer tab and listen to the summary in the Summary tab."

    # Summary related questions
    if "summary" in user_input or "summarize" in user_input:
        return "You can find the document summary in the Summary tab. There's also an audio version you can play!"

    # Audio related questions
    if "audio" in user_input or "listen" in user_input or "play" in user_input:
        return "You can listen to the audio version of the summary in the Summary tab. Just click the play button!"

    # Help
    if "help" in user_input:
        return "I can help you with:\n- Information about the PDF document\n- How to access the summary\n- How to play the audio version\n- General questions about the report"

    # Thank you
    if "thank" in user_input:
        return "You're welcome! Is there anything else you'd like to know about the document?"

    # Goodbye
    if any(word in user_input for word in ["bye", "goodbye", "see you", "exit"]):
        return "Goodbye! Feel free to come back if you have more questions about the document."

    # Default response
    return "I'm a simple chatbot focused on this PDF document. I can help with basic questions about the report, summary, and audio features. Could you rephrase your question?"


async def main():
    st.markdown(
        '<h1 class="main-header">📄  StrategyKit Report Analyzer</h1>',
        unsafe_allow_html=True,
    )

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📄 PDF Viewer", "📝 Summary", "💬 Chatbot"])

    with tab1:
        st.header("PDF Viewer")
        st.subheader("Pumpkin Porters - Social Performance Progress Report")
        display_pdf(PDF_PATH)

    with tab2:
        st.header("Document Summary")

        st.subheader("🔊 Audio Summary")
        display_audio(AUDIO_PATH)

        st.write("**Transcript Summary:**")
        st.write(TRANSCRIPT)

    with tab3:
        st.header("Chat with Assistant")

        # Show maintenance banner if chatbot is disabled
        if not CHATBOT_ENABLED:
            st.markdown(
                """
                <div class="maintenance-banner">
                    🔧 Chatbot is temporarily disabled - We're working on improvements!<br>
                    <small> Thank you for your patience.</small>
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.write("Ask me about the PDF document, summary, or audio features!")

        # Wrap the chat interface in a container that can be disabled
        chat_container_class = "disabled-overlay" if not CHATBOT_ENABLED else ""

        if chat_container_class:
            st.markdown(f'<div class="{chat_container_class}">', unsafe_allow_html=True)

        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                if message["type"] == "user":
                    st.markdown(
                        f"""
                    <div class="chat-message user">
                        <div><strong>You:</strong> {message["content"]}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                    <div class="chat-message bot">
                        <div><strong>Assistant:</strong> {message["content"]}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Type your message:",
                placeholder="Chatbot is temporarily disabled..."
                if not CHATBOT_ENABLED
                else "Hello, can you tell me about this document?",
                disabled=not CHATBOT_ENABLED,
            )
            col1, col2 = st.columns([1, 4])

            with col1:
                submit_button = st.form_submit_button(
                    "Send", use_container_width=True, disabled=not CHATBOT_ENABLED
                )

            if submit_button and user_input and CHATBOT_ENABLED:
                # Add user message to chat history
                st.session_state.chat_history.append({
                    "type": "user",
                    "content": user_input,
                })

                # Generate bot response
                bot_response = get_bot_response(user_input)

                # Add bot response to chat history
                st.session_state.chat_history.append({
                    "type": "bot",
                    "content": bot_response,
                })

                st.rerun()

        # Quick action buttons
        st.write("**Quick Actions:**")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("👋 Say Hello", disabled=not CHATBOT_ENABLED):
                if CHATBOT_ENABLED:
                    st.session_state.chat_history.append({
                        "type": "user",
                        "content": "Hello",
                    })
                    st.session_state.chat_history.append({
                        "type": "bot",
                        "content": get_bot_response("Hello"),
                    })
                    st.rerun()

        with col2:
            if st.button("📄 About PDF", disabled=not CHATBOT_ENABLED):
                if CHATBOT_ENABLED:
                    st.session_state.chat_history.append({
                        "type": "user",
                        "content": "Tell me about the PDF",
                    })
                    st.session_state.chat_history.append({
                        "type": "bot",
                        "content": get_bot_response("Tell me about the PDF"),
                    })
                    st.rerun()

        with col3:
            if st.button("📝 About Summary", disabled=not CHATBOT_ENABLED):
                if CHATBOT_ENABLED:
                    st.session_state.chat_history.append({
                        "type": "user",
                        "content": "Tell me about the summary",
                    })
                    st.session_state.chat_history.append({
                        "type": "bot",
                        "content": get_bot_response("Tell me about the summary"),
                    })
                    st.rerun()

        with col4:
            if st.button("🔄 Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()

        if chat_container_class:
            st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    asyncio.run(main())
