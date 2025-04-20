import os
from dotenv import load_dotenv
from langchain_ollama.llms import OllamaLLM
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
google_api = os.getenv("GOOGLE_API")

def set_llm():
    choice = input("Enter choice of LLM Host Ollama or Google:\n")
    if choice.lower() == "ollama":
        llm = OllamaLLM(
            model="hf.co/mradermacher/Qwen2.5-0.5B-Instruct-GGUF:Q8_0",
            temperature=0,
            seed=42,
        )
    elif choice.lower() == "google":
        llm = ChatGoogleGenerativeAI(
            model="gemma-3-27b-it",
            temperature=0,
            max_tokens=8192,
            api_key = google_api,
        )
    else:
        raise ValueError("Invalid choice. Please choose 'ollama' or 'google'.")
    return llm