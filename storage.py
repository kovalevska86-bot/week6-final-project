import json
import os

FILENAME = "expenses.json"

def load_expenses():
    """Nolasa expenses.json; ja fails neeksistē, atgriež tukšu sarakstu."""
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as f:
        return json.load(f)

def save_expenses(expenses):
    """Saglabā sarakstu JSON failā ar ensure_ascii=False."""
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=4, ensure_ascii=False)