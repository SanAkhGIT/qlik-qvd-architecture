"""Validate the synthetic source extracts before Qlik ingestion."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sample"


def read(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    customers = read("customers.csv")
    products = read("products.csv")
    orders = read("orders.csv")

    assert len(customers) == 8, "Expected 8 customers"
    assert len(products) == 8, "Expected 8 products"
    assert len(orders) == 100, "Expected 100 synthetic orders"

    customer_ids = {row["CustomerID"] for row in customers}
    product_ids = {row["ProductID"] for row in products}
    order_ids = [row["OrderID"] for row in orders]

    assert len(customer_ids) == len(customers), "Duplicate customer keys"
    assert len(product_ids) == len(products), "Duplicate product keys"
    assert len(order_ids) == len(set(order_ids)), "Duplicate order keys"
    assert all(row["CustomerID"] in customer_ids for row in orders), "Orphan customer reference"
    assert all(row["ProductID"] in product_ids for row in orders), "Orphan product reference"

    for row in orders:
        order_date = date.fromisoformat(row["OrderDate"])
        modified_date = date.fromisoformat(row["ModifiedDate"])
        quantity = int(row["Quantity"])
        discount = float(row["Discount"])
        sales = float(row["SalesAmount"])

        assert modified_date >= order_date, f"ModifiedDate precedes OrderDate: {row['OrderID']}"
        assert 1 <= quantity <= 5, f"Invalid quantity: {row['OrderID']}"
        assert 0 <= discount <= 0.15, f"Invalid discount: {row['OrderID']}"
        assert sales >= 0, f"Invalid sales amount: {row['OrderID']}"

    print(f"PASS: {len(customers)} customers, {len(products)} products, {len(orders)} orders")


if __name__ == "__main__":
    main()
