__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import importlib
import traceback
import chromadb
import ocr_processor
import splitter_processor
import os
from pathlib import Path
import shutil
from langchain.chains import RetrievalQA 
from langchain_core.documents import Document
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from chromadb.config import Settings
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv
importlib.reload(ocr_processor)
importlib.reload(splitter_processor)
load_dotenv()

class VectorDbProcessor:
    def __init__(self, llm: str, embed_model: str, **kwargs):
        """
        Initialize relevant settings for LLMs, OCR and Splitter.
        """
        print("Initializing OCR Processor...")
        self.ocr = ocr_processor.OcrProcessor()

        print("Initializing splitter...")
        self.splitter = splitter_processor.SplitterProcessor()
        
        print("Initializing Vector DB/LLM settings...")
        self.initialize_db_settings(llm, embed_model, **kwargs)
            
    def initialize_db_settings(self, llm: str, embed_model: str, **kwargs):
        print("Initializing settings for LLM model...")
        self.llm = OpenAI(
            model=llm, 
            temperature=0.1,
            api_key=os.getenv('GRANITE_API_KEY'),
            base_url=os.getenv('GRANITE_API_BASE'),
        )
            
        print("Initializing embedding model...")
        self.embed_model = OpenAIEmbeddings(
            api_key=os.getenv('EMBED_API_KEY'),
            base_url=os.getenv('EMBED_API_BASE'),
            dimensions=768,
            model=embed_model,
        )
        
        print(f"Initializing ChromaDb Client...")
        self.chroma_client = chromadb.HttpClient(host= f"http://{os.getenv('CHROMA_API_BASE')}", settings=Settings(allow_reset=True))
        # self.chroma_client = chromadb.PersistentClient(path=f"{Path.cwd()}/db")
            
        print(f"Initializing Vector Store...")
        self.vector_store = Chroma(
            client=self.chroma_client,
            embedding_function=self.embed_model,
            persist_directory='/data',
            collection_name=kwargs.get('collection_name') or 'langchain',
        )

        if 'source_dir' in kwargs and 'collection_name' in kwargs:
            self.load_documents(kwargs['source_dir'], kwargs['collection_name'])

    def load_documents(self, source_dir: str, collection_name: str):
        
        print(f"Creating collection {collection_name} (if it does not exist)...")
        
        chroma_collection = self.chroma_client.get_or_create_collection(collection_name)

        print(f"Loading documents from {source_dir} into collection {collection_name}...")
        
        try:

            for root, _, source_files in os.walk(source_dir):
                
                for source_file in source_files:
                
                    chunks = self.splitter.process(os.path.join(root,source_file))
                    
                    documents = [Document(id=str(uuid4()), page_content=chunk) for chunk in chunks]
                    
                    self.vector_store.add_documents(documents=documents)
                
            print("Loading complete.")
        except Exception as e: 
            print(f"Error loading docs: {e}") 
            
            traceback.print_exc()
        
    def process(self, collection_name: str = None, prompt: str = None ): 
        
        try:
            chroma_collection = self.chroma_client.get_or_create_collection(collection_name)
            
            print(f"Performing query on collection {collection_name} ({chroma_collection.count()} docs total)...")
            
            results = self.vector_store.similarity_search(prompt, k=3)
            
            for res in results:
                print(f"* {res.page_content} [{res.metadata}]")
                
        except Exception as e:
            print(f"Error converting source doc: {e}") 
            
            traceback.print_exc()

if __name__ == "__main__":  
    
    source_dir = f"{os.path.expanduser('~')}/{os.getenv('APP_NAME')}/scraped/studentaid"
    
    processor = VectorDbProcessor(llm='granite-3-8b-instruct',
                                  embed_model='nomic-embed-text-v1.5',
                                  collection_name='scholarships',)
                                  # source_dir=source_dir,)
    
    processor.process(collection_name="scholarships", prompt="What are the academic year requirements for scholarships in Maryland?")