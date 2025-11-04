class Tool:
    def __init__(self,name:str,description:str,func_name:str,return_format:dict) -> None:
        self.name = name
        self.description = description
        self.func_name = func_name
        self.return_format = return_format
    
    def __repr__(self) -> str:
        return f"Tool(name={self.name}, description={self.description}, func_name={self.func_name}, return_format={self.return_format})"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "func_name": self.func_name,
            "return_format": self.return_format
        }
    @staticmethod
    def from_dict(data: dict) -> 'Tool':
        return Tool(
            name=data.get("name", ""),
            description=data.get("description", ""),
            func_name=data.get("func_name", ""),
            return_format=data.get("return_format", {})
        )
        




def create_tool(name: str, description: str, func_name: str, return_format: dict) -> Tool:
    """Create a Tool object with the given parameters."""
    return Tool(name, description, func_name, return_format)



tools:list[Tool] = [
    create_tool("write", "Write to Events file if user wants to add a event to his schedule at some DD-MM-YYYY TIME or DD-MM-YYYY your job is to generate the content using query of user and return in return_format only inside ```return_format```", "append_file", {"function":"append_event","file_path": "events.txt","content": "to be added by Jarvis"}),
    create_tool("delete", "Delete from Events file if user wants to delete a event from his schedule at some DD-MM-YYYY TIME or DD-MM-YYYY return in return_format only inside ```return_format```", "update_file", {"function":"delete_event","file_path": "events.txt","old_content": "content to be deleted","new_content": "new content after deletion"}),
    create_tool("list_files", "List all files in the documents directory if user wants to know what documents are available return in return_format only inside ```return_format```", "list_files",{"function":"list_files"}),
]