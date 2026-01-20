from utils.file_handler import read_file
from utils.data_processor import clean_and_validate_data
import os

def main():
    file_path = os.path.join("data", "sales_data.txt")
    
    print("Reading data file...")
    try:
        lines = read_file(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return
        
    print("Processing data...")
    valid_records = clean_and_validate_data(lines)
    
    # Optional: Save valid records to output (not explicitly requested but good practice/placeholder)
    # output_path = os.path.join("output", "cleaned_sales_data.csv")
    # ...

if __name__ == "__main__":
    main()