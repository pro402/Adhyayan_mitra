import streamlit as st
from components.question_generator import questions

def qa_page():
    # Check prerequisites
    required_vars = ['llm', 'provider', 'doc_result', 'trans_result', 'gap_analysis']
    if not all(var in st.session_state and st.session_state[var] for var in required_vars):
        st.error("Complete previous steps first!")
        st.page_link("pages/1_📊_GAP_Analysis.py", label="← Return to GAP Analysis", icon="📊")
        st.stop()

    st.title("❓ Q&A Session")

    # Initialize session state variables
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'answers' not in st.session_state:
        st.session_state.answers = []

    # Generate questions if not already done
    if not st.session_state.questions:
        if st.button("✨ Generate Questions"):
            try:
                with st.spinner("Generating personalized questions..."):
                    generated_questions = questions.question_gen(
                        llm=st.session_state.llm,
                        provider=st.session_state.provider,
                        doc_result=st.session_state.doc_result,
                        trans_result=st.session_state.trans_result,
                        analysis=st.session_state.gap_analysis
                    )
                    if generated_questions:
                        st.session_state.questions = generated_questions
                        st.session_state.answers = [""] * len(generated_questions)
                        st.rerun()
                    else:
                        st.error("Failed to generate questions. Please try again.")
            except Exception as e:
                st.error(f"Question generation failed: {str(e)}")

    # Display all questions in a form
    if st.session_state.questions:
        with st.form(key="qa_form"):
            st.subheader("Please answer all questions below:")
            answer_inputs = []
            for idx, q in enumerate(st.session_state.questions):
                answer = st.text_area(
                    f"Q{idx+1}: {q}",
                    value=st.session_state.answers[idx] if len(st.session_state.answers) > idx else "",
                    height=100,
                    key=f"answer_{idx}"
                )
                answer_inputs.append(answer)
            submitted = st.form_submit_button("✅ Submit All Answers")

        if submitted:
            st.session_state.answers = answer_inputs
            st.session_state.qa_pairs = [
                {"question": q, "answer": a}
                for q, a in zip(st.session_state.questions, st.session_state.answers)
            ]
            st.success("Your answers have been submitted!")

    # Show completion and download
    if 'qa_pairs' in st.session_state:
        # st.subheader("📝 Your Answers")
        qna_md = ""
        for i, pair in enumerate(st.session_state.qa_pairs):
            qna_md += f"### Q{i+1}: {pair['question']}\n"
            qna_md += f"**Answer:** {pair['answer']}\n\n"
        # st.markdown(qna_md)
        st.download_button(
            "📥 Download Q&A Report",
            data=qna_md,
            file_name="learning_qa.md",
            mime="text/markdown",
            help="Download your questions and answers in markdown format"
        )
        # Unlock next section
        if not st.session_state.unlocked_pages['Final_Analysis']:
            st.session_state.unlocked_pages['Final_Analysis'] = True
            st.toast("✅ Final Analysis unlocked! Check sidebar to proceed.", icon="📈")

qa_page()