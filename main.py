import streamlit as st
import base64
import os
import asyncio
from pathlib import Path
import json
from datetime import datetime


from strategy_kit_chatbot.core.chains import chatbot_reply_chain

pumpkin_porters_transcript = """
Here’s a detailed summary of the key points, analysis, and important details from the document:

Pumpkin Porters’ marketing progress from June to August 2025 shows significant growth in social media visibility and engagement, especially on Instagram. The brand has been consistently posting and running Facebook Ads, which have expanded in volume. However, the report notes that Facebook Ads now require fresh creatives to control the cost per click (CPC) and recover the efficiency seen in July.

**Big Wins and Key Metrics:**
- Instagram impressions increased dramatically from 60 in July to 389 in August, a 548% growth.
- Facebook posts increased from 5 in June to 11 in August, also a 548% growth.
- Facebook Ads delivered 469 clicks at a 12.14% click-through rate (CTR) in July, with an efficient CPC of $0.31 in August, representing a 110% increase in clicks.
- The brand maintained a 100% review response rate, which is crucial for building trust with the local audience.

**Initial Strategy Commitments:**
- The initial strategy set follower and engagement targets for both Facebook and Instagram, with a $50 ad spend on Facebook and Google. The goal was to build early visibility and attract local customers.
- For Facebook, the target was to grow from 0 to 50–70 followers over 12 months. For Instagram, the target was 18–30 followers in the same period.
- The report emphasizes that followers are considered meaningful local leads, likely to convert into customers.

**Content and Campaign Delivery:**
- Ongoing and on-demand posts were published to boost brand visibility and engagement, including seasonal promotions and new ad creatives.
- Two Facebook ad campaigns were launched to drive engagement and visibility.
- The timeline of content delivery includes initial campaign content in June, brand voice highlights in July, and engagement-focused posts and new ad creatives in August.

**Growth Analysis:**
- Instagram was the strongest growth driver, with impressions rising from 60 to 389.
- Facebook Ads delivered engagement but need refreshed creatives to reduce CPC and lift CTR back above 12%.
- Facebook impressions dropped from 2,235 in July to 77 in August, a 67% decrease, indicating the need for new ad content.
- Facebook Ads clicks dropped from 469 in July to 88 in August, an 81% decrease, further highlighting the need for creative updates.

**Ad Performance:**
- Six active Facebook ad campaigns ran in August, with an average CPC of $0.31, up from $0.09 in July.
- The CTR for Facebook Ads was 10.15% in August, down from 12.14% in July, but still considered strong.
- Google Ads were not active in August; only organic search and maps visibility contributed, resulting in three site clicks. The report notes that Google Ads remain a missed opportunity until reactivated.

**September Game Plan:**
- Instagram: Submit on-demand requests for seasonal content to lift reach to over 500 impressions. Posts will focus on event highlights and specials.
- Google Ads: Relaunch local keyword campaigns with a goal of generating 150+ clicks. This requires confirming the budget and creating new ads.
- Facebook Ads: Request edits for ad creatives to improve CTR above 12%. The plan is to refresh visuals and copy for better engagement.
- Social Media: Share seasonal event stories and customer reviews, aiming for 1,000+ impressions per platform. The plan includes scheduling 3–4 posts weekly to showcase fall events and customer experiences.

**Quick Actions for the Client:**
- Submit requests for event-based posts and ad variations to test and optimize performance.
- Share customer photos and reviews to update ad visuals and captions.

**Summary of Key Insights:**
- Instagram visibility is rapidly increasing, and Facebook Ads are still driving engagement, but both need ongoing creative updates to maintain efficiency.
- Google Ads are currently underutilized and represent a significant opportunity for growth if reactivated.
- Consistent content and engagement strategies are strengthening Pumpkin Porters’ local presence.
- The focus for September is on refreshing ad creatives, relaunching Google Ads, and leveraging seasonal content to boost visibility, engagement, and customer conversions.

**Graph Analysis:**
- The graph for Facebook shows a steady increase in followers, with the current number approaching the 30–50 range, moving toward the 50–70 target.
- The Instagram graph shows a similar upward trend, with current followers in the 10–18 range, progressing toward the 18–30 target.
- Both graphs reinforce the message that the brand is on track with its follower growth goals, and that continued engagement and content delivery are key to reaching the targets.

In summary, Pumpkin Porters is making strong progress in building its local brand presence through social media and advertising. The main areas for improvement are refreshing Facebook ad creatives and reactivating Google Ads to maximize reach and efficiency in the coming months.
"""

