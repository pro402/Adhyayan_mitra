import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
google_api = os.getenv("GOOGLE_API")

def set_llm(
        model: str = "gemma-3-27b-it",
):
    """
    Set the LLM to use based on user input.
    Args:
        model (str): The model to use. Default is "gemma-3-27b-it".
        Choose model from https://aistudio.google.com
    Returns:
        llm: The selected LLM.
    """
    llm = ChatGoogleGenerativeAI(
        model=model,
        temperature=0,
        max_tokens=8192,
        api_key = google_api,
    )
    return [llm, model,"google_genai"]