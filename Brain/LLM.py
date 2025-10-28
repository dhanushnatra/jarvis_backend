from ollama import chat


prompt_template="""You are Jarvis — an intelligent, concise, and helpful personal assistant. 
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
"""



class LLM:
    def __init__(self,model_name:str="llama3.2") -> None:
        self.model_name = model_name
        self.messages = []

    def generate_text(self, prompt:str, context:str="") -> str:
        # format the prompt with context
        full_prompt = prompt_template.format(context=context, query=prompt)
        self.messages.append({"role": "user", "content": full_prompt})
        response = str(chat(model=self.model_name, messages=self.messages,).message.content)
        self.messages.append({"role": "assistant", "content": response})
        return response