# !pip install -U huggingface_hub
# !huggingface-cli download Qwen/Qwen2.5-0.5B-Instruct-GGUF qwen2.5-0.5b-instruct-q8_0.gguf --local-dir . --local-dir-use-symlinks False

import os
from langchain_community.llms import LlamaCpp

def set_llm(
        model_path: str = "/home/prasun/Desktop/ADHYAYAN_MITRA/qwen2.5-0.5b-instruct-q8_0.gguf",
):
    """
    Set the LLM to use based on user input.
    Args:
        model (str): The model to use. Default is "path to qwen2.5-0.5b-instruct-q8_0.gguf".
        Choose model by typing ollama list in terminal.
    Returns:
        llm: The selected LLM.
    """
    llm = LlamaCpp(
        model_path=model_path,  # Path to your downloaded GGUF file
        temperature=0.0,  # Set as needed
        n_ctx=32768,       # Context window, adjust as needed
        max_tokens=8192,   # Max tokens for the response
        n_batch = 64,
        n_gpu_layers=0,   # 0 for CPU-only inference
        verbose=False  
    )
    return [llm, model_path, "llama_cpp"]