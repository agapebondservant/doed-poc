import ocr_processor
import traceback
import importlib
import os
from pathlib import Path
import shutil
importlib.reload(ocr_processor)


class WebscraperProcessor:
    def __init__(self, **kwargs):
        """
        Initialize the OCR processor.
        """
        self.ocr = ocr_processor.OcrProcessor()
        
    def process(self, source_urls: list, target_files: list): 
        
        try:
            if len(source_urls) != len(target_files):
                raise ValueError("Error: Number of source urls does not match number of target files.")
                
            for webpage_url, output_file in zip(source_urls, target_files):

                tmp_dir = os.path.dirname(output_file)
                
                tmp_file = ocr.export_to_markdown(webpage_url, tmp_dir)

                # Cleanup

                print(tmp_file)

                # print(output_file)

                # shutil.move(tmp_file, output_file)

                # os.rmdir(os.path.dirname(tmp_file))

            print("Webscraping complete.")
                
        except Exception as e:
            print(f"Error converting webpage: {e}") 
            
            traceback.print_exc()

if __name__ == "__main__":  
    webscraper = WebscraperProcessor()
    
    #source_urls = ["https://www.tuitionfundingsources.com/financial-aid/?state={num}" for num in [1]] #range(1,52)]
    
    #target_files = [f"{os.path.expanduser('~')}/cohesity-poc/scraped/financialaid_{num}.md" for num in [1]] #range(1,52)]

    source_urls = [f"{os.path.expanduser('~')}/doed-poc/resources/wyoming.html"]

    target_files = [f"{os.path.expanduser('~')}/doed-poc/scraped/wyoming.md"]
    
    webscraper.process(source_urls, target_files)