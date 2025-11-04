from pathlib import Path
from Brain import Retriever

def main():
    retriever:Retriever = Retriever(memory_path=Path("./jarvis_memory"),docs_path=Path("docs"))
    
    
    while True:
        inp = input("User :")
        if inp == "q":
            print("Jarvis : Have a Good day Sir !!")
            break
        response:str = retriever.retrieve(inp)
        print(f"\nJarvis :{response}\n\n press q to quit \n\n")
    


if __name__=="__main__":
    main()