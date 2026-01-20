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
    
    return filtered_list, invalid_count, filter_summary

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float (total revenue)
    """
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)

def region_wise_sales(transactions):
    """
    Analyzes sales by region
    Returns: dictionary with region statistics
    """
    region_stats = {}
    total_revenue = calculate_total_revenue(transactions)
    
    # Aggregation
    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']
        
        if region not in region_stats:
            region_stats[region] = {'total_sales': 0.0, 'transaction_count': 0}
        
        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1
        
    # Calculate percentages and format
    result = {}
    for region, stats in region_stats.items():
        percentage = (stats['total_sales'] / total_revenue * 100) if total_revenue > 0 else 0
        result[region] = {
            'total_sales': stats['total_sales'],
            'transaction_count': stats['transaction_count'],
            'percentage': round(percentage, 2)
        }
        
    # Sort by total_sales descending
    sorted_result = dict(sorted(result.items(), key=lambda item: item[1]['total_sales'], reverse=True))
    return sorted_result

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_stats = {}
    
    for t in transactions:
        pname = t['ProductName']
        qty = t['Quantity']
        amount = qty * t['UnitPrice']
        
        if pname not in product_stats:
            product_stats[pname] = {'qty': 0, 'revenue': 0.0}
            
        product_stats[pname]['qty'] += qty
        product_stats[pname]['revenue'] += amount
        
    # Convert to list of tuples
    products_list = [
        (pname, stats['qty'], stats['revenue']) 
        for pname, stats in product_stats.items()
    ]
    
    # Sort by TotalQuantity descending
    products_list.sort(key=lambda x: x[1], reverse=True)
    
    return products_list[:n]

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    Returns: dictionary of customer statistics
    """
    customer_stats = {}
    
    for t in transactions:
        cid = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        pname = t['ProductName']
        
        if cid not in customer_stats:
            customer_stats[cid] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }
            
        customer_stats[cid]['total_spent'] += amount
        customer_stats[cid]['purchase_count'] += 1
        customer_stats[cid]['products_bought'].add(pname)
        
    # Finalize format
    result = {}
    for cid, stats in customer_stats.items():
        avg_value = stats['total_spent'] / stats['purchase_count'] if stats['purchase_count'] > 0 else 0
        result[cid] = {
            'total_spent': stats['total_spent'],
            'purchase_count': stats['purchase_count'],
            'avg_order_value': round(avg_value, 2),
            'products_bought': list(stats['products_bought']) 
        }
        
    # Sort by total_spent descending
    sorted_result = dict(sorted(result.items(), key=lambda item: item[1]['total_spent'], reverse=True))
    return sorted_result

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    Returns: dictionary sorted by date
    """
    daily_stats = {}
    
    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        cid = t['CustomerID']
        
        if date not in daily_stats:
            daily_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }
            
        daily_stats[date]['revenue'] += amount
        daily_stats[date]['transaction_count'] += 1
        daily_stats[date]['customers'].add(cid)
        
    # Format and Sort chronologically
    sorted_dates = sorted(daily_stats.keys())
    result = {}
    for date in sorted_dates:
        stats = daily_stats[date]
        result[date] = {
            'revenue': stats['revenue'],
            'transaction_count': stats['transaction_count'],
            'unique_customers': len(stats['customers'])
        }
        
    return result

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    Returns: tuple (date, revenue, transaction_count)
    """
    trend = daily_sales_trend(transactions)
    if not trend:
        return None
        
    peak_date = max(trend.items(), key=lambda x: x[1]['revenue'])
    date = peak_date[0]
    stats = peak_date[1]
    
    return (date, stats['revenue'], stats['transaction_count'])

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_stats = {}
    
    for t in transactions:
        pname = t['ProductName']
        qty = t['Quantity']
        amount = qty * t['UnitPrice']
        
        if pname not in product_stats:
            product_stats[pname] = {'qty': 0, 'revenue': 0.0}
            
        product_stats[pname]['qty'] += qty
        product_stats[pname]['revenue'] += amount
        
    # Filter and format
    low_performers = []
    for pname, stats in product_stats.items():
        if stats['qty'] < threshold:
            low_performers.append((pname, stats['qty'], stats['revenue']))
            
    # Sort by TotalQuantity ascending
    low_performers.sort(key=lambda x: x[1])
    
    return low_performers