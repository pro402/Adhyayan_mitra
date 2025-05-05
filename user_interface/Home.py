import streamlit as st
import sys
import os
import librosa
from datetime import timedelta
import tempfile
from audio_recorder_streamlit import audio_recorder

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.sTT_model.whisper_tiny import AudioTranscriptor
from components.select_llm import google_genai, ollama, llama_cpp, build_nvidia
from components.doc_pipeline.pipeline import DocumentProcessor

# --- Session State Initialization ---
if 'unlocked_pages' not in st.session_state:
    st.session_state.unlocked_pages = {
        'GAP_Analysis': False,
        'QA': False,
        'Final_Analysis': False,
        'Learning_Material': False
    }

session_vars = [
    'file_path', 'duration', 'llm', 'model', 
    'provider', 'doc_result', 'trans_result'
]
for var in session_vars:
    if var not in st.session_state:
        st.session_state[var] = None

def valid_audio_file(file_path):
    """Validate audio file existence and content"""
    return file_path and os.path.exists(file_path) and librosa.get_duration(path=file_path) > 0

st.set_page_config(page_title="Adhyayan Mitra", page_icon="🎓", layout="wide")

# --- Main Header ---
with st.container():
    st.title("Adhyayan Mitra - AI Learning Companion")
    with st.expander("📘 How It Works"):
        st.markdown("""
        **Welcome to your personalized learning journey!**  
        This system helps you:
        - 🎧 Record or upload and transcribe learning sessions
        - 📝 Analyze knowledge gaps
        - ❓ Generate practice questions
        - 📚 Create study resources
        
        1. **Record or upload** your learning session  
        2. **Transcribe** to text for analysis  
        3. **Select** an AI model for processing  
        4. **Upload** study materials for enhanced analysis  
        5. **Receive** personalized feedback and resources
        """)

