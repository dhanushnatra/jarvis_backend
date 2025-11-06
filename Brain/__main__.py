from . import LLM
def main():
    query = input("Enter your query for LLM: ")
    llm = LLM(agent_llm="llama3.2", helper_llm="llama3.2", model_provider="ollama")
    response = llm.get_response(user_input=query)
    print("\n\n\nResponse:", response[1])
    print("\n\n\nThought Process:", response[0])
if __name__ == "__main__":
    main()