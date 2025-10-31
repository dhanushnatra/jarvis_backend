from os import listdir
from pathlib import Path
from datetime import datetime

class FileOps:
    def __init__(self, base_path: str | Path = Path("docs")) -> None:
        self.base_path = Path(base_path)
        if not self.base_path.exists():
            self.base_path.mkdir(parents=True)
        self.files = listdir(self.base_path)  
        self.now = datetime.now().date().strftime("%Y-%m-%d.txt")
    
    def is_today(self) -> tuple[bool, str | None]:
        if self.now in self.files:
            return True, self.now
        with open(self.base_path / self.now, "w", encoding="utf-8") as f:
            f.write("") 
        self.files = listdir(self.base_path)
        return False, "but created new file for today. no worries!"
    
    def append_to_file(self, content: str) -> bool:
        self.is_today()
        try:
            with open(self.base_path / self.now, "a", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error appending to file: {e}")
            return False