# --- Topic Information Header ---
st.markdown("""
<div style="padding: 10px; border-radius: 5px; margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h2 style="color: #1e3a8a; margin-bottom: 5px;">The Rise of Nationalism in Europe</h2>
            <p style="color: #6b7280; margin-top: 0;">Class 10 • NCERT History</p>
        </div>
        <div>
            <p style="color: #3b82f6; text-align: right;">Ready to learn? Let's get started!</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Audio Input Section (Record or Upload) ---
with st.container():
    st.header("🎤 Learning Session: Record or Upload Audio")
    st.info("""
    **What to record:** Please record yourself explaining the key events, causes, and impacts of the French Revolution based on your understanding.

    **Purpose:** Your recording helps assess your comprehension of the historical events and concepts related to the French Revolution.
    """)
    
    audio_mode = st.radio(
        "Choose how you'd like to provide audio:",
        ("Upload an audio file", "Record with microphone"),
        horizontal=True,
        help="Record directly or upload an existing audio file (WAV/MP3/M4A/OGG)."
    )

    if audio_mode == "Record with microphone":
        col1, col2 = st.columns([1,2])
        with col1:
            st.caption("Recording will automatically stop after 5s of pause, or click the mic to stop recording.")
            audio_bytes = audio_recorder(
                text="⏺️ Click to record",
                recording_color="#e8b62c",
                neutral_color="#6aa36f",
                icon_size="2x",
                pause_threshold=5.0,
            )
            if audio_bytes:
                st.toast("🎙️ Recording started")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(audio_bytes)
                    st.session_state.file_path = tmp_file.name
                if valid_audio_file(st.session_state.file_path):
                    st.session_state.duration = librosa.get_duration(path=st.session_state.file_path)
                    st.toast(f"✅ Recording saved ({timedelta(seconds=int(st.session_state.duration))})")
                else:
                    st.error("⚠️ Please Retry.")
        with col2:
            if valid_audio_file(st.session_state.file_path):
                st.audio(st.session_state.file_path)
                st.caption(f"⏱️ Audio duration: {st.session_state.duration:.2f} seconds")
    else:  # Upload an audio file
        st.caption("Upload a recording of yourself explaining the French Revolution")
        uploaded_audio = st.file_uploader(
            "Upload your audio file (wav, mp3, m4a, ogg)",
            type=['wav', 'mp3', 'm4a', 'ogg'],
            help="Upload a pre-recorded audio file."
        )
        if uploaded_audio:
            temp_audio_path = None
            try:
                file_extension = os.path.splitext(uploaded_audio.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                    tmp_file.write(uploaded_audio.getvalue())
                    temp_audio_path = tmp_file.name
                if valid_audio_file(temp_audio_path):
                    st.session_state.file_path = temp_audio_path
                    st.session_state.duration = librosa.get_duration(path=temp_audio_path)
                    st.audio(temp_audio_path)
                    st.caption(f"⏱️ Audio duration: {st.session_state.duration:.2f} seconds")
                    st.toast("✅ Audio uploaded and ready!", icon="🎧")
                else:
                    st.error("⚠️ Uploaded file is not a valid audio file.")
            except Exception as e:
                st.error(f"❌ Error processing uploaded audio: {str(e)}")

# --- Transcription Section ---
with st.container():
    st.header("📝 Transcription & Analysis")
    st.info("""
    **What happens here:** Your explanation of the French Revolution will be converted to text for analysis, If edited make sure to Update the Transcript.

    **Purpose:** This text version allows the AI to evaluate your understanding of key historical events and concepts.
    """)
    trans_col1, trans_col2 = st.columns([3,1])
    with trans_col1:
        if st.button("✨ Generate Transcript", 
                    disabled=not valid_audio_file(st.session_state.file_path),
                    help="Convert audio to text for analysis"):
            if st.session_state.duration < 30:
                st.warning(f"⚠️ Minimum 30 seconds required (Current: {st.session_state.duration:.2f}s)")
            else:
                try:
                    with st.spinner("🔍 Analyzing content..."):
                        transcriptor = AudioTranscriptor()
                        st.session_state.trans_result = transcriptor.whisper_transcribe(
                            st.session_state.file_path
                        )
                    st.toast("Transcript generated!", icon="✅")
                except Exception as e:
                    st.error(f"❌ Transcription failed: {str(e)}")

        # Editable transcript area and update button
        if st.session_state.trans_result:
            st.subheader("📄 Learning Session Transcript")
            edited_transcript = st.text_area(
                "Edit Transcript:",
                value=st.session_state.trans_result,
                height=250,
                key="transcript_editor",
                help="Make any corrections to the transcript"
            )
            col_upd, col_dl = st.columns([1, 3])
            with col_upd:
                if st.button("🔄 Update Transcript"):
                    st.session_state.trans_result = edited_transcript
                    st.toast("Transcript updated!", icon="📝")
            with col_dl:
                st.download_button(
                    label="💾 Download Transcript",
                    data=st.session_state.trans_result,
                    file_name="french_revolution_explanation.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# --- AI Model Selection ---
with st.container():
    st.header("🧠 AI Processing Setup")
    st.info("""
    **What to do:** Select an AI provider and model to analyze your explanation of the French Revolution.

    **Purpose:** The AI will compare your explanation with historical facts to assess your understanding.
    """)
    model_col1, model_col2 = st.columns(2)
    with model_col1:
        provider = st.selectbox(
            "🤖 Select AI Provider",
            ("Google GenAI","Build With NVIDIA", "Ollama", "Llama-CPP"),
            index=0,
            help="Choose your preferred AI engine"
        )
        if provider == "Google GenAI":
            model = st.selectbox(
                "🧠 Select Model",
                (
                    "gemini-2.0-flash", "gemini-2.0-flash-lite",
                    "gemini-2.5-pro-preview-03-25", "gemini-2.5-flash-preview-04-17",
                    "gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.5-flash-8b"
                ),
                index=0,
                help="Choose the model for Google GenAI"
            )
            st.caption("Note: Ensure you have a valid Google API key.")
            st.caption("Get your API key from https://aistudio.google.com")
            google_api = st.text_input("🔑 Google API Key", type="password", help="Get your API key from https://aistudio.google.com")
            if google_api:
                try:
                    llm_config = google_genai.set_llm(model=model, google_api=google_api)
                    st.session_state.update({
                        'llm': llm_config[0],
                        'model': llm_config[1],
                        'provider': llm_config[2],
                    })
                    st.success("✅ Google GenAI authenticated successfully")
                except Exception as e:
                    st.error(f"❌ Authentication failed: {str(e)}")
        elif provider == "Build With NVIDIA":
            model = st.selectbox(
                "🧠 Select Model",
                (
                    "meta/llama-3.3-70b-instruct",
                    "deepseek-ai/deepseek-r1-distill-llama-8b",
                    "qwen/qwen-32b"
                ),
                index=0,
                help="Choose the NVIDIA AI Foundation model"
            )
            st.caption("Note: Ensure you have a valid NVIDIA API key.")
            st.caption("Get your API key from https://build.nvidia.com")
            nvidia_api_key = st.text_input("🔑 NVIDIA API Key", 
                                        type="password",
                                        help="API key starts with 'nvapi-'")
            if nvidia_api_key:
                try:
                    llm_config = build_nvidia.set_llm(
                        model=model, 
                        nvidia_api_key=nvidia_api_key
                    )
                    st.session_state.update({
                        'llm': llm_config[0],
                        'model': llm_config[1],
                        'provider': llm_config[2],
                    })
                    st.success("✅ NVIDIA AI authenticated successfully")
                except Exception as e:
                    st.error(f"❌ Authentication failed: {str(e)}")
        elif provider == "Ollama":
            llm_config = ollama.set_llm()
            st.session_state.update({
                'llm': llm_config[0],
                'model': llm_config[1],
                'provider': llm_config[2]
            })
        else:
            llm_config = llama_cpp.set_llm()
            st.session_state.update({
                'llm': llm_config[0],
                'model': llm_config[1],
                'provider': llm_config[2]
            })
    with model_col2:
        st.subheader("🔧 Active Configuration")
        st.metric("Selected Provider", provider)
        st.metric("Active Model", st.session_state.model)
        st.caption("Model parameters and settings")

# --- Document Processing ---
with st.container():
    st.header("📚 Study Material Analysis")
    st.info("""
    **What to upload:** Please upload your French Revolution study materials, textbook chapters, or class notes.

    **Purpose:** These materials serve as the reference against which your understanding will be evaluated.
    """)
    doc_col1, doc_col2 = st.columns([2,1])
    with doc_col1:
        uploaded_file = st.file_uploader("Upload French Revolution study materials (PDF/DOCX/MD)", 
                                       type=['pdf', 'docx', 'md'],
                                       help="Enhance analysis with course materials")
        if uploaded_file:
            temp_path = None
            try:
                with st.spinner("📖 Processing documents..."):
                    file_extension = os.path.splitext(uploaded_file.name)[1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        temp_path = tmp_file.name
                    processor = DocumentProcessor(
                        llm=st.session_state.llm,
                        provider=st.session_state.provider,
                    )
                    st.session_state.doc_result = processor.process_document(
                        file_path=temp_path
                    )
                st.success("✅ French Revolution materials processed successfully")
            except Exception as e:
                st.error(f"❌ Processing failed: {str(e)}")
            finally:
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)

    # Key Insights section immediately below header
    if st.session_state.doc_result:
        st.subheader("📌 Key Insights from French Revolution Materials")
        col_md, col_raw = st.columns([3, 1])
        with col_md:
            st.markdown(st.session_state.doc_result, unsafe_allow_html=True)
        with col_raw:
            with st.expander("📄 Raw Content"):
                st.code(st.session_state.doc_result, language="markdown")
        st.download_button(
            label="📥 Export French Revolution Insights",
            data=st.session_state.doc_result,
            file_name="french_revolution_insights.md",
            mime="text/markdown",
            use_container_width=True
        )

# --- Unlock Next Page ---
if (
    st.session_state.trans_result
    and st.session_state.doc_result
    and st.session_state.llm
):
    st.session_state.unlocked_pages['GAP_Analysis'] = True
    st.success("🎉 All steps completed! You can now proceed to analyze your understanding of the French Revolution.")
    if st.button("➡️ Continue to Knowledge Gap Analysis", use_container_width=True):
        st.switch_page("pages/1_📊_GAP_Analysis.py")

# --- System Status ---
with st.container():
    st.divider()
    status_cols = st.columns(3)
    with status_cols[0]:
        st.metric("Recording Status", "Ready for recording ⏺️")
    with status_cols[1]:
        st.metric("Last Session Duration", f"{st.session_state.duration:.2f}s" if st.session_state.duration else "N/A")
    with status_cols[2]:
        st.metric("AI Model Ready", "✅ Operational" if st.session_state.llm else "❌ Offline")
