from langchain.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel # Assuming you use a ChatModel

def qna_check_and_scoring(llm: BaseChatModel, provider, doc_result: str, trans_result: str, analysis: str, qna: str) -> str:
    """
    Generates an expert evaluation of student Q&A based on provided materials.

    Args:
        llm: The language model instance.
        doc_result: The primary learning material content.
        trans_result: The student's prior knowledge or transcript.
        analysis: Previous gap analysis history.
        qna: The specific question(s) and the student's answer(s).

    Returns:
        A string containing the structured evaluation report.
    """
    answer_checker_prompt = PromptTemplate.from_template(
        """
    **Role**: You are an Expert Assessment Assistant specializing in Historical Analysis. Your task is to provide a rigorous, multi-dimensional evaluation of a student's response based on the provided materials.

    **Input Documents**:
    *   **LEARNING MATERIAL ({doc1_ref})**: {doc1}
    *   **STUDENT'S PRIOR KNOWLEDGE ({doc2_ref})**: {doc2}
    *   **GAP ANALYSIS HISTORY ({doc3_ref})**: {doc3}
    *   **QUESTION & ANSWER ({qna_ref})**: {question_answers}

    **Core Instruction**: Generate a structured evaluation report. The report **MUST** begin with the Total Score, followed immediately by a detailed Scoring Breakdown presented in a Markdown table. Adhere strictly to the output format specified below.

    **Required Output Format**:

    ## Student Performance Evaluation

    ### **Total Score**: [Awarded Score]/100

    ### **Scoring Breakdown**
    | Evaluation Category  | Max Points | Awarded Points | Justification Snippet / Rationale                                     |
    |----------------------|------------|----------------|-----------------------------------------------------------------------|
    | **Accuracy Check**   | 30         | [Score]        | [Brief rationale referencing factual alignment/chronology/precision]  |
    | **Depth Analysis**   | 25         | [Score]        | [Brief rationale referencing critical thinking/cause-effect/context]  |
    | **Completeness**     | 20         | [Score]        | [Brief rationale referencing coverage/required elements/perspectives] |
    | **Conceptual Clarity**| 15         | [Score]        | [Brief rationale referencing terminology/linkages/identifications]    |
    | **Critical Analysis**| 10         | [Score]        | [Brief rationale referencing insight/comparison/argumentation]      |
    | **TOTAL**            | **100**    | **[Total Score]**| **Overall Assessment Summary**                                          |

    *(Note: Fill in [Score] and [Total Score] with calculated values. Justification should be concise here, detailed elaboration follows below if needed.)*

    ---

    ### **Detailed Feedback**

    #### Strong Areas
    *   [Identify 1-3 specific points where the student excelled, quoting or referencing their answer and linking to LEARNING MATERIAL ({doc1_ref}) concepts. Example: "Excellent grasp of [Concept X] as evidenced by '[Student's relevant phrase]', aligning well with {doc1_ref} section Y."]

    #### Areas for Improvement & Gap Analysis
    *   **Factual Errors**:
        *   [List specific inaccuracies found in the student's answer ({qna_ref}). Provide the correction and reference the LEARNING MATERIAL ({doc1_ref}). Example: "Incorrectly stated [Event Z] occurred in [Year A]; it occurred in [Year B] (see {doc1_ref}, p. 5)."]
    *   **Conceptual Gaps**:
        *   [Identify specific theories, principles, or concepts from {doc1_ref} that were misunderstood or poorly explained in {qna_ref}. Example: "Misunderstood the concept of [Concept W], described in {doc1_ref} section Z."]
    *   **Omissions**:
        *   [List critical elements, perspectives, or details required by the question or present in {doc1_ref} that were missing from the student's answer ({qna_ref}). Example: "Failed to mention the significance of [Key Figure/Event] discussed in {doc1_ref}."]
    *   **Vague Assertions**:
        *   [Point out claims in {qna_ref} lacking specific evidence or support from {doc1_ref}. Example: "The statement '[Vague Student Claim]' needs substantiation, potentially using evidence from {doc1_ref} regarding [Topic V]."]

    ---

    ### **Misconception Analysis**
    | Identified Misconception (from {qna_ref}) | Relevant Material ({doc1_ref} Excerpt/Ref) | Correction / Clarification |
    |-------------------------------------------|--------------------------------------------|----------------------------|
    | [Student's specific error or misunderstanding] | [Relevant quote or page/section reference] | [Accurate explanation or context] |
    | ...                                       | ...                                        | ...                        |

    ---

    ### **Personalized Learning Path**

    #### 1. Immediate Focus Areas:
        *   [Priority 1: e.g., Review factual details of Event X]
        *   [Priority 2: e.g., Deepen understanding of Concept Y]
        *   [Priority 3: e.g., Practice structuring comparative arguments]

    #### 2. Resource Recommendations:
        *   **Primary Material Review**: Focus on [Specific section(s) or pages in {doc1_ref}] related to identified gaps.
        *   **Prior Knowledge Link**: Revisit [Specific concept in {doc2_ref}] and compare with {doc1_ref}.
        *   **Visual Aid**: Consider [Suggest relevant map, timeline, or diagram, potentially from {doc1_ref} or external].
        *   **Further Reading/Practice**: [Suggest specific exercises, related articles, or primary sources].

    #### 3. Skill-Building Exercises:
        *   **Accuracy Drill**: [e.g., Create a timeline of key events from {doc1_ref} section X].
        *   **Analysis Practice**: [e.g., Write a short paragraph explaining the cause-effect relationship between A and B, using {doc1_ref}].
        *   **Argumentation**: [e.g., Outline an argument comparing perspective C and D based on {doc1_ref}].

    ---

    ### **Detailed Rubric Application Notes**
    *(Elaborate on the scoring decisions made in the table above, providing specific examples from the student's answer ({qna_ref}) for each category.)*
    *   **Accuracy Check**: [Detailed reasoning for the awarded points, citing specific correct/incorrect statements from {qna_ref} vs {doc1_ref}].
    *   **Depth Analysis**: [Detailed reasoning, citing examples of critical thought or lack thereof in {qna_ref}].
    *   **Completeness**: [Detailed reasoning on coverage vs omissions in {qna_ref} based on question requirements and {doc1_ref}].
    *   **Conceptual Clarity**: [Detailed reasoning on terminology use and understanding shown in {qna_ref}].
    *   **Critical Analysis**: [Detailed reasoning on original insight, comparison quality, or argumentation structure in {qna_ref}].

    **End of Evaluation**
    """
    )

    # Add reference names for clarity in the prompt
    doc1_ref = "Learning Material"
    doc2_ref = "Prior Knowledge/Transcript"
    doc3_ref = "Gap Analysis"
    qna_ref = "Q&A"

    chain = answer_checker_prompt | llm
    judge = chain.invoke({
        "doc1": doc_result,
        "doc1_ref": doc1_ref,
        "doc2": trans_result,
        "doc2_ref": doc2_ref,
        "doc3": analysis,
        "doc3_ref": doc3_ref,
        "question_answers": qna,
        "qna_ref": qna_ref
    })

    # Assuming the LLM response is in the .content attribute for models like Gemma
    # Adjust this based on the specific Langchain LLM wrapper you use
    if provider == "google_genai":
        return judge.content
    elif provider == "llama_cpp":
        return judge
    elif provider == "ollama":
        return judge