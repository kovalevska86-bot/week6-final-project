import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import storage
import logic
import export  # Neaizmirsti izveidot export.py failu!

CATEGORIES = ["Ediens", "Transports", "Izklaide", "Komunālie maksājumi", "Veselība", "Iepirkšanās", "Cits"]

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Izdevumu izsekotājs")
        self.root.geometry("750x700") # Palielināts logs, lai viss ietilpst
        
        self.expenses = storage.load_expenses()
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # 1. Ievades sekcija
        input_frame = tk.LabelFrame(self.root, text="Pievienot izdevumu", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Datums:").grid(row=0, column=0)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Summa:").grid(row=1, column=0)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1)

        tk.Label(input_frame, text="Kategorija:").grid(row=2, column=0)
        self.cat_var = tk.StringVar(value=CATEGORIES[0])
        tk.OptionMenu(input_frame, self.cat_var, *CATEGORIES).grid(row=2, column=1, sticky="w")

        tk.Label(input_frame, text="Apraksts:").grid(row=3, column=0)
        self.desc_entry = tk.Entry(input_frame)
        self.desc_entry.grid(row=3, column=1)

        tk.Button(input_frame, text="Pievienot", command=self.add_expense_action, bg="lightgreen").grid(row=4, columnspan=2, pady=5)

        # 2. Filtrs un Eksports (Frame)
        action_frame = tk.Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(action_frame, text="Filtrēt pēc mēneša:").pack(side="left")
        self.filter_var = tk.StringVar(value="Visi")
        
        # Konteiners speciāli filtra dropdownam
        self.filter_container = tk.Frame(action_frame)
        self.filter_container.pack(side="left", padx=5)
        self.update_filter_options()

        # Eksporta poga (prasība #5 un #8) [cite: 210]
        tk.Button(action_frame, text="Eksportēt uz CSV", command=self.export_action).pack(side="right")
        
        # 3. Saraksta sekcija
        self.tree = ttk.Treeview(self.root, columns=("date", "amount", "category", "desc"), show="headings")
        
        self.tree.heading("date", text="Datums")
        self.tree.column("date", width=100, anchor="center")
        self.tree.heading("amount", text="Summa")
        self.tree.column("amount", width=80, anchor="e")
        self.tree.heading("category", text="Kategorija")
        self.tree.column("category", width=120, anchor="w")
        self.tree.heading("desc", text="Apraksts")
        self.tree.column("desc", width=300, anchor="w") # Platāks apraksts
        
        self.tree.pack(fill="both", expand=True, padx=10)
        
        # 4. Kopsavilkuma sekcija 
        self.summary_label = tk.Label(self.root, text="KOPĀ: 0.00 EUR", font=("Arial", 12, "bold"))
        self.summary_label.pack(pady=10)

    def update_filter_options(self):
        # Izlabots: vairs nav dubultā def un lietojam pareizo konteineru
        months = ["Visi"] + logic.get_available_months(self.expenses)
        
        if hasattr(self, 'filter_menu'):
            self.filter_menu.destroy()
            
        self.filter_menu = tk.OptionMenu(self.filter_container, self.filter_var, *months, command=lambda _: self.refresh_table())
        self.filter_menu.pack(side="left")

    def add_expense_action(self):
        try:
            new_exp = {
                "date": self.date_entry.get(),
                "amount": float(self.amount_entry.get()),
                "category": self.cat_var.get(),
                "description": self.desc_entry.get()
            }
            self.expenses.append(new_exp)
            storage.save_expenses(self.expenses)
            self.refresh_table()
            self.update_filter_options()
            messagebox.showinfo("Success", "Izdevums pievienots!")
        except ValueError:
            messagebox.showerror("Kļūda", "Ievadiet derīgu skaitli summas laukā!")

    def export_action(self):
        # Lieto filedialog saskaņā ar prasību #8 [cite: 210]
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV faili", "*.csv"), ("Visi faili", "*.*")],
            initialfile="izdevumi.csv"
        )
        if filepath:
            # Eksportējam tos datus, kas šobrīd ir redzami (filtrētos) [cite: 219]
            display_list = self.get_filtered_data()
            export.export_to_csv(display_list, filepath)
            messagebox.showinfo("Eksports", "Dati veiksmīgi eksportēti!")

    def get_filtered_data(self):
        selected_month = self.filter_var.get()
        if selected_month == "Visi":
            return self.expenses
        y, m = selected_month.split("-")
        return logic.filter_by_month(self.expenses, y, m)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        display_list = self.get_filtered_data()
            
        for exp in display_list:
            self.tree.insert("", "end", values=(exp["date"], f"{exp['amount']:.2f}", exp["category"], exp["description"]))
            
        total = logic.sum_total(display_list)
        self.summary_label.config(text=f"KOPĀ: {total:.2f} EUR")

if __name__ == "__main__":
    app_root = tk.Tk()
    ExpenseApp(app_root)
    app_root.mainloop()