from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions, validate_and_filter,
    calculate_total_revenue, region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend, find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products, create_product_mapping, 
    enrich_sales_data, save_enriched_data
)
from utils.report_generator import generate_sales_report
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
    
    # Task 1.3: Validate and Filter (Get Clean Data)
    print("\n--- Task 1.3: Validation ---")
    # We use the filtered list (without specific filters) as our valid dataset for analysis
    valid_transactions, invalid_count, summary = validate_and_filter(transactions)
    print(f"Valid transactions for analysis: {len(valid_transactions)}")
    
    if not valid_transactions:
        print("No valid transactions to analyze.")
        return

    # Task 3: API Integration & Enrichment
    print("\n--- Task 3: API Integration & Enrichment ---")
    
    enriched_transactions = []
    # 3.1 Fetch and Map
    api_products = fetch_all_products()
    if api_products:
        product_mapping = create_product_mapping(api_products)
        print(f"Created mapping for {len(product_mapping)} products.")
        
        # 3.2 Enrich
        print("Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        
        # Check match rate
        matches = sum(1 for t in enriched_transactions if t['API_Match'])
        print(f"Enriched {matches} out of {len(enriched_transactions)} transactions.")
        
        # Save
        save_enriched_data(enriched_transactions)
    else:
        print("Skipping enrichment due to API failure.")

    # Task 2.1: Sales Summary Calculator
    print("\n--- Task 2.1: Sales Summary Calculator ---")
    
    # a) Total Revenue
    total_revenue = calculate_total_revenue(valid_transactions)
    print(f"Total Revenue: {total_revenue:,.2f}")
    
    # b) Region-wise Sales
    print("\nRegion-wise Sales Analysis:")
    region_stats = region_wise_sales(valid_transactions)
    for region, stats in region_stats.items():
        print(f"  {region}: Sales={stats['total_sales']:,.2f}, Count={stats['transaction_count']}, Share={stats['percentage']}%")
        
    # c) Top Selling Products
    print("\nTop 5 Selling Products:")
    top_products = top_selling_products(valid_transactions, n=5)
    for prod in top_products:
        print(f"  {prod[0]}: Qty={prod[1]}, Revenue={prod[2]:,.2f}")
        
    # d) Customer Analysis (Top 3 for brevity)
    print("\nCustomer Purchase Analysis (Top 3):")
    cust_stats = customer_analysis(valid_transactions)
    for cid, stats in list(cust_stats.items())[:3]:
        print(f"  {cid}: Spent={stats['total_spent']:,.2f}, Orders={stats['purchase_count']}, Avg={stats['avg_order_value']:,.2f}")
        print(f"        Products: {stats['products_bought']}")

    # Task 2.2: Date-based Analysis
    print("\n--- Task 2.2: Date-based Analysis ---")
    
    # a) Daily Sales Trend
    print("Daily Sales Trend:")
    daily_stats = daily_sales_trend(valid_transactions)
    for date, stats in daily_stats.items():
        print(f"  {date}: Revenue={stats['revenue']:,.2f}, Tx={stats['transaction_count']}, Cust={stats['unique_customers']}")
        
    # b) Peak Sales Day
    peak_day = find_peak_sales_day(valid_transactions)
    if peak_day:
        print(f"\nPeak Sales Day: {peak_day[0]} (Revenue: {peak_day[1]:,.2f}, Tx: {peak_day[2]})")

    # Task 2.3: Product Performance
    print("\n--- Task 2.3: Product Performance ---")
    
    # a) Low Performing Products (Threshold=5 for demo)
    threshold = 5
    print(f"Low Performing Products (Qty < {threshold}):")
    low_performers = low_performing_products(valid_transactions, threshold=threshold)
    if low_performers:
        for prod in low_performers:
            print(f"  {prod[0]}: Qty={prod[1]}, Revenue={prod[2]:,.2f}")
    else:
        print("  No products found below threshold.")

    # Task 4.1: Generate Sales Report
    print("\n--- Task 4.1: Generating Report ---")
    generate_sales_report(valid_transactions, enriched_transactions)

if __name__ == "__main__":
    main()