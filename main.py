from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter
import os

def main():
    file_path = os.path.join("data", "sales_data.txt")
    
    # Task 1.1: Read Data
    print("--- Task 1.1: Reading Data ---")
    try:
        raw_lines = read_sales_data(file_path)
        print(f"Successfully read {len(raw_lines)} lines.")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return
        
    # Task 1.2: Parse Data
    print("\n--- Task 1.2: Parsing Data ---")
    transactions = parse_transactions(raw_lines)
    print(f"Parsed {len(transactions)} transaction records.")
    if transactions:
        print(f"Sample record: {transactions[0]}")
        
    # Task 1.3: Validate and Filter
    print("\n--- Task 1.3: Validation and Filtering ---")
    # Example usage: Filter by 'North' region, and maybe some amount
    # The requirement says "Displays available options to user", which is done inside the function.
    # But for this script, we can demonstrate a call.
    
    # Let's do a run without filters first to show validation stats
    print("1. Run without filters:")
    valid_tx, invalid_count, summary = validate_and_filter(transactions)
    print("Summary:", summary)
    
    # Let's do a run WITH filters (e.g., Region='North')
    print("\n2. Run with Region='North':")
    valid_tx_north, invalid_count_north, summary_north = validate_and_filter(transactions, region='North')
    print("Summary:", summary_north)

if __name__ == "__main__":
    main()