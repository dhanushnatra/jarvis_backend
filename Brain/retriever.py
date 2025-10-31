
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .LLM import LLM
from .chunking import create_chunks_from_folder
from .file_ops import FileOps

class Retriever:
    def __init__(self,chunk_overlap:int=0, collection_name: str = "memory", embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2", chunk_size: int = 1024, docs_path: str | Path = Path("Brain/docs")) -> None:
        if isinstance(docs_path, Path):
            docs_path = str(docs_path.absolute().resolve())
        
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        if isinstance(docs_path, Path):
            docs_path = str(docs_path.absolute().resolve())
        self.docs_path = docs_path
        self.file_ops = FileOps(base_path=self.docs_path)
        self.embedder = SentenceTransformer(embedding_model)
        self.llm = LLM()
        self.chunk_overlap = chunk_overlap
        self.docs = create_chunks_from_folder(self.docs_path, self.chunk_size, chunk_overlap=chunk_overlap)
        self.doc_embeddings = self.embedder.encode([doc for doc in self.docs])
    
    def change_llm_model(self, model_name: str) -> None:
        """Change the LLM model used for generating answers."""    
        try:
            self.llm = LLM(model_name=model_name)
            print(f"LLM model changed to {model_name}")
        except Exception as e:
            print(f"Error changing LLM model: {e}")

    def change_embedding_model(self, model_name: str) -> None:
        try:
            self.embedder = SentenceTransformer(model_name)
            self.doc_embeddings = self.embedder.encode([doc for doc in self.docs])
            print(f"Embedding model changed to {model_name}")
        except Exception as e:
            print(f"Error changing embedding model: {e}")

    def train(self):
        try:
            print("Training retriever on the provided documents...")
            self.docs = create_chunks_from_folder(self.docs_path, self.chunk_size, chunk_overlap=self.chunk_overlap)
            self.doc_embeddings = self.embedder.encode([doc for doc in self.docs])
        except Exception as e:
            print(f"Error during training: {e}")

    def answer(self, user_query: str, n_results: int = 3) -> str:
        try:
            query_embedding = self.embedder.encode([user_query])
            similarities = cosine_similarity(query_embedding, self.doc_embeddings)[0]
            top_indices = similarities.argsort()[-n_results:][::-1]
            context = "\n\n".join([self.docs[i] for i in top_indices])
            [print(f"Document {i}: {self.docs[i]}") for i in top_indices]
            response= self.llm.generate_text(prompt=user_query, context=context)
            self.file_ops.append_to_file(f"User Query: {user_query}\nContext Used: {context}\nResponse: {response}\n\n")
            return response
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "Sorry, I couldn't process your request at this time."