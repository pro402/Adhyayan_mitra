from langchain.prompts import PromptTemplate
import re
import ast

def extract_qa_string_list(text):
    """
    Extracts a Python list of Q|A strings from the LLM's output string.
    """
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if not match:
        return []
    content = match.group(0)
    try:
        qa_list = ast.literal_eval(content)
        if isinstance(qa_list, list) and all(isinstance(item, str) for item in qa_list):
            return qa_list
    except Exception:
        pass
    return []

def parse_qa_string(qa_str):
    """
    Splits a string of format 'Q: ... | A: ...' into a dict.
    """
    parts = qa_str.split('|')
    if len(parts) == 2:
        q = parts[0].replace('Q:', '').strip()
        a = parts[1].replace('A:', '').strip()
        return {'question': q, 'answer': a}
    return None

def supplementary_qa_gen(
    llm,
    provider,
    evaluation_report,
    qna,
    analysis,
    doc_result,
    trans_result
):
    prompt = PromptTemplate.from_template(
        """
        You are a Teaching Assistant. Your task is to generate a set of 7-8 open-ended, descriptive supplementary questions WITH their correct answers, based on the following materials:

        - Evaluation Report: {evaluation_report}
        - Student Q&A Attempts: {qna}
        - Knowledge Gap Analysis: {analysis}
        - Reference Materials: {doc_result}
        - Student's Own Explanation: {trans_result}

        Instructions:
        - Each question should address a specific gap, misconception, or missed topic from the student's work.
        - Each answer should be clear, concise, and factually correct, based on the provided materials.
        - Output ONLY a Python list of strings, each formatted as "Q: <question> | A: <answer>".

        Example:
        [
            "Q: What is the Napoleonic Code? | A: The Napoleonic Code was a legal code established by Napoleon that influenced many modern legal systems.",
            "Q: Explain the significance of the Bastille. | A: The storming of the Bastille marked the beginning of the French Revolution and symbolized the end of absolute monarchy."
        ]

        Do not include any other text, comments, or formatting.
        """
    )

    chain = prompt | llm
    result = chain.invoke({
        "evaluation_report": evaluation_report,
        "qna": qna,
        "analysis": analysis,
        "doc_result": doc_result,
        "trans_result": trans_result
    })

    if provider == "google_genai":
        output = result.content
    else:
        output = result

    qa_string_list = extract_qa_string_list(output)
    qa_pairs = [parse_qa_string(qas) for qas in qa_string_list if parse_qa_string(qas) is not None]
    return qa_pairs
