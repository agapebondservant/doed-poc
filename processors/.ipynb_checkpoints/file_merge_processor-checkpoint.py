import os
import glob
import traceback
from pathlib import Path

class FileMergeProcessor:
    def __init__(self):
        """
        Initialize the FileMergeProcessor.
        """
        pass

    def process(self, input_dir, output_file):
        """
        Concatenates the files in this directory into one large master file.
        Currently supports MARKDOWN files.
        """

        SUPPORTED_EXTENSIONS = "md"

        print(f"Generating merged file {output_file} from directory {input_dir}...\n\n")

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        input_files = glob.glob(f"{input_dir}/*.{SUPPORTED_EXTENSIONS}", recursive=False)

        if not input_files:
            print(f"No matching files found in <{input_dir}>.")
            return

        with open(output_file, 'w') as outfile:
            for input_file in input_files:
                print(f"Adding file {os.path.basename(input_file)}...")
                with open(input_file, "r") as infile:
                    outfile.write(infile.read() + "\n\n")  
                    print(f"{os.path.basename(input_file)} added.\n\n")
            print("Merged file generated successfully.\n\n")
                        
if __name__ == "__main__": 
    
    processor = FileMergeProcessor()
    
    try:

        processor.process(
            f"{Path(__file__).resolve().parents[1]}/scraped/studentaid/state scholarships/", 
            f"{Path(__file__).resolve().parents[1]}/scraped/studentaid/merged/state scholarships/merged.md")
        
    except Exception as e:
        
        print("An exception occurred:")
        traceback.print_exc()
        print(f"Exception message: {e}")      
