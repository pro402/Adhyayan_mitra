from pathlib import Path
import re
from transformers import AutoTokenizer
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from docling.document_converter import DocumentConverter
from .doc_ex import ex_summarized_text, ex_text

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
        self.llm = OllamaLLM(
            # model="qwen2.5:0.5b",
            model = "hf.co/mradermacher/Qwen2.5-0.5B-Instruct-GGUF:Q8_0",
            temperature=0,
        )
        self.summarize_template = """
        You are tasked with summarizing a document in a clear, concise, and professional manner. 
        Your summary should retain all critical information while eliminating unnecessary details. 

        To guide your approach, here is an example:
        Document:
        {ex_text}
        Summary:
        {ex_summarized_text}

        Now, summarize the following document:
        {text}

        Make sure the response is in Markdown format.
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
            "ex_text": ex_text,
            "ex_summarized_text": ex_summarized_text,
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
            str: Processed document content
        """
        text = self.convert_to_markdown(file_path)
        
        while self.count_tokens(text) >= self.max_tokens:
            print(f"Document exceeds {self.max_tokens} tokens. Summarizing...")
            text = self.summarize(text)
            
        return text

# # Usage example
# if __name__ == "__main__":
#     processor = DocumentProcessor()
#     result = processor.process_document()
#     print(result)