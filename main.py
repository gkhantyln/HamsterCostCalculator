import tkinter as tk
from tkinter import ttk
import os

class HamsterKombatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hamster Kombat Cost Calculator")

        # Variables
        self.entries = []

        # Load existing data from file
        self.load_data()

        # Create filter and buttons
        self.create_filter_and_buttons()

        # Create table
        self.create_table()

        # Create sorting buttons
        self.create_sorting_buttons()

        # Populate table with loaded data
        self.update_table()

    def create_filter_and_buttons(self):
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=10)

        self.filter_entry = tk.Entry(filter_frame)
        self.filter_entry.pack(side=tk.LEFT, padx=5)

        filter_button = tk.Button(filter_frame, text="Filter", command=self.filter_by_card_name)
        filter_button.pack(side=tk.LEFT, padx=5)

        self.buttons = {
            "PR&Team": tk.Button(filter_frame, text="PR&Team", command=lambda: self.get_data("PR&Team")),
            "Markets": tk.Button(filter_frame, text="Markets", command=lambda: self.get_data("Markets")),
            "Legal": tk.Button(filter_frame, text="Legal", command=lambda: self.get_data("Legal")),
            "Specials": tk.Button(filter_frame, text="Specials", command=lambda: self.get_data("Specials")),
        }

        for button in self.buttons.values():
            button.pack(side=tk.LEFT, padx=5)

    def create_table(self):
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(pady=20)

        self.tree = ttk.Treeview(self.table_frame, columns=("category", "card_name", "cost_value", "hourly_profit", "card_value", "hourly24_value"), show="headings")
        self.tree.heading("category", text="Category")
        self.tree.heading("card_name", text="Card Name")
        self.tree.heading("cost_value", text="Cost Value")
        self.tree.heading("hourly_profit", text="Hourly Profit")
        self.tree.heading("card_value", text="Card Value")
        self.tree.heading("hourly24_value", text="1 Day")

        self.tree.bind("<Double-1>", self.on_item_double_click)

        self.tree.pack()

    def create_sorting_buttons(self):
        sort_frame = ttk.Frame(self.root)
        sort_frame.pack(pady=10)

        sort_buttons = {
            "Cost": tk.Button(sort_frame, text="Cost", command=lambda: self.sort_table("cost_value")),
            "Hourly": tk.Button(sort_frame, text="Hourly", command=lambda: self.sort_table("hourly_profit")),
            "Card": tk.Button(sort_frame, text="Card", command=lambda: self.sort_table("card_value")),
            "1 Day": tk.Button(sort_frame, text="1 Day", command=lambda: self.sort_table("hourly24_value")),
        }

        for button in sort_buttons.values():
            button.pack(side=tk.LEFT, padx=5)

    def get_data(self, category):
        data_window = tk.Toplevel(self.root)
        data_window.title(f"Enter Data for {category}")
        data_window.geometry("250x250")

        tk.Label(data_window, text="Card Name:").pack(pady=5)
        card_name_entry = tk.Entry(data_window)
        card_name_entry.pack(pady=5)

        tk.Label(data_window, text="Card Value:").pack(pady=5)
        coin_entry = tk.Entry(data_window)
        coin_entry.pack(pady=5)

        tk.Label(data_window, text="Hourly Profit:").pack(pady=5)
        profit_entry = tk.Entry(data_window)
        profit_entry.pack(pady=5)

        def submit_data():
            card_name = card_name_entry.get()
            coin = float(coin_entry.get())
            profit = float(profit_entry.get())
            cost = coin / profit
            hourly24_value = profit * 24

            self.entries.append((category, card_name, cost, profit, coin, hourly24_value))
            self.save_data()
            self.update_table()
            data_window.destroy()

        tk.Button(data_window, text="Submit", command=submit_data).pack(pady=10)

    def on_item_double_click(self, event):
        item_id = self.tree.selection()[0]
        item = self.tree.item(item_id)
        category, card_name, cost, profit, coin, hourly24_value = item['values']

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Entry")
        edit_window.geometry("250x350")

        tk.Label(edit_window, text="Category:").pack(pady=5)
        category_entry = tk.Entry(edit_window)
        category_entry.insert(0, category)
        category_entry.pack(pady=5)

        tk.Label(edit_window, text="Card Name:").pack(pady=5)
        card_name_entry = tk.Entry(edit_window)
        card_name_entry.insert(0, card_name)
        card_name_entry.pack(pady=5)

        tk.Label(edit_window, text="Card Value:").pack(pady=5)
        coin_entry = tk.Entry(edit_window)
        coin_entry.insert(0, coin)
        coin_entry.pack(pady=5)

        tk.Label(edit_window, text="Hourly Profit:").pack(pady=5)
        profit_entry = tk.Entry(edit_window)
        profit_entry.insert(0, profit)
        profit_entry.pack(pady=5)

        tk.Label(edit_window, text="Cost Value:").pack(pady=5)
        cost_entry = tk.Entry(edit_window)
        cost_entry.insert(0, cost)
        cost_entry.pack(pady=5)

        def calculate_cost(event=None):
            if coin_entry.get() and profit_entry.get():
                try:
                    coin = float(coin_entry.get())
                    profit = float(profit_entry.get())
                    calculated_cost = coin / profit
                    cost_entry.delete(0, tk.END)
                    cost_entry.insert(0, calculated_cost)
                except ValueError:
                    pass

        coin_entry.bind("<KeyRelease>", calculate_cost)
        profit_entry.bind("<KeyRelease>", calculate_cost)

        def submit_edit():
            new_category = category_entry.get()
            new_card_name = card_name_entry.get()
            new_coin = float(coin_entry.get())
            new_profit = float(profit_entry.get())
            new_cost = new_coin / new_profit
            new_hourly24_value = new_profit * 24

            for i, entry in enumerate(self.entries):
                if entry[1] == card_name:  # Find by card name
                    self.entries[i] = (new_category, new_card_name, new_cost, new_profit, new_coin, new_hourly24_value)
                    break

            self.save_data()
            self.update_table()
            edit_window.destroy()

        tk.Button(edit_window, text="Submit", command=submit_edit).pack(pady=10)

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, (category, card_name, cost, profit, coin, hourly24_value) in enumerate(self.entries):
            self.tree.insert("", "end", values=(category, card_name, f"{cost:.2f}", f"{profit:.2f}", f"{coin:.2f}", f"{hourly24_value:.2f}"))

    def save_data(self):
        with open("combats.txt", "w") as f:
            for entry in self.entries:
                f.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]},{entry[5]}\n")

    def load_data(self):
        if os.path.exists("combats.txt"):
            with open("combats.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 5:
                        category, card_name, cost, profit, coin = parts
                        hourly24_value = float(profit) * 24
                    else:
                        category, card_name, cost, profit, coin, hourly24_value = parts
                    self.entries.append((category, card_name, float(cost), float(profit), float(coin), float(hourly24_value)))

    def filter_by_card_name(self):
        filter_text = self.filter_entry.get().strip().lower()
        if filter_text:
            filtered_entries = [entry for entry in self.entries if filter_text in entry[1].lower()]
        else:
            filtered_entries = self.entries

        self.update_table_with_filtered_data(filtered_entries)

    def update_table_with_filtered_data(self, filtered_entries):
        for row in self.tree.get_children():
            self.tree.delete(row)

        sorted_entries = sorted(filtered_entries, key=lambda x: x[2])  # Sort by Cost Value
        for i, (category, card_name, cost, profit, coin, hourly24_value) in enumerate(sorted_entries):
            self.tree.insert("", "end", values=(category, card_name, f"{cost:.2f}", f"{profit:.2f}", f"{coin:.2f}", f"{hourly24_value:.2f}"))

    def sort_table(self, col):

        if col == "cost_value":
            self.entries.sort(key=lambda x: x[2])
        else:
            self.entries.sort(key=lambda x: x[{"category": 0, "card_name": 1, "hourly_profit": 3, "card_value": 4, "hourly24_value": 5}[col]], reverse=True)

        self.update_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = HamsterKombatApp(root)
    root.mainloop()
