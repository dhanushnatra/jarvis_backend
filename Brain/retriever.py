from pathlib import Path
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from os import listdir, path
from shutil import rmtree
from .LLM import LLM
from .file_ops import FileOps
import re




def is_file_ops(text:str)-> tuple[bool,dict]:
    pattern= r'```.*?(\{[\s\S]*?\})\s*```'
    match = re.search(pattern, text, re.DOTALL)
    return (match is not None, eval(match.group(1)) if match else {})



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
        
        is_file_op, return_format = is_file_ops(response)
        print(is_file_op, return_format)
        if is_file_op:
            if return_format["function"] == "append_event":
                file_path = return_format["file_path"]
                content = return_format["content"]
                self.file_ops.append_event(file_path=file_path, content=" "+content)
                return f"Event added successfully. Appended to {file_path} with {content}"
            elif return_format["function"] == "update_event":
                file_path = return_format["file_path"]
                old_content = return_format["old_content"]
                new_content = return_format["new_content"]
                self.file_ops.update_event(file_path=file_path, old_content=old_content, new_content=new_content)
                return f"Event updated successfully. Updated {file_path} with {new_content}"
            elif return_format["function"] == "list_files":
                files = listdir(self.docs_path)
                response = "Available files are:\n" + "\n".join(files)
                return response
        self.train()
        return response