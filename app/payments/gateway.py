import uuid
from datetime import datetime
from typing import Tuple
from app.calculator import format_currency

def generate_final_receipt(name: str, balance: float) -> Tuple[str, str, float]:
    """
    Generates the immutable record. 
    The logic remains identical to preserve data integrity.
    """
    transaction_id = str(uuid.uuid4())[:8].upper()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (transaction_id, timestamp, balance)

def format_receipt_display(receipt: Tuple[str, str, float], user_name: str) -> str:
    """
    Text-only receipt without ASCII borders.
    Uses simple spacing for alignment.
    """
    tid, ts, bal = receipt
    
    formatted_bal = format_currency(bal)
    
    return (
        f"\nOFFICIAL BUDGET ANALYSIS RECORD\n"
        f"{'='*31}\n"
        f"USER:       {user_name}\n"
        f"RECEIPT ID: {tid}\n"
        f"TIMESTAMP:  {ts}\n"
        f"FINAL BAL:  {formatted_bal}\n"
        f"{'='*31}\n"
    )