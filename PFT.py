import os
import json
from datetime import datetime
from collections import defaultdict

# File to store data
FILENAME = "finance_data.json"

# Load transactions from file
def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return []

# Save transactions to file
def save_data(transactions):
    with open(FILENAME, "w") as f:
        json.dump(transactions, f, indent=4)

# Add transaction
def add_transaction(transactions):
    t_type = input("Enter type (income/expense): ").lower()
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))
    date = input("Enter date (dd-mm-yyyy): ")

    transaction = {
        "id": len(transactions) + 1,
        "type": t_type,
        "category": category,
        "amount": amount,
        "date": date
    }
    transactions.append(transaction)
    print("✅ Transaction added successfully!")

# Display transactions
def view_transactions(transactions):
    if not transactions:
        print("No transactions found.")
        return
    print("\nID   Type      Category     Amount     Date")
    print("--------------------------------------------------")
    for t in transactions:
        print(f"{t['id']: <4} {t['type']: <9} {t['category']: <12} {t['amount']: <9} {t['date']}")

# Sort transactions
def sort_transactions(transactions):
    choice = input("Sort by (amount/date): ").lower()
    if choice == "amount":
        transactions.sort(key=lambda x: x['amount'])
    elif choice == "date":
        transactions.sort(key=lambda x: datetime.strptime(x['date'], "%d-%m-%Y"))
    print("✅ Transactions sorted.")

# Search transactions
def search_transactions(transactions):
    keyword = input("Enter category/type to search: ").lower()
    results = [t for t in transactions if keyword in t['category'].lower() or keyword in t['type']]
    view_transactions(results)

# Filter transactions
def filter_transactions(transactions):
    threshold = float(input("Show expenses greater than: "))
    results = [t for t in transactions if t['type'] == "expense" and t['amount'] > threshold]
    view_transactions(results)

# Savings goal
def savings_goal(transactions):
    goal = float(input("Enter your savings goal: "))
    income = sum(t['amount'] for t in transactions if t['type'] == "income")
    expenses = sum(t['amount'] for t in transactions if t['type'] == "expense")
    savings = income - expenses

    print(f"\n💰 Income: {income}")
    print(f"💸 Expenses: {expenses}")
    print(f"📊 Savings: {savings}")
    if savings >= goal:
        print("🎉 Goal achieved!")
    else:
        print(f"⚠️ You need {goal - savings} more to reach your goal.")

# ASCII bar chart
def spending_chart(transactions):
    monthly_expenses = defaultdict(float)
    for t in transactions:
        if t['type'] == "expense":
            month = datetime.strptime(t['date'], "%d-%m-%Y").strftime("%B")
            monthly_expenses[month] += t['amount']

    print("\n📊 Monthly Spending Chart:")
    for month, amount in monthly_expenses.items():
        stars = "*" * int(amount // 100)  # each * = 100
        print(f"{month: <10} | {stars} ({amount})")

# Main program
def main():
    transactions = load_data()

    while True:
        print("\n==== Personal Finance Tracker ====")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. Sort Transactions")
        print("4. Search Transactions")
        print("5. Filter Transactions")
        print("6. Set/View Savings Goal")
        print("7. Show Monthly Spending Chart")
        print("8. Save & Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            sort_transactions(transactions)
        elif choice == "4":
            search_transactions(transactions)
        elif choice == "5":
            filter_transactions(transactions)
        elif choice == "6":
            savings_goal(transactions)
        elif choice == "7":
            spending_chart(transactions)
        elif choice == "8":
            save_data(transactions)
            print("💾 Data saved. Exiting...")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
