import streamlit as st
import base64
import os
import asyncio

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

# File paths
PDF_PATH = "pdf/Pumpkin Porters - Social Performance Progress-Aug-report-v1.pdf"
AUDIO_PATH = "audio/audio.wav"


def display_pdf(pdf_path):
    """Display PDF from local file"""
    try:
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode("utf-8")
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.error(f"PDF file not found at: {pdf_path}")
    except Exception as e:
        st.error(f"Error displaying PDF: {str(e)}")


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

        # Display transcript as summary

        st.subheader("🔊 Audio Summary")

        if os.path.exists(AUDIO_PATH):
            with open(AUDIO_PATH, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/wav")
        else:
            st.error(f"Audio file not found at: {AUDIO_PATH}")
            st.info("Please make sure the audio.wav file is in your project directory.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.write("**Transcript Summary:**")
        st.write(TRANSCRIPT)
        st.markdown("</div>", unsafe_allow_html=True)

        # Audio player
        st.markdown('<div class="audio-container">', unsafe_allow_html=True)

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

            # Alternative: Use Streamlit's built-in warning
            # st.warning("🔧 **Chatbot Temporarily Disabled**  \nWe're currently working on improvements. Please check back soon!")
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
