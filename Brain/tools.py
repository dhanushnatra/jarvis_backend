from pathlib import Path
from langchain.tools import tool
from os import listdir
from ddgs.ddgs import DDGS



docs_path = str(Path("docs").absolute().resolve())



@tool("Update the content of a file by replacing old_content with new_content.",return_direct=True)
def update_file(file_path: str, old_content: str, new_content: str) -> str:
    """Update the content of a file by replacing old_content with new_content."""
    try:
        with open(docs_path+"/"+file_path, 'r') as file:
            content = file.read()
        
        updated_content = content.replace(old_content, new_content)

        with open(docs_path+"/"+file_path, 'w') as file:
            file.write(updated_content)
        
        return "File updated successfully."
    except Exception as e:
        return f"An error occurred: {e}"
@tool("Append content to a file. or write content of a file",return_direct=True)
def append_files(file_path: str, content: str) -> str:
    """Append content to a file. or write content of a file"""
    try:
        with open(docs_path+"/"+file_path, 'a') as file:
            file.write(content + '\n')
        return "Content written successfully."
    except Exception as e:
        return f"An error occurred: {e}"
    
@tool("List all files in the given directory.",return_direct=True)
def list_files() -> list[str]:
    """List all files in the given directory."""
    files = listdir(docs_path)
    try:
        
        return files
    except Exception as e:
        return [f"An error occurred: {e}"]


@tool("Search the Internet for content ",return_direct=True)
def search_internet(query:str,max_results:int)->str:
    """Search the Internet for content """
    result = ""
    with DDGS() as ddgs:
        res = ddgs.text(query=query,max_results=max_results)
        for r in res:
            result += f"Data from the internet: {r['body']}, metadata: 'source': {r['href'] + r['title']}"
    return result


all_tools = [list_files,search_internet,update_file,append_files]