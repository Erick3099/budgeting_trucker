def format_currency(value: float) -> str:
    return f"${value:,.2f}"

def get_budget_status(remaining: float, income: float) -> str:
    if income <= 0:
        return "INCOMPLETE: No Income Data"
    
    ratio = remaining / income
    if ratio < 0:
        return "CRITICAL: Overdrawn"
    if ratio < 0.15:
        return "WARNING: Low Reserves"
    return "HEALTHY: Budget Balanced"