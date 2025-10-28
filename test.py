from pathlib import Path
from Brain import Retriever


if __name__=="__main__":
    retriever = Retriever(docs_path=Path("docs"),chunk_size=100)
    print("Embedding model used:", retriever.embedder.__class__.__name__)
    query = "what am i doing from 9AM to 10AM ?"
    answer = retriever.answer(user_query=query, n_results=3)
    print(f"Q: {query}\nA: {answer}")