from app.models import Bill
def is_high_priority(bill: Bill) -> bool:
    return bill.is_fixed and bill.amount > 1000
def get_bill_category(bill: Bill) -> str:
    return "Mandatory" if bill.is_fixed else "Optional"