from datetime import datetime

def sum_total(expenses):
    """Aprēķina visu izdevumu kopējo summu."""
    return sum(expense["amount"] for expense in expenses)

def filter_by_month(expenses, year, month):
    """Atgriež izdevumus, kuru datums ir norādītajā mēnesī."""
    result = []
    for expense in expenses:
        # Parsējam datumu no teksta formāta "YYYY-MM-DD"
        d = datetime.strptime(expense["date"], "%Y-%m-%d")
        if d.year == int(year) and d.month == int(month):
            result.append(expense)
    return result

def sum_by_category(expenses):
    """Aprēķina kopsummas katrai kategorijai un atgriež vārdnīcu."""
    totals = {}
    for expense in expenses:
        cat = expense["category"]
        totals[cat] = totals.get(cat, 0) + expense["amount"]
    return {cat: round(total, 2) for cat, total in totals.items()}

def get_available_months(expenses):
    """Atgriež unikālo mēnešu sarakstu ["2025-01", "2025-02"]."""
    months = set()
    for expense in expenses:
        months.add(expense["date"][:7])
    return sorted(list(months), reverse=True)

# Testa bloks (kad laidīsi logic.py, terminālī parādīsies rezultāts)
if __name__ == "__main__":
    test_data = [
        {"date": "2025-02-15", "amount": 12.50, "category": "Ēdiens"},
        {"date": "2025-02-20", "amount": 5.00, "category": "Transports"}
    ]
    print("Kopā iztērēts:", sum_total(test_data))