junk_text = """Marketing Progress
Pumpkin Porters
https://www.facebook.com/people/Pumpkin-Porters/61577839870228/#
https://tinyurl.com/ycxwea5y
(817) 456-5484
https://pumpkinporters.com/
June – August 2025Big Wins This Month
Your Brand in Action
Growth at a Glance
What’s Coming in September – Game Plan
Initial Strategy Commitments
Here’s What We Delivered for You
How Your Ads Performed
Quick Actions for You
Table of
ContentsBig Wins This Month
What Does It Mean?
Pumpkin Porters is growing visibility through Instagram and consistent posting. Facebook Ads expanded in volume but 
need fresh creatives to control CPC and recover July-level eﬃciency.
Facebook Ads Delivered  
Results
CTR (Click Through Rate)
CPC (Cost Per Click) 
469 clicks at $12.14 CTR
eﬃcient $0.31 in August
(+110% increase)
Facebook Posts
June
Aug
5 → 11
(+548% growth)
Instagram Impression
July
Aug
60 → 389Initial Strategy Commitments
At launch, we set follower and engagement targets for Facebook and Instagram, along with a $50 ad spend on 
Facebook and Google — all designed to build visibility and attract your ideal local audience. These commitments 
were established to generate early traction and lay the foundation for long-term growth.
Goals & Current Progress
Facebook
Instagram
Month
0
25
50
75
100
3
6
1
12
0
0-5
50
15–30
30–50
50–70
Followers
Initial
Current
Target
Followers
Month
0
10
20
30
40
3
6
1
12
0
0–5
5–10
10–18
18–30
Initial
Current
Target
3
What Does It Mean?
‘Followers’ represent meaningful local leads, most likely to convert into customers. 
100% review response rate is maintained as part of trust-building strategy.Here’s What We Delivered for You
Jun 04
On Going Post
Initial ongoing campaign content published to start 
brand visibility.
Jul 29
highlight Pumpkin Porters’ unique 
brand voice.
On Demand Post
August 19–21
Engagement + seasonal promos.
On-Demand Post
Aug 14
New ad creatives launched to sustain CTR and capture 
fresh audience segments.
Facebook Ads
August, 25–28
Oﬀers + community + month-end push.
On-demad Post 
Jul 25
Facebook Ad
Two ad campaigns launched to build visibility and drive 
engagement.Growth at a Glance
What Does It Mean?
Instagram drove the strongest growth. Facebook Ads delivered engagement but needs refreshed creatives to reduce CPC 
and lift CTR back above 12%.
Metric
Facebook 
Posts
Instagram 
Posts
July 
2025
June 
2025
13
5
4
0
Change
▼ –15%
+50%
Facebook 
Impressions
235
2
▼ –67%
Instagram 
Impressions
60
0
+548%
Aug 
2025
11
6
77
389
Facebook Ads 
CTR (%)
12.14
–
▼ –16%
10.15
Facebook Ads 
Clicks
469
0
▼ –81%
88Your Brand in Action
AD
ADHow Your Ads Performed
Facebook advertising campaigns, and here's how they performed for you:
What Does It Mean?
Facebook Ads are delivering a strong Click-Through Rate. Pumpkin Porters is steadily building a brand identity.
Facebook Ads – 
Awareness & Engagement 
Campaigns
Active Campaigns: 6 
Average CPC: $0.31 ( vs 
July’s $0.09)
Delivered 88 clicks at a 
10.15% Click Through 
Rate (strong, though 
from July’s 12.14%)
Google Ads Status
Only organic Maps/Search visibility 
contributed, producing 3 site clicks. 
Google Ads remain a missed 
opportunity until reactivated.
No active Google Ads 
this month.What’s Coming in September – Game Plan
Focus Area
Action
Goal
Execution
Instagram
Submit OD request for 
seasonal content
Lift reach to 500+
Fulﬁllment will recreate posts 
(e.g., event highlights, specials).
Google Ads
Relaunch local keyword 
campaigns
Generate 150+ clicks
Conﬁrm budget → Fulﬁllment 
will create ads and relaunch 
campaigns.
Facebook Ads
Request edits for ad 
creatives
Improve CTR above 
12%
Fulﬁllment will refresh visuals + 
copy to increase relevance & 
engagement.
Social Media
Share seasonal event stories 
+ reviews
1,000+ impressions per 
platform
Schedule 3–4 posts weekly 
showcasing fall events & 
customer experiences.Quick Actions for You
Submit OD request for event-based posts → Share oﬀers/events (e.g., Halloween sale); 
Fulﬁllment designs + publishes campaign posts.
Submit OD request for two ad variations → Fulﬁllment will test creatives and optimize 
ad performance.
Request edits for ad creatives → Share customer photos/reviews; Fulﬁllment updates 
visuals + captions.Instagram visibility is rising (+548%), and Facebook Ads continue to drive engagement. 
With fresh creatives and Google Ads reactivation, September can build stronger visibility, 
eﬃciency, and customer conversions.
Pumpkin Porters is strengthening its local presence with consistent content 
and engaging ads.
"""


level_two_summary = """
Hey Pumpkin Porters team! We wanted to create this quick audio summary to walk you through the key findings from our latest marketing report.

First, fantastic news on Instagram! Impressions jumped by over 500 percent in August, showing real momentum in our local brand visibility. Facebook posts and ad clicks also saw big increases, and we’re maintaining a perfect review response rate—great job building trust with our audience.

However, we do have some challenges to address. Facebook ad performance dropped in August, with fewer clicks and higher costs. This means it’s time to refresh our ad creatives to get those numbers back up. Also, Google Ads weren’t active last month, so we missed out on potential new customers there.

Looking ahead, our top priorities are: submitting new, seasonal content for Instagram to keep that growth going; relaunching Google Ads to drive at least 150 clicks; and updating Facebook ad visuals and copy to boost engagement. Let’s also keep sharing customer stories and reviews to connect with our community.

In summary, we’re making strong progress, especially on Instagram, but we need to act quickly on ad updates and Google campaigns to keep the momentum. Thanks for your hard work, and let’s keep pushing for even better results this month!
"""


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
