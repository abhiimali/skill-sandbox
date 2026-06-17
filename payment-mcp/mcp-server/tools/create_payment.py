import sys
from pathlib import Path


BANK_SERVICE_PATH = Path(__file__).resolve().parents[2] / "bank-service"
sys.path.insert(0, str(BANK_SERVICE_PATH))

from payment_engine import bank


def create_payment(from_account: str, receiver_account: str, amount: float) -> dict:
    """Create a payment by calling the dummy bank service."""
    return bank.create_payment(
        from_account=from_account,
        receiver_account=receiver_account,
        amount=amount,
    )
