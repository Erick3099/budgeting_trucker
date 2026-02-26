import sys

from app.users.profile import UserProfile
from app.models import Bill
from app.engine import run_budget_analysis, flat_tax_logic, progressive_tax_logic, calculate_tax_summary
from app.payments.gateway import generate_final_receipt, format_receipt_display
from app.calculator import format_currency, get_budget_status

def main():
    print(".. BUDGET SYSTEM TRACKER ..")
    try:

        name = input("Enter Name: ")
        raw_income = input("Monthly Income: ")
        income = float(raw_income)
        user = UserProfile(name, income)

        tax_choice = input("Use Flat Tax (10%)? (y/n): ").lower()
        strategy = flat_tax_logic if tax_choice == 'y' else progressive_tax_logic

        while True:
            desc = input("\nExpense Name (or 'done' to finish): ")
            if desc.lower() == 'done': 
                break
            try:
                amt = float(input(f"Amount for {desc}: "))
                user.add_bill(Bill(desc, amt))
            except ValueError:
                print("Invalid amount. Please enter a number.")

        expense_list = [t.amount for t in user.vault.get_all_transactions()]
        total_spent = sum(expense_list)
        tax_amt = strategy(income)
        
        final_bal = run_budget_analysis(income, expense_list, strategy)
        summary = calculate_tax_summary(income, tax_amt, total_spent)

        print("\n" + "="*40)
        print(f"FINANCIAL SUMMARY FOR: {user.username.upper()}")
        print("-" * 40)
        print(f"Gross Income:    {format_currency(summary['gross_income'])}")
        print(f"Tax Deducted:    {format_currency(summary['tax_amount'])} ({summary['tax_percentage']:.1f}%)")
        print(f"Total Expenses:  {format_currency(summary['total_expenses'])}")
        print(f"Net Remaining:   {format_currency(final_bal)}")
        print(f"Budget Health:   {get_budget_status(final_bal, income)}")
        print("="*40)
        
        receipt = generate_final_receipt(user.username, final_bal)
        print(format_receipt_display(receipt, user.username))

    except ValueError:
        print("Input Error: Please ensure income and expenses are numbers.")
    except Exception as e:
        print(f"System Error: {e}")

if __name__ == "__main__":
    main()