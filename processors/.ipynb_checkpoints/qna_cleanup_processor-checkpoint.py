import os

class QnaCleanupProcessor:
    def __init__(self, source_dir: str):
        """
        Initialize the QnaCleanupProcessor.
        """
        self.source_dir = source_dir

    def process(self) -> list:
        """
        Replaces special characters with appropriate tokens.
        """
        try:

            for root, _, source_files in os.walk(source_dir):
                
                for source_file in source_files:
                    
                    print(f"Performing cleanup on {input_file}...")
                    
                    
        except Exception as e: 
            print(f"Error loading docs: {e}") 
            
            traceback.print_exc()
    
if __name__ == "__main__":  
    
    source_dir = f"{os.path.expanduser('~')}/{os.getenv('APP_NAME')}/scraped/studentaid"
    
    processor = QnaCleanupProcessor(source_dir)
    
    processor.process()
