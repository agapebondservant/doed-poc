import os
import glob

class DataCollectionProcessor:
    def __init__(self):
        """
        Initialize the DataCollectionProcessor.
        """
        pass

    def process(self, input_dir, output_dir, table_dir) -> tuple[list, list, list]:
        """
        Prepares the dataset (files/directories, environment settings/variables etc) that will be used
        as the source for a data processing job.
        """
        input_subdirs = glob.glob(f"{input_dir}/**/", recursive=True)

        input_subdirs = [subdir for subdir in input_subdirs if glob.glob(f"{subdir}/*.md")]

        if not input_subdirs:
            print(f"No Markdown files found in <{input_dir}>.")
            return
        
        output_subdirs = [f"{output_dir}{subdir.partition(input_dir)[2]}" for subdir in input_subdirs]
        
        table_subdirs = [f"{table_dir}{subdir.partition(input_dir)[2]}" for subdir in input_subdirs]

        return input_subdirs, output_subdirs, table_subdirs
