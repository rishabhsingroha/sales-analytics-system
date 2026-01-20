import os

file_path = "data/sales_data.txt"

# Read with latin-1 (as established)
try:
    with open(file_path, 'r', encoding='latin-1') as f:
        content = f.read()

    # Replace IDs to match API range (1-100)
    # P101 -> P1, P102 -> P2, etc.
    content = content.replace("P101", "P1")
    content = content.replace("P102", "P2")
    content = content.replace("P103", "P3")
    content = content.replace("P104", "P4")
    content = content.replace("P105", "P5")

    # Write back
    with open(file_path, 'w', encoding='latin-1') as f:
        f.write(content)

    print("Updated ProductIDs in data/sales_data.txt")
except Exception as e:
    print(f"Error: {e}")