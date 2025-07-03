from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker.tokenizer.base import BaseTokenizer
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from transformers import AutoTokenizer
import os

class SpecialCharactersProcessor:
    def __init__(self, source_dir: str):
        """
        Initialize the SpecialCharactersProcessor.
        """
        self.source_dir = source_dir
        self.target_tokens = []
        self.replacement_tokens = []

    def process(self) -> list:
        """
        Replaces special characters with appropriate tokens.
        """
        try:

            for root, _, source_files in os.walk(source_dir):
                
                for source_file in source_files:
                    
                    print(f"Updating special characters in {input_file}...")
                    
                    
        except Exception as e: 
            print(f"Error loading docs: {e}") 
            
            traceback.print_exc()
    
if __name__ == "__main__":  
    
    source_dir = f"{os.path.expanduser('~')}/{os.getenv('APP_NAME')}/scraped/studentaid"
    
    processor = SpecialCharactersProcessor(source_dir)
    
    processor.process()
