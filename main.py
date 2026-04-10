import csv
import os
from datetime import datetime


class ExpenseTracker:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self.fields = ["Date", "Category", "Amount", "Description"]
        self._initialize_file()

    def _initialize_file(self):
        """Internal method to ensure the file is ready."""
        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fields)
                writer.writeheader()

    def add_expense(self, category, amount, description):
        """Adds a new expense entry to the CSV file."""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.filename, mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fields)
                writer.writerow(
                    {
                        "Date": date,
                        "Category": category,
                        "Amount": f"{float(amount):.2f}",
                        "Description": description,
                    }
                )
            print("\n[✔] Expense added successfully!")
        except ValueError:
            print("\n[✘] Error: Amount must be a valid number.")

    def view_all_expenses(self):
        """Reads and displays all expenses from the CSV."""
        if not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0:
            print("\n[!] No records found.")
            return

        print("\n" + "=" * 60)
        print(f"{'Date':<20} | {'Category':<15} | {'Amount':<10} | {'Description'}")
        print("-" * 60)

        with open(self.filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(
                    f"{row['Date']:<20} | {row['Category']:<15} | ${row['Amount']:<9} | {row['Description']}"
                )
        print("=" * 60)

    def view_total_spending(self):
        """Calculates and displays the total sum of all expenses."""
        total = 0.0
        try:
            with open(self.filename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    total += float(row["Amount"])
            print(f"\n[💰] Total Expenses to date: ${total:.2f}")
        except (FileNotFoundError, ValueError):
            print("\n[!] No valid data to calculate total.")


def main_menu():
    tracker = ExpenseTracker()

    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Spending")
        print("4. Exit")

        choice = input("\nChoose an option (1-4): ")

        if choice == "1":
            category = input(
                "Enter category (e.g., Food, Transport, Rent): "
            ).capitalize()
            try:
                amount = float(input("Enter amount: "))
                description = input("Enter a short description: ")
                tracker.add_expense(category, amount, description)
            except ValueError:
                print("\n[✘] Invalid input. Amount must be a number.")

        elif choice == "2":
            tracker.view_all_expenses()

        elif choice == "3":
            tracker.view_total_spending()

        elif choice == "4":
            print("\nExiting... Goodbye!")
            break

        else:
            print("\n[✘] Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
