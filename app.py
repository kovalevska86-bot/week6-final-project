import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date # Pievienots datetime validācijai
import storage
import logic
import export 

CATEGORIES = ["Ediens", "Transports", "Izklaide", "Komunālie maksājumi", "Veselība", "Iepirkšanās", "Cits"]

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Izdevumu izsekotājs")
        self.root.geometry("750x700")
        
        self.expenses = storage.load_expenses()
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # 1. Ievades sekcija
        input_frame = tk.LabelFrame(self.root, text="Pievienot izdevumu", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Datums (GGGG-MM-DD):").grid(row=0, column=0, sticky="w")
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=1, pady=2)

        tk.Label(input_frame, text="Summa:").grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, pady=2)

        tk.Label(input_frame, text="Kategorija:").grid(row=2, column=0, sticky="w")
        self.cat_var = tk.StringVar(value=CATEGORIES[0])
        tk.OptionMenu(input_frame, self.cat_var, *CATEGORIES).grid(row=2, column=1, sticky="w")

        tk.Label(input_frame, text="Apraksts:").grid(row=3, column=0, sticky="w")
        self.desc_entry = tk.Entry(input_frame)
        self.desc_entry.grid(row=3, column=1, pady=2)

        tk.Button(input_frame, text="Pievienot izdevumu", command=self.add_expense_action, bg="lightgreen", font=("Arial", 10, "bold")).grid(row=4, columnspan=2, pady=10)

        # 2. Filtrs un Eksports
        action_frame = tk.Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(action_frame, text="Filtrēt pēc mēneša:").pack(side="left")
        self.filter_var = tk.StringVar(value="Visi")
        
        self.filter_container = tk.Frame(action_frame)
        self.filter_container.pack(side="left", padx=5)
        self.update_filter_options()

        tk.Button(action_frame, text="Eksportēt uz CSV", command=self.export_action).pack(side="right")
        
        # 3. Tabula
        self.tree = ttk.Treeview(self.root, columns=("date", "amount", "category", "desc"), show="headings")
        self.tree.heading("date", text="Datums")
        self.tree.column("date", width=100, anchor="center")
        self.tree.heading("amount", text="Summa (EUR)")
        self.tree.column("amount", width=100, anchor="e")
        self.tree.heading("category", text="Kategorija")
        self.tree.column("category", width=120, anchor="w")
        self.tree.heading("desc", text="Apraksts")
        self.tree.column("desc", width=300, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10)
        
        # 4. Kopsavilkums
        self.summary_label = tk.Label(self.root, text="KOPĀ: 0.00 EUR", font=("Arial", 12, "bold"), fg="blue")
        self.summary_label.pack(pady=10)

    def update_filter_options(self):
        months = ["Visi"] + logic.get_available_months(self.expenses)
        if hasattr(self, 'filter_menu'):
            self.filter_menu.destroy()
        self.filter_menu = tk.OptionMenu(self.filter_container, self.filter_var, *months, command=lambda _: self.refresh_table())
        self.filter_menu.pack(side="left")

    def add_expense_action(self):
        # Iegūstam datus un notīrām liekās atstarpes
        d = self.date_entry.get().strip()
        a = self.amount_entry.get().strip()
        c = self.cat_var.get()
        desc = self.desc_entry.get().strip()

        # VALIDĀCIJA (Svarīgi 3 punktiem)
        if not d or not a or not desc:
            messagebox.showwarning("Brīdinājums", "Visi lauki ir obligāti!")
            return

        try:
            # 1. Datuma validācija
            datetime.strptime(d, "%Y-%m-%d")
            
            # 2. Summas validācija
            amount = float(a)
            if amount <= 0:
                messagebox.showerror("Kļūda", "Summai jābūt lielākai par 0!")
                return
            
            new_exp = {
                "date": d,
                "amount": amount,
                "category": c,
                "description": desc
            }
            
            self.expenses.append(new_exp)
            storage.save_expenses(self.expenses)
            self.refresh_table()
            self.update_filter_options()
            
            # Notīrām laukus pēc veiksmīgas pievienošanas
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Izdevums pievienots!")
            
        except ValueError:
            messagebox.showerror("Kļūda", "Nepareizs formāts!\nDatums: GGGG-MM-DD\nSumma: skaitlis (piem. 10.50)")

    def export_action(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV faili", "*.csv")],
            initialfile=f"izdevumi_{date.today()}.csv"
        )
        if filepath:
            display_list = self.get_filtered_data()
            if not display_list:
                messagebox.showwarning("Eksports", "Nav datu, ko eksportēt!")
                return
            export.export_to_csv(display_list, filepath)
            messagebox.showinfo("Eksports", "Dati veiksmīgi eksportēti!")

    def get_filtered_data(self):
        selected_month = self.filter_var.get()
        if selected_month == "Visi":
            return self.expenses
        y, m = selected_month.split("-")
        return logic.filter_by_month(self.expenses, y, m)

    def refresh_table(self):
        # Notīrām vecos datus no tabulas
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Iegūstam filtrētos datus (vai visus)
        display_list = self.get_filtered_data()
            
        for exp in display_list:
            # Šeit notiek formatēšana: f"{exp['amount']:.2f}" 
            # pārvērš 20 par 20.00 un 15.5 par 15.50
            formatted_amount = f"{exp['amount']:.2f}"
            
            self.tree.insert("", "end", values=(
                exp["date"], 
                formatted_amount, 
                exp["category"], 
                exp["description"]
            ))
            
        # Atjaunojam kopsummu loga apakšā
        total = logic.sum_total(display_list)
        self.summary_label.config(text=f"KOPĀ: {total:.2f} EUR")

if __name__ == "__main__":
    app_root = tk.Tk()
    ExpenseApp(app_root)
    app_root.mainloop()