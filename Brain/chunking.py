import os
import re
from pathlib import Path

def chunk_text(text, max_chars=500, overlap=50):
    """
    Split text into overlapping chunks.
    max_chars: chunk size
    overlap: how many characters to overlap between chunks
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += max_chars - overlap
    return chunks

def create_chunks_from_folder(input_folder:str|Path="docs",max_chars=500)->list[str]:
    final_chunks = []
    for file in os.listdir(input_folder):
        if not file.endswith(".txt"):
            continue
        with open(os.path.join(input_folder, file), "r", encoding="utf-8") as f:
            text = f.read()
        
        # optional: clean text
        text = re.sub(r"\s+", " ", text)
        chunks = chunk_text(text, max_chars=max_chars)
        for chunk in chunks:
            final_chunks.append(chunk)
    print(len(final_chunks))
    return final_chunks