import streamlit as st
from components.gap_analyzer import analyzer

def gap_analysis():
    # Check prerequisites
    required_vars = ['llm', 'provider', 'doc_result', 'trans_result']
    if not all(var in st.session_state and st.session_state[var] for var in required_vars):
        st.error("Complete previous steps first: Need LLM setup, documents processed, and transcript generated")
        st.page_link("Home.py", label="← Return to Home", icon="🏠")
        st.stop()

    st.title("📊 Learning Gap Analysis")

    # Only compute analysis if not already done or if user requests regeneration
    regenerate = st.button("🔄 Regenerate GAP Analysis")
    if 'gap_analysis' not in st.session_state or st.session_state.gap_analysis is None or regenerate:
        with st.spinner("Analyzing learning gaps..."):
            try:
                analysis = analyzer.learning_gap(
                    llm=st.session_state.llm,
                    provider=st.session_state.provider,
                    doc_result=st.session_state.doc_result,
                    trans_result=st.session_state.trans_result
                )
                st.session_state.gap_analysis = analysis
                st.success("GAP Analysis completed!")
            except Exception as e:
                st.error(f"Gap analysis failed: {str(e)}")
                st.stop()

    # Display formatted analysis
    st.subheader("🔍 Identified Learning Gaps")
    st.markdown(st.session_state.gap_analysis, unsafe_allow_html=True)
    
    # Download button with original analysis
    st.download_button(
        "📥 Download Analysis Report",
        data=st.session_state.gap_analysis,
        file_name="learning_gaps.md",
        mime="text/markdown",
        help="Download the full gap analysis report in Markdown format",
        use_container_width=True
    )

    # Automatically unlock next section when analysis completes
    if st.session_state.gap_analysis and not st.session_state.unlocked_pages['QA']:
        st.session_state.unlocked_pages['QA'] = True
        st.toast("✅ Q&A section unlocked! Check sidebar to proceed.", icon="❓")

gap_analysis()
