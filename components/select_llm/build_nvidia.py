from langchain_nvidia_ai_endpoints import ChatNVIDIA

def set_llm(
    model: str = "meta/llama-3.3-70b-instruct",
    nvidia_api_key: str = None  # Correct parameter name
):
    """
    Configure NVIDIA AI Foundation Model with proper authentication
    
    Args:
        model: Valid NVIDIA model name
        nvidia_api_key: API key from NVIDIA API Catalog (starts with 'nvapi-')
    
    Returns:
        List containing [llm, model_name, provider]
    """
    try:
        llm = ChatNVIDIA(
            model=model,  # Use passed model parameter
            temperature=0.3,
            max_output_tokens=8192,  # Correct parameter name
            api_key=nvidia_api_key  # Pass API key directly
        )
        return [llm, model, "build_nvidia"]
    except Exception as e:
        raise ValueError(f"Failed to initialize NVIDIA AI: {str(e)}")
