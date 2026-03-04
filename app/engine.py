from typing import List, Callable

def run_budget_analysis(income: float, expenses: List[float], tax_callback: Callable) -> float:
    tax = tax_callback(income)
    return income - tax - sum(expenses)

def flat_tax_logic(income: float) -> float:
    return income * 0.10

def progressive_tax_logic(income: float) -> float:
    if income <= 3000: return income * 0.05
    elif income <= 6000: return income * 0.15
    return income * 0.25

def calculate_tax_summary(income: float, tax: float, expenses: float) -> dict:
    remaining = income - tax - expenses
    safe_perc = lambda val: (val / income * 100) if income > 0 else 0
    return {
        'gross_income': income,
        'tax_amount': tax,
        'tax_percentage': safe_perc(tax),
        'total_expenses': expenses,
        'expense_percentage': safe_perc(expenses),
        'remaining_balance': remaining,
        'remaining_percentage': safe_perc(remaining)
    }
