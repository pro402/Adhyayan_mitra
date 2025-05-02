import re
from langchain.prompts import PromptTemplate

def get_key_vocab(
    llm,
    provider,
    evaluation_report,
    qna,
    analysis,
    doc_result,
    trans_result
):
    vocab_prompt = PromptTemplate.from_template(
        """
        You are an educational content generator.
        Your task is to create a list of 10-15 key vocabulary terms essential for the student's understanding of the topic, focusing on:
        - Terms/concepts the student misunderstood or struggled with (from evaluation report, Q&A, gap analysis)
        - Fundamental and essential terms for mastering the topic
        - Important people, events, or places if relevant
        For each vocabulary word:
        - Write the word or phrase in bold markdown format (**Term**), followed by a colon and a clear, concise definition in plain English (1-2 sentences).
        - Output ONLY a Markdown unordered list, with each item on a new line in this format:
        - **Term**: Definition
        Do NOT include any introduction, explanation, or extra text. Only output the Markdown list.
        Materials for context:
        Evaluation Report: {evaluation_report}
        Student Q&A Attempts: {qna}
        Knowledge Gap Analysis: {analysis}
        Reference Materials: {doc_result}
        Student's Own Explanation: {trans_result}
        Example output:
        - **Revolution**: A major change in how a country is governed, often involving violence or war.
        - **Bastille**: A prison in Paris that was attacked at the start of the French Revolution.
        - **Ancien Regime**: The old system of government in France before the Revolution.
        """
    )
    chain = vocab_prompt | llm
    key_terms = chain.invoke({
        "evaluation_report": evaluation_report,
        "qna": qna,
        "analysis": analysis,
        "doc_result": doc_result,
        "trans_result": trans_result
    })
    
    if provider == "google_genai":
        key_terms = key_terms.content
    
    # Additional formatting to ensure the output matches the desired format
    # This will make sure terms are in bold format with proper list structure
    formatted_terms = key_terms.strip()
    
    # If the model didn't use proper markdown formatting, we can fix it
    if "**" not in formatted_terms:
        lines = formatted_terms.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip().startswith('- ') and ':' in line:
                term, definition = line.split(':', 1)
                term = term.strip()
                if term.startswith('- '):
                    term = term[2:]  # Remove the list marker
                formatted_line = f"- **{term.strip()}**: {definition.strip()}"
                formatted_lines.append(formatted_line)
            elif line.strip():  # If it's not empty
                formatted_lines.append(line)
        formatted_terms = '\n'.join(formatted_lines)
    
    return formatted_terms