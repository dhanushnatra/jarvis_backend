from pathlib import Path
memory_path = str(Path("jarvis_memory").absolute().resolve())
docs_path = str(Path("docs").absolute().resolve())



def set_memory_path(path: str | Path):
    global memory_path
    if isinstance(path, Path):
        path = str(path.absolute().resolve())
    memory_path = path
def set_docs_path(path: str | Path):
    global docs_path
    if isinstance(path, Path):
        path = str(path.absolute().resolve())
    docs_path = path