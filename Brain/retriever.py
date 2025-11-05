from pathlib import Path
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma


from .LLM import LLM
from .file_ops import FileOps



class Retriever:
    def __init__(self,memory_path:str|Path, docs_path: str | Path,embedding_model:str="mxbai-embed-large",llm_model="llama3.2",chunk_size:int=1000):
        """Initialize the Retriever with a vector store and embedding model."""
        
        
        if isinstance(docs_path, Path):
            docs_path = str(docs_path.absolute().resolve())
            
        if isinstance(memory_path, Path):
            memory_path = str(memory_path.absolute().resolve())
            
        self.docs_path = docs_path
        self.llm = LLM(llm_model=llm_model)
        self.embedding_model = OllamaEmbeddings(model=embedding_model)
        self.vector_store = Chroma(
            embedding_function=self.embedding_model,
            collection_name="jarvis",
            persist_directory= memory_path
        )
        
        self.retriever = self.vector_store.as_retriever()
        self.chunk_size=chunk_size
        self.file_ops = FileOps(docs_path=self.docs_path,chunk_size=self.chunk_size)
        self.train()

    def train(self):
        docs,ids = self.file_ops.read_files()
        self.vector_store.add_documents(documents=docs,ids=ids)
        
    def refresh_memory(self):
        """Refresh the vector store by deleting existing data and retraining."""
        self.vector_store.delete_collection()
        self.train()
    
    def retrieve(self, query: str) -> str:
        """Retrieve relevant documents from the vector store based on the query."""
        context = self.retriever.invoke(query)
        response= self.llm.get_response(context=context,query=query)
        return response