import streamlit as st
from components.qna_judge import judge

def final_analysis():
    # Check prerequisites
    required_vars = ['llm', 'provider', 'doc_result', 'trans_result', 'gap_analysis', 'qa_pairs']
    if not all(var in st.session_state and st.session_state[var] for var in required_vars):
        st.error("Complete Q&A session first!")
        st.page_link("pages/2_❓_QA.py", label="← Return to Q&A", icon="❓")
        st.stop()

    st.title("📈 Final Performance Evaluation")

    # Generate QNA string from pairs
    qna_content = "\n".join(
        [f"Q{i+1}. {pair['question']}\nAns: {pair['answer']}\n" 
         for i, pair in enumerate(st.session_state.qa_pairs)]
    )

    # Initialize evaluation report
    if 'evaluation_report' not in st.session_state:
        st.session_state.evaluation_report = None

    if st.button("🔄 Generate Comprehensive Evaluation"):
        try:
            with st.spinner("Conducting in-depth analysis..."):
                evaluation = judge.qna_check_and_scoring(
                    llm=st.session_state.llm,
                    provider=st.session_state.provider,
                    doc_result=st.session_state.doc_result,
                    trans_result=st.session_state.trans_result,
                    analysis=st.session_state.gap_analysis,
                    qna=qna_content
                )
                
                st.session_state.evaluation_report = evaluation
                
                st.success("Evaluation completed!")
                
                # Unlock next section
                st.session_state.unlocked_pages['Learning_Material'] = True
                st.toast("✅ Learning Materials unlocked!", icon="📚")

        except Exception as e:
            st.error(f"Evaluation failed: {str(e)}")
            st.stop()

    # Display evaluation report
    if st.session_state.evaluation_report:
        st.subheader("📊 Detailed Assessment Report")
        
        # Formatted markdown display
        with st.expander("View Full Evaluation Report", expanded=True):
            st.markdown(st.session_state.evaluation_report, unsafe_allow_html=False)
        
        # Download button
        st.download_button(
            "📥 Download Evaluation Report",
            data=st.session_state.evaluation_report,
            file_name="performance_evaluation.md",
            mime="text/markdown",
            help="Download complete evaluation in markdown format",
            use_container_width=True
        )

        # Progress to next section
        if st.session_state.unlocked_pages['Learning_Material']:
            st.page_link("pages/4_📚_Learning_Material.py", 
                        label="Proceed to Learning Materials →",
                        icon="📚")

final_analysis()