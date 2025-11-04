from ddgs.ddgs import DDGS
from langchain_core.documents import Document

def search_internet(query:str,max_results:int=5)->list[Document]:
    result:list[Document] = []
    with DDGS() as ddgs:
        res = ddgs.text(query=query,max_results=max_results)
        for r in res:
            result.append(Document(page_content=r["body"],metadata={"source":r["href"]+r["title"]}))
    return result