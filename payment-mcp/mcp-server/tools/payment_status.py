import sys
from pathlib import Path


BANK_SERVICE_PATH = Path(__file__).resolve().parents[2] / "bank-service"
sys.path.insert(0, str(BANK_SERVICE_PATH))

from payment_engine import bank


def payment_status(payment_id: str) -> dict:
    """Get payment status by calling the dummy bank service."""
    return bank.payment_status(payment_id)
