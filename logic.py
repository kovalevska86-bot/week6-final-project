from datetime import datetime

def sum_total(expenses):
    """Aprēķina visu izdevumu kopējo summu un noapaļo līdz 2 zīmēm."""
    total = sum(expense["amount"] for expense in expenses)
    return round(total, 2)

def filter_by_month(expenses, year, month):
    """Atgriež izdevumus, kuru datums ir norādītajā mēnesī."""
    result = []
    for expense in expenses:
        try:
            # Parsējam datumu no teksta formāta "YYYY-MM-DD"
            d = datetime.strptime(expense["date"], "%Y-%m-%d")
            if d.year == int(year) and d.month == int(month):
                result.append(expense)
        except (ValueError, KeyError):
            # Ja datums ir kļūdains, mēs šo ierakstu vienkārši izlaižam
            continue
    return result

def get_available_months(expenses):
    """Atgriež unikālo mēnešu sarakstu formātā 'YYYY-MM'."""
    months = set()
    for expense in expenses:
        # Paņemam pirmos 7 simbolus (piemēram, "2026-02")
        if "date" in expense and len(expense["date"]) >= 7:
            months.add(expense["date"][:7])
    
    # Sakārtojam no jaunākā uz vecāko
    return sorted(list(months), reverse=True)

def sum_by_category(expenses):
    """Aprēķina kopsummas katrai kategorijai."""
    totals = {}
    for expense in expenses:
        cat = expense.get("category", "Cits")
        totals[cat] = totals.get(cat, 0) + expense.get("amount", 0)
    return {cat: round(total, 2) for cat, total in totals.items()}

# Testa bloks
if __name__ == "__main__":
    test_data = [
        {"date": "2026-02-15", "amount": 12.50, "category": "Ediens"},
        {"date": "2026-01-20", "amount": 5.00, "category": "Transports"}
    ]
    print(f"Kopā iztērēts: {sum_total(test_data)} EUR")
    print(f"Pieejamie mēneši: {get_available_months(test_data)}")