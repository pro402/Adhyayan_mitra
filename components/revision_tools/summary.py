import re
from langchain.prompts import PromptTemplate

def get_summary_notes(
    llm,
    provider,
    evaluation_report,
    qna,
    analysis,
    doc_result,
    trans_result
):

    summary_prompt = PromptTemplate.from_template(
        """
        You are an expert educational content creator specializing in creating concise, targeted study notes.
        
        Create comprehensive summary notes for the student based on their learning assessment. These notes should:
        
        1. Focus primarily on concepts where the student showed knowledge gaps or misconceptions
        2. Present key information in a clear, structured format with proper headings and subheadings
        3. Highlight important vocabulary terms and concepts in bold
        4. Provide correct explanations for questions the student attempted, with special attention to areas of confusion
        5. Include concise explanations of fundamental concepts that support understanding
        6. Use examples, analogies, or visual descriptions where appropriate
        7. Organize information in a logical learning sequence
        
        FORMAT REQUIREMENTS:
        - Use clear headings (## for main sections, ### for subsections)
        - Bold key terms and important concepts using **asterisks**
        - Use numbered lists for sequential information or steps
        - Use bullet points for related but non-sequential items
        - Include a "Common Misconceptions" section addressing specific errors
        - Create a "Key Questions & Answers" section with correct responses
        
        ASSESSMENT MATERIALS:
        Evaluation Report: {evaluation_report}
        Student Q&A Attempts: {qna}
        Knowledge Gap Analysis: {analysis}
        Reference Materials: {doc_result}
        Student's Original Explanation: {trans_result}
        
        Create targeted study notes that will help this student master the concepts they're struggling with while reinforcing their existing knowledge.
        """
    )

    chain = summary_prompt | llm
    summary_note = chain.invoke({
        "evaluation_report": evaluation_report,
        "qna": qna,
        "analysis": analysis,
        "doc_result": doc_result,
        "trans_result": trans_result
        }
    )

    if provider == "google_genai":
        summary_note = summary_note.content    
    elif provider == "llama_cpp":
        summary_note = summary_note
    elif provider == "ollama":
        summary_note = summary_note

    summary_note = re.sub(r'[^a-zA-Z0-9\s()+-,.?!$%&\'"]', '', summary_note)    
    
    return summary_note