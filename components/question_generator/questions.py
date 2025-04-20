from langchain.prompts import PromptTemplate
import re

def extract_python_list(text):
    # Find content between square brackets
    match = re.search(r'\[(.*?)\]', text, re.DOTALL)
    if not match:
        return None
    
    # Get the content and split by commas followed by newlines
    content = match.group(1).strip()
    items = re.findall(r'"(.*?)"', content)
    
    return items

def question_gen(llm, doc_result, trans_result, analysis):
  question_gen_prompt = PromptTemplate.from_template(
      """
      You are a Teaching Assistant responsible for generating a set of descriptive, open-ended questions based on a student's response to course material. Your questions should assess understanding and encourage critical thinking.

      STEPS:
      1. Carefully review the STUDENT'S RESPONSE/KNOWLEDGE (from transcript) and compare it against the LEARNING MATERIAL and the LEARNING GAP ANALYSIS.
      2. Identify any topics the student did not explain properly, any skipped concepts, or misunderstandings highlighted in the gap analysis.
      3. Formulate questions that directly target these missing explanations or omitted topics to probe deeper understanding.
      4. Also include questions that revisit core concepts from the material that were not fully addressed in the transcript.

      LEARNING MATERIAL:
      {doc1}

      STUDENT'S RESPONSE/KNOWLEDGE (from transcript):
      {doc2}

      LEARNING GAP ANALYSIS:
      {doc3}

      Instructions:
      - Generate between 7 to 10 descriptive, open-ended questions.
      - Each question must focus on an identified gap: missing explanations, skipped topics, or misunderstandings.
      - Ensure every question probes deeper into the student’s comprehension and addresses specific gaps found in the transcript.
      - Present the questions as a Python list of strings, for example:
        [
            "Describe how...",
            "Explain why...",
            "What would happen if...",
            "Compare...",
            "Discuss the significance of...",
            "How does... relate to...",
            "In what ways..."
        ]
      """
  )

  chain = question_gen_prompt | llm
  questions = chain.invoke({"doc1": doc_result, "doc2":trans_result, "doc3": analysis})

  if llm.model == "models/gemma-3-27b-it":
      return extract_python_list(questions.content)
  else:
      return extract_python_list(questions)
