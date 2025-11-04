
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

        # Read files and create initial Document objects
        for file_name in self.files:
            file_path = Path(self.docs_path) / file_name
            # skip directories
            if file_path.is_dir():
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    text = text.replace("\n", " ")
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


    def update_event(self,file_path: str, old_content: str, new_content: str) -> str:
        """Update the content of a file by replacing old_content with new_content."""
        try:
            with open(self.docs_path+"/"+file_path, 'r') as file:
                content = file.read()
            
            updated_content = content.replace(old_content, new_content)

            with open(self.docs_path+"/"+file_path, 'w') as file:
                file.write(updated_content)
            
            return "File updated successfully."
        except Exception as e:
            return f"An error occurred: {e}"

    def append_event(self, file_path: str, content: str) -> str:
        """Append content to a file."""
        try:
            with open(self.docs_path+"/"+file_path, 'a') as file:
                file.write(content + '\n')
            return "Content written successfully."
        except Exception as e:
            return f"An error occurred: {e}"

    def list_files(self) -> list[str]:
        """List all files in the given directory."""

        try:
            return self.files
        except Exception as e:
            return [f"An error occurred: {e}"]