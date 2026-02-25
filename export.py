import csv

def export_to_csv(expenses, filepath):
    """Eksportē izdevumus CSV failā ar Excel saderīgu kodējumu."""
    # utf-8-sig nodrošina, ka latviskie burti Excelī rādīsies pareizi
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        # Ierakstām kolonnu nosaukumus
        writer.writerow(["Datums", "Summa", "Kategorija", "Apraksts"])
        
        # Cikls cauri visiem sarakstā esošajiem izdevumiem
        for expense in expenses:
            writer.writerow([
                expense["date"],
                f"{expense['amount']:.2f}",
                expense["category"],
                expense["description"]
            ])