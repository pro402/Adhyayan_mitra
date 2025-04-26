import os
from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# load_dotenv()

# google_api = os.getenv("GOOGLE_API_KEY")
# if google_api:
#     os.environ["GOOGLE_API_KEY"] = google_api

def set_llm(
    model: str = "gemini-2.0-flash",
    google_api: str = None
):
    """
    Set the LLM to use based on user input.
    Args:
        model (str): The model to use. Default is "gemini-2.0-flash".
        google_api (str): The API key to use.
    Returns:
        llm: The selected LLM.
    """
    if google_api:
        os.environ["GOOGLE_API_KEY"] = google_api

    try:
        llm = ChatGoogleGenerativeAI(
            model=model,
            temperature = 0,
            max_tokens = 8192
        )
        return [llm, model, "google_genai"]
    except Exception as e:
        raise ValueError(f"Failed to initialize Google GenAI: {str(e)}")
