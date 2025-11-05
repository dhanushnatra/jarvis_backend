
from os import listdir
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter





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
        splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.overlap)
        
        for file_name in self.files:
            if file_name.endswith(".txt"):
                with open(self.docs_path+"/"+file_name,"r") as f:
                    content = f.read()
                    splits = splitter.split_text(content)
                    documents+=[Document(page_content=split,metadata={"source": file_name}) for split in splits]
                ids +=file_name
                
        return documents,ids
    
    