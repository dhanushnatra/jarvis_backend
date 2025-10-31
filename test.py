from Brain import Retriever



def test_retriever_initialization():
    retriever = Retriever(docs_path="docs",chunk_size=100,chunk_overlap=40)
    retriever.change_llm_model("llama3.2")
    print("\n\n Answer:",retriever.answer("what are my upcoming projects ?",n_results=4))
    
if __name__ == "__main__":
    test_retriever_initialization()