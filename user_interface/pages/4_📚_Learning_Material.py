import streamlit as st
import os
from components.transcript_gen import transcript
from components.audio_gen import kokoro_tts

def learning_material():
    # Check prerequisites
    required_vars = ['evaluation_report', 'qa_pairs', 'gap_analysis', 
                    'doc_result', 'trans_result', 'llm', 'provider']
    if not all(var in st.session_state and st.session_state[var] for var in required_vars):
        st.error("Complete previous steps first!")
        st.page_link("pages/3_📈_Final_Analysis.py", label="← Return to Final Analysis", icon="📈")
        st.stop()

    st.title("📚 Personalized Learning Material")
    
    # Initialize TTS engine
    if 'tts' not in st.session_state:
        st.session_state.tts = kokoro_tts.Kokoro_TTS(
            audio_chunk_dir=os.path.join(os.path.dirname(__file__), "audio_chunks")
        )

    # Generate transcript
    if 'learning_transcript' not in st.session_state:
        with st.spinner("Creating personalized learning content..."):
            try:
                qna_content = "\n".join(
                    [f"Q{i+1}. {pair['question']}\nAns: {pair['answer']}\n" 
                     for i, pair in enumerate(st.session_state.qa_pairs)]
                )
                
                st.session_state.learning_transcript = transcript.get_transcript(
                    llm=st.session_state.llm,
                    provider=st.session_state.provider,
                    evaluation_report=st.session_state.evaluation_report,
                    qna=qna_content,
                    analysis=st.session_state.gap_analysis,
                    doc_result=st.session_state.doc_result,
                    trans_result=st.session_state.trans_result
                )
                st.success("Learning material generated!")
            except Exception as e:
                st.error(f"Transcript generation failed: {str(e)}")
                st.stop()

    # Display transcript
    with st.expander("📄 View Learning Transcript", expanded=True):
        st.markdown(st.session_state.learning_transcript)

    # Audio generation controls
    col1, col2 = st.columns([1, 2])
    with col1:
        voice = st.selectbox(
            "🗣️ Select Voice",
            options=["af_heart", "am_adam", "am_emma"],
            index=0,
            help="Choose voice personality for audio material"
        )
        lang_code = st.selectbox(
            "🌐 Select Language",
            options=[("English (US)", "a"), ("Hindi", "h"), ("Spanish", "e")],
            format_func=lambda x: x[0],
            index=0
        )[1]

    with col2:
        if st.button("🔊 Generate Audio Material"):
            try:
                with st.spinner("Synthesizing audio content..."):
                    audio_path = st.session_state.tts.generate_audio(
                        text=st.session_state.learning_transcript,
                        output_path="learning_material.mp3",
                        voice=voice,
                        lang_code=lang_code
                    )
                    st.session_state.audio_path = audio_path
                    st.toast("Audio material ready!", icon="🎧")
            except Exception as e:
                st.error(f"Audio generation failed: {str(e)}")
                st.stop()

    # Audio player and download
    if 'audio_path' in st.session_state and os.path.exists(st.session_state.audio_path):
        st.subheader("🎧 Audio Learning Material")
        st.audio(st.session_state.audio_path)
        
        st.download_button(
            "📥 Download Audio",
            data=open(st.session_state.audio_path, "rb").read(),
            file_name="personalized_learning.mp3",
            mime="audio/mpeg",
            use_container_width=True
        )

    # Final completion
    st.success("🎉 Learning Journey Complete!")
    st.page_link("Home.py", label="Restart Learning Session →", icon="🔄")

learning_material()