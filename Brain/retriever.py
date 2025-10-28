import fasttext
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .LLM import LLM
from .chunking import create_chunks_from_folder
class Retriever:
    def __init__(self, collection_name: str = "memory", embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2", chunk_size: int = 1024, docs_path: str | Path = Path("Brain/docs")) -> None:
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        self.docs_path = Path(docs_path)
        self.embedder = SentenceTransformer(embedding_model)
        self.llm = LLM()
        self.docs = create_chunks_from_folder(self.docs_path, self.chunk_size)
        self.doc_embeddings = self.embedder.encode([doc for doc in self.docs])
    
    def answer(self, user_query: str, n_results: int = 3) -> str:
        query_embedding = self.embedder.encode([user_query])
        similarities = cosine_similarity(query_embedding, self.doc_embeddings)[0]
        top_indices = similarities.argsort()[-n_results:][::-1]
        context = "\n\n".join([self.docs[i] for i in top_indices])
        [print(f"Document {i}: {self.docs[i]}") for i in top_indices]
        return self.llm.generate_text(prompt=user_query, context=context)