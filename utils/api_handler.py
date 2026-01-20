import requests
import re
import os

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"
    try:
        print(f"Fetching products from {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        products = data.get('products', [])
        print(f"Successfully fetched {len(products)} products.")
        return products
    except requests.exceptions.RequestException as e:
        print(f"Error fetching products: {e}")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    Parameters: api_products from fetch_all_products()
    Returns: dictionary mapping product IDs to info
    """
    mapping = {}
    for p in api_products:
        pid = p.get('id')
        if pid is not None:
            mapping[pid] = {
                'title': p.get('title'),
                'category': p.get('category'),
                'brand': p.get('brand'),
                'rating': p.get('rating')
            }
    return mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()
    Returns: list of enriched transaction dictionaries
    """
    enriched = []
    for t in transactions:
        new_t = t.copy()
        
        # Extract numeric ID from ProductID (e.g., P101 -> 101)
        p_id_str = str(t.get('ProductID', ''))
        match = re.search(r'\d+', p_id_str)
        
        api_match = False
        if match:
            try:
                numeric_id = int(match.group())
                if numeric_id in product_mapping:
                    info = product_mapping[numeric_id]
                    new_t['API_Category'] = info['category']
                    new_t['API_Brand'] = info['brand']
                    new_t['API_Rating'] = info['rating']
                    api_match = True
            except ValueError:
                pass # Should not happen with re.search checking digits
        
        if not api_match:
             new_t['API_Category'] = None
             new_t['API_Brand'] = None
             new_t['API_Rating'] = None
        
        new_t['API_Match'] = api_match
        enriched.append(new_t)
    return enriched

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    """
    if not enriched_transactions:
        print("No enriched data to save.")
        return

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    headers = [
        'TransactionID', 'Date', 'ProductID', 'ProductName', 'Quantity', 
        'UnitPrice', 'CustomerID', 'Region', 
        'API_Category', 'API_Brand', 'API_Rating', 'API_Match'
    ]
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write Header
            f.write('|'.join(headers) + '\n')
            
            for t in enriched_transactions:
                row = []
                for h in headers:
                    val = t.get(h)
                    # Handle None and formatting
                    if val is None:
                        row.append('None')
                    else:
                        row.append(str(val))
                f.write('|'.join(row) + '\n')
        print(f"Successfully saved enriched data to {filename}")
    except IOError as e:
        print(f"Error saving file: {e}")