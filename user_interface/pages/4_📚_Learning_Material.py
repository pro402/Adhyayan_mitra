import streamlit as st
import os
from components.transcript_gen import transcript
from components.audio_gen import kokoro_tts
from components.revision_tools import summary
from components.revision_tools import key_vocab
from components.revision_tools import ex_questions

def learning_material():
    # Check prerequisites
    required_vars = ['evaluation_report', 'qa_pairs', 'gap_analysis', 
                    'doc_result', 'trans_result', 'llm', 'provider']
    if not all(var in st.session_state and st.session_state[var] for var in required_vars):
        st.error("Complete previous steps first!")
        st.page_link("pages/3_📈_Final_Analysis.py", label="← Return to Final Analysis", icon="📈")
        st.stop()

    st.title("📚 Personalized Learning Material")

    # --- INFO: Use case and features ---
    st.info(
        """
        **What is this page for?**
        
        This tool generates personalized learning materials based on your study session and performance analysis. 
        It helps you revise, reinforce, and practice the concepts you need most.
        
        **Features:**
        - 🔊 **Audio Explainer:** Listen to a summary of your learning material, tailored to your needs.
        - 📄 **Summary Notes:** Review concise, AI-generated notes focusing on your strengths and weaknesses.
        - ❓ **Supplementary Questions:** Practice with targeted questions based on your learning gaps.
        - 📚 **Key Vocabulary:** Revise essential terms and definitions central to your topic.
        
        Use these tools for effective revision, self-testing, and to strengthen your understanding before exams!
        """
    )

    # --- Audio Explainer Section ---
    st.subheader("🔊 Audio Explainer")
    if 'tts' not in st.session_state:
        st.session_state.tts = kokoro_tts.Kokoro_TTS(
            audio_chunk_dir=os.path.join(os.path.dirname(__file__), "audio_chunks")
        )
    col1, col2 = st.columns([1, 1])
    with col1:
        voice = st.selectbox(
            "🗣️ Select Voice",
            options=["af_heart", "am_adam", "am_emma"],
            index=0,
            help="Choose voice personality for audio material"
        )
    with col2:
        lang_code = st.selectbox(
            "🌐 Select Language",
            options=[("English (US)", "a"), ("Hindi", "h"), ("Spanish", "e")],
            format_func=lambda x: x[0],
            index=0
        )[1]
    if st.button("Generate Audio Explanation", key="audio_explainer_btn"):
        if 'learning_transcript' not in st.session_state:
            with st.spinner("Generating transcript for audio explainer..."):
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
        try:
            with st.spinner("Synthesizing audio content..."):
                audio_path = st.session_state.tts.generate_audio(
                    text=st.session_state.learning_transcript,
                    output_path="learning_material.mp3",
                    voice=voice,
                    lang_code=lang_code
                )
                st.session_state.audio_path = audio_path
                st.toast("Audio explanation ready!", icon="🎧")
        except Exception as e:
            st.error(f"Audio generation failed: {str(e)}")
            st.stop()
    if 'audio_path' in st.session_state and os.path.exists(st.session_state.audio_path):
        st.audio(st.session_state.audio_path)
        st.download_button(
            "📥 Download Audio Explanation",
            data=open(st.session_state.audio_path, "rb").read(),
            file_name="french_revolution_explanation.mp3",
            mime="audio/mpeg",
            use_container_width=True
        )

    # --- Summary Notes Section ---
    st.subheader("📄 Summary Notes")
    if st.button("Generate Summary Notes", key="summary_btn"):
        with st.spinner("Generating summary notes..."):
            st.session_state.summary_notes = summary.get_summary_notes(
                llm=st.session_state.llm,
                provider=st.session_state.provider,
                evaluation_report=st.session_state.evaluation_report,
                qna=st.session_state.qa_pairs,
                analysis=st.session_state.gap_analysis,
                doc_result=st.session_state.doc_result,
                trans_result=st.session_state.trans_result 
            )
    if 'summary_notes' in st.session_state:
        with st.expander("View Summary Notes", expanded=False):
            st.markdown(st.session_state.summary_notes)
        st.download_button(
            "📥 Download Summary Notes",
            data=st.session_state.summary_notes,
            file_name="french_revolution_summary.md",
            mime="text/markdown",
            use_container_width=True
        )

    # --- Supplementary Questions Section ---
    st.subheader("❓ Supplementary Questions")
    if st.button("Generate Supplementary Questions", key="supp_qa_btn"):
        with st.spinner("Generating supplementary questions..."):
            st.session_state.qs_pairs = ex_questions.supplementary_qa_gen(
                llm=st.session_state.llm,
                provider=st.session_state.provider,
                evaluation_report=st.session_state.evaluation_report,
                qna=st.session_state.qa_pairs,
                analysis=st.session_state.gap_analysis,
                doc_result=st.session_state.doc_result,
                trans_result=st.session_state.trans_result
            )
    if 'qs_pairs' in st.session_state:
        with st.expander("Practice Questions", expanded=False):
            for i, pair in enumerate(st.session_state.qs_pairs):
                st.markdown(f"**Q{i+1}: {pair['question']}**")
                st.divider()
        def format_qa_for_download(qs_pairs):
            return "\n\n".join([f"Q{i+1}: {pair['question']}\nA{i+1}: {pair['answer']}" for i, pair in enumerate(qs_pairs)])
        st.download_button(
            "📥 Download Questions & Answers",
            data=format_qa_for_download(st.session_state.qs_pairs),
            file_name="french_revolution_questions_answers.txt",
            mime="text/plain",
            use_container_width=True
        )

    # --- Key Vocabulary Section ---
    st.subheader("📚 Key Vocabulary")
    if st.button("Generate Key Vocabulary", key="vocab_btn"):
        with st.spinner("Generating key vocabulary..."):
            st.session_state.vocab = key_vocab.get_key_vocab(
                llm=st.session_state.llm,
                provider=st.session_state.provider,
                evaluation_report=st.session_state.evaluation_report,
                qna=st.session_state.qa_pairs,
                analysis=st.session_state.gap_analysis,
                doc_result=st.session_state.doc_result,
                trans_result=st.session_state.trans_result
            )
    if 'vocab' in st.session_state:
        with st.expander("Important Terms and Concepts", expanded=False):
            st.markdown(st.session_state.vocab)

    # Final completion
    st.success("🎉 Learning Journey Complete!")
    st.page_link("Home.py", label="Restart Learning Session →", icon="🔄")

learning_material()
