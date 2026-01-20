import os
from datetime import datetime
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # 1. HEADER
        f.write("=" * 44 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {len(transactions)}\n")
        f.write("=" * 44 + "\n\n")
        
        # 2. OVERALL SUMMARY
        total_revenue = calculate_total_revenue(transactions)
        total_tx = len(transactions)
        avg_order_value = total_revenue / total_tx if total_tx > 0 else 0
        
        dates = [t['Date'] for t in transactions if t.get('Date')]
        if dates:
            date_range = f"{min(dates)} to {max(dates)}"
        else:
            date_range = "N/A"
            
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 15 + "\n")
        f.write(f"Total Revenue:       {total_revenue:,.2f}\n")
        f.write(f"Total Transactions:  {total_tx}\n")
        f.write(f"Average Order Value: {avg_order_value:,.2f}\n")
        f.write(f"Date Range:          {date_range}\n\n")
        
        # 3. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write(f"{'Region':<15} {'Sales':<15} {'% of Total':<15} {'Transactions':<15}\n")
        f.write("-" * 60 + "\n")
        region_stats = region_wise_sales(transactions)
        # Sort by sales amount descending
        sorted_regions = sorted(region_stats.items(), key=lambda x: x[1]['total_sales'], reverse=True)
        
        for region, stats in sorted_regions:
            pct_str = f"{stats['percentage']:.2f}%"
            f.write(f"{region:<15} {stats['total_sales']:<15,.2f} {pct_str:<15} {stats['transaction_count']:<15}\n")
        f.write("\n")
        
        # 4. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write(f"{'Rank':<5} {'Product Name':<30} {'Quantity':<10} {'Revenue':<15}\n")
        f.write("-" * 60 + "\n")
        top_prods = top_selling_products(transactions, n=5)
        for i, (name, qty, rev) in enumerate(top_prods, 1):
             f.write(f"{i:<5} {name:<30} {qty:<10} {rev:<15,.2f}\n")
        f.write("\n")

        # 5. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write(f"{'Rank':<5} {'Customer ID':<15} {'Total Spent':<15} {'Orders':<10}\n")
        f.write("-" * 50 + "\n")
        cust_stats = customer_analysis(transactions)
        # Sort by total_spent
        sorted_cust = sorted(cust_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True)[:5]
        for i, (cid, stats) in enumerate(sorted_cust, 1):
            f.write(f"{i:<5} {cid:<15} {stats['total_spent']:<15,.2f} {stats['purchase_count']:<10}\n")
        f.write("\n")
        
        # 6. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write(f"{'Date':<15} {'Revenue':<15} {'Transactions':<15} {'Unique Customers':<20}\n")
        f.write("-" * 65 + "\n")
        daily_stats = daily_sales_trend(transactions)
        # Sort by date
        sorted_days = sorted(daily_stats.items())
        for date, stats in sorted_days:
            f.write(f"{date:<15} {stats['revenue']:<15,.2f} {stats['transaction_count']:<15} {stats['unique_customers']:<20}\n")
        f.write("\n")
        
        # 7. PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        peak_day = find_peak_sales_day(transactions)
        if peak_day:
             f.write(f"Best Selling Day: {peak_day[0]} (Revenue: {peak_day[1]:,.2f})\n")
        else:
             f.write("Best Selling Day: N/A\n")
             
        low_performers = low_performing_products(transactions, threshold=5) # Assuming threshold 5 as per previous steps
        if low_performers:
            lp_names = ", ".join([p[0] for p in low_performers])
            f.write(f"Low Performing Products: {lp_names}\n")
        else:
            f.write("Low Performing Products: None\n")
            
        f.write("Average Transaction Value per Region:\n")
        for region, stats in sorted_regions:
            avg_val = stats['total_sales'] / stats['transaction_count'] if stats['transaction_count'] > 0 else 0
            f.write(f"  - {region}: {avg_val:,.2f}\n")
        f.write("\n")
        
        # 8. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        total_enriched_tx = len(enriched_transactions)
        matched_tx = [t for t in enriched_transactions if t.get('API_Match')]
        match_count = len(matched_tx)
        success_rate = (match_count / total_enriched_tx * 100) if total_enriched_tx > 0 else 0
        
        f.write(f"Total Products Enriched: {match_count}\n") # Using match count as proxy for products enriched in context of transactions
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        
        # List of products that couldn't be enriched
        # Identify ProductNames where API_Match is False
        unmatched_products = set()
        for t in enriched_transactions:
            if not t.get('API_Match'):
                unmatched_products.add(t.get('ProductName', 'Unknown'))
        
        if unmatched_products:
            f.write("Products that couldn't be enriched:\n")
            for p in unmatched_products:
                f.write(f"  - {p}\n")
        else:
            f.write("All products successfully enriched.\n")

    print(f"Report generated successfully at {output_file}")