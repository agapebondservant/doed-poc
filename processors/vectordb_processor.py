import traceback
import ocr_processor
import importlib
import os
from pathlib import Path
import shutil
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from langchain_nomic import NomicEmbeddings
from llama_index.embeddings.openai import OpenAIEmbedding
importlib.reload(ocr_processor)
import chromadb

class VectorDbProcessor:
    def __init__(self, **kwargs):
        """
        Initialize the OCR processor.
        """
        print("Initializing OCR Processor...")
        self.ocr = ocr_processor.OcrProcessor()
        
        print(f"Initializing ChromaDb Client...")
        self.chroma_client = chromadb.HttpClient(host= f"http://{os.getenv('CHROMA_API_BASE')}")

        print("Initializing embedding model...")
        self.embed_model = OpenAIEmbedding(
            api_key=os.getenv('EMBED_API_KEY'),
            api_base=os.getenv('EMBED_API_BASE'),
            dimensionality=1536,
            model_name="nomic-embed-text-v1.5",
        )

        self.index = None
        
        if 'source_dir' in kwargs and 'collection_name' in kwargs:
            self.index = self.load_documents(kwargs['source_dir'], kwargs['collection_name'])

    def load_documents(self, source_dir: str, collection_name: str):
        print(f"Loading documents into collection {collection_name}...")
        documents = SimpleDirectoryReader(input_dir=source_dir, recursive=True).load_data()
        
        vector_store = ChromaVectorStore(chroma_collection=collection_name)
        
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        try:
            index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context, embed_model=self.embed_model
            )
            print("Loading complete.")
        except: 
            print(f"Error loading docs: {e}") 
            
            traceback.print_exc()
        
        return index
        
    def process(self, collection_name: str): 
        
        try:
            chroma_collection = self.chroma_client.get_or_create_collection(collection_name)
            
            query_engine = self.index.as_query_engine()
            
            response = query_engine.query("What are the academic year requirements?")
            
            display(Markdown(f"<b>{response}</b>"))
        except Exception as e:
            print(f"Error converting source doc: {e}") 
            
            traceback.print_exc()

if __name__ == "__main__":  
    source_dir = f"{os.path.expanduser('~')}/doed-poc/resources/studentaid"
    
    processor = VectorDbProcessor(source_dir=source_dir, collection_name='scholarships')
    
    processor.process("scholarships")