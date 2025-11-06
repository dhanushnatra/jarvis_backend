from pathlib import Path
from langchain.tools import tool
from os import listdir
from ddgs.ddgs import DDGS
from .retriever import Retriever
from langchain_core.documents import Document
from .variables import docs_path, memory_path





retriever = Retriever(memory_path=memory_path, docs_path=docs_path)







@tool
def read_file(file_path: str) -> str:
    """Read the content of a file.
    
    Args:
        file_path (str): The path to the file.
        
    Returns:
        str: The content of the file or an error message.
    """
    try:
        print(f"Reading file from path: {docs_path+'/'+file_path}")
        with open(docs_path+"/"+file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return f"An error occurred: {e}"



@tool
def update_file(file_path: str, old_content: str, new_content: str) -> str:
    """Update the content of a file by replacing old_content with new_content.
    Args:
        file_path (str): The path to the file.
        old_content (str): The content to be replaced.
        new_content (str): The new content to replace with.
    Returns:
        str: Success or error message.
    """
    try:
        print(f"Updating file at path: {docs_path+'/'+file_path}")
        with open(docs_path+"/"+file_path, 'r') as file:
            content = file.read()
        
        updated_content = content.replace(old_content, new_content)

        with open(docs_path+"/"+file_path, 'w') as file:
            file.write(updated_content)
        
        return "File updated successfully."
    except Exception as e:
        return f"An error occurred: {e}"
@tool
def append_files(file_path: str, content: str) -> str:
    """Append content to a file. or write content of a file
    
    Args:
        file_path (str): The path to the file.
        content (str): The content to append.
    Returns:
        str: Success or error message.
        
    """
    try:
        print(f"Appending to file at path: {docs_path+'/'+file_path}")
        with open(docs_path+"/"+file_path, 'a') as file:
            file.write(content + '\n')
        return "Content written successfully."
    except Exception as e:
        return f"An error occurred: {e}"
    

@tool(description="List all files in the documents directory")
def list_files() -> list[str]:
    """List all files in the given directory.
    Returns:
        list[str]: List of file names or an error message.
    """
    files = listdir(docs_path)
    try:
        print(f"Listing files in directory: {docs_path}")
        return files
    except Exception as e:
        return [f"An error occurred: {e}"]


@tool(description="Search the Internet for content")
def search_internet(query:str,max_results:int)->list[dict]:
    """Search the Internet for content 
    
    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to retrieve.

    Returns:
        str: Aggregated search results.
    """
    print(f"Searching the internet for query: {query}")
    with DDGS() as ddgs:
        res = ddgs.text(query=query,max_results=max_results)
    print("Search complete.:",res)
    return res


@tool(description="Retrieve relevant information from vector store memory whenever user asks about his/her projects, schedule, or anything personal.")
def retrieve_from_memory(query:str)->list[dict]:
    """Retrieve relevant information from vector store memory whenever user asks about his/her projects, schedule, or anything personal.
    
    Args:
        query (str): The query to search in memory.
        
    Returns:
        list[Document]: Retrieved documents from memory.
    """
    print(f"Retrieving from memory for query: {query}")
    response = retriever.retrieve(query=query)
    return [{"content": doc.page_content , "metadata": doc.metadata} for doc in response]


all_tools = [list_files,search_internet,update_file,append_files,read_file,retrieve_from_memory]