import os
from langchain_ollama.llms import OllamaLLM

def set_llm(
        model: str = "hf.co/mradermacher/Qwen2.5-0.5B-Instruct-GGUF:Q8_0",
):
    """
    Set the LLM to use based on user input.
    Args:
        model (str): The model to use. Default is "hf.co/mradermacher/Qwen2.5-0.5B-Instruct-GGUF:Q8_0".
        Choose model by typing ollama list in terminal.
    Returns:
        llm: The selected LLM.
    """
    llm = OllamaLLM(
        model=model,
        temperature=0,
        seed=42,
    )
    return [llm, model,"ollama"]