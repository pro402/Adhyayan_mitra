from pathlib import Path
import re
from transformers import AutoTokenizer
from langchain_core.prompts import PromptTemplate
from docling.document_converter import DocumentConverter
from ..select_llm import llama_cpp, ollama
# from .doc_ex import ex_summarized_text, ex_text

class DocumentProcessor:
    """
    A class that handles document processing pipeline including:
    - Converting documents to markdown
    - Counting tokens
    - Summarizing content
    """
    
    def __init__(self, model_name="Qwen/Qwen2.5-0.5B-Instruct", max_tokens=2000):
        """
        Initialize the document processor with specified parameters
        
        Args:
            model_name (str): The name of the tokenizer model to use
            max_tokens (int): Maximum number of tokens allowed before summarization
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_tokens = max_tokens
        
        selector = input("Select summarizer Ollama or LLama.CPP: \n")

        if selector.lower() == "ollama":
            self.llm = ollama.set_llm()
        elif selector.lower() in ["llama", "llama cpp", "llamacpp", "llama_cpp", "cpp"]:
            self.llm = llama_cpp.set_llm()
        else:
            raise ValueError(f"Unsupported LLM backend: {selector}. Choose from 'ollama' or 'llama_cpp'.")
        
        # self.summarize_template = """
        # You are tasked with summarizing a document in a clear, concise, and professional manner. 
        # Your summary should retain all critical information while eliminating unnecessary details. 

        # To guide your approach, here is an example:
        # Document:
        # {ex_text}
        # Summary:
        # {ex_summarized_text}

        # Now, summarize the following document:
        # {text}

        # Make sure the response is in Markdown format.
        # """

        self.summarize_template = """
You are an expert educational content curator specializing in creating detailed study materials. Your task is to transform the provided notes into a thorough yet optimized version that retains nearly all educational value while improving structure and readability.

COMPREHENSIVE SUMMARIZATION GUIDELINES:

1. CONTENT PRESERVATION:
   - Retain 85-90% of all key information and concepts
   - Preserve ALL definitions, theorems, formulas, and core principles
   - Keep ALL numerical examples, case studies, and practical applications
   - Maintain ALL critical relationships between concepts
   - Include ALL lists of important points, steps, or classifications

2. OPTIMIZATION TECHNIQUES:
   - Condense verbose explanations without removing their substantive content
   - Convert lengthy paragraphs into structured bullet points where appropriate
   - Use tables to organize comparative information more efficiently
   - Standardize terminology and eliminate unnecessary repetition
   - Merge similar examples while preserving their distinct educational points

3. STRUCTURAL ENHANCEMENTS:
   - Organize content with clear hierarchical headings (##, ###)
   - Create visual separation between major topics
   - Use bold formatting for key terms and concepts
   - Employ numbered lists for sequential processes
   - Add section summaries for complex topics

4. EDUCATIONAL INTEGRITY:
   - Never sacrifice accuracy for brevity
   - Maintain the original pedagogical flow and logical progression
   - Preserve nuance in complex explanations
   - Retain cautionary notes and exception cases
   - Keep all citations and references to external sources

INPUT NOTES:
{text}

Create a comprehensive educational resource in Markdown format that preserves nearly all educational value while enhancing structure and readability. This should serve as a complete study resource that students can rely on for thorough understanding and revision.
"""
        self.summarize_prompt = PromptTemplate.from_template(self.summarize_template)
    
    def convert_to_markdown(self, file_path=None):
        """
        Convert a document to markdown format
        
        Args:
            file_path (str, optional): Path to the document. If None, will prompt user for input.
            
        Returns:
            str: The document content in markdown format
        """
        if file_path is None:
            path = Path(input("Enter the path to the document (format PDF, MD, DOCX)\n"))
        else:
            path = Path(file_path)
            
        if path.is_file() and path.suffix.lower() in ['.pdf', '.md', '.docx']:
            converter = DocumentConverter()
            result = converter.convert(path)
            text = result.document.export_to_markdown()
            return text
        else:
            print("The file needs to be PDF, DOCX or MD format.")
            return ""
    
    def count_tokens(self, input_text):
        """
        Count the number of tokens in the input text
        DocumentPipeline
        Args:
            input_text (str): The text to count tokens for
            
        Returns:
            int: Number of tokens in the text
        """
        tokens = self.tokenizer(input_text, return_tensors="pt")
        num_tokens = len(tokens["input_ids"][0])
        return num_tokens
    
    def summarize(self, input_text):
        """
        Summarize the input text
        
        Args:
            input_text (str): The text to summarize
            
        Returns:
            str: Summarized text in markdown format
        """
        chain = self.summarize_prompt | self.llm
        text = chain.invoke({
            # "ex_text": ex_text,
            # "ex_summarized_text": ex_summarized_text,
            "text": input_text
        })
        pattern = r"```markdown\n(.*?)$"
        result = re.search(pattern, text, re.DOTALL)

        if result:
            text = result.group(1).strip()
        
        return text
    
    def process_document(self, file_path=None):
        """
        Process a document through the entire pipeline:
        1. Convert to markdown
        2. Check token count
        3. Summarize if needed
        
        Args:
            file_path (str, optional): Path to the document. If None, will prompt user for input.
            
        Returns:
            str: Processed document content or error message
        """
        text = self.convert_to_markdown(file_path)
        token_count = self.count_tokens(text)
        
        if token_count > 5000:
            return f"Text is Too large to process {token_count} Tokens"
        elif token_count > 2000 and token_count <= 5000:
            print(f"Document has {token_count} tokens. Summarizing...")
            text = self.summarize(text)
        else:
            # For documents with <= 2000 tokens, use the raw text
            print(f"Document has {token_count} tokens. Using raw document.")
            
        return text

# Usage example
# if __name__ == "__main__":
#     processor = DocumentProcessor()
#     result = processor.process_document()
#     print(result)