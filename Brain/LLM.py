from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

class LLM:
    def __init__(self,llm_model:str) -> None:
        self.model = OllamaLLM(model=llm_model)



        self.prompt = PromptTemplate.from_template("""You are Jarvis — an intelligent, concise, and helpful personal assistant. 
        Your goal is to help the user by accurately answering their query using the provided context. 
        You are polite, efficient, and explain only what is necessary.

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
        if (user asks to change or update document or his data ): respond with 1 in the start line 
        then [old content ]
        [new content]
        """)

        self.chain = self.prompt | self.model



    def get_response(self,context: list[Document], query: str) -> str:
        """Generate a response using the LLM chain with the given context and query."""
        return self.chain.invoke({"context": context, "query": query})