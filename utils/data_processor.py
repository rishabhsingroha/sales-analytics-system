def clean_and_validate_data(lines):
    """
    Parses, cleans, and validates sales data lines.
    
    Args:
        lines (list): List of raw strings from the file.
        
    Returns:
        list: List of valid, cleaned dictionaries representing records.
    """
    valid_records = []
    total_parsed = 0
    invalid_count = 0
    
    # Skip header if present
    start_index = 0
    if lines and 'TransactionID' in lines[0]:
        start_index = 1
        
    for i in range(start_index, len(lines)):
        line = lines[i].strip()
        if not line:
            continue
            
        total_parsed += 1
        parts = line.split('|')
        
        # Check for missing or extra fields (expected 8 fields)
        if len(parts) != 8:
            invalid_count += 1
            continue
            
        tid, date, pid, pname, qty_str, price_str, cid, region = parts
        
        # Clean fields
        pname = pname.replace(',', '').strip()
        qty_str = qty_str.replace(',', '').strip()
        price_str = price_str.replace(',', '').strip()
        cid = cid.strip()
        region = region.strip()
        tid = tid.strip()
        
        # Validation checks
        is_valid = True
        
        # 1. TransactionID must start with 'T'
        if not tid.startswith('T'):
            is_valid = False
            
        # 2. Missing CustomerID or Region
        if not cid or not region:
            is_valid = False
            
        # 3. Numeric conversions and checks
        qty = 0
        price = 0.0
        try:
            qty = int(qty_str)
            price = float(price_str)
            
            if qty <= 0 or price <= 0:
                is_valid = False
                
        except ValueError:
            # Could not convert to number
            is_valid = False
            
        if is_valid:
            record = {
                'TransactionID': tid,
                'Date': date.strip(),
                'ProductID': pid.strip(),
                'ProductName': pname,
                'Quantity': qty,
                'UnitPrice': price,
                'CustomerID': cid,
                'Region': region
            }
            valid_records.append(record)
        else:
            invalid_count += 1

    print(f"Total records parsed: {total_parsed}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_records)}")
    
    return valid_records