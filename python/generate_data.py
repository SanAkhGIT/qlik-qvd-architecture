"""Generate synthetic source data for the Qlik QVD Architecture Lab."""
from __future__ import annotations
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "sample"
OUT.mkdir(parents=True, exist_ok=True)

customers = [
    [f"C{i:04d}", f"Customer {i:04d}", region, "India", segment]
    for i, (region, segment) in enumerate([
        ("West", "Consumer"), ("North", "Corporate"), ("South", "Consumer"),
        ("East", "Small Business"), ("West", "Corporate"), ("North", "Consumer"),
        ("South", "Corporate"), ("East", "Consumer")], 1)
]
products = [
    ["P001", "Laptop Pro 14", "Computers", "Laptops", 95000],
    ["P002", "Laptop Air 13", "Computers", "Laptops", 72000],
    ["P003", "Office Monitor 27", "Computers", "Monitors", 24000],
    ["P004", "Wireless Keyboard", "Accessories", "Keyboards", 3500],
    ["P005", "Wireless Mouse", "Accessories", "Mice", 1800],
    ["P006", "USB-C Dock", "Accessories", "Docks", 8500],
    ["P007", "Noise Cancelling Headset", "Audio", "Headsets", 12500],
    ["P008", "Webcam HD", "Audio", "Webcams", 4500],
]

orders = []
start = date(2026, 1, 1)
for i in range(1, 501):
    d = start + timedelta(days=random.randint(0, 241))
    product = random.choice(products)
    qty = random.randint(1, 5)
    discount = random.choice([0, 0, 0.05, 0.10, 0.15])
    sales = round(product[4] * qty * (1 - discount), 2)
    customer = random.choice(customers)
    orders.append([f"O{i:06d}", d.isoformat(), customer[0], product[0], qty, discount, sales, d.isoformat()])


def write_csv(filename, headers, rows):
    with (OUT / filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

write_csv("customers.csv", ["CustomerID", "CustomerName", "Region", "Country", "Segment"], customers)
write_csv("products.csv", ["ProductID", "ProductName", "Category", "Subcategory", "UnitPrice"], products)
write_csv("orders.csv", ["OrderID", "OrderDate", "CustomerID", "ProductID", "Quantity", "Discount", "SalesAmount", "ModifiedDate"], orders)
print(f"Generated {len(customers)} customers, {len(products)} products and {len(orders)} orders in {OUT}")
