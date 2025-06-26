import traceback
import ocr_processor
import importlib
import os
from pathlib import Path
import shutil
importlib.reload(ocr_processor)


class VectorDbProcessor:
    def __init__(self, **kwargs):
        """
        Initialize the OCR processor.
        """
        self.ocr = ocr_processor.OcrProcessor()
        
    def process(self, source_docs: list, target_dir: str): 
        
        for source_doc in source_docs:
            try:
                self.ocr.export_to_markdown(source_doc, target_dir)
            except Exception as e:
                print(f"Error converting source doc: {e}") 
                
                traceback.print_exc()

                continue

if __name__ == "__main__":  
    processor = VectorDbProcessor()

    source_dir = f"{os.path.expanduser('~')}/doed-poc/resources"

    target_dir = f"{os.path.expanduser('~')}/doed-poc/scraped"

    os.makedirs(source_dir, exist_ok=True)

    os.makedirs(target_dir, exist_ok=True)

    source_urls = [f"{source_dir}/{file_name}" for file_name in os.listdir(source_dir)]
    
    processor.process(source_urls, target_dir)