import sys
from app.models import BudgetVault, Bill
from app.calculator import format_currency, get_budget_status
from app.engine import run_budget_analysis, flat_tax_logic
from app.storage.json_storage import JSONStorage

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'


def print_success(message: str):
    print(f"{Colors.GREEN}{message}{Colors.RESET}")


def print_error(message: str):
    print(f"{Colors.RED}ERROR: {message}{Colors.RESET}")


def print_warning(message: str):
    print(f"{Colors.YELLOW}WARNING: {message}{Colors.RESET}")


def print_info(message: str):
    print(f"{Colors.BLUE}{message}{Colors.RESET}")


def display_banner():
    print(f"\n{Colors.CYAN}{Colors.BOLD}")
    print("")
    print("TRUCKER BUDGET MANAGER. ")
    print("")
    print(f"{Colors.RESET}")


def display_menu():
    print(f"\n{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print("1. Set Monthly Salary")
    print("2. Add Bill")
    print("3. View Bills")
    print("4. Update Bill")
    print("5. Delete Bill")
    print("6. View Budget Summary")
    print("7. Save & Exit")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}")

def validate_positive_number(prompt: str):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print_error("Value must be greater than zero.")
                continue
            return value
        except ValueError:
            print_error("Please enter a valid number.")


def set_salary(vault: BudgetVault):
    salary = validate_positive_number("Enter monthly salary: $")
    vault.salary = salary
    print_success(f"Salary set to {format_currency(salary)}")


def add_bill(vault: BudgetVault):
    name = input("Bill name: ").strip()
    if not name:
        print_error("Bill name cannot be empty.")
        return

    amount = validate_positive_number("Amount: $")
    vault.add_transaction(Bill(name, amount))
    print_success(f"Added {name} - {format_currency(amount)}")


def view_bills(vault: BudgetVault):
    bills = vault.get_all_transactions()
    if not bills:
        print_warning("No bills recorded.")
        return
    print_info("\nBills:")
    for i, bill in enumerate(bills, 1):
        print(f"{i}. {bill.name} - {format_currency(bill.amount)}")


def update_bill(vault: BudgetVault):
    view_bills(vault)
    bills = vault.get_all_transactions()
    if not bills:
        return
    try:
        idx = int(input("Enter bill number to update: ")) - 1
        bill = bills[idx]
        new_name = input(f"New name [{bill.name}]: ").strip() or bill.name
        amt_input = input(f"New amount [{bill.amount}]: ").strip()
        new_amount = float(amt_input) if amt_input else bill.amount
        vault.update_transaction(idx, new_name, new_amount)
        print_success("Bill updated successfully.")
    except (ValueError, IndexError):
        print_error("Invalid bill number.")


def delete_bill(vault: BudgetVault):
    view_bills(vault)
    bills = vault.get_all_transactions()
    if not bills:
        return
    try:
        idx = int(input("Enter bill number to delete: ")) - 1
        removed = vault.remove_transaction(idx)
        print_success(f"Deleted bill: {removed.name}")
    except (ValueError, IndexError):
        print_error("Invalid bill number.")


def view_summary(vault: BudgetVault):
    if not hasattr(vault, "salary") or vault.salary <= 0:
        print_error("Please set salary first.")
        return

    income = vault.salary
    expenses = [t.amount for t in vault.get_all_transactions()]
    total_expenses = sum(expenses)
    tax = flat_tax_logic(income)
    remaining = run_budget_analysis(income, expenses, flat_tax_logic)

    print("\n" + "=" * 40)
    print(f"Income:         {format_currency(income)}")
    print(f"Tax (10%):      {format_currency(tax)}")
    print(f"Total Expenses: {format_currency(total_expenses)}")
    print(f"Remaining:      {format_currency(remaining)}")

    status = get_budget_status(remaining, income)
    if "CRITICAL" in status:
        print_error(status)
    elif "WARNING" in status:
        print_warning(status)
    else:
        print_success(status)
    print("=" * 40)


def main():
    display_banner()

    vault = BudgetVault()
    storage = JSONStorage()

    while True:
        display_menu()
        choice = input("Select option: ")

        if choice == "1":
            set_salary(vault)
        elif choice == "2":
            add_bill(vault)
        elif choice == "3":
            view_bills(vault)
        elif choice == "4":
            update_bill(vault)
        elif choice == "5":
            delete_bill(vault)
        elif choice == "6":
            view_summary(vault)
        elif choice == "7":
            if hasattr(vault, "salary"):
                storage.save("trucker_user", vault.salary, vault.get_all_transactions())
                print_success("Data saved successfully.")
            print_info("Goodbye!")
            sys.exit()
        else:
            print_error("Invalid option. Please select 1-7.")


if __name__ == "__main__":
    main()