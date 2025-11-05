
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain.chat_models import init_chat_model
from .tools import all_tools






class LLM:
    def __init__(self,llm_model:str) -> None:
        
        self.model = init_chat_model(model=llm_model,model_provider="ollama",)
        self.model=self.model.bind_tools(all_tools)
        self.prompt = PromptTemplate.from_template("""You are Jarvis — an intelligent, concise, and helpful personal assistant. 
        Your goal is to help the user by accurately answering their query using the provided context. 
        You are polite, efficient, and explain only what is necessary.
        You have access to user documents and data to assist in answering queries.
        
        ### Instructions:
        1. Use the context below to answer the query.
        2. If the answer is not directly found in the context, respond based on your general knowledge — but clearly state that it’s inferred or general.
        3. Never invent facts that contradict the context.
        4. Respond in a friendly, assistant-like tone (like Iron Man’s Jarvis).
        5. Keep responses short and clear unless the user asks for details.
        6. Always aim to be helpful, accurate, and as concise as possible.

        ---

        ### Context:
        {context}

        ---

        ### Query:
        {query}

        ---

        ### Output Format:
        """)
        
        self.chain = self.prompt | self.model

    def get_response(self, context: list[Document], query: str) -> str:
        """Generate a response using the LLM chain with the given context and query."""
        
        for doc in context:
            print(f"Source: {doc.metadata.get('source', 'unknown')}\nContent: {doc.page_content}\n---\n")

        llm_response = self.chain.invoke({"context": context, "query": query}).text
        
        return llm_response