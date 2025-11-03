from pathlib import Path
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from os import listdir
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .LLM import LLM


class FileOps:
    def __init__(self,docs_path: str | Path,chunk_size:int=1000):
        """Initialize FileOps with the path to the documents directory."""
        if isinstance(docs_path, Path):
            docs_path = str(docs_path.absolute().resolve())
        
        self.chunk_size = chunk_size
        self.overlap = chunk_size // 10
        self.docs_path = docs_path
        self.files = listdir(self.docs_path)
    
    def read_files(self) -> tuple[list[Document], list[str]]:
        """Read all text files in the documents directory and return them as a list of Document objects."""
        
        documents: list[Document] = []
        ids: list[str] = []

        # Read files and create initial Document objects
        for file_name in self.files:
            file_path = Path(self.docs_path) / file_name
            # skip directories
            if file_path.is_dir():
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception:
                # skip files we can't read as text
                continue

            # store source metadata so split chunks retain reference
            doc = Document(page_content=text, metadata={"source": str(file_path)})
            documents.append(doc)

        # Use recursive splitter to create chunks from the documents
        splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.overlap)
        if documents:
            chunked_docs = splitter.split_documents(documents)
        else:
            chunked_docs = []

        # build ids for each chunk (use filename-stem + index when possible)
        for i, d in enumerate(chunked_docs):
            src = d.metadata.get("source", "unknown")
            stem = Path(src).stem if src != "unknown" else "doc"
            ids.append(f"{stem}-{i}")

        return chunked_docs, ids



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
        self.file_ops=FileOps(self.docs_path,chunk_size=self.chunk_size)
        docs,ids = self.file_ops.read_files()
        self.vector_store.add_documents(documents=docs,ids=ids)
    
    def retrieve(self, query: str) -> str:
        """Retrieve relevant documents from the vector store based on the query."""
        context = self.retriever.invoke(query)
        response= self.llm.get_response(context=context,query=query)
        self.train()
        return response