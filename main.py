import streamlit as st
import base64
import os
import asyncio
from pathlib import Path
import json
from datetime import datetime

from strategy_kit_core_model.utils.constants import (
    pumpkin_porters_transcript,
    junk_text,
    level_two_summary,
)
from strategy_kit_chatbot.core.chains import chatbot_reply_chain

# Set page config
st.set_page_config(
    page_title="StrategyKit Report Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
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
    background-color: #e3f2fd;
    justify-content: flex-start;
    border-left: 4px solid #2196f3;
    color: black;
}
.chat-message.bot {
    background-color: #f3e5f5;
    justify-content: flex-start;
    border-left: 4px solid #9c27b0;
    color: black;
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
if "chat_session_id" not in st.session_state:
    st.session_state.chat_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# File paths
BASE_DIR = Path(__file__).parent
PDF_PATH = (
    BASE_DIR / "pdf" / "Pumpkin Porters - Social Performance Progress-Aug-report-v1.pdf"
)
AUDIO_PATH = BASE_DIR / "audio" / "audio.wav"

ALTERNATIVE_PDF_PATHS = [
    "pdf/Pumpkin Porters - Social Performance Progress-Aug-report-v1.pdf",
    "./pdf/Pumpkin Porters - Social Performance Progress-Aug-report-v1.pdf",
    "Pumpkin Porters - Social Performance Progress-Aug-report-v1.pdf",
]

ALTERNATIVE_AUDIO_PATHS = [
    "audio/audio.wav",
    "./audio/audio.wav",
    "audio.wav",
]


def find_file(primary_path, alternative_paths):
    """Find file from multiple possible locations"""
    if os.path.exists(primary_path):
        return str(primary_path)

    for path in alternative_paths:
        if os.path.exists(path):
            return path
    return None


def add_message_to_history(message_type, content):
    """Add a message to chat history"""
    message = {
        "type": message_type,
        "content": content,
    }
    st.session_state.chat_history.append(message)


def display_pdf(pdf_path):
    """Display PDF with download and view options"""
    actual_pdf_path = find_file(pdf_path, ALTERNATIVE_PDF_PATHS)

    if actual_pdf_path:
        st.markdown(
            f"""
            <div class="file-info">
                📁 <strong>File found:</strong> {actual_pdf_path}
            </div>
        """,
            unsafe_allow_html=True,
        )

        file_size = os.path.getsize(actual_pdf_path)
        st.info(
            f"📊 PDF file size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)"
        )

        with open(actual_pdf_path, "rb") as f:
            pdf_bytes = f.read()

        base64_pdf = base64.b64encode(pdf_bytes).decode()

        # Download button
        st.download_button(
            label="📥 Download PDF Document",
            data=pdf_bytes,
            file_name="Pumpkin_Porters_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

        # View in browser
        st.markdown("---")
        st.subheader("🌐 View PDF in Browser")

        universal_script = f"""
        <script>
        function openPDFUniversal() {{
            try {{
                const base64Data = '{base64_pdf}';
                const byteCharacters = atob(base64Data);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {{
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }}
                const byteArray = new Uint8Array(byteNumbers);
                const blob = new Blob([byteArray], {{type: 'application/pdf'}});
                
                const blobUrl = URL.createObjectURL(blob);
                const newWindow = window.open(blobUrl, '_blank');
                if (!newWindow) {{
                    const link = document.createElement('a');
                    link.href = blobUrl;
                    link.download = 'Pumpkin_Porters_Report.pdf';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    URL.revokeObjectURL(blobUrl);
                }}
            }} catch (error) {{
                alert('PDF opening failed. Please use the download button above.');
            }}
        }}
        </script>
        <button onclick="openPDFUniversal()" style="background-color: #28a745; color: white; border: none; padding: 15px 30px; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold;">
            🚀 Open PDF (All Browsers)
        </button>
        """
        st.markdown(universal_script, unsafe_allow_html=True)

    else:
        st.error("📄 PDF file not found!")
        uploaded_file = st.file_uploader("Upload the PDF file here:", type="pdf")

        if uploaded_file is not None:
            st.download_button(
                label="📥 Download Uploaded PDF",
                data=uploaded_file.getvalue(),
                file_name=uploaded_file.name,
                mime="application/pdf",
            )


def display_audio(audio_path):
    """Display audio player"""
    actual_audio_path = find_file(audio_path, ALTERNATIVE_AUDIO_PATHS)

    if actual_audio_path:
        with open(actual_audio_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/wav")
    else:
        st.error("🔊 Audio file not found!")
        uploaded_audio = st.file_uploader(
            "Upload the audio file here:", type=["wav", "mp3", "m4a"]
        )
        if uploaded_audio is not None:
            st.audio(uploaded_audio.read())


async def get_bot_response(user_input, chat_history=[]):
    """Enhanced chatbot with chat history context"""
    user_input = user_input.lower().strip()
    print("++++==============+++")
    print(chat_history)
    print(user_input)
    if user_input:
        with st.spinner("Thinking..."):
            response = await chatbot_reply_chain(
                junk_data=junk_text,
                ai_data=pumpkin_porters_transcript,
                query=user_input,
                chat_history=chat_history,
            )

        return response

    # Default response
    return "I'm focused on helping with the Pumpkin Porters Social Performance Progress report. I can assist with PDF access, audio summary, report content questions, and navigation help. Could you please rephrase your question?"


async def main():
    st.markdown(
        '<h1 class="main-header">📄 StrategyKit Report Analyzer</h1>',
        unsafe_allow_html=True,
    )

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📝 Summary", "💬 Chatbot", "📄 Detailed Report"])

    with tab1:
        st.header("Document Summary")

        # PDF download
        actual_pdf_path = find_file(PDF_PATH, ALTERNATIVE_PDF_PATHS)
        if actual_pdf_path:
            try:
                with open(actual_pdf_path, "rb") as f:
                    pdf_bytes = f.read()

                st.download_button(
                    label="📥 Download Strategy Kit PDF",
                    data=pdf_bytes,
                    file_name="StrategyKit_Pumpkin_Porters_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
                st.markdown("---")
            except Exception as e:
                st.error(f"Error loading PDF: {str(e)}")

        st.subheader("🔊 Audio Summary")
        display_audio(AUDIO_PATH)

        st.write("**Quick Audio Transcript:**")
        st.write(level_two_summary)

    with tab2:
        st.header("Chat with Assistant")

        # Display chat history
        for message in st.session_state.chat_history:
            if message["type"] == "user":
                st.markdown(
                    f"""
                <div class="chat-message user">
                    <div style="color: black;"><strong>You:</strong> {message["content"]}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                <div class="chat-message bot">
                    <div style="color: black;"><strong>Assistant:</strong> {message["content"]}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Type your message:",
                placeholder="Hello, can you tell me about this document?",
            )
            submit_button = st.form_submit_button("Send", use_container_width=True)

            if submit_button and user_input:
                # Add user message
                add_message_to_history("user", user_input)

                # Generate bot response with chat history
                bot_response = await get_bot_response(
                    user_input, st.session_state.chat_history
                )

                # Add bot response
                add_message_to_history("bot", bot_response)

                st.rerun()

        # Export chat history
        if st.session_state.chat_history:
            st.markdown("---")
            st.write("**Export Chat History:**")

            export_data = {
                "session_id": st.session_state.chat_session_id,
                "exported_at": datetime.now().isoformat(),
                "total_messages": len(st.session_state.chat_history),
                "chat_history": st.session_state.chat_history,
            }

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    label="📥 Download Chat (JSON)",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"chat_history_{st.session_state.chat_session_id}.json",
                    mime="application/json",
                )

            with col2:
                text_export = f"Chat Session: {st.session_state.chat_session_id}\n"
                text_export += (
                    f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                text_export += "=" * 50 + "\n\n"

                for msg in st.session_state.chat_history:
                    if msg["type"] == "user":
                        text_export += f"USER: {msg['content']}\n\n"
                    else:
                        text_export += f"ASSISTANT: {msg['content']}\n\n"

                st.download_button(
                    label="📄 Download Chat (Text)",
                    data=text_export,
                    file_name=f"chat_history_{st.session_state.chat_session_id}.txt",
                    mime="text/plain",
                )

    with tab3:
        st.header("Detailed Report Summary")
        st.write(pumpkin_porters_transcript)


if __name__ == "__main__":
    asyncio.run(main())
