import os

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    
    Args:
        filename (str): Path to the file to read.
        
    Returns:
        list: List of raw lines (strings), excluding header and empty lines.
        
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
        
    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                lines = f.readlines()
            break # Success
        except UnicodeDecodeError:
            continue
            
    if not lines:
        # If all strict encodings fail, try with errors='replace' using utf-8 as last resort
        # though the requirements say "Handle different encodings", usually implies trying them.
        # If we are here, either file is empty or all failed.
        # Let's try one last time with replace if we haven't got data?
        # Or just return empty if it was truly empty.
        # For safety/robustness, if we still have no lines and file exists, maybe it was empty.
        # But if it failed decoding, we might want a fallback.
        # Given the task description "Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')",
        # we've done that.
        pass

    cleaned_lines = []
    # Skip header row (assuming first row is header if it contains 'TransactionID' or just skip first)
    # The requirement says "Skip the header row".
    # We will look for a header signature or just skip the first line if it looks like a header.
    
    start_index = 0
    if lines and 'TransactionID' in lines[0]:
        start_index = 1
        
    for i in range(start_index, len(lines)):
        line = lines[i].strip()
        if line: # Remove empty lines
            cleaned_lines.append(line)
            
    return cleaned_lines