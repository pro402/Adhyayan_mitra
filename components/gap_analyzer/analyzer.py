from langchain_core.prompts import PromptTemplate

def learning_gap(llm,doc_result, trans_result):
    
    learning_gap_analysis_prompt = PromptTemplate.from_template(
        """
        You are a Teaching Assistant responsible for providing detailed feedback on a student's understanding of course material. Your goal is to help the instructor identify knowledge gaps and provide constructive guidance to the student.
        
        COURSE LEARNING MATERIAL:
        {doc1}
        
        STUDENT'S RESPONSE/KNOWLEDGE (from transcript):
        {doc2}
        
        As a TA, provide a comprehensive learning gap analysis that includes:
        
        1. DEMONSTRATED KNOWLEDGE: Identify specific concepts from the learning material that the student clearly understands, with direct examples from their response.
        
        2. KNOWLEDGE GAPS: List important concepts or topics from the learning material that are missing or inadequately addressed in the student's response. Be specific about which key points were overlooked.
        
        3. MISCONCEPTIONS: Highlight any errors or misconceptions in the student's understanding, explaining the correct concept alongside each misconception.
        
        4. DEPTH OF UNDERSTANDING: Assess whether the student demonstrates surface-level knowledge or deeper conceptual understanding. Identify areas where their understanding lacks depth.
        
        5. LEARNING PRIORITIES: Rank the identified gaps in order of importance for the student's academic progress.
        
        6. TARGETED RECOMMENDATIONS: Suggest specific study activities, practice exercises, or supplementary resources to address each identified gap.      

        Your analysis should be detailed and precise, referencing specific content from both the learning material and student response. Focus on actionable insights that will help both the instructor guide the student and the student improve their understanding.
        """
    )

    chain = learning_gap_analysis_prompt | llm 
    analysis = chain.invoke({"doc1": doc_result, "doc2": trans_result})    
    if llm.model in ["models/gemma-3-27b-it","models/gemini-2.0-flash-lite"]:
        return analysis.content
    else:
        return analysis