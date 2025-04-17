import csv
from datetime import datetime

# === Balance Handling ===
def get_balance():
    try:
        with open('balance.txt', 'r') as f:
            return float(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0.0

def set_balance(new_balance):
    with open('balance.txt', 'w') as f:
        f.write(f"{new_balance:.2f}")

def add_funds(amount):
    try:
        amount = float(amount)
        current_balance = get_balance()
        set_balance(current_balance + amount)
    except ValueError:
        raise ValueError("Amount must be a number.")

# === Expense Logging ===
def expense(amount, category, date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    try:
        amount = float(amount)
    except ValueError:
        raise ValueError("Amount must be a number.")

    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Date must be in 'YYYY-MM-DD' format.")

    with open('expenses.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])

    current_balance = get_balance()
    set_balance(current_balance - amount)

# === Debt Management ===
def add_debt(name, amount, reason, date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    try:
        amount = float(amount)
    except ValueError:
        raise ValueError("Amount must be a number.")

    with open('debts.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, amount, reason, date])

def view_debts():
    try:
        with open('debts.csv', newline='') as file:
            reader = csv.reader(file)
            print("\nWho        | Amount   | Reason        | Date")
            print("-----------------------------------------------")
            for row in reader:
                print(f"{row[0]:<10} | ${float(row[1]):<8.2f} | {row[2]:<13} | {row[3]}")
    except FileNotFoundError:
        print("[!] No debts found.")

# === Personal Debt List ===
def add_personal_debt(name, total_amount, description="", due_date=None):
    if due_date is None:
        due_date = datetime.now().strftime('%Y-%m-%d')
    try:
        total_amount = float(total_amount)
    except ValueError:
        raise ValueError("Amount must be a number.")

    with open('my_debts.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, total_amount, description, due_date, 0.0])

def view_personal_debts():
    try:
        with open('my_debts.csv', newline='') as file:
            reader = csv.reader(file)
            print("\nDebt       | Owed     | Paid     | Due       | Notes")
            print("------------------------------------------------------------")
            for row in reader:
                owed = float(row[1])
                paid = float(row[4])
                print(f"{row[0]:<10} | ${owed:<8.2f} | ${paid:<8.2f} | {row[3]} | {row[2]}")
    except FileNotFoundError:
        print("[!] No personal debts found.")

def make_debt_payment(name, payment_amount):
    updated_rows = []
    found = False

    try:
        with open('my_debts.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == name:
                    found = True
                    paid_so_far = float(row[4])
                    new_paid = paid_so_far + float(payment_amount)
                    row[4] = str(new_paid)
                updated_rows.append(row)
    except FileNotFoundError:
        print("[!] Debt file not found.")
        return

    if not found:
        print("[!] Debt not found.")
        return

    with open('my_debts.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)
    print("[✓] Payment logged.")

# === Main CLI Interface ===
def main():
    print("\nWelcome to the Personal Expense Tracker!")

    while True:
        print("\nChoose an option:")
        print("1. Add personal debt")
        print("2. View personal debts")
        print("3. Make a personal debt payment")
        print("4. Add general debt")
        print("5. View general debts")
        print("6. Log an expense")
        print("7. Add funds")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            print("Type 'exit' to cancel.")
            name = input("Debt name: ")
            if name.lower() == 'exit': continue
            amount = input("Amount owed: ")
            if amount.lower() == 'exit': continue
            description = input("Description: ")
            if description.lower() == 'exit': continue
            due_date = input("Due date (YYYY-MM-DD): ")
            if due_date.lower() == 'exit': continue

            try:
                add_personal_debt(name, amount, description, due_date)
            except ValueError as e:
                print(f"[!] Error: {e}")

        elif choice == '2':
            view_personal_debts()

        elif choice == '3':
            print("Type 'exit' to cancel.")
            name = input("Debt name: ")
            if name.lower() == 'exit': continue
            payment = input("Payment amount: ")
            if payment.lower() == 'exit': continue
            try:
                make_debt_payment(name, payment)
            except ValueError:
                print("[!] Invalid amount.")

        elif choice == '4':
            print("Type 'exit' to cancel.")
            name = input("Who do you owe or who owes you? ")
            if name.lower() == 'exit': continue
            amount = input("Amount: ")
            if amount.lower() == 'exit': continue
            reason = input("Reason: ")
            if reason.lower() == 'exit': continue
            date = input("Date (YYYY-MM-DD): ")
            if date.lower() == 'exit': continue

            try:
                add_debt(name, amount, reason, date)
            except ValueError as e:
                print(f"[!] Error: {e}")

        elif choice == '5':
            view_debts()

        elif choice == '6':
            print("Type 'exit' to cancel.")
            category = input("Category: ")
            if category.lower() == 'exit': continue
            amount = input("Amount: ")
            if amount.lower() == 'exit': continue
            date = input("Date (YYYY-MM-DD) [leave blank for today]: ")
            if date.lower() == 'exit': continue

            try:
                expense(amount, category, date if date else None)
            except ValueError as e:
                print(f"[!] Error: {e}")

        elif choice == '7':
            print("Type 'exit' to cancel.")
            amount = input("Amount to add to balance: ")
            if amount.lower() == 'exit': continue

            try:
                add_funds(amount)
                print("[✓] Funds added.")
            except ValueError as e:
                print(f"[!] Error: {e}")

        elif choice == '8':
            print("Goodbye!")
            break

        else:
            print("[!] Invalid option.")

if __name__ == "__main__":
    main()
