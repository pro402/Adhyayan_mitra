import os
import sys
import streamlit as st
import tempfile
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import other components but skip the audio recorder that's causing issues
from components.sTT_model.whisper_tiny import AudioTranscriptor
from components.select_llm import google_genai, ollama, llama_cpp, built_in
from components.doc_pipeline.pipeline import DocumentProcessor
from components.question_generator.questions import QuestionGenerator
from components.gap_analyzer.analyzer import GapAnalyzer
from components.qna_judge.judge import QnAJudge

# Set page configuration
st.set_page_config(
    page_title="Adhyayan Mitra",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1rem;
    }
    .info-text {
        font-size: 1rem;
        color: #616161;
    }
    .highlight {
        background-color: #f0f7ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='main-header'>Adhyayan Mitra</h1>", unsafe_allow_html=True)
    st.markdown("<p class='info-text'>Your AI-powered learning assistant</p>", unsafe_allow_html=True)
    
    # Initialize session state variables if they don't exist
    if 'audio_file' not in st.session_state:
        st.session_state.audio_file = None
    if 'transcript' not in st.session_state:
        st.session_state.transcript = None
    if 'document' not in st.session_state:
        st.session_state.document = None
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'gaps' not in st.session_state:
        st.session_state.gaps = []
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    
    # Sidebar for navigation and settings
    with st.sidebar:
        st.markdown("<h2>Settings</h2>", unsafe_allow_html=True)
        
        # LLM Selection
        st.markdown("<h3>Select LLM</h3>", unsafe_allow_html=True)
        llm_option = st.selectbox(
            "Choose a language model:",
            ["Google Gemini", "Ollama", "Llama.cpp", "Built-in"]
        )
        
        # API Key input for Google Gemini
        if llm_option == "Google Gemini":
            api_key = st.text_input("Enter Google API Key:", type="password")
        
        # Reset button
        if st.button("Reset Session"):
            st.session_state.audio_file = None
            st.session_state.transcript = None
            st.session_state.document = None
            st.session_state.questions = []
            st.session_state.answers = []
            st.session_state.gaps = []
            st.session_state.feedback = None
            st.experimental_rerun()
    
    # Main content area
    st.markdown("<h2 class='sub-header'>Record or Upload Audio</h2>", unsafe_allow_html=True)
    
    # Use Streamlit's built-in audio recorder instead of custom recorder
    audio_bytes = st.audio_input("Record your voice")
    
    if audio_bytes:
        # Save the recorded audio to a temporary file
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_audio_file.write(audio_bytes)
        temp_audio_file.close()
        
        st.session_state.audio_file = temp_audio_file.name
        st.success(f"Audio recorded successfully! File saved as {temp_audio_file.name}")
    
    # Or allow file upload
    uploaded_file = st.file_uploader("Or upload an audio file", type=["wav", "mp3", "m4a"])
    if uploaded_file:
        # Save the uploaded file to a temporary location
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}")
        temp_audio_file.write(uploaded_file.getvalue())
        temp_audio_file.close()
        
        st.session_state.audio_file = temp_audio_file.name
        st.success(f"Audio file uploaded successfully! File saved as {temp_audio_file.name}")
    
    # Transcribe audio if available
    if st.session_state.audio_file and st.button("Transcribe Audio"):
        with st.spinner("Transcribing audio..."):
            try:
                transcriptor = AudioTranscriptor()
                st.session_state.transcript = transcriptor.transcribe(st.session_state.audio_file)
                st.success("Audio transcribed successfully!")
            except Exception as e:
                st.error(f"Error transcribing audio: {str(e)}")
    
    # Display transcript if available
    if st.session_state.transcript:
        st.markdown("<h2 class='sub-header'>Transcript</h2>", unsafe_allow_html=True)
        st.markdown(f"<div class='highlight'>{st.session_state.transcript}</div>", unsafe_allow_html=True)
        
        # Process document
        if st.button("Process Document"):
            with st.spinner("Processing document..."):
                try:
                    # Select LLM based on user choice
                    if llm_option == "Google Gemini":
                        llm = google_genai.GoogleGenAI(api_key)
                    elif llm_option == "Ollama":
                        llm = ollama.Ollama()
                    elif llm_option == "Llama.cpp":
                        llm = llama_cpp.LlamaCpp()
                    else:
                        llm = built_in.BuiltIn()
                    
                    # Process document
                    processor = DocumentProcessor(llm)
                    st.session_state.document = processor.process(st.session_state.transcript)
                    
                    # Generate questions
                    question_generator = QuestionGenerator(llm)
                    st.session_state.questions = question_generator.generate(st.session_state.document)
                    
                    st.success("Document processed and questions generated successfully!")
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")
    
    # Display navigation to other pages
    st.markdown("<h2 class='sub-header'>Next Steps</h2>", unsafe_allow_html=True)
    st.markdown("""
    1. Go to the **QA** page to answer questions about your document
    2. Check the **GAP Analysis** page to identify knowledge gaps
    3. View the **Final Analysis** page for comprehensive feedback
    """)

if __name__ == "__main__":
    main()
