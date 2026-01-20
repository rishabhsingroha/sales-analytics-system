import os

def read_file(file_path):
    """
    Reads a file with non-UTF-8 encoding (handling potential encoding issues).
    
    Args:
        file_path (str): Path to the file to read.
        
    Returns:
        list: List of strings (lines) from the file.
        
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    try:
        # Try reading with latin-1 (common for non-utf-8) or cp1252
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.readlines()
    except UnicodeDecodeError:
        # Fallback to errors='replace' if strict decoding fails
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.readlines()