import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

DATA_FOLDER = "data"
EXPENSE_FILE = os.path.join(DATA_FOLDER, "expenses.csv")
BUDGET_FILE = os.path.join(DATA_FOLDER, "budget.csv")

def ensure_files_exist():
    os.makedirs(DATA_FOLDER, exist_ok=True)

    if not os.path.exists(EXPENSE_FILE):
        pd.DataFrame(columns=["Date", "Category", "Amount", "Note"]).to_csv(EXPENSE_FILE, index=False)

    if not os.path.exists(BUDGET_FILE):
        pd.DataFrame(columns=["Category", "Budget"]).to_csv(BUDGET_FILE, index=False)

def load_expenses():
    return pd.read_csv(EXPENSE_FILE, parse_dates=["Date"])

def load_budgets():
    return pd.read_csv(BUDGET_FILE)

def log_expense():
    date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    date = pd.to_datetime(date_input) if date_input else pd.to_datetime("today")
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))
    note = input("Optional note: ")

    new_expense = pd.DataFrame([[date, category, amount, note]], columns=["Date", "Category", "Amount", "Note"])
    df = pd.concat([load_expenses(), new_expense], ignore_index=True)
    df.to_csv(EXPENSE_FILE, index=False)
    print("Expense logged successfully.")

def set_budget():
    category = input("Enter category to set/update budget: ")
    amount = float(input("Enter monthly budget amount: "))
    budgets = load_budgets()

    if category in budgets["Category"].values:
        budgets.loc[budgets["Category"] == category, "Budget"] = amount
    else:
        budgets = pd.concat([budgets, pd.DataFrame([[category, amount]], columns=["Category", "Budget"])], ignore_index=True)

    budgets.to_csv(BUDGET_FILE, index=False)
    print("Budget saved.")

def show_monthly_summary():
    df = load_expenses()
    if df.empty:
        print("No expenses found.")
        return

    df["Month"] = df["Date"].dt.to_period("M")
    summary = df.groupby(["Month", "Category"])["Amount"].sum().unstack(fill_value=0)
    print("\n--- Monthly Expense Summary ---")
    print(summary)

    budgets = load_budgets().set_index("Category")["Budget"]
    total_per_category = df.groupby("Category")["Amount"].sum()

    print("\n--- Budget Comparison ---")
    for cat, total in total_per_category.items():
        budget = budgets.get(cat, None)
        if budget is not None:
            if total > budget:
                print(f"⚠️ Over budget in {cat}: ₹{total:.2f} / ₹{budget:.2f}")
            else:
                print(f"{cat}: ₹{total:.2f} / ₹{budget:.2f}")
        else:
            print(f"{cat}: ₹{total:.2f} (no budget set)")

def show_weekly_summary():
    df = load_expenses()
    if df.empty:
        print("No expenses found.")
        return

    df["Week"] = df["Date"].dt.strftime("Week %U")
    summary = df.groupby(["Week", "Category"])["Amount"].sum().unstack(fill_value=0)
    print("\n--- Weekly Expense Summary ---")
    print(summary)

def visualize_spending():
    df = load_expenses()
    if df.empty:
        print("No expenses to show.")
        return

    category_totals = df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(8, 6))
    category_totals.plot(kind="pie", autopct="%1.1f%%", startangle=140)
    plt.title("Spending by Category")
    plt.ylabel("")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

def export_data():
    print(f"Data exported to:\n- {EXPENSE_FILE}\n- {BUDGET_FILE}")

def main():
    ensure_files_exist()
    while True:
        print("\nExpense Tracker Menu")
        print("1. Log Expense")
        print("2. Set Budget")
        print("3. View Monthly Summary")
        print("4. View Weekly Summary")
        print("5. Visualize Spending")
        print("6. Export Data")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            log_expense()
        elif choice == "2":
            set_budget()
        elif choice == "3":
            show_monthly_summary()
        elif choice == "4":
            show_weekly_summary()
        elif choice == "5":
            visualize_spending()
        elif choice == "6":
            export_data()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
