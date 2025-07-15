from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
def get_from_web(query: str) -> str:
    """Get information from the web using DuckDuckGo.
    Args:
        query (str): The search query to run.
    Returns:
        str: The result of the search.
    """
    result = search.run(query)
    return result

if __name__ == "__main__":
    query = "how to install flutter in windows "
    print(get_from_web(query))