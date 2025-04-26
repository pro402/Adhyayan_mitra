import streamlit as st
import re
from components.question_generator import questions
from langchain.prompts import PromptTemplate

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
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0

    # Question generation section
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
                        st.session_state.current_question = 0
                        st.rerun()
                    else:
                        st.error("Failed to generate questions. Please try again.")
            except Exception as e:
                st.error(f"Question generation failed: {str(e)}")

    # Question-Answer interface
    if st.session_state.questions:
        st.subheader(f"Question {st.session_state.current_question + 1}/{len(st.session_state.questions)}")
        
        # Display current question
        current_q = st.session_state.questions[st.session_state.current_question]
        st.markdown(f"**{current_q}**")
        
        # Answer input
        answer = st.text_area(
            "Your Answer:",
            value=st.session_state.answers[st.session_state.current_question],
            height=150,
            key=f"answer_{st.session_state.current_question}"
        )
        
        # Navigation controls
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.session_state.current_question > 0:
                if st.button("← Previous"):
                    st.session_state.current_question -= 1
                    st.rerun()
        with col2:
            if st.session_state.current_question < len(st.session_state.questions) - 1:
                if st.button("Next →") and answer.strip():
                    st.session_state.answers[st.session_state.current_question] = answer
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("✅ Submit All Answers"):
                    st.session_state.answers[st.session_state.current_question] = answer
                    st.session_state.qa_pairs = [
                        {"question": q, "answer": a} 
                        for q, a in zip(st.session_state.questions, st.session_state.answers)
                    ]
                    st.rerun()

    # Show completion and download
    if 'qa_pairs' in st.session_state:
        st.subheader("📝 Your Answers")
        
        # Format Q&A as markdown
        qna_md = ""
        for i, pair in enumerate(st.session_state.qa_pairs):
            qna_md += f"### Q{i+1}: {pair['question']}\n"
            qna_md += f"**Answer:** {pair['answer']}\n\n"
        
        # Display and download
        st.markdown(qna_md)
        
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