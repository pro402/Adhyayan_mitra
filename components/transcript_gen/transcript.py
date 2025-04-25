# Using evaluation_report + qna + GAP_Analysis + Doc_result + transcript 
# -> to Genenrate a Audio Which discusses topics that can help student learn from hearing them
# -> The Generated transcript will be in text format(not any markdown or any special symbols)
import re
from langchain.prompts import PromptTemplate

def get_transcript(
    llm,
    provider,
    evaluation_report,
    qna,
    analysis,
    doc_result,
    trans_result
):

    transcript_prompt = PromptTemplate.from_template(
        """
        You are an expert Teaching Assistant dedicated to helping students deeply understand their subject matter.
        Your goal is to create a comprehensive, engaging, and easy-to-follow transcript designed to be read aloud as an educational audio resource.

        Use the provided evaluation report, QnA, gap analysis, document result, and any previous transcripts to:
        - Identify and clearly explain key concepts, especially those where the student has shown misunderstandings or gaps.
        - Address misconceptions directly, using simple language and relatable examples.
        - Reinforce correct knowledge and expand on important points with additional context or analogies.
        - Encourage curiosity and active learning by posing thought-provoking questions or prompts for reflection.
        - Ensure the transcript flows logically and naturally, as if you are speaking directly to the student in a friendly, supportive manner.
        - Avoid technical jargon unless it is explained clearly.
        - Keep the tone warm, encouraging, and positive to boost student motivation and confidence.

        Important:
        - The transcript should be detailed, well-structured, and suitable for listening.
        - Do not use any markdown, bullet points, or special symbols—write in plain, natural text as it would be spoken.
        - Focus on clarity, engagement, and actionable learning.

        Here is the evaluation report:
        {evaluation_report}
        Here is the QnA:
        {qna}
        Here is the GAP Analysis:
        {analysis}
        Here is the Document Result:
        {doc_result}
        Here is the Previous Transcript:
        {trans_result}

        Now, generate a detailed and engaging transcript that helps the student understand the material, corrects their misconceptions, fills their knowledge gaps, and motivates them to keep learning.
        """
    )

    chain = transcript_prompt | llm
    transcript = chain.invoke({
        "evaluation_report":evaluation_report,
        "qna":qna,
        "analysis":analysis,
        "doc_result":doc_result,
        "trans_result":trans_result
        }
    )

    if provider == "google_genai":
        transcript = transcript.content    
    elif provider == "llama_cpp":
        transcript = transcript
    elif provider == "ollama":
        transcript = transcript

    transcript = re.sub(r'[^a-zA-Z0-9\s()+-,.?!$%&\'"]', '', transcript)    
    
    return transcript