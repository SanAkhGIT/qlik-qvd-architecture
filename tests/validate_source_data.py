"""Lightweight validation for the synthetic source extracts.

Run from the repository root with: python tests/validate_source_data.py
"""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sample"


def read(name):
    with (DATA / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    customers = read("customers.csv")
    products = read("products.csv")
    orders = read("orders.csv")

    customer_ids = {r["CustomerID"] for r in customers}
    product_ids = {r["ProductID"] for r in products}
    order_ids = [r["OrderID"] for r in orders]

    assert customers and products and orders
    assert len(customer_ids) == len(customers), "Duplicate customer keys"
    assert len(product_ids) == len(products), "Duplicate product keys"
    assert len(order_ids) == len(set(order_ids)), "Duplicate order keys"
    assert all(r["CustomerID"] in customer_ids for r in orders), "Orphan customer reference"
    assert all(r["ProductID"] in product_ids for r in orders), "Orphan product reference"
    assert all(float(r["Quantity"]) > 0 for r in orders), "Invalid quantity"
    assert all(float(r["SalesAmount"]) >= 0 for r in orders), "Invalid sales amount"

    print(f"PASS: {len(customers)} customers, {len(products)} products, {len(orders)} orders")


if __name__ == "__main__":
    main()
