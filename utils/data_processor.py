def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries.
    
    Args:
        raw_lines (list): List of raw strings from the file.
        
    Returns:
        list: List of dictionaries with clean data types.
    """
    transactions = []
    
    for line in raw_lines:
        parts = line.split('|')
        
        # Skip rows with incorrect number of fields (expected 8)
        if len(parts) != 8:
            continue
            
        tid, date, pid, pname, qty_str, price_str, cid, region = parts
        
        # Handle commas within ProductName
        pname = pname.replace(',', '').strip()
        
        # Clean numeric fields (remove commas)
        qty_str = qty_str.replace(',', '').strip()
        price_str = price_str.replace(',', '').strip()
        
        # Convert types
        try:
            qty = int(qty_str)
            price = float(price_str)
        except ValueError:
            # Skip if conversion fails
            continue
            
        record = {
            'TransactionID': tid.strip(),
            'Date': date.strip(),
            'ProductID': pid.strip(),
            'ProductName': pname,
            'Quantity': qty,
            'UnitPrice': price,
            'CustomerID': cid.strip(),
            'Region': region.strip()
        }
        transactions.append(record)
        
    return transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    
    Args:
        transactions (list): List of transaction dictionaries.
        region (str, optional): Filter by specific region.
        min_amount (float, optional): Minimum transaction amount.
        max_amount (float, optional): Maximum transaction amount.
        
    Returns:
        tuple: (valid_transactions, invalid_count, filter_summary)
    """
    
    # 1. Validation Phase
    validated_list = []
    invalid_count = 0
    
    for t in transactions:
        is_valid = True
        
        # Check required fields presence (should be handled by parser mostly, but double check empty strings)
        if not t['TransactionID'] or not t['Date'] or not t['ProductID'] or not t['ProductName'] or not t['CustomerID'] or not t['Region']:
            is_valid = False
            
        # Quantity > 0
        if t['Quantity'] <= 0:
            is_valid = False
            
        # UnitPrice > 0
        if t['UnitPrice'] <= 0:
            is_valid = False
            
        # TransactionID must start with 'T'
        if not t['TransactionID'].startswith('T'):
            is_valid = False
            
        # ProductID must start with 'P' (Case insensitive check to be safe, or strict 'P'/'p')
        # Requirement says "ProductID must start with 'p'". Sample data has 'P'.
        if not t['ProductID'].upper().startswith('P'):
            is_valid = False
            
        # CustomerID must start with 'C'
        if not t['CustomerID'].startswith('C'):
            is_valid = False
            
        if is_valid:
            validated_list.append(t)
        else:
            invalid_count += 1
            
    # 2. Filtering Phase
    
    # Print available regions
    unique_regions = sorted(list(set(t['Region'] for t in validated_list)))
    print(f"Available regions: {unique_regions}")
    
    # Print transaction amount range
    amounts = [t['Quantity'] * t['UnitPrice'] for t in validated_list]
    if amounts:
        print(f"Transaction amount range: Min={min(amounts):.2f}, Max={max(amounts):.2f}")
    else:
        print("Transaction amount range: N/A (no valid records)")
        
    filtered_list = validated_list[:]
    filter_summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': 0,
        'filtered_by_amount': 0,
        'final_count': 0
    }
    
    # Filter by Region
    if region:
        before_count = len(filtered_list)
        filtered_list = [t for t in filtered_list if t['Region'] == region]
        filter_summary['filtered_by_region'] = before_count - len(filtered_list)
        
    # Filter by Amount
    before_count_amt = len(filtered_list)
    if min_amount is not None:
        filtered_list = [t for t in filtered_list if (t['Quantity'] * t['UnitPrice']) >= min_amount]
        
    if max_amount is not None:
        filtered_list = [t for t in filtered_list if (t['Quantity'] * t['UnitPrice']) <= max_amount]
        
    filter_summary['filtered_by_amount'] = before_count_amt - len(filtered_list)
    filter_summary['final_count'] = len(filtered_list)
    
    # Show count of records after each filter applied (as per requirement)
    # The summary dict captures the deltas.
    # The requirement says "Show count of records after each filter applied".
    # I'll print it here as well to satisfy "Filter Display" requirement.
    
    print(f"Records after validation: {len(validated_list)}")
    if region:
        print(f"Records after region filter ({region}): {len(validated_list) - filter_summary['filtered_by_region']}")
    if min_amount is not None or max_amount is not None:
         print(f"Records after amount filter: {filter_summary['final_count']}")
         
    return filtered_list, invalid_count, filter_summary